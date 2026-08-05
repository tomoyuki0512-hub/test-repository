---
title: AI駆動開発 用語集・チートシート
---

# 用語集・チートシート

[← 総合インデックスに戻る](README.md)

用語辞典・逆引き表・コマンド集です。

---

## 1. 用語集

### MCP・AI関連

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **MCP** | Model Context Protocol。AIに外部データ・機能を提供する共通規格 | [④](04-figma-mcp.md) |
| **MCPサーバー** | MCPで機能を提供する側（Figma MCP・GitHub MCP など） | [④](04-figma-mcp.md) |
| **MCPクライアント** | MCPサーバーに接続する側（Claude Code など） | [④](04-figma-mcp.md) |
| **`CLAUDE.md`** | AIが毎回読む恒久ルールを書くファイル | [⑤](05-ai-workflow.md) |
| **品質ゲート** | CIで機械的に落とす仕組み（Lint・型・テスト） | [⑤](05-ai-workflow.md) |
| **AI駆動開発** | AIが実装の主体となり、人間が指示とレビューを担う開発形態 | [①](01-overview.md) |

### Figma関連

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **Figma MCPサーバー** | FigmaのデザインをAIに提供するMCPサーバー。**ベータ** | [④](04-figma-mcp.md) |
| **リモート版MCP** | `mcp.figma.com/mcp`。**全プラン・全シートで利用可（推奨）** | [④](04-figma-mcp.md) |
| **デスクトップ版MCP** | Figmaアプリ経由。**Dev/Fullシート＋有料プラン必須** | [④](04-figma-mcp.md) |
| **`get_code`** | 選択範囲を React + Tailwind で生成するツール | [④](04-figma-mcp.md) |
| **`get_variable_defs`** | 使用されている変数・スタイルを取得 | [④](04-figma-mcp.md) |
| **`get_code_connect_map`** | Figmaノード → 実コンポーネントの対応を取得 | [④](04-figma-mcp.md) |
| **`use_figma`** | キャンバスへ書き込むツール（リモート版） | [④](04-figma-mcp.md) |
| **Dev Mode** | Figmaの開発者向けモード。有料プランが必要 | [①](01-overview.md) |
| **node-id** | Figmaのノード識別子。URLの `?node-id=1-23` | [③](03-code-connect.md) |
| **Auto Layout** | Figmaの自動レイアウト機能。**これが無いと絶対配置になる** | [⑦](07-adoption-roadmap.md) |
| **Variables** | Figmaの変数機能。トークンの源 | [②](02-design-tokens.md) |
| **バリアント** | Figmaコンポーネントの状態違い（Primary/Secondary等） | [③](03-code-connect.md) |

### Code Connect

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **Code Connect** | Figmaノードと実コンポーネントの対応表。**Organization以上** | [③](03-code-connect.md) |
| **`*.figma.tsx`** | Code Connectの定義ファイル | [③](03-code-connect.md) |
| **`figma.connect()`** | 対応付けを宣言する関数 | [③](03-code-connect.md) |
| **`figma.string()`** | Figmaのテキストプロパティを対応付ける | [③](03-code-connect.md) |
| **`figma.boolean()`** | ブールプロパティを対応付ける | [③](03-code-connect.md) |
| **`figma.enum()`** | バリアントを対応付ける | [③](03-code-connect.md) |
| **`figma.instance()`** | インスタンススワップ（アイコン等）を対応付ける | [③](03-code-connect.md) |
| **`figma.children()`** | 子要素を受け取る | [③](03-code-connect.md) |
| **`importPaths`** | 相対パスをエイリアスへ変換する設定。**必須級** | [③](03-code-connect.md) |
| **`figma connect parse`** | Code Connectの整合性を検証。**CIで必須化** | [③](03-code-connect.md) |
| **`figma connect publish`** | Figmaへ公開する | [③](03-code-connect.md) |

### デザイントークン

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **デザイントークン** | 値に名前を付けたもの（`#3B82F6` → `color-primary`） | [②](02-design-tokens.md) |
| **プリミティブトークン** | 原始値（`blue-500`）。ほぼ変わらない | [②](02-design-tokens.md) |
| **セマンティックトークン** | 意味（`color-primary`）。**テーマ切替点** | [②](02-design-tokens.md) |
| **コンポーネントトークン** | 用途特化（`button-bg-primary`） | [②](02-design-tokens.md) |
| **W3C Design Tokens形式** | 標準化されたJSON形式。2025年10月に安定版 | [②](02-design-tokens.md) |
| **Tokens Studio** | Figma VariablesをGitに同期するプラグイン | [②](02-design-tokens.md) |
| **Style Dictionary** | トークンJSONを各形式へ変換するツール | [②](02-design-tokens.md) |
| **`outputReferences`** | 参照関係を保つ設定。**ダークモードに必須** | [②](02-design-tokens.md) |
| **`@theme inline`** | Tailwind v4でCSS変数への参照を保つ記法 | [②](02-design-tokens.md) |
| **任意値記法** | `bg-[#3B82F6]` のような直書き。**禁止対象** | [②](02-design-tokens.md) |

### Git・レビュー

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **GitHub MCP** | GitHub APIをAIに提供するMCPサーバー | [⑥](06-git-github-mcp.md) |
| **ブランチ保護** | mainへの直接pushやマージを制限する設定 | [⑥](06-git-github-mcp.md) |
| **Conventional Commits** | `feat:` `fix:` 等の規約 | [⑥](06-git-github-mcp.md) |
| **CI自動修正** | CI失敗のログを読んでAIが直す運用 | [⑥](06-git-github-mcp.md) |
| **ビジュアル回帰テスト** | スクリーンショット比較で見た目の変化を検出 | [⑤](05-ai-workflow.md) |

---

## 2. 逆引き表 — 困った時どの章？

| やりたいこと・困りごと | 見る章 |
| --- | --- |
| **導入すべきか判断したい** | [① 導入判断](01-overview.md#4-プラン要件--実質的な足切りライン) |
| 何ができて何ができないか知りたい | [① できること/できないこと](01-overview.md#3-できること--できないこと) |
| 費用対効果を見積もりたい | [① 費用対効果](01-overview.md#5-費用対効果をどう見るか) |
| プラン要件を確認したい | [① プラン要件](01-overview.md#4-プラン要件--実質的な足切りライン) |
| セキュリティ観点を整理したい | [① ガバナンス](01-overview.md#7-セキュリティガバナンスの観点) |
| トークンを整備したい | [② デザイントークン](02-design-tokens.md) |
| Figma VariablesをGitに同期したい | [② Tokens Studio](02-design-tokens.md#4-tokens-studio-で-git-に同期する) |
| Tailwindとトークンを繋ぎたい | [② Tailwind v4](02-design-tokens.md#6-tailwind-css-v4-と繋ぐ) |
| **ハードコードを防ぎたい** | [② Lint](02-design-tokens.md#8-ハードコードを検出する) |
| ダークモードで色が変わらない | [② outputReferences](02-design-tokens.md#5-style-dictionary-で変換する) |
| **生成コードの品質を上げたい** | [③ Code Connect](03-code-connect.md) |
| Code Connectの書き方を知りたい | [③ 基本の書き方](03-code-connect.md#4-基本の書き方) |
| バリアントを対応付けたい | [③ プロパティ対応](03-code-connect.md#5-プロパティ対応のパターン) |
| Code ConnectをCIで回したい | [③ CI](03-code-connect.md#7-ciで自動公開する) |
| どのコンポーネントから張るべきか | [③ 優先順位](03-code-connect.md#8-どこから張るか--費用対効果の高い順) |
| Figma MCPを繋ぎたい | [④ 接続](04-figma-mcp.md#3-claude-code-への接続) |
| リモート版/デスクトップ版どちら | [④ 比較](04-figma-mcp.md#2-リモート版とデスクトップ版) |
| 効果的な指示の書き方 | [④ 指示](04-figma-mcp.md#5-効果的な指示の出し方) |
| 生成結果を検証したい | [④ 検証](04-figma-mcp.md#7-検証の方法) |
| **AIが規約を守らない** | [⑤ CLAUDE.md](05-ai-workflow.md#2-claudemd-の設計) |
| 品質を仕組みで担保したい | [⑤ 品質ゲート](05-ai-workflow.md#5-品質ゲート--機械で止める) |
| レビューで何を見るべきか | [⑤ レビュー観点](05-ai-workflow.md#6-人間がレビューで見るべき点) |
| チームの役割分担を決めたい | [⑤ 役割分担](05-ai-workflow.md#8-チームでの役割分担) |
| AI利用コストを下げたい | [⑤ コスト管理](05-ai-workflow.md#9-コスト管理) |
| **git連携にMCPが要るか知りたい** | [⑥ MCP不要の境界](06-git-github-mcp.md#-git操作にmcpは不要) |
| PRを自動作成したい | [⑥ Gitフロー](06-git-github-mcp.md#3-標準的なgitフロー) |
| CI失敗を自動修正したい | [⑥ CI自動修正](06-git-github-mcp.md#5-ci失敗の自動修正) |
| AIの権限をどこまで許すか | [⑥ 権限設計](06-git-github-mcp.md#7-権限設計--どこまでaiに許すか) |
| **どこから始めるべきか** | [⑦ ロードマップ](07-adoption-roadmap.md#2-段階導入ロードマップ) |
| 自分たちの現状を評価したい | [⑦ フェーズ0](07-adoption-roadmap.md#フェーズ0現状評価1日) |
| 失敗パターンを知りたい | [⑦ アンチパターン](07-adoption-roadmap.md#3-アンチパターン集) |
| 品質が出ない原因を切り分けたい | [⑦ 切り分け](07-adoption-roadmap.md#5-トラブル時の切り分けフロー) |
| 導入効果を測りたい | [⑦ 効果測定](07-adoption-roadmap.md#6-効果測定) |

---

## 3. コマンド・チートシート

### Code Connect

```bash
npx figma connect create      # 対話形式で初期設定
npx figma connect parse       # 検証（CIで必須化）
npx figma connect publish     # Figmaへ公開
npx figma connect unpublish   # 公開を取り消し

export FIGMA_ACCESS_TOKEN="figd_..."   # Secretsで管理
```

### デザイントークン

```bash
npx style-dictionary build    # トークンを変換
```

### MCP（Claude Code）

```
/plugin      # プラグイン管理（figma / github を追加）
/mcp         # 接続中のMCPサーバーを確認
```

### 品質チェック

```bash
npm run lint          # ハードコード検出を含む
npx tsc --noEmit      # 型チェック
npm run test          # ユニットテスト
npm run build         # ビルド
npx playwright test   # E2E・ビジュアル回帰
```

---

## 4. 設定ファイルのひな形

### `figma.config.json`

```json
{
  "codeConnect": {
    "include": ["src/components/**/*.figma.tsx"],
    "parser": "react",
    "label": "React",
    "importPaths": { "src/components/*": "@/components/*" }
  }
}
```

### Code Connect（最小）

```tsx
import figma from '@figma/code-connect'
import { Button } from './button'

figma.connect(Button, 'https://figma.com/design/xxx?node-id=1-23', {
  props: {
    label: figma.string('Label'),
    variant: figma.enum('Variant', { Primary: 'primary', Secondary: 'secondary' }),
  },
  example: ({ label, variant }) => <Button variant={variant}>{label}</Button>,
})
```

### `CLAUDE.md`（Figma実装ルールの抜粋）

```markdown
## Figmaからの実装ルール
- components/ui/ の既存コンポーネントを最優先で使う
- 色・余白はトークンのみ（bg-[#xxx] は禁止）
- 既定は Server Component、'use client' は末端のみ
- クリック要素は <button>（<div onClick> 禁止）
- 1PR = 1コンポーネント
- 実装後: npm run lint && npx tsc --noEmit && npm run test && npm run build

## 禁止
- テストを削除・スキップして通すこと
- any / @ts-ignore で型エラーを回避すること
- Figma MCPの出力をそのまま貼り付けること
```

---

## 5. 判断早見表

| 状況 | 判断 |
| --- | --- |
| Professionalプラン | Code Connect不可 → **トークン層のみ導入** |
| Organizationプラン以上 | フル構成が可能 → [⑦](07-adoption-roadmap.md) の順で |
| Figmaが絶対配置だらけ | **まずFigma整理**。MCPは後 |
| デザイナーの協力が得られない | **導入見送りも妥当** |
| 画面が10枚未満 | 費用対効果が薄い |
| デザインシステムがある | ✅ 効果が出やすい |
| git操作をMCPでやろうとしている | **不要**。素のgitでよい |
| 生成コードをそのままコミットしたい | ❌ レビューで落とす |
| 自動マージしたい | ❌ マージは人間 |

---

## 6. 前提バージョン（執筆時点：2026年8月）

| 項目 | バージョン / 状態 |
| --- | --- |
| Figma MCPサーバー | **ベータ**（無料。将来は従量課金予定） |
| Code Connect | Organization プラン以上 |
| `@figma/code-connect` | 1.5 系 |
| `style-dictionary` | 5 系 |
| Tailwind CSS | 4 系 |
| React / Next.js | 19 / 16 系 |
| Node.js | 24 LTS |

> ⚠️ **Figma MCPはベータのため、ツール名・出力形式・課金体系が変わる可能性があります。** 一方、**トークン層（②）とCode Connect（③）はMCPが変わっても資産として残ります。**

---

## 7. 関連シリーズ

- 🔵 [React 完全ガイド](../react/README.md) ← コンポーネント設計・[⑧実践パターン](../react/08-practice-patterns.md)
- ⚫ [Next.js 完全ガイド](../nextjs/README.md) ← [⑦スタイリング](../nextjs/07-styling-ui.md)・[⑬アーキテクチャ](../nextjs/13-architecture-practice.md)
- 🟢 [Node.js 完全ガイド](../nodejs/README.md) ← CI・ビルド環境
- 📖 [JavaScript・Node.js・React・Next.js の関係](../js-stack-relations.md)

---

[← 総合インデックスに戻る](README.md)
