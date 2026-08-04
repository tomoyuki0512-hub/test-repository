---
title: ⑦ スタイリングとUI
---

# ⑦ スタイリングとUI — Tailwind・CSS Modules・shadcn/ui

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑥ Server Actionsとフォーム](06-server-actions-forms.md) ｜ 次 → [⑧ 認証とデータベース](08-auth-database.md)

Next.js は特定のCSS手法を強制しません。この章では**選択肢の比較**と、現在の主流である **Tailwind CSS ＋ shadcn/ui** の実務的な組み方を扱います。

---

## 1. 選択肢の比較

| 手法 | 概要 | RSC対応 | 現在の位置づけ |
| --- | --- | --- | --- |
| **Tailwind CSS** | ユーティリティクラスをHTMLに直接書く | ✅ | **事実上の標準**。新規はまずこれ |
| **CSS Modules** | `.module.css` でスコープ付きCSS | ✅ | 標準機能。Tailwindが合わない場合の堅実な選択 |
| **Vanilla Extract** | TypeScriptでCSSを書き、ビルド時に静的化 | ✅ | 型安全重視のチーム向け |
| **CSS-in-JS**（styled-components / Emotion） | JSでスタイルを定義 | ⚠️ | **Server Componentで使えない**。新規採用は非推奨 |
| **Panda CSS** | ゼロランタイムCSS-in-JS | ✅ | CSS-in-JSの書き味を保ちたい場合 |

> 🚨 **CSS-in-JS の注意**：styled-components / Emotion は実行時にJSでスタイルを生成するため、**Server Componentで使えません**。使うと配下全体が `'use client'` になり、[④](04-server-client-components.md) で説明した利点が失われます。既存プロジェクトの移行では最初の障害になりやすい部分です。

**迷ったら Tailwind CSS** で問題ありません。以降はこれを前提に説明します。

---

## 2. Tailwind CSS の基本

`create-next-app` でYesを選べば設定済みです。手動導入の場合：

```bash
npm install tailwindcss @tailwindcss/postcss postcss
```

```css
/* app/globals.css — v4では1行のimportだけ */
@import "tailwindcss";
```

> ⚠️ **Tailwind v4 の変更点**：v3までの `tailwind.config.js` と `@tailwind base;` の3行は不要になりました。設定はCSSファイル内で `@theme` を使って書きます。ネットのv3向け記事をそのまま適用すると動きません。

### 書き方

```tsx
<div className="flex items-center gap-4 rounded-lg bg-white p-6 shadow-sm">
  <img className="h-12 w-12 rounded-full" src={user.avatar} alt="" />
  <div>
    <p className="font-bold text-gray-900">{user.name}</p>
    <p className="text-sm text-gray-500">{user.email}</p>
  </div>
</div>
```

**「クラス名を考えなくていい」「使っていないCSSが消える」「ファイルを行き来しなくていい」**のが利点です。「HTMLが汚くなる」という批判はありますが、コンポーネント化すれば繰り返しは1箇所に収まります。

### デザイントークンを定義する

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  --color-brand-50:  oklch(0.97 0.02 250);
  --color-brand-500: oklch(0.62 0.19 250);
  --color-brand-900: oklch(0.35 0.12 250);
  --font-sans: var(--font-inter), sans-serif;
  --radius-card: 0.75rem;
}
```

これで `bg-brand-500` `rounded-card` が使えるようになります。**色や余白を直値で散らかさず、トークンとして定義する**のがチーム開発では重要です。

### ダークモード

```tsx
<div className="bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-100">
```

システム設定に追従するだけなら上記で十分です。手動切り替えを付けるなら `next-themes` が定番です。

```tsx
// app/layout.tsx
import { ThemeProvider } from 'next-themes'

<html lang="ja" suppressHydrationWarning>   {/* ← これが必要 */}
  <body>
    <ThemeProvider attribute="class">{children}</ThemeProvider>
  </body>
</html>
```

> ⚠️ `suppressHydrationWarning` が必要なのは、テーマ適用がブラウザ側で行われ、サーバーのHTMLと一瞬食い違うためです（→ [④のHydrationエラー](04-server-client-components.md#7-よくあるエラーと対処)）。

### 条件付きクラスは `cn()` でまとめる

クラス名を文字列結合すると衝突（`p-2` と `p-4` が両方残る等）が起きます。定番のヘルパーを用意します。

```ts
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

```tsx
<button className={cn(
  'rounded px-4 py-2',
  variant === 'primary' && 'bg-brand-500 text-white',
  disabled && 'opacity-50 pointer-events-none',
  className,               // 呼び出し元からの上書きを許す
)} />
```

---

## 3. CSS Modules（Tailwindを使わない場合）

Next.js に標準で入っており、追加設定は不要です。

```css
/* components/Card.module.css */
.card {
  padding: 1.5rem;
  border-radius: 0.5rem;
  background: white;
}
```

```tsx
import styles from './Card.module.css'

export function Card() {
  return <div className={styles.card}>...</div>
}
```

クラス名は自動でユニーク化されるため、**グローバルな衝突が起きません**。「CSSをちゃんと書きたい」「デザイナーがCSSを触る」チームには今でも良い選択です。

---

## 4. UIコンポーネントライブラリ

### 比較

| ライブラリ | 方式 | 特徴 |
| --- | --- | --- |
| **shadcn/ui** | **コードをコピーして自分の物にする** | 最も人気。カスタマイズ自由。Tailwind＋Radix UI |
| **Radix UI** | ヘッドレス（機能のみ、見た目なし） | shadcn/uiの土台。アクセシビリティが堅牢 |
| **Base UI** | ヘッドレス | Radixチーム由来の後継系 |
| **MUI** | 完成品コンポーネント | 業務システム向け。デザイン変更は重い |
| **Mantine** | 完成品コンポーネント | 機能が豊富で開発が速い |
| **Chakra UI** | 完成品コンポーネント | 書き味が良い。RSC対応に注意 |

### shadcn/ui が主流な理由

**npmパッケージではなく、ソースコードを自分のリポジトリにコピーする**という発想です。

```bash
npx shadcn@latest init
npx shadcn@latest add button dialog form
```

```
components/ui/
├── button.tsx     ← 自分のコードとして追加される
├── dialog.tsx
└── form.tsx
```

| 利点 | 欠点 |
| --- | --- |
| 中身を自由に書き換えられる | 更新は自分で取り込む必要がある |
| ライブラリのバージョン地獄がない | コンポーネント数が増えると管理が必要 |
| Tailwindのトークンがそのまま効く | Tailwind前提 |

「ライブラリの仕様に合わせてデザインを妥協する」ことがなくなるのが決定的な利点です。

### 使用例

```tsx
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogTrigger } from '@/components/ui/dialog'

<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">開く</Button>
  </DialogTrigger>
  <DialogContent>本文</DialogContent>
</Dialog>
```

---

## 5. フォントと画像（表示速度に直結）

### フォント

```tsx
// app/layout.tsx
import { Inter, Noto_Sans_JP } from 'next/font/google'

const notoSansJP = Noto_Sans_JP({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-noto-sans-jp',
})

export default function RootLayout({ children }) {
  return (
    <html lang="ja" className={notoSansJP.variable}>
      <body className="font-sans">{children}</body>
    </html>
  )
}
```

`next/font` を使うと**ビルド時にフォントを自分のサーバーへ取り込み**、外部リクエストが消えます。さらにレイアウトシフト（CLS）を防ぐサイズ調整も自動で行われます。

> 💡 日本語フォントはファイルサイズが大きい（数MB）ため、**サブセット化**や、見出しだけWebフォント・本文はシステムフォント、といった割り切りも検討してください。詳細は [⑩ パフォーマンス](10-performance-seo.md)。

### 画像

```tsx
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="サービスの説明"
  width={1200}
  height={630}
  priority          // ファーストビューの画像には付ける
/>
```

`next/image` は自動で WebP/AVIF 変換・サイズ別配信・遅延読み込みを行います。詳しくは [⑩](10-performance-seo.md) で扱います。

---

## 6. UI実装のよくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| Tailwindのクラスが効かない | v3の設定を書いている | v4は `@import "tailwindcss"` のみ |
| 動的なクラス名が効く／効かない | `` `text-${color}-500` `` は検出されない | クラス名は**完全な文字列**で書く |
| ダークモードでチラつく | Hydration前に旧テーマが見える | `next-themes` ＋ `suppressHydrationWarning` |
| UIライブラリでRSCエラー | ライブラリがクライアント専用 | ラッパーに `'use client'` を付ける |
| スタイルが上書きできない | クラスの衝突 | `cn()`（tailwind-merge）を使う |

### 動的クラス名の正しい書き方

```tsx
// ❌ ビルド時に検出されず、CSSが生成されない
<div className={`text-${color}-500`} />

// ✅ 完全なクラス名をマップで持つ
const colorMap = {
  red: 'text-red-500',
  blue: 'text-blue-500',
} as const
<div className={colorMap[color]} />
```

Tailwind は**ソースコードを文字列として走査**してクラスを収集するため、実行時に組み立てた名前は見つけられません。

---

## 7. この章のまとめ

- **迷ったら Tailwind CSS v4**。設定は `@import "tailwindcss"` の1行、トークンは `@theme`
- **CSS-in-JS（styled-components / Emotion）は Server Component で使えない**。新規採用は避ける
- コンポーネントは **shadcn/ui**（コードを自分の物にする方式）が現在の主流
- `cn()` = `clsx` + `tailwind-merge` を最初に用意しておくと後がラク
- **動的にクラス名を組み立てない**。完全な文字列で書く
- フォントは `next/font`、画像は `next/image`。どちらも表示速度に直結する

---

次の章 → [⑧ 認証とデータベース](08-auth-database.md)
