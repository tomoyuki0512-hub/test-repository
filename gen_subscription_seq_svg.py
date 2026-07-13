#!/usr/bin/env python3
"""サブスクリプション主要フローのシーケンス図SVGを生成するスクリプト。

docs/subscription-sequence-diagrams.md から参照される以下のSVGを docs/ に出力する:
  - subscription-seq-purchase.svg        新規購入
  - subscription-seq-restore.svg         購入復元
  - subscription-seq-webhook.svg         Webhook受信→DB更新
  - subscription-seq-billing-failure.svg 課金失敗→回復
  - subscription-seq-refund.svg          返金・取り消し

実行: python3 gen_subscription_seq_svg.py
"""

import html
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

FONT = "'Helvetica Neue',Arial,'Hiragino Sans','Noto Sans JP',sans-serif"

# 登場人物ごとの配色（状態遷移図SVGと統一）
PALETTE = {
    "user":    ("#ede7f6", "#5e35b1", "#4527a0"),
    "app":     ("#e8f5e9", "#43a047", "#1b5e20"),
    "store":   ("#e3f2fd", "#1e88e5", "#0d47a1"),
    "backend": ("#fff3e0", "#fb8c00", "#bf360c"),
    "db":      ("#eceff1", "#78909c", "#37474f"),
}

P_W = 150      # 参加者ボックス幅
P_H = 46
GAP = 40       # ボックス間隔
TOP = 96       # ライフライン開始y
ROW_MSG = 40   # メッセージ1行の高さ
ROW_SELF = 46
ROW_NOTE = 34
ROW_PHASE = 34
MARGIN = 30


def esc(s):
    return html.escape(s, quote=True)


def build(title, subtitle, participants, events, filename):
    n = len(participants)
    width = MARGIN * 2 + n * P_W + (n - 1) * GAP
    xs = {}  # participant id -> lifeline x
    for i, (pid, _label, _pal) in enumerate(participants):
        xs[pid] = MARGIN + i * (P_W + GAP) + P_W // 2

    # 高さを先に計算
    y = TOP + 18
    for ev in events:
        kind = ev[0]
        y += {"msg": ROW_MSG, "self": ROW_SELF, "note": ROW_NOTE, "phase": ROW_PHASE}[kind]
    height = y + 30

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" style="max-width:{width}px;font-family:{FONT}">'
    )
    out.append('<defs>'
               '<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
               '<path d="M0,0 L10,5 L0,10 z" fill="#37474f"/></marker>'
               '<marker id="ad" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
               '<path d="M0,0 L10,5 L0,10 z" fill="#78909c"/></marker>'
               '</defs>')
    out.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>')
    out.append(f'<text x="{width//2}" y="26" font-size="16" font-weight="bold" fill="#263238" text-anchor="middle">{esc(title)}</text>')
    if subtitle:
        out.append(f'<text x="{width//2}" y="44" font-size="11" fill="#607d8b" text-anchor="middle">{esc(subtitle)}</text>')

    # ライフライン
    for pid, _label, _pal in participants:
        x = xs[pid]
        out.append(f'<line x1="{x}" y1="{TOP}" x2="{x}" y2="{height-24}" stroke="#cfd8dc" stroke-width="1.2" stroke-dasharray="4 4"/>')

    # 参加者ボックス
    for i, (pid, label, pal) in enumerate(participants):
        fill, stroke, tcol = PALETTE[pal]
        bx = MARGIN + i * (P_W + GAP)
        out.append(f'<rect x="{bx}" y="{TOP - P_H}" width="{P_W}" height="{P_H}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
        lines = label.split("\n")
        if len(lines) == 1:
            out.append(f'<text x="{bx + P_W//2}" y="{TOP - P_H//2 + 5}" font-size="12.5" font-weight="bold" fill="{tcol}" text-anchor="middle">{esc(lines[0])}</text>')
        else:
            out.append(f'<text x="{bx + P_W//2}" y="{TOP - P_H//2 - 2}" font-size="12" font-weight="bold" fill="{tcol}" text-anchor="middle">{esc(lines[0])}</text>')
            out.append(f'<text x="{bx + P_W//2}" y="{TOP - P_H//2 + 13}" font-size="10" fill="{tcol}" text-anchor="middle">{esc(lines[1])}</text>')

    # イベント
    y = TOP + 18
    for ev in events:
        kind = ev[0]
        if kind == "msg":
            _, src, dst, label, style = ev
            x1, x2 = xs[src], xs[dst]
            y += ROW_MSG
            mid = (x1 + x2) // 2
            dash = ' stroke-dasharray="5 4"' if style == "dashed" else ""
            col = "#78909c" if style == "dashed" else "#37474f"
            marker = "ad" if style == "dashed" else "a"
            out.append(f'<text x="{mid}" y="{y - 7}" font-size="11" fill="{col}" text-anchor="middle">{esc(label)}</text>')
            out.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="1.6"{dash} marker-end="url(#{marker})"/>')
        elif kind == "self":
            _, who, label = ev
            x = xs[who]
            y += ROW_SELF
            out.append(f'<path d="M{x},{y-22} C{x+56},{y-22} {x+56},{y} {x+6},{y}" fill="none" stroke="#37474f" stroke-width="1.6" marker-end="url(#a)"/>')
            out.append(f'<text x="{x + 64}" y="{y - 14}" font-size="11" fill="#37474f">{esc(label)}</text>')
        elif kind == "note":
            _, text = ev
            y += ROW_NOTE
            out.append(f'<rect x="{MARGIN + 16}" y="{y - 22}" width="{width - 2*(MARGIN+16)}" height="26" rx="5" fill="#fffde7" stroke="#f9a825" stroke-width="1"/>')
            out.append(f'<text x="{width//2}" y="{y - 5}" font-size="10.5" fill="#795548" text-anchor="middle">{esc(text)}</text>')
        elif kind == "phase":
            _, text = ev
            y += ROW_PHASE
            out.append(f'<rect x="{MARGIN}" y="{y - 22}" width="{width - 2*MARGIN}" height="26" rx="4" fill="#eceff1"/>')
            out.append(f'<text x="{width//2}" y="{y - 5}" font-size="11.5" font-weight="bold" fill="#455a64" text-anchor="middle">{esc(text)}</text>')

    out.append('</svg>')
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"wrote {path} ({width}x{height})")


# 共通の参加者セット
FULL = [
    ("user", "ユーザー", "user"),
    ("app", "Flutterアプリ\n(in_app_purchase)", "app"),
    ("store", "ストア\n(App Store / Play)", "store"),
    ("backend", "自前バックエンド", "backend"),
    ("db", "DB\n(subscriptions)", "db"),
]

# ① 新規購入
build(
    "① 新規購入フロー",
    "購入 → 検証 → 権利付与 → 完了確定（acknowledge / completePurchase）",
    FULL,
    [
        ("msg", "user", "app", "購入ボタンをタップ", "solid"),
        ("msg", "app", "store", "buyNonConsumable()（購入リクエスト）", "solid"),
        ("msg", "store", "user", "決済シート表示・認証", "solid"),
        ("msg", "user", "store", "支払い承認", "solid"),
        ("msg", "store", "app", "purchaseStream: PurchaseStatus.purchased", "dashed"),
        ("msg", "app", "backend", "POST /iap/verify（レシート / purchaseToken）", "solid"),
        ("msg", "backend", "store", "検証API（App Store Server API / subscriptionsv2.get）", "solid"),
        ("msg", "store", "backend", "ステータス・有効期限（expiryTime）", "dashed"),
        ("msg", "backend", "db", "権利をUPSERT（ACTIVE）", "solid"),
        ("msg", "backend", "store", "acknowledge（Androidのみ・3日以内必須）", "solid"),
        ("msg", "backend", "app", "200 OK（entitlement）", "dashed"),
        ("msg", "app", "store", "completePurchase()（完了通知・必須）", "solid"),
        ("msg", "app", "user", "プレミアム機能を解放", "solid"),
        ("note", "completePurchase / acknowledge を怠ると3日後に自動返金される（Android）"),
    ],
    "subscription-seq-purchase.svg",
)

# ② 購入復元
build(
    "② 購入復元（restorePurchases）フロー",
    "機種変更・再インストール時に権利を取り戻す（iOS審査要件）",
    FULL,
    [
        ("msg", "user", "app", "「購入を復元」をタップ", "solid"),
        ("msg", "app", "store", "restorePurchases()", "solid"),
        ("msg", "store", "app", "purchaseStream: PurchaseStatus.restored（過去の購入）", "dashed"),
        ("msg", "app", "backend", "POST /iap/verify（レシート / purchaseToken）", "solid"),
        ("msg", "backend", "store", "最新ステータスを照会", "solid"),
        ("msg", "store", "backend", "ACTIVE・有効期限", "dashed"),
        ("msg", "backend", "db", "user_id と購入情報を紐付け・権利UPSERT", "solid"),
        ("msg", "backend", "app", "200 OK（entitlement）", "dashed"),
        ("msg", "app", "user", "「購入を復元しました」", "solid"),
        ("note", "別ユーザーIDに紐付く購入が来た場合の扱い（付け替え/拒否）は事前にポリシーを決めておく"),
    ],
    "subscription-seq-restore.svg",
)

# ③ Webhook受信
build(
    "③ サーバー通知（Webhook）受信フロー",
    "iOS: App Store Server Notifications V2 ／ Android: RTDN（Cloud Pub/Sub push）",
    [
        ("store", "ストア\n(App Store / Play)", "store"),
        ("backend", "自前バックエンド\n(Webhook受信)", "backend"),
        ("db", "DB", "db"),
        ("app", "Flutterアプリ", "app"),
    ],
    [
        ("msg", "store", "backend", "POST（iOS: JWS / Android: Pub/Sub push）", "solid"),
        ("self", "backend", "署名検証（JWS証明書チェーン / Bearer Token）"),
        ("msg", "backend", "db", "subscription_events に生ペイロードをINSERT", "solid"),
        ("msg", "backend", "store", "200 OK（即時応答。重い処理は後段に回す）", "dashed"),
        ("msg", "backend", "store", "最新ステータスを照会（通知を鵜呑みにしない）", "solid"),
        ("msg", "store", "backend", "最新の状態・有効期限", "dashed"),
        ("msg", "backend", "db", "subscriptions.status を更新（冪等）", "solid"),
        ("phase", "―― 以降、アプリは起動時・フォアグラウンド復帰時に最新状態を取得 ――"),
        ("msg", "app", "backend", "GET /me/subscription", "solid"),
        ("msg", "backend", "app", "最新の権利（status・期限）", "dashed"),
        ("note", "通知は重複・順不同・欠落があり得る。必ず照会APIで状態を確定させ、DBを「正」とする"),
    ],
    "subscription-seq-webhook.svg",
)

# ④ 課金失敗→回復
build(
    "④ 課金失敗 → 猶予期間 → 停止 → 回復フロー",
    "iOS: GRACE_PERIOD → BILLING_RETRY ／ Android: IN_GRACE_PERIOD → ON_HOLD",
    FULL,
    [
        ("phase", "更新日：課金失敗（カード期限切れ等）"),
        ("msg", "store", "backend", "DID_FAIL_TO_RENEW / SUBSCRIPTION_IN_GRACE_PERIOD", "solid"),
        ("msg", "backend", "db", "status = GRACE_PERIOD（アクセスは維持）", "solid"),
        ("msg", "app", "user", "「お支払いに問題があります」バナー＋更新導線", "solid"),
        ("phase", "猶予期間終了：まだ未解決"),
        ("msg", "store", "backend", "GRACE_PERIOD_EXPIRED / SUBSCRIPTION_ON_HOLD", "solid"),
        ("msg", "backend", "db", "status = BILLING_RETRY / ON_HOLD（アクセス停止）", "solid"),
        ("msg", "app", "user", "全面ブロック画面＋支払い方法の更新導線", "solid"),
        ("phase", "ユーザーが支払い方法を修正"),
        ("msg", "user", "store", "ストアの設定で支払い方法を更新", "solid"),
        ("msg", "store", "backend", "DID_RENEW / SUBSCRIPTION_RECOVERED", "solid"),
        ("msg", "backend", "db", "status = ACTIVE（アクセス復元）", "solid"),
        ("msg", "app", "user", "「ご利用を再開しました」", "solid"),
        ("note", "猶予期間中のアクセス維持と支払い更新導線が解約防止の要（UX設計ガイド 第10章参照）"),
    ],
    "subscription-seq-billing-failure.svg",
)

# ⑤ 返金・取り消し
build(
    "⑤ 返金・取り消し（Revoke）フロー",
    "ユーザーはストアに直接返金申請する（開発者は関与できない）",
    FULL,
    [
        ("msg", "user", "store", "返金申請（ストアのサポート窓口へ直接）", "solid"),
        ("self", "store", "審査・承認"),
        ("msg", "store", "backend", "iOS: REFUND / REVOKE ・ Android: SUBSCRIPTION_REVOKED", "solid"),
        ("msg", "backend", "db", "status = REVOKED（権利を即時剥奪）", "solid"),
        ("msg", "backend", "db", "subscription_events に記録（返金率の分析用）", "solid"),
        ("msg", "app", "backend", "GET /me/subscription（起動時）", "solid"),
        ("msg", "backend", "app", "権利なし", "dashed"),
        ("msg", "app", "user", "利用終了の案内画面", "solid"),
        ("note", "iOSの REFUND（アクセス継続の返金）と REVOKE（権利剥奪）は別イベント。REVOKE のみ即時停止する"),
    ],
    "subscription-seq-refund.svg",
)
