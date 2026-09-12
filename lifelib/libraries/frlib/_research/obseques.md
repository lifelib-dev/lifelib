# Funeral Insurance (contrat obsèques, capital form) — research notes (France)

Research notes for the French individual funeral insurance contract (*contrat obsèques*) in its
capital form — a whole-life assurance (*assurance vie entière*) whose death capital is earmarked
to the payment of the insured's funeral. These notes are the citation ground truth for the frlib
`obseques` product documents: source ids S1..S20 and R1..R25 below are frozen — never renumber.

Access date for all citations: 2026-08-26.

Citation discipline: every extracted fact is tagged `[S#]` or `[R#]` pointing at a document that
was actually fetched and read. `[unverified]` marks statements from general knowledge or from
secondary summaries of documents that could not be retrieved. Where a fetch failed the failure is
recorded and the item is kept only as a known reference (fetched_ok = false).

Language note: French terms of art are kept in French and glossed on first use — *contrat en
capital* (capital-form contract), *contrat en prestations* (services-form contract), *notice
d'information* (policy information booklet), *conditions générales* (general conditions),
*cotisation* / *prime* (premium), *délai de carence* or *délai d'attente* (waiting period),
*participation aux bénéfices* (PB, profit sharing), *revalorisation* (uprating of the guaranteed
capital), *rachat* (surrender), *valeur de rachat* (surrender value), *réduction* (making the
contract paid-up), *valeur de réduction* (paid-up sum assured), *provision mathématique* (PM,
mathematical reserve), *renonciation* (cooling-off), *opérateur funéraire* (funeral operator).

A structural point that shapes everything below: since July 2025 every French funeral insurer
publishes a **standardised comparison table** ("tableau d'exemples normalisés") giving, for a
5 000 € guaranteed capital and entry ages 50 / 60 / 70, the annual premium, the cumulative
premiums by age at death, and the surrender values by duration, for each premium form on offer.
These tables were produced under a 2024 CCSF opinion [R11, R13–R16] and are the closest thing to
a public rate card that exists for any French life product. Sixteen of them, from seven insurers,
are the numerical backbone of these notes.

---

## Primary sources

### S1 — Harmonie Mutuelle / Mutex, "NÉOBSIA Garantie obsèques en capital — Conditions générales"
- Publisher: Mutex SA (insurer, Code des assurances, branche 20 Vie-Décès), distributed by
  Harmonie Mutuelle; assistance by Ressources Mutuelles Assistance (RMA)
- Doc type: Conditions générales valant note d'information, 14 pp.
- URL: https://www.harmonie-mutuelle.fr/sites/default/files/2024-02/CG-GARANTIEOBSEQUES.pdf
- Retrieved: YES (PDF downloaded, full text extracted with PyMuPDF).
- Content: the single most complete contract wording retrieved. Individual whole-life contract
  (*contrat individuel d'assurance vie entière*), branche 20, subject to the Code des assurances,
  serving art. L. 2223-33-1 CGCT. Capital chosen between 2 000 € and 10 000 €, all Mutex funeral
  capitals for one insured capped at 10 000 € in aggregate. Entry age 18 to 84 inclusive
  (*différence de millésime*), **no medical selection whatsoever**. Premium durations: constant
  temporary over 5, 10, 15, 20 or 25 years, or constant lifetime (*viagère*); the choice is final;
  premiums payable annually in advance with monthly / quarterly / half-yearly instalment options.
  One-year *délai d'attente*: accidental death covered from inception, all other causes covered
  only after one year; death by other than accident in year 1 pays back the premiums collected.
  Suicide excluded in the first year (and in the first year following a capital increase), war and
  nuclear exclusions — in every excluded case the insurer's liability is limited to the surrender
  value. Charges: 5 % on every premium; 0,40 % p.a. of the guaranteed capital for the whole life of
  the contract, plus 0,57 % p.a. during the lifetime-premium paying period or 0,80 % p.a. during a
  temporary-premium paying period; no exit charge, no instalment charge. PB under arts. A. 132-10
  to A. 132-17 CA, allocated as *participation aux bénéfices pour une durée maximale* (A. 132-16),
  a rate set annually for contracts in force at least one year. Post-mortem revalorisation under
  art. L. 132-5 CA at the lesser of the 12-month average TME and the last TME available at 1
  November of the preceding year. Surrender at any time equal to the mathematical provision, paid
  within 30 days (art. 20.3: at the latest within the month following receipt of documents).
  Réduction on cessation of premiums; automatic substitution of rachat for réduction if the
  surrender value falls below half the monthly SMIC (art. R. 132-2 CA). 30 calendar-day
  renonciation with full refund. First-rank beneficiary is the funeral firm that carried out the
  services, failing that whoever paid the invoice; the balance goes to the designated
  beneficiaries; payment within 8 days of receipt of documents. Annual statement per L. 132-22 CA.
  Taxation: arts. 990 I and 757 B CGI on death, art. 125-0 A CGI on surrender, social levies under
  art. L. 136-7 CSS. FGAP membership under art. L. 423-1 CA. Contains a worked table of premiums
  and surrender values for entry age 65, capital 1 000 €, technical rate 0 %, for all six premium
  forms (reproduced in §11 below).

### S2 — Mutex / Harmonie Mutuelle, "NÉOBSIA CAPITAL OBSÈQUES — tableaux comparatifs des cotisations et des valeurs de rachat" (18/08/2025)
- Publisher: Mutex SA; document ref "2560394 - Pôle PAO Mutex - 08/2025"
- Doc type: CCSF standardised examples table, 12 pp.
- URL: https://www.harmonie-mutuelle.fr/sites/default/files/pdf/Tableaux_comparatifs_Neobsia_HM_18-08-2025.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: standardised tables for 5 000 € capital at entry ages 50, 60, 70. In the
  Harmonie-Mutuelle distribution the *viager* and *prime unique* columns are marked **NA** — only
  temporary premiums over 5/10/15/20/25 years are sold. Revalorisation clause: "revalorisation
  annuelle du capital obsèques, via le versement de la participation aux bénéfices", plus the
  post-mortem revalorisation described in S1.

### S3 — Mutex, "NÉOBSIA PRESTATIONS OBSÈQUES — tableaux comparatifs" (01/07/2025)
- Publisher: Mutex SA
- Doc type: CCSF standardised examples table for the *prestations* (services) form, 6 pp.
- URL: https://www.mutex.fr/app/uploads/2025/06/tableaux-neobsia_prestations.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the services variant of the same whole-life chassis. Three service packages, each tied
  to a guaranteed capital: **Essentielle 3 500 €, Exigence 4 500 €, Sérénité 6 000 €**. The
  partner operator is La Maison des Obsèques (LMO); a footnote states that the insured keeps free
  choice of funeral operator until the contract is settled, even where an operator is named in the
  contract. Premiums at entry age 50 for a 5 000 € capital are **identical** to the capital-form
  table S2 (356 / 405 / 494 / 678 / 1 240 € for 25/20/15/10/5-year terms) — evidence that the
  services form is the same tariff with the capital earmarked to a service list.

### S4 — CNP Assurances, "Contrats obsèques garantis par CNP Assurances : tableaux comparatifs des cotisations et des valeurs de rachat" (index page)
- Publisher: CNP Assurances
- Doc type: Regulated-information index page
- URL: https://www.cnp.fr/particuliers/info-reglementee/contrats-obseques-garantis-par-cnp-assurances-tableaux-comparatifs-des-cotisations-et-des-valeurs-de-rachat
- Retrieved: YES (page fetched twice; second fetch used to enumerate the PDF links).
- Content: lists the three funeral contracts CNP publishes standardised tables for — Plurio
  Solutions Obsèques Mgéfi n° MI-12-001 [S7], Trésor Prévoyance Garantie Obsèques 2 via Amétis
  [S5], Solution Obsèques de La Banque Postale [S6] — with their PDF URLs.

### S5 — CNP Assurances, "Trésor Prévoyance Garantie Obsèques 2 — tableaux comparatifs" (01/01/2026)
- Publisher: CNP Assurances SA (Issy-les-Moulineaux, 341 737 062 RCS Nanterre)
- Doc type: CCSF standardised examples table, 6 pp.
- URL: https://www.cnp.fr/media/fichiers/particuliers/operations-et-infos-reglementees/tableaux-comparatifs-contrats-obseques/tresor-prevoyance-garantie-obseques-2-ametis
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the **most complete public rate card retrieved** — seven premium forms (viager,
  temporary 25/20/15/10/5 years, and *prime unique*) × three entry ages × 5 000 € capital, with
  cumulative premiums by age at death and surrender values by duration. Explicit revalorisation
  clause: premiums are fixed at inception and are **never indexed or revalued**. Surrender values
  are shown "sans participation aux bénéfices". Footnote: 5 000 € was chosen "car il est proche du
  coût moyen des obsèques en France hors marbrerie" (close to the average cost of a funeral in
  France excluding monumental masonry). Full figures in §7 and §11.

### S6 — CNP Assurances Prévoyance / La Banque Postale, "Solution Obsèques de La Banque Postale — tableaux comparatifs" (12/11/2025)
- Publisher: CNP Assurances Prévoyance, distributed by La Banque Postale
- Doc type: CCSF standardised examples table, 6 pp.
- URL: https://www.cnp.fr/media/fichiers/particuliers/operations-et-infos-reglementees/tableaux-comparatifs-contrats-obseques/solution-obseques-de-la-banque-postale
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: four premium forms only — viager, temporary 15 years, temporary 10 years, prime unique.
  Same "no indexation of premiums" clause as S5. Assistance guarantees included in the premium,
  with a chargeable "Service Assistance Plus" option outside the quoted premium. In the age-60
  table the cumulative lifetime premium is the same at age 90 and at age 95 (9 400 €), which
  implies lifetime premiums cease at about age 90 — see §6 and the caveat in the Gaps section.

### S7 — CNP Assurances / Mgéfi, "PLURIO Solutions Obsèques Mgéfi n° MI-12-001 — tableaux comparatifs" (26/10/2023)
- Publisher: CNP Assurances, group contract of La Mutuelle Générale de l'Économie, des Finances et
  de l'Industrie (Mgéfi)
- Doc type: CCSF standardised examples table, 6 pp.
- URL: https://www.cnp.fr/media/fichiers/particuliers/operations-et-infos-reglementees/tableaux-comparatifs-contrats-obseques/plurio-solutions-obseques-mgefi-mi-12-001
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: three premium forms (viager, temporary 15, temporary 10). Premiums include the
  assistance guarantee. Same "premiums fixed at inception, no indexation" clause. Dated 26/10/2023,
  i.e. predating the CCSF commitments but already in the standardised format.

### S8 — VIASANTÉ Mutuelle / UCR, "Notice d'information — SÉRÉNITÉ OBSÈQUES" (Notice V3.1)
- Publisher: VIASANTÉ Mutuelle (Livre II du Code de la mutualité, SIREN 777 927 120); distributed
  and administered by UCR (courtier, Orias 07 000 616); group contract subscribed by the
  Association pour le Développement de la Prévoyance Mutualiste (ADPM)
- Doc type: Notice d'information, 8 pp. plus an annexe of surrender values
- URL: https://ucr.fr/wp-content/uploads/2025/11/Notice-Serenite-Obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: a *mutualité*-code funeral contract, useful precisely because it states its technical
  basis. Capital chosen from nine options 2 000 / 3 000 / … / 10 000 €. Aggregate cap 10 000 € per
  member, or 20 000 € where death follows an accident from the second membership year. Entry ages
  are **premium-form dependent**: 10-year temporary under 80, 15-year under 75, 20-year under 70,
  25-year under 65, lifetime from 40 to under 86; no *prime unique* is offered. One-year *délai de
  carence*: accidental death pays the full capital from inception; non-accidental death in year 1
  refunds the premiums (excluding the assistance premium) to the estate. From year 2, accidental
  death pays **double** the chosen capital. Charges: acquisition max 10 % of the annual premium
  (10,3 % for lifetime premiums) and in any case not more than 2,5 % of the guaranteed capital per
  art. L. 223-20-1 du Code de la mutualité; administration of premium collection max 20 % of the
  annual premium; ongoing charges max 0,4 % p.a. of the guaranteed capital plus 3,3 % p.a. of the
  annual premium; a 5 % charge is levied inside the mathematical provision during the first eight
  years; assistance premium 12 € p.a. Surrender allowed once one annual premium has been paid,
  total surrender only, equal to the mathematical provision, paid within 30 days, with a **5 %
  penalty if surrender occurs in the first ten years**. Réduction available at any time after one
  annual premium; automatic surrender if the reduced capital falls below 50 % of the SMIC.
  Post-mortem revalorisation under art. L. 223-19-1 du Code de la mutualité at the lesser of the
  12-month average TME and the last TME at 1 November of the previous year; payment within one
  month of receiving documents (L. 223-22-1), then legal interest doubled for two months and
  tripled thereafter. **Technical basis stated explicitly: surrender values are computed on table
  TH 00-02 with a technical rate of 0,75 %.** Long exclusion list (suicide year 1, murder by a
  beneficiary, war, nuclear, professional sport, listed amateur sports, motor competition, driving
  without a licence, unlicensed flying, narcotics, drink-driving) — in an excluded case the
  beneficiaries receive the surrender value, or the premiums collected net of tax if the capital
  exceeds it. 30-day renonciation. Annexe 1 gives a full surrender-value / cumulative-premium grid
  per 1 000 € capital by entry age, from age 40 upward, for lifetime premiums.

### S9 — Macif Santé Prévoyance, "Garantie Obsèques — Note d'information détaillée" (U 821 - UNI/PREI/G OBS/05 - 07/26)
- Publisher: Macif Santé Prévoyance (Livre II du Code de la mutualité, SIREN 779 558 501);
  assistance by IMA Assurances
- Doc type: Note d'information détaillée, 20 pp., "garanties en vigueur au 1er juillet 2026"
- URL: https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_prevoyance/NID_garantie_obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: group contract with optional membership. Capital formula 2 000 € or 3 000 €;
  complementary capitals in 500 € tranches on top of the 3 000 € formula up to 13 000 €. Entry
  age 18–80 inclusive, no medical formality. One-year *délai d'attente* for death by illness with
  refund of premiums (net of instalment charges); suicide excluded for 12 months with the
  mathematical provision refunded. Premium options: 5 years, 10 years, until age 80, or lifetime.
  Charges expressed as a percentage of the capital guaranteed at subscription: max **5,38 %** for
  the "Capital" formula and **4,89 %** for complementary capitals (annual percentage over the
  average contract duration); no ongoing charges, no exit charges, instalment charges only.
  Participation aux bénéfices feeds a *fonds de revalorisation*; the insurer sets an annual
  revalorisation rate for the guarantees within the limits of that fund, applied to each contract's
  mathematical provision on 1 April of the following year, and **the revalorisation is accompanied
  by an increase in the remaining premiums at the same rate**. Annexe C sets out the full PB
  mechanics (technical account, PB account, revalorisation fund) including a own-funds allocation
  equal to 10 % of the technical-account surplus plus 15 % of the excess net investment income
  after technical interest. Non-payment: 10 days then a 40-day formal-notice period, then either
  termination (if surrender value is nil or insufficient) or réduction; the insurer may substitute
  surrender for réduction under art. L. 223-22 du Code de la mutualité. Surrender is total only,
  equal to the mathematical provision, paid within 2 months. Annexe B gives two worked
  surrender-value grids for the first eight years (age 50 / capital 3 800 € and age 55 / capital
  4 580 €, each for two premium forms). Taxation: arts. 757 B and 990 I CGI, social levies.

### S10 — Macif, "GARANTIE OBSÈQUES — tableaux comparatifs" (01/01/2026)
- Publisher: Macif Santé Prévoyance
- Doc type: CCSF standardised examples table, 6 pp.
- URL: https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_prevoyance/tableaux-comparatifs-garantie-obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: four premium forms — viager, "jusqu'à 80 ans", temporary 10 years, temporary 5 years —
  at ages 50/60/70 for 5 000 €. Revalorisation footnote restates the fonds-de-revalorisation
  mechanism and the matching uprating of remaining premiums. Full figures in §7 and §11.

### S11 — Macif Santé Prévoyance, "Garantie Obsèques — Document d'informations clés" (DIC / PRIIPs KID, 1er juillet 2026)
- Publisher: Macif Santé Prévoyance
- Doc type: PRIIPs key information document, 3 pp., ref "DIC Garantie Obsèques - 07/26"
- URL: https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_prevoyance/DIC_garantie_obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: risk class **2 of 7** on a 30-year holding; explicit warning that total premiums may
  exceed the capital paid on death; FGAP cover limited to **70 000 €** in aggregate per insured
  across capital contracts. Performance scenario for entry age 60, capital 3 000 €, premiums to
  age 80: cumulative premiums 247,60 € / 3 714,50 € / 4 952,60 € at 1, 15 and 30 years; surrender
  values 138,13 € / 2 080,06 € / 2 943,16 €; death capital without revalorisation 3 000 € at all
  three durations; death capital **with** revalorisation 3 038,56 € / 3 633,50 € / 4 400,77 €
  (implying a constant illustrative revalorisation rate of 1,2854 % p.a. — derived, see §10).
  Cumulative premiums by premium form and instalment frequency for the same case (annual: 3 779,17 €
  over 5 years, 4 156,34 € over 10 years, 4 952,68 € to age 80, 4 194,18 € lifetime). Footnote:
  the lifetime figure is computed over **the life expectancy of a 60-year-old man on table
  TH 00-02**. Costs: total 75 € / 1 120 € / 1 493 € at 1 / 15 / 30 years; reduction in yield
  24,08 % / 4,86 % / **1,77 %** p.a.; the whole 1,77 % is classified as an entry cost, with zero
  ongoing, exit, transaction and performance costs. Recommended holding period: lifetime.
  Renonciation 30 calendar days.

### S12 — Macif Santé Prévoyance, "Garantie Obsèques — Synthèse" (garanties en vigueur au 1er juillet 2026)
- Publisher: Macif Santé Prévoyance
- Doc type: Contract synthesis / pre-contractual summary, 9 pp.
- URL: https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_prevoyance/synthese_garantie_obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: confirms entry ages 18–80 inclusive by *différence de millésime*, no medical formality,
  residence conditions, and gives the aggregate cap: **total whole-life death guarantees for one
  insured with this insurer may not exceed 17 580 €**. Restates the exclusions (murder by a
  beneficiary, nuclear, war, participation in a crime, suicide within 12 months) and the sums paid
  in each excluded case (mathematical provision). Sets out the default beneficiary clause, the
  obligation to append "à charge pour ce ou ces bénéficiaires de financer les obsèques … à
  concurrence de leur coût et dans la limite du capital garanti" to a named designation, and the
  procedure for changing the designated funeral operator at any time.

### S13 — Macif Santé Prévoyance, "Assurance Obsèques — Document d'information sur le produit d'assurance (DIPA)" (01/26)
- Publisher: Macif Santé Prévoyance
- Doc type: IPID (insurance product information document), 2 pp.
- URL: https://www.macif.fr/files/live/sites/maciffr/files/dipa/DIPA_garantie_obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the clearest statement retrieved of the **two contract forms sold side by side under one
  product**: two *prestations* formulas equivalent to a capital of **3 800 €** and **4 580 €** (the
  second with an ecological-prestations variant), organised and delivered by a *pompes funèbres
  conventionnée*; and a *capital* formula paying **2 000 € or 3 000 €** to the designated
  beneficiaries. Complementary capitals in 500 € tranches up to 13 000 € are available on every
  formula except the 2 000 € capital. Subscription without medical formality; one-year waiting
  period for death by illness; overseas stays limited to 12 continuous months.

### S14 — AXA France, "Tableaux des exemples normalisés — Serenova" (6 juin 2025, réf 2007517 08 2025)
- Publisher: AXA France Vie / AXA Assurances Vie Mutuelle; assistance by Inter Partner Assistance;
  association ANPERE named on the document
- Doc type: CCSF standardised examples table, 3 pp.
- URL: https://media.axa.fr/content/dam/axa-fr/image/particuliers/sante/document-pdf/pdf-tableau-serenova-2025-v2.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: three premium forms (viager, temporary 20 years, temporary 10 years) at ages 50/60/70
  for 5 000 €. **Unique among the retrieved documents in carrying a contractually guaranteed
  uprating: "le contrat prévoit une revalorisation annuelle de 1 % du capital souscrit sans
  augmentation de la cotisation."** Entry for the 20-year premium term is limited to age 69. A
  "couple" discount exists but is excluded from the quoted premiums. Surrender values exceed
  5 000 € at long durations, consistent with the 1 % capital uprating.

### S15 — SOGECAP, "CONTRAT GARANTIE OBSEQUES formule BUDGET — tableau CCSF" (01/07/2025)
- Publisher: SOGECAP SA (086 380 730 RCS Nanterre), Société Générale Assurances
- Doc type: CCSF standardised examples table, 3 pp.
- URL: https://www.assurances.societegenerale.com/fileadmin/2025/tableau_CCSF_BUDGET.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: four premium forms (viager, temporary 10, temporary 5, prime unique) at ages 50/60/70.
  Revalorisation clause: "chaque année, le capital garanti peut être majoré de la participation aux
  résultats prévue au contrat" — discretionary, not guaranteed. The tables run to attained age 115
  for the age-70 case and show lifetime premiums continuing throughout, with cumulative lifetime
  premiums reaching 24 019 € against a 5 000 € capital. Surrender values converge to exactly
  5 000 € at the longest durations.

### S16 — BPCE Vie, "SECUR' OBSEQUES — tableaux comparatifs des cotisations et valeurs de rachat" (juillet 2025)
- Publisher: BPCE Vie SA (349 004 341 RCS Paris)
- Doc type: CCSF standardised examples table, 3 pp.
- URL: https://dda.assurances.groupebpce.com/pdfs/tableaux_comparatifs_des_cotisations_et_valeurs_de_rachat_secur_obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: **only two premium forms — temporary 5 years and temporary 10 years**; no lifetime and
  no single premium. Carries the most explicit PB formula retrieved: "cette participation correspond
  à 90 % des bénéfices techniques et financiers, déduction faite d'un taux de prélèvement de gestion
  sur encours égal à 1 % et du taux d'intérêt technique garanti à l'adhésion, visé à l'article
  A 335-1 du Code des assurances", allocated to the mathematical provision so that **the guaranteed
  capital rises while premiums stay unchanged**. Surrender values reach exactly 5 000 € at the end
  of the premium term.

### S17 — Malakoff Humanis, "Contrat obsèques — Note d'information valant conditions générales" (MH-12934-2004-2021-012)
- Publisher: Malakoff Humanis
- Doc type: Note d'information valant conditions générales
- URL: https://www.malakoffhumanis.com/sites/smile/files/files/malakoff-humanis-contrat-obseques-note-information-valant%20cg-MH-12934-2004-2021-012.pdf
- Retrieved: NO — HTTP 410 Gone (document withdrawn from the host). Known reference only; nothing
  is cited from it.

### S18 — Auxia (BRED / Prépar), "Prépar'Obsèques — Notice d'informations" (VST3_652_042019-1)
- Publisher: Auxia Assurances
- Doc type: Notice d'information
- URL: https://www.acommeassure.com/cg/OBSEQUES/auxia/CG_PREPAROBSEQUES_V1.pdf
- Retrieved: NO — HTTP 403 Forbidden on both attempts. Known reference only.

### S19 — PFG (OGF), "Comment financer ses obsèques ?"
- Publisher: PFG — Pompes Funèbres Générales (groupe OGF)
- Doc type: Product/guide web page
- URL: http://www.pfg.fr/assurance-obseques/nos-guides-conseils/financer-obseques
  (the https URL https://www.pfg.fr/assurance-obseques/financer-obseques 301-redirects here)
- Retrieved: NO — HTTP 403 Forbidden on both attempts. Known reference only. A search-engine
  snippet describes a PFG capital contract of 1 000 € to 15 000 € revalued annually, with no
  waiting period for a single premium and no waiting period for accidental death where premiums are
  instalments — **[unverified]**, no PFG document was retrieved.

### S20 — Banque Populaire / BPCE Vie, "Assurance obsèques — tableaux comparatifs" (01/07/2025)
- Publisher: BPCE Vie, Banque Populaire distribution
- Doc type: CCSF standardised examples table
- URL: https://www.img.banquepopulaire.fr/app/uploads/sites/5/2025/07/04170155/assurance-obseques-tableaux-comparatifs-01072025.pdf
- Retrieved: NO — not attempted; the same insurer's Secur'Obsèques tables [S16] were used instead.
  Kept as a known reference.

---

## Regulatory and actuarial references

### R1 — Légifrance, Code général des collectivités territoriales, art. L. 2223-33
- Publisher: Direction de l'information légale et administrative (Légifrance)
- URL: https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006192270/
- Retrieved: YES (sub-section page, articles L2223-31 à L2223-34-2).
- Content: "A l'exception des formules de financement d'obsèques, sont interdites les offres de
  services faites en prévision d'obsèques ou pendant un délai de deux mois à compter du décès …".
  This is the article that makes a *formule de financement d'obsèques* (i.e. an insurance contract)
  the only lawful way to pre-arrange and pre-pay a funeral.

### R2 — Légifrance, CGCT art. L. 2223-33-1
- URL: https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006192270/
- Retrieved: YES (same page as R1).
- Content: "Les formules de financement d'obsèques prévoient expressément l'affectation à la
  réalisation des obsèques du souscripteur ou de l'adhérent, à concurrence de leur coût, du capital
  versé au bénéficiaire." This is the earmarking rule every retrieved notice implements through its
  beneficiary clause [S1][S8][S9][S12].

### R3 — Légifrance, CGCT art. L. 2223-34-1 (version en vigueur depuis le 28 juillet 2013)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000027783339
- Retrieved: YES (article page with legislative history).
- Content, verbatim: "Toute clause d'un contrat prévoyant des prestations d'obsèques à l'avance
  sans que le contenu détaillé et personnalisé de ces prestations soit défini est réputée non
  écrite. / Tout contrat prévoyant des prestations d'obsèques à l'avance précise les conditions
  d'affectation des bénéfices techniques et financiers, conformément à l'article L. 132-5 du code
  des assurances. Il lui est affecté chaque année, lorsqu'il est positif, un montant correspondant
  à une quote-part du solde créditeur du compte financier, au moins égale à 85 % de ce solde
  multiplié par le rapport entre les provisions mathématiques relatives à ce contrat et le total
  des provisions mathématiques, diminuée des intérêts crédités aux provisions mathématiques
  relatives à ce même contrat au cours de l'exercice. Il fait aussi l'objet d'une information
  annuelle conformément à l'article L. 132-22 du même code. Un arrêté précise les modalités de
  calcul et d'affectation de cette quote-part." Legislative history on the page: **modified by
  LOI n° 2013-672 du 26 juillet 2013, arts. 73 and 74**. The article was originally inserted by
  loi n° 2004-1343 du 9 décembre 2004 [R21] and amended by loi n° 2008-1350 art. 8 [R6]. Note that
  the mandatory 85 % PB floor is drafted for *contrats prévoyant des prestations d'obsèques à
  l'avance* — i.e. the **prestations form**; whether it reaches a pure capital contract is not
  settled by the text retrieved.
- Note: the sub-section listing page (R1/R2 URL) returns only the first paragraph of this article;
  the article page above returns the full text.

### R4 — Légifrance, CGCT art. L. 2223-34-2 (version du 14 mai 2009)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000020625551/2026-08-25
- Retrieved: YES.
- Content: creates a national file centralising *contrats prévoyant des prestations d'obsèques à
  l'avance* taken out with insurers under art. L. 310-1 CA and mutuelles under art. L. 111-1 du
  Code de la mutualité; implementing rules by décret en Conseil d'État after CNIL opinion. Created
  by **LOI n° 2009-526 du 12 mai 2009, art. 25** (not by the loi Sueur, which had enacted an
  earlier version of the same idea — see R6).

### R5 — Légifrance, CGCT art. L. 2223-35-1 (en vigueur depuis le 16 décembre 2005)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006390319
- Retrieved: YES (article page with legislative history).
- Content: the freedom-of-modification rule. The contract must explicitly provide the subscriber
  with the ability, throughout life, to change the nature of the funeral, the mode of burial, the
  content of the services and supplies, the designated authorised operator and, where applicable,
  the mandatary appointed to see the wishes carried out; changes at equivalent services and
  supplies may attract only the management charges set out in the general conditions; breach — or
  offering a contract that omits the faculty — carries a fine of **15 000 € per infringement**.
  Legislative history on the page: **created by LOI n° 2005-1564 du 15 décembre 2005, art. 15 (V)**
  — note this contradicts the widely circulated attribution to loi n° 2004-1343 (see R21 and the
  Gaps section).

### R6 — Légifrance, LOI n° 2008-1350 du 19 décembre 2008 relative à la législation funéraire ("loi Sueur")
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000019960926
- Retrieved: YES (JORF consolidated text).
- Content: art. 7 amends L. 2223-33 (advance offers of service prohibited except *formules de
  financement d'obsèques*); **art. 8 adds to L. 2223-34-1: "Le capital versé par le souscripteur
  d'un contrat prévoyant des prestations d'obsèques à l'avance produit intérêt à un taux au moins
  égal au taux légal."**; art. 9 creates L. 2223-34-2 (national file, later re-enacted — see R4).
  The retrieved text does **not** contain the "contenu détaillé et personnalisé" wording or the
  modification faculty; those come from the 2004 and 2005 statutes respectively [R3][R5][R21].

### R7 — Légifrance, Code des assurances, Section I "Dispositions générales" (arts. L. 132-1 à L. 132-27-2)
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000006174038/
- Retrieved: YES (fetched twice; the second fetch returned full text for L. 132-13 and L. 132-20).
- Content: art. **L. 132-1** — "La vie d'une personne peut être assurée par elle-même ou par un
  tiers …", the enabling article for whole-life assurance on one's own head, which is the legal
  form of every capital-form funeral contract retrieved [S1][S8][S9]. Art. **L. 132-3** — prohibition
  of death cover on the head of a child under twelve, an adult under *tutelle*, or a person in
  psychiatric hospitalisation; premiums must be refunded in full. Art. **L. 132-5-1** — 30-day
  renonciation right. Art. **L. 132-13**, verbatim: "Le capital ou la rente payables au décès du
  contractant à un bénéficiaire déterminé ne sont soumis ni aux règles du rapport à succession, ni
  à celles de la réduction pour atteinte à la réserve des héritiers du contractant. / Ces règles ne
  s'appliquent pas non plus aux sommes versées par le contractant à titre de primes, à moins que
  celles-ci n'aient été **manifestement exagérées eu égard à ses facultés**." Art. **L. 132-20**,
  verbatim: the insurer has no action to compel premium payment; on non-payment within ten days of
  the due date, a registered letter starts a forty-day period at whose expiry non-payment triggers
  either termination (where the surrender value is non-existent or insufficient) or *réduction* of
  the contract.

### R8 — Légifrance, Code des assurances art. L. 132-5 (version du 1er janvier 2016)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006792939
- Retrieved: YES (full verbatim text).
- Content: the life contract must contain clauses defining the object of the contract and the
  parties' obligations; **"Le contrat précise les conditions d'affectation des bénéfices techniques
  et financiers"** (the hook art. L. 2223-34-1 CGCT hangs the funeral-contract PB rule on); and the
  contract must state the conditions under which, on death, the guaranteed capital is revalued from
  the date of death until receipt of the documents listed in art. L. 132-23-1 or deposit at the
  Caisse des dépôts under art. L. 132-27-2, with charges after the date of knowledge of death
  capped by decree and no charge for the insurer's search-and-inform obligations. The final
  paragraph sets a floor rate for that post-mortem revalorisation, fixed by décret en Conseil
  d'État — the rate the notices restate as the lesser of the 12-month average TME and the last TME
  at 1 November of the previous year [S1][S8].

### R9 — Légifrance, Code des assurances art. L. 132-22 (version du 24 octobre 2024)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006793125
- Retrieved: YES (key provisions quoted; long article, only the material paragraphs returned).
- Content: annual communication to the policyholder of the surrender (or transfer) value, the
  guaranteed return and the technical and financial profit sharing on the contract; a specific
  statement one month before any term date; and annual website publication of guaranteed returns,
  average charges and average net returns within 90 business days after 31 December. Last modified
  by loi n° 2023-973 du 23 octobre 2023 art. 35 (V). This is the article cross-referenced by
  art. L. 2223-34-1 CGCT [R3] and implemented by the annual statements described in [S1][S8].

### R10 — Légifrance, Code des assurances art. L. 132-23 (version du 14 juin 2026)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006793141
- Retrieved: YES (full verbatim text).
- Content: first paragraph — *assurances temporaires en cas de décès* and immediate or in-payment
  life annuities may carry **neither réduction nor rachat**; survivorship capital/annuity contracts
  and pure endowments and deferred annuities without return of premium may carry no rachat. Last
  paragraphs — "Pour les autres assurances sur la vie … l'assureur ne peut refuser la réduction ou
  le rachat", and "L'assureur peut d'office substituer le rachat à la réduction si la valeur de
  rachat est inférieure à un montant fixé par décret." Whole-life funeral contracts fall in the
  "autres assurances sur la vie" bucket, which is why every retrieved capital contract carries both
  a surrender and a paid-up value [S1][S8][S9][S11].

### R11 — Comité consultatif du secteur financier (CCSF), "Avis du 8 octobre 2024 — Les contrats d'assurance obsèques"
- Publisher: CCSF, hosted by Banque de France
- URL: https://www.banque-france.fr/system/files/import/ccsf/ccsf_avis_contrats_obseques.pdf
  (also served with the query string `?v=1738946978`)
- Retrieved: **NO — HTTP 403 Forbidden on three attempts** (both URL forms). Known reference only;
  its content is described here only through the secondary summaries R13–R16, and every such
  statement is tagged [unverified].

### R12 — CCSF, "Communiqué de presse — Avis du CCSF" (Paris, 15 octobre 2024)
- Publisher: CCSF / Banque de France
- URL: https://www.banque-france.fr/system/files/import/ccsf/medias/documents/ccsf_avis_contrats_obseques_cp.pdf
- Retrieved: NO — HTTP 403 Forbidden. Known reference only.

### R13 — MoneyVox, "Assurance obsèques : ce qui va changer en juillet pour votre contrat"
- Publisher: MoneyVox (financial news site) — **secondary source**
- URL: https://www.moneyvox.fr/assurance/actualites/104034/assurance-obseques-ce-qui-va-changer-en-juillet-pour-votre-contrat
- Retrieved: YES.
- Content: summary of the CCSF avis. Standardised table for entry ages 50/60/70 and a 5 000 €
  guaranteed capital, showing cumulative premiums for deaths between ages 65 and 95 and surrender
  values; premium forms named as *viager*, *temporaire* (25/20/15/10/5 years) and *unique*.
  Commitments effective **1 July 2025**: cap the *délai de carence* at **one year maximum**
  (previously up to two years); systematically offer temporary alternatives alongside lifetime
  premiums; limit contractual exclusion clauses; state explicitly the surrender value payable when
  death falls within an exclusion; make the tables downloadable. First effectiveness review July
  2026. The avis is non-binding. All of this is [unverified] against the avis itself.

### R14 — La finance pour tous, "Assurances obsèques : une amélioration des pratiques attendue pour juillet 2025" (31 October 2024)
- Publisher: IEFP — La finance pour tous — **secondary source**
- URL: https://www.lafinancepourtous.com/2024/10/31/assurances-obseques-une-amelioration-des-pratiques-attendue-pour-juillet-2025/
- Retrieved: YES.
- Content: market figures attributed to the CCSF avis — **more than 5,3 million contracts in force
  in 2023, a portfolio of 1,8 bn €, about 190 000 deaths covered a year (≈30 % of deaths in
  France), average capital about 5 000 €**. Two contract structures (capital and prestations);
  three premium modes (single, temporary, lifetime). Commitments as in R13. All figures
  [unverified] against the avis itself.

### R15 — Planète CSCA, "Le CCSF adopte un avis pour une meilleure lisibilité et un renforcement des garanties des contrats d'assurance obsèques"
- Publisher: Planète CSCA (brokers' federation) — **secondary source**
- URL: https://www.planetecsca.fr/actualites/pratiques-du-metier/le-ccsf-adopte-un-avis-pour-une-meilleure-lisibilite-et-un-renforcement-des-garanties-des-contrats-dassurance-obseques/
- Retrieved: YES.
- Content: gives the market as **1,8 bn € of premiums and 539 000 new policies in 2023**;
  describes the standardised table contents (cumulative premiums by entry age 50/60/70, surrender
  value at the end of the premium-paying period, downloadable from distributors' websites); repeats
  the one-year *délai de carence* cap, the obligation to offer non-lifetime alternatives, the
  limitation of exclusions and the surrender-value disclosure; deadline 1 July 2025, assessment one
  year later. [unverified] against the avis itself.

### R16 — Institut national de la consommation (INC), "Contrats d'assurance obsèques : pour une meilleure lisibilité et un renforcement des garanties"
- Publisher: INC — **secondary source**
- URL: https://www.inc-conso.fr/content/assurance/contrats-dassurance-obseques-pour-une-meilleure-lisibilite-et-un-renforcement-des-garanties
- Retrieved: YES, but thin.
- Content: confirms the scope of the CCSF work — individual contracts and group contracts with
  individual membership, based on a **whole-life guarantee, excluding savings contracts and
  fixed-term guarantee contracts** — and the finding of "un manque de lisibilité globale des
  informations précontractuelles". Implementation by 1 July 2025, review one year later. No
  figures.

### R17 — service-public.gouv.fr, "Qui doit payer les frais d'obsèques ?" (fiche F17059, vérifiée le 1er janvier 2026)
- Publisher: DILA
- URL: https://www.service-public.gouv.fr/particuliers/vosdroits/F17059
- Retrieved: YES.
- Content: up to **5 965 €** may be drawn from the deceased's bank account to pay funeral costs,
  within the available balance, under art. **L. 312-1-4 du Code monétaire et financier**; funeral
  expenses are deductible from the estate up to **1 500 €** (monument and flowers excluded). The
  *contrat obsèques* is described as a *prévoyance* contract, not a savings product, paying a fixed
  capital against premiums, and specifying both the capital and the actual funeral services;
  premium options are listed as single payment, temporary premiums (5–10 years) or lifetime
  premiums.

### R18 — service-public.gouv.fr, "Assurance-vie et assurance décès : comment les distinguer ?" (fiche F35395)
- Publisher: DILA
- URL: https://www.service-public.gouv.fr/particuliers/vosdroits/F35395
- Retrieved: YES.
- Content: distinguishes *assurance-vie* (savings) from *assurance décès* (risk cover paying a fixed
  capital), and notes that funeral insurance is confined to covering the formalities and costs of a
  funeral. The page contains **no** tax thresholds and **no** reference to art. 990 I or 757 B CGI.

### R19 — service-public.gouv.fr, "Demander la recherche d'un contrat d'assurance obsèques" (service R63577)
- Publisher: DILA / AGIRA
- URL: https://www.service-public.gouv.fr/particuliers/vosdroits/R63577
- Retrieved: YES.
- Content: AGIRA operates an online request service (formulaireobseques.agira.asso.fr) for locating
  a deceased person's funeral insurance contract; a death certificate must be supplied; insurers
  respond within a maximum of **3 business days** of AGIRA receiving the request. This is the
  operational counterpart of the national file created by art. L. 2223-34-2 CGCT [R4].

### R20 — service-public.gouv.fr, "Obsèques : une notice d'information obligatoire pour mieux accompagner les familles" (actualité A19044)
- Publisher: DILA
- URL: https://www.service-public.gouv.fr/particuliers/actualites/A19044
- Retrieved: YES.
- Content: **décret n° 2026-770 du 13 août 2026** and an **arrêté du 13 août 2026** (art. R. 2223-24-1
  CGCT), both published in the Journal officiel of 14 August 2026, oblige every funeral operator to
  hand families a standardised, neutral information notice (free and non-binding quotations, the
  freedom to choose the funeral company, mandatory versus optional services, coffin and transport
  rules, ash dispersal, dispute routes). Applicable from **1 October 2026**. This bears on the
  *prestations* form and on the funeral-cost benchmark, not on the insurance mechanics.

### R21 — AFIF (Association française d'information funéraire), "La souscription d'un contrat de prévoyance décès obsèques — explications et conseils"
- Publisher: AFIF, association loi 1901 — **consumer body, secondary for legal text**
- URL: https://www.afif.asso.fr/francais/conseils/prevoyance.obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted, 11 pp.).
- Content: sets out the two contract categories exactly as the model needs them — (1) *contrat de
  prestations d'obsèques à l'avance*, where an insurer and a named funeral firm jointly guarantee
  the execution of a specified quotation, and (2) *contrat de capital ou d'épargne en prévision
  d'obsèques*, where the funeral firm merely introduces the subscriber to an insurer and the
  capital is paid to the firm up to the amount available. Lists the general life-insurance settlement
  forms: *prime unique*, *primes périodiques viagères*, *primes périodiques durant une période
  déterminée*. Warns that for lifetime premiums "la somme totale des prélèvements en viager pourra
  être équivalente à plusieurs fois le prix des obsèques". Describes the *délai de carence* as a
  period during which death by illness produces only a refund of the premiums paid, and states it
  does not apply to accidental death, with the standard market definition of accident excluding
  myocardial infarction, coronary and cardio-vascular conditions and emotional shock. Quotes
  **loi n° 2004-1343 du 9 décembre 2004** (JO n° 287 of 10 December 2004) as inserting CGCT
  art. L. 2223-34-1 ("… sans que le contenu détaillé de ces prestations soit défini est réputée non
  écrite") **and** art. L. 2223-35-1 (freedom to modify, 15 000 € fine) — note the attribution of
  L. 2223-35-1 conflicts with Légifrance's own legislative history [R5]. Also: 30-day renonciation
  under art. L. 132-5-1 CA, extended where the general conditions were not handed over (Cass. 2e
  civ., 8 March 2006, pourvoi n° 05-10324); three clauses struck down as abusive by TGI Paris on
  9 October 2006 (compulsory direct debit; unilateral modification by the operator; retention of
  5 % of premiums where the chosen operator does not perform); the prohibition since the décret
  n° 95-653 du 9 mai 1995 on a funeral operator holding client money in advance (art. L. 2223-20
  CGCT); and the registration obligation for funeral firms selling insurance under the loi du
  15 décembre 2005 and its décrets of 30 August 2006.

### R22 — Boursorama, "Quel est le coût moyen des obsèques et comment le réduire ?" (16 October 2025)
- Publisher: Boursorama, reporting a study by the Silver Alliance grouping — **secondary source**
- URL: https://www.boursorama.com/budget/actualites/quel-est-le-cout-moyen-des-obseques-et-comment-le-reduire-97ff12aed4ecf90a41dedadec558e76d
- Retrieved: YES.
- Content: average French funeral cost **4 730 € in 2025** (Silver Alliance study published late
  2024); **5 044 € for an inhumation, 4 434 € for a crémation**; higher in Normandie, Île-de-France
  and Pays de la Loire, lower in Occitanie, PACA and Nouvelle-Aquitaine. The primary study itself
  was not retrieved.

### R23 — Légifrance, Code de la mutualité (table of contents only)
- URL: https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006074067
- Retrieved: PARTIAL — the code's landing page loads and confirms the code identity, but the
  individual articles cited by the *mutualité*-code contracts were **not** retrieved:
  **L. 223-19-1** (post-mortem revalorisation), **L. 223-20-1** (cap on acquisition charges for
  *formules de financement d'obsèques* — quoted by S8 as 2,5 % of the guaranteed capital),
  **L. 223-22** and **L. 223-22-1** (réduction; one-month payment deadline), **L. 223-25-4**
  (deposit at the Caisse des dépôts), **L. 223-8** and **L. 221-18** (renonciation), **R. 223-9**
  (minimum post-mortem revalorisation rate). Everything attributed to these articles below rests on
  the insurer notices [S8][S9] and the article texts themselves are [unverified].

### R24 — Légifrance, Code général des impôts (table of contents only)
- URL: https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006069577
- Retrieved: PARTIAL — the code's landing page loads (dated 25 August 2026) but **arts. 990 I,
  757 B and 125-0 A were not retrieved**: the intermediate table-of-contents page exceeded the
  fetcher's 10 MB content limit and the search interface is JavaScript-rendered. The *applicability*
  of arts. 990 I and 757 B to these contracts is verified from four primary documents
  [S1][S9][S11][S13]; the numerical thresholds and rates are **[unverified]** here.

### R25 — Éditions Législatives, "À l'aube de la fête des défunts, le CCSF fait leur fête aux contrats d'assurance obsèques !"
- Publisher: Éditions Législatives — secondary
- URL: https://www.editions-legislatives.fr/actualite/a-laube-de-la-fete-des-defunts-le-ccsf-fait-leur-fete-aux-contrats-dassurance-obseques%C2%A0/
- Retrieved: NO — the host returned a "Request Rejected" page to the automated fetch. Known
  reference only.

---

## Extracted specifications

### 1. Product structure and legal form
- The capital-form *contrat obsèques* is an **individual whole-life assurance (assurance vie
  entière)** on the subscriber's own head, written under the Code des assurances (branche 20
  Vie-Décès) or, for mutuelles, under Livre II du Code de la mutualité [S1 art. 1][S8 arts. 1, 3]
  [S9][S13]. The enabling provision is art. L. 132-1 CA — a person's life may be insured by
  themselves or by a third party [R7].
- Subscriber and insured are the **same person** in every retrieved contract [S1 defs][S8 art. 3];
  Macif additionally permits a *sociétaire* to insure a spouse, ascendant or descendant [S9][S12].
- Cover is **lifelong and has no maturity date**: the contract ends only on death, on surrender, or
  on lapse [S1 art. 5.2][S8 art. 6][S9][S11]. There is no survival benefit of any kind. Total
  premiums may exceed the capital — the DIC states this in terms: "Le total des cotisations payées
  pendant toute la durée du contrat peut dépasser le montant du capital qui sera versé en cas de
  décès" [S11].
- The product is sold both as an **individual contract** (Mutex/Harmonie Néobsia [S1]) and as a
  **group contract with optional individual membership** (Macif [S9][S12], VIASANTÉ/UCR through the
  ADPM association [S8], Mgéfi [S7]). The CCSF work covered both [R16].
- Classification for the model: a non-linked, participating whole-life death benefit with level
  premiums, guaranteed-issue underwriting and a contractual waiting period.

### 2. The two forms — *contrat en capital* versus *contrat en prestations*
- **Contrat en capital**: the insurer pays a capital sum on death; the first-rank beneficiary is
  the funeral firm that performed the services (or whoever paid its invoice), up to the amount of
  the invoice and within the guaranteed capital; any balance goes to the freely designated
  beneficiaries [S1 art. 11.1][S8 art. 16][S9][S12]. This is the earmarking that art. L. 2223-33-1
  CGCT requires [R2].
- **Contrat en prestations**: the same whole-life capital, but tied to a defined and personalised
  list of funeral goods and services which a named operator undertakes to deliver [R21][S3][S13].
  Art. L. 2223-34-1 CGCT makes any clause promising advance funeral services **without a detailed
  and personalised description of them "réputée non écrite"** [R3]; art. L. 2223-35-1 CGCT requires
  the contract to let the subscriber change, at any time during life, the nature of the funeral,
  the mode of burial, the content of the services and supplies, the designated operator and any
  mandatary, with only the general conditions' management charges payable for changes at equivalent
  services, on pain of a **15 000 € fine per infringement** [R5].
- Observed prestations pricing, all whole-life:
  - Mutex NÉOBSIA Prestations: **Essentielle 3 500 €, Exigence 4 500 €, Sérénité 6 000 €**, operator
    La Maison des Obsèques, free choice of operator retained [S3].
  - Macif: two prestations formulas **equivalent to a capital of 3 800 € and 4 580 €** (the latter
    with an ecological-prestations version), delivered by a *pompes funèbres conventionnée* [S13].
- The premium tariff is the same object in both forms: Mutex's prestations table reproduces the
  capital table's premiums exactly for a 5 000 € capital at age 50 [S2][S3]. **The model targets
  the capital form**; the prestations form differs only in who receives the money and in the
  contractual service list, not in the cash-flow mechanics.
- Only insurers, mutuelles and institutions de prévoyance may offer *formules de financement
  d'obsèques*; a funeral operator has been barred since the décret n° 95-653 du 9 mai 1995 from
  holding a client's money in advance of death (art. L. 2223-20 CGCT) [R21]. Advance offers of
  funeral services are otherwise prohibited by art. L. 2223-33 CGCT [R1].

### 3. Legal frame — the statutes that shape the contract
| Provision | Effect | Source |
|---|---|---|
| Code des assurances art. L. 132-1 | whole-life assurance on one's own head | [R7] |
| Code des assurances art. L. 132-3 | no death cover on a child under 12, an adult under *tutelle*, or a person in psychiatric hospitalisation; premiums fully refunded | [R7][R21] |
| Code des assurances art. L. 132-5 | contract must state PB allocation conditions and the post-mortem revalorisation rules; floor rate set by decree | [R8] |
| Code des assurances art. L. 132-5-1 | 30-day renonciation | [R7][R21] |
| Code des assurances art. L. 132-13 | death capital outside *rapport à succession* and *réduction*, unless premiums were **manifestement exagérées eu égard aux facultés** of the subscriber | [R7] |
| Code des assurances art. L. 132-20 | 10 days + 40-day formal notice, then termination or *réduction* | [R7] |
| Code des assurances art. L. 132-22 | annual statement of surrender value, guaranteed return and PB | [R9] |
| Code des assurances art. L. 132-23 | whole-life contracts are rachetables and réductibles; insurer may substitute rachat for réduction below a decreed threshold | [R10] |
| CGCT art. L. 2223-33 | advance funeral service offers prohibited except *formules de financement d'obsèques* | [R1] |
| CGCT art. L. 2223-33-1 | the capital must be earmarked to the funeral, up to its cost | [R2] |
| CGCT art. L. 2223-34-1 | detailed and personalised description of prestations, or the clause is void; PB quota of at least 85 % of the credit balance of the financial account, pro-rated by mathematical provisions, less technical interest credited; annual information | [R3][R6] |
| CGCT art. L. 2223-34-2 | national file of advance-prestations contracts (operated as the AGIRA search) | [R4][R19] |
| CGCT art. L. 2223-35-1 | lifelong freedom to modify the funeral, the operator and the service content; 15 000 € fine | [R5] |
| CMF art. L. 312-1-4 | up to 5 965 € (2026) may be drawn from the deceased's account for funeral costs | [R17] |
- **Loi Sueur = loi n° 2008-1350 du 19 décembre 2008** relative à la législation funéraire: art. 7
  amends L. 2223-33; **art. 8 adds the legal-interest floor to L. 2223-34-1**; art. 9 creates the
  national file [R6]. The "detailed description" and "freedom to modify" obligations that the brief
  attributes to the loi Sueur are in fact older: **loi n° 2004-1343 du 9 décembre 2004** inserted
  L. 2223-34-1 [R21], and Légifrance attributes L. 2223-35-1 to **loi n° 2005-1564 du 15 décembre
  2005 art. 15 (V)** [R5], while AFIF attributes it to loi 2004-1343 [R21] — see Gaps.
- The current wording of L. 2223-34-1, including the word *personnalisé* and the whole 85 % PB
  paragraph, comes from **loi n° 2013-672 du 26 juillet 2013, arts. 73–74** [R3].

### 4. Eligibility, entry ages and underwriting
- **No medical questionnaire and no medical examination** — every retrieved contract is
  guaranteed-issue: "Votre contrat est accepté sans aucune sélection médicale" [S1 art. 10];
  "La souscription au contrat s'effectue sans formalité médicale" [S13]; "Aucune formalité médicale
  n'est demandée" [S11][S12]. The waiting period is the anti-selection device that replaces
  underwriting [R21].
- Entry ages actually published:
  | Insurer / product | Minimum | Maximum | Basis | Source |
  |---|---|---|---|---|
  | Mutex NÉOBSIA (capital) | 18 revolus | **84** | *différence de millésime* | [S1 art. 10] |
  | Macif Garantie Obsèques | 18 | **80 inclusive** | *différence de millésime* | [S9][S11][S12] |
  | VIASANTÉ / UCR Sérénité Obsèques — 10-yr temporary | 18 | under **80** | *différence de millésime* | [S8 art. 5] |
  | … 15-yr temporary | 18 | under **75** | | [S8 art. 5] |
  | … 20-yr temporary | 18 | under **70** | | [S8 art. 5] |
  | … 25-yr temporary | 18 | under **65** | | [S8 art. 5] |
  | … lifetime premiums | **40** | under **86** | | [S8 art. 5] |
  | AXA Serenova — 20-yr temporary | not stated | **69** | | [S14 note 12] |
  | CNP / Macif / Sogecap / BPCE / AXA standardised tables | — | tables are published at entry ages **50, 60 and 70** | | [S5][S6][S7][S10][S14][S15][S16] |
- Age is uniformly computed by *différence de millésime* — calendar year of subscription minus
  calendar year of birth [S1][S8][S9]. **This is the age definition the model must use**; it is not
  age last birthday and not age nearest birthday.
- Residence conditions: metropolitan France, Monaco and the four DROM for Mutex [S1 art. 10];
  France including Corsica and the DROM-COM for VIASANTÉ, with a move abroad terminating cover
  [S8 art. 5, art. 19]; France plus stays abroad of no more than 12 continuous months for Macif
  [S11][S12][S13]. VIASANTÉ additionally limits cover abroad to 90 consecutive and 90 non-
  consecutive days in any 12 months [S8 art. 4.3].
- Misstatement of age is corrected by calling the correct premium, and on refusal the contract is
  put into *réduction* [S1 art. 10].

### 5. Capital amounts and caps
- Published ranges for the **capital form**:
  | Insurer / product | Capital range | Aggregate cap | Source |
  |---|---|---|---|
  | Mutex NÉOBSIA | **2 000 – 10 000 €**, free choice | 10 000 € across all Mutex funeral contracts on one head | [S1 arts. 7, 10] |
  | VIASANTÉ / UCR Sérénité | nine steps: **2 000, 3 000, 4 000, 5 000, 6 000, 7 000, 8 000, 9 000, 10 000 €** | 10 000 € per member; 20 000 € where death follows an accident from year 2 | [S8 arts. 4.1, 4.2] |
  | Macif Garantie Obsèques | **2 000 € or 3 000 €** base, plus complementary capitals in **500 €** tranches up to **13 000 €** | **17 580 €** total whole-life death guarantees per insured with this insurer | [S9][S12][S13] |
  | CCSF standardised tables (all insurers) | illustrated at **5 000 €** | — | [S5][S6][S7][S10][S14][S15][S16] |
- The 5 000 € figure is not arbitrary: every standardised table carries the same footnote — 5 000 €
  "a été choisi à titre d'exemple car il est proche du coût moyen des obsèques en France hors
  marbrerie" [S5][S6][S7][S10][S14][S15][S16]. **This is the single best-supported benchmark in the
  file**: seven insurers independently assert it.
- Minimum after a reduction in cover: 2 000 € at Mutex, and the new capital may not be lower than
  the contract's *valeur de réduction* [S1 art. 15.1.2].
- The brief's expected range of 2 000 – 15 000 € is confirmed at the lower end (2 000 €) by three
  insurers, and at the upper end the retrieved caps are 10 000 € (Mutex, VIASANTÉ), 13 000 €
  complementary / 17 580 € aggregate (Macif). A 15 000 € ceiling is attributed to PFG by a
  search-engine snippet only — **[unverified]**, S19 could not be retrieved.

### 6. Premium forms and durations
- Three families, exactly as the brief expects, and every retrieved contract offers at least two of
  them [R14][R17][R21]:
  - **prime unique** — a single payment at inception;
  - **primes temporaires** — a level premium payable for a fixed term, or to a fixed age;
  - **primes viagères** — a level premium payable for life.
- What each insurer actually sells:
  | Insurer / product | unique | 5 yr | 10 yr | 15 yr | 20 yr | 25 yr | to age 80 | viagère | Source |
  |---|---|---|---|---|---|---|---|---|---|
  | Mutex NÉOBSIA (conditions générales) | no | yes | yes | yes | yes | yes | no | yes | [S1 art. 13.1] |
  | Mutex NÉOBSIA (Harmonie distribution tables) | **NA** | yes | yes | yes | yes | yes | no | **NA** | [S2] |
  | CNP Trésor Prévoyance GO 2 | yes | yes | yes | yes | yes | yes | no | yes | [S5] |
  | CNP / La Banque Postale Solution Obsèques | yes | no | yes | yes | no | no | no | yes | [S6] |
  | CNP / Mgéfi PLURIO | no | no | yes | yes | no | no | no | yes | [S7] |
  | VIASANTÉ / UCR Sérénité | no | no | yes | yes | yes | yes | no | yes | [S8 art. 7] |
  | Macif Garantie Obsèques | no | yes | yes | no | no | no | **yes** | yes | [S9][S10] |
  | AXA Serenova | no | no | yes | no | yes | no | no | yes | [S14] |
  | Sogecap formule BUDGET | yes | yes | yes | no | no | no | no | yes | [S15] |
  | BPCE Vie Secur'Obsèques | no | yes | yes | no | no | no | no | no | [S16] |
- The choice is **final at inception** at Mutex ("ce choix effectué à la souscription est
  définitif") [S1 art. 13.1].
- Premiums are annual and payable in advance, with monthly / quarterly / half-yearly instalment
  options; instalment charges apply at Macif and are nil at Mutex [S1 arts. 13.1, 13.4][S8 art. 8]
  [S9]. Monthly instalments force direct debit at VIASANTÉ [S8 art. 8]. The DIC quantifies the
  instalment loading at Macif: for entry age 60, capital 3 000 €, premiums to age 80, cumulative
  premiums are 4 952,68 € annual, 5 007,08 € half-yearly, 5 061,48 € monthly — a **2,2 % uplift
  from annual to monthly** [S11].
- **Do lifetime premiums ever stop?** The retrieved tables disagree, and this matters for the model:
  - Sogecap's tables run lifetime premiums to attained age **115** with no cessation [S15].
  - CNP Trésor Prévoyance runs them to attained age **95** with no cessation shown [S5].
  - La Banque Postale's age-60 table shows the same cumulative lifetime premium at age 90 and at
    age 95 (9 400 € in both columns), which implies **premiums cease at about age 90** — an
    inference from the printed figures, flagged in Gaps [S6].
  - Macif offers an explicit "jusqu'à vos 80 ans" option (open to entry ages up to 70 inclusive)
    alongside the lifetime option, with the last premium pro-rated to the policy anniversary in the
    year the insured turns 80 [S9][S10].
- Capital increases: allowed at Mutex up to age 84, once the temporary premium term is still
  running (or at any time for lifetime premiums); the incremental capital is priced on the
  technical basis and age at the date of the request and carries its **own fresh one-year waiting
  period** [S1 art. 15.1.1]. VIASANTÉ allows one increase per membership year up to age 86, again
  with a fresh one-year waiting period and a fresh two-year suicide exclusion on the increment
  [S8 art. 10].

### 7. Observed premium rates — the CCSF standardised tables
All figures are the **annual premium for a 5 000 € guaranteed capital**, exactly as printed. The
three CNP tables were located through CNP's regulated-information index page [S4].

| Insurer (date) | Entry 50 | Entry 60 | Entry 70 | Source |
|---|---|---|---|---|
| CNP Trésor Prévoyance GO 2 (01/01/2026) — viager | 164,52 € | 234,24 € | 361,92 € | [S5] |
| … temporaire 25 / 20 / 15 / 10 / 5 ans (entry 50) | 211,44 / 249,72 / 317,16 / 455,64 / 877,80 € | — | — | [S5] |
| … temporaire 25 / 20 / 15 / 10 / 5 ans (entry 60) | — | 258,72 / 292,44 / 358,92 / 502,68 / 948,36 € | — | [S5] |
| … temporaire 25 / 20 / 15 / 10 / 5 ans (entry 70) | — | — | 367,80 / 386,64 / 439,56 / 576,60 / 1 035,24 € | [S5] |
| … prime unique | 4 274,04 € | 4 548,60 € | 4 819,56 € | [S5] |
| LBP Solution Obsèques (12/11/2025) — viager | 252 € | 313 € | 434 € | [S6] |
| … temporaire 15 / 10 ans | 469 / 651 € | 481 / 660 € | 517 / 682 € | [S6] |
| … prime unique | 4 305 € | 4 530 € | 4 772 € | [S6] |
| Mgéfi PLURIO (26/10/2023) — viager | 194 € | 277 € | not printed | [S7] |
| … temporaire 15 / 10 ans | 354 / 507 € | 402 / 557 € | 504 / 647 € | [S7] |
| Macif Garantie Obsèques (01/01/2026) — viager | 232 € | 325 € | 499 € | [S10] |
| … jusqu'à 80 ans | 266 € | 406 € | 793 € | [S10] |
| … temporaire 10 / 5 ans | 636 / 1 182 € | 683 / 1 245 € | 771 / 1 333 € | [S10] |
| AXA Serenova (06/06/2025) — viager | 336,03 € | 390,68 € | 524,23 € | [S14] |
| … temporaire 20 ans | 391,85 € | 423,39 € | not available (entry limit 69) | [S14] |
| … temporaire 10 ans | 651,26 € | 663,61 € | 693,43 € | [S14] |
| Sogecap BUDGET (01/07/2025) — viager | 250 € | 352 € | 534 € | [S15] |
| … temporaire 10 / 5 ans | 685 / 1 261 € | 720 / 1 350 € | 820 / 1 455 € | [S15] |
| … prime unique | 4 282 € | 4 530 € | 4 751 € | [S15] |
| Mutex NÉOBSIA capital (18/08/2025) — temporaire 25 / 20 / 15 / 10 / 5 ans, entry 50 | 356 / 405 / 494 / 678 / 1 240 € | — | — | [S2] |
| … entry 60, temporaire 25 / 15 / 10 / 5 ans | — | 400 / 519 / 695 / 1 245 € | — | [S2] |
| BPCE Secur'Obsèques (07/2025) — temporaire 5 / 10 ans, entry 50 | 1 075,61 / 547,89 € | — | — | [S16] |

Derived from the table above (arithmetic performed on the printed figures, not quoted from any
document):
- **Lifetime premium as a percentage of the guaranteed capital**: 3,3 % (CNP) to 6,7 % (AXA) at
  entry 50; 4,7 % to 7,8 % at entry 60; 7,2 % to 10,7 % at entry 70. The spread between the
  cheapest and dearest insurer is roughly **2:1 at every age**.
- **Single premium as a percentage of the capital**: 85–86 % at entry 50, 91 % at entry 60, 95–96 %
  at entry 70, and the three insurers publishing one agree to within 0,6 pp [S5][S6][S15]. This is
  the clearest signal of the underlying reserving basis: a single premium of 0,855 × capital at
  entry 50 implies a discounted whole-life EPV plus loadings at a very low interest rate.
- **Age at which cumulative lifetime premiums first exceed the 5 000 € capital**, across entry ages
  50 / 60 / 70: age 80–84 (CNP Trésor Prévoyance), 76–78 (Mgéfi, two ages only), 70–82 (LBP), 72–80
  (Macif), 65–80 (AXA), 70–79 (Sogecap). For AXA at entry 50 it is **age 65** — the insured is
  expected to have paid more than the capital within fifteen years.
- The longest cumulative figure printed anywhere: **24 019 €** of lifetime premiums against a
  5 000 € capital, for entry age 70 surviving to 115 [S15]. This is the arithmetic behind the
  CCSF's concern about "situations in which the insured pays well beyond the guaranteed death
  capital" [R13] and behind AFIF's warning [R21].
- Premiums are **fixed at inception and never indexed** at CNP and its distributors [S5][S6][S7],
  at AXA (where the capital rises 1 % a year with no premium increase) [S14] and at BPCE (PB raises
  the capital, premiums unchanged) [S16]; but at Macif **the annual revalorisation of the guarantees
  is matched by a proportional increase in the remaining premiums** [S9][S10][S11]. This is a
  first-order modelling fork — see §10.

### 8. Délai de carence / délai d'attente
- Universal architecture: **accidental death is covered from the effective date; death from any
  other cause is covered only after a waiting period**, during which a non-accidental death
  produces a refund rather than the capital [S1 art. 8][S8 art. 1][S9][S11][S12][S13][R21].
- Retrieved durations and refund rules:
  | Insurer | Duration | Cause covered from day 1 | Paid on non-accidental death inside the period | Source |
  |---|---|---|---|---|
  | Mutex NÉOBSIA | **1 year** | accident | the **sum of premiums collected**, to the balance beneficiaries; assistance guarantees do not apply | [S1 art. 8] |
  | VIASANTÉ / UCR Sérénité | **1 year** | accident (full capital) | **premiums paid, excluding the assistance premium**, refunded to the estate | [S8 art. 1] |
  | Macif Garantie Obsèques | **1 year** | accident | **premiums paid, less any instalment charges**, to the subscriber or to the designated beneficiaries | [S9][S11][S13] |
- On a **capital increase** the increment carries a fresh waiting period of the same length; a
  non-accidental death inside it pays the pre-increase capital plus a refund of the incremental
  premiums (net of charges at VIASANTÉ) [S1 art. 15.1.1][S8 art. 10][S9][S13].
- Definition of accident, from the two contracts that give one:
  - Mutex: "toute atteinte corporelle de l'assuré, non intentionnelle de sa part, provenant de
    l'action soudaine et imprévisible d'une cause extérieure. Cependant, ne sont jamais considérés
    comme accident … les accidents cérébraux ou cardio-vasculaires quelle qu'en soit l'origine.";
    the burden of proving the accidental cause lies on the insured or their beneficiaries
    [S1 defs].
  - VIASANTÉ: "l'action violente, soudaine et imprévisible, d'une cause extérieure et non
    intentionnelle"; acute or chronic illness, and harm resulting from medical or surgical treatment
    or from medical examinations, are not accidents [S8 art. 2].
  - AFIF's market description matches, adding that myocardial infarction, coronary and
    cardio-vascular conditions and emotional shock are not accidents [R21].
- **Market cap**: the CCSF commitments, effective 1 July 2025, limit the waiting period to **one
  year maximum** for new contracts, against previously observed periods of up to **two years**
  [R13][R14][R15] — **[unverified]** against the avis itself (R11 could not be retrieved). All three
  contracts retrieved here already sit at one year.
- No retrieved contract pays interest on the refunded premiums. The "refund with interest" variant
  in the brief is **[unverified]**. What *is* in the law is a different rule: art. 8 of the loi
  Sueur requires the capital paid by the subscriber of an advance-**prestations** contract to bear
  interest at not less than the legal rate [R6].
- A single premium removes the exposure differently: a search snippet reports that PFG applies no
  waiting period at all where the premium is paid in one instalment — **[unverified]**, S19 could
  not be retrieved. None of the retrieved single-premium tables [S5][S6][S15] states a waiting-period
  variation by premium form.

### 9. Exclusions
- **Suicide** in the first year (Mutex [S1 art. 9], VIASANTÉ [S8 art. 17]) or first 12 months
  (Macif [S12][S13]) from the effective date, and again for the first year (Mutex, VIASANTÉ) or two
  years (VIASANTÉ, on the increment) following a capital increase.
- **War, civil war and military conflict**; **nuclear** transmutation and radiation — all three
  contracts [S1 art. 9][S8 art. 17][S12].
- **Murder of the insured by a beneficiary**, for that beneficiary's share, where convicted
  [S8 art. 17][S12].
- Macif additionally excludes death resulting from the insured's participation in an intentional
  offence or a crime [S12][S13].
- VIASANTÉ has by far the longest list: professional sport; listed amateur sports (air sports,
  bungee jumping, aerobatics, scuba with autonomous apparatus, ski jumping, freestyle skiing,
  caving, high-mountain alpinism, rock climbing); motor and boat racing and record attempts;
  accidents while driving without the required licence; flying in an aircraft without a certificate
  of airworthiness or with an unlicensed pilot; use of non-prescribed narcotics; and manifest
  drunkenness or blood alcohol at or above the Code de la route limit [S8 art. 17].
- **What is paid in an excluded case** — the parameter a model needs:
  - Mutex: "la garantie de l'assureur sera limitée à la **valeur de rachat** du contrat" [S1 art. 9].
  - VIASANTÉ: the **valeur de rachat**, or, where the death capital exceeds it, the **premiums
    collected net of contributions and taxes** [S8 art. 17].
  - Macif: the **provision mathématique** [S12].
- The CCSF commitments include limiting exclusion clauses and stating explicitly in the notice what
  surrender value is payable when death falls within an exclusion [R13][R15] — **[unverified]**
  against the avis itself. All three retrieved notices already do the latter.

### 10. Revalorisation — participation aux bénéfices and post-mortem uprating
Two distinct mechanisms, both present, and the model must keep them separate.

**(a) In-force revalorisation of the guaranteed capital.** Four distinct designs were retrieved:
- **PB credited annually to the capital, premiums unchanged.** Mutex: "revalorisation annuelle du
  capital obsèques, via le versement de la participation aux bénéfices" [S2]; the capital insured is
  "le capital choisi … majoré des participations aux bénéfices" [S1 art. 6]. PB is determined at
  each year end on the technical and financial results of the contract category, net of the
  technical interest used in pricing (art. A. 132-11 CA), and allocated as *participation aux
  bénéfices pour une durée maximale* (art. A. 132-16 CA); a rate is set each year for contracts in
  force at least one year [S1 art. 14]. BPCE is explicit about the formula: PB equals **90 % of
  technical and financial profits, after deducting a 1 % management charge on funds under management
  and the technical interest rate guaranteed at inception (art. A 335-1 CA)**, allocated to the
  mathematical provision so that the guaranteed capital rises with premiums unchanged [S16].
  Sogecap: "chaque année, le capital garanti **peut** être majoré de la participation aux résultats
  prévue au contrat" — discretionary [S15].
- **PB credited to the capital, with a matching increase in the remaining premiums.** Macif: PB
  from technical and financial management feeds a *fonds de revalorisation*; the insurer sets an
  annual revalorisation rate within the limits of that fund; the uprating is applied to each
  contract's mathematical provision on **1 April** of the following year, only at the principal
  due date and only once the contract has been in force more than a year; and **"la revalorisation
  s'accompagne d'une augmentation des cotisations restant à payer, d'un taux équivalent au taux de
  revalorisation"** [S9][S10][S11]. Annexe C sets out the accounts: a technical account (credit:
  premiums written, opening provisions, technical interest, the revalorisation awarded on 1 April
  of the following year; debit: claims, closing provisions, acquisition costs, management costs)
  and a PB account (credit: technical-account surplus, net investment income; debit: technical
  deficit, technical interest credited to mathematical provisions, prior-year PB deficit carried
  forward, and an **own-funds allocation equal to 10 % of the technical-account surplus plus 15 % of
  net investment income in excess of technical interest**) [S9 annexe C].
- **A contractual guaranteed uprating.** AXA Serenova: "le contrat prévoit une **revalorisation
  annuelle de 1 % du capital souscrit sans augmentation de la cotisation**" [S14]. This is the only
  guaranteed (as opposed to discretionary) uprating rate retrieved anywhere.
- **No uprating of the capital at all in the illustration.** CNP's tables present surrender values
  "sans participation aux bénéfices" and state that premiums are never indexed [S5][S6][S7]; they do
  not state that the capital is never uprated, only that the tables exclude PB.
- **Premiums are never uprated** at CNP/LBP/Mgéfi [S5][S6][S7], at AXA [S14] and at BPCE [S16]; they
  **are** uprated in step with the guarantees at Macif [S9][S10][S11]. Mutex's tables and conditions
  do not say either way for the premium — **[unverified]** for Mutex.
- Only one numerical revalorisation rate is retrievable end to end: the Macif DIC's illustration for
  entry age 60, capital 3 000 €, premiums to 80, gives revalorised death capitals of 3 038,56 € at
  1 year, 3 633,50 € at 15 years and 4 400,77 € at 30 years [S11]. Those three figures are a
  geometric series: the implied constant rate is **1,2854 % p.a.** (derived — 3 000 × 1,012854¹ =
  3 038,56; ×1,012854¹⁵ = 3 633,50; ×1,012854³⁰ = 4 400,77). This is an illustration, not a
  guarantee.
- The statutory floor for the prestations form: art. L. 2223-34-1 CGCT requires an annual allocation
  of **at least 85 %** of the credit balance of the financial account, multiplied by the ratio of
  the contract's mathematical provisions to total mathematical provisions, less the technical
  interest credited to that contract's provisions in the year; an *arrêté* is to specify the
  calculation [R3]. **That arrêté was not retrieved** — see Gaps.

**(b) Post-mortem revalorisation.** Required by art. L. 132-5 CA (and art. L. 223-19-1 du Code de
la mutualité for mutuelles) [R8][S8 art. 11]. The capital is uprated from the date of death (or the
date the insurer learns of it) until all documents needed for payment are received, or until
deposit at the Caisse des dépôts. The rate stated identically by two insurers is **the lower of
(i) the twelve-month average of the *taux moyen des emprunts de l'État français* (TME) calculated at
1 November of the preceding year and (ii) the last TME available at 1 November of the preceding
year** [S1 art. 6][S8 art. 11]. VIASANTÉ adds the statutory escalation: payment within one month of
receiving the documents, and beyond that the unpaid capital bears legal interest, **doubled for two
months and then tripled** [S8 art. 11]. Charges levied after the date of knowledge of death are
capped by decree, and no charge may be taken for the insurer's search-and-inform work [R8].

### 11. Rachat (surrender) and observed surrender values
- Every retrieved capital contract **carries a surrender value** — consistent with art. L. 132-23 CA,
  under which only temporary death assurance and annuities in payment are barred from carrying one
  [R10]. This holds **for lifetime-premium contracts too**: CNP, LBP, Macif, AXA and Sogecap all
  publish lifetime-premium surrender values [S5][S6][S10][S14][S15]. The brief's expectation that
  *primes viagères* often carry no surrender value is **not supported by any retrieved document**.
- The surrender value is the **provision mathématique** at the effective date of the request
  [S1 art. 20.1][S8 art. 13][S9][S12]. Total surrender only — no partial surrender at Mutex
  ("rachat total"), VIASANTÉ ("seules des demandes de rachat total seront acceptées") or Macif
  ("le rachat partiel du contrat n'est pas possible") [S1][S8][S9][S11].
- Payment deadlines: 30 days at Mutex (art. 20.3 says at the latest within the month following
  receipt of documents) [S1]; 30 days at VIASANTÉ [S8 art. 13]; **2 months** at Macif [S9][S11].
- Conditions and penalties:
  - VIASANTÉ: the right to surrender is acquired once **one annual premium** has been paid, and a
    **5 % penalty may be applied if surrender occurs in the first ten years**; separately, a 5 %
    charge is taken inside the mathematical provision during the **first eight years** [S8 arts. 7,
    13].
  - Mutex and Macif quote no surrender penalty; Macif's DIC states "aucune pénalité de sortie
    anticipée n'est appliquée" and a 0 % exit cost [S11].
  - Where a beneficiary has accepted the designation, surrender requires their consent
    [S8 art. 16][S11].
- **Technical basis for surrender values, where stated**: VIASANTÉ computes them "selon les
  paramètres techniques réglementaires du Code de la mutualité, la table de mortalité utilisée étant
  la **table TH 00-02** et le **Taux Technique … de 0,75 %**" [S8 art. 13]. Macif's DIC uses
  **TH 00-02** to define the life expectancy of a 60-year-old man for its lifetime-premium
  illustration [S11]. Mutex's worked example is computed at a **technical rate of 0 %** [S1 art. 20.1].
  These are the only technical bases published anywhere in the retrieved set.
- **Observed surrender values, 5 000 € capital** (euros, exactly as printed):
  | Insurer, entry age, form | 5 yr | 10 yr | 15 yr | 20 yr | 25 yr | 30 yr | 35 yr | 40 yr | 45 yr | Source |
  |---|---|---|---|---|---|---|---|---|---|---|
  | CNP TPGO, 50, viager | 650,15 | 1 275,19 | 1 876,68 | 2 460,79 | 3 004,02 | 3 484,41 | 3 876,12 | 4 176,77 | 4 399,53 | [S5] |
  | CNP TPGO, 50, unique | 4 162,06 | 4 282,64 | 4 398,69 | 4 511,38 | 4 616,18 | 4 708,86 | 4 784,43 | 4 842,43 | 4 885,41 | [S5] |
  | CNP TPGO, 50, temp 10 | 2 083,01 | 4 282,64 | 4 398,69 | 4 511,38 | 4 616,18 | 4 708,86 | 4 784,43 | 4 842,43 | 4 885,41 | [S5] |
  | CNP TPGO, 70, viager | 1 069,61 | 2 015,21 | 2 786,24 | 3 378,05 | 3 816,54 | — | — | — | — | [S5] |
  | LBP, 50, viager | 518 | 1 044 | 1 595 | 2 183 | 2 801 | 3 424 | 4 033 | 4 707 | 4 797 | [S6] |
  | LBP, 50, unique | 3 392 | 3 539 | 3 691 | 3 851 | 4 016 | 4 175 | 4 316 | 4 426 | 4 495 | [S6] |
  | Macif, 50, viager | 662 | 1 309 | 1 935 | 2 520 | 3 055 | 3 534 | 3 925 | 4 213 | 4 420 | [S10] |
  | Macif, 50, temp 5 | 4 429 | 4 516 | 4 600 | 4 678 | 4 750 | 4 814 | 4 867 | 4 905 | 4 933 | [S10] |
  | Macif, 60, viager | 847 | 1 639 | 2 363 | 3 011 | 3 540 | 3 930 | 4 210 | — | — | [S10] |
  | Macif, 70, viager | 1 076 | 2 039 | 2 825 | 3 404 | 3 821 | — | — | — | — | [S10] |
  | AXA Serenova, 50, viager | 784,01 | 1 574,90 | 2 346,97 | 3 151,33 | 3 980,74 | 4 828,57 | 5 659,93 | 6 429,96 | 7 135,11 | [S14] |
  | AXA Serenova, 50, temp 10 | 2 701,65 | 5 767,93 | 6 003,11 | 6 256,67 | 6 530,11 | 6 824,80 | 7 142,86 | 7 485,99 | 7 854,08 | [S14] |
  | Sogecap BUDGET, 50, viager | 695 | 1 351 | 1 977 | 2 553 | 3 078 | 3 539 | 3 910 | 4 191 | 4 395 | [S15] |
  | Sogecap BUDGET, 70, viager | 1 148 | 2 067 | 2 808 | 3 369 | 3 775 | 4 129 | 4 473 | 5 000 | 5 000 | [S15] |
  | Mutex NÉOBSIA, 50, temp 25 | 981 | 1 958 | 2 933 | 3 938 | 5 074 | 5 057 | 5 043 | 5 033 | 5 026 | [S2] |
  | BPCE Secur', 50, temp 10 | 2 477 | 5 000 | — | — | — | — | — | — | — | [S16] |
- Three shapes to notice, all first-order for the model:
  1. **Lifetime-premium surrender values rise steadily but stay well below the capital** for
     decades — at CNP entry 50 the value is still only 88 % of the capital after 45 years [S5].
  2. **Paid-up contracts (single or expired temporary premiums) sit just below the capital and drift
     up towards it** — CNP's paid-up value grows from 4 162 € to 4 885 € between years 5 and 45, and
     Sogecap's reaches exactly 5 000 € at 40 years [S5][S15]. This is the mathematical provision of a
     paid-up whole life converging on the sum assured.
  3. **Where the capital is uprated, the surrender value overshoots the original capital** — AXA's
     paid-up value reaches 7 854 € against a 5 000 € original capital at 45 years, consistent with
     its guaranteed 1 % annual uprating [S14]; Mutex's temporary-premium values peak at 5 074 € and
     then *decline* slowly [S2].
- **Mutex worked example** [S1 art. 20.1], entry age 65, capital **1 000 €**, technical rate 0 %,
  before PB and taxes — the only per-1 000 grid in a contract wording:
  | Form | Annual premium | Cum. prem. yr 8 | Surrender value yr 1 | yr 5 | yr 8 |
  |---|---|---|---|---|---|
  | viagère | 80,26 € | 642,07 € | 41,95 € | 201,74 € | 312,79 € |
  | temporaire 5 ans | 259,02 € | 1 295,10 € (paid up after yr 5) | 203,34 € | 1 053,28 € | 1 045,87 € |
  | temporaire 10 ans | 145,95 € | 1 167,57 € | 97,77 € | 496,28 € | 812,94 € |
  | temporaire 15 ans | 110,49 € | 883,96 € | 64,67 € | 321,64 € | 516,40 € |
  | temporaire 20 ans | 95,28 € | 762,25 € | 50,47 € | 246,70 € | 389,14 € |
  | temporaire 25 ans | 88,84 € | 710,71 € | 44,46 € | 214,97 € | 335,25 € |
  Note the 5-year row: after the last premium the surrender value **decreases** (1 053,28 →
  1 050,76 → 1 048,29 → 1 045,87), because the annual charge of 0,40 % of the guaranteed capital
  continues while no premium comes in [S1 art. 13.4].
- **Macif worked grids** [S9 annexe B], first eight years, excluding revalorisation and taxes:
  entry 50, capital 3 800 €, adhesion 01/04/2024 — premiums to age 80 at 204,99 €/yr give surrender
  values 119,88 € (yr 1) rising to 954,39 € (yr 8); premiums over 10 years at 489,61 €/yr give
  329,55 € rising to 2 714,96 €. Entry 55, capital 4 580 € — premiums to 80 at 299,16 €/yr give
  170,88 € to 1 365,10 €; over 10 years at 608,76 €/yr give 401,27 € to 3 324,60 €.

### 12. Réduction (paid-up) and non-payment of premiums
- The statutory path is art. L. 132-20 CA: the insurer has no action to compel payment; ten days
  after the due date it sends a registered letter; forty days later, continued non-payment produces
  **either termination** (where the surrender value is nil or insufficient) **or réduction** of the
  contract [R7]. Every retrieved contract implements exactly this [S1 art. 13.3][S8 art. 9][S9].
- Cover is **suspended during the forty-day period**: "Aucune prise en charge du paiement du capital
  décès n'interviendra durant la période de 40 jours précitée de suspension de la garantie"
  [S1 art. 13.3].
- VIASANTÉ splits by contract year: non-payment in **year 1** terminates the membership; from
  **year 2** it puts the contract into réduction [S8 art. 9].
- The paid-up sum assured (*valeur de réduction*) is a function of the mathematical provision
  reached, the insured's attained age, the regulatory technical rate in force and the contractual
  loading rates [S8 defs, art. 14]; Mutex computes it from entry age, completed years of premium
  payment, the guaranteed capital at the date of réduction and the premium form [S1 art. 16].
- **Automatic substitution of surrender for réduction** where the reduced amount is too small: Mutex
  substitutes surrender if the surrender value is below **half the monthly SMIC** (art. R. 132-2 CA)
  [S1 art. 13.3]; VIASANTÉ substitutes surrender if the reduced capital is below **50 % of the
  SMIC** [S8 art. 14]; Macif may substitute under art. L. 223-22 du Code de la mutualité [S9].
  Art. L. 132-23 CA gives the insurer that power generally [R10].
- **Assistance guarantees are cancelled on réduction** [S1 art. 16][S8 art. 14][S9] — a small but
  real reduction in benefit outgo the model may ignore, since assistance is not a cash benefit.
- Macif's DIC quantifies a réduction: entry 60, capital 3 000 €, premiums to 80 — the paid-up
  guarantee equals the surrender value at 1 and 15 years (138,13 € and 2 080,06 €), and réduction is
  "sans objet" at 30 years because the premium-paying period has ended [S11].

### 13. Charges
The three insurers that disclose a charge structure disclose three different structures.

| Charge | Mutex NÉOBSIA [S1 art. 13.4] | VIASANTÉ / UCR Sérénité [S8 art. 7] | Macif Garantie Obsèques [S9][S12] |
|---|---|---|---|
| Entry / on premiums | **5 %** of every premium | acquisition max **10 %** of the annual premium (**10,3 %** for lifetime premiums), and in any case ≤ **2,5 % of the guaranteed capital** (art. L. 223-20-1 Code de la mutualité); collection administration max **20 %** of the annual premium | max **5,38 %** of the capital guaranteed at subscription for the "Capital" formula; **4,89 %** for complementary capitals (annual percentage over the average contract duration) |
| Ongoing | **0,40 % p.a. of the guaranteed capital** for the whole contract life, **plus 0,57 % p.a.** during a lifetime-premium paying period **or 0,80 % p.a.** during a temporary-premium paying period | max **0,4 % p.a. of the guaranteed capital** plus **3,3 % p.a. of the annual premium** | **none** |
| Exit / surrender | none | 5 % taken inside the mathematical provision during the **first 8 years**; a **5 % penalty** if surrender occurs in the **first 10 years** | none |
| Instalment | none | not stated | yes (amount on the individual certificate) |
| Other | assistance cost included in the premium | assistance premium **12 € p.a.**, outside the above | assistance included |
- Macif's PRIIPs KID puts a single number on the whole thing: **reduction in yield of 1,77 % p.a.
  over a 30-year holding** (24,08 % over 1 year, 4,86 % over 15), all of it classified as an entry
  cost, with zero ongoing, exit, transaction and performance costs; total costs 75 € / 1 120 € /
  1 493 € at 1 / 15 / 30 years on a premium of 247,60 € a year [S11].
- Statutory anchor: art. L. 2223-35-1 CGCT permits, for a change of funeral, operator or service
  content at equivalent services, **only the management charges provided in the general conditions**
  [R5]. AFIF records that a clause allowing the bank or insurer to retain 5 % of premiums where the
  chosen operator does not perform was struck down as abusive (TGI Paris, 9 October 2006) [R21].

### 14. Beneficiary designation and payment mechanics
- The default architecture in every capital contract is two-tier: **first-rank beneficiary** is the
  funeral firm that carried out the services (or, failing that, whoever paid its invoice), up to the
  costs actually incurred and within the guaranteed capital; the **balance** goes to the beneficiaries
  freely designated by the subscriber, and failing them to a standard cascade — surviving spouse not
  judicially separated, failing that the PACS partner, failing that the *concubin notoire*, failing
  that the children born or to be born in equal shares, failing that the heirs under the legal
  devolution [S1 arts. 3, 11][S8 art. 16][S9][S12].
- Macif requires a named designation to be followed by the words "à charge pour ce ou ces
  bénéficiaires de financer les obsèques de l'assuré à concurrence de leur coût et dans la limite du
  capital garanti", and by "à défaut à mes héritiers" [S12] — the drafting device that carries
  art. L. 2223-33-1 CGCT [R2] into the beneficiary clause.
- The funeral operator may be named as beneficiary and can be **changed at any time** by changing
  the beneficiary clause, per art. L. 2223-35-1 CGCT [S12][R5].
- Acceptance by a beneficiary makes the designation irrevocable and blocks both a change of
  beneficiary and a surrender [S1 art. 11.1][S8 art. 16][S11]. Acceptance of a gratuitous
  designation cannot take place until at least thirty days after the subscriber is informed the
  contract is concluded [S1 art. 11.1].
- Documents required on death: death certificate; a **detailed paid invoice from the funeral
  operator**; proof of the beneficiaries' identity and entitlement; documents required by tax law;
  and, where death occurs inside the waiting period, a **medical certificate stating whether the
  cause was illness, accident or suicide** [S1 art. 17][S8 art. 15][S9]. VIASANTÉ routes medical
  documents to its *médecin conseil* under confidential cover and makes payment subject to that
  doctor's prior acceptance [S8 arts. 15, 18].
- Payment deadlines: **8 days** from receipt of documents at Mutex [S1 art. 18]; **30 days** at
  Macif [S9][S12] and at VIASANTÉ [S8 art. 15]; the statutory maximum for mutuelles is one month
  (art. L. 223-22-1) [S8 art. 11].
- Contract search: AGIRA operates the national file created by art. L. 2223-34-2 CGCT; a request
  with a death certificate obliges insurers to respond within **3 business days** [R4][R19].

### 15. Renonciation (cooling-off)
- **30 calendar days** from the moment the subscriber is informed the contract is concluded, under
  art. L. 132-5-1 CA [S1 art. 19][R7][R21], or art. L. 223-8 du Code de la mutualité for mutuelles,
  with the distance-selling variant running from the later of the effective date and the date the
  membership conditions and the notice are received (art. L. 221-18) [S8 art. 20].
- Effect: **full refund of all premiums paid**, within 30 days of receipt of the notice; all
  guarantees cease at the date the letter is received [S1 art. 19][S8 art. 20][S11].
- Failure to hand over the general conditions or the notice extends the 30-day period; the Cour de
  cassation (2e civ., 8 March 2006, pourvoi n° 05-10324) held that the sanction is prorogation of
  the period only, "30 jours et 8 années" in AFIF's phrase [R21].

### 16. Taxation
- **Applicability is verified from four primary documents** [S1 art. 26][S9][S11][S13]:
  - death benefits arising from premiums paid **before** the insured's 70th birthday fall under a
    specific levy under **art. 990 I CGI**;
  - premiums paid **from** the insured's 70th birthday fall under ordinary inheritance duty under
    **art. 757 B CGI**;
  - a surrender is taxed on its gain under **art. 125-0 A CGI**, by income tax or by election a
    *prélèvement libératoire*;
  - social levies apply under **art. L. 136-7 du Code de la sécurité sociale** [S1 art. 26.3], each
    year, on surrender and where applicable on death [S9].
- **The numerical thresholds and rates were not retrieved.** The commonly cited 152 500 € allowance
  per beneficiary, the 20 % / 31,25 % levy under 990 I and the 30 500 € global allowance under
  757 B are **[unverified]** here: neither Légifrance's CGI articles nor a service-public page
  carrying them could be fetched (see R24, R18 and the Gaps section).
- **"Primes manifestement exagérées"** — verified verbatim from art. L. 132-13 CA [R7]: the death
  capital escapes *rapport à succession* and *réduction pour atteinte à la réserve*, and so do the
  premiums, "à moins que celles-ci n'aient été manifestement exagérées eu égard à ses facultés".
  This is the risk the brief flags at high ages: a funeral contract taken out very late, with a
  large single premium relative to the subscriber's means, can be re-integrated into the estate at
  the heirs' request. **No retrieved document quantifies the threshold** — it is a judge-made,
  fact-specific test (age, family and financial situation, utility of the operation) and no
  numerical rule exists in the retrieved sources. Note that the practical exposure for this product
  is bounded by the aggregate capital caps in §5 (10 000 € at Mutex and VIASANTÉ, 17 580 € at Macif)
  and by the single premiums in §7 (at most 4 819,56 € for 5 000 € of cover at age 70 [S5]).
- Guarantee fund: the FGAP (Fonds de garantie des assurances de personnes) covers, in aggregate
  across all capital contracts held by one insured with the failed undertaking, up to **70 000 €**
  [S11]; Mutex states its FGAP membership under art. L. 423-1 CA [S1 art. 25].
- Estate-side figures: up to **5 965 €** may be drawn from the deceased's bank account for funeral
  costs (art. L. 312-1-4 CMF, figure verified at 1 January 2026), and funeral expenses are
  deductible from the estate up to **1 500 €** [R17].

### 17. Technical bases retrievable from public sources
- **Mortality table**: **TH 00-02** — used by VIASANTÉ to compute surrender values [S8 art. 13] and
  by Macif to define the life expectancy underlying its lifetime-premium illustration [S11]. TH/TF
  00-02 are the regulatory population tables for death cover; the generation tables TGH05/TGF05 are
  for annuities and are not used here. **The arrêté du 1er août 2006 annexing these tables was not
  retrieved** (no Légifrance URL could be resolved without a working search) — see Gaps.
- **Technical rate**: **0,75 %** at VIASANTÉ [S8 art. 13]; **0 %** in Mutex's worked example
  [S1 art. 20.1]; BPCE refers to "le taux d'intérêt technique garanti à l'adhésion, visé à l'article
  A 335-1 du Code des assurances" without giving a number [S16]; VIASANTÉ defines the technical rate
  as the minimum return included in the pricing, with regulatory limits depending on the TME
  [S8 defs].
- **Post-mortem revalorisation rate**: the lower of the 12-month average TME calculated at 1 November
  of the preceding year and the last TME available at that date [S1 art. 6][S8 art. 11].
- **PB formula**: 90 % of technical and financial profits less a 1 % charge on funds under
  management and less the guaranteed technical interest [S16]; art. A. 132-11 CA basis with
  allocation "pour une durée maximale" under A. 132-16 [S1 art. 14]; the Macif revalorisation-fund
  accounts with a 10 % / 15 % own-funds allocation [S9 annexe C]; and the statutory 85 % floor for
  prestations contracts under art. L. 2223-34-1 CGCT [R3].
- **Charge levels**: §13 above.
- **Lapse / surrender experience**: **no public source gives any lapse, surrender or paid-up rate
  for this product.** Nothing retrieved contains a decrement assumption other than mortality.
- **Expense assumptions in currency terms**: none published; only the percentage charge structures
  in §13 and the PRIIPs reduction-in-yield [S11].

### 18. Market size and the funeral-cost benchmark
- Market (all figures from secondary summaries of the CCSF avis, **[unverified]** against R11):
  - **more than 5,3 million contracts in force in 2023**, a portfolio of **1,8 bn €**, about
    **190 000 deaths covered a year (≈30 % of French deaths)**, average capital about **5 000 €**
    [R14];
  - **1,8 bn € of premiums and 539 000 new policies in 2023** [R15].
- Funeral cost:
  - **Primary and unanimous**: seven insurers' standardised tables state that 5 000 € "est proche du
    coût moyen des obsèques en France **hors marbrerie**" [S5][S6][S7][S10][S14][S15][S16].
  - **Secondary**: average French funeral cost **4 730 € in 2025**, split **5 044 € inhumation /
    4 434 € crémation**, per a Silver Alliance study published late 2024 and reported 16 October
    2025 [R22]. The underlying study was not retrieved.
  - For scale, the state-side figures: 5 965 € drawable from the deceased's account, 1 500 €
    deductible from the estate [R17].
- Distribution and conduct context: funeral firms selling these contracts must be registered as
  insurance intermediaries (loi du 15 décembre 2005 and its décrets of 30 August 2006) [R21]; from
  **1 October 2026** every funeral operator must hand families a standardised neutral information
  notice (décret n° 2026-770 and arrêté du 13 août 2026) [R20].

### 19. The CCSF commitments (effective 1 July 2025)
All of this is **[unverified]** against the avis itself, which returned HTTP 403 on every attempt
(R11, R12). It is reported consistently by four independent secondary sources [R13][R14][R15][R16],
and the standardised tables retrieved here [S2][S3][S5][S6][S10][S14][S15][S16] are direct physical
evidence that the table commitment was implemented.
- Publish a **standardised examples table**: for a **5 000 €** guaranteed capital and entry ages
  **50, 60 and 70**, show the annual premium, the cumulative premiums by age at death, and the
  surrender values by duration, for every premium form offered; make it downloadable from the
  distributor's website [R13][R15].
- Cap the **délai de carence at one year** (previously up to two years) [R13][R14][R15].
- **Systematically offer temporary-premium alternatives** alongside lifetime premiums [R13][R15].
- **Limit contractual exclusions**, and state in the notice the surrender value payable when death
  falls within an exclusion [R13][R15].
- Inform the subscriber annually of the capital revalorisation [R15 — search-snippet level,
  weakest of the four].
- Scope: individual contracts and group contracts with individual membership, on a **whole-life**
  guarantee, **excluding savings contracts and fixed-term guarantee contracts** [R16].
- Effectiveness review one year after 1 July 2025, i.e. July 2026 [R13][R15]. The avis is
  **non-binding** [R13].

### 20. What no public source gives — flag these for `[std]` at drafting time
- **Any insurer's actual pricing basis**: the mortality table, technical rate, expense loading and
  profit margin behind the published premiums. Only two technical-basis fragments exist anywhere in
  the retrieved set (TH 00-02 / 0,75 % at VIASANTÉ [S8]; 0 % in Mutex's worked example [S1]).
- **Lapse, surrender and paid-up (réduction) rates.** Nothing. Not one figure.
- **The PB rate actually declared** by any insurer in any year for a funeral contract. Only
  mechanisms and one illustrative rate derived from a KID scenario (1,2854 % p.a. at Macif [S11]) and
  one contractual guarantee (1 % p.a. at AXA [S14]).
- **Mortality experience of guaranteed-issue lives inside and just after the waiting period** — the
  anti-selection load the waiting period exists to control. No public data.
- **Age at which lifetime premiums cease**, where they cease at all: only inferable, and
  inconsistently, from the tables (§6).
- **The proportion of contracts sold in each premium form**, and the average entry age. Not
  published.
- **The split of the market between capital and prestations forms.** Not published.
- **Tax thresholds under arts. 990 I and 757 B CGI** — the articles could not be fetched (R24).
- **The arrêté implementing the 85 % PB quota** of art. L. 2223-34-1 CGCT (R3). Not located.
- **Any French funeral-contract experience study** from the Institut des actuaires or the ACPR. No
  such document was located within this session's search budget.

---

## Variations across insurers

| Feature | Mutex NÉOBSIA [S1][S2][S3] | CNP (TPGO / LBP / Mgéfi) [S5][S6][S7] | VIASANTÉ / UCR Sérénité [S8] | Macif Garantie Obsèques [S9]–[S13] | AXA Serenova [S14] | Sogecap BUDGET [S15] | BPCE Secur' [S16] |
|---|---|---|---|---|---|---|---|
| Legal chassis | individual, Code des assurances | group / individual, Code des assurances | group (ADPM), Code de la mutualité | group with optional membership, Code de la mutualité | individual, Code des assurances | individual/group, Code des assurances | individual/group, Code des assurances |
| Capital range | 2 000–10 000 € | tables at 5 000 € | nine steps 2 000–10 000 € | 2 000 / 3 000 € + 500 € tranches to 13 000 € | tables at 5 000 € | tables at 5 000 € | tables at 5 000 € |
| Aggregate cap | 10 000 € | not stated | 10 000 € (20 000 € accidental from yr 2) | **17 580 €** | not stated | not stated | not stated |
| Entry ages | 18–84 | not stated in tables | 18–<86, **band depends on premium term** | 18–80 incl. | ≤69 for the 20-yr term | not stated | not stated |
| Medical underwriting | none | none stated | none stated | none | none stated | none stated | none stated |
| Prime unique | no | **yes** (TPGO, LBP) | no | no | no | **yes** | no |
| Primes viagères | yes in the wording, **NA in the Harmonie tables** | yes | yes (ages 40–85) | yes | yes | yes | **no** |
| Temporary terms | 5/10/15/20/25 | 5–25 (TPGO), 10/15 (LBP, Mgéfi) | 10/15/20/25 | 5/10 and "to age 80" | 10/20 | 5/10 | 5/10 |
| Délai de carence | 1 yr, illness; accident from day 1 | "carences" referenced in footnotes, duration not in tables | 1 yr, illness; accident from day 1 | 1 yr, illness; accident from day 1 | "carences" referenced, duration not in tables | "carences" referenced | "carences" referenced |
| Paid inside the waiting period | premiums collected | not stated in tables | premiums paid, less assistance premium | premiums paid, less instalment charges | not stated | not stated | not stated |
| Accidental death bonus | none | none | **double capital from year 2** | none | none | none | none |
| Capital revalorisation | annual PB credited to the capital | tables exclude PB; premiums never indexed | PB by board decision, contracts ≥1 yr old | PB → *fonds de revalorisation* → 1 April credit | **guaranteed 1 % p.a.** | discretionary PB "peut" raise the capital | PB = 90 % of profits less 1 % charge and technical interest |
| Premiums revalued too? | not stated | **no** | not stated | **yes, in the same proportion** | **no** | not stated | **no** |
| Surrender | yes, PM, total only, 30 days | yes (tables published for every form) | yes after 1 annual premium; **5 % penalty in the first 10 yrs** | yes, PM, total only, **2 months** | yes | yes | yes |
| Entry charge | 5 % of each premium | not disclosed | ≤10 % (10,3 % viagère) of premium, ≤2,5 % of capital | ≤5,38 % of capital (4,89 % on top-ups) | not disclosed | not disclosed | not disclosed |
| Ongoing charge | 0,40 % + 0,57 %/0,80 % of capital | not disclosed | ≤0,4 % of capital + 3,3 % of premium | **none** | not disclosed | not disclosed | 1 % on encours (inside the PB formula) |
| Technical basis published | technical rate 0 % in the worked example | none | **TH 00-02, 0,75 %** | **TH 00-02** (life-expectancy illustration) | none | none | art. A 335-1 CA referenced |
| Prestations form sold | **yes** — Essentielle 3 500 €, Exigence 4 500 €, Sérénité 6 000 € (LMO) | not in the retrieved documents | no | **yes** — 3 800 € and 4 580 € equivalents, eco variant | not in the retrieved document | not in the retrieved document | not in the retrieved document |

Representative design for a reference implementation: **Mutex NÉOBSIA Garantie obsèques en capital
[S1]** is the cleanest single wording — an individual whole-life contract, capital 2 000–10 000 €,
entry 18–84 with no medical selection, six premium forms (5/10/15/20/25-year and lifetime), a
one-year waiting period with premium refund, a fully specified charge structure, PB credited to the
capital, post-mortem revalorisation on the TME rule, surrender at the mathematical provision, and a
published worked grid of premiums and surrender values. Where NÉOBSIA is silent or unusual (it
publishes no single premium and its Harmonie distribution suppresses lifetime premiums), **CNP
Trésor Prévoyance Garantie Obsèques 2 [S5]** supplies the missing arm: seven premium forms including
the single premium, at three entry ages, with cumulative premiums and surrender values. Between
them the two documents pin down every quantity the model needs except the pricing basis itself.

The structural forks that a configurable model must carry:
1. **Premium form** — single, temporary (5/10/15/20/25 years or to a fixed age), or lifetime; and,
   for lifetime, whether premiums cease at an age (LBP appears to stop near 90 [S6]; Sogecap does
   not stop at all [S15]).
2. **Revalorisation coupling** — capital only (CNP, AXA, BPCE, Sogecap, Mutex) versus capital *and*
   remaining premiums in the same proportion (Macif) [S9][S10][S11].
3. **Waiting-period benefit** — refund of premiums gross (Mutex), net of the assistance premium
   (VIASANTÉ), or net of instalment charges (Macif).
4. **Exclusion benefit** — surrender value (Mutex, VIASANTÉ) versus mathematical provision (Macif);
   in practice the same quantity, but the wordings differ and VIASANTÉ substitutes the net premiums
   where they exceed the surrender value [S8 art. 17].
5. **Surrender penalty** — none (Mutex, Macif) versus 5 % in the first ten years plus a 5 % charge
   inside the provision in the first eight (VIASANTÉ) [S8].
6. **Accidental-death multiplier** — 1× everywhere except VIASANTÉ, where accidental death from
   year 2 pays **double** the capital, subject to a 20 000 € cap [S8 art. 4.2].

---

## Gaps and caveats

1. **The CCSF avis itself could not be retrieved.** `https://www.banque-france.fr/system/files/import/ccsf/ccsf_avis_contrats_obseques.pdf`
   returned HTTP 403 on three attempts, with and without its query string, and the CCSF press
   release at the same host returned 403 as well [R11][R12]. Everything attributed to the avis —
   the market figures (5,3 M contracts, 1,8 bn €, 190 000 deaths, 539 000 new policies, 5 000 €
   average capital), the one-year carence cap, the exclusion limits, the commitment to offer
   temporary alternatives, and the July 2026 review — comes from four secondary summaries
   [R13][R14][R15][R16] and is tagged **[unverified]**. The one part that is independently
   corroborated is the standardised table itself: sixteen tables from seven insurers were retrieved
   in the prescribed format.
2. **Tax thresholds are not verified.** Légifrance's CGI landing page loads [R24] but the
   intermediate table-of-contents page exceeds the fetcher's 10 MB limit and the article search is
   JavaScript-rendered, so **arts. 990 I, 757 B and 125-0 A were never read**. Their *applicability*
   is verified from four insurer documents [S1][S9][S11][S13]; the 152 500 € allowance, the 20 % /
   31,25 % rates and the 30 500 € allowance are **[unverified]**. service-public's page on
   distinguishing assurance-vie from assurance décès [R18] carries no tax figures at all.
3. **Code de la mutualité articles not read.** The code's landing page loads [R23], but
   arts. L. 223-8, L. 221-18, L. 223-19-1, **L. 223-20-1** (the 2,5 %-of-capital acquisition-charge
   cap for *formules de financement d'obsèques*), L. 223-22, L. 223-22-1, L. 223-25-4 and R. 223-9
   were not retrieved. Everything attributed to them rests on the VIASANTÉ and Macif notices
   [S8][S9] and the article texts are **[unverified]**.
4. **The arrêté implementing the 85 % PB quota** of art. L. 2223-34-1 CGCT was not located [R3].
   Nor is it settled from the retrieved text whether that quota binds a pure **capital** contract or
   only a **prestations** contract: the article is drafted for "tout contrat prévoyant des
   prestations d'obsèques à l'avance". The drafter should not assume it applies to the capital form.
5. **Legislative attribution conflict on art. L. 2223-35-1.** Légifrance's own article page states
   it was **created by loi n° 2005-1564 du 15 décembre 2005, art. 15 (V)** [R5]; AFIF's guide quotes
   it as inserted by **loi n° 2004-1343 du 9 décembre 2004** [R21]. Légifrance is the authority and
   is followed here, but the discrepancy is recorded because the 2004 attribution is widespread. The
   full text of loi n° 2004-1343 and of loi n° 2013-672 was **not** retrieved — only their effects,
   through the consolidated article pages [R3][R5] and AFIF's quotation [R21].
6. **The loi Sueur does less than the brief assumes.** The retrieved JORF text of loi n° 2008-1350
   du 19 décembre 2008 [R6] contains the legal-interest floor (art. 8), the amendment to L. 2223-33
   (art. 7) and the national file (art. 9). The "detailed and personalised description of the
   prestations" and the "faculty to modify" come from the 2004 and 2005 statutes and from the 2013
   rewrite [R3][R5][R21], not from the loi Sueur.
7. **Three insurer documents could not be retrieved.** Malakoff Humanis' note d'information returned
   **HTTP 410 Gone** [S17]; Auxia's Prépar'Obsèques notice returned **403** twice [S18]; PFG's
   funeral-financing page returned **403** twice, on both the https and the redirected http URL
   [S19]. The PFG figures circulating in search snippets (capital 1 000–15 000 € revalued annually,
   no waiting period for a single premium) are therefore **[unverified]** and no PFG or OGF wording
   is cited. AG2R La Mondiale, Groupama, MAIF, Crédit Mutuel/ACM, GMF, Swiss Life and Le Conservateur
   were **not sourced at all**: the session's WebSearch budget (200 calls) was exhausted before their
   documents could be located, and without search their PDF URLs cannot be discovered honestly.
   Snippet-level claims seen in search results — AG2R reducing the waiting period to six months, and
   Crédit Mutuel applying twelve months for non-accidental death — are **[unverified]** and are not
   used anywhere above.
8. **Table extraction artefacts.** Several standardised tables are laid out as free-floating text
   runs and the PDF text extractor loses thousand separators and empty cells:
   - In Mutex's worked example [S1 art. 20.1] the 5-year row's cumulative premiums extract as
     "036,08" and "295,10" where the page prints 1 036,08 and 1 295,10; the values used above are
     reconstructed from the annual premium (259,02 × 4 and × 5) and are internally consistent.
   - In La Banque Postale's age-50 lifetime row [S6] eight cumulative figures were recovered for
     nine age columns; the value in the 95-column is **not legible** in the extraction and is not
     quoted. In the age-60 row the 90- and 95-columns both read 9 400 €, from which premium
     cessation near age 90 is **inferred, not stated** by the document.
   - Mutex's age-60 table [S2] prints no legible annual premium for the 20-year term (the cumulative
     figures imply about 438,80 €/yr); the figure is omitted above rather than guessed.
   - Mgéfi's age-70 table [S7] shows a "Viager / Jusqu'au Décès" row with **no figures in any
     column**; whether lifetime premiums are unavailable at that age or the cells simply failed to
     extract cannot be determined from the extraction, so nothing is quoted for it.
   Every figure quoted in §7 and §11 is one that appeared verbatim in the extracted text.
9. **Standardised tables are illustrations, not contracts.** Each carries the line "Ce tableau …
   n'a pas de valeur contractuelle" and "Ces valeurs de rachat sont présentées sans participation aux
   bénéfices" [S5][S6][S7][S10][S14][S15][S16]. They are excellent for calibrating a mechanics
   demonstration and worthless as a pricing basis.
10. **Regulatory mortality tables are cited but not shipped.** TH 00-02 is named by two insurers
    [S8][S11] and is annexed to the arrêté du 1er août 2006, but **that arrêté was not retrieved** —
    no Légifrance URL for it could be resolved once the search budget was gone. Consistent with the
    frlib house rule, the decrement CSVs shipped with this product must be **[std] proxies** built
    from INSEE population data and anchored so that the model reproduces the notes' own placeholder
    rate; the arrêté and its tables are cited by name and never redistributed.
11. **No experience data of any kind.** No lapse rate, no surrender rate, no paid-up rate, no
    mortality experience for guaranteed-issue funeral lives, and no declared PB rate for any funeral
    contract in any year was found in any public source. Every such assumption in the product
    documents will have to be **[std]**.
12. **Version drift.** The retrieved documents span 26/10/2023 (Mgéfi tables [S7]) to 01/07/2026
    (Macif note d'information and DIC [S9][S11]). Where they disagree — for example on whether a
    given insurer offers lifetime premiums — the difference may be distribution-specific rather than
    a change over time. Mutex is the clearest case: the conditions générales [S1] offer lifetime
    premiums, while the Harmonie-Mutuelle standardised tables [S2] mark them NA.
13. **Living texts.** Légifrance article versions were captured as at 2026-08-26: L. 2223-34-1 at
    its 28/07/2013 version [R3], L. 2223-35-1 at 16/12/2005 [R5], L. 132-5 at 01/01/2016 [R8],
    L. 132-22 at 24/10/2024 [R9], L. 132-23 at 14/06/2026 [R10]. Check for later amendments before
    relying on article numbers. The funeral-operator information notice under décret n° 2026-770
    only takes effect on 1 October 2026 [R20].
