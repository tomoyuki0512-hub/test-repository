---
title: ② イベントループと非同期
---

# ② イベントループと非同期 — Node.jsの核心

[← 総合インデックスに戻る](README.md) ｜ 前 → [① Node.jsとは何か](01-what-is-nodejs.md) ｜ 次 → [③ モジュールとnpm](03-modules-packages.md)

**この章がNode.jsシリーズで最も重要です。** 「なぜこの順番で実行されるのか」「なぜサーバーが固まるのか」の答えがすべてここにあります。

---

## 1. シングルスレッドとは

**Node.jsはJavaScriptを1本の流れでしか実行しません。** 同時に2つの処理は走りません。

```
❌ よくある誤解：「非同期＝並列に実行される」
✅ 実際       ：「非同期＝待ち時間に他の仕事をする」
```

### たとえ話：一人で回すラーメン店

```
👨‍🍳 店員は1人（シングルスレッド）

❌ 同期的なやり方
   客A: 注文 → 麺を茹でる3分間、じっと待つ → 提供
   客B: ← 3分間何もされず待たされる
   客C: ← 同上

✅ Node.jsのやり方（非同期）
   客A: 注文 → 麺を茹で器に入れる（タイマーを仕掛ける）
   客B: 注文を受ける → 麺を茹で器へ
   客C: 注文を受ける → 麺を茹で器へ
   （タイマーが鳴る）→ 客Aの麺を提供
   → 一人でも大量に捌ける
```

**重要**：店員が増えたわけではありません。「**待つ作業を他人（OS・libuv）に任せて、自分は次の注文を取る**」という仕組みです。

---

## 2. イベントループの仕組み

「終わった仕事」を順番に拾って処理する司令塔が **イベントループ** です。

```
        ┌───────────────────────────┐
        │  コールスタック            │  ← 今実行中のJS（1本だけ）
        └───────────────────────────┘
                    ↑
                    │ スタックが空になったら取り出す
                    │
        ┌───────────────────────────┐
        │  マイクロタスクキュー      │  ← 優先度：高
        │  Promise.then / await の続き│
        └───────────────────────────┘
                    ↑
        ┌───────────────────────────┐
        │  マクロタスクキュー        │  ← 優先度：低
        │  setTimeout / I/O完了      │
        └───────────────────────────┘
```

### 処理の順序ルール

```
1. 同期コードを最後まで実行する
2. マイクロタスク（Promise）を「空になるまで」全部処理する
3. マクロタスク（setTimeout等）を1つ処理する
4. → 2に戻る
```

> 🔑 **最重要ルール**：**マイクロタスクはマクロタスクより必ず先**。しかも「空になるまで全部」処理されます。

---

## 3. 実行順序の実例

```js
console.log('1: 同期')

setTimeout(() => console.log('2: setTimeout'), 0)

Promise.resolve().then(() => console.log('3: Promise'))

queueMicrotask(() => console.log('4: microtask'))

process.nextTick(() => console.log('5: nextTick'))

console.log('6: 同期')
```

**出力**：

```
1: 同期
6: 同期
5: nextTick        ← 最優先
3: Promise         ← マイクロタスク
4: microtask       ← マイクロタスク
2: setTimeout      ← マクロタスク（最後）
```

### なぜこの順番か

```
① 同期コードを全部実行        → 「1」「6」
② nextTickキューを処理        → 「5」（Node.js固有・最優先）
③ マイクロタスクを全部処理     → 「3」「4」
④ マクロタスクを処理          → 「2」
```

> ⚠️ **`setTimeout(fn, 0)` は「今すぐ」ではありません。** 「同期コードとマイクロタスクを全部終えた後」です。この誤解はバグの原因になります。

### async/await との関係

```js
async function main() {
  console.log('A')
  await null              // ここで一旦中断し、続きはマイクロタスクへ
  console.log('C')        // ← マイクロタスクとして実行される
}

console.log('start')
main()
console.log('B')

// 出力: start → A → B → C
```

**`await` の後ろのコードは、マイクロタスクとして後回しになります。** `await` は「そこで止まる」のではなく「**残りを予約して、一旦呼び出し元に処理を返す**」動作です。

---

## 4. 🚨 イベントループを止めてはいけない

Node.jsで最も重大な事故のパターンです。

```js
// 🚨 これをやると、サーバー全体が5秒間停止する
app.get('/heavy', (req, res) => {
  let sum = 0
  for (let i = 0; i < 10_000_000_000; i++) {   // 重いループ
    sum += i
  }
  res.json({ sum })
})
```

```
リクエストA: /heavy を実行中（5秒）
リクエストB: ← 待たされる（応答なし）
リクエストC: ← 待たされる
ヘルスチェック: ← 応答なし → 「サーバーが死んだ」と判定される
```

**1人のユーザーの重い処理が、全ユーザーに影響します。** これがシングルスレッドの代償です。

### ブロッキングを起こす典型例

| 危険なコード | 代わりに |
| --- | --- |
| `fs.readFileSync()` | `await fs.promises.readFile()` |
| `JSON.parse(巨大な文字列)` | ストリーム処理・分割 |
| 巨大配列の `sort()` / `filter()` | DB側で処理する・ページング |
| 同期的な暗号処理（`pbkdf2Sync`） | 非同期版（`pbkdf2`）を使う |
| 正規表現のバックトラッキング爆発 | 正規表現を見直す（ReDoS対策） |
| 長いループ | `worker_threads` / ジョブキュー |

### 検知する方法

```js
// イベントループの遅延を計測する
import { monitorEventLoopDelay } from 'node:perf_hooks'

const h = monitorEventLoopDelay({ resolution: 20 })
h.enable()

setInterval(() => {
  console.log('遅延の最大値:', h.max / 1e6, 'ms')   // 100msを超えたら要注意
  h.reset()
}, 10_000)
```

### 重い処理の逃がし方

```js
// ① worker_threads で別スレッドへ
import { Worker } from 'node:worker_threads'

const worker = new Worker('./heavy-task.js', { workerData: { input } })
worker.on('message', (result) => res.json(result))

// ② ジョブキューに投げて非同期処理（BullMQ等）
await queue.add('image-resize', { fileId })
res.status(202).json({ status: 'processing' })   // 「受け付けました」だけ返す

// ③ 処理を分割してイベントループに制御を返す
for (const chunk of chunks) {
  await processChunk(chunk)
  await new Promise((r) => setImmediate(r))   // 他の処理に順番を譲る
}
```

---

## 5. 非同期処理の3世代

Node.jsの歴史上、3つの書き方があります。**新規では async/await だけ使えば十分**ですが、古いコードを読むために知っておきます。

### 第1世代：コールバック（2009〜）

```js
fs.readFile('a.txt', (err, data) => {
  if (err) return handleError(err)
  fs.readFile('b.txt', (err, data2) => {
    if (err) return handleError(err)
    fs.writeFile('c.txt', data + data2, (err) => {
      if (err) return handleError(err)
      console.log('完了')
    })
  })
})
```

ネストが深くなる **「コールバック地獄」** が問題でした。

> 💡 **エラーファーストコールバック**：Node.jsの慣習で、コールバックの第1引数は必ずエラーです（`(err, data) => {}`）。古いAPIを使うときに知っておくと読めます。

### 第2世代：Promise（2015〜）

```js
fs.promises.readFile('a.txt')
  .then((data) => fs.promises.readFile('b.txt').then((d2) => data + d2))
  .then((content) => fs.promises.writeFile('c.txt', content))
  .then(() => console.log('完了'))
  .catch(handleError)
```

ネストは解消しましたが、まだ読みにくさが残ります。

### 第3世代：async/await（2017〜、現在の標準）

```js
try {
  const [a, b] = await Promise.all([
    fs.promises.readFile('a.txt'),
    fs.promises.readFile('b.txt'),
  ])
  await fs.promises.writeFile('c.txt', a + b)
  console.log('完了')
} catch (err) {
  handleError(err)
}
```

**同期コードのように読める**のが最大の利点です。詳しくは [⑤ 非同期処理を書きこなす](05-async-patterns.md)。

---

## 6. Node.js は本当にシングルスレッドか

**厳密には「JavaScriptの実行が1本」なだけ**です。裏では複数スレッドが動いています。

```
┌──────────────────────────────────┐
│ メインスレッド                    │
│  └ JavaScriptの実行（1本）        │  ← ここが詰まると全部止まる
├──────────────────────────────────┤
│ スレッドプール（既定4本 / libuv） │
│  └ ファイルI/O・DNS・暗号処理など  │  ← 裏で並列に動いている
└──────────────────────────────────┘
```

だから `fs.readFile`（非同期版）を10個同時に呼んでも、ある程度は並列に処理されます。

```bash
# スレッドプールのサイズは変更できる
UV_THREADPOOL_SIZE=8 node app.js
```

> 💡 ただし**ネットワークI/O**（HTTPリクエストやDB接続）はスレッドプールを使わず、OSのイベント通知機構（epoll等）を直接使うため、この制限を受けません。

---

## 7. 複数コアを活用する

シングルスレッドなので、**そのままではCPUのコアを1つしか使えません**。本番では複数プロセスを立てます。

| 方法 | 特徴 |
| --- | --- |
| **`cluster` モジュール** | Node.js標準。マスターが子プロセスを管理 |
| **PM2** | 定番のプロセスマネージャ。再起動・ログ管理込み |
| **コンテナを複数起動** | Kubernetes / ECS でスケール。**現代の主流** |

```js
// cluster の例
import cluster from 'node:cluster'
import { availableParallelism } from 'node:os'

if (cluster.isPrimary) {
  for (let i = 0; i < availableParallelism(); i++) cluster.fork()
  cluster.on('exit', () => cluster.fork())   // 落ちたら再起動
} else {
  startServer()
}
```

> 💡 **クラウド環境（Vercel・Cloud Run・ECS）では、`cluster` を使わずコンテナを増やすほうが一般的**です。プロセス管理はプラットフォームに任せ、アプリは1プロセスに集中させます。

---

## 8. よくあるつまずき

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| `setTimeout(fn, 0)` が期待より遅い | マイクロタスクが先に処理される | 仕様通り。順序を理解する |
| サーバーが応答しなくなる | 同期処理でブロック | 非同期版を使う・workerへ逃がす |
| ループ内の `await` が遅い | 直列実行になっている | `Promise.all`（→ [⑤](05-async-patterns.md)） |
| `forEach` 内の `await` が効かない | `forEach` は非同期を待たない | `for...of` を使う |
| CPU使用率が100%に張り付く | 重い同期処理 | イベントループ遅延を計測 |
| メモリが増え続ける | リスナー登録の解除漏れ | `removeListener` / `AbortController` |

### `forEach` の罠

```js
// ❌ awaitが無視され、完了前に次へ進む
items.forEach(async (item) => {
  await save(item)
})
console.log('完了')   // まだ保存されていない

// ✅ for...of なら待つ（直列）
for (const item of items) {
  await save(item)
}

// ✅ 並列にするなら Promise.all
await Promise.all(items.map((item) => save(item)))
```

---

## 9. この章のまとめ

- **Node.jsのJS実行は1本（シングルスレッド）**。非同期は「並列」ではなく「待ち時間の有効活用」
- イベントループの順序は **同期 → nextTick → マイクロタスク（Promise）→ マクロタスク（setTimeout）**
- **`setTimeout(fn, 0)` は「今すぐ」ではない**。`await` の後ろはマイクロタスクになる
- 🚨 **重い同期処理はサーバー全体を止める**。`readFileSync`・巨大なループ・同期暗号処理に注意
- 逃がし方は **`worker_threads` / ジョブキュー / 処理の分割**
- 裏ではスレッドプール（既定4本）が動いており、完全な単一スレッドではない
- 複数コア活用は **`cluster` / PM2 / コンテナ複製**。クラウドではコンテナ複製が主流
- **`forEach` の中の `await` は待たれない**。`for...of` か `Promise.all` を使う

---

次の章 → [③ モジュールとnpm](03-modules-packages.md)
