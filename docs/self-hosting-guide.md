---
title: 自作サーバーでWebサイトを公開する方法
---

# 自作サーバーでWebサイトを公開する方法

GitHub Pagesを使わず、自分でサーバーを用意してWebサイトを公開する方法まとめ。

---

## ドメインとIPアドレスは別々に調達する

お名前.comなどでドメインを取得しても、IPアドレスは含まれない。

```
ドメイン（お名前.com等）  ＝ 看板の「名前」だけ
サーバー（VPS等）        ＝ 実際にファイルを置く「土地」＋IPアドレス
```

この2つをDNSで紐付けることで、はじめてWebサイトが公開できる。

---

## 全体の流れ

```
① ドメイン取得（お名前.com等）
        +
② サーバーを借りる（VPS等）← IPアドレスが発行される
        ↓
③ DNSでドメイン → IPアドレスを紐付け（Aレコードを設定）
        ↓
④ サーバーにWebサーバー（Nginx等）を立てる
        ↓
⑤ HTMLファイルを置く
        ↓
⑥ Let's EncryptでHTTPS化（certbotが自動で行う）
        ↓
⑦ 完成：https://mysite.com でアクセスできる
```

GitHub Pagesは③〜⑥を全部やってくれるサービス。自作の場合はこれを自分でやる。

---

## サーバーの種類と比較

| 種類 | 例 | 費用 | 難易度 | 向いている用途 |
|---|---|---|---|---|
| **レンタルサーバー** | さくら、Xserver、ConoHa | 月500〜1,000円 | 低 | 小規模HP・ブログ |
| **VPS** | さくらVPS、ConoHa VPS、Vultr | 月500〜2,000円 | 中 | 自由にカスタマイズしたいとき |
| **クラウド（AWS等）** | AWS EC2、GCP、Azure | 使った分だけ | 高 | 大規模・本番環境 |
| **AWS S3** | S3 + CloudFront | 月数十円〜 | 中 | 静的サイト・GitHub Pagesの代替 |
| **自宅サーバー** | 自分のPC | 電気代のみ | 高 | 勉強・実験用 |

### レンタルサーバーとVPSの違い

| | レンタルサーバー | VPS |
|---|---|---|
| サーバーの管理 | 業者がやってくれる | 自分でやる |
| 自由度 | 低い（決まった機能のみ） | 高い（何でもできる） |
| 初心者向け | ○ | △ |
| 学習になるか | △ | ○ |

---

## AWS S3でWebサイトを公開する

### S3にはIPアドレスがない

S3は通常のサーバーと違い、**固定IPアドレスが発行されない**。URLでアクセスするサービスで、裏側では複数のIPが動的に使われている。

```
通常のサーバー → IPアドレスが1つ固定で発行される
S3             → URLが発行される（例：バケット名.s3.amazonaws.com）
```

### AWSのサービスとIPアドレスの関係

| AWSサービス | IPアドレス | 用途 |
|---|---|---|
| **EC2** | あり（Elastic IPで固定も可能） | 仮想サーバー・VPSに相当 |
| **S3** | なし（URL形式） | ファイル置き場・静的サイト |
| **CloudFront** | なし（URL形式・CDN） | S3の前に置いてHTTPS・高速化 |
| **ALB/ELB** | なし（URL形式） | 複数EC2への振り分け |

### S3で静的サイトを公開する構成

```
独自ドメイン
    ↓ CNAME
CloudFront（HTTPS・CDN・カスタムドメイン対応）
    ↓
S3バケット（HTMLファイルを置く場所）
```

GitHub Pagesに近い使い方ができ、大量アクセスにも強い。費用は月数十円〜。

### S3のDNS設定

IPアドレスがないためAレコードではなくCNAMEを使う：

| 種別 | ホスト名 | 値 |
|---|---|---|
| CNAME | www | バケット名.s3-website-ap-northeast-1.amazonaws.com |

**注意：** rootドメイン（`example.com` そのもの）にはCNAMEが設定できないため、CloudFrontを経由するかRoute 53（AWSのDNSサービス）のAlias機能を使う必要がある。

---

## VPSを使った公開手順（具体例）

### 1. VPSを借りる

ConoHa VPS（月880円〜）などでアカウントを作り、サーバーを追加するとIPアドレスが発行される。

### 2. AレコードをVPSのIPに設定

ドメイン登録サービスのDNS設定画面で：

| 種別 | ホスト名 | 値 |
|---|---|---|
| A | @ | VPSのIPアドレス（例：203.0.113.1） |
| A | www | VPSのIPアドレス（例：203.0.113.1） |

### 3. VPSにNginxをインストール

VPSにSSHで接続し、Webサーバーをインストールする。

```bash
# Ubuntu/Debianの場合
sudo apt update
sudo apt install nginx

# Nginxを起動
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 4. HTMLファイルを配置

```bash
# Webサイトのファイルをここに置く
/var/www/html/index.html
```

### 5. Let's EncryptでHTTPS化

```bash
# certbotをインストール
sudo apt install certbot python3-certbot-nginx

# 証明書を取得（ドメインを指定）
sudo certbot --nginx -d mysite.com -d www.mysite.com
```

certbotが自動でNginxの設定を書き換え、証明書の自動更新も設定してくれる。

---

## 自宅サーバーの場合：DDNSが必要な理由

### 問題：自宅のIPアドレスは毎日変わる

一般家庭のインターネット回線は、ルーターを再起動したり接続し直したりするたびにIPアドレスが変わる（**動的IP**）。

```
月曜日：自宅のIP = 203.0.113.10
火曜日：自宅のIP = 203.0.113.55（変わった！）
水曜日：自宅のIP = 203.0.113.23（また変わった！）
```

DNSのAレコードに固定のIPを設定しても、翌日には別のIPになってしまうためサイトにアクセスできなくなる。

### 解決策1：固定IPオプション（ISPに申し込む）

プロバイダ（NTT、ソフトバンク等）に固定IPオプションを申し込むと、常に同じIPアドレスが使える。

- 費用：月数百円〜数千円
- 手間：申し込むだけ
- デメリット：費用がかかる

### 解決策2：DDNS（Dynamic DNS）を使う

**DDNS（ダイナミックDNS）**は、IPアドレスが変わるたびに自動でDNSを更新してくれるサービス。

---

## DDNSの使い方（詳細）

### DDNSの仕組み

```
① 自宅PCが「今の自分のIPアドレスは何？」と確認
        ↓
② IPが変わっていたら、DDNSサービスに「IPが変わったよ」と通知
        ↓
③ DDNSサービスがDNSのAレコードを自動で更新
        ↓
④ ドメインが常に最新のIPを向き続ける
```

### 主なDDNSサービス

| サービス | 費用 | 特徴 |
|---|---|---|
| **Cloudflare（DDNSとして使う）** | 無料 | 高機能・安定・おすすめ |
| **No-IP** | 無料プランあり | 老舗・使いやすい |
| **DynDNS（Dyn）** | 有料 | 老舗だが有料化 |
| **MyDNS.jp** | 無料 | 日本向け・日本語OK |
| **ieServer.net** | 無料 | 日本向け |

### CloudflareでDDNSを設定する方法（おすすめ）

Cloudflareは本来DNS管理サービスだが、APIを使ってIPアドレスを自動更新することでDDNSとして使える。

#### 手順1：Cloudflareにドメインを追加

1. Cloudflare（cloudflare.com）でアカウント作成
2. 「Add a Site」でドメインを追加
3. ドメイン登録サービス側のNSレコードをCloudflareのものに変更

#### 手順2：APIトークンを取得

1. Cloudflareの右上アイコン → 「My Profile」
2. 「API Tokens」→「Create Token」
3. 「Edit zone DNS」テンプレートを選択して作成
4. 表示されたトークンをメモしておく

#### 手順3：自動更新スクリプトを設定

自宅PCにDDNSクライアントをインストールする。

**cloudflare-ddns（Linuxの場合）：**

```bash
# インストール
sudo apt install curl

# IPを自動更新するスクリプトを作成
cat << 'EOF' > ~/ddns-update.sh
#!/bin/bash
# 設定
API_TOKEN="あなたのAPIトークン"
ZONE_ID="CloudflareのゾーンID"
RECORD_ID="DNSレコードのID"
DOMAIN="mysite.com"

# 現在のIPアドレスを取得
CURRENT_IP=$(curl -s https://api.ipify.org)

# CloudflareのAレコードを更新
curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records/${RECORD_ID}" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data "{\"type\":\"A\",\"name\":\"${DOMAIN}\",\"content\":\"${CURRENT_IP}\",\"ttl\":60}"
EOF

chmod +x ~/ddns-update.sh
```

**5分ごとに自動実行する設定（cron）：**

```bash
# crontabを開く
crontab -e

# 以下を追記（5分ごとに実行）
*/5 * * * * ~/ddns-update.sh
```

**Windowsの場合（DDNSクライアントソフト）：**

- **DDclient**：Linux/Windows対応の定番DDNSクライアント
- **DDNS-Updater**（GUIあり）：Dockerで動かせる便利なツール

#### 手順4：動作確認

```bash
# 現在の自宅のIPを確認
curl https://api.ipify.org

# CloudflareのDNSを確認（変更が反映されているか）
nslookup mysite.com 1.1.1.1
```

---

### No-IPでDDNSを設定する方法（初心者向け）

No-IPは専用クライアントソフトがあり、設定が簡単。

#### 手順1：No-IPでアカウント作成・ホスト名取得

1. No-IP（noip.com）でアカウント作成
2. 「Dynamic DNS」→「No-IP Hostnames」→「Create Hostname」
3. ホスト名を入力（例：`mysite.ddns.net`）
4. ドメインの種類は無料の `.ddns.net` などを選ぶ

#### 手順2：No-IP DUC（クライアントソフト）をインストール

- **Windows**：No-IPのサイトからDUC（Dynamic Update Client）をダウンロードしてインストール
- **Mac/Linux**：コマンドラインでインストール可能

**Windowsでの設定：**

1. DUCを起動してNo-IPのアカウントでログイン
2. 更新するホスト名にチェックを入れる
3. 「Save」をクリック

これだけでIPが変わるたびに自動更新される。

#### 手順3：独自ドメインとNo-IPを紐付ける

お名前.comなどで取得したドメインのCNAMEレコードをNo-IPのホスト名に向ける：

| 種別 | ホスト名 | 値 |
|---|---|---|
| CNAME | @ または www | mysite.ddns.net |

---

## 自宅サーバーを使う場合の注意点

| 注意点 | 内容 |
|---|---|
| **セキュリティ** | 外部に公開するため、ファイアウォールの設定が必須 |
| **停電・再起動** | 自宅PCが止まるとサイトも止まる |
| **回線速度** | 自宅回線の上り速度がサイトの表示速度に影響する |
| **プロバイダの規約** | 一部のプロバイダはサーバー公開を禁止している場合がある（規約を確認）|
| **電気代** | 24時間稼働させると月数百〜数千円の電気代がかかる |

---

## まとめ：どれを選ぶべきか

| 状況 | おすすめ |
|---|---|
| とにかく簡単に公開したい | GitHub Pages（無料） |
| 独自ドメイン＋お手軽 | Netlify / Vercel（無料プランあり） |
| 本格的に自分で管理したい | VPS（月500円〜） |
| 勉強・実験目的 | 自宅サーバー＋DDNS |
| 動的IP問題を解決したい | DDNS（Cloudflare推奨） |
