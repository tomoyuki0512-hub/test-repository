---
title: ⑨ Route HandlersとAPI連携
---

# ⑨ Route HandlersとAPI連携 — `route.ts` と `proxy.ts`

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑧ 認証とデータベース](08-auth-database.md) ｜ 次 → [⑩ パフォーマンス最適化とSEO](10-performance-seo.md)

[⑥](06-server-actions-forms.md) の Server Actions で多くの更新処理は書けますが、**外部に公開するAPI**や**リクエストを横断的に処理する仕組み**は別途必要です。この章ではその2つを扱います。

---

## 1. Route Handlers（`route.ts`）

`page.tsx` の代わりに `route.ts` を置くと、**そのURLがAPIエンドポイント**になります。

```
app/api/posts/route.ts        →  /api/posts
app/api/posts/[id]/route.ts   →  /api/posts/123
```

```ts
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const q = request.nextUrl.searchParams.get('q')
  const posts = await db.post.findMany({
    where: q ? { title: { contains: q } } : undefined,
  })
  return NextResponse.json(posts)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const post = await db.post.create({ data: body })
  return NextResponse.json(post, { status: 201 })
}
```

`GET` `POST` `PUT` `PATCH` `DELETE` `HEAD` `OPTIONS` をエクスポートできます。

### 動的パラメータ

```ts
// app/api/posts/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },   // ⚠️ Promise
) {
  const { id } = await params
  const post = await db.post.findUnique({ where: { id } })
  if (!post) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  return NextResponse.json(post)
}
```

### Server Actions との使い分け

| 用途 | 使うもの |
| --- | --- |
| 画面のフォーム送信・更新処理 | **Server Actions**（→ [⑥](06-server-actions-forms.md)） |
| 外部サービスからのWebhook受信 | **Route Handler** |
| モバイルアプリ・他システム向けAPI | **Route Handler** |
| OAuthコールバック | **Route Handler** |
| ファイル配信・OG画像生成 | **Route Handler** |
| cron/定期実行の受け口 | **Route Handler** |

> 🔑 **判断基準**：「**自分の画面からしか呼ばれない**」なら Server Actions、「**外部から決まったURLで叩かれる**」なら Route Handler。

---

## 2. 実務でよく書くRoute Handler

### ① Webhook受信（署名検証は必須）

```ts
// app/api/webhooks/stripe/route.ts
import { headers } from 'next/headers'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(request: Request) {
  const body = await request.text()          // ⚠️ json() ではなく text()
  const signature = (await headers()).get('stripe-signature')!

  let event: Stripe.Event
  try {
    // 🚨 署名検証。これがないと誰でも偽のWebhookを送れる
    event = stripe.webhooks.constructEvent(
      body, signature, process.env.STRIPE_WEBHOOK_SECRET!,
    )
  } catch {
    return new Response('Invalid signature', { status: 400 })
  }

  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckout(event.data.object)
      break
  }

  return NextResponse.json({ received: true })
}
```

> 🚨 **Webhookで必ず守る2点**
> 1. **署名検証**：これを省くと、誰でも「支払いが完了した」という嘘のリクエストを送れます
> 2. **冪等性**：Webhookは**同じイベントが複数回届く前提**です。イベントIDを保存し、処理済みならスキップしてください

### ② OG画像の動的生成

```tsx
// app/api/og/route.tsx
import { ImageResponse } from 'next/og'

export async function GET(request: Request) {
  const title = new URL(request.url).searchParams.get('title') ?? 'My Site'
  return new ImageResponse(
    (
      <div style={{
        display: 'flex', width: '100%', height: '100%',
        alignItems: 'center', justifyContent: 'center',
        fontSize: 60, background: '#0f172a', color: 'white',
      }}>
        {title}
      </div>
    ),
    { width: 1200, height: 630 },
  )
}
```

SNSシェア時のカード画像を記事ごとに自動生成できます（→ [⑩](10-performance-seo.md)）。

### ③ 定期実行（cron）の受け口

```ts
// app/api/cron/cleanup/route.ts
export async function GET(request: Request) {
  // 🚨 認証必須。公開URLなので誰でも叩ける
  const authHeader = request.headers.get('authorization')
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 })
  }
  await db.session.deleteMany({ where: { expiresAt: { lt: new Date() } } })
  return NextResponse.json({ ok: true })
}
```

Vercelなら `vercel.json` でスケジュールを設定します。

```json
{ "crons": [{ "path": "/api/cron/cleanup", "schedule": "0 3 * * *" }] }
```

---

## 3. `proxy.ts`（旧 `middleware.ts`）

**全リクエストの手前で動く処理**です。Next.js 16 で `middleware.ts` から改称されました。

```ts
// proxy.ts （プロジェクトルート、src/ を使うなら src/proxy.ts）
import { NextRequest, NextResponse } from 'next/server'

export function proxy(request: NextRequest) {
  const isLoggedIn = Boolean(request.cookies.get('session'))
  const { pathname } = request.nextUrl

  if (pathname.startsWith('/dashboard') && !isLoggedIn) {
    const url = new URL('/login', request.url)
    url.searchParams.set('from', pathname)
    return NextResponse.redirect(url)
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    // 静的ファイル・画像最適化・favicon を除外
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}
```

### ⚠️ Next.js 16 での変更点

| 項目 | 15以前 | 16 |
| --- | --- | --- |
| ファイル名 | `middleware.ts` | **`proxy.ts`** |
| 関数名 | `middleware` | **`proxy`** |
| ランタイム | Edge（既定） | **Node.js**（変更不可） |

> 🚨 **移行時の最大の落とし穴**：`middleware.ts` を残したままアップグレードすると、**エラーが出ないまま単に実行されなくなります**。「気づかないうちに認証リダイレクトが無効化されていた」という事故が報告されています。アップグレード後は必ず、未ログイン状態で保護対象URLにアクセスして動作を確認してください。
>
> `next-intl` など `middleware.ts` を前提とするライブラリも、対応バージョンへの更新が必要です。

### 向いている用途／向いていない用途

| ✅ 向いている | ❌ 向いていない |
| --- | --- |
| 未ログイン時のリダイレクト（UX） | **本格的な認可**（→ [⑧](08-auth-database.md#3--認可authorizationをどこに置くか)） |
| A/Bテストの振り分け | DBアクセスを伴う重い処理 |
| 多言語のロケール判定 | データ取得 |
| セキュリティヘッダーの付与 | 複雑なビジネスロジック |
| Bot判定・地域制限 | — |

**全リクエストで動くため、重い処理を書くとサイト全体が遅くなります。** 軽く保つのが原則です。

---

## 4. 外部APIとの連携

### 型安全に扱う

外部APIのレスポンスは `any` になりがちです。**Zodで境界を検証**すると安全になります。

```ts
import { z } from 'zod'

const WeatherSchema = z.object({
  temp: z.number(),
  condition: z.string(),
})

export async function getWeather(city: string) {
  'use cache'
  const res = await fetch(`https://api.example.com/weather?city=${city}`, {
    headers: { Authorization: `Bearer ${process.env.WEATHER_API_KEY}` },
  })
  if (!res.ok) throw new Error(`Weather API failed: ${res.status}`)

  // 実際の形が想定と違えばここで落ちる → 原因が特定しやすい
  return WeatherSchema.parse(await res.json())
}
```

> 💡 **APIキーはServer Componentか Route Handler の中でのみ使う**。Client Componentから外部APIを直接呼ぶと、キーがブラウザに露出します（→ [②の環境変数](02-setup-and-structure.md#環境変数envlocal)）。

### タイムアウトとリトライ

外部APIが応答しないと、ページ全体が固まります。

```ts
export async function fetchWithTimeout(url: string, ms = 5000) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), ms)
  try {
    return await fetch(url, { signal: controller.signal })
  } finally {
    clearTimeout(timer)
  }
}
```

### CORS（外部サイトから呼ばれる場合）

```ts
export async function OPTIONS() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': 'https://trusted-site.example',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}
```

> ⚠️ `Access-Control-Allow-Origin: *` は**認証付きAPIでは使わない**でください。許可するオリジンは明示的に列挙します。

---

## 5. Route Handler のセキュリティ

Server Actions と同様、**`route.ts` は公開エンドポイント**です。

```ts
export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  // ① 認証
  const session = await auth()
  if (!session?.user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // ② 認可（所有者条件をクエリに含める）
  const { id } = await params
  const deleted = await db.post.deleteMany({
    where: { id, authorId: session.user.id },
  })
  if (deleted.count === 0) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }

  return new Response(null, { status: 204 })
}
```

チェックリスト：

- [ ] 認証・認可をハンドラ内で確認している
- [ ] 入力（body / query / params）をZod等で検証している
- [ ] レート制限をかけている（特に公開API・ログイン系）
- [ ] エラーメッセージにDB構造や内部パスを含めていない
- [ ] Webhookは**署名検証**と**冪等化**をしている
- [ ] cronエンドポイントに**シークレット認証**をかけている

---

## 6. この章のまとめ

- `route.ts` を置けばそのURLがAPIになる。`GET`/`POST`... をexportする
- **「自分の画面からしか呼ばれない」→ Server Actions、「外部から叩かれる」→ Route Handler**
- Webhookは**署名検証**と**冪等化**が必須。`request.text()` で生のbodyを取る
- **`middleware.ts` は Next.js 16 で `proxy.ts` に改称**。放置すると無言で動かなくなる
- `proxy.ts` は軽く保つ。**認可の本体はデータアクセス層に置く**
- 外部APIのレスポンスは **Zodで検証**し、タイムアウトを設定する

---

次の章 → [⑩ パフォーマンス最適化とSEO](10-performance-seo.md)
