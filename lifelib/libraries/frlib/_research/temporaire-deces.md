# Term Life Assurance (Assurance temporaire décès) — research notes (France)

Research notes for the French individual standalone term life contract — *assurance temporaire
décès*, the pure protection contract that pays a *capital décès* (death lump sum) if the insured
dies inside the cover period and pays nothing otherwise. These notes cover the **standalone**
product only. *Assurance emprunteur* (ADE, borrower's cover attached to a loan) is a separate
product with its own research file; it is referenced here only where French law or French
actuarial practice treats the two differently, because several of the most useful public documents
on French mortality pricing were written about ADE.

These notes are the citation ground truth for the frlib `temporaire_deces` product documents:
source ids S1..S16 and R1..R23 below are **frozen** — never renumber. Unused ids are simply
omitted downstream, leaving gaps.

Access date for all citations: **2026-08-26**.

Citation discipline: every extracted fact is tagged `[S#]` or `[R#]` pointing at a document that
was actually fetched and read. `[unverified]` marks statements from general knowledge or from
secondary summaries of documents that could not be retrieved. Where a fetch failed the failure is
recorded and the item is kept only as a known reference (fetched_ok = false). PDF sources were
downloaded and their text layer extracted locally; where a figure is load-bearing (the MAIF tariff
grid, section 12) the extraction was re-checked against the PDF's own word coordinates.

Language note: French terms of art are kept in French — *notice d'information*, *conditions
générales*, *cotisation*, *capital décès*, *perte totale et irréversible d'autonomie* (PTIA),
*fonds perdu*, *surprime*, *participation aux bénéfices*, *délai d'attente*, *écrêtement*,
*décalage d'âge* — with a gloss on first use.

---

## Primary sources

### S1 — MAAF Vie, "Assurance décès — Notice d'information" (Réf. TDR. 014-06/2026)
- Publisher: MAAF Vie (SA, RCS Niort 337 804 819), group contract n° 02120 subscribed by ANS
  Vie-Covéa (Association Nationale des Souscripteurs Vie Covéa)
- Doc type: *notice d'information* for a *contrat d'assurance de groupe sur la vie à adhésion
  facultative*, 22 pp.
- URL: https://www.maaf.fr/fr/files/live/sites/maaf/files/DOCUMENTS/Vie_quotidienne/CG/MAAF_Conditions_generales_Assurance_deces_2313.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Document code Réf. TDR. 014-06/2026;
  tax content stated "en vigueur au 1er janvier 2026".
- Content: the richest of the retrieved documents. Contract is *branche 20 (vie/décès)* governed
  by arts. L. 141-1 ff. of the Code des assurances. Insured aged 18–75 at adhesion, excluding
  *cascadeurs* and *jockeys*, resident in metropolitan France or the DROM. Garantie I = capital
  paid on PTIA to the insured, or on death to the designated beneficiaries; optional *doublement
  du capital en cas de décès accidentel*; Garantie II = *rente éducation*; Garantie III = both.
  Death and PTIA benefits are mutually exclusive. Capital 10 000 € – 2 000 000 € (total insured
  capital capped at 2 000 000 € per insured; 1 000 000 € if the accidental-doubling option is
  taken). Rente éducation 75 € – 3 810 € per quarter per child, payable to 31 December preceding
  the child's 26th birthday, children under 25 at adhesion. Worldwide cover. Full exclusion list
  (suicide in the first year from effect and from the last increase avenant, drugs, air sports,
  motor competition, solo ocean racing, scuba and caving, war where France is a belligerent,
  riots/terrorism/*rixes*, nuclear, intentional acts, driving without a valid licence, manifest
  drunkenness, professional sport, listed dangerous sports, federated competition; occupational
  death excluded for firefighters, military, police and gendarmerie). Underwriting: *Questionnaire
  Médical Confidentiel* valid 3 months; the insurer may accept at normal rate, accept with
  *aménagements de tarification*, adjourn, or refuse; arts. L. 113-8 / L. 113-9 quoted in full.
  Adhesion runs to 31 December and renews by *tacite reconduction* each 1 January; terminates of
  right on 31 December of the year the insured reaches **85**, on death, or on payment of the PTIA
  capital. Cotisation set by garanties/option, capital and/or rente, **age of the insured at the
  effective date and then at each renewal**, age of the rente-éducation children, any *majoration*
  for particular risks, and smoker profile; age by *différence de millésime*. Fractionation
  loadings and *frais d'échéance* given as a table (section 13 below). Optional *revalorisation*
  indexes both garanties and cotisations to the *plafond annuel de la Sécurité sociale* (PASS).
  Payment of the capital within 15 days of receipt of the listed documents; conversion to a
  quarterly *rente temporaire* possible with *frais de gestion*, and a regulatory minimum annuity
  of 110 € per month is cited under art. A. 160-2. Post-death revalorisation under art. L. 132-27-2
  and a floor rate set by decree. *Participation aux bénéfices* decided globally by MAAF Vie and
  applied as higher benefits and/or lower cotisations. Full tax section (990 I / 757 B mechanics,
  152 500 €, 30 500 €, 700 000 €, exemptions under 796-0 ter) and the statement that a temporaire
  décès, unlike assurance vie, is **not** subject to *prélèvements sociaux*. Renunciation: 30
  calendar days under art. L. 132-5-2.

### S2 — Macif, "Notice d'information — Garantie Décès, Capital forfaitaire" (garanties en vigueur au 1er janvier 2019)
- Publisher: Prévoyance Aésio Macif (insurer); Macif and Macif-Mutualité (subscribers of group
  contracts n° 219.002-A and n° 219.002-B); Macif-Mutualité (gestionnaire); IMA Assurances
  (assistance)
- Doc type: *notice d'information* for a *contrat d'assurance collectif à adhésion facultative*,
  21 pp.
- URL: https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_prevoyance/PAM/NID_Deces_20190708.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the notice describes itself as a *contrat temporaire décès*. Adhesion 18–67 inclusive
  (*formule Essentielle* to 50 inclusive), residence in metropolitan France, the DROM, Monaco, or
  abroad for continuous stays not exceeding 12 months. Cover: *Capital forfaitaire décès/PTIA*
  25 000 € – 762 000 € (Essentielle 15 000 € – 24 999 €); *avance* of 4 000 € payable to a
  designated beneficiary; optional *doublement accident* where death or PTIA follows an accident
  and occurs within 12 months of it. Death cover to the *échéance principale* (1 April) of the
  calendar year following the 80th birthday; PTIA cover to the 1 April following the **75th**
  birthday. PTIA is an anticipated payment of the death capital and ends the death cover; the
  capital is only due if the insured is alive on the day of payment. *Garantie immédiate accident*
  during medical underwriting: up to 60 days from receipt of the signed application, first
  application only, limited to the amount applied for with a maximum of 76 000 €. Exclusions
  include war, terrorism/riots where the insured takes an active part, air sports (coverable by
  *surcotisation* if declared and accepted), motorised acrobatics/records, nuclear, murder by a
  beneficiary for that beneficiary's share, and **suicide within the 12 months following inception**
  (and, on an increase, for the increment). PTIA-specific exclusions for drink-driving and
  non-prescribed narcotics. Underwriting: *déclaration de santé* and, if needed, a *questionnaire
  médical*; possible outcomes are acceptance, deferral pending further examinations at the
  applicant's cost, acceptance with *surcotisation* and/or restricted cover, refusal or
  adjournment. Cotisation annual, payable in advance, evolving each year with **age** and with the
  insurer's revalorisation rate; age by *différence de millésime*; fractionation (half-yearly or
  monthly) attracts *frais de fractionnement*. Non-payment: 10 days then *mise en demeure*,
  resiliation 40 days after the letter. Renunciation 30 calendar days with full refund within 30
  days. *Participation aux bénéfices* determined globally under art. A. 331-4; guarantees
  revalorised at the *échéance principale* at a rate set by the insurer, refusable but definitively;
  post-death revalorisation not below the art. R. 132-3-1 rate, to the deposit at the Caisse des
  dépôts under art. L. 132-27-2. Marketing panel: 10 % permanent discount on the death cotisations
  of two contracts taken simultaneously by related persons (Essentielle excluded).

### S3 — MAIF VIE, "Assurance décès — Rassurcap Solutions, Note d'information"
- Publisher: MAIF VIE (SA, RCS Niort 330 432 782)
- Doc type: *note d'information* (individual contract), 24 pp. Retrieved via a third-party mirror
  (coover.fr) because MAIF's own contractual-documentation host was not reachable for this file.
- URL: https://www.coover.fr/wp-content/uploads/2021/08/assurance-deces-maif-rassurcap-solutions.pdf
- Retrieved: YES (PDF downloaded, full text extracted). **Vintage: the worked example inside the
  document is dated April 2019 / September 2019 and the mirror was posted in 2021; treat the
  tariff grid as a 2019–2021 edition, not as the current rate card** (see S4 for the current
  headline figures and the gaps section).
- Content: the only retrieved document that publishes a **full attained-age tariff grid** for a
  French standalone temporaire décès (reproduced in section 12). "Rassurcap Solutions est un
  contrat **individuel** d'assurance décès, d'une durée d'un an, renouvelable par tacite
  reconduction… contrat d'assurance sur la vie, régi par le Code des assurances (branche 20 :
  Vie-décès)"; the notice states explicitly that, given its characteristics, it **is not a loan
  cover**. Risks: death from any cause, and *Invalidité Permanente Absolue* (IPA) from any cause —
  MAIF's name for the PTIA acceleration — payment of which ends the contract. Death cover runs to
  the *date d'échéance* following the insured's **75th** birthday, IPA cover to the échéance
  following the **65th**. Capital: chosen by the subscriber, minimum 20 000 €; decreases allowed
  subject to the minimum; increases allowed to the échéance following age 65 with fresh medical
  formalities, plus a *forfait* increase of 5 000 € every 5 years without medical formalities and
  the same 5 000 € forfait within 12 months of birth, adoption, marriage, PACS, divorce, PACS
  break-up or the death of the spouse/partner — at most 4 formality-free increases over the life
  of the contract. Three payout modes (capital; rente; *versement mixte famille*), with a matrix by
  beneficiary type; annuity conversion uses "la table de mortalité en vigueur au jour de la
  conversion du capital en rente et un taux d'intérêt technique défini à cette date", **frais de
  service de la rente 3 % du capital à convertir**, and a legal minimum of 480 € per year cited
  under art. A. 160-2. *Avance* of up to 4 000 € to the spouse/PACS partner within 48 h. Provisional
  accident cover from receipt of the application for up to 30 days, capital limited to 15 000 €.
  Subscription conditions: legal majority, residence in France/DROM, not under *tutelle* nor
  hospitalised in a psychiatric establishment, **not more than 65 (until the day before the 66th
  birthday)**, medical formalities satisfied, one individual death contract per person at MAIF VIE.
  Underwriting outcomes: insure without reserve; insure with partial exclusions and/or
  *surtarification* subject to acceptance; decline. Renunciation 30 days under art. L. 132-5-1.
  Exclusions listed in section 9 below. Cotisation "calculé en fonction de l'âge de l'assuré à la
  date d'effet **puis de reconduction** du contrat, du tarif en vigueur à la même date, du montant
  du capital choisi", with a possible *majoration* for particular risks; premiums are collected at
  the latest to the échéance following the 75th birthday, and if a claim occurs during medical
  underwriting the temporary death premium is deducted from the capital due. Full tax section:
  capital exempt from *droits de succession*; annual premium paid before 70 exceeding 305 € to be
  declared in full; cumulative premiums after 70 declared with only the fraction above 30 500 €
  subject to *droits de succession*; annuity taxation table by age at entry (70 % / 50 % / 40 % /
  30 %), social contributions at 17.2 % on the taxable fraction, *rente temporaire* exempt from
  income tax but not from social contributions, IPA capital exempt from income tax.

### S4 — MAIF, "Assurance Décès : Protégez vos proches" (product page, Rassurcap Solutions)
- Publisher: MAIF
- Doc type: insurer product page (current edition)
- URL: https://www.maif.fr/famille-vie-quotidienne/assurance-deces
- Retrieved: YES.
- Content: current headline parameters for the same product as S3 — minimum capital 20 000 €, no
  stated overall ceiling; **simplified underwriting (no medical examination) up to age 40 for a
  capital of up to 250 000 €**; maximum subscription age 65; guarantees décès, PTIA, plus a
  *maladie grave* flat capital of 5 000 € and a 3-year suspension of the spouse's cotisations after
  a death; published price point **6,29 € per month for a 35-year-old for a capital of 40 000 €**;
  and the explicit statement that the cotisation "est déterminée en fonction de votre âge à la date
  d'effet et à chaque reconduction de votre contrat (recalcul chaque année)". The page does not
  mention any *valeur de rachat*.

### S5 — MAIF, consumer guide pages "Assurance décès à fonds perdus" and "Fin du contrat d'assurance décès"
- Publisher: MAIF
- Doc type: insurer consumer-guide pages (two URLs, both retrieved)
- URLs:
  - https://www.maif.fr/famille-vie-quotidienne/guide-assurance-deces/a-fonds-perdus (page dated 31 March 2023)
  - https://www.maif.fr/famille-vie-quotidienne/guide-assurance-deces/fin-de-contrat-assurance-deces (page dated 9 August 2018)
- Retrieved: YES (both).
- Content: the *fonds perdu* characterisation stated by an insurer in its own words — if the
  insured survives to the end of the contract, "les cotisations versées restent acquises à
  l'assureur", or the contract is renewed automatically; a temporaire décès offers no *rachat*
  whereas a *vie entière* contract does, the latter carrying a *tableau de rachat* showing
  recoverable amounts by duration; a temporaire décès is not a savings vehicle and nothing is
  repaid absent the insured event. Restates the simplified-underwriting parameters (to age 40 for
  up to 250 000 €, minimum 20 000 €).

### S6 — Mutex, "Assurance Décès — Conditions générales / Notice d'information" (doc 20318)
- Publisher: Mutex (group contract, *adhésion facultative*)
- Doc type: *conditions générales* / *notice d'information*, 16 pp.
- URL: https://www.mutex.fr/app/uploads/2022/06/20318_-_assurance_deces_-_conditions_generales.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the clearest retrieved statement of French **underwriting thresholds and waiting-period
  mechanics**. Adhesion from 18 (*révolus*) to 80 (*différence de millésime*); the adhesion ends of
  right at its anniversary in the year the insured reaches **85 (death cover) / 80 (PTIA)**.
  Capital capped at 200 000 € (100 000 € for adhesions from age 70 with the accidental-doubling
  option); *acompte* of 5 000 € to the spouse/concubin/PACS partner or the sole named beneficiary.
  PTIA cover is compulsorily attached to the death cover; its payment terminates the adhesion.
  Optional accidental cover pays an **additional capital equal to the death capital** where death
  or PTIA follows an accident within one year, the causal link to be proved by the claimant.
  Formalités médicales table: capital ≤ 40 000 € **and** age ≤ 50 → no medical formality, but the
  illness-caused death/PTIA cover then only takes effect after a **12-month *délai d'attente***
  (death during that period returns the premiums collected to the heirs); capital > 40 000 € →
  *questionnaire médical*, no waiting period; age > 50 → *Déclaration de Bonne Santé*, escalating to
  a *questionnaire médical* if any box is ticked "OUI". Acceptance with reserves means one or more
  exclusions and/or a *majoration de tarif appelée sur cotisation*, to be returned within 15 days
  marked "BON POUR ACCORD". Exclusions include suicide or attempted suicide in the first year
  following the effective date of the adhesion **or of any increase**, intentional acts, alcohol
  above the Code de la route limit, drugs and non-prescribed tranquillisers, and a list of hazardous
  occupations. Cotisation "déterminée en fonction de votre âge et des informations que vous avez
  fournies à l'adhésion notamment concernant votre état de santé", payable annually in advance with
  half-yearly, quarterly or monthly options, and evolving each year at the adhesion anniversary with
  **age** and with revalorisation, and also with garantie changes, legislative changes, and "les
  résultats des garanties Assurance Décès". Non-payment: 10 days, then LRAR, then definitive
  resiliation 40 days later with no cover for events in the suspension window. Post-death
  revalorisation under art. L. 132-5 at the lower of the 12-month average TME (*taux moyen des
  emprunts de l'État français*) calculated at 1 November of the preceding year and the last TME
  available at that date.

### S7 — AXA France Vie / ANPERE, "Prévoyance — Notice d'Information Avizen"
- Publisher: AXA France Vie and AXA Assurances Vie Mutuelle; subscriber ANPERE
- Doc type: *notice d'information* for a *contrat d'assurance de groupe à adhésion facultative*,
  40 pp. Retrieved via a third-party mirror.
- URL: https://guide.reassurez-moi.fr/guide/wp-content/uploads/2018/12/conditions-generales-assurance-deces-axa.pdf
- Retrieved: YES (PDF downloaded, full text extracted). **Vintage: the tax section states "le
  régime fiscal français en vigueur au 01/09/2013"; the structural clauses are used here, the tax
  figures are taken from S1/R14–R16 instead.**
- Content: the retrieved document that states the no-surrender rule in an insurer's own words —
  **"Article 13 - Rachat et réduction. Votre adhésion ne comporte ni valeur de rachat, ni valeur de
  réduction."** Contract falls under *branches* 20 (Vie-décès), 1 (Accident) and 2 (Maladie) of art.
  R. 321-1. Death capital payable if death occurs before the end of the insurance year in which the
  insured reaches **85**; *Invalidité Permanente Totale* (IPT) accelerates the same capital, payable
  if consolidation occurs while the cover runs — before retirement and at the latest before the end
  of the insurance year in which the insured reaches **67**. Riders: *capital décès par accident*
  (death within 12 months of the accident; IPT by accident within 24 months); *capital décès double
  garantie* (a further capital if the insured, already in IPT, dies at least one year after
  consolidation); *garantie double effet* (a further capital equal to the one already paid, to the
  children fiscally dependent on the spouse/partner/concubin, if that person dies simultaneously or
  later); *rente éducation* to the child's 26th birthday with steps of **100 % (ages 0–11), 125 %
  (12–17), 150 % (18–26)** of the subscribed amount, continued for life for a disabled beneficiary
  under stated conditions; *rente décès* reduced by **50 %** from the beneficiary's 65th birthday.
  Annuities are paid quarterly in arrears with a *certificat de vie* each January. Cotisation is
  set by **the insured's age, a tariff group defined by occupation, and smoker/non-smoker status**,
  and also depends on medical acceptance conditions, working conditions and sporting activities;
  age is the *différence de millésime*, computed at adhesion and re-computed at each anniversary;
  art. L. 132-26 governs errors of age (cover void and premiums returned if the true age is outside
  the limits; otherwise benefits reduced or the premium surplus refunded). Premiums payable in
  advance monthly/quarterly/half-yearly/annually within 10 days; non-payment → LRAR → resiliation 40
  days later with premiums already collected staying with the insurer; premium payment stops on
  death or on recognition of IPT (IPT also suspends payment). Indexation option reprices garanties
  and cotisation by the PASS movement without medical examination, ceasing at the anniversary in
  the year the insured reaches **70**; refusal of indexation is definitive. Capital may be raised by
  up to **20 %** without medical selection within 3 months of marriage/PACS/birth/adoption. Suicide,
  conscious or unconscious, is excluded in the first year of insurance and again for the increment
  after any increase. Loi Evin art. 6 lets the insurer terminate the **non-death** guarantees within
  the first two years.

### S8 — ANTARIUS (Société Générale group), "Assurance Temporaire Décès — Document d'information sur le produit d'assurance" (Antarius Protection Premium, Série C, février 2018)
- Publisher: ANTARIUS SA (SIREN 402 630 826), distributed through Crédit du Nord and associated banks
- Doc type: **IPID** (*document d'information sur le produit d'assurance*), 2 pp.
- URL: https://www.assurances.societegenerale.com/fileadmin/2023/IPID/Antarius/IPID_APP_022018.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Release code
  `T3_18_V17.1_20180926.00`, "Document Réf : Série C – Février 2018".
- Content: a *bancassurance* variant. "Ce produit, dédié aux particuliers de **18 ans à moins de 66
  ans**, prévoit le versement d'un capital garanti aux bénéficiaires désignés en cas de Décès de
  l'assuré, ou à l'assuré en cas de Perte Totale et Irréversible d'Autonomie (PTIA)". Capital
  **100 000 € – 1 000 000 €**; *avance* of 10 % of the capital capped at **10 000 €** paid within two
  days of the death declaration; a *Double Effet* rider paying a further capital equal to the
  guaranteed capital and **capped at 500 000 €** where the spouse dies before their 70th birthday
  or suffers PTIA before their 65th, simultaneously with or after the insured's death or PTIA, to
  the children fiscally dependent at both dates. Death cover ceases at the adhesion anniversary
  following the insured's **70th** birthday; PTIA at the anniversary following the **65th**.
  Exclusions: legal exclusions (intentional acts of the insured or beneficiaries, war/insurrection/
  riot/*rixes* with active participation), suicide or attempted suicide in the first year of the
  adhesion, consequences of a condition pre-dating the effective date, non-prescribed narcotics,
  accidents with blood alcohol at or above the legal limit, professional sport, *parapente* and
  bungee jumping, off-piste snow sports, competitions and dares. Cotisations payable annually in
  advance with quarterly or monthly fractionation, by direct debit. Cover is worldwide but is
  conditional on holding a bank account at Crédit du Nord or an affiliate and on remaining tax
  resident in metropolitan France or Monaco — **all guarantees cease if either condition fails**.
  Annual contract renewed by *tacite reconduction*; resiliation at any time by registered letter,
  effective the day before the following premium due date.

### S9 — MUTUALP / mutuelle LA FRONTALIÈRE, "Notice « GARANTIE DÉCÈS » — Notice d'information valant Conditions Générales au 1er janvier 2023" (n° 06015000005/01)
- Publisher: MUTUALP (insurer, Livre II du Code de la mutualité); mutuelle LA FRONTALIÈRE
  (subscriber, SIREN 421110305)
- Doc type: *notice d'information valant conditions générales*, 9 pp.
- URL: https://www.mutuelle-lafrontaliere.fr/storage/app/media/documents%20pr%C3%A9voyance/NOTICE%20DECES%20MUTUALP_LA%20FRONTALIERE_2023.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: a *mutualité*-sector contract, useful precisely because it is governed by the **Code de
  la mutualité** rather than the Code des assurances and still behaves identically. Self-described
  as "un contrat d'assurance collectif à adhésion facultative **de type « assurance temporaire
  décès »**". The regulatory summary box states three things this library needs verbatim: "Le
  capital garanti n'est pas égal aux sommes versées par l'Adhérent"; "**Le contrat ne prévoit pas de
  participation aux bénéfices**"; "**Le contrat ne comprend pas de faculté de rachat**". *Délai
  d'attente*: the right to the capital is acquired after **3 months** from the effective date, waived
  for accidental death or where the insured already held equivalent or higher cover through the
  subscriber for more than three months. Base capital **6 097,96 €**, extensible by a supplementary
  death capital up to a **45 000 €** ceiling; accidental death pays a supplementary capital equal to
  **50 %** of the death capital, for deaths within 12 months of the accident. Increases only below
  age 50, subject to renewed medical formalities. Guarantees cease at the latest on **31 December of
  the year of the 65th birthday**. Cotisations determined each year by **attained age**, the change
  taking effect on 1 January of the civil year following the birthday, payable annually,
  half-yearly, quarterly or monthly in advance by direct debit on the 10th. Territorial scope:
  worldwide for professional and personal stays not exceeding **60 consecutive days per civil
  year**. Exclusions: war, nuclear, aviation outside commercial lines, hang-gliders/paragliders and
  parachuting, **suicide or attempted suicide in the first year following adhesion**, combat and
  mechanical sports in competition, listed competition activities (bobsleigh, rafting, freestyle
  skiing, caving, canyoning, mountaineering), and any activity prohibited by law; separate
  exclusions for the accidental-death cover. Non-payment: cover suspended **30 days after the mise
  en demeure** (the *mutualité* timetable, shorter than the Code des assurances' 40 days).
  Withdrawal at 31 December on request before 1 November (art. L. 221-10 Code de la mutualité);
  renunciation under art. L. 223-8 Code de la mutualité. Late payment of the capital carries
  interest at twice the legal rate.

### S10 — MetLife France, "Assurance décès : protéger sa famille" (product page)
- Publisher: MetLife France
- Doc type: insurer product page
- URL: https://www.metlife.fr/assurance-prevoyance/assurance-deces/
- Retrieved: YES. No page date shown.
- Content: the widest age and capital envelope found. Subscription **18–84**; temporary death cover
  ceasing at **90**. Capital up to **50 M€** for death and up to **20 M€** for the PTIA option.
  Optional *rente de conjoint* up to 5 000 €/month and *rente éducation* up to 2 000 €/month per
  child. Pricing depends on "âge, état de santé, antécédents médicaux, profession, fumeur ou non",
  with non-smoker status revisable downwards after 12 months without tobacco. Published price point
  **8,24 € per month in year one for a 40-year-old non-smoker with a capital of 50 000 €** — the
  phrase "in year one" is the page's own signal that the cotisation is revised thereafter.
  Exclusions: suicide within the first 12 months, undeclared conditions, drugs, alcohol above the
  legal threshold.

### S11 — MetLife France, "Assurance décès à fonds perdus" (guide page)
- Publisher: MetLife France
- Doc type: insurer guide page
- URL: https://www.metlife.fr/assurance-prevoyance/assurance-deces/fonds-perdu/
- Retrieved: YES.
- Content: an insurer's own definition of the *fonds perdu* character: a temporaire décès pays a
  capital or annuity to beneficiaries on death before an age limit, and if death does not occur
  during cover "les cotisations auront été versées « pour rien »". Contrast drawn with the *vie
  entière* contract, which covers death whenever it occurs and permits partial or total recovery of
  premiums through a surrender clause, at a higher premium. Recommends cover of both death and
  PTIA. No figures.

### S12 — MACSF, "Plan de prévoyance — libéraux" (product page)
- Publisher: MACSF
- Doc type: insurer product page (with links to three *DIPA* product-information PDFs by
  profession — médecins libéraux, chirurgiens-dentistes, infirmières)
- URL: https://www.macsf.fr/nos-produits-services/sante-prevoyance/prevoyance/plan-de-prevoyance/plan-de-prevoyance-liberaux
- Retrieved: YES (page). **The three DIPA PDFs were NOT retrieved — the page exposes only truncated
  `/content/download/...` paths.**
- Content: the source for the **triplement accidentel** variant. Capital paid on death and on
  *IFTD* (*invalidité fonctionnelle totale et définitive* — MACSF's name for the PTIA
  acceleration); the base capital is **doubled** if death or IFTD results from an accident and
  **tripled** if it results from a road-traffic accident, terrorism, an *attentat* or an
  *agression*. Adhesion until the day before the **57th** birthday (day before the **50th** for
  *infirmières*); private-sphere guarantees, including the death capital, modifiable until the day
  before the **65th** birthday. No premium structure, capital amounts or tariff figures on the page.

### S13 — La Banque Postale, "Assurance temporaire décès" (guide page, 31/05/2023)
- Publisher: La Banque Postale
- Doc type: insurer/bank guide page
- URL: https://www.labanquepostale.fr/particulier/accompagner/actualites-et-conseils/actus/assurance-temporaire-deces.html
- Retrieved: YES. Page dated 31/05/2023.
- Content: cover normally runs one year with *tacite reconduction*, with some contracts extending
  to 5 years; guarantees are death plus total disability from illness or accident; some formulas
  cover all causes including suicide after the 12-month waiting period; premiums are set annually
  and depend on the target capital, the subscriber's age and health, and are higher where health is
  impaired; if death does not occur the capital is not repaid and the cotisations are definitively
  lost. Tax figures consistent with R14–R16.

### S14 — Abeille Assurances, "Assurance décès vie entière ou temporaire"
- Publisher: Abeille Assurances (ex-Aviva France)
- Doc type: insurer guide page
- URL: https://www.abeille-assurances.fr/conseils-en-assurance/mes-proches/assurance-deces-vie-entiere-ou-temporaire.html
- Retrieved: **NO — HTTP 403 Forbidden on two attempts** (host blocks automated fetches). Kept as a
  known reference only; nothing is cited from it.

### S15 — Previssima, "Qu'est-ce qu'une assurance temporaire décès ?" (updated 11 February 2025)
- Publisher: Previssima (French insurance and social-protection reference site) — **secondary**, not
  a product document
- Doc type: reference article
- URL: https://www.previssima.fr/question-pratique/quest-ce-quune-assurance-temporaire-deces.html
- Retrieved: YES.
- Content: the source for the **capital constant / capital décroissant** distinction in the French
  market. *Capital constant* = a fixed sum payable throughout; *capital décroissant* = a sum
  following an amortisation schedule, "common in loan insurance". Contracts are typically annual
  with *tacite reconduction*, some insurers offering 5-year renewal periods. "Si le risque garanti
  ne survient pas pendant cette période, aucune somme n'est versée." Exclusions cited: suicide,
  extreme sports, undisclosed pre-existing illness. No Code des assurances article references.

### S16 — Meilleurtaux, "Focus assurance temporaire décès" (page dated 22 June 2026)
- Publisher: Meilleurtaux (broker) — **secondary**, not a product document
- Doc type: broker guide page
- URL: https://www.meilleurtaux.com/comparateur-assurance/assurance-deces/guide-assurance-deces/focus-assurance-temporaire-deces.html
- Retrieved: YES.
- Content: minimum age 18, maximum "souvent à 70 ans" with some insurers accepting older
  applicants; durations of **10, 15 or 20 years** cited as examples alongside the annual form; two
  formula families — accidental death only, or all causes with suicide covered after 12 months; the
  *fonds perdus* statement "aucun capital n'est versé et les cotisations déjà payées ne sont pas
  remboursées". No tariff figures and no statement on level versus attained-age premiums.

---

## Regulatory and actuarial references

### R1 — Code des assurances, art. L. 132-7 (suicide)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006792964
- Retrieved: YES (two independent fetches, consistent). **Version en vigueur : 20 août 2026**,
  modified by LOI n° 2026-794 du 18 août 2026 – art. 18 (V).
- Content, alinéa by alinéa:
  1. "L'assurance en cas de décès est de nul effet si l'assuré se donne volontairement la mort au
     cours de la première année du contrat."
  2. "L'assurance en cas de décès doit couvrir le risque de suicide à compter de la deuxième année
     du contrat. En cas d'augmentation des garanties en cours de contrat, le risque de suicide,
     pour les garanties supplémentaires, est couvert à compter de la deuxième année qui suit cette
     augmentation."
  3. The first alinéa does not apply to contracts under art. L. 141-1 subscribed by the bodies in
     the last alinéa of art. L. 141-6.
  4. Death cover must apply **from inception, within a ceiling set by decree**, for art. L. 141-1
     contracts subscribed by those bodies to secure repayment of a loan taken to finance the
     acquisition of the insured's **principal residence**.
  5. Death cover applies to death resulting from the *aide à mourir* under art. L. 1111-12-1 of the
     Code de la santé publique. **This alinéa is new as of 20 August 2026** and is the reason the
     article's version date is so recent.

### R2 — Code des assurances, art. R. 132-5 (the suicide-cover ceiling)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006811988
- Retrieved: YES. Version en vigueur : 5 avril 2002.
- Content, in full: "Le plafond mentionné au dernier alinéa de l'article L. 132-7 ne peut être
  inférieur à **120 000 Euros**." This is the figure that makes the *immediate* suicide cover of the
  fourth alinéa of L. 132-7 operative — and it is confined to group loan cover on a principal
  residence, i.e. it does **not** reach a standalone temporaire décès.

### R3 — Code des assurances, art. L. 132-23 (no *réduction*, no *rachat*)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038837141
- Retrieved: YES. Version en vigueur : 14 juin 2026.
- Content: first alinéa, verbatim: "**Les assurances temporaires en cas de décès ainsi que les
  rentes viagères immédiates ou en cours de service ne peuvent comporter ni réduction ni rachat.**"
  The same alinéa continues with "les assurances de capitaux de survie et de rente de survie, les
  assurances en cas de vie sans contre-assurance et les rentes viagères différées sans
  contre-assurance", which may not carry a *rachat*. For all other life contracts and capitalisation
  operations the insurer may not refuse *réduction* or *rachat*; contracts tied to occupational
  retirement may restrict them for defined periods except in hardship cases. This single article is
  the legal foundation of the *fonds perdu* character of the product and of the absence of any
  surrender-value state variable in the model.

### R4 — Code des assurances, art. A. 132-18 (tariff bases: technical rate and mortality tables)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514715
- Retrieved: YES. Version en vigueur : 7 septembre 2017 (arrêté du 14 août 2017 – art. 1). The full
  French text is additionally reproduced verbatim inside R13, which is how the clause-level detail
  below was confirmed.
- Content: tariffs of life and capitalisation undertakings "comprennent la rémunération de
  l'entreprise" and are built from (1) a technical interest rate set under art. A. 132-1, and (2)
  one of two families of tables: **(a)** tables homologated by ministerial *arrêté*, established by
  sex, on insured-population data for annuity contracts and **on INSEE data for all other
  contracts**; or **(b)** tables established by the undertaking, by sex or not, and certified by an
  independent actuary approved by a recognised actuarial association, built on the undertaking's own
  or demographically equivalent experience data. Where family (a) is used and a **single table is
  retained for all insureds, it must be the appropriate table giving the most prudent tariff**. "Pour
  les contrats en cas de vie autres que les contrats de rente viagère, les tables mentionnées au a
  sont utilisées en corrigeant l'âge de l'assuré conformément aux **décalages d'âge** ci-annexés."
  For annuity contracts, a family-(b) tariff may not be lower than the family-(a) one. And, directly
  relevant here: "**Pour les contrats collectifs en cas de décès résiliables annuellement, le tarif
  peut être établi d'après les tables mentionnées au a avec une méthode forfaitaire si celle-ci est
  justifiable.**"

### R5 — Code des assurances, art. A. 132-1 (maximum technical interest rate)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514601
- Retrieved: YES. Version en vigueur : 7 septembre 2017.
- Content: tariffs must be built on a rate at most equal to **75 % of the TME** (*taux moyen des
  emprunts de l'État français*), and beyond eight years may not exceed the lower of **3,5 %** and
  **60 % of the TME**. "Pour les contrats à primes périodiques ou à capital variable, quelle que soit
  leur durée, ce taux ne peut excéder le plus bas des deux taux suivants : 3,5 % ou 60 % du taux
  moyen" — the clause that binds an annually-renewable temporaire décès regardless of term. Foreign
  currency contracts use 75 % of the relevant sovereign long-term rate. The "barème de taux d'origine
  0 et de pas 0,25 point" rule reported by secondary summaries was **not visible in the retrieved
  text** and is `[unverified]`.

### R6 — Arrêté du 20 décembre 2005 relatif aux tables de mortalité (NOR ECOT0591210A)
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000636581
- Retrieved: YES.
- Content: the instrument that homologates **TH00-02** (male insureds) and **TF00-02** (female
  insureds), alongside TD 88-90 and TV 88-90 from the 1993 arrêté, and rewrites art. A. 335-1.
  "Les dispositions du présent arrêté entrent en vigueur le **1er janvier 2006**, à l'exception du
  dernier alinéa du paragraphe V et du paragraphe VI de l'article 2, qui entrent en vigueur le
  1er juillet 2006." The *décalage d'âge* rule appears in the same wording later carried into
  A. 132-18: "Pour les contrats en cas de vie autres que les contrats de rente viagère, les tables
  mentionnées au a sont utilisées en corrigeant l'âge de l'assuré conformément aux décalages d'âge
  ci-annexés." TH00-02/TF00-02 apply to contracts **other than** annuity contracts.

### R7 — Arrêté du 1er août 2006 portant homologation des tables de mortalité pour les rentes viagères
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000820127
- Retrieved: YES.
- Content: homologates the **generational** tables **TGF05** (female) and **TGH05** (male) with
  effect from **1 January 2007**, per art. 2: "Les tables prévues au quatrième alinéa de l'article
  A. 335-1 … sont à compter du 1er janvier 2007 : – la table TGF05 ci-annexée concernant les
  assurés de sexe féminin ; – la table TGH05 ci-annexée concernant les assurés de sexe masculin."
  Modifies A. 335-1, A. 331-1-1, A. 331-1-2, A. 441-4-1, A. 132-1, A. 132-4, A. 160-2, A. 160-4
  and others; imposes a transitional floor to 1 August 2008 against the previous 1993 generation
  table. **No maximum technical interest rate appears in this arrêté.** Recorded here because a
  temporaire décès touches TGH05/TGF05 only where a death capital is converted into an annuity
  (S3, S1).

### R8 — Code des assurances, art. A. 335-1 and its annexe (abrogated)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019265297
- Retrieved: YES.
- Content: the historic tariff article. In force **26 August 2006 → 1 January 2016**, **abrogated by
  the arrêté du 28 décembre 2015 with effect from 1 January 2016** (the Solvency II transposition
  package). It named TF 00-02 for female insureds, TH 00-02 for male insureds and TD 88-90 for
  contracts *en cas de décès*, and annexed the tables together with *décalages d'âge* by sex and
  age band. The operative successor is A. 132-18 [R4]. Any citation of "A. 335-1" in a current
  French product document is a legacy reference.

### R9 — Institut des actuaires, "Notice d'utilisation — Tables de mortalité TH 00-02 et TF 00-02"
- Publisher: Institut des actuaires
- URL: https://www.institutdesactuaires.com/docs/2007017232113_NOTICETHTF0002.pdf
- Retrieved: YES (PDF downloaded, 17 pp., full text extracted).
- Content: the profession's own note on how to apply the regulatory tables. It records that the
  arrêté (which this note dates **29 December 2005** — see the gaps section on the date discrepancy
  with R6) introduced TH 00-02 and TF 00-02 from 1 January 2006, that these tables **do not apply to
  *rentes viagères*** (covered by a separate arrêté effective 1 July 2006), and that the text
  specifies *décalages d'âge* for *contrats en cas de vie* **without specifying how to apply them**.
  The note poses the question directly — should the shift be applied to the l(x) or to the q(x)? —
  and concludes: "**La seule méthode à recommander est celle qui fait porter les décalages d'âge sur
  les qx**, déterminant ainsi des lx reconstitués aboutissant à un calcul de provisions « lissé » au
  passage d'un changement de valeur du décalage." Applying the shift to l(x) instead produces
  erratic q(x) growth and hence erratic life expectancies and annuity values. The note also contains
  extracts of the TH 00-02 and TF 00-02 l(x)/d(x)/q(x) columns and comparison charts; those numeric
  tables are **not reproduced here** (see the gaps section on table redistribution).

### R10 — Code des assurances, art. L. 111-7 (unisex pricing)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000027783391
- Retrieved: YES. Version en vigueur : 24 octobre 2024; current wording from LOI n° 2023-973 du
  23 octobre 2023 – art. 35.
- Content: "toute discrimination directe ou indirecte fondée sur la prise en compte du sexe … est
  interdite" in the calculation of premiums and benefits; pregnancy and maternity costs may not
  produce less favourable treatment for women. A ministerial derogation for sex-differentiated
  premiums where "des données actuarielles et statistiques pertinentes et précises établissent que
  le sexe est un facteur déterminant" survives **only for "contrats et adhésions à des contrats
  d'assurance de groupe conclus ou effectuées au plus tard le 20 décembre 2012"**, with specific
  rules for later modifications and renewals. This is the French implementation of CJEU C-236/09
  (*Test-Achats*) `[unverified as to the case number — the judgment itself was not fetched]`; the
  operative fact for pricing is the **21 December 2012** cut-off implied by the article's own
  "au plus tard le 20 décembre 2012".

### R11 — Code des assurances, art. R. 343-3 (life technical provisions)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039739686
- Retrieved: YES. Version en vigueur : 1er janvier 2020.
- Content: enumerates eleven categories of technical provision for life, *nuptialité-natalité* and
  capitalisation operations. 1° **Provision mathématique**: "différence entre les valeurs actuelles
  des engagements respectivement pris par l'assureur et par les assurés"; for contracts involving a
  survival or mortality table, the provision **must include an estimate of future management costs**
  borne by the insurer over the cover period beyond the premium-paying period, equal to the
  *chargements de gestion* built into the tariff. The other categories include the provision pour
  participation aux bénéfices, réserve de capitalisation, provision de gestion, provision pour aléas
  financiers, provision pour risque d'exigibilité, provision pour frais d'acquisition reportés,
  **provision d'égalisation (assurance de groupe contre le risque décès)**, provision de
  diversification, provision collective de diversification différée, and provision de garantie de
  terme. "Un engagement ne peut être provisionné qu'au titre d'une seule des catégories." No
  *provision pour risques croissants* appears in the life article — see R12.

### R12 — Code des assurances, art. R. 343-7 (provision pour risques croissants)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047658116
- Retrieved: YES. Version en vigueur : 10 juin 2024.
- Content: "**Provision pour risques croissants** : provision pouvant être exigée pour les
  opérations d'assurance contre les risques de maladie et d'invalidité et égale à la différence des
  valeurs actuelles des engagements respectivement pris par l'assureur et par les assurés." Note the
  scope: *maladie* and *invalidité*, i.e. the non-life side. The equivalent provision on a death
  cover is the *provision mathématique* of R. 343-3 [R11].

### R13 — Institut des actuaires, "Provisions pour risques croissants — Guidelines" (working group on assurance emprunteur, sub-group SGT4)
- Publisher: Institut des actuaires, 4 rue Chauveau-Lagarde, 75008 Paris
- Doc type: professional guidance document, 43 pp. (working group launched end-2019)
- URL: https://www.institutdesactuaires.com/global/gene/link.php?doc_id=17428
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: written about *assurance emprunteur*, but it is the best public French source on how a
  death cover whose premium rate is flat while mortality rises is reserved, and it reproduces the
  operative regulatory texts verbatim. Confirms and quotes: R. 343-3 (provision mathématique) and
  R. 343-7 (PRC); **art. A. 343-1-1** — "Les provisions mathématiques des contrats d'assurance sur la
  vie … à primes périodiques, doivent être calculées en prenant en compte les chargements destinés
  aux frais d'acquisition dans l'engagement du payeur de primes. La provision résultant du calcul
  précédent ne peut être négative, ni inférieure à la valeur de rachat du contrat, ni inférieure à
  la provision correspondant au capital réduit."; **ANC 2015-11 art. 142-3** (as amended by ANC
  2016-12) — mathematical provisions computed at rates at most equal to those used to set the
  tariff and, where there is a *viager* element, on the tables in force when the tariff was applied,
  with the option to move all in-force contracts to the tables appropriate at each subsequent
  annual inventory and to spread the effect of a change of basis over at most eight years; and the
  full text of **A. 132-18** [R4]. It states explicitly that on the life side "la provision
  mathématique est souvent définie comme une PRC décès", and that "**la même provision de prime
  s'appelle PM en vie et PRC en non-vie**". Formula notation is given (x, i, d, C_k, τ, q_x, l_x,
  chute law), with the insurer's engagement as the discounted expectation of future benefit flows
  and the provision as the difference of the two present values. Worked illustrations use: loan
  100 000 €, age 37, table TF 00-02, interest 1 %, technical rate 0,5 % (death) / 0 % (with
  incapacity); a **mixed unisex death table of 60 % TH 00-02 / 40 % TF 00-02**; and a medical-
  selection abatement on claims of **70 % in year 1, 50 % in year 2, 20 % in year 3**. Its
  qualitative conclusion transfers directly to a level-rate temporaire décès: where the premium
  rate is flat and the death rate rises, "**un montant de PRC est toujours constitué pendant la
  durée**", whereas a tariff expressed on an initial (rather than outstanding) capital tends to
  produce a negative provision early on. Its recommendations include building reference tables under
  the Institut's aegis, because the existing regulatory table "ne vaut que pour le décès (TH 00-02)"
  and no market product actually prices on it.

### R14 — Code général des impôts, art. 990 I (and 990 I bis)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069577/LEGISCTA000006162644/
- Retrieved: YES. Version date shown: 11 mars 2023.
- Content: the levy on sums paid by insurers on the insured's death. Taxable base = the
  beneficiary's share less a fixed **abattement of 152 500 €**; rates "**20 % pour la fraction de la
  part taxable de chaque bénéficiaire inférieure ou égale à 700 000 €**" and "**31,25 % pour la
  fraction de la part taxable de chaque bénéficiaire excédant cette limite**". Exemptions where the
  beneficiary qualifies under arts. 795, 796-0 bis (spouse / PACS partner) or 796-0 ter (siblings
  under conditions). Art. 990 I bis, effective 1 January 2016, applies the same rates with a
  15 000 € abattement to sums deposited at the Caisse des dépôts et consignations.

### R15 — BOFiP, BOI-TCAS-AUT-60 (30 March 2023) — doctrine on the art. 990 I levy
- Publisher: Direction générale des finances publiques (bofip.impots.gouv.fr)
- URL: https://bofip.impots.gouv.fr/bofip/1335-PGP.html/identifiant%3DBOI-TCAS-AUT-60-20230330
- Retrieved: YES. Document identifier BOI-TCAS-AUT-60-20230330.
- Content: the scope statement this product needs — the levy reaches sums due by insurers by reason
  of the insured's death to designated beneficiaries, and **that expressly includes *assurance décès
  temporaire* and *assurance décès pure***, provided the beneficiary is designated *à titre gratuit*.
  Contracts designated *à titre onéreux* — the paradigm being loan-protection cover assigned to a
  lender — are **excluded** from the levy. Confirms the 152 500 € abattement, the 20 % / 31,25 %
  rates with the 700 000 € boundary, the additional 20 % proportional abattement for *vie-génération*
  contracts, and the exemptions (surviving spouse, PACS partner, siblings, qualifying charities).
  Premiums paid after the insured's 70th birthday on contracts subscribed after 20 November 1991
  fall instead under *droits de mutation à titre gratuit* per art. 757 B, exempt below **30 500 €**.

### R16 — CNP Assurances, "Notice explicative : attestation sur l'honneur article 990 I du code général des impôts"
- Publisher: CNP Assurances (SA, RCS Paris 341 737 062)
- Doc type: insurer tax-procedure notice, 2 pp.
- URL: https://www.cnp.fr/media/fichiers/particuliers/faq/remplir-l-attestation-sur-l-honneur-etablie-en-application-de-l-article-990-i-du-code-general-des-impots
- Retrieved: YES (PDF downloaded, full text extracted). No document date printed.
- Content: the operational statement of the levy, in capital terms rather than taxable-share terms,
  which is how it appears on a claim file: the levy applies to payments and gains after 13 October
  1998 and **before the insured's 70th birthday**, after an abattement of **152 500 € per
  beneficiary across all life contracts of the same insured, with one or several companies**; and
  the rate schedule is stated as "**20 % sur la part de capital comprise entre 152 500 € et
  852 500 €**" and "**31,25 % sur la part de capital au-delà de 852 500 €**" — i.e. the 700 000 €
  boundary of R14 measured from the top of the abattement. For deaths before 31 July 2011 the rate
  stays capped at 20 %. Spouse and PACS partner are wholly exempt and file no attestation; a sibling
  is wholly exempt if three cumulative conditions are met. The insurer is responsible for applying
  the levy and remitting it to the Trésor public, which is why the beneficiary must declare whether
  the 152 500 € abattement has already been used. The *vie génération* 20 % proportional abattement
  is noted for contracts subscribed from 1 January 2014 (or transformed between 1 January 2014 and
  1 January 2016) and unwound by death from 1 July 2014.

### R17 — Convention AERAS, version actualisée 2023
- Publisher: signatories — the State (Ministry of the Economy; Ministry of Health), banking and
  finance federations, insurance and mutual federations, and patient/consumer associations
- Doc type: inter-professional convention, 44 pp.
- URL: https://www.aeras-infos.fr/files/live/sites/aeras/files/contributed/docs/Convention%20AERAS%202023.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content, and the **scope point that matters most for this product**: AERAS is a *borrowing*
  convention. Its preamble, Titre III and Titre IV all frame it around "l'assurance emprunteur" and
  it applies to "les prêts à la consommation affectés ou dédiés, les prêts professionnels pour
  l'acquisition de locaux et/ou de matériels, les prêts immobiliers"; Titre IV states "Ce titre
  s'applique aux prêts professionnels et immobiliers visés au titre III." **Nothing in the retrieved
  text extends it to a standalone temporaire décès unconnected to a loan.** Key figures: a
  three-level examination process (standard insurer; a *deuxième niveau* device for individualised
  re-examination after a health-based refusal; a *pool des risques très aggravés* at *troisième
  niveau*), the third level conditioned on the insurance contract maturing **before the borrower's
  71st birthday** and on the insured share of outstanding loans not exceeding **420 000 €** (for a
  principal residence, ignoring bridging loans; otherwise on cumulative outstanding loans). Health
  questionnaires are dropped for *prêts à la consommation affectés ou dédiés* where the insured
  amount does not exceed **17 000 €**, the repayment term is **≤ 4 years**, and the applicant is
  **50 or under**, subject to a sworn non-cumulation declaration. *Écrêtement des surprimes*: applies
  at the 2nd and 3rd examination levels, to property and professional loans of at most 420 000 €;
  eligibility by income against the *plafond de la sécurité sociale* (PASS) and the household's tax
  *parts* — **≤ 1 × PASS for 1 part, ≤ 1,25 × PASS for 1,5 to 2,5 parts, ≤ 1,5 × PASS for 3 parts and
  above**; where eligible, "**la prime d'assurance ne peut représenter plus de 1,4 point dans le taux
  effectif global de l'emprunt**", and the *surprime* on a zero-rate loan (PTZ) for borrowers under
  35 is met in full by the professionals. The BCAC administers the *écrêtement*. *Droit à l'oubli*:
  no medical information about a cancer or hepatitis C may be sought "dès lors que le protocole
  thérapeutique … est achevé depuis plus de **5 ans** et en l'absence de rechute", subject to the
  same loan-type and age-71 conditions, with precise definitions of the end of the therapeutic
  protocol and of relapse. A *grille de référence AERAS* lists pathologies for which cover is
  granted without *surprime* or exclusion, or on conditions close to standard, with maximum surprime
  rates and delays set per pathology and stated **per garantie (Décès, PTIA, GIS)**; it is evaluated
  by the insurer's medical service and updated by a dedicated working group under the *Commission
  de suivi et de propositions*. The preamble also records the interaction with the **loi du
  28 février 2022** on borrower insurance (the *loi Lemoine*), whose conditions remove health
  questionnaires altogether for qualifying property loans.

### R18 — aeras-infos.fr, the convention's official site
- Publisher: signatories of the Convention AERAS
- URL: https://www.aeras-infos.fr/
- Retrieved: YES (partially — the site's summary pages render; per-figure detail sits in the PDF at
  R17).
- Content: confirms the 2023 version as current, **with an amendment (*avenant*) signed 5 July
  2024**; describes the three examination levels and the *droit à l'oubli* five-year rule and the
  *grille de référence*. Loan ceilings and age limits are not restated on the pages retrieved.

### R19 — Code général des impôts, art. 757 B (premiums paid after age 70)
- Publisher: Légifrance
- URL: not resolved — the article's Légifrance identifier could not be located without a web search
  (the search budget for this session was exhausted; a URL was **not** guessed).
- Retrieved: **NO.** Known reference only.
- Content: the substance is nevertheless confirmed against two retrieved documents and is cited from
  them, not from the article: premiums paid after the insured's 70th birthday on contracts
  subscribed after 20 November 1991 are subject to *droits de mutation à titre gratuit* according to
  the relationship between subscriber and beneficiary, with a single global abattement of **30 500 €**
  shared across taxable beneficiaries and across all life contracts of the same insured [R15][S1].
  S1 adds that the 30 500 € abattement also takes in the whole of any death capital from a *Plan
  d'Épargne Retraite* where death occurs after the 70th birthday. Anything article-level about
  757 B is `[unverified]`.

### R20 — ACPR (Autorité de contrôle prudentiel et de résolution)
- Publisher: ACPR / Banque de France
- URL: https://acpr.banque-france.fr/ (and https://acpr.banque-france.fr/en)
- Retrieved: **NO — HTTP 403 Forbidden on both, on repeated attempts** (the host rejects plain
  fetchers). Known reference only. The ACPR is named as the supervisory authority in S1, S2, S6 and
  S9, at "4 place de Budapest, CS 92459, 75436 Paris Cedex 09"; nothing further is cited from the
  ACPR in these notes, and no ACPR *analyse et synthèse* on prévoyance was retrieved.

### R21 — France Assureurs, "Nos chiffres clés — L'assurance santé et prévoyance"
- Publisher: France Assureurs
- URL: https://www.franceassureurs.fr/nos-chiffres-cles/lassurance-sante-et-prevoyance/
- Retrieved: YES (headline figure only).
- Content: "**40,3 Md€ Cotisations en assurance prévoyance en 2025**". The page does not break the
  figure down between *garanties décès* (temporaire décès, obsèques, emprunteur), incapacité-
  invalidité and dépendance; that breakdown sits in the linked report "L'assurance prévoyance en
  2025", which was not retrieved.

### R22 — France Assureurs, home page (market context)
- Publisher: France Assureurs
- URL: https://www.franceassureurs.fr/
- Retrieved: YES.
- Content: headline of the day — "Avec **19,3 milliards d'euros de cotisations en juin 2026**, les
  épargnants maintiennent leur confiance dans l'assurance vie". Also lists the *chiffres clés*
  sections (assurance vie; santé et prévoyance; données globales) and the reference publication
  "L'assurance française — Données clés 2025". Recorded to place the protection market beside the
  savings market; the savings figure is not used for this product.

### R23 — economie.gouv.fr, "S'assurer et emprunter avec un risque aggravé de santé : la convention AERAS peut vous aider" / service-public.gouv.fr fiche F2377
- Publisher: Ministère de l'Économie; DILA
- URLs:
  - https://www.economie.gouv.fr/particuliers/gerer-mon-argent/emprunter-et-sassurer/sassurer-et-emprunter-avec-un-risque-aggrave-de-sante-la-convention-aeras-peut-vous-aider
  - https://www.service-public.gouv.fr/particuliers/vosdroits/F2377
- Retrieved: **NO** — the economie.gouv.fr page returns HTTP 403 on repeated attempts; the
  service-public fiche F2377 redirects from `service-public.fr` to `service-public.gouv.fr` and then
  returns HTTP 404 (the fiche appears to have been retired or renumbered, and the correct id could
  not be found without a web search). Both kept as known references; nothing is cited from either.
  The official-portal view of the product is therefore missing from this file — see the gaps
  section.

---

## Extracted specifications

### 1. Product structure and legal form
- A French *assurance temporaire décès* is a pure protection contract: the insurer pays a *capital
  décès* to the designated beneficiaries if the insured dies while the cover is in force, and pays
  nothing at all if the insured survives to the end of cover [S9][S11][S13][S15][S16].
- It is **life assurance business** — *branche 20 (vie-décès)* of art. R. 321-1 — not accident
  business, even though it pays only on death [S3][S1][S7]. AXA's Avizen adhesion spans branches 20,
  1 (Accident) and 2 (Maladie) because it bundles incapacity and invalidity covers alongside the
  death capital [S7].
- Two legal wrappers are used, and both are common:
  - **Individual contract** (*contrat individuel d'assurance décès*) — MAIF Rassurcap Solutions,
    "un contrat individuel d'assurance décès, d'une durée d'un an, renouvelable par tacite
    reconduction" [S3].
  - **Group contract with voluntary membership** (*contrat d'assurance de groupe à adhésion
    facultative*, arts. L. 141-1 ff.) — MAAF Vie contract n° 02120 subscribed by the association ANS
    Vie-Covéa [S1]; Macif/Macif-Mutualité contracts n° 219.002-A and -B with Prévoyance Aésio Macif
    [S2]; AXA/ANPERE Avizen [S7]; Mutex [S6]. In this form the *notice d'information* is the
    document delivered to the member and is the contractual reference; the subscriber association
    and the insurer may amend the group contract by *avenant*, with prior written notice to members
    (MAAF: at least three months before the change takes effect) [S1][S2].
- A parallel *mutualité* form exists, governed by Livre II of the **Code de la mutualité** rather
  than the Code des assurances, with the same economics but different procedural timers: MUTUALP /
  LA FRONTALIÈRE, "un contrat d'assurance collectif à adhésion facultative de type « assurance
  temporaire décès »" [S9].
- A *bancassurance* form ties the cover to a bank relationship: Antarius Protection Premium requires
  an account at Crédit du Nord or an affiliate and French/Monaco tax residence, and **all guarantees
  cease if either condition lapses** [S8].
- Participation aux bénéfices: the product is normally non-participating in substance. MUTUALP
  states flatly "Le contrat ne prévoit pas de participation aux bénéfices" [S9]. MAAF and Macif do
  run a *participation aux bénéfices* but compute it **globally across the insurer's life book** and
  distribute it as higher benefits, higher benefits in payment and/or lower cotisations called —
  not as a policy-level account [S1][S2]. There is no policyholder account value in any retrieved
  contract.

### 2. Contract forms: temporaire vs vie entière, capital constant vs décroissant
- **Temporaire décès vs assurance décès vie entière.** The temporaire pays only if death falls
  inside the cover period; the *vie entière* pays whenever death occurs, at a higher premium, and —
  decisively for modelling — a *vie entière* contract may carry a *valeur de rachat* and a *tableau
  de rachat*, while a temporaire may not [S5][S11]. This is not a commercial choice: art. L. 132-23
  forbids *réduction* and *rachat* on *assurances temporaires en cas de décès* [R3].
- **Capital constant vs capital décroissant.** *Capital constant* pays a fixed sum throughout;
  *capital décroissant* pays a sum that steps down along an amortisation schedule and is described
  as belonging to loan cover [S15]. **Every standalone contract retrieved for this file is capital
  constant** [S1][S2][S3][S6][S7][S8][S9] — none of them offers a decreasing sum insured. The
  decreasing form belongs to *assurance emprunteur*, where the industry distinguishes a tariff on
  *capital initial* (CI) from one on *capital restant dû* (CRD) [R13]. A frlib `temporaire_deces`
  model should therefore treat *capital décroissant* as an out-of-scope variant of the ADE product
  and model the constant capital, with the decreasing schedule available as a scaling on the sum
  insured if it is ever wanted.
- The nearest thing to a decreasing benefit found in a standalone contract is a **step-up on the
  beneficiary side**, not on the sum insured: AXA's *rente éducation* pays 100 % of the subscribed
  amount for a child aged 0–11, 125 % for 12–17 and 150 % for 18–26 [S7]; and its *rente décès* is
  **halved from the beneficiary's 65th birthday** [S7].

### 3. Duration, renewal and age limits
- The dominant French form is an **annual contract renewed by *tacite reconduction***
  [S1][S2][S3][S6][S8][S9][S13][S15]. Renewal dates differ: MAAF renews each 1 January with the
  adhesion first running to 31 December [S1]; Macif renews each 1 April, the *échéance annuelle*
  [S2]; MAIF's *date d'échéance* is the first day of the month following the anniversary of the
  effective date [S3]; MUTUALP runs on the civil year with an *échéance principale* at 1 January
  [S9].
- Fixed multi-year forms (5-year renewal periods; 10, 15 or 20-year terms) are reported by a bank
  guide and a broker guide [S13][S16] but were **not confirmed against any insurer contract
  document** — treat as `[unverified]`.
- Age limits retrieved, at entry and at cessation of each cover:

| Insurer | Entry age | Death cover ceases | PTIA/IPA/IPT cover ceases |
|---|---|---|---|
| MAAF [S1] | 18–75 | 31 Dec of the year the insured reaches 85 | same (PTIA ends the contract when paid) |
| Macif [S2] | 18–67 incl. (Essentielle to 50) | *échéance principale* (1 Apr) of the year after the 80th birthday | 1 Apr of the year after the **75th** birthday |
| MAIF [S3][S4] | up to 65 (to the day before 66) | *échéance* following the **75th** birthday | *échéance* following the **65th** |
| Mutex [S6] | 18–80 | adhesion anniversary in the year of the **85th** | anniversary in the year of the **80th** |
| AXA Avizen [S7] | not stated in the retrieved text | end of the insurance year of the **85th** | end of the insurance year of the **67th** (and before retirement) |
| Antarius [S8] | 18 to under 66 | adhesion anniversary after the **70th** | anniversary after the **65th** |
| MUTUALP [S9] | not stated in the retrieved text | 31 Dec of the year of the **65th** | n/a (no PTIA cover) |
| MetLife [S10] | 18–84 | **90** | not stated |
| MACSF [S12] | to the day before the 57th (50th for *infirmières*) | not stated | not stated |

- The pattern to carry into the model: **cover ends at a policy-year boundary defined by attained
  age, and the PTIA/IPA acceleration always ends earlier than the death cover** (Macif 75 vs 80,
  MAIF 65 vs 75, Mutex 80 vs 85, AXA 67 vs 85, Antarius 65 vs 70). The only exception found is
  MAAF, where PTIA and death share the same age-85 limit [S1].
- Age is computed as the **difference of millésimes** — calendar year of the contract year minus
  calendar year of birth, irrespective of birth month — by MAAF [S1], Macif [S2] ("pour une personne
  née en 1967, l'âge retenu en 2019 est : 2019 − 1967 = 52 ans"), Mutex [S6] and AXA [S7]. This is
  an integer age that increments on 1 January, not on the policyholder's birthday, and it is the
  single most important convention to get right in a French annual-step model.
- Additional entry conditions found: residence in metropolitan France or the DROM
  [S1][S2][S3][S8]; not under *tutelle* nor hospitalised in a psychiatric establishment, and one
  individual death contract per person at the insurer [S3]; excluded occupations at entry
  (*cascadeurs*, *jockeys* at MAAF [S1]; a longer list of hazardous occupations at Mutex [S6]).

### 4. Guarantee — décès toutes causes
- The core guarantee is death **from any cause, accident or illness**, subject only to the stated
  exclusions [S1][S2][S3][S6][S7][S9].
- Territorial scope is normally worldwide, with residence or travel-duration conditions rather than
  a geographic carve-out: MAAF worldwide, with an obligation to elect a French domicile for stays
  abroad over 3 months [S1]; Macif worldwide for continuous trips not exceeding 12 months, with
  cover ceasing of right on a continuous stay abroad exceeding 12 months [S2]; MUTUALP worldwide for
  professional and personal stays not exceeding **60 consecutive days per civil year** [S9]; MAIF
  requires notification within 15 days of any trip or stay abroad longer than 6 months [S3];
  Antarius worldwide [S8].
- Settlement timing: MAAF pays within **15 days** of receiving the listed documents [S1]; MAIF
  within **one month** [S3]; MUTUALP within a period that may not exceed one month, with interest at
  twice the legal rate for late payment [S9]. An *avance* on the capital is common — Macif 4 000 €
  [S2], MAIF 4 000 € to the spouse/PACS partner within 48 h [S3], Mutex an *acompte* of 5 000 €
  [S6], Antarius 10 % of the capital capped at 10 000 € within two days [S8]. These are advances on
  a benefit already due, not a separate cover, and can be ignored in an annual cash-flow model.

### 5. Guarantee — PTIA, the French acceleration
- **PTIA (*perte totale et irréversible d'autonomie*) is paid as an anticipated payment of the death
  capital, to the insured, and it extinguishes the death cover.** This is the standard French
  acceleration and it is present in every standalone contract retrieved except the MUTUALP mutual
  one [S1][S2][S3][S6][S7][S8][S10][S12].
- Naming varies without changing the substance: **PTIA** (MAAF, Macif, Mutex, Antarius, MetLife),
  **IPA** *invalidité permanente absolue* (MAIF), **IPT** *invalidité permanente totale* (AXA),
  **IFTD** *invalidité fonctionnelle totale et définitive* (MACSF) [S1][S2][S3][S6][S7][S8][S10][S12].
- The definition is stable across insurers and is a **two-limb test**: (a) the insured is unfit to
  engage in any occupation or activity producing gain or profit, and (b) the insured must have
  recourse to the permanent assistance of a third person to perform the ordinary acts of daily life
  — MAAF's list is "se laver, se vêtir, se nourrir, se déplacer" [S1]; Mutex's is "se lever, se
  laver, s'habiller, s'alimenter, se déplacer" [S6]; MAIF requires the state to be an "incapacité
  absolue et définitive" with a **definitive** need for third-party assistance [S3]. Recognition
  requires *consolidation* — the point at which the state of health is no longer susceptible of
  notable change and the sequelae become permanent [S1][S7].
- Interlocks the model must respect:
  - Death and PTIA benefits **cannot be cumulated** [S1].
  - Payment of the PTIA capital **ends the contract / the death cover** [S2][S3][S6].
  - The capital is due only if the insured is **alive on the day of payment**; if the insured dies
    first, the death cover operates instead [S2].
  - AXA suspends premium payment for the duration of the invalidity and, on recognition of IPT, ends
    all guarantees except the *rente décès*, *rente éducation décès* and *capital double garantie*,
    which remain payable on the later death [S7]. MAIF likewise stops premium collection at death
    or IPA [S3]; AXA stops it at death or IPT [S7].
- Evidence: for social-security insureds, MAAF accepts the *notification de la caisse attestant
  l'invalidité de IIIème catégorie* as proof [S1]. MAIF requires the PTIA state to be **medically
  established in France**, with the guarantee's start date being that first French medical
  observation, and provides a three-doctor arbitration procedure where cover is refused [S3].

### 6. Optional guarantees — doublement, triplement, double effet, rentes
- **Doublement accidentel.** An option paying a second capital equal to the first where death (and
  usually PTIA) results from an accident. Present at MAAF [S1], Macif [S2], Mutex [S6], MUTUALP (at
  **50 %**, not 100 %) [S9], AXA (as a separate *capital décès par accident*) [S7], MACSF [S12].
  Standard conditions: the death or PTIA must occur within **12 months** of the accident
  [S2][S6][S7][S9]; AXA allows **24 months** for IPT by accident [S7]. The option is usually
  capital-capped: MAAF limits the base capital to 1 000 000 € where doubling is taken (against
  2 000 000 € otherwise) [S1]; Mutex limits the capital to 100 000 € for adhesions from age 70 with
  the option [S6].
- **Triplement accidentel.** Found only at MACSF: the capital is **doubled** for an accident and
  **tripled** where the accident is a road-traffic accident, or results from terrorism, an *attentat*
  or an *agression* [S12].
- **Double effet.** A distinctively French rider: if the spouse, PACS partner or *concubin* dies
  simultaneously with, or after, the insured, a further capital is paid to the children who were
  fiscally dependent on that person. AXA pays a capital equal to the one already paid [S7]; Antarius
  pays a capital equal to the guaranteed capital, **capped at 500 000 €**, with the spouse's death
  before age 70 or PTIA before 65 [S8]. AXA also doubles a *rente éducation* already in payment on
  the same trigger [S7].
- **Capital décès double garantie** (AXA): where the insured, already in IPT, dies at least one year
  after consolidation, a further capital equal to the IPT capital already paid is due, provided
  death occurs before the end of the insurance year of the 85th birthday [S7]. This is a genuine
  second decrement on an already-accelerated life and is easy to model wrongly.
- **Rente éducation.** MAAF: 75 € – 3 810 € per quarter per child, payable to 31 December preceding
  the child's 26th birthday, children under 25 at adhesion, the amount identical for all
  beneficiaries and adjustable with the number and ages of children [S1]. AXA: paid to the child's
  26th birthday with 100 % / 125 % / 150 % steps and lifetime continuation for a disabled
  beneficiary where the allowance was granted before the 21st birthday and the cover was taken
  before the child's 16th [S7]. MetLife: up to 2 000 €/month per child [S10]. MAIF converts part of
  the death capital into a *rente temporaire* to age 26 where the beneficiary is a child under 26
  [S3].
- **Rente de conjoint / rente décès.** AXA pays a life annuity to the designated beneficiary,
  **halved from the beneficiary's 65th birthday** [S7]; MetLife offers up to 5 000 €/month [S10];
  MAIF's *versement d'une rente* mode pays a life annuity to the spouse/PACS partner and a temporary
  annuity to children under 26 [S3].
- **Assistance and services.** Every retrieved contract bundles some assistance package (IMA at
  Macif [S2]; a *guide d'accompagnement* and capped call-based services at MAIF [S3]; assistance in
  Mutex and MUTUALP [S6][S9]). These carry no material cash flow and are out of scope.
- **Maladie grave.** MAIF's current page offers a 5 000 € flat capital for a serious illness [S4] —
  not present in the 2019/2021 note d'information [S3], so a recent addition.

### 7. Capital amounts, increases and indexation
- Retrieved capital ranges:

| Insurer | Minimum | Maximum |
|---|---|---|
| MAAF [S1] | 10 000 € | 2 000 000 € per insured (1 000 000 € with accidental doubling) |
| Macif [S2] | 25 000 € (Essentielle 15 000 €) | 762 000 € (Essentielle 24 999 €) |
| MAIF [S3][S4] | 20 000 € | no stated ceiling; 250 000 € under simplified underwriting to age 40 |
| Mutex [S6] | not stated | 200 000 € (100 000 € from age 70 with the accident option) |
| Antarius [S8] | 100 000 € | 1 000 000 € |
| MUTUALP [S9] | base 6 097,96 € | 45 000 € including the supplementary capital |
| MetLife [S10] | not stated | 50 M€ death, 20 M€ PTIA |

- **Increases** always re-open selection, except for defined life-event or automatic increments:
  - MAIF: a **5 000 € forfait** every 5 years without medical formalities, plus the same 5 000 €
    within 12 months of birth, adoption, marriage, PACS, divorce, PACS break-up or the spouse's
    death — **at most 4 formality-free increases over the life of the contract**; other increases
    need a new *questionnaire de santé simplifié* or *questionnaire médical* and MAIF VIE's express
    agreement, and are only possible to the *échéance* following age 65 [S3].
  - AXA: up to **20 %** of the capital without medical selection within 3 months of marriage, PACS,
    birth or adoption [S7].
  - MAAF, Macif, Mutex, MUTUALP: any increase requires renewed health declaration and/or medical
    formalities [S1][S2][S6][S9]; MUTUALP additionally restricts increases to members under 50 [S9].
- **The suicide clock restarts on the increment, not on the whole contract.** MAAF applies the
  one-year suicide exclusion afresh "à la date d'effet du dernier avenant d'augmentation pour
  l'excédent de capital souscrit" [S1]; Macif applies it "en cas d'augmentation des garanties (pour
  le différentiel de garantie)" [S2]; MAIF, Mutex and AXA state the same [S3][S6][S7]. This is
  art. L. 132-7 alinéa 2 operating directly [R1].
- **Indexation.** An optional *revalorisation* indexes both the capital and the cotisation:
  - MAAF and AXA index on the **plafond annuel de la Sécurité sociale (PASS)** — MAAF by the
    difference between the two preceding years' values [S1], AXA by the PASS movement, ceasing at
    the anniversary in the year the insured reaches 70 [S7].
  - Macif and Mutex index at **a rate set by the insurer** [S2][S6].
  - Refusal of indexation is possible and, at Macif, Mutex and AXA, **definitive** — once refused it
    cannot be resumed [S2][S6][S7].
- **Decreases** are allowed, subject to the minimum capital, and reduce the cotisation with a fresh
  *avis d'échéance* [S2][S3]. MUTUALP penalises a decrease by barring future increases unless the
  change is tied to a change of marital status or employment conditions [S9].

### 8. Waiting periods (*délais d'attente*) and provisional cover
- Two distinct mechanisms exist and must not be confused.
- **Délai d'attente** — cover does not begin for a stated period:
  - Mutex: where the adhesion carries **no medical formality** (capital ≤ 40 000 € and age ≤ 50), the
    illness-caused death and PTIA cover takes effect only after a **12-month délai d'attente**; death
    during that period returns **the sum of the cotisations collected** to the heirs. Where medical
    formalities are done, **no waiting period applies** [S6].
  - MUTUALP: the right to the capital is acquired after **3 months**, waived for accidental death or
    where the member already held equivalent or higher cover through the subscriber for more than
    three months [S9].
  - No waiting period appears in MAAF, Macif, MAIF, AXA or Antarius [S1][S2][S3][S7][S8].
- **Garantie provisoire / garantie immédiate accident** — cover *during* medical underwriting,
  limited to accidental causes:
  - Macif: immediate accidental-death cover for at most **60 days** from receipt of the signed
    application, first application only, limited to the amount applied for with a maximum of
    **76 000 €** [S2].
  - MAIF: provisional cover for death or IPA following an accident, from receipt of the application
    until the earlier of acceptance, refusal, renunciation or **30 days**, capital limited to
    **15 000 €** regardless of the number of beneficiaries, and paid **after deduction of the
    temporary death premium** [S3].
- Effective-date mechanics also matter: several insurers make the effective date conditional on
  medical acceptance, so cover for illness starts at the acceptance date, not the application date
  [S2][S6][S3].

### 9. Exclusions
- **Suicide** is the only exclusion fixed by statute. Art. L. 132-7 makes death cover "de nul effet"
  where the insured takes their own life in the **first year of the contract**, and requires cover
  from the **second year**, with the clock restarting for the increment on any increase of cover
  [R1]. Every retrieved contract implements exactly this and no more — MAAF [S1], Macif ("les
  suicides dans les 12 mois qui suivent la prise d'effet du contrat", plus attempted suicide and
  self-mutilation consequences) [S2], MAIF [S3], Mutex [S6], AXA (suicide "conscient ou inconscient")
  [S7], Antarius [S8], MUTUALP [S9], MetLife [S10].
- The **immediate** suicide cover of L. 132-7 alinéa 4, capped by art. R. 132-5 at not less than
  **120 000 €**, applies only to art. L. 141-1 group contracts securing a loan taken to buy the
  insured's **principal residence** [R1][R2]. **It does not reach a standalone temporaire décès**, and
  a model of this product should not carry it.
- As of **20 August 2026**, art. L. 132-7 also provides that death cover applies to death resulting
  from the *aide à mourir* under art. L. 1111-12-1 of the Code de la santé publique [R1]. None of the
  retrieved product documents reflects this yet.
- **Contractual exclusions**, recurring across insurers, with representative wording:
  - War (civil or foreign), generally with a legislative reservation where France is a belligerent
    [S1][S2][S3][S6][S9].
  - Nuclear — effects direct or indirect of explosion, heat release or irradiation from the
    transmutation of atomic nuclei [S1][S2][S3][S9].
  - Riots, popular movements, terrorism, sabotage, *rixes*, strikes, wagers, assaults — normally
    only where the insured **takes an active part**, with self-defence carved out [S1][S2][S9].
  - Intentional acts of the insured, and voluntary conscious harm to one's own physical integrity
    [S1][S3][S8].
  - Alcohol and narcotics: driving with blood alcohol at or above the Code de la route threshold,
    driving without a valid licence, and non-prescribed narcotics or psychotropics
    [S1][S2][S6][S8].
  - Air sports and extreme sports — the longest lists. MAAF: air sport competitions, raids, aerobatic
    and test flights, ULM, hang-gliders and paragliders, record attempts, non-homologated
    parachutes, bungee jumping, kite-surfing; plus motor competition, solo ocean racing, motorboat
    competition, scuba diving with cylinders, caving, professional sport, federated competition, and
    a defined list of *sports dangereux* (ice hockey, air sports, spearfishing with self-contained
    apparatus, water skiing, unguided mountaineering, bungee jumping, caving, combat sports) [S1].
    MAIF: ULM, paragliding, autogyro, hang-gliding, parachuting, gliding, bungee jumping,
    kitesurfing; diving below **20 metres**; solo sailing beyond **25 nautical miles**; snow and ice
    sports other than amateur practice on authorised pistes; mountain hiking, alpinism and climbing
    above **3 000 metres** — with an explicit carve-out for *initiation* under a qualified
    professional [S3]. Antarius: paragliding, bungee jumping, off-piste snow sports, professional
    sport, competitions and dares [S8].
  - Pre-existing conditions: MAIF excludes the consequences of an evolving or chronic illness or
    infirmity present at subscription **unless expressly declared and not excluded in the conditions
    particulières** [S3]; Antarius excludes "les suites et conséquences d'un état antérieur à la
    prise d'effet des garanties" [S8]; Mutex excludes any pathology observed between the signature
    of the medical questionnaire and the effective date [S6].
  - Occupational exclusions: MAAF excludes death or PTIA arising from the occupation itself for
    firefighters, military, police and gendarmerie [S1].
  - Murder of the insured by a beneficiary, for that beneficiary's share [S2].
- **Some exclusions are priceable rather than absolute**: Macif will cover air sports for a
  *surcotisation* if declared at adhesion and accepted by the medical service, with a mention in the
  *certificat individuel de garantie* [S2]. Individual exclusions can also be written into the
  *certificat* at underwriting [S2][S6].

### 10. Underwriting: questionnaire de santé, formalités médicales, surprimes, AERAS
- The health questionnaire is **retained** for this product. The *loi Lemoine* abolition of the
  health questionnaire applies to qualifying **borrower** cover only [R17]; nothing in the retrieved
  material removes it from a standalone temporaire décès.
- **Two-tier declaration.** Insurers use a short *déclaration de santé* / *déclaration de bonne
  santé* / *questionnaire de santé simplifié*, escalating to a full *questionnaire médical* on a
  trigger, and thence to examinations at the medical officer's request [S2][S3][S6]. Macif notes
  that if the applicant answers "no" to the single question in the *déclaration de santé*, their
  declared occupational and sporting activities are **not** taken into account in the pricing [S2].
- **The only retrieved numeric formalities grid** is Mutex's [S6]:

| | Capital ≤ 40 000 € | Capital > 40 000 € |
|---|---|---|
| **Age ≤ 50** | No medical formality — but a **12-month délai d'attente** for illness-caused death/PTIA | *Questionnaire médical*; no waiting period |
| **Age > 50** | *Déclaration de Bonne Santé*; escalates to *questionnaire médical* if any "OUI" is ticked | *Questionnaire médical*; no waiting period |

  MAIF's published equivalent is coarser: **simplified underwriting up to age 40 for a capital of up
  to 250 000 €** [S4][S5]. No other insurer publishes its thresholds.
- **Questionnaire validity**: MAAF fixes the *Questionnaire Médical Confidentiel* at **3 months**
  from signature; if not received within that window a fresh one is required [S1]. Applicants must
  notify any change of health between application and acceptance [S2][S3].
- **Underwriting outcomes** are the same four everywhere: accept at standard rate; accept with a
  *surprime* / *surcotisation* / *surtarification* and/or partial exclusions, subject to the
  applicant's acceptance; adjourn (*ajourner*) pending examinations or a later re-examination fixed
  by the medical service; decline [S1][S2][S3][S6]. Mutex documents the mechanics: the offer of
  reserves is notified by confidential letter naming the condition justifying the exclusion and/or
  the amount of the *surcotisation*, and must be returned within **15 days** signed "BON POUR
  ACCORD"; otherwise the applicant is treated as having renounced and the cotisation is refunded
  [S6]. **No insurer publishes a surprime scale.**
- **In-force re-rating on risk change.** A change of occupation or of sporting activity must be
  declared and can trigger an increase in cotisation or an exclusion; refusal of the new terms
  causes resiliation, and leaving a listed hazardous occupation triggers a **reduction** with a new
  *avis d'échéance* [S2]. AXA requires declaration within 30 days by registered letter and treats a
  return to smoking as a declarable change [S7]. Misstatement is governed by arts. L. 113-8
  (intentional — contract void, premiums retained as damages) and L. 113-9 (non-intentional — before
  a claim, premium increase or termination on ten days' notice with pro-rata refund; after a claim,
  the benefit is reduced in proportion to the ratio of premiums paid to premiums that would have
  been due) [S1][S2][S3][S6][S7].
- **Convention AERAS.** AERAS is retrieved in full [R17] and its scope is unambiguous: it governs
  *assurance emprunteur* on *prêts immobiliers*, *prêts professionnels* for premises and/or
  equipment, and *prêts à la consommation affectés ou dédiés*. **A standalone temporaire décès
  unconnected to a loan is outside AERAS.** Its parameters are recorded here because the *grille de
  référence* and the *droit à l'oubli* shape how French medical officers assess aggravated risks
  generally, and because the frlib ADE product will cite them: three examination levels; third-level
  eligibility conditioned on maturity **before the borrower's 71st birthday** and an insured share of
  outstanding loans not exceeding **420 000 €**; health questionnaires dropped on consumer loans of
  **≤ 17 000 €**, term **≤ 4 years**, applicant **≤ 50**; *écrêtement des surprimes* at the 2nd and
  3rd levels for eligible incomes (≤ 1 / 1,25 / 1,5 × PASS by number of tax *parts*), capping the
  insurance premium at **1,4 point in the taux effectif global**, with full absorption of the
  surprime on a PTZ for borrowers under 35; *droit à l'oubli* after **5 years** from the end of the
  therapeutic protocol without relapse for cancer and hepatitis C; and a *grille de référence*
  setting maximum surprime rates and delays **per garantie (Décès, PTIA, GIS)** [R17]. The 2023
  version carries an *avenant* of 5 July 2024 [R18].

### 11. Premiums: attained-age revisable vs level
- **The French standalone temporaire décès is priced on an annually revisable attained-age basis.**
  This is uniform across every insurer document retrieved and is stated in the contracts themselves:
  - MAAF: the cotisation depends on "l'âge de l'assuré à la date d'effet de l'adhésion **puis à la
    date de la reconduction** de l'adhésion", and "le tarif évolue au 1er janvier de chaque année, il
    est calculé en fonction de l'âge de l'assuré" [S1].
  - Macif: "La cotisation évolue chaque année en fonction de votre âge et du taux de revalorisation
    fixé par l'Assureur" [S2].
  - MAIF: the cotisation is a percentage of the capital "correspondant à votre âge au moment de la
    souscription, **puis au moment de la reconduction annuelle**"; "Pour un même capital garanti,
    votre cotisation évoluera en cours de contrat en fonction de votre âge : elle sera donc calculée
    à chaque échéance annuelle" [S3]; the current page repeats "recalcul chaque année" [S4].
  - Mutex: "Votre cotisation va évoluer chaque année, à la date anniversaire de votre adhésion, en
    fonction de votre âge" [S6].
  - AXA: "les cotisations évoluent, à l'échéance anniversaire de l'adhésion, en fonction de l'âge de
    l'assuré" [S7].
  - MUTUALP: cotisations "déterminé chaque année en fonction de l'âge atteint", changing on 1 January
    of the civil year following the birthday [S9].
  - MetLife's own price point is quoted "in year one" [S10].
- **A level (*constante* / *nivelée*) premium was not found on any standalone French contract in
  this research.** The level form appears in French practice on *assurance emprunteur*, where the
  rate is guaranteed for the whole loan term and is expressed either on *capital initial* or on
  *capital restant dû* [R13]. A broker guide mentions 10, 15 and 20-year terms for temporaire décès
  [S16] but does not say the premium is level, and no insurer document confirms it. **Treat "level
  premium temporaire décès" as `[unverified]` for France**, and let the model's default be the
  attained-age revisable form — with the level form available as an alternative, since it is the
  form that generates a *provision mathématique*/PRC and is therefore the more interesting mechanics
  demonstration [R11][R13].
- The pricing drivers stated in the contracts, beyond age and capital:
  - **Smoker / non-smoker**: MAAF ("votre profil tabagique") [S1], AXA (declared at adhesion, with a
    duty to notify a return to smoking) [S7], MetLife (non-smoker status revisable downwards after
    12 months without tobacco) [S10].
  - **Occupation**: AXA prices by a "groupe tarifaire défini en fonction de sa profession" [S7];
    Macif and MUTUALP annex lists of hazardous occupations that modify the tariff [S2][S9].
  - **Sporting activities** and **conditions of exercise of the occupation** [S7][S2].
  - **Medical acceptance conditions** — the *surprime* [S1][S2][S3][S6][S7].
  - **Sex may not be a driver** for contracts written from 21 December 2012 [R10].
- **Other repricing triggers**, all of which appear in the contracts and all of which are
  policyholder-facing rather than actuarial:
  - Legislative or regulatory change [S1][S6][S7].
  - "L'accroissement de la fréquence et/ou du coût moyen des sinistres" [S1] and "les résultats des
    garanties Assurance Décès" [S6] — i.e. **experience repricing of the whole class**.
  - Where an increase is decided by the insurer (as opposed to arising from age, indexation or a
    legislative change), the member may terminate within **30 days** of learning of it, with cover
    maintained on the old terms until termination takes effect one month after the request [S1];
    AXA gives **15 days** to terminate on a tariff change, effective one month later [S7]. An
    increase resulting from a change of age, of the index, or of law "n'ouvre droit ni à
    contestation ni à résiliation" [S1].
- **Premium payment** is annual in advance as the base case, with half-yearly, quarterly and monthly
  fractionation available and normally by SEPA direct debit [S1][S2][S6][S7][S8][S9]. Premium
  payment **ceases** at death and at recognition of PTIA/IPT [S3][S7], and is collected at the
  latest to the échéance following the death-cover age limit [S3].
- **Age-error rule.** Art. L. 132-26: if the true age falls outside the contract's limits the cover
  is void and premiums are returned; if it falls inside, an underpaid premium reduces the benefits
  proportionately and an overpaid premium is refunded [S7].

### 12. A real published tariff structure
- MAIF publishes the whole grid in its *note d'information* — the only complete French standalone
  temporaire décès rate card retrieved. "Pour calculer votre cotisation annuelle, il vous suffit de
  multiplier le montant du capital que vous choisissez par le tarif en pourcentage … correspondant à
  votre âge au moment de la souscription, puis au moment de la reconduction annuelle." [S3]

  **Tarif de base annuel, in per cent of the guaranteed capital, by attained age** [S3]:

| Age | Rate | Age | Rate | Age | Rate | Age | Rate | Age | Rate |
|---|---|---|---|---|---|---|---|---|---|
| 18–34 | 0,15 % | 42 | 0,32 % | 50 | 0,64 % | 58 | 1,05 % | 66\* | 2,55 % |
| 35 | 0,17 % | 43 | 0,36 % | 51 | 0,69 % | 59 | 1,13 % | 67\* | 2,78 % |
| 36 | 0,17 % | 44 | 0,40 % | 52 | 0,74 % | 60 | 1,56 % | 68\* | 2,88 % |
| 37 | 0,19 % | 45 | 0,44 % | 53 | 0,79 % | 61 | 1,68 % | 69\* | 3,14 % |
| 38 | 0,20 % | 46 | 0,48 % | 54 | 0,85 % | 62 | 1,81 % | 70\* | 3,43 % |
| 39 | 0,22 % | 47 | 0,52 % | 55 | 0,91 % | 63 | 1,97 % | 71\* | 3,74 % |
| 40 | 0,24 % | 48 | 0,56 % | 56 | 0,93 % | 64 | 2,14 % | 72\* | 4,09 % |
| 41 | 0,29 % | 49 | 0,60 % | 57 | 0,99 % | 65 | 2,33 % | 73\* | 4,46 % |
| | | | | | | | | 74\* | 4,86 % |

  \* MAIF's own footnote: "Vous ne devez pas avoir plus de 65 ans lors de la souscription : la
  dernière colonne vous indique donc le tarif de base, en cours de contrat, pour couvrir le risque
  de décès entre 65 et 75 ans." [S3]

- MAIF's two worked examples, which the grid must and does reproduce: "Vous avez 34 ans et souhaitez
  être assuré(e) pour un capital de 20 000 €. Votre cotisation s'élèvera à : 20 000 € × (0,15 : 100)
  = **30 €** pour un an." and "Vous avez 49 ans … pour un capital de 150 000 € … 150 000 € × (0,60 :
  100) = **900 €** pour un an." [S3]
- Structural features of the grid, which a `[std]` proxy table should reproduce:
  - **Flat at 0,15 % from 18 to 34** — a floor, not a mortality curve. Below age 35 the rate is
    dominated by expenses and by the minimum viable premium, not by q(x).
  - From 35 the rate rises at roughly **7–9 % per year of age**. Over ages 42–58 the ratio
    r(x+1)/r(x) runs from 1,022 (the flat step 55 → 56, 0,91 % → 0,93 %) to 1,125 (42 → 43), with a
    median near 1,076; over ages 66–74 it runs from 1,036 (the flat step 67 → 68) to 1,094, median
    about 1,090.
  - A **discontinuity at 59 → 60**: 1,13 % → 1,56 %, a jump of **+38 %** against a trend of +8 %.
    This is a tariff step, not a mortality step, and is the sort of thing a fitted curve will smooth
    away and a test should catch.
  - The rate at 74 (4,86 %) is **32,4×** the rate at 34 (0,15 %).
- Two further published price points, both consistent in order of magnitude and both signalling that
  rates have drifted since the S3 vintage:
  - MAIF, current page: **6,29 €/month at age 35 for a capital of 40 000 €** [S4] — 75,48 €/year, i.e.
    0,189 % of the capital, against the 0,17 % in the S3 grid. The gap is partly rate drift and
    partly the monthly-payment loading.
  - MetLife: **8,24 €/month in year one for a 40-year-old non-smoker with a capital of 50 000 €**
    [S10] — 98,88 €/year, i.e. 0,198 %, against MAIF's 0,24 % at age 40. MetLife's is a non-smoker
    rate, MAIF's grid is not smoker-differentiated.
- **No other insurer publishes rates.** MAAF, Macif, Mutex, AXA, Antarius, MUTUALP and MACSF all
  refer the member to the *certificat d'adhésion* or *avis d'échéance* for the amount
  [S1][S2][S6][S7][S8][S9][S12].

### 13. Charges
- French *notices* separate three things, and only the first two are actuarial:
- **Frais de gestion** (management charges) are built into the tariff and are not separately
  disclosed on any retrieved contract. Their existence is nevertheless load-bearing for reserving:
  art. R. 343-3 requires the *provision mathématique* to include an estimate of future management
  costs "égale au montant des chargements de gestion prévus dans les conditions tarifaires" [R11].
  So the tariff loading is the reserving loading, by construction.
- **Frais sur cotisation** in the sense used for savings contracts (an entry load on each premium)
  does **not** appear as a separate line on any retrieved temporaire décès. The nearest disclosed
  equivalents are the fractionation loadings below and the annuity-conversion charge.
- **Frais de fractionnement et frais d'échéance** — the only charges disclosed with figures, at MAAF
  [S1]:

| Payment frequency | Frais de fractionnement, included in the cotisation TTC | Frais d'échéance / frais de gestion annuels, billed once |
|---|---|---|
| Annual | none; **1 % discount** included in the cotisation where paid by direct debit | none |
| Half-yearly | **2,50 %** | **3 €** |
| Quarterly | **4 %** | **6 €** |
| Monthly (10 or 12 instalments, direct debit compulsory) | **4 %** | **15 €** for 10 instalments, **18 €** for 12 |

  MAAF's own worked example: on a monthly-in-12 basis with an annual tariff of 250 € TTC, the
  embedded loading is 250 − 250/1,04 = **9,61 €** [S1]. These charges are revisable annually, and an
  increase gives the member 30 days to terminate [S1]. Macif and Mutex apply *frais de
  fractionnement* whose level is stated in the *certificat individuel de garantie* rather than the
  notice [S2][S6].
- **Association subscription.** MAAF remits **1,30 € per member per year** to ANS Vie-Covéa out of
  the charges levied [S1]. A small but real per-policy expense in a group wrapper.
- **Annuity conversion charge.** MAIF: **3 % of the capital to be converted** as *frais de service de
  la rente* [S3]. MAAF levies unspecified *frais de gestion* on a conversion [S1].
- **Taxes.** The contracts quote cotisations "TTC" [S1], but no retrieved document states a rate of
  *taxe sur les conventions d'assurance* for this cover. `[unverified]`.

### 14. Pricing and reserving bases: tables, unisex, technical rate
- **Regulatory tables.** For contracts other than *rentes viagères*, the homologated tables are
  **TH00-02** (male) and **TF00-02** (female), homologated by the arrêté du 20 décembre 2005 with
  effect from **1 January 2006** and built by INSEE from observed French mortality over **2000–2002**
  [R6][R9]. They are *moment* (period) tables, not generational [R9]. The generational **TGH05** and
  **TGF05**, homologated by the arrêté du 1er août 2006 with effect from 1 January 2007, apply to
  *rentes viagères* and are relevant to this product only where a death capital is converted into an
  annuity [R7][S3][S1].
- **Which article now governs.** The historic home of the rule, art. A. 335-1, was **abrogated with
  effect from 1 January 2016** by the arrêté du 28 décembre 2015 [R8]. The operative article is now
  **art. A. 132-18** [R4].
- **Two admissible families of table** under A. 132-18 [R4][R13]:
  - **(a)** ministerially homologated tables, by sex, built on INSEE data for non-annuity contracts;
    where a single table is used for all insureds, it must be **the appropriate table producing the
    most prudent tariff** — which for a death cover means the male table, TH00-02.
  - **(b)** the undertaking's own tables, by sex or not, **certified by an independent actuary**
    approved by a recognised actuarial association, built on the undertaking's own or
    demographically equivalent experience data. The floor requiring family (b) not to undercut
    family (a) applies to **annuity** contracts, not to death contracts [R4].
- **Décalages d'âge.** Homologated tables in family (a) must be applied "en corrigeant l'âge de
  l'assuré conformément aux décalages d'âge ci-annexés", for *contrats en cas de vie* other than
  annuities [R4][R6]. The Institut des actuaires notes that the arrêté specifies the shifts but
  **not how to apply them**, and recommends applying the shift **to the q(x), not to the l(x)**,
  because shifting l(x) produces erratic q(x) growth and hence erratic life expectancies, annuity
  values and provisions [R9]. The numeric shift table is annexed to A. 132-18 but the Légifrance
  page carries only a pointer to the JO facsimile (JO n° 0301 du 29/12/2015, texte n° 35); **the
  values were not retrieved** [R4].
- **Unisex.** Art. L. 111-7 forbids direct or indirect sex-based differences in premiums and
  benefits; the surviving derogation covers only contracts and group-contract adhesions "conclus ou
  effectuées **au plus tard le 20 décembre 2012**" [R10]. New business has therefore been unisex
  since **21 December 2012**. The tension with the sex-specific regulatory tables is resolved in
  practice either by taking the single most prudent family-(a) table (TH00-02 for a death cover)
  [R4], or by a **mixed table**: the Institut des actuaires' working group uses **60 % TH 00-02 /
  40 % TF 00-02** as its unisex death basis [R13]. Neither weighting is prescribed by any retrieved
  text; a model that adopts one must tag it `[std]`.
- **Group-contract simplification.** "Pour les contrats collectifs en cas de décès **résiliables
  annuellement**, le tarif peut être établi d'après les tables mentionnées au a **avec une méthode
  forfaitaire** si celle-ci est justifiable" [R4]. That clause covers most of the group products in
  this file (S1, S2, S6, S7) and explains why their published rate structures are coarse.
- A newer derogation, **art. A. 132-18-1** (created by the arrêté du 18 novembre 2024, in force
  23 November 2024), allows tariffs for contracts under art. L. 911-1 of the Code de la sécurité
  sociale to use a **single mortality table for all insureds**, with a table annexed by age and birth
  year. This was read only from the Légifrance section listing, not from the article text — treat
  the detail as `[unverified]` [R4 section listing].
- **Technical interest rate.** Art. A. 132-1 caps the tariff rate at **75 % of the TME**, and beyond
  eight years at the lower of **3,5 %** and **60 % of the TME**; and, decisively for an annual
  renewable product, "pour les contrats **à primes périodiques** ou à capital variable, quelle que
  soit leur durée, ce taux ne peut excéder le plus bas des deux taux suivants : **3,5 % ou 60 % du
  taux moyen**" [R5]. In practice a one-year renewable death cover has almost no discounting to do;
  the Institut des actuaires' worked examples use technical rates of **0,5 %** and **0 %** against a
  1 % interest assumption [R13].
- **No French insurer publishes its pricing basis** — no table, no A/E factor, no loading, no lapse
  assumption appears in any retrieved product document.

### 15. No surrender value, no reduction — and why arts. L. 132-20 ff. do not bite
- Art. L. 132-23 alinéa 1: "**Les assurances temporaires en cas de décès ainsi que les rentes
  viagères immédiates ou en cours de service ne peuvent comporter ni réduction ni rachat.**" [R3]
  The prohibition is on the **insurer's ability to offer** these features, not merely on the
  policyholder's ability to demand them.
- The insurers say the same in their own words: "Article 13 - Rachat et réduction. **Votre adhésion
  ne comporte ni valeur de rachat, ni valeur de réduction.**" [S7]; "**Le contrat ne comprend pas de
  faculté de rachat.**" [S9]; "les cotisations versées restent acquises à l'assureur" at term [S5];
  "aucun capital n'est versé et les cotisations déjà payées ne sont pas remboursées" [S16]; "Si le
  risque garanti ne survient pas pendant cette période, aucune somme n'est versée" [S15].
- **Consequence for the model.** There is no account value, no surrender benefit, no paid-up
  (*réduit*) state and no non-forfeiture mechanism. A lapse is a pure termination: the cover ends,
  the unearned portion of a prepaid cotisation may be refunded (MAAF refunds the portion of the
  cotisation received in advance for the period after termination, except where the termination
  follows an intentional misstatement or non-payment [S1]), and nothing else is paid. `claims_lapse`
  is structurally zero for this product.
- The *rachat* machinery of arts. L. 132-20 and following — the insurer's duty to inform, the
  two-month transfer deadline of art. L. 132-21, the annual notification of the *valeur de rachat* —
  is written for contracts that **have** a surrender value. On a temporaire décès it is inoperative
  because L. 132-23 removes the value the machinery would act upon [R3]. The one place surrender
  value still appears in a reserving text is art. A. 343-1-1, which floors the *provision
  mathématique* at "la valeur de rachat du contrat" and at "la provision correspondant au capital
  réduit" — both of which are **zero** here, so the operative floor is simply that the provision may
  not be negative [R13].
- The non-payment path is therefore the whole of the lapse machinery: cotisation due within **10
  days** of the due date; a registered *mise en demeure*; resiliation **40 days** after the letter
  under the Code des assurances [S1][S2][S3][S6][S7], or suspension **30 days** after the mise en
  demeure under the Code de la mutualité [S9]. No cover attaches to events in the suspension window
  [S6].

### 16. Participation aux bénéfices and revalorisation
- Three distinct things are called *revalorisation* in these documents and must be separated:
  1. **Revalorisation des garanties et des cotisations** — the optional indexation of section 7,
     driven by the PASS or by an insurer-set rate [S1][S2][S6][S7].
  2. **Participation aux bénéfices** — computed globally at insurer level, not policy level, and
     paid out as higher benefits, higher benefits in payment, and/or reduced cotisations called
     [S1][S2]. Macif computes it under art. A. 331-4 and spreads it over the maximum period allowed
     by the Code des assurances [S2]. MUTUALP has none at all [S9].
  3. **Revalorisation post mortem** — the statutory uprating of the death capital from the date of
     death until the file is complete or the sum is deposited at the Caisse des dépôts under art.
     L. 132-27-2. MAAF: net of charges, at a rate set for each civil year, not below a floor set by
     decree [S1]. Macif: not below the art. R. 132-3-1 rate [S2]. MAIF: under art. R. 132-3-1 [S3].
     Mutex, under art. L. 132-5: the lower of the twelve-month average TME calculated at 1 November
     of the preceding year and the last TME available at that date [S6].
- **Capitaux non réclamés**: unclaimed capital is deposited at the Caisse des dépôts et
  consignations after **ten years** from the insurer's knowledge of the death or the contract's
  term, within the month following the expiry of that period [S1]. Beneficiaries' actions are
  prescribed at the latest **thirty years** after the death [S1].

### 17. Lapse, termination and the policyholder's exit
- **By the policyholder.** MAAF: two months' notice before 31 December each year [S1]. Macif: at any
  time, effective on receipt of the letter [S2]. MAIF: at the annual échéance, registered letter at
  least one month before [S3]. AXA: two months' notice before the anniversary [S7]. Antarius: at any
  time, effective the day before the premium due date following receipt [S8]. MUTUALP: withdrawal at
  31 December on request before 1 November [S9]. **The notice regime is materially different across
  insurers, and it drives the lapse timing a model assumes.**
- **By the insurer.** Non-payment [S1][S2][S6]; misstatement of risk at adhesion or in force where
  the member refuses the revised cotisation [S1][S2]; intentional misstatement [S2]; refusal of the
  new tariff after a change of occupation or sport [S2].
- **Of right.** At the age limits; on death; on payment of the PTIA capital; on termination of the
  underlying group contract (though MUTUALP's in-force adhesions continue to their term where the
  group contract is terminated) [S1][S2][S6][S9]; and at Antarius on closure of the bank account or
  loss of French/Monaco tax residence [S8].
- **Renunciation** (*délai de renonciation*): **30 calendar days** from being informed that the
  contract is concluded, under art. L. 132-5-1 [S3] or L. 132-5-2 [S1]; Macif runs the period from
  receipt of the *certificat individuel de garantie* and refunds the cotisations in full within 30
  days [S2]; MUTUALP under art. L. 223-8 of the Code de la mutualité [S9].
- **Prescription**: two years from the event, extended to **ten years** where the beneficiary is a
  person distinct from the member, and thirty years from the death as an absolute long-stop; arts.
  L. 114-1 to L. 114-3 and civil code arts. 2240 ff. are reproduced in full in the notices
  [S1][S3].
- **No insurer publishes a lapse rate.** Nothing in the retrieved corpus supports a lapse assumption;
  any assumption in the model is `[std]`.

### 18. Taxation
- **On the capital paid.** The death capital of a temporaire décès is not part of the estate: MAAF
  states "le capital versé au titre du contrat d'assurance vie temporaire décès est exonéré de
  fiscalité" and MAIF states "exonération de droits de succession" on the capital [S1][S3]. What
  applies instead is the art. 990 I levy and, for premiums paid after 70, art. 757 B [R14][R15].
- **Art. 990 I** — premiums paid **before the insured's 70th birthday**: abattement of **152 500 €
  per beneficiary**, aggregated across all life contracts of the same insured with all companies;
  then **20 %** on the taxable share up to **700 000 €** and **31,25 %** above it [R14][R15][R16][S1].
  Stated in capital terms as an insurer applies it: 20 % between 152 500 € and 852 500 €, 31,25 %
  above 852 500 € [R16]. The insurer withholds and remits, which is why the beneficiary must file an
  *attestation sur l'honneur* stating how much of the abattement has already been used [R16].
- **Art. 757 B** — premiums paid **from the insured's 70th birthday** on contracts subscribed after
  20 November 1991: subject to *droits de mutation à titre gratuit* by relationship, with a single
  global abattement of **30 500 €** shared across taxable beneficiaries and across all the insured's
  life contracts [R15][S1][S3]. MAAF adds that the 30 500 € also absorbs the entirety of any PER
  death capital where death occurs after the 70th birthday [S1]. `[unverified]` at article level —
  see R19.
- **Exemptions**: the surviving **spouse** and **PACS partner** are wholly exempt (art. 796-0 bis),
  as are **siblings** meeting the cumulative conditions of art. 796-0 ter [R14][R15][R16][S1][S7].
  Exempt beneficiaries file no attestation [R16].
- **Scope confirmation that matters here**: BOFiP states that the 990 I levy reaches *assurance décès
  temporaire* and *assurance décès pure* where the beneficiary is designated *à titre gratuit*, and
  **excludes** contracts designated *à titre onéreux* — the paradigm being loan cover assigned to a
  lender [R15]. So a standalone temporaire décès is in scope; the borrower product typically is not.
- **Premiums are not deductible.** No retrieved document grants any income-tax deduction for the
  cotisations of a standalone temporaire décès. What the notices instead impose is a *declaration*
  duty: MAIF requires the beneficiary to declare in full any annual premium paid before age 70
  exceeding **305 €**, and requires a sworn statement of sums received from other insurers where the
  contract's annual cotisation exceeds **305 €** [S3].
- **Social contributions.** MAAF states explicitly: "L'assurance temporaire décès à la différence de
  l'assurance vie **n'est pas soumise aux prélèvements sociaux**" [S1]. Where the capital is
  converted to an annuity, however, MAIF's schedule applies: the taxable fraction of a *rente
  viagère* is **70 %** below age 50, **50 %** at 50–59, **40 %** at 60–69 and **30 %** from 70, taxed
  at income-tax rates and subject to **17,2 %** social contributions on the taxable fraction; a
  *rente temporaire* is exempt from income tax but bears the same social contributions [S3].
- **PTIA/IPA benefits** are exempt from income tax [S3][S7].

### 19. Reserving and prudential context (for the projection model)
- **Statutory (French GAAP) provisions** for a life contract are listed at art. R. 343-3; the
  operative one here is the **provision mathématique**, "la différence entre les valeurs actuelles
  des engagements respectivement pris par l'assureur et par les assurés", which **must include an
  estimate of future management costs** equal to the *chargements de gestion* in the tariff [R11].
  A commitment may be provisioned under one category only [R11]. The list also contains a
  **provision d'égalisation** specifically for *assurance de groupe contre le risque décès* [R11].
- **On a one-year attained-age renewable contract the mathematical provision is close to nil at each
  anniversary** — the premium for the year has been charged for that year's risk — and what remains
  is an unearned-premium and outstanding-claims position. On a **level-premium** contract the
  provision builds and releases in the classic way, and the French texts call it a PM in life and a
  PRC in non-life for the identical calculation [R13].
- **Provision pour risques croissants** (art. R. 343-7) is defined for *maladie* and *invalidité*
  operations, not death [R12]; its death-cover analogue is the R. 343-3 PM [R11][R13].
- **Art. A. 343-1-1**: mathematical provisions on periodic-premium contracts must bring the
  acquisition loadings into the premium-payer's commitment; the resulting provision may be neither
  negative, nor below the surrender value, nor below the reduced-capital provision — the latter two
  being zero for a temporaire décès [R13][R3].
- **ANC 2015-11 art. 142-3** (as amended by ANC 2016-12): provisions are computed at interest rates
  at most equal to those used to build the tariff, and on the tables in force when the tariff was
  applied, with the option to migrate all in-force contracts to the tables appropriate at each
  subsequent annual inventory, and to spread the effect of a change of basis over **at most eight
  years** [R13].
- **The qualitative reserving result to carry into the technical notes** [R13]: where the premium
  *rate* is flat while the death rate rises with age, a provision is built throughout the term —
  "un montant de PRC est toujours constitué pendant la durée" — whereas a tariff expressed on an
  initial (rather than declining) capital tends to show a **negative** provision in the early years,
  which the non-negativity floor then bites on. Medical selection changes the picture materially:
  the working group's illustrative abatement on claims is **70 % in year 1, 50 % in year 2, 20 % in
  year 3**, and under that assumption a provision can become necessary even on an initial-capital
  tariff [R13].
- **Solvency II** sits above all of this; nothing product-specific was retrieved for France, and the
  ACPR's own site could not be fetched [R20]. The library's posture is to treat the capital layer as
  cited-not-specified.

### 20. Market context
- French *assurance prévoyance* premiums were **40,3 Md€ in 2025** [R21]. The split between
  *garanties décès* (temporaire décès, obsèques, emprunteur), *incapacité-invalidité* and
  *dépendance* is not published on the retrieved page and is **not** available in this file.
- For scale against the savings side, assurance vie premiums ran at **19,3 Md€ in the single month
  of June 2026** [R22].
- The comparison French insurers use to size the product is the state death benefit: Macif notes
  that the Sécurité sociale pays a flat *capital décès* of **3 450 €** (amount at 1 April 2018)
  regardless of the deceased employee's earnings, against an estimated need of more than a year's
  salary [S2].

---

## Variations across insurers

| Feature | MAAF [S1] | Macif [S2] | MAIF [S3][S4] | Mutex [S6] | AXA Avizen [S7] | Antarius [S8] | MUTUALP [S9] | MetLife [S10] |
|---|---|---|---|---|---|---|---|---|
| Wrapper | group, assoc. ANS Vie-Covéa | group, Macif/Macif-Mutualité | **individual** | group | group, ANPERE | group, bancassurance | group, **Code de la mutualité** | not stated |
| Entry age | 18–75 | 18–67 (Ess. ≤ 50) | ≤ 65 | 18–80 | not stated | 18 to <66 | not stated | 18–84 |
| Death cover ends | year of 85 | 1 Apr after 80 | échéance after 75 | anniv. in year of 85 | ins. year of 85 | anniv. after 70 | 31 Dec of year of 65 | 90 |
| PTIA cover ends | same as death | 1 Apr after 75 | échéance after 65 | anniv. in year of 80 | ins. year of 67 | anniv. after 65 | none | not stated |
| Capital range | 10 k – 2 M € | 25 k – 762 k € | 20 k € – no ceiling | ≤ 200 k € | not stated | 100 k – 1 M € | 6 097,96 € – 45 k € | ≤ 50 M € |
| Accidental option | doubling | doubling | none in notice | additional capital = death capital | separate accident capital | none | **+50 %** | not stated |
| Triplement | no | no | no | no | no | no | no | no (MACSF only [S12]) |
| Double effet | no | no | no | no | **yes** | **yes**, ≤ 500 k € | no | no |
| Rente éducation | 75–3 810 €/quarter | no | via payout mode | no | with 100/125/150 % steps | no | no | ≤ 2 000 €/month |
| Délai d'attente | none | none | none | **12 months** if no medical formality | none | none | **3 months** | none |
| Provisional accident cover | not stated | **60 days**, ≤ 76 k € | **30 days**, ≤ 15 k € | not stated | not stated | not stated | not stated | not stated |
| Underwriting thresholds published | no | no | **≤ 250 k € to age 40 simplified** | **≤ 40 k € and ≤ 50: none** | no | no | no | no |
| Smoker rating | **yes** | no | not in notice | no | **yes** | no | no | **yes**, revisable after 12 months |
| Occupation rating | excluded occupations only | hazardous-occupation annex | *majoration* possible | hazardous-occupation list | **tariff group by profession** | no | hazardous-occupation annex | yes |
| Premium basis | attained age, revised 1 Jan | attained age, revised annually | attained age, **grid published** | attained age, revised at anniversary | attained age, revised at anniversary | not stated | attained age, revised 1 Jan | attained age ("year one") |
| Indexation | PASS | insurer rate | not in notice | insurer rate | PASS, ends at 70 | not stated | no | not stated |
| Participation aux bénéfices | yes, global | yes, global (A. 331-4) | not stated | not stated | not stated | not stated | **none** | not stated |
| Fractionation charges published | **yes, full table** | in the certificat | no | no | no | no | no | no |
| Lapse notice | 2 months before 31 Dec | any time | 1 month before échéance | any time | 2 months before anniv. | any time | before 1 Nov for 31 Dec | not stated |

**Representative design for a reference implementation.** MAIF Rassurcap Solutions [S3][S4] is the
cleanest representative and should be the model's template: an **individual** annual contract
renewed by *tacite reconduction*; death cover from any cause to the échéance following age 75; an
**IPA/PTIA acceleration** of the same capital, ending the contract, running to the échéance following
age 65; a constant capital chosen by the subscriber with a 20 000 € minimum; **cotisation = capital ×
published attained-age rate, recomputed at every renewal**; premiums payable annually or monthly and
ceasing at death or acceleration; **no surrender value and no reduced paid-up value**; a suicide
exclusion in the first year, restarting for the increment on any increase; and a defined list of
contractual exclusions. It is the only retrieved contract that publishes a full rate card, so it is
the only one whose premiums a model can reproduce exactly rather than assume.

The other seven differ in **parameter bounds and rider inventory, not in structure**: the same
annual-renewable, attained-age-priced, no-surrender-value cash-flow engine covers all of them with
configuration. The genuine structural variants a reference implementation should be able to switch
on are four:
1. the **délai d'attente** with return of premiums, where underwriting is waived (Mutex, MUTUALP)
   [S6][S9];
2. the **double effet** second death benefit on the spouse (AXA, Antarius) [S7][S8];
3. the **capital décès double garantie** — a further capital on death at least a year after an IPT
   acceleration (AXA) [S7];
4. the **accidental multiplier**, at ×2 or, at MACSF, ×3 for road accidents, terrorism, *attentat* or
   *agression* [S1][S2][S6][S9][S12].

Rider-level annuity conversions (*rente éducation*, *rente de conjoint*, *rente temporaire*) are
best treated as a post-death payout mode on the same capital rather than as separate liabilities;
every retrieved contract computes them from the same guaranteed capital using the tables and
technical rate in force **at the date of conversion**, not at issue [S3][S1].

Institutional variations, context rather than model scope:
- The *mutualité* form (MUTUALP [S9]) is regulated under the Code de la mutualité, uses shorter
  non-payment timers (30 days rather than 40) and different renunciation and withdrawal articles
  (L. 223-8, L. 221-10), but is economically identical.
- The *bancassurance* form (Antarius [S8]) ties cover to a bank relationship and terminates it when
  the account closes — a lapse driver with no actuarial counterpart in the other contracts.
- The professional-body form (MACSF [S12]) segments its tariff and its age limits by profession
  (*infirmières* enter only to the day before their 50th birthday against 57 for others).
- *Assurance emprunteur* is a separate product with its own file. It shares the death risk and the
  regulatory tables but differs on every point that matters for cash flows: a decreasing or fixed
  sum insured tied to a loan, a **rate guaranteed for the whole loan term** rather than revised
  annually, the AERAS and *loi Lemoine* underwriting regime, immediate suicide cover up to
  120 000 € on a principal residence, and a beneficiary designated *à titre onéreux* which takes it
  outside the 990 I levy [R1][R2][R13][R15][R17].

---

## Gaps and caveats

1. **No level-premium French contract was found.** The brief anticipated a *cotisation constante /
   nivelée* form alongside the *révisable par âge* form. Every one of the eight standalone contracts
   retrieved prices on the attained-age revisable basis [S1][S2][S3][S6][S7][S9][S10], and the two
   secondary guides that mention multi-year terms [S13][S16] say nothing about the premium being
   level. The level form was confirmed only for *assurance emprunteur*, where the rate is guaranteed
   for the loan term [R13]. **Any level-premium temporaire décès in the frlib product spec is a
   `[std]` construction**, defensible as a mechanics demonstration (it is the form that generates a
   real *provision mathématique*) but not sourced to a French contract.

2. **The MAIF tariff grid is a 2019–2021 vintage.** S3 was retrieved from a third-party mirror and
   its internal worked examples are dated 2019. MAIF's current page quotes 6,29 €/month at age 35 for
   40 000 € [S4], which implies about 0,189 % against the grid's 0,17 % — so rates have moved. Use
   the grid for **shape**, and treat its levels as a dated data point rather than a current rate
   card. MAIF's own contractual-documentation host was not reachable for this file, so no current
   edition of the note d'information was retrieved.

3. **The AXA Avizen notice is a 2013-vintage tax section.** Its structural clauses (the no-rachat
   article, the IPT and double-effet mechanics, the tariff-group and smoker drivers, the L. 132-26
   age rule) are used here; its tax figures are not — the tax content in these notes comes from S1
   (2026), R14, R15 and R16 instead.

4. **The *décalages d'âge* values were not retrieved.** The Légifrance page for the annexe to
   art. A. 132-18 carries only a pointer to the JO facsimile (JO n° 0301 du 29/12/2015, texte n° 35)
   [R4]. Any statement about the magnitude or age bands of the shifts is `[unverified]`. A summary
   fetch of the abrogated A. 335-1 annexe reported shifts "ranging from −13 to 0 years, varying by
   gender and age bracket" [R8]; that range is a **secondary summary, not a read table**, and is
   tagged `[unverified]`.

5. **Regulatory table data is cited, not shipped.** TH00-02, TF00-02, TGH05 and TGF05 are annexed to
   ministerial *arrêtés* [R6][R7], and partial extracts appear inside the Institut des actuaires
   notice [R9], but this library does not redistribute them. The frlib decrement CSVs must be
   `[std]` proxies built from public INSEE data, anchored so the model's best-estimate factor
   reproduces the notes' own placeholder rate exactly — the same posture uklib takes about CMI
   tables. The 60 % TH00-02 / 40 % TF00-02 unisex mix is a **market practice observed in one
   actuarial working-group document** [R13], not a rule; adopting it requires a `[std]` tag.

6. **Date discrepancy on the TH/TF arrêté.** Légifrance carries the instrument as the **arrêté du
   20 décembre 2005** (NOR ECOT0591210A) [R6]; the Institut des actuaires' own notice heads itself
   "ARRÊTÉ DU 29 DÉCEMBRE 2005" [R9]. Both agree the tables took effect on 1 January 2006. The
   Légifrance date is the one to cite; the discrepancy is most likely signature date versus JO
   publication date, but this was **not confirmed**.

7. **CGI art. 757 B was not retrieved at article level** [R19]. Its Légifrance identifier could not
   be located: the session's web-search budget was exhausted and no URL was guessed. The 30 500 €
   abattement, the 20 November 1991 subscription cut-off and the post-70 premium rule are cited from
   BOFiP [R15], from CNP's notice [R16] and from the MAAF and MAIF notices [S1][S3] instead.
   Anything article-level about 757 B is `[unverified]`.

8. **Three official French sources returned errors and are cited from nowhere.** The ACPR site
   returns HTTP 403 to a plain fetcher on both its French and English roots [R20] — consistent with
   the known behaviour of French and UK regulator hosts. The economie.gouv.fr AERAS page returns
   HTTP 403 on repeated attempts, and the service-public fiche F2377 redirects to
   `service-public.gouv.fr` and then 404s, so **no official government-portal description of the
   product is in this file** [R23]. Abeille Assurances' comparison page likewise 403s [S14]. Nothing
   is cited from any of them.

9. **A. 132-1's rate-step rule is unconfirmed.** Secondary summaries describe a *barème* of technical
   rates with origin 0 and a step of 0,25 point, floored at 0; that sentence was **not visible** in
   the retrieved article text [R5] and is `[unverified]`.

10. **Art. A. 132-18-1 was read only from a section listing.** The 18 November 2024 derogation
    allowing a single mortality table for art. L. 911-1 CSS contracts, and its annexed table by age
    and birth year, were reported by the Légifrance section index; the article text itself was not
    fetched. Treat as `[unverified]`.

11. **A. 160-2 minimum-annuity thresholds disagree across vintages.** MAAF's 2026 notice cites
    **110 € per month** [S1]; MAIF's 2019/2021 note cites **480 € per year** [S3]. Both quote art.
    A. 160-2. The threshold has evidently been raised between the two vintages; the article itself
    was **not retrieved**, so neither figure is confirmed at source and the model should not depend
    on either.

12. **No pricing bases, no surprime scales, no lapse rates, no expense loadings are public.** No
    French insurer publishes its mortality table, A/E factor, expense assumption, lapse assumption or
    *surprime* scale for this product [S1][S2][S3][S6][S7][S8][S9][S12]. The MAIF grid [S3] is the
    only rate card in the corpus, and it is a gross premium scale, not a basis. Everything else the
    model needs — decrements, expenses, lapses, the split of the gross premium into risk premium and
    loading — is `[std]`.

13. **The MACSF DIPA PDFs were not retrieved.** The product page names three profession-specific
    DIPA documents but exposes only truncated `/content/download/...` paths [S12], so the MACSF
    doubling/tripling parameters are recorded at page level only, with no capital amounts, age
    tables or premium structure.

14. **Insurer coverage is deliberately mutualist-heavy.** MAAF, Macif, MAIF, Mutex and MUTUALP are
    mutual insurers; AXA and Antarius supply the stock-company and bancassurance comparators, and
    MetLife the foreign-owned specialist. **Generali, Groupama, CNP (as a manufacturer of this
    product), Cardif, Swiss Life, AG2R La Mondiale and Malakoff Humanis were not sourced** — the
    web-search budget was exhausted before their document libraries could be located, and no URL was
    guessed. Their contracts may carry variants not represented here.

15. **The prévoyance market breakdown is missing.** France Assureurs publishes a headline
    40,3 Md€ of *cotisations en assurance prévoyance* for 2025 [R21], but the split by garantie
    (temporaire décès vs obsèques vs emprunteur vs incapacité-invalidité vs dépendance) sits in the
    linked report "L'assurance prévoyance en 2025", which was **not retrieved**. There is therefore
    no sourced figure for the size of the standalone temporaire décès segment.

16. **Art. L. 132-7 changed on 20 August 2026 and no product document reflects it.** The new alinéa
    bringing death by *aide à mourir* within the death cover [R1] post-dates every retrieved
    *notice* and *conditions générales*. Insurer wordings will be updated; until they are, there is a
    gap between the statutory rule and the contractual text, and any statement about how insurers
    will administer it is `[unverified]`.

17. **Living texts.** L. 132-23 was captured as at 14 June 2026 [R3]; L. 132-7 as at 20 August 2026
    [R1]; L. 111-7 as at 24 October 2024 [R10]; A. 132-1 and A. 132-18 as at 7 September 2017
    [R4][R5]; R. 343-3 as at 1 January 2020 [R11]; R. 343-7 as at 10 June 2024 [R12]; CGI 990 I as at
    11 March 2023 [R14]; BOFiP BOI-TCAS-AUT-60 as at 30 March 2023 [R15]; the Convention AERAS at its
    2023 version plus a 5 July 2024 *avenant* [R17][R18]. Check for later amendments before relying
    on any article number or figure.
