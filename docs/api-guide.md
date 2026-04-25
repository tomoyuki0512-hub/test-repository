---
title: APIの種類・特徴・歴史 完全ガイド
---

# APIの種類・特徴・歴史 完全ガイド

---

## APIとは何か — レストランのたとえ

- **あなた**（お客さん） = アプリやWebサービスを使う側
- **厨房** = データを持っているサーバー
- **ウェイター** = **API**

あなたは厨房に直接入れない。でもウェイター（API）に「ハンバーグ定食をください」と言えば、厨房に伝えて料理を持ってきてくれる。**APIはアプリ同士の「取次役」。**

天気予報アプリは気象庁のサーバーにAPIで「今日の東京の天気は？」と聞いて、答えを受け取って画面に表示している。

---

## 時代の流れ — 年表

```
1990年代
  ├─ 1991 ─ World Wide Webの誕生
  ├─ 1998 ─ XMLが標準化
  └─ 1999 ─ SOAPが登場（企業間の堅いAPI）

2000年代
  ├─ 2000 ─ RESTの概念登場（Roy Fieldingの博士論文）
  ├─ 2004 ─ Facebookが誕生（API連携の需要が爆発）
  ├─ 2006 ─ AWS・Twitter APIが公開（APIビジネスモデルの確立）
  └─ 2008 ─ iPhone普及（モバイル＋APIが当たり前に）

2010年代
  ├─ 2011 ─ WebSocket標準化（リアルタイム通信が普及）
  ├─ 2012 ─ REST APIが業界標準に定着
  ├─ 2015 ─ GraphQLをFacebookが公開
  ├─ 2016 ─ gRPCをGoogleが公開（マイクロサービス時代）
  └─ 2018 ─ API経済が本格化（APIを製品として販売）

2020年代
  ├─ 2020 ─ コロナでデジタル化が加速
  ├─ 2021 ─ tRPC登場（TypeScript型安全RPC）
  ├─ 2022 ─ ChatGPT登場、AI APIの時代が始まる
  ├─ 2024 ─ MCP（Model Context Protocol）登場
  └─ 現在  ─ REST・GraphQL・gRPC・WebSocket・SSEを用途で使い分ける成熟期
```

---

## 過去の主流

### SOAP — 役所の公文書のやり取り

**登場：** 1999年（Microsoft・IBM・W3Cが策定）

役所に書類を提出するとき、決まった様式・決まった順番・判子が必要……あの感じ。

```xml
<!-- SOAPのリクエスト例（こんなに書く必要がある）-->
<soap:Envelope>
  <soap:Body>
    <GetWeather>
      <City>Tokyo</City>
    </GetWeather>
  </soap:Body>
</soap:Envelope>
```

| 項目 | 内容 |
|---|---|
| データ形式 | XML（タグで囲む厳格な形式） |
| 長所 | セキュリティ高・エラー処理厳密・トランザクション対応 |
| 短所 | 書くのが面倒・データが重い・学習コスト高 |
| 向いている場面 | 銀行・医療・政府系の厳格なシステム |

**なぜ廃れたか：** XMLのペイロードが肥大化・仕様が複雑すぎ・Web/モバイル時代にRESTの軽量さが圧倒。現在はレガシー基幹システムの保守でのみ残存。

---

### XML-RPC・CORBA

- **XML-RPC（1998年）：** SOAPの前身。XMLでメソッドを呼び出す。SOAPに取って代わられた。
- **CORBA（1991年）：** オブジェクト指向の分散通信。実装間の互換性問題が多発し衰退。概念はgRPCに受け継がれた。

---

## 現在の主流

### REST — 普通の会話

**登場：** 2000年（Roy Fieldingの博士論文で提唱）

友達に「今日の東京の天気教えて」と自然に聞く感じ。決まりきった書式は不要。

```
// リクエスト（シンプル）
GET https://api.example.com/weather/tokyo

// レスポンス
{ "city": "Tokyo", "temp": 22, "weather": "晴れ" }
```

**HTTPメソッドの意味：**

| メソッド | 操作 | 例 |
|---|---|---|
| GET | 取得する | ユーザー情報を見る |
| POST | 新しく作る | 投稿を作成する |
| PUT | 全体を更新する | プロフィールを書き換える |
| PATCH | 一部を更新する | 名前だけ変える |
| DELETE | 削除する | 投稿を消す |

| 項目 | 内容 |
|---|---|
| データ形式 | JSON（読みやすい） |
| 長所 | シンプル・学習コスト低・エコシステム最大・CDNキャッシュと相性◎ |
| 短所 | Over/Under-fetching（不要なデータが来る or 足りない）・リアルタイムが苦手 |
| 向いている場面 | Webサービス全般・スマホアプリ・公開API |
| 採用例 | GitHub・Twitter・AWS・ほぼ全てのWebサービス |

---

### GraphQL — 欲しいものだけのビュッフェ

**登場：** 2015年（Facebookが公開）

ランチセットだと「サラダ・メイン・スープ・デザート」が全部来るが、メインだけ欲しい。GraphQLはビュッフェ形式で欲しいものだけ取れる。

```graphql
# 「名前」と「フォロワー数」だけが欲しい場合
query {
  user(id: "123") {
    name
    followersCount
  }
}
```

単一エンドポイント（通常 `POST /graphql`）で、クライアントがフィールドを指定する。

| 項目 | 内容 |
|---|---|
| データ形式 | JSON |
| 長所 | データの過不足なし・1回で複数リソース取得・型安全・コード自動生成 |
| 短所 | キャッシュが難しい・N+1問題が出やすい・小規模には過剰 |
| 向いている場面 | 複雑なデータ構造・SNS・BFFパターン |
| 採用例 | GitHub・Shopify・Netflix・Facebook |

---

### gRPC — 工場間の高速コンベア

**登場：** 2016年（Googleが公開）

工場Aと工場Bが生産ラインで直結され、人の手を介さず部品が高速で自動的に流れるイメージ。人間が読む必要はなく、速さと効率が優先。

```protobuf
// Protocol Buffers（.protoファイル）でスキーマを定義
service WeatherService {
  rpc GetWeather (WeatherRequest) returns (WeatherResponse);
  rpc StreamWeather (WeatherRequest) returns (stream WeatherResponse);
}
```

`.proto` ファイルから複数言語のクライアント/サーバーコードが自動生成される。

**通信パターン：**

| パターン | 説明 |
|---|---|
| Unary | 1リクエスト → 1レスポンス（通常の通信） |
| Server Streaming | 1リクエスト → 複数レスポンス（データを少しずつ返す） |
| Client Streaming | 複数リクエスト → 1レスポンス |
| Bidirectional | 複数リクエスト ↔ 複数レスポンス |

| 項目 | 内容 |
|---|---|
| データ形式 | Protocol Buffers（バイナリ）。JSONより3〜10倍小さく高速 |
| 通信 | HTTP/2 |
| 長所 | 超高速・型安全・多言語コード自動生成・ストリーミング標準対応 |
| 短所 | ブラウザから直接使いにくい・バイナリは人間が読めない |
| 向いている場面 | マイクロサービス間通信・内部API |
| 採用例 | Google・Square・Lyft・Dropbox |

---

### WebSocket — 電話（つなぎっぱなし）

**登場：** 2011年（RFC 6455として標準化）

普通のAPI通信は「手紙のやり取り」（送る→待つ→返事が来る）。WebSocketは「電話」。一度つながったら、どちらからでも、いつでも話しかけられる。

```
クライアント ──接続要求──▶ サーバー
クライアント ◀──承認────── サーバー
クライアント ◀──▶ サーバー（以降、双方向にリアルタイム通信）
```

| 項目 | 内容 |
|---|---|
| データ形式 | テキスト・バイナリ両対応 |
| 長所 | サーバーからもプッシュできる・低遅延・HTTPオーバーヘッドなし |
| 短所 | 接続維持でサーバー負荷が高い |
| 向いている場面 | チャット・オンラインゲーム・株価のリアルタイム表示 |
| 採用例 | Discord・Slack・Figma・Binance |

---

### SSE（Server-Sent Events）— ラジオ放送（一方向）

**登場：** HTML5仕様として策定

ラジオは放送局（サーバー）が一方的に電波を流し、リスナー（クライアント）は受け取るだけ。クライアントからは話しかけられない。

```
// サーバーが送るデータの形式
data: {"token": "こんにちは"}\n\n
data: {"token": "、今日の"}\n\n
data: {"token": "天気は晴れです"}\n\n
data: [DONE]\n\n
```

> **ChatGPTやClaudeが文字を少しずつ表示するのはSSEの仕組み。** LLMがトークンを生成するたびにSSEで送信している。

| 項目 | 内容 |
|---|---|
| データ形式 | テキスト |
| 長所 | 実装が簡単・通常のHTTPで動く・自動再接続が標準内蔵 |
| 短所 | サーバー→クライアントの一方向のみ |
| 向いている場面 | AIストリーミング・通知・ニュース速報 |
| 採用例 | OpenAI API・Anthropic API・各LLM API |

---

## 未来・今後のトレンド

### tRPC — TypeScript型安全RPC

**登場：** 2021年

TypeScriptを使う前提で、スキーマ定義ファイル不要。サーバー関数の型がそのままクライアントに伝わる。

```typescript
// サーバーの定義がそのままクライアントの型になる
const user = await trpc.user.getById.query({ id: "1" });
//                                          ^ 型が自動推論される
```

- **向いている場面：** Next.js・Remixなどのフルスタックアプリ
- **弱点：** TypeScript以外の言語には対応しない

---

### AsyncAPI — イベント駆動API仕様

**登場：** 2017年

RESTのOpenAPI（Swagger）に相当する、**非同期・イベント駆動APIの仕様記述標準**。Kafka・MQTT・WebSocketなどのメッセージブローカーを定義対象とする。

- IoT・金融系リアルタイムシステム・マイクロサービスで採用拡大中

---

### WebTransport — HTTP/3ベースの次世代通信

**登場：** 2022年（Chrome 97〜）

WebSocketの後継として設計。HTTP/3（QUIC）上で動作し、UDP的な低遅延通信とTCP的な信頼性を両立。

- **用途：** オンラインゲーム・ライブ映像配信・VR/AR
- **現状：** Chrome・Edgeは対応済み。Firefox・Safariは実装中。本番事例はまだ少ない。

---

### AI/LLM API — 台頭する新しい軸

ChatGPT以降、AIをAPIとして呼び出す設計が急拡大。

| 機能 | 概要 |
|---|---|
| **ストリーミング** | SSEでトークンを逐次返却。ChatGPT・Claude・Geminiが採用 |
| **Function Calling** | モデルが外部関数を呼び出すようJSON形式で宣言。エージェント実装に使用 |
| **Structured Output** | JSON Schemaを指定してレスポンスを構造化 |
| **Embeddings API** | テキストをベクトル化。類似検索・RAGに使用 |
| **MCP（Model Context Protocol）** | Anthropicが2024年に提唱。LLMがツール・リソースにアクセスするための標準プロトコル |

---

### Edge API — ユーザーの近くで処理する

Cloudflare Workers・Vercel Edge Functionsなど、CDNのエッジノード上でAPIロジックを実行。

- コールドスタートがほぼゼロ
- グローバル分散で低レイテンシ
- **用途：** A/Bテスト・認証ゲートウェイ・AI推論（軽量モデル）

---

## 全API比較表

| APIスタイル | 時代 | 通信方向 | 速度 | 学習コスト | 主な用途 | 現在の主流度 |
|---|---|---|---|---|---|---|
| **CORBA** | 過去 | 双方向 | 中 | 非常に高 | 分散オブジェクト通信 | ほぼなし |
| **XML-RPC** | 過去 | 双方向 | 遅い | 中 | レガシーRPC | ほぼなし |
| **SOAP** | 過去〜現在 | 双方向 | 遅い | 高い | 銀行・医療・官公庁 | 低い（保守のみ） |
| **REST** | 現在 | 双方向 | 普通 | 低い | Webサービス全般 | **非常に高い（事実上標準）** |
| **GraphQL** | 現在 | 双方向 | 中 | 中程度 | 複雑なデータ・SNS | 高い |
| **gRPC** | 現在 | 双方向 | 非常に速い | 高い | マイクロサービス間 | 高い（バックエンド間） |
| **WebSocket** | 現在 | 双方向 | 速い | 中程度 | チャット・ゲーム | 高い（リアルタイム用途） |
| **SSE** | 現在〜未来 | 一方向 | 速い | 低い | AIストリーミング・通知 | 急速に拡大中 |
| **tRPC** | 現在〜未来 | 双方向 | 速い | 低い（TS前提） | TSフルスタック | 成長中 |
| **AsyncAPI** | 未来 | 非同期 | N/A | 中程度 | イベント駆動 | 成長中 |
| **WebTransport** | 未来 | 双方向 | 非常に速い | 高い | ゲーム・VR/AR | 普及段階 |
| **LLM API** | 現在〜未来 | 双方向 | モデル依存 | 中程度 | AI推論・エージェント | 急速に上昇中 |
| **Edge API** | 現在〜未来 | 双方向 | 非常に速い | 中程度 | 低レイテンシAPI | 成長中 |

---

## どれを選ぶべきか

```
リアルタイム通信が必要？
  ├─ YES ─ 双方向（サーバー↔クライアント）？
  │           ├─ YES → WebSocket（チャット・ゲーム）
  │           └─ NO  → SSE（通知・AIストリーミング）
  │
  └─ NO ─ サービス間の内部通信（高速さ重視）？
              ├─ YES → gRPC（マイクロサービス）
              └─ NO ─ データ構造が複雑？
                          ├─ YES → GraphQL（SNS・複雑なアプリ）
                          └─ NO ─ 銀行・医療・官公庁？
                                      ├─ YES → SOAP
                                      └─ NO  → REST（Webサービス全般）
```

> **迷ったらRESTから始める。** 世界中のほぼ全てのWebサービスで使われており、ドキュメントも豊富。特別な要件が出てきたときに他の方式を検討するのが現実的。

---

## 詳細パターン別 選択ガイド

---

### パターン1：チームサイズ × 人件費単価

| チーム規模 | 人数 | 人件費の目安 | 推奨API | 理由 |
|---|---|---|---|---|
| 個人開発 / フリーランス | 1人 | 〜100万円/月 | **REST** または **tRPC** | 習熟コストゼロ・ドキュメント豊富・一人で全部見られる |
| スタートアップ | 2〜5人 | 50〜80万円/人月 | **REST** ＋ 必要に応じ **GraphQL** | 速く作る・後から拡張しやすい。GraphQLはデータが複雑になってから追加 |
| 成長期スタートアップ | 5〜15人 | 70〜120万円/人月 | **REST**（外部）＋ **gRPC**（内部） | フロント向けはREST、バックエンド間はgRPCで高速化しはじめる段階 |
| 中規模企業 | 15〜50人 | 80〜150万円/人月 | **REST / GraphQL / gRPC** を役割分担 | チームが分かれるため、サービス間通信の設計が重要。GraphQLはBFF層に集約 |
| 大企業 / エンタープライズ | 50人以上 | 100〜200万円/人月 | **gRPC**（内部）＋ **REST / SOAP**（外部・レガシー連携） | 大規模マイクロサービス。既存システムとのSOAP連携が残ることも多い |

> **BFF（Backend For Frontend）：** フロントエンド専用のAPIゲートウェイ層。GraphQLをここに置き、内部のgRPCサービスを束ねる構成が大企業では多い。

---

### パターン2：性能 × 用途

| 性能要件 | 重視点 | 推奨API | 補足 |
|---|---|---|---|
| **超低遅延（〜10ms）** | ゲーム・取引・VR | **WebSocket** / **WebTransport** / **gRPC** | WebTransportはUDP的な低遅延。本番はWebSocketが安定 |
| **高スループット（大量データ転送）** | マイクロサービス内部 | **gRPC** | バイナリ形式でJSON比3〜10倍軽量。HTTP/2多重化で並列処理 |
| **リアルタイム双方向** | チャット・コラボツール | **WebSocket** | 接続維持コストと引き換えに最低遅延の双方向を実現 |
| **サーバー→クライアントのプッシュ** | AI返答・通知・速報 | **SSE** | 実装がシンプルで通常のHTTPで動く。ChatGPT/Claudeも採用 |
| **通常のCRUD** | Webサービス全般 | **REST** | スループット・レイテンシともに「十分」な水準。スケールはCDN/キャッシュで対応 |
| **複雑なデータ取得を最適化** | SNS・ダッシュボード | **GraphQL** | 1リクエストで複数リソースを取得。Over-fetchingによる帯域浪費を削減 |
| **セキュリティ・完全性最優先** | 銀行・医療・官公庁 | **SOAP** | WS-Securityによる暗号化・署名・トランザクションが標準仕様に含まれる |

**速度の目安（同条件の比較）：**

```
gRPC（バイナリ）  ████████████████ 最速
WebSocket        ████████████░░░░ 速い（常時接続）
REST（HTTP/2）   ████████░░░░░░░░ 普通（キャッシュ効果大）
REST（HTTP/1.1） ██████░░░░░░░░░░ 普通（接続確立のオーバーヘッドあり）
GraphQL          █████░░░░░░░░░░░ N+1問題に注意
SOAP（XML）      ███░░░░░░░░░░░░░ 遅い（ペイロード肥大）
```

---

### パターン3：コスト構造（インフラ × 開発）

| API | インフラコスト | 開発コスト | 保守コスト | トータルコスト評価 |
|---|---|---|---|---|
| **REST** | 低〜中（CDNキャッシュ効果大） | 低（エンジニア全員が使える） | 低（仕様変更が容易） | ★★★★★ コスパ最高 |
| **GraphQL** | 中（キャッシュが難しい） | 中（スキーマ設計・N+1対策必要） | 中（スキーマ変更の影響範囲が広い） | ★★★☆☆ 規模次第 |
| **gRPC** | 低（バイナリ・圧縮率高） | 高（proto定義・多言語対応・知識） | 中（proto変更管理が必要） | ★★★☆☆ 大規模向け |
| **WebSocket** | 高（接続維持でサーバーコスト増） | 中（状態管理が複雑） | 高（スケールアウトにSticky Sessionが必要） | ★★☆☆☆ リアルタイム専用 |
| **SSE** | 低〜中（HTTP通常接続） | 低（実装が簡単） | 低 | ★★★★☆ AIには最適 |
| **tRPC** | 低 | 非常に低（コード自動生成・型安全） | 低（TSが守る） | ★★★★★ TS限定でコスパ最高 |
| **SOAP** | 低〜中 | 非常に高（XMLスキーマ・WSDLが複雑） | 非常に高（仕様が硬直的） | ★☆☆☆☆ 新規開発には非推奨 |

**開発コスト試算イメージ（エンジニア1人月100万円の場合）：**

```
REST APIでCRUDアプリを構築：
  設計0.5人月 + 実装1人月 + テスト0.5人月 = 2人月 → 200万円

同仕様をSOAPで構築：
  設計1人月 + 実装3人月 + テスト1.5人月 = 5.5人月 → 550万円（2.75倍）

同仕様をgRPCで構築（マイクロサービス前提）：
  設計1.5人月 + 実装2人月 + テスト1人月 = 4.5人月 → 450万円
  ただし通信コストが 1/5〜1/10 になるため、大規模になるほど元が取れる
```

---

### パターン4：フレームワーク × API 相性表

| フレームワーク | 言語 | 最も相性の良いAPI | 対応可能なAPI | 備考 |
|---|---|---|---|---|
| **Next.js** | TypeScript | **REST**（API Routes）/ **tRPC** | GraphQL（Apollo）, SSE | tRPCはNext.jsのために設計された。フルスタックならtRPCが最速 |
| **React（Vite）** | TypeScript | **REST** / **GraphQL** | tRPC, WebSocket, SSE | APIサーバーが別の場合はREST。Shopify等GraphQL APIを使うならGraphQL |
| **Vue.js / Nuxt** | TypeScript | **REST** | GraphQL（urql）, tRPC | NuxtもtorPC対応あり。基本はREST |
| **Rails** | Ruby | **REST**（標準・scaffold対応） | GraphQL（graphql-ruby）, WebSocket（ActionCable） | scaffoldがRESTを自動生成。GraphQLも成熟した gem がある |
| **Django** | Python | **REST**（DRF: Django REST Framework） | GraphQL（Graphene）, WebSocket（Django Channels） | DRFはRest API構築ライブラリとして最大級 |
| **FastAPI** | Python | **REST**（標準・自動ドキュメント生成）/ **SSE**（標準対応） | gRPC（grpcio）, WebSocket（標準） | Swagger UIが自動生成される。SSEもネイティブ対応でAI APIとの相性◎ |
| **Express.js** | JavaScript | **REST** | WebSocket（ws/Socket.IO）, GraphQL（Apollo Server） | 最小構成で自由度高い。Socket.IOは実質WebSocketのデファクト |
| **NestJS** | TypeScript | **REST** / **GraphQL** / **gRPC** | WebSocket（標準）, tRPC | 全方式をモジュールで切り替え可能。大規模TS構成に向く |
| **Spring Boot** | Java/Kotlin | **REST**（Spring MVC/WebFlux） | gRPC（grpc-spring-boot）, GraphQL（Spring for GraphQL）, SOAP（Spring WS） | 金融・医療でSOAPを使うケースが現在も残る |
| **Laravel** | PHP | **REST**（標準） | GraphQL（Lighthouse）, WebSocket（Laravel Echo + Pusher） | Laravelはデフォルト構成がRESTに最適化されている |
| **Flutter** | Dart | **REST**（http/dio）/ **gRPC**（公式対応） | WebSocket（標準）, SSE | Googleが作ったため、gRPCとの親和性が高い。Firebase利用ならWebSocket不要 |

---

### パターン5：プロジェクト種別 × 総合推奨

| プロジェクト種別 | 規模感 | チーム | 推奨構成 | フレームワーク例 |
|---|---|---|---|---|
| **個人ポートフォリオ・ランディングページ** | 極小 | 1人 | REST（またはAPIなし） | Next.js（静的）/ Rails |
| **MVP・プロトタイプ** | 小 | 1〜3人 | **REST** | Next.js + Prisma / Rails / FastAPI |
| **一般的なWebサービス（SaaS）** | 中 | 5〜15人 | **REST**（外部）+ 必要に応じ **GraphQL** | Next.js / NestJS / Spring Boot |
| **SNS・コラボツール（リアルタイム）** | 中〜大 | 10〜30人 | **REST** + **WebSocket** | Express + Socket.IO / Rails + ActionCable |
| **AIサービス（チャット・生成系）** | 中 | 5〜20人 | **REST** + **SSE** | FastAPI / Next.js / Express |
| **大規模マイクロサービス** | 大 | 30人以上 | **gRPC**（内部）+ **REST / GraphQL**（外部） | Spring Boot / NestJS / Go（Gin） |
| **金融・医療・官公庁システム** | 大 | 20〜100人 | **SOAP**（レガシー連携）+ **REST**（新規） | Spring Boot / .NET |
| **モバイルアプリ（iOS/Android）** | 中 | 5〜20人 | **REST** または **gRPC** | Flutter + FastAPI / Flutter + Firebase |
| **IoT・センサーデータ収集** | 中〜大 | 10〜30人 | **gRPC** または **AsyncAPI**（Kafka/MQTT） | FastAPI / Spring Boot |
| **ゲーム（リアルタイム対戦）** | 大 | 20人以上 | **WebSocket** または **WebTransport** | Node.js（コライダーサーバー）+ REST（API） |

---

### まとめ：判断の優先順位

```
① まずリアルタイム通信が必要か確認
     双方向リアルタイム → WebSocket
     サーバー→クライアント一方向 → SSE
     （どちらでもなければ次へ）

② チームのスキルセット・人件費を確認
     TypeScript中心・小チーム → tRPC（コスト最小）
     大規模・多言語マイクロサービス → gRPC（パフォーマンス最大）
     （それ以外は次へ）

③ データ構造の複雑さを確認
     複数リソースを複雑に結合する → GraphQL
     シンプルなCRUD中心 → REST

④ 規制・コンプライアンスを確認
     銀行・医療・官公庁 → SOAP（既存システムとの連携で必要）

⑤ どれでもなければ → REST
     全体の80%以上のケースはRESTで解決できる
```
