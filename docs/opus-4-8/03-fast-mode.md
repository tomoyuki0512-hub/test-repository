# 03. Fast mode(高速モード)

Fast mode は、**同じモデル**をより高速な推論構成で実行する機能です。`speed: "fast"` を指定すると、標準速度に比べて**出力トークン毎秒(OTPS)が最大2.5倍**になります。知性・能力に変化はありません。

> **リサーチプレビュー**です。利用にはアカウントマネージャーへの依頼、または [waitlist](https://claude.com/fast-mode) への登録が必要です。

## ポイント

- 速度向上は **出力速度(OTPS)** に対するもので、**最初のトークンまでの時間(TTFT)** は対象外
- 同じモデルの重み・挙動(別モデルではない)
- ベータヘッダー `anthropic-beta: fast-mode-2026-02-01` が必要
- 対応モデル:`claude-opus-4-8`、`claude-opus-4-7`、`claude-opus-4-6`
  - Opus 4.6 の Fast mode は Opus 4.8 リリースとともに非推奨(約30日後に削除)。削除後は標準速度・標準価格にフォールバック
- Opus 4.8 の Fast mode は Claude API(Claude Managed Agents を含む)**のみ**。Vertex AI / Bedrock / Microsoft Foundry では非対応

## 価格(標準レートへの倍率)

| モデル | Input | Output |
| --- | --- | --- |
| Opus 4.6 / Opus 4.7 | $30 / MTok | $150 / MTok |
| **Opus 4.8** | **$10 / MTok** | **$50 / MTok** |

Opus 4.8 では従来モデルの約3分の1の価格になりました。プロンプトキャッシュ倍率やデータレジデンシー倍率は Fast mode 価格の上に積算されます。

## 使用例

### cURL

```bash
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: fast-mode-2026-02-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-8",
        "max_tokens": 4096,
        "speed": "fast",
        "messages": [{
            "role": "user",
            "content": "このモジュールを依存性注入を使うようリファクタして"
        }]
    }'
```

### Python

```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    speed="fast",                          # ← 高速モードを有効化
    betas=["fast-mode-2026-02-01"],        # ← 必須のベータ指定
    messages=[
        {"role": "user", "content": "このモジュールを依存性注入を使うようリファクタして"}
    ],
)

print(response.content[0].text)
```

### TypeScript

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 4096,
  speed: "fast",
  betas: ["fast-mode-2026-02-01"],
  messages: [
    { role: "user", content: "このモジュールを依存性注入を使うようリファクタして" }
  ]
});
```

## どの速度で処理されたか確認する

レスポンスの `usage.speed` に `"fast"` または `"standard"` が入ります。

```python
response = client.beta.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    speed="fast",
    betas=["fast-mode-2026-02-01"],
    messages=[{"role": "user", "content": "Hello"}],
)

print(response.usage.speed)  # "fast" または "standard"
```

```json
{
  "usage": {
    "input_tokens": 8,
    "output_tokens": 12,
    "speed": "fast"
  }
}
```

## レート制限とフォールバック

- Fast mode には**標準 Opus とは別枠のレート制限**がある
- 上限超過時は `429` と `retry-after` ヘッダーが返る。SDK は既定で最大2回まで自動リトライ(`max_retries` で調整可)
- レスポンスヘッダー(例):`anthropic-fast-output-tokens-remaining`、`anthropic-fast-output-tokens-reset` など
- 待たずに標準速度へ切り替えたい場合は、`429` を捕捉して `speed: "fast"` なしで再リクエスト

```python
import anthropic

client = anthropic.Anthropic()

def create_with_fallback(**params):
    try:
        # 初回リクエストの自動リトライを無効化して即座にフォールバック
        return client.with_options(max_retries=0).beta.messages.create(**params)
    except anthropic.RateLimitError:
        if params.get("speed") == "fast":
            del params["speed"]                 # 標準速度で再試行
            return create_with_fallback(**params)
        raise

message = create_with_fallback(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
    betas=["fast-mode-2026-02-01"],
    speed="fast",
)
```

> Fast ↔ Standard を切り替えるとプロンプトキャッシュは**ミス**します(速度違いはキャッシュ済みプレフィックスを共有しない)。

## 制約

- **Batch API** では利用不可
- **Priority Tier** では利用不可
- **Claude Platform on AWS** では現状利用不可
- 非対応モデルに `speed: "fast"` を送るとエラー

## Claude Code での Fast mode

Claude Code では `/fast` コマンドでトグルできます。Opus 4.8 / 4.7 / 4.6 で利用可能で、小型モデルへのダウングレードではなく、Opus のまま出力が高速になります。

## 出典

- [Fast mode — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/fast-mode)
- [What's new in Claude Opus 4.8 — Claude API Docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)
