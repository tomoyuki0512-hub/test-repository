---
title: ⑫ デプロイと運用
---

# ⑫ デプロイと運用

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑪ テストと品質管理](11-testing-quality.md) ｜ 次 → [⑬ 実践アーキテクチャ](13-architecture-practice.md)

作ったものを公開し、動かし続けるための章です。**Next.jsはVercel社の製品**なのでVercelが最も相性が良いのですが、他の選択肢とその制約も押さえておきます。

---

## 1. デプロイ先の比較

| 選択肢 | 費用感 | 機能の完全性 | 向いている場面 |
| --- | --- | --- | --- |
| **Vercel** | 個人無料〜、商用は従量 | ◎ 全機能が動く | 迷ったらこれ。個人〜中規模 |
| **Cloudflare Workers** | 安価 | ○ 一部制約あり | エッジ配信・コスト重視 |
| **AWS Amplify / SST** | 従量 | ○ | AWSに寄せたい企業 |
| **Netlify** | 無料枠あり | ○ | 静的寄りのサイト |
| **Docker（自前 / ECS / Cloud Run）** | サーバー費用 | ○ 自分で構築 | 社内要件・データ所在地の制約 |
| **静的出力（`output: 'export'`）** | ほぼ無料 | △ 機能が大幅に制限 | 完全静的サイトのみ |

> ⚠️ **`output: 'export'`（静的出力）の制約**：Server Actions・Route Handlers・ISR・`next/image` の最適化・`proxy.ts` がすべて使えません。「S3に置きたい」という理由で選ぶと、この教材で扱った機能の大半が失われます。**Next.jsを選ぶ意味がなくなるなら、Astro等を検討したほうが適切**です。

---

## 2. Vercelへのデプロイ

```
1. GitHubにpush
2. Vercelでリポジトリを import
3. 環境変数を設定
4. Deploy
```

以降は**push するたびに自動デプロイ**されます。PRごとにプレビューURLが発行されるのが実務では非常に便利です。

### 環境変数の設定

| 環境 | 用途 |
| --- | --- |
| Production | 本番（mainブランチ） |
| Preview | PRごとのプレビュー |
| Development | ローカル（`vercel env pull` で取得） |

```bash
vercel env pull .env.local    # 本番の設定をローカルに同期
```

> 🚨 **プレビュー環境が本番DBを向いていないか必ず確認してください。** PRのプレビューで本番データを壊す事故は実際に起きます。Neonのブランチ機能やSupabaseのブランチを使い、**プレビュー用のDBを分ける**のが安全です。

---

## 3. Dockerでのセルフホスト

### `next.config.ts` の設定

```ts
const nextConfig: NextConfig = {
  output: 'standalone',   // 依存を含む最小構成を出力
}
```

### Dockerfile

```dockerfile
# ---- 依存インストール ----
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# ---- ビルド ----
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# ⚠️ NEXT_PUBLIC_* はビルド時に埋め込まれるのでここで渡す
ARG NEXT_PUBLIC_SITE_URL
ENV NEXT_PUBLIC_SITE_URL=$NEXT_PUBLIC_SITE_URL
RUN npm run build

# ---- 実行 ----
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -S nodejs && adduser -S nextjs -G nodejs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

### セルフホスト時の注意点

| 項目 | 注意 |
| --- | --- |
| **`NEXT_PUBLIC_*`** | **ビルド時に埋め込まれる**。実行時のenvでは変わらない |
| 画像最適化 | `sharp` が必要。または外部ローダーを設定 |
| ISR/キャッシュ | 複数インスタンスならキャッシュハンドラの共有設定（Redis等）が必要 |
| ヘルスチェック | `/api/health` を用意してロードバランサから叩く |
| リバースプロキシ配下 | Server Actionsの `allowedOrigins` 設定が必要な場合がある |

> 🔑 **`NEXT_PUBLIC_*` はビルド時固定**という性質は、Dockerで最も多いハマりどころです。「同じイメージを検証環境と本番で使い回す」ことができません。実行時に切り替えたい値は、**サーバー側で読んでpropsで渡す**設計にしてください。

---

## 4. 環境変数とシークレット管理

| やること | 理由 |
| --- | --- |
| `.env.local` を `.gitignore` に入れる | 初期状態で入っている。消さない |
| `.env.example` をコミットする | 必要なキーの一覧をチームで共有 |
| 起動時にZodで検証する | 設定漏れを即座に検知（→ [⑪](11-testing-quality.md#環境変数の型安全化)） |
| シークレットは環境変数管理サービスに置く | Vercel / AWS Secrets Manager / Doppler など |
| 漏洩したら即ローテーション | Gitの履歴に残ったキーは無効化する |

```bash
# .env.example （コミットする。値はダミー）
DATABASE_URL="postgresql://user:password@localhost:5432/db"
AUTH_SECRET=""
NEXT_PUBLIC_SITE_URL="http://localhost:3000"
```

---

## 5. 監視・ログ・エラー通知

### 何を見るか

| 種類 | 見るもの | ツール例 |
| --- | --- | --- |
| **エラー** | 例外の発生と発生源 | Sentry |
| **パフォーマンス** | Core Web Vitals の実測 | Vercel Speed Insights |
| **アクセス解析** | PV・導線 | Vercel Analytics / GA4 / Plausible |
| **ログ** | サーバーの出力 | Vercel Logs / Datadog / CloudWatch |
| **稼働監視** | 死活・応答時間 | UptimeRobot / Better Stack |

### Sentry の導入

```bash
npx @sentry/wizard@latest -i nextjs
```

Server Component・Server Action・Client のいずれのエラーも捕捉できます。**ソースマップをアップロードする設定**を忘れると、圧縮後のコードでスタックトレースが読めません。

### エラー画面の設計

```tsx
// app/error.tsx
'use client'
export default function Error({ error, reset }) {
  return (
    <div>
      <h2>問題が発生しました</h2>
      {/* 🚨 本番で error.message を出さない（内部情報が漏れる） */}
      <p>時間をおいて再度お試しください。</p>
      {error.digest && <p className="text-xs text-gray-400">Ref: {error.digest}</p>}
      <button onClick={reset}>再試行</button>
    </div>
  )
}
```

`error.digest` はNext.jsが生成するIDで、**サーバーログと突合できます**。ユーザーには詳細を見せず、問い合わせ時にこのIDを伝えてもらう運用が実務的です。

---

## 6. セキュリティヘッダー

```ts
// next.config.ts
const nextConfig: NextConfig = {
  poweredByHeader: false,     // X-Powered-By: Next.js を消す
  async headers() {
    return [{
      source: '/:path*',
      headers: [
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
        {
          key: 'Strict-Transport-Security',
          value: 'max-age=63072000; includeSubDomains; preload',
        },
      ],
    }]
  },
}
```

CSP（Content-Security-Policy）も設定できますが、`nonce` の管理が必要で難易度が上がります。**まずは上記4つを入れ、CSPは余力があれば**という順序で問題ありません。

---

## 7. リリース前チェックリスト

**機能**
- [ ] `npm run build` がローカルとCIの両方で通る
- [ ] 本番ビルド（`npm run start`）で主要な画面を確認した
- [ ] 404 / 500 / エラー画面が正しく出る

**セキュリティ**
- [ ] Server Action / Route Handler に認証・認可がある（→ [⑥](06-server-actions-forms.md)・[⑨](09-route-handlers-api.md)）
- [ ] `NEXT_PUBLIC_` に秘密情報が入っていない
- [ ] セキュリティヘッダーを設定した
- [ ] 依存の脆弱性を確認した（`npm audit`）

**パフォーマンス・SEO**
- [ ] Lighthouse を本番相当で確認した（→ [⑩](10-performance-seo.md)）
- [ ] メタデータ・OG画像・sitemap・robots を設定した
- [ ] Search Console に登録した

**運用**
- [ ] エラー監視（Sentry等）を入れた
- [ ] DBのバックアップ設定を確認した
- [ ] ロールバック手順を把握している
- [ ] 環境変数が本番・プレビューで正しく分かれている

---

## 8. 障害時の初動

```
1. 影響範囲を確認   → 全体か一部か。監視ツールとログを見る
2. 直前の変更を疑う → 直近のデプロイをロールバック（Vercelなら即時可能）
3. 原因を特定       → Sentryのスタックトレース・error.digest で突合
4. 恒久対応         → 修正＋再発防止のテストを追加（→ ⑪章）
5. 記録             → ポストモーテムを残す
```

> 💡 **「まず直す」より「まず戻す」**。原因調査は復旧後で構いません。Vercelは過去のデプロイに即座に戻せるので、この判断がしやすいのが利点です。

---

## 9. この章のまとめ

- **迷ったらVercel**。全機能が動き、PRごとのプレビューが便利
- **`output: 'export'` は機能が大幅に制限される**。選ぶ前に必要な機能を確認
- Dockerなら `output: 'standalone'`。**`NEXT_PUBLIC_*` はビルド時固定**に注意
- 🚨 **プレビュー環境が本番DBを向いていないか確認する**
- エラー監視（Sentry）とパフォーマンス監視を入れる。`error.digest` でログと突合
- セキュリティヘッダーを設定し、`poweredByHeader` を切る
- 障害時は**まず戻す**。原因調査は復旧後

---

次の章 → [⑬ 実践アーキテクチャ](13-architecture-practice.md)
