# Borrower's protection insurance (assurance emprunteur) — research notes (France)

Research notes for the French *assurance emprunteur* (ADE) — the death, disability and
incapacity cover attached to a mortgage (*crédit immobilier*), sold either as the lender's own
group policy (*contrat groupe*) or as an individual policy from a third-party insurer
(*délégation d'assurance*). These notes are the citation ground truth for the frlib
assurance-emprunteur product documents: source ids S1..S14 and R1..R20 below are frozen —
never renumber.

Access date for all citations: 2026-08-26.

Citation discipline: every extracted fact is tagged `[S#]` or `[R#]` pointing at a document
that was actually fetched and read. `[unverified]` marks statements from general knowledge or
from secondary summaries of documents that could not be retrieved. Where a fetch failed the
failure is recorded and the item is kept only as a known reference (fetched_ok = false).

Language note: French terms of art are kept in French and glossed on first use — *quotité*
(the share of the loan insured on one life), *franchise* (the deductible waiting period on an
incapacity claim), *carence* (the initial waiting period before a guarantee can be triggered
at all), *capital restant dû* / CRD (outstanding principal), *échéance* (a loan instalment),
*notice d'information* (the group-policy booklet handed to the member), *fiche standardisée
d'information* / FSI (the mandatory standardised pre-sale sheet), *conditions générales*
(policy conditions of an individual contract).

---

## Primary sources

### S1 — BNP Paribas Cardif, "Cardif Libertés Emprunteur — Cotisations fixes" (notice d'information, janvier 2022)
- Publisher: CARDIF Assurance Vie / BNP Paribas Cardif; group conventions n° 2827/736 (UFEP);
  administered by Cbp France (Orias 07 009 030)
- Doc type: notice d'information valant conditions générales, 29 pp.
- URL: https://assurance-de-pret-expert.com/wp-content/uploads/2022/07/Conditions-Generales-Cardif-Liberte-Emprunteur-cotisations-fixes.pdf
- Retrieved: YES (PDF downloaded, full text extracted with PyMuPDF). Third-party broker mirror;
  document is the insurer's own January 2022 edition.
- Content: full notice for the *cotisations fixes* (level-premium) variant. Lexique with
  contractual definitions of *accident*, *capital assuré (capital initial)*, *capital restant
  dû*, *carence*, *consolidation*, *franchise*, *fumeur*, *quotité assurée*, *sinistre*;
  eligible loans (amortising fixed/variable rate, in fine, prêt à paliers, prêt relais ≤3 yrs,
  private and vendor loans), loan duration 1–35 years extendable by 5 without exceeding 40;
  four guarantee combinations A–D (Décès / +PTIA / +ITT+IPT / +IPP); age conditions at
  adhesion and guarantee-end ages; guarantee definitions for Décès, PTIA, IPT, IPP, ITT, PE;
  the *barème croisé* invalidity table (functional × professional incapacity); ITT franchise
  choice 30/60/90/180 days, 1 095-day maximum, €10 000 monthly cap, mi-temps thérapeutique at
  50 % capped €5 000 for 180 days, relapse rules; IPP benefit formula (N−33)/33; option
  Prévoyance, option Sérénité+, option Perte d'emploi; GIS (garantie invalidité spécifique)
  under the AERAS convention; premium-waiver during ITT/IPP; premium drivers and the guarantee
  that net-of-tax premiums do not change; the pre-Lemoine résiliation regime (12-month Hamon
  window and annual Bourquin anniversary).

### S2 — BNP Paribas Cardif, "Cardif Libertés Emprunteur — Cotisations variables" (notice d'information, janvier 2022)
- Publisher: CARDIF Assurance Vie / BNP Paribas Cardif; same conventions and administrator
- Doc type: notice d'information valant conditions générales, 29 pp.
- URL: https://assurance-de-pret-expert.com/wp-content/uploads/2022/07/Conditions-Generales-Cardif-Liberte-Emprunteur-cotisations-variables.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the *cotisations variables* twin of S1. Structurally identical guarantee wording,
  franchise set (30/60/90/180), 1 095-day ITT cap and €10 000 monthly cap. The material
  difference is the premium basis: the premium depends on *l'âge de l'assuré* (attained, not
  age at inception as in S1) and, on partial early repayment, the new premium base is the
  *capital restant dû* in force before the repayment less the amount repaid — where S1 rebases
  on the original *capital emprunté*. Also extends ITT cover wording to rental instalments
  ("l'échéance de prêt ou du loyer") for lease-purchase financing.

### S3 — BNP Paribas Cardif, "Cardif Libertés Emprunteur — Votre partenaire privilégié en assurance de prêt" (broker plaquette, conventions n° 2827/736 et 2828/727)
- Publisher: BNP Paribas Cardif (document à caractère publicitaire destiné aux courtiers)
- Doc type: product brochure for intermediaries, 16 pp.
- URL: https://www.evassure.fr/wp-content/uploads/2021/07/plaquette-cardif-clecrd.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: states plainly that Cardif Libertés Emprunteur is "un contrat **forfaitaire** à
  cotisations variables ou à cotisations fixes"; age-limit grid at adhesion and at cover end by
  guarantee; carence and franchise grid; the four options (Sérénité+, Prévoyance, Perte
  d'emploi, Extension de garantie to 70); a two-page mapping of the contract against the **18
  CCSF criteria**, with the explicit statement that a lender may impose at most 11 of the 18,
  plus at most 4 of the 8 perte d'emploi criteria; unisex tariff; €10 file fee; age computed by
  difference of calendar years; benefit summary — Décès/PTIA pay the CRD, ITT pays the
  instalment (or interest only on in fine / relais), **IPT at the insured's choice pays either
  the CRD or the instalments**, IPP pays instalments scaled by the invalidity rate.

### S4 — Cardif, "Les 18 critères CCSF pour comparer votre assurance emprunteur / Délégation d'assurance : les exigences de l'organisme prêteur" (web page)
- Publisher: BNP Paribas Cardif
- Doc type: insurer consumer web page
- URL: https://www.cardif.fr/assurance-emprunteur/delegation-ade-exigences-organisme-preteur
- Retrieved: YES (HTML fetched).
- Content: confirms the 11-of-18 + 4-of-8 rule; describes the FSI as delivered at the first
  costed simulation and as carrying the proposed guarantees, the *quotité*, the personalised
  cost estimate and the right to insure elsewhere; states the equivalence test is "un niveau de
  garanties au moins équivalent" and that a refusal must be written, dated, explicit and
  precisely motivated; notes the loi Lemoine right to cancel *à tout moment* with no notice
  period. The page does not describe the CCSF *fiche personnalisée* separately.

### S5 — APRIL, "Assurance de Prêt APRIL — Notice (valant conditions générales)" (PRT150115)
- Publisher: APRIL (individual contract distributed through an association)
- Doc type: notice valant conditions générales, 24 pp. (document code PRT150115)
- URL: https://assurance-de-pret-expert.com/wp-content/uploads/2021/01/Conditions-Generales-ADP-APRIL.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: guarantee-by-guarantee wording. Décès/PTIA pay the *capital restant dû* shown on the
  amortisation schedule, capped at the *Montant garanti*; death cover ends at 31 December of the
  85th birthday year; PTIA must be consolidated before pension entitlement and at the latest at
  31 December of the 70th birthday year while still working. ITT pays the falling instalments
  from the 31st, 61st, 91st or 181st day per the franchise chosen; half-time therapeutic return
  pays 50 % for up to six months after at least two months of ITT indemnification; a relapse
  within two months is the same claim with no fresh franchise. IPT requires a combined
  invalidity rate ≥66 % from a double-entry functional × professional table; IPP requires
  33 %–65 % and pays 50 % of the ITT/IPT insured instalment. Options Confort and Confort + buy
  back the disco-vertebral and psychiatric exclusions. Option Prévoyance covers the uninsured
  *quotité* for a chosen beneficiary, combined ≤100 %. Premium base is the guaranteed loan
  amount, but at 1 January of each insurance year the premium is recomputed on the **capital
  restant dû garanti** and the age attained at 31 December; premiums are waived pro rata during
  ITT/IPT/IPP claims.

### S6 — APRIL, "Assurance de Prêt APRIL — livret de garanties (Optimum +)"
- Publisher: APRIL Santé Prévoyance
- Doc type: retail product brochure (document à caractère publicitaire), 8 pp.
- URL: https://assets.april.fr/prismic/doc-part-april-adp-optimum-plus-livret-garanties.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: a plain-language explanation of the *indemnitaire* versus *forfaitaire* indemnity
  bases and of the "impossibility to exercise **any** profession" versus "**her/his** profession"
  ITT definitions, with a worked illustration (a baker with a broken arm). Guarantee table:
  Décès/PTIA pay the CRD; ITT and IPT pay the instalments after the franchise, franchise choice
  30/60/90/180 days (90/180 only for the non-working and for DROM / EU / EEA / UK residents);
  IPP 33 %–65 % pays half the ITT/IPT instalment at the same *quotité* and franchise; maximum
  monthly instalment insured €25 000 (€6 000 in the DROM), maximum capital €15 000 000
  (€5 000 000 in the DROM), €2 500 000 for the medical-professions invalidity option. Age grid:
  subscribe up to 80 and be indemnified to 85 for Décès/PTIA; subscribe up to 64 and be
  indemnified to 71 for ITT/IPT/IPP. Also records the legislative history as the market
  understood it — loi Lagarde (Sept. 2010), loi Hamon (11.5 months from the loan offer),
  the 2013/2014 banking-separation rule (10 days for the lender's answer, no change to the loan
  rate, no delegation fee), AERAS and *droit à l'oubli*.

### S7 — APRIL / AXERIA Prévoyance, "Assurance Emprunteur — Document d'information sur le produit d'assurance : APRIL ASSURANCE DE PRET OPTIMUM + (cotisation variable)" (OPIV012022DIP)
- Publisher: AXERIA Prévoyance (insurer), APRIL Santé Prévoyance (Orias 07 002 609, manager)
- Doc type: IPID / DIPA (standardised insurance product information document), 2 pp.
- URL: https://assets.april.fr/prismic/documents/particuliers/doc-part-april-adp-optimum-plus-document-information-produit-cotisation-variable.pdf?vh=3a7365&func=proxy
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the cleanest published statement of the decreasing-premium design — "Le montant des
  cotisations d'assurance change tous les ans en fonction de l'âge de l'emprunteur et du montant
  du capital restant dû." Guarantee summary: Décès and PTIA pay the CRD; ITT pays the
  instalments, 50 % for up to 6 months on a half-time therapeutic return; **IPT pays either the
  CRD ("IPT en capital") or the instalments ("IPT en rente")** at ≥66 %; IPP pays 50 % of the
  instalment for 33 %–65 %. Principal exclusions (suicide in year 1, prior conditions, unlisted
  sports, aerial and motorised sports, psychiatric and disco-vertebral conditions unless bought
  back). Restrictions: a 3-month *délai d'attente* on illness claims for loans already running
  and previously uninsured; ITT franchise 30/60/90/180 days. Cover ends at 31 December of the
  90th birthday year for Décès, of the 71st for PTIA, and at retirement and at the latest
  31 December of the 65th (71st with the "Extension 65+" option) for the other guarantees.
  Cancellation *à tout moment* from signature of the loan offer for non-professional mortgages.

### S8 — APRIL, "Notice (valant conditions générales) — APRIL Assurance de Prêt Intégrale (Perte d'Emploi)" (ITGP042023)
- Publisher: APRIL (conventions MNCA2023P1 / MNCA2023P2; PE modules MNAC2023P4 variable and
  MNAC2023P5 constant)
- Doc type: notice valant conditions générales, 17 pp.
- URL: https://www.meilleurtaux.com/images/ade/Conditions-Generales/CG_APRIL_Integrale-perte-emploi.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the *perte d'emploi* module only. Eligibility 18–60 at 31 December of the year cover
  starts, continental France, salaried on a single open-ended contract (CDI), minimum insured
  loan €18 000, PE *quotité* ≤ the ITT/IPT *quotité*. Benefit starts on the 91st consecutive day
  of *chômage total* with unemployment benefit in payment, requires ≥12 months' CDI seniority at
  the loss, is capped at €3 500 per month across all insured loans, and runs for at most 12
  months (continuous or not) per redundancy. Detailed franchise-suspension and
  return-to-work rules with worked timelines. Article 8 states the two premium bases verbatim:
  *cotisation variable* — first premium on the initial *Montant garanti*, later premiums on the
  guaranteed *capital restant dû* at 1 January and the age attained at 31 December;
  *cotisation constante* — premium always on the initial *Montant garanti* at the age at
  inception.

### S9 — CNP Assurances, "Assurance de prêt — Note et notice d'information" (contrat d'assurance de groupe en couverture de prêts n° A217Y, edition 25_02_A217Y)
- Publisher: CNP Assurances (RCS Nanterre 341 737 062); subscriber association ASSOCIAREA;
  administrator Multi-Impact
- Doc type: note d'information + notice d'information of a group policy, 23 pp. (2025 edition)
- URL: https://www.meilleurtaux.com/images/ade/Conditions-Generales/Notice_CNP_CI_A217Y_12032025.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the most complete and most recent group-contract source in this set, and the only one
  that already carries the CCSF *garantie aide à la famille*. Definitions of *capital assuré*,
  *capital initial*, *capital restant dû*, *franchise*, *quotité assurée*. Guarantee table with
  the age ceiling and the maximum benefit for each guarantee (Décès to 85 = CRD; PTIA to 70 =
  CRD; ITT to 70 = 100 % of the monthly instalment; IPT to 70 = 100 %; IPP to 70 = 50 %;
  mi-temps thérapeutique to 70 = 50 %; invalidité AERAS to 70 = 100 %; GAF to 67 = 50 %).
  Franchise levels 30/60/90/120/180 days spelled out day by day. Full IPT/IPP mechanics with the
  published *taux global d'incapacité* cross table and its worked example. ITT relapse: no new
  franchise if the interruption was under 90 days. *Quotité* chosen in 1 % steps from 1 % to
  100 % per insured, applying to every guarantee, with a two-borrower worked example (100 % and
  40 %). Maximum *encours* €5 000 000 per insured. Loans: amortising up to 35 years, in fine up
  to 10 years, relais up to 3 years, euro-denominated only. Medical formalities: none where the
  insured share of the cumulative credit *encours* does not exceed €200 000 and repayment falls
  before the 60th birthday; otherwise a health questionnaire valid 6 months. Premium: a rate set
  by age at adhesion, loan term, loan type, guarantees and options, **applied to the capital
  initial**; partial early repayment rebases on the guaranteed CRD less the amount repaid.
  Article 13 restates the loi Lemoine right to cancel at any time from signature of the loan
  offer, with the ten-business-day lender decision and the effective-date rule.

### S10 — CNP Assurances / BPCE Vie, "Contrat d'assurance de groupe en couverture de prêts n° A340G" (edition 21_06_A340G, distributed by Banque Populaire)
- Publisher: CNP Assurances and BPCE Vie (Natixis Assurances), subscriber BPCE (Orias 08045100)
- Doc type: note + notice d'information of a bancassurance group policy, 14 pp.
- URL: https://www.img.banquepopulaire.fr/app/uploads/sites/24/2022/03/23094728/cg-assurances-emprunteur-a340g.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the reference *contrat groupe bancaire* of this set, and the single most important
  source for the indemnitaire/forfaitaire distinction. Premiums "calculées en pourcentage du
  capital initial du prêt **ou** du capital restant dû … et proportionnellement à la quotité
  d'assurance", rate shown in the loan offer. Cover matrix by loan type (mortgage / works /
  consumer / zero-rate / rental investor / in fine / relais / non-resident) showing which of the
  three options — 30-day franchise, IPP, *Prestation Forfaitaire* — are available; consumer
  loans ≤ €21 500 get Décès-PTIA only. ITT/IPT benefit is **indemnitaire by default for
  employees, civil servants and jobseekers drawing benefit** — the monthly benefit is the
  instalment scaled by the *quotité* but "dans tous les cas limitée à la perte de revenu",
  defined as *revenu de référence* (average net taxable income and allowances over the 12 months
  before the stoppage) minus *revenu de remplacement* (all social-security, employer and
  supplementary benefits, recomputed on that reference income), with a wage-index revaluation of
  the reference income after three consecutive years of claim. It is **forfaitaire at 100 %** for
  the self-employed, for Swiss-franc loans, and for anyone who took the *Prestation Forfaitaire*
  option, and forfaitaire at **50 %** for the non-working who draw no unemployment benefit.
  Franchise 90 days as standard, 30 days as an option; no new franchise on a relapse if the
  interruption ran under 90 days. IPT requires a combined rate ≥66 % fixed at consolidation and
  **"au plus tard trois ans après le début de son Incapacité Temporaire Totale"**; IPP is
  33 %–<66 % and pays 50 % of the ITT benefit; the *temps partiel thérapeutique* guarantee pays
  50 % for at most 180 days. Cover ends at the 80th birthday for Décès and the 67th for PTIA,
  invalidité AERAS, ITT, IPT and IPP. Late payment: exclusion 40 days after formal notice under
  art. L. 141-3 of the Code des assurances.

### S11 — MAIF VIE, "Avantage Emprunteur — Notice d'information"
- Publisher: MAIF VIE; subscriber association "Association pour l'union et le recours en
  assurances" (Meyreuil); administrator Multi-Impact
- Doc type: notice d'information, 30 pp.
- URL: https://www.meilleurtaux.com/images/ade/Conditions-Generales/Notice_MAIF.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: a mutual-insurer alternative contract. Single fixed franchise of 90 continuous days
  ("La franchise est de 90 jours continus dans le contrat Avantage Emprunteur"). ITT pays from
  the 91st day, forfaitaire ("L'indemnité garantie est forfaitaire, égale aux mensualités venant
  à échéance"), with a **maximum of 1 095 consecutive days** for the same ITT; a relapse does not
  restart the franchise, but any new ITT more than 60 days after the return to work does;
  half-time therapeutic return pays 50 % for at most 180 days per ITT claim. ITT ends at
  consolidation, at which point IPT/IPP are assessed. IPT ≥66 % at consolidation, which must
  occur before the 67th birthday; the benefit is the instalments, not the CRD. IPP is 33 %–66 %
  with an explicit benefit formula "Taux de prise en charge = (taux d'invalidité − 33) / 33".
  Guarantee end ages: 85 Décès, 70 PTIA, 67 ITT/IPT/IPP. *Quotité* ≤100 % per head, applying to
  every guarantee on the same loan. Premium: set by guarantees, adhesion date, age at adhesion,
  occupation, smoker status, declared medical and sporting risks, loan characteristics, **capital
  initial du prêt**, *quotité* and the co-borrower insured; fixed for the whole term and only
  changeable on the member's request or a tax change; premiums waived throughout an ITT/IPT/IPP
  claim. Restates the L. 113-12-2 cancellation right.

### S12 — MetLife, "SUPER NOVATERM CRÉDIT — Note d'information" (NISNC19, mars 2017) bound with the conditions générales
- Publisher: MetLife (France branch)
- Doc type: note d'information under arts. L. 132-5-2 and A. 132-4 of the Code des assurances,
  plus conditions générales, 13 pp.
- URL: https://assurance-de-pret-expert.com/wp-content/uploads/2021/01/Conditions-Generales-Super-Novaterm-Credit.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: an **individual** (not group) term-life contract, branch 20 (Vie–Décès), used as
  mortgage cover. The insured capital is stated in the *conditions particulières*, so the death
  benefit is a scheduled sum rather than the lender's CRD — the lender is beneficiary only "à
  concurrence des sommes restant dues", any surplus going to the insured's named beneficiaries.
  ITT is paid as **forfaitaire daily indemnities** whose amount is fixed in the conditions
  particulières, after a franchise of **15, 30, 60, 90 or 180 days at the insured's choice**, for
  at most **1 095 days per claim**; partial incapacity on a therapeutic half-time pays 50 % of
  the daily indemnity for at most 180 days; the premium-waiver benefit (EXO) can be bought
  separately with a fixed 90-day franchise and also runs to 1 095 days. IPT at ≥66 % pays the
  death capital, capped at €5 000 000 per insured across MetLife; IPP is >33 % and <66 % and pays
  a fraction of that capital; a medical/paramedical professional-invalidity guarantee is
  available. Buying back the disc/vertebral and psychiatric exclusions caps the benefit at €350
  per day and €1 500 000 per insured and imposes a 90-day franchise for those causes whatever
  franchise was chosen. Age ceilings: the annual policy anniversary following the 65th birthday
  (70th by option) for ITT, and the anniversary following the 70th for IPT/IPP/IP. Provisional
  accidental-death cover during underwriting: up to the applied-for capital, maximum €500 000, 60
  days, insured under 70. 30-day *renonciation* right under art. L. 132-5-1.

### S13 — CNP Assurances / CNP IAM / MFPrévoyance, "Notice d'information du contrat d'assurance de groupe en couverture de prêts immobiliers n° 7371 M" (Banque Française Mutualiste)
- Publisher: coinsurance — CNP Assurances and CNP IAM as *apériteur* (10 %) and MFPrévoyance SA
  (90 %); subscriber Banque Française Mutualiste
- Doc type: notice d'information of a group policy, 12 pp.
- URL: https://www.assurance-emprunteur.bzh/sites/kelemprunteur/files/insurance/cgv-banque-francaise-mutualiste-fr.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: a deliberately narrow group contract — Décès, PTIA, Invalidité AERAS and ITT only,
  **no IPT and no IPP**. Classified under branches 1, 2 and 20 of art. R. 321-1 of the Code des
  assurances. Adhesion before the 65th birthday. Franchise **90 or 180 days only**, and only
  some categories may choose 90. ITT requires, for general-scheme members, that the insured is
  actually drawing sickness/accident cash benefits or is classified in category 2 or 3
  invalidity under art. L. 341-4 of the Code de la sécurité sociale — an explicitly
  social-security-linked trigger. Benefits are whole instalments falling due after the 90th or
  180th day: "Le contrat ne prévoit pas de prise en charge prorata temporis." Relapse: a return
  to work under two months (under six months after a therapeutic half-time) does not restart the
  franchise. Cover ends at the monthly premium date after the 75th birthday for Décès, at the
  65th for PTIA, and at the first instalment after the 65th for ITT. Premium: an annual rate
  applied to the **capital initial assuré** weighted by the *quotité*, set by age at signature of
  the individual adhesion form and by the chosen franchise, and — decisively for modelling — "Le
  taux de prime a été **nivelé** sur la durée du prêt ; par conséquent, la cessation de ces
  garanties n'a pas d'incidence sur le montant de la prime."

### S14 — Crédit Agricole, "Notice d'information ADI – P / 103-2016" (group borrower policy)
- Publisher: Crédit Agricole (Assurance Décès Invalidité, ADI)
- Doc type: notice d'information of a bancassurance group policy
- URL: https://www.ce-g3-esimulca-enligne.credit-agricole.fr/pep//resources/pdf/info-assurance.pdf
- Retrieved: **NO (HTTP 502 Bad Gateway)**. fetched_ok = false. Kept as a known reference only;
  nothing in these notes relies on it. Crédit Agricole is, per [R12], one of the three largest
  writers of the risk, so its absence is a real gap in the *contrat groupe* sample.

---

## Regulatory and actuarial references

### R1 — LOI n° 2022-270 du 28 février 2022 pour un accès plus juste, plus simple et plus transparent au marché de l'assurance emprunteur ("loi Lemoine")
- Publisher: Légifrance (Journal officiel)
- Doc type: statute, 11 articles
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045268729
- Retrieved: YES.
- Content: Title I — right to cancel at any time. Art. 1 amends art. L. 113-12-2 of the Code des
  assurances and art. L. 221-10 of the Code de la mutualité, replacing the twelve-month window
  with "à tout moment" and routing notification through art. L. 113-14. Art. 2 amends arts.
  L. 313-8, L. 313-28, L. 313-30, L. 313-31 and L. 313-32 of the Code de la consommation,
  deleting the "group" qualifier and requiring explicit refusals stating every reason and naming
  the missing information. Art. 3 creates art. L. 113-15-3 (assurances) and L. 221-10-4
  (mutualité): an annual duty to remind the borrower of the cancellation right, with
  administrative fines of €3 000 for individuals and €15 000 for legal persons; the art. L. 313-8
  notice must state the possibility to cancel at any time. Art. 4 extends the retention of
  insurance information to eight years. Art. 5 fixes the lender's answer at ten business days.
  Art. 6 requires the lender to disclose loan details including the amortisation method. Art. 7
  sets the matching sanctions on lenders. **Art. 8 — entry into force: 1 June 2022 for new loan
  offers, 1 September 2022 for contracts already running.** Title II — art. 9 amends art.
  L. 1141-5 of the Code de la santé publique, capping the collectable medical history for cancer
  and hepatitis C at five years from the end of the therapeutic protocol and requiring
  renegotiation on other pathologies within three months. **Art. 10 creates art. L. 113-2-1 of
  the Code des assurances: no health questionnaire and no medical examination where the insured
  share of the cumulative credit outstanding is ≤ €200 000 per insured and the loan's repayment
  falls before the insured's 60th birthday; in force 1 June 2022.** Art. 11 requires a report to
  Parliament within two years on the effect on mutualisation, pricing and access to credit.

### R2 — Code des assurances, article L. 113-2-1
- Publisher: Légifrance
- Doc type: statutory code article (version in force from 1 June 2022)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045271000/2026-04-29
- Retrieved: YES.
- Content: verbatim conditions — "La part assurée sur l'encours cumulé des contrats de crédit
  n'excède pas 200 000 euros par assuré" and "L'échéance de remboursement du crédit contracté est
  antérieure au soixantième anniversaire de l'assuré". Both conditions are cumulative. A decree
  in Conseil d'État may set more favourable thresholds; none was retrieved.

### R3 — Code des assurances, article L. 113-12-2
- Publisher: Légifrance
- Doc type: statutory code article (version in force from 1 June 2022)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045271930
- Retrieved: YES.
- Content: by derogation from art. L. 113-12, where the contract secures repayment of all or part
  of the amount outstanding on a credit under art. L. 313-1 1° of the Code de la consommation, or
  payment of its instalments, the insured may cancel **at any time from signature of the loan
  offer defined in art. L. 313-24**. Notification is by registered letter or registered
  electronic mail. On the lender's acceptance the cancellation takes effect ten days after the
  insurer receives the lender's decision, or on the substitute contract's effective date if
  later; on refusal the contract is not cancelled. Throughout the contract the insurer may not
  cancel for aggravation of risk except in cases fixed by decree.

### R4 — Code de la consommation, sous-section "Information relative à l'assurance-emprunteur" (articles L. 313-8 to L. 313-10)
- Publisher: Légifrance
- Doc type: statutory code sub-section
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069565/LEGISCTA000032222229/
- Retrieved: YES.
- Content: **L. 313-8** (in force 1 June 2022) — every document given to the borrower before the
  offer must state the cost of the insurance in three forms: as a *taux annuel effectif de
  l'assurance* (TAEA) allowing comparison with the loan's TAEG; as a total amount in euros **over
  eight years and over the full term of the loan**; and as an amount in euros per instalment
  period, stating whether it is added to the loan instalment. The FSI of L. 313-10 and the
  insurance notice must accompany those documents, and the notice must state the cancellation
  right. **L. 313-9** extends the L. 313-8 duties to any insurance intermediary or insurer.
  **L. 313-10** (in force 1 April 2018) — a *fiche standardisée d'information* is given at the
  first simulation to anyone offered or requesting insurance covering repayment of a loan
  exceeding **€75 000** secured by a mortgage or comparable security on residential property; it
  sets out the types of guarantee offered and the borrower's freedom to insure elsewhere under
  arts. L. 313-29 and L. 313-30.

### R5 — Code de la consommation, articles R. 313-8 to R. 313-10 (contents of the fiche standardisée d'information)
- Publisher: Légifrance
- Doc type: regulatory code sub-section (as at 3 December 2025 view)
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069565/LEGISCTA000032807522/2025-12-03
- Retrieved: YES.
- Content: **R. 313-9** fixes the FSI content: (1) the definition and description of the types of
  guarantee offered; (2) the minimum guarantee characteristics required by the lender, if any;
  (3) the types of guarantee the borrower intends to take and the **share of capital covered**
  (the *quotité*); (4) a personalised cost estimate — the cost in euros per instalment period,
  the total insurance cost over the loan term, and the **TAEA for the whole loan as defined in
  art. R. 314-12**; (5) notice of the right to take another insurer under art. L. 313-30, with
  the conditions and time limits. **R. 313-10** requires the sheet to be given to each borrower
  and co-borrower separately.

### R6 — Code de la consommation, article R. 314-12 (definition of the TAEA)
- Publisher: Légifrance
- Doc type: regulatory code article (version in force from 1 October 2016)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032807626
- Retrieved: YES.
- Content: the TAEA is the **difference** between (1) the TAEG of art. L. 314-1 computed under
  arts. R. 314-1 to R. 314-10 on the assumption that the proposed insurance is entirely required
  by the lender, and (2) the TAEG computed the same way assuming no insurance is required. The
  computation therefore inherits the TAEG's equivalence-of-discounted-cash-flows method. The
  article carries no separate eight-year rule — that lives in L. 313-8 [R4].

### R7 — Code de la consommation, article L. 313-30
- Publisher: Légifrance
- Doc type: statutory code article (version in force 1 June 2022)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045271935
- Retrieved: YES.
- Content: verbatim — until the borrower signs the offer of art. L. 313-24 the lender may not
  refuse another insurance contract as security "dès lors que ce contrat présente un niveau de
  garantie équivalent au contrat d'assurance qu'il propose", and the same applies where the
  borrower exercises the cancellation right of art. L. 113-12-2 of the Code des assurances or of
  the third paragraph of art. L. 221-10 of the Code de la mutualité. Any refusal must be explicit
  and state all its reasons, specifying the missing information and guarantees.

### R8 — Code de la consommation, Section 5 "Formation du contrat de crédit" (articles L. 313-24 to L. 313-39), read for L. 313-29, L. 313-31 and L. 313-32
- Publisher: Légifrance
- Doc type: statutory code section
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069565/LEGISCTA000032222201
- Retrieved: YES.
- Content: **L. 313-29** — where the lender proposes insurance, the credit contract must carry a
  notice setting out the risks covered and the claims procedure; the definitions of the risks
  covered and the pricing may not be changed without the borrower's agreement; refusal of cover
  by the insurer resolves the credit contract without charge. **L. 313-31** — the lender notifies
  acceptance or refusal within a "délai de dix jours ouvrés", and on acceptance amends the credit
  contract "sans frais supplémentaires", the amendment carrying the new TAEG computed under arts.
  L. 314-1 to L. 314-4. **L. 313-32** — the lender may not, in exchange for accepting a
  substitute insurance, modify the loan rate (fixed, variable or revisable) or the credit
  conditions, nor charge any additional fee, including analysis fees.

### R9 — Arrêté du 29 avril 2015 précisant le format et le contenu de la fiche standardisée d'information relative à l'assurance ayant pour objet le remboursement d'un prêt
- Publisher: Légifrance (consolidated LODA text, including the annexed FSI model)
- Doc type: ministerial order with an annexed template
- URL: https://www.legifrance.gouv.fr/loda/id/JORFTEXT000030555752
- Retrieved: YES (consolidated text and the structure of the annexed model read; the annex is a
  form template, so the retrieval yields its headings and fields rather than prose).
- Content: the model FSI has eight numbered parts plus a "remarques" block — (1) identity of the
  distributor with SIREN/ORIAS; (2) the insurance candidate's profile; (3) the loan's
  characteristics (lender, project type, amount, type — amortising / in fine / relais, term,
  indicative rates); (4) **the minimum guarantees required by the lender with the required
  quotité for each of Décès, PTIA, ITT, IPT, IPP and perte d'emploi**; (5) the guarantees offered
  with their definitions and the solution envisaged, again with *quotité* boxes; (6) the
  underwriting section; (7) the personalised cost estimate — share of capital covered per
  guarantee and per loan, premium per period, total insurance cost over the loan term, the
  **TAEA for the whole loan**, and (added in 2022) the total cost over the first eight years, and
  whether the premium is level or variable with its minimum and maximum; (8) warnings on excluded
  risks, *carence* and *franchise*, the consequences of a false medical declaration, and the
  medical-questionnaire exemption. Applies with local adaptations in New Caledonia and French
  Polynesia.

### R10 — Arrêté du 27 mai 2022 modifiant l'arrêté du 29 avril 2015 (FSI)
- Publisher: Légifrance (Journal officiel)
- Doc type: ministerial order
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045833541
- Retrieved: YES.
- Content: three operative articles, in force **1 June 2022**. Art. 1 inserts a complementary
  notice that the contract's invalidity guarantee is independent of the social-security notion of
  invalidity — "La garantie invalidité … est indépendante de la notion d'invalidité retenue par
  la sécurité sociale". Art. 2 renumbers the cost part as 7.1 and adds **7.2, the total insurance
  cost over the first eight years of the contract**. Art. 3 rewrites part 8 to add the
  medical-questionnaire exemption (≤ €200 000 cumulative insured share and repayment before age
  60) and the right to switch insurers at equivalent guarantee level.

### R11 — CCSF, "Avis du Comité consultatif du secteur financier sur l'équivalence du niveau de garantie en assurance emprunteur", 13 janvier 2015, with its annexed *liste de place*
- Publisher: Comité consultatif du secteur financier (secretariat at the Banque de France)
- Doc type: formal opinion (avis) with an annexed criteria list, 8 pp.
- URL: https://www.moneyvox.fr/r/CCSF/CCSF-2015-assurance-emprunteur.pdf
- Retrieved: YES (PDF downloaded, full text extracted). This is a third-party mirror; the
  Banque de France copies of the CCSF corpus all returned HTTP 403 (see R13, R14, R15, R20).
- Content: the three-step common method. (1.1) a closed list of guarantee characteristics that
  lenders may require, agreed by market consensus and revisable annually after the CCSF's
  opinion; (1.2) **each lender chooses at most 11 criteria from the list, plus at most 4 on the
  perte d'emploi guarantee**, must state the required value wherever possible — "par exemple son
  caractère forfaitaire ou indemnitaire" — and must publish its list on its website and on the
  FSIs it issues; (1.3) after the individual analysis the lender hands the borrower a *fiche
  personnalisée* giving the fully valued list of required criteria, in good time and in any case
  before the loan offer is issued. (2) the FSI is reinforced: systematic delivery from the first
  costed simulation, and a space for the lender's general requirements. (3) a CCSF *assurance
  emprunteur* glossary before 30 April 2015; written, dated and explicit refusal reasons; the
  method must not impede the AERAS convention. (4) monitoring by the ACPR and the DGCCRF, with a
  first review in Q1 2016. (5) **entry into force at the latest 1 October 2015, and from
  1 May 2015 lenders undertake to motivate any equivalence refusal only by characteristics
  drawn from the *liste de place*.** The annex is the operative criteria grid — see
  "Extracted specifications §11" for the criterion-by-criterion transcription.

### R12 — CCSF, "Rapport annuel 2023" (rapport adressé au Président de la République et au Parlement), chapter 1.1 "L'assurance emprunteur"
- Publisher: Comité consultatif du secteur financier; copy served by vie-publique.fr
- Doc type: annual report, 94 pp.
- URL: https://www.vie-publique.fr/files/rapport/pdf/298146.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the CCSF's summary of its December 2023 *bilan de l'assurance emprunteur* to
  Parliament, based on a market study by Actélior. Substitution requests received by banking
  networks per half-year: 99 265 (H1 2021), 121 830 (H1 2022), 184 528 (H2 2022), 181 600
  (H1 2023) — an increase of more than 80 % between H1 2021 and H1 2023. Portfolio split by
  contract type: 2021 — 73.6 % *contrat groupe bancaire*, 4.4 % *contrat alternatif bancaire*,
  15.3 % *contrat alternatif externe*, 6.7 % uninsured; 2022 — 73.0 / 4.3 / 15.5 / 7.2; at
  31 May 2023 — 72.2 / 4.4 / 16.0 / 7.4. About 215 000 external alternative contracts added in
  17 months, 117 000 of them between January and May 2023. Socio-professional skew: CSP1 are
  58 % of substitutions and 69 % of external alternative contracts taken at loan origination but
  only 27 % of the banks' mortgage portfolios. On the questionnaire waiver: 58.5 % of borrowers
  had an insured amount below €200 000 on the operation, but **only 23 % of those contracts were
  eligible for the waiver, and contracts without medical selection are only 31 % of
  substitutions**, because lengthening loan terms push the term past the 60th birthday. Pricing:
  external alternative contracts *without* medical selection were repriced up by about 10 % on
  average versus 2021 tariffs, while tariffs overall continued to fall — the report's charts show
  2019→2023 changes for medically-selected external alternative contracts ranging from −40 % at
  the youngest ages to +16 % at the oldest, and bank group tariffs falling 14 %–30 % across the
  age range. Substitution acceptance rates 88 %–90 % via banking networks and 70 %–87 % via
  intermediaries. Claim declines: 2.5 %–4.4 % (8.3 % in 2020) on death/PTIA for external
  alternative contracts and 2.5 %–3.8 % for bank group contracts; 10.2 %–12.8 % on
  incapacity/invalidity for bank group contracts and 7.7 %–16.3 % for external alternative
  contracts. Between 50 % and 75 % of declines by external alternative players are
  mis-declarations — wrong insurer, claim declared inside the *franchise*, maximum cover age
  exceeded. Also records the **CCSF avis of 12 December 2023** by which insurers undertake to
  offer a *garantie aide à la famille* (temporary cover of instalments where the insured stops
  work to care for a seriously ill or injured minor child) in at least one borrower-insurance
  contract distributed from **July 2025**.

### R13 — CCSF, "Bilan de l'assurance emprunteur — Rapport adressé au Parlement" (décembre 2023)
- Publisher: Comité consultatif du secteur financier / Banque de France
- Doc type: report to Parliament under art. 11 of the loi Lemoine
- URL: https://www.banque-france.fr/system/files/import/ccsf/medias/documents/bilan_ae_2023.pdf
- Retrieved: **NO (HTTP 403, retried once, 403 again)**. fetched_ok = false. Its conclusions are
  used here only as summarised inside the CCSF annual report [R12], which was retrieved. Figures
  circulating in secondary coverage of the later 2024/2025 CCSF work — 22.15 million contracts
  covering mortgages, €6.830 bn of premiums, 496 654 substitution requests in 2024 of which
  93.91 % accepted, alternative share 17.48 % — are **[unverified]** and are not relied on.

### R14 — Banque de France, press release "Assurance emprunteur : le bilan très positif de la loi Lemoine"
- Publisher: Banque de France (for the CCSF), 15 January 2024
- Doc type: press release
- URL: https://www.banque-france.fr/fr/communiques-de-presse/assurance-emprunteur-le-bilan-tres-positif-de-la-loi-lemoine
- Retrieved: **NO (HTTP 403, retried once, 403 again)**. fetched_ok = false.

### R15 — CCSF, "Bilan du CCSF sur l'équivalence du niveau de garantie en assurance emprunteur" (décembre 2016)
- Publisher: Comité consultatif du secteur financier / Banque de France
- Doc type: review report on the 2015 avis
- URL: https://www.banque-france.fr/system/files/import/ccsf/medias/documents/ccsf-rapport-equivalence-niveau-garantie-2016.pdf
- Retrieved: **NO (HTTP 403)**. fetched_ok = false. Kept as a known reference; the 2015 avis
  itself [R11] was retrieved in full and carries the operative criteria.

### R16 — Code de la santé publique, article L. 1141-5 (droit à l'oubli and the AERAS grille de référence)
- Publisher: Légifrance
- Doc type: statutory code article (version in force 2 March 2022)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045272010
- Retrieved: YES.
- Content: the AERAS convention sets the terms and time limits beyond which people who have had
  a cancer may not be surcharged or excluded, and beyond which no medical information about it
  may be collected; the pathologies and delays are set against a published *grille de référence*
  built on proposals from the national cancer institute (art. L. 1415-2). **In every case the
  delay beyond which no medical information on cancers or hepatitis C may be collected may not
  exceed five years from the end of the therapeutic protocol.** A Conseil d'État decree sets the
  sanctions; applicants must be informed of the prohibition; the convention must extend the
  regime to other, notably chronic, pathologies as therapeutic evidence allows.

### R17 — Convention AERAS, "Document d'information AERAS" (décembre 2023)
- Publisher: Convention AERAS (s'Assurer et Emprunter avec un Risque Aggravé de Santé)
- Doc type: official information document for insurance applicants, 2 pp.
- URL: https://www.aeras-infos.fr/files/live/sites/aeras/files/contributed/docs/Document%20Information%20AERAS%20d%C3%A9cembre%202023.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: opens by restating the loi Lemoine questionnaire waiver (≤ €200 000 insured share of
  the cumulative outstanding, repayment before the 60th birthday). *Droit à l'oubli*: applies to
  affected consumer loans, professional loans for premises/equipment and mortgages, where the
  contract's term falls **before the borrower's 71st birthday**; the applicant need not declare a
  past cancer or hepatitis C where the end of the therapeutic protocol is more than **five years**
  before the application and there has been no relapse, and gets cover with no surcharge and no
  exclusion for that history; definitions of "end of therapeutic protocol" and "relapse" are
  given. *Grille de référence*: applies to mortgages and professional loans for premises/
  equipment where the insured share does not exceed **€420 000** (per operation for a principal
  residence, otherwise on the cumulative outstanding) and the term falls before the 71st
  birthday; list I gives pathologies insurable at standard conditions after shorter delays than
  the *droit à l'oubli*, list II gives pathologies insurable with a **capped surcharge** stated
  per guarantee. Other pathologies and any current incapacity, invalidity or unfitness must still
  be declared.

### R18 — France Assureurs, "L'assurance prévoyance en 2024" (étude, juillet 2025)
- Publisher: France Assureurs (Fédération française de l'assurance), Direction Statistiques &
  Recherche Économique
- Doc type: annual market study, 25 pp.
- URL: https://www.franceassureurs.fr/wp-content/uploads/lassurance-prevoyance-en-2024.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: French *prévoyance* premiums €29.2 bn in 2024, +4.7 %; claims charge €16.6 bn,
  +14.5 %; claims-to-premiums ratio 56.9 %, up 4.9 points. In the "produits spécifiques" table
  (Code des assurances undertakings only), the line **"Contrats emprunteurs (garantie décès)"**
  — that is, the death guarantee of individually-underwritten borrower contracts — shows
  **5 223 thousand contracts at end-2024 (+15.1 %), €979 m of premiums (+2.5 %) and €330 m of
  benefits (−6 %)**. Emprunteur premiums grew +2.5 % in 2024 and the emprunteur claims charge
  fell −5.9 % after +7.3 %. Charts split individual death-cover premiums between *temporaires
  (hors emprunteurs)*, *emprunteurs*, *vie entière* and *combinés*, with emprunteurs at 17 % of
  individual death-cover premiums in 2024. **These figures cover only the death guarantee of
  individual-adhesion contracts written by Code des assurances undertakings** — they exclude the
  incapacity/invalidity premium, the bancassurance group business and mutuelles/institutions de
  prévoyance, so they are far smaller than the whole-market figures cited in [R12] and are not
  a market total.

### R19 — Code de la consommation, article R. 313-8
- Publisher: Légifrance
- Doc type: regulatory code article (version in force 1 July 2016)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032807524
- Retrieved: YES.
- Content: verbatim — the FSI of art. L. 313-10 "énonce de manière claire et lisible les
  principales caractéristiques de l'assurance ayant pour objet de garantir le remboursement d'un
  prêt soumis aux dispositions du chapitre III du titre Ier, dont le modèle est annexé au présent
  code."

### R20 — Comité consultatif du secteur financier, institutional site
- Publisher: CCSF
- Doc type: document portal
- URL: https://www.ccsfin.fr/
- Retrieved: **NO (HTTP 403)**. fetched_ok = false. The whole banque-france.fr / ccsfin.fr estate
  refused automated fetches in this session; the CCSF documents used here were obtained from
  mirrors ([R11] via moneyvox, [R12] via vie-publique).

---

## Extracted specifications

### 1. Product structure, legal forms and the three market regimes

- The product is life-and-health cover attached to a mortgage, whose beneficiary is normally the
  lender up to the sums still owed. Three regimes coexist and are measured separately by the
  regulator [R12]:
  - **contrat groupe bancaire** — the lender's own group policy, joined by adhesion; 72.2 % of
    insured mortgage portfolios at 31 May 2023 [R12]. Examples in this set: BPCE/Banque Populaire
    A340G [S10], Banque Française Mutualiste 7371 M [S13].
  - **contrat alternatif bancaire** — an alternative contract still distributed inside a banking
    group; 4.4 % [R12].
  - **contrat alternatif externe** (*délégation d'assurance*) — an individual or association
    group contract from an insurer unconnected to the lender; 16.0 % [R12]. Examples: Cardif
    Libertés Emprunteur [S1][S2], APRIL [S5][S6][S7], CNP A217Y through ASSOCIAREA [S9], MAIF VIE
    Avantage Emprunteur [S11], MetLife Super Novaterm Crédit [S12].
  - 7.4 % of mortgage portfolios carried no insurance at all [R12].
- Legal wrappers observed: *contrat d'assurance de groupe à adhésion facultative* under
  arts. L. 141-1 ff. of the Code des assurances, with an association or the bank as
  *souscripteur* [S1][S9][S10][S11][S13]; and a true individual contract with *conditions
  particulières*, here MetLife's branch 20 term-life policy [S12]. BFM's 7371 M is written across
  **branches 1, 2 and 20** of art. R. 321-1 of the Code des assurances [S13] — accident, sickness
  and life-death — which is the exact regulatory signature of a combined death + incapacity
  borrower cover.
- Coinsurance is normal in the bancassurance segment: 7371 M is 10 % CNP Assurances/CNP IAM as
  *apériteur* and 90 % MFPrévoyance [S13]; A340G names CNP Assurances and BPCE Vie [S10].
- Delegated management is also normal: Cbp France administers the Cardif contract [S1],
  Multi-Impact administers both the CNP A217Y and the MAIF contracts [S9][S11].
- Market concentration: the three largest writers are Crédit Agricole, CNP Assurances and Crédit
  Mutuel Alliance Fédérale [unverified — from a search summary, not a retrieved document].

### 2. The substitution and cancellation regime (Lagarde → Hamon → Bourquin → Lemoine)

- **Loi Lagarde (1 July 2010)** introduced *équivalence du niveau de garantie*: the lender may not
  refuse another insurance contract offering an equivalent level of guarantee, and any refusal
  must be motivated. The CCSF quotes the then-art. L. 312-9 wording verbatim [R11]; the insurer
  brochure dates it September 2010 [S6]. The loi Lagarde text itself was **not retrieved**.
- The **loi bancaire of 26 July 2013** extended the lender's analysis period to 10 days [R11].
- **Loi Hamon (17 March 2014)** created the FSI and a 12-month substitution window from signature
  of the loan offer [R11 records the FSI origin in "la loi relative à la consommation du 17 mars
  2014"; S6 states the borrower has "11,5 mois pour résilier à compter de la signature de votre
  offre de prêt"; S1 records the 12-month window with notice at least 15 days before its end].
  The loi Hamon text itself was **not retrieved**.
- The **amendement Bourquin (2017)** added an annual cancellation right at each *échéance
  annuelle* of the insurance contract with two months' notice. This is visible in the pre-Lemoine
  contract wording — Cardif [S1] states cancellation "à chaque échéance annuelle correspondant à
  la date d'anniversaire de la signature de l'offre de prêt, au plus tard deux mois avant". The
  loi n° 2017-203 text itself was **not retrieved**; the attribution of that right to the
  Bourquin amendment is [unverified].
- **Loi Lemoine (loi n° 2022-270 du 28 février 2022)** [R1]:
  - *Résiliation à tout moment* from signature of the loan offer, by amendment of art. L. 113-12-2
    of the Code des assurances [R1 art. 1][R3]. **In force 1 June 2022 for new loan offers and
    1 September 2022 for contracts already running** [R1 art. 8].
  - The lender must answer a substitution request within **ten business days** [R1 art. 5]
    [R8, L. 313-31], amend the credit contract **without additional fees**, and restate the TAEG
    [R8, L. 313-31]. It may not change the loan rate or the credit conditions, nor charge any fee
    including analysis fees [R8, L. 313-32].
  - Refusals must be **explicit, state every reason, and name the missing information and
    guarantees** [R1 art. 2][R7].
  - An **annual duty** on the insurer to inform the borrower of the cancellation right, with
    fines of €3 000 (individuals) / €15 000 (legal persons); matching sanctions on lenders
    [R1 arts. 3 and 7].
  - Insurance information must be retained **eight years** [R1 art. 4].
  - Cancellation takes effect **ten days after the insurer receives the lender's acceptance**, or
    on the substitute contract's effective date if later; on refusal the contract is not cancelled
    [R3]. The 2025 CNP notice implements exactly this [S9].
- Contract-level implementation observed: the CNP 2025 notice cites arts. L. 113-12-2,
  L. 313-30 and L. 313-31 and requires the member to notify the manager, send the substitute
  contract to the lender, then notify the lender's decision and the substitute's effective date
  [S9]. The APRIL DIPA distinguishes non-professional mortgages (any time) from other loans
  (annually, before 31 October for a 31 December effect) [S7]. Cardif's professional-loan
  adhesions are excluded from annual cancellation by derogation from art. L. 113-12 [S1].
- **Substitution volumes and outcomes** [R12]: 99 265 requests in H1 2021 rising to 181 600 in
  H1 2023 (+80 %); acceptance 88 %–90 % through banking networks and 70 %–87 % through
  intermediaries; about 215 000 external alternative contracts added in 17 months.

### 3. Suppression of the health questionnaire (the "Lemoine waiver")

- Both conditions must hold **cumulatively** [R2]:
  1. the insured share of the **cumulative credit outstanding** does not exceed **€200 000 per
     insured** (per *assuré*, not per loan, and across all lenders); and
  2. the loan's **repayment falls before the insured's 60th birthday**.
- Where they hold, no health information and no medical examination may be required [R2]; in
  force 1 June 2022 [R1 art. 10].
- Contract implementation: CNP A217Y states the candidate signs only the individual adhesion form
  with no medical formality, and defines *encours cumulé* as all the candidate's existing
  mortgages plus the new operation [S9]. The FSI model carries the same statement since the 2022
  amendment [R9][R10].
- Where the waiver does not apply, a health questionnaire is required, with laboratory tests and
  possibly a medical examination at the insurer's expense; CNP fixes the questionnaire's validity
  at **6 months** [S9]. Cardif can accept at normal terms, accept with a *surprime* and/or
  guarantee restrictions, or decline [S1]. APRIL applies a **3-month waiting period** on illness
  claims where an already-running, previously uninsured loan is brought into cover [S7].
- Take-up is much narrower than the headline suggests: 58.5 % of borrowers had an insured amount
  under €200 000, but only 23 % of those contracts were eligible, and contracts without medical
  selection are only 31 % of substitutions — because lengthening loan terms push the repayment
  date past the 60th birthday [R12].
- Pricing effect: external alternative contracts **without** medical selection were repriced up
  by roughly **10 % on average** versus 2021 tariffs [R12].

### 4. Droit à l'oubli and the AERAS convention

- **Droit à l'oubli**: no declaration of a past cancer or hepatitis C where the end of the
  therapeutic protocol is more than **five years** old and there has been no relapse; cover is
  then granted with no surcharge and no exclusion for that history [R17]. The five-year cap is
  statutory [R16][R1 art. 9]. It applies to affected consumer loans, professional loans for
  premises/equipment and mortgages whose **term falls before the borrower's 71st birthday**
  [R17].
- **Grille de référence AERAS**: applies where the insured share does not exceed **€420 000**
  (per operation for a principal residence; otherwise on the cumulative outstanding) and the term
  falls before the **71st birthday**; list I sets shorter-than-five-year delays after which
  standard terms apply, list II sets **maximum surcharge rates by guarantee** [R17].
- **Garantie invalidité spécifique (GIS)**: where the ITT/IPT/IPP guarantees are refused on
  medical grounds, the AERAS convention requires a specific invalidity guarantee to be studied.
  Cardif's version pays the CRD, has no pathology exclusions but may carry a surcharge, cannot be
  requested directly, and requires either category 2 or 3 social-security invalidity (employees),
  long-term sick leave (civil servants), a notification of total unfitness for the profession
  (self-employed), or a **functional incapacity rate ≥70 %** on the civil-and-military-pensions
  scale; it must be triggered before the end of the year in which the minimum retirement age is
  reached and at the latest before 65 (or 70 where PTIA was extended to 70) [S1]. CNP calls the
  equivalent guarantee *Invalidité AERAS* and pays 100 % of the instalment up to age 70 [S9];
  BFM 7371 M also carries an *Invalidité AERAS* guarantee [S13]. APRIL's brochure describes the
  same idea, triggered from **70 % functional incapacity** [S6].

### 5. The guarantees, precisely

**DÉCÈS.** Pays the *capital restant dû*, weighted by the *quotité*.
- CNP A217Y: the CRD shown on the amortisation table the day after the instalment immediately
  preceding death (an instalment falling on the day of death is deemed due), **plus interest
  accrued since that instalment**; during a partial-deferral period it is the initial loan amount
  plus accrued interest; on a fully deferred loan, the initial amount plus contractual accrued
  interest [S9]. MAIF: the CRD at the instalment preceding death, **plus accrued interest**, and
  the total paid on one loan may not exceed the CRD at the date of death [S11].
- Cardif: the CRD as shown on the *échéancier* at the date of death; payment of the CRD ends all
  guarantees for that insured [S1]. APRIL: the CRD on the lender's schedule within the *Montant
  garanti* [S5][S7].
- MetLife's individual contract is the exception: it pays the **capital garanti stated in the
  conditions particulières**, with the lender beneficiary only up to the sums still owed and the
  surplus going to the insured's named beneficiaries [S12].
- Cover-end ages observed: **90th birthday** (Cardif, at the adhesion renewal following it [S1];
  APRIL Optimum + at 31 December of the 90th birthday year [S7]); **85th** (CNP A217Y [S9], MAIF
  [S11], APRIL PRT150115 at 31 December of the 85th year [S5], APRIL Optimum + brochure "indemnisé
  jusqu'à 85 ans" [S6]); **80th** (BPCE A340G [S10]); **75th** (BFM 7371 M, at the monthly premium
  date after the 75th birthday [S13]). Adhesion age ceilings: under 85 (Cardif [S1]), up to 80
  (APRIL Optimum + [S6]), 66–80 for a death-only CNP adhesion [S9], under 65 (BFM [S13]).

**PTIA — perte totale et irréversible d'autonomie.** Assimilated to death and paying the same
benefit [S5][S9][S11].
- Definition, consistent across every retrieved contract: the insured is definitively unable to
  engage in any remunerated occupation **and** must permanently call on a third person for the
  ordinary acts of daily life. Cardif requires assistance for **at least three of the four** acts
  — se laver, se vêtir, se nourrir, se déplacer [S1]; CNP and APRIL require assistance for **all
  four** [S9][S5]. That three-of-four versus four-of-four difference is the whole substance of the
  PTIA definition and is a real dispersion point.
- Cover-end ages: 65 (extendable to 70 on request) at Cardif [S1][S3]; 70 at CNP [S9], MAIF [S11]
  and APRIL PRT150115 [S5]; 71 at APRIL Optimum + [S7]; 67 at BPCE [S10]; 65 at BFM [S13].
- Evidence normally required: category 3 social-security invalidity for scheme members
  [S1][S11].

**ITT — incapacité temporaire totale de travail.**
- Definition, working insured: temporarily and completely unable, following illness or accident,
  to carry on **his or her own** occupation [S1][S9][S11][S12]. Non-working insured: medically
  prescribed complete rest preventing all ordinary daily occupations [S1][S9][S12], or inability
  to carry on the *Occupations de la vie quotidienne* [S5][S6].
- The "own occupation" versus "any occupation" split is the most consequential wording
  difference in the product; APRIL's own brochure makes the point with a baker who breaks an arm
  and would be paid under an own-occupation definition and refused under an any-occupation one
  [S6]. The CCSF criteria list makes it a selectable criterion [R11].
- BFM 7371 M's definition is instead **anchored to social security**: a general-scheme member is
  in ITT only if actually drawing sickness/accident cash benefits or classified in category 2 or 3
  invalidity under art. L. 341-4 of the Code de la sécurité sociale [S13]. By contrast, Cardif
  states expressly that "L'appréciation par CARDIF de la notion d'incapacité ou d'invalidité n'est
  pas liée à la décision de la Sécurité sociale" [S1], and since 2022 the FSI model must carry the
  same warning [R10].
- **Franchise** (deductible days), retrieved values:
  | Contract | Franchise options |
  |---|---|
  | Cardif Libertés Emprunteur [S1][S2] | 30, 60, 90, 180 (choice at adhesion, changeable at renewal with the insurer's and lender's agreement; shortening requires new underwriting) |
  | CNP A217Y [S9] | 30, 60, 90, 120, 180 |
  | APRIL PRT150115 [S5] | benefit from the 31st, 61st, 91st or 181st day |
  | APRIL Optimum + [S6][S7] | 30, 60, 90, 180 (90/180 only for the non-working and for DROM / EU / EEA / UK residents) |
  | BPCE A340G [S10] | 90 standard; 30 as a priced option |
  | BFM 7371 M [S13] | 90 or 180 only, and 90 only for some categories |
  | MAIF [S11] | 90, fixed, no choice |
  | MetLife [S12] | 15, 30, 60, 90, 180 |
  The CCSF criteria list offers the lender the boxes **≤30 / ≤60 / ≤90 / ≤120 / ≤180 days** [R11].
- **Maximum indemnification duration:** **1 095 days** (three years) per claim at Cardif [S1][S2],
  MAIF [S11] and MetLife [S12]. CNP A217Y and APRIL do not state a day cap in the retrieved text;
  they end ITT at consolidation, at which point IPT/IPP are assessed [S9][S11][S5]. BPCE ties the
  two together from the other side: the consolidation that opens IPT is fixed "au plus tard trois
  ans après le début de son Incapacité Temporaire Totale" [S10]. So the 1 095-day figure is real
  and widespread but is **not universal as an explicit contractual cap**.
- **Benefit:** 100 % of the loan instalment (capital and interest) computed from the amortisation
  schedule at the date of the claim, scaled by the *quotité* [S1][S9][S11]. On deferred-capital
  loans only the interest instalments are covered, and the final capital instalment of an in fine
  loan is never indemnified [S9][S1]. Pro-rating: Cardif prorates by days at 1/30, 1/90 or 1/360
  according to the loan's instalment frequency [S1]; MAIF decomposes quarterly, half-yearly and
  annual instalments into equal monthly ones [S11]; BFM pays **whole instalments only** — "Le
  contrat ne prévoit pas de prise en charge prorata temporis" [S13].
- **Monetary caps:** €10 000 per month per insured across all loans (Cardif [S1]); €25 000 per
  month (APRIL Optimum +, €6 000 in the DROM) [S6][S7]; €350 per day and €1 500 000 per insured
  where MetLife's exclusion buy-back applies [S12].
- **Therapeutic part-time return:** 50 % of the instalment for at most **180 days** (Cardif, cap
  €5 000/month [S1]; MAIF [S11]; BPCE [S10]; MetLife [S12]) or **6 months** (APRIL, after at least
  two months of ITT indemnification [S5][S7]; CNP, as its *garantie mi-temps thérapeutique* [S9]).
  The CCSF criterion is "prise en charge minimale de 50 % sur une durée d'au moins 90 jours"
  [R11].
- **Relapse rules** (whether a fresh *franchise* applies), a genuine dispersion point:
  | Contract | No new franchise if the return to work lasted |
  |---|---|
  | Cardif [S1] | ≤ 60 days |
  | MAIF [S11] | relapse: never; a new ITT more than 60 days after return: new franchise |
  | APRIL [S5] | ≤ 2 months |
  | CNP A217Y [S9] | interruption < 90 days |
  | BPCE A340G [S10] | interruption < 90 days |
  | BFM 7371 M [S13] | return < 2 months, or < 6 months after a therapeutic part-time |
  | MetLife [S12] | relapse within 60 days (per the ITT wording) |
- **Cessation:** return to work even part-time (except therapeutic part-time), retirement or
  pre-retirement, consolidation, the age ceiling, recognition of PTIA/IPT/IPP, or exhaustion of
  the 1 095 days [S1][S9][S11]. Statutory maternity leave is expressly not indemnified [S5].
- **Premium waiver during claim:** Cardif refunds the premiums of the affected insured during ITT
  (to the 1 095th day) and IPP [S1]; APRIL waives the ITT/IPT/IPP and Confort option premiums pro
  rata [S5]; MAIF waives premiums throughout an ITT/IPT/IPP claim [S11]; CNP requires the member
  to advance the premiums and refunds them with the benefit [S9]. MetLife sells the waiver as a
  separate EXO guarantee with a fixed 90-day franchise and a 1 095-day limit [S12].

**IPT — invalidité permanente totale.** Combined invalidity rate **≥66 %** at consolidation, plus
(in most wordings) permanent inability to carry on the occupation practised at the date of the
claim [S1][S5][S9][S10][S11][S12].
- **The benefit basis is the single biggest structural difference in the product.** Retrieved
  variants:
  - **CRD (capital)** — Cardif pays the *capital restant dû* at the medical recognition of IPT,
    which ends every guarantee for that insured [S1][S2]; APRIL PRT150115's medical-professions
    invalidity likewise pays the CRD [S5]; the APRIL DIPA calls this "IPT en capital" [S7].
  - **Instalments (rente)** — CNP A217Y pays "la prestation identique à celle prévue dans le cadre
    de la garantie ITT" [S9]; MAIF pays the instalments falling due [S11]; APRIL calls this "IPT
    en rente" [S7]; APRIL PRT150115's IPT uses "la base de calcul des prestations … identique à
    celle de l'I.T.T." [S5].
  - **Insured's choice** — Cardif's broker material states IPT prestation "au choix : CRD ou
    échéances selon la quotité assurée" [S3].
  - **Not offered at all** — BFM 7371 M has no IPT guarantee [S13].
- Cover-end ages: 65/70 (Cardif [S1]), 70 (CNP [S9], APRIL PRT150115 [S5]), 71 (APRIL Optimum +
  [S6]; 65 without the "Extension 65+" option [S7]), 67 (BPCE [S10], MAIF consolidation before 67
  [S11]).

**IPP — invalidité permanente partielle.** A band of **33 % to below 66 %** [S1][S9][S10][S11],
stated as **33 %–65 %** at APRIL [S5][S6][S7] and as ">33 % and <66 %" at MetLife [S12]. Below
33 %, nothing is payable [S9][S11].
- Benefit formulas, all applied to the ITT instalment and scaled by the *quotité*:
  - **Linear ramp (N−33)/33** — Cardif pays "(N−33)/33 fois le montant de l'échéance de prêt prévu
    au titre de l'Invalidité permanente totale (N étant le taux d'invalidité reconnu) dans la
    limite de 100 %", with N revisable upward on aggravation [S1]. MAIF states the same:
    "Taux de prise en charge = (taux d'invalidité − 33) / 33" [S11]. At N = 66 % the ramp gives
    exactly 100 %, so IPP and IPT meet continuously.
  - **Flat 50 %** — CNP A217Y [S9], BPCE A340G [S10], APRIL [S5][S6][S7] all pay 50 % of the ITT
    benefit anywhere in the band.
  That is a materially different liability profile for the same medical state and must be a
  configurable option in any model.
- IPP is an **option**, not a base guarantee, at CNP [S9], BPCE [S10], APRIL [S5] and Cardif
  (combination D only) [S1]; it is unavailable to the non-working at CNP [S9] and BPCE [S10].
- The IPP monthly cap follows the ITT cap: €10 000 per month per insured at 100 % invalidity at
  Cardif [S1].

**The barème croisé (combined invalidity rate).** Both retrieved tables are double-entry grids
crossing a *taux d'incapacité fonctionnelle* (assessed on the *barème de droit commun du concours
médical*, without regard to occupation) with a *taux d'incapacité professionnelle* (assessed on
the occupation practised before the event and the remaining possibility of practising it,
disregarding retraining into another occupation) [S1][S5][S9][S10][S11].
- Fitting the two published grids [S1][S9] reproduces every cell of both to the printed precision
  with **N = (IF² × IP)^(1/3)** — the cube root of the squared functional rate times the
  professional rate. Cardif's own worked example (IF 40 %, IP 80 % → 50.40 %) and CNP's (IF 50 %,
  IP 40 % → 46 %) both satisfy it. *This formula is a derivation from the published tables, not a
  quotation: neither contract states it.* Treat it as a fitted reconstruction, and ship the tables
  themselves where an exact match matters.
- For an insured with no occupation at the date of the claim, only the functional rate is used
  [S9][S10][S11]; APRIL then switches to the médico-légale scale of the Société de Médecine Légale
  / AMEDOC rather than the *concours médical* scale [S5].

**PERTE D'EMPLOI (optional).**
- Cardif: covers redundancy giving entitlement to unemployment benefit (a *rupture
  conventionnelle* is expressly not a redundancy) and loss of activity by an owner-manager
  covered by a private managers' unemployment scheme; **carence 180 consecutive days**, **franchise
  90 consecutive days**, pays **50 % of the insured share of the instalments**, capped **€2 500 per
  month per insured**, for **up to 18 months** in one or more claims, renewable **two years** after
  the last payment; benefit stops if the insured moves onto ITT; a suspension of unemployment
  benefit under 180 days resumes cover with no franchise, over 180 days with a 90-day franchise;
  adhesion under 61 [S1][S3].
- Cardif also includes, free of charge, an *Aide au retour à l'emploi* lump sum of **€1 000** after
  **30 consecutive days** of unemployment, paid **once per insured for the life of the contract**
  [S1].
- APRIL Intégrale: benefit from the **91st consecutive day of *chômage total*** with unemployment
  benefit in payment, requires **≥12 months' CDI seniority** with a single employer at the loss,
  capped **€3 500 per month**, **maximum 12 months per redundancy** (continuous or not), adhesion
  18–60, PE *quotité* ≤ ITT/IPT *quotité*, minimum insured loan €18 000 [S8].
- CCSF criteria for perte d'emploi allow the lender to fix *carence* ≤3/6/12 months, *franchise*
  ≤60/90/120 days, per-claim duration ≥12 or ≥24 months, a total duration of at least 36 months,
  the share of the instalment covered (≤50 %, ≤75 %, <100 %, 100 %), a *forfaitaire* basis, and
  cover without a CDI-seniority condition [R11]. Both retrieved PE modules sit well inside those
  bounds.

**GARANTIE AIDE À LA FAMILLE (GAF).** New: insurers undertook in the CCSF avis of 12 December 2023
to offer it in at least one borrower-insurance contract distributed from **July 2025** [R12]. CNP
A217Y already carries it [S9]: requires ITT and IPT cover, a mortgage financing a principal,
secondary or rental residence (not relais or in fine), a dependent child under 20 with a serious
illness, disability or accident within arts. L. 544-1 ff. of the Code de la sécurité sociale, the
insured drawing the *allocation journalière de présence parentale* (AJPP), and a partial or total
stop of work. Pays **50 % of the ITT benefit**, capped **€4 000 per month per insured**, for as
long as the AJPP runs and at most **28 months**, ceasing at the 67th birthday; not cumulable with
any other guarantee of the contract [S9].

### 6. Indemnitaire versus forfaitaire — the first modelling switch

- **Forfaitaire**: the benefit is the contractually insured instalment (or a fixed daily
  indemnity), paid whatever the employer or the compulsory scheme pays. **Indemnitaire**: the
  benefit is capped by the actual income loss, so an insured whose salary is fully maintained
  receives nothing [S6].
- Death and PTIA are always effectively *forfaitaire* against the CRD; the distinction bites only
  on ITT, IPT, IPP and perte d'emploi.
- Retrieved positions:
  - **Cardif Libertés Emprunteur is a *contrat forfaitaire*** — the broker plaquette says so in
    terms, and the ITT wording pays 100 % of the instalment "quelle que soit la prise en charge de
    votre employeur ou de votre régime obligatoire" [S3][S1].
  - **MAIF: "L'indemnité garantie est forfaitaire"** [S11]. **MetLife: "indemnités journalières
    forfaitaires"** whose amount is set in the conditions particulières [S12]. **APRIL: forfaitaire
    by design** — "Vos garanties sont forfaitaires … quelle que soit la prise en charge de votre
    employeur" [S6].
  - **BPCE A340G is indemnitaire by default and forfaitaire by option** [S10]. Its four benefit
    rules are the clearest statement of the mechanic anywhere in this corpus:
    | Category | ITT/IPT benefit |
    |---|---|
    | Self-employed, non-civil-servant; or Swiss-franc loan | 100 % of the monthly instalment (insurance premium included), pro-rated by days, × *quotité* |
    | Non-working and drawing no unemployment benefit | 50 % of the monthly instalment, same basis |
    | Employee / civil servant / jobseeker drawing benefit | instalment × *quotité*, **but limited to the income loss** |
    | Anyone who took the *Prestation Forfaitaire* option and has not cancelled it | 100 % of the monthly instalment |
    "Prestation Forfaitaire" is already included for the self-employed and the non-working [S10].
  - The income loss is defined contractually: *revenu de référence* = average monthly net taxable
    income and allowances over the **12 months** before the stoppage; *revenu de remplacement* =
    all benefits owed by social security, the employer (statute, collective agreement, company
    agreements) and any *prévoyance* schemes, recomputed at the claim date on the reference income;
    after **three consecutive years** of claim the reference income is revalued by the published
    private-sector wage index [S10].
- The CCSF criteria list makes the *forfaitaire* basis an explicitly selectable lender requirement
  in two places — "prestation égale à la mensualité assurée sans référence à la perte de revenu
  subie pendant le sinistre" for incapacity and "prise en charge de l'invalidité totale, sans
  référence à la perte de revenu subie" for invalidity [R11] — and the 2015 avis tells lenders to
  state the required value, "par exemple son caractère forfaitaire ou indemnitaire" [R11].

### 7. Capital initial versus capital restant dû — the second modelling switch

Two independent things are at stake, and the sources keep them separate.

**(a) The benefit base.** Death, PTIA and capital-form IPT pay the **capital restant dû** in every
group contract retrieved [S1][S5][S9][S10][S11], plus interest accrued since the last instalment
at CNP and MAIF [S9][S11]. The one exception in this set is MetLife's individual term-life
contract, which pays a **scheduled capital garanti** [S12]. CNP defines the two terms formally:
*capital assuré* = *capital initial* × *quotité*; *capital initial* = the amount borrowed at the
credit contract's inception; *capital restant dû* = the share of the borrowed capital the borrower
still owes at a given date [S9]. Cardif's lexique is equivalent [S1].

**(b) The premium base.** This is where the market genuinely splits.
| Contract | Premium base | Age used | Resulting shape |
|---|---|---|---|
| BPCE A340G [S10] | "en pourcentage du **capital initial** du prêt **ou** du **capital restant dû**" × *quotité* | — | both offered |
| CNP A217Y [S9] | rate applied **au capital initial** | age at adhesion | level |
| BFM 7371 M [S13] | annual rate × **capital initial assuré** × *quotité* | age at signature of the adhesion form | level — "Le taux de prime a été **nivelé** sur la durée du prêt" |
| MAIF [S11] | set on the **capital initial du prêt**, "définie pour la durée totale du contrat" | age at adhesion | level |
| Cardif *cotisations fixes* [S1] | on the financed capital; net-of-tax premium "garanti pendant toute la durée du contrat" | age at the guarantees' effective date | level |
| Cardif *cotisations variables* [S2] | rebased on the **capital restant dû** | *l'âge de l'assuré* (attained) | decreasing |
| APRIL PRT150115 [S5] | base is the guaranteed loan amount, but at **1 January each year** the premium reflects the guaranteed **CRD** and the age attained at 31 December | attained | decreasing, annual steps |
| APRIL Intégrale, *cotisation variable* [S8] | first premium on the initial *Montant garanti*, later premiums on the guaranteed **CRD at 1 January** | attained at 31 December | decreasing, annual steps |
| APRIL Intégrale, *cotisation constante* [S8] | always the initial *Montant garanti* | age at the guarantees' effective date | level |
| APRIL Optimum + (variable) [S7] | "change tous les ans en fonction de l'âge de l'emprunteur et du montant du capital restant dû" | attained | decreasing |

- Consequences to model. A level premium on the *capital initial* is a **nivelé** rate: the insurer
  overcharges early and undercharges late relative to the annual risk, so a genuine
  policy-year-by-policy-year projection of a level-premium book must carry the corresponding
  reserve. BFM states the nivelé design in terms and draws the consequence that the cessation of
  the PTIA and ITT guarantees at 65 "n'a pas d'incidence sur le montant de la prime" [S13] — the
  cover shrinks and the premium does not. The regulatory name for the reserve that such a design
  implies is not established by any document retrieved here; treat the reserving treatment as
  **[unverified]** and see "Gaps and caveats" §9.
- A CRD-based premium with an annually re-read attained age is, by construction, a one-year
  renewable rate on a declining sum insured: no level-premium reserve is implied and the premium
  profile follows the amortisation schedule multiplied by a rising age-rate [S5][S7][S8][S2].
- Partial early repayment: Cardif *fixes* rebases on the original borrowed capital less the
  repayment [S1]; Cardif *variables* on the CRD in force before the repayment less the repayment
  [S2]; CNP and BPCE on the guaranteed CRD less the repayment [S9][S10]; BFM sets the insured
  capital to the new loan amount with the *quotité* unchanged [S13].
- Late-joining co-borrowers and guarantors are always priced on the **CRD at the date of their
  adhesion form**, whatever the contract's normal base [S9][S10][S13].
- Tariff drivers, retrieved: financed capital, *quotité*, age, smoker status, occupation, chosen
  guarantee combination and options, payment frequency and the current rate table plus any
  underwriting loading (Cardif [S1]); age at adhesion, loan term, loan type, guarantees and
  options including the chosen *franchise* and any exclusion buy-back (CNP [S9]); guarantees,
  adhesion date, age, occupation and its conditions, smoker status, declared medical and sporting
  risks, loan characteristics, *capital initial*, *quotité* and the co-borrower insured (MAIF
  [S11]); age at adhesion and the chosen *franchise* (BFM [S13]). **Cardif applies a unisex
  tariff** [S3].
- Premium revision: Cardif guarantees the net-of-tax premium for the whole term but revises it
  **downward** on a change of life habits reducing the risk (change of occupation, 24 months
  without tobacco) and may revise the **perte d'emploi rate only**, at renewal, with three months'
  notice, if the unemployment risk's actuarial characteristics justify it — the member may then
  cancel [S1][S3]. APRIL and MAIF pass on tax changes [S5][S11].
- Frequency and lapse mechanics: premiums payable in advance monthly, quarterly, half-yearly or
  annually [S1][S9][S11][S12]; Cardif reserves the right to change the frequency if a fraction
  falls below €15 and charges a one-off €10 file fee [S1][S3]. Non-payment follows art. L. 113-3
  for individual contracts — formal notice, suspension 30 days later, cancellation 10 days after
  that [S1][S5] — and art. L. 141-3 for group contracts: exclusion 40 days after the notice, and
  contractually 120 days once an over-indebtedness commission has fixed the liabilities [S9][S10].

### 8. Quotité

- Definition: the percentage of the borrowed capital insured on one life, chosen on the adhesion
  form; it applies to **every** guarantee of that insured's cover [S1][S9][S11].
- **Per insured, the *quotité* may not exceed 100 %** [S1][S5][S9][S11]. CNP sets the granularity:
  "par tranche de 1 % à 100 %" [S9].
- Across co-borrowers the total may exceed 100 %. CNP's worked example: on a €100 000 loan the
  borrower takes 100 % and the co-borrower 40 %, so the insurer pays 100 % of the CRD or
  instalment on the first life and 40 % on the second [S9]. Cardif's: 80 % and 60 % [S1]; the
  brochure's: 60 % and 40 % [S3].
- **The claim that the total must be at least 100 % and may reach 200 % is [unverified] as a
  contractual rule.** No retrieved notice imposes a 100 % floor — that is a lender requirement,
  set through the *fiche personnalisée* and the FSI's "garanties minimales exigées par le prêteur"
  block [R9][R11], not an insurance-contract term. The 200 % ceiling follows arithmetically from
  the per-head 100 % cap. Cardif's *option Prévoyance* is available only where "la somme des
  quotités des deux assurés doit être inférieure à 200 %" [S1] — that is, it exists precisely to
  fill the gap up to 200 % and is unavailable once the gap is closed.
- Anti-duplication: "le contrat … ne peut, en aucune façon, donner lieu à une indemnisation
  supérieure à 100 % en cas de sinistres concomitants ou non pour deux assurés d'un même contrat
  de prêt" (Cardif [S1]); MetLife has the same clause [S12]; MAIF caps the total paid on one loan
  at the CRD [S11].
- *Option Prévoyance* (Cardif [S1][S3], APRIL [S5][S6]): the uninsured *quotité* is covered for a
  beneficiary of the member's choosing rather than for the lender, so that on death or PTIA the
  bank is repaid its share and the survivor receives the balance. Combined *quotité* must stay
  ≤100 % of the loan for the APRIL version [S5].
- Raising a *quotité* mid-contract requires fresh underwriting [S9].

### 9. Pricing disclosure — TAEA and the fiche standardisée d'information

- **TAEA = TAEG(with the proposed insurance treated as fully required) − TAEG(with no insurance
  required)**, both computed under arts. R. 314-1 to R. 314-10 [R6]. It is therefore a difference
  of two internal rates of return on the credit's cash flows, not a rate applied to a balance.
- Three mandatory cost presentations before the offer [R4, L. 313-8]:
  1. the **TAEA**, expressed so that it can be compared with the loan's TAEG;
  2. the total cost **in euros over eight years** and **over the full term of the loan**;
  3. the cost **in euros per instalment period**, saying whether it is added to the loan
     instalment.
  The insurance notice must also state the cancellation right [R4]. In force 1 June 2022 [R4].
- **FSI** — delivered at the first simulation for a loan above **€75 000** secured by a mortgage or
  comparable security on residential property [R4, L. 313-10], to **each borrower and co-borrower**
  [R5, R. 313-10], in the model annexed to the code [R19]. Its content is fixed by R. 313-9:
  guarantee definitions, the lender's minimum requirements, the guarantees chosen with the
  *quotité*, the personalised cost estimate (per-period cost, total cost, TAEA for the whole loan
  per R. 314-12), and notice of the right to insure elsewhere with the conditions and time limits
  [R5]. The model has eight parts, with part 7 carrying the cost table and, since the 2022
  amendment, the eight-year total and a statement of whether the premium is level or variable with
  its minimum and maximum [R9][R10].
- Part 4 of the FSI model carries **the lender's minimum required guarantees with a required
  *quotité* box for each of Décès, PTIA, ITT, IPT, IPP and perte d'emploi** [R9] — that is the
  place where the lender's *quotité* floor is actually expressed.
- Since 1 June 2022 the FSI must also state that the invalidity guarantee is independent of the
  social-security notion of invalidity, and must carry the medical-questionnaire exemption and the
  switching right [R10].
- **No retrieved source publishes an actual TAEA figure or a rate card.** The only quantitative
  pricing evidence retrieved is the CCSF's aggregated tariff series [R12] (see §12) and one
  advertising claim: APRIL's "up to €15 000 saved", built on a 37-year-old non-smoking
  professional couple borrowing €200 000 over 20 years at 2 % with effect 1 January 2017, sourced
  to the Observatoire BAO February 2016 [S6]. That is a marketing illustration, not a tariff.

### 10. Age limits, in one place

| Guarantee | Cardif [S1][S3] | CNP A217Y [S9] | BPCE A340G [S10] | MAIF [S11] | APRIL PRT150115 [S5] | APRIL Optimum + [S6][S7] | BFM 7371 M [S13] | MetLife [S12] |
|---|---|---|---|---|---|---|---|---|
| Adhesion, Décès | 18 to <85 | 66–80 for the death-only note | — | — | — | to 80 | <65 | — |
| Adhesion, PTIA | 18 to <65 | — | — | — | — | to 80 | <65 | — |
| Adhesion, ITT/IPT/IPP | 18 to <65 | — | — | — | — | to 64 | <65 | — |
| Adhesion, PE | 18 to <61 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Cover ends, Décès | renewal after 90 | 85 | 80 | 85 | 31 Dec of the 85th yr | 85 (brochure) / 31 Dec of the 90th yr (DIPA) | month after 75 | per conditions particulières |
| Cover ends, PTIA | renewal after 65 (70 by option) | 70 | 67 | 70 | 31 Dec of the 70th yr | 71 | 65 | 70 |
| Cover ends, ITT/IPT/IPP | renewal after 65 (70 by option), and at definitive cessation of work | 70 | 67 | 67 | 31 Dec of the 70th yr while working | 71 (65 without "Extension 65+") | ITT: first instalment after 65; no IPT/IPP | ITT 65 or 70 by option; IPT/IPP 70 |
| Cover ends, GAF | n/a | 67 | n/a | n/a | n/a | n/a | n/a | n/a |

Every incapacity/invalidity guarantee also ends on retirement or pre-retirement, however early,
unless the retirement itself results from the insured state being indemnified [S1][S9][S10][S11].
Cardif maintains ITT after a partial pension liquidation where employment continues alongside a
pension [S1].

### 11. The CCSF *liste de place* — the 18 criteria and the 8 perte d'emploi criteria

The lender selects **at most 11** of the 18, plus **at most 4** of the 8 on perte d'emploi, and
must state the required value wherever possible [R11][S3][S4]. Transcribed from the annex [R11]:

*Common to Décès, PTIA, invalidité and incapacité*
1. Cover of the amateur sports practised by the borrower at the date of subscription — Yes/No.
2. Maintenance of cover on travel worldwide, personally and professionally/for humanitarian work
   — Yes/No for each.

*Garantie Décès*
3. Death cover for the whole term of the loan — Yes/No.

*Garantie PTIA*
4. PTIA cover for the whole term of the loan — Yes/No.

*Garantie incapacité*
5. Cover for the whole term of the loan — Yes/No.
6. *Délai de franchise* — ≤30 / ≤60 / ≤90 / ≤120 / ≤180 days.
7. For a working person, assessment by reference to the occupation practised at the date of the
   claim — Yes/No.
8. For a working person, benefit equal to the insured instalment with no reference to the income
   lost during the claim — Yes/No.
9. Maintenance of cover on a therapeutic part-time return, with a minimum 50 % benefit for at
   least 90 days — Yes/No.
10. Cover of the non-working at the date of the claim — Yes/No, and if yes the benefit rate:
    1–49 % / 50–99 % / 100 %.
11. Cover of back conditions — without any hospitalisation or surgery condition / with a
    hospitalisation (<10 days, or 10 days and more) or surgery condition.
12. Cover of psychiatric conditions — without any hospitalisation condition / with a
    hospitalisation condition (<10 days, or 10 days and more).

*Garantie invalidité*
13. Cover for the whole term of the loan — Yes/No.
14. Assessment by reference to the occupation practised at the date of the claim — Yes/No.
15. Cover of total invalidity with no reference to the income lost at the date of the claim —
    Yes/No.
16. Cover of partial invalidity (IPP) **from 33 %** — Yes/No.
17. Cover of back conditions — same options as 11.
18. Cover of psychiatric conditions — same options as 12.

*Garantie perte d'emploi (8, of which at most 4)*
1. Cover for the whole term of the loan with no age limit — Yes/No.
2. *Délai de carence* — ≤3 / ≤6 / ≤12 months.
3. *Délai de franchise* — ≤60 / ≤90 / ≤120 days.
4. Indemnification period per claim — ≥12 / ≥24 months.
5. Total indemnification period of at least 36 months — Yes/No.
6. Share of the instalment covered — ≤50 % / ≤75 % / <100 % / 100 %.
7. Benefit equal to the instalment with no reference to income lost — Yes/No.
8. Cover with no CDI-seniority condition — Yes/No.

The annex's header also carries a *quotité* box for each of Décès, PTIA, ITT, IPT, IPP and perte
d'emploi, "exigés par le prêteur" [R11] — the same structure later mandated in part 4 of the FSI
model [R9].

Process, from the same avis [R11]: the list may be updated annually by the professions after the
CCSF's opinion; each lender publishes its chosen list on its website and on the FSIs it issues; a
*fiche personnalisée* with the fully valued required criteria must be handed over as early as
possible and in any case before the loan offer; refusal reasons must be written, dated and
explicit; the method may not obstruct the AERAS convention; the ACPR and the DGCCRF supervise. In
force at the latest **1 October 2015**, with lenders bound from **1 May 2015** to motivate any
equivalence refusal only by listed characteristics.

Cardif's published self-assessment against all 18 criteria is a useful worked example of how an
alternative insurer demonstrates equivalence — including the honest entries "OUI (option jusqu'à
70 ans)" for whole-term ITT/IPT cover and "OUI (option Sérénité+)" for back and psychiatric
conditions, i.e. two of the eighteen are met only if the borrower buys an option [S3].

### 12. Market size and shape

- **Portfolio split of insured mortgages** [R12]: at 31 May 2023, 72.2 % *contrat groupe
  bancaire*, 4.4 % *contrat alternatif bancaire*, 16.0 % *contrat alternatif externe*, 7.4 %
  uninsured (2021: 73.6 / 4.4 / 15.3 / 6.7).
- **Substitution requests** received by banking networks [R12]: 99 265 (H1 2021), 121 830
  (H1 2022), 184 528 (H2 2022), 181 600 (H1 2023).
- **Acceptance rates** [R12]: 88 %–90 % (banking networks), 70 %–87 % (intermediaries).
- **Claim declines** [R12]: death/PTIA 2.5 %–4.4 % (8.3 % in 2020) on external alternative
  contracts, 2.5 %–3.8 % on bank group contracts; incapacity/invalidity 10.2 %–12.8 % on bank
  group contracts, 7.7 %–16.3 % on external alternative contracts. Claims declared in 2022 and
  still open in May 2023: 7.2 % (bank group) and 9.5 % (external alternative).
- **Tariff trend 2019→2023** [R12]: external alternative contracts with medical selection changed
  by −40 % to +16 % depending on age, cover and smoker status, with the largest falls at the
  youngest ages and for non-smokers; bank group tariffs fell 14 %–30 % across all ages; contracts
  without medical selection were repriced up by about 10 % versus 2021.
- **Premiums and contracts (narrow definition)** [R18]: individual-adhesion *contrats emprunteurs*
  written by Code des assurances undertakings, **death guarantee only** — 5 223 thousand contracts
  at end-2024 (+15.1 %), €979 m premiums (+2.5 %), €330 m benefits (−6 %). Whole-market premium
  figures around €6.8–7 bn and around 22 million contracts circulate in secondary coverage of the
  CCSF's later work but the source document could not be retrieved: **[unverified]**, see §R13.
- **Whole-of-prévoyance context** [R18]: French *prévoyance* premiums €29.2 bn in 2024 (+4.7 %),
  claims €16.6 bn (+14.5 %), claims/premiums 56.9 %.

### 13. Exclusions and underwriting outcomes (the parts that bite on experience)

- Standard exclusions across the retrieved contracts: intentional acts including suicide attempts
  and self-mutilation; suicide in the first year (Cardif carves out principal-residence financing
  up to €120 000 [S3]; APRIL excludes suicide in year 1 outright [S7]); conditions first medically
  observed before adhesion and not declared, except where the *droit à l'oubli* applies; narcotics
  and non-prescribed doses; drunk driving above the statutory limit; nuclear effects; excluded
  sports [S1][S7].
- The two commercially decisive exclusions are **affections disco-vertébrales** (back) and
  **affections psychiatriques**, both normally excluded unless hospitalisation thresholds are met,
  and both routinely bought back by a priced option: Cardif *Sérénité+* (limit €1 500 000 per
  insured, only for *franchises* ≥90 days) [S1][S3]; APRIL *Confort* and *Confort +* [S5][S6];
  MetLife's buy-back (benefit capped €350/day and €1 500 000, 90-day franchise for those causes)
  [S12]; CNP's *rachat des exclusions spécifiques* [S9]. Without the option, Cardif still covers
  psychiatric conditions requiring more than 20 continuous days of hospitalisation within six
  months of the first day off work, and back conditions requiring 9+ days' continuous
  hospitalisation or a vertebral fracture [S3].
- Underwriting outcomes: acceptance at standard terms, acceptance with a *surprime* and/or
  guarantee restrictions notified by letter the member must countersign, or refusal [S1].
- Non-disclosure sanctions are the general ones: nullity for intentional misstatement (art.
  L. 113-8) and proportional benefit reduction for good-faith misstatement (art. L. 113-9), both
  quoted in the notices [S1][S9].
- Claim-notification deadlines are short and are a real source of declines: CNP requires the ITT
  file within 90 days of the end of the *franchise*, with partial forfeiture for late notice under
  art. L. 113-2 4° [S9]; Cardif requires it within 6 months of the end of the chosen *franchise*
  [S1]; MetLife within 30 days of the end of the franchise, and refuses files received more than
  3 months after it [S12]. The CCSF found that 50 %–75 % of declines by external alternative
  insurers were mis-declarations — wrong insurer, claim inside the *franchise*, or the maximum
  cover age already passed [R12].
- Amortisation-schedule gaming is blocked: an increase in the instalments at the member's
  initiative in the 12 months before the claim (Cardif [S1]), 90 days before (CNP [S9]) or
  180 days before (BPCE [S10]) is disregarded, while a decrease is applied immediately [S9][S10].

### 14. Contract lifecycle mechanics that a projection must respect

- Cover starts at the date shown on the adhesion form or, failing that, at acceptance of the loan
  offer, or at conclusion of the adhesion if earlier; on a distance sale Cardif defers effect by
  30 calendar days unless immediate effect is requested [S1]. Provisional accidental-death cover
  runs during underwriting — Cardif up to €350 000 for at most 60 days [S1][S3]; MetLife up to
  €500 000 for 60 days for insureds under 70 [S12].
- Perte d'emploi cover starts only after a **180-day *carence*** running from the effective date
  of the other guarantees (Cardif [S1][S3]).
- The adhesion runs for an initial period ending on the anniversary of signature of the loan
  offer and renews annually by tacit renewal for the loan's term [S1]; the group policy itself is
  a one-year contract renewed annually [S9][S10].
- Cover ends at the loan's contractual expiry, on acceleration of the loan, on total early
  repayment, on cancellation, on the age ceilings, on non-payment, on nullity for intentional
  misstatement, and on payment of the death or PTIA capital [S1][S9].
- Insurable loan types and terms: amortising fixed or variable rate including VEFA, with deferrals
  ≤24 months (Cardif [S1]) or ≤35 years with total or partial deferral (CNP [S9]); in fine (CNP:
  max 10 years [S9]); *prêt relais* max 3 years [S1][S9]; *prêt à paliers*; private and vendor
  loans on death/PTIA only [S1]. Loan term 1–35 years, extendable by 5 without exceeding 40
  (Cardif [S1][S3]). Euro-denominated loans only (CNP [S9]); Cardif variables also covers
  lease-purchase [S2][S3]; APRIL covers Swiss-franc loans and BPCE has a Swiss-franc regime with
  forfaitaire ITT [S7][S10].
- Deferred-capital and in fine loans: ITT/IPP pay **interest only**, never capital [S1][S9][S10]
  [S5]. On a partially deferred loan CNP pays the initial loan amount plus accrued interest on
  death during the deferral [S9].
- Maximum insured amounts per life: €5 000 000 (CNP A217Y *encours* [S9]; MetLife IPT capital
  [S12]); €15 000 000 death/PTIA and €25 000 monthly instalment (APRIL Optimum +, reduced to
  €5 000 000 and €6 000 in the DROM) [S6][S7]; €1 500 000 where an exclusion buy-back applies
  [S1][S12]. Cardif's monthly benefit cap can be lifted by individual agreement
  ("déplafonnement") [S1][S3].
- Territoriality: cover worldwide (Cardif [S1], APRIL [S5][S7]); CNP requires documents certified
  through the French consulate outside the EU/DROM-COM/bordering countries and requires any
  medical control to take place in France [S9].
- Cancellation right on the contract itself (*renonciation*): 30 calendar days [S7][S10][S12].

---

## Variations across insurers

| Feature | Cardif Libertés Emprunteur [S1][S2][S3] | APRIL (PRT150115 / Optimum +) [S5][S6][S7] | CNP A217Y [S9] | BPCE A340G [S10] | MAIF Avantage Emprunteur [S11] | MetLife Super Novaterm Crédit [S12] | BFM 7371 M [S13] |
|---|---|---|---|---|---|---|---|
| Regime | alternative external | alternative external | alternative external (association) | bank group | alternative external (mutual) | individual contract | bank group |
| Guarantees | DC, PTIA, ITT, IPT, IPP, PE | DC, PTIA, ITT, IPT, IPP, PE (separate module), medical-professions invalidity | DC, PTIA, ITT, IPT, IPP, MTT, invalidité AERAS, GAF | DC, PTIA, ITT/IPT, IPP (option), TPT, invalidité AERAS | DC, PTIA, ITT, IPT, IPP, GIS | DC, PTIA, ITT, IPT, IPP, IP, EXO | DC, PTIA, ITT, invalidité AERAS only |
| Indemnity basis | forfaitaire | forfaitaire | forfaitaire (instalment) | **indemnitaire by default, forfaitaire by option** | forfaitaire | forfaitaire daily indemnity | instalment, no pro-rating |
| ITT franchise | 30/60/90/180 | 31/61/91/181 or 30/60/90/180 | 30/60/90/120/180 | 90, or 30 by option | 90 only | 15/30/60/90/180 | 90 or 180 |
| ITT maximum | 1 095 days | not stated; ends at consolidation | not stated; ends at consolidation | not stated; consolidation ≤3 yrs from ITT start | 1 095 days | 1 095 days | ends at 65 / amortisation end |
| IPT benefit | CRD (broker material: CRD or instalments at choice) | CRD ("en capital") or instalments ("en rente") | instalments | instalments | instalments | death capital | n/a |
| IPP benefit | (N−33)/33 × instalment, ≤100 % | flat 50 % of the ITT instalment | flat 50 % | flat 50 % | (N−33)/33 | fraction of the IPT capital | n/a |
| IPP band | 33 % to <66 % | 33 %–65 % | 33 %–65 % | 33 % to <66 % | 33 %–66 % | >33 % and <66 % | n/a |
| Premium base | capital initial (fixes) **or** CRD (variables) | initial amount, rebased on CRD each 1 January (variable) or fixed (constante) | capital initial | capital initial **or** CRD | capital initial, level | per conditions particulières | capital initial, explicitly *nivelé* |
| PTIA daily-acts test | 3 of 4 | 4 of 4 | 4 of 4 | — | — | — | — |
| Distinctive | unisex tariff; free €1 000 return-to-work lump sum; €10 file fee; Sérénité+ buy-back; 12-month "Passeport" underwriting decision | two IPT forms; "Extension 65+"; explicit forfaitaire/indemnitaire pedagogy; €25 000 monthly cap | already carries the GAF; 1 % *quotité* steps; five franchise levels | four-way benefit rule by professional status; income-loss definition with wage indexation | single 90-day franchise; premium waived throughout claims | true individual contract with a scheduled capital and daily indemnities | social-security-linked ITT trigger; whole instalments only; no IPT/IPP; explicit level rate |

Representative design for a reference implementation. The cleanest representative of the mass
market is a **group contract paying the *capital restant dû* on Décès and PTIA and the loan
instalment on ITT and IPT, with an optional IPP paying half the instalment in the 33 %–65 % band,
a 90-day *franchise*, a 1 095-day ITT limit followed by an IPT assessment at a 66 % combined
invalidity threshold, cover ending at 65–70 for the incapacity guarantees and at 85 for death, a
per-head *quotité* of at most 100 %, and a level premium expressed as an annual rate on the
*capital initial* × *quotité*** — i.e. essentially CNP A217Y [S9] with BFM's stated level-rate
design [S13]. Every other retrieved contract is a parameterisation of that skeleton, with three
switches that must be explicit configuration rather than hard-coded:
1. **benefit base for IPT** — CRD versus instalments [S7][S3][S9];
2. **indemnity basis for ITT/IPT/IPP** — forfaitaire versus indemnitaire [S10][S6];
3. **premium base** — level rate on *capital initial* versus annually re-read rate on the CRD
   [S10][S8].

Institutional variations noted but not modelled here:
- The *contrat alternatif bancaire* (4.4 % of portfolios [R12]) — an alternative contract still
  inside a banking group — was not sampled; no document for one was retrieved.
- Professional-loan adhesions are excluded from the annual cancellation right by derogation from
  art. L. 113-12 [S1] and from the Lemoine *à tout moment* right, which is tied to art. L. 313-1
  1° credits [R3].
- Consumer-credit borrower insurance is a different, much smaller product: BPCE gives consumer
  loans ≤ €21 500 death and PTIA only, with no options [S10].
- Lease-purchase (*crédit-bail*) cover restates the CRD as the total of the remaining rentals
  inclusive of tax plus any residual purchase-option value [S5][S2].

---

## Gaps and caveats

1. **The whole Banque de France / CCSF estate refused automated fetches.** `banque-france.fr`
   and `ccsfin.fr` returned HTTP 403 on every attempt, each retried once [R13][R14][R15][R20]. The
   two CCSF documents used here were obtained from mirrors — the 2015 avis via moneyvox [R11] and
   the 2023 annual report via vie-publique [R12]. **The dedicated December 2023 *Bilan de
   l'assurance emprunteur* report to Parliament [R13] was never read**; its findings enter these
   notes only through the CCSF annual report's own summary of them [R12]. Any figure attributed to
   the *bilan* that is not in [R12] is [unverified], including the widely-quoted 2024/2025 numbers
   (22.15 m contracts, €6.830 bn premiums, 496 654 substitution requests, 93.91 % acceptance,
   17.48 % alternative share).
2. **No ACPR document was retrieved at all.** No supervisory notice, recommendation or *analyses
   et synthèses* study on assurance emprunteur was obtained, because the ACPR sits on the same
   403-ing host and the session's web-search budget was exhausted before an alternative URL could
   be located. Any statement about ACPR expectations on this product would be unsupported and none
   is made.
3. **No reserving or prudential source was retrieved.** The level-premium (*nivelé*) design is
   stated in a contract [S13] and follows from the tariff structures in [S9][S11][S1], but the
   Code des assurances provisioning articles (including whatever governs a *provision pour risques
   croissants* and the claims provisions for open incapacity and invalidity claims) were not
   fetched. **Everything about how a French insurer reserves this product is [unverified] here**
   and must be sourced separately before the technical notes make any reserving claim.
4. **No tax source was retrieved.** Premiums are quoted taxes-included in the notices [S11], and
   Cardif and APRIL both provide for premium changes on a change of tax rates [S1][S5], but the
   applicable *taxe spéciale sur les conventions d'assurance* treatment of the death versus the
   incapacity/invalidity components was not established. Treat any tax rate as [unverified].
5. **No decrement, incidence or termination table was retrieved.** Nothing in this corpus gives a
   mortality basis, an ITT incidence or recovery rate, an invalidity transition rate or a
   perte d'emploi incidence rate. Insurer rate cards are proprietary and none is public; the CCSF
   tariff charts [R12] give aggregate annual premium levels by age and smoker status as chart
   series, not as tabulated numbers, and the extracted text preserves only the percentage changes,
   not the euro values behind the plotted points. **The model's decrement assumptions will
   therefore be [std] throughout.**
6. **No TAEA figure and no premium rate exists in any retrieved document.** The statutory
   definition [R6] and disclosure duties [R4][R5][R9][R10] were retrieved in full, but no filled-in
   FSI was obtained. The only euro figures available are product caps and one marketing saving
   claim [S6].
7. **The annexed FSI model is a form, not prose.** [R9] was retrieved as a consolidated LODA text
   and the annex's part-by-part structure and field list were read, but the retrieval renders a
   form template; individual box labels beyond those recorded in §9 and §11 above should be
   re-checked against the annex before being quoted.
8. **Vintage mismatch inside the Cardif and APRIL sets.** The Cardif notices [S1][S2] are the
   January 2022 editions and still describe the **pre-Lemoine** cancellation regime (12-month
   Hamon window plus annual Bourquin anniversary), citing the repealed art. L. 312-9. Their
   guarantee mechanics are current; their cancellation clauses are not. The Cardif brochure [S3]
   is likewise pre-Lemoine. The APRIL notice [S5] carries the code PRT150115 and is plainly an
   older edition than the Optimum + material [S6][S7]; where they disagree — most visibly on the
   death cover-end age, 85 in [S5] and [S6] versus 31 December of the 90th birthday year in [S7] —
   the disagreement is recorded rather than resolved, because the documents describe different
   product generations. Only CNP A217Y [S9] (2025) and the APRIL Intégrale module [S8] (2023) are
   demonstrably post-Lemoine editions.
9. **The *quotité* floor is not a contract term.** No retrieved notice requires the sum of the
   co-borrowers' *quotités* to reach 100 %. That requirement is imposed by lenders through the FSI
   and the *fiche personnalisée* [R9][R11], and the assertion that "the total must be at least
   100 %" is **[unverified]** as stated. The 200 % ceiling is arithmetic, from the per-head 100 %
   cap [S1][S5][S9][S11].
10. **The 1 095-day ITT limit is common but not universal.** It is explicit at Cardif, MAIF and
    MetLife [S1][S2][S11][S12]; CNP and APRIL instead end ITT at consolidation with no stated day
    cap [S9][S5]; BPCE fixes consolidation at three years from the start of ITT [S10]. A model
    that hard-codes 1 095 days for every carrier would misstate CNP-style and APRIL-style
    contracts.
11. **The 66 % IPT threshold and the 33 %–66 % IPP band are solid; the transition mechanism is
    not uniform.** Every retrieved contract that offers IPT uses 66 % and every one that offers
    IPP uses 33 % as the floor [S1][S5][S9][S10][S11][S12], and the CCSF criterion fixes 33 % for
    IPP [R11]. But whether IPP tops out at "below 66 %" or at "65 %" varies, and the benefit shape
    inside the band is either a linear ramp or a flat 50 % — see §5.
12. **The barème croisé formula is fitted, not quoted.** N = (IF² × IP)^(1/3) reproduces every
    published cell of the Cardif [S1] and CNP [S9] tables and both of their worked examples, but
    neither contract states it. It is a reconstruction and is labelled as such wherever used.
13. **Crédit Agricole is missing from the sample.** Its ADI notice [S14] returned HTTP 502. Since
    Crédit Agricole is reported as the largest writer of the risk, the *contrat groupe* sample
    here (BPCE, BFM) may not be representative of the largest book in the market. Generali,
    Suravenir, MNCAP, AFI-ESCA and Swiss Life were not sampled at all — the web-search budget for
    the session was exhausted before URLs for them could be located, and no URL was guessed.
14. **Loi Lagarde, loi Hamon and the Bourquin amendment texts were not retrieved.** Their content
    is recorded here only as it is described inside the retrieved CCSF avis [R11], the retrieved
    insurer documents [S1][S6] and the loi Lemoine's own amending articles [R1]. Statements about
    what those three statutes did are therefore secondary and are flagged [unverified] in §2 where
    the primary text was not read.
15. **The AERAS *grille de référence* itself was not retrieved** — only the convention's
    information document describing how it works [R17]. The pathology-by-pathology delays and the
    capped surcharge rates in lists I and II are therefore not reproduced here, and must not be
    invented. The grid is public on aeras-infos.fr and updated periodically; check it before
    quoting any specific delay other than the statutory five-year cap [R16].
