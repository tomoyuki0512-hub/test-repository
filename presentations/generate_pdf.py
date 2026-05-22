#!/usr/bin/env python3
"""光ファイバー スライドの内容を日本語PDF（16:9・1スライド1ページ）で生成する。"""
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

FONT = "HeiseiKakuGo-W5"
pdfmetrics.registerFont(UnicodeCIDFont(FONT))

IN = 72.0
PAGE_W, PAGE_H = 13.333 * IN, 7.5 * IN

NAVY = HexColor("#1F3A5F")
BLUE = HexColor("#2E6DB4")
LIGHT = HexColor("#EDF3FA")
GRAY = HexColor("#444444")
CFE0F2 = HexColor("#CFE0F2")
GOLD = HexColor("#D8B840")
CORE_Y = HexColor("#FFF3C4")
RED = HexColor("#D12E2E")
PALEBLUE = HexColor("#CFE0F2")

OUT = "/home/user/test-repository/presentations/optical-fiber-presentation.pdf"
c = canvas.Canvas(OUT, pagesize=(PAGE_W, PAGE_H))


# ---- coordinate helpers (top-left inch based) ----
def X(v):
    return v * IN


def box(L, T, W, H):
    """rect from top-left inch coords -> reportlab bottom-left points."""
    return X(L), PAGE_H - (T + H) * IN, W * IN, H * IN


def text_tl(L, T, s, size, color=GRAY, align="l", bold_box=None):
    c.setFont(FONT, size)
    c.setFillColor(color)
    y = PAGE_H - T * IN - size * 0.82
    if align == "c":
        c.drawCentredString(X(L), y, s)
    elif align == "r":
        c.drawRightString(X(L), y, s)
    else:
        c.drawString(X(L), y, s)


def wrap(text, size, max_w_pt):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if cur and pdfmetrics.stringWidth(cur + ch, FONT, size) > max_w_pt:
            lines.append(cur); cur = ch
        else:
            cur += ch
    lines.append(cur)
    return lines


def fill_rect(L, T, W, H, color, stroke=None, lw=1):
    x, y, w, h = box(L, T, W, H)
    c.setFillColor(color)
    if stroke is not None:
        c.setStrokeColor(stroke); c.setLineWidth(lw)
    c.rect(x, y, w, h, stroke=1 if stroke is not None else 0, fill=1)


# ---- page templates ----
def title_page(title, subtitle, footer):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    text_tl(0.9, 2.7, title, 40, white)
    text_tl(0.9, 3.7, subtitle, 20, HexColor("#CFE0F2"))
    text_tl(0.9, 6.7, footer, 13, HexColor("#9FB6D0"))
    c.showPage()


def section_page(num, title):
    c.setFillColor(BLUE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    text_tl(0.95, 2.9, num, 22, HexColor("#CFE0F2"))
    text_tl(0.95, 3.5, title, 38, white)
    c.showPage()


def header(title):
    c.setFillColor(white); c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    fill_rect(0, 0, 13.333, 1.05, NAVY)
    text_tl(0.5, 0.32, title, 24, white)


def draw_bullets(items, L, T, W, size, gap=0.16):
    y = T
    for text, level in items:
        sz = size - level * 2
        indent = level * 0.34
        prefix = "• " if level == 0 else "–  "
        pw = pdfmetrics.stringWidth(prefix, FONT, sz)
        avail = (W - indent) * IN - pw
        lines = wrap(text, sz, avail)
        for k, ln in enumerate(lines):
            if k == 0:
                text_tl(L + indent, y, prefix, sz, NAVY if level == 0 else BLUE)
                c.setFont(FONT, sz); c.setFillColor(GRAY)
                c.drawString(X(L + indent) + pw, PAGE_H - y * IN - sz * 0.82, ln)
            else:
                c.setFont(FONT, sz); c.setFillColor(GRAY)
                c.drawString(X(L + indent) + pw, PAGE_H - y * IN - sz * 0.82, ln)
            y += (sz + 5) / IN
        y += gap


def draw_table(headers, rows, L, T, W, col_fracs, fsize):
    ncol = len(headers)
    col_w = [W * f for f in col_fracs]
    pad = 0.09
    lh = (fsize + 4) / IN

    def cell_lines(val, j):
        return wrap(val, fsize, (col_w[j] - 2 * pad) * IN)

    def row_height(cells):
        return max(len(cell_lines(v, j)) for j, v in enumerate(cells)) * lh + 2 * pad

    y = T
    # header
    hh = row_height(headers)
    x = L
    for j, htext in enumerate(headers):
        fill_rect(x, y, col_w[j], hh, NAVY, stroke=white, lw=0.7)
        text_tl(x + col_w[j] / 2, y + pad, htext, fsize, white, align="c")
        x += col_w[j]
    y += hh
    # body
    for i, row in enumerate(rows):
        rh = row_height(row)
        x = L
        for j, val in enumerate(row):
            bg = LIGHT if i % 2 == 0 else white
            fill_rect(x, y, col_w[j], rh, bg, stroke=HexColor("#C9D6E5"), lw=0.6)
            lines = cell_lines(val, j)
            ty = y + pad
            col = NAVY if j == 0 else GRAY
            for ln in lines:
                text_tl(x + pad, ty, ln, fsize, col)
                ty += lh
            x += col_w[j]
        y += rh


def legend(L, T, items, size=12):
    sw, gap = 0.24, 0.46
    for i, (color, text) in enumerate(items):
        y = T + i * gap
        fill_rect(L, y, sw, sw, color, stroke=NAVY, lw=0.5)
        text_tl(L + sw + 0.12, y - 0.01, text, size, GRAY)


# ---- diagrams ----
def draw_tir(L, T, W, H):
    x, y, w, h = box(L, T, W, H)
    c.setFillColor(CFE0F2); c.setStrokeColor(NAVY); c.setLineWidth(1.25)
    c.roundRect(x, y, w, h, 8, stroke=1, fill=1)
    core_h = H * 0.46
    core_top = T + (H - core_h) / 2
    cx0, cy0, cw0, ch0 = box(L, core_top, W, core_h)
    c.setFillColor(CORE_Y); c.setStrokeColor(GOLD); c.setLineWidth(0.75)
    c.rect(cx0, cy0, cw0, ch0, stroke=1, fill=1)
    # zigzag
    y_hi, y_lo = core_top, core_top + core_h
    y_mid = core_top + core_h / 2
    n = 4
    xs = [L + W * i / n for i in range(n + 1)]
    pts = [(L, y_mid)]
    for i in range(1, n):
        pts.append((xs[i], y_hi if i % 2 == 1 else y_lo))
    pts.append((L + W, y_mid))
    c.setStrokeColor(RED); c.setLineWidth(2.5)
    for i in range(len(pts) - 1):
        x1, t1 = pts[i]; x2, t2 = pts[i + 1]
        c.line(X(x1), PAGE_H - t1 * IN, X(x2), PAGE_H - t2 * IN)
    # bounce dots
    c.setFillColor(RED)
    for i in range(1, n):
        mx = xs[i]; mt = y_hi if i % 2 == 1 else y_lo
        c.circle(X(mx), PAGE_H - mt * IN, 0.05 * IN, stroke=0, fill=1)
    # arrowhead at right-mid
    xe, ye = X(L + W), PAGE_H - y_mid * IN
    ah = 0.14 * IN
    p = c.beginPath(); p.moveTo(xe, ye)
    p.lineTo(xe - ah, ye + ah * 0.55); p.lineTo(xe - ah, ye - ah * 0.55); p.close()
    c.drawPath(p, stroke=0, fill=1)
    text_tl(L + 0.12, T + 0.05, "クラッド（跳ね返す壁）", 11, NAVY)
    text_tl(L + W / 2, y_lo + 0.04, "コア（光の通り道）", 11, HexColor("#B89010"), align="c")


def draw_cross_section(cx, cy, outer_d):
    layers = [
        (outer_d, HexColor("#DDE3EA"), NAVY),
        (outer_d * 0.72, HexColor("#BFD6EE"), BLUE),
        (outer_d * 0.34, HexColor("#FFEC99"), GOLD),
    ]
    pcx, pcy = X(cx), PAGE_H - cy * IN
    for d, fill, stroke in layers:
        c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(1.25)
        c.circle(pcx, pcy, d / 2 * IN, stroke=1, fill=1)


# ====================== build deck ======================
title_page(
    "光ファイバー 完全ガイド",
    "第1部：基礎のしくみ ／ 第2部：ケーブル・コードと接続部材",
    "出典：docs/optical-fiber-guide.md・docs/optical-fiber-cable-types.md をまとめたスライド版",
)

header("目次（アジェンダ）")
draw_bullets([
    ("第1部　光ファイバーの基礎", 0),
    ("光ファイバーとは／なぜ光を使うのか", 1),
    ("全反射のしくみ／3層構造", 1),
    ("シングルモードとマルチモード", 1),
    ("データの流れ・メリデメ・身近な用途", 1),
    ("第2部　ケーブル・コードと接続部材", 0),
    ("テープスロット型 vs 層より型ケーブル", 1),
    ("単心／メガネ／FOコードの違い", 1),
    ("ケーブルとコードの違い", 1),
    ("成端箱とクロージャ／コネクタと規格", 1),
    ("付録：用語集", 0),
], 0.7, 1.35, 12.0, 18)
c.showPage()

section_page("第1部", "光ファイバーの基礎")

header("光ファイバーとは？（ざっくり結論）")
draw_bullets([
    ("髪の毛ほどの細さ（約0.125mm）の「ガラスの糸」", 0),
    ("中を光（点いた/消えた）が通り、1と0でデータを運ぶ", 0),
    ("速くて遠くまで弱まりにくい → 大量・高速・長距離", 0),
    ("家の光回線・海底ケーブル・データセンターの土台", 0),
    ("イメージ：光のモールス信号をガラスのストロー内で高速点滅", 0),
], 0.7, 1.6, 12.0, 20)
c.showPage()

header("なぜ電気でなく「光」を使う？")
draw_table(["比較", "銅線（電気）", "光ファイバー（光）"], [
    ["速さ・容量", "限界がある", "けた違いに大きい"],
    ["遠くへ送る", "すぐ弱まる", "弱まりにくい"],
    ["ノイズ", "電磁波に弱い", "電気ノイズに強い"],
    ["盗聴", "されやすい", "されにくい"],
    ["重さ・太さ", "重く太い", "軽く細い"],
], 0.6, 1.45, 12.1, [0.25, 0.375, 0.375], 16)
c.showPage()

header("いちばん大事なしくみ：全反射")
draw_bullets([
    ("光は密度の違う物質の境目で曲がる/跳ね返る", 0),
    ("ある角度より浅いと100%跳ね返る ＝ 全反射", 0),
    ("たとえ：プールの底から水面を見ると底が鏡のように映る", 1),
    ("中心(コア)を外側(クラッド)で包む構造", 0),
    ("ジグザグに反射しながら進み曲げても漏れにくい", 0),
], 0.6, 1.55, 6.1, 18)
draw_tir(7.0, 2.3, 5.7, 2.3)
text_tl(9.85, 4.9, "▲ 光が全反射しながら進むようす", 13, NAVY, align="c")
c.showPage()

header("3層構造（輪切りにすると）")
draw_table(["部分", "役割", "たとえ"], [
    ["コア（芯）", "光が通る道（屈折率 高）", "水の通り道"],
    ["クラッド", "跳ね返す（屈折率 低）", "鏡の壁"],
    ["被覆", "傷・水・曲げから守る", "服・よろい"],
], 0.5, 1.55, 7.2, [0.24, 0.46, 0.30], 14)
draw_bullets([("ポイント：コア＞クラッドの屈折率差が全反射を生む", 0)], 0.5, 4.95, 7.2, 16)
text_tl(10.3, 1.5, "断面図（輪切り）", 15, NAVY, align="c")
draw_cross_section(10.3, 3.35, 2.6)
legend(8.55, 5.0, [
    (HexColor("#FFEC99"), "コア（光が通る芯）"),
    (HexColor("#BFD6EE"), "クラッド（跳ね返す層）"),
    (HexColor("#DDE3EA"), "被覆（保護の服）"),
])
c.showPage()

header("種類：シングルモード vs マルチモード")
draw_table(["", "シングルモード(SMF)", "マルチモード(MMF)"], [
    ["コア径", "細い（約9µm）", "太い（約50〜62.5µm）"],
    ["距離", "長距離が得意", "短距離向け"],
    ["容量", "非常に大きい", "大きい"],
    ["コスト", "機器が高め", "比較的安い"],
    ["主用途", "幹線・光回線・海底", "建物内・データセンター内"],
], 0.6, 1.45, 12.1, [0.22, 0.39, 0.39], 16)
c.showPage()

header("データの流れ：電気 → 光 → 電気")
draw_bullets([
    ("送信側：電気の1/0をレーザー/LEDの点滅に変換", 0),
    ("伝送中：光が全反射しながら高速で進む", 0),
    ("受信側：フォトダイオードが光を電気の1/0へ戻す", 0),
    ("長距離では中継器・光増幅器(EDFA)で光を増幅して届ける", 0),
], 0.7, 1.6, 12.0, 20)
c.showPage()

header("メリットとデメリット")
draw_table(["メリット", "デメリット"], [
    ["超高速・大容量", "折れ・急な曲げに弱い"],
    ["遠くまで届く（低減衰）", "接続作業がデリケート（専用工具）"],
    ["電気ノイズに強い", "電気（電力）は送れない"],
    ["軽くて細い", "端末で電気⇄光の変換機器が必要"],
    ["盗聴されにくい", "—"],
], 0.6, 1.45, 12.1, [0.5, 0.5], 16)
c.showPage()

header("身近な使われ方")
draw_bullets([
    ("家庭の光回線（FTTH）：電柱→家へ引込み、ONUで光⇄電気変換", 0),
    ("海底ケーブル：大陸間を結び国際通信を支える", 0),
    ("データセンター：サーバー同士を光で高速接続", 0),
    ("携帯基地局間：スマホの裏側も基地局間は光", 0),
    ("医療・工業：内視鏡、レーザー加工、センサーなど", 0),
], 0.7, 1.6, 12.0, 20)
c.showPage()

section_page("第2部", "ケーブル・コードと接続部材")

header("テープスロット型 vs 層より型ケーブル")
draw_table(["観点", "テープスロット型", "層より型（ストランド型）"], [
    ["心線の並べ方", "テープ心線を溝(スロット)に積層", "心線をテンションメンバ周りに層状撚り"],
    ["心数・密度", "超多心・高密度が得意", "中小心数向け"],
    ["接続作業", "多心一括融着で速い", "単心ごとに融着"],
    ["単心の分岐", "テープ単位(SZ撚りで中間分岐可)", "単心の識別・分岐がしやすい"],
    ["主用途", "幹線・大容量・地下管路", "中小規模配線・引き落とし"],
], 0.6, 1.45, 12.1, [0.19, 0.405, 0.405], 14)
c.showPage()

header("単心 / メガネ / FOコードの違い")
draw_table(["", "心線数", "形・特徴", "主な用途"], [
    ["単心コード", "1心", "円1つ。単方向(シンプレクス)", "機器接続・パッチ片側"],
    ["メガネコード", "2心", "8の字型。双方向・裂いて分離", "スイッチ／サーバー間"],
    ["FOコード", "4/8/12心", "テープ心線を1心ずつに展開(ファンアウト)", "架内配線・テープ心線の成端"],
], 0.6, 1.45, 12.1, [0.18, 0.13, 0.40, 0.29], 14)
draw_bullets([("FO＝Fiber Optic ではなく「ファンアウト(Fan-Out)」の略", 0)], 0.7, 4.5, 12.0, 18)
c.showPage()

header("ケーブルとコードの違い")
draw_table(["観点", "コード（cord）", "ケーブル（cable）"], [
    ["主な場所", "屋内・機器のそば", "屋外・長距離・幹線"],
    ["心数", "1〜十数心が中心", "数十〜数千心も"],
    ["強度部材", "アラミド繊維で軽く補強", "鋼線/FRPで頑丈に"],
    ["外被・耐性", "柔らかく取り回し重視", "厚く頑丈・防水耐候"],
    ["役割", "機器⇄配線盤の最後の区間", "区間と区間を結ぶ幹"],
], 0.6, 1.45, 12.1, [0.2, 0.4, 0.4], 15)
c.showPage()

header("成端箱とクロージャの違い")
draw_table(["観点", "成端箱", "クロージャ"], [
    ["位置", "ケーブルの端末", "ケーブルの途中"],
    ["主目的", "心線をコネクタ化(成端)して機器へ", "接続・分岐点を保護・収納"],
    ["設置場所", "屋内が中心", "屋外(架空・地中)が中心"],
    ["防水", "屋内前提(屋外型もあり)", "防水・防塵が前提"],
    ["イメージ", "配線盤/パッチパネル", "電線途中の保護ボックス"],
], 0.6, 1.45, 12.1, [0.19, 0.405, 0.405], 15)
c.showPage()

header("コネクタと規格（つなぎ口の種類）")
draw_table(["コネクタ", "形・固定方法", "よく見る場所"], [
    ["SC", "四角形・押して固定（プッシュプル）", "家庭のONU・通信機器"],
    ["LC", "SCを小型化・ツメで固定", "データセンター・スイッチ"],
    ["ST", "丸型・ひねって固定（バヨネット）", "古めの設備・LAN"],
    ["FC", "丸型・ねじで締めて固定", "計測器・産業用"],
], 0.9, 1.9, 11.5, [0.165, 0.495, 0.34], 17)
c.showPage()

header("まとめ")
draw_bullets([
    ("光ファイバー＝全反射で光を閉じ込めて運ぶガラスの糸", 0),
    ("コア径でシングルモード(長距離)／マルチモード(短距離)", 0),
    ("集合方式：テープスロット型(高密度)／層より型(分岐容易)", 0),
    ("コード：単心(1)・メガネ(2)・FO(テープ展開)で使い分け", 0),
    ("ケーブル=屋外頑丈多心／コード=屋内柔軟機器寄り", 0),
    ("成端箱=端末でコネクタ化／クロージャ=途中を防水保護", 0),
], 0.7, 1.5, 12.0, 20)
c.showPage()

section_page("付録", "用語集")

header("用語集 ①（基礎のことば）")
draw_table(["用語", "意味"], [
    ["コア", "光が通る中心の芯（屈折率 高）"],
    ["クラッド", "光をはね返す外側の層（屈折率 低）"],
    ["被覆／ジャケット", "傷・水・曲げから守る外装"],
    ["全反射", "光が境界で100%はね返る現象。伝送の基本原理"],
    ["屈折率", "光の曲がりやすさ。コア＞クラッド"],
    ["シングルモード(SMF)", "細い芯。長距離・大容量向き"],
    ["マルチモード(MMF)", "太い芯。短距離・低コスト向き"],
    ["減衰", "信号が進むうちに弱まること"],
    ["波長", "光の「色」にあたる性質（nmで表す）"],
    ["WDM", "複数波長を1本に多重して容量を増やす技術"],
], 0.6, 1.35, 12.1, [0.28, 0.72], 14)
c.showPage()

header("用語集 ②（機器・配線のことば）")
draw_table(["用語", "意味"], [
    ["FTTH", "家庭まで光ファイバを引く方式"],
    ["ONU", "家庭で光⇄電気を変換する装置"],
    ["EDFA", "光を直接増幅する装置（光増幅器の一種）"],
    ["テンションメンバ", "ケーブルの抗張力体（鋼線/FRPなどの強度部材）"],
    ["テープ心線", "複数心を並べてテープ状にした心線"],
    ["ファンアウト(FO)", "テープ心線を1心ずつのコネクタに展開すること"],
    ["成端", "心線をコネクタ化して端末を仕上げること"],
    ["ピグテール", "片端にコネクタが付いた短い心線"],
    ["融着接続", "ファイバ同士を熱で溶かして接続する方法"],
    ["クロージャ", "ケーブル途中の接続・分岐点を保護する箱"],
], 0.6, 1.35, 12.1, [0.28, 0.72], 14)
c.showPage()

c.save()
print("saved:", OUT)
