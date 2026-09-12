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
- **Projection frequency.** Monthly grid **[std]**. Every piece of intra-year
  contractual structure this product has is monthly — the step-down of the
  decreasing-shape benefit, the FIB instalments, and the premium itself, which is quoted
  and collected per month [S5] [S6] [S8] — so the grid is the frequency the contract is
  written in and no mid-year approximation arises. The assumption tables are quoted
  annually (mortality by attained age, lapse by policy year) and are converted with
  `q_m = 1 − (1 − q)^(1/12)` and `w_m = 1 − (1 − w)^(1/12)` **[std]**, which compound
  back to the annual rate exactly, so the in-force at every anniversary is identical to
  an annual-grid projection of the same table (a useful implementation check — see the
  worked example).
- **Time index.** `t` is 0-based and counts policy **months** from issue: the issue
  month is `t = 0`, the policy year containing month `t` is `t // 12 + 1`, and the frame
  is `t = 0 … N − 1` where `N = 12n` is the number of months and the exclusive end.
  Month `t` runs from time `t` to time `t + 1`: `l(t)` is the in-force at its start,
  start-of-month flows fall at time `t` and end-of-month flows at time `t + 1`. Where
  the notes say "policy year k" they mean the contractual label, i.e. months
  `t = 12(k − 1) … 12k − 1`.
- **Timing conventions [std].** Premiums received at the start of each policy month, in
  advance, and only from policies still in force at that point; maintenance expenses at
  the start of each month; death/TI claims paid at the end of the policy month of death;
  lapses occur at the end of the month, after deaths. Acquisition expenses and initial
  commission at issue (start of `t = 0`).
- **Age basis.** Age nearest birthday at entry, plus curtate policy year — attained age
  in month `t` is `x + t // 12` **[std]**, advancing on the policy anniversary rather
  than monthly, which is what an age-nearest-birthday basis means. (The fetched product
  documents do not state an age basis; UK assured-lives tables are select tables — AM92
  has a 2-year select period, TMNL16/TFNL16 a 5-year select period [R12] — so the
  mortality interface must accept select-by-duration rates.)
- **Currency.** GBP throughout. Benefits are paid in sterling to UK bank accounts
  [S1].
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
  No aggregation logic is specified here.
- **Termination.** All states terminate at the end of the term: cover expires with no
  maturity value, no renewal, and no conversion — there is no US-style post-level-term
  ART tail [S1] [S2] [S6] [S8] [R8]. The projection horizon is exactly `N = 12n` months,
  `t = 0 … N − 1`.
- **Contract boundary.** Premiums are guaranteed, so the insurer has no unilateral
  repricing right and the Solvency UK contract boundary is the full term [R3]: all
  `N` months of premiums and benefits are inside the boundary. (Reviewable-premium
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
| `l(t)` | In-force probability at the start of month t; `l(0) = 1` | monthly recursion |
| `q(t)`, `q_m(t)` | Annual mortality rate (incl. TI acceleration) for the policy year containing month t, and its monthly equivalent | annual lookup, monthly conversion |
| `w(t)`, `w_m(t)` | Annual lapse rate for that policy year, and its monthly equivalent | annual lookup, monthly conversion |
| `D(t)` | Expected deaths/TI claims in month t = `l(t) × q_m(t)` | monthly |
| `DB(t)` | Death benefit payable for deaths in month t (shape-dependent) | monthly (schedule) |
| `idx(t)` | Cumulative indexation factor (1 if option not elected/declined) | on anniversaries; level within the policy year |
| `FIBcum(t)` | Cumulative expected FIB income streams in payment at start of month t = `Σ_{s<t} D(s)` (fib shape) | monthly |
| `CF(t)` | Net liability cash flow of month t (insurer perspective, + = inflow) | monthly |

The FIB in-payment ledger is **not** decremented by mortality after the claim: the
instalments are an annuity-certain to the end of the term regardless of any life
[S6] [S8].

Two of these step on the policy anniversary rather than every month, and it matters
which: `q`, `w`, `idx` and the expense inflation factor are constant through a policy
year, because the mortality table is entered at an attained age that advances on the
anniversary, the lapse table is keyed by policy year, and the indexation offer is an
anniversary event. Only the benefit schedule `B(k)` and the FIB ledger move monthly.

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
| TI acceleration timing | None modeled: death and TI are one decrement, one benefit. Modelling the acceleration on a monthly grid would need a terminal-illness diagnosis basis separate from the mortality table, which the subscriber-restricted tables do not supply, so the payment stays at the month of the combined decrement **[std]** | definition [S1] [S6] [S8]; 16-Series mortality includes TI [R10] |
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

The table is keyed by the contractual policy year; `w(t)` reads the row for policy
year `t // 12 + 1`, so `w(t) = 10%` for the twelve months `t = 0 … 11`. The rate is
annual and the projection decrements by `w_m(t) = 1 − (1 − w(t))^(1/12)` **[std]**.

(Year 3 staying elevated after the 2-year clawback period ends, and the year-5
uptick after the 4-year clawback period ends, echo the post-clawback spike pattern
[R9]; levels are standardized calibrations to be replaced with the user's
experience.)

**Expenses and commission (all levels [std]; structure evidence as cited).**

| Input | Value | Basis |
|---|---|---|
| Initial (acquisition) expense | £150 per policy at issue | **[std]** |
| Initial commission | 150% of annualized premium, paid upfront at issue | upfront pattern ~96% of commission [R9]; level **[std]** |
| Commission clawback | On lapse in months 1–48: clawback of `(48 − months in force)/48` of initial commission, `t + 1` months in force at the end of month `t` (linear, 4-year) — optional module, base model off | clawback periods 2–4 years [R9]; formula **[std]** |
| Renewal commission | 2.5% of premiums from policy year 2 (`t ≥ 12`) | **[std]** |
| Maintenance expense | £30 per policy p.a. — a twelfth of it each month — inflating 3% p.a. on each anniversary | **[std]** |
| Claim expense | £250 per death/TI claim | **[std]** |
| Expense inflation | 3% p.a. flat | **[std]** |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t`, `k` | policy month index, 0-based from issue, t = 0..N−1, N = 12n; the two are the same index and `k` is written where a benefit schedule is meant |
| `y(t)` | policy year containing month t = `t // 12 + 1`; attained age in month t = x + t // 12 (x = issue age) |
| `P_m`, `P_a` | monthly premium = 12.00 (anchor cell) **[std]**; annualized premium = 12 × P_m = 144.00 |
| `q(t)`, `q_m(t)` | annual mortality (incl. TI) rate for policy year y(t), select-adjusted; monthly rate = 1 − (1 − q)^(1/12) **[std]** |
| `w(t)`, `w_m(t)` | annual lapse rate for policy year y(t); monthly rate = 1 − (1 − w)^(1/12) **[std]** (end-of-month, after deaths) **[std order]** |
| `l(t)` | in-force probability at start of month t; l(0) = 1 |
| `D(t)` | expected claims in month t = l(t) × q_m(t) |
| `SA0` | initial sum assured (level/decreasing) |
| `I` | FIB monthly income |
| `j`, `j_m` | decreasing schedule annual rate; j_m = (1+j)^(1/12) − 1 |
| `B(k)` | decreasing-shape benefit after k months (formula below) |
| `idx(t)` | cumulative indexation factor in month t (1 if not indexed); steps on anniversaries |
| `E0`, `e(t)` | initial expense (150); maintenance expense = (30/12) × 1.03^(y(t)−1) per month |
| `c0`, `c_r` | initial commission (1.5 × P_a); renewal commission rate (0.025, from t = 12) |
| `ec` | claim expense (250) |
| `CF(t)` | net cash flow of month t, insurer perspective (+ inflow, − outflow) |

Dimensional check: `q`, `w` are per-annum probabilities and `q_m`, `w_m` per-month
probabilities (all dimensionless); `B`, `SA0` are GBP; `I` is GBP/month and the grid is
monthly, so FIB outgo is one instalment per stream per month and carries no month-count
multiplier; all `CF` components are GBP per month.

### Benefit amount by shape

**Level:** `DB(t) = SA0 × idx(t)`.

**Decreasing** [S1] [S6] [S8]:

    B(k) = SA0 × [(1+j_m)^N − (1+j_m)^k] / [(1+j_m)^N − 1],   B(0) = SA0, B(N) = 0

The schedule steps down monthly, so the balance is constant through month `t` and the
death benefit is that balance exactly:

    DB(t) = B(t)

No mid-year reading is needed. (The whole-year identity `(1+j_m)^12 = 1+j` gives the
anniversary balances in closed form, `B(12u) = SA0 × [(1+j)^n − (1+j)^u] /
[(1+j)^n − 1]`, which is the quickest way to check an implementation's monthly
convention against an annual one.) Numeric anchor (SA0 = 150,000, j = 6%, n = 25):
`B(60) = 150,000 × (1.06^25 − 1.06^5) / (1.06^25 − 1) = 150,000 × (4.291871 −
1.338226) / 3.291871 = £134,588` — the benefit after 5 years. Indexation and the
decreasing shape are not combined **[std scope]** (no fetched insurer offers indexed
decreasing cover).

**Family income benefit** [S2] [S6] [S8]: a death in month k triggers `N − k` monthly
instalments of `I`, in arrears, ending at month N — an annuity-certain independent of
survival. On the monthly grid the instalments are counted one by one: each stream in
payment pays exactly one instalment at the end of each month, the month of death
included, so

    Claims_fib(t) = I × [ D(t) + FIBcum(t) ],   FIBcum(t) = Σ_{s<t} D(s)

and one death in month s generates `N − s` instalments in all, which is the contractual
count with no rounding. (An annual grid has to place the death at mid-year and count
six instalments in the year of death and twelve in each later year; that approximation
is what the monthly grid removes.)

Optional commutation module **[std]**: replace the instalment stream at death with a
lump sum `CV(k) = I × a(N−k)` where `a(m) = [1 − (1+r_c)^(−m/12)] / [(1+r_c)^(1/12) − 1]`
is the m-month annuity-certain factor at the snapshot commutation rate `r_c` = 3%
**[std]** (contractually the insurer reduces the sum of remaining instalments
"fairly and reasonably" [S6] [S8]). On the monthly grid the factor is taken at the exact
death month, `k = t`. Base model: no commutation.

### In-force recursion and processing order

Monthly processing for month t = 0..N−1 **[std]**:

1. **Start of month:** premium income `P_m × idx_p(t) × l(t)` (where `idx_p(t)` is the
   cumulative *premium* indexation factor — equal to 1 in the base run), or
   `12 × P_m × idx_p(t) × l(t)` in the first month of each policy year on an
   annual-mode payer and nil in its other eleven; maintenance expense `e(t) × l(t)`;
   renewal commission `c_r × P_m × idx_p(t) × l(t)` (from t ≥ 12). At t = 0
   additionally `E0` and `c0` (per policy issued, l(0) = 1).
2. **Benefit schedule:** compute `DB(t)` per shape (the month's exact balance `B(t)`
   for decreasing).
3. **End of month — claims:** expected death/TI outgo `DB(t) × D(t)` (level/
   decreasing) or the FIB formula above; claim expense `ec × D(t)`.
4. **End of month — lapses:** applied to survivors of mortality **[std order: death
   before lapse]**; lapse pays nothing (no surrender value [S6] [R8]).
5. **Update:**

       l(t+1) = l(t) × (1 − q_m(t)) × (1 − w_m(t))

6. **Anniversary (if indexation elected):** at each month t with `t mod 12 = 0` and
   t > 0, with acceptance (behavior section),
   `idx(t) = idx(t−1) × (1 + min(max(RPI, 0), 0.10))` and
   `idx_p(t) = idx_p(t−1) × (1 + min(1.5 × increase, 0.15))` [S1] [S2] [S6]; both are
   held level through the other eleven months of the policy year.

At the end of t = N − 1 the projection ends: no maturity payment, no tail states
[S1] [S6] [S8] [R8].

Because `q_m` and `w_m` compound back to `q` and `w` exactly over the twelve months of a
policy year, and because both are constant within the year, the recursion reproduces
`l(12y) = Π_{u<y} (1 − q(u))(1 − w(u))` — the in-force an annual-grid projection of the
same table would report at every anniversary. That identity is the cheapest check on a
monthly implementation, and it holds whatever the decrement levels are.

### Net cash flow

Level/decreasing shapes:

    CF(t) = P_m × idx_p(t) × l(t)                                   (premiums)
          − DB(t) × D(t)                                            (death/TI claims)
          − ec × D(t)                                               (claim expense)
          − e(t) × l(t)                                             (maintenance)
          − c_r × P_m × idx_p(t) × l(t) × 1{t ≥ 12}                 (renewal commission)
          − (E0 + c0) × 1{t = 0}                                    (acquisition)

FIB shape: replace the claims term with `Claims_fib(t)` and add `− ec × D(t)` only in
the month of death. Premiums stop at death, but FIB instalments continue — premium
income always carries `l(t)`, never the FIB ledger.

What the monthly grid settles. An annual grid has to take the decreasing benefit at the
mid-year balance `B(12t + 6)` and to collect a full year's premium in advance from lives
that may leave during the year; the first understates claims slightly and the second
overstates income slightly, and the two are an offsetting pair whose net effect no
annual projection can report. Here neither arises: the benefit is the balance of the
month the claim falls in and the premium is collected month by month from the lives
still in force. An implementation must not carry a further half-year premium adjustment
on top — there is nothing left to adjust for.

### Waiver of premium (optional module, base off)

With `wop = true`, an incapacity state is added: incidence `inc(t)` **[std]**
(no public UK incidence basis for the WOP work-tasks definitions is in the fetched
sources), 26-week deferred period [S1], premiums waived while incapacitated (premium
income multiplied by the active-payer probability), mortality unchanged. The WOP
extra premium and the incidence/recovery basis are both **[std]** placeholders.

On the monthly grid the deferred period is carried explicitly, as `defer` = 6 months
**[std]** — the reading of 26 weeks a monthly grid can express, where an annual one
could only round it to "incidence in year t, waiver from year t + 1". With monthly
incidence and recovery rates `inc_m`, `rec_m` converted as above, the waived fraction
follows

    u(t+1) = u(t)(1 − rec_m) + inc_m × [1 − u(t − defer)] × (1 − rec_m)^defer

— the lives entering waiver this month are those who became incapacitated `defer`
months ago and have not recovered since.

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
  always accept, RPI scenario input flat 3% **[std]**, giving a factor of 1.03 on cover
  and 1.045 on premium at each anniversary (premium factor 1.5 [S1] [S2] [S6]), both
  held level through the twelve months of the policy year that follows.
- **GIO exercise.** Not modeled: exercises create *new* policies at then-current
  rates [S1] [S6] [S8], so they add model points rather than changing this one
  **[std scope]**.

---

## Worked example

Anchor cell: male 35 non-smoker, single life, level shape, `n` = 25 (`N` = 300
months), `SA0` = £150,000, `P_m` = £12.00 **[std]**, monthly premium mode; no
indexation, no WOP, no commutation; base lapse table; no selective-lapse or rebroking
modules. Mortality placeholders `q = 0.00055, 0.00060, 0.00065` for policy years 1, 2
and 3 are **[std] illustrative values in the shape of a non-smoker temporary assurance
table** — they are NOT taken from any CMI table (the current tables are subscriber-only
[R11]; see assumption class (c)). Expenses per the [std] table: `E0` = 150,
`c0` = 1.5 × 144 = 216.00, `e(t)` = (30/12) × 1.03^(y−1) per month, `c_r` = 2.5% from
t = 12, `ec` = 250. Rows are labelled by the 0-based month `t`; policy year
y = t // 12 + 1.

The monthly decrements the first two policy years run on:

| Policy year | `q` | `q_m = 1 − (1 − q)^(1/12)` | `w` | `w_m = 1 − (1 − w)^(1/12)` |
|---|---|---|---|---|
| 1 | 0.00055 | 0.00004584 | 0.10 | 0.00874161 |
| 2 | 0.00060 | 0.00005001 | 0.08 | 0.00692438 |

| t | y | l(t) | Premiums `P_m·l(t)` | Claims `SA0·D(t)` | Claim exp `ec·D(t)` | Maint. + initial exp | Commission | Net CF(t) |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 1.000000 | 12.00 | 6.88 | 0.0115 | 152.50 | 216.00 | −363.39 |
| 1 | 1 | 0.991213 | 11.89 | 6.82 | 0.0114 | 2.48 | 0.00 | +2.59 |
| 11 | 1 | 0.907479 | 10.89 | 6.24 | 0.0104 | 2.27 | 0.00 | +2.37 |
| 12 | 2 | 0.899505 | 10.79 | 6.75 | 0.0112 | 2.32 | 0.27 | +1.45 |
| 24 | 3 | 0.827048 | 9.92 | 6.72 | 0.0112 | 2.19 | 0.25 | +0.75 |

Trace, t = 0 (first month of policy year 1): `D(0) = 1.0 × 0.00004584 = 0.00004584`;
claims = 150,000 × 0.00004584 = 6.88; claim expense = 250 × 0.00004584 = 0.0115;
expenses = `E0` + e(0) = 150.00 + 30/12 = 152.50; commission = `c0` = 216.00;
CF(0) = 12.00 − 6.88 − 0.0115 − 152.50 − 216.00 = −363.39.
Update: `l(1) = 1.0 × (1 − 0.00004584) × (1 − 0.00874161) = 0.991213`.

Trace, t = 12 (first month of policy year 2): premiums = 12.00 × 0.899505 = 10.79;
`D(12) = 0.899505 × 0.00005001 = 0.00004499`; claims = 150,000 × 0.00004499 = 6.75;
claim expense = 0.0112; maintenance = (30/12) × 1.03 × 0.899505 = 2.32; renewal
commission = 0.025 × 10.79 = 0.27; CF(12) = 10.79 − 6.75 − 0.0112 − 2.32 − 0.27 =
+1.45.

**The anniversary check.** `l(12) = 0.899505` and `l(24) = 0.827048` are exactly the
in-force an annual-grid projection of the same table reports at the first and second
anniversaries — `1 × (1 − 0.00055)(1 − 0.10)` and that times
`(1 − 0.00060)(1 − 0.08)` — because `(1 − q_m)^12 = 1 − q` and `(1 − w_m)^12 = 1 − w`
and both rates are constant within the policy year. An implementation whose
anniversary in-force drifts from those figures has the decrement conversion wrong.

Totalled over the policy year, the cash flows are:

| Policy year | Premiums | Claims | Claim exp | Expenses | Commission | Net CF |
|---|---|---|---|---|---|---|
| 1 | 137.24 | 78.65 | 0.13 | 178.59 | 216.00 | −336.13 |
| 2 | 124.67 | 77.94 | 0.13 | 26.75 | 3.12 | +16.73 |
| 3 | 115.19 | 78.02 | 0.13 | 25.46 | 2.88 | +8.70 |

Premium income is below the annual grid's `P_a × l(t)` in every year — 137.24 against
144.00 in year 1 — and that difference is the annual-in-advance bias, now removed
rather than offset: the monthly grid stops collecting from a policy the month it
leaves.

The pattern is characteristic of guaranteed term: a deep new-business strain in the
first month, t = 0 (upfront commission and acquisition expense against one month's
premium [R9]) and thin positive margins thereafter — the level premium prefunds the
rising mortality cost, so early-duration lapses forfeit margin to the insurer while
late-duration lapses relieve it.

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
   claim outgo persists up to `N − 1` months after death — omitting the in-payment
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
  income by mortality or lapse; only *new* claims depend on `l(t)` [S6] [S8]. Paying
  only the instalment falling in the month of death understates the liability by up to
  `N − 1` months of income.
- **Decreasing-schedule conventions.** `j_m = (1+j)^(1/12) − 1` **[std]** vs a
  nominal `j/12` convention changes `B(k)` slightly; state the convention and use
  the `B(60) = £134,588` anchor to validate implementations.
- **Decrement conversion.** Convert the annual table rates with
  `1 − (1 − q)^(1/12)`, not the nominal `q/12`: twelve months of the latter leave
  `(1 − q/12)^12 > 1 − q`, so it **understates** the decrement — materially on the
  10% year-one lapse rate — and it breaks the anniversary identity above, which is the
  symptom to look for. Keep the annual rate as the quantity the tables are read in and
  the monthly one as a derived quantity, so the assumption basis is never restated in
  monthly units.
- **Do not carry annual-grid corrections onto a monthly grid.** The mid-year benefit
  balance for the decreasing shape and the half-year premium adjustment are both
  corrections for an annual step. On this grid the benefit is the month's own balance
  and the premium is collected monthly from the lives still in force, so applying
  either on top double-counts a correction for a bias that is no longer there.
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
