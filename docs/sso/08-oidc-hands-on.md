---
title: ⑧ OIDCログイン実装ハンズオン 〜自社アプリに「◯◯でログイン」を組み込む〜
---

# ⑧ OIDCログイン実装ハンズオン 〜自社アプリに「◯◯でログイン」を組み込む〜

> **この章でわかること**
> - 認証サービス（IDaaS）をどう選ぶか（Auth0 / Cognito / Firebase / Keycloak）
> - **Auth0 + Node.js で「ログイン付きWebアプリ」を実際に動かすまでの全手順**（コード付き）
> - Flutterアプリに組み込む場合のコード例（flutter_appauth）
> - 自前実装する場合に絶対に外せない検証チェックリスト

> 前提知識：[③OAuth 2.0](03-oauth2.md) と [④OIDC](04-oidc.md) を読んでいると、コードの各行が「何をしているか」まで理解できます。読んでいなくても動かすことは可能です。

---

## 1. 大原則：認証は「作らず借りる」

最初に結論です。**ログイン機能をゼロから自前実装するのは、ほとんどの場合やめるべき**です。

- パスワードのハッシュ化・漏洩対策・MFA・パスキー・アカウントロック・ブルートフォース対策・セッション管理……正しく作るのは専門家でも大変
- 認証のバグは「即・全ユーザーに影響する脆弱性」になる
- IDaaS（認証のクラウドサービス）を使えば、**数十行のコードで上記すべてが手に入る**

### 主要サービスの選び方

| サービス | 向いているケース | 無料枠の目安 |
| --- | --- | --- |
| **Auth0**（Okta傘下） | まず迷ったらこれ。ドキュメント最強、あらゆる言語のSDKあり | 〜25,000 MAU |
| **Firebase Authentication** | モバイルアプリ中心、Google系サービスと併用 | ほぼ無制限（電話認証等は従量） |
| **Amazon Cognito** | インフラがAWS中心 | 〜10,000 MAU |
| **Keycloak**（OSS） | 自前ホストしたい、ライセンス費を払いたくない、要件が特殊 | 無料（運用は自己責任） |

いずれも中身は本シリーズで学んだ **OIDC** です。つまり**1つ使えるようになれば、他への乗り換えも本質的には設定の書き換えだけ**です。

---

## 2. ハンズオン：Auth0 + Node.js で30分で動かす

「ログイン／ログアウトができ、ログイン中のユーザー名を表示するWebアプリ」を作ります。

### Step 1：Auth0側の準備（ブラウザ作業・5分）

1. [auth0.com](https://auth0.com) で無料アカウントを作成（テナント名とリージョンを聞かれる。リージョンは日本ならJPでOK）
2. ダッシュボード左メニュー **「Applications」→「Create Application」**
3. 名前を入力し、種類は **「Regular Web Applications」** を選択
4. 作成後、**「Settings」タブ**で以下の3つをメモする
   - **Domain**（例：`dev-abc123.jp.auth0.com`）
   - **Client ID**
   - **Client Secret**
5. 同じSettingsタブの下方で、コールバック関連を設定して **Save**
   - **Allowed Callback URLs**：`http://localhost:3000/callback`
   - **Allowed Logout URLs**：`http://localhost:3000`

> ここでやったことは、[③OAuth 2.0](03-oauth2.md) で学んだ「**Clientの登録**」と「**リダイレクトURIの事前登録**」そのものです。

### Step 2：Node.jsプロジェクトの作成（5分）

```bash
mkdir my-login-app && cd my-login-app
npm init -y
npm install express express-openid-connect dotenv
```

`.env` ファイルを作り、Step 1でメモした値を入れます：

```bash
# .env（このファイルは絶対にgitにコミットしないこと! .gitignoreに追加）
AUTH0_DOMAIN=dev-abc123.jp.auth0.com
AUTH0_CLIENT_ID=あなたのClient ID
AUTH0_CLIENT_SECRET=あなたのClient Secret
SESSION_SECRET=ランダムな長い文字列（openssl rand -hex 32 で生成）
BASE_URL=http://localhost:3000
```

### Step 3：アプリ本体（app.js）——これで全部です

```javascript
require('dotenv').config();
const express = require('express');
const { auth, requiresAuth } = require('express-openid-connect');

const app = express();

// この1ブロックで OIDC の認可コードフロー一式が組み込まれる
// （/login /logout /callback ルートが自動で生える）
app.use(
  auth({
    authRequired: false,               // 全ページ強制ログインにはしない
    auth0Logout: true,                 // ログアウト時にIdP側セッションも消す（RP-Initiated Logout）
    baseURL: process.env.BASE_URL,
    clientID: process.env.AUTH0_CLIENT_ID,
    clientSecret: process.env.AUTH0_CLIENT_SECRET,
    issuerBaseURL: `https://${process.env.AUTH0_DOMAIN}`,
    secret: process.env.SESSION_SECRET // セッションCookieの暗号化キー
  })
);

// トップページ：ログイン状態で表示を出し分け
app.get('/', (req, res) => {
  if (req.oidc.isAuthenticated()) {
    res.send(`
      <h1>ようこそ、${req.oidc.user.name} さん</h1>
      <p>メール: ${req.oidc.user.email}</p>
      <a href="/profile">プロフィール(要ログインページ)</a> |
      <a href="/logout">ログアウト</a>
    `);
  } else {
    res.send('<h1>未ログインです</h1><a href="/login">ログイン</a>');
  }
});

// ログイン必須ページの作り方：requiresAuth() を挟むだけ
app.get('/profile', requiresAuth(), (req, res) => {
  res.send(`<pre>${JSON.stringify(req.oidc.user, null, 2)}</pre>`);
});

app.listen(3000, () => console.log('http://localhost:3000 で起動しました'));
```

### Step 4：起動して動きを確認する

```bash
node app.js
```

1. `http://localhost:3000` を開く →「未ログインです」
2. 「ログイン」を押す → **Auth0のログイン画面へリダイレクトされる**（＝IdPへの誘導）
3. サインアップしてログイン → アプリに戻り「ようこそ、◯◯さん」
4. `/profile` を開くと、**IDトークン由来のユーザー情報（`sub`・`email`・`name`…）**がJSONで見える
5. F12のNetworkタブを開いてやり直すと、[④OIDC](04-oidc.md)で学んだ `authorize?...scope=openid...` → `callback?code=...` の流れがそのまま観察できる

> **たった30行で**、認可コードフロー・state検証・トークン検証・セッション管理・ログアウトまで実装されました。これが「作らず借りる」の威力です。

### Step 5（任意）：「Googleでログイン」ボタンを足す

Auth0ダッシュボード →「Authentication」→「Social」→「Create Connection」→ Google を有効化するだけ。**アプリのコードは1行も変えずに**、次回からログイン画面にGoogleボタンが現れます。ソーシャルログインの追加がインフラ設定だけで済むのも、IDaaSを使う利点です。

---

## 3. Flutterアプリに組み込む場合

モバイルアプリでは **flutter_appauth** パッケージ（OIDC標準の [AppAuth](https://appauth.io/) ライブラリのFlutter版）を使うのが定石です。**PKCE（[③参照](03-oauth2.md)）を自動で使ってくれます。**

```yaml
# pubspec.yaml
dependencies:
  flutter_appauth: ^7.0.0
  flutter_secure_storage: ^9.0.0   # トークンの安全な保存用
```

```dart
import 'package:flutter_appauth/flutter_appauth.dart';

final FlutterAppAuth appAuth = const FlutterAppAuth();

Future<void> login() async {
  // 認可コードフロー + PKCE + トークン交換までを一括実行
  final AuthorizationTokenResponse result =
      await appAuth.authorizeAndExchangeCode(
    AuthorizationTokenRequest(
      'あなたのClient ID',
      'com.example.myapp://callback',        // モバイルはカスタムURLスキームで戻る
      issuer: 'https://dev-abc123.jp.auth0.com',
      scopes: ['openid', 'profile', 'email'],
    ),
  );

  // IDトークン(JWT)・アクセストークンが取得できる
  print(result.idToken);
  // トークンは flutter_secure_storage 等の安全な領域に保存する
  // （SharedPreferences への平文保存はNG）
}
```

モバイル特有の注意点：

- **リダイレクトはカスタムURLスキーム**（`com.example.myapp://callback`）。Android は `AndroidManifest.xml`、iOS は `Info.plist` にスキーム登録が必要（flutter_appauthのREADME参照）
- **Client Secretは使わない**（アプリ内に秘密は置けない。だからPKCEが必須——[③OAuth 2.0](03-oauth2.md)で学んだ通り）
- Auth0側のApplication種類は「**Native**」で作成する

---

## 4. Amazon Cognito を使う場合の差分

やることの構造はAuth0と同じです。読み替え表：

| Auth0 | Cognito | 備考 |
| --- | --- | --- |
| テナント作成 | **ユーザープール**作成 | AWSコンソール →「Cognito」 |
| Application登録 | **アプリクライアント**作成 | Regular Web App相当は「機密クライアント」 |
| Domain | **Cognitoドメイン**（またはカスタムドメイン）を有効化 | ホストされたログイン画面用 |
| Allowed Callback URLs | **許可されているコールバックURL** | 同じ概念 |
| `issuerBaseURL` | `https://cognito-idp.<region>.amazonaws.com/<ユーザープールID>` | OIDCのissuer |

`express-openid-connect` は汎用OIDCクライアントなので、**上のapp.jsの `issuerBaseURL`・`clientID`・`clientSecret` をCognitoの値に差し替えるだけでそのまま動きます**。「OIDCを1つ覚えれば乗り換えは設定だけ」の実例です。

---

## 5. 自前で実装する場合の検証チェックリスト

フレームワークを使わず自分でトークンを扱う場合（またはコードレビューで見るべき点）：

- [ ] **署名検証**：IdPの公開鍵（`/.well-known/openid-configuration` → `jwks_uri`）でJWTの署名を検証しているか
- [ ] **`iss` 検証**：期待するIdPからの発行か
- [ ] **`aud` 検証**：自分のClient ID宛てか（**トークン差し替え攻撃対策**——[③参照](03-oauth2.md)）
- [ ] **`exp` / `iat` 検証**：期限切れ・未来すぎる発行時刻を拒否しているか
- [ ] **`state` 検証**：認可リクエスト時に生成した値と一致するか（CSRF対策）
- [ ] **`nonce` 検証**：IDトークンのリプレイ（使い回し）対策
- [ ] **PKCE**：認可コードフローで必ず使っているか
- [ ] **トークンの保存場所**：Webは`HttpOnly` Cookie推奨（localStorageはXSSに弱い）、モバイルはセキュアストレージ
- [ ] **Client Secretの管理**：コード・リポジトリに直書きしていないか（環境変数・シークレット管理サービスへ）
- [ ] **HTTPSの強制**：本番でhttpのリダイレクトURIを許可していないか

> このリストの1つ1つが「なぜ必要か」は、[③OAuth 2.0](03-oauth2.md)・[④OIDC](04-oidc.md)・[⑤セキュリティ](05-security-mfa.md)で解説した攻撃と対応しています。チェック項目として暗記するより、攻撃とセットで理解するのがおすすめです。

---

## 前後の章

- 前へ ← [⑦ シングルログアウト（SLO）](07-slo.md)
- [シリーズの目次に戻る](README.md)
