# Product Specification

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of a French **assurance temporaire décès** — the standalone term
life contract that pays a *capital décès* (death lump sum) if the insured dies inside the cover
period and pays nothing otherwise. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents: *notices d'information*, *conditions
générales*, *notes d'information*, IPID and insurer product pages) and [R#]
(regulatory/actuarial references), both numbered per `_research/temporaire-deces.md` and
resolved in `sources.md` (same directory; numbering frozen, never renumbered), and [REG-R#] (the
cross-product reference library `references/regulatory-and-actuarial-references.md`, whose own
R-numbering is distinct) — were extracted from the cited document. Values marked **[std]** are
standardizations introduced for the reference implementation; each **[std]** table row carries a
numbered footnote giving the rationale and, where the research file recorded one, the observed
range across insurers. Facts the research file could not verify are flagged [unverified]. The
composite is drawn from **eight retrieved carriers**: seven contractual documents — two mutual
group contracts [S1] [S2], one individual contract with a **published attained-age rate card**
[S3] [S4] [S5], one mutual group contract with published underwriting thresholds [S6], one
stock-company group contract [S7], one *bancassurance* IPID [S8] and one *Code de la mutualité*
contract [S9] — plus an eighth carrier evidenced only by its **product page** [S10], which is the
eighth column of the research file's variations table. Where this document counts to "eight", it
counts those eight carriers, one of which is a web page rather than a contract. Two further
insurer pages [S11] [S12] and three secondary guides [S13] [S15] [S16] are used for context only.
*Assurance emprunteur* (ADE, borrower's cover attached to a loan) is a separate frlib product
(`products/assurance_emprunteur/`) and is referenced only where French law or French actuarial
practice treats the two differently.

---

## Product overview and market role

A French assurance temporaire décès is **life assurance business** — *branche 20
(vie-décès)* of art. R. 321-1 of the Code des assurances — not accident business, even
though it pays only on death [S1] [S3] [S7]. It is pure protection: a *cotisation*
(premium) buys a *capital décès* for the cover period, with **no savings element, no
account value, no *valeur de rachat* (surrender value) and no *valeur de réduction*
(paid-up value)**. If the insured survives, "les cotisations versées restent acquises à
l'assureur" — the contract is *fonds perdu* [S5] [S11] [S15] [S16]. That is not a
commercial choice: art. L. 132-23 alinéa 1 provides that "les assurances temporaires en cas
de décès … ne peuvent comporter ni réduction ni rachat", and the prohibition binds the
insurer's ability to offer the feature, not merely the policyholder's ability to demand it
[R3].

Three features make the French chassis different from its UK and US siblings, and each of them
changes the shape of the projected cash flows:

1. **The cotisation is revised each year with attained age.** Seven of the eight retrieved
   carriers price on an annually revisable attained-age basis
   [S1] [S2] [S3] [S6] [S7] [S9] [S10]; the eighth, a *bancassurance* IPID, states no premium
   basis at all [S8], so nothing in the corpus contradicts it. The dominant legal form is a **one-year contract renewed
   by *tacite reconduction*** (automatic renewal) [S1] [S2] [S3] [S6] [S8] [S9] [S13] [S15], and
   the tariff is recomputed at every renewal from the insured's attained age. A reader who
   assumes a level premium by default will build the wrong model.
2. **PTIA is an acceleration, not an extra benefit.** *Perte totale et irréversible d'autonomie*
   — total and irreversible loss of autonomy — triggers **anticipated payment of the same death
   capital to the insured**, and payment extinguishes the death cover [S1] [S2] [S3] [S6]. It is
   present in every retrieved standalone contract but the *mutualité* one [S9].
3. **There is no cash value at any duration.** No surrender, no reduction, no non-forfeiture
   mechanism, no *tableau de rachat* [R3] [S5] [S7] [S9].

Contract wrappers vary without changing the economics. The **individual** form is "un contrat
individuel d'assurance décès, d'une durée d'un an, renouvelable par tacite reconduction" [S3].
The **group contract with voluntary membership** (*contrat d'assurance de groupe à adhésion
facultative*, arts. L. 141-1 ff.) is at least as common — an association subscribes and the
member receives a *notice d'information* which is the contractual reference [S1] [S2] [S6] [S7].
A parallel form under Livre II of the **Code de la mutualité** behaves identically with shorter
procedural timers [S9], and a *bancassurance* form ties the cover to a bank relationship and
terminates it when the account closes [S8].

French *assurance prévoyance* premiums were **40,3 Md€ in 2025** [R21]; the split between
*garanties décès*, *incapacité-invalidité* and *dépendance* is not published, so there is **no
sourced figure for the size of the standalone temporaire décès segment** [R21]. For scale,
assurance vie premiums ran at €19,3 bn in the single month of June 2026 [REG-R49]. The comparison
French insurers use to size the need is the state benefit: the Sécurité sociale pays a flat
*capital décès* of **3 450 €** (amount at 1 April 2018) regardless of the deceased employee's
earnings [S2].

---

## Representative specification

The representative design is the individual contract of [S3] [S4] — the only retrieved
French standalone contract that publishes a complete attained-age rate card, and therefore
the only one whose premiums a model can reproduce rather than assume.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Annually renewable temporaire décès; *branche 20 (vie-décès)*; non-participating in substance; no cash values | [S3] [S1] [S7] [S9] |
| Legal wrapper | Individual contract, renewed by *tacite reconduction*; group *adhésion facultative* is the equally common alternative | [S3]; [S1] [S2] [S6] [S7]; choice **[std]** (1) |
| Premium form (model-point parameter) | (i) `revisable` — cotisation recomputed each year at attained age; (ii) `constante` — level for the whole cover period | (i) [S1] [S2] [S3] [S6] [S7] [S9] [S10]; (ii) **[std]** (2) |
| Benefit shape (model-point parameter) | (i) `constant` — *capital constant*; (ii) `decreasing` — *capital décroissant*, out of scope here | (i) [S1] [S2] [S3] [S6] [S7] [S8] [S9]; (ii) [S15]; scope **[std]** (3) |
| Lives basis | Single life. No joint-life basis appears in any retrieved French standalone contract | [S1] [S2] [S3] [S6] [S7] [S8] [S9] |
| Entry ages | 18 to 65 (to the day before the 66th birthday) | [S3]; envelope **[std]** (4) |
| Death cover ceases | At the *échéance* following the 75th birthday | [S3]; envelope **[std]** (4) |
| PTIA cover ceases | At the *échéance* following the 65th birthday — earlier than the death cover, which is the pattern at **five of the eight carriers** but not an invariant: one ends both at 85 [S1] and one has no PTIA cover at all [S9] | [S3]; pattern [S2] [S6] [S7] [S8]; exceptions [S1] [S9] |
| Age basis | *Différence de millésime*: calendar year of the contract year minus calendar year of birth, irrespective of birth month | [S1] [S2] [S6] [S7] |
| Sum assured | Minimum 20 000 €; no stated ceiling; 250 000 € under simplified underwriting to age 40 | [S3] [S4] [S5]; envelope **[std]** (5) |
| Residence | France or the DROM; not under *tutelle* nor hospitalised in a psychiatric establishment; one individual death contract per person at the insurer | [S3] |
| Territorial scope of cover | Worldwide, subject to notification of stays abroad longer than 6 months | [S3] |
| Anchor model cell | Issue age 58, sum assured 150 000 €, `revisable`, `constant` shape, cover to 75, PTIA to 65, standard rates, annual premium mode | **[std]** (6) |

Footnotes to **[std]** rows:

1. Wrapper is a legal, not an economic, variable: the individual form [S3] and the group
   *adhésion facultative* form [S1] [S2] [S6] [S7] produce identical cash flows. The composite
   adopts the individual form because the representative rate card [S3] belongs to it, and
   because the group form adds an association subscription (1,30 € per member per year at one
   carrier [S1]) and an amendment procedure [S1] [S2] that are wrapper, not liability,
   mechanics.
2. **No level-premium French standalone contract was found.** Every retrieved carrier whose
   premium basis is stated prices on the attained-age revisable basis — seven of the eight
   [S1] [S2] [S3] [S6] [S7] [S9] [S10], the eighth silent [S8]; the two
   secondary guides that mention 5-year renewal periods and 10/15/20-year terms [S13] [S16]
   say nothing about the premium being level, and those multi-year terms are themselves
   [unverified] against any insurer document. The level form is confirmed only for *assurance
   emprunteur*, where the rate is guaranteed for the loan term [R13]. The `constante` form is
   therefore a **[std]** construction, retained because it generates a real *provision
   mathématique* [R11] [R13] and because a UK/US reader will otherwise assume it silently.
3. Every standalone contract retrieved is *capital constant* [S1] [S2] [S3] [S6] [S7] [S8]
   [S9]; none offers a decreasing sum insured. *Capital décroissant* is described as belonging
   to loan cover [S15], where the industry distinguishes a tariff on *capital initial* from one
   on *capital restant dû* [R13]. The composite carries `benefit_shape` as a column driven by
   an external schedule table, with `constant` (factor 1.0 at every duration) as the only
   shipped schedule; the decreasing form belongs to `products/assurance_emprunteur/`.
4. Observed entry ages: 18–75 [S1]; 18–67 [S2]; ≤ 65 [S3]; 18–80 [S6]; 18 to under 66 [S8];
   18–84 [S10]; to the day before the 57th birthday [S12]. Observed death-cover cessation: the
   year of the 85th birthday [S1] [S6] [S7]; 1 April after the 80th [S2]; the *échéance* after
   the 75th [S3]; the anniversary after the 70th [S8]; 31 December of the year of the 65th
   [S9]; 90 [S10]. The composite takes the representative carrier's own envelope [S3] rather
   than a mode, because entry age, cessation age and the rate card must be mutually consistent
   and only [S3] publishes all three.
5. Observed capital ranges: 10 000 – 2 000 000 € [S1]; 25 000 – 762 000 € [S2]; 20 000 € to no
   stated ceiling [S3] [S4]; ≤ 200 000 € [S6]; 100 000 – 1 000 000 € [S8]; 6 097,96 – 45 000 €
   [S9]; ≤ 50 M€ death and ≤ 20 M€ PTIA [S10].
6. Issue age 58 is chosen so that the entire projection (17 policy years, attained ages 58–74)
   fits one worked-example table, and so that it straddles both of the product's distinctive
   discontinuities: the rate card's **+38 % step from age 59 to age 60** and the **cessation of
   PTIA cover at 65** [S3]. Sum assured 150 000 € is the capital used in the representative
   carrier's own published worked example [S3].

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | **Cotisation annuelle révisable par âge**: recomputed at the effective date and again at every annual renewal from the insured's attained age | [S1] [S2] [S3] [S4] [S6] [S7] [S9] [S10] |
| Rate expression | Cotisation = sum assured × the tariff percentage for the attained age: "multiplier le montant du capital que vous choisissez par le tarif en pourcentage … correspondant à votre âge au moment de la souscription, puis au moment de la reconduction annuelle" | [S3] |
| Published rate card | 0,15 % of capital flat for ages 18–34, rising to 4,86 % at age 74 (full grid reproduced in the technical notes) | [S3]; vintage caveat **[std]** (7) |
| Rate at the anchor age | 1,05 % at attained age 58 → 1 575,00 € per year on 150 000 € | [S3] |
| Frequency | Annual in advance is the base case; half-yearly, quarterly and monthly available, normally by SEPA direct debit | [S1] [S2] [S6] [S7] [S8] [S9] |
| Rating factors | Attained age; sum assured; medical acceptance (*surprime*); smoker status; occupation tariff group; declared sporting activities. **Sex may not be a rating factor** for contracts written from 21 December 2012 | [S1] [S2] [S3] [S6] [S7] [S10]; unisex [R10] |
| Rating multiplier (model-point parameter) | `rating_factor`, applied to the tariff rate; 1.00 at standard rates | mechanics [S1] [S2] [S3] [S6]; value **[std]** (8) |
| Other repricing triggers | Legislative or regulatory change [S1] [S6] [S7]; and, at two carriers only, "l'accroissement de la fréquence et/ou du coût moyen des sinistres" [S1] and "les résultats des garanties Assurance Décès" [S6] — i.e. experience repricing of the whole class | [S1] [S6] [S7], as tagged in the cell |
| Policyholder remedy on an insurer-decided increase | Terminate within 30 days of learning of it (15 days at one carrier), cover maintained on the old terms until termination takes effect one month later. An increase arising from **age**, from the index or from a change of law "n'ouvre droit ni à contestation ni à résiliation" | [S1] [S7] |
| Premium cessation | Premiums stop on death and on recognition of PTIA; they are collected at the latest to the échéance following the death-cover age limit | [S3] [S7] |
| Age-error rule | Art. L. 132-26: true age outside the contract's limits → cover void, premiums returned; inside → benefits reduced in proportion to the premium underpaid, or the overpayment refunded | [S7] |

7. The published grid was retrieved from a third-party mirror of a **2019–2021 vintage** *note
   d'information*; its own internal worked examples are dated 2019 [S3]. The same carrier's
   current page quotes **6,29 €/month at age 35 for a capital of 40 000 €** [S4] — 0,189 % of
   capital against the grid's 0,17 % — so levels have drifted. A second carrier publishes
   **8,24 €/month in year one for a 40-year-old non-smoker with 50 000 €** [S10], 0,198 %,
   against 0,24 % at age 40 in the grid. **Use the grid for shape; treat its levels as a dated
   data point, not a current rate card.** No other insurer in the corpus publishes any rate
   [S1] [S2] [S6] [S7] [S8] [S9] [S12].
8. **No insurer publishes a *surprime* scale** [S1] [S2] [S3] [S6] [S7]. The mechanics are
   uniformly documented — the offer of reserves is notified by confidential letter naming the
   condition and/or the amount of the *surcotisation*, to be returned within 15 days marked
   "BON POUR ACCORD" [S6] — but no level is public, so `rating_factor` is a pure model-point
   input. The only public French price evidence on rated lives is on borrower cover: the
   average insurance rate for AERAS *écrêtement* beneficiaries is **1,01 % of initial capital
   before capping and 0,65 % after** [REG-R37], which bounds a standard rate from above rather
   than describing one.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Death benefit | The sum assured, from any cause — accident or illness — subject only to the stated exclusions | [S1] [S2] [S3] [S6] [S7] [S9] |
| PTIA benefit | **Anticipated payment of the same capital**, to the insured; payment ends the contract | [S1] [S2] [S3] [S6] [S8] |
| PTIA definition | Two limbs: (a) unfit to engage in any occupation or activity producing gain or profit, and (b) permanent recourse to the assistance of a third person for the ordinary acts of daily life ("se laver, se vêtir, se nourrir, se déplacer"). Recognition requires *consolidation* | [S1] [S3] [S6] [S7] |
| Death/PTIA interlock | The two benefits **cannot be cumulated**; the PTIA capital is due only if the insured is alive on the day of payment, failing which the death cover operates instead | [S1] [S2] |
| Suicide | Not covered in the **first year** of the contract; covered from the second year; the clock restarts on any increase, for the increment only | [R1]; implemented at [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S10] |
| Immediate suicide cover | The alinéa 4 exception (immediate cover, ceiling not below **120 000 €**) reaches only art. L. 141-1 group contracts securing a loan on the insured's **principal residence** — **it does not reach a standalone temporaire décès** | [R1] [R2] |
| *Aide à mourir* | From 20 August 2026, death cover applies to death resulting from the *aide à mourir* under art. L. 1111-12-1 of the Code de la santé publique. **No retrieved product document reflects this yet** | [R1]; administration [unverified] |
| Settlement timing | Within one month of the complete file at the representative carrier; 15 days at one carrier, one month at another; the statutory clock is 15 days to request documents and one month to pay from the complete file | [S3]; [S1] [S9]; [REG-R31] |
| *Avance* on the capital | 4 000 € to the spouse or PACS partner within 48 h; 4 000 €, 5 000 € and 10 % capped at 10 000 € observed elsewhere | [S3]; [S2] [S6] [S8]; not modeled **[std]** (9) |
| Post-death revalorisation | The capital is uprated from death until the file is complete or the sum is deposited at the Caisse des dépôts, at a rate not below the art. R. 132-3-1 floor | [S1] [S2] [S3] [S6]; [REG-R39] |
| Payout modes | Capital; conversion of all or part into a *rente* using the table and technical rate in force **at the date of conversion**; a *versement mixte famille* matrix by beneficiary type | [S3] |
| Annuity conversion charge | 3 % of the capital converted, as *frais de service de la rente* | [S3] |
| Expiry | Cover ceases at the age limit; nothing is payable; no maturity value, no renewal beyond the age limit, no conversion into a savings contract | [S3] [S5] [S11] [S15] [S16] |

9. *Avances* and *acomptes* are advances on a benefit already due, not a separate cover
   [S2] [S3] [S6] [S8]; they change the timing inside the settlement of a claim already
   incurred, a window shorter than the model's month, and are ignored. Post-death
   revalorisation is likewise ignored in the base projection: it runs between death and
   settlement, a sub-monthly window on this product.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Health evidence | Retained in full. The *loi Lemoine* abolition of the health questionnaire applies to qualifying **borrower** cover only; nothing in the corpus removes it from a standalone temporaire décès | [R17] |
| Two-tier declaration | Short *déclaration de santé* / *questionnaire de santé simplifié*, escalating to a full *questionnaire médical* on a trigger and thence to examinations | [S2] [S3] [S6] |
| Simplified-underwriting threshold | No medical examination up to **age 40 for a capital of up to 250 000 €** | [S3] [S4] [S5] |
| The one published numeric grid | Capital ≤ 40 000 € **and** age ≤ 50 → no medical formality, but a **12-month *délai d'attente*** for illness-caused death and PTIA, cotisations returned to the heirs on death inside it; capital > 40 000 € → *questionnaire médical*, no waiting period; age > 50 → *Déclaration de Bonne Santé*, escalating on any "OUI" | [S6] |
| Questionnaire validity | 3 months from signature; changes of health between application and acceptance must be notified | [S1]; [S2] [S3] |
| Underwriting outcomes | Accept at standard rate; accept with a *surprime*/*surcotisation*/*surtarification* and/or partial exclusions, subject to the applicant's acceptance; adjourn; decline | [S1] [S2] [S3] [S6] |
| Provisional cover | Accident-only cover from receipt of the application until acceptance, refusal, renunciation or 30 days, capital limited to 15 000 €, paid net of the temporary death premium | [S3]; [S2] variant |
| Convention AERAS | An *assurance emprunteur* convention. Its own text applies it to *prêts immobiliers*, *prêts professionnels* and *prêts à la consommation affectés ou dédiés*: **a standalone temporaire décès unconnected to a loan is outside AERAS** | [R17] [R18] |
| In-force re-rating | A change of occupation or of sporting activity must be declared and can raise the cotisation or add an exclusion; refusal of the new terms causes resiliation. A return to smoking is a declarable change | [S2] [S7] |
| Misstatement | Arts. L. 113-8 (intentional — contract void, premiums retained) and L. 113-9 (non-intentional — before a claim, premium increase or termination on ten days' notice; after a claim, benefit reduced in the ratio of premiums paid to premiums that would have been due) | [S1] [S2] [S3] [S6] [S7] |

**What the convention AERAS does and does not do to this model.** AERAS is retrieved in full and
its scope is unambiguous: it governs *assurance emprunteur* on property, professional and
dedicated consumer loans, and its Titre IV states "Ce titre s'applique aux prêts professionnels
et immobiliers visés au titre III" [R17]. Nothing in the retrieved text extends it to a
standalone temporaire décès. Its parameters — three examination levels, the third conditioned on
maturity **before the borrower's 71st birthday** and an insured share of outstanding loans
**≤ 420 000 €**; questionnaires dropped on consumer loans **≤ 17 000 €**, term **≤ 4 years**,
applicant **≤ 50**; *écrêtement des surprimes* for eligible incomes (**≤ 1 / 1,25 / 1,5 × PASS**
by number of tax *parts*), capping the premium at **1,4 point in the taux effectif global**; and
a *droit à l'oubli* after **5 years** from the end of the therapeutic protocol without relapse,
with maximum surprime rates set per garantie (Décès, PTIA, GIS) [R17], as amended by an *avenant*
of 5 July 2024 [R18] — are recorded because the *grille de référence* shapes how French medical
officers assess aggravated risks generally. **Effect on this model: none directly** —
`rating_factor` is unbounded on a standalone contract, and the AERAS caps live in
`products/assurance_emprunteur/`.

### Charges

| Parameter | Representative value | Basis |
|---|---|---|
| *Frais de gestion* (management charges) | Built into the tariff; **not separately disclosed on any retrieved contract**. Their existence is load-bearing for reserving: the *provision mathématique* must include future management costs "égale au montant des chargements de gestion prévus dans les conditions tarifaires" | [R11]; disclosure gap [S1] [S2] [S3] [S6] [S7] [S8] [S9] |
| *Frais sur cotisation* (premium load) | Does **not** appear as a separate disclosed line on any retrieved temporaire décès; the disclosed near-equivalents are the fractionation loadings below | [S1] [S2] [S3] [S6] [S7] [S8] [S9] |
| *Frais de fractionnement* | Annual: none, with a **1 % discount** included in the cotisation where paid by direct debit. Half-yearly: **2,50 %**. Quarterly: **4 %**. Monthly: **4 %** | [S1] |
| *Frais d'échéance* | Annual: none. Half-yearly: **3 €**. Quarterly: **6 €**. Monthly: **15 €** for 10 instalments, **18 €** for 12 | [S1] |
| Worked fractionation example | On a monthly-in-12 basis at an annual tariff of 250 € TTC, the embedded loading is 250 − 250/1,04 = **9,61 €** | [S1] |
| Association subscription | **1,30 €** per member per year remitted to the subscriber association, in the group wrapper only | [S1] |
| Annuity conversion charge | **3 %** of the capital converted | [S3] |
| Acquisition and maintenance expense levels | Not disclosed anywhere in the corpus | **[std]** (10) |
| Commission | Not disclosed anywhere in the corpus | **[std]** (10) |
| *Taxe sur les conventions d'assurance* | Cotisations are quoted "TTC" but **no retrieved document states a rate** for this cover | [S1]; rate [unverified] |

10. **No French insurer publishes any pricing basis** — no table, no A/E factor, no expense
    loading, no commission scale, no lapse assumption appears in any retrieved product document
    [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S12], and the published grid [S3] is a gross premium
    scale, not a basis. Every expense and commission level in the technical notes is a
    **[std]** placeholder; the only cited charge figures in this library are the fractionation
    table [S1], the association subscription [S1] and the annuity conversion charge [S3].

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| *Valeur de rachat* | **None.** "Votre adhésion ne comporte ni valeur de rachat, ni valeur de réduction"; "Le contrat ne comprend pas de faculté de rachat" | [R3]; [S7] [S9] |
| *Valeur de réduction* | **None** — prohibited by the same article | [R3] [S7] |
| Effect of a lapse | Pure termination. Cover ends; the unearned portion of a prepaid cotisation may be refunded, except where the termination follows an intentional misstatement or non-payment; nothing else is paid | [S1]; [R3] |
| Non-payment path | Cotisation due within 10 days; registered *mise en demeure*; resiliation 40 days after the letter (Code des assurances) or suspension 30 days after it (Code de la mutualité). No cover attaches to events in the suspension window | [S1] [S2] [S3] [S6] [S7]; [S9]; [S6] |
| Termination by the policyholder | At the annual échéance, by registered letter at least one month before. Observed elsewhere: two months before 31 December, at any time, before 1 November for 31 December | [S3]; [S1] [S2] [S8] [S9] |
| Termination of right | At the age limits; on death; on payment of the PTIA capital; on termination of the underlying group contract | [S1] [S2] [S3] [S6] [S9] |
| *Renonciation* | **30 calendar days** from being informed that the contract is concluded, with repayment of all sums paid within 30 days | [S3]; [S1] [S2]; [REG-R29] |
| Reinstatement | No general contractual reinstatement right appears in the retrieved conditions; a lapse is final in the composite | scope **[std]** (11) |
| Prescription | Two years from the event, ten years where the beneficiary is a person distinct from the member, thirty years from the death as a long-stop | [S1] [S3] |
| Unclaimed capital | Deposited at the Caisse des dépôts et consignations ten years after the insurer's knowledge of the death or the contract's term, within the following month | [S1]; [REG-R39] |

11. Only one carrier's suicide clause running "from the date cover started **or restarted**"
    hints at a restart mechanism [S8], and no retrieved document sets out a general
    reinstatement provision. The composite terminates lapsed contracts finally, which is
    also the conservative choice for a product with no cash value.

---

## Contractual mechanics

### Cotisation révisable par âge — the operative rule

At the effective date and again at **every annual renewal**, the cotisation for the coming
policy year is

    cotisation(t) = sum_assured × tariff_rate(attained_age(t)) × rating_factor × frequency_load

where `attained_age(t)` is the *différence de millésime* age at that renewal
[S1] [S2] [S6] [S7], `tariff_rate` is read from the insurer's rate card in force at that date
[S3], and `rating_factor` carries any *surprime* accepted at underwriting [S1] [S2] [S3] [S6].
Four contracts state the rule in their own words: "l'âge de l'assuré à la date d'effet de
l'adhésion **puis à la date de la reconduction**" [S1]; "La cotisation évolue chaque année en
fonction de votre âge" [S2]; "votre cotisation évoluera en cours de contrat en fonction de
votre âge : elle sera donc calculée à chaque échéance annuelle" [S3], with the current page
repeating "recalcul chaque année" [S4]; "les cotisations évoluent, à l'échéance anniversaire
de l'adhésion, en fonction de l'âge de l'assuré" [S7].

Two consequences follow and both are load-bearing. First, **there is no prefunding**: each
year's cotisation buys that year's risk, so the *provision mathématique* is close to nil at
each anniversary and what remains is an unearned-premium and outstanding-claims position
[R11] [R13]. Second, the cotisation rises steeply — on the published grid it is **32,4× larger
at age 74 than at age 34** [S3] — so the premium stream, not the benefit stream, carries the
shape of the liability. The grid also carries a **tariff discontinuity that is not a mortality
discontinuity**: from age 59 to age 60 the rate steps from 1,13 % to 1,56 %, **+38 %** against
a surrounding trend of about +8 % per year of age [S3]. A fitted curve smooths it away; a rate
table preserves it, which is why the reference implementation reads the grid as data.

### The cotisation constante variant

The `constante` (also *nivelée*) form charges one cotisation for the whole cover period. **It
was not found on any French standalone contract in this research**
[S1] [S2] [S3] [S6] [S7] [S9] [S10] and is a **[std]** construction (footnote 2). It is
retained because it is the form that generates a real French *provision mathématique*: where
the premium rate is flat while the death rate rises, "un montant de PRC est toujours constitué
pendant la durée", whereas a tariff expressed on an initial rather than a declining capital
tends to produce a negative provision early, on which the non-negativity floor then bites
[R11] [R13]. The standardized definition, stated in full in the technical notes, is the level
cotisation whose actuarial present value equals that of the revisable stream over the cover
period, on the tariff mortality basis and the technical rate.

### Benefit shape — capital constant, capital décroissant

The benefit is the sum assured throughout, from any cause [S1] [S2] [S3] [S6] [S7] [S9].
Increases re-open selection except for defined life-event or automatic increments — a 5 000 €
*forfait* every 5 years plus the same 5 000 € within 12 months of a birth, adoption, marriage,
PACS, divorce, PACS break-up or the death of the spouse, **at most four formality-free
increases over the life of the contract** and only to the échéance following age 65 [S3];
another carrier allows +20 % within 3 months of the same events [S7]. **On any increase the
suicide clock restarts for the increment only** [S1] [S2] [S3] [S6] [S7] — art. L. 132-7 alinéa
2 operating directly [R1]. Optional *revalorisation* indexes capital and cotisation together, on
the *plafond annuel de la Sécurité sociale* (PASS) [S1] [S7] or at an insurer-set rate
[S2] [S6]; refusal is possible and, at three carriers, **definitive** [S2] [S6] [S7].

A decreasing sum insured following an amortisation schedule is a **loan-cover** design [S15] and
appears in none of the retrieved standalone contracts. The composite carries it as a
`benefit_shape` value driven by an external schedule table so the chassis can serve
`products/assurance_emprunteur/`, where the industry distinction between a tariff on *capital
initial* and one on *capital restant dû* lives [R13].

### PTIA — the anticipated payment of the death capital

PTIA pays **the death capital, early, to the insured**, and payment terminates the contract
[S1] [S2] [S3] [S6] [S8]. Naming varies without changing the substance: PTIA
[S1] [S2] [S6] [S8] [S10]; *invalidité permanente absolue* (IPA) [S3]; *invalidité permanente
totale* (IPT) [S7]; *invalidité fonctionnelle totale et définitive* (IFTD) [S12]. Four interlocks
are explicit in the contracts and all four must survive into the model: death and PTIA benefits
**cannot be cumulated** [S1]; payment of the PTIA capital **ends the contract and the death
cover** [S2] [S3] [S6]; the capital is due only if the insured is **alive on the day of
payment**, failing which the death cover operates instead [S2]; and premium payment ceases at
death and at recognition of PTIA/IPT [S3] [S7]. **PTIA cover usually ceases earlier than the
death cover, but not always** — 65 vs 75 [S3], 75 vs 80 [S2], 80 vs 85 [S6], 67 vs 85 [S7],
65 vs 70 [S8], against one carrier where both end at 85 [S1] and one contract with no PTIA cover
at all [S9]. Five of the eight carriers, so a model must carry the two ages as separate
parameters rather than assume the gap.

One retrieved contract carries a genuine **second** decrement on an already-accelerated life: a
further capital where the insured, already in IPT, dies at least a year after consolidation
[S7]. That *capital décès double garantie* rider is the one place where paying twice is correct,
and it is out of scope here (see Riders and options).

### Suicide — art. L. 132-7

Alinéa 1: "L'assurance en cas de décès est de nul effet si l'assuré se donne volontairement la
mort au cours de la première année du contrat." Alinéa 2 requires cover from the second year and
restarts the clock, for the supplementary guarantees only, on any increase of cover [R1]. Every
retrieved contract carries exactly that and no more [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S10];
one frames it as suicide "conscient ou inconscient" [S7]. The **immediate** suicide cover of
alinéa 4, whose ceiling art. R. 132-5 fixes at not less than **120 000 €**, is confined to art.
L. 141-1 group contracts securing a loan taken to acquire the insured's **principal residence**
[R1] [R2]: it does not reach a standalone temporaire décès and this model must not carry it. The
model implements alinéa 1 as a **first-year benefit exclusion factor on death claims only** —
PTIA is not death and is unaffected; the factor and its rationale are in the technical notes.

### No rachat, no réduction

Art. L. 132-23 alinéa 1 is the legal foundation of the whole cash-flow shape: "Les assurances
temporaires en cas de décès ainsi que les rentes viagères immédiates ou en cours de service ne
peuvent comporter ni réduction ni rachat" [R3]. The insurers restate it in their own words
[S5] [S7] [S9], and the guides restate the consequence: "aucun capital n'est versé et les
cotisations déjà payées ne sont pas remboursées" [S16]. The *rachat* machinery of arts.
L. 132-20 ff. [REG-R31] is written for contracts that **have** a surrender value and is
inoperative here because L. 132-23 removes the value it would act upon [R3]. The one place
surrender value still appears in a reserving text is art. A. 343-1-1, which floors the *provision
mathématique* at the surrender value and at the reduced-capital provision — both **zero** here,
so the operative floor is simply that the provision may not be negative [R13].

### Waiting periods and provisional cover

Two mechanisms exist and must not be confused. A ***délai d'attente*** delays the start of cover:
12 months for illness-caused death and PTIA where the adhesion carried no medical formality, with
the cotisations collected returned to the heirs on death inside the window [S6]; 3 months at
another carrier, waived for accidental death or where equivalent cover was already held [S9].
None appears at five of the eight carriers [S1] [S2] [S3] [S7] [S8]. A ***garantie provisoire***
covers accidental causes *during* medical underwriting: 30 days and 15 000 € at the
representative carrier, paid net of the temporary death premium [S3]; 60 days and 76 000 € at
another [S2]. The composite runs with **no waiting period** [S3] and carries `waiting_period_y`
as a model-point column so the [S6] and [S9] variants can be switched on.

### Expiry, the age basis and lapse

Cover ends at a policy-year boundary defined by attained age, and nothing is payable at that
boundary [S3] [S5] [S11] [S15] [S16]. The age driving both the tariff and the limits is the
***différence de millésime***: "pour une personne née en 1967, l'âge retenu en 2019 est :
2019 − 1967 = 52 ans" [S2] — an integer age that increments on 1 January rather than on the
policyholder's birthday [S1] [S2] [S6] [S7], and the single most important convention to get
right in a French life model. The reference model steps monthly, and the age nevertheless steps
at the **policy anniversary** and not monthly: a finer projection grid does not make the age
basis finer. The non-payment path is the whole of the lapse machinery,
because there is no value to forfeit: the cotisation is due within 10 days; a registered *mise en
demeure* follows; resiliation takes effect 40 days after the letter under the Code des assurances
[S1] [S2] [S3] [S6] [S7], or cover is suspended 30 days after it under the Code de la mutualité
[S9], with no cover attaching to events in the suspension window [S6]. The voluntary notice
regime differs materially — one month before the échéance [S3], two months before 31 December
[S1], at any time [S2] [S8], before 1 November for a 31 December exit [S9] — and it drives the
lapse timing a model assumes.

---

## Riders and options

**In scope (modeled or parameterized):** the **PTIA acceleration**, embedded rather than
optional at the representative carrier and modeled as a second decrement paying the same
capital and terminating the contract [S1] [S2] [S3] [S6] [S8]; the **accidental multiplier**
`accident_multiplier`, base value 1.0 — observed as an additional capital equal to the death
capital where death or PTIA follows an accident within 12 months [S1] [S2] [S6] [S7], as
**50 %** rather than 100 % at one carrier [S9], as ×2 for an accident and **×3** for a
road-traffic accident, terrorism, an *attentat* or an *agression* at another [S12], with 24
months allowed for IPT by accident at a third [S7], and usually capital-capped [S1] [S6], but
run off in the base case because no retrieved source gives an accidental share of deaths; the
**surprime** `rating_factor` (footnote 8); the **waiting period** `waiting_period_y`, with
return of cotisations on death inside the window [S6], base run 0; and **indexation** on the
PASS or an insurer rate, described but not projected because the index is exogenous
[S1] [S2] [S6] [S7].

**Out of scope:** *double effet*, a further capital to the children fiscally dependent on the
spouse or PACS partner where that person dies simultaneously with or after the insured, capped
at 500 000 € at one carrier [S7] [S8] — a second life is required and no model point carries
one; *capital décès double garantie*, a further capital where the insured, already in IPT,
dies at least one year after consolidation [S7], excluded precisely because it is the
exception that makes the "never paid twice" rule testable; *rente éducation*, 75 € – 3 810 €
per quarter per child to 31 December preceding the child's 26th birthday [S1], with
100 % / 125 % / 150 % steps [S7] or ≤ 2 000 €/month [S10] elsewhere; *rente de conjoint* /
*rente décès*, halved from the beneficiary's 65th birthday [S7], ≤ 5 000 €/month elsewhere
[S10]; the *maladie grave* 5 000 € flat capital on the representative carrier's current page
[S4] but absent from its own note d'information [S3]; the assistance packages every retrieved
contract bundles [S2] [S3] [S6] [S9], which carry no material cash flow; and annuity
conversion of the death capital, a post-death payout mode on the same capital using the tables
and technical rate in force at conversion [S1] [S3] with a 3 % conversion charge [S3] — the
annuity itself belongs to `products/rente_viagere/`.

---

## Variations across insurers

1. **Wrapper.** Individual contract [S3] vs group *adhésion facultative* under arts. L. 141-1
   ff. [S1] [S2] [S6] [S7] vs *Code de la mutualité* collective [S9] vs *bancassurance* tied to
   an account [S8]. Composite: individual, because the rate card belongs to it. The economics
   are identical; the timers and the exit rules are not.
2. **Age envelope.** Entry from 18 to somewhere between 57 [S12] and 84 [S10]; death cover
   ceasing between 65 [S9] and 90 [S10]. Composite: entry ≤ 65, death cover to 75 [S3].
3. **PTIA cessation relative to death cessation.** Earlier in five of the eight carriers —
   65/75 [S3], 75/80 [S2], 80/85 [S6], 67/85 [S7], 65/70 [S8] — equal in one [S1], absent in one
   [S9], unstated in one [S10]. Composite: earlier, with both ages as model-point columns.
4. **Waiting period.** None at five carriers [S1] [S2] [S3] [S7] [S8]; 12 months where
   underwriting is waived, with return of cotisations [S6]; 3 months unconditionally [S9].
   Composite: none, with the mechanism parameterized.
5. **Accidental option.** Doubling [S1] [S2] [S7] [S12]; an additional capital equal to the
   death capital [S6]; **+50 %** [S9]; tripling for road accidents, terrorism, *attentat* or
   *agression* [S12]; none in the representative note [S3]. Composite: a multiplier column, base
   1.0 — the variation is too wide, and the incidence data too absent, to standardize a level.
6. **Smoker and occupation rating.** Smoker rating at three carriers [S1] [S7] [S10], absent
   from four [S2] [S6] [S8] [S9]; occupation as an explicit tariff group at one [S7], a
   hazardous-occupation annex at three [S2] [S6] [S9], an entry exclusion at one [S1].
   Composite: both carried as columns feeding `rating_factor`; neither has a published level.
7. **Indexation.** PASS-linked [S1] [S7]; insurer-set rate [S2] [S6]; not in the representative
   note [S3]; refusal definitive at three carriers [S2] [S6] [S7]. Composite: described, not
   projected.
8. **Participation aux bénéfices.** One carrier states flatly "Le contrat ne prévoit pas de
   participation aux bénéfices" [S9]; two run a PB computed **globally across the insurer's life
   book** and distributed as higher benefits and/or lower cotisations called, not as a
   policy-level account [S1] [S2]. **There is no policyholder account value in any retrieved
   contract.** Composite: non-participating.
9. **Charge disclosure.** One full fractionation table [S1]; charges stated in the *certificat
   individuel de garantie* rather than the notice at two [S2] [S6]; nothing at the rest.
   Composite: the one published table, as the observed range.
10. **What does not vary — with two exceptions worth naming.** The first-year suicide exclusion
    is implemented by every retrieved carrier, and by exactly as much as the statute requires
    [R1] [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S10]; the absence of any surrender or reduction
    value and expiry without value are statutory [R3] and are said in those words by the
    carriers that address them at all [S5] [S7] [S9] [S11] [S15] [S16]. All three are legal
    facts rather than commercial ones. The other two limbs of the composite's core each have one
    carrier that does not support them. **Attained-age revisable pricing**: seven carriers
    [S1] [S2] [S3] [S6] [S7] [S9] [S10], with the *bancassurance* IPID stating no premium basis
    [S8] — a silence, not a contradiction. **PTIA acceleration of the same capital, ending the
    contract**: seven carriers [S1] [S2] [S3] [S6] [S7] [S8] [S10], with the *Code de la
    mutualité* contract carrying **no PTIA cover at all** [S9] — a real exception, and the reason
    `ptia_ratio` and `ptia_end_age` are model-point columns rather than constants.

---

## Regulatory context

**Contract law — Code des assurances.** The product sits in *branche 20 (vie-décès)* of art.
R. 321-1 [S1] [S3] [S7]. Three articles do most of the work: **L. 132-7** (suicide — void in
year one, covered from year two, the clock restarting on an increase; immediate cover with a
floor of 120 000 € confined to principal-residence loan cover; and, from 20 August 2026,
cover of death by *aide à mourir*) [R1] [R2]; **L. 132-23** (no *réduction*, no *rachat* on a
temporaire décès) [R3]; and **L. 132-26** (errors of age) [S7]. Renunciation is 30 calendar
days with repayment of all sums within 30 days [REG-R29] [S1] [S2] [S3]; the *notice
d'information* and the one-page *encadré* are prescribed by arts. A. 132-4 and A. 132-8
[REG-R30]; and the death-settlement clock — 15 days to request documents, one month to pay
from the complete file — is art. L. 132-23-1 [REG-R31]. Unclaimed capital transfers to the
Caisse des dépôts after ten years, with revaluation continuing until the deposit
[REG-R39] [S1]. The *mutualité* form runs the same economics under Livre II of the Code de la
mutualité, with a 30-day rather than 40-day suspension timer and renunciation under art.
L. 223-8 [S9].

**Tariff bases.** Art. **A. 132-18** governs what a French tariff may be built on: a technical
interest rate fixed under art. A. 132-1, plus one of exactly two families of mortality table —
**(a)** tables homologated by ministerial *arrêté*, by sex, built on INSEE data for non-annuity
contracts, or **(b)** the undertaking's own tables, by sex or not, **certified by an independent
actuary** approved by a recognised actuarial association [R4] [REG-R23]. Where a single
family-(a) table is used for all insureds it must be the one giving **the most prudent tariff**
— for a death cover, the male table [R4]. The homologated non-annuity tables are **TH 00-02**
(male) and **TF 00-02** (female), homologated by the arrêté du 20 décembre 2005 with effect from
1 January 2006 and built by INSEE on French mortality observed over 2000–2002 [R6] [R9]
[REG-R22]; the generational **TGH05/TGF05** apply to *rentes viagères* and reach this product
only through an annuity conversion [R7]. The historic home of the rule, art. **A. 335-1**, was
abrogated with effect from 1 January 2016, so any citation of it in a current French product
document is a legacy reference [R8]. The annexed ***décalages d'âge*** (age shifts) are required
by a clause with a scope this product falls outside: "pour les contrats **en cas de vie** autres
que les contrats de rente viagère, les tables mentionnées au a sont utilisées en corrigeant
l'âge de l'assuré conformément aux décalages d'âge ci-annexés" [R4] [R6] [REG-R23]. A temporaire
décès is a contract *en cas de décès*, so on the retrieved texts **no age shift is required
here** — a user substituting TH 00-02 for the [std] proxy should apply the table unshifted.
Where the shifts do bite, the profession's own note records that the arrêté specifies them but
not how to apply them, and recommends applying them **to the q(x), not to the l(x)**, because
shifting l(x) produces erratic q(x) growth and hence erratic provisions [R9]. The numeric annexe to the current A. 132-18 was **not retrieved** [R4]; the abrogated
A. 335-1 annexe carried shifts from **−11 years at ages 16–32 to 0 at age 94+** for TF 00-02 and
from **−13 years at ages 16–38 to −3 at age 75+** for TH 00-02 [REG-R23]. A newer derogation,
art. A. 132-18-1 (arrêté du 18 novembre 2024), allowing a single table for art. L. 911-1 CSS
contracts, was read only from a section listing and is [unverified] [R4].

**Technical interest rate.** Art. A. 132-1 caps a tariff rate at **75 % of the TME** (*taux
moyen des emprunts de l'État français*) and, beyond eight years, at the lower of **3,5 %** and
**60 % of the TME**; and — decisively for an annually renewable product — "pour les contrats à
primes périodiques ou à capital variable, **quelle que soit leur durée**, ce taux ne peut
excéder le plus bas des deux taux suivants : 3,5 % ou 60 % du taux moyen" [R5] [REG-R17]. The
rate-step *barème* reported by secondary summaries was not visible in the retrieved article text
and is [unverified] [R5].

**Unisex pricing.** Art. L. 111-7 forbids direct or indirect sex-based differences in premiums
and benefits; the surviving derogation covers only contracts and group-contract adhesions
"conclus ou effectuées **au plus tard le 20 décembre 2012**" [R10]. New business has therefore
been unisex since 21 December 2012, while the homologated valuation tables remain sex-specific
[R6] [REG-R22] — **the same reconciliation problem the annuity product faces**, resolved the
same two ways: take the single most prudent family-(a) table [R4], or blend. The Institut des
actuaires' working group uses **60 % TH 00-02 / 40 % TF 00-02** as its unisex death basis [R13];
neither weighting is prescribed by any retrieved text, so a model that adopts one must tag it
**[std]**. See `products/rente_viagere/product-spec.md` for the annuity side of the same
tension. On group business the pressure is relieved by a further clause: "pour les contrats
collectifs en cas de décès **résiliables annuellement**, le tarif peut être établi d'après les
tables mentionnées au a **avec une méthode forfaitaire** si celle-ci est justifiable" [R4]
[REG-R23] — which covers most of the group products in this file [S1] [S2] [S6] [S7] and
explains why their published rate structures are coarse.

**Statutory provisions and prudential.** Art. R. 343-3 enumerates the eleven French life
technical provisions; the operative one here is the ***provision mathématique***, which **must
include an estimate of future management costs** equal to the *chargements de gestion* built into
the tariff, and the list also carries a *provision d'égalisation* specifically for *assurance de
groupe contre le risque décès* [R11] [REG-R6]. The *provision pour risques croissants* of art.
R. 343-7 is defined for *maladie* and *invalidité*, not death; its death-cover analogue is the
R. 343-3 PM — "la même provision de prime s'appelle PM en vie et PRC en non-vie"
[R12] [R13] — and art. A. 343-1-1 floors it at zero, at the surrender value and at the
reduced-capital provision, the last two being zero here [R3] [R13]. Above that sits Solvabilité
II: best estimate plus risk margin under Directive 2009/138/CE [REG-R1] and Delegated Regulation
(EU) 2015/35 [REG-R2] as described by EIOPA [REG-R4], with the curves published monthly
[REG-R5]; Directive (EU) 2025/2 takes effect **30 January 2027** [REG-R3] and nothing here
implements a 2027 basis. The ACPR supervises under art. L. 612-1 of the Code monétaire et
financier [REG-R10] and is named in four of the retrieved notices [S1] [S2] [S6] [S9]; its own
site could not be retrieved, so **no ACPR analysis of the prévoyance market is cited anywhere in
this product's documents** [R20]. The statutory participation aux bénéfices obligation of art.
L. 331-3 [REG-R14] applies but is discharged globally at insurer level, not credited to a policy
[S1] [S2]; one contract has none at all [S9].

**Taxation.** The death capital is outside the estate [S1] [S3]. What applies instead is the
art. **990 I** levy on premiums paid **before the insured's 70th birthday**: an abattement of
**152 500 € per beneficiary** across all life contracts of the same insured, then **20 %** up to
**700 000 €** of the taxable share and **31,25 %** above [R14] [R15] [R16] [REG-R41] [S1]. An
insurer applies it in capital terms — 20 % between 152 500 € and 852 500 €, 31,25 % above
852 500 € — and withholds and remits it, which is why the beneficiary files an *attestation sur
l'honneur* recording how much of the abattement is already used [R16]. BOFiP confirms the scope
point that matters here: the levy **expressly reaches *assurance décès temporaire* and
*assurance décès pure*** where the beneficiary is designated *à titre gratuit*, and **excludes**
contracts designated *à titre onéreux* — the paradigm being loan cover assigned to a lender
[R15]. Premiums paid **from the 70th birthday** on contracts subscribed after 20 November 1991
fall instead under art. **757 B**, with a single global abattement of **30 500 €** shared across
taxable beneficiaries and all the insured's life contracts, the charge falling on the premiums
only [R15] [REG-R41] [S1] [S3]; the article itself was not retrieved in the product research
[R19], so the product-level citation rests on [R15], [R16] and [REG-R41]. Spouse and PACS
partner are wholly exempt, as are siblings meeting the cumulative conditions
[R14] [R15] [R16] [S1] [S7]. Premiums are **not deductible**; the representative carrier instead
imposes a declaration duty on annual premiums above **305 €** paid before age 70 [S3]. And,
distinctively, "L'assurance temporaire décès à la différence de l'assurance vie **n'est pas
soumise aux prélèvements sociaux**" [S1].

**Professional standards.** Actuarial modeling of this product sits under the Institut des
actuaires' *Norme de Pratique Actuarielle 2 — Modèles actuariels*, a recommended practice
adopted 15 June 2015 with effect from 1 January 2016, whose scope expressly covers pricing and
the technical studies attached to new products [REG-R44]. IFRS 17 applies to IFRS reporters from
1 January 2023 with no French carve-out [REG-R45].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-temporaire_deces-r1
[R10]: #frlib-temporaire_deces-r10
[R11]: #frlib-temporaire_deces-r11
[R12]: #frlib-temporaire_deces-r12
[R13]: #frlib-temporaire_deces-r13
[R14]: #frlib-temporaire_deces-r14
[R15]: #frlib-temporaire_deces-r15
[R16]: #frlib-temporaire_deces-r16
[R17]: #frlib-temporaire_deces-r17
[R18]: #frlib-temporaire_deces-r18
[R19]: #frlib-temporaire_deces-r19
[R2]: #frlib-temporaire_deces-r2
[R20]: #frlib-temporaire_deces-r20
[R21]: #frlib-temporaire_deces-r21
[R3]: #frlib-temporaire_deces-r3
[R4]: #frlib-temporaire_deces-r4
[R5]: #frlib-temporaire_deces-r5
[R6]: #frlib-temporaire_deces-r6
[R7]: #frlib-temporaire_deces-r7
[R8]: #frlib-temporaire_deces-r8
[R9]: #frlib-temporaire_deces-r9
[REG-R1]: #frlib-reg-r1
[REG-R10]: #frlib-reg-r10
[REG-R14]: #frlib-reg-r14
[REG-R17]: #frlib-reg-r17
[REG-R2]: #frlib-reg-r2
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R29]: #frlib-reg-r29
[REG-R3]: #frlib-reg-r3
[REG-R30]: #frlib-reg-r30
[REG-R31]: #frlib-reg-r31
[REG-R37]: #frlib-reg-r37
[REG-R39]: #frlib-reg-r39
[REG-R4]: #frlib-reg-r4
[REG-R41]: #frlib-reg-r41
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R49]: #frlib-reg-r49
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
