# Flutterアプリ サブスクリプション システム構成設計

## 前提

| 項目 | 内容 |
|---|---|
| クライアント | Flutter（iOS / Android） |
| バックエンド | Java API（既存） |
| DB | PostgreSQL（既存。既存テーブルは変更なし） |
| IAPパッケージ | `in_app_purchase`（Flutter公式） |
| インフラ | 既存環境に準拠 |

RevenueCatは使わないため、レシート検証・サブスクリプション状態管理はすべて自前実装する。

---

## 1. 全体構成

```
【クライアント層】
  Flutter App（iOS / Android）
       │ HTTPS REST
       ▼
【バックエンド層】
  既存 Java API サーバー（新規モジュールを追加）
  ├── IAPController          … Flutter向けエンドポイント
  ├── AppleWebhookController … App Store通知受信
  ├── GooglePubSubController … Google Pub/Sub受信
  ├── ReceiptVerificationService … 検証ロジック
  └── SubscriptionService    … 権利管理ロジック
       │
       ├──────────────────────────────┐
       ▼                              ▼
【DB層】                       【外部サービス】
  PostgreSQL（既存に追加）         ├── App Store Server API（JWT認証）
  ├── subscriptions                └── Google Play Developer API（OAuth2）
  ├── subscription_events
  └── iap_receipts

【Webhook受信】
  iOS:     App Store Server → POST /webhook/apple（APIエンドポイントに直接HTTPS POST）
  Android: Google Play → Google Cloud Pub/Sub（トピック）→ Push配信 → POST /webhook/google/pubsub
           ※ Google PlayはAPIに直接POSTしない。Google Cloud Pub/Subが必ず中間に入る
           ※ インフラがAWSであってもGoogle Cloud Pub/Subのセットアップは必須
```

### 通知受信方式の比較

| | iOS | Android |
|---|---|---|
| 通知の送り元 | Apple が直接 HTTPS POST | Google Cloud Pub/Sub 経由 |
| 必要なインフラ | APIエンドポイントのみ | **Google Cloud Pub/Sub ＋ APIエンドポイント** |
| Google Cloudアカウント | 不要 | **必須**（インフラがAWSでも不要にはできない） |
| エンドポイントへの到達経路 | Apple → API | Google Play → Pub/Sub トピック → Push サブスクリプション → API |

---

## 2. 新規DBテーブル設計

既存PostgreSQLに以下の3テーブルを追加する。既存テーブルへの変更は不要。

### 2-1. `subscriptions`（権利テーブル）

ユーザーのサブスクリプション有効状態を管理する中心テーブル。

| カラム | 型 | 説明 |
|---|---|---|
| id | BIGSERIAL PK | — |
| user_id | BIGINT NOT NULL | 既存ユーザーテーブルへのFK |
| platform | VARCHAR(10) | `'ios'` / `'android'` |
| product_id | VARCHAR(255) | プロダクトID（例: `com.example.app.monthly`） |
| original_transaction_id | VARCHAR(255) | iOS専用。ライフサイクル全体の追跡キー |
| purchase_token | TEXT | Android専用。**更新のたびに新しい値が発行される**ため、`SUBSCRIPTION_RENEWED`受信時に最新値へ更新する |
| status | VARCHAR(30) | 下記ステータス定義を参照 |
| current_period_start | TIMESTAMPTZ | 契約期間の開始 |
| current_period_end | TIMESTAMPTZ | 契約期間の終了（= 次回課金日） |
| grace_period_end | TIMESTAMPTZ | Grace Period終了日時（課金失敗時のみ設定） |
| auto_renew_status | BOOLEAN DEFAULT TRUE | 自動更新フラグ |
| created_at | TIMESTAMPTZ DEFAULT NOW() | — |
| updated_at | TIMESTAMPTZ DEFAULT NOW() | — |

**インデックス:**
- `UNIQUE(user_id, platform)` — 1ユーザーにつきプラットフォームごとに1レコード
- `INDEX(original_transaction_id)` — iOS Webhookの検索用
- `INDEX(purchase_token)` — Android Webhookの検索用
- `INDEX(status, current_period_end)` — 期限切れバッチ処理用

**AndroidのpurchaseToken更新について:**

Androidでは更新のたびに新しい`purchaseToken`が発行される。新しいトークンには`linkedPurchaseToken`フィールドで前のトークンへの参照が含まれる。

| 更新回数 | orderId | purchaseToken |
|---|---|---|
| 初回購入 | GPA.xxx-001 | token_AAA |
| 1回目更新 | GPA.xxx-002 | token_BBB（linkedPurchaseToken: token_AAA） |
| 2回目更新 | GPA.xxx-003 | token_CCC（linkedPurchaseToken: token_BBB） |

`SUBSCRIPTION_RENEWED`受信時に`subscriptions.purchase_token`を新しいトークンへ上書き更新する。

**AndroidのorderIdについて:**

`orderId`はiOSの`transaction_id`に相当する「1回の課金ごとのユニークID」。サブスクリプション追跡の主キーとしては不要（`purchase_token`で追跡可能）だが、問い合わせ対応・請求照合に役立つため`subscription_events.raw_payload`（JSONB）にWebhookペイロードごと保持する。サポート対応が多い場合は専用カラムの追加を検討する。

**statusの定義値:**

| 値 | 意味 | アクセス可否 |
|---|---|---|
| `ACTIVE` | 有効（課金正常） | ○ |
| `GRACE_PERIOD` | 課金失敗・猶予期間中 | ○（維持） |
| `CANCELED` | 解約済み（期間内） | ○（期間終了まで） |
| `BILLING_RETRY` | iOS: Billing Retry中 | ✗ |
| `ACCOUNT_HOLD` | Android: Account Hold中 | ✗ |
| `PAUSED` | Android: 一時停止中 | ✗ |
| `EXPIRED` | 失効 | ✗ |
| `REVOKED` | 強制取り消し | ✗ |

### 2-2. `subscription_events`（Webhookログ）

ストアから受信した全Webhookイベントを記録する。状態遷移の監査証跡として使う。

| カラム | 型 | 説明 |
|---|---|---|
| id | BIGSERIAL PK | — |
| subscription_id | BIGINT | subscriptions.id へのFK（特定不能時はNULL） |
| platform | VARCHAR(10) | — |
| event_type | VARCHAR(100) | iOS: notificationType / Android: 定数名 |
| event_subtype | VARCHAR(100) | iOS: subtype / Android: NULL |
| original_transaction_id | VARCHAR(255) | iOS専用 |
| purchase_token | TEXT | Android専用 |
| raw_payload | JSONB | 受信した元ペイロード（検証・デバッグ用） |
| processed_at | TIMESTAMPTZ DEFAULT NOW() | — |
| is_duplicate | BOOLEAN DEFAULT FALSE | 冪等性確認フラグ |

**インデックス:**
- `INDEX(original_transaction_id, event_type)`
- `INDEX(purchase_token, event_type)`
- `INDEX(processed_at)`

### 2-3. `iap_receipts`（検証記録）

Flutterから送信されたレシート・トークンの検証結果を記録する。二重検証の防止と障害追跡に使う。

| カラム | 型 | 説明 |
|---|---|---|
| id | BIGSERIAL PK | — |
| user_id | BIGINT | — |
| platform | VARCHAR(10) | — |
| transaction_id | VARCHAR(255) UNIQUE | iOS: transactionId |
| original_transaction_id | VARCHAR(255) | iOS: originalTransactionId |
| purchase_token | TEXT | Android |
| product_id | VARCHAR(255) | — |
| verification_status | VARCHAR(20) | `SUCCESS` / `FAILED` / `PENDING` |
| verification_response | JSONB | ストアAPIのレスポンス |
| verified_at | TIMESTAMPTZ | 検証完了日時 |
| created_at | TIMESTAMPTZ DEFAULT NOW() | — |

---

## 3. 新規APIエンドポイント

### 3-1. Flutter向け

すべて既存の認証機構（JWT Bearer Token等）を通過した上でアクセスする。

#### POST `/api/subscriptions/verify`

購入完了後にFlutterから呼び出す。レシート/トークンをストアAPIで検証し権利を付与する。

**処理フロー:**
1. `iap_receipts` で重複チェック（二重検証防止）
2. ストアAPIで検証（App Store Server API or Google Play Developer API）
3. 検証結果を `iap_receipts` に記録
4. 検証成功なら `subscriptions` をUPSERT（status=ACTIVE）
5. Flutter側で `completePurchase()` を呼ぶよう結果を返す（**Android必須: 3日以内に確認しないと自動キャンセル**）

#### GET `/api/subscriptions/status`

アプリ起動・画面遷移時に現在の権利状態を取得する。DBを正（Single Source of Truth）として扱い、ストアAPIへの問い合わせは行わない。

**アクセス権付与の判定条件:**
```sql
status IN ('ACTIVE', 'GRACE_PERIOD', 'CANCELED')
AND current_period_end > NOW()
```

#### POST `/api/subscriptions/restore`

「購入を復元する」操作時（iOS審査要件）。App Store Server APIで状態を取得しDBを同期する。

### 3-2. Webhook受信エンドポイント

認証不要（外部から到達できること）だが、受信後に必ず真正性を検証する。

#### POST `/webhook/apple`（iOS）

AppleがこのエンドポイントにHTTPSで直接POSTする。APIエンドポイントを用意するだけでよい。

- Body: `{ "signedPayload": "<JWS文字列>" }`
- 処理は非同期化し、**HTTP 200を即時返却**する（Appleは受信失敗時に最大6回リトライする）
- 処理フロー: JWS署名検証 → ペイロードデコード → `subscription_events`にログ → `subscriptions`を更新

#### POST `/webhook/google/pubsub`（Android）

Google PlayはこのエンドポイントにはPOSTしない。**Google Cloud Pub/SubのPush配信**がこのエンドポイントを呼び出す。

```
Google Play
  └→ Google Cloud Pub/Sub（トピック）  ← Google Cloudのセットアップが必要
        └→ Push サブスクリプション
              └→ POST /webhook/google/pubsub（APIエンドポイント）
```

- Body: Pub/Sub Push形式（`message.data`にBase64エンコードされた通知JSON）
- **HTTP 204**を返す（Pub/Subは2xxで成功とみなす）
- 処理フロー: Bearer Token検証 → Base64デコード → Google Play Developer APIで最新状態を取得 → `subscription_events`にログ → `subscriptions`を更新

---

## 4. 外部サービス連携

### 4-1. App Store Server API（iOS）

**認証方式:** JWT（ES256）

**App Store Connectから取得するもの:**
- Issuer ID
- Key ID
- Private Key（.p8ファイル。取得後は再ダウンロード不可）

**JWT生成ルール:**
- Algorithm: ES256
- `iss`: Issuer ID
- `aud`: `"appstoreconnect-v1"`
- `bid`: アプリのBundle ID
- `exp`: 現在時刻 + 60秒（最大1時間だが短く設定推奨）

**主要エンドポイント:**

| 用途 | URL |
|---|---|
| サブスク状態取得 | GET `https://api.storekit.itunes.apple.com/inApps/v1/subscriptions/{originalTransactionId}` |
| トランザクション履歴 | GET `https://api.storekit.itunes.apple.com/inApps/v1/history/{transactionId}` |
| Sandbox用ベースURL | `https://api.storekit-sandbox.itunes.apple.com/...` |

### 4-2. Google Play Developer API（Android）

**認証方式:** OAuth2サービスアカウント

**セットアップ手順:**
1. Google Cloud ConsoleでAndroid Developer APIを有効化
2. サービスアカウントを作成しJSON鍵をダウンロード
3. Google Play Consoleの「ユーザーとアクセス」でサービスアカウントに「財務データの閲覧」権限を付与

**主要エンドポイント:**

| 用途 | URL |
|---|---|
| サブスク状態取得（推奨） | GET `.../subscriptionsv2/tokens/{purchaseToken}` |
| 強制取り消し | POST `.../subscriptions/{productId}/tokens/{token}:revoke` |

### 4-3. Google Cloud Pub/Sub セットアップ

```
Google Play Console（通知設定）
  └→ Pub/Sub トピック
        └→ Push サブスクリプション（OIDCトークン認証）
              └→ POST /webhook/google/pubsub
```

**手順:**
1. Pub/Subトピックを作成
2. `google-play-developer-notifications@system.gserviceaccount.com` に「パブリッシャー」ロールを付与
3. Push型サブスクリプションを作成（エンドポイント: `/webhook/google/pubsub`、OIDC認証を有効化）
4. Google Play Consoleの収益化設定でトピックのリソース名を登録

---

## 5. セキュリティ考慮点

### 5-1. Apple Webhook（JWS検証）

1. JWSを分割し、Headerの`x5c`から証明書チェーンを取得
2. 証明書チェーンが**Apple Root CA（G3）**に連鎖していることを検証
3. 証明書の有効期限を確認
4. リーフ証明書の公開鍵でSignatureを検証
5. `environment`が`PRODUCTION`であることを確認（本番環境）
6. `notificationUUID`を一定期間キャッシュし、重複処理をスキップ（`is_duplicate`フラグを活用）

### 5-2. Google Pub/Sub（Bearer Token検証）

1. AuthorizationヘッダーのBearerトークンを取り出す
2. Google公開鍵（`https://www.googleapis.com/oauth2/v3/certs`）で検証
3. `iss`が`accounts.google.com`であることを確認
4. `aud`がエンドポイントURLと一致することを確認

### 5-3. 共通事項

| 項目 | 対応方針 |
|---|---|
| 通信 | Flutter→API間はHTTPS（TLS 1.2以上）必須 |
| ログ出力 | purchaseToken / transactionIdをアプリケーションログ（ファイル・収集サービス）に出力しない。アクセス制御が緩いログ環境では漏洩リスクがあるため |
| DB保存 | DBへの保存はログ出力とは別。アクセス制御された環境のため保存は必要かつ適切（`iap_receipts`の`transaction_id`はUNIQUE制約による二重検証防止に必須） |
| 入力値検証 | FlutterからのproductIdをそのまま権利付与に使わない。必ずストアAPIの検証結果を正とする |
| シークレット管理 | Apple .p8 / Googleサービスアカウント JSONはGit管理外。環境変数またはシークレット管理サービスで保管 |
| レート制限 | `/api/subscriptions/verify` にユーザーIDベースのレート制限を設ける |

---

## 6. WebhookイベントとDBステータスの対応

### 6-1. iOS

| notificationType / subtype | status更新 |
|---|---|
| `SUBSCRIBED / INITIAL_BUY` | `ACTIVE`、current_period更新 |
| `DID_RENEW` | `ACTIVE`、current_period更新 |
| `DID_RENEW / BILLING_RECOVERY` | `ACTIVE`（課金回復） |
| `DID_FAIL_TO_RENEW / GRACE_PERIOD` | `GRACE_PERIOD`、grace_period_end設定 |
| `GRACE_PERIOD_EXPIRED` | `BILLING_RETRY` |
| `DID_CHANGE_RENEWAL_STATUS / AUTO_RENEW_DISABLED` | `CANCELED`、auto_renew_status=false |
| `DID_CHANGE_RENEWAL_STATUS / AUTO_RENEW_ENABLED` | auto_renew_status=true |
| `EXPIRED` | `EXPIRED` |
| `REFUND` | `REVOKED` |

### 6-2. Android

| notificationType | status更新 |
|---|---|
| `SUBSCRIPTION_PURCHASED` (4) | `ACTIVE` |
| `SUBSCRIPTION_RENEWED` (2) | `ACTIVE`、current_period更新 |
| `SUBSCRIPTION_IN_GRACE_PERIOD` (6) | `GRACE_PERIOD` |
| `SUBSCRIPTION_ON_HOLD` (5) | `ACCOUNT_HOLD` |
| `SUBSCRIPTION_RECOVERED` (1) | `ACTIVE`（課金回復） |
| `SUBSCRIPTION_CANCELED` (3) | `CANCELED` |
| `SUBSCRIPTION_RESTARTED` (7) | auto_renew_status=true |
| `SUBSCRIPTION_PAUSED` (10) | `PAUSED` |
| `SUBSCRIPTION_EXPIRED` (13) | `EXPIRED` |
| `SUBSCRIPTION_REVOKED` (12) | `REVOKED` |

---

## 7. 実装上の重要注意点

| 項目 | 内容 |
|---|---|
| `completePurchase()` 必須 | Androidは購入確認を3日以内に完了しないと自動キャンセル。`/verify`のレスポンスを受け取った後、Flutter側で必ず呼ぶ |
| Webhookの冪等性 | 同一イベントが複数回届く（Appleは最大6回リトライ）。`notificationUUID`と`is_duplicate`フラグで重複処理を防ぐ |
| DBを正とする | アプリ起動時の権利確認はDBから行う。ストアAPIへの問い合わせはWebhook未着のフォールバックと「購入を復元する」操作時のみ |
| Grace Period有効化 | iOSはApp Store Connectで手動ON（デフォルトOFF）。フリートライアルを使う場合は「無料オファーからの移行も含む」オプションもONにする |
| `originalTransactionId`の保持 | iOS全ライフサイクルの追跡キー。初回購入時に必ずDB保存 |
| 期限切れの定期チェック | Webhookは必達でない。日次バッチで`current_period_end`が過去のレコードをストアAPIで再確認し状態を同期する |
| 環境分離 | AppleはSandbox、GoogleはテストトラックをDev/Staging環境で使用。本番とSandboxのWebhookエンドポイントを分離する |

---

## 参照ドキュメント

- `docs/flutter-subscription-guide.md` — IAP要件定義資料
- `docs/flutter-subscription-events.md` — iOS/Androidイベント一覧
