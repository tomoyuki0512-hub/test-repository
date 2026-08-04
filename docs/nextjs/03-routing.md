---
title: ③ ルーティング（App Router）
---

# ③ ルーティング（App Router） — ファイル構造がそのままURLになる

[← 総合インデックスに戻る](README.md) ｜ 前 → [② 環境構築とプロジェクト構造](02-setup-and-structure.md) ｜ 次 → [④ Server / Client Components](04-server-client-components.md)

App Router の中心にあるのは **「ディレクトリを掘るとURLになる」** という規約です。この章では基本から、実務で必要になる高度なパターンまでを扱います。

---

## 1. 基本ルール — フォルダがURL、ファイルが役割

**フォルダ名がURLのパス**になり、**その中に置く特別な名前のファイル**が役割を決めます。

```
app/
├── page.tsx                 →  /
├── about/
│   └── page.tsx             →  /about
├── blog/
│   ├── page.tsx             →  /blog
│   └── [slug]/
│       └── page.tsx         →  /blog/hello-world
└── dashboard/
    ├── layout.tsx           →  /dashboard 以下すべてを包む枠
    ├── page.tsx             →  /dashboard
    └── settings/
        └── page.tsx         →  /dashboard/settings
```

> 🔑 **重要**：フォルダを作っただけではURLになりません。**`page.tsx` を置いて初めてアクセス可能**になります。`app/lib/utils.ts` のようにフォルダを作っても、`page.tsx` がなければ `/lib` は404です（＝ロジックを `app/` 配下に同居させても安全）。

---

## 2. 特別な意味を持つファイル

| ファイル名 | 役割 | いつ表示されるか |
| --- | --- | --- |
| `page.tsx` | ページの中身 | そのURLにアクセスしたとき |
| `layout.tsx` | 共通の外枠 | 配下すべて。**ページ移動しても再描画されない** |
| `loading.tsx` | ローディング表示 | データ取得の待ち時間中（自動でSuspense化） |
| `error.tsx` | エラー画面 | 配下でエラーが起きたとき（Client Component必須） |
| `not-found.tsx` | 404画面 | `notFound()` 呼び出し時・該当ページなし |
| `route.ts` | APIエンドポイント | `page.tsx` の代わりに置く（→ [⑨](09-route-handlers-api.md)） |
| `template.tsx` | layoutに似た枠 | layoutと違い**毎回再生成**される（アニメーション用途） |
| `default.tsx` | 並列ルートの既定表示 | Parallel Routesで未一致のとき |

### 入れ子の様子

```
app/layout.tsx           ← いちばん外（<html><body>）
 └ app/dashboard/layout.tsx   ← サイドバーなど
    └ app/dashboard/settings/page.tsx  ← 実際の中身
```

実際のDOMではこう包まれます。

```tsx
<RootLayout>
  <DashboardLayout>
    <SettingsPage />
  </DashboardLayout>
</RootLayout>
```

### `loading.tsx` の効果

`loading.tsx` を置くだけで、そのセグメントが自動的に Suspense で包まれ、**データ待ちの間ローディングを出しつつ、他の部分を先に表示**できます。

```tsx
// app/blog/loading.tsx
export default function Loading() {
  return <div className="animate-pulse">記事を読み込み中...</div>
}
```

### `error.tsx` の書き方

エラー境界はブラウザ側の機能なので、**必ず `'use client'` が必要**です。

```tsx
// app/blog/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>問題が発生しました</h2>
      {/* 本番では error.message を出さない。digest でログと突合する */}
      <button onClick={() => reset()}>再試行</button>
    </div>
  )
}
```

> ⚠️ `error.tsx` は**同階層の `layout.tsx` のエラーは捕捉できません**（layoutの方が外側にあるため）。ルートレイアウトのエラーを捕まえたい場合は `app/global-error.tsx` を使います。

---

## 3. 動的ルート（URLの一部を変数にする）

### 単一パラメータ `[id]`

```
app/posts/[id]/page.tsx   →  /posts/1  /posts/2  /posts/abc
```

```tsx
// app/posts/[id]/page.tsx
export default async function PostPage({
  params,
}: {
  params: Promise<{ id: string }>   // ⚠️ Promise であることに注意
}) {
  const { id } = await params
  return <h1>記事ID: {id}</h1>
}
```

> ⚠️ **Next.js 15 以降、`params` と `searchParams` は Promise です。** 必ず `await` してください。15より前の記事では `params.id` と直接書かれているので、そのままコピーすると動きません。

### 複数階層をまとめて受ける

| 書き方 | マッチするURL | 受け取る値 |
| --- | --- | --- |
| `[id]` | `/posts/1` | `{ id: '1' }` |
| `[...slug]` | `/docs/a/b/c` | `{ slug: ['a','b','c'] }` |
| `[[...slug]]` | `/docs` **も** `/docs/a/b` | `{ slug: undefined }` or `['a','b']` |

`[...slug]`（Catch-all）は `/docs` 自体にはマッチせず、`[[...slug]]`（Optional Catch-all）はマッチする、が違いです。ドキュメントサイトやCMS連携で多用します。

### クエリパラメータ（`?page=2`）

```tsx
export default async function ListPage({
  searchParams,
}: {
  searchParams: Promise<{ page?: string; q?: string }>
}) {
  const { page = '1', q } = await searchParams
  return <p>{q} の検索結果 {page}ページ目</p>
}
```

### ビルド時に静的生成したいとき

```tsx
// app/posts/[id]/page.tsx
export async function generateStaticParams() {
  const posts = await getPosts()
  // 返した分だけビルド時にHTMLが作られる
  return posts.map((post) => ({ id: String(post.id) }))
}
```

`getStaticPaths`（Pages Router）の後継です。

---

## 4. ルートグループ `(name)` — URLに出ないフォルダ

**丸括弧で囲んだフォルダはURLに含まれません。** レイアウトを分けたり、コードを整理するために使います。

```
app/
├── (marketing)/            ← URLに出ない
│   ├── layout.tsx          ← マーケ用の共通ヘッダー
│   ├── page.tsx            →  /
│   └── pricing/page.tsx    →  /pricing
└── (app)/                  ← URLに出ない
    ├── layout.tsx          ← ログイン後用のサイドバー
    └── dashboard/page.tsx  →  /dashboard
```

「トップページと管理画面でヘッダーを完全に変えたい」というよくある要件が、これだけで実現できます。

---

## 5. プライベートフォルダ `_name`

**アンダースコア始まりのフォルダはルーティングから除外**されます。ページに密接なコンポーネントを近くに置きたいときに使います。

```
app/dashboard/
├── _components/        ← URLにならない。dashboard専用の部品置き場
│   └── Chart.tsx
└── page.tsx
```

---

## 6. リンクと画面遷移

### `<Link>` を使う（基本）

```tsx
import Link from 'next/link'

<Link href="/about">会社概要</Link>
<Link href={`/posts/${id}`}>記事を読む</Link>
```

> 💡 **`<a>` タグを使ってはいけない理由**：`<a>` はページ全体を再読み込みします。`<Link>` は必要な部分だけを差し替え、さらに**画面内に入った時点で遷移先を先読み（プリフェッチ）**するため体感速度がまったく違います。外部サイトへのリンクだけ `<a>` を使います。

### コード内から遷移する

```tsx
'use client'
import { useRouter } from 'next/navigation'   // ⚠️ 'next/router' ではない

export function SaveButton() {
  const router = useRouter()
  return (
    <button onClick={async () => {
      await save()
      router.push('/dashboard')   // 遷移
      router.refresh()            // サーバーデータを再取得
    }}>
      保存
    </button>
  )
}
```

### サーバー側で遷移・404にする

```tsx
import { redirect, notFound } from 'next/navigation'

export default async function Page({ params }) {
  const { id } = await params
  const post = await getPost(id)

  if (!post) notFound()              // not-found.tsx を表示
  if (!post.published) redirect('/') // 別URLへ飛ばす
  return <article>{post.title}</article>
}
```

### 現在のURLを知る（Client Component）

```tsx
'use client'
import { usePathname, useSearchParams, useParams } from 'next/navigation'

const pathname = usePathname()        // "/posts/1"
const searchParams = useSearchParams() // ?q=abc を読む
const params = useParams()             // { id: "1" }
```

---

## 7. 応用：並列ルート（Parallel Routes）

**1つのURLで複数の領域を同時に描画**する仕組みです。`@name` フォルダで定義し、レイアウトがpropsとして受け取ります。

```
app/dashboard/
├── layout.tsx
├── page.tsx
├── @analytics/page.tsx     ← 同時に表示される領域その1
└── @team/page.tsx          ← 同時に表示される領域その2
```

```tsx
// app/dashboard/layout.tsx
export default function Layout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="col-span-2">{children}</div>
      {analytics}
      {team}
    </div>
  )
}
```

**利点**：それぞれ独立に `loading.tsx` / `error.tsx` を持てるため、**片方の読み込みが遅くても、もう片方は先に表示**できます。ダッシュボードのようにパネルが並ぶ画面で威力を発揮します。

---

## 8. 応用：インターセプトルート（Intercepting Routes）

**「一覧から画像をクリックするとモーダルで開く。でもURLを直接叩くと通常ページで開く」** という、InstagramやX（Twitter）のような挙動を実現します。

```
app/
├── feed/page.tsx
├── photo/[id]/page.tsx           ← 直接アクセス時：通常ページ
└── feed/
    └── (..)photo/[id]/page.tsx   ← feedから遷移時：モーダル
```

| 記法 | 意味 |
| --- | --- |
| `(.)` | 同じ階層 |
| `(..)` | 1つ上の階層 |
| `(..)(..)` | 2つ上の階層 |
| `(...)` | app直下から |

並列ルートと組み合わせて使うのが定番です。**URLが共有可能なまま、UXはモーダル**という両立ができます。

---

## 9. よくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| 404になる | `page.tsx` がない | フォルダだけではURLにならない |
| `params.id` が `undefined` | 15以降は Promise | `const { id } = await params` |
| `useRouter is not defined` | `next/router` を import している | `next/navigation` から import |
| `useState` でエラー | Server Componentで使っている | `'use client'` を付ける（→ [④](04-server-client-components.md)） |
| ページ移動でレイアウトが再描画される | `template.tsx` を使っている | `layout.tsx` に変える |
| データが更新されない | キャッシュ | `router.refresh()` / `revalidateTag`（→ [⑤](05-data-fetching-caching.md)） |

---

## 10. この章のまとめ

- **フォルダ = URL、`page.tsx` = 中身**。`page.tsx` がなければURLにならない
- `layout` は額縁で**再描画されない**、`loading` / `error` / `not-found` を置くだけで境界が作られる
- **`params` / `searchParams` は Promise。`await` が必須**（15以降）
- `(group)` はURLに出ない整理用、`_folder` はルーティング対象外
- 内部リンクは必ず `<Link>`（プリフェッチが効く）、`useRouter` は **`next/navigation`** から
- 並列ルート・インターセプトルートで「複数パネル」「モーダル遷移」が宣言的に書ける

---

次の章 → [④ Server ComponentsとClient Components](04-server-client-components.md)
