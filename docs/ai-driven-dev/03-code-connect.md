---
title: ③ Code Connect
---

# ③ Code Connect — このシリーズで最も重要な章

[← 総合インデックスに戻る](README.md) ｜ 前 → [② デザイントークン連携](02-design-tokens.md) ｜ 次 → [④ Figma MCPの接続と使い方](04-figma-mcp.md)

**ここを読まずにFigma MCPを繋ぐと、ほぼ確実に失望します。** Code Connect は「Figmaのコンポーネント ↔ リポジトリの実コンポーネント」の対応表であり、AI駆動開発の品質を決定づけます。

---

## 1. Code Connect が無いと何が起きるか

同じFigmaのボタンを、AIに実装させた結果の比較です。

```tsx
// ❌ Code Connectなし
<div className="flex items-center justify-center px-4 py-2 bg-[#3B82F6] rounded-[6px] text-white text-[14px] font-medium">
  送信
</div>
```

```tsx
// ✅ Code Connectあり
<Button variant="primary" size="md">送信</Button>
```

### 何が問題なのか

| 問題 | 影響 |
| --- | --- |
| **既存コンポーネントを使っていない** | 同じボタンが画面ごとに再実装される |
| **値がハードコード** | トークン変更が反映されない |
| `div` にクリックを付ける | **キーボード操作できない**（a11y違反） |
| バリアントの概念がない | `primary` / `danger` の区別が失われる |
| **状態が実装されない** | hover / disabled / loading が抜ける |

実測では **Code Connect なしのスタイル不一致率は85〜90%** と報告されています。つまり「ほぼ全部書き直し」です。

---

## 2. Code Connect とは何か

**Figmaのノードと、コード上のコンポーネントを対応付けるファイル**です。リポジトリに置いて `publish` すると、FigmaのDev ModeとMCPの出力が「実際のコード」に変わります。

```
┌─────────────────┐         ┌──────────────────────┐
│ Figma           │         │ リポジトリ            │
│  Button         │ ←────→  │  components/ui/       │
│  node-id=1:23   │  対応   │    button.tsx         │
│  Variant=Primary│  表     │    button.figma.tsx ★ │
└─────────────────┘         └──────────────────────┘
                                      ↓ publish
                            Figma Dev Mode / MCP が
                            <Button variant="primary"> を返すようになる
```

### 前提条件

| 項目 | 条件 |
| --- | --- |
| Figmaプラン | **Organization 以上** |
| パッケージ | `@figma/code-connect`（1.5系） |
| 対象 | React / Web Components / SwiftUI / Compose など |

---

## 3. セットアップ

```bash
npm install -D @figma/code-connect
npx figma connect create   # 対話形式で初期設定
```

### 設定ファイル

```json
// figma.config.json
{
  "codeConnect": {
    "include": ["src/components/**/*.figma.tsx"],
    "exclude": ["**/node_modules/**"],
    "parser": "react",
    "label": "React",
    "importPaths": {
      "src/components/*": "@/components/*"
    }
  }
}
```

| 項目 | 意味 |
| --- | --- |
| `include` | Code Connectファイルの場所 |
| `parser` | `react` を指定 |
| `label` | Dev Modeに表示されるタブ名 |
| **`importPaths`** | **実際のパスをエイリアスに変換**（重要） |

> 🔑 **`importPaths` は必ず設定してください。** これが無いと `import { Button } from '../../../components/ui/button'` のような相対パスが出力されます。`@/components/ui/button` に変換されるようにします（→ [Next.js②](../nextjs/02-setup-and-structure.md)）。

### 認証

```bash
export FIGMA_ACCESS_TOKEN="figd_..."   # Code Connect の書き込み権限が必要
```

Personal Access Token をFigmaの設定から発行します。CIではSecretsに登録します。

---

## 4. 基本の書き方

コンポーネントの隣に `*.figma.tsx` を置きます。

```
src/components/ui/
├── button.tsx           # 実装
└── button.figma.tsx     # ★対応表
```

```tsx
// src/components/ui/button.figma.tsx
import figma from '@figma/code-connect'
import { Button } from './button'

figma.connect(
  Button,
  'https://www.figma.com/design/AbCdEf/DesignSystem?node-id=1-23',
  {
    props: {
      // Figmaのプロパティ名 → コードのpropsへ対応付ける
      label: figma.string('Label'),
      variant: figma.enum('Variant', {
        Primary: 'primary',
        Secondary: 'secondary',
        Danger: 'destructive',
      }),
      size: figma.enum('Size', {
        Small: 'sm',
        Medium: 'md',
        Large: 'lg',
      }),
      disabled: figma.boolean('Disabled'),
    },
    example: ({ label, variant, size, disabled }) => (
      <Button variant={variant} size={size} disabled={disabled}>
        {label}
      </Button>
    ),
  },
)
```

### node-id の取得方法

```
1. Figmaでコンポーネントを選択
2. 右クリック → Copy link to selection
3. URLの ?node-id=1-23 部分がノードID
```

---

## 5. プロパティ対応のパターン

### 主なヘルパー

| ヘルパー | Figma側 | 用途 |
| --- | --- | --- |
| `figma.string('Label')` | テキストプロパティ | ラベル・見出し |
| `figma.boolean('Disabled')` | ブールプロパティ | 有効/無効・表示切替 |
| `figma.enum('Variant', {...})` | バリアント | primary / secondary 等 |
| `figma.instance('Icon')` | インスタンススワップ | アイコン差し込み |
| `figma.children(['*'])` | 子要素 | ネストしたコンテンツ |
| `figma.className([...])` | — | クラス名の組み立て |
| `figma.textContent('Label')` | テキストノード | 直下のテキスト |

### boolean で要素ごと出し分ける

```tsx
props: {
  // trueのときだけアイコンを描画する
  icon: figma.boolean('Has icon', {
    true: figma.instance('Icon'),
    false: undefined,
  }),
},
example: ({ label, icon }) => (
  <Button>
    {icon}
    {label}
  </Button>
),
```

### 子要素をそのまま受け取る

```tsx
// Card のように中身が可変なコンポーネント
figma.connect(Card, 'https://figma.com/...?node-id=2-45', {
  props: {
    title: figma.string('Title'),
    children: figma.children(['*']),   // 中の全要素
  },
  example: ({ title, children }) => (
    <Card title={title}>{children}</Card>
  ),
})
```

`figma.children` を使うと、**中に置かれた別のコンポーネントも Code Connect 経由で解決**されます。これが効くと、画面まるごとが実コンポーネントの組み合わせとして出てきます。

### バリアントごとに別コンポーネントを返す

Figmaでは1コンポーネントでも、コードでは分かれている場合があります。

```tsx
figma.connect(Alert, 'https://figma.com/...?node-id=3-11', {
  variant: { Type: 'Error' },      // ★このバリアントのときだけ適用
  example: ({ message }) => <ErrorAlert>{message}</ErrorAlert>,
})

figma.connect(Alert, 'https://figma.com/...?node-id=3-11', {
  variant: { Type: 'Success' },
  example: ({ message }) => <SuccessAlert>{message}</SuccessAlert>,
})
```

---

## 6. 公開と検証

```bash
# 検証（構文・Figma側との整合性チェック）
npx figma connect parse

# 公開
npx figma connect publish

# 特定の設定ファイルを使う
npx figma connect publish --config figma.config.json

# 取り消し
npx figma connect unpublish
```

`publish` すると、FigmaのDev Modeに実際のコードが表示され、**Figma MCPの `get_code_connect_map` がその対応を返す**ようになります。

### 公開されたか確認する

```
1. FigmaでDev Modeを開く
2. 対象コンポーネントを選択
3. 右パネルに「React」タブが出て、自分のコードが表示されればOK
```

---

## 7. CIで自動公開する

**Code Connectは「張って終わり」ではありません。** コンポーネントを変更したら追従が必要です。手動運用は必ず腐るので、CIに載せます。

```yaml
# .github/workflows/code-connect.yml
name: Code Connect

on:
  push:
    branches: [main]
    paths: ['src/components/**']
  pull_request:
    paths: ['src/components/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 24, cache: npm }
      - run: npm ci

      # PRでは検証だけ
      - name: Code Connect を検証
        run: npx figma connect parse
        env:
          FIGMA_ACCESS_TOKEN: ${{ secrets.FIGMA_ACCESS_TOKEN }}

  publish:
    if: github.ref == 'refs/heads/main'
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 24, cache: npm }
      - run: npm ci

      # mainにマージされたら公開
      - name: Code Connect を公開
        run: npx figma connect publish
        env:
          FIGMA_ACCESS_TOKEN: ${{ secrets.FIGMA_ACCESS_TOKEN }}
```

> 🚨 **`FIGMA_ACCESS_TOKEN` は必ずGitHub Secretsへ。** コードに書くと、Figmaのデザインファイルへの書き込み権限が漏れます（→ [Next.js⑫](../nextjs/12-deploy-operations.md)）。

---

## 8. どこから張るか — 費用対効果の高い順

全コンポーネントに張る必要はありません。**上から10個で効果の大半が出ます。**

```
優先度1（必ず張る）★ ここだけで劇的に変わる
  Button / Input / Select / Checkbox / Radio
  → 出現頻度が圧倒的。a11yの担保にも直結

優先度2（早めに張る）
  Card / Badge / Avatar / Icon / Alert
  → 画面のあちこちに出る

優先度3（余力があれば）
  Table / Modal / Tabs / Dropdown / Tooltip
  → 複雑だが、張れば効果は大きい

優先度4（不要なことが多い）
  ページ固有のレイアウト・1回しか使わない要素
  → 保守コストのほうが上回る
```

### 進め方の目安

| 段階 | やること | 期待効果 |
| --- | --- | --- |
| 1週目 | 優先度1の5個 | ハードコードが大幅減 |
| 2〜3週目 | 優先度2の5個 | 画面実装がコンポーネント組立になる |
| 以降 | 新規コンポーネント作成時に必ずセットで作る | 腐らない運用へ |

> 🔑 **「新規コンポーネントを作るときは `.figma.tsx` も同時に作る」をチームのルールにしてください。** 後からまとめて張ろうとすると、絶対に終わりません。

---

## 9. 運用上の注意

### Figma側の変更に追従する

```
Figmaでプロパティ名を変更（"Label" → "Text"）
        ↓
Code Connect の figma.string('Label') が解決できなくなる
        ↓
npx figma connect parse で検出される  ← CIで落とす
```

**PRで `parse` を走らせておけば、ズレは自動検出されます。** これが無いと、静かに壊れて「なぜかCode Connectが効かない」状態になります。

### node-id のハードコードを避ける

ファイル移動やコンポーネントの再作成でnode-idが変わることがあります。

```
対策：
  ・Code Connect ファイルはコンポーネントの隣に置く（対応が追いやすい）
  ・Figma側でコンポーネントを「再作成」せず「編集」する
  ・parse をCIで常時実行し、壊れたら気づける状態にする
```

### shadcn/ui との組み合わせ

shadcn/ui は**コードが自分のリポジトリに入る**方式なので、Code Connect と非常に相性が良いです（→ [Next.js⑦](../nextjs/07-styling-ui.md)）。

```
components/ui/button.tsx        ← shadcn/uiで追加したコード（自分の物）
components/ui/button.figma.tsx  ← Code Connect を隣に置く
```

npmパッケージ型のUIライブラリだと、内部実装を触れないためpropsの対応付けが難しくなる場合があります。

---

## 10. よくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| `publish` が権限エラー | トークンの権限不足 | Code Connect 書き込み権限を付与 |
| Dev Modeに出ない | publishしていない／別ファイル | `npx figma connect publish` を実行 |
| プロパティが解決されない | Figma側の名前と不一致 | `parse` で検出。名前を揃える |
| import文が相対パスになる | `importPaths` 未設定 | `figma.config.json` に追加 |
| 一部のバリアントだけ効かない | `variant` 指定漏れ | バリアントごとに `figma.connect` を書く |
| MCPが古い対応を返す | publish後のキャッシュ | 再publish・Figma再読込 |
| 保守されず腐る | 手動運用 | **CIで `parse` を必須化** |

---

## 11. この章のまとめ

- 🚨 **Code Connect の有無が品質のほぼすべてを決める**（無いと不一致率85〜90%）
- コンポーネントの隣に **`*.figma.tsx`** を置き、`figma.connect()` で対応付ける
- `figma.string` / `figma.boolean` / `figma.enum` / `figma.instance` / `figma.children` を使い分ける
- **`importPaths` を設定**しないと相対パス地獄になる
- **`FIGMA_ACCESS_TOKEN` はSecretsへ**。コードに書かない
- **CIで `parse` を必須化**し、Figma側の変更で壊れたら検出する
- **優先度1の5個（Button/Input/Select/Checkbox/Radio）だけで効果の大半**が出る
- 🔑 **新規コンポーネント作成時に `.figma.tsx` も同時に作る**をルール化する

---

次の章 → [④ Figma MCPの接続と使い方](04-figma-mcp.md)
