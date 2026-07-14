---
title: ④ OpenID Connect（OIDC）を詳しく 〜現代SSOの主流〜
---

# ④ OpenID Connect（OIDC）を詳しく 〜現代SSOの主流〜

> **この章でわかること**
> - OIDCとは何か（＝OAuth 2.0＋ログイン機能）
> - IDトークン（JWT）の構造と、**手元で実際にデコードしてみる追体験**
> - **「Googleでログイン」の裏側をブラウザで覗く手順**
> - SAML / OAuth / OIDC の比較表と、迷わない選び方

---

## 1. OIDCとは

**OpenID Connect（オープンアイディーコネクト、OIDC）** は、**OAuth 2.0の上に「認証（ログイン）」の機能を正しく追加した**、現代SSOの主流プロトコルです（2014年標準化）。

> ひとことで：**OIDC ＝ OAuth 2.0 ＋ ログイン（本人確認）機能**

「Googleでログイン」「Appleでサインイン」などの**ソーシャルログイン**の多くはOIDCで動いています。[前章](03-oauth2.md)で見た「OAuth単体ログインのなりすまし問題」を、**IDトークン**という仕組みで解決したのがOIDCです。

### OAuthとの違いは「IDトークン」

| | OAuth 2.0 | OIDC |
| --- | --- | --- |
| 発行されるもの | アクセストークン | アクセストークン + **IDトークン** |
| トークンが答える問い | 「何ができるか」 | 「**誰がログインしたか**」も答えられる |
| 宛先の検証 | 標準では不可 | `aud` クレームで検証できる → 差し替え攻撃を検知 |

---

## 2. OIDCの流れ

基本はOAuthの認可コードフローと同じです。違いは `scope` に **`openid`** を含めること。これによりIDトークンが追加発行されます。

```mermaid
sequenceDiagram
    autonumber
    actor U as ユーザー(ブラウザ)
    participant RP as アプリ (RP)
    participant OP as IdP / OP<br/>例: Google

    U->>RP: 「Googleでログイン」を押す
    RP-->>U: 認可リクエスト(scope=openid email profile)で<br/>Googleへリダイレクト
    U->>OP: Googleアカウントでログイン・同意
    OP-->>U: 認可コードを付けてアプリへリダイレクト
    U->>RP: 認可コードがアプリに渡る
    rect rgb(230, 240, 255)
        Note over RP,OP: 裏側(サーバー間通信)
        RP->>OP: 認可コードを提出
        OP-->>RP: IDトークン + アクセストークンを発行
    end
    RP->>RP: IDトークン(JWT)の署名・iss・aud・expを検証
    RP-->>U: 「この人は本物」と確認 → ログイン完了!
```

*（図が表示されない環境用：[SVG版](svg/04-oidc-1.svg)）*

> 用語メモ：OIDCではSPのことを **RP（Relying Party）**、IdPのことを **OP（OpenID Provider）** と呼びます。役割は同じです。

---

## 3. IDトークンの正体：JWT

IDトークンの形式は **JWT（ジョット / JSON Web Token）**。`.`（ドット）で3つに区切られた文字列です。

```
ヘッダー.ペイロード.署名
eyJhbGc....eyJpc3M....SflKxwRJ...
```

| 部分 | 中身 | 暗号化されている？ |
| --- | --- | --- |
| ヘッダー | 署名アルゴリズムなどのメタ情報 | ❌ Base64エンコードのみ（**誰でも読める**） |
| ペイロード | クレーム（ユーザーID・名前・有効期限など） | ❌ 同上 |
| 署名 | 改ざん検知用のデジタル署名 | 🔏 IdPの秘密鍵で署名 |

> **重要**：JWTは「読めないように隠す」ものではなく「**改ざんされていないことを証明する**」ものです。だからペイロードに機密情報を入れてはいけません。

### 追体験：JWTを実際にデコードしてみよう

以下は本物と同じ構造のサンプルIDトークンです（署名部分はダミー）。

```
eyJhbGciOiJSUzI1NiIsImtpZCI6ImExYjJjM2Q0IiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJzdWIiOiIxMTAxNjk0ODQ0NzQzODYyNzYzMzQiLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJleHAiOjE3ODM5MzY4MDAsImlhdCI6MTc4MzkzMzIwMCwiZW1haWwiOiJ0YXJvLnlhbWFkYUBleGFtcGxlLmNvbSIsIm5hbWUiOiJUYXJvIFlhbWFkYSJ9.dummy-signature
```

Mac / Linux のターミナルで、1つ目の区切り（ヘッダー）をデコードしてみます：

```bash
echo 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImExYjJjM2Q0IiwidHlwIjoiSldUIn0=' | base64 -d
```

結果：

```json
{"alg":"RS256","kid":"a1b2c3d4","typ":"JWT"}
```

2つ目の区切り（ペイロード）も同様にデコードすると：

```json
{
  "iss": "https://accounts.google.com",
  "sub": "110169484474386276334",
  "aud": "407408718192.apps.googleusercontent.com",
  "exp": 1783936800,
  "iat": 1783933200,
  "email": "taro.yamada@example.com",
  "name": "Taro Yamada"
}
```

> コマンドが苦手な人は **[jwt.io](https://jwt.io)** にJWTを貼り付けるだけで中身を見られます（※本物のトークンを外部サイトに貼るのは避け、サンプルで試しましょう）。

### 主要クレームの読み方

| クレーム | 正式名 | 意味 | 検証で果たす役割 |
| --- | --- | --- | --- |
| `iss` | issuer | 発行者（どのIdPか） | 知らない発行者なら拒否 |
| `sub` | subject | ユーザーの一意なID | 「誰か」の本体。メールより不変で確実 |
| `aud` | audience | このトークンの宛先アプリ | **自分宛てでなければ拒否 → 差し替え攻撃を防ぐ** |
| `exp` / `iat` | expiration / issued at | 有効期限 / 発行時刻 | 期限切れ・古すぎるトークンを拒否 |
| `email`, `name` | — | ユーザー属性 | 画面表示やアカウント作成に利用 |

---

## 4. 追体験：「Googleでログイン」の裏側を覗いてみよう

OIDCは毎日あなたのブラウザの中で動いています。実際に観察してみましょう。

1. Chromeで適当なサイト（例：どこかの「Googleでログイン」があるサービス）を開く
2. **F12** で開発者ツールを開き、**Network** タブを選択
3. 「**Preserve log**（ログを保持）」にチェック（リダイレクトで消えないように）
4. 「Googleでログイン」ボタンを押す
5. Networkタブで `accounts.google.com` へのリクエストを探してクリック

すると、URLの中に前章で学んだパラメータがそのまま見えます：

```
https://accounts.google.com/o/oauth2/v2/auth
  ?client_id=...
  &redirect_uri=...
  &response_type=code
  &scope=openid email profile   ← ここに openid がある = OIDC!
  &state=...
```

- `scope` に `openid` が入っていれば、それは**OIDCによるログイン**です
- ログイン完了後、`redirect_uri` のアドレスに `code=...`（認可コード）付きで戻る様子も観察できます
- トークンへの交換はサーバーの裏側で行われるため、ブラウザからは見えません——それ自体が「安全設計が機能している」証拠です

---

## 5. SAML vs OAuth vs OIDC 比較

| 項目 | SAML 2.0 | OAuth 2.0 | OpenID Connect |
| --- | --- | --- | --- |
| 主目的 | 認証（SSO） | **認可**（権限委譲） | 認証（SSO） |
| データ形式 | XML | JSON / トークン | JSON（JWT） |
| 登場時期 | 2005年 | 2012年 | 2014年 |
| 得意分野 | 企業内・SaaS | API権限の委譲 | モバイル・SPA・ソーシャルログイン |
| トークン | SAMLアサーション | アクセストークン | IDトークン + アクセストークン |
| モバイル相性 | △ 弱い | ○ | ◎ 強い |
| 設定の手軽さ | △ やや複雑 | ○ | ○ |
| 代表例 | Salesforce連携 | 「フォトへのアクセスを許可」 | 「Googleでログイン」 |

### 迷わない選び方

```mermaid
flowchart TD
    Q1{何がしたい?} -->|社内の業務SaaSを<br/>まとめてSSO化| A1[SAML<br/>対応SaaSが最多。新しめのSaaSならOIDCも]
    Q1 -->|自社のWeb/モバイルアプリに<br/>ログイン機能を作る| A2[OIDC<br/>現代の標準。Auth0/Cognito等で楽に実装]
    Q1 -->|他社サービスのデータを<br/>読む権限だけ欲しい| A3[OAuth 2.0<br/>ログインではなく認可ならこれ]
    Q1 -->|ゼロから新規で迷ったら| A2
```

*（図が表示されない環境用：[SVG版](svg/04-oidc-2.svg)）*

---

## 前後の章

- 前へ ← [③ OAuth 2.0を詳しく](03-oauth2.md)
- 次へ → [⑤ セキュリティとMFA・パスキー](05-security-mfa.md)
- [シリーズの目次に戻る](README.md)
