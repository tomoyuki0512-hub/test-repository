---
title: Claude Codeで結果をすぐにプレビューする方法
---

# Claude Codeで結果をすぐにプレビューする方法

Claude Code（CLI）にはClaudeウェブ版のような「アーティファクトビューア」はない。
しかし以下の方法で、ファイル作成後すぐに結果を確認・自動化できる。

---

## そもそも何者？

### `open` コマンド

**macOSに標準で入っているOSコマンド。** 別途インストール不要。

「ファイルをダブルクリックして開く」をターミナルから行うだけのもの。HTMLファイルを指定するとブラウザで開く。WindowsやLinuxにも同等のコマンドがある。

```bash
open index.html        # Mac（標準搭載）
start index.html       # Windows（標準搭載）
xdg-open index.html   # Linux（標準搭載）
```

ファイル保存しても**自動リロードはされない**。1回開くだけ。

---

### browser-sync

**フロントエンド開発者向けのnpmパッケージ（オープンソース）。**
2013年頃から広く使われているツールで、`npx` 経由でインストールなしに使える。

```bash
npx browser-sync start --server --files "**"
```

仕組み：

```
① browser-syncが小さなWebサーバーを立てる
② 監視対象ファイルに変更があるか常に見張っている
③ 変更を検知したら、ブラウザに「リロードしてね」と信号を送る
④ ブラウザが自動でリロードされる
```

**スマホも同じWi-Fiにつないでいれば同時リロードできる**のが最大の特徴。

---

### live-server

**browser-syncのシンプル版にあたるnpmパッケージ（オープンソース）。**
設定が最小限で、「とにかく自動リロードしたい」というときに使いやすい。

```bash
npx live-server
```

browser-syncより機能は少ないが、コマンド1つで動くシンプルさが人気。

---

### 3つの比較

| | `open` | `browser-sync` | `live-server` |
|---|---|---|---|
| 何者か | OSの標準コマンド | npmパッケージ | npmパッケージ |
| インストール | 不要（OS標準） | 不要（npx） | 不要（npx） |
| ブラウザを自動で開く | ○ | ○ | ○ |
| 保存で自動リロード | **✗** | ○ | ○ |
| スマホも同時リロード | ✗ | ○ | ✗ |
| 複数ブラウザ同時リロード | ✗ | ○ | ✗ |
| 設定のシンプルさ | 最簡単 | 中 | 簡単 |

**使い分けの目安：**
- 1回だけ確認 → `open`
- 普段の開発・修正を繰り返す → `live-server`
- スマホでも確認・複数ブラウザ → `browser-sync`

---

## 方法の比較

| 方法 | 自動化 | ファイル変更で自動リロード | 向いている用途 |
|---|---|---|---|
| `open` コマンドで即ブラウザ起動 | ○ | ✗ | 1回確認したいとき |
| `browser-sync` | ○ | **○** | HTML/CSS/JS開発 |
| `live-server` | ○ | **○** | HTML/CSS/JS開発 |
| VS Code Live Preview | △（手動） | ○ | VS Code使用時 |
| フレームワークのdev server | ○ | ○（HMR） | React/Next.js/Rails等 |
| Claude Code Hooks | ○ | △ | 全自動化したいとき |

---

## 方法1：作成後すぐブラウザで開く（最もシンプル）

Claude Codeにこの指示を出すだけで、ファイル作成後に自動でブラウザが開く。

### 指示テンプレート

```
index.htmlを作成したら、最後に以下のコマンドでブラウザで開いてください。

# Mac
open index.html

# Windows
start index.html

# Linux
xdg-open index.html
```

### 自動化された指示例（コピペ用）

```
シンプルな飲食店のトップページHTMLを作成してください。
作成後、自動でブラウザで開くコマンドも実行してください（OSはMacです）。
```

---

## 方法2：browser-sync（ファイル変更で自動リロード・おすすめ）

`browser-sync` はファイルを保存するたびにブラウザを自動でリロードするツール。
Claude Codeがファイルを編集するたびに画面が自動更新される。

### インストール不要で即使える

```bash
# HTMLファイルがあるフォルダで実行
npx browser-sync start --server --files "**/*.html,**/*.css,**/*.js"
```

実行すると：
- ブラウザが自動で開く
- `http://localhost:3000` でアクセスできる
- HTMLやCSSを変更するたびにブラウザが自動リロードされる

### Claude Codeへの指示テンプレート

```
以下をお願いします：
1. [作りたいもの] のHTMLファイルを作成してください
2. 作成後に `npx browser-sync start --server --files "**"` を実行してください
3. 私がブラウザで確認したらフィードバックを伝えます
```

### ポートを変えたい場合

```bash
npx browser-sync start --server --files "**" --port 4000
```

---

## 方法3：live-server（シンプル版）

```bash
npx live-server
```

- `index.html` を自動で開く
- ファイル変更で自動リロード
- デフォルトポートは8080

### Claude Codeへの指示テンプレート

```
[作りたいもの]のHTMLを作成して、`npx live-server` で起動してください。
```

---

## 方法4：Claude Code Hooksで完全自動化

Claude Codeの **Hooks機能** を使うと、「ファイルを書き込むたびに自動でブラウザリロード」を設定できる。

### Hooksとは

Claude Codeのツール実行前後に、自動でシェルコマンドを実行できる仕組み。

```
ファイルを書き込む（Write/Edit）
    ↓ PostToolUseフック発動
browser-sync が自動リロード
    ↓
ブラウザが最新の状態を表示
```

### 設定方法

プロジェクトの `.claude/settings.json` に以下を追記する：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'ファイルが更新されました'"
          }
        ]
      }
    ]
  }
}
```

### より実用的な設定例（browser-syncと組み合わせ）

**Step 1：browser-syncをバックグラウンドで起動しておく**

```bash
npx browser-sync start --server --files "**" &
```

**Step 2：`.claude/settings.json` を設定**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "touch .reload-trigger"
          }
        ]
      }
    ]
  }
}
```

---

## 方法5：フレームワーク別のdev server（変更が即反映）

各フレームワークには **HMR（ホットモジュールリプレースメント）** という、コード変更を保存するとブラウザに即反映される機能がある。

### フレームワーク別の起動コマンドと指示テンプレート

#### React / Vite

```bash
npm run dev
# → http://localhost:5173 が自動で開く
```

**指示テンプレート：**
```
Vite + ReactのプロジェクトでTodoアプリを作ってください。
`npm run dev` でサーバーを起動して、私がブラウザで確認します。
コードを変更するたびに自動でブラウザに反映されます。
```

---

#### Next.js

```bash
npm run dev
# → http://localhost:3000 が開く
```

**指示テンプレート：**
```
Next.jsで飲食店のトップページを作ってください。
`npm run dev` を起動して、ブラウザで確認できる状態にしてください。
```

---

#### Ruby on Rails

```bash
rails server
# → http://localhost:3000 が開く
```

**指示テンプレート：**
```
Railsで[機能]を実装してください。
`rails server` を起動して確認できる状態にしてください。
```

---

#### FastAPI（Swagger UIで即確認）

```bash
uvicorn main:app --reload
# → http://localhost:8000/docs でSwagger UIが開く
```

**指示テンプレート：**
```
FastAPIで[API]を作ってください。
`uvicorn main:app --reload` を起動して、
http://localhost:8000/docs でAPIを確認できる状態にしてください。
```

> FastAPIはSwagger UIが自動生成されるため、APIの動作確認がブラウザ上でGUIで行える。

---

## 自動化のための指示テンプレート集

### パターン1：HTMLを作ってすぐ確認（Mac）

```
以下の手順で進めてください：
1. [内容]のHTMLファイルを作成する
2. `npx browser-sync start --server --files "**"` を実行する
3. ブラウザが開いたら私に教えてください
```

### パターン2：修正のたびに確認したい（開発中）

```
browser-syncをバックグラウンドで起動してください：
`npx browser-sync start --server --files "**" &`

その後、[内容]を実装してください。
ファイルを保存するたびにブラウザが自動リロードされます。
```

### パターン3：複数ファイルを作りながら確認

```
以下のファイル構成でランディングページを作成してください：
- index.html
- style.css
- script.js

作成後に `npx live-server` を起動し、
ブラウザで確認できる状態にしてください。
修正依頼は画面を見ながら伝えます。
```

### パターン4：APIとフロントエンドを同時に確認

```
バックエンド（FastAPI）とフロントエンド（Vanilla JS）を作成してください。

起動手順：
1. バックエンド: `uvicorn main:app --reload` （ポート8000）
2. フロントエンド: `npx live-server --port=5500`

CORS設定も忘れずに行ってください。
```

---

## まとめ：状況別おすすめ

| 状況 | おすすめ | コマンド |
|---|---|---|
| HTMLを1回確認したい | `open` コマンド | `open index.html` |
| HTML/CSS開発で常に確認したい | browser-sync | `npx browser-sync start --server --files "**"` |
| フレームワーク開発中 | dev server | `npm run dev` / `rails server` 等 |
| API開発 | FastAPI + Swagger UI | `uvicorn main:app --reload` → `/docs` |
| 完全自動化したい | Claude Code Hooks | `.claude/settings.json` に設定 |

---

## `npx serve .` との併用について

### 基本：併用しない

`browser-sync` と `live-server` は**サーバー機能も内蔵している**ため、`npx serve .` の代わりになる。同時に起動するとポートが競合する。

```
npx serve .    → サーバーのみ（自動リロードなし）
browser-sync   → サーバー＋自動リロード（serve の上位互換）
live-server    → サーバー＋自動リロード（serve の上位互換）
```

### 例外：プロキシモードなら併用できる

`browser-sync` には既存サーバーの前に挟む **プロキシモード** がある。
Express・FastAPI・Railsなど**自前のサーバーが既にある場合**に使える。

```bash
# ① 既存サーバーを起動（例：npx serve .）
npx serve . --listen 3001

# ② browser-syncをプロキシとして前に挟む
npx browser-sync start --proxy "localhost:3001" --files "**"
```

```
ブラウザ → browser-sync（:3000）→ npx serve（:3001）
                ↑
         ファイル変更を検知して自動リロードを追加
```

### 状況別まとめ

| 状況 | 使うもの |
|---|---|
| HTMLだけの静的サイト | `browser-sync` か `live-server` 単体でOK（serve不要） |
| Expressなど自前サーバーあり | `自前サーバー` ＋ `browser-sync --proxy` |
| FastAPI・Railsのバックエンド | サーバー自体にホットリロードあり（`--reload` 等） |
