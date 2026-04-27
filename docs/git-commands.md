# Git コマンド一覧

リポジトリ: https://github.com/tomoyuki0512-hub/claude-code-notes
ローカルパス: C:\Users\user\Desktop\ai-invest-app
ブランチ: main

---

## 1. 初期設定

```bash
# ユーザー名・メールを設定（全プロジェクト共通）
git config --global user.name "tomoyuki0512-hub"
git config --global user.email "tomoyuki0512@gmail.com"

# 設定内容を確認
git config --list
```

---

## 2. リポジトリの取得・作成

```bash
# GitHubからクローン（別PCや別フォルダに取得する）
git clone https://github.com/tomoyuki0512-hub/claude-code-notes.git

# トークン認証が必要な場合
git clone https://<YOUR_TOKEN>@github.com/tomoyuki0512-hub/claude-code-notes.git

# 既存フォルダをGit管理下に置く（このプロジェクトで実施済み）
git init
```

---

## 3. 状態確認

```bash
# 変更・未追跡ファイルを確認
git status

# 例: work/claude-code-capabilities/claude-code-capabilities.md を編集後
# → "modified: work/claude-code-capabilities/claude-code-capabilities.md" と表示される
```

---

## 4. 差分確認

```bash
# 編集内容をステージング前に確認
git diff

# 例: claude-code-capabilities.md の変更前後を表示
git diff work/claude-code-capabilities/claude-code-capabilities.md

# ステージング済みの差分を確認
git diff --cached
```

---

## 5. ステージング（コミット対象に追加）

```bash
# 特定ファイルをステージング
git add work/claude-code-capabilities/claude-code-capabilities.md

# 複数ファイルをまとめてステージング
git add work/claude-code-capabilities/

# すべての変更をステージング
git add -A

# ステージングを取り消す（ファイルは変更されたまま）
git restore --staged work/claude-code-capabilities/claude-code-capabilities.md
```

---

## 6. コミット

```bash
# ステージング済みの内容をコミット
git commit -m "monthly update: claude-code-capabilities 2026-05"

# ステージングとコミットを同時に行う（新規ファイルは対象外）
git commit -am "fix: typo in claude-code-capabilities.md"

# 直前のコミットメッセージを修正（pushする前のみ）
git commit --amend -m "monthly update: claude-code-capabilities 2026-05"
```

---

## 7. リモートへのpush

```bash
# mainブランチをpush
git push origin main

# 初回のみ（上流ブランチを設定しながらpush）
git push -u origin main

# トークンをURLに含めてpush（認証が通らない場合）
git remote set-url origin https://<YOUR_TOKEN>@github.com/tomoyuki0512-hub/claude-code-notes.git
git push origin main
```

---

## 8. リモートからのpull・fetch

```bash
# GitHubの最新内容をローカルに反映（fetch + merge）
git pull

# 別フォルダにいても実行できる
git -C C:\Users\user\Desktop\ai-invest-app pull

# リモートの変更を取得するだけ（マージしない）
git fetch origin

# リモートの状態を確認
git remote -v
# → origin  https://github.com/tomoyuki0512-hub/claude-code-notes.git (fetch)
# → origin  https://github.com/tomoyuki0512-hub/claude-code-notes.git (push)
```

---

## 9. 履歴確認

```bash
# コミット履歴を表示
git log

# 1行で表示
git log --oneline
# → 609fa57 initial commit: Claude Code notes with capabilities doc and diagram scripts

# ファイル単位の履歴
git log --oneline work/claude-code-capabilities/claude-code-capabilities.md

# 変更内容も含めて表示
git log -p work/claude-code-capabilities/claude-code-capabilities.md
```

---

## 10. ブランチ操作

```bash
# ブランチ一覧を表示（* が現在いるブランチ）
git branch
# → * main
#     feature/add-mcp-section

# 新しいブランチを作成して切り替え（推奨）
git switch -c feature/add-mcp-section

# 作成だけして切り替えない
git branch feature/add-mcp-section

# ブランチを切り替え
git switch main

# ブランチをmainにマージ
git merge feature/add-mcp-section

# ブランチを削除（マージ済みのもの）
git branch -d feature/add-mcp-section

# ブランチをGitHubにpush
git push origin feature/add-mcp-section
```

---

## 11. 変更を元に戻す

```bash
# rm で削除したファイルを1つ復元（最後のコミット時点に戻す）
git restore work/claude-code-capabilities/claude-code-capabilities.md

# フォルダごと一括復元
git restore work/claude-code-capabilities/

# カレントディレクトリ以下の削除・変更をすべて復元
git restore .

# 直前のコミットを取り消す（変更内容はローカルに残す）
git reset HEAD~1

# 指定コミット時点まで戻す（履歴ごと削除 ※注意）
git reset --hard 609fa57
```

---

## 12. ファイルの削除・移動

```bash
# Gitの管理からファイルを削除（ファイル自体も消える）
git rm work/old-file.md

# Gitの管理からのみ除外（ファイルはローカルに残す）
git rm --cached work/old-file.md

# ファイルを移動・リネーム
git mv work/scripts/old-name.mjs work/scripts/new-name.mjs
```

---

## 13. .gitignore（除外設定）

```bash
# 除外設定ファイルを確認
cat .gitignore

# 除外したいファイルの例（.gitignore に記述する内容）
# node_modules/
# *.log
# .env
```

---

## 14. プルリクエスト（PR）

PRは「自分のブランチの変更をmainに取り込んでほしい」と提案する機能。
一人開発では不要だが、レビューを挟みたい場合や別ブランチで作業するときに使う。

```bash
# ① 作業ブランチを作成
git switch -c feature/add-mcp-section

# ② 変更してコミット
git add work/claude-code-capabilities/claude-code-capabilities.md
git commit -m "add: MCP section to capabilities doc"

# ③ GitHubにpush（この時点ではmainには反映されない）
git push origin feature/add-mcp-section

# → GitHubを開くと「Compare & pull request」ボタンが表示される
# → PRを作成 → 自分でマージ → mainに反映される

# ④ マージ後にブランチを削除
git branch -d feature/add-mcp-section
```

**このリポジトリは一人運用のため、直接 `git push origin main` でPRなしに反映できる。**

---

## 15. リモート（origin）の管理

`origin` はリモートリポジトリにつけたニックネーム。`git clone` 時に自動でつく慣習的な名前。

```bash
# リモートの一覧を確認
git remote -v
# → origin  https://github.com/tomoyuki0512-hub/claude-code-notes.git (fetch)
# → origin  https://github.com/tomoyuki0512-hub/claude-code-notes.git (push)

# originのURLを変更（トークン更新時など）
git remote set-url origin https://github.com/tomoyuki0512-hub/claude-code-notes.git

# 別名でリモートを追加（複数リモートを持つ場合）
git remote add github https://github.com/tomoyuki0512-hub/claude-code-notes.git

# リモートを削除
git remote remove github
```

origin 以外のよくある名前：
- `upstream` — forkの場合に元のリポジトリを指す慣習的な名前

---

## 16. fork

他人のGitHubリポジトリを自分のアカウントにコピーすること（ブラウザで行う操作）。

```
他人のリポジトリ                     自分のリポジトリ（fork）
github.com/anthropics/claude-code → github.com/tomoyuki0512-hub/claude-code
```

| | fork | clone |
|---|---|---|
| 何をするか | GitHubに自分用コピーを作る | ローカルPCにダウンロードする |
| どこで行うか | GitHub上（ブラウザ） | ターミナル |
| pushできるか | 自分のforkにはできる | 元リポジトリへは権限次第 |

```bash
# fork後の典型的な流れ
# ① ブラウザでfork → 自分のアカウントにコピーされる
# ② forkしたリポジトリをclone
git clone https://github.com/tomoyuki0512-hub/claude-code.git

# ③ 元リポジトリをupstreamとして登録
git remote add upstream https://github.com/anthropics/claude-code.git

# ④ 元リポジトリの最新を取り込む
git fetch upstream
git merge upstream/main

# ⑤ 変更してpush → GitHubでPRを送る
git push origin main
```

### forkの作成手順（ブラウザ操作）

1. forkしたいリポジトリをブラウザで開く
   例: `https://github.com/anthropics/claude-code`
2. ページ右上の **「Fork」** ボタンをクリック
3. Owner: `tomoyuki0512-hub` を選択、Repository name はそのままでOK
4. **「Create fork」** をクリック
5. `github.com/tomoyuki0512-hub/claude-code` が作成される

```bash
# fork後にローカルへ取得
git clone https://github.com/tomoyuki0512-hub/claude-code.git
```

**このリポジトリは自分で作ったものなのでforkは不要。**

---

## よく使う組み合わせ

```bash
# 変更 → 確認 → コミット → push の基本フロー
git status
git add work/claude-code-capabilities/claude-code-capabilities.md
git commit -m "update: add new Claude Code features"
git push origin main

# GitHubの最新を取り込んでから作業開始
git pull

# rm で消したファイルをまとめて復元
git restore .
```
