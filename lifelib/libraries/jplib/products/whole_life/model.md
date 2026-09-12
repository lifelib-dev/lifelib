# Implementation Notes

**Status:** Draft, 2026-08-20. Built from
[`products/whole_life/technical-notes.md`](technical-notes.md); the product it
implements is specified in [`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the level whole-of-life benefit with no 満期保険金,
> 高度障害 paid at the same amount and inside the same decrement, the 0.70 suppression
> factor and its identity with the premium-paying period, the step at 払込満了, the
> 自動振替貸付 continuation test and its 年8% interest ceiling, the 9/10 and 8/10 契約者貸付
> fractions, and the clawback that keeps the suppressed basis in force where low-period
> premiums went unpaid. Every quantitative assumption is a **[std]** standardization.
> The assumed interest rate (*yotei riritsu*, 予定利率), 予定死亡率 and 予定事業費率 live in the
> filed but unpublished 算出方法書 [REG-R2]; no carrier publishes an expense basis, a
> commission scale or a lapse curve by duration; and the mortality table shipped here is a construction, not the published
> table. Replace them with company data and a real 算出方法書 before drawing any
> conclusion from the numbers.

## Run it

```bash
python products/whole_life/run.py
python products/whole_life/run.py 6      # another model point
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/whole_life/WholeLife_JP_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by the 0-based policy **month** `t` with one
column per cash flow line, `pols_if` first and `net_cf` last; `expenses` there is acquisition plus
maintenance, with the claim handling expense in its own `claim_expenses` column.
`result_pols()` and `result_val()` publish
the decrement and the value runs beside it, the second because the surrender value is
the quantity the whole product turns on and printing it only inside a cash flow is not
enough.

## The time index counts months; the anniversary index beside it counts years

**`t` is 0-based and its unit is the policy month.** `t = 0` is the first policy month,
month `t` runs from time `t` to time `t + 1`, the frame is `range(proj_len())` —
`t = 0 … proj_len() − 1`, so `len(result_cf()) == proj_len()` — and `proj_len()` is the
**number** of policy months projected, `12 (omega_age() − age_at_entry()) + 1`. The
contractual **policy year is the 1-based label `policy_year(t) = 1 + t // 12`**, with
`duration(t) = t // 12` beside it; both are cells of their own, derived and never indexed
by. The 保険料払込期間 `m`, `pua_year`, `pol_loan_year` and the rows of `lapse_table.csv` are
all quoted in policy years, and every comparison against them goes through one of the two.
The attained age is `age(t) = age_at_entry() + t // 12`, so it steps on the anniversary.
`df.groupby(df.index // 12).sum()` reads the statement back by policy year.

**The contractual values stayed on the anniversary index, and that is the point of the
split.** `prosp_val_pp`, `surr_charge_pp`, `pol_val_pp`, `cv_pp`, `cv_pp_susp`,
`reserve_pp`, `cv_mult`, `cum_prem_pp`, `apl_test_val` and `loan_pp` are indexed by the
**anniversary** `d = 0 … proj_years()`, `d = 0` at issue — values *at a 年単位の契約応当日*,
not flows of a period — and **none of their numbers moved** when `t` became a month:
`cv_pp(15)` is the same ¥2,928,631.87 it always was. The construction is calibrated to one
carrier's published **annual** surrender-value run, so re-deriving it monthly would move a
fitted number rather than a modelled one.

What the monthly grid adds is a companion for each: `pol_val_at_m(u)`, `surr_charge_at_m(u)`,
`cv_at_m(u)`, `cv_susp_at_m(u)`, `cv_mult_at_m(u)`, `apl_test_val_m(u)` and
`cum_prem_pp_m(u)` read the same quantities at an **elapsed month** `u`, linearly between
the anniversaries they interpolate **[std]** — the 算出方法書 that would state the real
within-year rule is unpublished [REG-R2] — and each reproduces its annual original exactly
at `u = 12d`. A surrender in month `t` is paid `cv_at_m(t + 1)`, net of `loan_pp(duration(t))`,
the loan balance actually outstanding. `result_val()` is indexed by `d` and not by `t`, so
the two frames cannot be read as one by accident.

## What the monthly grid changed, and what it did not

**Annual, because the contract is.** The policy value construction — `epv_death`,
`annuity_due`, `prem_net_level_pp`, `prosp_val_pp`, `reserve_pp` — and the checks that roll
and close it. The **loan balances**, because the 約款 states a 年利 capitalised at the
契約応当日. And the **APL continuation test**, which is the question an insurer asks when an
annual premium goes unpaid: its cohort index `s` is a policy year, not a month.

**Monthly, because the experience is.** Mortality and ordinary surrender convert on the
effective convention `r_m = 1 − (1 − r)^(1/12)`, so twelve months compound back to the
annual rate exactly and `pols_if(12 j)` is the annual-step model's `pols_if(j)`. Maintenance
expense is a twelfth a month, inflating once a policy year. The **premium**, being 年払, now
falls in one month out of twelve. And the **cliff is one month wide**.

**One ruling changed.** `cv_mult_at_m` ends the suppression at the month the contract ends
it, `u = 12 m`, so eleven of the twelve months of policy year `m` are now paid the suppressed
value and the 15% surge falls in the month **after** the last premium, beside the step that
provokes it. The annual grid had to pay the whole of policy year `m` post-step under a stated
**[std ordering]** rule, because the step and the grid landed on the same year. That is the
largest single difference between the two runs: undiscounted net cash flow on the anchor
cell moves from −¥1,559,835.29 to −¥1,522,509.28, while premium income is unchanged at
¥2,212,542.21.

## No maturity, no tail states, and a horizon that is the table's

There is no
maturity date and no 満期保険金 [S1] [S3] [S5] [S7] [S9] [S10], so the horizon is not the
contract's — it is the terminal age of the mortality table, ω = 109 (M) / 113 (F)
[REG-R18] [R1]. The table's rate at ω is 1, so its monthly equivalent is 1 as well and every
remaining life dies in the **first month** of the terminal policy year; the frame stops
there, at `proj_len() − 1`, rather than carrying eleven rows of zeros after it.
`pols_if(proj_len())` is zero, and nothing is paid at the horizon but the death benefit. On
the anchor cell the frame is `t = 0 … 948`, 949 rows — eighty policy years, twelve months
each, plus the terminal month.

That is what `check_decrement_sum()` asserts: every policy issued leaves by a modelled
decrement, so the deaths, the surrenders, the APL exhaustions and the loan-excess
terminations sum to `pols_if(0)` with no residual population anywhere. On the anchor cell
the split is 0.303360 deaths against 0.696640 surrenders.

The second structural fact is the one a term model does not have: **premiums stop at
払込満了 and nothing else does.** `premiums(t)` is zero once `policy_year(t) > prem_end()` and
so is renewal commission; maintenance expense, death claims, surrender benefits and the cash
value all continue for life — and on the monthly grid that point is made every month rather
than once a year. More than three quarters of the anchor cell's expected death claims fall
from the month `t = 480`, after policy year 40. A projection that ends at 払込満了 misses the
majority of the
liability, and one that keeps charging renewal commission past it charges commission on a
premium nobody pays.

## One policy value, one multiplier

`prosp_val_pp(d)` is the prospective net level premium policy value `W(d)`,
`surr_charge_pp(d)` the 解約控除 `SC(d)` grading linearly to zero at the anniversary `d = m`,
`pol_val_pp(d)`
the ordinary surrender value `V(d) = max(0, W(d) − SC(d))`, and `cv_pp(d)` the amount
actually payable. There is exactly one `V` series in this model and one multiplier on it.
Running two reserve bases, one suppressed and one ordinary, is the notes' third listed
pitfall: at duration 40 the suppressed and the ordinary product have **identical**
surrender values at the one carrier that publishes both [S7].

`cv_pp_susp(d)` is the third quantity the notes need, `k V(d)` at every duration. It is
two things at once — the value an instant before the step at `d = m`, against which
`cv_pp(m)` an instant after must stand in the exact ratio `1 / k`; and the value a
clawed-back APL cohort keeps for life. `cv_mult(d)` returns `k` before the step and 1
after it, with no interpolation of any kind, and on a 終身払 point it returns `k` for
life because the suppressed period has no end date there.

The one anniversary at which the value is not rolled forward is the 払済保険 election at
`pua_year() − 1`, where
`pua_sum_assured()` re-bases the contract onto a single-premium value computed from the
suppressed value at that anniversary. That is a contractual re-basing and not a step of the
recursion, so `check_pol_val_roll_fwd_resid(t)` is defined as zero for the one period that
rolls into it, `t = pua_year() − 2`, rather than forced through it.

The check that ties the value construction to the statutory quantity is
`check_reserve_identity()`, swept over every anniversary `d = 0 … proj_years()`:
`reserve_pp(d) − pol_val_pp(d) = surr_charge_pp(d)`, the whole
difference being the 解約控除 that 平準純保険料式 forbids the reserve to carry [REG-R10]. It
holds **only** because `i_std` defaults to `i_cv`; the current numeric standard
valuation rate (*hyōjun riritsu*, 標準利率) could not be established from any
retrieved official document [R8], and under a deep 逆ざや the ordering
`reserve_pp ≥ pol_val_pp ≥ cv_pp` fails outright. The model therefore never asserts
that ordering, and `reserve_pp` never appears in `net_cf`.

## Lapse is a funded event

`default_rate(t)` moves policies out of the premium-paying cohort into an **APL state**,
not out of the contract. Only the failure of the continuation test terminates them:

    apl_test_val(d + 1) >= loan_apl_pp(d, s) + premium_pp() * (1 + i_loan)

while a premium is due, and `apl_test_val(d + 1) >= loan_apl_pp(d, s)` once none is [S1]
[S3] [S10] — the value at the anniversary the advanced premium would carry the contract to,
against the balance at the anniversary the test is made at. Applying a lapse rate to unpaid
premiums without first running that test models a decrement the contract does not have.

**The whole module is on the anniversary clock**, and stays there on the monthly grid: one
annual premium, one 契約応当日, one test. `default_rate(t)` is accordingly non-zero only in an
anniversary month — a default is the failure to pay one premium on one date, not a hazard
running through a year — and the cohort index `s` is a policy year. What *is* monthly is the
**population**: the cohort on APL is decremented every month like any other in force, and it
terminates in the single month `12 × apl_fail_year(s)`.

The cohorts are indexed by the **entry anniversary `s`** and never collapsed to an average
balance, because the APL exhausts at a duration that depends on when the loan started.
`apl_advances(s)` and `apl_fail_year(s)` publish the two numbers that make the point: on
the anchor cell a default at `s = 1` — the anniversary opening policy year 2 — buys **one**
advance at `k = 0.70` and **thirteen** at `k = 1.00`, from the same default at the same
duration on the same underlying policy value. Model points 5 and 6 are exactly that pair.
`apl_fail_year(s)` and `loan_fail_year()` return an **anniversary**, with `proj_years()` —
one past the last one — as the never-reached sentinel; `apl_fail_month(s)` and
`loan_fail_month()` are the same events on the monthly frame.

Two consequences are wired in and tested. **The advance is not cash income** — an APL cohort
produces no `premiums` entry and no renewal commission, only growth in `loan_apl_pp`, so
`net_cf` is unchanged by an advance in the month it is made. And **the clawback survives the
step**: with `apl_clawback` on, a cohort carried through the low period keeps `k V(d)` for
ever, and the cohort defaulting at `s = 9` exhausts at `d = 52` instead of `d = 68`. Sixteen
years of in force, on one boolean.

## 契約者貸付, and every payment floored at zero

The 契約者貸付 is the same machinery on the paying cohort. `pol_loan_draw(d)` takes the
elected fraction of the value at the anniversary `d = pol_loan_year() − 1`, capped by
`loan_cap_rate` at the contractual 9/10 while premiums are due and 8/10 once 払込済 [S1]
[S3] [S7]; `loan_fail_year()` is the 約款's loan-excess termination. Model point 7 draws
the maximum at the anniversary `d = 39`, which opens policy year 40 — the month `t = 468` —
and terminates decades later, with the benefit floored at **zero**, the loan having consumed
the value. Every payment in this model is
floored: `pol_val_pp`, the death benefit `SA − L` and the surrender benefit `CV − L` can
all go negative in principle and none of them may produce a negative payment.

## Inputs are external files

Three CSVs sit beside `run.py`, outside the model folder, and are read by `Data` **once
per model**.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | 10 model points, indexed by `point_id` | **[std]** cells; the anchor's premium is sourced [S4] |
| `mort_table.csv` | `mort_rate` by `sex` and attained `age` | **[std]** construction anchored on quoted rates [REG-R18] [R1] |
| `lapse_table.csv` | base `lapse_rate` by `policy_year` | **[std]**; industry bound only [R12] [REG-R31] |

**No CSV column is the model's time index, so no CSV value moved when `t` became a month.**
Column by column: `lapse_table.csv`'s key is `policy_year`, a **contractual 1-based label**
whose values stay 1, 2, 3 — `lapse_rate_base(t)` maps through
`policy_year(t) = 1 + t // 12`, so the first twelve projected months read the
`policy_year = 1` row — and its rates stay **annual**, with `lapse_rate_mth(t)` deriving the
month's decrement. `mort_table.csv` is keyed by `sex` and attained `age`, not by time at all.
In `model_point_table.csv`, `prem_term` is a **count** of policy years (0 denoting 終身払) and
is already basis-free; `pua_year` and `pol_loan_year` are **contractual policy-year numbers**,
1-based labels the model compares against `policy_year(t)`; and `issue_age` is an age.
Nothing else in any of the three files carries a time. Every input is quoted in the unit the
contract or the source states it in, and the conversion to a month happens once, in the
projection, where it can be named.

**The mortality table is a construction, and the reason is the licence.**
生保標準生命表2018（死亡保険用）is published in full, free, at a stable public URL — the
sharp contrast with `uklib`, whose CMI tables cannot be read at all without a
subscription. But the publisher's site terms prohibit reproduction, alteration and
transmission to third parties without prior written consent [REG-R21], so this library
must not ship a copy. `mort_table.csv` is the **canonical `jplib` death table**: one file,
built once from the union of the anchors every product in this library sources and shipped
identically by all of them, so a rate quoted in two products carries the same number and
the same provenance in both. This product ships the age range it reads, 15 to ω.

Every row is one of two kinds and its `provenance` says which. An **ANCHOR** row is a rate
quoted and attributed to [REG-R18]; an **INTERPOLATED** row is filled by **log-linear
interpolation in ln `q` between the two neighbouring anchors**, in double precision,
rounded to five decimal places. Nothing is extrapolated — each sex runs from an age-0
anchor to a terminal anchor. Over the range shipped here, **27 of the 95 male rows and 24
of the 99 female rows are anchors**; the other 68 and 75 are the standardization and are
not IAJ values.

How far an interpolated row sits from the published rate is **not known and is not
asserted**: the library reads the anchors and constructs the rest, so it has nothing to
measure the fill against. An earlier revision of this file quoted such a comparison and
has been corrected. A user who has downloaded the IAJ PDF replaces `mort_table.csv` with a
same-schema file and changes no formula.

Expense, commission and interest levels are Projection References rather than a fourth
table, because each is a single scalar: `expense_acq` ¥50,000, `expense_maint` ¥8,000
inflating at `inflation_rate` 1%, `expense_claim` ¥20,000, `comm_init_rate` 0.90,
`comm_renewal_rate` 0.03, `i_cv` 1.468%, `i_std` 1.468%, `i_loan` 2.75%, `acq_dedn_rate`
0.0090.

## Modules that are off in the base run

Six of the notes' optional constructions are implemented and switched off, so the base
run reproduces the worked example while the machinery stays visible and testable.

| Module | Switch | Off value | Exercised on | What it does |
|---|---|---|---|---|
| Premium default and the 自動振替貸付 | `default_rate` | `0.0` | points 5, 6 | Moves policies out of the paying cohort into an APL state at 1% p.a. **[std]**, and terminates them only when the continuation test fails. Points 5 and 6 run it on the suppressed and the ordinary form of the same policy |
| 契約者貸付 | `pol_loan_util` | `0.0` | point 7 | A single capped drawdown at the anniversary opening the policy year `pol_loan_year` **[std]**, at the contractual 9/10 while premiums are due and 8/10 once 払込済. Point 7 draws the maximum at the anniversary `d = 39`, which opens policy year 40, and reaches the loan-excess termination decades later, with a zero benefit |
| Dynamic surrender on the 払戻率 | `dyn_lapse` | `False` | point 8 | Multiplies the lapse rate by `min(3, max(1, 1 + β(CV/cumprem − 1)))` with `β = 2` **[std]**. The value-to-premiums ratio crosses 1 exactly at the cliff, so with `lapse_spike` also at zero the surge at 払込満了 is produced endogenously — the factor steps 1.0000 → 1.2318 there — rather than imposed |
| The cliff surge | `lapse_spike` | `0.15` **[std]**, and `0.0` on point 8 | point 8 (off) | A **one-off proportion** of the survivors of the single month `t = 12m`, the month after the last premium, applied through `lapse_spike_rate(t)` and never converted to a monthly rate — it is a decision taken on a date, not a hazard running through a year. The step in `cv_at_m` is contractual; the surge at the step is behavioural and nothing in any retrieved document quantifies it. The two must not be confused, which is why the surge is a cells of its own, outside `lapse_rate`, and one point runs without it |
| 払済保険 conversion | `pua_year` | `0` | point 4 | Stops the premium, re-bases the sum assured to `(CV(d) − L(d)) / A(x + d)` at the conversion anniversary `d = pua_year() − 1` and drops the 解約控除. The conversion is made on the suppressed value, so the 払済保険金額 is permanently smaller: ¥4,700,513 against an original ¥10,000,000 |
| 5年ごと利差配当 | `dividend_type` | `none` | point 9 | Declares `div_spread × div_period × pol_val_pp(y)` in the **last month** of every fifth policy year — `t = 59, 119, 179, …` — with `div_spread` = **0.25% p.a. [std]** and `div_period` = **5**. The composite is 無配当; the declaration rate is a 三利源 calculation inside the unpublished 算出方法書 and no carrier publishes it, so the spread is **[std]** — the five-year period is not, it is in the product name [S7] [S10] |

The `apl_clawback` Reference is a seventh switch and is the only one that ships **on**,
because on it is the correct treatment: a cohort carried through the low period by
unrepaid advances has not paid those premiums, which is the contractual trigger. It is
still switched in testing, because switching it moves the exhaustion of the cohort
defaulting at `s = 9` from the anniversary `d = 52` to `d = 68`.

`mort_be_factor` is the last lever, 1.00 on every point but 9. **At 1.00 the base run is
a valuation-table run, not a best estimate** [REG-R20]. The terminal rate is held at 1
whatever `mort_be_factor` is set to, because `omega_age` is the table's horizon and not an
experience assumption.

Not implemented, and stated as absences rather than gaps: reinstatement (**復活**), which
understates later-duration in force and therefore both premium income and claims, because
no retrieved source gives a reinstatement rate; **前納**, which changes the premium stream
without changing any mechanic this chassis exists to demonstrate; **リビング・ニーズ**, which
accelerates the death benefit and reduces `SA` by what it pays, so modelling it as an
addition would double-count; and **免責 incidence**, where a refused claim pays the
保険料積立金 to the policyholder rather than nothing [S1] [S9] [S10].

**Sum-assured reduction (*gengaku*, 減額) is not implemented either, and the absence is
worth its own paragraph** because it is the one in-scope contractual option on this
chassis that no model in the library implements. `product-spec.md` records it as universal
and as treated by contract as a **partial surrender**: the reduced portion is cancelled and
pays the surrender value attaching to it, the remainder continuing on a smaller `SA` at a
smaller premium [S1] [S3] [S9] [S10]. The same is true of the two savings products that
inherit this chassis — the [endowment (養老保険)](../endowment/product-spec.md) and the
[FX whole life (外貨建終身保険)](../fx_whole_life/product-spec.md) specify it the same way — so all three
savings specifications carry it in scope and none of the three models moves a policy
through it. Nothing in the model rejects a 減額 input: there is no such input to reject.
Modelling it would need a partial-decrement state, because a reduced policy is neither
fully in force nor fully surrendered, and no retrieved source gives a 減額 election rate to
drive it. The consequence for the shipped numbers is one-directional and small in the base
run, which carries no elections at all: where policyholders reduce rather than surrender,
this model books the whole policy as a surrender or none of it, so it overstates the
variance of the surrender stream while leaving its expected level alone.

## Sign convention

The notes' `CF(t)` is already **income positive** — premiums less claims, expenses and
commission — which is the library-wide sign of `net_cf`, so there is no outgo-positive
`liability_cf` companion to publish: one stream, one sign, one name.

That the published statement adds up is `check_net_cf()`, with the per-`t` signed residual
at `check_net_cf_resid(t)` — the library-wide name for this check on every model. It sums
the `result_cf()` columns of a row against that row's `net_cf`, so a third benefit kind
added to `claims` and left out of the statement shows up here rather than vanishing from
it. `result_cf()` publishes `claims_death` and `claims_lapse` and no bare `claims` column,
so the columns sum to `net_cf` with nothing to skip.

## Naming

Cells names follow lifelib's `basiclife.BasicTerm_S` and `savings.CashValue_SE` wherever
those models have an analogue: `pols_*` for policy counts, plural nouns for cash flows,
`*_rate` for rates, `*_pp` for per-policy amounts, `claims(t, kind)` with an uppercase
`kind` string, `pols_if_at(t, timing)` for the within-year in-force reads. This is a cash
surrender value and not an account value, so it is `cv_pp` and there is no `av_pp`
anywhere. `lapse_rate` is the annual rate, as on every annual-grid model in the library.

The technical notes use compact actuarial symbols; the full mapping lives in the
`Projection` Space docstring. Six cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `l(t)`, `lp(t)` | `pols_if` / `pols_pay_bef_decr` | Two populations, and the difference is the APL cohort. `pols_if` weights maintenance expense and every benefit; `pols_pay_bef_decr` weights **premium and renewal commission**, because an APL advance is a loan asset and not cash income. They coincide in the base run, where nothing defaults, which is exactly why the notes now carry `lp(t)` as a symbol of its own |
| `V(d)`, `CV(d)`, `k V(d)` | `pol_val_pp` / `cv_pp` / `cv_pp_susp` | Three names for one series and one multiplier, all indexed by the **anniversary** `d` rather than the month `t`. `cv_pp_susp` exists because the notes need `k V` at *every* duration — as the value an instant before the step, and as the value a clawed-back APL cohort keeps for life |
| (between anniversaries) | `*_at_m(u)` | Every value cells has a monthly companion — `pol_val_at_m`, `cv_at_m`, `cv_susp_at_m`, `cv_mult_at_m`, `surr_charge_at_m`, `apl_test_val_m`, `cum_prem_pp_m` — reading the same quantity at an elapsed month **[std]**. The suffix is the warning: `cv_pp(d)` is what the contract defines at an anniversary, `cv_at_m(u)` what this model pays someone who surrenders between two |
| `w(t)`, `s(t)` | `lapse_rate` / `lapse_rate_mth` / `lapse_spike_rate` | The ordinary surrender rate is annual with a monthly companion; the cliff surge is neither, and is deliberately **not** inside `lapse_rate`, where the annual grid had to put it |
| `L(d)` | `loan_pp` / `loan_apl_pp(d, s)` | One symbol, two objects: the paying cohort's 契約者貸付 and the APL balance of the cohort entering at anniversary `s`, both at an anniversary. Collapsing them to one name hid the fact that the APL exhausts at a duration that depends on `s` |
| `m` | `prem_term` / `prem_period` / `prem_period_months` / `prem_end` | `prem_term` is the model point column, with **0 denoting 終身払**; `prem_period` is the effective number of years, `proj_years()` on a 終身払 contract; `prem_period_months` is `12 m`, the month 払込満了 falls at; `prem_end` is the last **policy year** a premium is actually due, which a 払済保険 election moves |
| `E0`, `e(t)`, `ec` | `expenses` / `claim_expenses` | `expenses` is **acquisition plus maintenance only**; the claim handling expense is `claim_expenses`, deducted explicitly in `net_cf` and published as its own `claim_expenses` column. That is the settled meaning across the three libraries, so an `expenses` column means the same thing in all of them |
| `mort_be_factor` | `mort_be_factor` | The cells carries the library-wide name for the multiplier turning the shipped valuation table into the projection basis. The model-point **column** keeps its own spelling, `mort_adj`, so a CSV written against an earlier revision still loads |

## Standardizations used

Every one is tagged **[std]** at its cells and in `technical-notes.md`: the cash-value
basis rate `i_cv` = 1.468% and the acquisition deduction `α` = 0.0090, both solved
against one carrier's published surrender table [S4]; `i_std` defaulting to `i_cv`; the
mortality interpolation and the reading of the table at the attained age (*man-nenrei*, 満年齢)
with no nearest-birthday insurance age (*hoken-nenrei*, 保険年齢) adjustment; `mort_be_factor` = 1.00; the lapse curve 4% / 3% / 2% and the 15% cliff
surge; the **effective** monthly conversion of the annual decrement rates, and the **linear
interpolation of the policy value between anniversaries**, which is the one convention the
monthly grid needs and the contract does not publish [REG-R2]; `default_rate` = 1% in the
module, applied once per premium; the APL test read at the next anniversary's value, the
clawback treatment of the defaulting cohort, and no notice-and-top-up period; the 契約者貸付
as a single capped drawdown at an elected anniversary; expense and commission levels and the
1% expense inflation, stepped once a policy year; the surrender expense folded into
maintenance; death before lapse as the processing order; the 0.25% dividend spread (its
five-year period is sourced, not standardized [S7] [S10]); and the premium scale for
every cell but the anchor.

The anchor's premium is sourced — 12 × a published monthly premium for exactly that cell
[S4] — and the other nine are solved from it by one rule **[std]**. A suppressed cell is
priced at the anchor's own ratio of gross premium to net level premium, ¥174,960 /
¥176,618.83 = 0.990608, applied to that cell's `prem_net_level_pp()`; an ordinary cell
divides that by the **83.7%** the one carrier publishing both scales for one identical
model point discloses [S7]. Points 2, 4 and 10 are priced that way, and point 2 is the
anchor's own ordinary twin at ¥209,032 — the same trade the suppressed form makes, at the
sourced price.

**Point 6 is the one exception, and it is deliberate.** It is the ordinary form of the
anchor held at the anchor's *suppressed* premium of ¥174,960, not at the ¥209,032 the rule
would give it, so that points 5 and 6 differ in `k` and in nothing else. That is what makes
"one advance against thirteen" a statement about the suppression rather than about two
different prices. Point 6 is therefore a controlled comparison and not a priced product;
point 2 is the priced ordinary twin. The whole rule, exception included, is asserted in
`tests/test_whole_life_jp.py` on all ten points, so a premium edited into the CSV by hand
fails the suite rather than drifting quietly.

## Tests

`tests/test_whole_life_jp.py` holds the notes' worked example **hard-coded as a
module-level table** — the eight cash-flow rows, the eight surrender values, the
calibration triple, the eight-point fit, the undiscounted totals and the decrement split
— so that a reviewer can lay it beside the notes and compare by eye. Money is asserted to
the yen-cent, in-force to six decimals and the decrement totals to nine, which is the
precision the notes display. The cash-flow goldens are keyed by the 0-based **month** `t`
(rows 0, 1, 2, 11, 12, 179, 180, 181) and the surrender-value goldens by the anniversary `d`
(1 … 5, 14, 15, 16) — the second set unchanged from the annual-step model, because the value
construction did not move; the frame assertion is
`list(df.index) == list(range(949))`, ending at `proj_len() − 1`.

Every entry in the notes' **Known modeling pitfalls** list has a test of its own, named
after the pitfall, because each of them is a way an implementation can look right and be
wrong: the cliff as a step rather than a ramp and its exact `1 / k` ratio; its absence on
the 終身払 point; the policy-year-`m` surrender paid on the full value with both values still
published; one policy value and one multiplier, shown by running points 1 and 6 side by
side; the eleven months of policy year `m` that are now paid the suppressed value and the
one that is not; lapse as a funded event; the advance that is not cash income; the APL test on the
suppressed value, one advance against thirteen; the clawback's sixteen years; premiums
stopping where nothing else does; the horizon at ω on both sexes; 高度障害 inside the
death rate and リビング・ニーズ as an acceleration; the zero floor on every payment; and
`reserve_pp` against `cv_pp`, including that the identity is withdrawn rather than forced
when `i_std` is moved off `i_cv`.

Two further tests are about the **conversion** rather than about the product: that twelve
monthly decrements compound back to the annual rates exactly, and that the anniversary
values — `pol_val_pp`, `cv_pp`, `reserve_pp` — are the same numbers the annual-step model
published, which is what makes the two runs comparable.

Beyond those: all six `check_*` identities on all ten model points, the roll-forward and
decrement-sum identities rebuilt independently of the recursions, each optional module in
**both** positions, the `result_cf` column vocabulary, the docstrings against the
structure they describe, the CSVs' encoding and the mortality table's row-by-row
provenance, an input swapped by repointing a filename Reference, and a
read → write → re-read round trip against the same golden values.

```bash
python -m pytest tests/test_whole_life_jp.py -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-whole_life-r1
[R12]: #jplib-whole_life-r12
[R8]: #jplib-whole_life-r8
[REG-R10]: #jplib-reg-r10
[REG-R18]: #jplib-reg-r18
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R31]: #jplib-reg-r31
[std]: #jplib-std
<!-- END generated citation links -->
