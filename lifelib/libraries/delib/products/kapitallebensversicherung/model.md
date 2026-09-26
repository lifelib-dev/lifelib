# Implementation Notes

**Status:** Draft, 2026-08-29. Built from
[`products/kapitallebensversicherung/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the surplus declared as a percentage of the
> *Deckungskapital*, in four carrier wordings that agree on the base and differ on the
> timing and the waiting period [S7] [S18] [S9] [S3], booked into the *Deckungskapital* at
> the *Bilanztermin* [S9], the declared level being revisable annually and capable of being
> zero [S1] [S9]; the *Rückkaufswert* as the *Deckungskapital* on the *Rechnungsgrundlagen
> der Prämienkalkulation* struck at the end of the current *Versicherungsperiode* and
> floored by the five-year spreading [R2], restated verbatim in the model wording [S1] and
> in three carrier wordings [S7] [S18] [S3]; the *Stornoabzug* as *vereinbart*, *beziffert*
> and *angemessen* [R2] [R22], quantified on three different bases by three carriers
> [S3] [S9] [S18] [R30]; the § 165 VVG *Mindestversicherungsleistung* test and the paid-up
> sum bought with the § 169 value [R3] [S1] [S7]; the § 161 VVG substitution of the
> *Rückkaufswert* for the sum insured on a suicide inside three years [R4] [S1]; the ending
> of the contract, and so of the premium, with the death payment [S7]; and both DeckRV
> cohort ceilings, each fixed at conclusion for the whole term [R7] [REG-R15] [REG-R16].
> **Every behavioural and experience assumption is a [std] standardization.** No German
> insurer publishes a mortality basis, an expense loading, a commission scale, a
> terminal-bonus rate or a lapse rate for this product — the six carrier documents read for
> this library contain none of them [S3] [S4] [S5] [S7] [S9] [S18] [S11] [S12] [S13] — and
> the DAV tables — **DAV 2008 T** here — are the property of the Deutsche
> Aktuarvereinigung, are not public and are cited by name rather than redistributed [R14]
> [REG-R47] [REG-R48]. delib was drafted with HTTP egress blocked and nothing
> retrieved; the citations have since been re-verified, and forty-five of the forty-seven
> entries in `sources.md` now record a document that was opened and read. **That verifies
> the mechanics cited above and none of the levels below**, which no retrieved document
> supplies. Replace the decrement, surplus and expense tables with company data before
> using any number here.

## Run it

```bash
python products/kapitallebensversicherung/run.py
python products/kapitallebensversicherung/run.py 8      # the Bonussystem variant
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/kapitallebensversicherung/KLV_DE_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by the policy **month** `t` with one column per
cash flow line; `result_cf_annual()` sums it into policy years, which is the view the technical
notes' worked example is stated on; and `result_surplus()` is the **annual** state behind both —
the reserve, the declared rate, the surplus base and credit, the *Überschussguthaben*, the accrued
terminal share and the *Rückkaufswert* at each anniversary. The frames are separate on purpose: a
cash flow statement whose columns do not all sum to its bottom line is one a reader has to know
which columns to skip, and a state table that moves once a year should not be printed twelve times
over.

The model and both its Spaces carry docstrings — `model.doc` describes the product and the
projection basis, `model.Projection.doc` holds the full mapping between the technical notes'
symbols and the cells names, and `model.Data.doc` says what each input file is and, for the
mortality table, what it is *not*.

## Two clocks: a monthly frame over an annual product

`t` is the **policy month index, 0-based and counted from issue**, and
`proj_len() = 12 × policy_term` is the frame's **exclusive** end. The frame is
`t = t_start() … proj_len() - 1`, contiguous, with `t_start() = 12 × duration_init()` —
`duration_init` being an elapsed count of policy **years**, so the conversion is a multiplication.
The anchor cell publishes **300 rows, `t` = 0 to 299**, and the in-force point 10
(`duration_init` = 14) **192 rows, `t` = 168 to 359**. There is no `t = proj_len()` row;
`pols_if(proj_len())` is defined for the closure identities and weights no cash flow.

**Almost nothing on this product is monthly, and the argument of a cells says so.** Cells that
state an **annual account** take a 0-based policy year `k` — the whole pricing block, all three
reserves, the § 169 value, the paid-up purchase, every part of the *Überschussbeteiligung*, the
*Stornoabzug* band and the expense inflation. Cells that state a **month** take `t` — the in
force, the claims, the premium instalments and every `result_cf()` column. `duration(t) = t // 12`
is the bridge, `age(t) = age_y(duration(t))` steps on the anniversary,
`policy_year(t) = duration(t) + 1` is the contractual 1-based label, and
`is_anniv(t) = (t % 12 == 11)` marks the month the annual machinery acts in.

The decrement rates take `t` and return the **year's annual** rate — the vectors the notes tabulate
— while `mort_rate_mth(t)` and `lapse_rate_mth(t)` are what the recursion applies, each
`1 - (1 - r)^(1/12)`, so twelve of each compound back to the year's rate. That is what leaves the
whole annual layer **bit-identical** to the annual-step model this replaced: `pols_if` at every
anniversary is unchanged, and with it every reserve, every declared credit and every ledger
balance. `result_surplus()` is row for row the table it always was.

**What a mid-year exit is paid.** A claim in a non-anniversary month is paid the balances standing
at the **last** anniversary — `av_sur_close_pp`, `bonus_si_close_pp`, `term_bonus_close_pp` and
`res_guar_close_pp` — because the *Überschussdeklaration* has not happened yet. On a *gezillmert*
contract that makes the guaranteed leg of a surrender exactly **zero through the whole first policy
year**, which is the consumer fact this product is best known for and one the annual grid could not
express: it had to pay a month-0 surrender the value the coming anniversary would close at.

**What that meant for the input files.** No CSV value changed, in this conversion or in the earlier
move to a 0-based frame. Every time-like key column keeps its own scale:

| File | Column | Decision | Why |
|---|---|---|---|
| `lapse_table.csv` | `policy_year` (1–40) | **unchanged**; read as `policy_year(t) = duration(t) + 1` | A contractual, 1-based policy-year label, not the frame's `t`. The 6,0 % spike belongs to *policy year* 12, which the model reads across months 132 to 143 |
| `surplus_rate_table.csv` | `policy_year` (1–40 per scenario) | **unchanged**; read as `k + 1` | The same label, on the same scale, for `decl_rate`, `term_rate` and `ans_rate`, all of which are annual |
| `model_point_table.csv` | `duration_init` | **unchanged** | An **elapsed count** of completed policy **years**; it *is* `k_start()`, and `t_start()` is twelve times it |
| `model_point_table.csv` | `bfz_year` | **unchanged**, still the 1-based policy year | 0 means "never" and has to stay free. The model maps it instead: the election falls at the end of the 0-based policy year `bfz_year - 1` — month `12(bfz_year - 1) + 11` — and `is_paid_up(k)` is `k >= bfz_year()` |
| `model_point_table.csv` | `issue_year` | **unchanged** | A calendar year and a cohort key, not a point on the frame |
| `deckrv_table.csv` | `issue_year` | **unchanged** | The same cohort key |
| `mort_table.csv` | `age` | **unchanged** | An attained age, reached through `age(t)`, and its rates stay **annual** |

`cost_table.csv` and `freq_loading_table.csv` carry no time-like column at all — but
`freq_loading_table.csv`'s `instalments` column, which the annual grid could not use for anything,
now sets the premium collection cycle.

## The declared rate is a total, not an add-on — the German delta

This is the one thing about the product a reader arriving from a US or UK participating
model will get wrong, and it is a subtraction rather than an addition. The *laufende
Verzinsung* **is** the *Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung*
[REG-R53], so on the anchor cell a declared 2,70 % — Allianz's 2025 rate for its combined
classic life-and-annuity book, as reported by the trade press [R26] — against a 1,00 %
guarantee [R7] [R15] is a **1,70 pp** credit and never 2,70 pp on top of 1,00 pp:

```
zins_ueberschuss_rate(k) = max(0, decl_rate(k) - rechnungszins())
```

The interest-surplus rate is **derived and never an input**, and both halves of that line
are load-bearing. The outer `max` is what keeps the `nil` scenario honest: the declared
rate is then below the guarantee, which the reserve roll-forward still meets in full, so
the surplus is zero rather than negative. Model point 14 runs that path.

The base it multiplies is the ***Deckungskapital*** — "in Prozent des maßgeblichen
Deckungskapitals" [S7], the reserve "um ein Jahr mit dem Rechnungszins abgezinst" [S18] —
`surplus_base_pp(k) = max(res_pp_at(k, "AFT_INT"), 0)` — the **closing** guaranteed
reserve of the year, not the sum insured and not the premium. The inner `max` guards the
other end: a *gezillmerte Deckungskapital* is negative at issue, and a positive rate on a
negative base credits a negative surplus. **On the shipped 25 ‰ basis that guard is
inert**, because the base is the closing reserve and it is already +570,75 € in the first
policy year (`k` = 0) against an opening −1 252,53 €; it is not inert at the pre-2015 40 ‰
ceiling [R7] [REG-R16], where that closing reserve is −190,22 € and the credit is nil. The test
suite exercises both, the second on a 2014-cohort copy of the anchor cell rather than by
asserting a behaviour the base run does not show.

## Three reserves, and the one the customer gets

The product has three constructions and needs all three. They are the **premium-paying**
constructions throughout, computed on the full `sum_assured` over the whole remaining
term; only `res_pp` switches to the paid-up basis.

All four take the **policy year `k`**, not the month: the *Deckungskapital* of this tariff is
defined at anniversaries and the monthly frame does not interpolate it.

| Cells | What it is | On the anchor cell at `k` = 0 |
|---|---|---|
| `res_net_pp(k)` | The net prospective reserve, no acquisition cost at all | 0,00 € — the equivalence principle stated as a reserve |
| `res_zill_pp(k)` | The *gezillmerte Deckungskapital* the insurer holds | **−1 252,53 €**, exactly `-alpha_cost()` |
| `res_min_pp(k)` | The § 169 Abs. 3 VVG floor: the same net reserve with the acquisition cost spread **evenly over the first five contract years** [R2] | −1 252,53 €, equal at duration 0 |
| `res_guar_pp(k)` | `max(res_zill_pp(k+1), res_min_pp(k+1), 0)` — the § 169 value at the **end** of year `k` | 776,70 €, the floor already binding |

`res_guar_pp` reads the reserves at `k + 1` because § 169 Abs. 3 strikes the value *zum
Schluss der laufenden Versicherungsperiode* and not at the cancellation date [R2], and it
takes the maximum because the *Mindestrückkaufswert* is a floor on the **value**. On a
long *gezillmert* contract the floor **normally binds**: `ann_due_prem_fut(k) /
ann_due_prem_1st()` falls roughly linearly over `m` years while `max(0, 1 − k/5)` reaches
zero after five, so the two coincide only at durations 0 and `m`. `res_guar_pp(11)` — the
value struck at the end of the twelfth policy year, so the reserves read at `k` = 12 — is the
floor's 22 413,46 € against a Zillmer reserve of 21 722,40 €: 691,06 € the customer would lose to
a model that published the Zillmer reserve alone as the surrender value.

Model point 13 (`zillmer_on = 0`) makes all three coincide at every duration and the floor
slack, which is the invariance test; model point 2 (`prem_term = 1`) reverses the ordering
from the first anniversary, a single premium leaving almost nothing to amortise. Both are
the right answer rather than degenerate cases. Note that the acquisition cost is charged
in the **premium** either way: `zillmer_on` enters `alpha_cost`, a *reserving* quantity,
and not the pricing equation. `zillmer_on = 0` is a **[std]** switch, not an observed
market option: § 4 DeckRV sets a ceiling rather than a mandate [R7], and every carrier
wording read here applies the *Verrechnungsverfahren* [S7] [S9] [S18].

## Beitragsfreistellung is not a lapse, and it can fail

§ 165 VVG converts the contract to a reduced *beitragsfreie Versicherungssumme* bought
with the § 169 value, `bfz_si_pp() = res_guar_pp(e) / pu_single_prem(e + 1)` with
`e = bfz_year() - 1` [R3]. `bfz_year` is the **contractual, 1-based** policy year at whose end
the election falls — the column keeps that scale because 0 has to stay free to mean "never" —
so the election year is period `e` and the contract is paid-up from period `bfz_year` onwards. The policy **stays in `pols_if`** — only a *Kündigung* removes it — with that
reduced sum in place of `sum_assured()`, no further premium and a reserve
`bfz_si_pp() * pu_single_prem(k)`. On model point 11 the election at the end of policy year 10
(`k` = 9, so the last premium month is `t` = 119) leaves `pols_if` bit-identical to the anchor's
while the paid-up sum falls to 21 403,08 € and the maturity benefit from 65 227,99 € to
31 621,11 €.

**Unless the resulting sum falls below the agreed *Mindestversicherungsleistung*.** Then
the statute obliges the insurer to pay the § 169 value instead and the election **becomes
a surrender** [R3]: `lapse_rate` returns 1.0 in that year, the whole cohort leaves as
`claims(t, "LAPSE")` and every later row is zero. Model point 12 takes that branch — a
897,49 € paid-up sum against `bfz_min_si` = 2 500 € **[std]** — and terminates at the end of
policy year 3, month `t` = 35.

That year is the one place a rate of 1.0 must **not** be spread over twelve months.
`lapse_rate_mth` is `1 - (1 - lapse_rate(t))^(1/12)` everywhere except here, where twelve-th
rooting a certainty would empty the cohort in the year's *first* month and pay the *Kündigung*
eleven months early; `bfz_fails()` detects the branch and `lapse_rate_mth` places the whole
decrement in the anniversary month instead. The election is a dated contractual act, not an
experience rate.

Because the § 169 floor generally exceeds the Zillmer reserve, the paid-up sum bought is
worth more than the Zillmer reserve released. `bfz_uplift_pp` is that difference,
discounted to the start of the election year, and it enters `res_pp_at` so
`check_res_roll_fwd()` **still closes in the election year** rather than being switched
off there — and what it then asserts is a real identity: that the paid-up purchase was
made at exactly the § 169 value.

## What a surrender pays, and what § 161 substitutes

```
surr_value_pp(t) = res_guar_close_pp(t) * (1 - storno_rate(duration(t)))
                   + av_sur_close_pp(t)
                   + term_surr_share * term_bonus_close_pp(t)
```

The three `*_close_pp` cells are the bridge between the monthly frame and the annual ledger: each
returns the balance standing at the **last anniversary passed**, stepping up in the month
`is_anniv(t)` is true. A surrender in March is paid the December figures, because the
*Überschussdeklaration* that would move them has not happened.

The ***Stornoabzug* bites on the guaranteed value alone**: two of the three published
deductions are struck on the *Deckungskapital* or on the gap between the sum insured and it
[S3] [S18] [R30], and none of the three reaches the accumulated *Überschussguthaben*, which
§ 169 Abs. 7 VVG in any case makes payable in addition to the § 169 Abs. 3 to 6 amount
[R2]. So the *Überschussguthaben* passes through undeducted. `term_surr_share = 0` in the base run — the
accrued *Schlussüberschussanteil* is paid at the *Ablauf* and on death and **not** on
surrender, the choice that does not invent an entitlement the sources do not describe; the
parameter is exposed rather than hard-coded because it is what would move surrender values
most.

The same amount is what a suicide inside three years is paid. § 161 VVG makes the insurer
*leistungsfrei* **and** obliges it to pay the *Rückkaufswert* including *Überschussanteile*
under § 169 [R4], so the German rule is a benefit **substitution** and not a forfeiture —
materially unlike art. L. 132-7 of the French code, where the cover is of no effect in the
first year and there is no surrender value to fall back on. `benefit_death_pp(t)` is
`0.98 * benefit_full_pp(t) + 0.02 * surr_value_pp(t)` for `duration(t) < 3` — policy years 1 to
3, which are the months `t` = 0 to 35 — and `benefit_full_pp(t)`
thereafter, on `suicide_share = 0.02` **[std]**. The three-year window is a term of the
contract and so ends on the third anniversary, not at a month the monthly grid happens to
make convenient; what the monthly grid adds is that a death inside it is now paid the
*Rückkaufswert* of the anniversary it follows, which through the whole first policy year is
**nil** on the guaranteed leg. Paying **nil** on the excluded share would
be the error; setting the share to zero is a defensible variant.

Unlike a *Risikolebensversicherung*, a lapse here is a real and often large outflow —
9 112,99 € over the anchor projection against 33 365,26 € of premium — and in the final
policy year the difference between a surrender and a maturity decides a payment rather than
only a label. That total is 992,00 € below the annual-step model's, and the gap is the whole
point of the conversion: a surrender in a non-anniversary month is now paid the value
standing at the anniversary behind it rather than the one ahead of it.

## The three Überschussverwendung systems

One `surplus_credit_pp(k)` and three destinations, exactly one live per model point. All three
ledgers are **annual**, and all three take `k`:

| `surplus_use` | Ledger | Maturity benefit | Death benefit at `t` = 59 |
|---|---|---:|---:|
| `ansammlung` (point 1) | `av_sur_pp(k+1) = av_sur_pp(k) (1 + a(k)) + C(k)` | **65 227,99 €** | 50 460,89 € |
| `bonus` (point 8) | `bonus_si_pp(k+1) = bonus_si_pp(k) + C(k) / pu_single_prem(k+1)` | 63 562,77 € | **50 532,10 €** |
| `beitragsverrechnung` (point 9) | `prem_offset_pp(k) = min(prem_charged_pp(k), C(k−1))` | 52 428,98 € | 50 085,64 € |

`t` = 59 is the twelfth month of the fifth policy year, and the column is quoted there because
that is where the monthly model reproduces the annual one exactly. Through months 48 to 58 the
same three benefits are 50 286,07 €, 50 334,46 € and 50 053,54 € — the year's declaration has not
been made, so `av_sur_close_pp` and `bonus_si_close_pp` still stand at the previous anniversary.
The step is a **plateau and a jump**, once a year, which is what a once-a-year declaration is.

That is exactly the asymmetry the sources record — "compared with the *Bonussystem*, the
*verzinsliche Ansammlung* leads to a higher payment at maturity, while the *Bonussystem*
produces higher death benefits" [R28] — and it is arithmetic rather than coincidence: the
*Ansammlung* compounds at `ans_rate` = 2,70 % while bonus sum insured accumulates at
`rechnungszins` = 1,00 %, but the bonus is **paid-up insurance** whose whole face amount
falls due at once on death. A model that set the two rates equal would lose the
distinction, correctly. *Beitragsverrechnung* moves the surplus out of the benefit stream
entirely: premiums collected fall by 5 349,15 €.

Under *Beitragsverrechnung* the **renewal commission is charged on the tariff instalment
`prem_charged_inst_pp(t)`, not on the collected `prem_inst_pp(t)`**: the intermediary is paid on the tariff premium, the surplus offset
being a discretionary policyholder rebate the insurer may withdraw without invoking § 163
VVG at all [REG-R27].

## Two mortality bases over one sex-specific table

Three quantities, deliberately not two indexings of one:

- **`mort_rate_at_age(x)`** is the first-order **tariff** rate: it prices and it reserves,
  and it is a fixed unisex blend, `½ q₁(M, x) + ½ q₁(F, x)` **[std]**, because German new
  business has been unisex since 21 December 2012 [REG-R34]. Points 1 and 7 differ only in
  `sex` and price identically at 2 004,0420 €; pricing off the policy's own row moved that
  premium by 9,15 € when the model was first written that way.
- **`mort_rate_base(t)`** is the policy's own sex-specific table row, and
  **`mort_rate(t) = mort_rate_base(t) × mort_be_factor`** with `mort_be_factor = 0.75`
  **[std]** is the best estimate that **projects**. The 33 % wedge is the
  *Sicherheitszuschlag*, whose systematic release **is** the *Risikoüberschuss* [REG-R47] —
  which this model does not compute, and which a model that reserved on the best estimate
  would have thrown away. `res_pp` is invariant to `mort_be_factor`; `pols_death` moves
  with it.
- **`rating_factor`** is a third thing again: the *Risikozuschlag* [R5]. It multiplies the
  first-order rate in the **death leg of the pricing and the prospective reserve only** —
  never the survivorship, never the benefit, never a best-estimate rate. On model point 14
  it raises the *Bruttobeitrag* from 2 530,90 € to 2 611,45 € and leaves `mort_rate` and
  the death benefit untouched.

The table itself is a **[std]** Makeham-form proxy anchored at
`mort_rate_1st(M, 37) = 0.001200` exactly, and **one table serves both legs**. The
direction of prudence forks — a death benefit wants mortality assumed higher than
expected, a survival benefit lower [REG-R47] [REG-R48] — so no single first-order table is
prudent for both. German practice resolves that in the tariff rather than in the table and
the model follows, with the compromise named rather than papered over.

## The Ratenzahlungszuschlag applies to an unechte Zahlweise only

`prem_freq_load()` is the table value where `unterjaehrig_form` is `unecht` — 1,000 annual,
1,020 half-yearly, 1,030 quarterly, 1,050 monthly **[std]** — and **exactly 1,000 where it
is `echt`**, because a genuine sub-annual *Versicherungsperiode* is not an instalment of an
annual one and carries no loading [R28]. Model points 4 and 5 are the same monthly contract
under the two readings and differ by 1 642,40 € of projected premium.

**The other half of the *Zahlweise* is now real.** `instalments()` no longer merely justifies a
loading it does not otherwise touch: `prem_cycle() = 12 // instalments()` is the collection
period in months, `prem_due(t)` is true when `duration_mth(t) % prem_cycle() == 0`, and
`prem_inst_pp(t) = prem_paid_pp(duration(t)) / instalments()` where one falls due is a single
instalment rather than a year's premium — formed from the annual amount so the
*Beitragsverrechnung* offset is spread over the year exactly as the charge is. An annual payer is charged in month 0 of each policy year and nothing in
the other eleven; a monthly payer is charged every month; a quarterly payer in months 0, 3, 6
and 9. The cohort that has already died or surrendered mid-year pays nothing further, which is
why the point 4 / point 5 gap moved from 1 668,26 € to 1 642,40 € — an annual grid had to
collect the whole year's premium from a cohort measured at the year's start.

## Inputs are external files

The seven input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `KLV_DE_S/` holds nothing but formulas:

```
products/kapitallebensversicherung/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  lapse_table.csv
  surplus_rate_table.csv
  cost_table.csv
  freq_loading_table.csv
  deckrv_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  KLV_DE_S/                    <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its input file beside the model
and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/` directory
and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for every
policy. They live instead in an unparameterized **`Data`** Space, which `Projection`
references as `data` — so each file is read once per model no matter how many policies are
projected. `test_model_conventions_de.py` counts the reads against the set registered in
`de_registry.INPUT_FILES`. `Data.input_dir()` resolves the location from
`_model.path.parent` when the model is read, so it works wherever the repository is checked
out.

**The trade-off:** the model is not portable on its own. Copy `KLV_DE_S/` without the CSVs
and it will read fine, then fail on first evaluation. What you gain is that a diff of the
model shows logic changes only, and an input can be swapped in place with no formula change.

| Reference | Cells | File | Contents and provenance |
|---|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` | Fourteen configurations. **Point 1 is the worked-example anchor** (M 37, term 25, 50 000 €, ratio 1,00, annual, 1,00 %, zillmered, `ansammlung`, `base`). The **only file without a `provenance` column**: a model point is a configuration, not an assumption |
| `mort_table_file` | `mort_table()` | `mort_table.csv` | First-order death rates by sex and age 0–120. **[std]** Makeham proxy `0.00022 + B·1.10^x` for males and a three-year setback for females, `B` fixed by the anchor `mort_rate_1st(M, 37) = 0.001200`. Stands in for **DAV 2008 T**, which is cited and never shipped [R14] |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` | Two different things by policy year: `lapse_rate`, the surrender **decrement**, and `storno_rate`, the **deduction**. Both **[std]** — the only German data are market aggregates that count conversions to *beitragsfrei* alongside surrenders [R20] |
| `surplus_rate_file` | `surplus_rate_table()` | `surplus_rate_table.csv` | `decl_rate`, `term_rate`, `ans_rate` by scenario and policy year; `base`, `low`, `nil`. The 2,70 % declared rate is [S11]; held level, and the other two paths, **[std]** |
| `cost_file` | `cost_table()` | `cost_table.csv` | The first-order tariff loadings and the second-order expense basis **on the same row**, because the difference between them *is* the *Kostenüberschuss*. Ceilings cited [R7] [REG-R16] [R29]; every level **[std]** |
| `freq_loading_file` | `freq_loading_table()` | `freq_loading_table.csv` | `instalments` and the *Ratenzahlungszuschlag* by frequency. The 2 / 3 / 5 % market convention [R28]; the single values **[std]** |
| `deckrv_file` | `deckrv_table()` | `deckrv_table.csv` | Both DeckRV ceilings by `issue_year` — § 2's *Höchstrechnungszins* and § 4's *Höchstzillmersatz* — because both are **cohort facts** that travel with the contract [REG-R14] [REG-R15] [REG-R16] |

Every file but the model point table carries a per-row `provenance` column, which is this
library's second ruling and is machine-checked.

## The identities the model publishes

Nine `check_*()` cells, each taking no argument and returning a `bool` over the whole frame,
each carrying a per-period residual beside it. **The residual's argument follows its cells'
clock:** the six monthly identities carry `check_*_resid(t)` over policy months, and the three
that state an annual account — `check_res_roll_fwd_resid(k)`, `check_surplus_roll_fwd_resid(k)`
and `check_surr_floor_resid(k)` — carry a residual per policy **year**. A Fackler recursion has
nothing to say about a policy month on a tariff whose *Deckungskapital* is only defined at
anniversaries, and inventing a monthly residual for it would have invented a monthly reserve.

**`check_net_cf()` — this library's first ruling — is
`net_cf == premiums − claims_death − claims_maturity − claims_lapse − expenses −
commissions`, rebuilt from `result_cf()`'s own published columns.**

The other eight: `check_pols_roll_fwd()`, the in-force recursion and the final year's
maturity count; `check_decrement_closure()`, deaths plus surrenders plus maturities summing
to `pols_if_init()` by direct summation over the exit cells; `check_res_roll_fwd()`, the
Fackler recursion `(V + P^Z + uplift)(1 + i₁) = f q₁ SD + (1 − q₁) V(k+1)` computed
retrospectively on the left and prospectively on the right — the strongest single check in
the model, since it holds only if the premium, the first-order mortality, the
*Rechnungszins* and the prospective formula are mutually consistent;
`check_surplus_roll_fwd()`, whichever of the three surplus ledgers is live;
`check_surr_floor()`, § 169 Abs. 3; `check_equivalence()`, the first-order pricing
equivalence; and `check_rechnungszins_cap()` and `check_zillmer_cap()`, the two DeckRV
cohort ceilings. The last two are **parameter invariants** rather than roll-forward
identities, and they live in the model rather than in a build script because a German model
point's cohort *is* an assumption: a 4,00 % guarantee on a 2026 issue year is not a stress,
it is a data error.

`check_zillmer_cap()` and `check_surr_floor()` are separate on purpose. § 4 DeckRV caps
**how much** may be zillmered — a cap on the *charge* — while § 169 Abs. 3 VVG fixes **how**
the acquisition cost is spread for the surrender floor — a floor on the *value* [R2] [R7]
[REG-R16] [REG-R28]. One search summary in the corpus conflates them; delib does not.

## Modules that are off in the base run

Three constructions are implemented and switched off, so the base run reproduces the worked
example while the machinery stays visible and testable.

| Module | Switch | Off value | What it does |
|---|---|---|---|
| Premium-shock lapse | `beta_shock` | `0.0` | `1 + β·max(0, prem_paid_pp(k)/prem_paid_pp(k−1) − 1 − 0.05)`. Inert on a level *Bruttobeitrag*, but live under *Beitragsverrechnung*, where a fall in the declared rate raises the *Zahlbeitrag* |
| Rate-gap lapse | `lapse_gap_a` | `0.0` | `a·max(0, ref_rate − decl_rate(k) − 0.005)` on `ref_rate = 0.03`, keyed on the gap between the declared rate and what is available elsewhere |
| *Beteiligung an den Bewertungsreserven* | `bwr_rate` | `0.0` | Adds `bwr_rate × res_guar_pp(n − 1)` to the maturity benefit. § 153 Abs. 3 VVG allocates half the reserves determined on termination [R1], but § 139 VAG permits participation only to the extent they exceed the *Sicherungsbedarf* [R8], and that need has routinely exhausted them |

All three enter through **annual** quantities, and both lapse modules move `lapse_rate`, the
year's rate, rather than `lapse_rate_mth` — a shock to a decrement is a statement about the year
and the geometric split then carries it into the months on its own.

`term_surr_share = 0` is a fourth switch of the same kind: the accrued
*Schlussüberschussanteil* is not paid on surrender in the base run, and raising it is what
a user who reads a carrier's wording differently would do first. **No German calibration of
any of these numbers exists in the corpus**, which is why all four ship off.

Also not implemented, and stated rather than left to be discovered: no premium-default path
(§§ 37 and 38 VVG were never researched, gap 20), no *Widerruf* decrement (§ 152 VVG,
likewise), no dynamic *Beitragsfreistellung* take-up — the election is a deterministic model
point column because the corpus gives **no take-up rate at all** [R3] [R20] — no management
action on the declared rate, and no *Zusatzversicherung*, *Kapitalwahlrecht* or *Dynamik*.

## Sign convention

`net_cf` is **income positive** — *Beiträge* in, claims, expenses and commission out —
which is the notes' own orientation and the library-wide sign. `liability_cf` publishes the
same stream outgo-positive, `liability_cf(t) = −net_cf(t)` exactly, and both are columns of
`result_cf()` so the identity is verifiable in the frame rather than only in prose. A
Solvency II best estimate is `Σ v(t) × liability_cf(t)` over the relevant risk-free term
structure, plus a risk margin [REG-R1] [REG-R2] [REG-R6]; nothing in this library discounts.

`expenses` **excludes** commission, which is the deliberate difference from the frlib
chassis, where the commission sits *inside* the expense column and is published beside it.
Here `commissions` is a separate line, so the six flow columns of `result_cf()` sum to
`net_cf` with no double count. Whichever convention a model takes, taking both at once is
the error, and `check_net_cf()` is what makes the choice checkable.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE` wherever those
models have an analogue: `pols_*` for policy counts, plural nouns for cash flows, `*_rate`
for rates, `*_pp` for per-policy amounts, `claims(t, kind)` with an uppercase `kind` string,
and `*_at(t, timing)` — or `*_at(k, timing)` on the annual ledgers — for the within-period
reads. The technical notes use compact actuarial
symbols; the full mapping lives in the `Projection` Space docstring. Six cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `q₁(x)`, `q(t)` | `mort_rate_at_age` / `mort_rate_base` / `mort_rate` | Three quantities: the unisex **tariff** rate that prices and reserves, the policy's own sex-specific table row, and the best estimate that projects. `mort_rate_table` and `mort_ae_factor` are both retired names |
| `V(t)` | `res_pp` / `res_net_pp` / `res_zill_pp` / `res_min_pp` / `res_guar_pp` | One symbol, five amounts. `res_pp` is what the contract holds; the middle three are constructions; `res_guar_pp` is the § 169 value at the **end** of the year |
| `B`, `P^n`, `P^Z` | `prem_gross_pp` / `prem_net_level_pp` / `prem_zill_pp` | The *Bruttobeitrag* and two **pricing quantities that never become cash flows**. `premium_net_pp` is a retired name; `prem_net_level_pp` is the one that won |
| (charged / paid) | `prem_charged_pp(k)` / `prem_paid_pp(k)` | The **year's** *Zahlbeitrag* before and after the *Beitragsverrechnung* offset, with `prem_charged_inst_pp(t)` and `prem_inst_pp(t)` the instalments the *Zahlweise* makes due. The renewal commission reads the charged instalment |
| `U(t)` | `av_sur_pp`, `av_sur_pp_at`, `av_sur`, `av_sur_at` | The **surplus** half of the house account-value pair, on the *Überschussguthaben* — which receives surplus and **never premium**, so `prem_to_av_pp` has no counterpart here and is not published. Library-wide `av_pp` is the *principal* balance (`RV_DE_S`'s and `Basis_DE_S`'s *Deckungskapital*, `FRV_DE_S`'s *Fondsguthaben*) and `av_sur_pp` the *verzinsliche Ansammlung* beside it, which is `RV_DE_S`'s spelling on the one model carrying both; this product's principal balance is a **reserve**, `res_pp`, so there is no `av_pp` here. `withdrawals` is likewise absent: no located wording gives a classic endowment a partial-withdrawal right |
| `w(t)`, `σ(t)` | `lapse_rate` / `storno_rate` | A decrement and a deduction, in one CSV and easy to confuse. `lapse_rate(t)` returns the **annual** rate of the policy year `t` falls in, per the library convention, and `lapse_rate_mth(t)` is what the recursion applies; `storno_rate(k)` is a band read by policy **year** and never twelfth-rooted — a deduction is a percentage, not a decrement |

**The sister models that share this chassis.** `KLV_DE_S` is the *Überschussbeteiligung*
chassis the rest of delib's savings side reuses: `RV_DE_S` (*klassische Rentenversicherung*)
is the same machinery with an annuity rather than a lump sum at the *Ablauf*, `Basis_DE_S`
and `Riester_DE_S` add a tax wrapper and a state *Zulage* to it, and `Index_DE_S` spends the
declared surplus on an index participation instead of accumulating it. `FRV_DE_S` does
**not** share it: a unit-linked *Rückkaufswert* is a *Zeitwert* of fund units and not a
*Deckungskapital* [R2]. Across libraries the nearest relatives are lifelib's
`annuallife/TradLife_A`, whose external-input layout this model copies, and frlib's
`Euro_FR_S`, whose *participation aux bénéfices* is the same idea under a different statute
— with the difference that a French *fonds euros* credits a rate to an account balance while
a German endowment credits it to a **reserve**.

## Standardizations used

Everything in this table is **[std]**. The rule the library enforces is that every
quantitative parameter is either source-tagged or marked here.

| Standardization | Value | Rationale |
|---|---|---|
| Mortality proxy and its anchor | `0.00022 + B·1.10^x`, `mort_rate_1st(M, 37) = 0.001200` | DAV 2008 T is not public and is not redistributed [R14]. The anchor is what makes the worked example reproduce, and is the one number a replacement must preserve |
| Unisex blend `unisex_share` | 0.5 | New business is unisex [REG-R34]; **no insurer publishes the portfolio mix behind its own tariff** |
| `mort_be_factor` | 0.75 | A 33 % first-order safety loading. The *Sicherheitszuschlag* level is not established for any German carrier |
| Age basis | Age last birthday at issue, stepping at the anniversary | **No located German endowment wording states one** |
| `alpha_rate` | 25 ‰ of the *Beitragssumme* | The § 4 DeckRV **ceiling** is cited [R7] [REG-R16]; sitting at it is the choice, no carrier's actual acquisition cost being public (gap 7) |
| `beta_rate`, `gamma_rate` | 3,0 % of premium; 1,5 ‰ of `sum_assured` p.a. | The *form* of the premium loading is established [R28]; the *form* of the sum-insured loading is **not** (gap 17). Neither level is |
| Expense basis | 300 € acquisition; 45 € maintenance at 1,8 % p.a.; 120 € per claim | **No carrier charge level is established** (gap 7). The one product-level cost disclosure in the corpus is a PRIIP-BIB for a different product, showing a 5,3 % annual cost impact over twenty years on its own model case [S10]. Sized so the first-year acquisition outgo modestly exceeds what the *Zillmerung* recovers |
| Commission | 2,5 % of the *Beitragssumme* initial; 1,5 % renewal | Set at the 25 ‰ *zillmering* ceiling [R7], which is **not** a commission cap [R29]. **No carrier commission rate is established anywhere in the corpus** |
| `decl_rate` held level | 2,70 % for the whole projection | The **level** is [R26]'s report of Allianz's **2025** declaration for a combined classic life-and-annuity book — no carrier publishes an endowment rate — and holding it level is a modelling choice, not a forecast. `low` and `nil` ship so the sensitivity is exercisable |
| `term_rate` | 0,40 % p.a. of the *Deckungskapital* | **No terminal-bonus rate of any kind was established, for any insurer, in any year** (gap 1) |
| `ans_rate` | 2,70 %, equal to `decl_rate` | A market convention. It matters because `ans_rate > rechnungszins` is what produces the maturity/death asymmetry between the two surplus systems [R28] |
| `term_surr_share`, `bwr_rate` | 0.0 | Not inventing an entitlement the sources do not describe; and the *Sicherungsbedarf* has routinely exhausted the *Bewertungsreserven* [R1] [R8] |
| `storno_rate` schedule | 10 / 7,5 / 5 / 2,5 % by duration band | Against **three** carrier schedules on three incompatible bases — 0–20 % of the *Deckungskapital* decaying to nil over the last ten years, under collective action and a BGH remittal [S3] [R22] [R30]; 50 € + 0,15 % of premiums × years remaining [S9]; 100 € + 0,2 % of (sum insured − reserve) [S18]. Three figures on three bases are not a market range; a declining percentage of the reserve matches one of the three and is the only shape the model's state variables express |
| `lapse_rate` schedule | 5 / 3,5 / 2 / 6 / 2,5 %, and **0** in the final year | The **shape** follows the twelve-year tax threshold [R10] [REG-R45]; the **levels** are not sourced (gap 10). The final-year zero is what makes the survivors leave as a maturity |
| `suicide_share` | 0.02 | § 161 VVG's rule is sourced [R4]; **no source gives a suicide share of deaths at any age** |
| `bfz_min_si` | 2 500 € | § 165 VVG's test is sourced [R3]; no carrier's *Mindestversicherungsleistung* was located |
| Five-year spreading read as straight-line | `max(0, 1 − k/5)` | § 169 Abs. 3's *gleichmäßige Verteilung* [R2] admits a five-year *Zillmerung* reading too, which gives a slightly lower floor at durations 1–4 and the same value from 5 |
| *Bilanztermin* → policy-year end | — | Die Bayerische allocates at 31 December [S9]; on a policy-year grid that falls inside a policy year for every contract not written on 1 January. Gothaer instead allocates at the policy's own *Stammtag* [S7] and VPV at the start of the policy year [S18], so the policy-year convention is one of the observed ones. The effect against a calendar-year allocation is a timing shift of up to one year |
| `zillmer_on = 0` (model point 13) | switch | § 4 DeckRV sets a **ceiling**, not a mandate [R7], but every carrier wording read applies the *Verrechnungsverfahren* at 2,5 % or, pre-2015, 4 % [S7] [S9] [S18]. The un-zillmered point exercises the invariance, not an observed market option |
| Surplus *Wartezeit* = none | — | The wordings give three answers: none [S9], one year [S18], three years [S7] tariff group A and [S3]. The model takes the shortest |
| DeckRV split years | 1994 and 2000 take the **higher** rate; 2027+ hold 1,00 % | The published history splits both years mid-year and a year-keyed table cannot [REG-R15], so `check_rechnungszins_cap()` is permissive in exactly those two years |
| `prem_freq_load` values | 1,000 / 1,020 / 1,030 / 1,050 | The 2 / 3 / 5 % market range is cited [R28]; **no carrier publishes its own scale** |
| Behaviour modules off | `beta_shock = 0`, `lapse_gap_a = 0` | No German calibration of either exists |
| The fourteen model points | — | No entry age, premium level or sum-insured band was established (gap 21); the anchor is a construction from the term band plus the twelve-year tax minimum |

The quantities that are **not** standardizations are the two DeckRV ceilings [R7]
[REG-R15] [REG-R16], the 2,70 % declared rate itself [R26], and the structural rules — the
surplus base and timing, the § 169 calculation and floor, the *Stornoabzug* biting on the
guaranteed value, the § 165 test, the § 161 substitution, premium cessation on death, and
the *echte* / *unechte* distinction.

## Tests

`tests/test_kapitallebensversicherung_de.py` asserts all twenty-five rows — policy years 1 to
25 — of the notes' worked example to the cent off `result_cf_annual()` and `pols_if` to six
decimals, the twelve months of policy year 1 on the monthly frame beside them, the totals at full
precision, the ten printed rows of the state table, the notes' four independent rebuilds — the
*Bruttobeitrag* from the equivalence, the first anniversary's reserve by Fackler, the year-2
surplus credit and the year-12 surrender payment from its three parts — the closure
identity, the *Einmalbeitrag* and *Überschussverwendung* variants, every `check_*()` and its
residual, and **one test per numbered modeling pitfall**: the declared rate derived and not
added, the surplus base being the reserve, the negative-base guard shown on a 40 ‰ cohort,
three reserves rather than one, the § 4 cap and the § 169 floor asserted separately, the
*Stornoabzug* sparing the *Überschussguthaben*, § 161 substituting rather than forfeiting,
*Beitragsfreistellung* succeeding and failing, a paid-up policy staying in force, the lapse
table's [std] provenance, the premium-cessation rule applied once, the *Risikozuschlag*
reaching only the pricing death leg, one table serving both legs, the two mortality bases
kept apart, the surplus systems' asymmetry, the *Zahlbeitrag* not being guaranteed, `sex`
never reaching the premium, and the *Ablauf* year having no surrender.

The conversion added its own group: that the annual layer is **unchanged** — `pols_if` at every
anniversary, every reserve and every ledger balance equal to the annual-step model's — that the
two decrement rates compound rather than divide, that `result_cf_annual()` reproduces the annual
totals column by column, that a mid-year exit is paid the last anniversary's balances, that the
guaranteed leg of a first-year surrender is nil, that the *Beitragsfreistellung* failure lands in
the anniversary month rather than being spread over twelve, and that an annual payer is charged
in one month of each policy year and a monthly payer in all twelve.

```bash
python -m pytest tests/test_kapitallebensversicherung_de.py -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-kapitallebensversicherung-r1
[R10]: #delib-kapitallebensversicherung-r10
[R14]: #delib-kapitallebensversicherung-r14
[R15]: #delib-kapitallebensversicherung-r15
[R2]: #delib-kapitallebensversicherung-r2
[R20]: #delib-kapitallebensversicherung-r20
[R22]: #delib-kapitallebensversicherung-r22
[R26]: #delib-kapitallebensversicherung-r26
[R28]: #delib-kapitallebensversicherung-r28
[R29]: #delib-kapitallebensversicherung-r29
[R3]: #delib-kapitallebensversicherung-r3
[R30]: #delib-kapitallebensversicherung-r30
[R4]: #delib-kapitallebensversicherung-r4
[R5]: #delib-kapitallebensversicherung-r5
[R7]: #delib-kapitallebensversicherung-r7
[R8]: #delib-kapitallebensversicherung-r8
[REG-R1]: #delib-reg-r1
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R2]: #delib-reg-r2
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R34]: #delib-reg-r34
[REG-R45]: #delib-reg-r45
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R53]: #delib-reg-r53
[REG-R6]: #delib-reg-r6
[std]: #delib-std
<!-- END generated citation links -->
