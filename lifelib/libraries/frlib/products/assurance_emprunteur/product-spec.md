# Product Specification

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of French *assurance emprunteur* (ADE) — the death,
disability and incapacity cover attached to a *crédit immobilier*. It does not describe
any single insurer's product. Facts carrying a source tag — [S#] (primary product
documents: *notice d'information*, *conditions générales*, IPID/DIPA, brochures) and
[R#] (regulatory/actuarial references), both numbered per
`_research/assurance-emprunteur.md` — resolve against `sources.md` in this directory
(numbering carried over verbatim; never renumbered). [REG-R#] tags resolve against the
cross-product reference library `references/regulatory-and-actuarial-references.md`
(its own frozen R1–R49 numbering). Values marked **[std]** are standardizations
introduced for the reference implementation; each [std] table row carries a footnote
giving the rationale and, where the research file recorded one, the observed range
across insurers. Facts the research file could not verify are flagged [unverified].
French terms of art are kept in French and glossed on first use.

---

## Product overview and market role

*Assurance emprunteur* is the largest individual protection market in France and the most
mechanically intricate product in this library. It pays the lender the *capital restant dû*
(CRD — outstanding principal) on the borrower's death, and the monthly loan *échéance*
(instalment) while the borrower is unable to work; the beneficiary is normally the lender,
up to the sums still owed. Three market regimes coexist and the regulator measures them
separately. At 31 May 2023
the insured mortgage portfolios split **72.2 % *contrat groupe bancaire*** (the lender's
own group policy, joined by adhesion), **4.4 % *contrat alternatif bancaire***,
**16.0 % *contrat alternatif externe*** (*délégation d'assurance* — an individual or
association contract from an insurer unconnected to the lender), with **7.4 %** of
portfolios carrying no insurance at all [R12]. The sampled corpus covers two bank group
policies [S10] [S13], four alternative external contracts [S1] [S2] [S5] [S9] [S11], and
one individual term-life policy used as mortgage cover [S12]. The usual wrapper is a
*contrat d'assurance de groupe à adhésion facultative* under arts. L. 141-1 ff. of the
Code des assurances with an association or the bank as *souscripteur*
[S1] [S9] [S10] [S11] [S13]; one sampled policy is written across **branches 1, 2 and 20**
of art. R. 321-1 — accident, sickness and life-death [S13], the exact regulatory signature
of a combined death-plus-incapacity borrower cover. Coinsurance [S13] and delegated
management [S1] [S9] [S11] are both normal.

Market size, on the only public measures retrieved: **€11.8 bn of premiums in 2023**,
**85 % (€9 987 m)** on bank group contracts and **15 % (€1 824 m)** on *délégation
d'assurance*; by loan type **67 % mortgage, 25 % consumer, 9 % professional**; by guarantee
**69 % death, 30 % incapacité-invalidité, 2 % unemployment** [REG-R37]. A much narrower cut
— the death guarantee only, of individually-underwritten contracts written by Code des
assurances undertakings — shows **5 223 thousand contracts at end-2024, €979 m of premiums
and €330 m of benefits**, which is not a market total [R18]. Whole-market figures in
secondary coverage of the CCSF's 2024/2025 work are **[unverified]**: the December 2023
*Bilan de l'assurance emprunteur* to Parliament could not be retrieved [R13].

The **loi Lemoine** (loi n° 2022-270 du 28 février 2022) rewrote the product's behavioural
economics: the borrower may cancel *à tout moment* from signature of the loan offer (art. 1)
[R1] [R3] [REG-R35], and no health questionnaire may be required where the insured share of
the cumulative credit outstanding is ≤ €200 000 and the loan matures before the borrower's
60th birthday (art. 10) [R1] [R2]. Substitution requests received by banking networks rose
from **99 265 in H1 2021 to 181 600 in H1 2023**, more than 80 % [R12].

The representative design specified below is a **group contract paying the CRD on Décès
and PTIA and the *échéance* on ITT and IPT, with a 90-day *franchise*, a 1 095-day ITT
limit followed by an IPT assessment at a 66 % combined invalidity threshold, cover ending
at 70 for the incapacity guarantees and at 85 for death, a per-head *quotité* of at most
100 %, and a level premium expressed as an annual rate on the *capital initial* ×
*quotité*** — essentially the 2025 CNP group notice [S9] with the explicitly *nivelé*
(levelled) rate design of one bank policy [S13]. Every other retrieved contract is a
parameterisation of that skeleton. Three switches are configuration, not chassis, and are
carried as model point columns: the **IPT benefit base** (CRD versus *échéances*)
[S3] [S7] [S9]; the **indemnity basis** (*forfaitaire* versus *indemnitaire*) [S10] [S6];
and the **premium base** (*capital initial* versus *capital restant dû*) [S8] [S10].

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Group borrower policy, *adhésion facultative*, arts. L. 141-1 ff. C. ass.; lender beneficiary up to the sums owed | [S1] [S9] [S10] [S11] [S13] |
| Market regime | *Contrat groupe bancaire* chassis, alternative-contract wording | 72.2 % of portfolios [R12]; wording [S9] |
| Regulatory branches | 1 (accident), 2 (maladie) and 20 (vie-décès) of art. R. 321-1 C. ass. | [S13] |
| Guarantee set | Décès + PTIA + ITT + IPT; IPP and *perte d'emploi* optional | [S1] [S9] [S10]; IPP optional [S5] [S9] [S10] |
| Insurable loan | Euro-denominated only; amortising, *in fine* (to 10 years) or *relais* (to 3 years) | [S9]; loan-type grid [S10] |
| Loan modelled here | Amortising, fixed nominal rate, principal residence | **[std]** (1) |
| Loan term band | 1–35 years, extendable by 5 without exceeding 40 | [S1] [S3]; 35 years [S9] |
| Entry ages | 18 to before the 65th birthday for the full guarantee set | [S1] [S13]; to 64 [S6] |
| Quotité granularity | 1 % steps from 1 % to 100 % per insured | [S9]; ≤100 % per head [S1] [S5] [S11] |
| Maximum insured *encours* | €5 000 000 per insured | [S9]; also [S12] |
| Medical formalities | None where the insured share of the cumulative credit *encours* ≤ €200 000 **and** repayment falls before the 60th birthday; otherwise a health questionnaire valid 6 months | [R2] [R1] art. 10 [S9] |
| Renonciation | 30 calendar days | [S7] [S10] [S12] |
| Base model cell | Male, entry age 52, loan €200 000 at 3.00 % nominal over 240 months, *quotité* 100 %, *franchise* 90 days, level premium 0.84 %/yr of *capital initial* | **[std]** (1) |

Footnotes to [std] rows:

1. Pure modeling cell, chosen so that every distinctive mechanic bites. Entry age 52 with
   a 20-year loan means the loan matures at attained age 72 while the ITT, IPT and PTIA
   guarantees end at 70 — the last **24 months** of the loan carry death cover only, and
   the *nivelé* premium does not fall [S13]. It also means repayment falls **after** the
   60th birthday, so the loi Lemoine questionnaire waiver does **not** apply [R2] —
   which is the normal case: 58.5 % of borrowers had an insured amount below €200 000 but
   only 23 % of those contracts were eligible for the waiver, because lengthening loan
   terms push the repayment date past the 60th birthday [R12]. €200 000 insured at
   *quotité* 100 % sits exactly on the statutory ceiling [R2], which makes the
   interaction explicit. No retrieved document publishes a standard-risk rate card, so the
   loan amount, term and rate are modeling picks. **Fixed rate** and **principal residence**
   are modeling narrowings too, not eligibility conditions: [S9] restricts the loan only to
   euro denomination and to the amortising / *in fine* / *relais* forms, and its *garantie
   aide à la famille* expressly contemplates a mortgage on a principal, a secondary **or**
   a rental residence, while [S10]'s loan-type grid carries a rental-investor column. The
   model wants one level *échéance*, which a fixed nominal rate gives it; residence type it
   does not use at all.

### The loan and the capital restant dû

| Parameter | Representative value | Basis |
|---|---|---|
| *Capital initial* | €200 000 — the amount borrowed at the credit contract's inception | definition [S9]; amount **[std]** (1) |
| Loan nominal annual rate | 3.00 %, monthly rate = nominal ÷ 12 | **[std]** (2) |
| Loan term | 240 months (20 years) | **[std]** (1); band [S1] [S3] [S9] |
| *Échéance* | €1 109.20 per month, level, capital and interest | **[std]** (3) |
| *Capital restant dû* | The share of the borrowed capital still owed at a given date, read off the *échéancier* | [S9]; equivalent lexique [S1] |
| *Capital assuré* | *capital initial* × *quotité* | [S9] |
| Amortisation-schedule anti-gaming | An instalment increase at the borrower's initiative in the 90 days before a claim is disregarded; a decrease applies immediately | [S9]; 180 days [S10]; 12 months [S1] |

2. French loan documents quote a *taux nominal annuel* and the monthly rate is the
   nominal rate divided by twelve; the resulting annual effective rate is
   (1 + 0.03/12)^12 − 1 = 3.0416 %. No retrieved source states a loan rate — the sampled
   documents are insurance notices, not credit offers — so the rate is a modeling pick.
   The convention (nominal ÷ 12 rather than an effective-rate conversion) is a
   standardization; it is what makes the *échéance* below reproducible.
3. Derived, not assumed: *échéance* = *capital initial* × i / (1 − (1 + i)^(−n)) with
   i = 0.0025 and n = 240, giving €1 109.1952. The reference implementation **computes**
   the CRD schedule from these three inputs and never reads it from a table; every
   sampled contract instead reads the CRD off the lender's *échéancier* [S1] [S5] [S9].

### The guarantee set

| Guarantee | Trigger | Benefit | Cover ends at | Basis |
|---|---|---|---|---|
| **Décès** | Death from any cause (suicide excluded in year 1) | CRD × *quotité*, extinguishing all cover for that insured | 85 | benefit [S1] [S5] [S9] [S10] [S11]; age 85 [S9] [S11]; accrued interest added [S9] [S11] |
| **PTIA** — *perte totale et irréversible d'autonomie* | Definitive inability to engage in **any** remunerated occupation **and** permanent need of a third person for the ordinary acts of daily life | CRD × *quotité*, as an acceleration of Décès — never both | 70 | [S5] [S9] [S11]; 3-of-4 acts [S1] vs 4-of-4 [S5] [S9] |
| **ITT** — *incapacité temporaire totale de travail* | Temporary and complete inability, after illness or accident, to carry on **his or her own** occupation, after the *franchise* | *échéance* × *quotité* per month, for at most 1 095 days per claim | 70 | benefit [S1] [S9] [S11]; 1 095 days [S1] [S11] [S12]; age 70 [S9] |
| **IPT** — *invalidité permanente totale* | Combined invalidity rate ≥ 66 % at consolidation, on the *barème croisé* | *échéance* × *quotité* per month to the end of the loan or the age limit | 70 | ≥66 % [S1] [S5] [S9] [S10] [S11] [S12]; instalment form [S5] [S9] [S11] |
| **IPP** — *invalidité permanente partielle* (option, not modeled) | Combined rate 33 % to below 66 % | 50 % of the ITT benefit — or (N − 33)/33 × the benefit at other insurers | 70 | flat 50 % [S5] [S9] [S10]; ramp [S1] [S11]; band [S1] [S9] [S10] [S11] |
| **Mi-temps thérapeutique** (not modeled) | Medically prescribed part-time return to work | 50 % of the benefit for at most 180 days — 6 months at the insurers that say so instead | 70 | 180 days [S1] [S10] [S11] [S12]; 6 months [S5] [S7] [S9]; age 70 [S9] |
| **Perte d'emploi** (option, not modeled) | Redundancy giving entitlement to unemployment benefit | 50 % of the insured instalments, capped €2 500/month, for up to 18 months after a 180-day *carence* and a 90-day *franchise* | 61 at adhesion | [S1] [S3]; a second module pays from the 91st day, capped €3 500/month, 12 months per redundancy [S8] |
| **Garantie aide à la famille** (not modeled) | Insured stops work to care for a seriously ill child, drawing the AJPP | 50 % of the ITT benefit, capped €4 000/month, at most 28 months | 67 | [S9]; market undertaking from July 2025 [R12] |

### ITT and IPT claim mechanics

| Parameter | Representative value | Basis |
|---|---|---|
| *Franchise* (deductible days) | 90 continuous days | **[std]** (4); menu 30/60/90/120/180 [S9] |
| Maximum ITT indemnification | 1 095 days (three years) per claim | [S1] [S11] [S12]; **[std]** as a universal rule (5) |
| ITT benefit | 100 % of the *échéance* (capital and interest) read from the amortisation schedule at the claim date, × *quotité* | [S1] [S9] [S11] |
| Pro-rating | Whole instalments; no *prorata temporis* | [S13]; daily pro-rating at 1/30 elsewhere [S1] |
| Relapse | No new *franchise* where the interruption ran under 90 days | [S9] [S10]; 60 days [S1] [S12]; 2 months [S5] |
| IPT threshold | Combined rate ≥ 66 %, fixed at consolidation and at the latest three years after the start of the ITT | ≥66 % [S1] [S5] [S9] [S10] [S11] [S12]; three-year rule [S10] |
| *Barème croisé* | Double-entry grid crossing a *taux d'incapacité fonctionnelle* with a *taux d'incapacité professionnelle*; for an insured with no occupation only the functional rate is used | [S1] [S5] [S9] [S10] [S11]; non-working rule [S9] [S10] [S11] |
| Combined-rate formula | N = (IF² × IP)^(1/3) | **[std]** (6) |
| Indemnity basis | *Forfaitaire* — the insured instalment is paid whatever the employer or the compulsory scheme pays | [S1] [S3] [S6] [S11]; *indemnitaire* alternative [S10] |
| Monthly benefit cap | €10 000 per month per insured across all loans | [S1]; €25 000 [S6] [S7] |
| Claim notification | ITT file within 90 days of the end of the *franchise* | [S9]; 6 months [S1]; 30 days [S12] |
| Independence from social security | The contract's invalidity notion is independent of the social-security notion | [S1]; mandatory FSI statement since 1 June 2022 [R10]; contrary design [S13] |

4. Observed *franchise* menus: 30/60/90/180 [S1] [S2]; 30/60/90/120/180 [S9]; benefit
   from the 31st/61st/91st/181st day [S5]; 30/60/90/180 with 90/180 restricted to the
   non-working and to DROM/EU/EEA/UK residents [S6] [S7]; 90 standard with 30 as a priced
   option [S10]; 90 or 180 only [S13]; a single fixed 90 [S11]; 15/30/60/90/180 [S12].
   The CCSF criteria list offers lenders the boxes ≤30 / ≤60 / ≤90 / ≤120 / ≤180 days
   [R11]. 90 days is the modal standard and the only value present in every menu.
5. The 1 095-day cap is explicit at three sampled insurers [S1] [S2] [S11] [S12], but is
   **not universal**: two others end ITT at consolidation with no stated day cap
   [S5] [S9], and a third fixes consolidation "au plus tard trois ans après le début de
   son Incapacité Temporaire Totale" [S10] — which reaches the same three years from the
   other side. The composite adopts 1 095 days as a hard cap and treats consolidation as
   occurring there; a model that hard-codes it for every carrier would misstate the
   consolidation-based wordings.
6. **A fitted reconstruction, not a quotation.** N = (IF² × IP)^(1/3) reproduces every
   printed cell of both retrieved *barème croisé* grids [S1] [S9] and both of their worked
   examples (IF 40 %, IP 80 % → 50.40 % [S1]; IF 50 %, IP 40 % → 46 % [S9]), but neither
   contract states it. Where an exact match matters, ship the published grid rather than
   the formula.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium base | Annual rate applied to the *capital initial* × *quotité*, level for the whole term | [S9] [S11] [S13]; alternative CRD base [S2] [S7] [S8] [S10] |
| Representative rate | 0.84 % per year of *capital initial* | **[std]** (7) |
| Monthly premium | €140.00, payable monthly in advance | **[std]** (7); frequency [S1] [S9] [S11] [S12] |
| Levelling | The rate is *nivelé* over the loan term, so the cessation of the PTIA/ITT/IPT guarantees at the age limit does **not** reduce the premium | [S13] |
| Tariff drivers | Age at adhesion, loan term, loan type, guarantees and options including the chosen *franchise*; elsewhere also occupation, smoker status and declared medical and sporting risks | [S9]; wider list [S1] [S11]; unisex tariff at one insurer [S3] |
| Premium guarantee | Net-of-tax premium guaranteed for the whole term; revised downward on a risk-reducing change of life habits | [S1]; level for the term [S11] |
| Waiver during claim | Premiums waived (or advanced and refunded) throughout an ITT/IPT/IPP claim | [S11] [S5]; refund mechanics [S1] [S9] |
| Partial early repayment | Premium rebased on the guaranteed CRD less the amount repaid | [S9] [S10]; on the original capital elsewhere [S1] |
| Non-payment | Group contract: exclusion 40 days after formal notice, art. L. 141-3 C. ass. | [S9] [S10]; individual contracts follow art. L. 113-3 [S1] [S5] |
| File fee | €10 one-off at one insurer; not in the composite | [S1] [S3] |

7. **No retrieved document publishes a standard-risk rate card**, and none publishes a
   TAEA figure. The only public price point in the corpus is an aggravated-risk average:
   for the 18 569 borrowers whose premiums were capped under the AERAS *écrêtement* in 2023
   (average age 46.4, average insured capital €82 700, average term 18.1 years), **the
   average insurance rate was 1.01 % of initial capital before *écrêtement* and 0.65 %
   after** [REG-R37]. Those are aggravated lives, so 1.01 % bounds a standard rate from
   above rather than describing it. The composite's 0.84 %/yr is a modeling pick inside that
   bound, chosen so that its present value over the base cell equals, to 0.11 %, that of the
   CRD-based alternative scale in `technical-notes.md` — see the Worked example. It is
   **not** an insurer's rate and carries no pricing authority.

### Cost disclosure — TAEA and the fiche standardisée

| Parameter | Representative value | Basis |
|---|---|---|
| TAEA definition | TAEG computed assuming the proposed insurance is entirely required, **minus** the TAEG computed assuming no insurance is required, both under arts. R. 314-1 to R. 314-10 | [R6] |
| Base cell TAEA | 1.40 percentage points (loan TAEG 3.0416 % without insurance, 4.4381 % with) | **[std]** (8) |
| Cost per instalment period | €140.00, added to the loan *échéance* (total monthly outlay €1 249.20) | [R4] L. 313-8; amount **[std]** (7) |
| Total cost over the first 8 years | €13 440.00 | duty [R4] [R10] [REG-R36]; amount **[std]** (8) |
| Total cost over the full loan term | €33 600.00 | duty [R4] [REG-R36]; amount **[std]** (8) |
| *Fiche standardisée d'information* (FSI) | Handed at the first costed simulation for a loan above €75 000 secured by a mortgage on residential property, to **each** borrower and co-borrower separately | [R4] L. 313-10, [R5] R. 313-10 [S4] |
| FSI content | Guarantee definitions; the lender's minimum required guarantees with a required *quotité* box for each of Décès, PTIA, ITT, IPT, IPP and *perte d'emploi*; the guarantees chosen with their *quotité*; the personalised cost estimate; notice of the right to insure elsewhere | [R5] R. 313-9, [R9]; model annexed to the code [R19] |
| FSI additions since 1 June 2022 | The eight-year cost total; a statement that the invalidity guarantee is independent of the social-security notion of invalidity; the medical-questionnaire exemption; the switching right | [R10] |

8. Computed from the base cell's own cash flows, not taken from a document. The TAEA is
   the difference of two internal rates of return on the credit's cash flows [R6]: the
   monthly IRR of 240 payments of €1 109.1952 against €200 000 is exactly 0.25 %/month
   (3.0416 % annual effective), and adding €140.00 to each payment raises it to
   0.3625 %/month (4.4381 % annual effective), a difference of 1.3965 percentage points.
   The eight-year and full-term totals are 96 × €140.00 and 240 × €140.00. No filled-in FSI
   was retrieved, so no published TAEA exists in the corpus to check these against.

---

## Contractual mechanics

### The amortising loan and the CRD

The loan is the spine of the product and everything else is read off it. With *capital
initial* `C`, monthly rate `i = taux nominal / 12` and term `n` months, the *échéance* is

    ech = C x i / (1 - (1 + i)^(-n))

and the CRD immediately after the k-th instalment is

    CRD(k) = ech x (1 - (1 + i)^(-(n - k))) / i,    k = 0..n,  CRD(0) = C,  CRD(n) = 0

equivalently `CRD(k) = CRD(k−1) × (1 + i) − ech`. Contractually this schedule is the lender's
*échéancier* and the insurer reads the CRD off it [S1] [S5] [S9]; the reference model
computes it, so the loan is three numbers rather than a table. Deferred-capital and *in fine*
loans, where only the interest instalments are covered and the final capital instalment is
never indemnified [S1] [S5] [S9] [S10], are out of scope.

### Décès and PTIA

Décès pays the CRD weighted by the *quotité*; the wordings differ on the exact cut — the
CRD shown on the amortisation table the day after the instalment immediately preceding
death, **plus interest accrued since that instalment**, with an instalment falling on the
day of death deemed due [S9]; the same, capped at the CRD at the date of death [S11]; the
CRD shown on the *échéancier* at the date of death [S1]. Payment of the death capital ends
every guarantee for that insured [S1]. PTIA is assimilated to death and pays the same
benefit [S5] [S9] [S11]; its definition is consistent everywhere — definitive inability to
engage in any remunerated occupation **and** permanent need of a third person for the
ordinary acts of daily life — but the acts test is not, requiring assistance for **at least
three of the four** acts (*se laver, se vêtir, se nourrir, se déplacer*) at one insurer [S1]
against **all four** at two others [S5] [S9]. Evidence normally required is category 3
social-security invalidity for scheme members [S1] [S11].

PTIA and Décès are never both paid: PTIA accelerates the death capital. They nevertheless
have **different cover-end ages** — 85 for Décès against 70 for PTIA in the composite
[S9] [S11] — so they cannot be collapsed into one decrement.

### ITT — franchise, benefit, duration

Benefit begins on the day after the *franchise* of `F` continuous days of total
incapacity and is the *échéance* × *quotité* per month [S1] [S9] [S11]; the composite
takes `F` = 90 days. A relapse does not restart the *franchise* where the return to work
ran under 90 days [S9] [S10]. Payment ends on the earliest of: return to work even
part-time (except a therapeutic part-time), retirement or pre-retirement, consolidation,
the age ceiling, recognition of PTIA/IPT/IPP, and exhaustion of the 1 095 days
[S1] [S9] [S11]. Statutory maternity leave is expressly not indemnified [S5]. The
composite pays whole instalments and does not prorate — "Le contrat ne prévoit pas de
prise en charge prorata temporis" [S13]; other insurers prorate by days at 1/30, 1/90 or
1/360 [S1], or decompose non-monthly instalments into equal monthly ones [S11].

### IPT — threshold, barème croisé and the two benefit forms

IPT requires a **combined invalidity rate ≥ 66 %** at consolidation, plus, in most
wordings, permanent inability to carry on the occupation practised at the date of the claim
[S1] [S5] [S9] [S10] [S11] [S12]. The combined rate comes from a double-entry grid crossing
a *taux d'incapacité fonctionnelle* (assessed on the *barème de droit commun du concours
médical*, without regard to occupation) with a *taux d'incapacité professionnelle* (assessed
on the occupation practised before the event, disregarding retraining) [S1] [S5] [S9] [S10]
[S11]; for an insured with no occupation at the claim date only the functional rate is used
[S9] [S10] [S11]. Consolidation is what converts ITT into IPT, and one bank contract fixes
it explicitly — the rate is set at consolidation and **at the latest three years after the
start of the ITT** [S10], the same three years as the 1 095-day cap elsewhere
[S1] [S11] [S12]; the composite therefore treats duration 1 095 days as a forced assessment
point.

The IPT benefit base is the single biggest structural difference in the product: the **CRD**
("IPT en capital"), paid at the medical recognition of IPT and ending every guarantee for
that insured [S1] [S2] [S7]; the ***échéances*** ("IPT en rente"), identical to the ITT
benefit and running to the end of the loan or the age limit [S5] [S7] [S9] [S11]; the
insured's choice between the two [S3]; or no IPT at all, in one narrow bank group policy
carrying Décès, PTIA, *invalidité AERAS* and ITT only [S13]. The composite takes the *rente*
form; the `crd` form is a model point switch, not a different model — it converts IPT from
an annuity into a single payment that extinguishes cover.

### Forfaitaire versus indemnitaire

*Forfaitaire*: the benefit is the contractually insured instalment, paid whatever the
employer or the compulsory scheme pays. *Indemnitaire*: the benefit is capped by the actual
income loss, so an insured whose salary is fully maintained receives nothing [S6]. Death and
PTIA are always effectively *forfaitaire* against the CRD; the distinction bites only on
ITT, IPT, IPP and *perte d'emploi*. Four sampled contracts are *forfaitaire* by design
[S1] [S3] [S6] [S11] [S12]; one bank group policy is **indemnitaire by default and
forfaitaire by option**, and its four-way rule is the clearest statement of the mechanic in
the corpus [S10]:

| Category | ITT/IPT benefit |
|---|---|
| Self-employed, non-civil-servant; or Swiss-franc loan | 100 % of the monthly instalment (insurance premium included), pro-rated by days, × *quotité* |
| Non-working and drawing no unemployment benefit | 50 % of the monthly instalment, same basis |
| Employee, civil servant, or jobseeker drawing benefit | instalment × *quotité*, **but limited to the income loss** |
| Anyone holding the *Prestation Forfaitaire* option | 100 % of the monthly instalment |

The income loss is defined contractually: *revenu de référence* (average monthly net taxable
income and allowances over the 12 months before the stoppage) less *revenu de remplacement*
(all benefits owed by social security, the employer and any *prévoyance* scheme, recomputed
at the claim date on the reference income), the reference income being revalued by the
published private-sector wage index after three consecutive years of claim [S10]. The CCSF
criteria list makes the *forfaitaire* basis an explicitly selectable lender requirement and
tells lenders to state the required value, "par exemple son caractère forfaitaire ou
indemnitaire" [R11].

### Quotité and the anti-duplication rule

The *quotité* is the percentage of the borrowed capital insured on one life, chosen on the
adhesion form, and it applies to **every** guarantee of that insured's cover
[S1] [S9] [S11]. Per insured it may not exceed 100 % [S1] [S5] [S9] [S11], in 1 % steps
[S9]. Across co-borrowers the total may exceed 100 %: on a €100 000 loan a borrower at
100 % and a co-borrower at 40 % means the insurer pays 100 % of the CRD or instalment on
the first life and 40 % on the second [S9]; other retrieved examples are 80 %/60 % [S1]
and 60 %/40 % [S3]. Raising a *quotité* mid-contract requires fresh underwriting [S9].

Two rules bound the total. The **200 % ceiling follows arithmetically** from the per-head
100 % cap. **The 100 % floor is not a contract term** — no retrieved notice imposes one;
it is a lender requirement expressed through the FSI's "garanties minimales exigées par le
prêteur" block and the CCSF *fiche personnalisée* [R9] [R11], so the assertion that "the
total must be at least 100 %" is **[unverified]** as an insurance-contract rule.
Anti-duplication is explicit: the contract "ne peut, en aucune façon, donner lieu à une
indemnisation supérieure à 100 % en cas de sinistres concomitants ou non pour deux assurés
d'un même contrat de prêt" [S1] [S12]; a third contract caps the total paid on one loan at
the CRD [S11].

### Guarantee-specific age limits

Every guarantee has its own cover-end age, and they differ by up to twenty years:

| Guarantee | Composite | Observed range |
|---|---|---|
| Décès | 85 | 75 [S13] · 80 [S10] · 85 [S5] [S6] [S9] [S11] · 90 [S1] [S7] |
| PTIA | 70 | 65 [S13] · 65 extendable to 70 [S1] · 67 [S10] · 70 [S5] [S9] [S11] · 71 [S7] |
| ITT / IPT / IPP | 70 | 65 [S13] · 65 or 70 by option [S1] · 67 [S10] [S11] · 70 [S5] [S9] · 71 [S6] |

Every incapacity and invalidity guarantee also ends on retirement or pre-retirement,
however early, unless the retirement itself results from the indemnified state
[S1] [S9] [S10] [S11]. **A cover that ends before the loan does is a real and
under-modelled feature.** In the base cell the loan matures at attained age 72 while the
ITT, IPT and PTIA guarantees end at 70, so the last 24 months of the loan carry Décès only
— and, because the rate is *nivelé*, the premium is unchanged: "Le taux de prime a été
nivelé sur la durée du prêt ; par conséquent, la cessation de ces garanties n'a pas
d'incidence sur le montant de la prime" [S13]. The CCSF found 50 %–75 % of claim declines
by external alternative insurers were mis-declarations — wrong insurer, claim inside the
*franchise*, or **the maximum cover age already passed** [R12].

### Résiliation à tout moment (loi Lemoine)

The borrower may cancel the insurance **at any time from signature of the loan offer**
defined in art. L. 313-24 of the Code de la consommation, by registered letter or
registered electronic mail [R3] [R1] art. 1 [REG-R35]. In force **1 June 2022 for new loan
offers and 1 September 2022 for contracts already running** [R1] art. 8. The mechanics:

- The lender may not refuse a substitute contract presenting **an equivalent level of
  guarantee**; any refusal must be explicit and state every reason, naming the missing
  information and guarantees [R7] [R1] art. 2 [REG-R36].
- The lender answers within a **délai de dix jours ouvrés** and amends the credit contract
  **without additional fees**, restating the TAEG [R8] L. 313-31, [R1] art. 5; it may not
  change the loan rate or the credit conditions, nor charge any fee including analysis
  fees [R8] L. 313-32.
- Cancellation takes effect **ten days after the insurer receives the lender's
  acceptance**, or on the substitute contract's effective date if later; on refusal the
  contract is not cancelled [R3], and the 2025 group notice implements exactly this [S9].
- The insurer owes an **annual reminder** of the cancellation right, with fines of €3 000
  for individuals and €15 000 for legal persons [R1] art. 3; insurance information must be
  retained eight years [R1] art. 4.

Equivalence is assessed against the CCSF *liste de place*: the lender selects **at most 11
of 18 criteria**, plus at most 4 of the 8 on *perte d'emploi*, must state the required
value wherever possible, must publish its list on its website and on the FSIs it issues,
and must hand the borrower a *fiche personnalisée* with the fully valued list before the
loan offer [R11] [S3] [S4]. Two earlier regimes survive in older wordings and are not the
composite: a 12-month window from signature of the loan offer with notice 15 days before
its end [S1] [S6], and an annual right at each loan-offer anniversary with two months'
notice [S1] — the attribution of that annual right to the 2017 *amendement Bourquin* is
**[unverified]**, the statute not having been retrieved. Professional-loan adhesions are
excluded from the *à tout moment* right, which is tied to art. L. 313-1 1° credits
[R3] [S1].

### Underwriting, exclusions and the droit à l'oubli

Where the questionnaire waiver does not apply, a health questionnaire is required, valid
6 months [S9], with laboratory tests and possibly a medical examination at the insurer's
expense; the outcome is acceptance at standard terms, acceptance with a *surprime* and/or
guarantee restrictions the member countersigns, or refusal [S1]. Non-disclosure sanctions are
the general ones — nullity for intentional misstatement (art. L. 113-8), proportional benefit
reduction for good-faith misstatement (art. L. 113-9) [S1] [S9].

**Droit à l'oubli.** No past cancer or hepatitis C need be declared where the end of the
therapeutic protocol is more than **five years** old and there has been no relapse; cover
is then granted with no surcharge and no exclusion for that history, where the contract's
term falls before the borrower's **71st birthday** [R17]. The five-year cap is statutory
[R16] [R1] art. 9 [REG-R35]. The **grille de référence AERAS** applies where the insured
share does not exceed **€420 000** (per operation for a principal residence, otherwise on
the cumulative outstanding) and the term falls before the 71st birthday; list I sets
shorter delays after which standard terms apply, list II sets maximum surcharge rates by
guarantee [R17]. The grid itself was **not retrieved**; its pathology-by-pathology delays
must not be invented.

The two commercially decisive exclusions are ***affections disco-vertébrales*** (back) and
***affections psychiatriques***, both normally excluded unless hospitalisation thresholds
are met, and both routinely bought back by a priced option [S1] [S3] [S5] [S6] [S9] [S12].
Other standard exclusions: intentional acts including attempted suicide; suicide in the
first year; undeclared prior conditions except where the *droit à l'oubli* applies;
narcotics; drunk driving; nuclear effects; excluded sports [S1] [S7].

---

## Riders and options

**In scope (modeled).** The **ITT → IPT transition**, as a competing exit from the ITT
state at the claim duration and at the 1 095-day assessment [S1] [S10] [S11]; **premium
waiver during claim** [S5] [S11], as zero premium income from lives in claim; and three
switches carried as model point columns — the **premium base**, level on *capital initial*
[S9] [S11] [S13] versus annually re-read on the CRD at the attained age [S2] [S5] [S7] [S8];
the **indemnity basis**, *forfaitaire* [S1] [S3] [S6] [S11] versus *indemnitaire* [S10]; and
the **IPT benefit form**, *échéances* [S5] [S9] [S11] versus CRD [S1] [S2] [S7].

**Out of scope (documented, no cash flows projected):** *perte d'emploi* [S1] [S3] [S8] — a
separate module with its own *carence*, *franchise*, eligibility and duration limits and its
own eight CCSF criteria [R11]; **IPP** and every partial benefit below the 66 % IPT threshold
[S1] [S5] [S9] [S10] [S11]; *mi-temps thérapeutique* [S1] [S9] [S10] [S11] [S12]; *garantie
aide à la famille* [S9] [R12]; *garantie invalidité spécifique* / *invalidité AERAS*
[S1] [S6] [S9] [S13]; *option Prévoyance*, covering the uninsured *quotité* for a beneficiary
of the member's choosing [S1] [S5] [S6]; exclusion buy-backs [S1] [S5] [S6] [S9] [S12];
medical-professions invalidity [S5] [S12]; the extension-to-70 options [S1] [S6] [S7];
provisional accidental-death cover during underwriting [S1] [S12]; the free €1 000
return-to-work lump sum [S1]; and multi-head aggregation across co-borrowers [S1] [S9].

---

## Variations across insurers

1. **Indemnity basis.** *Forfaitaire* dominates the alternative-contract segment
   [S1] [S3] [S6] [S11] [S12]; one bank group policy is *indemnitaire by default* with a
   priced *forfaitaire* option and a fully specified income-loss definition [S10] — the
   difference between a benefit that is a fixed instalment and one that is a function of
   the claimant's employment contract and *prévoyance* cover.
2. **IPT benefit base.** CRD [S1] [S2], *échéances* [S5] [S9] [S11], the insured's choice
   [S3] [S7], or no IPT at all [S13].
3. **IPP benefit shape.** A linear ramp (N − 33)/33 capped at 100 % [S1] [S11] — which
   meets IPT continuously at N = 66 % — against a flat 50 % of the ITT benefit anywhere in
   the band [S5] [S9] [S10]: materially different liability profiles for the same medical
   state.
4. **Franchise menus and the ITT day cap.** Menus run from a single fixed 90 days [S11] to
   15/30/60/90/180 [S12]; the 1 095-day cap is explicit at three insurers [S1] [S11] [S12]
   and absent at two others, which end ITT at consolidation [S5] [S9] — see footnote 5.
5. **Premium base.** Level on *capital initial* [S9] [S11] [S13]; annually re-read on the
   CRD and the attained age [S2] [S5] [S7] [S8]; both offered [S10]. One contract states the
   *nivelé* design in terms and draws the consequence [S13].
6. **Age limits.** See the table above; the spread on Décès alone is 75 to 90.
7. **ITT trigger.** "Own occupation" is the mainstream definition [S1] [S9] [S11] [S12];
   one bank group policy instead anchors ITT to social security — a general-scheme member
   is in ITT only if actually drawing sickness or accident cash benefits, or classified in
   category 2 or 3 invalidity under art. L. 341-4 of the Code de la sécurité sociale [S13]
   — while another states expressly that its assessment "n'est pas liée à la décision de
   la Sécurité sociale" [S1], the warning the FSI model has carried since 1 June 2022
   [R10]. The PTIA acts test likewise splits three-of-four [S1] against four-of-four
   [S5] [S9].
8. **Structural outlier.** One sampled product is a true **individual** branch-20 term-life
   contract used as mortgage cover: the death benefit is a *capital garanti* stated in the
   *conditions particulières* rather than the lender's CRD, the lender is beneficiary only
   "à concurrence des sommes restant dues", ITT is paid as fixed **daily** indemnities, and
   IPT pays the death capital [S12]. It needs a scheduled-sum-insured chassis, not a CRD
   chassis.
9. **Sampling caveat.** Crédit Agricole — reported as one of the three largest writers of
   the risk [unverified] — is missing: its group notice returned HTTP 502 and was never
   read [S14]. Generali, Suravenir, MNCAP, AFI-ESCA and Swiss Life were not sampled at
   all, and the *contrat alternatif bancaire* segment (4.4 % of portfolios [R12]) has no
   document in the corpus.

---

## Regulatory context

**Prudential (ACPR / Solvabilité II).** ADE liabilities are valued as a best estimate —
the probability-weighted average of future cash flows discounted at the relevant risk-free
term structure — plus a risk margin, under Solvabilité II as transposed into the Code des
assurances [REG-R4], with the curves published monthly by EIOPA [REG-R5]. The
French statutory balance sheet carries its own eleven technical provisions under art.
R. 343-3, of which the *provision mathématique* and the *provision pour égalisation* for
mortality fluctuations on group death business are the ones an ADE book touches [REG-R6];
supervision is by the ACPR [REG-R10]. **No reserving or prudential source specific to this
product was retrieved**: the *nivelé* design is stated in a contract [S13] and follows from
the tariff structures elsewhere [S1] [S9] [S11], but nothing retrieved establishes how a
French insurer reserves the resulting increasing-risk pattern, and **everything about that
is [unverified]** here. No ACPR document on assurance emprunteur was obtained at all — the
whole `banque-france.fr` estate refused automated fetches in the research pass (see the
provenance note in `sources.md`), so no statement about ACPR expectations is made anywhere
in these documents.

**Mortality basis.** Death and PTIA sit on the non-annuity homologated tables **TH 00-02**
(male) and **TF 00-02** (female), homologated by the arrêté du 20 décembre 2005 for
"contrats autres que de rente viagère" [REG-R22], applied with the *décalage d'âge* (age
shift) schedules annexed to art. A. 335-1 of the Code des assurances, which permits exactly
two kinds of table — homologated tables by sex, or the undertaking's own *tables
d'expérience* certified by an independent approved actuary [REG-R23]. Neither is
redistributable here; the decrement CSVs this library ships are **[std] proxies** built
from INSEE population data [REG-R24].

**Conduct.** Distribution follows the DDA as transposed by ordonnance n° 2018-361 and
décret n° 2018-431, in force 1 October 2018 [REG-R32], the IPID/DIPA being the retail
disclosure [S7]. The product-specific layer is the Code de la consommation: L. 313-8, the
three mandatory cost presentations [R4] [REG-R36]; L. 313-10 and R. 313-8 to R. 313-10, the
FSI [R4] [R5] [R19], on the model annexed by the arrêté du 29 avril 2015 [R9] as amended by
the arrêté du 27 mai 2022 [R10]; and L. 313-29 to L. 313-32, the notice in the credit
contract, the ten-working-day answer and the no-fee, no-rate-change rules [R8]. The CCSF
*avis* of 13 janvier 2015 supplies the equivalence method and the *liste de place* [R11].

**Aggravated risks.** The AERAS convention and art. L. 1141-5 of the Code de la santé
publique govern the *droit à l'oubli* and the *grille de référence* [R16] [R17]. In 2023,
2.9 million loan-insurance applications were assessed, of which **7.6 % (224 068)**
presented a *risque aggravé de santé*, down from 9.6 % in 2022 and 12.1 % in 2021 — a fall
attributed to the loi Lemoine questionnaire removal and the five-year *droit à l'oubli*;
**94.5 %** of those received an offer covering at least death, and, excluding files sent to
the very-high-risk pool, offers with no *surprime* and no exclusion ran at **death 65 %,
PTIA 87 %, incapacité-invalidité 51 %** [REG-R37].

**Actuarial standards and accounting.** French actuarial work on this product sits under
the Institut des actuaires' *normes de pratique actuarielle* — NPA 1 on general practice
[REG-R43] and NPA 2 on actuarial models, which expressly covers pricing and the technical
studies attached to new products [REG-R44]; both are category-3 *pratiques recommandées*
from which a departing member must be able to explain why. IFRS 17 applies to
IFRS-reporting French insurers [REG-R45]; its fulfilment-cash-flow engine consumes the same
projections with its own discounting, risk adjustment and CSM layers
(cited-not-specified).

**Tax.** **No tax source was retrieved.** Premiums are quoted taxes-included [S11] and two
insurers provide for premium changes on a change of tax rates [S1] [S5], but the applicable
*taxe spéciale sur les conventions d'assurance* treatment of the death versus the
incapacity/invalidity components was not established. Treat any tax rate as
**[unverified]**; the reference model carries none.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-assurance_emprunteur-r1
[R10]: #frlib-assurance_emprunteur-r10
[R11]: #frlib-assurance_emprunteur-r11
[R12]: #frlib-assurance_emprunteur-r12
[R13]: #frlib-assurance_emprunteur-r13
[R16]: #frlib-assurance_emprunteur-r16
[R17]: #frlib-assurance_emprunteur-r17
[R18]: #frlib-assurance_emprunteur-r18
[R19]: #frlib-assurance_emprunteur-r19
[R2]: #frlib-assurance_emprunteur-r2
[R3]: #frlib-assurance_emprunteur-r3
[R4]: #frlib-assurance_emprunteur-r4
[R5]: #frlib-assurance_emprunteur-r5
[R6]: #frlib-assurance_emprunteur-r6
[R7]: #frlib-assurance_emprunteur-r7
[R8]: #frlib-assurance_emprunteur-r8
[R9]: #frlib-assurance_emprunteur-r9
[REG-R10]: #frlib-reg-r10
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R32]: #frlib-reg-r32
[REG-R35]: #frlib-reg-r35
[REG-R36]: #frlib-reg-r36
[REG-R37]: #frlib-reg-r37
[REG-R4]: #frlib-reg-r4
[REG-R43]: #frlib-reg-r43
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
