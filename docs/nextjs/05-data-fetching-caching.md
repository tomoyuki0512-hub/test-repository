---
title: ⑤ データ取得とキャッシュ
---

# ⑤ データ取得とキャッシュ — Cache Componentsと`use cache`

[← 総合インデックスに戻る](README.md) ｜ 前 → [④ Server / Client Components](04-server-client-components.md) ｜ 次 → [⑥ Server Actionsとフォーム](06-server-actions-forms.md)

Next.js で最も評判が悪かったのが「**キャッシュがわかりにくい**」ことでした。Next.js 16 の **Cache Components** はその答えです。この章では新しい仕組みを中心に、実務で必要な取得パターンまでを扱います。

---

## 1. データ取得の基本 — `await` するだけ

Server Component は `async` にできるので、データ取得は素直に書けます。

```tsx
// app/posts/page.tsx
export default async function PostsPage() {
  const posts = await db.post.findMany()      // DB直アクセス
  const rates = await fetch('https://api.example.com/rates').then(r => r.json())

  return <PostList posts={posts} />
}
```

APIエンドポイントも `useEffect` も状態管理ライブラリも要りません。

### 並列で取得する（重要）

**逐次に `await` すると待ち時間が足し算になります。** 依存関係がないなら必ず並列化してください。

```tsx
// ❌ 直列：合計 300ms + 400ms = 700ms
const user = await getUser()      // 300ms
const posts = await getPosts()    // 400ms

// ✅ 並列：合計 400ms（遅い方に律速）
const [user, posts] = await Promise.all([
  getUser(),
  getPosts(),
])
```

> 💡 これは Next.js 固有の話ではなく普通のJSの話ですが、**Server Componentで最も効くパフォーマンス改善**です。

---

## 2. Next.js 16 のキャッシュモデル

### 何が変わったのか

| | Next.js 15以前 | **Next.js 16（Cache Components）** |
| --- | --- | --- |
| 既定の動作 | `fetch` が暗黙にキャッシュされることがある | **キャッシュしない。毎リクエスト実行** |
| 有効化 | 自動 | **`'use cache'` と書いたところだけ** |
| ハマりどころ | 「なぜか古いデータが出る」 | 明示しない限り古くならない |

**Next.js 16 の考え方はシンプルです。**

```
何も書かない            → 毎回サーバーで実行される（＝常に最新）
'use cache' と書く      → その部分だけキャッシュされる
```

「意図せずキャッシュされて事故る」のではなく、「**速くしたい場所を自分で選ぶ**」モデルになりました。

### 有効化する

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

---

## 3. `use cache` の使い方

`'use cache'` は**3つのスコープ**で書けます。

### ① 関数単位（最もよく使う）

```ts
// lib/posts.ts
export async function getPosts() {
  'use cache'
  const res = await fetch('https://api.example.com/posts')
  return res.json()
}
```

### ② コンポーネント単位

```tsx
async function PopularPosts() {
  'use cache'
  const posts = await db.post.findMany({ orderBy: { views: 'desc' } })
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

### ③ ファイル単位（ファイル先頭に書くと全exportが対象）

```tsx
// app/blog/page.tsx
'use cache'

export default async function BlogPage() {
  const posts = await getPosts()
  return <PostList posts={posts} />
}
```

> 🔑 **キャッシュキーは自動生成されます。** 引数・呼び出し位置からNext.jsのコンパイラがキーを作るので、`getPost(1)` と `getPost(2)` は別々にキャッシュされます。自分でキーを組み立てる必要はありません。

---

## 4. キャッシュの寿命を決める：`cacheLife`

```ts
import { unstable_cacheLife as cacheLife } from 'next/cache'

export async function getNews() {
  'use cache'
  cacheLife('hours')      // プロファイル名で指定
  return fetch('...').then(r => r.json())
}
```

### 組み込みプロファイル

| プロファイル | 目安 | 用途 |
| --- | --- | --- |
| `seconds` | 数秒 | リアルタイム性が高いもの |
| `minutes` | 数分 | ニュース・ランキング |
| `hours` | 数時間 | 記事一覧・商品一覧 |
| `days` | 数日 | カテゴリ・タグ一覧 |
| `weeks` / `max` | 長期 | 利用規約・マスタデータ |

カスタム指定もできます。

```ts
cacheLife({
  stale: 60,        // クライアントが古い値を使ってよい秒数
  revalidate: 300,  // サーバーが再検証を始めるまでの秒数
  expire: 3600,     // これを過ぎたら必ず作り直す秒数
})
```

**`stale` / `revalidate` / `expire` の関係**：

```
0秒 ─────── 60秒 ─────────── 300秒 ──────────── 3600秒 ────→
   即座に返す   キャッシュを返しつつ    再検証する      期限切れ
              裏で更新（stale-while-revalidate）  （待たせて取得）
```

「多少古くても速く出す」を選べるのがポイントです。

---

## 5. 更新時に消す：`cacheTag` と `revalidateTag` / `updateTag`

時間切れを待たず、**データを更新したタイミングでキャッシュを捨てたい**場面が実務では大半です。

### タグを付ける

```ts
import { unstable_cacheTag as cacheTag } from 'next/cache'

export async function getPost(id: string) {
  'use cache'
  cacheTag(`post-${id}`, 'posts')   // 複数付けられる
  return db.post.findUnique({ where: { id } })
}
```

### 更新時に捨てる

```ts
'use server'
import { revalidateTag, updateTag } from 'next/cache'

export async function updatePost(id: string, data: FormData) {
  await db.post.update({ where: { id }, data: { /* ... */ } })

  updateTag(`post-${id}`)   // 自分の更新を即座に見せたいとき
  revalidateTag('posts')    // 一覧は次のアクセスで作り直せばよいとき
}
```

### `revalidateTag` と `updateTag` の使い分け

| | `revalidateTag` | `updateTag` |
| --- | --- | --- |
| 挙動 | 期限切れ扱いにする。**古い値が一度返ることがある** | **即座に無効化**し、次のリクエストは新しい値を待つ |
| 使う場面 | 他人の更新・一覧の再生成 | **自分の編集結果をすぐ見せる**（read-your-own-writes） |

> 💡 **実務の定石**：「投稿を編集したのに一覧が古いまま」というクレームの典型的な原因は、`revalidateTag` で済ませていることです。**編集した本人に見せる画面は `updateTag`** を使ってください。

### パス単位で捨てる

```ts
import { revalidatePath } from 'next/cache'
revalidatePath('/posts')
revalidatePath('/posts/[id]', 'page')
```

タグの方が精密なので、**まずタグ、どうしても難しいときにパス**という優先順位が推奨されます。

---

## 6. PPRとストリーミング — ページを部分ごとに出す

Cache Components を有効にすると、**Partial Prerendering（PPR）が既定の挙動**になります。`Suspense` が「静的な部分」と「動的な部分」の境界になります。

```tsx
import { Suspense } from 'react'

export default function ProductPage() {
  return (
    <div>
      {/* 静的：即座に配信される */}
      <ProductInfo />

      {/* 動的：準備できたら後から流れてくる */}
      <Suspense fallback={<StockSkeleton />}>
        <StockStatus />     {/* 在庫はリアルタイムで取りたい */}
      </Suspense>

      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews />         {/* 重いので後回しでよい */}
      </Suspense>
    </div>
  )
}
```

```
時間 →
0ms   ┌──────────────────────┐
      │ 商品情報（静的）      │  ← すぐ表示
      │ [ローディング...]     │
      │ [ローディング...]     │
      └──────────────────────┘
200ms ┌──────────────────────┐
      │ 商品情報              │
      │ 在庫: 残り3点         │  ← 届いた順に埋まる
      │ [ローディング...]     │
      └──────────────────────┘
```

> 🔑 **設計のコツ**：「このページ全体をSSRにするかSSGにするか」で悩む必要はもうありません。**遅いもの・毎回変わるものを `Suspense` で囲む**、それだけです。囲まなければページ全体がその処理を待ちます。

### 動的APIを使うと自動的に動的になる

次のものを使ったコンポーネントは、リクエスト時に実行されます。

```tsx
import { cookies, headers } from 'next/headers'

async function UserGreeting() {
  const cookieStore = await cookies()     // ⚠️ 15以降は await が必要
  const session = cookieStore.get('session')
  return <p>ようこそ</p>
}
```

`cookies()` / `headers()` / `searchParams` / `connection()` が該当します。これらを使う部分は必ず `Suspense` で囲むと、ページ全体が動的化するのを防げます。

---

## 7. Client Component でのデータ取得

サーバーで取れるならサーバーで取るのが原則ですが、**ブラウザ側で取る必要がある場面**もあります。

| 場面 | 手段 |
| --- | --- |
| 検索のインクリメンタル表示 | TanStack Query / SWR |
| 無限スクロール | TanStack Query の `useInfiniteQuery` |
| ポーリング（定期更新） | TanStack Query の `refetchInterval` |
| フォーム送信後の更新 | **Server Action ＋ `revalidateTag`**（→ [⑥](06-server-actions-forms.md)） |

```tsx
'use client'
import { useQuery } from '@tanstack/react-query'

export function SearchResults({ q }: { q: string }) {
  const { data, isLoading } = useQuery({
    queryKey: ['search', q],
    queryFn: () => fetch(`/api/search?q=${q}`).then(r => r.json()),
    enabled: q.length > 1,
  })
  if (isLoading) return <Spinner />
  return <ul>{data.map(...)}</ul>
}
```

> ⚠️ **App Routerでは「とりあえずTanStack Query」は不要になりました。** 初期表示のデータはServer Componentで取り、TanStack Query は**上記のような本当にクライアント主導が要る箇所だけ**に使うのが現在の定石です。

---

## 8. パフォーマンスの落とし穴

### N+1問題

```tsx
// ❌ 記事100件 → クエリ101回
const posts = await db.post.findMany()
return posts.map(async (post) => {
  const author = await db.user.findUnique({ where: { id: post.authorId } })
  ...
})

// ✅ JOINで1回に
const posts = await db.post.findMany({ include: { author: true } })
```

### 同じデータを複数箇所で使う

React の `cache()` を使うと、**同一リクエスト内での重複呼び出しが1回にまとまります**（メモ化）。

```ts
import { cache } from 'react'

export const getUser = cache(async (id: string) => {
  return db.user.findUnique({ where: { id } })
})
```

`layout.tsx` と `page.tsx` の両方でログインユーザーを取りたい、といったときに有効です。`'use cache'`（リクエストをまたぐ永続キャッシュ）とは別物なので混同しないでください。

| | `cache()` (React) | `'use cache'` (Next.js) |
| --- | --- | --- |
| 範囲 | **同一リクエスト内**のみ | リクエストをまたぐ |
| 用途 | 重複呼び出しの排除 | 表示の高速化 |

---

## 9. ⚠️ バージョン差分

| 項目 | 15以前 | 16 |
| --- | --- | --- |
| `fetch` のキャッシュ | 既定でキャッシュされることがあった | されない。`'use cache'` で明示 |
| `export const revalidate = 60` | セグメント設定で指定 | `cacheLife()` に置き換え |
| `export const dynamic = 'force-dynamic'` | よく使われた | 既定が動的なので基本不要 |
| `unstable_cache()` | これを使っていた | `'use cache'` に置き換え |
| `experimental.ppr` | 実験的フラグ | 削除。Cache Componentsに統合 |
| `cookies()` / `headers()` | 同期（15で非同期化） | **`await` 必須** |

> 移行の詳細は公式のガイド（`nextjs.org/docs/app/guides/migrating-to-cache-components`）と `npx @next/codemod@canary upgrade latest` を参照してください。

---

## 10. この章のまとめ

- Server Component では **`await` するだけ**。依存がなければ `Promise.all` で並列化
- **Next.js 16 は「既定でキャッシュしない」**。速くしたい場所に `'use cache'` を書く
- 寿命は `cacheLife`、破棄は `cacheTag` ＋ `revalidateTag` / `updateTag`
- **自分の更新をすぐ見せたいなら `updateTag`**、一覧の作り直しは `revalidateTag`
- **遅い部分を `Suspense` で囲む**だけでPPR（部分配信）になる
- クライアント取得は「本当に必要な箇所だけ」。初期表示はサーバーで取る

---

次の章 → [⑥ Server Actionsとフォーム](06-server-actions-forms.md)
