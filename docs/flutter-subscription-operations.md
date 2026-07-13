---
title: サブスクリプション 運用ガイド（Runbook）
---

# サブスクリプション 運用ガイド（リコンサイル・監視・障害対応・CS）

リリース後の**運用フェーズ**で必要になる手順をまとめたRunbookです。設計は[システム構成設計](flutter-subscription-system-design.md)、実装は[コード例集](flutter-subscription-code-backend.md)を前提にしています。

---

## 1. 日次リコンサイル（通知取りこぼし対策）

Webhookは**欠落し得る**前提で運用します（受信側障害・ストア側遅延・Pub/Sub設定ミス等）。DBとストアの状態を突き合わせる日次バッチが安全網です。

### 対象の抽出

| 優先度 | 対象 | 理由 |
| --- | --- | --- |
| 高 | `current_period_end < 明日` かつ `status IN (ACTIVE, GRACE_PERIOD, CANCELED)` | 期限切れ直前・直後。更新/失効の取りこぼしを1日以内に検出 |
| 中 | `status IN (BILLING_RETRY, ACCOUNT_HOLD, PAUSED)` 全件 | 回復・失効の取りこぼし検出 |
| 低 | 全ACTIVEレコードの週次全件照会 | 返金・取り消しの完全な検出（任意） |

### 手順

1. 対象レコードをストアAPIで照会（iOS: `Get All Subscription Statuses` / Android: `subscriptionsv2.get`）
2. [共通のステータスマッピング関数](flutter-subscription-code-backend.md#3-ステータスマッピングストア--db)でDB値と比較
3. 差分があれば `subscriptions` を更新し、`subscription_events` に `event_type = 'RECONCILE_FIX'` で記録
4. **差分件数をメトリクスとして記録**（多い日はWebhook側の異常を疑うシグナル）

> Android の purchaseToken はサブスク終了から**60日で照会不能**になります。失効レコードの照会は60日以内に。

---

## 2. 監視項目とアラート

| メトリクス | 取り方 | アラート目安 |
| --- | --- | --- |
| Webhook受信数（platform別・時間別） | `subscription_events` を集計 | **1時間ゼロ件**が継続（普段は更新通知が常時来る）→ 受信系の障害 |
| Webhook署名検証エラー数 | 401返却数 | 急増 → 攻撃 or 証明書/設定の破損 |
| 検証API失敗率 | `iap_receipts.verification_status = FAILED` 率 | 5%超 → ストアAPI障害 or 不正の急増 |
| リコンサイル差分件数 | 上記バッチ | 通常ほぼ0。急増 → Webhook取りこぼし |
| ストアAPIのエラー率・レイテンシ | HTTPクライアントの計測 | 5xx継続 → ストア側障害（[ステータスページ](https://developer.apple.com/system-status/)確認） |
| Apple証明書・鍵の期限 | In-App Purchase キー / サービスアカウントキー | 期限30日前に通知 |

---

## 3. 障害対応Runbook

### 3-1. Webhookが届かない（受信ゼロ）

1. **切り分け:** テスト通知を送る（iOS: Request a Test Notification API / Android: Play Console「テスト通知を送信」）
2. 届かない場合 → インフラ側: DNS・TLS証明書・LB・エンドポイントのデプロイ状態を確認
3. iOS: App Store Connect の通知URL設定を確認。**Appleは失敗時に最大5回リトライ**するため、数時間以内の復旧なら概ね自動回復
4. Android: Pub/Sub の**未配信メッセージ数**（サブスクリプションのbacklog）を確認。push失敗分はPub/Subが保持しており、**エンドポイント復旧後に自動再配信**される（デフォルト保持7日）
5. 復旧後: 障害時間帯をカバーする**臨時リコンサイル**を実行（§1の手順を対象期間全件で）

### 3-2. 誤って権利を剥奪してしまった（DB事故）

1. `subscription_events` の生ペイロード（`raw_payload`）から正しい状態を特定
2. ストアAPIで現在の状態を再取得 → `subscriptions` を修正
3. 影響ユーザー数を `subscription_events` から算出し、必要ならお詫び通知

### 3-3. ストアAPI障害（Apple/Google側）

- 検証API（`/api/subscriptions/verify`）が失敗する間、**購入は成立しているのに権利が付与されない**状態になる
- 対応: `iap_receipts` に `PENDING` で記録しておき、**復旧後に再検証するリトライキュー**を回す（購入自体はストアが保証しているため焦らない）
- ユーザーには「反映に時間がかかる場合があります」と表示

### 3-4. 大量の返金・チャーン急増

1. `subscription_events` で `REVOKED` / `VoidedPurchase` を日次集計
2. 急増時: 直近リリースの不具合（機能が使えない→返金）を最優先で疑う
3. Apple の「App Store での返金は Apple が承認」であり開発者は止められない。**原因の除去とアプリ内での先回りサポート導線**が対策

---

## 4. 返金・問い合わせ対応

### 4-1. 開発者ができること・できないこと

| | iOS | Android |
| --- | --- | --- |
| ユーザーの返金申請先 | Apple（reportaproblem.apple.com） | Google Play（購入後48時間以内）→以降は開発者にも権限 |
| 開発者による返金 | **不可**（Appleのみが返金可能） | **可**（Play Console / API から注文単位で返金・取り消し可能） |
| 返金の検知 | `REFUND` / `REVOKE` 通知 | `SUBSCRIPTION_REVOKED` / `VoidedPurchaseNotification` |

### 4-2. CS問い合わせ対応テンプレート

**「解約したのに請求された」**
> ストアのサブスクリプションは**アプリの削除では解約されません**。iOS:「設定 > Apple ID > サブスクリプション」/ Android:「Playストア > お支払いと定期購入」で解約状況をご確認ください。解約後も**現在の期間の終了日までは請求済みの期間としてご利用いただけます**（日割り返金はストアの規定によります）。

**「返金してほしい」（iOS）**
> App Store での購入の返金は Apple が承認・処理を行っています。恐れ入りますが [reportaproblem.apple.com](https://reportaproblem.apple.com) から返金をご申請ください。

**「課金されたのに使えない」**
> アプリ内の「購入を復元」をお試しください。改善しない場合は、購入時のレシート（注文番号）を添えてお問い合わせください。
> （社内手順: `iap_receipts` を注文番号/ユーザーIDで検索 → 検証失敗なら再検証、検証成功なのに権利がなければ §3-2 の手順）

**社内エスカレーション基準:** 同一事象の問い合わせが1日5件を超えたら障害として扱い、§3のRunbookへ。

---

## 5. 定例運用チェックリスト

**毎日（自動）**
- [ ] 日次リコンサイル実行・差分件数の記録
- [ ] Webhook受信数・検証失敗率のダッシュボード確認

**毎月**
- [ ] KPI集計（MRR・チャーン率・回復率。定義は[事業視点ガイド](flutter-subscription-business.md)）
- [ ] `subscription_events` の肥大化確認（古いレコードのアーカイブ）
- [ ] 猶予期間からの回復率を確認（低い場合は[UX 第10章](flutter-subscription-ux.md)の導線を見直し）

**四半期ごと**
- [ ] Apple In-App Purchase キー・Googleサービスアカウントキーの棚卸し・ローテーション
- [ ] ストアの手数料・ポリシー変更の確認（[要件定義 第1章](flutter-subscription-guide.md)の一次情報リンク）
- [ ] Billing Library / `in_app_purchase` のバージョン期限確認（毎年8月末がAndroidの公開ゲート）

## 関連ドキュメント

- [システム構成設計](flutter-subscription-system-design.md) ／ [実装コード例（バックエンド）](flutter-subscription-code-backend.md)
- [テスト・QAガイド](flutter-subscription-testing.md)（Webhook停止からの回復テスト）
- [法務・表記ガイド](flutter-subscription-legal-jp.md)

## 出典・参考リンク（公式情報）

- Apple: [App Store Server Notifications（リトライ仕様）](https://developer.apple.com/documentation/appstoreservernotifications/responding-to-app-store-server-notifications) ／ [返金の処理](https://developer.apple.com/documentation/storekit/handling-refund-notifications)
- Google: [注文の管理と返金](https://support.google.com/googleplay/android-developer/answer/2741495?hl=ja) ／ [Cloud Pub/Sub 再配信とbacklog](https://cloud.google.com/pubsub/docs/subscription-overview)

> **更新日:** 2026-07-13
