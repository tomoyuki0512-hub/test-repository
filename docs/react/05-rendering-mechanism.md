---
title: ⑤ レンダリングの仕組み
---

# ⑤ レンダリングの仕組み — 「なぜ動かないか」の9割はここ

[← 総合インデックスに戻る](README.md) ｜ 前 → [④ フック（Hooks）体系](04-hooks.md) ｜ 次 → [⑥ 状態設計と状態管理](06-state-design.md)

**この章がReactシリーズで最も重要です。** 「なぜか更新されない」「なぜか無限ループする」「なぜか重い」——これらの原因はすべてここにあります。

---

## 1. レンダリングの3段階

Reactが画面を更新するとき、内部では3つの段階を経ています。

```
① トリガー   何かがきっかけで「描き直す」と決まる
                ・初回表示
                ・setState が呼ばれた
                ↓
② レンダリング  コンポーネント関数を実行してJSXを得る
                ※この時点ではまだ画面は変わらない
                ↓
③ コミット     前回との差分を実際のDOMに反映する
                ※ここで初めて画面が変わる
```

> 🔑 **「レンダリング＝画面が変わること」ではありません。** レンダリングは「関数を実行して設計図を作ること」。実際に画面が変わるのは③のコミットだけです。差分がなければ、②を実行しても画面は何も変わりません。

---

## 2. コンポーネントは「毎回最初から実行される」

これが最も重要な理解です。

```tsx
function Counter() {
  console.log('実行された')          // ← setCountのたびに出力される
  const [count, setCount] = useState(0)
  const doubled = count * 2           // ← 毎回計算し直される
  const handleClick = () => setCount(count + 1)   // ← 毎回新しい関数が作られる

  return <button onClick={handleClick}>{doubled}</button>
}
```

`setCount` を呼ぶたびに、**この関数がまるごと最初から実行されます**。

```
1回目の実行: count=0, doubled=0, handleClick=関数A
    ↓ ボタンクリック → setCount(1)
2回目の実行: count=1, doubled=2, handleClick=関数B（Aとは別物）
```

### ここから導かれること

| 事実 | 帰結 |
| --- | --- |
| 関数内の変数は毎回作り直される | 値を保持したいなら `useState` か `useRef` |
| 関数も毎回新しく作られる | 子に渡すと「毎回違うprops」になる |
| `useState(0)` の `0` は初回のみ使われる | 2回目以降はReactが記憶した値が返る |
| レンダリング中に副作用を書くと毎回走る | 副作用は `useEffect` かイベントハンドラへ |

---

## 3. いつ再レンダリングされるか

**3つのきっかけしかありません。**

```
① 自分の state が変わったとき
② 自分の props が変わったとき（正確には「親が再レンダリングされたとき」）
③ 使っている Context の値が変わったとき
```

### 🚨 誤解しやすい点：親が再レンダリングされると子も再レンダリングされる

```tsx
function Parent() {
  const [count, setCount] = useState(0)
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>{count}</button>
      <Child name="固定値" />      {/* propsは変わっていないのに再レンダリングされる */}
    </div>
  )
}
```

**propsが同じでも、親が再レンダリングされれば子も再レンダリングされます。** これはReactの既定の動作です。

ただし——**それは通常、問題になりません。** レンダリング（関数の実行）は軽く、DOMへの反映は差分がなければ起きないためです。

> ⚠️ **「再レンダリング＝悪」ではありません。** 初学者が最適化に走りすぎてコードを複雑にするのはよくある失敗です。**実際に遅いと計測できてから**対処してください。

---

## 4. 更新されないときの原因

### 原因1：オブジェクト/配列を書き換えた（最頻出）

```tsx
// ❌ 同じ配列を渡している → Reactは「変わっていない」と判断
items.push(newItem)
setItems(items)

// ✅ 新しい配列
setItems([...items, newItem])
```

Reactは **`Object.is()` による比較**（参照の比較）で変更を判断します。

```js
const a = [1, 2]
const b = a
b.push(3)
Object.is(a, b)   // true → 「変わっていない」と判断される
```

詳しくは [③ イミュータブル更新](03-state-events.md#ルール3stateは書き換えず新しい値を作るイミュータブル)。

### 原因2：propsをstateにコピーしている

```tsx
// ❌ 初回の値で固定される
function Editor({ post }) {
  const [text, setText] = useState(post.body)   // post が変わっても更新されない
```

**対処**：`key` を変えてコンポーネントごと作り直す。

```tsx
<Editor key={post.id} post={post} />
```

### 原因3：同じ値をsetしている

```tsx
setCount(0)   // すでに0なら、Reactは再レンダリングをスキップする
```

これは最適化であり、正常な動作です。

---

## 5. 無限ループの原因と対処

```tsx
// ❌ 無限ループ：Effect内でstateを更新 → 再レンダリング → Effect実行 → ...
useEffect(() => {
  setCount(count + 1)
})   // 依存配列がない
```

```tsx
// ❌ 無限ループ：オブジェクトは毎回「新しい」と判定される
const options = { limit: 10 }         // 毎回新しいオブジェクト
useEffect(() => {
  fetchData(options)
}, [options])                          // 毎回変わったと判定 → 無限ループ

// ✅ 対処1：プリミティブ値を依存配列に入れる
useEffect(() => {
  fetchData({ limit })
}, [limit])

// ✅ 対処2：Effectの中で作る
useEffect(() => {
  const options = { limit: 10 }
  fetchData(options)
}, [])
```

> 🔑 **依存配列にはプリミティブ値（文字列・数値・真偽値）を入れる**のが鉄則です。オブジェクトや配列を入れると毎回「変わった」と判定されます。

---

## 6. `key` とコンポーネントの同一性

`key` は「リストの警告を消すもの」ではなく、**Reactが要素を識別する仕組み**です。

```tsx
// key が変わると、Reactは「別のコンポーネント」として扱う
// → 状態がリセットされ、Effectが再実行される
<UserProfile key={userId} userId={userId} />
```

これは**意図的に状態をリセットしたいとき**に使える強力なテクニックです。

```tsx
// ❌ useEffectでリセットする（一瞬古い値が見える）
useEffect(() => { setDraft('') }, [postId])

// ✅ keyでコンポーネントごと作り直す
<Editor key={postId} />
```

### リストでの `key` の重要性（再掲）

```tsx
// ❌ 削除・並び替えで表示がズレる
{items.map((item, i) => <Row key={i} item={item} />)}

// ✅
{items.map((item) => <Row key={item.id} item={item} />)}
```

---

## 7. パフォーマンス最適化 — ただし後回しでよい

### React Compiler の登場で状況が変わった

**React Compiler 1.0（安定版）** は、ビルド時にコードを解析して**自動でメモ化を挿入**します。

```tsx
// Compilerが有効なら、これだけで最適化される
function ProductList({ products, filter }) {
  const filtered = products.filter((p) => p.category === filter)   // 自動でメモ化
  return <List items={filtered} />
}
```

> 🔑 **新規コードでは `useMemo` / `useCallback` を書かないでください。** Compilerが手動より正確に判断します。手書きのメモ化は、依存配列の書き間違いでかえってバグの原因になります。

有効化（Next.js の場合）：

```ts
// next.config.ts
const nextConfig = {
  reactCompiler: true,
}
```

### 手動メモ化が今も必要な場面

Compilerが対応しきれないケースもあります。

| API | 用途 | 今も必要な場面 |
| --- | --- | --- |
| `useMemo` | 計算結果を保持 | **本当に重い計算**（数千件のソート等） |
| `useCallback` | 関数の同一性を保つ | 外部ライブラリが参照の同一性を要求する場合 |
| `React.memo` | propsが同じなら再レンダリングを skip | 巨大なリストの各行など |

```tsx
// 重い計算の例
const sorted = useMemo(
  () => hugeArray.slice().sort((a, b) => b.score - a.score),
  [hugeArray],
)
```

### 最適化の正しい順序

```
1. まず計測する（React DevTools Profiler / Performance Tracks）
      ↓
2. 本当に遅いか確認する（体感で判断しない）
      ↓
3. データ構造・アルゴリズムを見直す  ← 最も効く
      ↓
4. 表示件数を減らす（ページング・仮想スクロール）
      ↓
5. それでも必要ならメモ化
```

> ⚠️ **メモ化にもコストがあります。** 比較処理とメモリを消費するため、軽い処理に付けると**かえって遅くなります**。「とりあえず `useMemo`」は避けてください。

### 計測ツール

| ツール | 用途 |
| --- | --- |
| **React DevTools Profiler** | どのコンポーネントが何ms掛かったか |
| **Performance Tracks**（19.2） | Chrome DevTools上でReactの内部処理を可視化 |
| **Highlight updates** | 再レンダリングされた箇所を画面上で光らせる |

---

## 8. 重い更新を後回しにする（`useTransition`）

入力に対する反応は即座に、重い処理は後回しにできます。

```tsx
function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  function handleChange(e) {
    setQuery(e.target.value)          // 即座に反映（入力欄はカクつかない）

    startTransition(() => {
      setResults(search(e.target.value))   // 重い処理は低優先度で
    })
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <ResultList results={results} />
    </>
  )
}
```

「検索結果の描画が重くて入力がカクつく」という典型的な問題を解決できます。

---

## 9. よくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| 画面が更新されない | 配列/オブジェクトを直接変更 | 新しい値を作る |
| 無限ループ | 依存配列にオブジェクト | プリミティブ値にする |
| propsが変わっても表示が古い | propsをstateにコピー | `key` で作り直す |
| リストの状態がズレる | `key={index}` | データのIDを使う |
| 入力がカクつく | 重い処理が同期実行 | `useTransition` |
| メモ化しても速くならない | ボトルネックが別の場所 | Profilerで計測する |

---

## 10. この章のまとめ

- レンダリングは **①トリガー → ②レンダリング → ③コミット** の3段階。②は画面を変えない
- **コンポーネント関数は毎回最初から実行される**。変数も関数も作り直される
- 再レンダリングのきっかけは **state・props（親の再レンダリング）・Context** の3つだけ
- **親が再レンダリングされれば子もされる**。ただし通常は問題にならない
- 更新されない原因の筆頭は **オブジェクト/配列の直接書き換え**
- 無限ループの原因は **依存配列のオブジェクト**
- **`key` を変えると状態がリセットされる**——意図的なリセット手段として使える
- **React Compilerにより `useMemo`/`useCallback` は原則不要**。計測してから最適化する

---

次の章 → [⑥ 状態設計と状態管理](06-state-design.md)
