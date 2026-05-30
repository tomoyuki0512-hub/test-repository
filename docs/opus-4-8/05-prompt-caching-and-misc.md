# 05. プロンプトキャッシュの最小トークン低下・その他の変更

## プロンプトキャッシュの最小トークン低下

Opus 4.8 でキャッシュ可能なプロンプトの**最小長は 1,024 トークン**に下がりました(Opus 4.7 より低い)。

- Opus 4.7 では短すぎてキャッシュできなかったプロンプトも、**コード変更なしで**キャッシュエントリを作れるようになった
- 短いシステムプロンプトや小さめの会話でもキャッシュの恩恵を受けやすくなる

> なお、キャッシュは `cache_control` を指定したときのみ有効になります。指定がなければ何もキャッシュされず、毎回フルの入力トークン料金がかかります。

## 拒否時の詳細(Refusal stop details)

拒否レスポンスに付く `stop_details` オブジェクトが公式にドキュメント化されました(機能自体は Opus 4.7 から存在)。ベータヘッダーは不要です。

- Claude がリクエストを拒否した際、既存の `refusal` という stop reason に加えて、**拒否のカテゴリ**を `stop_details` が示す
- アプリ側で拒否の種類を区別し、ユーザーを適切な次のステップへ誘導しやすくなる

## Effort のデフォルトは high

`effort` パラメータのデフォルトは、Claude API・Claude Code を含む**すべてのサーフェスで `high`**。明示的に設定している場合は変わりません。詳細は [02. Effort 制御](./02-effort-control.md) を参照。

## 適応的思考(Adaptive thinking)

Opus 4.8 は適応的思考を採用し、**そのターンに思考が必要かをモデル自身が判断**します。

- 単純な検索や短いエージェントステップでは直接応答
- 複雑な多段階問題では応答前に推論
- 同じ effort レベルでも、Opus 4.7 に比べて**無駄な思考トークンが削減**(bimodal なワークロードで顕著)
- 思考はデフォルトでオフ。`thinking: {type: "adaptive"}` を明示しない限り思考しない

## Opus 4.7 から引き継いだ API 制約

Opus 4.7 から変わらないため、すでに Opus 4.7 で動くコードは変更不要です(Messages API のみ。Claude Managed Agents は対象外)。

### サンプリングパラメータ非対応

`temperature` / `top_p` / `top_k` を非デフォルト値に設定すると **400 エラー**。これらは省略し、プロンプトで挙動を誘導します。

### 適応的思考が唯一の思考モード

拡張思考の予算指定 `thinking: {"type": "enabled", "budget_tokens": N}` は **400 エラー**。適応的思考と `effort` で思考の深さを制御します。

```python
# 旧(Opus 4.6 以前)
thinking = {"type": "enabled", "budget_tokens": 32000}

# 新(Opus 4.7 以降 / Opus 4.8)
thinking = {"type": "adaptive"}
output_config = {"effort": "high"}
```

## 挙動の変化(破壊的変更ではないがプロンプト調整が必要な場合あり)

- **無駄な思考トークンの削減**:適応的思考有効時、ターンごとに思考要否を判断するため
- **ツール起動の改善**:タスクに必要なツール呼び出しをスキップしにくくなった(Opus 4.7 で一部ユーザーが報告していた問題)
- **コンパクション処理と長文脈品質の向上**:長いエージェントトレースでも、コンパクション後の脱線が減少

## 移行について

Claude Code や Agent SDK を使っている場合、[Claude API skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill) がこれらの移行手順をコードベースに自動適用できます。

## 出典

- [What's new in Claude Opus 4.8 — Claude API Docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)
- [Prompt caching — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Adaptive thinking — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)
- [Handling stop reasons — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
