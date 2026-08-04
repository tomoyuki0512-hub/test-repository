---
title: ① Reactとは何か
---

# ① Reactとは何か — 宣言的UIと仮想DOM

[← 総合インデックスに戻る](README.md) ｜ 次 → [② JSX・コンポーネント・props](02-jsx-components-props.md)

この章では **「Reactは何を解決するために生まれたのか」** を理解します。ここが腑に落ちると、以降の書き方が丸暗記ではなく理屈でわかるようになります。

---

## 1. Reactが解決した問題

### React以前の世界

ボタンを押すとカウンタが増える、という単純な機能を素のJavaScriptで書くとこうなります。

```js
// ❌ 手続き的：「どう変えるか」を全部書く
let count = 0
const button = document.getElementById('btn')
const label = document.getElementById('label')
const badge = document.getElementById('badge')

button.addEventListener('click', () => {
  count++
  label.textContent = `現在: ${count}`         // ここを書き換えて
  badge.textContent = count > 5 ? '多い' : ''  // ここも書き換えて
  if (count > 10) {
    button.disabled = true                     // ここも…
  }
})
```

問題は **「画面のどこを、どの順で書き換えるか」を人間が全部管理する**点です。表示箇所が増えるほど書き忘れが起き、「特定の操作をしたときだけ表示がズレる」という追いにくいバグが発生します。

### Reactの答え：宣言的UI

```jsx
// ✅ 宣言的：「どう見えるべきか」だけ書く
function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>現在: {count}</p>
      {count > 5 && <span>多い</span>}
      <button onClick={() => setCount(count + 1)} disabled={count > 10}>
        増やす
      </button>
    </div>
  )
}
```

**「countが3のときはこう見える」と書くだけ**で、実際の書き換えはReactがやってくれます。

```
手続き的： 「AをBに変えて、CをDに変えて…」  ← 手順を指示
宣言的：   「完成形はこれです」              ← 結果だけ指示
```

> 🔑 **料理に例えると**：手続き的は「鍋を火にかけて、3分待って、塩を入れて…」というレシピ。宣言的は「カレーができている状態」とだけ言えば出てくる、ということです。

---

## 2. 仮想DOM — なぜ速いのか

「完成形を毎回作り直す」と聞くと遅そうですが、Reactは工夫しています。

### DOM操作は重い

ブラウザの画面（DOM）を直接書き換えるのは、コンピュータにとって高コストな処理です。頻繁にやると画面がカクつきます。

### Reactのやり方

```
1. stateが変わる
     ↓
2. コンポーネント関数を再実行 → 新しい「設計図」ができる
     ↓
3. 前回の設計図と比較（差分検出＝ diffing）
     ↓
4. 「本当に変わった部分だけ」実際のDOMに反映
```

この「設計図」が **仮想DOM（Virtual DOM）** です。JavaScriptのただのオブジェクトなので、作ったり比較したりが高速です。

```js
// 仮想DOMの実体は、こういう普通のオブジェクト
{
  type: 'p',
  props: { children: '現在: 3' }
}
```

```
100個の要素があるリストで、1個だけ内容が変わったとき

❌ 全部書き換える     → 100回のDOM操作（重い）
✅ Reactの差分検出   → 1回のDOM操作（軽い）
```

> ⚠️ **よくある誤解**：「仮想DOMがあるからReactは速い」は正確ではありません。**素のJSで最適に書けばReactより速い**です。仮想DOMの価値は「**宣言的に書いても、そこそこ速い**」という点、つまり**開発しやすさと速度の両立**にあります。

---

## 3. コンポーネント — 画面を部品に分ける

Reactでは画面を**部品（コンポーネント）**の組み合わせとして作ります。

```
┌─────────────────────────────┐
│ <Header />                   │
├─────────────────────────────┤
│ <Sidebar />  │ <PostList />  │
│              │  ├ <PostCard/>│
│              │  ├ <PostCard/>│
│              │  └ <PostCard/>│
├─────────────────────────────┤
│ <Footer />                   │
└─────────────────────────────┘
```

```jsx
function App() {
  return (
    <div>
      <Header />
      <PostList />
      <Footer />
    </div>
  )
}
```

**利点**：

- 同じ部品を何度も使える（`<PostCard />` を並べるだけ）
- 修正が1箇所で済む
- 部品ごとにテストできる
- 名前を見れば構造がわかる

---

## 4. Reactの位置づけ — 「ライブラリ」であること

React は**フレームワークではなくライブラリ**です。この違いが重要です。

| | ライブラリ（React） | フレームワーク（Next.js等） |
| --- | --- | --- |
| 範囲 | UIの組み立てだけ | アプリ全体の構造 |
| 自由度 | 高い（他は自分で選ぶ） | 低い（流儀に従う） |
| 決めること | 多い | 少ない |

**Reactに入っていないもの**：

| 必要なもの | Reactに入っているか | どうするか |
| --- | --- | --- |
| ルーティング（URL設計） | ❌ | React Router か Next.js |
| データ取得の作法 | ❌ | fetch / TanStack Query |
| サーバー処理 | ❌ | Node.js / Next.js |
| スタイリング | ❌ | CSS / Tailwind |
| ビルド設定 | ❌ | Vite / Next.js |
| フォーム管理 | ❌ | 自前 / React Hook Form |

> 🔑 だからこそ **[Next.js](../nextjs/README.md)** のようなフレームワークが存在します。関係の整理は [JavaScript・Node.js・React・Next.js の関係](../js-stack-relations.md) を参照してください。

---

## 5. 環境構築 — 何から始めるか

### 選択肢

| 方法 | コマンド | 向いている場面 |
| --- | --- | --- |
| **Vite** | `npm create vite@latest` | **学習・SPA・管理画面**。軽くて速い |
| **Next.js** | `npx create-next-app@latest` | 本番のWebサービス（SEO・サーバー処理が要る） |
| **オンライン環境** | StackBlitz / CodeSandbox | インストール不要で試したいとき |

> 💡 **学習の最初は Vite をおすすめします。** Next.jsはServer/Client Componentsの概念が最初から入ってくるため、「Reactそのもの」を学ぶには余計な複雑さになります。

### Viteで始める

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev
```

> ℹ️ `npm` は Node.js に付属するコマンドです。Reactの開発には **Node.js のインストールが必須**です（→ [Node.js①](../nodejs/01-what-is-nodejs.md)）。

### 最初のコンポーネント

```tsx
// src/App.tsx
import { useState } from 'react'

export default function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <h1>はじめてのReact</h1>
      <p>クリック回数: {count}</p>
      <button onClick={() => setCount(count + 1)}>クリック</button>
    </div>
  )
}
```

---

## 6. Reactの歴史（情報の新旧を見分けるために）

ネットの記事が「いつの話か」を判断するのに役立ちます。

| 時期 | 出来事 | 見分け方のキーワード |
| --- | --- | --- |
| 2013 | React公開（Facebook製） | — |
| 2015 | クラスコンポーネント全盛 | `class extends React.Component`、`this.state` |
| **2019** | **フック（Hooks）登場（v16.8）** | `useState`、`useEffect` ← **現代の書き方はここから** |
| 2022 | v18。並行レンダリング・`Suspense`強化 | `createRoot` |
| **2024** | **v19。Server Components・Actions が安定版に** | `use`、`useActionState`、`'use client'` |
| 2025 | React Compiler 1.0 | 手動メモ化が原則不要に |
| 2025〜 | v19.2。`<Activity>`・`useEffectEvent` | — |

> ⚠️ **古い記事の見分け方**：`class Component`、`this.setState`、`componentDidMount`、`React.FC`、`propTypes` が出てくる記事は**2019年以前の書き方**です。動きはしますが、新規で真似しないでください。対応表は [④ フック](04-hooks.md#8-クラスコンポーネントとの対応表保守用) にあります。

---

## 7. 他のUIライブラリとの比較

| ライブラリ | 特徴 | Reactと比べて |
| --- | --- | --- |
| **React** | エコシステム最大・求人最多 | 基準 |
| **Vue** | 学習しやすい・公式が手厚い | 初心者に優しいが、日本以外では求人が少なめ |
| **Svelte** | コンパイル方式で高速・記述量が少ない | 快適だが情報量・採用実績は少ない |
| **Angular** | フルフレームワーク・大規模向け | 決まりが多く学習コスト高。企業システムで採用 |
| **Solid** | Reactに似た記法で高速 | 仮想DOMを使わない。エコシステムは小さい |

### Reactを選ぶ理由・選ばない理由

```
✅ Reactが向いている
   ・情報量と求人が最重要（学習リソースが圧倒的）
   ・Next.js / React Native と組み合わせたい
   ・チームに経験者がいる

⚠️ 別の選択肢も検討すべき
   ・小さなサイトに少し動きを付けたいだけ  → 素のJS / Alpine.js
   ・とにかく学習コストを下げたい          → Vue
   ・パフォーマンスが最優先                → Svelte / Solid
```

---

## 8. この章のまとめ

- Reactの本質は **宣言的UI**——「どう変えるか」ではなく「**どう見えるべきか**」を書く
- **仮想DOM**は「宣言的に書いても速度が保てる」ための仕組み。速さそのものが目的ではない
- 画面は**コンポーネント**（部品）に分けて組み立てる
- Reactは**ライブラリ**。ルーティング・データ取得・サーバー処理は含まれない
- 学習開始は **Vite** がおすすめ。Node.jsのインストールが前提
- `class` / `this.state` / `componentDidMount` が出る記事は**2019年以前**の書き方

---

次の章 → [② JSX・コンポーネント・props](02-jsx-components-props.md)
