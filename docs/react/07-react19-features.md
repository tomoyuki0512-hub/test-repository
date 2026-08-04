---
title: ⑦ React 19の新機能
---

# ⑦ React 19の新機能 — Server Components・Actions・その先

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑥ 状態設計と状態管理](06-state-design.md) ｜ 次 → [⑧ 実践パターンとアンチパターン](08-practice-patterns.md)

React 19 は **フック導入（2019）以来の大きな転換点**です。この章では何が変わったか、なぜ変わったかを扱います。**Next.jsを使う人には特に重要**な内容です。

---

## 1. React 19 の全体像

| 機能 | 何が変わったか | 影響度 |
| --- | --- | --- |
| **Server Components** | Reactがサーバーでも動くようになった | ★★★ 最大の変化 |
| **Actions** | 非同期処理＋状態管理の定型文が不要に | ★★★ |
| **`use()`** | Promise・Contextを条件付きで読める | ★★☆ |
| **ref as prop** | `forwardRef` が不要に | ★★☆ |
| **Document Metadata** | `<title>` 等をどこでも書ける | ★☆☆ |
| **`<Context>`** | `.Provider` を省略できる | ★☆☆ |
| **`<Activity>`**（19.2） | UIを「隠す/一時停止」できる | ★☆☆ |
| **`useEffectEvent`**（19.2） | Effect内で最新値を安全に使う | ★☆☆ |

---

## 2. Server Components（RSC）— 最大の変化

### 何が変わったのか

**Reactコンポーネントがサーバーで実行できるようになりました。**

```tsx
// Server Component（サーバーでのみ実行される）
async function PostList() {
  const posts = await db.post.findMany()    // ★DBに直接アクセスできる

  return (
    <ul>
      {posts.map((p) => <li key={p.id}>{p.title}</li>)}
    </ul>
  )
}
```

従来との比較：

```tsx
// ❌ 従来（Client Component）
function PostList() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/posts').then(r => r.json()).then(setPosts).finally(() => setLoading(false))
  }, [])

  if (loading) return <Spinner />
  return <ul>{posts.map(...)}</ul>
}
```

**APIエンドポイントも状態管理もローディング管理も不要**になりました。

### 得られるもの

| 利点 | 内容 |
| --- | --- |
| **JSが減る** | Server Componentのコードはブラウザに送られない |
| **秘密を守れる** | APIキー・DB接続情報がブラウザに露出しない |
| **ウォーターフォールが減る** | 「HTML取得→JS実行→API呼び出し」の連鎖が消える |
| **コードがシンプル** | `async/await` をそのまま書ける |

### 制約

```tsx
// ❌ Server Componentでは使えない
useState / useEffect / onClick / window / localStorage
```

インタラクティブな部分は `'use client'` を付けてClient Componentにします。

```tsx
'use client'
import { useState } from 'react'

export function LikeButton() {
  const [liked, setLiked] = useState(false)
  return <button onClick={() => setLiked(!liked)}>{liked ? '❤️' : '🤍'}</button>
}
```

> 🔑 **設計の鉄則：Client Componentは葉っぱ（末端）に置く。** ページ全体を `'use client'` にすると利点が全部消えます。詳細は [Next.js④](../nextjs/04-server-client-components.md) で図解しています。

### ⚠️ 使うにはフレームワークが必要

**React単体（Viteなど）ではRSCを使えません。** サーバー側でのレンダリング基盤とビルド設定が必要なため、[Next.js](../nextjs/README.md) のようなフレームワークが前提になります。

---

## 3. Actions — 非同期処理の定型文をなくす

### 従来の悩み

フォーム送信のたびに、同じコードを書いていました。

```tsx
// ❌ 毎回この定型文
const [isPending, setIsPending] = useState(false)
const [error, setError] = useState(null)

async function handleSubmit(e) {
  e.preventDefault()
  setIsPending(true)
  setError(null)
  try {
    await updateName(name)
  } catch (err) {
    setError(err.message)
  } finally {
    setIsPending(false)
  }
}
```

### `useActionState`

```tsx
import { useActionState } from 'react'

function NameForm() {
  const [state, formAction, isPending] = useActionState(
    async (prevState, formData: FormData) => {
      try {
        await updateName(formData.get('name') as string)
        return { message: '更新しました' }
      } catch (e) {
        return { error: (e as Error).message }
      }
    },
    { message: '' },
  )

  return (
    <form action={formAction}>
      <input name="name" />
      <button disabled={isPending}>{isPending ? '送信中...' : '更新'}</button>
      {state.error && <p className="error">{state.error}</p>}
      {state.message && <p>{state.message}</p>}
    </form>
  )
}
```

**ローディング状態・エラー状態が自動管理**されます。

### `useFormStatus`

フォームの送信状態を、**子コンポーネントから**取得できます。

```tsx
import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? '送信中' : '送信'}</button>
}
```

> ⚠️ **`useFormStatus` は `<form>` の子孫でのみ動きます。** 同じコンポーネント内で呼んでも `pending` は常に `false` です。**送信ボタンを別コンポーネントに切り出す必要があります**——これは非常によくあるハマりどころです。

### `useOptimistic` — 楽観的更新

サーバーの応答を待たず、先に画面を更新します。

```tsx
function LikeButton({ postId, likes }: { postId: string; likes: number }) {
  const [optimisticLikes, addOptimistic] = useOptimistic(
    likes,
    (current: number, delta: number) => current + delta,
  )

  return (
    <form action={async () => {
      addOptimistic(1)          // 即座に画面へ反映
      await toggleLike(postId)  // 裏で通信
    }}>
      <button>❤️ {optimisticLikes}</button>
    </form>
  )
}
```

**失敗したらReactが自動的に元の値へ戻します。** 「いいね」「フォロー」など、成功が前提の操作で体感速度が大きく改善します。

---

## 4. `use()` — 新しい読み取りAPI

**フックではなく「API」**なので、**条件分岐やループの中でも呼べます**（フックのルールが適用されません）。

### Promiseを読む

```tsx
import { use, Suspense } from 'react'

function Comments({ commentsPromise }: { commentsPromise: Promise<Comment[]> }) {
  const comments = use(commentsPromise)   // 解決するまでSuspenseに委ねる
  return <ul>{comments.map((c) => <li key={c.id}>{c.text}</li>)}</ul>
}

function Page() {
  const commentsPromise = fetchComments()   // awaitしないで渡す
  return (
    <Suspense fallback={<Spinner />}>
      <Comments commentsPromise={commentsPromise} />
    </Suspense>
  )
}
```

### Contextを条件付きで読む

```tsx
function Panel({ show }: { show: boolean }) {
  if (!show) return null
  const theme = use(ThemeContext)   // ✅ if の後でも呼べる（useContextでは不可）
  return <div className={theme}>...</div>
}
```

> ⚠️ **注意**：Client Componentでレンダリング中に `fetch()` してそのPromiseを `use()` に渡すと、**再レンダリングのたびに新しいリクエストが飛びます**。Promiseはサーバー側で作るか、キャッシュされたものを渡してください。

---

## 5. 細かいが嬉しい改善

### ref を普通のpropsとして渡せる

```tsx
// ❌ React 18まで：forwardRefが必要
const Input = forwardRef<HTMLInputElement, Props>((props, ref) => (
  <input ref={ref} {...props} />
))

// ✅ React 19：普通のpropsでOK
function Input({ ref, ...props }: Props & { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />
}
```

`forwardRef` の煩雑さが消えました。**既存コードもそのまま動きます**（`forwardRef` は非推奨化の方向）。

### メタデータをどこでも書ける

```tsx
function ProductPage({ product }) {
  return (
    <article>
      <title>{product.name} | ショップ</title>          {/* 自動で<head>へ */}
      <meta name="description" content={product.summary} />
      <link rel="canonical" href={`/products/${product.id}`} />
      <h1>{product.name}</h1>
    </article>
  )
}
```

`react-helmet` のようなライブラリが不要になりました。

> 💡 ただし **Next.jsを使う場合は `metadata` API のほうが機能が豊富**です（OG画像・テンプレート等）。→ [Next.js⑩](../nextjs/10-performance-seo.md)

### Context の `.Provider` が不要

```tsx
// React 18
<ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>

// React 19
<ThemeContext value={theme}>{children}</ThemeContext>
```

### エラーハンドリングの改善

`createRoot` にエラーハンドラを渡せるようになり、Hydrationエラーの表示も分かりやすくなりました。

```tsx
createRoot(container, {
  onUncaughtError: (error, errorInfo) => reportToSentry(error, errorInfo),
  onCaughtError: (error, errorInfo) => { /* Error Boundaryで捕捉されたもの */ },
})
```

---

## 6. React 19.2 の追加機能

### `<Activity>` — UIを隠す・一時停止する

```tsx
<Activity mode={isVisible ? 'visible' : 'hidden'}>
  <ExpensiveTab />
</Activity>
```

`display: none` と違い、**Reactが「一時停止」として扱います**。

| 従来 | `<Activity>` |
| --- | --- |
| アンマウント → 状態が消える・再取得が必要 | **状態を保持したまま非表示** |
| `display:none` → Effectは動き続ける | Effectも停止される |

タブ切り替えで「戻ったときにスクロール位置や入力が残っている」といった体験が簡単に作れます。

### `useEffectEvent` — Effect内で最新値を使う

```tsx
// ❌ 問題：theme が変わるたびに再接続してしまう
useEffect(() => {
  const conn = connect(roomId)
  conn.on('connected', () => showToast('接続しました', theme))
  return () => conn.disconnect()
}, [roomId, theme])   // themeも依存に入れざるを得ない

// ✅ useEffectEvent で切り離す
const onConnected = useEffectEvent(() => {
  showToast('接続しました', theme)    // 常に最新のthemeを見る
})

useEffect(() => {
  const conn = connect(roomId)
  conn.on('connected', onConnected)
  return () => conn.disconnect()
}, [roomId])          // themeは依存に不要
```

「**Effectは再実行したくないが、中では最新の値を使いたい**」という長年の悩みへの解答です。

### Performance Tracks

Chrome DevToolsのPerformanceタブに、React専用の情報が表示されるようになりました。

- **Scheduler track**：どの更新が高優先度/低優先度で処理されたか
- **Components track**：各コンポーネントのレンダリング時間とEffectの実行タイミング

「なぜこのレンダリングが遅いのか」を可視化できます（→ [⑤](05-rendering-mechanism.md#計測ツール)）。

---

## 7. React 18 からの移行

### 主な破壊的変更

| 変更 | 対処 |
| --- | --- |
| `propTypes` / `defaultProps`（関数コンポーネント）削除 | TypeScriptの型とデフォルト引数へ |
| 文字列 ref (`ref="input"`) 削除 | `useRef` へ |
| `ReactDOM.render` 削除 | `createRoot` へ |
| `react-test-renderer` 非推奨 | Testing Library へ |
| Legacy Context 削除 | `createContext` へ |

### 移行手順

```bash
# 1. まず18の最新版で警告を潰す
npm install react@18 react-dom@18

# 2. コードモッドで自動変換
npx codemod@latest react/19/migration-recipe

# 3. アップグレード
npm install react@19 react-dom@19 @types/react@19 @types/react-dom@19
```

> 💡 **多くのアプリは大きな書き換えなしに移行できます。** ただし古いサードパーティライブラリがReact 19に未対応な場合があるため、**依存ライブラリの対応状況を先に確認**してください。

---

## 8. どこから使い始めるか

```
Viteなどの SPA を使っている
    → Actions（useActionState / useOptimistic）から。すぐ効果が出る
    → Server Componentsは使えない（フレームワークが必要）

Next.js を使っている
    → Server Components が既定。まず ④章の境界設計を理解する
    → Server Actions（→ Next.js⑥章）で更新処理を書く

これから新規開発
    → Next.js + React 19 で、最初からRSC前提の設計にする
```

---

## 9. この章のまとめ

- **Server Components が最大の変化**。Reactがサーバーでも動き、DB直アクセス・JS削減が可能に
- ただし **RSCの利用にはNext.js等のフレームワークが必要**（React単体では使えない）
- **Actions（`useActionState` / `useFormStatus` / `useOptimistic`）** で非同期処理の定型文が消えた
- **`useFormStatus` は `<form>` の子孫で呼ぶ**（同じコンポーネント内では動かない）
- **`use()`** はフックではないため、条件分岐の中でも呼べる
- `forwardRef` 不要、`<title>` をどこでも書ける、`.Provider` 省略可
- 19.2の **`<Activity>`**（状態を保ったまま非表示）と **`useEffectEvent`**（Effect内で最新値）
- 移行はコードモッドで大部分が自動化される。**依存ライブラリの対応確認を先に**

---

次の章 → [⑧ 実践パターンとアンチパターン](08-practice-patterns.md)
