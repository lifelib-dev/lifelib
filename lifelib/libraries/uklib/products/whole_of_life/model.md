# Implementation Notes

**Status:** Draft, 2026-08-15. Built from
[`products/whole_of_life/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the moratorium and its return-of-premiums benefit,
> accidental death paying the full cash sum from day one, premium cessation at 90 with
> cover continuing, the absence of any surrender value, the suicide clause, the
> escalation ratios, the pro-rata paid-up formula. Every **rate** is a **[std]**
> standardization: the CMI's current tables are restricted to Authorised Users
> [REG-R22] [R7], so both mortality bases are proxies **shaped like** the tables the notes
> name, and no insurer publishes whole of life premium rate tables, so the premium is a
> model point input.

## Run it

```bash
python products/whole_of_life/run.py         # the O50 anchor cell
python products/whole_of_life/run.py 5       # the underwritten cell
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/whole_of_life/WOL_UK_S")
model.Projection[1].result_cf()
```

## Two cells, one engine

| | **RefWOL-UW** (`cell = "UW"`) | **RefWOL-O50** (`cell = "O50"`) |
|---|---|---|
| Underwriting | full | **none** — guaranteed acceptance |
| Premiums | level, **for life** | level, **ceasing at the anniversary on or after the 90th birthday**; cover continues |
| Year-1 death | sum assured, less a suicide refund carve-out | **twelve-month moratorium**: non-accidental death returns premiums paid, accidental death pays the full cash sum |
| Mortality basis | assured-lives shape, 100% | population shape, **120% anti-selection loading** |
| Anchor | M40 NS, £150,000, £101.25/month | F70 NS, £5,000, £30.00/month |
| Crossover | none at the anchor | month **167** — 13 years 11 months |

**Neither cell has an account value, a unit fund or a surrender value.** Both are pure
decrement protection models: premiums in, death benefits and expenses out, weighted by
survivorship. That is the deliberate contrast with
[`WholeLife_US_A`](../../../uslib/products/whole_life/model.md), the U.S. whole life model in
the same library, which is built around a guaranteed cash value schedule, three-factor
dividends, paid-up additions, a dividend accumulation balance and policy loans. None of
that machinery exists here — no `cv_pp`, no `div_*`, no `pua_*`, no `loan_bal` — and a
lapse on either UK cell pays exactly nothing.

### The bases must not be swapped

Full underwriting restores select experience, so the UW cell takes an assured-lives
shape. Guaranteed acceptance removes underwriting, so the O50 pool cannot be better than
the population and self-selects worse; it takes a population shape with a **120%**
anti-selection loading **[std]**. The CMI analyses non-underwritten whole of life
separately from underwritten business for exactly this reason [R7].

`mort_basis()` and `mort_loading()` are therefore **derived from `cell()`** rather than
left as free parameters. Feeding either cell the other's basis produces
plausible-looking but wrong margins, and the FCA's price differential between the two
designs — £71.73 against £8.10 per £1,000 of cover [R2] — is the scale of that error.

## The moratorium is a discontinuity, not a curve

During the O50 cell's first twelve months:

- a **non-accidental** death returns `CumPrem(t)` — the premiums paid, **not** the cash
  sum and **not** an annualized premium;
- an **accidental** death pays the full cash sum from day one.

At month 13 the full cash sum becomes payable for any death, and expected death outgo
jumps about **elevenfold** on the anchor cell: £0.91 at t = 12 against £10.00 at t = 13.
That step is the signature of the product and must not be smoothed — an annual-grid
implementation has to split policy year 1 explicitly.

Note where the year-one outgo actually comes from. At month 1 the blended benefit is
`0.97 × £30 + 0.03 × £5,000 = £179.10`: five sixths of it is the small accidental tail
paying the full cash sum, not the premium refund. An implementation that dropped the
accidental split would understate year-one claims by about that much.

**The accidental-multiplier variant** doubles the accidental benefit, but **only on and after
the first anniversary** [S7]. Inside the moratorium the accidental benefit is already the
full cash sum, so doubling it there — or applying the multiplier to all deaths — overstates
outgo. `adb_multiplier()` is applied in exactly one place, `benefit_pp(t, "ACC")`, past the
moratorium only.

## Lapse pays nothing, which is the whole economics

There is no surrender value at any duration on either cell [S1] [S4] [S5] [S7] [S9] [S10], so
a lapse produces no cash flow at all: its entire effect is through `pols_if`. Every lapse
therefore extinguishes a liability for nothing, the best estimate falls **monotonically**
as assumed lapses rise, and the FCA records that without the continuing-payer
cross-subsidy insurers would need to rely on lapses to remain profitable [R2].

Two consequences are wired into the model rather than left as prose:

**No lapse after premiums cease.** There is nothing left to stop paying once the O50 cell
reaches cessation, so `lapse_rate(t)` is zero from month 241 on the anchor. Applying a
lapse decrement past cessation silently destroys liability, and the notes list it as a
pitfall. The post-cessation period is pure outgo — the worked example's month 241 row
shows premium income at zero while death outgo *rises*.

**The pro-rata paid-up variant is a different product.** Once half the expected payments
have been made, a would-be lapse converts to a **paid-up** policy at
`SA × N_paid / N_expected` [S9] instead of forfeiting everything. That converts lapse
profit into a retained pro-rata liability and collapses most of the lapse sensitivity —
on the shipped points it takes the O50 anchor's total net cash flow from about −£41 to
about −£418. It is a variant to model separately, never a small adjustment.

It is carried as a **second population strand**:

| Cells | What it holds |
|---|---|
| `pols_if(t)` | policies still on full cover — the notes' `l`, and the column the worked example prints |
| `pols_pu(t)` | paid-up policies |
| `pu_benefit(t)` | the **aggregate paid-up cover** in force |
| `pols_all(t)` | the sum, which is what the maintenance expense is carried on |

Carrying the aggregate benefit alongside the count is what removes the need for a
per-conversion cohort dimension: the paid-up payout depends on *when* the policy
converted, but every paid-up policy thereafter rolls forward on the same survival factor,
so the sum of their payouts satisfies the same recursion as the count. Death outgo on the
strand is then simply `pu_benefit(t) × q_m(t)`.

## The crossover

On the O50 cell cumulative premiums eventually exceed the cash sum. `crossover_mth()`
finds the month: on the anchor cell `floor(5000/30) + 1 = 167` months — **13 years 11
months**, which is the FCA's stylised example exactly [R2]. Total premiums are capped at
`P × T_cess` (£7,200 against a £5,000 cash sum), so a crossover exists only where the cash
sum is below that cap; the underwritten anchor has none.

It is **searched** rather than closed-form so that an escalating variant still resolves,
and it is **reported rather than acted on**. The notes' crossover-aware lapse module,
which raises lapse past the tipping point, is a pure stress dial: `lapse_crossover_beta`
is 0 in the base run, and the FCA has seen no evidence that a significant proportion of
customers reach the premium caps [R2].

## `pols_maturity` means something different here

The name is borrowed from the term models, but whole of life has **no maturity**. The
cells is the population still alive when the projection is truncated at the limiting age,
so it is a **truncation artefact** rather than a benefit, and it pays nothing. It exists
so the roll-forward closes in the last month.

`check_truncation()` asserts it is negligible, and that is the substantive statement: the
shipped mortality tables reach 1 well before `omega_age = 120`, so the population is
exhausted *inside* the projection rather than cut off by it. A limiting age set too low
would drop liability off the end instead of merely rounding it.

## Age last birthday

This is the one model in the library on **ALB** rather than age nearest birthday: the
underwritten cell's specimen defines entry age x as "before the (x+1)th birthday" [S10],
which is ALB, and the over-50s documents price on "age at outset" without stating a basis
**[std]**. All age lookups here are on that one basis.

## Inputs are external files

The three input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `WOL_UK_S/` holds nothing but formulas:

```
products/whole_of_life/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  lapse_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  WOL_UK_S/                   <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`. `Projection` is parameterized by
`point_id`, so the CSV readers live in an unparameterized **`Data`** Space and each file
is read once per model rather than once per model point; a test counts the reads.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |

Both the mortality and the lapse table are keyed by the **cell** as well as by the usual
rating factors, for the reason above.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Seven model points. **Point 1 is the worked-example anchor cell** (O50 / F70 / non-smoker / £5,000 / £30.00 a month / cessation at 240 months); points 2–4 are the accidental-double, pro-rata paid-up value and RPI-increasing O50 variants; points 5–6 are the underwritten cell level and on the 5% increasing-cover variant; point 7 is an O50 male smoker on a longer cessation | anchor cell **[std]**, technical notes' worked example |
| `mort_table.csv` | Annual mortality by basis × sex × smoker × age 18–120, capped at 1, with a `provenance` column | **[std]** throughout. The `population` rates are anchored so that `q(F, NS, 70) × 1.20 = 0.024` with 10% p.a. age progression — the notes' walk-through basis *exactly* — and the `assured` rates are anchored at `q(M, NS, 40) = 0.00090` on the same progression. Sex and smoker cells are flat factors. Neither basis is a published table |
| `lapse_table.csv` | Annual lapse by cell and policy year: O50 8/6/4/4/4/4 %, UW 6/5/3/3/3/2 % | **[std]**; no public UK whole of life lapse study was retrieved, and on a product with no surrender value this is the single largest lever on the liability |

The mortality table is a **[std]** construction with no separate "worked example" basis
switch, because the notes' walk-through basis and the shipped population basis are the
same object: the notes describe their `q(y) = 0.024 × 1.10^(y−1)` as "a 0.020
population-style rate at 70 × the 120% anti-selection loading, with 10% p.a. age
progression", so the shipped table *is* that, extended over the full age range and capped
at 1. The worked example reproduces without any special-casing.

## Sign convention, and reading the worked example

`net_cf` is **income positive**, the notes' own sign and the library-wide one, so there
is no outgo-positive `liability_cf` companion.

One caveat for a reader checking the worked example by eye: **the notes' table omits
expenses entirely**, "for clarity", and prints premium income and death outgo as separate
positive columns. So `net_cf` will not equal any column of that table; the tests assert
`premiums(t)` and `claims(t, "DEATH")` against it directly.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE`: `pols_*` for
policy counts, plural nouns for cash flows, `*_rate` for annual rates and `*_rate_mth`
for monthly ones, `*_pp` for per-policy amounts, `claims(t, kind)` and
`benefit_pp(t, kind)` with uppercase `kind` strings. The full symbol mapping lives in the
`Projection` Space docstring. Three cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `l(t)` | `pols_if` / `pols_pu` / `pols_all` | The pro-rata paid-up variant splits the population into full-cover and paid-up strands; on every other model point the three coincide |
| `SA` | `sum_assured` / `cover_pp` | A constant in the notes and a function of `t` here, because the escalating variants move it |
| *(no analogue)* | `pols_maturity` | Borrowed from the term models but a **truncation artefact**, not a benefit — see above |

## Standardizations used

Everything in this list is **[std]**: both mortality bases and their sex/smoker factors;
the 120% anti-selection loading and the 100% assured factor; the mortality improvement
dial (zero in base, a flat annual rate as the proxy for a subscriber-restricted CMI
projections model); both lapse tables; the accidental share of deaths (3%) and the
suicide share of year-one deaths (1%); premium cessation at the anniversary on or after
90; the 5% increasing-cover pick; the flat 3% RPI snapshot; full escalation take-up (the
three-declines rule cannot be represented in a deterministic run and is not implemented);
the crossover lapse stress dial; the assumption that **all** would-be lapses convert once
the pro-rata paid-up halfway point is passed; acquisition £150 / £300 and maintenance £30 /
£50 a year inflating at 3%; initial commission at 25% of first-year premiums; and
death-before-lapse as the processing order.

Deliberately excluded, per the notes: terminal illness acceleration (it pays the same
amount earlier and is **not** an additional decrement — modelling it as one would
double-count), claims interest at BoE − 0.5%, premium reduction options, payment holidays,
and the anti-selective milestone-benefit increases on the underwritten cell.

## Tests

`tests/test_whole_of_life_uk.py` asserts all eleven rows of the notes' worked example to
the penny and the in-force column to five decimals, the month-12/13 moratorium
discontinuity and its size, the accidental split's share of year-one outgo, the
month-167 crossover, that lapse pays nothing and stops at cessation, both escalation
variants, the pro-rata paid-up strand and its effect on the liability, the two mortality
bases against each other, and that the truncation residual is negligible.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R2]: #uklib-whole_of_life-r2
[R7]: #uklib-whole_of_life-r7
[REG-R22]: #uklib-reg-r22
[std]: #uklib-std
<!-- END generated citation links -->
