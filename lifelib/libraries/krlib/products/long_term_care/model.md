# Implementation Notes

**Status:** Draft, 2026-09-03. Built from [`technical-notes.md`](technical-notes.md); the
product those notes describe is specified in [`product-spec.md`](product-spec.md), and every
source tag on this page resolves in [`sources.md`](sources.md). Where the model carries
something the documents do not settle, it is named here rather than absorbed.

> **This is a mechanics demonstration, not a pricing or reserving result.** What is sourced
> on this product is the contractual machinery: the grade-only trigger with no company-basis
> limb, the 최초 1회한 장기요양진단급여금 (*janggi-yoyang jindan geubyeogeum*) that
> extinguishes its own benefit line without terminating the contract, the survival-tested
> 간병연금 (*ganbyeong yeongeum*) with its twelve-month guarantee and 120-month cap, the
> amount and the 감액 both frozen at first certification, the 납입면제 firing on the same
> event as the benefit, the bar on surrender once the annuity has started, the nil
> 해약환급금 during the premium-paying period, and the 계약자적립액 payable on death from a
> cause the contract does not cover [S1] [S2] [S3] [S4] [REG-R17]. Almost everything
> quantitative is **[std]**. 보험개발원 publishes **neither a 장기요양 incidence table nor a
> post-onset mortality table**, the 경험생명표 is not released in full [REG-R33] [REG-R34], and
> no 산출방법서 was retrieved for any Korean long-term-care product — so the office premium is
> a model-point **input**, the mortality table is a construction anchored on published summary
> 기대여명, and the morbidity basis is built in public from the 노인장기요양보험 통계연보 [R4]
> and calibrated against the one disclosed 예정위험률 [S1]. Replace the assumption tables with
> company data before reading anything off the output.

`LTC_KR_S` is the modelx implementation: a monthly, single-model-point projection of gross
best-estimate liability cash flows for 간병보험 (*ganbyeong boheom*, long-term-care
insurance) on the **공적기준 (type ②)** design, whose 지급사유 is written by reference to a
장기요양등급 awarded by a 등급판정위원회 under the 노인장기요양보험법 and to nothing else.

**The chassis.** This product states its deltas against the `krlib` fixed-benefit (정액)
제3보험 chassis, whose model is [`Cancer_KR_S`](../cancer/model.md). `LTC_KR_S` does **not**
inherit from it in modelx — `Projection._bases` is empty — so the relationship is documentary.
What is inherited in substance is the monthly grid, the timing conventions, the 만나이 basis,
the mortality construction, the 보장개시일 with its 재해 carve-back, the 50% 감액기간, the
무해지환급형 cliff and the log-linear lapse vector. What is replaced is the trigger and with it
the shape of the liability: cancer pays on a **pathological event with a date**, long-term care
on an **administrative determination of a state** in which the insured then lives, draws an
annuity, stops paying premiums and dies well above a healthy life's rate. There is no severity
ladder, no 유사암 tier and no 재진단 clock; there is a compartment chain and a survival-tested
annuity ledger instead.

## Run it

From the repository root:

```bash
python products/long_term_care/run.py       # the anchor cell, point_id = 1
python products/long_term_care/run.py 5     # the 100세만기 cell, 치매 rider on
```

`run.py` prints the model point, the first thirteen policy months of the statement, the
policy-year-1 and whole-projection totals, the calibration ratio against the one disclosed
예정위험률 and the six `check_*` identities. Everything it prints is ASCII, so the output lands
on a Windows console under any code page: amounts are labelled `KRW`, the Korean is romanized
and the thresholds print as the `g1` … `g6` codes the input tables use. Real output, with the
thirteen-row statement and the policy-year-1 list elided — both are in
[`technical-notes.md`](technical-notes.md) in full:

```text
model point 1: LTC-000001 - ganbyeong boheom, M40 man-nai, to age 90, 20-year pay, frame = 601 rows (t = 0 .. 600)
lump 10,000,000 KRW at g2   annuity 500,000 / 300,000 KRW per month x120 months (12 guaranteed), on = True
premium = 5,600.00 KRW/month (67,200.00 p.a.)   uw loading = 1.00   dementia rider = False   wait = 3 mths   reduction = 12 mths
cv form = mijigeup   lapse form = mujihae   net premium ratio = 0.7932   care mortality multiple = 3.00

first 13 policy months, t = 0 .. 12 (columns claims_dementia, claims_void and claims_maturity omitted here; result_cf() carries them):

    [ the t = 0..12 rows of result_cf(), eleven columns ]

policy year 1 totals, t = 0 .. 11 (unrounded sums):

    [ the ten policy-year-1 lines, net_cf -10,481.10 ]

whole projection, undiscounted:
  premiums                  973,533.06
  ltc benefits              814,977.83
  gyeyakja-jeongnipaek on death 326,783.93
  haeyak-hwangeupgeum on lapse  70,149.78
  expenses + commission      210,476.72
  net_cf                   -448,855.21
  lives ever certified at the benefit grade: 0.02681

model incidence over the disclosed yejeong-wiheomnyul, first-entry basis:
  man-nai 40: ratio 0.240
  man-nai 50: ratio 0.246
  man-nai 60: ratio 0.240

checks: pols_roll_fwd=True nesting=True ann_ledger=True av_continuity=True cv_form=True net_cf=True
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/long_term_care/LTC_KR_S")
model.Projection[1].result_cf()      # the worked example's anchor cell
```

`result_cf()` returns a `DataFrame` indexed by policy month `t` with seventeen columns;
`result_pols()` prints the compartments, the entry and exit counts, the annuity ledger's count,
the decrement rates and `av_pp` / `cv_pp` beside them, which is where the compartment chain
becomes legible. It carries `pols_entry_care` whole; the two routes into it are cells and not
columns of it, so read `pols_entry_care_direct(t)` and `pols_entry_care_prog(t)` directly — the
second overtakes the first at `t = 8` on the anchor cell. `model.Projection.doc` maps the
notes' symbols to the cells names and states the age basis; `model.Data.doc` says what each
input file is and, for the mortality table, what it is **not**. A cold sweep of all nine model
points takes about **40 seconds**.

## Four compartments, three of which add to `pols_if`

The contract is a **three-state model** — healthy, in long-term care, dead — but the care state
is not entered in one step. Only **13.3%** of current 1등급 certifications arose from a first
application, against 69.5% from a renewal, whereas at 인지지원등급 — a grade nobody can
progress *down* into — the first-application share is **69.8%** [R4 표2-5, derived](#krlib-long_term_care-r4):
severe-grade lives are in the main people who entered years earlier at a light grade and
deteriorated. So the block is carried in three compartments and one counter:

| Cells | What it holds | Premium | Lapse | Mortality |
|---|---|---|---|---|
| `pols_healthy(t)` | never certified | pays | exposed | `mort_rate_mth` |
| `pols_light(t)` | certified **below** `benefit_grade()` | pays | exposed | `mort_rate_light_mth` |
| `pols_care(t)` | certified at or above it | waived | **not** exposed | `mort_rate_care_mth` |
| `pols_dem(t)` | already paid the 치매 rider | — | — | `mort_rate_dem_mth` |

`pols_act(t)` is the first two together — the premium-paying, lapse-exposed population — and
`pols_if(t) = pols_act(t) + pols_care(t)`. `pols_dem` is a **first-event counter nested
inside** the block, never added to it; `check_nesting()` asserts both the addition and the
nesting.

Zero lapse in the care state is a **constraint, not an assumption**: the premium is waived and
the 약관 bars surrender once the annuity has started — 「최초 지급사유가 발생한 후에는 이
특약을 해지할 수 없습니다」 [S1]. Within a month the order is **certification, then mortality,
then lapse** [std]; `pols_*_mid(t)` are the counts after the month's certifications and before
its mortality, which is what the death and lapse decrements are taken from, and `pols_if_at(t,
timing)` publishes the three reads.

## 인정률 is a prevalence, and converting it is the modelling work

The one large public dataset counts people **holding** a certification, not people entering one
[R4]. Writing `P(x)` for the all-grade prevalence at 만나이 `x`, `s_G(x)` for the share of
certified lives at grade `G` or above, `P_C = s_G P`, `P_L = P - P_C`, and `mu_L`, `mu_C` for
the two impaired forces with `mu_bar` the population average, the compartment identities in a
stationary population are

    inflow_C(x) = P_C'(x) + P_C(x) ( mu_C(x) - mu_bar(x) )
    inflow_L(x) = P_L'(x) + P_L(x) ( rho(x) + mu_L(x) - mu_bar(x) )

**The excess-mortality term is not a refinement.** A rising prevalence understates entry,
because the compartment it measures is being drained by an excess mortality the population
around it does not carry — and that drain is what the 간병연금 is exposed to. Using `mu_C`
alone in place of `mu_C - mu_bar` overstates entry, which is why `mort_force_avg_at` exists.

Two equations carry three unknowns, and the closing assumption is the one the sources leave
open: `direct_entry_share` = **0.20** [std], the share of gross inflow into the care state
arriving straight from health rather than by progression, anchored on the split above. Then

    i_D(x) = direct_entry_share * inflow_C(x) / ( 1 - P(x) )
    rho(x) = ( 1 - direct_entry_share ) * inflow_C(x) / P_L(x)
    i_L(x) = inflow_L(x) / ( 1 - P(x) )

which are `inc_rate_direct_at`, `prog_rate_at` and `inc_rate_light_at`. Getting
`direct_entry_share` wrong changes the lifetime claim count little — 0.05 and 0.50 move
lifetime benefit outgo +0.7% and −1.8% — but it changes **when** the claim arrives, which on a
contract priced at 2.0% over fifty years is most of the answer.

Three properties belong in front of a reader rather than in a footnote.

- **Stationarity.** The cross-sectional 인정률 is read as the prevalence path a cohort will
  follow; the certified stock grew **71.8%** in six years [R4] [R18], so it **understates**
  entry.
- **The care compartment leaves only by death**, where **107,365** current certifications —
  9.2% of the stock — arose from a 등급변경신청 [R4 표2-5](#krlib-long_term_care-r4). No retrieved source gives a
  transition matrix, so the omission understates entry again.
- **Below 65 there is no prevalence data at all**, the statute admitting an under-65 applicant
  only through the closed 25-item 노인성 질병 list [REG-R55] [R2]. Below 65 the two entry rates
  are carried down from their age-65 values on `sub65_factor_at`, the log-gradient of the one
  disclosed 예정위험률 — **13.0% a year for men and 17.9% for women** [S1, derived]. The
  progression rate is **not** scaled, being a property of a life already certified rather than
  of the gate, so `rho(40) = 0.0340` exceeds `rho(65) = 0.0153`: wrong-looking on a decrement
  table, right here.

## The disclosed 예정위험률, and the ratio the model publishes

Exactly one retrieved document publishes a Korean long-term-care incidence rate: one carrier's
예정위험률 at 만나이 40, 50 and 60 by sex, for 요양(1등급) and 요양(2등급) separately [S1]. It
is used for its **gradient and its sex ratio** below 65, and as a level cross-check — never as
the level. `disclosed_inc_ratio_at(x)` publishes the comparison rather than hiding it:

on the male anchor cell it is **0.240** at 만나이 40, **0.246** at 50 and **0.240** at 60. So
the disclosed pricing rate is about **4.2 times** this model's best estimate at the same age,
and the ratio is almost flat — a level difference rather than a shape difference. Four things
all push the same way and none of them is quantified by any retrieved source: a 예정위험률 is a
**loaded** rate and not a best estimate; the conversion reads a cross-section as a cohort path
in a growing scheme; the care compartment is treated as leaving only by death; and the
disclosed card is quoted on **보험나이**, about half a year older than this model's 만나이. It
is the largest single uncertainty in the model and `technical-notes.md` carries it as a stated
sensitivity rather than closing it with an invented factor.

The construction is nonetheless coherent with the *other* sourced anchor. The PV at the
예정이율 of the anchor cell's benefit outgo is **46.03%** of the PV of premium income, and the
PV of its expense and commission basis **20.26%** against the **20.68%** loading
`net_prem_ratio()` implies. Only the first of those two is evidence: `expense_maint` is
*calibrated* to that loading, so 20.26 against 20.68 is a construction and the 0.42-point gap
is the rounding of `expense_maint` to a whole ₩200. The 46.03% is calibrated to nothing — the
incidence basis comes from the 통계연보 [R4] and the ₩5,600 premium from a published rate card
[S2] — and that is the agreement worth having.

## The grade share is indexed by age, and that is load-bearing

`share_ge_at(grade, x)` interpolates linearly between six sourced band representative ages —
60, 67, 72, 77, 82 and 88.5 — because the severe share is **U-shaped** in age: 1·2등급 is
**22.2%** of certified lives under 65 on the shipped table, falls to **11.1%** at 80-84 and
rises again to **14.8%** at 85 and over [R4 표2-9, derived](#krlib-long_term_care-r4). (That 22.2% is the sum of the
two rounded grade shares; [R4]'s own derived 1·2등급 계 for the band is 22.3%, and the tenth of
a point between them is rounding inside the source table.) The under-65 population is severe
because only the 노인성 질병 list gets in at all; the 80-84 trough is where the marginal
entrant is a lightly impaired person newly crossing the 51-point line. **One grade-mix vector
at all ages mis-prices a 1~2등급 benefit by up to a factor of two.**

Because the share moves with age, `prev_care_slope_at` uses the **full product rule**, `s_G'(x)
P(x) + s_G(x) P'(x)`. The first term is negative over most of the range for a severe threshold;
dropping it inflates `P_C'` by 1.82× at 만나이 65, and the symptom is a `claims_lump` rising
monotonically with age where the shipped model has it **falling** between `t = 239` and `t =
240` — 139.1227 to 101.8715. `share_slope_at` is exact for the piecewise-linear share and
`prev_slope_at` is the **analytic** derivative of the logistic; a numerical one would put noise
into the claim rate.

## The 간병연금 ledger: monthly instalments, an annual test, two freezes

Instalments are **monthly**; the cohort certified in month `s` is paid in months
`s … s + n_A - 1`, the first twelve guaranteed against death and each later block of twelve
released only by the annual survival test on the anniversary of the 진단확정일 [S1]:

    ann_count(t) = sum over u = 0 … n_A-1 of  n_C(t-u) * weight(u)
    weight(u)    = 1                                   for u < annuity_guar_mths()
                 = S_C(t-u, t-u + 12*floor(u/12))      otherwise

The first instalment falls in the **month of certification**. `care_surv(s, t)` is a **partial
product** of `(1 - q_C(u))` and never a ratio of cumulative products: `q_C` is capped at 1 and
the cap binds from 만나이 108 on the male table and 112 on the female one, so a cumulative
product underflows to zero from there on and the ratio form divides by zero exactly where the
tail of a 종신 variant would live.

`ann_pay(t)` is the same sum valued at each cohort's **own** amount, `ann_amount_at(s)`, which
is what carries the two freezes [S1]:

- the **amount** is the grade blend at the entry age — `annuity_high` at 1등급 and
  `annuity_low` at every other grade in the gate, weighted by the age-specific shares — so a
  life entering at 2등급 and deteriorating to 1등급 keeps the lower rate for all ten years;
- the **감액 decision** is frozen too: a claim starting inside the reduction window stays
  halved for the whole term of the annuity. Re-testing it at each instalment date overstates
  every claim arising in the first policy year — ₩64.78 on the anchor cell, ₩1,065.24 at issue
  age 70 — and is the most easily mis-modelled rule in the product. Evaluate `red_factor` at
  `s`.

`ann_tests(t)` counts the annual proof-of-life events [S1], and the claim-handling expense is
charged on those, not on every monthly instalment: 0.0990 events against 1.4539 instalments
over the projection, a factor of fifteen in that expense line.

## The horizon is the 만기, and the annuity is truncated with it

`t` is the policy month and it is **0-based**: `t = 0` is the first projected month, the one
that carries the office premium, the acquisition expense and the initial commission together
with that month's own decrements. `proj_len() = 12 × (term_age − issue_age) + 1` is the
**number of projected months, the frame's exclusive end** — not the last index — so
`result_cf()` carries `proj_len()` rows, **601** on the anchor cell, indexed `t = 0 … 600`, and
the frame is `range(proj_len())`. The `+ 1` is the terminal row: the 600 months of cover are
`t = 0 … proj_len() − 2` and `t = proj_len() − 1` is the 90세 계약해당일 itself, where
`pols_if(600) = 0.2102` reaches maturity, `pols_maturity` records the cover ending, and every
cash flow on the row is zero. That asymmetry is visible in the guards: the cash-flow cells stop
at `t >= proj_len() - 1`, the in-force counts run to `t >= proj_len()`, and swapping the two
either puts outgo on the maturity row or drops the row `check_pols_roll_fwd()` closes on.

The annuity cap and the maturity bind **jointly**: nothing is paid on the maturity row
`t = proj_len() − 1` or after it. An insured certified at 85 on a 90세만기 contract has five
years of term and ten of annuity, and
**no retrieved document resolves whether the instalments continue past maturity**; the model
truncates, the conservative reading, and understates the benefit for late entrants [std]. The
만기 is the first sensitivity a user should run rather than a neutral choice: the same cell to
100세만기 raises lump-sum claims **70.6%** and annuity claims **59.3%** and takes
PV(benefit)/PV(premium) from 0.4603 to 0.6762 on an unchanged premium, because 90세만기
truncates the exposure at the band with the highest certification rate of all.

## 보장개시일 and 감액기간 are two different mechanisms

Korean practice keeps them apart and so does the model.

- **보장개시일.** A certification inside the window does **not** defer the claim: it makes the
  benefit 무효 and the premiums paid for it come back — 「특약을 무효로 하며, 이미 납입한
  보험료를 돌려드립니다」 [S1] [S2] — and unlike the cancer chassis there is no cancellation
  option and no revival. Those lives are `pols_void(t)`, **a decrement of its own** with
  `claims(t, "VOID")` attached, and never reach `pols_entry_care`. It is carried as a product
  fact, not for materiality: ₩0.0073 refunded over the projection. The refund is valued at
  `cum_prem_pp(t + 1)` and not `cum_prem_pp(t)` — premium falls at the start of month `t` and
  the void is recognised at the end of it, so a life voided in month 0 has paid one month's
  premium and 「이미 납입한 보험료를 돌려드립니다」 returns it.
- **감액기간.** Cover has started and the benefit is merely halved: `red_factor(t)` returns
  `1 - (1 - red_fraction) * disease_share`. The 약관 test is on the **cause**, not the grade —
  a 질병-caused certification inside the window is paid at 50%, an 상해/재해-caused one in full
  [S4] — and the frequency of the two is in **no retrieved source**, so `disease_share` = 0.95
  [std] and the blended factor is **0.525**.

Model point 9 carries the other observed combination — 180 days and two years at 50%, the
우체국 design [S1].

## The 계약자적립액, and why a pure protection contract carries an account

감독규정 제7-63조제1항제1호 requires a 제3보험 contract to pay the **계약자적립액**, plus the
미경과보험료, on death from a cause the policy does not cover, and terminate [REG-R17]
[REG-R25 제22조](#krlib-reg-r25). So death here is **a decrement with a large cash flow attached**: 35.4% of
the anchor cohort dies before maturity and `claims_death` is ₩326,784 undiscounted, a third of
premium income and larger than the lump sum. Deaths *in* the care state pay nothing [S1] —
which is why `pols_death` is split into `pols_death_act` and `pols_death_care`, 0.0166 of the
0.3543 cumulative deaths paying nothing.

`av_pp(t)` has two branches meeting at 납입완료: up to it, the accumulation of the net premium
at the **예정이율 of 2.0%** — the one place in `krlib` where the pricing interest rate is a
*retrieved* figure, stated in terms in a 기초서류 extract [S1]; after it, the sourced run-off
of `av_table.csv`, indexed on the **fraction of the way from 납입완료 to maturity** so one
published progression serves every term and paying period [std].

`net_prem_ratio()` is **derived, not assumed**: the fraction that, accumulated at the 예정이율,
reproduces the sourced 계약자적립액 at 납입완료 — **0.7931662309087683** on the anchor cell, a
예정사업비 loading of 20.68%. `check_av_continuity()` asserts the join at `t = 240`
(₩1,309,056.0000 read two ways) and fails the moment the derivation becomes a round number.

Two reconstruction assumptions are named rather than buried: the 기본형 whose value the
미지급형 progression is 50% of **cannot be bought** — 「'기본형'은 … 가입이 불가능하며」 [S2] —
and its premium is higher, so the two accounts are not in fact the same quantity [std]; and the
run-off between the sourced anchors is linear [std], where the real curve bends with the risk
cost.

## The surrender-value cliff, and four forms under three names

`cv_pp(t)` implements three of the four forms on the Korean shelf as a model point field rather
than a switch on a ratio, because reading 「50%」 without reading which side of 납입완료 it
attaches to puts the cliff upside down:

| `cv_form` | during the paying period | after 납입완료 | source |
|---|---|---|---|
| `mijigeup` | **nil** | 50% of the 계약자적립액 | [S2] |
| `half_during` | 50% | 100% | [S4] |
| `pyojun` | `max(AV - 해약공제액, 0)` from year 1 | the same | [S1] [REG-R19] |

The composite is `mijigeup`: **63.8% of Korean 보장성 초회보험료 in 2024 H1 was written in a
무·저해지 form** [REG-R27], so a library modelling only 표준형 would be modelling a minority of
the market. Its legal basis is 감독규정 제7-66조제4항, which lets a 순수보장성보험 priced on a
**최적해지율** pay less than the ordinary 계약자적립액 − 해약공제액 floor [REG-R19] [REG-R28].

On the anchor cell the model reproduces the published 환급률 progression exactly — **0.0% at
years 1, 5, 10 and 15, 48.7% at 20, 54.4% at 30, 50.5% at 40 and 0.0% at 50** [S2] — because
those figures *are* the input. `check_cv_form()` asserts the shape rather than the values. The
cliff itself is two steps in one month at `t = 240`: the lapse rate goes from the 0.1%
convergence point to the 0.8% ultimate, an eightfold jump in `pols_lapse`, and the value paid
on each lapse goes from nil to ₩654,528, so `net_cf` turns from +₩2,496.27 to −₩1,284.52.

`surr_chg_pp(t)` runs the 해약공제액 off straight-line over the premium-paying period **capped
at seven years** [REG-R19 제7-66조제1항](#krlib-reg-r19), at the supervisor's rule of thumb of **13 times the
monthly premium** for a 보장성보험 [REG-R29]. The rule of thumb is used rather than 별표 14's
formula because 별표 15 제9호 computes the notional 보험가입금액 as a ratio of risk premiums
that **excludes** 「치매 또는 일상생활장해 등 타인의 간병을 필요로 하는 상태」 — read
literally, it excludes long-term-care risk premium from the very ratio that gives a care-only
contract its 보험가입금액 [REG-R21].

## The waiver is not an independent decrement here

`G_W = G_B`. The 납입면제 fires on the **same event** as the benefit, waiving the main contract
and every attached rider [S3], so unlike the Japanese counterpart there is **no band of lives
paying nothing and claiming nothing** — the most mis-modelled item in that product does not
exist here. It is implemented by charging premium on `pols_act(t)` rather than `pols_if(t)` and
by nothing else; charging the whole block overstates lifetime premium income by ₩414.65 on the
anchor cell, 0.043%, and by far more at the top of the issue-age range.

It is not free, though: it converts a level premium into a stream that stops at an uncertain
date and stays stopped for the duration of the care state — the quantity the
prevalence-to-incidence conversion cannot pin down. On the anchor cell it almost never bites
inside the paying period; at model point 6, issue 65 with a 10-year pay, it does.

## Four columns that are zero on purpose

`result_cf()` publishes them rather than dropping them: a column that is absent and a column
that is zero say different things, and only one of them can be tested.

- **`claims_maturity` is zero at every `t` on every model point** — 「이 상품은
  순수보장성보험으로 … 만기환급금이 없습니다」 [S3] — a product fact, not an omission, and the
  maturity row is where a reader looks for it.
- **`claims_lapse` is zero for the whole premium-paying period** on the 미지급형 form — 240 of
  the anchor cell's 601 rows — and then steps to ₩281.90 in one month. Publishing the zeros is
  what makes the cliff visible as a cliff.
- **`claims_dementia` is zero on seven of the nine model points**, the rider being off.
- **`claims_void` is not zero but is of order 1e-3**, and is carried as its own column because
  a voided cover is a different mechanism from a refused claim.

There is **no `claims` column**, only the seven `claims_*` splits: an aggregate beside its own
parts would stop the columns summing to `net_cf`, and the library retires the name for it.

## Modules that are off in the base run

- **The 치매진단급여금 rider** (`dementia_rider`, on at model points 5 and 8). Its incidence is
  built by the **same prevalence-to-incidence identity** from a *sourced* prevalence — the 2023
  치매역학조사 band rates, 4.99% at 65-69 rising to 21.18% at 85 and over [R7] — rather than as
  a share of the certification rate, the two triggers being correlated but not proportional.
  `dementia_wait_mths = 15` is the one-year 보장개시일 plus the 90-day persistence test written
  into the definition of the state [S2] [S4], the one-year period being the settled market
  answer to the 2019 supervisory intervention [R10]. Two weaknesses are named: no logistic
  reproduces the near-equal 65-69 and 70-74 anchors (the fit is out by 31% at 70-74), and the
  sex factor is **flat in age** where the sourced series crosses over at 80 [R7] — so the model
  does **not** reproduce the market fact that 치매 covers are priced cheaper for women while
  장기요양 covers are dearer [S2].
- **The 간병연금** (`annuity_on`, off at model point 4). Switching it off removes most — not
  all — of the dependence on the post-onset mortality basis, the waiver still stopping premium
  for the care state's duration. It is two thirds of the anchor's benefit; without it `net_cf`
  turns positive.
- **The 간편심사 loading** (`uw_loading`, 1.40 at model point 8). A **premium** multiplier
  only: no retrieved source gives the simplified pool's incidence, so the extra premium is pure
  margin here and that pool's claim cost is understated [S2]. Model point 8's positive `net_cf`
  of +₩1,152,142 is an artefact of exactly that.
- **The 표준형 lapse vector** (`lapse_form`, `pyojun` at model point 7), carried so the two
  assumptions can be compared, which is what [REG-R27] requires an insurer to disclose. Not a
  small switch: the level 4.0% vector cuts lifetime benefit outgo 61.1% and turns `net_cf`
  positive.

## Absences that are product facts

- **No general death benefit**: no retrieved life-side long-term-care contract pays one [S1]
  [S3], and what `claims_death` carries is the statutory **계약자적립액**, not a sum assured.
- **No policy loan and no 보험료 자동대출납입** during the paying period on the 미지급형 form:
  with no surrender value to lend against, a missed premium lapses the contract outright
  [REG-R25 제33조](#krlib-reg-r25) [REG-R28] — nothing breaks the fall, and the lapse assumption nonetheless
  has lapse *falling* toward 납입완료.
- **No recovery decrement.** The amount is frozen and the instalments are metered on
  **survival**, not on continued certification [S1], so a Korean 간병연금 needs a post-onset
  **mortality** basis and not a recovery basis. The simplification is the *contract's*, not the
  model's — and it would **not** be available for the utilisation-conditioned 지원금 form [S2].
- **No 갱신형 machinery.** Every retrieved document writes the benefit 비갱신형 and attaches
  renewal to the riders travelling with it [S1] [S2]. The invariance is the finding.
- **No 간병인사용일당.** The daily indemnity for hiring a carer during a hospital stay shares
  nothing with this product but the word 간병: it is a hospital-days frequency-severity cover
  [R15], out of scope, and its one published rate is a **frequency, not a probability** [S1].

## Inputs are external files

Eight CSVs in `products/long_term_care/`, beside `run.py`, read at run time. The model folder
holds `__init__.py`, `_system.json` and its two Space folders and nothing else — no `_data/`,
no IOSpec, no embedded values — so a diff of the model shows logic changes only. This is the
`annuallife.TradLife_A` layout; contrast `basiclife.BasicTerm_S`, which keeps its inputs inside
the model. The consequence: **the model is not portable on its own.** Copying `LTC_KR_S`
without its parent's CSVs produces a model that reads and then fails on first evaluation.

| File | Reference | Reader | Contents |
|---|---|---|---|
| `model_point_table.csv` | `model_point_file` | `Data.model_point_table()` | nine model points, indexed by `point_id` |
| `mort_table.csv` | `mort_table_file` | `Data.mort_table()` | healthy-life annual `q` by sex and 만나이 30–120 |
| `prevalence_table.csv` | `prevalence_file` | `Data.prevalence_table()` | five sourced 인정률 anchors per sex and the fitted logistic |
| `grade_share_table.csv` | `grade_share_file` | `Data.grade_share_table()` | cumulative grade shares by grade and age band |
| `incidence_table.csv` | `incidence_file` | `Data.incidence_table()` | the disclosed 예정위험률 at three ages by sex |
| `dementia_table.csv` | `dementia_file` | `Data.dementia_table()` | the 치매역학조사 prevalence, its logistic and two sex factors |
| `lapse_table.csv` | `lapse_table_file` | `Data.lapse_table()` | four lapse parameters |
| `av_table.csv` | `av_table_file` | `Data.av_table()` | the 계약자적립액 run-off, four anchors |

**No input file is keyed by the time index `t`**, which is why the move to the 0-based frame
left every CSV byte-identical. The keys are `point_id`, `(sex, age)`, `(grade, age)`,
`(sex, param)`, `param` and `runoff_fraction` — attained ages and parameter names, never
policy months. The time-like *columns* are all inside `model_point_table.csv` and all of them
are **elapsed counts or contract parameters, not positions on the frame's axis**, so none
shifted: `term_age` and `prem_period_years` are contract terms; `annuity_max_mths` (120) and
`annuity_guar_mths` (12) are lengths of the annuity's own ledger measured from each cohort's
certification month `s`; and `wait_mths` (3) and `red_mths` (12) are window lengths measured
from `t = 0`, read as `t < wait_mths()` and `t >= red_mths()`, which are already the correct
0-based boundaries — the 보장개시일 falls at the start of month 3 and the 감액기간 expires at
the start of month 12 on both the old frame and the new one. `av_table.csv`'s
`runoff_fraction` is a fraction of the way from 납입완료 to maturity, not a time index; only
its denominator in `av_pp` moved, from `proj_len() − n_P` to `proj_len() − 1 − n_P`, so that
the fraction still reaches exactly 1.0 on the maturity row.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache; readers placed there would re-read every file for every policy. They
live in the unparameterized `Data` Space instead, and
`test_inputs_are_read_once_not_once_per_model_point` asserts that against the file set in
`kr_registry.INPUT_FILES`. `input_dir()` returns `_model.path.parent`, resolved at run time.

**Every assumption CSV carries a `provenance` column and every cell in it begins with a
citation tag**, `model_point_table.csv` being the only exemption. That escalation of the house
rule is Korea's: when **every** row of every decrement file is a standardization, "the column
is populated" stops being a meaningful check and "the row names its authority" starts being
one.

### `mort_table.csv` is a construction, and two multiples sit on top of it

경험생명표 — the industry experience table, 제10회 applied from 2024-04 — is produced by
보험개발원 and is **not published in full**: only the summary, the 평균수명 and the 기대여명,
is released [REG-R33] [REG-R34], and the single-year 완전생명표 `qx` tables were not retrieved
either [REG-R39]. `mort_table.csv` is therefore a **[std] Makeham-Gompertz construction**,

    q(x) = 1 - exp( -( A + B * c^x ) ),   A = 0.0003 [std],  c = 1.10 [std]

in which `B` is solved per sex so that the complete expectation of life at 65 reproduces the
published 경험생명표 65세 기대여명 — **23.7 years for men and 27.1 for women** [REG-R33] — and
that is the only thing fitted. The construction then reproduces the *second* published summary
statistic without being asked to: the implied 평균수명 at issue age 40 is **86.4** for men
against the published 86.3, and **90.3** for women against 90.7. That is a cross-check on the
shape, not evidence about any insurer's experience, and **no conclusion about Korean insured
mortality should be drawn from the file**. There is no best-estimate factor — the anchor is an
experience statistic, not a valuation margin — which is where this model differs from
`Term_KR_S`, built from disclosed *pricing* rates and carrying a `mort_be_factor`.

Two impaired-life bases sit on top of it as multiples, because **no retrieved source gives a
post-certification mortality table by grade**:

- `care_mort_mult = 3.0` [std]. The yearbook roll-forward and the application-route estimator
  agree that the mean duration of a certification is near **4 to 5.5 years** [R4]
  [R18, derived](#krlib-long_term_care-r18); at 만나이 82 on the shipped table a mean duration of 4.5 years implies a
  force of 0.222 against a healthy 0.075, a multiple of **2.96**. The one study measuring time
  from certification to death — 516.2 days, 8.7% inside a month, 45.6% inside a year [R11] — is
  a **right-censored decedent cohort** and fixes the early shape, not the level. Note the
  coupling: it is also the excess-mortality term of the incidence identity, so it moves entry
  and run-off in **opposite directions at once**, and it is the model's largest quantified
  sensitivity — at 1.0, lifetime lump-sum claims fall 37.7%.
- `light_mort_mult = 1.8` [std], between healthy and care: the mean 인정점수 of certified
  decedents is 82.1, inside 2등급 [R11], so deaths concentrate in the severe grades and a
  light-grade life is healthier than that cohort. **No observed range.**
- `dem_mort_mult = 2.5` [std], for the rider's own ledger. No source gives it.

### Three morbidity files, because it is three different things

- **`prevalence_table.csv`** carries the 연령별 인정률 of the 2024 통계연보 by sex, computed as
  (계 − 등급외) over population [R4 표2-9, 표1-2, derived](#krlib-long_term_care-r4), with the three **[std]** parameters
  of the logistic fitted through them; the five anchors are carried for provenance. Two
  features of the sourced curve survive the fit: a gradient of about 17% per year of age, and a
  **sex crossover at about 70** — the reverse of a death-benefit table, independently confirmed
  by the disclosed 예정위험률 [S1].
- **`grade_share_table.csv`** carries `share_ge`, the share of certified lives at that grade
  **or above**, by grade and age band [R4 표2-9, derived](#krlib-long_term_care-r4), on the six ASCII codes `g1` … `g6`
  that `benefit_grade` selects from.
- **`incidence_table.csv`** carries the disclosed 예정위험률 [S1], the only sourced *incidence*
  here and the only table not used for its level; **`dementia_table.csv`** carries the 2023
  치매역학조사 band prevalences [R7], their fitted logistic **[std]** and two sourced 65+ sex
  factors, read once per model whether or not the rider is on.

### `lapse_table.csv` and `av_table.csv`

`lapse_table.csv` ships four parameters, not a curve, because that is what Korea discloses: the
first-year rate **[std]**, the **0.1%** convergence point at 납입완료 and the **0.8%**
post-완납 ultimate the 2024 계리가정 guidance sets for a 무·저해지 form [REG-R27], and the
표준형 comparison level **[std]**. The durational *shape* between them is the guidance's own
log-linear principle model, applied in `lapse_rate(t)`. The instrument itself was not
retrieved, so the functional form is [unverified] at instrument level [R14, secondary](#krlib-long_term_care-r14) while
the two values are verified from the 보도자료 [REG-R27].

`av_table.csv` is the one file whose numbers are a **carrier's own published figures**: four
환급률 anchors on the 미지급형 at 40세, 90세만기, 20년납, 월납 [S2], doubled because that form
pays 50% of the notional 기본형 value after 납입완료, and indexed on the fraction of the way
from 납입완료 to maturity so one progression serves every term.

## Sign convention

`net_cf(t)` is **income positive**: premiums less every benefit, expense, claim expense and
commission. The technical notes print the same sign, so there is no outgo-positive
`liability_cf` companion. The shape to expect is a deep month-0 strain — 5.2 months of
acquisition expense plus 7.8 months of initial commission against one month's premium — then
thin positive margins for twenty years, then a long negative tail from 납입완료 on.

The model projects **undiscounted gross best-estimate liability cash flows** and nothing else.
The 책임준비금 [REG-R3] [REG-R10], the 해약환급금준비금 [REG-R11], the IFRS 17 CSM and risk
adjustment [REG-R60] and the K-ICS 요구자본 [REG-R13] are cited and left to a layer that
consumes them; `av_pp` and `cv_pp` are published per policy so that layer can be built on them.
The present values in the technical notes are computed outside the model.

## Naming

`lower_snake_case` throughout, reusing lifelib's vocabulary: `pols_*` for policy counts, plural
nouns for cash flows, `*_rate` for rates, `*_pp` for per-policy amounts, `claims(t, kind)` with
an uppercase `kind`, `pols_if_at(t, timing)` for the within-month reads, and `check_*()` with
no argument returning a `bool` beside its per-`t` residual `check_*_resid(t)`.

### The notes' symbols, and where they live

`model.Projection.doc` carries the full table; the load-bearing rows are these.

| Notes symbol | Cells | Meaning |
|---|---|---|
| `t` | the index of `result_cf()` | policy month, 0-based; the frame is `t = 0 … n − 1` |
| `n` | `proj_len()` | the **number** of projected policy months, the frame's exclusive end, `12 × (term_age − issue_age) + 1`; the maturity row is `t = n − 1` |
| `y(t)` | `policy_year()` | the contractual policy year, the derived 1-based label `t // 12 + 1` |
| `x`, `x + floor(t/12)` | `issue_age()`, `age(t)` | 만나이 at the 계약일, attained 만나이 |
| `P`, `n_P` | `premium_mth_pp()`, `prem_period_mths()` | level monthly office premium, paying months |
| `A_B`, `G_B` | `lump_amount()`, `benefit_grade()` | 진단급여금 sum insured, the 등급 threshold |
| `q(x)`, `q_C(x)`, `q_L(x)` | `mort_rate`, `mort_rate_care`, `mort_rate_light` | the three annual mortalities |
| `P(x)`, `P_C(x)`, `P_L(x)` | `prev_rate_at`, `prev_care_at`, `prev_light_at` | prevalence, all grades / at or above `G_B` / below |
| `i_D(x)`, `i_L(x)`, `rho(x)` | `inc_rate_direct_at`, `inc_rate_light_at`, `prog_rate_at` | direct entry, light entry, progression |
| `h`, `l_L`, `l_C`, `l` | `pols_healthy`, `pols_light`, `pols_care`, `pols_if` | the compartments and their sum |
| `n_C(t)`, `S_C(s,t)` | `pols_entry_care`, `care_surv` | entrants at or above `G_B`, care-state survival |
| `CF(t)` | `net_cf` | net cash flow, income positive |

Cells whose names end `_at` and take an **age** — `mort_rate_at_age`, `prev_rate_at`,
`share_ge_at`, `av_ratio_at` — exist because the morbidity construction has to evaluate the
whole basis at 만나이 65 while the life projected is younger. The suffix does two jobs in this
library: `pols_if_at(t, timing)` is the house's *timing*-keyed accessor, used by nine models,
while these are age-keyed; the argument tells a reader which, and no cells takes both.

### Names this product settled, and one it did not

Recorded in `RETIRED_NAMES` so no krlib model reintroduces them; this model is on the right
side of each.

- `prem_int_rate`, not `yejeong_rate` — the 예정이율 is the *pricing* interest rate and must
  not share a name with a declared crediting rate (공시이율), which this product does not have.
- `pols_maturity`, not `pols_expiry`; `surr_chg_pp`, not `surr_charge_pp`; `val_tol`, not
  `value_tol`; `check_net_cf`, not `check_cf_ledger`; `mort_rate_at_age`, not
  `mort_rate_table`; and no `claims` **column** beside the splits, though `claims(t, kind)`
  stays.
- `pols_act` is this model's own name and appears in no other krlib model: it is neither
  `pols_payer` — the lives paying premium and the lives exposed to lapse are the *same* set
  here, and two names would have implied two — nor `pols_healthy`, which excludes the light
  compartment.

The one open item, recorded rather than resolved: this model spells the waiting parameters
`wait_mths` and `red_mths`, following the `_mths` suffix six libraries use in `horizon_mths`,
`prem_period_mths` and thirty others, while `Cancer_KR_S` spells the same two fields
`wait_months` and `reduction_months`. A cross-model review should settle the suffix in one
direction; nothing in either model depends on the answer.

## The identity `check_net_cf()` closes

`net_cf(t)` = `premiums` − `claims_lump` − `claims_annuity` − `claims_dementia` −
`claims_death` − `claims_lapse` − `claims_void` − `claims_maturity` − `expenses` −
`claim_expenses` − `commissions`, read back out of the published `result_cf()` columns so that
a reader adding up the printed statement gets the printed total.

Reading it back out of the frame rather than recomputing it is the point: it catches a benefit
kind that exists in `claims(t, kind)` but was never given a column. Here that is a live hazard
— there are **seven** kinds, two of them (`VOID`, `MATURITY`) mechanisms rather than claims and
one (`DEATH`) not a benefit of the contract at all.

The other five checks:

| Check | What it asserts |
|---|---|
| `check_pols_roll_fwd()` | `l(t) − l(t+1) = deaths + lapses + voids + maturities` — the four ways a life leaves |
| `check_nesting()` | the three compartments are non-negative and add to `pols_if`; `pols_dem` stays inside it |
| `check_ann_ledger()` | `ann_count(t)` equals an independent rebuild that re-derives every cohort's weight from its own age |
| `check_av_continuity()` | the two branches of `av_pp` meet at 납입완료 |
| `check_cv_form()` | `cv_pp` is non-negative, never exceeds the account, and is **identically nil** during the paying period on the 미지급형 form |

All six take no argument, return a real `bool`, and are `True` on every one of the nine shipped
model points. Three close to `roll_fwd_tol = 1e-12`, being identities between policy counts;
`check_av_continuity`, `check_cv_form` and `check_net_cf` close to `val_tol = 1e-6`, because
they compare won amounts of order 1e6 that have been through a `DataFrame` round trip — still
far below the one won a reader adding up the printed statement could see.

One thing no check catches: lapse wrongly applied to the care compartment leaves the
roll-forward consistent and `claims_annuity` unmoved, and shows only as ₩489.73 of surrender
value paid to lives the 약관 forbids from surrendering — which is why `cv_pp` and `pols_lapse`
are read together in the test module.

## Standardizations used

Every row is **[std]** unless the tag says otherwise; the sourced contractual and pricing
parameters live in the other two documents and are not repeated. "Observed range" is what the
retrieved documents actually bound, and here several bound nothing at all — which is said
rather than papered over.

| Parameter | Value | Rationale | Observed range |
|---|---|---|---|
| `care_mort_mult` | 3.0 | at 만나이 82 a mean duration of 4.5 years implies a force of 0.222 against a healthy 0.075, a multiple of 2.96; the duration bracket is 4–5.5 years [R4] [R18, derived](#krlib-long_term_care-r18) | **none published anywhere.** The one decedent-cohort study [R11] is right-censored by construction and fixes the early shape only. Model range 1.0–4.0 moves lifetime lump-sum claims −37.7% to +20.1% |
| `light_mort_mult` | 1.8 | between healthy and care; certified decedents' mean 인정점수 is 82.1, inside 2등급, so deaths concentrate in the severe grades [R11] | none |
| `dem_mort_mult` | 2.5 | between the light and care multiples: a CDR 1 diagnosis is lighter than a 1·2등급 certification | none |
| `direct_entry_share` | 0.20 | the closing assumption of the two-equation, three-unknown identity; the 13.3% / 69.8% first-application split at 1등급 and 인지지원등급 [R4 표2-5, derived](#krlib-long_term_care-r4) | nothing published. 0.05–0.50 moves lifetime benefit outgo +0.7% / −1.8% and the PV ratio 0.4653 → 0.4485: it carries the **timing**, not the level |
| `prog_rate_cap` | 1.0 | a guard rather than an assumption: `rho` cannot exceed a certainty. It does **not** bind on any shipped model point | nothing bounds it, because no source gives a progression rate at all |
| `sub65_age` | 65 | the statutory 노인 boundary, 노인장기요양보험법 제2조제1호 [REG-R54] | statutory, not a choice |
| `disease_share` | 0.95 | the 감액 test is on the **cause**; a 질병 certification inside the window is halved, an 상해/재해 one is not [S4] | the 질병 / 상해 split of certifications is in **no** retrieved source; `red_mths` 0 / 24 bounds the whole mechanic at ±0.02% of lifetime outgo on the anchor cell |
| `red_fraction` | 0.50 | **[S4]**, and invariant wherever a 감액 is stated | 50% in every retrieved document [S1] [S4] |
| `dementia_wait_mths` | 15 | **[S2] [S4]**: a one-year 보장개시일 plus the 90-day persistence test inside the definition of the state | one year is uniform across the market after the 2019 intervention [R10]; the persistence test is 90 days in both retrieved 약관 |
| `prem_int_rate` | 0.02 | **[S1], retrieved**: 「연단위 복리 2.0%」 in a 기초서류 extract | 2.0% [S1] against the cancer chassis's [std] 2.50%; no other Korean 예정이율 for this product class is published [REG-R2] [REG-R48] |
| `surr_chg_ratio`, `surr_chg_years` | 13.0, 7 | the supervisor's rule of thumb for a 보장성보험's 표준해약공제액 [REG-R29], run off over the statutory 해약공제기간 cap [REG-R19 제7-66조제1항](#krlib-reg-r19) | 별표 14's formula is **unusable here**: 별표 15 제9호 excludes 간병 risk premium from the ratio that gives a care-only contract its 보험가입금액 [REG-R21] [REG-R20] |
| `expense_acq_mths` | 5.2 | 13.0 − 7.8, so acquisition plus initial commission is exactly the 표준해약공제액 | no Korean carrier publishes an expense rate at all |
| `comm_init_mths` | 7.8 | 60% of the 13-month 표준해약공제액 — the cap the 2019 사업비·모집수수료 reform sets on annual commission, now 감독규정 제4-32조제8항 [REG-R29] [REG-R22] | the 60% cap is the only published bound; no commission scale is disclosed |
| `comm_renewal_rate` | 0.03 | renewal commission rides on `premiums`, so it stops with the waiver and at 납입완료 | none published |
| `expense_maint` | ₩200 per policy per month | set so the PV of the whole expense and commission basis at the 예정이율 lands on the 20.68% loading `net_prem_ratio()` implies; it lands at 20.26% | none published; the calibration target is itself derived from [S1] and [S2] |
| `expense_claim` | ₩30,000 per claim **event** | first certification, each **annual** survival test, a dementia diagnosis — not per monthly instalment | none published; the unit is higher than a cancer chassis's because the evidence is a 장기요양인정서 produced by a public body |
| `inflation_rate` | 0.02 | the Bank of Korea inflation target, stepping at each 계약해당일 | no Korean expense-inflation assumption was retrieved |
| `prev_ceil`, `prev_beta`, `prev_x_mid` | fitted per sex | three-parameter logistic, least squares through five sourced 인정률 [R4] | refitting the male ceiling at 0.35 / 0.50 / 0.95 moves lifetime outgo −0.3% / +0.5% / −0.3%; **nothing above 만나이 88.5 is sourced** |
| `dem_ceil`, `dem_beta`, `dem_x_mid`, `dem_factor_m`, `dem_factor_f` | fitted; 0.9568, 1.0346 | logistic through five sourced band prevalences, with the **[R7, derived](#krlib-long_term_care-r7)** 65+ sex factors applied flat in age | the fit is out by 31% at the 70-74 anchor, and the sourced sex series crosses over at 80 where the model's factors do not |
| `lapse_year1`, `lapse_level_std` | 0.08, 0.04 | the first-year level and the level of the 표준형 comparison vector, both standardizations | **no Korean durational persistency series for a 보장성 contract was retrieved.** The 표준형 comparison at a level 4.0% changes lifetime benefit outgo by −61.1% |
| `lapse_completion`, `lapse_ultimate` | 0.001, 0.008 | **[REG-R27]**, the guidance's own values for a 무·저해지 form | prescribed; the permitted alternatives (선형-로그, 로그-로그) carry quarterly disclosure of the difference |
| `wait_mths`, `red_mths` | 3, 12 | 90 days and one year on a monthly grid [S2] [S4] | 90 days at three carriers against **180 days** at 우체국, and a one-year 감액 against a **two-year** one — both combinations shipped, the second at model point 9 [S1] |
| processing order | certification, then mortality, then lapse | a life certified in the month is certified before it can die of the state | fixed by the contract's own sequence, not by a disclosure |
| annuity truncation at maturity | instalments stop on the maturity row `proj_len() − 1` | the conservative reading | **no retrieved document resolves it**; understates the benefit for entrants inside the last ten years of term |
| `roll_fwd_tol`, `val_tol` | 1e-12, 1e-6 | count identities against won amounts read back out of a `DataFrame` | both far below one won |

Model point premiums are **inputs**, not assumptions: the two anchors are [S2]-derived — ₩5,600
male and ₩8,400 female, each built from two rows of one published card — and the other seven
sit at approximately the anchor's implied discounted benefit ratio, a configuration choice
recorded in [`technical-notes.md`](technical-notes.md).

## Tests

`tests/test_long_term_care_kr.py` asserts the notes' worked example **hard-coded**, so a
reviewer checks it by eye rather than by re-running the model:

- The anchor cell's derived scalars — `proj_len() = 601` and therefore **601** rows, indexed
  `t = 0 … 600`,
  `prem_period_mths() = 240`, `net_prem_ratio() = 0.7931662309087683`, `comm_init_pp() =
  43,680.0`, `sub65_gradient() = 0.12221178050285361` — and the assumption values the first
  rows use, at the precision the notes print them: `mort_rate(0) = 0.00097601273`,
  `lapse_rate_mth(0) = 0.006924382628299419`, `P(40) = 0.00038039917723430234`,
  `i_D(40) = 0.0000022292964462128687`, `rho(40) = 0.03396845379835368`.
- The `t = 0 … 12` cash flow statement to six decimals and the compartment table to ten,
  including the rows the notes single out: `t = 0`, `t = 1` and `t = 2` carrying a non-zero
  `claims_void` and no other benefit, `t = 3` as the first payable certification, and `t = 12`
  where `claims_lump` steps from 2.198380 to 4.601130 as the 감액 expires while
  `claims_annuity` does **not**, the earlier cohorts being frozen at ₩207,495.74.
- The policy-year-1 aggregate — ₩64,670.302783 of premium against **−₩10,481.095370** of net
  cash flow — the strongest single target in the file, one set of rates driving a whole cycle.
- The milestone rows, the cliff at `t = 240` in particular: `cv_pp(239) = 0` against
  `cv_pp(240) = 654,528.0`, a 환급률 of 48.700000%, and `net_cf` turning from +2,496.2682 to
  −1,284.5196.
- The undiscounted totals — ₩973,533.0572 of premium, ₩268,065.6927 + ₩546,912.1402 of benefit,
  ₩326,783.9323 of 계약자적립액 on death and **−₩448,855.2128** of net cash flow — with the
  cohort decomposition: 0.026808014544 ever certified, 0.354308072159 deaths, 0.435534876925
  lapses and 0.210156424636 reaching the 90세 계약해당일.
- The zero columns asserted **as zeros** rather than left implied: `claims_maturity` at every
  `t`, `claims_dementia` on the seven points where the rider is off, and `claims_lapse` for
  `t < 240` on the anchor cell.

Each of the notes' pitfalls earns a test named after it: that the prevalence-to-incidence ratio
is 10.5× at 65 and 3.8× at 85 rather than a constant; that dropping `mu_bar` inflates the
inflow at 65 by 8.2% while dropping the excess-mortality term cuts lump-sum claims 37.7%; that
`P_C'` needs the full product rule, whose symptom is `claims_lump` falling between `t = 239`
and `t = 240`; that the 감액 is frozen at first certification (₩64.78 on the anchor, ₩1,065.24
at issue age 70); that the annuity's first instalment falls in the month of certification and
`ann_tests` totals 0.0990 against `ann_count`'s 1.4539; that `care_surv` is a partial product;
that premium rides on `pols_act` (₩414.65); that lapse applied to `pols_care` leaves
`claims_annuity` untouched and `check_pols_roll_fwd()` closing while paying ₩489.73 the 약관
forbids; that a certification inside the 보장개시일 window is a decrement; that widening
`benefit_grade` from `g2` to `g5` multiplies benefit outgo by 2.43 rather than scaling one
rate; and that `proj_len()` is a row count and not the last index. The optional modules are
asserted in **both** positions of their switch, and all nine model points are projected end to
end with the six `check_*()` cells `True`.

`tests/test_model_conventions_kr.py` adds the house style, parametrized over
`kr_registry.MODELS` rather than restated here: the two-Space layout, external inputs with no
orphan CSV, the `provenance` column and its citation tag on every assumption CSV, the
docstrings and their required phrases, the 만나이 basis registered for this model, the
`result_cf()` contract — indexed by `t`, contiguous, ending at `proj_len() − 1`, first column
`pols_if`, all names `lower_snake_case` and no NaN — the read-once property, the round trip
through `mx.write_model`, and that every `check_*()` is `True` on **every** model point.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #krlib-long_term_care-r10
[R11]: #krlib-long_term_care-r11
[R15]: #krlib-long_term_care-r15
[R18]: #krlib-long_term_care-r18
[R2]: #krlib-long_term_care-r2
[R4]: #krlib-long_term_care-r4
[R7]: #krlib-long_term_care-r7
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R17]: #krlib-reg-r17
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R39]: #krlib-reg-r39
[REG-R48]: #krlib-reg-r48
[REG-R54]: #krlib-reg-r54
[REG-R55]: #krlib-reg-r55
[REG-R60]: #krlib-reg-r60
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
