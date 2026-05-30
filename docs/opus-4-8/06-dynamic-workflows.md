# 06. Dynamic Workflows(Claude Code)

**Dynamic Workflows** は、Claude Code 上で Opus 4.8 がさらに大きなタスクを扱えるようにする新機能です(**リサーチプレビュー**)。最大1,000個の並列サブエージェントをオーケストレーションし、数十万行規模のコードベースの移行を、着手からマージまで自律的に実行できます。

## 概要

- **ダイナミックワークフローは、サブエージェントを大規模にオーケストレーションする JavaScript スクリプト**です
- あなたが説明したタスクに対して **Claude がそのスクリプトを書き**、ランタイムがバックグラウンドで実行する
- Claude はプロンプトから動的に計画を立て、タスクをサブタスクに分解
- サブエージェントが**並列**かつ独立した観点から問題に取り組む
- 別のエージェントがその結果に**反証を試み**、回答が収束するまで反復
- 結果は**検証された上で**ユーザーに届く

## 制限・要件

| 項目 | 内容 |
| --- | --- |
| 同時実行エージェント数 | 最大 **16** |
| 1ラン合計のエージェント数 | 最大 **1,000** |
| 必要バージョン | Claude Code **v2.1.154 以降** |
| 実行環境 | CLI、デスクトップアプリ、VS Code 拡張 |
| 対象プラン | Max / Team / Enterprise |
| ステータス | リサーチプレビュー |

## 代表的なユースケース

- **コードベース規模の移行**:数十万行に及ぶフレームワーク/言語/API の移行を、既存のテストスイートを合格基準として実行
- **大規模リファクタリング**:多数のファイルにまたがる横断的変更
- **大規模な調査・検証**:多数のサブエージェントで多角的に調査し、相互に反証して結論を収束させる

## 使い方(イメージ)

Dynamic Workflows はリサーチプレビュー段階のため、まずは前提を整えます。

1. **Claude Code を v2.1.154 以降に更新**する
2. **Opus 4.8 を選択**する(高自律タスク向けに `xhigh` 以上の effort を推奨)
3. Claude Code で**大規模タスクを自然言語で依頼**する。例:

   ```
   このリポジトリ全体を React のクラスコンポーネントから
   関数コンポーネント+Hooks へ移行して。
   既存のテストスイートが全部パスすることを完了の基準にして。
   ```

4. Claude がタスクを分解し、**ダイナミックワークフロー(JavaScript スクリプト)を生成**。ランタイムがサブエージェントを並列起動してバックグラウンド実行する
5. サブエージェントの成果は相互の反証・**テストスイートによる検証**を経て統合され、最終的にマージ候補としてまとまる

> Dynamic Workflows は「着手からマージまで(from kickoff to merge)」を、既存テストを品質のバーとして自律的に進める点が特徴です。大規模変更では、テストカバレッジが結果の品質を左右します。

## effort との関係(ultracode)

Claude Code の effort メニューにある `ultracode` は、`xhigh` effort に加えてマルチエージェントワークフローの自動起動権限を付与したモードです(詳細は [02. Effort 制御](./02-effort-control.md))。Dynamic Workflows のような大規模並列実行と相性が良い設定です。

## 出典

- [Anthropic releases Opus 4.8 with new 'dynamic workflow' tool — TechCrunch](https://techcrunch.com/2026/05/28/anthropic-releases-opus-4-8-with-new-dynamic-workflow-tool/)
- [Anthropic Ships Claude Opus 4.8 Alongside Dynamic Workflows … Capped at 1,000 Subagents — MarkTechPost](https://www.marktechpost.com/2026/05/28/anthropic-ships-claude-opus-4-8-alongside-dynamic-workflows-and-cheaper-fast-mode-with-workflows-capped-at-1000-subagents/)
- [Introducing Claude Opus 4.8 — Anthropic](https://www.anthropic.com/news/claude-opus-4-8)
- [Claude Opus 4.8 launches today with agentic improvements — 9to5Google](https://9to5google.com/2026/05/28/claude-opus-4-8-launches-today-with-agentic-improvements-new-features/)
