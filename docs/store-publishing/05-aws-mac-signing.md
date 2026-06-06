---
title: AWSでMacを起動してストア資材を準備する（EC2 Mac 署名ガイド）
---

# AWSでMacを起動してストア資材を準備する（EC2 Mac 署名ガイド）

「iOSアプリを出したいけど手元にMacが無い」を解決する方法のひとつが **AWS の EC2 Mac インスタンス** です。
クラウド上で本物のMacを起動し、**Xcodeでのビルド・証明書/プロファイルの署名・notarization（公証）・App Store Connectへのアップロード** までを行えます。

このページでは、ゼロからEC2 Macを立ち上げてストア資材を準備する流れをまとめます。
（公開フロー全体は [Apple 公開フロー](01-apple-app-store.md) を参照）

---

## 0. 前提：そもそもなぜ「AWSのMac」なのか

iOSアプリの署名・ビルド・提出には **macOS + Xcode が実質必須**（[Apple公開フロー](01-apple-app-store.md) 参照）。Macを持っていない/CIで使いたい場合に、AWSがクラウドでMacを貸してくれます。

| 方法 | 向いている人 |
|---|---|
| 手元のMac | すでにMacがある人（最も安い・簡単） |
| **AWS EC2 Mac**（本ページ） | Macが無い／CIに組み込みたい／一時的に使いたい人 |
| その他クラウドMac（MacStadium等） | 同上の代替サービス |

> **重要な注意（先に把握）:** EC2 Mac は **専用ホスト（Dedicated Host）上でしか動かず、Appleのライセンス条件により最低24時間は確保（課金）される** 仕組みです。「数分だけ使ってすぐ解放」はできません。**思ったより高くつきやすい**ので、コスト感を最初に押さえてください（[後述](#9-料金とコストの注意)）。

---

## 1. 全体の流れ（8ステップ）

```
① 事前準備（AWSアカウント・Apple Developer登録・キーペア）
        ▼
② Dedicated Host（Mac専用ホスト）を割り当て
        ▼
③ EC2 Mac インスタンスを起動（macOS AMIを選択）
        ▼
④ 接続（SSH → 画面操作はVNC/画面共有）
        ▼
⑤ Xcode をインストール・初期設定
        ▼
⑥ 署名資材を準備（証明書・App ID・プロファイル）
        ▼
⑦ ビルド → アーカイブ → 署名 →（必要なら）公証
        ▼
⑧ App Store Connect へアップロード → ホスト解放（コスト停止）
```

---

## 2. ステップ①：事前準備

| 必要なもの | 内容 |
|---|---|
| AWSアカウント | 課金可能な状態。EC2 Mac利用には**上限緩和（クォータ申請）が必要なことが多い** |
| Apple Developer Program | 年99USD（[Apple公開フロー](01-apple-app-store.md) 参照） |
| SSHキーペア | EC2接続用。AWSコンソールで作成しておく |
| 対象リージョン | EC2 Macが提供されているリージョンを選ぶ |
| インスタンスタイプの選定 | `mac2`（Apple M1）, `mac2-m2`, `mac2-m2pro` 等のApple Silicon系を推奨（Intelの`mac1`より新しいSDKに対応しやすい） |

> **クォータ申請:** 初めてEC2 Macを使う場合、「Dedicated Hosts: 該当ファミリー」の上限が0のことがあります。Service Quotas から事前に緩和申請を出しておきましょう（承認に時間がかかる場合あり）。

---

## 3. ステップ②：Dedicated Host を割り当て

EC2 Mac は通常のEC2と違い、**まず物理ホストを確保**します。

1. EC2コンソール →「Dedicated Hosts」→「Dedicated Host を割り当て」
2. インスタンスファミリー（例 `mac2`）とアベイラビリティゾーンを選択
3. 割り当て完了（**ここから24時間の最低課金が始まる**点に注意）

---

## 4. ステップ③：EC2 Mac インスタンスを起動

1. EC2 →「インスタンスを起動」
2. **AMI**: macOS（Sonoma / Ventura など、使いたいXcodeに対応するバージョン）を選択
3. **インスタンスタイプ**: 割り当てたホストに合うもの（例 `mac2.metal`）
4. **テナンシー**: 「専有ホスト（Dedicated Host）」を選び、②で割り当てたホストを指定
5. キーペア・セキュリティグループ（自分のIPからのSSH/VNCのみ許可）・ストレージ（EBS、Xcodeは大きいので余裕を持って）を設定
6. 起動 → ステータスチェック通過まで待つ

---

## 5. ステップ④：接続する

### まずSSHで接続

```bash
ssh -i /path/to/key.pem ec2-user@<パブリックIP>
```

### GUI（Xcodeの一部操作）にはVNC＝画面共有

1. SSHで接続後、VNC用パスワードを設定し画面共有を有効化
   ```bash
   # 例：ec2-user のパスワード設定
   sudo /usr/bin/dscl . -passwd /Users/ec2-user <新パスワード>
   # 画面共有(ARD)を有効化（公式手順に従う）
   ```
2. ローカルからSSHポートフォワーディングでVNCトンネルを張る
   ```bash
   ssh -i key.pem -L 5900:localhost:5900 ec2-user@<パブリックIP>
   ```
3. Mac/Windowsの画面共有(VNC)クライアントで `localhost:5900` へ接続

> セキュリティ上、VNC(5900)はインターネットに直接開けず、**SSHトンネル越し**に使うのが安全です。

---

## 6. ステップ⑤：Xcode のインストール・初期設定

GUIで操作する場合:

1. App Store アプリにApple IDでサインインしてXcodeを入手、または Apple Developer サイトから `.xip` をダウンロード
2. インストール後、ライセンス同意・コマンドラインツール設定
   ```bash
   sudo xcodebuild -license accept
   xcode-select -p   # パスの確認
   ```
3. （CI/自動化なら）`xcodes` ツールでバージョン管理する方法も便利

> Xcodeは数十GBあるため、**EBSの容量**に注意。足りなければボリュームを拡張します。

---

## 7. ステップ⑥：署名資材を準備（証明書・App ID・プロファイル）

[Apple公開フロー ステップ②](01-apple-app-store.md) と同じ内容を、このMac上で行います。

| 資材 | 準備方法 |
|---|---|
| 配布用証明書（Distribution Certificate） | Xcodeの自動署名で生成、または Developerサイトで作成しキーチェーンに取り込み |
| App ID（Bundle ID） | Developerサイトで登録 |
| プロビジョニングプロファイル | 自動署名なら自動生成 |

### CI・自動化での署名（GUIを使わない場合）

ヘッドレス環境では **キーチェーンの操作**と**証明書/プロファイルの取り込み**をコマンドで行います。

```bash
# 一時キーチェーンを作成して署名証明書を取り込む例
security create-keychain -p "<pw>" build.keychain
security import dist_cert.p12 -k build.keychain -P "<p12pw>" -T /usr/bin/codesign
security list-keychains -s build.keychain
security unlock-keychain -p "<pw>" build.keychain
security set-key-partition-list -S apple-tool:,apple: -s -k "<pw>" build.keychain
```

> 証明書(`.p12`)やApp Store Connect APIキーなどの**秘密情報は AWS Secrets Manager / SSM Parameter Store** に置き、インスタンスにIAMロールで読み込ませると安全です。

---

## 8. ステップ⑦〜⑧：ビルド → 署名 →（公証）→ アップロード

### ビルド & アーカイブ（CLI例）

```bash
# アーカイブ作成
xcodebuild -scheme MyApp -configuration Release \
  -archivePath build/MyApp.xcarchive archive

# IPAへエクスポート（ExportOptions.plistで署名方法を指定）
xcodebuild -exportArchive \
  -archivePath build/MyApp.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath build/
```

Flutterの場合は `flutter build ipa --export-options-plist=ExportOptions.plist` でも可。

### 公証（notarization）※Mac用アプリを直接配布する場合

App Store経由のiOSアプリでは通常不要ですが、**Mac用アプリをストア外で配布**する場合は公証が必要です。

```bash
xcrun notarytool submit MyApp.zip \
  --apple-id <AppleID> --team-id <TeamID> --password <App用パスワード> --wait
xcrun stapler staple MyApp.app
```

### App Store Connect へアップロード

```bash
# Transporter相当（altool は非推奨化が進むため notarytool/altool/Transporter の最新手段を確認）
xcrun altool --upload-app -f build/MyApp.ipa -t ios \
  --apiKey <KeyID> --apiIssuer <IssuerID>
```

アップロード後は [Apple公開フロー ステップ⑤以降](01-apple-app-store.md)（掲載情報→審査→公開）へ進みます。

### ⑧ 終わったらホストを解放（コストを止める）

**ここが最重要。** 使い終わったら課金を止めます。

```
1. EC2インスタンスを終了（Terminate）
2. Dedicated Host を「解放（Release）」する
   ※ ただし最低割り当て24時間を経過しないと解放できない
```

> インスタンスを停止しただけでは**ホスト課金は止まりません**。**ホストの解放**まで行って初めてコストが止まります。

---

## 9. 料金とコストの注意

EC2 Macは一般的なEC2より高額です。コスト構造を理解しておきましょう。

| 課金要素 | 内容 |
|---|---|
| Dedicated Host 利用料 | **秒単位課金だが最低24時間が確保される**（Appleライセンス要件）。途中解放しても24時間分は課金 |
| EBSストレージ | Xcode用に大容量を確保した分 |
| データ転送 | アップロード/ダウンロード分 |

**コスト節約のコツ**
- 一度のセッションで**まとめて作業**する（24時間使い切る前提で計画）
- 継続利用ならEBSにXcode環境を残し、必要なときだけ使う運用も検討
- 使い終わったら**必ずホストを解放**（消し忘れが一番の事故）
- 単発・たまにしか使わないなら、**ローカルMac購入やGitHub Actions等のmacOSランナー**の方が安いこともある

---

## 10. AWS EC2 Mac の代替手段

| 手段 | 特徴 |
|---|---|
| **GitHub Actions（macOSランナー）** | CIでビルド・署名・提出を自動化。たまの提出なら手軽でコスト効率が良いことが多い |
| MacStadium / Mac専用クラウド | Mac特化のホスティング |
| 手元のMac mini等 | 頻繁に使うなら結局これが最安・最速なことも |

> 「**たまに提出するだけ**」なら GitHub Actions、「**常設のビルド基盤がほしい/AWS内で完結させたい**」なら EC2 Mac、と使い分けるのがおすすめです。

---

## 11. まとめ

- AWS EC2 Mac で、Macが無くても **ビルド・署名・公証・提出** が可能。
- 通常EC2と違い **Dedicated Host を確保 → 最低24時間課金** という独特の仕組み。
- 秘密情報（証明書・APIキー）は **Secrets Manager / SSM** に置き、VNCは **SSHトンネル越し**で安全に。
- **使い終わったらホストを解放**しないと課金が続く（最大の注意点）。
- 単発提出なら GitHub Actions などの代替も比較検討を。

---

## 出典・参考リンク（公式情報）

- AWS: [Amazon EC2 Mac インスタンス](https://aws.amazon.com/jp/ec2/instance-types/mac/) / [EC2 Mac ユーザーガイド](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-mac-instances.html) / [Dedicated Hosts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html)
- Apple: [App Store への提出](https://developer.apple.com/jp/app-store/submitting/) / [notarytool / 公証](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)
- 関連（本リポジトリ）: [Apple App Store 公開フロー](01-apple-app-store.md)

> **更新日:** 2026-06-06 ／ EC2 Macの料金・提供リージョン・対応AMI、Appleの署名/提出ツールは変動します。実作業前に必ず一次情報を確認してください。
</content>
