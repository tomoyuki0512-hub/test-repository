---
title: Next.js 用語集・チートシート
---

# 用語集・チートシート

[← 総合インデックスに戻る](README.md)

全章横断の用語辞典と、「困った時どの章を見ればいいか」の逆引き表です。

---

## 1. 用語集

### レンダリング関連

| 用語 | 読み・正式名 | 意味 |
| --- | --- | --- |
| **CSR** | Client Side Rendering | ブラウザ側でHTMLを組み立てる。素のReactの方式 |
| **SSR** | Server Side Rendering | リクエストのたびにサーバーでHTMLを作る |
| **SSG** | Static Site Generation | ビルド時にHTMLを作り置きする |
| **ISR** | Incremental Static Regeneration | 静的HTMLを一定時間ごとに裏で作り直す |
| **PPR** | Partial Prerendering | 1ページ内で静的部分と動的部分を混ぜる。Next.js 16の既定 |
| **ハイドレーション** | Hydration | サーバー製HTMLにブラウザでJSを結びつけ、操作可能にする処理 |
| **ストリーミング** | Streaming | できた部分から順にHTMLを送る。`Suspense` が境界になる |

### コンポーネント関連

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **RSC** | React Server Components の略。サーバーでのみ動くコンポーネント | [④](04-server-client-components.md) |
| **Server Component** | 既定のコンポーネント。DB直アクセス可、JSは送られない | [④](04-server-client-components.md) |
| **Client Component** | `'use client'` を付けたもの。状態・イベントが使える | [④](04-server-client-components.md) |
| **`'use client'`** | 「ここから先はクライアントでも動く」境界宣言 | [④](04-server-client-components.md) |
| **`'use server'`** | Server Action の宣言。`'use client'` とは逆の意味 | [⑥](06-server-actions-forms.md) |
| **`'use cache'`** | キャッシュ対象にする宣言（Next.js 16） | [⑤](05-data-fetching-caching.md) |
| **シリアライズ可能** | Server→Clientに渡せる値のこと。関数やクラスは不可 | [④](04-server-client-components.md) |

### ルーティング関連

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **App Router** | `app/` を使う現行のルーティング方式 | [③](03-routing.md) |
| **Pages Router** | `pages/` を使う旧方式。新規採用は非推奨 | [②](02-setup-and-structure.md#6-pages-router-との対応表既存プロジェクト保守用) |
| **セグメント** | URLの階層1つ分（`/blog/post` なら `blog` と `post`） | [③](03-routing.md) |
| **動的ルート** | `[id]` のようにURLの一部を変数にしたもの | [③](03-routing.md) |
| **Catch-all** | `[...slug]`。複数階層をまとめて受ける | [③](03-routing.md) |
| **ルートグループ** | `(name)`。URLに出ないフォルダ | [③](03-routing.md) |
| **並列ルート** | `@name`。1URLで複数領域を同時描画 | [③](03-routing.md) |
| **インターセプトルート** | `(..)`。一覧からはモーダル、直URLは通常ページ | [③](03-routing.md) |
| **`proxy.ts`** | 全リクエストの手前で動く処理。旧 `middleware.ts` | [⑨](09-route-handlers-api.md) |

### データ・キャッシュ関連

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **Cache Components** | Next.js 16のキャッシュ機構。`cacheComponents: true` で有効化 | [⑤](05-data-fetching-caching.md) |
| **`cacheLife`** | キャッシュの寿命を指定（`'hours'` 等） | [⑤](05-data-fetching-caching.md) |
| **`cacheTag`** | キャッシュにタグを付ける | [⑤](05-data-fetching-caching.md) |
| **`revalidateTag`** | タグを期限切れにする。古い値が一度返ることがある | [⑤](05-data-fetching-caching.md) |
| **`updateTag`** | タグを即座に無効化。自分の更新をすぐ見せたいとき | [⑤](05-data-fetching-caching.md) |
| **`revalidatePath`** | パス単位でキャッシュを破棄 | [⑤](05-data-fetching-caching.md) |
| **`cache()`** | Reactの機能。**同一リクエスト内**の重複呼び出しを1回に | [⑤](05-data-fetching-caching.md) |
| **stale-while-revalidate** | 古い値を返しつつ裏で更新する方式 | [⑤](05-data-fetching-caching.md) |
| **N+1問題** | 一覧1回＋各件1回ずつクエリが飛ぶ非効率な状態 | [⑤](05-data-fetching-caching.md) |

### フォーム・更新関連

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **Server Actions** | サーバーの関数をクライアントから直接呼べる仕組み | [⑥](06-server-actions-forms.md) |
| **`useActionState`** | Actionの結果（エラー等）を受け取るReactフック | [⑥](06-server-actions-forms.md) |
| **`useFormStatus`** | 送信中かを取得。**`<form>` の子孫で呼ぶ必要がある** | [⑥](06-server-actions-forms.md) |
| **`useOptimistic`** | 楽観的更新。応答を待たず先に画面を更新 | [⑥](06-server-actions-forms.md) |
| **Route Handler** | `route.ts`。外部から叩けるAPIエンドポイント | [⑨](09-route-handlers-api.md) |
| **冪等性** | 同じ操作を何度実行しても結果が変わらない性質。Webhookで必須 | [⑨](09-route-handlers-api.md) |

### 性能・SEO関連

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **LCP** | Largest Contentful Paint。主要要素の表示時間。2.5秒以下が目標 | [⑩](10-performance-seo.md) |
| **INP** | Interaction to Next Paint。操作への反応速度。200ms以下が目標 | [⑩](10-performance-seo.md) |
| **CLS** | Cumulative Layout Shift。表示のズレ。0.1以下が目標 | [⑩](10-performance-seo.md) |
| **Core Web Vitals** | 上記3指標の総称。検索順位の要素 | [⑩](10-performance-seo.md) |
| **JSON-LD** | 構造化データの記述形式。リッチリザルトに必要 | [⑩](10-performance-seo.md) |
| **canonical** | 重複コンテンツの正規URLを示す指定 | [⑩](10-performance-seo.md) |

### その他

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **Turbopack** | Rust製バンドラ。Next.js 16で既定 | [②](02-setup-and-structure.md) |
| **`server-only`** | クライアントからのimportをビルド時に禁止するパッケージ | [⑧](08-auth-database.md) |
| **DAL** | Data Access Layer。データ取得と認可を集約する層 | [⑧](08-auth-database.md)・[⑬](13-architecture-practice.md) |
| **ヘッドレス** | 機能だけ提供し見た目を持たない設計（UIライブラリ・CMS） | [⑦](07-styling-ui.md)・[⑭](14-ecosystem-frameworks.md) |
| **モノレポ** | 複数アプリ・パッケージを1リポジトリで管理する構成 | [⑬](13-architecture-practice.md) |

---

## 2. 逆引き表 — 困った時どの章？

| やりたいこと・困りごと | 見る章 |
| --- | --- |
| Next.jsを使うべきか判断したい | [① 他フレームワーク比較](01-what-is-nextjs.md#6-他フレームワークとの比較--nextjsを選ぶべきか) |
| SSR/SSG/ISRの違いを知りたい | [① レンダリング方式](01-what-is-nextjs.md#3-レンダリング方式--この章の山場) |
| プロジェクトを作りたい | [② 環境構築](02-setup-and-structure.md#2-プロジェクトを作る) |
| 環境変数の扱いを知りたい | [② 環境変数](02-setup-and-structure.md#環境変数envlocal) |
| Pages Routerから移行したい | [② 対応表](02-setup-and-structure.md#6-pages-router-との対応表既存プロジェクト保守用) |
| URLとページの対応を作りたい | [③ ルーティング](03-routing.md) |
| `/posts/123` のようなURLを作りたい | [③ 動的ルート](03-routing.md#3-動的ルートurlの一部を変数にする) |
| ローディング・エラー画面を出したい | [③ 特別なファイル](03-routing.md#2-特別な意味を持つファイル) |
| モーダルで開きたい（URLは共有可能に） | [③ インターセプトルート](03-routing.md#8-応用インターセプトルートintercepting-routes) |
| `useState` でエラーが出る | [④ `'use client'`](04-server-client-components.md#3-use-client--ホールに出す宣言) |
| Hydrationエラーが出る | [④ よくあるエラー](04-server-client-components.md#7-よくあるエラーと対処) |
| Client の中で Server を使いたい | [④ 組み合わせのルール](04-server-client-components.md#5-組み合わせのルール) |
| DBからデータを取りたい | [⑤ データ取得の基本](05-data-fetching-caching.md#1-データ取得の基本--await-するだけ) |
| データが古いまま更新されない | [⑤ cacheTag / updateTag](05-data-fetching-caching.md#5-更新時に消すcachetag-と-revalidatetag--updatetag) |
| ページの一部だけ遅れて表示したい | [⑤ PPRとストリーミング](05-data-fetching-caching.md#6-pprとストリーミング--ページを部分ごとに出す) |
| 表示を速くしたい（キャッシュ） | [⑤ `use cache`](05-data-fetching-caching.md#3-use-cache-の使い方) |
| フォームを作りたい | [⑥ Server Actions](06-server-actions-forms.md) |
| バリデーションエラーを表示したい | [⑥ `useActionState`](06-server-actions-forms.md#3-実務レベルのフォームuseactionstate) |
| 「いいね」を即座に反映したい | [⑥ `useOptimistic`](06-server-actions-forms.md#5-楽観的更新useoptimistic) |
| Server Actionsのセキュリティが不安 | [⑥ セキュリティ](06-server-actions-forms.md#7--セキュリティ--この章で最も重要) |
| CSSをどう書くか決めたい | [⑦ 選択肢の比較](07-styling-ui.md#1-選択肢の比較) |
| ボタンやモーダルを楽に作りたい | [⑦ shadcn/ui](07-styling-ui.md#4-uiコンポーネントライブラリ) |
| ダークモードを付けたい | [⑦ ダークモード](07-styling-ui.md#ダークモード) |
| Tailwindのクラスが効かない | [⑦ つまずき](07-styling-ui.md#6-ui実装のよくあるつまずき) |
| ORMを選びたい | [⑧ Prisma vs Drizzle](08-auth-database.md#prisma-と-drizzle-の選び方) |
| ログイン機能を付けたい | [⑧ 認証](08-auth-database.md#2-認証authentication) |
| 他人のデータを守りたい（認可） | [⑧ 認可の置き場所](08-auth-database.md#3--認可authorizationをどこに置くか) |
| APIエンドポイントを作りたい | [⑨ Route Handlers](09-route-handlers-api.md#1-route-handlersroutets) |
| Webhookを受け取りたい | [⑨ Webhook受信](09-route-handlers-api.md#2-実務でよく書くroute-handler) |
| `middleware.ts` が動かなくなった | [⑨ `proxy.ts`](09-route-handlers-api.md#3-proxyts旧-middlewarets) |
| 表示が遅い | [⑩ 改善の優先順位](10-performance-seo.md#8-パフォーマンス改善の優先順位) |
| 画像を最適化したい | [⑩ 画像](10-performance-seo.md#2-画像の最適化--lcp改善の最大要因) |
| SEO対策をしたい | [⑩ メタデータ](10-performance-seo.md#5-seo--メタデータ) |
| OG画像を動的に作りたい | [⑨ OG画像生成](09-route-handlers-api.md#2-実務でよく書くroute-handler) |
| テストを書きたい | [⑪ テスト戦略](11-testing-quality.md#1-nextjsにおけるテスト戦略) |
| `next lint` が動かない | [⑪ ESLint](11-testing-quality.md#5-eslint-と-prettier) |
| デプロイしたい | [⑫ デプロイ先の比較](12-deploy-operations.md#1-デプロイ先の比較) |
| Dockerで動かしたい | [⑫ セルフホスト](12-deploy-operations.md#3-dockerでのセルフホスト) |
| 本番公開前に確認したい | [⑫ リリース前チェックリスト](12-deploy-operations.md#7-リリース前チェックリスト) |
| ディレクトリ構成に迷っている | [⑬ 規模別構成](13-architecture-practice.md#1-規模別のディレクトリ構成) |
| 状態管理ライブラリを選びたい | [⑬ 状態管理の判断](13-architecture-practice.md#3-状態管理の判断) |
| コードが散らかってきた | [⑬ アンチパターン集](13-architecture-practice.md#4-アンチパターン集) |
| **何のライブラリを使えばいいか** | [⑭ 併用フレームワーク総覧](14-ecosystem-frameworks.md) |
| スタック構成の例が見たい | [⑭ 目的別スタック](14-ecosystem-frameworks.md#3-目的別推奨スタック) |

---

## 3. コマンド・チートシート

```bash
# プロジェクト作成
npx create-next-app@latest my-app

# 開発
npm run dev                    # 開発サーバー
npm run build && npm run start # 本番相当で確認（★重要）

# 品質チェック（Next.js 16では next lint は廃止）
npx eslint .
npx tsc --noEmit

# バンドル解析
ANALYZE=true npm run build

# アップグレード
npx @next/codemod@canary upgrade latest
```

---

## 4. 最頻出エラー早見表

| エラーメッセージ | 原因 | 対処 |
| --- | --- | --- |
| `You're importing a component that needs useState` | Server Componentでhooks使用 | `'use client'` を付ける（→ [④](04-server-client-components.md)） |
| `Functions cannot be passed directly to Client Components` | 関数をpropsで渡した | Server Actionにするか、Client側で定義 |
| `Hydration failed` | サーバーとブラウザで描画結果が違う | `useEffect` 後に描画（→ [④](04-server-client-components.md#7-よくあるエラーと対処)） |
| `window is not defined` | サーバーでブラウザAPIを使用 | `useEffect` 内 or `dynamic(..., { ssr: false })` |
| `params.id is undefined` | 15以降 `params` はPromise | `const { id } = await params` |
| `useRouter is not defined` | `next/router` からimport | `next/navigation` からimport |
| `Too many connections` | Prismaクライアントの多重生成 | `globalForPrisma` パターン（→ [⑧](08-auth-database.md)） |
| `Text content does not match` | Hydration不一致の一種 | 上記Hydration対処と同じ |
| `next lint` が動かない | Next.js 16で削除 | `npx eslint .` を使う |
| `proxy.ts` が動いていない | `middleware.ts` のまま | ファイル名と関数名を変更（→ [⑨](09-route-handlers-api.md)） |

---

## 5. バージョン別の注意点まとめ

| バージョン | 主な変更 | 影響 |
| --- | --- | --- |
| **13** | App Router登場 | `pages/` 前提の記事が使えなくなった |
| **15** | `params`/`searchParams`/`cookies()`/`headers()` が非同期に | `await` が必須になった |
| **15** | React 19対応 | `useActionState` 等が使える |
| **16** | Node.js 20.9以上が必須 | Node 18環境は動かない |
| **16** | Turbopackが既定 | ビルドが高速化。Webpack設定は要見直し |
| **16** | `middleware.ts` → `proxy.ts` | **無言で動かなくなるので要注意** |
| **16** | `next lint` 削除 | CIスクリプトの修正が必要 |
| **16** | Cache Components導入 | `unstable_cache` / `export const revalidate` から移行 |
| **16** | `experimental.ppr` 削除 | Cache Componentsに統合 |

---

[← 総合インデックスに戻る](README.md)
