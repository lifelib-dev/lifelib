# Product Specification

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** This is a *standardized composite specification* of Japanese endowment
assurance (*yōrō hoken*, 養老保険) together with educational endowment (*gakushi hoken*, 学資保険) as
a second model cell, assembled for reference liability cash-flow modeling. It does not
describe any single insurer's product. Facts carrying a source tag — [S#] (primary product
documents: policy conditions (*yakkan*, 約款), ご契約のしおり, 商品パンフレット and published rate releases)
and [R#] (regulatory and actuarial references), both numbered per `_research/endowment.md`
and resolved in `sources.md` (same directory; numbering frozen, never renumbered), and
[REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) —
were extracted from the cited document. Values marked **[std]** are standardizations
introduced for the reference implementation; each [std] table row carries a numbered
footnote giving the rationale and, where one exists, the observed range across insurers.
Facts the research pass could not verify are flagged [unverified]. The composite is drawn
from six carriers: three publishing on both products [S2]–[S5], [S6]–[S9] and [S13]–[S15],
and three publishing on 学資保険 alone [S1], [S10]–[S12] and [S16]. Two full 養老保険 約款 [S2] [S8]
and four full 学資保険 約款 [S1] [S3] [S6] [S10] were read.

**This product inherits the library's savings chassis by reference.** The policy value
(*hokenryō tsumitatekin*, 保険料積立金), surrender value (*kaiyaku-henreikin*, 解約返戻金), policy loan
(*keiyakusha kashitsuke*, 契約者貸付), automatic premium loan (*jidō furikae kashitsuke*,
自動振替貸付, APL), grace (*yūyo kikan*, 猶予期間), lapse (*shikkō*, 失効), reinstatement (*fukkatsu*, 復活)
and reduced paid-up (*haraizumi hoken*, 払済保険) machinery is specified once, in the
[whole life product specification (終身保険)](../whole_life/product-spec.md), and is **not restated here**.
What this document adds is what is genuinely this product's: a **finite 保険期間** with a
**maturity benefit (*manki hokenkin*, 満期保険金) equal to the death benefit**, and — on the
second cell — a maturity benefit split into staged education money
(*gakushikin*, 学資金), an advertised return ratio (*henreiritsu*, 返戻率), a death
benefit that is a return of premiums rather than a sum assured, and above all
**waiver of premium (*hokenryō haraikomi menjo*, 保険料払込免除) on the death or
severe disability of the policyholder (*keiyakusha*, 契約者) — a decrement on a life
who is not the insured**, after which the policy continues and pays every benefit with no
further premium. That last mechanic has no analogue anywhere in `uslib` or `uklib` and is
given full treatment below.

---

## Product overview and market role

養老保険 is a fixed-term contract that pays a death benefit (死亡保険金) on death within the 保険期間 and
a 満期保険金 on survival to the end of it, **with the two amounts equal** [R10] [S2] [S8]. The
equality is not a convention but the literal drafting: both cells of the 約款 benefit table
read 基準保険金額 at one carrier [S2] and 保険金額 at the other [S8]. It is a first-sector (*dai-ichi
bun'ya*, 第一分野) contract — fixed-sum insurance on human survival or death under 保険業法第3条第4項第1号
[REG-R1] — so its statutory valuation basis is 生保標準生命表2018（死亡保険用）for contracts concluded
from 1 April 2018 [REG-R10] [REG-R11] [R1], the same table as the whole-life chassis it
inherits.

The consumer taxonomy is blunt about what this buys: 養老保険 carries a savings function, but
the maturity benefit **can fall short of total premiums paid** [R10]. On the one carrier
that publishes a rate, it does. At the published cell — 契約年齢 30, 満期 60, 保険金額 ¥5,000,000,
male, 月払 ¥15,095 for contracts dated on or after 2025-01-02 — thirty years of premiums total
¥5,434,200 against a ¥5,000,000 maturity benefit, a ratio of **92.0%** (derived from [S9]).
That is the product's honest arithmetic at a 1.00% assumed interest rate (*yotei riritsu*,
予定利率) [S9], and it is why 養老保険 has become a small line.

**Market position: small on every published measure.** For FY2024, 養老保険 was ¥1.5347
trillion of new business sum assured, **2.7%** of the individual total — which the source
publishes as shares rather than as a total, the shares implying about ¥57 trillion (derived
from [R9]) — against 43.2% for 定期保険 and 22.8% for 終身保険; in force it was 7.34 million policies
(**3.8%** of 195.30 million) and ¥27.0379 trillion of sum assured (**3.5%** of ¥778.9902
trillion). こども保険 — the statistical category holding 学資保険 — was ¥347.7 billion of new
business sum assured, **0.6%** [R9] [REG-R31]. Both lines sit an order of magnitude below
医療保険 (23.3% of in-force policy count) and 終身保険 (19.7%) [R9]. The industry 解約・失効率 was
**5.6%** of opening in-force sum assured, but that is an amount-weighted, all-product figure
and no retrieved source gives a lapse curve by duration, or anything specific to either line
[R9] [REG-R31] — so the lapse basis here is **[std]** and says so.

**学資保険 is the same chassis with two substitutions, and it is bought for a different
reason.** The survival benefit is split into instalments timed to school entry, and the
premium stream is made contingent on the survival of the **policyholder** — normally a
parent — rather than of the insured child [S1] [S3] [S7] [S10] [S13] [S16]. The connection
between the two products is explicit in one carrier's contract: converting a 学資保険 to 払済保険
turns it into "a paid-up 養老保険 of the same term", after which the 祝金 and the death benefit
cease and only a maturity / death / 高度障害 benefit equal to the 払済保険金額 remains [S10]. The
product is sold on a single number, the **返戻率**: total receipts divided by total premiums,
published between **105.8%** (derived from [S7] [S9]) and **131.3%** [S12] across the six
carriers. That premium over 100% is not a better interest basis — the same carrier prices
学資保険 and 養老保険 at the same 1.00% 予定利率 [S9] — it is the near-absence of a mortality cost on a
child, together with a premium-paying period that ends years before the benefits are paid.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Guaranteed-premium 養老保険; 死亡保険金 = 満期保険金 = 基準保険金額 over a fixed 保険期間; non-participating (*mu-haitō*, 無配当) composite | [R10] [S2] [S8]; participation **[std]** (1) |
| Second cell | 学資保険 on the same chassis: the maturity benefit split into staged 学資金, the death benefit replaced by a return of premiums, and 保険料払込免除 on the 契約者 | [S1] [S3] [S7] [S10] [S13] [S16] |
| Regulatory class | 第一分野, 保険業法第3条第4項第1号 | [REG-R1] |
| 保険期間 — 養老 cell | Observed 10–60 years in one-year steps; composite **30 years** (歳満期 at age 60) | [S4] [S9]; pick **[std]** (2) |
| 保険期間 — 学資 cell | Observed 17 / 18 / 20 / 21 / 22歳満期; composite **22歳満期** | [S1] [S5] [S10] [S14] [S16]; pick **[std]** (3) |
| 保険料払込期間 | 養老: equal to 保険期間. 学資: observed to ages 5 / 10 / 11 / 12 / 14 / 15 / 17 / 18 and 全期間; composite **17 years** | [S4] [S5] [S10] [S11] [S14] [S16]; pick **[std]** (3) |
| 契約年齢 — 被保険者 | 養老: observed 6–75; composite 30. 学資: observed 0–12 by course, 0–7 in the adopted 祝金 grid; composite **0** | [S15] [S5] [S10] |
| 契約年齢 — 契約者 (学資 cell only) | Observed 18–65 at two carriers, one stating that the upper limit moves with market rates; composite **30** | [S5] [S14] |
| Age basis | Attained age (*man-nenrei*, 満年齢) at 契約日 with the fractional year resolved by the carrier's own rule; the rating age then increments at each 年単位の契約応当日, not on the birthday | [S1] [S2] [S10] [S13]; rounding **[std]** (4) |
| 基準保険金額 | 養老: ¥1,000,000–¥10,000,000. 学資: ¥500,000–¥7,000,000 (¥5,000,000 on some courses) | [S4] [S5] |
| Sex | Rated separately; on the one published 養老保険 cell the female premium is 99.3% of the male (¥14,990 against ¥15,095) | [S9] |
| Lives basis | Single insured life. **On the 学資 cell the 契約者 is a second life and is not the insured** | [S1] [S10] |
| **Anchor model cell** | 養老保険: male, 契約年齢 30, 保険期間 30年 (満期 at 60), 保険料払込期間 30年, 基準保険金額 ¥5,000,000 = 死亡保険金 = 満期保険金, 月払保険料 ¥15,095, annualized **¥181,140** | [S9]; annualization **[std]** (5) |
| Second model cell | 学資保険: 契約者 male 30, 被保険者 (child) 0, 22歳満期, 保険料払込期間 17年, 基準保険金額 ¥1,000,000, S型 祝金 grid, 月払保険料 ¥9,047, annualized **¥108,564** | [S10] [S11]; grid **[std]** (6) |

Footnotes to [std] rows:

1. Participation splits four to two. Participating: 有配当 (社員配当) at one carrier on both
   products [S6] [S8]; annual plus long-duration 契約者配当 on its 養老保険 at a second [S2];
   ５年ごと配当付 at a third [S1] and a fourth [S10]. Non-participating: **no dividend at all** at
   a fifth [S13] and 無配当 at a sixth [S16]. The
   third 養老保険 carrier does not publish its dividend class [S15]. The composite takes 無配当,
   because a dividend is an insurer-discretionary element under 施行規則第30条の2 and must not
   sit inside a guaranteed cash flow [REG-R9]. The ５年ごと配当 variant is specified here and
   **not implemented**: the model carries a `dividend_type` attribute and rejects the
   value by name, which is a harder line than the savings chassis takes — that chassis
   declares the dividend on a [std] spread, and no retrieved document on *this* product
   publishes a scale, a 配当基準 or a 三利源 split to calibrate one against.
2. Only one carrier publishes a 養老保険 term envelope at all: 10–60 years selectable in
   one-year steps, with 基準保険金額 ¥1,000,000–¥10,000,000 [S4]. A second publishes 被保険者 issue
   ages 6–75 varying with the term but no terms and no amounts [S15]; the third's 給付約款
   carries no age or term table at all [S8]. The composite takes 30 years because that is
   the term of the only model point in the set for which a premium is actually published —
   契約年齢 30 to 満期 60 [S9] — so the whole anchor cell is sourced rather than assembled.
3. On the 学資 cell the envelope is wide and every carrier sits inside it differently:
   maturity at 18 or 22 at one [S1]; 17 / 18 / 21 at a second [S5]; an elected 学資年金開始年齢 with
   five annual instalments at a third [S7]; 22 at a fourth [S10]; 21 at a fifth [S14]; and
   17 / 18 / 20 / 22 at a sixth [S16]. Premium-paying periods run to ages 5, 10, 11, 12, 14,
   15, 17 and 18, or the whole term [S5] [S10] [S11] [S14] [S16]. The composite takes 22歳満期
   with a 17-year paying period because it is the one combination for which a carrier
   publishes receipts, monthly premium, total premiums **and** 返戻率 together [S11], which
   makes the entire cell checkable by arithmetic rather than assertion.
4. Four different rounding rules are observed for 満年齢 at 契約日: months counted from the birth
   month, rounded up at ≥ 7 and down at ≤ 6 [S2]; rounded up above 6 months and down at ≤ 6
   [S1]; **truncated** [S10]; and truncated [S13]. All four then add one year at each
   年単位の契約応当日 [S1] [S2] [S10] [S13]. The composite truncates, matching the savings chassis.
   Both model cells are at exact integer ages at issue, so the rule does not bind on either
   — it is recorded because it does bind on any model point built off a real date of birth.
5. `Endowment_JP_A` runs on an annual grid, so the annual premium is standardized as 12 ×
   the published monthly figure: 12 × ¥15,095 = ¥181,140. No carrier publishes an
   annual-mode premium for this cell, so the modal discount a real 年払 scale would carry is
   **not** applied and the annual premium is slightly overstated; the direction of the error
   is stated in `technical-notes.md` rather than hidden. The cell reconciles end to end: 30
   × ¥181,140 = ¥5,434,200 of premiums against a ¥5,000,000 maturity benefit, a ratio of
   92.0% (derived from [S9]). ¥5,000,000 is exactly one statutory heir's worth of the
   inheritance-tax exemption [REG-R44]. It is **not** claimed to sit in any particular band
   of the national survey: that entry publishes 世帯普通死亡保険金 as a banded distribution rather
   than a mean, and its bands were not read [REG-R32], so the survey supports the statement
   that a household sum-assured distribution exists to check a model point against and no
   statement about where this one falls in it.
6. Total receipts as a percentage of 基準保険金額 vary four-fold across the six carriers — 100% /
   130% [S3], 150% / 200% [S1], 200% / 210% [S10], 300% / 360% [S7] and 400% [S13] — because
   the carriers scale the 基準保険金額 differently, not because they pay differently in yen. The
   composite adopts the **S型 grid at child 契約年齢 0–1** [S10]: 5% / 5% / 10% / 10% / 70% / 10%
   of 基準保険金額, then 満期保険金 100%, totalling 210%. It is chosen because it is the only grid in
   the set that is written in the 約款 as an explicit percentage table **and** has a published
   plan behind it whose arithmetic closes: 12 × ¥9,047 × 17 = ¥1,845,588 of premiums against
   ¥2,100,000 of receipts [S11]. The J型 alternative at the same carrier — a single 祝金 of
   100% at one date, then 満期保険金 100% [S10] — is retained as the degenerate variant, because
   a grid collapsing to two payments is the sharpest test that the schedule is data and not
   code.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level and guaranteed for the whole of 保険料払込期間; no review mechanic in any retrieved 約款 | [S1] [S2] [S8] [S10] |
| Mode (払込回数) | 月払 / 半年払 / 年払 / 一時払 in the taxonomy; one carrier's 学資 base contract offers monthly and annual only. Composite default 年払 | [R10] [S1] [S6] [S10]; default **[std]** (7) |
| 予定利率 | **1.00% p.a. on both cells**, for contracts dated on or after 2025-01-02 (学資保険 0.85% → 1.00%; 養老保険（一時払を除く）0.60% → 1.00%) | [S9]; adoption **[std]** (8) |
| 予定死亡率 / 予定事業費率 | Not published — they live in the 保険料及び責任準備金の算出方法書, a filed but unpublished 基礎書類 | [REG-R2]; **[std]** (8) |
| Volume bands (高額割引) | Observed as a three-band unit rate per ¥100,000 of 基準保険金額 and as a flat ¥30 per ¥100,000 above ¥700,000. Out of scope | [S7] [S13]; scope **[std]** (9) |
| 前納 / 一括払込 discounts | 3–12 months of monthly premiums together, and 前納 of two or more years; the discount rates are company-set and unpublished. Out of scope | [S1] [S2] [S6] [S10]; scope **[std]** (9) |
| Prenatal entry (出生前加入) | Cover from 140 days before the expected date of birth, with the child's 契約年齢 set to 0; a stillbirth voids the contract and refunds premiums. Out of scope | [S3] [S10] [S13] [S14] [S16]; scope **[std]** (9) |
| 保険料払込免除 — 養老 cell | On the **insured's** 重度障害 in the main contract at one carrier, and as an attachable 保険料払込免除特約 — a rider (*tokuyaku*, 特約) rather than part of the main contract (*shu-keiyaku*, 主契約) — at another. Off in the base run | [S2] [S8] [S15]; scope **[std]** (10) |
| 保険料払込免除 — 学資 cell | On the **契約者's** death, 高度障害, or 身体障害 from a listed accident within 180 days. **In the main contract and on by default** | [S1] [S3] [S10] [S13] [S16]; trigger set **[std]** (11) |

7. Modes are 月払 / 半年払 / 年払 / 一時払 in the neutral taxonomy [R10] and 月払 / 半年払 / 年払 in the 約款
   at three carriers [S1] [S2] [S10], with one carrier's 学資 base contract restricted to
   monthly and annual [S6]. Every published premium in the set is a monthly figure [S9]
   [S11] [S13] [S16]. The model is annual-step, so the composite pays annually at 12 × the
   monthly figure (footnote 5). One carrier states the sales point plainly — paying in
   larger blocks lowers total premiums and raises the 返戻率 [S16] — and a second's highest
   published ratio, 129.2%, is quoted on a 一括払込 basis [S14]. The modal loading is therefore
   real, material to the number the product is sold on, and unpublished; applying one would
   be an invention.
8. **This is the one place `jplib` is better supplied than its whole-life chassis.** The
   予定利率 for both cells is published by name, by product group, before and after a dated
   revision: 学資保険・こども保険 0.85% → 1.00% and 養老保険（一時払を除く）0.60% → 1.00%, effective for contracts
   dated on or after 2025-01-02, described by the carrier as the first 予定利率 increase in
   about forty years [S9]. Only one of the six publishes it, so *adopting* it as the
   composite basis is the standardization — the number itself is sourced. The other two legs
   of the pricing basis stay dark: the 予定死亡率, the 予定事業費率 and the surrender-value formula sit
   in the 算出方法書, one of the four 基礎書類 filed under 保険業法第4条第2項 and not published [REG-R2]. The
   statutory standard valuation rate (*hyōjun riritsu*, 標準利率) is a different rate on a
   different calendar, set by 平成8年大蔵省告示第48号 off the lower of the three-year and ten-year
   average 10-year JGB yield and determined annually [R4] [REG-R10]; **its current numeric
   value could not be established from any retrieved official document** [R4] [R5], so no
   標準利率 figure is asserted anywhere in these documents.
9. Three premium-side refinements are specified and excluded together, because each needs an
   unpublished rate to model and none changes a mechanic this product exists to demonstrate.
   The **volume bands** are real and asymmetric — one carrier's 学資保険 unit rate per ¥100,000
   of 基準保険金額 is ¥1,313 at ¥1,000,000 and above, ¥1,343 from ¥700,000, and ¥1,373 below that
   [S7], and a second discounts ¥30 per ¥100,000 monthly at ¥700,000 and above with nothing
   below [S13]; the consequence worth recording is that a **減額 can push a policy into a
   worse rate band** [S13]. The **前納 discounts** are stated at four carriers without a rate
   [S1] [S2] [S6] [S10]. **出生前加入** is standard at four [S3] [S10] [S13] [S16] but starts
   cover on a life that does not yet exist, which is a model-point question rather than a
   cash-flow one.
10. On the 養老 cell the waiver is not universal and not aimed at the same life: one carrier
    writes it into the main contract on the **insured's** 重度障害, and separately and very
    narrowly on the **policyholder's accidental death** where the policyholder is the
    insured's parent, grandparent or elder sibling and the child is under 10 [S2]; the
    second carrier puts it in an attachable 保険料払込免除特約 instead [S8]; the third does not
    publish [S15]. The composite leaves it off in the base 養老 run, because 高度障害 is already
    inside the death rate of the statutory valuation table [REG-R20] and adding a separate
    disability decrement on top would double-count it.
11. On the 学資 cell the waiver is in the main contract at five of the six carriers [S1] [S3]
    [S10] [S13] [S16], and death-only in the main contract at the sixth, which sells the
    wider trigger as a 契約者保障保険料払込免除特約 [S6] [S7]. Trigger sets observed: death + 高度障害 +
    accident-caused 身体障害 within 180 days at three [S1] [S10] [S16]; death + 重度障害 at one
    [S3]; death + 身体障害表 第1級・第2級 at one, which also offers a variant adding a
    malignant-neoplasm diagnosis more than 90 days after the 責任開始日 but **does not currently
    sell it** [S13]; and death alone at one [S7]. The composite takes the three-carrier set.
    One carrier also sells a 保険料払込免除不担保特則 — the same product **without** the waiver [S1] —
    which is the cleanest evidence in the file that the waiver is a priced component rather
    than an incident of the contract, and it is the off position the model must be able to
    run.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| 死亡保険金 — 養老 cell | 基準保険金額, level for the term, net of loans and unpaid premiums | [S2] [S8] |
| 満期保険金 — 養老 cell | 基準保険金額 on survival to the end of 保険期間 — **equal to the death benefit** | [R10] [S2] [S8] |
| 高度障害 / 重度障害 — 養老 cell | Treated as death: the insured is deemed to have died on the notice date and the death provisions apply, without the double payment. The policyholder may instead elect the waiver treatment and keep the contract in force | [S2] [S15] |
| Juvenile graded death benefit | 50% of 基準保険金額 below the insured's age 3 and 80% below age 6, floored at the 積立金. Out of the composite | [S2]; scope **[std]** (12) |
| Accidental double indemnity | A second amount equal to the death benefit on a listed accident within 180 days or a listed 感染症, once 1年6か月 has run from 契約日 (6 months from a 復活日). Out of the composite | [S2]; scope **[std]** (12) |
| Death : maturity ratio | **1 : 1**. A 定額型 / 2倍保障型 / 5倍保障型 / 10倍保障型 menu exists at one carrier, in which only the 定額型 is the textbook endowment. Out of the composite | [S4] [R10]; scope **[std]** (12) |
| 学資金 / 祝金 schedule — 学資 cell | 5% / 5% / 10% / 10% / 70% / 10% of 基準保険金額 at policy years 3 / 6 / 12 / 15 / 18 / 20, then 満期保険金 100% at 22 — 210% in all | [S10] [S11]; grid **[std]** (6); timing **[std]** (13) |
| 死亡給付金 — 学資 cell | max(cumulative premiums paid − 学資金 already paid − loans and unpaid premiums, 積立金). **Not a sum assured** | [S3] [S13]; form **[std]** (14) |
| 自動すえ置 of paid 学資金 | Paid 学資金 are automatically deferred at a company-set interest rate unless the policyholder asks otherwise, at three of the six carriers. Out of the composite | [S1] [S10] [S13]; scope **[std]** (15) |
| 免責 — suicide of the insured | No benefit where the insured commits suicide within **3 years** of the 責任開始の日, reset to the latest 復活; the 積立金 or policy reserve (*sekinin-junbikin*, 責任準備金) is paid instead | [S2] [S8]; statutory frame [REG-R34] |
| 免責 — other | Intentional act of the 保険契約者 or of a named beneficiary; war and civil disturbance, subject to a pricing-materiality override that restores cover where the extra deaths do not disturb the basis | [S1] [S2] [S3] [S8] [S10] |
| What is paid when a benefit is refused | The 積立金 / 責任準備金 at two carriers on the 養老 cell, the 返戻金 at one of them on the 学資 cell, and **nothing at all** at two others | [S2] [S3] [S8] [S1] [S10]; **[std]** (16) |
| Contestability (告知義務違反) | Rescission within **2 years** of the 責任開始期; on the 学資 cell the 告知 is the **policyholder's** as well as the insured's | [S1] [S6]; statutory ceiling [REG-R35] |

12. Three 養老保険 shape variants sit at one carrier alone and are excluded together, because
    each breaks the equality the product is defined by. The **juvenile graded death
    benefit** cuts the benefit to 50% below age 3 and 80% below age 6, floored at the 積立金
    [S2] — a real anti-selection control on child lives, absent from the second carrier's 約款
    [S8] and not published by the third [S15]. The **accidental double indemnity** doubles
    the payment after a 1年6か月 waiting period with an extensive conduct exclusion list [S2].
    The **multiplier menu** sells the same contract at death-to-maturity ratios of 1×, 2×,
    5× and 10×, so a "¥5,000,000 policy" can mean a ¥500,000 maturity benefit [S4]; the
    neutral taxonomy defines 養老保険 by the equality [R10], so anything but the 定額型 is a
    different product wearing the name. All three are named here so that a reader meeting
    them in the market knows they are real and knows this library does not model them.
13. The 約款 pay each 学資金 on a fixed calendar date following an age attained in years and
    months — the 11月1日 following 17歳7ヵ月 at the adopted carrier [S10], and elsewhere the 2月1日
    following 満15歳 [S1], the 2月1日 following 5歳10カ月 [S7], the 12月1日 following 満5歳8か月 [S3] and
    the 10月1日 following age 18 [S13] — with the stated age reduced by one for children born
    inside a named window at two carriers [S1] [S13]. `Endowment_JP_A` runs on annual policy
    years, so each payment is standardized to the **policy anniversary following the stated
    attained age**: t = 3, 6, 12, 15, 18, 20. On the second model cell the child's 契約年齢 is
    0, so attained age equals t and the standardization moves each payment forward by
    between one and five months. No amount changes; only timing does, and only inside a
    policy year. It is a known modelling pitfall and is listed as one in
    `technical-notes.md`.
14. Five death-benefit definitions are observed and none is a sum assured: cumulative
    monthly premium × elapsed months [S1]; the **greater** of (premiums × elapsed months −
    学資祝金 paid − unpaid premiums and loans) and the 積立金 [S3]; the same maximum form on
    月掛保険料相当額 × 経過年月数 [S13]; the 責任準備金相当額 alone [S10]; and a 別表2 schedule that was in neither
    retrieved file at the sixth carrier and is therefore [unverified] [S7]. The composite
    takes the **maximum form** — two of the six — because it dominates the other two
    published forms rather than sitting between them: it reproduces the pure
    return-of-premiums shape early and the pure-reserve shape late. The choice moves almost
    nothing, and that is the point. On the male 死亡保険用 table, q(x) runs 0.00081 at age 0,
    0.00022 at 3, 0.00010 at 10, 0.00046 at 18 and 0.00066 at 22 [R1] [REG-R18], so the
    child's mortality over the whole 22-year term is a rounding error against a benefit that
    is roughly the reserve anyway.
15. Automatic deferral of paid 学資金 with interest is the default at three carriers [S1] [S10]
    [S13], but at a rate the insurer sets and may change with market rates and which no
    retrieved document publishes. The composite pays each 学資金 on its due date. Deferral is a
    policyholder election over an insurer-discretionary crediting rate — assumption class
    (b) in `technical-notes.md` — and modelling it would require inventing the rate.
16. What happens when an exclusion bites splits three ways, and the spread is wider on this
    product than on the whole-life chassis. On the 養老 cell the refused death claim pays the
    積立金 at one carrier [S2] and the 責任準備金 at the other [S8]. On the 学資 cell, where the
    policyholder intentionally kills the insured child, one carrier pays the 返戻金 [S3] and
    two pay **nothing at all — not even the reserve** [S1] [S10]. The composite pays the
    保険料積立金 on a refused claim, matching the savings chassis and the majority of the
    retrieved wording; the zero-payment position is named because a model that assumes it
    universally overstates the insurer by the whole reserve.

### Options and contract alterations

| Parameter | Representative value | Basis |
|---|---|---|
| 契約者貸付 | Available against the surrender value at four of the six carriers; **2.40% p.a.** for contracts dated on or after 2025-01-02 (from 2.00%) | [S9] [S1] [S2] [S7] [S8] [S10]; rate adoption **[std]** (17) |
| Loan over-run | Where principal plus interest exceeds the surrender value the contract lapses — immediately at one carrier, after a notice month at a second, on a 基準日 re-test at a third; a fourth instead nets the loan off the 積立金 and reduces the sum assured | [S1] [S2] [S7] [S10] |
| APL (保険料の自動貸付) | Elected, default on; at grace expiry the insurer advances the premium against the surrender value and the contract continues. Interest capped at 年8% (半年4%) | [S1] [S10]; presence **[std]** (18); election requirement [REG-R14] |
| 復活 | Within **3 years** of lapse, on fresh 告知 and payment of arrears; the 責任開始期 resets, restarting the suicide and contestability clocks and the waiver | [S1] [S10]; window **[std]** (19) |
| Reduction of 基準保険金額 (減額) | Treated as a partial surrender: the reduced portion releases its surrender value and future premiums are re-rated. Refused once the 学資年金開始日 has arrived at one carrier | [S1] [S2] [S6] [S10] |
| 払済保険 | On the 学資 cell, conversion turns the contract into a paid-up **養老保険 of the same term**: 祝金 and 死亡払戻金 cease and one benefit equal to the 払済保険金額 remains, revertible within 2 years. Out of the base run | [S10] [S2]; scope **[std]** (20) |
| 学資年金 commutation | The remaining instalments may be commuted to their present value, terminating the contract. Out of the base run | [S7]; scope **[std]** (20) |
| Successor policyholder (後継保険契約者) | Nominated at issue at two carriers, the **insured child** succeeding at a third and a 承継保険契約者 at a fourth. No cash-flow effect; it changes who holds the surrender election | [S1] [S7] [S10] [S13] |

17. The loan rate is one of the few pricing parameters a Japanese carrier publishes, and it
    moved with the 予定利率: **2.00% → 2.40%** for contracts dated on or after 2025-01-02 [S9].
    What the 約款 publish instead are ceilings — 年8%, with 半年4% for monthly and semi-annual
    modes, at two carriers [S1] [S10]. The composite takes 2.40% for both the 契約者貸付 and the
    APL balance, and the modelling lesson is the one the whole-life chassis already
    recorded: the loan rate tracks the contract's vintage 予定利率, not the current market, so
    it is a model-point attribute rather than a scenario variable.
18. APL presence is a genuine three-way split, and on this product it is not the majority
    position. Offered outright at two carriers — advancing the premium at each grace expiry
    with an opt-out at one [S1], and **six months of premium at a time** on monthly
    contracts at the other, on a test run as if those six premiums had been paid [S10].
    Present in disguise at a third, whose 契約者貸付 article expressly contemplates loans "made
    for the purpose of switching into premium" [S2]. And **absent at two**: one has no APL
    article in its base 約款 at all [S6], and the other states outright that 自動振替貸付 is not
    handled [S13]. The composite takes the chassis position — an election with a default-on
    flag, per 監督指針 IV-1-12, which requires the feature to be at the policyholder's election
    with prompt notice when exercised [REG-R14] — and the model point carries the flag so
    that the off position, which two of six carriers represent, must be exercised in
    testing.
19. 復活 within **3 years** at two carriers [S1] [S10]; within **1 year** at a third [S2];
    **not offered at all** at a fourth [S13]; and no 復活 article in the base 約款 of a fifth
    [S6]. Composite: 3 years, matching the chassis. One consequence is specific to this
    product and is not obvious: two carriers pay a 学資金 whose payment date fell **while the
    policy was lapsed**, but only if the policy is subsequently reinstated [S1] [S10] — so a
    lapse inside the benefit schedule is recoverable, and lapse is not a terminal state for
    benefits already due.
20. Both alterations are specified and excluded from the base run for the same reason: each
    needs an insurer-set basis that no retrieved document publishes. 払済保険 solves a reduced
    sum assured off the surrender value on a company basis [S10]; the 学資年金 commutation
    discounts the remaining instalments on an unpublished rate [S7]. The 払済保険 article is
    quoted in full in the mechanics below because it is the clearest statement in the whole
    research set that 学資保険 and 養老保険 are one chassis. One carrier offers neither, along with
    復活, 自動振替貸付, 転換 and 延長定期保険 [S13] — the minimum-alteration design point of the observed
    set.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 解約返戻金 basis | A function of the elapsed months since 契約日, capped at the paid months while premiums are due — and, on the 学資 cell, of the 学資金 already paid. The formula itself is in the unpublished 算出方法書 | [S1] [S2] [S10] [REG-R2]; construction **[std]** (21) |
| Early-duration level | Usually less than total premiums paid and, in the early durations, "either nothing at all or very little"; **capped at the death benefit**, and each 祝金 paid reduces it | [S7] |
| 満期保険金 | 基準保険金額 at the end of 保険期間 — the defining cash flow of this product and the one thing the whole-life chassis does not have | [R10] [S2] [S8] |
| Grace (猶予期間) | 月払: from the first day of the month after the 払込期月 to the last day of that month. 半年払 / 年払: to the 月単位の契約応当日 in the second following month, with named end-of-month substitutions | [S1] [S10]; regime **[std]** (22) |
| Lapse (失効) | From the day after grace expiry, **only where the APL cannot carry the premium** | [S1] [S10] |
| Termination on the policyholder's death where the waiver does **not** apply | The contract ends and the 責任準備金 is paid to the policyholder's legal heirs | [S1] [S10] [S7] |
| クーリング・オフ | 8 days from the later of delivery of the disclosure document and the application date, effective on dispatch. Out of scope | [REG-R36]; scope **[std]** (23) |
| Policyholder protection | On a member insurer's failure, up to **90%** of the 責任準備金 at the failure date | [REG-R40] [REG-R41] |

21. No carrier publishes a surrender-value formula or a numeric surrender-value table for
    either product — a sharper gap than on the whole-life chassis, where two carriers
    publish complete tables. What the 約款 publish is the argument list: 経過年月数, capped at
    払込年月数 where the elapsed term exceeds the paid term, at three carriers [S1] [S2] [S10],
    **plus the timing of the 学資金 payments** at one of them [S1]. The library therefore
    constructs the surrender value as a **[std]** function — a net-level-premium policy
    value on the 1.00% 予定利率 [S9] less an acquisition-cost deduction grading to zero, net of
    the 学資金 already paid — with the construction and its calibration set out in
    `technical-notes.md`. The three published qualitative constraints it must satisfy are
    all from one carrier and all testable: the value is below total premiums paid, it is
    capped at the death benefit, and each 祝金 reduces it [S7]. That is the honest position:
    the *shape* is standardized, and the *constraints* on it are sourced.
22. Three grace regimes are observed and they are not variants of one rule. The roughly
    one-month 約款 grace above, at two carriers [S1] [S10]. A materially longer one at a
    third, running to the day before the 月ごとの契約応当日 in the **third** month after the payment
    window, with a first-premium failure rescinding the contract and a later failure lapsing
    it [S2]. And at a fourth, **no grace article at all**: on non-payment the insurer serves
    notice and the contract is *rescinded* at the 月ごと応当日 in the third month after the due
    month [S6]. The composite takes the two-carrier one-month grace, matching the chassis.
    The rescission regime is excluded because it differs in kind rather than in length — a
    rescinded contract cannot be reinstated, and that carrier has no 復活 article either [S6].
23. The statutory cooling-off applies to every contract in this composite; the exclusion for
    terms of one year or less cannot bite on a 10-to-60-year endowment [REG-R36]. `jplib`
    projects from the point cover is in force and scopes the window out, stated here rather
    than silently omitted because it is a real early-duration decrement that a first-year
    study would see.

---

## Contractual mechanics

Notation used below and carried into `technical-notes.md`:

    x        被保険者's 契約年齢 (満年齢, fractional year discarded)
    y        契約者's 契約年齢 — the 学資 cell only, and a life who is NOT the insured
    t        completed policy years since 契約日 (the annual grid step)
    n        保険期間 in years
    m        保険料払込期間 in years; m = n on the 養老 cell, m < n on the 学資 cell
    S        基準保険金額
    P        annual premium, level for t < m and zero for t >= m
    g(t)     the 学資金 / 祝金 payable at t, as a fraction of S
    V(t)     the policy value (保険料積立金) at t
    CV(t)    the 解約返戻金 payable at t
    L(t)     outstanding 契約者貸付 + 自動振替貸付 principal and interest at t
    W(t)     1 if the premium waiver is in force at t, else 0

### 養老保険 — the equality, and the finite term

The 養老 cell is the whole-life chassis with two changes and no others:

    death benefit at t < n      DB(t) = S - L(t)
    maturity benefit at t = n   MB(n) = S - L(n)

The death benefit is level for the term and the maturity benefit equals it [R10] [S2] [S8].
Everything else — the reserve, the surrender value, the loan and APL recursions, grace,
lapse and reinstatement — is the chassis, unchanged, and is specified in the
[whole life product specification (終身保険)](../whole_life/product-spec.md). The two consequences that
follow from the finite term are worth stating because they change how the model terminates
rather than how it steps. First,
**there is no tail**: every state closes at `t = n`, and the terminal cash flow is a certain
payment of `S` on the surviving in-force, not a decrement. Second, the reserve must reach
`S` at `t = n` by construction, which makes the roll-forward identity a real check rather
than a formality — a 養老保険 reserve that does not converge on the maturity benefit is wrong in
a way a whole-life reserve can hide for decades.

高度障害 / 重度障害 is not an additional benefit: the insured is deemed to have died on the notice
date and the death provisions apply, minus the double payment [S2]. The statutory valuation
table already works this way — 生保標準生命表2018（死亡保険用）**includes 高度障害 inside the death rate**
[REG-R20] — so a projection using it must not add a separate disability decrement. The one
election worth recording is that the policyholder may decline the 高度障害保険金 and take the
premium waiver instead, keeping the contract in force to maturity [S2].

The **suicide exclusion runs three years** at both carriers publishing a 養老保険 約款 [S2] [S8],
three times the twelve months of the UK composite in `uklib`. That period is **contractual,
not statutory**: 保険法第51条 excludes suicide with no time limit at all, and the three-year 免責期間
is a narrowing of the statute in the insurer's own 約款, permitted because it favours the
policyholder [REG-R34]. Where the exclusion bites the contract does not simply forfeit — the
積立金 [S2] or the 責任準備金 [S8] is paid to the policyholder.

### 学資保険 — the staged survival benefit

The composite schedule, as a fraction of `S`:

    g(3) = g(6) = 0.05      g(12) = g(15) = 0.10      g(18) = 0.70      g(20) = 0.10
    maturity at t = 22:  S
    total receipts:      2.10 * S

paid on the policy anniversary following the attained age the 約款 names [S10], standardized
per footnote 13. Two structural facts follow. **The schedule is data, not code**: the
observed designs range from a single 100% payment [S10] through three 20% 祝金 plus a
five-instalment 学資年金 [S7] to four equal 教育資金 payments of 100% each [S13], so any
implementation that hard-codes a shape is modelling one carrier. **And the schedule is not a
decrement**: a 学資金 is paid on survival at a fixed date to a policy still in force, so it is
a certain outflow weighted by in-force, exactly like the maturity benefit — not a claim.

The interaction with the surrender value is the part a model gets wrong: each 祝金 paid
**reduces the surrender value** [S7], and one carrier computes the surrender value from the
elapsed months **and the timing of the 学資金 payments** [S1]. The staged benefit is therefore
a partial release of the policy value, not a payment beside it.

### 学資保険 — the death benefit is a return of premiums

    DB_g(t) = max( P * min(t, m) - S * sum of g(s) for s <= t - L(t) ,  V(t) )

None of the retrieved 学資保険 contracts pays a sum assured on the child's death [S1] [S3] [S7]
[S10] [S13]. What is paid is cumulative premiums less benefits already taken, floored at the
policy value [S3] [S13] — or, at one carrier, the policy value alone [S10]. This is the
single biggest structural difference from every protection product in this library and it
changes the sign of the mortality strain: the child's death releases roughly the reserve the
contract is already holding, so the decrement is near-zero-strain, and the mortality
assumption on the insured has almost no influence on the projected cash flows. Exclusions
are correspondingly narrow — intentional killing by the policyholder, and war [S1] [S3]
[S10].

### 保険料払込免除 — the waiver on the policyholder

**This is the product's defining mechanic and it has no analogue in `uslib` or `uklib`.** It
is a decrement on a life who is *not* the insured, and it does not terminate the contract —
it removes the premium income while leaving every benefit outgo in place.

**The states.** A 学資保険 in force occupies one of two states, and both must be projected:

    (a) premium-paying in force   W(t) = 0 : premiums P payable, all benefits payable
    (b) waived in force           W(t) = 1 : NO premium, all benefits payable in full

Transitions out of (a) are: the insured child's death (pays `DB_g`, terminates); the
policyholder's death or qualifying disability **with** the waiver (moves to (b)); the
policyholder's death **without** the waiver (terminates, paying the 責任準備金 to the
policyholder's legal heirs [S1] [S10] [S7]); surrender; and lapse. From (b) the only exits
are the insured's death, surrender, and maturity — **there is no lapse from the waived
state**, because there is no premium to miss.

**What the waiver actually promises.** Every future benefit — 学資金, 満期保険金, 死亡給付金 — is paid on
schedule, and each future premium is *treated as having been paid* on its 契約応当日 [S1] [S10]
[S13]. The waiver bites from the next 払込期月 or 月単位の契約応当日 after the triggering event [S1]
[S10] [S13]; on the annual grid this is standardized to "premiums cease from `t+1`" where
the trigger falls in year `t`. Contract alterations are frozen afterwards: one carrier
disallows 減額, 保険契約者の変更 and 転換 [S1], a second disallows everything from a change of payment
mode to a change of policyholder [S10], and a third refuses a change of policyholder while
premiums are waived [S6].

**What it is worth.** The waiver benefit is the outstanding premium stream, so its amount at
risk is `P × (m − t)` undiscounted — a **decreasing term assurance on the policyholder over
the premium-paying period**. On the second model cell that is ¥1,845,588 at issue against a
¥1,000,000 maturity benefit: at duration zero the waiver insures **more than the maturity
benefit itself**, and it runs off to zero at `t = 17` while the maturity benefit is still
five years away. The frequency is small and the amount is not. On the male 死亡保険用 table the
policyholder decrement runs q(30) = 0.00068, q(35) = 0.00077, q(40) = 0.00118 and q(45) =
0.00177 [R1] [REG-R18] — so over the 17-year paying period from age 30 the cumulative
probability is of the order of a percent, applied to an amount that starts above the sum
assured. A model that omits the waiver understates the liability by a small probability
times a large amount, which is exactly the error that survives a sensibility check on the
base case.

**Which table, and in which direction the margin points.** The waiver decrement is priced
off 生保標準生命表2018（死亡保険用）at the *policyholder's* age [R1], adjusted to a best estimate as a
**[std]** step, because the statutory table is a **valuation** table carrying an explicit
margin — 2008, 2009 and 2011 experience, a forward improvement allowance, and a 数学的危険論による補整
sized to about a 2σ level [R2] [REG-R20]. The direction matters and is opposite to the usual
one. The waiver is a *cost*, so a table that overstates the policyholder's mortality
**overstates** the liability and is prudent; on the insured child, whose death benefit is
roughly the reserve, the same margin is nearly neutral. One projection therefore carries a
margin that is conservative on one life and neutral on the other, which is a reason to hold
the two decrements as separate assumption inputs rather than one mortality basis. The
national complete life table [REG-R24] is the freely redistributable benchmark against which
that margin can actually be quantified.

**The carve-outs, which are where the waiver fails.** Suicide of the **policyholder** is
excluded for **three years** from the 責任開始期 at three carriers [S1] [S3] [S7] and for only
**two years** at a fourth [S10]; the composite takes three years. Also excluded: the
intentional act of the 後継保険契約者 [S1] [S7] or of the 被保険者 [S3] [S10], and war and civil
disturbance subject to the same pricing-materiality override the death benefit carries [S1]
[S10]. On the accident-caused 身体障害 trigger only, a long conduct list applies — gross
negligence, crime, mental disorder, intoxication, unlicensed and drink driving, earthquake,
eruption and tsunami [S1] [S10]. **When a carve-out bites the contract does not simply lose
the waiver: it dies with the policyholder**, paying the 責任準備金 to the policyholder's legal
heirs [S1] [S10], and one carrier names exactly three ways this happens — three-year
suicide, the successor's intentional act, and war [S7].

**Three further mechanics a model has to know about, and one trap.** The waiver is
underwritten on the policyholder: the 告知義務 is the policyholder's, it is re-imposed on a
change of policyholder and on 復活, and contestability is two years from the 責任開始期 [S1] [S6]
[S10]. A waiver can be **undone** — a 告知義務違反 rescission after the waiver has begun restores
the premium obligation retrospectively, unless the claimant proves the waiver event was
unconnected to the undisclosed fact [S1] [S6]. Succession differs: two carriers require a
後継保険契約者 nominated at issue [S1] [S7], and a third makes the **insured child** succeed to the
policyholder's rights on the waiver [S10]. And the trap, stated identically at three
carriers: **if the waiver event happens while a premium is unpaid inside the grace period,
the unpaid premium must be paid by the end of that grace period or the waiver is refused**
[S1] [S10] [S6]. That is a direct interaction between the two decrements — a policyholder
who dies one week into arrears loses the whole benefit — and it is the clearest reason the
waiver cannot be modelled as an independent overlay on a premium stream.

The composite treats the two lives as **independent [std]**, because no retrieved document
gives a dependency and none could. Where the policyholder is the insured child's parent,
common-accident dependence is real and unmodelled; it is listed as a model risk in
`technical-notes.md`.

### 払済保険 — the article that proves the two products are one chassis

One carrier's 学資保険 約款 converts a policy to 払済保険 by applying the surrender value as a single
premium to "a paid-up **養老保険** of the same 保険期間 as the original contract", after which the
祝金 and the 死亡払戻金 cease and a single benefit equal to the 払済保険金額 is payable on maturity,
death or 高度障害 [S10]. Reversion to the original contract is available within two years [S10].
That is the inheritance made explicit in a contract rather than in a modelling note: strip
the staged schedule and the return-of-premiums death benefit off a 学資保険 and what remains
**is** a 養老保険.

---

## Riders and options

**In scope (modelled or parameterized):**

- **満期保険金** — the main contract's defining benefit, equal to the death benefit, paid on
  survival to `t = n` [R10] [S2] [S8].
- **保険料払込免除 on the 契約者** — main-contract cover on the 学資 cell at five of six carriers,
  modelled as a second decrement with its own state, its own life and its own table [S1]
  [S3] [S10] [S13] [S16]. The off position (the 保険料払込免除不担保特則 [S1], and the death-only
  trigger set [S7]) must be exercisable.
- **学資金 / 祝金 schedule** — a data table on the model point, not a hard-coded shape [S10]
  [S11].
- **契約者貸付 and 自動振替貸付** — inherited from the savings chassis, with the loan rate 2.40% [S9]
  and the APL as an election with a default-on flag [S1] [S10] [REG-R14].
- **５年ごと配当** — specified as an insurer-discretionary cash flow and carried as a model-point
  attribute, but **not implemented**: no retrieved document on either cell publishes a
  dividend scale, so the model rejects the value by name rather than projecting a 無配当
  contract under a 有配当 label [S1] [S10] [REG-R9].
- **リビング・ニーズ特約** — attached automatically to 終身保険 and 養老保険 at one carrier [S8]; modelled as
  an acceleration of the death benefit, per the chassis.

**Out of scope:** the educational annuity on the policyholder's death (育英年金特約), which exists
at two carriers but whose own 特約条項 was retrieved at neither, so its amount, term and taper
are **[unverified]** [S1] [S6]; the juvenile graded death benefit, the accidental double
indemnity and the 2倍 / 5倍 / 10倍保障型 menu, all at one carrier [S2] [S4]; 出生前加入特則 and 兄弟加入特則,
the latter carrying an unpublished sibling discount [S10] [S12]; the medical and accident
riders attachable to 学資保険 — up to three of four at one carrier [S3] [S5], two named riders
at a second [S1], a separate packaged child medical contract at a third [S6] and a packaged
child medical policy with three exceptions at a fourth [S12] — whose shape belongs to
`medical`; 保険料払込免除特約 on the 養老 cell [S8]; 保険契約者代理特約 and 代理請求特約 [S15]; the 学資年金 commutation
[S7]; 転換 and 延長定期保険, named as not offered at one carrier [S13] and 転換 named as an
alteration the waiver freezes at another [S1], neither modelled anywhere in this library;
and the corporate
「ハーフタックスプラン」 form of 養老保険, which was not researched and which would add tax mechanics rather
than product mechanics [unverified].

---

## Variations across insurers

1. **Total receipts as a percentage of 基準保険金額.** 100% or 130% [S3]; 150% or 200% [S1]; 200%
   or 210% [S10]; 300% or 360% [S7]; 400% [S13]; not published [S16]. A four-fold spread
   that is an artefact of how each carrier scales the 基準保険金額, not of what each pays.
   Composite: the 210% S型 grid [S10], because its arithmetic closes against a published plan
   [S11].
2. **The 学資金 payment-date rule.** The first 2月1日 after the stated age [S1] [S7]; the 12月1日
   after it [S3]; the 11月1日 after it [S10]; the 10月1日 after it [S13]; the 契約応当日 for the 学資年金
   [S7]. Two carriers reduce the stated age by one for children born in a named window [S1]
   [S13]. Composite: the policy anniversary following the stated attained age (footnote 13)
   — the only rule an annual grid can express without inventing a birth date.
3. **The child's death benefit.** Cumulative premium × elapsed months [S1]; max(premiums −
   benefits − loans, 積立金) [S3] [S13]; 責任準備金相当額 [S10]; a 別表2 schedule that was not retrieved
   and is [unverified] [S7]. Composite: the maximum form (footnote 14), which dominates
   rather than splits the difference.
4. **Waiver trigger set.** Death + 高度障害 + accident-caused 身体障害 within 180 days at three [S1]
   [S10] [S16]; death + 重度障害 at one [S3]; death + 身体障害表 第1級・第2級 at one, with an unsold
   cancer variant [S13]; death alone in the main contract at one, the rest sold as a rider
   [S6] [S7]. Composite: the three-carrier set. On the 養老 cell the same feature points at
   the *insured* instead [S2], or is a rider [S8] — the clearest sign that the two cells are
   different products at this point and not one parameterization.
5. **The waiver's suicide carve-out.** **3 years** at three [S1] [S3] [S7]; **2 years** at a
   fourth [S10]; not published at two [S13] [S16]. Composite: 3 years. The gap matters more
   than a year of exposure suggests: inside the carve-out the contract does not merely keep
   paying premiums, it terminates.
6. **Grace, and what follows it.** One month at two [S1] [S10]; to the 契約応当日 in the third
   month at a third [S2]; and **no grace article at all** at a fourth, which serves notice
   and rescinds the contract at the 月ごと応当日 in the third month after the due month [S6].
   Composite: the one-month grace. Rescission is a different termination, not a longer
   grace.
7. **保険料の自動貸付.** Present with an opt-out at one [S1]; present, six months at a time, at a
   second [S10]; present in disguise as a purpose-built 契約者貸付 at a third [S2]; **absent** at
   two [S6] [S13]. Composite: an election with a default-on flag [REG-R14], and the off
   position must be tested — this is the single largest source of divergence in projected
   lapse experience across the six.
8. **復活 window.** 3 years at two [S1] [S10]; 1 year at a third [S2]; **not offered** at a
   fourth [S13]; no article at a fifth [S6]. Composite: 3 years, with the 学資金-during-lapse
   rule of two carriers carried with it [S1] [S10].
9. **Participation.** ５年ごと配当 at two [S1] [S10]; 有配当 at a third [S6] [S8]; annual plus
   long-duration 契約者配当 at a fourth [S2]; **none at all** at a fifth [S13]; 無配当 at a sixth
   [S16]. Composite: 無配当, with the ５年ごと配当 variant specified and rejected by name rather
   than parameterized. No retrieved document publishes a dividend scale or a 三利源 split.
10. **Contract alterations.** 払済保険 turning the contract into a 養老保険 at one [S10] and
    available after two years on the 養老 cell at a second [S2]; **払済保険, 延長定期保険, 転換, 復活 and
    自動振替貸付 all absent** at a third [S13]; 減額 refused after the 学資年金開始日 at a fourth [S6].
    Composite: 減額 in, the rest specified and out of the base run.
11. **Riders and packaging.** Up to three of four attachable riders at one [S3] [S5]; two
    named riders plus an 育英年金特約 at a second [S1]; a separate packaged child medical
    *contract* sharing one 契約基本約款 at a third [S6]; a packaged child medical policy with
    three named exceptions at a fourth [S12]; and **no riders at all**, with one policy per
    insured child and no policy document issued, at a fifth [S13] [S14]. Composite: main
    contract only.
12. **Volume discounts.** A three-band unit rate per ¥100,000 of 基準保険金額 at one [S7]; a flat
    ¥30 per ¥100,000 above ¥700,000 at a second [S13]; not published at four. Composite: out
    of scope, with the 減額-into-a-worse-band consequence recorded [S13].
13. **Tax treatment of the staged benefits.** 学資年金 as 雑所得 and こども祝金 as 一時所得 at one carrier
    [S7]; **both** the 教育資金 and the 満期保険金 as 雑所得, with a stated 必要経費 formula, at a second
    [S13]; not published at four. Composite: the instalment stream as 雑所得 (see Regulatory
    context) — but this is a disclosure difference about the same tax law [R6], not a
    product difference, and `jplib` models contractual cash flows rather than the
    policyholder's tax position.
14. **What does not vary.** On 養老保険: the death benefit and the maturity benefit are
    **equal**, in the neutral taxonomy and in both retrieved 約款 [R10] [S2] [S8] [S15]; the
    suicide exclusion runs **three years** from the 責任開始の日 and pays the reserve rather than
    nothing [S2] [S8]. On 学資保険: the death benefit is a **return of premiums or of the
    reserve, never a sum assured**, at all four carriers that publish it [S1] [S3] [S10]
    [S13] and impliedly at a fifth [S7]; a premium waiver on the policyholder exists in
    some form at **all six** [S1] [S3] [S7] [S10] [S13] [S16]; the waiver leaves every
    benefit payable in full and treats each future premium as paid [S1] [S10] [S13]; and the
    type, once elected, cannot be changed after issue [S7]. Across both: 契約年齢 is 満年齢 at 契約日,
    incrementing at the 年単位の契約応当日 rather than the birthday [S1] [S2] [S10] [S13]; 減額 is
    treated as a partial surrender releasing the corresponding value [S1] [S2] [S6] [S10];
    loans and unpaid premiums are netted off every benefit payment [S1] [S3] [S6] [S10];
    contestability is **two years** [S1] [S6]; premiums fall in the 一般生命保険料控除 basket [R8];
    and **no carrier publishes a full rate basis, a 予定事業費率 or a surrender-value table** [S4]
    [S5] [S11] [S16]. Those are the invariant core, and every one is a fact a model can rely
    on without a [std] tag.

---

## Regulatory context

**Prudential — ESR, and what it replaced.** From **31 March 2026** Japanese insurers are
supervised on economic-value-based solvency regulation (*keizai-kachi bēsu no soruvenshī
kisei*, 経済価値ベースのソルベンシー規制, **ESR**): assets at fair value, liabilities at
current estimate (*genzai suikei*, 現在推計) plus MOCE, re-measured at each 基準日 on assumptions
re-set then and discounted on a prescribed yield curve, calibrated in principle to
**99.5%**, with early corrective action at an ESR below **100%** — replacing the old
ソルベンシー・マージン比率 **200%** trigger [REG-R15] [REG-R17]. The change bites on this product in a
specific way. A 30-year 養老保険 written at a 1.00% 予定利率 [S9] is a long, fixed, guaranteed
maturity obligation, and the old basis was **ロックイン** — the assumptions fixed at issue. Under
a re-measured basis the maturity guarantee is re-valued on each 基準日's curve, which is
exactly what a re-projectable, assumption-parameterized liability model of the kind this
library builds is for. `jplib` computes neither ratio; the standard-formula coefficients sit
in 告示 that were not opened in the research pass and are [unverified] [REG-R16].

**Statutory reserving — cited, not reproduced.** 保険業法第116条 obliges the insurer to hold 責任準備金
and delegates the accumulation method and the level of the assumed coefficients for
long-term contracts [REG-R4]. 施行規則第68条 sets the scope: all life contracts except
separate-account contracts whose reserve varies with the fund, contracts holding no 保険料積立金
or 払戻積立金, and contracts whose 約款 lets the insurer change the 予定利率 — so a conventional 養老保険
or 学資保険, with a fixed 予定利率 and a real 保険料積立金, is squarely **in** scope [R3] [REG-R7]. 第69条
splits the reserve into 保険料積立金, 未経過保険料, 払戻積立金 and contingency reserve (*kiken junbikin*,
危険準備金), and imposes the net level premium method (*heijun jun-hokenryō-shiki*, **平準純保険料式**)
floor — defined in the ordinance itself as levelling the funding over the whole
premium-paying period — on anything out of scope [R3] [REG-R8]. The Commissioner's
instrument is 平成8年大蔵省告示第48号, which sets the 積立方式, the 予定死亡率 and the 標準利率 machinery [R4]
[REG-R10]; the 2021 amendments brought USD- and AUD-denominated contracts written from
2022-04-01 into scope, which is the scope boundary this yen composite sits inside [R5]
[REG-R12]. **The current numeric 標準利率 could not be established from any retrieved official
document** [R4] [R5], so no 標準利率 figure is asserted downstream. 価格変動準備金 is asset-driven and
out of scope [REG-R3]. This library projects gross cash flows and builds none of these
reserves.

One point specific to the 学資 cell: the 約款 use 積立金 and 責任準備金 interchangeably for the reserve
— one carrier defines 積立金 as "the 責任準備金 for the base contract computed by the method the
company determines" [S2] [S3], and a second defines it identically [S13]. That makes the
reserve a **contractual floor on a benefit**, not only a balance-sheet quantity: it floors
the juvenile graded death benefit [S2], the war-risk reduction [S2] [S8] and the 学資保険 death
benefit [S3] [S13]. A model that treats the reserve as purely a valuation output cannot
compute this product's benefits.

What the regime asks of a projection is set by 保険業法第121条第1項第1号, which requires the 保険計理人
appointed under 第120条 to confirm in an 意見書 that the reserve is soundly accumulated [REG-R5]
[REG-R6]; the IAJ practice standard turns that into the **1号収支分析**, a forward
income-and-outgo analysis over at least ten future years by product segment, under
prescribed scenarios, with sufficiency tested over the first five [REG-R22]. That is the
shape of this product's projection.

**Mortality basis.** 生保標準生命表2018（死亡保険用）is the statutory valuation table on both cells and
both lives [R1] [REG-R10] [REG-R11] [REG-R18], produced by 日本アクチュアリー会 as the 指定法人 designated
under the Act and commissioned by 金融庁 [REG-R23]. Two qualifications must both be kept. It is
a **valuation** table — 2008/2009/2011 experience, select-period truncation at 10 years,
policy years to 30, exposure of 40.68 million policy-years male and 30.02 million female,
then a margin sized to roughly 2σ [R2] [REG-R20] — so any best-estimate basis is a **[std]**
adjustment *of* a sourced table, and each document says which of the two it means. And the
IAJ's site terms prohibit reproduction and transmission to third parties without written
consent [REG-R21], so `jplib` cites the tables by URL, quotes only the individual rates its
worked example needs, and ships `mort_table.csv` as a **[std]** construction whose
`provenance` column points at the IAJ entries. It is never a copy of the IAJ file. The
freely redistributable 第23回生命表 is the comparison basis against which that margin can be
quantified [REG-R24].

**Conduct and classification.** The supervisory guideline requires 解約返戻金 to be disclosed
clearly — the amount on the policy schedule or the method in the 約款 (IV-1-10) — and a 自動振替貸付
to be at the policyholder's election with prompt notice when exercised (IV-1-12) [REG-R14].
Both bear directly on a product whose surrender value is below premiums paid for most of its
life [S7]. The **返戻率** raises the sharper conduct question: it is a ratio of guaranteed
receipts to guaranteed premiums on a 無配当 design [S13] [S16] but a partly non-guaranteed one
on a 有配当 design [S1] [S6] [S10], and presenting a non-guaranteed element as certain is
断定的判断の提供 under 消費者契約法第4条 [REG-R38], with 説明義務 under 金融サービス提供法第4条 covering the
surrender-value profile [REG-R39]. No FSA, 消費者庁 or 国民生活センター publication specific to 学資保険
return-ratio disclosure was located in the research pass, so any claim that the disclosure
is *regulated* would be [unverified]; the published ratios are carrier marketing
disclosures. A yen, fixed-予定利率 養老保険 or 学資保険 is **not** a 特定保険契約 under 保険業法第300条の2 — that
classification and its FIEA-grade conduct rules attach to the 外貨建 and 変額 designs [REG-R37].
クーリング・オフ is eight days on a dispatch rule and is scoped out [REG-R36]. On insurer failure,
contracts are covered up to **90% of the 責任準備金** at the failure date, the rate set by
ordinance under 保険業法第270条の3 [REG-R40] [REG-R41].

**Tax — where this product's design actually comes from.** Three regimes matter, and the
split between the first two is the reason 学資保険 and 養老保険 are taxed differently despite being
one chassis.

*Lump sum versus instalments.* Where the premium payer and the recipient are the same
person, a lump-sum 満期保険金 is **一時所得**: receipts, less premiums paid, less a ¥500,000 特別控除, of
which only half enters taxable income [R6] [REG-R46]. A benefit taken as a stream is **雑所得**
— the year's payment less the premiums attributable to it, with neither the ¥500,000
deduction nor the halving [R6] [REG-R46]. One carrier applies exactly that to its staged
product: both the 教育資金 and the 満期保険金 are 雑所得, with 必要経費 = (総払込保険料 ÷ 総受取額) × payment [S13].
On the second model cell that fraction is ¥1,845,588 ÷ ¥2,100,000 = 0.8789, so **12.1% of
every receipt is taxable 雑所得** (derived from [S11] [S13]). A second carrier splits its own
product, treating the 学資年金 as 雑所得 and the こども祝金 as 一時所得 [S7]. And on the anchor 養老 cell the
一時所得 computation produces **nothing at all**: receipts of ¥5,000,000 against premiums of
¥5,434,200 are a loss before the ¥500,000 deduction is even reached (derived from [S9]). At
a 1.00% 予定利率 the tax advantage of the lump sum is theoretical.

*Premium deduction.* Both products fall in the 一般生命保険料 basket — contracts paying on survival
or death [R8] — deductible on a banded schedule to ¥40,000 per basket with an overall
income-tax cap of ¥120,000 across the three post-2012 baskets [R7] [REG-R43]. Neither
product can reach the 個人年金保険料 basket, whose 税制適格 conditions require the annuitant to be the
payer or spouse, level premiums for ten or more years, and a ten-year-certain or life
annuity generally from age 60 [R8]. Both model cells saturate the 一般 basket on their own —
¥181,140 and ¥108,564 of annual premium both exceed the ¥80,000 point at which the deduction
flattens to ¥40,000 [R7] — which is a concrete instance of the deduction structure shaping
Japanese product design rather than rewarding concentration. Savings-type contracts with a
term under five years are excluded from the deduction entirely [R8], a floor on the 養老保険
term envelope.

*Inheritance.* On the **policyholder's** death the right under a 学資保険 is inheritance-taxable
property, and the later 教育資金 and 満期保険金 are then taxed as 雑所得 only on the part not already
caught by inheritance tax [S13]. The ¥5,000,000 × statutory heirs exemption of 相続税法第12条
attaches to a **死亡保険金** [REG-R44] [REG-R45]; what passes here is a contract *right*, not a
death benefit, and whether the exemption reaches it is **[unverified]**.

**Professional standards and the accounting frame.** The basis any model uses is
professionally owned by the 保険計理人 appointed under 保険業法第120条 [REG-R5], working to the IAJ's
実務基準 [REG-R22], and the table that binds the statutory reserve is produced by the IAJ in its
指定法人 capacity [REG-R23]. The frame a reader arriving from `uklib` or `uslib` must not
import: **IFRS 17 is not mandatory in Japan** — IFRS applies as 指定国際会計基準 on a voluntary
basis [REG-R47]. J-GAAP statutory reserving, the ESR economic balance sheet and IFRS 17 are
three separate bases over one set of projected cash flows, and this product keeps the cash
flows basis-agnostic, with discounting, margins and tax layered on top.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-endowment-r1
[R10]: #jplib-endowment-r10
[R2]: #jplib-endowment-r2
[R3]: #jplib-endowment-r3
[R4]: #jplib-endowment-r4
[R5]: #jplib-endowment-r5
[R6]: #jplib-endowment-r6
[R7]: #jplib-endowment-r7
[R8]: #jplib-endowment-r8
[R9]: #jplib-endowment-r9
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
[REG-R23]: #jplib-reg-r23
[REG-R24]: #jplib-reg-r24
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
