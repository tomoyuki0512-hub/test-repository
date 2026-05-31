---
title: 年金 繰上げ・繰下げ 図解ガイド（SVG）
---

# 年金 繰上げ・繰下げ 図解ガイド（SVG）

**目的：年齢による「損益分岐点」を可視化すること。** 老齢年金の受給開始は **60〜75歳の間で選べ**、**厚生年金（報酬比例）** と **基礎年金** は**別々の時期に**繰上げ・繰下げできます（併用可）。本ガイドでは代表パターンをSVGで図解し、**何歳まで生きると、どの選択が得か**を示します。

> 🎯 結論を急ぐ人へ → 下の「[年齢による損益分岐点](#-年齢による損益分岐点このガイドの目的)」の折れ線グラフと早見表を見てください。

> モデル前提：**厚生年金（報酬比例 本来額）＝ 1,578,528円/年**（平均標準報酬月額60万・40年加入）、**基礎年金 満額＝ 831,700円/年**（令和7年度）。繰上げ ▲0.4%/月、繰下げ ＋0.7%/月。

## 増減率の早見

| 受給開始 | 増減率 | 厚生年金/年 | 基礎年金/年 | 合計/年 |
| --- | --- | --- | --- | --- |
| 60歳 | ×0.76（-24.0%） | 1,199,681円 | 632,092円 | 1,831,773円 |
| 65歳 | ×1.00（+0.0%） | 1,578,528円 | 831,700円 | 2,410,228円 |
| 70歳 | ×1.42（+42.0%） | 2,241,510円 | 1,181,014円 | 3,422,524円 |
| 72歳 | ×1.59（+58.8%） | 2,506,702円 | 1,320,740円 | 3,827,442円 |
| 75歳 | ×1.84（+84.0%） | 2,904,492円 | 1,530,328円 | 4,434,820円 |

**凡例**

<svg viewBox="0 0 760 30" width="100%" style="max-width:760px;font-family:sans-serif"><rect x="70" y="8" width="16" height="14" fill="#4a7fb5" opacity="0.9"/><text x="92" y="19" font-size="12" fill="#333">厚生年金(報酬比例)</text><rect x="250" y="8" width="16" height="14" fill="#5fa86b" opacity="0.9"/><text x="272" y="19" font-size="12" fill="#333">基礎年金</text><rect x="360" y="11" width="22" height="7" fill="#c9ccd1"/><text x="388" y="19" font-size="12" fill="#333">受給待機(もらわない期間)</text></svg>

---

## ① 繰上げ（60歳から早めにもらう）

65歳より早く受け取る代わりに、**一生 ▲24% の減額**。早く・長くもらえるが総額は伸びにくい。

<svg viewBox="0 0 760 150" xmlns="http://www.w3.org/2000/svg" role="img" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="150" fill="#ffffff"/>
<line x1="70" y1="120" x2="725" y2="120" stroke="#8a9099" stroke-width="1.5"/><line x1="70.0" y1="28" x2="70.0" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="70.0" y="135" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text><line x1="171.6" y1="28" x2="171.6" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="171.6" y="135" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text><line x1="273.1" y1="28" x2="273.1" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="273.1" y="135" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text><line x1="374.7" y1="28" x2="374.7" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="374.7" y="135" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text><line x1="476.2" y1="28" x2="476.2" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="476.2" y="135" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text><line x1="577.8" y1="28" x2="577.8" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="577.8" y="135" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text><line x1="679.4" y1="28" x2="679.4" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="679.4" y="135" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<rect x="70.0" y="97.2" width="655.0" height="22.8" fill="#4a7fb5" opacity="0.9"/>
<rect x="70.0" y="85.2" width="655.0" height="12.0" fill="#5fa86b" opacity="0.9"/>
<line x1="70.0" y1="32" x2="70.0" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<line x1="70.0" y1="32" x2="70.0" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<text x="730" y="79.2" font-size="12" font-weight="bold" fill="#333" text-anchor="end">年 1,831,773円</text>
<text x="70" y="20" font-size="12.5" font-weight="bold" fill="#333">① 繰上げ 60歳開始（厚生・基礎とも ×0.76）</text>
</svg>

- メリット：60歳から受給開始、健康不安・資金需要に対応
- デメリット：減額が**一生続く**。長生きするほど不利
- 年額 **1,831,773円**（厚生1,199,681＋基礎632,092）

---

## ② 繰上げ・繰下げ なし（65歳・本来）

標準の受給開始。増減なしの基準パターン。

<svg viewBox="0 0 760 150" xmlns="http://www.w3.org/2000/svg" role="img" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="150" fill="#ffffff"/>
<line x1="70" y1="120" x2="725" y2="120" stroke="#8a9099" stroke-width="1.5"/><line x1="70.0" y1="28" x2="70.0" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="70.0" y="135" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text><line x1="171.6" y1="28" x2="171.6" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="171.6" y="135" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text><line x1="273.1" y1="28" x2="273.1" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="273.1" y="135" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text><line x1="374.7" y1="28" x2="374.7" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="374.7" y="135" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text><line x1="476.2" y1="28" x2="476.2" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="476.2" y="135" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text><line x1="577.8" y1="28" x2="577.8" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="577.8" y="135" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text><line x1="679.4" y1="28" x2="679.4" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="679.4" y="135" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<line x1="70.0" y1="120" x2="171.6" y2="120" stroke="#c9ccd1" stroke-width="7" stroke-dasharray="3 3"/>
<text x="120.8" y="112" font-size="10" fill="#999" text-anchor="middle">待機</text>
<rect x="171.6" y="90.0" width="553.4" height="30.0" fill="#4a7fb5" opacity="0.9"/>
<rect x="171.6" y="74.2" width="553.4" height="15.8" fill="#5fa86b" opacity="0.9"/>
<line x1="171.6" y1="32" x2="171.6" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<line x1="171.6" y1="32" x2="171.6" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<text x="730" y="68.2" font-size="12" font-weight="bold" fill="#333" text-anchor="end">年 2,410,228円</text>
<text x="70" y="20" font-size="12.5" font-weight="bold" fill="#333">② 65歳開始（本来額・増減なし）</text>
</svg>

- 年額 **2,410,228円**（厚生1,578,528＋基礎831,700）
- 判断に迷うときの基準。加給年金も65歳から通常どおり

---

## ③ 繰下げ 3パターン（70歳・72歳・75歳）

受給を遅らせるほど**一生 増額**。75歳が上限（+84%）。長生きリスクへの備え（＝長生き保険）。

<svg viewBox="0 0 760 150" xmlns="http://www.w3.org/2000/svg" role="img" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="150" fill="#ffffff"/>
<line x1="70" y1="120" x2="725" y2="120" stroke="#8a9099" stroke-width="1.5"/><line x1="70.0" y1="28" x2="70.0" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="70.0" y="135" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text><line x1="171.6" y1="28" x2="171.6" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="171.6" y="135" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text><line x1="273.1" y1="28" x2="273.1" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="273.1" y="135" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text><line x1="374.7" y1="28" x2="374.7" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="374.7" y="135" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text><line x1="476.2" y1="28" x2="476.2" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="476.2" y="135" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text><line x1="577.8" y1="28" x2="577.8" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="577.8" y="135" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text><line x1="679.4" y1="28" x2="679.4" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="679.4" y="135" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<line x1="70.0" y1="120" x2="273.1" y2="120" stroke="#c9ccd1" stroke-width="7" stroke-dasharray="3 3"/>
<text x="171.55" y="112" font-size="10" fill="#999" text-anchor="middle">待機</text>
<rect x="273.1" y="77.4" width="451.9" height="42.6" fill="#4a7fb5" opacity="0.9"/>
<rect x="273.1" y="55.00000000000001" width="451.9" height="22.4" fill="#5fa86b" opacity="0.9"/>
<line x1="273.1" y1="32" x2="273.1" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<line x1="273.1" y1="32" x2="273.1" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<text x="730" y="49.00000000000001" font-size="12" font-weight="bold" fill="#333" text-anchor="end">年 3,422,524円</text>
<text x="70" y="20" font-size="12.5" font-weight="bold" fill="#333">③-a 繰下げ 70歳開始（×1.42 / +42%）</text>
</svg>

<svg viewBox="0 0 760 150" xmlns="http://www.w3.org/2000/svg" role="img" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="150" fill="#ffffff"/>
<line x1="70" y1="120" x2="725" y2="120" stroke="#8a9099" stroke-width="1.5"/><line x1="70.0" y1="28" x2="70.0" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="70.0" y="135" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text><line x1="171.6" y1="28" x2="171.6" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="171.6" y="135" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text><line x1="273.1" y1="28" x2="273.1" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="273.1" y="135" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text><line x1="374.7" y1="28" x2="374.7" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="374.7" y="135" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text><line x1="476.2" y1="28" x2="476.2" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="476.2" y="135" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text><line x1="577.8" y1="28" x2="577.8" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="577.8" y="135" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text><line x1="679.4" y1="28" x2="679.4" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="679.4" y="135" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<line x1="70.0" y1="120" x2="313.8" y2="120" stroke="#c9ccd1" stroke-width="7" stroke-dasharray="3 3"/>
<text x="191.9" y="112" font-size="10" fill="#999" text-anchor="middle">待機</text>
<rect x="313.8" y="72.4" width="411.2" height="47.6" fill="#4a7fb5" opacity="0.9"/>
<rect x="313.8" y="47.300000000000004" width="411.2" height="25.1" fill="#5fa86b" opacity="0.9"/>
<line x1="313.8" y1="32" x2="313.8" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<line x1="313.8" y1="32" x2="313.8" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<text x="730" y="41.300000000000004" font-size="12" font-weight="bold" fill="#333" text-anchor="end">年 3,827,442円</text>
<text x="70" y="20" font-size="12.5" font-weight="bold" fill="#333">③-b 繰下げ 72歳開始（×1.588 / +58.8%）</text>
</svg>

<svg viewBox="0 0 760 150" xmlns="http://www.w3.org/2000/svg" role="img" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="150" fill="#ffffff"/>
<line x1="70" y1="120" x2="725" y2="120" stroke="#8a9099" stroke-width="1.5"/><line x1="70.0" y1="28" x2="70.0" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="70.0" y="135" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text><line x1="171.6" y1="28" x2="171.6" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="171.6" y="135" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text><line x1="273.1" y1="28" x2="273.1" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="273.1" y="135" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text><line x1="374.7" y1="28" x2="374.7" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="374.7" y="135" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text><line x1="476.2" y1="28" x2="476.2" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="476.2" y="135" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text><line x1="577.8" y1="28" x2="577.8" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="577.8" y="135" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text><line x1="679.4" y1="28" x2="679.4" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="679.4" y="135" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<line x1="70.0" y1="120" x2="374.7" y2="120" stroke="#c9ccd1" stroke-width="7" stroke-dasharray="3 3"/>
<text x="222.35" y="112" font-size="10" fill="#999" text-anchor="middle">待機</text>
<rect x="374.7" y="64.8" width="350.3" height="55.2" fill="#4a7fb5" opacity="0.9"/>
<rect x="374.7" y="35.699999999999996" width="350.3" height="29.1" fill="#5fa86b" opacity="0.9"/>
<line x1="374.7" y1="32" x2="374.7" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<line x1="374.7" y1="32" x2="374.7" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<text x="730" y="29.699999999999996" font-size="12" font-weight="bold" fill="#333" text-anchor="end">年 4,434,820円</text>
<text x="70" y="20" font-size="12.5" font-weight="bold" fill="#333">③-c 繰下げ 75歳開始（×1.84 / +84%・上限）</text>
</svg>

- 70歳：年額 **3,422,524円** / 72歳：**3,827,442円** / 75歳：**4,434,820円**
- デメリット：待機中は年金ゼロ。**繰下げ待機中は加給年金がもらえない**
- **注意：繰下げで増えても“遺族年金”は増えない**（遺族厚生は本来額×3/4で計算）

---

## ④ 併用（厚生と基礎で時期をずらす）

厚生年金と基礎年金は**別々に**受給開始できる。例：**厚生は65歳から（生活費＆加給年金を確保）、基礎は75歳まで繰下げ**。

<svg viewBox="0 0 760 150" xmlns="http://www.w3.org/2000/svg" role="img" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="150" fill="#ffffff"/>
<line x1="70" y1="120" x2="725" y2="120" stroke="#8a9099" stroke-width="1.5"/><line x1="70.0" y1="28" x2="70.0" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="70.0" y="135" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text><line x1="171.6" y1="28" x2="171.6" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="171.6" y="135" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text><line x1="273.1" y1="28" x2="273.1" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="273.1" y="135" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text><line x1="374.7" y1="28" x2="374.7" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="374.7" y="135" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text><line x1="476.2" y1="28" x2="476.2" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="476.2" y="135" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text><line x1="577.8" y1="28" x2="577.8" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="577.8" y="135" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text><line x1="679.4" y1="28" x2="679.4" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="679.4" y="135" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<line x1="70.0" y1="120" x2="171.6" y2="120" stroke="#c9ccd1" stroke-width="7" stroke-dasharray="3 3"/>
<text x="120.8" y="112" font-size="10" fill="#999" text-anchor="middle">待機</text>
<rect x="171.6" y="90.0" width="553.4" height="30.0" fill="#4a7fb5" opacity="0.9"/>
<rect x="374.7" y="60.9" width="350.3" height="29.1" fill="#5fa86b" opacity="0.9"/>
<line x1="171.6" y1="32" x2="171.6" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<line x1="374.7" y1="32" x2="374.7" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<text x="730" y="54.9" font-size="12" font-weight="bold" fill="#333" text-anchor="end">年 3,108,856円</text>
<text x="730" y="38.9" font-size="10" fill="#888" text-anchor="end">(全部開始後)</text>
<text x="70" y="20" font-size="12.5" font-weight="bold" fill="#333">④ 併用：厚生65歳 ＋ 基礎75歳繰下げ</text>
</svg>

- 65〜74歳：厚生のみ 1,578,528円/年
- 75歳以降：合計 **3,108,856円/年**（基礎が＋84%）
- 基礎年金は**遺族厚生年金と全額併給**できるため、繰下げ増額が生涯まるごと残る（残された配偶者対策に有効）

---

## ⑤ Claude Code オススメ（いいとこ取り）

**厚生は65歳から・基礎は70歳まで繰下げ**。これまでの議論（遺族年金・加給年金）を踏まえたバランス重視の推奨案。

<svg viewBox="0 0 760 150" xmlns="http://www.w3.org/2000/svg" role="img" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="150" fill="#ffffff"/>
<line x1="70" y1="120" x2="725" y2="120" stroke="#8a9099" stroke-width="1.5"/><line x1="70.0" y1="28" x2="70.0" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="70.0" y="135" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text><line x1="171.6" y1="28" x2="171.6" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="171.6" y="135" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text><line x1="273.1" y1="28" x2="273.1" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="273.1" y="135" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text><line x1="374.7" y1="28" x2="374.7" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="374.7" y="135" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text><line x1="476.2" y1="28" x2="476.2" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="476.2" y="135" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text><line x1="577.8" y1="28" x2="577.8" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="577.8" y="135" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text><line x1="679.4" y1="28" x2="679.4" y2="120" stroke="#e6e8eb" stroke-width="1"/><text x="679.4" y="135" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<line x1="70.0" y1="120" x2="171.6" y2="120" stroke="#c9ccd1" stroke-width="7" stroke-dasharray="3 3"/>
<text x="120.8" y="112" font-size="10" fill="#999" text-anchor="middle">待機</text>
<rect x="171.6" y="90.0" width="553.4" height="30.0" fill="#4a7fb5" opacity="0.9"/>
<rect x="273.1" y="67.6" width="451.9" height="22.4" fill="#5fa86b" opacity="0.9"/>
<line x1="171.6" y1="32" x2="171.6" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<line x1="273.1" y1="32" x2="273.1" y2="120" stroke="#d6663b" stroke-width="1" stroke-dasharray="2 2"/>
<text x="730" y="61.599999999999994" font-size="12" font-weight="bold" fill="#333" text-anchor="end">年 2,759,542円</text>
<text x="730" y="45.599999999999994" font-size="10" fill="#888" text-anchor="end">(全部開始後)</text>
<text x="70" y="20" font-size="12.5" font-weight="bold" fill="#333">⑤ 推奨：厚生65歳 ＋ 基礎70歳繰下げ</text>
</svg>

- **厚生を65歳から**：繰り下げても遺族年金は増えない＆**加給年金を確保**できるため、65歳受給が合理的
- **基礎を70歳まで繰下げ（+42%）**：基礎は遺族厚生と**全額併給**で、本人にも残された配偶者にも生涯効く
- 65〜69歳：厚生のみ 1,578,528円/年 → 70歳以降：合計 **2,759,542円/年**
- 財力に余裕がない場合は、無理せず②（65歳から両方）でOK。遺族年金は変わりません

---

## 🎯 年齢による損益分岐点（このガイドの目的）

各パターンを「累計でいくら受け取ったか」で比較すると、線が交わる年齢が**損益分岐点**です。**その年齢より長生きすれば繰下げが得、短ければ繰上げ／65歳が得**になります。

<svg viewBox="0 0 760 440" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="440" fill="#ffffff"/>
<text x="20" y="26" font-size="15" font-weight="bold" fill="#333">年齢による損益分岐点（累計受給額の推移）</text>
<line x1="70" y1="390.0" x2="730" y2="390.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="64" y="394.0" font-size="10" fill="#8a9099" text-anchor="end">0万</text>
<line x1="70" y1="351.7" x2="730" y2="351.7" stroke="#e6e8eb" stroke-width="1"/>
<text x="64" y="355.7" font-size="10" fill="#8a9099" text-anchor="end">1000万</text>
<line x1="70" y1="313.3" x2="730" y2="313.3" stroke="#e6e8eb" stroke-width="1"/>
<text x="64" y="317.3" font-size="10" fill="#8a9099" text-anchor="end">2000万</text>
<line x1="70" y1="275.0" x2="730" y2="275.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="64" y="279.0" font-size="10" fill="#8a9099" text-anchor="end">3000万</text>
<line x1="70" y1="236.7" x2="730" y2="236.7" stroke="#e6e8eb" stroke-width="1"/>
<text x="64" y="240.7" font-size="10" fill="#8a9099" text-anchor="end">4000万</text>
<line x1="70" y1="198.3" x2="730" y2="198.3" stroke="#e6e8eb" stroke-width="1"/>
<text x="64" y="202.3" font-size="10" fill="#8a9099" text-anchor="end">5000万</text>
<line x1="70" y1="160.0" x2="730" y2="160.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="64" y="164.0" font-size="10" fill="#8a9099" text-anchor="end">6000万</text>
<line x1="70" y1="121.7" x2="730" y2="121.7" stroke="#e6e8eb" stroke-width="1"/>
<text x="64" y="125.7" font-size="10" fill="#8a9099" text-anchor="end">7000万</text>
<line x1="70" y1="83.3" x2="730" y2="83.3" stroke="#e6e8eb" stroke-width="1"/>
<text x="64" y="87.3" font-size="10" fill="#8a9099" text-anchor="end">8000万</text>
<line x1="70" y1="45.0" x2="730" y2="45.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="64" y="49.0" font-size="10" fill="#8a9099" text-anchor="end">9000万</text>
<line x1="70.0" y1="45" x2="70.0" y2="390" stroke="#e6e8eb" stroke-width="1"/>
<text x="70.0" y="406" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text>
<line x1="164.3" y1="45" x2="164.3" y2="390" stroke="#e6e8eb" stroke-width="1"/>
<text x="164.3" y="406" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text>
<line x1="258.6" y1="45" x2="258.6" y2="390" stroke="#e6e8eb" stroke-width="1"/>
<text x="258.6" y="406" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text>
<line x1="352.9" y1="45" x2="352.9" y2="390" stroke="#e6e8eb" stroke-width="1"/>
<text x="352.9" y="406" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text>
<line x1="447.1" y1="45" x2="447.1" y2="390" stroke="#e6e8eb" stroke-width="1"/>
<text x="447.1" y="406" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text>
<line x1="541.4" y1="45" x2="541.4" y2="390" stroke="#e6e8eb" stroke-width="1"/>
<text x="541.4" y="406" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text>
<line x1="635.7" y1="45" x2="635.7" y2="390" stroke="#e6e8eb" stroke-width="1"/>
<text x="635.7" y="406" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<line x1="730.0" y1="45" x2="730.0" y2="390" stroke="#e6e8eb" stroke-width="1"/>
<text x="730.0" y="406" font-size="11" fill="#8a9099" text-anchor="middle">95歳</text>
<line x1="70" y1="390" x2="730" y2="390" stroke="#8a9099" stroke-width="1.5"/>
<line x1="464.1" y1="45" x2="464.1" y2="390" stroke="#d6663b" stroke-width="1" stroke-dasharray="4 3" opacity="0.7"/>
<text x="464.1" y="41" font-size="10.5" font-weight="bold" fill="#d6663b" text-anchor="middle">81歳</text>
<line x1="484.9" y1="45" x2="484.9" y2="390" stroke="#d6663b" stroke-width="1" stroke-dasharray="4 3" opacity="0.7"/>
<text x="484.9" y="41" font-size="10.5" font-weight="bold" fill="#d6663b" text-anchor="middle">82歳</text>
<line x1="579.1" y1="45" x2="579.1" y2="390" stroke="#d6663b" stroke-width="1" stroke-dasharray="4 3" opacity="0.7"/>
<text x="579.1" y="41" font-size="10.5" font-weight="bold" fill="#d6663b" text-anchor="middle">87歳</text>
<polyline points="70.0,390.0 88.9,383.0 107.7,376.0 126.6,368.9 145.4,361.9 164.3,354.9 183.1,347.9 202.0,340.8 220.9,333.8 239.7,326.8 258.6,319.8 277.4,312.8 296.3,305.7 315.1,298.7 334.0,291.7 352.9,284.7 371.7,277.7 390.6,270.6 409.4,263.6 428.3,256.6 447.1,249.6 466.0,242.5 484.9,235.5 503.7,228.5 522.6,221.5 541.4,214.5 560.3,207.4 579.1,200.4 598.0,193.4 616.9,186.4 635.7,179.3 654.6,172.3 673.4,165.3 692.3,158.3 711.1,151.3 730.0,144.2" fill="none" stroke="#4a7fb5" stroke-width="2.4"/>
<text x="734.0" y="147.2" font-size="10.5" font-weight="bold" fill="#4a7fb5">①繰上60</text>
<polyline points="70.0,390.0 88.9,390.0 107.7,390.0 126.6,390.0 145.4,390.0 164.3,390.0 183.1,380.8 202.0,371.5 220.9,362.3 239.7,353.0 258.6,343.8 277.4,334.6 296.3,325.3 315.1,316.1 334.0,306.8 352.9,297.6 371.7,288.4 390.6,279.1 409.4,269.9 428.3,260.7 447.1,251.4 466.0,242.2 484.9,232.9 503.7,223.7 522.6,214.5 541.4,205.2 560.3,196.0 579.1,186.7 598.0,177.5 616.9,168.3 635.7,159.0 654.6,149.8 673.4,140.5 692.3,131.3 711.1,122.1 730.0,112.8" fill="none" stroke="#6b8e23" stroke-width="2.4"/>
<text x="734.0" y="115.8" font-size="10.5" font-weight="bold" fill="#6b8e23">②65本来</text>
<polyline points="70.0,390.0 88.9,390.0 107.7,390.0 126.6,390.0 145.4,390.0 164.3,390.0 183.1,390.0 202.0,390.0 220.9,390.0 239.7,390.0 258.6,390.0 277.4,376.9 296.3,363.8 315.1,350.6 334.0,337.5 352.9,324.4 371.7,311.3 390.6,298.2 409.4,285.0 428.3,271.9 447.1,258.8 466.0,245.7 484.9,232.6 503.7,219.4 522.6,206.3 541.4,193.2 560.3,180.1 579.1,167.0 598.0,153.8 616.9,140.7 635.7,127.6 654.6,114.5 673.4,101.4 692.3,88.2 711.1,75.1 730.0,62.0" fill="none" stroke="#b5894a" stroke-width="2.4"/>
<text x="734.0" y="65.0" font-size="10.5" font-weight="bold" fill="#b5894a">③繰下70</text>
<polyline points="70.0,390.0 88.9,390.0 107.7,390.0 126.6,390.0 145.4,390.0 164.3,390.0 183.1,390.0 202.0,390.0 220.9,390.0 239.7,390.0 258.6,390.0 277.4,390.0 296.3,390.0 315.1,390.0 334.0,390.0 352.9,390.0 371.7,373.0 390.6,356.0 409.4,339.0 428.3,322.0 447.1,305.0 466.0,288.0 484.9,271.0 503.7,254.0 522.6,237.0 541.4,220.0 560.3,203.0 579.1,186.0 598.0,169.0 616.9,152.0 635.7,135.0 654.6,118.0 673.4,101.0 692.3,84.0 711.1,67.0 730.0,50.0" fill="none" stroke="#8a5a2b" stroke-width="2.4"/>
<text x="734.0" y="53.0" font-size="10.5" font-weight="bold" fill="#8a5a2b">③繰下75</text>
<polyline points="70.0,390.0 88.9,390.0 107.7,390.0 126.6,390.0 145.4,390.0 164.3,390.0 183.1,383.9 202.0,377.9 220.9,371.8 239.7,365.8 258.6,359.7 277.4,349.2 296.3,338.6 315.1,328.0 334.0,317.4 352.9,306.9 371.7,296.3 390.6,285.7 409.4,275.1 428.3,264.5 447.1,254.0 466.0,243.4 484.9,232.8 503.7,222.2 522.6,211.6 541.4,201.1 560.3,190.5 579.1,179.9 598.0,169.3 616.9,158.8 635.7,148.2 654.6,137.6 673.4,127.0 692.3,116.4 711.1,105.9 730.0,95.3" fill="none" stroke="#d6663b" stroke-width="2.4"/>
<text x="734.0" y="98.3" font-size="10.5" font-weight="bold" fill="#d6663b">⑤推奨</text>
</svg>

### 損益分岐年齢（65歳受給を基準にした早見表）

| 比較 | 損益分岐年齢 | 読み方 |
| --- | --- | --- |
| ① 繰上げ60歳 vs ② 65歳 | **約81歳** | これより長生きするなら繰上げは損（65歳が逆転） |
| ③ 繰下げ70歳 vs ② 65歳 | **約82歳** | これより長生きするなら繰下げ70歳が得 |
| ③ 繰下げ72歳 vs ② 65歳 | **約84歳** | これより長生きするなら繰下げ72歳が得 |
| ③ 繰下げ75歳 vs ② 65歳 | **約87歳** | これより長生きするなら繰下げ75歳が得 |
| ⑤ 推奨(厚65/基70) vs ② 65歳 | **約82歳** | これより長生きするなら推奨案が得 |

> ざっくり：**繰下げは「受給開始からおよそ11〜12年」で元が取れる**（70歳開始なら約82歳、75歳開始なら約87歳）。日本人の平均余命（65歳男性≒85歳・女性≒90歳）を踏まえると、健康なら繰下げが分岐点を超えやすい計算です。

---

## 累計受給額の比較（90歳まで）

長生きするほど繰下げが有利。下図は各パターンを90歳まで受給した場合の累計です。

<svg viewBox="0 0 760 340" width="100%" style="max-width:760px;font-family:sans-serif">
<text x="20" y="24" font-size="14" font-weight="bold" fill="#333">90歳までの年金 累計受給額</text>
<text x="172" y="58" font-size="11.5" fill="#333" text-anchor="end">①繰上げ60歳</text>
<rect x="180" y="40" width="415" height="26" fill="#4a7fb5" opacity="0.85" rx="3"/>
<text x="601" y="58" font-size="11.5" font-weight="bold" fill="#333">5495万円</text>
<text x="172" y="98" font-size="11.5" fill="#333" text-anchor="end">②なし65歳</text>
<rect x="180" y="80" width="455" height="26" fill="#6b8e23" opacity="0.85" rx="3"/>
<text x="641" y="98" font-size="11.5" font-weight="bold" fill="#333">6026万円</text>
<text x="172" y="138" font-size="11.5" fill="#333" text-anchor="end">③繰下げ70歳</text>
<rect x="180" y="120" width="517" height="26" fill="#b5894a" opacity="0.85" rx="3"/>
<text x="703" y="138" font-size="11.5" font-weight="bold" fill="#333">6845万円</text>
<text x="172" y="178" font-size="11.5" fill="#333" text-anchor="end">③繰下げ72歳</text>
<rect x="180" y="160" width="520" height="26" fill="#b5894a" opacity="0.85" rx="3"/>
<text x="706" y="178" font-size="11.5" font-weight="bold" fill="#333">6889万円</text>
<text x="172" y="218" font-size="11.5" fill="#333" text-anchor="end">③繰下げ75歳</text>
<rect x="180" y="200" width="502" height="26" fill="#b5894a" opacity="0.85" rx="3"/>
<text x="688" y="218" font-size="11.5" font-weight="bold" fill="#333">6652万円</text>
<text x="172" y="258" font-size="11.5" fill="#333" text-anchor="end">④併用(厚65/基75)</text>
<rect x="180" y="240" width="471" height="26" fill="#7a5fa8" opacity="0.85" rx="3"/>
<text x="657" y="258" font-size="11.5" font-weight="bold" fill="#333">6242万円</text>
<text x="172" y="298" font-size="11.5" fill="#333" text-anchor="end">⑤推奨(厚65/基70)</text>
<rect x="180" y="280" width="476" height="26" fill="#d6663b" opacity="0.85" rx="3"/>
<text x="662" y="298" font-size="11.5" font-weight="bold" fill="#333">6308万円</text>
</svg>

| パターン | 80歳まで | 85歳まで | 90歳まで |
| --- | --- | --- | --- |
| ① 繰上げ60歳 | 3664万円 | 4579万円 | 5495万円 |
| ② なし65歳 | 3615万円 | 4820万円 | 6026万円 |
| ③ 繰下げ70歳 | 3423万円 | 5134万円 | 6845万円 |
| ③ 繰下げ72歳 | 3062万円 | 4976万円 | 6889万円 |
| ③ 繰下げ75歳 | 2217万円 | 4435万円 | 6652万円 |
| ④ 併用(厚65/基75) | 3133万円 | 4687万円 | 6242万円 |
| ⑤ 推奨(厚65/基70) | 3549万円 | 4929万円 | 6308万円 |

> 80歳前後が損益分岐の目安。**早く亡くなりそうなら繰上げ／②、長生き前提なら繰下げ**が有利です。

---

## まとめ

1. **厚生年金と基礎年金は別々に**繰上げ・繰下げできる（④⑤の併用が可能）。
2. **繰下げ＝一生増額**だが、待機中は無年金＆**加給年金が止まる**、そして**遺族年金は増えない**。
3. **基礎年金の繰下げは遺族厚生と全額併給**でき、残された配偶者にも効く（⑤推奨の核心）。
4. 財力に余裕がなければ②（65歳）で十分。遺族年金額は繰下げの有無で変わりません。

> 本ガイドはモデル前提を置いた概算です。実額は加入記録・年齢差・加給年金・在職老齢年金等で変わります。正確な試算は年金事務所・ねんきんネットでご確認ください。

関連：[遺族年金・遺族厚生年金 完全ガイド](survivors-pension-guide.md)
