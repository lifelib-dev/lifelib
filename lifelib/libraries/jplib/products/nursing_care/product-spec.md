# Product Specification

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents: policy conditions (*yakkan*, 約款),
policy booklet (*go-keiyaku no shiori*, ご契約のしおり), pre-contract disclosure (*keiyaku
teiketsu-mae kōfu shomen*, 契約締結前交付書面), product brochure (商品パンフレット) and product pages) and [R#]
(product-specific regulatory, statistical and actuarial references), both numbered per
`_research/nursing-care.md` and resolved in `sources.md` (same directory; numbering frozen,
never renumbered), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) —
were extracted from the cited document. Values marked **[std]** are standardizations
introduced for the reference implementation; each [std] table row carries a numbered
footnote giving the rationale and the observed range across insurers. Facts the research
file could not verify are flagged [unverified]. The composite is drawn from **seven
carriers'** current retail nursing-care and dementia products: one carrier's three-tier
contract, the only one for which both the pre-contract disclosure and the full 約款 were
retrieved [S1] [S2] [S3]; a second carrier's five-型 elective chassis with its rider menu and
a published rate table [S4] [S5] [S6]; a third carrier's annuity-only contract on simplified
underwriting [S7]; a fourth carrier's three separate products — lump sum, 要支援 cover and
annuity [S8] [S9] [S10]; a fifth carrier's 要支援1 contract [S11]; a sixth carrier's
accelerated-benefit whole-life chassis [S12]; and a seventh carrier's stand-alone dementia
product [S13]. Only [S1], [S2] and [S12] are contractual or pre-contractual documents; the
other ten are consumer product pages, and where such a page is silent this specification
says so rather than inferring.

**This document states its deltas against
[the medical product specification](../medical/product-spec.md), the `jplib` third-sector
chassis.** It inherits that chassis's contract machinery — non-participating (*mu-haitō*,
無配当) and 無解約返戻金型, carrying no surrender value (*kaiyaku-henreikin*, 解約返戻金)
at any duration; no automatic premium loan (*jidō furikae kashitsuke*, 自動振替貸付); the
grace/lapse/復活 sequence; the declaration (*kokuchi*, 告知) duty; the third-sector
(*dai-san-bun'ya*, 第三分野) reserving overlay; and the 第三分野標準生命表2018 valuation
mortality — and replaces its benefit structure entirely. Medical cover is **frequency ×
severity × limit**: a daily amount multiplied by paid days, capped per hospitalization and
again in aggregate. Nursing care is **incidence into a persistent state**: a lump sum on
entering a defined care state, an annuity while the insured survives in it, and a premium
waiver from a *lower* care state than either. There is no daily amount (*nichigaku*, 日額), no
per-event day limit (支払限度日数), no 通算 aggregate day limit and no 181-day one-hospitalization
rule anywhere in this product. What replaces them is a decrement into a state whose entry is
certified by a municipality, not diagnosed by a physician.

**And this is private cover written on top of the public scheme, not the public scheme.**
The public long-term-care insurance scheme (*kōteki kaigo hoken*, 公的介護保険) is a compulsory
social-insurance programme run under the Long-Term Care Insurance Act (*Kaigo Hoken-hō*,
介護保険法) by municipalities; it pays for services in kind against a certification of need [R1].
The product specified here is a private 第三分野 insurance
contract that pays **cash** to the insured, and it borrows the public scheme only as a
**benefit trigger**. Nothing in this document describes an entitlement under 公的介護保険.

---

## Product overview and market role

Nursing-care insurance (*kaigo hoken*, 介護保険) in its private form is 第三分野 business, the class
保険業法 第3条 makes writable under either a life or a non-life licence [REG-R1], and the 金融庁
groups it with 医療保険 and がん保険 as the field paying "insurance money or benefits on disease or
injury and for treatment" [R10]. The dominant design is public-scheme-linked (*kōteki kaigo
hoken rendō-gata*, 公的介護保険連動型): the contract's payment trigger (支払事由) is written by
reference to a grade of public certification, so the insurer outsources the adjudication of
"is this person in a care state?" to a municipal administrative process it does not control.

**The public scheme the trigger points at.** 介護保険法 第7条第1項 defines a state requiring nursing
care (*yō-kaigo jōtai*, 要介護状態) as a state in which, because of a physical or mental
impairment, the person is expected to require constant care for all or part of the basic
daily-living actions — bathing, toileting, eating and the like — continuously over a period
fixed by ministerial ordinance [R1] [REG-R42]. 要支援状態 is the parallel, milder definition for
a state needing support to prevent deterioration [R1]. Two classes of insured exist:
**第一号被保険者**, residents aged 65 and over, and **第二号被保険者**, residents aged 40 to 64 who belong
to a public health-insurance scheme [R1]. The 40–64 class can be certified **only** where
the care state arises from one of the **16 特定疾病** (*tokutei shippei*, specified diseases)
listed exhaustively in 介護保険法施行令 第2条 — terminal cancer, ALS, early-onset dementia,
cerebrovascular disease, Parkinson's disease and twelve others [R3] [R1]. One carrier states
the restriction in plain terms on its own consumer page [S8]. That single statutory fact is
why almost every company-basis alternative trigger in this product class is written for
lives under 65 (see Contractual mechanics).

Certification runs on seven grades — 要支援1, 要支援2 and 要介護1 through 要介護5 — and the grades are
defined **quantitatively**, in the estimated minutes of care per day computed by a
ministry-defined method from a 74-item assessment (*yō-kaigo nintei-tō kijun jikan*, 要介護認定等基準時間)
[R2]:

| Band | 要介護認定等基準時間 | Additional test |
|---|---|---|
| 要支援1 | 25–32 minutes | — |
| 要支援2 | 32–50 minutes | support would materially reduce or prevent worsening |
| 要介護1 | 32–50 minutes | (the 要支援2 case excluded) |
| 要介護2 | 50–70 minutes | — |
| 要介護3 | 70–90 minutes | — |
| 要介護4 | 90–110 minutes | — |
| 要介護5 | 110 minutes and over | — |

**要支援2 and 要介護1 share the same 32–50 minute band** and are separated only by the
improvement-potential test [R2]. The certification scale is therefore not a clean severity
ladder, and it is not one at exactly the point where several carriers place their trigger.

**The public incidence data is the sharp contrast with `uklib`, and with `medical`.** Where
a UK long-term-care model has no public morbidity series at all, and where `medical` must
construct incidence from 患者調査 prevalence, a Japanese nursing-care model can be calibrated
from a **national census of certified persons**, published annually by 厚生労働省 and split by
sex, six age bands and all seven grades. At 31 March 2024 there were **about 7.08 million**
certified persons — 6,952 thousand 第一号被保険者 and 131 thousand 第二号被保険者 — against 35,890
thousand 第一号被保険者, a certification rate (認定率) of **19.4%**, up from 19.0% a year earlier and
from 13.9% in the scheme's first year [R4] [R5] [REG-R30]. The age gradient is the product:
**4.3%** of the 65–74 population is certified against **31.1%** of the 75-and-over
population [R4] [R5], and among 第一号被保険者 the counts run 200 thousand at 65–70 to 2,028
thousand at 90 and over, with women outnumbering men **3.6 : 1** at 90+ [R4]. Certified
persons have grown roughly **2.8-fold** in the 23 years since the scheme began [R16].

The grade composition is what converts that prevalence into a benefit-triggering prevalence
[R4] [REG-R30]:

| Band | Certified (thousands) | Share |
|---|---|---|
| 要支援1 | 1,020 | 14.4% |
| 要支援2 | 996 | 14.1% |
| 要介護1 | 1,464 | 20.7% |
| 要介護2 | 1,191 | 16.8% |
| 要介護3 | 927 | 13.1% |
| 要介護4 | 895 | 12.6% |
| 要介護5 | 590 | 8.3% |
| Total | 7,083 | 100.0% |

From which **要介護2以上 = 50.8%**, **要介護3以上 = 34.0%** and **要介護1以上 = 71.5%** of all certified
persons [R4] [REG-R30]. One carrier's own brochure quotes the same 50.8% for an earlier year
[S12]. Two caveats travel with the arithmetic: the source rounds to thousands and warns that
column sums need not match printed totals, and the 要介護5 share is derived as the residual
rather than read, though it is consistent with the printed male 7.2% and female 8.9%
sub-shares [R4]. Utilisation, as a sanity check rather than an incidence measure, ran to
6,754.0 thousand distinct recipients in 令和6年度, drawn from every claim record in the
介護保険総合データベース [R6].

**Market position.** Private nursing-care cover is a growing minority line, not a saturated
one. Among households insured with a private-sector life insurer — the survey's own base,
which excludes the postal insurer (*minpo kanyū setai*, 民保加入世帯), **20.1%** hold a 介護保険
or a 介護特約 (a nursing-care 特約 — *tokuyaku*, rider), up from 16.7% at the previous survey, and **7.6%** hold a 認知症保険 or 認知症特約, up from 6.6%
[R14]. Against that, 医療保険・医療特約 stands at 95.1% and ガン保険・ガン特約 at 68.2% [R14]. The 20.1% is a
**floor rather than a point estimate**: 31.4% of respondents answered 不明 to the nursing-care
question [REG-R32]. Average enrolled 介護給付金月額 is ¥92,000 for the household head and ¥65,000
for a spouse [R14]. The benefit-adequacy backdrop is the same survey's account of care
actually given: an average duration of **55.0 months (4 years 7 months)**, with 27.9% of
cases at 4–10 years and 14.8% at ten years or more, at a monthly cost averaging **¥90,000**
plus a one-off average of **¥472,000** [R14]. The most common grade among those being cared
for was 要介護3, then 要介護2, then 要介護4 [R14].

Two honest limits on that duration figure, because a model will be tempted to use it as a
termination basis. It surveys people who *provided* care, not certified persons; and it is
truncated, since respondents still caring are counted at elapsed duration [R14]. No official
statistic for the duration of the certified state was found in any register.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 介護保険, 公的介護保険連動型, 無配当 and 無解約返戻金型; stand-alone main contract (*shu-keiyaku*, 主契約) paying 介護一時金 and 介護年金, with 特約 attached | [S1] [S4] [S7] [S8] [S11] |
| Regulatory class | 第三分野 (保険業法 第3条第4項第2号 / 第5項第2号) | [REG-R1] [R10] |
| Chassis | Stand-alone third-sector cover, no death benefit and no surrender value; the accelerated-benefit whole-life chassis is out of scope | five of seven carriers [S1] [S4] [S7] [S8] [S11] against [S12]; **[std]** (1) |
| Issue age (契約年齢) range | 40–79 | observed 15–80; **[std]** (2) |
| Age basis | Attained age at 契約日 with the fraction discarded (*man-nenrei*, 満年齢), incremented at each 年単位の契約応当日 | [S1] |
| Policy term (保険期間) | Whole of life (*shūshin*, 終身), to the terminal age of the mortality table | [S1] [S4] [S7] [S8] [S10] [S11] |
| Premium-paying period (保険料払込期間) | Pay for life (終身払) | [S1] [S4] [S7] [S8] [S10] [S11] |
| Lives basis | Single life only | [S1] [S4] [S7] [S8] [S11] |
| Death benefit (死亡保険金) | None; the contract terminates on death with nothing payable | [S11] explicit, [S1] [S7] by absence; **[std]** (3) |
| Lump-sum amount (介護一時金額) menu | ¥500,000–¥3,000,000 in ¥100,000 steps; composite default **¥3,000,000** | [S1] [S8]; **[std]** (4) |
| Annuity base amount (基準介護年金額) menu | ¥200,000–¥1,200,000 in ¥100,000 steps; composite default **¥600,000** per year | [S1] [S6] [S7]; **[std]** (5) |
| Underwriting | Written declaration (告知扱い), no medical examination; anyone who holds, has ever held, or has applied for a 要支援 or 要介護 certification is declined, as is anyone resident in a 高齢者向け施設 | [S1] [S7] [S11] |
| **Anchor model cell** | Male, 契約年齢 60, 終身 / 終身払, 介護一時金 ¥3,000,000 on 要介護2以上, 介護年金 ¥600,000 per year from 要介護3以上 capped at 10 payments, 保険料払込免除 from 要介護1以上, 認知症一時金特約 off, level 月払 premium **¥11,500** | **[std]** (6) |

Footnotes to [std] rows:

1. Two chassis are in the market and they are different products, not variants. Five of the
   seven carriers write stand-alone third-sector cover with no death benefit and (usually)
   no surrender value [S1] [S4] [S7] [S8] [S11]; one writes nursing care as an **accelerated
   death benefit** on a 低解約返戻金型 whole-life contract — 介護保険金 equal to 50% of the sum insured,
   after which the sum insured is reduced by the same amount, premiums are waived and death
   cover continues for life [S12]; one sells dementia cover only [S13]. The composite takes
   the stand-alone chassis: it is the majority design, it is the one whose benefit trigger
   is the interesting mechanic, and the accelerated design already has a `jplib` home — it
   is `whole_life` with a benefit acceleration, not a third-sector product.
2. Observed: 満18歳–満79歳 [S1]; 15–69 on one direct channel, 70 and over face-to-face [S6];
   40–79 across all three products at one carrier, 40–75 on its 定期 variant [S8] [S9] [S10];
   a published premium table spanning 30–80 with the envelope itself unstated [S7]
   [unverified]; not published at two carriers [S11] [S13] [unverified]. The composite takes
   40–79: 40 is the age at which public cover itself begins [R1], so it is the age below
   which the 公的介護保険連動型 trigger cannot fire at all, and 79 is the modal upper bound. The 15
   and 18 lower bounds are outliers on products whose company-basis limb does the work at
   young ages.
3. No stand-alone product observed carries a death benefit; one carrier says so in terms —
   死亡保障はありません [S11]. Two conditional forms exist and are excluded: a 死亡給付金 equal to the
   first annuity instalment where the insured dies having never received one [S10], and a
   死亡時返戻金 equal to the (5%) surrender value [S4]. The composite pays nothing on death, which
   makes death a pure decrement with no cash flow — the same position as `medical`, and the
   opposite of `whole_life`.
4. Observed lump-sum ranges: 要介護1一時金額 and 要介護2一時金額 each ¥100,000–¥1,000,000 in ¥10,000 steps
   [S1]; ¥500,000–¥3,000,000 on one postal plan [S8]; a fixed ¥3,000,000 in the only
   published rate table [S6]; up to ¥2,000,000 [S9] [S10]; ¥500,000 maximum where the
   insured is 65 or over at issue [S11]; 介護一時金特約 and 認知症一時金特約 capped at ¥2,000,000
   **combined** [S7]. ¥3,000,000 is the default because it is the amount at which **two**
   independent carriers publish rates on nearly the same specification [S6] [S8], so the
   anchor cell's premium and its benefit are consistent with each other.
5. Observed annuity ranges: 基準介護年金額 ¥300,000–¥1,200,000 in ¥60,000 steps [S1]; 介護年金額
   ¥200,000–¥1,000,000 in ¥100,000 steps for issue ages 20–60, ¥200,000–¥500,000 for 61–80
   [S7]; up to ¥2,000,000 [S10]; a fixed ¥600,000 in the published rate table [S6]. The
   composite takes the union range on the ¥100,000 step, which is the majority step, and
   ¥600,000 as the default for the same reason as footnote 4.
6. **No carrier publishes 予定発生率, assumed interest rate (*yotei riritsu*, 予定利率) or 予定死亡率
   for this product**, and the regulator
   confirms there is nothing standard to publish [R10]; the 算出方法書 is a 基礎書類 filed with the
   金融庁 and is not public [REG-R2]. The office premium is therefore a model-point input, not
   a computed quantity. The ¥11,500 anchor is built from two published scales at male 60,
   月払, 終身/終身払: **¥5,820** for a ¥3,000,000 要介護2 lump sum [S6] and **¥5,817** for a
   ¥3,000,000 要介護3 lump sum at a second carrier [S8] — an agreement to three yen that is
   itself worth recording — plus **¥5,730** for a ¥600,000 要介護2 annuity on the 5年確定 basis
   [S6]. The lump-sum and annuity rates sum to ¥11,550, rounded to ¥11,500: a modeling
   value, not a quote. The composite's annuity sits at the higher 要介護3 trigger (cheaper)
   but runs to ten payments rather than five (dearer), and the two effects are treated as
   offsetting. Age 60 is one of the three ages — 40, 50 and 60 — at which all three of those
   carriers publish a rate [S6] [S7] [S8], and is the one in the middle of the composite's
   40–79 issue range.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level 平準払 for the whole of life, 無配当 — no dividend, no premium review, no renewal repricing | [S1] [S4] [S7] [S8] |
| Rating factors | Sex and 契約日における満年齢 only — no smoker, occupation or amount band was disclosed by any carrier | [S1] |
| Frequency (払込回数) | Monthly (月払) default; 半年払 and 年払 available, with a refund of the unexpired whole months where premiums cease mid-period | [S1]; default **[std]** (7) |
| Payment route (払込経路) | 口座振替 or クレジットカード扱 | [S1] [S6] |
| Rate structure | Not published by any carrier; the office premium is a model-point input, backed by a **[std]** incidence basis constructed from 介護保険事業状況報告 in the technical notes | [R10]; **[std]** (8) |
| Anchor premium | ¥11,500 per month | **[std]** (6) |
| Sex differential | Female rates **exceed** male at every age on the lump-sum shapes, by about 1.09–1.16×; on the 終身年金 shape the female loading reaches 1.65× at age 40 and 1.79× at 69. The 要支援-level whole-life product runs the other way, female slightly below male | [S6] [S8]; counter-example [S9] |
| Premium waiver (保険料払込免除) | On 要介護1以上 certification (or the company-basis limb at that level), and on 高度障害状態, and on a listed 身体障害状態 reached within 180 days of an accident; waived premiums are treated as paid on each 払込期月の契約応当日 | [S1] [S2] [S8]; threshold **[std]** (9) |

7. Monthly is the dominant retail mode and the mode of every published rate table found [S6]
   [S7] [S8] [S9] [S10] [S12]; the composite standardizes on it, which is also why the model
   runs on a monthly grid. The unearned-premium refund on 半年払・年払 [S1] is treated as an
   immaterial modal refinement and is not modeled.
8. The absence of a published pricing basis is not a research gap, it is the regulatory
   position: for 第三分野 business 「標準死亡率、参考純率といったスタンダードな指標が存在しておらず、
   公的なデータや各社の実績等から給付事由ごとその発生率を見込まざるを得ない」 [R10]. Each insurer estimates incidence per benefit
   trigger from public data and its own experience, and must disclose the model it used
   [R10]. The reference implementation does the same thing in public: the incidence basis is
   a **[std]** construction from the 認定率 and grade composition of [R4] and [R5], and every
   value in it carries that provenance.
9. Waiver triggering at a **lower** care state than the main benefit is the market pattern
   and is the reverse of `medical`, where the base waiver is disability-triggered and
   independent of the benefit. Observed: waiver on the 要介護1一時金 trigger against a 要介護3以上
   annuity [S1]; waiver at 要介護1以上 against a 要介護3以上 lump sum [S8]; waiver on the **first
   annuity payment**, so simultaneous with the benefit [S4]; waiver on the 介護年金 trigger,
   carrying the riders' premiums too [S7]; waiver on payment of the 介護保険金 [S12]; not stated
   at two carriers [S11] [S13] [unverified]. The composite takes 要介護1以上 — the lowest
   observed threshold and the one two carriers publish [S1] [S8] — because a waiver that
   fires strictly before the benefit is the case a model can get wrong, and a waiver
   simultaneous with the benefit is the trivial special case of it.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Care lump sum (*kaigo ichijikin*, 介護一時金) | 介護一時金額 paid **once only** per contract, on first satisfaction of the 要介護2以上 trigger; does not terminate the contract | four of seven carriers [S1] [S4] [S7] [S12]; threshold **[std]** (10) |
| Care annuity (*kaigo nenkin*, 介護年金) | 基準介護年金額 paid annually in advance, the first instalment on the date the 要介護3以上 trigger was first met (介護年金支払基準日) and later instalments on its annual anniversaries, **at most 10 payments** | [S1] [S7] [S10]; threshold and cap **[std]** (11) |
| Annuity metering | **Survival-tested** — each instalment requires only that the insured be alive on the payment date; the **state-tested** variant, which additionally requires the care state to persist, is a switch | [S4] [S7] [S10] [S12] against [S1]; **[std]** (11) |
| Unpaid lump sum at annuity start | Where the annuity triggers before the lump sum has been paid, the unpaid lump sum is paid together with the first annuity instalment | [S1] |
| Company-basis limb — physical | Dependency in defined daily-living actions, physician-diagnosed (約款所定の要介護状態) that has **continued 180 days or more**; available only where the insured is 満65歳未満 | [S1] [S2] [S4] [S12]; **[std]** (12) |
| Company-basis limb — dementia | Organic dementia (*kishitsusei ninchishō*, 器質性認知症) with disorientation (見当識障害) in the absence of clouded consciousness, **continued 90 days or more**; 満65歳未満 only | [S1] [S2] |
| Both limbs satisfied | The public-certification limb governs and its amount is paid | [S1] |
| Waiting period | **None** on the care benefits; a 180-day 認知症診断責任開始期 applies to the dementia rider only | [S1] against [S4] [S5] [S7] [S13]; **[std]** (13) |
| Pre-inception (責任開始期前) rule | Nothing is paid where the certification, or the company-basis state, results from an illness contracted or an accident occurring before the 責任開始期 | [S1] [S2] |
| Exclusions (免責事由) | 故意 or 重大な過失 of the policyholder or the insured; the insured's 犯罪行為; 戦争その他の変乱; 薬物依存. The war exclusion is qualified — where the number of lives affected would not materially change the insurer's liability the benefit may still be paid | [S2] |
| Other refusal grounds | Certification at 要支援1, 要支援2 or 非該当（自立）where the contractual threshold is a 要介護 band; failure to meet the 約款 definition of a company-basis state; lapse; rescission for non-disclosure or for 重大事由 | [S1] |
| Suicide | Nothing is paid where the care state results from an intentional act of the insured; no separate 免責期間 is stated for this product | [S2]; statutory frame [REG-R34] |
| Contract termination | On the **10th annuity payment**, effective retroactively to the date that payment's trigger was met; otherwise on death, on lapse, or on rescission | [S1]; **[std]** (14) |

10. The observed threshold range is the widest single spread in this product, running from
    要支援1 to 要介護3: 要支援1以上 as a main-contract trigger at one carrier [S11] and as a 特則 at a
    second [S5]; 要支援2以上 at a third [S9]; 要介護1以上 at three [S1] [S4] [S8]; **要介護2以上 at four**
    [S1] [S4] [S7] [S12]; 要介護3以上 at three [S1] [S8] [S10]; and a graded payout across
    要介護3/4/5 at two [S1] [S12]. The composite takes 要介護2以上 for the lump sum: it is the modal
    single threshold, it is what 公的介護保険連動型 usually means in market copy, and it is the
    threshold whose public base rate is best evidenced — 50.8% of all certified persons [R4]
    [REG-R30], a figure a carrier quotes back in its own brochure [S12]. It is also the
    threshold at which the 要支援2 / 要介護1 band overlap [R2] stops mattering, which removes the
    single worst source of ambiguity in the certification scale.
11. Annuity metering is the most model-relevant divergence in the product, and the two
    designs need different machinery. **State-tested**: instalments fall on the annual
    anniversaries of the 介護年金支払基準日 and each requires the insured to *still be* in the state
    on that date; at most one payment a year and **at most 10 over the contract**; if the
    state lapses and the insured later re-qualifies, a **new** 介護年金支払基準日 is set [S1] [S2].
    **Survival-tested**: 5年確定年金 or 終身年金 elected at issue, tested only on 生存している限り, with the
    remaining instalments commutable at present value [S4]; 5年有期 / 10年有期 / 終身年金 with the
    carrier stating explicitly that recovery does **not** stop payment [S7]; 終身 or
    5/10/15年有期 [S10]; 保証金額付 or 10年保証期間付 terminal annuities by conversion [S12]. The
    composite takes **survival-tested, 10 annual payments**: survival-testing is four
    carriers against one [S4] [S7] [S10] [S12], and ten payments is simultaneously the one
    carrier's hard cap [S1] and one of another's published terms [S7], so the cap is
    evidenced from both sides. The state-tested variant is retained as a switch because it
    needs a recovery decrement that the base run does not — see
    [`technical-notes.md`](technical-notes.md). The
    composite's 要介護3以上 annuity threshold is the one written by two of the four carriers
    selling a main-contract annuity [S1] [S10]; a third writes 要介護2以上 [S7] and the fourth
    lets the buyer elect 要介護1以上 or 要介護2以上 at issue [S4]. Putting it one grade above the
    lump sum makes the contract a **ladder of thresholds**, which three carriers write in
    some form: one across waiver, two lump-sum tiers and the annuity [S1], a second splitting
    a 要介護1以上 waiver from a 要介護3以上 lump sum [S8], and a third reserving its top annuity
    tier for 要介護4 / 要介護5 [S12].
12. Every carrier writes the trigger as an **either/or** — the public certification, or a
    company-defined care state that has persisted for a stated number of days [S1] [S4] [S7]
    [S11] [S12] [S13] [R15]. Observed durations: 180日以上 [S1] [S4] [S12]; 180日を**超えて**, a
    strictly tighter form of the same test [S7]; 180日間継続, stated by that carrier to
    correspond to 要介護2以上 [S11]; 90日以上 for the dementia-defined state [S1] [S2]; 180日
    continuation for a dementia treatment annuity [S13]. Age restriction: 満65歳未満 at three
    carriers [S1] [S4] [S12], **no age restriction stated** at two [S7] [S11]. The composite
    takes 180 days (90 for dementia) with the 満65歳未満 restriction, the majority position and
    the one the statute explains: below 65 the public limb can only fire on a 特定疾病 [R1]
    [R3], so the company limb is filling a hole that closes at 65. One carrier grants a
    **relief** the composite adopts: where the insured qualified under the company limb
    while under 65, the age condition is not re-applied to instalments 2 onwards once the
    insured passes 65, provided the state continues [S1].
13. **Two mechanisms both appear in marketing copy as "180日" and they are not the same
    thing.** A 不担保期間 or waiting period means cover has not started yet; a duration test
    inside the trigger means the care state must have *persisted* before it counts. Observed
    waiting periods: none stated on the care benefits at one carrier, which relies on the
    責任開始期前 rule instead [S1] [S2]; none on the care benefits but a 認知症診断責任開始期 of
    責任開始日から180日を経過した日の翌日（181日目）on the dementia and MCI benefits at a second [S4] [S5]; a
    **1-year 不担保期間 on every benefit** at a third, the explicit price of three-question
    simplified underwriting [S7]; **90 days** from the 契約日 at a fourth, on dementia benefits
    [S13]; not stated at the remaining three. The composite takes no waiting period on the
    care benefits — the position of the only carrier whose 約款 was read [S2] — and the
    180-day 認知症診断責任開始期 on the dementia rider [S4] [S5]. The 1-year 不担保期間 belongs to a
    simplified-underwriting product and is carried as a model-point flag, not as a composite
    default.
14. One carrier extinguishes the contract on the 10th annuity payment, retroactively to the
    date that payment's trigger was met [S1]; one pays once only and extinguishes [S11]; one
    extinguishes on payment of the 軽度介護保険金, the 死亡保険金 or the 高度障害保険金 [S9]. The composite
    terminates on the last annuity payment. This gives the model a **benefit-driven
    termination decrement**, as `medical` has on exhausting both aggregate limits — but here
    it is a counter of ten annual payments, not a counter of days.

### Options — 特約 and 特則

| Parameter | Representative value | Basis |
|---|---|---|
| Dementia lump-sum rider (認知症一時金特約) | ¥1,000,000 on the first diagnosis of 約款所定の器質性認知症 after the 認知症診断責任開始期, once per contract; **10% of that amount** on the first diagnosis of MCI (*keido ninchi shōgai*, 軽度認知障害), once and extinguishing for that benefit line; where dementia is diagnosed first with no prior MCI claim, both are paid together | [S4] [S5] [S7] [S13]; **[std]** (15) |
| Dementia diagnostic standard | 器質性認知症 requires an acquired organic brain lesion and a persistent, global loss of already-acquired intelligence caused by it; diagnosis must rest on cognitive testing and imaging, with a reasonable-grounds fallback where those cannot be performed. MCI is 日常生活動作は自立しているものの、認知機能が低下し、認知機能領域の障害が認められる状態 | [S2] [S4] [S5] |
| Mild-care lump sum (軽度介護一時金給付特則) | A lump sum at 要支援1以上 or 要支援2以上; paying it extinguishes the 特則 and stops its premium but leaves the contract in force. **Out of the base run** | [S5] [S9] [S11]; scope **[std]** (16) |
| 新保険料払込免除特約 | Extends the waiver to a listed disease range, priced separately. Out of scope | [S5] |
| 健康祝金特則 | 10% of the 介護年金額 every five years while no claim has been made. Out of scope | [S7] |
| 介護保険金割増年金支払特約 | Converts a lump sum into an enhanced annuity, with a 40-or-over commencement age and the top tier reserved for 要介護4 / 要介護5. Out of scope | [S12] |
| 引受基準緩和型 / simplified underwriting | Out of scope — a different morbidity basis, not a rider | [S7]; scope **[std]** (16) |

15. Dementia cover is sold in four architectures: as a **主契約の型** elected instead of a care
    型, paying 認知症診断一時金 [S4], with MCI on a separate 特則 [S5]; as a rider splitting one amount
    **10% MCI / 90% dementia**, with the 認知症一時金特約 and 介護一時金特約 capped at ¥2,000,000 combined
    [S7]; as a **stand-alone product** with three layers — 軽度認知障害保険金 fixed at 10% of the
    認知症診断保険金 (¥10,000–¥300,000), 認知症診断保険金 ¥100,000–¥3,000,000, and 認知症治療年金
    ¥40,000–¥2,000,000 payable once the 所定の状態 has continued 180 days and annually thereafter
    on survival [S13]; and as a **separate carrier product** at issue ages 40–75 [S8]. One
    carrier sells no dementia benefit at all on this contract, letting dementia in only
    through the 90-day 認知症による要介護状態 limb of the same three care benefits [S1] [S2]. The
    composite takes the rider form with a ¥1,000,000 amount and the **10% MCI fraction,
    which is uniform at both carriers that publish one** [S7] [S13] — one of the few
    genuinely market-wide parameters here. Household penetration of dementia cover is 7.6%
    against 20.1% for care cover [R14], so it is a rider, not the chassis.
16. Scope exclusions rather than value standardizations. 要支援-level benefits are a real and
    growing segment — one carrier's whole main contract triggers at 要支援1以上 [S11] — but they
    roughly **double** the triggering population against the composite's lump-sum threshold
    (要支援1以上 is 100% of certified persons against 50.8% at 要介護2以上 [R4]) and treble it
    against the annuity threshold (34.0% at 要介護3以上 [R4]), and they change the product from
    a severe-disability cover into a high-frequency one. They are carried as a threshold parameter, not as a base-run
    benefit. Simplified underwriting is a different risk pool priced with a 1-year 不担保期間
    [S7]; the composite is fully underwritten.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 解約返戻金 | **None at any duration** — 「この保険契約の解約払戻金はありません」 | [S1] [S2] [S7] [S8]; **[std]** (17) |
| Policyholder dividend (配当金) | None — the chassis is 無配当; none of the four statutory surplus-distribution methods applies | [S1] [S2] [S4]; [REG-R9] |
| 契約者貸付 / 自動振替貸付 | Neither is offered: there is no surrender value to lend against, so a missed premium lapses the contract | [S2]; [REG-R14]; **[std]** (17) |
| Grace (払込猶予期間), 月払 | From the first day of the month following the 払込期月 to the **last day of that month** | [S2] |
| 払込猶予期間, 半年払・年払 | From the first day of the month following the 払込期月 to the 月単位の契約応当日 in the month after that | [S2] |
| Claims during grace | Unpaid premiums are deducted from the benefit; where the benefit is smaller than the arrears the balance must be paid by the end of grace, failing which the contract lapses and **no benefit is paid** | [S2] |
| Lapse (*shikkō*, 失効) | From the day after the grace period expires | [S2] |
| Reinstatement (*fukkatsu*, 復活) | Within **1 year** of the lapse date, on fresh 告知, payment of arrears and the insurer's consent; the 復活日 is the later of the arrears payment date and the 告知日, and the 責任開始期 resets to it | [S1] [S2]; **[std]** (18) |
| Non-disclosure (告知義務違反) | Rescission where a material misstatement is found within **2 years** of the 責任開始日; the two-year bar does not protect the policyholder where the claim event fell inside those two years; rescission for fraud is not time-limited | [S1]; ceiling [REG-R35] |
| クーリング・オフ | 8 days from the later of the 申込日 and the 告知日, full refund; out of scope | [S1]; [REG-R36]; scope **[std]** (18) |
| Death of the insured | Contract terminates, nothing payable | [S1] [S11]; **[std]** (3) |

17. **Four of the seven carriers publish an outright nil surrender value** [S1] [S2] [S7]
    [S8], and one of them carries the fact in the formal product name itself — 介護保険〔無解約払戻金
    2021〕 [S1]. The two designs that do produce a value are excluded: 5% of the elected
    benefit amount, available only after a *short* premium-paying period completes and only
    before the main benefit has triggered, with a 死亡時返戻金 equal to it [S4]; and the full
    低解約返戻金型 whole-life progression, suppressed to **70% of the ordinary value** during the
    premium-paying period and stepping to 100% at 払込満了 [S12], plus a 低解約返戻金型 form of the 要支援
    product [S9]. The composite's nil value is what removes 自動振替貸付 from this product, and
    with it the whole soft-landing mechanic that `whole_life` has and this chassis does not
    [REG-R14]. The lapse is real and immediate.
18. Reinstatement within one year is the only window found in a retrieved 約款 [S1] [S2], and
    it is a caution rather than a market statement: the three-year window commonly quoted
    for the Japanese market as a whole is **[unverified]** and this carrier's own window is
    one year. No other carrier's grace, lapse or reinstatement terms were retrievable, so
    the composite rests on one contract and says so. クーリング・オフ is the eight-day dispatch-rule
    right of 保険業法 第309条 [REG-R36]; `jplib` models from the point cover is in force and
    treats the window as a pre-inception matter it has no new-business funnel to represent.

---

## Contractual mechanics

### The trigger, which is the product

Write `g` for a certification grade on the ordered scale 要支援1 < 要支援2 ≈ 要介護1 < 要介護2 < 要介護3 <
要介護4 < 要介護5, and `G_L`, `G_N`, `G_W` for the contractual thresholds of the lump sum, the
annuity and the waiver — 要介護2, 要介護3 and 要介護1 in the composite. The trigger is a disjunction,
evaluated separately for each of the three benefits:

    trigger(G, t) = 1  if the insured holds a public certification at grade G or above,
                       effective at or before t
                  = 1  if the 約款-defined company-basis care state has persisted 180 days
                       (90 days where dementia-defined) and the insured was under 65 at
                       the date that state was diagnosed
                  = 0  otherwise

Where both limbs are satisfied the public limb governs and its amount is paid [S1]. The
public limb is an **administrative act, not a clinical one**, and three of its properties
belong in a model rather than in a footnote [R1]:

- **The decision is due within 30 days of application and takes effect retroactively to the
  application date.** The claim date is therefore the application date, not the decision
  date, and a projection that dates claims at notification is systematically late by up to a
  month.
- **The certification has a finite 有効期間 and must be renewed** (要介護更新認定). The grade can move
  **up or down** at renewal.
- **Below 65 the public limb fires only on one of the 16 特定疾病** [R1] [R3], which is what the
  company-basis limb exists to cover, and why three carriers restrict that limb to lives
  under 65 [S1] [S4] [S12].

The composite treats the care state as **absorbing** once entered — a **[std]**
simplification forced by the sources, since no public transition-rate table exists in any
register and no carrier publishes one. It is a real simplification and not a harmless one:
the statute provides for downgrade at renewal [R1], a carrier's own FAQ addresses what
happens 「要介護状態が改善された場合」 [S3], and the state-tested annuity variant [S1] cannot be modeled at
all without a recovery decrement. [`technical-notes.md`](technical-notes.md) carries the
recovery rate as a named **[std]** input set to zero in the base run, not as an omission —
and states what that rate does and does not cover, since it models the fall below the
annuity grade rather than a return to health.

### 介護一時金

    lump_sum(t) = A_L * 1{ first t at which trigger(G_L, t) = 1 }

paid once per contract and **not** terminating it [S1] [S4]. `A_L` is the 介護一時金額, ¥3,000,000
in the composite. Where a carrier writes two lump-sum tiers — a 要介護1一時金 and a 要介護2一時金, each
once only [S1] [S2] — the composite collapses them into the single 要介護2 tier and keeps the
要介護1 threshold for the waiver alone, so that the model has one lump sum and one waiver
rather than two of each.

### 介護年金

    ann_start   = first t at which trigger(G_N, t) = 1        (the 介護年金支払基準日)
    pay_date(k) = ann_start + (k - 1) years,     k = 1 .. 10
    annuity(k)  = A_N * 1{ insured alive at pay_date(k) }              (survival-tested)
    annuity(k)  = A_N * 1{ alive and trigger(G_N, pay_date(k)) = 1 }   (state-tested switch)

with `A_N` = ¥600,000. Instalments are annual and in advance, at most one a year, at most
ten in total [S1] [S7]. The contract terminates on the tenth payment, effective
retroactively to the date that payment's trigger was met [S1]. If the annuity triggers
before the lump sum has been paid, the unpaid lump sum is paid **together with the first
annuity instalment** [S1] — which is not merely a timing nicety, because it means a life
entering directly at 要介護3以上 receives `A_L + A_N` on one date.

Under the state-tested switch, a lapse of the state does not merely suspend payment: if the
insured later re-qualifies, a **new** 介護年金支払基準日 is set and the anniversary schedule restarts
from it [S1]. A model that keeps the original schedule and skips instalments is wrong for
that design.

The two metering bases need different assumption sets, and the difference is first-order. A
survival-tested annuity is a life annuity conditional on one-time entry, and after entry it
needs only an impaired-life mortality basis. A state-tested annuity needs a recovery (or
de-certification) decrement as well, on top of the ten-payment cap. Where the annuity is
survival-tested, one carrier says in terms that recovery does not stop it —
「介護年金のお支払事由に該当した後、容体が改善した場合」も年金支払期間中、生存されている限りお受け取りいただけます — and that the premium waiver
likewise stays in force [S7].

### 保険料払込免除

    premium(t) = 0  for every t after the first date at which trigger(G_W, t) = 1

with `G_W` = 要介護1, plus the two disability limbs — 高度障害状態 from any cause, and a listed
身体障害状態 arising from an 不慮の事故 within 180 days of it [S1] [S2]. Waived premiums are treated as
though paid on each 払込期月の契約応当日, so the contract continues in full force; while the waiver is
running the payment mode cannot be changed and the benefit amount cannot be reduced [S1]
[S2].

Because `G_W` sits **below** `G_L`, the waiver is not a by-product of the claim: there is a
band of the population — 要介護1 lives, 20.7% of all certified persons [R4] — for whom the
contract has stopped collecting premium and has not yet paid anything. That interval is the
single most easily mis-modeled item in this product.

### Waiting periods against duration tests

The composite has **no waiting period on the care benefits**; protection runs instead
through the 責任開始期前 rule, which refuses any claim where the certification or the
company-basis state results from an illness contracted, or an accident occurring, before the
責任開始期 [S1] [S2]. The dementia rider carries a 認知症診断責任開始期 of 責任開始日から180日を経過した日の翌日（181日目）[S4]
[S5].

These are different mechanisms from the **180-day (or 90-day) persistence test inside the
company-basis trigger**, which is a property of the care state, not of the contract's cover
period. Both are written "180日" in marketing copy. A model that implements one of them
twice, or the wrong one, will be wrong at inception and wrong again in the tail.

### Underwriting, exclusions, grace, lapse and reinstatement

Underwriting is 告知扱い and the front door is tight: one carrier declines anyone currently
hospitalised or advised to be hospitalised or operated on, **or who has ever been certified
for, or has ever applied for, 要支援 or 要介護** [S1]; another declines applicants already
applying for or actively considering certification, or living in a 高齢者向け施設 [S11]; the
simplified-underwriting carrier asks three questions, one of them whether the applicant has
ever applied for certification, and prices that leniency with a 1-year 不担保期間 [S7]. The
anti-selection this guards against is unusually direct, because the thing being selected
against is an application to a public body that leaves a record.

免責事由 are 故意 or 重大な過失 of the policyholder or the insured, the insured's 犯罪行為, 戦争その他の変乱 and
薬物依存, with the war exclusion qualified where the number of lives affected would not
materially change the insurer's liability [S2]. Note what is **not** on the list: no
period-limited suicide exclusion is stated for this product, which is consistent with 保険法
第51条 imposing no statutory time limit and leaving any 免責期間 to the contract [REG-R34].

For a 月払 contract, grace runs from the first day of the month following the 払込期月 to the last
day of that month; non-payment produces 失効 from the day after grace expires [S2]. A claim
arising in the grace window is paid net of the arrears, and where the benefit is smaller
than the arrears the balance must be paid by the end of grace, failing which the contract
lapses and **no benefit is paid at all** [S2]. There is nothing to break the fall: with no
surrender value there is no 自動振替貸付 [S2] [REG-R14]. 復活 is available within one year on fresh
告知 and payment of arrears, and it is not a rewind — cover restarts from the 復活日 and the
責任開始期 resets to it, which matters precisely because the whole benefit definition is anchored
to 責任開始期以後の傷害または疾病 [S1] [S2]. 告知義務違反 supports rescission for two years from the 責任開始日,
inside the five-year statutory ceiling [REG-R35].

---

## Riders and options

**In scope (modeled or parameterized):**

- **介護一時金** — the main-contract lump sum at 要介護2以上, once only [S1] [S4] [S7] [S12].
- **介護年金** — the main-contract annuity from 要介護3以上, ten payments, survival-tested [S1]
  [S7] [S10]. Switchable to state-tested, which switches on the recovery decrement.
- **保険料払込免除** — from 要介護1以上, plus the 高度障害 and accident-disability limbs [S1] [S2] [S8].
  Always on; the threshold is a parameter.
- **Company-basis trigger limb** — 180-day persistence, 90 days where dementia-defined,
  lives under 65, with the post-65 continuation relief [S1] [S2] [S4] [S12]. Switchable off,
  which reduces the product to pure 公的介護保険連動型.
- **認知症一時金特約** — ¥1,000,000 on first 器質性認知症 diagnosis with 10% of it on first MCI diagnosis,
  behind a 180-day 認知症診断責任開始期 [S4] [S5] [S7] [S13]. Off in the base run.
- **Trigger-threshold parameter** — `G_L`, `G_N` and `G_W` are model-point fields spanning
  要支援1 to 要介護3, so the whole observed market spread is reachable without a second chassis
  [S1] [S4] [S5] [S7] [S8] [S9] [S10] [S11] [S12].
- **1-year 不担保期間** — a model-point flag for the simplified-underwriting design [S7]. Off in
  the base run.

**Out of scope:** the accelerated-benefit whole-life chassis and its 低解約返戻金型 surrender
progression, 自動振替貸付, 延長定期保険, 払済保険 and 減額 [S12] — that machinery belongs to the
[whole life product specification (終身保険)](../whole_life/product-spec.md) and its model
[`WholeLife_JP_A`](../whole_life/model.md);
介護保険金割増年金支払特約 and the 介護年金移行特約, which convert a lump sum into an enhanced annuity with 要介護4
/ 要介護5 top tiers [S12]; 軽度介護一時金給付特則 and 軽度認知障害診断一時金給付特則 as separate extinguishing benefit
lines [S5]; 新保険料払込免除特約 [S5]; 健康祝金特則 [S7]; the 5%-of-benefit post-払込満了 surrender value and
the matching 死亡時返戻金 [S4]; the 死亡給付金 equal to one annuity instalment [S10]; the 認知症治療年金 as a
third dementia layer [S13]; commutation of remaining annuity instalments at present value
[S4]; 引受基準緩和型 chassis [S7]; and クーリング・オフ [S1] [REG-R36].

---

## Variations across insurers

1. **Public-certification threshold.** 要支援1以上 [S11] [S5]; 要支援2以上 [S9]; 要介護1以上 [S1] [S4]
   [S8]; 要介護2以上 [S1] [S4] [S7] [S12]; 要介護3以上 [S1] [S8] [S10]; graded across 要介護3/4/5 [S1]
   [S12]. Composite: 要介護2以上 for the lump sum, 要介護3以上 for the annuity, 要介護1以上 for the waiver
   — the modal tiering, and the one with the best public base rates (footnote 10).
2. **Company-basis limb.** 180日以上 at three carriers [S1] [S4] [S12]; 180日を**超えて** at a
   fourth, strictly tighter [S7]; 180日間継続 at a fifth [S11]; 90日以上 for the dementia-defined
   state [S1] [S2]; not stated on the pages fetched for a sixth [S8] [unverified]. Age
   restriction 満65歳未満 at three [S1] [S4] [S12], none stated at two [S7] [S11]. Composite:
   180 days, 90 for dementia, 満65歳未満 (footnote 12).
3. **Benefit form.** Lump sum only at three [S8] [S9] [S11]; annuity only at two [S7] [S10];
   both, tiered by grade, at one [S1]; one **or** the other elected at issue from five
   mutually exclusive 保険契約の型 that cannot be changed mid-term at one [S4] [S6]; lump sum
   convertible to an annuity at one [S12]. Composite: both, tiered — the design that
   exercises every mechanic the others use in isolation.
4. **Annuity metering.** State-tested annually with a hard 10-payment cap and contract
   extinction at one carrier [S1]; survival-tested at four [S4] [S7] [S10] [S12], with
   payout shapes 5年確定 [S4], 5/10年有期 or 終身 [S7], 終身 or 5/10/15年有期 [S10], and 保証金額付 or
   10年保証期間付終身 [S12]. Composite: survival-tested, ten payments (footnote 11). **This is the
   widest genuinely structural divergence in the product** — the two designs do not differ
   by a parameter, they differ by whether a recovery decrement exists.
5. **Amount graded by certification band.** Two carriers grade the payout: 1型 pays 基準介護年金額
   at 要介護5, ×5/6 at 要介護4 and ×4/6 at 要介護3, while 2型 pays ×1 / ×2/3 / ×1/3, with the
   company-basis limb paid at the 要介護3 fraction [S1]; a second reserves its top enhanced
   annuity tier for 要介護4 or 要介護5 [S12]. Five carriers pay a flat amount above the threshold
   [S4] [S7] [S8] [S10] [S11]. Composite: flat — the majority, and the graded form is
   reachable by running the model at each fraction.
6. **Premium waiver threshold.** 要介護1以上 at two [S1] [S8]; simultaneous with the first
   annuity payment at one [S4]; on the 介護年金 trigger, carrying rider premiums too, at one
   [S7]; on payment of the 介護保険金 at one [S12]; not stated at two [S11] [S13] [unverified].
   Composite: 要介護1以上, strictly below the benefit threshold (footnote 9).
7. **Waiting period.** None stated on the care benefits at one [S1]; none on care benefits
   but 180 days on dementia and MCI at a second [S4] [S5]; **one year on every benefit** at
   a third, the price of three-question underwriting [S7]; 90 days from the 契約日 on dementia
   at a fourth [S13]; not stated at three. Composite: none on care, 180 days on the dementia
   rider (footnote 13).
8. **Dementia and MCI.** A main-contract 型 with MCI on a 特則 [S4] [S5]; a rider splitting one
   amount 10% MCI / 90% dementia [S7]; a three-layer stand-alone product [S13]; a separate
   product at issue ages 40–75 [S8]; and no dementia benefit at all, dementia entering only
   through the 90-day company-basis limb [S1] [S2]. Composite: a rider at 10% / 90% — the
   uniform fraction wherever one is published [S7] [S13] (footnote 15).
9. **Surrender value.** None at four [S1] [S2] [S7] [S8]; 5% of the elected benefit after a
   completed short premium term, and only before the benefit triggers, at one [S4]; a full
   低解約返戻金型 progression at 70% during the premium-paying period at one [S12], with a 低解約返戻金型
   form of the 要支援 product at another [S9]; not stated at two [S11] [S13] [unverified].
   Composite: none (footnote 17).
10. **Issue ages and amount limits.** 18–79 [S1]; 15–69 on a direct channel [S6]; 40–79, and
    40–75 on a 定期 variant [S8] [S9] [S10]; a rate table spanning 30–80 with the envelope
    unstated [S7] [unverified]; a ¥500,000 cap where the insured is 65 or over at issue
    [S11]; a rate table published only at issue ages 20/30/40/50 [S12]. Composite: 40–79
    (footnote 2).
11. **Chassis.** Stand-alone third-sector cover at five carriers [S1] [S4] [S7] [S8] [S11];
    an accelerated 介護保険金 of 50% of the sum insured on a whole-life contract at one, after
    which the sum insured drops by the same amount, premiums are waived and death cover
    continues for life [S12]; a dementia-only product at one [S13]. Composite: stand-alone
    (footnote 1).
12. **What does not vary.** Every product ties its primary trigger to the public 要介護 or 要支援
    certification and names 介護保険法 as the scheme it means, one carrier citing the
    certification ordinance by name inside its own contract wording [S1] [S12] [R2]; every
    one carries a company-basis alternative expressed as a defined dependency state that
    must have **persisted** for a stated number of days [S1] [S4] [S7] [S11] [S12] [R15];
    every stand-alone product is written 終身 with 終身払 premiums [S1] [S4] [S7] [S8] [S10]
    [S11]; every one has a premium-waiver mechanic tied to the care state [S1] [S4] [S7]
    [S8] [S12]; every 一時金 benefit is once-only per contract [S1] [S4] [S5] [S9] [S11];
    premiums are rated on sex and 満年齢 alone, with **female rates above male at every age on
    the lump-sum shapes** at the two carriers publishing a rate at this severity [S6] [S8] —
    though the 要支援-level product runs the other way [S9], which is what the invariant is
    worth; and **no carrier publishes an incidence basis, a 予定発生率
    or a 予定利率**, which the regulator confirms is the expected state of affairs for 第三分野
    business [R10]. These are the invariant core of the composite.

---

## Regulatory context

**Classification.** Private 介護保険 is 第三分野 business under 保険業法 第3条, writable under either a
life or a non-life licence [REG-R1], and the 金融庁 groups it with 医療保険 and がん保険 in the field
paying on disease, injury and treatment [R10]. The classification, not the product's shape,
is what pulls in everything below. The public 公的介護保険 scheme it links to is not insurance
business at all: it is social insurance under 介護保険法, administered by municipalities [R1]
[REG-R42].

**Prudential — the third-sector reserving overlay.** 保険業法 第116条 requires a
policy reserve (*sekinin-junbikin*, 責任準備金) at each 決算期 and delegates the
accumulation method for long-term contracts [REG-R4]; 施行規則 第68条 sets the scope
of the resulting 標準責任準備金 [REG-R7]; 平成8年大蔵省告示第48号 fixes the method as net level
premium (**平準純保険料式**) with the table vintages and the standard valuation interest
rate (*hyōjun riritsu*, 標準利率) reset machinery [REG-R10]; and for contracts
concluded on or after 1 April 2018 the third-sector valuation mortality is
**第三分野標準生命表2018** [REG-R11]. **The 標準利率 applicable to this product class could
not be established from a retrieved document and is [unverified].**

On top of that sits the overlay that is specific to this class and decisive for this
product. 施行規則 第69条 divides the reserve into 保険料積立金, 未経過保険料, 払戻積立金 and 危険準備金, and requires a
separately identified 第三分野保険の保険リスクに備える危険準備金 [REG-R8]. The 金融庁 framework paper states plainly
that for 第三分野 there is no standard incidence indicator — 「標準死亡率、参考純率といった
スタンダードな指標が存在しておらず、公的なデータや各社の実績等から給付事由ごとその発生率を見込まざるを得ない」 — and imposes, on top of 標準責任準備金, an
annual **ストレステスト** checking that the 予定事故発生率 covers the 99th percentile of incidence risk
over a **ten-year** horizon, with 危険準備金 topped up where it does not; a **負債十分性テスト** by
future cash flow analysis where the 予定発生率 fails to cover risk defined at **97.7%**;
disclosure of the incidence model used; and a transparent numeric **基礎率変更権** exercise
standard disclosed at point of sale [R10]. The stress test itself must be computed under
平成10年6月8日大蔵省告示第231号, with organisational separation between the calculating unit and
internal audit [REG-R14] [REG-R13]; **the notification's own text was not retrieved, so its
stress magnitudes are [unverified] and no numeric stress level is asserted anywhere in these
documents.**

**This is the exact boundary at which the reference model marks its incidence basis [std].**
The 日本アクチュアリー会, in its 指定法人 role [REG-R23], publishes a **mortality** table for this class
and no morbidity table: 第三分野標準生命表2018 contains `qx` and nothing else [R8]. Its own
construction summary records that it is graduated from **第21回生命表（2010年）**, the *national*
life table rather than insured experience — a deliberate change from the 2007 edition — and
that it **excludes 高度障害**, which the 2007 edition included [R9] [REG-R20]. It is also
deliberately **lighter** than the death-insurance table at every age: male `q65` is 0.00845
against 0.01015, and `q75` 0.02242 against 0.02637 [R8]. That is the correct direction of
conservatism for a living-benefit product, where longer survival means more annuity
instalments — and it means a best-estimate nursing-care model must not adopt the valuation
table as its mortality decrement without an explicit **[std]** adjustment, and must say
which of the two it is using at each point. The tables are published free and in full at
stable public URLs [REG-R18], but the 日本アクチュアリー会 site terms restrict reproduction and
transmission [REG-R21], so this library **cites** them and **ships** a documented proxy,
never a copy.

What fills the morbidity hole is public administrative data rather than an actuarial table:
the 認定率 and grade composition of 介護保険事業状況報告 [R4] [R5] [REG-R30], with the five-year-band 認定率
that a finer basis wants available in the e-Stat release of the same statistic, which was
not fetched [REG-R33]. Post-onset mortality is a harder gap: no impaired life table for the
care state exists in any retrieved source, so the population anchor is the 完全生命表 — 平均余命
19.97 years for a male at 65 and 24.88 for a female, 12.54 and 16.22 at 75 [R13] — and since
more than 90% of certified 第一号被保険者 are 75 or over [R4], the 75 figures are the relevant
ones. Both the post-onset mortality basis and the recovery rate are **[std]**.

**Prudential — solvency.** From **31 March 2026** insurers are supervised on the
economic-value **ESR** (経済価値ベースのソルベンシー規制), in which liabilities are 現在推計 plus MOCE,
re-measured at each 基準日 on assumptions re-set then, with required capital calibrated at
**99.5%** and early corrective action triggered below an ESR of 100% [REG-R15]. It
supersedes the ソルベンシー・マージン比率 trigger at **200%** [REG-R17], and the two are not comparable.
`jplib` computes neither. What it owes the regime is that its projections are re-runnable on
a re-set assumption basis at a stated 基準日 — for a third-sector product, precisely the
capability the ストレステスト already demands [R10]. J-GAAP reserving, ESR and IFRS 17 (voluntary
in Japan) are three separate measurement bases fed by one projection [REG-R47].

**Conduct.** 監督指針 fixes what the 契約締結前交付書面 must contain — 商品の仕組み, the main 支払事由 and 免責事由,
the attachable 特約, 保険期間, 引受条件, 保険料, 配当金に関する事項 and 解約返戻金等の水準 in the 契約概要; クーリング・オフ, 告知義務,
責任開始期, the main non-payment cases and 保険料の払込猶予期間・失効・復活 in the 注意喚起情報 [REG-R14] — which is,
item for item, the source document this specification is largely built from [S1]. The
point-of-sale disclosure of a numeric 基礎率変更権 standard [R10] rides on the 説明義務 of 金融サービス提供法
第4条 [REG-R39]; for a product whose benefit trigger is an administrative grade the customer
does not control, that duty is doing real work. クーリング・オフ is the eight-day dispatch-rule
right of 保険業法 第309条, scoped out here [REG-R36]. Non-disclosure remedies run under 保険法 第55条,
whose ceiling is five years from inception with a one-month clock from discovery [REG-R35];
the two-year contractual window observed [S1] is a permitted narrowing in the policyholder's
favour. The suicide exclusion of 保険法 第51条 carries no statutory time limit, so the absence of
a stated 免責期間 in this product's 免責事由 list [S2] is a contractual fact, not an oversight
[REG-R34]. On insurer failure, contracts are compensated up to **90% of the 責任準備金** at the
failure date through the 生命保険契約者保護機構 [REG-R40], the rate set by ordinance under 保険業法 第270条の3
[REG-R41].

**Tax.** Premiums for this product fall in the **介護医療保険料** basket of the post-2012 生命保険料控除
regime — one of three baskets (一般 / 介護医療 / 個人年金), each computed on the same schedule (up to
¥20,000 in full; ¥20,000–40,000 half plus ¥10,000; ¥40,000–80,000 a quarter plus ¥20,000;
above ¥80,000 a flat **¥40,000**), with an overall cap of **¥120,000** [R11] [REG-R43]. The
basket covers contracts written on or after 2012-01-01 paying on 疾病または身体の傷害等 where payment
is triggered by a 医療費支払事由, excludes terms under five years and savings-type contracts, and
requires every beneficiary to be the premium payer, a spouse or a relative [R12]. A contract
mixing coverages is assigned to the basket of its 主たる保障内容 and rider premiums are allocated
by the rider's own coverage [R11] — which is why the 主契約 + 特約 architecture of Japanese
products has a tax consequence, and why a dementia rider on a care contract does not change
the basket. The anchor cell's ¥11,500 monthly premium is ¥138,000 a year, comfortably past
the ¥80,000 point at which the basket deduction flattens to ¥40,000, so at the composite's
benefit level the marginal premium yen carries no relief at all.

**Professional standards and 三利源.** The 保険計理人 must give an 意見書 on, among other things, the
soundness of the reserve [REG-R6], supported by the 1号収支分析 of the profession's 実務基準 — a
projection of at least ten future years, per segment [REG-R22]. The ten-year horizon is the
same horizon the third-sector ストレステスト uses [R10], which is convenient rather than
coincidental. Because this chassis is **無配当**, none of the four surplus-distribution methods
of 施行規則 第30条の2 applies [REG-R9], and the 三利源 (死差 / 利差 / 費差) framing that drives dividends on
有配当 products has no dividend to drive here — it survives only as an analysis of where the
profit came from.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-nursing_care-r1
[R10]: #jplib-nursing_care-r10
[R11]: #jplib-nursing_care-r11
[R12]: #jplib-nursing_care-r12
[R13]: #jplib-nursing_care-r13
[R14]: #jplib-nursing_care-r14
[R15]: #jplib-nursing_care-r15
[R16]: #jplib-nursing_care-r16
[R2]: #jplib-nursing_care-r2
[R3]: #jplib-nursing_care-r3
[R4]: #jplib-nursing_care-r4
[R5]: #jplib-nursing_care-r5
[R6]: #jplib-nursing_care-r6
[R8]: #jplib-nursing_care-r8
[R9]: #jplib-nursing_care-r9
[REG-R1]: #jplib-reg-r1
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R13]: #jplib-reg-r13
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R23]: #jplib-reg-r23
[REG-R30]: #jplib-reg-r30
[REG-R32]: #jplib-reg-r32
[REG-R33]: #jplib-reg-r33
[REG-R34]: #jplib-reg-r34
[REG-R35]: #jplib-reg-r35
[REG-R36]: #jplib-reg-r36
[REG-R39]: #jplib-reg-r39
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R42]: #jplib-reg-r42
[REG-R43]: #jplib-reg-r43
[REG-R47]: #jplib-reg-r47
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[REG-R9]: #jplib-reg-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
