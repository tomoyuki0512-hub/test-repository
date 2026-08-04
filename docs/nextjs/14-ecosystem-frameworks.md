---
title: ⑭ 併用フレームワーク・ライブラリ総覧
---

# ⑭ 併用フレームワーク・ライブラリ総覧 — Next.jsと一緒に使う技術

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑬ 実践アーキテクチャ](13-architecture-practice.md) ｜ 次 → [用語集](glossary.md)

**「Next.jsと合わせて何を使うのか」への回答がこの章です。** Next.js はルーティング・レンダリング・ビルドを担当しますが、**DB・認証・UI・フォーム・テストなどは自分で選ぶ**必要があります。用途別の定番と選び方をまとめます。

---

## 1. 全体像 — Next.jsが担当する範囲と、しない範囲

```
┌─────────────────────────────────────────────────┐
│              Next.js が担当する                  │
│  ルーティング / レンダリング(SSR・SSG・PPR)      │
│  ビルド(Turbopack) / 画像・フォント最適化        │
│  Server Actions / Route Handlers / メタデータ    │
└─────────────────────────────────────────────────┘
                      ＋
┌─────────────────────────────────────────────────┐
│           自分で選ぶ（この章の内容）             │
│  UI  │ フォーム │ 検証 │ 状態 │ DB/ORM         │
│  認証 │ 決済 │ CMS │ メール │ テスト │ 監視     │
└─────────────────────────────────────────────────┘
```

---

## 2. 用途別・定番ライブラリ一覧

### UI・スタイリング（→ [⑦](07-styling-ui.md)）

| 用途 | 定番 | 対抗馬 | 選び方 |
| --- | --- | --- | --- |
| CSS | **Tailwind CSS v4** | CSS Modules / Panda CSS | 迷ったらTailwind |
| コンポーネント | **shadcn/ui** | Mantine / MUI / Chakra UI | デザイン自由度重視ならshadcn、速さ重視ならMantine |
| ヘッドレス基盤 | **Radix UI** | Base UI / React Aria | shadcn/uiに同梱される |
| アイコン | **lucide-react** | react-icons / Heroicons | shadcn/uiの既定はlucide |
| アニメーション | **Motion**（旧Framer Motion） | CSS Transitions | 凝った動きが要るときだけ |
| ダークモード | **next-themes** | 自前実装 | ほぼ一択 |
| 通知トースト | **sonner** | react-hot-toast | shadcn/uiと統合済み |
| テーブル | **TanStack Table** | AG Grid | 複雑な表なら必須級 |
| グラフ | **Recharts** | Chart.js / visx / Nivo | shadcn/ui chartsがRecharts採用 |

### フォーム・バリデーション（→ [⑥](06-server-actions-forms.md)）

| 用途 | 定番 | 補足 |
| --- | --- | --- |
| スキーマ検証 | **Zod** | 事実上の標準。サーバー・クライアント両方で使い回す |
| 軽量な代替 | Valibot / ArkType | バンドルサイズを詰めたいとき |
| フォーム管理 | **React Hook Form** | 複雑なフォーム（多段・動的項目）で有効 |
| 標準機能 | `useActionState` | **単純なフォームはこれで十分。ライブラリ不要** |
| 連携 | `@hookform/resolvers` | React Hook Form × Zod をつなぐ |

> 💡 **App Routerでの判断**：入力項目が5個程度までなら `useActionState` ＋ Zod でライブラリなしに書けます。**多段フォーム・動的な項目追加・リアルタイム検証**が要るときに React Hook Form を足してください。

### データベース・ORM（→ [⑧](08-auth-database.md)）

| 用途 | 定番 | 対抗馬 |
| --- | --- | --- |
| ORM | **Prisma** | **Drizzle** / Kysely |
| DB（マネージド） | **Neon**（PostgreSQL） | Supabase / PlanetScale / Turso |
| キャッシュ・KV | **Upstash Redis** | Vercel KV |
| ファイル保存 | **Vercel Blob** / **S3** | Cloudflare R2 / UploadThing |
| ベクトル検索（AI用途） | pgvector / Pinecone | Upstash Vector |

### 認証（→ [⑧](08-auth-database.md)）

| ライブラリ | 費用 | 特徴 |
| --- | --- | --- |
| **Auth.js (NextAuth v5)** | 無料 | OSSの定番。自前DBに保存 |
| **Better Auth** | 無料 | TypeScript製。プラグインで機能追加。近年伸びている |
| **Clerk** | 従量（無料枠あり） | UI込みで最速。組織機能・MFAが標準 |
| **Supabase Auth** | 従量（無料枠あり） | Supabase利用時の自然な選択 |
| Auth0 / Cognito | 従量 | 企業要件・既存IdP統合 |

### 状態管理（→ [⑬](13-architecture-practice.md#3-状態管理の判断)）

| 用途 | 定番 | 備考 |
| --- | --- | --- |
| サーバーデータ | **不要**（Server Components） | まずこれを検討 |
| クライアント主導のデータ取得 | **TanStack Query** | 無限スクロール・ポーリング |
| 軽量なグローバル状態 | **Zustand** | 最も手軽 |
| アトミックな状態 | **Jotai** | 細かい粒度で管理したいとき |
| URL状態 | **nuqs** | `searchParams` を型安全に扱う |
| Redux | ⚠️ | App Routerでは出番が大きく減った |

### テスト（→ [⑪](11-testing-quality.md)）

| 用途 | 定番 | 対抗馬 |
| --- | --- | --- |
| ユニット・結合 | **Vitest** | Jest |
| コンポーネント | **Testing Library** | — |
| E2E | **Playwright** | Cypress |
| APIモック | **MSW** | — |
| ビジュアル回帰 | Chromatic / Playwright snapshots | — |
| UIカタログ | **Storybook** | Ladle |

### 品質・開発体験

| 用途 | 定番 | 対抗馬 |
| --- | --- | --- |
| Lint | **ESLint 9** | **Biome**（高速・統合型） |
| フォーマッタ | **Prettier** | Biome |
| コミット前チェック | **husky + lint-staged** | lefthook |
| モノレポ | **Turborepo** | Nx / pnpm workspaces |
| パッケージ管理 | **pnpm** | npm / bun |

### 外部サービス連携

| 用途 | 定番 | 備考 |
| --- | --- | --- |
| 決済 | **Stripe** | Webhookは署名検証と冪等化を必須で（→ [⑨](09-route-handlers-api.md)） |
| メール送信 | **Resend** ＋ **React Email** | JSXでメールを書ける |
| ヘッドレスCMS | **microCMS**（国内）/ Contentful / Sanity | 日本語サポートならmicroCMS |
| MDXコンテンツ | **Contentlayer** / next-mdx-remote | ブログ・ドキュメント |
| 検索 | **Algolia** / Meilisearch / Typesense | — |
| エラー監視 | **Sentry** | （→ [⑫](12-deploy-operations.md)） |
| アクセス解析 | Vercel Analytics / GA4 / Plausible | — |
| レート制限 | **Upstash Ratelimit** | Server Actions保護に |
| AI連携 | **Vercel AI SDK** | ストリーミングUIが簡単に作れる |
| 国際化(i18n) | **next-intl** | ⚠️ Next.js 16では `proxy.ts` 対応版が必要 |

---

## 3. 目的別・推奨スタック

### ① 個人開発・MVP（最速で出す）

```
Next.js 16 (App Router)
├── UI:      Tailwind CSS v4 + shadcn/ui
├── DB:      Supabase または Neon + Drizzle
├── 認証:    Clerk（UIが最初から付いてくる）
├── 検証:    Zod
├── 決済:    Stripe
├── デプロイ: Vercel
└── 監視:    Sentry
```

**狙い**：認証UIを自作しないことで数日短縮できます。無料枠の範囲なら費用もかかりません。

### ② 受託・業務システム（コストと保守性重視）

```
Next.js 16 (App Router)
├── UI:      Tailwind CSS + shadcn/ui（または Mantine）
├── DB:      PostgreSQL (RDS/Cloud SQL) + Prisma
├── 認証:    Auth.js（無料・自前DB）
├── 検証:    Zod
├── フォーム: React Hook Form（項目が多いため）
├── テスト:  Vitest + Playwright
├── デプロイ: Docker（ECS / Cloud Run）
└── 監視:    Sentry + CloudWatch
```

**狙い**：SaaS依存を減らし、データを自社管理下に置きます。顧客のセキュリティ要件に対応しやすい構成です。

### ③ メディア・ブログ（コンテンツ主体）

```
Next.js 16 (App Router)
├── コンテンツ: microCMS / Contentful（または MDX）
├── UI:        Tailwind CSS
├── キャッシュ: 'use cache' + cacheLife('hours')
├── SEO:       generateMetadata + sitemap.ts + JSON-LD
└── デプロイ:   Vercel
```

> ⚠️ **本当にNext.jsが最適か検討してください。** 完全に静的なコンテンツサイトなら **Astro** のほうが軽く速くなります。「会員機能や検索がある」「動的な要素が混ざる」ならNext.jsが有利です。

### ④ 大規模SaaS（チーム開発）

```
Turborepo
├── apps/web    … Next.js 16（顧客向け）
├── apps/admin  … Next.js 16（管理画面）
└── packages/
    ├── ui      … 共通デザインシステム（Tailwind + Radix）
    ├── db      … Prisma / Drizzle スキーマ
    └── config  … ESLint / TS 設定

認証: Auth.js or Clerk（組織・ロール機能）
状態: TanStack Query（クライアント主導部分のみ）
テスト: Vitest + Playwright + Storybook
CI/CD: GitHub Actions + Vercel
監視: Sentry + Datadog
```

---

## 4. 「入れなくていい」ものリスト

App Router では、**従来は必須だったものが不要になっています。** 入れる前に一度立ち止まってください。

| ライブラリ | 従来の役割 | App Routerでは |
| --- | --- | --- |
| **React Router** | ルーティング | ❌ Next.jsが担当 |
| **Redux / Redux Toolkit** | グローバル状態 | ⚠️ 大半はサーバー側かURLに移る |
| **axios** | HTTP通信 | ⚠️ 標準の `fetch` で足りることが多い |
| **TanStack Query**（初期表示用） | データ取得 | ⚠️ Server Componentで取れる |
| **styled-components / Emotion** | スタイリング | ❌ Server Componentで使えない |
| **moment.js** | 日付処理 | ❌ 重い。`date-fns` / `Intl` へ |
| **express** | サーバー | ❌ Route Handlersが担当 |

> 🔑 **判断の順番**：「Next.jsの標準機能でできないか？」→「素のJS/CSSでできないか？」→「それでも必要ならライブラリ」。React時代の常識をそのまま持ち込むと、不要な依存とクライアントJSが増えます。

---

## 5. 選定時のチェックポイント

ライブラリを追加する前に確認してください。

- [ ] **RSC対応しているか**（`'use client'` を強制されないか）
- [ ] メンテナンスが継続しているか（最終リリース・Issue対応の頻度）
- [ ] バンドルサイズは妥当か（[bundlephobia](https://bundlephobia.com) で確認）
- [ ] TypeScriptの型が同梱されているか
- [ ] 日本語を含む多言語・タイムゾーンを正しく扱えるか
- [ ] ライセンスは要件に合うか（商用利用可か）
- [ ] **本当に必要か**（標準機能で代替できないか）

> ⚠️ **RSC対応の確認方法**：READMEに `'use client'` の記載があるか、importしてServer Componentでビルドが通るかを試すのが確実です。UIライブラリの多くは内部でhooksを使うため、クライアント専用のことがあります。

---

## 6. Next.js以外の選択肢（再掲）

念のため、**そもそもNext.jsが最適でない場合**の代替も挙げておきます（詳細は [①](01-what-is-nextjs.md#6-他フレームワークとの比較--nextjsを選ぶべきか)）。

| 状況 | 適した選択 |
| --- | --- |
| ブログ・ドキュメント中心、動きが少ない | **Astro** |
| SEO不要な社内管理画面 | **Vite + React**（SPA） |
| Vueが社内標準 | **Nuxt** |
| 記述量を減らしたい・小規模 | **SvelteKit** |
| Web標準に沿ったシンプルな構成が好み | **React Router v7**（旧Remix） |
| モバイルアプリ向けAPIが主目的 | **NestJS / Hono** ＋ フロントは別 |

---

## 7. この章のまとめ

- Next.js は**ルーティング・レンダリング・ビルドまで**。**DB・認証・UIは自分で選ぶ**
- 現在の定番は **Tailwind v4 ＋ shadcn/ui ＋ Zod ＋ Prisma/Drizzle ＋ Auth.js/Clerk ＋ Vitest/Playwright**
- 用途別の推奨スタックは「個人MVP」「受託」「メディア」「大規模SaaS」で大きく変わる
- **React時代の定番が不要になっている**（React Router / Redux / styled-components / axios）
- 追加前に **RSC対応・保守状況・サイズ・本当に必要か**を確認する
- コンテンツ主体なら **Astro**、SEO不要なら **Vite+React** のほうが適切なこともある

---

シリーズ最終ページ → [用語集・チートシート](glossary.md)
