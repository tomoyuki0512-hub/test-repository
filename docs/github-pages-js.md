---
title: GitHub PagesでJavaScriptを使う
---

# GitHub PagesでJavaScriptを使う

GitHub Pagesは「静的コンテンツ」のホスティングサービスだが、JavaScriptは問題なく使える。

---

## 「静的」と「動的」の違い

| | 静的サイト | 動的サイト |
|---|---|---|
| 処理の場所 | **ブラウザ（クライアント側）** | サーバー側 |
| 例 | HTML・CSS・JS | PHP・Python・Ruby |
| GitHub Pages | ○ 使える | ✗ 使えない |

**静的 = サーバーが処理しない** という意味。ブラウザ上で動くJavaScriptは「クライアントサイド」の処理なので問題なく動く。

---

## GitHub Pagesでできること・できないこと

### ○ できること（クライアントサイドJS）

- ボタンクリック・スクロール等のイベント処理
- アニメーション・DOM操作
- フォームのバリデーション（入力チェック）
- LocalStorage / SessionStorage（ブラウザにデータを保存）
- Fetch API で外部APIを叩く（天気API、GitHubAPIなど）
- React・Vue・Vanilla JSなどのフロントエンドフレームワーク
- チャート・地図など（Chart.js、Leaflet.jsなど）

### ✗ できないこと（サーバーサイド処理）

- データベースへの直接接続
- ファイルのサーバー保存
- サーバーサイドでのメール送信
- ユーザー認証（セッション管理）
- PHPやPythonのスクリプト実行

---

## Markdownファイルの中にJSを書く方法

Jekyll（GitHub Pagesの変換エンジン）はMarkdownの中にHTMLやJSをそのまま書ける。

### 基本：`<script>` タグをMarkdown内に直接書く

````markdown
# ページタイトル

通常のMarkdownテキスト。

<button onclick="greet()">クリックしてね</button>

<script>
function greet() {
  alert('こんにちは！');
}
</script>
````

### 外部JSファイルを読み込む

`docs/` フォルダにJSファイルを置いて読み込む：

```
docs/
├── index.md
├── js/
│   └── main.js     ← JSファイルをここに置く
```

Markdownファイルの中で読み込む：

```html
<script src="js/main.js"></script>
```

---

## 実用的なサンプル

### サンプル1：ダークモード切り替えボタン

```html
<button id="toggle-btn" onclick="toggleDark()">🌙 ダークモード</button>

<style>
  .dark-mode { background: #1a1a1a; color: #ffffff; }
</style>

<script>
function toggleDark() {
  document.body.classList.toggle('dark-mode');
  const btn = document.getElementById('toggle-btn');
  btn.textContent = document.body.classList.contains('dark-mode')
    ? '☀️ ライトモード'
    : '🌙 ダークモード';
}
</script>
```

---

### サンプル2：コピーボタン

```html
<pre id="code-block">npx serve .</pre>
<button onclick="copyCode()">コピー</button>

<script>
function copyCode() {
  const text = document.getElementById('code-block').textContent;
  navigator.clipboard.writeText(text).then(() => {
    alert('コピーしました！');
  });
}
</script>
```

---

### サンプル3：外部API（天気）を呼び出す

Fetch APIで外部サービスのデータを取得できる。

```html
<button onclick="getWeather()">東京の天気を取得</button>
<p id="weather-result"></p>

<script>
async function getWeather() {
  const res = await fetch('https://wttr.in/Tokyo?format=3');
  const text = await res.text();
  document.getElementById('weather-result').textContent = text;
}
</script>
```

---

### サンプル4：LocalStorageで入力内容を保存

```html
<input type="text" id="memo" placeholder="メモを入力" oninput="saveMemo()">
<p id="saved-text"></p>

<script>
// ページ読み込み時に保存済みデータを表示
window.onload = () => {
  const saved = localStorage.getItem('memo');
  if (saved) {
    document.getElementById('memo').value = saved;
    document.getElementById('saved-text').textContent = '保存済み：' + saved;
  }
};

function saveMemo() {
  const value = document.getElementById('memo').value;
  localStorage.setItem('memo', value);
  document.getElementById('saved-text').textContent = '保存済み：' + value;
}
</script>
```

---

## CDN経由でライブラリを使う

外部ライブラリはCDNから読み込むと、ファイルをリポジトリに置かずに使える。

### Chart.js でグラフを表示

```html
<canvas id="myChart" width="400" height="200"></canvas>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx = document.getElementById('myChart').getContext('2d');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['1月', '2月', '3月'],
    datasets: [{
      label: 'アクセス数',
      data: [120, 190, 300],
      backgroundColor: ['#4e79a7', '#f28e2b', '#e15759']
    }]
  }
});
</script>
```

### Alpine.js でシンプルな動的制御

小さなインタラクションに便利なライブラリ。

```html
<script src="https://cdn.jsdelivr.net/npm/alpinejs@3" defer></script>

<div x-data="{ count: 0 }">
  <button @click="count++">クリック</button>
  <p>クリック回数：<span x-text="count"></span></p>
</div>
```

---

## できないことへの対処法

サーバーサイド処理が必要な機能は、**外部サービスと組み合わせる**ことで実現できる。

| やりたいこと | 解決策 |
|---|---|
| フォームからメール送信 | Formspree・Netlify Forms（無料プランあり） |
| ユーザー認証・ログイン | Firebase Authentication・Auth0（無料プランあり） |
| データベース | Firebase Firestore・Supabase（無料プランあり） |
| サーバーサイドの処理全般 | Netlify Functions・Vercel Functions（無料プランあり） |

---

## まとめ

```
GitHub Pages（静的）
    ├─ HTML / CSS        → ○ そのまま使える
    ├─ JavaScript（JS）  → ○ ブラウザで動くなら全部OK
    ├─ 外部API呼び出し   → ○ Fetch APIで使える
    ├─ PHPなどのサーバー処理 → ✗ できない
    └─ データベース直接接続  → ✗ できない（外部サービスで代替）
```

静的サイトでもJSを使えばかなりリッチな表現が可能。複雑なバックエンド処理が必要になったときは、NetlifyやVercelへの移行を検討する。
