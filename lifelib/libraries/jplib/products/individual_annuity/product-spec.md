# Product Specification

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** This is a *standardized composite specification* of a Japanese fixed
individual deferred annuity — individual annuity insurance (*kojin nenkin hoken*, 個人年金保険) in
its fixed (*teigaku*, 定額) form — assembled for reference liability cash-flow modeling. It
describes no single insurer's contract. Facts carrying a source tag — [S#] (primary product
documents) and [R#] (product-specific regulatory/actuarial references), both numbered per
`_research/individual-annuity.md` and resolved in `sources.md` (same directory; numbering
frozen, never renumbered), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) —
were extracted from the cited document. Values marked **[std]** are standardizations
introduced for the reference implementation; each [std] table row carries a numbered
footnote giving the rationale and, where one exists, the observed range across carriers.
Facts the research file could not verify are flagged [unverified]. Documents from **seven**
carriers were pursued; **five** yielded extractable text and are the basis of this composite
— one carrier's policy conditions (*yakkan*, 約款) booklet, tax rider and tontine release [S1]
[S2] [S3]; a second's booklet bound with its 契約概要／注意喚起情報 [S4]; a third's rate release and
product page [S5] [S6]; a fourth's rate release, two product pages and rate schedule [S8]
[S9] [S10] [S11]; and a fifth's product page and declared-rate page [S12] [S13]. Two
further booklets [S14] [S15] and one pre-contract disclosure [S7] downloaded cleanly but
are typeset in subset CID fonts with no ToUnicode map, so no parameter below rests on them.

The composite is a **level-annual-premium 生存保障重視型** (*seizon hoshō jūshi-gata*,
survival-benefit-weighted) fixed deferred annuity with the tax-qualification rider (*zeisei
tekikaku tokuyaku*, **税制適格特約**) attached, paying a **10年確定年金** (*kakutei nenkin*,
annuity-certain) from age 65. Its two phases — accumulation to an annuity fund (*nenkin
genshi*, 年金原資), then payout — run on one annual grid in `Annuity_JP_A`. Variable (変額) and
foreign-currency (外貨建) annuities are out of scope and appear below as scope boundaries.

---

## Product overview and market role

個人年金保険 is first-sector (*dai-ichi-bun'ya*, 第一分野) business — fixed-sum insurance on human
survival or death under 保険業法第3条第4項第1号 [REG-R1]. Level premiums accumulate over a deferral
phase to a 年金原資; on the annuity payment start date (*nenkin shiharai kaishi-bi*, 年金支払開始日)
that fund buys the annuity, paid annually thereafter [S2] [S4] [R16]. Japanese practice uses
deferral period (*sueoki kikan*, 据置期間) narrowly, for the gap between the end of premium
payment and the annuity start; this document keeps that narrow sense and says "deferral
phase" for the whole pre-annuitisation period.

The block is large and growing on both measures. At 31 March 2025, **20.06 million**
policies were in force (100.6% of the prior year — the first rise in eight years) carrying
**¥104.1428 trillion** of 契約高, of which 定額年金 was **87.5%** by count and **84.4%** by amount
[R15]. New business ran to 1.47 million policies in FY2024, split 定額 **64.9%** by count and
**57.6%** by amount — so the fixed product dominates the stock while the variable product
has taken a much larger share of flow [R15]. In-force 年換算保険料 was ¥6.1399 trillion against
¥22.1448 trillion on 個人保険 [REG-R31]. Household penetration is **23.2%** [REG-R32] — one
household in four, against 95.1% for medical cover, which is the shape of a tax-driven
savings purchase rather than a protection purchase. New business skews female: 45.9% male,
54.1% female [R15].

One definition must be carried into any model built from these figures: for annuities 契約高
means **年金原資 before annuitisation and policy reserve (*sekinin-junbikin*, 責任準備金)
after it** [R15] — a quantity that grows with duration, so it is not comparable to a sum
assured. The published **解約・失効率 of 3.4%** for
FY2024 is measured on pre-annuitisation in-force 契約高 at the start of the year only [R15],
which makes it exactly the deferral-phase decrement a projection needs; the 個人保険 figure is
5.6% [REG-R31].

What the product is *for* is the third basket of the life insurance premium deduction (*seimei
hokenryō kōjo*, **生命保険料控除**). Post-2012 the deduction runs in three baskets — 一般 / 介護医療
/ 個人年金 — each capped at **¥40,000**, with an overall ceiling of **¥120,000** at national
income-tax level [REG-R43] [R11]. The 個人年金 basket is reachable only by a contract meeting
所得税法第76条第8項 [R9] and 所得税法施行令第211条・第212条 [R10]; the 税制適格特約 is what binds the policy to them.
Without it the premium falls into the 一般 basket, competing with the household's death cover
for the same ¥40,000 [S12] [R16]. That fact shapes almost every parameter below — the
ten-year minimum premium term, the age-60 annuity-start floor, the ten-year minimum payment
period, the progressively-increasing death benefit, and the bars on drawing dividends and
part-commuting the annuity.

Underwriting is largely absent. One carrier's annuity states 「ご契約に際して、告知は不要です」 — no
disclosure at all [S2] — and the same carrier's tontine advertises no medical examination
and no disclosure [S3]; a second offers a no-selection special provision (*musentaku tokusoku*,
無選択特則) which, attached, removes both the disclosure duty and the premium-waiver benefit
[S4]. The mortality risk the insurer carries in deferral is a *refund* obligation capped at
premiums paid, not a sum assured, so there is little to select against.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 定額個人年金保険, deferred, level annual premium, 生存保障重視型 | [S2] [S4] [S5] [S6] [R16] |
| Regulatory class | 第一分野 life business (保険業法第3条第4項第1号) | [REG-R1] |
| Participation | Interest-differential dividend every five years (5年ごと利差配当) | adoption **[std]** (1) |
| Lives basis | Single life; 被保険者 = 年金受取人 = 保険契約者 | [S1] [S4] [S9] [S10] |
| Underwriting | None — no medical examination, no disclosure (告知) | [S2] [S3] [S4] |
| Issue age (契約年齢) | 20–55, on an insurance age — age nearest birthday (*hoken-nenrei*, 保険年齢) basis | envelope **[std]** (2) |
| 保険料払込期間 | To age 60, a whole number of years, minimum 10 | **[std]** (3); ≥ 10 forced by [S1] [R9] |
| 据置期間 (narrow sense) | 5 years, from 払込満了 to the 年金支払開始日 | **[std]** (3) |
| 年金支払開始年齢 | 65 | **[std]** (3) |
| Base annuity type | 10年確定年金, fixed at issue | menu [S2] [S3] [S9]; pick **[std]** (11) |
| Minimum 年金年額 | ¥120,000 | [R16] |
| Currency | JPY | [S2] [S4] [S5] [S6] [S8] [S9] |
| Rider attached in the base run | 個人年金保険料税制適格特約 | [S1] [S2] [S4] [S9] [S12] |
| **Anchor model cell** | Male, 保険年齢 30 at issue; level annual premium ¥180,000 to age 60 (30 premiums, ¥5,400,000 cumulative); 5-year 据置期間; annuity from age 65; 10年確定年金; 税制適格特約 attached | **[std]** (4) |

Footnotes to [std] rows:

1. Three of the five carriers write this chassis as participating on a five-year cycle:
   5年ごと利差配当 at two [S4] [S5] [S6], 5年ごと配当 on a third's tontine [S3]. A fourth's dividend
   basis was not extracted from the documents retrieved; the fifth is outside the chassis,
   paying a 金利キャッチアップ配当 when new-business assumed interest rate (*yotei riritsu*, 予定利率) rises
   above the rate at issue [S12]. Market-wide the menu is 無配当 / 5年ごと利差配当 / 毎年配当, 無配当 dominating
   single-premium, 積立利率変動型 and foreign-currency annuities [R16]. The composite takes
   5年ごと利差配当 and then sets the declared dividend to zero in the base run — footnote 16.
2. Observed 契約年齢: **0–75** [S6]; **7–65**, narrowing to 18–55 online [S9]; **0–80** on one
   carrier's ordinary annuity [S3]; **from 18** [S12]. Market-wide, carriers start at 0 and
   top out around 65–70, with single-premium contracts written into the late 80s [R16].
   Tontine designs sit at the top — 50–80 [S3], male 50–87 / female 50–86 [S10] — and are
   excluded from the envelope. The composite takes **20–55**: the intersection of the four
   ordinary-annuity envelopes once the rider's ten-year premium term and age-60
   annuity-start floor are imposed [S1] [R9] [R10], since an issue age above 55 cannot pay
   ten years of premiums and start at 65.
3. These three interlock and share one rationale. 保険料払込期間 observed **5–30 years** [S3], with
   the rider forcing ≥ 10 [S1] [R9]. 据置期間 observed **≤ 15 years** [S3] and named by one
   carrier as an explicit lever — setting a deferral period between the end of premium
   payment and the annuity start increases the annuity [S6]. 年金支払開始年齢 observed **60–90** on
   a tontine [S3], **65** in one carrier's standard illustrations [S5] [S6], "in principle
   65" at a second [S12]; market-wide the common menu outside single-premium business is
   55 / 60 / 65 / 70 / 75 [R16]. The composite takes **払込満了 60 / 据置 5 / 年金開始 65** — the
   specimen that carrier publishes on both its documents [S5] [S6], clearing 所令212's age-60
   floor with margin [R10] and exercising the 据置期間 lever rather than degenerating it to
   zero. A model that never separates 払込満了 from 年金支払開始日 cannot reproduce that lever.
4. Premium rates are not public: 予定利率, 予定死亡率 and 予定事業費率 live in the 保険料及び責任準備金の算出方法書 filed
   with the FSA, which is not published [REG-R2]. The anchor is therefore built on a
   **published specimen at the identical model point** — level monthly premium ¥15,000
   (¥180,000 a year), 契約年齢 30 male, 60歳払込満了, 65歳年金開始, 10年確定年金, as at 2025年10月: 払込保険料総額
   ¥5,400,000, 年金原資 approximately ¥6,260,000, 一括受取率 approximately 115.9%, 基本年金額 ¥638,300,
   年金受取総額 ¥6,383,000, 年金受取率 approximately 118.2% [S6]. ¥180,000 is the annualisation of that
   monthly figure, clears the same carrier's ¥15,000 premium-band discount threshold [S6],
   and sits in the ¥12万–24万 band of household annual premiums [REG-R32]. Male, because
   the same specimen is published for both sexes and the two differ by under 0.4% at this
   age [S6] — a sex difference the deferral phase barely carries, unlike the payout phase.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level, guaranteed for the whole 保険料払込期間; no reviews | [S2] [S4] [S5] [S6] |
| Frequency | Annual, in advance | modes [S4] [R16]; default **[std]** (5) |
| Payment route | Direct debit (口座振替) | [S2] [S4] |
| 予定利率, deferral phase | 1.00% p.a. | adoption **[std]** (6) |
| 予定利率, payout phase | 0.65% p.a., set separately from the deferral rate | [S5]; adoption **[std]** (7) |
| 予定事業費率 | Not published; a [std] loading is specified in `technical-notes.md` | [REG-R2]; **[std]** (8) |
| Premium-band discount | Applied once the monthly-equivalent premium reaches ¥15,000 | [S6] |
| Prepayment of ≥ 3 annual premiums (前納) | Discounted at a declared rate, balance accumulated at a declared rate. Out of scope | [S4] [S11] |
| Policy loan (契約者貸付) | Within a stated fraction of the surrender value (*kaiyaku-henreikin*, 解約返戻金), compound at 2.40% p.a. for the current issue cohort; none after annuitisation | [S4] [S11]; adoption **[std]** (9) |
| Automatic premium loan (自動振替貸付) | A policyholder election; compound interest capped at 8% p.a. | [S4] [REG-R14]; scope **[std]** (17) |
| Refund of unused premium | Whole unused months refunded on annual and semi-annual modes; nothing on monthly | [S4] |

5. Modes are 月払 / 年払 / 半年払 plus 一時払 on single-premium products [S4] [R16]. The composite
   takes **annual**, matching the annual grid. This is cheaper than it looks: two carriers
   define the deferral-phase death benefit as 月払保険料 × 経過月数 — *the same amount whichever mode
   is in force* [S2] [S4] — so the benefit is mode-invariant by construction. What the
   annual grid does lose is the sub-annual grace mechanics; footnote 18.
6. Published 予定利率 for level-premium annuity business: **1.00%** from 0.60%, for 契約日 from
   2025-01-02 [S8]; **1.20%** where 30 or more years remain to annuitisation and **1.00%**
   where fewer do, from 0.80% / 0.65%, for 契約日 from 2025-10-02 [S5]; and a
   **minimum-guarantee 予定利率 of 0.50%** on a rate-resetting design, fixed at issue [S12]. The
   2025 increase was the first in about **40 years** [S8]. The composite takes **1.00%** —
   the value two carriers reach on the current cohort, and the more conservative arm of the
   one banded pair. Two structural facts from the same table are carried into the model: the
   deferral rate can be **banded by years remaining to annuitisation**, and the payout phase
   carries **its own** rate [S5].
7. The payout-phase **0.65%** is published by one carrier and was left unchanged when that
   carrier's deferral rates moved [S5] — the clearest evidence in the retrieved set that the
   phases are priced on separate bases. The only other retrieved payout figures are
   illustration assumptions on a rate-resetting design: **0.55%** rate-maintained or rising,
   **0.15%** falling [S12]. The consequence the worked example must show: a payout rate
   *below* the deferral rate means each yen of 年金原資 buys less annuity than a single-rate
   model would say.
8. No retrieved document discloses 予定事業費率 or a 死差 / 利差 / 費差 decomposition for this line —
   the 算出方法書 is not public [REG-R2], and 三利源 is practice vocabulary in any event:
   保険業法施行規則第30条の2 permits distribution 「剰余金の生じた原因に応じて」 without naming the three sources
   [REG-R9]. Expense loadings are wholly **[std]** and specified in the technical notes.
9. One carrier publishes the contract-loan rate by issue-date cohort — 3.05% (2012-04-02 to
   2014-04-01), 2.55% (to 2017-04-01), 2.25% (to 2022-04-01), 2.00% (to 2025-01-01) and
   **2.40%** from 2025-01-02, the increase announced alongside the 予定利率 rise [S11] [S8].
   Another states only that the rate is declared and reviewed on the first business day of
   January and July, applying from the following 1 April and 1 October [S4]. The composite
   takes 2.40% and the **8% p.a.** cap that second carrier states for its 自動振替貸付 [S4]. 監督指針
   IV-1-12 requires the loan limit to be reasonable against the surrender value with
   over-loan prevention [REG-R14]; the composite caps at the surrender value, and the
   contract lapses **from the moment the excess arose** if the demanded payment is not made
   [S4].

### Benefit provisions — deferral phase

| Parameter | Representative value | Basis |
|---|---|---|
| Death benefit (死亡給付金) | Cumulative premiums paid, contractually 月払保険料 × 経過月数 — the monthly premium for the basic annuity times elapsed months, whatever the actual mode | [S2] [S4]; [S6] states it as 既払込保険料相当額 |
| Why that shape | 所得税法施行令第211条第1号ロ requires the death or severe-disability amount to increase progressively with elapsed duration or cumulative premiums | [R10] |
| Payment form | Lump sum, as an annuity, or left on deposit at a declared rate | [S4] |
| Deductions | Unpaid premiums, policy-loan principal and interest, 自動振替貸付 balances | [S2] [S4] |
| Where an exclusion bites | Policy reserve (責任準備金), capped at the death-benefit amount, paid to the policyholder | [S2] |
| Surrender value (解約返戻金) | From 経過年月数, capped at the 払込年月数 while premiums are being paid, and **limited to the death-benefit amount** | [S2] [S4] |
| Consequence | On a 生存保障重視型 contract it can never exceed cumulative premiums paid | [S4] [R16] |
| Early durations | Nil or negligible for an initial period; equal to the death benefit after a period | shape [S2] [S4]; schedule **[std]** (10) |
| Surrender after annuitisation | Not available | [S2] [S4] [R16] |
| Reduction of the 基本年金額 (減額) | Permitted, releasing the surrender value of the reduced portion — but under the rider that amount is **not paid out** | [S1] [S2] [S4] |
| Claim settlement | Within five business days of a complete claim file | [S2] [S4] |

10. Both 約款 read state the shape but not the parameters: 「ご契約後短期間で解約されたときには、解約返還金がない場合があります」
    [S2] and 「まったくないか、あってもごくわずか」, with 「この保険の解約返戻金は、一定期間経過後は死亡給付金と同額になります」 [S4]. Neither
    publishes the period or the schedule; the formula sits in the unpublished 算出方法書
    [REG-R2]. The composite standardizes the *schedule* — `max(0, 保険料積立金 − 解約控除)` capped at
    the death benefit, with the surrender charge (*kaiyaku kōjo*, 解約控除) run off linearly
    over a **[std]** ten initial policy years — while holding both sourced invariants
    exactly: a hard cap at cumulative premiums paid, and a nil-or-negligible value at the
    shortest durations. Only the path between them is [std]. One carrier outside this design
    instead states a duration after which the surrender value **exceeds** cumulative
    premiums [S12], which is possible only because that design is not 生存保障重視型.

### Benefit provisions — payout phase

| Parameter | Representative value | Basis |
|---|---|---|
| 年金原資 | The accumulated fund at the 年金支払開始日 out of which the annuity is bought; one carrier publishes both 一括受取率 (= 年金原資 ÷ 払込保険料総額) and 年金受取率 (= 年金受取総額 ÷ 払込保険料総額) at one model point, pinning the definition down | [S6] |
| Base annuity | 10年確定年金 — paid on the 年金支払開始日 and its nine annual anniversaries, regardless of survival | menu 5/10/15 [S2] [S3] [S9]; pick **[std]** (11) |
| Alternative elected at annuitisation | Life annuity with a guarantee period (*hoshō-kikan-tsuki shūshin nenkin*, 10年保証期間付終身年金) | [S2] [S4] [S9]; period **[std]** (12) |
| 年金支払開始日 | The 年単位の契約応当日 on which the insured's 保険年齢 reaches the 年金支払開始年齢 chosen at issue | [S2] [S4] [S9] |
| When the amount is fixed | At issue for a type chosen at issue; **at annuitisation**, on the 基礎率 then in force, for a type elected at annuitisation | [S2] [S3] [S9] |
| Death during a 確定年金 period | The present value of the unpaid instalments (未払年金の現価) is paid; the recipient may instead elect **continuation** to the end of the term | [S2] [R16] |
| Death inside a guarantee period | The present value of the unpaid guaranteed instalments is paid | [S4] [R16] |
| Commutation (年金の一括払) | From the 年金支払開始日 to the last 年金支払日, at the present value of the remaining certain or guaranteed instalments; the contract then terminates | [S2] [S4] |
| Commutation discount rate | 0.40% p.a. | derived from [S2]; **[std]** (13) |
| After annuitisation | No policy loan, no reduction of the annuity, no surrender; commutation only | [S4] |
| Partial commutation | Refused; where the fund was split across types, a request on one is a request on **all** | [S1] [S4]; required by 所令211①ハ [R10] |

11. The 確定年金 menu is **5 / 10 / 15 years**, chosen at issue, at two of the five carriers
    [S2] [S3] [S9]. **A 5-year 確定年金 is incompatible with the rider** — 所令212第1号 requires
    payments to continue ten years or more [R10] — and one carrier's rider therefore refuses
    a change to a 5-year term outright [S2]. The composite takes **10 years**: the shortest
    qualifying term, the term in every retrieved specimen [S3] [S5] [S6] [S8] [S10], and the
    mode of the menu.
12. Guarantee periods observed: **10 years** at two carriers [S2] [S3] [S9], **5 years**
    on the tontine of the second of those two [S10]. The composite takes 10. That carrier
    attaches the warning worth carrying into any model of the shorter guarantee: on a
    5-year guaranteed life annuity, depending on how long the annuitant survives the
    annuity start, annuity plus death payments can total **below** premiums paid [S10].
13. One carrier's 約款 publishes a 未払年金の現価 factor table — 1.010, 2.016, 3.018, 4.016, 5.010,
    6.000, 6.986, 7.968, 8.946, 9.921, 10.891, 11.858, 12.821, 13.780 for 1 to 14 remaining
    instalments [S2]. Successive first differences fall in a near-constant ratio of 0.99602,
    an implied `i` of about **0.400%**, and the factors are close to an annuity-due at that
    rate scaled by about 1.010. The 約款 then discounts the result from the death or
    commutation date to the day before the next 年金支払日 at a separately **declared** rate
    [S2]. The 0.40% is an inference from published factors, not a published 予定利率, and is
    tagged **[std]** for that reason. The composite reproduces the published factors for the
    anchor cell's ten-year term and uses 0.40% only outside the published range.

### Options

| Parameter | Representative value | Basis |
|---|---|---|
| 個人年金保険料税制適格特約 | Attached in the base run; four attachment conditions, reshaping dividends, refunds, loans, contract changes and paid-up conversion | [S1] [S4] [S9] [S10] [S12] |
| 年金内容変更制度 | One election at annuitisation, between the base type and 10年保証期間付終身年金 | [S4] [S9]; scope **[std]** (14) |
| Splitting the fund (複数年金選択制度) | Available at one carrier; out of scope | [S4]; **[std]** (14) |
| Deferral of the first annuity payment date | Up to five years at one carrier; out of scope | [S9]; **[std]** (14) |
| 年金の自動すえ置 | Instalments falling due automatically left on deposit with interest, at one carrier; out of scope | [S2]; **[std]** (14) |
| Premium waiver (保険料の払込免除) | Excluded | [S4] [S9]; **[std]** (15) |
| 指定代理請求特約 | Out of scope — no cash-flow effect | [S2] |
| 夫婦年金特約 / 夫婦年金移行特約 | Out of scope; contract mechanics [unverified] | [S2] [R16] |

14. Election machinery at annuitisation varies widely and is modelled as a single binary.
    Observed: election between 保証期間付終身年金 and 確定年金 **with the fund splittable across more
    than one type** [S4]; election among 5/10/15年確定年金 or 10年保証期間付終身年金, subject to the type
    still being offered and the annuity clearing the insurer's minimum [S9]; a 10年保証期間付終身年金
    reachable only through a rider, whose amount is set on the 基礎率 in force at the 年金支払開始日
    [S2] [S9]; automatic deposit of instalments [S2]; and deferral of the first payment date
    by up to five years [S9]. The composite implements one election — 10年確定年金 (default)
    versus 10年保証期間付終身年金 — with a **[std]** take-up assumption in the technical notes, and
    excludes the rest. Excluding the split is not cosmetic: where the fund *is* split and
    the rider is attached, a commutation request on one tranche is a request on all [S1], so
    a split model needs a joint commutation state.
15. The waiver observed at one carrier waives future premiums on the 約款-defined 高度障害状態 or a
    listed 身体障害の状態 from an accident within 180 days — but **not** where the 無選択特則 is
    attached [S4]. Another sells it as a rider triggered by the three major diseases [S9].
    The composite is built on the no-underwriting chassis, on which that carrier's own
    wording removes the waiver [S4], so it is excluded. Note the interaction: triggering a
    premium waiver is one of the events that causes the 税制適格特約 itself to be **deemed to have
    lapsed** [S1].

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 契約者配当 | Declared from the sixth policy year then every five years, and on death, surrender, reduction and commutation. **Zero** in the base run | [S4]; base run **[std]** (16) |
| Dividends before annuitisation | Accumulated at a declared 配当積立利率 and applied to increase the 基本年金額; **cannot be withdrawn** under the rider | [S1] [S2] [S4] [S12]; required by 所令211①ニ [R10] |
| 自動振替貸付 | Optional module, off in the base run | present [S4], absent [S2]; **[std]** (17) |
| Grace (払込猶予期間) | Monthly: to the last day of the month after the 払込期月. Annual and semi-annual: to the monthly contract anniversary of the second following month | [S4]; annual-grid mapping **[std]** (18) |
| Lapse (失効) | Effect lost from the day after grace expires, where the premium is unpaid and no 自動振替貸付 is made | [S4] |
| Reinstatement (復活) | Within **three years** of lapse and only before the 年金支払開始日; all arrears plus late interest in one sum, and fresh 告知 (waived under the 無選択特則) | [S2] [S4] |
| Paid-up (払済年金保険) | Premiums stop, the 基本年金額 is redefined from the surrender value, the 年金支払開始日 is unchanged, the death benefit held at its value at conversion. **Refused inside the first ten policy years under the rider** | [S1] [S2] [S4] [S12] |
| Reversal (復旧) | Within three years of a paid-up conversion or a reduction | [S4] |
| Suicide exclusion (自殺免責) | No death benefit where the insured takes their own life within **three years**, counted inclusively, from the 責任開始日 — or from the last 復活日 | [S2] [S4] |
| 告知義務違反 | Rescission within **two years** of the 責任開始日 or 復活日, and within one month of discovery | [S4]; statutory ceiling five years [REG-R35] |
| 詐欺・不法取得目的 | Contract void; premiums not refunded | [S2] [S4] |
| クーリング・オフ | Eight days from the later of application and delivery of the disclosure documents. Out of scope | [S4] [REG-R36] |

16. Dividends are contractual in form but discretionary in amount, and 消費者契約法第4条 makes it
    actionable to present a non-guaranteed element as certain [REG-R38] — which is why a
    Japanese illustration separates 保証 from 非保証 elements. One carrier's declared 社員配当金の積立利率
    was **年0.60%** as at 2026年4月2日, the same rate it applies to refunds arising on a
    tax-qualified annuity [S11]. No retrieved document publishes a dividend *rate* on this
    line. The composite keeps the machinery — accumulation at a declared rate, no withdrawal
    before annuitisation, application as a single premium increasing the 基本年金額 — and sets
    the declared dividend to **zero** in the base run, exposed as an assumption-class-(b)
    input. Two sourced facts constrain any non-zero run: one carrier pays no dividend at all
    on surrender or reduction within the first two policy years, and states that the
    dividend on surrender is smaller than the one on death [S4].
17. 自動振替貸付 is **product-specific, not universal** — the clearest divergence in the set. One
    carrier operates it: the insurer automatically lends the unpaid premium against the
    surrender value, compound at a rate reviewed twice yearly and capped at 年8%, keeping the
    policy in force unless the policyholder has opted out [S4]. Another states outright
    「この保険には、保険料の自動貸付の取り扱いはありません」 [S2]. 監督指針 IV-1-12 requires the facility to be **at the
    policyholder's election**, with prompt notice when exercised [REG-R14]. The composite
    therefore implements it as an **optional module, off in the base run**, never as an
    automatic no-lapse rule. It changes the lapse mechanic outright: while the surrender
    value can carry the premium, a policy on the module does not lapse at the end of grace,
    and the loan balance is then deducted from the death benefit or the 年金原資.
18. Grace is published only in monthly-anniversary terms [S4]: **monthly** premiums, from
    the first day of the month after the 払込期月 to the **last day of that month**; **annual
    and semi-annual**, from the first day of the next month to the monthly contract
    anniversary of the month after that, with special handling where the anniversary falls
    on the last day of February, June or November (running then to the last day of April,
    August or January). On an annual grid the composite maps this to a **[std]** rule: a
    premium unpaid at `t` terminates the contract at `t` unless the 自動振替貸付 module is on,
    with no partial-year grace state. One further sourced fact does not survive the annual
    grid and is recorded here because the monthly-grid products reuse it: where a death
    claim or waiver trigger arises during grace on a monthly direct-debit contract, **two
    months** of premium are deducted from the claim or must be paid [S4].

---

## Contractual mechanics

### Timing, premiums, grace, lapse and reinstatement

Two dates govern everything. The date cover attaches (*sekinin kaishi-bi*, **責任開始日**)
starts the suicide-exclusion and contestability clocks [S2] [S4]. The **年金支払開始日** is the
年単位の契約応当日 on which the insured's 保険年齢 reaches the 年金支払開始年齢 chosen at issue, and the 年金支払日
are that date and its annual anniversaries [S2] [S4] [S9]. Almost no mechanic survives it:
surrender, policy loans, reduction and reinstatement all stop there, leaving commutation as
the annuitant's only remaining lever [S2] [S4] [R16]. On the annual grid, write `t` for
years since issue, `m` for the premium term (30 at the anchor cell), `d` for the 据置期間 (5)
and `n = m + d` (35). Premiums fall at `t = 0 … m − 1`; the fund accumulates over `t = 0 …
n`; the annuity is paid at `t = n … n + 9`.

The office premium is level and guaranteed for the whole 保険料払込期間 [S2] [S4] [S5] [S6]; the
only in-force mechanisms that change it are 減額 and paid-up conversion, both constrained by
the rider, and there are no premium reviews on this chassis. Where a premium is unpaid at
the end of the 払込猶予期間 the contract lapses the following day, unless the 自動振替貸付 module is in
force and the surrender value can carry the premium [S4]. Where loan principal and interest
come to exceed the surrender value the insurer demands a payment, and the contract lapses
**from the moment the excess arose** if it is not made by the deadline [S4]. A lapsed
contract may be reinstated within three years, and only before the 年金支払開始日, on payment of
all arrears plus late interest in one sum and on fresh 告知 — waived under the 無選択特則; cover
restarts when the insurer accepts and receives the money [S2] [S4]. Reinstatement is barred
once a refund equal to the surrender value has been claimed [S2]. **Japanese policies really
do come back**: a model that treats lapse as absorbing is modelling a different product, and
the reinstated policy carries a fresh three-year suicide clock from the 復活日 [S2] [S4].

### Death benefit during deferral

The composite's deferral-phase death benefit is cumulative premiums paid:

    DB(t) = P * min(t, m)          (annual grid; P = the level annual premium)

which is the annual-grid form of the contractual 月払保険料 × 経過月数 [S2] [S4] and of the 既払込保険料相当額
wording a third carrier uses [S6]. The three market designs [R16] differ only in the
multiplier on that base: **生存保障重視型** holds the benefit down *to* cumulative premiums, buying
a larger annuity; a **tontine** holds it to about **70%** of them, buying a larger annuity
still; a third family adds a 災害死亡給付金 at an uplift (e.g. 110%). The composite takes the
first.

The shape is not a marketing choice. 所得税法施行令第211条第1号ロ requires that, on a
deduction-qualifying annuity, the death or severe-disability amount **increase
progressively** with elapsed duration or cumulative premiums [R10]; a level sum assured
would disqualify the contract. Unpaid premiums, policy-loan principal and interest and any
自動振替貸付 balance are deducted [S2] [S4], and the benefit may be taken as a lump sum, as an
annuity, or left on deposit [S4]. Where an exclusion bites — suicide inside the three-year
window, or death caused intentionally by the policyholder or by the beneficiary — one 約款
pays the **責任準備金 instead, capped at the death-benefit amount**, to the policyholder [S2];
where the beneficiary caused the death the remaining beneficiaries are paid their shares
[S2] [S4]. The three-year 免責期間 is a **contractual narrowing**: 保険法第51条第1号 excludes suicide
with **no time limit at all**, so the familiar Japanese window is the 約款 giving cover back,
not the statute taking it away [REG-R34]. Its length is a per-carrier fact and is tagged as
one.

### Surrender value during deferral

Surrender is available only before the 年金支払開始日 [S2]. The value is computed from 経過年月数,
capped at the 払込年月数 while premiums are being paid, and is **limited to the death benefit
amount** — 「解約返還金は…死亡給付金の額を限度とします」 [S2]. The second carrier makes the same point from the
other side: where the fund accumulated for future annuity payments exceeds the death
benefit, the surrender value is paid only up to the death benefit, so the policyholder
receives less than the accumulated fund [S4]. The composite carries the ceiling as a hard
constraint:

    CV(t) = min( max(0, 保険料積立金(t) - 解約控除(t)), DB(t) )

Two consequences must be reproduced rather than smoothed. First, on a 生存保障重視型 contract the
surrender value **can never exceed cumulative premiums paid** [S4] [R16]: the accumulated
fund runs ahead of the ceiling and is clipped by it, so beyond some duration surrender value
and death benefit are *the same number*, exactly as one carrier states [S4]. A model in
which the surrender value strictly exceeds the death benefit at any deferral duration is
wrong. Second, the ceiling is how the product funds a larger annuity: what the policyholder
gives up on death and surrender is what buys the survival benefit. A tontine takes the same
idea further — 70% of cumulative premiums, so surrender is loss-making at **every** duration
[S3] [S10].

### 年金原資, the annuitisation election and the payout phase

The 年金原資 is the accumulated fund at the 年金支払開始日 out of which the annuity is bought. One
carrier pins the definition down by publishing, for one model point, both the **一括受取率** (=
年金原資 ÷ 払込保険料総額) and the **年金受取率** (= 年金受取総額 ÷ 払込保険料総額) [S6]; the gap between the two —
115.9% against 118.2% at the anchor model point — is the interest earned over the ten-year
payment period, and it is the cleanest published check on a payout-phase basis in the
retrieved set.

For a type chosen **at issue** the annuity amount was fixed at issue on the 予定利率 then
applied [S2] [S3]. For a type elected **at annuitisation** — notably 保証期間付終身年金 — it is
computed on the 基礎率 (予定利率, 予定死亡率 and the rest) in force at the 年金支払開始日, and is therefore
*not* determined at issue [S2] [S9]. That asymmetry is a modelling instruction: the base
確定年金 is a guaranteed stream from issue, while the life-annuity election is an option on the
insurer's future basis, and the two cannot share one treatment.

**確定年金** instalments are paid on each 年金支払日 independent of survival. If the insured dies
during the payment period before the last instalment, the present value of the unpaid
instalments is paid to the nominated 未払年金現価受取人, who may instead elect **continuation** of
the instalments to the end of the term [S2] [R16]. So the 確定年金 payout phase carries **no
mortality decrement on the cash flow** — only on its recipient. That is the most
consequential structural fact about this product's payout phase, and it is why the base run
needs no payout-phase mortality table at all. **保証期間付終身年金** instalments are paid for life;
inside the guarantee period payment does not depend on survival, and death inside it pays
the present value of the unpaid guaranteed instalments [S4] [R16]. There mortality does
bite, from the end of the guarantee onward, and with a different valuation table from the
deferral phase — see *Regulatory context*.

**年金の一括払.** From the 年金支払開始日 to the last 年金支払日 the annuitant may take the present value of
the remaining instalments — the remaining payment period for 確定年金, the remaining guarantee
period for 保証期間付終身年金 — as a lump sum, terminating the contract [S2] [S4]. Where the fund was
split and the rider is attached, a request on one type is a request on **all** [S1], and
partial commutation of one type alone is refused [S4]: the contractual expression of 所令211①ハ
[R10]. After annuitisation no policy loan is available, the annuity may not be reduced and
the contract may not be surrendered [S4] [R16]. Any outstanding loan is settled at the
年金支払開始日 — netted off a commutation lump sum, deducted from successive instalments [S4], or,
where the balance exceeds a stated amount, deducted from the 責任準備金 with the net paid as a
lump sum that terminates the contract [S1] [S2]; where it is netted off the reserve, the
residual reserve redefines the annuity, and if that falls below the insurer's minimum it is
paid as a lump sum instead [S4].

### 税制適格特約 — the rider that shapes the product

**The four attachment conditions**, verbatim from one rider's 第1条 [S1]:

1. 年金受取人は保険契約者またはその配偶者のいずれかであること
2. 年金受取人は被保険者と同一人であること
3. 保険料払込期間は10年以上であること
4. 年金の種類が確定年金または保証期間付有期年金の場合、年金支払開始日における被保険者の年齢は60歳以上で、かつ、年金支払期間は10年以上であること

Two of the five carriers state the same four in the same order — the rider itself [S1] and a
second carrier on both its product pages [S9] [S10]; a third splits them into an 所得税法 limb
and an 所得税法施行令 limb, adding that condition 4 **does not apply to 保証期間付終身年金** [S4] —
consistent with 所令212第2号, which qualifies a lifetime annuity without any term test [R10].

**How they map onto the statute** [R9] [R10] [R11] [R12]. Condition 1 is 所法76⑧一 — the
recipient is the premium payer or, where alive, their spouse. Condition 3 is 所法76⑧二 —
premiums paid periodically over ten years or more **before the annuity payment start date**.
Condition 4 is 所令212第1号 — payments begin on or after a contract-stated date falling on or
after **1 January of the year in which the recipient turns 60** (moved back to 1 July of the
previous year where the 60th birthday falls between 1 January and 30 June) and continue for
ten years or more. Condition 2 — 年金受取人 = 被保険者 — is **not** in the retrieved statutory text:
所法76⑧ ties the recipient to the payer or spouse [R9], 所令211 and 212 govern the payment
structure and the recipient's age [R10], and the tax authority's restatement does not
mention it either [R12]. Three of the five carriers state it [S1] [S4] [S9] [S10] — every
carrier whose documents state the conditions at all — and it is best read as the industry's
way of making the age-60 test operable on the policy's own age basis.
Treat the *statutory* status of condition 2 as [unverified]; its *contractual* status is
fully sourced.

**The contract-design conditions the rider must also satisfy** — 所令211第1号 [R10]: **イ** no
cash payment other than the annuity, except on death or severe disability (dividends and
surrender value excepted) — one carrier's own summary is
「年金以外の金銭によるお支払いは、死亡給付金（死亡保険金）、高度障害保険金、解約返戻金に限ること」 [S4]; **ロ** the death or severe-disability
amount must **increase progressively** with elapsed duration or cumulative premiums, which
is why the death benefit is 月払保険料 × 経過月数 [S2] [S4] rather than a level sum assured; **ハ**
annuities paid at least yearly throughout the payment period, and **no partial
commutation**; **ニ** no cash distribution of dividends before the 年金支払開始日 beyond that year's
premium.

**What attaching it does** [S1] [S2] [S4] [S9] [S12]. The 年金受取人 may not be changed. Changes
that would breach the conditions are refused, including bringing the premium term below ten
years and changing to a 5-year 確定年金. Paid-up conversion is allowed only after ten years of
premiums have been paid. Any refund arising on a change — a 減額, cancellation of another
rider, the residue of prepaid premiums — is **not paid out**: it is accumulated at a
declared rate to the 年金支払開始日 and applied as a single premium increasing the 基本年金額, reaching
the policyholder or the death-benefit beneficiary only if the contract terminates before
annuitisation. One carrier publishes the rate applied to exactly this amount —
税制適格型年金保険の払戻金等の積立利率, 年0.60% as at 2026年4月2日 [S11]. On a 減額 the loan is **not** netted off
the payment, and a 減額 that would leave the loan exceeding the surrender value is refused
outright [S1] [S2]. Dividends before annuitisation are accumulated and applied to increase
the annuity and cannot be drawn. The rider **cannot be surrendered on its own** —
「この特約のみの解約はできません」 [S1] [S4] — and is **deemed to have lapsed** when the main contract
terminates, when the premium waiver is triggered, or when a change of policyholder breaks
condition 1 [S1].

**What it buys, and what the benefits then cost.** The premium enters the 個人年金保険料控除 basket
rather than the 一般 basket [S12] [R16]. Each basket deducts the whole premium to ¥20,000,
then ¥20,000 plus half the excess to ¥40,000, then ¥30,000 plus a quarter of the excess to
¥80,000, then a flat **¥40,000**, with the three capped together at **¥120,000**; the
residence-tax schedule is lower and caps at ¥28,000 per basket and ¥70,000 overall, and
支払保険料等 is premiums **net of dividends received or accumulated that year** [REG-R43] [R11]
[S4]. At the anchor cell's ¥180,000 the basket is saturated several times over, which is the
ordinary case and is why the deduction shapes *whether* a household buys the product rather
than how much. On the benefit side, where payer and annuitant coincide the annuity is
**雑所得** — the annuity less the matching premium, the fraction being total premiums over
total (or expected total) payments, fixed at the annuity start date and rounded up at the
third decimal [R10] [R13] [S4] — with withholding at 10.21% of the excess and none where
that excess is under ¥250,000 for the year [R13]. A lump sum taken **instead of** the future
annuity, before or after the start date, is **一時所得** [R13] [REG-R46], which is why the
commutation-versus-annuity election is a tax decision and not a coin flip. Where payer and
annuitant differ the right is deemed gifted and gift tax applies, with a stepped income-tax
schedule thereafter keyed to the 相続税評価割合 [R13] [R14] [S4]. The deferral-phase death benefit
is 相続税 where 契約者 = 被保険者, 所得税（一時所得）where 契約者 = 受取人, and 贈与税 where all three differ [S4].
`jplib` models contractual cash flows, not the policyholder's tax position; these facts are
carried because they drive the annuitisation and commutation assumptions.

---

## Riders and options

A Japanese policy is a main contract (*shu-keiyaku*, 主契約) with riders (*tokuyaku*, 特約)
attached, and which of the two a mechanic sits in decides whether it is in scope here.

**In scope (modelled or parameterized):**

- **個人年金保険料税制適格特約** — attached in the base run and load-bearing on the product's shape, not
  merely on its tax treatment: it forces the ten-year premium term, the age-60 annuity-start
  floor, the ten-year payment period, the progressively-increasing death benefit, the
  no-partial-commutation rule and the ten-year bar on paid-up conversion [S1] [S4] [R9]
  [R10].
- **年金内容変更制度** — the single election at annuitisation between 10年確定年金 and 10年保証期間付終身年金, the
  latter priced on the basis in force at the 年金支払開始日 [S2] [S4] [S9]; take-up is a **[std]**
  behavioural assumption in the technical notes.
- **年金の一括払** — modelled from the 年金支払開始日 at the published 未払年金の現価 factors [S2], with take-up
  a **[std]** behavioural assumption.
- **契約者貸付** — an optional module at a declared 2.40% [S11], hard-capped at the surrender
  value [S4] [REG-R14].
- **自動振替貸付** — an optional module, **off in the base run**, because it exists at one carrier
  [S4] and expressly does not at another [S2], and because 監督指針 IV-1-12 requires it to be a
  policyholder election rather than an automatic rule [REG-R14].
- **減額 and 払済** — described with the rider's constraints applied (no release of the refund;
  no paid-up conversion inside ten years); neither is exercised in the base run **[std
  scope]** [S1] [S2] [S4].

**Out of scope:** 複数年金選択制度 [S4]; deferral of the first annuity payment date [S9]; 年金の自動すえ置
[S2]; 保険料の払込免除 and the three-major-disease waiver rider, removed in any event by the 無選択特則
the composite is built on [S4] [S9]; 指定代理請求特約 [S2]; 夫婦年金特約 and 夫婦年金移行特約, whose own
conditions live in a booklet that was not retrieved, so anything beyond "either spouse's
survival keeps the annuity in payment, usually with a roughly ten-year guarantee" is
[unverified] [S2] [R16]; 前納 of three or more annual premiums [S4] [S11]; temporary annuity
(*yūki nenkin*, 有期年金), which survives in the taxonomy [R16] and in one rider's
contemplation of 保証期間付有期年金 [S1] but which **no retrieved carrier product offers today**, so
"有期年金 is sold in the current market" is [unverified]; 年金総額保証付終身年金 [R16]; and クーリング・オフ, an
eight-day dispatch-rule withdrawal right on every contract of this term [S4] [REG-R36],
scoped out explicitly rather than silently omitted — the model begins where cover is in
force.

---

## Variations across insurers

1. **Annuity types at issue.** 確定年金 5/10/15 only, with 10年保証期間付終身年金 through a rider [S2];
   確定年金 and 保証期間付終身年金（定額型）both at issue [S4]; 確定年金, ten-year in every published example [S5]
   [S6]; 確定年金 5/10/15 [S9]. Composite: **10年確定年金 at issue, 10年保証期間付終身年金 electable at
   annuitisation** — the shape all four support, and the only one on which "fixed at issue"
   and "priced at annuitisation" can both be modelled.
2. **Deferral-phase death benefit.** 月払保険料 × 経過月数 at two carriers [S2] [S4]; 既払込保険料相当額 at a
   third [S6] — the same idea in different words; 70% of cumulative premiums on one tontine
   [S3]; **no death cover at all** on another tontine, where the death payment equals the
   surrender value [S10]; and a fifth carrier whose death benefit runs only to the end of
   premium payment [S12]. Composite: **cumulative premiums paid** — held by three of the
   five carriers, and the design 所令211①ロ is written for [R10].
3. **Surrender ceiling.** At or below the death benefit at two carriers [S2] [S4], one
   adding that after a period the two are equal [S4]; below premiums paid during the premium
   period at a third [S6]; a 70% suppression, always below premiums, on a tontine [S10]; and
   one carrier stating a duration after which the surrender value **exceeds** cumulative
   premiums [S12]. Composite: the death-benefit cap, exactly as the two 約款 state it.
4. **予定利率 disclosure and structure.** Two carriers publish before-and-after rates in pricing
   releases [S5] [S8]; two publish nothing on the retrieved documents [S2] [S4]; one
   publishes only a minimum-guarantee rate [S12]. One publisher **bands the deferral rate by
   years remaining to annuitisation** (1.20% at 30 years or more, 1.00% below) and publishes
   a separate, unchanged post-annuitisation rate of 0.65% [S5]. Composite: a single deferral
   rate of 1.00% and a separate payout rate of 0.65%, with the banding exposed as an input
   rather than hard-coded (footnotes 6 and 7).
5. **Rate-resetting designs.** One carrier refreshes the whole basis once, at a stated
   duration, subject to a minimum-guarantee 予定利率 of 0.50% fixed at issue, with the 年金原資
   moving with it and a 金利キャッチアップ配当 when new-business rates rise [S12]. This is a regulatory
   construction, not a flourish: 保険業法施行規則第68条 excludes from the 標準責任準備金 regime any contract
   whose 約款 lets the insurer change the 予定利率 — **except** where the 約款 guarantees a floor at
   or above the standard valuation interest rate (*hyōjun riritsu*, 標準利率) applicable at
   issue [R5] [REG-R7]. The minimum guarantee is what keeps the contract inside the
   standard-reserve regime. Composite: excluded; the composite's
   予定利率 is fixed at issue.
6. **自動振替貸付 and 契約者貸付.** The automatic premium loan is present, compound and capped at 年8%
   at one carrier [S4] and expressly absent at another [S2]. The contract-loan rate is
   published by issue-date cohort, 3.05% down to 2.00% and back up to 2.40% from 2025-01-02,
   at one carrier [S11] [S8], and described only as declared and reviewed each January and
   July at another [S4]. Composite: 2.40%, with the automatic premium loan an optional
   module off in the base run (footnotes 9 and 17).
7. **Tontine annuities (トンチン年金).** The sharpest variation in the set, and a distinctively
   Japanese design. One is a 5年ごと配当付生存保障重視型個人年金保険: 契約年齢 50–80, 年金支払開始年齢 60–90, 保険料払込期間 5–30
   years, すえ置期間 ≤ 15 years, contract-to-annuitisation ≤ 30 years, 10年保証期間付終身年金 or 確定年金
   5/10/15, a **死亡返還金 fixed at 70% of cumulative premiums**, a surrender refund capped at
   that, and no underwriting [S3]. The other is a 長寿生存保険（低解約払戻金型）: 契約年齢 male 50–87 / female
   50–86, 5年保証期間付終身年金 or 10年確定年金, **no death cover as such** —
   「死亡保障を行わないため…解約払戻金と同額の死亡払戻金しか支払われません」 — and a **70% suppression ratio** on the surrender
   value itself [S10]. The first carrier prices the *same model point* on its tontine and
   its ordinary annuity — 50-year-old male, premiums to 65, annuity from 75, ¥50,000 a
   month, 10年確定年金 — giving ¥1,024,500 a year at a 113.8% 返還率 against ¥948,600 at 105.4%
   [S3]. **The tontine buys about 8% more annuity for the same premium by giving up 30% of
   the death and surrender floor**, and that is the whole economics of the design. A second
   signature: on the 70%-suppressed design the **female premium exceeds the male** at every
   issue age for the same guaranteed annuity — male ¥14,622 against female ¥14,904 monthly
   at issue age 50, ¥17,784 against ¥18,132 at 55, ¥22,572 against ¥22,998 at 60 [S10] — and
   the same direction runs through that carrier's own rate-change release for the same
   product [S8]. With the death benefit suppressed, the longer-lived sex must pay more.
   Composite: **excluded**, but built so
   that the tontine is a *parameterization* of it rather than a different chassis — a
   death-benefit ratio of 0.70 instead of 1.00 on the same cumulative-premium base, under
   the same surrender ceiling. `Annuity_JP_A` carries the ratio as a model-point field. One
   of the two is sold explicitly as a 低解約返戻金型 product [S10], a category 監督指針 IV-1-9 names as
   needing extra explanation [REG-R14] and one of the three features 金融サービス提供法第4条 requires
   to be explained as a restriction on cancellation [REG-R39]; `jplib`'s 低解約返戻金型 cliff
   itself lives in the [whole life technical notes (終身保険)](../whole_life/technical-notes.md).
8. **Underwriting.** No 告知 at all on one carrier's annuity or on its tontine [S2] [S3]; a
   無選択特則 at a second which, attached, removes both the disclosure duty and the premium
   waiver [S4]; a 保険料払込免除特約 for the three major diseases at a third [S9]. Composite: no
   underwriting, no waiver.
9. **Variable and foreign-currency annuities — the scope boundary.** 変額個人年金保険 runs in a 特別勘定
   with the market risk on the policyholder; the annuity fund and total payments may or may
   not be guaranteed, surrender values usually are not, death benefits are usually
   guaranteed at premiums paid, and the account normally moves to the 一般勘定 at annuitisation
   so the annuity is fixed from then on [R17]. Foreign-currency and MVA annuities exist in
   the same market and likewise place market risk on the policyholder [R16]. Both are
   excluded here, and the exclusion is regulatory as well as practical: a contract whose
   reserve varies with 特別勘定 assets sits **outside** the 標準責任準備金 regime altogether [R5]
   [REG-R7], though its minimum guarantee sits inside it; foreign-currency contracts were
   brought inside only by the 2021 amendment, from 2021-10-01 and, for the second limb,
   2022-04-01 [REG-R12]; and both are 特定保険契約, so their sales conduct is FIEA-grade
   [REG-R37]. Single-premium business is excluded on the same principle: its rate mechanics
   are different in kind, reset twice monthly for new business and then at stated 予定利率計算基準日,
   floored by a minimum guarantee and pegged to named JGB benchmarks [S13] — and no
   annuity-specific single-premium 予定利率 was retrieved, so any such figure would be
   [unverified].
10. **Distinctive single-carrier features, all excluded but one.** A published 未払年金の現価
    factor table and 年金の自動すえ置 [S2]; 複数年金選択制度 [S4]; 据置期間 marketed as an explicit
    annuity-increasing lever, with 一括受取率 published alongside 年金受取率 [S6]; deferral of the
    first annuity payment date by up to five years [S9]; a 予定利率 refreshed once mid-contract
    with a floor [S12]. Only the factor table is used, as the source of the commutation
    basis (footnote 13).
11. **What does not vary.** Every retrieved carrier fixes the annuity at issue for a type
    chosen at issue; suppresses the deferral-phase death benefit to **at most** cumulative
    premiums paid; **caps the surrender value at that death benefit**; offers commutation of
    the remaining certain or guaranteed instalments; states the same four tax-qualification
    conditions; and stops policy loans and annuity reductions at the 年金支払開始日 [S1] [S2] [S3]
    [S4] [S6] [S9] [S10] [S12]. Those six are the invariant core of the composite, and each
    is a testable model property.

---

## Regulatory context

**Prudential — ESR, and what it replaced.** From **2026-03-31** insurers are supervised on
the economic-value-based solvency regulation (*keizai-kachi bēsu no soruvenshī kisei*,
経済価値ベースのソルベンシー規制, ESR), applied from the 2026年3月期 accounts on a three-pillar structure. Early
corrective action triggers when the **ESR falls below 100%**, where the old regime triggered
when the ソルベンシー・マージン比率 fell below **200%** [REG-R15] [REG-R17]. Under ESR assets are at fair
value and liabilities are re-measured at each 基準日 as **current estimate (現在推計) plus MOCE**,
against the old ロックイン basis on which mortality, lapse, incidence and interest were fixed at
issue; required capital is calibrated to **99.5%** over one year [REG-R15]. `jplib` computes
neither ratio. What this product owes the regime is that its projection is re-runnable on a
basis re-set at a stated 基準日 — for a 35-year deferral followed by a ten-year payout, not a
small property.

**Statutory reserving.** 保険業法第116条第1項 requires a 責任準備金 at each period end and 第2項 delegates
the method and coefficient levels for long-term contracts [REG-R4]. 保険業法施行規則第68条 fixes which
contracts are inside the 標準責任準備金 regime — excluding contracts whose reserve varies with 特別勘定
assets, and contracts whose 約款 lets the insurer change the calculation coefficients, with a
carve-out where the 約款 guarantees a floor at or above the 標準利率 applicable at issue [R5]
[REG-R7]. 第69条 gives the taxonomy — 保険料積立金, 未経過保険料, 払戻積立金 and 危険準備金 [REG-R8]. The method and
rates are in 平成8年大蔵省告示第48号: accumulation on the net level premium method (*heijun
jun-hokenryō-shiki*, **平準純保険料式**) with no Zillmer adjustment, the standard rate reset annually on a
1 October 基準日 from JGB yields with banded safety coefficients, and the mortality table the
指定法人 produces for the contract's vintage [REG-R10] [REG-R23]. **The current numeric 標準利率
could not be established from a retrieved official document** — the mechanism is verified,
the level is not, so any figure used downstream is **[std]** or [unverified] [REG-R10]. This
library projects gross cash flows and builds none of these reserves; they are cited, not
reproduced. The appointed actuary (*hoken keirinin*, 保険計理人) must submit an 意見書 confirming
the reserve is properly accumulated [REG-R6], and the 実務基準 sets out how: the **1号収支分析** is a
forward income-and-outgo analysis run annually by 区分経理 segment over **at least ten future
years**, with sufficiency tested against the standard reserve being accumulable at each year
end over the first five [REG-R22]. That is precisely the shape `Annuity_JP_A` produces.

**The two valuation tables, and why this product needs both.** For contracts concluded from
2018-04-01 the standard-reserve mortality basis is 生保標準生命表2018（死亡保険用）for death cover — and
**生保標準生命表2007（年金開始後用）**, expressly **not** updated in 2018, for annuities in payment
[REG-R10] [REG-R11]. The 2018 file published by 日本アクチュアリー会 contains exactly four tables —
死亡保険用 男/女 and third sector (*dai-san-bun'ya*, 第三分野) 男/女 — and **no 年金開始後用 table at all** [R2] [REG-R18]; the only public,
machine-readable source located for the 年金開始後用 table is the combined Excel workbook [R3]
[REG-R19]. The IAJ confirmed on 2025-12-18 that all three continue to apply for FY2026 [R4].
The annuity table is materially **lighter** than the death-cover table at every adult age —
male q80 = 0.03357 against 0.05006, male q90 = 0.08318 against 0.15760 — and runs to
terminal ages of **122 (male) and 126 (female)** against 109 and 113 [R3] [REG-R18]. So this
product's accumulation and payout phases read **different tables**, in opposite prudential
directions, and an annuity reserve computed off the death-cover table is wrong by
construction. Two constraints apply to both. They are **valuation** tables carrying an
explicit roughly-2σ margin and a forward improvement allowance, built for a 保険年齢 basis
[REG-R20], so any best-estimate basis is a **[std]** adjustment of a sourced table. And the
publisher's terms **prohibit reproduction and transmission to third parties without written
consent** [REG-R21] — `jplib` therefore cites the tables by URL, quotes only the individual
rates a worked example needs, and ships `mort_table.csv` as a **[std]** construction whose
`provenance` column points at [REG-R18] and [REG-R19]. It does not ship the tables.

**Conduct and classification.** This is 第一分野 business [REG-R1]. It is **not** a 特定保険契約: the
possibility of receiving less than total premiums paid arises here from the surrender
ceiling and from early surrender, not from movements in interest rates, currency values or
market prices, so 保険業法第300条の2 does not attach — while it emphatically does attach to the 変額
and 外貨建 annuities this composite excludes [REG-R37]. The eight-day クーリング・オフ of 保険業法第309条
runs from the later of the application date and delivery of the disclosure documents, and
takes effect **on dispatch** [S4] [REG-R36]. 監督指針 II-4-2-2 fixes what the 契約締結前交付書面 must
carry — 商品の仕組み, 保障の内容 with its 支払事由 and 免責事由, 付加できる主な特約, 引受条件, 保険料, 配当金に関する事項 and
**解約返戻金等の水準**, plus クーリング・オフ, 告知義務, 責任開始期, the main non-payment cases and
**保険料の払込猶予期間、契約の失効、復活** in the 注意喚起情報 [REG-R14]. 消費者契約法第4条 makes 断定的判断の提供 — presenting an
uncertain future amount as certain — a ground for rescission [REG-R38], which is the legal
reason a Japanese illustration separates 保証 from 非保証 elements and the reason this library
splits assumption class (a) from class (b), and 金融サービス提供法第4条's 説明義務 expressly covers any
**restriction on cancellation** [REG-R39]. Contractual limits sit inside statutory ones: the
three-year 自殺免責 narrows an exclusion with no statutory time limit [REG-R34], and the
two-year 告知義務違反 window sits inside the statutory ceiling of five years from inception, with
a one-month clock from discovery [REG-R35]. Where a 相互会社 distributes surplus it must do so
per contract category by one of four permitted methods, of which 「剰余金の生じた原因に応じて」 is the
statutory form of the three sources of surplus (*san-rigen*, 三利源) dividend; the article does
not name 死差, 利差 or 費差 and neither does the 監督指針 [REG-R9], so this library uses the
vocabulary without attributing it to a regulatory text.

**Tax, protection and accounting.** The product exists in this shape because of 所得税法第76条 —
three baskets of ¥40,000 capped at ¥120,000 [REG-R43] — reached through 所法76⑧ [R9] and
所令211・212 [R10], restated at [R11] and [R12], with benefit taxation at [R13], [R14] and
[REG-R46]. The insolvency backstop is the 生命保険契約者保護機構, covering **90% of the 責任準備金等** at the
failure date, with a reduced rate for 高予定利率契約 whose detail is [unverified]; the 90% is set
in ordinance under the delegation in 保険業法第270条の3, not in the statute [S4] [REG-R40]
[REG-R41]. Japan has **no mandatory IFRS 17**: IFRS applies as 指定国際会計基準 and adoption is
voluntary [REG-R47]. Statutory accounts are J-GAAP with 責任準備金 on the 平準純保険料式 [REG-R10]; ESR
is a separate regulatory measurement, not an accounting standard [REG-R15]. Three bases, one
set of projected cash flows — this library projects the cash flows and treats discounting,
margins and tax as configuration layered on top.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #jplib-individual_annuity-r10
[R11]: #jplib-individual_annuity-r11
[R12]: #jplib-individual_annuity-r12
[R13]: #jplib-individual_annuity-r13
[R14]: #jplib-individual_annuity-r14
[R15]: #jplib-individual_annuity-r15
[R16]: #jplib-individual_annuity-r16
[R17]: #jplib-individual_annuity-r17
[R2]: #jplib-individual_annuity-r2
[R3]: #jplib-individual_annuity-r3
[R4]: #jplib-individual_annuity-r4
[R5]: #jplib-individual_annuity-r5
[R9]: #jplib-individual_annuity-r9
[REG-R1]: #jplib-reg-r1
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R12]: #jplib-reg-r12
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R19]: #jplib-reg-r19
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R23]: #jplib-reg-r23
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
[REG-R46]: #jplib-reg-r46
[REG-R47]: #jplib-reg-r47
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[REG-R9]: #jplib-reg-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
