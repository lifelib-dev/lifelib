# Immediate Life Annuity (rente viagère immédiate, individual) — research notes (France)

Research notes for the French individual immediate life annuity — the *rente viagère
immédiate*: a capital sum converted, once and irrevocably, into a stream of *arrérages*
(annuity instalments) payable for life. In France the same liability arises three ways: as
the *sortie en rente* of an *assurance vie* contract, as the *liquidation en rente* of a
*Plan d'Épargne Retraite* (PER) or of an older *PERP* / *Madelin* / *régime L. 441*, or under
a standalone *contrat de rente viagère*. These notes are the citation ground truth for the
frlib `rente_viagere` product documents: source ids S1..S10 and R1..R26 below are frozen —
never renumber.

Access date for all citations: 2026-08-26.

Citation discipline: every extracted fact is tagged `[S#]` or `[R#]` pointing at a document
that was actually fetched and read. `[unverified]` marks statements from general knowledge,
from a secondary summary, or from a primary document that asserts a legal basis the retrieved
text of that legal basis does not contain. Where a fetch failed the failure is recorded and
the item is kept only as a known reference (fetched_ok = false).

French terms of art are kept in French and glossed on first use: *arrérages* (annuity
instalments), *terme échu* (in arrears) vs *terme à échoir* (in advance), *réversion*
(survivor continuation), *annuités garanties* (guaranteed payment period), *rente par paliers*
(stepped annuity), *participation aux bénéfices* (profit sharing), *taux technique* (technical
interest rate priced into the annuity factor), *capital aliéné* / *capital réservé*
(capital alienated / capital reserved, i.e. with a return-of-premium death benefit),
*quittance d'arrérages* (the annuity payment slip, the unit the fee rules bite on).

---

## Primary sources

### S1 — Carac, "Règlement Mutualiste C valant Note d'Information — Rente Viagère Immédiate"
- Publisher: Carac, mutuelle d'épargne, de retraite et de prévoyance, Livre II du Code de la
  mutualité, SIREN 775 691 165
- Doc type: règlement mutualiste valant note d'information, 12 pp.; "Dispositions générales
  en vigueur au 15 novembre 2023"; file reference `RM005 … 16100023_VF`
- URL: https://www.carac.fr/media/rm/RM005_Reglement%20Mutualiste%20Rente%20Viagere%20Immediate_16100023_VF.pdf
- Retrieved: YES (PDF downloaded, full text extracted with `pdftotext -layout`).
- Content: the only genuine **standalone immediate annuity contract** retrieved. Individual
  life operation in euros. Entry ages 50–85 at the effective date, top-up payments allowed up
  to 85 [Art. C5, C8]. Two capitalisation modes: *capital réservé* (a death capital of at least
  70 % of the sums paid in that mode, net of entry charges, plus accrued *bonification*) and
  *capital aliéné* (nothing paid on death, higher annuity) [encadré, Art. C3, C17.1]; a
  *capital réservé* holding may be converted irreversibly to *capital aliéné* at any time to
  raise the annuity, effective the 1st of the month of the request, provided the death
  beneficiaries have not accepted their designation [Art. C15]. Charges: 2,44 % on each
  payment, 0,55 % on the *provisions mathématiques* levied at 31 December, "autres frais:
  néant" [encadré, Art. C9, C10]. Each payment buys a *fraction de rente* effective on the
  1st day of the 3rd month following the payment [Art. C12]. Arrears are paid **semi-annually,
  terme échu, on 30 June and 31 December** [Art. C13]. Optional *réversion* to a spouse, PACS
  partner or cohabitant at **50 %, 60 % or 100 %**, elected at joining only, the reversionary
  beneficiary being aged 50–85 at election, the rate choice definitive and the reduction set by
  a *tarif spécial* under the regulation in force; Carac may refuse the option if it drops the
  annuitant's annuity, or the reversion annuity itself, below **77 € a year** [Art. C16].
  Reversion annuity effective the 1st day following the death [Art. C12]. Uplift is by
  *bonification* set annually by the Conseil d'administration in the management report
  [Art. C11, C18]. **No surrender:** "les rentes viagères immédiates et les rentes viagères en
  cours de service ne peuvent être rachetées" [Art. C3]. Proof of life required by *attestation
  sur l'honneur* on request, failing which payment is suspended [Art. C13]. Arrears accrued but
  unpaid at death go to the heirs if they reach **15 €**; overpayments are recovered at the same
  **15 €** floor [Art. C17.2]. Death capital bears interest from the date of death at a rate no
  lower than the lesser of the 12-month average TME and the last TME available at 1 November of
  the previous year, and must be paid within one month of a complete file [Art. C17.1].
  30 calendar days *renonciation* with full refund within 30 days [Art. C7]. Prescription
  2 years, 10 years where the beneficiary is not the member [Art. C20]. The *encadré* is
  produced under the arrêté du 15 mai 2006. No *annuités garanties*, no *paliers*, no
  dependency option, no indexation option.

### S2 — Suravenir, "SURAVENIR PER — Notice du contrat n° 2240" (Réf. 5257-4, 08.2024)
- Publisher: Suravenir (groupe Crédit Mutuel Arkéa); PDF hosted by the distributor
  assurancevie.com (Puissance Avenir PER)
- Doc type: notice d'information of a group PER, 25 pp.
- URL: https://www.assurancevie.com/assets/files/web/puissance_avenir_per/notice_suravenir_per.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Reference `5257-4 (08.2024)`.
- Content: the richest retrieved description of French annuity **option mechanics**.
  Conversion basis at point 10.d: the annuity is set from (i) the adherent's age, (ii) the
  reversion beneficiary's age where applicable, (iii) the options and parameters chosen,
  (iv) "la table de mortalité des rentiers en vigueur à la date d'effet de la rente", and
  (v) "un taux d'intérêt technique de **0,00 %**". The annuity takes effect on the 1st day of
  the civil month following receipt of the complete file and is "payable par mois civil à
  **terme échu**". Where the annuity falls below the minimum at art. A. 160-2 of the Code des
  assurances, the rights may be liquidated as a single capital payment with the insured's
  agreement. An annual *attestation valant certificat de vie* plus a birth extract under three
  months old must be returned within 30 days or the annuity is suspended from the following
  month. Options (point 10.e) are **not cumulative** and the choice is **irrevocable**:
  *réversion* at any percentage from **1,00 % to 100,00 %** of the annuity reached at the date
  of death, recalculated if the surviving spouse/PACS partner at death is not the one named at
  liquidation or if another entitled party emerges; *annuités garanties* for a term between
  **5 years** and **the adherent's life expectancy at liquidation minus 5 years, capped at
  25 years**, chosen in **5-year steps**, mutually exclusive with reversion, the annuity
  continuing for life with no further beneficiary if the annuitant survives the term;
  *rentes par paliers croissants* — scheme 1: 100 % for a first step of 5 or 10 years then
  **200 %**; scheme 2: 100 %, then **125 %** for an equal second step, then **150 %**;
  *rentes par paliers décroissants* — scheme 1: 100 % then **50 %**; scheme 2: 100 %, then
  **75 %**, then **50 %**. Revalorisation (point 10.f): "Chaque année, au 31 décembre, les
  rentes servies sont majorées de la participation aux bénéfices". Charges: "0,00 % sur
  quittances d'arrérages" but "**Frais sur encours de rentes : 0,80 %**"; accumulation-phase
  annual management charges 0,80 % on euro rights and 0,60 % on unit-linked rights (0,90 %
  under an arbitration mandate). Tax table gives the PER compartment split (see §17) and
  states the **110 € / month** threshold for compartment C3.

### S3 — Suravenir, "Notice du contrat n° 2139 — Puissance Avenir PERP" (Réf. 4833-3, 10/2018)
- Publisher: Suravenir / Association d'Épargne pour la Retraite (AER); PDF hosted by
  assurancevie.com
- Doc type: notice d'information of a PERP (the pre-PACTE individual retirement contract)
- URL: https://www.assurancevie.com/assets/files/web/puissance_avenir_perp/notice_pa_perp.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Reference `4833-3 (10/2018)`.
- Content: the same option architecture as S2 (réversion 1–100 %, *annuités garanties* 5 years
  to life expectancy − 5 capped at 25 in 5-year steps, the four *paliers* schemes), the same
  monthly *terme échu* payment and the same 0 % technical rate, but a **different charging
  structure on the annuity: 0 % on *quittances d'arrérages* and 0,68 % *frais sur encours de
  rente***. It is the only retrieved document that states the annuity profit-sharing mechanism
  in operative terms: "Chaque année, Suravenir établit le compte de participation aux bénéfices
  des rentes en cours de service conformément au point III de l'article A. 132-11 du Code des
  assurances en incluant le résultat technique généré par ces mêmes rentes. La participation aux
  bénéfices attribuée chaque année aux rentes de l'actif isolé du contrat est égale à **100 % du
  solde créditeur du compte de participation aux bénéfices**." Annuities in service for less
  than one year at 1 January are revalorised pro rata temporis from the effective date to
  31 December. Transfer indemnity 2 % within 10 years; inbound transfer charge up to 3,90 %.

### S4 — Spirica, "ASAC-FAPES PER — Conditions Générales valant Notice d'information" (CG9406, 01/10/2022)
- Publisher: Spirica (groupe Crédit Agricole Assurances) for ASAC-FAPES; PDF hosted by gpm.fr
- Doc type: conditions générales valant notice d'information, 34 pp.
- URL: https://www.gpm.fr/wp-content/uploads/2022/12/CONDITIONS_GENERALES_PER_ERES_SPIRICA.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Page footer `CG9406 - 01/10/2022`.
- Content: annuity payable **monthly, quarterly, half-yearly or annually** at the adherent's
  choice; "Aucun frais n'est prélevé sur quittance d'arrérages de Rente et les frais de gestion
  du support de la rente sont de **2,3 % maximum**"; separately, "Les éventuels frais de service
  de la Rente, fixés à **0 %** de chaque montant brut de Rente versée et **plafonnés à 1 % du
  Plafond Mensuel de Sécurité Sociale par arrérage**". Annuity types (7.3.2.2): *rente viagère*;
  *rente viagère réversible* at **50 % to 150 % in 10-point steps**; *rente viagère avec annuités
  garanties*, the number "limité par le nombre d'années d'espérance de vie de l'Adhérent-Assuré,
  à l'effet de la Rente, diminué de 5 ans", the document attributing that limit to art. A. 335-1
  of the Code des assurances; *rente viagère réversible à annuités garanties* with reversion
  **50 % to 100 %** and two ranked beneficiaries; *rente viagère par paliers* where "chacune des
  deux premières périodes de versement est limitée à **10 ans**" and "le nombre de majorations ou
  de diminutions est au maximum de **2**". Pricing inputs (7.3.2.3): the *Valeur Atteinte* net of
  social and tax levies; the dates of birth of the annuitant and reversion beneficiary; the
  mortality table in force at conversion; the option chosen; the periodicity; the number of
  guaranteed annuities; and "le taux d'intérêt technique en vigueur … Le taux maximum est encadré
  par la réglementation en vigueur". The insurer does not guarantee the annuity amount before
  liquidation. Annuities in payment are revalorised "selon le compte de participation aux
  résultats techniques et financiers". Small-annuity commutation is stated under
  **art. A. 160-2-1** of the Code des assurances at **100 € a month** including *majorations
  légales*, the threshold multiplied by the number of months for longer periodicities, with the
  right to group several annuity contracts held with the same insurer to reach it and then to
  choose between *rachat* and *transformation*. Electing the annuity at joining is irrevocable;
  the *versements obligatoires* compartment must be liquidated as an annuity.

### S5 — CNP Assurances / GERP CNP, "Solution Plan Épargne Retraite — Notice d'information"
- Publisher: CNP Assurances, group life contract subscribed by the Groupement Épargne Retraite
  Populaire CNP; PDF mirrored on a third-party site (reassurez-moi.fr)
- Doc type: notice d'information of an individual PER, ~35 pp.
- URL: https://guide.reassurez-moi.fr/guide/wp-content/uploads/2021/02/per_prevoir_cg.pdf
- Retrieved: YES (PDF downloaded, full text extracted). **No document reference code or edition
  date appears in the extracted text**; the mirror was posted in February 2021, so the edition
  is treated as 2020/2021 vintage and anything time-sensitive from it is flagged.
- Content: the CNP source. Annuity charges in the *encadré*: "**Frais sur les rentes servies :
  3 % maximum sur le montant de chaque arrérage**", plus "frais annuels sur encours
  s'appliquant aux capitaux constitutifs de rente : **1 % maximum par an**". "La rente viagère
  est servie **trimestriellement à terme échu**". Capital is converted "selon les bases
  techniques en vigueur au moment de la demande de liquidation". Small annuity: "Avec l'accord
  de l'assuré, si la rente viagère est inférieure à un montant fixé par la réglementation, la
  prestation sera versée sous forme de capital", and the same rule applies to the reversion
  annuity with the *réversataire*'s agreement. *Réversion*: total, or partial at **60 % or
  80 %**; "La décision d'opter ou non pour la réversion, de même que la désignation du
  bénéficiaire sont définitives". **Dependency doubling option**: "L'option doublement de la
  rente viagère en cas de dépendance" may be elected at liquidation, **before the adherent's
  70th birthday**, subject to the insurer's acceptance, and **only where the annuity is
  non-reversible**; "La définition de la dépendance, les conditions tarifaires et la sélection
  médicale sont celles en vigueur à la date de liquidation". Revalorisation is by reference to
  art. 12.2 of the notice.

### S6 — Préfon / CNP Retraite, "Notice d'information du régime de retraite supplémentaire de la Préfon" (application 1 January 2026)
- Publisher: Préfon (souscripteur), CNP Retraite (assureur)
- Doc type: notice d'information of a points-based PER (Préfon-Retraite), 20 pp. + annexes
- URL: https://www.prefon.fr/assets/files/prefon-retraite/notices/notice-d-information-prefon-retraite-2026.pdf
- Retrieved: YES (PDF downloaded, full text extracted). "mise en application au 1er janvier 2026".
- Content: a *régime en points*, so annuity levels move through the *valeur de service du point*
  rather than a *participation aux bénéfices*: "Préfon-Retraite ne prévoit pas de participation
  aux bénéfices contractuelle." Arrears "sont payés **mensuellement à terme échu depuis le
  31 juillet 2023**", starting no earlier than the 1st day of the month following the liquidation
  request, and cease from the 1st day of the month following death. **Rentes non inscriptibles:**
  only annuities of at least **40 € a month (120 € a quarter)** are issued — measured *before*
  reversion and dependency options — otherwise a single capital payment is made with the
  member's agreement recorded on the liquidation request [Art. 5.2.3 b)]. *Réversion* after
  liquidation (Art. 5.4.3) is at **60 %, 80 % or 100 %**, elected at liquidation only and never
  later, payable from the 1st day of the month or quarter following death, to a spouse/PACS
  partner or, failing that, to another named beneficiary but only from age 25; it **definitively**
  reduces the member's own rights, by the following published coefficient table applied to the
  points, keyed on the age difference (by birth-year millésime) between the member and the
  reversionary:

  | Age difference (reversionary vs member) | 60 % | 80 % | 100 % |
  |---|---|---|---|
  | Older by 8 years or more | 0,93 | 0,91 | 0,89 |
  | Older by 4–7 years | 0,89 | 0,86 | 0,83 |
  | Within 3 years either way | 0,81 | 0,76 | 0,72 |
  | Younger by 4–7 years | 0,76 | 0,70 | 0,65 |
  | Younger by 8–15 years | 0,66 | 0,59 | 0,54 |
  | Younger by 16–23 years | 0,58 | 0,51 | 0,45 |
  | Younger by 24–29 years | 0,53 | 0,46 | 0,40 |
  | Younger by 30–34 years | 0,49 | 0,42 | 0,37 |
  | Younger by 35–39 years | 0,47 | 0,40 | 0,35 |
  | Younger by 40–44 years | 0,42 | 0,35 | 0,30 |
  | Younger by 45 years or more | 0,35 | 0,29 | 0,24 |

  **Garantie optionnelle dépendance** (Art. 5.4.4 and Annexe 2): elected irrevocably at
  liquidation by members **aged under 70** who satisfy five health declarations (no prior
  invalidity pension, no inaptitude pension, no 100 % sickness-insurance cover, no hospital stay
  over 15 consecutive days nor sick leave over 3 consecutive months in the last five years, no
  rheumatological/neurological/psychiatric/cardiac/vascular follow-up), otherwise subject to
  medical underwriting; available on the member's own rights only, not on derived rights
  (reversion or orphan allowances). **The dependency annuity "est égale, à tout moment, à la
  rente servie par le régime Préfon-Retraite"** — i.e. the annuity doubles. It is bought by a
  monthly contribution deducted from the annuity: **3 % (liquidation at 55–60), 4 % (61–65),
  5 % (66–70)** of the annuity served; a 12 % loading is taken from those contributions for
  expenses; rates may be revised but never beyond 150 % of their initial cost for existing
  beneficiaries. Dependency is defined by two grids (four ADLs — feeding, dressing, washing,
  moving — scored 1 partial / 2 total, plus a psychiatric grid scored 1 or 2), giving an index
  0–10; **0–5 refused, 6–10 accepted** after medical opinion, and one of three situations must
  hold (cure-section or care-home residence, long-stay hospitalisation, or simultaneous home
  nursing plus a full-time paid third party). Waiting: cover starts at acceptance if dependency
  follows an accident, otherwise **one year** after acceptance and **three years** for mental
  causes; payment begins **6 months after recognition** of dependency (**3 months** if
  accidental) and ceases at the end of the quarter in which dependency ends, or on death.
  Regime charges: 1 % on contributions and inbound transfers, 0,70 % max of technical provisions
  plus 2 % of the net financial income of the PTS assets, "**Il n'y a pas de frais prélevés sur
  les rentes servies, ni sur les capitaux versés**", 1 % transfer indemnity waived after 5 years.

### S7 — La France Mutualiste, "Contrat individuel de rente viagère différée — Retraite Mutualiste du Combattant" (RMCADH0422/D1)
- Publisher: La France Mutualiste (Code de la mutualité)
- Doc type: dossier d'adhésion containing the note d'information valant règlement mutualiste
  and a fiscal annexe
- URL: https://www.la-france-mutualiste.fr/sites/default/files/paragraph/files/2023-01/RMCADH0422-D1%20-%20V2.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Reference `RMCADH0422/D1`, posted 2023-01.
- Content: a deferred-or-immediate annuity contract with a State *majoration*, so a niche
  product, but it states the annuity mechanics that matter here explicitly. The *barème*
  converting each payment into a *fraction de rente* "tient compte … du taux de frais de
  transformation en rente précisé à l'article 17.3, **des tables prospectives de génération et
  du taux d'intérêt technique en vigueur**", and may be changed in-year if the generation tables
  or the technical rate move, "Les règles de modification de ce taux de capitalisation sont
  fixées par arrêté" [Art. 5.3]. Charges: entry 2,10 % below 10 000 €, 1,70 % from 10 000 € to
  under 30 000 €, 1,40 % at 30 000 € and above; 0,50 % a year on managed savings; "**Frais de
  transformation en rente : 3 % de frais sont appliqués sur chaque arrérage de rente**"
  [Art. 17.1–17.3]; 5 % penalty on surrender before the 10th anniversary [Art. 15].
  "**Votre rente est payée trimestriellement à terme échu**"; depending on the liquidation date
  the first instalment covers at least two months of arrears; the board reserves the right to
  change the payment periodicity **including for annuities already in payment** [Art. 6.3].
  Arrears accrued and unpaid at death are due to the heirs; an overpayment at death is owed by
  the estate [Art. 7.3]. Profit sharing: "Le compte de participation annuel aux excédents
  comprend au moins **85 %** du solde du compte financier", allocated by the board annually to
  the personal annuity and, under the *capitaux réservés* regime, to the reserved capital
  [encadré §3–4, Art. 16]. *Capitaux réservés* may be alienated at or after liquidation to buy
  a deferred survivor annuity for a spouse aged at least 50, effective the 1st of the month
  following death, irreversible once the endorsement takes effect, and void if the spouse dies
  or a separation/divorce begins within 6 months [Art. 10]. Fiscal annexe: the annuity above the
  *plafond majorable* is taxed under the *rente viagère à titre onéreux* rules with an abatement
  of **50 % (age 50–59), 60 % (60–69), 70 % (70 and over)** by age at *entrée en jouissance*;
  social levies at 1 January 2022 CSG 9,2 %, CRDS 0,5 %, prélèvement de solidarité 7,5 %
  (**17,2 %** total).

### S8 — AG2R La Mondiale, "Rente Universelle — une rente viagère pour compléter vos revenus"
- Publisher: AG2R La Mondiale
- Doc type: product web page (marketing), not a notice d'information
- URL: https://www.ag2rlamondiale.fr/rente-viagere
- Retrieved: YES (web page).
- Content: a currently marketed standalone immediate annuity. **Minimum capital 30 000 €**;
  minimum annuity **40 € a month**; instalments "mensuels, trimestriels, semestriels ou annuels";
  the decision is "irréversible". Options named: *réversion* from **5 % to 100 %**, a *réversion
  majorée* up to **200 %**, *annuités garanties* (durations not stated), a *capital décès*, and a
  dependency guarantee that doubles the income on recognised dependency. *Frais d'arrérage* are
  named without a figure. RVTO taxation is described with the 70/50/40/30 taxable fractions.
  The page does **not** mention *réversion croisée*, *rente par paliers*, *rente indexée*,
  a maximum subscription age, or whether arrears are *terme échu* or *terme à échoir*.

### S9 — CRH / C.G.O.S, "Guide Infos 2025" (Complément Retraite des Hospitaliers), pages 26–28
- Publisher: Comité de Gestion des Œuvres Sociales des établissements hospitaliers publics
  (C.G.O.S) for the CRH régime
- Doc type: member guide (flipbook HTML pages)
- URL: https://crh.cgos.info/flipbook-guide-info-retraite/files/basic-html/page27.html
  (pages 26 and 28 also fetched)
- Retrieved: YES (pages 26, 27, 28).
- Content: a second points-based régime, useful because it publishes both a reversion cost table
  and the guaranteed-period cap. *Réversion* at **60 %, 80 % or 100 %** with corresponding
  coefficients on the member's own annuity of **92,5 %, 90 % and 87,5 %**. *Annuités garanties*:
  "la durée des annuités garanties : est fixée à **25 ans au maximum**", and additionally may not
  exceed life expectancy less five years on the generational mortality tables. "Les arrérages
  sont payables **trimestriellement à terme échu**." Age coefficients applied to the annuity run
  from **75 %** (under 45 to 51) through **100 %** (60–67) to **107,5 %** (70 and over). Where the
  reversion entitlement falls below 500 points a lump sum equal to the net present value of the
  insurer's commitments is paid instead. Page 26 does not cover mortality tables, technical
  rate, fees or revalorisation; page 28 covers death benefits only.

### S10 — Allianz France, "Contrats de rente viagère" (espace client guide)
- Publisher: Allianz France
- Doc type: product guide page
- URL: https://espaceclient.allianz.fr/pmt/guide/Retraites.STANDARD/Contrats_de_rente_viagere_18.html
- Retrieved: **NO — HTTP 403 Forbidden on two successive attempts.** Kept as a known reference
  only; no content from Allianz is cited anywhere in these notes.

---

## Regulatory and actuarial references

### R1 — Arrêté du 1er août 2006 portant homologation des tables de mortalité pour les rentes viagères et modifiant certaines dispositions du code des assurances
- Publisher: Ministère de l'économie, des finances et de l'industrie (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000820127 (also fetched as
  https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000820127)
- Retrieved: YES (both the JORF and the LODA consolidated views).
- Content: five articles plus annexed tables. **Article 2 verbatim:** "Les tables prévues au
  quatrième alinéa de l'article A. 335-1 du code des assurances pour les contrats de rente
  viagère sont à compter du 1er janvier 2007 : — la table **TGF05** ci-annexée concernant les
  assurés de sexe féminin ; — la table **TGH05** ci-annexée concernant les assurés de sexe
  masculin." Article 3 annexes the two tables to art. A. 335-1. Article 1 makes fourteen
  numbered amendments to the Code des assurances (including creating art. A. 335-1-1 on the
  *décalages d'âge*) and replaces the earlier generation table homologated by the arrêté du
  28 juillet 1993 (the "TPG 1993"). Article 4 brings points 3° and 10° of article 1 into force
  on 1 January 2007. **Explicitly checked and absent:** the arrêté contains no rule about
  *annuités garanties* and no "life expectancy minus five years" limit.

### R2 — Code des assurances, article A. 335-1 (version in force 21/12/2012 – 01/01/2016; article now abrogated)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000026806627
- Retrieved: YES. Legifrance banner: "Version en vigueur du 21/12/2012 au 01/01/2016", last
  modified by "Arrêté du 18 décembre 2012 - art. 2", and the article is marked **ABROGÉ** in the
  section table of contents.
- Content: the historic tariff article that the arrêté du 1er août 2006 [R1] amends and that
  insurer documents [S4] still cite. Its text is materially the same as the current
  art. A. 132-18 [R3]. **Important for citation hygiene:** the brief's premise that TGH05/TGF05
  are mandated "via art. A. 335-1" is historically correct but no longer the live reference; the
  live reference is art. A. 132-18. The exact abrogating instrument and date were not confirmed
  from the retrieved page, and there is an unexplained gap between 01/01/2016 and the creation
  of A. 132-18 on 07/09/2017 — [unverified].

### R3 — Code des assurances, article A. 132-18 (in force since 07/09/2017)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514715
- Retrieved: YES (full verbatim text). "Version en vigueur depuis le 07/09/2017", modified by
  "Arrêté du 14 août 2017 - art. 1".
- Content: the operative tariff article. Tariffs of life insurers, capitalisation undertakings
  and *fonds de retraite professionnelle supplémentaire* comprise the undertaking's remuneration
  and are built from **1°** a technical interest rate fixed under art. A. 132-1, and **2°** one of
  two table families: **a)** tables homologated by ministerial arrêté, established by sex, "sur la
  base de populations d'assurés pour les contrats de rente viagère, et sur la base de données
  publiées par l'INSEE pour les autres contrats"; **b)** tables built by the undertaking, with or
  without sex, and "certifiées par un actuaire indépendant de cette entreprise, agréé à cet effet
  par l'une des associations d'actuaires reconnues par l'autorité mentionnée à l'article
  L. 310-12", based on the undertaking's own experience data or demographically equivalent data.
  Then the three operative constraints:
  - **the unisex rule** — "Lorsque les tarifs sont établis d'après des tables mentionnées au a, et
    dès lors qu'est retenue une table unique pour tous les assurés, celle-ci correspond à la table
    appropriée conduisant au **tarif le plus prudent**";
  - the *décalages d'âge* correction for non-annuity survival contracts;
  - **the experience-table floor for annuities** — "Pour les contrats de rentes viagères, en ce
    compris celles revêtant un caractère temporaire, et à l'exception des contrats relevant du
    chapitre III du titre IV du livre Ier, le tarif déterminé en utilisant les tables mentionnées
    au b ne peut être inférieur à celui qui résulterait de l'utilisation des tables appropriées
    mentionnées au a."
  A forfaitary method is allowed for annually cancellable group death contracts.

### R4 — Code des assurances, article A. 132-1 (in force since 07/09/2017)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514601
- Retrieved: YES (text retrieved, partly as summary rather than full verbatim).
- Content: the maximum *taux technique*. Tariffs must be built on a rate at most equal to **75 %
  of the average rate of French State borrowings (TME) computed on a half-yearly basis**, and
  beyond **eight years** may not exceed the lower of **3,5 %** and **60 % of that average**. For
  periodic-premium or variable-capital contracts the lower of 3,5 % and 60 % applies whatever the
  duration. Foreign-currency contracts follow equivalent rules on the relevant long-term
  government rates with the same 60 % cap beyond eight years. The applicable rate is the one at
  subscription; the article does not apply to the collective operations of Book IV. **The
  retrieved text contains no rule written specifically for *rentes viagères***, and no mention of
  a "taux mensuel de référence" or of a 0,25-point scale — those live in A. 132-1-1 [R5].

### R5 — Code des assurances, article A. 132-1-1 (created by arrêté du 26 décembre 2019 art. 4, in force 01/01/2020)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801948
- Retrieved: YES.
- Content: the mechanics that turn the TME into a usable ceiling. The **taux de référence
  mensuel** is the arithmetic mean of State borrowing rates observed on the primary and secondary
  markets over the preceding six months, multiplied by **60 % or 75 %**. "Le taux d'intérêt
  technique maximal applicable aux tarifs est fixé sur une échelle de taux d'origine 0 et de pas
  de **0,25 point**, sans descendre en-dessous de 0." The maximum is sticky: it only moves when
  the reference rate falls by at least **0,10 point** or rises by at least **0,35 point**, and
  then moves to the next rate down on the 0,25-point scale; undertakings have **three months** to
  implement a change.

### R6 — Code des assurances, article A. 132-3 (version 07/09/2017)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514611
- Retrieved: YES (retrieved as a structured summary rather than full verbatim).
- Content: caps on rates and profit-sharing that may be guaranteed **in advance**. Guaranteed
  rates may not exceed the lower of **150 % of the maximum technical rate** and the higher of
  **120 % of the maximum technical rate** and **110 % of the average rates credited to
  policyholders over the two preceding financial years**; newly authorised undertakings may
  guarantee up to 120 % of the maximum technical rate until the end of the second financial year
  after authorisation. Guaranteed profit-sharing is capped by the difference between **80 %** of
  (two-year average asset return × mathematical provisions) and the technical interest credited
  in the prior year. Guaranteed rates must be fixed for at least **six months** and at most until
  the end of the following financial year.

### R7 — Code des assurances, Section V "Participation aux bénéfices techniques et financiers", articles A. 132-10 to A. 132-17
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000031738019/
  and https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038714192/2019-07-01 (A. 132-11)
- Retrieved: YES (section listing and A. 132-11; content returned as summary, not full verbatim).
- Content: the minimum profit-sharing machinery. The minimum *participation aux bénéfices* for a
  financial year is determined globally from a **compte de participation aux résultats**
  (art. A. 132-11), fed by the underwriting elements of the relevant insurance categories, by
  **85 % of the balance of a financial account**, by the reinsurance balance, and by any deficit
  carried forward; the insurer retains as its own share of the technical result the **greater of
  10 % of the credit balance and 4,5 % of annual premiums** [the exact wording of this last clause
  was returned as a paraphrase, not verbatim — **[unverified]** as to precise formulation].
  Art. A. 132-16 carries the eight-year rule: "Les sommes portées à cette dernière provision sont
  affectées à la provision mathématique ou versées aux souscripteurs au cours des **huit
  exercices** suivant celui au titre duquel elles ont été portées". Point III of art. A. 132-11 is
  the paragraph a PERP/PER insurer uses to build a separate profit-sharing account for annuities
  in payment [S3].

### R8 — Code des assurances, article L. 132-23
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038837141
- Retrieved: YES. Version in force since 14 June 2026, created/amended by LOI n° 2026-492 du
  12 juin 2026 - art. 3.
- Content: **the no-surrender rule, verbatim:** "Les assurances temporaires en cas de décès ainsi
  que les rentes viagères immédiates ou en cours de service ne peuvent comporter ni réduction ni
  rachat." The article then lists the exceptional early-release cases for retirement contracts
  (exhaustion of unemployment benefit after involuntary job loss; cessation of a non-salaried
  activity after judicial liquidation; 2nd- or 3rd-category invalidity; serious illness,
  disability or severe accident affecting a dependent child; death of a spouse or PACS partner;
  over-indebtedness; and cases determined by the president of a commercial court).

### R9 — Code des assurances, article L. 160-5
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006793993
- Retrieved: YES (full verbatim).
- Content: "Nonobstant toutes dispositions contractuelles contraires, les entreprises d'assurance
  sur la vie peuvent, dans les conditions et suivant un barème fixé par arrêté du ministre de
  l'économie et des finances, procéder à la transformation ou au rachat des rentes qu'elles ont
  constituées et dont les quittances d'arrérages sont d'un montant inférieur à un montant minimal
  fixé par ledit arrêté." The statute fixes no figure; it delegates both the schedule and the
  threshold to an arrêté [R10].

### R10 — Code des assurances, Section IV "Rachat par les entreprises d'assurance sur la vie des rentes inférieures à un certain montant minimal", articles A. 160-2, A. 160-2-1 (abrogated), A. 160-3, A. 160-4
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000006173957/
- Retrieved: YES (section listing with per-article version banners).
- Content: **A. 160-2** (version in force since **22/07/2023**, from the **arrêté du 17 juillet
  2023**): insurers may buy back annuities, with the beneficiary's consent, where "les quittances
  d'arrérages mensuelles ne dépassent pas **110 euros**, en y incluant le montant des majorations
  légales"; "Lorsque les quittances d'arrérages sont versées selon une périodicité de paiement
  supérieure à un mois, le seuil mentionné au premier alinéa est **multiplié par le nombre de mois
  inclus dans la période de paiement**." **A. 160-2-1** was the PER-specific twin, in force
  **01/07/2021 – 22/07/2023**, with a **100 euros** monthly threshold and the same periodicity
  multiplier; it is now **abrogated**, the two regimes having been merged into A. 160-2 at
  110 euros. **A. 160-3** (since 01/01/2016): the buy-back barème values the annuity on the
  mathematical provision computed with the tables and interest rates of the **règlement ANC
  n° 2015-11 du 26 novembre 2015**. **A. 160-4** (since 12/08/2019): several annuity contracts held
  with the same insurer may be grouped to reach the threshold, and the beneficiary then chooses
  between *rachat* and *transformation*.

### R11 — Arrêté du 20 décembre 2005 relatif aux tables de mortalité
- Publisher: Ministère de l'économie (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000636581
- Retrieved: YES.
- Content: homologates **TH00-02** (male) and **TF00-02** (female) for contracts other than
  annuities, and sets the framing sentence later carried into A. 335-1 / A. 132-18: tables are
  "établies par sexe, sur la base de populations d'assurés pour les contrats de rente viagère, et
  sur la base de données publiées par l'INSEE pour les autres contrats". In force 1 January 2006,
  with the last paragraph of art. 2 (V) and art. 2 (VI) applying from 1 July 2006. Article 2
  allows undertakings to build tables from their own or demographically equivalent experience
  data under supervisory oversight; the retrieved text does not mention independent actuarial
  certification (that requirement appears in the later A. 335-1 / A. 132-18 wording).

### R12 — Code des assurances, Annexe (9) à l'article A. 335-1 — table TGF05
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019266402/2019-05-24
- Retrieved: YES (structure only; the numeric table was not extracted).
- Content: the annexed **TGF05** table as published in the Code. Ages **0 to 120**; survivors
  indexed to 100 000 at the generation's entry age; the fetched fragment showed the 1966–1976
  generation columns with dashes below age 20. Legifrance marks this annexe article "Abrogé par
  Arrêté du 28 décembre 2015" with effect from 1 January 2016 — consistent with the abrogation of
  A. 335-1 [R2] and with the tables having been re-annexed elsewhere. **The library does not
  redistribute TGH05/TGF05 values.**

### R13 — Code général des impôts, article 158 (paragraphs 5-a and 6)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042158853/2020-07-25
- Retrieved: YES.
- Content: **art. 158, 6** — *rentes viagères à titre onéreux* (RVTO) are taxable only on a
  fraction of each instalment, fixed once and for all by the beneficiary's age at *entrée en
  jouissance*: **70 %** under 50; **50 %** from 50 to 59 inclusive; **40 %** from 60 to 69
  inclusive; **30 %** over 69. (The corresponding *abattements* are 30 / 50 / 60 / 70 %.) The
  paragraph excludes annuities arising from contributions that took a specified monetary-code
  option. **art. 158, 5-a** — pensions and *rentes viagères à titre gratuit* get a **10 %**
  abatement, capped at **3 850 €** per household and floored at **393 €** (not exceeding the
  gross pension).

### R14 — BOFiP, BOI-RSA-PENS-30-20 — "Rentes viagères à titre onéreux"
- Publisher: Direction générale des Finances publiques
- URL: https://bofip.impots.gouv.fr/bofip/369-PGP.html/identifiant=BOI-RSA-PENS-30-20-20170711
- Retrieved: YES.
- Content: the administrative doctrine that fixes the RVTO fraction in practice. The taxable
  fractions are the four bands of CGI art. 158, 6. The **date d'entrée en jouissance** is, for an
  immediate annuity, the contract date or the date the funds are handed over; for a deferred
  annuity, the date payments actually begin, not the theoretical contractual date. For an annuity
  set up on two or more heads with survivorship, "l'âge à retenir pour le calcul de la fraction
  imposable de la rente est, en principe, celui du **plus jeune**", **except** for spousal
  reversions, where the **elder spouse's age** is used throughout — both during joint lives and
  after the first death — as the more favourable treatment; if the annuity later passes to a third
  party, that party's age at first receipt applies. Where the annuity is later topped up, each new
  tranche takes its own fraction based on the age at the date of that tranche.

### R15 — BOFiP, BOI-RSA-PENS-10-40 — "Rentes viagères à titre gratuit ou à titre onéreux"
- Publisher: Direction générale des Finances publiques
- URL: https://bofip.impots.gouv.fr/bofip/366-PGP.html/identifiant=BOI-RSA-PENS-10-40-20140502
- Retrieved: YES.
- Content: the boundary between the two regimes. A *rente à titre gratuit* is granted without
  consideration; a *rente à titre onéreux* is granted against a capital payment or a transfer of
  movable or immovable property. Both fall inside CGI art. 79; only the onerous kind gets the
  attenuated art. 158, 6 treatment. The doctrine lists as **onerous**: annuities from the sale of
  real estate or a business, **annuities served by insurance companies against a capital**,
  *rentes-survie* for disabled children, FONPEL/CAREL elected-official pensions, and annuities
  awarded as a divorce indemnity.

### R16 — CJUE, affaire C-236/09, Association belge des Consommateurs Test-Achats ASBL e.a., 1 March 2011
- Publisher: Court of Justice of the European Union (EUR-Lex / Curia)
- URL: https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX:62009CJ0236
- Retrieved: **NO — the EUR-Lex PDF endpoint returned an empty body.** Curia's case page was not
  fetched. Kept as a known reference. Its substance is carried here only through the French
  ministerial answers [R17][R18] and a media summary [R25], and every statement about the
  judgment's operative wording is therefore tagged **[unverified]**.

### R17 — Assemblée nationale, question écrite n° 41093 (Véronique Louwagie, 21 September 2021) and ministerial answer (28 December 2021)
- Publisher: Assemblée nationale / Ministère de l'économie, des finances et de la relance
- URL: https://questions.assemblee-nationale.fr/q15/15-41093QE.htm
- Retrieved: YES.
- Content: the clearest official statement of how France applies unisex pricing to annuities.
  The deputy's premise (her claim, not the ministry's): insurers generalised the **female table
  TGF05** to both sexes after the unisex requirement, penalising men by about **15 %**. The
  ministry's answer: insurers may use either the regulatory tables or certified experience tables
  under **art. A. 132-18** of the Code des assurances; a 2011 CJEU ruling struck down the
  sex-based derogation in directive 2004/113/CE; the **loi du 26 juillet 2013** on the separation
  and regulation of banking activities amended **art. L. 111-7** of the Code des assurances to
  prohibit sex-based discrimination; using TGF05 generates technical surpluses that must be
  returned to policyholders in substantial part **within eight years**, the answer citing
  art. A. 132-11 (the eight-year rule itself is at art. A. 132-16 [R7] — the discrepancy is noted
  and not resolved); and the government "does not intend to undertake regulatory work on this
  subject".

### R18 — Assemblée nationale, question écrite n° 14295 (Jean-Carles Grelier) and ministerial answer
- Publisher: Assemblée nationale / Ministère de l'économie
- URL: https://questions.assemblee-nationale.fr/q15/15-14295QE.htm
- Retrieved: YES.
- Content: the same question one legislature earlier. The deputy's claim: insurers applied the
  female table to both sexes after the non-discrimination requirement took effect on
  **20 December 2012**, disadvantaging men by up to **20 %**. The answer cites directive
  2004/113/CE, the CJEU ruling of **1 March 2011**, the French law of 26 July 2013,
  art. L. 111-7, art. A. 132-18 (permitted tables) and art. A. 132-11 (surplus redistribution),
  states that since 2012 unisex pricing operates through "mutual solidarity" on life-expectancy
  differences, and declines regulatory intervention.

### R19 — Institut des actuaires / Frédéric Planchet (WINTER & Associés / ISFA), "Tables TGH / TGF 05 : Construction", réunion du 22 mars 2007
- Publisher: Institut des actuaires (document posted on institutdesactuaires.com; the slide
  footer reads "CONFIDENTIEL", but the file is served publicly from the Institute's site)
- URL: https://www.institutdesactuaires.com/global/gene/link.php?doc_id=242&fg=1
- Retrieved: YES (PDF downloaded, 16 slides, full text extracted).
- Content: how the two mandatory annuity tables were actually built.
  **Data:** annuitant observations from **19 portfolios** (16 from the FFSA, 3 from the CTIP),
  covering roughly **700 000 liquidated annuities** and about 2 million records over
  **1993–2005**; per-life fields were sex, birth date (day-of-month excluded), liquidation date,
  joining date, exit date and exit cause; contract-level fields were collected but not used.
  **Reference:** because the sample was small for a prospective table, the experience mortality
  was *positioned* against an external reference — a set of INSEE historic and prospective period
  tables built from the 1962–2000 period tables (Serant [2005]) with a cubic-spline logit model
  with knots at ages 20, 28, 40, 80 and 90, the time series then treated Lee-Carter fashion to
  extrapolate the surface.
  **Graduation:** raw rates by **Kaplan-Meier**, pre-smoothed by a locally-Gompertz smoother of
  amplitude 5 years, then a logit-on-logit regression against the reference for each age
  **40–95** over **1994–2004**, constrained by `a_x = α + β·b_x` because a and b proved strongly
  correlated. Below age 40 there was **no data at all**: the INSEE structure was imposed over
  0–40 and joined to the market tables at 40 with a C1 condition, which pins the parameters
  uniquely.
  **Projection:** rates projected **2005–2100**; the raw extrapolation implied insured mortality
  above general-population mortality from 2015, judged implausible, so the logit gap was forced
  to converge to the national table.
  **Closure:** above age 95 the logits are extended quadratically with a C1 join at 95 and
  q = ½ at a **drifting pivot age** `x_p = a·t + b` fitted by least squares over ages 85–95 —
  the first attempt, fixing q = ½ at age 110, produced crossing rates.
  **Adjustments:** at the ACAM's request male death rates were **increased by 1 % from ages 60 to
  94**, described as immaterial for residual life expectancies. The construction rules make male
  projected rates fall below female rates in some cells; the impact on reserving was judged
  negligible. The tables provide rates where **age + generation > 1995**.
  **Results (residual life expectancy at age 60):** men — **26,8 years** for the 1936 generation
  rising to **36,7 years** for the 2005 generation (+37 %), with male annuitants aged 60 in 2006
  (generation 1946) at **28,4 years**; women — **30,6 years** (1936) to **40,4 years** (2005,
  +32 %), with female annuitants aged 60 in 2006 at **32,0 years**. The superseded TPG 1993 gave
  **29,6 years** at 60 for both.

### R20 — ACPR, Analyses et Synthèses n° 66, "Le taux technique en assurance vie (Code des assurances)" (Pierre-Emmanuel Darpeix, 2016)
- Publisher: Autorité de contrôle prudentiel et de résolution / Banque de France
- URL: https://acpr.banque-france.fr/sites/default/files/medias/documents/201606_as66_le_taux_technique_en_assurance_vie.pdf
  (landing page: https://acpr.banque-france.fr/fr/publications-et-statistiques/publications/ndeg-66-le-taux-technique-en-assurance-vie-code-des-assurances)
- Retrieved: **NO from the ACPR — both the PDF and the landing page returned HTTP 403 on two
  successive attempts.** The abstract was retrieved from the RePEc mirror
  https://ideas.repec.org/p/bfr/analys/66.html (Retrieved: YES).
- Content (abstract only): the technical rate is a fundamental contractual parameter, used for
  pricing but in life insurance generally functioning as "a minimum guaranteed return rate for the
  entire contract duration". Since 1995 the regulatory maximum is referenced to the average rate of
  French government borrowing. Findings reported in the abstract: by end-2014 average technical
  rates were well below the then legal ceiling; zero-technical-rate contract families dominate in
  every commercialisation year, with wide insurer-to-insurer variation; successive surveys show a
  downward trend; contracts with high technical rates correlate with large net outflows or with
  rate reductions. The body of the paper — including anything it says specifically about *rentes
  viagères* — was **not read**.

### R21 — Addactis, "Taux techniques Vie et non Vie" (running tracker)
- Publisher: Addactis (actuarial software and consulting firm) — **secondary source**
- URL: https://www.addactis.com/fr/blog/taux-techniques-vie-non-vie/
- Retrieved: YES.
- Content: the current published values of the ceiling computed under R4/R5. As at **31 July 2026**:
  **maximum technical rate 2,00 %**, monthly reference TME **3,90 %**; page last updated
  **1 August 2026**. The page states the 60 %-of-six-month-average construction and the
  0,25-point scale, and does **not** break the ceiling out by contract duration or premium type.
  Because this is a commercial tracker rather than an official publication, the 2,00 % figure is
  usable as an order of magnitude but should be re-derived from the TME before being relied on.

### R22 — Arrêté du 7 décembre 2012 portant majoration de certaines rentes viagères
- Publisher: Ministère de l'économie (Légifrance, LODA consolidated to 29/04/2018)
- URL: https://www.legifrance.gouv.fr/loda/id/LEGITEXT000026768614/2018-04-29
- Retrieved: YES.
- Content: the *majorations légales* machinery that A. 160-2 [R10] tells insurers to include when
  testing the small-annuity threshold. Made under the loi n° 48-957 du 9 juin 1948 (veterans'
  annuities through mutual societies), the loi n° 49-420 du 25 mars 1949 (revision of certain
  annuities between private parties), the loi n° 51-695 du 24 mai 1951 and art. 126 of the loi de
  finances pour 2000 (n° 99-1172). It sets a **1,75 %** uplift of the majoration rates for
  annuities paid in **2013** and carries a coefficient table keyed on the year the original annuity
  originated, running from **104 537,90** for annuities originating before 1 August 1914 down to
  **1,75** for 2011 (e.g. **11 048,20** for 1939–1940). These are State-funded uplifts of legacy
  annuities; they are **not** the ordinary commercial revalorisation of a modern annuity.

### R23 — MoneyVox, "Rentes viagères : quelle différence entre frais d'arrérage et frais de gestion ?" (2 April 2015)
- Publisher: MoneyVox (personal-finance press) — **secondary source, and dated**
- URL: https://www.moneyvox.fr/placement/actualites/51409/rentes-viageres-quelle-difference-entre-frais-arrerage-et-frais-de-gestion
- Retrieved: YES.
- Content: the market picture of annuity charging that the retrieved contracts corroborate.
  *Frais d'arrérage* are taken on each instalment, "typically around **3 %** of the gross annuity",
  with Axa quoted as charging a flat **2–5 € per instalment** on the Cler contract distributed by
  Agipi. *Frais de gestion du fonds de rente* run about **0,60 %–0,90 %** a year on the annuity
  fund. Named examples: Apicil **0,75 % encours + 3 % on service**; Suravenir **0,68 % encours and
  0 % on arrears for PERP, 0 % encours and 3 % on arrears for assurance vie**. The Suravenir PERP
  figure is independently confirmed verbatim by [S3]. All other figures here are press-reported
  and **[unverified]**.

### R24 — UFC-Que Choisir Var-Est, "La rente viagère avec des frais d'arrérage et frais de gestion"
- Publisher: UFC-Que Choisir (consumer association local branch) — **secondary source**
- URL: https://www.ufc-quechoisir-var-est.org/la-rente-viagere-avec-des-frais-darrerage-et-frais-de-gestion/
- Retrieved: YES.
- Content: a republication of the same 2 April 2015 material. Useful for one point: the
  terminology itself is not standardised — "frais sur arrérages de rentes", "frais de quittances"
  and "frais de gestion sur arrérages" all denote the same deduction, which is why a model has to
  read each contract's own definition rather than a market label.

### R25 — MoneyVox, "Table de calcul des rentes viagères TGF05 et TGH05"
- Publisher: MoneyVox — **secondary source**
- URL: https://www.moneyvox.fr/retraite/tables-mortalite-tgf05-tgh05.php
- Retrieved: YES.
- Content: describes TGF05/TGH05 as INSEE-built prospective generation tables covering
  **generations 1900–2005** and **ages 0–120**, introduced by the arrêté of 1 August 2006 and
  mandatory from 1 January 2007, insurers being free instead to use certified experience tables
  that are at least as prudent; and states that after the 2012 European decision, contracts signed
  **after 20 December 2012** must use the female table where no mixed table exists. It further
  claims that a 2023 law introduced a unified mortality table for collective retirement plans with
  effect from 24 October 2024 — **[unverified]**; no legal instrument for that claim was retrieved,
  though it would be consistent with the carve-out for "contrats relevant du chapitre III du titre
  IV du livre Ier" in art. A. 132-18 [R3]. The page reproduces survivor rows for three sample
  generations; **none of those figures is used or reproduced here**.

### R26 — Kos Avocats, "Pas de discrimination entre les tables TGH et TGF !" (6 July 2023)
- Publisher: Kos Avocats (law firm blog) — **secondary source**
- URL: http://kos-avocats.fr/blog/2023/07/06/pas-de-discrimination-entre-les-tables-tgh-et-tgf/
- Retrieved: **NO — the page was returned truncated and no substantive content could be read.**
  Kept as a known reference: it is a commentary on a French decision about applying TGF05 to male
  annuitants. Nothing from it is cited.

---

## Extracted specifications

### 1. Product structure and legal form
- The contract is the exchange of a **capital constitutif** for a stream of *arrérages* payable
  while the annuitant lives. It arises in three settings, and the mechanics differ only at the
  edges:
  1. **Standalone *contrat de rente viagère immédiate*** — a single-premium life operation, e.g.
     Carac's Rente Viagère Immédiate [S1] under the Code de la mutualité, or AG2R La Mondiale's
     Rente Universelle [S8].
  2. **Exit of a retirement wrapper** — PER, PERP, Madelin or a points régime; the annuity is
     bought with the *valeur de transfert* / *valeur atteinte* at liquidation [S2][S3][S4][S5][S6][S9].
  3. **Exit of an *assurance vie*** — the *sortie en rente* option; the contract's accumulated
     value is converted on the insurer's *bases techniques* of the day. No retrieved primary
     document covers this route directly, so the assurance-vie-specific mechanics are
     **[unverified]** here; the pricing and payment mechanics of §4–§13 are common to all three.
- **Legal capacity of the option once taken.** Every retrieved contract makes the choice
  irrevocable at liquidation: options "ne sont pas cumulatives et … le choix est irrévocable"
  [S2 pt 10.e][S3 pt 11.d]; "ce choix est irrévocable" for an annuity elected at joining
  [S4 §7.3]; "La décision d'opter ou non pour la réversion, de même que la désignation du
  bénéficiaire sont **définitives**" [S5]; "Le choix de la rente de réversion est irréversible"
  and "Cette option est irréversible" for alienation of reserved capital [S1 Art. C15, C16];
  the reversion election "ne pourra pas l'être ultérieurement" [S6 Art. 5.4.3]; "irréversible"
  [S8].
- **Capital aliéné vs capital réservé.** French practice distinguishes the annuity bought with
  capital **alienated** (nothing returns on death, higher annuity) from capital **reserved**
  (a death capital of at least **70 %** of the sums paid in that mode net of entry charges,
  plus accrued uplift, lower annuity) [S1 encadré, Art. C3, C17.1][S7 encadré §2]. Reserved
  capital can be alienated later to raise the annuity, effective the 1st of the month of the
  request, but only while the death beneficiaries have not accepted their designation, and the
  conversion is irreversible [S1 Art. C15][S7 Art. 9–10]. This is the French analogue of a
  return-of-premium/*contre-assurance* annuity and is a genuine second product shape, not a rider.

### 2. Regulatory pricing basis — mortality tables
- The tariff of a French life insurer is built from a technical rate plus **one** of two table
  families [R3, verbatim]:
  - **(a) homologated tables**, by sex, "sur la base de populations d'assurés pour les contrats de
    rente viagère" — i.e. **annuitant-experience** tables for annuities, INSEE population data for
    everything else;
  - **(b) the undertaking's own tables**, by sex or not, built from its own or demographically
    equivalent experience data and **certified by an actuary independent of the undertaking**,
    accredited by an actuarial association recognised by the ACPR (art. L. 310-12).
- **The homologated annuity tables are TGH05 (male) and TGF05 (female)**, applicable to
  *contrats de rente viagère* **from 1 January 2007** [R1 art. 2, verbatim]. They replaced the
  generation table homologated by the arrêté du 28 juillet 1993 ("TPG 1993") [R1]. **TH00-02 /
  TF00-02**, homologated by the arrêté du 20 décembre 2005 and in force from 1 January 2006, are
  the non-annuity tables built on INSEE data [R11] and are *not* used to price an annuity.
- **Table nature and coverage.** TGH05/TGF05 are prospective **generation** tables: a rate depends
  on age *and* year of birth. Published coverage is ages **0–120**, generations **1900–2005**
  [R25, secondary]; the construction document states the tables give rates where
  **age + generation > 1995** [R19]. Residual life expectancy at 60 from the tables: men 26,8
  (generation 1936) → 36,7 (2005), 28,4 for a 60-year-old male annuitant in 2006; women 30,6 →
  40,4, 32,0 for a 60-year-old female annuitant in 2006; TPG 1993 gave 29,6 for both [R19].
- **Construction, in one line for the modeller:** annuitant experience from 19 French portfolios
  (700 000 annuities, 1993–2005), Kaplan-Meier raw rates, locally-Gompertz pre-smoothing, logit
  positioning against an INSEE spline/Lee-Carter prospective reference over ages 40–95 and years
  1994–2004, projection to 2100 forced to converge on national mortality, quadratic logit closure
  above 95 with a drifting pivot at q = ½, and a flat **+1 % on male rates from age 60 to 94** at
  the supervisor's request [R19].
- **The experience-table floor.** For *rentes viagères*, including temporary ones, and excluding
  contracts under chapter III of title IV of book I, "le tarif déterminé en utilisant les tables
  mentionnées au b ne peut être inférieur à celui qui résulterait de l'utilisation des tables
  appropriées mentionnées au a" [R3, verbatim]. An insurer may use its own certified table but may
  never price an annuity *cheaper* than the regulatory table would. This one-sided floor is the
  single most important structural fact about French annuity pricing.
- What the retrieved contracts actually say they use: "la table de mortalité des rentiers en
  vigueur à la date d'effet de la rente" [S2][S3]; "La table de mortalité en vigueur, au moment de
  la transformation" [S4]; "les tables prospectives de génération" [S7 Art. 5.3]; "les bases
  techniques en vigueur au moment de la demande de liquidation" [S5]. **No retrieved primary
  product document names TGH05 or TGF05 explicitly** — the table is always referenced generically.

### 3. Unisex application of TGH05/TGF05
- The rule inside the tariff article: "Lorsque les tarifs sont établis d'après des tables
  mentionnées au a, et dès lors qu'est retenue une **table unique pour tous les assurés**,
  celle-ci correspond à la **table appropriée conduisant au tarif le plus prudent**"
  [R3, verbatim]. For an annuity the most prudent table is the one with the lower mortality, i.e.
  the **female table TGF05**. That is the mechanism by which unisex pricing operates in France:
  the regulation does not create a unisex table, it forces the single table used to be the more
  prudent of the two sex-specific ones.
- Chain of authority as stated by the ministry [R17][R18]: directive 2004/113/CE → CJEU ruling of
  **1 March 2011** (case C-236/09, *Test-Achats*) striking down the sex-based derogation →
  **loi du 26 juillet 2013** (separation and regulation of banking activities) amending
  **art. L. 111-7** of the Code des assurances to prohibit sex-based discrimination in premiums
  and benefits.
- **Effective date — handle carefully.** The brief's date of **21 December 2012** is the date on
  which the derogation in art. 5(2) of directive 2004/113/CE ceased to have effect under the
  judgment; the retrieved French sources render it as contracts concluded "après le **20 décembre
  2012**" [R18][R25] and one deputy's question refers loosely to "une directive du 21 décembre
  2012" [R17]. **The judgment itself was not retrieved [R16]**, so the exact operative wording and
  the precise cut-off convention are **[unverified]**; "new contracts concluded from 21 December
  2012" and "contracts after 20 December 2012" are the same rule stated two ways, and the model
  should not depend on the boundary day.
- **Consequence the ministry acknowledges:** applying TGF05 to men produces a systematic technical
  surplus, which must in substantial part be returned to policyholders within **eight years**
  [R17] — i.e. it flows back as *participation aux bénéfices* rather than being retained. Deputies
  quantified the male disadvantage at **~15 %** [R17] and "up to **20 %**" [R18]; both are the
  questioners' assertions, not the ministry's, and are **[unverified]**.
- Contracts written under the **Code de la mutualité** (Carac [S1], La France Mutualiste [S7]) sit
  under a parallel arrêté (the arrêté du 8 décembre 2006 relatif aux tables de mortalité
  applicables aux mutuelles was located but **not fetched**) — **[unverified]** as to whether its
  table rules are identical.

### 4. Regulatory pricing basis — taux technique
- **Ceiling.** Tariffs must use a rate at most **75 % of the TME** (average rate of French State
  borrowings, half-yearly basis); beyond **eight years** the rate may not exceed the **lower of
  3,5 % and 60 % of that average**; for periodic-premium or variable-capital contracts the lower
  of 3,5 % and 60 % applies regardless of duration [R4]. The rate that binds is the one in force
  at subscription [R4].
- **Mechanics of the ceiling** [R5]: the *taux de référence mensuel* is the arithmetic mean of
  State borrowing rates on the primary and secondary markets over the preceding six months,
  multiplied by 60 % or 75 %. The maximum technical rate then sits on a scale with **origin 0 and
  step 0,25 point, never below 0**; it moves only when the reference rate falls by ≥ **0,10 point**
  or rises by ≥ **0,35 point**, and undertakings get **three months** to apply the change.
- **A lifetime immediate annuity is unambiguously a "beyond eight years" contract**, so the binding
  ceiling is `min(3,5 %, 60 % × TME_6m)` rounded down onto the 0,25-point ladder. **[unverified]**
  as an inference — no retrieved document states it in those words for annuities specifically, and
  R4's retrieved text contains no annuity-specific paragraph.
- **Current level:** maximum technical rate **2,00 %** with monthly reference TME **3,90 %** as at
  31 July 2026 [R21, secondary tracker].
- **What insurers actually use.** Two retrieved PER/PERP notices price at **0,00 %**
  [S2 pt 10.d][S3 pt 11.e]. Others say only that the rate in force at conversion applies and that
  "Le taux maximum est encadré par la réglementation en vigueur" [S4 §7.3.2.3], or that the barème
  reflects "le taux d'intérêt technique en vigueur" and may be revised in-year when market rates
  move materially, "Les règles de modification de ce taux de capitalisation sont fixées par arrêté"
  [S7 Art. 5.3]. Carac indexes the reserved-capital percentage to "la variation du taux minimum
  d'intérêt technique" [S1 Art. C1]. The ACPR's own finding is that zero-technical-rate contract
  families dominate every commercialisation cohort [R20, abstract only].
- **Related ceiling on guaranteed rates** [R6]: a guaranteed rate may not exceed the lower of 150 %
  of the maximum technical rate and the higher of (120 % of the maximum technical rate, 110 % of
  the average rates credited over the two preceding years); guarantees must run at least six months
  and at most to the end of the following financial year. This bounds any *taux minimum garanti*
  layered on top of the annuity's technical rate.

### 5. Charges on the annuity
Three distinct deductions exist, and every retrieved contract uses one, two or none of them:
- **Frais d'arrérages** — a percentage of each *quittance d'arrérages*:
  - **3 % maximum on each instalment** — CNP Assurances [S5 encadré: "Frais sur les rentes servies :
    3 % maximum sur le montant de chaque arrérage"].
  - **3 % on each instalment** — La France Mutualiste, styled *frais de transformation en rente*
    [S7 Art. 17.3].
  - **0,00 %** — Suravenir PER and PERP [S2][S3], Spirica [S4], Préfon [S6: "Il n'y a pas de frais
    prélevés sur les rentes servies, ni sur les capitaux versés"], Carac [S1 encadré: "Autres frais:
    néant"].
  - AG2R names *frais d'arrérage* without a figure [S8].
  - Market range reported in the press: around 3 %, or a flat **2–5 € per instalment** at one
    insurer [R23][R24, both secondary and dated 2015].
- **Frais sur encours de rentes** — an annual charge on the annuity fund:
  - **0,80 %** — Suravenir PER [S2]; **0,68 %** — Suravenir PERP [S3]; **1 % maximum a year** on
    the *capitaux constitutifs de rente* — CNP [S5]; **2,3 % maximum** on the annuity support —
    Spirica [S4]; **0,55 %** on *provisions mathématiques* at 31 December — Carac [S1 Art. C9];
    **0,50 %** a year on managed savings — La France Mutualiste [S7 Art. 17.2]; **0,70 % maximum**
    of technical provisions plus 2 % of the net financial income of the PTS — Préfon [S6 Art. 12].
  - Press range for the annuity-fund charge: **0,60 %–0,90 %** [R23, secondary].
- **A cap expressed in social-security units.** Spirica caps any annuity-service fee at
  **1 % of the Plafond Mensuel de Sécurité Sociale per instalment** while setting the rate itself
  at 0 % [S4 §7.3.2.3]. This is the only ceiling of that shape found.
- **Terminology is not standardised** — "frais sur arrérages de rentes", "frais de quittances",
  "frais de gestion sur arrérages" and "frais de transformation en rente" all denote a deduction
  from the instalment [R24]. A model must read the contract, not the label.
- **Entry charges on the capital** (where the annuity is bought directly): 2,44 % per payment
  [S1]; 2,10 % / 1,70 % / 1,40 % by payment size band [S7 Art. 17.1]; 1 % on contributions [S6].
- **No public conversion-rate cards.** No retrieved document publishes a *taux de rente* or an
  annuity factor table. AG2R publishes only a minimum capital and a minimum monthly annuity [S8].
  Spirica states explicitly that "L'Assureur ne garantit pas le montant de la Rente avant la
  liquidation sous forme de rente" [S4 §7.3.2.3]. **A drafter must treat every conversion rate as
  `[std]`.**

### 6. Payment frequency and timing
- **Frequencies observed:** monthly [S2][S3][S6]; quarterly [S5][S7][S9]; semi-annually [S1];
  monthly / quarterly / half-yearly / annual at the annuitant's choice [S4][S8].
- **Timing: every single retrieved document pays *terme échu* (in arrears).**
  "payable par mois civil à terme échu" [S2][S3]; "payés mensuellement à terme échu depuis le
  31 juillet 2023" [S6]; "servie trimestriellement à terme échu" [S5]; "payée trimestriellement à
  terme échu" [S7 Art. 6.3]; "payables trimestriellement à terme échu" [S9]; "payés
  semestriellement et à terme échu" [S1 Art. C13]. **No retrieved French document offers a
  *terme à échoir* option.** This is a real structural difference from the UK market, where advance
  and arrears are both standard, and the model should treat *terme échu* as the base case and
  *terme à échoir* as an unobserved variant.
- **First instalment.** The annuity takes effect on the 1st day of the civil month following
  receipt of the complete file [S2][S3]; no earlier than the 1st day of the month following the
  liquidation request [S6]; a purchased *fraction de rente* takes effect on the 1st day of the
  3rd month following payment [S1 Art. C12]. La France Mutualiste states the first instalment
  "représente au moins deux mois d'arrérages" depending on the liquidation date [S7 Art. 6.3] —
  i.e. a stub, not a proportionate reduction.
- **Fixed calendar payment dates** are used by some mutuelles: 30 June and 31 December [S1 Art. C13].
- **Cessation.** Instalments "cessent d'être dus à compter du premier jour du mois qui suit le décès"
  [S6]. Arrears accrued but unpaid at death belong to the heirs, and overpayments are recovered
  from the estate [S1 Art. C17.2][S7 Art. 7.3]; Carac applies a **15 €** de-minimis in both
  directions [S1].
- **Periodicity may be changed unilaterally.** La France Mutualiste's board "se réserve le droit de
  modifier la périodicité des paiements des rentes, **y compris pour les rentes en cours de
  service**" [S7 Art. 6.3].
- **Proof of life is a payment condition.** An annual *attestation valant certificat de vie* plus a
  birth extract under three months old must be returned within **30 days**, failing which service
  is suspended from the following month until it arrives [S2][S3]; Carac requires an *attestation
  sur l'honneur* on request, "À défaut, le paiement de la rente est suspendu" [S1 Art. C13];
  La France Mutualiste may condition payment on a proof of life [S7 Art. 6.3].

### 7. Option — réversion
- **Available reversion rates, by insurer:**

  | Insurer | Rates offered | Notes |
  |---|---|---|
  | Suravenir (PER and PERP) | any % from **1 % to 100 %** | of the annuity *reached at the date of death* [S2][S3] |
  | Spirica — simple reversible | **50 % to 150 % in 10-point steps** | [S4 §7.3.2.2] |
  | Spirica — reversible with guaranteed annuities | **50 % to 100 %** | two ranked beneficiaries [S4] |
  | CNP Assurances | total (100 %), or **60 % / 80 %** | decision and designation "définitives" [S5] |
  | Préfon-Retraite | **60 % / 80 % / 100 %** | with a published coefficient table, §S6 above |
  | CRH / C.G.O.S | **60 % / 80 % / 100 %** | coefficients 92,5 % / 90 % / 87,5 % [S9] |
  | Carac | **50 % / 60 % / 100 %** | reversionary must be 50–85 at election [S1 Art. C16] |
  | AG2R La Mondiale | **5 % to 100 %**, plus a *réversion majorée* to **200 %** | [S8] |

  The commonly quoted "60 % / 100 %" pair in the brief is real but incomplete: **60 %** appears in
  five of the eight, **100 %** in all eight, and continuous ranges (1–100 %, 5–100 %,
  50–150 % in steps) are as common as discrete menus.
- **Cost of the option.** Where it is published, the reduction is a coefficient on the annuitant's
  own annuity, keyed on the **age difference** between annuitant and reversionary and on the
  reversion rate — see the Préfon table in [S6] (0,93 down to 0,24) and the CRH coefficients
  (92,5 % / 90 % / 87,5 %) [S9]. Carac says only that the reduction follows "un tarif spécial
  établi selon la réglementation en vigueur" [S1 Art. C16].
- **Beneficiary rules.** Spouse, PACS partner or cohabitant [S1]; spouse/PACS partner by default,
  another named person otherwise but served only from age 25 [S6]; "un bénéficiaire désigné selon
  son choix, ou à défaut à son conjoint ou partenaire de Pacs" [S2].
- **Recalculation on a change of spouse.** Suravenir: if the surviving spouse or PACS partner at
  death is not the one named at liquidation, "le montant de la rente sera recalculé pour tenir
  compte de l'âge du bénéficiaire au jour du décès", and likewise if another entitled party emerges
  [S2][S3]. This is a live option the reserving model has to notice.
- **Reversion effective date.** 1st day following death [S1 Art. C12]; 1st day of the month or
  quarter following death [S6].
- **Reduction is definitive even if the reversionary predeceases** — "Le choix de la réversion
  implique une réduction définitive, même si le bénéficiaire de la réversion vient à décéder
  antérieurement à l'Affilié(e)" [S6 Art. 5.4.3].
- **A de-minimis on the option itself:** Carac may refuse reversion if it would drop either the
  annuitant's annuity or the reversion annuity below **77 € a year** [S1 Art. C16].
- **Réversion croisée** (mutual cross-reversion between two annuitants) is named in the brief but
  appears in **no retrieved document** — **[unverified]**; AG2R's *réversion majorée* to 200 % is
  the closest retrieved analogue [S8].

### 8. Option — annuités garanties (guaranteed payment period)
- **Duration rule, corroborated by three independent primary documents:**
  minimum **5 years**; maximum the lesser of **25 years** and **the annuitant's life expectancy at
  the effective date of the annuity minus 5 years**; chosen in **5-year steps**
  [S2 pt 10.e][S3 pt 11.d][S4 §7.3.2.2][S9]. The brief's "10, 15, 20 years" menu is consistent with
  the 5-year-step rule but is not itself the published menu in any retrieved document.
- **Legal basis of the "life expectancy minus 5 years" cap: [unverified].** Spirica attributes it to
  **art. A. 335-1 of the Code des assurances** [S4], but the retrieved text of A. 335-1 in its
  2012–2016 version [R2], the retrieved text of its successor A. 132-18 [R3], and the fourteen
  amending points of the arrêté du 1er août 2006 [R1] all **explicitly do not contain it**. The
  cap is real market practice with an unlocated legal source; a drafter should present it as
  observed practice, not as a cited statutory rule.
- **Mechanics.** The insurer pays the annuity to the annuitant and, on death within the term, to
  the definitively and irrevocably designated beneficiary or beneficiaries for the balance of the
  term; the instalments continue at the same amount as the annuitant's own [S2][S3][S4]. If the
  annuitant survives the term, "le versement de la rente se poursuit jusqu'à son décès, sans autre
  bénéficiaire d'annuités garanties, ni de réversion possible" [S2][S3].
- **Mutual exclusivity.** At Suravenir the options "ne sont pas cumulatives" — reversion, guaranteed
  annuities and stepped annuities cannot be combined [S2][S3]. Spirica by contrast sells a combined
  *rente viagère réversible à annuités garanties* with a first-rank and a second-rank beneficiary,
  reversion capped at 100 % in that combination [S4]. This is a genuine design fork.
- **Commutation of the remaining guaranteed instalments to a lump sum is not offered by any
  retrieved French contract** — unlike the UK market, the balance is paid as continuing
  instalments. **[unverified]** as a market-wide statement.
- Carac offers no guaranteed period at all; its death protection is the *capital réservé* instead
  [S1].

### 9. Option — rente par paliers (stepped annuity)
Two published designs, both stated in full:
- **Suravenir** [S2 pt 10.e][S3 pt 11.d] — four fixed schemes, the first step always 5 or 10 years:
  - increasing, scheme 1: **100 % → 200 %**;
  - increasing, scheme 2: **100 % → 125 % (equal second step) → 150 %**;
  - decreasing, scheme 1: **100 % → 50 %**;
  - decreasing, scheme 2: **100 % → 75 % (equal second step) → 50 %**.
- **Spirica** [S4 §7.3.2.2] — free-form: the amount is increased or decreased relative to a first
  period; "Chacune des deux premières périodes de versement est limitée à **10 ans**"; "Le nombre
  de majorations ou de diminutions est au maximum de **2**"; the coefficients and the period lengths
  are chosen by the annuitant at conversion.
Both are level-within-step step functions on a single life, not escalation. Carac, CNP, Préfon,
CRH, La France Mutualiste and AG2R do **not** offer stepped annuities in the retrieved documents.

### 10. Option — rente dépendance (doubling on dependency)
- **CNP Assurances** [S5]: "L'option doublement de la rente viagère en cas de dépendance",
  electable at liquidation, **before the annuitant's 70th birthday**, subject to the insurer's
  acceptance, and **only where the annuity is non-reversible**. The definition of dependency, the
  pricing conditions and the medical selection are those in force at liquidation — i.e. **not fixed
  by the contract**.
- **Préfon-Retraite** [S6 Art. 5.4.4 and Annexe 2] — the only retrieved document that publishes the
  whole rider:
  - eligibility: **under 70** at liquidation, on the member's own rights only (not on reversion or
    orphan annuities), automatic acceptance on five negative health declarations, medical
    underwriting otherwise;
  - **benefit: an additional annuity "égale, à tout moment, à la rente servie par le régime" — the
    total annuity doubles**;
  - **price: a monthly contribution deducted from the annuity of 3 % (liquidation at 55–60), 4 %
    (61–65), 5 % (66–70) of the annuity served**, with a **12 %** expense loading taken from those
    contributions, revisable but never beyond **150 %** of the initial cost for existing
    beneficiaries;
  - **definition**: a 4-ADL grid (feeding, dressing, washing, moving) scored 1 partial / 2 total,
    plus a psychiatric grid scored 1 (partial supervision) or 2 (constant supervision and
    assistance), giving an index 0–10 — **0–5 refused, 6–10 accepted** after medical opinion — plus
    one of three qualifying situations (cure-section/care-home residence, long-stay
    hospitalisation, or simultaneous prescribed home nursing and a full-time paid third party);
  - **waiting periods:** cover effective at acceptance if dependency follows an **accident**,
    otherwise **1 year** after acceptance, and **3 years** for mental causes; **payment starts
    6 months after recognition of dependency (3 months if accidental)**;
  - **cessation:** end of the quarter in which dependency ceases, or death;
  - exclusions: intentional self-harm, non-prescribed narcotics, civil or foreign war, atomic
    explosions and radiation, racing/matches/betting other than normal sporting competition.
- **AG2R La Mondiale** [S8]: a dependency guarantee that doubles the income; no figures published.
  A search summary attributed a **2 500 € per month** dependency cap and an "18 annuity options"
  count to AG2R, but neither appears in the fetched page — **[unverified]**.
- Carac, Suravenir, Spirica, La France Mutualiste and CRH offer no dependency option in the
  retrieved documents.

### 11. Option — indexation, and what French annuities do instead
- **No retrieved French contract offers a contractual index-linked annuity.** There is no RPI/CPI
  escalation option, no LPI equivalent, and no fixed-percentage escalation clause anywhere in
  S1–S9. The uprating mechanism is **discretionary profit-sharing** (§12), not indexation.
- The two indexation-shaped features that do exist are unrelated to inflation-linked pricing:
  - the *majoration d'État* and *revalorisation d'État* attached to the Retraite Mutualiste du
    Combattant, which are statutory and product-specific [S7 encadré §2, Art. 3];
  - the **majorations légales de rentes viagères** under the loi n° 49-420 du 25 mars 1949 and
    successors, uprated by arrêté — 1,75 % for annuities paid in 2013, with coefficients from
    104 537,90 (pre-1914 origin) to 1,75 (2011 origin) [R22]. These apply to legacy annuities and
    must be **included when testing the small-annuity threshold** [R10 art. A. 160-2].
- Consequently a French annuity model needs a **discretionary uplift** mechanism, not an escalation
  parameter. Where a project needs an escalating French annuity, it is a **[std]** construction.

### 12. Revalorisation of the annuity in payment
- **Statutory frame.** The minimum profit-sharing for a financial year is set globally from a
  *compte de participation aux résultats* which is credited with **85 % of the balance of the
  financial account** plus the underwriting elements and the reinsurance balance, the insurer
  retaining the greater of 10 % of the technical credit balance and 4,5 % of annual premiums
  [R7 art. A. 132-11 — the retained-share wording is a paraphrase, **[unverified]**]. Amounts placed
  in the *provision pour participation aux bénéfices* must be transferred to the *provision
  mathématique* or paid to policyholders **within the eight financial years** following the year of
  allocation [R7 art. A. 132-16, verbatim].
- **How it reaches the *arrérages* — the operative sentence** [S3, verbatim]: "Chaque année,
  Suravenir établit le compte de participation aux bénéfices des **rentes en cours de service**
  conformément au point III de l'article A. 132-11 du Code des assurances **en incluant le résultat
  technique généré par ces mêmes rentes**. La participation aux bénéfices attribuée chaque année aux
  rentes de l'actif isolé du contrat est égale à **100 % du solde créditeur** du compte de
  participation aux bénéfices." The annuity's own mortality surplus (including the TGF05 prudence
  margin of §3) therefore flows back into the annuity, not into shareholders' funds.
- **Timing and pro-rating.** "Chaque année, au 31 décembre, les rentes servies sont majorées de la
  participation aux bénéfices" [S2 pt 10.f]. Annuities in service for less than one year at
  1 January are revalorised pro rata from the effective date to 31 December [S3].
- **Other formulations retrieved:** revalorisation "selon le compte de participation aux résultats
  techniques et financiers" [S4 §7.3.2.3]; annual *bonification* rates set by the board in the
  management report and adopted by the general meeting [S1 Art. C11, C18]; "Le compte de
  participation annuel aux excédents comprend au moins **85 %** du solde du compte financier",
  allocated annually by the board to the annuity and to the reserved capital [S7 encadré §3–4].
- **A points régime has no contractual profit-sharing at all:** "Préfon-Retraite ne prévoit pas de
  participation aux bénéfices contractuelle. La revalorisation des droits s'opère selon les règles
  [du régime]" — the annuity moves with the *valeur de service du point* [S6].
- **Modelling consequence.** The uplift is discretionary, annual, non-negative in every retrieved
  formulation, and applied to the annuity in payment. It is not a guaranteed escalation and must be
  a scenario input, not a contractual parameter.

### 13. No surrender, and the small-annuity commutation
- **The statutory rule** [R8, verbatim]: "Les assurances temporaires en cas de décès ainsi que les
  **rentes viagères immédiates ou en cours de service ne peuvent comporter ni réduction ni rachat**."
  Carac restates it in the contract: "Conformément au Code de la mutualité, les rentes viagères
  immédiates et les rentes viagères en cours de service ne peuvent être rachetées" [S1 Art. C3].
  This is the *aliénation du capital*: once the annuity is liquidated the capital is gone and there
  is no surrender value at any duration.
- **The one exception — commutation of a small annuity.** Art. L. 160-5 lets an insurer, "nonobstant
  toutes dispositions contractuelles contraires", transform or buy back annuities whose *quittances
  d'arrérages* fall below a minimum fixed by arrêté [R9, verbatim]. The current figure:
  - **110 € a month**, "en y incluant le montant des majorations légales", under **art. A. 160-2**
    in the version in force since **22 July 2023** (arrêté du 17 juillet 2023) [R10];
  - for longer payment periodicities the threshold is **multiplied by the number of months in the
    payment period** — so 330 € a quarter, 660 € a half-year, 1 320 € a year [R10];
  - **art. A. 160-2-1**, the PER-specific twin at **100 € a month** in force 1 July 2021 to
    22 July 2023, is now **abrogated**, the two regimes having been merged [R10];
  - the buy-back barème values the annuity on the **provision mathématique** computed with the
    tables and interest rates of the **règlement ANC n° 2015-11 du 26 novembre 2015**
    [R10 art. A. 160-3];
  - several annuity contracts held with the same insurer may be **grouped** to reach the threshold,
    the beneficiary then choosing between *rachat* and *transformation* [R10 art. A. 160-4].
- **How contracts implement it.** "Lorsque le montant de la rente est inférieur au minimum défini à
  l'article A. 160-2 du code des assurances, la liquidation des droits pourra, **avec l'accord de
  l'assuré**, s'effectuer sous la forme d'un versement unique en capital" [S2]; the same at [S3];
  "si la rente viagère est inférieure à un montant fixé par la réglementation, la prestation sera
  versée sous forme de capital", including for the reversion annuity with the *réversataire*'s
  agreement [S5]; Spirica reproduces the whole A. 160-2-1 text with the 100 € figure and the
  grouping right [S4]; Suravenir's PER tax table gives **110 € / mois** as the only route to a
  capital exit from the *versements obligatoires* compartment [S2].
- **Régime-specific floors that are not the statutory one:** Préfon issues only annuities of at
  least **40 € a month (120 € a quarter)**, measured **before** reversion and dependency options,
  and pays a single sum otherwise with the member's agreement recorded on the liquidation request
  [S6]; AG2R's product minimum is **40 € a month** [S8]; CRH pays a lump sum where a reversion
  entitlement falls below **500 points**, equal to the net present value of the insurer's
  commitments [S9]; Carac's option-level floor is **77 € a year** [S1].
- **Before liquidation the position is different.** A deferred annuity contract under the *capitaux
  réservés* regime can be surrendered while the liquidation date has not been reached, with a 5 %
  penalty before the 10th anniversary [S7 encadré §5, Art. 15]. Retirement wrappers have the
  statutory early-release cases listed in art. L. 132-23 [R8]. None of this survives liquidation.

### 14. Death benefits other than reversion and guaranteed annuities
- **Capital réservé** [S1 Art. C17.1][S7 Art. 7.2]: on death, a capital of at least **70 %** of the
  sums paid under that mode, net of entry charges and plus accrued uplift, is paid to the named
  beneficiaries; the percentage is set by the general meeting or the board by delegation and only
  payments made after a change are affected [S1 Art. C1]. The death capital bears interest from the
  date of death at a rate at least equal to the lower of the 12-month TME average and the last TME
  available at 1 November of the previous year, must be paid within one month of a complete file,
  and thereafter bears double the legal rate for two months and then triple [S1 Art. C17.1].
- **Réinvestissement option** [S1 Art. C17.1]: the reserved capital may be reinvested into another
  Carac guarantee in the beneficiary's name with no entry charge if elected within **3 months** of
  payment (except into the Plan Obsèques, where entry charges stand).
- **Aliénation of the reserved capital into a survivor annuity** [S7 Art. 10]: at or after
  liquidation, the reserved capital may be converted into a deferred annuity for a spouse aged at
  least 50, effective the 1st of the month following death, co-signed by the spouse, irreversible
  once the endorsement takes effect, and void if within 6 months the spouse dies or a separation or
  divorce begins.
- **Prorata d'arrérages.** Arrears accrued and unpaid at death go to the heirs; an overpayment is
  owed by the estate [S1 Art. C17.2][S7 Art. 7.3]; Carac's **15 €** de-minimis applies both ways
  [S1].

### 15. Eligibility and size limits
| Item | Value | Source |
|---|---|---|
| Minimum capital, standalone annuity | **30 000 €** | AG2R [S8] |
| Entry age band, standalone annuity | **50–85** at the effective date; top-ups to 85 | Carac [S1 Art. C5, C8] |
| Minimum age for *entrée en jouissance* | **50** | Carac [S1 Art. C12] |
| Reversionary's age at election | **50–85** | Carac [S1 Art. C16] |
| Minimum monthly annuity issued | **40 € / month (120 € / quarter)** | Préfon [S6]; AG2R [S8] |
| Statutory commutation threshold | **110 € / month** incl. *majorations légales* | [R10] |
| Maximum age for the dependency option | under **70** at liquidation | CNP [S5]; Préfon [S6] |
| Renonciation period | **30 calendar days**, full refund within 30 days | Carac [S1 Art. C7]; LFM [S7 encadré §1] |
| Prescription | **2 years**, **10 years** where the beneficiary is not the member | Carac [S1 Art. C20] |
No retrieved document states a maximum annuity, a maximum capital, or a residence requirement other
than Carac's requirement of French tax domicile under CGI art. 4 B [S1 Art. C2].

### 16. Taxation of the annuity
- **Rente viagère à titre onéreux (RVTO)** — the regime for an annuity bought with a capital,
  including an annuity served by an insurer against a capital [R15]. Only a fraction of each
  instalment is taxable, fixed once and for all by the annuitant's age at *entrée en jouissance*
  [R13 CGI art. 158, 6]:

  | Age at entrée en jouissance | Taxable fraction | Abattement |
  |---|---|---|
  | Under 50 | **70 %** | 30 % |
  | 50 to 59 inclusive | **50 %** | 50 % |
  | 60 to 69 inclusive | **40 %** | 60 % |
  | 70 and over ("plus de 69 ans") | **30 %** | 70 % |

  Corroborated independently by [S7 fiscal annexe] (which quotes the 50/60/70 % abattements for the
  three upper bands) and [S8].
- **Fixing the age** [R14]: for an **immediate** annuity the reference date is the contract date or
  the date the funds are handed over; for a **deferred** annuity it is the date payments actually
  begin, not the theoretical contractual date. The fraction is then fixed for the life of the
  annuity.
- **Reversion and the fraction** [R14]: for an annuity on two or more heads with survivorship the
  age used is **in principle that of the younger**; **for spousal reversions the elder spouse's age
  applies throughout**, both during joint lives and after the first death, as the more favourable
  treatment; if the annuity later passes to a third party, that party's age at first receipt
  applies. Each later top-up tranche takes its own fraction at the age of that tranche.
- **Rente viagère à titre gratuit (RVTG)** — an annuity granted without consideration, and the
  regime for retirement annuities funded by **deducted** contributions. Taxed as a pension under
  CGI art. 79 after the **10 % abattement** of art. 158, 5-a, capped at **3 850 €** per household
  and floored at **393 €** [R13][R15]. Préfon's fiscal annexe states it directly: arrears
  corresponding to contributions deducted under CGI art. 163 quatervicies are taxed "dans les mêmes
  conditions que les pensions et rentes viagères visées à l'article 79 du CGI … après application
  … de l'abattement spécifique de 10 % prévu à l'article 158-5-a"; where contributions were **not**
  deducted, the arrears are taxed under the RVTO regime of art. 158, 6 [S6 annexe fiscale, A.1 and
  C.1].
- **The PER splits on compartment, not on product** [S6 annexe fiscale][S2 tax table]:
  compartment C1 (deducted voluntary payments) → RVTG; C1bis (non-deducted voluntary payments) →
  RVTO; C3 / *versements obligatoires* → RVTG and annuity-only, with a capital exit permitted only
  where the instalment is below **110 € / month** [S2].
- **Social levies** [S6 annexe fiscale III]:
  - **replacement-income rates** (RVTG): CSG at the normal rate **8,3 %**, median **6,6 %**, reduced
    **3,8 %** or exempt; CRDS **0,5 %** or exempt; CASA **0,3 %** or exempt (art. L. 14-10-4 of the
    Code de l'action sociale et des familles);
  - **investment- and asset-income rates** (RVTO): CSG **9,2 %** + CRDS **0,5 %** + solidarity levy
    = **17,20 %** total, applied **to the taxable fraction only** ("En fonction de l'âge de
    liquidation (cf. article 158-6 du CGI …), une fraction de la prestation versée est assujettie
    aux prélèvements sociaux");
  - Suravenir's table gives **10,1 %** for RVTG arising from the *versements obligatoires*
    compartment and **17,2 %** on the taxable fraction for RVTO [S2].
  - La France Mutualiste states the same 17,2 % as CSG 9,2 % + CRDS 0,5 % + solidarity 7,5 % at
    1 January 2022 [S7].
- **Not verified here:** the tax treatment of converting an *assurance vie* into an annuity (whether
  accumulated gains are taxed at conversion) — **[unverified]**; no retrieved document covers it.

### 17. Reserving and supervisory pointers
- The buy-back of a small annuity is valued on the **provision mathématique** computed with the
  tables and interest rates of the **règlement ANC n° 2015-11 du 26 novembre 2015**
  [R10 art. A. 160-3] — the closest thing retrieved to a statement of the French statutory reserve
  basis for annuities in payment.
- The technical rate priced at issue functions in practice as a lifetime minimum guaranteed return
  [R20, abstract]; combined with the TGF05 prudence margin (§3) and the 100 %-of-surplus
  profit-sharing on the isolated annuity asset pool (§12), the French annuity is structurally a
  **prudently priced, profit-shared** liability rather than a hard-guaranteed one.
- Charges taken from the annuity fund (§5) reduce the profit-sharing base, not the guaranteed
  annuity, in every retrieved contract.
- The Solvency II layer (best-estimate technical provisions, risk margin, SCR) is a cross-product
  matter and belongs in `references/regulatory-and-actuarial-references.md`; nothing product-specific
  to annuities was retrieved for it here.

### 18. Published conversion rates
- **There are none.** No retrieved document publishes a *taux de rente*, an annuity factor, an
  age-by-age conversion table, or a specimen annuity for a specimen capital. AG2R publishes only a
  minimum capital (30 000 €) and a minimum instalment (40 €/month) [S8]. Spirica states the annuity
  is not guaranteed before liquidation [S4]. Préfon and CRH publish **points** machinery — age
  coefficients (CRH: 75 % at under-45–51, 100 % at 60–67, 107,5 % at 70+ [S9]) and reversion
  coefficients (§7) — but the *valeur de service du point* itself is set annually and was not
  retrieved.
- The only quantitative anchors available to a drafter are therefore: the mandatory table family
  (TGH05/TGF05, most-prudent-single-table rule), the technical-rate ceiling
  (`min(3,5 %, 60 % × TME_6m)` on a 0,25-point ladder; 2,00 % as at 31 July 2026 [R21]), the
  observed pricing rate (0,00 % at two insurers [S2][S3]), and the charge levels of §5.
  **Everything else about the conversion rate must be `[std]`.**

---

## Variations across insurers

| Feature | Carac RVI [S1] | Suravenir PER/PERP [S2][S3] | Spirica PER [S4] | CNP PER [S5] | Préfon-Retraite [S6] | AG2R Rente Universelle [S8] |
|---|---|---|---|---|---|---|
| Product shape | standalone immediate annuity (mutuelle) | PER / PERP exit | PER exit | PER exit | points régime, PER-eligible | standalone immediate annuity |
| Minimum capital / annuity | set by the board; option floor 77 €/yr | statutory A. 160-2 floor | statutory floor (100 € text, pre-2023) | "montant fixé par la réglementation" | 40 €/month issue floor | 30 000 € capital; 40 €/month |
| Entry ages | **50–85** | not stated | not stated | not stated | régime rules; dependency < 70 | not stated |
| Payment frequency | **semi-annual only** (30 Jun / 31 Dec) | **monthly** | monthly / quarterly / half-yearly / annual | **quarterly** | **monthly** (since 31/07/2023) | monthly / quarterly / half-yearly / annual |
| Timing | terme échu | terme échu | terme échu | terme échu | terme échu | not stated |
| Technical rate | "taux minimum d'intérêt technique" referenced, not published | **0,00 %** | in force at conversion, capped by regulation | bases techniques of the day | points régime | not published |
| Frais d'arrérages | **néant** | **0,00 %** | **0 %**, capped at 1 % PMSS | **3 % max per instalment** | **none** | named, no figure |
| Frais sur encours de rente | **0,55 %** on PM | **0,80 %** (PER) / **0,68 %** (PERP) | **2,3 % max** on the annuity support | **1 % max/yr** on capitaux constitutifs | 0,70 % max on provisions + 2 % of PTS income | not published |
| Réversion | 50 / 60 / 100 %; reversionary 50–85; floor 77 €/yr | **1–100 %**, recalculated on change of spouse | **50–150 %** in 10-pt steps (50–100 % with guarantees) | 100 % / 80 % / 60 % | 60 / 80 / 100 % with published coefficients | **5–100 %**, *majorée* to **200 %** |
| Annuités garanties | **none** | 5 yrs → min(25, e−5), 5-yr steps, XOR reversion | ≤ e−5; combinable with reversion | not offered | not offered | offered, durations not published |
| Rente par paliers | none | **4 fixed schemes** (200 / 125-150 / 50 / 75-50) | free-form, ≤ 2 steps, each ≤ 10 yrs | none | none | none |
| Rente dépendance | none | none | none | **doubling**, before 70, non-reversible only | **doubling**, 3/4/5 % of the annuity by age band | doubling, no figures |
| Death benefit other than the above | **capital réservé ≥ 70 %** of net payments | none | none | none | garantie décès / réversion machinery | *capital décès* |
| Revalorisation | annual *bonification* set by the board | PB at 31 Dec; PERP: **100 % of the PB account credit balance** incl. annuity technical result | *compte de participation aux résultats* | art. 12.2 of the notice | **no contractual PB**; *valeur de service du point* | annual, on the euro fund's return |

**Representative design for a reference implementation.** The cleanest representative is the
**Suravenir** annuity [S2][S3]: single premium; **monthly, terme échu**; priced on the annuitant's
age, the reversionary's age, the annuitant-experience generation table in force at the effective
date, and an explicit technical rate (0,00 % as published); a mutually exclusive option set of
*réversion* (1–100 % of the annuity reached at death), *annuités garanties* (5 years to
min(25, life expectancy − 5), in 5-year steps) and four fixed *paliers* schemes; **no surrender**;
statutory commutation below the art. A. 160-2 floor; annual discretionary uplift at 31 December
from a profit-sharing account built on the annuities in payment including their own technical
result; and a charge structure of 0 % on the instalment plus a percentage on the annuity fund.
Carac [S1] and CNP [S5] are the two informative departures: Carac for the *capital réservé* /
*capital aliéné* fork and for semi-annual payment, CNP for the 3 %-per-instalment charge and the
dependency doubling. Préfon [S6] is the points-régime variant and is the only source with published
option costs.

**Structural facts that hold across every retrieved carrier and that a model must not parametrise
away:**
1. **terme échu** — no French annuity in the sample pays in advance;
2. **no contractual indexation** — uplift is discretionary profit-sharing only;
3. **no surrender after liquidation** — art. L. 132-23 [R8], with the single small-annuity
   commutation exception;
4. **the annuity option is irrevocable at liquidation**, and where reversion is elected the
   reduction is permanent even if the reversionary predeceases;
5. **the mortality table is annuitant-experience, generational, and floored** by the regulatory
   table [R3];
6. **a single table applied to all lives must be the more prudent one**, which for annuities means
   the female table.

**Not modelled, recorded as context:**
- *Réversion croisée* — named in the brief, found in no retrieved document [unverified].
- Group and occupational annuities under chapter III of title IV of book I of the Code des
  assurances, which art. A. 132-18 carves out of the experience-table floor [R3]; a possible unisex
  table for those from 24 October 2024 is claimed by a media source only [R25, unverified].
- Legacy annuities carrying State *majorations légales* [R22][S7], whose uprating is statutory and
  whose thresholds interact with A. 160-2.

---

## Gaps and caveats

1. **The CJEU judgment itself was never read.** [R16] — the EUR-Lex PDF endpoint returned an empty
   body and Curia was not fetched. Everything about *Test-Achats* here comes from two French
   ministerial answers [R17][R18] and one media page [R25]. The **date is reported inconsistently**
   in those secondary sources ("après le 20 décembre 2012" [R18][R25] vs "directive du 21 décembre
   2012" [R17]); the brief's 21 December 2012 is the standard reading of the judgment's temporal
   effect but is **[unverified]** against the judgment text. Do not build a date-boundary test on it.

2. **ACPR blocks automated fetching.** [R20] — both the PDF and the landing page for Analyses et
   Synthèses n° 66 returned HTTP 403 on two attempts. Only the RePEc abstract was read. Anything the
   paper says specifically about *rentes viagères*, about how the technical rate is set for
   annuities, or about observed annuity technical rates is **unknown**, not summarised.

3. **The "life expectancy minus five years" cap on *annuités garanties* has no located legal
   source.** Three primary documents apply it [S2][S3][S4][S9] and one attributes it to
   art. A. 335-1 [S4], but the retrieved text of A. 335-1 (2012–2016) [R2], of its successor
   A. 132-18 [R3], and of all fourteen amending points of the arrêté du 1er août 2006 [R1] were
   checked and **do not contain it**. Treat it as observed market practice.

4. **A. 335-1 is abrogated and the brief's citation is stale.** Legifrance marks A. 335-1 abrogated;
   the version whose text is quoted here ran 21/12/2012 – 01/01/2016 [R2]. The live article is
   **A. 132-18**, in force since 07/09/2017 from the arrêté du 14 août 2017 [R3]. The abrogating
   instrument and the fate of the article between 01/01/2016 and 07/09/2017 were **not resolved**
   [unverified]. Product documents should cite A. 132-18 for the live rule and A. 335-1 only when
   quoting the arrêté du 1er août 2006, which refers to the then-current numbering.

5. **Two Code articles were returned as paraphrase rather than verbatim.** A. 132-1 [R4] and
   A. 132-3 [R6] and A. 132-11 [R7] came back as structured summaries. The 75 % / 60 % / 3,5 % / 8-year
   structure of A. 132-1 and the eight-year rule of A. 132-16 are safe (each was returned twice or
   quoted). **The A. 132-11 retained-share wording ("greater of 10 % of the credit balance and 4,5 %
   of premiums") is [unverified] as to exact formulation**, as are the A. 132-3 percentages, which
   should be re-read before any of them is put in a parameter table.

6. **No annuity rate card exists anywhere.** [S1]–[S9] publish minimum capitals, minimum instalments,
   charge levels, reversion coefficients and points coefficients — **never a conversion rate**.
   Every *taux de rente*, annuity factor or specimen income in the product documents must be
   `[std]`, with the technical basis (table family, technical rate ceiling, charge level) cited and
   the factor itself standardised.

7. **TGH05/TGF05 values are not reproducible here, by design.** The tables are annexed to the Code
   des assurances [R12], and the annexe article for TGF05 is itself marked abrogated as of
   1 January 2016 with the tables presumably re-annexed elsewhere — the current annexe location was
   **not identified** [unverified]. The library ships **[std] proxy decrement tables built from
   public INSEE data**, anchored so that the model's best-estimate annuity factor reproduces the
   technical notes' own placeholder rate exactly. This is the same posture uklib takes on CMI
   tables. Do not ship TGH05/TGF05 rates.

8. **The Institut des actuaires construction deck is stamped CONFIDENTIEL.** [R19] — it is served
   publicly from institutdesactuaires.com and is cited here for methodology and headline life
   expectancies only. No rate values are taken from it.

9. **The assurance-vie route into an annuity is undocumented in this sample.** All five wrapper-exit
   sources are PER, PERP or a points régime [S2]–[S6][S9]; the two standalone contracts are a
   mutuelle règlement [S1] and a marketing page [S8]. **No *assurance vie* notice describing the
   *sortie en rente* was retrieved**, so the assurance-vie-specific mechanics — including whether
   accumulated gains are taxed at conversion — are **[unverified]**.

10. **Allianz could not be read.** [S10] — HTTP 403 on two attempts. No Allianz content is cited.
    Kos Avocats [R26] returned truncated and is likewise uncited. Generali, MACSF, Groupama,
    Swiss Life France, Malakoff Humanis, Le Conservateur and Garance were **not sourced at all**;
    the eight retrieved carriers were judged sufficient and no claim of market-wide coverage is made.

11. **CNP's notice has no edition date.** [S5] — no reference code or edition date appears in the
    extracted text, and the PDF is a third-party mirror posted in February 2021. Its charge levels
    (3 % per instalment, 1 % on annuity encours) and its 60/80/100 % reversion menu are treated as
    2020/2021-vintage and should be re-checked against a current CNP notice before being quoted as
    current.

12. **Fee-market figures from the press are ten years old.** [R23][R24] date from 2 April 2015.
    Where they agree with a retrieved contract (Suravenir PERP 0,68 % encours / 0 % arrears) the
    contract governs [S3]; the rest — the "around 3 %" norm, the 0,60–0,90 % encours band, the Axa
    flat 2–5 € per instalment, the Apicil 0,75 % + 3 % combination — is **[unverified]**.

13. **Claims found only in search-result summaries were not adopted.** AG2R's "18 annuity options"
    and a "2 500 € per month" dependency cap do not appear in the fetched AG2R page and are recorded
    as **[unverified]** rather than cited. Likewise the claim that a 2023 law introduced a unified
    mortality table for collective retirement plans from 24 October 2024 [R25].

14. **Live texts.** The Code des assurances and the CGI are living texts. Article versions were read
    on 2026-08-26: A. 132-18 as at 07/09/2017, A. 132-1-1 as at 01/01/2020, A. 160-2 as at
    22/07/2023, L. 132-23 as at 14/06/2026 (LOI n° 2026-492 du 12 juin 2026). The technical-rate
    ceiling of 2,00 % [R21] is a 31 July 2026 reading and moves. Re-check before relying on any
    article number, date or figure.
