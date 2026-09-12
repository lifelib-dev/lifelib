# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** These notes specify a reference liability cash-flow projection model for
the standardized composite *rente viagère immédiate* defined in `product-spec.md` (same
directory). This is not any single insurer's product. [S#]/[R#] tags refer to the source
list in `sources.md`, numbering carried verbatim from `_research/rente-viagere.md`;
[REG-R#] tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own frozen R1–R49 numbering).
**[std]** marks standardizations introduced for the reference implementation. Parameter
values are identical to those in `product-spec.md`. The model these notes are implemented
as is **`Rente_FR_S`**, on a **monthly** grid. It shares its payout chassis with the UK
sibling `PA_UK_S` and the US sibling `SPIA_US_S`, and reuses their cells names wherever
the machinery is the same — `lives_if`, `lives_death`, `certain_floor`, `payment_factor`,
`payment_surv_mth`, `cum_annuity_pp`, `annuity_pp`, `annuity_payments`, `pols_if`,
`liability_cf`. Amounts are in euros with the English decimal point; quoted French text
keeps its original comma.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (*arrérages* to the
  annuitant, the *prorata d'arrérages* on death, the reversion stream, the *frais
  d'arrérages* retained, maintenance expenses) for one *rente viagère* in payment.
  Discounting and reserves are not computed (see Valuation and reserve pointers).
- **Mortality is the model.** After conversion the contract has no premiums, no surrender
  value [R8], no account value and no policyholder option of any kind [S1] [S2] [S3] [S4]
  [S5] [S6] [S8]. The only decrements are deaths. There is **no lapse machinery anywhere
  in this model** and that is a cited product feature, not an omission.
- **Projection frequency and origin.** Monthly grid, **0-based**: t = 0, 1, …, proj_len − 1
  months from the effective date, which is always the 1st day of a civil month
  [S2] [S3] [S6]; month t is the whole civil month beginning at the t-th month-start after
  it, so t = 0 is the civil month of the effective date itself and month t runs from time t
  to time t + 1. proj_len is the **number** of months projected, the policy year containing
  month t is t ÷ 12 + 1 (integer division), and the attained ages step at each 12-month
  multiple of t. Survival is carried at the **time points** t = 0, 1, …: l(t) is the
  probability of being alive at time t, l(0) = 1, so month t opens at l(t) and closes at
  l(t + 1), and no quantity is ever indexed before time 0.
- **The model carries the calendar, not just the duration.** Revalorisation is credited at
  **31 December** [S2 pt 10.f], so the model point carries the effective date's calendar
  year and civil month. Nothing in this product happens on a policy anniversary.
- **Age basis and generation.** Age last birthday at the effective date, incrementing on
  each 12-month multiple of it **[std]**. The **generation** (*millésime*, year of birth)
  is a separate model point attribute and is **never derived from the projection year**:
  the tables are generational and the birth year is the table key [R1] [R19].
- **No improvement scale.** TGH05/TGF05 are prospective generation tables: q(sex,
  generation, age) already gives the rate the life will experience at that age in calendar
  year generation + age [R1] [R19] [R25, secondary](#frlib-rente_viagere-r25). A separate improvement projection —
  which the UK sibling needs, because ONS national life tables are *period* tables — would
  double-count the trend. `Rente_FR_S` has no `improve_factor` cells and must not acquire
  one.
- **Limiting age.** ω = 120, the published top age of the tables [R25, secondary](#frlib-rente_viagere-r25); the
  **[std]** proxy CSV caps q at 1 there. The construction document states the tables give
  rates where age + generation > 1995 [R19], which the 50–85 issue band respects.
- **Model points and rounding.** EUR throughout; single-policy model points on an expected
  (probability-weighted) basis, with a **scenario** mortality basis **[std]** carried as
  in `PA_UK_S` so the worked example is reproducible row by row. Annuitant and reversionary
  mortality are independent **[std]** — a documented model risk. No intermediate rounding;
  displayed figures are rounded to the cent independently, so a rounded gross minus a
  rounded charge can differ by one cent from the rounded net.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `purchase_price` C | currency | 200,000 **[std]** |
| `effective_year` Y0 | int | 2026 **[std]** |
| `effective_month` M0 | int 1–12 (civil month of the effective date) | 4 (April) **[std]** |
| `annuitant_age` x_a0 | int, age last birthday at the effective date, 50–85 [S1] | 65 **[std]** |
| `annuitant_birth_year` g_a | int (*millésime*; the generational table key) | 1961 **[std]** |
| `annuitant_sex` | enum {`M`, `F`, `mix`} | `M` **[std]** |
| `annuity_rate` ρ | float, *taux de rente* per unit of capital p.a. | 0.0330 **[std]** |
| `reversion_pct` δ | float 0–1 [S2] [S3]; 0 if no *réversion* | 0.60 **[std]** |
| `reversion_coeff` κ | float, definitive reduction of the annuitant's own annuity | 0.76 [S6 Art. 5.4.3] |
| `reversion_age` x_r0 | int, age last birthday at the effective date | 61 **[std]** |
| `reversion_birth_year` g_r | int | 1965 **[std]** |
| `reversion_sex` | enum {`M`, `F`, `mix`} | `F` **[std]** |
| `guarantee_years` | int, 0 or 5–min(25, e − 5) in 5-year steps [S2] [S3] [S4] [S9]; XOR `reversion_pct` [S2] [S3] | 0 |
| `palier_scheme` | enum {`none`, `inc1`, `inc2`, `dec1`, `dec2`} [S2 pt 10.e] | `none` |
| `palier_step_years` S | int {5, 10} [S2] | 0 |
| `payment_freq` m | enum {12, 4, 2, 1} [S2] [S4] [S5] [S6] | 12 |
| `payment_timing` | enum {`arrears`, `advance`} — French contracts are all `arrears` [S1]–[S9] | `arrears` |
| `arrerage_charge_rate` f | float, *frais d'arrérages* per *quittance* | 0.03 [S5] [S7 Art. 17.3] |
| `technical_rate` i | float, *taux technique* priced at conversion | 0.0000 [S2 pt 10.d] [S3] |
| `mort_basis` | enum {`table`, `scenario`}; the scenario switch is **[std]** (see Worked example) | `scenario` |
| `death_mth` | int, month of death on the `scenario` basis, on the 0-based clock; blank or negative = survives | 25 (annuitant), −1 (reversionary) |

Every **[std]** in the Example column is a choice of the worked configuration, not a
product feature; each is restated and tagged in the Worked example section below, and the
rates among them (ρ, κ, f) carry their own footnotes in `product-spec.md` and in
assumption class (b).

C is the amount actually applied to the annuity: for a wrapper exit the *valeur atteinte*
net of social and tax levies [S4 §7.3.2.3], with any entry charge taken before the model
starts [S1] [S6] [S7 Art. 17.1]. The initial gross annual annuity is **derived**, not
carried: A₀ = C ρ κ, because ρ and κ are the two quantities a real *barème* computes and
the model must show the arithmetic rather than take its answer as an input.
`technical_rate` is carried although it appears in **no recursion** — it reaches the
projection only through ρ, and is recorded so a reader can see which rate ρ was struck on.
Neither the revalorisation rate nor the charge on the annuity fund is a model point
attribute: both are insurer-discretionary, set portfolio-wide, and live in class (b).

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `cal_year_index(t)` k(t) | Number of 31 Decembers strictly before the start of month t | monthly |
| `revalo_factor(t)` R(t) | Cumulative revalorisation index; R = 1 until the first 1 January | at each 1 January |
| `palier_factor(t)` Π(t) | Step multiplier of the *rente par paliers* schedule; 1 when none | at palier boundaries |
| `annual_income(t)` A(t) | Gross annualised *rente* in force = A₀ R(t) Π(t) | monthly |
| `lives_if(t, life)` l(t, ·) | Survival probability to **time** t, t = 0 at the effective date; l(0) = 1 | monthly |
| `lives_death(t, life)` d(t, ·) | l(t, ·) − l(t + 1, ·), the deaths of month t | monthly |
| `certain_floor(t)` γ(t) | 1 while the *annuités garanties* run, else 0 | monthly |
| `payment_factor(t)` | max(γ(t), l_a at the payment point) — the annuitant stream's factor | payment months |
| `reversion_factor(t)` | δ (1 − l_a(t)) l_r at the payment point | payment months |
| `cum_annuity_pp(t, kind)` G(t) | Cumulative gross *arrérages*, as-if-alive (`"ANNUITANT"`) or expected across both streams (`"ALL"`) | payment months |
| `pols_if(t)` | Probability any payment obligation remains | monthly |
| `inflation_factor(t)` | Expense inflation index, stepping at each 1 January | at each 1 January |

R(t), Π(t) and A(t) are **deterministic** given the assumption set: the annuity level does
not depend on survival, only the payment factors do. G(t) on the `"ANNUITANT"` kind is
therefore a pure schedule and needs no path simulation.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Instalment | A(t)/m at each payment date, *terme échu* | [S2] [S3] [S6] |
| Instalment on the month of death | Due in full: instalments "cessent d'être dus à compter du premier jour du mois qui suit le décès" | [S6]; accrued arrears to the heirs [S1 Art. C17.2] [S7 Art. 7.3] |
| Mortality table family | TGH05 (male) / TGF05 (female), generational, mandatory for *rentes viagères* from 1 January 2007 | [R1 art. 2, verbatim](#frlib-rente_viagere-r1) [REG-R21] |
| Single-table rule | One table for all lives must be the most prudent — TGF05 | [R3, verbatim](#frlib-rente_viagere-r3) [REG-R23] |
| Experience-table floor | An experience-table tariff may never be lower than the homologated-table tariff | [R3, verbatim](#frlib-rente_viagere-r3) |
| *Taux technique* ceiling | min(3.50%, 60% × TME) beyond eight years, on a 0.25-point ladder floored at zero | [R4] [R5] [REG-R17] |
| Reversion | δ × the annuity reached at death, for life, from the 1st day of the **month or quarter** following death [S6] — the 1st day following death at [S1 Art. C12]; the reduction κ is definitive even if the reversionary predeceases | [S2] [S3] [S1 Art. C12] [S6 Art. 5.4.3] |
| Reversion coefficient table | Published coefficients by age difference and reversion rate (table below) | [S6 Art. 5.4.3] |
| *Annuités garanties* | n months of instalments certain at the same amount, to designated beneficiaries; no lump-sum commutation offered | [S2] [S3] [S4] |
| *Paliers* schemes | inc1 100→200%; inc2 100→125→150%; dec1 100→50%; dec2 100→75→50%; first step 5 or 10 years, second step equal | [S2 pt 10.e] [S3 pt 11.d] |
| Revalorisation date and floor | Credited at 31 December, pro rata temporis in the first partial calendar year, never negative | [S2 pt 10.f] [S3] |
| Surrender value | None, at any duration | [R8, verbatim](#frlib-rente_viagere-r8) [S1 Art. C3] |
| Commutation threshold | €110 per month including *majorations légales*, × months in the payment period | [R10 art. A. 160-2](#frlib-rente_viagere-r10) |

**Reversion coefficient table** [S6 Art. 5.4.3], applied to the annuitant's own annuity.
It is the only published option-cost table in the sources; it was built for a points
régime and its adoption here as a euro-annuity coefficient is **[std]** (spec footnote 15).
The key is the difference in *millésime* between the reversionary and the annuitant.

| Age difference (reversionary vs annuitant) | 60% | 80% | 100% |
|---|---|---|---|
| Older by 8 years or more | 0.93 | 0.91 | 0.89 |
| Older by 4–7 years | 0.89 | 0.86 | 0.83 |
| Within 3 years either way | 0.81 | 0.76 | 0.72 |
| Younger by 4–7 years | **0.76** | 0.70 | 0.65 |
| Younger by 8–15 years | 0.66 | 0.59 | 0.54 |
| Younger by 16–23 years | 0.58 | 0.51 | 0.45 |
| Younger by 24–29 years | 0.53 | 0.46 | 0.40 |
| Younger by 30–34 years | 0.49 | 0.42 | 0.37 |
| Younger by 35–39 years | 0.47 | 0.40 | 0.35 |
| Younger by 40–44 years | 0.42 | 0.35 | 0.30 |
| Younger by 45 years or more | 0.35 | 0.29 | 0.24 |

### (b) Insurer-discretionary current elements

Unlike the UK sibling, **this class is not empty** — it is where the French product's
uprating lives.

| Input | Value | Basis |
|---|---|---|
| Revalorisation rate ν | **1.50%** a year, floored at zero | **[std]** (i) |
| *Frais sur encours de rentes* φ | **0.80%** a year, entering ν rather than the cash flow | [S2]; level **[std]** (ii) |
| *Frais d'arrérages* f | **3.00%** of each *quittance* | [S5] [S7 Art. 17.3]; composite **[std]** (spec footnote 10) |
| *Taux de rente* ρ at conversion | **3.30%** at age 65, unisex TGF05 basis | **[std]** (iii) |
| Guarantee coefficient (when *annuités garanties* are elected) | **0.9820** for a 15-year term at 65 | **[std]** (iv) |

(i) No retrieved document publishes a revalorisation rate, a formula or a history for
annuities in payment. The uplift is fed by the annuities' own profit-sharing account,
built under point III of art. A. 132-11 "en incluant le résultat technique généré par ces
mêmes rentes", with "100 % du solde créditeur" attributed to the annuities
[S3, verbatim] [R7] [REG-R15]; sums parked in the *provision pour participation aux
bénéfices* must reach policyholders within eight financial years [R7 art. A. 132-16,
verbatim](#frlib-rente_viagere-r7) [REG-R16]. 1.50% is a round placeholder between the 0.00% *taux technique*
[S2] [S3] and the 2.00% technical-rate ceiling [R21, secondary](#frlib-rente_viagere-r21), with the contractual
floor of zero as the only cited bound. **It is a scenario input, not a contractual
parameter.** The machinery it stands for is specified in the
[assurance vie euro technical notes](../assurance_vie_euro/technical-notes.md) and not
restated here; *Where ν comes from*, under the revalorisation recursion, says what this
product inherits from it and where it departs.
(ii) The charge bites on the *provision mathématique* backing the annuity and reduces the
profit-sharing base, never the guaranteed annuity, in every retrieved contract
[S1 Art. C9] [S2] [S5] [S6] [S7]. It therefore appears in these notes only as a reason ν
is lower than the gross return on the annuity fund, and **must not be netted from any
instalment**. Observed range 0.55%–2.3% (spec footnote 11).
(iii) Spec footnotes 6 and 7: derived from the TGF05 residual life expectancies published
in [R19] with a **[std]** loading of about 2%. Struck on a 0.00% *taux technique*
[S2] [S3]. The same construction on the male table gives 3.73%.
(iv) No retrieved document publishes the cost of *annuités garanties*. 0.9820 is a
**[std]** derived figure: the certain-period annuity factor exceeds the life factor by
the sum over the guaranteed months of (1 − survival), which on the [R19]-implied basis is
about 0.54 years against a factor of about 29.63. The coefficient therefore varies with
the term — 0.9986 at 5 years, 0.9267 at 25 — and is recomputed from the mortality basis
rather than carried as a model point attribute.

### (c) Behavioral / experience assumptions (modeler's view)

| Input | Recommended basis | Basis tags |
|---|---|---|
| Base mortality | The mandatory tables are TGH05/TGF05 [R1] [REG-R21], annexed to the Code des assurances [R12]; **this library does not redistribute them**. The reference basis is a **[std]** generational proxy keyed on (sex, generation, age), built from INSEE population data [REG-R24] and anchored so the **tariff** annuity factor — the female-table factor the unisex rule selects — reproduces the placeholder ρ of assumption (iii). The best-estimate factor is *not* anchored: on the male table it gives 3.73%, not ρ | [R1] [R12] [R19] [REG-R21] [REG-R24]; proxy **[std]** (v) |
| Mortality improvements | **None applied.** The table is generational and carries its own projection [R1] [R19] | [R1] [R19] |
| Tariff table | TGF05 for every life, regardless of sex, per the most-prudent-single-table rule | [R3, verbatim](#frlib-rente_viagere-r3); adoption **[std]** (spec footnote 4) |
| Best-estimate table | The sex-appropriate table where the model point carries a sex; the blend at `portfolio_male_share` where it carries `mix` | [R3] [R17] [R18]; blend **[std]** (vi) |
| `portfolio_male_share` θ | **0.45** | **[std]** (vi) |
| Lapse / surrender | **None** — no surrender value exists at any duration | [R8, verbatim](#frlib-rente_viagere-r8) [S1 Art. C3] |
| Maintenance expense | €30 per contract per annum, payable monthly while any obligation remains, inflating at π | **[std]** (vii) |
| Expense inflation π | 1.50% a year, stepping at each 1 January | **[std]** (vii) |
| Proof-of-life suspension | Not modeled | [S1] [S2] [S3]; **[std]** (viii) |

(v) TGH05/TGF05 are annexed to the Code des assurances and the annexe article carrying
TGF05 is itself marked abrogated as of 1 January 2016, with the current location of the
tables unidentified [R12] [unverified]. The proxy CSV has the same *shape* as a
generational table — a rate is keyed on (sex, generation, age) and on nothing else — so
the model's indexing is exercised honestly even though the rates are not the regulatory
ones. This is the same posture the UK sibling takes on CMI tables. **Substituting a
licensed basis means replacing the CSV with a same-schema file; no formula changes.**
(vi) The tariff is unisex by law while the tables are sex-distinct [R3]; the ministry
states the resulting surplus on male lives must in substantial part be returned to
policyholders within eight years [R17] [REG-R16]. A portfolio mix is the assumption that
reconciles the two: the insurer prices one rate for a cohort whose expected mortality is a
blend of the two tables. **Art. A. 132-18 does not forbid that blend.** Its second table
family expressly permits tables built by the undertaking, "with or without sex", certified
by an actuary independent of it on its own or demographically equivalent experience — a
blended, non-sex-distinct table is precisely what that permits — subject to a one-sided
floor rather than a prohibition: for *rentes viagères* the tariff from such a table "ne
peut être inférieur" to the tariff the appropriate homologated table would give
[R3, verbatim](#frlib-rente_viagere-r3). The most-prudent-table rule is the *other* limb;
it bites only where a single **homologated** table is applied to all lives, and then
selects TGF05. This model takes that homologated route — prices on TGF05 and projects on
the sex-appropriate best estimate — which is one of two lawful constructions, not the only
one; a certified blend would remain floored at the TGF05 tariff, so the direction of the
prudence margin is the same either way. θ = 0.45 is **[std]** — no retrieved document
publishes the sex mix of a French annuitant portfolio — and sits below one half because
the unisex tariff itself
deters male annuitants (see Policyholder behavior modeling).
(vii) No insurer publishes expense assumptions. €30 a year is a round placeholder for
in-payment administration; note that at the composite's 3% *frais d'arrérages* the charge
on the worked configuration is about €150 a year, so the French charging structure
recovers far more than in-payment administration and the balance funds distribution and
margin. Acquisition cost is out of scope (single premium, priced in).
(viii) An unreturned *attestation valant certificat de vie* suspends payment from the
following month until it arrives [S2] [S3] [S1 Art. C13]. It shifts timing, not amount,
and no source publishes a suspension frequency.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | month index from the effective date, 0-based: t = 0, 1, …, proj_len − 1 |
| Y0, M0 | calendar year and civil month of the effective date (M0 = 1 for January) |
| k(t) | completed 31 Decembers strictly before the start of month t |
| g_a, g_r | *millésimes* (birth years) of annuitant and reversionary |
| x_a(t), x_r(t) | attained ages, x(t) = x(0) + floor(t/12) **[std]** (Model scope, "Age basis and generation") |
| m | payments per year; payment months T = {t : (t + 1) mod (12/m) = 0} (arrears) |
| C, ρ, κ | *capital constitutif*, *taux de rente*, option coefficient |
| A₀, A(t) | gross annual *rente* at conversion and in force in month t |
| ν, R(t) | annual revalorisation rate and its cumulative index |
| Π(t) | *palier* step multiplier |
| δ, n | *taux de réversion*; *annuités garanties* in months |
| f, φ | *frais d'arrérages* rate; *frais sur encours de rentes* rate |
| q(s, g, x) | annual mortality from the generational table, sex s, generation g, age x |
| l_a, l_r, d_a, d_r | survival probabilities of the two lives, at time points, and their death densities over month t |
| γ(t) | certain-period indicator, 1{t < n}; C alone is always the capital |
| h(t) | complete months elapsed since the last payment date, measured at the start of month t |
| θ | portfolio male share **[std]** (assumption (vi)) |
| c_e, π | maintenance expense p.a. and expense inflation |

Dimensional check: A, C and every cash flow are currency; ρ, ν, f, φ, δ, κ, θ, q, l and
the factors are dimensionless; A/m is currency per payment. Every flow below is currency
per month.

### Calendar index and the revalorisation recursion

The annuity is in service for 13 − M0 months of its first calendar year — months
t = 0 … 12 − M0 — so

    k(t) = 0                                 for t < 13 − M0
    k(t) = 1 + floor((t − (13 − M0)) / 12)   otherwise

    R(t) = 1                                                     for k(t) = 0
    R(t) = (1 + ν · (13 − M0)/12) · (1 + ν)^(k(t) − 1)           for k(t) ≥ 1

The pro-rating factor (13 − M0)/12 implements "les rentes en service depuis moins d'un an
au 1er janvier sont revalorisées prorata temporis de la date d'effet au 31 décembre" [S3];
it is 1 for a 1 January effective date, so the general form degenerates correctly. The
uplift is credited at 31 December [S2 pt 10.f] and reaches instalments payable from the
following 1 January **[std]** (spec footnote 12), which is why k(t) counts 31 Decembers
*strictly before* month t. ν ≥ 0 always [S1] [S2] [S3] [S4] [S7].

**Where ν comes from.** The *participation aux bénéfices* machinery ν is drawn out of is
specified once for this library, in the
[assurance vie euro technical notes](../assurance_vie_euro/technical-notes.md), and is not
redeveloped here. **Inherited from there**: the *compte de participation aux résultats*
built under art. A. 132-11 on a financial account and a technical account, with 85% of the
financial balance and the technical balance less the insurer's share (the greater of 10%
of the credit balance and 4.5% of premiums — a clause returned as paraphrase and
**[unverified]** as to exact formulation) [R7] [REG-R15]; and the *provision pour
participation aux bénéfices* with its eight-year clock [R7 art. A. 132-16, verbatim](#frlib-rente_viagere-r7)
[REG-R16], which is where a year's excess is parked and from which an older vintage is
forced out. **Where this product deviates**, in four places:

1. **A different account.** The annuities in payment have their own *compte de
   participation aux bénéfices*, built under **point III** of art. A. 132-11 "en incluant
   le résultat technique généré par ces mêmes rentes", with **100% du solde créditeur**
   attributed to them [S3, verbatim] [R7]. It is not the euro fund's account and it is not
   fed by the euro fund's *épargne acquise*.
2. **The technical result is not a loading result.** On the euro support the death benefit
   is the account value, so the underwriting result is nil and the technical account is the
   charges less the expenses. Here the technical result is dominated by the **mortality**
   result on the annuities, including the TGF05 prudence margin every male life carries
   under the unisex rule [R3] [R17] — which is what makes the revalorisation of an annuity
   book structurally different from that of a savings book.
3. **ν is an input, not an output.** `Euro_FR_S` derives the credited rate from the
   constrained allocation and uses the PPB as a lever; this model carries no *provision
   mathématique* ledger, no average-provision base and no PPB vintage ledger, so ν is an
   exogenous **[std]** scalar (assumption (b), note (i)). Substituting the euro model's
   credited-rate path for the flat ν is the intended extension, and nothing in the
   recursion above assumes ν is constant.
4. **The uplift lands on the annuity and is irreversible.** A euro-fund credit lands in the
   *épargne acquise*, which a surrender can take away; R(t) multiplies the *rente* for the
   remainder of its life and there is no surrender at any duration [R8]. There is also no
   TMG here: *i* is a pricing rate, not a floor on ν, whose only cited bound is zero.

### Palier factor

    palier_scheme = none                Π(t) = 1
    two-step (inc1, dec1)               Π(t) = π₁ for t < 12S,  π₂ for t ≥ 12S
    three-step (inc2, dec2)             Π(t) = π₁ for t < 12S,  π₂ for 12S ≤ t < 24S,  π₃ after

with (π₁, π₂, π₃) from the scheme table of assumption (a) and S ∈ {5, 10} years; the
second step is "d'une durée égale" to the first [S2] [S3]. Π is a step function of
duration and nothing compounds — a *rente par paliers* is not escalation.

### Conversion at the effective date

    A₀ = C · ρ · κ

κ = 1 with no option; the reversion coefficient of the [S6] table where *réversion* is
elected; the **[std]** guarantee coefficient where *annuités garanties* are elected. The
options are not cumulative [S2] [S3], so exactly one of δ > 0 and n > 0 may hold.

**Admission test, not a cash flow.** A model point is projectable only if its gross
*quittance d'arrérages* exceeds the statutory threshold:

    A₀ · Π(0) / m  >  110 · (12/m)                                [R10 art. A. 160-2]

Below it the insurer may, with the annuitant's agreement, pay a capital instead
[R9] [R10] [S2] [S3] [S5], so there is no annuity to project. `check_commutation_floor()`
must fail such a point rather than project it.

### Generational mortality construction

    q(t, life)     = qtab(basis(life), g(life), x(life, t))       — pure table lookup
    q_mth(t, life) = 1 − (1 − q(t, life))^(1/12)                  **[std]**
    l(t, life)     = l(t − 1, life) · (1 − q_mth(t − 1, life)),   l(0, ·) = 1
    d(t, life)     = l(t, life) − l(t + 1, life)

l is indexed by **time** and q by the **month** it applies over: survival to time t takes
the rates of months 0 … t − 1, and the deaths of month t are the difference between its
opening and closing survivals.

with

    basis(life) = "M" or "F"                    where the model point carries a sex
    q           = θ q(M, g, x) + (1 − θ) q(F, g, x)   where it carries `mix`   **[std]**

**There is no improvement factor and no calendar-year argument.** q depends on t only
through the attained age x(life, t); the generation g is fixed at the model point. That
single line is the largest structural difference from `PA_UK_S`, whose period base table
requires a separate improvement projection to become a cohort view.

On the `scenario` basis **[std]** the survival path is the step function
l(t, life) = 1{t ≤ `death_mth`(life)} — survival to time t, so a life dying in month d is
alive at time d, the start of that month, and gone from time d + 1 — with a blank or
negative `death_mth` meaning the life survives the projection; the device `PA_UK_S` uses,
and the basis the worked example runs on.

**The tariff table and the best-estimate table are different objects.** ρ is struck on
TGF05 for every life [R3, verbatim](#frlib-rente_viagere-r3) while the projection decrements on `basis(life)`; for
a male annuitant the two differ by construction, and the gap is the systematic technical
surplus that must flow back to policyholders within eight years [R17] [REG-R16] — which
here it does, through ν. Collapsing them destroys both halves of the mechanic (pitfall 3).

### Payment factors

    payment_surv_mth(t) = t + 1                 arrears (*terme échu*): the end of month t
                        = t                     advance (*terme à échoir*, unobserved in France):
                                                its start

    certain_floor(t)    = 1 if t < n else 0
    payment_factor(t)   = max(certain_floor(t), l_a(payment_surv_mth(t)))
    reversion_factor(t) = δ · (1 − l_a(t)) · l_r(payment_surv_mth(t))

The `max` makes the *annuités garanties* an annuity-**certain floor** rather than a second
stream: while the guarantee runs the full instalment is payable regardless of survival
[S2] [S3] [S4], and an additive form would pay 1 + l_a.

The reversion gate is `(1 − l_a(t))`, the annuitant's survival to the **start** of month t,
**not** `(1 − l_a(t + 1))`, its survival to the end: the survivor's first
instalment falls in the month *after* the month of death, immediately after the *prorata
d'arrérages* has settled it. What [S6] states for the *réversion* is that it is payable
"from the 1st day of the **month or quarter** following death"; the annuitant's own
instalments are the ones that "cessent d'être dus à compter du premier jour du mois qui
suit le décès" [S6], and that verbatim sentence is the cessation rule quoted in assumption
(a), not the reversion-start rule. The model applies the **one-month** gate at every
payment frequency **[std]**, which reads the disjunction on its monthly limb: at m = 12 —
Préfon's own periodicity, and the periodicity of every model point that carries a
*réversion* — the two limbs coincide, but on a quarterly contract the gate opens the
survivor's stream up to a quarter earlier than the second limb would. No source states
which limb governs which contract, and no shipped model point combines a *réversion* with
m < 12.

### Scheduled instalment and cumulative arrérages

    A(t)            = A₀ · R(t) · Π(t)
    annuity_pp(t)   = A(t)/m   for t ∈ T, else 0
    cum_annuity_pp(t, "ANNUITANT") = cum_annuity_pp(t − 1, ·) + annuity_pp(t)
    cum_annuity_pp(t, "ALL")       = cum_annuity_pp(t − 1, ·)
                                     + annuity_pp(t) · (payment_factor(t) + reversion_factor(t))
                                     + prorata_pp(t) · prorata_factor(t)

for t ≥ 1; month 0 is the first projected month, so the accumulation opens there — G(0) is
what month 0 itself pays, and there is no month-zero row to carry.

`"ANNUITANT"` is the deterministic as-if-alive schedule; `"ALL"` is the expected total
paid across both streams. On a probability-weighted run `"ALL"` is an expectation rather
than a path; in a scenario run the two coincide for a surviving annuitant.

### Expected cash flows (month t)

**Arrérages.**

    E[ANN(t)] = pols_if_init · annuity_pp(t) · (payment_factor(t) + reversion_factor(t))

**Prorata d'arrérages** — the accrued instalment settled on death [S1 Art. C17.2] [S6]
[S7 Art. 7.3]. With h(t) = t mod (12/m) complete months since the last payment date,

    prorata_pp(t)     = ((h(t) + 1)/(12/m)) · A(t)/m     *terme échu*
                      = 0                                *terme à échoir* **[std]**
    prorata_factor(t) = d_a(t) · (1 − γ(t))  +  δ · (1 − l_a(t)) · d_r(t)
    E[PRO(t)]         = pols_if_init · prorata_pp(t) · prorata_factor(t)

The second branch is the unobserved *terme à échoir* switch (spec footnote 9): the
instalment covering the month of death was paid at the start of it, so nothing has accrued
unpaid and there is nothing to settle. Only shipped model point 11 takes it.

At m = 12, h(t) = 0 for every t, so `prorata_pp(t)` is exactly **one full instalment** —
the month of death is due in full [S6]; at m = 4 a death in the first month of a quarter
settles one third of the quarterly instalment. The `(1 − γ(t))` gate suppresses the term
while the *annuités garanties* run, the full instalment being payable there already, and
the second term is the symmetric settlement on the reversionary's own death. There is no
"with/without proportion" election in France: the *prorata* is the rule.

**Frais d'arrérages** — retained by the insurer out of each *quittance* [S5] [S7 Art. 17.3]:

    E[FRA(t)] = f · (E[ANN(t)] + E[PRO(t)])

**Maintenance expense**:

    pols_if(t) = min(1, max(γ(t), l_a(t + 1)) + 1{δ > 0} · (1 − l_a(t)) · l_r(t + 1))
    E[EXP(t)]  = (c_e/12) · (1 + π)^k(t) · pols_if(t)                       **[std]**

**Total gross liability cash flow**:

    liability_cf(t) = E[ANN(t)] + E[PRO(t)] − E[FRA(t)] + E[EXP(t)]
    net_cf(t)       = − liability_cf(t)

There is no premium income (C is a pricing input at the effective date), no surrender outgo [R8] and no
death capital — the representative design is *capital aliéné*. The *frais sur encours de
rentes* appear nowhere in this recursion by design: they reduce the profit-sharing base,
hence ν, and never an instalment.

### Monthly processing order

1. Advance the calendar: compute k(t). If k(t) > k(t − 1), step the revalorisation index
   R (pro-rated when k = 1) and the expense inflation index [S2 pt 10.f] [S3]. At t = 0,
   k = 0 and R = 1 by construction, so there is no earlier month to read.
2. Update the *palier* factor Π(t) if t reaches 12S or 24S [S2] [S3].
3. Set A(t) = A₀ R(t) Π(t). If t ∈ T, record `annuity_pp(t)`.
4. Decrement mortality: attained ages from the effective-date ages, rates from the
   generational table at each life's own *millésime*; update l_a, l_r, d_a, d_r.
5. Compute `certain_floor(t)`, `payment_factor(t)` at `payment_surv_mth(t)`, and
   `reversion_factor(t)` using l_a(t), the annuitant's survival to the start of month t.
6. Compute E[ANN(t)], then E[PRO(t)] (gated off while the guarantee runs), then
   E[FRA(t)] on the sum of the two. Update `cum_annuity_pp`.
7. Accrue E[EXP(t)] on `pols_if(t)`.
8. Stop once both lives have passed ω = 120 and the guarantee has run: the projected
   months are t = 0 … max(n, 12(ω − min x_i)) − 1, so the last of them is the last month
   of age ω − 1 of the **youngest** covered life — stopping on the annuitant's age alone
   truncates a younger reversionary's tail.

### Known modeling pitfalls

These are the specific ways an implementation of **this** product looks right and is
wrong. Each is a test.

1. **Applying an improvement scale on top of the generational table.** TGH05/TGF05 are
   prospective; the trend is inside them [R1] [R19]. Any `improve_factor` double-counts
   it. Test: q must be unchanged when the effective year moves and the *millésime* does
   not.
2. **Indexing the table by projection calendar year instead of birth year.** A
   period-table implementation reads the rate for age 66 in calendar year 2027 and walks
   diagonally across generations; a generational table reads (g = 1961, x = 66) whatever
   the projection year. Test: two model points with the same entry age and different
   *millésimes* must give different rates at the same attained age.
3. **Using the tariff table as the best estimate.** Pricing every life on TGF05 [R3] and
   also projecting a male life on TGF05 makes the unisex prudence margin invisible — no
   surplus, so no source for the revalorisation the contract shares [S3] [R17]. Projecting
   him on TGH05 without crediting the surplus back through ν shows a permanent retained
   profit the eight-year rule does not allow [REG-R16]. The two tables must be separate
   objects.
4. **Revalorising on the policy anniversary instead of 31 December.** The uplift is a
   calendar event [S2 pt 10.f]: on the worked configuration the anniversary convention
   gives twelve months at the initial level instead of nine and shifts every later step by
   three months.
5. **Dropping the first-year pro-rata, or uplifting the December instalment.** The first
   uplift is ν · (13 − M0)/12 [S3]; applying the full ν overstates the annuity for the whole
   of its remaining life, because R(t) is a running product. The credit is at 31 December
   and reaches instalments payable from 1 January **[std]**; applying it to the December
   arrears instalment adds one instalment a year at the new level.
6. **Losing the arrérage of the month of death.** The UK sibling's default pays nothing
   for the final partial period; the French rule settles the accrued arrears to the heirs
   [S1 Art. C17.2] [S6] [S7 Art. 7.3], which at m = 12 is a whole instalment. Test: on the
   scenario basis the number of instalments paid equals `death_mth` + 1, the months of
   service through the month of death, the index being 0-based.
7. **Starting the reversion in the month of death.** The gate is (1 − l_a(t)), the
   annuitant's survival to the start of month t [S6]; using (1 − l_a(t + 1)), its survival
   to the end, pays the reversion and the *prorata d'arrérages* in the same month, so the
   month of death is paid 1 + δ times.
8. **Paying a prorata during the guarantee period, or adding the certain floor instead of
   taking a max.** While the *annuités garanties* run the full instalment is already
   payable regardless of survival [S2] [S3], so the prorata on top double-pays the month
   of death and an additive `certain_floor + l_a` pays 1 + l_a for the whole term.
9. **Mishandling the reversion coefficient.** κ reduces the annuitant's own annuity once,
    permanently, at conversion [S6 Art. 5.4.3]. It must not also scale the reversion
    stream — the survivor receives δ × the *already reduced* annuity reached at death
    [S2] — and it is not released if the reversionary predeceases: "une réduction
    définitive, même si le bénéficiaire de la réversion vient à décéder antérieurement"
    [S6 Art. 5.4.3, verbatim].
10. **Modeling a surrender.** There is none [R8, verbatim](#frlib-rente_viagere-r8). Any lapse rate, surrender
    value or paid-up value here is a defect. The single exception is not a cash flow but
    an admission test: `check_commutation_floor()` must reject a model point whose gross
    monthly *quittance* does not exceed €110 [R10].
11. **Netting the *frais sur encours de rentes* off the instalment.** They bite on the
    *provision mathématique* and reduce the profit-sharing base, never the guaranteed
    annuity [S1 Art. C9] [S2] [S5] [S6] [S7]; subtracting them from an instalment cuts the
    annuitant's income, which no retrieved contract does.
12. **Charging the *frais d'arrérages* on the annualised rente.** The deduction is per
    *quittance d'arrérages* [S5] [S7 Art. 17.3]. At a flat percentage the two coincide; at
    a per-instalment cap [S4 §7.3.2.3] or a flat per-instalment fee [R23, secondary](#frlib-rente_viagere-r23) they
    do not, and the payment frequency then changes the total.
13. **Discounting the projected flows at the *taux technique*.** It reaches the projection
    only through ρ; the best estimate discounts at the risk-free term structure
    [REG-R4] [REG-R5]. Reusing i as a discount rate produces neither a price nor
    a reserve.
14. **Applying a palier step to the reversion stream.** The survivor receives δ × the
    annuity *reached at death* [S2]; a step falling later belongs to the annuitant's
    schedule. The representative options are mutually exclusive so it cannot arise here,
    but a Spirica-style combinable engine [S4] must gate Π(t) on the annuitant being
    alive.

---

## Policyholder behavior modeling

There is none to model after conversion, and this is a cited product feature. There is no
surrender or reduction of any kind [R8, verbatim](#frlib-rente_viagere-r8) [S1 Art. C3], no transfer, no premium
flexibility, and every option is irrevocable once elected [S1 Art. C15, C16] [S2 pt 10.e]
[S3 pt 11.d] [S4 §7.3] [S5] [S6 Art. 5.4.3] [S8]. The model therefore carries **no lapse
decrement and no dynamic behavior formulas**.

Three behaviors sit at the boundary and are handled outside the projection. **The
commutation election**: below the art. A. 160-2 threshold the insurer may pay a capital
instead, but only "avec l'accord de l'assuré" [S2] [S3] [S5] [R9] [R10] — a one-off
election at liquidation, implemented as an admission test rather than an in-force option
(pitfall 10). **Proof of life**: failure to return the annual certificate suspends payment
from the following month until it arrives [S1 Art. C13] [S2] [S3], a timing effect on an
otherwise unchanged obligation, not modeled **[std]**. **Change of spouse**: where the
survivor at death is not the person named at liquidation the reversion annuity is
recalculated on the survivor's age at death [S2] [S3] — a live option a single-policy
model point cannot carry (spec footnote 16).

Behavior enters the *basis*, not the projection, as selection effects **[std]**.

- **Annuitization anti-selection.** Annuitizing is voluntary outside the *versements
  obligatoires* compartment [REG-R34] [S2], so voluntary annuitants self-select for
  longevity. TGH05/TGF05 are annuitant-experience tables built on exactly that population
  [R1] [R19], so the effect is already inside the mandatory basis — which is why this
  library applies no annuitant adjustment factor of the kind the UK sibling needs.
- **Sex anti-selection, and the direction of θ.** The unisex tariff is struck on the
  female table [R3], so a male annuitant receives about 13% less than his own table would
  give (spec footnote 7). Men therefore annuitize less readily than women, and the
  realised male share of a French annuitant portfolio sits below the population share.
  That is the direction, not the magnitude, of the **[std]** θ = 0.45; no retrieved
  document publishes a portfolio mix.
- **Option selection.** Reversion is chosen disproportionately by annuitants with a
  younger spouse, *annuités garanties* by annuitants who expect to die early — both push
  realised experience away from the tariff basis, and no source quantifies either
  [unverified].

---

## Worked example

Configuration (the worked model point; parameters as in `product-spec.md`). Capital
C = €200,000 **[std]**; effective date **1 April 2026** **[std]**, so Y0 = 2026 and
M0 = 4. Annuitant **male, born 1961, age 65** at the effective date **[std]** — inside the
50–85 band [S1 Art. C5, C12]. Reversionary **female, born 1965, age 61** **[std]** —
inside the 50–85 reversionary band [S1 Art. C16], and **younger by 4 years** in
*millésime*. *Taux de rente* ρ = **3.30%** **[std]** (assumption (iii)), struck on a
*taux technique* of **0.00%** [S2 pt 10.d] [S3]. *Réversion* at δ = **60%**
[S2] [S3] [S6] [S9], snapshot **[std]**, with coefficient κ = **0.76** from the "younger
by 4–7 years / 60%" cell of the published table [S6 Art. 5.4.3]. **Monthly, *terme
échu*** [S2] [S3] [S6]. *Frais d'arrérages* f = **3.00%** [S5] [S7 Art. 17.3].
Revalorisation ν = **1.50%** a year **[std]**, credited at 31 December, pro-rated
9/12 in 2026 [S3]. Maintenance expense €30 a year inflating at 1.50% **[std]**. No
*annuités garanties* and no *paliers* — the options are not cumulative [S2] [S3].
Mortality basis **`scenario`** **[std]**: the annuitant dies in month 25 (May 2028) — the
26th month of service, the index being 0-based — and the reversionary survives throughout.
All amounts in euros, unrounded in the model and displayed to the cent.

Conversion: A₀ = C ρ κ = 200,000 × 0.0330 × 0.76 = **€5,016.00** a year, so the gross
monthly *quittance* is 5,016.00 / 12 = **€418.00**. Admission test: 418.00 > 110
[R10 art. A. 160-2](#frlib-rente_viagere-r10), and also above the €40 monthly issue floor of [S6] and [S8], so the
point projects.

| t | Civil month | Event | R(t) | Gross arrérage | Frais (3%) | Net to payee |
|---|---|---|---|---|---|---|
| 0 | Apr 2026 | first arrérage, *terme échu* | 1.000000 | 418.00 | 12.54 | 405.46 |
| 8 | Dec 2026 | last instalment at the initial level | 1.000000 | 418.00 | 12.54 | 405.46 |
| 9 | Jan 2027 | 31 Dec 2026 uplift, pro-rated 9/12 → 1.125% | 1.011250 | 422.70 | 12.68 | 410.02 |
| 11 | Mar 2027 | — | 1.011250 | 422.70 | 12.68 | 410.02 |
| 20 | Dec 2027 | — | 1.011250 | 422.70 | 12.68 | 410.02 |
| 21 | Jan 2028 | 31 Dec 2027 uplift, full 1.50% | 1.026419 | 429.04 | 12.87 | 416.17 |
| 24 | Apr 2028 | last instalment to the annuitant | 1.026419 | 429.04 | 12.87 | 416.17 |
| 25 | May 2028 | annuitant dies; *prorata d'arrérages* to the heirs — one whole month | 1.026419 | 429.04 | 12.87 | 416.17 |
| 26 | Jun 2028 | *réversion* begins at 60% of the *rente atteinte* | 1.026419 | 257.43 | 7.72 | 249.70 |
| 29 | Sep 2028 | — | 1.026419 | 257.43 | 7.72 | 249.70 |
| 32 | Dec 2028 | — | 1.026419 | 257.43 | 7.72 | 249.70 |
| 33 | Jan 2029 | 31 Dec 2028 uplift reaches the reversion stream | 1.041815 | 261.29 | 7.84 | 253.45 |
| 35 | Mar 2029 | — | 1.041815 | 261.29 | 7.84 | 253.45 |

**Checks.** *Conversion, a different way.* The unisex tariff is struck on TGF05 for every
life [R3]; 1/ρ = 1/0.0330 = 30.30 years, against the annuity factor of about 29.63 implied
at age 65 for the 1961 generation by the TGF05 life expectancies published in [R19] — the
gap being the **[std]** loading of about 2% (spec footnote 6). Had the same male annuitant
been priced on **his own table**, ρ = 3.73% (spec footnote 7) would give
A₀ = 200,000 × 0.0373 × 0.76 = €5,669.60 and a monthly *quittance* of **€472.47** — a
**13.0%** higher income than the €418.00 he actually receives. That difference is the
price of the unisex rule, and it is the surplus that must flow back to policyholders
within eight years [R17] [REG-R16], which in this model it does through ν.

*The month-9 instalment, a different way.* k(9) = 1, and the first uplift is
ν(13 − M0)/12 = 0.015 × 9/12 = 1.125%, so the instalment is 418.00 × 1.01125 = 422.7025,
displayed 422.70 — identical to 5,016.00 × 1.011250 / 12. On a policy-anniversary
convention the uplift would not arrive until t = 12 and the March 2027 row would still
read 418.00 (pitfall 4).

*The reversion instalment, a different way.* The survivor receives 60% of the *rente
atteinte* at death, i.e. 0.60 × 429.043038 = 257.4258, displayed **257.43** — the same as
0.60 × A(25)/12 with A(25) = 5,016.00 × 1.026419 = 5,148.5165. Note that a lower reversion
rate would engage the commutation rule: at δ = 20% the survivor's *quittance* would be
0.20 × 429.043038 = **€85.81**, below the €110 threshold, and CNP applies the rule to the
reversion annuity with the *réversataire*'s agreement [S5] [R10].

*Cumulative arrérages and total charge.* 26 monthly amounts are paid over 26 months of
service, t = 0 … 25 — nine at 418.00, twelve at 422.7025 and five at 429.043038, the last
of those five being the *prorata* settled at t = 25 — so
`cum_annuity_pp(25, "ALL")` = 9 × 418.00 + 12 × 422.7025 + 5 × 429.043038 =
**€10,979.65**, of which the insurer retains 3% = **€329.39** and the annuitant and his
heirs receive **€10,650.26**. Losing the month-of-death instalment (pitfall 6) would leave
25 amounts and understate the outgo by €429.04.

*Full liability cash flow, two months.* liability_cf(9) = 422.7025 × 0.97 + (30/12) ×
1.015 = 410.021425 + 2.5375 = **€412.56**; liability_cf(26) = 257.425822 × 0.97 +
(30/12) × 1.015² = 249.703048 + 2.575563 = **€252.28**. `net_cf` is the negative of each.

**The annuités garanties variant.** Replace the *réversion* with *annuités garanties* of
15 years (n = 180 months, inside the 5-to-min(25, e − 5) range in 5-year steps
[S2] [S3] [S4] [S9]) and the coefficient κ = 0.9820 **[std]** (assumption (iv)); the
options are not cumulative, so δ = 0 [S2] [S3]. Then A₀ = 200,000 × 0.0330 × 0.982002 =
€6,481.21 a year, an instalment of **€540.10** at the initial level, **€546.18** from
t = 9 and **€554.37** from t = 21. The death in month 25 now changes **nothing**:
`certain_floor(t)` is 1 through t = 179 — the guarantee covers the 180 months t = 0 … 179
— so the full instalment continues to the designated beneficiaries at
the same amount and rises with the same revalorisation index [S2] [S3]; no *prorata* is
due, because the full instalment is already payable (pitfall 8); and from t = 180 the
stream stops, there being no reversion in that configuration [S2] [S3]. In expectation the
same flows come out of
`payment_factor(t) = max(certain_floor(t), l_a(payment_surv_mth(t)))` with n = 180.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers consume
them and are **cited, not specified**.

- **French statutory provisions.** An annuity in payment is held in the *provision
  mathématique*, the difference between the actuarial present values of the two sides'
  commitments *including future management costs*, one of the eleven technical provisions
  at art. R. 343-3 [REG-R6]. The *provision pour participation aux bénéfices* holds profit
  shares attributed but not yet payable and must be released within eight financial years
  [R7 art. A. 132-16, verbatim](#frlib-rente_viagere-r7) [REG-R16]; the *provision pour risque d'exigibilité*
  attaches to the assets backing it [REG-R7]. The only statutory reserving basis retrieved
  for annuities is the commutation *barème*, which values the annuity on the *provision
  mathématique* computed with the tables and interest rates of the **règlement ANC
  n° 2015-11 du 26 novembre 2015** [R10 art. A. 160-3](#frlib-rente_viagere-r10).
- **Solvabilité II.** The best estimate is the probability-weighted average of future cash
  flows discounted at the relevant risk-free term structure, with EIOPA publishing the
  curves monthly [REG-R5]. Both statements are carried on EIOPA's authority [REG-R4]:
  neither the directive [REG-R1] nor the delegated regulation [REG-R2] could be retrieved
  here — both return an AWS WAF challenge — so no Solvency II article number in this
  library was read from the instrument itself and every such number is [unverified]. The
  `liability_cf(t)` vector above is exactly
  that input. Nothing product-specific to *rentes viagères* was retrieved for the SCR or
  risk-margin layer, and no cost-of-capital rate in this library was read from a retrieved
  instrument. **The technical rate is not a discount rate**: *i* prices the annuity at
  conversion [S2] [S4] [S7] and thereafter functions as a lifetime minimum guaranteed
  return [R20, abstract only](#frlib-rente_viagere-r20), never as a valuation rate (pitfall 13).
- **The liability is structurally prudent and profit-shared.** A prudently priced tariff
  (TGF05 for every life [R3]), a zero or near-zero technical rate [S2] [S3] [R21], and
  100% of the annuity profit-sharing account's credit balance attributed back to the
  annuities [S3, verbatim] make the French annuity a *prudently priced, profit-shared*
  liability rather than a hard-guaranteed one. A best estimate that ignores ν values only
  the guaranteed floor.
- **IFRS 17, tax, professional standards.** French listed insurers report on IFRS 17 from
  2023 with no French carve-out; the fulfilment cash flows are the same vector with the
  risk adjustment and contractual service margin layered on [REG-R45]. Policyholder
  taxation — RVTO fractions by age at *entrée en jouissance* [R13] [R14], the RVTG pension
  regime [R13] [R15], social levies [S2] [S6] [S7] — does not enter the insurer's
  liability cash flows. NPA 1 and NPA 2 (*Modèles actuariels*), category-3 recommended
  practices adopted 15 June 2015, frame the assumption-setting and documentation here
  [REG-R43] [REG-R44]; NPA 4, on best-estimate life provisions, was not retrieved
  [unverified].

---

## Key sensitivities and model risks

Dominant assumptions, in order.

1. **Longevity level and the generational surface.** The liability is a life-contingent
   payment stream with no offsetting decrement, so the mortality level is the single
   largest lever on it. The **[std]** INSEE-shaped generational proxy [REG-R24] stands in
   for TGH05/TGF05, which cannot be redistributed [R12]; production work substitutes a
   same-schema licensed file. Because the trend is *inside* the table, a basis error is
   not a level error but a surface error: the wrong generation column mis-states every
   future year at once.
2. **The unisex reconciliation.** The tariff is TGF05 for every life [R3] while the best
   estimate is sex-dependent; θ and the sex mix therefore move the projected surplus
   directly, and the surplus is the source of ν [S3] [R17] [REG-R16]. A model that sets
   θ = 1 or collapses the two tables reports a materially different profit signature from
   one that does not.
3. **The revalorisation path.** ν is discretionary, non-negative, unpublished and fed by
   the annuities' own technical and financial result net of the *frais sur encours*
   [S1] [S2] [S3] [S5]. A deterministic ν values the zero floor at intrinsic only: the
   floor never binds on a flat positive path, so the option the annuitant holds — an
   uplift that can rise but never fall — is worth nothing in this projection. The eight-
   year release rule [REG-R16] additionally makes ν path-dependent on the PPB stock, which
   this model does not carry.
4. **Reversion assumptions.** δ, the age difference (which selects κ [S6]) and the
   survivor's own generational rates drive the reversion tail. Independence **[std]**
   ignores broken-heart dependence and shared lifestyle, modestly overstating that stream;
   the change-of-spouse recalculation [S2] [S3] is an unmodeled option that can only
   increase the liability.
5. **The taux de rente itself, and the charge levels.** ρ is **[std]** because no French
   insurer publishes a rate card and the annuity is not guaranteed before liquidation
   [S4 §7.3.2.3]; every euro figure here scales linearly with it. f is disclosed as a
   maximum, not a cap [REG-R30], and ranges from 0.00% to 3% across the retrieved carriers
   (spec footnote 10). Expense inflation is second-order against the instalments, but the
   in-payment term is 30 years and more, so π compounds.
6. **Data risk in the sources themselves.** The CJEU judgment was never read [R16]; the
   ACPR study of the *taux technique* returned HTTP 403 and only its abstract is used
   [R20]; the "life expectancy minus five years" cap on *annuités garanties* has no located
   legal source [S2] [S3] [S4] [S9] against [R1] [R2] [R3]; the technical-rate ceiling of
   2.00% is a commercial tracker's reading at 31 July 2026 and moves [R21]; and the
   press-reported charge levels date from 2015 [R23] [R24]. Each is flagged where used and
   none is load-bearing on the recursions.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-rente_viagere-r1
[R10]: #frlib-rente_viagere-r10
[R12]: #frlib-rente_viagere-r12
[R13]: #frlib-rente_viagere-r13
[R14]: #frlib-rente_viagere-r14
[R15]: #frlib-rente_viagere-r15
[R16]: #frlib-rente_viagere-r16
[R17]: #frlib-rente_viagere-r17
[R18]: #frlib-rente_viagere-r18
[R19]: #frlib-rente_viagere-r19
[R2]: #frlib-rente_viagere-r2
[R20]: #frlib-rente_viagere-r20
[R21]: #frlib-rente_viagere-r21
[R23]: #frlib-rente_viagere-r23
[R24]: #frlib-rente_viagere-r24
[R3]: #frlib-rente_viagere-r3
[R4]: #frlib-rente_viagere-r4
[R5]: #frlib-rente_viagere-r5
[R7]: #frlib-rente_viagere-r7
[R8]: #frlib-rente_viagere-r8
[R9]: #frlib-rente_viagere-r9
[REG-R1]: #frlib-reg-r1
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R17]: #frlib-reg-r17
[REG-R2]: #frlib-reg-r2
[REG-R21]: #frlib-reg-r21
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R30]: #frlib-reg-r30
[REG-R34]: #frlib-reg-r34
[REG-R4]: #frlib-reg-r4
[REG-R43]: #frlib-reg-r43
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[REG-R7]: #frlib-reg-r7
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
