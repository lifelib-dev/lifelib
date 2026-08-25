# Technical Notes

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** These notes turn the standardized composite of `product-spec.md` (same
directory) into a reference liability cash-flow projection model on paper. They describe no
single insurer's product. [S#] and [R#] tags resolve in `sources.md`, whose numbering is
carried verbatim from `_research/medical.md` and is frozen; [REG-R#] tags resolve in the
cross-product reference library `references/regulatory-and-actuarial-references.md`, whose
R-numbering is separate. **[std]** marks a standardization introduced for the reference
implementation, always with a rationale and, where one exists, the observed range;
[unverified] marks a claim not confirmed against a retrieved document. **Every contractual
parameter these notes share with `product-spec.md` carries the same value there.** What
these notes add is the whole modelling basis, which `product-spec.md` does not carry
because none of it is contractual: the decrement assumptions (the mortality adjustment and
the lapse curve), the expense and commission scale, the 疾病/災害 limb split, and — the
three that carry the claim cost and are the load-bearing additions — the hospitalization
**incidence** rate, the **length-of-stay distribution**, and the **surgery frequency** per
hospitalization. Every one of them is introduced below as **[std]** with its rationale.

**This is the `jplib` third-sector chassis in model form.**
[cancer (がん保険)](../cancer/technical-notes.md) and [nursing care (介護保険)](../nursing_care/technical-notes.md)
state deltas against the machinery below — in particular against the day-limit ledger and
the frequency × severity × limit decomposition — rather than restating it.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows for a single-policy model
  point of third-sector medical insurance (*iryō hoken*, 医療保険): office premiums,
  hospitalization benefit (*nyūin kyūfukin*, 入院給付金), surgery benefit (*shujutsu kyūfukin*,
  手術給付金), advanced-medicine benefit (*senshin iryō kyūfukin*, 先進医療給付金),
  maintenance and claim expenses, and commission. The intended sense is the current estimate
  (*genzai suikei*, **現在推計**) that the economic-value solvency regime requires:
  probability-weighted future cash flows on assumptions re-set at a stated reporting date
  (*kijunbi*, 基準日) rather than locked in at issue [REG-R15]. It is also the shape
  the 1号収支分析 takes — a forward income-and-outgo projection over at least ten future
  years, by 区分経理 segment [REG-R22].
- **Out of scope, cited not reproduced.** Discounting, MOCE, required capital, and every
  reserving basis. Standard policy reserve (*hyōjun sekinin-junbikin*, 標準責任準備金),
  contingency reserve (*kiken junbikin*, 危険準備金) including the third-sector limb, the ESR
  balance sheet and IFRS 17 all consume these cash flows and are pointed at in *Valuation
  and reserve pointers*, not computed here.
- **Projection frequency.** Monthly grid. This is not a refinement of an annual model: the
  daily benefit's unit of account is a **day**, the per-hospitalization limit is 60 days —
  about two months — and the premium mode is monthly (月払) at every carrier in the
  composite [S1] [S4] [S10]. `t` is the **policy month**, `t = 0, 1, …, proj_len − 1`, and
  month `t` is the interval from `t` to `t + 1` months after the contract date
  (*keiyakubi*, 契約日).
- **Timing conventions [std].** Office premium received at the **start** of month `t`;
  maintenance expense at the start of month `t`; hospitalization, surgery and 先進医療
  benefits and the claim-handling expense at the **end** of month `t`; mortality then lapse
  applied at the end of month `t`, in that order. Acquisition expense and initial commission
  at `t = 0`.
- **Spell convention [std] — the one that matters.** A hospitalization *starting* in month
  `t` is resolved in full in month `t`: its paid days, its benefit, its surgery benefit and
  its consumption of both day limits are all recognised at `t`. Rationale: the
  per-hospitalization limit is a property of the whole spell, so a grid that split the spell
  would have to carry a partial-spell state, and the sourced mean stay is 20.2 days at ages
  35–64 and 28.4 days nationally [REG-R27] — under one month for the bulk of the
  distribution. The convention accelerates payment by at most `L1 / 30.4 − 1` months, about
  one month at `L1` = 60 and three at `L1` = 120, and the model does not discount, so the
  distortion is confined to the termination boundary and to deaths in hospital. A
  day-accrual alternative is named in the pitfalls list.
- **Age basis.** Attained age at 契約日 with the fraction discarded (*man-nenrei*, 満年齢),
  incremented at each 年単位の契約応当日 [S4] [S10]. Attained age in month `t` is
  `age(t) = x + floor(t / 12)`, `x` the 契約年齢. 第三分野標準生命表2018 is constructed for use on
  a nearest-birthday (*hoken-nenrei hōshiki*, 保険年齢方式) basis [R5] [REG-R20], so reading it
  at 満年齢 understates the valuation age by about half a year. `jplib` accepts the offset in
  the base run and marks it **[std]**; the alternative — reading the table at `age(t) + 0.5`
  — is a switch.
- **Currency.** JPY throughout. Amounts are yen; there is no minor unit in the contract, but
  expected values are fractional and are displayed to ¥0.01.
- **Model points.** One policy at a time, projected on an expected (probability-weighted)
  basis: `pols_if(t)` multiplies each per-policy cash flow. `Projection` is parameterized by
  `point_id`; no aggregation logic is specified here.
- **Termination.** Whole-of-life cover: the projection runs to the terminal age of
  第三分野標準生命表2018, **116 for males and 118 for females** [REG-R18] [REG-R20], so
  `proj_len = 12 × (terminal_age − x + 1)` — 924 months for the anchor cell. There is no
  maturity benefit and no 満期保険金; the only cash flow at the horizon is nothing at all
  [S1] [S6]. The product does, uniquely on this chassis, carry a **benefit-driven
  termination**: cover ceases when both the 疾病 and 災害 aggregate day limits are exhausted
  [S9], which is why the aggregate limit is a tracked state variable and not a cap applied
  at the end (see *Cash flow components*).
- **Contract boundary.** On the 終身 chassis the premium is level and 無配当 with no insurer
  repricing right [S3] [S6] [S8], so all future premiums and benefits are inside the
  boundary and the projection horizon is the whole of life. On the 定期 model-point flag the
  ten-year renewal reprices, which would ordinarily close the boundary at each renewal — but
  where the policy is on premium waiver, [REG-R14] II-2-1-2(4) requires the *reserve* to be
  computed as though every automatic renewal to final expiry occurs. The two treatments
  point in opposite directions; `jplib` projects the 定期 flag to final expiry and records the
  tension rather than resolving it.
- **Rounding.** Intermediates at full double precision. Displayed cash flows to ¥0.01,
  `pols_if` to six decimals, day ledgers to four decimals of a day **[std]**. Monthly rows
  rounded for display do **not** re-add to the displayed annual totals; the totals are sums
  of unrounded values.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | — |
| `chassis` | enum {shushin, teiki} | shushin (終身) |
| `issue_age` (`x`) | int, 満年齢, 20–80 | 40 |
| `sex` | enum {M, F} | M |
| `daily_amount` (`D`) | JPY per day, menu ¥3,000–¥15,000 | 5,000 |
| `limit_per_hosp` (`L1`) | int days ∈ {60, 120} | 60 |
| `limit_agg` (`LA`) | int days ∈ {1,095, 1,000}, per limb | 1,095 |
| `prem_period` | enum {whole_life, to_65} | whole_life (終身払) |
| `premium` (`P`) | JPY per month, office premium, model-point input | 2,100 **[std]** |
| `prem_mode` | enum {monthly, semiannual, annual} | monthly |
| `surg_mult_ih` (`m_ih`) | multiple of `D`, in hospital ∈ {20, 10} | 20 |
| `surg_mult_op` (`m_op`) | multiple of `D`, outpatient ∈ {5, 0} | 5 |
| `min_days_5` | bool — five-day minimum payment switch | false |
| `adv_rider` | bool — 先進医療特約 | true |
| `lump_rider` | bool — 入院一時金特約 | false |
| `tokusoku_3dis` | bool — 三大疾病無制限 特則 | false |
| `waiver_3dis` | bool — 特定三疾病保険料払込免除特則 | false |
| `surg_after_limit` | bool — pay in-hospital surgery once `L1` is exhausted | true |
| `issue_date` | date | — |

`premium` is an **input, not a computed quantity**. No carrier publishes a rate table by
age and duration; the statement of the method of calculating premiums and reserves
(*sanshutsu hōhō-sho*, 算出方法書) is a 基礎書類 filed with the 金融庁 and is not published [REG-R2]. The
anchor value sits between the two public specimen rates for this exact specification —
¥2,121 and ¥2,080 at age 40 male on a ¥5,000 daily amount, 60日型, 終身払 [S8] [S3].

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | In-force probability at the **start** of month `t`; `pols_if(0) = 1` | monthly recursion |
| `age(t)` | Attained 満年齢 = `x + floor(t / 12)` | annually |
| `agg_days_dis(t)` | 疾病 limb 通算 ledger: expected paid days consumed, **per surviving policy**, at the start of month `t` | monthly |
| `agg_days_acc(t)` | 災害 limb 通算 ledger, same basis | monthly |
| `adv_paid(t)` | 先進医療 ledger: cumulative 技術料 reimbursed per surviving policy, against the ¥20,000,000 cap | monthly |
| `waived(t)` | Probability the policy is on 保険料払込免除 at `t` (module; 0 in the base run) | monthly |
| `mort_rate_mth(t)` | Monthly best-estimate mortality applied in month `t` | lookup |
| `lapse_rate_mth(t)` | Monthly lapse applied in month `t`, after mortality | lookup |
| `inc_rate_mth(t)` | Monthly hospitalization incidence per in-force policy | lookup |
| `net_cf(t)` | Net cash flow of month `t`, insurer perspective, **income-positive** | monthly |

Three absences are product facts, not gaps. There is **no cash-surrender-value state**: the
main contract is without surrender value (*mu-kaiyaku-henreikin-gata*, 無解約返戻金型) at
every carrier during the premium-paying period [S1] [S6] [S9], so `cv_pp` does not exist on
the anchor cell and lapse carries **no cash flow**.
There is **no 契約者貸付 / 自動振替貸付 state**: with no surrender value there is nothing to lend
against, and one carrier says so in terms [S1] — so, unlike the
[whole life savings chassis (終身保険)](../whole_life/technical-notes.md), a missed premium really does
lapse the policy. And there is **no death benefit**: the main
contract pays nothing on death [S1] [S4] [S6] [S9] [S10], so mortality is a pure
liability-releasing decrement and `claims_death` does not exist.

The two day ledgers are **per surviving policy**, not weighted by `pols_if`. A ledger
multiplied by the in-force probability measures the block's consumption, not the
individual's, and defers the limit indefinitely. This is the easiest state-variable
error in the product.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| Daily benefit | `D` × paid days per hospitalization | [S1] [S2] [S6] [S9] [S10] |
| 日帰り入院 | Covered — the 支払事由 is one day or more of 入院 | [S3] [S6] [S9] |
| Per-hospitalization limit `L1` | 60 days (120 switch); elected at issue, never changeable | [S1] [S4] [S9]; **[std]** default |
| One-hospitalization test | Same cause or medically related; new spell on the **181st day** counting the day after discharge as day 1 | [S1] [S2] [S6] [S7] [S10] |
| Aggregate limit `LA` | 1,095 days, **separately** for the 疾病 and 災害 limbs | [S4] [S6] [S7] [S10]; separateness [S4] [S1] |
| Termination on exhaustion | Contract ceases when **both** limbs are exhausted | [S9] |
| 災害 limb | Same daily amount; admission within 180 days of the accident | [S1] [S4] [S9] [S10] |
| Concurrency | 疾病 and 災害 benefits never paid for the same day | [S1] [S2] [S4] [S9] [S10] |
| Surgery multiple | `m_ih` = 20 in hospital, `m_op` = 5 outpatient; unlimited count | [S1] [S3] |
| Surgery trigger | Procedures chargeable under 手術料 in the 医科診療報酬点数表, plus 放射線治療料 and 骨髄移植術 limbs, plus 先進医療 | [S1] [S2] [S4] [S9] [S10] |
| Surgery frequency limits | One per day (highest paying); per-day-charged 手術料 pays day one only; 放射線照射 and 温熱療法 at most once per 60 days | [S1] [S2] [S9] [S10] |
| 先進医療 cap | ¥20,000,000 lifetime; rider terminates on reaching it | [S1] [S3] [S5] [S6] [S7] [S9] |
| 先進医療 top-up | 10% of the benefit, capped ¥500,000 per 療養 | [S1]; **[std]** composite |
| Surrender value | Zero under 終身払 at every duration; 10 × `D` after a completed 短期払 | [S1] [S6] [S9] |
| Grace, 月払 | To the last day of the month following the 払込期月 | [S1] [S4] [S10] |
| 復活 | Within 1 year of 失効, fresh 告知, clocks reset to the 復活日 | [S4] [S9]; **[std]** composite |
| Suicide | Nothing paid within 3 years of 責任開始日 | [S1]; statutory frame [REG-R34] |

### (b) Insurer-discretionary current elements

This class is **nearly empty, and its emptiness is the product fact.** The main contract is
non-participating (*mu-haitō*, 無配当) — carried in the formal product name at three of the
five carriers [S2] [S6] [S7] and stated in terms at two [S1] [S6], with no retrieved
document showing a participating medical main contract anywhere. So there
is no policyholder dividend (契約者配当), and the 三利源 framing of 死差 / 利差 / 費差 and
the surplus-distribution methods of 施行規則 第30条の2 [REG-R9] simply do not
attach to it. There is no premium review on the 終身 chassis, no MVA, no bonus
and no non-guaranteed charge scale. What remains:

| Input | Snapshot value | Basis |
|---|---|---|
| Incidence basis (*kiken hasseiritsu*, 危険発生率) | The insurer's own, unpublished, sitting in the 算出方法書 | [REG-R2]; regulator requires a **test**, not a table [R3] [REG-R13] [REG-R14] |
| 定期 flag renewal rates | Recomputed at each ten-year renewal at then-current rates | [S7] [S10]; base run holds the issue rate flat **[std]** |
| Catastrophe proportionality | Insurer may pay in full or reduce in proportion after earthquake, eruption, tsunami or war | [S4]; not modelled **[std scope]** |
| Prospective 支払事由 change | Insurer may vary the surgery trigger with 主務官庁 approval if the 診療報酬点数表 is amended | [S2] [S6]; not modelled **[std scope]** |

### (c) Behavioral / experience assumptions (modeler's view)

**Mortality.** 第三分野標準生命表2018 is public, free and machine-readable [REG-R18]
[REG-R19] — the sharp contrast with [uklib](../../../uklib/index.md), which had to proxy
subscriber-only CMI tables.
But it is a **valuation** table, and on a morbidity product its margin runs the *wrong way
for a best estimate*: death releases the liability, so the table is set deliberately
**below** national mortality, with the risk-theory adjustment bounded **below at 70% and
above at 85%** of the pre-adjustment rate [R5] [REG-R20]. Male q40 on it is **0.00076**
against 0.00118 on 生保標準生命表2018（死亡保険用） [R4] [REG-R18]. A best-estimate medical
model must therefore scale it **up**:

    mort_rate(age) = mort_be_factor × q_third_sector(age, sex)

with `mort_be_factor` = **1.25 [std]** — the reciprocal of 0.80, a round value inside the
sourced 0.70–0.85 adjustment band [REG-R20] and a little above its 0.775 midpoint, so the factor
unwinds the table's stated margin and nothing more. Reading the band's own endpoints
instead would give 1.176 at 0.85 and 1.429 at 0.70, which is the range the single figure
stands over. At age 40 male this gives 0.00095, between the two published tables, which is
the direction sanity requires. `mort_rate_mth(t) = 1 − (1 − mort_rate(age(t)))^(1/12)`
**[std]**. Two further table facts a model must not blur: 第三分野標準生命表2018 **excludes
高度障害** (severe disability), unlike its 2007 predecessor [R5] [REG-R20], so a 高度障害 state
must be added separately and not read out of the table; and the IAJ's site terms prohibit
reproduction and transmission without written consent [REG-R21], so `jplib` ships
`mort_table.csv` as a **[std]** construction whose `provenance` column points at [REG-R18]
and [REG-R19], never as a copy. That construction is the library's **canonical** one and
is shared, value for value, with every other `jplib` product that reads a third-sector
rate: the 22 rates the research pass read out of the table are carried as anchors and
reproduced exactly, and the ages between adjacent anchors are graduated log-linearly,
`q(x) = q(a)·(q(b)/q(a))^((x−a)/(b−a))` — locally the Gompertz family the table itself
follows. So the 0.00076 quoted above is the number the shipped file holds at 男 40, not an
approximation to it.

**Morbidity — the incidence basis, and where it comes from.** There is no published
morbidity table in Japan: 日本アクチュアリー会 publishes the mortality basis only [R4] [REG-R23],
and every insurer's 危険発生率 is its own [REG-R2]. What is public, and what makes this model
buildable, is Patient Survey (*kanja chōsa*, 患者調査), a 基幹統計 of 厚生労働省 [R6] [R7]
[REG-R26] [REG-R27]. The construction, in three steps:

1. **入院受療率** (*nyūin juryō-ritsu*) is a point-in-time **prevalence** per 100,000
   population — the expected proportion of the population in hospital on the census day, not
   an incidence rate [REG-R26]. Sourced values (October 2023, both sexes): national 945; by
   five-year band 20–24 137 · 30–34 239 · **40–44 258** · 50–54 441 · 60–64 838 · 70–74
   1,502 · 80–84 2,952 · 90歳以上 6,275 [R6] [REG-R26].
2. **退院患者平均在院日数** (*heikin zaiin nissū*) gives mean stay, September 2023: national
   28.4 days; by age band 0–14 **7.6** · 15–34 **10.5** · 35–64 **20.2** · 65歳以上 **35.5**
   [R6] [REG-R27].
3. In a stationary population, person-days in hospital per year equal admissions × mean
   stay, so the **[std] conversion** — flagged as needed and as a standardization by
   [REG-R26] itself — is

       inc_rate(age) = (juryoritsu(band(age)) / 100,000) × 365 / alos(band(age))

   annual hospitalization incidence per life, with `inc_rate_mth(t) = inc_rate(age(t))/12`
   **[std]** (uniform within the policy year). At age 40 this gives
   `0.00258 × 365 / 20.2 = 0.046619` per year. The band mapping is **[std]**: 受療率 uses the
   five-year band, 平均在院日数 the four broad bands, because that is the granularity each
   statistic is published at [REG-R26] [REG-R27].

**Length-of-stay distribution [std].** A single mean is not usable: the sourced per-cause
means run from **白内障 2.4 days** to **精神及び行動の障害 290.4 days** [R6] [REG-R27], and a
60-day cap bites at one end and never at the other. 患者調査 publishes the stay distribution
in **32 bands** by five-year age band and cause (e-Stat tables Z111, Z114–Z117, cumulative
Z120), but those CSV files were **not downloaded** in the research pass [R7] [REG-R33], so
the distribution's shape is **[std]** — a five-band discrete distribution over the *same*
day values at all ages, with the probabilities in each row solved so that the row mean
**equals the sourced 平均在院日数 for that band exactly** [REG-R27]:

| Age band | stay = 2 d | 8 d | 20 d | 45 d | 160 d | mean (= sourced) |
|---|---|---|---|---|---|---|
| 0–14 | 0.565 | 0.325 | 0.080 | 0.022 | 0.008 | 7.6 |
| 15–34 | 0.460 | 0.340 | 0.150 | 0.036 | 0.014 | 10.5 |
| **35–64** | **0.300** | **0.325** | **0.225** | **0.100** | **0.050** | **20.2** |
| 65+ | 0.190 | 0.240 | 0.250 | 0.200 | 0.120 | 35.5 |

The 160-day band stands for the psychiatric and neurological tail that drives the sourced
national mean [REG-R27]; the 2-day band for the day-surgery mode. Any user with the Z120
CSVs should replace the whole table — that is what the `provenance` column is for.

**Sex [std].** The 概況 publishes 入院受療率 by sex for all ages (893 male / 995 female) and by
age band for both sexes combined, but **not the age × sex cross-tabulation**, which lives in
e-Stat table Z69 and was not downloaded [R6] [R7] [REG-R33]. The sex factor on incidence is
therefore **[std]**: male 1.00 at every age; female **1.45** at ages 20–34, **0.80** at 35
and over. It is chosen so the *incidence* ordering crosses over between ages 30 and 40 —
female heavier below, lighter above — because both published premium scales show that
crossover, a morbidity fact and not a pricing artefact [S3] [S8]. Whether it reproduces
the *premium* crossover depends on the mortality and expense loads too, and is a validation
target for the model, not a claim here.

**Surgery frequency [std].** 患者調査 crosses 推計退院患者数 and 平均在院日数 with 手術の有無
(Z106–Z109, Z125, Z126), giving a public in-hospital surgery proportion — but again the CSVs
were not downloaded [R7] [REG-R33]. So: `surg_ih_per_hosp` = **0.35** payable surgeries per
hospitalization at the in-hospital multiple, and `surg_op_per_hosp` = **0.15** per
hospitalization at the outpatient multiple, both **[std]**, both scaling with incidence so
that surgery frequency ages with hospitalization frequency. Radiation therapy is **inside**
these frequencies, not a separate stream: the composite folds 放射線治療 into 手術給付金 through
the 放射線治療料 limb of the trigger, subject to the 60-day lockout every carrier imposes [S1]
[S2] [S6] [S9] [S10].

**先進医療 [std].** Frequency `adv_freq` = **0.00040 per life-year**, flat across ages.
Severity `adv_sev` = **¥150,000 per 療養**. The sourced anchors: in 令和5年度, 144,282 patients
received 先進医療 across 81 technologies; 先進医療A averaged about **¥67,700** per case, while
陽子線治療 ran to about ¥2,660,000 over 824 cases and 重粒子線治療 to about ¥3,140,000 over 462
cases [R9]. A count-weighted mean of just those three figures is about ¥92,300 — but the A
count is dominated by high-volume fertility technologies whose exposure is not this rider's
[R9], so the [std] severity sits about 1.6× above it. No public exposure denominator for the
frequency was retrieved, so it carries no observed range. The spread the [std] tag is
standing over is a **factor of 46** between the 先進医療A average per case and 重粒子線治療's
[R9]; no per-technology minimum was extracted, so the true spread is wider than that.

**Lapse [std].** The only published industry-wide persistency figure in Japan is
解約・失効率 5.6% p.a. on 個人保険, measured on **opening in-force sum assured** [REG-R31] — a
sum-assured-weighted rate on a book dominated by 定期 and 終身 death cover, which a 医療保険 with
no sum assured cannot even enter. No Japanese durational lapse curve is public. The [std]
table is anchored to that figure by construction:

| Policy year | 1 | 2 | 3 | 4 | 5 | 6–20 | 21+ |
|---|---|---|---|---|---|---|---|
| `lapse_rate` **[std]** | 9.0% | 7.0% | 6.0% | 5.5% | 5.0% | 4.5% | 3.0% |

The first ten years average **5.5%**, at the sourced 5.6% [REG-R31]. The 21+ step down is
[std] reasoning stated openly: on a contract with no surrender value and rising morbidity
exposure, a long-duration policyholder has no cash incentive to lapse and a growing reason
not to. `lapse_rate_mth(t) = 1 − (1 − lapse_rate(year(t)))^(1/12)` **[std]**.

**Premium waiver [std].** The base 保険料払込免除 is disability-triggered — 高度障害状態 from any
cause, or a listed 身体障害の状態 from an 不慮の事故 within 180 days [S1] [S2] [S10]. Because
第三分野標準生命表2018 **excludes** 高度障害 [R5] [REG-R20], the incidence cannot be read out of
the mortality basis, and no public Japanese 高度障害 incidence table was retrieved. The waiver
is therefore specified as a state with `waiver_inc` = **0 in the base run [std]**, and a
suggested placeholder of 0.25 × `mort_rate(age)` when switched on. The anchor cell is 終身払,
so the waiver is live for the entire projection when it is switched on — which is exactly
why leaving it at zero must be stated rather than assumed.

**Expenses and commission (all levels [std]; no Japanese medical expense or commission
scale is public).**

| Input | Value | Basis |
|---|---|---|
| Acquisition expense | ¥20,000 per policy at `t = 0` | **[std]** |
| Initial commission | 1.5 × annualized premium at `t = 0` (¥37,800 on the anchor) | **[std]** |
| Renewal commission | 3.0% of premiums from policy year 2 | **[std]** |
| Maintenance expense | ¥250 per policy per month, inflating 1.0% p.a. at each anniversary | **[std]** |
| Claim expense | ¥3,000 per hospitalization event (covers the day benefit and any surgery on the same spell) | **[std]** |
| Expense inflation | 1.0% p.a. flat | **[std]** |

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning |
|---|---|
| `t` | policy month, `t = 0, 1, …, proj_len − 1` |
| `x`, `age(t)` | 契約年齢 (満年齢); attained age `x + floor(t/12)` |
| `y(t)` | policy year, `floor(t/12) + 1` |
| `D` | 入院給付金日額, JPY per day |
| `L1`, `LA` | per-hospitalization day limit (60); 通算 day limit per limb (1,095) |
| `F` | five-day minimum floor: 5 when `min_days_5`, else 0 |
| `g_j`, `pi_j` | length-of-stay band day-value and probability, `j = 1..5` |
| `i(t)` | monthly hospitalization incidence per in-force policy, `inc_rate(age(t))/12` |
| `s_dis`, `s_acc` | limb split of incidence: 0.92 / 0.08 **[std]** |
| `d_pay` | expected **paid days** per hospitalization = `Σ_j pi_j × min(g_j, L1)` |
| `d_ben` | expected **benefit days** per hospitalization = `Σ_j pi_j × max(F, min(g_j, L1))` |
| `A_dis(t)`, `A_acc(t)` | 通算 ledgers, days, per surviving policy |
| `V(t)` | 先進医療 ledger, JPY, per surviving policy; cap `LV` = 20,000,000 |
| `s_ih`, `s_op` | surgeries per hospitalization, in hospital / outpatient (0.35 / 0.15) |
| `m_ih`, `m_op` | surgery multiples of `D` (20 / 5) |
| `f_adv`, `S_adv` | 先進医療 monthly frequency and mean 技術料 per 療養 |
| `q(t)`, `w(t)` | `mort_rate_mth(t)`, `lapse_rate_mth(t)` |
| `P`, `e(t)`, `ec` | monthly office premium; monthly maintenance expense; claim expense per hospitalization |

**Dimensional check.** `i(t)`, `q(t)`, `w(t)` and `pi_j` are dimensionless probabilities per
month or per event. `g_j`, `d_pay`, `d_ben`, `A_dis`, `A_acc`, `L1` and `LA` are **days**.
`D` is JPY/day, so `D × d_ben` is JPY per hospitalization and `i(t) × D × d_ben` is JPY per
policy-month. `m_ih` and `m_op` are dimensionless multiples of `D`, and `s_ih`, `s_op` are
surgeries per hospitalization, so `i(t) × s_ih × m_ih × D` is again JPY per policy-month.
`V(t)`, `S_adv`, `P`, `e(t)` and `ec` are JPY. Every `net_cf` term is JPY per month. The
error this check catches is the commonest one in the product: multiplying a **prevalence**
(dimensionless) by a daily amount as if it were an incidence (per month).

### The day-limit machinery

Three limits act in a fixed order, and getting the order wrong is the classic implementation
failure.

**1 — the per-hospitalization limit `L1`.** Applied *inside* the length-of-stay
expectation, spell by spell, before anything else:

    d_pay = Σ_j pi_j × min(g_j, L1)

On the anchor cell's 35–64 row this is `0.300×2 + 0.325×8 + 0.225×20 + 0.100×45 +
0.050×60 = 15.20` days, against an uncapped mean of 20.20 — the 60-day cap removes
**24.75%** of raw days. At `L1` = 120 it is 18.20 days.

**2 — the five-day minimum, which is an amount and not days.** The carriers express the
floor as 「入院日数が5日以内の場合は、入院給付金日額×5」 — a payment of `D × 5`, not a credit of five
days [S4] [S6] [S7]. So it enters `d_ben` and **not** `d_pay`:

    d_ben = Σ_j pi_j × max(F, min(g_j, L1))

With `F` = 5 the 35–64 row gives 16.10 benefit days against 15.20 paid days — the floor adds
0.90 days of benefit (+5.9%) and **zero days** to the 通算 ledger. A model that credits the
floor to the ledger would let a short stay consume days it never used.

**3 — the aggregate limit `LA`, per limb, with memory.** Two ledgers, because the 通算 limit
is applied separately to the 疾病 and 災害 limbs [S4] [S1]:

    room_dis(t)  = max(0, LA − A_dis(t))
    d_pay_dis(t) = min(d_pay, room_dis(t))
    d_ben_dis(t) = d_ben × d_pay_dis(t) / d_pay          [std proportional scaling]

and identically for the 災害 limb. The scaling as written is the base run's, where nothing
is exempt. Under the 三大疾病無制限 特則 the exempt days do not depend on the ledger at all,
so they are held out of the scaling and added back unscaled: writing `d_ben_free` for them
and `d_ben_ltd` for the rest, `d_ben_dis(t) = d_ben_free + d_ben_ltd × d_pay_dis(t) / d_pay`,
and `d_pay` itself carries only the non-exempt share. A model that scaled the exempt days
by the ledger room would re-impose the limit the 特則 removes. The 疾病/災害 split of incidence is **[std]** at 0.92 / 0.08:
損傷・中毒等 is 107 of the national 入院受療率 of 945 (11.3%) [REG-R26], and not every 損傷
admission arises from an 不慮の事故 with admission inside 180 days [S1] [S4] [S9] [S10]. In the
base run the two limbs carry the **same** `D`, `L1` and length-of-stay distribution, so the
split is economically inert in the cash flows and structurally essential in the ledgers —
which is precisely the reason there are two of them.

**Benefit-driven termination.** Cover ceases when **both** limbs are exhausted [S9]:

    term(t) = 1 if A_dis(t) ≥ LA and A_acc(t) ≥ LA, else 0

**The honest statement about the aggregate limit.** On a deterministic expected-value grid,
`A_dis` grows by roughly `inc_rate(age) × d_pay` days a year — 0.709 days a year at age 40,
about 15.2 at 90+ — so for the anchor cell it reaches only single-digit hundreds of days by
the terminal age and **`LA` never binds**, `term(t)` stays 0, and the 先進医療 cap is never
approached either. That is a property of the expectation, not of the product:
`E[min(Σ days, LA)] ≠ min(E[Σ days], LA)`, and the deterministic ledger therefore
**understates** the limit's bite by ignoring dispersion **[std]**. The machinery is
specified and implemented anyway for two reasons. A seriatim or stochastic run needs it,
because the dispersion the expectation averages away is exactly what makes `LA` bite. And
the 三大疾病無制限 特則 cannot be expressed without it: the 特則 takes がん, 心疾患 and
脳血管疾患 days out of the 通算 count entirely [S1] [S2], which is a change in *what the
ledger counts* — and which defers the termination further still rather than bringing it
closer. It is **not** kept for the two deltas: **neither dependant inherits it.**
[cancer (がん保険)](../cancer/technical-notes.md) records having no `L1` and no `LA` at all, and
[nursing care (介護保険)](../nursing_care/technical-notes.md) no `d_pay`, no `d_ben` and no `agg_days_*`
ledger — each states the deletion as a product fact of its own. Do not delete a ledger
because it reads zero.

### 先進医療 recursion

    pay(t)       = min(S_adv, LV − V(t))
    adv_claim(t) = f_adv × [ pay(t) + min(0.10 × pay(t), 500,000) ]
    V(t+1)       = V(t) + f_adv × pay(t)

The rider terminates when `V` reaches `LV` = ¥20,000,000 [S1] [S5]. Eligibility is tested at
the treatment date, so a technology that has left the 厚生労働大臣's 先進医療 list pays nothing
[S1] [S5], and 患者申出療養 is a different scheme and is excluded [S6] — both are scope facts,
not modelled states.

### Surgery recursion

    surg_ih_eff(t) = s_ih                          if surg_after_limit
                   = s_ih × d_pay / Σ_j pi_j g_j   otherwise                  [std]
    claims_surgery(t) = pols_if(t) × i(t) × D × ( surg_ih_eff(t) × m_ih + s_op × m_op )

The switch resolves a **contradiction between carriers**, not a gap: where surgery is
performed during a stay for which 入院給付金 is no longer payable because `L1` is exhausted, one
carrier pays at the in-hospital multiple [S4] and another pays nothing at all [S10]. The
composite pays [S4]. With the switch reversed, and surgeries assumed uniform over stay-days
**[std]**, the truncated day fraction `1 − 15.20/20.20 = 24.75%` of in-hospital surgeries
fall outside cover. The two differ by a quarter of the in-hospital surgery benefit —
they are not roundable into each other.

### Processing order

For `t = 0, 1, …, proj_len − 1`:

1. **Start of month.** `premiums(t) = P × pols_if(t) × (1 − waived(t))`;
   maintenance `e(t) × pols_if(t)` with `e(t) = 250 × 1.01^floor(t/12)`;
   renewal commission `0.03 × premiums(t)` for `t ≥ 12`. At `t = 0` additionally the
   acquisition expense ¥20,000 and the initial commission `1.5 × 12P`.
2. **Look up the age basis.** `age(t)`, hence `mort_rate(age(t))`, `inc_rate(age(t))` and
   the length-of-stay row; hence `d_pay` and `d_ben` at the model point's `L1` and `F`.
3. **Apply the ledgers.** `d_pay_dis`, `d_ben_dis`, `d_pay_acc`, `d_ben_acc` per the room
   formulas above; `min(S_adv, LV − V(t))` for the rider.
4. **End of month — claims.**

       claims_hosp(t)     = pols_if(t) × D × i(t)
                            × ( s_dis·d_ben_dis(t) + s_acc·d_ben_acc(t) )
       claims_surgery(t)  = pols_if(t) × i(t) × D × ( surg_ih_eff(t)·m_ih + s_op·m_op )
       claims_advanced(t) = pols_if(t) × adv_claim(t)
       claims(t)          = claims_hosp(t) + claims_surgery(t) + claims_advanced(t)

   and the claim-handling expense `pols_if(t) × i(t) × ec`.
5. **End of month — decrements**, mortality **then** lapse **[std order]**, plus the
   benefit-driven termination:

       pols_if(t+1) = pols_if(t) × (1 − q(t)) × (1 − w(t)) × (1 − term(t))

   Lapse pays **nothing** — there is no surrender value on the anchor cell [S1] [S6] [S9] —
   so `claims_lapse(t)` is identically zero, and that zero is the product fact worth
   publishing.
6. **Ledger update**, unweighted by `pols_if`:

       A_dis(t+1) = A_dis(t) + i(t) × s_dis × d_pay_dis(t)
       A_acc(t+1) = A_acc(t) + i(t) × s_acc × d_pay_acc(t)
       V(t+1)     = V(t) + f_adv × min(S_adv, LV − V(t))

### Net cash flow

    net_cf(t) = premiums(t)
              − claims_hosp(t) − claims_surgery(t) − claims_advanced(t)
              − expenses(t) − claim_expenses(t)
              − commissions(t)

with `expenses(t) = e(t)·pols_if(t) + 20,000·1{t = 0}`,
`claim_expenses(t) = ec·i(t)·pols_if(t)` and
`commissions(t) = 1.5·12P·1{t = 0} + 0.03·premiums(t)·1{t ≥ 12}`. `net_cf` is
**income-positive** in the shipped model, per the library convention.

`expenses` is **acquisition and maintenance only**, and the claim handling expense is a
line of its own — its own cells, its own subtraction above, and its own column in
`result_cf()`. That is the meaning the two names carry in every model in the three
libraries, and it keeps the acquisition strain and the morbidity-driven handling cost
from moving together in one figure.

---

## Policyholder behavior modeling

- **Lapse is real and immediate.** On a product with a surrender value (*kaiyaku-henreikin*,
  解約返戻金) the insurer would advance an unpaid premium under 自動振替貸付, which
  [REG-R14] IV-1-12 requires be at the policyholder's
  **election** with prompt notice. This chassis has none, and one carrier states
  that neither 契約者貸付 nor 自動振替貸付 is offered [S1]. So there is no mechanism that carries a
  policy through a missed premium, and no lapse-suppression term belongs in the recursion.
  This is the structural fork between the third-sector and savings chassis in `jplib`,
  and it is why the 自動振替貸付 machinery of the
  [whole life savings chassis (終身保険)](../whole_life/technical-notes.md) must **not** be inherited
  here.
- **Grace [std scope].** Grace runs to the last day of the month following the 払込期月 [S1]
  [S4] [S10] — roughly one month. The base run applies lapse at the end of the month in
  which the premium is missed and does not model the one-month lag or the grace-window claim
  rule (a claim in grace is paid net of the arrears, and if the benefit is smaller than the
  arrears and the balance is unpaid, **neither the benefit nor the waiver** is given [S4]).
  The lag is a one-month timing effect on an undiscounted projection; the grace-window rule
  is second-order and is named rather than modelled.
- **Reinstatement (復活) [std scope].** Available within one year at the composite [S4] [S9],
  but a reinstated policy is **not the policy that lapsed**: the 責任開始期 for
  pre-existing-condition tests resets to the 復活日 [S4] and waiting periods re-run from it
  [S9]. It therefore belongs in the model as a *new model point*, not as a negative lapse,
  and the base run treats lapse as absorbing. The composite's choice of a one-year window is
  the widest carrier divergence in the product — not available at all at one carrier [S6]
  [S8], three years at another [S10] — and it is the parameter that decides whether
  lapse is absorbing.
- **No dynamic lapse from surrender value or interest.** With no cash value, no assumed
  interest rate (*yotei riritsu*, 予定利率) disclosure on this chassis and no MVA, there is
  no economic surrender trigger to model.
  The 低解約返戻金型 cliff that drives the
  [whole life (終身保険)](../whole_life/technical-notes.md) surrender spike has no analogue here.
- **Anti-selective lapse [std] (optional module, off in the base run).** Healthy lives lapse
  first; the persisting block is progressively impaired on the *morbidity* basis rather than
  the mortality one, which is the reverse of the term-assurance case:

      inc_eff(t) = inc_rate(age(t)) × [ 1 + lam × max(0, w_cum(t) − w_ref) ]

  with `w_cum(t)` the cumulative lapse proportion, `w_ref` = 0.20, `lam` = 0.30 **[std]**.
  Base run `lam` = 0. No Japanese selective-lapse evidence was retrieved.
- **型 elections are not behaviour.** `L1`, `LA` and the 三大疾病無制限 特則 are elected at issue
  and can **never** be changed [S4] [S9] [S2]. They are model-point attributes; a model that
  lets them move over the projection is modelling something that does not exist.
- **Advance payment (前納) and mode.** Monthly is the dominant retail mode and one net-direct
  product is 月払 only [S10]; 6- or 12-month prepayment at a company-set discount [S4] is
  treated as an immaterial modal refinement and is not modelled **[std scope]**.
- **クーリング・オフ.** Out of scope: it is a pre-inception decrement, eight days from dispatch
  under 保険業法 第309条 [REG-R36] and contracted to fifteen at one carrier [S1], and modelling
  it would need a new-business funnel this library does not have.

---

## Worked example

**Anchor cell (`point_id = 1`).** Male, 契約年齢 40 (満年齢), 終身 chassis, 入院給付金日額
`D` = ¥5,000, `L1` = 60 日型, `LA` = 1,095 日 per limb, 終身払, office premium `P` = ¥2,100
per month, 手術給付金 20倍 / 5倍, 先進医療特約 attached, five-day minimum **off**,
三大疾病無制限 特則 **off**, 入院一時金特約 **off**, waiver module **off**,
`surg_after_limit` **true**.

Assumption values used, every one of them:

- **Mortality.** 第三分野標準生命表2018 男 q40 = **0.00076** [R4] [REG-R18], quoted here because
  a worked example needs it and `jplib` quotes only the rates it uses [REG-R21]. Best
  estimate `mort_rate(40) = 1.25 × 0.00076 = 0.00095` **[std]**;
  `mort_rate_mth = 1 − (1 − 0.00095)^(1/12) = 0.0000792012`.
- **Lapse.** Policy year 1, `lapse_rate = 9.0%` **[std]**;
  `lapse_rate_mth = 1 − (1 − 0.09)^(1/12) = 0.0078284203`.
- **Incidence.** 受療率(40–44) = **258** per 100,000 [R6] [REG-R26]; 平均在院日数(35–64) =
  **20.2** days [R6] [REG-R27]; so `inc_rate(40) = 0.00258 × 365 / 20.2 = 0.046618812` per
  year and `i(t) = 0.0038849010` per month **[std conversion]**.
- **Length of stay.** The 35–64 **[std]** row: days (2, 8, 20, 45, 160) with probabilities
  (0.300, 0.325, 0.225, 0.100, 0.050), mean 20.2 exactly. Hence
  `d_pay = d_ben = 15.20` days (floor off).
- **Surgery.** `s_ih` = 0.35, `s_op` = 0.15 **[std]**; benefit per hospitalization
  `= 5,000 × (0.35 × 20 + 0.15 × 5) = 5,000 × 7.75 = ¥38,750`.
- **先進医療.** `f_adv` = 0.00040 / 12 = 0.0000333333 per month **[std]**; benefit per 療養
  `= 150,000 + min(0.10 × 150,000, 500,000) = ¥165,000` **[std]**.
- **Expenses.** `e(t)` = ¥250 (policy year 1); `ec` = ¥3,000; acquisition ¥20,000; initial
  commission `1.5 × 12 × 2,100 = ¥37,800`; renewal commission 3% from `t = 12` — so zero in
  every row below **[std]**.
- **Limb split.** `s_dis` = 0.92, `s_acc` = 0.08 **[std]**.

Every decrement rate above is either quoted from 第三分野標準生命表2018 [REG-R18] or from
患者調査 [REG-R26] [REG-R27] with its citation, or is marked **[std]** as an illustrative
value in the shape of such a table. None of them is an insurer's basis, and none could be:
the 算出方法書 is not published [REG-R2].

| t | `pols_if` | `premiums` | `claims_hosp` | `claims_surgery` | `claims_advanced` | `expenses` | `claim_expenses` | `commissions` | `net_cf` | `agg_days_dis` |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 2,100.00 | 295.25 | 150.54 | 5.50 | 20,250.00 | 11.65 | 37,800.00 | −56,412.95 | 0.0000 |
| 1 | 0.992093 | 2,083.40 | 292.92 | 149.35 | 5.46 | 248.02 | 11.56 | 0.00 | +1,376.09 | 0.0543 |
| 2 | 0.984249 | 2,066.92 | 290.60 | 148.17 | 5.41 | 246.06 | 11.47 | 0.00 | +1,365.20 | 0.1087 |
| 3 | 0.976466 | 2,050.58 | 288.30 | 147.00 | 5.37 | 244.12 | 11.38 | 0.00 | +1,354.41 | 0.1630 |

**Trace, month 0.** `pols_if(0) = 1`. Premium `= 2,100 × 1 = 2,100.00`.
Incidence `i(0) = 0.046618812 / 12 = 0.0038849010`.
`claims_hosp = 1 × 5,000 × 15.20 × 0.0038849010 = 76,000 × 0.0038849010 = 295.2525` — and
the 92/8 limb split does not change it, since `0.92 × 15.20 + 0.08 × 15.20 = 15.20`.
`claims_surgery = 0.0038849010 × 38,750 = 150.5399`.
`claims_advanced = 0.0000333333 × 165,000 = 5.50`.
`expenses = 250 (maintenance) + 20,000 (acquisition) = 20,250.0000`;
`claim_expenses = 0.0038849010 × 3,000 = 11.6547`.
`commissions = 1.5 × 25,200 = 37,800.00`.
`net_cf(0) = 2,100.00 − 295.2525 − 150.5399 − 5.50 − 20,250.0000 − 11.6547 − 37,800.00
= −56,412.95`.
Ledgers: `A_dis(1) = 0 + 0.0038849010 × 0.92 × 15.20 = 0.054326` days;
`A_acc(1) = 0.0038849010 × 0.08 × 15.20 = 0.004724` days; `V(1) = 0.0000333333 × 150,000
= ¥5.00`. Neither ledger is anywhere near its limit and `term(0) = 0`.
Decrements: `pols_if(1) = 1 × (1 − 0.0000792012) × (1 − 0.0078284203) = 0.992093`.

**Trace, month 1.** `pols_if(1) = 0.992093`. Premium `= 2,100 × 0.992093 = 2,083.3953`.
Every per-policy rate is unchanged — `age(1) = 40`, policy year still 1 — so each claim
line is month 0's scaled by `pols_if`: `claims_hosp = 295.2525 × 0.992093 = 292.9179`;
`claims_surgery = 150.5399 × 0.992093 = 149.3496`;
`claims_advanced = 5.50 × 0.992093 = 5.4565`.
`expenses = 250 × 0.992093 = 248.0233` — no acquisition expense after `t = 0`;
`claim_expenses = 11.6547 × 0.992093 = 11.5625`. `commissions = 0` (renewal commission
starts at `t = 12`).
`net_cf(1) = 2,083.3953 − 292.9179 − 149.3496 − 5.4565 − 248.0233 − 11.5625 = +1,376.09`.
`A_dis(2) = 0.054326 + 0.0038849010 × 0.92 × 15.20 = 0.108653` days.
`pols_if(2) = 0.992093 × 0.992093 = 0.984249`.

**Trace, month 2.** Identical structure. Every line is month 0's scaled by
`pols_if(2) = 0.98424852`: `premiums = 2,066.9219`; `claims_hosp = 290.6018`;
`claims_surgery = 148.1687`; `claims_advanced = 5.4134`; `expenses = 246.0621`;
`claim_expenses = 11.4711`; `net_cf(2) = +1,365.20`. `A_dis(3) = 0.162979`.
`pols_if(3) = 0.976466`.

**Policy year 1 in aggregate** (`t = 0…11`, all at age 40, all in policy year 1 — the
strongest single test target in this file, because it exercises the whole annual cycle on
one set of rates). `Σ_{t=0}^{11} pols_if(t) = 11.491651`, so:

| Line | Policy year 1 total |
|---|---|
| `premiums` | 24,132.47 |
| `claims_hosp` | 3,392.94 |
| `claims_surgery` | 1,729.95 |
| `claims_advanced` | 63.20 |
| `expenses` | 22,872.91 |
| `claim_expenses` | 133.93 |
| `commissions` | 37,800.00 |
| `net_cf` | **−41,860.47** |

with `pols_if(12) = 0.909136`, `agg_days_dis(12) = 0.651917`, `agg_days_acc(12) = 0.056688`
and `adv_paid(12) = ¥60.00`. (The totals are sums of unrounded monthly values; the four
displayed monthly rows do not re-add to them, and the year-1 `net_cf` differs by ¥0.01 from
the sum of the rounded line totals.)

**What the numbers say.** Year-1 claims of ¥5,186.09 are **21.5%** of year-1 premium — the
level premium prefunds a morbidity cost that rises steeply with age. On the [std] basis,
annual incidence runs from 0.0466 at age 40 to 0.6452 at 90 and over (a factor of **13.8** —
the 受療率 ratio of 24.3 [REG-R26] damped by the 平均在院日数 ratio 20.2 / 35.5 [REG-R27],
because a longer stay converts the same prevalence into fewer admissions), and expected
paid days per year from 0.709 to 15.16
(a factor of **21.4**, once the 65+ length-of-stay row is applied [REG-R27]). Against that,
the ¥57,800 of acquisition expense and initial commission at `t = 0` produce the
characteristic new-business strain, recovered out of the margin in the early durations. The
per-hospitalization limit is doing real work throughout — it removes 24.75% of raw days at
every age band with the 35–64 row and 33.8% with the 65+ row — while the 通算 limit and the
先進医療 cap, on the expectation, never bind at all.

---

## Valuation and reserve pointers

This library projects gross cash flows. Every valuation layer below consumes them and is
cited, never reproduced.

- **標準責任準備金.** 保険業法 第116条第1項 requires a policy reserve (*sekinin-junbikin*,
  責任準備金) at each 決算期 and 第2項 delegates the accumulation method [REG-R4]; 施行規則 第68条
  fixes scope [R2] [REG-R7]; 平成8年大蔵省告示第48号 sets
  the method as net level premium (*heijun jun-hokenryō-shiki*, **平準純保険料式**), with no
  Zillmer adjustment, on the standard valuation interest rate (*hyōjun riritsu*, 標準利率) and
  the standard table [REG-R10]. For contracts from **1 April 2018** the third-sector
  valuation mortality is **第三分野標準生命表2018** [REG-R11] [R4] [REG-R18]. The 標準利率 in force
  could not be established from a retrieved official document; any value asserted for it is
  [unverified] or must be derived under the 告示 machinery and labelled **[std]** [REG-R10].
- **危険準備金, and the third-sector limb specifically.** 施行規則 第69条第1項 divides the reserve
  into 保険料積立金, 未経過保険料, 払戻積立金 and 危険準備金 [R2] [REG-R8], and **第69条第6項第1号の2 requires
  a separately identified「第三分野保険の保険リスクに備える危険準備金」** [R2]. The 監督指針 requires it be
  computed under the **ストレステスト** of 平成10年6月8日大蔵省告示第231号, with a 負債十分性テスト, both
  reflecting the uncertainty that 保険事故発生率 deteriorates, run per contract grouping sharing
  the same 基礎率, with the calculating unit separated from internal audit [R3] [REG-R13]
  [REG-R14]. **The notification itself was not retrieved and its stress magnitudes are
  [unverified]** [REG-R13]. `jplib` implements the *capability* the regime demands — a
  re-runnable incidence basis, parameterized so a shock can be applied per grouping — and
  **not** the statutory stress. That distinction must not be blurred anywhere downstream.
- **ESR.** From **31 March 2026** insurers are supervised on the economic-value 経済価値ベース
  のソルベンシー規制, liabilities measured as **現在推計 + MOCE** at each 基準日 on assumptions re-set
  then, required capital at **99.5%**, early corrective action below an ESR of **100%**
  [REG-R15]. It supersedes the ソルベンシー・マージン比率 **200%** trigger [REG-R17], and the two are
  not comparable — the 2025 field test showed 生保単体 ESR 215% against SMR 873% [REG-R15].
  `jplib` computes neither. What it owes the regime is exactly what these notes deliver: a
  projection re-runnable on a re-set assumption basis at a stated 基準日.
- **1号収支分析.** The 保険計理人 appointed under 保険業法 第120条 [REG-R5] submits an 意見書 under
  第121条 [REG-R6]; the 実務基準 turns that into a forward income-and-outgo analysis over
  「少なくとも将来10年間」, by 区分経理 segment, with sufficiency judged over the first five years
  [REG-R22]. That is the shape of this projection, and the reason it runs monthly over a
  whole lifetime rather than to a truncated horizon.
- **Three bases, one projection.** J-GAAP statutory reserving [REG-R10], the ESR economic
  balance sheet [REG-R15] and IFRS 17 — **voluntary in Japan, not mandatory** [REG-R47] —
  are three measurement bases fed by one set of projected cash flows. That is why these
  notes keep the cash flows basis-agnostic and undiscounted.
- **Not applicable to this chassis.** 契約者配当 and the surplus-distribution methods of
  施行規則 第30条の2 [REG-R9] do not attach: the main contract is 無配当 [S1] [S6]. 価格変動準備金
  under 第115条 is asset-driven and outside a liability projection entirely [REG-R3].
- **Policyholder tax, not modelled.** The premium falls in the 介護医療保険料 basket of the
  post-2012 生命保険料控除 [R11] [REG-R43]; the anchor's ¥25,200 annual premium sits in the
  second income-tax band for a deduction of about ¥22,600 [R10]. Benefits are not projected
  net of policyholder tax.

---

## Key sensitivities and model risks

In rough order of leverage on a third-sector block:

1. **The morbidity basis is the whole model, and it is [std].** Incidence, stay length and
   surgery frequency are all constructions on public 患者調査 statistics [REG-R26] [REG-R27],
   not an insurer's 危険発生率, which is unpublished by regulation [REG-R2]. The prevalence →
   incidence conversion, the five-band length-of-stay shape and the surgery frequencies are
   three independent [std] levers on the claim cost, and no observed range exists for any of
   them.
2. **The length-of-stay *distribution*, not its mean.** The 60-day limit removes 24.75% of
   raw days on the 35–64 row and 33.8% on the 65+ row; a distribution with the same mean and
   a fatter tail changes the capped expectation without changing the sourced calibration
   target at all. The sourced per-cause spread — 白内障 2.4 days against 精神及び行動の障害 290.4
   [REG-R27] — is the size of the risk being standardized over.
3. **Stay lengths are falling and the data ages fast.** The sourced series runs 40.8 days
   (平成8年) → 32.8 (平成23年) → 32.3 (令和2年, COVID-affected and flagged as such by 厚生労働省) →
   **28.4** (令和5年) [R6] [REG-R27]. A duration basis calibrated on data more than a few years
   old systematically **overstates** a per-day benefit — and the market's answer, the 一時金
   design, does not shrink with it [R6] [S1] [S9] [S10].
4. **Mortality direction.** On a health product death *releases* the liability, so an
   understatement of mortality **overstates** the liability. The valuation table is set
   deliberately low for exactly that reason [R5] [REG-R20]; using it unadjusted as a
   best-estimate decrement is a conservative error in the reserving direction and a
   *material* one over the anchor cell's 77-year projection.
5. **Longevity, not mortality, is the tail risk.** Incidence at 90 and over is 13.8× the
   age-40 rate and paid days 21.4× [REG-R26] [REG-R27], so the liability is concentrated in
   the ages where the survival assumption is least certain and where the projection horizon
   is set by a table's terminal age rather than by a contract term.
6. **The 三大疾病無制限 特則, when switched on.** It does not merely raise the limits: it removes
   がん, 心疾患 and 脳血管疾患 days from the 通算 count entirely [S1] [S2], and lifetime cancer
   incidence in Japan is about 61.1% for men and 50.1% for women [REG-R28]. It is a
   mass-market feature, not a fringe option, and it defers the benefit-driven termination.
7. **Expense inflation on a small premium.** ¥250 a month of maintenance against a ¥2,100
   premium is 11.9% of premium; the level premium is fixed for life and the expense is not.

### Known modeling pitfalls

- **受療率 is a prevalence, not an incidence.** 入院受療率 is a point-in-time count per 100,000
  [REG-R26]. Multiplying it by a daily amount, or treating it as an annual claim frequency,
  is the single commonest error in a Japanese medical model. The conversion needs
  平均在院日数 [REG-R27] and is an explicit **[std]** step.
- **The five-day minimum is an amount, not five days.** `d_ben` gets the floor; `d_pay` and
  therefore the 通算 ledger do not [S4] [S6] [S7]. Crediting the floor to the ledger lets a
  two-day stay consume five days of a lifetime limit it never used.
- **Apply `L1` inside the stay expectation, not to the annual total.**
  `Σ_j pi_j min(g_j, L1) = 15.20`, but `min(Σ_j pi_j g_j, L1) = min(20.20, 60) = 20.20`.
  Capping a mean instead of capping each stay silently removes the limit.
- **The 通算 ledger is per surviving policy, unweighted by `pols_if`.** Weighting it by the
  in-force probability measures the block, not the policyholder, and defers the limit
  forever.
- **Two ledgers, not one.** The 通算 limit runs separately on the 疾病 and 災害 limbs, and
  termination requires **both** to be exhausted [S4] [S1] [S9]. One combined ledger
  terminates the contract roughly twice as early.
- **Do not delete the ledgers because they read zero.** On the anchor cell's expectation
  `LA` never binds and the ¥20,000,000 先進医療 cap is never approached — but
  `E[min(Σ, LA)] ≠ min(E[Σ], LA)`, so the deterministic ledger *understates* the limit, and
  [cancer (がん保険)](../cancer/technical-notes.md) and
  [nursing care (介護保険)](../nursing_care/technical-notes.md) inherit the same code with limits that do
  bind.
- **Radiation is not a separate claim stream.** The composite folds 放射線治療 into 手術給付金
  through the 放射線治療料 limb of the trigger, once per 60 days [S1] [S2] [S6] [S10]. Adding a
  separate 放射線治療給付金 — which one carrier does pay, at 日額 × 10 [S4] — double-counts.
- **Surgery during a limit-exhausted stay is a switch, not a default.** One carrier pays at
  the in-hospital multiple [S4], another pays nothing [S10]; the two differ by 24.75% of the
  in-hospital surgery benefit on the [std] basis. Hard-coding either without the switch
  misstates one design.
- **No surrender value, no APL, no policy loan.** `claims_lapse(t)` is identically zero and
  no mechanism carries a policy through a missed premium [S1] [S6] [S9]. Importing the
  [whole life (終身保険)](../whole_life/technical-notes.md) 自動振替貸付 logic into this chassis
  suppresses lapses that really happen.
- **No death benefit.** Mortality is a pure release [S1] [S4] [S6] [S9] [S10]; a
  `claims_death` column on this model is a benefit that does not exist.
- **第三分野標準生命表2018 excludes 高度障害.** [R5] [REG-R20]. A model that treats 高度障害 as a
  termination or a waiver trigger must add its incidence separately; reading it out of the
  table double-counts nothing and *under*-counts the waiver.
- **The 型 is fixed at issue.** `L1`, `LA` and the 三大疾病無制限 特則 can never be changed after
  issue [S4] [S9] [S2]. Any code path that varies them over `t` models a contract term that
  does not exist.
- **Age basis mismatch.** The contract ages on 満年齢 [S4] [S10]; the standard table is built
  for 保険年齢 [R5] [REG-R20]. Half a year of age sits between the projection basis and the
  valuation basis, and it must be stated, not silently absorbed.
- **The 180-day rule is a grouping rule, not a waiting period.** Two admissions inside 180
  days of the previous discharge are **one** hospitalization against `L1`, with a new spell
  starting on the **181st day** counting the day after discharge as day 1 [S1] [S2]. An
  implementation that resets `L1` on every admission removes the limit for repeat claimants;
  one that treats 180 days as an exclusion pays nothing where the contract pays the balance
  of the limit.
- **Monthly rounding does not re-add.** The displayed monthly rows sum to a year-1 `net_cf`
  one yen away from the total computed on unrounded values; assert against the unrounded
  aggregation.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #jplib-medical-r10
[R11]: #jplib-medical-r11
[R2]: #jplib-medical-r2
[R3]: #jplib-medical-r3
[R4]: #jplib-medical-r4
[R5]: #jplib-medical-r5
[R6]: #jplib-medical-r6
[R7]: #jplib-medical-r7
[R9]: #jplib-medical-r9
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R13]: #jplib-reg-r13
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
[REG-R26]: #jplib-reg-r26
[REG-R27]: #jplib-reg-r27
[REG-R28]: #jplib-reg-r28
[REG-R3]: #jplib-reg-r3
[REG-R31]: #jplib-reg-r31
[REG-R33]: #jplib-reg-r33
[REG-R34]: #jplib-reg-r34
[REG-R36]: #jplib-reg-r36
[REG-R4]: #jplib-reg-r4
[REG-R43]: #jplib-reg-r43
[REG-R47]: #jplib-reg-r47
[REG-R5]: #jplib-reg-r5
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[REG-R9]: #jplib-reg-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
