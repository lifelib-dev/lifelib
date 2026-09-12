# Product Specification

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It describes no single insurer's product. Facts carrying a
source tag — [S#] (primary product documents) and [R#] (product-specific
regulatory/actuarial references), both numbered per `_research/dependance.md` — resolve
against `sources.md` in this directory; that numbering is carried over verbatim and is
never renumbered. [REG-R#] tags resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is frozen
separately. Values marked **[std]** are standardizations introduced for the reference
implementation; every [std] row in a parameter table carries a numbered footnote giving
the rationale and, where the research file recorded one, the observed range across
insurers. Claims the research file could not confirm against a retrieved document are
flagged [unverified] here too. French terms of art are kept in French and glossed on first
use; the model built from this specification is **Dep_FR_S**, on a monthly grid, and its
cells, columns and CSV headers are English `lower_snake_case` throughout.

---

## Product overview and market role

French individual long-term-care insurance — *assurance dépendance* — pays a *rente
mensuelle viagère* (a lifetime monthly annuity) once the insured is recognised in a
contractual state of *dépendance* (loss of autonomy), usually alongside an optional
*capital d'équipement* (an equipment and home-adaptation lump sum) and a package of
*prestations d'assistance* (care-coordination services) [R8 §2.2](#frlib-dependance-r8) [S1] [S2] [S3] [S4]
[S8] [S10]. Three structural facts shape everything below.

**It is written as a group contract that individuals join.** Almost every retrieved
"individual" product is a *contrat d'assurance de groupe à adhésion facultative* — a
policy subscribed by an association or a distributor, which the customer joins by signing
a *bulletin d'adhésion*. Confirmed subscribers: ANPERE for AXA [S1 §1.1.1], the
Fédérations Régionales de Crédit Mutuel and APCAS for Suravenir [S7 p2], the Banque de
France for CNP 0658 Q [S5 art. 1], the MSPP for CNP A063 F [S6 art. 1.1]; Antarius, BPCE
Prévoyance and Sogecap are described the same way [S2] [S3] [R12 §1.2.1](#frlib-dependance-r12). The customer
therefore holds a *notice d'information*, not *conditions générales*, and the *notice* is
the contractual document [REG-R30]. The wrapper is annual and tacitly renewed; the
membership inside it is *viagère* — lifelong — and survives termination of the wrapper as
long as premiums are paid [S1 §8.2] [S5 art. 25].

**It is a non-life risk carrying a lifelong guarantee.** Cover sits in branches 1
(Accidents) and 2 (Maladie) of art. R. 321-1 of the Code des assurances [S1 §1.1.1] [S3]
[S6 art. 1.1]; optional death benefits sold alongside sit in branch 20 (Vie-Décès)
[S1 §1.1.1]. There is no LTC-specific regime in the Code des assurances, the branch
*agrément* is at the insurer's discretion, and on [R12]'s reading the *participation aux
bénéfices* obligation does not bite because the risk covered is not human life
[R12 §1.1.2.2](#frlib-dependance-r12). That reading is one actuarial dissertation's, not a settled position:
art. L. 331-3 states the obligation in general terms, and the reference entry for it records
that case law and parliamentary answers hold **no category of contract to be carved out of
the obligation *a priori*** [REG-R14]. Under Solvabilité II the business falls in the
**Health-SLT** underwriting module, life techniques applying because of the long-term
commitment [R12 §1.1.2.1](#frlib-dependance-r12)
[REG-R4].

**It is *fonds perdu*.** There is no surrender value at any time — "Votre adhésion ne
comporte pas de valeur de rachat" [S1 §7.3] — and if the insured stays autonomous until
death, nothing is paid and the premiums are lost [S11]. What replaces surrender is a
*mise en réduction*: after a qualifying number of years of premiums a lapsing member keeps
a reduced *rente* determined by a *barème* [S1 §1.3] [S2] [S5 art. 24.2] [S7 §4.6]
[R12 §1.2.1](#frlib-dependance-r12). The Code des assurances requires the contract to state how that *valeur de
réduction* is computed [REG-R31]; the CCSF's standing criticism is that it is not
highlighted clearly enough at the point of sale [R8 §4.2](#frlib-dependance-r8).

Market scale, 2024. Insurance undertakings covered **2.4 million** people, down 6.9% on
the year, individual memberships (two thirds of the portfolio) falling 9.9%; **28,400**
new subscribers, down 13.7%; premiums **618.1 M€**, down 3.0%; benefits paid **357.3 M€**,
up 6.3%; provisions **6.4 Md€**, falling for a third consecutive year; **44,200** *rentes*
in payment on sole-and-principal-guarantee contracts, **41,900** of them individual, at a
**mean monthly rente of 583 €** and a mean age at onset of **80**; typical subscription
age **64** [R10 §2.3](#frlib-dependance-r10) [R13 p6](#frlib-dependance-r13) [REG-R28]. Across mutuelles, insurance undertakings and
institutions de prévoyance together, **6.0 million** people were insured — 56% / 40% / 4%
[R13 p6](#frlib-dependance-r13) [REG-R28]. DREES puts dependence cover at about **1%** of the premiums private
insurers collect for social risks [R14]; the CCSF's aggregate is **814 M€** of premiums
for **2.64 million** people, 28% collective [R9 §1](#frlib-dependance-r9).

The representative design below is the individual *rente viagère* design of **AXA
*Entour'Age* [S1]**, which the research file identifies as the cleanest representative of
the retrieved individual market: group contract with facultative membership, entry 40–75,
a chosen *rente mensuelle viagère*, a *dépendance totale* trigger on an AVQ count with
cognitive alternatives, an optional *dépendance partielle* at 50%, an optional *capital
d'équipement*, waiting periods of nil / 1 year / 3 years by cause, a three-month absolute
*franchise*, monthly payment in arrears, discretionary annual *revalorisation* of both the
guarantee and the *rente* in service, a premium level for the entry age but revisable for
the portfolio, no surrender value and a paid-up reduction after eight years. The purely
GIR-triggered designs [S3] [S7], the severity-ladder design [S5] and the points-based
collective design [R13 pp. 17–21](#frlib-dependance-r13) are documented as variations.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Individual *assurance dépendance*, *rente mensuelle viagère* form, written as a *contrat de groupe à adhésion facultative*, branches 1 and 2 of art. R. 321-1 | [S1 §1.1.1] [S3] [S6 art. 1.1] |
| Cover duration | *Viagère* from the effective date; no age limit — "L'Assuré reste garanti quels que soient son âge et l'évolution de son état de santé" | [S5 art. 8] [S1 §1.1.5] |
| Entry ages | 40–75 inclusive at signature, age by *différence de millésimes* | [S1 §1.1.2.1]; band **[std]** (1) |
| Underwriting | Two-stage: short *déclaration d'état de santé*, then a full *questionnaire de santé* assessed by the *médecin-conseil*, who sets acceptance terms; a *majoration tarifaire pour risque aggravé* may be applied | [S5 art. 3] [S7 §2.2] [S3] [S4] [S1 §1.2.1] |
| Territorial scope | Residence in metropolitan France, Monaco or a DOM; stays outside of no more than three continuous months | [S1 §1.1.6] [S3]; composite **[std]** (3) |
| Renunciation | 30 days from signature | [S1 §7.6] [S5 art. 8] [S7 §2.5] — the window only; no retrieved document states what becomes of premiums already paid |
| Resiliation by the member | Annually, 60 days' notice | [S1 §1.1.4.2a]; window pick **[std]** (4) |
| Surrender value | **None at any duration** | [S1 §7.3] [S11] |
| Base model cell | Female, entry age 70, *formule* Dépendance Totale et Partielle, *rente totale* 1,000 €/month, *rente partielle* 500 €/month, *capital d'équipement* 3,500 €, `trigger_grid = avq5`, premium 75 €/month | rente/premium pair [R8 §2.2](#frlib-dependance-r8); remainder **[std]** (2) |

Footnotes to **[std]** rows:

1. Observed entry-age bands: 40–75 inclusive [S1 §1.1.2.1]; 50 to under 75 [S2]
   [R12 §1.2.1](#frlib-dependance-r12); under 75 [S5 art. 2] [S7 §2.1]; recommended from 40, generally not
   available after 77 [S8]. The compulsory group variant runs cover only to 65 for members
   joining after inception [S6 IPID]; two IPIDs state nothing [S3] [S4] — a silence of the
   retrieved document, which by construction summarises and omits, and not a finding that
   there is no limit. 40–75 is
   the widest band in a retrieved *notice*.
2. Pure modeling cell, except the price point. Entry at 70 sits inside every retrieved
   band and above the market mean subscription age of 64 [R10 §2.3](#frlib-dependance-r10) [R13 p6](#frlib-dependance-r13) [REG-R28].
   The 1,000 €/month total plus 500 €/month partial cover at **75 €/month** is *not*
   [std]: it is the CCSF's indicative market price for exactly that cover at entry age 70,
   published in 2013 [R8 §2.2](#frlib-dependance-r8) — the only age-graded price point for a two-tier individual
   contract in any retrieved source, the CNP Banque de France scale [S5 annexe 1] being
   for a group product on a **four-rung severity ladder** (2, 3, 4 and 5-or-6 AVQ of 6) sold
   across **five subscribed coverage levels** [S5 arts. 13, 16, 17, annexe 1]. It is dated
   and indicative; it is used because inventing a premium would be worse. For scale, the
   2024 mean individual premium on a sole-and-principal-guarantee contract was
   **472 €/year (39 €/month)** at a mean subscription age of 64, and the mean *rente* in
   payment **583 €/month** [R10 §2.3](#frlib-dependance-r10)
   [R13 p6](#frlib-dependance-r13) — so the base cell is a larger-than-average cover bought later than average,
   and its premium is correspondingly above the market mean. Sex is female because 70% of
   APA beneficiaries are women and the female prevalence rate is nearly double the male one
   (9.1% against 4.8% of the 60-and-over population) [R7], which is where the decrement
   basis of `technical-notes.md` is anchored; the *premium* is unisex, compulsory since the
   2004 EU directive [R12 §3.2.1](#frlib-dependance-r12).
3. Observed clauses run from metropolitan France, Monaco or a DOM with the carer resident
   too [S1 §1.1.6], through principal residence in metropolitan France or DOM/TOM [S4] and
   recognition performed in France or an EU country [S7 §3.6], to worldwide cover with
   stays outside France capped at three continuous months [S2] [S3], and at most 90 days a
   year outside the EU with benefit paid only from return to France so that medical control
   can be exercised [S6 IPID]. No cash-flow effect in the reference model.
4. Observed notice: 60 days [S1 §1.1.4.2a]; one month [S7 §4.5]; before 1 November for a
   1 January effect [S5 art. 9a]. No cash-flow effect on a monthly grid.

### The two assessment grids and the trigger definitions

There is no single French definition of dependence in insurance. Two referentials coexist
and contracts use one, the other, or both [R8 §3.2](#frlib-dependance-r8) [R12 §1.1.1](#frlib-dependance-r12).

**(a) AGGIR — the public grid.** *Autonomie Gérontologie Groupes Iso-Ressources*.
Statutory, annexed to the Code de l'action sociale et des familles as annexe 2-1 in the
version created by *décret n° 2017-882 du 9 mai 2017* art. 5 [R1]; referenced by CASF
art. R. 232-3 and used by *départements* to award the *allocation personnalisée
d'autonomie* (APA), which is restricted to GIR 1 to 4 [R2 arts. R. 232-3, R. 232-4](#frlib-dependance-r2) [R3].
Ten *variables discriminantes* (cohérence, orientation, toilette, habillage, alimentation,
élimination urinaire et fécale, transferts, déplacements à l'intérieur, déplacements à
l'extérieur, alerter) and seven *variables illustratives* (gestion, cuisine, ménage,
transports, achats, suivi du traitement, activités du temps libre), each scored A (does it
alone, spontaneously, totally, habitually and correctly), B (alone but not spontaneously
and/or partially and/or not habitually and/or incorrectly) or C (does not do it alone)
[R1]. The six bands [R1] [R3] [R7] [S1 §2.1.2] [S7 defs]:

| GIR | Profile |
|---|---|
| 1 | Confined to bed or chair, mental functions gravely impaired, continuous attendance required; or a person at end of life |
| 2 | Confined to bed or chair with mental functions not wholly impaired, care needed for most everyday activities; or mentally impaired but mobile, requiring permanent supervision |
| 3 | Mental autonomy retained, locomotor autonomy partly retained, help with bodily care several times a day |
| 4 | Cannot transfer alone but moves about indoors once up, needs help washing and dressing; or no locomotor problem but needs help with bodily care and meals |
| 5 | Needs only occasional help with washing, meal preparation and housework |
| 6 | Still autonomous for the essential acts of everyday life |

**(b) AVQ — the insurer-built grids.** Grids of 4 to 6 *actes de la vie quotidienne*
(activities of daily living), built by insurers precisely because AGGIR is applied by
*départements* the insurer does not control — an uncertainty that complicates rating and
reserving [R8 §3.2](#frlib-dependance-r8). The five acts of the GAD common definition are *transfert*,
*déplacement*, *toilette*, *habillage*, *alimentation* [R11] [R12 §1.1.1.1](#frlib-dependance-r12) [S1 §2.1.1];
six-act grids add *continence* [S4] [S5 art. 12] [S6] [S9]. *AIVQ* grids (transport,
telephone, medication, budget) exist in the market but no retrieved contract used them
[R8 §3.2](#frlib-dependance-r8).

**(c) The cognitive overlay.** The *Mini Mental State Examination* (Folstein / MMSE) is
the standard route to psychic dependence. Thresholds observed: **below 15** certified by a
psychiatrist or neurologist [S5 art. 11] [S6 art. 21.1] [S7 defs]; **≤ 10** for AXA's
psychic route to *totale*, **≤ 15** for its mixed route, **< 15** for *partielle*, **< 18**
for its light tier [S1 §2.2]; **≤ 15** and **≤ 10** in the Sogecap tiers [R12 §1.2.1](#frlib-dependance-r12). The
Blessed test also appears [R8 §3.2](#frlib-dependance-r8).

| State | Representative trigger | Basis |
|---|---|---|
| *Dépendance totale* | Definitive need of a third person **and** (≥ 4 of 5 AVQ; or dementia with Folstein ≤ 10 and prompting needed for ≥ 2 of 5 AVQ; or dementia with Folstein ≤ 15 and ≥ 3 of 5 AVQ) | [S1 §2.2]; corroborated [R12 §1.2.1](#frlib-dependance-r12) |
| *Dépendance partielle* | AGGIR group 1, 2 **or 3** **and** (≥ 3 of 5 AVQ; or dementia with Folstein < 15) | [S1 §2.2] |
| Consolidation | The state must be *consolidé* — permanent, irreversible, "non susceptible d'amélioration" — before it is indemnifiable | [S1 §2.2] [S2] [S4] [S6 art. 20] |
| Independence from the public decision | "L'Assureur n'est pas lié par les éventuelles décisions des services publics pour déterminer l'état et le degré de dépendance de l'assuré" | [S5 art. 13] [S6 art. 21.1] |
| Recognition process | Claim form (CNP: *attestation médicale d'état de dépendance*, AMED) completed with the treating doctor, sent under confidential cover to the *médecin-conseil*, who fixes the date the state reached an indemnifiable level; that date cannot precede the date the insurer received the claim; decision within 45 working days of a complete file | [S5 art. 19] [S6 arts. 23–24] |
| Model trigger grid | `trigger_grid = avq5` in the base cell; `avq6` and `aggir` the alternatives | **[std]** (5) |

5. The three grids are alternative *definitions of the same two states*, and the reference
   model has to price all three: the CCSF's 30-contract sample found AGGIR-only and
   AVQ-only about equally frequent, with a significant share combining both [R8 §3.2](#frlib-dependance-r8).
   What no retrieved document states is the **equivalence** between them — and the model
   needs one, because its decrement basis is built from public GIR-graded APA data. Two
   retrieved contracts require **both** grids at once and are the only direct evidence of
   how an insurer equates them: AXA's *partielle* requires AGGIR 1–3 **and** ≥ 3 of 5 AVQ
   [S1 §2.2]; BPCE's requires GIR 3–4 **and** constant third-party help for ≥ 2 of 4 AVQ
   [S3]. Everything else is inference, so the mapping used by `technical-notes.md` is
   **[std]**:

   | Contract state | 5-act AVQ | 6-act AVQ | AGGIR | Direct evidence |
   |---|---|---|---|---|
   | *Dépendance totale* | ≥ 4 of 5 [S1] [R12 §1.2.1](#frlib-dependance-r12) | ≥ 5 of 6 [S4] [S6 art. 21] | GIR 1–2 [S3] [S7 defs] | none equates the three; equivalence **[std]** |
   | *Dépendance partielle* | ≥ 3 of 5 [S1] [R12 §1.2.1](#frlib-dependance-r12) | ≥ 4 of 6 [S4] [S6 art. 21] | GIR 3–4 [S3] [S7 defs] | AXA: GIR 1–3 *and* ≥ 3/5 [S1 §2.2]; BPCE: GIR 3–4 *and* ≥ 2/4 [S3] |

   There is **no observed range** for the equivalence itself, but the direction of the
   residual uncertainty is known: the CCSF records greater variability for *partielle* than
   for *totale*, and *dépendance lourde* variously defined as GIR 1–2, as GIR 1–2–3 subject
   to a cognitive score, as 3 AVQ of 4, as 5 AVQ of 6, or as 3 AVQ of 4 with 2 AIVQ of 4
   [R8 §3.2](#frlib-dependance-r8). A 6-act grid is stricter than a 5-act grid at the same count, and a GIR
   trigger is looser than either because it borrows a public classification the insurer
   would not have made itself.

### Benefit amounts

| Parameter | Representative value | Basis |
|---|---|---|
| *Rente* form | *Rente mensuelle viagère*, paid monthly *à terme échu* (in arrears) while the insured state persists, at the latest until death | [S1 §4.3.1.2] [S5 art. 16] [S6 art. 26] [S7 §4.2.1] [S11] |
| *Rente totale* — chosen range | 500–3,000 €/month; base cell 1,000 | [S1 §1.1.2.2a]; cell pick **[std]** (2) |
| *Rente partielle* | 50% of the chosen total amount | [S1] [S2] [S7] [S8] [R12 §1.2.1](#frlib-dependance-r12); ratio **[std]** (6) |
| *Capital d'équipement* | 3,500 €, optional, paid **once** per membership on first entry into a covered state; the guarantee is extinguished on payment regardless of later deterioration | [S1 §1.1.2.2c, §4.3.2.1] [S2] [S5 art. 17]; amount **[std]** (7) |
| Cessation of the *rente* | On death, or when improvement takes the insured out of a covered state | [S1 §4.3.1.2] [S6 art. 26] [S7 §4.2.1] |
| Mutual exclusivity | Total and partial *rentes* are mutually exclusive; recognition of *totale* never opens partial rights | [S1 §4.3.1.2] |
| Continued entitlement | Annual proof of life and of the persisting state; non-return suspends payment with retroactive settlement on receipt; the insurer may re-examine at any time and stop payment on refusal of medical control | [S1 §4.3.1.2] [S6 arts. 23–24] [S7 §4.2.1] |
| Taxation of the *rente* | Not subject to income tax outside the *loi Madelin* framework | [S1 §1.1.1] [S8] |
| GAD-label minimum *rente* | 500 €/month for *dépendance lourde* | [R11 criterion 4](#frlib-dependance-r11) [R8 §4.3](#frlib-dependance-r8) |

6. Observed partial/total ratios: **50%** at five providers [S1] [S2] [S7] [S8]
   [R12 §1.2.1](#frlib-dependance-r12) and at OCIRP [R13 p19](#frlib-dependance-r13); **60%** at CNP *Ecureuil*, which also offers a
   *légère* tier at 30% [S4]; a **doubling** of the base *rente* at the top rung of the CNP
   Banque de France ladder [S5 arts. 13, 16]. 50% is modal. Observed *rente* ranges:
   500–3,000 [S1] [S10] [R12 §1.2.1](#frlib-dependance-r12); 400–3,000 in steps of 100 [S4]; 300–2,100 [S2];
   200–2,000 [S8]; 300–4,000 "selon les contrats" [S11]; five fixed levels of 158.61 to
   951.66 €/month at rung 3 [S5 annexe 1]; 200 €/month flat in the compulsory group
   variant [S6 annexe 2].
7. Observed *capital* amounts: 3,500 € [S1]; 3,000 € [S2] [S4], with 900 € on the light
   tier deducted from any later payment [S4]; at most 3,200 € on total and 2,400 € on
   partial, net of earlier payments [S3]; up to 5,000 € of adaptation costs reimbursed
   [S8]; 5,000 € or 10,000 €, paid with **no franchise** [S10]; 5,000 € [R12 §1.2.1](#frlib-dependance-r12);
   1,586.10 € to 9,516.60 € by coverage level [S5 annexe 1].

### Waiting period (*délai de carence*) and elimination period (*délai de franchise*)

These are two different things and the reference implementation keeps them apart. The
*carence* (also *délai d'attente*) runs from **inception** and decides whether a state is
covered at all. The *franchise* runs from **recognition** and decides when payment starts
on a state that is covered.

| Parameter | Representative value | Basis |
|---|---|---|
| *Carence* — accident | None | [S1 §1.1.5] [S2] [S3] [S4] [S5 art. 7] [S7 §3.2] [R12 §1.2.1](#frlib-dependance-r12) |
| *Carence* — illness other than neurological or psychiatric | 1 year | [S1 §1.1.5] [S2] [S3] [S4] [S5 art. 7] [R12 §1.2.1](#frlib-dependance-r12) |
| *Carence* — neurological, neurodegenerative or psychiatric illness | 3 years | [S1 §1.1.5] [S2] [S3] [S4] [S5 art. 7] [S7 §3.2] [R12 §1.2.1](#frlib-dependance-r12) |
| Consequence of dependence arising inside the *carence* | No benefit is ever payable for that state **and the membership is terminated**, premiums refunded in full | [S1 §1.1.4.2c] [S3] [S5 art. 7] [S7 §3.2] |
| Extension | AXA extends termination to a dependence-causing condition merely **diagnosed** during the *carence* | [S1 §1.1.4.2c] |
| Restart | Any increase in cover restarts the *carence* on the additional cover | [S1 §1.1.3] [S7 §3.3] |
| Cause mix weighting the three *carences* | accident 10% / other illness 55% / neurological or psychiatric 35% | **[std]** (8) |
| *Franchise* | Absolute, **3 months**; the *rente* starts on the **91st day** after recognition | [S1 §4.3.1.2] [S7 §4.2.1] [S8]; three months / 90 days [S4] [S5 art. 14] [S6 arts. 24, 26] |
| *Franchise* on the *capital d'équipement* | None — paid at recognition | [S10]; composite **[std]** (9) |

8. **No retrieved document states a cause mix.** The three-way split is close to universal
   in *structure* — six of the eight contracts in the research file's table — and France
   Assureurs states the market range as one to three years [R11], the CCSF as nil or very
   short for accident, about one year for illness, up to three years for neurological
   disease [R8 §2.2](#frlib-dependance-r8). What is missing is the *weight* of each cause, which is what a
   projection needs. The 10 / 55 / 35 split has **no observed range**; it carries a large
   neurological share because every retrieved contract puts an MMSE overlay on exactly
   that cause [S1 §2.2] [S5 art. 11] [S6 art. 21.1] [S7 defs] and singles it out for the
   longest *carence*, which is what an insurer does when a cause is both frequent and
   adversely selected. Its sensitivity is reported in `technical-notes.md`.
9. Only Generali states in terms that its *capital d'équipement* is paid with no franchise
   delay [S10]; AXA, Antarius, CNP and Suravenir do not state a *franchise* for the
   *capital* separately from the *rente* [S1] [S2] [S4] [S5] [S7]. Because the *capital*
   is a one-off, the choice moves its timing by three months and nothing else.

### Premiums — the *cotisation viagère révisable*

| Parameter | Representative value | Basis |
|---|---|---|
| Form | Level for the entry age but payable **for life** — there is no premium-paying term | [S1 §1.2.1] [S5 art. 21] [S7 §4.4] |
| Rating factors | Age at entry (*différence de millésimes*), covers and *rente* level chosen, health at entry, the *formule* | [S1 §1.2.1] [S7 §4.4] |
| Payment | In advance; monthly, quarterly, half-yearly or annually; base cell monthly | [S1 §1.2.2] [S2] [S5 art. 21] |
| Base cell premium | 75 €/month at issue, for 1,000 + 500 €/month at entry age 70 | [R8 §2.2](#frlib-dependance-r8) (2013 indicative pricing) |
| *Exonération* on claim | Premiums cease from the premium due date **following recognition of the state**; they become due again if the insured leaves the dependent state | [S1 §1.2.4] [S4] [S5 art. 21] [S6 art. 18] [S7 §4.4] |
| Indexation with the guarantee | The premium rises **in the same proportion** as the *revalorisation* of the guarantees | [S1 §1.2.3] [S5 art. 21] [S7 §3.4] |
| Tariff revision | The scale may be revised for the whole portfolio on legislative, regulatory or fiscal change, on the contract's technical and/or financial results, or "à raison des évolutions constatées ou projetées des statistiques nationales relatives à la dépendance" | [S1 §1.2.3] [S5 art. 22] [S7 §4.4] |
| Protections against revision | No change because of the insured's age or deterioration in health; the member may refuse by cancelling optional covers or resiliating within two months of notification, with a possible *mise en réduction* at the same date | [S1 §1.2.3] |
| Cap on revision | **10% per year**, excluding *revalorisation* | [S7 §4.4] — the only numerical cap in any retrieved document |
| Modeled revision path | 0% in policy years 1–5, then 1.5% per year | **[std]** (10) |
| Couple discount | 10%, permanent; the joining window differs by insurer — **three months** at AXA, lost if either membership is resiliated or reduced [S1 §1.2.6]; **six months** at CNP Banque de France, on the two premiums combined [S5 art. 21]; no window stated at Groupama [S8] | [S1 §1.2.6] [S5 art. 21] [S8]; window and forfeiture from [S1] alone; off in the base cell **[std]** (11) |
| Non-payment | Art. L. 141-3 machinery: registered letter, exclusion 40 days after it is sent | [S1 §1.2.5] [S5 art. 23] [S6] [S7 §4.4] |

10. **A real tariff revision is a management action, not a projected assumption**, and this
    row is a placeholder for one. No retrieved document discloses a revision ever
    exercised, a formula for exercising it, or a projected path; the only sourced
    constraints are the trigger conditions [S1 §1.2.3] [S5 art. 22] [S7 §4.4], the 10%
    annual cap [S7 §4.4] and the prohibition on revising for age or health [S1 §1.2.3].
    The model therefore carries the revision as a **scheduled rate index** — an input
    column by policy year, defaulting to 0 / 0 / 0 / 0 / 0 / 1.5% / 1.5% / … — so the
    capability is present and testable, and it takes a deliberate substitution of that
    column to project a repricing. Setting the column non-zero is a statement about
    insurer behaviour, not about the contract; the 1.5% level is arbitrary inside the
    0–10% band the contract permits. Two retrieved contracts index the premium on something
    else entirely — Sogecap on the growth of the *PASS* [R12 §1.2.1](#frlib-dependance-r12), Suravenir and CNP
    Banque de France on the *revalorisation* of the guarantees [S5 art. 21] [S7 §3.4] — a
    different mechanism, modeled separately below.
11. Real and common [S1 §1.2.6] [S5 art. 21] [S8], but a rating adjustment with no
    cash-flow mechanics beyond scaling the premium, conditional on facts about a second
    life the model point does not carry. A model-point flag, off in the base cell.

### Absence of surrender value; *mise en réduction*

| Parameter | Representative value | Basis |
|---|---|---|
| *Valeur de rachat* | None, at any duration | [S1 §7.3] [S11] |
| Qualifying period | **8 full consecutive years** of premiums | [S1 §1.3] [S2] [S7 §4.6] [R12 §1.2.1](#frlib-dependance-r12) |
| Effect | The membership is maintained with a **reduced *rente***, set by a *barème* whose coefficients depend on the years of premiums already paid | [S1 §1.3] [S2] [S7 §4.6] |
| Scope of the reduced cover | *Dépendance totale* only; the *capital d'équipement* option is lost | [S7 §4.6] [R12 §1.2.1](#frlib-dependance-r12); composite **[std]** (12) |
| *Revalorisation* of the reduced guarantee | None — reduced guarantees are no longer revalued | [S7 §4.6] |
| Assistance | *Prestations d'assistance* end on *mise en réduction* | [S1 §1.3] [S5 art. 24.2] |
| Reduction scale | The published CNP Banque de France *barème de maintien des garanties*, applied from year 8 | [S5 annexe 2]; re-basing **[std]** (13) |
| Disclosure obligation | The contract must state how the *valeur de réduction* is computed | [REG-R31]; disclosure found inadequate [R8 §4.2](#frlib-dependance-r8) |

12. Observed scope: reduced guarantee on *dépendance totale* [S7 §4.6], and the same at
    Sogecap, which also removes the *capital d'équipement* option [R12 §1.2.1](#frlib-dependance-r12); **partial
    maintenance of both the *rente* and the *Capital Premiers Frais*** at AXA [S1 §1.3];
    partial maintenance of the *rente* with *capital* and assistance lost at CNP Banque de
    France [S5 art. 24.2]. The composite takes the majority on both points, against the
    AXA chassis it otherwise follows — a deliberate departure, recorded so it is not
    mistaken for the AXA rule.
13. The **only published French LTC reduction scale** found is CNP Banque de France annexe
    2, in force 1 January 2012, whose qualifying period is **5 years**, not 8
    [S5 annexe 2]:

    | Years of premiums | 5 | 6 | 7 | 8 | 9 | 10 | 15 | 20 | 25 | ≥ 30 |
    |---|---|---|---|---|---|---|---|---|---|---|
    | Coefficient | 16% | 18% | 21% | 25% | 28% | 30% | 40% | 50% | 60% | 70% |

    The full scale is stated for every integer year from 5 to 29, rising at about
    2 percentage points a year from year 10 and capped at 70% [S5 annexe 2]. The composite
    adopts it verbatim but applies it from the **8-year** qualifying period of the
    AXA/Antarius/Suravenir/Sogecap chassis [S1 §1.3] [S2] [S7 §4.6] [R12 §1.2.1](#frlib-dependance-r12), so the
    coefficient at first qualification is **25%** and the rows for 5, 6 and 7 years are
    unreachable. No retrieved 8-year contract publishes its own scale.

### *Revalorisation*

Two distinct indexations exist and both are discretionary in every retrieved contract.

| Parameter | Representative value | Basis |
|---|---|---|
| *Revalorisation des garanties* (guaranteed *rente* and *capital* before claim) | Annual, on the insurer's declaration; the premium rises in the same proportion; modeled at **1.0% per year** | mechanics [S1 §1.2.3] [S5 art. 21] [S7 §3.4]; rate **[std]** (14) |
| *Revalorisation des rentes en service* (the *rente* in payment) | Annual; modeled at **1.5% per year** | mechanics [S1 §4.3.1.3] [S5 art. 15] [S6 art. 16] [S7 §4.2.3]; rate **[std]** (14) |
| Reference index for *rentes en service* | AXA: joint ANPERE/AXA management committee, at the latest 1 April. CNP Banque de France: 1 January, by reference to the rate applied to French civil and military retirement pensions, subject to the *fonds de revalorisation*; the **AGIRC point** if the group contract is resiliated. Suravenir: 1 January, by reference to the annual change in the **AGIRC point value**, within a fund fed by **36% of any surplus** on the result account. CNP MSPP: only by agreement between insurer and subscriber, subject to results | [S1 §4.3.1.3, §8.1] [S5 arts. 15, 25] [S6 art. 16] [S7 §4.2.3] |
| Reduced (paid-up) guarantees | Not revalued | [S7 §4.6] |

14. Neither rate is contractual and neither is published. The mechanics are fully sourced —
    the two indexations exist, they are separately governed, the premium follows the first
    and not the second, and the reduced guarantee follows neither — but every retrieved
    clause makes the *rate* a discretionary decision taken "en fonction des résultats
    techniques et financiers" or by reference to an external pension index whose future
    path is unknown [S1 §4.3.1.3] [S5 art. 15] [S6 art. 16] [S7 §4.2.3]. The CCSF flags
    this as the market's weakest disclosure and warns that a *rente* promised fifteen or
    twenty years ahead can be substantially eroded at 2% average inflation [R8 §3.3](#frlib-dependance-r8). The
    two rates are set **different** on purpose: setting them equal collapses two ledgers
    into one and hides a capability the contract requires. There is **no observed range**.

---

## Contractual mechanics

### The amount payable at recognition

The cleanest statement in any retrieved document is AXA's three-factor formula
[S1 §4.3.1.1]: the amount paid equals the guaranteed amount, times the *revalorisation*
factor accumulated between adhesion and recognition, times — if the membership had been
resiliated after at least eight full consecutive years — the reduction coefficient in force
at recognition. With `G0` the guaranteed *rente totale*, `g_G` the *revalorisation des
garanties* rate, `n` completed policy years at recognition and `c` the reduction
coefficient (1 for a membership still in force):

    rente totale at recognition    = G0 x (1 + g_G)^n x c
    rente partielle at recognition = 0.50 x rente totale at recognition

Thereafter the amount in payment grows at the *revalorisation des rentes en service* rate
`g_S`, a different rate under a different clause [S1 §4.3.1.3] [S5 art. 15] [S7 §4.2.3].
For a reduced membership `c` freezes the guarantee, so `(1 + g_G)^n` stops accruing at the
reduction date [S7 §4.6].

### *Carence*: what it blocks, and what it terminates

The *carence* runs from the effective date of cover and is cause-specific (table above).
Its consequence is **not** simply "no benefit": a state of dependence arising inside the
*carence* for a cause not yet covered **ends the membership**, and the premiums paid are
refunded in full [S1 §1.1.4.2c] [S3] [S5 art. 7] [S7 §3.2]; AXA extends this to a
dependence-causing condition merely *diagnosed* during the *carence* [S1 §1.1.4.2c]. Two
consequences for a projection. First, the *carence* is a decrement with a **cash outflow
attached** — the refunded premiums, which [R12 §3.2.1](#frlib-dependance-r12) prices as a *contre-assurance* term.
Second, the incidence rate is scaled, not switched: inside the three-year window some
causes are covered and others are not, so the model needs a *carence factor* between 0 and
1. [R12 §3.2.1](#frlib-dependance-r12) models exactly this, as coefficients S1 ≤ S2 ≤ S3 applied to incidence over
the first three contract years with S4 = 100%; the composite's cause mix (footnote 8)
produces that shape.

### *Franchise*: when the *rente* starts

Three months, absolute, from recognition: "un délai de franchise absolue de 3 mois, soit à
compter du 91e jour qui suit la date de reconnaissance" [S1 §4.3.1.2]; "à partir du 91e
jour" [S8]; "Le point de départ de la rente est fixé au 91ème jour" [S7 §4.2.1]; three
months at CNP [S4] [S5 art. 14] [S6 art. 24], described as 90 days in the A063 F notice and
IPID [S6 arts. 24, 26]; three months at Sogecap [R12 §1.2.1](#frlib-dependance-r12). Market range 30 to 90 days
[R8 §2.2](#frlib-dependance-r8); France Assureurs states "généralement 90 jours" [R11]; GAD-labelled products
carry `fr = 3` in the pricing formulae [R12 §3.2.1](#frlib-dependance-r12).

Because the *rente* is paid **monthly in arrears** [S1 §4.3.1.2] [S5 art. 16] [S6 art. 26]
[S7 §4.2.1], a three-month *franchise* removes three monthly instalments. The proof that
this is the right reading is Antarius, which carries the same three-month *franchise* but
pays a **first instalment equal to three monthly *rentes*** [S2] — economically neutral
precisely because it restores the three instalments the standard design drops. Two
carve-outs are not in the composite: CNP A063 F pays from the recognition date itself where
the cause is an accident [S6 art. 24], and Generali pays its *capital* with no *franchise*
[S10] (which the composite does adopt, footnote 9). Recognition has its own lead time on
top: the *médecin-conseil* rules within 45 working days of a complete file, and the
recognition date cannot precede the date the insurer received the claim [S6 arts. 23–24].

### Deterioration from *partielle* to *totale*, and the *capital d'équipement*

A new claim file is required; the new amount takes effect **from the first day of the month
following the opening of the right**, and the two *rentes* are mutually exclusive —
recognition of *totale* never opens partial rights [S1 §4.3.1.2]. CNP allows the level to
move in **either** direction on a fresh medical file [S5 art. 13], so improvement out of a
covered state is contractually possible and stops the *rente* [S1 §4.3.1.2] [S6 art. 26]
[S7 §4.2.1]. The actuarial literature retrieved does **not** model this transition:
[R12 §3.1.2](#frlib-dependance-r12) sets it to zero for want of a transition law and prices two separate guarantees
instead. The reference implementation does model it; the consequences are in
`technical-notes.md`.

The *capital d'équipement* is paid **once** and extinguished on payment, so a life that took
it on entering *partielle* takes nothing further on becoming *totale* [S1 §4.3.2.1] [S2]
[S4] [S5 art. 17]; Suravenir instead pays half on *partielle* and the balance on
deterioration [S7 tableau des garanties]. Its trigger sometimes sits **below** the *rente*
trigger: on *dépendance légère* [S1 §4.3.2.1], at severity level 2, two rungs below the
*rente* [S5 art. 17], or on a "Dépendance sensible" [S2]. The composite pays it on first
entry into either covered state and carries no light tier.

### Premium *exonération*, non-payment, and *mise en réduction*

Premiums cease from the premium due date following recognition of the state [S1 §1.2.4]
[S4] [S5 art. 21] [S6 art. 18], and become due again if the insured leaves the dependent
state [S7 §4.4]. Note the boundary: *exonération* runs from **recognition**, not from the
start of *rente* payment, so the three months of the *franchise* are **not** premium-paying
months. On non-payment art. L. 141-3 applies — registered letter, exclusion 40 days after it
is sent [S1 §1.2.5] [S5 art. 23] [S6] [S7 §4.4]. Before the qualifying period the excluded
membership ends with no value [S1 §7.3]; from eight full consecutive years of premiums it
becomes a *mise en réduction* and the membership is maintained with a reduced *rente*
[S1 §1.3] [S2] [S5 art. 24.2] [S7 §4.6] [R12 §1.2.1](#frlib-dependance-r12):

    reduced rente totale = G0 x (1 + g_G)^n x c(n)

with `c(n)` the *barème* coefficient (footnote 13). Suravenir is explicit that the reduced
guarantee is **no longer revalued**, that any value quoted at the reduction date is
indicative only, and that the definitive reduced *rente* is computed at the claim date on
the bases then in force [S7 §4.6]; AXA likewise lets the joint committee adjust the reduced
amounts, while no claim has occurred, in the light of the contract's technical and financial
balance [S1 §1.3]. Assistance ends [S1 §1.3] [S5 art. 24.2]. The GAD label requires
"des conditions de maintien des droits en cas d'interruption de paiement des cotisations"
as one of its nine criteria [R11 criterion 9](#frlib-dependance-r11) [R8 §4.3](#frlib-dependance-r8).

### *Revalorisation* of the guarantee and of the *rente* in service

Before a claim the guaranteed amounts grow at the declared *revalorisation des garanties*
rate and the premium rises in the same proportion [S1 §1.2.3] [S5 art. 21] [S7 §3.4]. In
payment the *rente* grows at a separately declared rate, on a calendar date (1 January at
CNP and Suravenir, at the latest 1 April at AXA) applied to **all** *rentes en service*
regardless of how long each has been in payment [S1 §4.3.1.3] [S5 art. 15] [S7 §4.2.3].

---

## Riders and options

**In scope (modeled):**

- ***Formule* Dépendance Totale et Partielle** — the partial tier at 50% of the chosen
  *rente*, on in the base cell [S1] [S2] [S7] [S8] [R12 §1.2.1](#frlib-dependance-r12); the total-only *formule*
  is the alternative model-point value [S1] [S7 *Contrat Essentiel*].
- ***Capital d'équipement*** (AXA: *Capital Premiers Frais*) — 3,500 €, paid once, on in
  the base cell [S1 §1.1.2.2c].
- **Premium *exonération* on claim** — zero premium income from lives in a recognised
  state [S1 §1.2.4] [S4] [S5 art. 21] [S6 art. 18].
- ***Mise en réduction*** — a paid-up state carrying a reduced *rente totale*, entered on
  lapse from eight years [S1 §1.3] [S2] [S7 §4.6] [R12 §1.2.1](#frlib-dependance-r12).

**Out of scope (listed for completeness; no charges or benefits projected):** the
*dépendance légère* tier and its 900 € *capital* [S1 §2.2] [S4]; Antarius's "Dépendance
sensible" *capital* trigger [S2]; the optional *Capital décès* and *Capital décès
remboursement des cotisations*, which end at the end of the insurance year in which the
insured turns 85 [S1 §1.1.4.1, §1.1.5] and are branch-20 business [S1 §1.1.1]; Generali's
death option requiring death before 85 [S10]; the *Garantie Fracture* paying 300 € [S4];
the *prestations d'assistance* themselves — 24/7 line, teleassistance, meal and medicine
delivery, home help, sitting and respite services, memory assessment and training, an
ergotherapist's home-adaptation assessment, help finding an establishment, legal and social
support [R8 annexe 2](#frlib-dependance-r8) [S1 ch. 3–5] [S8] [S10] [R13 p24](#frlib-dependance-r13), which are a *prestation en nature*
subject to an obligation of means, not of result [S1 §7.2.2], and are carried only as an
expense line; the *loi Madelin* framework, which makes premiums deductible and the *rente*
taxable [S1 §1.1.1]; the 10% couple discount [S1 §1.2.6] [S5 art. 21] [S8]; increases and
decreases in cover [S1 §1.1.3] [S7 §3.3] [R12 §1.2.1](#frlib-dependance-r12); and the exclusion set — intentional
acts and attempted suicide, narcotics and non-prescribed medicines, blood alcohol above the
criminal threshold and the complications of chronic alcohol abuse, war, riot and terrorism
where the insured takes an active part, nuclear transmutation, motorised competitions,
unapproved air sports [S1 §7.1] [S3] [S4] [S6 art. 22] [S7 §3.5], with BPCE's
disease-specific exclusions of fibromyalgia, chronic fatigue syndrome, Ehlers-Danlos and
fasciitis [S3].

---

## Variations across insurers

1. **Trigger grid.** Purely AVQ: AXA on 5 acts with a Folstein overlay [S1 §2.2], CNP
   *Ecureuil* [S4] and CNP MSPP [S6 art. 21] on 6 acts, Sogecap on 5 acts [R12 §1.2.1](#frlib-dependance-r12).
   Purely AGGIR: BPCE, GIR 1–2 for *totale* and GIR 3–4 plus 2 of 4 AVQ for *partielle*
   [S3]; Suravenir, "L'état de dépendance est évalué selon la grille de référence AGGIR du
   décret 97-427 du 28 avril 1997", GIR 1–2 and GIR 3–4, with MMSE below 15 for
   neuro-degenerative conditions [S7 defs]. Mixed: AXA requires AGGIR 1–3 *and* an AVQ
   count for *partielle* only, AGGIR playing no part in its *totale* definition [S1 §2.2].
   Groupama documents AGGIR with a four-rung 6-act ladder as "un complément ou une
   alternative" without publishing the contractual trigger [S8] [S9]. Representative: the
   AXA 5-act definitions, with `trigger_grid` a model-point column.
2. **Partial/total ratio.** 50% at five providers [S1] [S2] [S7] [S8] [R12 §1.2.1](#frlib-dependance-r12); 60% at
   CNP *Ecureuil*, which adds a 30% light tier [S4]; the CNP Banque de France ladder
   monetises severity differently, paying nothing at 2 or 3 AVQ of 6 except the equipment
   *capital*, the base *rente* at 4 of 6 and **double** it at 5 or 6 of 6, across five
   subscribed coverage levels [S5 arts. 13, 16, 17, annexe 1]. Representative: 50%.
3. **Reduction.** Qualifying period eight full years [S1 §1.3] [S2] [S7 §4.6]
   [R12 §1.2.1](#frlib-dependance-r12), **five** at CNP Banque de France, the only contract publishing its scale
   [S5 arts. 23–24.2, annexe 2]; the two IPIDs state nothing [S3] [S4]. What survives
   differs too: *rente* and *capital* both partially maintained [S1 §1.3]; *rente* only,
   *capital* and assistance lost [S5 art. 24.2]; *rente* on *totale* only [S7 §4.6], with
   the *capital* option removed as well [R12 §1.2.1](#frlib-dependance-r12).
4. **Cap on tariff revision.** Only Suravenir states one — 10% per year excluding
   *revalorisation*, the member then free to ask for a reduction of the guaranteed *rente*
   or resiliate on one month's notice [S7 §4.4]. AXA, CNP and Sogecap state the right with
   no numerical cap [S1 §1.2.3] [S5 art. 22] [R12 §1.2.1](#frlib-dependance-r12).
5. **Indexation.** For the *rente* in service: joint-committee decision by 1 April
   [S1 §4.3.1.3]; the rate applied to French civil and military retirement pensions, and
   the **AGIRC point** on resiliation of the group contract [S5 arts. 15, 25]; the AGIRC
   point in a fund fed by 36% of surplus [S7 §4.2.3]; agreement between insurer and
   subscriber subject to results [S6 art. 16]; the contract's technical and financial
   results [R12 §1.2.1](#frlib-dependance-r12). For the premium: in the same proportion as the guarantees
   [S5 art. 21] [S7 §3.4], or on the growth of the *PASS* [R12 §1.2.1](#frlib-dependance-r12).
6. **Structural outliers.** (a) The **severity-ladder** design: CNP's Banque de France
   contract 0658 Q, four rungs on 6 AVQ (2/6, 3/6, 4/6, 5-or-6/6), the *rente* starting at
   rung 3 and doubling at rung 4, plus a **placement condition** — residence in a *section
   de cure médicale* or an establishment for the elderly, long-stay hospitalisation, or the
   combination of home nursing care and third-person assistance [S5 arts. 12, 13, 16, 17].
   The same ladder is what Groupama documents [S9]. (b) The **points-based collective**
   design: OCIRP, where contributions of 0.40%–1.50% of the *PMSS* buy *points de rente
   dépendance* at an age-dependent or mutualised *valeur d'acquisition* and the *rente*
   equals points × *valeur de service*; the guaranteed minimum is 200–750 €/month for
   GIR 1–2 and half of it for GIR 3; recognition is **automatic on receipt of APA at
   GIR 1–2**, otherwise requiring a state lasting more than three months and inability to
   perform 2 or 3 of 4 everyday acts; there is **no reduction value at all**; and the final
   *rente* is unknown at inception [R13 pp. 17–21, 31](#frlib-dependance-r13) [REG-R28]. Neither is the
   representative chassis: a severity-ladder model needs a rung index in place of a
   two-state machine, and a points model needs an accumulation account and a *valeur de
   service* the insurer sets each year.
7. **Compulsory group cover, for scale.** CNP MSPP A063 F pays 200 €/month on *totale* and
   100 €/month on *partielle* for **20.40 €/year (1.70 €/month)** per insured person
   [S6 annexe 2] — an order of magnitude below individual pricing, which is the
   mutualisation effect the CCSF's 2024 recommendation argues for [R9 §1](#frlib-dependance-r9).

---
## Regulatory context

**Contract law and classification.** Cover sits in branches 1 and 2 of art. R. 321-1 of the
Code des assurances [S1 §1.1.1] [S3] [S6 art. 1.1]; the group-contract machinery of arts.
L. 141-1 ff. governs the *notice d'information*, the member's rights and the non-payment
procedure of art. L. 141-3 [S1 §1.1.1, §1.2.5] [S5 art. 23]. Art. A. 132-4 and its annexe
prescribe what a *note d'information* must disclose — the guarantees, the premium
arrangements, the *délai et modalités de renonciation*, the claims procedure, and reduction,
surrender and transfer values — and art. A. 132-8 the one-page *encadré* [REG-R30]. Art.
L. 132-21 requires the contract to state how the *valeur de réduction* is computed
[REG-R31], the statutory hook under the *mise en réduction* clauses above. There is **no
LTC-specific regime**: LTC is best read as a non-life risk carrying a lifelong guarantee,
the branch *agrément* is at the insurer's discretion, and [R12] reads the *participation aux
bénéfices* obligation as not applying because the risk covered is not human life
[R12 §1.1.2.2](#frlib-dependance-r12). **That proposition rests on the dissertation alone.** Art. L. 331-3
imposes the obligation in general terms and carves out no category on its face; the reference
entry for it records case law and parliamentary answers holding that none is carved out
*a priori*, and warns that the served version ends 1 January 2016, so it is cited here for the
substance of the obligation and no current article number is asserted [REG-R14]. Nothing in
this library's cash flows turns on the point — no *participation aux bénéfices* is projected
on this product either way. Mis-statement falls under arts. L. 113-8 (intentional —
nullity, premiums retained) and L. 113-9 (non-intentional — proportional reduction, or
resiliation after ten days) [S1 §1.1.2.2] [S7 §2.4].

**Prudential.** Under Solvabilité II technical provisions are a best estimate — the
probability-weighted average of future cash flows discounted at the relevant risk-free term
structure — plus a risk margin, in a three-pillar regime transposed into the Code des
assurances rather than applied directly [REG-R4] [REG-R1] [REG-R2]. EIOPA publishes the
risk-free term structures monthly [REG-R5]; this library produces undiscounted cash flows
and stops short of the discounting. LTC sits in the **Health-SLT** underwriting module
[R12 §1.1.2.1](#frlib-dependance-r12). On the French statutory balance sheet art. R. 343-3 enumerates the eleven
technical provisions, item 1 being the *provision mathématique*, computed *including future
management costs* [REG-R6]. This product generates two: the **provision pour risques
croissants** for autonomous insureds (present value of future commitments less present value
of future premiums, allowing for the waiting-period incidence reduction and for the
counter-insurance of refunded premiums) and the **provision mathématique des rentes** for
*rentes* in payment [R12 §3.2.2](#frlib-dependance-r12). **The code article governing the PRC was not retrieved**
— the *partie législative* table of contents was retrieved and the code identity and version
confirmed [R18], but the *partie réglementaire* is not exposed on that page — so everything
said about the PRC rests on [R12], an actuarial dissertation, not on the code. Reinsurance
is usually quota-share; the Sogecap product cedes 70% [R12 §1.2.1](#frlib-dependance-r12).

**Mortality tables.** A French tariff must use a *taux d'intérêt technique* fixed under
art. A. 132-1 and one of exactly two permitted kinds of mortality table: homologated tables
by sex, or the undertaking's own tables certified by an independent actuary approved by a
recognised actuarial association [REG-R23]. For a *rente viagère* the homologated tables are
the generational **TGH05 / TGF05** [REG-R21]; for everything that is not an annuity,
**TH 00-02 / TF 00-02** [REG-R22]. Neither family is reproduced here — they are cited by
name and arrêté, and the decrement CSV shipped for this product is a **[std]** proxy that
takes no value from any retrieved source: a two-parameter Gompertz force fixed entirely by
the two unsourced anchors `mort_rate(60) = 0.00400` and `mort_rate(90) = 0.10500`
(`technical-notes.md` (c)), shaped like a French female population table. INSEE publishes the
only freely redistributable French mortality series and is what a production implementation
would fit here [REG-R24]; this one does not read it, and the shipped `provenance` column says
so on every row. The technical-rate ceiling for a contract with
periodic premiums is the lower of 3.5% and 60% of the semi-annual average rate of French
State borrowings [REG-R17]; no technical rate is disclosed in any retrieved product
document.

**The public benefit this *rente* tops up.** The APA is paid to people aged 60 or over
classified in GIR 1 to 4 [R2 arts. R. 232-1, R. 232-4](#frlib-dependance-r2) [R3]. Assessment is by the
*département*'s *équipe médico-sociale APA* during a home visit, and the *plan d'aide* states
the GIR, the aids financed and the beneficiary's participation rate; GIR 5–6 are redirected
to pension-fund assistance [R5]. At home the GIR is set by a departmental professional, in
an establishment by the establishment's physician, usually within a month of admission [R6]
— so the same insured can be re-graded by a different assessor on entering an EHPAD.
Monthly *plan d'aide* ceilings from 1 January 2026: GIR 1 **2,080.33 €**, GIR 2
**1,682.30 €**, GIR 3 **1,215.99 €**, GIR 4 **811.52 €**, the beneficiary contributing
nothing up to a monthly income of 933.89 €, between 0% and 90% up to 3,439.31 €, and 90%
above [R4]; the 2024 ceilings were 1,955.60 / 1,581.44 / 1,143.09 / 762.87 € [REG-R26].
Against those, the *reste à charge* in an EHPAD was about **1,957 €/month** per a DREES
study of July 2022, roughly 120% of the average gross pension [R9 §2](#frlib-dependance-r9) — the gap a
1,000 €/month private *rente* is sold to close.

**Consumer protection and the label.** The **GAD ASSURANCE DÉPENDANCE®** label sets nine
criteria, published verbatim by France Assureurs [R11] and reproduced by the CCSF [R8 §4.3](#frlib-dependance-r8)
— among them a minimum *rente* of 500 €/month for *dépendance lourde*, a common definition
of *dépendance lourde* on the five *actes élémentaires*, and conditions for maintaining
rights on interruption of premium payment. GAD-labelled contracts covered 194,900 people at
end 2024 at an average annual premium of 584 €, 14% of insureds on
sole-and-principal-guarantee contracts but 38% of new business in that category [R10 §2.3](#frlib-dependance-r10).
**The label's rule book was not retrieved**, and whether any contract cited here carries the
label is [unverified] — no retrieved *notice* claims it; the label's prohibition on medical
selection before age 50 [R8 §4.3 point 6](#frlib-dependance-r8) [R11] is likewise [unverified] as applied to any
contract above. The CCSF's January 2024 recommendation would replace the individual market
with a compulsory *Contrat Dépendance Solidaire* covering GIR 1–2 only, with a single
lifelong tariff grid, **no waiting period**, a reduction mechanism for interrupted payment,
portability through a single insurance pool, and automatic payment on receipt of APA at
GIR 1 or 2 [R9 §I.C](#frlib-dependance-r9) — a recommendation, not law: **nothing here should be read as saying
that a compulsory French LTC contract exists**.

**A supervisory gap this library cannot close.** No ACPR material on *assurance dépendance*
could be retrieved: the ACPR news page on the lessons of its LTC supervisory inspections and
the September 2023 *Revue de l'ACPR* article both return HTTP 403, as does the DGCCRF
consumer *fiche pratique*, and the ACPR host returns an HTML error page rather than the PDF
even to a request carrying a browser User-Agent. Those three references are **omitted from
`sources.md`** rather than cited, and nothing here rests on them. The supervisor's own view
of pricing adequacy, provisioning practice and claims handling on this product is missing
from this library.

**Standards and accounting.** Institut des actuaires NPA 2, *Modèles actuariels*, is a
category-3 *pratique recommandée* adopted 15 June 2015 with effect from 1 January 2016,
applying "à tout modèle actuariel, qu'il soit basé sur des logiciels externes ou des
développements internes", read under a principle of proportionality and covering pricing and
the technical studies attached to new products [REG-R44] — the standard against which a
published model documentation, worked example and test suite are judged. IFRS 17, effective
for annual reporting periods beginning on or after 1 January 2023, measures a group of
contracts as risk-adjusted fulfilment cash flows plus a contractual service margin
[REG-R45]; French listed insurers report on that basis, with no French carve-out.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-dependance-r1
[R11]: #frlib-dependance-r11
[R12]: #frlib-dependance-r12
[R14]: #frlib-dependance-r14
[R18]: #frlib-dependance-r18
[R3]: #frlib-dependance-r3
[R4]: #frlib-dependance-r4
[R5]: #frlib-dependance-r5
[R6]: #frlib-dependance-r6
[R7]: #frlib-dependance-r7
[REG-R1]: #frlib-reg-r1
[REG-R14]: #frlib-reg-r14
[REG-R17]: #frlib-reg-r17
[REG-R2]: #frlib-reg-r2
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R26]: #frlib-reg-r26
[REG-R28]: #frlib-reg-r28
[REG-R30]: #frlib-reg-r30
[REG-R31]: #frlib-reg-r31
[REG-R4]: #frlib-reg-r4
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
