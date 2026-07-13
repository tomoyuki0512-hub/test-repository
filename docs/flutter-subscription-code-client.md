---
title: サブスクリプション実装コード例（Flutter側）
---

# サブスクリプション実装コード例 — Flutter側（`in_app_purchase`）

[要件定義資料](flutter-subscription-guide.md)・[システム構成設計](flutter-subscription-system-design.md)で定義した仕様を、`in_app_purchase`（3.3.x）で実装するコード例です。**処理の流れは[シーケンス図集](subscription-sequence-diagrams.md)の①②と対応**しています。

> バックエンド側の実装は [バックエンド編](flutter-subscription-code-backend.md) を参照。
> コードは要点を示すためのサンプルです。実際のアプリではDI・状態管理（Riverpod等）に合わせて分割してください。

---

## 0. セットアップ

```yaml
# pubspec.yaml
dependencies:
  in_app_purchase: ^3.3.0
```

- iOS: Xcode の Signing & Capabilities で **In-App Purchase** を有効化
- Android: `minSdk 21` 以上（`BILLING` パーミッションはパッケージが自動処理）
- ストア側でプロダクト（例: `com.example.app.monthly`）を登録しておく

---

## 1. 初期化と purchaseStream の購読

**最重要ポイント：`purchaseStream` の購読はアプリ起動直後に開始する**こと。購入処理中にアプリが落ちた場合や、Ask to Buy（承認待ち）の購入は、次回起動時にこのストリームへ流れてきます。購入ボタンを押した後に購読を始める実装だと、これらを取りこぼします。

```dart
import 'dart:async';
import 'package:in_app_purchase/in_app_purchase.dart';

class SubscriptionService {
  SubscriptionService(this._api); // 自前バックエンドのAPIクライアント

  final BackendApi _api;
  final InAppPurchase _iap = InAppPurchase.instance;
  StreamSubscription<List<PurchaseDetails>>? _subscription;

  static const Set<String> _productIds = {'com.example.app.monthly'};

  /// main() 直後・アプリ起動時に必ず呼ぶ
  Future<void> init() async {
    _subscription = _iap.purchaseStream.listen(
      _onPurchaseUpdated,
      onError: (Object e) => _log('purchaseStream error: $e'),
    );
  }

  void dispose() => _subscription?.cancel();
}
```

---

## 2. 商品情報の取得（価格表示）

価格は**ハードコードせず、必ずストアから取得した `price`（ローカライズ済み文字列）を表示**します。国・通貨によって価格が異なるためです。

```dart
Future<List<ProductDetails>> loadProducts() async {
  final bool available = await _iap.isAvailable();
  if (!available) {
    throw SubscriptionException('ストアに接続できません');
  }

  final ProductDetailsResponse response =
      await _iap.queryProductDetails(_productIds);

  if (response.notFoundIDs.isNotEmpty) {
    // プロダクトIDの登録漏れ・審査未通過・契約書未同意などが典型原因
    _log('not found: ${response.notFoundIDs}');
  }
  return response.productDetails; // .price に「¥980」等の表示用文字列
}
```

---

## 3. 購入フロー

サブスクリプションの購入は `buyNonConsumable()` を使います（自動更新サブスクは非消耗型として扱う）。

```dart
Future<void> buy(ProductDetails product) async {
  final PurchaseParam param = PurchaseParam(
    productDetails: product,
    applicationUserName: null, // ユーザーIDをストアに渡したい場合はハッシュ化して設定
  );
  // 戻り値 true は「購入フローを開始できた」だけ。結果は purchaseStream に届く
  await _iap.buyNonConsumable(purchaseParam: param);
}
```

> **プラン変更（Android）**: アップグレード/ダウングレードは `GooglePlayPurchaseParam(changeSubscriptionParam: ...)` で旧購入を指定します。iOSは同一サブスクリプショングループ内なら自動処理されます（[要件定義 第10章](flutter-subscription-guide.md)）。

---

## 4. purchaseStream のハンドリング（本体）

購入・復元・保留・エラーのすべてがここに届きます。**「検証 → 権利付与 → completePurchase」の順序**が重要です。

```dart
Future<void> _onPurchaseUpdated(List<PurchaseDetails> purchases) async {
  for (final PurchaseDetails purchase in purchases) {
    switch (purchase.status) {
      case PurchaseStatus.pending:
        // コンビニ払い・Ask to Buy 等。UIは「処理中」表示のみ。権利は付与しない
        _showPending();
        break;

      case PurchaseStatus.purchased:
      case PurchaseStatus.restored:
        try {
          // ① 自前バックエンドで検証（クライアントでの判定は信用しない）
          final entitlement = await _api.verifyPurchase(
            platform: Platform.isIOS ? 'ios' : 'android',
            productId: purchase.productID,
            // iOS(StoreKit 2): JWS形式のトランザクション
            // Android: purchaseToken を含むJSON
            verificationData:
                purchase.verificationData.serverVerificationData,
          );
          // ② 検証成功後に権利を反映
          _applyEntitlement(entitlement);
        } catch (e) {
          // 検証失敗時は権利を付与しない。completePurchase は呼んでよい
          // （サーバー側で iap_receipts に記録済みのため再検証可能）
          _showVerifyError();
        }
        break;

      case PurchaseStatus.error:
        // ユーザーキャンセルもここに来る（storekit2: SKError.paymentCancelled 等）
        _log('purchase error: ${purchase.error}');
        _showPurchaseError(purchase.error);
        break;

      case PurchaseStatus.canceled:
        _showCanceled();
        break;
    }

    // ③ 最後に必ず完了を通知（pending 中は呼ばない）
    if (purchase.pendingCompletePurchase) {
      await _iap.completePurchase(purchase);
    }
  }
}
```

**ここで間違えやすいポイント**

| 間違い | 何が起きるか |
| --- | --- |
| `completePurchase()` を呼ばない | Android: 3日後に自動返金・キャンセル。iOS: トランザクションがキューに残り続け、起動のたびに再配信される |
| 検証前に権利を付与 | 偽レシートによる不正利用が可能になる |
| `pending` で権利を付与 | 支払い未完了のまま機能を解放してしまう |
| ストリーム購読が遅い | 中断された購入・承認された Ask to Buy を取りこぼす |

---

## 5. 購入の復元（iOS審査要件）

設定画面などに「購入を復元」ボタンを設置します（**未設置はiOSのリジェクト対象**）。復元された購入は `PurchaseStatus.restored` として上記ハンドラに届きます。

```dart
Future<void> restore() async {
  await _iap.restorePurchases();
  // 結果は purchaseStream に restored として流れてくる。
  // 何も届かない場合＝復元対象なし。「購入が見つかりませんでした」を表示する
}
```

> 復元された購入が**別のアカウントに紐付いていた場合**の扱い（付け替え/拒否）はバックエンド側で判定します（[UX設計ガイド 第5章](flutter-subscription-ux.md)）。

---

## 6. 起動時の権利チェック

アプリ起動時・フォアグラウンド復帰時は、ストアではなく**自前バックエンド（DBが正）**に問い合わせます。解約・課金失敗・返金はWebhook経由でDBに反映済みのためです。

```dart
Future<Entitlement> fetchEntitlement() async {
  // GET /api/subscriptions/status
  return _api.getSubscriptionStatus();
}
```

```dart
// UI側: ステータスに応じた画面出し分け（UX設計ガイドの画面①〜⑩に対応）
switch (entitlement.status) {
  case 'ACTIVE':          // 通常表示
  case 'GRACE_PERIOD':    // 利用可＋「お支払いに問題があります」バナー
  case 'CANCELED':        // 利用可＋「◯月◯日まで利用できます」バナー
    return const PremiumHome();
  case 'BILLING_RETRY':
  case 'ACCOUNT_HOLD':    // 全面ブロック＋支払い更新導線
    return const PaymentBlockedScreen();
  default:                // EXPIRED / REVOKED / 未購入 → ペイウォール
    return const PaywallScreen();
}
```

---

## 7. テストの注意

実機＋Sandbox/テストトラックでの検証が前提です。手順・チェックリストは[テスト・QAガイド](flutter-subscription-testing.md)を参照してください。

## 関連ドキュメント

- [実装コード例：バックエンド編](flutter-subscription-code-backend.md)
- [シーケンス図集（購入・復元・Webhook・課金失敗・返金）](subscription-sequence-diagrams.md)
- [要件定義資料](flutter-subscription-guide.md) ／ [システム構成設計](flutter-subscription-system-design.md)

## 出典・参考リンク（公式情報）

- [in_app_purchase（pub.dev）](https://pub.dev/packages/in_app_purchase) ／ [公式サンプル](https://pub.dev/packages/in_app_purchase/example)
- [Flutter: In-app purchases overview](https://docs.flutter.dev/resources/in-app-purchases-overview)

> **更新日:** 2026-07-13（`in_app_purchase` 3.3.x 時点）
