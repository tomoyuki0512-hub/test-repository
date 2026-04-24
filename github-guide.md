# GitHub 基本ガイド

GitHubを使う上で知っておきたい情報まとめ。

---

## GitHub Pagesで公開する

リポジトリのファイルをWebサイトとして無料公開できる機能。

### 有効化の手順

1. GitHubでリポジトリを開く
2. 「**Settings**」タブをクリック
3. 左メニューの「**Pages**」をクリック
4. 「**Branch**」でブランチを選択
5. フォルダは「**/ docs**」を選択
6. 「**Save**」をクリック

数分後に以下のURLで公開される：
```
https://ユーザー名.github.io/リポジトリ名/
```

### スマホからの設定

スマホのブラウザでも同じ手順で設定できる。
Settingsタブが見えない場合はデスクトップ表示に切り替える：
- Safari: 共有ボタン →「デスクトップ用Webサイトを表示」
- Chrome: メニュー →「PC版サイト」

---

## Public / Private の違い

| | Public | Private |
|---|---|---|
| 誰でも閲覧できる | はい | いいえ |
| GitHub Pages（無料） | 使用可 | 使用不可 |
| GitHub Pages（有料Pro） | 使用可 | 使用可 |

### Privateリポジトリで無料公開したい場合

- **Netlify** → GitHubと連携、Privateリポジトリでも無料で公開可能
- **Vercel** → 同様にPrivateリポジトリ対応・無料プランあり

### PublicとPrivateの切り替え方法

1. リポジトリの「**Settings**」を開く
2. ページ一番下の「**Danger Zone**」へスクロール
3. 「**Change visibility**」をクリック
4. 「Change to public」または「Change to private」を選択
5. リポジトリ名を入力して確認

※ 後から変更可能なので Danger Zone と書いてあっても安心してよい

---

## 個人情報の確認と対策

Publicリポジトリにすると以下が全員に見える。

| 項目 | 内容 |
|---|---|
| ファイルの中身 | リポジトリ内の全ファイル |
| コミット履歴 | 変更履歴・日時 |
| コミットに紐づく名前・メールアドレス | ⚠️ 注意ポイント |

### コミットに登録された情報を確認する

```bash
git config user.name
git config user.email
```

または履歴を確認：

```bash
git log --format="%an %ae" | head -5
```

### メールアドレスを非公開にする方法

GitHubは非公開メールアドレスを提供している：

1. GitHub → 右上アイコン →「**Settings**」
2. 「**Emails**」をクリック
3. 「**Keep my email address private**」にチェック
4. 表示される `@users.noreply.github.com` のアドレスをgitに設定する

```bash
git config --global user.email "xxxxxxxx@users.noreply.github.com"
```

---

## アカウントの削除方法

### 削除手順

1. GitHubにログイン
2. 右上のアイコン →「**Settings**」
3. 左メニューを一番下までスクロール
4. 「**Delete your account**」をクリック
5. 確認フレーズを入力
6. パスワードを入力して確認

### 削除前に知っておくこと

| 項目 | 削除後の扱い |
|---|---|
| 自分のリポジトリ | **完全に削除される** |
| 他人のリポジトリへのコントリビューション | 記録は残る場合あり |
| IssueやPRのコメント | 残る場合がある |
| ユーザー名 | 一定期間は他人が使えない |
| **復元** | **できない（完全削除）** |

削除前にリポジトリをローカルにバックアップしておくことを推奨。

### 確認フレーズが一致しないエラーへの対処

`The confirmation phrase didn't match.` と表示された場合：

- 画面に表示されているフレーズを**そのままコピー&ペースト**する
- **全て小文字**で入力する
- 単語間のスペースは**半角スペース1つ**
- **日本語入力モードをOFF**にしてから入力する（重要）

通常求められるフレーズ例：
```
delete my account
```
