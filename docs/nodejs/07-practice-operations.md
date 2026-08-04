---
title: ⑦ 実務・運用
---

# ⑦ 実務・運用 — ログ・セキュリティ・パフォーマンス・デプロイ

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑥ サーバーとフレームワーク](06-server-frameworks.md) ｜ 次 → [用語集](glossary.md)

作ったサーバーを **本番で動かし続ける**ための章です。ここが疎かだと、動くものは作れても運用で苦しみます。

---

## 1. ログ — `console.log` を卒業する

### なぜ `console.log` ではダメか

| 問題 | 影響 |
| --- | --- |
| 構造化されていない | ログ検索・集計ができない |
| ログレベルがない | 重要なエラーが埋もれる |
| 同期I/Oになりうる | 大量出力でイベントループを止める |
| コンテキストがない | どのリクエストのログか追えない |

### 構造化ログ（pino）

```ts
import pino from 'pino'

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  // 🚨 秘密情報をマスクする
  redact: ['req.headers.authorization', 'req.headers.cookie', '*.password', '*.token'],
})

logger.info({ userId: '123', action: 'login' }, 'ユーザーがログインしました')
logger.error({ err, orderId }, '注文処理に失敗')
```

出力（JSON）：

```json
{"level":30,"time":1754...,"userId":"123","action":"login","msg":"ユーザーがログインしました"}
```

**JSONで出すことで、Datadog・CloudWatch などで検索・集計・アラートが可能になります。**

### ログレベルの使い分け

| レベル | 使う場面 |
| --- | --- |
| `fatal` | プロセスを止めるべき致命的な問題 |
| `error` | 処理が失敗した（要調査） |
| `warn` | 想定内だが注意すべき（リトライ発生・非推奨API利用） |
| `info` | 通常の業務イベント（起動・ログイン・注文） |
| `debug` | 開発時の詳細（本番では出さない） |

### リクエストIDで追跡する

```ts
import { randomUUID } from 'node:crypto'

app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] ?? randomUUID()
  req.log = logger.child({ requestId: req.id })   // 子ロガーを作る
  res.setHeader('x-request-id', req.id)
  next()
})

// 以降 req.log を使うと、全ログに requestId が付く
req.log.info({ orderId }, '注文を作成')
```

**「このユーザーのこのリクエストで何が起きたか」を一続きで追える**ようになります。障害調査の速度が劇的に変わります。

### 🚨 ログに出してはいけないもの

- パスワード・トークン・APIキー
- クレジットカード番号
- 個人情報（要件次第。マスクを検討）
- リクエストボディの丸ごと出力（秘密情報が混ざる）

---

## 2. セキュリティ

### 依存パッケージ

```bash
npm audit                    # 脆弱性チェック
npm audit fix                # 自動修正
```

- **Dependabot / Renovate** で自動更新PRを作る
- 使っていないパッケージは削除する
- 導入前にダウンロード数・更新状況を確認（→ [③](03-modules-packages.md#-npmパッケージのセキュリティ)）

### 主要な脆弱性と対策

| 脆弱性 | 対策 |
| --- | --- |
| **SQLインジェクション** | ORM／パラメータ化クエリ。**文字列結合でSQLを作らない** |
| **XSS** | 出力エスケープ。テンプレートエンジンの自動エスケープを切らない |
| **パストラバーサル** | `path.resolve` 後に想定ディレクトリ内か確認（→ [④](04-core-apis.md)） |
| **コマンドインジェクション** | `exec` を避け `execFile` を使う。ユーザー入力を渡さない |
| **SSRF** | ユーザー指定URLへのリクエストは、宛先を許可リストで制限 |
| **ReDoS** | 正規表現のバックトラッキングに注意。入力長を制限 |
| **プロトタイプ汚染** | `JSON.parse` 結果をそのままマージしない |
| **総当たり攻撃** | レート制限（→ [⑥](06-server-frameworks.md)） |

```ts
// ❌ コマンドインジェクション
exec(`convert ${userInput} out.png`)

// ✅ 引数を配列で渡す（シェルを経由しない）
execFile('convert', [userInput, 'out.png'])
```

### パスワードの扱い

```ts
import argon2 from 'argon2'

const hash = await argon2.hash(password)          // 保存時
const ok = await argon2.verify(hash, password)    // 検証時
```

**必ず argon2 か bcrypt を使ってください。** SHA-256 等の高速ハッシュは総当たりに弱く、パスワード用途には不適切です。

---

## 3. パフォーマンス

### 計測が先

```bash
# CPUプロファイルを取る
node --cpu-prof --cpu-prof-dir=./prof app.js
# 出力された .cpuprofile を Chrome DevTools で開く

# メモリのヒープスナップショット
node --heap-prof app.js
```

```ts
// イベントループ遅延の常時監視（→ ②章）
import { monitorEventLoopDelay } from 'node:perf_hooks'
const h = monitorEventLoopDelay()
h.enable()
setInterval(() => {
  if (h.max / 1e6 > 100) logger.warn({ maxDelayMs: h.max / 1e6 }, 'イベントループ遅延')
  h.reset()
}, 30_000)
```

### よくあるボトルネックと対処

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| APIが遅い | 直列 `await` | `Promise.all`（→ [⑤](05-async-patterns.md)） |
| DBが遅い | N+1クエリ | JOIN／`include` でまとめる |
| DBが遅い | インデックス不足 | 実行計画（`EXPLAIN`）を確認 |
| メモリが増え続ける | リスナー解除漏れ・キャッシュ肥大 | ヒープスナップショット比較 |
| CPU 100% | 重い同期処理 | worker/キューへ（→ [②](02-event-loop.md)） |
| 起動が遅い | 大量のimport | 遅延importを検討 |
| 接続エラー多発 | DB接続数の上限 | プール設定・プーラー導入 |

### N+1問題

```ts
// ❌ 101回のクエリ
const posts = await db.post.findMany()
for (const post of posts) {
  post.author = await db.user.findUnique({ where: { id: post.authorId } })
}

// ✅ 1回
const posts = await db.post.findMany({ include: { author: true } })
```

### キャッシュ

```ts
import { Redis } from 'ioredis'
const redis = new Redis(env.REDIS_URL)

async function getUser(id: string) {
  const cached = await redis.get(`user:${id}`)
  if (cached) return JSON.parse(cached)

  const user = await db.user.findUnique({ where: { id } })
  await redis.setex(`user:${id}`, 300, JSON.stringify(user))   // 5分
  return user
}
```

> ⚠️ **キャッシュを入れる前に、まずクエリとインデックスを見直してください。** キャッシュは「古いデータが出る」「無効化の考慮が必要」という複雑さを持ち込みます。安易に入れるとバグの温床になります。

---

## 4. Docker でのデプロイ

### マルチステージビルド

```dockerfile
# ---- 依存インストール ----
FROM node:24-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci                                  # ★lock通りに

# ---- ビルド ----
FROM node:24-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# ---- 実行 ----
FROM node:24-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN npm ci --omit=dev                       # ★本番依存のみ
COPY --from=builder /app/dist ./dist

# ★rootで動かさない
RUN addgroup -S app && adduser -S app -G app
USER app

# ★シグナルを正しく処理させる（PID 1問題対策）
RUN apk add --no-cache dumb-init
ENTRYPOINT ["dumb-init", "--"]

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### 押さえるべきポイント

| ポイント | 理由 |
| --- | --- |
| **`npm ci`** を使う | lockファイル通りで再現性がある |
| **`--omit=dev`** | 本番イメージを小さく・安全に |
| **非rootユーザー** | 侵害されたときの被害を限定 |
| **`dumb-init`** | Node.jsをPID 1で動かすとSIGTERMが正しく届かない |
| **`.dockerignore`** | `node_modules` `.git` を除外してビルドを高速化 |
| **`NODE_ENV=production`** | 多くのライブラリが本番モードに切り替わる |

```
# .dockerignore
node_modules
.git
.env
dist
```

### グレースフルシャットダウン（再掲・重要）

コンテナは頻繁に停止・再作成されます。**処理中のリクエストを完了させてから終了**しないと、デプロイのたびにエラーが出ます。

```ts
process.on('SIGTERM', async () => {
  server.close(async () => {
    await db.end()
    process.exit(0)
  })
  setTimeout(() => process.exit(1), 10_000).unref()
})
```

詳細は [④](04-core-apis.md#グレースフルシャットダウン)。

---

## 5. ヘルスチェックと監視

```ts
// 生存確認（プロセスが動いているか）
app.get('/healthz', (req, res) => res.json({ status: 'ok' }))

// 準備確認（依存先も含めて処理可能か）
app.get('/readyz', async (req, res) => {
  try {
    await db.$queryRaw`SELECT 1`
    await redis.ping()
    res.json({ status: 'ready' })
  } catch (err) {
    res.status(503).json({ status: 'not ready' })
  }
})
```

> 🔑 **`healthz` と `readyz` を分ける理由**：DBが一時的に落ちているときに `healthz` まで失敗させると、コンテナが再起動を繰り返します。「プロセスは生きている（healthz）が、まだリクエストは受けられない（readyz）」を区別するのが正しい設計です。

### 監視すべき指標

| 指標 | 閾値の目安 |
| --- | --- |
| エラー率 | 1%を超えたらアラート |
| レスポンスタイム（p95 / p99） | サービス要件による |
| **イベントループ遅延** | 100msを超えたら要調査 |
| メモリ使用量 | 上限の80%で警告 |
| DB接続数 | プール上限に近づいたら警告 |
| 再起動回数 | 頻発していれば異常 |

---

## 6. テスト

```ts
// Vitest の例
import { describe, it, expect, vi } from 'vitest'
import request from 'supertest'
import { app } from '../src/app'

describe('POST /users', () => {
  it('正常なデータで201を返す', async () => {
    const res = await request(app)
      .post('/users')
      .send({ name: '田中', email: 'tanaka@example.com' })

    expect(res.status).toBe(201)
    expect(res.body).toMatchObject({ name: '田中' })
  })

  it('不正なメールアドレスで400を返す', async () => {
    const res = await request(app).post('/users').send({ name: 'x', email: 'invalid' })
    expect(res.status).toBe(400)
  })

  it('未認証では401を返す', async () => {
    const res = await request(app).delete('/posts/1')
    expect(res.status).toBe(401)
  })
})
```

### テストの優先順位

```
1. 認証・認可（壊れると被害が大きい）       ← 最優先
2. バリデーション（境界値・異常系）
3. ビジネスロジックの中核
4. エラーハンドリング
5. 正常系のハッピーパス
```

> 💡 **DBを使うテスト**は、Testcontainers か Docker Compose で実際のDBを立てるのが最も確実です。モックだけだと「モックは通るが本番で壊れる」が起きます。

---

## 7. CI/CD

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: postgres }
        options: >-
          --health-cmd pg_isready --health-interval 10s --health-retries 5
        ports: ['5432:5432']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/postgres
      - run: npm run build
      - run: npm audit --audit-level=high
```

---

## 8. 本番リリース前チェックリスト

**設定**
- [ ] `NODE_ENV=production` が設定されている
- [ ] 環境変数が起動時に検証される（→ [④](04-core-apis.md)）
- [ ] 秘密情報がコード・ログに含まれていない
- [ ] Node.jsのバージョンがLTS（24系）

**信頼性**
- [ ] グレースフルシャットダウンを実装した
- [ ] `unhandledRejection` / `uncaughtException` を処理した
- [ ] ヘルスチェック（`healthz` / `readyz`）がある
- [ ] 外部API呼び出しにタイムアウトがある

**セキュリティ**
- [ ] 入力を全てバリデーションしている
- [ ] 認証・認可（所有者チェック含む）がある
- [ ] レート制限がある
- [ ] `helmet`・CORS制限・ボディサイズ上限
- [ ] `npm audit` に高危険度の問題がない
- [ ] 非rootユーザーで実行している

**運用**
- [ ] 構造化ログ＋リクエストIDがある
- [ ] エラー監視（Sentry等）を入れた
- [ ] イベントループ遅延を監視している
- [ ] DBのバックアップとロールバック手順を確認した

---

## 9. この章のまとめ

- ログは **構造化ログ（pino）＋リクエストID**。`console.log` は本番では不十分
- 🚨 **ログに秘密情報を出さない**。`redact` でマスクする
- パスワードは **argon2 / bcrypt**。高速ハッシュ（SHA-256）は不適切
- **計測してから最適化**。イベントループ遅延・CPUプロファイルを見る
- **キャッシュの前にクエリとインデックスを見直す**
- Dockerでは **`npm ci` / `--omit=dev` / 非root / dumb-init** を押さえる
- **`healthz`（生存）と `readyz`（準備完了）を分ける**
- テストは **認証・認可を最優先**。DBは実物を使うのが確実

---

次 → [用語集・チートシート](glossary.md)
