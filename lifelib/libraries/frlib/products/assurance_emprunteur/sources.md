# Sources

Source ids, titles, publishers, URLs and retrieval markers are carried over **verbatim** from
`_research/assurance-emprunteur.md`, the citation ground truth for the [S#]/[R#] tags used in
`product-spec.md` and `technical-notes.md`. Ids S1–S14 and R1–R20 are frozen there and are
never renumbered here. Entries the two documents do not cite are omitted, leaving gaps rather
than closing them: **R14, R15 and R20 are omitted** — the Banque de France press release on
the loi Lemoine bilan, the CCSF's December 2016 review of the equivalence avis, and the CCSF
institutional portal, all three of which returned HTTP 403 and none of which any statement in
these documents relies on. No new source was fetched at drafting.

Access date for all citations: **2026-08-26**.

---

## Primary product sources [S#]

(frlib-assurance_emprunteur-s1)=

### S1 — Cardif Libertés Emprunteur, "Cotisations fixes" (notice d'information, janvier 2022)
- Publisher / doc type: CARDIF Assurance Vie (BNP Paribas Cardif), conventions n° 2827/736 (UFEP), administered by Cbp France (Orias 07 009 030); *notice d'information valant conditions générales*, 29 pp.
- URL: https://assurance-de-pret-expert.com/wp-content/uploads/2022/07/Conditions-Generales-Cardif-Liberte-Emprunteur-cotisations-fixes.pdf
- Retrieved: YES (PDF downloaded, full text extracted with PyMuPDF). Third-party broker mirror of the insurer's own January 2022 edition.
- Used for: the level-premium design and the lexique definitions (*capital assuré*,
  *capital restant dû*, *carence*, *franchise*, *quotité*); the guarantee combinations and
  age conditions; the three-of-four PTIA acts test; the 30/60/90/180-day *franchise*, the
  1 095-day ITT cap, the €10 000 monthly cap and the IPP ramp (N−33)/33; IPT paid as the CRD;
  the *barème croisé*; anti-duplication; *perte d'emploi*; exclusions and the *Sérénité+*
  buy-back; the pre-Lemoine cancellation regime.

(frlib-assurance_emprunteur-s2)=

### S2 — Cardif Libertés Emprunteur, "Cotisations variables" (notice d'information, janvier 2022)
- Publisher / doc type: CARDIF Assurance Vie, same conventions and administrator as S1; *notice d'information valant conditions générales*, 29 pp.
- URL: https://assurance-de-pret-expert.com/wp-content/uploads/2022/07/Conditions-Generales-Cardif-Liberte-Emprunteur-cotisations-variables.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the decreasing-premium twin of S1 — premium rebased on the *capital restant dû*
  at the attained age and the partial-early-repayment rule; identical *franchise* set and
  1 095-day cap; IPT paid as the CRD.

(frlib-assurance_emprunteur-s3)=

### S3 — Cardif, "Votre partenaire privilégié en assurance de prêt" (plaquette courtiers, conventions n° 2827/736 et 2828/727)
- Publisher / doc type: BNP Paribas Cardif; brochure for intermediaries (*document à caractère publicitaire*), 16 pp.
- URL: https://www.evassure.fr/wp-content/uploads/2021/07/plaquette-cardif-clecrd.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the statement that the contract is *forfaitaire*; the age-limit grid by
  guarantee; the unisex tariff and €10 file fee; the self-assessment against the 18 CCSF
  criteria and the 11-of-18 plus 4-of-8 rule; IPT "au choix : CRD ou échéances".

(frlib-assurance_emprunteur-s4)=

### S4 — Cardif, "Les 18 critères CCSF / Délégation d'assurance : les exigences de l'organisme prêteur" (web page)
- Publisher / doc type: BNP Paribas Cardif; insurer consumer web page.
- URL: https://www.cardif.fr/assurance-emprunteur/delegation-ade-exigences-organisme-preteur
- Retrieved: YES (HTML fetched).
- Used for: the 11-of-18 plus 4-of-8 rule; the FSI delivered at the first costed simulation
  carrying the guarantees, the *quotité* and the cost estimate; the requirement that an
  equivalence refusal be written, dated, explicit and precisely motivated.

(frlib-assurance_emprunteur-s5)=

### S5 — APRIL, "Assurance de Prêt APRIL — Notice valant conditions générales" (PRT150115)
- Publisher / doc type: APRIL (individual contract distributed through an association); *notice valant conditions générales*, 24 pp.
- URL: https://assurance-de-pret-expert.com/wp-content/uploads/2021/01/Conditions-Generales-ADP-APRIL.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: Décès/PTIA paying the CRD within the *Montant garanti*; the four-of-four PTIA
  acts test; ITT from the 31st/61st/91st/181st day with the two-month relapse rule; IPT ≥66 %
  on the ITT basis and IPP 33 %–65 % at 50 %; the annual re-computation of the premium on the
  guaranteed CRD and attained age; premium waiver pro rata; the *option Prévoyance*.

(frlib-assurance_emprunteur-s6)=

### S6 — APRIL, "Assurance de Prêt APRIL — livret de garanties (Optimum +)"
- Publisher / doc type: APRIL Santé Prévoyance; retail brochure (*document à caractère publicitaire*), 8 pp.
- URL: https://assets.april.fr/prismic/doc-part-april-adp-optimum-plus-livret-garanties.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the *indemnitaire* versus *forfaitaire* explanation and the "own profession"
  versus "any profession" ITT distinction; the *franchise* menu and its residence
  restrictions; the €25 000 monthly and €15 000 000 capital maxima; the 80/85 and 64/71 age
  grid.

(frlib-assurance_emprunteur-s7)=

### S7 — APRIL / AXERIA Prévoyance, "APRIL Assurance de Prêt Optimum + (cotisation variable)" (IPID/DIPA, OPIV012022DIP)
- Publisher / doc type: AXERIA Prévoyance (insurer), APRIL Santé Prévoyance (Orias 07 002 609, manager); standardised insurance product information document, 2 pp.
- URL: https://assets.april.fr/prismic/documents/particuliers/doc-part-april-adp-optimum-plus-document-information-produit-cotisation-variable.pdf?vh=3a7365&func=proxy
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the cleanest published statement of the decreasing-premium design ("le montant
  des cotisations change tous les ans en fonction de l'âge de l'emprunteur et du montant du
  capital restant dû"); the "IPT en capital" versus "IPT en rente" naming; cover-end ages
  90/71/65; the 30-day *renonciation*; the three-month *délai d'attente*.

(frlib-assurance_emprunteur-s8)=

### S8 — APRIL, "Assurance de Prêt Intégrale (Perte d'Emploi)" (notice valant conditions générales, ITGP042023)
- Publisher / doc type: APRIL, conventions MNCA2023P1/P2, PE modules MNAC2023P4 (variable) and MNAC2023P5 (constant); *notice valant conditions générales*, 17 pp.
- URL: https://www.meilleurtaux.com/images/ade/Conditions-Generales/CG_APRIL_Integrale-perte-emploi.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the *perte d'emploi* module's eligibility, 91st-day trigger, €3 500 cap and
  12-month limit; and its article 8, which states the two premium bases verbatim —
  *cotisation variable* on the guaranteed CRD at 1 January with the age attained at
  31 December, *cotisation constante* on the initial *Montant garanti*.

(frlib-assurance_emprunteur-s9)=

### S9 — CNP Assurances, "Assurance de prêt — Note et notice d'information" (contrat de groupe n° A217Y, édition 25_02_A217Y)
- Publisher / doc type: CNP Assurances (RCS Nanterre 341 737 062), subscriber association ASSOCIAREA, administrator Multi-Impact; note + *notice d'information* of a group policy, 23 pp., 2025 edition.
- URL: https://www.meilleurtaux.com/images/ade/Conditions-Generales/Notice_CNP_CI_A217Y_12032025.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: **the chassis of the representative design** — the definitions of *capital
  assuré*, *capital initial* and *capital restant dû*; the guarantee table with each
  guarantee's age ceiling and maximum benefit (Décès 85, PTIA 70, ITT/IPT/IPP/MTT 70, GAF
  67); the 30/60/90/120/180-day *franchise*; the IPT/IPP mechanics with the published *taux
  global d'incapacité* cross table and its worked example; the <90-day relapse rule;
  *quotité* in 1 % steps with the 100 %/40 % example; the €5 000 000 *encours* maximum; the
  medical-formality rule and 6-month questionnaire validity; the premium on the *capital
  initial* at the age at adhesion; the 90-day notification deadline; the loi Lemoine
  cancellation procedure; the *garantie aide à la famille*.

(frlib-assurance_emprunteur-s10)=

### S10 — CNP Assurances / BPCE Vie, "Contrat d'assurance de groupe en couverture de prêts n° A340G" (édition 21_06_A340G)
- Publisher / doc type: CNP Assurances and BPCE Vie (Natixis Assurances), subscriber BPCE (Orias 08045100), distributed by Banque Populaire; note + *notice d'information*, 14 pp.
- URL: https://www.img.banquepopulaire.fr/app/uploads/sites/24/2022/03/23094728/cg-assurances-emprunteur-a340g.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: **the indemnitaire/forfaitaire distinction** — the four-way benefit rule by
  professional status and the definitions of *revenu de référence* and *revenu de
  remplacement*; premiums "en pourcentage du capital initial du prêt **ou** du capital restant
  dû"; the 90-day standard *franchise* with a 30-day option; consolidation "au plus tard trois
  ans après le début de son Incapacité Temporaire Totale"; the flat-50 % IPP; cover ending at
  80 for Décès and 67 for the rest.

(frlib-assurance_emprunteur-s11)=

### S11 — MAIF VIE, "Avantage Emprunteur — Notice d'information"
- Publisher / doc type: MAIF VIE, subscriber association "Association pour l'union et le recours en assurances" (Meyreuil), administrator Multi-Impact; *notice d'information*, 30 pp.
- URL: https://www.meilleurtaux.com/images/ade/Conditions-Generales/Notice_MAIF.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: a mutual-insurer contract with a single fixed 90-day *franchise*; "l'indemnité
  garantie est forfaitaire, égale aux mensualités venant à échéance"; the 1 095-day ITT
  maximum; IPT ≥66 % paid as instalments and the IPP formula (taux − 33)/33; guarantee-end
  ages 85/70/67; the premium on the *capital initial*, fixed for the term and waived
  throughout a claim.

(frlib-assurance_emprunteur-s12)=

### S12 — MetLife, "SUPER NOVATERM CRÉDIT — Note d'information" (NISNC19, mars 2017) with the conditions générales
- Publisher / doc type: MetLife (France branch); note d'information under arts. L. 132-5-2 and A. 132-4 C. ass. plus *conditions générales*, 13 pp.
- URL: https://assurance-de-pret-expert.com/wp-content/uploads/2021/01/Conditions-Generales-Super-Novaterm-Credit.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the structural outlier — an **individual** branch-20 term-life contract paying a
  scheduled *capital garanti* with the lender beneficiary only "à concurrence des sommes
  restant dues"; ITT as *forfaitaire* daily indemnities after a 15/30/60/90/180-day
  *franchise* for at most 1 095 days; IPT ≥66 % paying the death capital.

(frlib-assurance_emprunteur-s13)=

### S13 — CNP Assurances / CNP IAM / MFPrévoyance, "Notice d'information du contrat de groupe n° 7371 M" (Banque Française Mutualiste)
- Publisher / doc type: coinsurance, CNP Assurances and CNP IAM as *apériteur* (10 %) and MFPrévoyance SA (90 %), subscriber Banque Française Mutualiste; *notice d'information*, 12 pp.
- URL: https://www.assurance-emprunteur.bzh/sites/kelemprunteur/files/insurance/cgv-banque-francaise-mutualiste-fr.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: **the *nivelé* premium statement that drives the model's premium rule** — "Le
  taux de prime a été nivelé sur la durée du prêt ; par conséquent, la cessation de ces
  garanties n'a pas d'incidence sur le montant de la prime"; branches 1, 2 and 20 of art.
  R. 321-1; whole instalments with no *prorata temporis*; the social-security-anchored ITT
  trigger; no IPT and no IPP; cover ending at 75 for Décès and 65 for PTIA and ITT.

(frlib-assurance_emprunteur-s14)=

### S14 — Crédit Agricole, "Notice d'information ADI – P / 103-2016" (group borrower policy)
- Publisher / doc type: Crédit Agricole (Assurance Décès Invalidité); *notice d'information* of a bancassurance group policy.
- URL: https://www.ce-g3-esimulca-enligne.credit-agricole.fr/pep//resources/pdf/info-assurance.pdf
- Retrieved: **NO (HTTP 502 Bad Gateway)**. fetched_ok = false.
- Used for: nothing substantive — cited once, in `product-spec.md`, to record that the
  largest reported writer of the risk is absent from the sample.

---

## Regulatory and actuarial references [R#] (product research file numbering)

(frlib-assurance_emprunteur-r1)=

### R1 — LOI n° 2022-270 du 28 février 2022 ("loi Lemoine")
- Publisher / doc type: Légifrance (Journal officiel); statute, 11 articles.
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045268729
- Retrieved: YES.
- Used for: *résiliation à tout moment* (art. 1); explicit motivated refusals (art. 2); the
  annual reminder duty and its €3 000 / €15 000 fines (art. 3); eight-year retention (art. 4);
  the ten-business-day lender answer (art. 5); entry into force 1 June 2022 / 1 September 2022
  (art. 8); the five-year *droit à l'oubli* cap (art. 9); the questionnaire suppression
  (art. 10).

(frlib-assurance_emprunteur-r2)=

### R2 — Code des assurances, art. L. 113-2-1
- Publisher / doc type: Légifrance; statutory code article, version in force from 1 June 2022.
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045271000/2026-04-29
- Retrieved: YES.
- Used for: the two **cumulative** conditions of the questionnaire waiver — insured share of
  the cumulative credit *encours* not exceeding €200 000 per insured, and repayment falling
  before the insured's 60th birthday.

(frlib-assurance_emprunteur-r3)=

### R3 — Code des assurances, art. L. 113-12-2
- Publisher / doc type: Légifrance; statutory code article, version in force from 1 June 2022.
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045271930
- Retrieved: YES.
- Used for: cancellation at any time from signature of the art. L. 313-24 loan offer; effect
  ten days after the insurer receives the lender's acceptance, or at the substitute's
  effective date if later; no cancellation on refusal; the tie to art. L. 313-1 1° credits.

(frlib-assurance_emprunteur-r4)=

### R4 — Code de la consommation, arts. L. 313-8 to L. 313-10 (borrower-insurance information)
- Publisher / doc type: Légifrance; statutory code sub-section.
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069565/LEGISCTA000032222229/
- Retrieved: YES.
- Used for: the three mandatory cost presentations — the TAEA, the euro total over eight
  years and over the full term, and the euro cost per instalment period; the duty to hand over
  the FSI and the cancellation notice; the €75 000 FSI threshold.

(frlib-assurance_emprunteur-r5)=

### R5 — Code de la consommation, arts. R. 313-8 to R. 313-10 (content of the fiche standardisée)
- Publisher / doc type: Légifrance; regulatory code sub-section (3 December 2025 view).
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069565/LEGISCTA000032807522/2025-12-03
- Retrieved: YES.
- Used for: the five heads of FSI content fixed by R. 313-9, including the *quotité* and the
  TAEA for the whole loan per art. R. 314-12; and R. 313-10, requiring the sheet to be given to
  each borrower and co-borrower separately.

(frlib-assurance_emprunteur-r6)=

### R6 — Code de la consommation, art. R. 314-12 (definition of the TAEA)
- Publisher / doc type: Légifrance; regulatory code article, version in force from 1 October 2016.
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032807626
- Retrieved: YES.
- Used for: the operative definition the worked TAEA implements — the difference between the
  TAEG computed assuming the proposed insurance is entirely required and the TAEG computed
  assuming no insurance is required, both under arts. R. 314-1 to R. 314-10.

(frlib-assurance_emprunteur-r7)=

### R7 — Code de la consommation, art. L. 313-30
- Publisher / doc type: Légifrance; statutory code article, version in force 1 June 2022.
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045271935
- Retrieved: YES.
- Used for: the equivalence rule — the lender may not refuse another contract presenting "un
  niveau de garantie équivalent", and any refusal must be explicit and state all its reasons.

(frlib-assurance_emprunteur-r8)=

### R8 — Code de la consommation, Section 5 (arts. L. 313-24 to L. 313-39), read for L. 313-29, L. 313-31 and L. 313-32
- Publisher / doc type: Légifrance; statutory code section.
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069565/LEGISCTA000032222201
- Retrieved: YES.
- Used for: the notice in the credit contract and the rule that risk definitions and pricing
  may not change without the borrower's agreement (L. 313-29); the "délai de dix jours ouvrés"
  and the fee-free amendment restating the TAEG (L. 313-31); the prohibition on changing the
  loan rate or credit conditions or charging any fee (L. 313-32).

(frlib-assurance_emprunteur-r9)=

### R9 — Arrêté du 29 avril 2015 (format and content of the fiche standardisée d'information)
- Publisher / doc type: Légifrance (consolidated LODA text with the annexed FSI model); ministerial order with an annexed template.
- URL: https://www.legifrance.gouv.fr/loda/id/JORFTEXT000030555752
- Retrieved: YES (consolidated text and the annex's part-by-part structure read; the annex is a form template, so retrieval yields headings and fields rather than prose).
- Used for: the eight-part FSI model, in particular **part 4** — the lender's minimum required
  guarantees with a *quotité* box for each of Décès, PTIA, ITT, IPT, IPP and *perte d'emploi*,
  which is where a lender's *quotité* floor is expressed — and part 7, the cost estimate.

(frlib-assurance_emprunteur-r10)=

### R10 — Arrêté du 27 mai 2022 modifiant l'arrêté du 29 avril 2015 (FSI)
- Publisher / doc type: Légifrance (Journal officiel); ministerial order, three operative articles, in force 1 June 2022.
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045833541
- Retrieved: YES.
- Used for: the statement that the invalidity guarantee is independent of the social-security
  notion of invalidity; the new part 7.2, the cost over the first eight years; the rewritten
  part 8 carrying the questionnaire exemption and the switching right.

(frlib-assurance_emprunteur-r11)=

### R11 — CCSF, "Avis sur l'équivalence du niveau de garantie en assurance emprunteur", 13 janvier 2015, with its annexed *liste de place*
- Publisher / doc type: Comité consultatif du secteur financier (secretariat at the Banque de France); formal opinion with an annexed criteria list, 8 pp.
- URL: https://www.moneyvox.fr/r/CCSF/CCSF-2015-assurance-emprunteur.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Third-party mirror — the Banque de France copies of the CCSF corpus all returned HTTP 403.
- Used for: the three-step equivalence method; the rule that each lender chooses **at most
  11** of the 18 criteria plus **at most 4** of the 8 *perte d'emploi* criteria and must state
  the required value, "par exemple son caractère forfaitaire ou indemnitaire"; the *fiche
  personnalisée*; the criteria themselves, including the ≤30/≤60/≤90/≤120/≤180-day *franchise*
  boxes and the IPP-from-33 % criterion.

(frlib-assurance_emprunteur-r12)=

### R12 — CCSF, "Rapport annuel 2023", chapter 1.1 "L'assurance emprunteur"
- Publisher / doc type: Comité consultatif du secteur financier, copy served by vie-publique.fr; annual report, 94 pp.
- URL: https://www.vie-publique.fr/files/rapport/pdf/298146.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the portfolio split by contract type (72.2 / 4.4 / 16.0 / 7.4 at 31 May 2023);
  substitution requests 99 265 → 181 600 between H1 2021 and H1 2023 and ~215 000 external
  alternative contracts added in 17 months; acceptance rates 88 %–90 % and 70 %–87 %; claim
  declines by guarantee and contract type, and the finding that 50 %–75 % of external-insurer
  declines are mis-declarations including "maximum cover age exceeded"; the 2019→2023 tariff
  movements; the questionnaire-waiver take-up (58.5 %, 23 %, 31 %) and the ~10 % repricing of
  contracts without medical selection; the CSP1 skew; the *garantie aide à la famille* avis.

(frlib-assurance_emprunteur-r13)=

### R13 — CCSF, "Bilan de l'assurance emprunteur — Rapport adressé au Parlement" (décembre 2023)
- Publisher / doc type: CCSF / Banque de France; report to Parliament under art. 11 of the loi Lemoine.
- URL: https://www.banque-france.fr/system/files/import/ccsf/medias/documents/bilan_ae_2023.pdf
- Retrieved: **NO (HTTP 403, retried once, 403 again)**. fetched_ok = false.
- Used for: recording, in `product-spec.md`, that this report was never read — so the
  widely-circulated 2024/2025 figures (22.15 m contracts, €6.830 bn premiums, 496 654
  substitution requests, 93.91 % acceptance, 17.48 % alternative share) are **[unverified]**.
  Its conclusions enter these documents only through [R12].

(frlib-assurance_emprunteur-r16)=

### R16 — Code de la santé publique, art. L. 1141-5 (droit à l'oubli and the AERAS grille)
- Publisher / doc type: Légifrance; statutory code article, version in force 2 March 2022.
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045272010
- Retrieved: YES.
- Used for: the statutory cap — the delay beyond which no medical information on cancers or
  hepatitis C may be collected may not exceed **five years** from the end of the therapeutic
  protocol.

(frlib-assurance_emprunteur-r17)=

### R17 — Convention AERAS, "Document d'information AERAS" (décembre 2023)
- Publisher / doc type: Convention AERAS (s'Assurer et Emprunter avec un Risque Aggravé de Santé); official information document for applicants, 2 pp.
- URL: https://www.aeras-infos.fr/files/live/sites/aeras/files/contributed/docs/Document%20Information%20AERAS%20d%C3%A9cembre%202023.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the *droit à l'oubli* conditions and the 71st-birthday term limit; the *grille de
  référence* scope (insured share ≤ €420 000, term before the 71st birthday), list I setting
  shorter delays and list II capping surcharges by guarantee. The grid itself was **not
  retrieved**, so no pathology-specific delay is quoted anywhere in these documents.

(frlib-assurance_emprunteur-r18)=

### R18 — France Assureurs, "L'assurance prévoyance en 2024" (étude, juillet 2025)
- Publisher / doc type: France Assureurs, Direction Statistiques & Recherche Économique; annual market study, 25 pp.
- URL: https://www.franceassureurs.fr/wp-content/uploads/lassurance-prevoyance-en-2024.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the narrow "contrats emprunteurs (garantie décès)" line — 5 223 thousand
  contracts at end-2024, €979 m of premiums and €330 m of benefits — with the caveat that it
  covers only the death guarantee of individual-adhesion contracts written by Code des
  assurances undertakings and is not a market total.

(frlib-assurance_emprunteur-r19)=

### R19 — Code de la consommation, art. R. 313-8
- Publisher / doc type: Légifrance; regulatory code article, version in force 1 July 2016.
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032807524
- Retrieved: YES.
- Used for: the rule that the FSI states the principal characteristics of the insurance
  clearly and legibly "dont le modèle est annexé au présent code" — the link between the
  statutory duty and the annexed template of [R9].

---

## Cross-product references ([REG-R#])

Cited with the [REG-R#] prefix to avoid collision with the product research file's own
R-numbering. Full annotated entries — titles, publishers, URLs, retrieval markers, access
date 2026-08-26 — live in `references/regulatory-and-actuarial-references.md`, whose R1–R49
numbering is frozen. Entries cited by the two documents in this directory. The Solvabilité II
directive itself (REG-R1) is deliberately **not** cited: it could not be fetched, and that
library's own rule is to cite REG-R4 — the EIOPA framework page that was — for any statement
of Solvency II fact.

| Tag | Short title | Why this product cites it | Retrieval status |
|---|---|---|---|
| REG-R2 | Règlement délégué (UE) 2015/35 | why no cost-of-capital or lapse-shock figure here is sourced | not fetched (same challenge) |
| REG-R4 | EIOPA — Solvency II framework page | the authority on which the best-estimate rule is stated | fetched |
| REG-R5 | EIOPA — risk-free interest rate term structures | the curve a reader applies to these cash flows; the model uses a flat [std] rate | fetched |
| REG-R6 | C. ass. art. R. 343-3 — eleven technical provisions | the *provision mathématique* and *provision pour égalisation* an ADE book touches | fetched |
| REG-R10 | CMF art. L. 612-1 — the ACPR | the supervisor; no ACPR document on this product was obtainable | fetched |
| REG-R22 | Arrêté du 20 décembre 2005 — TH 00-02 / TF 00-02 | the homologated non-annuity tables the Décès and PTIA legs sit on | fetched |
| REG-R23 | C. ass. art. A. 335-1 and its Annexe | which mortality basis a French tariff may use, and the *décalage d'âge* schedules | fetched (older version served) |
| REG-R24 | INSEE — mortalité, espérance de vie | the only redistributable French mortality data, behind the [std] proxy tables | fetched |
| REG-R32 | Devoir de conseil — L. 132-27-1 (abrogated) and the DDA | the distribution frame for an advised borrower-insurance sale | fetched (article); DDA substance [unverified] |
| REG-R35 | Loi n° 2022-270 (loi Lemoine) | the same statute as [R1], verified article by article in the shared library | fetched |
| REG-R36 | C. consommation arts. L. 313-8 / L. 313-30 | the TAEA and the eight-year / full-term euro cost an ADE model must produce | fetched |
| REG-R37 | France Assureurs — *Statistiques Convention AERAS 2023* | the only public French price point (1.01 % / 0.65 % of initial capital) and the 69/30/2 guarantee split | fetched |
| REG-R43 | Institut des actuaires — NPA 1 | the professional frame for the assumption-setting these notes make explicit | fetched |
| REG-R44 | Institut des actuaires — NPA 2 (modèles actuariels) | the standard against which this documentation and worked example are judged | fetched |
| REG-R45 | IFRS 17 *Insurance Contracts* | the accounting layer that consumes the same projections | fetched |

---

## Provenance note

Extraction details live in `_research/assurance-emprunteur.md`, which records which fact came
from which source and every [unverified] flag. The caveats that travel with this product:

- **The whole Banque de France / CCSF estate refused automated fetches** — HTTP 403 on every
  attempt [R13] — so the two CCSF documents used here come from mirrors, the 2015 avis via
  moneyvox [R11] and the 2023 annual report via vie-publique [R12]. **No ACPR document was
  retrieved at all**, and no statement about supervisory expectations on this product is made.
- **No reserving, prudential or tax source was retrieved.** The *nivelé* premium design is
  stated in a contract [S13], but how a French insurer reserves the resulting increasing-risk
  pattern, and the *taxe spéciale sur les conventions d'assurance* treatment of the death
  versus the incapacity components, are both **[unverified]** here.
- **No decrement, incidence or termination table exists in this corpus**, and no standard-risk
  rate card or filled-in FSI was retrieved. Every decrement, the premium rate, the expense
  assumptions and the discount rate in `technical-notes.md` are therefore **[std]**, and the
  worked example's TAEA and cost totals are computed from those [std] inputs, not quoted.
- **Mirror hosting.** S1, S2, S5 and S12 were retrieved from `assurance-de-pret-expert.com`,
  S8, S9 and S11 from `meilleurtaux.com`, S3 from `evassure.fr` and S13 from
  `assurance-emprunteur.bzh` — intermediary mirrors of the insurers' own documents. Publisher,
  document code and edition are recorded above for re-verification.
- **Vintage mismatch and sampling gap.** The Cardif documents [S1] [S2] [S3] are January 2022
  editions describing the **pre-Lemoine** cancellation regime and citing the repealed art.
  L. 312-9 — their guarantee mechanics are current, their cancellation clauses are not — and
  the APRIL notice [S5] is an older edition than the Optimum + material [S6] [S7], the two
  disagreeing on the death cover-end age (85 against 31 December of the 90th birthday year),
  which is recorded rather than resolved; only [S9] (2025) and [S8] (2023) are demonstrably
  post-Lemoine. Crédit Agricole's notice [S14] returned HTTP 502, Generali, Suravenir, MNCAP,
  AFI-ESCA and Swiss Life were not sampled, and the *contrat alternatif bancaire* segment has
  no document here at all.
- **Two derivations, labelled as such.** The *barème croisé* formula N = (IF² × IP)^(1/3)
  reproduces every printed cell of both retrieved grids [S1] [S9] and both worked examples,
  but **neither contract states it** — it is a fitted reconstruction. And the claim that the
  co-borrowers' *quotités* must total at least 100 % is **[unverified]** as an
  insurance-contract rule: it is a lender requirement expressed through the FSI and the CCSF
  *fiche personnalisée* [R9] [R11].

Standardizations marked **[std]** in `product-spec.md` and `technical-notes.md` are introduced
at drafting and are attributable to no source. The [std] decrement tables in
`technical-notes.md` are placeholders shaped like the quantities a real basis would carry;
they are **not** TH 00-02 / TF 00-02 values and carry no actuarial authority.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-assurance_emprunteur-r1
[R11]: #frlib-assurance_emprunteur-r11
[R12]: #frlib-assurance_emprunteur-r12
[R13]: #frlib-assurance_emprunteur-r13
[R9]: #frlib-assurance_emprunteur-r9
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
