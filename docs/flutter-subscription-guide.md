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

- **最新バージョン（2026年4月時点）：** 3.2.3
- **pub.dev：** Flutter Favorite 認定パッケージ

**概要**

Flutterチームが公式メンテナンスするパッケージ。iOS（StoreKit2）とAndroid（Google Play Billing Library）を統一APIで扱えます。プラットフォーム固有のAPIが必要な場合は、`store_kit_wrappers`（iOS）・`billing_client_wrappers`（Android）でより細かい制御も可能です。

**特徴**

- 外部サービスへの依存なし
- 低レベルAPIのため、実装量はやや多め（購入状態の管理・エラーハンドリングを自前で行う）
- サブスクリプション管理・分析機能は自前実装が必要
- 将来的な外部依存を排除したい場合に最適

**向いているケース**

- バックエンドが既にあり、レシート検証を自前で行える
- RevenueCat 等の外部サービスへの依存を避けたい
- プラン構成がシンプル（1〜3プラン程度）

**セットアップ（pubspec.yaml）**

```yaml
dependencies:
  in_app_purchase: ^3.2.3
```

**iOS 追加設定**

Xcode の Signing & Capabilities で「In-App Purchase」を有効化し、App Store Connect でサブスクリプションプロダクトを登録する必要があります。

**Android 追加設定**

`android/app/build.gradle` の `minSdk` を 21 以上に設定し、Google Play Console でサブスクリプションプロダクトを登録します。`AndroidManifest.xml` への `BILLING` パーミッション追加は不要（パッケージが自動で処理）。

**購入フロー（概要）**

```
1. InAppPurchase.instance.queryProductDetails({productId}) でプロダクト情報を取得
2. InAppPurchase.instance.buyNonConsumable(PurchaseParam) で購入リクエスト
3. InAppPurchase.instance.purchaseStream をリッスンして購入状態の変化を受け取る
4. PurchaseStatus.purchased を検知 → 権利を付与
5. InAppPurchase.instance.completePurchase(purchase) で購入完了を通知（必須）
```

**注意点：** `completePurchase()` を呼ばないと Android では購入がキャンセル扱いになります（3日以内に呼ばないと自動キャンセル）。

---

### 3-2. `purchases_flutter`（RevenueCat）

- **最新バージョン（2026年4月時点）：** 8.x系
- **対応最小バージョン：** iOS 13.0+、Android SDK 21+

**概要**

RevenueCat が提供するサードパーティSDK。IAPの複雑な処理を抽象化し、サブスクリプション管理・分析・Webhook 等の機能をクラウドで提供します。バックエンドなしでも権利管理が完結するのが最大の強みです。

**特徴**

- iOS / Android の差異を吸収したシンプルなAPI（プラットフォームごとの実装分岐が不要）
- 購入履歴・権利管理・レシート検証をRevenueCatのサーバーが担当
- ダッシュボードでリアルタイムの収益・チャーン分析が可能
- Webhook でサブスクリプションイベントをバックエンドへ通知可能
- entitlement（権利）の概念で複数プランを一元管理

**向いているケース**

- バックエンドを持たない、または最小限にしたい
- 複数プランやプロモーション管理が複雑になる見込み
- 収益分析・チャーン分析をしたい
- 実装工数を削減したい

**RevenueCat の料金（2026年時点）**

| 月間売上（MTR） | 料金 |
|---|---|
| $2,500 以下 | **無料**（本番環境でフル機能利用可） |
| $2,500 超の部分 | **1%**（例：MTR $10,000 なら $75/月） |
| エンタープライズ | ボリューム割引あり（要問合せ） |

無料枠でも SDK・レシート検証・REST API・Webhook・ダッシュボードがすべて使えます。

**セットアップ（pubspec.yaml）**

```yaml
dependencies:
  purchases_flutter: ^8.0.0
```

**購入フロー（概要）**

```
1. Purchases.configure(PurchasesConfiguration(apiKey)) でSDK初期化
2. Purchases.getOfferings() でプロダクト一覧（Offering）を取得
3. Purchases.purchasePackage(package) で購入
4. CustomerInfo.entitlements.active でentitlementの有無を確認 → 機能を解放
```

---

### パッケージ選択基準

| 判断軸 | `in_app_purchase` | `purchases_flutter`（RevenueCat） |
|---|---|---|
| バックエンドの有無 | 自前実装が必要 | 不要（RevenueCatが管理） |
| プランの複雑さ | シンプルなら問題なし | 複雑なプランも管理しやすい |
| 分析・ダッシュボード | 不要 or 自前実装 | RevenueCatが提供 |
| 外部サービス依存 | なし | RevenueCatに依存 |
| 実装コスト | やや高め | 低い |
| コスト | 無料 | 月間売上$2,500超から1%課金 |
| iOS/Android の差異吸収 | 部分的（コード分岐が必要な場合も） | ほぼ完全に吸収 |

---

## 4. iOS / Android 各種相違点

### 4-1. 主要な差異一覧

| 項目 | iOS (App Store) | Android (Google Play) |
|---|---|---|
| ネイティブ決済SDK | **StoreKit2**（StoreKit1はWWDC24でdeprecated） | **Google Play Billing Library 7+**（7.0未満は2025年8月以降に公開不可） |
| Flutterラッパー | `in_app_purchase`（iOS実装） | `in_app_purchase`（Android実装） |
| サブスクリプション管理画面 | App Store Connect | Google Play Console |
| 手数料 | 15〜30%（Small Business Program適用時15%） | 10〜20%（2026年3月改定）|
| 外部決済 | デジタルコンテンツは原則禁止（EU除く） | Alternative Billing あり（地域によって選択可） |
| レシート形式 | JWS（JSON Web Signature）形式のトランザクション | purchaseToken（文字列） |
| レシート検証API | App Store Server API | Google Play Developer API |
| プロダクト登録タイミング | アプリ審査と同時に申請 | アプリとは独立して登録・審査可能 |
| 解約導線 | サブスク管理ページ（`itms-apps://...`）への導線必須 | Google Play サブスク管理ページへの導線必須 |
| プロモーション機能 | Introductory Offer / Promotional Offer | Introductory Price / Promo Codes |
| ファミリー共有 | Family Sharing（オプトイン） | Family Library（オプトイン） |
| オフライン時 | StoreKit が自動ハンドリング | Billing Library が自動ハンドリング |
| 最低OS要件（2026年） | iOS 13+（purchases_flutter）/ iOS 15+（StoreKit2直接利用） | Android SDK 21+（Android 5.0） |

### 4-2. SDKバージョンに関する重要事項

#### iOS：StoreKit1 の deprecated

- WWDC 2024 にて Apple が StoreKit1 API を正式に deprecated
- 新機能追加は StoreKit2 のみ。今後はStoreKit2への移行が必須
- `in_app_purchase` パッケージは内部でStoreKit2対応を進めている
- StoreKit2 は **iOS 15 以上が必要**（iOS 13/14 サポートが必要な場合は要注意）

#### Android：Google Play Billing Library 7 の義務化

- **2025年8月31日以降**、Google Play Console は Billing Library 7.0 未満を使用したアプリの更新を拒否
- `in_app_purchase` の最新バージョンは Billing Library 7 に対応済み
- 既存アプリは早急に最新パッケージへの更新が必要
- Billing Library 7 でのサブスクリプション構造：`SubscriptionOfferDetails`（ベースプラン + オファー）

### 4-3. テスト方法の違い

#### iOS（Sandbox テスト）

| 手順 | 内容 |
|---|---|
| 1 | App Store Connect → ユーザーとアクセス → Sandbox テスターを作成 |
| 2 | 実機の「設定 → App Store → Sandbox アカウント」でサインイン |
| 3 | アプリからIAPをテスト |
| 更新間隔 | 1ヶ月 → 5分、1年 → 1時間（自動短縮） |

**注意点：** シミュレーターではIAPのテストが制限あり（実機推奨）。Xcode の StoreKit Testing を使えばオフラインでのモックテストも可能。

#### Android（テストトラック）

| 手順 | 内容 |
|---|---|
| 1 | Google Play Console → 設定 → ライセンステスター にメールアドレスを登録 |
| 2 | 内部テストトラックにアプリをアップロード |
| 3 | テスターのアカウントで実機テスト |
| 更新間隔 | 1ヶ月 → 5分、1年 → 30分（自動短縮） |

**注意点：** テストはGoogle Playに一度アップロードが必要（ローカルビルドのみでは不可）。エミュレーターでもPlay Storeがインストールされていれば一部テスト可能。

---

## 5. ストア申請・審査の制約と注意点

### 5-1. App Store（iOS）

#### サブスクリプション提供の要件

- **継続的な価値の提供が必要：** サブスクリプションは「定期的に更新されるコンテンツ」「SaaS機能」「クラウド機能」など、継続的な価値を提供するものに限る。単なる機能アンロックを月額課金にすることは審査で否認される可能性がある
- **最低期間：** サブスクリプション期間は7日以上であること
- **全デバイス対応：** 同一Appleアカウントの全デバイスでサブスクリプションが有効になるよう実装すること

#### 決済ルール

- **IAPの強制：** デジタルコンテンツ・機能へのアクセスは必ずIAPを使用する。アプリ内や通知でWebへ誘導して外部決済を促すことも禁止（EUは例外あり）
- **代替決済UIの禁止：** 「より安く購入できます」といったIAP以外の決済を示唆する表示も禁止

#### 表示・UI の義務

- **価格・条件の明示：** 購入前に価格・更新頻度・解約方法をユーザーへ明示する義務がある
- **解約導線：** アプリ内にサブスクリプション管理ページへのリンクを設置する必要がある
  - URL: `itms-apps://apps.apple.com/account/subscriptions`
- **フリートライアルの告知：** 試用終了後に課金が開始される旨を事前に明示する義務がある

#### 技術要件（2026年時点）

- **⚠️ 2026年4月28日以降：** App Store Connect へのアップロードには **iOS & iPadOS 26 SDK（Xcode 26）以上**でのビルドが必須
- **StoreKit1 の deprecated：** 新規実装はStoreKit2を使用すること（WWDC24で正式deprecated）
- **StoreKit2 最低OS：** iOS 15以上が必要

---

### 5-2. Google Play（Android）

#### サブスクリプション提供の要件

- **明確な説明：** 定期購入の内容（価格・更新頻度・何を提供するか）をアプリ内に分かりやすく明示する義務がある
- **フリートライアルの告知：** 試用期間終了後の課金開始を事前に明示する

#### 解約導線（2026年要件）

- **アプリ内解約フローの提供が義務化：** ユーザーがアプリ内またはWebサイトで簡単に解約できるオンラインの方法を提供しなければならない（Google Playの管理画面への誘導だけでは不十分になる可能性）
- **解約後の扱い：** 解約は次の請求期間の開始時に適用（現期間中は継続して使える）

#### 決済ルール

- **Alternative Billing：** 2026年以降、米国など一部地域でGoogle Pay以外の決済も条件付きで認められる。ただし実装が複雑なため、通常はGoogle Play Billing Library一択で対応する

#### 技術要件

- **Billing Library 7.0以上が必須：** 2025年8月31日以降、旧バージョン使用アプリのアップデートは拒否される

---

### 5-3. 共通の注意事項

| 項目 | 内容 |
|---|---|
| 価格表示 | 税込み価格、通貨を明示。自動更新である旨を告知 |
| フリートライアル | 終了後の課金タイミングと金額を事前に提示 |
| 返金ポリシー | 各プラットフォームの返金ポリシーに準拠（プラットフォームが返金処理を担当） |
| 重複課金の禁止 | ユーザーが誤って同じサブスクリプションを複数購入しないような実装が必要 |
| 購入の復元 | 「購入を復元する」機能の実装が審査上推奨されている（iOS では審査通過に影響する場合あり） |

---

## 6. バックエンド要件（購入検証）

### 6-1. 購入検証とは

購入完了時にプラットフォームからアプリに渡されるトークン・トランザクション情報を、バックエンドサーバー側でプラットフォームの公式APIを使って確認する仕組みです。クライアント側の情報は改ざんできるため、サーバーリソースへのアクセス制御が必要な場合には必須です。

### 6-2. 検証が必要なケース

| ケース | 検証要否 | 理由 |
|---|---|---|
| アプリ内のみで権利管理（オフライン機能の開放等） | 不要 | クライアントの信頼で完結 |
| APIやサーバーリソースへのアクセス制御 | **必要** | 不正利用を防ぐ必要がある |
| 複数デバイスでの権利同期 | **必要** | サーバーが正とならないといけない |
| ユーザーアカウントとサブスク状態の紐付け | **必要** | 自前アカウントシステムと連携 |
| 不正利用・リセール防止 | **必要** | — |

### 6-3. iOS のサーバーサイド検証（App Store Server API）

#### ⚠️ 旧 `verifyReceipt` は deprecated

旧来の `/verifyReceipt` エンドポイントはAppleが非推奨とし、**App Store Server API への移行が必須**です。

#### 新しい検証フロー（App Store Server API）

```
1. アプリが transactionId（またはoriginalTransactionId）をバックエンドへ送信
2. バックエンドがJWT（JSON Web Token）を使ってApp Store Server APIへリクエスト
   - エンドポイント: GET /inApps/v1/subscriptions/{originalTransactionId}
3. AppleからJWS（JSON Web Signature）形式の署名付きレスポンスを受け取る
4. バックエンドがJWSの署名を検証し、サブスクリプションの有効期限・状態を確認
5. 権利をユーザーに付与
```

#### リアルタイム通知（App Store Server Notifications V2）

Appleからのサブスクリプションイベント（更新・解約・課金失敗等）をリアルタイムでバックエンドに通知する仕組みです。

| イベント例 | 用途 |
|---|---|
| `SUBSCRIBED` | 新規購入 |
| `DID_RENEW` | 自動更新成功 |
| `DID_FAIL_TO_RENEW` | 課金失敗（督促期間） |
| `EXPIRED` | サブスクリプション失効 |
| `REFUND` | 返金 |

**重要：** `originalTransactionId` をDBに保存すること。これがサブスクリプションのライフサイクル全体（更新・解約・アップグレード等）の追跡キーになります。

---

### 6-4. Android のサーバーサイド検証（Google Play Developer API）

#### 検証フロー

```
1. アプリが purchaseToken をバックエンドへ送信
2. バックエンドがサービスアカウント（OAuth2）でGoogle Play Developer APIを認証
3. subscriptionsV2.get エンドポイントへリクエスト
   - GET https://androidpublisher.googleapis.com/androidpublisher/v3/applications
     /{packageName}/purchases/subscriptionsv2/tokens/{token}
4. サブスクリプションの状態（ACTIVE/EXPIRED等）・有効期限を確認
5. 権利をユーザーに付与
```

**注意：** 旧 `subscriptions.get` より **`subscriptionsv2.get` が推奨**です（Billing Library 5以降の新しいサブスクリプション構造に対応）。

#### リアルタイム通知（Real-Time Developer Notifications / RTDN）

Google Cloud Pub/Sub を使ってバックエンドがサブスクリプションイベントを受信できます。

| 通知タイプ例 | 用途 |
|---|---|
| `SUBSCRIPTION_PURCHASED` | 新規購入 |
| `SUBSCRIPTION_RENEWED` | 自動更新成功 |
| `SUBSCRIPTION_ON_HOLD` | 課金失敗で保留中 |
| `SUBSCRIPTION_CANCELED` | 解約 |
| `SUBSCRIPTION_EXPIRED` | 失効 |

---

### 6-5. RevenueCat を使う場合

RevenueCat がレシート検証・権利管理・通知処理をすべて担当するため、**自前バックエンドは不要**になります。

```
アプリ（RevenueCat SDK）
  │ 購入時に自動でRevenueCatサーバーへ送信
  ▼
RevenueCat（検証・権利管理）
  │ Webhook で必要なイベントをバックエンドへ通知（任意）
  ▼
自前バックエンド（任意）
```

バックエンドが既存する場合も、RevenueCat Webhookからのイベントを受け取るだけで済むため実装コストを大幅に削減できます。

---

### 6-6. entitlement（権利）管理の考え方

「ユーザーがどの機能・コンテンツにアクセスできるか」を示す概念です。

| パターン | 管理方法 |
|---|---|
| `in_app_purchase` ＋ 自前バックエンド | DB に `originalTransactionId` / `purchaseToken` とサブスク状態を保存し、APIアクセス時に確認 |
| `in_app_purchase` ＋ アプリ内のみ | プラットフォームSDKにその都度問い合わせて状態を取得（サーバー不要だが複数デバイス管理は困難） |
| RevenueCat | ダッシュボードでentitlementを定義し、SDKの `CustomerInfo.entitlements.active` を参照するだけ |

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
