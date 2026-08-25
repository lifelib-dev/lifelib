# Implementation Notes

**Status:** Draft, 2026-08-20. Built from
[`technical-notes.md`](technical-notes.md); the product it implements is specified in
[`product-spec.md`](product-spec.md). Every parameter value below is one of theirs, and
where this document adds one it says so and tags it **[std]**.

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced; every quantitative input is a standardization. No
> carrier publishes a medical rate table, there is no published morbidity table in Japan
> at all, and 第三分野標準生命表2018 may not be redistributed — so the office premium is a
> model point input, the incidence basis is a construction on public 患者調査 statistics,
> and the shipped mortality file is a documented proxy rather than the real table.
> Replace the assumption tables with company data before drawing any conclusion from the
> output.

`Medical_JP_S` is the executable counterpart of
[`technical-notes.md`](technical-notes.md): a monthly, by-policy projection of gross
best-estimate liability cash flows for third-sector medical insurance (*iryō hoken*, 医療保険).
It is the `jplib` **third-sector chassis** — [`Cancer_JP_S`](../cancer/model.md)
and [`LTC_JP_S`](../nursing_care/model.md) state deltas against the day-limit machinery
here rather than restating it.

---

## Run it

```bash
python products/medical/run.py        # anchor cell, point_id = 1
python products/medical/run.py 4      # another model point
```

`run.py` prints the model point, the first thirteen months of the cash flow statement, the
benefit-day and rider ledgers, the first five policy-year totals, and the seven `check_*`
identities. Its output is ASCII-only so it prints on a Windows console under any code
page: amounts are written "JPY" and the product is romanized.

In a session:

```python
import modelx as mx
model = mx.read_model("products/medical/Medical_JP_S")
model.Projection[1].result_cf()      # the worked example's anchor cell
model.Projection[1].result_days()    # the 通算 ledgers, per surviving policy
```

`Projection[1]` reproduces the worked example of `technical-notes.md` to the precision the
notes display: all four printed monthly rows, every figure of the three prose traces, and
the policy-year-1 aggregate of −¥41,860.47.

---

## Structure

Two Spaces, the house layout. `Data` is unparameterized and holds the five CSV readers and
their filename References, so each file is read **once per model** however many policies
are projected; `Projection` is parameterized by `point_id`, so every `Projection[N]` is a
separate ItemSpace with its own cells cache and readers placed there would re-read every
file for every policy.

`Projection` carries 100 cells and 33 References. `t` is the **policy month**,
`t = 0 … proj_len() − 1`, and month `t` runs from `t` to `t + 1` months after the 契約日.
Premium and maintenance expense fall at the start of the month, benefits and the claim
expense at the end, then mortality, then lapse, then the benefit-driven termination.
Acquisition expense and initial commission fall at `t = 0`.

The horizon is set by the mortality basis, not by a contract term: `proj_len()` is
`12 × (omega_age() − x + 1)`, 924 months on the anchor cell, and `omega_age()` is read off
`mort_table.csv` rather than hard-coded so that replacing the table replaces the horizon
with it. On the 定期 model point flag the horizon is instead the last ten-year renewal
completing by age 80 [S10], and `pols_maturity` carries the survivors out at it. The other
term carrier's 定期医療保険 renews to a higher age [S7], so 80 is that carrier's limit and
not a market-wide one.

### The day-limit machinery is the model

A death-benefit model prices a sum assured; this one prices **frequency × severity ×
limit**. Three limits act in a fixed order and the order is the product:

1. **`L1` inside the stay expectation**, spell by spell — `d_pay_capped(t)`. On the
   anchor's 35–64 length-of-stay row that is 15.20 days against an uncapped mean of 20.20,
   so the 60-day limit removes 24.75% of raw days. Capping the *mean* instead would give
   `min(20.20, 60) = 20.20` and remove the limit silently.
2. **The five-day minimum as an amount, not five days** — `d_ben_capped(t)`. The carriers
   write 「入院給付金日額×5」 [S4] [S6] [S7], so the floor raises the *benefit* and adds
   nothing to the 通算 ledger. With it on, the same row gives 16.10 benefit days against
   15.20 ledger days.
3. **The 通算 limit, per limb, with memory** — `agg_days_dis(t)` and `agg_days_acc(t)`,
   with `d_pay_dis`/`d_pay_acc` capped by the room left and `d_ben_dis`/`d_ben_acc` scaled
   in proportion. Two ledgers, because the 通算 limit runs separately on the 疾病 and
   災害 limbs [S4] [S1]; one combined ledger terminates the contract roughly twice as
   early.

Both day ledgers and the 先進医療 and 入院一時金 ledgers are carried **per surviving
policy** and are never weighted by `pols_if`. A ledger multiplied by the in-force
probability measures the block's consumption rather than the policyholder's and defers the
limit indefinitely; it is the easiest state-variable error in this product, and
`result_days()` is printed unweighted so that the basis is visible.

`term_rate(t)` is the benefit-driven termination — cover ceases when **both** limbs are
exhausted [S9] — and `pols_term(t)` the decrement it produces. On every shipped model
point's expectation it is identically zero: expected paid days run about 0.709 a year at
age 40 and about 15.2 at 90 and over, and the 疾病 limb takes 92% of them, so
`agg_days_dis` reaches about 541 days by the terminal age against its 1,095-day limit
while `agg_days_acc` reaches about 47. That is a property of the expectation, not of the
product, since `E[min(Σ, LA)] ≠ min(E[Σ], LA)`, and the ledgers are implemented anyway
for two reasons. A seriatim or stochastic run needs them — the dispersion an
expected-value grid averages away is exactly what makes `LA` bite. And the
三大疾病無制限 特則 cannot be expressed without them: it takes がん, 心疾患 and 脳血管疾患
days out of the 通算 count entirely, which is a change in *what the ledger counts* and
which defers the benefit-driven termination further still. They are **not** kept for the
dependants: **neither [`Cancer_JP_S`](../cancer/model.md) nor
[`LTC_JP_S`](../nursing_care/model.md) inherits them**, and both document the deletion as
a product fact — [cancer (がん保険)](../cancer/technical-notes.md) has no `L1` and no `LA`,
[nursing care (介護保険)](../nursing_care/technical-notes.md) no `d_pay`, no `d_ben` and no `agg_days_*`
ledger. **Do not delete a ledger because it reads zero.**

One statement here is sharper than the notes'. A ledger advances by
`i(t) × s × min(d_pay, room)` — a *fraction* of the room left, because `i(t) × s < 1` in
every month — so on a deterministic grid it approaches `LA` geometrically and never
reaches it. `term_rate` is therefore **unreachable** on an expected-value projection, not
merely unreached at the anchor cell's parameters. The test suite pins both halves of that:
re-read against a model point whose `LA` is five days and the cap bites in the very first
month — `d_pay_dis` falls from 15.20 to the 5.00 of room left, `d_ben_dis` scales with it,
and the ledger stops just short of the limit instead of overflowing it — while `term_rate`
stays 0 for the whole 924 months. That is `E[min(Σ, LA)] ≠ min(E[Σ], LA)` in its strongest
form, and it is why the benefit-driven termination is a seriatim or stochastic property
rather than an expected-value one.

### Three absences, each a product fact

There is **no death benefit** — the main contract pays nothing on death [S1] [S4] [S6]
[S9] [S10] — so mortality is a pure liability release and no `claims_death` exists. There
is **no 契約者貸付 and no 自動振替貸付** [S1], so nothing carries a policy through a missed
premium and no lapse-suppression term belongs in the recursion; the automatic-premium-loan
machinery of the [whole life savings chassis (終身保険)](../whole_life/technical-notes.md) must **not**
be inherited here. And there is **no
surrender value** under 終身払 at any duration, so `claims(t, "LAPSE")` is identically zero
on eight of the nine model points and the zero column is published rather than dropped.
`cv_pp` exists only because the 65歳払済 short-pay variant acquires 10 × 入院給付金日額 once
the premium-paying period completes [S1] [S6] — model point 4, and the single route by
which this chassis ever has a surrender value at all.

---

## Inputs are external files

CSVs beside `run.py`, read at run time; the model folder holds formulas only — no
`_data/`, no IOSpec, no embedded values. `Data.input_dir()` resolves the directory from
`_model.path.parent`, so the model works from any checkout. The consequence worth knowing
is that **the model is not portable on its own**: copy `Medical_JP_S/` without its
parent's CSVs and it reads cleanly and then fails on first evaluation.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | 9 model points: chassis, 契約年齢, sex, 日額, `L1`, `LA`, premium period, office premium, surgery multiples, and the six rider (*tokuyaku*, 特約), special provision (*tokusoku*, 特則) and switch flags | Contractual columns from the composite [S1] [S4] [S6] [S9] [S10]; the office premium is **[std]** on every row |
| `mort_table.csv` | Annual `mort_rate` by sex and age, 20 to the terminal age (116 male, 118 female) | The library-wide canonical **[std]** construction: log-linear graduation between the 22 sourced anchors read out of 第三分野標準生命表2018, exact at every one of them — 男 q40 = 0.00076 [R4] [REG-R18] [REG-R19] [REG-R20]; **not** a copy — redistribution is prohibited [REG-R21] |
| `lapse_table.csv` | Annual `lapse_rate` by policy year 1–21, last row applying onward | **[std]**, anchored by construction to the 5.6% industry 解約・失効率 [REG-R31] |
| `incidence_table.csv` | 入院受療率 per 100,000 by five-year band, 平均在院日数 by broad band, and the sex factors | All fifteen 受療率 bands sourced [R6] [REG-R26], all four 平均在院日数 bands sourced [R6] [REG-R27]; sex factors **[std]** |
| `los_table.csv` | Five-band length-of-stay distribution per broad age band | **[std]** shape; probabilities solved so each row mean equals the sourced 平均在院日数 [R6] [REG-R27] |

Every row of every assumption table carries a `provenance` column tagging it `[std] …` or
naming the source it came from. Files are UTF-8 without a BOM; headers and every cells
name are ASCII `lower_snake_case`.

**The mortality file is a proxy on purpose.** 第三分野標準生命表2018 is public, free and
machine-readable — the sharp contrast with [uklib](../../../uklib/index.md), which had
to proxy subscriber-only tables — so anyone can retrieve it and check a rate. But the publisher's terms prohibit
reproduction and transmission to third parties without written consent [REG-R21]. `jplib`
therefore **cites** the table by URL, **quotes** the handful of rates the worked example
needs, and **ships** a documented construction over those quoted rates. The construction is
**canonical across the library**: the same file, value for value and provenance string for
provenance string, ships in every `jplib` product that reads a third-sector rate, so the
same cell cannot carry two values in two products. It takes the union of the anchors the
research pass actually read — 22 of them, both sexes, age 0 to the terminal age — and
graduates **log-linearly (geometrically)** between adjacent anchors,
`q(x) = q(a)·(q(b)/q(a))^((x−a)/(b−a))`. Every anchor is reproduced **exactly**, so male
`q40` is exactly 0.00076 and `q` at the terminal age is exactly 1 — which is what closes
the projection horizon — and the curve is locally the Gompertz family the publisher's own
table uses. Each row's `provenance` says which it is: an anchor quotes its rate, an
interpolated row names the two anchors it sits between. Nothing in it is a statement about
Japanese third-sector mortality.

**受療率 is a prevalence, not an incidence,** and `inc_rate_base` is where the model
refuses to confuse the two. The conversion `inc = (juryoritsu / 100,000) × 365 / alos` is
an explicit **[std]** step flagged as needed by the source itself [REG-R26]; at age 40 it
turns the published 0.00258 into 0.046619 a year, a factor of 18.07.

---

## Modules that are off in the base run

Five of the notes' optional constructions are implemented and switched off on the anchor
cell, so the base run reproduces the worked example while the machinery stays visible and
testable. Each is exercised somewhere, and the test suite asserts both positions of each.

| Module | Off position | Switched on |
|---|---|---|
| Anti-selective lapse: `inc_eff = inc × [1 + lam · max(0, w_cum − w_ref)]` on the *morbidity* basis — the reverse of the term-assurance case, where the loading falls on mortality. Both shape and level **[std]**; no Japanese selective-lapse evidence was retrieved | `sel_lapse_lambda = 0`, so the loading is 1 in every month | At the notes' 0.30 the anchor cell's lifetime `net_cf` falls from +¥48,981.58 to +¥16,965.77, two-thirds of the margin |
| 保険料払込免除: an **absorbing** state on the premium-paying population, since the 特定三疾病 特則 waives premiums for life once triggered [S1] and has no recovery limb | Incidence zero unless the 特則 is elected. The base *disability* waiver is zero in **every** run, not only the base one: 第三分野標準生命表2018 excludes 高度障害 [R5] [REG-R20] and no public 高度障害 incidence table was retrieved | Model point 7, at the notes' placeholder `waiver_inc_mult = 0.25 × mort_rate`: 6.9% on waiver at ten years, 94.5% by the horizon |
| The 三大疾病無制限 特則: it does not merely raise the limits — it removes `L1` for がん, 心疾患 and 脳血管疾患 and takes those days out of the 通算 count entirely [S1] [S2], deferring the benefit-driven termination | `share_free()` returns 0 and `d_ben` collapses onto `d_pay` | Model point 4: benefit days per hospitalization 15.20 → 16.70, ledger-consuming days 15.20 → 10.64 |
| 入院一時金特約: ¥100,000 per hospitalization against a 通算50回 count ledger [S1] | `lump_claims_pp` and the count ledger are identically zero | Model points 3 and 7; point 3 pays ¥231,914.26 over the lifetime and reaches a count of 24.91 |
| The age-basis offset: the contract ages on attained age with the fraction discarded (*man-nenrei*, 満年齢) [S4] [S10] while 第三分野標準生命表2018 is built for nearest-birthday (*hoken-nenrei hōshiki*, 保険年齢方式) [R5] [REG-R20], so half a year sits between the projection basis and the valuation basis | `age_basis_offset = 0` accepts the offset **[std]** | 0.5 reads the table at `age(t) + 0.5` by linear interpolation and moves the anchor's lifetime `net_cf` by +¥2,704.33 |

`surg_after_limit` is a switch too, but it is **on** in the base run because it resolves a
genuine **contradiction between carriers** rather than an optional feature: where surgery
is performed during a stay whose day limit is exhausted, one carrier pays at the
in-hospital multiple [S4] and another pays nothing [S10]. The composite pays. Reversed —
model point 5 — the truncated day fraction of 24.75% of in-hospital surgeries falls outside
cover, so the two positions differ by a quarter of the in-hospital surgery benefit and are
not roundable into each other.

### Named and not modelled

The one-month 払込猶予期間 lag and the grace-window claim rule [S1] [S4] [S10]; 復活, which
belongs in the model as a *new model point* because the 責任開始期 resets to the 復活日
[S4] [S9]; 前納 discounting [S4]; catastrophe proportionality [S4]; prospective 支払事由
change on amendment of the 診療報酬点数表 [S2] [S6]; and クーリング・オフ, a pre-inception
decrement [REG-R36]. Each is a **[std scope]** exclusion in the notes and each stays one
here.

---

## Sign convention

`net_cf` is **income positive** — premiums less every benefit limb, less acquisition and
maintenance expense, less claim expense, less commission — which is both the notes' own
orientation and the library-wide convention. The
notes print the stream that way too, so unlike the whole life and payout annuity models
there is no outgo-positive `liability_cf` companion to publish: one stream, one sign, one
name.

The shape to expect is a deep month-0 strain — ¥57,800 of acquisition expense and initial
commission against one month's ¥2,100 premium — then thin positive margins that thin
further with age: the level premium prefunds a morbidity cost that rises for the whole of
life, and year-1 claims are only 21.5% of year-1 premium at age 40.

---

## Naming

Cells names follow lifelib's `basiclife/BasicTerm_S` wherever it has an analogue: `pols_*`
for policy counts, plural nouns for cash flows, `*_rate` for annual rates with `*_rate_mth`
for their monthly companions, `*_pp` for per-policy amounts, `claims(t, kind)` with an
uppercase `kind` string, and `pols_if_at(t, timing)` for the within-month in-force reads.
The technical notes use compact symbols; the full mapping lives in the `Projection` Space
docstring. Six cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `i(t)`, `inc_rate(age)` | `inc_rate_mth` / `inc_rate` | The notes give the *monthly* rate the shorter symbol. A bare `*_rate` is annual across this library and `*_rate_mth` its monthly companion, as `mort_rate` / `mort_rate_mth` already are — exactly the collision the convention exists to prevent |
| `d_pay` vs `d_ben` | `d_pay` / `d_ben` | Two different quantities: ledger days and benefit days, separated by the five-day floor. `check_day_limits` asserts `d_ben ≥ d_pay` in every month |
| `term(t)` | `term_rate` / `pols_term` | The notes' 0/1 indicator is a decrement *rate*, spelled beside `mort_rate_mth` and `lapse_rate_mth`; the count it produces is a different quantity and gets its own name |
| `A_dis`, `A_acc` | `agg_days_dis` / `agg_days_acc` | Spelled out because the unit is **days** and the limb is the whole point of having two of them |
| `V(t)`, `LV` | `adv_paid` / `adv_cap` | A JPY ledger and its cap, named for what they hold rather than for the notes' letters |
| *(no symbol)* | `pols_maturity` | Library-wide, the count whose cover ends at the **scheduled end of the contract**, paid or not; a payment for it would be `claims(t, "MATURITY")`, and this product has none. The 終身 chassis has no scheduled end — the projection stops where the mortality table does and everybody has already died — so the notes need no symbol. The 定期 flag does have one, and without the term the roll-forward would appear to lose lives with no cause in the final month |

Four names are fixed by rulings that run across all nine `jplib` models rather than by
anything particular to this product, and this model carries its share of them:

| Cells | Ruling |
|---|---|
| `expenses` / `claim_expenses` | `expenses(t)` is **acquisition + maintenance only**. The claim handling expense is its own cells, subtracted on its own line in `net_cf(t)` and published in its own `claim_expenses` column of `result_cf()`. `check_net_cf` rebuilds the statement from the two separately, so folding them back together fails it |
| `prem_period_type()` | `prem_period` names a *duration in the model's grid unit* library-wide, and this cells is a category — 終身払 or 65歳払済 — so it is `prem_period_type()`. The model point column keeps the name `prem_period`; only the cells is renamed |
| `mort_rate_at_age(x)` | The table lookup keyed by **age**, beside `mort_rate_base(t)`, the same table rate read in projection month `t`. The old `mort_table_rate` said which file it read rather than what it was keyed by |
| `mort_be_factor` | The multiplier turning the shipped valuation table into the projection basis, in all nine models. `mort_ae_factor` means an actual-to-expected ratio, which is a different quantity and stays in use elsewhere for it |

---

## Standardizations used

Everything the notes mark **[std]** is carried through unchanged: `mort_be_factor` = 1.25,
the
0.92 / 0.08 疾病 / 災害 limb split, `s_ih` = 0.35 and `s_op` = 0.15, `adv_freq` = 0.00040 with
`adv_sev` = ¥150,000 and the 10% / ¥500,000 top-up, the lapse curve, the five-band
length-of-stay shape, the sex factors on incidence, the expense and commission scale, and
the monthly conversions.

Two standardizations are introduced **here** rather than in the notes, because they are
implementation parameters that a document about the product on paper does not need:

1. **`share_3dis` = 0.30 [std].** The share of *hospitalizations* the 三大疾病無制限 特則
   exempts from both day limits. It carries **no observed range**: no cause split of
   入院受療率 was extracted in the research pass [R7] [REG-R33]. It is inert unless the
   特則 is elected, and the base run is bit-identical with it at any value.
2. **The 定期 final expiry age [std].** 「Renewable to age 80」 [S10] is read as *the last
   ten-year renewal whose term completes at or before 80*, so an issue age of 35 expires at
   75. `teiki_expiry_age` and `teiki_renewal_term` are References.

Nothing in `incidence_table.csv` is interpolated: the 概況 publishes 入院受療率 for every
five-year band from 20–24 to 90歳以上, so all fifteen bands the model needs are sourced
row by row [R6] [REG-R26]. Only the sex factors on that table are **[std]**.

The nine office premiums are **[std]** model point inputs. The anchor's ¥2,100 is the
notes' own, sitting between the two public specimen rates for that exact specification
[S8] [S3] and 14.6% above the break-even premium this model's own [std] basis implies; the
other eight sit between 8.6% and 19.7% above their own break-even, so that no shipped model
point projects a lifetime loss on its own assumptions. They are not rates, and no rate
table exists to check them against — the 算出方法書 is a 基礎書類 filed with the 金融庁 and
is not published [REG-R2].

---

## Tests

`tests/test_model_conventions_jp.py` applies the house style: the layout, the
`Data`/`Projection` split, read-once inputs, the docstrings, the naming register, the
`result_cf()` column conventions, that every model point projects without NaN, and the
read → write → re-read round trip.

Seven `check_*` cells assert the identities this product implies. Each takes no argument
and returns a `bool` over all `t`, with the signed per-month residual at
`check_*_resid(t)`; all seven return `True` on all nine shipped model points.

| Check | What it closes |
|---|---|
| `check_pols_roll_fwd` | `pols_if(t) − pols_if(t+1) =` deaths + lapses + benefit-driven terminations + the 定期 flag's scheduled end |
| `check_agg_days` | Both 通算 ledgers advance by exactly the month's ledger-consuming paid days, unweighted by `pols_if`, and neither overflows `LA` |
| `check_day_limits` | The three limits act in order: no expectation exceeds `L1`, benefit days are never fewer than ledger days, and no month consumes more days than its limb has left |
| `check_adv_ledger` | The 先進医療 ledger advances by the reimbursed 技術料 only — not the cash top-up — and never passes ¥20,000,000 |
| `check_lump_ledger` | The 入院一時金 count ledger advances by the month's payments and never passes 通算50回 |
| `check_waiver_roll_fwd` | The 保険料払込免除 state is absorbing and stays in [0, 1] |
| `check_net_cf` | The printed cash flow statement adds to `net_cf`: no benefit limb counted twice or dropped |

The nine model points cover both sexes, issue ages 20 and 80 at the edges, both
per-hospitalization limits, both aggregate limits, the five-day floor, the 10倍 and
in-hospital-only surgery structures, both positions of the surgery-after-limit
contradiction, the 入院一時金 rider, the 三大疾病無制限 特則, the 特定三疾病 waiver, the
65歳払済 short-pay point that is the only one with a surrender value, and the 定期
ten-year-renewable chassis. Model point 1 is the anchor cell and reproduces the notes'
worked example to the precision the notes display.

`tests/test_medical_jp.py` is this model's own suite. It asserts:

- **The worked example, hard-coded** as a module-level table rather than pickled, so a
  reviewer can check it against the notes by eye — all four printed monthly rows to the
  yen-cent and to six decimals of `pols_if`, every assumption value the notes quote before
  the table, the month-0 trace as products rather than totals, the policy-year-1 aggregate
  of −¥41,860.47 line by line on unrounded values, and the closing state at `t = 12`.
  `pols_if(12) = 0.99905 × 0.91` is an exact half-unit tie at six decimals, so the tolerance
  there is a half unit plus the tie, stated in the test rather than hidden in a rounder.
- **Every entry in the notes' Known modeling pitfalls list**, one test each, named after
  the pitfall it protects — fifteen of them, from 受療率 as a prevalence through the
  five-day minimum, the order of the three day limits, the unweighted per-policy ledger,
  the two limbs, radiation folded into 手術給付金, the absent death benefit and surrender
  value, the fixed 型, the age-basis mismatch, the 180-day grouping rule, to monthly
  rounding that does not re-add. Each fails if its pitfall is committed.
- **The roll-forward identities and all seven `check_*` cells on all nine model points**,
  plus the month-by-month residual, the mortality-before-lapse order and `pols_if` as a
  decreasing probability in [0, 1].
- **Each optional module in both positions** — anti-selective lapse off and at 0.30, the
  premium waiver off and elected, the 三大疾病無制限 特則 off and elected, the 入院一時金
  rider off and attached, the age-basis offset at 0 and 0.5, and `surg_after_limit` in both
  of its contradictory readings.
- **The structural product facts**: the horizon set by the mortality table rather than by a
  contract term, the 定期 flag's expiry with no maturity value, the short-pay point as the
  single route to a surrender value, the sex crossover in incidence between ages 30 and 40,
  the benefit-driven termination as a third decrement, the provenance column on every
  assumption row, and that an input can be swapped without touching a formula.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R4]: #jplib-medical-r4
[R5]: #jplib-medical-r5
[R6]: #jplib-medical-r6
[R7]: #jplib-medical-r7
[REG-R18]: #jplib-reg-r18
[REG-R19]: #jplib-reg-r19
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R26]: #jplib-reg-r26
[REG-R27]: #jplib-reg-r27
[REG-R31]: #jplib-reg-r31
[REG-R33]: #jplib-reg-r33
[REG-R36]: #jplib-reg-r36
[std]: #jplib-std
<!-- END generated citation links -->
