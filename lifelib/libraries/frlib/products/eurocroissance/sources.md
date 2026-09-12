# Sources

Source ids — **[S#]** primary product and firm documents, **[R#]** regulatory and actuarial
references — are carried **verbatim** from `_research/eurocroissance.md` and are frozen; they are
never renumbered. Only sources actually cited in `product-spec.md` or `technical-notes.md` are
listed. **Omitted, and retaining their numbers in the research file: S11, R17 and R20.** S11
(Profession CGP, "Fonds eurocroissance : l'âge de raison ?") returned HTTP 403 twice and nothing
was ever cited from it; R17 (ACPR *Analyses et synthèses* n° 170 on the 2024 life market) was
retrieved but carries no eurocroissance figure these documents rely on; R20 (ACPR n° 179 on the
2025 life market) returned HTTP 403 to WebFetch and to `curl` with a browser User-Agent. No new
sources were fetched at drafting. Each heading below carries the publisher and the document type.

**Access date for every entry: 2026-08-26.** The consequential gap: **no *notice d'information*,
*conditions générales* or PRIIPs *document d'information clé* for any eurocroissance support
could be retrieved** [S10], so every insurer-level parameter here is a third-party fact-sheet
figure [S8] [S9] or **[std]**.

---

## Primary product and firm documents [S#]

(frlib-eurocroissance-s1)=

### S1 — AXA France Vie, "Fonds Croissance" — retail insurer product page
- URL: https://www.axa.fr/epargne-retraite/assurance-vie/eurocroissance.html
- Retrieved: YES (page fetched and read).
- Used for: the *provision mathématique* / *provision de diversification* split and the statement
  that the insurer commits to **the number of parts but not their value**; guarantee **100 % of
  net invested capital** at a **10-year minimum** maturity; total or partial capital loss before
  maturity; the *garantie décès plancher*; the 2018–2023 net returns and the 2.98 % average since
  2017.

(frlib-eurocroissance-s2)=

### S2 — AXA France Vie, "Fonds Croissance" — second retail product page
- URL: https://www.axa.fr/particuliers/epargne/assurance-vie/eurocroissance.html
- Retrieved: YES.
- Used for: 100 % of net invested capital guaranteed at the 10-year maturity; **rachat at any
  time without surrender penalty** but exposed to capital loss; **SRI 2/7**.

(frlib-eurocroissance-s3)=

### S3 — AXA France, "AXA France annonce une hausse de ses rendements" — press release, 15 January 2026 (2025 credited rates)
- URL: https://www.axa.fr/particuliers/qui-sommes-nous/espace-presse/epargne-retraite/assurance-vie-rendements-2025.html
- Retrieved: YES (full press-release text).
- Used for: Fonds Croissance 2025 **2.50 %–4.50 %**, average **3.13 %**; euro supports
  2.25 %–4.25 %; PER "Ma Retraite" eurocroissance 3.25 %; the 2026 bonus device (+0.50 % on
  pre-2026 savings, **+2.00 %** on new payments, ≥ **45 %** unit-linked condition).

(frlib-eurocroissance-s4)=

### S4 — AXA France Vie, "Dispositifs euro + et eurocroissance + 2026" — insurer product page
- URL: https://www.axa.fr/epargne-retraite/assurance-vie/bonus-euro-2026.html
- Retrieved: YES.
- Used for: the **Eurocroissance +** conditions — +2 % on 2026 payments up to 4.50 %, the ≥ 45 %
  unit-linked condition, the hold to **31 December 2026** and through to the attribution date **no
  later than 1 April 2027**, exclusions; and the **art. A. 132-3** guaranteed-rate ceiling.

(frlib-eurocroissance-s5)=

### S5 — Generali France, "Fonds croissance" — insurer press-room topic index
- URL: https://presse.generali.fr/fonds-croissance.html
- Retrieved: YES (index page read; headline figures only).
- Used for: G Croissance 2014 as Generali's first eurocroissance fund and **G Croissance 2020**
  launched December 2020 as its PACTE successor — the two generations being distinct funds.

(frlib-eurocroissance-s6)=

### S6 — Generali France, "Generali France annonce des rendements 2025 solides" — press release, 26 January 2026
- URL: https://www.generali.fr/actu/generali-strategie-diversification-2025-taux-pb/
- Retrieved: YES (press-release text read).
- Used for: the 2025 euro-fund average of **2.55 %** for life insurance — the comparator for the
  eurocroissance premium — and the description of Fonds Croissance as carrying a **partial
  capital guarantee at maturity**.

(frlib-eurocroissance-s7)=

### S7 — Crédit Agricole Assurances (Predica), "Predica lance Objectif programmé" — product-launch press release, 16 October 2014
- URL: https://www.ca-assurances.com/publication/predica-lance-objectif-programme-son-premier-support-croissance-eurocroissance/
- Retrieved: YES.
- Used for: the first-generation parameters — **duration 8 to 40 years**, **guarantee level 80 %
  to 100 %**, both chosen by the saver — and the distribution list.

(frlib-eurocroissance-s8)=

### S8 — FranceTransactions, "G CROISSANCE 2020 (Generali)" — third-party fund fact page (secondary; Generali's own notice could not be retrieved, see S10)
- URL: https://www.francetransactions.com/assurance-vie/fonds-euro-croissance/g-croissance-2020-generali-eurocroissance.html
- Retrieved: YES (published 7 February 2021; performance table updated 27 January 2026).
- Used for: the only retrieved charge levels for any eurocroissance support — *frais de gestion*
  **1.00 %**, *frais sur versements* **4.50 % max**, *frais de conversion* **0.50 %** — plus
  guarantee **80 %**, term **8 to 30 years**, and the 2020–2025 return series. Third-party, so
  treated as indicative and marked as such wherever used.

(frlib-eurocroissance-s9)=

### S9 — MoneyVox, "Eurocroissance : principe et fiscalité du contrat d'assurance vie" — third-party explainer with a cross-insurer rate table
- URL: https://www.moneyvox.fr/assurance-vie/euro-croissance.php
- Retrieved: YES (page last updated 26 May 2026 per the fetched page).
- Used for: the 2025 cross-market net-return table (0.90 %–3.40 % across seven supports);
  **€11.3 bn** across more than **700 000** contracts at March 2025; the social levy at the
  fund's maturity; and — reported and **marked [unverified]** — the reserved-name claim.

(frlib-eurocroissance-s10)=

### S10 — Generali Vie, G Croissance 2014 / 2020 — *notice d'information valant conditions générales* and PRIIPs *document d'information clé*
- URL: not located (Generali's pages refer to the notice but expose no PDF)
- Retrieved: **NO**. Known reference only; nothing is cited from it.
- Used for: the record, in both scope notes, that **no contractual document for any
  eurocroissance support could be retrieved**.

---

## Regulatory and actuarial references (product research numbering) [R#]

(frlib-eurocroissance-r1)=

### R1 — Légifrance, Code des assurances, arts. L. 134-1 to L. 134-5 (legislative part, Chapter IV)
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000029141706/ ;
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038611220 (L. 134-1)
- Retrieved: YES (Légifrance pages; the full chapter also read verbatim from the consolidated code
  PDF, edition 2026-07-19, at https://codes.droit.org/PDF/Code%20des%20assurances.pdf, downloaded
  with a browser User-Agent).
- Used for: the **two modalities** and the exclusion of temporary death assurance (L. 134-1); the
  *comptabilité auxiliaire d'affectation* (L. 134-2); the duty to **complete the representation**
  of 1° engagements and to constitute a **PGT** for 2° engagements (L. 134-3); policyholder
  priority over all other creditors (L. 134-4).

(frlib-eurocroissance-r2)=

### R2 — Légifrance, Code des assurances, arts. R. 134-1 to R. 134-12 (regulatory part, Chapter IV)
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000029426878/ ;
  .../LEGIARTI000039739654 (R. 134-1) ; .../LEGIARTI000039739643 (R. 134-4)
- Retrieved: YES (Légifrance pages; full chapter also read verbatim from the consolidated code
  PDF, edition 2026-07-19).
- Used for: nearly every mechanic in both documents — the minimum part value and the denomination
  arrêté (R. 134-1); rights in **number of parts** and the PM as the discounted guarantee
  (R. 134-2); the **six permitted charge bases**, base 3° restricted to accounts holding no 1°
  engagements (R. 134-3); the participation account, its destinations and the part-value floor on
  a debit balance (R. 134-4); the **surrender and transfer values** and the eight-year cap on a
  non-surrender period (R. 134-5); the **maturity amounts** and the three-month notice (R. 134-6);
  complementary guarantees outside the account (R. 134-7); assets at realisation value (R. 134-8);
  admitted provisions (R. 134-9); pre-sale disclosure (R. 134-10); per-account application
  (R. 134-11).

(frlib-eurocroissance-r3)=

### R3 — Légifrance, Code des assurances, arts. A. 134-1 to A. 134-7 (arrêté part, Chapter IV)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801782 (A. 134-1) ;
  .../LEGIARTI000039801776 (A. 134-2) ; .../LEGIARTI000039801769 (A. 134-3) ;
  .../LEGIARTI000046824887 (A. 134-6)
- Retrieved: YES (four Légifrance article pages; A. 134-4, A. 134-5 and A. 134-7 read verbatim
  from the consolidated code PDF, edition 2026-07-19).
- Used for: the **90 %-of-TEC*n*** discount ceiling with interpolation, the longest-TEC rule, the
  zero floor and the irreversible per-account method choice (A. 134-1); the **PGT** definition and
  its A. 132-18 basis (A. 134-2); the two tests gating a guarantee revaluation (A. 134-3); the
  five-year and 15 %-of-PM conversion gates (A. 134-4); the **at-least-monthly** intermediate
  value and the forward part value used for exits (A. 134-5); the **SRI ≤ 2** maturity default
  (A. 134-6); the annual ACPR return by maturity year and guarantee level (A. 134-7).

(frlib-eurocroissance-r4)=

### R4 — Légifrance (JORF), LOI n° 2019-486 du 22 mai 2019 (loi PACTE), article 72
- URL: https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000038496267
- Retrieved: YES.
- Used for: the creation of the **2° modality** — no euro guarantee during accumulation, a euro
  guarantee at maturity — and the transformation of 1° into 2° engagements by agreement.

(frlib-eurocroissance-r5)=

### R5 — Légifrance (JORF), Décret n° 2019-1437 du 23 décembre 2019 (implementing decree for PACTE art. 72)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000039667326
- Retrieved: YES (JORF text page read).
- Used for: the rewriting of the whole regulatory chapter and the addition to R. 343-3 of the
  provisions 9°, 10° and 11°; in force **1 January 2020**.

(frlib-eurocroissance-r6)=

### R6 — Légifrance (JORF), Arrêté du 12 septembre 2014 (the first-generation A. 134 series)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000029446963
- Retrieved: YES (JORF text page read).
- Used for: the **2014 regime** — the 90 %-of-TEC rule PACTE retained, and the 8 % volume cap and
  8-year holding period PACTE removed and lengthened.

(frlib-eurocroissance-r7)=

### R7 — Légifrance (JORF), Décret n° 2025-1333 du 26 décembre 2025 (reinstating art. R. 134-12, apports d'actifs)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053174741
- Retrieved: YES (JORF text page read; R. 134-12 also read verbatim in the consolidated code PDF).
- Used for: contributions up to **10 % of the diversification provision**, entering at realisation
  value and **endowing the PCDD**; the three-limb re-allocation cap and the **sixteenth-year**
  deadline; and the rule that affectations happen on the participation-account striking dates
  **after the balance has been allocated**, which fixes the model's annual processing order.

(frlib-eurocroissance-r8)=

### R8 — Légifrance (consolidated code PDF), Code des assurances art. R. 343-3 (catalogue of life provisions)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039739686 ;
  https://codes.droit.org/PDF/Code%20des%20assurances.pdf
- Retrieved: YES (text read verbatim from the consolidated PDF).
- Used for: the definitions of 9° *provision de diversification*, 10° *provision collective de
  diversification différée* and 11° *provision pour garantie à terme*, and the rule that an
  engagement is provisioned under only one category.

(frlib-eurocroissance-r9)=

### R9 — Légifrance (consolidated code PDF), Code des assurances art. A. 132-16 (holding period for profit-sharing reserves)
- URL: https://codes.droit.org/PDF/Code%20des%20assurances.pdf
- Retrieved: YES (read verbatim; version from the arrêté du 26 décembre 2019 art. 2).
- Used for: the **fifteen-year** clock on sums carried to the PCDD, against eight years for a euro
  fund's *provision pour participation aux bénéfices*.

(frlib-eurocroissance-r10)=

### R10 — Légifrance (consolidated code PDF), Code des assurances arts. A. 132-18 and R. 132-5-3
- URL: https://codes.droit.org/PDF/Code%20des%20assurances.pdf
- Retrieved: YES (both read verbatim; A. 132-18 from the arrêté du 14 août 2017, R. 132-5-3 from
  décret n° 2024-539 art. 2).
- Used for: the mortality bases A. 134-2 points to for the PGT — homologated tables by sex, or an
  insurer table **certified by an independent approved actuary** — and the **5 %** surrender
  indemnity cap, together with R. 132-5-3's **permission** for the contract to provide no
  indemnity at all once it has been in force more than ten years. The article grants that
  permission; it does not prohibit an indemnity after ten years, and the reference contract's
  zero beyond ten years is the permission taken up, **[std]**.

(frlib-eurocroissance-r11)=

### R11 — Légifrance (consolidated CSS PDF), Code de la sécurité sociale art. L. 136-7 (social levy)
- URL: https://codes.droit.org/PDF/Code%20de%20la%20s%C3%A9curit%C3%A9%20sociale.pdf
- Retrieved: YES (read verbatim; version from LOI n° 2026-103 du 19 février 2026 art. 24).
- Used for: the product-specific trigger at II 3° b) — CSG/CRDS levied **"à l'atteinte de la
  garantie"** on the surrender value of those engagements less the premiums allocated to them.

(frlib-eurocroissance-r12)=

### R12 — Légifrance (consolidated CGI PDF), Code général des impôts arts. 125-0 A and 990 I
- URL: https://codes.droit.org/PDF/Code%20g%C3%A9n%C3%A9ral%20des%20imp%C3%B4ts.pdf
- Retrieved: YES (both read verbatim; 125-0 A from LOI n° 2021-1900 art. 35, 990 I from LOI
  n° 2023-171 art. 3).
- Used for: the ordinary assurance-vie income-tax regime; the **transformation neutrality** of
  125-0 A I 2°, which preserves fiscal seniority on a move into diversification-provision rights;
  and 990 I — €152 500 per beneficiary, then 20 % up to €700 000 and 31.25 % above.

(frlib-eurocroissance-r13)=

### R13 — Institut des actuaires, Peltier and Odier, "Eurocroissance : quels sont les impacts attendus de la loi PACTE ?" — published actuarial *mémoire*, 86 pp.
- URL: https://www.institutdesactuaires.com/docs/mem/8e47df87101af694559589fb43a46a29.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Undated on its cover; its placement in
  **2020–2021** is inferred and **[unverified]**.
- Used for: the only complete public parameterisation of this product, and the anchor for most
  **[std]** levels — initial premium €10 000 with free additional premiums of €2 000, age 57,
  10-year term, `g` = 100 %, **entry charge 2 %**, **encours charge 0.8 %**, **performance charge
  10 %**, initial part value **€10**, the **90 %** TEC haircut, surrender rates 2 %–3 % (full) and
  6 % then 2 %–4 % (partial), *transfert de richesse* at 10 % of net premiums for three years, the
  **euro-fund rate + 0.30 %** PCDD piloting objective — plus its structural findings (the reform
  removes the PM and gives **one common return for all savers**; solvency improves 20–26 points,
  worth 13 %–20 % more equity exposure; pooling two maturity cohorts gives **no** mutualisation
  benefit). Its printed discount expression is dimensionally suspect and is **not** copied.

(frlib-eurocroissance-r14)=

### R14 — France Assureurs, "En 2024, l'assurance vie a confirmé son attractivité" — trade-body press release, 31 January 2025
- URL: https://www.franceassureurs.fr/espace-presse/les-communiques-de-presse/assurance-vie-attractivite-2024/
- Retrieved: YES.
- Used for: the only retrieved document sizing eurocroissance directly — **€11.1 bn (+24 %) across
  673 000 contracts (+26 %) at end-2024** — and the €1 989 bn market denominator.

(frlib-eurocroissance-r15)=

### R15 — France Assureurs, "L'assurance vie en 2024" — chiffres clés page, 23 September 2025
- URL: https://www.franceassureurs.fr/nos-chiffres-cles/assurance-vie/lassurance-vie-en-2024/
- Retrieved: YES.
- Used for: the unit-linked comparator (**€587.1 bn** of provisions at end-2024), and as evidence
  that eurocroissance is **not broken out** in the standard statistical presentation.

(frlib-eurocroissance-r16)=

### R16 — France Assureurs, "L'assurance vie en 2025" — trade-body press release, 27 January 2026
- URL: https://www.franceassureurs.fr/espace-presse/lassurance-vie-en-2025-une-collecte-solide-au-service-de-leconomie-francaise/
- Retrieved: YES.
- Used for: end-2025 encours **€2 107 bn**, and the fact that this release carries **no
  eurocroissance line**, so no end-2025 product size is available from a retrieved source.

(frlib-eurocroissance-r18)=

### R18 — ACPR / Banque de France, "Analyses et synthèses n° 146 — Le marché de l'assurance-vie en 2022" — supervisory analysis, 20 March 2023
- URL: https://acpr.banque-france.fr/system/files/import/acpr/medias/documents/20230320_as146_av_2022_vf.pdf
- Retrieved: YES — only via `curl` with a browser User-Agent; a plain fetcher returns HTTP 403 on
  this host. Full text extracted.
- Used for: the methodological fact that ACPR's weekly life-flows collection "se concentre sur
  l'analyse des supports rachetables (**excluant l'épargne retraite et les produits
  eurocroissance**)".

(frlib-eurocroissance-r19)=

### R19 — ACPR / Banque de France, "Analyses et synthèses n° 175 — Revalorisation 2024" — annual revaluation study, 4 August 2025
- URL: https://acpr.banque-france.fr/system/files/2025-08/20250804_AS175_Revalorisation_contrats_assurance_vie_2024.pdf
- Retrieved: YES (via `curl` with a browser User-Agent; full text extracted).
- Used for: the macro anchor behind the **[std]** TEC10 level — the **10-year OAT averaged 3.0 %**
  in both 2024 and 2023 — and as evidence that the study contains no eurocroissance section.

(frlib-eurocroissance-r21)=

### R21 — Sia Partners, "Eurocroissance : un nouvel élan" — practitioner analysis, 17 November 2023
- URL: https://www.sia-partners.com/fr/publications/publications-de-nos-experts/eurocroissance-un-nouvel-elan
- Retrieved: YES.
- Used for: market sizing at **€7.1 bn (end-2022)** and **€7.6 bn (mid-2023, +41 %)** across more
  than 470 000 contracts; PCDD smoothing over **15 years**; and the verdict that only a handful of
  insurers offer the new eurocroissance. Its 8-year minimum-duration statement is reported as
  **[unverified]**.

(frlib-eurocroissance-r22)=

### R22 — Légifrance, Ordonnance n° 2014-696 du 26 juin 2014 (the ordonnance that created Chapter IV)
- URL: not resolved (a guessed identifier returned an empty page; the search budget was exhausted
  before a verified URL could be obtained)
- Retrieved: **NO**. Known reference only.
- Used for: the chronology only, and cited as not retrieved. What is verified about it comes from
  the texts that cite it [R1] [R4]; the content of its article 3 is **[unverified]**.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against `references/regulatory-and-actuarial-references.md` (ids R1–R49
frozen there; prefixed REG- in product documents to avoid collision with the product research
numbering above). Research provenance: `_research/regulatory-actuarial.md`. Entries cited by the
two documents in this directory:

- **REG-R1** — Directive 2009/138/CE (Solvabilité II): best estimate plus risk margin; the capital layer is cited-not-specified here. (fetched_ok: no — EUR-Lex WAF challenge)
- **REG-R2** — Règlement délégué (UE) 2015/35: the technical-provision mechanics. (fetched_ok: no)
- **REG-R5** — EIOPA risk-free term structures: the curves a market-consistent valuation would use; no numeric curve reproduced. (fetched_ok: yes)
- **REG-R6** — C. ass. art. R. 343-3: the eleven French life provisions, of which 9–11 exist only for eurocroissance. (fetched_ok: yes)
- **REG-R7** — C. ass. art. R. 343-5 (PRE): no purpose inside an auxiliary account whose assets are at realisation value. (fetched_ok: yes)
- **REG-R13** — CMF art. L. 631-2-1 (HCSF): the power to limit surrender payments for up to six consecutive months. (fetched_ok: yes)
- **REG-R15** — C. ass. arts. A. 132-10 to A. 132-15: the minimum-PB machinery, from which **A. 132-12 excludes art. L. 134-1 contracts**. (fetched_ok: yes)
- **REG-R16** — C. ass. arts. A. 132-16 / A. 132-16-1: the eight-year PPB clock, comparator for the fifteen-year PCDD clock. (fetched_ok: yes)
- **REG-R17** — C. ass. arts. A. 132-1 / A. 132-1-1: the maximum technical rate, a different and stricter object than the A. 134-1 discount ceiling. (fetched_ok: yes)
- **REG-R18** — C. ass. arts. A. 132-2 / A. 132-3: the TMG ceiling any guaranteed rate is subject to. (fetched_ok: yes)
- **REG-R19** — C. ass. art. L. 134-1 and R. 134-1 to R. 134-12: the cross-product anchor, and the note that **no percentages and no time limits** appear in R. 134-4. (fetched_ok: yes)
- **REG-R20** — Décret n° 2019-1437: the cross-product anchor for the PACTE reform and its 1 January 2020 / 1 October 2020 transitional dates. (fetched_ok: yes)
- **REG-R21** — Arrêté du 1er août 2006 (TGH05 / TGF05): the generational annuity tables an annuity option at maturity would use — cited, never shipped. (fetched_ok: yes)
- **REG-R22** — Arrêté du 20 décembre 2005 (TH 00-02 / TF 00-02): the homologated non-annuity tables — cited, never shipped. (fetched_ok: yes)
- **REG-R23** — C. ass. art. A. 335-1 and Annexe: which mortality table a French tariff may use, and the *décalages d'âge*. (fetched_ok: yes, served in a pre-2016 version)
- **REG-R24** — INSEE mortality data: the only freely redistributable French series, and the basis of this library's **[std]** decrement proxies. (fetched_ok: yes)
- **REG-R29** — C. ass. arts. L. 132-5-1 / L. 132-5-2: the thirty-day *renonciation* right. (fetched_ok: yes)
- **REG-R30** — C. ass. arts. A. 132-4 / A. 132-8: the *note d'information* and the *encadré*, which require **maximum** charges to be disclosed but cap nothing — the reason every charge level here is **[std]**. (fetched_ok: yes)
- **REG-R31** — C. ass. arts. L. 132-21 / L. 132-22 / L. 132-23-1: the two-month surrender settlement, and the duty to update art. L. 134-1 information **at least quarterly** and to give a statement one month before term. (fetched_ok: yes)
- **REG-R33** — PRIIPs Règlement (UE) 1286/2014 and AMF DOC-2011-05: the synthetic risk indicator behind the SRI ≤ 2 maturity default. (fetched_ok: partial — the regulation was not retrieved)
- **REG-R40** — CGI art. 125-0 A: the eight-year threshold and the €4 600 / €9 200 abattement that shape surrender timing. (fetched_ok: yes)
- **REG-R41** — CGI arts. 990 I and 757 B: the death-benefit levy and its abatements. (fetched_ok: yes)
- **REG-R44** — Institut des actuaires, NPA 2 *Modèles actuariels*: the standard this documentation, worked example and test suite sit under. (fetched_ok: yes)
- **REG-R45** — IFRS 17: the reporting basis from 2023; the variable fee approach for direct-participating contracts is **[unverified]** here. (fetched_ok: yes, landing page only)

---

## Provenance note

Extraction details — the per-source content notes, the nineteen extracted specification sections,
the cross-insurer variation analysis and the twelve-item gaps register these documents draw on —
live in `_research/eurocroissance.md`; the cross-product regulatory bibliography lives in
`references/regulatory-and-actuarial-references.md`.

Recorded gaps inherited by this specification, visible as [std] or [unverified] tags in the two
documents: **no contractual document exists in the source set** [S10], so charge levels for AXA
and Predica and the **minimum part value for every insurer** are unknown; the "eurocroissance"
**denomination arrêté** appears never to have been issued, so the reserved-name and
8-year-minimum claims [S9] [R21] are [unverified]; the *mémoire*'s statement that PACTE made the
participation-account and asset-performance levies simultaneous, capped at 15 % and 10 %, is
[unverified] against the retrieved R. 134-3 5°, which reads "ou alternativement" and states no
caps [R2] [R13]; the *transfert de richesse* conditions it describes predate décret n° 2025-1333
and are [unverified] against the reinstated R. 134-12 [R7]; its own date and its printed
mortality table ("TH00-05") are [unverified] [R13]; ACPR's 2025 life-market study and Profession
CGP's analysis both returned HTTP 403 (research ids R20 and S11, omitted from this
list because nothing is cited from either); the Légifrance page for ordonnance
n° 2014-696 was not resolved [R22]; and the regulatory mortality tables are cited by name and
arrêté but **never shipped**, the decrement CSVs being [std] proxies built from INSEE data
[REG-R21] [REG-R22] [REG-R23] [REG-R24]. Host behaviour worth recording: `legifrance.gouv.fr`
and `codes.droit.org` serve fully to a plain fetcher, while **ACPR PDFs require `curl` with a
browser User-Agent** — that technique retrieved [R18] and [R19] but still failed on the
2025 life-market study.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-eurocroissance-r1
[R13]: #frlib-eurocroissance-r13
[R18]: #frlib-eurocroissance-r18
[R19]: #frlib-eurocroissance-r19
[R2]: #frlib-eurocroissance-r2
[R21]: #frlib-eurocroissance-r21
[R22]: #frlib-eurocroissance-r22
[R4]: #frlib-eurocroissance-r4
[R7]: #frlib-eurocroissance-r7
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
