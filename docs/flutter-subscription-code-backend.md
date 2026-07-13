---
title: サブスクリプション実装コード例（バックエンド側）
---

# サブスクリプション実装コード例 — バックエンド側（検証・Webhook・権利管理）

[システム構成設計](flutter-subscription-system-design.md)で定義したエンドポイント・テーブルを実装するコード例です。**Node.js（Express）＋公式ライブラリ**を使いますが、処理の構造（コメント参照）は他言語でも同じです。

> Flutter側の実装は [Flutter編](flutter-subscription-code-client.md)、処理の流れは[シーケンス図集](subscription-sequence-diagrams.md)の①③④⑤を参照。

**使用ライブラリ**

```bash
npm install @apple/app-store-server-library   # Apple公式（JWS検証・Server API）
npm install googleapis google-auth-library    # Google公式（Play Developer API・OIDC検証）
```

---

## 1. iOS — App Store Server API クライアントとJWS検証

Apple公式の [`app-store-server-library`](https://github.com/apple/app-store-server-library-node) を使うと、**JWTによるAPI認証**と**JWS署名検証（証明書チェーン検証）**を自前実装せずに済みます。

```js
// apple.js
const {
  AppStoreServerAPIClient, Environment, SignedDataVerifier,
} = require('@apple/app-store-server-library');
const fs = require('fs');

// App Store Connect「ユーザーとアクセス > 統合 > アプリ内課金」で発行したキー
const issuerId = process.env.APPLE_ISSUER_ID;
const keyId = process.env.APPLE_KEY_ID;
const bundleId = 'com.example.app';
const privateKey = fs.readFileSync(process.env.APPLE_KEY_PATH, 'utf8'); // .p8
const env = Environment.PRODUCTION; // Sandboxテスト時は Environment.SANDBOX

const apiClient = new AppStoreServerAPIClient(privateKey, keyId, issuerId, bundleId, env);

// Apple Root CA証明書（https://www.apple.com/certificateauthority/ から取得して同梱）
const appleRootCAs = [
  fs.readFileSync('certs/AppleRootCA-G3.cer'),
  fs.readFileSync('certs/AppleRootCA-G2.cer'),
];
const verifier = new SignedDataVerifier(
  appleRootCAs, /* enableOnlineChecks */ true, env, bundleId,
);

module.exports = { apiClient, verifier };
```

---

## 2. Android — Play Developer API クライアント

サービスアカウント（[構成設計 4-2](flutter-subscription-system-design.md)の手順で作成）で認証します。

```js
// google.js
const { google } = require('googleapis');

const auth = new google.auth.GoogleAuth({
  keyFile: process.env.GOOGLE_SA_KEY_PATH, // サービスアカウントJSON
  scopes: ['https://www.googleapis.com/auth/androidpublisher'],
});
const androidpublisher = google.androidpublisher({ version: 'v3', auth });
const packageName = 'com.example.app';

module.exports = { androidpublisher, packageName };
```

---

## 3. ステータスマッピング（ストア → DB）

ストアの状態を `subscriptions.status`（[構成設計 2-1](flutter-subscription-system-design.md)の定義値）へ変換します。**変換ロジックを1関数に集約**しておくと、Webhook・検証・リコンサイルのすべてで同じ判定が使えます。

```js
// iOS: Get All Subscription Statuses の status 値 → DB status
function mapIosStatus(status, renewalInfo) {
  switch (status) {
    case 1: // Active（解約予約中も1のまま）
      return renewalInfo.autoRenewStatus === 0 ? 'CANCELED' : 'ACTIVE';
    case 2: return 'EXPIRED';
    case 3: return 'BILLING_RETRY';
    case 4: return 'GRACE_PERIOD';
    case 5: return 'REVOKED';
    default: return 'EXPIRED'; // 未知の値は安全側に倒す
  }
}

// Android: subscriptionsv2.get の subscriptionState → DB status
function mapAndroidStatus(state) {
  return {
    SUBSCRIPTION_STATE_ACTIVE: 'ACTIVE',
    SUBSCRIPTION_STATE_CANCELED: 'CANCELED',
    SUBSCRIPTION_STATE_IN_GRACE_PERIOD: 'GRACE_PERIOD',
    SUBSCRIPTION_STATE_ON_HOLD: 'ACCOUNT_HOLD',
    SUBSCRIPTION_STATE_PAUSED: 'PAUSED',
    SUBSCRIPTION_STATE_EXPIRED: 'EXPIRED',
  }[state] ?? 'EXPIRED';
}
```

---

## 4. POST `/api/subscriptions/verify` — 購入検証

シーケンス図①の「検証 → 権利UPSERT →（Androidのみ）acknowledge」を実装します。

```js
app.post('/api/subscriptions/verify', authenticate, async (req, res) => {
  const { platform, productId, verificationData } = req.body;
  const userId = req.user.id;

  try {
    let entitlement;
    if (platform === 'ios') {
      entitlement = await verifyIos(userId, verificationData);
    } else {
      entitlement = await verifyAndroid(userId, productId, verificationData);
    }
    res.json(entitlement);
  } catch (e) {
    // 失敗も iap_receipts に FAILED で記録済み（監査・再検証用）
    res.status(422).json({ error: 'verification_failed' });
  }
});

async function verifyIos(userId, signedTransaction) {
  // ① JWS署名を検証してデコード（偽レシートはここで弾かれる）
  const tx = await verifier.verifyAndDecodeTransaction(signedTransaction);

  // ② 重複チェック（同じ transactionId の二重検証を防ぐ）
  if (await db.iapReceipts.exists({ transaction_id: tx.transactionId })) {
    return db.subscriptions.findByUser(userId, 'ios'); // 冪等: 既存の権利を返す
  }

  // ③ Server API で最新ステータスを取得（真実の源）
  const statuses = await apiClient.getAllSubscriptionStatuses(tx.originalTransactionId);
  const item = statuses.data[0].lastTransactions[0];
  const renewalInfo = await verifier.verifyAndDecodeRenewalInfo(item.signedRenewalInfo);
  const txInfo = await verifier.verifyAndDecodeTransaction(item.signedTransactionInfo);

  // ④ 記録と権利付与（同一トランザクション内で）
  return db.tx(async (t) => {
    await t.iapReceipts.insert({ user_id: userId, platform: 'ios',
      transaction_id: tx.transactionId,
      original_transaction_id: tx.originalTransactionId,
      product_id: tx.productId, verification_status: 'SUCCESS',
      verification_response: statuses, verified_at: new Date() });
    return t.subscriptions.upsert({           // UNIQUE(user_id, platform)
      user_id: userId, platform: 'ios',
      product_id: txInfo.productId,
      original_transaction_id: tx.originalTransactionId,
      status: mapIosStatus(item.status, renewalInfo),
      current_period_end: new Date(txInfo.expiresDate),
      auto_renew_status: renewalInfo.autoRenewStatus === 1 });
  });
}

async function verifyAndroid(userId, productId, verificationData) {
  const { purchaseToken } = JSON.parse(verificationData);

  // ① subscriptionsv2.get で検証＋最新状態取得（不正トークンはここで404）
  const { data: sub } = await androidpublisher.purchases.subscriptionsv2.get({
    packageName, token: purchaseToken,
  });

  // ② 再購入の場合、旧トークンの権利を無効化（重複権利の防止）
  if (sub.linkedPurchaseToken) {
    await db.subscriptions.expireByToken(sub.linkedPurchaseToken);
  }

  const lineItem = sub.lineItems[0];
  const entitlement = await db.subscriptions.upsert({
    user_id: userId, platform: 'android',
    product_id: lineItem.productId,
    purchase_token: purchaseToken,
    status: mapAndroidStatus(sub.subscriptionState),
    current_period_end: new Date(lineItem.expiryTime),
    auto_renew_status: lineItem.autoRenewingPlan?.autoRenewEnabled ?? false,
  });

  // ③ acknowledge（3日以内必須。冪等なので毎回呼んでよい）
  if (sub.acknowledgementState === 'ACKNOWLEDGEMENT_STATE_PENDING') {
    await androidpublisher.purchases.subscriptions.acknowledge({
      packageName, subscriptionId: lineItem.productId, token: purchaseToken,
    });
  }
  return entitlement;
}
```

---

## 5. POST `/webhook/apple` — App Store Server Notifications V2

シーケンス図③の実装です。**署名検証 → ログ → 即時200 → 状態確定** の順に処理します。

```js
app.post('/webhook/apple', async (req, res) => {
  let notification;
  try {
    // ① JWS署名検証（証明書チェーン＋bundleId＋環境の一致を確認）
    notification = await verifier.verifyAndDecodeNotification(req.body.signedPayload);
  } catch {
    return res.status(401).end(); // 偽の通知
  }

  // ② 冪等化: notificationUUID で重複を弾く
  const isNew = await db.subscriptionEvents.insertIfAbsent({
    dedupe_key: notification.notificationUUID,
    platform: 'ios',
    event_type: notification.notificationType,   // 例: DID_RENEW
    event_subtype: notification.subtype ?? null, // 例: BILLING_RECOVERY
    raw_payload: notification,
  });

  res.status(200).end(); // ③ 即時応答（Appleは失敗時に最大5回リトライ）

  if (!isNew) return; // 重複通知はログのみで終了

  // ④ 通知ペイロードは信用せず、Server APIで最新状態を取得して確定
  const txInfo = await verifier.verifyAndDecodeTransaction(
    notification.data.signedTransactionInfo);
  await refreshIosSubscription(txInfo.originalTransactionId);
});

// Webhook・リコンサイルの両方から呼ぶ共通処理
async function refreshIosSubscription(originalTransactionId) {
  const statuses = await apiClient.getAllSubscriptionStatuses(originalTransactionId);
  const item = statuses.data[0].lastTransactions[0];
  const renewalInfo = await verifier.verifyAndDecodeRenewalInfo(item.signedRenewalInfo);
  const txInfo = await verifier.verifyAndDecodeTransaction(item.signedTransactionInfo);

  await db.subscriptions.updateByOriginalTransactionId(originalTransactionId, {
    status: mapIosStatus(item.status, renewalInfo),
    current_period_end: new Date(txInfo.expiresDate),
    auto_renew_status: renewalInfo.autoRenewStatus === 1,
  });
}
```

---

## 6. POST `/webhook/google/pubsub` — RTDN（Pub/Sub push）

```js
const { OAuth2Client } = require('google-auth-library');
const oidcClient = new OAuth2Client();

app.post('/webhook/google/pubsub', async (req, res) => {
  // ① Pub/Sub push の OIDC トークンを検証（構成設計 5-2）
  try {
    const token = (req.headers.authorization ?? '').replace('Bearer ', '');
    const ticket = await oidcClient.verifyIdToken({
      idToken: token, audience: process.env.PUBSUB_PUSH_AUDIENCE,
    });
    if (ticket.getPayload().email !== process.env.PUBSUB_SA_EMAIL) throw new Error();
  } catch {
    return res.status(401).end();
  }

  // ② Base64デコード
  const payload = JSON.parse(
    Buffer.from(req.body.message.data, 'base64').toString('utf8'));

  // ③ 冪等化: Pub/Sub の messageId で重複を弾く
  const sn = payload.subscriptionNotification;
  const isNew = await db.subscriptionEvents.insertIfAbsent({
    dedupe_key: req.body.message.messageId,
    platform: 'android',
    event_type: String(sn?.notificationType ?? payload.testNotification ? 'TEST' : 'UNKNOWN'),
    purchase_token: sn?.purchaseToken ?? null,
    raw_payload: payload,
  });

  res.status(204).end(); // ④ 2xxで即時応答（返さないとPub/Subが再送し続ける）

  if (!isNew || !sn) return; // 重複・テスト通知はここまで

  // ⑤ 最新状態を取得して確定（通知タイプによる分岐はしない＝状態機械はストア側）
  const { data: sub } = await androidpublisher.purchases.subscriptionsv2.get({
    packageName, token: sn.purchaseToken,
  });
  await db.subscriptions.updateByPurchaseToken(sn.purchaseToken, {
    status: sub.subscriptionState === undefined && sn.notificationType === 12
      ? 'REVOKED' : mapAndroidStatus(sub.subscriptionState),
    current_period_end: new Date(sub.lineItems[0].expiryTime),
    purchase_token: sn.purchaseToken, // RENEWED時は新トークンに更新
  });
}
```

> **通知タイプで分岐しない設計について:** `notificationType` ごとに処理を書き分けると、順不同・欠落に弱くなります。**「通知はトリガー、状態は照会APIで確定」**に統一すると、未知の通知タイプが増えても壊れません（例外は `SUBSCRIPTION_REVOKED` (12) のような即時剥奪系のみ）。

---

## 7. 冪等化キーの持ち方

| プラットフォーム | 冪等化キー | 備考 |
| --- | --- | --- |
| iOS | `notificationUUID` | 通知ごとに一意。再送時も同じ値 |
| Android | Pub/Sub `message.messageId` | 配信ごとに一意 |

`subscription_events` に `dedupe_key UNIQUE` カラムを追加し、`INSERT ... ON CONFLICT DO NOTHING` の結果で新規/重複を判定するのが最も簡単です（[構成設計 2-2](flutter-subscription-system-design.md) の `is_duplicate` の実装方法）。

---

## 8. 定期リコンサイル（通知取りこぼし対策）

Webhookは欠落し得るため、**日次バッチで「まもなく期限切れ」のレコードをストアAPIと突き合わせ**ます。実装・運用手順は[運用ガイド](flutter-subscription-operations.md)にまとめています。

```js
// 毎日実行: 期限が近い/過ぎたのにACTIVE系のままのレコードを再照会
const stale = await db.subscriptions.find({
  status: ['ACTIVE', 'GRACE_PERIOD', 'CANCELED'],
  current_period_end: { lt: addDays(new Date(), 1) },
});
for (const s of stale) {
  s.platform === 'ios'
    ? await refreshIosSubscription(s.original_transaction_id)
    : await refreshAndroidSubscription(s.purchase_token);
}
```

## 関連ドキュメント

- [実装コード例：Flutter編](flutter-subscription-code-client.md)
- [システム構成設計（DB・API・セキュリティ）](flutter-subscription-system-design.md)
- [シーケンス図集](subscription-sequence-diagrams.md) ／ [イベント一覧](flutter-subscription-events.md)
- [運用ガイド（リコンサイル・監視・返金対応）](flutter-subscription-operations.md)

## 出典・参考リンク（公式情報）

- Apple: [app-store-server-library-node](https://github.com/apple/app-store-server-library-node) ／ [App Store Server API](https://developer.apple.com/documentation/appstoreserverapi) ／ [App Store Server Notifications V2](https://developer.apple.com/documentation/appstoreservernotifications)
- Google: [purchases.subscriptionsv2](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2) ／ [RTDN リファレンス](https://developer.android.com/google/play/billing/rtdn-reference?hl=ja) ／ [Pub/Sub push 認証](https://cloud.google.com/pubsub/docs/authenticate-push-subscriptions)

> **更新日:** 2026-07-13
