# Implementation Notes

**Status:** Draft, 2026-08-29; citations re-verified against the primary documents
2026-08-30. Built from
[`products/risikolebensversicherung/technical-notes.md`](technical-notes.md); the product
it implements is specified in [`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> *mechanics* are sourced — at drafting only through corroboration inherited from a sibling
> delib research file, and since the 2026-08-30 re-verification from the instruments and
> wordings themselves: the *Bruttobeitrag* is guaranteed for the term and the *Zahlbeitrag*
> is not [R5] [R6] [REG-R24] [REG-R27]; the MindZV obliges an insurer to allocate at least
> **90 % of the *Risikoergebnis***, which on a term product is essentially the whole
> technical result [R9] [REG-R18]; § 161 VVG makes the insurer *leistungsfrei* for an
> intentional self-inflicted death inside **three years**, substituting a *Rückkaufswert*
> that here is nil or nominal [R1] [REG-R26]; § 169 Abs. 1 VVG confines the surrender-value
> **duty on *Kündigung*** to a contract whose insured event is *gewiss*, and a term
> assurance's is not, so **the model carries no cash value at any duration — though two of
> the three retrieved wordings do provide for one, at a nil-or-nominal amount** [R2] [R3]
> [R8] [S1] [S3] [S4] [REG-R28]; sex may not enter the premium for contracts concluded from
> 21 December 2012 [R13] [REG-R34]; and the DeckRV ***Höchstzinssatz*** of **1,00 %** and
> *Höchstzillmersatz* of **25 ‰ of the *Summe aller Prämien*** bound the tariff — both are
> **ceilings the composite adopts as rates**, and a retrieved carrier prices at 0,25 %
> [R10] [REG-R14] [REG-R16] [S3].
>
> **Almost no level is sourced, and none is adopted.** This model was drafted with direct
> HTTP egress blocked and the session's `WebSearch` budget exhausted **before** this product
> was researched, so every level rested on the authoring model's own knowledge. The
> citations have since been re-verified against the primary documents — **22 of the 40
> entries in `sources.md` now read `Retrieved: yes` and 18 still read `no`**. On *levels* it
> reached exactly one carrier: [S2]'s published model case gives a *Tarifbeitrag*, a
> *Zahlbeitrag*, an α of **2,41 %** and a **0,25 %** *Rechnungszins*, which the
> standardization table below records **as checks and not as inputs**. The cost-disclosure
> duty is owed to the applicant and not to the public [R17], so there is still no rate card,
> and no spread ratio, smoker ratio, commission scale or lapse rate was established for any
> German carrier [S3]–[S13] [S14] [S16] [R18]. Every price, charge, margin and behavioural
> level here is therefore still **[std]** with a stated rationale, and the DAV tables —
> **DAV 2008 T**, with its *NR* and *R* variants — are the property of the Deutsche
> Aktuarvereinigung, are cited by name and are **never shipped** [R12] [REG-R48]. Replace
> the decrement and charge tables with company data before drawing any conclusion from the
> output.

## Run it

```bash
python products/risikolebensversicherung/run.py
python products/risikolebensversicherung/run.py 7     # the Einmalbeitrag form
python products/risikolebensversicherung/run.py 8     # the in-force cell, opening at t = 144
```

```python
import modelx as mx
model = mx.read_model("products/risikolebensversicherung/RLV_DE_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell — entry
age 35, male, non-smoker, 300 000 € *konstante Versicherungssumme*, 25 years' cover and 25
years' premium, annual mode, participating. `result_cf()` returns a `DataFrame` indexed by
the **0-based** policy month `t` with eleven columns; `result_cf_annual()` sums it into
policy years, which is the view the technical notes' worked example is stated on; and
`result_pols()` publishes the decrement, rate, benefit, premium and reserve side beside the
monthly frame.

**The time index.** `t` counts policy **months** from issue and starts at **0**: month `t`
runs from time `t` to time `t + 1`. `proj_len()` is the number of projected months,
`12 × policy_term`, and it is the frame's **exclusive end**: `result_cf()` runs over
`range(proj_start(), proj_len())`, so its last index is `proj_len() − 1` and it has
`12 × (policy_term − duration_y)` rows — three hundred rows `t = 0 … 299` on the anchor,
216 rows `t = 144 … 359` on the in-force point 8. `proj_start()` is `12 × duration_y`,
`duration_y` being an elapsed count of completed policy years that is already 0-based.

**The product is annual and stays annual.** `duration_mth(t) = t`, `duration(t) = t // 12`
and `policy_year(t) = duration(t) + 1` are derived and never indexed by, and everything the
contract puts on the anniversary stays there: `age(t) = issue_age + duration(t)`, the
*Versicherungssumme* schedule, the *Nachversicherungsgarantie* steps, the § 161 three-year
windows, the *Beitragszahlungsdauer*, the expense inflation, and the whole first-order
equivalence — whose `G`, `Gn`, `v_d` and *Deckungskapital* are **bit-identical** to the
annual-step model this replaced. What the finer grid resolves is timing: `mort_rate` and
`lapse_rate` are the policy year's **annual** rates and `mort_rate_mth` and `lapse_rate_mth`
the monthly rates derived from them at `1 − (1 − r)^(1/12)`, so twelve of each compound back
to the year's rate and `pols_if` at every anniversary is the annual model's own figure.

**What the CSVs are keyed on.** `benefit_schedule.csv`, `nvg_schedule.csv` and
`lapse_table.csv` are keyed on `policy_year`, the contractual **1-based** label, and their
values are unchanged by the monthly frame: the readers map through `policy_year(t)`. In
`model_point_table.csv`, `duration_y` is an elapsed count of **years** and `policy_term` and
`prem_term` are counts of years; no column there is a point on the frame's time axis, so no
model-point value moves either. `mort_table.csv` is keyed on attained age, which is not a
time index, and its rates stay **annual**. **No CSV value changed** in the move to the
monthly grid, and none changed in the earlier move to the 0-based frame.

The model and both its Spaces carry
docstrings: `model.Projection.doc` holds the full mapping between the notes' actuarial
symbols and the cells names, and `model.Data.doc` says what each input file is and, for
the mortality table, **what it is not** and what a replacement must preserve.

## The customer is not billed the premium the contract guarantees

This is the German delta, visible in the frame rather than buried in a parameter. A German
*Risikolebensversicherung* carries **two** premiums, and a model carrying one cannot
represent it [R6]. The ***Bruttobeitrag*** `G` is struck once, at issue, by first-order
equivalence on tariff survivorship — mortality only, no lapse — so it is acyclic with
respect to everything behavioural, and it is what the contract guarantees: the maximum the
policyholder can ever be required to pay, unchanged for the term [R6] [REG-R27]. The
***Zahlbeitrag*** then follows from the surplus mechanic rather than from an assumption —
the tariff's own mortality margin has actuarial value `(m/(1+m))·A` at issue, and the
declared *Beitragsverrechnungssatz* returns `surplus_share` of it over the paying term:

```
G   = ( A + γ·Γ ) / ( (1 − β)·ä − z·k )
    = ( 23 472,374330 + 0,00030 × 6 491 248,23 ) / ( 0,95 × 21,6374941 − 0,025 × 25 )
    = 1 275,411882 €

v_d = min( v_max, decl_scale · surplus_share · (m/(1+m)) · A / (G·ä) )
    = decl_scale · surplus_share · (m/(1+m)) · [ 1 − β − (γ·Γ + z·k·G)/(G·ä) ]
    = 1,00 × 0,90 × 0,5556 × 0,85054952 = 0,42527476
```

— the surplus share, times the margin fraction of the risk element, times the risk share
of the gross premium. So `Zahlbeitrag / Bruttobeitrag = 0,574725` on the anchor,
reproducing the research file's frozen **[std]** 0.57 **from the mechanic rather than by
assumption**. The model publishes `prem_gross` (guaranteed), `premiums` (billed, and the
one inside `net_cf`) and `prem_rebate` between them.

**What the model deliberately does not do here.** It does not treat `v` as a free input,
`v` being an output of the surplus mechanic in the real product; it does not return the
*Kostenüberschuss* alongside the *Risikoüberschuss*, the MindZV's *übriges Ergebnis* limb
carrying a different minimum share and no basis for splitting a German term tariff's
expense result having been established [R9] — the cost result emerges in `net_cf` and
stays there; and it does not implement § 163 VVG's *Treuhänder* adjustment, essentially
never used on this product [R6] [unverified]. The lever that matters is `decl_scale`:
setting it to **0** raises `premiums` to `prem_gross` at every `t` — 21 303,65 € against
12 243,75 €, a **74,0 %** increase in the bill with no change to any benefit, decrement or
guaranteed term, and so with no § 163 procedure, no *Treuhänder* and no remedy. That is
the largest policyholder risk here, and it is a one-Reference change. `surplus_form =
keine` is the § 153-excluded non-participating tariff [R5]: `v_d` is zero and the billed
premium *is* the guaranteed one — model point 12, shipped so the zero branch is exercised
rather than merely reachable.

## The tariff is unisex and the projection is not

Sex may not enter a German premium for contracts concluded from 21 December 2012 [R13]
[REG-R34], while the DAV 2008 T tables the tariff is built on remain **sex-distinct**
[R12] [REG-R48]. Every German term tariff is therefore a blend at a mixing ratio the
carrier chooses from its own expected new-business mix — proprietary, unpublished, and one
of the largest single sources of unexplained rate spread between German carriers.

`mort_rate_tar` prices on a 50/50 blend **[std]** and `mort_rate` projects on the policy's
own sex, so the cross-subsidy appears in the cash flows instead of in the price. Model
points 1 and 2 differ **only** in `sex`: they pay the same premium to the last bit,
`beitragsverrechnung_rate()` is identical, and their `claims_death` totals stand at
9 899,20 € against 5 009,05 €. The ratio `mort_rate_tar / mort_rate` is **not** `1 + m`:
it is `2.25 × (unisex blend / own-sex rate)`, which on the shipped proxy is **1.6875 for a
male and 3.375 for a female**, the blend being `0.75 × q̃(M)`. **What the model does not
do** is price on `sex`, or carry a carrier-specific mixing ratio, none being public;
`sex_mix_male` is a Reference so a user with a real new-business mix can move it in one
place, and moving it changes every premium and no claim.

## No cash value in the model — and yet a *Deckungskapital*

§ 169 Abs. 1 VVG confines the surrender-value **duty on *Kündigung*** to a policy insuring
"ein Risiko ..., bei dem der Eintritt der Verpflichtung des Versicherers **gewiss** ist",
which a term assurance's is not — read verbatim from the canonical XML [R2] [REG-R28]. So
this model carries **no account value, no `av_pp_at`, no surrender cells and no paid-up
state**, and a lapse is a pure decrement. `claims(t, "LAPSE")` and `claims(t, "MATURITY")`
are published as zero columns rather than dropped — a non-zero lapse row is what a reader
arriving from a US model with cash surrender values will import — and
`check_no_cash_value()` asserts them everywhere.

**Read that zero as an approximation of a small number, not as a rule of German law.** An
earlier draft said § 165's *Beitragsfreistellung* right and the insurer-side paid-up
conversion "both collapse into the same nil through the minimum-benefit test". The retrieved
wordings do not bear that out. § 165 carries no *gewiss* limitation, and on a constant sum
insured the paid-up right produces a real, small cover: the contract ends only below a
paid-up sum of 300 € at Cosmos or 2 500 € at Hannoversche [S3] § 15, [S4] § 13. On
*Kündigung*, the GDV model wording and Hannoversche **convert** the contract and pay a
*Rückkaufswert* under § 169 — less a *Stornoabzug*, 60 % of the *Deckungskapital* at
Hannoversche — where that minimum fails; only Cosmos pays nothing at all [S1] § 13 Abs. 8,
[S3] § 15 Abs. 10, [S4] § 13. What **is** uniform is the size, and both wordings say why in
the same words: the *Kostenverrechnung* leaves "keine oder nur geringe Mittel" [S1] § 14
Abs. 4, [S3] § 16 Abs. 4. The cash flow is unaffected either way — a *Beitragsfreistellung*
pays nothing at the time; it converts — so `claims_lapse = 0` stands, and **changing it
would move the worked example and the golden tests, which is a decision for a later pass,
not a provenance one**.

What is **not** true is that nothing accumulates, and this is the modelling error the
product invites. A level premium charged against a rising death rate overcharges early and
undercharges late, and the difference is a *Deckungskapital* that peaks near the middle of
the term and runs off to exactly zero at expiry — **7 553,29 €**, 2,52 % of the sum
insured, in **policy year 15**. The reserve takes a policy-year argument and stays an annual
construction on the monthly grid, so every figure here is unmoved by the conversion.
`check_res_roll_fwd()` asserts the Thiele recursion with
`res_pp_at(0) = 0` by the equivalence and `res_pp_at(n) = 0` by exhaustion; building on
"no *Sparanteil*, therefore no reserve" fails it.

**What the reserve is not.** It is a **pricing diagnostic**: net, not *gezillmert*, not
floored, entering no cash flow, and not a *Deckungsrückstellung* under HGB § 341f — which
requires the prospective method and says nothing about prudent margins, those being DeckRV
§ 5 Abs. 1's "Die Ableitung von Rechnungsgrundlagen auf der Basis eines besten Schätzwertes
genügt nicht" [R21] [R10]
[REG-R54]. `res_zill_pp_at` subtracts the unamortised Zillmer balance and opens at
`−z·k·G = −797,132426 €` — negative from the first day, which is what *Zillmerung* on a
contract with almost no reserve looks like [R10]. The *Nullstellung* question — whether a
negative individual reserve must be floored for balance-sheet purposes — was not
established, and no reserve of any kind enters `result_cf()`.

## The § 161 window is three years, and each increment carries its own

§ 161 VVG makes the insurer *leistungsfrei* where the *versicherte Person* intentionally
takes her own life "vor Ablauf von drei Jahren nach Abschluss des Versicherungsvertrags",
substituting the *Rückkaufswert* nach § 169 — which on this product is nil or nominal, so
the German three-year rule is **an exclusion in all but name** [R1] [R2] [REG-R26]. **The
per-increment restart is no longer a modelling choice**: all three retrieved wordings say
"Wenn unsere Leistungspflicht durch eine Änderung des Vertrages erweitert wird oder der
Vertrag wiederhergestellt wird, beginnt die Dreijahresfrist bezüglich des geänderten oder
wiederhergestellten Teils neu" [S1] § 5 Abs. 3, [S3] § 2 Abs. 4, [S4] § 19 Abs. 3. The model
applies it as a **benefit switch on death claims only**, tranche by tranche:

```
benefit_paid_pp(t) = S0 · f(t) · Σ_j Δu(y_j) · σ_j(t),
σ_j = 1 − suicide_share  if  duration(t) < y_j + 3
```

so `suicide_factor(t) = benefit_paid_pp(t)/benefit_pp(t)` is **0,97 through the first
thirty-six months and 1 thereafter** on the anchor, and a **weighted average strictly
between 0,97 and 1** where one tranche is inside its window and another is not — 0,995
through policy years 6 to 8 and 0,9957142857 through policy years 12 to 14 on model point 9,
whose *Nachversicherungsgarantie* steps the sum to 1.2 at policy year 6 (month 60) and 1.4
at policy year 12 (month 132). On the in-force point 8 it is 1 at every projected `t`.

Both clocks are annual and every window boundary therefore falls on an anniversary, so the
monthly grid resolves the switch **exactly** rather than approximately: `duration(t) < 3` is
the same statement as `t < 36`.

**What the model does not do.** It does not model the mental-illness exception, the ground
on which German *Selbsttötung* claims are actually litigated [R23] and not something a
best-estimate switch can carry; it does not apply the switch to a lapse or an expiry, both
of which pay nothing anyway; and it does not model *Nachversicherungsgarantie* take-up as
a decision — **take-up is exogenous**, a schedule in `nvg_schedule.csv`, `keine` in the base
run. The event list, window and caps that were previously unestablished now are: a carrier
wording gives nine events, a twelve-month window, 20 % of the original sum insured or
50 000 € per event, five occasions in all and an end above age 50 [S3] § 13. What the model
*does* do with an increment is not exogenous: the clock restarts for it — **which all three
retrieved wordings provide expressly** [S1] [S3] [S4], as does the French statute [R1].

## Three *Versicherungssumme* shapes, one mechanic

German tariffs offer *konstant*, *linear fallend* and *annuitätisch fallend* on the same
underwriting and *Rechnungsgrundlagen*. All three are one mechanic — a schedule `f(t)` on
the initial sum — carried as a first-class external input, because **a model that
hard-codes a constant sum insured cannot represent two of the three shapes the German
market sells**. The falling shapes price lower *mechanically*: the equivalence integrates `B(t)`, and
nothing is applied as a "discount". `benefit_schedule.csv` is term-specific by
construction — an amortisation shape is agreed at issue for a stated term — and the
annuity shape falls **slowly then fast**: on point 5 the first year's fall is 8 407,70 €
against 19 236,22 € in the last, the property a linear schedule gets backwards. The
nominal rate is a schedule parameter fixed at issue and does not follow a borrower's loan;
no German rate was established, so 3,00 % is **[std]** (gap 15). *Dynamik* — a rising
shape — is a different mechanic and is **not modelled**.

## Two lives, one benefit, combined before loading

The *verbundene Leben* form is one contract on two lives paying **once**, on the first
death — a `lives = 2` variant on the same chassis, not a second engine, and **off in the
base run** (model point 10 exercises it). The two lives are combined at **table level,
before any loading**, on an independence assumption **[std]**:
`Q̃ = q̃_A + q̃_B − q̃_A·q̃_B`, and the same combination is applied to the two unisex blends
before `(1 + m)·rf`. Combining *after* loading inflates the cross term; on point 10 the
combined rate is 0,0015156941 against a naive sum of 0,0015162642. The assumption
**understates** the true first-death rate for a couple sharing a household, a vehicle and
a lifestyle, and no German figure bounds the understatement.

The ***Über-Kreuz-Versicherung*** is **not** in this model, and its absence is deliberate:
it is a *contracting structure* with identical cover, premiums and cash flows, and only the
*Erbschaftsteuer* outcome changes [R15] [REG-R46]. No column, cells or CSV refers to it,
and taxation is documented in `product-spec.md` and computed nowhere.

## The last policy year has no lapse

Lapses fall at the **end** of the month, after the death decrement, and the end of the last
month `t = proj_len() − 1` is the moment cover expires. A lapse and an expiry are then the
same event paying the same nothing, so `lapse_rate` is **0 through the whole of the final
policy year** — `duration(t) ≥ proj_len_y() − 1`, months 288 to 299 on the anchor — and the
surviving cohort leaves through `pols_maturity`. The zero covers the year rather than merely
its last month, because that is what the annual-step model this replaced said of it. The
table's own row for policy year `n` still reads 3 %: the zero is a property of the last
policy year, not of the assumption.

No cash flow moves either way, but the closure identity is load-bearing: on the anchor it
divides **0,03261764** deaths, **0,53597922** lapses and **0,43140314** expiries, summing
to `pols_if_init() = 1` exactly with `pols_if(300) = 0` — which is what lets `result_cf()`
stop at `proj_len() − 1 = 299` with nothing left over. The expiring cohort is the annual-step
model's own figure to the last digit; the split between deaths and lapses moved by 0,00044,
which is the one thing interleaving the two decrements monthly genuinely changes.

## Inputs are external files

The six input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `RLV_DE_S/` holds nothing but formulas:

```
products/risikolebensversicherung/
  model_point_table.csv  mort_table.csv  benefit_schedule.csv     <- inputs live here
  nvg_schedule.csv       lapse_table.csv freq_loading_table.csv
  run.py  model.md  product-spec.md  technical-notes.md  sources.md
  RLV_DE_S/                    <- formulas only
    __init__.py  _system.json  Data/__init__.py  Projection/__init__.py
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its input file beside the
model and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which
stores its inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/`
directory and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache, and readers placed there would re-read every file for
every policy. They live instead in an unparameterized **`Data`** Space, which `Projection`
references as `data`, so each file is read once per model however many policies are
projected. The conventions suite counts the reads and asserts the *set* against
`tests/de_registry.py`.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `benefit_schedule_file` | `benefit_schedule()` | `benefit_schedule.csv` |
| `nvg_schedule_file` | `nvg_schedule()` | `nvg_schedule.csv` |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` |
| `freq_loading_file` | `freq_loading_table()` | `freq_loading_table.csv` |

**The trade-off:** the model is not portable on its own — copy `RLV_DE_S/` without the
CSVs and it reads fine, then fails on first evaluation. What you gain is that a diff shows
logic changes only, and an input can be swapped in place: point `Data.mort_table_file` at
another same-schema file and the projection follows, with no formula change. Tests cover
both halves of that bargain. **Every file but the model point table carries a per-row
`provenance` column** — this library's second ruling, machine-checked, in the same `[S#]` /
`[R#]` / `[REG-R#]` / `[std]` vocabulary the documents use. `model_point_table.csv` is the
single exemption, a model point being a *configuration* rather than an assumption.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Fourteen model points. **Point 1 is the worked-example anchor cell.** The rest cover both premium forms, all four *Zahlweisen*, all three sum shapes, an in-force point opening at `t = 144`, a *Nachversicherungsgarantie* with two increments, *verbundene Leben*, a *Risikozuschlag* on an impaired smoker, the § 153-excluded tariff, an *abgekürzte Beitragszahlungsdauer*, and two boundary cells | **[std]**; exempt from the provenance rule |
| `mort_table.csv` | Second-order annual death rates by `table_id`, `sex`, `smoker` and attained age 18–80 | **[std]** Gompertz proxy `base(sex) × smoker_mult × 1.095^(age−30)`, `base(M) = 0.00040`, `base(F) = 0.00020`, `smoker_mult(R) = 2.20`. **DAV 2008 T / T NR / T R are cited by name and never shipped** [R12] [REG-R48]. The three anchors a replacement must preserve: the 50/50 non-smoker blend `0.00030 × 1.095^(x−30)`, the female-to-male ratio 0.50, and the smoker multiplier 2.20 |
| `benefit_schedule.csv` | `benefit_factor` by schedule id and **1-based** `policy_year`, read at `t + 1`: `konstant`, `linear_fallend` (`(21 − policy_year)/20`, i.e. `(20 − t)/20`), `annuitaet_fallend_3pct` | **[std]** — the three German shapes are structural [S15]; **no schedule parameter was established** (gap 15) |
| `nvg_schedule.csv` | Cumulative `sum_uplift`: `keine` ≡ 1.0, `nvg_zwei_erhoehungen` stepping to 1.2 at year 6 and 1.4 at year 12 | **[std]** — the schedule is a mechanics demonstration and take-up is exogenous. **Gap 7 is now closed**: [S3] § 13 gives a nine-item event list, a **twelve-month** exercise window, a per-event cap of **20 % of the original sum insured, at most 50 000 €**, at most **five** occasions in all, and an end above **age 50**. Two 20 % increments are inside those caps; that both are taken is a model assumption no document supports. **The CSV is unchanged** [S3] [S11] [S17] |
| `lapse_table.csv` | **Annual** lapse by **1-based** `policy_year`, read at `policy_year(t)`, 6 / 4 / 4 / 3 %; spread to the month by `lapse_rate_mth` | **[std]**, argued from structure, not data: nothing is forfeited by lapsing, exit is frictionless because the *Versicherungsperiode* follows the *Zahlweise* [R8], and the need amortises. The GDV whole-market *Stornoquote* [R18] is **deliberately not used** (gap 13) |
| `freq_loading_table.csv` | *Ratenzahlungszuschlag* and instalment count by *Zahlweise*: 1.000 / 1.02 / 1.03 / 1.05 | **[std]** — a German market convention with **no carrier attribution** (gap 21). Whether carriers strike it on the *Bruttobeitrag* or the *Zahlbeitrag* was not established; this model loads the **billed** amount |

## The published identities

Five `check_*` cells, each a `bool` over all `t` with a per-`t` residual companion
`check_*_resid(t)`, and all five called on **every** model point by the conventions suite.
The first is delib's own ruling and is stated here in one line:

**`check_net_cf()`:  `result_cf()` row `t` satisfies `net_cf = premiums − claims_death − claims_lapse − claims_maturity − expenses − commissions`.**

It is rebuilt **from the frame's own published columns**, and by a different route from
`net_cf`'s own, which subtracts the kind-less `claims(t)` subtotal. So it crosses the
cells-to-frame boundary — a column dropped, renamed or mis-signed on the way into
`result_cf()` fails here — and the `claims(t, kind)` dispatch, where a benefit kind can
exist in the model and not in the subtotal. Which columns are *not* in it is the other
half of publishing it: `prem_gross` is the
guaranteed stream and does not enter, and `prem_rebate` is the difference between the two
premium columns and must not be subtracted again. `expenses` here **excludes**
`commissions` — the opposite convention from `frlib.TD_FR_S`, whose notes fold commission
into the expense total. The two libraries' columns look alike and do not mean the same
thing; this identity settles the reading.

| Check | Identity |
|---|---|
| `check_net_cf()` | On `result_cf()` row `t`: `net_cf = premiums − claims_death − claims_lapse − claims_maturity − expenses − commissions` |
| `check_pols_roll_fwd()` | `pols_if(t+1) = pols_if(t) − pols_death(t) − pols_lapse(t) − pols_maturity(t)`, and the three exits sum to `pols_if_init()` |
| `check_prem_split()` | `prem_gross_pp(t) = prem_paid_pp(t) + prem_rebate_pp(t)`, with `0 ≤ prem_rebate_pp < prem_gross_pp` where a premium is due and all three zero where none is |
| `check_res_roll_fwd()` | The Thiele step `(res + Gn·1{t<k})(1+i) = q₁·B + (1−q₁)·res(t+1)`, plus `res_pp_at(0) = 0` and `res_pp_at(n) = 0` |
| `check_no_cash_value()` | `claims(t,"LAPSE") = 0` and `claims(t,"MATURITY") = 0` at every `t` |

Two further identities are **scalar rather than per-period** — the first-order equivalence
`G·ä = A + z·k·G + β·G·ä + γ·Γ` and the surplus equivalence
`v_d·G·ä = decl_scale·surplus_share·(m/(1+m))·A` — and are asserted in the product's test
module instead. Forcing a scalar identity into a per-`t` residual would mean inventing a
per-period decomposition the product does not have.

## Modules that are off in the base run

Two behavioural constructions are implemented and switched off, so the base run reproduces
the worked example while the machinery stays visible and testable.

| Module | Switch | Off value | What it does |
|---|---|---|---|
| Premium-shock lapse | `shock_lapse_lambda` | `0.0` | `M_shock(t) = 1 + λ_s·max(0, prem_paid_pp(t)/prem_paid_pp(t−12) − 1)`, reference `λ_s = 2.0` **[std]**. The ratio is between **consecutive renewals**, so it reads the annual *Zahlbeitrag* twelve months back and not the instalment one month back. Inert in the base run because the billed premium is level there; it bites exactly when `decl_scale` is stressed, which is when it should. A stress that raises the *Zahlbeitrag* toward the *Bruttobeitrag* and leaves lapse unchanged is understating itself |
| Selective lapse | `sel_lapse_lambda` | `0.0`, with `sel_lapse_ref = 0.25` | `q₂_eff = q₂·(1 + λ·max(0, w_cum − w_ref))`, reference `λ = 0.30` **[std]**. Healthy lives can re-underwrite into a cheaper contract and impaired lives cannot, so persisters' mortality drifts up. delib does not model it in the base run — one basis for stayers and leavers — a **stated simplification**, not an oversight |

Both are driven off the premium and the lapse table alone, never off `pols_if`, so the
projection stays acyclic: a pricing quantity struck by equivalence must not depend on a
behavioural assumption that depends on the path that depends on the premium. Three further
things are described in the sources and **not** implemented, each because modelling it
would add an assumption with no source rather than a mechanic: the *Summenzuwachs*,
*verzinsliche Ansammlung* and *Todesfallbonus* surplus forms; the *Dynamik* and every rider
— UZV, BUZ, *Beitragsbefreiung*, *vorgezogene Todesfallleistung*, *Verlängerungs-* and
*Umtauschoption*, *vorläufiger Versicherungsschutz*; and the *Kriegsklausel* with its ABC
companion, a catastrophe-scenario provision rather than a best-estimate one.

## Sign convention

`net_cf` is **income positive** — billed premiums in, claims, expenses and commission out
— the notes' own orientation and the library-wide sign. `liability_cf` publishes the same
stream outgo-positive, `liability_cf(t) = −net_cf(t)` exactly, and both are columns of
`result_cf()`, so the identity is verifiable in the frame. A Solvency II best estimate is
`Σ v(t)·liability_cf(t)` plus a risk margin [REG-R1] [REG-R2] [REG-R6]; **nothing here
discounts a published cash flow** — the one place a discount rate appears is the pricing
equivalence and the first-order reserve, neither of which is a cash flow.

The shape to expect on the anchor, read on `result_cf_annual()`, is a first-year strain of
**−351,88 €** — the acquisition cost and initial commission together exceed the first year's
billed premium — thin positive years while the level premium runs ahead of the natural risk
premium, and a crossover in **policy year 14**. Within policy year 1 the monthly frame shows
what the annual grid could not: **−108,90 €** in month 0, where the whole year's premium is
collected against 826,64 € of acquisition cost and commission, then eleven months of about
−22 € each. The total is **−644,78 €** on model point 1 and **+4 252,82 €** on
model point 2, the same cell with `sex = F`. Neither is a profit measure: the stream is
undiscounted, the tariff was struck at 1,00 % on no-lapse survivorship, and no reserve is
held against the later years. The *difference* is the unisex cross-subsidy the law
requires, and the model is meant to show that rather than hide it.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` wherever that model has an analogue —
`model_point`, `proj_len`, `age`, `sum_assured`, `policy_term`, `pols_if`, `pols_death`,
`pols_lapse`, `pols_maturity`, `mort_rate`, `lapse_rate`, `premiums`, `claims`,
`expenses`, `commissions`, `inflation_factor`, `net_cf`, `result_cf` — with `*_pp` for
per-policy amounts, `claims(t, kind)` with an uppercase `kind`, and `pols_if_at(t, timing)`
for the within-year reads, which is `savings/CashValue_SE`'s form. The external-CSV layout
and `Data.input_dir()` come from `annuallife/TradLife_A`. The full symbol mapping lives in
the `Projection` Space docstring. Four cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `Gn`, `P(t)` | `prem_net_level_pp` / `prem_paid_pp` | The three "netto"s. `prem_net_level_pp` is the **actuarial** *Nettoprämie* `A/ä`, a pricing quantity that never becomes a cash flow; `prem_paid_pp` is the **consumer** *Zahlbeitrag*. The *Nettotarif* is a third, unrelated sense and is not modelled. The bare word *Nettobeitrag* is never a name here, and `prem_net_pp` is on the library's retired-names register |
| `q₁(t)`, `q₂(t)` | `mort_rate_tar` / `mort_rate` | `q₁` **prices** and enters the premium and the reserve and nothing else; `q₂` **projects** and drives every decrement and claim. Their ratio is `2.25 × (blend / own-sex rate)`, not `1 + m` |
| `B(t)` | `benefit_pp` / `benefit_paid_pp` | `benefit_pp` is the contractual *Versicherungssumme*; what a death claim actually pays differs inside a § 161 window, tranche by tranche, and `suicide_factor` is the ratio of the two |
| `w(t)` vs `w_cum(t)` | `lapse_rate` / `lapse_cum` | `lapse_cum` is a proportion of the original cohort, not a running total of `lapse_rate`, and the loading it feeds moves *claims* |

**The sister model that shares this chassis is `frlib`'s `TD_FR_S`** — the French
*temporaire décès*, the same product in another market — and the shared vocabulary is
deliberate: `pols_if_at`, `lapse_cum`, `suicide_factor`, `benefit_pp`, `mort_rate_base`,
`prem_freq_load`, `check_no_cash_value` and `liability_cf` mean the same thing on both.
Three differences are named so a reader does not carry one across: the French cotisation
is **revisable at attained age** and the German *Bruttobeitrag* is **level**; the French
product carries a **PTIA acceleration** and the German one has no living benefit at all;
and `expenses` **includes** commission there and **excludes** it here. Within delib,
`KLV_DE_S` shares the *Überschussbeteiligung* chassis in a different *Überschussverwendung*
form — surplus credited to a *Deckungskapital* rather than netted against the premium —
and the biometric siblings `BU_DE_S` and `Pflege_DE_S` are monthly multi-state models
sharing no recursion with this one. `issue_date`, `instalments` and `policy_id` are
carried and drive no formula: the notes' attribute table lists all three, and a silently
missing column is worse than an inert one.

## Standardizations used

Everything in this table is **[std]**. Where an instrument fixes a *bound* rather than a
level — the DeckRV *Höchstzinssatz*, the *Höchstzillmersatz*, the MindZV minimum — the bound
is cited and the choice to sit at it is the standardization. **Where a retrieved document now
gives an observed value for a [std] parameter, the row records it — and the parameter is
unchanged.** One direct writer's published model case is not a market, and recalibrating the
composite to it would move the worked example and its golden tests. The observations are
checks, not inputs.

| Parameter | Value | Rationale |
|---|---|---|
| `mort_table.csv` | `base(sex) × smoker_mult × 1.095^(age−30)` | DAV 2008 T is proprietary and is cited, never shipped [R12]. The 9,5 % slope is the research file's own construction with **no German source**, and on model point 14's forty-year run it is the single most exposed number in the model |
| `base(M)`, `base(F)` | 0.00040, 0.00020 | Anchored so the 50/50 blend is the research file's frozen `0.00030 × 1.095^(x−30)`; the female-to-male ratio 0.50 is the order of magnitude reported for insured lives at these ages [unverified] |
| Smoker multiplier | 2.20 | Mid-point of the two-to-three range reported for insured-lives smoker mortality at working ages [unverified]; reproduces a *premium* ratio of **2.007** between points 3 and 1 |
| `sicherheitszuschlag_m` | 1.25 | The DAV *Richtlinie* regulates the **procedure** for setting the *Sicherheitszuschläge*, not the level [R12] (gap 6); DeckRV § 5 Abs. 1 requires that a loading exist — "Die Ableitung von Rechnungsgrundlagen auf der Basis eines besten Schätzwertes genügt nicht" [R10]. Calibrated so the derived `Zahl/Brutto` lands at 0.57; argued range 1.0–1.5. **Observed check**: a published model case gives `Zahl/Brutto = 0.450` [S2], at the bottom of the argued range — i.e. a wider spread than this composite produces |
| `sex_mix_male` | 0.50 | The mechanism is required by law [R13]; **no carrier discloses its own mix** |
| `mort_be_factor` | 1.00 | So the shipped proxy *is* the best estimate, and there is one unsourced mortality level rather than two stacked |
| `surplus_share` | 0.90 | The MindZV **minimum** allocation from the *Risikoergebnis* is 90 % [R9] [REG-R18]; modelling the minimum is the conservative choice for the *Zahlbeitrag*, and it is the only level any instrument fixes |
| `decl_scale` | 1.00 | The insurer declares exactly the minimum. No German declaration for this product was located (gap 1); this is the stress lever |
| `v_max` | 0.95 | A rebate may not exceed the premium. Binds nowhere in the shipped points; it exists so `check_prem_split()` has a stated domain |
| `zillmer_rate` | 0.025 | The *Höchstzillmersatz* **ceiling** [R10] [REG-R16]; the composite assumes a term tariff runs at the cap. **Two corrections from retrieved documents.** (i) The assumption is close to right for one direct writer: its published model case shows acquisition cost at **2,41 % of the *Tarifbeitragssumme*** [S2]. (ii) But the ceiling is **mis-typed as the whole α**: DeckRV § 4 caps only the part recovered through *Zillmerung*, and both the GDV model wording and the carrier AVB spread "die restlichen Abschluss- und Vertriebskosten ... über die gesamte Beitragszahlungsdauer" [S1] § 14 Abs. 3, [S3] § 16 Abs. 3. *Zillmerung* is also optional on this line [S1] fn. 28 (gap 8) |
| `comm_rate_init` | 0.020 of the *Beitragssumme* | Splits the α of the ceiling into commission and other acquisition cost. No German commission scale is public |
| `beta_tariff`, `gamma_rate` | 0.05 of each *Bruttobeitrag*; 0.00030 of `benefit_pp` a year | **Correction:** German term-life charge levels are *not* "structurally undisclosed". § 2 Abs. 1 Nr. 1 VVG-InfoV requires the *Abschlusskosten* as one total and the other costs as a share of the annual premium, § 2 Abs. 2 requires them **in Euro**, and § 4 Abs. 2 puts them on the *Informationsblatt*; both wordings point the customer there [S1] § 14 Abs. 1, [S3] § 16 Abs. 1 [R17]. What is missing is a **published rate card**. There is no *Effektivkostenquote* — § 2 Abs. 1 Nr. 9 confines that duty to a *gewiss* risk — and no *Basisinformationsblatt*, the product not being a PRIIP. **Observed check**: one specimen gives other annual costs of 48,52 € on a 218,52 € annual *Tarifbeitrag*, i.e. **22,2 %**, of which 35,20 € (**16,1 %**) administration [S2] — far above this composite's 5 % β, because the specimen's figure is a euro amount over a small premium, not a percentage loading. **Not recalibrated** (gap 8) |
| `maint_prem_pct`, `comm_rate_renew` | 0.03 and 0.010 of each *Zahlbeitrag* | Deliberately different from `beta_tariff`: the gap is the *Kostenüberschuss*, which is **not returned** and emerges in `net_cf` |
| `expense_infl` | 0.02, on sum-related admin only | The tariff's γ is level while the modelled one inflates, so the cost result narrows over a long term and eventually reverses — a real feature of a 25-year contract |
| `claim_expense` | 250 € per death claim | No German figure is public; worth 0,16 € in the anchor's first year |
| `suicide_share` | 0.03 | No German cause-of-death share was retrieved; stands for "about three per cent of deaths at these ages are suicides", argued range 0,01–0,05 [unverified]. The **three-year window itself is sourced** [R1] |
| `suicide_years` | 3 | The statutory minimum, extendable by *Einzelvereinbarung* [R1] [REG-R26]. A Reference so an extended window can be modelled. **All three retrieved wordings adopt the statutory three and none extends it** [S1] [S3] [S4] |
| Lapse table | 6 % / 4 % / 4 % / 3 % **a year**, zero through the final policy year | Argued from three structural features (mechanic 17); **no German figure supports any of it**, argued range 2–8 % in the early durations (gap 13). The final-year zero is a property of the last policy year and lives in the formula, not the table. The annual rate is spread to the month at `1 − (1 − w)^(1/12)` **[std]**: no German instrument states a conversion convention for any decrement, and what is not optional is that twelve of the monthly rates compound back to the year's |
| `prem_freq_load` | 1.000 / 1.02 / 1.03 / 1.05 | A market convention with no carrier attribution (gap 21), applied to the **billed** amount so the split identity holds at every frequency |
| Benefit schedules | `(21 − policy_year)/20`, i.e. `(20 − duration(t))/20`, stepping on the anniversary; a 3,00 % thirty-year annuity balance | The three shapes are structural; **no schedule parameter was established** (gap 15) |
| NVG schedule | 1.2 at year 6, 1.4 at year 12 | Take-up is exogenous. **Gap 7 is closed and the schedule is not consistent with the one wording that fills it**: [S3] § 13 caps each event at **20 % of the original sum insured, at most 50 000 €**, allows at most **five** occasions and ends the right above age 50, all within a twelve-month window of a listed event. Two increases of +20 % each is within that; but a cumulative 1.4 by year 12 assumes two qualifying events and full take-up, which no document supports. **The schedule is unchanged** — it is a mechanics demonstration, off in the base run — and the carrier's caps are now on the record beside it |
| `lives = 2` combination | `q_A + q_B − q_A·q_B`, before loading | An independence assumption that **understates** the true first-death rate for a couple; no German figure bounds it (gap 15) |
| `rating_factor` | 1.00 standard, 1.75 on point 11 | A *Risikozuschlag* is a **mortality** loading on both orders, not a price loading — which is why the `Zahl/Brutto` ratio moves by less than half a point across it. **No German or French *Risikozuschlag* scale is public** |
| `premium_form = einmal` | Model point 7 | A **[std]** construction exercising the premium engine at `k = 1`. **No German standalone RLV in the corpus is written on it**; the out-of-scope *Restschuldversicherung* is, and it is a different product sold a different way |
| Timing conventions | A premium instalment on the *Zahlweise*'s own cycle and the month's expenses at the beginning of the month, claims and lapses at the end, acquisition cost at issue only where `duration_y = 0` | **The approximation this row used to record is gone.** On the annual grid the model booked exits at anniversaries and said so, and the note recorded that the approximation was larger than first assumed: § 168 Abs. 1 with § 12 VVG gives termination at the end of the *Versicherungsperiode*, but both retrieved carriers allow it "jederzeit zum Ende des laufenden Monats" whatever the *Zahlweise* [S3] § 15 Abs. 9, [S4] § 13 Abs. 1. The monthly grid expresses exactly that. What remains **[std]** is the conversion of the annual rates to the month and the placing of claims at the end of the month |
| `shock_lapse_lambda`, `sel_lapse_lambda` | 0.0 (references 2.0 and 0.30) | Both modules off, so the base run reproduces the worked example |
| `roll_fwd_tol`, `val_tol` | 1e-10, 1e-9 | Tolerances scaled by `pols_if_init()` and `sum_assured()` respectively |
| The fourteen model points | — | The anchor is the research file's representative composite; the rest are chosen to exercise the mechanics, not to describe a market |

The only quantities **not** standardizations are the structural rules: the guaranteed
*Bruttobeitrag* and non-guaranteed *Zahlbeitrag* [R6] [S3] [S5], the MindZV's 90 % minimum
from the *Risikoergebnis*, now citable as **§ 7 MindZV** [R9], the three-year § 161 window
[R1] and its restart for each increment [S1] [S3] [S4], the unisex rule [R13], the DeckRV
ceilings of 1,00 % and 25 ‰ [R10], and the absence of a premium-tax line, VersStG 2021 § 4
Abs. 1 Nr. 5 Buchst. a [R16].

**One item has moved off that list.** "The absence of any surrender, paid-up or maturity
value" was carried here as a structural rule. It is not one. No § 169 Abs. 1 **duty**
attaches on *Kündigung* — that much is verified [R2] — but § 165's paid-up right is live on
a constant sum insured, and two of the three retrieved wordings pay a *Rückkaufswert* where
the paid-up sum fails a contractual minimum [S1] [S4]. The amount is nil or nominal in every
one of them, so `claims_lapse = 0` and `claims_maturity = 0` remain right as **best-estimate
approximations** — but they belong in the table above, as standardizations, not here.

## Tests

`tests/test_risikolebensversicherung_de.py` asserts all twenty-five rows of the notes'
annual worked example — off `result_cf_annual()`, keyed on the 1-based `policy_year` — to
the cent and `pols_if` to six decimals, the twelve months of policy year 1 on the monthly
frame beside them, that the annual view **regroups** the monthly frame rather than
reprojecting it, the frame's own shape (`list(result_cf().index) == list(range(300))` on
the anchor and `range(144, 360)` on the in-force point 8), the totals at full precision, the
*Bruttobeitrag* 1 275,411882 € and the *Beitragsverrechnungssatz* 0,42527476 reached two
independent ways, the notes' three rebuilds and three closure identities, the
`decl_scale = 0` and *Einmalbeitrag* variant tables, the five `check_*` identities with
their residuals, and **one test per listed modeling pitfall** — the three "netto"s in the
order the model produces them, two premium streams rather than one, the *Zahlbeitrag* not
guaranteed, no *Rückkaufswert*, a *Deckungskapital* that exists, `sex` never reaching the
price, the *Sicherheitszuschlag* never reaching the projection, the § 161 switch confined
to three years and to death claims, the clock restarting per increment, the
*Ratenzahlungszuschlag* applied once, premium cessation not double-counted, the premium
stopping at the *Beitragszahlungsdauer*, the three sum shapes, two lives combined before
loading, the *Kostenüberschuss* not returned, the *Stornoquote* not used, `rating_factor`
never scaling the benefit, and the *Über-Kreuz-Versicherung* not a product.

The house style — two Spaces, the external-CSV layout, the read-once `Data`, the shared
vocabulary, the retired names, the 0-based frame ending at `proj_len() − 1`, the round trip
and both of delib's own rulings — is asserted for every model by
`tests/test_model_conventions_de.py`, which also owns the library's single model-point
sweep.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-risikolebensversicherung-r1
[R10]: #delib-risikolebensversicherung-r10
[R12]: #delib-risikolebensversicherung-r12
[R13]: #delib-risikolebensversicherung-r13
[R15]: #delib-risikolebensversicherung-r15
[R16]: #delib-risikolebensversicherung-r16
[R17]: #delib-risikolebensversicherung-r17
[R18]: #delib-risikolebensversicherung-r18
[R2]: #delib-risikolebensversicherung-r2
[R21]: #delib-risikolebensversicherung-r21
[R23]: #delib-risikolebensversicherung-r23
[R3]: #delib-risikolebensversicherung-r3
[R5]: #delib-risikolebensversicherung-r5
[R6]: #delib-risikolebensversicherung-r6
[R8]: #delib-risikolebensversicherung-r8
[R9]: #delib-risikolebensversicherung-r9
[REG-R1]: #delib-reg-r1
[REG-R14]: #delib-reg-r14
[REG-R16]: #delib-reg-r16
[REG-R18]: #delib-reg-r18
[REG-R2]: #delib-reg-r2
[REG-R24]: #delib-reg-r24
[REG-R26]: #delib-reg-r26
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R34]: #delib-reg-r34
[REG-R46]: #delib-reg-r46
[REG-R48]: #delib-reg-r48
[REG-R54]: #delib-reg-r54
[REG-R6]: #delib-reg-r6
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
