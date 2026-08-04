---
title: ⑧ 認証とデータベース
---

# ⑧ 認証とデータベース — Auth.js / Clerk / Prisma / Drizzle

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑦ スタイリングとUI](07-styling-ui.md) ｜ 次 → [⑨ Route HandlersとAPI連携](09-route-handlers-api.md)

Next.js は認証機能もORMも内蔵していません。**ここで何を選ぶかがプロジェクトの寿命を左右します**。この章では選定基準と、正しい認可の置き場所を扱います。

---

## 1. データベースとORM

### ORMの選択肢

| ORM | 特徴 | 向いている場面 |
| --- | --- | --- |
| **Prisma** | 独自スキーマ言語＋強力な型生成。ツールが充実 | 学習コスト重視・チーム開発・管理画面が要る |
| **Drizzle** | TypeScriptでスキーマを書く。SQLに近く軽量 | パフォーマンス重視・SQLを把握したい・エッジ環境 |
| **Kysely** | 型安全なクエリビルダ（ORMではない） | SQLを自分で書きたい |
| 生SQL | `postgres.js` 等 | 小規模・既存DBが複雑 |

### Prisma の例

```prisma
// prisma/schema.prisma
model Post {
  id        String   @id @default(cuid())
  title     String
  body      String
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())

  @@index([authorId])
}
```

```ts
// lib/db.ts — 開発時のホットリロードで接続が増え続けるのを防ぐ定型句
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient }

export const db = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db
```

> ⚠️ この「グローバルに1つだけ持つ」パターンは**必ず入れてください**。入れないと開発中に `Too many connections` でDBが停止します。Drizzle等でも同様の考慮が要ります。

### Drizzle の例

```ts
// db/schema.ts
import { pgTable, text, boolean, timestamp } from 'drizzle-orm/pg-core'

export const posts = pgTable('posts', {
  id: text('id').primaryKey(),
  title: text('title').notNull(),
  published: boolean('published').default(false),
  authorId: text('author_id').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
})
```

```ts
const rows = await db.select().from(posts).where(eq(posts.authorId, userId))
```

### Prisma と Drizzle の選び方

```
SQLをあまり書きたくない・チームの経験が浅い・管理画面(Prisma Studio)が欲しい
    → Prisma

SQLを把握しておきたい・バンドルサイズや起動速度を詰めたい・エッジで動かす
    → Drizzle

既存の複雑なDBに後付けする
    → Kysely または 生SQL
```

どちらも実務で十分に使われています。**チームが読めるかどうか**で決めるのが失敗しにくい基準です。

### データベース本体

| サービス | 種類 | 特徴 |
| --- | --- | --- |
| **Neon** | PostgreSQL | サーバーレス。ブランチ機能がPRごとの検証に便利 |
| **Supabase** | PostgreSQL＋認証＋ストレージ | 一式そろう。個人開発〜中規模で人気 |
| **PlanetScale** | MySQL | スキーマ変更が安全 |
| **Turso** | SQLite | エッジ分散。軽量用途 |
| **Vercel Postgres** | PostgreSQL | Vercelと統合が容易 |
| 自前RDS/Cloud SQL | 任意 | 企業要件・既存資産がある場合 |

> 💡 **サーバーレス環境での注意**：関数が都度起動するため、通常のコネクションプールが機能しません。**接続プーラー**（Neonのpooled接続、Supabaseの Supavisor、PgBouncer）を経由する接続文字列を使ってください。これを忘れると本番でDB接続が枯渇します。

---

## 2. 認証（Authentication）

### 選択肢

| 方式 | 概要 | 月額目安 | 向いている場面 |
| --- | --- | --- | --- |
| **Auth.js (NextAuth v5)** | 自前ホスト。OSS・無料 | 無料 | コスト重視・DBを自分で持ちたい |
| **Better Auth** | TypeScript製の新しいOSS。機能が豊富 | 無料 | 型安全・拡張性重視。近年採用が増加 |
| **Clerk** | SaaS。UI込みで最速 | 無料枠あり→従量 | 開発速度最優先・MFAや組織機能が要る |
| **Supabase Auth** | SupabaseのDBとセット | 無料枠あり | Supabaseを使うなら自然 |
| **Auth0 / Cognito** | エンタープライズSaaS | 従量 | 企業要件・既存IdPとの統合 |
| 自前実装 | 自分で全部書く | — | **原則おすすめしない** |

> 🚨 **認証の自前実装は避けてください。** パスワードハッシュ、セッション管理、CSRF、トークンローテーション、パスワードリセット、アカウント列挙対策……どれか1つでも間違えると重大な事故になります。既存ライブラリを使うのが最も安全です。

### Auth.js（NextAuth v5）の最小構成

```ts
// auth.ts
import NextAuth from 'next-auth'
import GitHub from 'next-auth/providers/github'
import { PrismaAdapter } from '@auth/prisma-adapter'
import { db } from '@/lib/db'

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(db),
  providers: [GitHub],
  session: { strategy: 'database' },
})
```

```ts
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth'
export const { GET, POST } = handlers
```

```tsx
// Server Component からセッションを読む
import { auth } from '@/auth'

export default async function Page() {
  const session = await auth()
  if (!session) return <p>ログインしてください</p>
  return <p>こんにちは、{session.user?.name}さん</p>
}
```

### Clerk の最小構成

```tsx
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html lang="ja"><body>{children}</body></html>
    </ClerkProvider>
  )
}
```

```tsx
import { auth, currentUser } from '@clerk/nextjs/server'

export default async function Page() {
  const { userId } = await auth()
  if (!userId) redirect('/sign-in')
  const user = await currentUser()
  return <p>{user?.firstName}</p>
}
```

ログイン画面・パスワードリセット・MFA・組織管理まで最初から付いてきます。**時間を金で買う**選択です。

### セッション方式の違い

| | JWT（トークン） | データベースセッション |
| --- | --- | --- |
| 保存先 | Cookieの中に情報を含む | DBに保存、CookieにはIDのみ |
| DB負荷 | なし | 毎回参照 |
| 即時失効 | **難しい**（有効期限まで有効） | **簡単**（DBから消すだけ） |
| 向いている場面 | 大規模・エッジ | 管理者による強制ログアウトが要る場合 |

> 「退会したユーザーがまだログインできる」という要件違反は、JWT方式で失効設計を怠った場合に起きます。**強制ログアウトが要件にあるならDBセッション**を選んでください。

---

## 3. 🚨 認可（Authorization）をどこに置くか

**この節がこの章で最も重要です。** 認証（誰か）ができていても、認可（何をしてよいか）の置き場所を間違えると穴が空きます。

### よくある誤り：`proxy.ts` だけで守る

```ts
// proxy.ts — ⚠️ これ「だけ」では不十分
export function proxy(request: NextRequest) {
  const session = request.cookies.get('session')
  if (!session) return NextResponse.redirect(new URL('/login', request.url))
}
```

これは**UX改善（未ログインならログイン画面へ誘導）としては正しい**のですが、防御としては不十分です。

- Server Actions は経路が異なるため、意図通りに通らない場合がある
- マッチャーの書き漏れで特定のパスが素通りする
- 「ログインしているか」は見ても「**そのデータの持ち主か**」は見ていない

### 正しい多層防御

```
第1層 proxy.ts        → 未ログインをログイン画面へ誘導（UX）
第2層 レイアウト/ページ → 画面の出し分け（UX）
第3層 データアクセス層  → ★ここが本当の防御★
```

**「データを取り出す関数の中で必ず確認する」** のが鉄則です。

```ts
// lib/dal.ts （Data Access Layer）
import 'server-only'      // ← クライアントへの誤importをビルド時に検出
import { cache } from 'react'
import { auth } from '@/auth'

export const requireUser = cache(async () => {
  const session = await auth()
  if (!session?.user) throw new Error('Unauthorized')
  return session.user
})

export async function getMyPost(postId: string) {
  const user = await requireUser()
  // ★ 所有者条件をクエリに含める
  const post = await db.post.findFirst({
    where: { id: postId, authorId: user.id },
  })
  if (!post) throw new Error('Not found')
  return post
}
```

```ts
// ❌ 危険：IDさえ知っていれば他人の投稿が取れる
const post = await db.post.findUnique({ where: { id } })

// ✅ 安全：所有者でなければそもそも取れない
const post = await db.post.findFirst({ where: { id, authorId: user.id } })
```

> 🔑 **`import 'server-only'`** を認証・DB関連のファイルに書いておくと、誤ってClient Componentからimportしたときに**ビルドが失敗**します。秘密情報の漏洩を型システムの外側で防ぐ、安価で効果的な保険です。

### 認可チェックの置き場所チェックリスト

- [ ] Server Action の**冒頭**で認証・認可を確認しているか（→ [⑥](06-server-actions-forms.md#7--セキュリティ--この章で最も重要)）
- [ ] Route Handler（`route.ts`）でも確認しているか（→ [⑨](09-route-handlers-api.md)）
- [ ] DBクエリに**所有者条件**が入っているか
- [ ] 管理者判定を**クライアントから渡された値**で行っていないか
- [ ] `proxy.ts` を「唯一の防御」にしていないか

---

## 4. パスワード認証を自前で扱う場合の最低ライン

外部SaaSを使わず、Auth.jsのCredentialsプロバイダ等でパスワードを扱うなら、最低限これらが必要です。

| 項目 | 実装 |
| --- | --- |
| ハッシュ化 | **bcrypt / argon2**。MD5・SHA-1は論外 |
| Cookie | `httpOnly` `secure` `sameSite: 'lax'` |
| レート制限 | ログイン試行の回数制限（総当たり対策） |
| アカウント列挙対策 | 「メールが存在しない」と「パスワードが違う」を**区別して返さない** |
| リセットトークン | 有効期限つき・使い捨て・十分な長さの乱数 |
| セッション固定化対策 | ログイン成功時にセッションIDを再発行 |

> それでも、**可能ならソーシャルログインやマジックリンクに寄せる**ほうが安全です。パスワードを持たない設計が最も事故が少なくなります。

---

## 5. この章のまとめ

- ORMは **Prisma（学習しやすい）vs Drizzle（軽量・SQL寄り）**。チームが読める方を選ぶ
- **`globalForPrisma` パターンは必須**。入れないと開発中にDB接続が枯渇する
- サーバーレスでは**接続プーラー**を必ず経由する
- 認証は **Auth.js（無料）/ Better Auth（型安全）/ Clerk（最速）** から選ぶ。**自前実装は避ける**
- 🚨 **認可の本体はデータアクセス層に置く。`proxy.ts` はUX改善であって防御ではない**
- DBクエリには**所有者条件**を入れる。`findUnique({ where: { id } })` は危険
- 認証・DBのファイルには **`import 'server-only'`** を付けて誤importを防ぐ

---

次の章 → [⑨ Route HandlersとAPI連携](09-route-handlers-api.md)
