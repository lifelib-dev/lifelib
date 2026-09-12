# Implementation Notes

**Status:** Draft, 2026-08-20. Built from
[`products/endowment/technical-notes.md`](technical-notes.md); the product it implements is
specified in [`product-spec.md`](product-spec.md). The savings machinery underneath it — the
policy value (*hokenryō tsumitatekin*, 保険料積立金), the surrender value (*kaiyaku-henreikin*,
解約返戻金), policy loan (*keiyakusha kashitsuke*, 契約者貸付), automatic premium loan (*jidō furikae
kashitsuke*, 自動振替貸付) and the grace, 失効 and 復活 chain — is specified once in
[whole life technical notes (終身保険)](../whole_life/technical-notes.md) and implemented in
[`WholeLife_JP_S`](../whole_life/model.md), whose cells names this model carries wherever
the two express the same quantity — `pol_val_pp`, `cv_pp`, `surr_charge_pp`, `reserve_pp`,
`loan_pp`, `pols_if_at`, `check_net_cf`. This file states the deltas; where it sets an
inherited parameter to a different number — the loan rate — it names the difference as a
deviation and gives its reason rather than leaving it silent.

> **This is a mechanics demonstration, not a pricing or reserving result.** Three things
> here are sourced and everything else is constructed. Both annual premiums are twelve
> times a monthly premium published for exactly the model point they sit on — the 養老保険
> (*yōrō hoken*, endowment assurance) anchor cell [S9] and the education endowment (*gakushi
> hoken*, 学資保険) cell [S11]; the assumed interest rate (*yotei riritsu*, 予定利率) of
> 1.00% that the cash-value construction runs on is published by product group, before and
> after a dated revision [S9]; and the staged education money (*gakushikin*, 学資金) grid is
> one carrier's published S型 schedule [S10] [S11]. The surrender-value formula, the expense
> basis and the surrender curve are published by **no** carrier for either cell — a sharper
> gap than the savings chassis faced — so `α`, every expense level and the whole lapse table
> are **[std]**. The shipped mortality table is a **[std]** construction whose `provenance`
> column points at the Institute of Actuaries of Japan (日本アクチュアリー会); it is not a copy of
> 生保標準生命表2018（死亡保険用）, which the publisher's site terms forbid this library to
> redistribute [REG-R21]. Replace the tables and the cash-value basis with a company
> 算出方法書 before drawing any conclusion from the numbers.

## Run it

```bash
python products/endowment/run.py            # the 養老 anchor cell (point_id = 1)
python products/endowment/run.py 2          # the 学資 cell
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/endowment/Endowment_JP_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked example's anchor cell and
`Projection[2]` its second cell. `result_cf()` returns a `DataFrame` indexed by the **policy
month** `t` with one column per cash flow line, `pols_if` first and `pols_if_pay` and
`pols_wv` beside it. Two further
result tables sit beside it: `result_pols()` for the in-force probabilities and decrement
rates, and `result_val()` for the per-policy value construction — that one indexed by the
**anniversary** `k`, one row per policy year, because the values it publishes are annual
quantities and printing each of them twelve times would only look like information.

## Three clocks: the month `t`, the anniversary `k`, the elapsed month `u`

`t` is the projection index and it counts **policy months**, 0-based: `t = 0` is the first
policy month, `t = proj_len() - 1 = 12n - 1` the last, `proj_len()` is the *number* of
projected months so `len(result_cf()) == proj_len() == 12 * policy_term()` and the frame is
`range(proj_len())`, and the contractual **policy year is the 1-based label
`policy_year(t) = 1 + t // 12`** with `duration(t) = t // 12` beside it. Month `t` runs from
time `t` to time `t + 1`: premium (in anniversary months only), maintenance expense and
commission sit at its start; death, staged, maturity and surrender benefits at its end.
`age(t) = x + t // 12`, `pols_if(0) = 1`, surrender is suppressed in `t = 12n - 1`, maturity
falls in that same month, and `pols_if(12n) = 0`.

Beside it runs **`k`, the anniversary index, in years**, `k = 0` at issue. Everything that
is a *value at a point in time* rather than a *flow during a period* is indexed by `k`, and
**none of those numbers moved when the projection index became a month**:
`pol_val_pp(k)`, `pol_val_pre_pp(k)`, `surr_charge_pp(k)`, `surr_val_pp(k)`, `cv_pp(k)`,
`reserve_pp(k)`, `benefit_pct(k)`, `benefit_pct_cum(k)`, `prem_cum_pp(k)`, `loan_pp(k)` and
`edu_epv(k, i)`. That is deliberate and it is the design decision of the conversion: those
are contractual constructions defined at the 年単位の契約応当日, and restating them as monthly
recursions would invent a within-year rule the 算出方法書 does not publish [REG-R2].

Between anniversaries the projection reads them through a third index, **`u`, an elapsed
month**, by linear interpolation **[std]**: `pol_val_pre_at_m(u)`, `pol_val_at_m(u)`,
`surr_charge_at_m(u)`, `cv_at_m(u)` and the step function `prem_cum_pp_m(u)`. The flows of
month `t` read them at `u = t + 1`, the closing instant of the month — so
`claims(t, "LAPSE")` reads `cv_at_m(t + 1)` and `death_ben_pp(t)` reads
`pol_val_pre_at_m(t + 1)`. At `u = 12k` each `*_at_m` cells returns its anniversary value
exactly, which is what makes the annual and the monthly model agree wherever they are both
defined. `loan_pp` is the exception that proves the rule: the loan rate is a 年利 capitalised
at the 契約応当日, so the balance genuinely does not move between anniversaries and month `t`
settles against `loan_pp(duration(t))` with no interpolation at all.

`SC(0)` is the deduction at issue and `W(n) = S` the value at maturity; neither number moved,
and neither did the 学資金 grid at anniversaries 3 / 6 / 12 / 15 / 18 / 20 — each of which is
now the staged claim of the single month `t = 12k - 1`.

## What the conversion changed, and what it did not

Survivorship at the anniversaries did not change: mortality and surrender are quoted per
annum and applied per month on the effective convention `r_m = 1 - (1 - r)^(1/12)`, so twelve
months compound back to the annual rate exactly and `pols_if(12j)` reproduces the annual
model's `pols_if(j)`. Neither did the premium income, because the premium is 年払 on every
shipped point and falls at the same anniversaries it always did. Four things did change, and
each is a modelling improvement rather than an artefact:

- **The 年払 premium is one month in twelve.** `result_cf()` is a sawtooth — one large inflow
  a year against maintenance expense and claims every month — which is the shape of the
  contract and which the annual grid could not draw.
- **The final-month surrender carve-out.** Surrender is suppressed only in `t = 12n - 1`,
  where it would collide with the maturity payment, instead of for the whole final policy
  year. Eleven months of genuine surrender come back, and the anchor cell's maturing
  fraction falls from 0.5042 to **0.4949**.
- **The staged benefits are one month wide.** Each 学資金 falls in `t = 12k - 1` and is zero
  in the other eleven months of its policy year.
- **Both limbs of the education cell's death benefit now bind.** The premium limb steps up by
  a whole 年払 premium each anniversary month and the value accretes through the year to
  overtake it, so the `max` switches **85 times in 264 months** where on the annual grid it
  never switched at all.

The premium-default proportion feeding the APL is the one rate that is **not** converted: it
is the failure to pay one premium on one date, so it is applied once per premium and is zero
in the eleven months between.

The model and its `Projection` Space both carry docstrings: `model.doc` describes the
product and the projection basis, and `model.Projection.doc` holds the full mapping between
the technical notes' symbols and the cells names.

## Two cells, one model

`cell` is a model point column and it selects between two genuinely different
constructions, not two parameter sets.

On the **endowment** cell the contract is an endowment assurance, so the death benefit sits
inside the expected present value:

```
pi     = S x A(x, n) / a-due(x, m)
W(k)   = S x A(x + k, n - k) - pi x a-due(x + k, max(m - k, 0))
DB(t)  = S - L(t)
```

On the **education** cell the death payment releases the value rather than adding to it, so
the value is built from the survival benefits alone and the death benefit is a return of
premiums floored at that value:

```
EPV(k) = S x [ sum over s > k of g(s) v^(s-k) (s-k)p  +  v^(n-k) (n-k)p ]
pi_g   = EPV(0) / a-due(x, m)
W(k)   = EPV(k) - pi_g x a-due(x + k, max(m - k, 0))
Wb(k)  = W(k) + S x g(k)
DB(t)  = max( P x min(ceil((t + 1)/12), m) - S x G(t // 12) - L(t // 12),  Wb(t + 1) )
```

`DB(t)` is where all three clocks meet: a death in month `t` is paid at the end of it, so the
value limb is the interpolated `Wb(t + 1)`; the premiums *due* are the
`min(ceil((t + 1)/12), m)` that have actually fallen by then, which steps up once a policy
year; the loan is the balance outstanding at `t // 12`; and the staged benefits *already
received* are those to anniversary `t // 12`, because a payment falling at the close of month
`t` is still inside `Wb(t + 1)`.

Both value forms live in `pol_val_at(k, i)`, which branches on `cell()`; `pol_val_pp(k)` is
that at `i_cv` and `reserve_pp(k)` the same at `i_std`. Excluding the death benefit from the
education cell's EPV is the **[std]** step, and it is one carrier's own wording read
literally: its 死亡払戻金 *is* the 責任準備金相当額 — the amount equivalent to the policy reserve
(*sekinin-junbikin*, 責任準備金) [S10] — so on that design the decrement is exactly
value-neutral and the composite's max-form dominates it [S3] [S13].

Both limbs of that `max` must be evaluated, and on the monthly grid both of them bind on the
shipped cell. On the annual grid the value limb dominated at every *anniversary* and the
`max` never switched; read month by month it switches **85 times in 264** — eleven months of
policy year 1, then fewer each year until the value pulls clear for good in policy year 13 —
because the premium limb steps up by a whole 年払 premium each anniversary month and the value
accretes through the year to overtake it. Hard-coding either limb is now right eleven months
a year at best, and the tests assert both the crossover pattern and a copy of the cell with a
raised premium where the refund limb takes over for good.

## The policy value must land on its own maturity benefit

At anniversary `k = n` there is no future benefit beyond maturity and no future premium on
either
construction, so `W(n) = S` **exactly**. That is `check_pol_val_terminal()`, and it is the
one thing a whole life chassis can never check: a whole life reserve that drifts can hide
for decades, while an endowment reserve that does not converge on its own maturity benefit
is wrong on the first run.

`pol_val_db_pp(k)` names the death benefit *inside* the EPV — `S` on the endowment cell,
zero on the education cell — so that a single recursion covers both, rolling the policy year
from its opening anniversary `k` to its closing one `k + 1`:

```
(W(k) + pi 1{k < m}) (1 + i_cv) = q(k) DB_val + (1 - q(k)) Wb(k + 1)
```

with `W(0) = 0` at issue. It is `check_pol_val_roll_fwd_resid(k)`, an **annual** check on an
annual construction — on the monthly grid it is the one roll-forward that is not indexed by
`t`, because restating it per month would require the within-year value rule the contract
does not publish.
That is `check_pol_val_roll_fwd()`, and it pins the timing as well as the arithmetic:
premium credited at the start of the policy year, interest for the whole year, death benefit
and staged benefit at the end. Its `q(k)` is the **unadjusted** table rate, because the policy
value is a contractual quantity on the pricing basis: a best-estimate adjustment to the
projection must not move it. That is testable rather than asserted — model point 4 carries
`mort_be_factor = 1.25` and its `pol_val_pp` series is identical to model point 2's to the last
bit.

A third identity falls out of `i_std` defaulting to `i_cv`, which it does because the
numeric standard valuation rate (*hyōjun riritsu*, 標準利率) could not be established from any
retrieved official document [R4] [R5]:
`reserve_pp(k) - cv_pp(k) = surr_charge_pp(k)` exactly at every anniversary, wherever the
value exceeds the
deduction. That is `check_surr_charge()`; the one branch it does not assert is where the
deduction would exhaust the value and `surr_val_pp` floors at zero.

## Two lives, two decrements, one policy

The education cell carries waiver of premium (*hokenryō haraikomi menjo*, **保険料払込免除**) on
the policyholder (*keiyakusha*, 契約者) — a second decrement on a second life who is not the
insured (*hihokensha*, 被保険者). It has no analogue in `uslib` or `uklib`.

`mort_rate(t)` reads the table at the insured's `x + t // 12`; `mort_rate_ph(t)` reads it at
the policyholder's `y + t // 12`. Both are **annual** rates and both have a monthly companion,
`mort_rate_mth(t)` and `mort_rate_ph_mth(t)`, which is what the in-force recursion actually
runs on. Reading one table at one age for both is the most likely
implementation error on this product, and on the anchor cell the two ages coincide, so it
would not show there. Model point 2 has an insured aged 0 and a policyholder aged 30, and
the two rates differ by a factor of five in the fifth policy year.

`mort_rate_ph(t)` is **zero from `t = 12m` on**, the premium-paying months being
`t = 0 .. 12m - 1`. Every waiver trigger in the retrieved 約款 is
conditional on the event falling during 保険料払込期間 [S1] [S10], and the
termination-without-waiver path is the failure mode of that same provision, so after 払込満了
there is nothing for the provision to act on and the composite treats the contract as
continuing through the 契約者's death by succession [S1] [S7] [S10] [S13]. Carrying the
decrement into the months `t >= 12m` would move a further **0.8250%** of policies out of the
premium-paying state — terminating a share of them wherever `wv_frac < 1`, and deleting their
maturity benefits — in exactly the years in which 86% of the second cell's receipts fall.

The waiver produces **no outgo line at all**. What it produces is the absence of premium
income: `premiums(t)` is carried on `pols_if_pay(t)` alone while `maint_expenses(t)` runs on
`pols_if(t)`, the total, and `commissions(t)` pays renewal commission on the paying state
only. A waived policy costs the insurer administration and pays the distributor nothing.
Because omitting the waiver altogether leaves every claim column unchanged, neither
booking a phantom "waiver benefit" nor dropping the module is visible in a benefit
reconciliation — so the test runs a copy of the cell with `waiver = False` and asserts that
every claim column is bit-identical while the premium line moves.

Premiums on a waived policy are **deemed paid**, so `prem_cum_pp(k)` and its monthly reading
`prem_cum_pp_m(u)` keep growing on a policy that pays nothing and `cv_pp(k)` is the same series in both states [S1] [S10] [S13].
A model that keeps two value series is modelling a contract nobody wrote.

## The staged schedule is data

`benefit_schedule()` reads the whole grid from `benefit_schedule_table.csv`, keyed by the
model point's `schedule_id`, and `benefit_pct(k)` is a lookup into it. The file's key column
is `k`, the **anniversary** the payment falls on — a time point in years, already 0-based —
so the payment at `k` is the staged claim of the single month `t = 12k - 1` and
`claims(t, "STAGED")` returns zero unless `(t + 1) % 12 == 0`, reading
`benefit_pct((t + 1) // 12)` when it does. Total receipts range
from 100% to 400% of 基準保険金額 across the six carriers in the source set
[S1] [S3] [S7] [S10] [S13], so a model that treats the grid as anything but data is
modelling one carrier. Model point 3 runs the degenerate `J` variant — one payment of 100%
at anniversary 18, then maturity — without touching a formula.

`schedule_id = none` on the endowment cell is a product fact and not a missing value: the
survival benefit there is a single payment at anniversary `n`. The 満期保険金 is never a schedule row;
it is present on both cells and held separately, so a schedule with no rows still matures.

The staged benefit is **not a claim and not a decrement**. It is paid on survival at a fixed
anniversary — one month wide on this grid — to everything in force in **both** states, and it
terminates nothing.
`check_staged_value()` asserts that it comes **out of** the policy value rather than beside
it — `Wb(k) - W(k) = S g(k)` — which is the sourced constraint that each 祝金 reduces the
解約返戻金 [S7]. On the second cell the surrender value falls from ¥1,738,755.93 to
¥1,056,811.08 across the 70% payment; a model that pays the benefit beside the value
inflates every later surrender.

## The composite's seam is printed, not smoothed

`prem_net_level_pp()` is the net level premium on `i_cv` and it is a **derived output, never
an input**: the gross premium is sourced and the loading is what falls out. On the anchor
cell that loading is ¥35,243.66, or 19.457% of the gross premium — plausible for a thirty-year
endowment, and coherent because the premium and the rate come from the same carrier and the
same release [S9]. On the education cell the same calculation gives a net premium **above**
the gross one, a loading of −1.745% that no real product carries, because that premium is a
different carrier's [S11] and that carrier does not publish its 予定利率.

`implied_rate()` restates each loading as a rate, solved by bisection on
`prem_net_level_at(i)` — −0.4239% p.a. on the anchor cell and +1.1592% on the education
cell. Both are published
rather than suppressed: the seam belongs to a composite built from several carriers'
documents, and hiding it would make the library less honest rather than more accurate. The
bisection costs about eighty extra evaluations of the EPV cells the first time it runs, so
it is deliberately not on the `result_cf()` path.

`henreiritsu()` is the 返戻率 the products are actually sold on, and it is a **contractual**
ratio: `(S x sum of g(k) + S) / (P x m)`, on one policy that survives, pays every premium,
takes every benefit in cash and receives no dividend. It reads the contractual premium term
and never the projected premium income, because it is undefined on a policy that surrenders
and unbounded on a waived one. It returns 92.0099% on the anchor cell and 113.7849% on the
education cell, against the "approx. 113.7%" published for exactly that plan [S11] — the
carrier truncates where the model rounds. It is not a rate of return, not probability
weighted, not discounted and not net of expenses, so it is not the ratio the cash-flow
statement produces.

## What is absent, and why that is a product fact

There is **no cliff**. No retrieved document offers a suppressed-surrender-value
(*tei-kaiyaku-henreikin-gata*, 低解約返戻金型) form of either cell, so there is
no suppression multiplier, no step at 払込満了 and no surrender spike, and no lapse-rate spike
to go
with them. `surr_val_pp(k)` and `cv_pp(k)` are the same series and both are published, so
that the absence is stated rather than inferred. Importing the savings chassis's 0.70
suppression multiplier,
its step at `m` or its 15% surrender spike would model a product that does not exist here.
Model point 7 is the only shipped point with `m < n`, so it is where such a step would show;
its value crosses 払込満了 smoothly.

There is **no tail and no terminal age**. `proj_len()` is the 保険期間 exactly — `12 x n`, the
*number* of projected months, so the last row is `t = 12n - 1` and
`len(result_cf()) == proj_len()` — everything
closes at the end of that month, `pols_if(12n) = 0`, and the closing cash flow is a certain
payment of `S` to the survivors
rather than a decrement. The surrender rate is forced to zero **[std]** in that one month: a
surrender at its close and the maturity payment fall at the same instant at the same amount,
so running both double-counts the terminal payment and running the surrender instead of the
maturity misclassifies 61% of the anchor cell's undiscounted outgo. The carve-out is **one
month, not the final policy year** — on the annual grid it could only be a whole year, which
suppressed eleven months of genuine surrender and is why the anchor cell's maturing fraction
moved from 0.5042 to 0.4949 when the grid changed. `pols_maturity` names the survivors so
that the roll-forward closes in the final month, where they neither die nor surrender.

## Model points

| `point_id` | Cell | What it exercises |
|---|---|---|
| 1 | endowment | The worked example's anchor cell: M30, 30/30, ¥5,000,000, ¥181,140 [S9] |
| 2 | education | The worked example's second cell: child 0 / 契約者 30, 22/17, S型 grid, waiver [S10] [S11] |
| 3 | education | The degenerate `J` grid — the schedule is data |
| 4 | education | `wv_frac` = 0.90, `wv_load` = 1.50, `mort_be_factor` = 1.25 — the carve-out and both margins |
| 5 | education | `wv_lapse_mult` = 0.50, female lives — the waived state persists |
| 6 | endowment | F40, 20/20, dynamic surrender **on** and inert |
| 7 | endowment | M35, 25/**15** — 短期払, where `m < n` |
| 8 | endowment | The automatic premium loan module on |
| 9 | endowment | A 契約者貸付 drawn at half the first year's surrender value |

## Inputs are external files

Four CSVs live beside `run.py`, not inside the model folder. **Every one of them is still
keyed in years**, because every rate and every schedule in them is an annual observation or a
contractual anniversary; the monthly grid derives what it needs from them rather than
restating them. The model folder holds
`__init__.py` and `_system.json` per Space and nothing else, so a diff of the model shows
logic changes only. This is the `annuallife.TradLife_A` layout; `basiclife.BasicTerm_S`
keeps its inputs inside the model instead. The consequence worth knowing is that the model
is not portable on its own: copy `Endowment_JP_S/` without its parent's CSVs and it reads
cleanly, then fails on first evaluation.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Nine model points indexed by `point_id`, both cells, every module switch | Points 1 and 2 sourced [S9] [S10] [S11]; the other seven **[std]** |
| `mort_table.csv` | Mortality by sex and attained age, 0 to 60, one `provenance` tag per row | The **library-wide canonical [std] construction** anchored to [REG-R18] [R1]: 22 male and 18 female ANCHOR rows read at quoted ages, the rest log-linearly interpolated in `ln q` to five decimals. Both sexes built from their own anchors |
| `lapse_table.csv` | **Annual** surrender and premium-default rates keyed by `policy_year`, 4 / 3 / 2 percent and 1.0 / 0.8 / 0.6 percent | **[std]**; the industry 解約・失効率 of 5.6% is an amount-weighted all-product ceiling only [R9] [REG-R31] |
| `benefit_schedule_table.csv` | The staged 学資金 grids, one row per payment, keyed by `schedule_id` with the anniversary in `k` | S型 grid [S10] [S11]; `J` degenerate variant [S10]; timing **[std]** |

### What the time-like columns mean

Three input columns look like time and only one of them is a duration on the projection's
own clock. None of them shifted when the projection index became a month, and each says so
here so that a reader can check the readers against the files:

| File | Column | Decision | Reason |
|---|---|---|---|
| `lapse_table.csv` | `policy_year` | **1-based contractual label; values unchanged** | It is the policy year the 約款-style duration table is written in, values 1, 2, 3. `lapse_rate_base(t)` and `default_rate(t)` map through it as `policy_year(t) = 1 + t // 12`, capped at the last row. The rates themselves are per annum and `lapse_rate_mth(t)` converts them |
| `benefit_schedule_table.csv` | `k` (was `t`) | **anniversary in years, `k = 0` at issue; values unchanged** | It is a time *point*, not a period: the 学資金 at `k` = 3 / 6 / 12 / 15 / 18 / 20 are sourced anniversaries and they feed `edu_epv(k, i)`, whose discounting is `v^(s-k)` from anniversary `k`. The column was renamed from `t` to `k` so that it cannot be mistaken for the frame's index; `claims(t, "STAGED")` reads it at `(t + 1) // 12` in the months where `(t + 1) % 12 == 0` |
| `mort_table.csv` | `age` | **attained age; values unchanged** | Not a time index at all — a table key read at `age(t) = x + t // 12` |
| `model_point_table.csv` | `policy_term`, `prem_term` | **lengths in years; values unchanged** | Counts of years, not points on the frame, and they stayed years when the frame became months: `proj_len()` is `12 x policy_term()` and `prem_period_months()` is `12 x prem_term()`. There is no `duration_init`, no entry year and no point on the time axis in this file: every model point is new business at issue and opens the frame at `t = 0` |

The readers and the four `*_file` References live on `Data`, which takes no parameters, so
each file is read **once per model** however many model points are projected; `Projection`
reaches them through its `data` Reference. `Data.input_dir()` resolves to
`_model.path.parent` at run time, so the model works from any checkout location, and an
input can be swapped by repointing a filename Reference with no formula change.

### The mortality table is a construction, not a copy

生保標準生命表2018（死亡保険用）is published by 日本アクチュアリー会 at a stable public URL, free and in
full [REG-R18] — a real contrast with `uklib`, whose CMI tables cannot be read at all
without a subscription — so anyone can retrieve it and check a rate. But the publisher's
site terms prohibit reproduction and transmission without written consent [REG-R21]. This
library therefore **cites** the table by URL, **quotes** the individual rates its worked
example needs, and **ships** a table whose `provenance` column says of each row which of two
things it is: an ANCHOR row read at a quoted age, or an INTERPOLATED row filled log-linearly
in `ln q` between the two neighbouring anchors and rounded to five decimals.

`mort_table.csv` is the **canonical construction shared across the library**, identical row
for row in every `jplib` product that ships it, so the same cell carries the same value and
the same provenance string wherever it appears. Both sexes are built the same way from their
own sourced anchors — there is no ratio and no derivation of one sex from the other, and
model points 5 and 6, which read the female column, read published female anchors rather
than a multiple of the male ones. The file is restricted to attained ages 0 to 60, which is
every age these nine model points reach: the 養老 anchor cell matures at attained age 60.

Two further distinctions survive that one, both in the `Data` docstring. The shipped rates
trace a **valuation** table carrying a margin sized to roughly a 2σ level [R2] [REG-R20],
not best-estimate experience — which is what `mort_be_factor` is for. And the table is read at
attained age (*man-nenrei*, 満年齢) while the published table is built on a nearest-birthday
(*hoken-nenrei hōshiki*, 保険年齢方式) basis [REG-R20], an understatement of up to half
a year of age that the notes name rather than hide.

## Modules that are off in the base run

Five of the notes' optional constructions are implemented and switched off, so the base run
reproduces the worked example while the machinery stays visible and testable. Each is
exercised in both positions by the tests.

| Module | Switch | Off | On at | What it does |
|---|---|---|---|---|
| Automatic premium loan (自動振替貸付) | `apl_default_mult` | `0.0` | point 8 | Scales the table premium-default rate. The advance is applied to the premium, so it moves `premiums(t)` and `loan_pp(t)` and leaves the in-force recursion alone: a default is **not** a lapse, and a policy does not lapse while the cash value can carry the premium [S1] [S10]. `apl_advance_pp(t)` is capped at the value still free of loan. Two of the six carriers do not offer it at all [S6] [S13], so the off position is a product variant and not merely a switch |
| Policy loan (契約者貸付) | `pol_loan_util` | `0.0` | point 9 (0.50) | Draws that fraction of `cv_pp(1)` at outset **[std]**, rolling up at `i_loan` = 2.40% [S9] — **a deviation from `WholeLife_JP_S`'s 2.75%**, and a deliberate one. The chassis picks 2.75% off a different carrier's vintage 貸付利率 schedule, the band a contract written under the older 予定利率 falls in, and marks the pick **[std]**. Here the rate is the 契約貸付利率 this product's own anchor carrier publishes — 2.00% → 2.40% for contracts dated on or after 2025-01-02, moved in the same release as the 予定利率 the model runs on [S9] — so the loan rate and the pricing rate come from one document. Both sets of notes give the same reason the two products need not agree: the loan rate tracks the contract's vintage 予定利率, not the market. No cash flow of its own: it nets off `death_ben_pp(t)` and the surrender benefit, which is why every benefit in the base run is gross |
| The refused waiver | `wv_frac` | `1.00` | point 4 (0.90) | Splits the 契約者 decrement between a transition to the waived state and a **termination** paying `pol_val_pre_pp(t + 1)`, the value at the closing anniversary, to the 契約者's legal heirs [S1] [S7] [S10]. `claims_ph_death` is a column of zeros while this is 1, and that zero is the product fact |
| Dynamic surrender | `dyn_lapse` | `False` | point 6 | `w x min(3, max(1, 1 + β (CV / cumprem − 1)))`, β = 2.0 **[std]**. **Inert wherever it is switched on**, which is the finding rather than a defect: the value never reaches cumulative premiums on either cell, peaking at 92.0% at maturity on the anchor cell, so an owner is never given a value reason to surrender |
| Mortality margins | `mort_be_factor`, `wv_load` | `1.00` | point 4 (1.25, 1.50) | Two inputs and not one, because the margin points opposite ways on the two lives: on the 契約者 the waiver is a cost, so an overstated rate is prudent, while on an insured child whose death benefit is roughly the reserve already held it is nearly neutral. `wv_load` is the one place a separate disability decrement is right — 高度障害 is inside the table rate [R2] [REG-R20], the waiver's third trigger 身体障害 within 180 days of a listed accident is not [S1] [S10] [S16] — so 1.00 *understates* the waiver |
| Waived-state persistency | `wv_lapse_mult` | `1.00` | point 5 (0.50) | Multiplies the surrender rate in the waived state. Almost certainly too high at 1.00: a waived policy receives every benefit for no further premium and has a strictly dominant reason to persist. Named so that it can be moved |

Three constructions are named and deliberately **not** implemented, and the model says so
by name rather than by silence. `dividend_type` is validated and the value `five_year` is
**rejected**: the ５年ごと利差配当 variant [S1] [S10] needs a 配当基準 that sits in the filed but
unpublished 算出方法書 [REG-R2], and the notes' cash flow equation carries no dividend term.
`net_cf` evaluates the validator, so such a model point fails on its first cash flow rather
than being projected silently under a 有配当 label. Reinstatement (復活) is not modelled
either, and it costs more here than on a protection product: two carriers pay a 学資金 whose
payment date fell while the policy was lapsed once the policy is reinstated [S1] [S10], so
treating every exit as terminal understates later-duration in force, premium income, staged
benefits and the maturity benefit together.

Reduction of the sum assured (*gengaku*, **減額**) is the third, and it belongs to the
chassis rather than to this product: reducing 基準保険金額 is treated as a partial surrender,
the reduced portion releasing its own 解約返戻金 and the future premium being re-rated
[S1] [S2] [S6] [S10]. It is in the composite specification and **not implemented** — there
is no reduction year, no `sum_assured_at` and no partial-surrender cash flow, so every
shipped model point carries one `sum_assured()` for the whole term. The absence is stated
because it is not free here: on the education cell a 減額 re-scales the whole staged 学資金
grid, every payment of which is a percentage of 基準保険金額, and one carrier refuses it
outright once the 学資年金開始日 has arrived [S6]. It is the chassis's mechanic, so
[`WholeLife_JP_S`](../whole_life/model.md) is where it should be built first.

## Sign convention

The notes' `CF(t)` is already **income positive** — premiums less every outgo — which is the
library-wide sign of `net_cf`, so there is no outgo-positive `liability_cf` companion to
publish here: one stream, one sign, one name.

## Naming

Cells names follow lifelib's `basiclife.BasicTerm_S` and `savings.CashValue_SE` wherever
those models have an analogue: `pols_*` for policy counts, plural nouns for cash flows,
`*_rate` for rates, `*_pp` for per-policy amounts, `claims(t, kind)` with an uppercase
`kind` string, `pols_if_at(t, timing)` for the within-year in-force reads with
`pols_if_pay_at(t, timing)` and `pols_wv_at(t, timing)` for the same read on one state. The
full mapping from the notes' symbols to the cells names is the table in the `Projection`
docstring, headed `Notes symbol`. Six library-wide rulings and five local cases needed care
beyond that.

The six rulings are the settled cross-library names, and this product carries its share of
them: `mort_rate_at_age(sx, z)` is the table lookup keyed by age; `mort_be_factor()` is the
multiplier turning the shipped valuation table into the projection basis (the model point
column keeps its own name, `mort_adj`); `prem_net_level_pp()` / `prem_net_level_at(i)` are
the actuarial net level premium, which is a pricing quantity and never a cash flow;
`check_pols_roll_fwd()` / `check_pols_roll_fwd_resid(t)` is the per-month in-force
roll-forward check; `pols_if(t)` is the **total** in force with the premium-paying subset at
`pols_if_pay(t)` / `pols_if_pay_at(t, timing)`; and `expenses(t)` is acquisition plus
maintenance only, with `claim_expenses(t)` deducted explicitly in `net_cf(t)` and published
as its own column.

Two of those change what a number means rather than only what it is called.
`pols_if` was the premium-paying state here and is now `pols_if_pay + pols_wv`, so the
`result_cf()` weight column is the whole surviving block — which is what the death, staged
and maturity benefits and the maintenance expense have always run on, and what `pols_if`
means in every other model in the library. And `expenses` no longer carries the claim
handling expense, so the column is a per-policy servicing cost in this model exactly as it
is in the other eight.

| Notes | Cells | Why |
|---|---|---|
| `W(k)` vs `Wb(k)` | `pol_val_pp` / `pol_val_pre_pp` | They differ only where a staged benefit falls due at anniversary `k`. The death benefit and the refused-waiver termination read the value *before* the payment; the surrender value reads it *after*, which is the sourced fact that each 祝金 reduces the 解約返戻金 [S7] |
| `q(t)` for two lives | `mort_rate` / `mort_rate_ph` | The notes use one symbol shape for the 被保険者's decrement at `x + t` and the 契約者's at `y + t`. They are separate cells on separate ages, and `mort_rate_at_age` is the raw lookup both read |
| `CV(k)` | `cv_pp`, not `av_pp` | This is a traditional guaranteed contract, not an account-value one, so it takes the savings family's cash-surrender-value name. `surr_val_pp` is published beside it although the two are equal, so that the absence of a 低解約返戻金型 multiplier is stated rather than inferred |
| *(no symbol)* | `pols_maturity` | The notes write the closing payment as `S x R(12n - 1)` and give it no symbol. It is named so that the in-force roll-forward closes in the final month, where the survivors neither die nor surrender |
| *(no symbol)* | `pol_val_db_pp` | The death benefit *inside* the cash-value EPV — `S` on one cell, zero on the other. Not a cash flow; it exists so that one policy-value recursion covers both constructions |

## Standardizations used

Everything below is **[std]**, and each is a lever a user with a company basis replaces.

| Input | Value | Where |
|---|---|---|
| Cash-value basis rate `i_cv` | 1.00%, the published 予定利率 adopted directly [S9] | Reference on `Projection` |
| Reference valuation rate `i_std` | 1.00%, defaulted to `i_cv` because the numeric 標準利率 could not be established [R4] [R5] | Reference on `Projection` |
| Acquisition deduction `α` | 0.25 of one annual premium, grading linearly to zero at `m` | Reference on `Projection` |
| Loan rate `i_L` | 2.40%, held flat [S9] — the *adoption* is the standardization; the rate itself is sourced. **Deviates from the chassis's 2.75%**, itself a **[std]** pick off a different carrier's vintage schedule; see "Modules that are off in the base run" | Reference on `Projection` |
| Acquisition expense | ¥50,000 per policy at issue | Reference on `Projection` |
| Maintenance expense | ¥8,000 p.a. charged as a twelfth a month, inflating at 1.0% once a policy year, on both states | Reference on `Projection` |
| Claim expense | ¥20,000 per death claim | Reference on `Projection` |
| Initial commission | 90% of the annual premium | Reference on `Projection` |
| Renewal commission | 3% of premium, policy years 2 to `m` — the anniversary months `t = 12, 24, ...` — paying state only | Reference on `Projection` |
| Surrender rates | 4% / 3% / 2% **per annum**, converted to the month as `1 - (1 - w)^(1/12)`, zero in the final month | `lapse_table.csv` |
| Within-year values | `pol_val_pre_at_m`, `surr_charge_at_m` and `cv_at_m` interpolate linearly in elapsed months between anniversaries; the 算出方法書 stating the real rule is unpublished [REG-R2] | `Projection` |
| Premium-default rates | 1.0% / 0.8% / 0.6%, gated to zero by `apl_default_mult` | `lapse_table.csv` |
| Mortality basis | The table construction, `mort_be_factor`, `wv_load` | `mort_table.csv`, model point |
| Waiver behaviour | `wv_frac`, `wv_lapse_mult`, and independence of the two lives | model point |
| Staged-benefit timing | Each payment resolved to the policy anniversary following its stated age, and paid in the single month whose close is that anniversary | `benefit_schedule_table.csv` |
| Premiums on points 6 and 7 | The net premium grossed at the anchor cell's 19.457% implied loading, rounded to the yen — ¥170,217 and ¥350,241; points 3 to 5 carry point 2's sourced premium and points 8 and 9 point 1's | `model_point_table.csv` |

`α` is re-based on **one annual premium** rather than on the sum assured, because 基準保険金額 is
a benefit-scaling unit and not a sum assured on the education cell — total premiums are 1.85
times it. At `α` = 0.25 the deduction at issue is ¥45,285 on the anchor cell, within 0.7% of
the level the savings chassis calibrated against a real published surrender-value run, so
the only genuine Japanese surrender-value calibration in this library is carried across
rather than discarded. It satisfies the three sourced quantitative constraints [S7] — below
cumulative premiums at every duration on both cells, capped at the death benefit, reduced by
each 祝金 — but not the fourth, adjectival one, that the early durations return very little:
`cv_pp(1)` is 55.4% of the first year's premium on the anchor cell. `α` is the named lever
and this is a listed model risk.

Two scope limits belong in this list because they change the answer. The APL exhaustion test
and the commission clawback are scoped to the savings chassis by the notes and are not
implemented here; `apl_advance_pp(t)` is capped at the value still free of loan in their
place. And the 学資金 whose payment date falls during a lapse, which two carriers pay on
reinstatement [S1] [S10], is out of scope with 復活 itself.

## Tests

`tests/test_model_conventions_jp.py` asserts the house style — the folder layout, the
`Data` / `Projection` split, the read-once property, the docstrings, the naming, the
`result_cf()` conventions, that every model point projects without NaN, and that
read → write → re-read reproduces the same file set and the same numbers.

`tests/test_endowment_jp.py` asserts this product:

- the notes' worked example on **both** anchor cells, hard-coded to the yen and to six
  decimals of in-force so that a reviewer can check it against the notes by eye: the two
  mortality vectors, `A(30,30)` and `ä(30,30)`, `π` = ¥145,896.34 with its 19.457% loading
  and `π_g` = ¥110,458.94 with its −1.745% one, the `W` / `SC` / `CV` table, the notes' cash
  flow rows on each cell, every line of the notes' traces, the undiscounted column totals,
  the roll-forward closing to 1.000000000, and what the waiver is worth;
- `henreiritsu()` at 92.0099% and 113.7849%, and `implied_rate()` at −0.4239% and +1.1592%;
- every one of the notes' known modelling pitfalls, one test named after each: that maturity
  is certain and not a decrement, that the surrender rate is zero in the final **month** and
  non-zero in the eleven before it, that
  `pol_val_pp(n)` at the final anniversary is
  `sum_assured()`, that the two lives read the table at two ages, that `mort_rate_ph(t)` is
  zero from `t = 12m` on and by how much that moves the block, that the waiver produces no benefit
  outgo, that waived premiums are deemed paid, that 高度障害 is inside the death rate while
  accident-caused 身体障害 is not, that a carve-out terminates the contract, that the staged
  benefit is paid to both states and terminates nothing, that it comes out of the value,
  that the schedule is data, that both death-benefit limbs are live, that `henreiritsu()` is
  contractual, and that there is no cliff;
- the roll-forward identities rebuilt independently of the checks, and all six `check_*()`
  cells with their residuals — the in-force and net-cash-flow ones per month over
  `range(proj_len())`, the policy-value, surrender-charge and staged-value ones per
  anniversary over `range(policy_term() + 1)` — on every one of the nine
  shipped model points;
- the conversion itself: that `pols_if(12j)` on the monthly grid reproduces the annual model's
  `pols_if(j)` at every anniversary, that each `*_at_m` cells returns its anniversary value
  exactly at `u = 12k`, and that premium income is unchanged because the premium is 年払;
- each optional module in both positions, and the structural product facts: no tail states —
  `list(result_cf().index) == list(range(12 * n))`, `pols_if_pay(0) == 1`,
  `pols_if_pay(12n) == 0` —
  the 短期払 point where `m < n`, the income-positive sign with no `liability_cf`, the
  `result_cf()` column order, that the enum accessors validate rather than propagating a
  typo, that `dividend_type = "five_year"` is rejected by name on the projection path, and
  that every shipped assumption row carries its own `provenance`.

The three clocks show in the test module itself: the cash-flow and in-force literals are
0-based **months**, while the `W` / `SC` / `CV` table, the 学資金 grid and every
`prem_cum_pp` literal are anniversaries **in years** and are unchanged from the annual model.
Loop and parameter names say which is meant — `t` for a month, `k` for an anniversary, `u`
for an elapsed month.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-endowment-r1
[R2]: #jplib-endowment-r2
[R4]: #jplib-endowment-r4
[R5]: #jplib-endowment-r5
[R9]: #jplib-endowment-r9
[REG-R18]: #jplib-reg-r18
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R31]: #jplib-reg-r31
[std]: #jplib-std
<!-- END generated citation links -->
