# Technical Notes

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's product. [S#]/[R#] tags refer to the source list in
`sources.md` (numbering carried from `_research/term-assurance.md`; frozen);
[REG-R#] tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation; [unverified] marks
claims not confirmed against a retrieved document. Parameter values are identical to
those in `product-spec.md`.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premiums, death and
  terminal illness claims by benefit shape, expenses, commission) for a single-policy
  model point of guaranteed-premium UK term assurance, in the sense required for a
  Solvency UK best-estimate projection: probability-weighted future cash-flows, gross
  of reinsurance [R1], covering the cash-flow categories of the PRA cash-flows rule
  (benefits, expenses, premiums, intermediary payments) [R2]. Discounting, risk
  margin and capital layers are out of scope (see Valuation and reserve pointers).
- **Projection frequency.** Annual grid **[std]**, with a monthly option. The only
  intra-year contractual structure is the monthly step-down of the decreasing-shape
  benefit and the monthly FIB instalments [S6] [S8]; the annual grid handles both with
  mid-year approximations (below), and the monthly grid removes the approximation.
- **Timing conventions [std].** Premiums received at the start of each policy year
  (annualized, in advance); maintenance expenses at the start of each year; death/TI
  claims paid at the end of the policy year of death; lapses occur at the end of the
  policy year, after deaths. Acquisition expenses and initial commission at issue
  (start of year 1).
- **Age basis.** Age nearest birthday at entry, plus curtate policy year — attained
  age in year `t` is `x + t − 1` **[std]**. (The fetched product documents do not
  state an age basis; UK assured-lives tables are select tables — AM92 has a 2-year
  select period, TMNL16/TFNL16 a 5-year select period [R12] — so the mortality
  interface must accept select-by-duration rates.)
- **Currency.** GBP throughout. Benefits are paid in sterling to UK bank accounts
  [S1].
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
  No aggregation logic is specified here.
- **Termination.** All states terminate at the end of the term: cover expires with no
  maturity value, no renewal, and no conversion — there is no US-style post-level-term
  ART tail [S1] [S2] [S6] [S8] [R8]. The projection horizon is exactly `n` years.
- **Contract boundary.** Premiums are guaranteed, so the insurer has no unilateral
  repricing right and the Solvency UK contract boundary is the full term [R3]: all
  `n` years of premiums and benefits are inside the boundary. (Reviewable-premium
  variants — CI riders, out of scope — would require the rules 3.3/3.7 test [R3].)
- **Rounding.** Intermediate values at full precision; displayed cash flows to pence
  **[std]**.

---

## Model point attributes

| Attribute | Type | Example (anchor cell **[std]**) |
|---|---|---|
| `shape` | enum {level, decreasing, fib} | level |
| `issue_age` | int (age nearest birthday) | 35 |
| `sex` | enum {M, F} | M |
| `smoker` | enum {N, S} | N |
| `term_y` (`n`) | int, years (1–50; decreasing 5–50; FIB 5–40) | 25 |
| `sum_assured` (`SA0`) | GBP (level/decreasing shapes) | 150,000 |
| `fib_income` (`I`) | GBP/month (fib shape) | 1,000 |
| `sched_rate` (`j`) | annual effective (decreasing shape) | 0.06 **[std]** |
| `joint_first_death` | bool (base model: false) | false |
| `indexation` | bool (RPI option elected) | false |
| `wop` | bool (waiver rider; base model: false) | false |
| `premium_monthly` (`P_m`) | GBP/month | 12.00 **[std]** |
| `premium_mode` | enum {monthly, annual} | monthly |
| `issue_date` | date | — |

The anchor premium is a pure modeling value: no UK insurer publishes premium rate
tables (quote-engine pricing; only the £5/month minimum is public [S5]), so any
reference premium basis is constructed, not observed **[std]**.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l(t)` | In-force probability at the start of policy year t; `l(1) = 1` | annual recursion |
| `q(t)` | Mortality rate (incl. TI acceleration) applied in year t | assumption lookup |
| `w(t)` | Lapse rate applied in year t | assumption lookup |
| `D(t)` | Expected deaths/TI claims in year t = `l(t) × q(t)` | annual |
| `DB(t)` | Death benefit payable for deaths in year t (shape-dependent) | annual (schedule) |
| `idx(t)` | Cumulative indexation factor (1 if option not elected/declined) | on anniversaries |
| `FIBcum(t)` | Cumulative expected FIB income streams in payment at start of year t = `Σ_{s<t} D(s)` (fib shape) | annual |
| `CF(t)` | Net liability cash flow of year t (insurer perspective, + = inflow) | annual |

The FIB in-payment ledger is **not** decremented by mortality after the claim: the
instalments are an annuity-certain to the end of the term regardless of any life
[S6] [S8].

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| Premium `P_m` | Level, guaranteed for the full term | guarantee [S2] [S6] [S9]; level **[std]** |
| Level benefit | `SA0` constant | [S1] [S6] |
| Decreasing benefit schedule | `B(k)` amortization formula at rate `j` (below) | mechanics [S1] [S6] [S8]; `j` = 6% **[std]** |
| FIB benefit | `I`/month, in arrears, death to end of term; annuity-certain | [S2] [S6] [S8] |
| Terminal illness | 100% acceleration, two-limb 12-month definition, terms ≥ 2 years | [S1] [S6] [S8] [R8] [S2] [S4] |
| Suicide exclusion | 12 months, year-one only | [S1] [S6] [S8] |
| Grace | 60 days from due date; then lapse without value | [S1] [S6] |
| Surrender/paid-up value | None | [S1] [S6] [S8] [R8] |
| Indexation option terms | cover +min(max(RPI,0),10%); premium ×(1 + 1.5×increase), cap 15%; removed after 3 declines | [S1] [S2] [S6] [S7]; composite **[std]** |
| Expiry | Cover ceases at end of term; no renewal/conversion | [S1] [S2] [S6] [S8] [R8] |

### (b) Insurer-discretionary current elements

For guaranteed-premium life-only term assurance this class is **nearly empty** — a
deliberate contrast with cash-value products: there are no bonus rates, no MVRs, no
reviewable premiums, and no non-guaranteed charge scales on the composite. The two
residual discretionary items:

| Input | Snapshot value | Basis |
|---|---|---|
| FIB commutation basis | Commuted value = PV of remaining instalments at `r_c` = 3.0% p.a. **[std]** snapshot; base model take-up 0% | discretion ("fairly and reasonably") [S6] [S8]; rate **[std]** (no insurer publishes the basis) |
| Underwriting exclusions / rated terms | None on the composite cell (standard rates) | case-by-case schedule exclusions exist [S1] [S3]; scope **[std]** |

Reviewable-premium mechanics (5-yearly reviews on claims experience, reinsurance
cost, lapses, expenses, etc.) exist on CI-type covers at two of the three carriers
[S6] [S8] and are documented there as a modeling template, but are out of scope here.

### (c) Behavioral / experience assumptions (modeler's view)

**Mortality.** The current UK protection experience tables are the CMI "16" Series —
term assurance mortality *including terminal illness* and accelerated CI, graduated
on 2015–2018 experience [R10] — with public confirmation of the table names
TMNL16/TFNL16 (male/female non-smoker, 5-year select) via their adoption in the IFoA
Formulae and Tables 2025 edition [R12]. **However, CMI tables issued after 1 March
2013 are subscriber-only** [R11], so the full 16-Series set (including
smoker/duration variants) cannot be redistributed in an open reference
implementation. The reference basis is therefore a **[std] proxy**, stated honestly:

| Input | Recommended public basis | Basis tags |
|---|---|---|
| Best-estimate mortality (incl. TI) | Shape of the public "00" Series temporary assurance tables — TMN00/TMS00 (male non-smoker/smoker), TFN00/TFS00 (female), 1999–2002 experience — scaled by a **[std]** adjustment factor (suggested 75%) to proxy improvement to the 16-Series era; AM92 (2-year select, prior Formulae and Tables basis) is the teaching-table alternative | tables [R13] [R11]; AM92 role [R12]; factor **[std]** |
| Mortality improvement | None in base **[std]**. The CMI Mortality Projections Model is the market-standard overlay — CMI_2024 (June 2025, WP201) [R14], superseded by CMI_2025 (March 2026, WP211) [REG-R30] — but the model is subscriber-restricted; a production basis would be "x% of TMNL16/TFNL16 with CMI_2025 improvements at a chosen long-term rate", all subscriber inputs | [R14] [REG-R30] [R11] |
| Population fallback | ONS national life tables (single-age qx, freely redistributable under OGL) — heavier than insured experience; use only as a last-resort open base | [REG-R32] |
| TI acceleration timing | None modeled: death and TI are one decrement, one benefit; acceleration shifts payment earlier by less than 12 months, immaterial on an annual grid **[std]** | definition [S1] [S6] [S8]; 16-Series mortality includes TI [R10] |
| Suicide-exclusion offset | Year-one claims not reduced for excluded suicides **[std]** (immaterial; no incidence data in fetched sources) | clause [S1] [S6] [S8] |

**Lapse.** FCA evidence (2024, pure protection in force): average lapse rate 5% p.a.;
highest observed early lapse 23% in policy year 1 (non-advised intermediated sales
with 4-year clawback); modest lapse spikes just after the 2-year and 4-year
commission clawback periods end [R9]. A full duration curve is not public, so the
reference table is **[std]**, anchored to the 5% average and the clawback-spike
pattern:

| Policy year | 1 | 2 | 3 | 4 | 5 | 6+ |
|---|---|---|---|---|---|---|
| Annual lapse `w(t)` **[std]** | 10% | 8% | 7% | 5% | 6% | 4% |

(Year 3 staying elevated after the 2-year clawback period ends, and the year-5
uptick after the 4-year clawback period ends, echo the post-clawback spike pattern
[R9]; levels are standardized calibrations to be replaced with the user's
experience.)

**Expenses and commission (all levels [std]; structure evidence as cited).**

| Input | Value | Basis |
|---|---|---|
| Initial (acquisition) expense | £150 per policy at issue | **[std]** |
| Initial commission | 150% of annualized premium, paid upfront at issue | upfront pattern ~96% of commission [R9]; level **[std]** |
| Commission clawback | On lapse in years 1–4: clawback of `(48 − months in force)/48` of initial commission (linear, 4-year) — optional module, base model off | clawback periods 2–4 years [R9]; formula **[std]** |
| Renewal commission | 2.5% of premiums from year 2 | **[std]** |
| Maintenance expense | £30 per policy p.a., inflating 3% p.a. | **[std]** |
| Claim expense | £250 per death/TI claim | **[std]** |
| Expense inflation | 3% p.a. flat | **[std]** |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy year, t = 1..n; attained age in year t = x + t − 1 (x = issue age) |
| `k` | policy month, k = 0..N, N = 12n (monthly grid / benefit schedules) |
| `P_a` | annualized premium = 12 × P_m = 144.00 (anchor cell) **[std]** |
| `q(t)` | mortality (incl. TI) rate for year t, select-adjusted |
| `w(t)` | lapse rate for year t (end-of-year, after deaths) **[std order]** |
| `l(t)` | in-force probability at start of year t; l(1) = 1 |
| `D(t)` | expected claims in year t = l(t) × q(t) |
| `SA0` | initial sum assured (level/decreasing) |
| `I` | FIB monthly income |
| `j`, `j_m` | decreasing schedule annual rate; j_m = (1+j)^(1/12) − 1 |
| `B(k)` | decreasing-shape benefit after k months (formula below) |
| `idx(t)` | cumulative indexation factor at start of year t (1 if not indexed) |
| `E0`, `e(t)` | initial expense (150); maintenance expense = 30 × 1.03^(t−1) |
| `c0`, `c_r` | initial commission (1.5 × P_a); renewal commission rate (0.025, from year 2) |
| `ec` | claim expense (250) |
| `CF(t)` | net cash flow of year t, insurer perspective (+ inflow, − outflow) |

Dimensional check: `q`, `w` are per-annum probabilities (dimensionless); `B`, `SA0`
are GBP; `I` is GBP/month so FIB outgo terms carry explicit month counts; all `CF`
components are GBP per year.

### Benefit amount by shape

**Level:** `DB(t) = SA0 × idx(t)`.

**Decreasing** [S1] [S6] [S8]:

    B(k) = SA0 × [(1+j_m)^N − (1+j_m)^k] / [(1+j_m)^N − 1],   B(0) = SA0, B(N) = 0

Annual-grid death benefit uses the mid-year balance **[std]**:

    DB(t) = B(12(t−1) + 6)

(whole-year identity `(1+j_m)^12 = 1+j` allows `B(12t) = SA0 × [(1+j)^n − (1+j)^t] /
[(1+j)^n − 1]`; the monthly grid uses `B(k)` at the exact month of death).
Numeric anchor (SA0 = 150,000, j = 6%, n = 25): `B(60) = 150,000 × (1.06^25 − 1.06^5)
/ (1.06^25 − 1) = 150,000 × (4.291871 − 1.338226) / 3.291871 = £134,588` — the
benefit after 5 years. Indexation and the decreasing shape are not combined
**[std scope]** (no fetched insurer offers indexed decreasing cover).

**Family income benefit** [S2] [S6] [S8]: a death in month k triggers `N − k` monthly
instalments of `I`, in arrears, ending at month N — an annuity-certain independent of
survival. On the annual grid, with deaths at mid-year **[std]**, a death in year s
generates expected instalment outgo:

    FIB outgo in year s (year of death):        6 × I × D(s)
    FIB outgo in later year u, s < u ≤ n:      12 × I × D(s)

so total FIB claim outgo in year t is

    Claims_fib(t) = I × [ 6 × D(t) + 12 × FIBcum(t) ],   FIBcum(t) = Σ_{s<t} D(s)

Optional commutation module **[std]**: replace the instalment stream at death with a
lump sum `CV(k) = I × a(N−k)` where `a(m) = [1 − (1+r_c)^(−m/12)] / [(1+r_c)^(1/12) − 1]`
is the m-month annuity-certain factor at the snapshot commutation rate `r_c` = 3%
**[std]** (contractually the insurer reduces the sum of remaining instalments
"fairly and reasonably" [S6] [S8]). Base model: no commutation.

### In-force recursion and processing order

Annual processing for year t = 1..n **[std]**:

1. **Start of year:** premium income `P_a × idx_p(t) × l(t)` (where `idx_p(t)` is the
   cumulative *premium* indexation factor — equal to 1 in the base run); maintenance
   expense `e(t) × l(t)`; renewal commission `c_r × P_a × idx_p(t) × l(t)` (from
   t ≥ 2). At t = 1 additionally `E0` and `c0` (per policy issued, l(1) = 1).
2. **Benefit schedule:** compute `DB(t)` per shape (mid-year balance for decreasing).
3. **End of year — claims:** expected death/TI outgo `DB(t) × D(t)` (level/
   decreasing) or the FIB formula above; claim expense `ec × D(t)`.
4. **End of year — lapses:** applied to survivors of mortality **[std order: death
   before lapse]**; lapse pays nothing (no surrender value [S6] [R8]).
5. **Update:**

       l(t+1) = l(t) × (1 − q(t)) × (1 − w(t))

6. **Anniversary (if indexation elected):** with acceptance (behavior section),
   `idx(t+1) = idx(t) × (1 + min(max(RPI, 0), 0.10))` and
   `idx_p(t+1) = idx_p(t) × (1 + min(1.5 × increase, 0.15))` [S1] [S2] [S6].

At t = n the projection ends: no maturity payment, no tail states [S1] [S6] [S8] [R8].

### Net cash flow

Level/decreasing shapes:

    CF(t) = P_a × idx_p(t) × l(t)                                   (premiums)
          − DB(t) × D(t)                                            (death/TI claims)
          − ec × D(t)                                               (claim expense)
          − e(t) × l(t)                                             (maintenance)
          − c_r × P_a × idx_p(t) × l(t) × 1{t ≥ 2}                  (renewal commission)
          − (E0 + c0) × 1{t = 1}                                    (acquisition)

FIB shape: replace the claims term with `Claims_fib(t)` and add `− ec × D(t)` only in
the year of death. Premiums stop at death, but FIB instalments continue — premium
income always carries `l(t)`, never the FIB ledger.

Monthly-grid variant: the same components at monthly frequency with `P_m`, monthly
decrements `q_m = 1 − (1 − q)^(1/12)`, `w_m = 1 − (1 − w)^(1/12)` **[std]**, exact
`B(k)`, and exact FIB instalments; the annualization and mid-year approximations
disappear. The annual grid slightly overstates premium income (no allowance for
premiums ceasing at mid-year deaths/lapses) — a known bias of the annual-in-advance
convention **[std]**, quantified in the pitfalls list.

### Waiver of premium (optional module, base off)

With `wop = true`, an incapacity state is added: incidence `inc(t)` **[std]**
(no public UK incidence basis for the WOP work-tasks definitions is in the fetched
sources), 26-week deferred period [S1], premiums waived while incapacitated (premium
income multiplied by the active-payer probability), mortality unchanged. The WOP
extra premium and the incidence/recovery basis are both **[std]** placeholders.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; calibration evidence is
cited where it exists.

- **Base lapse [std].** Duration table above, anchored to the FCA 5% in-force average
  and clawback-spike pattern [R9]. Channel matters: the 23% year-1 observation is
  specific to non-advised intermediated business with 4-year clawback [R9]; the
  composite table is channel-blended.
- **Selective lapsation [std] (optional module).** Lapsers are healthier on average;
  persisters' mortality is loaded:

      q_eff(t) = q(t) × [1 + λ × max(0, w_cum(t) − w_ref)]

  with `w_cum(t)` = cumulative lapse proportion to date, `w_ref` = 0.20 and λ = 0.25
  **[std]**. Base run: off (λ = 0).
- **Rebroking/dynamic lapse [std].** Guaranteed premiums mean no premium-shock lapse;
  the economic driver is rebroking when quoted market premiums for the attained age
  fall below the in-force premium (younger select lives, falling mortality). A
  reference multiplier:

      M_reb(t) = min(2.0, max(1.0, P_inforce / P_market(t)))

  applied to `w(t)`, with `P_market(t)` an external input; base run `P_market =
  P_inforce`, so M_reb = 1.
- **Indexation take-up [std].** If `indexation = true`: each anniversary the increase
  is accepted with probability 80% **[std]**; after 3 consecutive declines the option
  is removed [S1] [S6] (two at one insurer [S8]). Deterministic base run:
  always accept, RPI scenario input flat 3% **[std]**, giving
  `idx(t+1) = idx(t) × 1.03` and `idx_p(t+1) = idx_p(t) × 1.045`
  (premium factor 1.5 [S1] [S2] [S6]).
- **GIO exercise.** Not modeled: exercises create *new* policies at then-current
  rates [S1] [S6] [S8], so they add model points rather than changing this one
  **[std scope]**.

---

## Worked example

Anchor cell: male 35 non-smoker, single life, level shape, `n` = 25, `SA0` =
£150,000, `P_m` = £12.00 (`P_a` = £144.00) **[std]**; no indexation, no WOP, no
commutation; base lapse table; no selective-lapse or rebroking modules. Mortality
placeholders `q(1) = 0.00055, q(2) = 0.00060, q(3) = 0.00065` are **[std]
illustrative values in the shape of a non-smoker temporary assurance table** — they
are NOT taken from any CMI table (the current tables are subscriber-only [R11]; see
assumption class (c)). Expenses per the [std] table: `E0` = 150, `c0` = 1.5 × 144 =
216.00, `e(t)` = 30 × 1.03^(t−1), `c_r` = 2.5% from year 2, `ec` = 250.

| t | l(t) | Premiums `P_a·l(t)` | Claims `SA0·D(t)` | Claim exp `ec·D(t)` | Maint. + initial exp | Commission | Net CF(t) |
|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 144.00 | 82.50 | 0.14 | 180.00 | 216.00 | −334.64 |
| 2 | 0.899505 | 129.53 | 80.96 | 0.13 | 27.79 | 3.24 | +17.41 |
| 3 | 0.827048 | 119.09 | 80.64 | 0.13 | 26.32 | 2.98 | +9.02 |

Trace, year 1: `D(1) = 1.0 × 0.00055 = 0.00055`; claims = 150,000 × 0.00055 = 82.50;
claim expense = 250 × 0.00055 = 0.14; expenses = E0 + e(1) = 150.00 + 30.00 = 180.00;
commission = c0 = 216.00; CF(1) = 144.00 − 82.50 − 0.14 − 180.00 − 216.00 = −334.64.
Update: `l(2) = 1.0 × (1 − 0.00055) × (1 − 0.10) = 0.899505`.

Trace, year 2: premiums = 144 × 0.899505 = 129.53; `D(2) = 0.899505 × 0.00060 =
0.000540`; claims = 150,000 × 0.000540 = 80.96; claim expense = 0.13; maintenance =
30 × 1.03 × 0.899505 = 27.79; renewal commission = 0.025 × 129.53 = 3.24;
CF(2) = 129.53 − 80.96 − 0.13 − 27.79 − 3.24 = +17.41.
Update: `l(3) = 0.899505 × (1 − 0.00060) × (1 − 0.08) = 0.827048`.

The pattern is characteristic of guaranteed term: a deep new-business strain in year
1 (upfront commission and acquisition expense against one year's premium [R9]) and
thin positive margins thereafter — the level premium prefunds the rising mortality
cost, so early-duration lapses forfeit margin to the insurer while late-duration
lapses relieve it.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers
consume them and are cited, not reproduced:

- **Solvency UK best estimate.** BEL = probability-weighted average of future
  cash-flows, discounted at the relevant risk-free term structure, realistic
  assumptions, gross of reinsurance (recoverables separate) [R1]; required cash-flow
  categories per the PRA cash-flows rule — benefits, expenses, premiums,
  intermediary payments, policyholder-charged taxation [R2]; contract boundary =
  full term for guaranteed premiums [R3]. `BEL = Σ_t v(t) × [outgo(t) − income(t)]`
  over the recursion above. Note: for profitable guaranteed term assurance the BEL
  is commonly **negative** at issue (PV premiums > PV claims + expenses) — an asset
  on the regulatory balance sheet; models must not floor it at zero (derivation, no
  source).
- **Risk margin.** Technical provisions = best estimate + risk margin [REG-R1];
  cost-of-capital method at 4% with life risk-tapering factor λ = 0.9, floor 0.25
  [REG-R4] — requires an SCR run-off projection, cited-not-specified here.
- **Regime.** PS15/24 completed the restatement of Solvency II assimilated law into
  PRA rules from end-2024 ("Solvency UK") [R5].
- **IFRS 17.** UK-adopted IFRS 17 (adopted 16 May 2022, effective 1 January 2023)
  applies to IFRS reporters [REG-R38]; the fulfilment-cash-flow engine is the same
  expected-cash-flow projection; grouping, CSM and risk-adjustment layers are out of
  scope [mechanics beyond the adoption facts: unverified].
- **Professional standards.** Technical actuarial work using this model in scope of
  UK regulation falls under TAS 100 v2.0 [R15] and TAS 200 v2.0 [R16].

---

## Key sensitivities and model risks

Dominant assumptions, in rough order for a protection block:

1. **Mortality basis risk.** The reference basis is a [std] proxy (scaled "00"
   Series) because the current 16-Series tables are subscriber-only [R11] [R13];
   the proxy scaling factor (75% [std]) is the single largest lever on claims.
   Production users should substitute subscriber tables (TMNL16/TFNL16 [R12] [R10])
   and a CMI projections overlay [R14] [REG-R30].
2. **Early-duration lapse.** With ~96% of commission upfront and 2–4 year clawback
   [R9], year-1–4 lapse rates drive new-business strain recovery; the clawback
   module changes the sign of the sensitivity inside the clawback window.
3. **Selective lapsation.** Guaranteed premiums plus healthy-life rebroking imply
   persisting lives are progressively impaired; the λ loading materially moves
   late-duration claims on long terms.
4. **Expense inflation on small premiums.** Premiums as low as £5/month [S5] against
   £30/year maintenance make per-policy expense inflation a solvency-relevant
   assumption for small-sum-assured blocks.
5. **Shape-specific risks.** Decreasing: the schedule rate `j` is contractual, so
   the risk is *specification* error, not experience (mis-implementing the
   amortization or the monthly convention); FIB: the annuity-certain run-off means
   claim outgo persists up to `n − 1` years after death — omitting the in-payment
   ledger understates liabilities.
6. **Indexation take-up.** The ×1.5 premium factor [S1] [S2] [S6] makes accepted
   increases premium-margin-accretive if mortality is proportional to cover;
   selective acceptance (impaired lives accept, healthy decline) reverses the sign
   **[std]** concern; no public take-up data exists in the fetched sources.

Known modeling pitfalls:

- **TI is not an extra benefit.** Death and terminal illness are one decrement and
  one payment [S1] [S6] [S8]; adding a separate TI decrement double-counts claims.
  The 16-Series mortality tables already include terminal illness [R10].
- **FIB instalments are certain, not contingent.** Do not decrement the in-payment
  income by mortality or lapse; only *new* claims depend on `l(t)` [S6] [S8].
- **Decreasing-schedule conventions.** `j_m = (1+j)^(1/12) − 1` **[std]** vs a
  nominal `j/12` convention changes `B(k)` slightly; state the convention and use
  the `B(60) = £134,588` anchor to validate implementations.
- **Annual-grid biases.** Mid-year benefit for the decreasing shape and
  annual-in-advance premiums are offsetting small biases; the monthly grid is the
  arbiter. Do not apply both the mid-year claim timing and a separate half-year
  premium adjustment — pick one convention.
- **Lapse pays nothing.** There is no surrender value [S6] [R8]; a lapse row in the
  cash-flow output must be zero-valued (it affects only `l(t)`), unlike US models
  with CSV outflows.
- **No tail states.** Terminate everything at month N: no renewal, no conversion,
  no extended coverage [S1] [S2] [S6] [S8] [R8]. Importing a US-style post-level-term
  tail materially misstates UK term liabilities.
- **Joint life first death.** Model as a single joint decrement
  `q_joint = 1 − (1−q_1)(1−q_2)` on one policy **[std]**; the policy pays once and
  ends [S1] [S6]. Separation/replacement options create new policies and are out of
  scope.
- **Boundary discipline.** All guaranteed premiums are inside the contract boundary
  [R3]; truncating premium income at an assumed "repricing" point (a Solvency II
  habit from reviewable business) is wrong for this product.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-term_assurance-r1
[R10]: #uklib-term_assurance-r10
[R11]: #uklib-term_assurance-r11
[R12]: #uklib-term_assurance-r12
[R13]: #uklib-term_assurance-r13
[R14]: #uklib-term_assurance-r14
[R15]: #uklib-term_assurance-r15
[R16]: #uklib-term_assurance-r16
[R2]: #uklib-term_assurance-r2
[R3]: #uklib-term_assurance-r3
[R5]: #uklib-term_assurance-r5
[R8]: #uklib-term_assurance-r8
[R9]: #uklib-term_assurance-r9
[REG-R1]: #uklib-reg-r1
[REG-R30]: #uklib-reg-r30
[REG-R32]: #uklib-reg-r32
[REG-R38]: #uklib-reg-r38
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
