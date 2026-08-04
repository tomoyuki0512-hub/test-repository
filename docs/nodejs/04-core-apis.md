---
title: ④ 標準APIを使う
---

# ④ 標準APIを使う — fs・path・http・stream・process

[← 総合インデックスに戻る](README.md) ｜ 前 → [③ モジュールとnpm](03-modules-packages.md) ｜ 次 → [⑤ 非同期処理を書きこなす](05-async-patterns.md)

Node.jsに最初から入っている機能を扱います。**ライブラリを入れる前に、標準で足りないか確認する**習慣をつけると、依存が減って保守が楽になります。

---

## 1. `fs` — ファイル操作

### 🚨 必ず非同期版を使う

```js
import fs from 'node:fs/promises'    // ✅ Promise版をimportする

// 読み込み
const text = await fs.readFile('data.txt', 'utf-8')

// 書き込み
await fs.writeFile('out.txt', 'こんにちは')

// 追記
await fs.appendFile('log.txt', 'ログ行\n')

// 存在確認（例外で判定する）
try {
  await fs.access('config.json')
  // 存在する
} catch {
  // 存在しない
}

// ディレクトリ作成（親ごと）
await fs.mkdir('a/b/c', { recursive: true })

// 一覧
const files = await fs.readdir('./src')

// 情報取得
const stat = await fs.stat('file.txt')
console.log(stat.size, stat.isDirectory())

// 削除
await fs.rm('temp', { recursive: true, force: true })
```

> 🚨 **`readFileSync` などの同期版は、サーバーでは使わないでください。** 実行中はイベントループが完全に止まり、全リクエストが待たされます（→ [②](02-event-loop.md#4--イベントループを止めてはいけない)）。起動時の設定ファイル読み込みなど、**リクエスト処理外の一度きりの処理**でのみ許容されます。

### `utf-8` を忘れると

```js
const data = await fs.readFile('a.txt')            // Buffer（バイト列）が返る
const text = await fs.readFile('a.txt', 'utf-8')   // 文字列が返る
```

---

## 2. `path` — パス操作

**OSによってパスの区切り文字が違う**（`/` と `\`）ため、文字列結合ではなく `path` を使います。

```js
import path from 'node:path'

path.join('src', 'lib', 'a.js')        // 'src/lib/a.js'
path.resolve('src', 'a.js')            // 絶対パスに変換
path.extname('photo.png')              // '.png'
path.basename('/a/b/c.txt')            // 'c.txt'
path.basename('/a/b/c.txt', '.txt')    // 'c'
path.dirname('/a/b/c.txt')             // '/a/b'
path.parse('/a/b/c.txt')               // { dir, base, ext, name }
```

```js
// ❌ Windowsで壊れる
const p = dir + '/' + filename

// ✅
const p = path.join(dir, filename)
```

### 🚨 パストラバーサル対策

ユーザー入力をパスに使うときは**必ず検証**してください。

```js
// 🚨 危険：'../../etc/passwd' を渡されると任意のファイルが読める
app.get('/files/:name', async (req, res) => {
  const content = await fs.readFile(path.join(UPLOAD_DIR, req.params.name))
  res.send(content)
})

// ✅ 正規化してから、想定ディレクトリ内か確認する
const target = path.resolve(UPLOAD_DIR, req.params.name)
if (!target.startsWith(path.resolve(UPLOAD_DIR) + path.sep)) {
  return res.status(400).json({ error: 'Invalid path' })
}
```

---

## 3. `process` — プロセスと環境変数

```js
process.env.NODE_ENV        // 環境変数
process.argv                // コマンドライン引数
process.cwd()               // 現在のディレクトリ
process.version             // Node.jsのバージョン
process.exit(1)             // 終了（1は異常終了）
process.memoryUsage()       // メモリ使用量
```

### 環境変数の扱い

```bash
# .env （Gitにコミットしない）
DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=secret123
PORT=3000
```

**Node.js 20.6 以降は `--env-file` で読み込めます**（dotenvパッケージが不要）。

```bash
node --env-file=.env app.js
```

### 🚨 起動時に検証する

```ts
import { z } from 'zod'

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
})

export const env = envSchema.parse(process.env)
```

**設定漏れが起動時に即座にわかります。** 「本番デプロイ後、特定の機能を使った瞬間に `undefined` で落ちる」という事故を防げます。

### 🚨 秘密情報の扱い

```js
// ❌ 絶対にやってはいけない
const API_KEY = 'sk-abc123...'        // コードに直書き
console.log(process.env)              // ログに全部出る
```

- 秘密情報は**必ず環境変数**（またはSecrets Manager）
- `.env` は `.gitignore` に入れる
- `.env.example` をコミットして必要なキーだけ共有
- **ログに環境変数を丸ごと出さない**

### グレースフルシャットダウン

コンテナ環境では、終了シグナルを受けたら**処理中のリクエストを完了させてから**終了する必要があります。

```js
async function shutdown(signal) {
  console.log(`${signal} を受信。シャットダウンします`)
  server.close(async () => {          // 新規接続を止め、処理中を待つ
    await db.end()                     // DB接続を閉じる
    process.exit(0)
  })
  // 保険：一定時間で強制終了
  setTimeout(() => process.exit(1), 10_000).unref()
}

process.on('SIGTERM', () => shutdown('SIGTERM'))
process.on('SIGINT', () => shutdown('SIGINT'))
```

**これがないと、デプロイのたびに処理中のリクエストが切断されます。**

---

## 4. `http` — サーバーとリクエスト

### 素のHTTPサーバー

```js
import http from 'node:http'

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' })
    res.end(JSON.stringify({ status: 'ok' }))
    return
  }
  res.writeHead(404)
  res.end('Not Found')
})

server.listen(3000, () => console.log('http://localhost:3000'))
```

実務ではこれをそのまま使うことは稀で、Express等のフレームワークを使います（→ [⑥](06-server-frameworks.md)）。ただし**中で何が起きているかを知っておく**と、トラブル時に役立ちます。

### 外部APIを呼ぶ（`fetch`）

**Node.js 18 以降、`fetch` が標準搭載**されました。axiosは不要になりつつあります。

```js
const res = await fetch('https://api.example.com/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: '田中' }),
})

if (!res.ok) {
  throw new Error(`API error: ${res.status} ${res.statusText}`)
}
const data = await res.json()
```

> ⚠️ **`fetch` はHTTPエラー（404・500）で例外を投げません。** `res.ok` の確認を忘れると、エラーのHTMLをJSONとしてパースしようとして意味不明なエラーになります。

### タイムアウトを必ず付ける

```js
const res = await fetch(url, {
  signal: AbortSignal.timeout(5000),   // 5秒でタイムアウト
})
```

**タイムアウトがないと、相手が応答しないときに永久に待ち続けます。** 外部API呼び出しでは必須です。

---

## 5. `stream` — 大きなデータを扱う

**巨大なファイルを一度にメモリへ載せると、プロセスが落ちます。**

```js
// ❌ 1GBのファイルを全部メモリに載せる → クラッシュ
const data = await fs.readFile('huge.csv')

// ✅ 少しずつ流す
import { createReadStream, createWriteStream } from 'node:fs'
import { pipeline } from 'node:stream/promises'
import { createGzip } from 'node:zlib'

await pipeline(
  createReadStream('huge.csv'),
  createGzip(),
  createWriteStream('huge.csv.gz'),
)
```

```
❌ 一括読み込み        ✅ ストリーム
┌──────────┐          ┌──┐→┌──┐→┌──┐→
│  1GB     │  メモリ   └──┘ └──┘ └──┘
│  全部     │          少しずつ流すのでメモリは一定
└──────────┘
```

### 行単位で処理する

```js
import readline from 'node:readline'

const rl = readline.createInterface({
  input: createReadStream('huge.log'),
  crlfDelay: Infinity,
})

for await (const line of rl) {
  if (line.includes('ERROR')) console.log(line)
}
```

> 💡 **`pipeline` を使う理由**：`.pipe()` はエラー時にストリームを閉じ忘れることがあり、リソースリークの原因になります。`pipeline` は自動で後片付けをしてくれます。

---

## 6. その他のよく使う標準API

### `crypto` — ハッシュ・乱数

```js
import crypto from 'node:crypto'

crypto.randomUUID()                                     // ID生成
crypto.randomBytes(32).toString('hex')                  // トークン生成
crypto.createHash('sha256').update(data).digest('hex')  // ハッシュ

// 🚨 パスワードのハッシュには使わない（bcrypt/argon2を使う）
// 🚨 トークンの比較はタイミング攻撃対策を
crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b))
```

> ⚠️ **`Math.random()` をセキュリティ用途に使わない**でください。予測可能です。トークンやIDには `crypto.randomUUID()` / `randomBytes` を使います。

### `os` — システム情報

```js
import os from 'node:os'
os.platform()              // 'linux' / 'darwin' / 'win32'
os.availableParallelism()  // 利用可能なCPU数
os.totalmem() / os.freemem()
```

### `url` / `URLSearchParams`

```js
const url = new URL('https://example.com/path?q=abc')
url.searchParams.get('q')       // 'abc'
url.pathname                    // '/path'
```

### `AbortController` — 処理のキャンセル

```js
const controller = new AbortController()
setTimeout(() => controller.abort(), 3000)

await fetch(url, { signal: controller.signal })
```

### `node:test` — 標準テストランナー

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'

test('add', () => {
  assert.equal(add(1, 2), 3)
})
```

```bash
node --test
```

**追加ライブラリなしでテストが書けます。** 小規模ならこれで十分です（本格的にはVitest等が便利）。

---

## 7. ブラウザと共通のWeb標準API

近年のNode.jsは**ブラウザと同じAPI**を多く取り込んでいます。これによりフロント/バックでコードを共有しやすくなりました。

| API | 用途 | 対応 |
| --- | --- | --- |
| `fetch` | HTTP通信 | Node 18〜 |
| `URL` / `URLSearchParams` | URL操作 | ✅ |
| `AbortController` | キャンセル | ✅ |
| `structuredClone()` | 深いコピー | Node 17〜 |
| `TextEncoder` / `TextDecoder` | 文字コード変換 | ✅ |
| `Blob` / `FormData` | ファイル・フォーム | Node 18〜 |
| `crypto.subtle` | Web Crypto | ✅ |
| `setTimeout` 等 | タイマー | ✅ |

```js
// 深いコピーがライブラリなしでできる
const copy = structuredClone(complexObject)
```

---

## 8. よくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| サーバーが固まる | `readFileSync` 等の同期API | 非同期版を使う |
| 文字化けする | エンコーディング未指定 | `'utf-8'` を渡す |
| Windowsでパスが壊れる | 文字列結合 | `path.join()` |
| メモリ不足で落ちる | 巨大ファイルの一括読み込み | ストリーム処理 |
| `fetch` のエラーを検知できない | `res.ok` を見ていない | 明示的に確認 |
| 外部APIで固まる | タイムアウト未設定 | `AbortSignal.timeout()` |
| デプロイ時にリクエストが切れる | シャットダウン処理がない | SIGTERMを処理 |
| `process.env.X` が `undefined` | `.env` を読んでいない | `--env-file` / 起動時検証 |

---

## 9. この章のまとめ

- 🚨 **同期API（`*Sync`）はサーバーで使わない**。イベントループを止める
- パス操作は必ず **`path`**。ユーザー入力を使うときは**パストラバーサル対策**
- **環境変数は起動時にZod等で検証**する。秘密情報はコードに書かない
- **`fetch` は標準搭載**（Node 18〜）。`res.ok` の確認と**タイムアウト設定**を忘れない
- 巨大データは**ストリーム＋`pipeline`**。一括読み込みはメモリ不足の原因
- 乱数・トークンは **`crypto.randomUUID()`**。`Math.random()` は使わない
- **SIGTERMを処理してグレースフルシャットダウン**を実装する
- **標準APIで足りないか先に確認**する。`fetch`・`structuredClone`・`node:test` など標準化が進んでいる

---

次の章 → [⑤ 非同期処理を書きこなす](05-async-patterns.md)
