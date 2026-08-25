# Technical Notes

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** These notes turn the standardized composite of `product-spec.md` (same
directory) into a reference liability cash-flow projection model on paper. They describe no
single insurer's product. [S#] and [R#] tags resolve in `sources.md`, whose numbering is
carried verbatim from `_research/cancer.md` and is frozen; [REG-R#] tags resolve in the
cross-product reference library `references/regulatory-and-actuarial-references.md`, whose
R-numbering is separate. **[std]** marks a standardization introduced for the reference
implementation, always with a rationale and, where one exists, the observed range;
[unverified] marks a claim not confirmed against a retrieved document. **Every parameter
value here is identical to `product-spec.md`'s.** Eleven **assumption inputs** appear here
that `product-spec.md` does not carry, because they are modelling constructs rather than
contractual terms and each is introduced below as such: the **first-diagnosis incidence**
rate, the **上皮内新生物 incidence** increment, the **post-diagnosis survival** basis, the
**relapse hazard** that drives the repeat cycle, the **hospitalisation frequency** and mean
stay for a diagnosed life, the **surgery frequency**, the **qualifying-treatment-month
probability**, the **outpatient-day frequency**, and the 先進医療 frequency and severity.

**Deltas against the medical insurance (*iryō hoken*, 医療保険) chassis.** The
[medical technical notes (医療保険)](../medical/technical-notes.md) are the third-sector
(*dai-san-bun'ya*, 第三分野) chassis in model form and are not restated here. Five
things change, and every one of them changes the *shape* of the model rather than a
parameter in it:

1. **A three-state model, not a one-state model.** `medical` projects a single in-force
   population and reads a hospitalisation incidence off it. A cancer model cannot: the
   diagnosis benefit repeats on a two-year cycle, the inpatient benefit has no day limit,
   and the treatment benefit pays by the month — so all three run on **how long the insured
   lives after diagnosis**. This model therefore carries a never-diagnosed state and a
   diagnosed state, and needs a **survival model as well as an incidence model**.
2. **The 90-day waiting period is a hard zero** in months `t = 0, 1, 2`. No cancer benefit
   of any kind is payable, and the premium is [S1] [S5] [S6] [S7] [S10].
3. **No `L1` and no `LA`.** The per-hospitalization and lifetime aggregate (*tsūsan*, 通算)
   day ledgers that dominate `medical` do not exist here, and neither does the
   benefit-driven termination they create [S1] [S3] [R11]. What replaces them is a
   **60-month ledger on the treatment benefit**, which is a ledger on *months*, not days.
4. Carcinoma in situ (*jōhinai shinseibutsu*, **上皮内新生物**) **is a second benefit tier, not a
   discount** — a separate benefit at 50% of the diagnosis lump sum, payable once, on its
   own cap, not triggering the premium waiver [S6] [S11] [S7] [S10].
5. **The premium waiver is correlated with the insured event**, not independent of it. It
   fires on the same first diagnosis that starts every other benefit [S10] [S11], so the
   premium stream is carried by the **never-diagnosed sub-population alone**.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows for a single-policy model
  point of cancer insurance (*gan hoken*, がん保険): office premiums, cancer diagnosis lump sum
  (*gan shindan ichijikin*, がん診断一時金), the 上皮内新生物 diagnosis benefit, cancer hospitalization
  benefit (*gan nyūin kyūfukin*, がん入院給付金), cancer surgery benefit (*gan shujutsu kyūfukin*,
  がん手術給付金), monthly cancer treatment benefit (*gan chiryō kyūfukin*, がん治療給付金),
  cancer outpatient benefit (*gan tsūin kyūfukin*, がん通院給付金), advanced-medicine benefit
  (*senshin iryō kyūfukin*, 先進医療給付金), maintenance and claim expenses, and commission. The
  intended sense is the current estimate (*genzai suikei*, **現在推計**) the economic-value
  solvency regime requires: probability-weighted future cash flows on assumptions re-set at
  a stated reporting date (*kijunbi*, 基準日) rather than locked in at issue [REG-R15]. It is
  also the shape the 1号収支分析 takes — a forward income-and-outgo projection over at least ten
  future years, by 区分経理 segment [REG-R22].
- **Out of scope, cited not reproduced.** Discounting, MOCE, required capital and every
  reserving basis — standard policy reserve (*hyōjun sekinin-junbikin*, 標準責任準備金), contingency
  reserve (*kiken junbikin*, 危険準備金), the ESR balance sheet and IFRS 17 all consume
  these cash flows and are pointed at in *Valuation and reserve pointers*.
- **Projection frequency.** Monthly grid. Three of the product's mechanics are monthly by
  construction and not by approximation: the 90-day waiting period is three months of the
  grid, the treatment benefit's unit of payment **is** the calendar month [S5] [S10] [S11],
  and the premium mode is monthly (月払) at every carrier in the composite [S1] [S6] [S11]
  [S12]. `t` is the **policy month**, `t = 0, 1, …, proj_len − 1`; month `t` is the interval
  from `t` to `t + 1` months after the contract date (*keiyakubi*, 契約日).
- **The waiting period lands on a grid boundary.** がん責任開始日 is the 91st day counting the
  date cover attaches (*sekinin kaishibi*, 責任開始日) as day 1 [S1] [S5] [S6] [S10] [S13]; two
  carriers instead write three calendar months [S8] [S11]. On a monthly grid these are the
  same boundary, `t = 3` **[std]**, and the model does not claim a precision it does not
  have. A daily implementation must separate them; the two wordings are recorded in
  `product-spec.md` footnote 9.
- **Timing conventions [std].** Office premium received at the **start** of month `t`;
  maintenance expense at the start of month `t`; every benefit and the claim-handling
  expense at the **end** of month `t`; decrements at the end of month `t`, mortality then
  lapse. Acquisition expense and initial commission at `t = 0`.
- **Episode convention [std].** A diagnosis arising in month `t` pays its lump sum in month
  `t`, and the diagnosed life enters the diagnosed state at the **end** of month `t` — so
  the inpatient, surgery, treatment and outpatient benefits that follow the diagnosis begin
  at `t + 1`. Rationale: those four benefits are modelled as **continuing hazards on the
  diagnosed state**, not as a resolved episode, which is exactly what makes them depend on
  post-diagnosis survival. The one-month lag is a timing effect on an undiscounted
  projection; the alternative — recognising a treatment episode in the diagnosis month — is
  named in the pitfalls list.
- **Age basis.** Attained age at the 契約日 with the fraction discarded (*man-nenrei*, 満年齢),
  incremented at each 年単位の契約応当日; 契約年齢 is age last birthday at the 契約日 [S8]. Attained age in
  month `t` is `age(t) = x + floor(t / 12)`, `x` the 契約年齢. 第三分野標準生命表2018 is constructed for
  use on a nearest-birthday age (*hoken-nenrei hōshiki*, 保険年齢方式) basis [R2] [REG-R20], so
  reading it at 満年齢 understates the valuation age by about half a year; the base run accepts
  the offset and marks it **[std]**, with reading at `age(t) + 0.5` as a switch. The
  incidence basis is published by **five-year age band** [R5], so it is read at the band
  containing `age(t)` and steps, not glides.
- **Currency.** JPY throughout. There is no minor unit in the contract, but expected values
  are fractional and are displayed to ¥0.01.
- **Model points.** One policy at a time, projected on an expected (probability-weighted)
  basis. `Projection` is parameterized by `point_id`; no aggregation logic is specified
  here.
- **Termination.** Whole-of-life cover: the projection runs to the terminal age of
  第三分野標準生命表2018, **116 for males and 118 for females** [REG-R18] [REG-R20], so `proj_len =
  12 × (terminal_age − x + 1)` — 924 months for the anchor cell. There is no maturity
  benefit and no 満期保険金. **There is no benefit-driven termination**: payment of the diagnosis
  lump sum neither terminates nor exhausts the contract [S1], and with no day limits the
  inpatient benefit cannot exhaust it either [S1] [S3] [R11]. The decrements are death and
  lapse, and nothing else.
- **Contract boundary.** On the whole-of-life (終身) chassis the premium is level and
  non-participating (*mu-haitō*, 無配当) with no insurer repricing right [S5] [S6] [S11], so all
  future premiums and benefits are inside the boundary and the horizon is the whole of life.
  On the ten-year renewable term (10年更新 定期) model-point flag the renewal reprices, which
  would ordinarily close the boundary at each renewal; `jplib` projects that flag to final
  expiry and records the tension rather than resolving it, exactly as the `medical` chassis
  does.
- **Rounding.** Intermediates at full double precision. Displayed cash flows to ¥0.01,
  `pols_if` and the state split to six decimals, the diagnosed state to eight decimals, and
  the treatment-month ledger to four decimals of a month **[std]**. Monthly rows rounded for
  display do **not** re-add to the displayed annual totals; the totals are sums of unrounded
  values.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | — |
| `chassis` | enum {shushin, teiki} | shushin (終身) |
| `issue_age` (`x`) | int, 満年齢, 20–75 | 40 |
| `sex` | enum {M, F} | M |
| `base_amount` (`A`) | 基本給付金額, JPY, menu {5,000, 10,000} | 10,000 |
| `diag_benefit` (`DB`) | JPY, = 100 × `A` | 1,000,000 |
| `cycle_months` (`C`) | int, repeat cycle | 24 |
| `insitu_pct` | fraction of `DB` for 上皮内新生物 ∈ {1.00, 0.50, 0.10} | 0.50 |
| `daily_amount` (`D`) | がん入院給付金日額, JPY/day, = `A` | 10,000 |
| `surg_mult` (`m_s`) | multiple of `A` per cancer surgery | 20 |
| `treat_benefit` (`B_tr`) | JPY per qualifying month, = 10 × `A` | 100,000 |
| `treat_cap` (`K`) | int months, lifetime cap on the monthly benefit | 60 |
| `outp_daily` | がん通院給付金日額, JPY/day, = `A` | 10,000 |
| `wait_months` (`W`) | int months, 90-day waiting period on the grid | 3 |
| `prem_period` | enum {whole_life, to_65} | whole_life (終身払) |
| `premium` (`P`) | JPY per month, office premium, model-point input | 3,000 **[std]** |
| `prem_mode` | enum {monthly, semiannual, annual} | monthly |
| `waiver_trigger` | enum {cancer_diag, disability, none} | cancer_diag |
| `adv_rider` | bool — がん先進医療特約 (*tokuyaku*, rider) | true |
| `disch_rider` | bool — がん退院一時金 | false |
| `repeat_conditioned` | bool — second and later payments require treatment | false |
| `issue_date` | date | — |

`premium` is an **input, not a computed quantity**, and on this product that is a stronger
statement than on any other in the library. No carrier publishes a rate table for a cancer
main contract; the statement of the method of calculating premiums and reserves (*sanshutsu
hōhō-sho*, 算出方法書) is a 基礎書類 filed with the 金融庁 and is not published [REG-R2]; and for
third-sector business there is additionally **no standard incidence table and no reference
pure premium to fall back on** [R3]. The single retrieved price point is a ten-year term at
twice the composite's benefit amounts on a 2013 calculation basis [S5]. The anchor's ¥3,000
is a round modelling figure in that neighbourhood and no result in this library depends on
its being a market rate.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_healthy(t)` | In force at the start of month `t` and **never diagnosed with an 悪性新生物**; `pols_healthy(0) = 1` | monthly recursion |
| `pols_locked(t)` | In force, diagnosed, **within `C` months of the last payment trigger** | monthly recursion |
| `pols_open(t)` | In force, diagnosed, cycle expired, eligible for a repeat payment | monthly recursion |
| `pols_cancer(t)` | `pols_locked(t) + pols_open(t)` — the diagnosed in-force population | derived |
| `pols_if(t)` | `pols_healthy(t) + pols_cancer(t)` — total in force at the start of `t` | derived |
| `insitu_avail(t)` | Probability, per never-invasively-diagnosed policy, that the once-only 上皮内新生物 benefit is still unused; `insitu_avail(0) = 1` | monthly |
| `treat_months(t)` | Qualifying treatment months already paid, **per diagnosed life**, against the cap `K` | monthly |
| `adv_paid(t)` | 先進医療 技術料 reimbursed, **per diagnosed life**, against the ¥20,000,000 cap | monthly |
| `age(t)` | Attained 満年齢 = `x + floor(t / 12)` | annually |
| `mort_rate_mth(t)` | Monthly best-estimate mortality for a never-diagnosed life | lookup |
| `mort_rate_canc_mth(t)` | Monthly mortality for a diagnosed life = baseline plus excess hazard | derived |
| `lapse_rate_mth(t)` | Monthly lapse, applied after mortality, to never-diagnosed lives only | lookup |
| `inc_rate_mth(t)` | Monthly first-diagnosis incidence per never-diagnosed policy | lookup |
| `net_cf(t)` | Net cash flow of month `t`, insurer perspective, **income-positive** | monthly |

**Why three states and not two.** The two-year cycle is not a cap and not a lockout on a
counter: it is a *clock keyed to an event*, and the event that restarts it is the previous
payment trigger [S5]. A life that has just been paid cannot be paid again for `C` months;
after that it can, on a fresh relapse (再発), metastasis (転移) or new primary, without limit
[S5] [S7] [S10]. `pols_locked` and `pols_open` are exactly that distinction, and the flow
between them is a **24-month delay**, not a rate. This clock is emphatically **not** the
180-day one-hospitalization memory of the `medical` chassis: different length, different
trigger, different consequence. A model that reuses one clock for both is wrong.

**Three absences are product facts, not gaps.** There is **no cash-surrender-value state**:
the composite is 無解約払戻金型 at every duration under 終身払 [S7] [S10] [S11], so `cv_pp` does not
exist and lapse carries no cash flow. There is **no 契約者貸付 / 自動振替貸付** (*jidō furikae
kashitsuke*, automatic premium loan) **state**: with no surrender value there is nothing to
lend against [S1] [S7] [S10] [S11], so a missed premium really does lapse the policy. And
there is **no death benefit** in the composite [S1], so mortality is a pure
liability-releasing decrement and `claims_death` does not exist.

**Both ledgers are per diagnosed life, unweighted by `pols_cancer`.** `treat_months` and
`adv_paid` measure what an individual has consumed, not what the block has. Because
diagnosed lives enter at different times, each ledger is carried as a **cohort average**
that is diluted by new entrants (the recursion is given below); that is a documented
approximation with a stated direction of error, not an accident.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| Waiting period | 90 days; cover from the 91st day, `t = 3` on the grid | [S1] [S5] [S6] [S10] [S13] [R11]; grid **[std]** |
| Diagnosis inside the window | Contract **void**, not merely unpayable; premiums refunded where neither party knew | [S1] [S5] [S10] |
| Reach of the voidness rule | Not applied where no benefit event occurs within 5 years of がん責任開始日 | [S1] |
| がん診断一時金 | 100 × `A` = ¥1,000,000 | [S2] [S3] [S13] |
| Repeat cycle | At most once in any 2 years, **no lifetime cap** | [S5] [S7] [S10] |
| Clock measured from | The **previous payment trigger** date | [S5] |
| Deeming rule | Still an inpatient the day after the cycle expires ⇒ fresh trigger | [S1] |
| 上皮内新生物 diagnosis benefit | 50% of `DB`, payable **once**, own cap, not after a full-rate payment | [S6] [S11] |
| 上皮内新生物 elsewhere | Paid in full on every other benefit; does **not** trigger the waiver | [S7] [S10] |
| がん入院給付金 | `D` × days, **no per-hospitalization and no 通算 day limit** | [S1] [S3] [S5] [S6] [S10] [S13] [R11] |
| がん手術給付金 | 20 × `A` = ¥200,000; unlimited count; simultaneous procedures count as one | [S2] [S6] |
| がん治療給付金 | ¥100,000 per **calendar month** in which a qualifying treatment occurred; several in one month pay once; lifetime cap 60 months | [S5] [S10] [S11] |
| がん通院給付金 | `A` per qualifying attendance day, treatment-linked, **no day limit** | [S1] [S7] |
| Outpatient during a paid stay | Not payable | [S7] [S10] |
| 先進医療 | 技術料 in full, lifetime cap ¥20,000,000, rider terminates on the cap; cash top-up 10% capped ¥500,000 per 療養 | [S1] [S7] [S11] |
| 保険料払込免除 | On first 悪性新生物 diagnosis on or after がん責任開始日; 上皮内新生物 does not trigger it | [S10] [S11] |
| Surrender value | **None** at any duration under 終身払 | [S7] [S10] [S11] |
| Grace, 月払 | To the last day of the month following the 払込期月 | [S1] [S6] [S8] |
| 失効 / 復活 | Lapse from the day after grace; reinstatement within 1 year, **waiting period re-runs from the 復活日** | [S1] [S6] [S8] |
| Termination on payment | **None** — the contract does not end and cannot exhaust | [S1] [S3] [R11] |

### (b) Insurer-discretionary current elements

This class is **nearly empty, and its emptiness is the product fact.** The composite is 無配当
wherever the dividend basis is stated [S5] [S6] [S11]: there is no policyholder dividend
(契約者配当), so the three sources of surplus (*san-rigen*, 三利源) framing and the
surplus-distribution methods of 施行規則 第30条の2 [REG-R9] do not attach. There is no premium
review on the 終身 chassis, no MVA and no non-guaranteed charge scale. What remains:

| Input | Snapshot value | Basis |
|---|---|---|
| Incidence basis (*kiken hasseiritsu*, 危険発生率) | The insurer's own, unpublished, in the 算出方法書 | [REG-R2]; the regulator supplies a **test**, not a table [R3] [R4] [REG-R13] |
| Prospective 支払事由 change | The insurer may vary the treatment-benefit trigger prospectively with 主務官庁 approval and two months' notice if the public fee schedule changes | [S1] [S5]; not modelled **[std scope]** |
| 定期 flag renewal rates | Recomputed at each ten-year renewal at then-current rates | [S5] [S7]; base run holds the issue rate flat **[std]** |
| 給付倍率 election | On one design the diagnosis benefit is 入院給付金日額 × a 倍率 the policyholder picks from an insurer-set range | [S6]; model-point input, not a projected variable |

### (c) Behavioral / experience assumptions (modeler's view)

**Mortality of the never-diagnosed.** 第三分野標準生命表2018 is public, free and machine-readable
[R1] [REG-R18] [REG-R19] — the sharp contrast with `uklib`, which had to proxy
subscriber-only tables. But it is a **valuation** table whose margin runs the wrong way for
a best estimate on a morbidity product: death releases the liability, so the table sits
deliberately below national mortality, its risk-theory adjustment bounded at 70% below and
85% above the unadjusted rate [R2] [REG-R20]. A best-estimate basis scales it **up**:

    mort_rate(age) = mort_be_factor × q_third_sector(age, sex)

with `mort_be_factor` = **1.25 [std]** — the reciprocal of 0.80, a round value inside the
sourced 70–85% band [R2] [REG-R20] (its arithmetic midpoint is 0.775, whose reciprocal is
1.29), so the factor unwinds the table's stated margin and nothing more. This
is the same adjustment the `medical` chassis uses, and the two products must not disagree
about it. `mort_rate_mth(t) = 1 − (1 − mort_rate(age(t)))^(1/12)` **[std]**. The product is
capped at 1, which binds at the terminal age alone, where the table already carries a
sourced `q = 1.00000`.

The IAJ's site terms prohibit reproduction and transmission without written consent
[REG-R21], so `jplib` ships `mort_table.csv` as a **[std]** construction, never as a copy.
The construction is **one table for the whole library**, built on the union of the
individual 第三分野標準生命表2018 rates `jplib`'s products quote and attribute — 22 anchor rows
across the two sexes, 男 q(40) = 0.00076 among them, and the terminal rows
男 q(116) = 1.00000 and 女 q(118) = 1.00000 [REG-R18] [REG-R19] [REG-R20] — **graduated
log-linearly (geometrically)** between adjacent anchors:

    q(x) = q(a) × ( q(b) / q(a) )^((x − a) / (b − a))     for a ≤ x ≤ b, a and b adjacent anchors

Two properties earn the choice. It reproduces **every** quoted rate exactly, so nothing
sourced is disturbed by the graduation; and it is locally the Gompertz family, which is the
family the publisher itself uses at the older ages. Each row's `provenance` column says
whether it is an anchor quoted under attribution or an interpolation between two of them,
and points at [REG-R18] and [REG-R19] either way. The file shipped in this directory is cut
to the ages this model can reach — **male 20–116, female 20–118** — which is the composite's
issue-age range through to each sex's terminal age.

**Incidence — and this is the one assumption in `jplib` that is genuinely sourced.** For
third-sector business the FSA states flatly that no standard incidence rate and no reference
pure premium exist, and that insurers must build the rate for each 支払事由 from public data and
their own experience [R3]. For cancer the public data is excellent. The national cancer
registry (*zenkoku gan tōroku*, 全国がん登録), collected under 「がん登録等の推進に関する法律」, publishes
罹患数 and 罹患率 by **five-year age band, site, sex and diagnosis year**, freely downloadable
[R5] [REG-R29]. Age-specific crude rates per 100,000, both sexes, 2023, all sites C00–C96
[R5]:

| band | 15–19 | 20–24 | 25–29 | 30–34 | 35–39 | 40–44 | 45–49 | 50–54 | 55–59 |
|---|---|---|---|---|---|---|---|---|---|
| rate | 16.51 | 24.38 | 40.14 | 75.77 | 132.21 | **220.28** | 340.48 | 453.38 | 641.76 |

| band | 60–64 | 65–69 | 70–74 | 75–79 | 80–84 | 85–89 | 90–94 | 95–99 | 100+ |
|---|---|---|---|---|---|---|---|---|---|
| rate | 959.00 | 1,406.59 | 1,948.71 | 2,306.96 | 2,459.27 | 2,497.39 | 2,360.63 | 2,275.13 | 1,889.77 |

**A unisex basis is materially wrong at every age**, because the male and female curves
cross: at 35–39 female incidence is 193.89 against male 72.92, and at 70–74 male 2,684.60
against female 1,291.07 [R5]. The published age-banded rates above are both sexes combined,
and the by-sex age-band grid was not extracted band by band, so the sex split is a **[std]**
construction anchored on those two sourced pairs:

    f_male(a) = linear interpolation in a of  male / both-sexes rate,
                from 0.551547 at band midpoint 37.5   (72.92 / 132.21)
                to   1.377629 at band midpoint 72.5   (2,684.60 / 1,948.71)   [R5]

    mid(age)         = band(age) + 2.5      the midpoint of the five-year band   [std]
    inc_rate(age, M) = inc_both(band(age)) × f_male(mid(age))
    inc_rate(age, F) = inc_both(band(age)) × (2 − f_male(mid(age)))     [std]

`f_male` is read at the **band midpoint**, not at the attained age **[std]**: the band rate
it scales is itself a band figure, so scaling it by a factor that glides inside the band
would give the annual rate a slope the registry does not publish. Reading at the midpoint
keeps the whole annual rate a step function, which is the pitfall below.

`f_male` is clamped to `[0, 2]` **[std]**, and the clamp is not decoration. Outside
that interval one limb of the construction goes negative, and a negative incidence is
not a rate: the linear form reaches 2 at age 98.87, so at the 100+ band midpoint of
102.5 it gives a female factor of −0.085699 and a female rate of −162.0 per 100,000 —
on a projection that runs to attained age 118 for a female life. The admissible domain
of a construction whose two limbs must sum to twice the band rate and must both be
non-negative is exactly `f_male` between 0 and 2, and the clamp binds on the 100+ band
alone.

Two properties of the construction are validation targets rather than claims. `f_male = 1`
at age **56.5**, against a sourced crossover somewhere between about 25 and about 55 [R5].
And the female limb does **not** reproduce the sourced female rates exactly: it gives 191.5
at 35–39 against 193.89 (−1.2%) and 1,212.8 at 70–74 against 1,291.07 (−6.1%) [R5], because
`inc_both` is a population-weighted average rather than the arithmetic mean the `2 − f_male`
form assumes. The error is small at the anchor age and material in the tail; it disappears
the moment the by-sex grid replaces the construction. At the anchor cell,
`f_male(42.5) = 0.669559` and
`inc_rate(40, M) = 220.28 × 0.669559 = 147.49` per 100,000 = **0.00147490** per year.
`inc_rate_mth(t) = inc_rate(age(t), sex) / 12` **[std]** (uniform within the band year). Any
user should replace the whole construction with the by-sex grid from the same workbook —
that is what the `provenance` column is for, and the attribution string the dataset requires
must travel with it [R5] [REG-R29].

**上皮内新生物 incidence.** The registry publishes paired rows with and without 上皮内がん: 全部位 C00–C96
at 993,469 against 全部位（上皮内がん含む）C00–C96 D00–D09 at 1,114,642, an increment of **121,173**
cases, **12.2%** of the invasive count [R5]. The model takes

    insitu_rate(age, sex) = 0.122 × inc_rate(age, sex)          [std age-invariance]

The 12.2% is sourced; its **age-invariance is [std]** and is very likely wrong in a knowable
direction (in-situ detection is screening-driven and concentrated at the screened ages), but
the age-banded breakdown on the in-situ-inclusive basis was not confirmed cell by cell [R5].

**Post-diagnosis survival — the assumption a cancer model has that a medical model does
not.** 全国がん登録 publishes five-year relative survival (5年相対生存率) by site, sex and 臨床進行度: for
2018 diagnoses, all sites, **63.17% male** and **66.84% female** [R6] [REG-R28]. Relative
survival already nets out background mortality, so it converts directly into an **excess
hazard** without double-counting:

    mu_ex(sex) = −ln(S5(sex)) / 5                                       [std, flat]
    mort_rate_canc_mth(t) = 1 − (1 − mort_rate_mth(t)) × exp(−mu_ex / 12)

Male: `mu_ex = −ln(0.6317)/5 = 0.0918681` per year. Two honest statements come with it.
First, **the hazard is held flat for the whole diagnosed lifetime [std]**, which overstates
late-duration mortality — real relative-survival curves flatten as the cured fraction
emerges — and therefore **understates** the repeating diagnosis benefit and the unlimited
inpatient benefit, which are precisely the long-survivor benefits. A duration-banded excess
hazard is a switch, and it needs cohort tracking the base run does not carry. Second, the
never-diagnosed keep the **population** table rate, which already contains cancer deaths, so
the aggregate double-counts cancer mortality inside the table's own rates; at the anchor age
the table rate 0.00095 is 1% of the excess hazard and the effect is second-order, but it
grows with age and a `net_of_cancer` baseline is a switch. Neither point can be resolved
from a source: [R6] is a *relative* survival table, not a cohort mortality table, and any
post-diagnosis survival model built on it is a **[std]** construction [R6].

**The relapse hazard — the largest single [std] lever in the product.** Once a diagnosed
life's cycle has expired it becomes eligible again on a fresh 再発／転移／新生 [S5], and the
composite does not condition the payment on being under treatment (`repeat_conditioned` is a
switch, because two of the three sourced two-year designs do condition it [S7] [S10]). No
public source gives a relapse rate. The model takes

    rel_rate = 0.06 per year   ⇒  rel_rate_mth = 0.005          [std]

with the deeming rule (a continuing hospitalisation at cycle expiry is a fresh trigger [S1])
folded into it. The calibration target is stated so it can be argued with: at the anchor
cell's decrement rates held flat, a diagnosed life survives the 24-month lock with
probability `(1 − 0.0077050)^24 = 0.830575`, then wins the race between relapse and exit
with probability `0.005 / (0.005 + 0.0077050) = 0.393544`, giving `p = 0.326868` per cycle
and an expected `p / (1 − p)` = **0.485593 repeat payments**, i.e. **1.485593 diagnosis
payments per diagnosed life**. Read the two numbers apart: `p` = **32.7%** of diagnosed lives
collect at least a second lump sum and `p²` = **10.7%** at least a third, and it is the
lives collecting three and more that lift the expected *count* to 0.4856. A third of
diagnosed lives paid twice is the design intent of a repeating benefit with no lifetime cap.
There is no observed range.

**Hospitalisation of a diagnosed life.** The mean stay is sourced: 退院患者平均在院日数 for 悪性新生物
discharges in September 2023 was **14.4 days**, against 28.4 days for all conditions, with a
mild age gradient (35–64: 10.7; 65+: 15.5; 75+: 17.6) [R7] [REG-R27]. The base run uses the
all-ages 14.4 and carries the age gradient as a switch **[std]**, because the gradient is
published on four broad bands and the incidence on twenty-one narrow ones. The *frequency*
is derived from two sourced counts, and the derivation needs no population figure at all
because the population cancels:

    admissions per diagnosed person (lifetime)
        = ( 推計入院患者数(悪性新生物) × 365 / 平均在院日数 ) / 罹患数
        = ( 106,100 × 365 / 14.4 ) / 993,469
        = 2.707020                                    [R7] [R5]; stationarity [std]

— 2,689,340 cancer admissions a year against 993,469 new diagnoses a year. At 14.4 days each
that is **38.98 inpatient days per diagnosed person over a cancer lifetime**, which is the
single most useful number in this file for sanity-checking an implementation. Spreading it
over the diagnosed state at a constant hazard, and using the mean diagnosed-state duration
`1 / mort_rate_canc_mth = 129.79 months = 10.815 years` implied by the survival basis above:

    hosp_rate = 2.707020 / 10.815 = 0.250293  →  0.25 admissions per diagnosed
                life-year                                              [std]

The rounding is to two decimals and the derivation is the rationale. Note what the constant
hazard does and does not claim: it makes the inpatient benefit **proportional to survival**,
which is the product's actual economics under an unlimited-day design, and it does *not*
front-load admissions onto the diagnosis month, which real cancer treatment does. The
front-loaded alternative is a switch and is named in the pitfalls list.

**Surgery.** `surg_per_hosp` = **0.35 [std]** payable cancer surgeries per cancer admission,
carried over unchanged from the `medical` chassis so the two products do not disagree about
the same statistic; 患者調査 crosses 退院患者数 with 手術の有無 but those e-Stat tables were not
downloaded for this product [R7] [REG-R33]. The implied lifetime figure is `0.35 × 2.707 =
0.947` payable surgeries per diagnosed person — about one — which is the sanity check. For
上皮内新生物 the composite pays the surgery benefit in full [S7], and in-situ disease is by
definition managed by local excision, so `surg_per_insitu` = **0.80 [std]** surgeries
recognised in the in-situ diagnosis month.

**上皮内新生物 generates no continuing exposure [std].** The composite gives an in-situ diagnosis
the reduced lump sum and the surgery benefit and **nothing else**: no inpatient, no
treatment months, no outpatient days, and no state change. The rationale is a data fact
rather than a convenience: the sourced 推計患者数 and 平均在院日数 figures are for **悪性新生物** and do not
measure in-situ exposure [R7], so attaching the invasive frequencies to in-situ lives would
credit them with an exposure no retrieved statistic observes. The direction of the error is
stated: it understates the in-situ tier.

**Qualifying treatment months.** `treat_prob` = **0.10 [std]** — the probability that a
diagnosed life has at least one qualifying chemotherapy, hormone-therapy or radiotherapy
month in a given month, i.e. 1.2 qualifying months per diagnosed life-year. No public source
gives it, and there is no observed range. The only calibration anchor is the cap itself: at
0.10 and the diagnosed-state duration above, a life diagnosed at the anchor age accumulates
an expected `0.10 × 129.79 = 12.98` qualifying months against the **60-month** cap two
carriers write [S5] [S11], so the cap binds for a long-course minority — which is what a
60-month cap is for. The benefit is an **indicator per month**, not a count and not a
duration: a prescription covering two months pays one month and two triggers in one month
pay once [S10] [S11].

**Outpatient days.** `outp_days` = **1.10 [std]** qualifying attendance days per diagnosed
life-year, derived on the same population-cancelling trick as the admissions rate: 推計外来患者数
for 悪性新生物 was **186,400** on the survey day [R7]; at **250 [std]** outpatient operating days
a year that is 46,600,000 cancer outpatient visits, or `46,600,000 / 993,469 = 46.91` visits
per diagnosed person over a cancer lifetime. The composite's benefit is **treatment-linked**
— attendance *for* surgery, radiation, thermal therapy or non-oral chemotherapy [S1] [S7] —
not attendance for follow-up, so a **25% [std]** qualifying share gives 11.73 days, and
`11.73 / 10.815 = 1.084` per diagnosed life-year, taken as 1.10. Both the 250 and the 25%
are unsourced; between them they are a factor-of-four uncertainty on this benefit.

**先進医療 [std].** `adv_freq` = **0.012 療養 per diagnosed life-year** and `adv_sev` = **¥600,000
per 療養**, both **[std]** with no observed range. The `medical` chassis carries the sourced
先進医療 cost anchors (see the [medical technical notes (医療保険)](../medical/technical-notes.md));
this product's own source set does
not, so neither figure can be tagged here. The severity is set well above the `medical`
chassis's population-wide figure because a cancer-only trigger selects for particle-beam
therapy, which is the expensive end of the 先進医療 list; the direction is defensible and the
level is not sourced.

**Lapse [std].** The only published industry-wide persistency figure in Japan is 解約・失効率 5.6%
p.a. on 個人保険, measured on **opening in-force sum assured** [REG-R31] — a
sum-assured-weighted rate on a book dominated by death cover, which a がん保険 with no sum
assured cannot even enter, and no cancer-specific persistency source was retrieved. The
table is the `medical` chassis's, unchanged, so the two third-sector products share a
persistency basis:

| Policy year | 1 | 2 | 3 | 4 | 5 | 6–20 | 21+ |
|---|---|---|---|---|---|---|---|
| `lapse_rate` **[std]** | 9.0% | 7.0% | 6.0% | 5.5% | 5.0% | 4.5% | 3.0% |

`lapse_rate_mth(t) = 1 − (1 − lapse_rate(year(t)))^(1/12)` **[std]**. The first ten years
average 5.5%, at the sourced 5.6% [REG-R31].

**Lapse applies to the never-diagnosed only [std].** This is a product fact, not a
refinement. The waiver fires on the first 悪性新生物 diagnosis [S10] [S11], a diagnosed life
therefore has no premium to miss, and there is no surrender value to cash in [S7] [S10]
[S11] — so there is no mechanism by which a diagnosed policy leaves the book other than
death. `lapse_rate_canc_mth = 0` in the base run, with a non-zero value as a switch for the
disability-trigger and no-waiver designs [S1] [S5] [S6] [S7].

**Expenses and commission (all levels [std]; no Japanese cancer expense or commission scale
is public).** Carried from the `medical` chassis, scaled to this product's premium.

| Input | Value | Basis |
|---|---|---|
| Acquisition expense | ¥20,000 per policy at `t = 0` | **[std]** |
| Initial commission | 1.5 × annualized premium at `t = 0` (¥54,000 on the anchor) | **[std]** |
| Renewal commission | 3.0% of premiums from policy year 2 | **[std]** |
| Maintenance expense | ¥250 per policy per month, inflating 1.0% p.a. at each anniversary | **[std]** |
| Claim expense, diagnosis | ¥5,000 per diagnosis trigger (invasive or in-situ) | **[std]** |
| Claim expense, hospitalisation | ¥3,000 per cancer admission | **[std]** |
| Expense inflation | 1.0% p.a. flat | **[std]** |

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning |
|---|---|
| `t` | policy month, `t = 0, 1, …, proj_len − 1` |
| `x`, `age(t)` | 契約年齢 (満年齢); attained age `x + floor(t/12)` |
| `y(t)` | policy year, `floor(t/12) + 1` |
| `W` | waiting period in months (3); `cover(t) = 1{t ≥ W}` |
| `A`, `DB` | 基本給付金額 (10,000); diagnosis lump sum `100 × A` |
| `D`, `m_s` | がん入院給付金日額 (`= A`); surgery multiple of `A` (20) |
| `B_tr`, `K` | monthly treatment benefit (`10 × A`); lifetime cap in months (60) |
| `C` | repeat cycle in months (24) |
| `u` | 上皮内新生物 grading of the diagnosis benefit (0.50) |
| `i(t)` | monthly first-diagnosis incidence, `inc_rate(age(t), sex) / 12` |
| `iz(t)` | monthly 上皮内新生物 incidence, `0.122 × i(t)` |
| `r` | monthly relapse hazard once the cycle is open (0.005) |
| `q(t)`, `q_c(t)` | monthly mortality, never-diagnosed / diagnosed |
| `w(t)`, `w_c(t)` | monthly lapse, never-diagnosed / diagnosed (`w_c = 0`) |
| `mu_ex` | annual excess hazard from 5年相対生存率 |
| `h` | monthly cancer admissions per diagnosed life (`0.25 / 12`) |
| `L` | mean cancer stay in days (14.4) |
| `s_h`, `s_z` | surgeries per admission (0.35); per in-situ diagnosis (0.80) |
| `p_tr` | probability of a qualifying treatment month (0.10) |
| `o` | monthly qualifying outpatient days per diagnosed life (`1.10 / 12`) |
| `f_a`, `S_a`, `LV` | 先進医療 monthly frequency, mean 技術料, lifetime cap (¥20,000,000) |
| `M(t)`, `V(t)` | treatment-month ledger; 先進医療 ledger, both per diagnosed life |
| `Z(t)` | `insitu_avail(t)` |
| `P`, `e(t)` | monthly office premium; monthly maintenance expense |
| `ec_d`, `ec_h` | claim expense per diagnosis trigger; per admission |

**Dimensional check.** `i`, `iz`, `r`, `q`, `q_c`, `w`, `h`, `p_tr` and `f_a` are
dimensionless probabilities *per month*; `mu_ex` is a hazard *per year* and appears only as
`exp(−mu_ex/12)`. `L` and `o` are **days**, `M` and `K` are **months**, `s_h` is surgeries
per admission and `s_z` surgeries per in-situ diagnosis. `D` is JPY/day, so `D × L` is JPY
per admission and `D × L × h × pols_cancer(t)` is JPY per policy-month. `B_tr` is JPY per
month, so `B_tr × p_tr` is JPY per policy-month directly — **no day count enters the
treatment benefit at all**, and inserting one is the commonest way to break this product.
`DB`, `S_a`, `V`, `LV`, `P`, `e`, `ec_d` and `ec_h` are JPY. Every `net_cf` term is JPY per
month. The error this check catches: `medical`'s benefit is `日額 × days` and this product's
central benefit is `月額 × months`; the two have different dimensions and cannot share a
formula.

### The waiting period

    cover(t) = 1 if t ≥ W = 3, else 0

and `cover(t)` multiplies **every** cancer benefit, the incidence transition and the in-situ
transition. In months 0, 1 and 2 the model pays nothing, transitions nobody, and collects
the premium [S1] [S5] [S6] [S7] [S10]. It is a **hard zero**, not a reduced rate.

The invalidity rule is not modelled in the base run and the omission is quantified rather
than waved at. A diagnosis inside the window makes the contract **void** [S1] [S5] [S10] — a
**de-recognition, not a decrement**: the policy was never in force, so it releases the
premium already collected as well as the future benefit, and it belongs in a validity
adjustment at outset, not in the lapse column. At the anchor cell the probability is `1 − (1
− 0.000122909)^3 = 0.000368681`, 0.037% of policies against at most three months of premium,
and the composite additionally does not apply the treatment at all where no benefit event
occurs within five years of the がん責任開始日 [S1]. The `void_adjust` switch implements the
de-recognition; the base run leaves it off and says so.

On 復活 the waiting period **re-runs from the 復活日** [S1] [S6], so a reinstated policy is a
different model point with `W` measured from a new date — which is why reinstatement is
modelled as a new model point rather than as a negative lapse.

### The diagnosis benefit and the two-year cycle

    diag_first(t) = pols_healthy(t) × i(t) × cover(t)
    diag_rep(t)   = pols_open(t)    × r    × cover(t)
    trig(t)       = diag_first(t) + diag_rep(t)
    claims_diag(t) = DB × trig(t)

with no limit on the number of payments [S5] [S7] [S10] and no termination on payment [S1].
The cycle is a **delay**, and the delay is implemented on the trigger history rather than as
a rate:

    unlock(t) = trig(t − C) × Π_{v = t−C}^{t−1} (1 − q_c(v)) (1 − w_c(v)),   t ≥ C
              = 0                                                            otherwise

    sc(t) = (1 − q_c(t)) × (1 − w_c(t))

    pols_locked(t+1) = ( pols_locked(t) + trig(t) )     × sc(t) − unlock(t+1)
    pols_open(t+1)   = ( pols_open(t) − diag_rep(t) )   × sc(t) + unlock(t+1)

Read the two lines together: a life triggered in month `t` — first diagnosis or repeat —
enters `locked`, survives `C` months of diagnosed decrements, and arrives in `open` in month
`t + C`. With `repeat_conditioned = true` the second and later payments additionally require
the insured to be in treatment [S7] or hospitalised [S10]; the switch multiplies `r` by the
conditional probability of being in treatment, which on the [std] basis is `p_tr` — and the
two designs therefore differ by an order of magnitude, not by a rounding.

### The 上皮内新生物 tier

    insitu_ev(t)    = pols_healthy(t) × Z(t) × iz(t) × cover(t)
    claims_insitu(t) = u × DB × insitu_ev(t)
    Z(t+1)           = Z(t) × ( 1 − iz(t) × cover(t) )

The benefit is payable **once** over the policy term, on its own cap, and is not payable
once a full-rate benefit has been paid [S6] [S11] — which is why it attaches to
`pols_healthy` alone and why `Z` is a separate ledger rather than a flag on the diagnosis
benefit. It does **not** move the life out of `pols_healthy`, does **not** start the
two-year cycle, and does **not** trigger the premium waiver [S7] [S10]. It is a second tier
of benefit at a second rate, and the three sourced treatments of in-situ — full rate [S1]
[S5] [S10] [S13], half rate [S6] [S11], 10% [S7] — are a single model-point parameter
`insitu_pct`.

### The care benefits, all on the diagnosed state

    claims_hosp(t)      = D × L × h × pols_cancer(t)
    claims_surgery(t)   = m_s × A × ( s_h × h × pols_cancer(t) + s_z × insitu_ev(t) )
    paid_months(t)      = min( p_tr, max(0, K − M(t)) )
    claims_treat(t)     = B_tr × paid_months(t) × pols_cancer(t)
    claims_outpatient(t)= A × o × pols_cancer(t)
    pay(t)              = min( S_a, LV − V(t) )
    claims_advanced(t)  = f_a × ( pay(t) + min(0.10 × pay(t), 500,000) ) × pols_cancer(t)

At the anchor cell's parameters each is a fixed yen amount per diagnosed life-month, and the
five numbers are worth memorising as an implementation check: **¥3,000.00** inpatient,
**¥1,458.33** surgery, **¥10,000.00** treatment, **¥916.67** outpatient and **¥660.00**
advanced medicine — **¥16,035.00** per diagnosed life-month in total.

The two ledgers are cohort averages over the diagnosed population, diluted by new entrants:

    M(t+1) = ( M(t) + paid_months(t) ) × pols_cancer(t) / ( pols_cancer(t) + diag_first(t) )
    V(t+1) = ( V(t) + f_a × pay(t) )   × pols_cancer(t) / ( pols_cancer(t) + diag_first(t) )

with `M = V = 0` while `pols_cancer = 0`. Only `diag_first` dilutes: a repeat trigger is an
already-diagnosed life whose ledgers continue. The direction of the approximation is the
same one the `medical` chassis records for its day ledger — `E[min(Σ, K)] ≠ min(E[Σ], K)`,
so a deterministic average **understates** the cap's bite. Here the understatement matters
more than it does on `medical`, because the 60-month cap is reached by a real minority
(12.98 expected months against 60) rather than never.

### Processing order

For `t = 0, 1, …, proj_len − 1`:

1. **Start of month.** `premiums(t) = P × pols_healthy(t)` — **the never-diagnosed
   sub-population only**, because the waiver fires on the first invasive diagnosis [S10]
   [S11]; maintenance `e(t) × pols_if(t)` with `e(t) = 250 × 1.01^floor(t/12)`; renewal
   commission `0.03 × premiums(t)` for `t ≥ 12`. At `t = 0` additionally the acquisition
   expense ¥20,000 and the initial commission `1.5 × 12P`.
2. **Look up the age basis.** `age(t)`, hence `mort_rate(age(t))` and the five-year
   incidence band, hence `i(t)`, `iz(t)`, `q(t)` and `q_c(t)`.
3. **Apply `cover(t)`.** Below `W` every cancer term is zero, so step 4 produces nothing at
   all and step 5 applies the two decrements to a population that is entirely healthy.
4. **End of month — triggers and claims.** `diag_first(t)`, `diag_rep(t)`, `insitu_ev(t)`,
   then the seven claim lines above and the claim-handling expense `ec_d × (trig(t) +
   insitu_ev(t)) + ec_h × h × pols_cancer(t)`.
5. **End of month — decrements**, mortality **then** lapse **[std order]**, on the two
   populations separately, with no benefit-driven termination:

       pols_healthy(t+1) = ( pols_healthy(t) − diag_first(t) ) × (1 − q(t)) × (1 − w(t))
       pols_locked(t+1), pols_open(t+1)  per the cycle recursion above

   A life diagnosed in month `t` leaves `pols_healthy` before the decrement and takes the
   **diagnosed** mortality in its month of diagnosis **[std]**. Lapse pays nothing — there
   is no surrender value [S7] [S10] [S11] — so `claims_lapse(t)` is identically zero, and
   that zero is a product fact worth publishing.
6. **Ledger update.** `Z(t+1)`, `M(t+1)`, `V(t+1)` per the recursions above.

### Net cash flow

    net_cf(t) = premiums(t)
              − claims_diag(t) − claims_insitu(t) − claims_hosp(t)
              − claims_surgery(t) − claims_treat(t) − claims_outpatient(t)
              − claims_advanced(t)
              − expenses(t) − claim_expenses(t) − commissions(t)

with

    expenses(t)       = e(t) × pols_if(t) + 20,000 × 1{t = 0}
    claim_expenses(t) = ec_d × ( trig(t) + insitu_ev(t) ) + ec_h × h × pols_cancer(t)
    commissions(t)    = 1.5 × 12P × 1{t = 0} + 0.03 × premiums(t) × 1{t ≥ 12}

`expenses` is **acquisition and maintenance only** and the claim-handling cost is a line of
its own, deducted explicitly here and published as its own `claim_expenses` column. The
split is library-wide, and on this product it earns itself: the first rides on `pols_if`,
which a waiver does not reduce, and the second on the diagnosis and admission counts, which
are the diagnosed state.

`net_cf` is **income-positive** in the shipped model, per the library convention. Note the
asymmetry that defines the product's cash-flow signature: **premiums are weighted by
`pols_healthy` and claims by `pols_cancer`**, and the two are disjoint. Weighting premium by
`pols_if` overstates income by exactly the waived population.

---

## Policyholder behavior modeling

- **Lapse is real and immediate — for the never-diagnosed.** On a product with a surrender
  value (*kaiyaku-henreikin*, 解約返戻金) the insurer would advance an unpaid
  premium under 自動振替貸付, which [REG-R14] requires be at the policyholder's election
  with prompt notice; the composite has no surrender value, so
  neither 契約者貸付 nor 自動振替貸付 can operate [S1] [S7] [S10] [S11]. On the one retrieved cancer
  contract that does carry a value, the APL runs at **≤ 8% p.a.** compounded until principal
  plus interest would exceed the surrender value [S6], and a model that lapses that contract
  on a missed premium is wrong; that is a switch, not the base.
- **Grace [std scope].** Grace runs to the last day of the month following the 払込期月 [S1]
  [S6] [S8]; two months at one carrier [S11]. The base run applies lapse at the end of the
  month in which the premium is missed and does not model the one-month lag, nor the
  grace-window rule under which a claim is paid net of the arrears and two months' premium
  is deducted where the event falls on or after the anniversary inside the window [S1] [S6].
- **Reinstatement (復活) — and on this product it is not a persistency detail.** Available
  within one year at the composite [S1] [S8]; three years at one carrier [S6]; **not at
  all** at another [S11]. What makes it structural here is that the **90-day waiting period
  re-runs from the 復活日** [S1] [S6]: a reinstated cancer policy is a policy with 90 days of
  no cover in front of it, which is a genuine anti-selection control. It therefore enters
  the model as a **new model point**, not as a negative lapse, and the base run treats lapse
  as absorbing. One carrier additionally refuses reinstatement outright once any cancer
  benefit has been paid [S1] — a control conditional on the claim history the model is
  already carrying.
- **Anti-selective lapse [std] (optional module, off in the base run).** Healthy lives lapse
  first, so the persisting never-diagnosed block is progressively impaired on the
  *incidence* basis:

      inc_eff(t) = inc_rate(age(t), sex) × [ 1 + lam × max(0, w_cum(t) − w_ref) ]

  with `w_cum(t)` the cumulative lapse proportion among the never-diagnosed, `w_ref` = 0.20
  and `lam` = 0.30 **[std]**. Base run `lam` = 0. No Japanese evidence was retrieved. On
  this product the effect is amplified by the waiver: the healthiest lives are also the only
  ones still paying.
- **No dynamic lapse from surrender value or interest.** With no cash value, no assumed
  interest rate (*yotei riritsu*, 予定利率) disclosure on this chassis and no MVA, there is
  no economic surrender trigger. The 低解約返戻金型 cliff that drives the `whole_life` surrender
  spike has no analogue here.
- **Elections are not behaviour.** `base_amount`, `insitu_pct`, `treat_cap` and the rider
  set are fixed at issue; benefit reduction (減額) is available on request with fresh
  underwriting for any increase [S1] [S6] [S12] and is not projected. A model that lets them
  move over `t` is modelling a contract term that does not exist.
- **クーリング・オフ.** Out of scope: a pre-inception decrement, eight days from dispatch under 保険業法
  第309条 [REG-R36] and contracted to fifteen at one carrier [S1]. Modelling it would need a
  new-business funnel this library does not have.

---

## Worked example

**Anchor cell (`point_id = 1`).** Male, 契約年齢 40 (満年齢), 終身 chassis, 終身払, 基本給付金額 `A` =
¥10,000; がん診断一時金 `DB` = ¥1,000,000 on a `C` = 24-month cycle with no lifetime cap; 上皮内新生物 at
50% of `DB`, once; がん入院給付金日額 `D` = ¥10,000 with **no day limit**; がん手術給付金 20 × `A` =
¥200,000; がん治療給付金 ¥100,000 per qualifying month capped at `K` = 60 months; がん通院給付金日額
¥10,000; 先進医療特約 attached; premium waiver on first 悪性新生物 diagnosis; がん退院一時金 **off**;
`repeat_conditioned` **false**; `void_adjust` **off**; office premium `P` = ¥3,000 per
month; `W` = 3 months.

Assumption values used, every one of them:

- **Incidence.** 罹患率 at 40–44, both sexes, all sites, 2023 = **220.28** per 100,000 [R5];
  [std] male factor `f_male(42.5) = 0.551547 + (1.377629 − 0.551547) × 5 / 35 = 0.669559`
  from the two sourced pairs [R5]; so `inc_rate(40, M) = 0.00147490` per year and `i =
  0.000122909` per month.
- **上皮内新生物.** `iz = 0.122 × i = 0.0000149949` per month, from the sourced 121,173 / 993,469
  = 12.2% increment [R5]; age-invariance **[std]**.
- **Mortality, never-diagnosed.** 第三分野標準生命表2018 男 q(40) = **0.00076** [R1] [REG-R18] —
  quoted here because a worked example needs it and `jplib` quotes only the rates it uses
  [REG-R21]. It is an **anchor** of the shipped construction, reproduced exactly, so the
  worked example reads a sourced rate and not an interpolation. Best estimate
  `mort_rate(40) = 1.25 × 0.00076 = 0.00095` **[std]**; `q = 1 − (1 − 0.00095)^(1/12) =
  0.0000792012`.
- **Mortality, diagnosed.** 5年相対生存率, male, all sites, 2018 diagnoses = **0.6317** [R6]
  [REG-R28]; `mu_ex = −ln(0.6317)/5 = 0.0918681` p.a. **[std flat]**; `q_c = 1 − (1 −
  0.0000792012) × exp(−0.0918681/12) = 0.0077050451`.
- **Lapse.** Policy year 1, `lapse_rate` = 9.0% **[std]**; `w = 1 − (1 − 0.09)^(1/12) =
  0.0078284203`. `w_c = 0` **[std]** — a waived life cannot lapse.
- **Relapse.** `r = 0.06 / 12 = 0.005` per month **[std]**. Zero in every row below: the
  first `unlock` cannot occur before `t = C + W = 27`.
- **Cancer care per diagnosed life-month.** `h = 0.25/12 = 0.0208333` admissions **[std]**,
  `L = 14.4` days [R7] [REG-R27], `s_h = 0.35` **[std]**, `p_tr = 0.10` **[std]**, `o =
  1.10/12 = 0.0916667` days **[std]**, `f_a = 0.012/12 = 0.001` **[std]** at `S_a` =
  ¥600,000 **[std]**. Hence ¥3,000.00 + ¥1,458.33 + ¥10,000.00 + ¥916.67 + ¥660.00 =
  **¥16,035.00** of benefit per diagnosed life-month.
- **In-situ surgery.** `s_z = 0.80` **[std]**, so an in-situ diagnosis pays `0.80 × 200,000
  = ¥160,000` of surgery benefit per event alongside the ¥500,000 lump sum.
- **Expenses.** `e(t)` = ¥250 (policy year 1) and acquisition ¥20,000 — together the
  `expenses` line; `ec_d` = ¥5,000 and `ec_h` = ¥3,000 — together the `claim_expenses` line;
  initial commission `1.5 × 12 × 3,000 = ¥54,000`; renewal commission 3% from `t = 12`, so
  zero in every row below **[std]**.

Every decrement rate above is either quoted from 第三分野標準生命表2018 [R1] [REG-R18], from 全国がん登録
[R5] [R6] [REG-R28] [REG-R29] or from 患者調査 [R7] [REG-R27] with its citation, or is marked
**[std]** as an illustrative value in the shape of such a table. None of them is an
insurer's basis, and none could be: the 算出方法書 is not published [REG-R2] and there is no
standard third-sector incidence table to substitute for it [R3].

**In-force and non-claim lines.**

| t | `pols_if` | `pols_healthy` | `pols_cancer` | `premiums` | `expenses` | `claim_expenses` | `commissions` |
|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 1.000000 | 0.00000000 | 3,000.00 | 20,250.00 | 0.0000 | 54,000.00 |
| 1 | 0.992093 | 0.992093 | 0.00000000 | 2,976.28 | 248.02 | 0.0000 | 0.00 |
| 2 | 0.984249 | 0.984249 | 0.00000000 | 2,952.75 | 246.06 | 0.0000 | 0.00 |
| 3 | 0.976466 | 0.976466 | 0.00000000 | 2,929.40 | 244.12 | 0.6733 | 0.00 |
| 4 | 0.968745 | 0.968626 | 0.00011909 | 2,905.88 | 242.19 | 0.6753 | 0.00 |
| 5 | 0.961085 | 0.960849 | 0.00023631 | 2,882.55 | 240.27 | 0.6773 | 0.00 |

**Claim lines.**

| t | `claims_diag` | `claims_insitu` | `claims_hosp` | `claims_surgery` | `claims_treat` | `claims_outpatient` | `claims_advanced` | `claims(t)` | `net_cf` |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | −71,250.00 |
| 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | +2,728.26 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | +2,706.68 |
| 3 | 120.02 | 7.32 | 0.00 | 2.34 | 0.00 | 0.00 | 0.00 | 129.68 | +2,554.93 |
| 4 | 119.05 | 7.26 | 0.36 | 2.50 | 1.19 | 0.11 | 0.08 | 130.55 | +2,532.47 |
| 5 | 118.10 | 7.20 | 0.71 | 2.65 | 2.36 | 0.22 | 0.16 | 131.39 | +2,510.20 |

The `claims(t)` column above is the benefit **total**, shown here so that the row can be
read; it is not a column of the published statement. `result_cf()` publishes the split lines
and no subtotal beside them, so that its columns add to `net_cf` as they stand — a statement
carrying its own subtotal among its parts stops being additive unless the reader knows
which column to skip. The total remains available as the `claims(t)` cells with its `kind`
omitted.

The row for `t = 5` is the one to check a rounding convention against: its seven displayed
components re-add to 131.40 while `claims(t)` is 131.39, because the total is the sum of the
unrounded lines. Assert against the unrounded values, not against the printed row.

**Trace, month 0.** `pols_healthy(0) = 1`, `pols_cancer(0) = 0`. Premium `= 3,000 × 1 =
3,000.00`. `cover(0) = 0`, so every cancer term is zero — not small, **zero**. `expenses =
250 (maintenance) + 20,000 (acquisition) = 20,250.00` and `claim_expenses = 0`, because
there are no claim events. `commissions = 1.5 × 36,000 = 54,000.00`. `net_cf(0) = 3,000.00 −
20,250.00 − 0 − 54,000.00 = −71,250.00`. Decrements: `pols_healthy(1) = 1 × (1 − 0.0000792012) ×
(1 − 0.0078284203) = 0.992093`; `pols_cancer(1) = 0`; `Z(1) = 1` (the in-situ ledger cannot
move before `t = 3`).

**Trace, month 1.** `premiums = 3,000 × 0.992093 = 2,976.2790`; `expenses = 250 × 0.992093 =
248.0232` and `claim_expenses = 0`; `commissions = 0` (renewal commission starts at `t =
12`); `net_cf(1) = 2,976.2790 − 248.0232 = +2,728.26`. `pols_healthy(2) = 0.992093 ×
0.992093 = 0.984249`. **Month 2 is month 1 scaled again**: `premiums = 2,952.7456`,
`expenses = 246.0621`, `net_cf(2) = +2,706.68`, `pols_healthy(3) = 0.976466`.

**Trace, month 3 — cover attaches.** `cover(3) = 1` for the first time and the model starts
paying, from a **diagnosed population that is still empty**: `diag_first(3) = 0.976466 ×
0.000122909 = 0.000120016`, so `claims_diag(3) = 1,000,000 × 0.000120016 = 120.0161`.
`insitu_ev(3) = 0.976466 × 1 × 0.0000149949 = 0.0000146420`, so `claims_insitu(3) = 500,000
× 0.0000146420 = 7.3210` and the in-situ surgery is `0.80 × 200,000 × 0.0000146420 = 2.3427`
— which is the **whole** of `claims_surgery(3)`, because `pols_cancer(3) = 0`. Every other
claim line is zero for the same reason. `claims(3) = 120.0161 + 7.3210 + 2.3427 = 129.6798`.
`expenses = 250 × 0.976466 = 244.1165` and `claim_expenses = 5,000 × (0.000120016 +
0.0000146420) = 0.6733`, ¥244.7898 of expense between them. `net_cf(3) = 2,929.3982 −
129.6798 − 244.1165 − 0.6733 = +2,554.93`. Decrements:
`pols_healthy(4) = (0.976466 − 0.000120016) × 0.992093 = 0.968626`; `pols_locked(4) =
0.000120016 × (1 − 0.0077050451) = 0.000119091`, and `unlock` is zero because `t + 1 < C`.
`Z(4) = 1 × (1 − 0.0000149949) = 0.999985`.

**Trace, month 4 — the diagnosed state is live.** `pols_cancer(4) = 0.00011909`, and the
five care benefits are that number times the per-diagnosed-life-month amounts above:
`claims_hosp = 3,000.00 × 0.000119091 = 0.3573`; `claims_treat = 100,000 × 0.10 ×
0.000119091 = 1.1909` (`M(4) = 0`, so `paid_months = min(0.10, 60) = 0.10`);
`claims_outpatient = 916.6667 × 0.000119091 = 0.1092`; `claims_advanced = 0.001 × (600,000 +
60,000) × 0.000119091 = 0.0786`. `claims_surgery` now has both limbs: `200,000 × (0.35 ×
0.0208333 × 0.000119091 + 0.80 × 0.0000145242) = 200,000 × (0.00000086837 + 0.0000116193) =
2.4975`, where `insitu_ev(4) = 0.968626 × 0.999985 × 0.0000149949 = 0.0000145242`.
`diag_first(4) = 0.968626 × 0.000122909 = 0.000119053` gives `claims_diag = 119.0525`, and
`diag_rep(4) = 0` because `pols_open(4) = 0`. `claims(4) = 119.0525 + 7.2621 + 0.3573 +
2.4975 + 1.1909 + 0.1092 + 0.0786 = 130.5481`. `premiums(4) = 3,000 × 0.968626 = 2,905.8782`
— note that it is **`pols_healthy`, not `pols_if`**: the 0.000119 of diagnosed lives pay
nothing. `expenses = 250 × 0.968745 = 242.1863` — the maintenance expense is on `pols_if`,
because a waived policy is still serviced — and `claim_expenses = 5,000 × (0.000119053 +
0.0000145242) + 3,000 × 0.0208333 × 0.000119091 = 0.6679 + 0.0074 = 0.6753`, ¥242.8616 of
expense between them. `net_cf(4) = 2,905.8782 − 130.5481 − 242.1863 − 0.6753 = +2,532.47`.

**Policy year 1 in aggregate** (`t = 0…11`, all at age 40, all in policy year 1 — the
strongest single test target in this file, because it exercises the waiting-period boundary
and the first three months of the diagnosed state on one set of rates).

| Line | Policy year 1 total |
|---|---|
| `premiums` | 34,462.5629 |
| `claims_diag` | 1,046.0977 |
| `claims_insitu` | 63.8082 |
| `claims_hosp` | 12.3980 |
| `claims_surgery` | 26.4454 |
| `claims_treat` | 41.3265 |
| `claims_outpatient` | 3.7883 |
| `claims_advanced` | 2.7275 |
| `claims(t)` total | 1,196.5915 |
| `expenses` | 22,872.9134 |
| `claim_expenses` | 6.1269 |
| `commissions` | 54,000.0000 |
| `net_cf` | **−43,613.0689** |

with `Σ pols_if(t) = 11.491654`, `Σ pols_healthy(t) = 11.487521`, `Σ pols_cancer(t) =
0.004133`, and at the year end `pols_if(12) = 0.909137`, `pols_healthy(12) = 0.908130`,
`pols_cancer(12) = 0.001006`, `M(12) = 0.4002`, `V(12) = ¥2,401.31` and `Z(12) = 0.999865`.
(The totals are sums of unrounded monthly values; the six displayed monthly rows do not
re-add to them.)

**What the numbers say.** Year-1 claims are **3.47%** of year-1 premium, against 21.5% on
the `medical` chassis at the same age, same daily amount basis and same expense scale — and
the gap is the product, not an error. Three things drive it. The first quarter pays
**nothing**. The diagnosed population starts empty and is still only **0.11%** of the
in-force after twelve months, so the five benefits that run on it — at ¥16,035 per diagnosed
life-month — contribute `16,035 × 0.004133 = ¥66.27` in the whole year, and of the ¥26.45 of
surgery benefit ¥20.42 is in-situ surgery, which is not on that state at all. And cancer
incidence at 40 is 0.00147 a year against
the `medical` chassis's 0.0466 hospitalisation incidence — a factor of 32 — while the
sourced incidence curve rises by a factor of **11.3** from the 40–44 band to the 85–89 band
(220.28 to 2,497.39 per 100,000 [R5]). This is a product whose cost is almost entirely in
front of it: the ¥74,000 of acquisition expense and initial commission at `t = 0` is
recovered from an early margin that the incidence curve then takes back with interest. A
ten-year projection — the horizon the 1号収支分析 [REG-R22] and the third-sector ストレステスト [R3]
both use — sees almost none of the liability this contract actually carries.

---

## Valuation and reserve pointers

This library projects gross cash flows. Every valuation layer below consumes them and is
cited, never reproduced. The statutory chain is the third-sector chain and is set out once,
on the chassis, in the [medical technical notes (医療保険)](../medical/technical-notes.md); only what
differs for cancer is repeated here.

- **標準責任準備金.** 保険業法 第116条 requires the reserve and delegates the method [REG-R4], 施行規則 第68条
  fixes scope [REG-R7], and 平成8年大蔵省告示第48号 sets it as net level premium (*heijun
  jun-hokenryō-shiki*, **平準純保険料式**) on the standard valuation interest rate (*hyōjun riritsu*,
  標準利率) and the standard table [R4] [REG-R10]; for contracts from **1 April 2018**
  that table is **第三分野標準生命表2018** [R1] [R2] [REG-R11] [REG-R18]. The 標準利率 in force could not
  be established from a retrieved document and any value asserted for it is [unverified]
  [REG-R10]. What the chain does **not** contain is a cancer-incidence basis: the reserve's
  morbidity assumption is the insurer's own, unpublished [R3] [REG-R2].
- **危険準備金, third-sector limb.** 施行規則 第69条 carries the reserve taxonomy [REG-R8]; the 監督指針
  requires the limb be computed under the **ストレステスト** of 平成10年6月8日大蔵省告示第231号 with a
  **負債十分性テスト**, reflecting the uncertainty that 保険事故発生率 deteriorates, in principle per 契約区分
  sharing a common 基礎率 [R4] [REG-R13] [REG-R14]. The FSA policy paper puts the stress at
  危険発生率A covering **99%** of incidence risk and 危険発生率B **97.7%**, over a **10-year**
  horizon, with annual 事後検証 [R3]; **the notification itself was not retrieved and its
  magnitudes are [unverified]** [REG-R13]. `jplib` implements the *capability* the regime
  demands — a re-runnable incidence basis, parameterized so a shock can be applied per
  grouping — and **not** the statutory stress. That distinction must not be blurred.
- **ESR, and 1号収支分析.** From **31 March 2026** insurers are supervised on 経済価値ベースの ソルベンシー規制:
  **現在推計 + MOCE** at each 基準日 on assumptions re-set then, required capital at **99.5%**,
  corrective action below **100%** [REG-R15], superseding the ソルベンシー・マージン比率 **200%** trigger
  [REG-R17]. `jplib` computes neither; what it owes both is a projection re-runnable at a
  stated 基準日. The appointed actuary (*hoken keirinin*, 保険計理人) of 保険業法 第120条 [REG-R5] submits
  the 意見書 of 第121条 [REG-R6], which the 実務基準 turns into a forward income-and-outgo analysis
  over 「少なくとも将来10年間」 by 区分経理 segment [REG-R22] — and on this product more than any other,
  ten years is a small fraction of the liability. J-GAAP [REG-R10], ESR [REG-R15] and IFRS
  17, voluntary in Japan [REG-R47], are three measurement bases fed by one set of cash
  flows, which is why these stay undiscounted.
- **Not applicable to this chassis.** 契約者配当 and the surplus-distribution methods of 施行規則
  第30条の2 [REG-R9] do not attach: the composite is 無配当 [S5] [S6] [S11]. 価格変動準備金 under 第115条
  is asset-driven and outside a liability projection [REG-R3].
- **Policyholder tax, not modelled.** The premium falls in the 介護医療保険料控除 basket of the
  post-2012 生命保険料控除 [R8] [REG-R43]; the anchor's ¥36,000 annual premium sits in the second
  income-tax band for a deduction of ¥28,000 = ¥36,000 × 1/2 + ¥10,000 [R9]. Benefits are
  stated to be in principle non-taxable where the payee is the insured, a spouse, a lineal
  relative or a 生計を一にする親族 [S1], and are not projected net of policyholder tax.

---

## Key sensitivities and model risks

In rough order of leverage on a cancer block:

1. **The survival basis, not the incidence basis, is the biggest lever — and it is the one a
   medical model does not have.** Three of the seven benefit streams (repeating diagnosis,
   unlimited-day inpatient, monthly treatment) are integrals over post-diagnosis survival.
   The base run's flat excess hazard from a 5-year relative survival figure [R6] is a
   **[std]** construction that overstates late-duration mortality, and every month of
   survival it removes takes benefit the product is designed to pay with it. A cure-fraction
   or duration-banded hazard moves the liability in one direction only: up.
2. **The relapse hazard.** `rel_rate` = 0.06 p.a. **[std]** produces 1.4856 diagnosis
   payments per diagnosed life at the anchor age. There is no source. Doubling it to 0.12
   p.a. moves the diagnosis benefit by more than any other single parameter, and the
   `repeat_conditioned` switch [S7] [S10] moves it by an order of magnitude in the other
   direction.
3. **The incidence basis is genuinely sourced — and that makes its remaining [std] parts
   sharper, not softer.** The age-band rates are public and citable [R5] [REG-R29]; the
   **sex split** is a two-point interpolation, and the male and female curves cross, so a
   unisex or badly split basis is wrong at every age [R5]. The in-situ increment's
   **age-invariance** is [std] and is the second-order version of the same problem.
4. **The treatment benefit's frequency, and the 60-month cap.** `treat_prob` = 0.10
   **[std]** with no observed range gives 12.98 expected qualifying months against a
   60-month cap [S5] [S11]. Because the cap binds for a real minority rather than never, the
   deterministic cohort-average ledger's understatement of `E[min(Σ, K)]` is a live error
   here, not the dormant one it is on the `medical` chassis.
5. **Longevity, not mortality, is the tail risk — twice over.** The sourced incidence curve
   rises by a factor of 11.3 from the 40–44 band to the 85–89 band [R5], so the liability is
   concentrated where the survival assumption is least certain; and on top of that a
   **lighter** mortality basis keeps more lives in the diagnosed state, where they are
   drawing ¥16,035 a month at the anchor cell's parameters. Using the valuation table
   unadjusted as a best estimate is a conservative error in the reserving direction and a
   material one over a 76-year projection [R2] [REG-R20].
6. **The waiver makes premium and claims anti-correlated by construction.** Every first
   diagnosis simultaneously starts the benefit stream and stops the premium [S10] [S11], and
   a diagnosed life then cannot lapse. Any error in incidence therefore hits both sides of
   the cash flow at once, roughly doubling its effect on `net_cf`.
7. **The premium is an input with no market anchor.** No carrier publishes a rate table for
   this product; the only retrieved price point is a 2013-basis ten-year term at twice the
   composite's benefit amounts [S5], and the 算出方法書 is not published [REG-R2]. Every
   profitability statement about the anchor cell is a statement about ¥3,000 **[std]**, not
   about the market.
8. **Expense inflation on a small premium.** ¥250 a month of maintenance against a ¥3,000
   premium is 8.3% of premium, the premium is fixed for life, and the expense is not — and
   on the waived population the expense runs with no premium against it at all.

### Known modeling pitfalls

- **The 90-day waiting period is a hard zero, not a reduced rate.** No cancer benefit of any
  kind is payable in months 0, 1 and 2, and no life transitions into the diagnosed state
  [S1] [S5] [S6] [S10] [S13]. A model that starts the incidence at `t = 0` pays three months
  of benefit that no contract in the retrieved set pays.
- **The premium is still charged during the waiting period.** Five carriers charge from
  inception [S1] [S5] [S6] [S7] [S10]; one charges nothing for three months and says
  explicitly that this is not a discount [S11]. The composite charges. Suppressing the
  premium and the benefit together is a different product.
- **An in-window diagnosis voids the contract; it does not lapse it.** Premiums already
  collected come back [S1] [S5] [S10]. Putting it in the lapse column keeps premium income
  the insurer never earned. The base run omits the adjustment and the omission is 0.037% of
  policies at the anchor cell — state it, do not silently absorb it.
- **上皮内新生物 is a second benefit tier, not a discount on the first.** It has its own once-only
  cap, it is not payable after a full-rate benefit, it does not start the two-year cycle,
  and it does **not** trigger the premium waiver [S6] [S11] [S7] [S10]. Implementing it as
  `insitu_pct × claims_diag` inside the main diagnosis benefit gets the amount right and the
  cap, the cycle and the waiver all wrong.
- **Premiums are weighted by `pols_healthy`, claims by `pols_cancer`.** The waiver fires on
  the same event that starts every benefit [S10] [S11]. Multiplying the premium by `pols_if`
  is the single largest arithmetic error available in this product, and it is invisible in
  the first three months because the two are equal.
- **A diagnosed life cannot lapse.** No premium to miss and no surrender value to take [S7]
  [S10] [S11]. Applying the healthy lapse rate to the diagnosed state deletes exactly the
  claimants the product exists to pay.
- **There is no `L1`, no `LA` and no benefit-driven termination.** Inheriting `medical`'s
  60/120-day per-hospitalization cap, its 1,095-day aggregate or the termination they create
  caps a benefit that every source says is uncapped [S1] [S3] [S5] [S6] [S10] [S13] [R11],
  and it terminates a contract that cannot exhaust [S1].
- **The 2-year cycle is not the 180-day one-hospitalization rule.** Different length,
  different trigger (a payment, not a discharge), different consequence (eligibility, not
  grouping) [S5] [S1]. Sharing one clock between `medical` and `cancer` breaks both.
- **The cycle clock runs from the previous *trigger*, not the previous payment or
  admission.** The three sourced two-year designs measure it from the trigger date [S5],
  from the first day of the calendar month of the previous payment [S7], and from the start
  date of the last hospitalisation [S10]. Only the first needs no second date carried
  alongside; implementing one and documenting another is a silent divergence.
- **The treatment benefit's unit is a month, not a day and not an event.** A prescription
  covering two months pays one month; two triggers in one month pay once; two triggers on
  one day pay once [S10] [S11]. Any formula in which a day count reaches `claims_treat` is
  wrong by construction, and the dimensional check above is there to catch it.
- **The 60-month cap is a ledger on months, and the ledger is per diagnosed life.**
  Weighting it by `pols_cancer` measures the block's consumption, not the individual's, and
  defers the cap forever. Diluting it with `diag_rep` as well as `diag_first` resets a
  ledger that should keep running: a repeat trigger is an already-diagnosed life.
- **Do not delete a ledger because it reads small.** `M(12) = 0.4002` months and `V(12) =
  ¥2,401.31` at the anchor cell, but `E[min(Σ, K)] ≠ min(E[Σ], K)`, and unlike `medical`'s
  通算 day ledger this one is reached by a real minority of diagnosed lives.
- **In-situ diagnoses generate the surgery benefit and nothing continuing [std].** They do
  not enter `pols_cancer`, so they contribute no inpatient, treatment or outpatient benefit
  — a documented simplification with a stated direction of error, not an omission. A model
  that routes them into the diagnosed state credits them with an exposure 患者調査 does not
  measure [R7].
- **`claims_lapse(t)` is identically zero and `claims_death(t)` does not exist.** There is
  no surrender value under 終身払 [S7] [S10] [S11] and no death benefit in the composite [S1].
  A non-zero column for either is a benefit the contract does not have.
- **第三分野標準生命表2018 is a valuation table, not experience.** Using it unadjusted as a
  best-estimate decrement understates mortality, which on a morbidity product **overstates**
  the liability; the [std] 1.25 factor unwinds the sourced 70–85% adjustment band and
  nothing more [R2] [REG-R20]. The same factor must be used here and on the `medical`
  chassis.
- **Relative survival is not a mortality table.** [R6] publishes 5年相対生存率, which nets out
  background mortality — so it converts into an **excess hazard added to** the baseline, not
  into a replacement for it. Multiplying survivorship by a relative-survival figure
  double-counts the background.
- **Cancer deaths sit on both sides of the mortality basis.** The never-diagnosed carry a
  population table that already contains cancer mortality, and the diagnosed carry it again
  as an excess hazard. At the anchor age the effect is 1% of the excess hazard; at 80 it is
  not. A `net_of_cancer` baseline is a switch, and the double-count must be stated rather
  than discovered.
- **Age-band incidence steps; it does not glide.** The registry publishes five-year bands
  [R5]. Interpolating within a band is a choice, not a correction, and it must be the same
  choice in the model and in the CSV's `provenance` column.
- **復活 re-runs the waiting period.** A reinstated cancer policy has 90 days of no cover in
  front of it [S1] [S6]. Modelling reinstatement as a negative lapse restores cover the
  contract does not restore, and it deletes a real anti-selection control.
- **Rounded lines do not re-add.** The `t = 5` claim components displayed to ¥0.01 sum to
  131.40 against a `claims(t)` value of 131.39, and the seven policy-year-1 claim lines
  displayed to four decimals sum to 1,196.5916 against a `claims(t)` total of 1,196.5915.
  Assert against the unrounded aggregation, never against a sum of displayed figures.
- **A subtotal published beside its own parts.** The benefit total is a *cells*, never a
  column: `result_cf()` carries the nine `claims_*` splits and nothing named `claims`, so
  its columns add to `net_cf` as they stand. Publishing the total alongside them makes the
  statement silently non-additive for any reader who sums the row, and doubles the benefit
  side of every check written off the table.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-cancer-r1
[R11]: #jplib-cancer-r11
[R2]: #jplib-cancer-r2
[R3]: #jplib-cancer-r3
[R4]: #jplib-cancer-r4
[R5]: #jplib-cancer-r5
[R6]: #jplib-cancer-r6
[R7]: #jplib-cancer-r7
[R8]: #jplib-cancer-r8
[R9]: #jplib-cancer-r9
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
[REG-R27]: #jplib-reg-r27
[REG-R28]: #jplib-reg-r28
[REG-R29]: #jplib-reg-r29
[REG-R3]: #jplib-reg-r3
[REG-R31]: #jplib-reg-r31
[REG-R33]: #jplib-reg-r33
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
