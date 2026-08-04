---
title: ④ フック（Hooks）体系
---

# ④ フック（Hooks）体系

[← 総合インデックスに戻る](README.md) ｜ 前 → [③ stateとイベント](03-state-events.md) ｜ 次 → [⑤ レンダリングの仕組み](05-rendering-mechanism.md)

フックは **「関数コンポーネントからReactの機能を使うための仕組み」** です。この章で主要なフックを体系的に押さえます。

---

## 1. フックの全体像

| フック | 何をするか | 使用頻度 |
| --- | --- | --- |
| **`useState`** | 状態を持つ | ★★★ 毎日使う |
| **`useEffect`** | 外部との同期（購読・タイマー等） | ★★☆ 使うが誤用も多い |
| **`useRef`** | DOM参照・再レンダリング不要な値の保持 | ★★☆ |
| **`useContext`** | 離れた場所へ値を配る | ★★☆ |
| **`useReducer`** | 複雑な状態遷移をまとめる | ★☆☆ |
| **`useMemo` / `useCallback`** | 計算結果・関数のメモ化 | ★☆☆（Compilerで不要に） |
| **`useId`** | 一意なIDを生成（アクセシビリティ用） | ★☆☆ |
| **`useTransition`** | 重い更新を低優先度にする | ★☆☆ |
| **`useEffectEvent`** | Effect内で最新値を使う（19.2） | ★☆☆ |
| **カスタムフック** | 自作のロジック再利用 | ★★★ |

---

## 2. 🚨 フックのルール（絶対）

```tsx
// ✅ 必ずコンポーネントの最上位で呼ぶ
function Good() {
  const [a, setA] = useState(0)
  const [b, setB] = useState(0)
  // ...
}

// ❌ 条件分岐の中で呼ぶ
function Bad({ flag }) {
  if (flag) {
    const [a, setA] = useState(0)   // エラー
  }
}

// ❌ ループ・ネストした関数の中で呼ぶ
function Bad2({ items }) {
  items.forEach(() => {
    const [x] = useState(0)         // エラー
  })
}
```

**理由**：Reactはフックを**呼ばれた順番**で管理しています。条件によって呼ぶ数が変わると、値の対応がずれて壊れます。

```
1回目: useState(0) → 1番目のstate
       useState('') → 2番目のstate

2回目: （条件がfalseで1つ目がスキップされると）
       useState('') → 1番目のstateとして扱われる → 壊れる
```

**ルールは2つだけ**：

1. **トップレベルで呼ぶ**（条件・ループ・ネスト関数の中で呼ばない）
2. **React関数の中で呼ぶ**（コンポーネントかカスタムフックの中だけ）

ESLintの `eslint-plugin-react-hooks` が自動検出してくれるので、必ず有効にしてください。

---

## 3. `useEffect` — 最も誤用されるフック

### 何のためのフックか

**「Reactの外の世界と同期する」ため**のものです。それ以外に使うべきではありません。

```tsx
useEffect(() => {
  // 実行したい処理
  return () => {
    // クリーンアップ（後片付け）
  }
}, [依存配列])
```

### 依存配列の意味

```tsx
useEffect(() => { ... })           // 毎回のレンダリング後に実行（ほぼ使わない）
useEffect(() => { ... }, [])       // 最初の1回だけ
useEffect(() => { ... }, [userId]) // userId が変わったときだけ
```

### 正しい使い方

```tsx
// ✅ タイマー
useEffect(() => {
  const id = setInterval(() => setTime(new Date()), 1000)
  return () => clearInterval(id)      // ★必ず片付ける
}, [])

// ✅ イベント購読
useEffect(() => {
  const onResize = () => setWidth(window.innerWidth)
  window.addEventListener('resize', onResize)
  return () => window.removeEventListener('resize', onResize)
}, [])

// ✅ 外部システムとの接続
useEffect(() => {
  const socket = connectToChat(roomId)
  return () => socket.disconnect()
}, [roomId])
```

> 🔑 **クリーンアップを忘れない**：タイマーやイベントリスナーを片付けないと、コンポーネントが消えた後も動き続け、メモリリークや「消えたはずの画面が更新されようとしてエラー」の原因になります。

### 🚨 useEffectを使うべきでない場面

#### ① データの整形・計算

```tsx
// ❌ 無駄な再レンダリングが1回増える
const [items, setItems] = useState([])
const [filtered, setFiltered] = useState([])
useEffect(() => {
  setFiltered(items.filter((i) => i.active))
}, [items])

// ✅ レンダリング中に計算するだけでよい
const filtered = items.filter((i) => i.active)
```

#### ② イベントへの反応

```tsx
// ❌ 「送信されたら通知」をEffectでやる
useEffect(() => {
  if (submitted) showToast('送信しました')
}, [submitted])

// ✅ イベントハンドラの中で直接やる
function handleSubmit() {
  await save()
  showToast('送信しました')
}
```

**「ユーザーの操作がきっかけ」ならイベントハンドラ、「画面が表示されたことがきっかけ」ならEffect** と覚えてください。

#### ③ propsが変わったときにstateをリセット

```tsx
// ❌ 一瞬古い値が表示される
useEffect(() => { setDraft(post.body) }, [post.id])

// ✅ key を変えてコンポーネントごと作り直す
<PostEditor key={post.id} post={post} />
```

`key` が変わると、Reactはそれを**別のコンポーネント**とみなして状態を初期化します。これは覚えておくと便利なテクニックです。

#### ④ データ取得（現代では非推奨寄り）

```tsx
// ⚠️ 動くが、競合状態・ローディング管理・キャッシュを自前で書くことになる
useEffect(() => {
  fetch(`/api/user/${id}`).then(r => r.json()).then(setUser)
}, [id])
```

**代わりに使うべきもの**：

| 環境 | 推奨 |
| --- | --- |
| Next.js（App Router） | **Server Component で `await`**（→ [Next.js⑤](../nextjs/05-data-fetching-caching.md)） |
| SPA（Vite等） | **TanStack Query** / SWR |
| React 19 | `use()` ＋ `Suspense`（→ [⑦](07-react19-features.md)） |

どうしても `useEffect` で取得するなら、**競合状態（race condition）の対策が必須**です。

```tsx
useEffect(() => {
  let ignore = false            // ★このフラグが重要
  fetch(`/api/user/${id}`)
    .then((r) => r.json())
    .then((data) => { if (!ignore) setUser(data) })
  return () => { ignore = true }
}, [id])
```

**これがないと**：idを素早く切り替えたとき、遅れて返ってきた古いリクエストの結果が後から上書きし、**選んだものと違うデータが表示されます**。

---

## 4. `useRef` — 再レンダリングを起こさない箱

### 用途1：DOMを直接触る

```tsx
function SearchInput() {
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    inputRef.current?.focus()      // 表示時にフォーカスを当てる
  }, [])

  return <input ref={inputRef} />
}
```

### 用途2：再レンダリング不要な値を保持

```tsx
const timerRef = useRef<number | null>(null)

function start() {
  timerRef.current = window.setInterval(tick, 1000)
}
function stop() {
  if (timerRef.current) clearInterval(timerRef.current)
}
```

### `useState` との違い

| | `useState` | `useRef` |
| --- | --- | --- |
| 変更時 | **再レンダリングされる** | されない |
| 値の読み書き | `count` / `setCount()` | `ref.current` |
| 用途 | 画面に出るデータ | DOM参照・タイマーID・前回値 |

> 💡 **判断基準**：「その値が変わったとき、画面を描き直す必要があるか？」→ Yesなら `useState`、Noなら `useRef`。

---

## 5. `useContext` — propsバケツリレーの解消

離れたコンポーネントに値を届ける仕組みです。

```tsx
// 1. Contextを作る
const ThemeContext = createContext<'light' | 'dark'>('light')

// 2. 配る（React 19 では .Provider を省略できる）
function App() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  return (
    <ThemeContext value={theme}>
      <Layout />
    </ThemeContext>
  )
}

// 3. 受け取る（何階層下でもOK）
function Button() {
  const theme = useContext(ThemeContext)
  return <button className={theme}>ボタン</button>
}
```

> ⚠️ **バージョン差分**：React 19 から `<ThemeContext.Provider>` を `<ThemeContext>` と書けるようになりました。18以前は `.Provider` が必須です。

### ⚠️ Contextの注意点

**値が変わると、そのContextを使っている全コンポーネントが再レンダリングされます。** 更新頻度の高い値を入れると、アプリ全体が重くなります。

```
✅ Contextに向いている：テーマ・言語設定・ログインユーザー（滅多に変わらない）
❌ 向いていない：入力中のテキスト・マウス座標（頻繁に変わる）
```

頻繁に変わる状態は Zustand や Jotai を検討してください（→ [⑥ 状態設計](06-state-design.md)）。

---

## 6. `useReducer` — 複雑な状態遷移をまとめる

stateが複数あって互いに関連する場合、`useReducer` にまとめると見通しが良くなります。

```tsx
type State = { status: 'idle' | 'loading' | 'success' | 'error'; data?: User; error?: string }
type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: User }
  | { type: 'FETCH_ERROR'; error: string }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':   return { status: 'loading' }
    case 'FETCH_SUCCESS': return { status: 'success', data: action.payload }
    case 'FETCH_ERROR':   return { status: 'error', error: action.error }
  }
}

function UserProfile() {
  const [state, dispatch] = useReducer(reducer, { status: 'idle' })
  // dispatch({ type: 'FETCH_START' }) のように使う
}
```

**利点**：「loading中なのにdataもerrorも入っている」といった**ありえない状態を作れなくなります**。

| 使い分け | 目安 |
| --- | --- |
| `useState` | 状態が独立している・2〜3個まで |
| `useReducer` | 状態が絡み合う・遷移パターンが決まっている |

---

## 7. カスタムフック — ロジックの再利用

**`use` で始まる自作の関数**です。フックを使うロジックを切り出せます。

```tsx
// hooks/useLocalStorage.ts
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    // 初期値の計算が重い場合は関数を渡す（遅延初期化）
    const stored = localStorage.getItem(key)
    return stored ? JSON.parse(stored) : initialValue
  })

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value))
  }, [key, value])

  return [value, setValue] as const
}

// 使う側はスッキリ
function Settings() {
  const [theme, setTheme] = useLocalStorage('theme', 'light')
  return <button onClick={() => setTheme('dark')}>{theme}</button>
}
```

### よく作るカスタムフック

```tsx
// 入力の遅延反映（検索ボックスなど）
function useDebounce<T>(value: T, delay = 500) {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(id)
  }, [value, delay])
  return debounced
}

// 開閉状態
function useToggle(initial = false) {
  const [on, setOn] = useState(initial)
  return { on, toggle: () => setOn((p) => !p), setOn }
}
```

> 🔑 **カスタムフックは「状態を共有しません」。** 2つのコンポーネントが同じカスタムフックを使っても、**それぞれ独立した状態を持ちます**。共有したいならContextか状態管理ライブラリが必要です。ここは誤解しやすい点です。

---

## 8. クラスコンポーネントとの対応表（保守用）

古いコードを読むときの変換表です。

| クラス | フック |
| --- | --- |
| `this.state = {...}` | `useState` |
| `this.setState({...})` | `setX(...)` |
| `componentDidMount` | `useEffect(() => {...}, [])` |
| `componentDidUpdate` | `useEffect(() => {...}, [deps])` |
| `componentWillUnmount` | `useEffect` の return（クリーンアップ） |
| `shouldComponentUpdate` | `React.memo` |
| `createRef` | `useRef` |
| `contextType` | `useContext` |

> 新規開発でクラスコンポーネントを書く理由はありません。既存コードの保守でのみ必要な知識です。

---

## 9. よくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| `Invalid hook call` | 条件・ループ内でフックを呼んだ | トップレベルで呼ぶ |
| useEffectが無限に実行される | 依存配列にオブジェクト/配列を入れた | プリミティブ値にするか `useMemo` |
| useEffectが実行されない | 依存配列が `[]` のまま | 必要な値を依存配列へ |
| 古い値を掴んでいる | クロージャが古いstateを参照 | 関数形式 or `useEffectEvent` |
| 開発時に2回実行される | StrictModeの意図的な挙動 | クリーンアップを正しく書けば問題なし |
| データがちらつく/入れ替わる | 競合状態 | `ignore` フラグ or TanStack Query |

### StrictModeで2回実行される件

開発モードでは、React が**わざと**Effectを2回実行します（マウント→アンマウント→再マウント）。これは**クリーンアップの書き忘れを検出するため**です。

```
本番では1回しか実行されません。
2回実行されて問題が出る＝クリーンアップが不足しているサイン
```

「2回実行されるのが嫌だからStrictModeを外す」は**問題を隠すだけ**なので避けてください。

---

## 10. この章のまとめ

- 🚨 **フックはトップレベルでのみ呼ぶ**（条件・ループの中は禁止）
- **`useEffect` は「外の世界との同期」専用**。計算・イベント反応・データ取得には使わない
- Effectには**クリーンアップを必ず書く**。StrictModeの2回実行はその検出用
- **`useRef` は再レンダリングを起こさない箱**。DOM参照・タイマーIDに使う
- **`useContext` は滅多に変わらない値に**。頻繁に変わる値はアプリ全体を重くする
- **`useReducer`** は状態が絡み合うときに「ありえない状態」を防ぐ
- **カスタムフックは状態を共有しない**（それぞれ独立した状態を持つ）

---

次の章 → [⑤ レンダリングの仕組み](05-rendering-mechanism.md)
