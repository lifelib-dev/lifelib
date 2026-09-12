# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26; see `sources.md`).

**Scope note.** These notes specify a reference liability cash-flow projection model,
**UC_FR_S**, for the standardized composite `contrat d'assurance vie multisupport` defined
in `product-spec.md` (same directory), on a **monthly** grid. This is not any single
insurer's product. [S#]/[R#] tags refer to the source list in
`_research/assurance-vie-uc.md` (carried into `sources.md` here); [REG-R#] tags refer to the
cross-product reference library `references/regulatory-and-actuarial-references.md` (its own
frozen R-numbering). **[std]** marks standardizations introduced for the reference
implementation; [unverified] marks claims not confirmed against a retrieved document.
Parameter values are identical to those in `product-spec.md`.

**The euro leg is a pointer.** UC_FR_S models the `unités de compte` leg. The `fonds en
euros` enters as a single allocation share carrying an annual credited rate net of its own
management charge, because that is all the UC model needs it for: the euro balance is part
of the account value that sizes the `capital sous risque`, and it is the first source from
which the `garantie plancher` premium is levied [S1] [S3] [S4]. `Taux minimum garanti`,
`participation aux bénéfices`, the `provision pour participation aux bénéfices`, the `effet
cliquet` and the euro leg's own margin are specified and implemented in
`products/assurance_vie_euro/technical-notes.md` (model `Euro_FR_S`) and are **not restated,
not re-derived and not re-implemented here**. `net_cf` from UC_FR_S is therefore the UC-leg
and rider result, not the contract's total margin.

---

## Model scope and conventions

- **Purpose.** Project gross liability cash flows for a single-policy model point,
  decomposed into the **unit leg** (the `unités de compte` — a unit count valued at an
  exogenous liquidation value, matched by the linked assets) and the **non-unit cash flows**
  accruing to the insurer: charges collected, less expenses and the `garantie plancher`
  death strain. The decomposition is the same one `products/unit_linked_bond/` uses for a UK
  unit-linked bond; what is French about it is that art. A. 132-5 makes the unit **count**
  the thing guaranteed [R2], so the unit leg is a deterministic sequence and every charge is
  a unit cancellation. Reserves are not computed (see Valuation and reserve pointers).
- **Projection frequency.** Monthly. Sourced, not chosen: two of the seven retrieved
  contracts levy the UC management charge monthly [S7] [S13 art. 32.4], and the `garantie
  plancher` premium is levied monthly in arrears in three of them [S1] [S3] [S4].
- **Time index [std].** `t` is the policy month and is **0-based**: `t = 0` is the issue
  month, month `t` runs from time `t` to time `t + 1`, and the frame is
  `t = 0, 1, …, proj_len − 1`, so `result_cf()` has `proj_len` rows. The contractual policy
  year is the 1-based label `y = t // 12 + 1`; it is derived and never indexed by. The
  balances **at issue** — time 0, before month 0 opens — are not a row of the frame: they
  are written with an `init` subscript (`p_init`, `n_init`, `V_init`, `S_init`, `B_init`),
  and `X_init` is the opening balance of month 0 exactly as `X(t−1)` is the opening balance
  of month `t` for `t ≥ 1`.
- **Timing conventions [std].** Within month `t`, in order: liquidation value moves and the
  euro leg accrues; the UC management charge is taken on the units held at the **start** of
  the month; arbitrages and withdrawals settle; the `capital sous risque` is observed; the
  plancher premium is levied; decrements act at end of month. Settlement frictions (J+3
  value dating [S10 ART 12.B], next-working-day arbitrage dating [S7], six-month deferral
  powers [S7]) are ignored.
- **Age basis.** Age last birthday **[std]**; policy year `y = t // 12 + 1`, attained age
  `age(t) = issue_age + t // 12`, so the tariff steps at each policy anniversary. The
  published tariffs are quoted by the insured's attained age at the calculation date
  [S4 Annexe I] and are read at `age(t)`.
- **Currency and precision.** EUR; full precision carried, unit counts and liquidation values
  reported to four decimals (`au dix millième` [S13 art. 32.2]), money to cents **[std]**.
- **Model points.** Single-policy, expected (probability-weighted) basis: survivorship
  factors multiply per-policy cash flows. One composite UC support **[std]** (spec footnote 6).
- **Unit-price scenario.** The liquidation value path is **exogenous**. The base run uses a
  deterministic annual UC return, the worked example a stress path. No stochastic generator is
  specified here and the plancher is **not** valued as an option — see Key sensitivities.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `point_id` | int | 1 |
| `issue_age` | int (age last birthday) | 65 **[std]** |
| `sex` | enum {M, F} | M **[std]** |
| `premium` | currency, single premium | 100,000 **[std]** |
| `prem_charge_rate` | rate — `frais sur versement` | 0.0100 **[std]** |
| `uc_alloc` | share of the net premium to the UC leg | 0.70 **[std]** |
| `euro_alloc` | share to the euro support, = 1 − `uc_alloc` | 0.30 **[std]** |
| `unit_price_init` | liquidation value of the UC support at issue | 100.00 **[std]** |
| `mgmt_fee_rate_uc` | annual UC `frais de gestion sur encours` | 0.0088 **[std]** [R13] |
| `euro_credit_rate` | annual rate credited to the euro leg, **net** of the euro charge | 0.0250 **[std]** — pointer to `Euro_FR_S` |
| `arbitrage_fee_rate` | rate on the amount switched | 0.0050 [S13] |
| `plancher_flag` | bool — rider elected | True **[std]** (base cell); the rider itself is [S1] [S3] [S4] [S7] |
| `plancher_basis` | enum {`simple`, `indexee`, `cliquet`} | `simple` **[std]** (spec footnotes 14–15) |
| `plancher_index_rate` | annual indexation used by `indexee` | 0.0350 [S1] [S3] |
| `plancher_ratchet_months` | ratchet period used by `cliquet` | 12 **[std]** |
| `plancher_gross_basis` | bool — floor on gross rather than net premiums | False [S4]; True is [S1] [S3] [S13] |
| `plancher_end_age` | attained age at which the cover ceases | 75 [S1] [S3] [S4] |
| `plancher_cap` | cap on the `capital sous risque` | 300,000 [S1] [S3] [S4] |
| `plancher_levy_source` | enum {`euro_first`, `uc_units`} | `euro_first` [S1] [S3] [S4] |
| `wd_pattern` | enum {`none`, `one_off`, `programmed`} | `one_off`: 5,000 at t = 5 **[std]** |
| `arb_pattern` | enum {`none`, `one_off`, `progressive`} | `one_off`: 10,000 euro → UC at t = 2 **[std]** |
| `uc_return_scenario` | id of a monthly UC return path in `uc_scenario_table.csv` | `stress_yr1` **[std]** |
| `proj_len` | number of months projected — the exclusive end of the frame `t = 0 … proj_len − 1` | 12 in the worked example; 360 in the base run **[std]** |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `unit_price(t)` | Liquidation value of the composite UC support at end of month t | scenario input |
| `units(t)` | Number of UC units held per policy | monthly recursion |
| `av_uc_pp(t)` | UC account value per policy = `units(t) × unit_price(t)` | derived |
| `av_euro_pp(t)` | Euro-support account value per policy | monthly recursion |
| `av_pp_at(t, timing)` | Total account value per policy at `"OPENING"`, `"BEF_FEE"`, `"BEF_WD"`, `"BEF_LEVY"` or `"BEF_DECR"`; `"OPENING"` is the balance the month opens on, `prem_to_av_pp` when `t = 0` | derived |
| `av_at(t, timing)` | `av_pp_at(t, timing) × pols_if_at(t, "AFT_DECR")` — the in-force account value, a **stock** weighted by the end-of-month count `l(t+1)` | derived |
| `cum_prem_net(t)` | Floor base: cumulative premiums net of `frais sur versement`, less partial surrenders | on premium / surrender |
| `plancher_ratchet(t)` | Highest account value observed at a ratchet date, adjusted proportionally for surrenders (`cliquet` only) | at ratchet dates and on surrender |
| `plancher_amount(t)` | The floor `F(t)` under the elected basis | monthly |
| `nar(t)` | `Capital sous risque` — the net amount at risk | monthly |
| `uc_cost_basis(t)` | Cumulative net amounts invested in the UC leg, less the pro-rata cost of amounts taken out — the `prélèvements sociaux` base | on premium / arbitrage / outflow |
| `pols_if(t)` | In-force probability at the **start** of month t — the notes' `l(t)`, and the weight on every flow of month t; `pols_if(0) = 1` | monthly decrements |
| `pols_if_at(t, timing)` | The same count at `"BEF_DECR"`, `"BEF_LAPSE"` or `"AFT_DECR"`; `"AFT_DECR"` is the end-of-month count, the notes' `l(t+1)` | monthly decrements |
| `age(t)` | Attained age = `issue_age + t // 12` | monthly |

---

## Assumption inputs

Three classes are distinguished explicitly, because on this product they behave very
differently: (a) is thin and hard, (b) is where the insurer's discretion lives, and (c) is
where every number is the modeler's.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| What is guaranteed on the UC leg | The **number** of units, never their value | [R2]; reproduced [S1] [S3] [S4 art. 17.1.1] [S7] [S10 ART 9.A] [S13 art. 32.5] |
| Death benefit | `max(plancher_amount, account value)` = account value + `capital sous risque`, before the cessation age | [S1] [S3] [S4]; basis choice **[std]** (spec footnotes 14–15) |
| Cap on the cover | `capital sous risque` ≤ 300,000 €, the excess reducing the floor | [S1] [S3] [S4] |
| Cessation of the cover | Attained age 75; also on total surrender or payment of the benefit | [S1] [S3] [S4] [S7] [S11] |
| Charge base for the rider | The `capital sous risque`, by attained age; nil when the account value is at or above the floor | [S4 Annexe I] [S3 art. 21] [S4 art. 17.1.2] |
| Levy order for the rider | Euro support first, then the largest UC support by cancelling units | [S1] [S3] [S4] |
| Surrender value | Account value across all supports; no exit charge | [S1] [S3] [S4] [S7] [S10] [S11] [S13] |
| Charge mechanism on UC | Percentage rates applied by **cancelling units** | [S1] [S3] [S4] [S7] [S13 art. 32.4] [S10 ART 12.A] |
| Partial surrender allocation | Pro rata across supports unless elected | [S10 ART 13.A]; default **[std]** |
| Effect of a surrender on the floor | Reduces the floor base by the amount surrendered | [S1] [S3] [S4 Annexe I] |
| Effect of an arbitrage on the floor | None — an arbitrage is neither a premium nor a surrender | [S1] [S4] [S7] [S10] [S13] |
| `Prélèvements sociaux` on UC | 17.2%, levied only at `dénouement` | [S4 Annexe II] [R8 II, 3°, c)](#frlib-assurance_vie_uc-r8) |
| Unit precision | Four decimals | [S13 art. 32.2] |

### (b) Insurer-discretionary current elements (snapshot)

All revisable — art. A. 132-8 requires charge **maxima** to be disclosed, not levels to be
capped [REG-R30], and MACSF may renegotiate the plancher tariff with the `souscripteur` if
the group's demographics or the guarantee's technical results change [S10 ART 8.D]. The
model holds the snapshot.

| Input | Snapshot value | Basis |
|---|---|---|
| UC management charge `c` | 0.88% p.a. | **[std]** anchored on the market average [R13] [R14] [REG-R48]; range 0.475%–1.50% across [S1]–[S13] |
| `Frais sur versement` `e` | 1.00% | **[std]**; range nil–4.50% [S1] [S3] [S4] [S6]–[S8] [S10] [S11] [S13] |
| `Frais d'arbitrage` `φ` | 0.50% of the amount switched | [S13]; level **[std]**; range nil [S11] to 2% [S10] |
| Plancher tariff `PA(a)` | The Spirica published table, annual premium per 10,000 € of `capital sous risque`, ages 12–74 | [S4 Annexe I]; shipped as `plancher_rate_table.csv` |
| `euro_credit_rate` | 2.50% p.a., net of the euro management charge | **[std]** — the euro leg's `participation aux bénéfices` machinery and its citations live in `Euro_FR_S` |
| Indexation of an `indexee` floor | 3.50% p.a. | [S1] [S3]; the PRO BTP form sets it annually at the insurer's discretion [S12] [S13 art. 8.2] |
| `Gestion pilotée` surcharge | Off (0 bp); +29 bp when enabled | [R13]; **[std]** |
| Fund-level recurring costs | 1.60% p.a., inside `unit_price` — **not** insurer income | [R13]; **[std]** |

### (c) Behavioral / experience assumptions (modeler's view)

Everything in this table is **[std]**. The research file is explicit that the retrieved
documents give a modeler **no mortality basis** (the tariffs are rate cards, and the table,
age definition, loading and margin behind them are undisclosed), **no surrender or arbitrage
behavior**, **no unit-return assumption** beyond the ±10% p.a. and ±50%-over-8-years
disclosure conventions, and **no expense basis**.

| Input | Recommended basis | Basis tags |
|---|---|---|
| Best-estimate mortality `mort_rate` | INSEE-derived **[std]** proxy, sex-distinct, single year of age, anchored so the model's base factor reproduces the placeholder below exactly | [REG-R24]; anchoring **[std]**; the permitted-table rule is [REG-R23] |
| Placeholder `q` at the worked-example age | 1.20% p.a. at male 65 | **[std]** (1) |
| Mortality improvement | None in the base | **[std]** |
| Base surrender `lapse_rate` | Table below, with a **duration-8 spike** | **[std]** (2) [REG-R40] |
| Dynamic surrender multiplier | Formulas under Policyholder behavior modeling | **[std]** |
| Partial-surrender pattern | `one_off` 5,000 € at t = 5 in the worked cell; `programmed` = 5% of the account value a year in the base run | **[std]** |
| Arbitrage pattern | `one_off` 10,000 € euro → UC at t = 2 in the worked cell | **[std]** |
| Base UC return | 4.90% p.a., the five-year average performance of UC supports net of fund charges | [R13] [REG-R48]; use as a projection assumption **[std]** |
| Worked-example UC return | `stress_yr1`: +1.00% a month for months `t = 0`–`5`, −5.00% a month for months `t = 6`–`11` | **[std]** (3) |
| Acquisition expense | 400 € per policy at issue | **[std]** |
| Maintenance expense | 40 € per policy p.a., level | **[std]** |

1. Order-of-magnitude placeholder consistent with the class-(c) proxy, chosen so the worked
   example's decrement arithmetic is checkable by hand. It is **not** the mortality implied
   by the plancher tariff: 196 € per 10,000 € of `capital sous risque` at age 65 [S4] is
   1.96% of the net amount at risk a year, which would be a very heavy `q` if it were pure
   risk premium — but no insurer publishes the split between mortality, expense loading and
   margin, so the tariff cannot be decomposed [S1] [S3] [S4] [S7]. The model therefore
   carries the tariff as a **price** and the mortality as an **assumption**, and the
   difference between them is the rider's expected margin.
2. Shape rationale: the recommended holding period is 8 years [S5] [S12], and art. 125-0 A
   CGI makes the eighth anniversary the point at which the withholding rate falls to 7.5%
   and the 4,600 € / 9,200 € annual `abattement` becomes available [REG-R40] [S4 Annexe II].
   A model with no duration-8 spike has ignored the single strongest driver of French
   surrender timing. Level anchor: UC benefits of 32.6 bn € against UC `provisions
   mathématiques` of 666.4 bn € imply an aggregate outflow of roughly **4.9% of provisions**
   in 2025 — a figure **derived** from [R13], not published, and one that mixes surrenders,
   deaths and maturities.
3. A deliberate stress, not a best estimate. It is chosen so the worked example crosses the
   floor: the `capital sous risque` is zero for the first seven months and positive
   thereafter, which is the branch an implementation most often gets wrong.

Reference base surrender table **[std]** (annual rates on the whole contract):

| Policy year | 1 | 2–4 | 5–7 | 8 | 9+ |
|---|---|---|---|---|---|
| `lapse_rate` | 2% | 4% | 6% | **12%** | 6% |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy month, **0-based**: t = 0, 1, …, `proj_len − 1`; `y = t // 12 + 1`; `a = age(t) = issue_age + t // 12` |
| `X_init` | the value of a state variable **at issue** — time 0, before month 0 opens; the opening balance of month 0, as `X(t−1)` is the opening balance of month `t ≥ 1` |
| `P`, `e` | single premium (100,000) and `frais sur versement` rate (0.0100) |
| `α` | `uc_alloc` (0.70); the euro share is `1 − α` |
| `p(t)` | `unit_price(t)`, end of month t; `p_init = 100.00` |
| `n(t)` | `units(t)`, end of month t; `n_init = P(1−e)α / p_init` |
| `c`, `c_m` | UC management charge 0.0088 p.a.; `c_m = c/12 = 0.000733333` **[std 1/12 convention]** |
| `i_e` | `euro_credit_rate` 0.0250 p.a.; monthly factor `(1+i_e)^(1/12) = 1.002059836` **[std]** |
| `V(t)` | `av_euro_pp(t)`, the euro-support balance |
| `U(t)` | `av_uc_pp(t) = n(t) × p(t)` |
| `S(t)` | `cum_prem_net(t)`, the floor base |
| `F(t)` | `plancher_amount(t)` |
| `R(t)` | `plancher_ratchet(t)` (`cliquet` only) |
| `K(t)` | `nar(t)`, the `capital sous risque` |
| `π(a)` | `plancher_rate(a) = PA(a)/10 000`; `π(65) = 0.0196`; monthly `π(a)/12` |
| `W(t)`, `W_uc(t)`, `W_eur(t)` | `withdrawals(t)` and its pro-rata split |
| `A(t)`, `φ` | gross amount arbitraged euro → UC; `arbitrage_fee_rate` 0.0050 |
| `B(t)` | `uc_cost_basis(t)` |
| `τ` | `prélèvements sociaux` rate, 0.172 [S4 Annexe II] |
| `q_m(t)`, `w_m(t)` | monthly mortality and surrender rates, `1 − (1 − rate_ann)^(1/12)` |
| `l(t)` | in force at the **start** of month t, `l(0) = 1`, and the weight on that month's flows; the cells is `pols_if(t)` |
| `l(t+1)` | in force at the **end** of month t, once its decrements have gone; the cells is `pols_if_at(t, "AFT_DECR")` |
| `E(t)` | maintenance expense = 40/12 per month **[std]** |

Dimension check: `c_m`, `π(a)/12`, `q_m`, `w_m`, `τ`, `φ` and `e` are dimensionless
per-period rates; `n(t)` is a pure count; `p(t)` is EUR per unit; `U`, `V`, `S`, `F`, `R`,
`K`, `W`, `A`, `B`, `E` are EUR; `π(a)/12 × K(t)` and `q_m(t) × K(t)` are EUR per
policy-month.

### Issue (time 0, before month `t = 0`)

These are the balances the first projected month opens on. They are **not** a row of the
cash-flow frame: nothing happens at time 0 that is not part of month 0.

    prem_to_av_pp = P × (1 − e)
    p_init = 100.00
    n_init = prem_to_av_pp × α / p_init
    V_init = prem_to_av_pp × (1 − α)
    S_init = prem_to_av_pp                  [net-premium floor basis, S4 Annexe I]
    R_init = av_pp_at(0, "OPENING") = prem_to_av_pp
    B_init = prem_to_av_pp × α
    l(0) = 1,   F_init = S_init,   K_init = 0

`K_init = 0` exactly, because the net-premium floor equals the account value at issue. That
is an assertable invariant, not a coincidence — see spec footnote 14.

### The unit leg

The UC management charge is taken on the units held at the start of the month and cancels
units [S7] [S13 art. 32.4]. Throughout these recursions `n(t−1)`, `p(t−1)` and `V(t−1)`
mean the **opening** balance of month `t`, which in month `t = 0` is `n_init`, `p_init`
and `V_init`; the model reads them through `units_open(t)`, `unit_price_open(t)` and
`av_euro_open_pp(t)`:

    fee_units(t) = n(t−1) × c_m
    mgmt_fee_uc(t) = fee_units(t) × p(t)            ← insurer income, in EUR
    n'(t) = n(t−1) × (1 − c_m)

then the month's events settle on the unit count:

    n(t) = n'(t) + A(t)(1 − φ)/p(t) − W_uc(t)/p(t)
                 − 1{plancher_levy_source = uc_units} × plancher_charge(t)/p(t)

With `plancher_levy_source = euro_first` the last term vanishes and **the unit count is a
deterministic function of the event schedule alone** — market-independent, exactly as art.
A. 132-5 implies [R2]. With no events at all it collapses to
`n(t) = n_init × (1 − c_m)^(t+1)` — `t + 1` monthly levies have fallen by the end of month
`t` — which is the sequence the insurers publish: at 0.1875% a quarter Bourso Vie prints 100 →
99.2521 → 98.5098 → 97.7731 → 97.0418 → 96.3161 → 95.5957 → 94.8808 → 94.1711 over eight
years [S3 art. 21], and at 0.25% a quarter Himalia prints 99.0037 → 98.0174 [S2].

    U(t) = n(t) × p(t)

### The euro leg (pointer)

    V(t) = V(t−1) × (1 + i_e)^(1/12) − A(t) − W_eur(t)
                 − 1{plancher_levy_source = euro_first} × plancher_charge(t)

`i_e` is credited **net of the euro management charge**, so the euro leg produces no margin
line in UC_FR_S. The euro fund's real machinery — the `participation aux bénéfices`, the
PPB and its eight-year vintage ledger, the `effet cliquet`, all of it fixed for the closing
financial year and credited at 31 December — is `Euro_FR_S`'s. The 1/12 accrual here is a
**[std]** smoothing of that annual credit across the months, and it is a simplification
rather than a grid artefact: `Euro_FR_S` runs on the **same monthly grid** as this model
and does not smooth, landing the whole year's `taux servi` in the anniversary month.
Because twelve monthly factors compound to exactly `1 + i_e`, the two readings agree at
every anniversary and differ only for a mid-year exit — which `Euro_FR_S` pays the
contractual floor rate `pro rata temporis` and this model pays a pro-rated share of the
year's credit.

### Withdrawals and arbitrages

A partial surrender is split pro rata across the supports [S10 ART 13.A]:

    av_pp_at(t, "BEF_WD") = U_before(t) + V_before(t)
    W_uc(t)  = W(t) × U_before(t) / av_pp_at(t, "BEF_WD")
    W_eur(t) = W(t) − W_uc(t)
    S(t) = S(t−1) − W(t)                    [floor base falls by the nominal amount]

An arbitrage moves `A(t)` out of the euro leg, pays `A(t) × φ` to the insurer and invests
`A(t)(1 − φ)` in units at `p(t)`. **It does not touch `S(t)`.**

### The garantie plancher

Floor, by `plancher_basis`:

    simple    F(t) = S(t)
    indexee   F(t) = [F(t−1) × (1 + plancher_index_rate)^(1/12)] − W(t)
    cliquet   R(t) = R(t−1) × (1 − W(t)/av_pp_at(t, "BEF_WD"))          on a surrender
              R(t) = max(R(t), av_pp_at(t, "BEF_LEVY"))                 at a ratchet date
              F(t) = max(S(t), R(t))

A ratchet date falls at the **end** of month `t`, which is `t + 1` months from issue, so an
`n`-month ratchet fires where `(t + 1) mod n = 0`: the first annual ratchet is the end of
`t = 11`.

The `indexee` recursion indexes the running floor and then deducts the **nominal**
withdrawal, which is arithmetically identical to indexing the withdrawal forward from its own
date and deducting it later — the sources' rule that surrenders are indexed on the same basis
as the floor [S1] [S3]. The
`cliquet` adjustment is **proportional**, because a ratchet is a value level, not a premium
tally; that is the only reason `cliquet` differs from `simple` in a year with no ratchet
event, and it is asserted in the worked example.

Net amount at risk and charge:

    av_pp_at(t, "BEF_LEVY") = U(t) + V(t)          (after fee, arbitrage and withdrawal)
    K(t) = 0                                        if not plancher_flag or a ≥ plancher_end_age
    K(t) = min(plancher_cap, max(0, F(t) − av_pp_at(t, "BEF_LEVY")))    otherwise
    plancher_charge(t) = K(t) × π(a) / 12

`K(t)` is observed once a month and used for **both** the charge and the benefit; the
published design observes weekly and levies monthly in arrears [S1] [S3] [S4], and the
half-month timing difference is the **[std]** discretization (spec footnote 16).

### Benefits and decrements

    av_pp_at(t, "BEF_DECR") = av_pp_at(t, "BEF_LEVY") − plancher_charge(t)
    death benefit per death        = av_pp_at(t, "BEF_DECR") + K(t)
    surrender benefit per lapse    = av_pp_at(t, "BEF_DECR")
    claims_death(t)  = l(t) × q_m(t) × [av_pp_at(t, "BEF_DECR") + K(t)]
    claims_lapse(t)  = l(t) × (1 − q_m(t)) × w_m(t) × av_pp_at(t, "BEF_DECR")
    withdrawals(t)   = l(t) × W(t)
    l(t+1) = l(t) × (1 − q_m(t)) × (1 − w_m(t))          [deaths before surrenders, **[std]**]

The whole of the account value is funded by cancelling units and by the euro balance, so the
insurer's non-unit cost per death is **exactly `K(t)`** — the `capital sous risque`, and
nothing else.

### Prélèvements sociaux

The UC leg is taxed only at `dénouement` [R8 II, 3°, c)](#frlib-assurance_vie_uc-r8); the euro leg is taxed annually as
interest is credited [R8 II, 3°, a)](#frlib-assurance_vie_uc-r8) and that flow belongs to `Euro_FR_S`. On an outflow of
`X` from the UC leg (partial surrender, surrender or death):

    B(t) = B_open(t) + A(t)(1 − φ)                        on investments, with
           B_open(t) = B_init for t = 0 and B(t−1) for t ≥ 1
    gain(X) = X × (1 − B / U_before)
    social_levy_uc = τ × max(0, gain(X))
    B := B − B × X / U_before                              pro-rata cost removal

The levy is **withheld and remitted** — a pass-through, not insurer income or expense. It is
reported in its own column and is excluded from `net_cf`. On a UC loss it is zero, and art.
L. 136-7 III bis provides for restitution of an excess already levied on the euro leg where
the contract's final liquidation produces a negative base [R8]. Whether the plancher top-up
above the account value is inside the levy base is **not stated in any retrieved document**;
the model puts it outside and flags the treatment [unverified] (spec footnote 21).

### Non-unit (insurer) cash flow extraction

| Cash flow | Formula | Sign | In-force weight |
|---|---|---|---|
| `Frais sur versement` | `P × e` at t = 0 | + | 1 |
| UC management charge | `mgmt_fee_uc(t)` | + | `l(t)` |
| `Frais d'arbitrage` | `A(t) × φ` | + | `l(t)` |
| Plancher charge | `plancher_charge(t)` | + | `l(t)` |
| Plancher death strain | `K(t)` | − | `l(t) × q_m(t)` |
| Maintenance expense | `E(t)` | − | `l(t)` |
| Acquisition expense | 400 **[std]** at t = 0 | − | 1 |
| Account-value benefits (death, surrender, withdrawal) | funded by unit cancellation and the euro balance — no non-unit flow | 0 | — |
| Euro-leg margin | out of scope; produced by `Euro_FR_S` | 0 | — |
| Fund-level recurring costs | inside `unit_price`, accrue to the fund manager | 0 | — |
| `Prélèvements sociaux` | withheld and remitted — pass-through | 0 | — |

    net_cf(t) = l(t) × [ mgmt_fee_uc(t) + A(t)φ + plancher_charge(t)
                         − E(t) − q_m(t) × K(t) ]
                + (P·e − 400) × 1{t = 0}

The premium charge and the acquisition expense fall in the **first projected month**,
`t = 0`. The issue instant is not a row of its own: the issue balances are what month 0
opens on, not a period. Because `l(0) = 1` they carry their full per-policy amount.
`UC_FR_S` is the source of truth for the placement: `result_cf()` has rows
`t = 0 … proj_len − 1` and `prem_charge(0) = 1,000.00`, `expenses(0) = 403.33`,
`net_cf(0) = 647.99`.

`net_cf` is income-positive; an outgo-positive presentation is simply `−net_cf(t)`, and no
`liability_cf` cells is shipped.

**The in-force weight, and the column that publishes it.** `l(t)` above is the count at
the **start** of month t, and it is what `result_cf()` publishes in its own `pols_if` column
on that same row: `pols_if(t) = l(t)`. Divide any flow on row t by that row's `pols_if`
and the per-policy amount comes back. The end-of-month count `l(t+1)` is reached through
`pols_if_at(t, "AFT_DECR")` — the `CashValue_SE` timing form the library's shared vocabulary
prescribes — and it is what the account-value *stock* `av_at(t, timing)` is weighted by.

### Monthly processing order **[std]**

For month `t`, per policy in force at its start:

1. Advance `y`, `a`, `E(t)`; read `p(t)` from the scenario.
2. Accrue the euro leg: `V ← V × (1 + i_e)^(1/12)`.
3. Take the UC management charge on the **opening** unit count: cancel `n(t−1) × c_m` units,
   book `mgmt_fee_uc(t) = n(t−1) × c_m × p(t)`.
4. Settle any arbitrage: `V ← V − A(t)`; book `A(t) × φ`; buy `A(t)(1 − φ)/p(t)` units; add
   `A(t)(1 − φ)` to `B`.
5. Settle any withdrawal: split `W(t)` pro rata, cancel `W_uc(t)/p(t)` units, reduce `V` by
   `W_eur(t)`, reduce `S` by `W(t)`, reduce `R` proportionally, compute the UC gain component
   and the `prélèvements sociaux`, and remove the pro-rata cost from `B`.
6. Set `av_pp_at(t, "BEF_LEVY") = U(t) + V(t)`; update `F(t)` on the elected basis; observe
   `K(t)`.
7. Levy `plancher_charge(t) = K(t) × π(a)/12` from the euro leg (or by cancelling units if
   `plancher_levy_source = uc_units`); set `av_pp_at(t, "BEF_DECR")`.
8. Decrements at end of month, deaths before surrenders: book `claims_death(t)` at
   `av_pp_at(t, "BEF_DECR") + K(t)` and `claims_lapse(t)` at `av_pp_at(t, "BEF_DECR")`; roll
   `l(t)` forward to `l(t+1)`.
9. Extract the non-unit row and accumulate `net_cf(t)`. In month `t = 0` that row also
   carries the `frais sur versement` and the acquisition expense.

### Known modeling pitfalls

These are the ways an implementation of *this* product looks right and is wrong. Each one is
a test.

- **Charging the plancher on the account value instead of on the net amount at risk.** The
  charge base is `K(t)`, not `av_pp_at(t, ·)` [S4 Annexe I]. On the worked cell at t = 11 the
  correct charge is `16,642.74 × 0.0196/12 = 27.18`; on the account value it would be
  `77,357.26 × 0.0196/12 = 126.35`, a factor of 4.6. Test: with the plancher out of the money
  the charge must be **exactly zero**, and `sum(plancher_charge) == 0` for any path on which
  `av_pp_at(t, "BEF_LEVY") ≥ plancher_amount(t)` for all `t`.
- **Forgetting that the net amount at risk is floored at zero.** `max(0, F − av)`, not
  `F − av`. Without the floor the rider pays the insurer a negative charge (a rebate) in
  every rising month, and the death strain becomes negative — the model silently books the
  gain on the units as insurance profit.
- **Applying the cap to the benefit rather than to the risk.** The cap is on the `capital
  sous risque`, and any excess **reduces the floor** [S1] [S3] [S4]; capping the death
  benefit at 300,000 € instead is a different, much cruder contract.
- **Letting an arbitrage move the floor.** `S(t)` changes on premiums and surrenders only.
  An arbitrage moves value between the legs, pays a fee and leaves the guarantee untouched;
  in the worked example the 10,000 € switch at t = 2 leaves `plancher_amount = 99,000.00`.
- **Adjusting the `cliquet` floor by the nominal withdrawal.** A ratchet is a value level, so
  it is reduced **proportionally**; the `simple` floor base is reduced **nominally**. In the
  worked example the two rules give 94,216.29 and 94,000.00 at t = 11 on the same path.
- **Charging the management fee on the closing rather than the opening unit count.** In a
  month with an arbitrage the two differ by the arbitrage's units: at t = 2 the opening-count
  fee is 52.28 and the closing-count fee would be 59.54. Immaterial monthly, systematic over
  decades, and a common source of a persistent reconciliation break against an admin system.
- **Using `1 − (1 − c)^(1/12)` instead of `c/12`.** The insurers compound the *periodic*
  rate: 0.25% a quarter gives an annual factor of `(1 − 0.0025)^4 = 0.99003744`, not
  `1 − 1.00%` [S1] [S2]. The model uses `c/12` for the same reason. Note that Suravenir's own
  published table prints `100 × (1 − 0.60%) = 99.4000` after a year while a monthly 1/12
  levy gives 99.4016 [S7] — the two conventions differ in the fourth decimal of the unit
  count, which is exactly the precision the contract guarantees [S13 art. 32.2].
- **Levying the plancher premium from the wrong place.** With `euro_first` the UC unit count
  must be **unchanged** by the rider. Test: `units(11)` is 745.036125 under `euro_first` and
  744.044774 under `uc_units` on the same path — if the two agree, the levy is not being
  applied at all.
- **Applying `prélèvements sociaux` to the UC leg year by year.** That is the euro rule
  [R8 II, 3°, a)](#frlib-assurance_vie_uc-r8); the UC leg is taxed at `dénouement` only [R8 II, 3°, c)](#frlib-assurance_vie_uc-r8). A model that
  accrues the UC levy annually understates the account value throughout and overstates the
  charge base the management fee is levied on.
- **Booking the social levy, the fund-level costs or the euro credited interest as insurer
  cash flow.** All three are pass-throughs or out of scope. On the worked cell, adding the
  1.60% fund-level cost to `net_cf` would inflate the year's result by 1,136.76 € against a
  true `net_cf` of 1,262.66 — both survivorship-weighted at `l(t)`, which is the only way
  the two are comparable. The **unweighted** per-policy sum `Σ av_uc_pp(t) × 1.60%/12` is
  1,152.86 €; putting that figure against a weighted `net_cf` overstates the distortion by
  about 16 €, and is the same weighted/unweighted trap as the 630.20 / 621.33 split.
- **Reading `net_cf` as the contract's total margin.** It is the UC leg plus the rider. The
  euro leg's margin is `Euro_FR_S`'s output and must be added outside this model.
- **Letting the guarantee run past the cessation age.** `K(t)` is zero from attained age 75
  [S1] [S3] [S4], and the tariff table stops at 74 — an implementation that extrapolates the
  tariff instead of switching the cover off will silently invent a price.
- **Treating the plancher charge as a premium for contract-boundary purposes.** It is a
  deduction from an existing account, not a new premium; the rider is elected once at
  subscription and cannot be restarted [S1] [S3] [S4].

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions. No public French persistency or
arbitrage study was retrieved, and no insurer document gives a lapse table, an arbitrage
frequency or a plancher claims ratio.

- **Base surrender.** `lapse_rate(y)` per the class-(c) table, converted monthly by
  `w_m = 1 − (1 − lapse_rate)^(1/12)`.
- **Duration-8 spike [std].** The 12% rate at `y = 8` is the tax threshold of art. 125-0 A
  CGI made behavioral: at eight years the withholding falls to 7.5% and the 4,600 € / 9,200 €
  annual `abattement` opens [REG-R40] [S4 Annexe II], and the recommended holding period in
  both retrieved DICs is eight years [S5] [S12].
- **Performance multiplier [std].** `M_perf(t) = min(2.0, 1 + 2.0 × max(0, g_ref − R_12m(t)))`
  where `R_12m(t)` is the UC return over the twelve **completed** months ending at the start
  of month `t` — so it is undefined, and the multiplier exactly 1, for `t < 12` — and
  `g_ref = 4.90%` [R13]. Poor performance raises surrenders; on the deterministic base run
  `M_perf = 1`.
- **Plancher moneyness multiplier [std].** `M_pl(t) = 0.5` while `K(t) > 0` and
  `plancher_flag`, else 1.0. A policyholder holding an in-the-money floor has a reason not to
  surrender that a UK bondholder does not — surrendering forfeits the guarantee [S1] [S3]
  [S4] [S11]. This is the one behavioral assumption specific to this product, it is a pure
  standardization, and it should be the first thing a user replaces.
- **Total surrender.** `lapse_rate(t) = min(0.35, base(y) × M_perf(t) × M_pl(t))`
  **[std cap]**, where `y = t // 12 + 1` is the contractual policy year.
- **Partial surrender.** `programmed`: 5% of the account value a year, taken monthly and
  split pro rata **[std]**. Rationale: it is the pattern the eight-year tax design
  encourages, and it keeps the floor base falling in step with the account.
- **Arbitrage.** `progressive`: a fixed monthly amount from the euro leg into UC, the
  `investissement progressif` design [S4 art. 11.2.1] [S7] [S13]. Trigger-based options
  (`sécurisation des plus-values`, `limitation des moins-values`) are specified in
  `product-spec.md` and are not implemented in the base recursion; they matter because they
  systematically move value **out** of UC after a rise, shrinking the management-charge base
  and the plancher exposure at the same time.
- **Renonciation.** A 30-day unwind [REG-R29] is a real first-month lapse effect and is
  carried inside the year-1 surrender rate **[std]**, not as a separate decrement.
- **No paid-up state.** A single-premium contract carries no premium obligation.

---

## Worked example

Anchor cell, all parameters **[std]** per the tables above: male, `issue_age` 65, single
premium `P` = 100,000 €, `prem_charge_rate` 1.00%, `uc_alloc` 0.70, `unit_price_init`
100.00 €, `mgmt_fee_rate_uc` 0.88% p.a., `euro_credit_rate` 2.50% p.a. net,
`arbitrage_fee_rate` 0.50%, `plancher_flag` True, `plancher_basis` `simple`,
`plancher_end_age` 75, `plancher_cap` 300,000 €, `plancher_levy_source` `euro_first`,
`plancher_rate` = 196 € per 10,000 € of `capital sous risque` at attained age 65 [S4 Annexe
I], i.e. `π(65) = 0.0196` and `π/12 = 0.001633333`.

Events: an arbitrage of 10,000 € from the euro leg to UC at `t = 2`, the third month; a
partial surrender of 5,000 € at `t = 5`, the sixth month, split pro rata.

Scenario `stress_yr1` **[std]**: `unit_price` rises 1.00% a month for months `t = 0`–`5` and
falls 5.00% a month for months `t = 6`–`11`. Decrements: `mort_rate` 1.20% p.a. and `lapse_rate` 2.00% p.a.
**[std]**, so `q_m = 0.001005543` and `w_m = 0.001682143`. Derived monthly factors:
`c_m = 0.000733333`, `(1 + i_e)^(1/12) = 1.002059836`.

Per policy in force, EUR; unit prices and counts to four decimals, money to cents. Balances
are end-of-month, after that month's levy, so each row's `av_euro_pp` is the next row's
opening euro balance. The `init` row is the position **at issue**, before month `t = 0`
opens; it is not a row of `result_av()`, whose twelve rows are `t = 0 … 11`.

| t | `unit_price` | `units` | `av_uc_pp` | `av_euro_pp` | `av_pp_at(t,"BEF_DECR")` | `plancher_amount` | `nar` | `mgmt_fee_uc` | `plancher_charge` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *init* | 100.0000 | 693.0000 | 69,300.00 | 29,700.00 | 99,000.00 | 99,000.00 | 0.00 | — | — |
| 0 | 101.0000 | 692.4918 | 69,941.67 | 29,761.18 | 99,702.85 | 99,000.00 | 0.00 | 51.33 | 0.00 |
| 1 | 102.0100 | 691.9840 | 70,589.29 | 29,822.48 | 100,411.77 | 99,000.00 | 0.00 | 51.80 | 0.00 |
| 2 | 103.0301 | 788.0502 | 81,192.89 | 19,883.91 | 101,076.80 | 99,000.00 | 0.00 | 52.28 | 0.00 |
| 3 | 104.0604 | 787.4723 | 81,944.69 | 19,924.87 | 101,869.55 | 99,000.00 | 0.00 | 60.14 | 0.00 |
| 4 | 105.1010 | 786.8949 | 82,703.44 | 19,965.91 | 102,669.35 | 99,000.00 | 0.00 | 60.69 | 0.00 |
| 5 | 106.1520 | 748.3227 | 79,435.96 | 19,040.29 | 98,476.25 | 94,000.00 | 0.00 | 61.26 | 0.00 |
| 6 | 100.8444 | 747.7739 | 75,408.83 | 19,079.51 | 94,488.34 | 94,000.00 | 0.00 | 55.34 | 0.00 |
| 7 | 95.8022 | 747.2256 | 71,585.85 | 19,113.43 | 90,699.28 | 94,000.00 | 3,295.34 | 52.53 | 5.38 |
| 8 | 91.0121 | 746.6776 | 67,956.69 | 19,141.54 | 87,098.23 | 94,000.00 | 6,890.52 | 49.87 | 11.25 |
| 9 | 86.4615 | 746.1300 | 64,511.51 | 19,164.14 | 83,675.65 | 94,000.00 | 10,307.52 | 47.34 | 16.84 |
| 10 | 82.1384 | 745.5829 | 61,240.99 | 19,181.47 | 80,422.46 | 94,000.00 | 13,555.40 | 44.94 | 22.14 |
| 11 | 78.0315 | 745.0361 | 58,136.28 | 19,193.80 | 77,330.08 | 94,000.00 | 16,642.74 | 42.66 | 27.18 |
| **Yr 1** | — | — | — | — | — | — | — | **630.20** | **82.80** |

Terminal quantities at t = 11: `uc_cost_basis` 75,420.62, `l(12)` 0.968240 — the count once
twelve months of decrements have gone, which is `pols_if_at(11,"AFT_DECR")` and not the
start-of-month `l(11) = pols_if(11)` = 0.970848 the twelfth `result_cf` row is weighted at —
and `av_at(11,"BEF_DECR")` = 77,330.08 × 0.968240 = 74,874.07.

**Plancher basis variants**, each run end to end on the same scenario with only
`plancher_basis` (and, for `cliquet`, `plancher_ratchet_months`) changed:

| Basis | `plancher_amount(11)` | `nar(11)` | `av_pp_at(11,"BEF_LEVY")` | year-1 `plancher_charge` |
|---|---:|---:|---:|---:|
| `simple` | 94,000.00 | 16,642.74 | 77,357.26 | 82.80 |
| `indexee`, 3.50% p.a. | 97,378.25 | 20,041.15 | 77,337.10 | 108.39 |
| `cliquet`, 12-month ratchet | 94,216.29 | 16,860.46 | 77,355.83 | 84.57 |
| `cliquet`, 1-month ratchet | 98,476.25 | 21,155.09 | 77,321.17 | 126.04 |

`av_uc_pp(11)` is **58,136.28 in all four**, because with `plancher_levy_source = euro_first`
the rider never touches the unit count.

**Insurer-side extraction, year 1** (per policy, survivorship-weighted at `l(t)`, the
start-of-month count, which is the `pols_if(t)` column of `result_cf()`):

- `Frais sur versement` at t = 0: **+1,000.00**
- UC management charge: **+621.33**
- `Frais d'arbitrage` (10,000 × 0.50% at t = 2): **+49.73**
- Plancher charge: **+80.67**
- Plancher death strain (`Σ l(t) q_m K(t)`): **−49.67**
- Maintenance expense (40 € p.a.): **−39.41**
- Acquisition expense at t = 0: **−400.00**
- **`net_cf` year 1 = +1,262.66**

The first and last of those fall in the **first projected month**, `t = 0`; the issue instant
is not a row of its own, and `l(0) = 1` weights them in full. That row reads
`prem_charge` 1,000.00, `mgmt_fee_uc` 51.33, `expenses` 403.33 (400 acquisition plus 40/12
maintenance), `net_cf` **647.99**.

Expected benefit and withdrawal flows, year 1: `claims_death` **1,158.20**, `claims_lapse`
**1,852.58**, `withdrawals` **4,933.21**. None of the three is a non-unit cash flow.

**Settlement arithmetic.** *Partial surrender at t = 5*: `av_pp_at(5,"BEF_WD")` =
83,469.22 + 20,007.04 = 103,476.25; the UC share is 0.80665095, so `W_uc` = 4,033.25 and
`W_eur` = 966.75; 4,033.25 / 106.1520 = 37.9951 units are cancelled; the UC gain component is
`4,033.25 × (1 − 79,250.00/83,469.22)` = **203.87**, and the `prélèvements sociaux` withheld
are `17.2% × 203.87` = **35.07** [S4 Annexe II] [R8 II, 3°, c)](#frlib-assurance_vie_uc-r8); `uc_cost_basis` falls from
79,250.00 to 75,420.62; `cum_prem_net` falls from 99,000.00 to 94,000.00.
*Death at t = 11*: the benefit is 77,330.08 + 16,642.74 = **93,972.82**, of which 16,642.74
is the insurer's strain. The UC gain is 58,136.28 − 75,420.62 = **−17,284.34**, so the UC
social levy is **zero** — and any excess levied year by year on the euro leg is restituted at
final liquidation under art. L. 136-7 III bis [R8].

**Checks.**

*Unit count.* With no events, `n(t) = n_init × (1 − c_m)^(t+1)`:
`693.0000 × (1 − 0.000733333)^2 = 691.9840` matches row `t = 1` to four decimals. Across the
arbitrage, `693 × (1 − c_m)^3 = 691.4765` units survive the third month's fee and
`9,950.00 / 103.0301 = 96.5737` are bought, giving `788.0502` — row `t = 2`. Across the
surrender, `786.3178 − 37.9951 = 748.3227` — row `t = 5`. From there
`748.3227 × (1 − c_m)^6 = 745.0361` — row `t = 11`, reached without the rider touching a
single unit.

*Independent reproduction of published tables.* The same recursion at 0.1875% a quarter gives
99.2521, 98.5098, 97.7731, 97.0418, 96.3161, 95.5957, 94.8808, 94.1711 — Bourso Vie's printed
eight-year table, digit for digit [S3 art. 21]; at 0.25% a quarter it gives 99.0037 and
98.0174 [S2]; and at an annual 0.60% on 99 units it gives 98.41, 97.82, 97.23, 96.65, 96.07,
95.49, 94.92, 94.35 — MACSF's pre-70 table [S10 ART 12.A].

*Net amount at risk, row `t = 8`.* `av_euro_pp` in the table is post-levy, so the observation base
is `87,098.23 + 11.25 = 87,109.48`, and `94,000.00 − 87,109.48 = 6,890.52`. The charge is
`6,890.52 × 0.0196/12 = 11.25` — the same figure that was added back, which is the arrears
convention closing on itself.

*Decrements.* `l(12) = [(1 − q_m)(1 − w_m)]^12 = (1 − 0.012)(1 − 0.020) = 0.968240` exactly
— twelve months of decrements, `pols_if_at(11,"AFT_DECR")` — which is the only sensible test
that the monthly rates were derived geometrically rather than by dividing by twelve.

*Total row.* **Yr 1** is the full-precision column sum rounded once (630.1985 → 630.20;
82.7961 → 82.80); adding the printed cells gives 630.18 and 82.79. The survivorship-weighted
totals in the extraction above (621.33 and 80.67) are smaller because they are multiplied by
`l(t) < 1` from the second month on.

*Euro leg.* `29,700.00 × 1.025^(2/12) = 29,822.48` — row `t = 1`, before any event.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers consume them
and are cited, not reproduced.

- **French statutory.** Art. R. 343-3 enumerates eleven technical provisions and defines the
  **provision mathématique** as the difference between the actuarial present values of the
  insurer's and the insured's respective commitments, including future management costs
  [REG-R6]. It says nothing about `unités de compte`, nothing about a unit count and nothing
  about a liquidation-value measurement, and it does not say which of the eleven provisions
  carries a UC engagement; **no retrieved statutory or ACPR text does**. The conventional
  reading — that the UC engagement sits in the provision mathématique and that for `unités de
  compte` that provision is the unit count at the liquidation value, which is arithmetic and
  is reproduced exactly by `av_uc_at(t)` — is therefore [unverified] as a statutory
  proposition. The one retrieved *primary* document that writes a `provision mathématique`
  recursion in units is MACSF's notice, whose arts. 11–12 set out the provision and the
  surrender values in units with an eight-year table [S10 ART 11–12]. The `garantie plancher`
  is a separate engagement, and **no retrieved ACPR or insurer document states how it is
  provisioned** — closed-form option valuation, stochastic
  projection or unearned premium. This library asserts nothing about it, and a user who needs
  a plancher reserve must supply the method.
- **Solvabilité II.** Technical provisions are a best estimate plus a risk margin, the best
  estimate being the probability-weighted average of future cash flows discounted at the
  relevant risk-free term structure [REG-R1] [REG-R4]. That is stated on EIOPA's authority:
  EUR-Lex could not be fetched, so no Solvency II or Delegated Regulation article number in
  this library was read from the instrument, and **no cost-of-capital rate, no lapse shock and
  no expense-inflation rule here rests on a retrieved text** [REG-R1] [REG-R2]. The natural
  presentation is a unit reserve equal to `av_uc_at(t) + av_euro_at(t)` plus the non-unit best
  estimate of the `net_cf` stream — commonly negative, because future charges exceed future
  costs.
- **Mortality basis.** Art. A. 335-1 permits only homologated tables (by sex, on INSEE data
  for non-annuity contracts) or an undertaking's own experience table certified by an
  independent actuary [REG-R23]. TH 00-02 / TF 00-02 are cited by name and article and are
  **not shipped**; the decrement CSVs are **[std]** proxies built from INSEE's freely
  redistributable series and anchored to reproduce the placeholder above [REG-R24].
- **IFRS 17 and professional standards.** IFRS 17, effective for periods from 1 January 2023,
  measures a group of contracts as risk-adjusted fulfilment cash flows plus a contractual
  service margin [REG-R45]; a multisupport contract is a candidate for the variable fee
  approach, but the VFA mechanics were not read from the standard and are [unverified]. NPA 2
  *Modèles actuariels* — a category 3 `pratique recommandée` effective 1 January 2016,
  applying to "tout modèle actuariel" under a principle of proportionality — is the standard
  this documentation, worked example and test suite are written against [REG-R44], with NPA 1
  as the general assumption-setting frame [REG-R43]. NPA 4 (best-estimate provisions in life)
  was not retrieved and is the standard most directly relevant to the plancher liability.

---

## Key sensitivities and model risks

In order of influence on this product's result:

1. **The unit-return path — twice over.** Every charge line scales with the account value,
   and the plancher cost scales with the *shortfall* of the account value below the floor.
   Those two exposures point in opposite directions and neither is symmetric: a fall cuts the
   management charge roughly proportionally and turns the rider on non-linearly. On the worked
   cell the rider costs nothing for seven months and 27.18 € at `t = 11` alone. **The base run
   is deterministic and therefore understates the plancher cost**, because `E[max(0, F − AV)]`
   exceeds `max(0, F − E[AV])`. A stochastic or scenario-set run is not an enhancement here;
   it is the only way to price the rider.
2. **Surrender behavior, and its interaction with the guarantee.** A surrender extinguishes
   the whole future charge stream at no exit cost [S1] [S3] [S4] [S7] [S10] [S11] [S13], and
   it also extinguishes an in-the-money guarantee. The `M_pl` multiplier that ties the two
   together is a pure **[std]** invention with no evidence behind it, and it moves the rider's
   result in both directions at once — hold the in-the-money policies and the strain rises,
   but so does the charge income.
3. **The plancher tariff versus the mortality assumption.** The tariff is a price [S4]; the
   mortality is an assumption [REG-R24]. Their difference is the rider's margin, and neither
   the insurers' mortality basis nor their loading is published, so the sign of that margin at
   any age is genuinely unknown. Sensitivity-test the tariff and `mort_rate` independently,
   never as a single "plancher basis".
4. **The cessation age, the cap and the charge level.** Cover ceases at 75 [S1] [S3] [S4] and
   the tariff table stops at 74, so moving the cessation age to 80 [S12] [S13] requires a
   tariff the sources do not contain. The 300,000 € cap never binds on the anchor cell but
   binds precisely in the deep drawdowns where the guarantee is worth something. And 0.88%
   p.a. is a market average [R13] [REG-R48], not a contractual rate: there is **no statutory
   ceiling** on any French life charge [REG-R30], and retrieved contract rates span 0.475% to
   1.50% — a factor of three on the dominant income line.
5. **The euro leg's credited rate.** It enters only through the account value and the levy
   source, but it does both: a lower credited rate makes the floor bite sooner *and* shrinks
   the balance the plancher premium is taken from, which under `euro_first` eventually forces
   the levy onto the units and makes the unit count path-dependent.
6. **Macroprudential and liquidity tail.** The HCSF may limit surrender payments for up to six
   consecutive months and defer or restrict arbitrages and advances [REG-R13]; arts. R. 131-8
   to R. 131-12 govern a UC whose underlying fund gates redemptions [R7]. Neither is modeled,
   and both are why a French mass-surrender stress is a scenario, not a multiplier.
7. **What the sources do not give, and the model therefore invents.** No mortality basis, no
   lapse or arbitrage experience, no unit-return assumption, no expense basis, no reserving
   method for the plancher, and no French `plancher cliquet` design at all. Every one of those
   is **[std]** here, and the honest reading of this model is as a mechanics demonstration
   whose parameters must be replaced before any of its numbers mean anything.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R13]: #frlib-assurance_vie_uc-r13
[R14]: #frlib-assurance_vie_uc-r14
[R2]: #frlib-assurance_vie_uc-r2
[R7]: #frlib-assurance_vie_uc-r7
[R8]: #frlib-assurance_vie_uc-r8
[REG-R1]: #frlib-reg-r1
[REG-R13]: #frlib-reg-r13
[REG-R2]: #frlib-reg-r2
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R4]: #frlib-reg-r4
[REG-R40]: #frlib-reg-r40
[REG-R43]: #frlib-reg-r43
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R48]: #frlib-reg-r48
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
