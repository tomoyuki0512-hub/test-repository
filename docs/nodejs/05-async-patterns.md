---
title: ⑤ 非同期処理を書きこなす
---

# ⑤ 非同期処理を書きこなす

[← 総合インデックスに戻る](README.md) ｜ 前 → [④ 標準APIを使う](04-core-apis.md) ｜ 次 → [⑥ サーバーとフレームワーク](06-server-frameworks.md)

[②](02-event-loop.md) で仕組みを理解しました。この章は **「正しく速く書く」実践編**です。Node.jsアプリの性能とバグの大半は、この章の内容で決まります。

---

## 1. Promise の基本

**Promise は「まだ結果が出ていない値」を表すオブジェクト**です。3つの状態を持ちます。

```
pending（処理中）
   ├─→ fulfilled（成功）… .then / await で値を受け取る
   └─→ rejected（失敗） … .catch / try-catch で捕まえる
```

```js
// async関数は必ずPromiseを返す
async function getUser(id) {
  return { id, name: '田中' }
}

getUser(1)          // Promise<{id, name}> が返る（オブジェクトではない）
await getUser(1)    // { id, name } が返る
```

> 🔑 **よくある間違い**：`const user = getUser(1)` とすると `user` は Promise オブジェクトです。`console.log(user)` すると `Promise { <pending> }` と表示されます。`await` を忘れているサインです。

---

## 2. 🚨 直列と並列 — 最も効く高速化

**これがNode.jsで最も重要なパフォーマンス改善**です。

### 直列（逐次）— 遅い

```js
// ❌ 合計 300 + 200 + 400 = 900ms
const user = await getUser(id)        // 300ms
const posts = await getPosts(id)      // 200ms
const stats = await getStats(id)      // 400ms
```

```
時間 →
getUser  ████████
getPosts         ██████
getStats               ████████████
                                    合計900ms
```

### 並列 — 速い

```js
// ✅ 合計 400ms（最も遅いものに律速）
const [user, posts, stats] = await Promise.all([
  getUser(id),
  getPosts(id),
  getStats(id),
])
```

```
時間 →
getUser  ████████
getPosts ██████
getStats ████████████
                     合計400ms
```

> 🔑 **判断基準**：「**互いの結果が必要か？**」→ 不要なら `Promise.all`。この1点を意識するだけで、APIの応答時間が半分以下になることは珍しくありません。

### ループの中の `await` は要注意

```js
// ❌ 100件 × 50ms = 5秒
for (const id of ids) {
  results.push(await fetchItem(id))
}

// ✅ 並列 → 50ms程度
const results = await Promise.all(ids.map((id) => fetchItem(id)))
```

### ⚠️ ただし並列にしすぎない

```js
// 🚨 1万件を一斉に実行 → 相手のAPIを落とす・DB接続が枯渇する
await Promise.all(tenThousandIds.map((id) => fetchItem(id)))
```

**同時実行数を制限する**必要があります。

```js
// 手動でチャンクに分ける
async function inBatches(items, size, fn) {
  const results = []
  for (let i = 0; i < items.length; i += size) {
    const chunk = items.slice(i, i + size)
    results.push(...await Promise.all(chunk.map(fn)))
  }
  return results
}

await inBatches(ids, 10, fetchItem)    // 10件ずつ
```

実務では **`p-limit`** パッケージが便利です。

```js
import pLimit from 'p-limit'
const limit = pLimit(5)                                   // 同時5件まで
await Promise.all(ids.map((id) => limit(() => fetchItem(id))))
```

---

## 3. Promise の各メソッド

| メソッド | 挙動 | 使いどころ |
| --- | --- | --- |
| **`Promise.all`** | 全部成功で成功。**1つ失敗したら即失敗** | 全部必要なとき |
| **`Promise.allSettled`** | 全部の結果を待つ（成功も失敗も） | **一部失敗を許容するとき** |
| **`Promise.race`** | 最初に決着したものを返す | タイムアウト実装 |
| **`Promise.any`** | 最初に**成功**したものを返す | 複数ミラーから取得 |

### `allSettled` — 部分的な失敗を許す

```js
const results = await Promise.allSettled([
  fetchWeather(),
  fetchNews(),
  fetchStocks(),
])

for (const r of results) {
  if (r.status === 'fulfilled') {
    render(r.value)
  } else {
    logger.warn({ err: r.reason }, '一部の取得に失敗')
  }
}
```

**ダッシュボードなど「一部が取れなくても画面は出したい」場面で必須**です。`Promise.all` だと1つの失敗で全滅します。

### `race` でタイムアウト

```js
const result = await Promise.race([
  fetchData(),
  new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 5000)),
])
```

> 💡 `fetch` なら `AbortSignal.timeout(5000)` のほうが簡潔です（→ [④](04-core-apis.md)）。

---

## 4. 🚨 エラーハンドリング

非同期のエラーは**普通のtry/catchから漏れやすい**ため、注意が必要です。

### 基本

```js
try {
  const data = await fetchData()
  return data
} catch (err) {
  logger.error({ err }, 'データ取得に失敗')
  throw new AppError('データを取得できませんでした', { cause: err })
}
```

### ❌ 漏れるパターン

```js
// ❌ コールバック内のエラーはtry/catchで捕まらない
try {
  setTimeout(() => {
    throw new Error('これは捕まらない')    // プロセスがクラッシュする
  }, 100)
} catch (e) {
  // ここには来ない
}

// ❌ awaitを付け忘れると捕まらない
try {
  saveData()          // awaitがない → Promiseが投げたエラーは外へ漏れる
} catch (e) {
  // ここには来ない
}
```

> 🚨 **`await` の付け忘れは、Node.jsで最も見つけにくいバグの1つ**です。ESLintの `@typescript-eslint/no-floating-promises` ルールを有効にすると自動検出できます。**必ず設定してください。**

### エラーの型を絞る（TypeScript）

```ts
try {
  await risky()
} catch (err) {
  // catchされる値は unknown 型（何でも投げられるため）
  if (err instanceof AppError) {
    return { status: err.statusCode, message: err.message }
  }
  if (err instanceof Error) {
    logger.error({ err }, 'unexpected')
  }
  throw err
}
```

### カスタムエラークラス

```ts
class AppError extends Error {
  constructor(
    message: string,
    public statusCode = 500,
    options?: { cause?: unknown },
  ) {
    super(message, options)
    this.name = 'AppError'
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} が見つかりません`, 404)
  }
}
```

**`cause` を使うと元のエラーを保持できます**（Node.js 16.9〜）。ログで原因を追跡しやすくなります。

### プロセス全体の保険

```js
process.on('unhandledRejection', (reason) => {
  logger.fatal({ err: reason }, 'Unhandled rejection')
  process.exit(1)      // ログを出してから終了する
})

process.on('uncaughtException', (err) => {
  logger.fatal({ err }, 'Uncaught exception')
  process.exit(1)
})
```

> ⚠️ **これは「保険」であって「対処」ではありません。** ここに到達した時点でアプリの状態は信用できないため、**ログを出して終了する**のが正しい対応です。プロセスマネージャやコンテナオーケストレータが再起動してくれます。「握りつぶして動き続ける」のは危険です。

---

## 5. リトライとタイムアウト

外部APIやDBは**必ず失敗するもの**として設計します。

### 指数バックオフ付きリトライ

```js
async function retry(fn, { retries = 3, baseDelay = 200 } = {}) {
  let lastError
  for (let i = 0; i <= retries; i++) {
    try {
      return await fn()
    } catch (err) {
      lastError = err
      if (i === retries) break
      // 待機時間を倍々にし、ランダム値を加える（jitter）
      const delay = baseDelay * 2 ** i + Math.random() * 100
      await new Promise((r) => setTimeout(r, delay))
    }
  }
  throw lastError
}

const data = await retry(() => fetchFromFlakeyApi())
```

> 🔑 **ジッター（ランダム値）を入れる理由**：全クライアントが同時にリトライすると、復旧しかけたサーバーを再び倒します（thundering herd問題）。

### ⚠️ リトライしてはいけないケース

| 状況 | 理由 |
| --- | --- |
| 4xx エラー（400・401・404） | 何度やっても結果は同じ |
| **決済・注文などの副作用がある処理** | **二重実行のリスク** |
| ユーザーが待っている同期処理 | 待ち時間が伸びるだけ |

決済のような処理でリトライが必要なら、**冪等キー**（同じキーなら1回しか実行しない仕組み）とセットにしてください。

---

## 6. 非同期の反復処理

### `for await...of`

```js
// 非同期イテレータを順番に処理
for await (const line of readLines('huge.log')) {
  process(line)
}
```

### 非同期ジェネレータ

```js
// ページネーションAPIを全件取得する
async function* fetchAllPages(url) {
  let next = url
  while (next) {
    const res = await fetch(next).then((r) => r.json())
    yield* res.items
    next = res.nextUrl
  }
}

for await (const item of fetchAllPages('/api/items')) {
  console.log(item)      // メモリに全件載せずに処理できる
}
```

**全件をメモリに載せずに処理できる**のが利点です。件数が読めないAPIを扱うときに有効です。

---

## 7. 実践例：外部API連携の完成形

これまでの要素を組み合わせた、実務で通用する形です。

```ts
import pLimit from 'p-limit'

const limit = pLimit(5)

async function fetchUserSafely(id: string): Promise<User | null> {
  try {
    const res = await fetch(`${API_BASE}/users/${id}`, {
      headers: { Authorization: `Bearer ${env.API_KEY}` },
      signal: AbortSignal.timeout(5000),         // ① タイムアウト
    })

    if (res.status === 404) return null           // ② 想定内はエラーにしない
    if (!res.ok) throw new AppError(`API error: ${res.status}`)

    return UserSchema.parse(await res.json())     // ③ レスポンスを検証
  } catch (err) {
    logger.warn({ err, id }, 'ユーザー取得に失敗')
    return null                                    // ④ 呼び出し側で扱える形に
  }
}

export async function fetchUsers(ids: string[]) {
  // ⑤ 同時実行数を制限しつつ並列化
  const results = await Promise.all(
    ids.map((id) => limit(() => fetchUserSafely(id))),
  )
  return results.filter((u): u is User => u !== null)
}
```

| # | ポイント |
| --- | --- |
| ① | **タイムアウト**がないと永久に待つ |
| ② | 404は「エラー」ではなく「見つからない」として扱う |
| ③ | 外部データは**Zodで検証**（型は実行時には存在しない） |
| ④ | 呼び出し側が扱いやすい形（`null`）に変換 |
| ⑤ | **並列化しつつ同時実行数を制限** |

---

## 8. よくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| `Promise { <pending> }` と表示される | `await` 忘れ | `await` を付ける |
| 処理が終わる前に次へ進む | `forEach` 内の `await` | `for...of` / `Promise.all` |
| 極端に遅い | ループ内の直列 `await` | `Promise.all` |
| 相手のAPIを落とした | 並列数が無制限 | `p-limit` で制限 |
| 一部の失敗で全部止まる | `Promise.all` | `Promise.allSettled` |
| エラーが捕まらない | `await` 忘れ／コールバック内 | `no-floating-promises` を有効化 |
| プロセスが突然落ちる | unhandledRejection | ハンドラでログを出して終了 |
| 永久に応答が返らない | タイムアウト未設定 | `AbortSignal.timeout()` |

---

## 9. この章のまとめ

- **`async` 関数は必ずPromiseを返す**。`await` 忘れは `Promise { <pending> }` で気づく
- 🚨 **依存関係がなければ `Promise.all` で並列化**。最も効く高速化
- **ループ内の `await` は直列**。`map` + `Promise.all` に置き換える
- ただし**並列にしすぎない**。`p-limit` で同時実行数を制限する
- 一部失敗を許容するなら **`Promise.allSettled`**
- 🚨 **`await` 忘れはエラーを漏らす**。ESLintの `no-floating-promises` を必ず有効に
- `unhandledRejection` は**ログを出して終了**する（握りつぶさない）
- リトライは**指数バックオフ＋ジッター**。**副作用のある処理は冪等キーとセット**
- 外部API連携では**タイムアウト・検証・同時実行制限**を必ず入れる

---

次の章 → [⑥ サーバーとフレームワーク](06-server-frameworks.md)
