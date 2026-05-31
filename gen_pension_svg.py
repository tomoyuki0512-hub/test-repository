#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""年金 繰上げ・繰下げ 図解(SVG入りMarkdown)生成スクリプト"""

H = 1578528   # 厚生年金(報酬比例 本来額) 平均標準報酬月額60万・40年
K = 831700    # 老齢基礎年金 満額(令和7年度)

R = {60:0.76, 65:1.00, 70:1.42, 72:1.588, 75:1.84}  # 繰上0.4%/月,繰下0.7%/月

def amt(base, age): return round(base*R[age])

# ---- 座標変換 ----
X0, AGE_MIN, AGE_MAX = 70, 60, 92
PXY = (720-X0)/(AGE_MAX-AGE_MIN)        # 1歳あたりpx
Y0 = 120                                # バー基準線
YPM = 19/1_000_000                      # 1円あたりpx (≒19px/100万円)
def ax(age): return round(X0+(age-AGE_MIN)*PXY,1)
def hh(yen): return round(yen*YPM,1)

C_KOSEI="#4a7fb5"; C_KISO="#5fa86b"; C_WAIT="#c9ccd1"; C_GRID="#e6e8eb"; C_AX="#8a9099"

def axis():
    s=[f'<line x1="{X0}" y1="{Y0}" x2="725" y2="{Y0}" stroke="{C_AX}" stroke-width="1.5"/>']
    for a in range(60,91,5):
        x=ax(a)
        s.append(f'<line x1="{x}" y1="28" x2="{x}" y2="{Y0}" stroke="{C_GRID}" stroke-width="1"/>')
        s.append(f'<text x="{x}" y="{Y0+15}" font-size="11" fill="{C_AX}" text-anchor="middle">{a}歳</text>')
    return "".join(s)

def timeline(kosei_start,kosei_amt,kiso_start,kiso_amt,sub=""):
    parts=[f'<svg viewBox="0 0 760 150" xmlns="http://www.w3.org/2000/svg" role="img" width="100%" style="max-width:760px;font-family:sans-serif">']
    parts.append(f'<rect x="0" y="0" width="760" height="150" fill="#ffffff"/>')
    parts.append(axis())
    start_min=min(kosei_start,kiso_start)
    # 待機期間
    if start_min>60:
        parts.append(f'<line x1="{ax(60)}" y1="{Y0}" x2="{ax(start_min)}" y2="{Y0}" stroke="{C_WAIT}" stroke-width="7" stroke-dasharray="3 3"/>')
        parts.append(f'<text x="{(ax(60)+ax(start_min))/2}" y="{Y0-8}" font-size="10" fill="#999" text-anchor="middle">待機</text>')
    # 厚生(下段)
    hk=hh(kosei_amt)
    parts.append(f'<rect x="{ax(kosei_start)}" y="{Y0-hk}" width="{725-ax(kosei_start)}" height="{hk}" fill="{C_KOSEI}" opacity="0.9"/>')
    # 基礎(上段, 厚生の上に積む)。基礎の開始が厚生より遅い場合は途中から
    hb=hh(kiso_amt)
    parts.append(f'<rect x="{ax(kiso_start)}" y="{Y0-hk-hb}" width="{725-ax(kiso_start)}" height="{hb}" fill="{C_KISO}" opacity="0.9"/>')
    # 開始マーカー
    for stg,amtv,lbl in [(kosei_start,kosei_amt,"厚生"),(kiso_start,kiso_amt,"基礎")]:
        parts.append(f'<line x1="{ax(stg)}" y1="32" x2="{ax(stg)}" y2="{Y0}" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>')
    # 合計額(同時開始なら1つ, 別開始なら最終合算を右に表示)
    total=kosei_amt+kiso_amt
    parts.append(f'<text x="730" y="{Y0-hk-hb-6}" font-size="12" font-weight="bold" fill="#333" text-anchor="end">年 {total:,}円</text>')
    if kosei_start!=kiso_start:
        parts.append(f'<text x="730" y="{Y0-hk-hb-22}" font-size="10" fill="#888" text-anchor="end">(全部開始後)</text>')
    if sub:
        parts.append(f'<text x="{X0}" y="20" font-size="12.5" font-weight="bold" fill="#333">{sub}</text>')
    parts.append('</svg>')
    return "\n".join(parts)

def legend():
    return ('<svg viewBox="0 0 760 30" width="100%" style="max-width:760px;font-family:sans-serif">'
            f'<rect x="70" y="8" width="16" height="14" fill="{C_KOSEI}" opacity="0.9"/>'
            '<text x="92" y="19" font-size="12" fill="#333">厚生年金(報酬比例)</text>'
            f'<rect x="250" y="8" width="16" height="14" fill="{C_KISO}" opacity="0.9"/>'
            '<text x="272" y="19" font-size="12" fill="#333">基礎年金</text>'
            f'<rect x="360" y="11" width="22" height="7" fill="{C_WAIT}"/>'
            '<text x="388" y="19" font-size="12" fill="#333">受給待機(もらわない期間)</text>'
            '</svg>')

# ---- 累計バーチャート(90歳まで) ----
def cumulative(rows):
    # rows: (label, total90, color)
    mx=max(r[1] for r in rows)
    W=760; barH=26; gap=14; top=40
    h=top+len(rows)*(barH+gap)+20
    s=[f'<svg viewBox="0 0 {W} {h}" width="100%" style="max-width:760px;font-family:sans-serif">']
    s.append(f'<text x="20" y="24" font-size="14" font-weight="bold" fill="#333">90歳までの年金 累計受給額</text>')
    x0=180; xmax=700
    for i,(lab,val,col) in enumerate(rows):
        y=top+i*(barH+gap)
        w=round((val/mx)*(xmax-x0))
        s.append(f'<text x="{x0-8}" y="{y+barH-8}" font-size="11.5" fill="#333" text-anchor="end">{lab}</text>')
        s.append(f'<rect x="{x0}" y="{y}" width="{w}" height="{barH}" fill="{col}" opacity="0.85" rx="3"/>')
        s.append(f'<text x="{x0+w+6}" y="{y+barH-8}" font-size="11.5" font-weight="bold" fill="#333">{val/10000:.0f}万円</text>')
    s.append('</svg>')
    return "\n".join(s)

# ---- 損益分岐点: 累計関数 & 折れ線チャート ----
def cum_at(p, age):
    ks,ka,bs,ba = p
    return ka*max(0,age-ks) + ba*max(0,age-bs)

def breakeven(p_base, p_other):
    """p_other が p_base を追い抜く年齢(0.1刻み)。なければ None"""
    prev=None
    a=60.0
    while a<=99.0:
        d=cum_at(p_other,a)-cum_at(p_base,a)
        if prev is not None and prev<0 and d>=0:
            return round(a,1)
        prev=d; a+=0.1
    return None

def linechart(series, marks):
    W,Hh=760,440
    xL,xR,yB,yT=70,730,390,45
    aMin,aMax=60,95; vMax=90_000_000
    def px(a): return round(xL+(a-aMin)/(aMax-aMin)*(xR-xL),1)
    def py(v): return round(yB-(v/vMax)*(yB-yT),1)
    s=[f'<svg viewBox="0 0 {W} {Hh}" width="100%" style="max-width:760px;font-family:sans-serif">']
    s.append(f'<rect x="0" y="0" width="{W}" height="{Hh}" fill="#ffffff"/>')
    s.append(f'<text x="20" y="26" font-size="15" font-weight="bold" fill="#333">年齢による損益分岐点（累計受給額の推移）</text>')
    # Y軸グリッド(1000万円刻み)
    for v in range(0,91,10):
        y=py(v*1_000_000)
        s.append(f'<line x1="{xL}" y1="{y}" x2="{xR}" y2="{y}" stroke="{C_GRID}" stroke-width="1"/>')
        s.append(f'<text x="{xL-6}" y="{y+4}" font-size="10" fill="{C_AX}" text-anchor="end">{v*100}万</text>')
    # X軸
    for a in range(60,96,5):
        x=px(a)
        s.append(f'<line x1="{x}" y1="{yT}" x2="{x}" y2="{yB}" stroke="{C_GRID}" stroke-width="1"/>')
        s.append(f'<text x="{x}" y="{yB+16}" font-size="11" fill="{C_AX}" text-anchor="middle">{a}歳</text>')
    s.append(f'<line x1="{xL}" y1="{yB}" x2="{xR}" y2="{yB}" stroke="{C_AX}" stroke-width="1.5"/>')
    # 損益分岐の縦線
    for age,lbl in marks:
        x=px(age)
        s.append(f'<line x1="{x}" y1="{yT}" x2="{x}" y2="{yB}" stroke="#d6663b" stroke-width="1" stroke-dasharray="4 3" opacity="0.7"/>')
        s.append(f'<text x="{x}" y="{yT-4}" font-size="10.5" font-weight="bold" fill="#d6663b" text-anchor="middle">{lbl}</text>')
    # 折れ線
    for lab,p,col in series:
        pts=" ".join(f"{px(a)},{py(cum_at(p,a))}" for a in range(60,96))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.4"/>')
        ya=py(cum_at(p,95))
        s.append(f'<text x="{px(95)+4}" y="{ya+3}" font-size="10.5" font-weight="bold" fill="{col}">{lab}</text>')
    s.append('</svg>')
    return "\n".join(s)

# ---- 繰上げ60＋運用 シナリオの資産推移チャート ----
def invest_series(P60, D, r=0.05):
    """ages 60..95 の 運用残高 / 取崩累計 / 経済価値 を返す"""
    bal={60:0.0}; cumW={60:0.0}
    b=0.0; cw=0.0
    for age in range(60,95):
        if age<65:                 # 60->65: 全額運用・取崩なし
            b=b*(1+r)+P60
        else:                      # 65以降: 年金を運用継続＋少し取崩
            b=b*(1+r)+P60-D; cw+=D
        bal[age+1]=b; cumW[age+1]=cw
    econ={a:bal[a]+cumW[a] for a in range(60,96)}
    return bal,cumW,econ

def assetchart(P60, cash65, cash75, D):
    bal,cumW,econ=invest_series(P60,D)
    W,Hh=760,460
    xL,xR,yB,yT=78,705,400,55
    aMin,aMax=60,95; vMax=150_000_000
    def px(a): return round(xL+(a-aMin)/(aMax-aMin)*(xR-xL),1)
    def py(v): return round(yB-(min(v,vMax)/vMax)*(yB-yT),1)
    s=[f'<svg viewBox="0 0 {W} {Hh}" width="100%" style="max-width:760px;font-family:sans-serif">']
    s.append(f'<rect x="0" y="0" width="{W}" height="{Hh}" fill="#ffffff"/>')
    s.append(f'<text x="20" y="26" font-size="15" font-weight="bold" fill="#333">繰上げ60＋年利5%運用：資産の推移</text>')
    # 5年間 全額運用フェーズ 帯
    s.append(f'<rect x="{px(60)}" y="{yT}" width="{px(65)-px(60)}" height="{yB-yT}" fill="#eef4fb"/>')
    s.append(f'<text x="{(px(60)+px(65))/2}" y="{yT+14}" font-size="9.5" fill="#5a7fb0" text-anchor="middle">5年間 全額運用</text>')
    s.append(f'<text x="{(px(60)+px(65))/2}" y="{yT+26}" font-size="9.5" fill="#5a7fb0" text-anchor="middle">(取崩なし)</text>')
    # Y軸グリッド(2000万刻み)
    for v in range(0,150000001,20000000):
        y=py(v)
        s.append(f'<line x1="{xL}" y1="{y}" x2="{xR}" y2="{y}" stroke="{C_GRID}" stroke-width="1"/>')
        s.append(f'<text x="{xL-6}" y="{y+4}" font-size="10" fill="{C_AX}" text-anchor="end">{v//10000:,}万</text>')
    for a in range(60,96,5):
        x=px(a)
        s.append(f'<text x="{x}" y="{yB+16}" font-size="11" fill="{C_AX}" text-anchor="middle">{a}歳</text>')
    s.append(f'<line x1="{xL}" y1="{yB}" x2="{xR}" y2="{yB}" stroke="{C_AX}" stroke-width="1.5"/>')
    # 運用残高(面)
    pts=[f"{px(60)},{py(0)}"]+[f"{px(a)},{py(bal[a])}" for a in range(60,96)]+[f"{px(95)},{py(0)}"]
    s.append(f'<polygon points="{" ".join(pts)}" fill="{C_KOSEI}" opacity="0.25"/>')
    s.append(f'<polyline points="{" ".join(f"{px(a)},{py(bal[a])}" for a in range(60,96))}" fill="none" stroke="{C_KOSEI}" stroke-width="2.4"/>')
    # 経済価値(残高+取崩累計)
    s.append(f'<polyline points="{" ".join(f"{px(a)},{py(econ[a])}" for a in range(60,96))}" fill="none" stroke="#d6663b" stroke-width="2.6"/>')
    # 比較:②65現金 ③繰下75現金(無運用)
    s.append(f'<polyline points="{" ".join(f"{px(a)},{py(cash65*max(0,a-65))}" for a in range(60,96))}" fill="none" stroke="#6b8e23" stroke-width="2" stroke-dasharray="5 3"/>')
    s.append(f'<polyline points="{" ".join(f"{px(a)},{py(cash75*max(0,a-75))}" for a in range(60,96))}" fill="none" stroke="#8a5a2b" stroke-width="2" stroke-dasharray="5 3"/>')
    # ラベル
    s.append(f'<text x="{px(95)+2}" y="{py(econ[95])+3}" font-size="10" font-weight="bold" fill="#d6663b">経済価値</text>')
    s.append(f'<text x="{px(95)+2}" y="{py(bal[95])+12}" font-size="10" font-weight="bold" fill="{C_KOSEI}">運用残高</text>')
    s.append(f'<text x="{px(95)+2}" y="{py(cash75*20)+3}" font-size="9.5" fill="#8a5a2b">③繰下75(現金)</text>')
    s.append(f'<text x="{px(95)+2}" y="{py(cash65*30)+3}" font-size="9.5" fill="#6b8e23">②65歳(現金)</text>')
    s.append('</svg>')
    return "\n".join(s),bal,cumW,econ

# ---- 汎用 複数線チャート(資産/累計) ----
def acc(P, start, age, r):
    """年金Pをstart歳から年利rで運用(取崩なし・末入金)。age時点の残高"""
    n=age-start
    return P*(((1+r)**n-1)/r) if n>0 else 0.0

def multiline(title, series, vMax, ytick=20_000_000, subtitle=None):
    """series: [(label,color,dash(bool),func(age)->value)]"""
    W,Hh=760,440
    xL,xR,yB,yT=82,665,392,(70 if subtitle else 52)
    aMin,aMax=60,95
    def px(a): return round(xL+(a-aMin)/(aMax-aMin)*(xR-xL),1)
    def py(v): return round(yB-(min(v,vMax)/vMax)*(yB-yT),1)
    s=[f'<svg viewBox="0 0 {W} {Hh}" width="100%" style="max-width:760px;font-family:sans-serif">']
    s.append(f'<rect x="0" y="0" width="{W}" height="{Hh}" fill="#ffffff"/>')
    s.append(f'<text x="20" y="26" font-size="15" font-weight="bold" fill="#333">{title}</text>')
    if subtitle:
        s.append(f'<text x="20" y="44" font-size="11.5" fill="#777">{subtitle}</text>')
    for v in range(0,vMax+1,ytick):
        y=py(v)
        s.append(f'<line x1="{xL}" y1="{y}" x2="{xR}" y2="{y}" stroke="{C_GRID}" stroke-width="1"/>')
        s.append(f'<text x="{xL-6}" y="{y+4}" font-size="10" fill="{C_AX}" text-anchor="end">{v//10000:,}万</text>')
    for a in range(60,96,5):
        x=px(a)
        s.append(f'<text x="{x}" y="{yB+16}" font-size="11" fill="{C_AX}" text-anchor="middle">{a}歳</text>')
    s.append(f'<line x1="{xL}" y1="{yB}" x2="{xR}" y2="{yB}" stroke="{C_AX}" stroke-width="1.5"/>')
    ylab=[]
    for lab,col,dash,fn in series:
        da=' stroke-dasharray="5 3"' if dash else ''
        pts=" ".join(f"{px(a)},{py(fn(a))}" for a in range(60,96))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.4"{da}/>')
        ylab.append((py(fn(95)),lab,col))
    # 終端ラベル(重なり回避で軽くずらす)
    ylab.sort()
    last=-100
    for y,lab,col in ylab:
        yy=max(y, last+12); last=yy
        s.append(f'<text x="{xR+4}" y="{yy+3}" font-size="10" font-weight="bold" fill="{col}">{lab}</text>')
    s.append('</svg>')
    return "\n".join(s)

# ===== 各パターン定義 =====
A=(60,amt(H,60),60,amt(K,60))
B=(65,H,65,K)
C70=(70,amt(H,70),70,amt(K,70))
C72=(72,amt(H,72),72,amt(K,72))
C75=(75,amt(H,75),75,amt(K,75))
D=(65,H,75,amt(K,75))               # 併用: 厚生65・基礎75
E=(65,H,70,amt(K,70))               # Claudeオススメ: 厚生65・基礎70

def total90(kosei_start,kosei_amt,kiso_start,kiso_amt):
    return kosei_amt*(90-kosei_start)+kiso_amt*(90-kiso_start)

rowsC=[
 ("①繰上げ60歳", total90(*A), C_KOSEI),
 ("②なし65歳",   total90(*B), "#6b8e23"),
 ("③繰下げ70歳", total90(*C70), "#b5894a"),
 ("③繰下げ72歳", total90(*C72), "#b5894a"),
 ("③繰下げ75歳", total90(*C75), "#b5894a"),
 ("④併用(厚65/基75)", total90(*D), "#7a5fa8"),
 ("⑤推奨(厚65/基70)", total90(*E), "#d6663b"),
]

# ===== Markdown 組み立て =====
md=[]
md.append("---")
md.append("title: 年金 繰上げ・繰下げ 図解ガイド（SVG）")
md.append("---")
md.append("")
md.append("# 年金 繰上げ・繰下げ 図解ガイド（SVG）")
md.append("")
md.append("**目的：年齢による「損益分岐点」を可視化すること。** 老齢年金の受給開始は **60〜75歳の間で選べ**、"
          "**厚生年金（報酬比例）** と **基礎年金** は**別々の時期に**繰上げ・繰下げできます（併用可）。"
          "本ガイドでは代表パターンをSVGで図解し、**何歳まで生きると、どの選択が得か**を示します。")
md.append("")
md.append("> 🎯 結論を急ぐ人へ → 下の「[年齢による損益分岐点](#-年齢による損益分岐点このガイドの目的)」の折れ線グラフと早見表を見てください。")
md.append("")
md.append("> モデル前提：**厚生年金（報酬比例 本来額）＝ 1,578,528円/年**（平均標準報酬月額60万・40年加入）、"
          "**基礎年金 満額＝ 831,700円/年**（令和7年度）。繰上げ ▲0.4%/月、繰下げ ＋0.7%/月。")
md.append("")
md.append("## 増減率の早見")
md.append("")
md.append("| 受給開始 | 増減率 | 厚生年金/年 | 基礎年金/年 | 合計/年 |")
md.append("| --- | --- | --- | --- | --- |")
for a in [60,65,70,72,75]:
    sign = f"{(R[a]-1)*100:+.1f}%"
    md.append(f"| {a}歳 | ×{R[a]:.2f}（{sign}） | {amt(H,a):,}円 | {amt(K,a):,}円 | {amt(H,a)+amt(K,a):,}円 |")
md.append("")
md.append("**凡例**")
md.append("")
md.append(legend())
md.append("")
md.append("---")
md.append("")

def section(no,title,desc,svg,notes):
    md.append(f"## {no}")
    md.append("")
    md.append(desc)
    md.append("")
    md.append(svg)
    md.append("")
    for n in notes:
        md.append(f"- {n}")
    md.append("")
    md.append("---")
    md.append("")

section("① 繰上げ（60歳から早めにもらう）",
 "繰上げ",
 "65歳より早く受け取る代わりに、**一生 ▲24% の減額**。早く・長くもらえるが総額は伸びにくい。",
 timeline(*A, sub="① 繰上げ 60歳開始（厚生・基礎とも ×0.76）"),
 ["メリット：60歳から受給開始、健康不安・資金需要に対応",
  "デメリット：減額が**一生続く**。長生きするほど不利",
  f"年額 **{A[1]+A[3]:,}円**（厚生{A[1]:,}＋基礎{A[3]:,}）"])

section("② 繰上げ・繰下げ なし（65歳・本来）",
 "なし",
 "標準の受給開始。増減なしの基準パターン。",
 timeline(*B, sub="② 65歳開始（本来額・増減なし）"),
 [f"年額 **{B[1]+B[3]:,}円**（厚生{B[1]:,}＋基礎{B[3]:,}）",
  "判断に迷うときの基準。加給年金も65歳から通常どおり"])

svgC="\n\n".join([
  timeline(*C70, sub="③-a 繰下げ 70歳開始（×1.42 / +42%）"),
  timeline(*C72, sub="③-b 繰下げ 72歳開始（×1.588 / +58.8%）"),
  timeline(*C75, sub="③-c 繰下げ 75歳開始（×1.84 / +84%・上限）"),
])
section("③ 繰下げ 3パターン（70歳・72歳・75歳）",
 "繰下げ",
 "受給を遅らせるほど**一生 増額**。75歳が上限（+84%）。長生きリスクへの備え（＝長生き保険）。",
 svgC,
 [f"70歳：年額 **{C70[1]+C70[3]:,}円** / 72歳：**{C72[1]+C72[3]:,}円** / 75歳：**{C75[1]+C75[3]:,}円**",
  "デメリット：待機中は年金ゼロ。**繰下げ待機中は加給年金がもらえない**",
  "**注意：繰下げで増えても“遺族年金”は増えない**（遺族厚生は本来額×3/4で計算）"])

section("④ 併用（厚生と基礎で時期をずらす）",
 "併用",
 "厚生年金と基礎年金は**別々に**受給開始できる。例：**厚生は65歳から（生活費＆加給年金を確保）、基礎は75歳まで繰下げ**。",
 timeline(*D, sub="④ 併用：厚生65歳 ＋ 基礎75歳繰下げ"),
 ["65〜74歳：厚生のみ 1,578,528円/年",
  f"75歳以降：合計 **{D[1]+D[3]:,}円/年**（基礎が＋84%）",
  "基礎年金は**遺族厚生年金と全額併給**できるため、繰下げ増額が生涯まるごと残る（残された配偶者対策に有効）"])

section("⑤ Claude Code オススメ（いいとこ取り）",
 "推奨",
 "**厚生は65歳から・基礎は70歳まで繰下げ**。これまでの議論（遺族年金・加給年金）を踏まえたバランス重視の推奨案。",
 timeline(*E, sub="⑤ 推奨：厚生65歳 ＋ 基礎70歳繰下げ"),
 ["**厚生を65歳から**：繰り下げても遺族年金は増えない＆**加給年金を確保**できるため、65歳受給が合理的",
  "**基礎を70歳まで繰下げ（+42%）**：基礎は遺族厚生と**全額併給**で、本人にも残された配偶者にも生涯効く",
  f"65〜69歳：厚生のみ 1,578,528円/年 → 70歳以降：合計 **{E[1]+E[3]:,}円/年**",
  "財力に余裕がない場合は、無理せず②（65歳から両方）でOK。遺族年金は変わりません"])

# ===== 損益分岐点 セクション(主役) =====
be_AB = breakeven(A,B)      # 65本来 が 繰上げ60 を抜く年齢
be_70 = breakeven(B,C70)    # 繰下70 が 65 を抜く
be_72 = breakeven(B,C72)
be_75 = breakeven(B,C75)
be_E  = breakeven(B,E)      # 推奨 が 65 を抜く
marks=[(be_AB,f"{be_AB:.0f}歳"),(be_70,f"{be_70:.0f}歳"),(be_75,f"{be_75:.0f}歳")]
series=[
 ("①繰上60", A, C_KOSEI),
 ("②65本来", B, "#6b8e23"),
 ("③繰下70", C70, "#b5894a"),
 ("③繰下75", C75, "#8a5a2b"),
 ("⑤推奨",   E, "#d6663b"),
]
md.append("## 🎯 年齢による損益分岐点（このガイドの目的）")
md.append("")
md.append("各パターンを「累計でいくら受け取ったか」で比較すると、線が交わる年齢が**損益分岐点**です。"
          "**その年齢より長生きすれば繰下げが得、短ければ繰上げ／65歳が得**になります。")
md.append("")
md.append(linechart(series, marks))
md.append("")
md.append("### 損益分岐年齢（65歳受給を基準にした早見表）")
md.append("")
md.append("| 比較 | 損益分岐年齢 | 読み方 |")
md.append("| --- | --- | --- |")
md.append(f"| ① 繰上げ60歳 vs ② 65歳 | **約{be_AB:.0f}歳** | これより長生きするなら繰上げは損（65歳が逆転） |")
md.append(f"| ③ 繰下げ70歳 vs ② 65歳 | **約{be_70:.0f}歳** | これより長生きするなら繰下げ70歳が得 |")
md.append(f"| ③ 繰下げ72歳 vs ② 65歳 | **約{be_72:.0f}歳** | これより長生きするなら繰下げ72歳が得 |")
md.append(f"| ③ 繰下げ75歳 vs ② 65歳 | **約{be_75:.0f}歳** | これより長生きするなら繰下げ75歳が得 |")
md.append(f"| ⑤ 推奨(厚65/基70) vs ② 65歳 | **約{be_E:.0f}歳** | これより長生きするなら推奨案が得 |")
md.append("")
md.append("> ざっくり：**繰下げは「受給開始からおよそ11〜12年」で元が取れる**（70歳開始なら約82歳、75歳開始なら約87歳）。"
          "日本人の平均余命（65歳男性≒85歳・女性≒90歳）を踏まえると、健康なら繰下げが分岐点を超えやすい計算です。")
md.append("")
md.append("---")
md.append("")
md.append("## 累計受給額の比較（90歳まで）")
md.append("")
md.append("長生きするほど繰下げが有利。下図は各パターンを90歳まで受給した場合の累計です。")
md.append("")
md.append(cumulative(rowsC))
md.append("")
md.append("| パターン | 80歳まで | 85歳まで | 90歳まで |")
md.append("| --- | --- | --- | --- |")
def cum(p,age): return p[1]*(age-p[0])+p[3]*(age-p[2])
labels=[("① 繰上げ60歳",A),("② なし65歳",B),("③ 繰下げ70歳",C70),("③ 繰下げ72歳",C72),
        ("③ 繰下げ75歳",C75),("④ 併用(厚65/基75)",D),("⑤ 推奨(厚65/基70)",E)]
for lab,p in labels:
    md.append(f"| {lab} | {cum(p,80)/10000:.0f}万円 | {cum(p,85)/10000:.0f}万円 | {cum(p,90)/10000:.0f}万円 |")
md.append("")
md.append("> 80歳前後が損益分岐の目安。**早く亡くなりそうなら繰上げ／②、長生き前提なら繰下げ**が有利です。")
md.append("")
md.append("---")
md.append("")
# ===== ⑥ 繰上げ60＋運用 セクション =====
P60=A[1]+A[3]            # 繰上げ60の年金合計
cash65=B[1]+B[3]        # 65歳本来の年金合計
cash75=C75[1]+C75[3]    # 繰下げ75の年金合計
Dwd=1_200_000           # 65歳以降の取り崩し(月10万)
ac_svg,bal,cumW,econ=assetchart(P60,cash65,cash75,Dwd)
md.append("## 💹 ⑥ 繰上げ60歳＋年利5%運用（早くもらって投資する作戦）")
md.append("")
md.append("「**早くもらって運用すれば繰下げに勝てるか？**」を検証します。"
          f"繰上げ60歳の年金（**{P60:,}円/年**）を年利5%で運用するモデルです。")
md.append("")
md.append("**前提（モデル）**")
md.append("")
md.append(f"- **60〜64歳**：年金を全額、年利5%で運用（取り崩しゼロ）→ 65歳時点で元手 **約{bal[65]/10000:.0f}万円**")
md.append(f"- **65歳以降**：年金を運用に回し続けつつ、生活の足しに**毎年{Dwd:,}円（月10万円）取り崩し**、残りは5%運用を継続")
md.append("- 比較対象（点線）：②65歳・③繰下げ75歳を**運用せず現金で受け取った**場合の累計")
md.append("")
md.append(ac_svg)
md.append("")
md.append("### 年齢別の資産（繰上げ60＋運用）")
md.append("")
md.append("| 年齢 | 運用残高 | 取崩累計 | 経済価値(残高+取崩) | 参考:②65現金累計 | 参考:③繰下75現金累計 |")
md.append("| --- | --- | --- | --- | --- | --- |")
for age in [65,70,75,80,85,90,95]:
    md.append(f"| {age}歳 | {bal[age]/10000:,.0f}万円 | {cumW[age]/10000:,.0f}万円 | "
              f"**{econ[age]/10000:,.0f}万円** | {cash65*max(0,age-65)/10000:,.0f}万円 | {cash75*max(0,age-75)/10000:,.0f}万円 |")
md.append("")
md.append("> 👀 **ポイント**：5%で運用できるなら、**繰上げ60＋運用の経済価値は早い段階から現金受給を上回り続けます**。"
          "繰上げの「一生▲24%減額」という弱点を、5年間の運用益と複利が補って余りある計算です。")
md.append("")
md.append("> ⚠️ **公平のための注意**：これは「60歳パターンだけ運用」という指定どおりの試算です。"
          "**②65歳や③繰下げも同様に5%運用すれば結果は変わります**（例：②65歳の年金も5%運用すると90歳で約1.1億円）。"
          "また**年利5%は元本保証ではなく価格変動・元本割れリスク**があり、繰下げ（+0.7%/月＝公的保証の増額）とは性質が異なります。"
          "「確実性の繰下げ」か「期待値の運用」かは、リスク許容度次第です。")
md.append("")
md.append("---")
md.append("")
# ===== ⑦ 公平比較：全パターンを同率5%運用 =====
C70tot=C70[1]+C70[3]
ser7=[
 ("①繰上60", C_KOSEI, False, lambda a: acc(P60,60,a,0.05)),
 ("②65歳",   "#6b8e23", False, lambda a: acc(cash65,65,a,0.05)),
 ("③繰下70", "#b5894a", False, lambda a: acc(C70tot,70,a,0.05)),
 ("③繰下75", "#8a5a2b", False, lambda a: acc(cash75,75,a,0.05)),
 ("⑤推奨",   "#d6663b", False, lambda a: acc(1578528,65,a,0.05)+acc(1181014,70,a,0.05)),
]
md.append("## ⚖️ ⑦ 公平比較：全パターンを同じ年利5%で運用したら？")
md.append("")
md.append("⑥は「60歳だけ運用」でしたが、ここでは**どのパターンも受け取った年金を全額・年利5%で運用**（取り崩しなし）した"
          "**純資産**で比較します。早くもらうほど運用期間が長く、複利が効きます。")
md.append("")
md.append(multiline("全パターンを年利5%で運用した純資産", ser7, 180_000_000,
                    subtitle="各パターンの年金を全額・年利5%で積立運用(取り崩しなし)した場合の残高"))
md.append("")
md.append("| 年齢 | ①繰上60 | ②65歳 | ③繰下70 | ③繰下75 | ⑤推奨 |")
md.append("| --- | --- | --- | --- | --- | --- |")
for age in [80,85,90,95]:
    row=[acc(P60,60,age,0.05),acc(cash65,65,age,0.05),acc(C70tot,70,age,0.05),
         acc(cash75,75,age,0.05),acc(1578528,65,age,0.05)+acc(1181014,70,age,0.05)]
    md.append(f"| {age}歳 | "+" | ".join(f"{v/10000:,.0f}万" for v in row)+" |")
md.append("")
md.append("> 👀 **結論：全員が同率で運用すると、むしろ①繰上げ60歳が長く優位**（90歳時点でも最大級）。"
          "**運用前提では「早くもらう」ほど有利**になりやすく、繰下げの“増額”メリットは運用益に追いつかれます。"
          "ただし繰下げの本質的価値は**「死ぬまで増えた年金が保証される」長生き・インフレ保険**であり、"
          "運用は**元本割れリスク**を負う点が決定的に違います。")
md.append("")
md.append("---")
md.append("")
# ===== ⑧ 感応度：年利3/4/5%でどこまで戦えるか =====
# 繰上げ60を3/4/5%運用(純資産) vs 繰下げ75・65の現金(無運用)
ser8=[
 ("繰上60@5%", "#c0392b", False, lambda a: acc(P60,60,a,0.05)),
 ("繰上60@4%", "#e67e22", False, lambda a: acc(P60,60,a,0.04)),
 ("繰上60@3%", "#f0b27a", False, lambda a: acc(P60,60,a,0.03)),
 ("③繰下75(現金)", "#8a5a2b", True, lambda a: cash75*max(0,a-75)),
 ("②65歳(現金)",   "#6b8e23", True, lambda a: cash65*max(0,a-65)),
]
# 繰上60純資産(90歳)=繰下75現金(90歳)となる利回りを数値探索
target=cash75*15
lo,hi=0.0,0.10
for _ in range(60):
    mid=(lo+hi)/2
    if acc(P60,60,90,mid)<target: lo=mid
    else: hi=mid
thr=(lo+hi)/2
md.append("## 📈 ⑧ 感応度分析：年利が何%なら運用が勝てる？")
md.append("")
md.append("「繰上げ60歳を運用」した**純資産**を、年利**3%/4%/5%**で比べ、繰下げ・本来受給を"
          "**運用せず現金で受け取った**場合（点線）と対比します。")
md.append("")
md.append(multiline("繰上げ60の運用(3/4/5%) vs 繰下げ・本来の現金受給", ser8, 180_000_000,
                    subtitle="実線=繰上げ60を各利回りで運用した純資産 / 点線=無運用の累計受給(現金)"))
md.append("")
md.append("| 年齢 | 繰上60@3% | 繰上60@4% | 繰上60@5% | ③繰下75(現金) | ②65歳(現金) |")
md.append("| --- | --- | --- | --- | --- | --- |")
for age in [80,85,90,95]:
    row=[acc(P60,60,age,0.03),acc(P60,60,age,0.04),acc(P60,60,age,0.05),
         cash75*max(0,age-75),cash65*max(0,age-65)]
    md.append(f"| {age}歳 | "+" | ".join(f"{v/10000:,.0f}万" for v in row)+" |")
md.append("")
md.append(f"> 👀 **しきい値**：繰上げ60を運用した純資産が、90歳時点で③繰下げ75歳の現金累計に並ぶ利回りは**わずか約{thr*100:.1f}%**。"
          "つまり**年1〜2%でも運用できれば、現金で受け取る繰下げの“受給総額”は上回ります**（複利と早期受給の効果）。")
md.append("")
md.append("> ⚠️ ただし上記は**現金（無運用）の繰下げ**との比較です。繰下げの真価は受給額そのものではなく、"
          "**生涯保証・長生き保険・遺族年金の土台**にあります。「期待リターンの運用」か「確実性の繰下げ」かは、"
          "**運用リスクを取れるか／長生きにどう備えるか**で選ぶのが本筋です。")
md.append("")
md.append("---")
md.append("")
md.append("## まとめ")
md.append("")
md.append("1. **厚生年金と基礎年金は別々に**繰上げ・繰下げできる（④⑤の併用が可能）。")
md.append("2. **繰下げ＝一生増額**だが、待機中は無年金＆**加給年金が止まる**、そして**遺族年金は増えない**。")
md.append("3. **基礎年金の繰下げは遺族厚生と全額併給**でき、残された配偶者にも効く（⑤推奨の核心）。")
md.append("4. 財力に余裕がなければ②（65歳）で十分。遺族年金額は繰下げの有無で変わりません。")
md.append("5. **運用前提（⑥⑦⑧）では「早くもらって投資」が受給総額で有利**になりやすい。"
          "ただし繰下げは**元本割れのない生涯保証・長生き保険**——“期待値の運用”か“確実性の繰下げ”かはリスク許容度で選ぶ。")
md.append("")
md.append("> 本ガイドはモデル前提を置いた概算です。実額は加入記録・年齢差・加給年金・在職老齢年金等で変わります。正確な試算は年金事務所・ねんきんネットでご確認ください。")
md.append("")
md.append("関連：[遺族年金・遺族厚生年金 完全ガイド](survivors-pension-guide.md)")
md.append("")

open("/home/user/test-repository/docs/pension-deferral-svg-guide.md","w",encoding="utf-8").write("\n".join(md))
print("written:", len("\n".join(md)), "bytes")
print("cum90 E=",cum(E,90), "B=",cum(B,90))
