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

## 💹 ⑥ 繰上げ60歳＋年利5%運用（早くもらって投資する作戦）

「**早くもらって運用すれば繰下げに勝てるか？**」を検証します。繰上げ60歳の年金（**1,831,773円/年**）を年利5%で運用するモデルです。

**前提（モデル）**

- **60〜64歳**：年金を全額、年利5%で運用（取り崩しゼロ）→ 65歳時点で元手 **約1012万円**
- **65歳以降**：年金を運用に回し続けつつ、生活の足しに**毎年1,200,000円（月10万円）取り崩し**、残りは5%運用を継続
- 比較対象（点線）：②65歳・③繰下げ75歳を**運用せず現金で受け取った**場合の累計

<svg viewBox="0 0 760 460" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="460" fill="#ffffff"/>
<text x="20" y="26" font-size="15" font-weight="bold" fill="#333">繰上げ60＋年利5%運用：資産の推移</text>
<rect x="78.0" y="55" width="89.6" height="345" fill="#eef4fb"/>
<text x="122.8" y="69" font-size="9.5" fill="#5a7fb0" text-anchor="middle">5年間 全額運用</text>
<text x="122.8" y="81" font-size="9.5" fill="#5a7fb0" text-anchor="middle">(取崩なし)</text>
<line x1="78" y1="400.0" x2="705" y2="400.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="72" y="404.0" font-size="10" fill="#8a9099" text-anchor="end">0万</text>
<line x1="78" y1="354.0" x2="705" y2="354.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="72" y="358.0" font-size="10" fill="#8a9099" text-anchor="end">2,000万</text>
<line x1="78" y1="308.0" x2="705" y2="308.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="72" y="312.0" font-size="10" fill="#8a9099" text-anchor="end">4,000万</text>
<line x1="78" y1="262.0" x2="705" y2="262.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="72" y="266.0" font-size="10" fill="#8a9099" text-anchor="end">6,000万</text>
<line x1="78" y1="216.0" x2="705" y2="216.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="72" y="220.0" font-size="10" fill="#8a9099" text-anchor="end">8,000万</text>
<line x1="78" y1="170.0" x2="705" y2="170.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="72" y="174.0" font-size="10" fill="#8a9099" text-anchor="end">10,000万</text>
<line x1="78" y1="124.0" x2="705" y2="124.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="72" y="128.0" font-size="10" fill="#8a9099" text-anchor="end">12,000万</text>
<line x1="78" y1="78.0" x2="705" y2="78.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="72" y="82.0" font-size="10" fill="#8a9099" text-anchor="end">14,000万</text>
<text x="78.0" y="416" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text>
<text x="167.6" y="416" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text>
<text x="257.1" y="416" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text>
<text x="346.7" y="416" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text>
<text x="436.3" y="416" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text>
<text x="525.9" y="416" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text>
<text x="615.4" y="416" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<text x="705.0" y="416" font-size="11" fill="#8a9099" text-anchor="middle">95歳</text>
<line x1="78" y1="400" x2="705" y2="400" stroke="#8a9099" stroke-width="1.5"/>
<polygon points="78.0,400.0 78.0,400.0 95.9,395.8 113.8,391.4 131.7,386.7 149.7,381.8 167.6,376.7 185.5,374.1 203.4,371.4 221.3,368.5 239.2,365.4 257.1,362.3 275.1,358.9 293.0,355.4 310.9,351.7 328.8,347.9 346.7,343.8 364.6,339.5 382.5,335.1 400.5,330.4 418.4,325.4 436.3,320.2 454.2,314.8 472.1,309.1 490.0,303.1 507.9,296.8 525.9,290.2 543.8,283.2 561.7,275.9 579.6,268.3 597.5,260.3 615.4,251.8 633.3,243.0 651.3,233.6 669.2,223.9 687.1,213.6 705.0,202.8 705.0,400.0" fill="#4a7fb5" opacity="0.25"/>
<polyline points="78.0,400.0 95.9,395.8 113.8,391.4 131.7,386.7 149.7,381.8 167.6,376.7 185.5,374.1 203.4,371.4 221.3,368.5 239.2,365.4 257.1,362.3 275.1,358.9 293.0,355.4 310.9,351.7 328.8,347.9 346.7,343.8 364.6,339.5 382.5,335.1 400.5,330.4 418.4,325.4 436.3,320.2 454.2,314.8 472.1,309.1 490.0,303.1 507.9,296.8 525.9,290.2 543.8,283.2 561.7,275.9 579.6,268.3 597.5,260.3 615.4,251.8 633.3,243.0 651.3,233.6 669.2,223.9 687.1,213.6 705.0,202.8" fill="none" stroke="#4a7fb5" stroke-width="2.4"/>
<polyline points="78.0,400.0 95.9,395.8 113.8,391.4 131.7,386.7 149.7,381.8 167.6,376.7 185.5,371.3 203.4,365.8 221.3,360.2 239.2,354.4 257.1,348.5 275.1,342.4 293.0,336.1 310.9,329.6 328.8,323.0 346.7,316.2 364.6,309.2 382.5,301.9 400.5,294.5 418.4,286.8 436.3,278.8 454.2,270.6 472.1,262.2 490.0,253.4 507.9,244.4 525.9,235.0 543.8,225.3 561.7,215.2 579.6,204.8 597.5,194.0 615.4,182.8 633.3,171.2 651.3,159.1 669.2,146.6 687.1,133.6 705.0,120.0" fill="none" stroke="#d6663b" stroke-width="2.6"/>
<polyline points="78.0,400.0 95.9,400.0 113.8,400.0 131.7,400.0 149.7,400.0 167.6,400.0 185.5,394.5 203.4,388.9 221.3,383.4 239.2,377.8 257.1,372.3 275.1,366.7 293.0,361.2 310.9,355.7 328.8,350.1 346.7,344.6 364.6,339.0 382.5,333.5 400.5,327.9 418.4,322.4 436.3,316.8 454.2,311.3 472.1,305.8 490.0,300.2 507.9,294.7 525.9,289.1 543.8,283.6 561.7,278.0 579.6,272.5 597.5,267.0 615.4,261.4 633.3,255.9 651.3,250.3 669.2,244.8 687.1,239.2 705.0,233.7" fill="none" stroke="#6b8e23" stroke-width="2" stroke-dasharray="5 3"/>
<polyline points="78.0,400.0 95.9,400.0 113.8,400.0 131.7,400.0 149.7,400.0 167.6,400.0 185.5,400.0 203.4,400.0 221.3,400.0 239.2,400.0 257.1,400.0 275.1,400.0 293.0,400.0 310.9,400.0 328.8,400.0 346.7,400.0 364.6,389.8 382.5,379.6 400.5,369.4 418.4,359.2 436.3,349.0 454.2,338.8 472.1,328.6 490.0,318.4 507.9,308.2 525.9,298.0 543.8,287.8 561.7,277.6 579.6,267.4 597.5,257.2 615.4,247.0 633.3,236.8 651.3,226.6 669.2,216.4 687.1,206.2 705.0,196.0" fill="none" stroke="#8a5a2b" stroke-width="2" stroke-dasharray="5 3"/>
<text x="707.0" y="123.0" font-size="10" font-weight="bold" fill="#d6663b">経済価値</text>
<text x="707.0" y="214.8" font-size="10" font-weight="bold" fill="#4a7fb5">運用残高</text>
<text x="707.0" y="199.0" font-size="9.5" fill="#8a5a2b">③繰下75(現金)</text>
<text x="707.0" y="236.7" font-size="9.5" fill="#6b8e23">②65歳(現金)</text>
</svg>

### 年齢別の資産（繰上げ60＋運用）

| 年齢 | 運用残高 | 取崩累計 | 経済価値(残高+取崩) | 参考:②65現金累計 | 参考:③繰下75現金累計 |
| --- | --- | --- | --- | --- | --- |
| 65歳 | 1,012万円 | 0万円 | **1,012万円** | 0万円 | 0万円 |
| 70歳 | 1,641万円 | 600万円 | **2,241万円** | 1,205万円 | 0万円 |
| 75歳 | 2,443万円 | 1,200万円 | **3,643万円** | 2,410万円 | 0万円 |
| 80歳 | 3,468万円 | 1,800万円 | **5,268万円** | 3,615万円 | 2,217万円 |
| 85歳 | 4,775万円 | 2,400万円 | **7,175万円** | 4,820万円 | 4,435万円 |
| 90歳 | 6,443万円 | 3,000万円 | **9,443万円** | 6,026万円 | 6,652万円 |
| 95歳 | 8,572万円 | 3,600万円 | **12,172万円** | 7,231万円 | 8,870万円 |

> 👀 **ポイント**：5%で運用できるなら、**繰上げ60＋運用の経済価値は早い段階から現金受給を上回り続けます**。繰上げの「一生▲24%減額」という弱点を、5年間の運用益と複利が補って余りある計算です。

> ⚠️ **公平のための注意**：これは「60歳パターンだけ運用」という指定どおりの試算です。**②65歳や③繰下げも同様に5%運用すれば結果は変わります**（例：②65歳の年金も5%運用すると90歳で約1.1億円）。また**年利5%は元本保証ではなく価格変動・元本割れリスク**があり、繰下げ（+0.7%/月＝公的保証の増額）とは性質が異なります。「確実性の繰下げ」か「期待値の運用」かは、リスク許容度次第です。

---

## ⚖️ ⑦ 公平比較：全パターンを同じ年利5%で運用したら？

⑥は「60歳だけ運用」でしたが、ここでは**どのパターンも受け取った年金を全額・年利5%で運用**（取り崩しなし）した**純資産**で比較します。早くもらうほど運用期間が長く、複利が効きます。

<svg viewBox="0 0 760 440" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="440" fill="#ffffff"/>
<text x="20" y="26" font-size="15" font-weight="bold" fill="#333">全パターンを年利5%で運用した純資産</text>
<text x="20" y="44" font-size="11.5" fill="#777">各パターンの年金を全額・年利5%で積立運用(取り崩しなし)した場合の残高</text>
<line x1="82" y1="392.0" x2="665" y2="392.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="396.0" font-size="10" fill="#8a9099" text-anchor="end">0万</text>
<line x1="82" y1="356.2" x2="665" y2="356.2" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="360.2" font-size="10" fill="#8a9099" text-anchor="end">2,000万</text>
<line x1="82" y1="320.4" x2="665" y2="320.4" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="324.4" font-size="10" fill="#8a9099" text-anchor="end">4,000万</text>
<line x1="82" y1="284.7" x2="665" y2="284.7" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="288.7" font-size="10" fill="#8a9099" text-anchor="end">6,000万</text>
<line x1="82" y1="248.9" x2="665" y2="248.9" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="252.9" font-size="10" fill="#8a9099" text-anchor="end">8,000万</text>
<line x1="82" y1="213.1" x2="665" y2="213.1" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="217.1" font-size="10" fill="#8a9099" text-anchor="end">10,000万</text>
<line x1="82" y1="177.3" x2="665" y2="177.3" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="181.3" font-size="10" fill="#8a9099" text-anchor="end">12,000万</text>
<line x1="82" y1="141.6" x2="665" y2="141.6" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="145.6" font-size="10" fill="#8a9099" text-anchor="end">14,000万</text>
<line x1="82" y1="105.8" x2="665" y2="105.8" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="109.8" font-size="10" fill="#8a9099" text-anchor="end">16,000万</text>
<line x1="82" y1="70.0" x2="665" y2="70.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="74.0" font-size="10" fill="#8a9099" text-anchor="end">18,000万</text>
<text x="82.0" y="408" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text>
<text x="165.3" y="408" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text>
<text x="248.6" y="408" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text>
<text x="331.9" y="408" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text>
<text x="415.1" y="408" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text>
<text x="498.4" y="408" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text>
<text x="581.7" y="408" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<text x="665.0" y="408" font-size="11" fill="#8a9099" text-anchor="middle">95歳</text>
<line x1="82" y1="392" x2="665" y2="392" stroke="#8a9099" stroke-width="1.5"/>
<polyline points="82.0,392.0 98.7,388.7 115.3,385.3 132.0,381.7 148.6,377.9 165.3,373.9 181.9,369.7 198.6,365.3 215.3,360.7 231.9,355.9 248.6,350.8 265.2,345.4 281.9,339.8 298.5,334.0 315.2,327.8 331.9,321.3 348.5,314.5 365.2,307.3 381.8,299.8 398.5,291.9 415.1,283.6 431.8,275.0 448.5,265.8 465.1,256.2 481.8,246.2 498.4,235.6 515.1,224.5 531.7,212.9 548.4,200.6 565.1,187.8 581.7,174.3 598.4,160.1 615.0,145.3 631.7,129.6 648.3,113.2 665.0,96.0" fill="none" stroke="#4a7fb5" stroke-width="2.4"/>
<polyline points="82.0,392.0 98.7,392.0 115.3,392.0 132.0,392.0 148.6,392.0 165.3,392.0 181.9,387.7 198.6,383.2 215.3,378.4 231.9,373.4 248.6,368.2 265.2,362.7 281.9,356.9 298.5,350.8 315.2,344.5 331.9,337.8 348.5,330.7 365.2,323.4 381.8,315.6 398.5,307.5 415.1,299.0 431.8,290.0 448.5,280.6 465.1,270.7 481.8,260.3 498.4,249.4 515.1,238.0 531.7,226.0 548.4,213.4 565.1,200.1 581.7,186.2 598.4,171.6 615.0,156.3 631.7,140.2 648.3,123.3 665.0,105.5" fill="none" stroke="#6b8e23" stroke-width="2.4"/>
<polyline points="82.0,392.0 98.7,392.0 115.3,392.0 132.0,392.0 148.6,392.0 165.3,392.0 181.9,392.0 198.6,392.0 215.3,392.0 231.9,392.0 248.6,392.0 265.2,385.9 281.9,379.4 298.5,372.7 315.2,365.6 331.9,358.2 348.5,350.4 365.2,342.2 381.8,333.5 398.5,324.5 415.1,315.0 431.8,305.0 448.5,294.5 465.1,283.6 481.8,272.0 498.4,259.9 515.1,247.2 531.7,233.8 548.4,219.8 565.1,205.0 581.7,189.6 598.4,173.3 615.0,156.3 631.7,138.3 648.3,119.5 665.0,99.8" fill="none" stroke="#b5894a" stroke-width="2.4"/>
<polyline points="82.0,392.0 98.7,392.0 115.3,392.0 132.0,392.0 148.6,392.0 165.3,392.0 181.9,392.0 198.6,392.0 215.3,392.0 231.9,392.0 248.6,392.0 265.2,392.0 281.9,392.0 298.5,392.0 315.2,392.0 331.9,392.0 348.5,384.1 365.2,375.7 381.8,367.0 398.5,357.8 415.1,348.2 431.8,338.0 448.5,327.4 465.1,316.2 481.8,304.5 498.4,292.2 515.1,279.3 531.7,265.7 548.4,251.5 565.1,236.5 581.7,220.8 598.4,204.3 615.0,187.0 631.7,168.8 648.3,149.7 665.0,129.7" fill="none" stroke="#8a5a2b" stroke-width="2.4"/>
<polyline points="82.0,392.0 98.7,392.0 115.3,392.0 132.0,392.0 148.6,392.0 165.3,392.0 181.9,389.2 198.6,386.2 215.3,383.1 231.9,379.8 248.6,376.4 265.2,370.7 281.9,364.7 298.5,358.4 315.2,351.8 331.9,344.8 348.5,337.5 365.2,329.9 381.8,321.8 398.5,313.4 415.1,304.5 431.8,295.2 448.5,285.4 465.1,275.1 481.8,264.4 498.4,253.0 515.1,241.2 531.7,228.7 548.4,215.6 565.1,201.8 581.7,187.4 598.4,172.2 615.0,156.3 631.7,139.6 648.3,122.0 665.0,103.6" fill="none" stroke="#d6663b" stroke-width="2.4"/>
<text x="669" y="99.0" font-size="10" font-weight="bold" fill="#4a7fb5">①繰上60</text>
<text x="669" y="111.0" font-size="10" font-weight="bold" fill="#b5894a">③繰下70</text>
<text x="669" y="123.0" font-size="10" font-weight="bold" fill="#d6663b">⑤推奨</text>
<text x="669" y="135.0" font-size="10" font-weight="bold" fill="#6b8e23">②65歳</text>
<text x="669" y="147.0" font-size="10" font-weight="bold" fill="#8a5a2b">③繰下75</text>
</svg>

| 年齢 | ①繰上60 | ②65歳 | ③繰下70 | ③繰下75 | ⑤推奨 |
| --- | --- | --- | --- | --- | --- |
| 80歳 | 6,057万 | 5,201万 | 4,305万 | 2,451万 | 4,892万 |
| 85歳 | 8,743万 | 7,970万 | 7,385万 | 5,578万 | 7,768万 |
| 90歳 | 12,170万 | 11,503万 | 11,317万 | 9,570万 | 11,439万 |
| 95歳 | 16,545万 | 16,013万 | 16,335万 | 14,664万 | 16,124万 |

> 👀 **結論：全員が同率で運用すると、むしろ①繰上げ60歳が長く優位**（90歳時点でも最大級）。**運用前提では「早くもらう」ほど有利**になりやすく、繰下げの“増額”メリットは運用益に追いつかれます。ただし繰下げの本質的価値は**「死ぬまで増えた年金が保証される」長生き・インフレ保険**であり、運用は**元本割れリスク**を負う点が決定的に違います。

---

## 📈 ⑧ 感応度分析：年利が何%なら運用が勝てる？

「繰上げ60歳を運用」した**純資産**を、年利**3%/4%/5%**で比べ、繰下げ・本来受給を**運用せず現金で受け取った**場合（点線）と対比します。

<svg viewBox="0 0 760 440" width="100%" style="max-width:760px;font-family:sans-serif">
<rect x="0" y="0" width="760" height="440" fill="#ffffff"/>
<text x="20" y="26" font-size="15" font-weight="bold" fill="#333">繰上げ60の運用(3/4/5%) vs 繰下げ・本来の現金受給</text>
<text x="20" y="44" font-size="11.5" fill="#777">実線=繰上げ60を各利回りで運用した純資産 / 点線=無運用の累計受給(現金)</text>
<line x1="82" y1="392.0" x2="665" y2="392.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="396.0" font-size="10" fill="#8a9099" text-anchor="end">0万</text>
<line x1="82" y1="356.2" x2="665" y2="356.2" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="360.2" font-size="10" fill="#8a9099" text-anchor="end">2,000万</text>
<line x1="82" y1="320.4" x2="665" y2="320.4" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="324.4" font-size="10" fill="#8a9099" text-anchor="end">4,000万</text>
<line x1="82" y1="284.7" x2="665" y2="284.7" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="288.7" font-size="10" fill="#8a9099" text-anchor="end">6,000万</text>
<line x1="82" y1="248.9" x2="665" y2="248.9" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="252.9" font-size="10" fill="#8a9099" text-anchor="end">8,000万</text>
<line x1="82" y1="213.1" x2="665" y2="213.1" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="217.1" font-size="10" fill="#8a9099" text-anchor="end">10,000万</text>
<line x1="82" y1="177.3" x2="665" y2="177.3" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="181.3" font-size="10" fill="#8a9099" text-anchor="end">12,000万</text>
<line x1="82" y1="141.6" x2="665" y2="141.6" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="145.6" font-size="10" fill="#8a9099" text-anchor="end">14,000万</text>
<line x1="82" y1="105.8" x2="665" y2="105.8" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="109.8" font-size="10" fill="#8a9099" text-anchor="end">16,000万</text>
<line x1="82" y1="70.0" x2="665" y2="70.0" stroke="#e6e8eb" stroke-width="1"/>
<text x="76" y="74.0" font-size="10" fill="#8a9099" text-anchor="end">18,000万</text>
<text x="82.0" y="408" font-size="11" fill="#8a9099" text-anchor="middle">60歳</text>
<text x="165.3" y="408" font-size="11" fill="#8a9099" text-anchor="middle">65歳</text>
<text x="248.6" y="408" font-size="11" fill="#8a9099" text-anchor="middle">70歳</text>
<text x="331.9" y="408" font-size="11" fill="#8a9099" text-anchor="middle">75歳</text>
<text x="415.1" y="408" font-size="11" fill="#8a9099" text-anchor="middle">80歳</text>
<text x="498.4" y="408" font-size="11" fill="#8a9099" text-anchor="middle">85歳</text>
<text x="581.7" y="408" font-size="11" fill="#8a9099" text-anchor="middle">90歳</text>
<text x="665.0" y="408" font-size="11" fill="#8a9099" text-anchor="middle">95歳</text>
<line x1="82" y1="392" x2="665" y2="392" stroke="#8a9099" stroke-width="1.5"/>
<polyline points="82.0,392.0 98.7,388.7 115.3,385.3 132.0,381.7 148.6,377.9 165.3,373.9 181.9,369.7 198.6,365.3 215.3,360.7 231.9,355.9 248.6,350.8 265.2,345.4 281.9,339.8 298.5,334.0 315.2,327.8 331.9,321.3 348.5,314.5 365.2,307.3 381.8,299.8 398.5,291.9 415.1,283.6 431.8,275.0 448.5,265.8 465.1,256.2 481.8,246.2 498.4,235.6 515.1,224.5 531.7,212.9 548.4,200.6 565.1,187.8 581.7,174.3 598.4,160.1 615.0,145.3 631.7,129.6 648.3,113.2 665.0,96.0" fill="none" stroke="#c0392b" stroke-width="2.4"/>
<polyline points="82.0,392.0 98.7,388.7 115.3,385.3 132.0,381.8 148.6,378.1 165.3,374.3 181.9,370.3 198.6,366.1 215.3,361.8 231.9,357.3 248.6,352.7 265.2,347.8 281.9,342.8 298.5,337.5 315.2,332.1 331.9,326.4 348.5,320.5 365.2,314.3 381.8,308.0 398.5,301.3 415.1,294.4 431.8,287.2 448.5,279.8 465.1,272.0 481.8,263.9 498.4,255.5 515.1,246.8 531.7,237.7 548.4,228.3 565.1,218.4 581.7,208.2 598.4,197.6 615.0,186.5 631.7,175.0 648.3,163.1 665.0,150.7" fill="none" stroke="#e67e22" stroke-width="2.4"/>
<polyline points="82.0,392.0 98.7,388.7 115.3,385.3 132.0,381.9 148.6,378.3 165.3,374.6 181.9,370.8 198.6,366.9 215.3,362.9 231.9,358.7 248.6,354.4 265.2,350.0 281.9,345.5 298.5,340.8 315.2,336.0 331.9,331.1 348.5,325.9 365.2,320.7 381.8,315.3 398.5,309.7 415.1,304.0 431.8,298.0 448.5,291.9 465.1,285.7 481.8,279.2 498.4,272.5 515.1,265.7 531.7,258.6 548.4,251.3 565.1,243.8 581.7,236.1 598.4,228.1 615.0,220.0 631.7,211.5 648.3,202.8 665.0,193.9" fill="none" stroke="#f0b27a" stroke-width="2.4"/>
<polyline points="82.0,392.0 98.7,392.0 115.3,392.0 132.0,392.0 148.6,392.0 165.3,392.0 181.9,392.0 198.6,392.0 215.3,392.0 231.9,392.0 248.6,392.0 265.2,392.0 281.9,392.0 298.5,392.0 315.2,392.0 331.9,392.0 348.5,384.1 365.2,376.1 381.8,368.2 398.5,360.3 415.1,352.3 431.8,344.4 448.5,336.5 465.1,328.5 481.8,320.6 498.4,312.7 515.1,304.7 531.7,296.8 548.4,288.9 565.1,280.9 581.7,273.0 598.4,265.1 615.0,257.1 631.7,249.2 648.3,241.3 665.0,233.3" fill="none" stroke="#8a5a2b" stroke-width="2.4" stroke-dasharray="5 3"/>
<polyline points="82.0,392.0 98.7,392.0 115.3,392.0 132.0,392.0 148.6,392.0 165.3,392.0 181.9,387.7 198.6,383.4 215.3,379.1 231.9,374.8 248.6,370.4 265.2,366.1 281.9,361.8 298.5,357.5 315.2,353.2 331.9,348.9 348.5,344.6 365.2,340.3 381.8,335.9 398.5,331.6 415.1,327.3 431.8,323.0 448.5,318.7 465.1,314.4 481.8,310.1 498.4,305.8 515.1,301.5 531.7,297.1 548.4,292.8 565.1,288.5 581.7,284.2 598.4,279.9 615.0,275.6 631.7,271.3 648.3,267.0 665.0,262.7" fill="none" stroke="#6b8e23" stroke-width="2.4" stroke-dasharray="5 3"/>
<text x="669" y="99.0" font-size="10" font-weight="bold" fill="#c0392b">繰上60@5%</text>
<text x="669" y="153.7" font-size="10" font-weight="bold" fill="#e67e22">繰上60@4%</text>
<text x="669" y="196.9" font-size="10" font-weight="bold" fill="#f0b27a">繰上60@3%</text>
<text x="669" y="236.3" font-size="10" font-weight="bold" fill="#8a5a2b">③繰下75(現金)</text>
<text x="669" y="265.7" font-size="10" font-weight="bold" fill="#6b8e23">②65歳(現金)</text>
</svg>

| 年齢 | 繰上60@3% | 繰上60@4% | 繰上60@5% | ③繰下75(現金) | ②65歳(現金) |
| --- | --- | --- | --- | --- | --- |
| 80歳 | 4,922万 | 5,455万 | 6,057万 | 2,217万 | 3,615万 |
| 85歳 | 6,679万 | 7,629万 | 8,743万 | 4,435万 | 4,820万 |
| 90歳 | 8,715万 | 10,273万 | 12,170万 | 6,652万 | 6,026万 |
| 95歳 | 11,075万 | 13,491万 | 16,545万 | 8,870万 | 7,231万 |

> 👀 **しきい値**：繰上げ60を運用した純資産が、90歳時点で③繰下げ75歳の現金累計に並ぶ利回りは**わずか約1.3%**。つまり**年1〜2%でも運用できれば、現金で受け取る繰下げの“受給総額”は上回ります**（複利と早期受給の効果）。

> ⚠️ ただし上記は**現金（無運用）の繰下げ**との比較です。繰下げの真価は受給額そのものではなく、**生涯保証・長生き保険・遺族年金の土台**にあります。「期待リターンの運用」か「確実性の繰下げ」かは、**運用リスクを取れるか／長生きにどう備えるか**で選ぶのが本筋です。

---

## まとめ

1. **厚生年金と基礎年金は別々に**繰上げ・繰下げできる（④⑤の併用が可能）。
2. **繰下げ＝一生増額**だが、待機中は無年金＆**加給年金が止まる**、そして**遺族年金は増えない**。
3. **基礎年金の繰下げは遺族厚生と全額併給**でき、残された配偶者にも効く（⑤推奨の核心）。
4. 財力に余裕がなければ②（65歳）で十分。遺族年金額は繰下げの有無で変わりません。
5. **運用前提（⑥⑦⑧）では「早くもらって投資」が受給総額で有利**になりやすい。ただし繰下げは**元本割れのない生涯保証・長生き保険**——“期待値の運用”か“確実性の繰下げ”かはリスク許容度で選ぶ。

> 本ガイドはモデル前提を置いた概算です。実額は加入記録・年齢差・加給年金・在職老齢年金等で変わります。正確な試算は年金事務所・ねんきんネットでご確認ください。

関連：[遺族年金・遺族厚生年金 完全ガイド](survivors-pension-guide.md)
