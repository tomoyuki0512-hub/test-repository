---
title: ③ モジュールとnpm
---

# ③ モジュールとnpm — コードの分割と依存管理

[← 総合インデックスに戻る](README.md) ｜ 前 → [② イベントループと非同期](02-event-loop.md) ｜ 次 → [④ 標準APIを使う](04-core-apis.md)

コードを分割する仕組み（モジュール）と、外部ライブラリを管理する仕組み（npm）を扱います。**「なぜかimportできない」系のトラブルの原因もここにあります。**

---

## 1. 2つのモジュール方式

Node.jsには歴史的経緯から**2つの方式**が共存しています。これが混乱の元です。

| | **CommonJS（CJS）** | **ES Modules（ESM）** |
| --- | --- | --- |
| 読み込み | `require()` | `import` |
| 公開 | `module.exports` | `export` |
| 登場 | Node.js独自（2009〜） | JS標準（2015〜） |
| 読み込み方式 | 同期 | 非同期 |
| ブラウザ | 動かない | 動く |
| 現在の位置づけ | 既存コードで現役 | **新規はこちら** |

### CommonJS

```js
// utils.js
function add(a, b) { return a + b }
module.exports = { add }

// main.js
const { add } = require('./utils')
```

### ES Modules（推奨）

```js
// utils.js
export function add(a, b) { return a + b }
export default class Calculator {}

// main.js
import Calculator, { add } from './utils.js'    // ⚠️ 拡張子が必要
```

---

## 2. ESMを使う設定

```json
// package.json
{
  "type": "module"
}
```

これで `.js` ファイルがESMとして扱われます。指定しない場合はCommonJSです。

| 拡張子 | 扱い |
| --- | --- |
| `.js` | `"type"` の設定に従う |
| `.mjs` | **常にESM** |
| `.cjs` | **常にCommonJS** |

### ⚠️ ESMの注意点

#### ① 拡張子が必須

```js
import { add } from './utils'       // ❌ エラー
import { add } from './utils.js'    // ✅
```

TypeScriptで書いていても、**出力後のファイル名（`.js`）を書く**必要があります（`"moduleResolution": "bundler"` などの設定で緩和できます）。

#### ② `__dirname` / `__filename` が使えない

```js
// ❌ ESMでは未定義
console.log(__dirname)

// ✅ 代替（Node.js 20.11以降）
console.log(import.meta.dirname)
console.log(import.meta.filename)

// ✅ 古いバージョンでの書き方
import { fileURLToPath } from 'node:url'
import path from 'node:path'
const __dirname = path.dirname(fileURLToPath(import.meta.url))
```

#### ③ JSONのimportには属性が必要

```js
import config from './config.json' with { type: 'json' }
```

#### ④ トップレベルawaitが使える（利点）

```js
// ESMでは関数の外でawaitできる
const data = await fetch('https://api.example.com').then((r) => r.json())
```

### 相互運用

```js
// ESMからCommonJSを読む → できる
import lodash from 'lodash'          // ✅

// CommonJSからESMを読む → 同期requireは基本的に不可
const mod = await import('./esm-module.js')   // ✅ 動的importなら可能
```

> 🚨 **`ERR_REQUIRE_ESM` エラー**：CommonJSのコードからESM専用パッケージを `require` したときに出ます。近年、多くのライブラリがESM専用に移行しているため頻繁に遭遇します。**対処**：自分のプロジェクトを `"type": "module"` にするか、動的 `import()` を使ってください。

---

## 3. package.json の読み方

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "dev": "node --watch src/index.js",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "vitest"
  },
  "dependencies": {
    "express": "^5.0.0"
  },
  "devDependencies": {
    "typescript": "^5.7.0"
  },
  "engines": {
    "node": ">=24.0.0"
  }
}
```

| フィールド | 意味 |
| --- | --- |
| `type` | `"module"` でESM、省略でCommonJS |
| `scripts` | `npm run <名前>` で実行できるコマンド |
| **`dependencies`** | **本番で必要**なパッケージ |
| **`devDependencies`** | **開発時だけ**必要（TypeScript・テスト・Lint） |
| `engines` | 必要なNode.jsバージョン |

> 🔑 **`dependencies` と `devDependencies` を正しく分ける**と、本番のイメージサイズと起動時間が改善します。`@types/*`・テストツール・Lintは必ず `devDependencies` へ。

### バージョン指定の記号

```json
"express": "^5.1.0"    // 5.x.x の最新（メジャーは上げない）← 既定
"express": "~5.1.0"    // 5.1.x の最新（マイナーも上げない）
"express": "5.1.0"     // このバージョンに固定
```

| 記号 | 許容範囲 | 使いどころ |
| --- | --- | --- |
| `^` | マイナー・パッチ更新 | 通常はこれ |
| `~` | パッチ更新のみ | 慎重にいきたいとき |
| なし | 完全固定 | 破壊的変更を絶対に避けたいとき |

---

## 4. lockファイルが最重要

```
package.json       … 「^5.1.0 が欲しい」という希望
package-lock.json  … 「実際に入れたのは 5.1.3」という記録 ← ★これが重要
```

> 🚨 **`package-lock.json` は必ずGitにコミットしてください。** これがないと、開発環境と本番環境で違うバージョンが入り、「自分の環境では動くのに本番で壊れる」が起きます。

```bash
npm install    # package.json を見て解決 → lockを更新
npm ci         # ★lockファイル通りに正確にインストール（CI・本番用）
```

**CIとDockerビルドでは必ず `npm ci` を使ってください。** 速く、かつ再現性が保証されます。

---

## 5. よく使うnpmコマンド

```bash
npm install <pkg>            # 追加（dependencies）
npm install -D <pkg>         # 追加（devDependencies）
npm uninstall <pkg>          # 削除
npm ci                       # lock通りにインストール（CI用）
npm update                   # 許容範囲内で更新
npm outdated                 # 古くなったパッケージ一覧
npm audit                    # 脆弱性チェック
npm audit fix                # 自動修正（可能なもののみ）
npm ls <pkg>                 # 依存ツリーのどこにあるか確認
npx <cmd>                    # インストールせず1回だけ実行
```

### パッケージマネージャの比較

| | npm | pnpm | yarn | bun |
| --- | --- | --- | --- | --- |
| 同梱 | ✅ Node.jsに付属 | ❌ | ❌ | ❌ |
| 速度 | 標準 | **速い** | 速い | **最速** |
| ディスク | 重複あり | **共有して省容量** | 重複あり | 省容量 |
| モノレポ | 対応 | **得意** | 対応 | 対応 |

> 💡 **迷ったらnpmで十分**です。プロジェクトが増えてディスクを圧迫する、モノレポを扱う、といった段階で **pnpm** を検討してください。**プロジェクト内で混在させない**ことが重要です（lockファイルが競合します）。

---

## 6. 依存関係のトラブル対処

### よくある症状と対処

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| `Cannot find module 'xxx'` | 未インストール／パス間違い | `npm install`、パスと拡張子を確認 |
| `ERR_REQUIRE_ESM` | CJSからESMをrequire | `"type": "module"` か動的import |
| 型が見つからない | 型定義パッケージがない | `npm i -D @types/xxx` |
| ローカルでは動くがCIで失敗 | lockと不一致 | `npm ci` を使う |
| インストールが壊れた | キャッシュ・不整合 | `rm -rf node_modules package-lock.json && npm install` |
| バージョンが競合する | 複数バージョンが混在 | `npm ls <pkg>` で確認、`overrides` で固定 |

### 依存を強制的に揃える

```json
// package.json — 推移的依存のバージョンを強制
{
  "overrides": {
    "semver": "^7.5.4"
  }
}
```

脆弱性のあるパッケージが依存の奥深くにある場合の対処法です。

---

## 7. 🚨 npmパッケージのセキュリティ

npmは誰でも公開できるため、**悪意あるパッケージが混入するリスク**があります。

### 導入前のチェック

- [ ] 週間ダウンロード数は十分か（極端に少ないものは要注意）
- [ ] 最終更新はいつか（数年放置されていないか）
- [ ] GitHubのIssue・PRに反応があるか
- [ ] **パッケージ名にタイポがないか**（`react` と `raect` のような**typosquatting**）
- [ ] ライセンスは要件に合うか
- [ ] インストールスクリプト（`postinstall`）で不審なことをしていないか

### 運用での対策

```bash
npm audit                              # 定期的に脆弱性を確認
npm ci --ignore-scripts                # インストールスクリプトを実行しない
```

- **Dependabot / Renovate** を有効にして自動更新PRを作る
- 依存は少ないほど安全。「数行の処理のためにパッケージを入れない」

> 💡 **依存を増やすことのコスト**を意識してください。1つのパッケージが数十の推移的依存を連れてくることがあります。`npm ls` で確認する習慣をつけると、無自覚な肥大化を防げます。

---

## 8. 自分のコードを整理する

### ディレクトリ構成の例

```
src/
├── index.ts           # エントリポイント
├── routes/            # ルーティング
├── services/          # ビジネスロジック
├── repositories/      # DB操作
├── lib/               # 汎用ユーティリティ
├── config/            # 設定・環境変数
└── types/             # 型定義
```

### インポートパスを短くする

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  }
}
```

```ts
import { logger } from '@/lib/logger'   // ../../../ が消える
```

### 標準モジュールは `node:` プレフィックスを付ける

```js
import fs from 'node:fs/promises'    // ✅ 推奨
import fs from 'fs'                  // 動くが非推奨
```

**`node:` を付ける利点**：npmパッケージと明確に区別でき、`fs` という名前のパッケージに乗っ取られる事故（依存混同攻撃）を防げます。

---

## 9. この章のまとめ

- モジュール方式は **CommonJS（`require`）と ESM（`import`）** の2つ。**新規はESM**
- ESMを使うには `package.json` に **`"type": "module"`**
- ESMの注意点：**拡張子必須・`__dirname` は `import.meta.dirname`・トップレベルawaitが使える**
- `ERR_REQUIRE_ESM` は CJS から ESM専用パッケージを読んだときに出る
- **`dependencies` と `devDependencies` を正しく分ける**
- 🚨 **`package-lock.json` は必ずコミット**。CI・本番では **`npm ci`**
- パッケージ導入前に**ダウンロード数・更新状況・名前のタイポ**を確認する
- 標準モジュールは **`node:` プレフィックス**を付ける

---

次の章 → [④ 標準APIを使う](04-core-apis.md)
