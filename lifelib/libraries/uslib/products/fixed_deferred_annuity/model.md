# Implementation Notes

**Status:** Draft, 2026-08-14. Built from
[`products/fixed_deferred_annuity/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the 4.45% declared rate, the 0.25% GMIR, the 2.80% GMSV rate,
> the 9/8/7/6/5 surrender charge, the 10% free withdrawal, the linear-duration MVA and
> its symmetric cap, and the NAIC Model #805 floor — are sourced from the composite
> specimen. Every behavioural and expense assumption is a **[std]** standardization
> introduced for the reference implementation, and the shipped mortality table is
> illustrative, *not* a published basis. Replace them with company data before drawing
> any conclusion from the numbers.

This is the **deferred annuity base chassis** of the library. The fixed-indexed annuity,
variable annuity and registered index-linked annuity models reference the surrender
benefit composition order and the Model #805 floor construction implemented here rather
than restating them.

## Run it

```bash
python products/fixed_deferred_annuity/run.py
python products/fixed_deferred_annuity/run.py 2      # the stress model point
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/fixed_deferred_annuity/MYGA_US_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by policy month `t` with one column per
cash flow line; `result_av()` returns the account value and Model #805 floor table — the
first five of its columns *are* the notes' worked example — and `result_pols()` the
in-force movements.

The model and both of its Spaces carry docstrings. `model.doc` describes the product and
the projection basis, `model.Projection.doc` holds the full mapping between the technical
notes' symbols and the cells names, and `model.Data.doc` the input arrangement.

## Monthly, not annual

`t` counts **policy months**, 1-based, and `policy_year(t) = ceil(t/12)`, so anniversaries
fall at `t = 12, 24, …` and the five-year guarantee period ends at `t = 60`. **Note the
contrast with `Term_US_A`, where `t` counts years.** The contract credits interest daily
against a quoted *annual effective* rate, while surrender charges and the MVA step on
contract-year boundaries; monthly is the coarsest grid that resolves both. It hits every
anniversary exactly and puts the guarantee-period-end window and the shock-lapse boundary
within one step. Finer grids buy nothing on a book-value chassis with no daily-valued
index.

Twelve monthly factors `(1 + i_cr)^(1/12)` reproduce the declared annual effective rate
**exactly** — `av_pp(12) == 100,000 × 1.0445` to the twelfth significant figure — so the
discretization moves interest only *within* a month. Do not compound daily as well; a test
pins this.

Within a month, the notes' processing order is: BOM — roll the free-withdrawal counters,
apply the guarantee-period boundary, take the elective withdrawal, take annuitization
elections, update the IRC §72 tax basis; EOM — credit interest, roll the Model #805 floor,
apply decrements in the order annuitization, mortality, surrender **[std]**, with every
decrement benefit valued on the post-crediting account value.

## Inputs are external files

The seven input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `MYGA_US_S/` holds nothing but formulas:

```
products/fixed_deferred_annuity/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  surr_charge_table.csv
  surr_charge_age_cap.csv
  rate_scenario.csv
  withdrawal_table.csv
  mva_factor_table.csv
  run.py
  README.md
  MYGA_US_S/      <- formulas only
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
ItemSpace with its own cells cache. Readers placed there would re-read every file for every
model point. They live instead in an unparameterized **`Data`** Space, which `Projection`
references as `data` — so each file is read once per model no matter how many contracts are
projected, and `Projection[1].data is Projection[2].data`.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is read,
so it works wherever the repository is checked out. Each table has a filename Reference and
a reader Cells, both on `Data`:

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `surr_charge_file` | `surr_charge_table()` | `surr_charge_table.csv` |
| `surr_charge_age_cap_file` | `surr_charge_age_cap_table()` | `surr_charge_age_cap.csv` |
| `rate_scenario_file` | `rate_scenario()` | `rate_scenario.csv` |
| `withdrawal_file` | `withdrawal_table()` | `withdrawal_table.csv` |
| `mva_factor_file` | `mva_factor_table()` | `mva_factor_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `MYGA_US_S/`
without the CSVs and it will read fine, then fail on first evaluation. What you gain is
that a diff of the model shows logic changes only, and an input can be edited or swapped in
place — point `Data.mort_table_file` at another same-schema file and the projection follows,
with no formula change.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Seven contracts, all on the anchor cell M60 ANB / NQ / $100,000 / 5-year period, differing only in the switches the notes make first-class parameters. **Point 1 is the worked-example anchor**; point 2 is the same contract on the 10% stress reference yield; points 3–7 carry Camp B, the registered-contract conventions, the net-of-charges MGSV convention with its interest-only free withdrawal and interest-credited cap [S5] [S6] [S8] [S9], the asymmetric cap and the declared-differential MVA | contract terms sourced [S10] [S11]; behavioural switches **[std]** |
| `mort_table.csv` | Annual mortality by attained age 40–120 and sex, with a `provenance` column | **[std]** illustrative Makeham annuitant curve. **Not a published table.** The prescribed basis is 2012 IAM **Basic** with Projection Scale G2 and the VM-22 Table 6.7 factors [R2 §6.B.8](#uslib-fixed_deferred_annuity-r2) [R9], which may not be redistributed here — swap it in by repointing `Data.mort_table_file` |
| `surr_charge_table.csv` | The initial and renewal schedules, keyed by `(schedule, contract_year)` | initial 9/8/7/6/5 sourced [S10]; renewal 5/4/3/2/1 sourced [S2], adoption **[std]** |
| `surr_charge_age_cap.csv` | The attained-age cap on the renewal charge, 4% at 94 down to 0% at 98–100 | sourced [S1] [S2] |
| `rate_scenario.csv` | Three deterministic scenarios keyed by `(scenario_id, t)`, read as step functions: `base` (it = 6.50%, MR = CR = 4.45%), `stress` (it = 10.00%) and `differential` (MR = 6.00%) | **[std]**; the index is a state-filed variable [S8] [S12], so the model takes a scalar series rather than hard-coding one |
| `withdrawal_table.csv` | Three withdrawal programmes keyed by `(wd_schedule_id, t)`: the worked example's $4,000 at month 13, an empty one, and one charged excess withdrawal | worked example [S10] [S11]; the variant **[std]** |
| `mva_factor_table.csv` | The declared-differential duration factors `F_s` by whole years remaining, both rate columns | specimen table [S14] |

Every model point projects to completion, and a test asserts it. Between them they exercise
**all three MVA formula families, all five cap rules, both renewal architectures, both
Model #805 withdrawal conventions, both free-withdrawal rules and both settings of
`free_wd_mva_exempt`** — the notes' own headline finding is that the cross-carrier
divergence lives in exactly those switches, so none of them is dead code.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE` wherever those
models have an analogue: `pols_*` for policy counts, `av_*` for account values, plural nouns
for cash flows, `*_rate` for rates, `*_pp` for per-contract amounts, `*_at(t, timing)` for a
quantity read at a point inside the month, plus `model_point`, `age_at_entry`, `sex`,
`policy_term`, `proj_len`, `duration_mth`, `duration`, `age`, `net_cf`, `result_cf`,
`check_av_roll_fwd`.

The technical notes use compact actuarial symbols instead; the full mapping lives in the
`Projection` Space docstring. Six cases needed care, and every one of them is a collision the
notes themselves carry:

| Notes | Cells | Why |
|---|---|---|
| `d(t)` — the floor deduction | `mgsv_wd_deduct_pp` | `d(t)` is deaths in `Term_US_A`; here it is the withdrawal deducted from the Model #805 floor in step 7 |
| `c(t)` — the contract charge | `mgsv_charge_pp` | `c(t)` is conversions in `Term_US_A` |
| `E(t)` — two different bases | `wd_excess_pp` / `surr_excess_pp` | The excess of a *withdrawal* over the allowance and the excess of the whole *account value* over it are both written `E(t)`; `E(t)` is also expenses in `Term_US_A`, here `expenses` |
| `X` — the lapse exponent | `lapse_dyn_exponent` | `X(t)` is premium tax in `Term_US_A`, here `premium_taxes` |
| `T(t)` — the MVA duration | `mva_term` | `T` is in years while `t` is the policy month |
| `MGSV` / `GMSV` / `MGV` | `mgsv_pp` | One concept, three labels across the sources; MGSV is the library's term |

Two further names carry a **library-wide** convention that does not follow the notes'
indexing, and in both cases the notes' own quantity survives under a second name rather
than being dropped:

| Notes | Cells | Why |
|---|---|---|
| `l(t)` — end-of-month in-force | `pols_if(t)` is the **start**-of-month count; the notes' `l(t)` is `pols_if_at(t, "AFT_DECR")` | `pols_if(t)` is the weight applied to month `t`'s cash flows, so the `pols_if` column of `result_cf()` reconciles with the row it sits on — `withdrawals(t) / wd_payment_pp(t)` and `expenses(t) / ((expense_maint/12) × inflation_factor(t))` both return it. This matches `Term_US_A` (`pols_if(1) == pols_if_init()`) and `CashValue_SE`. `pols_if(t+1) == pols_if_at(t, "AFT_DECR")` in every month but the last |
| `w(t)` monthly, `w_annual(t)` annual | `lapse_rate_mth` / `lapse_rate` | `lapse_rate` is the **annual** rate everywhere in the library, pairing with `lapse_rate_mth` exactly as `mort_rate` pairs with `mort_rate_mth`. The notes already carry both quantities; only the suffixes move |

The roll-forward self-checks follow `CashValue_SE`: `check_av_roll_fwd()` and
`check_pols_roll_fwd()` take **no argument and return a bool** over every projected month,
so one test can call the same check across every model in the library. The signed per-month
residual — genuinely more useful once a check has failed — is `check_av_roll_fwd_resid(t)`
and `check_pols_roll_fwd_resid(t)`, and the bools are defined in terms of them against the
tolerances `check_tol_av` (1e-6) and `check_tol_pols` (1e-12).

## `pols_maturity` and the projection horizon — the notes give none

The technical notes state no projection length, and under the `rollover` architecture there
is nothing in the contract that ends it: the guarantee period renews indefinitely and the
notes write the base-lapse pattern as a repeating five-year cycle with no terminal date.

The model runs to the contract anniversary at attained age **100 [std]** —
`proj_len() = 12 × (maturity_age − age_at_entry())`, 480 months on the anchor cell. Age 100
is not arbitrary: it is the last attained age in the *sourced* cap band on the renewal
surrender charge — 4% at 94, 3% at 95, 2% at 96, 1% at 97, 0% at 98–100 [S1] [S2]. The cap
*reaches* zero at 98; 100 is where the sourced band stops, so past it the model would be
extrapolating a schedule no source states. It is also well past the Model #805 §8 deemed
maturity date [R1]. The survivors at that anniversary are annuitized out through
`pols_maturity(t)`, zero in every month but the last, so that

```
pols_if(t) − pols_if(t+1) = pols_annuitization(t) + pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

closes for every `t` — `pols_if(t)` is the start-of-month count, so it opens the row, the
four exits are taken during the month, and the next month opens on what is left. Including
the last month, where the block would otherwise appear to lose
lives with no cause. This is bookkeeping determined by the horizon, not a new assumption; the
name and the construction follow `BasicTerm_S.pols_maturity` and `Term_US_A`. It matters
little in practice: with a 90% shock lapse every five years, in-force falls by roughly a
factor of ten per cycle — end of month 60 `pols_if_at(60, "AFT_DECR")` = 0.9077, end of
month 120 = 0.0808, end of month 240 = 5.6e-4 — so what enters the horizon month,
`pols_if(480)`, is 3.0e-9 of the contract and the choice of horizon moves nothing
material. Under `annual_redeclare` the shock happens once, so it matters more; run
both architectures before quoting a duration, as the notes' first sensitivity says.

## `result_cf()` starts at `t = 0`, not `t = 1`

The notes' cash flow ledger indexes the single premium, the acquisition commission and the
premium tax at `t = 0`, and `AV(0)`, `MGSV(0)` and `l(0)` are the initial branches of the
three recursions. Putting those three flows in month 1 instead would double-count them
against a month that also credits interest. So `result_cf()` runs `t = 0 … proj_len()` and
`net_cf(0) = +98,000` on the anchor cell. Note the contrast with `Term_US_A`, the model
this one takes its structure from, whose result table starts at `t = 1`: the index here is
the notes' own, not a house convention, so read `t = 0` before comparing the two ledgers.

## The 30-day window sits *after* the boundary, not before it

The product spec describes the free-out window as "the 30 days **before** each guarantee
period ends"; the technical notes' processing order places it in the month *after* the
period closes — "if the previous month ended a guarantee period (`t − 1 ≡ 0 mod 12n`)".
On a monthly grid the two readings differ by one step and cannot both be implemented.

**The technical notes are the specification, so the model follows them:** `in_gp_window(t)`
is true at `t = 61, 121, 181, …`. This is also the reading that makes the rest of the notes
consistent — the annuitization rule is stated as "only in a 30-day window, `t > 12`", and
the prescribed base lapse puts the 75% shock in contract **year 6**, which is months 61–72.
Under `annual_redeclare` there is exactly one window, at the end of the initial term.

## The annuitization transfer is valued at BOM, though the notes name `SV(t)`

The notes say annuitization "transfers `AV'(t)` (in the window) or `SV(t)`" out of the
accumulation block, and they exclude the MVA from it. But `SV(t) = AV(t) + M(t) − C(t)` is
composed on the *post*-crediting account value, while the same notes make annuitization an
elective **BOM** transaction. On a monthly grid the two readings differ by one month's
interest and cannot both be implemented.

The model annuitizes at BOM **[std]**: `annuitization_pp(t)` is `AV'(t)` in the window and
`AV'(t) − sc(y) × E(AV'(t))` outside it, and `claim_from_av_pp(t, "ANNUITIZATION")`
releases the matching `AV'(t)`. Paying the literal `SV(t)` against a BOM exit would hand
the annuitant `(AV(t) − AV'(t)) × (1 − sc(y))` of interest the block never credited to
those contracts, and that would show up as a positive `claims_over_av` with no binding
Model #805 floor behind it.

It is inert on the shipped model points — `a(t)` is 1.0% in the window and 0% everywhere
else, so the non-window branch never carries a contract — but it is the branch a user
switching on mid-term annuitization would land in first, so a test pins it open. If your
admin system settles annuitizations at EOM instead, return `av_pp(t) − surr_charge_pp(t)`
there and move the claim's release basis with it.

## The shock lapse is spread across the shock contract year

The notes give the base lapse annually by contract year and convert it with
`w_base_m = 1 − (1 − w_base_annual)^(1/12)`. Applied to the 90% shock year that is 17.5% per
month for twelve months, not a point event at the window. Only the first of those months —
the window itself — is free of surrender charge and MVA; months 62–72 carry the fresh 5%
renewal charge while still lapsing at 17.5% a month.

That is what the notes prescribe and the model implements it literally, but it is worth
knowing before quoting a liability duration: a design that concentrates the shock in the
window month would pay out sooner and would pay the full account value on all of it. The
architecture switch, not this discretization, is the first-order decision — but this is the
second-order one.

## `T(t)` and the geometric `tau` are the same number here

The notes define the linear-duration `T(t)` as (days to the end of the current contract year
÷ 365) + whole years remaining in the MVA period, and the geometric `tau` as days to
maturity ÷ 365.25 — two different day-count conventions, from two different carriers. On a
monthly grid the first collapses algebraically to `(12·n·k − t)/12`, which is exactly the
second on exact twelfths. `mva_term(t)` therefore serves both branches, and a test asserts
the identity. Reconciling to an admin system that runs actual days will reintroduce the
difference; that is a discretization consequence, not a modelling choice.

## `av_initial` and `mgsv_initial` are derived, not input

The notes list `av_initial`, `mgsv_initial` and `tax_basis_initial` as model point
attributes. Two of the three are fixed by rules the notes also state: 100% of premium is
credited with no front-end load [S5] [S10] [S16], and the Model #805 floor starts at 87.5% of
gross consideration [R1 §4.A(2)](#uslib-fixed_deferred_annuity-r1). Shipping them as data would let a model point silently
violate the statute. They are computed instead, from the References `load_prem_rate` (0.0)
and `net_consideration_ratio` (0.875). Only `tax_basis_initial` stays a column, because it
genuinely varies with tax status.

## `free_wd_mva_exempt = False` moves the surrender charge too

In the market the flag is about the **MVA**: the two registered contracts apply the
adjustment to free-amount withdrawals, the retail MYGAs do not
[S2] [S3] [S4] [S9] [S10] [S15] [S16]. The technical notes are explicit that setting it
False gives `E(t) = AV(t)` and collapses the surrender benefit to
`max(AV(t) × (1 + μ(t) − sc(y)), MGSV(t))` — the multiplicative form — which moves the
surrender *charge* onto the whole account value as well.

The model implements the notes' reading, because that identity is the one the notes use for
their dimensional-consistency check and a test pins it on model point 4. If you need the
market split — MVA on the free amount, charge not — split `surr_excess_pp` into two bases;
nothing else has to change.

## What is not implemented

Named here so the gaps cannot be mistaken for oversights; the model docstring carries the
same list.

- **The RMD module.** The notes give the charge and MVA exemption but no RMD amount formula.
- **Nursing-home and terminal-illness waiver withdrawals.** No incidence basis is given.
- **VM-22 Table 6.2 partial-withdrawal rates.** The retrieved table is the *Qualified* column
  only and its 80-and-over row was truncated; the notes say not to present it as a
  non-qualified assumption. The base run withdraws 0% **[std]**, and the free-withdrawal
  utilization variant `free_wd_util` is the switch that is implemented.
- **The `greatest_of` free-withdrawal rule.** Described, no formula.
- **The gross-up solve for a stated net check.** `wd_pp(t)` is gross by construction.
- **Model #805 §6's paid-up annuity leg.** Noted but not implemented in the notes themselves.
- **`check_margin()`.** The product carries no contract charges and the model projects no
  asset side, so there is no charge-versus-cost decomposition to check. `check_av_roll_fwd()`
  and `check_pols_roll_fwd()` are implemented — no argument, returning `True` over every
  projected month — and both close to floating point, with
  `check_av_roll_fwd_resid(t)` / `check_pols_roll_fwd_resid(t)` giving the signed residual.
- **Stochastic scenarios.** The reference yield and competitor rate are read from a
  deterministic scenario table.

## Standardizations used

Everything in this list is **[std]**: the monthly grid and the BOM/EOM placement of each
step; the decrement order annuitization → mortality → surrender; the mapping of VM-22
Table 6.5 onto a five-year architecture (1% inside the period, 75% at expiry, repeating
under `rollover`); the 0.35 best-estimate `Φ_MVA` against VM-22's prescribed 0; the renewal
declaration rule `max(GMIR, MR − s_ren)` with `s_ren = 0`; the 1.0% annuitization take-up at
each window against VM-22's prescribed 0%; the 0% base partial withdrawal; the 2.00%
acquisition commission; the $50 per contract per year maintenance expense inflating at 2.5%;
the 0% premium tax; the exogenous reference-yield and competitor-rate scenarios and the
`i0 = 5.00%` issue lock; the illustrative mortality table; and the attained age 100
projection horizon. Non-qualified tax status and the `pct_av` / `sym_sc` /
`linear_duration` / `rollover` / `gross` switch settings on the anchor cell are also
**[std]** picks from a genuinely split market — the model point table carries the
alternatives.

## Tests

`tests/test_fixed_deferred_annuity_us.py` asserts all seven rows and five columns of the
notes' worked example table to the cent; the notes' own exactness checks (`AV(12) =
100,000 × 1.0445`, `AV(24) = 100,450 × 1.0445`, `MGSV(24) = (89,950 − 4,000) × 1.028`) to the
twelfth significant figure; the month-30 surrender trace line by line, cap and floor both
inactive; the month-6 stress trace, where the symmetric cap bites at −8,298.07 and the Model
#805 floor then adds 3,111.90; one registered contract's geometric-branch factors 1.01897
and 0.96944 and its −2.06% expense-adder case [S4]; both roll-forwards at every month; and
one test per entry in the notes' "Known modeling pitfalls" list — composition order, the
free-amount/MVA interaction, gross versus net withdrawals, the two Model #805 withdrawal
conventions, the 15 bp floor (and that the statute states a *minimum*, not a cap), the
surrender-charge clock on renewal, and the mortality plumbing.

Two tolerances are worth knowing. Money is asserted to **0.006** rather than 0.005 because
the notes round half-up for display and `AV(24) = 104,920.025` sits exactly on the boundary.
And `E(30)` is asserted to **0.01**, because the notes state that "the surrender traces below
are computed from the cent-rounded values shown": they print
`107,229.09 − 10,492.00 = 96,737.09` where full precision gives `96,737.0843`. Everything
else in the traces agrees to well under a cent.

```bash
python -m pytest tests/test_fixed_deferred_annuity_us.py -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_fixed_deferred_annuity_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_fixed_deferred_annuity_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-fixed_deferred_annuity-r1
[R9]: #uslib-fixed_deferred_annuity-r9
[std]: #uslib-std
<!-- END generated citation links -->
