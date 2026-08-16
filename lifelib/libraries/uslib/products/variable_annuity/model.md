# Implementation Notes

**Status:** Draft, 2026-08-14. Built from
[`products/variable_annuity/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the 1.30% base contract asset charge, the $35 contract fee, the
> 8.5%→0.0% withdrawal charge scale on Remaining Premium, the excess-withdrawal algebra,
> the $10m benefit base cap, the age-81 GMDB growth cutoff — are sourced from the
> composite specimen, and the rate-sheet parameters are dated **2026-04-27**. Everything
> behavioural and expense-related is a **[std]** standardization, the return path is
> illustrative and the shipped mortality table is *not* a published basis.
> **Guarantee cost cannot be valued deterministically**: VM-21 makes that structural,
> the Alternative Methodology being unavailable to any GLWB block. This model verifies
> the recursion, not the value of the guarantees.

This product sits on the deferred annuity chassis of the library,
[`MYGA_US_S`](../fixed_deferred_annuity/model.md), for **structure** —
the `Data`/`Projection` split, the naming, the timing-argument vocabulary, the result
tables and the roll-forward checks. It deliberately does **not** inherit its mechanics;
see *The chassis' Model #805 floor and MVA are absent by design* below.

## Run it

```bash
python products/variable_annuity/run.py
python products/variable_annuity/run.py 2      # the in-force worked-example cell
python products/variable_annuity/run.py 3      # the decline scenario, to depletion
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/variable_annuity/VA_US_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by projection month `t` with one column
per cash flow line; `result_av()` returns the subaccount and contract value table — the
worked example's own columns — `result_bases()` the guarantee bases, the death benefit
and the two moneyness ratios, and `result_pols()` the in-force movements.

The model and both of its Spaces carry docstrings. `model.doc` describes the product and
the projection basis, `model.Projection.doc` holds the full mapping between the technical
notes' symbols and the cells names, and `model.Data.doc` the input arrangement.

## Monthly, not annual — because there are three clocks

`t` counts **projection months**, and the *policy* month is
`duration_mth(t) = duration_mth_init() + t`. For an at-issue cell the two coincide; for
an in-force cell they do not, and **every calendar test is written on `duration_mth`,
never on `t`**. `policy_year(t) = ceil(duration_mth(t)/12)`, so Contract Anniversaries
fall at the end of policy months 12, 24, … and Contract Quarterly Anniversaries at the
end of policy months 3, 6, 9, …

**Note the contrast with `Term_US_A`, where `t` counts years.** Monthly is forced here
by the notes' own last pitfall, *discretization drift*: the base contract charge accrues
**daily** on separate-account value and is applied at one-twelfth of the annual rate at
each month end **[std]**; the two rider charges are assessed **quarterly** on benefit
bases; and the GMDB roll-up and the GLWB bonus are credited **annually** at the Contract
Anniversary. Three different clocks, and changing any one changes the answer. A test
pins all three.

Within a month the processing order is the notes':

| | |
|---|---|
| BOM | if already depleted, run the post-depletion routine and skip the rest |
| BOM | premium buys units at the prior unit value; `GWB`, `BB`, `NP`, `RP`, `RB`, `GAWA`, `ADJ` all rise |
| BOM | withdrawal: fix the GAWA% if it is the first, split excess from non-excess, charge the CDSC, cancel units, update `GWB`, `GAWA`, `BB` |
| — | unit value growth over the month |
| EOM | rider fees at a Contract Quarterly Anniversary, then the contract fee at a Contract Anniversary, both by pro-rata unit cancellation |
| EOM | at a Contract Anniversary only: the seven guarantee events in order |
| EOM | depletion test |
| EOM | decrements — **death first, then surrender** **[std]** |

## Inputs are external files

The eight input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `VA_US_S/` holds nothing but formulas:

```
products/variable_annuity/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  fund_table.csv
  return_scenario.csv
  rate_scenario.csv
  gawa_pct_table.csv
  cdsc_table.csv
  transaction_table.csv
  run.py
  README.md
  VA_US_S/           <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-contract projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps `input.xlsx` beside the model
and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/` directory
and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for
every model point. They live instead in an unparameterized **`Data`** Space, which
`Projection` references as `data` — so each file is read once per model no matter how
many contracts are projected, and `Projection[1].data is Projection[2].data`.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is read,
so it works wherever the repository is checked out.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `fund_file` | `fund_table()` | `fund_table.csv` |
| `return_scenario_file` | `return_scenario()` | `return_scenario.csv` |
| `rate_scenario_file` | `rate_scenario()` | `rate_scenario.csv` |
| `gawa_pct_file` | `gawa_pct_table()` | `gawa_pct_table.csv` |
| `cdsc_file` | `cdsc_table()` | `cdsc_table.csv` |
| `transaction_file` | `transaction_table()` | `transaction_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `VA_US_S/` without
the CSVs and it will read fine, then fail on first evaluation. What you gain is that a
diff of the model shows logic changes only, and an input can be edited or swapped in place
— point `Data.mort_table_file` at another same-schema file and the projection follows,
with no formula change.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Nine contracts, all on the anchor cell M60 ANB / single Designated Life / NQ / $100,000 / 60-40, differing only in the switches the notes make first-class parameters. **Point 1 is the worked-example anchor**, projected from issue; point 2 is the same carried state entered as an in-force cell; points 3–9 carry depletion, excess withdrawals, the highest-quarterly step-up with the ratchet GMDB, the VIX and CMT variants, the never-withdraw basic-DB cell, the never-withdraw roll-up cell and the *withdrawing* basic-DB cell | contract terms sourced [S1] [S2]; rate-sheet parameters [S3]; behavioural switches **[std]** |
| `mort_table.csv` | Annual mortality by attained age 40–120 and sex, with a `provenance` column | **[std]** illustrative annuitant curve. **Not a published table.** The prescribed basis is the 2012 IAM **Basic** Table improved to 2017-12-31 on Scale G2 [R1] [REG-R59], which may not be redistributed here — swap it in by repointing `Data.mort_table_file`. Do **not** substitute a CSO or VBT life table |
| `fund_table.csv` | Two subaccounts keyed by `(fund_set, sub_id)`: 60% equity at 0.95% p.a. and 40% fixed income at 0.65% p.a. | **[std]**; two subaccounts is the minimum that exercises pro-rata charge allocation, and both expense ratios sit inside the observed 0.52%–2.28% range [S2] |
| `return_scenario.csv` | Gross monthly fund returns keyed by `(scenario_id, sub_id, t)`, read as step functions | **[std]** illustrative. The `base` path is **reverse-engineered** — see below. VM-21 requires a crafted proxy fund per subaccount [R1], so the model takes the series as an input |
| `rate_scenario.csv` | The quarterly average of daily VIX-squared and the 10-year CMT, keyed by `(scenario_id, t)` | disclosed VIX² examples 204.42 and 602.30 [S4]; CMT levels **[std]**. Used only by the two optional variant modules |
| `gawa_pct_table.csv` | The GAWA% grid by attained-age band, Single/Core | sourced [S3], rate sheet dated 2026-04-27 |
| `cdsc_table.csv` | 8.5 / 7.5 / 6.5 / 5.5 / 5.0 / 4.0 / 2.0 / 0.0 % by completed years since receipt, plus a no-charge advisory schedule | sourced [S2]; the `none` schedule **[std]**, observed at [S4] [S7] |
| `transaction_table.csv` | Scheduled premiums and withdrawals keyed by `(txn_id, t)`; scheduled withdrawals **add to** the derived GLWB withdrawal | worked example carries none; the `excess` programme **[std]** |

Every model point projects to completion, and a test asserts it. Between them they
exercise all three GMDB forms, both step-up bases, all three fee-reset rules, both
roll-up rules, both CDSC schedules, both entry modes and both utilization settings — so
no branch of the notes' parameter set is dead code.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE`, and
`MYGA_US_S` wherever the two products share a concept: `pols_*` for policy
counts, `av_*` for account values, plural nouns for cash flows, `*_rate` for rates,
`*_pp` for per-contract amounts, `*_at(t, timing)` for a quantity read at a point inside
the month, plus `model_point`, `age_at_entry`, `sex`, `policy_term`, `proj_len`,
`duration_mth`, `duration`, `age`, `net_cf`, `result_cf`, `check_av_roll_fwd`.

Three of the shared names carry a convention worth stating outright, because on this
product the alternative reading is tempting:

* **`pols_if(t)` is the count in force at the *start* of month `t`** — the notes'
  `l(t−1)` — and is the weight carried by every cash flow on that same row. That is what
  makes the in-force column of `result_cf()` reconcile with the cash flows printed beside
  it: `premiums(t) / premium_pp(t)` is exactly `pols_if(t)`. The notes' own end-of-month
  `l(t)` has not gone anywhere — it is `pols_if_at(t, "AFT_DECR")`, and `result_pols()`
  publishes it as `pols_if_aft_decr` so a row of that table reads across from the opening
  count through the three decrements to the closing one.
* **`lapse_rate(t)` is the *annual* surrender rate and `lapse_rate_mth(t)` the monthly
  one**, matching the `mort_rate` / `mort_rate_mth` pair. Both spellings of the notes'
  `q^w` are present and the suffix is the only thing separating them.
* **`prem_to_av_pp(t)` is the net premium credited to the account value**, the
  per-contract form of `prem_to_av(t)` and the name every account-value model in the
  library uses.

The technical notes use compact actuarial symbols; the full mapping lives in the
`Projection` Space docstring. Seven cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `E(t)` — the **guarantee** excess | `wd_excess_pp` | In `MYGA_US_S` the same name means the **charge** base. Here those are two different quantities and both exist; the charge base is `wd_chargeable_pp`. This is the easiest mistake to make in this library |
| `E(t)` in `Term_US_A` | `expenses` | Expenses there, a withdrawal split here |
| `c(t)` — the CDSC | `wd_charge_pp` | `c(t)` is the Model #805 contract charge on the chassis and conversions in `Term_US_A` |
| `M` — moneyness | `moneyness_glwb` / `moneyness_gmdb` | `M(t)` is the market value adjustment on the chassis. A VA separate account has no MVA at all, so the collision is only in the reader's memory |
| `g` — the GAWA% | `gawa_pct_at_age` | `g` is the monthly nonforfeiture factor on the chassis |
| `b` — the bonus percentage | `bonus_pct` | `b` is the MVA distribution yield on the chassis |
| the charge-free amount | `wd_free_pp` vs `wd_exempt_pp` | See below — two exemptions stack on this product, and only the chassis' one is called `wd_free_pp` |

### `wd_free_pp` is the allowance portion; `wd_exempt_pp` is everything that bears no charge

On the deferred annuity chassis a withdrawal meets exactly one exemption, the free
withdrawal allowance, and `wd_free_pp(t) = min(W, FW)` is the portion it covers. This
product stacks a second one on top: **no CDSC applies to cumulative withdrawals within
`L`** [S1], so the whole non-excess portion is already exempt before the allowance is
reached at all.

The model keeps the chassis' name for the chassis' quantity — `wd_free_pp(t)` is
`min(FW, E(t))`, the part of the *guarantee excess* the allowance covers — and names the
union `wd_exempt_pp(t)`, identically `wd_nonexcess_pp(t) + wd_free_pp(t)`. It is
`wd_exempt_pp`, **not** `wd_free_pp`, that complements `wd_chargeable_pp`, and reading
across the two models without checking which is which will silently understate the CDSC
by the whole non-excess portion. The contract-year cumulative of the allowance used is
`free_wd_used_cum_pp(t)`. A test pins all four relationships on model point 4, the only
cell that takes an excess withdrawal.

## The worked example is a *carried state*, so it is reproduced twice

The notes' worked example is a **single month** — policy month 27, the ninth Contract
Quarterly Anniversary — computed from a state the notes simply state: subaccounts at
66,000 / 44,000, `GWB` = `BB` = 112,500, `RB` = 112,360, `NP` = `RP` = 100,000, no
withdrawals to date. The notes narrate how that state arises (a 6,000 bonus at
anniversary 1 against a contract value of 104,000 that is too low to step up; a second
6,000 bonus at anniversary 2 taking `GWB` to 112,000, then a step-up to the anniversary
contract value of 112,500 which sets `BB` and restarts the Bonus Period) but the two
contract values along the way are marked **[std illustrative]**.

A carried state can be honoured in two ways, and the model ships both:

* **Model point 1 projects from issue.** `return_scenario.csv` carries a `base` path
  reverse-engineered so that `AV(12) = 104,000.00`, `AV(24) = 112,500.00` and
  `AV(26) = 110,000.00` split exactly 66,000 / 44,000 all fall out of the projection.
  The gross returns are therefore ugly numbers (0.6912% and 0.6660% a month over the
  first year, and so on) and are marked **[std] illustrative** with that reason in the
  `provenance` column. What this buys is that the worked-example month is verified
  *together with* every anniversary event that produced its inputs: two bonuses, the
  step-up, the Bonus Period restart, two roll-up credits and eight quarterly fee
  assessments.
* **Model point 2 enters the state directly**, as an in-force cell with
  `duration_mth_init = 26`. The notes' own model point attribute table provides for this
  (`av_initial`, `gwb_initial`, `bb_initial`, `rb_initial` are listed as "currency
  (in-force cells)"), and it reproduces the month without depending on the
  reverse-engineered path at all.

Every worked-example assertion in `tests/test_variable_annuity_us.py` is parameterized
over both readings, and a further test asserts the two agree to the cent. The one
modelling choice the in-force route needs is how to split `av_initial` across
subaccounts: the model uses `alloc[i]` **[std]**, which is exactly right here because the
notes' carried state is at its 60/40 target.

It is worth being precise about *why* it is still at target after twenty-six months,
because the tempting one-line answer is wrong. Pro-rata unit cancellation multiplies each
subaccount by the same `(1 − C / AV)` and so leaves the value weights untouched — that is
the whole reason the unit ledger exists — but **that is necessary, not sufficient**.
Unequal growth moves the weights whatever the charges do. The `base` path is
reverse-engineered so that the two subaccounts also grow at the *same rate net of fund
expense* (that is what the `provenance` column of `return_scenario.csv` means by "paired
with sub_id 1"), and only the two conditions together hold the split at exactly 60/40.
The worked-example month is its own counter-example: `r_1` = +1.20% against
`r_2` = −0.30% takes `w_1` from 0.600000 to the notes' own 0.603519 inside that single
month. A test asserts both halves.

## The chassis' Model #805 floor and MVA are absent by design

`MYGA_US_S` is built around `SB(t) = max(AV + M − C, MGSV)`. None of that
survives the crossing. NAIC Model #805 **expressly excludes variable annuities**
[REG-R42] and reaches a VA only through its *fixed* account under Model #250 §7.B
[REG-R43] — and electing the Roll-up GMDB removes the Fixed Account Options altogether
[S1]. The chassis' own technical notes say so in terms: "The **variable annuity** notes
do not, and must not" reuse the Model #805 construction.

So there is no `mgsv_pp`, no `mva_rate`, no `credit_rate`, and no `surr_value_pp` to
distinguish from `surr_benefit_pp` — the surrender proceeds are `AV(t)` less the CDSC,
with nothing underneath. A test asserts those names are *absent*, so a future consistency
pass cannot quietly add them back.

What replaces them is a **unit ledger** and a **four-base charge stack**: the M&E and
administrative asset charge on account value, inside the unit value; the two rider
charges on benefit bases, by unit cancellation; the contract fee per contract; and the
CDSC on Remaining Premium. The notes call putting the rider fee on account value "the
most common and most consequential error" on this product, and `check_charge_split()`
plus a dedicated test pin the four bases apart.

## `net_cf` is the notes' ledger; `net_cf_ga` is the insurer's own view

The notes' cash flow table lists premium income and every charge income line as
**positive** and the gross death benefit, surrender proceeds, withdrawal proceeds,
post-depletion GLWB payments and maintenance expense as **negative** — and gives no net
row. `net_cf(t)` sums exactly that, with the notes' signs.

It is worth being clear about what that line is not. A VA's separate account is legally
segregated, so `net_cf` mixes separate-account movements (premium in, benefits out) with
transfers into the general account (the charges), and it omits investment return
entirely. It therefore does **not** reconcile to the account value; `check_av_roll_fwd()`
is the identity that does. The insurer's own view — charge income less the general-account
strain (`max(0, guarantee − AV)` on death, plus the insurer-funded post-depletion GLWB
payments) less expenses — is `net_cf_ga(t)`, reported as a memo. The notes are explicit
that the gross benefit and the net strain are both needed and are not interchangeable:
projecting only the strain understates gross outgo and breaks reconciliation with
statutory exhibits, projecting both double counts.

## The notes' ledger double-counts the withdrawal charge

Two rows of the ledger are `Charge income — CDSC | c(t) | +` and
`Withdrawal proceeds | W(t) − c(t) | −`. Taken together they net to `−W + 2c`: the charge
is counted twice. Only one of the two readings can go into a net line.

The model takes the **net proceeds** into `net_cf` — `withdrawals(t)` is
`(W(t) − c(t)) · pols_if(t)`, the notes' `l(t−1)` weight and exactly as the notes define
that row — and reports the charge
separately as `wd_charges(t)`, which is not a `result_cf()` column and is not in
`charge_income(t)`. A test pins both halves. Reading the other way (gross withdrawals
plus CDSC income) gives the same net and would also be defensible; what is not
defensible is adding both rows as printed.

## Bonus, then step-up

The notes are unusually candid here: the research file "does not settle whether the
year-end bonus is credited before or after the anniversary step-up test", and the
**[std]** order (bonus, then step-up) gives `GWB_new = max(GWB_old + bonus, AV)` while the
reverse gives `max(GWB_old, AV) + bonus`, which is strictly more generous. The [std]
choice follows the one design in the set that states the interaction explicitly [S8].

The model implements the notes' order, and the worked example's own narrative confirms
it: at anniversary 2, `106,000 + 6,000 = 112,000` and *then* a step-up to 112,500 — not
`max(106,000, 112,500) + 6,000 = 118,500`. That is a strong check, because the notes'
carried `GWB` of 112,500 is only reachable under the [std] order. **Treat the alternative
as a first-order sensitivity, not a rounding issue:** it moves the benefit base by a full
year's bonus in every ratcheting year, and the notes rank it fourth in their sensitivity
list.

## The GMDB withdrawal adjustment needed a base the notes do not give

The rule is dollar-for-dollar up to `ρ × RB(prior anniversary)` and **proportional above
that, applied at the end of the Contract Year** — not at the withdrawal, because applying
it immediately changes the base the roll-up compounds on. The notes give the
dollar-for-dollar half exactly and describe the other half only as "`RB ×` (proportional
CV reduction from the excess)", with no base stated.

The model accrues the adjustment withdrawal by withdrawal and applies it at the
anniversary: `gmdb_dfd_acc_pp(t)` accumulates the dollar-for-dollar portion against the
year's remaining allowance, and `gmdb_factor_acc(t)` accumulates a proportional factor
measured the same way the GLWB measures its own — against the contract value **after** the
dollar-for-dollar portion has been deducted. That choice is **[std]**, and it is the one
that makes the two adjustments in the contract consistent with each other. It is
signposted in the cells docstring, not buried.

## The `basic` GMDB election and the unreduced `NP` floor

The notes describe the death benefit twice, and the two descriptions disagree.

* The **state table** carries `NP(t)`, "cumulative Net Premiums (a GMDB floor)", updated
  by **premium** and by nothing else, and the death benefit is
  `DB(t) = max(AV(t), NP(t), RB(t))`.
* The **GMDB form table** lists three elective forms, the first of which is *Return of
  premium (proportional)*: `G(t) = G(t−1) + P(1−τ)`, reduced on a withdrawal by
  `G ← G · (1 − W/AV_pre)` — "proportional, **not** dollar-for-dollar", with the emphasis
  in the source.

Under the representative `rollup` election there is no conflict: `NP` is the *included*
return-of-premium benefit that comes with the contract and `RB` is the separately elected
roll-up base, two different guarantees, and `max` of them is what is floored under `DB`.
The model does exactly that.

Under `gmdb_option = "basic"` they are the **same** guarantee — the elected form *is* the
return of premium — and then the two readings cannot both hold. `NP` is the same premium
sum without the withdrawal adjustment, so it dominates the adjusted base at every `t`
after the first withdrawal, and the form table's emphasized proportional rule can never
change a single number. That is not a small effect: on model point 9 the guarantee would
sit at 100,000.00 for ever where the form's own recursion gives 22,540.94 at policy month
240 — a 77,459.06 per-contract overstatement of the floor under `DB`.

The model takes the **elected form as governing**: `gmdb_guarantee_pp(t)` is
`max(NP, RB)` on the `rollup` and `HQAV` elections and `RB` alone on `basic`. The choice
is **[std]** and it is the reading that leaves neither table inert — the alternative
leaves an emphasized contractual rule with no effect and an election that changes
nothing. `np_pp` still carries cumulative net premiums exactly as the state table defines
it, and is still reported in `result_bases()`; it simply is not layered over the form
that already contains it.

Because a cell that never withdraws cannot tell the two readings apart, the model point
table carries **two** `basic` cells: point 7 never withdraws (it is there for the GWB
Adjustment Date and the quinquennial fee increase) and **point 9 withdraws from age 70**,
which is what makes the proportional reduction bite. A test pins the difference, and it
fails against the unreduced-floor reading.

## `pols_maturity` and the horizon — the guarantee outlives the account

The technical notes state no projection horizon, and this contract does not supply one.
Once the contract value is exhausted the For Life Guarantee is a **pure life-contingent
annuity at GAWA**, which the notes rank sixth in their sensitivity list precisely because
the mortality basis then becomes the whole story. Truncating the projection early would
throw away the part of the liability that the notes say matters most.

The model therefore runs to attained age **120 [std]** — `proj_len() = 12 × (120 −
age_at_entry()) − duration_mth_init()`, 720 months on the anchor cell — the terminal age
of the mortality table, where `q = 1`. `pols_maturity(t)` carries the survivors out at
that month and is zero everywhere else, so that

```
pols_if(t) − pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

closes for every `t`. The identity is written on the start-of-month counts `pols_if`
carries: `pols_if(proj_len() + 1)` is zero, every survivor of the horizon month having
left as `pols_maturity`. This is bookkeeping determined by the horizon, not an added
assumption; the name and the construction follow `BasicTerm_S.pols_maturity`,
`Term_US_A` and `MYGA_US_S`.

Worth knowing: **the base run depletes.** On the anchor cell the account reaches zero at
policy month 229, attained age 79 — 5.75% of a benefit base that keeps ratcheting, plus
1.30% on account value and 2.15% on the two bases, against an illustrative 4.4% blended
gross return. From there the ledger is nothing but insurer-funded GLWB payments, and the
rider fees stop exactly when the guarantee starts paying. That is the product, not a bug,
and it is why the notes insist a deterministic run demonstrates the recursion and nothing
else.

## What is not implemented

Named here so the gaps cannot be mistaken for oversights; the model docstring carries the
same list.

- **The stochastic scenario interface.** Real-world and risk-neutral scenario sets, proxy
  fund mapping, and the CTE70 / CTE(98) layers that consume them. Returns come from a
  deterministic scenario table.
- **The Withdrawal Delay Cohort Method and the never-withdraw cohort** (weights 0.20
  non-qualified and 0.05 tax-qualified [R1]). Both need a revised-GAPV construction the
  notes do not supply, and blending cohorts needs parallel projections. The base run's
  single activation age is the notes' own **[std]** alternative.
- **The RMD module.** `L = max(GAWA, RMD)` carries the term but no divisor table is given,
  and the base cell is non-qualified, which is why the spec calls the RMD interaction
  "disclosed but inactive".
- **The combination GMDB** `max(roll-up, ratchet)`. It needs two parallel benefit bases,
  and the notes state neither which component carries the 0.90% charge nor how the
  withdrawal adjustment splits between them. `rollup`, `HQAV` and `basic` are all
  implemented and all three are exercised by a model point — `basic` by two of them, one
  never withdrawing and one withdrawing, because a cell that never withdraws cannot
  exercise the form's proportional reduction at all (see *The `basic` GMDB election and
  the unreduced `NP` floor* above).
- **Premium-tranche CDSC aging.** Remaining Premium is carried as one undifferentiated
  pool and the charge band is read off the contract duration, so a subsequent premium
  does not restart its own charge clock. The notes key the band on completed years since
  receipt of *the premium being withdrawn* [S2], which coincides with the contract
  duration only while the contract is single premium — model point 4 is not: it pays a
  second $25,000 at policy month 73 and is read at that contract's 6-year 2.0% band
  rather than the new tranche's 8.5%. Splitting the pool needs a withdrawal-ordering rule
  across tranches that no retrieved source states. A test pins the divergence.
- **The highest-quarterly step-up adjustment.** `highest_quarterly_CV` takes the highest
  of the four most recent quarterly contract values, *without* the source's adjustment of
  each for subsequent premiums and withdrawals under the dollar-for-dollar / proportional
  rule.
- **The two-table post-depletion payout** [S8]. No Table B values appear in the sources.
- **The Latest Income Date** at owner age 95 [S2] as a forced annuitization. The
  prescribed annuitization assumption is 0% at all projection intervals for a contract
  with no GMIB [R1], and no retrieved document carries an annuity rate table.
- **The charge-increase opt-out**, the terminal illness and extended care waivers,
  spousal continuation, joint-life elections, the transfer charge and the large-contract
  asset charge reduction. All described in the sources; none modelled.
- **`check_margin()`.** The model projects no asset side, so there is no
  charge-versus-cost decomposition to check. `check_av_roll_fwd()`,
  `check_pols_roll_fwd()` and `check_charge_split()` are implemented and all three close
  to floating point. Each takes **no argument and returns a bool** over every projected
  month, following `savings/CashValue_SE`, so one test can call the same check across the
  whole library; the signed per-month residual is `check_av_roll_fwd_resid(t)` and its two
  counterparts, which is what a debugging session wants when a check goes false.

## Standardizations used

Everything in this list is **[std]**: the monthly grid, the BOM/EOM placement of each
step and the quarterly-anniversary calendar; the monthly discretization of the daily
asset charge (`annual/12`) and of the decrements (`1 − (1 − q)^(1/12)`); the decrement
order death → surrender; the 1.00% M&E / 0.30% administrative split of the cited 1.30%
total; pro-rata deduction of the two rider charges, extended from the cited contract-fee
rule; the quarterly frequency of the GMDB charge; the 3.00% guaranteed maximum GLWB
charge; the bonus-then-step-up ordering; the two-subaccount 60/40 allocation and its
0.95% / 0.65% fund expense ratios; the whole illustrative return path, including the
reverse-engineered `base` scenario; the ANB rendering of the 59½ For Life threshold;
activation at attained age 70 at 100% of GAWA, and the withdrawal falling at the start of
each contract year; the premium portion of a withdrawal for the Remaining Premium
roll-forward; the contract-value base for the GMDB proportional adjustment; the reading
that lets the `basic` election's proportional withdrawal reduction bite against the
notes' unreduced `NP` floor; the
`alloc[i]` split of an in-force contract value; capping charges and withdrawals at the
available account value; the half-cent depletion threshold; the post-depletion payment
falling at the start of each contract year; the illustrative mortality table; the 2026
valuation year in the prescribed expense formula; zero acquisition expense and zero
premium tax; and the attained age 120 horizon. The switch settings on the anchor cell —
non-qualified, `rollup` GMDB, `annual_CV` step-up, `commission_7yr` CDSC, `none` fee
reset, `fixed` roll-up — are also **[std]** picks from a genuinely split market, and the
model point table carries the alternatives.

## Tests

`tests/test_variable_annuity_us.py` asserts every row and column of the notes' worked
example — the two subaccount balances at each of the six printed steps, the growth
factors to seven decimals, the pro-rata weights to six, both rider fees, the end-of-month
balances and the `110,463.56 − 604.37 = 109,859.19` trace, all three memo lines
(M&E and admin inside the unit value, the fund expense that is *not* insurer revenue, and
the 724.17 of insurer charge income), the GMDB test with `DB = 112,360.00` and a
guarantee claim of `2,500.81`, the moneyness ratios and the λ = 1.000 multiplier, the
CDSC and free-withdrawal memo, and the GAWA memo — **on both the at-issue and the
in-force reading**, and asserts the two agree to the cent. It also asserts the carried
state the notes narrate at anniversaries 1 and 2, the exact compound roll-up, both
roll-forwards and the charge-split identity at every month, and one test per entry in the
notes' "Known modeling pitfalls" list: gross versus net death claim, the fee stopping at
`AV = 0`, withdrawals measured gross of charges, excess-withdrawal ordering, any
withdrawal killing the year's bonus, the Bonus Period restarting on a step-up, the GMDB
adjustment landing at Contract Year end, age-based rather than duration-based growth
cutoffs, charge-base confusion, the absent fixed account and MVA, the rate-sheet vintage
and the three clocks.

Three further tests pin the library-wide conventions this model shares rather than the
notes' own arithmetic: that every `check_*` is a no-argument bool with a `_resid(t)`
companion; that `pols_if(t)` is the start-of-month count and is the weight on every cash
flow of that row, with `pols_if_at(t, "AFT_DECR")` carrying the notes' `l(t)`; and that
`wd_free_pp` is the free-allowance portion of a withdrawal while `wd_exempt_pp` is
everything that bears no charge.

Three more pin the decisions this README argues out rather than the notes'
worked example: that the `basic` election's proportional reduction actually bites and is
not floored by `NP` (model point 9); that the never-withdraw roll-up cell depletes at
policy month 555 on rider fees alone, which fixes the GAWA% by depletion rather than by a
withdrawal; and that the CDSC band is keyed on the contract duration rather than on the
vintage of the premium being withdrawn, which is a divergence from the notes and is named
as one.

```bash
python -m pytest tests/test_variable_annuity_us.py -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_variable_annuity_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_variable_annuity_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-variable_annuity-r1
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R59]: #uslib-reg-r59
[S1]: #uslib-variable_annuity-s1
[S2]: #uslib-variable_annuity-s2
[S3]: #uslib-variable_annuity-s3
[S4]: #uslib-variable_annuity-s4
[S7]: #uslib-variable_annuity-s7
[S8]: #uslib-variable_annuity-s8
[std]: #uslib-std
<!-- END generated citation links -->
