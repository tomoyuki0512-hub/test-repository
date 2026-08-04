---
title: Node.js 用語集・チートシート
---

# 用語集・チートシート

[← 総合インデックスに戻る](README.md)

用語辞典と「困った時どの章？」の逆引き表です。

---

## 1. 用語集

### 基本

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **Node.js** | ブラウザ外でJSを動かす**実行環境**（言語ではない） | [①](01-what-is-nodejs.md) |
| **V8** | JavaScriptを実行するエンジン。Chromeと同じもの | [①](01-what-is-nodejs.md) |
| **libuv** | 非同期I/Oとイベントループを担うC言語ライブラリ | [①](01-what-is-nodejs.md) |
| **REPL** | 対話実行環境。`node` と打つと起動する | [①](01-what-is-nodejs.md) |
| **LTS** | Long Term Support。長期サポート版。**偶数バージョンのみ** | [①](01-what-is-nodejs.md) |
| **Deno / Bun** | Node.js以外のJS実行環境 | [①](01-what-is-nodejs.md) |

### 非同期・イベントループ

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **シングルスレッド** | JSの実行が1本だけ。同時に2つは走らない | [②](02-event-loop.md) |
| **イベントループ** | 終わった仕事を順に処理する司令塔 | [②](02-event-loop.md) |
| **コールスタック** | 実行中の関数が積まれる場所 | [②](02-event-loop.md) |
| **マイクロタスク** | Promise の続き。**マクロタスクより優先** | [②](02-event-loop.md) |
| **マクロタスク** | `setTimeout`・I/O完了など | [②](02-event-loop.md) |
| **`process.nextTick`** | Node.js固有。マイクロタスクより更に優先 | [②](02-event-loop.md) |
| **ブロッキング** | 同期処理でイベントループを止めること。**最大の事故要因** | [②](02-event-loop.md) |
| **スレッドプール** | libuvが持つ裏方スレッド（既定4本） | [②](02-event-loop.md) |
| **`worker_threads`** | 重いCPU処理を別スレッドで実行する仕組み | [②](02-event-loop.md) |
| **`cluster`** | 複数プロセスを立てて複数コアを使う仕組み | [②](02-event-loop.md) |
| **C10K問題** | 1万同時接続を捌けない問題。Node.js誕生の背景 | [①](01-what-is-nodejs.md) |

### モジュール・パッケージ

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **CommonJS（CJS）** | `require` / `module.exports` の旧方式 | [③](03-modules-packages.md) |
| **ES Modules（ESM）** | `import` / `export` の標準方式。**新規はこちら** | [③](03-modules-packages.md) |
| **`"type": "module"`** | package.jsonでESMを有効にする設定 | [③](03-modules-packages.md) |
| **`import.meta.dirname`** | ESMでの `__dirname` の代替 | [③](03-modules-packages.md) |
| **`ERR_REQUIRE_ESM`** | CJSからESM専用パッケージをrequireしたエラー | [③](03-modules-packages.md) |
| **lockファイル** | 実際に入れたバージョンの記録。**必ずコミット** | [③](03-modules-packages.md) |
| **`npm ci`** | lock通りに正確にインストール。CI・本番用 | [③](03-modules-packages.md) |
| **`dependencies`** | 本番で必要な依存 | [③](03-modules-packages.md) |
| **`devDependencies`** | 開発時だけ必要な依存 | [③](03-modules-packages.md) |
| **`overrides`** | 推移的依存のバージョンを強制する設定 | [③](03-modules-packages.md) |
| **typosquatting** | 似た名前の偽パッケージを紛れ込ませる攻撃 | [③](03-modules-packages.md) |
| **`node:` プレフィックス** | 標準モジュールであることを明示する記法 | [③](03-modules-packages.md) |

### 標準API

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **`fs`** | ファイル操作。**`*Sync` はサーバーで使わない** | [④](04-core-apis.md) |
| **Buffer** | バイト列を扱うNode.js固有の型 | [④](04-core-apis.md) |
| **ストリーム** | 大きなデータを少しずつ流す仕組み | [④](04-core-apis.md) |
| **`pipeline`** | ストリームを安全に連結する関数 | [④](04-core-apis.md) |
| **`process.env`** | 環境変数 | [④](04-core-apis.md) |
| **`AbortController`** | 処理をキャンセルする標準の仕組み | [④](04-core-apis.md) |
| **グレースフルシャットダウン** | 処理中のリクエストを終えてから終了すること | [④](04-core-apis.md)・[⑦](07-practice-operations.md) |
| **SIGTERM** | 「終了してください」というシグナル | [④](04-core-apis.md) |
| **パストラバーサル** | `../` で想定外のファイルにアクセスする攻撃 | [④](04-core-apis.md) |

### 非同期パターン

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **Promise** | まだ結果の出ていない値を表すオブジェクト | [⑤](05-async-patterns.md) |
| **`Promise.all`** | 全部並列実行。**1つ失敗で全体失敗** | [⑤](05-async-patterns.md) |
| **`Promise.allSettled`** | 成功も失敗も全部待つ | [⑤](05-async-patterns.md) |
| **`Promise.race`** | 最初に決着したものを採用 | [⑤](05-async-patterns.md) |
| **floating promise** | `await` されていないPromise。**エラーが漏れる** | [⑤](05-async-patterns.md) |
| **`unhandledRejection`** | 誰も捕まえなかったPromiseのエラー | [⑤](05-async-patterns.md) |
| **指数バックオフ** | リトライ間隔を倍々に伸ばす手法 | [⑤](05-async-patterns.md) |
| **ジッター** | リトライ時刻をばらけさせる乱数 | [⑤](05-async-patterns.md) |
| **冪等性** | 何度実行しても結果が同じ性質 | [⑤](05-async-patterns.md) |

### サーバー・運用

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **ミドルウェア** | リクエストが順に通過する処理。`next()` で次へ | [⑥](06-server-frameworks.md) |
| **認証（Authentication）** | 「誰か」を確認すること → 401 | [⑥](06-server-frameworks.md) |
| **認可（Authorization）** | 「何をしてよいか」を確認すること → 403 | [⑥](06-server-frameworks.md) |
| **CORS** | 別オリジンからのアクセス制御 | [⑥](06-server-frameworks.md) |
| **レート制限** | 一定時間内のリクエスト数を制限する | [⑥](06-server-frameworks.md) |
| **BFF** | Backend For Frontend。フロント専用のAPI集約層 | [①](01-what-is-nodejs.md) |
| **構造化ログ** | JSON形式のログ。検索・集計できる | [⑦](07-practice-operations.md) |
| **N+1問題** | 一覧1回＋各件1回ずつクエリが飛ぶ非効率 | [⑦](07-practice-operations.md) |
| **`healthz` / `readyz`** | 生存確認 / 準備完了確認。**分ける** | [⑦](07-practice-operations.md) |
| **PID 1問題** | コンテナでシグナルが届かない問題。dumb-initで対処 | [⑦](07-practice-operations.md) |

---

## 2. 逆引き表 — 困った時どの章？

| やりたいこと・困りごと | 見る章 |
| --- | --- |
| Node.jsが何なのか知りたい | [① Node.jsとは](01-what-is-nodejs.md) |
| ブラウザとの違いを知りたい | [① 違い](01-what-is-nodejs.md#2-何が違うのか--ブラウザ-vs-nodejs) |
| `window is not defined` が出る | [① 違い](01-what-is-nodejs.md#2-何が違うのか--ブラウザ-vs-nodejs) |
| Node.jsが向く用途を知りたい | [① 得意不得意](01-what-is-nodejs.md#5-nodejsの得意不得意) |
| インストール・バージョン管理 | [① インストール](01-what-is-nodejs.md#6-インストールと最初の一歩) |
| Deno/Bunと比較したい | [① 比較](01-what-is-nodejs.md#7-deno-と-bun--後発の選択肢) |
| **実行順序が理解できない** | [② イベントループ](02-event-loop.md#2-イベントループの仕組み) |
| **サーバーが固まる** | [② ブロッキング](02-event-loop.md#4--イベントループを止めてはいけない) |
| CPU使用率が100%になる | [② ブロッキング](02-event-loop.md#4--イベントループを止めてはいけない) |
| 重い処理を逃がしたい | [② 逃がし方](02-event-loop.md#重い処理の逃がし方) |
| 複数コアを使いたい | [② 複数コア](02-event-loop.md#7-複数コアを活用する) |
| `forEach` 内の `await` が効かない | [② forEachの罠](02-event-loop.md#foreach-の罠) |
| `import` と `require` の違い | [③ モジュール方式](03-modules-packages.md#1-2つのモジュール方式) |
| `ERR_REQUIRE_ESM` が出る | [③ ESMの注意点](03-modules-packages.md#️-esmの注意点) |
| `__dirname` が使えない | [③ ESMの注意点](03-modules-packages.md#️-esmの注意点) |
| package.jsonの読み方 | [③ package.json](03-modules-packages.md#3-packagejson-の読み方) |
| CIで動かない・環境差が出る | [③ lockファイル](03-modules-packages.md#4-lockファイルが最重要) |
| `Cannot find module` が出る | [③ トラブル対処](03-modules-packages.md#6-依存関係のトラブル対処) |
| パッケージの安全性を確認したい | [③ セキュリティ](03-modules-packages.md#7--npmパッケージのセキュリティ) |
| ファイルを読み書きしたい | [④ fs](04-core-apis.md#1-fs--ファイル操作) |
| パスを組み立てたい | [④ path](04-core-apis.md#2-path--パス操作) |
| 環境変数を扱いたい | [④ process](04-core-apis.md#3-process--プロセスと環境変数) |
| 外部APIを呼びたい | [④ fetch](04-core-apis.md#外部apiを呼ぶfetch) |
| 巨大ファイルでメモリ不足 | [④ stream](04-core-apis.md#5-stream--大きなデータを扱う) |
| デプロイ時にリクエストが切れる | [④ シャットダウン](04-core-apis.md#グレースフルシャットダウン) |
| トークンを生成したい | [④ crypto](04-core-apis.md#crypto--ハッシュ乱数) |
| **APIが遅い** | [⑤ 直列と並列](05-async-patterns.md#2--直列と並列--最も効く高速化) |
| 相手のAPIを落としてしまった | [⑤ 並列数制限](05-async-patterns.md#️-ただし並列にしすぎない) |
| 一部失敗でも続行したい | [⑤ allSettled](05-async-patterns.md#allsettled--部分的な失敗を許す) |
| **エラーが捕まらない** | [⑤ エラー処理](05-async-patterns.md#4--エラーハンドリング) |
| プロセスが突然落ちる | [⑤ エラー処理](05-async-patterns.md#プロセス全体の保険) |
| リトライを実装したい | [⑤ リトライ](05-async-patterns.md#5-リトライとタイムアウト) |
| APIサーバーを作りたい | [⑥ Express](06-server-frameworks.md#2-express-の基本) |
| フレームワークを選びたい | [⑥ 比較](06-server-frameworks.md#1-フレームワークの比較) |
| 入力を検証したい | [⑥ バリデーション](06-server-frameworks.md#3-バリデーションは必須) |
| ログイン機能を作りたい | [⑥ 認証と認可](06-server-frameworks.md#4-認証と認可) |
| REST APIを設計したい | [⑥ REST設計](06-server-frameworks.md#5-rest-api-の設計) |
| 401と403の使い分け | [⑥ ステータスコード](06-server-frameworks.md#ステータスコード) |
| 本番向けの設定を知りたい | [⑥ セキュリティ設定](06-server-frameworks.md#6-本番用のセキュリティ設定) |
| Next.jsで別サーバーが要るか | [⑥ 判断](06-server-frameworks.md#8-nextjs-を使う場合の判断) |
| ログを整備したい | [⑦ ログ](07-practice-operations.md#1-ログ--consolelog-を卒業する) |
| 障害を追跡したい | [⑦ リクエストID](07-practice-operations.md#リクエストidで追跡する) |
| 脆弱性対策を知りたい | [⑦ セキュリティ](07-practice-operations.md#2-セキュリティ) |
| メモリリークを調べたい | [⑦ パフォーマンス](07-practice-operations.md#3-パフォーマンス) |
| Dockerでデプロイしたい | [⑦ Docker](07-practice-operations.md#4-docker-でのデプロイ) |
| ヘルスチェックを作りたい | [⑦ 監視](07-practice-operations.md#5-ヘルスチェックと監視) |
| リリース前に確認したい | [⑦ チェックリスト](07-practice-operations.md#8-本番リリース前チェックリスト) |
| **ReactやNext.jsとの関係** | [関係ガイド](../js-stack-relations.md) |

---

## 3. 頻出エラー早見表

| エラー / 症状 | 原因 | 対処 |
| --- | --- | --- |
| `Cannot find module 'xxx'` | 未インストール・パス誤り | `npm install`・拡張子確認 |
| `ERR_REQUIRE_ESM` | CJSからESMをrequire | `"type": "module"` / 動的import |
| `ERR_MODULE_NOT_FOUND` | ESMで拡張子を省略 | `./utils.js` と書く |
| `__dirname is not defined` | ESMで使用 | `import.meta.dirname` |
| `EADDRINUSE` | ポートが使用中 | 別プロセスを終了 / ポート変更 |
| `EACCES` | 権限不足（1024未満のポート等） | ポート変更 / 権限確認 |
| `ECONNREFUSED` | 接続先が起動していない | DB/APIの起動確認 |
| `ETIMEDOUT` | 応答がない | タイムアウト設定・疎通確認 |
| `UnhandledPromiseRejection` | `.catch` / `await` 忘れ | エラー処理を追加 |
| `JavaScript heap out of memory` | メモリ不足 | ストリーム化・`--max-old-space-size` |
| `MaxListenersExceededWarning` | リスナー解除漏れ | `removeListener` を追加 |
| `Too many connections` | DB接続の作りすぎ | プール設定・シングルトン化 |
| `Promise { <pending> }` と出る | `await` 忘れ | `await` を付ける |
| サーバーが応答しない | 同期処理でブロック | 非同期版・worker |

---

## 4. チートシート

### よく使うコマンド

```bash
node app.js                      # 実行
node --watch app.js              # ファイル変更で自動再起動
node --env-file=.env app.js      # 環境変数を読み込む
node --test                      # 標準テストランナー
node --cpu-prof app.js           # CPUプロファイル取得
node -v                          # バージョン確認

npm ci                           # lock通りにインストール（CI/本番）
npm outdated                     # 古いパッケージ一覧
npm audit                        # 脆弱性チェック
npm ls <pkg>                     # 依存ツリーを確認
npx <cmd>                        # 一度だけ実行
```

### よく使うコード片

```js
// 標準モジュール（node: プレフィックス付き）
import fs from 'node:fs/promises'
import path from 'node:path'
import crypto from 'node:crypto'

// ESMでの__dirname
import.meta.dirname

// 並列実行
const [a, b] = await Promise.all([fa(), fb()])

// 一部失敗を許容
const results = await Promise.allSettled([fa(), fb()])

// タイムアウト付きfetch
await fetch(url, { signal: AbortSignal.timeout(5000) })

// 待機
await new Promise((r) => setTimeout(r, 1000))

// ID・トークン生成
crypto.randomUUID()
crypto.randomBytes(32).toString('hex')

// グレースフルシャットダウン
process.on('SIGTERM', () => server.close(() => process.exit(0)))
```

### 必ず入れたいESLintルール

```js
'@typescript-eslint/no-floating-promises': 'error',   // await忘れ検出
'@typescript-eslint/no-misused-promises': 'error',
'require-atomic-updates': 'error',
```

---

## 5. バージョン別の注意点

| バージョン | 変更 | 影響 |
| --- | --- | --- |
| **18** | `fetch` 標準搭載 | axios が不要に |
| **20.6** | `--env-file` 対応 | dotenv が不要に |
| **20.11** | `import.meta.dirname` | ESMでのパス取得が簡単に |
| **22** | Maintenance LTS（EOL: 2027/4） | 順次移行を |
| **24** | **Active LTS（EOL: 2028/4）** | ✅ **本番はこれ** |
| **24** | TypeScript直接実行 | ビルドなしで `.ts` を実行可（型チェックはしない） |
| **26** | Current（2026/10にLTS化予定） | 本番利用は待つ |

---

## 6. 関連シリーズ

- 📖 [JavaScript・Node.js・React・Next.js の関係](../js-stack-relations.md) ← 全体像
- 🔵 [React 完全ガイド](../react/README.md) ← 画面を作る
- ⚫ [Next.js 完全ガイド](../nextjs/README.md) ← Reactでサービスを作る

---

[← 総合インデックスに戻る](README.md)
