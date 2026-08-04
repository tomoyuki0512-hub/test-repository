---
title: ② 環境構築とプロジェクト構造
---

# ② 環境構築とプロジェクト構造

[← 総合インデックスに戻る](README.md) ｜ 前 → [① Next.jsとは何か](01-what-is-nextjs.md) ｜ 次 → [③ ルーティング](03-routing.md)

この章では実際に手を動かして、Next.js プロジェクトを立ち上げ、**生成されたファイルが何のためにあるのか**を1つずつ理解します。

---

## 1. 必要なもの

| 項目 | 必要バージョン | 確認コマンド |
| --- | --- | --- |
| Node.js | **20.9 以上**（LTS推奨） | `node -v` |
| パッケージマネージャ | npm / pnpm / yarn / bun のどれか | `npm -v` |
| エディタ | VS Code 推奨 | — |

> ⚠️ **Next.js 16 から Node.js 18 はサポート対象外**です。`node -v` が `v18.x` なら先に更新してください。バージョン管理には `nvm` / `fnm` / `volta` などを使うと、プロジェクトごとに切り替えられて便利です。

**推奨VS Code拡張**

- ESLint / Prettier（コード整形）
- Tailwind CSS IntelliSense（Tailwindを使う場合）
- Error Lens（エラーを行内に表示。RSC関連のエラーは長いので効果的）

---

## 2. プロジェクトを作る

```bash
npx create-next-app@latest my-app
```

対話形式で聞かれるので、迷ったら次のように答えます。

| 質問 | 推奨 | 理由 |
| --- | --- | --- |
| TypeScript? | **Yes** | 現在のエコシステムは実質TS前提 |
| ESLint? | **Yes** | 初期設定を自動で作ってくれる |
| Tailwind CSS? | **Yes**（好みで） | 迷うならYes。あとから外すのは簡単 |
| `src/` directory? | **Yes** | 設定ファイルとコードが混ざらず見通しが良い |
| App Router? | **Yes** | 現行の推奨（→ [①](01-what-is-nextjs.md#5-pages-router-と-app-router)） |
| Turbopack? | **Yes** | 16では既定。開発サーバが大幅に速い |
| import alias? | **No**（既定の `@/*`） | 既定のままで困らない |

作成後、起動します。

```bash
cd my-app
npm run dev
```

`http://localhost:3000` を開いて初期ページが出れば成功です。

### 主なコマンド

| コマンド | 用途 | 備考 |
| --- | --- | --- |
| `npm run dev` | 開発サーバー起動 | ファイル保存で即反映（HMR） |
| `npm run build` | 本番ビルド | **デプロイ前に必ず通す**。型エラーもここで出る |
| `npm run start` | ビルド結果を起動 | 本番と同じ挙動の確認用 |
| `npx next build --debug` | ビルドの詳細出力 | 原因不明のビルド失敗の調査に |

> 💡 **開発中は動くのに本番で壊れる**、はNext.jsで最も多いトラブルです。原因の大半はキャッシュ挙動の違い（→ [⑤](05-data-fetching-caching.md)）。**こまめに `npm run build && npm run start` で確認する**習慣をつけると事故が激減します。

---

## 3. 生成されたファイルの意味

```
my-app/
├── src/
│   └── app/                 ← ここがルーティングの起点。URLと直結する
│       ├── layout.tsx       ← 全ページ共通の外枠（HTML/bodyタグはここ）
│       ├── page.tsx         ← "/" に対応するページ
│       ├── globals.css      ← 全体に効くCSS
│       └── favicon.ico
├── public/                  ← 画像等の静的ファイル。/logo.png のように参照
├── next.config.ts           ← Next.js本体の設定
├── tsconfig.json            ← TypeScriptの設定
├── eslint.config.mjs        ← ESLintの設定（v9のflat config形式）
├── package.json
└── .env.local               ← 環境変数（自分で作る。Gitに入れない）
```

### 特に重要な2つ

**`app/layout.tsx`（ルートレイアウト）** — 全ページを包む外枠です。**`<html>` と `<body>` を書けるのはここだけ**で、必須です。

```tsx
// src/app/layout.tsx
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'My App',
  description: 'Next.jsの学習用アプリ',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  )
}
```

**`app/page.tsx`（ページ）** — そのURLで表示される中身です。

```tsx
// src/app/page.tsx  →  "/" でこれが表示される
export default function Home() {
  return <h1>トップページ</h1>
}
```

> **`layout.tsx` と `page.tsx` の関係**：`layout` が額縁、`page` が絵です。ページを移動しても額縁（レイアウト）は再描画されず、中身だけが差し替わります。

---

## 4. `src/` の中をどう分けるか

`app/` 配下にはURLになるファイルだけを置き、**それ以外は `app/` の外に出す**のが管理しやすい構成です。

```
src/
├── app/                     ← URLになるものだけ
│   ├── (marketing)/         ← ルートグループ（URLに出ない。→ ③章）
│   ├── dashboard/
│   └── layout.tsx
├── components/              ← 再利用するUI部品
│   └── ui/                  ← ボタン等の最小単位（shadcn/uiの置き場所）
├── lib/                     ← 汎用ロジック・DBクライアント・ユーティリティ
├── features/                ← 機能ごとのまとまり（中〜大規模で有効）
│   └── posts/
│       ├── components/
│       ├── actions.ts
│       └── queries.ts
├── hooks/                   ← カスタムフック
└── types/                   ← 型定義
```

> 規模別の使い分けと判断基準は [⑬ 実践アーキテクチャ](13-architecture-practice.md) で詳しく扱います。**最初は `app/` `components/` `lib/` の3つだけ**で始めて、増えてきたら `features/` を導入する、で十分です。

### `@/` エイリアス

`tsconfig.json` に設定されており、相対パスの `../../..` 地獄を避けられます。

```tsx
// ❌ 読みにくい
import { Button } from '../../../components/ui/button'

// ✅ どこからでも同じ書き方
import { Button } from '@/components/ui/button'
```

---

## 5. 設定ファイル

### `next.config.ts`

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Cache Components（use cache）を有効化 → ⑤章
  cacheComponents: true,

  images: {
    // 外部画像を next/image で使うなら許可が必要
    remotePatterns: [
      { protocol: 'https', hostname: 'images.example.com' },
    ],
  },

  // 本番デプロイをDocker等で行う場合の最小構成出力 → ⑫章
  // output: 'standalone',
}

export default nextConfig
```

> ⚠️ **やってはいけない設定**
> ```ts
> typescript: { ignoreBuildErrors: true },   // 型エラーを無視
> eslint:     { ignoreDuringBuilds: true },  // Lintを無視
> ```
> 「ビルドを通すため」に一時的に入れられがちですが、**入れた瞬間に本番の型安全性が消えます**。急ぎで入れる場合も、必ず期限とIssueをセットにしてください。

### 環境変数（`.env.local`）

```bash
# .env.local （Gitにコミットしない）
DATABASE_URL="postgresql://..."          # サーバーでのみ読める
NEXT_PUBLIC_SITE_URL="http://localhost:3000"  # ブラウザにも露出する
```

| 書き方 | どこから読めるか | 使ってよいもの |
| --- | --- | --- |
| `DATABASE_URL` | **サーバーのみ** | APIキー・DB接続情報・シークレット |
| `NEXT_PUBLIC_XXX` | サーバー＋**ブラウザ** | 公開URL・公開キーなど、漏れても困らない値だけ |

> 🚨 **最重要の落とし穴**：`NEXT_PUBLIC_` を付けた値は**ビルド時にJSへ埋め込まれ、誰でも見られます**。APIの秘密鍵に `NEXT_PUBLIC_` を付けてしまう事故は実際に多発しています。「Client Componentで値が `undefined` になるから `NEXT_PUBLIC_` を付けた」は**ほぼ確実に設計ミス**です。その処理はサーバー側（Server Component / Server Action）に移してください。

読み込み順は `.env.local` > `.env.production` / `.env.development` > `.env` です。`.env.local` は `.gitignore` に最初から入っています。

---

## 6. Pages Router との対応表（既存プロジェクト保守用）

古い記事や既存コードを読むときの変換表です。**新規開発では左側は使いません。**

| Pages Router（旧） | App Router（現行） |
| --- | --- |
| `pages/about.tsx` | `app/about/page.tsx` |
| `pages/posts/[id].tsx` | `app/posts/[id]/page.tsx` |
| `pages/_app.tsx` / `_document.tsx` | `app/layout.tsx` |
| `pages/api/hello.ts` | `app/api/hello/route.ts` |
| `getServerSideProps` | Server Componentで直接 `await`（キャッシュしない） |
| `getStaticProps` | Server Component＋`'use cache'` |
| `getStaticPaths` | `generateStaticParams` |
| `next/head` の `<Head>` | `export const metadata` |
| `useRouter()` from `next/router` | `useRouter()` from `next/navigation` |
| `middleware.ts` | **`proxy.ts`**（→ [⑨](09-route-handlers-api.md)） |

> `app/` と `pages/` は**同一プロジェクトに共存できます**。全面書き換えではなく、新規ページから `app/` で作り、既存を順次移していく段階移行が現実的です。

---

## 7. ⚠️ バージョン差分（15 → 16）

| 項目 | Next.js 15 | Next.js 16 |
| --- | --- | --- |
| Node.js 最低要件 | 18.18 以上 | **20.9 以上** |
| バンドラ | Webpack既定（Turbopackは任意） | **Turbopack が dev/build とも既定** |
| `next lint` | あり | **削除**。ESLint/Biomeを直接実行（→ [⑪](11-testing-quality.md)） |
| `middleware.ts` | あり | **`proxy.ts` に改称**（→ [⑨](09-route-handlers-api.md)） |
| キャッシュ | 暗黙のキャッシュが残る | **Cache Components で明示的に**（→ [⑤](05-data-fetching-caching.md)） |
| `experimental.ppr` | 実験的フラグ | 削除。Cache Componentsに統合 |

アップグレードは公式のコードモッドが用意されています。

```bash
npx @next/codemod@canary upgrade latest
```

---

## 8. この章のまとめ

- `npx create-next-app@latest` で作り、迷ったら **TypeScript / ESLint / src / App Router は全部Yes**
- `app/` は**URLになるものだけ**。部品は `components/`、ロジックは `lib/` へ
- `layout.tsx` は額縁、`page.tsx` は絵。`<html>`/`<body>` はルートレイアウトだけ
- **`NEXT_PUBLIC_` はブラウザに露出する**。秘密情報には絶対に付けない
- **`npm run build` をこまめに通す**。開発サーバーだけで確認すると本番で事故る
- `getServerSideProps` / `pages/` が出てくる情報は Pages Router（旧作法）

---

次の章 → [③ ルーティング（App Router）](03-routing.md)
