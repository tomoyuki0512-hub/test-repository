---
title: React 用語集・チートシート
---

# 用語集・チートシート

[← 総合インデックスに戻る](README.md)

用語辞典と「困った時どの章？」の逆引き表です。

---

## 1. 用語集

### 基本概念

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **宣言的UI** | 「どう変えるか」ではなく「どう見えるべきか」を書く方式 | [①](01-what-is-react.md) |
| **仮想DOM** | 前回との差分を計算するためのJSオブジェクト表現 | [①](01-what-is-react.md) |
| **コンポーネント** | 画面の部品。JSXを返す関数（**必ず大文字始まり**） | [②](02-jsx-components-props.md) |
| **JSX** | HTMLに似たJavaScriptの構文。ビルド時に関数呼び出しへ変換 | [②](02-jsx-components-props.md) |
| **フラグメント** | `<>...</>`。DOMを増やさず複数要素をまとめる | [②](02-jsx-components-props.md) |
| **props** | 親から子へ渡すデータ。**読み取り専用** | [②](02-jsx-components-props.md) |
| **children** | タグで挟んだ中身を受け取る特別なprops | [②](02-jsx-components-props.md) |
| **state** | 変化して画面に影響するデータ | [③](03-state-events.md) |
| **リフトアップ** | 共有したいstateを共通の親に移すこと | [③](03-state-events.md) |
| **イミュータブル** | 元の値を変えず、新しい値を作ること | [③](03-state-events.md) |
| **制御コンポーネント** | 入力値をstateで管理するフォーム | [③](03-state-events.md) |

### フック

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **フック** | 関数コンポーネントからReactの機能を使う仕組み。`use`で始まる | [④](04-hooks.md) |
| **`useState`** | 状態を持つ | [③](03-state-events.md) |
| **`useEffect`** | **外部との同期**（購読・タイマー）。計算や取得には使わない | [④](04-hooks.md) |
| **クリーンアップ** | Effectのreturnで行う後片付け。忘れるとリーク | [④](04-hooks.md) |
| **依存配列** | Effectを再実行する条件。**プリミティブ値を入れる** | [④](04-hooks.md) |
| **`useRef`** | 再レンダリングを起こさない箱。DOM参照・タイマーID | [④](04-hooks.md) |
| **`useContext`** | 離れた場所へ値を配る。滅多に変わらない値向け | [④](04-hooks.md) |
| **`useReducer`** | 複雑な状態遷移をまとめる。ありえない状態を防ぐ | [④](04-hooks.md) |
| **カスタムフック** | 自作のフック。**状態は共有されない**（各所で独立） | [④](04-hooks.md) |
| **`useTransition`** | 重い更新を低優先度にして入力のカクつきを防ぐ | [⑤](05-rendering-mechanism.md) |
| **`useEffectEvent`** | Effect内で最新値を使う（19.2） | [⑦](07-react19-features.md) |

### レンダリング

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **レンダリング** | コンポーネント関数を実行してJSXを得ること（**画面変更ではない**） | [⑤](05-rendering-mechanism.md) |
| **コミット** | 差分を実際のDOMに反映する段階。ここで画面が変わる | [⑤](05-rendering-mechanism.md) |
| **再レンダリング** | state・props・Contextの変化で関数が再実行されること | [⑤](05-rendering-mechanism.md) |
| **`key`** | Reactが要素を識別する目印。**変えると状態がリセットされる** | [②](02-jsx-components-props.md)・[⑤](05-rendering-mechanism.md) |
| **メモ化** | 前回の計算結果を再利用すること | [⑤](05-rendering-mechanism.md) |
| **React Compiler** | 自動でメモ化を挿入するビルドツール。1.0で安定版 | [⑤](05-rendering-mechanism.md) |
| **StrictMode** | 開発時にEffectを2回実行し、不備を検出するモード | [④](04-hooks.md) |
| **Hydration** | サーバー製HTMLにブラウザでJSを結びつける処理 | [⑦](07-react19-features.md) |

### 状態管理

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **サーバー状態** | DB/APIから来るデータ。**グローバル状態にしない** | [⑥](06-state-design.md) |
| **URL状態** | 検索条件・ページ番号など。URLに置くべき状態 | [⑥](06-state-design.md) |
| **派生状態** | 他のstateから計算できる状態。**stateにしない** | [③](03-state-events.md)・[⑥](06-state-design.md) |
| **正規化** | データの重複を排除しIDで参照する設計 | [⑥](06-state-design.md) |
| **判別可能なユニオン型** | `status` で分岐し、ありえない状態を型で防ぐ手法 | [⑥](06-state-design.md) |
| **propsバケツリレー** | 使わない中間層をpropsが通り抜ける状態 | [⑧](08-practice-patterns.md) |

### React 19

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **RSC / Server Components** | サーバーで実行されるコンポーネント。DB直アクセス可 | [⑦](07-react19-features.md) |
| **`'use client'`** | Client Componentの境界宣言 | [⑦](07-react19-features.md) |
| **Actions** | 非同期処理と状態管理を統合した仕組み | [⑦](07-react19-features.md) |
| **`useActionState`** | Actionの結果・pending状態を管理 | [⑦](07-react19-features.md) |
| **`useFormStatus`** | 送信状態を取得。**`<form>` の子孫で呼ぶ** | [⑦](07-react19-features.md) |
| **`useOptimistic`** | 楽観的更新。応答前に画面を更新 | [⑦](07-react19-features.md) |
| **`use()`** | Promise/Contextを読むAPI。**条件分岐内でも呼べる** | [⑦](07-react19-features.md) |
| **`<Activity>`** | 状態を保持したままUIを非表示・一時停止（19.2） | [⑦](07-react19-features.md) |

### 設計・その他

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **Error Boundary** | エラーで画面が真っ白になるのを防ぐ境界 | [⑧](08-practice-patterns.md) |
| **Suspense** | 読み込み中の表示を宣言的に扱う仕組み | [⑦](07-react19-features.md) |
| **Compound Components** | `<Tabs.Trigger>` のように関連部品をまとめる設計 | [⑧](08-practice-patterns.md) |
| **a11y** | アクセシビリティ（accessibility の略記） | [⑧](08-practice-patterns.md) |
| **SPA** | Single Page Application。1つのHTMLで画面遷移する方式 | [①](01-what-is-react.md) |

---

## 2. 逆引き表 — 困った時どの章？

| やりたいこと・困りごと | 見る章 |
| --- | --- |
| Reactが何なのか知りたい | [① Reactとは](01-what-is-react.md) |
| 環境構築したい | [① 環境構築](01-what-is-react.md#5-環境構築--何から始めるか) |
| Vue/Svelteと比較したい | [① 他ライブラリ比較](01-what-is-react.md#7-他のuiライブラリとの比較) |
| JSXの書き方を知りたい | [② JSX](02-jsx-components-props.md#1-jsx--htmlに見えるがjavascript) |
| コンポーネントの分け方に迷う | [② コンポーネント](02-jsx-components-props.md#2-コンポーネント--画面の部品) |
| 親から子にデータを渡したい | [② props](02-jsx-components-props.md#3-props--親から子へデータを渡す) |
| 条件で表示を切り替えたい | [② 条件分岐](02-jsx-components-props.md#4-条件分岐--出し分ける) |
| リストを表示したい | [② リスト表示とkey](02-jsx-components-props.md#5-リスト表示と-key) |
| ボタンで値を変えたい | [③ state](03-state-events.md#1-state-とは--コンポーネントが持つ記憶) |
| **画面が更新されない** | [③ イミュータブル](03-state-events.md#ルール3stateは書き換えず新しい値を作るイミュータブル) |
| フォームを作りたい | [③ フォーム](03-state-events.md#4-フォームの扱い) |
| 子から親のデータを変えたい | [③ リフトアップ](03-state-events.md#5-stateをどこに置くか--リフトアップ) |
| stateにすべきか迷う | [③ stateにすべきでないもの](03-state-events.md#-stateにすべきでないもの) |
| useEffectの使い方を知りたい | [④ useEffect](04-hooks.md#3-useeffect--最も誤用されるフック) |
| **useEffectが無限ループする** | [⑤ 無限ループ](05-rendering-mechanism.md#5-無限ループの原因と対処) |
| DOMを直接触りたい | [④ useRef](04-hooks.md#4-useref--再レンダリングを起こさない箱) |
| propsのバケツリレーを解消したい | [④ useContext](04-hooks.md#5-usecontext--propsバケツリレーの解消) |
| ロジックを再利用したい | [④ カスタムフック](04-hooks.md#7-カスタムフック--ロジックの再利用) |
| クラスコンポーネントを読みたい | [④ 対応表](04-hooks.md#8-クラスコンポーネントとの対応表保守用) |
| 再レンダリングの仕組みを知りたい | [⑤ レンダリングの3段階](05-rendering-mechanism.md#1-レンダリングの3段階) |
| **表示が古いまま更新されない** | [⑤ 更新されない原因](05-rendering-mechanism.md#4-更新されないときの原因) |
| 画面が重い | [⑤ 最適化の順序](05-rendering-mechanism.md#最適化の正しい順序) |
| useMemoを使うべきか | [⑤ React Compiler](05-rendering-mechanism.md#react-compiler-の登場で状況が変わった) |
| 入力がカクつく | [⑤ useTransition](05-rendering-mechanism.md#8-重い更新を後回しにするusetransition) |
| 状態管理ライブラリを選びたい | [⑥ ライブラリ比較](06-state-design.md#5-状態管理ライブラリの比較) |
| 状態の置き場所に迷う | [⑥ 判断フロー](06-state-design.md#判断フロー) |
| API取得データの扱いに迷う | [⑥ 状態の分類](06-state-design.md#1-まず状態を分類する) |
| 検索条件を保持したい | [⑥ URL状態](06-state-design.md#2-url状態を活用する見落とされがち) |
| Server Componentsを知りたい | [⑦ RSC](07-react19-features.md#2-server-componentsrsc--最大の変化) |
| フォーム送信を楽に書きたい | [⑦ Actions](07-react19-features.md#3-actions--非同期処理の定型文をなくす) |
| React 18から移行したい | [⑦ 移行](07-react19-features.md#7-react-18-からの移行) |
| コンポーネント設計を学びたい | [⑧ 設計パターン](08-practice-patterns.md#1-コンポーネント設計パターン) |
| コードが汚くなってきた | [⑧ アンチパターン](08-practice-patterns.md#2-アンチパターン集) |
| エラーで画面が真っ白になる | [⑧ Error Boundary](08-practice-patterns.md#3-エラーハンドリング) |
| アクセシビリティを改善したい | [⑧ a11y](08-practice-patterns.md#4-アクセシビリティa11y) |
| テストを書きたい | [⑧ テスト](08-practice-patterns.md#5-テスト) |
| **Next.jsとの関係を知りたい** | [関係ガイド](../js-stack-relations.md) |
| **Node.jsとの関係を知りたい** | [関係ガイド](../js-stack-relations.md) |

---

## 3. 頻出エラー早見表

| エラー / 症状 | 原因 | 対処 |
| --- | --- | --- |
| 何も表示されない | コンポーネント名が小文字 | 大文字で始める |
| `Objects are not valid as a React child` | オブジェクトを直接表示 | `{obj.name}` とする |
| `Each child should have a unique "key"` | `map` に `key` がない | 一意なIDを渡す |
| `Invalid hook call` | 条件・ループ内でフック | トップレベルで呼ぶ |
| `Too many re-renders` | レンダリング中にsetState | `onClick={fn()}` の `()` を外す |
| `Cannot read property of undefined` | データ取得前のアクセス | `?.` かローディング分岐 |
| `Maximum update depth exceeded` | Effectの無限ループ | 依存配列を見直す |
| 画面が更新されない | 配列/オブジェクトの直接変更 | 新しい値を作る |
| リストに `0` が出る | `&&` の左辺が数値 | `length > 0 &&` にする |
| チェック状態がズレる | `key={index}` | データのIDを使う |
| Effectが2回実行される | StrictMode（開発時のみ） | クリーンアップを書く |
| `pending` が常にfalse | `useFormStatus` を同一階層で呼んだ | 子コンポーネントに分ける |
| 入力できない | `value` のみで `onChange` なし | `onChange` を追加 |

---

## 4. チートシート

### 配列のイミュータブル操作

```ts
[...arr, x]                                    // 末尾に追加
[x, ...arr]                                    // 先頭に追加
arr.filter((item) => item.id !== id)           // 削除
arr.map((item) => item.id === id ? { ...item, done: true } : item)  // 更新
[...arr].sort((a, b) => a.n - b.n)             // 並び替え（コピーしてから）
[...arr].reverse()                             // 反転（コピーしてから）
```

### オブジェクトの更新

```ts
{ ...obj, key: value }                              // 浅い
{ ...obj, nested: { ...obj.nested, key: value } }   // 深い
```

### よく使うフックの形

```tsx
const [x, setX] = useState(0)
setX((prev) => prev + 1)                       // 前の値を使うとき

useEffect(() => {
  const id = setInterval(tick, 1000)
  return () => clearInterval(id)               // クリーンアップ
}, [deps])

const ref = useRef<HTMLInputElement>(null)
ref.current?.focus()

const value = useContext(MyContext)
```

### コマンド

```bash
npm create vite@latest my-app -- --template react-ts   # 新規作成
npm run dev                                            # 開発サーバー
npm run build                                          # 本番ビルド
```

---

## 5. バージョン別の注意点

| バージョン | 変更 | 影響 |
| --- | --- | --- |
| **16.8**（2019） | フック導入 | クラス → 関数コンポーネントへ |
| **18**（2022） | 並行レンダリング・`createRoot` | StrictModeで2回実行に |
| **19**（2024） | Server Components・Actions安定版 | `propTypes`・文字列ref削除 |
| **19** | `forwardRef` 不要・`.Provider` 省略可 | 書き方が簡潔に |
| **19.2**（2025） | `<Activity>`・`useEffectEvent` | — |
| **Compiler 1.0** | 自動メモ化 | `useMemo`/`useCallback` が原則不要に |

---

## 6. 関連シリーズ

- 📖 [JavaScript・Node.js・React・Next.js の関係](../js-stack-relations.md) ← 全体像
- 🟢 [Node.js 完全ガイド](../nodejs/README.md) ← 実行環境・サーバー側
- ⚫ [Next.js 完全ガイド](../nextjs/README.md) ← Reactでサービスを作る

---

[← 総合インデックスに戻る](README.md)
