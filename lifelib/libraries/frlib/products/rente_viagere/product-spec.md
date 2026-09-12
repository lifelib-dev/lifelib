# Product Specification

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of the French individual immediate life annuity — the
*rente viagère immédiate*. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents) and [R#]
(regulatory/actuarial references), both numbered per `_research/rente-viagere.md` and
resolved in `sources.md` (same directory) — were extracted from the cited document.
[REG-R#] tags resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, frozen at
R1–R49 and distinct from the product research file's). Values marked **[std]** are
standardizations introduced for the reference implementation; each [std] table row
carries a numbered footnote giving the rationale and, where the research recorded one,
the observed range across insurers. Facts the research file could not verify are flagged
[unverified] here too. French terms of art are kept in French and glossed on first use.
Amounts are in euros and this document uses the English decimal point and thousands
comma; quoted French text keeps its original comma decimal. The mechanics anchor is the
Suravenir PER/PERP annuity [S2] [S3], with Carac [S1], Spirica [S4], CNP [S5] and
Préfon-Retraite [S6] as the informative departures.

---

## Product overview and market role

A *rente viagère immédiate* is the exchange of a *capital constitutif* (the converting
capital) for a stream of *arrérages* (annuity instalments) payable while the annuitant
lives. The same liability arises three ways and the mechanics differ only at the edges:
as a standalone single-premium annuity contract [S1] [S8]; as the *liquidation en rente*
of a retirement wrapper — a PER, an older PERP or Madelin, or a points régime
[S2] [S3] [S4] [S5] [S6] [S9]; or as the *sortie en rente* of an *assurance vie*. No
*assurance vie* notice describing that last route was retrieved, so its contract-specific
detail is [unverified]; the pricing and payment mechanics below are common to all three.
The PER route has a statutory anchor: a plan must offer the possibility of acquiring a
*rente viagère* at maturity with a reversion option, and the *versements obligatoires*
compartment must be liquidated as an annuity [REG-R34] [S4].

Four structural facts hold across every retrieved carrier and a model must not
parametrize them away. **Payment is *terme échu* — in arrears** [S1 Art. C13] [S2] [S3]
[S5] [S6] [S7 Art. 6.3] [S9]; no retrieved French document offers a *terme à échoir*
option, a real difference from the UK market where both conventions are standard.
**There is no contractual indexation**: no inflation-linked, LPI-equivalent or
fixed-percentage escalating annuity appears anywhere in [S1]–[S9], and uprating is
*revalorisation* out of the *participation aux bénéfices* (profit sharing) —
discretionary, annual and non-negative, not an escalation guarantee. **There is no
surrender after liquidation**: "les rentes viagères immédiates ou en cours de service ne
peuvent comporter ni réduction ni rachat" [R8, verbatim](#frlib-rente_viagere-r8), the capital being *aliéné*
(alienated), with the statutory commutation of a small annuity as the single exception
[R9] [R10]. And **the mortality basis is annuitant-experience, generational and
floored**: the homologated tables are **TGH05** (male) and **TGF05** (female), applicable
to *contrats de rente viagère* from 1 January 2007 [R1 art. 2, verbatim](#frlib-rente_viagere-r1) [REG-R21], and
an insurer using its own certified table may never price an annuity below what the
appropriate homologated table would give [R3, verbatim](#frlib-rente_viagere-r3) — a one-sided floor, and the
single most important structural fact about French annuity pricing.

On top of those sits the mechanic with no counterpart in the UK or US siblings: **the
tariff must be unisex while the mandatory tables remain sex-distinct**. Where a single
homologated table is applied to all lives it must be "la table appropriée conduisant au
tarif le plus prudent" [R3, verbatim](#frlib-rente_viagere-r3) — for an annuity, the female table TGF05. This
composite therefore prices every life on TGF05 and carries the resulting systematic
surplus on male lives back to policyholders through the *participation aux bénéfices*,
which is what the ministry says happens in practice [R17] [R18].

The representative design is Suravenir's [S2] [S3]: single premium; monthly, *terme
échu*; priced on both heads' ages, the annuitant-experience generation table in force at
the effective date and an explicit *taux technique*; a mutually exclusive option set of
*réversion*, *annuités garanties* and *rentes par paliers*; no surrender; statutory
commutation below the art. A. 160-2 floor; annual discretionary uplift at 31 December;
and a charge structure of a percentage on the instalment plus a percentage on the annuity
fund. The chassis choice is **[std]**.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-premium immediate lifetime annuity on one head, *capital aliéné*, participating through *revalorisation* | [S2] [S3] [S8]; chassis **[std]** (1) |
| Legal wrapper | Standalone *contrat de rente viagère*, or the *liquidation en rente* of a PER / PERP / points régime | [S1] [S2] [S3] [S4] [S5] [S6] [S8] [S9] [REG-R34] |
| Premium | One *capital constitutif* at conversion; no additions afterwards | [S2] [S3] [S8] |
| Minimum capital | €30,000 | [S8]; adoption **[std]** (2) |
| Entry-age band | 50–85 at the effective date | [S1 Art. C5, C8, C12]; adoption **[std]** (3) |
| Minimum annuity issued | €40 per month. Préfon adds the €120-per-quarter equivalent and measures the floor *before* the reversion and dependency options [S6 Art. 5.2.3 b)]; AG2R publishes the monthly figure alone, with no quarterly equivalent and no measurement basis [S8] | [S6 Art. 5.2.3 b)] [S8] |
| Statutory commutation threshold | €110 per month including *majorations légales*, multiplied by the number of months in the payment period | [R10 art. A. 160-2](#frlib-rente_viagere-r10) |
| Effective date | 1st day of the civil month following receipt of the complete liquidation file | [S2] [S3] [S6] |
| Irrevocability | The annuity election and every option chosen with it are irrevocable | [S1 Art. C15, C16] [S2 pt 10.e] [S3 pt 11.d] [S4 §7.3] [S5] [S6 Art. 5.4.3] [S8] |
| Surrender value | **None, ever** | [R8, verbatim](#frlib-rente_viagere-r8) [S1 Art. C3] |
| Currency | EUR | [S1]–[S9] |
| Renonciation | 30 calendar days, full refund within 30 days | [S1 Art. C7] [S7 encadré §1] [REG-R29] |
| Prescription | 2 years; 10 years where the beneficiary is not the member | [S1 Art. C20] |

Footnotes to [std] rows:

1. The Suravenir annuity [S2] [S3] is the cleanest structural representative of the
   eight retrieved carriers: it publishes the option set, the payment convention, the
   technical rate, the charge structure and the profit-sharing rule in operative terms.
   Carac's *capital réservé* fork [S1] and CNP's dependency doubling [S5] are genuine
   alternative shapes and are documented under Variations rather than defaulted.
2. Only one retrieved document states a minimum capital at all [S8]. Carac sets its
   minimum by board decision [S1]; the wrapper-exit contracts inherit the wrapper's
   accumulated value and state none [S2] [S3] [S4] [S5] [S6]. €30,000 is adopted so the
   model has a bounded premium domain.
3. Only Carac publishes an entry-age band (50–85, top-ups to 85, minimum age 50 for
   *entrée en jouissance*) [S1 Art. C5, C8, C12]. The wrapper-exit contracts state no
   band, the liquidation age being governed by the wrapper [S2]–[S6] [REG-R34]. 50–85 is
   adopted so the model has a bounded issue-age domain; it also keeps every model point
   inside the generational tables' usable region, where the construction document states
   rates exist for age + generation > 1995 [R19].

### Conversion basis — table, taux technique and the taux de rente

| Parameter | Representative value | Basis |
|---|---|---|
| Mortality tables | **TGH05** (male) / **TGF05** (female), homologated by the arrêté du 1er août 2006, mandatory for *contrats de rente viagère* from 1 January 2007 | [R1 art. 2, verbatim](#frlib-rente_viagere-r1) [REG-R21] |
| Table nature | Prospective **generation** tables: a rate is indexed by age *and* year of birth, so the mortality trend is inside the table and no separate improvement scale applies | [R1] [R19]; ages 0–120, generations 1900–2005 [R25, secondary](#frlib-rente_viagere-r25) |
| Permitted alternative | The undertaking's own table, by sex or not, built on its own or demographically equivalent experience and certified by an actuary independent of the undertaking | [R3, verbatim](#frlib-rente_viagere-r3) [REG-R23] |
| Experience-table floor | For *rentes viagères*, a tariff on an experience table may never be lower than the tariff the appropriate homologated table would give | [R3, verbatim](#frlib-rente_viagere-r3) |
| Single-table rule (unisex) | Where one homologated table is applied to all lives it must be "la table appropriée conduisant au tarif le plus prudent" — for an annuity, **TGF05** | [R3, verbatim](#frlib-rente_viagere-r3) [R25, secondary](#frlib-rente_viagere-r25) |
| Tariff table used here | TGF05 for every life, regardless of sex | [R3] [R17] [R18]; adoption **[std]** (4) |
| *Taux technique* (technical rate) | 0.00% | [S2 pt 10.d] [S3 pt 11.e] |
| Regulatory ceiling on the *taux technique* | min(3.50%, 60% × TME six-month average), on a 0.25-point ladder floored at zero, sticky to ±0.10 / ±0.35 point moves, three months to implement | [R4] [R5] [REG-R17] |
| Ceiling level in force | 2.00%, monthly reference TME 3.90%, at 31 July 2026 | [R21, secondary tracker](#frlib-rente_viagere-r21) (5) |
| *Taux de rente* (annuity rate) at age 65 | **3.30%** of the capital per annum, unisex basis | **[std]** (6) |
| Same rate on the male table TGH05 | **3.73%** — i.e. a male priced on his own table would receive **13.0%** more income | **[std]** (7) |

4. The Code does not create a unisex table; it forces the single table used to be the more
   prudent of the two sex-specific ones [R3]. The chain runs directive 2004/113/CE → the
   CJEU ruling of 1 March 2011 in case C-236/09 *Test-Achats* → the loi du 26 juillet 2013
   amending art. L. 111-7 [R17] [R18]; the eight-year statement itself — that the
   resulting surplus must in substantial part return to policyholders — is made in
   [R17] alone. [R18] cites art. A. 132-11 for the redistribution and describes unisex
   pricing as "mutual solidarity", but states neither the horizon nor "in substantial
   part". The judgment
   was not retrieved [R16], so the cut-off convention is [unverified] — the boundary is
   rendered "après le 20 décembre 2012" [R18] [R25] and "21 décembre 2012" [R17], and
   **the model must not depend on the boundary day**. No retrieved product document names
   TGH05 or TGF05 explicitly; the table is always referenced generically [S2] [S3]
   [S7 Art. 5.3].
5. A commercial tracker, not an official publication; an order of magnitude, to be
   re-derived from the TME before being relied on [R21]. The ACPR's own study could not be
   fetched (HTTP 403, two attempts); its abstract reports that zero-technical-rate
   contract families dominate every commercialisation cohort [R20].
6. **No French insurer publishes an annuity rate card** — no *taux de rente*, no annuity
   factor, no specimen annuity anywhere in [S1]–[S9] — and Spirica states expressly that
   "L'Assureur ne garantit pas le montant de la Rente avant la liquidation sous forme de
   rente" [S4 §7.3.2.3]. 3.30% is therefore a standardization, but not an arbitrary one:
   at a 0.00% *taux technique* [S2] [S3] the rate is the reciprocal of the annuity factor,
   i.e. of residual life expectancy. [R19] publishes TGF05 life expectancy at 60 of 30.6
   years (generation 1936), 40.4 (2005) and 32.0 for a female annuitant aged 60 in 2006
   (generation 1946); linear interpolation in generation reproduces that third point to
   0.02 years and gives 34.15 for generation 1961. Stepping to 65 on a **[std]** five-year
   survival of 0.985 gives a factor of about 29.63 and a raw rate of 3.375%; 3.30% carries
   an implicit loading of about 2% at a level no source publishes.
7. Same construction on the male figures of [R19] — 26.8 (1936), 36.7 (2005), 28.4 at 60
   in 2006 — giving 30.39 years at 60 for generation 1961, a factor of about 26.25 at 65
   on a **[std]** five-year survival of 0.970, and 3.73% after the same loading. Deputies
   put the male disadvantage at "environ 15 %" [R17] and "jusqu'à 20 %" [R18]; both are
   the questioners' assertions, not the ministry's, and both are [unverified]. The 13.0%
   here is of the same order and is **[std]**, not a market observation.

### Payment of the arrérages

| Parameter | Representative value | Basis |
|---|---|---|
| Payment frequency | Monthly | [S2] [S3] [S6]; representative choice **[std]** (8) |
| Payment timing | *Terme échu* (in arrears) | [S1] [S2] [S3] [S5] [S6] [S7] [S9] |
| First instalment | End of the first civil month of service; the annuity takes effect on the 1st of a civil month | [S2] [S3] [S6] |
| Cessation | Instalments "cessent d'être dus à compter du premier jour du mois qui suit le décès" — the arrérage of the month of death is due in full | [S6] |
| *Prorata d'arrérages* | Arrears accrued and unpaid at death belong to the heirs; an overpayment is owed by the estate | [S1 Art. C17.2] [S7 Art. 7.3] |
| De-minimis on the *prorata* | €15 in both directions | [S1 Art. C17.2] |
| Proof of life | Annual *attestation valant certificat de vie* plus a birth extract under three months old, returned within 30 days, failing which service is suspended from the following month until it arrives | [S2] [S3]; [S1 Art. C13] [S7 Art. 6.3] |
| Periodicity change | The insurer may change the payment periodicity, including for annuities already in payment | [S7 Art. 6.3] |
| *Terme à échoir* | Not offered by any retrieved carrier; retained as an unobserved model variant only | **[std]** (9) |

8. Observed frequencies: monthly [S2] [S3] [S6]; quarterly [S5] [S7] [S9]; semi-annual
   only, on 30 June and 31 December [S1 Art. C13]; the annuitant's choice of all four
   [S4] [S8]. Monthly is modal among the wrapper-exit contracts and is the finest grid, so
   every coarser frequency is a restriction of it. The commutation threshold scales with
   the periodicity [R10], so frequency is not a presentational choice.
9. Every retrieved contract pays in arrears. The advance convention is kept as a switch
   only because the payout chassis is shared with the UK and US siblings; it is **not** a
   French product feature, and the one shipped model point that sets it — point 11, at a
   1.00% *taux technique* — exists to exercise the branch, not to represent an observed
   contract. On that branch the *prorata d'arrérages* is zero **[std]**: the instalment
   covering the month of death was paid at the start of it, so nothing has accrued unpaid.

### Charges

Three distinct deductions exist, and every retrieved contract uses one, two or none of
them. The terminology is not standardized — "frais sur arrérages de rentes", "frais de
quittances", "frais de gestion sur arrérages" and "frais de transformation en rente" all
denote a deduction from the instalment [R24] — so a model reads each contract's own
definition rather than a market label.

| Parameter | Representative value | Basis |
|---|---|---|
| *Frais d'arrérages* (per instalment) | **3.00%** of each gross *quittance d'arrérages* | [S5 encadré] [S7 Art. 17.3]; adoption **[std]** (10) |
| *Frais sur encours de rentes* (annual, on the annuity fund) | **0.80%** a year | [S2]; adoption **[std]** (11) |
| Where the *frais sur encours* bite | On the *provision mathématique* backing the annuity, reducing the profit-sharing base — **not** the guaranteed annuity | [S1 Art. C9] [S2] [S3] [S5] [S6] [S7] |
| Cap expressed in social-security units | Spirica caps any annuity-service fee at 1% of the *Plafond Mensuel de Sécurité Sociale* per instalment while setting the rate itself at 0% | [S4 §7.3.2.3] |
| Entry charge on the capital | Out of scope: the capital modelled is the amount actually applied to the annuity, net of any entry charge | [S1] [S6] [S7 Art. 17.1] |

10. Observed *frais d'arrérages*: 3% maximum per instalment [S5 encadré]; 3% as *frais de
    transformation en rente* [S7 Art. 17.3]; **0.00%** at Suravenir [S2] [S3], Spirica
    [S4], Préfon [S6: "Il n'y a pas de frais prélevés sur les rentes servies"] and Carac
    [S1 encadré: "Autres frais: néant"]; named without a figure at AG2R [S8]. The press
    reports "around 3%", or a flat €2–5 per instalment at one insurer [R23] [R24, both
    secondary, 2 April 2015 — [unverified]]. The composite takes 3% because a non-zero
    rate exercises the mechanic; zero is a parameter setting, not a different engine.
11. Observed *frais sur encours de rentes*: 0.80% [S2]; 0.68% [S3]; 1% maximum a year on
    the *capitaux constitutifs de rente* [S5]; 2.3% maximum on the annuity support [S4];
    0.55% on *provisions mathématiques* at 31 December [S1 Art. C9]; 0.50% a year on
    managed savings [S7 Art. 17.2]; 0.70% maximum of technical provisions plus 2% of the
    net financial income of the PTS assets [S6 Art. 12]. Press range 0.60%–0.90%
    [R23, secondary](#frlib-rente_viagere-r23). 0.80% is the modal published figure among the wrapper-exit
    contracts.

### Revalorisation of the annuity in payment

| Parameter | Representative value | Basis |
|---|---|---|
| Mechanism | Annual *participation aux bénéfices* credited to the annuities in payment, increasing the annuity for the remainder of its life | [S2 pt 10.f] [S3] [S4 §7.3.2.3] |
| Date | 31 December each year; the uplift reaches instalments payable from the following 1 January | [S2 pt 10.f]; the 1 January application is a **[std]** convention (12) |
| First-year pro-rating | Annuities in service for less than one year at 1 January are revalorised pro rata temporis from the effective date to 31 December | [S3] |
| Contractual floor | Zero — every retrieved formulation is non-negative | [S1 Art. C11] [S2] [S3] [S4] [S7 encadré §3–4] |
| Guarantee status | **None.** A discretionary increase is not an escalation guarantee, and no retrieved contract promises a rate or a formula in advance | [S1]–[S7]; see also the ceilings on rates that *may* be guaranteed in advance [R6] [REG-R18], whose percentages are [unverified] |
| Profit-sharing account | Built for the *rentes en cours de service* under point III of art. A. 132-11, "en incluant le résultat technique généré par ces mêmes rentes"; the attribution is "100 % du solde créditeur du compte de participation aux bénéfices" | [S3, verbatim] [R7] [REG-R15] |
| Statutory frame | A life insurer must share technical and financial profits; sums placed in the *provision pour participation aux bénéfices* must reach policyholders within eight financial years | [REG-R14] [R7 art. A. 132-16, verbatim](#frlib-rente_viagere-r7) [REG-R16] |
| Assumed rate | **1.50%** a year | **[std]** (13) |

12. [S2] fixes the credit date ("Chaque année, au 31 décembre, les rentes servies sont
    majorées de la participation aux bénéfices") but no retrieved document says which
    instalment first carries the increase. The composite applies it from 1 January, so the
    December instalment of the crediting year is paid at the old level; the alternative
    reading is a documented ambiguity, not a modeled option.
13. No retrieved document publishes a revalorisation rate, formula or history. The rate is
    discretionary, fed by the annuities' own technical result including the TGF05 prudence
    margin [S3] [R17] and reduced by the *frais sur encours* [S1] [S2] [S5]; 1.50% is a
    round placeholder between the 0.00% *taux technique* and the 2.00% ceiling [R21], with
    the floor of zero as the only cited bound. A points régime has no contractual profit
    sharing at all and moves annuity levels through the *valeur de service du point*
    [S6].

### Options elected at conversion

All options are elected at conversion, are irrevocable, and are **not cumulative** at the
anchor carrier: "les options ne sont pas cumulatives et … le choix est irrévocable"
[S2 pt 10.e] [S3 pt 11.d].

| Option | Representative rule | Basis |
|---|---|---|
| *Réversion* (survivor continuation) | A named reversionary receives a taux de réversion δ of "la rente atteinte à la date du décès", for life, from the 1st day of the **month or quarter** following death [S6] — the 1st day following death at [S1 Art. C12] | [S2] [S3] [S1 Art. C12] [S6 Art. 5.4.3] |
| Available reversion rates | Any percentage from 1% to 100% | [S2] [S3]; representative snapshot **60%** **[std]** (14) |
| Cost of the reversion | A definitive coefficient on the annuitant's own annuity, keyed on the reversion rate and the age difference by birth-year *millésime* | [S6, published table]; adoption **[std]** (15) |
| Definitiveness | The reduction stands even if the reversionary predeceases the annuitant | [S6 Art. 5.4.3, verbatim] |
| Recalculation | Where the surviving spouse or PACS partner at death is not the one named at liquidation, the annuity is recalculated on the beneficiary's age at the date of death | [S2] [S3]; out of model scope **[std]** (16) |
| *Annuités garanties* (guaranteed period) | Instalments continue to the designated beneficiaries for the balance of the term if the annuitant dies inside it, at the same amount; if the annuitant survives the term the annuity continues for life with no further beneficiary | [S2] [S3] [S4] |
| Guaranteed-period range | Minimum 5 years; maximum the lesser of 25 years and the annuitant's life expectancy at the effective date minus 5 years; chosen in 5-year steps | [S2] [S3] [S4 §7.3.2.2] [S9] (17) |
| Guarantee vs reversion | Mutually exclusive | [S2] [S3]; representative rule **[std]** (18) |
| *Rente par paliers* (stepped annuity) | The annuity is a level-within-step function of duration, the first step running 5 or 10 years | [S2 pt 10.e] [S3 pt 11.d] |
| Published *paliers* schemes | Increasing: 100% → 200%, or 100% → 125% (equal second step) → 150%. Decreasing: 100% → 50%, or 100% → 75% (equal second step) → 50% | [S2] [S3] |
| *Rente dépendance* (dependency doubling) | Out of representative scope | [S5] [S6]; scope **[std]** (19) |
| Indexation | Not offered by any retrieved carrier | [S1]–[S9] |

14. Observed reversion menus: 1%–100% free-form [S2] [S3]; 50%–150% in 10-point steps, or
    50%–100% when combined with guaranteed annuities [S4 §7.3.2.2]; 100 / 80 / 60% [S5];
    60 / 80 / 100% [S6] [S9]; 50 / 60 / 100% with the reversionary aged 50–85
    [S1 Art. C16]; 5%–100% plus a *réversion majorée* to 200% [S8]. 60% appears in five of
    the eight and 100% in all eight; 60% is the snapshot because it is modal and because
    the only published cost table [S6] is keyed on it. *Réversion croisée* appears in no
    retrieved document — [unverified].
15. Préfon-Retraite publishes the only age-difference coefficient table found
    [S6 Art. 5.4.3], reproduced in `technical-notes.md`; CRH publishes flat coefficients of
    92.5 / 90 / 87.5% for 60 / 80 / 100% with no age-difference dimension [S9]; Carac says
    only that the reduction follows "un tarif spécial établi selon la réglementation en
    vigueur" [S1 Art. C16]. Adopting the Préfon table is **[std]**: it was built for a
    points régime and its coefficients apply to points, not to a euro annuity.
16. Modeling a change of spouse between liquidation and death needs marriage-state
    modeling a single-policy model point cannot carry. A named reversionary with
    attributes fixed at conversion is the only basis the reference model implements.
17. Three independent primary documents apply the "life expectancy minus 5 years" cap
    [S2] [S3] [S4] and one attributes it to art. A. 335-1 [S4]. The retrieved text of
    A. 335-1 in its 2012–2016 version [R2], of its successor A. 132-18 [R3] and of all
    fourteen amending points of the arrêté du 1er août 2006 [R1] were checked and **do not
    contain it**: observed market practice with an unlocated legal source, **[unverified]**
    as a statutory rule.
18. Suravenir's options are not cumulative [S2] [S3]. Spirica sells a combined *rente
    viagère réversible à annuités garanties* with two ranked beneficiaries and reversion
    capped at 100% in that combination [S4]. The exclusive rule is the anchor carrier's
    and keeps the death-benefit state machine to a single branch.
19. CNP doubles the annuity on recognised dependency, electable at liquidation before the
    70th birthday and only on a non-reversible annuity, with the definition, pricing and
    medical selection "en vigueur à la date de liquidation" — not fixed by the contract
    [S5]. Préfon publishes the whole rider: eligibility under 70; a benefit equal at all
    times to the annuity served; a monthly contribution deducted from the annuity of 3%
    (55–60), 4% (61–65) or 5% (66–70) with a 12% expense loading; a 4-ADL plus psychiatric
    grid scored 0–10 with 6–10 accepted; waiting of one year, three for mental causes,
    none after an accident; payment from six months after recognition, three if accidental
    [S6 Art. 5.4.4, Annexe 2]. AG2R doubles with no figures published [S8]. Dependency
    incidence and duration belong to the `dependance` product.

### Taxation of the arrérages — context, not a liability cash flow

Policyholder taxation does not enter the insurer's liability cash flows and is recorded
for completeness.

| Parameter | Representative value | Basis |
|---|---|---|
| Regime for an annuity bought with a capital | *Rente viagère à titre onéreux* (RVTO): only a fraction of each instalment is taxable, fixed once and for all by the annuitant's age at *entrée en jouissance* | [R13 CGI art. 158, 6](#frlib-rente_viagere-r13) [R15] |
| Taxable fractions | 70% under 50; 50% from 50 to 59; 40% from 60 to 69; 30% at 70 and over | [R13]; corroborated by [S7 fiscal annexe] and [S8] |
| Fixing the age | For an immediate annuity, the contract date or the date the funds are handed over; for a deferred annuity, the date payments actually begin. For a spousal reversion the **elder** spouse's age applies throughout, before and after the first death | [R14] |
| Regime for a retirement annuity funded by deducted contributions | *Rente viagère à titre gratuit*: taxed as a pension after the 10% abatement, capped at €3,850 per household and floored at €393. PER compartments C1 → RVTG, C1bis → RVTO, C3 → RVTG and annuity-only | [R13 art. 158, 5-a](#frlib-rente_viagere-r13) [R15] [S2 tax table] [S6 annexe fiscale] |
| Social levies | RVTO: 17.20% (CSG 9.2% + CRDS 0.5% + solidarity levy) on the taxable fraction only. RVTG: CSG 8.3% / 6.6% / 3.8% or exempt, CRDS 0.5%, CASA 0.3% | [S6 annexe fiscale III] [S2] [S7] |
| Conversion of an *assurance vie* into an annuity | Whether accumulated gains are taxed at conversion is **[unverified]** — no retrieved document covers it | — |

---

## Contractual mechanics

### Conversion of the capital

The *capital constitutif* C is converted once, at the effective date, into a gross annual
annuity. The retrieved documents agree on the inputs and never on the output. Suravenir
lists them at point 10.d: the adherent's age; the reversion beneficiary's age where
applicable; the options and parameters chosen; "la table de mortalité des rentiers en
vigueur à la date d'effet de la rente"; and "un taux d'intérêt technique de 0,00 %" [S2].
Spirica adds the *Valeur Atteinte* net of levies, the dates of birth of both heads, the
periodicity, the number of guaranteed annuities and "le taux d'intérêt technique en
vigueur" [S4 §7.3.2.3]; La France Mutualiste's *barème* "tient compte … des tables
prospectives de génération et du taux d'intérêt technique en vigueur" and may change
in-year if either moves [S7 Art. 5.3]; CNP converts on "les bases techniques en vigueur
au moment de la demande de liquidation" [S5].

Two things follow. **The dates of birth, not the ages, are the pricing keys**: the table
is generational, so the annuitant's *millésime* selects the column and the age selects
the row. And **the annuity is not guaranteed before liquidation** [S4 §7.3.2.3] — the
conversion rate is a pricing snapshot, not a contractual promise, so every *taux de
rente* in this library is **[std]**. Where an option is elected the gross annuity is
reduced by a definitive coefficient; for *réversion* Préfon's published table
[S6 Art. 5.4.3] runs from 0.93 (reversionary eight or more years older, 60% reversion)
down to 0.24 (45 or more years younger, 100%) and is reproduced in `technical-notes.md`.

### Payment of the arrérages, and what death does to the last one

The annuity takes effect on the 1st day of a civil month [S2] [S3] [S6] and is paid
*terme échu*. Instalments "cessent d'être dus à compter du premier jour du mois qui suit
le décès" [S6] — so **the arrérage of the month of death is due in full**, and on a
monthly frequency the estate receives one whole instalment for the month in which the
annuitant died. On a coarser frequency the same rule produces a stub: arrears accrued and
unpaid at death belong to the heirs, an overpayment is owed by the estate, and Carac
applies a €15 de-minimis in both directions [S1 Art. C17.2] [S7 Art. 7.3]. This is the
opposite default from the UK sibling, where an arrears policy "without proportion" pays
nothing for the final partial period; in France there is no "proportion" option to elect,
because the *prorata d'arrérages* is the rule.

Payment is conditional on proof of life: an annual *attestation valant certificat de vie*
plus a birth extract under three months old, returned within 30 days, failing which the
annuity is suspended from the following month until it arrives [S2] [S3] [S1 Art. C13].

### Revalorisation out of the participation aux bénéfices

The statutory obligation is to share technical and financial profits with policyholders
[REG-R14]; the mechanics live at arts. A. 132-10 to A. 132-17 [R7] [REG-R15]. The minimum
*participation aux bénéfices* for a financial year is determined **globally, not contract
by contract**, from a *compte de participation aux résultats* credited with the
underwriting elements, 85% of the balance of a financial account and the reinsurance
balance, the insurer retaining the greater of 10% of the credit balance and 4.5% of
annual premiums [R7] [REG-R15] — that last clause was returned as a paraphrase and is
**[unverified]**. Sums placed in the *provision pour participation aux bénéfices* must
reach the *provision mathématique* or the policyholders "au cours des huit exercices
suivant celui au titre duquel elles ont été portées" [R7 art. A. 132-16, verbatim](#frlib-rente_viagere-r7)
[REG-R16].

How that reaches the *arrérages* is stated operatively only once, and it is the sentence
this composite is built on [S3, verbatim]:

> Chaque année, Suravenir établit le compte de participation aux bénéfices des **rentes
> en cours de service** conformément au point III de l'article A. 132-11 du Code des
> assurances **en incluant le résultat technique généré par ces mêmes rentes**. La
> participation aux bénéfices attribuée chaque année aux rentes de l'actif isolé du
> contrat est égale à **100 % du solde créditeur** du compte de participation aux
> bénéfices.

Two consequences. The annuities' own mortality surplus — including the TGF05 prudence
margin carried by every male life under the unisex rule — flows back into the annuities
rather than into shareholders' funds, which is the mechanism the ministry describes
[R17]. And the *frais sur encours de rentes* reduce that account, so they reduce the
revalorisation and never the guaranteed annuity [S1] [S2] [S5] [S6] [S7].

The increase is credited at 31 December [S2 pt 10.f], pro rata temporis from the
effective date for annuities in service less than a year at 1 January [S3], and is
non-negative in every retrieved formulation. **A discretionary increase is not an
escalation guarantee.** What may be guaranteed in advance is capped separately, at the
lower of 150% of the maximum technical rate and the higher of 120% of that maximum and
110% of the average rates credited over the two preceding years, for at least six months
and at most to the end of the following financial year [R6] [REG-R18] — **[unverified]**
as to the exact percentages. Art. A. 132-3 came back as a structured summary rather than
verbatim text, and the research flags these percentages in the same breath as the
A. 132-11 retained share, to be re-read before any of them is relied on. Nothing in this
model depends on them: ν is a **[std]** scenario input and no rate is guaranteed in
advance here.

### Réversion, annuités garanties, rente par paliers

If *réversion* is elected, on the annuitant's death a named reversionary receives δ × "la
rente atteinte à la date du décès" for life [S2] [S3], starting from the 1st day of the
"month or quarter" following death [S6] — the only retrieved dating of the reversion
start, and a disjunction rather than a single rule; Carac dates it the 1st day following
death [S1 Art. C12]. On a monthly *terme échu* basis the two limbs coincide, and the first
reversion instalment is paid at the end of the month *after* the month of death,
immediately after the *prorata d'arrérages* has settled the month of death. The two never
overlap and never leave a gap. At a coarser frequency they part, and the composite reads
the monthly limb — a **[std]** choice, recorded in the technical notes, that no retrieved
document settles. The election reduces the annuitant's own annuity by a definitive
coefficient: "Le choix de la réversion implique une réduction définitive, même si le
bénéficiaire de la réversion vient à décéder antérieurement à l'Affilié(e)"
[S6 Art. 5.4.3, verbatim]. If the reversionary dies first the annuitant's reduced annuity
simply continues and no reversion is ever paid. Beneficiary rules vary — spouse, PACS
partner or cohabitant [S1]; spouse or PACS partner by default, another named person
otherwise but served only from age 25 [S6] — and Carac may refuse the option if it would
drop either annuity below €77 a year [S1 Art. C16].

If *annuités garanties* are elected, the annuity is paid to the annuitant and, on death
within the term, to the definitively designated beneficiaries for the balance of the term
at the same amount [S2] [S3] [S4]; if the annuitant survives the term, "le versement de
la rente se poursuit jusqu'à son décès, sans autre bénéficiaire d'annuités garanties, ni
de réversion possible" [S2] [S3]. It is an annuity-certain **floor** on one stream, not a
second stream — the same shape as the UK sibling's guarantee period. **Commutation of the
remaining guaranteed instalments to a lump sum is not offered by any retrieved French
contract** [S2] [S3] [S4]; that this holds market-wide is [unverified].

A *rente par paliers* is a level-within-step function of duration: Suravenir's four fixed
schemes with a first step of 5 or 10 years [S2 pt 10.e] [S3 pt 11.d], or Spirica's
free-form version where "Chacune des deux premières périodes de versement est limitée à
10 ans" and "Le nombre de majorations ou de diminutions est au maximum de 2"
[S4 §7.3.2.2]. It is **not** escalation: nothing compounds and the schedule is fixed at
conversion.

### No surrender, and the small-annuity commutation

"Les assurances temporaires en cas de décès ainsi que les rentes viagères immédiates ou
en cours de service ne peuvent comporter ni réduction ni rachat" [R8, verbatim](#frlib-rente_viagere-r8); Carac
restates it in the contract [S1 Art. C3]. Once the annuity is liquidated the capital is
gone: no surrender value at any duration, no *valeur de réduction*, no transfer. The
statutory early-release cases at art. L. 132-23 belong to the accumulation phase of a
retirement contract and do not survive liquidation [R8], as does the 5% penalty a
*capitaux réservés* deferred contract charges before its tenth anniversary [S7 Art. 15].

Art. L. 160-5 lets an insurer, "nonobstant toutes dispositions contractuelles
contraires", transform or buy back annuities whose *quittances d'arrérages* fall below a
minimum fixed by arrêté [R9, verbatim](#frlib-rente_viagere-r9). The current figure is **€110 a month**, "en y
incluant le montant des majorations légales", under art. A. 160-2 in force since 22 July
2023; for longer periodicities the threshold is "multiplié par le nombre de mois inclus
dans la période de paiement" — €330 a quarter, €660 a half-year, €1,320 a year [R10].
Art. A. 160-2-1, the PER-specific twin at €100 a month in force from 1 July 2021 to
22 July 2023, is abrogated and the two regimes merged [R10]. The buy-back *barème* values
the annuity on the *provision mathématique* computed with the tables and rates of the
règlement ANC n° 2015-11 du 26 novembre 2015 [R10 art. A. 160-3](#frlib-rente_viagere-r10), and several contracts
with the same insurer may be grouped to reach the threshold, the beneficiary then
choosing between *rachat* and *transformation* [R10 art. A. 160-4](#frlib-rente_viagere-r10).

Contracts implement it as an election at liquidation, not as an in-force option:
"Lorsque le montant de la rente est inférieur au minimum défini à l'article A. 160-2 … la
liquidation des droits pourra, **avec l'accord de l'assuré**, s'effectuer sous la forme
d'un versement unique en capital" [S2]; the same at [S3]; CNP applies it to the reversion
annuity too, with the *réversataire*'s agreement [S5]. Régime-specific floors sit above
the statutory one and are not it: Préfon issues only annuities of at least €40 a month,
measured **before** the reversion and dependency options [S6]; AG2R's minimum is €40 a
month [S8]; CRH pays a lump sum below 500 points of reversion entitlement [S9]; Carac's
option-level floor is €77 a year [S1 Art. C16]. The consequence for a reference model is
that a model point whose gross monthly quittance is at or below €110 is not an annuity to
project — it is a capital payment at outset.

---

## Riders and options

A *rente viagère* has no riders in the US sense. Everything is elected at conversion,
priced into the *barème*, and irrevocable thereafter [S1] [S2] [S3] [S4] [S5] [S6] [S8].

**In scope (the representative option set):** payment frequency [S2] [S3] [S4] [S6] [S8];
*réversion* at δ ≤ 100% with a definitive coefficient on the annuitant's own annuity
[S2] [S3] [S6]; *annuités garanties* of 5 to min(25, e − 5) years in 5-year steps
[S2] [S3] [S4] [S9], mutually exclusive with *réversion* [S2] [S3]; the four Suravenir
*paliers* schemes with a first step of 5 or 10 years [S2] [S3].

**Out of scope (listed for completeness):**

- *Rente dépendance* — the doubling of the annuity on recognised dependency, offered by
  CNP [S5], Préfon [S6] and AG2R [S8]; belongs to the `dependance` product.
- *Capital réservé* — a death capital of at least 70% of the sums paid in that mode, net
  of entry charges and plus accrued *bonification*, in exchange for a lower annuity
  [S1 encadré, Art. C3, C17.1] [S7 encadré §2] — a genuine second product shape, the
  French analogue of a return-of-premium annuity, not a rider. With it go the *aliénation*
  of reserved capital into a deferred survivor annuity for a spouse aged at least 50
  [S7 Art. 10] and Carac's conversion of a reserved holding to *capital aliéné*
  [S1 Art. C15].
- Recalculation of the reversion annuity where the surviving spouse at death is not the
  one named at liquidation [S2] [S3]; *réversion majorée* to 200% [S8]; *réversion
  croisée* (named in no retrieved document — [unverified]); and Spirica's combined *rente
  viagère réversible à annuités garanties* with two ranked beneficiaries [S4].
- Points régimes, whose annuity levels move through the *valeur de service du point*
  rather than through a *participation aux bénéfices* [S6] [S9].
- Legacy annuities carrying State *majorations légales*, uprated by arrêté and which must
  be included when testing the small-annuity threshold [R22] [R10 art. A. 160-2](#frlib-rente_viagere-r10).

---

## Variations across insurers

| Feature | Carac RVI [S1] | Suravenir PER/PERP [S2] [S3] | Spirica PER [S4] | CNP PER [S5] | Préfon-Retraite [S6] | AG2R Rente Universelle [S8] |
|---|---|---|---|---|---|---|
| Product shape | standalone immediate annuity (mutuelle) | PER / PERP exit | PER exit | PER exit | points régime, PER-eligible | standalone immediate annuity |
| Minimum capital / annuity | board-set; option floor €77/yr | statutory A. 160-2 floor | statutory floor (€100 text, pre-2023) | "montant fixé par la réglementation" | €40/month issue floor | €30,000 capital; €40/month |
| Entry ages | **50–85** | not stated | not stated | not stated | régime rules; dependency < 70 | not stated |
| Payment frequency | **semi-annual only** (30 Jun / 31 Dec) | **monthly** | monthly / quarterly / half-yearly / annual | **quarterly** | **monthly** (since 31/07/2023) | monthly / quarterly / half-yearly / annual |
| Timing | *terme échu* | *terme échu* | *terme échu* | *terme échu* | *terme échu* | not stated |
| *Taux technique* | referenced, not published | **0.00%** | in force at conversion, capped by regulation | *bases techniques* of the day | points régime | not published |
| *Frais d'arrérages* | **néant** | **0.00%** | **0%**, capped at 1% PMSS | **3% max per instalment** | **none** | named, no figure |
| *Frais sur encours* | **0.55%** on PM | **0.80%** (PER) / **0.68%** (PERP) | **2.3% max** on the annuity support | **1% max/yr** on *capitaux constitutifs* | 0.70% max on provisions + 2% of PTS income | not published |
| *Réversion* | 50 / 60 / 100%; reversionary 50–85; floor €77/yr | **1–100%**, recalculated on change of spouse | **50–150%** in 10-point steps (50–100% with guarantees) | 100 / 80 / 60% | 60 / 80 / 100% with published coefficients | **5–100%**, *majorée* to **200%** |
| *Annuités garanties* | **none** | 5 yrs → min(25, e − 5), 5-yr steps, XOR reversion | ≤ e − 5; combinable with reversion | not offered | not offered | offered, durations not published |
| *Rente par paliers* | none | **four fixed schemes** | free-form, ≤ 2 steps, each ≤ 10 yrs | none | none | none |
| *Rente dépendance* | none | none | none | **doubling**, before 70, non-reversible only | **doubling**, 3/4/5% of the annuity by age band | doubling, no figures |
| Death benefit otherwise | **capital réservé ≥ 70%** of net payments | none | none | none | reversion / orphan machinery | *capital décès* |
| Revalorisation | annual *bonification* set by the board | PB at 31 Dec; PERP: **100% of the PB account credit balance** including the annuities' technical result | *compte de participation aux résultats* | art. 12.2 of the notice | **no contractual PB**; *valeur de service du point* | annual, on the euro fund's return |

Why the representative choices were made:

1. **Chassis.** Suravenir [S2] [S3] publishes the option set, the payment convention, the
   technical rate, the charge structure and the profit-sharing rule in operative terms;
   the others state some of those and never all. Research conclusion; adoption **[std]**.
2. ***Terme échu* and monthly.** Not a choice: every retrieved carrier pays in arrears,
   and monthly is the finest published frequency, so every other frequency is a
   restriction of the same engine [S1]–[S9].
3. **Reversion XOR guarantee.** The anchor carrier's rule [S2] [S3]. Spirica's combinable
   design [S4] is implementable in the same engine by letting the certain-period floor
   and the reversion stream coexist, with the reversion percentage capped at 100% in that
   combination; it is documented, not defaulted.
4. **Charges.** A non-zero *frais d'arrérages* (CNP's 3% [S5]) is taken with Suravenir's
   *frais sur encours* (0.80% [S2]) so that both mechanics are exercised, even though no
   single retrieved carrier charges both at those levels. An explicit composite; **[std]**.
5. **Excluded chassis.** *Capital réservé* [S1] [S7] changes the death-benefit shape
   entirely — a lower annuity, a death capital of at least 70% of the net sums paid in
   that mode, and the right to alienate that capital later into a survivor annuity
   [S7 Art. 10]. Points régimes [S6] [S9] move annuity levels through a *valeur de service
   du point* no retrieved document publishes, and Préfon has no contractual profit sharing
   at all [S6]; their published option-cost tables are used, their annuity mechanics are
   not. Both are second chassis, not parameters.
6. **Vintage and coverage caveats.** CNP's notice carries no reference code or edition
   date and was read from a third-party mirror posted in February 2021, so its 3% and 1%
   charge levels and its 60/80/100% reversion menu are treated as 2020/2021 vintage [S5].
   Allianz's annuity guide could not be read — HTTP 403 on two successive attempts — and
   nothing from it is cited [S10]. Generali, MACSF, Groupama, Swiss Life France, Malakoff
   Humanis, Le Conservateur and Garance were not sourced at all; no claim of market-wide
   coverage is made.

---

## Regulatory context

**Mortality tables.** The arrêté du 1er août 2006 homologates TGF05 for female lives and
TGH05 for male lives for *contrats de rente viagère* from 1 January 2007, replacing the
generation table homologated in 1993 [R1 art. 2, verbatim](#frlib-rente_viagere-r1) [REG-R21]. TH00-02 / TF00-02,
homologated by the arrêté du 20 décembre 2005 on INSEE data, apply to "contrats autres
que de rente viagère" and are **not** used to price an annuity [R11].
**Citation hygiene matters here.** The arrêté speaks of art. A. 335-1, the then-current
numbering; Légifrance now marks A. 335-1 abrogated and serves it only in its 21 December
2012 – 1 January 2016 version [R2] [REG-R23], the live tariff article being **A. 132-18**,
in force since 7 September 2017 [R3]. The abrogating instrument and the gap between the
two dates were not resolved and are [unverified] [R2]. Cite A. 132-18 for the live rule
and A. 335-1 only when quoting the arrêté. The annexe article carrying TGF05 is itself
marked abrogated as of 1 January 2016, the tables presumably re-annexed elsewhere; the
current location was not identified [R12] [unverified]. **This library does not
redistribute TGH05/TGF05 values**: they are cited by name and article, and the decrement
CSVs shipped here are **[std]** proxies built from public INSEE data [REG-R24], anchored
so the model's **tariff** annuity factor — the female-table factor the unisex rule
selects — reproduces the technical notes' placeholder rate exactly. The anchor is on the
tariff side, not the best-estimate side: the two tables are different objects here, and a
male life's best-estimate factor of 26.21 gives 3.73%, not the 3.30% quoted.

How they were built is set out in the technical notes; two properties of that
construction matter here. **The tables are prospective, so the mortality trend is inside
them and no separate improvement scale applies**, and the construction lets male
projected rates fall below female rates in some cells [R19].

**Unisex pricing.** Art. A. 132-18 permits either homologated tables by sex or the
undertaking's own certified experience tables, then imposes three constraints: a single
homologated table applied to all insureds must be the one "conduisant au tarif le plus
prudent"; the *décalages d'âge* correction applies to non-annuity survival contracts;
and for *rentes viagères* an experience-table tariff may never be lower than the
homologated-table tariff [R3, verbatim](#frlib-rente_viagere-r3). The chain of authority as the ministry states it
runs directive 2004/113/CE → the CJEU ruling of 1 March 2011 in case C-236/09
(*Test-Achats*) → the loi du 26 juillet 2013 amending art. L. 111-7 [R17] [R18]. The
judgment was not retrieved [R16] and the secondary sources date the boundary
inconsistently — "après le 20 décembre 2012" [R18] [R25] against "une directive du
21 décembre 2012" [R17] — so the cut-off convention is [unverified]. The ministry
acknowledges that applying TGF05 to men produces a systematic technical surplus which
must in substantial part be returned to policyholders within eight years, and declines to
legislate further [R17]. Contracts under the Code de la mutualité [S1] [S7] sit under a
parallel arrêté (du 8 décembre 2006) located but not fetched — [unverified] whether its
table rules are identical.

**Technical rate.** Tariffs must use a rate at most 75% of the TME on a half-yearly basis
and, beyond eight years, at most the lower of 3.50% and 60% of that average, the rate in
force at subscription binding [R4] [REG-R17]; the maximum sits on a 0.25-point ladder of
origin zero and moves only when the monthly reference rate falls by at least 0.10 point
or rises by at least 0.35 point, with three months to implement [R5] [REG-R17]. **A
lifetime immediate annuity is unambiguously a "beyond eight years" contract**, so the
binding ceiling is min(3.50%, 60% × TME) — [unverified] as an inference, since the
retrieved text of A. 132-1 contains no annuity-specific paragraph [R4]. The ceiling stood
at 2.00% with a monthly reference TME of 3.90% at 31 July 2026 [R21, secondary](#frlib-rente_viagere-r21).

**Participation aux bénéfices, surrender and commutation.** The profit-sharing obligation
is statutory [REG-R14]; the arithmetic is at arts. A. 132-10 to A. 132-15 and is computed
globally rather than contract by contract [R7] [REG-R15]; the eight-year release horizon
on the *provision pour participation aux bénéfices* is at art. A. 132-16 [R7, verbatim](#frlib-rente_viagere-r7)
[REG-R16]; and point III of art. A. 132-11 is the paragraph a PERP or PER insurer uses to
build a separate profit-sharing account for the annuities in payment [S3] [R7].
Art. L. 132-23 forbids reduction and surrender of immediate and in-payment life annuities
[R8, verbatim](#frlib-rente_viagere-r8); art. L. 160-5 delegates the buy-back schedule and threshold to an arrêté
[R9, verbatim](#frlib-rente_viagere-r9); art. A. 160-2 sets that threshold at €110 a month including *majorations
légales*, scaled by the payment periodicity [R10]. *Majorations légales* are the
State-funded uplifts of legacy annuities under the loi n° 49-420 du 25 mars 1949 and
successors, uprated by arrêté with coefficients keyed on the year the annuity originated
[R22] — not the ordinary commercial revalorisation of a modern annuity.

**Prudential, disclosure, professional standards.** The French statutory balance sheet
carries eleven technical provisions, of which the *provision mathématique* — the
difference between the actuarial present values of the two sides' commitments, including
future management costs — holds an annuity in payment [REG-R6]. Solvabilité II sits on
top: the best estimate is the probability-weighted average of future cash flows
discounted at the relevant risk-free term structure — carried here on EIOPA's authority
[REG-R4], because neither the directive [REG-R1] nor the delegated regulation [REG-R2]
could be retrieved (both return a WAF challenge), so their article numbers are
[unverified] in this library — with EIOPA publishing the curves monthly [REG-R5]; nothing
product-specific to *rentes viagères* was retrieved for that layer. The *note d'information* and the one-page *encadré* prescribe
what must be disclosed, including fees in four categories with maximum amounts or
percentages [REG-R30] — maxima, not caps: no statutory ceiling on any French life charge
appears in the retrieved texts, which is why every charge level here carries a source or
a **[std]** tag and never a "market standard" claim. The 30-day *renonciation* right
applies before the annuity starts [S1 Art. C7] [REG-R29] and is outside the projection.
Actuarial work using this model sits under the Institut des actuaires' NPA 1 and NPA 2,
both category-3 recommended practices adopted 15 June 2015 [REG-R43] [REG-R44]; NPA 4, on
best-estimate life provisions, was not retrieved and is [unverified].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-rente_viagere-r1
[R10]: #frlib-rente_viagere-r10
[R11]: #frlib-rente_viagere-r11
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
[R22]: #frlib-rente_viagere-r22
[R23]: #frlib-rente_viagere-r23
[R24]: #frlib-rente_viagere-r24
[R25]: #frlib-rente_viagere-r25
[R3]: #frlib-rente_viagere-r3
[R4]: #frlib-rente_viagere-r4
[R5]: #frlib-rente_viagere-r5
[R6]: #frlib-rente_viagere-r6
[R7]: #frlib-rente_viagere-r7
[R8]: #frlib-rente_viagere-r8
[R9]: #frlib-rente_viagere-r9
[REG-R1]: #frlib-reg-r1
[REG-R14]: #frlib-reg-r14
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R17]: #frlib-reg-r17
[REG-R18]: #frlib-reg-r18
[REG-R2]: #frlib-reg-r2
[REG-R21]: #frlib-reg-r21
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R34]: #frlib-reg-r34
[REG-R4]: #frlib-reg-r4
[REG-R43]: #frlib-reg-r43
[REG-R44]: #frlib-reg-r44
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
