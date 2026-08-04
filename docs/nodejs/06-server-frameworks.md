---
title: ⑥ サーバーとフレームワーク
---

# ⑥ サーバーとフレームワーク — Express・Fastify・Hono・NestJS

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑤ 非同期処理を書きこなす](05-async-patterns.md) ｜ 次 → [⑦ 実務・運用](07-practice-operations.md)

実際にAPIサーバーを作ります。**フレームワークの選び方**と、**Next.jsを使う場合に別サーバーが要るのか**という判断も扱います。

---

## 1. フレームワークの比較

| | **Express** | **Fastify** | **Hono** | **NestJS** |
| --- | --- | --- | --- | --- |
| 特徴 | 最も普及・情報量最大 | 高速・スキーマ検証内蔵 | 超軽量・エッジ対応 | 構造化・大規模向け |
| 学習コスト | 低 | 低〜中 | 低 | **高** |
| 速度 | 標準 | **速い** | **速い** | 標準 |
| 型安全 | 弱い | 中 | **強い** | 強い |
| 実行環境 | Node.js | Node.js | Node/Deno/Bun/**エッジ** | Node.js |
| 向いている場面 | 学習・既存資産・小〜中規模 | 性能が要る中〜大規模 | エッジ・軽量API | 大規模・チーム開発 |

### 選び方

```
初めて学ぶ・情報量重視・既存プロジェクトがExpress
    → Express

性能を重視・スキーマ検証を標準で使いたい
    → Fastify

Cloudflare Workers等のエッジで動かす・型安全重視
    → Hono

大人数・長期運用・DIやレイヤ構造をきちんと敷きたい
    → NestJS（ただし学習コストは高い）
```

> 💡 **Next.jsを使うなら、多くの場合これらは不要**です。Route Handlers（[Next.js⑨](../nextjs/09-route-handlers-api.md)）がAPIの役割を果たします。別サーバーが必要になるのは「モバイルアプリ専用のAPI」「画面を持たないバックエンド」「重いバッチ処理」などの場合です。

---

## 2. Express の基本

```bash
npm install express
npm install -D @types/express
```

```ts
import express from 'express'

const app = express()

app.use(express.json())                    // JSONボディをパース

app.get('/health', (req, res) => {
  res.json({ status: 'ok' })
})

app.get('/users/:id', async (req, res) => {
  const user = await db.user.findUnique({ where: { id: req.params.id } })
  if (!user) return res.status(404).json({ error: 'Not found' })
  res.json(user)
})

app.post('/users', async (req, res) => {
  const user = await db.user.create({ data: req.body })
  res.status(201).json(user)
})

app.listen(3000, () => console.log('http://localhost:3000'))
```

### ミドルウェア — Expressの中心概念

**リクエストが順番に通過していく処理のパイプライン**です。

```
リクエスト
   ↓
[ログ記録] → [JSONパース] → [認証] → [ルートハンドラ] → レスポンス
                                ↓ 失敗
                          [エラーハンドラ]
```

```ts
// 自作ミドルウェア
function requestLogger(req, res, next) {
  const start = Date.now()
  res.on('finish', () => {
    logger.info({ method: req.method, url: req.url, status: res.statusCode, ms: Date.now() - start })
  })
  next()      // ★次へ渡す。呼ばないとリクエストが固まる
}

app.use(requestLogger)
```

### 🚨 エラーハンドラは4引数

```ts
// ★引数が4つであることでエラーハンドラと認識される
app.use((err, req, res, next) => {
  logger.error({ err }, 'Unhandled error')

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ error: err.message })
  }
  // 🚨 内部情報を漏らさない
  res.status(500).json({ error: 'Internal Server Error' })
})
```

**必ず最後に登録**してください。順序が重要です。

> ⚠️ **Express 4 では非同期エラーが自動で捕まりません。**
> ```ts
> // ❌ Express 4：この例外は捕まらずプロセスが落ちる
> app.get('/x', async (req, res) => { throw new Error('boom') })
> ```
> **Express 5 以降は非同期エラーも自動でエラーハンドラに渡されます。** Express 4 を使う場合は `express-async-errors` を導入するか、各ハンドラを try/catch で包んでください。

---

## 3. バリデーションは必須

**クライアントから来るデータは一切信用できません。**

```ts
import { z } from 'zod'

const CreateUserSchema = z.object({
  name: z.string().min(1).max(50),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
})

app.post('/users', async (req, res) => {
  const parsed = CreateUserSchema.safeParse(req.body)
  if (!parsed.success) {
    return res.status(400).json({ errors: z.flattenError(parsed.error).fieldErrors })
  }
  const user = await db.user.create({ data: parsed.data })   // ここから先は型安全
  res.status(201).json(user)
})
```

### 検証すべき箇所

- [ ] リクエストボディ
- [ ] URLパラメータ（`req.params`）
- [ ] クエリ文字列（`req.query`）
- [ ] ヘッダー（認証トークン等）
- [ ] **外部APIからのレスポンス**（→ [⑤](05-async-patterns.md)）

> 🔑 **TypeScriptの型は実行時に存在しません。** `req.body as CreateUserInput` と書いても、実際に何が来るかは保証されません。**実行時の検証（Zod等）が必須**です。

---

## 4. 認証と認可

```ts
// 認証ミドルウェア
async function authenticate(req, res, next) {
  const header = req.headers.authorization
  if (!header?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Unauthorized' })
  }

  try {
    const payload = jwt.verify(header.slice(7), env.JWT_SECRET)
    req.user = await db.user.findUnique({ where: { id: payload.sub } })
    if (!req.user) return res.status(401).json({ error: 'Unauthorized' })
    next()
  } catch {
    return res.status(401).json({ error: 'Invalid token' })
  }
}

// 認可（権限チェック）
function requireRole(role: string) {
  return (req, res, next) => {
    if (req.user?.role !== role) {
      return res.status(403).json({ error: 'Forbidden' })
    }
    next()
  }
}

app.get('/admin/users', authenticate, requireRole('admin'), handler)
```

### 🚨 所有者チェックを忘れない

```ts
// ❌ ログインしていれば他人の投稿も削除できてしまう
app.delete('/posts/:id', authenticate, async (req, res) => {
  await db.post.delete({ where: { id: req.params.id } })
})

// ✅ 所有者条件をクエリに含める
app.delete('/posts/:id', authenticate, async (req, res) => {
  const result = await db.post.deleteMany({
    where: { id: req.params.id, authorId: req.user.id },
  })
  if (result.count === 0) return res.status(404).json({ error: 'Not found' })
  res.status(204).end()
})
```

**「認証（誰か）」と「認可（何をしてよいか）」は別物**です。認証だけで満足すると、他人のデータを操作できる脆弱性が残ります。

---

## 5. REST API の設計

### URL設計

```
GET    /users           一覧
GET    /users/:id       個別取得
POST   /users           作成
PATCH  /users/:id       部分更新
PUT    /users/:id       全体置換
DELETE /users/:id       削除

GET    /users/:id/posts ネストしたリソース
```

| 原則 | 例 |
| --- | --- |
| 名詞の複数形を使う | `/users`（`/getUser` ではない） |
| 動詞はHTTPメソッドで表す | `POST /users`（`/createUser` ではない） |
| ネストは2階層まで | `/users/1/posts` はOK、それ以上は避ける |
| フィルタはクエリで | `/users?role=admin&page=2` |

### ステータスコード

| コード | 意味 | 使う場面 |
| --- | --- | --- |
| 200 | OK | 取得・更新成功 |
| 201 | Created | 作成成功 |
| 204 | No Content | 削除成功（本文なし） |
| 400 | Bad Request | バリデーションエラー |
| 401 | Unauthorized | **未認証**（ログインしていない） |
| 403 | Forbidden | **権限なし**（ログイン済みだが不許可） |
| 404 | Not Found | リソースが存在しない |
| 409 | Conflict | 重複（メールアドレスが既に存在等） |
| 422 | Unprocessable Entity | 意味的に処理できない |
| 429 | Too Many Requests | レート制限 |
| 500 | Internal Server Error | サーバー側のエラー |

> 💡 **401 と 403 の違い**：401は「あなたが誰かわからない」、403は「あなたが誰かはわかるが、許可されていない」。混同されがちですが、クライアント側の挙動（ログイン画面へ飛ばすか、エラーを出すか）が変わります。

### ページネーション

```ts
// オフセット方式（実装が簡単・ページ番号を出せる）
app.get('/posts', async (req, res) => {
  const page = Number(req.query.page ?? 1)
  const limit = Math.min(Number(req.query.limit ?? 20), 100)   // ★上限を設ける

  const [items, total] = await Promise.all([
    db.post.findMany({ skip: (page - 1) * limit, take: limit }),
    db.post.count(),
  ])

  res.json({ items, total, page, totalPages: Math.ceil(total / limit) })
})
```

> ⚠️ **`limit` に上限を設けないと、`?limit=999999` で全件取得されサーバーが落ちます。** 実際によくある攻撃・事故のパターンです。件数が多い場合はカーソル方式（`?after=<id>`）のほうが高速です。

---

## 6. 本番用のセキュリティ設定

```ts
import helmet from 'helmet'
import cors from 'cors'
import rateLimit from 'express-rate-limit'
import compression from 'compression'

app.use(helmet())                       // セキュリティヘッダー
app.use(compression())                  // gzip圧縮
app.use(express.json({ limit: '1mb' })) // ★ボディサイズ上限

app.use(cors({
  origin: ['https://myapp.example'],    // ★ '*' は使わない
  credentials: true,
}))

app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000,
  limit: 100,
  standardHeaders: 'draft-7',
}))

// ログイン系はさらに厳しく（総当たり対策）
app.use('/api/auth/login', rateLimit({ windowMs: 15 * 60 * 1000, limit: 5 }))
```

### チェックリスト

- [ ] `helmet` でセキュリティヘッダーを設定
- [ ] CORSのoriginを**明示的に列挙**（`*` を使わない）
- [ ] **ボディサイズの上限**を設定
- [ ] レート制限（特にログイン・パスワードリセット）
- [ ] 入力を**すべてバリデーション**
- [ ] SQLは**必ずパラメータ化**（ORMを使えば自動）
- [ ] エラーレスポンスに**スタックトレースを含めない**
- [ ] 秘密情報は環境変数（→ [④](04-core-apis.md)）

---

## 7. Fastify と Hono の例

### Fastify — スキーマ駆動

```ts
import Fastify from 'fastify'

const app = Fastify({ logger: true })   // ログ機能が標準搭載

app.post('/users', {
  schema: {
    body: {
      type: 'object',
      required: ['name', 'email'],
      properties: {
        name: { type: 'string', minLength: 1 },
        email: { type: 'string', format: 'email' },
      },
    },
  },
}, async (request, reply) => {
  const user = await db.user.create({ data: request.body })
  reply.code(201).send(user)
})

await app.listen({ port: 3000 })
```

**スキーマを書くだけで検証・シリアライズ・ドキュメント生成が効く**のが利点です。

### Hono — 軽量・型安全・どこでも動く

```ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'

const app = new Hono()

app.get('/users/:id', async (c) => {
  const user = await getUser(c.req.param('id'))
  return c.json(user)
})

app.post('/users', zValidator('json', CreateUserSchema), async (c) => {
  const data = c.req.valid('json')      // ★型が付いている
  return c.json(await createUser(data), 201)
})

export default app
```

Node.js・Bun・Deno・Cloudflare Workers・Vercel で**同じコードが動きます**。

---

## 8. Next.js を使う場合の判断

```
Next.jsのRoute Handlersで足りる？

画面（フロント）と同じプロジェクトでよい
  → ✅ Next.jsのRoute Handlers（別サーバー不要）

モバイルアプリ・他システムからも呼ばれる
  → 独立したAPIサーバーを検討（Express / Fastify / Hono / NestJS）

重いバッチ処理・長時間実行がある
  → 別サーバー or ジョブキュー（Next.jsのサーバーレス環境は実行時間制限がある）

WebSocketによる常時接続が必要
  → 別サーバー（サーバーレス環境では扱いにくい）

すでにバックエンドチームが別言語で運用している
  → そのまま。Next.jsはフロント＋BFFとして使う
```

詳しくは [Next.js⑨ Route HandlersとAPI連携](../nextjs/09-route-handlers-api.md) を参照してください。

---

## 9. この章のまとめ

- フレームワークは **Express（情報量）/ Fastify（性能）/ Hono（軽量・エッジ）/ NestJS（大規模）**
- Expressの中心は**ミドルウェア**。`next()` を呼ばないとリクエストが固まる
- **エラーハンドラは4引数で最後に登録**。Express 4 は非同期エラーを自動で捕まえない
- 🚨 **入力は必ず実行時に検証**（Zod等）。TypeScriptの型は実行時に存在しない
- **認証と認可は別物**。所有者条件をクエリに含める
- ステータスコードの **401（未認証）と 403（権限なし）** を使い分ける
- **`limit` に上限を設ける**。設けないと全件取得で落ちる
- 本番では **helmet・CORS制限・ボディサイズ上限・レート制限** を必ず入れる
- **Next.jsを使うなら別サーバーは多くの場合不要**。モバイルAPI・WebSocket・重い処理が必要なときだけ

---

次の章 → [⑦ 実務・運用](07-practice-operations.md)
