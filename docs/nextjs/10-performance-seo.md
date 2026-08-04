---
title: ⑩ パフォーマンス最適化とSEO
---

# ⑩ パフォーマンス最適化とSEO

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑨ Route HandlersとAPI連携](09-route-handlers-api.md) ｜ 次 → [⑪ テストと品質管理](11-testing-quality.md)

Next.js を選ぶ最大の理由が「速さ」と「SEO」です。しかし**書き方を間違えると素のReactより遅くなります**。この章では計測方法と具体的な改善手段を扱います。

---

## 1. 何を測るか — Core Web Vitals

Googleが検索順位の要素として使う3指標です。

| 指標 | 意味 | 良い | 要改善 | 主な原因 |
| --- | --- | --- | --- | --- |
| **LCP** | 最大要素の表示時間 | 2.5秒以下 | 4秒超 | 大きい画像・サーバー応答の遅さ |
| **INP** | 操作への反応速度 | 200ms以下 | 500ms超 | JSが重い・メインスレッド占有 |
| **CLS** | レイアウトのズレ | 0.1以下 | 0.25超 | 画像のサイズ未指定・後から入る広告 |

### 計測手段

| ツール | 用途 |
| --- | --- |
| Chrome DevTools の Lighthouse | 手元で手軽に。**必ず本番ビルドで測る** |
| PageSpeed Insights | 実ユーザーデータ（CrUX）も見られる |
| `@next/bundle-analyzer` | JSバンドルの内訳を可視化 |
| Vercel Speed Insights | 本番の実測値を継続監視 |

> ⚠️ **開発サーバー（`npm run dev`）で測っても意味がありません。** 最適化が効いていない状態なので、必ず `npm run build && npm run start` で測ってください。

---

## 2. 画像の最適化 — LCP改善の最大要因

```tsx
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="サービス紹介"
  width={1200}
  height={630}
  priority                       // ★ファーストビューの画像には必須
  sizes="(max-width: 768px) 100vw, 1200px"
/>
```

`next/image` が自動でやってくれること：

- WebP / AVIF への変換
- デバイス幅ごとのサイズ生成と出し分け
- 遅延読み込み（画面外の画像は読まない）
- 幅・高さの予約による**CLS防止**

### 押さえるべきポイント

| ポイント | 理由 |
| --- | --- |
| **ファーストビューの画像に `priority`** | 遅延読み込みを止めて最優先で読む。**LCPに直結** |
| `sizes` を正しく指定 | 不適切だと巨大画像がスマホに配信される |
| `fill` 使用時は親に `position: relative` | 崩れる原因の定番 |
| 外部画像は `remotePatterns` に登録 | 未登録だとエラーになる |
| SVGアイコンは `next/image` を使わない | そのままimportするかインライン化 |

```ts
// next.config.ts
images: {
  remotePatterns: [{ protocol: 'https', hostname: 'cdn.example.com' }],
  formats: ['image/avif', 'image/webp'],
}
```

> 💡 **`priority` の付けすぎは逆効果**です。全部に付けると優先度の意味がなくなります。**ファーストビューに見える1〜2枚だけ**にしてください。

---

## 3. フォントの最適化

```tsx
import { Noto_Sans_JP } from 'next/font/google'

const notoSansJP = Noto_Sans_JP({
  subsets: ['latin'],
  display: 'swap',        // 読み込み中も代替フォントで表示（FOIT回避）
  preload: true,
  variable: '--font-noto',
})
```

`next/font` は**ビルド時にフォントを自分のドメインへ取り込む**ため、Google Fontsへの外部リクエストが消えます。プライバシー面（GDPR）でも有利です。

> ⚠️ **日本語フォントは重い**（Noto Sans JP は全ウェイトで数MB）。次の割り切りを検討してください。
> - 使うウェイトを2つ程度に絞る（`weight: ['400', '700']`）
> - 見出しだけWebフォント、本文はシステムフォント
> - `font-family: system-ui, sans-serif` で十分な場合も多い

---

## 4. JavaScriptを減らす

**最も効くのは [④](04-server-client-components.md) の原則です。** `'use client'` の範囲を狭めることが、どんな小手先の最適化より効果があります。

### バンドルを見る

```bash
npm install -D @next/bundle-analyzer
ANALYZE=true npm run build
```

```ts
// next.config.ts
import bundleAnalyzer from '@next/bundle-analyzer'
const withBundleAnalyzer = bundleAnalyzer({ enabled: process.env.ANALYZE === 'true' })
export default withBundleAnalyzer(nextConfig)
```

### 重いライブラリは動的import

```tsx
import dynamic from 'next/dynamic'

// グラフライブラリ・エディタ・地図など重いものは分離
const Chart = dynamic(() => import('@/components/Chart'), {
  loading: () => <ChartSkeleton />,
})

// ブラウザ専用ライブラリはSSRを切る
const Map = dynamic(() => import('@/components/Map'), { ssr: false })
```

### よくある無駄

| 問題 | 対処 |
| --- | --- |
| `moment.js`（重い） | `date-fns` / `dayjs` / 標準の `Intl` に置き換え |
| lodash全体をimport | `import debounce from 'lodash/debounce'` のように個別に |
| アイコンライブラリ全体 | 使うアイコンだけ個別import |
| 巨大なUIライブラリ | 使う部分だけ／shadcn/uiに置き換え |

### サードパーティスクリプト

```tsx
import Script from 'next/script'

<Script src="https://example.com/analytics.js" strategy="lazyOnload" />
```

| strategy | タイミング | 用途 |
| --- | --- | --- |
| `beforeInteractive` | ハイドレーション前 | 同意管理など必須のもの |
| `afterInteractive`（既定） | ハイドレーション後 | タグマネージャ |
| `lazyOnload` | アイドル時 | チャット・アナリティクス |

---

## 5. SEO — メタデータ

### 静的なメタデータ

```tsx
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),   // 相対URL解決に必要
  title: {
    default: 'サービス名',
    template: '%s | サービス名',      // 各ページのtitleに自動で付く
  },
  description: 'サービスの説明を120文字程度で',
  openGraph: {
    type: 'website',
    locale: 'ja_JP',
    siteName: 'サービス名',
  },
  twitter: { card: 'summary_large_image' },
  robots: { index: true, follow: true },
}
```

### 動的なメタデータ

```tsx
// app/posts/[id]/page.tsx
export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  const { id } = await params
  const post = await getPost(id)
  if (!post) return { title: '記事が見つかりません' }

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      images: [`/api/og?title=${encodeURIComponent(post.title)}`],  // → ⑨章
      publishedTime: post.createdAt.toISOString(),
    },
    alternates: { canonical: `/posts/${id}` },   // 重複コンテンツ対策
  }
}
```

> 💡 `generateMetadata` と `page` が同じデータを取る場合、React の `cache()` でラップすれば**DBアクセスは1回で済みます**（→ [⑤](05-data-fetching-caching.md#同じデータを複数箇所で使う)）。

---

## 6. sitemap・robots・構造化データ

### sitemap.xml

```ts
// app/sitemap.ts
import type { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await db.post.findMany({ where: { published: true } })

  return [
    { url: 'https://example.com', changeFrequency: 'daily', priority: 1 },
    ...posts.map((p) => ({
      url: `https://example.com/posts/${p.id}`,
      lastModified: p.updatedAt,
      priority: 0.8,
    })),
  ]
}
```

### robots.txt

```ts
// app/robots.ts
import type { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: '*', allow: '/', disallow: ['/admin/', '/api/'] },
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```

### 構造化データ（JSON-LD）

検索結果のリッチリザルト（星評価・パンくず等）に必要です。

```tsx
export default async function PostPage({ params }) {
  const post = await getPost((await params).id)
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    datePublished: post.createdAt.toISOString(),
    author: { '@type': 'Person', name: post.author.name },
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>...</article>
    </>
  )
}
```

---

## 7. SEOの基本チェックリスト

- [ ] 各ページに**固有の** `title` と `description` がある
- [ ] `<html lang="ja">` が設定されている
- [ ] 見出しが `h1` → `h2` → `h3` と正しい階層になっている（`h1` はページに1つ）
- [ ] すべての画像に意味のある `alt` がある
- [ ] `canonical` URLを指定している（パラメータ違いの重複対策）
- [ ] `sitemap.xml` / `robots.txt` を出している
- [ ] 内部リンクは `<a>` ではなく `<Link>`
- [ ] 404は正しく404ステータスを返している（`notFound()` を使う）
- [ ] OG画像が設定され、SNSシェア時に表示される
- [ ] Google Search Console に登録し、インデックス状況を確認している

---

## 8. パフォーマンス改善の優先順位

効果が大きい順です。上から順に潰してください。

```
1. 'use client' の範囲を狭める            ← 最も効く（→ ④章）
2. 画像を next/image にし、priority を適切に
3. データ取得を Promise.all で並列化      （→ ⑤章）
4. 遅い部分を Suspense で囲む（PPR）      （→ ⑤章）
5. 'use cache' で繰り返し取得を減らす      （→ ⑤章）
6. 重いライブラリを動的import・置き換え
7. フォントのウェイトを絞る
8. サードパーティスクリプトを lazyOnload に
```

> 🔑 **計測してから直す**のが鉄則です。「速そう」という直感で最適化すると、効果のない場所に時間を使うことになります。Lighthouse と bundle-analyzer で**どこが重いか特定してから**着手してください。

---

## 9. この章のまとめ

- 指標は **LCP / INP / CLS**。**本番ビルドで計測**する（devサーバーの数値は無意味）
- 画像は `next/image` ＋ **ファーストビューに `priority`**。CLS防止にもなる
- フォントは `next/font`。**日本語フォントは重いのでウェイトを絞る**
- JS削減の本命は **`'use client'` の範囲を狭めること**
- メタデータは `metadata` / `generateMetadata`、`sitemap.ts` / `robots.ts` も標準機能
- 構造化データ（JSON-LD）でリッチリザルトに対応
- **効果の大きい順に直す。直感ではなく計測に基づく**

---

次の章 → [⑪ テストと品質管理](11-testing-quality.md)
