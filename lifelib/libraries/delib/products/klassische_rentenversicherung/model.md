# Implementation Notes

**Status:** Draft, 2026-08-29. Built from
[`technical-notes.md`](technical-notes.md); the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The contractual
> mechanics are sourced from retrieved clause text — the *Deckungskapital* as the premium net of
> risk and expense cover accumulated at the *Rechnungszins* [S8] [S11], the *Höchstzillmersatz* of
> 25 ‰ at § 4 Abs. 1 DeckRV [R7] [REG-R16], the § 169 Abs. 3 surrender floor and the § 169 Abs. 5
> *Stornoabzug* conditions [R1] [REG-R28], the § 165 paid-up rule and its minimum-benefit branch
> [R2], the death-benefit designs [S4] [S8] [S9] [R24], the conversion at
> `max(garantierter, aktueller) Rentenfaktor` [S9] [S14] [S18], the *Bewertungsreserven*
> crystallisation at the transition to annuity payment § 153 Abs. 4 VVG [R4] [S4], and the
> *Rentengarantiezeit* [S1] [S4] [S9]. **Every level in this model is still a standardization**,
> but that is now a choice and not a necessity: a retrieval pass on 2026-08-30 established a
> current declared surplus rate [S15] and a *Rentenfaktor* market range [R19] [R24], and the model
> does **not** use them — see *Where the model diverges from a retrieved document* below. No charge
> parameter, expense or behavioural rate is established at any German carrier, and the DAV tables —
> DAV 2004 R here [R12] [R13] — are the property of the Deutsche Aktuarvereinigung, are not public,
> and are cited by name rather than redistributed. Replace the decrement, charge and rate tables
> with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/klassische_rentenversicherung/run.py
python products/klassische_rentenversicherung/run.py 6     # the 2,75 % legacy vintage
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/klassische_rentenversicherung/RV_DE_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell,
`DE-RV-0001`. `result_cf()` returns a `DataFrame` indexed by the policy **month** `t` with one column
per cash flow line; `result_cf_annual()` sums it into policy years, which is the view the technical
notes' worked example is stated on; and `result_pols()` is the **annual state** behind both — the
rates, the premium decomposition, the three account balances per policy and at fund level, the year's
credits, the surrender value and the death benefit, at each anniversary. The frames are separate on
purpose: a cash flow statement whose columns do not all sum to its bottom line is one a reader has to
know which columns to skip, and a state table that moves once a year should not be printed twelve
times over.

The model and both its Spaces carry docstrings: `model.doc` describes the product and the
projection basis, `model.Projection.doc` holds the mapping between the notes' symbols and the
cells names, and `model.Data.doc` says what each input file is and, for the three proxies,
what it is *not*.

## Two clocks: a monthly frame over a mostly annual product

`t` is the **policy month index, 0-based and counted from issue**, and
`proj_len() = 12 × proj_len_y()` is the frame's **exclusive** end, with
`proj_len_y() = omega_age() − issue_age` the number of policy years. The frame is
`t = t_start() … proj_len() − 1`, contiguous, with `t_start() = 12 × duration_init` — `duration_init`
being an elapsed count of policy **years**, so the conversion is a multiplication. The anchor cell
publishes **852 rows, `t` = 0 to 851**, seventy-one policy years running to attained age 121; the
in-force point 6 (`duration_init` = 20) opens at `t = 240`. A life annuity has no term, so the
horizon is the age at which the annuitant cannot survive further.

**Almost nothing on this product is monthly, and the argument of a cells says so.** Cells that state
an **annual account** take a 0-based policy year `k` — the premium and its whole decomposition, the
*Deckungskapital*, the *Ansammlungsguthaben*, the § 169 Abs. 3 spread account, the declared rate and
the interest surplus, the surrender value, the death benefit, the *Beitragsfreistellung* election and
the *Überschussrente* step. Cells that state a **month** take `t` — the in force, the three
decrements, the claims, the annuity instalment, the expenses and every `result_cf()` column.
`duration(t) = t // 12` is the bridge, `policy_year(t) = duration(t) + 1` is the contractual 1-based
label, `age(t)` and `calendar_year(t)` both step on the **anniversary**, and
`is_anniv(t) = (t % 12 == 11)` marks the month the annual machinery acts in.

The decrement rates take `t` and return the **year's annual** rate — the vectors the notes tabulate
and `result_pols()` prints — while `mort_rate_mth(t)` and `lapse_rate_mth(t)` are what the recursion
applies, each `1 − (1 − r)^(1/12)`, so twelve of each compound back to the year's rate. That is what
leaves the whole annual layer **bit-identical** to the annual-step model this replaced, on all
fourteen model points: `pols_if` at every anniversary, both account balances, the § 169 floor, the
surrender value, the conversion capital and the premium income are unchanged, and `result_pols()` is
row for row the table it was.

**What the finer grid changed.** Three things, and the largest is the one the product is named for:

| | Annual grid | Monthly grid | Why |
|---|---|---|---|
| `annuity_payments` | 23 485,03 € | **23 115,89 €** | The *Rente* is monthly and is now paid monthly, in advance. Inside the *Rentengarantiezeit* the two agree to the cent, the count being fixed; the whole −369,14 € is in the survivor-weighted tail |
| `claims_death` / `claims_lapse` | 1 038,91 € / 10 670,70 € | **1 022,04 € / 10 688,30 €** | Deaths and surrenders compete month by month rather than once a year. The total exits at every anniversary are unchanged; the split is not |
| `expenses` | 1 669,77 € | **1 646,77 €** | A policy leaving mid-year bears administration for the months it was there |

**What it did not change.** The premium: § 12 Abs. 1 VVG makes the *Versicherungsperiode* the **year**
for this tariff and the *Beitrag* is payable in advance for it, so `prem_due(t)` is true in the first
month of each policy year and nowhere else, and premium income is identical. And what a claim is
**paid**: § 169 Abs. 3 VVG strikes the value *zum Schluss der laufenden Versicherungsperiode* and not
at the cancellation date, so a policy leaving in any month of policy year `k` is paid `cv_pp(k)` or
`db_pp(k)` — the year-end value it paid the year's premium in advance for. What moved is **when** the
claim falls and **how many policies are exposed** to it. (`KLV_DE_S` is the contrast: there the
*echt* reading makes the period genuinely monthly, two model points differ in nothing else, and the
instalment stream is in the frame.)

Two rates of 1 are **certainties rather than rates** and are placed in the anniversary month instead
of being twelfth-rooted: the terminal `q = 1` of the mortality proxy, which is the table's closure
convention, and the § 165 cash-out, which is a dated contractual act. Spreading either geometrically
would empty the cohort eleven months early.

**Time-like inputs.** No CSV value changed, in this conversion or in the earlier move to a 0-based
frame. `lapse_table.csv`'s `duration` is the **contractual policy year**, 1-based, and the model reads
it through `policy_year(t) = duration(t) + 1` — the § 20 EStG twelve-year step stays at duration 12,
which the model reads across months 132 to 143. `decl_rate_table.csv`'s `calendar_year` and the `age`
keys of `mort_table.csv` and `rentenfaktor_table.csv` are absolute and unaffected. On the model point
table, `duration_init` is an elapsed count of **years** and is `k_start()`, with `t_start()` twelve
times it; `aufschub_y`, `prem_term_y` and `rgz_years` are **counts of years**, so the comparisons
moved (`t < 12n` for the accumulation phase, `12m` guaranteed instalments) rather than the values;
and `pup_year` stays the 1-based contractual policy year of the *Beitragsfreistellung*, with 0
meaning "never", which the model maps to the paid-up policy year `k = pup_year − 1`.
`freq_load_table.csv`'s `n_instalments` column remains documentation: see *The
Ratenzahlungszuschlag*, below.

## The declared rate contains the guarantee — the German delta

This is the one thing a reader arriving from a US or UK account-value model will get wrong, and
it is the first listed modeling pitfall. The German *laufende Verzinsung* **is** the
*Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung* [REG-R53], not a surplus paid
on top of the guarantee. So:

```
bonus_rate(k) = max(0, decl_rate(k) − int_rate_guar())
```

and the two credits together deliver the declared rate on the post-premium *Deckungskapital*
and never more. On the anchor cell, the first policy year (`k = 0`):

| | rate | on | amount |
|---|---|---|---|
| `int_credited_pp(0)` | 1,00 % | 1 600,6317 € | 16,0063 € |
| interest-surplus term of `bonus_credited_pp(0)` | 1,55 % | 1 600,6317 € | 24,8098 € |
| **together** | **2,55 %** | 1 600,6317 € | **40,8161 €** |

A model that credits 1,00 % *and* a further 2,55 % puts 56,82 € into year one instead of
40,82 €, and reaches 63 768,69 € of accumulated value at the *Rentenbeginn* against the correct
58 788,98 € — 8,5 % too much, the whole error sitting in the *Ansammlungsguthaben*, 12 698,26 €
against 7 718,55 €.

The mirror image is model point 6, a 2,75 % legacy vintage against the same 2,55 % declaration:
`bonus_rate(k)` is **zero in every policy year** while `int_credited_pp(k)` is the largest in the table.
A contract already guaranteed more than the insurer is declaring receives no interest surplus at
all — a real German result, and what the `max(0, .)` exists to produce. Over point 6's five
remaining accumulation years the model credits 9 187,70 € of guaranteed interest and 399,55 € of
surplus, every euro of it the declared rate on the *Ansammlungsguthaben*'s **own** balance.

What the model does **not** do is decompose the declaration into its four German components:
*Zinsüberschuss*, *Risikoüberschuss*, *Kostenüberschuss* and *Schlussüberschussanteil* are one
declared rate here. Only the first was established for this product [R24], the other three
belong to the `kapitallebensversicherung` file that shares this chassis, and inventing a split
would be inventing three rates.

## The guarantee vintage is a model-point attribute

`int_rate_guar()` reads the model point, not a Reference. The lock is statutory: § 2 Abs. 2 Satz 1
DeckRV, *"Bei Versicherungsverträgen mit Zinsgarantie gilt der von einem Versicherungsunternehmen zum
Zeitpunkt des Vertragsabschlusses verwendete Rechnungszins für die Berechnung der
Deckungsrückstellung für die gesamte Laufzeit des Vertrages"* [R7] [REG-R14]. So a German life book is
a **layered stack of guarantee vintages** rather than one rate: points 1, 6 and 14 credit 1,00 %,
2,75 % and 0,90 % in one run. One carrier's own packs show the stack forming — DAV 2004R at 1,25 % in
Fassung 07/2015 [S5] [S6] and at 1,00 % in Fassung 01/2025 and 01/2026 [S7] [S16] [S4].

Re-running point 6 on a single global 1,00 % rate shows *how* that error surfaces: its
*Deckungskapital* at *Rentenbeginn* falls 7,7 %, from 82 833,38 € to 76 439,87 €, its
*Ansammlungsguthaben* rises 156 %, from 3 629,35 € to 9 292,76 €, and the conversion capital
moves by −0,8 %. The vintage error is a **misallocation between the two accounts**, not a hole
in the total, which is why it survives a reasonableness check on the headline.

## The within-year order, which no source fixes

Premium in advance, then the charges, then the *Rechnungszins* on what is left:

```
av_pp_at(k, "AFT_PREM") = av_pp(k) + prem_to_av_pp(k) − charge_from_av_pp(k)
int_credited_pp(k)      = int_rate_guar() × av_pp_at(k, "AFT_PREM")
av_pp_at(k, "AFT_INT")  = av_pp_at(k, "AFT_PREM") + int_credited_pp(k)
```

All three take a **policy year**. The *Rechnungszins* is credited per *Versicherungsjahr* and the
monthly grid does not interpolate it: there is no monthly *Deckungskapital* in this tariff, and a
model that invented one would be inventing a crediting rule no wording states.

**This ordering is a standardization.** No document in the corpus fixes the sequence of premium
credit, charge deduction and interest accrual, and it is the most consequential such choice in
the model: crediting interest on the opening balance alone changes year-one interest by the
whole of `i × (S(1) − C(1))`, 16,01 € of a 1 616,64 € closing balance on the anchor cell.

Two further conventions are **[std]**. `charge_risk_pp` and `charge_admin_pp` are struck on
**start-of-year** balances, or the recursion is circular — a risk charge on the post-charge
balance depends on itself. And charges are met **from the premium where there is one and from
the *Deckungskapital* where there is not**, which makes a *Beitragsfreistellung* cost something
instead of being free.

## The *Ratenzahlungszuschlag* is the whole of what the *Zahlweise* does

Instalments are **not** modelled, on the monthly grid as on the annual one: `freq_load()` charges the
loaded annual amount in the first month of the policy year, `prem_due(t)` is
`duration_mth(t) % 12 == 0`, and `n_instalments` stays documentation — so a monthly payer here pays
1,050 × the annual premium once a year, not twelve times.

That is a decision rather than an omission, and three things fix it. § 12 Abs. 1 VVG makes the
*Versicherungsperiode* the **year** where premiums are not measured in shorter periods. The
*Deckungskapital* the whole model turns on is defined at anniversaries and nowhere between them. And
§ 169 Abs. 3 VVG pays a mid-period exit the value struck at the **end** of that period — so a premium
payable in advance for the year and a value earned for the year are the consistent pair, and
splitting the premium without splitting the value would credit a policy with a year it did not pay
for. Modelling the instalments would need an unearned-premium convention on mid-year exits that no
source in this product's corpus establishes.

`KLV_DE_S` is the contrast, and the reason this is a considered choice: there the *echt* / *unecht*
distinction turns on whether the *Versicherungsperiode* is genuinely monthly, two model points differ
in nothing else, and the instalment stream is therefore in the frame.

## The § 169 Abs. 3 floor, carried as a difference

The surrender value is floored at the *Deckungskapital* that results from spreading the charged
acquisition costs **evenly over the first five contract years** — § 169 Abs. 3 Satz 1 VVG at article
level [R1], restated verbatim by five carriers [S1] [S4] [S8] [S9] [S11] [REG-R28]. The two accounts
differ only in that charge, so the model carries the difference, not a second full recursion:

```
spread_diff_pp_at(k, "AFT_INT") = (Δ(k) + charge_acq_pp(k) − charge_acq_spread_pp(k)) × (1 + i)
```

with `gamma` and `rho` taken at the same euro amount in both **[std]**, which is what makes the
difference exact. Two consequences are not obvious. The difference is **large in the first five
years** — on the anchor cell the whole 1 275,00 € is taken in the first year against 255,00 € — and it
**never returns to zero**, because the spread account earns the *Rechnungszins* on what has not
yet been deducted. So the floor sits above the tariff *Deckungskapital* at every duration;
whether it *binds* depends on the *Ansammlungsguthaben* and *Stornoabzug* beside it.

The floor is the § 169 Abs. 3 *Deckungskapital* **alone**: profit shares sit on top of the
statutory minimum rather than inside it, the reading § 165 Abs. 2's "surrender value …
including profit shares" supports [R2]. That lets both branches of
`cv_pp(k) = max(cv_tariff_pp(k), cv_floor_pp(k))` be exercised on the anchor cell alone — the
floor binds through `k = 3`, at 2 646,84 € against a tariff 1 608,62 € in the first year, and stops
binding at `t = 4`. The alternative reading, in which the floor also carries the
*Ansammlungsguthaben*, is **not implemented**; it would bind at every duration.

The *Stornoabzug* is a **flat percentage of the pre-deduction value with no duration term**,
the shape § 169 Abs. 5 allows: a deduction is permitted only if agreed, quantified and
appropriate, and one for not-yet-amortised *Abschluss- und Vertriebskosten* is void [R1] — a
duration-graded deduction unwinding over the first years would be exactly the void kind.
Whatever it is set to, `cv_pp` cannot fall below `cv_floor_pp`.

## *Beitragsfreistellung* is an election, not a decrement

*Beitragsfreistellung* is a **deterministic election** in the contractual policy year `pup_year`
— policy year `k = pup_year − 1` — rather than a rate: a
scalar per-policy account cannot carry two sub-populations with different *Deckungskapital*,
and no source establishes a rate. Both § 165 VVG branches [R2] are implemented and exercised:

- **Conversion** (model point 7). `prem_pp(k) = 0` from the paid-up year, the *Deckungskapital* is
  **reset to** `pup_value_pp()` — the § 169 Abs. 3–5 value, 30 303,91 € against a zillmered
  30 261,45 € — the *Ansammlungsguthaben* is untouched, `spread_diff_pp` goes to zero because
  the two accounts have merged, and `charge_admin_pp` switches from `gamma_rate` to
  `gamma_pup_rate`. No *Stornoabzug* is taken on this route **[std]**: Abs. 5 is drafted for a
  payout on *Kündigung*, and here the contract continues.
- **Cash-out** (model point 8). Where the paid-up annuity would fall below the
  *Mindestversicherungsleistung* — 5,45 € a month against a 30,00 € threshold **[std]** —
  § 165 has the contract cashed out at the surrender value including profit shares instead of
  made paid-up, so the whole surviving cohort leaves in the **last month** of policy year
  `k = pup_year − 2`. That is one of the two places `lapse_rate` returns 1 rather than a rate, and
  `lapse_rate_mth` places the certainty in the anniversary month rather than spreading it
  geometrically: § 165 makes the cash-out fall at the end of the *Versicherungsperiode*, not a
  twelfth of the way into it.

`pup_uplift(k)` is booked in the **transition year** `k = pup_year − 2`, weighted by
`pols_if(12 (pup_year − 1))`, because that is the year whose roll-forward needs it; it is real money
— 28,39 € on point 7 — and publishing it is what lets `check_av_roll_fwd()` close there.

A *Beitragsfreistellung* is **not** a lapse: the paid-up contract keeps its guarantee vintage
and its guaranteed *Rentenfaktor* and pays a reduced benefit, while the surrendered one is
gone for cash. On point 7 the conversion itself moves no policy — `lapse_rate` in policy year 9 is
the ordinary duration-9 table rate of 3,5 %, not 1. What is **not** true is that surrender ceases:
a *beitragsfrei* contract keeps its § 168 VVG *Kündigung* right, so `claims_lapse` stays
positive from the paid-up year on, 764,60 € in policy year 10.

## The *Rentenbeginn*: three things at one instant

Everything happens at the end of the last accumulation **month** `t = 12n − 1`, where
`n = aufschub_y` is the deferment period in years, on the survivors of that month's decrements. It is
an anniversary, so every quantity below is the annual-step model's to the last bit:

```
capital_gross_pp   = av_pp_at(n−1, "AFT_INT") + av_sur_pp_at(n−1, "AFT_INT")
capital_conv_pp    = max(guar_capital_pp, capital_gross_pp + val_reserve_pp)
annuity_rate_appl  = max(annuity_rate_guar, annuity_rate_curr)
annuity_guar_mth_pp = capital_conv_pp / 10 000 × annuity_rate_appl
```

On the anchor cell that is `max(0,00; 58 788,98 + 881,83) = 59 670,82 €` converted at
`max(28,00; 32,00) = 32,00` into a *garantierte Rente* of 190,9466 € a month.

The applied factor is a **written option on the insurer's own future annuity tariff**, and the
deterministic path does not price it. Both branches ship: the current factor wins on the anchor
cell, and on point 13 the guarantee binds over a `low` scenario while its `guar_capital_pp`
floor of 60 000,00 € binds at the same time. A model applying the guaranteed factor alone
understates the anchor's annuity by 12,5 %, the annuity scaling linearly in `f`.

`val_reserve_pp` is the *Bewertungsreserven* crystallisation, which § 153 Abs. 3 Satz 2 VVG makes
*hälftig* and which § 153 Abs. 4 VVG puts, **for annuities specifically**, at the *Beendigung der
Ansparphase* [R4]; [S4] § 3 Abs. 2 and [S15] apply it in those terms. The
**rate** is a placeholder, and the continuing participation during the payout phase that the
same source establishes is **not modelled**. The commuting policyholders receive
`capital_conv_pp`, the same capital the annuitants convert: the corpus gives no basis for
paying them less, and inventing one would be a charge no source supports.

## The *Rentengarantiezeit* is paid to the dead

Inside the guarantee window the instalment is due whether or not the annuitant is alive [R17]
[R24], so the annuity is weighted by the **annuitised** count and not by survivors:

```
pols_annuity(t) = pols_annuitization(12n−1)   for 12n ≤ t < 12n + 12m
                = pols_if(t)                  for t ≥ 12n + 12m
```

**The window is `12m` guaranteed instalments, not `m` annual lumps** — which is what a
*Rentengarantiezeit* is, the *Rente* being a monthly payment, and a thing the annual grid could only
approximate. On the anchor cell the two counts differ over `t = 204 … 323` and coincide from
`t = 324`. In policy year 27, the last guaranteed year, `pols_annuity` holds at 0,336143 in all
twelve months while `pols_if` falls to 0,307366 by the last of them, so the year's outgo is the full
862,65 € and not the roughly 800 € a survivor weighting would give.

Because the count is fixed inside the window, the annual and monthly grids pay the **same money to
the cent** there; they part company from policy year 28, where twelve monthly measurements of a
falling count are not one annual one, and that is where the whole −369,14 € of the conversion sits.

`check_annuity_guarantee()` states the identity as
`pols_annuity(t) = max(pols_if(t), 1{12n ≤ t < 12n+12m} × pols_annuitization(12n−1))`, which holds
because `pols_if(t) ≤ pols_annuitization(12n−1)` throughout the payout phase — and stating it that
way is what makes the check independent of the definition it checks.

## No death benefit after the *Rentenbeginn* — a modelled choice, not an evidential gap

`db_pp(k)` is zero for every `k ≥ n`, on every model point, and a test asserts it. **The reason has
changed.** *Beitragsrückgewähr in der Rentenbezugsphase* — the refund of premiums less instalments
received, on death after the *Rentenbeginn* — was recorded as unmentioned by any source in this
corpus. It is in [S4] § 1 Abs. 5, offered as an alternative to the *Rentengarantiezeit*: the premiums
paid less rider premiums and less annuities already received, the deduction taken only at the
inception-guaranteed annuity level, with the claim extinguishing once instalments exceed premiums,
and with the surplus attributable to it accumulated at interest until it is paid (§ 3 Abs. 7).
Implementing it means a second post-*Rentenbeginn* benefit path, a running refund balance and a new
decrement interaction, all of which move the worked example and the golden tests — so it is
**recorded as a known omission and left out of this pass**. The two mechanics that are modelled or
deliberately off remain the *Rentengarantiezeit* [S1] [S4] [S9], which is modelled, and the
survivor's-annuity rider [S10], which is off and which in any case begins only after a guarantee
period expires. Deaths still *happen* in the payout phase: they move `pols_if`, end the annuity
outside the guarantee window and carry an `expense_claim_pp` settlement cost, and they pay no benefit.

## Inputs are external files

The eight input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `RV_DE_S/` holds nothing but formulas:

```
products/klassische_rentenversicherung/
  model_point_table.csv  mort_table.csv  decl_rate_table.csv   <- inputs live here,
  rentenfaktor_table.csv  charge_table.csv  lapse_table.csv       beside run.py and
  freq_load_table.csv  param_table.csv  run.py                    the four documents
  RV_DE_S/                     <- formulas only
    __init__.py  _system.json     (model docstring)
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its input file beside the model
and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/` directory and
no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache, and readers placed there would re-read every file for every policy.
They live instead in an unparameterized **`Data`** Space, which `Projection` references as
`data` — so each file is read once per model however many policies are projected, and the
conventions suite counts the reads against a registered file set. `Data.input_dir()` resolves
the location from `_model.path.parent` when the model is read, so it works wherever the
repository is checked out.

| Reference | Cells | File | What it carries |
|---|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` | Fourteen policies, thirty columns. **Point 1 is the worked-example anchor cell.** The one file exempt from the `provenance` rule: a model point is a configuration, not an assumption |
| `mort_file` | `mort_table()` | `mort_table.csv` | `q_base(sex, age)` in the 2005 base year and an age-dependent `improve(age)`. A **[std]** Gompertz proxy, `0.002000 × 1.09^(age−50)` male and `0.001300 × 1.09^(age−50)` female, closed at `q = 1` at age 120. **Not** DAV 2004 R, which is DAV property and is not shipped [R12] [R13]. A replacement must preserve `q_base(M, 50) = 0.002000`, the 2005 base year, the terminal `q = 1`, and the **generational** form |
| `decl_rate_file` | `decl_rate_table()` | `decl_rate_table.csv` | The declared *laufende Verzinsung* by scenario and calendar year, 2005–2060, clamped at both ends. `base` level at 2,55 %, `low` at 1,50 % **[std]** |
| `rentenfaktor_file` | `rentenfaktor_table()` | `rentenfaktor_table.csv` | The *aktueller Rentenfaktor* by scenario and attained age at *Rentenbeginn*, rising 2,5 % per year of age. `base` / `low` / `high` anchored at age 67 on 32,00 € / 25,50 € / 35,00 € **[std]** — no market level was established for any carrier in any year (gap 3) |
| `charge_file` | `charge_table()` | `charge_table.csv` | Two charge sets, `zillmer_25` and `zillmer_40`, eight items each, keyed per item so every number carries its own provenance |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` | Annual surrender by contractual policy year (`duration` 1–40, read through `policy_year(t)`), last row held. Levels **[std]**; the one shaped feature is the **duration-12 step** at the § 20 Abs. 1 Nr. 6 EStG twelve-year threshold [R6] [REG-R45] |
| `freq_load_file` | `freq_load_table()` | `freq_load_table.csv` | The *Ratenzahlungszuschlag*: 1,000 / 1,020 / 1,030 / 1,050 **[std]**, and `n_instalments` for documentation — the premium is collected annually in advance whatever the elected frequency, for the reasons under *The Ratenzahlungszuschlag* above |
| `param_file` | `param_table()` | `param_table.csv` | Every scalar that is neither a charge nor a rate table — the four expense levels and their inflation, `mort_be_factor`, `mort_base_year`, `omega_age`, `val_reserve_rate`, the three *Überschussrente* parameters and `roll_fwd_tol`. They live in a file rather than in References so that each carries its own provenance tag, which a Reference cannot |

**The trade-off:** the model is not portable on its own — copy `RV_DE_S/` without the CSVs and
it reads fine, then fails on first evaluation. What you gain is that a diff of the model shows
logic changes only, and an input can be swapped in place: point `Data.mort_file` at another
same-schema file and the projection follows, with no formula change. Every file but the model
point table carries a per-row `provenance` column, this library's second ruling — an
assumption says on its own row where it came from, and the conventions suite checks it.

## The published identities

Nine `check_*` cells travel with the model, each taking no argument and returning a `bool` over the
whole frame, each with a residual beside it. **The residual's argument follows its cells' clock:**
five monthly identities carry `check_*_resid(t)` over policy months, and four that state an annual
account — the two account roll-forwards, the premium split and the § 169 floor — carry
`check_*_resid(k)`, one per policy **year**. A monthly residual for the *Deckungskapital*
roll-forward would first have had to invent a monthly reserve, which is the error the two-clock split
exists to make impossible. (`check_annuity_conv()` is a scalar identity evaluated at one point, and
is the ninth.)

**`check_net_cf()` — delib's first ruling, the identity in one line:**

```
net_cf(t) = premiums(t) − claims_death(t) − claims_lapse(t) − claims_commutation(t)
            − annuity_payments(t) − expenses(t)
```

rebuilt **from `result_cf()`'s own columns** rather than from the cells, together with
`liability_cf(t) = −net_cf(t)` exactly. It fails if a published column and the headline number
ever stop being the same arithmetic — the failure it exists to catch.

| Check | What it closes |
|---|---|
| `check_net_cf` | the cash flow statement above, and the sign convention |
| `check_pols_roll_fwd` | `pols_if(t) − pols_if(t+1) = deaths + surrenders + commutations`, month by month |
| `check_decrement_closure` | exits summed **directly** plus `pols_if(t+1)` equal the original cohort — 0,371014 + 0,484924 + 0,144061 + 0,000000 = 1,000000 on the anchor cell |
| `check_av_roll_fwd` | `av + prem_to_av − charge_from_av + int_credited + pup_uplift − av_release = av(k+1)`, at fund level, per policy **year**, across the paid-up reset and the *Rentenbeginn* |
| `check_av_sur_roll_fwd` | `av_sur + bonus_credited − av_sur_release = av_sur(k+1)`, per policy **year**; nothing else touches the side account |
| `check_prem_split` | every euro of premium is saved or spent on a charge, and every euro of charge is met from the premium or from the account |
| `check_cv_floor` | `cv_pp = max(cv_tariff_pp, cv_floor_pp)`, and never below the § 169 Abs. 3 floor however large the *Stornoabzug* is set |
| `check_annuity_conv` | the conversion arithmetic, `f ≥ f_g`, and `K ≥ guar_capital_pp` |
| `check_annuity_guarantee` | the *Rentengarantiezeit* weighting, stated with a `max` so it is independent of the definition it checks |

## Modules that are implemented and off in the base run

| Module | Switch | Off value | What it does when switched on |
|---|---|---|---|
| *Dynamik* (*Anpassungsversicherung*) | `dynamik_rate` on the model point | `0.0000` | Grows the scheduled premium by `(1 + rate)^k` and the *Beitragssumme* with it. On at 5 % on model point 12, where it lifts the *Beitragssumme* from 33 000,00 € to 57 757,82 € [S4] |
| *Beitragsfreistellung* | `pup_year` | `0` | The § 165 election, in both branches — conversion on point 7, cash-out on point 8 [R2] |
| *Kapitalwahlrecht* | `kapitalwahl_rate` | `0.30` on the anchor | The commutation take-up. `0.00` on points 2 and 10, `1.00` on point 9, which empties the cohort at `t = 12n − 1` [R6] [R21] |
| Death benefit including surplus | `db_incl_surplus` | `0` | Adds the *Ansammlungsguthaben* to the death benefit, the "premiums plus the attributable *Überschussbeteiligung*" form. On on points 4 and 12 [R24] |
| Guaranteed contract value | `guar_capital_pp` | `0.00` | The minimum guaranteed contract value floor at conversion. Binds on point 13 at 60 000,00 € [S9] |
| Payout-phase administration charge | `annuity_admin_rate` | recorded at 1,5 %, **never applied** | Would deduct a charge from each instalment. It is not applied because the *Rentenfaktor* is exogenous here and already carries the tariff's payout loading; deducting again charges it twice |
| `annuity_due_factor()` | — | diagnostic only | The **monthly** annuity-due factor on the shipped proxy at the guarantee basis, 273,7821 on the anchor, so the *Rentenfaktor* the proxy would imply is `10 000 / 273,7821 = 36,53` against the shipped 32,00. **No cash flow reads it.** It exists because the [std] *Rentenfaktor* and the [std] annuity table are **not calibrated to each other**, and the *Rentenfaktor* is authoritative. Monthly is what the annuity is; the annual-step model needed a twelve in the denominator to say the same thing |

Not implemented at all, and named here rather than left to be discovered: no *Bonusrente*
ledger; no *Zuzahlung* (gap 15); no survivor's-annuity or BU rider [S10]; no § 163 VVG
adjustment of the guaranteed *Rentenfaktor*, recorded as a model risk instead [R3] [R17]; no
dynamic surrender, because the surrenderer forfeits a guaranteed *Rentenfaktor* struck on old
bases and a rate-gap formula does not capture that; no premium-default path, although § 166 VVG
makes German lapse a three-way decrement in reality; no *Wiederinkraftsetzung*; no continuing
*Bewertungsreserven* participation in the payout phase; and **no tax**, so the *Ertragsanteil*
[R5] and the *Halbeinkünfteverfahren* [R6] appear in the documents and not in the model.

## Sign convention

`net_cf` is **income positive** — premiums in, benefits, annuity instalments and expenses out —
the notes' own orientation and the library-wide sign. `liability_cf` publishes the same stream
outgo-positive, `liability_cf(t) = −net_cf(t)` exactly, and both are columns of `result_cf()` so
the identity is verifiable in the frame. A Solvency II best estimate is
`Σ v(t) × liability_cf(t)` plus a risk margin [REG-R1] [REG-R4]; nothing here discounts.

`av`, `av_sur`, `prem_to_av`, `int_credited` and `bonus_credited` are **state movements
reported, not cash flows summed**: they move money inside the contract, never cross the boundary,
and move once a policy year, so they are columns of `result_pols()` rather than of the cash flow
statement. The six that do cross it are `premiums`, the three `claims_*`, `annuity_payments` and
`expenses` — exactly what `check_net_cf()` reconciles, and the whole of `result_cf()`'s flow
columns.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` first and `savings/CashValue_SE` second
wherever those models have an analogue: `pols_*` for policy counts, `av_*` for account
values, plural nouns for cash flows, `*_rate` for rates, `*_pp` for per-policy amounts,
`claims(t, kind)` with an uppercase `kind` string, `av_pp_at(k, timing)` for the within-**year**
reads of the annual accounts and `pols_if_at(t, timing)` for the within-**month** reads of the
population. The technical notes use compact actuarial symbols; the full mapping lives in the
`Projection` Space docstring. Five cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `Ď(k)`, `D(k)` | `db_base_pp` / `db_pp` | Two different quantities with deliberately similar names. `db_base_pp` is measured on **start-of-year** balances and exists only to strike the *Risikobeitrag*, because a risk charge on the post-charge balance would be circular. `db_pp` is what a claim actually pays, on end-of-year balances. Both take a policy year: a death in any month of year `k` is paid `db_pp(k)` |
| `β(k)`, `γ(k)` vs the expense lines | `charge_*` / `expense_*` | A **charge** is a tariff deduction that moves money inside the contract and produces no cash flow; an **expense** is the insurer's own outgo and is a cash flow. `expenses(t)` is invariant to `beta_rate` and `gamma_rate`; `av_pp(k+1)` is not |
| `V(k)`, `A(k)` | `av_pp` / `av_sur_pp` | Two accounts, not one balance split in two. The *Deckungskapital* carries the guarantee and is credited at `int_rate_guar()`; the *Ansammlungsguthaben* is the *verzinsliche Ansammlung* side account, credited at `decl_rate(k)` on its own balance plus `bonus_rate(k)` on the *Deckungskapital*'s post-premium base. Each has its own roll-forward check, and both are annual |
| `l(t)`, `a(t)` | `pols_if` / `pols_annuity` | They differ inside the *Rentengarantiezeit* and nowhere else. `pols_if(t)` is the start-of-**month** count and the weight on every cash flow of the same row; `pols_annuity(t)` is the count the instalment is *paid on* |
| `q(t)`, `w(t)` | `mort_rate`, `lapse_rate` / `mort_rate_mth`, `lapse_rate_mth` | The library's two speeds, not two spellings of one rate. The unsuffixed name is the **annual** rate of the policy year, which is what the notes tabulate and `result_pols()` prints; the `_mth` name is the geometric twelfth the recursion applies. Nothing here applies an unsuffixed decrement rate, and nothing divides one by twelve |

**The chassis this model shares.** `KLV_DE_S` (`products/kapitallebensversicherung`) is the
same *Überschussbeteiligung* and *Deckungskapital* machinery with a maturity benefit where
this one has a conversion, and is the primary home of the four-component surplus split.
`Sofort_DE_S` (`products/sofortrente`) is this model's payout phase as a product in its own
right — which is why an immediate-annuity document is direct evidence for a deferred
contract's conversion basis [S13] [S16]. `Index_DE_S` and `FRV_DE_S` replace the crediting
mechanic and keep the conversion. Names that mean the same thing across all of them:
`model_point`, `proj_len`, `proj_len_y`, `t_start`, `k_start`, `duration`, `duration_mth`,
`is_anniv`, `policy_year`, `age`, `calendar_year`, `pols_if`, `pols_if_at`, `pols_death`,
`pols_lapse`, `mort_rate`, `mort_rate_mth`, `lapse_rate`, `lapse_rate_mth`, `prem_pp`, `premiums`,
`av_pp`, `av_pp_at`, `prem_to_av_pp`, `claims`, `expenses`, `net_cf`, `liability_cf`, `result_cf`,
`result_cf_annual`.

## Standardizations used

Everything below is **[std]** — chosen where the sources vary, are proprietary or are silent.

| [std] | Value | Rationale |
|---|---|---|
| Mortality proxy | Gompertz `q_base(M, 50) = 0.002000 × 1.09^(age−50)`, female `0.001300`, terminal `q = 1` at 120; improvement 1,5 % a year below age 60 grading to 0,5 % at 100 and zero at 110 | DAV 2004 R is DAV property and is not redistributable [R12] [R13]. The proxy keeps the **generational** structure, which is the part that matters, and none of the values; the improvement shape is a deliberate simplification of the *Starttrend* / *Zieltrend* construction, documented as one rather than presented as a replication |
| `mort_be_factor` | 1.15, **above one on purpose** | For an annuity, prudence means assuming mortality *lower* than expected, so the first-order table sits below best estimate. Only the level margin is reproduced; the real one runs in level and trend |
| *Rentenfaktor* paths | `base` 32,00 € at age 67, `low` 25,50 €, `high` 35,00 €, +2,5 % per year of age | Anchors chosen so both branches of `max(garantierter, aktueller)` are exercised by the shipped points. **They are not market levels and now sit above the observed range**: 2025 averages of 24,33–27,18 guaranteed and 27,27–30,40 current by deferment term to age 67 [R24], and a 2022 current-factor average of 25,97 [R19] |
| Declared rate paths | `base` 2,55 %, `low` 1,50 %, level | Inside the only public market-average pair the library has for 2025 [REG-R53]; a scenario rather than a forecast. **A carrier's 2026 declaration is now on the record and is higher** — 3,00 % total credited interest before the *Rentenbeginn*, 3,35 % during it [S15] |
| Surplus on the *Ansammlungsguthaben* | the **full** declared rate on its own balance | No source splits the side account's crediting from the main declaration |
| `beta_rate`, `gamma_rate`, `gamma_pup_rate` | 4,0 % of premium; 20 bp; 30 bp p.a. | No German carrier publishes a charge loading for this product (gap 14). The premium-free rate is higher because a paid-up contract still bears administration cost |
| Use of the *Höchstzillmersatz* cap | the cap itself, 25 ‰ / 40 ‰ | The **cap** is statutory — § 4 Abs. 1 Satz 2 DeckRV, *"Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten"* [R7] [REG-R16], restated by four carriers as "2,5 % der Beiträge" [S1] [S4] [S8] [S9]; charging exactly it is the standardization, and it is what makes the year-one *Sparbeitrag* thin and the § 169 Abs. 3 floor bite |
| `stornoabzug_rate` | 2,0 % on `zillmer_25`, nil on `zillmer_40` | § 169 Abs. 5's three conditions are cited [R1]. **The earlier rationale was wrong**: a duration-graded deduction is not what Abs. 5 voids — it voids a deduction *for unamortised acquisition costs* — and the retrieved wordings show duration tapering is ordinary market practice [S11] § 34 Abs. 4–5. Observed forms are none [S8] [S9], a flat 250 EUR [S4], or tapering percentages [S11]. The flat rate is a simplification of that spread |
| `min_annuity_mth` | 30,00 € a month | The § 165 *Mindestversicherungsleistung* requirement is statutory, its level contractual; two carriers set **25,00 € a month** [S4] [S9] and one 600,00 € a year for a partial surrender [S8]. 30,00 € is chosen so one model point trips the cash-out branch |
| `annuity_admin_rate` | 1,5 %, recorded and **not applied** | The *Rentenfaktor* is exogenous and already carries the tariff's payout loading |
| `val_reserve_rate` | 1,5 % of the accumulated value | The *hälftige* participation (§ 153 Abs. 3 Satz 2) and the *Rentenbeginn* crystallisation (§ 153 Abs. 4, annuities only) are statutory [R4] and applied by [S4] and [S15]; **no amount, ratio or reserve level is established anywhere** |
| *Überschussrente* | `sur_ann_rate` 12 %, `sur_ann_growth` 1,5 %, `sur_ann_theta` 0,5 | The three payout systems and their *directions* are established [R19] [R20] [R24]; no level, rate or split is |
| Expenses | 400,00 € acquisition, 45,00 € p.a. accumulation, 30,00 € p.a. payout, 120,00 € per settlement, 2,0 % inflation | No German carrier publishes an expense assumption (gap 14) |
| `freq_load` | 1,000 / 1,020 / 1,030 / 1,050 | No carrier's *Ratenzahlungszuschlag* was established (gap 14) |
| Surrender table | 6,0 % falling to 3,0 %, with a **6,0 % step at duration 12** | No German *Stornoquote* for this product was established (gap 20). The duration-12 shape is argued from the § 20 Abs. 1 Nr. 6 EStG threshold; every level is a placeholder |
| Within-year order and charge incidence | premium, then charges, then interest; `γ` and `ρ` on start-of-year balances; charges from the premium first, then from the account | No document in the corpus fixes the sequence. Start-of-year incidence keeps the recursion acyclic; premium-first incidence is what makes a paid-up contract pay for itself |
| § 169 Abs. 3 floor scope | the *Deckungskapital* **alone**, and no *Stornoabzug* on the paid-up route | Profit shares sit on top of the statutory minimum, the reading § 165 Abs. 2 supports; the alternative is named and not implemented. Abs. 5 is drafted for a payout on *Kündigung*, and on the paid-up route the contract continues |
| Annuity timing | one instalment at the **start of each month**, in advance | The basis is established — *"monatlich, jeweils zum Monatsersten"* [S9] § 1 Abs. 1 — and the monthly grid now models it as stated, so the annual-grid compression this row used to record is **gone**. What remains [std] is the exact payment date within the month, which no source fixes |
| *Kapitalabfindung* amount, decrement order, no notice period | `capital_conv_pp`, the same capital annuitants convert; deaths at the end of each **month**, then surrenders; the election effective at *Rentenbeginn* | The corpus gives no basis for paying commuters less. No source fixes the decrement order. **Notice periods are established and are not modelled**: three years, or twelve years / five months, at Zurich [S4] § 2 Abs. 2–3; twelve years at CosmosDirekt [S8]; two months at Mecklenburgische [S14] |
| *Beitragsfreistellung* | a deterministic election on the model point | A scalar account cannot carry two sub-populations, and no rate is established |
| `kapitalwahl_rate` | 30 % base | The real decision is a tax comparison and this model computes no tax, so the rate stands in for a calculation it does not perform (gap 20) |
| `omega_age`, `roll_fwd_tol`, the model points | 121; 1e-9 relative; all fourteen | The terminal age fixes `proj_len_y` and lets the closure identity reach exactly zero — and its `q = 1` is a table **closure convention**, so the model places that certainty in the year's anniversary month rather than twelfth-rooting it, which would kill the cohort eleven months early; the tolerance is a float comparison, not an actuarial assumption; the model points are configurations chosen to exercise the mechanics, not observed policies |

The only quantities that are **not** standardizations are the *Höchstzillmersatz* ceiling of § 4
DeckRV [R7] [REG-R16], the five-year spread of acquisition costs in § 169 Abs. 3 [R1] [REG-R28],
the 2005 mortality base year [R13], and the structural rules: the *Deckungskapital* recursion
[S8] [S11], `max(garantierter, aktueller)` [S9] [S14] [S18], the conversion capital including
surplus and *Bewertungsreserven* and floored at the guaranteed contract value [S9], the § 165
branches [R2], the § 169 floor and *Stornoabzug* conditions [R1], the death-benefit forms
[S4] [S8] [S9] [R24], and the *Rentengarantiezeit* [S1] [S4] [S9].

## Where the model diverges from a retrieved document

The 2026-08-30 retrieval pass established four things the model does not implement. **None of them
was changed in that pass**, because each moves the worked example and the golden tests, and that is a
deliberate decision rather than a documentation edit. They are listed here so a user recalibrating
the model knows where to start.

| What a document says | What the model does |
|---|---|
| ***Beitragsrückgewähr während der Rentenzahlungszeit*** is offered as an alternative to the *Rentengarantiezeit*: premiums paid, less rider premiums, less annuities already received at their inception-guaranteed level, the claim lapsing once instalments exceed premiums [S4] § 1 Abs. 5 | `claims_death(t) = 0` for every `t ≥ 12n`, on every model point, and a test asserts it. The library previously recorded this benefit as *unmentioned by any source*; it is now a **known omission** |
| The *Rentenfaktor* market range for 2025 is 24,33–27,18 guaranteed and 27,27–30,40 current, by deferment term to age 67 [R24]; the current-factor average was 25,97 in 2022 [R19] | `rentenfaktor_table.csv` ships `base` 32,00, `low` 25,50, `high` 35,00 at age 67. The payout phase scales linearly in the factor, so a user recalibrating to market lowers the annuity block by roughly a sixth |
| A carrier's *Überschussverteilung 2026* credits **3,00 %** in total before the *Rentenbeginn* and 3,35 % during it, against 2,25 % and 2,5 % for 2025 [S15] | `decl_rate_table.csv` ships a level `base` of 2,55 %, a market average [REG-R53]. On the 1,00 % vintage the difference is 45 bp on a `bonus_rate` of 155 bp — a 29 % change |
| The *Stornoabzug* is either absent [S8] [S9], a flat 250 EUR waived at age 62 or after twenty years [S4], or percentages of the *Deckungskapital* tapering linearly to nil over the last ten years of the *Aufschubzeit* [S11] | `stornoabzug_rate` is a flat 2,0 % with no duration term, applied on `zillmer_25` only |

One further difference is a refinement rather than a divergence: [S9] applies
`max(garantierter, aktueller)` **at every monthly instalment**, while the model applies it once at
the *Rentenbeginn*. On a deterministic path with a single conversion event the two coincide — and the
monthly grid now at least puts the two on the same footing, the instalment being a real row of the
frame rather than a twelfth of an annual lump.

## Tests

`tests/test_klassische_rentenversicherung_de.py` asserts the notes' worked example — all
seventeen accumulation rows, `k = 0 … 16`, and the six sampled payout rows `k = 17, 26, 27, 39, 54`
and `70`, read off `result_cf_annual()`, money to the cent and `pols_if` to six decimals — the
twelve months of policy year 1 on the monthly frame beside them, the frame's shape on the 0-based
month index (`list(index) == list(range(852))` on the anchor, `index[-1] == proj_len() - 1` on every
point tested), the totals at full precision against the rounded-cell sums, the four columns the
conversion moved against the annual-step model's own totals, the three independent rebuilds below
the table, the closure split, both documented variants (the *Einmalbeitrag* form and the 2,75 %
legacy vintage), all nine `check_*` identities with their residuals — monthly for five, per policy
**year** for four — and **one test per listed modeling pitfall**: the declared rate containing the guarantee, the within-year
order, `max(garantierter, aktueller)`, the *Rentengarantiezeit* weighting, *Beitragsfreistellung*
against lapse, charges against expenses, the § 169 Abs. 3 floor, the *Stornoabzug*'s shape, the
two mortality bases, the generational surface, the zero net amount at risk, the unapplied payout
charge, the absent post-*Rentenbeginn* death benefit, the *Kapitalwahlrecht* leaving no account
behind, the guarantee vintage, unisex pricing, the *Beitragssumme* surviving a
*Beitragsfreistellung*, and the untruncated payout phase.

The conversion added its own assertions rather than a separate section: that the annual layer is
**unchanged** — every account balance, the § 169 floor, the surrender value, the conversion capital
and the premium income equal to the annual-step model's — that `result_cf_annual()` regroups the
monthly frame rather than reprojecting it, that both decrement rates **compound** back to the year
rather than dividing by twelve, that the two certainties (the terminal `q = 1` and the § 165
cash-out) fall in the anniversary month, that the *Rentengarantiezeit* is `12m` instalments, and
that the annuity is one instalment paid in advance each month.

The whole-model-point-table sweep is **not** here: the conventions suite owns the single sweep,
because a model point's first evaluation is the most expensive thing in the run.

```bash
python -m pytest lifelib/libraries/delib/tests/test_klassische_rentenversicherung_de.py -q
python -m pytest lifelib/libraries/delib/tests/test_model_conventions_de.py -q -k RV_DE_S
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-klassische_rentenversicherung-r1
[R12]: #delib-klassische_rentenversicherung-r12
[R13]: #delib-klassische_rentenversicherung-r13
[R17]: #delib-klassische_rentenversicherung-r17
[R19]: #delib-klassische_rentenversicherung-r19
[R2]: #delib-klassische_rentenversicherung-r2
[R20]: #delib-klassische_rentenversicherung-r20
[R21]: #delib-klassische_rentenversicherung-r21
[R24]: #delib-klassische_rentenversicherung-r24
[R3]: #delib-klassische_rentenversicherung-r3
[R4]: #delib-klassische_rentenversicherung-r4
[R5]: #delib-klassische_rentenversicherung-r5
[R6]: #delib-klassische_rentenversicherung-r6
[R7]: #delib-klassische_rentenversicherung-r7
[REG-R1]: #delib-reg-r1
[REG-R14]: #delib-reg-r14
[REG-R16]: #delib-reg-r16
[REG-R28]: #delib-reg-r28
[REG-R4]: #delib-reg-r4
[REG-R45]: #delib-reg-r45
[REG-R53]: #delib-reg-r53
[std]: #delib-std
<!-- END generated citation links -->
