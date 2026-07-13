---
title: サブスクリプション テスト・QAガイド
---

# サブスクリプション テスト・QAガイド（iOS Sandbox / Google Play テスト）

サブスクリプションの実装は**本番で初めて踏む地雷**が多い領域です（自動更新・課金失敗・返金は本番課金なしに再現しにくい）。このガイドは、iOS/Androidのテスト環境の使い方と、**[状態遷移図](ios-subscription-lifecycle.md)の遷移を1本ずつ潰していくチェックリスト**をまとめたものです。

> 基本の環境セットアップは[要件定義 5-3](flutter-subscription-guide.md)、実装は[コード例集（Flutter編](flutter-subscription-code-client.md)／[バックエンド編）](flutter-subscription-code-backend.md)を参照。

---

## 1. テスト環境の全体像

| | iOS | Android |
| --- | --- | --- |
| テスト環境 | **Sandbox**（App Store Connect） | **ライセンステスター**＋テストトラック |
| 事前準備 | Sandboxテスターアカウント作成 | Play Console「ライセンステスト」にGmail登録＋**内部テストトラックへアップロード** |
| 課金 | 実際の請求なし | 実際の請求なし（テストカード） |
| 実機/エミュレータ | **実機推奨**（シミュレータは制限あり） | 実機推奨（Play Store入りエミュレータでも可） |
| ローカル完結のモック | **StoreKit Testing**（Xcodeの`.storekit`設定ファイル） | なし（必ずPlayを経由） |
| サーバー通知のテスト | Sandbox用URLを別途設定＋テスト通知API | 本番と同じPub/Sub＋Play Consoleからテスト通知送信 |

---

## 2. iOS — Sandbox テストの実務

### 2-1. セットアップ

1. App Store Connect →「ユーザーとアクセス」→「Sandbox」→ **Sandboxテスターを作成**（本物のメールアドレス不要。`+`エイリアス可）
2. 実機の「設定 → App Store →（最下部）Sandboxアカウント」でサインイン
3. Xcodeからアプリをインストールして購入操作 → Sandbox価格表示（`[Environment: Sandbox]`）を確認

### 2-2. 更新期間の短縮（既定）

| 本番の期間 | Sandboxでの実時間 |
| --- | --- |
| 1週間 | 3分 |
| 1ヶ月 | 5分 |
| 2ヶ月 | 10分 |
| 3ヶ月 | 15分 |
| 6ヶ月 | 30分 |
| 1年 | 1時間 |

- **自動更新は最大12回**で停止 → その後 `EXPIRED` になる（失効テストに利用できる）
- App Store Connect の Sandbox テスター設定で**更新レートの変更**（さらに高速化）が可能

### 2-3. Sandboxテスターの便利機能（App Store Connect / 端末設定から）

| 機能 | 使いどころ |
| --- | --- |
| **購入履歴の消去**（Clear Purchase History） | 「初回購入」を何度でもテスト。イントロオファーの適用条件テストに必須 |
| **中断された購入**（Interrupted Purchases） | 購入フロー途中でストア側が追加操作を要求するケース。`purchaseStream` の取りこぼしテスト |
| **請求問題のシミュレーション**（Billing Problem） | **課金失敗 → Grace Period → Billing Retry** の遷移を実時間で再現 |
| アカウントの国/地域変更 | 価格・通貨表示のテスト |
| サブスクリプション管理画面 | 端末の設定アプリからSandboxサブスクの解約・再開・プラン変更が可能 |

### 2-4. StoreKit Testing（Xcodeローカルモック）

`.storekit` 構成ファイルを作ると**ネットワーク・App Store Connect登録なし**で購入UIを動かせます。単体・UIテストの高速化に有効ですが、**レシートがSandboxと異なりバックエンド検証は通らない**ため、結合テストはSandboxで行います。Xcodeの Transaction Manager から返金・期限切れ・オファーコード適用などを注入できます。

### 2-5. サーバー通知（ASSN V2）のテスト

1. App Store Connect →「App情報」→ **Sandbox用のServer Notification URL** を本番と別に設定
2. App Store Server API の **Request a Test Notification**（`POST /inApps/v1/notifications/test`）で疎通確認
3. Sandboxで購入→5分更新のたびに `DID_RENEW` が届くことを確認

---

## 3. Android — ライセンステスター＋テストトラックの実務

### 3-1. セットアップ

1. Play Console →「設定」→「ライセンステスト」→ テスターのGmailを登録（**テスト用の支払い方法**が使えるようになる）
2. **内部テストトラック**に `BILLING` 権限入りのビルドをアップロード（ローカルビルドだけでは購入テスト不可）
3. テスターをトラックに追加 → オプトインURLから参加 → Playストア経由でインストール

### 3-2. 更新期間の短縮（ライセンステスターのみ）

| 本番の期間 | テストでの実時間（目安） |
| --- | --- |
| 1週間 | 5分 |
| 1ヶ月 | 5分 |
| 3ヶ月 | 10分 |
| 6ヶ月 | 15分 |
| 1年 | 30分 |

- **猶予期間・Account Hold・一時停止も数分〜十数分に短縮**される（正確な値は[公式ドキュメント](https://developer.android.com/google/play/billing/test?hl=ja)で確認）

### 3-3. テストカードによる課金失敗の再現

ライセンステスターは購入時に支払い方法として**テストカード**を選べます。

| テストカード | 用途 |
| --- | --- |
| Test card, **always approves** | 正常系（購入・更新成功） |
| Test card, **always declines** | **更新失敗 → Grace Period → Account Hold** の遷移テスト |
| Slow test card（approves/declines after delay） | 保留(pending)購入・遅延決済のテスト |

「always approves」で購入 →購入後に「always declines」へ変更…はできないため、**更新失敗をテストする場合は最初から declines カードで購入**し、初回は成功・更新から失敗するシナリオは「approves」で購入後にストアの支払い方法を削除する等で再現します。

### 3-4. RTDNのテスト

1. Play Console →「収益化のセットアップ」→ RTDNトピック設定画面の **「テスト通知を送信」** で疎通確認（`TestNotification` が届く）
2. テスト購入 → 5分更新のたびに `SUBSCRIPTION_RENEWED` (2) が届くことを確認

---

## 4. 状態遷移テストチェックリスト

[iOS](ios-subscription-lifecycle.md)／[Android](android-subscription-lifecycle.md)の状態遷移図の**矢印を1本ずつ**テストします。「確認点」は共通で: ①アプリの画面表示 ②DBの `subscriptions.status` ③Webhookイベントの受信ログ、の3点です。

### 正常系

- [ ] **新規購入** — 購入→検証→権利付与→機能解放。`iap_receipts` に記録されること
- [ ] **自動更新**（5分待つ） — `DID_RENEW` / `RENEWED(2)` 受信で `current_period_end` が延びること
- [ ] **購入の復元** — 再インストール後に「購入を復元」で権利が戻ること
- [ ] **2台目の端末** — 同一ストアアカウントの別端末で復元できること
- [ ] **アプリ削除→権利継続** — アンインストールしても更新が続く（Webhookが届き続ける）こと

### 解約・再加入系

- [ ] **解約（期間内）** — ストアで解約→ `CANCELED` になり、**期限まで利用できる**こと
- [ ] **解約→期限内に再開** — iOS: 自動更新オン / Android: `RESTARTED(7)` で `ACTIVE` に戻ること
- [ ] **解約→失効** — 期限到来で `EXPIRED`・アクセス停止・ペイウォール表示
- [ ] **失効→再購入** — 再購入で復帰。**Android: 旧 `purchaseToken` の権利が無効化される**こと（`linkedPurchaseToken` 処理）

### 課金失敗系（iOS: Billing Problemシミュレーション / Android: declinesカード）

- [ ] **更新失敗→猶予期間** — `GRACE_PERIOD` になり**アクセス維持**＋バナー表示
- [ ] **猶予終了→停止** — `BILLING_RETRY` / `ACCOUNT_HOLD` で**アクセス即停止**＋全面ブロック画面
- [ ] **停止→回復** — 支払い解決で `DID_RENEW` / `RECOVERED(1)` → 即アクセス復元
- [ ] **停止→失効** — 未解決のまま期間終了で `EXPIRED`

### 例外系

- [ ] **返金・取り消し** — iOS: Transaction Managerで返金注入 / Android: Play Consoleから注文の返金＋取り消し → `REVOKED` で即停止
- [ ] **保留中の購入**（Android: slow test card） — `pending` 中に権利を付与しないこと・確定後に付与されること
- [ ] **中断された購入**（iOS: Interrupted Purchase） — 次回起動時に `purchaseStream` へ流れて完了できること
- [ ] **Webhook二重配信** — 同一通知を2回受けても権利が壊れないこと（`dedupe_key` の冪等化）
- [ ] **Webhook停止からの回復** — 受信エンドポイントを一時的に落とし、リトライ／[日次リコンサイル](flutter-subscription-operations.md)で追いつくこと
- [ ] **別アカウント紐付きの復元** — 他ユーザーの購入を復元した場合にポリシーどおり（付け替え/拒否）動くこと

### プラン変更系（複数プランがある場合）

- [ ] **アップグレード** — 即時適用・差額処理（iOS: グループ内ランク / Android: `changeSubscriptionParam`）
- [ ] **ダウングレード** — 次回更新日から適用されること

---

## 5. QA実施時の注意

- **Sandbox/テストの挙動は本番と完全一致ではない**（更新回数上限・時間短縮・通知順序など）。リリース直後は本番の少額プランで最終確認するのが安全。
- テスト用ユーザーのデータは本番DBに混ぜない（`platform` とは別に `is_sandbox` フラグ、または環境分離を推奨。iOSの通知には `environment: Sandbox` が入る）。
- 更新が5分で来るため、**テスト中はWebhookログが大量に積まれる**。`subscription_events` の肥大化に注意。

## 関連ドキュメント

- [イベント・ステータス一覧](flutter-subscription-events.md) ／ [状態遷移図 iOS](ios-subscription-lifecycle.md)・[Android](android-subscription-lifecycle.md)
- [実装コード例（Flutter](flutter-subscription-code-client.md)／[バックエンド）](flutter-subscription-code-backend.md)
- [運用ガイド（リコンサイル・監視）](flutter-subscription-operations.md)

## 出典・参考リンク（公式情報）

- Apple: [Testing in-app purchases with sandbox](https://developer.apple.com/documentation/storekit/testing-in-app-purchases-with-sandbox) ／ [Setting up StoreKit Testing in Xcode](https://developer.apple.com/documentation/xcode/setting-up-storekit-testing-in-xcode) ／ [Request a Test Notification](https://developer.apple.com/documentation/appstoreserverapi/request_a_test_notification)
- Google: [Google Play Billing のテスト](https://developer.android.com/google/play/billing/test?hl=ja) ／ [アプリライセンスでのテスト](https://support.google.com/googleplay/android-developer/answer/6062777?hl=ja)

> **更新日:** 2026-07-13 ／ 更新短縮時間・テスト機能はストア側の仕様変更が多いため、一次情報を必ず確認してください。
