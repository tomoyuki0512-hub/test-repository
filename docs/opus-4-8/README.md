# Claude Opus 4.8 新機能まとめ

2026年5月28日にリリースされた **Claude Opus 4.8**(API モデル ID: `claude-opus-4-8`)の新機能を、使い方の例とともにまとめたドキュメント集です。Opus 4.7 のわずか41日後にリリースされた、Anthropic の一般提供モデルとして最も高性能なモデルです。

## ドキュメント一覧

| # | ファイル | 内容 |
| --- | --- | --- |
| 01 | [概要・ベンチマーク・価格](./01-overview.md) | モデル概要、性能向上、価格、提供状況 |
| 02 | [Effort(労力)制御](./02-effort-control.md) | `effort` パラメータで思考量・トークン消費を制御 |
| 03 | [Fast mode(高速モード)](./03-fast-mode.md) | `speed: "fast"` で最大2.5倍の出力速度 |
| 04 | [会話途中のシステムメッセージ](./04-mid-conversation-system-messages.md) | キャッシュを壊さず途中で指示を追加 |
| 05 | [プロンプトキャッシュ・その他](./05-prompt-caching-and-misc.md) | キャッシュ最小トークン低下、拒否理由詳細、適応的思考 |
| 06 | [Dynamic Workflows(Claude Code)](./06-dynamic-workflows.md) | 大規模並列サブエージェントによる自律実行 |

## 新機能ハイライト

- **Effort 制御**:1つのモデルで思考の深さ・トークン消費を `low`〜`max` で調整(`xhigh` も対応)
- **Fast mode**:同じモデルを最大2.5倍速で実行(リサーチプレビュー)。Opus 4.8 では従来の3分の1の価格に
- **会話途中のシステムメッセージ**:`messages` 配列内に `role: "system"` を追加でき、キャッシュを維持したまま指示を更新可能
- **プロンプトキャッシュ最小トークンの低下**:1,024トークンから(Opus 4.7 より小さく)キャッシュ可能に
- **Dynamic Workflows**:Claude Code で最大1,000個のサブエージェントを使った大規模タスク実行(リサーチプレビュー)
- **より正直で、欺瞞が少ない**:進捗について正直になり、コードの欠陥を見逃す確率が約4分の1に

## 主要スペック

| 項目 | 内容 |
| --- | --- |
| API モデル ID | `claude-opus-4-8` |
| コンテキストウィンドウ | 1M トークン(Claude API / Bedrock / Vertex AI。Microsoft Foundry は 200k) |
| 最大出力トークン | 128k |
| 思考モード | 適応的思考(adaptive thinking) |
| 価格 | Opus 4.7 と同額(据え置き) |
| リリース日 | 2026年5月28日 |

## 出典

- [Introducing Claude Opus 4.8 — Anthropic](https://www.anthropic.com/news/claude-opus-4-8)
- [What's new in Claude Opus 4.8 — Claude API Docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)
- [Anthropic releases Opus 4.8 with new 'dynamic workflow' tool — TechCrunch](https://techcrunch.com/2026/05/28/anthropic-releases-opus-4-8-with-new-dynamic-workflow-tool/)
