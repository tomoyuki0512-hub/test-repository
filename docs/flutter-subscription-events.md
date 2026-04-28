# サブスクリプション ステータス・イベント一覧

iOS（App Store Server Notifications）と Android（Google Play Pub/Sub）で発生するイベントの全一覧と、それぞれが発生するタイミングをまとめます。

---

## 1. iOS — App Store Server Notifications（V2）

App Store はサブスクリプションの状態変化を **JWS（JSON Web Signature）形式**でバックエンドへ通知します。  
通知は `notificationType`（大分類）と `subtype`（小分類）の組み合わせで構成されます。

### 1-1. イベント一覧

| notificationType | subtype | 発生タイミング |
|---|---|---|
| `SUBSCRIBED` | `INITIAL_BUY` | 新規サブスクリプション購入時 |
| `SUBSCRIBED` | `RESUBSCRIBE` | 期限切れ後または解約後に再サブスクリプション購入時 |
| `DID_RENEW` | `BILLING_RECOVERY` | Billing Retry 期間中に課金が回復（支払い成功）したとき |
| `DID_RENEW` | なし | 通常の自動更新が成功したとき（毎更新日） |
| `EXPIRED` | `VOLUNTARY` | ユーザーが解約し、期間終了後に失効したとき |
| `EXPIRED` | `BILLING_RETRY` | Billing Retry 期間（60日）を過ぎても回収できず失効したとき |
| `EXPIRED` | `PRICE_INCREASE` | 価格改定に同意せず期間終了後に失効したとき |
| `EXPIRED` | `PRODUCT_NOT_FOR_SALE` | プロダクトが販売停止になり更新できず失効したとき |
| `EXPIRED` | `CUSTOMER_CANCELLED` | ユーザーがAppleサポート経由でキャンセルして即時失効したとき |
| `DID_FAIL_TO_RENEW` | `GRACE_PERIOD` | 更新日に課金が失敗し、Grace Period に入ったとき |
| `DID_FAIL_TO_RENEW` | なし | 更新日に課金が失敗し、Grace Period なしで Billing Retry に入ったとき |
| `GRACE_PERIOD_EXPIRED` | なし | Grace Period が終了しても支払いが回収できなかったとき |
| `DID_CHANGE_RENEWAL_STATUS` | `AUTO_RENEW_ENABLED` | ユーザーが一度解約した後、自動更新を再度ONにしたとき |
| `DID_CHANGE_RENEWAL_STATUS` | `AUTO_RENEW_DISABLED` | ユーザーがサブスクを解約操作（自動更新OFF）したとき |
| `DID_CHANGE_RENEWAL_PREF` | `UPGRADE` | 同一グループ内で上位プランへ変更したとき（即時反映） |
| `DID_CHANGE_RENEWAL_PREF` | `DOWNGRADE` | 同一グループ内で下位プランへ変更したとき（次回更新時に反映） |
| `DID_CHANGE_RENEWAL_PREF` | なし | 同一グループ内で同ランクのプランへ変更したとき |
| `OFFER_REDEEMED` | `INITIAL_BUY` | 初回購入時にオファー（割引・無料）を適用したとき |
| `OFFER_REDEEMED` | `RESUBSCRIBE` | 再サブスク時にオファーを適用したとき |
| `OFFER_REDEEMED` | `UPGRADE` | アップグレード時にオファーを適用したとき |
| `OFFER_REDEEMED` | `DOWNGRADE` | ダウングレード時にオファーを適用したとき |
| `REFUND` | なし | Appleがユーザーへの返金を承認したとき |
| `REFUND_DECLINED` | なし | 開発者がCONSUMPTION_REQUESTで返金拒否を通知し、Appleが却下判断したとき |
| `REFUND_REVERSED` | なし | 一度承認された返金がチャージバック等で取り消されたとき |
| `CONSUMPTION_REQUEST` | なし | Appleが返金審査のため消費状況の報告を開発者へ求めたとき（消費型のみ） |
| `PRICE_INCREASE` | `PENDING` | 価格改定が設定され、ユーザーの同意待ち状態になったとき |
| `PRICE_INCREASE` | `ACCEPTED` | ユーザーが価格改定に同意したとき（または自動同意されたとき） |
| `RENEWAL_EXTENSION` | `SUMMARY` | 開発者が一括で更新日延長を実行し完了したとき |
| `RENEWAL_EXTENSION` | `FAILURE` | 更新日延長処理でエラーが発生したとき |
| `REVOKE` | なし | ファミリー共有メンバーのアクセスが取り消されたとき（購入者が解約・共有停止等） |
| `TEST` | なし | App Store Connect から手動でテスト通知を送信したとき |

### 1-2. ステータス遷移フロー（iOS）

```
新規購入
  └─ SUBSCRIBED / INITIAL_BUY
        │
        ▼（更新日）
  ┌─ 課金成功 → DID_RENEW ──────────────────────────────────┐
  │                                                           │
  └─ 課金失敗                                                 │
        │                                                     │
        ├─ Grace Period あり → DID_FAIL_TO_RENEW / GRACE_PERIOD
        │       │                                             │
        │       ├─ 回収成功 → DID_RENEW / BILLING_RECOVERY   │
        │       └─ 回収失敗 → GRACE_PERIOD_EXPIRED           │
        │                         │                          │
        └─ Grace Period なし      │                          │
                  │               ▼                          │
                  └──────→ Billing Retry（60日）            │
                                  │                          │
                                  ├─ 回収成功 → DID_RENEW / BILLING_RECOVERY
                                  └─ 60日超過 → EXPIRED / BILLING_RETRY

解約操作 → DID_CHANGE_RENEWAL_STATUS / AUTO_RENEW_DISABLED
  └─（期間終了後）→ EXPIRED / VOLUNTARY

返金 → REFUND
  └─（取り消し）→ REFUND_REVERSED
```

---

## 2. Android — Google Play Real-time Developer Notifications

Google Play は **Pub/Sub** を通じてバックエンドへ通知します。  
通知は `SubscriptionNotificationType`（数値）で種別を識別します。

### 2-1. イベント一覧

| 種別値 | 定数名 | 発生タイミング |
|---|---|---|
| 1 | `SUBSCRIPTION_RECOVERED` | Account Hold 中に支払いが回収され、サブスクが回復したとき |
| 2 | `SUBSCRIPTION_RENEWED` | 自動更新が成功したとき（毎更新日）、またはダウングレードが適用されたとき |
| 3 | `SUBSCRIPTION_CANCELED` | ユーザーがサブスクを解約操作したとき（期間内はまだアクティブ） |
| 4 | `SUBSCRIPTION_PURCHASED` | 新規サブスクリプションが購入されたとき |
| 5 | `SUBSCRIPTION_ON_HOLD` | Grace Period が終了しても回収できず、Account Hold に入ったとき |
| 6 | `SUBSCRIPTION_IN_GRACE_PERIOD` | 更新日に課金が失敗し、Grace Period に入ったとき |
| 7 | `SUBSCRIPTION_RESTARTED` | 解約済み（期間内）のサブスクをユーザーが「再開」操作したとき |
| 8 | `SUBSCRIPTION_PRICE_CHANGE_CONFIRMED` | 価格改定にユーザーが同意したとき |
| 9 | `SUBSCRIPTION_DEFERRED` | 開発者が API でサブスクの更新日を延長したとき |
| 10 | `SUBSCRIPTION_PAUSED` | ユーザーがサブスクを一時停止したとき（Google Play Console で機能を有効化した場合のみ発生。デフォルトOFF） |
| 11 | `SUBSCRIPTION_PAUSE_SCHEDULE_CHANGED` | 一時停止のスケジュールが変更されたとき |
| 12 | `SUBSCRIPTION_REVOKED` | 開発者が API でサブスクを取り消したとき、またはGoogle Playが返金承認時にアクセス権を剥奪したとき |
| 13 | `SUBSCRIPTION_EXPIRED` | サブスクリプションが完全に失効したとき |
| 20 | `SUBSCRIPTION_PENDING_PURCHASE_CANCELED` | 保留中の購入（銀行振込等）がキャンセルされたとき |

### 2-2. ステータス遷移フロー（Android）

```
新規購入
  └─ SUBSCRIPTION_PURCHASED
        │
        ▼（更新日）
  ┌─ 課金成功 → SUBSCRIPTION_RENEWED ──────────────────────┐
  │                                                          │
  └─ 課金失敗                                                │
        │                                                    │
        ├─ Grace Period あり → SUBSCRIPTION_IN_GRACE_PERIOD  │
        │       │                                            │
        │       ├─ 回収成功 → SUBSCRIPTION_RENEWED          │
        │       └─ 回収失敗 → SUBSCRIPTION_ON_HOLD          │
        │                         │                         │
        └─ Grace Period なし      │                         │
                  │               ▼                         │
                  └──────→ Account Hold 中（リトライ継続）  │
                                  │                         │
                                  ├─ 回収成功 → SUBSCRIPTION_RECOVERED
                                  └─ 期限超過 → SUBSCRIPTION_EXPIRED

解約操作 → SUBSCRIPTION_CANCELED
  ├─（期間内に再開）→ SUBSCRIPTION_RESTARTED
  └─（期間終了）→ SUBSCRIPTION_EXPIRED

一時停止（ユーザー操作・要事前有効化）→ SUBSCRIPTION_PAUSED
  └─（再開日が来たとき）→ SUBSCRIPTION_RENEWED

取り消し → SUBSCRIPTION_REVOKED
  ├─（開発者が API で実行）
  └─（Google が返金承認時にアクセス権も剥奪）
        └─ SUBSCRIPTION_EXPIRED
```

### 2-3. 一時停止（SUBSCRIPTION_PAUSED）の詳細

| 項目 | 内容 |
|---|---|
| 操作主体 | ユーザー（Google Play のサブスク管理画面から操作） |
| 前提条件 | Google Play Console でサブスク商品ごとに「一時停止を許可する」を**有効化**する必要あり（デフォルト: OFF） |
| 停止期間 | ユーザーが 1・2・3 ヶ月から選択 |
| 課金 | 一時停止中は課金されない。再開日から通常課金が再開 |
| アクセス権 | 一時停止中はアクセスを停止する（`SUBSCRIPTION_PAUSED` 受信後にブロック） |
| 再開 | 設定した再開日が来ると自動的に `SUBSCRIPTION_RENEWED` が発生してアクセス復元 |
| ユーザーによる早期再開 | Google Play から手動で再開可能。その場合も `SUBSCRIPTION_RENEWED` が通知される |
| スケジュール変更 | 再開日を変更した場合は `SUBSCRIPTION_PAUSE_SCHEDULE_CHANGED` が発生 |

### 2-4. 強制取り消し（SUBSCRIPTION_REVOKED）の詳細

`SUBSCRIPTION_REVOKED` が発生するケースは2種類あります。

| ケース | 操作主体 | 内容 |
|---|---|---|
| 開発者による取り消し | 開発者 | Google Play Developer API の `purchases.subscriptions.revoke` を呼び出す。即時にサブスクが失効しアクセス権が剥奪される |
| Google による返金＋失効 | Google（ユーザーが返金申請） | ユーザーがGoogle Playサポートに返金申請し、Googleが承認した際にアクセス権も同時に剥奪するケース。返金のみ（アクセス継続）の場合はこのイベントは発生しない |

**`SUBSCRIPTION_REVOKED` 受信後の対応：** 即座にアクセスを停止し、`SUBSCRIPTION_EXPIRED` が続いて通知される（または内部的に失効扱いになる）。

---

## 3. iOS / Android 対応イベント比較

| ライフサイクルの状態 | iOS イベント | Android イベント |
|---|---|---|
| 新規購入 | `SUBSCRIBED / INITIAL_BUY` | `SUBSCRIPTION_PURCHASED` |
| 自動更新成功 | `DID_RENEW` | `SUBSCRIPTION_RENEWED` |
| 課金失敗 → Grace Period 開始 | `DID_FAIL_TO_RENEW / GRACE_PERIOD` | `SUBSCRIPTION_IN_GRACE_PERIOD` |
| Grace Period 終了（未回収） | `GRACE_PERIOD_EXPIRED` | `SUBSCRIPTION_ON_HOLD` |
| 課金回復 | `DID_RENEW / BILLING_RECOVERY` | `SUBSCRIPTION_RECOVERED` |
| 最終失効 | `EXPIRED / BILLING_RETRY` | `SUBSCRIPTION_EXPIRED` |
| 解約操作 | `DID_CHANGE_RENEWAL_STATUS / AUTO_RENEW_DISABLED` | `SUBSCRIPTION_CANCELED` |
| 解約後に再開 | `DID_CHANGE_RENEWAL_STATUS / AUTO_RENEW_ENABLED` | `SUBSCRIPTION_RESTARTED` |
| 再サブスク購入 | `SUBSCRIBED / RESUBSCRIBE` | `SUBSCRIPTION_PURCHASED` |
| アップグレード | `DID_CHANGE_RENEWAL_PREF / UPGRADE` | `SUBSCRIPTION_RENEWED`（即時適用後） |
| ダウングレード | `DID_CHANGE_RENEWAL_PREF / DOWNGRADE` | `SUBSCRIPTION_RENEWED`（次回更新時） |
| 返金 | `REFUND` | `SUBSCRIPTION_REVOKED` |
| 一時停止 | なし（iOS非対応） | `SUBSCRIPTION_PAUSED` |
| 価格改定の同意 | `PRICE_INCREASE / ACCEPTED` | `SUBSCRIPTION_PRICE_CHANGE_CONFIRMED` |
| ファミリー共有の取り消し | `REVOKE` | なし（Android非対応） |

---

## 4. RevenueCat を使う場合の対応

RevenueCat を使う場合、ストア固有のイベントは RevenueCat が抽象化し、統一された Webhook イベントとして配信されます。

| RevenueCat Webhook イベント | 対応するストアイベント |
|---|---|
| `INITIAL_PURCHASE` | iOS: `SUBSCRIBED/INITIAL_BUY` / Android: `SUBSCRIPTION_PURCHASED` |
| `RENEWAL` | iOS: `DID_RENEW` / Android: `SUBSCRIPTION_RENEWED` |
| `CANCELLATION` | iOS: `DID_CHANGE_RENEWAL_STATUS/AUTO_RENEW_DISABLED` / Android: `SUBSCRIPTION_CANCELED` |
| `UNCANCELLATION` | iOS: `AUTO_RENEW_ENABLED` / Android: `SUBSCRIPTION_RESTARTED` |
| `BILLING_ISSUE` | iOS: `DID_FAIL_TO_RENEW` / Android: `SUBSCRIPTION_IN_GRACE_PERIOD` |
| `SUBSCRIBER_ALIAS` | 内部のユーザーID統合（ストアイベントなし） |
| `EXPIRATION` | iOS: `EXPIRED` / Android: `SUBSCRIPTION_EXPIRED` |
| `PRODUCT_CHANGE` | iOS: `DID_CHANGE_RENEWAL_PREF` / Android: プラン変更通知 |
| `TRANSFER` | ユーザー間の権利移転（ストアイベントなし） |
| `REFUND` | iOS: `REFUND` / Android: `SUBSCRIPTION_REVOKED` |
