---
title: ⑪ テストと品質管理
---

# ⑪ テストと品質管理

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑩ パフォーマンス最適化とSEO](10-performance-seo.md) ｜ 次 → [⑫ デプロイと運用](12-deploy-operations.md)

App Router では **Server Component のテストが難しい**という固有の事情があります。この章では現実的なテスト戦略と、型・Lintによる品質確保を扱います。

---

## 1. Next.jsにおけるテスト戦略

一般的なテストピラミッドはそのまま当てはまりません。RSCの事情を踏まえると、こうなります。

```
        ▲  E2E（Playwright）
       ▲▲▲  ← Server Componentを含むページは実質ここでしか検証できない
     ▲▲▲▲▲  結合テスト（Route Handler / Server Action）
   ▲▲▲▲▲▲▲  ユニットテスト（純粋な関数・バリデーション・Client Component）
```

| 対象 | 手段 | 難易度 |
| --- | --- | --- |
| 純粋なロジック（計算・整形） | Vitest | ⭐ 簡単 |
| Zodスキーマ | Vitest | ⭐ 簡単 |
| Client Component | Vitest ＋ Testing Library | ⭐⭐ 普通 |
| Server Action | Vitest（関数として直接呼ぶ） | ⭐⭐ 普通 |
| Route Handler | Vitest（`GET(request)` を呼ぶ） | ⭐⭐ 普通 |
| **Server Component** | **Playwright（E2E）** | ⭐⭐⭐ 難しい |

> 🔑 **現実的な結論**：Server Component を単体テストしようとすると消耗します。**「ロジックを純粋関数に切り出してユニットテスト」＋「画面はE2Eで確認」**の二段構えが、労力対効果が最も高い構成です。

---

## 2. Vitest（ユニット・結合テスト）

Jestより設定が簡単で高速なため、現在の新規プロジェクトでは主流です。

```bash
npm install -D vitest @vitejs/plugin-react vite-tsconfig-paths \
  @testing-library/react @testing-library/user-event jsdom
```

```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./vitest.setup.ts'],
    globals: true,
  },
})
```

### ロジックのテスト

```ts
// lib/price.test.ts
import { describe, it, expect } from 'vitest'
import { calcTaxIncluded } from './price'

describe('calcTaxIncluded', () => {
  it('10%の税込価格を切り捨てで返す', () => {
    expect(calcTaxIncluded(100)).toBe(110)
    expect(calcTaxIncluded(105)).toBe(115)   // 115.5 → 115
  })

  it('負の金額は例外を投げる', () => {
    expect(() => calcTaxIncluded(-1)).toThrow()
  })
})
```

### Client Component のテスト

```tsx
// components/Counter.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Counter } from './Counter'

it('クリックでカウントが増える', async () => {
  render(<Counter />)
  await userEvent.click(screen.getByRole('button', { name: '0' }))
  expect(screen.getByRole('button')).toHaveTextContent('1')
})
```

### Server Action のテスト

Server Action は**ただの非同期関数**なので、直接呼べます。

```ts
// app/posts/actions.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createPost } from './actions'

vi.mock('@/lib/db', () => ({
  db: { post: { create: vi.fn() } },
}))
vi.mock('@/auth', () => ({
  auth: vi.fn(() => ({ user: { id: 'user-1' } })),
}))
vi.mock('next/cache', () => ({ revalidateTag: vi.fn() }))

it('タイトルが空ならバリデーションエラーを返す', async () => {
  const fd = new FormData()
  fd.set('title', '')
  fd.set('body', '十分な長さの本文です')

  const result = await createPost({}, fd)
  expect(result.errors?.title).toBeDefined()
})
```

> 💡 **セキュリティのテストは必ず書いてください。** 「未ログインなら弾く」「他人の投稿は削除できない」は、リグレッションが起きると被害が大きい部分です（→ [⑥](06-server-actions-forms.md#6--セキュリティ--この章で最も重要)）。

### Route Handler のテスト

```ts
import { GET } from './route'
import { NextRequest } from 'next/server'

it('クエリなしで一覧を返す', async () => {
  const res = await GET(new NextRequest('http://localhost/api/posts'))
  expect(res.status).toBe(200)
  expect(await res.json()).toHaveLength(3)
})
```

---

## 3. Playwright（E2Eテスト）

**Server Componentを含む画面を検証できる唯一の現実的な手段**です。

```bash
npm init playwright@latest
```

```ts
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  use: { baseURL: 'http://localhost:3000' },
  webServer: {
    command: 'npm run build && npm run start',   // ★本番ビルドで検証
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

```ts
// e2e/post.spec.ts
import { test, expect } from '@playwright/test'

test('記事を作成して一覧に表示される', async ({ page }) => {
  await page.goto('/posts/new')
  await page.getByLabel('タイトル').fill('テスト記事')
  await page.getByLabel('本文').fill('これは本文です。十分な長さがあります。')
  await page.getByRole('button', { name: '作成' }).click()

  await expect(page).toHaveURL('/posts')
  await expect(page.getByText('テスト記事')).toBeVisible()
})

test('未ログインではダッシュボードに入れない', async ({ page }) => {
  await page.goto('/dashboard')
  await expect(page).toHaveURL(/\/login/)
})
```

> ⚠️ **E2Eは `npm run dev` ではなく本番ビルドで走らせてください。** キャッシュ挙動が違うため、devで通っても本番で落ちるケースを取り逃します（設定例の `webServer.command` を参照）。

### E2Eで優先して書くべきもの

労力がかかるので、**壊れたら致命的な経路だけ**に絞ります。

- [ ] ログイン → 主要機能 → ログアウト
- [ ] 課金・申し込みなど収益に直結する導線
- [ ] 認可（他人のデータにアクセスできないこと）
- [ ] フォーム送信の成功・失敗

---

## 4. TypeScript の設定

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,                        // 必須
    "noUncheckedIndexedAccess": true,      // arr[0] が T | undefined になる
    "noUnusedLocals": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### 型チェックをCIで走らせる

```json
// package.json
"scripts": {
  "typecheck": "tsc --noEmit"
}
```

> ⚠️ **`next build` の型チェックだけに頼らない**でください。テストファイルなど、ビルド対象外のコードは検査されません。

### 環境変数の型安全化

`process.env.FOO` は常に `string | undefined` で、タイポにも気づけません。起動時に検証すると安全です。

```ts
// lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  AUTH_SECRET: z.string().min(32),
  NEXT_PUBLIC_SITE_URL: z.string().url(),
})

export const env = envSchema.parse(process.env)
```

設定漏れが**起動時に即座にわかる**ようになります（本番で初めて気づくのを防げます）。

---

## 5. ESLint と Prettier

### ⚠️ Next.js 16 の変更：`next lint` は削除されました

```bash
# ❌ Next.js 16 では動きません
npm run lint     # next lint を呼んでいる場合

# ✅ ESLintを直接実行する
npx eslint .
```

`next build` も自動でLintを実行しなくなったため、**CIで明示的に走らせる必要があります**。

```json
// package.json
"scripts": {
  "lint": "eslint .",
  "lint:fix": "eslint . --fix",
  "typecheck": "tsc --noEmit"
}
```

### ESLint 9（flat config）

```js
// eslint.config.mjs
import { FlatCompat } from '@eslint/eslintrc'

const compat = new FlatCompat({ baseDirectory: import.meta.dirname })

export default [
  ...compat.extends('next/core-web-vitals', 'next/typescript'),
  {
    rules: {
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
  { ignores: ['.next/**', 'node_modules/**'] },
]
```

### Biome という選択肢

ESLint＋Prettierを1つに統合したRust製ツールです。**圧倒的に高速**で、設定も1ファイルで済みます。

```bash
npm install -D @biomejs/biome
npx biome init
npx biome check --write .
```

Next.js固有のルール（`next/core-web-vitals`）が使えない点だけ注意してください。大規模プロジェクトで実行速度が問題になるなら有力な選択肢です。

---

## 6. CI（GitHub Actions）

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run test
      - run: npm run build        # ★ビルドが通ることを必ず確認
```

> 💡 **`npm run build` をCIに入れるのが最重要**です。型エラー・importミス・環境変数不足など、実際に本番を壊す問題の多くはここで検出できます。

### コミット前のチェック（husky ＋ lint-staged）

```bash
npm install -D husky lint-staged
npx husky init
echo "npx lint-staged" > .husky/pre-commit
```

```json
// package.json
"lint-staged": {
  "*.{ts,tsx}": ["eslint --fix", "prettier --write"]
}
```

---

## 7. この章のまとめ

- **Server Componentの単体テストは困難**。ロジックを純粋関数に切り出し、画面はE2Eで見る
- ユニット・結合は **Vitest**、E2Eは **Playwright**。E2Eは**本番ビルドで走らせる**
- Server Action / Route Handler は**普通の関数として直接テストできる**
- **認証・認可のテストは優先度が高い**（壊れたときの被害が大きい）
- TypeScriptは `strict: true`。環境変数は **Zodで起動時に検証**
- ⚠️ **`next lint` は Next.js 16 で削除**。ESLintを直接実行し、CIに組み込む
- CIには **lint / typecheck / test / build** の4点セットを入れる

---

次の章 → [⑫ デプロイと運用](12-deploy-operations.md)
