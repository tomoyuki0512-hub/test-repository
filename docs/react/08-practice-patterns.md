---
title: ⑧ 実践パターンとアンチパターン
---

# ⑧ 実践パターンとアンチパターン

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑦ React 19の新機能](07-react19-features.md) ｜ 次 → [用語集](glossary.md)

実務で使える設計パターンと、レビューで指摘されがちな失敗をまとめます。

---

## 1. コンポーネント設計パターン

### ① Container / Presentational（データと見た目の分離）

```tsx
// Presentational：見た目だけ。propsを受け取って描くだけ
function UserCard({ user, onFollow }: { user: User; onFollow: () => void }) {
  return (
    <div className="card">
      <img src={user.avatar} alt="" />
      <h3>{user.name}</h3>
      <button onClick={onFollow}>フォロー</button>
    </div>
  )
}

// Container：データ取得とロジック
function UserCardContainer({ userId }: { userId: string }) {
  const { data: user } = useQuery({ queryKey: ['user', userId], queryFn: () => fetchUser(userId) })
  const { mutate: follow } = useFollowMutation()
  if (!user) return <Skeleton />
  return <UserCard user={user} onFollow={() => follow(userId)} />
}
```

**利点**：見た目だけのコンポーネントは Storybook で確認でき、テストも簡単です。

> 💡 React Server Components（[⑦](07-react19-features.md)）が実質的にこの分離を言語レベルで実現しています。Next.jsを使うなら、Server Componentがデータ取得、Client Componentが操作、という自然な分離になります。

### ② Compound Components（関連する部品をまとめる）

```tsx
<Tabs defaultValue="profile">
  <Tabs.List>
    <Tabs.Trigger value="profile">プロフィール</Tabs.Trigger>
    <Tabs.Trigger value="settings">設定</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="profile"><Profile /></Tabs.Content>
  <Tabs.Content value="settings"><Settings /></Tabs.Content>
</Tabs>
```

内部でContextを使って状態を共有します。**propsを大量に渡さずに柔軟な組み立てができる**のが利点で、Radix UI や shadcn/ui はこの形を採用しています。

### ③ Render Props / children as function

```tsx
<DataLoader url="/api/users">
  {({ data, isLoading }) =>
    isLoading ? <Spinner /> : <UserList users={data} />
  }
</DataLoader>
```

現在はカスタムフックで代替できることが多いため、出番は減っています。

### ④ カスタムフックへのロジック抽出（最頻出・推奨）

```tsx
// ❌ コンポーネントが肥大化
function ProductPage() {
  const [products, setProducts] = useState([])
  const [filters, setFilters] = useState({})
  const [sort, setSort] = useState('new')
  // ... 100行のロジック
  return <div>{/* JSX */}</div>
}

// ✅ ロジックをフックに切り出す
function useProductList() {
  const [filters, setFilters] = useState({})
  const [sort, setSort] = useState('new')
  const { data, isLoading } = useQuery(...)
  const sorted = useMemo(() => sortProducts(data, sort), [data, sort])
  return { products: sorted, filters, setFilters, sort, setSort, isLoading }
}

function ProductPage() {
  const { products, isLoading, setFilters } = useProductList()
  if (isLoading) return <Skeleton />
  return <ProductGrid products={products} onFilterChange={setFilters} />
}
```

**「JSXを返す部分」と「ロジック」を分ける**——最も汎用的で効果の高い整理法です。

---

## 2. アンチパターン集

### ❌ 巨大コンポーネント

```
症状：1ファイル500行、useStateが10個、useEffectが5個
原因：責務が分かれていない
対処：①ロジックをカスタムフックへ ②JSXの塊をコンポーネントへ
```

**目安**：150行を超えたら分割を検討。useStateが5個を超えたら `useReducer` か状態設計の見直し（→ [⑥](06-state-design.md)）。

### ❌ propsバケツリレー

```tsx
// 使わないコンポーネントを props が通り抜けていく
<A user={user} />
  <B user={user} />
    <C user={user} />
      <D user={user} />   {/* ここでやっと使う */}
```

**対処の優先順**：
1. **`children` で構造を変える**（最も簡単）
2. Context
3. 状態管理ライブラリ

```tsx
// ✅ childrenで渡せば中間層は関与しない
<A>
  <B>
    <C>
      <D user={user} />
    </C>
  </B>
</A>
```

### ❌ useEffectでの過剰な同期

```tsx
// ❌ 3つのEffectが連鎖して、レンダリングが4回起きる
useEffect(() => { setB(calcB(a)) }, [a])
useEffect(() => { setC(calcC(b)) }, [b])
useEffect(() => { setD(calcD(c)) }, [c])

// ✅ 計算するだけ。レンダリングは1回
const b = calcB(a)
const c = calcC(b)
const d = calcD(c)
```

詳しくは [④ useEffectを使うべきでない場面](04-hooks.md#-useeffectを使うべきでない場面)。

### ❌ 早すぎる最適化

```tsx
// ❌ すべてに memo / useMemo / useCallback を付ける
const Item = memo(({ item, onClick }) => { ... })
const handleClick = useCallback(() => { ... }, [])
const value = useMemo(() => item.price * 1.1, [item.price])   // 掛け算1回
```

**メモ化にもコストがあります。** 軽い処理に付けると逆に遅くなります。React Compiler（→ [⑤](05-rendering-mechanism.md#react-compiler-の登場で状況が変わった)）がある今、**手動メモ化は原則不要**です。

### ❌ 配列の直接変更

```tsx
items.sort()          // ❌ 元の配列を書き換える
setItems(items)       // 画面が更新されない

setItems([...items].sort())   // ✅
```

### ❌ インデックスをkeyに使う

```tsx
{items.map((item, i) => <Row key={i} />)}   // 削除・並び替えで壊れる
```

### ❌ 何でもグローバル状態にする

```tsx
// ❌ モーダルの開閉までグローバルに置く
const useStore = create(() => ({ isModalOpen: false, ... }))
```

**そのコンポーネント内でしか使わない状態はローカルに置く**のが原則です。

### ❌ `dangerouslySetInnerHTML` の無防備な使用

```tsx
// 🚨 XSS脆弱性。ユーザー入力を直接入れてはいけない
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ サニタイズする
import DOMPurify from 'dompurify'
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(html) }} />
```

---

## 3. エラーハンドリング

### Error Boundary

Reactのエラーで**画面全体が真っ白になる**のを防ぎます。

```tsx
import { ErrorBoundary } from 'react-error-boundary'

<ErrorBoundary
  fallback={<p>問題が発生しました</p>}
  onError={(error, info) => reportToSentry(error, info)}
>
  <Dashboard />
</ErrorBoundary>
```

> ⚠️ **Error Boundaryが捕捉できないもの**：イベントハンドラ内のエラー、非同期処理のエラー、SSR中のエラー。これらは `try/catch` で個別に処理してください。

### 非同期エラー

```tsx
async function handleSubmit() {
  try {
    await save()
  } catch (e) {
    setError(e instanceof Error ? e.message : '不明なエラー')
  }
}
```

### Suspense と組み合わせる

```tsx
<ErrorBoundary fallback={<ErrorView />}>
  <Suspense fallback={<Skeleton />}>
    <UserProfile />
  </Suspense>
</ErrorBoundary>
```

「読み込み中」と「エラー」の両方を宣言的に扱えます。

---

## 4. アクセシビリティ（a11y）

見落とされがちですが、**実装コストは低く効果が大きい**部分です。

### 最低限守ること

```tsx
// ✅ 意味のあるHTMLを使う
<button onClick={handleClick}>送信</button>          // ⭕
<div onClick={handleClick}>送信</div>                // ❌ キーボードで操作できない

// ✅ 画像にalt
<img src="/chart.png" alt="売上推移グラフ" />
<img src="/decoration.png" alt="" />                 // 装飾ならalt=""

// ✅ フォームにラベル
<label htmlFor={id}>メールアドレス</label>
<input id={id} type="email" />

// ✅ useIdで一意なIDを生成
const id = useId()
```

### チェックリスト

- [ ] クリックできる要素は `<button>` か `<a>` を使っている
- [ ] すべての入力に `<label>` が紐付いている
- [ ] 画像に適切な `alt` がある
- [ ] キーボード（Tab / Enter / Esc）だけで操作できる
- [ ] モーダルを開いたらフォーカスが移動し、Escで閉じられる
- [ ] 色だけで情報を伝えていない（エラーを赤色だけで示さない）
- [ ] 見出しが `h1` → `h2` の順になっている

> 💡 **Radix UI / shadcn/ui を使うと、これらの多くが最初から実装されています**（→ [Next.js⑦](../nextjs/07-styling-ui.md)）。自前でモーダルやタブを実装するより、はるかに確実です。

---

## 5. テスト

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

test('フォーム送信でonSubmitが呼ばれる', async () => {
  const onSubmit = vi.fn()
  render(<LoginForm onSubmit={onSubmit} />)

  await userEvent.type(screen.getByLabelText('メールアドレス'), 'a@example.com')
  await userEvent.click(screen.getByRole('button', { name: 'ログイン' }))

  expect(onSubmit).toHaveBeenCalledWith({ email: 'a@example.com' })
})
```

### 良いテストの原則

| 原則 | 説明 |
| --- | --- |
| **ユーザー視点で書く** | 「classNameが付いた」ではなく「ボタンが押せる」を確認 |
| **`getByRole` を優先** | `getByTestId` は最後の手段。a11yの担保も兼ねる |
| **実装詳細をテストしない** | stateの中身ではなく、画面に見えるものを確認 |

```tsx
// ❌ 実装に依存（リファクタで壊れる）
expect(component.state.isOpen).toBe(true)

// ✅ ユーザーに見えるもの
expect(screen.getByRole('dialog')).toBeVisible()
```

Next.jsでのテスト戦略は [Next.js⑪](../nextjs/11-testing-quality.md) を参照してください。

---

## 6. ディレクトリ構成

### 小規模

```
src/
├── components/
├── hooks/
├── lib/
└── App.tsx
```

### 中規模以上（機能ごとにまとめる）

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── api.ts
│   └── posts/
│       ├── components/
│       ├── hooks/
│       └── api.ts
├── components/ui/      # 全機能共通の部品
├── hooks/              # 全機能共通のフック
└── lib/
```

**判断基準**：「この部品は他の機能でも使うか？」→ Yesなら共通、Noなら `features/` の中。

> より詳しい設計論は [Next.js⑬ 実践アーキテクチャ](../nextjs/13-architecture-practice.md) にまとめています。

---

## 7. コードレビューチェックリスト

**設計**
- [ ] コンポーネントが150行を超えていないか
- [ ] ロジックがカスタムフックに切り出されているか
- [ ] 状態の置き場所は適切か（→ [⑥](06-state-design.md)）

**正しさ**
- [ ] 配列/オブジェクトをイミュータブルに更新しているか
- [ ] `key` にindexを使っていないか
- [ ] `useEffect` の依存配列は正しいか、クリーンアップはあるか
- [ ] `&&` の左辺が数値になっていないか

**セキュリティ**
- [ ] `dangerouslySetInnerHTML` にサニタイズがあるか
- [ ] APIキーがクライアントコードに入っていないか

**アクセシビリティ**
- [ ] `<div onClick>` になっていないか
- [ ] ラベル・altがあるか

---

## 8. この章のまとめ

- **ロジックはカスタムフックへ、見た目はコンポーネントへ**——最も汎用的な整理法
- 複合UIは **Compound Components**（Contextで内部状態を共有）
- アンチパターンの筆頭は **巨大コンポーネント・propsバケツリレー・useEffectの過剰使用・早すぎる最適化**
- propsバケツリレーはまず **`children` で構造を変える**ことを検討
- **Error Boundary はイベントハンドラと非同期のエラーを捕捉しない**
- a11yは **意味のあるHTMLを使う**だけで大半が満たせる。UIライブラリ利用も有効
- テストは **`getByRole` でユーザー視点**。実装詳細をテストしない

---

次 → [用語集・チートシート](glossary.md)
