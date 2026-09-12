# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/assurance_vie_euro/technical-notes.md`](technical-notes.md); the product it
implements is specified in [`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The mechanics
> are sourced — the art. A132-11 allocation and which limb attaches to which account [R5]
> [R14, fn 12](#frlib-assurance_vie_euro-r14) [REG-R15], the art. A132-12 minimum benefit [R5] [REG-R15], the eight-year
> PPB release horizon [R5, art. A132-16](#frlib-assurance_vie_euro-r5) [R6] [REG-R16], the `effet cliquet` [S1] [S9],
> the `garantie nette` capital floor and its measurement before levies [S3] [S5] [S6]
> [S7], the death benefit being the `épargne acquise` and nothing more [S3], the absence
> of a `frais de rachat` [S2] [S3] [S10] [S13], and the annual timing of the `prélèvements
> sociaux` on euro-denominated rights [R9, art. L136-7 II](#frlib-assurance_vie_euro-r9). Every **rate** is a **[std]**
> standardization: no insurer publishes its dotation or release policy [R5] [REG-R16], no
> French euro-fund lapse experience is public [R15], no contract in the source set
> publishes a TMG [S1] [S2] [S3] [S4] [S11], and the statutory mortality tables annexed to
> the arrêté du 1er août 2006 [REG-R23] are cited but not redistributed — the shipped
> table is an INSEE-shaped proxy [REG-R24].

## Run it

```bash
python products/assurance_vie_euro/run.py            # the worked example's anchor cell
python products/assurance_vie_euro/run.py 7          # the same cell, low scenario
python products/assurance_vie_euro/run.py 8          # the high scenario, PPB building
```

```python
import modelx as mx
model = mx.read_model("products/assurance_vie_euro/Euro_FR_S")
model.Projection[1].result_cf()
```

`result_pb()` gives the crediting machinery — the `compte de participation aux résultats`,
the statutory floor rate it implies, the PPB dotation, release and balance, and the
`taux servi` credited — one row per projection **year**. `result_cf()` gives the cash
flows, one row per **month**, and `result_cf_annual()` the same frame summed into
projection years, which is what a reader lays beside the annual-step model this replaced.

## The time index

`t` is **0-based** and counts policy **months**, the library convention. `t = 0` is the
first projected month for every model point — new business and in force alike, since this
model's frame always opens at the valuation date and carries the elapsed time in
`duration_init` rather than in the index. Month `t` runs from time `t/12` to `(t + 1)/12`;
`pols_if(t)` and `av_pp(t)` are the count and the balance at its **start**, so
`av_pp(0) == av_pp_init()` and `pols_if(0) == pols_if_init()`, and `av_pp(t + 1)` — which
the death and surrender benefits are struck on — is the balance at its end.

`proj_len()` is the **number** of projected months, `12 × proj_years = 480`, so the frame
is `t = 0 … 479` and `result_cf()` has 480 rows indexed `0 … 479` with
`index.name == "t"`. `result_pb()` and `result_cf_annual()` have 40 rows indexed `0 … 39`
with `index.name == "y"`, because every column in them is a financial-year quantity.

**The product has two clocks and they are not the same clock**, which is the whole of the
conversion to a monthly grid. The crediting machinery — the `compte de participation aux
résultats`, the statutory minimum, the PPB and its eight-year vintage ledger, the declared
`taux servi`, the `frais de gestion`, the `prélèvements sociaux` — is a **financial-year**
statement, and stays one. The account movements, the expenses and the decrements are
continuous, and are monthly. Four derived clocks read off `t` and none of them is the
index:

- `proj_year(t) = t // 12`, the 0-based **projection year** `y`: the index of the annual
  layer, and the axis `fin_rate_table.csv` and `wd_start_year` are stated on;
- `is_anniv(t)`, `t % 12 == 11`: the 31 December of year `y`, which on this model's
  convention is also the policy anniversary and where every annual contractual event lands
  whole;
- `duration(t) = duration_init + t // 12`, the 0-based completed policy years, and
  `age(t) = issue_age + duration(t)`, so `age(0)` is the attained age at the valuation
  date and the age steps at the anniversary and never inside the year;
- `policy_year(t) = duration(t) + 1`, the contract's **1-based contractual policy
  year** — equally its completed policy years at the **31 December** that closes it — and
  the label the lapse table and the eight-year tax threshold are keyed to. This is the
  library's 1-based `policy_year`, not its 0-based `duration`; for a cell issued at the
  valuation date it is simply `t // 12 + 1`.

**One published column is offset by a year, deliberately.** In `result_pb()` the `ppb_pp`
column is `ppb_pp(y + 1)`, the PPB at the **end** of year `y` — the notes' Table 1 header
is literally `ppb_pp(y+1)`, because the reader wants the balance the year's dotation and
release leave behind — while `av_pp` and `guar_floor_pp` on the same row are the
start-of-year `av_pp(12y)` and `guar_floor_pp(12y)`. So the anchor cell's `y = 0` row shows
`ppb_pp` 3,637.06 even though the cells `ppb_pp(0)` is the 4,000.00 carried in. The
`result_pb()` docstring says the same thing.

The PPB vintage index `v` runs on the **financial-year** clock, like `y`: a dotation in
year `y` opens vintage `y`, and the opening balance's `ppb_vintages_init` vintages sit at
`v = −1, −2, … , −ppb_vintages_init`, falling due at `y = 7, 6, … , 0` for the default
eight. Art. A132-16 counts financial years, so the monthly grid does not reach into that
ledger.

**Two input columns are on the projection-year axis** and are read at `proj_year(t)`: the
`y` key of `fin_rate_table.csv`, which runs 0 to 39 — it is spelled `y` and not `t`
precisely because `t` is a month everywhere else in this model — and `wd_start_year` in
`model_point_table.csv` (5 on the anchor cell, 98 as the "never" sentinel, 0 on the
drawdown cell). Two are *not*: `policy_duration` in `lapse_table.csv` is the contractual
1-based label 1 … 9 that `policy_year(t)` maps onto, and `duration_init` in
`model_point_table.csv` is an elapsed count in years, 0-based by nature. `mort_table.csv`
is keyed by attained age.

**Decrements run at two speeds**, which is the library's convention: `mort_rate(t)` and
`lapse_rate(t)` are the **annual** rates of the policy year containing month `t` — the
vectors the technical notes tabulate, constant across the year's twelve months — and
`mort_rate_mth(t)` and `lapse_rate_mth(t)` are the monthly rates actually applied,
`1 − (1 − r)^(1/12)`, so that twelve of them compound back to exactly the annual rate.
That, together with the crediting machinery landing whole at 31 December, is why
`pols_if(12y)` and every financial-year quantity on this grid are exactly what the
annual-step model this replaced carried; `check_decrements_compound()` asserts the
conversion directly.

## The rate is an allocation, not an assumption

That sentence is the model.

```
fin_acct_pp(y)           = r_fin(y)·(pm_avg_pp(y) + ppb_pp(y))
tech_acct_pp(y)          = fee_pp(y) − expenses_pp(y)
insurer_tech_share_pp(y) = max(0.10·max(tech_acct_pp(y), 0), 0.045·prem_gross_pp(y))
pb_acct_pp(y)            = 0.85·fin_acct_pp(y) + tech_acct_pp(y) − insurer_tech_share_pp(y)
pb_min_pp(y)             = max(0, pb_acct_pp(y) − tmg_rate()·pm_avg_pp(y))
```

**This block is grid-invariant.** It is a financial-year statement indexed by `y`, and not
one operator in it changed when the projection went monthly; every figure it produces is
the annual-step model's, to the last bit.
Every year the insurer builds the account art. A132-11 prescribes, and the whole of that
balance must reach policyholders [R5] [REG-R15]. What the insurer chooses is only *when*:
what it does not credit this year is carried to the `provision pour participation aux
bénéfices`, and what it carried in an earlier year it may credit now. Four points of
substance, each a listed pitfall in the notes:

| | The rule | The popular error |
|---|---|---|
| Which percentage, which account | 85% of the `compte financier`; the `compte technique` less the insurer's share [R5, art. A132-11](#frlib-assurance_vie_euro-r5) | "90% of the financial account and 85% of the technical result" — EUR 3,319.09 against the correct EUR 3,071.86 at worked-example `y = 0` |
| The insurer's technical share | The **greater** of 10% of the credit balance and 4.5% of **annual** premiums — which is why `prem_gross_pp` stays a year's amount on a monthly grid | Dropping the premiums limb — EUR 108.00 against EUR 28.43 at `y = 5` |
| The financial base | `pm_avg_pp + ppb_pp`, because art. A132-14 works on average technical provisions [REG-R15] and the PPB is one of them [REG-R6] | Omitting the PPB (−EUR 41.81 at `y = 5`), or accreting the vintages as well, which pays its return twice |
| The charge | Subtracted **once**, between the PB amount and the rate | `av × (1 + ts_net) × (1 − c)`, which costs the policyholder 0.60% a year that was already taken [R14] |

Then the three levers on one rate:

```
pb_target_pp(y)     = ts_target()·pm_avg_pp(y) + fee_pp(y)
ppb_dotation_pp(y)  = max(0, pb_min_pp(y) − pb_target_pp(y))
ppb_discr_rel_pp(y) = min(max(0, pb_target_pp(y) − pb_min_pp(y)), ppb_pp(y))
ppb_forced_pp(y)    = Σ_v { ppb_vintage_pp(y, v) : v + 8 ≤ y }
ppb_release_pp(y)   = max(ppb_discr_rel_pp(y), ppb_forced_pp(y))
pb_credited_pp(y)   = pb_min_pp(y) − ppb_dotation_pp(y) + ppb_release_pp(y)
ts_net(y)           = max(tmg_rate(), ts_raw(y))
int_credited_mth_pp(t) = int_credited_pp(y) if is_anniv(t) else 0
```

The last line is all the monthly grid does here: the rate is fixed for the closing
financial year and credited at 31 December value date, so the whole of the year's
revalorisation arrives in one month and eleven months of twelve carry none of it — which
is also why a `dénouement` in one of those eleven is paid the account value without it.

A dotation and a forced release **coexist** in the worked example's first three rows —
this year's excess goes in while an eight-year-old vintage comes out — and where the
forced release wins the credited rate goes *above* the target: `y = 5` wants EUR 426.99
and must release EUR 500.00, so it credits 2.3589% against a 2.30% target.

Note what the invariant is not. `ts_net(y) ≥ ts_stat(y)` is **not** an invariant: a dotation
year credits less than the statutory floor rate and that is legal, because the balance goes
to the PPB and not to the insurer [R5] — model point 5, which opens with no PPB, does
exactly that at `y = 0`. `check_pb_allocation()` therefore states an allocation identity,
`I(y) + F(y) + D(y) − R(y) − A⁺(y) − topup(y) = 0`, not a rate inequality.

## What a mid-year `dénouement` is paid

`db_pp(t) = cv_pp(t) = av_pp(t + 1)`: the claim is always the balance closing the month of
exit. On a monthly grid that has a consequence the annual grid could not express. In the
**anniversary month** the closing balance carries the whole year's `taux servi`, exactly
as before. In the other **eleven months of twelve** it carries no in-year revalorisation
at all — which is the contractual rule, the announced floor rate `pro rata temporis`
[S1] [S2] [S3], nil at the `tmg_rate() = 0` every shipped model point carries.

That is the one place the finer grid changes an answer rather than its resolution, and it
retires a pitfall, a sensitivity and an out-of-scope bullet the annual model carried at
once. An annual step could only pay a March exit the following 31 December's balance,
which is a forward-looking payment at a date it is not yet due; it did so because the exit
and the crediting were the same instant. Measured on the anchor cell over forty years,
that correction together with the monthly collection of instalments moves `claims_death`
−4.14%, `claims_lapse` −0.55% and `liability_cf` −1.57%.

The **Afer variant** [S11] — the declared rate accrued `pro rata temporis`, one twelfth a
month — is a documented alternative rather than the base, and it is the bracket on what is
left uncertain: it gives `claims_death` −3.52%, `claims_lapse` +0.18% and `liability_cf`
−0.88% instead. It preserves the anniversary equivalence just as exactly, because the
year's interest still sums to `I(y)`, so nothing measurable decides between them — only
the sources do, and they favour the floor rate: BoursoVie's credit of the annual PB to
sums surrendered during the year is expressly conditional on the adhesion being in force
on the following 1 January [S1], which a `rachat total` is not.

## The PPB vintage ledger, and why it is a ledger

A dotation carried to the PPB in financial year `v` must be applied to mathematical
provisions or paid to policyholders **within the eight financial years following** the one
it was carried in [R5, art. A132-16](#frlib-assurance_vie_euro-r5) [R6, art. A331-9](#frlib-assurance_vie_euro-r6) [REG-R16]. The model therefore
carries `ppb_vintage_pp(y, v)`, a per-vintage balance drawn down FIFO by
`ppb_vintage_release_pp(y, v)`, so `v + 8` is a real deadline on a real balance — a
single-pot PPB with an average age meets the rule on average and breaches it on every one.
**Both indices are financial years**, and stay so on a monthly grid: A132-16 counts
financial years, so nothing here is made finer.

The statute prescribes no release order **[std]**. FIFO is the only order that satisfies the
eight-year constraint without slack, and it is what makes the ledger testable: releasing
newest-first would satisfy the aggregate recursion `Q(y+1) = Q(y) + D(y) − R(y)` exactly
while letting an old vintage sit past its deadline behind young ones that keep being spent.
`check_ppb_clock()` catches that; `check_ppb_roll_fwd()` cannot. The two are deliberately
separate recursions — `ppb_pp(y)` runs the aggregate, `ppb_ledger_pp(y)` sums the vintages
— because nothing forces them to agree, and an off-by-one in the FIFO draw breaks the tie
while leaving both numbers plausible. The anchor cell's clock closes exactly:

| `y` | Forced | Want, uncapped | Discretionary | Released | Drawn from |
|---|---|---|---|---|---|
| 0–2 | 500.00 | −137.06 → −32.52 | 0.00 | 500.00 | vintages −8 … −6, one a year |
| 3–5 | 500.00 | 77.81 → 426.99 | 77.81 → 426.99 | 500.00 | vintages −5 … −3, one a year |
| 6 | 500.00 | 606.30 | 606.30 | **606.30** | 500.00 from vintage −2, then 106.30 from vintage −1 |
| 7 | 393.70 | 736.57 | **650.58** | **650.58** | 393.70 from vintage −1, then the three dotations |
| 8–11 | 0.00 | 869.58 → 1,059.09 | 0.00 | 0.00 | the PPB is exhausted; `ts_net = ts_stat` |

The two middle columns are the two halves of `ppb_discr_rel_pp(y) = min(max(0,
pb_target_pp(y) − pb_min_pp(y)), ppb_pp(y))`. "Want, uncapped" is the raw difference
`s* B(y) + F(y) − A⁺(y)`; "Discretionary" is that difference floored at zero and capped
at the balance. They separate exactly twice on this cell and for different reasons — at
`y = 0` to `y = 2` the want is *negative*, which is what a dotation year is (the three
dotations named below are its mirror image), and from `y = 7` the *cap* binds, partially
and then to nothing. Neither is the release: `y = 6` wants 606.30 and gets it, `y = 5`
wants 426.99 and must release 500.00 because the clock outranks the target.

Twelve-year releases of EUR 4,256.88 against an opening EUR 4,000.00 plus three dotations
(137.06, 87.30, 32.52) of EUR 256.88. The opening balance is split into `ppb_vintages_init`
equal vintages carried in years `−1, −2, … , −ppb_vintages_init` **[std]** — a
steady-state construction, since a fund that has run the clock for eight years carries
roughly one eighth of its PPB in each open vintage, and no insurer publishes its own
profile. It matters: model point 6 carries the same EUR 4,000 in **four** vintages, and
nothing is forced out before `y = 4`.

## The `effet cliquet` is not "the account never falls"

What is ratcheted is **credited PB**, not the balance [S1] [S9]. Under the `garantie
nette` the account falls by the management charge in a nil-PB year, and the minimum
surrender-value tables insurers publish for exactly that case prove it: Suravenir's
994.00 … 952.99 is `1 000 × (1 − 0.006)ⁿ` truncated to the cent [S3], and MACSF's
965.15 … 955.52 is `970 × 0.995ⁿ` [S2]. Conflating the two is a pitfall, so the model
publishes two separate checks:

- `check_cliquet()` — `pb_cum_pp` is non-decreasing over each year,
  `int_credited_pp(y) ≥ 0` and `ts_net(y) ≥ tmg_rate()`. The ledger `pb_cum_pp(t)` carries
  a monthly index and steps once a year, in the month after the 31 December that credited
  the PB, so the ratchet is read at the year's boundaries. **Half of this is zero by
  construction**, because the
  `max(tmg_rate(), …)` in `ts_net` enforces the non-negativity; it is published because the
  constraint is a contractual fact, and a re-implementation that netted the charge against
  the revalorisation, or carried a negative `pb_acct_pp` through to the account, would break
  it. The ratchet half compares two independent recursions and is not by construction.
- `check_guar_floor()` — the weaker and correct statement about the balance,
  `av_pp(t) + soc_levy_cum_pp(t) ≥ guar_floor_pp(t)` at **every month**: a genuine
  inequality that nothing in the recursions enforces, measured **before** cumulative social
  levies because the published minimum surrender-value tables are [S1] [S2] [S3]. The floor
  steps down once a year, at the anniversary, while the account only catches up at the same
  date, so the monthly sweep looks at the tightest month of each year rather than at the
  year-end alone. On the anchor cell it reaches EUR 99,061.85 at `t = 144` against
  EUR 139,600.82 — it never binds on a path with a positive `taux servi`, and knowing that
  it does not bind is the reason to check it.

## `Prélèvements sociaux` are inside the account and outside `net_cf`

The 17.2% levy [S3] is withheld **as the interest is credited**, every year, whether or
not anything is withdrawn, because the rights are expressed in euros; only the UC part is
deferred to `dénouement` [R9, art. L136-7 II](#frlib-assurance_vie_euro-r9). This is the euro fund's signature mechanic
and the commonest foreign-model error. It sits **inside the account roll-forward**,
because it is money that genuinely leaves the contract each year and a model that defers
it to surrender overstates the account and every benefit measured on it — and **outside
`net_cf`**, because it is a policyholder tax the insurer withholds and remits to the State
rather than a benefit or an insurer expense. Its own `soc_levy` column lets a fund-level
asset projection add it back in one step.

The base is the interest actually inscribed on the contract, i.e. **net** of the management
charge **[std]**: art. L136-7 fixes the timing but not the base [R9], and no retrieved
product document says which it is (product-spec footnote 13). The next error along is
levying it on the *account*: 17.2% of EUR 100,000 is EUR 17,200, while 17.2% of the
worked example's EUR 2,827.60 at `y = 0` is EUR 486.35.

On the monthly grid the annual timing is **visible** rather than implicit. Art. L136-7 II
charges the products "lors de leur inscription au bon ou contrat", and the inscription is
the 31 December crediting, so `soc_levy_mth_pp(t)` is nil in eleven months of twelve and
carries the whole of the year's levy in the twelfth, moving with the interest it is struck
on. The `soc_levy` column of `result_cf()` is zero in 440 of its 480 rows, and that shape
is what an annual contractual event looks like on a finer grid.

## Behaviour keys on the gap, not on the level

```
lapse_dyn_add(t)  = lapse_dyn_a·max(0, ref_rate(y) − ts_net(y) − lapse_dyn_tol)
lapse_rate(t)     = min(lapse_cap, lapse_rate_base(t) + lapse_dyn_add(t))
lapse_rate_mth(t) = 1 − (1 − lapse_rate(t))^(1/12)
```

`lapse_rate(t)` is the **annual** rate, and `lapse_rate_mth(t)` is what the recursion
applies. The gap the dynamic term keys on is read once a year, at `proj_year(t)`, so the
annual rate is one number for the whole policy year and only the monthly conversion varies
inside it.

**The duration-8 step** in `lapse_rate_base` is the tax threshold, not a behavioural
guess: the reduced 7.5% rate and the EUR 4,600 / EUR 9,200 annual allowance both switch on
at eight years [R10] [R11] [REG-R40]. It is indexed by
`policy_year(t) = duration_init + t // 12 + 1`, the **contract's** 1-based policy year,
not by `t` — the anchor cell is five years in, so the step is **twelve months wide** and
covers `t = 24 … 35`. A model reading the table at `t` would put it in the third *month*
instead of the third *year*, which is the likeliest indexing error this grid can make.

**The dynamic term** is additive in the gap between the market reference rate and the
`taux servi`, one-sided, and capped. The sign of the relationship is observed rather than
assumed: in 2025 the euro rate was 2.63% while the Livret A averaged 2.20% and fell to 1.7%
in August and 1.5% in February 2026 [R14] [R15], and euro supports turned to a
**+EUR 6.4 bn** net inflow after five consecutive years of net outflow [R15]. The magnitude
has no public calibration, and `lapse_dyn_a = 4.0`, `lapse_dyn_tol = 0.25` point and
`lapse_cap = 30%` are the most consequential **[std]** values in the model. Because the
credited rate and the surrender rate move together, the model carries a feedback loop the
deterministic run samples only once.

## What is out of scope, and why

**No positive-TMG model point is shipped**, and that is a decision rather than an omission.
No contract in the source set publishes a TMG: the two Suravenir notices state no
guaranteed interest rate at all [S3] [S4], BoursoVie names a TMG "annoncé en début d'année"
without its value [S1], MACSF names a board-set art. A132-3 rate without giving it [S2],
and Afer names a `Taux Plancher Garanti` without giving it [S11]. So the composite's TMG is
0.00% **[std]** and every model point carries it.

The lever is implemented as the notes specify, and at `tmg_rate() = 0` the two things the
notes call the TMG coincide: the art. A132-12 subtraction of "interest already credited to
mathematical provisions" [R5] [REG-R15], which belongs to a `taux technique` fixed at
subscription, and the floor on the year's *total* revalorisation, which is what art.
A132-2/A132-3 actually guarantees [R3] [R4] [REG-R18]. Above zero they are different
quantities, and the product specification is explicit that the ACPR's average `taux
technique` of 0.32% must not be substituted for a TMG [R14] (product-spec footnote 7). A
positive-TMG cell would have to choose, so none is shipped and `insurer_topup_pp` — the
cells that would carry the guarantee's cost to the insurer — is nil throughout. On a
monthly grid a positive TMG would also have to be credited month by month inside the year
and squared up at 31 December against `ts_net`; no such cells is shipped either, for the
same reason. Also out of scope, per the notes:

- **The HCSF surrender-suspension power** under art. L631-2-1 5° ter [R8] [REG-R13]. No
  published trigger a deterministic model could key off, and precisely what would change a
  mass-lapse answer — so a mass-lapse run here is a **pre-management-action** number.
- **The exceptional PPB `reprise`** of art. A132-16-1 [REG-R16], available only on a
  negative life technical account *and* an uncovered SCR: a solvency-stress management
  action, not a projection assumption.
- **`Avances`.** All three insurers push the terms into a separate document that was not
  retrieved [S1] [S2] [S3], so `avance_on()` validates rather than inventing a rate, a
  ceiling and a duration.
- **`Arbitrages` and the UC compartment**, which is the sibling product
  `assurance_vie_uc`; and the **UC-holding bonus**, often 100 bp and sometimes above 200 bp
  [R14], because no retrieved contract publishes its grid.
- **Sub-annual crediting finer than the month**, such as BoursoVie's daily compounding
  [S1]: an approximation the monthly grid narrows rather than removes.

There is **no maturity decrement**: the euro support has no term, and the contract's stated
maturity, where one exists, is renewable annually without limit [S6]. The projection stops
at `proj_len()` and the survivors are paid nothing, because that ending is a modelling
truncation and not a contractual event.

## Inputs are external files

The four input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Euro_FR_S/` holds nothing but formulas:

```
products/assurance_vie_euro/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  lapse_table.csv
  fin_rate_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  Euro_FR_S/                   <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`. `Projection` is parameterized by
`point_id`, so the CSV readers live in an unparameterized **`Data`** Space and each file is
read once per model rather than once per model point; a test counts the reads.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |
| `fin_rate_file` | `fin_rate_table()` | `fin_rate_table.csv` |

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Eleven model points. **Point 1 is the notes' worked example** — M55 at duration 5, EUR 100,000, EUR 2,400 p.a. in, EUR 3,000 p.a. out from year `y = 5`, 0.60% charge, 2.30% target, EUR 4,000 PPB in eight vintages. Point 2 is the same cell on the `garantie brute`; 3 targets 2.90%; 4 is paid up; 5 opens with no PPB; 6 carries four vintages instead of eight; 7 and 8 are the low and high scenarios; 9 is a small new-business cell with a 0.50% entry charge and a 0.80% management charge; 10 is a drawdown cell, F82, EUR 250,000 with EUR 6,000 a year out; 11 is point 1 carrying 250 policies | anchor cell **[std]**, product-spec "Anchor model cell"; variants from the notes' pitfalls and sensitivities |
| `mort_table.csv` | Base annual mortality by sex and age 18–120, capped at 1 | **[std]** Makeham proxy shaped like French population mortality [REG-R24], anchored so that the 80% best-estimate factor gives the notes' `q(M, 60) = 0.0060` placeholder exactly — *not* TH00-02/TF00-02 or TGH05/TGF05, which are cited [REG-R23] and not redistributed |
| `lapse_table.csv` | Base **annual** surrender by completed policy duration: 4% at 1–7, **8% at 8**, 5% at 9+, spread over the policy year's twelve months at `lapse_rate_mth`. `policy_duration` is the contractual 1-based label `policy_year(t)` maps onto, not the frame's `t` | levels **[std]**, no public French euro-fund lapse experience [R15]; the duration-8 step is the tax threshold [R10] [R11] [REG-R40] |
| `fin_rate_table.csv` | Three scenarios × 40 years of `r_fin` and `ref_rate`, keyed by the model's own 0-based projection **year** `y`, 0 to 39 — spelled `y` and not `t`, because `t` is a policy month everywhere else in this model. Base 3.30% → 2.30% over twelve years then level; low 3.00% → 1.40%; high 4.00% level. `ref_rate` 2.20% throughout | **[std]** scenarios anchored to the ACPR's `taux de rendement de l'actif` — 2.8% in 2025, half of undertakings between 2.4% and 3.3% [R14] — and the 2025 average Livret A [R14]. Not forecasts |

Note what is **not** in a file. The crediting rule that actually drives this product — the
target `taux servi`, the dotation and release policy, the FIFO order, the expense loadings,
the dynamic-surrender coefficients — lives in model point columns and `Projection`
References rather than in a rate table. That is not an oversight: **none of it is
published.** Only the outer bounds of the discretion are public — at least 85% of the
`compte financier` and the A132-11 technical share must reach policyholders [R5], and the
PPB must be released within eight years [REG-R16] — and between those bounds every value is
a standardization. Putting them where a reader trips over them is better than filing them
in a table that looks like data. Each rate table does carry a `provenance` column saying in
words what its numbers are; no formula reads it, and it is there so a file lifted out of
this directory still says what it is.

## The worked example

`tests/test_assurance_vie_euro_fr.py` asserts every row of all four tables to the cent and
every rate to the fourth decimal of a percentage. The notes' Tables 1 and 2 are
financial-year statements, and the monthly grid leaves every figure in them exactly where
the annual grid put it; what changed is the index each is read at. The year-5 trace, where
every lever is active at once — year 5 being the twelve months `t = 60 … 71`:

| Step | Value |
|---|---|
| `pm_avg_pp` = 124,354.884701 + 1,200 − 1,500 | 124,054.884701 |
| `fee_pp` = 0.60% × base | 744.329308 |
| `expenses_pp` = 0.35% × base + 24 × 1.015⁵ | 460.046913 |
| `fin_acct_pp` = 2.80% × (base + 1,756.875780) | 3,522.729293 |
| 85% of it | 2,994.319899 |
| `tech_acct_pp` | 284.282396 |
| `insurer_tech_share_pp` = max(28.428, **108.000**) | 108.000000 |
| `pb_acct_pp` = `pb_min_pp` | 3,170.602295 |
| `ts_stat` | 1.955806% |
| `pb_target_pp` = 2.30% × base + `fee_pp` | 3,597.591656 |
| Discretionary release wanted / vintage falling due | 426.989361 / **500.000000** |
| `pb_credited_pp` | 3,670.602295 |
| **`ts_net`** | **2.358853%** |
| `int_credited_pp` | 2,926.272987 |
| `soc_levy_pp` | 503.318954 |
| `av_pp(72)` | 126,177.838734 |

The whole of that `int_credited_pp` and `soc_levy_pp` lands in **one month**, `t = 71`.
The other eleven months of year 5 move the account by the level instalments alone,
EUR 200.00 in and EUR 250.00 out, netting to −EUR 50.00 a month — and the
mid-month-weighted base, 124,054.8847, is literally the balance at the middle of the year,
the opening of month 66.

| Policy year 5 (`t = 60 … 71`) | Annual grid | Monthly grid |
|---|---|---|
| `av_pp` entering the year | 124,354.88 | 124,354.88 |
| `ts_net` | 2.3589% | 2.3589% |
| `av_pp` leaving the year | 126,177.84 | 126,177.84 |
| Premiums | 1,771.44 | 1,723.18 |
| `Rachats partiels` | 2,214.30 | 2,153.97 |
| Death claims | 862.56 | 829.63 |
| Surrender claims | 4,613.46 | 4,561.82 |
| Expenses | 339.56 | 330.31 |
| `liability_cf` | 6,258.43 | 6,152.55 |

Every state figure is unchanged and every flow figure moved down, which is the whole of
what the conversion did: the instalments are collected from a block that decrements every
month, the expense is borne by the in force of each month, and a claim falls at the end of
the month of exit carrying no in-year revalorisation.

The `taux servi` from a different direction —
`0.85·fin/base + (technical share)/base − fee_rate + (PPB flow)/base` — gives
`2.413706% + 0.142100% − 0.600000% + 0.403047% = 2.358853%` at `y = 5`, and
`2.082500% + 0.145673% − 0.600000% + 0.000000% = 1.628173%` at `y = 8` with the PPB
exhausted. The twelve-year account identity: credited interest EUR 31,800.82 and social
levies EUR 5,469.74, whose ratio is `0.172000` exactly, and
`100,000.00 + 28,800.00 − 21,000.00 + 31,800.82 − 5,469.74 = 134,131.08` — the same total
reached the other way from PB credited gross of the charge, EUR 40,538.97, less `frais de
gestion` of EUR 8,738.15.

Read year 8 for what it says. At `r_fin = 2.45%` and a 0.60% charge the most the account
could grow by is 1.85%; the model credits 1.6282%, and the 0.2218-point wedge is exactly
`0.15 × 2.45% = 0.3675%` retained from the `compte financier` less the 0.1457% of the
technical account that flows back [R5, art. A132-11](#frlib-assurance_vie_euro-r5). **A 2.30% target is not payable on a
2.45% asset return without the PPB**, and the model steps down rather than pretending
otherwise. The two management actions that would soften it — realising capital gains into
the year's financial account, and the `réserve de capitalisation` [REG-R6] — are outside it.

## Sign convention

`net_cf` is **income-positive**, the library's convention. `liability_cf` is the notes'
outgo-positive `CF(t)`, published verbatim, and `net_cf(t) == −liability_cf(t)` exactly:
`liability_cf = claims_death + claims_lapse + withdrawals + expenses − premiums`. Two
things are reported beside the flows and are **not** in either: `int_credited`, a state
movement rather than a settlement, and `soc_levy`, a policyholder tax. `withdrawals` is an
**owner election, not a claim** — money the policyholder asked for out of a balance the
policyholder owns — while a `rachat total` ends the contract and appears as
`claims_lapse`. Both leave the fund; keeping them apart is what lets a reader see the
difference between elective drawdown and exit.

## Naming

Most names carry across from the notes unchanged; these needed care.

| Notes symbol | Cells | Why |
|---|---|---|
| `t`, `y` | (the cells argument), `proj_year(t)` | `t` is the 0-based policy **month** and `y = t // 12` the projection year. A cells that states a **financial-year account** takes `y`; a cells that states a month takes `t`; the decrement rates take `t` and return the year's annual rate. The mixed convention is deliberate — art. A132-11 builds one participation account per financial year and A132-16 counts financial years, so restating that machinery at 480 months would carry two clocks in one signature |
| (none) | `is_anniv(t)` | `t % 12 == 11`, the 31 December of year `y` and this model's policy anniversary: where the revalorisation, the levy and the charge land whole |
| `B(y)` | `pm_avg_pp(y)` | Not an average of anything the model computes: it is the opening balance plus each month's movement at the mid-month weight `prem_wt_mth(k) = (11.5 − k)/12`, which on a level schedule is `AV(12y) + 0.5·P(y) − 0.5·W(y)`. `av_avg_pp` would suggest it came out of `av_pp_at` |
| `ŝ(y)`, `σ(y)` | `ts_stat(y)`, `ts_net(y)` | Both are **net of the management charge**. `pb_min_pp` is gross of it, and the charge is subtracted once, on the way from a PB amount to a rate |
| (the `max`) | `ts_raw(y)`, `insurer_topup_pp(y)` | The two halves of `max(g, ·)`: what the allocation produces, and what the guarantee costs the insurer in euros when it cannot |
| `Q_v(y)` | `ppb_vintage_pp(y, v)`, `ppb_vintage_release_pp(y, v)`, `ppb_ledger_pp(y)` | The ledger, the FIFO draw and the ledger's total — the last computed independently of `ppb_pp` so that the check compares two things. Both indices are financial years |
| `W(y)`, `P(y)` | `withdrawals_pp(y)`, `prem_to_av_pp(y)` | The **year's** amounts; `withdrawals_mth_pp(t)` and `prem_to_av_mth_pp(t)` are the month's twelfth of each, and `expenses_mth_pp(t)` likewise. The `*_mth_pp` suffix marks the monthly instalment of a per-policy annual amount. `wd_prog_pp()` is the *elected* amount before the start year and the balance cap apply |
| `q(y)`, `w(y)` | `mort_rate(t)`, `lapse_rate(t)` / `mort_rate_mth(t)`, `lapse_rate_mth(t)` | The unsuffixed name stays the **annual** rate the notes tabulate, read at `age(t)` and `policy_year(t)`; the `*_mth` companion is `1 − (1 − r)^(1/12)`, the rate actually applied in the month. Naming the monthly rate `lapse_rate` is a retired spelling the conventions suite rejects |
| `claims(t, "LAPSE")` | `claims_lapse` | Named for the `kind` argument that produces it, and for the library's `pols_lapse` decrement — not `claims_surr` |
| `d + t // 12 + 1` | `policy_year(t)` | The contract's 1-based contractual policy year — equally its completed years at the 31 December that closes it — which is what the tax threshold and the lapse table are keyed to. The library's 1-based `policy_year`, not its 0-based `duration` (`duration_init + t // 12`), and distinct from both `t` and `y` |
| (none) | `result_cf_annual()` | `result_cf()` summed into projection years: every flow column the total of its twelve months, `pols_if` the count entering the year. The frame regrouped, never a second projection |

## Standardizations used

Everything in this list is **[std]**: the 2.30% target `taux servi` and holding it level;
the crediting rule itself — dotation of the excess over the target, discretionary release
up to the target, FIFO order, no year-on-year cap on the rate; the per-policy attribution
of a collective PPB and its split into eight equal vintages; the 0.60% management charge
level and the `pro rata temporis` charge base; the nil TMG and nil entry charge on the
composite; the `garantie nette` as the composite's guarantee form and its seeding at
`av_pp_init` for an in-force cell; the **monthly grid** and the mid-month weight
`(11.5 − k)/12` from which the notes' 0.5 follows; the constant-force conversion
`1 − (1 − r)^(1/12)` of every annual decrement, since no retrieved French source states
one; the contractual `pro rata temporis` floor rate paid to a mid-year exit, nil at a zero
TMG, with the Afer top-up named as the documented alternative; collecting the `versement`
and the `rachat partiel programmé` in twelve equal instalments and striking the withdrawal
cap once a year on the year-open balance; accruing the expense a twelfth a month while the
inflation factor steps at the anniversary; the levy base being interest net of the charge;
the mortality table, the 80% best-estimate factor and age last birthday; the lapse levels
and all three dynamic-surrender parameters; expenses of EUR 24 a policy a year inflating at
1.5% plus 0.35% of the average balance; the three financial scenarios;
`proj_len() = 480` projected months (40 years);
death before surrender as the processing order; and no `avance` take-up, no UC-holding
bonus and no PPB accretion on the vintages.

## Tests

`tests/test_assurance_vie_euro_fr.py` asserts all four tables of the worked example row by
row, the year-5 trace at full precision, the `taux servi` decomposition from the other
direction, the twelve-year levy and account identities, the month-0 aggregate
roll-forward, the guarantee floor and the decrement extract — then one test per pitfall the
notes list: the charge deducted twice, the closing-balance crediting base, the statutory
split reversed, the 4.5%-of-premiums limb dropped, the PPB left out of the financial base
or accreted, a LIFO release or an overdue vintage, the statutory minimum lost rather than
allocated, the levy deferred to surrender or struck on the account, the cliquet tested as
"the account never falls", a death-benefit uplift, and the mid-year exit taking a full
year's rate — which is now asserted the other way round, as
`claim_pp(t, "LAPSE") == av_pp_at(t, "AFT_WD")` in a non-anniversary month.

Then one test per timing decision the monthly grid forced: that twelve monthly decrement
rates compound back to the annual ones and that `pols_if(12y)` therefore reproduces the
annual recursion written out from the model's own annual vectors, on every model point;
that the mid-month weights sum to exactly one half and the two neighbouring conventions do
not; that the `versement` and the `rachat partiel` are collected in twelve instalments and
the withdrawal cap is struck once a year; that the expense accrues a twelfth a month while
its inflation factor steps at the anniversary; that the `frais de gestion` and the
`prélèvements sociaux` land whole at 31 December and nowhere else; that the annual layer is
keyed by `y` and the monthly layer by `t`, cells by cells; that `result_cf_annual()` is the
monthly frame regrouped; and that the duration-8 surrender step is twelve months wide.
Then the variants each shipped model point carries, and all eight invariant checks on every
one of the eleven. The frame is pinned there too: `result_cf()` is indexed `0 … 479` and
has `proj_len() = 480` rows on every model point, and `result_cf_annual()` and
`result_pb()` 40.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #frlib-assurance_vie_euro-r10
[R11]: #frlib-assurance_vie_euro-r11
[R14]: #frlib-assurance_vie_euro-r14
[R15]: #frlib-assurance_vie_euro-r15
[R3]: #frlib-assurance_vie_euro-r3
[R4]: #frlib-assurance_vie_euro-r4
[R5]: #frlib-assurance_vie_euro-r5
[R6]: #frlib-assurance_vie_euro-r6
[R8]: #frlib-assurance_vie_euro-r8
[R9]: #frlib-assurance_vie_euro-r9
[REG-R13]: #frlib-reg-r13
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R18]: #frlib-reg-r18
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R40]: #frlib-reg-r40
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
<!-- END generated citation links -->
