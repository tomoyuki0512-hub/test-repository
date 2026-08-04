---
title: ⑬ 実践アーキテクチャ
---

# ⑬ 実践アーキテクチャ — ディレクトリ設計と大規模化

[← 総合インデックスに戻る](README.md) ｜ 前 → [⑫ デプロイと運用](12-deploy-operations.md) ｜ 次 → [⑭ 併用フレームワーク・ライブラリ総覧](14-ecosystem-frameworks.md)

ここまでの章は「機能をどう書くか」でした。この章は「**コードをどう置くか**」です。Next.js はディレクトリ構成を強制しないため、**チームで方針を決めないと1年で破綻します**。

---

## 1. 規模別のディレクトリ構成

### 小規模（〜20画面 / 1〜2人）

```
src/
├── app/
├── components/
│   ├── ui/           # ボタン等の最小単位（shadcn/ui）
│   └── ...           # それ以外
└── lib/
    ├── db.ts
    └── utils.ts
```

**最初はこれで十分です。** 早すぎる抽象化はかえって邪魔になります。

### 中規模（20〜100画面 / 3〜10人）— features構成

機能ごとにまとめる **Feature-based（コロケーション）** 構成に移行します。

```
src/
├── app/                      # ルーティングのみ。薄く保つ
│   ├── (marketing)/
│   └── (app)/
│       └── posts/
│           ├── page.tsx      # featuresから呼ぶだけ
│           └── [id]/page.tsx
├── features/                 # ★機能ごとのまとまり
│   ├── posts/
│   │   ├── components/       # この機能でしか使わないUI
│   │   ├── actions.ts        # Server Actions
│   │   ├── queries.ts        # データ取得
│   │   ├── schema.ts         # Zodスキーマ
│   │   └── types.ts
│   └── auth/
├── components/ui/            # 全機能で共通のUI
└── lib/                      # 全機能で共通のロジック
```

**判断基準**：「この部品は他の機能でも使うか？」→ Yesなら `components/`、Noなら `features/xxx/components/`。

### 大規模（100画面〜 / 10人以上）

`features/` に加え、モノレポやパッケージ分割を検討します。

```
apps/
├── web/              # Next.js本体
└── admin/            # 管理画面（別アプリ）
packages/
├── ui/               # 共通デザインシステム
├── db/               # スキーマ・クライアント
└── config/           # ESLint・TS設定の共有
```

ツールは **Turborepo** か **pnpm workspaces** が一般的です。

> ⚠️ **モノレポは早すぎると負債になります。** ビルド設定・依存管理の複雑さが増すため、「アプリが2つ以上ある」「チームが分かれている」が揃ってから導入してください。

---

## 2. レイヤ分割の考え方

Next.js には「Controller / Service / Repository」のような決まった型はありませんが、**責務を分けないとページコンポーネントが肥大化**します。

```
┌──────────────────────────────────────┐
│ app/**/page.tsx                       │  ← 画面の組み立てだけ
│  ・データを呼ぶ                        │
│  ・コンポーネントを並べる               │
└──────────────────────────────────────┘
              ↓ 呼ぶ
┌──────────────────────────────────────┐
│ features/*/queries.ts, actions.ts     │  ← ★ここに認可とロジック
│  ・認証/認可チェック                   │
│  ・バリデーション                      │
│  ・ビジネスルール                      │
└──────────────────────────────────────┘
              ↓ 呼ぶ
┌──────────────────────────────────────┐
│ lib/db.ts （ORM）                     │  ← データアクセスのみ
└──────────────────────────────────────┘
```

### 具体例

```ts
// features/posts/queries.ts
import 'server-only'
import { cache } from 'react'
import { requireUser } from '@/lib/auth'

export const getMyPosts = cache(async () => {
  const user = await requireUser()            // ★認可はここ
  return db.post.findMany({
    where: { authorId: user.id },             // ★所有者条件
    orderBy: { createdAt: 'desc' },
  })
})
```

```tsx
// app/(app)/posts/page.tsx — 薄い
import { getMyPosts } from '@/features/posts/queries'
import { PostList } from '@/features/posts/components/PostList'

export default async function PostsPage() {
  const posts = await getMyPosts()
  return <PostList posts={posts} />
}
```

> 🔑 **`page.tsx` に直接 `db.post.findMany()` を書かない**のがポイントです。認可チェックの書き漏れが起きやすく、同じクエリが複数ページに散らばります（→ [⑧](08-auth-database.md#3--認可authorizationをどこに置くか)）。

---

## 3. 状態管理の判断

App Router では「状態管理ライブラリを入れる前に考えること」があります。

```
その状態はどこにある？

サーバーのデータ（DB由来）
    → Server Componentで取る。ライブラリ不要 ✅

URLで表現できる（検索条件・ページ番号・タブ）
    → searchParams を使う ✅（共有・リロードに強い）

フォームの入力値
    → useState または React Hook Form

1コンポーネント内だけの表示状態（開閉など）
    → useState

複数コンポーネントで共有する画面状態（テーマ・カート）
    → Zustand / Jotai / Context

クライアント主導のサーバーデータ（無限スクロール等）
    → TanStack Query
```

> 💡 **「Reduxを入れる」から始めない**でください。App Routerでは、従来クライアント状態として持っていたものの多くがサーバー側かURLに移ります。**まず何も入れずに書き、必要になってから足す**のが正解です。

### URLを状態として使う

```tsx
// 検索条件をURLに持たせる → 共有・ブックマーク・戻るボタンが全部効く
// /posts?q=next&sort=new
export default async function Page({ searchParams }) {
  const { q, sort } = await searchParams
  const posts = await searchPosts({ q, sort })
  return <PostList posts={posts} />
}
```

`useState` で持つと、リロードで消え、URLを共有しても相手に同じ画面が出せません。**「他の人に見せたい情報か？」がURLに置くかの判断基準**です。

---

## 4. アンチパターン集

実際のプロジェクトでよく見る問題と、その修正方針です。

### ❌ ルートに `'use client'`

```tsx
// app/layout.tsx
'use client'   // 😱 アプリ全体がクライアントになる
```

**修正**：Provider が必要なら、Provider だけを `'use client'` のコンポーネントに切り出し、`children` を受け取る形にする（→ [④](04-server-client-components.md#5-組み合わせのルール)）。

### ❌ 自分のAPIを `fetch` する

```tsx
// Server Component の中で
const res = await fetch('http://localhost:3000/api/posts')   // 😱
```

同じサーバー内で無駄なHTTP往復が発生し、認証Cookieの引き回しも面倒になります。

**修正**：`db.post.findMany()` を直接呼ぶ。Route Handlerは外部向けだけ。

### ❌ `page.tsx` が数百行

**修正**：データ取得を `queries.ts` に、UIを `components/` に切り出す。`page.tsx` は「呼んで並べるだけ」に保つ。

### ❌ 認可チェックのコピペ

各ページに `if (!session) redirect('/login')` が散在している状態。1箇所書き忘れると穴になります。

**修正**：`requireUser()` のような関数を作り、**データ取得関数の中で必ず呼ぶ**。

### ❌ `any` の多用と `as` での握りつぶし

**修正**：外部データの境界（API・フォーム・環境変数）で **Zodを使って型を確定**させる。

### ❌ 巨大な `utils.ts`

無関係な関数が数十個入っているファイル。

**修正**：`lib/date.ts` `lib/price.ts` のように用途で分割する。

---

## 5. チームで最初に決めておくこと

技術的な正解より、**「揃っていること」が価値**の項目です。

| 決めること | 選択肢の例 |
| --- | --- |
| ディレクトリ構成 | features構成にするか / どこまで共通化するか |
| 命名規則 | ファイル名は kebab-case か PascalCase か |
| Server / Client の境界方針 | `'use client'` を書いてよい場所のルール |
| フォームの書き方 | Server Actions ＋ `useActionState` に統一するか |
| バリデーション | Zodスキーマの置き場所（`schema.ts`） |
| エラーハンドリング | 例外を投げるか結果型を返すか |
| コミット規約 | Conventional Commits を使うか |
| PRレビュー基準 | 何を必ず見るか（認可・型・テスト） |

これらを `CONTRIBUTING.md` か **ADR（Architecture Decision Record）** として残しておくと、後から参加した人が判断に迷いません。

---

## 6. 段階的な成長の道筋

```
フェーズ1: とにかく動かす
  app/ + components/ + lib/
  状態管理なし、テストは主要導線のE2Eだけ
        ↓ 画面が20を超える / 人が増える
フェーズ2: 機能で区切る
  features/ を導入。queries.ts / actions.ts に責務を分ける
  認可を requireUser() に集約
        ↓ 共通UIが増える / 別アプリが必要になる
フェーズ3: パッケージを分ける
  Turborepo / pnpm workspaces
  packages/ui にデザインシステムを切り出す
```

> 🔑 **最初からフェーズ3をやらないでください。** 「将来大きくなるかもしれないから」で構成を複雑にすると、立ち上がりが遅くなり、そもそも大きくなる前に頓挫します。**必要になったときに移行できる程度に整理しておく**が正解です。

---

## 7. この章のまとめ

- 小規模は `app/` `components/` `lib/` の3つで十分。**早すぎる抽象化を避ける**
- 中規模から **`features/` 構成**へ。判断基準は「他の機能でも使うか」
- `page.tsx` は薄く保ち、**認可とロジックは `queries.ts` / `actions.ts` に集約**
- 状態管理は**まず入れない**。サーバーデータはRSC、検索条件はURL（`searchParams`）
- アンチパターンの筆頭は **ルートの `'use client'`** と **自分のAPIを `fetch`**
- チームでは「正解」より**揃っていること**が重要。ADR等で決定を残す
- **段階的に成長させる**。最初からモノレポにしない

---

次の章 → [⑭ 併用フレームワーク・ライブラリ総覧](14-ecosystem-frameworks.md)
