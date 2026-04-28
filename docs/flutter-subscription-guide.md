# Flutterアプリ サブスクリプション要件定義資料（App内課金）

## 1. App内課金（IAP）の概要

### IAPとは

App内課金（In-App Purchase / IAP）とは、App Store（iOS）または Google Play（Android）のプラットフォームが提供する課金システムを経由して、アプリ内でデジタルコンテンツや機能へのアクセス権を販売する仕組みです。

課金処理はプラットフォーム側が担うため、開発者はプロダクトIDを用いて購入リクエストを送り、結果（購入成功・失敗・復元）をハンドリングするだけで済みます。

FlutterではプラットフォームごとのSDK（iOS: StoreKit2、Android: Google Play Billing Library）をDartから統一的に扱えるパッケージが提供されており、1つのコードベースでiOS/Android両対応のIAPを実装できます。

### 課金フロー（全体図）

```
ユーザー
  │
  ▼
アプリ（Flutter）
  │ 1. プロダクト情報をリクエスト（プロダクトID指定）
  ▼
App Store / Google Play
  │ 2. 価格・プロダクト情報を返却
  ▼
アプリ（購入ボタン表示）
  │ 3. 購入リクエスト
  ▼
App Store / Google Play（決済処理・認証）
  │ 4. 購入完了通知（レシート / purchaseToken）
  ▼
アプリ（権利を付与）
  │ 5.【任意】レシートをバックエンドへ送信して検証
  ▼
バックエンド → App Store Server API / Google Play Developer API
  │ 6. 検証結果を返却
  ▼
アプリ（機能・コンテンツを解放）
```

### サブスクリプション型 vs 買い切り型

| 項目 | サブスクリプション型 | 買い切り型（非消費型） |
|---|---|---|
| 課金方式 | 月額・年額で自動更新 | 1回限り |
| 収益モデル | 継続課金で安定収益 | 初回購入のみ |
| ユーザー管理 | 解約・更新・試用期間の管理が必要 | 購入後は管理不要 |
| ストア側の管理 | 自動更新・失効をプラットフォームが処理 | シンプル |
| 向いているケース | SaaS的機能・定期コンテンツ配信 | ゲームアイテム・機能アンロック |

### 手数料体系（2026年時点）

#### App Store（iOS）

| 条件 | 手数料 |
|---|---|
| 標準（年間売上100万ドル超） | 30% |
| Small Business Program（年間売上100万ドル以下） | 15% |
| サブスクリプション2年目以降 | 15%（標準でも） |

#### Google Play（Android）※2026年3月改定

2026年3月、EpicとのGoogle Play独占禁止訴訟の和解を受け、Googleは手数料を大幅に引き下げました。

| 条件 | 手数料 |
|---|---|
| 通常の新規インストールからのアプリ内課金 | 20% |
| 定期購入（サブスクリプション）の継続課金 | 10% |
| Google独自の決済システム（Google Billing）を使用 | 上記に追加5% |
| Apps Experience Program / Games Level Up 参加者 | 15%（新規インストール分） |

※ 新手数料は2026年6月30日までにEEA・UK・米国で適用開始。日本は2026年12月31日までに適用予定。

---

## 2. サブスクリプションの種類

### 2-1. サブスクリプション本体の種類

iOS と Android で、サブスクリプションの基本形式が異なります。

#### iOS（App Store）

| 種類 | 説明 | 推奨 |
|---|---|---|
| 自動更新サブスクリプション | 期間終了時に自動で更新される。最も一般的な形式 | ◎ |
| 非自動更新サブスクリプション | ユーザーが手動で更新が必要。現在は非推奨 | ✕ |

#### Android（Google Play）

Google Play Billing Library 5以降は「ベースプラン」＋「オファー」という構造になっています。

| 種類 | 説明 | 推奨 |
|---|---|---|
| 自動更新ベースプラン | 期間終了時に自動更新される標準形式 | ◎ |
| プリペイドベースプラン | ユーザーが手動で期間を延長する前払い形式 | 限定的 |
| インストールメント（分割払い） | 固定月額を一定期間分割払い（一部地域のみ） | 限定的 |

### 2-2. オファー（割引・試用）の種類

サブスクリプション本体に付加できる特典です。新規ユーザーの獲得・リテンション向上に使います。

| オファー種類 | 説明 | iOS | Android |
|---|---|---|---|
| フリートライアル | 無料期間（3日〜3年）終了後に通常料金で課金開始 | ○ | ○ |
| Pay Up Front（前払い割引） | 初回の一定期間を割引価格で一括払い（例：初月無料→年額一括） | ○ | ✕ |
| Pay As You Go（継続割引） | 初回の数ヶ月を毎月割引価格で課金 | ○ | ○（Introductory Pricing） |
| プロモーションオファー | 既存ユーザーや解約者向けの特別割引 | ○ | ○ |
| オファーコード | コード入力で特典を付与（マーケティング施策向け） | ○ | ○（Promo Codes） |

**iOS の制約：** 1つのサブスクリプショングループにつき、ユーザーが利用できるイントロダクトリーオファーは1回のみ（再購入や別グループへの移行では再利用不可）。

### 2-3. プラン構成の種類

| 構成パターン | 説明 | 例 |
|---|---|---|
| 単一プラン | 1種類のみ | 月額980円のみ |
| 月額・年額セット | 期間違いを並列提供 | 月額980円 / 年額7,800円 |
| 段階プラン（Tier） | 機能・容量で差別化した複数グレード | ベーシック / プレミアム / ビジネス |
| ファミリー共有 | 1契約で複数メンバーが利用 | iOS: Family Sharing / Android: Family Library |

### 推奨構成（新規導入時）

新規アプリへの導入であれば、**自動更新サブスクリプション + フリートライアル（7日間）の月額・年額セット**から始めるのが最もシンプルかつ効果的です。プロダクトが成熟してきた段階で段階プランやプロモーションオファーを追加するアプローチが一般的です。

---

## 3. FlutterパッケージでのIAP実装方法

### 3-1. `in_app_purchase`（Flutter公式）

**概要**

Flutterチームが公式メンテナンスするパッケージ。iOS（StoreKit / StoreKit2）とAndroid（Google Play Billing Library）の両方をひとつのAPIで扱えます。

**特徴**

- 外部サービスへの依存なし
- pub.dev の Flutter Favorite
- 低レベルAPIのため、実装量はやや多い
- サブスクリプション管理・分析機能は自前実装が必要

**向いているケース**

- バックエンドが既にあり、レシート検証を自前で行える
- RevenueCat 等の外部サービスへの依存を避けたい
- シンプルなプラン構成（1〜2プラン程度）

**セットアップ概要（pubspec.yaml）**

```yaml
dependencies:
  in_app_purchase: ^3.2.0
```

**iOS 追加設定**

`ios/Runner/Info.plist` に特別な設定は不要ですが、App Store Connect でのプロダクト登録と、Capabilities の「In-App Purchase」有効化が必要です。

**Android 追加設定**

`android/app/build.gradle` の `minSdkVersion` を 21 以上にする必要があります。Google Play Console でのプロダクト登録も必要です。

**購入フロー（概要）**

1. `InAppPurchase.instance.queryProductDetails(ids)` でプロダクト情報を取得
2. `InAppPurchase.instance.buyNonConsumable(purchaseParam)` で購入リクエスト
3. `InAppPurchase.instance.purchaseStream` で購入状態の変化をリッスン
4. `PurchaseStatus.purchased` を検知して権利を付与
5. `InAppPurchase.instance.completePurchase(purchase)` で購入完了を通知

---

### 3-2. `purchases_flutter`（RevenueCat）

**概要**

RevenueCat が提供するサードパーティSDK。IAPの複雑な処理を抽象化し、サブスクリプション管理・分析・Webhook 等の機能をクラウドで提供します。

**特徴**

- iOS / Android の差異を吸収したシンプルなAPI
- 購入履歴・権利管理をRevenueCatのサーバーが担当
- ダッシュボードでリアルタイム収益分析が可能
- Webhook でバックエンドへのイベント通知が可能
- バックエンドなしでも権利管理が完結

**向いているケース**

- バックエンドを持たない、または最小限にしたい
- 複数プラン・プロモーション管理が複雑になる見込み
- 収益分析・チャーン分析を行いたい
- 将来的に複数プラットフォームへ展開予定

**RevenueCat の料金プラン**

| プラン | 月間アクティブユーザー | 料金 |
|---|---|---|
| Free | 〜10,000 MAU | 無料 |
| Starter | 10,000〜 | $99/月〜 |
| Pro | 大規模 | 要問合せ |

**セットアップ概要（pubspec.yaml）**

```yaml
dependencies:
  purchases_flutter: ^7.0.0
```

**購入フロー（概要）**

1. `Purchases.configure(PurchasesConfiguration(apiKey))` で初期化
2. `Purchases.getOfferings()` でプロダクト一覧を取得
3. `Purchases.purchasePackage(package)` で購入
4. `CustomerInfo` から entitlement（権利）の有無を確認して機能を解放

---

### パッケージ選択基準

| 判断軸 | `in_app_purchase` | `purchases_flutter` |
|---|---|---|
| バックエンドの有無 | 自前実装が必要 | 不要（RevenueCatが管理） |
| プランの複雑さ | シンプルなら問題なし | 複雑なプランも管理しやすい |
| 分析・ダッシュボード | 不要or自前 | RevenueCatが提供 |
| 外部依存 | なし | RevenueCatに依存 |
| 実装コスト | やや高め | 低い |
| コスト | 無料 | MAUが増えると有料 |

---

## 4. iOS / Android 各種相違点

| 項目 | iOS (App Store) | Android (Google Play) |
|---|---|---|
| 決済SDK | StoreKit / StoreKit2 | Google Play Billing Library |
| Flutterラッパー | `in_app_purchase` iOS実装 | `in_app_purchase` Android実装 |
| サンドボックステスト | Apple ID のSandboxテスターを作成 | テストトラック（クローズドα等）＋ライセンステスター登録 |
| 手数料 | 15〜30% | 15〜30%（初年度15%） |
| 外部決済 | デジタルコンテンツは原則禁止 | Alternative Billing の選択肢あり |
| レシート検証API | App Store Server API | Google Play Developer API |
| 推奨SDK | StoreKit2（iOS15+） | Billing Library 6+ |
| 解約導線 | アプリ内にサブスクリプション管理ページへの導線必須 | Google Play のサブスク管理ページへの導線必須 |
| プロモーション機能 | Introductory Offer / Promotional Offer | Introductory Price / Promo Codes |
| ファミリー共有 | Family Sharing（オプトイン） | Family Library（オプトイン） |
| オフライン時の挙動 | StoreKit が自動ハンドリング | Billing Library が自動ハンドリング |
| プロダクト管理画面 | App Store Connect | Google Play Console |
| 審査タイミング | プロダクト登録はアプリ審査と同時 | プロダクト登録はアプリとは独立して可能 |

### 注意点：テスト方法の違い

**iOS（Sandbox）**
- App Store Connect で Sandbox テスターアカウントを作成
- 実機で Sandbox アカウントにサインインしてテスト
- 更新間隔が短縮される（例：1ヶ月 → 5分）

**Android（テスト）**
- Google Play Console でライセンステスターのメールアドレスを登録
- 内部テストトラックに配布してテスト
- テスト用の自動更新間隔短縮あり（1ヶ月 → 5分）

---

## 5. ストア申請・審査の制約と注意点

### App Store（iOS）

- **外部決済の禁止**：デジタルコンテンツ・機能へのアクセスはIAP必須。Webサイトへの誘導で外部決済を促すことも禁止
- **サブスクリプション説明文**：何が含まれるか、価格、更新頻度を明確に記載する必要がある
- **解約方法の明示**：アプリ内にサブスクリプション管理ページ（`itms-apps://apps.apple.com/account/subscriptions`）への導線が必須
- **フリートライアルの表示**：試用終了後に課金される旨を明確に表示する義務がある
- **StoreKit2 推奨**：iOS 15以降はStoreKit2 APIが推奨。`in_app_purchase` パッケージは内部でStoreKit2を使用

### Google Play（Android）

- **定期購入の説明**：価格・更新頻度・解約方法をアプリ内に明示する義務がある
- **解約方法の明示**：Google Play のサブスクリプション管理ページへの導線、またはアプリ内での解約フローが必要
- **Alternative Billing**：一部の地域でGoogle Play以外の決済も認められているが、複雑なため通常は使用しない

### 共通事項

- **価格表示**：税込み価格の表示、自動更新の告知が必要
- **フリートライアル**：試用期間終了後の課金開始タイミングを事前に明示する義務がある
- **返金ポリシー**：各プラットフォームの返金ポリシーに準拠する（開発者が個別に返金処理する場合を除く）

---

## 6. バックエンド要件（レシート検証）

### レシート検証とは

購入完了時にプラットフォームから発行されるレシート（証明書）を、サーバー側でプラットフォームのAPIを使って検証する仕組みです。不正な購入を防ぐために重要です。

### 検証が必要なケース

| ケース | 検証要否 |
|---|---|
| アプリ内のみで権利管理（オフライン利用） | 不要 |
| サーバーリソースへのアクセス制御が必要 | **必要** |
| 複数デバイス・複数プラットフォームで共通アカウント | **必要** |
| 不正利用を厳密に防ぎたい | **必要** |

### サーバーサイド検証の仕組み

**iOS（App Store Server API）**
1. アプリがレシートをバックエンドに送信
2. バックエンドが Apple の App Store Server API に問い合わせ
3. 検証結果（有効・無効・有効期限）を受け取る
4. 権利（entitlement）をユーザーに付与

**Android（Google Play Developer API）**
1. アプリが `purchaseToken` をバックエンドに送信
2. バックエンドが Google Play Developer API に問い合わせ
3. サブスクリプションの状態を確認
4. 権利をユーザーに付与

### RevenueCat を使う場合

RevenueCat がレシート検証・権利管理をすべて担当するため、**バックエンドは不要**になります。バックエンドが必要な場合も、Webhook を通じてRevenueCatからイベント通知を受け取る形で実装できます。

### entitlement（権利）管理の考え方

「ユーザーがどの機能・コンテンツにアクセスできるか」を管理する概念です。

- `in_app_purchase` の場合：購入状態をアプリまたは自前バックエンドで管理
- RevenueCat の場合：RevenueCatのダッシュボード上でentitlementを定義し、SDKで参照するだけで管理可能

---

## 7. 要件まとめ・判断チェックリスト

### パッケージ選択チェックリスト

以下の項目で「はい」が多い場合は **RevenueCat（purchases_flutter）** を推奨：

- [ ] バックエンドを持たない、または最小限にしたい
- [ ] 複数のサブスクリプションプランを管理する
- [ ] 収益・チャーンの分析ダッシュボードが欲しい
- [ ] Webhook でバックエンドにイベントを飛ばしたい
- [ ] 将来的に Web / その他プラットフォームへの展開を考えている

以下の項目で「はい」が多い場合は **in_app_purchase（公式）** を推奨：

- [ ] バックエンドが既にあり、レシート検証を自前で行える
- [ ] 外部サービスへの依存を最小限にしたい
- [ ] プランがシンプル（1〜2プラン）
- [ ] RevenueCatの料金を回避したい（MAU増加後）

### バックエンド有無の判断基準

| 要件 | バックエンド |
|---|---|
| 機能アクセスをアプリ内のみで管理 | 不要 |
| サーバーリソース（API等）へのアクセス制御 | **必要** |
| 複数デバイス間での権利同期 | **必要** |
| 不正利用防止のレシート検証 | **必要**（RevenueCatで代替可） |

### iOS / Android 両対応に必要な設定一覧

| 設定項目 | iOS | Android |
|---|---|---|
| ストアコンソールでのプロダクト登録 | App Store Connect | Google Play Console |
| Capabilities / Permission の有効化 | In-App Purchase を有効化 | `BILLING` パーミッションを追加 |
| サンドボックス / テストアカウントの準備 | Sandbox テスター作成 | ライセンステスター登録 |
| 解約導線のUI実装 | 管理ページへのリンク | 管理ページへのリンク |
| フリートライアルの表示 | 購入前に明示 | 購入前に明示 |
| 審査対応 | メタデータ・スクリーンショット準備 | プロダクト説明文の準備 |
