---
title: 問い合わせページの作り方
---

# 問い合わせページの作り方

飲食店・習い事サイトなどで問い合わせページを作る方法まとめ。

---

## GitHub Pages（静的サイト）で問い合わせはできる？

フォームの「送信」ボタンを押したとき、通常はサーバー側で「メールを送る」「DBに保存する」処理が必要。GitHub Pagesにはサーバー処理がないため、そのままでは動かない。

ただし、**外部サービスと組み合わせることで実現できる。**

---

## 方法の比較

| 方法 | 難易度 | 費用 | MDで使えるか | おすすめ度 |
|---|---|---|---|---|
| **Googleフォームへリンク** | 最簡単 | 無料 | ○ | ★★★★☆ |
| **Googleフォームを埋め込み** | 簡単 | 無料 | ○（HTML記述） | ★★★★★ |
| **Formspree（HTMLフォーム）** | 普通 | 無料（月50件まで） | △（HTML直書き） | ★★★★☆ |
| **EmailJS** | やや難 | 無料（月200件まで） | △（JS必要） | ★★★☆☆ |
| **Netlify Forms** | 簡単 | 無料（月100件まで） | ○（Netlifyに移行が必要） | ★★★★☆ |

---

## 方法1：Googleフォームへリンク（最も簡単）

Googleフォームを作成し、そのURLにリンクするだけ。

**MDファイルでの書き方：**

```markdown
[お問い合わせはこちら](https://forms.gle/xxxxxxxxx)
```

**メリット：** 設定ほぼゼロ・スマホ対応・回答がGoogleスプレッドシートに自動保存  
**デメリット：** Googleのページに飛ぶため、見た目が自サイトと変わる

---

## 方法2：Googleフォームを埋め込み（おすすめ）

Googleフォームの`<iframe>`をMDファイルやHTMLに貼り付けると、自サイト内に表示できる。

**Googleフォームの埋め込みコードの取得方法：**

1. Googleフォームを開く
2. 右上の「送信」ボタンをクリック
3. `<>` タブ（埋め込み）を選択
4. 表示されたコードをコピー

**MDファイルへの貼り付け方：**

```html
<iframe 
  src="https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform?embedded=true"
  width="100%" 
  height="600" 
  frameborder="0">
</iframe>
```

**メリット：** 自サイト内に表示される・設定簡単・無料  
**デメリット：** フォームのデザインはGoogleのもの（カスタマイズ不可）

---

## 方法3：Formspreeを使ったHTMLフォーム

HTMLで自由にデザインしたフォームを作り、Formspreeが送信処理を代行してくれる。

**手順：**

1. [formspree.io](https://formspree.io) でアカウント作成
2. 「New Form」でフォームを作成
3. 発行された `action` URLをHTMLに設定

```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
  <input type="text" name="name" placeholder="お名前" required>
  <input type="email" name="email" placeholder="メールアドレス" required>
  <textarea name="message" placeholder="お問い合わせ内容" required></textarea>
  <button type="submit">送信する</button>
</form>
```

**メリット：** フォームのデザインを自由にカスタマイズできる  
**デメリット：** 無料プランは月50件まで・Formspreeへの登録が必要

---

## MDとHTMLどちらが良いか？

| | MDファイル | HTMLファイル |
|---|---|---|
| 書きやすさ | ○ 簡単 | △ 知識が必要 |
| デザインの自由度 | △ Jekyllテーマに依存 | ○ 完全に自由 |
| Googleフォーム埋め込み | ○ iframeをそのまま貼れる | ○ |
| Formspreeフォーム | △ HTMLを直接書く必要がある | ○ |
| おすすめ用途 | ドキュメント・簡単なページ | デザインにこだわりたいページ |

---

## サンプルファイル

- [MDサンプル（Googleフォーム埋め込み）](contact-sample-md) — 飲食店向けサンプル
- [HTMLサンプル（Formspree）](contact-sample-html.html) — 習い事教室向けサンプル
