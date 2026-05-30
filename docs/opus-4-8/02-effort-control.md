# 02. Effort(労力)制御

`effort` パラメータは、Claude がリクエストに応答する際にどれだけ「気合いを入れて」トークンを使うかを制御します。**1つのモデルのまま**、応答の徹底度とトークン効率のトレードオフを調整できます。ベータヘッダーは不要です。

## ポイント

- **デフォルトは `high`**(Claude API・Claude Code すべてのサーフェスで)
- `effort: "high"` はパラメータを省略した場合とまったく同じ挙動
- effort は**応答内のすべてのトークン**に影響:テキスト応答、ツール呼び出しと引数、拡張思考(有効時)
- 思考(thinking)を有効にしなくても使える
- ツール呼び出しの回数にも影響(低 effort = ツール呼び出しが減る)

## Effort レベル

| レベル | 説明 | 典型的な用途 |
| --- | --- | --- |
| `max` | 制約なしの最大能力。最も深い推論 | 最も徹底した推論・分析が必要なタスク |
| `xhigh` | 長時間作業向けの拡張能力 | 30分超の長時間エージェント/コーディング(トークン予算が数百万規模) |
| `high` | 高能力。**デフォルト**(未設定と同等) | 複雑な推論、難しいコーディング、エージェント的タスク |
| `medium` | バランス型。中程度のトークン節約 | 速度・コスト・性能のバランスが必要なエージェント的タスク |
| `low` | 最も効率的。大幅なトークン節約(能力は一部低下) | 単純なタスク、サブエージェントなど速度・コスト最優先 |

> effort は厳密なトークン上限ではなく「行動シグナル」です。低 effort でも十分難しい問題には思考しますが、高 effort より思考量は少なくなります。

## Opus 4.8 の推奨設定

- **コーディング・エージェント用途は `xhigh` から始める**
- 知性が重要なその他のワークロードは `high` を最低ラインに
- コスト重視なら、評価(eval)で品質が保てることを確認した上で `medium` / `low` に下げる
- `xhigh` / `max` で実行する場合は、思考・サブエージェント・ツール呼び出しの余地を確保するため `max_tokens` を大きく(目安64kから調整)

## 使用例

### cURL

```bash
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-8",
        "max_tokens": 4096,
        "messages": [{
            "role": "user",
            "content": "マイクロサービスとモノリシックアーキテクチャのトレードオフを分析して"
        }],
        "output_config": {
            "effort": "medium"
        }
    }'
```

### Python

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "マイクロサービスとモノリシックアーキテクチャのトレードオフを分析して",
        }
    ],
    output_config={"effort": "medium"},  # ← ここで effort を指定
)

print(response.content[0].text)
```

### TypeScript

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content: "マイクロサービスとモノリシックアーキテクチャのトレードオフを分析して"
    }
  ],
  output_config: {
    effort: "medium"  // "low" | "medium" | "high" | "xhigh" | "max"
  }
});
```

## ツール使用時の effort の効き方

| 低 effort | 高 effort |
| --- | --- |
| 複数操作を少ないツール呼び出しにまとめる | ツール呼び出しが増える |
| 前置きなしですぐ行動 | 行動前に計画を説明 |
| 完了後は簡潔な確認のみ | 変更内容を詳しく要約 |
| — | コードコメントも充実 |

## 拡張思考(thinking)との関係

Opus 4.8 は**適応的思考(adaptive thinking)**を使います。

- 手動の拡張思考 `thinking: {"type": "enabled", "budget_tokens": N}` は **400エラー**(非対応)
- 思考を有効にするには `thinking: {"type": "adaptive"}` を指定(指定しなければ思考なしで実行)
- `high` / `xhigh` / `max` ではほぼ常に深く思考。低レベルでは単純な問題で思考を省略することがある

```python
# 旧(Opus 4.6 以前)
thinking = {"type": "enabled", "budget_tokens": 32000}

# 新(Opus 4.7 以降)
thinking = {"type": "adaptive"}
output_config = {"effort": "high"}
```

## Claude Code の「ultracode」モードについて

Claude Code の effort メニューに表示される `ultracode` は、API の追加 effort レベルではありません。`xhigh` effort に加えて、マルチエージェントワークフローを自動起動する常設パーミッションを([会話途中のシステムメッセージ](./04-mid-conversation-system-messages.md)経由で)付与したものです。API がそのまま受け付ける effort 値は `low` / `medium` / `high` / `xhigh` / `max` の5種類です。

## 注意:サンプリングパラメータ非対応

Opus 4.7 と同様、`temperature` / `top_p` / `top_k` を非デフォルト値に設定すると **400エラー**になります。これらは省略し、プロンプトで挙動を誘導してください。

## 出典

- [Effort — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/effort)
- [What's new in Claude Opus 4.8 — Claude API Docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)
