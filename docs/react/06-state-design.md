---
title: ⑥ 状態設計と状態管理
---

# ⑥ 状態設計と状態管理

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑤ レンダリングの仕組み](05-rendering-mechanism.md) ｜ 次 → [⑦ React 19の新機能](07-react19-features.md)

Reactアプリの保守性は **「状態をどこに、どんな形で置くか」** でほぼ決まります。この章では設計の指針と、状態管理ライブラリの選び方を扱います。

---

## 1. まず状態を分類する

「状態管理ライブラリを何にするか」の前に、**その状態がどの種類か**を見極めます。混同するとどんなライブラリを使っても破綻します。

| 種類 | 例 | 置き場所 |
| --- | --- | --- |
| **サーバー状態** | DBから取得した記事一覧・ユーザー情報 | サーバー（RSC）or TanStack Query |
| **URL状態** | 検索キーワード・ページ番号・タブ・フィルタ | **URL（クエリパラメータ）** |
| **フォーム状態** | 入力中の値 | `useState` / React Hook Form |
| **UI状態（ローカル）** | モーダルの開閉・アコーディオン | `useState` |
| **UI状態（グローバル）** | テーマ・サイドバー開閉・カート | Context / Zustand / Jotai |

> 🚨 **最も多い設計ミスは「サーバー状態をグローバル状態として持つ」こと**です。「APIから取ったデータをReduxに入れる」という設計は、キャッシュ・再取得・整合性を全部自前で管理することになり、必ず破綻します。**サーバー状態はサーバー状態として扱ってください。**

### 判断フロー

```
その状態は...

DBやAPIから来る？
  ├─ Next.js       → Server Componentで取得（→ Next.js⑤章）
  └─ SPA           → TanStack Query / SWR

他の人に見せたい・リロードで残したい？（検索条件・ページ番号）
  → URL（searchParams）

1つのコンポーネント内だけ？
  → useState

親子で共有？（2〜3階層）
  → 親にリフトアップ（→ ③章）

離れた場所で共有？滅多に変わらない？
  → Context

離れた場所で共有？頻繁に変わる？
  → Zustand / Jotai
```

---

## 2. URL状態を活用する（見落とされがち）

検索条件やページ番号を `useState` で持つと、**リロードで消え、URLを共有しても相手に同じ画面が出せません**。

```tsx
// ❌ リロードで消える・共有できない・戻るボタンが効かない
const [keyword, setKeyword] = useState('')
const [page, setPage] = useState(1)

// ✅ URLに持たせる（React Router の例）
const [searchParams, setSearchParams] = useSearchParams()
const keyword = searchParams.get('q') ?? ''
const page = Number(searchParams.get('page') ?? 1)
```

Next.jsの場合は [Next.js⑬](../nextjs/13-architecture-practice.md#3-状態管理の判断) を参照。

> 🔑 **判断基準**：「**この状態を他の人に見せたいか？**」→ Yesなら URL。検索結果・フィルタ・並び順・ページ番号・開いているタブは、ほぼすべてURLに置くべきです。

---

## 3. 状態を最小限にする

### 派生状態を作らない（再掲・重要）

```tsx
// ❌ 3つのstateが互いに矛盾しうる
const [items, setItems] = useState<Item[]>([])
const [count, setCount] = useState(0)
const [hasItems, setHasItems] = useState(false)

// ✅ 1つのstateから計算する
const [items, setItems] = useState<Item[]>([])
const count = items.length
const hasItems = items.length > 0
```

### 「ありえない状態」を作れなくする

```tsx
// ❌ isLoading と isError が同時にtrueになりうる
const [isLoading, setIsLoading] = useState(false)
const [isError, setIsError] = useState(false)
const [data, setData] = useState(null)

// ✅ 1つの状態で表現する（判別可能なユニオン型）
type State =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: User }
  | { status: 'error'; message: string }

const [state, setState] = useState<State>({ status: 'idle' })
```

TypeScriptがコンパイル時に矛盾を防いでくれます。`status: 'loading'` のときに `state.data` へアクセスすると型エラーになります。

### 正規化する（重複を持たない）

```tsx
// ❌ 同じユーザー情報が複数箇所にコピーされている
const [posts, setPosts] = useState([
  { id: 1, title: 'A', author: { id: 10, name: '田中' } },
  { id: 2, title: 'B', author: { id: 10, name: '田中' } },   // 重複
])
// → 田中さんが改名したとき、全部を更新しないとズレる

// ✅ IDで参照する
const [users, setUsers] = useState({ 10: { id: 10, name: '田中' } })
const [posts, setPosts] = useState([
  { id: 1, title: 'A', authorId: 10 },
  { id: 2, title: 'B', authorId: 10 },
])
```

---

## 4. Context — 使いどころと注意点

### 基本の型

```tsx
// contexts/ThemeContext.tsx
type Theme = 'light' | 'dark'
type ThemeContextValue = { theme: Theme; toggle: () => void }

const ThemeContext = createContext<ThemeContextValue | null>(null)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light')
  const toggle = () => setTheme((p) => (p === 'light' ? 'dark' : 'light'))

  return <ThemeContext value={{ theme, toggle }}>{children}</ThemeContext>
}

// ★カスタムフックとセットで公開するのが定石
export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider')
  return ctx
}
```

**Provider の外で使われたら例外を投げる**——これによって「値が `undefined` で謎のエラー」を防げます。

### ⚠️ Contextの2つの弱点

#### ① 値が変わると購読者全員が再レンダリングされる

```tsx
// ❌ 1つのContextに全部詰め込む
<AppContext value={{ user, theme, cart, notifications }}>
```

`cart` が変わっただけで、`theme` しか使っていないコンポーネントまで再レンダリングされます。

**対処**：Contextを分割する。

```tsx
<UserContext value={user}>
  <ThemeContext value={theme}>
    <CartContext value={cart}>
```

#### ② 値のオブジェクトが毎回新しくなる

```tsx
// ❌ 毎レンダリングで新しいオブジェクト → 常に「変わった」と判定
<ThemeContext value={{ theme, toggle }}>
```

React Compilerが有効なら自動で解決されますが、無効な環境では `useMemo` が必要です。

```tsx
const value = useMemo(() => ({ theme, toggle }), [theme])
<ThemeContext value={value}>
```

> 🔑 **Contextは「滅多に変わらない値の配達」に使う**。頻繁に変わる状態には向きません。

---

## 5. 状態管理ライブラリの比較

| ライブラリ | 特徴 | 向いている場面 |
| --- | --- | --- |
| **Zustand** | 最小限のAPI・軽量・学習が速い | **迷ったらこれ**。中小規模のグローバル状態 |
| **Jotai** | アトム単位で管理・再レンダリング範囲が狭い | 細かい粒度で制御したい |
| **TanStack Query** | サーバー状態専用（キャッシュ・再取得） | **API通信があるSPAでは実質必須** |
| **Redux Toolkit** | 大規模・DevToolsが強力・厳格 | 大人数・複雑な状態遷移・履歴が要る |
| **Valtio** | ミュータブルに書ける（Proxy方式） | 書き味重視 |
| **Context のみ** | 追加ライブラリ不要 | テーマ・言語など少数の値 |

### Zustand の例（最も手軽）

```ts
// stores/cartStore.ts
import { create } from 'zustand'

type CartStore = {
  items: CartItem[]
  add: (item: CartItem) => void
  remove: (id: string) => void
  total: () => number
}

export const useCartStore = create<CartStore>((set, get) => ({
  items: [],
  add: (item) => set((s) => ({ items: [...s.items, item] })),
  remove: (id) => set((s) => ({ items: s.items.filter((i) => i.id !== id) })),
  total: () => get().items.reduce((sum, i) => sum + i.price, 0),
}))
```

```tsx
// 使う側：Providerで包む必要すらない
function CartBadge() {
  const count = useCartStore((s) => s.items.length)   // ← 必要な部分だけ購読
  return <span>{count}</span>
}
```

**セレクタ（`(s) => s.items.length`）で必要な部分だけ購読する**ため、他の値が変わっても再レンダリングされません。Contextの弱点①が解消されています。

### TanStack Query の例（サーバー状態）

```tsx
function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetch(`/api/users/${userId}`).then((r) => r.json()),
    staleTime: 60_000,
  })

  if (isLoading) return <Spinner />
  if (error) return <ErrorMessage />
  return <div>{data.name}</div>
}
```

キャッシュ・重複排除・再取得・競合状態の対策が**全部入っています**。[④](04-hooks.md#useeffectを使うべきでない場面) で書いた `useEffect` での自前実装は、これらを全部自分で書くことになります。

> 💡 **Next.js（App Router）を使う場合**、初期表示のデータはServer Componentで取れるため、TanStack Query の出番は「無限スクロール」「ポーリング」など**クライアント主導の場面だけ**に減ります（→ [Next.js⑤](../nextjs/05-data-fetching-caching.md)）。

---

## 6. 「入れなくていい」判断

```
まず何も入れずに書いてみる
    ↓
propsのバケツリレーが3階層を超えて辛い？
    ↓ Yes
Contextで足りる？（滅多に変わらない値か）
    ├─ Yes → Context
    └─ No  → Zustand / Jotai

API通信が多く、キャッシュ管理が辛い？
    → TanStack Query
```

> ⚠️ **「規模が大きくなりそうだからRedux」は避けてください。** 現代のReactでは、サーバー状態をTanStack QueryかRSCに、URL状態をURLに逃がすと、**グローバル状態として残るものは驚くほど少なくなります**。多くの場合Zustandで十分です。

---

## 7. 実践：状態設計の見直し例

### Before（よくある形）

```tsx
function ProductPage() {
  const [products, setProducts] = useState([])       // サーバー状態
  const [isLoading, setIsLoading] = useState(false)  // サーバー状態
  const [error, setError] = useState(null)           // サーバー状態
  const [keyword, setKeyword] = useState('')         // URL状態
  const [page, setPage] = useState(1)                // URL状態
  const [filtered, setFiltered] = useState([])       // 派生状態
  const [isModalOpen, setIsModalOpen] = useState(false)  // UI状態

  useEffect(() => { /* 取得処理 */ }, [])
  useEffect(() => { setFiltered(/* 絞り込み */) }, [products, keyword])
  // ...
}
```

7つのstateと2つのEffectがあり、互いに絡み合っています。

### After（種類ごとに置き場所を変える）

```tsx
function ProductPage() {
  // URL状態 → URLへ
  const [searchParams, setSearchParams] = useSearchParams()
  const keyword = searchParams.get('q') ?? ''
  const page = Number(searchParams.get('page') ?? 1)

  // サーバー状態 → TanStack Query（キャッシュ・エラー処理込み）
  const { data: products = [], isLoading, error } = useQuery({
    queryKey: ['products', keyword, page],
    queryFn: () => fetchProducts({ keyword, page }),
  })

  // 派生状態 → 計算する
  const filtered = products.filter((p) => p.inStock)

  // UI状態 → useState（これだけが本当のローカル状態）
  const [isModalOpen, setIsModalOpen] = useState(false)
}
```

**stateは1つだけになり、Effectはゼロ**になりました。リロードしても検索条件は残り、URLを共有すれば同じ画面が出ます。

---

## 8. この章のまとめ

- 🚨 **まず状態を分類する**：サーバー状態 / URL状態 / フォーム / UI（ローカル・グローバル）
- **サーバー状態をグローバル状態にしない**。RSC か TanStack Query に任せる
- **検索条件・ページ番号はURLに置く**（共有・リロード・戻るボタンが効く）
- **派生状態を作らない**。計算で求める
- **「ありえない状態」を型で防ぐ**（判別可能なユニオン型）
- **Contextは滅多に変わらない値に**。分割し、カスタムフックとセットで公開する
- ライブラリは **迷ったらZustand、API通信が多いならTanStack Query**
- **まず何も入れずに書く**。必要になってから足す

---

次の章 → [⑦ React 19の新機能](07-react19-features.md)
