# Product Specification

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of the euro support of a French `contrat d'assurance vie`
(life savings contract). It does not describe any single insurer's contract or fund.
Facts carrying a source tag — [S#] (primary product documents: `notice d'information`,
`conditions générales`, `document d'information clé`, fee tables) and [R#]
(regulatory/actuarial references), both numbered per `_research/assurance-vie-euro.md`
and resolved against `sources.md` in this directory — were extracted from the cited
document. [REG-R#] resolves against the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own frozen R1–R49 numbering).
Values marked **[std]** are standardizations introduced for the reference
implementation; each carries a numbered footnote giving the rationale and, where the
research recorded one, the observed range across insurers. Claims the research file
could not confirm against a retrieved document are flagged [unverified]. The mechanics
anchors are six insurers' own booklets and fee tables — Generali Vie / Boursorama [S1],
MACSF [S2], Suravenir [S3] [S4] [S5], CNP Assurances [S6] [S7] [S8], Abeille Vie / Afer
[S9]–[S12] and MAIF VIE [S13] — and the quantitative anchor is the ACPR's annual
revaluation study [R14].

French terms of art are kept in French and glossed on first use: `fonds en euros` (euro
fund), `épargne acquise` (the savings accumulated on the support), `participation aux
bénéfices` (PB — profit participation), `provision pour participation aux bénéfices`
(PPB — the collective profit-participation reserve), `taux servi` (the rate actually
credited), `taux minimum garanti` (TMG), `effet cliquet` (ratchet), `rachat`
(surrender), `avance` (policy loan), `arbitrage` (switch between supports),
`prélèvements sociaux` (social levies).

---

## Product overview and market role

A French `contrat d'assurance vie` is a savings wrapper whose money sits on one or more
`supports`. The `fonds en euros` is the capital-guaranteed general-account support: the
insurer carries the investment risk, the policyholder's `épargne acquise` cannot fall
because of market movements, and each year's return is credited definitively by the
`effet cliquet` [S9] [S11]. Every contract retrieved here is **multisupport** — the euro
fund sits alongside `unités de compte` (UC, unit-linked) and, twice, an `eurocroissance`
support [S1] [S2] [S3] [S4] [S9]. A monosupport euro contract is the degenerate case
with the UC allocation set to zero; no monosupport notice was retrieved, and the claim
that such contracts are now rarely marketed is [unverified].

The dominant retail form is a `contrat d'assurance vie de groupe à adhésion facultative`
— a group policy between an insurer and a subscribing body (a bank or an association)
that individuals join by `adhésion` — verified across BoursoVie (Generali Vie /
Boursorama) [S1], RES Multisupport (MACSF / association AMAP) [S2], Meilleurtaux
Placement Vie 2 (Suravenir / VIREA) [S3], Croissance Avenir (Suravenir / SEREP) [S4],
Nuances 3D (CNP) [S6] and Multisupport Afer (Abeille co-insurers / Afer) [S9].
Genuinely individual contracts exist — CNP's Perspective Capi is a `contrat de
capitalisation individuel nominatif` [S8], which has no insured life and no beneficiary
clause but whose euro support behaves identically. Underwriting classification is
branch **20** (Vie-Décès) and branch **22** (contracts linked to investment funds) [S3].

The euro support is the largest single savings liability in France. Euro-support
`provisions mathématiques` (mathematical provisions) of individual contracts were
**EUR 1 207 bn** at end-2025 against EUR 1 178 bn at end-2024, and collective contracts
a further **EUR 154 bn** [R14]; total assurance vie encours was **EUR 2 088 bn** at
end-2025 [R17], of which capital-guaranteed contracts EUR 1 361 bn and UC EUR 612 bn,
against household financial wealth of which assurance vie and retirement savings are
**32.9%** [R15]. In 2025 the market took EUR 159.1 bn of premiums against EUR 115.1 bn
of benefits (surrenders EUR 71.0 bn, claims EUR 44.1 bn) for a **net inflow of
EUR 44.0 bn**, of which euro supports **+EUR 6.4 bn** — positive again after five
consecutive years of net outflow — and UC +EUR 37.6 bn [R15]. The recommended holding
period is **eight years** and the published reason is fiscal, not economic: "Durée de
détention recommandée : 8 ans compte tenu de la fiscalité en vigueur" [S6]. The euro
**support** on its own carries a recommended minimum holding period of **one year** and
a PRIIPs summary risk indicator of **1 out of 7**, the lowest class [S5].

This specification standardizes a single composite: a multisupport group contract with
one euro support, zero `frais sur versement` (entry charge), an annual `frais de gestion
sur encours` (charge on the account balance) levied at 31 December, a capital guarantee
**net of** those management charges, no contractual PB percentage, a TMG of zero, an
annual `taux servi` announced for the closing year and definitively acquired on
crediting, `prélèvements sociaux` at 17.2% taken as the interest is credited, and free
surrender at any time with no penalty. That is BoursoVie [S1], Meilleurtaux Placement
Vie 2 [S3] and MAIF's contract [S13] with their differences ironed out, sitting on the
ACPR's central figures — 2.63% credited, 0.63% charged, 0.32% average technical rate
[R14].

---

## Representative specification

### Contract form and wrapper

| Parameter | Representative value | Basis |
|---|---|---|
| Legal form | `contrat d'assurance vie de groupe à adhésion facultative`; individual `adhésion` to a group policy | [S1] [S2] [S3] [S4] [S6] [S9] |
| Branches | 20 (Vie-Décès) and 22 (linked to investment funds) | [S3] |
| Support architecture | Multisupport; this specification models the euro support only | [S1] [S2] [S3] [S4] [S9]; single-support scope **[std]** (1) |
| Premium forms | `versement initial`, `versements libres`, `versements libres programmés` (minimum EUR 50 monthly) | [S1] |
| Minimum initial payment | EUR 100 | [S10]; observed EUR 30 [S13] to EUR 300 [S1] |
| Minimum partial surrender | EUR 1 000, residual account value EUR 1 000; programmed EUR 150 monthly and only above EUR 10 000 on the euro funds | [S1] |
| Association fee | EUR 0 | [S13]; observed EUR 10/EUR 20 [S2], EUR 20 [S9] [S10]; choice **[std]** (2) |
| Renunciation | 30 full calendar days | [S2] [S6] [S9] [REG-R29] |

### The euro support — guarantee and charges

| Parameter | Representative value | Basis |
|---|---|---|
| Capital guarantee form | Premiums net of entry charges, **less the annual management charges** — the `garantie nette` | [S3] [S5] [S6] [S7]; choice **[std]** (3) |
| Guarantee measurement | On the account value **before** `prélèvements sociaux` and income tax | [S1] [S2] [S3] |
| Guarantee is a floor, not a return | Risk indicator 1 of 7; stress, unfavourable and intermediate one-year scenarios all return exactly the amount invested | [S5] |
| `Frais sur versement` (entry charge) | 0.00% | [S1] [S3] [S13]; observed 0.5% [S9] [S10] and 3% max [S2] |
| `Frais de gestion sur encours` | 0.60% p.a. of the euro-support balance | [S3]; level choice **[std]** (4) |
| Charge timing | Levied at 31 December value date; pro rata temporis on payments and disinvestments during the year | [S1] [S2] [S9] |
| Charge base convention | The average balance over the year (`prorata temporis`) | reconstructed from the published minimum surrender tables [S2] [S3]; **[std]** (5) |
| `Frais d'arbitrage` (switch charge) | 0.00% | [S1] [S3] [S10] |
| `Frais de rachat` (surrender charge) | 0.00% | [S2] [S3] [S10] [S13] |
| Annuity conversion charge | 3% of `arrérages` (annuity instalments) | [S3] [S4] [S10] [S13] |
| Charges internal to the fund | 0.24% p.a. management and operating plus 0.03% p.a. transaction costs, **excluded** from the contract's charges | [S5]; treatment **[std]** (6) |

### Crediting — `taux servi`, TMG and `participation aux bénéfices`

| Parameter | Representative value | Basis |
|---|---|---|
| Crediting date | 31 December, value date; PB definitively acquired once credited. Rate fixed by the board for the closing year, published in Q1 of the following year | [S1] [S2] [S6] [S7] [S9]; [S3] [S4] |
| `Taux minimum garanti` (TMG) | 0.00% p.a. | **[std]** (7) |
| TMG statutory ceiling and duration | Lower of 150% of the maximum technical rate, and the higher of 120% of that rate and 110% of the average rates credited over the two preceding financial years; fixed for at least six months and at most to the end of the following financial year | [R4] [REG-R18] |
| Maximum technical rate | 75% of the TME; beyond eight years, and for periodic-premium contracts of any duration, min(3.5%, 60% of the TME) | [R1] [REG-R17] |
| Contractual PB percentage | None — the statutory allocation applies | [S1] [S3] [S4]; observed 90% [S4] and 100% [S9]; choice **[std]** (8) |
| Statutory PB floor | The `compte de participation aux résultats` is credited with **85% of the balance of the compte financier** and with the balance of the `compte technique` **less** the insurer's share, that share being the **greater of 10% of the credit balance and 4.5% of annual premiums** | [R5, art. A132-11](#frlib-assurance_vie_euro-r5) [R6] [R14, fn 12](#frlib-assurance_vie_euro-r14) [REG-R15] |
| Statutory minimum benefit | The credit balance of that account, less interest already credited to mathematical provisions | [R5, art. A132-12](#frlib-assurance_vie_euro-r5) [REG-R15] |
| Reference `taux servi` target | 2.30% p.a., net of charges on the balance and before `prélèvements sociaux` | **[std]** (9) |
| Market `taux servi` 2025 | 2.63% individual, 2.64% collective, on the same net-of-charges basis; undertakings holding 50% of encours credited between 2.3% and 2.9%; inside one insurer the best- and worst-revalued groups were 0.99 point apart and the least-revalued sat 0.39 point below the mean | [R14] |
| UC-holding bonus | Often 100 bp, sometimes above 200 bp; not modeled | [R14]; exclusion **[std]** (10) |
| Asset return backing it | `Taux de rendement de l'actif` 2.8% in 2025 (2.5% in 2024); half of undertakings between 2.4% and 3.3%; bonds about 60% of investments | [R14] |
| Average technical rate | 0.32% individual, 0.98% collective in 2025 — a discount-rate statistic, **not** a TMG | [R14] |

### `Provision pour participation aux bénéfices` (PPB)

| Parameter | Representative value | Basis |
|---|---|---|
| Nature | Collective reserve holding PB attributed but not yet credited to individual contracts | [R5, art. A132-16](#frlib-assurance_vie_euro-r5) [S2] [S9] [REG-R6] [REG-R16] |
| Release constraint | Sums carried to the PPB must be applied to mathematical provisions or paid to policyholders **within the eight financial years following** the year they were carried | [R5, art. A132-16](#frlib-assurance_vie_euro-r5) [R6, art. A331-9](#frlib-assurance_vie_euro-r6) [S2] [REG-R16] |
| Opening level | 4.0% of the euro-support account value | [R14]; per-policy attribution **[std]** (11) |
| Market level | 4.0% of life provisions for individual contracts at end-2025 (4.3% end-2024, 4.9% end-2023); 2.0% collective. Bancassureurs 4.2%, traditional insurers 3.6% | [R14] [R16]; PPB stock EUR 53.6 bn at end-2024, −11.1% on end-2023 [REG-R47] |
| Purpose | Smoothing: over 1999–2023 the mechanism divides the volatility of credited rates by five relative to markets and redistributes about 1.6% of encours per year between cohorts | [R14, box 2](#frlib-assurance_vie_euro-r14) [S9] |
| Exceptional `reprise` | Permitted only where the life technical account was negative in the last financial year **and** the SCR is no longer covered, under an ACPR-approved recovery plan with restitution within eight years | [REG-R16]; out of scope **[std]** (12) |
| HCSF power | The Haut Conseil de stabilité financière may modulate the rules for constituting and releasing the PPB | [R8, 5° bis](#frlib-assurance_vie_euro-r8) [REG-R13] |

### Levies and taxation of the euro support

| Parameter | Representative value | Basis |
|---|---|---|
| `Prélèvements sociaux` rate | 17.2% | [S3] |
| `Prélèvements sociaux` timing | On the euro support, **as the products are credited to the contract** each year (`au fil de l'eau`), whether or not anything is withdrawn; the UC portion is charged only at `dénouement` or on death | [R9, art. L136-7 II](#frlib-assurance_vie_euro-r9) |
| Composition of the 17.2% | CSG 9.2% + CRDS 0.5% + prélèvement de solidarité 7.5% | [unverified]; neither art. L136-8 CSS nor art. 235 ter CGI was retrieved |
| Levy base | The interest actually credited, net of the management charge | **[std]** (13) |
| Income tax on surrender | 12.8% before eight years; 7.5% after eight years on products from premiums within EUR 150 000, 12.8% on the excess fraction; annual allowance EUR 4 600 single / EUR 9 200 jointly taxed | [S1] [S3] [R10] [R11] [REG-R40] |
| Death levy, premiums paid before age 70 | EUR 152 500 abattement per beneficiary, then 20% to EUR 700 000 and 31.25% above | [R12] [S1] [REG-R41] |
| Death duties, premiums paid after age 70 | Ordinary inheritance scale on the **premiums** only, after a global EUR 30 500 abattement | [R13] [S1] [REG-R41] |
| Capital/gain split of a partial surrender | Not stated in any retrieved document | [unverified] |

### Anchor model cell

| Parameter | Representative value | Basis |
|---|---|---|
| `épargne acquise` at the valuation date | EUR 100 000.00 | **[std]** (14) |
| Completed policy years at the valuation date | 5 | **[std]** (14) |
| Age at `adhésion` / attained age | 55 / 60, male | **[std]** (14) |
| `Versements libres programmés` | EUR 2 400 p.a., paid evenly through the year | **[std]** (14); above the EUR 50 monthly minimum [S1] |
| `Rachats partiels programmés` | EUR 3 000 p.a. from projection year 6, paid evenly through the year | **[std]** (14); above the EUR 150 monthly minimum, and the balance stays above the EUR 10 000 floor [S1] |
| `Frais sur versement` / `frais de gestion` | 0.00% / 0.60% p.a. | [S1] [S3] [S13] / [S3] |
| TMG | 0.00% | **[std]** (7) |
| PPB attributed at the valuation date | EUR 4 000.00, in eight equal vintages of EUR 500.00 | 4.0% [R14]; attribution and vintage split **[std]** (11) |
| Reference `taux servi` target | 2.30% p.a. net | **[std]** (9) |
| `Prélèvements sociaux` | 17.2% | [S3] |

Footnotes to [std] rows:

1. Every retrieved contract is multisupport [S1] [S2] [S3] [S4] [S9], but the euro
   support is separately valued, separately charged and separately revalued, and the PB
   machinery does not reach the UC part [R5, art. A132-10](#frlib-assurance_vie_euro-r5) [R9]. Modeling the euro
   support alone is a clean cut, not an approximation; the UC compartment is the sibling
   product `assurance_vie_uc`.
2. Observed: EUR 20 at Afer [S9] [S10]; EUR 10 individual / EUR 20 joint at MACSF [S2];
   none at MAIF [S13]. A bank-distributed contract has no association and no fee [S1];
   zero keeps the fee out of the account roll-forward.
3. The retrieved documents split cleanly. **Gross-style** (floor = premiums net of entry
   charges): Suravenir Rendement [S4], Afer's Fonds Garanti [S9], CNP Perspective Capi
   [S8]. **Net-of-management-charges**: Suravenir Rendement 2 and Opportunités 2 [S3]
   [S4], CNP Nuances 3D and Nuances Plus [S6] [S7], Suravenir's fund-level disclosure
   [S5]. Both designs run inside one insurer and even inside one notice [S4]. The net
   form is chosen as the modern design and the one whose arithmetic the published minimum
   surrender tables actually show [S3]. The date of the market shift from gross to net is
   [unverified] — no retrieved document dates it.
4. Observed contract levels: 0.475% [S9] [S10], 0.50% max [S2], 0.60% [S3] [S4], 0.75%
   max [S1], 0.80% [S13]. The ACPR's *actual* ratio of charges paid to average
   mathematical provisions was **0.63%** for individual contracts in 2025 (0.62% in
   2024), half of all undertakings between 0.5% and 0.8% [R14]. 0.60% is a real contract
   rate [S3] in the middle of that band; [S1], [S2] and the Opportunités 2 rate are
   stated as *maxima*, not actuals [R14].
5. No retrieved notice writes the charge formula; the eight-year minimum surrender-value
   tables settle it arithmetically. Suravenir publishes 994.00, 988.03, 982.10, 976.21,
   970.35, 964.53, 958.74, 952.99 for a EUR 1 000 net contribution at 0.60% with no PB
   [S3] — EUR 1 000 × (1 − 0.006)^n, truncated to the cent — and MACSF publishes 965.15,
   960.32, 955.52 for EUR 970 at 0.50%, which is 970 × 0.995^n [S2]. Both are a charge on
   the running balance, so the model levies it on the average balance over the year.
   BoursoVie's base including the year's PB [S1] is the observed variation; see
   `technical-notes.md`, known modeling pitfalls.
6. Suravenir states plainly that the fund's own 0.24% + 0.03% costs are internal to the
   fund and exclude the contract's charges [S5]. A `taux servi` quoted net of contract
   charges [R14] is already net of both, so deducting the fund's internal costs again
   double-counts. Afer caps its fund's asset-management charge at 0.1% of assets under
   management excluding OPCVM [S9].
7. **No public figure exists for the TMG of any contract in this set.** Meilleurtaux
   Placement Vie 2 and Croissance Avenir state no guaranteed interest rate at all under
   their "Rendement minimum garanti et participation" heading [S3] [S4]; BoursoVie names
   a TMG "annoncé en début d'année" without its value [S1]; MACSF names a board-set art.
   A132-3 rate without giving it [S2]; Afer names a `Taux Plancher Garanti` without
   giving it [S11]. Zero is the design the two Suravenir contracts describe. The nearest
   public anchor — the ACPR's average `taux technique` of 0.32% in 2025 [R14] — is a
   different quantity, the maximum rate at which the insurer's commitments are
   discounted, fixed at subscription and gross of charges, and must not be substituted.
8. Contractual PB is the exception: "il n'est pas prévu de participation aux bénéfices
   contractuelle" [S1], and likewise on the Rendement 2 / Opportunités 2 funds [S3] [S4].
   Where it exists it is specific — Suravenir Rendement fixes **90%** with the profit
   account written out in full [S4], Afer's Fonds Garanti **100%** of the net financial
   profits of the ring-fenced fund [S9]. A contractual percentage removes the insurer's
   discretion over the numerator; the composite keeps that discretion and floors it at
   the statutory minimum.
9. No insurer's forward crediting policy is public. 2.30% is the **bottom of the band
   covering 50% of encours** in 2025 (2.3%–2.9%) [R14] and matches an unbonused
   contract's position: the market mean was 2.63% and the least-revalued homogeneous
   group inside an insurer sat 0.39 point below its own mean [R14], about 2.24%. It is a
   target, not an outcome — the model credits it only where the statutory floor and the
   PPB allow (see `technical-notes.md`).
10. The ACPR observes UC-conditioned uplifts "souvent de 100 points de base, et allant
    jusqu'à plus de 200 points de base" [R14], but **no retrieved contract publishes its
    bonus grid**. Modeling one would mean inventing the grid, so the composite prices the
    unbonused rate and treats the bonus as a scenario overlay.
11. The PPB is collective and is not attributed to individual contracts in law;
    attributing a per-policy share is the device that makes the eight-year clock visible
    at model-point level. The 4.0% level is the ACPR's end-2025 ratio for individual
    contracts [R14], corroborated by France Assureurs' EUR 53.6 bn PPB stock at end-2024,
    about 4% of euro-support provisions [REG-R47]. The **eight equal vintages** are a
    steady-state construction — a fund that has run the art. A132-16 clock for eight
    years carries roughly one eighth of its PPB in each open vintage — and no insurer
    publishes its own vintage profile.
12. Art. A132-16-1 permits an exceptional `reprise` only on two cumulative conditions —
    a negative life technical account in the last financial year **and** an uncovered SCR
    — with an ACPR-approved recovery plan and a distribution ban until restitution
    [REG-R16]. It is a solvency-stress management action, not a projection assumption.
13. Art. L136-7 II fixes the *timing* of the levy on euro-denominated rights but not the
    base [R9], and no retrieved product document says whether the base is gross or net of
    the management charge. The model uses the interest actually inscribed on the
    contract, i.e. net of the charge, because that is the amount the contract's value
    rises by. The refund mechanism where levies taken at inscription exceed those finally
    due at `dénouement` was not retrieved and is [unverified].
14. Pure modeling anchor chosen to exercise the mechanics: an in-force cell five years
    in, so the eighth policy anniversary — the tax threshold that drives the surrender
    spike [R10] [REG-R40] — falls inside the projection; a programmed payment and a
    programmed partial surrender so that both the `prorata temporis` weighting [S1] and
    the account release path are exercised. The amounts are not priced values.

---

## Contractual mechanics

**The account.** The policyholder's balance on the euro support is the `épargne
acquise`, the per-contract share of the fund's `provision mathématique` — the first of
the eleven technical provisions a French life insurer carries [REG-R6]. BoursoVie
computes it **daily in compound interest** and credits the year's PB at 31 December value
date [S1]; the reference model works on a monthly grid with 31 December as the single
crediting date.

**The capital guarantee.** The composite carries the `garantie nette`: the floor equals
premiums net of entry charges, **reduced each year by the annual management charges**
[S3] [S5] [S6] [S7]. CNP states it most plainly — the contract "ne comporte pas de
garantie en capital au moins égale aux sommes versées nettes de frais sur versement,
mais il comporte une garantie en capital au moins égale aux sommes versées, nettes de
frais sur versement et nettes de frais de gestion annuels" [S6]. The floor is measured
**before** `prélèvements sociaux` and income tax, because the published minimum
surrender-value tables are explicitly before both [S1] [S2] [S3]. Where a notice says
only "nettes de frais" without saying which charges — MACSF's wording — the eight-year
table is the tiebreaker, and MACSF's falls at 0.50% a year [S2].

**Effet cliquet.** The insurers "garantissent définitivement le maintien total des
résultats acquis au 31 décembre de chaque année par un mécanisme appelé « effet de
cliquet »" [S9]; once a year's distribution has been credited "elle ne peut plus être
remise en cause" [S9], and it "est alors définitivement acquise à l'adhésion. Elle sera,
elle-même, revalorisée dans les mêmes conditions que les versements effectués" [S1]. The
ratchet is a statement about **credited interest**, not about the account balance: on a
`garantie nette` contract the balance can still fall, because the management charge
continues to bite in a year of zero PB. Both propositions are true at once and a model
must implement them separately.

**The annual crediting cycle.** The board fixes the rate for the closing year —
BoursoVie and MACSF credit at 31 December value date [S1] [S2], CNP describes the PB as
awarded "au 31 décembre de chaque année" [S6] [S7], Suravenir's Directoire decides during
Q1 of the following year and then applies it [S3] [S4]. The per-contract allocation is
the PB rate applied to the adhesion's mathematical provision on the fund, **weighted by
the time the sums were present on the fund during the year** [S1]. The management charge
is levied on the same date, on a base that at BoursoVie includes the year's PB [S1];
Afer applies its 0.475% "après affectation de la participation aux bénéfices" [S9].

**In-year `dénouement`.** Every insurer needs a rule for a policyholder leaving before
31 December, and all four devices are a floor rate applied `pro rata temporis`: the TMG
announced at the start of the year — "seul le taux minimum garanti annoncé en début
d'année sera attribué au prorata temporis" [S1]; the board-set art. A132-3 rate [S2]; the
annual Suravenir rate [S3]; or Afer's `Taux Plancher Garanti`, which alone carries a
following-year top-up to the definitive fund return [S11]. BoursoVie credits the full
annual PB to sums surrendered or switched during the year **provided the adhesion is
still in force on the following 1 January** [S1].

**The statutory participation floor.** The obligation to share technical and financial
results is statutory [REG-R14] and its mechanics sit in the arrêté [R5] [REG-R15]. The
`compte de participation aux résultats` is credited with **85% of the balance of the
`compte financier`**, and with the balance of the `compte technique` **less the insurer's
own share**, that share being the **greater of 10% of the credit balance and 4.5% of
annual premiums** [R5, art. A132-11](#frlib-assurance_vie_euro-r5) [R6, art. A331-4](#frlib-assurance_vie_euro-r6) [REG-R15]. The popular statement
of this rule — "90% of financial results and 85% of technical results" — is the wrong way
round and is not what the article says; the ACPR restates the correct form directly, that
only 85% of the `compte financier` "lui est destiné pour sa revalorisation, directement
ou par l'intermédiaire de la PPB", and that "certains contrats peuvent contractuellement
prévoir un pourcentage plus élevé" [R14, fn 12](#frlib-assurance_vie_euro-r14). Two consequences matter for a model. The
policyholder share of a *positive* technical balance is at most 90% and can be materially
less when premiums are large relative to the technical result, because the
4.5%-of-premiums limb then binds instead of the 10% limb. And the minimum is determined
**globally, not contract by contract** [REG-R15], with equal treatment required between
paid-up and premium-paying contracts of the same category and the same mathematical
provision [R5, art. A132-17](#frlib-assurance_vie_euro-r5).

**The PPB and its eight-year clock.** The participation may be credited directly to
mathematical provisions **or** carried, wholly or partly, to the `provision pour
participation aux bénéfices`; sums carried there must be applied to mathematical
provisions or paid to policyholders **within the eight financial years following** the
year in which they were carried [R5, art. A132-16](#frlib-assurance_vie_euro-r5) [R6, art. A331-9](#frlib-assurance_vie_euro-r6) [REG-R16]. MACSF
restates the limit in the contract itself — "les sommes portées à cette provision sont
affectées à la provision mathématique de chaque contrat dans un délai maximum de 8 ans"
[S2] — and Afer gives the purpose in the insurer's own words: part of the fund's revenues
may go to the PPB "afin de lisser les rendements … dans le temps et de constituer des
réserves pour pallier des revenus à la baisse", the dotation, management and release
being handled jointly through the association's supervisory committee [S9]. The clock is
what makes the PPB a *bounded* smoothing device: money parked in it is deferred, never
cancelled.

**`Prélèvements sociaux`.** This is the mechanic that most distinguishes a French euro
fund from any foreign guaranteed account. Under art. L136-7 II of the Code de la
sécurité sociale, products attached to contracts **whose rights are expressed in euros**
are charged "lors de leur inscription au bon ou contrat" — that is, **each year as the
PB is credited**, whether or not anything is withdrawn — while the unit-linked portion
is charged only at `dénouement` or on the insured's death [R9]. Under a multisupport
contract the euro portion follows the annual rule and the UC portion waits [R9]. The
contracts corroborate it: Suravenir's `dynamisation des plus-values` option switches the
euro fund's annual gain to UC "diminuée des prélèvements sociaux" [S3], and Boursorama's
tax annexe puts the products under art. L136-7 [S1]. The rate is **17.2%** [S3]. The
consequence for a projection is arithmetic and unavoidable: the euro account compounds
**net of 17.2% of each year's credited interest**, and the published minimum
surrender-value tables cannot be used to calibrate this because they are stated before
social and tax levies [S1] [S2] [S3].

**`Rachat`.** Every contract carries a `faculté de rachat`, partial or total, at any
time [S1] [S2] [S3] [S6]; the euro support is one the investor "peut racheter
unilatéralement et à tout instant" [S5]. Settlement is within two months by statute [R7]
[REG-R31], restated by BoursoVie and MACSF [S1] [S2] and contracted at 30 days by
Suravenir and CNP [S3] [S6]; late payment bears interest at 1.5× the legal rate for two
months then twice the legal rate [R7] [S3]. There is no surrender penalty — 0% or EUR 0
in every fee table retrieved [S2] [S10] [S13]. Absent instruction, BoursoVie surrenders
first from Eurossima, then Euro Exclusif, then the largest UC [S1]: an unspecified
withdrawal drains the euro fund first, which matters for any multisupport model. Two
things block liquidity — an `avance` in force suspends most options [S1] [S3], and once
a designated beneficiary has accepted under art. L132-9 the policyholder can no longer
surrender, take an avance, revoke the beneficiary or pledge the contract without that
beneficiary's agreement [S1] [S3].

**Death benefit.** The death capital equals the contract's account value — the `épargne
acquise` — determined at the date the insurer learns of the death, less outstanding
`avances` and their interest, plus any optional death cover [S3]. There is **no
additional guarantee on the euro part**: the capital floor already prevents a loss, which
is why the optional death riders exist only for the UC part [S3] [S4]. The euro part
carries its own in-year revaluation on the rules above [S1] [S2] [S11], and statutory
revaluation from death to settlement is required by art. L132-5 [S3]. Settlement is 30
days from a complete file at Suravenir with penalty interest at double then triple the
legal rate [S3], two months at BoursoVie [S1]; the statutory clock is fifteen days to
request documents and one month from the complete file [REG-R31]. Sums unclaimed for ten
years transfer to the Caisse des dépôts and become State property after twenty [REG-R39].

**Loi Sapin 2 / HCSF.** The Haut Conseil de stabilité financière may, on a proposal of
the Governor of the Banque de France and to prevent a serious and characterised threat
to financial stability, temporarily limit the payment of surrender values, restrict the
free disposal of assets, defer or restrict `arbitrages` and `avances`, and limit the
acceptance of premiums [R8, art. L631-2-1 5° ter](#frlib-assurance_vie_euro-r8) [REG-R13]. Measures run for **at most
three months, renewable**, with the surrender-value restriction capped at **six
consecutive months** [R8] [REG-R13]. Suravenir discloses the power but describes the
whole of it as "temporaire (maximum 6 mois renouvelable)" [S5]; the statute governs, and
the divergence is recorded rather than propagated. Whether the mechanism has ever been
triggered is [unverified]. It is **out of the projection's scope**, and
`technical-notes.md` says so rather than pretending the model covers it.

---

## Riders and options

**In scope (modeled as flags or as scenario overlays):**

- **`Avance`** (policy loan), offered by every insurer here but on terms held outside the
  notice: BoursoVie and MACSF refer to a separate "Règlement Général des Avances" the
  member must sign [S1] [S2], and Suravenir grants one "sous réserve de l'accord de
  Suravenir, dont les modalités et la tarification lui seront communiquées sur simple
  demande" [S3]. The insurer may grant advances up to the surrender value [REG-R31].
  **No rate, no maximum `quotité` and no maximum term is published in any retrieved
  document**; the usual market description (60–80% of the euro savings, up to three
  years renewable, at the credited rate plus a margin) is [unverified]. Modeled as an
  off-by-default flag with **[std]** parameters; outstanding advances and their interest
  are deducted from the death capital and any settlement [S3].
- **Optional death cover on the UC part.** Suravenir's rider covers the `capital sous
  risque` — the positive difference between cumulative net premiums and the surrender
  value — with a **one-year waiting period**, entry ages 12 to under 70, no medical
  formalities, at monthly premiums of **0.15‰ to 5.15‰ of capital at risk by age** [S3]
  [S4]; MACSF's automatic `garantie plancher` to the member's 70th birthday costs 0.10%
  p.a. on UC [S2]; Afer's non-optional death floor 0.055% p.a. of UC and eurocroissance
  savings [S9] [S10]; Suravenir's accidental-death option adds 0.14% to the annual charge
  [S3] [S4]. **These riders price the UC risk, not the euro risk**, and the composite
  carries no euro-side death rider.
- **`Sécurisation` and `dynamisation des plus-values`**, switching the euro fund's gain
  to UC above EUR 100 [S1] or EUR 25 cumulative [S3], the gain moving "diminuée des
  prélèvements sociaux" [S3]; BoursoVie's `sécurisation` option costs 1% max of the
  amount transferred [S1]. A scenario overlay on the account release, not a euro-fund
  mechanic.
- **Annuity conversion**, at 3% of `arrérages` at Afer [S10], MAIF [S13] and Suravenir
  [S3] [S4]. The resulting liability is the sibling product `rente_viagere`; this
  specification stops at the conversion.

**Out of scope for the composite:** the UC compartment and its `arbitrage` machinery
(sibling `assurance_vie_uc`); the `eurocroissance` support offered alongside the euro
fund on two retrieved contracts [S1] [S9] (sibling `eurocroissance`); UC-holding bonuses,
because no contract publishes its grid [R14]; beneficiary acceptance under art. L132-9
[S1] [S3]; the `réserve de capitalisation` and the other general-account technical
provisions [REG-R6] [REG-R7] [REG-R8]; and the HCSF suspension power [R8] [REG-R13].

---

## Variations across insurers

| Feature | BoursoVie — Generali Vie [S1] | RES Multisupport — MACSF [S2] | Meilleurtaux Placement Vie 2 / Croissance Avenir — Suravenir [S3] [S4] | Nuances 3D / Plus — CNP [S6] [S7] | Multisupport Afer — Abeille [S9] [S10] | ARS — MAIF VIE [S13] |
|---|---|---|---|---|---|---|
| Wrapper | Group, bank-distributed | Group via association AMAP | Group via associations VIREA / SEREP | Group, bank-distributed | Group via association Afer | Group, mutual-distributed |
| Capital guarantee | Premiums net of charges | "nettes de frais", but the 8-year table erodes at 0.50% p.a. | Rendement: gross; Rendement 2 / Opportunités 2: **net of annual management charges** | **Net of annual management charges** | Premiums net of **entry** charges | Not stated in the fee table |
| Contractual PB | None — statutory allocation under A132-16 | None stated — statutory allocation at 31 Dec | Rendement **90%**, profit account written out in full; Rendement 2 / Opportunités 2 none | None — PB awarded at 31 Dec | **100%** of the net financial profits of the ring-fenced fund | Not stated |
| PPB in the notice | Via art. A132-16 | Yes, with the **8-year** release limit | Yes — the whole positive balance carried to a shared PPB | Not in the DIC | Yes, managed through the Comité de Surveillance | Not stated |
| In-year rate on `dénouement` | TMG announced at the start of the year, pro rata | Board-set A132-3 rate, pro rata | Rate set at least annually, pro rata | Not stated in the DIC | **Taux Plancher Garanti**, pro rata, with a next-year top-up [S11] | Not stated |
| `Frais sur versement` (euro) | 0% | **3% max** | 0% | Entry-cost impact 0.45%–1.09% p.a. at 8 years, all options | **0.5%** | 0% |
| `Frais de gestion` (euro) | 0.75% max | 0.50% max | 0.60% (Rendement 2) | Not disclosed separately | **0.475%** | **0.80%** |
| Settlement deadline | 2 months | 2 months | **30 days** | **30 days** | Not extracted | Not stated |
| Distinctive feature | Daily compounding of the euro account | High entry charge, low annual charge | Two generations of euro fund in one notice, one gross-guaranteed and one net | The plainest published statement of the net guarantee | Association governance, 100% PB, ring-fenced fund, Taux Plancher Garanti | Zero entry charge, EUR 30 entry ticket |

What actually varies, in order of importance for a model:

1. **Whether the guarantee erodes.** Gross-guaranteed funds hold the floor at premiums
   net of entry charges [S4] [S8] [S9]; net-guaranteed funds let it fall by the
   management charge every year [S3] [S4] [S6] [S7]. Both designs coexist at the same
   insurer and inside the same notice [S4]. This is the single largest structural
   difference and it changes the shape of the guarantee cost, not merely its level.
2. **Where the charge sits.** The mutual and association contracts front-load (MACSF 3%
   entry / 0.50% annual; Afer 0.5% / 0.475%), the online and bancassurance contracts
   charge nothing at entry and more annually (BoursoVie 0% / 0.75% max; MAIF 0% / 0.80%;
   Suravenir 0% / 0.60%) [S1] [S2] [S3] [S10] [S13]. Over eight years these are not
   equivalent, and the ACPR's 0.63% actual sits in the middle of the annual cluster
   [R14]. Note also that three of these levels are stated as *maxima*, not actuals
   [S1] [S2] [S3].
3. **Whether PB is contractual.** Most contracts leave the sharing to the statutory
   minimum and the insurer's discretion [S1] [S3]; Suravenir Rendement fixes 90% with a
   written profit account [S4], Afer 100% of the net financial profits of a ring-fenced
   fund [S9]. A contractual percentage removes the insurer's discretion over the
   numerator and, with it, most of the PPB lever.
4. **The in-year credited rate.** All four named devices — TMG [S1], the A132-3 board
   rate [S2], the annual Suravenir rate [S3], the `Taux Plancher Garanti` [S11] — are a
   floor rate applied `pro rata temporis`; Afer alone commits to a following-year top-up
   to the definitive rate [S11].
5. **Bonuses.** The ACPR observes UC-conditioned uplifts of 100 to more than 200 basis
   points and a 0.99 point spread between the best- and worst-revalued contract groups
   inside a single insurer [R14], and **no retrieved notice publishes its bonus grid** —
   a variation that is large, real and undocumented at contract level.
6. **Settlement speed**, 30 days [S3] [S6] against the statutory two months [S1] [S2]
   [R7].

Two limits on this comparison are worth stating. The insurer sample is six groups across
thirteen retrieved documents, which supports the structural claims but not a market-wide
charge distribution — for that, use the ACPR's own distribution [R14]. Thirteen and not
fourteen because one document could not be retrieved: the Afer Génération notice
returned HTTP 404 [S14], so Afer EuroGénération's mechanics, including the reported
eight-year loyalty bonus, are [unverified]; only its 2025 rate of 4.05% is sourced
[S11] [S12].

---

## Regulatory context

**Profit participation and guaranteed rates.** The obligation is statutory — life and
capitalisation undertakings "doivent faire participer les assurés aux bénéfices
techniques et financiers qu'elles réalisent" — with the mechanics delegated to an arrêté
[REG-R14]. Those mechanics are arts. A132-10 to A132-17 [R5] [REG-R15] [REG-R16],
formerly A331-3 to A331-9 [R6]; insurers still cite the old numbering [S4], but the
operative modern text is the A132 series and Légifrance served the A331 articles only in
historic versions [R6]. The minimum is determined **globally**, not contract by contract,
and `contrats à capital variable` — the UC part — are outside the machinery
[R5, art. A132-10](#frlib-assurance_vie_euro-r5) [REG-R15], as are eurocroissance contracts under art. L134-1
[REG-R15]. On the guaranteed side, art. A132-2 permits an insurer to guarantee a
**total of technical interest plus profit participation** — not a separate credit stacked
on the technical rate — related to the fraction of mathematical provisions the guarantee
covers [R3] [REG-R18]; art. A132-3 caps those rates and fixes their duration [R4]
[REG-R18]; and arts. A132-1 and A132-1-1 fix the maximum technical rate that anchors the
cap at 75% of the `taux moyen des emprunts d'État` (TME), and beyond eight years the
lower of 3.5% and 60% of the TME, moving on a 0.25-point grid floored at zero and
changing only when the monthly reference rate has fallen 0.10 point or risen 0.35 point,
with three months to implement [R1] [R2] [REG-R17].

**Technical provisions.** A French life insurer carries **eleven** technical provisions
under art. R343-3, each engagement provisionable under exactly one of them [REG-R6]. Two
are load-bearing here: the **`provision mathématique`**, the difference between the
actuarial present values of the two sides' commitments *including future management
costs* — which is why a French PM is not a net-premium reserve — and the **PPB**, profit
shares attributed but not payable immediately after the close of the year that produced
them [REG-R6]. Three more shape the general account behind the fund without appearing in
this model: the `réserve de capitalisation`, the `provision pour risque d'exigibilité`
(one third of any net overall unrealised depreciation on the exposed assets) [REG-R7],
and the `provision pour aléas financiers`, whose mechanics are recorded from a retrieved
text but whose current article reference is [unverified] after the 2016 recodification
[REG-R8] [REG-R9].

**Contract law and information.** Art. L132-21 requires the contract to state how the
surrender, transfer and paid-up values are computed, forbids reduction charges against
the mathematical provision, permits `avances` up to the surrender value and caps
surrender settlement at two months [R7] [REG-R31]. Art. L132-22 fixes the annual
statement's contents, including "le rendement garanti et la participation aux bénéfices
techniques et financiers", and requires the insurer to publish average guaranteed
returns, average charge rates and the average net return served, contract by contract,
within 90 business days of 31 December, keeping it online five years [REG-R31]. Arts.
A132-4 and A132-8 prescribe the `note d'information` and the one-page `encadré`,
including PB percentages and charges in four categories **with maximum amounts or
percentages** [REG-R30] — which is why the retrieved notices give maxima and not levels,
and why every charge level here is either a contract maximum or **[std]**. Renunciation
is 30 full calendar days with a thirty-day repayment obligation [REG-R29] [S2] [S6]
[S9], and the minimum surrender values of the first eight years must appear in the
notice, as they do in every notice retrieved [S1] [S2] [S3] [S4].

**Macroprudential and prudential.** Art. L631-2-1 5° ter gives the HCSF the
surrender-limitation power described above and 5° bis lets it modulate PPB constitution
and release [R8] [REG-R13]. French insurers are supervised under Solvabilité II as
transposed into the Code des assurances; technical provisions are a **best estimate** —
the probability-weighted average of future cash flows discounted at the relevant
risk-free term structure — plus a **risk margin** [REG-R4], and EIOPA publishes those
term structures monthly with the volatility adjustment, the matching-adjustment
fundamental spreads and the ultimate forward rate [REG-R5]. The Solvency II treatment of
the euro fund's **future discretionary benefits** — the PPB and the discretionary share
of the credited rate — of management actions and of the time value of the capital
guarantee could not be read from a retrieved instrument: EUR-Lex returned an empty body
and then HTTP 202 with zero bytes [R18], and the cross-product entries record the same
block [REG-R2]. All of it is **[unverified]** in this library, and no cost-of-capital
rate, lapse shock or expense-inflation rule here rests on a retrieved text [REG-R2].

**Mortality basis.** Art. A335-1 permits exactly two kinds of table: homologated tables
by sex, built on insured populations for annuity contracts and on **INSEE** data for
other contracts, or an undertaking's own experience table certified by an independent
actuary [REG-R23]. For a euro fund the death benefit is the account value, so mortality
drives the *timing* of `dénouement` rather than the amount; the reference decrement table
is a **[std]** proxy built from the freely redistributable INSEE series [REG-R24], and
TH 00-02 / TF 00-02 are cited by name and article [REG-R23] but not shipped.

**Taxation.** Income taxation of surrenders sits at art. 125-0 A CGI [R10] [REG-R40] and
art. 200 A CGI [R11]; the social levies and their `au fil de l'eau` timing on
euro-denominated rights at art. L136-7 CSS [R9]; death taxation at arts. 990 I and 757 B
CGI [R12] [R13] [REG-R41]. The **EUR 150 000** premium threshold above which the 7.5%
rate stops applying to the excess was verified in art. 200 A [R11] but not in the text of
art. 125-0 A retrieved for the cross-product library, where it is [unverified] [REG-R40].
Tax is a behavioural driver here rather than a model output: a projection that puts no
surrender spike at policy year eight has ignored it [REG-R40].

**Guarantee fund and professional standards.** The `Fonds de garantie des assurances de
personnes` compensates up to **EUR 70 000 per insured, adherent or beneficiary per
company**, whatever the number of contracts [S6]; Suravenir contributes annually under
arts. L423-1 et seq. [S5]. Model documentation sits under the Institut des actuaires'
NPA 2, a category-3 recommended practice in force since 1 January 2016 applying "à tout
modèle actuariel" under a proportionality principle [REG-R44]. French listed insurers
report under IFRS 17 from 2023; the fonds en euros is the archetypal direct-participating
contract, but the variable fee approach's mechanics were not read from the standard text
and are [unverified] [REG-R45].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-assurance_vie_euro-r1
[R10]: #frlib-assurance_vie_euro-r10
[R11]: #frlib-assurance_vie_euro-r11
[R12]: #frlib-assurance_vie_euro-r12
[R13]: #frlib-assurance_vie_euro-r13
[R14]: #frlib-assurance_vie_euro-r14
[R15]: #frlib-assurance_vie_euro-r15
[R16]: #frlib-assurance_vie_euro-r16
[R17]: #frlib-assurance_vie_euro-r17
[R18]: #frlib-assurance_vie_euro-r18
[R2]: #frlib-assurance_vie_euro-r2
[R3]: #frlib-assurance_vie_euro-r3
[R4]: #frlib-assurance_vie_euro-r4
[R5]: #frlib-assurance_vie_euro-r5
[R6]: #frlib-assurance_vie_euro-r6
[R7]: #frlib-assurance_vie_euro-r7
[R8]: #frlib-assurance_vie_euro-r8
[R9]: #frlib-assurance_vie_euro-r9
[REG-R13]: #frlib-reg-r13
[REG-R14]: #frlib-reg-r14
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R17]: #frlib-reg-r17
[REG-R18]: #frlib-reg-r18
[REG-R2]: #frlib-reg-r2
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R31]: #frlib-reg-r31
[REG-R39]: #frlib-reg-r39
[REG-R4]: #frlib-reg-r4
[REG-R40]: #frlib-reg-r40
[REG-R41]: #frlib-reg-r41
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R47]: #frlib-reg-r47
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[REG-R7]: #frlib-reg-r7
[REG-R8]: #frlib-reg-r8
[REG-R9]: #frlib-reg-r9
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
