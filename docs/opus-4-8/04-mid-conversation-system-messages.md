# 04. 会話途中のシステムメッセージ(Mid-conversation system messages)

会話の途中で**システム指示を追加・更新**しても、その前のキャッシュ済みプレフィックスを壊さない機能です。**Opus 4.8 のみ**で利用可能で、ベータヘッダーは不要です。

## 何が嬉しいのか

通常、システム指示はトップレベルの `system` フィールドに置きます。これはプロンプトキャッシュには好都合ですが、**セッション途中で必要になった指示**には不向きです。`system` を編集するとプロンプトの先頭が変わり、以降すべてのキャッシュが無効化されてしまうためです。

この機能では、新しい指示が必要になった地点で `messages` 配列に `{"role": "system"}` メッセージを**末尾に追記**します。

- キャッシュ済みプレフィックスは変わらない → 次のリクエストでもキャッシュヒット
- 追記した指示は「ただのユーザーテキスト」ではなく**システム指示としての優先度**で適用される

## 典型的なユースケース

- **セッション途中のポリシー/ペルソナ変更**:「以降、SQL はすべてパラメータ化クエリで書く」など、数十ターン後の新制約
- **権威を持たせたいターン単位の文脈**:鮮度メモ、セッション期限、ツール可用性の変化など
- **ツール結果で挙動を変える**:「この顧客はエンタープライズプラン。コンシューマー向けアップグレード導線は提案しない」など
- **モード切替で常設権限を付与**:高コストな機能(マルチエージェント自動起動など)への同意を、数ターンごとのリフレッシュ付きで付与

## 仕組みと配置ルール

- `messages` 配列に `"role": "system"` のメッセージを追加。`content` は文字列でもコンテンツブロックでも可
- 指示はその地点以降に適用される
- 指示が競合する場合、**後のシステムメッセージが先のものに優先**。会話途中のシステムメッセージはトップレベル `system` より優先(以降のターンについて)

### 制約(違反すると 400 エラー)

- **最初のメッセージにはできない**:`messages` の先頭に置けない。会話全体に効かせたい指示はトップレベル `system` を使う
- **配置が限定**:`system` メッセージは `user` ターン(またはサーバーツール使用で終わる `assistant` ターン)の**直後**に置き、かつ `assistant` ターンが続くか配列の末尾でなければならない。実際には**最新の `user` ターンの後、配列末尾に追記**するのが定石
- **連続したシステムメッセージは不可**:指示は1つにまとめるか、次の `user` ターンを待って追記する
- **送信済みのシステムメッセージは編集・削除しない**:キャッシュが無効化される。指示を変えたいときは新しいシステムメッセージを追記する
- **セキュリティ境界ではない**:システム優先度は与えるが、信頼できないコンテンツを信頼できるものにはしない

## 使用例

### cURL

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "cache_control": {"type": "ephemeral"},
    "system": "あなたはコードレビューアシスタントです。簡潔に。",
    "messages": [
      { "role": "user", "content": "utils.py の process() の性能問題をレビューして。" },
      { "role": "assistant", "content": "小さい入力ならリスト内包表記で問題ありません。大きい入力ではジェネレータの利用を検討してください。" },
      { "role": "user", "content": "次に process() を呼んでいる側のコードをレビューして。" },
      { "role": "system", "content": "今後、すべての提案に明示的な型注釈を含めること。" }
    ]
  }'
```

### Python

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    # 自動プロンプトキャッシュ:各リクエストでそこまでの会話をキャッシュし、
    # 次のリクエストは変更のないプレフィックスをキャッシュから読む
    cache_control={"type": "ephemeral"},
    system="あなたはコードレビューアシスタントです。簡潔に。",
    messages=[
        {"role": "user", "content": "utils.py の process() の性能問題をレビューして。"},
        {"role": "assistant", "content": "小さい入力ならリスト内包表記で問題ありません。大きい入力ではジェネレータの利用を検討してください。"},
        {"role": "user", "content": "次に process() を呼んでいる側のコードをレビューして。"},
        # レビュー中に「全提案がチームの厳格な型付けポリシーを満たす必要がある」と気づいた。
        # ここに追記すれば前のターンはバイト単位で不変のままなので、
        # 直前のリクエストがキャッシュしたプレフィックスを引き続き再利用できる。
        {"role": "system", "content": "今後、すべての提案に明示的な型注釈を含めること。"},
    ],
)

print(response.content[0].text)
```

### TypeScript

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  cache_control: { type: "ephemeral" },
  system: "あなたはコードレビューアシスタントです。簡潔に。",
  messages: [
    { role: "user", content: "utils.py の process() の性能問題をレビューして。" },
    { role: "assistant", content: "小さい入力ならリスト内包表記で問題ありません。大きい入力ではジェネレータの利用を検討してください。" },
    { role: "user", content: "次に process() を呼んでいる側のコードをレビューして。" },
    // 末尾に system を追記してキャッシュを維持
    { role: "system", content: "今後、すべての提案に明示的な型注釈を含めること。" }
  ]
});
```

## プロンプトキャッシュとの組み合わせ

- **キャッシュは明示的に有効化**:`cache_control`(自動キャッシュ or 明示的ブレークポイント)が必要。会話途中のシステムメッセージ単体ではキャッシュエントリは作られない
- **安定プレフィックスを通常通りキャッシュ**:リクエスト間で変わらない最後のブロックに `cache_control` を置く
- **ブレークポイントの後にシステムメッセージを追記**:プレフィックスのハッシュが変わらないのでキャッシュヒットする
- **追記したシステムメッセージ自体もキャッシュ可能**:一度会話に入れば安定した履歴の一部になり、次ターン以降はキャッシュから読まれる

## 提供範囲

- Claude API および Claude Platform on AWS で利用可能
- Amazon Bedrock / Vertex AI / Microsoft Foundry では非対応

## 出典

- [Mid-conversation system messages — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages)
- [What's new in Claude Opus 4.8 — Claude API Docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)
