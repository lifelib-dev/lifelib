# Product Specification

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** This is a *standardized composite specification* of Japanese whole life
assurance (*shūshin hoken*, 終身保険), including its suppressed-surrender-value
(*tei-kaiyaku-henreikin-gata*, 低解約返戻金型) form, assembled for reference liability cash-flow
modeling. It does not describe any single insurer's product. Facts carrying a source tag — [S#]
(primary product documents: policy conditions (*yakkan*, 約款), ご契約のしおり, パンフレット and published rate
pages) and [R#] (regulatory and actuarial references), both numbered per
`_research/whole-life.md` and resolved in `sources.md` (same directory; numbering frozen,
never renumbered), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) —
were extracted from the cited document. Values marked **[std]** are standardizations
introduced for the reference implementation; each [std] table row carries a numbered
footnote giving the rationale and, where one exists, the observed range across insurers.
Facts the research pass could not verify are flagged [unverified]. The composite is drawn
from seven carriers' 約款 and brochures — two of which publish complete numeric
surrender-value tables [S4] [S7], four of which state the suppression factor [S3] [S7] [S9]
[S11], and two of which are deliberately included as counter-examples because they do *not*
offer the automatic premium loan [S8] [S9] — plus one carrier's published single-premium
rate page cited only for a scope boundary [S12].

This product is the library's **savings chassis**. The
[endowment product spec (養老保険)](../endowment/product-spec.md) inherits its reserve, surrender-value
and loan machinery and adds a maturity benefit (*manki hokenkin*, 満期保険金); the
[FX whole life product spec (外貨建終身保険)](../fx_whole_life/product-spec.md) inherits it and adds
a variable crediting rate (*tsumitate riritsu hendō*, 積立利率変動), market value adjustment, MVA
(*shijō kakaku chōsei*, 市場価格調整) and a currency layer.
Mechanics specified here are stated once, here.

---

## Product overview and market role

終身保険 is whole-of-life cover: a level premium buys a death benefit payable whenever the
insured dies, with no expiry date and no 満期保険金 [S1] [S3] [S5] [S7] [S9] [S10]. One carrier
states the negative flatly in its application terms: this contract has neither dividends nor
a maturity benefit [S5]. Participation varies by carrier, and the composite is 無配当. The main
contract pays two benefits at the same amount: death benefit (**死亡保険金**) on death, and
severe-disability benefit (*kōdo shōgai hokenkin*, **高度障害保険金**) on the insured reaching the
disability state defined in the 約款's own schedule; paying the second extinguishes the
contract retroactively to the date the state was reached [S1] [S3] [S7] [S9]. Because the
contract must eventually pay, it accumulates a policy value (*hokenryō tsumitatekin*, 保険料積立金)
and therefore a surrender value (*kaiyaku-henreikin*, 解約返戻金) — which is what makes it
a savings product sold on protection wording, and what makes every mechanic in this document
turn on the surrender value rather than on the sum assured.

It is a first-sector (*dai-ichi bun'ya*, 第一分野) contract — fixed-sum insurance on human
survival or death under 保険業法第3条第4項第1号 [REG-R1] — which decides the statutory mortality table
the reserve must use, 生保標準生命表2018（死亡保険用）for contracts concluded from 1 April 2018 [REG-R10]
[REG-R11] [R1], and separates this chassis from the third-sector products:
[medical (医療保険)](../medical/product-spec.md), [cancer (がん保険)](../cancer/product-spec.md) and
[nursing care (介護保険)](../nursing_care/product-spec.md).

**Market position: second-largest individual line on every measure, and the largest of the
savings-bearing lines.** For FY2024, individual insurance (個人保険) new business was 12.43
million policies, of which 終身保険 was 2.31 million (18.6%), behind 医療保険 at 23.8%; new business
by sum assured was ¥57.06 trillion, of which 終身保険 was ¥12.997 trillion (22.8%), behind 定期保険
at 43.2%. In force, 終身保険 was 38.48 million policies (19.7% of 195.3 million) and ¥215.10
trillion of sum assured (27.6% of ¥778.99 trillion) [R12] [REG-R31]. The industry 解約・失効率 was
5.6%, but the same report defines it as surrendered-and-lapsed sum assured over opening
in-force sum assured, industry-wide across all product types [R12] — an amount-weighted,
all-product bound, not a whole-life per-policy lapse rate, and used in this library only as
a sanity check on a **[std]** lapse basis.

Demand is driven by two things a US or UK reader will not assume. First, **inheritance tax
planning**: a death benefit received by an heir is exempt up to ¥5,000,000 multiplied by the
number of statutory heirs [R9] [R10] [REG-R44] [REG-R45], which is why sums assured cluster
in multiples of ¥5,000,000 and why a policy bought at 60 is a normal transaction. Second,
the life insurance premium deduction (*seimei hokenryō kōjo*, **生命保険料控除**): three baskets of
¥40,000 capped at ¥120,000 in total, whole life competing for the 一般 basket alongside term
cover [R11] [REG-R43]. The 低解約返戻金型 variant adds a third driver — a surrender value
engineered to cross 100% of premiums paid shortly after the premium-paying period ends, so
the contract is sold as a savings vehicle with a death benefit attached. On the one
published table, the 払戻率 runs 70.1% at duration 5, 78.0% at 15 while still suppressed, and
111.5% immediately after the suppression ends [S4].

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Level-premium 終身保険; non-participating (*mu-haitō*, 無配当); carries 保険料積立金 and 解約返戻金; not unit-linked | [S3] [S5] [S11]; default **[std]** (1) |
| Policy term (保険期間) | 終身 — whole of life. No expiry, no 満期保険金 | [S1] [S3] [S5] [S7] [S9] [S10] |
| Regulatory class | 第一分野, 保険業法第3条第4項第1号 | [REG-R1] |
| 低解約返戻金型 switch | Model-point flag. When on: suppression factor 70%, suppressed period identical to 保険料払込期間, full value from 払込満了 | Factor: [S3] [S7] [S9] [S11]. Period and full value from 払込満了: [S3] [S6] [S7] [S11]. **[S6] states the period only — it does not give the percentage** |
| Premium-paying period (保険料払込期間) | 終身払, or 年満了 5 / 10 / 15 / 20 年, or 歳満了 to age 50 / 55 / 60 / 65 / 70 / 75 / 80 | [S5] |
| Issue age (契約年齢) | 15–80; 歳満了 options gated by a 10-year minimum payment period (e.g. 60歳払済 to age 50), 20年払 to age 75 | [S5]; envelope **[std]** (2) |
| Age basis | Attained age (*man-nenrei*, 満年齢) with the fractional year discarded at 契約日; the rating age then increments on each 年単位の契約応当日, not on the birthday | [S1] [S3] [S9] |
| Sum assured (保険金額) | ¥2,000,000–¥50,000,000 in ¥1,000,000 units; a 5-year payment term requires ≥ ¥10,000,000 | [S5]; adoption **[std]** (3) |
| Sex | Male and female rated separately; the female rate is about 92% of the male rate at age 30 on the one published scale | [S4] |
| Lives basis | Single life; policyholder (契約者) and insured (被保険者) the same person | [S5]; scope **[std]** (4) |
| **Anchor model cell** | Male, 契約年齢 30, 低解約返戻金型 on, 保険金額 ¥5,000,000, 保険期間 終身, 保険料払込期間 15年, 月払保険料 ¥14,580 (annualized ¥174,960) | [S4]; annualization **[std]** (5) |

Footnotes to [std] rows:

1. Participation varies and is part of the product name at every carrier: 無配当 at three [S1]
   [S3] [S5] [S11], a dividend declared every five years out of investment margin (*go-nen
   goto risa haitō*, 5年ごと利差配当) at a fourth [S7], 5年ごと配当 at a fifth [S10], 有配当 at a sixth [S8],
   and a participating design at a seventh [S9]. 無配当 is the composite default because it is
   the largest single group and because a dividend is an insurer-discretionary element, not
   a contractual one [REG-R9]. The 5年ごと利差配当 design is retained as a parameterized variant,
   not dropped — see Riders and options.
2. Only one carrier publishes a complete issue-age × payment-term grid [S5]; a second
   publishes only the 契約年齢 definition and no envelope at all, because its envelopes live in
   a 契約概要 that is a separate document [S1]; a third is bound instead by a statutory maximum
   sum insurable (*kanyū gendogaku*, 加入限度額) [S9]. The composite adopts the one published
   grid verbatim, including its asymmetry — 年満了 short-pay is offered to the top of the issue
   range while 歳満了 short-pay is not [S5]. No carrier in the set publishes a maximum issue
   age above 80; whether that is universal is [unverified].
3. The band is one carrier's published range [S5]; its rule that the ¥1,000,000 unit is
   available only at ages 76–80 is dropped as a single-carrier refinement. The observed
   alternative is a hard **statutory** ceiling rather than an underwriting one — ¥7,000,000
   where the insured is 15 or under and ¥10,000,000 from 16, reaching a cumulative
   ¥20,000,000 at ages 20–55 subject to conditions, with over-limit applications declined
   outright and a breach discovered after issue voiding the excess [S9]. That ceiling has no
   analogue in the US or UK reference sets, and it is out of the composite because it
   belongs to one carrier's statutory position rather than to the product.
4. One carrier requires 契約者 = 被保険者 [S5]; the others do not make the requirement explicit in
   the retrieved documents. There is no joint-life whole life in the retrieved set, so the
   composite is single-life throughout and treats third-party-policyholder arrangements as a
   tax question rather than a cash-flow one [R9].
5. The anchor is the one model point for which a carrier publishes a complete
   surrender-value run — male 30, ¥5,000,000, 終身, 保険料払込期間 15年 (= the suppressed period),
   月払保険料 ¥14,580, with 解約払戻金 at durations 5 / 10 / 15 / 15+ / 20 / 30 / 40 / 50 [S4]. It is
   round, internally consistent (14,580 × 180 = ¥2,624,400, the published cumulative premium
   at 15 years, and every published 払戻率 reproduces to the displayed decimal), and it
   **exhibits the cliff**. `WholeLife_JP_A` runs on an annual grid, so the annual premium is
   standardized as 12 × the monthly figure = ¥174,960; no carrier publishes an annual-mode
   premium for this cell, so the modal discount a real 年払 scale would carry is not applied.
   The sum assured sits inside the household 普通死亡保険金 bands of the national survey [REG-R32]
   and is one heir's worth of the inheritance-tax exemption [REG-R44].

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level and guaranteed for the whole of 保険料払込期間; no review mechanic | [S1] [S3] [S7] [S10] |
| Mode (払込回数) | 月払 / 半年払 / 年払 at every carrier; composite default 年払 | [S1] [S3] [S5] [S9] [S10]; default **[std]** (6) |
| Route (払込経路) | Direct debit (口座振替) or クレジットカード払; one carrier lists five routes | [S1] [S3] [S5] |
| Rating factors | 契約年齢, sex, 保険金額 (via 高額割引), 保険料払込期間, and whether the 低解約返戻金型 form is taken | [S4] [S7] [S8] |
| 低解約返戻金型 premium discount | The suppressed form costs 83.7% of the ordinary form on the one carrier that publishes both scales for the same model point | [S7] |
| Volume discount (高額割引) | Applied from ¥10,000,000 of sum assured | observed [S4] [S7] [S8] [S11]; threshold **[std]** (7) |
| Assumed interest rate (*yotei riritsu*, 予定利率) | Not published for level-premium designs. Composite value 1.75% p.a., flat | [S11] [S12]; **[std]** (8) |
| Advance payment (前納) | Available — 6 or 12 months' monthly premiums at a company discount rate, or arbitrary future premiums on 半年払/年払 accumulated at a company rate. Out of scope | [S1] [S7] [S10]; scope **[std]** (9) |
| Premium waiver (保険料払込免除) | On a listed 身体障害の状態 arising from an 不慮の事故 within 180 days, with the usual conduct exclusions; does **not** apply after 払込満了; an optional 特定疾病 特則 extends the trigger | [S3] |
| Non-smoker rating | Handled as a rider (*tokuyaku*, 特約) substituting a 非喫煙保険料率 for the main contract and named riders, not as a rating class | [S1] |

6. Every carrier offers 月払 / 半年払 / 年払 [S1] [S3] [S5] [S9] [S10], and monthly is the mode the
   published scales are quoted in [S4] [S7]. The model is annual-step, so the composite pays
   annually at 12 × the monthly figure (footnote 5). No carrier publishes the modal loading
   a real 年払 scale carries, so applying one would be an invention; the direction of the
   resulting error — annual-mode premium slightly overstated — is stated in
   `technical-notes.md` rather than hidden.
7. Observed thresholds: ≥ ¥30,000,000 on an aggregation base at one carrier [S8]; ≥
   ¥10,000,000 in an illustration footnote at a second [S7]; a company-set threshold at a
   third [S11]; and a fourth embeds the discount in its rate table without naming a
   threshold, where ¥10,000,000 of cover costs ¥29,110/month against ¥29,160 for two
   ¥5,000,000 policies, and ¥2,000,000 of cover costs 2.2% more per ¥10,000 of sum assured
   than ¥5,000,000 does [S4]. ¥10,000,000 is taken because it is the only value stated twice
   and the point where the published per-unit rate visibly turns.
8. **The pricing basis is not public, and that is structural rather than accidental.** The
   予定利率, 予定死亡率 and 予定事業費率 live in the 保険料及び責任準備金の算出方法書, one of the four 基礎書類 (*kiso shorui*)
   filed with the FSA under 保険業法第4条第2項 and not published [REG-R2]. What is public: one
   carrier disclosed **1.75%** for a level-premium design in a booklet dated 2010 [S11], and
   single-premium rates are disclosed continuously — 2.44% (15-year plan) and 2.54% (30-year
   plan) for the fortnight from 16 August 2026, with a 最低保証予定利率 of 0.25% [S12]. The current
   level-premium 予定利率 is **[unverified]**, and secondary sources reporting a 1.75–2.5% range
   are not relied on. The composite takes 1.75% because it is the only level-premium figure
   actually read from a carrier document, and every document using it carries that date. The
   statutory standard valuation rate (*hyōjun riritsu*, 標準利率) is a separate rate on a
   separate calendar, and its current value could not be established from any retrieved
   official document either [R8] [REG-R10].
9. 前納, and one carrier's 保険料のステップ払込方式の特則 — an elective scale lower for a 10- or 15-year step
   period and higher afterwards, revertible with a settlement payment [S10] — are both
   excluded: they change the premium *stream* without changing any mechanic this chassis
   exists to demonstrate, and both need an unpublished discount or settlement basis to
   model.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| 死亡保険金 | 保険金額, level for life, paid on death at any time; net of any outstanding loan or APL balance | [S1] [S3] [S7] [S9] [S10] |
| 高度障害保険金 | Same amount as the death benefit, on the 高度障害状態 defined in the 約款's 別表; payment extinguishes the contract retroactively to the date the state was reached | [S1] [S3] [S7] [S9] |
| Precedence between the two | If the insured dies before claiming the 高度障害保険金, only the death benefit is paid | [S1] |
| Benefit shape | Level only. Step-down and multiplier designs are excluded | [S9]; scope **[std]** (10) |
| 免責 — suicide | No benefit where the insured commits suicide within **3 years** of the 責任開始期, reset to the latest 復活 | [S1] [S3] [S7] [S8] [S9] [S10]; statutory frame [REG-R34] |
| 免責 — other | Intentional act of the 保険契約者 or of the 死亡保険金受取人; war and civil disturbance. On the 高度障害保険金, also the insured's own intentional act or criminal act | [S1] [S9] [S10] |
| Payment when a benefit is refused | The 保険料積立金 / policy reserve (*sekinin-junbikin*, 責任準備金) is paid to the policyholder. Nothing is paid where the policyholder intentionally caused the death; where one of several beneficiaries acted intentionally, the others are paid and the reserve for the withheld share goes to the policyholder | [S1] [S9] [S10] |
| War clause | Scalable, not absolute: where the increase in affected insureds does not disturb the calculation basis the insurer may pay in full or pay a proportionately reduced amount | [S1] [S10] |
| Contestability (告知義務違反) | Rescission within **2 years** of the 責任開始日 (or of the 復活日); beyond that only where a claim event inside the window is involved | [S1] [S7] [S9]; statutory ceiling [REG-R35] |
| Underwriting loadings | Handled by a 特別条件付保険特約 rather than by declining | [S3] |

10. One carrier sells designs in which the death benefit is the 基準保険金額 during 保険料払込期間 and
    steps **down** to 50% of it afterwards, and separately doubles the benefit where death
    follows an 不慮の事故 within 180 days or a listed 感染症 [S9]. Both are that carrier's designs
    alone in this set. The composite death benefit is level for life: it is the shape at six
    of the seven carriers [S1] [S3] [S7] [S8] [S10] [S11], and a step-down at 払込満了 would
    collide with the 低解約返戻金型 cliff at the same date, making the model point unable to
    isolate either effect. The step-down design is named here so that a reader meeting it in
    the market knows it is real and knows this library does not model it.

### Options and contract alterations

| Parameter | Representative value | Basis |
|---|---|---|
| Automatic premium loan, APL (自動振替貸付) | Elected at outset, **on by default**; at the expiry of 猶予期間 the insurer advances the premium due against the surrender value and the contract continues | [S1] [S7] [S10] [S11]; default **[std]** (11); election requirement [REG-R14] |
| APL continuation condition | The advance plus interest must not exceed the surrender value computed as if the premium had been paid, net of any existing loan | [S1] [S3] [S10] |
| APL interest | Compound, rolled into principal at each subsequent grace expiry (annually on 年払). Published ceilings 年8% / 半年4% / 月 8/12%. Composite rate 2.75% p.a. | ceilings [S1] [S7] [S10]; level [S2]; pick **[std]** (12) |
| APL cancellation window | An advance already made is treated as never having happened if 解約, 減額 or conversion to 払済保険 is requested within **3 months** of the day after grace expiry | [S1] [S3] [S10] |
| Policy loan (契約者貸付) | Up to **9/10** of the surrender value while premiums are being paid, **8/10** once the contract is 保険料払込済; existing loan and APL principal and interest deducted first; compound interest at a company-set rate | [S1] [S3] [S7]; limit **[std]** (14) |
| Reduced paid-up (払済保険) | The surrender value net of loan and APL balance is applied as a single premium to a reduced sum assured. Term stays 終身; premiums cease; riders terminate | [S1] [S3] [S7] [S9] [S10] |
| Extended term (延長定期保険) | Surrender value applied as a single premium to term cover for the **same** sum assured, term set by the amount available, capped at the original 払込満了 date. **Out of scope** | [S7]; scope **[std]** (13) |
| Sum-assured reduction (減額) | Permitted; the reduced portion is treated as surrendered and pays the corresponding surrender value | [S1] [S3] [S9] [S10] |
| 保険料払込期間の変更 | Offered at two carriers subject to conditions. Out of scope | [S1] [S10]; scope **[std]** (9) |
| リビング・ニーズ特約 | Attached at no extra premium; on a prognosis of **6 months or less**, the 指定保険金額 elected by the insured is paid less 6 months' interest and premium equivalent, capped at ¥30,000,000; the main contract's sum assured reduces by the amount paid | [S1] [S3] [S4] [S7] |

11. Election varies more than any other mechanic in the file: **opt-out** at four carriers
    [S1] [S7] [S10] [S11]; **opt-in** at one, whose booklet states that without the request
    no APL is made [S3]; **absent** at two — one has none at all [S8], the other only a
    requested 保険料振替貸付 [S9]. The composite takes opt-out because it is the majority and
    because it is the position that changes lapse mechanics. The supervisory guideline
    requires an APL to be **at the policyholder's election** with prompt notice when
    exercised (監督指針 IV-1-12) [REG-R14], so the model implements it as an election with a
    default value, never as an unconditional no-lapse rule: the model point carries an
    `apl_elected` flag and the off position must be exercised in testing.
12. Only the *ceilings* are published, identically at three carriers — 年払 up to 8% p.a., 半年払
    up to 4% per half year, 月払 up to 8/12% per month [S1] [S7] [S10] — with a fourth
    publishing a single 年8% ceiling [S3]. One carrier publishes applied rates, banded by 契約日
    vintage rather than by current market: 4.00% for contracts to 1999-04-01, 3.25% to
    2001-04-01, and **2.75%** from 2001-04-02, the same schedule serving both 契約者貸付 and
    自動振替貸付 [S2]. The composite takes 2.75% — the band a currently written contract falls in
    on the only published schedule — and the vintage banding tells the modeller the right
    thing: the loan rate tracks the vintage's 予定利率, not the current market. Two carriers
    review the rate each January and July, the revision applying to existing loans [S7]
    [S11]; the composite holds it flat and lists the review as a sensitivity.
13. 延長定期保険 appears in **one** carrier's documents in the whole set [S7]; five others have no
    such article in their retrieved 約款 [S1] [S3] [S8] [S9] [S10], and it was not in the
    chapters retrieved from the seventh [S11]. Treating extended term as a universal
    Japanese whole life option would be wrong, so it is out of the composite and out of the
    model. It is specified in the table because a later product may need it, and because
    during the suppressed period the 70% base makes the solved term correspondingly shorter
    — a cliff effect worth recording. Its detail at that carrier: not written where the
    solved term is under one year or the insured is already 80, riders terminate except the
    proxy-claimant 特約, and 復旧 is available within 3 years [S7].
14. The 9/10-in-payment, 8/10-paid-up split is stated identically at three carriers [S1]
    [S3] [S7]. A fourth is tighter — 8/10 **less three months' premium**, the deduction
    waived once the contract is paid up or premiums are waived [S8] — and a fifth publishes
    no fraction at all, only a company method, with a fixed one-year 貸付期間 that auto-renews
    by capitalising interest [S9]. The composite takes the three-carrier split. Minimum draw
    amounts (¥50,000 first, ¥10,000 thereafter at one carrier [S7]) are not modelled.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 解約返戻金 basis | A function of **both** elapsed months and paid months during 保険料払込期間, and of elapsed months alone afterwards; the elapsed count is capped at the paid count while premiums are due. The formula itself is in the unpublished 算出方法書 | [S1] [S3] [S10]; construction **[std]** (15) |
| 低解約払戻期間 | Identical to 保険料払込期間. On a 終身払 contract it therefore runs for life | [S3] [S6] [S7] [S11] |
| Suppression factor | **0.70**, applied as a multiplier to the ordinary surrender value | [S3] [S7] [S9] [S11] |
| The step at 払込満了 | A discontinuity, not a ramp: on the one published table the value goes from ¥2,047,650 to ¥2,928,450 across the boundary, a 43.0% jump, and 払戻率 from 78.0% to 111.5% | [S4] [S7] |
| Clawback | If not all premiums falling in the suppressed period were paid, the suppressed basis continues to apply after the period ends | [S3] [S4] [S5] [S9] |
| 満期保険金 | None | [S5] |
| Grace (猶予期間) | 月払: from the first day of the month following the 払込期月 to the last day of that month. 半年払 / 年払: to the monthly 契約応当日 in the month after that, with named end-of-month substitutions | [S1] [S3] [S10]; regime **[std]** (16) |
| Lapse (失効) | From the day after grace expiry, **only where the APL cannot carry the premium**. The policyholder may then claim the surrender value | [S1] [S3] [S10] |
| Loan-excess termination | Where loan and APL principal and interest exceed the surrender value the insurer notifies for a top-up; if unpaid by the end of the month following the notice month the contract lapses from the next day | [S1] [S3] [S10] |
| Reinstatement (復活) | Within **3 years** of lapse, on fresh 告知 and payment of the arrears; barred once the surrender value has been claimed. The 責任開始期 resets, restarting both the suicide clause and the contestability clock | [S1] [S3] [S7] [S10]; window **[std]** (17) |
| クーリング・オフ | 8 days from the later of delivery of the disclosure document and the application date, effective on dispatch. **Out of scope** | [REG-R36]; scope **[std]** (18) |
| Policyholder protection | On a member insurer's failure, up to **90%** of the 責任準備金 at the failure date | [REG-R40] [REG-R41] |

15. No carrier publishes a surrender-value *formula*; the 算出方法書 that holds it is a filed but
    unpublished 基礎書類 [REG-R2]. What the 約款 do publish is the argument list — elapsed and
    paid months, with the elapsed count capped at the paid count during the premium-paying
    period [S1] [S3] [S10] — and two carriers publish complete numeric tables [S4] [S7]. The
    library therefore constructs the ordinary surrender value as a **[std]** function (a
    net-level-premium policy value less an acquisition-cost deduction grading to zero)
    calibrated to reproduce the published table at the anchor cell, with the construction
    and its fit stated in `technical-notes.md`. That is the honest position: the *level* is
    sourced at one model point, the *shape between points* is standardized.
16. Three grace regimes are observed and they are not variants of one rule: the roughly
    one-month 約款 grace above at four carriers [S1] [S3] [S7] [S10]; a **two-month** grace at
    one, whose worked example has a September premium due 9/1–9/30, grace 10/1–11/30 and
    lapse on 12/1 [S9]; and at one carrier no grace and no lapse at all — a 催告 naming a
    解除予定日, the monthly anniversary in the **third month after** the 払込期月, on which the
    contract is terminated (解除) and the surrender value paid net of unpaid premiums [S8].
    The composite takes the four-carrier grace. The 解除 regime is named but excluded because
    it differs in kind: a terminated contract cannot be reinstated at all, whereas a 失効
    contract can.
17. 3 years at four carriers [S1] [S3] [S7] [S10]; **1 year** at one [S9]; **none** at the
    carrier that terminates rather than lapsing [S8]. The composite takes 3 years. The
    window matters more than its length suggests: Japanese policies really do come back, so
    a lapse decrement on this chassis is not a terminal state, and the reinstatement
    assumption is a **[std]** behavioural input rather than an omission.
18. The statutory cooling-off applies to every contract in this composite — the exclusion
    for terms of one year or less cannot bite on a 終身 contract [REG-R36]. `jplib` projects
    from the point cover is in force and scopes the window out, stated here rather than
    silently omitted because it is a real early-duration decrement a first-year study would
    see.

---

## Contractual mechanics

Notation used below and carried into `technical-notes.md`:

    x       契約年齢 at issue (満年齢, fractional year discarded)
    t       completed policy years since 契約日 (the annual grid step)
    m       保険料払込期間 in years; m = infinity for a 終身払 contract
    SA      保険金額
    P       annual premium, level for t < m, zero for t >= m
    V(t)    the ordinary (unsuppressed) surrender value at t
    CV(t)   the surrender value actually payable at t
    k       解約払戻金支払割合, the suppression factor (0.70 when 低解約返戻金型 is on)
    L(t)    outstanding 契約者貸付 + 自動振替貸付 principal and interest at t
    i_L     the loan / APL interest rate

### Death and 高度障害 benefit

Both benefits are `SA`, paid net of `L(t)` [S1] [S9] [S10]. They are alternatives on one
sum: the 高度障害保険金 is not an addition to the death benefit but an acceleration of it on a
disability trigger, and its payment ends the contract retroactively to the date the 高度障害状態
was reached [S1] [S3] [S7] [S9]. If the insured dies before claiming it, only the death
benefit is paid [S1]. For modelling, the two are one decrement on one benefit amount — and,
usefully, the statutory valuation table already works that way: 生保標準生命表2018（死亡保険用）
**includes 高度障害 inside the death rate** [REG-R20] [R2], so a projection using it must not
add a separate disability decrement on top.

Where a benefit is refused for an 免責事由, the contract does not simply forfeit: the 保険料積立金 or
責任準備金 is paid to the policyholder instead [S1] [S9] [S10]. The only case in which nothing is
paid is where the policyholder intentionally caused the death [S1] [S10]. A model that
treats an exclusion as a zero-payment event overstates the insurer's position; the composite
treats a refused death claim as a payment of the policy value.

The **suicide exclusion runs three years**, at every carrier in the set [S1] [S3] [S7] [S8]
[S9] [S10] — three times the twelve months of the UK composite in `uklib`. That period is
**contractual, not statutory**: 保険法第51条第1号 excludes suicide with **no time limit at all**,
and the three-year 免責期間 is a narrowing of the statute in the insurer's 約款, permitted because
it favours the policyholder [REG-R34]. The same asymmetry applies to contestability: the 約款
window is 2 years [S1] [S7] [S9] against a statutory ceiling of 5 years from inception with
a one-month use-it-or-lose-it clock from discovery [REG-R35]. Both windows restart on 復活
[S1] [S7] [S9] [S10].

### 解約返戻金 and the 低解約返戻金型 cliff

The payable surrender value is

    CV(t) = k * V(t)     for t <  m      (k = 0.70 when 低解約返戻金型 is on, 1.00 otherwise)
    CV(t) =     V(t)     for t >= m

and the transition at `t = m` is a **step**. This is the product's signature and the one
thing a model must not smooth. Two carriers' published tables agree on it to rounding. On
the anchor cell, ¥2,047,650 the day before the boundary against ¥2,928,450 immediately after
— the pre-cliff figure is quoted one day earlier, which is why the observed ratio is 0.6992
rather than exactly 0.70 [S4]. On the other published pair, the ratios of suppressed to
ordinary value at durations 5, 10, 20 and 30 are 0.7004, 0.6999, 0.7001 and 0.6999 — exact
to rounding at every duration [S7]. That second table also settles what the suppression
*is*: at duration 40, well past 払込満了, the suppressed and ordinary products have
**identical** surrender values, ¥8,159,000 [S7]. The suppression is a pure haircut on a
common underlying policy value, not a different policy value — so a model needs one `V(t)`
and one multiplier, not two reserve runs.

Three consequences follow, and all three are contractual rather than incidental:

**Everything derived from the surrender value is suppressed with it.** The 払済保険金額, the 契約者貸付
amount and the 自動振替貸付 amount are all computed off `CV(t)`, so during the suppressed period
all three are 30% smaller [S7] [S9] [S11]; where 延長定期保険 exists the solved term is
correspondingly shorter [S7]. The APL consequence is the sharp one and is developed below.

**Conversion during the period is permanent.** Converting to 払済保険 switches the suppression
off for the future — one carrier's article says so in terms — but the conversion *itself* is
made on the suppressed value, so the resulting 払済保険金額 is permanently smaller [S3] [S7] [S9].

**A clawback survives the step.** If not all premiums falling in the suppressed period were
paid, the suppressed basis continues to apply after the period ends [S3] [S4] [S5] [S9]. A
policy carried through the low period by APL advances that were never repaid does not
necessarily get the full step-up.

The price of the suppression is disclosed at one carrier, which publishes both premium
scales for one identical model point: ¥17,040/month suppressed against ¥20,350/month
ordinary — the suppressed form costs **83.7%** of the ordinary one [S7]. That is the trade
the product makes, and a model that suppresses the value without discounting the premium
mis-prices it.

One carrier applies the factor only to the guaranteed part of the value on an 積立利率変動型
chassis: the low-period surrender value is 70% of the surrender value on the 基本保険金額 part
plus an **unsuppressed** amount derived from the excess of the actual 積立金 over the
予定利率-based 積立金 [S11]. That split belongs to the
[FX whole life (外貨建終身保険)](../fx_whole_life/product-spec.md), which inherits this chassis and
adds the crediting-rate layer; it is named here so that the inheritance is explicit.

### Premium payment, grace, and why lapse is a funded event

Premiums are due at the 払込期月 for the chosen mode. Non-payment starts the 猶予期間, which on the
composite runs to the end of the month following the 払込期月 for 月払 and to the monthly 契約応当日 in
the month after that for 半年払 and 年払, with named end-of-month substitutions [S1] [S3] [S10].
What happens at the end of grace is where Japanese whole life departs from every product in
`uslib` and `uklib`.

Automatic premium loan (*jidō furikae kashitsuke*, **自動振替貸付**). Where the premium is unpaid
at grace expiry and the contract has a surrender value, the insurer **lends the premium
against that value and applies it to the premium**, and the contract continues in force [S1]
[S3] [S7] [S10] [S11]. The advance is deemed made at the moment grace expires [S1] [S3] [S7]
[S10]. The test, stated the same way at three carriers, is:

    the APL fires at t if   CV*(t) - L(t) >= A + interest on A to the next roll-in
      where CV*(t) is the surrender value computed AS IF the premium had been paid,
            L(t)   is the existing loan and APL principal and interest,
            A      is the amount advanced.

One carrier extends the base from `CV` to `CV + 未経過保険料` [S7]. If the test fails, the
contract lapses; if it passes, it does not. **Lapse on this chassis is therefore a funded
event, not a behavioural one.** A policy does not lapse while the cash value can carry the
premium — which means a whole life lapse model that applies a lapse rate without first
testing the APL condition is modelling a decrement the contract does not have.

The amount advanced per event varies: three months' premium at a time on 月払 at one carrier,
falling back to the largest number of months that can be funded [S1]; the premiums from the
month due to the day before the next half-yearly anniversary at another [S10]; simply the
premium due at two more [S3] [S7]. Two carriers add a **downgrade rule** on 年払 contracts —
where the value cannot fund the annual premium plus interest but can fund a half-yearly one,
the mode is switched to 半年払 and the half-yearly premium is advanced [S3] [S10].

The balance rolls up at compound interest, with the interest capitalised into principal at
each subsequent grace expiry (annually on 年払) [S3] [S7]; one carrier adds a rule for the
post-払込満了 period, rolling interest in on the day after the payment period matures and
annually thereafter [S10]. On the annual grid the recursion is simply

    L(t+1) = (L(t) + A(t)) * (1 + i_L)

with `A(t) = P` when the APL fires at `t` and zero otherwise.

An advance already made is **unwound** — treated as never having happened — if the
policyholder requests 解約, 減額 or conversion to 払済保険 within three months of the day after
grace expiry [S1] [S3] [S10]. One carrier's list also includes rider surrender and reduction
[S3].

**The interaction with the cliff is the most important single fact in this document.**
During the 低解約払戻期間, `CV(t) = 0.70 × V(t)`, so the APL test is run against 70% of the value.
The number of premiums the contract can self-fund before the test fails is materially
smaller than on the ordinary form, and it is smallest exactly where policyholders are most
likely to stop paying — early duration, when `V(t)` is small anyway. A 低解約返戻金型 policy is
simultaneously the one with the strongest incentive to persist to 払込満了 and the one with the
least APL headroom to get there. Any model of this product that omits the APL, or that runs
it off the unsuppressed value, gets both the lapse timing and the loan balance wrong.

**Loan-driven termination.** Where `L(t)` exceeds `CV(t)` the insurer notifies for a top-up,
and if it is not paid by the end of the month following the month the notice issued, the
contract lapses from the next day [S1] [S3] [S10]. A policy lapsed this way can be
reinstated only on payment of an additional company-set amount [S1] [S10]. One carrier does
not lapse the policy for an unpaid loan at all: it applies the loan principal and interest
against the 積立金 and **reduces the 基準保険金額** instead — and on a 低解約返戻金型 contract before 払込満了
it applies them against 0.7 × 積立金, so the sum-assured reduction is correspondingly larger
and exceeds the loan balance [S9]. That is a genuinely different termination mechanic and it
is out of the composite.

### 復活, 払済保険 and 減額

**復活.** Within three years of lapse, on fresh 告知 and payment of the arrears, the contract is
restored; cover attaches when the arrears (and, where the declaration comes later, the
declaration) are received [S1] [S3] [S10]. Reinstatement is barred once the surrender value
has been claimed [S1] [S3] [S10]. The 責任開始期 resets, restarting the suicide and
contestability clocks [S1] [S7] [S9] [S10].

**払済保険.** The surrender value net of `L(t)` is applied as a single premium to a reduced sum
assured on a company-defined basis [S1] [S3] [S7] [S9] [S10]:

    SA_paid_up(t) = (CV(t) - L(t)) / A(x + t)

where `A(x+t)` is a whole-life single-premium net rate on the insurer's own basis. The term
stays 終身 and cover continues for life [S3] [S7]. Riders terminate on conversion, except
those a carrier names — one keeps the living-needs and proxy-claimant 特約 [S7]; two terminate
riders outright [S1] [S3]. Eligibility differs: three years of premiums paid and the
contract still inside 保険料払込期間 at one carrier [S10]; two years in force at another [S9]; only
a floor on the resulting sum assured at two more [S1] [S3]. Conversion is irreversible at
one carrier [S3] and reversible within three years by 復旧 at another [S7].

**減額.** Reducing the sum assured is universal and is treated as a partial surrender: the
reduced portion pays the corresponding surrender value [S1] [S3] [S9] [S10] — on the
suppressed basis if the reduction is made during the low period [S9].

### 契約者配当

On the 無配当 composite there is no dividend layer at all: one carrier's 約款 says so in a
dedicated article, and every rider in that booklet repeats it [S1]. On the participating
variant, the legal frame is 保険業法第114条 (any distribution provided for in the 約款 must follow
the fair-and-equitable standard set by ordinance) and 施行規則第30条の2, whose second permitted
method — identifying the distributable amount **by the cause in which it arose** — is the
legal footing of the three sources of surplus (*san-rigen*, 三利源: 死差 mortality, 利差 interest,
費差 expense) framing [R5] [R6] [REG-R9]. The limit stated honestly: neither the ordinance nor
the supervisory guideline names 死差, 利差 or 費差 — 三利源 is Japanese actuarial and industry
practice, and this library uses the vocabulary without attributing it to a regulatory text
[REG-R9]. In practice on a 5年ごと利差配当 design a dividend is declared every five years from
inception where the investment return on 責任準備金等 exceeds the return assumed in pricing, and
while the contract continues it accumulates at a company-set rate as 5年ごと積立配当金, withdrawable
on request; it is not promised, varies with performance and may be nil, and riders carry
none [S7]. Dividends therefore belong in assumption class (b), insurer-discretionary current
elements — and separating them from guaranteed elements is not a modelling nicety but the
reason a Japanese illustration must split 保証 from 非保証, since presenting a non-guaranteed
element as certain is 断定的判断の提供 under 消費者契約法第4条 [REG-R38].

---

## Riders and options

**In scope (modelled or parameterized):**

- **高度障害保険金** — part of the main contract, same amount, no extra premium; modelled as part
  of the death decrement because the valuation table already includes it [S1] [S3] [S7] [S9]
  [REG-R20].
- **低解約返戻金型** — a model-point flag with a suppression factor and a suppressed period, not a
  separate product [S3] [S6] [S7] [S9] [S11].
- **自動振替貸付** — modelled as an election with a default-on value, with the continuation test
  above; the off position must be exercised in testing [S1] [S3] [S7] [S10] [REG-R14].
- **契約者貸付** — modelled as an available balance and an interest accrual; take-up is a
  **[std]** behavioural assumption with no public data behind it [S1] [S3] [S7].
- **払済保険** — modelled as an election at a policyholder-chosen duration, using the surrender
  value net of loans [S1] [S3] [S7] [S9] [S10].
- **5年ごと利差配当** — parameterized as an insurer-discretionary cash flow, off in the base run
  [S7].
- **リビング・ニーズ特約** — specified and priced at zero, as it is in the market; modelled as an
  acceleration of the death benefit rather than an additional benefit [S1] [S3] [S4] [S7].

**Out of scope:** 延長定期保険 (one carrier only) [S7]; 保険料払込期間の変更 [S1] [S10]; 前納 and ステップ払込方式
[S1] [S10]; 保険料払込免除 and its 特定疾病 extension [S3]; 非喫煙割引特約 (a rating question, not a cash-flow
one) [S1]; 介護前払特約, payable after 払込満了 from age 65 on public 要介護4–5 as a discounted advance
of the death benefit [S3] [S4]; 年金支払移行特約, converting the 責任準備金等 into an annuity or care
benefit after 払込満了 [S7] [S11]; 指定代理請求特約 [S7]; the attachable protection riders (定期保険特約,
逓減/逓増定期保険特約, 家計保障定期保険特約, 災害割増特約, 傷害特約) and the third-sector riders (災害入院特約, 疾病入院特約,
三大疾病関連特約), whose shape belongs to the [medical (医療保険)](../medical/product-spec.md) [S1] [S3] [S7]; 特別条件付保険特約 [S3]; the 倍額保障 and
step-down designs of one carrier [S9]; and the 一時払 and 積立利率変動型 forms, which are scope
boundaries rather than riders — see below.

**Scope boundaries at the edge of this chassis.** Two neighbouring shapes are excluded and
named. Single-premium whole life (**一時払終身保険**) is the same benefit on a single-premium
chassis; it matters because it is the one form whose 予定利率 is publicly disclosed and
refreshed twice a month [S12], and because it sits on the 標準利率's quarterly reset calendar
rather than the annual one [R8] [REG-R10]. **積立利率変動型終身保険** replaces the fixed 予定利率 with a
crediting rate reset monthly off the 10-year JGB 応募者利回り less an explicit asset-management
margin, rounded to 0.01% and floored at the 予定利率, the excess buying ratcheting 増加保険金額 [S11].
It stays inside the 標準責任準備金 regime — 施行規則第68条 excludes contracts whose 約款 lets the insurer
change the *予定利率*, not contracts whose crediting rate floats above a fixed one [R6] [REG-R7]
— and it is the direct ancestor of the [FX whole life (外貨建終身保険)](../fx_whole_life/product-spec.md), which
adds the currency and MVA layers
[REG-R12] [REG-R37].

---

## Variations across insurers

1. **自動振替貸付 — presence and election.** Opt-out at four carriers [S1] [S7] [S10] [S11],
   opt-in at one [S3], absent at two — one has none at all [S8], the other only a requested
   保険料振替貸付 [S9]. Composite: **opt-out**, implemented as an election with a default-on flag,
   because that is the majority position and because the supervisory guideline requires the
   feature to be at the policyholder's election [REG-R14]. This is the single largest source
   of divergence in projected lapse experience across the seven carriers.
2. **What the APL advances, and on what cycle.** Three months' premium at a time on 月払 [S1];
   to the day before the next half-yearly anniversary [S10]; the premium due [S3] [S7]
   [S11]. Interest rolls into principal at each subsequent grace expiry [S3] [S7], with a
   distinct post-払込満了 rule at one carrier [S10]. Composite: **the premium due**, rolled
   annually — the simplest rule consistent with the annual grid, and the rule at two
   carriers.
3. **Grace and what follows it.** One month at four carriers [S1] [S3] [S7] [S10]; **two
   months** at one [S9]; and at one carrier neither grace nor lapse but a scheduled 解除 on
   the monthly anniversary in the third month after the 払込期月, with the surrender value paid
   net of unpaid premiums [S8]. Composite: the four-carrier one-month grace. The 解除 regime
   is not a longer grace — it is a different termination, and it cannot be reversed.
4. **復活 window.** Three years at four [S1] [S3] [S7] [S10]; **one year** at one [S9];
   **none** at the 解除 carrier [S8] — a factor of three across those that offer it, and a
   presence/absence split beyond that. Composite: three years.
5. **Suppression factor and period.** 70% wherever it is published — in the 約款 at two
   carriers [S3] [S9], in the 契約概要 at a third [S7], in the glossary at a fourth [S11]: four
   independent statements and no disagreement. The period is 保険料払込期間 at three [S3] [S7]
   [S11] and "before 払込満了" at the fourth [S9]. A fifth sells a 低解約払戻金型 form whose factor
   could not be read at all, because its special provisions are printed as 「（記載省略）」 in the
   retrieved booklet [S1]. Composite: **0.70 over 保険料払込期間**.
6. **How the suppression is applied on a variable-crediting chassis.** One carrier
   suppresses only the guaranteed part, adding an unsuppressed amount from the excess of the
   actual 積立金 over the 予定利率-based 積立金 [S11]; the others apply one multiplier to the whole
   value [S3] [S7] [S9]. Composite: one multiplier, the split deferred to the
   [FX whole life (外貨建終身保険)](../fx_whole_life/product-spec.md).
7. **契約者貸付 limit.** 9/10 in payment and 8/10 paid up at three [S1] [S3] [S7]; 8/10 less
   three months' premium at one [S8]; an unpublished company formula with a one-year 貸付期間 at
   another [S9]. Composite: 9/10 and 8/10.
8. **What happens when the loan exceeds the value.** Lapse after a month's notice at four
   [S1] [S3] [S7] [S10]; at one, the contract never lapses — the sum assured is reduced
   instead, by applying the loan against 積立金 (or 0.7 × 積立金 during the low period), so the
   reduction exceeds the loan balance [S9]. Composite: lapse, with the reduction mechanic
   named and excluded.
9. **Participation.** 無配当 at three [S1] [S3] [S5] [S11], 5年ごと利差配当 at a fourth [S7], 5年ごと配当
   at a fifth [S10], 有配当 at a sixth [S8], participating with a dividend chapter in the 約款 at
   a seventh [S9]. Composite: 無配当 base, 5年ごと利差配当 as an off-by-default variant.
10. **払済保険 eligibility, and whether it can be undone.** A floor on the resulting sum assured
    only, at two [S1] [S3]; two years in force at one [S9]; three years of premiums paid and
    still inside 保険料払込期間 at another [S10]; and reversibility split — irreversible at one
    [S3], 復旧 within three years at another [S7]. Composite: available from any duration with
    a sum-assured floor, irreversible.
11. **延長定期保険.** Offered by exactly one of the seven [S7]; no such article appears in five
    other carriers' retrieved 約款 [S1] [S3] [S8] [S9] [S10], and it was not in the chapters
    retrieved from the seventh [S11]. Composite: excluded. This is the clearest case in the
    file where a feature a US or UK reader would expect to be standard is not.
12. **Death-benefit shape and issue limits.** Level for life at six carriers; one sells a
    step-down design halving the benefit after 払込満了 and a doubling on accidental death or a
    listed 感染症 [S9]. Issue envelopes are published as a full grid at one carrier [S5], as a
    statutory 加入限度額 at another [S9], and not at all at a third [S1]. Composite: level
    benefit, one carrier's published grid.
13. **What does not vary.** Uniform wherever the retrieved documents state it, and at every
    one of the seven carriers for the first three: a 終身 term with no maturity benefit and no
    満期保険金 [S1] [S3] [S5] [S7] [S8] [S9] [S10] [S11]; a death benefit and a 高度障害保険金 at the
    same amount, the second extinguishing the contract [S1] [S3] [S7] [S9]; a **three-year**
    suicide exclusion measured from the 責任開始期 and reset on 復活, at six of the seven [S1] [S3]
    [S7] [S8] [S9] [S10]. Also without observed disagreement: a **two-year** contestability
    window [S1] [S7] [S9]; payment of the 保険料積立金 rather than nothing where a benefit is
    refused for an 免責事由 [S1] [S9] [S10]; a surrender value that is a function of elapsed and
    paid months [S1] [S3] [S10]; 減額 treated as a partial surrender [S1] [S3] [S9] [S10];
    払済保険 available in some form wherever the retrieved documents address it [S1] [S3] [S7]
    [S9] [S10] [S11]; 契約年齢 on 満年齢 with the fraction discarded, incrementing on the 契約応当日
    rather than the birthday [S1] [S3] [S9]; and 月払 / 半年払 / 年払 as the mode set [S1] [S3]
    [S5] [S9] [S10]. Those are the invariant core of the composite, and every one is a fact
    a model can rely on without a [std] tag.

---

## Regulatory context

**Prudential — ESR, and what it replaced.** From **31 March 2026** Japanese insurers are
supervised on economic-value-based solvency regulation, **ESR** (*keizai-kachi bēsu no
soruvenshī kisei*, 経済価値ベースのソルベンシー規制), a three-pillar regime in which assets
are at fair value and liabilities are current estimate (*genzai suikei*, 現在推計) plus MOCE,
re-measured at each 基準日 on assumptions re-set then and discounted on a prescribed yield
curve, calibrated in principle to **99.5%**. Early corrective action triggers when the ESR
falls below **100%**, replacing the old SMR (*soruvenshī mājin hiritsu*, ソルベンシー・マージン比率)
**200%** trigger [REG-R15] [REG-R17]. The change matters to this product specifically: the
old basis was **ロックイン** — mortality, lapse and interest fixed at issue — and a 終身保険 written
today has a run-off measured in decades, so a re-projectable, assumption-parameterized
liability model of exactly the kind this library builds is the operative artefact rather
than a one-off pricing exercise [REG-R15]. `jplib` computes neither ratio; the
standard-formula coefficients sit in 告示 that were not opened in the research pass and are
[unverified] [REG-R16].

**Statutory reserving — cited, not reproduced.** 保険業法第116条 obliges an insurer to hold 責任準備金
and empowers the Prime Minister to prescribe the accumulation method and the level of the
assumed coefficients for long-term contracts [R5] [REG-R4]. 施行規則第68条 says which contracts
are in scope — a level-premium 終身保険 with a fixed 予定利率 is [R6] [REG-R7] — and 第69条 splits the
reserve into 保険料積立金, 未経過保険料, 払戻積立金 and contingency reserve (*kiken junbikin*, 危険準備金), with a
floor of net level premium method (*heijun jun-hokenryō-shiki*, 平準純保険料式) for anything out of
scope [R6] [REG-R8]. 平成8年大蔵省告示第48号 sets the method (平準純保険料式, no Zillmer adjustment), the
table (生保標準生命表2018（死亡保険用）for contracts from 1 April 2018) and the 標準利率 machinery, which for
ordinary contracts resets off a 1 October 基準日 against the lower of the 3-year and 10-year
means of 10-year JGB issue yields, with banded safety coefficients, a 0.5% trigger, 0.25%
granularity and effect from the following 1 April [R7] [R8] [REG-R10] [REG-R11]. **The
current numeric 標準利率 could not be established from any retrieved official document**, and
the 安全率係数 table for the annual case is printed as 「［表略］」 in the retrieved redline [R8] — so
any 標準利率 figure downstream is [std] or [unverified], never asserted. 価格変動準備金 is asset-driven
and out of scope [REG-R3]. This library projects gross cash flows and builds none of these
reserves.

What the regime asks a liability model for is set by 保険業法第121条第1項第1号, which requires the
appointed actuary (保険計理人) to confirm in an 意見書 that the reserve is soundly accumulated
[REG-R6]; the IAJ practice standard turns that into the **1号収支分析**, a forward
income-and-outgo analysis over **at least ten future years** by product segment, under
prescribed deterministic scenarios or a stochastic set, with sufficiency tested over the
first five [REG-R22]. That is the shape of this product's projection: per-policy premiums,
claims, expenses, surrenders and loan movements over a long horizon, re-runnable on a re-set
basis.

**Mortality basis.** 生保標準生命表2018（死亡保険用）is the statutory valuation table here [R1] [REG-R10]
[REG-R11] [REG-R18], and — in sharp contrast with the subscriber-restricted CMI tables
`uklib` had to proxy — it is published in full, free, at a stable public URL. Two
qualifications must both be kept. It is a **valuation** table: 2008/2009/2011 experience,
carried forward by an improvement allowance of 2.5% p.a. for five years then 1.0% p.a. for
three, then loaded by a 数学的危険論による補整 sized to hold the probability of experience exceeding
the projected variation to about 2.28% (a 2σ level), capped at 130% of the unadjusted rate
[R2] [REG-R20] — so a best-estimate basis is a **[std]** adjustment *of* a sourced table,
and each document says which of the two it means. And the IAJ's site terms prohibit
reproduction and transmission to third parties without written consent [REG-R21], so `jplib`
cites the tables by URL, quotes only the rates its worked example needs, and ships
`mort_table.csv` as a **[std]** construction whose `provenance` column points at the IAJ
entries. The terminal age on the male 死亡保険用 basis is **109** — a hard parameter for a
whole-life projection, which terminates there [R1] [REG-R18]. The table is built for a
nearest-birthday insurance age (*hoken-nenrei*, 保険年齢) basis while this product ages on 満年齢
[REG-R20] [S1] [S3]; the difference
is handled in `technical-notes.md`.

The division that shapes this library's tagging is statutory: the 予定利率, 予定死亡率, 予定事業費率 and
the surrender-value formula live in the 保険料及び責任準備金の算出方法書, one of the four 基礎書類 filed under
保険業法第4条第2項 and **not published**, while the 約款, the ご契約のしおり and the パンフレット are [REG-R2]. No
amount of further research converts footnote 8 or footnote 15 into a sourced value.

**Conduct and classification.** The supervisory guideline names **低解約返戻金型 products** among
those needing extra explanation at the point of sale (IV-1-9), requires 解約返戻金 to be
disclosed clearly — the amount on the policy schedule or the method in the 約款 (IV-1-10) —
and requires a 契約者貸付 limit reasonable against the surrender value with over-loan prevention,
and a 自動振替貸付 to be **at the policyholder's election** with prompt notice when exercised
(IV-1-12) [REG-R14]. The statutory duty to explain a **restriction on cancellation** before
sale is what makes the suppression period a disclosable feature rather than a pricing detail
[REG-R39], and presenting a non-guaranteed dividend as certain is 断定的判断の提供 [REG-R38]. A yen,
fixed-予定利率 終身保険 is **not** a 特定保険契約 under 保険業法第300条の2 — that classification and its
FIEA-grade conduct rules attach to the 外貨建 and 変額 designs [REG-R37]. クーリング・オフ is eight days
on a dispatch rule and is scoped out [REG-R36]. On insurer failure, contracts are covered up
to **90% of the 責任準備金** at the failure date, the rate set by ordinance under 保険業法第270条の3;
the reduced rate for 高予定利率契約 is [unverified] [REG-R40] [REG-R41].

**Tax.** Two regimes drive design here. **Inheritance tax:** a death benefit is deemed
acquired by inheritance in the proportion of the premiums the decedent bore (相続税法第3条第1項第1号)
and is exempt for heirs up to **¥5,000,000 × the number of statutory heirs** (第12条),
apportioned pro rata above the limit [R9] [REG-R44]; renouncing heirs are counted as if they
had not renounced, adopted children are capped, and a non-heir recipient gets no exemption
at all [R10] [REG-R45]. **Premium deduction:** the premium sits in the 一般の生命保険料 basket of
the post-2012 three-basket regime, deductible on a banded schedule to ¥40,000 per basket
with an overall income-tax cap of ¥120,000 [R11] [REG-R43]. A surrender received by the
premium payer is 一時所得 — proceeds less premiums paid less a ¥500,000 特別控除, of which half
enters taxable income [REG-R46] — which is one reason the surrender decision on a 低解約返戻金型
contract is not driven by the cliff alone. `jplib` models contractual cash flows, not the
policyholder's tax position.

**Professional standards and the accounting frame.** The basis any model uses is
professionally owned by the 保険計理人 appointed under 保険業法第120条 [REG-R5], working to the IAJ's
実務基準 [REG-R22]; the tables that bind the statutory reserve are produced by the IAJ as the
指定法人 designated under 保険業法第122条の2 and commissioned by the FSA [R4] [R5]. The frame a reader
arriving from `uklib` or `uslib` must not import: **IFRS 17 is not mandatory in Japan** —
IFRS applies as 指定国際会計基準 on a voluntary basis [REG-R47]. J-GAAP statutory reserving, the ESR
economic balance sheet and IFRS 17 are three separate bases over one set of projected cash
flows, and this product keeps the cash flows basis-agnostic, with discounting, margins and
tax layered on top.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-whole_life-r1
[R10]: #jplib-whole_life-r10
[R11]: #jplib-whole_life-r11
[R12]: #jplib-whole_life-r12
[R2]: #jplib-whole_life-r2
[R4]: #jplib-whole_life-r4
[R5]: #jplib-whole_life-r5
[R6]: #jplib-whole_life-r6
[R7]: #jplib-whole_life-r7
[R8]: #jplib-whole_life-r8
[R9]: #jplib-whole_life-r9
[REG-R1]: #jplib-reg-r1
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R12]: #jplib-reg-r12
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R16]: #jplib-reg-r16
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R3]: #jplib-reg-r3
[REG-R31]: #jplib-reg-r31
[REG-R32]: #jplib-reg-r32
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
[REG-R9]: #jplib-reg-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
