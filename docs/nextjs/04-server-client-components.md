---
title: ④ Server ComponentsとClient Components
---

# ④ Server ComponentsとClient Components — App Router最大の関門

[← 総合インデックスに戻る](README.md) ｜ 前 → [③ ルーティング](03-routing.md) ｜ 次 → [⑤ データ取得とキャッシュ](05-data-fetching-caching.md)

**この章がシリーズで最も重要です。** App Router でつまずく人の8割はここを理解していないことが原因で、逆にここさえ腑に落ちれば残りは応用にすぎません。

---

## 1. たとえ話：厨房とホール

レストランで考えます。

```
🍳 厨房（サーバー）              🍽️ ホール（ブラウザ）
- 冷蔵庫（DB）に手が届く          - お客さんと直接やりとりする
- レシピ（APIキー）は門外不出     - ボタンを押す、入力する
- 料理を作って出すだけ            - 反応を返す
```

**Server Component は厨房のスタッフ、Client Component はホールのスタッフ**です。

- 厨房スタッフは冷蔵庫（DB）を開けられますが、お客さんの「ボタンを押した」に反応できません
- ホールスタッフはお客さんに反応できますが、冷蔵庫の中身を直接は取れません

App Router では **既定で全員が厨房スタッフ**です。ホールに出したいコンポーネントにだけ `'use client'` を付けます。

---

## 2. 既定はサーバー — ここが従来のReactと決定的に違う

```tsx
// app/page.tsx — 何も書かなければ Server Component
import { db } from '@/lib/db'

export default async function Page() {
  // 👇 ブラウザからは絶対に見えない。DBに直接アクセスできる
  const posts = await db.post.findMany()

  return (
    <ul>
      {posts.map((p) => <li key={p.id}>{p.title}</li>)}
    </ul>
  )
}
```

このコンポーネントは**サーバーでのみ実行され、結果のHTMLだけがブラウザに送られます**。つまり：

- ✅ DBの接続情報やAPIキーがブラウザに漏れない
- ✅ このコンポーネントのJavaScriptは**ブラウザに1バイトも送られない**（＝軽い）
- ✅ `async/await` がそのまま書ける（`useEffect` + `useState` の定型文が不要）
- ❌ `useState` / `onClick` / `window` は使えない

### 従来のReactとの比較

```tsx
// ❌ 従来（Client Component）: 3つの状態を自分で管理し、
//    画面が出てからデータを取りに行くので一瞬空になる
'use client'
function Posts() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/posts')
      .then((r) => r.json())
      .then(setPosts)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p>読み込み中...</p>
  if (error) return <p>エラー</p>
  return <ul>{posts.map(...)}</ul>
}

// ✅ Server Component: これだけ。APIも状態管理も不要
async function Posts() {
  const posts = await db.post.findMany()
  return <ul>{posts.map(...)}</ul>
}
```

**APIエンドポイントを作る必要すらない**のがポイントです。画面が必要なデータを、画面自身が直接取りに行きます。

---

## 3. `'use client'` — ホールに出す宣言

ファイルの**先頭**に書きます。

```tsx
'use client'   // ← ファイルの1行目（import より前）

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

### `'use client'` が必要になる条件

次のどれかを使うなら必要です。

| 使いたいもの | 例 |
| --- | --- |
| **状態** | `useState`, `useReducer` |
| **副作用** | `useEffect`, `useLayoutEffect` |
| **イベントハンドラ** | `onClick`, `onChange`, `onSubmit` |
| **ブラウザAPI** | `window`, `document`, `localStorage`, `navigator` |
| **Reactのcontext** | `useContext`, `createContext` |
| **クライアント用ライブラリ** | Framer Motion, Recharts, 多くのUIライブラリ |
| **カスタムフック** | 上記を内部で使っているもの |

> 🔑 **`'use client'` は「ここから先は全部クライアント」の境界宣言です。** そのファイルがimportしているコンポーネントも自動的にClient Componentになります。1ファイルごとに書く必要はありません（書いても害はありません）。

---

## 4. 最重要の設計原則：「Client は葉っぱに置く」

これが**Next.jsのパフォーマンス設計のすべて**と言っても過言ではありません。

### ❌ よくある失敗

```tsx
// app/page.tsx
'use client'   // 😱 ページ全体をクライアントにしてしまった

import { useState } from 'react'

export default function Page() {
  const [open, setOpen] = useState(false)   // 使いたいのはこれだけなのに...
  return (
    <div>
      <Header />
      <HugeArticleList />   {/* 全部クライアントJSとして送られる */}
      <Footer />
      <button onClick={() => setOpen(!open)}>開閉</button>
    </div>
  )
}
```

「ボタン1つのために `useState` が要る」→「じゃあページに `'use client'`」とすると、**配下の全コンポーネントのJSがブラウザに送られ**、DBへの直接アクセスもできなくなります。Next.jsを使う意味がほぼ消えます。

### ✅ 正しい形：インタラクティブな部分だけを切り出す

```tsx
// components/Toggle.tsx  ← 葉っぱだけクライアント
'use client'
import { useState } from 'react'

export function Toggle() {
  const [open, setOpen] = useState(false)
  return <button onClick={() => setOpen(!open)}>開閉</button>
}
```

```tsx
// app/page.tsx  ← ページはサーバーのまま
import { Toggle } from '@/components/Toggle'

export default async function Page() {
  const articles = await db.article.findMany()   // ✅ DB直アクセスできる
  return (
    <div>
      <Header />
      <ArticleList articles={articles} />   {/* JSは送られない */}
      <Footer />
      <Toggle />                            {/* これだけがJSになる */}
    </div>
  )
}
```

```
❌ 悪い構成               ✅ 良い構成
┌───────────────┐        ┌───────────────┐
│ 🔵 Page       │        │ ⚪ Page       │
│ ┌───────────┐ │        │ ┌───────────┐ │
│ │🔵 List    │ │        │ │⚪ List    │ │
│ │🔵 Item    │ │        │ │⚪ Item    │ │
│ │🔵 Button  │ │        │ │🔵 Button  │ │ ← ここだけ青
│ └───────────┘ │        │ └───────────┘ │
└───────────────┘        └───────────────┘
 全部JSで送信              ボタン分のJSだけ

  🔵 = Client Component（JSが送られる）
  ⚪ = Server Component（HTMLだけ）
```

---

## 5. 組み合わせのルール

### ✅ Server → Client（propsを渡す）：OK

```tsx
// Server Component
export default async function Page() {
  const user = await getUser()
  return <Profile name={user.name} />   // Clientコンポーネントに渡せる
}
```

ただし**渡せるのはシリアライズ可能な値だけ**です。

| 渡せる ✅ | 渡せない ❌ |
| --- | --- |
| 文字列・数値・真偽値・null | 関数（Server Actionを除く） |
| 配列・プレーンオブジェクト | クラスのインスタンス |
| Date・Map・Set | Symbol |
| JSX（`children`） | DBのコネクション等 |

### ✅ Client の中に Server を置く：`children` 経由ならOK

Client Component の中で Server Component を **import することはできません**。しかし、**`children` として受け取る**なら可能です。これは覚えておくと非常に役立つパターンです。

```tsx
// ❌ できない
'use client'
import { ServerStuff } from './ServerStuff'   // クライアント化されてしまう
export function Wrapper() {
  return <div><ServerStuff /></div>
}
```

```tsx
// ✅ できる：children として穴を開けておく
'use client'
export function Wrapper({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false)
  return (
    <div>
      <button onClick={() => setOpen(!open)}>開閉</button>
      {open && children}
    </div>
  )
}
```

```tsx
// app/page.tsx（Server Component）
export default function Page() {
  return (
    <Wrapper>
      <ServerStuff />   {/* ✅ サーバーで実行されたまま差し込まれる */}
    </Wrapper>
  )
}
```

**理由**：`children` は呼び出し元（サーバー側）ですでにレンダリング済みの「結果」として渡されるため、Clientコンポーネントは中身を実行しません。Providerでアプリ全体を包むときも、この形なら配下がクライアント化しません。

---

## 6. 判断フロー — どちらにすべきか

```
このコンポーネントは...

useState/useEffect/onClick/window を使う？
  │
  ├─ No  → ⚪ Server Component（何も書かない）✅ 既定
  │
  └─ Yes → その部分だけ切り出せない？
            │
            ├─ 切り出せる → 切り出して 🔵 'use client'
            │              （親はServerのまま）✅ 理想形
            │
            └─ 切り出せない → 🔵 'use client'
                             （なるべく葉に近い位置で）
```

### 実務での目安

| 種類 | どちら |
| --- | --- |
| ページ・レイアウト | ⚪ Server（原則） |
| 記事一覧・カード・テーブル表示 | ⚪ Server |
| ヘッダー・フッター | ⚪ Server（メニュー開閉部分だけ🔵に切り出す） |
| フォーム | 🔵 Client（ただし送信処理はServer Action → [⑥](06-server-actions-forms.md)） |
| モーダル・タブ・アコーディオン | 🔵 Client |
| グラフ・地図 | 🔵 Client（ライブラリがブラウザ前提のため） |
| 検索ボックス | 🔵 Client（入力の状態を持つため） |

---

## 7. よくあるエラーと対処

### `You're importing a component that needs useState...`

Server Component で `useState` を使っています。`'use client'` を付けるか、その部分を切り出してください。

### `Functions cannot be passed directly to Client Components`

Server Component から Client Component に関数を渡しています。

```tsx
// ❌
<Button onClick={() => console.log('hi')} />   // Server Componentから

// ✅ 方法1: Client Component側でハンドラを定義する
// ✅ 方法2: Server Action を渡す（→ ⑥章）
```

### `window is not defined`

サーバーで `window` を触っています。

```tsx
// ✅ 対処1: useEffect の中で使う（useEffectはブラウザでのみ動く）
'use client'
useEffect(() => {
  console.log(window.innerWidth)
}, [])

// ✅ 対処2: SSRを無効にして動的import
const Map = dynamic(() => import('./Map'), { ssr: false })
```

### Hydration failed（サーバーとクライアントで表示が違う）

サーバーで作ったHTMLと、ブラウザで再計算した結果が食い違うと出ます。

```tsx
// ❌ 原因の典型：レンダリングのたびに値が変わるもの
<p>{new Date().toLocaleString()}</p>
<p>{Math.random()}</p>

// ✅ 対処：マウント後に描画する
'use client'
const [mounted, setMounted] = useState(false)
useEffect(() => setMounted(true), [])
if (!mounted) return null
return <p>{new Date().toLocaleString()}</p>
```

他にも、ブラウザ拡張がDOMを書き換える、`<p>` の中に `<div>` を入れているなど不正なHTML構造、なども原因になります。

---

## 8. ⚠️ よくある誤解の整理

| 誤解 | 実際 |
| --- | --- |
| 「Client Componentはサーバーで動かない」 | **動きます**。初回はサーバーでHTML化され（SSR）、ブラウザで再度動く（Hydration）。`'use client'` は「サーバーで動かない」ではなく「**クライアントでも動く**」宣言 |
| 「`'use client'` を付けるとSEOに弱くなる」 | サーバーでHTML化されるのでSEOは基本的に問題なし。問題になるのは**JS量が増えること** |
| 「Server Componentは速い」 | 「JSが減るので初回表示が軽い」が正確。サーバー処理自体は遅いこともある |
| 「全部Serverにすべき」 | UIの反応性が要る部分は当然Client。**適材適所** |

---

## 9. この章のまとめ

- **既定はServer Component。** DBに直接アクセスでき、JSがブラウザに送られない
- `'use client'` は**境界宣言**。そのファイルがimportする先も全部クライアントになる
- **原則「Clientは葉っぱに置く」**。ページ全体に `'use client'` を付けたら設計を疑う
- Client の中に Server を入れたいときは **`children` 経由**
- Server → Client に渡せるのは**シリアライズ可能な値だけ**
- Hydrationエラーは「サーバーとブラウザで結果が変わるもの」を描画したときに出る

---

次の章 → [⑤ データ取得とキャッシュ](05-data-fetching-caching.md)
