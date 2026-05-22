#!/usr/bin/env python3
"""光ファイバー2ガイドをまとめたパワポを生成する。"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

JP_FONT = "Meiryo"
NAVY = RGBColor(0x1F, 0x3A, 0x5F)
BLUE = RGBColor(0x2E, 0x6D, 0xB4)
LIGHT = RGBColor(0xED, 0xF3, 0xFA)
GRAY = RGBColor(0x44, 0x44, 0x44)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def set_font(run, size=18, bold=False, color=GRAY, font=JP_FONT):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def add_bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def title_slide(title, subtitle, footer):
    slide = prs.slides.add_slide(BLANK)
    add_bg(slide, NAVY)
    # band
    band = slide.shapes.add_textbox(Inches(0.8), Inches(2.4), Inches(11.7), Inches(2.0))
    tf = band.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = title
    set_font(r, 44, True, WHITE)
    p2 = tf.add_paragraph()
    r = p2.add_run(); r.text = subtitle
    set_font(r, 22, False, RGBColor(0xCF, 0xE0, 0xF2))
    f = slide.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.6))
    p = f.text_frame.paragraphs[0]
    r = p.add_run(); r.text = footer
    set_font(r, 14, False, RGBColor(0x9F, 0xB6, 0xD0))
    return slide


def section_slide(num, title):
    slide = prs.slides.add_slide(BLANK)
    add_bg(slide, BLUE)
    box = slide.shapes.add_textbox(Inches(0.9), Inches(2.9), Inches(11.5), Inches(1.8))
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = num
    set_font(r, 24, True, RGBColor(0xCF, 0xE0, 0xF2))
    p2 = tf.add_paragraph()
    r = p2.add_run(); r.text = title
    set_font(r, 40, True, WHITE)
    return slide


def content_slide(title):
    slide = prs.slides.add_slide(BLANK)
    add_bg(slide, WHITE)
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), SW, Inches(1.05))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    tb = bar.text_frame; tb.word_wrap = True
    tb.margin_left = Inches(0.5); tb.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tb.paragraphs[0]
    r = p.add_run(); r.text = title
    set_font(r, 26, True, WHITE)
    return slide


def add_bullets(slide, items, top=1.4, left=0.7, width=12.0, size=18):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5.6))
    tf = box.text_frame; tf.word_wrap = True
    first = True
    for text, level in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = level
        bullet = ("• " if level == 0 else "  – ") + text
        r = p.add_run(); r.text = bullet
        set_font(r, size - level * 2, level == 0 and False, GRAY)
        p.space_after = Pt(6)
    return box


def add_table(slide, headers, rows, top=1.45, left=0.6, width=12.1, height=4.8,
              col_widths=None, fsize=14):
    nrows = len(rows) + 1
    ncols = len(headers)
    gtbl = slide.shapes.add_table(nrows, ncols, Inches(left), Inches(top),
                                  Inches(width), Inches(height))
    tbl = gtbl.table
    if col_widths:
        for i, w in enumerate(col_widths):
            tbl.columns[i].width = Inches(w)
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        tf = cell.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = h
        set_font(r, fsize, True, WHITE)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT if i % 2 else WHITE
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run(); r.text = val
            set_font(r, fsize, j == 0, NAVY if j == 0 else GRAY)
    return tbl


# ---------- 1. Title ----------
title_slide(
    "光ファイバー 完全ガイド",
    "第1部：基礎のしくみ ／ 第2部：ケーブル・コードと接続部材",
    "出典：docs/optical-fiber-guide.md・docs/optical-fiber-cable-types.md をまとめたスライド版",
)

# ---------- 2. Agenda ----------
s = content_slide("目次（アジェンダ）")
add_bullets(s, [
    ("第1部　光ファイバーの基礎", 0),
    ("光ファイバーとは／なぜ光を使うのか", 1),
    ("全反射のしくみ／3層構造", 1),
    ("シングルモードとマルチモード", 1),
    ("データの流れ・メリデメ・身近な用途", 1),
    ("第2部　ケーブル・コードと接続部材", 0),
    ("テープスロット型 vs 層より型ケーブル", 1),
    ("単心／メガネ／FOコードの違い", 1),
    ("ケーブルとコードの違い", 1),
    ("成端箱とクロージャの違い", 1),
], top=1.5, size=20)

# ---------- Section 1 ----------
section_slide("第1部", "光ファイバーの基礎")

# 光ファイバーとは
s = content_slide("光ファイバーとは？（ざっくり結論）")
add_bullets(s, [
    ("髪の毛ほどの細さ（約0.125mm）の「ガラスの糸」", 0),
    ("中を光（点いた/消えた）が通り、1と0でデータを運ぶ", 0),
    ("速くて遠くまで弱まりにくい → 大量・高速・長距離", 0),
    ("家の光回線・海底ケーブル・データセンターの土台", 0),
    ("イメージ：光のモールス信号をガラスのストロー内で高速点滅", 0),
], top=1.6, size=20)

# なぜ光
s = content_slide("なぜ電気でなく「光」を使う？")
add_table(s,
    ["比較", "銅線（電気）", "光ファイバー（光）"],
    [
        ["速さ・容量", "限界がある", "けた違いに大きい"],
        ["遠くへ送る", "すぐ弱まる", "弱まりにくい"],
        ["ノイズ", "電磁波に弱い", "電気ノイズに強い"],
        ["盗聴", "されやすい", "されにくい"],
        ["重さ・太さ", "重く太い", "軽く細い"],
    ],
    col_widths=[3.0, 4.55, 4.55], fsize=16)

# 全反射
s = content_slide("いちばん大事なしくみ：全反射")
add_bullets(s, [
    ("光は密度の違う物質の境目で曲がる/跳ね返る", 0),
    ("ある角度より浅いと100%跳ね返る ＝ 全反射", 0),
    ("たとえ：プールの底から水面を見ると底が鏡のように映る", 1),
    ("ファイバーは「光が通る中心」を「跳ね返す外側」で包む", 0),
    ("光はジグザグに反射しながら進み、曲げても漏れにくい", 0),
], top=1.6, size=20)

# 構造
s = content_slide("3層構造（輪切りにすると）")
add_table(s,
    ["部分", "役割", "たとえ"],
    [
        ["コア（芯）", "光が通る道（屈折率 高）", "ストロー内の水の通り道"],
        ["クラッド", "光を逃がさず跳ね返す（屈折率 低）", "通り道を囲む鏡の壁"],
        ["被覆/ジャケット", "傷・水・曲げから守る", "ケーブルの服・よろい"],
    ],
    col_widths=[3.0, 5.1, 4.0], fsize=16, height=3.0)
add_bullets(s, [
    ("ポイント：コア＞クラッドの屈折率差が全反射を生む", 0),
], top=5.1, size=18)

# 種類
s = content_slide("種類：シングルモード vs マルチモード")
add_table(s,
    ["", "シングルモード(SMF)", "マルチモード(MMF)"],
    [
        ["コア径", "細い（約9µm）", "太い（約50〜62.5µm）"],
        ["距離", "長距離が得意", "短距離向け"],
        ["容量", "非常に大きい", "大きい"],
        ["コスト", "機器が高め", "比較的安い"],
        ["主用途", "幹線・光回線・海底", "建物内・データセンター内"],
    ],
    col_widths=[2.6, 4.75, 4.75], fsize=16)

# データの流れ
s = content_slide("データの流れ：電気 → 光 → 電気")
add_bullets(s, [
    ("送信側：電気の1/0をレーザー/LEDの点滅に変換", 0),
    ("伝送中：光が全反射しながら高速で進む", 0),
    ("受信側：フォトダイオードが光を電気の1/0へ戻す", 0),
    ("長距離では中継器・光増幅器(EDFA)で光を増幅して届ける", 0),
], top=1.6, size=20)

# メリデメ
s = content_slide("メリットとデメリット")
add_table(s,
    ["メリット", "デメリット"],
    [
        ["超高速・大容量", "折れ・急な曲げに弱い"],
        ["遠くまで届く（低減衰）", "接続作業がデリケート（専用工具）"],
        ["電気ノイズに強い", "電気（電力）は送れない"],
        ["軽くて細い", "端末で電気⇄光の変換機器が必要"],
        ["盗聴されにくい", ""],
    ],
    col_widths=[6.05, 6.05], fsize=16)

# 用途
s = content_slide("身近な使われ方")
add_bullets(s, [
    ("家庭の光回線（FTTH）：電柱→家へ引込み、ONUで光⇄電気変換", 0),
    ("海底ケーブル：大陸間を結び国際通信を支える", 0),
    ("データセンター：サーバー同士を光で高速接続", 0),
    ("携帯基地局間：スマホの裏側も基地局間は光", 0),
    ("医療・工業：内視鏡、レーザー加工、センサーなど", 0),
], top=1.6, size=20)

# ---------- Section 2 ----------
section_slide("第2部", "ケーブル・コードと接続部材")

# テープスロット vs 層より
s = content_slide("テープスロット型 vs 層より型ケーブル")
add_table(s,
    ["観点", "テープスロット型", "層より型（ストランド型）"],
    [
        ["心線の並べ方", "テープ心線を溝(スロット)に積層", "心線をテンションメンバ周りに層状撚り"],
        ["心数・密度", "超多心・高密度が得意", "中小心数向け"],
        ["接続作業", "多心一括融着で速い", "単心ごとに融着"],
        ["単心の分岐", "テープ単位(SZ撚りで中間分岐可)", "単心の識別・分岐がしやすい"],
        ["主用途", "幹線・大容量・地下管路", "中小規模配線・引き落とし"],
    ],
    col_widths=[2.3, 4.9, 4.9], fsize=14)

# コード3種
s = content_slide("単心 / メガネ / FOコードの違い")
add_table(s,
    ["", "心線数", "形・特徴", "主な用途"],
    [
        ["単心コード", "1心", "円1つ。単方向(シンプレクス)", "機器接続・パッチ片側"],
        ["メガネコード", "2心", "8の字型。双方向・裂いて分離", "スイッチ／サーバー間"],
        ["FOコード", "4/8/12心", "テープ心線を1心ずつに展開(ファンアウト)", "架内配線・テープ心線の成端"],
    ],
    col_widths=[2.2, 1.6, 4.8, 3.5], fsize=14, height=3.0)
add_bullets(s, [
    ("FO＝Fiber Optic ではなく「ファンアウト(Fan-Out)」の略", 0),
], top=4.9, size=18)

# ケーブルとコード
s = content_slide("ケーブルとコードの違い")
add_table(s,
    ["観点", "コード（cord）", "ケーブル（cable）"],
    [
        ["主な場所", "屋内・機器のそば", "屋外・長距離・幹線"],
        ["心数", "1〜十数心が中心", "数十〜数千心も"],
        ["強度部材", "アラミド繊維で軽く補強", "鋼線/FRPで頑丈に"],
        ["外被・耐性", "柔らかく取り回し重視", "厚く頑丈・防水耐候"],
        ["役割", "機器⇄配線盤の最後の区間", "区間と区間を結ぶ幹"],
    ],
    col_widths=[2.4, 4.85, 4.85], fsize=15)

# 成端箱とクロージャ
s = content_slide("成端箱とクロージャの違い")
add_table(s,
    ["観点", "成端箱", "クロージャ"],
    [
        ["位置", "ケーブルの端末", "ケーブルの途中"],
        ["主目的", "心線をコネクタ化(成端)して機器へ", "接続・分岐点を保護・収納"],
        ["設置場所", "屋内が中心", "屋外(架空・地中)が中心"],
        ["防水", "屋内前提(屋外型もあり)", "防水・防塵が前提"],
        ["イメージ", "配線盤/パッチパネル", "電線途中の保護ボックス"],
    ],
    col_widths=[2.3, 4.9, 4.9], fsize=15)

# まとめ
s = content_slide("まとめ")
add_bullets(s, [
    ("光ファイバー＝全反射で光を閉じ込めて運ぶガラスの糸", 0),
    ("コア径でシングルモード(長距離)／マルチモード(短距離)", 0),
    ("集合方式：テープスロット型(高密度)／層より型(分岐容易)", 0),
    ("コード：単心(1)・メガネ(2)・FO(テープ展開)で使い分け", 0),
    ("ケーブル=屋外頑丈多心／コード=屋内柔軟機器寄り", 0),
    ("成端箱=端末でコネクタ化／クロージャ=途中を防水保護", 0),
], top=1.5, size=20)

out = "/home/user/test-repository/presentations/optical-fiber-presentation.pptx"
prs.save(out)
print("saved:", out, "slides:", len(prs.slides._sldIdLst))
