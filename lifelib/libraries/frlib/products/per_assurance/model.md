# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/per_assurance/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> mechanics are sourced — the *blocage* and the seven `L. 224-4` early-release cases
> [R3], release paid as a single payment of all or part of the eligible rights
> [R5 D. 224-4](#frlib-per_assurance-r5), the 1 % transfer indemnity nil after five years from the first
> *versement* [R3 L. 224-6](#frlib-per_assurance-r3), the 0 % maximum technical rate for a PER tariff
> [R9 A. 142-1](#frlib-per_assurance-r9), the regulatory de-risking grid and its four qualified profiles
> [R6 art. 1](#frlib-per_assurance-r6), the euro capital floor stated net of loading and net of charges levied
> [S1] [S3] [S7], death closing the plan [R3 L. 224-4 II](#frlib-per_assurance-r3), the compartment-3
> annuity-only rule [R3 L. 224-5](#frlib-per_assurance-r3) [S2], and the €110 monthly *quittance* commutation
> threshold [R10 A. 160-2](#frlib-per_assurance-r10). Every **rate** is a **[std]** standardization: the *encadré*
> requires charge **maxima** to be disclosed and caps no level [REG-R30], no sampled
> insurer publishes an annuity rate card [S1] [S2] [S4] [S7], TH 00-02 / TF 00-02 and
> TGH05 / TGF05 are cited and not shipped [REG-R21] [REG-R22] [REG-R23], and no public
> French experience exists for PER early-release, transfer or annuitisation behaviour.

## Run it

```bash
python products/per_assurance/run.py            # the notes' worked example
python products/per_assurance/run.py 6          # the annuity that is not commuted
python products/per_assurance/run.py 10         # the cell whose death floor bites
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/per_assurance/PER_FR_S")
model.Projection[1].result_cf()
```

Four frames come out of it, two on the month and two on the plan year.
`result_cf()` gives the cash flows, one row per **month**, and its `pols_if` column is the
count each row **opens** with, which is the weight that row's flows carry;
`result_state()` gives the glide path and the two supports, also monthly, where five of
its ten columns move in the month that opens a plan year and nowhere else.
`result_cf_annual()` sums the cash flows into plan years, and `result_state_annual()`
reads the state frame at the two months that determine each of its columns — that last one
is the technical notes' worked-example table, whose `pols_if_eoy` column is the notes'
end-of-year `l(t)`. `result_settlement()` gives the settlement at the horizon, down to the
commutation test.

## The time index

`t` is **0-based** and counts **plan months**, as in every monthly model in this library:
`t = 0` is the first projected month, month `t` runs from time `t` to time `t + 1`, and
`proj_len() = 12 × proj_years()` is the **number** of projected months rather than the last
index. Both monthly frames are `range(proj_len())` — `t = 0 … proj_len() − 1`,
`proj_len()` rows — so the anchor cell's twelve plan years are 144 months labelled
`t = 0 … 143`, and its settlement falls on row 143. Nothing is indexed at `t = −1`: the
state carried into the first month is the `"BEF_REBAL"` timing of `av_euro_pp_at`,
`av_uc_pp_at`, `av_pp_at` and `death_floor_pp_at`, which returns the model point's `*_init`
columns at `t = 0` and last month's closing balance afterwards.

Three clocks run beside `t` and none of them is it:

- `duration_mth(t) = t` is the months elapsed. It exists so that the monthly models in this
  library share one vocabulary, and so that the other two read as `// 12` of it rather than
  as a bare `t // 12`.
- `duration(t) = duration_ifo + t // 12` is the completed years since the **first
  *versement***, 0-based in lifelib's sense — nil through the plan's first year. An
  in-force cell opens the frame at `t = 0` like any other; its history is carried in
  `duration_ifo`, not in a frame offset, which on the finer grid is worth more rather than
  less: there is no `proj_start()` here and no month of the frame that is not projected.
- `plan_year(t) = duration(t) + 1` is the plan's own **1-based** *ancienneté* year, the
  contractual label the *ancienneté* schedules are written in. It keys `exit_table.csv`
  and the transfer indemnity window (`plan_year(t) < 5`), and it is the only place a
  1-based year appears in a formula.

All three step at the plan **anniversary** and are constant through the twelve months in
between, and so are `years_to_horizon(t) = proj_years() − t // 12` and the attained age
`age(t) = age_init() + t // 12`.

**Two months of each plan year carry its annual events, and they are not the same month.**
`is_plan_boy(t)` — `t % 12 == 0` — is the month that opens a plan year, where the
*versement* arrives and the balance is rebalanced onto the glide path. `is_anniv(t)` —
`t % 12 == 11` — is the month that closes it, where the management charge is levied and,
at `t = proj_len() − 1`, where the plan is liquidated. The *garantie plancher* base moves
at those two months and nowhere else. Everything that is not contractually annual — the
crediting of both supports, the three decrements, the maintenance expense — happens every
month, which is what the finer grid is for.

**The input CSVs.** No column in any of the five is the frame's `t` under another name,
and none of them shifts with it:

| File | Column | Decision |
|---|---|---|
| `allocation_grid.csv` | `years_to_horizon` | Unchanged, and unchanged by the monthly grid too. It is a whole-years-**remaining** key, read at `k(t) = n − t // 12`, which runs from `n` through the first plan year down to 1 through the last, constant inside each |
| `exit_table.csv` | `duration` | Unchanged. Its first row is the plan's **first** year, so it is a 1-based *ancienneté* label read at `plan_year(t)`, not the 0-based `duration(t)`; the rates it holds stay **annual** and are converted in the `*_rate_mth` cells |
| `mort_table.csv`, `annuity_factor.csv` | `age` | Unchanged. Attained age, read at `age(t)` — which steps once a plan year — and at `retirement_age()`. `annuity_factor.csv` holds a count of **annual** instalments and is not a function of the projection step at all |
| `model_point_table.csv` | `age`, `retirement_age` | Unchanged. Ages, not points on the frame |
| `model_point_table.csv` | `duration_ifo` | Unchanged. An elapsed count in whole **years**, already 0-based: two completed years is `2` |
| `model_point_table.csv` | `premium` | Unchanged. An amount **per year**, collected whole in the month that opens each plan year. No sourced modal factor exists for this product, so a `premium_freq` column is a documented extension rather than part of the monthly grid |

Every key in that table is a whole year or an age, which is why the finer grid needed no
input change: each is read at the plan year containing the month. The transfer-indemnity
window is the one that looks like it might have moved and provably has not — because
`duration_ifo` is a whole number of years, `plan_year(t) < 5` holds exactly when
`12 × duration_ifo + t < 48`, so the window is the same to the month on either grid.

## Accumulation with a two-way exit

That sentence is the product, and it is the reason this model looks unlike the other
savings models in the library.

The plan is **blocked** until the `L. 224-1` maturity [R3]. There is no surrender right,
no surrender charge and no market value adjustment, and the contracts say so in terms:
the accumulation phase carries "no surrender right except in the statutory cases"
[S2] [S3] [S4] [S7]. So there is **no `lapse_rate` and no `claims_lapse` anywhere in
`PER_FR_S`**, and `test_there_is_no_lapse_machinery_anywhere` asserts their absence
rather than leaving it to inspection.

What leaves the book instead are two decrements that are not the same event and do not
pay the same amount:

| | `early_release_rate` | `transfer_out_rate` |
|---|---|---|
| What it is | *Déblocage anticipé* on one of the seven `L. 224-4` cases [R3] | Transfer of acquired rights to another PER [R3 L. 224-6](#frlib-per_assurance-r3) |
| Trigger | A listed event — death of a spouse, invalidity, serious illness of a dependent child, over-indebtedness, exhaustion of unemployment rights, business liquidation, purchase of the main residence | The holder's election, at any time |
| Charge | **None** [S2] [S3] [S7] | 1 % of acquired rights while `plan_year(t) < 5`, nil after [R3 L. 224-6](#frlib-per_assurance-r3) |
| Pays | The **whole** account value | `A(t) · (1 − ι(t))` |
| Compartment 3 | Reduced — the main-residence limb is closed to it [R3 L. 224-4 I 6°](#frlib-per_assurance-r3) | Unchanged |
| Where the money goes | Out of the regime | Stays in the regime: the *blocage*, the compartments and the exit conditions travel with it |

Using one decrement for both, or naming either a lapse, silently attaches the wrong
payment formula to half the exits — and they dominate the run-off. At 2.60 % a year
combined they remove about a quarter of the book over the anchor cell's twelve years, far
more than mortality; the aggregate anchor is 2.62 % of accumulation-phase provisions
leaving every year [R22]. The two rates stay **annual** — they are what `exit_table.csv`
tabulates — and are applied month by month at the constant-force conversion, so the total
they remove over a plan year, and the in force at every anniversary, is exactly what the
annual grid produced. What the finer grid moves is the **split** between the three
decrements, because the ordered chain is walked twelve times with small steps instead of
once with large ones: over the anchor cell's first plan year deaths fall 1.19 %, releases
0.23 %, and transfers rise 0.98 %, summing to the same total.

Only the main-residence case of the seven is discretionary, and none of them responds to
investment performance, so a dynamic moneyness multiplier would be a category error on
`early_release_rate`. The behavioural lever that does exist on this product — the holder
moving the declared retirement date, which re-cuts the whole allocation immediately
[R5 D. 224-3](#frlib-per_assurance-r5) [S3] [S4] — has no public calibration and is not modelled.

## The glide path is an input table

`allocation_grid.csv` is keyed by (`allocation_profile`, `years_to_horizon`) and gives
`euro_share` and `uc_share`. `alloc_euro(t)` is a lookup, not a formula.

```
k(t) = n − t // 12
a(t) = allocation_grid[allocation_profile, k(t)].euro_share
```

The key is **whole years** to the horizon, so `a(t)` is constant through the twelve months
of a plan year and steps only at the anniversary.

That is deliberate, and it is the single most important design decision in this model.
*Gestion pilotée par horizon* is the **default management by law** [R3 L. 224-3](#frlib-per_assurance-r3), the
arrêté fixes four qualified profiles and a minimum low-risk share by distance to the
declared liquidation date [R6 art. 1](#frlib-per_assurance-r6), and **in this market the regulatory grid is not a
floor insurers beat; it is the product** — Suravenir reproduces it verbatim [S7] and
Generali's profiles hit exactly those percentages over exactly those bands [S2]. But the
anchor contract sits above it on **twenty one-year bands** rather than four [S1], and an
insurer may restate a profile's allocation unilaterally [S3] [S4]. A published grid is a
snapshot. Putting it in a file makes substituting one a table edit.

| Profile | `k > 10` | `10 ≥ k > 5` | `5 ≥ k > 2` | `k ≤ 2` |
|---|---|---|---|---|
| `prudent` | 30 % | 60 % | 80 % | 90 % |
| `equilibre` | — | 20 % | 50 % | 70 % |
| `dynamique` | — | — | 30 % | 50 % |
| `offensif` | — | — | 30 % | 50 % |

`dynamique` and `offensif` are shipped **identical**, which is what the arrêté says
[R6 art. 1](#frlib-per_assurance-r6) rather than an oversight.

**The boundary belongs to the tighter band** **[std]**: `k = 10` reads 20 %, `k = 5` reads
50 %, `k = 2` reads 70 %. R6's part (a) grid *was* extracted — percentages and band
headings both [research §5] — but the headings as rendered read "≥ 10 years out" and
"from 10 years out", which overlap at `k = 10`, and the same at 5 and at 2. The text
therefore does not say which band a boundary year falls in, the conservative rule is the
model's own, and the looser reading understates the euro share for a full year at each of
three transitions.

"Low risk" is realised wholly as the euro support **[std]**. The definition of *actifs
présentant un profil d'investissement à faible risque* is delegated to an arrêté that was
not retrieved [R5 D. 224-3](#frlib-per_assurance-r5), and the two contract definitions found disagree — SRRI ≤ 3
[S7] against ≤ 2 including the euro fund [S3]. Realising the bucket as the euro support is
the most conservative reading of both and keeps the model to two supports. The unlisted
minimum that bites since 24 October 2024 [R6 part (b)](#frlib-per_assurance-r6) [R7] is not carved out of the UC
bucket.

## The rebalancing, and which support pays for it

```
m(t)   = a(t)·A⁻(t) − E_eu⁻(t)
arb(t) = arb_rate·|m(t)|
E_eu   = E_eu⁻(t) + m(t)          + a(t)·V_net                     (m ≥ 0)
E_uc   = E_uc⁻(t) − m(t) − arb(t) + (1 − a(t))·V_net
```

in the month that **opens** a plan year, and with the roles of the two supports exchanged
when `m(t) < 0`. In the other eleven months `m(t) = 0`, `arb(t) = 0` and `V_net = 0`, so
the two supports simply carry forward: the rebalancing is a contractual annual event and is
not spread. A `⁻` is the balance carried into the **month** —
`av_pp_at(t, "BEF_REBAL")` and its two support halves, which are the model point's opening
state at `t = 0`. Two conventions, both **[std]** and both load-bearing.

**The arbitrage charge comes off the *source* support.** The destination receives the
switch in full, so on a de-risking switch the post-rebalancing euro share lands at or just
above the regulatory minimum rather than just below it. On the anchor cell's band crossing
— the rebalancing month `t = 84` — the BOM euro share is 50.0427 % against a 50 % target;
taking the charge from the destination instead would put it under, at every crossing, by
`(1 − a)·arb`. `check_euro_share_min()` asserts it.

**The *versement* is not a switch.** New money is allocated directly at the target mix and
bears no arbitrage charge, which is what "allocation of both contributions and existing
balance" means in the one contract publishing its ladder [S1].
`arbitrage_charge_pp(t) = 0` in the anchor cell's first two plan years, months `t = 0` and
`t = 12`, where the *équilibré* grid asks for no euro support at all, even though €3 000
was paid in each — and it is 0 in every month that is not a rebalancing month, on every
cell, because there is no switch in those months at all.

**The minimum binds at the rebalancing date, not continuously — and the monthly grid is
what makes that sentence bite.** Between dates the mix drifts with relative performance,
and there are now **eleven months** of drift rather than an instant: the anchor cell is at
70.0006 % euro after the rebalancing that opens its last plan year, month 132, and falls
monotonically to 69.67 % at the anniversary, month 143. The consequence is a real change to
the check: `check_euro_share_min()` iterates over the **rebalancing months alone**, because
in the other eleven the residual is negative by construction, and a check looping over the
whole frame would fail on every model point while nothing was wrong. Nothing in the model
reads the intra-year share, because re-imposing the target there would invent a rebalancing
frequency the contract does not have — real contracts rebalance quarterly to semi-annually
[S1] [S3] [S7], the finer grid could now express that, and doing it would be an assumption
change rather than a grid change. Measured, quarterly rebalancing costs the anchor cell
0.0142 % of its final balance and €0.46 of extra arbitrage over twelve years.

### The one case the convention cannot cover

The two halves of "charge the source" and "land at or above the minimum" come apart on a
**reverse** switch, and the notes do not say which half wins. Model point 2 arrives
holding 40 % euro against a 20 % minimum nine years out — which is what an incoming
transfer can do — so its first rebalancing sells euro down to the grid, the euro support
is itself the source, and charging the source takes €12.00 out of the very balance the
minimum is measured on. The share lands €9.60 below the line on €19 988, or 0.05 % of the
balance.

This model implements the notes' formula literally, symmetric in the two supports, rather
than quietly charging the UC side in both directions. `check_euro_share_min()` therefore
measures against `euro_share_min_bound(t)` — zero on a de-risking switch and
`−(1 − a)·arb` on a reverse one — so it states the property that is actually true in each
direction and still fails if the charge is taken from the destination on a de-risking
switch. A firm resolving the gap the other way changes one branch of `av_euro_pp_at` and
nothing else.

## The garantie plancher is not a floor at gross premiums

```
g(t) = g⁻(t) + V_net(t) − arb(t) − mgmt_charge_pp(t)
```

Unchanged in form by the monthly grid, and that is the point: its three moving terms are
non-zero in only **two months of the twelve** — the base steps up by `V_net − arb` in the
month that opens a plan year and down by the charge in the anniversary month, and is flat
in between.

*Versements* net of entry loading, less the management charges levied over the plan's
life, less benefits already paid — **[S1]'s drafting**, and [S7] states expressly of its
own guarantee that it is not a floor at gross premiums. [S3] drafts the same guarantee
with euro-fund interest net of charges **added**, which is a different quantity and not
what this model computes; see *The garantie plancher base* in the technical notes, which
is the source of truth for the recursion. It follows that

```
A(t) − g(t) = [A⁻(0) − g⁻(0)] + Σ gross investment return credited to date
```

so the floor bites only where cumulative investment return is negative.
`check_floor_identity()` asserts it in every projected **month**. That check is zero by
construction given the recursion — which is why it is written out. What it catches is the
*wrong* recursion: a base accumulated at gross `V`, a base that forgets the arbitrage
charge, or a base charged something other than what the account was actually charged. Each
breaks the identity in the first month in which it is wrong.

It is also the identity that decides the conversion's one load-bearing timing question.
The management charge is levied **whole in the anniversary month** and is not spread over
the year. Spreading it would leave the account value at the anniversary untouched, because
the monthly factors still compound back — but the base above accumulates a **sum** of
charges rather than a product of factors, and twelve monthly charges do not add to the
annual one: measured, a monthly levy moves `g` at the anniversary by up to €71.95 on the
anchor cell and €531.57 on model point 12. The price of keeping it annual, stated rather
than discovered: a mid-year exit is valued **gross** of the plan year's charge, 0.387 %
above the anniversary value at month 142 on the anchor cell's last plan year.

On the anchor cell the floor never bites: the gap is €22 821.04 at the horizon against an
opening gap of €600.00, so the guarantee sits 32.6 % below the account value throughout.
Model point 10 is the same cell with a €19 000 opening base — a plan whose accumulated
investment return to date is negative — where the floor sets the death benefit for the
first **twenty-six months**, the whole of the first two plan years and the first two months
of the third, and then stops. The crossing is located to the month on the finer grid,
because the base is flat inside a plan year while the account value grows every month; on
the annual grid it could only be reported as "two years".

The cover ceases at the member's **70th birthday** [S1] [S3] and the floor is capped at
€762 245 across contracts [S3]. Model point 9 retires at 70 and crosses it in its final
plan year — the cover is off for the whole of that plan year, because the age steps at the
anniversary and there is no sub-annual age in this product to test a month-exact rule
against **[std]**. The age-70 cliff is not incidental: it is also the age at which a PER death
benefit stops being taxed under CGI art. 990 I and enters the inheritance-duty base **in
its entirety** under art. 757 B [R15] [REG-R41], and from 2026 the age at which
contributions stop being deductible [R20] [R21]. One birthday, three consequences.

The *garantie plancher* charge is folded into the 0.70 % management charge **[std]**;
neither published figure — 0.10 % p.a. on UC balances [S3], 0.12 % inside a 1 % charge
[S1] — is separable in a way that transfers to a composite.

## Settlement: a capital leg, and a rente that usually is not one

In the last projected **month**, `t = proj_len() − 1` — the horizon anniversary — the
survivors settle. The settlement is a contractual event on a contractual date and is not
spread over the final plan year, so every figure in `result_settlement()` is the
annual-step model's to floating point. The capital leg bears **no exit charge** [S1] [S2] [S3] [S7] [S8]. The annuity leg is converted at
`annuity_factor()`, charged the *frais d'arrérages* at 1.50 % **[std]** [S8], and tested
against the commutation threshold.

Two things follow from the 0 % maximum technical rate [R9 A. 142-1](#frlib-per_assurance-r9).

**`a_x` is an undiscounted expected-instalment count**, not a discounted annuity factor.
Nothing in the model discounts it and `rente_gross_pp()` is a plain division; 22.0000
asserts 22 further annual payments to a male aged 64 **[std]**. A 2 % rate would shorten
the factor to about 17.66 and inflate the annuity by roughly a quarter. Note what fixes the
annuity's *frequency*: that table, which counts **annual** instalments — not the projection
grid, which is monthly. Paying quarterly or monthly means replacing `annuity_factor.csv`.

**Commuting at the conversion basis is nearly value-neutral**:

```
commuted = rente_net · a_x = annuity_cap · (1 − c_arr)
```

`check_commutation_identity()` asserts it. Commuting at a *book* value instead
manufactures a gain out of nothing. The mechanism is not marginal — €272 m of 2024
individual-PER benefits at an average €16 200 [R22] — and the €110 threshold is a
**monthly** *quittance* scaled by the months in the payment period [R10 A. 160-2](#frlib-per_assurance-r10), so an
annual frequency tests against €1 320. Testing €110 against an annual instalment would
commute almost nothing.

The anchor cell's annuity is €78.45 a month and duly commutes; the cliff sits at
`annuity_share = 42.06 %`, and model point 6 is the same cell at 50 %, whose €130.75 a
month is paid as a *rente*. That is a live instance of the market pattern: the average PER
annuity in payment is €1 300 a year, about €108 a month, just under the threshold
[R22] [R10].

## What is simplified, and where the rest of it lives

**The rente is cross-referenced, not re-implemented.** Where the annuity is not commuted
this model hands `annuity_conversion` to `Rente_FR_S` and records the amount. The annuity
reserve, the 0.80 % p.a. charge on annuity reserves [S7], reversion, *annuités garanties*
and revaluation through the profit-sharing account are specified in
[`../rente_viagere/technical-notes.md`](../rente_viagere/technical-notes.md). Duplicating
the payout chassis here would give the library two of them to keep in step.

**Staged capital is settled at the horizon** **[std]**. The *capital fractionné* option
[R3 L. 224-5](#frlib-per_assurance-r3) changes *when* the capital leg is paid, not how much: there is no exit
charge, and the technical notes fix the frame at the declared horizon. The model records
the whole capital leg at `t = proj_len() − 1`, publishes the instalment as
`capital_instalment_pp()`, and credits nothing to the unpaid balance. The finer grid does
**not** make the *fractionné* schedule expressible — its instalments fall *after* the
horizon and the frame ends there — so the reason for the simplification is now the frame's
end rather than the grid's coarseness.
Exact on an undiscounted gross-cash-flow basis;
not exact for anything that discounts, and a discounting layer needs the schedule.

**No PPB stock** **[std]**. The euro support is credited at the asset return [S9] and
charged on the post-crediting balance [S3]. The effective euro rate net of charge is
`1.0338 × 0.9930 − 1 = 2.6563 %` — not `3.38 − 0.70 = 2.68 %`, and not the 2.75 % actually
served in 2025, whose extra seven basis points came from a *provision pour participation
aux bénéfices* release [S9]. A PER's PPB release horizon is fifteen years rather than
eight, because the commitments sit in a *comptabilité auxiliaire d'affectation*
[REG-R16] [R8 L. 142-4](#frlib-per_assurance-r8); modelling that stock is a fund-level scenario extension, and four
of the seven sampled contracts have no contractual profit-sharing clause at all
[S4] [S5] [S6] [S7]. The machinery this stands in for is implemented next door in
`Euro_FR_S` and specified in
[`../assurance_vie_euro/technical-notes.md`](../assurance_vie_euro/technical-notes.md) —
the *compte de participation aux résultats*, the PPB dotation-and-release lever and its
vintage clock. Two cautions before lifting it: the release deadline there is eight years
and here it is fifteen, and a PER euro fund is not an assurance vie euro fund. See *The
euro leg is cross-referenced, not re-implemented* in this product's technical notes.

**Tax is outside the projection.** `deduction_elected` is carried on the model point and
enters no recursion. The election is the pivot of the whole exit tax treatment
[R19] [R20] [R21], but it changes what the holder keeps, not what the insurer pays.
`test_the_deduction_election_is_carried_and_inert` projects the anchor cell with the flag
flipped and asserts an identical cash flow table.

Also out of scope, per the notes: partial early release leaving the plan in force
[R5 D. 224-4](#frlib-per_assurance-r5); the 15 % transfer-value reduction on euro-denominated rights
[R5 R. 224-6](#frlib-per_assurance-r5) [S8]; profile and horizon changes during the projection; and the *provision
de diversification* supports [S4] [S6], which are the `eurocroissance` product.

### What the monthly grid changes, and what it does not

The rule the conversion follows is one sentence: **annual assumptions stay annual, annual
contract terms stay on their own month of the plan year, and only the grid underneath them
gets finer.** A monthly grid is not a monthly product. The *versement* and the rebalancing
land whole in the month that opens a plan year, the management charge lands whole in the
month that closes it, and the liquidation lands whole at the horizon; the decrements and
the two credited returns are converted at the constant force, so twelve months compound
back to exactly the published annual figure.

The consequence is worth stating precisely, because it is what makes a monthly run
comparable to the annual-step model it replaced. **Every anniversary state and the whole
settlement reproduce that model to floating point** — worst relative deviation 1.8e-14
across all twelve shipped model points on the two supports, the account value, the death
benefit, the management charge and the *garantie plancher* base, and 1.4e-14 absolute on
the in force. So do the plan-year totals of the credited return and of `premiums`, and
every quantity that is one value per plan year.

**The cash flows do not, and that is the point.** Claims now fall at the end of the month
of exit and are valued on the balance held then, so `claims_death` falls 2.49 %,
`claims_early_release` 1.54 % and `claims_transfer` 0.35 % on the anchor cell; maintenance
expense accrues monthly on a decrementing block, so the aggregate falls 0.61 % while the
per-policy total rises 0.82 % on the monthly-compounded inflation factor; and the split
between the three decrements moves — deaths −1.19 %, releases −0.23 %, transfers +0.98 %
over the first plan year — while their total, and so the in force at every anniversary, is
unchanged. `result_cf_annual()` and `result_state_annual()` exist so the two grids can be
laid side by side.

## Inputs are external files

The five input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `PER_FR_S/` holds nothing but formulas:

```
products/per_assurance/
  model_point_table.csv        <- inputs live here
  allocation_grid.csv
  mort_table.csv
  exit_table.csv
  annuity_factor.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  PER_FR_S/                    <- formulas only
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
| `allocation_grid_file` | `allocation_grid()` | `allocation_grid.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `exit_table_file` | `exit_table()` | `exit_table.csv` |
| `annuity_factor_file` | `annuity_factor_table()` | `annuity_factor.csv` |

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Twelve model points. **Point 1 is the technical notes' worked example** — M 52, horizon 64, `duration_ifo` 2, c1, *équilibré*, €16 600 all in UC against a €16 000 floor base, €3 000 a year, 70/30 exit. Point 2 is a c3 annuity-only cell arriving with a reverse switch; 3, 4 and 5 are the *prudent*, *dynamique* and *offensif* ladders; 6 is the anchor at a 50 % annuity share, above the commutation threshold; 7 and 8 are the two capital forms; 9 crosses the 70th birthday; 10 is the anchor with a floor that bites; 11 is a c2 cell with no floor and no contributions; 12 is a 32-year *prudent* annuity cell | anchor cell **[std]**, technical notes' worked example; €16 600 is the published average accumulation-phase balance [R22] |
| `allocation_grid.csv` | Target `euro_share` and `uc_share` by (`allocation_profile`, `years_to_horizon`), four profiles, `k` = 1 to 45 | the regulatory minimum grid [R6 art. 1](#frlib-per_assurance-r6); band edges **[std]** |
| `mort_table.csv` | Annual mortality by sex and age 18–120, capped at 1 | **[std]** proxy shaped on French population mortality [REG-R24]; **level** anchored so that `mort_be_factor × q(M, 52)` is the notes' 0.00500 placeholder exactly — *not* TH 00-02 / TF 00-02 [REG-R22] [REG-R23] |
| `exit_table.csv` | `early_release_rate` and `transfer_out_rate` by (`compartment`, `duration`), the `duration` key being the plan's **1-based** *ancienneté* year and so read at `plan_year(t)`; 1.60 % / 1.00 % on c1 and c2, reduced release on c3 | **[std]**, split of the 2.62 % aggregate of [R22]; c3 loses the main-residence case [R3 L. 224-4 I 6°](#frlib-per_assurance-r3) |
| `annuity_factor.csv` | Undiscounted conversion factors by sex and age 55–80, anchored at 22.0000 for a male 64 | **[std]** placeholder; TGH05 / TGF05 cited and not shipped [R12] [REG-R21] |

**What is deliberately not in a file.** The charge levels — the entry loading, the two
management charges, the arbitrage rate, the *frais d'arrérages* — are `Projection`
References. The *encadré* requires maxima to be disclosed and caps nothing [REG-R30], and
the sampled range is wide: entry loadings 0 % to 4.80 %, euro management charges 0.50 % to
2.30 % [S1]–[S8]. Every adopted level is a standardization, and putting them where a reader
trips over them is better than filing them in a table that looks like data.

## Sign convention

`liability_cf(t)` is the technical notes' orientation, **outgo-positive**: claims, plus the
capital handed to `Rente_FR_S`, plus expenses, less *versements*. `net_cf(t)` is exactly
its negative, **income-positive**, which is the house sign across the library, so
`result_cf()["net_cf"]` can be summed alongside any other model's without checking which
product it came from. `test_both_signs_of_the_net_flow_are_published` asserts the two are
negatives to 1e-9 and that the outgo columns rebuild `liability_cf`.

A contributing plan is cash-positive in every **plan year** but the settlement one, where
the whole account value leaves at once. On the monthly frame that reads differently: only
the twelve *versement* months are cash-positive, and the eleven ordinary months of each
plan year carry claims and expenses against no income. The plan-year statement is read off
`result_cf_annual()`, which is what that frame is for — years 0–10 positive, year 11 at
−47 395.16.

`annuity_conversion` is an **outgo**, not a memo item: where the annuity is not commuted
the converted capital leaves this projection. It and `commuted_pp` are mutually exclusive
by construction, and only one of them is ever non-zero on a cell.

## Naming

Cells names follow `basiclife.BasicTerm_S` and `savings.CashValue_SE` wherever those
models have an analogue. Six needed care, and the in-force count needed two entries
because the notes and the library index it at opposite ends of the year.

| Notes symbol | Cells | Why it needed care |
|---|---|---|
| `lapse_rate` | **does not exist** | There is no surrender right [R3 L. 224-4](#frlib-per_assurance-r3) [S2] [S3] [S4] [S7]. `early_release_rate` and `transfer_out_rate` are named for the events they are, and `claims_early_release` and `claims_transfer` for the amounts they pay |
| `l⁻(t)` | `pols_if(t)` | The count the year **opens** with, `pols_if(0) = 1`, and the weight on that same `result_cf()` row. This is the library's settled convention, shared with `MYGA_US_S` and `WP_UK_S`: divide a flow by its own row's `pols_if` and you get a per-policy amount for the same period |
| `l(t)` | `pols_if_at(t, "AFT_DECR")` | The count the year **ends** with — the notes' own indexing, and the column their worked-example table prints. It is published as the `pols_if_eoy` column of `result_state()` and it is one period ahead of `pols_if`: `pols_if_at(t, "AFT_DECR") == pols_if(t + 1)`. It carried the bare name `pols_if` in an earlier draft, which put the next period's exposure on every cash flow row — silently, since nothing raised — and the rename is what fixed it. `pols_if_at` also exposes the two intermediate steps, `"BEF_RELEASE"` and `"BEF_TRANSFER"` |
| `m(t)` | `switch_pp(t)` | **Signed**, because the sign decides which support bears the arbitrage charge. Positive on the ordinary de-risking switch; negative where a cell arrives above the grid's minimum |
| `a_x` | `annuity_factor()` | An **undiscounted expected-instalment count**, not a discounted annuity factor [R9 A. 142-1](#frlib-per_assurance-r9). Named for what it is so nothing discounts it twice. It counts **annual** instalments, and it — not the projection step — is what fixes the annuity's frequency |
| `A(t)` | `av_pp(t)` | **Per policy**, and published as a `result_cf()` column beside aggregate flows so that the difference is visible. `av_at(t, timing)` is the in-force weighted quantity, and no cash flow reads it: every claim is already a decrement times a per-policy amount |
| `q(t)`, `w_e(t)`, `w_r(t)` | `mort_rate`, `early_release_rate`, `transfer_out_rate` | The **annual** rates the notes tabulate and the CSVs hold, and they keep the bare names for that reason — the library register forbids the opposite spelling. They are properties of the plan year, constant across its twelve months |
| `q_m`, `w_e,m`, `w_r,m` | `mort_rate_mth`, `early_release_rate_mth`, `transfer_out_rate_mth` | The monthly rates actually applied, `1 − (1 − q)^(1/12)`. The `_mth` suffix marks "derived from an annual rate", not "monthly quantity" — which is why `expenses` and `premiums` carry no suffix |
| `r_eu,m`, `r_uc,m` | `return_euro_mth()`, `return_uc_mth()` | The same constant-force treatment in interest form, `(1 + r)^(1/12) − 1`, so twelve months compound back to the published annual rate exactly |
| (the month) | `duration_mth(t)`, `is_plan_boy(t)`, `is_anniv(t)` | `duration_mth` is `t`, kept so the monthly models in this library share one vocabulary. The two predicates mark the two months of a plan year that carry its annual events, and they are **different months** — the *versement* and the rebalancing at `t % 12 == 0`, the management charge and the liquidation at `t % 12 == 11` |
| (the timings) | `"BEF_REBAL"` / `"BOM"` / `"BEF_CHARGE"` / `"EOM"` | Points inside a **month**. `"BOY"` and `"EOY"` were retired with the annual grid — an `"EOY"` returned for month five of a plan year is a label that lies — and `"BEF_CHARGE"` is new, because crediting and charging no longer happen in the same month |

`claims(t, kind)` takes `"DEATH"`, `"EARLY_RELEASE"`, `"TRANSFER"` and `"MATURITY"`, and
the `result_cf()` columns are named for the `kind` that produces them. There is no
`claims` subtotal column beside them.

## Standardizations used

Everything in this list is **[std]**: the **monthly** projection frequency; the annual
*versement* and rebalancing at the plan-year start and the annual management charge at its
end; the geometric monthly conversion of both credited returns and of all three decrements;
the monthly accrual of maintenance expense and its monthly-compounded inflation; the
decrement and benefit ordering; the glide-path band edges and realising "low risk" wholly as the euro
support; taking the arbitrage charge from the source support and allocating the
*versement* at the target mix; the entry loading of 2.50 %, the euro and UC management
charges of 0.70 %, the arbitrage rate of 0.30 % and the *frais d'arrérages* of 1.50 %; the
UC gross return of 5.00 % and the euro-fund gross asset return of 3.38 %, which has a
source for its 2025 level [S9] but none for carrying it flat over twelve years; the whole
mortality table, its anchored level and the
`mort_be_factor` of 0.85, and the flat 0.00500 placeholder the worked example runs on; the
early-release rate of 1.60 %, the transfer-out rate of 1.00 % and the reduced c3 release
rate; the ordered dependent-decrement convention; folding the *garantie plancher* charge
into the management charge; the annuity factor ladder and its 22.0000 anchor; the annuity
election of 30 % and deterministic commutation whenever the test passes; maintenance
expense of €30 a plan a year inflating at 1.80 %; keeping the *garantie plancher* cessation
on the plan year rather than on the birthday month; settling staged capital at the horizon;
and carrying no PPB stock, no partial early release, no 15 % transfer-value reduction and
no profile or horizon change.

## Tests

`tests/test_per_assurance_fr.py` asserts every row of the notes' worked example to the
cent and `l(t)` to six decimals — on the 0-based **monthly** frame, `t = 0 … 143`, reading
each row at the rebalancing month `12y` and the anniversary month `12y + 11`, with
`result_cf_annual()` summing the 144 rows of `result_cf()` into the notes' twelve and
`result_state_annual()` publishing the notes' own table — the month-by-month table of the
first plan year, the constant-force rate conversions in the only direction that is true
(`1 − (1 − q_m)^12 = q`, never `12·q_m = q`), that the management charge falls in the
anniversary month alone, the settlement table and the commutation
identity, and
then one test per listed modelling pitfall — the glide-path band edge, the *versement*
that is not a switch, the source-charging convention and the reverse-switch bound, the
minimum binding at the rebalancing date, the floor identity and the two cells where the
floor bites and where it ceases, the absence of lapse machinery, the transfer indemnity
window measured from the first *versement*, the three decrements not double-counting, the
undiscounted conversion factor, the monthly commutation threshold and its cliff, the
per-policy against aggregate distinction, and the projection stopping at the horizon with
tax outside it. It asserts the exposure convention separately and over every model point,
because breaking it is silent: `result_cf()` has to open at `pols_if_init()` on row
`t = 0`, each row's `pols_if` has to be the count that row opens with, and the notes'
`l(t)` has to sit one period ahead of it at `pols_if_at(t, "AFT_DECR")`. It also asserts that a compartment-3
cell electing capital raises, that a contradictory `annuity_share` raises, that the glide
path can be swapped without touching a formula, and that the model round-trips.

```bash
python -m pytest lifelib/libraries/frlib/tests/test_per_assurance_fr.py -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #frlib-per_assurance-r10
[R12]: #frlib-per_assurance-r12
[R15]: #frlib-per_assurance-r15
[R19]: #frlib-per_assurance-r19
[R20]: #frlib-per_assurance-r20
[R21]: #frlib-per_assurance-r21
[R22]: #frlib-per_assurance-r22
[R3]: #frlib-per_assurance-r3
[R7]: #frlib-per_assurance-r7
[REG-R16]: #frlib-reg-r16
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R30]: #frlib-reg-r30
[REG-R41]: #frlib-reg-r41
[std]: #frlib-std
<!-- END generated citation links -->
