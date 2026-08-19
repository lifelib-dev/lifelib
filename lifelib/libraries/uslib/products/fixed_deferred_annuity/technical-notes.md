# Technical Notes

**Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope note.** These notes specify a reference liability cash-flow projection model for
the standardized composite product defined in `product-spec.md` (same directory). This is
not any single insurer's product. [S#]/[R#] tags refer to the source list in
`_research/fixed-deferred-annuity.md`; [REG-R#] tags refer to the cross-product
reference library `references/regulatory-and-actuarial-references.md`, whose shared
R-numbering now runs **R1–R157** with most of the **R73–R149** block unused (provenance:
`_research/regulatory-actuarial.md` for R1–R34,
`_research/regulatory-actuarial-annuities.md` for R35–R72, and the AP&P Manual appendix
extractions `_research/appp-ag33.md`, `appp-ag35.md`, `appp-a820-a821-a822.md` and
`appp-a585-a250-a255-a270.md` for R151–R157, all accessed **2026-08-06**).
**[std]** marks
standardizations introduced for the reference implementation. **Parameter values are
identical to those in `product-spec.md`.** This is the deferred annuity base chassis:
the **fixed-indexed annuity** notes reference the surrender-benefit composition order and
the Model #805 floor construction below rather than restating them, but restate — with
FIA-specific parameters — the account-value roll-forward (index-credit driven), the MVA
family, the death benefit and the lapse architecture; do not carry this file's recursions
or rates into an FIA model unexamined. The **variable annuity** notes do not, and must
not — a VA's separate account is
outside Model #805, which reaches only a VA fixed account via Model #250 §7.B
[REG-R42] [REG-R43].

---

## Model scope and conventions

- **Purpose.** Project gross liability cash flows (single premium in; free withdrawals,
  excess withdrawals, full surrenders, death benefits, annuitization transfers, and
  expenses out) for a single-contract model point of a 5-year MYGA with a market value
  adjustment. Reserves are **not** computed (see Valuation and reserve pointers).
- **Projection frequency: monthly **[std]**.** The contract credits interest **daily**,
  quoted as an annual effective rate [S4] [S5] [S16], and surrender charges/MVA step on
  **contract-year** boundaries [S8] [S10]. Monthly is the coarsest grid resolving both: it
  hits every contract anniversary exactly, and it resolves the 30-day guarantee-period-end
  window and the shock-lapse boundary to within one step. Finer grids buy nothing on a
  book-value chassis with no daily-valued index.
- **Crediting discretization.** Monthly compounding at `(1 + i_cr)^(1/12)`. Because the
  declared rate is an *effective annual* rate under both conventions, twelve monthly factors
  reproduce the annual accretion **exactly** — the discretization affects only the placement
  of interest *within* a month. Do not additionally compound daily; document the convention
  when reconciling to an admin system.
- **Timing.** Elective transactions (withdrawals, owner-elected surrenders, annuitization
  elections) at the **beginning of the policy month (BOM)**; interest credited at **end of
  month (EOM)**; decrements applied at **EOM** **[std]**, with decrement benefits valued on
  the post-crediting `AV(t)`.
- **Age basis: age nearest birthday (ANB) **[std]**.** The VM-22 prescribed mortality basis
  (2012 IAM Basic with Scale G2 and the Table 6.7 factors) is stated ANB, and the Valuation
  Manual supplies the ALB conversion
  `q(x)_ALB = [q(x)_ANB + (1 − q(x)_ANB) × q(x+1)_ANB] / (2 − q(x)_ANB)` rather than a native
  ALB table [R2 §6.B.8](#uslib-fixed_deferred_annuity-r2) [R9]; the SOA/LIMRA fixed-rate deferred surrender study is also ANB,
  with a Balducci exposure adjustment [R8].
- **Model points.** Single-contract model points on an expected (probability-weighted) basis:
  an in-force factor `l(t)` multiplies per-contract cash flows. Grouping is a caller concern.
- **Contract-year indexing.** `y(t) = ceil(t / 12)`; anniversaries at `t = 12, 24, …`.
  Guarantee period `n = 5`, so the initial guarantee and surrender charge periods both end at
  `t = 60`.
- **Rounding.** Full precision internally; cash flows reported to cents **[std]**.

---

## Model point attributes

| Attribute | Type | Example (anchor cell) |
|---|---|---|
| `issue_age` | int (ANB) | 60 |
| `sex` | enum {M, F} | M |
| `tax_status` | enum {NQ, IRA, Roth, inherited} | NQ **[std]** |
| `premium` | currency | 100,000 [S11 rate band ≥$100,000] |
| `issue_date` | date | contract month 0 |
| `guarantee_period_years` | int | 5 [S10] [S11] |
| `declared_rate_initial` | rate p.a. | 0.0445 [S11] |
| `gmir` | rate p.a. | 0.0025 [S11] |
| `gmsv_rate` (`i_nf`) | rate p.a. | 0.0280 [S11] |
| `sc_schedule_initial` | vector by contract year | (0.09, 0.08, 0.07, 0.06, 0.05) [S10] |
| `sc_schedule_renewal` | vector by contract year | (0.05, 0.04, 0.03, 0.02, 0.01) [S2] |
| `renewal_architecture` | enum {`rollover`, `annual_redeclare`} | `rollover` (Camp A) **[std]** |
| `free_wd_rule` | enum {`pct_av`, `interest_only`, `greatest_of`} | `pct_av` at 10% [S10] |
| `free_wd_mva_exempt` | bool | True **[std]** (False = the registered-contract convention [S3] [S4]) |
| `mva_family` | enum {`geometric`, `linear_duration`, `declared_differential`} | `linear_duration` [S8] [S9] |
| `mva_cap_rule` | enum {`sym_sc`, `min_sc_interest`, `asym_sc_snfl`, `gmir_floor`, `none`} | `sym_sc` [S2] |
| `mva_ref_yield_at_issue` (`i0`) | rate p.a. | 0.0500 **[std]** |
| `mva_period_years` | int | 5 (= surrender charge period) [S8] [S11] |
| `mgsv_withdrawal_convention` | enum {`gross`, `net_of_charges`} | `gross` [S11] |
| `mgsv_annual_charge` | currency p.a. | 0.00 [S11]; statutory max 50.00 [R1] |
| `premium_tax_rate` | rate | 0.00 **[std]** |
| `av_initial`, `mgsv_initial`, `tax_basis_initial` | currency | 100,000 / 87,500 / 100,000 |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `AV(t)` | Account value at end of policy month `t` | monthly recursion |
| `MGSV(t)` | Model #805 minimum guaranteed surrender value at end of month `t` | monthly recursion |
| `FWB(y)` | Free-withdrawal base fixed at the start of contract year `y` | each anniversary |
| `FW(t)` | Unused free-withdrawal allowance remaining in contract year `y(t)` | on withdrawal / anniversary |
| `i_cr(t)` | Declared credited rate in force | at each guarantee-period boundary |
| `gp_end(t)` | Months remaining in the current guarantee period | monthly |
| `sc_clock(t)` | Months elapsed in the current surrender-charge schedule | monthly (resets on renewal under `rollover`) |
| `i0_locked` | MVA reference yield locked at the start of the current guarantee period | each renewal |
| `basis(t)` | Investment in the contract (IRC §72 tax basis) | on withdrawal [R6] |
| `l(t)` | In-force probability at end of month `t`; `l(0) = 1` | monthly decrements |

---

## Assumption inputs

Three classes are distinguished explicitly and must never be blended in a parameter file.

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| Surrender charge schedule, initial term | 9%, 8%, 7%, 6%, 5%; 0% from year 6 | [S10] |
| Surrender charge base | amount in excess of the free allowance | [S8] [S9] |
| Free-withdrawal allowance | 10% of premium (year 1); 10% of AV at the last anniversary (years 2+) | [S10] |
| Free amount exempt from charge **and** MVA, incl. at full surrender | yes | [S8] [S11] |
| MVA formula | `μ = (i0 − it) × T` | [S8] [S9] |
| MVA cap | symmetric at the surrender charge amount | [S2] |
| MVA excluded from | death benefit, 30-day window, annuitization, RMDs, waiver withdrawals | [S2] [S4] [S5] [S8] [S13] [S16] |
| GMIR (floor on any declared rate) | 0.25% | [S11] |
| GMSV rate `i_nf` | 2.80% | [S11] |
| Model #805 net consideration ratio | 87.5% of gross considerations | [R1 §4.A(2)](#uslib-fixed_deferred_annuity-r1) [REG-R42] |
| Model #805 indexed-rate corridor | `min(3.00%, round(5-yr CMT, 1/20%) − 1.25%)`, floor **0.15%** | [R1 §4.B](#uslib-fixed_deferred_annuity-r1) [REG-R42] |
| Model #805 annual contract charge (max) | $50 p.a., accumulated at `i_nf` | [R1 §4.A](#uslib-fixed_deferred_annuity-r1) [REG-R42] |
| Death benefit | full account value; no charge, no MVA; never below the cash surrender benefit | [S1] [S2] [S13] [R1 §6](#uslib-fixed_deferred_annuity-r1) |
| 30-day guarantee-period-end window | full account value, no charge, no MVA | [S1] [S2] [S5] [S6] |
| Contract fees | none | [S5] [S10] [S13] [S16] |

### (b) Insurer-declared current elements (snapshot; non-guaranteed under ASOP 2 [REG-R26])

| Input | Value | Basis |
|---|---|---|
| Initial declared rate `i_cr`, months 1–60 | **4.45%** effective annual | [S11] (eff. 09/22/25, payments ≥$100,000; 4.10% under $100,000) |
| Renewal declared rate | `i_cr^ren(t) = max(GMIR, MR(t) − s_ren)` | rule **[std]**; discretion + GMIR floor [S1] [S2] [S11] [S16] |
| Renewal spread `s_ren` | 0.00% base run; 1.00% scenario | **[std]** (a) |
| Renewal surrender charge schedule | 5%, 4%, 3%, 2%, 1% | [S2]; adoption **[std]** |
| Attained-age cap on renewal charge | 4% at 94, 3% at 95, 2% at 96, 1% at 97, 0% at 98–100 | [S1] [S2] |
| MVA reference yield path `it` | exogenous scalar input series | **[std]**; index choice is state-filed [S8] [S12] |

The renewal surrender charge schedule and its attained-age cap are printed as **contract
terms** in [S1] [S2], not as declared elements; they are listed in (b) only because they
attach at a renewal the insurer also re-rates. Load them from the guaranteed-element file
and treat only the renewal *rate* as non-guaranteed.

(a) There is no public evidence on renewal-rate setting: one registered prospectus "observes
no specific formula" [S3] and the other "observes no specific method", both citing
fixed-income yields, competitive considerations, administrative costs and general economic
trends [S3] [S4]. The base run sets `s_ren = 0` so the credited rate equals the competitor rate
and the dynamic-lapse term is exactly zero — the same discipline the UL notes use. The
1.00% scenario exercises the dynamic term. Renewal declarations are non-guaranteed
elements: ASOP 2's scope expressly covers fixed deferred annuities [REG-R26].

### (c) Behavioral / experience assumptions (modeler's view; public bases recommended)

| Input | Recommended public basis | Basis tags |
|---|---|---|
| Mortality | `q_x^(2012+n) = q_x^(2012) × (1 − G2_x)^n × F_x` — 2012 IAM **Basic** Table (VM-M §2.C) with Projection Scale G2 (VM-M §1.J.1.c) and the VM-22 Table 6.7 factors `F_x` | [R2 §6.B.8](#uslib-fixed_deferred_annuity-r2) [R9] [REG-R59] |
| `F_x`, male, no guaranteed living benefit (selected) | ≤52 120.0%; 60 101.0%; 65 101.0%; 70 106.8%; 75 108.0%; 80 108.0%; 85 109.2%; 87+ 110.0% | [R2 Table 6.7](#uslib-fixed_deferred_annuity-r2) |
| Base lapse | VM-22 Table 6.5 (fixed annuities, no GLB), mapped to the 5-year architecture below | [R2] [REG-R36] |
| Base-lapse experience corroboration | SOA/LIMRA 2023–2024 Fixed-Rate Deferred Annuity Surrender Study — 24 companies, ~65% of industry new sales, ~4.8m contracts and $612bn of surrender exposure, >567,000 surrenders | [R8] [REG-R63] |
| Dynamic lapse | VM-22 §6.B.5 functional form, re-parameterized for best estimate | [R2]; parameters **[std]** |
| Partial withdrawal | 0% in the base run **[std]**; variant = VM-22 Table 6.2 (Accumulation, **Qualified**): ≤59 1.65%, 60–64 2.10%, 65–69 2.35%, 70–74 3.95%, 75–79 4.80% | [R2]; see model-risk note (b) |
| Annuitization take-up | 1.0% of in-force at each guarantee-period-end window; 0% otherwise **[std]** | rationale (c) |
| Acquisition commission | 2.00% of premium, paid at issue **[std]** | (d) |
| Maintenance expense | $50 per contract per year, 1/12 monthly, inflating 2.5% p.a. **[std]** | anchored on [R2 §6.B.3](#uslib-fixed_deferred_annuity-r2) |
| Premium tax | 0% **[std]** | spec footnote 3 [S3] [S16] |

(b) The research file recorded VM-22 Table 6.2 only for the **Qualified** column, and the
80-and-over row was truncated in text extraction [R2]. The anchor cell is non-qualified,
so using these rates is a proxy — hence the 0% base run. Do not present the qualified
table as a non-qualified assumption without re-reading VM-22.

(c) No public annuitization take-up study for deferred annuities was located: the SOA's
individual annuity experience index catalogues payout mortality, FIA behavior, fixed-rate
deferred surrender and VA behavior studies, but no annuitization-election series
[REG-R65]. VM-22 prescribes **0% annuitization at all projection intervals** for the
standard projection [R2 §6.B.6](#uslib-fixed_deferred_annuity-r2) — a deliberate statutory simplification, not an
experience estimate. The **[std]** 1.0%-at-the-window assumption reflects that income
options are only offered after contract year 1 and are elected at the guarantee-period
window [S1] [S2] [S5]. No annuitization bonus exists on this chassis (spec footnote 21).

(d) No retrieved document discloses MYGA commission. 2.00% of premium is a pure modeling
assumption. VM-22 prescribes `$35 × 1.025^(valuation-year offset)` per contract for
contracts the company does **not** administer [R2 §6.B.3](#uslib-fixed_deferred_annuity-r2); the $50 maintenance figure is a
[std] uplift of that anchor to a self-administered block.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy month index, `t = 1, 2, …`; `y = y(t) = ceil(t/12)` contract year |
| `n` | guarantee period in years (5); the surrender charge and MVA periods equal it |
| `P` | single purchase payment (100,000) |
| `i_cr(t)` | declared credited rate in force, effective annual |
| `f(t)` | monthly crediting factor = `(1 + i_cr(t))^(1/12)` |
| `i_nf` | GMSV / minimum-nonforfeiture accumulation rate (0.0280); `g = (1 + i_nf)^(1/12)` |
| `sc(y)` | surrender charge rate in contract year `y` of the current schedule |
| `FWB(y)` | free-withdrawal base: `P` for `y = 1`, else `AV(12(y−1))` [S10] |
| `FW(t)` | unused free allowance in contract year `y(t)`; reset to `0.10 × FWB(y)` at each anniversary |
| `W(t)` | **gross** amount removed from the account value at BOM of month `t` |
| `E(t)` | amount exposed to charge and adjustment = `max(0, W(t) − FW(t))` |
| `μ(t)` | MVA rate (signed, dimensionless) |
| `M(t)` | MVA amount (signed currency) |
| `C(t)` | surrender charge amount (currency, ≥ 0) |
| `AV'(t)` | account value after the BOM transaction, before crediting |
| `SV(t)` | gross surrender value before the nonforfeiture floor |
| `SB(t)` | surrender benefit actually paid |
| `MGSV(t)` | minimum guaranteed surrender value (Model #805 floor); the specimen [S11] calls it the "GMSV", `products/fixed_indexed_annuity/` the "guaranteed minimum value (`MGV`)" — one concept |
| `q(t)`, `w(t)` | monthly mortality and monthly total surrender rates |
| `a(t)` | monthly annuitization election rate |
| `l(t)` | in-force probability at end of month `t` |

Dimensional check: `μ(t)` and `sc(y)` are both pure rates multiplying the same currency
base `E(t)`; `M(t)`, `C(t)`, `AV(t)`, `MGSV(t)` and every ledger line are currency.
`T(t)` in the MVA is in years, so `(i0 − it) × T` is `rate × years` — dimensionless only
because it is the **first-order duration approximation** of the geometric factor
`[(1+i0)/(1+it)]^T − 1` (see MVA families).

### Monthly processing order

At month `t` (BOM steps 1–5, EOM steps 6–8):

1. **Roll counters.** Set `y = y(t)`. If `t ≡ 1 (mod 12)` (a contract anniversary has just
   passed), reset `FWB(y)` and `FW = 0.10 × FWB(y)` [S10].
2. **Guarantee-period boundary.** If the previous month ended a guarantee period
   (`t − 1 ≡ 0 mod 12n`): apply the 30-day window (full account value available, no charge,
   no MVA [S1] [S2]); redeclare `i_cr`; under `rollover`, reset `sc_clock` and start the
   renewal surrender charge and MVA schedule, and re-lock `i0` at the current reference
   yield [S2] [S11]; under `annual_redeclare`, set `sc(·) ≡ 0` and `μ ≡ 0` permanently and
   redeclare the rate each anniversary thereafter [S13].
3. **Elective withdrawal.** Compute `E(t)`, `C(t)`, `M(t)` (below); reduce `FW` by
   `min(W(t), FW)`; set `AV'(t) = AV(t−1) − W(t)`; emit the cash flow `W(t) + M(t) − C(t)`.
4. **Annuitization election** (only in a 30-day window, `t > 12`): a fraction `a(t)` of
   in-force transfers `AV'(t)` to the payout model (full account value in the window
   [S1] [S2]).
5. **Update the tax basis** for IRC §72 reporting: withdrawals are income-first, taxable to
   the extent `AV` (gross of surrender charge) exceeds `basis`; `basis` is reduced only by
   the non-taxable remainder [R6 §72(e)(3)(A)](#uslib-fixed_deferred_annuity-r6) [REG-R55]. This is a reported quantity, not a
   liability cash flow.
6. **Credit interest.** `AV(t) = AV'(t) × f(t)`.
7. **Roll the nonforfeiture floor.**
   `MGSV(t) = [ MGSV(t−1) − d(t) − c(t) ] × g`
   with `d(t) = W(t)` under the `gross` convention [S11] or `W(t) + M(t) − C(t)` under
   `net_of_charges` [S9], and `c(t)` the monthly slice of the annual contract charge
   ($0 representative, $50 p.a. statutory maximum [R1] [S11]).
8. **Decrements.** Deaths at `q(t)`, then surrenders at `w(t)` on survivors **[std order]**:
   `l(t) = l(t−1) × (1 − a(t)) × (1 − q(t)) × (1 − w(t))`.

With no withdrawals, steps 3–8 collapse to the core recursion:

    AV(t) = AV(t−1) × (1 + i_cr(t))^(1/12)                                [S4] [S5] [S16]
    MGSV(t) = MGSV(t−1) × (1 + i_nf)^(1/12)                               [R1] [S11]

with `AV(0) = P` [S5] [S10] [S16] and `MGSV(0) = 0.875 × P` [R1 §4.A(2)](#uslib-fixed_deferred_annuity-r1) [S11].

### Surrender benefit — the exact composition order

The order is **account value → MVA → surrender charge → nonforfeiture floor**, and it is
not interchangeable: both `M` and `C` are computed on `E(t)` *before* either is deducted
[S8]. For a full surrender at end of month `t`:

    E(t)  = AV(t) − FW(t)                                                 [S8] [S11]
    C(t)  = sc(y) × E(t)                                                  [S8] [S10]
    M(t)  = cap( μ(t) × E(t) )                                            [S8] [S2]
    SV(t) = AV(t) + M(t) − C(t)                                           [S8]
    SB(t) = max( SV(t), MGSV(t) )                                         [S8] [S9] [S12]

For a partial withdrawal of gross `W(t)`, replace `AV(t)` by `W(t)` in the first and
fourth lines; the amount paid is `W(t) + M(t) − C(t)` and the account value falls by
`W(t)`.

**MVA inside the free amount — the [std] convention.** The representative model sets
`free_wd_mva_exempt = True`: the free allowance is exempt from *both* the surrender charge
and the MVA, including at full surrender [S8] [S11]. **The market is genuinely split.** The
two registered contracts [S3] [S4] both state that the MVA applies to free-amount
withdrawals taken before maturity; the retail MYGAs do not [S2] [S9] [S10] [S15] [S16].
Setting the flag to `False` gives `E(t) = AV(t)` and the composition collapses to the
multiplicative form:

    SB(t) = max( AV(t) × (1 + μ(t) − sc(y)),  MGSV(t) )

which is the identity to use when checking dimensional consistency and when comparing
against contracts that quote an MVA *factor* rather than an MVA *rate*.

### MVA — three formula families, five cap variants

`mva_family` selects the rate; `mva_cap_rule` selects the limit. Both are **first-class
model parameters**, not hard-coded rules, because the cap is the largest single
cross-carrier divergence in the source set.

**(i) `geometric` — Treasury/swap discount factor, uncapped in the sources.**

    Φ(t) = [ (1 + a) / (1 + b + s_adm) ] ^ τ ;   μ(t) = Φ(t) − 1

`a` = reference yield at deposit; `b` = reference yield at distribution for a term equal to
the **remaining** period, partial years rounded **up** to a full year (capped at the
guarantee period) [S4]; `s_adm` = administrative-expense adder, **25 bp** in that registered
contract, explicitly covering the cost of liquidating fixed-income investments and
structurally biasing the adjustment against the owner [S4]; `τ` = days to maturity ÷
**365.25** [S4]. The other registered variant has `s_adm = 0`, uses Treasury notes maturing
in the last three months of the term, and `τ = x/365` measured from the Wednesday of the
week of withdrawal [S3]. Neither states any cap or collar [S3] [S4].

**(ii) `linear_duration` — the representative form.**

    μ(t) = (i0 − it) × T(t)                                               [S8] [S9]
    T(t) = (days from the surrender date to the end of the current contract year ÷ 365)
           + whole years remaining in the MVA period                       [S8]

`i0` = reference index value at issue (re-locked at each renewal); `it` = value at
surrender; source index = Barclay's US Credit Index, formula varying by state [S8]. This is
the first-order approximation of (i): at `i0 = 5%`, `it = 6.5%`, `T = 2.5` the linear form
gives −3.750% against −3.484% for `(1.05/1.065)^2.5 − 1` — a 27 bp gap, widening with
`|i0 − it| × T`, and always in the contract holder's disfavour when rates rise.

**(iii) `declared_differential` — the insurer's own new-money rate.** `M(t) = W × (Ic − In)
× F_s` [S14], with `Ic` the rate credited on the money withdrawn, `In` the rate that would
be credited on **new money** for a guarantee period of the same duration, and `F_s` a
contractual adjustment-factor table by whole years remaining `s` with partial years
interpolated. Specimen table (`Ic < 6%` / `Ic ≥ 6%`): s=0 0.00/0.00; 1 0.90/0.90;
2 1.80/1.75; 3 2.60/2.50; 4 3.40/3.15; 5 4.10/3.80; 6 4.80/4.35; 7 5.40/4.85; 8 6.00/5.35;
9 6.50/5.75; 10 7.00/6.15 [S14]. These are modified-duration factors, which is why the
higher-rate column is uniformly lower. Model #245 §4.I recognizes this branch alongside the
external-index branch [R4] [REG-R45].

**Cap variants (`mva_cap_rule`).**

| Value | Rule | Source design |
|---|---|---|
| `sym_sc` **[std]** | `M = clamp(M_raw, −C, +C)` | one carrier's New York form [S2] |
| `min_sc_interest` | `M = clamp(M_raw, −K, +K)` with `K = min(C, interest credited to date)` | the linear-duration family [S8] [S9] |
| `asym_sc_snfl` | `M ≤ +C`; on the downside no cap — only `SB ≥ MGSV` binds | another carrier's MVA explainer [S12] |
| `gmir_floor` | `AV + M ≥ P_accum@GMIR` (premiums less prior withdrawals accumulated at the GMIR); the surrender charge may still breach that level | the Camp B carrier [S13] |
| `none` | uncapped, fully two-sided | both registered contracts [S3] [S4] |

`μ(t) = 0`, unconditionally, when: the surrender is in the 30-day guarantee-period-end
window [S2]; the MVA period has expired [S8] [S13] [S16]; the benefit is a death benefit
[S2] [S4] [S8] [S13] [S16]; the withdrawal is an RMD or a waiver-rider withdrawal
[S2] [S5] [S13]; or the contract is being annuitized [S16] [std].

### Minimum guaranteed surrender value (Model #805)

    MGSV(0) = 0.875 × P
    MGSV(t) = [ MGSV(t−1) − d(t) − c(t) ] × (1 + i_nf)^(1/12)

with `i_nf` the contract GMSV rate (**2.80%** [S11]). The statute *defines* the indexed
nonforfeiture rate — it is not a band the contract rate sits inside:

    i_stat = max( 0.0015,  min( 0.03,  round_{1/20 of 1%}(CMT5) − 0.0125 ) )  [R1 §4.B] [REG-R42]

and the contract rate must satisfy `i_nf ≥ i_stat`; crediting the floor at more than the
statutory rate is permitted and simply produces a higher floor, which is exactly what
[S11] does ("the GMSV rate will not be less than the minimum rate required by each
state"). **Do not implement the reverse inequality** — capping `i_nf` at
`round(CMT5) − 1.25%` would make the representative 2.80% illegal at any CMT5 below
4.05% and is not what §4.B says. CMT5 is the five-year Constant Maturity Treasury rate
reported by the Federal Reserve as of a date, or averaged over a period, specified in the
contract and no longer than **15 months** before issue or redetermination [R1 §4.B](#uslib-fixed_deferred_annuity-r1).

**Do not implement a 1% floor.** The retrieved Model #805 print floors the indexed
nonforfeiture rate at **15 basis points** [R1 §4.B](#uslib-fixed_deferred_annuity-r1) [REG-R42]; the widely repeated 1%
figure is [unverified] against any retrieved document. `d(t)` is the withdrawal deduction
(`gross` [S11] or `net_of_charges` [S9]); `c(t)` is the monthly slice of the annual
contract charge, $0 representative and $50 statutory maximum [R1 §4.A](#uslib-fixed_deferred_annuity-r1) [S11]. Premium tax
actually paid and indebtedness are additional permitted deductions, both accumulated at
`i_nf`, and are zero here [R1 §4.A](#uslib-fixed_deferred_annuity-r1). The equity-index carve-out of §4.C (an additional
reduction of up to 100 bp) does not apply to a book-value MYGA [R1 §4.C](#uslib-fixed_deferred_annuity-r1).

### Death benefit and annuitization

- **Death benefit** = `AV(t)`, with no surrender charge and no MVA [S1] [S2] [S13], floored
  at the cash surrender benefit and hence at `MGSV(t)` [R1 §6](#uslib-fixed_deferred_annuity-r1). On the base run
  `AV(t) > MGSV(t)` at every duration **because the 4.45% credited rate exceeds the 2.80%
  GMSV rate** — not unconditionally: the floor accretes at 2.80% while a renewal rate may
  fall to the 0.25% GMIR, and at the GMIR the floor overtakes the account value after
  roughly 8.5 further years (≈ contract year 13–14 on the anchor cell). Test the floor on
  death at every duration **[std]**; the alternative "greater of accumulation value and
  minimum surrender value" design [S5] [S6] makes it live in the base run too.
- **Annuitization** transfers `AV'(t)` (in the window) or `SV(t)` (during the surrender
  charge period) out of the accumulation block [S1] [S2] [S5]. Payout factors are **not**
  specified here — no retrieved product document contains an annuity rate table [S4]. The
  accumulation model emits the transfer as an outgo and hands the amount to the payout
  model; the statutory maximum valuation rate for the resulting income stream is VM-V §1
  [REG-R37] and the mortality basis the 2012 IAM/IAR family [R9] [REG-R59] [REG-R60].

### Cash flow ledger

| Cash flow | Formula (per contract, month `t`) | In-force weight | Sign |
|---|---|---|---|
| Single premium | `P` at `t = 0` | 1 | + |
| Free withdrawal payment | `W(t)` where `W(t) ≤ FW(t)` | `l(t−1)` | − |
| Excess withdrawal payment | `W(t) + M(t) − C(t)` | `l(t−1)` | − |
| Full surrender payment | `SB(t) = max(AV(t) + M(t) − C(t), MGSV(t))` | `l(t−1)(1 − a(t))(1 − q(t)) w(t)` | − |
| Death benefit | `AV(t)` | `l(t−1)(1 − a(t)) q(t)` | − |
| Annuitization transfer | `AV'(t)` (window) or `SV(t)` | `l(t−1) a(t)` | − |
| Acquisition commission | `0.02 × P` at `t = 0` **[std]** | 1 | − |
| Maintenance expense | `(50/12) × 1.025^(y−1)` **[std]** | `l(t−1)` | − |
| Premium tax | `premium_tax_rate × P` **[std]** = 0 | 1 | − |

**Internal transfers are not cash flows.** Interest credited to the account value, the
surrender charge, the market value adjustment, and the movement of the Model #805 floor
are **internal accounting entries**: they drive `AV`, `MGSV` and the benefit *amount*,
but they are never separate ledger lines. Only amounts actually paid to or received from
the contract holder, and the insurer's own expenses, are cash flows. This is the
gross-liability convention of the library **[std]**. Two corollaries worth stating because
they are common implementation errors: (1) a binding nonforfeiture floor is **not** a
separate "top-up" cash flow — it raises `SB(t)`, and the difference `MGSV(t) − SV(t)` is a
reconciliation quantity only; (2) the IRC §72 taxable-income split is a *reported*
quantity and generates no insurer cash flow [R6] [REG-R55].

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions built on the VM-22 prescribed
functional form [R2 §6.B.5](#uslib-fixed_deferred_annuity-r2), which is the only publicly specified dynamic-lapse formula
for this product and is therefore the natural skeleton even for a best-estimate run.

### Base lapse by renewal architecture

VM-22 Table 6.5 (fixed annuities with no guaranteed living benefit) is keyed on years
before/after surrender-charge expiry and on whether the contract year contains an
interest-guarantee-period (IGP) expiry [R2]:

| Years before/after SC expiry | IGP ≤ 1 yr | IGP > 1 yr, not an IGP-expiry year | IGP-expiry year (IGP > 1 yr) |
|---|---|---|---|
| 3+ after | 3.0% | 2.0% | 55.0% |
| 2 after | 7.5% | 2.0% | 65.0% |
| 1 after | 10.0% | 2.0% | 75.0% |
| Upon expiry | 25.0% | 6.0% | 75.0% |
| 1 to expiry | 2.5% | 1.0% | 70.0% |
| 2 to expiry | 2.5% | 1.0% | 70.0% |
| 3+ to expiry | 2.5% | 1.0% | 70.0% |

Applying the mapping evidenced by the guideline's own 3-year worked examples [R2] to the
representative 5-year IGP / 5-year surrender charge period gives, as a **[std] extension**:

| `renewal_architecture` | Contract-year base lapse |
|---|---|
| `rollover` (Camp A: new 5-year IGP + new SC schedule) [S1] [S2] [S5] [S11] | 1%, 1%, 1%, 1%, 1%, **75%**, 1%, 1%, 1%, 1%, **75%**, … (period 5) |
| `annual_redeclare` (Camp B: annual rates, no SC) [S13] | 1%, 1%, 1%, 1%, 1%, **75%**, 10%, 7.5%, 3%, 3%, 3%, … |

These are the two patterns the guideline's Examples 1 and 2 generate for a 3-year contract
(1,1,1,75,10,7.5,3 and 1,1,1,75,1,1,75 respectively) [R2], scaled to a 5-year term. **The
architecture switch, not the level, is the first-order modeling decision:** Camp A creates
a repeating shock every five years, Camp B a single shock followed by ordinary
interest-sensitive lapse. Monthly conversion: `w_base_m = 1 − (1 − w_base_annual)^(1/12)`.

Experience corroboration, not calibration: the SOA/LIMRA 2023–2024 fixed-rate deferred study
reports surrender rates peaking in the year the surrender charge expired and remaining
elevated afterwards, decreasing as the GMIR band rose, decreasing as the credited rate rose,
and increasing with the excess of market over credited rate — that relationship "well
defined in the years after surrender charge expiry" but muted during the charge period — and
that "in the year the surrender charge expired, high 'shock' surrender rates were observed
that were not necessarily impacted or driven by market interest rate sensitivity"
[R8] [REG-R63]. Detailed tables sit behind the paid package and were not retrieved.

### Dynamic (interest-sensitive) lapse **[std]**

    w_annual(t) = clamp( Base(y) × G + Rate(t) × Φ_MVA(t),  0.005,  0.90 )
    Rate(t)     = Market(t) × max( 0, 1 − 5 × (1 − CSV(t)/AV(t)) )
    Market(t)   = −1.25 × (CR − MR)^X          if CR ≥ MR
                = 0                             if MR > CR ≥ MR − BF
                = +1.25 × (MR − BF − CR)^X      if CR < MR − BF

with, per the prescribed parameterization [R2 §6.B.5](#uslib-fixed_deferred_annuity-r2):

- `G` = GMIR Factor. Fixed annuities: **1.25** if GMIR ≤ 1.0%; 1.00 if 1.0% < GMIR ≤ 2.5%;
  0.70 if GMIR > 2.5%. Representative GMIR 0.25% [S11] → **G = 1.25**.
- `BF` = buffer factor = **50 bp** — the band inside which no dynamic response occurs.
- `X` = **2.0** during the surrender charge period, **2.5** at the shock and thereafter.
- `CR` = current crediting rate; `MR` = market competitor rate. For fixed annuities with an
  interest guarantee period of 5 ≤ IGP < 7 years, `MR` = the **7-year Treasury rate plus a
  50% A / 50% AA spread minus the Pricing Spread**, with Pricing Spread = 0% [R2].
- `CSV(t)/AV(t)` = `SB(t)/AV(t)`, so `1 − CSV/AV` is exactly the combined surrender-charge
  and negative-MVA haircut; the dynamic term switches **off entirely** once that haircut
  reaches 20%.
- ITM Factor = **1** for an Accumulation-category contract with no guaranteed living or
  death benefit — the guideline says so explicitly [R2].
- `Φ_MVA` = MVA Factor. **The prescribed value is 0 while an MVA is in effect and 1
  otherwise** [R2], i.e., the regulator's view is that an in-force MVA *completely*
  neutralizes interest-rate-driven disintermediation, leaving only `Base × G`.

**[std] departure for best estimate.** The reference model exposes `Φ_MVA` as a parameter
with the prescribed values {0 in force, 1 expired} as the statutory default and **0.35
while in force** as the best-estimate default. Rationale: the prescribed 0 is a regulatory
simplification, and the industry study found a "notable increase" in surrender rates
between a 0% and a 3% market-minus-credited spread *during* the surrender charge period
[R8]. That study does not separate MVA from non-MVA contracts, so 0.35 is a judgement, not
a calibration — sensitivity-test it (see model risks).

**Base deterministic run.** `MR(t) = CR(t) = 4.45%` and `s_ren = 0`, so `Market(t) = 0`,
`Rate(t) = 0`, and `w_annual(t) = Base(y) × 1.25`, floored at 0.5% and capped at 90%.
Contract years 1–5 therefore run at 1.25% and contract year 6 at **90%** (75% × 1.25
= 93.75%, capped) [R2].

### Partial withdrawal and annuitization behavior

- **Partial withdrawals.** 0% in the base run **[std]**; the VM-22 Table 6.2 age-banded
  rates are the variant (see assumption note (b)). Where an RMD module is switched on, RMD
  amounts are free of charge and MVA even above the free allowance [S15] [std], and are
  modeled as a withdrawal with `E(t) = 0`.
- **Annuitization.** `a(t) = 1.0%` in each 30-day guarantee-period-end window after
  contract year 1, 0% elsewhere **[std]** (assumption note (c)). Statutory alternative:
  `a(t) ≡ 0` [R2 §6.B.6](#uslib-fixed_deferred_annuity-r2).
- **Free-withdrawal utilization.** Base run 0; a utilization variant takes `u × FW(y)` each
  contract year with `u` a **[std]** input. Note the interaction: taking the free amount
  each year both lowers `AV` and lowers the future free base, and — under the `gross`
  Model #805 convention [S11] — reduces the nonforfeiture floor by the same amount.

---

## Worked example

Anchor cell: Male 60 ANB, non-qualified, `P` = $100,000, 5-year guarantee period,
`i_cr` = 4.45% [S11], `i_nf` = 2.80% [S11], surrender charge 9/8/7/6/5 [S10], free
withdrawal 10% [S10]. Monthly factors: `f = 1.0445^(1/12) = 1.0036348`,
`g = 1.028^(1/12) = 1.0023039` (both derived). A free withdrawal of $4,000 is taken at BOM
of month 13 (contract year 2 allowance = 10% × AV(12) = $10,445.00, so the whole amount is
free of charge and MVA [S10] [S11]). Full surrender at end of month 30. All figures in
dollars; full precision carried, displayed to cents.

| `t` | Event | `AV(t−1)` | `W(t)` | `AV'(t)` | `AV(t)` | `MGSV(t)` |
|---|---|---|---|---|---|---|
| 1 | — | 100,000.00 | 0.00 | 100,000.00 | 100,363.48 | 87,701.59 |
| 2 | — | 100,363.48 | 0.00 | 100,363.48 | 100,728.28 | 87,903.65 |
| 3 | — | 100,728.28 | 0.00 | 100,728.28 | 101,094.40 | 88,106.17 |
| 12 | 1st anniversary | 104,071.72 | 0.00 | 104,071.72 | 104,450.00 | 89,950.00 |
| 13 | free withdrawal | 104,450.00 | 4,000.00 | 100,450.00 | 100,815.11 | 86,148.02 |
| 24 | 2nd anniversary | 104,540.04 | 0.00 | 104,540.04 | 104,920.03 | 88,356.60 |
| 30 | full surrender | 106,840.74 | 0.00 | 106,840.74 | 107,229.09 | 89,585.05 |

Checks on the table: `AV(12) = 100,000 × 1.0445 = 104,450.00` exactly, and
`AV(24) = 100,450 × 1.0445 = 104,920.025` (displayed 104,920.03) — twelve monthly factors
reproduce the annual effective rate exactly. `MGSV(0) = 0.875 × 100,000 = 87,500.00`;
`MGSV(12) = 87,500 × 1.028 = 89,950.00`; the month-13 withdrawal is deducted **gross** (not
reduced by charges or MVA) under the [S11] convention, giving
`MGSV(24) = (89,950 − 4,000) × 1.028 = 88,356.60`. The surrender traces below are computed
from the cent-rounded values shown, so they reproduce by hand.

**Surrender trace, end of month 30** (contract year 3, `sc = 7%` [S10]; MVA reference yield
`i0` = 5.00% at issue, `it` = 6.50% at surrender, both **[std]**):

- Free allowance for contract year 3: `FW = 0.10 × AV(24) = 10,492.00` [S10], unused.
- `E = 107,229.09 − 10,492.00 = 96,737.09` [S8] [S11].
- `C = 0.07 × 96,737.09 = 6,771.60` [S8] [S10].
- `T = 0.5 + 2 = 2.5` years (six months to the end of contract year 3, plus contract years
  4 and 5 remaining in the 5-year MVA period) [S8].
- `μ = (0.0500 − 0.0650) × 2.5 = −0.037500` [S8] [S9]; `M_raw = −3,627.64`.
- Symmetric cap: `|M| ≤ C = 6,771.60` [S2] — **not binding**, so `M = −3,627.64`.
- `SV = 107,229.09 − 3,627.64 − 6,771.60 = 96,829.85`.
- `MGSV(30) = 88,356.60 × 1.028^(1/2) = 89,585.05` — **floor not binding**.
- **`SB(30) = 96,829.85`**, of which $10,492.00 is the untouched free amount and
  $86,337.85 the adjusted, charged excess.

**A case where the floor binds.** Same contract, full surrender at end of month **6**
(contract year 1, `sc = 9%` [S10]) with the reference yield at 10.00% (a stress level,
**[std]**, chosen to force both the cap and the floor to bind):
`AV(6) = 102,200.78`; `FW = 0.10 × 100,000 = 10,000.00` (year-1 base is purchase payments
[S10]); `E = 92,200.78`; `C = 8,298.07`; `T = 0.5 + 4 = 4.5`; `μ = −0.225`;
`M_raw = −20,745.18`, **capped to −8,298.07** by the symmetric rule [S2];
`SV = 102,200.78 − 8,298.07 − 8,298.07 = 85,604.64`; `MGSV(6) = 87,500 × 1.028^(1/2)
= 88,716.54`. **`SB(6) = 88,716.54`** — the Model #805 floor binds and adds $3,111.90.
Note the ordering lesson: with a symmetric cap the worst case is `AV − 2·sc·E`
(= `AV × (1 − 2·sc)` only when the free amount is zero — here it is
$102,200.78 − 2 × 0.09 × $92,200.78 = $85,604.64, not $102,200.78 × 0.82 = $83,804.64),
and it is only at short durations with a high surrender charge that this falls below
`0.875 × P × (1 + i_nf)^t`.

**Geometric-branch unit test [S4].** For `mva_family = geometric` one registered contract
supplies fully worked arithmetic that a regression test should reproduce exactly: a 5-year
GPO, $10,000 allocation, Specified Interest Rate 8.5%, 5-year swap at deposit `a` = 8%,
surrender 985 days from maturity, Specified Value $12,067.96,
`Φ = [(1 + a)/(1 + b + 0.0025)]^(985/365.25)`. At `b` = 7%: `Φ = 1.01897`, surrender value
**$12,296.89**. At `b` = 9%: `Φ = 0.96944`, surrender value **$11,699.17** [S4]. Recomputing
from the printed five-decimal factors reproduces both to within three cents; assert the
factors, not the dollar figures. Two implementation details: the contract selects `b`'s
maturity by rounding 985/365.25 = 2.69 **up to 3 years** while the exponent uses the exact
day count [S4]; and the Appendix A sensitivity table for a **10-year** GPO with `a` = 8%
shows **−2.06%** at `b` = 8% with 9 years remaining — the pure effect of the 25 bp expense
adder, and a second regression target [S4].

---

## Valuation and reserve pointers

This library projects **gross liability cash flows**. Reserve layers consume them and are
cited, not reproduced:

- **VM-22 principle-based reserves for non-variable annuities** [R2] [REG-R36]. Constitutes
  CARVM for in-scope contracts [R2 §1.A](#uslib-fixed_deferred_annuity-r2); applies for **valuation dates on or after
  January 1, 2026** [R2 §2.B](#uslib-fixed_deferred_annuity-r2); three-year elective transition on VM-A/VM-C/VM-M/VM-V for
  business issued in the first three years, mandatory prospectively thereafter [R2 §2.B](#uslib-fixed_deferred_annuity-r2)
  (2029 is arithmetic, not quotation [unverified]). A MYGA is in the **Accumulation
  Reserving Category** [R2]. Aggregate reserve = SR (CTE70) + DR for contracts passing the
  Single Scenario Test + formulaic reserves for excluded contracts; the additional
  standard projection amount is **disclosure-only** under VM-31 [R2 §3](#uslib-fixed_deferred_annuity-r2).
- **Formulaic CARVM — A-820 ¶¶14–15 as interpreted by AG 33** [REG-R153] [REG-R151], with the
  guideline family indexed at VM-C [REG-R41]. AG 33's printed title is **"Determining CARVM
  Reserves for Annuity Contracts With Elective Benefits"** and its printed *Effective Date*
  block reads "This guideline shall be effective on **December 31, 1998**, affecting all
  contracts issued on or after January 1, 1981" [REG-R151 *Effective Date*](#uslib-reg-r151). The
  **December 31, 1995** date and the alternative title this file previously carried come
  from IRS Rev. Rul. 2002-6, describing a differently-titled instrument [R7] [REG-R39].
  **Both are recorded and the reconciliation is unresolved** — the extracted pages carry no
  amendment history, so "a later revision" is an inference, not a fact from either source;
  the 1 January 1981 issue-date reach is common to both, and the 33⅓ / 66⅔ / 100% grade-in
  ran off by December 31, 2000. The mechanics are **no longer [unverified]**: they are in
  the primary-text extractions `_research/appp-a820-a821-a822.md` and
  `_research/appp-ag33.md`.
  **VM-V §1** carries the statutory maximum valuation interest rate on the post-annuitization
  payout stream [REG-R37].
- **Tax and GAAP.** IRC §807: greater of net surrender value and, post-TCJA, **92.81% of**
  the NAIC-prescribed method reserve (CARVM), capped at statutory [R7] [REG-R16]. LDTI
  (ASU 2018-12) with ASOP No. 10 on the U.S. GAAP basis [REG-R34] [REG-R71].
- **Standards for the modeling work itself.** ASOP 7 (life/health cash flow analysis — the
  standard for exactly this disintermediation/reinvestment/MVA work) [REG-R27]; ASOP 22 (asset adequacy) [REG-R29]; ASOP 56
  (modeling) [REG-R32]; ASOP 2 (non-guaranteed elements — the declared renewal rate)
  [REG-R26]; ASOP 54 (pricing) [REG-R70].

---

## Key sensitivities and model risks

Dominant assumptions, in rough order of impact on a MYGA block:

1. **The shock lapse at surrender-charge / guarantee-period expiry, and the renewal
   architecture switch that positions it.** Base lapse moves from 1% to 75% in a single
   contract year under the prescribed table [R2], and Camp A repeats that every five years
   while Camp B does it once [S11] [S13]. Nothing else in the model moves the liability
   duration as much. Run both architectures before quoting a duration.
2. **The renewal declared rate `s_ren`, jointly with dynamic lapse.** The credited-minus-
   competitor spread drives both the interest margin and the surrender rate, in opposite
   directions; the 50 bp buffer and the quadratic/2.5-power response make the sensitivity
   strongly convex around `CR = MR` [R2].
3. **`Φ_MVA` — whether the MVA suppresses dynamic lapse.** The prescribed value of 0 [R2]
   and the best-estimate **[std]** 0.35 bracket a large range; at 0 the entire dynamic term
   vanishes during the surrender charge period.
4. **The MVA cap rule.** Symmetric-at-charge, min(charge, interest credited),
   asymmetric-with-nonforfeiture-floor, GMIR-floored, and uncapped produce materially
   different tail surrender values on the same rate path [S2] [S3] [S4] [S8] [S9] [S12] [S13].
   The cap, not the formula family, is where the money is.
5. **The Model #805 floor at short durations.** As the worked example shows, the floor
   binds early (high charge, large negative MVA) and not later; a model that tests the
   floor only at full surrender in later durations will miss it entirely.

Known modeling pitfalls:

- **Composition order.** `MVA → surrender charge → floor`, with both computed on the
  pre-deduction excess `E` [S8]. Applying the charge first and the MVA to the net figure
  understates the adjustment by `sc × |M|`; applying the floor before the MVA silently
  removes the downside protection.
- **The free-amount / MVA interaction.** `free_wd_mva_exempt` is a real product difference
  [S2] [S3] [S4] [S9] [S10] and changes both the surrender value and the `1 − CSV/AV` haircut
  that gates dynamic lapse. Do not hard-code it.
- **Gross vs net withdrawals.** `W(t)` is the **gross** amount removed from the account
  value; contracts promising a stated net check need a gross-up solve — one registered
  prospectus works the case, $2,099.08 withdrawn to deliver a $2,000 check at a 0.9528
  factor [S3].
- **The Model #805 withdrawal convention.** `gross` [S11] versus `net_of_charges` [S9] are
  both live and give different floors; the difference then compounds at `i_nf` for the rest
  of the contract.
- **The 15 bp floor.** Implementing the folklore 1% floor overstates the Model #805 minimum
  in low-rate environments — the retrieved statute says 15 bp [R1 §4.B](#uslib-fixed_deferred_annuity-r1) [REG-R42].
- **Surrender-charge clock on renewal.** Under `rollover` the clock resets [S1] [S2] [S11];
  the two registered contracts run it from the original purchase payment date so it never
  restarts [S3] [S4]. Getting this wrong relocates the shock lapse by years.
- **Mortality table plumbing.** The prescribed formula uses the 2012 IAM **Basic** table
  (VM-M §2.C) with Scale G2 and the VM-22 `F_x` factors [R2 §6.B.8](#uslib-fixed_deferred_annuity-r2), not the 2012 IAM
  Period/IAR valuation table. Where the IAR generational table *is* used, the Valuation
  Manual's rounding trap applies: round from the 2012 period rate each time, never compound
  an already-rounded prior-year rate [REG-R59]. Do not substitute life bases — annuitant
  mortality is a different and lighter basis than the 2017 CSO / 2015 VBT / ILEC families
  [REG-R59] [REG-R60] [REG-R61], and annuity surrender behavior is structurally unlike life
  lapse [REG-R63]. Deferred-*period* annuitant mortality is under-evidenced: only a
  2011–2015 study and a 2006 analysis were identified, neither retrieved [REG-R65].
  Fortunately mortality is second-order here — death pays full account value with no charge
  and no MVA [S1] [S2] [S13].
- **Era and snapshot caveats.** The 4.45% declared rate, 2.80% GMSV rate and 0.25% GMIR
  [S11] are a September 2025 snapshot of one product; the same insurer's 2023 brochure
  stated the GMIR "will be 1% or higher" [S10]. Levels are era-representative; mechanics are
  stable.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-fixed_deferred_annuity-r1
[R2]: #uslib-fixed_deferred_annuity-r2
[R4]: #uslib-fixed_deferred_annuity-r4
[R6]: #uslib-fixed_deferred_annuity-r6
[R7]: #uslib-fixed_deferred_annuity-r7
[R8]: #uslib-fixed_deferred_annuity-r8
[R9]: #uslib-fixed_deferred_annuity-r9
[REG-R151]: #uslib-reg-r151
[REG-R153]: #uslib-reg-r153
[REG-R16]: #uslib-reg-r16
[REG-R26]: #uslib-reg-r26
[REG-R27]: #uslib-reg-r27
[REG-R29]: #uslib-reg-r29
[REG-R32]: #uslib-reg-r32
[REG-R34]: #uslib-reg-r34
[REG-R36]: #uslib-reg-r36
[REG-R37]: #uslib-reg-r37
[REG-R39]: #uslib-reg-r39
[REG-R41]: #uslib-reg-r41
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R45]: #uslib-reg-r45
[REG-R55]: #uslib-reg-r55
[REG-R59]: #uslib-reg-r59
[REG-R60]: #uslib-reg-r60
[REG-R61]: #uslib-reg-r61
[REG-R63]: #uslib-reg-r63
[REG-R65]: #uslib-reg-r65
[REG-R70]: #uslib-reg-r70
[REG-R71]: #uslib-reg-r71
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
