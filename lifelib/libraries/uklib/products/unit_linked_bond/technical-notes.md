# Technical Notes

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03; see `sources.md`).

**Scope note.** These notes specify a reference liability cash-flow projection model for
the standardized composite product defined in `product-spec.md` (same directory). This is
not any single insurer's product. [S#]/[R#] tags refer to the source list in
`_research/unit-linked-bond.md` (carried into `sources.md` here); [REG-R#] tags refer
to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `_research/regulatory-actuarial.md`). **[std]** marks standardizations
introduced for the reference implementation; [unverified] marks claims not confirmed
against a retrieved document. Parameter values are identical to those in
`product-spec.md`; the implementation anchor for mechanics is a single carrier's
KFD + Policy Provisions pair [S1] [S2].

---

## Model scope and conventions

- **Purpose.** Project gross liability cash flows for a single-policy model point of a
  clean-charge onshore unit-linked bond, decomposed in the classic UK way into the
  **unit fund** (the bid value of units, matched by the linked assets) and the
  **non-unit ("sterling") cash flows** accruing to the insurer: charges collected and
  fund-based margins, less expenses and death strain. This decomposition is standard
  UK actuarial practice but is tagged [unverified] as terminology — the IFoA archive
  papers evidencing the "sterling reserve" usage could not be text-extracted [R9];
  the rule-level anchor is the Solvency UK requirement that the best estimate reflect
  *all* cash in- and out-flows [R5 TP 3.2](#uklib-unit_linked_bond-r5) applied to the product cash flows in
  [S1]–[S5]. Reserves are not computed (see Valuation and reserve pointers).
- **Projection frequency.** Monthly **[std]**. The contract accrues the AMC daily
  through the unit price [S2 §5.1.1] and prices funds daily/at least monthly
  [S2 §3.2] [S3 Part E]; the model discretizes to monthly steps with all
  intra-month flows at the conventions below.
- **Timing conventions [std].** Fund growth, tax provision and fund-based charges
  accrue over the month; withdrawals, adviser charges and rider charges are unit
  cancellations at end of month (EOM); decrements (death, surrender) are EOM events
  after cancellations. Settlement frictions (12:00 cut-offs, 2-working-day large
  deals, 28-day PruFund waits, deferral powers [S2 §4, §8] [S5 Q9]) are ignored.
- **Age basis.** Age last birthday (ALB) **[std]**, chosen to index directly into
  single-year-of-age qx vectors of the ONS national life tables used as the [std]
  mortality proxy [REG-R32]. (Contractual age limits are quoted "next birthday" in
  the anchor documents [S1]; the difference is immaterial to a product with a 0.1%
  death strain.)
- **Currency.** GBP. Intermediate values carried at full precision; cash flows
  reported to pence **[std]**.
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
  A "policy" here is the whole bond of 100 identical segments **[std]** (spec
  footnote 3); per-segment values are the bond values ÷ 100 [S1] [S2 §2.4]. No
  aggregation logic is specified.
- **Top-ups.** Excluded from the base projection; a top-up is a new model point with
  its own premium, allowance clock and segments **[std]** (spec footnote 4)
  [R2 per-premium allowance arithmetic](#uklib-unit_linked_bond-r2).

---

## Model point attributes

| Attribute | Type | Example (anchor cell) |
|---|---|---|
| `issue_age` | int (ALB) | 65 **[std]** |
| `sex` | enum {M, F} | M **[std]** |
| `lives` | enum {single} (joint last-death out of scope, spec footnote 1) | single |
| `premium` | currency (single premium, net of set-up adviser charge [S2 §1, §12.2]) | 100,000 **[std]** |
| `n_segments` | int | 100 **[std]** |
| `db_uplift` | factor `u` | 1.001 [S1] [S2]; choice **[std]** |
| `amc_rate` | annual rate `c` | 0.0100 **[std]** |
| `further_costs_rate` | annual rate `f` | 0.0010 **[std]** |
| `tax_provision_rate` | rate `t_pf` | 0.20 **[std]** proxy [R6] |
| `wd_pattern` | enum {none, allowance_5pct, custom} | allowance_5pct **[std]** |
| `oac_rate` | annual rate on unit value (ongoing adviser charge) | 0 (module value 0.005 [S1] [S2 §7.1 example]) |
| `gmdb_flag` | bool (return-of-premium rider [S1] [S2 §5.2, §10] [S5]) | false **[std]** |
| `uf_initial` | currency (premium at issue; >0 for in-force cells) | 100,000 |
| `issue_date` / `policy_month_offset` | date / int | month 1 |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `UF(t)` | Unit fund = bid value of units at end of month t | monthly recursion |
| `l(t)` | In-force probability at end of month t; l(0) = 1 | monthly decrements |
| `y` | Policy year = ceil(t/12); insurance year for allowance tracking [R2] | monthly |
| `CumWD(n)` | Cumulative withdrawals + ongoing/ad hoc adviser charges to end of insurance year n (allowance-relevant [S2 §12.1.1] [S4] [S5 Q15]) | on withdrawal/charge |
| `CumAllow(n)` | Cumulative allowable element = premium × min(n, 20) × 5% [R2] | yearly |
| `ExcessGain(n)` | Excess-event gain at insurance-year end (policyholder-side flag, no insurer cash flow) [R1 s498/s507](#uklib-unit_linked_bond-r1) [R2] | yearly |
| `G(t)` | GMDB guaranteed amount = premium − withdrawals − ongoing/ad hoc adviser charges (if `gmdb_flag`) [S2 §10] | on events |
| `E(t)` | Maintenance expense in month t | monthly |

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited)

In a clean-charge unit-linked bond the guaranteed layer is thin — that is the point
of the design:

| Input | Value | Basis |
|---|---|---|
| Death benefit | `u × UF`, u = 1.001 (sum assured = 100.1% of bid value of units) | [S1] [S2]; u choice **[std]** (spec footnote 6) |
| Surrender value | `UF` (bid value of units; no penalty) | [S4]; composite scope **[std]** (spec footnote 13) |
| Withdrawal machinery | Regular/partial/segment surrender; 12-month regular cap = max(7.5% of plan value, 7.5% of total paid in) incl. ongoing adviser charges | [S1] [S2 §7.1, §7] |
| Charge basis | AMC accrues daily through the unit price; adviser/rider charges by unit cancellation | [S2 §5.1.1, §12] |
| Segmentation | 100 identical policies; premium and units divided equally | count **[std]**; mechanics [S1] [S2 §2.4] |
| Liability cap | Benefits derived from fund assets only; no make-whole on external default | [S2 §3.1.9] [S4] |

### (b) Insurer-discretionary current elements (snapshot)

All revisable by the insurer (AMC increase provisions are documented on the legacy
booklet [S3 Part D]); the model holds the snapshot level:

| Input | Snapshot value | Basis |
|---|---|---|
| AMC `c` | 1.00% p.a. | **[std]** — per-fund AMC rate cards not fetched (research gap 5); only the discount tier table is public [S1] |
| Further costs `f` | 0.10% p.a. (fund-borne, not insurer income) | existence [S1] [S2 §3.1.7]; level **[std]** |
| Fund-size discount | Off (level net AMC assumed) | tiers [S1] [S2 §5.1.4]; scope **[std]** |
| Life-fund tax pass-through `t_pf` | 20% of gross fund return, in-price, neutral to insurer | mechanism [S2 §3.2.1] [S4] [S5 Q15]; rate proxy **[std]** of the policyholder rate [R6] |
| GMDB mortality-factor scale | = monthly mortality rate from the class-(c) basis at attained age (cost-of-insurance style), applied to max(0, G − u×UF) | design [S2 §5.2, §10]; scale **[std]** — factors not published |
| MVR / bonus rates | Not applicable — with-profits and PruFund funds out of scope; see `products/with_profits/` | [S2 §3.3] [S3] |

The `t_pf` proxy deliberately ignores I-E timing detail: actual pass-through
distinguishes income (as received), realised gains (next charge date), an annual
deemed-disposal charge, and full-surrender settlement [S5 Q15] [S4], and the company's
I-E position includes an expense offset and minimum profits test [R6]. The base model
treats collected tax as exactly offsetting tax payable (zero insurer margin impact)
**[std]**.

### (c) Behavioral / experience assumptions (modeler's view)

| Input | Recommended public basis | Basis tags |
|---|---|---|
| Best-estimate mortality | 80% × ONS national life tables qx (single year of age, sex-distinct) **[std]** proxy | [REG-R32]; factor **[std]** |
| Mortality improvement | None in base **[std]**; production overlay "CMI_20xx with long-term rate p% **[std]**" | [REG-R30] |
| Base surrender (full) | [std] table below | **[std]**; design holding period [S1] [S4] [S5] |
| Withdrawal take-up | anchor cell: 5% of premium p.a., monthly | **[std]** (spec footnote 14) [R2] [S1] [S4] [S5] |
| Acquisition expense | £300 per policy at issue | **[std]** |
| Maintenance expense | £60 per policy p.a., inflating 2.5% p.a. | **[std]** |
| Gross fund return scenario `g` | 5.0% p.a. (deterministic base) | **[std]** |

**Honesty note on the mortality basis.** The CMI's current assured-lives tables and
Projections Model are restricted to Authorised Users (subscribers); older
publications are free but current qx cannot be redistributed [R8] [REG-R30]. The
canonical teaching tables (AM92/AF92) show the *shape* an assured-lives basis takes
[REG-R24], and the ONS national life tables are the only fully redistributable UK
mortality source (Open Government Licence; qx by single year of age) [REG-R32] —
hence the [std] proxy above, with the caveat that population mortality is heavier
than insured-lives experience [REG-R32] (the 80% factor is a crude allowance,
**[std]**). Specific CMI assured-lives table names for this product could not be
confirmed from the fetched CMI page and remain [unverified] (research gap 8) [R8].
Mortality is nearly irrelevant to this product — the net amount at risk is 0.1% of
the unit fund in the composite (0.1%–1% across insurers [S1] [S2] [S3] [S4] [S5]) —
unless the GMDB rider is enabled.

Reference base surrender table **[std]** (annual rates; to be replaced by portfolio
experience; shape rationale: the product is designed to be held 5–10 years or more
[S1] [S4] [S5], so surrenders are low early, rise as the advised holding period
completes, and settle at a high ultimate level):

| Policy year | 1 | 2 | 3–5 | 6–10 | 11+ |
|---|---|---|---|---|---|
| Annual full-surrender rate `w_base` | 2% | 3% | 5% | 8% | 10% |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | policy month, t = 1, 2, …; y = ceil(t/12); a = attained age (ALB) = issue_age + y − 1 |
| `P` | single premium (100,000) |
| `UF(t)` | unit fund at end of month t; UF(0) = P |
| `g` | annual gross fund return (0.05); `g_m` = (1+g)^(1/12) − 1 = 0.0040741 (derived) |
| `t_pf` | tax-provision rate (0.20) **[std]** |
| `c`, `f` | AMC (0.0100) and further costs (0.0010), annual; `c_m` = c/12 = 0.0008333, `f_m` = f/12 = 0.0000833 **[std 1/12 accrual convention]** |
| `u` | death-benefit uplift factor (1.001) |
| `W(t)` | regular + one-off withdrawals cancelled at EOM of month t (anchor: 5%×P/12 = 416.67) |
| `AC(t)` | ongoing/ad hoc adviser charges cancelled at EOM (0 in anchor cell) |
| `GC(t)` | GMDB rider charge (0 unless `gmdb_flag`) |
| `TX(t)` | tax provision deducted in month t; `AMC$(t)`, `FC$(t)` monetary AMC/further costs |
| `DS(t)` | death strain per death in month t |
| `q_m(t)` | monthly mortality rate = 1 − (1 − q_a)^(1/12) from the class-(c) basis; `w_m(t)` monthly surrender rate = 1 − (1 − w_ann)^(1/12) |
| `l(t)` | in-force probability at end of month t; l(0) = 1 |
| `E(t)` | maintenance expense = 60/12 × 1.025^(y−1) **[std]** |

Dimension check: `g_m`, `c_m`, `f_m`, `t_pf` are dimensionless per-month rates or
fractions; every product with `UF` is in GBP; `q_m × DS` is GBP per policy-month.
`W`, `AC`, `GC`, `TX`, `AMC$`, `FC$`, `E` are GBP per month.

### Monthly processing order **[std]**

For month t, per policy in force at t−1:

1. Update y, a, E(t).
2. **Fund growth and tax provision** (within unit price [S2 §3.2.1] [S4] [S5 Q15]):
   `G$(t) = g_m × UF(t−1)`;  `TX(t) = t_pf × G$(t)`;
   `UF_g(t) = UF(t−1) + G$(t) − TX(t) = UF(t−1) × (1 + g_m(1 − t_pf))`.
3. **Fund-based charges** (AMC accrues via price [S2 §5.1.1]; further costs
   fund-borne [S2 §3.1.7]):
   `AMC$(t) = c_m × UF_g(t)`;  `FC$(t) = f_m × UF_g(t)`;
   `UF'(t) = UF_g(t) × (1 − c_m − f_m)`.
4. **Unit cancellations (EOM):** withdrawals, adviser charges, rider charge:
   `GC(t) = q_m(t) × max(0, G(t) − u × UF'(t))` if `gmdb_flag` else 0
   (design [S2 §5.2, §10]; scale **[std]**);
   `UF(t) = UF'(t) − W(t) − AC(t) − GC(t)`.
   Enforce the product cap: rolling-12-month W + AC ≤ max(0.075 × UF, 0.075 × P)
   [S1] [S2 §7.1].
5. **Death strain per death:**
   `DS(t) = (u − 1) × UF(t) + max(0, G(t) − u × UF(t)) × 1{gmdb_flag}`
   — the sum assured is u × UF funded by cancelling the whole unit fund, so the
   non-unit cost is the 0.1% uplift [S1] [S2] plus any GMDB in-the-money amount
   [S2 §10] [S5].
6. **Decrements (EOM), deaths before surrenders [std]:**
   `l(t) = l(t−1) × (1 − q_m(t)) × (1 − w_m(t))`.
   Surrender pays `UF(t)` by cancelling all units — no non-unit cash flow (clean
   design [S4]; spec footnote 13) — but extinguishes all future margins.
7. **Allowance tracker (insurance-year end, policyholder side only):**
   `CumAllow(n) = P × min(n, 20) × 0.05` [R2];
   `ExcessGain(n) = max(0, CumWD(n) − CumAllow(n) − Σ prior excess gains)`
   [R1 s498/s507](#uklib-unit_linked_bond-r1) [R2]. Generates **no insurer cash flow**; feeds behavior only.
   Chargeable events on death/full surrender follow s484/s491 [R1] and are likewise
   policyholder-side (the insurer issues certificates [S5 Q15]).

The core unit-fund recursion (anchor cell: AC = GC = 0):

    UF(t) = UF(t−1) × (1 + g_m(1 − t_pf)) × (1 − c_m − f_m) − W(t)

### Non-unit (insurer) cash flow extraction

Per policy in force at t−1, before survivorship weighting:

| Cash flow | Formula | Sign |
|---|---|---|
| AMC margin | AMC$(t) = c_m × UF_g(t) | + |
| GMDB rider charge | GC(t) (0 in base) | + |
| Set-up adviser charge / commission | 0 — post-RDR adviser charges are pass-throughs facilitated by unit cancellation [S1] [S2 §12] [S4] | 0 |
| Maintenance expense | E(t) | − |
| Acquisition expense (t = 0) | 300 **[std]** | − |
| Death strain (per death) | DS(t) | − |
| Further costs FC$(t) | pass-through to fund costs — excluded from insurer margin **[std]** | 0 |
| Tax provision TX(t) | pass-through to corporation tax — neutral **[std]** (class (b) note) [R6] | 0 |
| Surrender / withdrawal payments | funded by unit cancellation — no non-unit flow (clean design) [S4] | 0 |

Aggregate expected cash flows multiply each row by the in-force factor: AMC, GC and
expenses by l(t−1); death strain by l(t−1) × q_m(t); nothing by surrenders (their
non-unit flow is zero) **[std timing]**. The expected net non-unit cash flow:

    NUCF(t) = l(t−1) × [ AMC$(t) + GC(t) − E(t) − q_m(t) × DS(t) ]  −  300 × 1{t=0}

Because AMC$(t) ≈ c_m × UF and DS(t) ≈ 0.001 × UF, the insurer's result is a
fund-based margin stream: proportional to the unit fund and to persistency, with
mortality contributing only ~0.001 × q of the fund per year. Lapse/withdrawal
behavior, not mortality, dominates value. Future margins typically exceed future
costs, so the non-unit best estimate is commonly negative (an asset-like offset to
the unit reserve) [unverified as standard-practice terminology — see scope note; the
rule anchor is R5 TP 3.2].

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; no public UK bond
persistency study was fetched (calibration is portfolio-specific).

- **Withdrawal take-up [std].** `wd_pattern = allowance_5pct`: W(t) = 0.05 × P / 12
  every month. Rationale: the 5%/20-year tax-deferred allowance [R2] is the pattern
  every fetched KFD leads with [S1] [S4] [S5], it sits inside the 7.5% product cap
  [S2 §7.1], and adviser charges consume the same allowance [S2 §12.1.1] [S5 Q15] —
  so rational take-up gravitates to 5% inclusive of charges. Sensitivity: `none`
  (accumulation cell) and `custom`.
- **Base surrender [std].** `w_base(y)` per the class-(c) table, converted monthly.
- **Dynamic surrender multiplier — market performance [std].**
  `M_perf(t) = min(2.0, 1 + 2.0 × max(0, g_ref − R_12m(t)))`,
  where `R_12m` is the trailing 12-month gross fund return and `g_ref` = g (5%).
  Poor recent performance raises surrender; base deterministic run has
  R_12m = g_ref so M_perf = 1.
- **Allowance-exhaustion step [std].**
  `M_allow(y) = 1.5 for y ≥ 21, else 1.0`. After 20 insurance years the cumulative
  allowance is fully drawn under the anchor withdrawal pattern [R2]; continued
  withdrawals then generate immediate excess-event gains [R1 s507](#uklib-unit_linked_bond-r1), pushing
  policyholders toward full surrender (or advice-driven restructuring).
- **Total surrender.** `w_ann(y,t) = min(0.35, w_base(y) × M_perf(t) × M_allow(y))`
  **[std cap]**.
- **Segment vs part-surrender election.** Whether a policyholder cashes whole
  segments or part-surrenders across all segments changes their tax [S1] [S4]
  [S5 Q12] [R1 s484/s498](#uklib-unit_linked_bond-r1), not the insurer's cash flow (both cancel the same unit
  value) — carried as a model note only **[std]**.
- **No paid-up state.** Single-premium product; no premium obligation exists
  [unverified as an explicit statement; consistent with S1–S5].

---

## Worked example

Anchor cell: male 65, P = £100,000, 100 segments (£1,000 each), u = 1.001,
c = 1.00%, f = 0.10%, t_pf = 20%, g = 5.0% p.a., W = £416.67/month (5% of premium
p.a. [R2 allowance](#uklib-unit_linked_bond-r2)), AC = GC = 0; all parameters **[std]** per the tables above.
Derived monthly rates: g_m = 0.0040741; g_m(1−t_pf) = 0.0032593; c_m = 0.0008333;
f_m = 0.0000833. Placeholder mortality for the year: q_a = 1.0% **[std order-of-
magnitude placeholder consistent with the class-(c) proxy]**, q_m = 0.000837.
Figures in GBP, displayed to pence, full precision carried.

| t | UF(t−1) | Gross return G$ | Tax TX | AMC$ | FC$ | W | UF(t) |
|---|---|---|---|---|---|---|---|
| 1 | 100,000.00 | 407.41 | 81.48 | 83.60 | 8.36 | 416.67 | 99,817.30 |
| 2 | 99,817.30 | 406.67 | 81.33 | 83.45 | 8.35 | 416.67 | 99,634.17 |
| 3 | 99,634.17 | 405.92 | 81.18 | 83.30 | 8.33 | 416.67 | 99,450.61 |
| … | … | … | … | … | … | … | … |
| 12 | 97,966.60 | 399.13 | 79.83 | 81.90 | 8.19 | 416.67 | 97,779.14 |
| **Yr 1** | — | **4,839.44** | **967.89** | **993.10** | **99.31** | **5,000.00** | **97,779.14** |

Trace, month 1: G$ = 0.0040741 × 100,000 = 407.41; TX = 0.20 × 407.41 = 81.48;
UF_g = 100,325.93; AMC$ = 0.0008333 × 100,325.93 = 83.60; FC$ = 8.36;
UF' = 100,233.96; UF(1) = 100,233.96 − 416.67 = 99,817.30.
Reconciliation, year 1: 100,000 + 4,839.44 − 967.89 − 993.10 − 99.31 − 5,000.00
= 97,779.14. ✓ Per segment: 977.79.

Insurer-side extraction, year 1 (per policy, survivorship factors ≈ 1 at this q/w):

- AMC margin collected: **+993.10**
- Maintenance expense (£60, year 1): **−60.00**
- Expected death strain: Σ q_m × 0.001 × UF(t) = **−0.99**
  (per actual death at month 12 the sum assured would be 1.001 × 97,779.14
  = 97,876.92, of which 97,779.14 is funded by cancelling units — strain 97.78)
- Tax provision (967.89) and further costs (99.31): pass-throughs, nil margin **[std]**
- **Net non-unit cash flow ≈ +932.11** (acquisition expense −300 falls at issue)

Policyholder-side check (no insurer cash flow): year-1 withdrawals 5,000 =
allowable element 100,000 × 1/20 = 5,000 [R2] — no excess event; unused allowance
carried forward is nil, and the 7.5% product cap (7,500 on paid-in) is not breached
[S2 §7.1].

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers
consume them and are cited, not reproduced:

- **Solvency UK technical provisions.** TP = best estimate + risk margin [R5 TP 2.4](#uklib-unit_linked_bond-r5);
  BE = probability-weighted average of future cash flows discounted at the risk-free
  term structure, gross of reinsurance, covering *all* cash in- and out-flows
  [R5 TP 3.1, 3.2](#uklib-unit_linked_bond-r5). For this product the natural presentation is unit reserve =
  UF(t) (replicated by the linked assets; cf. the TP 2.5 replication rule [R5]) plus
  the non-unit BE of the NUCF stream above — commonly negative [unverified as
  terminology; R9 archive papers not extractable].
- **Risk margin.** Reformed Solvency UK cost-of-capital formula: CoC = 4%, risk
  taper λ = 0.9 (floor 0.25) for long-term business, on the notional SCR runoff
  [R5 TP 1.2, 4A.1](#uklib-unit_linked_bond-r5) [REG-R4]. SCR aggregation is cited-not-specified in this library.
- **Matching adjustment / TMTP.** Not relevant: unit-linked bond cash flows are
  neither MA-eligible annuity-style liabilities nor pre-2016 back-book quantities in
  this composite (new-business model) — no [REG] layer is applied.
- **IFRS 17.** UK-adopted IFRS 17 (effective 1 January 2023) is the accounting frame
  [REG-R38]; a unit-linked bond is a candidate for the variable fee approach as
  direct-participation business [mechanics unverified — general knowledge; flagged
  as such in the reference library narrative]. The fulfilment-cash-flow engine is
  the same projection.
- **Standards for the modeling work.** TAS 100 v2.0 (effective 1 July 2023, all
  technical actuarial work; Principle 5 covers models) [R7] [REG-R33 same standard](#uklib-reg-r33);
  TAS 200 v2.0 (insurance work, effective 1 January 2025) [REG-R34].

---

## Key sensitivities and model risks

Dominant assumptions, in order, for a fund-margin product:

1. **Surrender and withdrawal behavior.** Every margin line is proportional to the
   unit fund *and* persistency; surrender costs nothing at the point of exit (SV =
   UF) but truncates the entire future AMC stream. The [std] base table, the
   performance multiplier and the year-21 allowance step are the first assumptions
   to sensitivity-test — no public UK bond persistency study backs them.
2. **Fund return level and path.** AMC income scales with UF, so the liability model
   inherits full market beta on the margin stream; a −20% market move cuts the
   margin base ~20% and (via M_perf) raises surrenders simultaneously.
3. **AMC snapshot vs expense inflation.** The 1.00% **[std]** AMC is a snapshot of a
   discretionary element (per-fund rate cards not public — research gap 5 [S1]);
   maintenance expenses inflate at 2.5% **[std]** while the margin is
   proportional-to-fund — small-fund cells go margin-negative late in life.
4. **Tax pass-through neutrality.** The 20%-of-gross-return in-price proxy **[std]**
   assumes collected tax exactly equals tax payable; the true I-E position has
   timing (deemed disposals, realised-gain charge dates [S5 Q15] [S4]) and base
   differences (expense relief, minimum profits test [R6]) that create insurer-side
   tax strain or float not captured here.
5. **Mortality — only if GMDB is enabled.** Base death strain is 0.001 × UF (≈ £1
   p.a. expected per £100k at q = 1%): negligible. With the return-of-premium rider
   the strain becomes market-contingent (max(0, G − u×UF)) and the unpublished
   charge scale [S2 §5.2] is a [std] guess — enable only with its own sensitivity
   set [S1] [S2 §10] [S5].

Known modeling pitfalls:

- **Charge-base ordering.** AMC accrues on the post-growth, pre-cancellation fund
  (in-price accrual [S2 §5.1.1]). Charging c_m on UF(t−1) or after withdrawals
  changes the margin by ~½ month's growth/withdrawal — small monthly, systematic
  over decades.
- **Counting pass-throughs as margin.** Further costs [S1] [S2 §3.1.7] and the tax
  provision [S4] [S5 Q15] reduce the unit fund but are not insurer income; booking
  them as margin overstates NUCF by ~107% of the AMC in the anchor cell (year-1
  tax provision 967.89 ≈ 97% and further costs 99.31 ≈ 10% of the 993.10 AMC).
- **Treating the 5% allowance as a product feature.** It is policyholder tax
  machinery [R1] [R2]: it never caps what can be withdrawn (the product cap is 7.5%
  [S2 §7.1]) and generates no insurer cash flow. Model it in behavior only.
- **Adviser charges are not insurer income.** Post-RDR set-up/ongoing/ad hoc adviser
  charges are facilitated pass-throughs by unit cancellation [S2 §12] [S4]; they
  reduce UF and consume allowance but add nothing to NUCF.
- **Segment-level granularity.** Modeling at bond level is exact only while all 100
  segments stay identical; segment surrenders break symmetry. The composite keeps
  bond-level modeling and notes the approximation **[std]**.
- **Smoothed funds must not be bolted on.** PruFund EGR/smoothing-limit mechanics
  [S2 §3.3.7–3.3.10] and MVR-bearing with-profits funds [S3] change the unit-price
  dynamics and add guarantee costs; they belong to the with-profits reference
  product (`products/with_profits/`), not this recursion.
- **Uplift factor slip.** 100.1% vs 101% [spec footnote 6] is a ×10 difference in
  death strain; keep `u` a parameter, never a hard-coded 1.001.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-unit_linked_bond-r1
[R2]: #uklib-unit_linked_bond-r2
[R5]: #uklib-unit_linked_bond-r5
[R6]: #uklib-unit_linked_bond-r6
[R7]: #uklib-unit_linked_bond-r7
[R8]: #uklib-unit_linked_bond-r8
[R9]: #uklib-unit_linked_bond-r9
[REG-R24]: #uklib-reg-r24
[REG-R30]: #uklib-reg-r30
[REG-R32]: #uklib-reg-r32
[REG-R34]: #uklib-reg-r34
[REG-R38]: #uklib-reg-r38
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
