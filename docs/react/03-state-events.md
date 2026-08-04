---
title: ③ stateとイベント
---

# ③ stateとイベント — 画面に動きをつける

[← 総合インデックスに戻る](README.md) ｜ 前 → [② JSX・コンポーネント・props](02-jsx-components-props.md) ｜ 次 → [④ フック（Hooks）体系](04-hooks.md)

[②](02-jsx-components-props.md) までで静的な画面は作れます。この章で **「操作すると変わる画面」** が作れるようになります。

---

## 1. state とは — コンポーネントが持つ記憶

**時間とともに変化し、変わったら画面を描き直すべきデータ**が state です。

```tsx
import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)
  //     ↑現在の値  ↑更新する関数        ↑初期値

  return (
    <button onClick={() => setCount(count + 1)}>
      {count} 回クリック
    </button>
  )
}
```

### なぜ普通の変数ではダメなのか

```tsx
// ❌ これは動かない
function Counter() {
  let count = 0

  return (
    <button onClick={() => { count++; console.log(count) }}>
      {count}
    </button>
  )
}
```

`count++` 自体は実行され、コンソールには増えた値が出ます。**しかし画面は変わりません。** 理由は2つ：

1. **Reactに「変わったから描き直して」と伝わっていない**
2. 仮に描き直されても、関数がまた最初から実行されて `let count = 0` に戻る

`useState` はこの両方を解決します。**値をReactが保持し、`setCount` を呼ぶと再レンダリングが起きる**のです。

```
setCount(1) を呼ぶ
    ↓
Reactが値を 1 として記憶
    ↓
Counter関数をもう一度実行
    ↓
useState(0) は「記憶している 1」を返す  ← 初期値0は最初の1回だけ
    ↓
新しいJSXができて画面が更新される
```

---

## 2. state更新の3つのルール

### ルール1：更新は非同期的にまとめられる

```tsx
function handleClick() {
  console.log(count)      // 0
  setCount(count + 1)
  console.log(count)      // ⚠️ まだ 0！（次のレンダリングまで変わらない）
}
```

**`setCount` を呼んだ直後に `count` を見ても、まだ古い値です。** これはバグではなく仕様で、Reactは複数の更新をまとめて一度に処理します（バッチ処理）。

### ルール2：前の値から計算するなら関数形式を使う

```tsx
// ❌ 3回呼んでも1しか増えない
setCount(count + 1)   // 0 + 1 = 1
setCount(count + 1)   // 0 + 1 = 1（countはまだ0）
setCount(count + 1)   // 0 + 1 = 1

// ✅ 関数形式なら正しく3増える
setCount((prev) => prev + 1)   // 0 → 1
setCount((prev) => prev + 1)   // 1 → 2
setCount((prev) => prev + 1)   // 2 → 3
```

> 🔑 **覚え方**：「**前の値を使うなら関数形式**」。特に非同期処理（`setTimeout`・`fetch` の後）の中で更新するときは、関数形式でないと古い値を掴んで不具合になります。

### ルール3：🚨 stateは書き換えず、新しい値を作る（イミュータブル）

**これがReactで最も重要なルールです。**

```tsx
// ❌ 直接書き換え → 画面が更新されない
const [items, setItems] = useState<string[]>([])
items.push('新項目')        // 配列を書き換えた
setItems(items)             // 同じ配列を渡している → Reactは「変わっていない」と判断

// ✅ 新しい配列を作る
setItems([...items, '新項目'])
```

Reactは **「前と同じオブジェクトか」** で変更を判断します（参照の比較）。中身を書き換えても入れ物が同じなら、Reactには変化が見えません。

#### 配列の操作チートシート

| やりたいこと | ❌ 書き換え | ✅ 新しく作る |
| --- | --- | --- |
| 末尾に追加 | `arr.push(x)` | `[...arr, x]` |
| 先頭に追加 | `arr.unshift(x)` | `[x, ...arr]` |
| 削除 | `arr.splice(i, 1)` | `arr.filter((_, idx) => idx !== i)` |
| 特定IDを削除 | — | `arr.filter((item) => item.id !== id)` |
| 更新 | `arr[i].done = true` | `arr.map((item) => item.id === id ? { ...item, done: true } : item)` |
| 並び替え | `arr.sort()` | `[...arr].sort()` |
| 反転 | `arr.reverse()` | `[...arr].reverse()` |

> ⚠️ **`sort()` と `reverse()` は元の配列を書き換えます。** 必ず `[...arr]` でコピーしてから呼んでください。これは見落としやすい罠です。

#### オブジェクトの更新

```tsx
const [user, setUser] = useState({ name: '田中', age: 30, address: { city: '東京' } })

// ✅ 浅い階層
setUser({ ...user, age: 31 })

// ✅ 深い階層（各階層を展開する必要がある）
setUser({
  ...user,
  address: { ...user.address, city: '大阪' },
})
```

深いネストが辛くなったら、**データ構造をフラットにする**か、[Immer](https://immerjs.github.io/immer/) の導入を検討してください。

---

## 3. イベント処理

### 基本

```tsx
<button onClick={handleClick}>クリック</button>
```

| 主なイベント | 用途 |
| --- | --- |
| `onClick` | クリック |
| `onChange` | 入力値の変更 |
| `onSubmit` | フォーム送信 |
| `onKeyDown` | キー押下 |
| `onFocus` / `onBlur` | フォーカスの取得/喪失 |
| `onMouseEnter` / `onMouseLeave` | ホバー |

### 🚨 関数を「渡す」のであって「呼ぶ」のではない

```tsx
<button onClick={handleClick}>OK</button>      // ✅ 関数を渡す
<button onClick={handleClick()}>NG</button>    // ❌ 即座に実行される
```

`handleClick()` と書くと、**レンダリング時にその場で実行**されてしまいます。state更新を含んでいると無限ループになります。

### 引数を渡したいとき

```tsx
// アロー関数で包む
<button onClick={() => handleDelete(item.id)}>削除</button>
```

### イベントオブジェクト

```tsx
function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault()    // ページのリロードを止める（フォームでは必須）
  // 送信処理
}

function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  console.log(e.target.value)
}
```

---

## 4. フォームの扱い

### 制御コンポーネント（基本形）

入力値をstateで管理する方式です。

```tsx
function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    console.log({ email, password })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}                                  // ← stateを表示
        onChange={(e) => setEmail(e.target.value)}     // ← 入力でstateを更新
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">ログイン</button>
    </form>
  )
}
```

```
入力する → onChange発火 → setState → 再レンダリング → valueが新しい値に
```

### 項目が多いときはオブジェクトでまとめる

```tsx
const [form, setForm] = useState({ name: '', email: '', message: '' })

function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  const { name, value } = e.target
  setForm((prev) => ({ ...prev, [name]: value }))   // ← 計算プロパティ名
}

<input name="name" value={form.name} onChange={handleChange} />
<input name="email" value={form.email} onChange={handleChange} />
```

`name` 属性とstateのキーを揃えることで、ハンドラを1つに統合できます。

### 各種入力の書き方

```tsx
// チェックボックス
<input type="checkbox" checked={agreed} onChange={(e) => setAgreed(e.target.checked)} />

// セレクト
<select value={selected} onChange={(e) => setSelected(e.target.value)}>
  <option value="a">A</option>
</select>

// ラジオ
<input type="radio" name="plan" value="free"
  checked={plan === 'free'} onChange={(e) => setPlan(e.target.value)} />

// テキストエリア（HTMLと違い、中身ではなくvalueで指定）
<textarea value={body} onChange={(e) => setBody(e.target.value)} />
```

> ⚠️ **`value` を渡して `onChange` を渡さない**と、入力できない（読み取り専用の）フィールドになり警告が出ます。意図的に読み取り専用にするなら `readOnly` を付けてください。

> 💡 **項目が10個を超える／バリデーションが複雑**なら、[React Hook Form](https://react-hook-form.com/) の導入を検討してください。Next.jsのServer Actionsを使う場合は [Next.js⑥](../nextjs/06-server-actions-forms.md) も参照。

---

## 5. stateをどこに置くか — リフトアップ

**複数のコンポーネントが同じデータを使うなら、共通の親に置きます。** これを「stateのリフトアップ」といいます。

```
❌ 兄弟同士でデータを共有できない
      App
     ↙    ↘
 Filter    List
 (state)   (stateが見えない)

✅ 共通の親に上げる
      App (state)
     ↙    ↘
 Filter    List
 (関数を受取) (値を受取)
```

```tsx
function App() {
  const [keyword, setKeyword] = useState('')      // ★親が持つ

  return (
    <div>
      <SearchBox keyword={keyword} onChange={setKeyword} />
      <ResultList keyword={keyword} />
    </div>
  )
}

// 子は「値」と「変える関数」を受け取るだけ
function SearchBox({ keyword, onChange }: { keyword: string; onChange: (v: string) => void }) {
  return <input value={keyword} onChange={(e) => onChange(e.target.value)} />
}
```

**子から親のstateを変えたいときは、親から関数を渡す** ——これが [②](02-jsx-components-props.md) で保留にした答えです。

> ⚠️ リフトアップを繰り返すと、使わないコンポーネントを props が通り抜ける「**props バケツリレー**」になります。3階層を超えたら Context や状態管理ライブラリを検討してください（→ [⑥ 状態設計](06-state-design.md)）。

---

## 6. 🚨 stateにすべきでないもの

**stateが増えるほどバグが増えます。** 次のものはstateにしないでください。

### ① 他のstateから計算できるもの（派生state）

```tsx
// ❌ 二重管理。同期を忘れるとズレる
const [items, setItems] = useState([])
const [count, setCount] = useState(0)     // itemsから求まる
const [total, setTotal] = useState(0)     // itemsから求まる

// ✅ レンダリングのたびに計算する
const [items, setItems] = useState([])
const count = items.length
const total = items.reduce((sum, item) => sum + item.price, 0)
```

「stateを更新したのに別の表示が古いまま」というバグの大半がこれです。

### ② propsをそのままコピーしたもの

```tsx
// ❌ 親でuserが変わってもnameは古いまま
function Profile({ user }) {
  const [name, setName] = useState(user.name)
```

初期値としてしか使われないため、propsの変更が反映されません。**編集フォームで「別のユーザーを選んでも前の名前が残る」**というバグの典型です。

### ③ 再レンダリングが不要なもの

タイマーIDやDOM参照など、変わっても画面に影響しないものは `useRef` を使います（→ [④](04-hooks.md)）。

### 判断フロー

```
このデータは...

親から渡される？          → props（stateにしない）
他の値から計算できる？     → 計算する（stateにしない）
変わっても画面が変わらない？ → useRef（stateにしない）
上のどれでもない？         → ✅ state にする
```

---

## 7. よくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| 画面が更新されない | 配列/オブジェクトを直接書き換えた | スプレッド構文で新しく作る |
| `setState` 直後の値が古い | 更新は次のレンダリングで反映 | 関数形式 `setX(prev => ...)` |
| 無限ループになる | `onClick={handleClick()}` と書いた | `()` を外す |
| 入力できない | `value` だけで `onChange` がない | `onChange` を追加 |
| フォーム送信でページが再読み込み | `e.preventDefault()` がない | 追加する |
| 別データを選んでも表示が古い | propsをstateにコピーしている | propsを直接使う |
| 表示が他と食い違う | 派生stateを二重管理している | 計算で求める |

---

## 8. この章のまとめ

- **state = 変化して画面に影響するデータ**。`useState` で宣言する
- `setState` の直後は**まだ古い値**。前の値を使うなら **関数形式** `setX(prev => ...)`
- 🚨 **stateは書き換えず新しい値を作る**（`push` ❌ → `[...arr, x]` ✅）。`sort`/`reverse` も要注意
- イベントは**関数を渡す**（`onClick={fn}`）。`fn()` と書くと即実行される
- フォームは **`value` ＋ `onChange`** の制御コンポーネントが基本
- 複数で使うstateは**共通の親に上げる**（リフトアップ）。子には関数を渡す
- 🚨 **計算で求まるもの・propsのコピーはstateにしない**

---

次の章 → [④ フック（Hooks）体系](04-hooks.md)
