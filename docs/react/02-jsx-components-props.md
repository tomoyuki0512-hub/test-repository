---
title: ② JSX・コンポーネント・props
---

# ② JSX・コンポーネント・props

[← 総合インデックスに戻る](README.md) ｜ 前 → [① Reactとは何か](01-what-is-react.md) ｜ 次 → [③ stateとイベント](03-state-events.md)

Reactのコードを構成する3つの基本要素を扱います。この章の内容だけで、**動きのない画面**は作れるようになります。

---

## 1. JSX — HTMLに見えるがJavaScript

```jsx
const element = <h1>こんにちは</h1>
```

HTMLのようですが、これは**JavaScriptの式**です。ビルド時に次のように変換されます。

```js
// 変換後（実際にブラウザで動くコード）
const element = React.createElement('h1', null, 'こんにちは')
```

つまり **JSXは「関数呼び出しの読みやすい書き方」** にすぎません。だから次のようなことができます。

```jsx
// 変数に入れられる
const title = <h1>タイトル</h1>

// 配列に入れられる
const items = [<li>A</li>, <li>B</li>]

// 関数から返せる
function getTitle() {
  return <h1>タイトル</h1>
}
```

### 波かっこ `{}` でJavaScriptを埋め込む

```jsx
const name = '田中'
const price = 1500

<div>
  <p>{name}さん</p>                        {/* 変数 */}
  <p>{price * 1.1}円（税込）</p>            {/* 計算式 */}
  <p>{name.toUpperCase()}</p>              {/* 関数呼び出し */}
  <p>{price > 1000 ? '高い' : '安い'}</p>   {/* 三項演算子 */}
</div>
```

> ⚠️ **`{}` の中に書けるのは「式」だけ**です。`if` 文や `for` 文（＝文）は書けません。条件分岐は三項演算子か `&&` を使います（後述）。

### HTMLとの違い（つまずきポイント）

| HTML | JSX | 理由 |
| --- | --- | --- |
| `class="box"` | **`className="box"`** | `class` はJSの予約語 |
| `for="id"` | **`htmlFor="id"`** | `for` はJSの予約語 |
| `onclick="..."` | **`onClick={...}`** | キャメルケース＋関数を渡す |
| `style="color: red"` | **`style={{ color: 'red' }}`** | オブジェクトで渡す |
| `<br>` | **`<br />`** | 必ず閉じる |
| `tabindex` | **`tabIndex`** | キャメルケース |

```jsx
// styleはオブジェクト。外側の{}は「JSを書く」、内側の{}は「オブジェクト」
<div style={{ color: 'red', fontSize: '16px' }}>赤い文字</div>
```

### 必ず1つの要素で包む

```jsx
// ❌ エラー：並列の要素を返せない
return (
  <h1>タイトル</h1>
  <p>本文</p>
)

// ✅ 親要素で包む
return (
  <div>
    <h1>タイトル</h1>
    <p>本文</p>
  </div>
)

// ✅ 余計なdivを作りたくないならフラグメント
return (
  <>
    <h1>タイトル</h1>
    <p>本文</p>
  </>
)
```

`<>...</>` は **フラグメント**といい、DOMに何も出力せずまとめるためのものです。

---

## 2. コンポーネント — 画面の部品

### 定義のしかた

**大文字で始まる関数**がコンポーネントです。JSXを返します。

```tsx
function Greeting() {
  return <h1>こんにちは</h1>
}

// 使う
<Greeting />
```

> 🚨 **必ず大文字で始めてください。** 小文字だとReactはHTMLタグだと解釈します。`<greeting />` は「greetingという名前のHTMLタグ」として扱われ、何も表示されません。**エラーも出ないので気づきにくい**、初学者が最もハマるポイントです。

### コンポーネントの分け方

「どこで分けるか」は初学者が迷うところです。目安は次のとおりです。

```
分けるべきサイン
  ・同じ見た目が2箇所以上に出てくる
  ・1つの関数が100行を超えてきた
  ・「〜カード」「〜リスト」など名前を付けられる塊がある
  ・その部分だけ独立してテストしたい

分けなくていいサイン
  ・1回しか使わず、10行程度
  ・分けると props の受け渡しが複雑になるだけ
```

> 💡 **「将来使い回すかも」で分けない**でください。実際に2回目が出てきたときに分けるほうが、適切な形になります。

---

## 3. props — 親から子へデータを渡す

コンポーネントに外から値を渡す仕組みです。**HTMLの属性のように書きます。**

```tsx
// 受け取る側
function Greeting({ name, age }: { name: string; age: number }) {
  return <p>{name}さん（{age}歳）</p>
}

// 渡す側
<Greeting name="田中" age={30} />
```

| 渡し方 | 書き方 |
| --- | --- |
| 文字列 | `name="田中"` |
| 数値・真偽値・変数 | `age={30}` `isActive={true}` `user={user}` |
| 真偽値のtrue | `isActive`（値を省略できる） |
| 関数 | `onClick={handleClick}` |

### 型定義（TypeScript）

```tsx
type ButtonProps = {
  label: string
  variant?: 'primary' | 'secondary'   // ? は省略可能
  disabled?: boolean
  onClick: () => void
}

function Button({ label, variant = 'primary', disabled = false, onClick }: ButtonProps) {
  return (
    <button className={variant} disabled={disabled} onClick={onClick}>
      {label}
    </button>
  )
}
```

`variant = 'primary'` のように**デフォルト値**を書けます。

### 🚨 propsは書き換えてはいけない

```tsx
function Bad({ name }) {
  name = name.toUpperCase()   // ❌ propsの書き換えは禁止
  return <p>{name}</p>
}

function Good({ name }) {
  const upperName = name.toUpperCase()   // ✅ 新しい変数を作る
  return <p>{upperName}</p>
}
```

**propsは「読み取り専用」** です。データは常に**親から子への一方向**に流れます。これによって「どこで値が変わったか」を追跡できます。

```
        App（データを持つ）
         ↓ props
      PostList
         ↓ props
      PostCard      ← 子は受け取るだけ。書き換えない
```

> ❓ **「子から親のデータを変えたい」場合は？** → 親から**関数を渡します**。子はその関数を呼ぶだけ。詳しくは [③ stateとイベント](03-state-events.md) で扱います。

### `children` — タグで挟んだ中身を受け取る

```tsx
function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="card-body">{children}</div>
    </div>
  )
}

// 使う側：タグで挟んだ部分が children になる
<Card title="お知らせ">
  <p>本日は営業しています。</p>
  <button>詳細</button>
</Card>
```

`children` は**レイアウト系コンポーネント**を作るときの基本パターンです。

---

## 4. 条件分岐 — 出し分ける

JSXの中に `if` は書けないため、次の3つを使います。

### ① 三項演算子（A か B）

```jsx
<p>{isLoggedIn ? 'ようこそ' : 'ログインしてください'}</p>
```

### ② `&&`（条件を満たすときだけ表示）

```jsx
{hasError && <p className="error">エラーがあります</p>}
{items.length > 0 && <ItemList items={items} />}
```

> 🚨 **`&&` の落とし穴**：左辺が **数値の0** のとき、`0` がそのまま画面に表示されます。
> ```jsx
> {items.length && <List />}   // ❌ 0件のとき画面に "0" と出る
> {items.length > 0 && <List />}  // ✅ 必ず真偽値にする
> ```
> これは実務でも頻繁に見るバグです。**`&&` の左辺は必ず真偽値にしてください。**

### ③ 早期リターン（複雑な場合）

```tsx
function UserProfile({ user, isLoading }) {
  if (isLoading) return <Spinner />
  if (!user) return <p>ユーザーが見つかりません</p>

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.bio}</p>
    </div>
  )
}
```

JSXの中がネストで読みにくくなったら、**早期リターンに書き換える**と一気に読みやすくなります。

---

## 5. リスト表示と `key`

配列から要素を並べるには `map()` を使います。

```tsx
function PostList({ posts }: { posts: Post[] }) {
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

### `key` は何のためにあるか

**Reactが「どれがどれか」を見分けるための目印**です。付けないと警告が出ます。

```
key なし：
  ["A", "B", "C"] → ["X", "A", "B", "C"] に変わったとき
  Reactは「1番目がAからXに、2番目がBからAに…」と
  全部が変わったと解釈して、全要素を作り直す

key あり：
  「Xが先頭に追加されただけ」と正しく判断でき、
  A・B・Cの要素はそのまま再利用される
```

### 🚨 `key` に配列のindexを使ってはいけない（並び替え・削除がある場合）

```jsx
// ❌ 危険：並び替え・削除・挿入があると表示がズレる
{items.map((item, index) => <Item key={index} item={item} />)}

// ✅ データ固有のIDを使う
{items.map((item) => <Item key={item.id} item={item} />)}
```

**具体的に何が起きるか**：チェックボックス付きリストで、2番目にチェックを入れてから1番目を削除すると、**チェックが別の項目に移動して見える**——`key={index}` だとこういうバグが起きます。

> 💡 indexを使ってよいのは「**並び順が絶対に変わらず、追加・削除もない**」静的なリストだけです。迷ったらIDを使ってください。

---

## 6. コンポーネント設計の実例

```tsx
// types.ts
type Post = {
  id: string
  title: string
  excerpt: string
  publishedAt: Date
}

// PostCard.tsx — 1件分の表示だけを担当
function PostCard({ post }: { post: Post }) {
  return (
    <article className="card">
      <h3>{post.title}</h3>
      <p>{post.excerpt}</p>
      <time>{post.publishedAt.toLocaleDateString('ja-JP')}</time>
    </article>
  )
}

// PostList.tsx — 並べることと空状態だけを担当
function PostList({ posts }: { posts: Post[] }) {
  if (posts.length === 0) {
    return <p>記事がまだありません</p>
  }

  return (
    <div className="list">
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  )
}
```

**それぞれが1つのことだけをしている**のがポイントです。`PostCard` は1件の見た目、`PostList` は並べ方と空状態。この分け方だと、後から「カードのデザインを変える」ときに触る場所が1箇所で済みます。

---

## 7. よくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| 何も表示されない | コンポーネント名が小文字 | **大文字で始める** |
| `Objects are not valid as a React child` | オブジェクトをそのまま表示した | `{obj.name}` のようにプロパティを指定 |
| リストに `0` が表示される | `&&` の左辺が数値 | `length > 0 &&` にする |
| `key` の警告が出る | `map` で `key` がない | 一意なIDを渡す |
| チェック状態がズレる | `key={index}` を使っている | データのIDを使う |
| `class` が効かない | `class` と書いている | `className` にする |
| `Cannot read property of undefined` | データ取得前にアクセスした | `user?.name` やローディング分岐 |

### `Objects are not valid as a React child` の例

```jsx
const user = { name: '田中', age: 30 }

<p>{user}</p>          // ❌ オブジェクトは表示できない
<p>{user.name}</p>     // ✅
<p>{JSON.stringify(user)}</p>   // ✅ デバッグ用
```

---

## 8. この章のまとめ

- **JSXはJavaScript**。`{}` の中には「式」だけ書ける（`if`文は書けない）
- HTMLとの違い：**`className`・`htmlFor`・キャメルケース・自己終了タグ**
- **コンポーネントは必ず大文字で始める**（小文字だと無言で表示されない）
- **propsは読み取り専用**。データは親から子への一方向に流れる
- `children` でタグの中身を受け取れる（レイアウト部品の基本）
- 条件分岐は**三項演算子・`&&`・早期リターン**。`&&` の左辺は必ず真偽値に
- リストの `key` は**データ固有のID**を使う。`index` は表示ズレの原因

---

次の章 → [③ stateとイベント](03-state-events.md)
