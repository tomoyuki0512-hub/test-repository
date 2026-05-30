# 01. 概要・ベンチマーク・価格

## モデル概要

**Claude Opus 4.8** は、2026年5月28日にリリースされた Anthropic の一般提供モデルとして最も高性能なモデルです。Claude Opus 4.7 をベースに、複雑な推論、長時間にわたるエージェント的コーディング、高い自律性が求められる作業に最適化されています。

| 項目 | 内容 |
| --- | --- |
| API モデル ID | `claude-opus-4-8` |
| コンテキストウィンドウ | 1M トークン(Claude API / Amazon Bedrock / Vertex AI。Microsoft Foundry は 200k) |
| 最大出力トークン | 128k |
| 思考モード | 適応的思考(adaptive thinking) |
| ツール・プラットフォーム機能 | Opus 4.7 と同じセットに対応 |
| リリース日 | 2026年5月28日(Opus 4.7 の41日後) |

## 主な改善点

Opus 4.7 と比較して、以下の点が向上しています。

- **長時間のエージェント的コーディング**:長いコンテキストの扱いが改善し、コンパクション(文脈圧縮)の発生回数が減少。コンパクション後の復帰も向上
- **推論労力(effort)のキャリブレーション**:各 effort レベルでの挙動がより安定
- **ツール起動(tool triggering)**:タスクに必要なツール呼び出しをスキップしてしまうケースが減少
- **正直さ・欺瞞の少なさ**:進捗について正直になり、根拠のない主張をしにくくなった。不確実性を自分から申告しやすくなった

## ベンチマーク(対 Opus 4.7)

| 指標 | Opus 4.7 | Opus 4.8 |
| --- | --- | --- |
| エージェント的コーディング | 64.3% | **69.2%** |
| ツール併用の多分野推論 | 54.7% | **57.9%** |
| 自分が生成したコードの欠陥を見逃す確率 | 基準 | **約4分の1に減少** |

## 価格

- **据え置き**:Opus 4.7 と Opus 4.8 の標準価格は同一です。
- Fast mode(高速モード)については [03. Fast mode](./03-fast-mode.md) を参照。Opus 4.8 の Fast mode は従来モデルの約3分の1の価格になりました。

## 提供状況

- Claude API、Amazon Bedrock、Vertex AI、Microsoft Foundry で利用可能(機能により一部制約あり)
- Claude アプリ、Claude Code でも利用可能
- GitHub Copilot でも一般提供
- 一部機能(Fast mode、Dynamic Workflows)はリサーチプレビュー

## 出典

- [Introducing Claude Opus 4.8 — Anthropic](https://www.anthropic.com/news/claude-opus-4-8)
- [What's new in Claude Opus 4.8 — Claude API Docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)
- [Anthropic debuts flagship Claude Opus 4.8 — Yahoo Finance](https://finance.yahoo.com/news/anthropic-debuts-flagship-claude-opus-48-ai-model-as-ipo-race-with-openai-heats-up-170000527.html)
- [Claude Opus 4.8 is generally available for GitHub Copilot — GitHub Changelog](https://github.blog/changelog/2026-05-28-claude-opus-4-8-is-generally-available-for-github-copilot/)
