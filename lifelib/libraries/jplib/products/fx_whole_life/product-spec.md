# Product Specification

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** This is a *standardized composite specification* of Japanese
foreign-currency-denominated whole life assurance (*gaika-date shūshin hoken*, 外貨建終身保険)
in its variable-crediting-rate (*tsumitate riritsu hendō gata*, 積立利率変動型) form, assembled for
reference liability cash-flow modeling. It does not describe any single insurer's product.
Facts carrying a source tag — [S#] (primary product documents: policy conditions (*yakkan*,
約款), policy handbook (ご契約のしおり), 商品パンフレット and published rate pages) and [R#]
(regulatory and actuarial references), both numbered per `_research/fx-whole-life.md` and
resolved in `sources.md` (same directory; numbering frozen, never renumbered), and [REG-R#]
(the cross-product reference library `references/regulatory-and-actuarial-references.md`,
whose own R-numbering is distinct) — were extracted from the cited document. Values marked
**[std]** are standardizations introduced for the reference implementation; each [std] table
row carries a numbered footnote giving the rationale and, where one exists, the observed
range across insurers. Facts the research pass could not verify are flagged [unverified].
The composite is drawn from eight carriers, of which three publish policy-conditions-grade
documents [S2] [S3] [S7], four publish live rate pages [S4] [S6] [S12] [S14], and one
publishes the only front-end charge scale in the set [S10]; a distributor's 重要情報シート
supplies the only quantified commission structure [S13].

**This product inherits the savings chassis.** Everything about policy reserve
(*sekinin-junbikin*, 責任準備金), surrender value (*kaiyaku-henreikin*, 解約返戻金) as a function of
elapsed and paid months, policy loan (*keiyakusha kashitsuke*, 契約者貸付), automatic premium
loan (*jidō furikae kashitsuke*, 自動振替貸付, APL), grace (猶予期間), lapse (失効), reinstatement (復活),
reduced paid-up (払済保険), sum-assured reduction (減額), severe-disability benefit (高度障害保険金) and
the suppressed-surrender-value (*tei-kaiyaku-henreikin-gata*, 低解約返戻金型) cliff is
specified once, in the [whole life product specification (終身保険)](../whole_life/product-spec.md), and is
**not restated here**. This document specifies only the three layers that make this a
different product — the **currency layer**, the **crediting layer** and the **surrender
layer** — plus the target-value conversion rider that follows from them, and the deltas
those layers force on the inherited mechanics.

---

## Product overview and market role

外貨建終身保険 is whole-of-life cover written in a foreign currency, almost always the US
dollar. Premiums are paid in yen and converted to the operating currency, the account value
accumulates in that currency at a rate the insurer declares, benefits are denominated in
that currency, and payment is converted back to yen — so the policyholder holds a
whole-life contract *and* an unhedged currency position, and can lose money against
premiums paid without the insurer's crediting rate ever going wrong. It is a
first-sector (*dai-ichi bun'ya*, 第一分野) contract under 保険業法第3条第4項第1号 [REG-R1], and because a
loss may arise from movements in currency values and interest rates it is also a specified
insurance contract (*tokutei hoken keiyaku*, **特定保険契約**) under 保険業法第300条の2, which pulls
FIEA-grade conduct rules — advertising, pre-contract disclosure, the suitability principle
(適合性の原則) — across to it by 準用 [REG-R37] [S5] [R3]. That single classification is the
reason this product's documentation, distribution and supervision look nothing like those of
the yen whole life it otherwise resembles.

**Three structurally different products are sold under the label, and the difference decides
the model.** The retrieved set separates cleanly:

1. **積立利率変動型, level premium.** The crediting rate is redeclared monthly and applied to an
   account value; there is **no** market value adjustment; the floor is the contract's own
   assumed interest rate (*yotei riritsu*, 予定利率), fixed at issue [S1] [S2].
2. **積立利率更改型 / 保証期間型, single premium.** The rate is fixed for a multi-year 積立利率適用期間
   and reset at each 積立利率計算基準日; surrender inside the period carries a market value
   adjustment, MVA (*shijō kakaku chōsei*, **市場価格調整**) [S3] [S4] [S8] [S12] [S14].
3. **指定通貨建 with a yen-fixed premium.** The premium is a level *yen* amount converted to
   USD each month and the 予定利率 resets every five years after 払込満了; the carrier states
   explicitly that the product has no MVA [S5] [S6].

The composite carries the **first two as a model-point parameter** and excludes the third
(footnote 1). A fourth neighbour — a USD whole life on a fixed 予定利率, with no crediting rate
and no MVA [S7] — is not this product at all: it is
[whole life (終身保険)](../whole_life/product-spec.md) with a currency layer, and it is used here only for
the mechanics the two share.

**Market role: a bank- and securities-channel savings substitute, and the most heavily
supervised retail life product in Japan.** No retrieved document gives a new-business volume
for 外貨建終身保険 specifically [unverified], but the conduct record is quantified in unusual
detail. About **60% of 外貨建一時払保険 are surrendered within four years** of purchase, and the
average holding period is **2.5 years** — against a whole-life contract with no maturity
date [R5] [R6]. Read against the industry-wide 解約・失効率 of 5.6% of sum assured [REG-R31], that
is not a lapse assumption transplanted from another product; it is a different behavioural
regime, and any model of this product that borrows a yen whole life's persistency is wrong
by an order of magnitude. The FSA's decomposition of one 2023 run-off cohort of **549,781**
policies found the crediting rate contributed thinly, most of the gain came from a weaker
yen, and **市場価格調整と解約控除費 pushed the realized margin down** [R5]. Distributor commission is
L-shaped — about **5.5% in year one against 0.1% thereafter** [R5], corroborated by the one
published schedule, 契約時手数料 of 4.00% or 2.60% of the single premium with a 継続手数料 of up to
0.75% p.a. for at most seven years [S13].

Complaints drove the supervision. Bank-channel 外貨建保険 complaints rose from **597 in 2012 to
2,543 in 2018**, with 2019 first-half running at an annualized 2,704; **68% were 説明不十分**
(inadequate explanation), and inside those, 元本割れリスク 37%, 適合性の確認 14% and mistaking the product
for a deposit (預金誤認) 8% [R7]. The complaint *rate* against in-force count fell from
0.14% to 0.08% over the same window [R7] — the product was growing faster than the
complaints. The industry response was an examination and then a licence: the 生命保険協会
created the 外貨建保険販売資格試験, with the common textbook from about April 2020, the examination
from October 2020, and a **販売資格者登録制 from around April 2022**, after which an unregistered
募集人 cannot sell the product [R7]. The FSA's own earlier framing had already required the
sales material to be comparable with an investment trust's prospectus (目論見書) [R9].

Demand has the same two tax drivers as the yen product — the ¥5,000,000 × statutory heirs
death-benefit exemption [REG-R44] [REG-R45] and the 一般 basket of the 生命保険料控除 [REG-R43]
[S13] — plus a third the yen product cannot offer: a US dollar crediting rate. In the
2026-08-16 window the declared 積立利率 on one single-premium contract was **4.72%** [S4] and
another carrier's 基準利率 was **5.15% / 5.29%** for 10- and 15-year guarantee periods [S14].
No retrieved source in *this* product's set prices a yen whole life, so the comparison is
made against the chassis, whose composite 予定利率 is **1.75%** — the only level-premium
figure any carrier in *that* product's set disclosed, dated 2010, with the current value
[unverified] there (the [whole life product specification (終身保険)](../whole_life/product-spec.md)).
The gap *is* the product's sales proposition, and the currency risk is what pays for it.

**The reserving regime is younger than the product,** and its scope decides the
composite's currency. Only US-dollar- and Australian-dollar-denominated contracts are
inside standard policy reserve (*hyōjun sekinin-junbikin*, 標準責任準備金) at all; every other
foreign currency is excluded from the 対象契約 [R1] [REG-R12]. So the composite is
US-dollar-denominated and treats AUD as a parameter rather than a second product, while a
euro-denominated contract — which one carrier does write [S8] — would be a different
*regulatory* object and is out of scope. The dates and the rate machinery are in
Regulatory context below.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Non-participating (無配当) 外貨建終身保険 with an account value (積立金) credited at a declared 積立利率 over a guaranteed floor; not unit-linked | [S1] [S2] [S3] [S4]; default **[std]** (1) |
| 契約形態 (model-point parameter) | (i) **LEVEL** — 平準払 積立利率変動型, rate redeclared monthly, no MVA; (ii) **SINGLE** — 一時払 積立利率更改型, rate fixed over an 積立利率適用期間, MVA on surrender inside it | [S1] [S2] vs [S3] [S4] [S8] [S12] [S14]; packaging **[std]** (1) |
| Policy term (保険期間) | 終身 — whole of life. No expiry, no 満期保険金 | [S1] [S2] [S3] [S7] |
| Operating currency (契約通貨) | US dollar (米ドル) only | [S1] [S3] [S5] [S7]; choice **[std]** (2) |
| Regulatory class | 第一分野, 保険業法第3条第4項第1号; **特定保険契約** under 保険業法第300条の2 | [REG-R1] [REG-R37] [S5] [R3] |
| Issue age (契約年齢) | LEVEL 満6歳〜満80歳; SINGLE 0歳〜90歳 | [S1] [S4]; envelope **[std]** (3) |
| Age basis | Attained age (*man-nenrei*, 満年齢) with the fractional year discarded at 契約日, incrementing on the 年単位の契約応当日 | inherited, [whole life product specification (終身保険)](../whole_life/product-spec.md) |
| 最低保険金額 / minimum premium | LEVEL 3万米ドル of 基本保険金額; SINGLE US$30,000 of single premium | [S1]; SINGLE minimum **[std]** (4) |
| 保険料払込期間 | LEVEL: 歳満了 short-pay (e.g. 60歳払込満了) or 終身払; SINGLE: 一時払 | [S1] [S2] [S3] |
| Sex | Male and female rated separately | [S2] |
| Lives basis | Single life; no joint-life form in the retrieved set | [S1] [S2] [S3] [S7] |
| **Anchor model cell** | Male, 契約年齢 40, LEVEL shape, 米ドル建, 基本保険金額 **US$100,000**, 保険期間 終身, 保険料払込期間 **60歳払込満了** (240 monthly premiums), 月払保険料 **US$239.60**, 低解約返戻金特則 **off**, 積立利率 at the guaranteed floor of **3.00%**, 契約日 TTM **US$1 = ¥159.43** | [S2]; FX level [S11]; scenario **[std]** (5) |

Footnotes to [std] rows:

1. The three market shapes are set out above. The composite carries **two** of them as one
   chassis with a model-point flag, following the packaging of the one carrier that writes
   several shapes on a single 通貨指定型 chassis [S12], because the two shapes share the whole
   account-value recursion and differ only in the premium stream, the rate-reset cycle and
   the presence of the MVA — which is exactly what a model-point parameter is for. The third
   shape, a level **yen** premium converted to USD monthly [S5] [S6], is excluded: its
   premium is fixed in the *policyholder's* currency, so it inverts the currency exposure on
   the premium leg, and it carries neither MVA nor APL nor 復活 [S5]. It is named here because
   a reader meeting it in the market should know it is a different cash-flow object, not a
   variant. Participation: 無配当 at every retrieved carrier on these two shapes [S1] [S2] [S3]
   [S7], with one 5年ごと配当付 design on the excluded third shape [S5].
2. 米ドル建 and 豪ドル建 are offered by every carrier that writes more than one currency [S3] [S12]
   [S14]; ユーロ建 appears at one [S8]; one 通貨指定型 chassis offers 円 as a third "currency" with
   its own guarantee periods and its own MVA rate [S12]. USD is taken because it is the only
   currency every retrieved carrier writes, because the two published run-off tables the
   composite is built on are USD tables [S3], and because **only USD and AUD are inside the
   標準責任準備金 regime** — every other foreign currency is excluded from the 対象契約 [R1] [REG-R12].
   AUD is a parameter change (a different index and a shorter guarantee period [S3]), not a
   different product; EUR would be a different *regulatory* product.
3. LEVEL: 満6歳〜満80歳 at the one carrier publishing a level-premium envelope [S1]. SINGLE:
   0歳〜90歳 [S4], against 0歳〜87歳 [S8] and an implied 40歳〜90歳 from the charge bands at a third
   [S10]. The composite adopts each shape's published envelope verbatim rather than
   intersecting them, because the two shapes are sold to different buyers — a 6-year-old is
   an insurable life on a savings contract, a 90-year-old is not, and the single-premium
   envelope reaching 90 is the inheritance-planning use case.
4. **No retrieved document publishes a minimum single premium**, for any carrier or any
   shape. US$30,000 is carried across from the published LEVEL 最低保険金額 [S1] on the ground
   that the SINGLE shape sets 基本保険金額 = 一時払保険料 at issue [S3], so the two minima are the
   same quantity. This is a modelling floor, not a market fact, and no result depends on it.
5. The anchor is the one model point for which a carrier publishes a **complete
   surrender-value run**, quoted on the main contract (*shu-keiyaku*, 主契約) — 主契約保険金額 is
   the sum assured on it, before any rider (*tokuyaku*, 特約): 米ドル建, male, 契約年齢40歳,
   主契約保険金額 100,000米ドル, 月払, 口座振替, 60歳払込満了, 保険期間終身, with 解約返戻金 at durations
   3 / 5 / 7 / 10 / 15 / 20 / 30 / 40 / 50 on three crediting scenarios,
   3.00% / 3.50% / 4.00% [S2]. On the guaranteed 3.00% column the
   published values are US$5,557 / 10,822 / 16,332 / 25,082 / 40,128 / 57,329 / 69,516 /
   81,350 / 90,715, against cumulative premiums of US$8,626 / 14,376 / 20,127 / 28,752 /
   43,128 / 57,504 [S2]. The cell is internally consistent and the consistency was
   recomputed, not assumed: 239.60 × 36 = 8,625.60, published as 8,626 (the booklet rounds
   the cumulative premium **up** to the whole dollar); × 60 = 14,376; × 84 = 20,126.40 →
   20,127; × 120 = 28,752; × 180 = 43,128; × 240 = 57,504 — every published figure
   reproduces exactly. The base run holds the crediting rate at the **floor**, which is the
   guaranteed column and the only column that is a contract term rather than an
   illustration; the 3.50% and 4.00% columns are scenarios, and keeping them separate is not
   tidiness but the requirement that a guaranteed element be presented separately from a
   non-guaranteed one [REG-R38] [R8]. The floor also makes two mechanics vanish identically
   in the base run — the 増加死亡保険金額 uplift and the 特別積立金 top-up, both of which are differences
   against a 予定利率 basis equal to the floor (see Contractual mechanics), which is why the
   published 3.00% column shows 特別積立金 of (0) at both 10 and 20 years [S2]. The FX level US$1
   = ¥159.43 is the reference TTM published for 2026-08-19 [S11] and is held flat in the
   base run **[std]**: this library models contractual cash flows, not an FX view, and a
   projected currency path would be an economic assumption dressed as a product feature.

### Premiums and the currency layer

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis, LEVEL | Level in **US dollars**, guaranteed for 保険料払込期間; 月払 by 口座振替 or credit card | [S1] [S2] |
| Premium basis, SINGLE | One 一時払保険料 in US dollars at 契約日; 基本保険金額 at issue = the single premium | [S3] |
| Yen-payment rider (円入金特約) | Attached; each yen premium is converted at the 入金用為替レート. Mandatory at one carrier, optional elsewhere | [S1] [S3] [S7]; attachment **[std]** (6) |
| Yen-benefit rider (円支払特約) | Attached; benefits, surrender value and annuity payments are converted at the 支払用為替レート | [S1] [S3] [S7] |
| 入金用為替レート | TTM **＋50銭** per US$1 (¥0.50) | observed range 0–50銭 [S1] [S3] [S5] [S11]; pick **[std]** (7) |
| 支払用為替レート | TTM **−50銭** per US$1 (¥0.50), floored at TTB | observed range 0–50銭 [S1] [S3] [S5] [S8] [S11]; pick **[std]** (7) |
| Reference rate | A nominated bank's TTM (対顧客電信仲値); where it changes more than once in a day the **first** quote of the day applies; 入金 capped at TTS, 支払 floored at TTB | [S1] [S3] [S5] [S7] |
| Reference TTM level | US$1 = ¥159.43, held flat | [S11]; flat path **[std]** (5) |
| Conversion base date | The **day before** the day the completed claim documents reach the insurer, for death, disability, surrender and policy-loan payments; the preceding business day where that day is a bank holiday | [S7] |
| Advance payment (前納) | Available at issue only; out of scope | [S2]; scope **[std]** (8) |
| Premium waiver (保険料払込免除) | On a listed 身体障害の状態 arising within 180 days of an 不慮の事故; the surrender value then progresses as if premiums were still paid. Out of scope | [S1] [S2]; scope **[std]** (8) |

6. 円入金特約 is *mandatory* at one carrier — 「この保険には円入金特約が付加されています」 — while 円支払特約 is
   optional there [S7]; both are elective at the others [S1] [S3]. The composite attaches
   both, because the yen-in / yen-out path is the one every retail buyer actually takes and
   because a model that receives premiums in USD hides the entire currency layer. A policy
   settling in USD throughout is a parameter position (both riders off), and the difference
   is exactly two conversion spreads.
7. The observed inbound spread is TTM＋50銭 at two carriers [S1] [S3], TTM＋25銭 at a third
   [S5], an unpublished 当社所定 rate at a fourth [S7] and **nil** on the 外国為替連動型 shape, which
   never converts at all [S11]. Outbound: TTM−50銭 [S1] [S8], TTM−25銭 [S5], 当社所定 floored at
   TTB [S7], and a printed TTM−1銭 (USD) / TTM−3銭 (AUD) at one carrier [S3] — the last is
   reported verbatim in the research file but a 1-sen outbound spread against a 50-sen
   inbound spread is fifty times outside every other published value, so it is treated as
   [unverified] and is **not** used as the basis of the composite. The composite takes the
   symmetric ±50銭: it is the modal published value, it is the widest, and the widest spread
   is the one that makes the mechanic visible. At the reference TTM this is 0.31% each way
   and **0.63% on a round trip** — the reason every carrier warns that a loss can arise with
   no exchange-rate movement at all.
8. 前納 [S2] and 保険料払込免除 [S1] [S2] change the premium stream without touching any of the
   three layers this document exists to specify, and 前納 additionally needs an unpublished
   discount rate. Both are specified and excluded, as they are on the chassis.

### Crediting rate and the account value

| Parameter | Representative value | Basis |
|---|---|---|
| 積立利率 declaration, LEVEL | Declared on the **1st of each month**; applied to the 積立金 from each monthly policy anniversary (**月単位の契約応当日**), not from the calendar month end | [S1] [S2]; timing per 約款第3条第2項 [S2] |
| 積立利率 declaration, SINGLE | Declared **twice a month** for new business (contracts dated 1st–15th and 16th–month-end) and then **fixed for the whole 積立利率適用期間** | [S3] [S4] [S14] |
| 積立利率適用期間 (SINGLE) | **15 years** | observed 1/3/10/15/20/30 [S3] [S8] [S12] [S14]; pick **[std]** (9) |
| Floor (最低保証積立利率), LEVEL | **年3.00%**, equal to the contract's own 予定利率, fixed at issue; the declared rate can never fall below it | [S1] [S2] |
| Floor (最低保証積立利率), SINGLE | **年0.01%** | [S3] |
| Base crediting scenario | LEVEL: the floor, 3.00%. SINGLE: **4.72%**, the rate declared for the 2026-08-16 window | [S2] [S4]; scenario **[std]** (10) |
| Crediting scenario range | LEVEL 3.00% / 3.50% / 4.00% (the published illustration set); SINGLE 4.45%–5.29% (a fortnightly 基準利率 series over twenty consecutive windows) | [S2] [S14] |
| Rate-setting mechanic | The declared rate is the earned rate on the backing asset pool **net of** the 資産運用のための運営費率, the 積立金を最低保証するための保証費率 and その他費用; on the SINGLE shape it is an index-linked rate inside a ±1.5% band, less 災害死亡保障費率 + 新契約費率 + 維持費率, capped at (米国債利回り平均 + 2.0%) less the same charges and floored at 0.01% | [S1] [S2] [S3] |
| Rate index (SINGLE) | An A-rated USD corporate bond index at 20 years below age 80 and at 10 years from 80 to under 91; the insurer may change the index on two months' notice with 主務官庁 approval | [S3] |
| 実質的な利回り disclosure | Must be shown alongside the 積立利率 on a 外貨建一時払 design, measured at the point where the MVA, the rate-variation period and the surrender charge have **all** expired | [R8] [S4] |
| Crediting frequency in the model | Monthly, at the 月単位の契約応当日; annual rate converted as (1 + i)^(1/12) − 1 | [S2]; convention **[std]** (11) |

9. Observed 積立利率適用期間 / 積立利率保証期間: 20 years below age 80, 15 from 80 to under 91 and 1 year
   from 91 at one carrier [S3]; 10 years, dropping to 3 from age 81, at a second [S8]; 30 or
   10 (USD) at a third [S12]; 10 or 15 at a fourth [S14]. Fifteen years is taken because it
   is the **only period for which a complete MVA rate table is published** [S3], and the
   composite's MVA is anchored on that table; choosing any other period would leave the
   surrender layer with no published artefact behind it. The age-banded shortening is
   specified but not modelled — the anchor cell never reaches the band.
10. The floor is a contract term on the LEVEL shape and therefore the honest base run: it is
    the guaranteed column of the published table [S2] and it is what the 約款 promises [S2].
    Any higher rate is an illustration. On the SINGLE shape there is no comparable
    guaranteed column — a 0.01% floor is a floor in name only — so the base run uses a
    **declared** rate actually observed in the market, 4.72% for the 2026-08-16 window [S4],
    with the twenty-window 基準利率 series [S14] as the scenario range. The declared-rate
    *history* for the LEVEL shape could not be retrieved at all: the carrier's rate page is
    a JavaScript application shell with no rate content in the served HTML [S16], so the
    floor and the three illustration rates in [S1] [S2] are the only crediting figures that
    exist for that shape.
11. The 約款 credits at the 月単位の契約応当日 [S2] while the 重要事項説明書 of the same booklet says the
    rate is set 毎月1日 [S2]. Both statements are in one document and they are not the same
    date; the 約款 governs, and the difference is a within-month offset that
    `technical-notes.md` carries explicitly rather than resolving silently. The monthly rate
    is the geometric twelfth root of the annual rate **[std]**; a nominal-over-12 convention
    is a permissible variant and the difference at these rates is immaterial, but the choice
    must be stated because the published surrender-value run is reproduced to the dollar.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| 死亡保険金, LEVEL | **基本保険金額 + 増加死亡保険金額** — the sum assured fixed at issue plus a ratcheting uplift computed at each 月単位の契約応当日 as the excess of the actual account value over the account value needed to fund the sum assured at the 予定利率 | [S1] [S2]; ratchet [unverified] (12) |
| 死亡保険金, SINGLE | **max(積立金相当額, 解約返戻金額)** at the date of death — no sum assured above the fund | [S3] |
| 高度障害保険金 | Same amount as the death benefit; payment extinguishes the contract | [S2]; inherited |
| 増加死亡保険金額 in the base run | **Identically zero**, because the base crediting rate equals the 予定利率 that defines the uplift | [S1] [S2] (5) |
| Experience top-up (特別積立金) | An amount computed from the ten-year investment performance is added to the 積立金 after **10** and after **20** years in force; never paid to a contract terminating earlier; **zero if the rate has run at the floor** | [S1] [S2] |
| 災害死亡保険金 | Paid **in addition** on accidental or infectious-disease death at one carrier on the SINGLE shape; out of scope | [S3]; scope **[std]** (13) |
| Currency of benefit | The operating currency; converted to yen at the 支払用為替レート where 円支払特約 is attached | [S1] [S3] [S7] |
| 免責 — suicide | No benefit where the insured commits suicide within **3 years** of the 責任開始期, reset on 復活 | [S2] [S7]; statutory frame [REG-R34]; window **[std]** (14) |
| Payment when a benefit is refused | The 積立金 or 解約返戻金 is still paid — a real cash flow on an account-value product, and one a pure protection model has no analogue for | [S2] |
| Contestability (告知義務違反) | Rescission within **2 years** of the 責任開始日 (or 復活日); fraud voids without time limit | [S3] [S7]; statutory ceiling [REG-R35] |

12. The uplift formula is verified from 約款第46条: the 増加死亡保険金額 is (i) the account value at
    the previous day's close on the actually-applied 積立利率, assuming all premiums due were
    paid, less (ii) the account value needed at the same moment to fund the then sum assured
    with no future premiums at the 予定利率 (年3.00%); it is not computed at all where the
    difference is non-positive; reducing the sum assured reduces the 積立金 and the
    増加死亡保険金額 in the same proportion, and the uplift cannot be reduced on its own [S2]. The
    **ratchet** — that the uplift cannot fall below the previous month's value — appears in
    the ご契約のしおり section of the same booklet but not in the extracted 約款第46条 text, so the
    ratchet specifically is **[unverified]** and is flagged as a re-check item rather than
    asserted as a contract term. The composite models the ratchet, because the alternative
    (a monthly high-water reset) is the more conservative reading of a booklet the insurer
    published, and `technical-notes.md` carries the switch.
13. Present at one carrier on the SINGLE shape only [S3] and absent at the others [S2]. An
    additional accidental-death layer is a separate decrement with its own incidence basis
    and no published rate anywhere in the set; it is specified and excluded.
14. 3 years at two carriers [S2] [S7] against 2 years at a third [S3]. The composite takes 3
    years, which is both the majority here and the chassis value (the
    [whole life product specification (終身保険)](../whole_life/product-spec.md)). The window is
    contractual, not statutory: 保険法第51条
    excludes suicide with **no time limit at all**, and a 3-year 免責期間 is a narrowing of the
    statute in the insurer's favour of the policyholder [REG-R34].

### Options and riders

| Parameter | Representative value | Basis |
|---|---|---|
| Target-value conversion (目標到達時円建終身保険移行特約) | Optional on the SINGLE shape. A 目標値 set by the policyholder; when the **yen-converted 解約返戻金** reaches the 目標額 the contract converts automatically to a yen whole life and both the death benefit and the surrender value are fixed in yen; neither FX nor MVA applies thereafter, and no 解約控除 is charged after conversion | [S8] [S9] [R6]; name [unverified] (15) |
| 目標値 | **110%** of the yen-converted single premium | observed 100–200% [S8] [S9] [R6]; pick **[std]** (16) |
| Target test | Every business day, from **one year** after 契約日; conversion inside the first year does not trigger; the target may be changed any number of times before it is reached, free of charge | [S9] [R5] |
| 低解約返戻金特則 | Optional on the LEVEL shape; 低解約返戻金割合 **70% / 77.5% / 85% / 92.5%** by 残余保険料払込年数 (≥4 / 3 / 2 / 1 years), applied to the ordinary surrender value over a period identical to 保険料払込期間 | [S2]; adoption **[std]** (17) |
| Premium saved by the 特則 | 225.00 against 239.60 US$/month on the anchor cell — the suppressed form costs **93.9%** of the ordinary one, a 6.1% reduction | [S2] |
| Periodic withdrawal (積立金定期引出特約) | Takes a periodic withdrawal from the account value, funded by **lowering the 積立利率**; the withdrawals themselves carry neither 解約控除 nor MVA. Out of scope | [S3] [S4]; scope **[std]** (18) |
| 年金支払移行特約 | Converts the death benefit or surrender value into an annuity, with a management charge of **1.00% of each payment**. Out of scope | [S1] [S8] [S10]; scope **[std]** (18) |
| リビング・ニーズ特約 | Attached at no extra premium; inherited | [S1]; [whole life product specification (終身保険)](../whole_life/product-spec.md) |
| APL (自動振替貸付) | Present on the LEVEL shape, inherited unchanged; **structurally absent on the SINGLE shape**, which has no premium to advance | [S2] [S7]; inherited |
| 契約者貸付, 払済保険, 減額, 復活 | Inherited; 復活 within **3 years** of lapse | [S7]; window **[std]** (19) |

15. **The rider name is [unverified].** The two retrieved carriers call theirs 円建終身移行特約 [S8]
    and 目標値到達時終身保険移行特約 [S9]; the name 目標到達時円建終身保険移行特約 is attributed in search results to a
    carrier whose entire site returns HTTP 403 to every fetcher tried [S15], so no retrieved
    document carries it. The *mechanic* is fully verified from [S8] [S9] and from the FSA's
    own definition of the class [R6]; only the name is not. The composite uses the name the
    brief names, flags it here, and cites the two verified names beside it.
16. Observed 目標値 menus: **105% to 200% in 1% steps** [S8]; **100% / 105% / 110%** chosen at
    issue [S9]; the FSA describes the class as "105%, or 110–200% in 10% steps" [R6]. 110%
    is taken because it is the only value inside all three menus, and because it is a target
    a 2.5-year average holding period can actually reach [R6] — a 200% target on a 4.72%
    credit is a twenty-year proposition and would never be exercised in a base run. The
    target is measured against the **yen-converted premium paid**, so a weaker yen alone can
    trigger it [S8] [R5].
17. Observed suppression scales on FX designs: the four-step 70 / 77.5 / 85 / 92.5% ramp by
    残余保険料払込年数 [S2]; a flat **7割** throughout the 低解約払戻期間 [S7]; and 70% below 10 years,
    graded from 10 to under 15 and 100% from 15 on the excluded yen-premium shape [S5]. The
    composite takes the four-step ramp — it is the scale of the anchor carrier, it is the
    only one published as an explicit schedule, and it differs from the chassis's flat 0.70
    (the [whole life product specification (終身保険)](../whole_life/product-spec.md)), which is exactly
    the kind of delta a derived product should carry rather than inherit. It is **off** in
    the anchor cell so that the crediting and currency layers can be read without the
    cliff on top of them; a dedicated model
    point turns it on. The "unpaid premium keeps you suppressed" clawback is inherited [S2].
18. Both are real options with published mechanics, and both change the *shape* of the
    liability rather than any of the three layers: the withdrawal rider converts the
    contract into an income product priced through the crediting rate [S3], and the annuity
    rider hands the run-off to the payout chassis in
    [individual annuity (個人年金保険)](../individual_annuity/product-spec.md). Excluded and
    named.
19. 復活 within **3 years** at one carrier [S7], within **1 year** at another [S2], and **not
    at all** on the excluded yen-premium shape [S5]. The composite keeps the chassis's
    3-year window rather than adopting the anchor carrier's 1 year, because a derived
    product should not move an inherited behavioural parameter without a reason the sources
    supply, and here they disagree.

### Termination, surrender values and the charge stack

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender value (解約返戻金) | `積立金 × (1 − 市場価格調整率 − 解約控除率)`, then multiplied by the 低解約返戻金割合 where the 特則 is in force | [S3]; suppression [S2] |
| Surrender charge (解約控除率) | **7.0%** in the first policy year, falling **0.7 percentage points per completed policy year** to zero at ten years, constant within each year, applied to the **積立金** | [S3]; adoption **[std]** (20) |
| 解約控除 window | Ten years from 契約日 — which on the anchor cell is also the shorter of the premium-paying period and ten years | [S1] [S2] [S3] [S7] [S8] |
| MVA (市場価格調整) | **SINGLE shape only.** Applied on surrender or 減額 inside an 積立利率適用期間; **not** applied on an 積立利率計算基準日 nor inside a one-year 積立利率適用期間 | [S3]; absent on LEVEL [S2] |
| MVA direction and size | Positive (reducing the surrender value) when the 基準利率 applicable at surrender exceeds the rate the contract's 積立利率 was set under; the published table for a 15-year period runs from +0.1795 at year 1 / Δ +2.0% to +0.0140 at year 14, decaying about **0.0126 per remaining year**, with the zero column at Δ = −0.1% | [S3]; reconstruction **[std]** (21) |
| Initial charge (契約初期費用), SINGLE | **4.50%** of the single premium at issue ages 40–69 (3.00% at 70–79, 2.00% at 80–90) | [S10] |
| 契約初期費用, LEVEL | A percentage of each premium received, at a higher rate over an initial period and a lower rate thereafter | [S1] [S2] establish only that a 締結・維持 cost is taken from the premium; the two-rate shape, its breakpoint and its levels are all **[std]** (22) |
| 保険関係費用 — 保障部分 | A monthly cost-of-insurance charge on the net amount at risk (死亡保険金 − 積立金), on 生保標準生命表2018（死亡保険用）rates | [S1] [S2] structure; basis **[std]** (22) |
| 保険関係費用 — 維持部分 | A flat annual percentage of the 積立金, deducted monthly | [S1] [S2] structure; level **[std]** (22) |
| Currency spread (為替手数料) | ±50銭 per US$1 on each conversion; 0.63% on a round trip at the reference TTM | [S1] [S3]; pick **[std]** (7) |
| 猶予期間, 失効, 自動振替貸付 | Inherited; 月払 grace runs from the first day of the month following the 払込期月 to the last day of that month | [S2] [S7]; [whole life product specification (終身保険)](../whole_life/product-spec.md) |
| 満期保険金, 契約者配当 | None on the 無配当 composite | [S2] |
| Policyholder protection | 90% of the 責任準備金等 at the failure date, with **no carve-out for 外貨建 contracts** | [R10] [REG-R40] [REG-R41] |
| クーリング・オフ | Eight days on a dispatch rule; out of scope | [REG-R36]; scope **[std]** (23) |

20. Observed 解約控除 scales: **7.0% → 0.7% straight-line over ten years on the 積立金**, identical
    for USD and AUD, constant within each policy year [S3]; **10% → 0%** and **5% → 0%** in
    two vintages at a second carrier [S8]; **6.5% → 0.0%** on the FX version and 3.5% → 0.1%
    on the yen version at a third — but applied to the **基本保険金額**, not to the fund [S13];
    and `20% × (1 − 経過月数 ÷ 120)` applied *after* a 70% low-surrender factor on the excluded
    yen-premium shape [S5]. Two carriers decline to publish any scale at all
    (「経過期間などにより異なるため、一律には記載できません」) [S2] [S7]. The composite takes the first, because it is
    the only complete published scale whose **base is the account value** — a 6.5% charge on
    the sum assured is not a 6.5% charge on the fund, and mixing the bases would be the
    single easiest way to get this product wrong by a factor of several. What does *not*
    vary is the endpoint: every published scale reaches zero at exactly ten years.
21. **No carrier publishes a closed-form MVA**, and the disclosure regime does not ask for
    one: the 監督指針 requires the mechanism, the loss warning and an illustration of
    「解約時の保険料積立金に対して控除される割合」 [R3] — which is precisely what a rate table is. The composite
    therefore adopts the **published table itself** as the reference artefact [S3] and
    specifies its algebraic reconstruction as a **[std]** in `technical-notes.md`, fitted to
    the table and reported with its fit. Two facts pin the reconstruction: the zero column
    sits at a rate move of −0.1%, which fixes the spread between the surrender-date
    reference rate and the contract's own at 0.1%; and the magnitude decays close to
    linearly in remaining term [S3]. A separate carrier publishes the 市場価格調整用利率 itself,
    fortnightly, by currency and guarantee period — USD 5.50% (30y) / 4.95% (10y) for the
    2026-08-16 window — and states that the same rate both sets the 積立利率 and computes the
    MVA [S12], which is the level check on any reconstruction. The MVA is **not a charge**:
    it is symmetric, it can be negative, and a fall in rates increases the surrender value
    [S3] [R8]. A model that implements it as a deduction is modelling a different product.
22. **Every carrier in the set refuses to quantify the mortality-and-expense charge**, in
    identical words: 「契約年齢・性別・経過期間などにより異なるため一律には記載できません」 [S2] [S7]. The layers themselves
    are published and are what the composite implements — a 締結・維持 cost deducted from the
    premium or the account value, a 死亡・高度障害保障 cost deducted from the account value, and a
    third block of asset-management, guarantee and other costs taken **inside** the
    crediting-rate calculation [S1] [S2]. The composite's charge *rates* are therefore
    **back-solved from the published surrender-value run at the anchor cell** [S2] rather
    than invented: the run is public at nine durations on three crediting scenarios, the
    crediting rate is a contract term at the floor, and the surrender charge is fixed by
    footnote 20, so the charge stack is the residual. `technical-notes.md` reports the
    fitted rates and the fit. Four independent order-of-magnitude checks bound the answer:
    the published front-end scale of 4.50% / 3.00% / 2.00% of a single premium by age band
    [S10]; the distributor's 契約時手数料 of 4.00% or 2.60% with a 継続手数料 of up to 0.75% p.a. for
    at most seven years [S13]; the FSA's L-shaped 5.5% / 0.1% reading of the sector [R5];
    and the 2.35% p.a. 保険契約関係費 published on a variable sleeve [S13], which is an upper bound
    because a variable sleeve carries fund cost the fixed account does not. On one
    single-premium contract the 実質的な利回り equals the declared 積立利率 exactly (4.72% = 4.72%)
    [S4], which bounds the charge taken *outside* the rate at zero for that design — the
    charge is entirely inside the crediting spread there, and the composite's split between
    "inside the rate" and "deducted from the fund" is itself a **[std]** presentation
    choice. The mortality basis for the cost-of-insurance layer is 生保標準生命表2018（死亡保険用）
    [REG-R18] with no further loading, on the ground that it is already a valuation table
    carrying an explicit margin sized to a 2σ level [REG-R20]; the library ships it as a
    **[std]** construction whose provenance column points at the IAJ entry rather than as a
    copy, because redistribution is restricted [REG-R21].
23. The statutory cooling-off applies in full to this contract [REG-R36], and on a product
    with a 60%-in-four-years surrender rate an eight-day window is a live early decrement.
    `jplib` projects from the point cover is in force and scopes it out, stated rather than
    silently omitted.

---

## Contractual mechanics

Notation used below and carried into `technical-notes.md`. The grid is **monthly**: `k`
counts completed policy months from 契約日.

    x        契約年齢 at issue (満年齢, fractional year discarded)
    k        completed policy months since 契約日; the crediting step
    SA       基本保険金額, in the operating currency
    P(k)     premium due at month k, in the operating currency (zero after 払込満了;
             on the SINGLE shape, P(0) = the single premium and P(k) = 0 for k > 0)
    AV(k)    積立金 — the account value at month k
    AV0(k)   the account value the same contract would hold on the 予定利率 basis
    IDB(k)   増加死亡保険金額 — the death-benefit uplift
    ic(k)    the declared 積立利率 applying over month k (annual, effective)
    i0       the 予定利率 — the guaranteed floor on the LEVEL shape (3.00%)
    sc(k)    解約控除率 — the surrender charge rate at month k
    mva(k)   市場価格調整率 — the MVA rate at month k (SINGLE shape; can be negative)
    kl(k)    低解約返戻金割合 — the suppression factor (1.00 unless the 特則 is in force)
    CV(k)    解約返戻金 — the surrender value payable at month k
    e(k)     the reference TTM at month k, yen per unit of operating currency
    s        the 為替手数料 spread, ¥0.50 per US$1

### The currency layer

Every cash flow crosses the currency boundary twice, and each crossing is a spread, not a
rate. A yen premium buys operating currency at `e(k) + s`; a payment out of the contract is
converted at `e(k) − s`:

    premium_JPY(k)  = P(k) × (e(k) + s)          [円入金特約]
    payment_JPY(k)  = amount_FX(k) × (e(k) − s)  [円支払特約, floored at TTB]

`e(k)` is a nominated bank's TTM, and where the published value moves more than once in a
day the **first** quote of that day applies [S1] [S3] [S5]. The inbound rate is capped at
TTS and the outbound rate floored at TTB, so the spread is a contractual maximum rather than
a free parameter [S3] [S5] [S7]. Conversion happens on a published base date, not on the
payment date: for death, disability, surrender and policy-loan payments it is the **day
before** the day the completed documents reach the insurer, rolled back to the preceding
business day where that is a bank holiday [S7].

Three consequences the model must carry. First, **the round trip costs 0.63% at the
reference TTM before anything else happens** — which is why every carrier warns that a loss
can arise with no exchange-rate movement at all, and why the ratio of yen out to yen in is
not the ratio of the account values. Second, the FX rate enters the *decision* mechanics,
not only the reporting: the target-value test is made on the yen-converted surrender value
(below), so a weaker yen can trigger a conversion the crediting rate alone would not have
earned [S8] [S9] [R5]. Third, receiving in operating currency instead is not free either —
送金手数料, 引出手数料 and リフティングチャージ apply and belong to the receiving bank, not to the insurer, so
they are outside the contract and outside this model [S1] [S7] [S13].

### The crediting layer

On the **LEVEL** shape the rate is redeclared monthly. The published wording of the two
documents differs and the difference is a real modelling fork: the 重要事項説明書 says the rate is
set 毎月1日, the 約款 says 「積立利率は、契約後、月単位の契約応当日ごとに更改を行ないます」 [S2]. The 約款 governs — the rate is
*declared* on the 1st and *applied* from the monthly policy anniversary — so a model that
credits on calendar month ends is off by the anniversary offset for the life of the
contract. The rate is the earned rate on this product's segregated asset pool for the
previous-but-one month, net of the asset-management, guarantee and other charge rates [S1]
[S2], and 約款第3条第3項 floors it at the contract's own 予定利率: 「積立利率は、この保険契約の 予定利率…を下回ることはありません」
[S2]. That floor is fixed at issue and is not a rate the insurer redeclares — which is why
it is 3.00% on a 2002-generation contract and 0.01% on a single-premium contract written in
2023 [S1] [S2] [S3]. The insurer notifies the policyholder annually of the current rate and
of the past twelve monthly rates [S2].

On the **SINGLE** shape the rate is set at 契約日 and at each 積立利率計算基準日 and is unchanged
through the whole 積立利率適用期間 [S3] [S4]. It is an index rate the insurer may set within ±1.5%
of a 基準利率, less 災害死亡保障費率 + 新契約費率 + 維持費率, capped at (the average US Treasury yield + 2.0%)
less the same three charge rates, and floored at 0.01% [S3]. The 基準利率 itself is an average
of the index over five days before a fixed date in the month before last (for contracts
dated 1st–15th) or before the 11th of the current month (for contracts dated 16th–month-end)
[S3] — a publication lag a scenario generator has to respect. The index is an A-rated USD
corporate bond index at 20 years below age 80 and at 10 years from 80 [S3].

The account value recursion is one line and is the same on both shapes:

    AV(k+1) = [ AV(k) + P(k) − C_init(k) − C_maint(k) − C_coi(k) ] × (1 + ic(k))^(1/12)

with the processing order — premium in, charges out, interest credited — fixed in
`technical-notes.md`, because the order changes the answer at the third decimal and the
published run is reproduced to the dollar. `C_coi(k)` is the cost of insurance on the net
amount at risk, `SA + IDB(k) − AV(k)` on the LEVEL shape and zero on the SINGLE shape, where
the death benefit never exceeds the fund.

### The death benefit and the two mechanics that vanish at the floor

On the LEVEL shape the death benefit is `SA + IDB(k)`, and the uplift is defined against the
予定利率 basis [S2]:

    IDB(k) = max( IDB(k−1), AV(k) − AV0(k) )     computed at each 月単位の契約応当日
    AV0(k) = the account value required at k to fund SA with no future premiums at i0

The uplift is not computed at all where `AV(k) − AV0(k) ≤ 0`, it exists only on the main
contract and never on a 特約, and reducing the sum assured reduces the 積立金 and the uplift in
the same proportion — the uplift cannot be reduced on its own [S1] [S2]. The `max` against
the previous month is the **ratchet**, which is sourced to the ご契約のしおり and not to the
extracted 約款 text, and is therefore [unverified] (footnote 12).

The base run makes both discretionary mechanics disappear, and this is a structural fact
rather than a modelling convenience. Because the base crediting rate **is** the 予定利率 that
defines `AV0`, `AV(k) = AV0(k)` identically and `IDB(k) = 0` for every `k`. The same
argument applies to the **特別積立金**: it is computed from ten-year investment performance, so a
contract whose rate ran at exactly the floor earns nothing — and the published table
confirms it, showing 特別積立金 of (0) in the 3.00% column at both 10 and 20 years against 147 /
527 at 3.50% and 302 / 1,120 at 4.00% [S2]. A model that produces a non-zero uplift or
top-up on the guaranteed run has a bug, and both are tests.

On the SINGLE shape there is no sum assured above the fund: the benefit is
`max(積立金相当額, 解約返戻金額)` at the date of death, and the 基本保険金額 at issue is simply set
equal to the 一時払保険料 [S3]. The `max` matters — where the MVA is strongly negative the
surrender value can exceed the account value, and the death benefit follows the higher.

### The surrender layer

The payable surrender value is the published formula [S3], with the chassis's suppression
factor applied on top where the 特則 is in force [S2]:

    CV(k) = AV(k) × (1 − mva(k) − sc(k)) × kl(k)

`sc(k)` is 7.0% in the first policy year and falls 0.7 percentage points at each policy
anniversary to zero at ten years, constant within the year [S3]. It is a **charge**: it is
one-sided, it never adds value, and it is disclosed under the 説明義務's restriction-on-
cancellation limb [REG-R39].

`mva(k)` is **not** a charge. It is a symmetric, interest-rate-linked adjustment: positive
(reducing the value) when rates have risen since the contract's rate was set, negative
(**increasing** it) when they have fallen [S3] [R8]. It applies only on the SINGLE shape,
only inside an 積立利率適用期間, and **not at all** on an 積立利率計算基準日 or inside a one-year period
— so a contract surrendered exactly at a reset date crosses the boundary with no adjustment,
a discontinuity a monthly model must place correctly [S3]. The published table for a 15-year
period is the reference artefact: at Δ = +2.0% the rate runs from 0.1795 in year 1 to 0.0140
in year 14 and is undefined in year 15, because year 15 *is* the reset date [S3]. The
industry's 適正表示ガイドライン sets that symmetry as the standard risk wording every illustration
of an MVA product must carry, and requires the no-move case to be printed beside any
illustration of a market move [R8].

Where the 特則 is in force, `kl(k)` is 70% while four or more premium-paying years remain and
steps to 77.5%, 85% and 92.5% at three, two and one remaining years, reaching 1.00 at 払込満了
[S2]. The remaining-years count is measured from the monthly policy anniversary of the
**last premium paid** and rounded **up** to whole years, so a contract carried by unpaid
premiums stays suppressed past the nominal date [S2] — the clawback the chassis specifies.
The step is a cliff, and the published run shows it: with the 特則, US$27,706 at duration 15
against US$53,029 at duration 20 [S2].

A 減額 is a partial surrender and carries both the MVA and the surrender charge on the reduced
portion; withdrawals under the 積立金定期引出特約 carry **neither**, because their cost is charged
by lowering the crediting rate instead — the 実質的な利回り on that variant is 3.32% against a
declared 積立利率 of 4.62% [S3] [S4].

### The target-value conversion

The rider is the reason this product has a lapse profile unlike any other in the library.
Its mechanics, composited from the two carriers that publish them [S8] [S9]:

    convert at month k  if  k >= 12  and  CV(k) × (e(k) − s)  >=  g × premium_JPY(0)

with `g` = 目標値 = 110% **[std]**. On a hit the insurer notifies within five business days and
the contract converts automatically to a **yen** whole life; the death benefit and the
surrender value are then fixed in yen, and **neither the exchange rate nor the MVA affects
the contract again** [S9]. No 解約控除 is charged after conversion [S8]. The policyholder may
also convert on demand at any time [S8], and may change the target any number of times
before it is reached, free of charge [S9] — which the FSA says the distributor should tell
the customer *before* the target is reached, precisely because raising it is free [R5].

Two features of the trigger are easy to get wrong and both are contractual. First, **the
test is made on the surrender value, not on the account value**, so the FX rate and the MVA
are applied in deciding whether the target has been hit [S9]: the trigger is not a clean
function of the fund, and a model that tests the account value will convert at the wrong
month in every scenario where rates have moved. Second, the **one-year dead zone** is real —
reaching the target inside the first year does not trigger the conversion [S9] — which
interacts with the surrender charge, at 7.0% and 6.3% over exactly that window [S3].

Population behaviour around the trigger is the single most quantified behavioural fact in
this product's source set, and it is not what the contract design implies. At every
focus-monitored distributor, **most ターゲット型 policies are surrendered on reaching the target
and the same product is immediately sold back to the same customer** — the front-loaded
commission charged twice, which the FSA calls economically irrational for the customer [R5]
[R6]. So the modelled event at a target hit is not "the contract continues as a yen whole
life"; it is, in the observed population, a surrender. `technical-notes.md` carries both as
elections and neither as the default.

### Premium payment, grace and lapse — the deltas

Grace, 失効, 自動振替貸付 and 復活 are inherited from the
[whole life product specification (終身保険)](../whole_life/product-spec.md) and are not restated. Three
deltas apply.

**The APL exists only on the LEVEL shape.** A single-premium contract has no premium to
advance, so lapse-from-non-payment is structurally absent on the SINGLE shape: the only
terminations are death, surrender, target conversion and loan-driven termination. Naming
that absence matters, because it means the two shapes have different decrement sets, not
different decrement rates.

**The APL runs against the *suppressed* value where the 特則 is in force**, exactly as on the
chassis, and on this product the interaction has a currency leg too: the advance is made in
the operating currency against a surrender value in the operating currency, while the
premium the policyholder failed to pay was a yen amount. The contract does not lapse because
the yen premium became expensive; it lapses when the account value can no longer carry it.

**復活 is available for 3 years [S7]** on the composite, against 1 year at the anchor carrier
[S2] and no reinstatement at all on the excluded yen-premium shape, where failure to pay
inside the 猶予期間 terminates the contract on the day after grace expiry and pays out the
surrender value [S5]. On reinstatement the 責任開始期 resets, restarting both the suicide and
the contestability clocks [S2] [S7].

---

## Riders and options

**In scope (modelled or parameterized):**

- **円入金特約 / 円支払特約** — modelled, on by default; the conversion spread is a cash-flow item,
  not a reporting convention [S1] [S3] [S7].
- **目標到達時円建終身保険移行特約** — modelled on the SINGLE shape as an election with a 目標値, a
  one-year dead zone and a surrender-value-based test; off in the base run [S8] [S9] [R6].
- **低解約返戻金特則** — a model-point flag with the four-step scale; off in the anchor cell, on
  in a dedicated model point [S2].
- **増加死亡保険金額** — part of the main contract on the LEVEL shape; modelled, with the ratchet
  as a switch because the ratchet itself is [unverified] [S1] [S2].
- **特別積立金** — modelled as a top-up at 10 and 20 years, identically zero in the base run
  because the base run credits at the floor [S1] [S2].
- **自動振替貸付, 契約者貸付, 払済保険, 減額, リビング・ニーズ特約, 高度障害保険金** — inherited unchanged from
  the [whole life product specification (終身保険)](../whole_life/product-spec.md); the APL's absence on
  the SINGLE shape is a product fact, not an omission [S2] [S7].

**Out of scope:** 積立金定期引出特約, whose cost is charged inside the crediting rate [S3] [S4];
年金支払移行特約 / 年金支払特約 and their 1.00%-of-each-payment management charge, which hand the
run-off to [individual annuity (個人年金保険)](../individual_annuity/product-spec.md) [S1] [S8] [S10];
介護年金支払移行特約, converting the surrender value into a care annuity on public 要介護1 or above
[S11]; 災害死亡保険金 as an additional benefit
[S3]; 三大疾病・介護給付終身保険特約, 三大疾病・介護保険料払込免除特約 and 定期保険特約（無解約返戻金型 米ドル建）, whose shape
belongs to [medical (医療保険)](../medical/product-spec.md) and [term life (定期保険)](../term_life/product-spec.md)
[S1]; 保険料払込免除 and 前納 [S1] [S2]; 保険料円入金特約
（クレジットカード払用）as a distinct rider [S1]; and the 変額部分 of the mixed fixed/variable designs,
with their 保険契約関係費 of 2.35% p.a. and 信託報酬 of 0.22% [S13] — a separate-account product, not
this one.

**Scope boundaries at the edge of this product.** Two neighbouring shapes are excluded and
named. The **指定通貨建 yen-premium** design fixes the premium in yen and converts it to USD each
month, resets the 予定利率 every five years after 払込満了 against the average of the 6-month and
5-year US Treasury yields with a 0.25% floor, carries no MVA, no APL and no 復活, and settles
a lapsed contract by paying the surrender value after a 送金待機期間 [S5] [S6]. The **外国為替連動型**
design never converts at all: premium and benefit are both in yen and the currency enters
only as a 為替変動率 multiplier of (FX rate at valuation ÷ FX rate at 契約日), with **no 為替手数料
charged** [S11]. That second design is the cleanest possible demonstration that the currency
spread and the currency exposure are separable — it keeps the exposure and drops the spread
— and it is excluded precisely because this product's spread layer is one of the three
things the document exists to specify.

---

## Variations across insurers

1. **Which shape the carrier sells.** Monthly-declared level premium [S1] [S2]; single
   premium with a multi-year rate lock [S3] [S4] [S8] [S12] [S14]; level yen premium with a
   five-yearly reset [S5] [S6]; fixed 予定利率 with no crediting rate at all [S7]. Composite:
   the first two as one chassis with a model-point flag, the third and fourth named and
   excluded (footnote 1). This is not a stylistic difference — the four shapes have
   different decrement sets.
2. **How often the rate is redeclared.** Monthly, applied from the monthly policy
   anniversary [S2]; twice monthly for new business and then locked for 1, 10, 15, 20 or 30
   years [S3] [S4] [S12] [S14]; monthly for 第1保険期間 then every five years [S5] [S6].
   Composite: monthly on the LEVEL shape and a 15-year lock on the SINGLE shape — a range of
   **one month to thirty years**, and the widest divergence in the file after the floor.
3. **The guaranteed floor.** **0.01%** [S3], **0.25%** [S5] [S6], **3.00%** [S1] [S2]. A
   factor of three hundred, and it is not noise: the 3.00% floor belongs to a
   2002-generation level-premium contract whose floor *is* its 予定利率 and which therefore
   carries a decades-long guarantee, while the 0.01% floor belongs to a contract that resets
   its rate every ten to twenty years and needs no guarantee between resets. Composite: each
   shape keeps its own published floor. A composite that averaged them would describe no
   product that exists.
4. **Whether an MVA exists at all.** Present on every single-premium 更改型 shape [S3] [S8]
   [S12] [S13]; **absent** on the monthly-declared level-premium shape [S2] and on the
   yen-premium shape, which says so explicitly [S5]. Composite: presence is a property of
   the shape, not a carrier preference, and the model-point flag carries it.
5. **How much of the MVA is disclosed.** A full rate table by elapsed year × rate move [S3];
   the 市場価格調整用利率 itself, fortnightly, by currency and guarantee period [S12]; narrative only
   [S8] [S13]. Composite: the full table, because it is the only artefact from which the
   adjustment can be reproduced (footnote 21).
6. **The surrender-charge scale and, more importantly, its base.** 7.0% → 0.7% on the 積立金
   [S3]; 10% → 0% and 5% → 0% in two vintages [S8]; 6.5% → 0.0% on the **基本保険金額** [S13];
   20% × (1 − 経過月数 ÷ 120) after a 70% factor [S5]; undisclosed at two carriers [S2] [S7].
   Composite: 7.0% → 0.7% on the 積立金. The base is the trap: three different bases are in
   use, and a rate quoted against one of them means nothing against another.
7. **The currency spread.** TTM ± 50銭 [S1] [S3] [S8]; TTM ± 25銭 [S5]; an unpublished 当社所定
   rate floored at TTB [S7]; **nil**, on the shape that never converts [S11]; and one
   printed asymmetric pair of +50銭 / −1銭 that is treated as [unverified] [S3]. Composite:
   symmetric ±50銭 (footnote 7). This is the one charge every carrier that converts does
   quantify.
8. **The charge stack's shape.** Three named layers, none quantified [S1] [S2]; charges
   named *inside* the crediting-rate formula and therefore observable only as a spread [S3];
   a single front-end percentage of the single premium banded by issue age, with no in-force
   charge at all because the rest sits inside the rate [S10]; and a split fixed/variable
   stack with 2.35% p.a. on the variable sleeve [S13]. Composite: the three named layers,
   with rates back-solved from the published surrender-value run (footnote 22). No two
   carriers in the set disclose the stack in compatible units.
9. **The death benefit's relation to the fund.** 基本保険金額 plus a ratcheting uplift [S1] [S2];
   **max(積立金, 解約返戻金)** with no sum assured above the fund [S3]; max(保障基準価格, 解約払戻金額) against
   a separately tracked guaranteed floor [S8]; a USD amount fixed for five years at a time
   and reset with the 予定利率 [S5]. Composite: the first on the LEVEL shape and the second on
   the SINGLE shape — the sharpest design fork in the product, because it decides whether
   there is a net amount at risk to charge for at all.
10. **The target-value menu and its test.** 105–200% in 1% steps, tested continuously with a
    one-year block on the conversion [S8]; 100 / 105 / 110%, tested every business day from
    one year after 契約日 [S9]; "105%, or 110–200% in 10% steps" in the FSA's description of
    the class [R6]. Composite: 110%, tested daily from month 12, on the yen-converted
    surrender value (footnote 16).
11. **The suppression factor, where it exists.** Four-step 70 / 77.5 / 85 / 92.5% [S2]; flat
    7割 [S7]; 70% → graded → 100% at 10 and 15 years [S5]. Composite: the four-step ramp — a
    deliberate delta against the chassis's flat 0.70.
12. **Reinstatement and the automatic premium loan.** 復活 within 3 years with an APL [S7];
    within 1 year with an APL [S2]; neither, with termination and payout of the surrender
    value instead [S5]. Composite: 3 years with the APL, inherited (footnote 19).
13. **What does not vary.** Uniform wherever the retrieved documents state it: every product
    is **終身** with no 満期保険金 [S1] [S2] [S3] [S7]; every 解約控除 runs to **zero at exactly ten
    years**, whatever its starting level and whatever its base [S3] [S5] [S8] [S13]; every
    減額 is treated as a partial surrender [S3]; every conversion uses a nominated bank's TTM
    with the **first published quote of the day** where it moves more than once [S1] [S3]
    [S5]; every contract is a **特定保険契約** requiring a 契約締結前交付書面 and, for a non-corporate
    policyholder, a **signed acknowledgement of FX risk** [S5] [R3] [REG-R37]; and every
    carrier warns that a loss can arise **with no exchange-rate movement at all**, purely
    from the currency spread. Equally uniform is a refusal: every carrier declines to
    publish the mortality-and-expense charge in currency terms, in the same words [S2] [S7].
    Those are the invariant core of the composite, and the last of them is why footnote 22
    exists.

---

## Regulatory context

**Prudential — ESR, and the reserving regime this product only recently entered.** From **31
March 2026** Japanese insurers are supervised on economic-value-based solvency regulation
(*keizai-kachi bēsu no soruvenshī kisei*, 経済価値ベースのソルベンシー規制, **ESR**), on which assets are
at fair value and liabilities are current estimate (現在推計) plus MOCE, re-measured at each 基準日
on assumptions re-set then and calibrated in principle to **99.5%**; early corrective action
triggers below **100%**, replacing the SMR (ソルベンシー・マージン比率) **200%** trigger [REG-R15]
[REG-R17]. Two features of the regime bear on this product specifically. **為替 is a named
market-risk category** in the standard model [REG-R15] — this is the one product in the
library whose liability is denominated in a currency the capital requirement charges for
directly. And the old basis was **ロックイン**, with mortality, lapse and interest fixed at
issue; a contract whose crediting rate is redeclared monthly and whose surrender value moves
with market rates is precisely the contract a locked-in basis cannot describe, which is why
a re-projectable, assumption-parameterized cash-flow model is the operative artefact here
rather than a one-off pricing exercise [REG-R15]. `jplib` computes neither ratio; the
standard-model coefficients sit in 告示 that were not opened and are [unverified] [REG-R16].

**標準責任準備金, and its start date.** 保険業法第116条 obliges an insurer to hold 責任準備金 and delegates
the method and the calculation basis [REG-R4]; 施行規則第68条 fixes the scope and 第69条 the
taxonomy — 保険料積立金, 未経過保険料, 払戻積立金, 危険準備金 [REG-R7] [REG-R8]; 平成8年大蔵省告示第48号 sets 平準純保険料式, the
table vintages and the standard valuation interest rate (*hyōjun riritsu*, 標準利率)
machinery [REG-R10]. The product-specific fact is the date:
**USD- and AUD-denominated contracts entered the regime only on 1 October 2021**, with the
平成13年金融庁告示第24号 amendments following on 1 April 2022, and **every other foreign currency
remains outside the 対象契約** [R1] [REG-R12]. The 標準利率 for USD contracts is built from a 基準利率 =
Σ (対象利率 in each band × 安全率係数), where the 対象利率 is derived from A-rated same-currency
corporate bond yields at 10 and 20 years, each taken as the lower of the one-month and
three-month trailing averages; the 基準日 is the **1st of every month**, a deviation of ≥0.05%
moves the rate to the nearest 0.05% multiple, and the new rate applies to contracts written
from one month after the 基準日 [R1]. The 安全率係数 run 1.0 at or below 0% down to 0.75 above 6%
for USD [R1]. **The resulting numeric 標準利率 is not published on any retrieved page**, so no
figure for it is asserted anywhere in this library; the carrier-published 基準利率 and 市場価格調整用利率
series [S4] [S12] [S14] are proxies for the *level*, not the statutory rate. An 積立利率変動
contract stays inside the regime because 施行規則第68条 excludes contracts whose 約款 lets the
insurer change the **予定利率**, not contracts whose crediting rate floats above a fixed one
[REG-R7]. Where the minimum-guarantee machinery is used, the 代替的方式 conditions apply to a
non-yen contract 「その特性に応じ…に準じた条件」, with the 10% tolerance against the 標準的方式 unchanged [R2].
価格変動準備金 is asset-driven and never modelled here [REG-R3], but it carries an FX-specific rule
worth naming: where it is computed inside the 責任準備金 of 外貨建て保険, the asset scope must come
from the asset classes matching the 外貨建て保険 segment on a segregated accounting basis, and the
**危険準備金Ⅱ** for those contracts must use the **外貨建て保険 risk coefficient** [R4]. This library
projects gross cash flows and builds none of these reserves.

What the regime asks a liability model for is set by 保険業法第121条第1項第1号, which requires the
appointed actuary (保険計理人), appointed under 第120条, to confirm in an 意見書 that the reserve is
soundly accumulated [REG-R5] [REG-R6]; the IAJ practice standard turns that into the
**1号収支分析**, a forward income-and-outgo analysis over at least ten future years by product
segment under prescribed scenarios, and it addresses MVA and foreign-currency business
explicitly [REG-R22]. That is the shape of this product's projection.

**Conduct — the layer that makes this product unusual.** Because it is a 特定保険契約 [REG-R37],
the FIEA rules on advertising, pre-contract disclosure and suitability apply by 準用, and the
契約締結前交付書面 must be set in at least 8-point type with certain items at 12 [R3]. The 監督指針 adds
two product-specific item sets. For **外貨建て保険**: that the yen-converted benefit at payment
can fall below the yen-converted amount at the contract date and that a loss may arise, and
an explanation of the fees that arise specifically from contracting in a foreign currency
[R3]. For an **MVA product**: that the surrender value reflects the market-driven price
movement of the backing assets, that a surrender within a period can produce a loss, **an
illustration of the proportion deducted from the 保険料積立金 at surrender**, and the in-force
charges [R3] [REG-R14] — the reason the MVA is public as a rate table and not as a formula.
Separately, on a non-corporate 外貨建て保険 sale the insurer must explain the FX risk fully and
**take a signed confirmation that the policyholder understood it** [R3]. The industry layer
adds the 適正表示ガイドライン, which requires the 実質的な利回り on a 外貨建一時払 design to be displayed alongside
the 積立利率 and measured **at the point where the MVA, the rate-variation period and the
surrender charge have all expired**, sets the standard risk wording for MVA products, and
requires any illustration of a market move to print the no-move case beside it [R8].
Presenting a non-guaranteed element as certain is 断定的判断の提供 [REG-R38], which is why the
guaranteed 3.00% column and the 3.50% / 4.00% columns are three columns and not an average
[S2]. The 説明義務 limb covering an **exercise period or restriction on cancellation** is the
statutory hook for all three of this product's surrender-layer mechanics — the 解約控除, the MVA
and the 低解約返戻金 suppression period [REG-R39]. The supervisory response to the complaint
record was the 外貨建保険販売資格試験 and its 販売資格者登録制 [R7], and the FSA's monitoring reports name the
target-hit-and-rebuy pattern, the L-shaped commission and the MVA-plus- surrender-charge
drag as the sector's live issues [R5] [R6] [R9]. On insurer failure, cover is 90% of the
責任準備金等 with **no carve-out for foreign-currency contracts** [R10] [REG-R40] [REG-R41].

**Classification and tax.** 第一分野 under 保険業法第3条第4項第1号 [REG-R1], and 特定保険契約 under 第300条の2
[REG-R37] — the two classifications are independent and both bite. The premium, including a
single premium, sits in the 一般 basket of the post-2012 生命保険料控除, deductible on a banded
schedule to ¥40,000 per basket against an overall income-tax cap of ¥120,000 [S13]
[REG-R43]. A death benefit where 契約者 = 被保険者 is subject to 相続税, exempt for heirs to
¥5,000,000 × the number of statutory heirs [REG-R44] [REG-R45] [S13]. Surrender or maturity
proceeds taken as a lump sum by the premium payer are **一時所得**: proceeds less premiums paid
(net of any 剰余金) less a ¥500,000 special deduction, of which **half** enters taxable income
[R11] [REG-R46] [S13]. Both legs are translated to yen for that computation, so the FX gain
is folded into the 一時所得 rather than taxed separately — but **no retrieved NTA page says so
explicitly**, and the treatment of 為替差益 on a foreign-currency policy is therefore
[unverified] [R11]. The contract is not eligible for NISA or iDeCo [S13]. `jplib` models
contractual cash flows, not the policyholder's tax position.

**Professional standards and the accounting frame.** The basis any model uses is
professionally owned by the 保険計理人 [REG-R5] working to the IAJ's 実務基準 [REG-R22]; the
mortality table that binds the statutory reserve is produced by the IAJ and published free
at a stable public URL [REG-R18], but its site terms prohibit reproduction and transmission
to third parties, so this library cites it, quotes only the rates a worked example needs,
and ships a **[std]** construction whose provenance column points at the IAJ entry
[REG-R21]. The table is a **valuation** table carrying an explicit margin at a 2σ level and
built on an insurance age, nearest birthday (*hoken-nenrei*, 保険年齢) basis [REG-R20], so any
best-estimate basis is a [std] adjustment *of* a sourced table. And the frame a reader
arriving from `uklib` must not import: **IFRS 17 is
not mandatory in Japan** — IFRS applies as 指定国際会計基準 on a voluntary basis [REG-R47]. J-GAAP
statutory reserving, the ESR economic balance sheet and IFRS 17 are three separate bases
over one set of projected cash flows, and this product keeps the cash flows basis-agnostic.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-fx_whole_life-r1
[R10]: #jplib-fx_whole_life-r10
[R11]: #jplib-fx_whole_life-r11
[R2]: #jplib-fx_whole_life-r2
[R3]: #jplib-fx_whole_life-r3
[R4]: #jplib-fx_whole_life-r4
[R5]: #jplib-fx_whole_life-r5
[R6]: #jplib-fx_whole_life-r6
[R7]: #jplib-fx_whole_life-r7
[R8]: #jplib-fx_whole_life-r8
[R9]: #jplib-fx_whole_life-r9
[REG-R1]: #jplib-reg-r1
[REG-R10]: #jplib-reg-r10
[REG-R12]: #jplib-reg-r12
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R16]: #jplib-reg-r16
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R3]: #jplib-reg-r3
[REG-R31]: #jplib-reg-r31
[REG-R34]: #jplib-reg-r34
[REG-R35]: #jplib-reg-r35
[REG-R36]: #jplib-reg-r36
[REG-R37]: #jplib-reg-r37
[REG-R38]: #jplib-reg-r38
[REG-R39]: #jplib-reg-r39
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R43]: #jplib-reg-r43
[REG-R44]: #jplib-reg-r44
[REG-R45]: #jplib-reg-r45
[REG-R46]: #jplib-reg-r46
[REG-R47]: #jplib-reg-r47
[REG-R5]: #jplib-reg-r5
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
