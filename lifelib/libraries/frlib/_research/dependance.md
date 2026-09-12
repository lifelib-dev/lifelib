# Long-term care insurance, annuity form (assurance dépendance individuelle, rente) — research notes (France)

Research notes for the French individual long-term care contract — an *assurance dépendance*
paying a *rente mensuelle viagère* (lifetime monthly annuity) once the insured is recognised in a
contractual state of *dépendance* (loss of autonomy), usually with an optional *capital
d'équipement* (equipment lump sum) and a package of *prestations d'assistance* (care-coordination
services). These notes are the citation ground truth for the frlib `dependance` product documents:
source ids S1..S12 and R1..R18 below are frozen — never renumber.

Access date for all citations: 2026-08-26.

Citation discipline: every extracted fact is tagged `[S#]` or `[R#]` pointing at a document that was
actually fetched and read. `[unverified]` marks statements from general knowledge or from secondary
summaries of documents that could not be retrieved. Where a fetch failed the failure is recorded and
the item is kept only as a known reference (fetched_ok = false).

Language note: the French terms of art are kept in French and glossed on first use — *dépendance
totale* / *partielle* (total / partial dependence), *AVQ* (*actes de la vie quotidienne*, activities
of daily living), *GIR* (*groupe iso-ressources*, the six public dependency bands), *AGGIR* (the
public assessment grid), *délai de carence* / *délai d'attente* (waiting period from inception),
*délai de franchise* (elimination period after recognition), *cotisation* (premium), *mise en
réduction* / *maintien partiel des garanties* (paid-up reduction), *valeur de rachat* (surrender
value), *revalorisation* (indexation), *APA* (*allocation personnalisée d'autonomie*, the public
benefit).

---

## Primary sources

### S1 — AXA France Vie / AXA Assurances Vie Mutuelle and ANPERE, "Notice d'information Entour'Age" (Réf. 963470 04 2023)
- Publisher: AXA France Vie (310 499 959 RCS Nanterre) and AXA Assurances Vie Mutuelle (Siren
  353 457 245); group contract subscribed by ANPERE (Association Nationale pour la Prévoyance,
  l'Épargne et la Retraite); assistance by Inter Partner Assistance ("AXA Assistance").
- Doc type: *notice d'information* (policy conditions of a group contract with facultative
  membership), 44 pp., dated "Prévoyance / Avril 2023", reference 963470 04 2023.
- URL: https://media.axa.fr/content/dam/axa-fr/image/particuliers/sante/document-pdf/pdf-notice-information-dependance-entourage.pdf
- Retrieved: YES (PDF downloaded, full text extracted, 44 pages).
- Content: the most complete individual-market document retrieved. Legal frame (art. L.141-1 ff. Code
  des assurances; branches 1 Accidents and 2 Maladie under R.321-1, except the optional death covers
  which are branch 20 Vie-Décès); eligibility (residence in metropolitan France, Monaco or a DOM;
  ANPERE membership; medical formalities; age 40 to 75 inclusive at signature, age by *différence de
  millésimes*); rente choice 500–3,000 €/month; two *formules* (Dépendance Totale, or Dépendance
  Totale et Partielle where partial pays 50%); options *Capital Premiers Frais* 3,500 €, *Capital
  décès* 3,500 €, *Capital décès remboursement des cotisations*; the three contractual dependence
  definitions built on 5 AVQ plus the Folstein/MMSE test, with AGGIR used only for the partial and
  light tiers and GIR 5–6 never covered; *délai d'attente* nil/1 year/3 years by cause; absolute
  3-month *délai de franchise* (91st day); monthly payment in arrears; annual revalorisation of
  rentes in service by 1 April on the decision of a joint ANPERE/AXA management committee; the
  premium-revision clause (including revision "à raison des évolutions constatées ou projetées des
  statistiques nationales relatives à la dépendance"); premium exoneration on claim; 10% couple
  discount; *mise en réduction* after 8 full consecutive years; explicit "Votre adhésion ne comporte
  pas de valeur de rachat"; 30-day renunciation; taxation of the rente; full exclusion list.

### S2 — Antarius (Société Générale), "Assurance Dépendance — Document d'information sur le produit d'assurance", product *Antarius Dépendance* (Série C, novembre 2019)
- Publisher: ANTARIUS, société anonyme d'assurance sur la vie et de capitalisation (402 630 826 RCS
  Nanterre), agrément 5021196; distributed through Société Générale.
- Doc type: IPID / *document d'information sur le produit d'assurance*, 2 pp.
- URL: https://www.assurances.societegenerale.com/fileadmin/2023/IPID/Antarius/IPID_Antarius_D%C3%A9pendance.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: individuals aged 50 to under 75; *rente viagère mensuelle* 300–2,100 € plus a *capital
  d'équipement* of 3,000 € on total dependence; optional partial dependence paying 50% of the chosen
  amount plus the same 3,000 € capital, which may be paid as early as recognition of a "Dépendance
  sensible"; waiting 1 year, 3 years for neuro-degenerative or psychiatric causes, none for accident;
  3-month franchise from recognition **but the first rente instalment equals three monthly rentes**;
  the capital d'équipement is paid once only; premiums debited monthly on the 5th; a Société Générale
  bank account is required; "Après 8 années révolues de cotisations, le contrat sera maintenu avec
  une rente réduite déterminée selon le barème en vigueur à la date de mise en réduction."

### S3 — BPCE Prévoyance, "Assurance Dépendance — Document d'information sur le produit d'assurance", product *AUTONOMIS_124 EI*
- Publisher: BPCE Prévoyance (352 259 717 RCS Paris); document hosted by BRED; assistance by IMA
  ASSURANCES.
- Doc type: IPID, 2 pp.
- URL: https://www.bred.fr/pdf/medias/pdf/informations-reglementaires/ipid-autonomis.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: a purely GIR-triggered design. Group contract with facultative membership, branches 1 and
  2. *Formule 1 dépendance totale* = classified GIR 1 or GIR 2 after consolidation; pays a *capital
  équipement forfaitaire* of at most 3,200 € (net of earlier payments) plus the monthly rente stated
  on the membership certificate. *Formule 2 dépendance partielle* = classified GIR 3 or GIR 4 **and**
  requiring constant third-party assistance for at least 2 of 4 AVQ (s'alimenter, faire sa toilette,
  s'habiller et se déshabiller, transferts); capital équipement at most 2,400 €. Dependence beyond
  GIR 4 is not insured. Waiting: none for accident, 3 years for a medically established neurological
  or psychic illness, 1 year in all other cases; a GIR 1–4 dependence arising during the waiting
  period ends the membership. Health disclosure through a *questionnaire de santé simplifié
  dépendance* or a *fiche de santé dépendance*. Worldwide cover provided stays outside France do not
  exceed three continuous months. Exclusion list includes fibromyalgia, chronic fatigue syndrome,
  Ehlers-Danlos and fasciitis.

### S4 — CNP Assurances (Caisse d'Épargne), "Assurance Dépendance — Document d'information sur le produit d'assurance", product *Ecureuil Assistance Vie*
- Publisher: CNP Assurances (341 737 062 RCS Paris); distributed by Caisse d'Épargne.
- Doc type: IPID, 2 pp.
- URL: https://www.img.caisse-epargne.fr/app/uploads/sites/3/2022/04/22161550/dip-dependance-ecureuil-assistance-vie.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: rente chosen from 400 to 3,000 €/month in steps of 100 €. Three benefit tiers on a 6-AVQ
  grid (toilette, habillage, alimentation, continence, déplacement, transferts): *dépendance totale*
  at ≥5 of 6 AVQ pays 100% of the rente plus a 3,000 € capital "Équipement"; *dépendance partielle*
  at ≥4 of 6 pays 60% of the rente plus the same 3,000 € capital (not re-paid on a later
  deterioration to total); optional *dépendance légère* at ≥2 of 6 pays 30% of the rente plus a 900 €
  capital, deducted from any later capital. Optional *Garantie Fracture* pays 300 €. *Délai
  d'attente* one year for non-accidental functional dependence, three years for non-accidental
  psychic dependence; *délai de franchise* three months for total or partial dependence. Premiums
  cease on recognition. Residence in metropolitan France or DOM/TOM required.

### S5 — CNP Assurances / Banque de France, "Notice d'information relative au contrat d'assurance collective en cas de Dépendance à adhésion facultative n° 0658 Q du personnel de la Banque de France"
- Publisher: CNP Assurances; subscriber Banque de France; claims handled by HUMANIS; assistance by
  FILASSISTANCE.
- Doc type: *notice d'information* with annexes (tariff table, reduction scale, assistance schedule),
  16 pp.
- URL: https://www.banque-france.fr/system/files/2024-11/assur_ni-dep-bdf-y.pdf
- Retrieved: YES (PDF downloaded via browser User-Agent after WebFetch returned HTTP 403 twice; full
  text extracted).
- Content: the single most useful document for a modeller, because it publishes an actual **premium
  scale by age at entry** and an actual **barème de maintien des garanties** (reduction coefficients
  by number of years of premiums paid). Open to Banque de France staff and their spouses, parents and
  parents-in-law, and to retirees, all aged under 75. Dependence defined on 6 AVQ, functional or
  psychic (psychic requiring an MMSE "Mini Mental State Examination" Folstein score below 15
  certified by a psychiatrist or neurologist), **plus** a placement condition (residence in a *section
  de cure médicale* or an establishment for the elderly, long-stay hospitalisation, or the combination
  of home nursing care and third-person assistance). Four severity levels: 2, 3, 4, and 5-or-6 AVQ of
  6. The rente is paid from level 3 and is doubled at level 4; the optional *capital premières
  dépenses* is paid from level 2. Five coverage levels with published amounts. *Délai d'attente* 1
  year, 3 years for psychiatric illness, none for accident; *délai de franchise* 3 months from
  recognition. Guarantees and rentes revalued each 1 January by reference to the rate applied to
  Banque de France pensions (that of civil and military retirement pensions), subject to the
  revalorisation fund; on resiliation of the group contract, by reference to the AGIRC pension point.
  Article 22 lets the insurer revise the tariff scale "en fonction de l'évolution des résultats".
  From five years of premiums paid, non-payment produces *maintien partiel des garanties* rather than
  exclusion.

### S6 — CNP Assurances / Mutuelle des Sapeurs Pompiers de Paris, "Notice d'information relative au Contrat d'assurance de groupe n° A063 F Dépendance à adhésion obligatoire" (2016NI14079, in force from 1 January 2019)
- Publisher: CNP Assurances; subscriber Mutuelle des Sapeurs Pompiers de Paris (MSPP).
- Doc type: *notice d'information* including the IPID (IPID DEPENDANCE_CNP_112018), 14 pp.
- URL: https://www.mspp.fr/wp-content/uploads/2022/07/Livret-complet-CNP-Dependance.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: a **compulsory** group contract, included here because it states the AVQ definitions and
  the franchise mechanics unusually cleanly and prices a small flat cover. *Dépendance totale* =
  consolidated state and either functional inability to perform alone at least 5 of the 6 AVQ from a
  medically established physical handicap, or psychic inability to perform at least 5 of 6
  spontaneously without prompting because of a medically established dementia, certified by a
  psychiatrist or neurologist with an MMSE Folstein score below 15. *Dépendance partielle* = the same
  two routes at 4 of 6. Explicit statement that "L'Assureur n'est pas lié par les éventuelles
  décisions des services publics pour déterminer l'état et le degré de dépendance de l'assuré."
  Medical adviser rules within 45 working days of a complete file; absolute 3-month franchise counted
  from the date the state reached an indemnifiable level (art. 24), described in art. 26 and in the
  IPID as 90 days from recognition; benefits due from the date of recognition where the cause is an
  accident. Rente viagère paid monthly in arrears. Benefit table: 2,400 €/year (200 €/month) for
  total, 1,200 €/year (100 €/month) for partial, for 20.40 €/year (1.70 €/month) per insured person.
  Annual *certificat de vie* required each 1 January. Revalorisation only "par un accord entre
  l'Assureur et le Souscripteur, sous réserve des résultats du Contrat".

### S7 — Suravenir Assurances / Crédit Mutuel, "Assurance Dépendance — Conditions générales" (contrat collectif n° 1014)
- Publisher: Suravenir Assurances (Saint-Herblain); subscribers the Fédérations Régionales de Crédit
  Mutuel and the association APCAS; document hosted by CMSO.
- Doc type: *conditions générales*, 22 pp. Filed under a 2013-12 path; no printed edition date was
  found in the extracted text, so treat the wording as of that vintage.
- URL: https://www.cmso.com/banque/assurance/credit-mutuel/upload/docs/application/pdf/2013-12/cg_dependance.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the cleanest purely-AGGIR contract retrieved. "L'état de dépendance est évalué selon la
  grille de référence AGGIR du décret 97-427 du 28 avril 1997." *Dépendance totale* = GIR 1 or GIR 2;
  *dépendance partielle* = GIR 3 or GIR 4, with the GIR definitions reproduced verbatim in the
  conditions; for neuro-degenerative conditions an MMSE below 15 must be produced. Two formulas
  (*Contrat Essentiel*, total only; *Contrat Confort*, total plus partial at 50%), optional *capital
  1er frais* (full on total, half on partial with the remainder on deterioration). Age at adhesion
  under 75. Rente starts on the 91st day after recognition, payable monthly in arrears. Annual
  revalorisation of guarantees within the limits of a *fonds de revalorisation*, with the premium
  raised in the same proportion; rentes in service revalued each 1 January by reference to the annual
  change in the AGIRC point value, the fund being fed by 36% of any surplus on the result account.
  A tariff-revision clause with an explicit **cap of 10% per year** excluding revalorisation. *Mise
  en réduction* from 8 years of premiums paid, with reduced guarantees no longer revalued and the
  definitive reduced rente computed at the claim date on the bases then in force.

### S8 — Groupama, "Assurance dépendance : contrat et garanties" (*Groupama Autonomie* product page)
- Publisher: Groupama.
- Doc type: insurer product page (not a notice).
- URL: https://www.groupama.fr/assurance-dependance/
- Retrieved: YES (page fetched and read).
- Content: two formulas (total; total and partial). Rente 200–2,000 €/month for total and
  100–1,000 €/month for partial (50% of the subscribed amount), stated as non-taxable. Optional
  *capital d'aménagement* reimbursing up to 5,000 € of home-adaptation and equipment costs, available
  on both formulas. The rente begins on the 91st day following recognition by the insurer's medical
  adviser. Entry recommended from age 40 and generally not available after 77. A worked premium
  illustration: the total-and-partial formula with a 400 €/800 € rente costs 53–76 €/month without
  the option and 62–89 €/month with it, for ages 55 to 65. 10% couple discount when both spouses
  subscribe together. Assistance: 24/7 line, ergotherapist assessment, psychological support for
  carers, help finding an establishment, coordination of home-care services.

### S9 — Groupama, "Grille AGGIR : quel degré de dépendance ?" (AGGIR/AVQ explainer)
- Publisher: Groupama.
- Doc type: insurer explanatory page.
- URL: https://www.groupama.fr/assurance-dependance/conseils/grilles-aggir-avq-comment-est-evaluee-la-dependance/
- Retrieved: YES.
- Content: reproduces the six GIR definitions and states that only GIR 1–4 open APA rights. Sets out
  a 6-act AVQ grid (toilette, habillage, alimentation, continence, déplacement, transferts) with four
  severity levels — 2 of 6, 3 of 6, 4 of 6, 5 or 6 of 6 — and states that the AVQ grid "peut être
  utilisée en complément ou comme alternative à la grille AGGIR". Useful as an insurer-side statement
  of the standard 4-tier AVQ ladder that S4 and S5 implement.

### S10 — Generali France, "Generali Assurance Dépendance" (product page)
- Publisher: Generali France.
- Doc type: insurer product page.
- URL: https://www.generali.fr/assurance-dependance/
- Retrieved: YES.
- Content: three formulas; rente 500–3,000 €/month for total dependence and 250–1,500 €/month for
  partial (formulas 2 and 3); formula 3 adds a *capital d'équipement* of 5,000 € or 10,000 € paid in
  one instalment with no franchise. An optional death benefit applies where death occurs before age
  85 without a prior dependence claim. Assistance through Europ Assistance, including an
  ergotherapist audit covered up to 300 €, and an "Assistance Plus" option with a social-worker
  consultation at age 70 and carer training. The page refers waiting periods to the *notice
  d'information* without stating them, and gives no AVQ counts.

### S11 — AG2R La Mondiale, "La rente dépendance : définition, comment ça marche"
- Publisher: AG2R La Mondiale.
- Doc type: insurer explanatory page.
- URL: https://www.ag2rlamondiale.fr/sante-prevoyance/dependance/conseil-qu-est-ce-que-la-rente-dependance
- Retrieved: YES.
- Content: states the market range of the *rente dépendance* as "entre 300 à 4 000 € par mois selon
  les contrats", that the benefit is "versée à vie", that the insurer's doctor assesses the file, and
  that the AGGIR scale is used with levels 1–2 representing the heaviest cases while definitions vary
  by contract. Explicit on the *fonds perdu* character: if the insured stays autonomous until death,
  no rente and no capital is paid and "les cotisations qui auront été versées sont perdues". No
  carence or franchise figures are given on this page.

### S12 — Sogecap, "Garantie Autonome Senior" (individual/collective LTC contract)
- Publisher: Sogecap (Société Générale group).
- Doc type: product specification — **no Sogecap document of any kind was retrieved**.
- URL: none located.
- Retrieved: NO (no notice, conditions générales or IPID for this product could be found). The full
  specification below is taken from the Institut des actuaires / ISUP dissertation written inside
  Sogecap [R12], which describes the product in detail; every figure attributed to S12 is therefore
  really an [R12] fact and is tagged as such where used.
- Content (as described in [R12]): collective contract with facultative membership renewed annually
  by tacit reconduction; insured aged 50 to under 75; total dependence = 4 of 5 AVQ, or 3 of 5 AVQ
  with a Folstein score ≤ 15, or 2 of 5 AVQ with a Folstein score ≤ 10; partial dependence = 3 of 5
  AVQ, or 2 of 5 AVQ with Folstein ≤ 15; rente 500–3,000 €/month in steps of 100 € for total and 50%
  of it for partial; optional *capital d'équipement* of 5,000 € paid once; 3-month franchise; waiting
  none / 3 years (neuro-degenerative or psychiatric) / 1 year; guarantees and benefits revalued at
  each annual due date from the contract's technical and financial results; *maintien partiel des
  garanties* only after 8 years of premiums, which removes the capital option and restricts the
  reduced cover to total dependence alone; rente increases allowed once a year subject to a 200 €
  minimum step and decreases once a year without condition; premium indexed annually on the growth of
  the *PASS* (plafond annuel de la sécurité sociale); quota-share reinsurance with Sogecap retaining
  30%.

---

## Regulatory and actuarial references

### R1 — Legifrance, Code de l'action sociale et des familles, Annexe 2-1 "Grille nationale AGGIR et son guide de remplissage"
- Publisher: Legifrance (Direction de l'information légale et administrative)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000034696537/
- Retrieved: YES (article page read).
- Content: the statutory AGGIR grid. Current version created by *décret n° 2017-882 du 9 mai 2017,
  art. 5*, in force since 11 May 2017. Ten *variables discriminantes* of corporeal and mental
  activity — cohérence, orientation, toilette, habillage, alimentation, élimination urinaire et
  fécale, transferts, déplacements à l'intérieur, déplacements à l'extérieur, alerter — and seven
  *variables illustratives* of domestic and social activity — gestion, cuisine, ménage, transports,
  achats, suivi du traitement, activités du temps libre. Three scoring modalities: **A** does it
  alone, spontaneously, totally, habitually and correctly; **B** does it alone but not spontaneously
  and/or partially and/or not habitually and/or incorrectly; **C** does not do it alone. The six GIR
  definitions are given in the annex; GIR 6 is not spelled out as a separate profile in the fetched
  rendering of the annex, but appears in the codified summaries [R2][R3].

### R2 — Legifrance, Code de l'action sociale et des familles, articles R232-1 to R232-6 (APA)
- Publisher: Legifrance
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006074069/LEGISCTA000006190052/
- Retrieved: YES (section page read).
- Content: R232-1 fixes the APA age condition at 60. R232-3 (version of 24/08/2008) provides that the
  loss of autonomy is "évaluée par référence à la grille nationale mentionnée à l'article L. 232-2 et
  figurant à l'annexe 2-1", the results being processed by the single calculation mode set out in
  annexe 2-2 to classify applicants into the six *groupes iso-ressources* according to the personal
  care and technical aids needed. R232-4 (26/10/2004) restricts APA to persons classified in "groups
  1 to 4 of the national grid". R232-5 and R232-6 govern the resource test behind the beneficiary's
  contribution. This is the statutory hook that makes GIR a *public* classification the insurance
  market can either adopt or deliberately depart from.

### R3 — service-public.gouv.fr, "Apa : que sont les Gir 1, Gir 2, Gir 3 et Gir 4 de la grille Aggir ?" (fiche F1229)
- Publisher: DILA / service-public.gouv.fr. Page last updated 9 January 2026.
- URL: https://www.service-public.gouv.fr/particuliers/vosdroits/F1229
- Retrieved: YES (page read; the older service-public.fr host 301-redirects to service-public.gouv.fr).
- Content: plain-language definitions of GIR 1 to GIR 6 and the statement that only GIR 1–4 open APA
  rights while GIR 5–6 can obtain household help or pension-fund assistance. Lists the ten
  discriminant and seven illustrative activities. Cites CASF articles R232-1 and R232-6 (with R232-3
  and R232-4) and the annex carrying the national grid, and links to the CNSA pages [R5][R6].

### R4 — CNSA / pour-les-personnes-agees.gouv.fr, "L'APA à domicile"
- Publisher: Caisse nationale de solidarité pour l'autonomie (CNSA)
- URL: https://www.pour-les-personnes-agees.gouv.fr/vivre-a-domicile/aides-financieres/l-apa-a-domicile
- Retrieved: YES.
- Content: the monthly *plan d'aide* ceilings applicable from 1 January 2026 — GIR 1 2,080.33 €,
  GIR 2 1,682.30 €, GIR 3 1,215.99 €, GIR 4 811.52 € — which may be raised where an indispensable
  family carer needs respite. Participation rules: no contribution up to a monthly income of
  933.89 €; a rate varying between 0% and 90% between 933.90 € and 3,439.31 €; 90% above 3,439.31 €.
  This is the public benefit the private rente is designed to top up.

### R5 — CNSA / pour-les-personnes-agees.gouv.fr, "APA : comment vos besoins sont évalués ?"
- Publisher: CNSA
- URL: https://www.pour-les-personnes-agees.gouv.fr/preserver-son-autonomie/perte-d-autonomie-evaluation-et-droits/comment-les-besoins-sont-ils-evalues
- Retrieved: YES.
- Content: the assessment is made by a professional of the department's *équipe médico-sociale APA*
  during a home visit; the resulting *plan d'aide* states the GIR, the aids financed (home-care hours,
  meal delivery, incontinence protections and so on), the total amount and the beneficiary's
  participation rate. GIR 5–6 are redirected to pension-fund assistance. The page does not publish
  the ceilings (those are on [R4]).

### R6 — CNSA / pour-les-personnes-agees.gouv.fr, "Comment votre GIR est-il calculé ?" (facile à lire et à comprendre)
- Publisher: CNSA
- URL: https://www.pour-les-personnes-agees.gouv.fr/annuaires-et-services/facile-a-lire-et-a-comprendre/comment-votre-gir-est-il-calcule
- Retrieved: YES.
- Content: confirms that at home the GIR is set by a departmental professional (nurse or social
  worker) and that in an establishment it is set by the establishment's physician, usually within a
  month of admission. This split matters for a model: the same insured can be re-graded by a
  different assessor on entering an EHPAD.

### R7 — DREES, "L'aide sociale aux personnes âgées ou handicapées — Édition 2025", Fiche 06 "L'allocation personnalisée d'autonomie (APA)"
- Publisher: Direction de la recherche, des études, de l'évaluation et des statistiques (DREES)
- URL: https://drees.solidarites-sante.gouv.fr/sites/default/files/2025-09/PAPH%20-%20Fiche%2006%20-%20L%E2%80%99allocation%20personnalis%C3%A9e%20d%E2%80%99autonomie%20(APA)_0.pdf
- Retrieved: YES (PDF downloaded via browser User-Agent, 8 pp., full text extracted).
- Content: the best public prevalence source for a French LTC model. End-2023 counts and rates,
  spending series 2005–2023, the GIR split at home and in establishments, APA prevalence by age and
  sex, and the APA-state life expectancy at 60. All the figures used below in section 16 come from
  this fiche. Sources given as DREES *enquête Aide sociale*, DREES *enquête EHPA 2023*, and INSEE
  provisional population estimates at 1 January 2024.

### R8 — CCSF, Fabrice Aubert, "L'information précontractuelle en matière d'assurance dépendance" (July 2013)
- Publisher: Comité consultatif du secteur financier (CCSF); author Fabrice Aubert, auditeur au
  Conseil d'État. Hosted on banque-france.fr and ccsfin.fr.
- URL: https://www.banque-france.fr/system/files/import/ccsf/medias/documents/rapport_assurance_dependance.pdf
  (the ccsfin.fr copy at https://www.ccsfin.fr/sites/default/files/medias/documents/rapport_assurance_dependance.pdf
  returns HTTP 403)
- Retrieved: YES (PDF downloaded via browser User-Agent, 23 pp., full text extracted; Annexe 3, the
  GAD common vocabulary, is a set of page images and its text could not be extracted).
- Content: the single best structural survey of the French LTC market. Contract taxonomy (facultative
  vs compulsory, principal vs optional vs included guarantee, viagère vs temporaire) with a 2010 CTIP
  headcount; the four benefit families (prevention/advice, assistance, rente, capital); waiting and
  franchise ranges; an indicative price point; the two assessment referentials with a count of how
  the two are used across a 30-contract sample; the enumerated ways "dépendance lourde" is defined
  across contracts; the nine GAD label criteria reproduced verbatim; and the consumer-protection
  criticisms (the *valeur de réduction* and the revalorisation clauses being insufficiently
  highlighted, and the risk of monetary erosion of a rente promised fifteen or twenty years ahead).

### R9 — CCSF, "Pour une meilleure protection des personnes dépendantes et de leur famille : Le Contrat Dépendance Solidaire" — communiqué de presse, 24 January 2024
- Publisher: CCSF (recommendation adopted at the plenary session of 16 January 2024)
- URL: https://www.banque-france.fr/system/files/import/ccsf/medias/documents/cp_recommandation_dependance_24012024.pdf
- Retrieved: YES (PDF downloaded via browser User-Agent, 5 pp., full text extracted).
- Content: the current French policy position. Market figures (814 M€ of premiums for 2.64 million
  people covered by dependence contracts, 28% collective, of which 1.48 million under specific
  dependence contracts); demographic projection (4 million seniors in loss of autonomy in 2050, 16.4%
  of the 60+, versus 15.3% in 2015; heavy loss of autonomy 4.3% versus 3.7% in 2015, sourced to INSEE
  *Tableaux de l'économie française* 2020); 30 Md€ of dependence spending, informal-carer work valued
  at 7–18 Md€ in 2014, and the Libault report's ~10 Md€ of additional annual funding needed by 2030;
  the mean age at onset of total dependence (about 78 for men and 84 for women) and a mean duration of
  receipt of the allocation of three years for heavy dependents; a *reste à charge* of about
  1,957 €/month in an EHPAD (DREES study of July 2022). The recommendation itself: a compulsory
  *Contrat Dépendance Solidaire* covering GIR 1–2 only, bolted onto *contrats santé responsables*,
  with a single lifelong tariff grid, no waiting period, a reduction mechanism for interrupted
  payment, portability through a single insurance pool, and automatic payment triggered by receipt of
  APA at GIR 1 or 2.

### R10 — France Assureurs, "L'assurance prévoyance — Étude, année 2024" (July 2025), section 2.3 "Les contrats dépendance"
- Publisher: France Assureurs (Fédération Française de l'Assurance)
- URL: https://www.franceassureurs.fr/wp-content/uploads/lassurance-prevoyance-en-2024.pdf
- Retrieved: YES (PDF downloaded, 25 pp., full text extracted with both PyMuPDF and pypdf).
- Content: the market statistics used in section 17 below. Note that both extractors drop the glyph
  "8" from the body text of this PDF (the file uses a subset font); the affected figures were
  reconstructed and then independently confirmed against [R13], which quotes the same release.
- Note: the per-cover average-premium series (dépendance lourde ≈ 308 €/year, dépendance lourde et
  partielle ≈ 535 €/year in 2024) was read off the page-14 chart labels by coordinate, not from
  running text; treat those two figures as chart-read rather than text-confirmed.

### R11 — France Assureurs, "L'assurance dépendance" (market explainer, GAD label criteria)
- Publisher: France Assureurs
- URL: https://www.franceassureurs.fr/lassurance-protege-finance-et-emploie/lassurance-protege/lassurance-en-pratique-pour-les-particuliers/assurance-dependance/
- Retrieved: YES (page read; the nine GAD criteria quoted verbatim in French).
- Content: the nine criteria of the **GAD ASSURANCE DÉPENDANCE®** label; the five *actes élémentaires*
  used for the common definition of dépendance lourde (transfert, déplacement, toilette, habillage,
  alimentation); *dépendance partielle* defined only as a lower degree than total; *délai de carence*
  between 1 and 3 years depending on the contract; *délai de franchise* generally 90 days after
  recognition. This is the label's own publisher, so it is the authoritative statement of the
  criteria; the same nine points appear in [R8].

### R12 — Institut des actuaires / ISUP (Sorbonne Université), Ledwing Osorio Cardenas, "Analyse de rentabilité d'un produit d'assurance dépendance" (mémoire, 22 October 2018)
- Publisher: Institut de statistique de l'Université de Paris (ISUP) for the Institut des actuaires;
  written inside Sogecap under Edith Buchet. Marked confidential for two years (expired).
- URL: https://www.institutdesactuaires.com/docs/mem/8864a367d81f149b52dce8663c200ded.pdf
- Retrieved: YES (PDF downloaded, 77 pp., full text extracted).
- Content: the actuarial framing this library needs. Chapter 1 describes the market, the AVQ and
  AGGIR grids, the GAD label, the Solvency II classification of LTC in the **Health-SLT** module, and
  the position that the Code des assurances contains no specific LTC regulation, that LTC can be read
  as a non-life risk with a lifelong guarantee, that the choice of branch *agrément* is at the
  insurer's discretion, and that article L331-3 on *participation aux bénéfices* does not bite because
  the risk covered is not human life. Chapter 3 sets out the multi-state model, the incidence and
  continuance laws, the treatment of *carence* through incidence-reduction coefficients, the
  franchise-adjusted annuity factor, unisex pricing, and the two provisions (*provision pour risques
  croissants* and *provision mathématique des rentes*). Also the full Sogecap product specification
  used for S12. The numerical bases (incidence and continuance tables, technical rate, loadings) are
  parameterised symbolically and not disclosed.

### R13 — Institut des actuaires, "Assurance dépendance : état des lieux, solutions assurantielles et innovations pour le bien-vieillir" (atelier technique, 24 November 2025)
- Publisher: Institut des actuaires; authors Aurélie Treilhou, Sana Ayadi, Alexandre Petit, Vincent
  Touzé.
- URL: https://www.institutdesactuaires.com/global/gene/link.php?doc_id=20056&fg=1
- Retrieved: YES (PDF downloaded, 37 slides, full text extracted).
- Content: restates the France Assureurs 2024 figures in clean form (and so served as the check on
  [R10]'s dropped digits); adds that 6.0 million people were insured against the dependence risk
  across the whole market in 2024, 56% by *mutuelles*, 40% by insurance companies and 4% by
  *institutions de prévoyance*; summarises a 2021 France Assureurs survey (one French person in ten
  holds a dependence contract, a majority does not know the product exists, most such contracts carry
  a rente below 500 €/month, 52% would like the cover to be compulsory); describes the German
  Pflegeversicherung for contrast; and documents the **OCIRP** *points*-based collective LTC
  guarantee — a defined-contribution deferred rente expressed in points, priced through an
  age-dependent (or mutualised) *valeur d'acquisition* and paid as points × *valeur de service*, with
  a guaranteed minimum monthly rente of 200–750 € for GIR 1–2 and half of it for GIR 3, funded by
  0.40%–1.50% of the PMSS, and **no reduction value applied if the insured stops contributing**.

### R14 — DREES, "Couverture des risques sociaux par les organismes privés d'assurance : mise à jour des données pour 2024"
- Publisher: DREES. Published 31 March 2026.
- URL: https://drees.solidarites-sante.gouv.fr/communique-de-presse-jeux-de-donnees/jeux-de-donnees/260331_couverture-des-risques-sociaux-par-les-organismes-priv%C3%A9s-d%E2%80%99assurance
- Retrieved: YES (landing page read; the underlying data files were not downloaded).
- Content: places dependence cover (rente or capital) at about 1% of premiums collected for social
  risks by private insurers, inside the 17.8 Md€ of "other bodily-injury guarantees" that also covers
  *incapacité* and *invalidité*. The page does not break dependence down by type of insurer; that
  split is in [R13].

### R15 — ACPR, "Enseignements des actions de contrôle menées sur l'assurance dépendance"
- Publisher: Autorité de contrôle prudentiel et de résolution
- URL: https://acpr.banque-france.fr/fr/actualites/enseignements-des-actions-de-controle-menees-sur-lassurance-dependance
- Retrieved: NO — HTTP 403 Forbidden on two WebFetch attempts. Kept as a known reference only. No
  content from this page is cited anywhere below.

### R16 — ACPR, *Revue de l'ACPR*, article on assurance dépendance (September 2023)
- Publisher: ACPR / Banque de France
- URL: https://acpr.banque-france.fr/system/files/import/acpr/medias/documents/20230926_article_assurance_dependance.pdf
- Retrieved: NO — HTTP 403 on two WebFetch attempts and on a curl attempt carrying a browser
  User-Agent, Accept-Language and Referer (the host returns an HTML error page, not the PDF). Known
  reference only; content not verified and not cited.

### R17 — DGCCRF (economie.gouv.fr), fiche pratique "Assurance dépendance"
- Publisher: Direction générale de la concurrence, de la consommation et de la répression des fraudes
- URL: https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/assurance-dependance
- Retrieved: NO — HTTP 403 on two WebFetch attempts. Known reference only; content not cited.

### R18 — Legifrance, Code des assurances
- Publisher: Legifrance
- URL: https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006073984/
- Retrieved: PARTIAL — the code's *partie législative* table of contents (articles L100-1 to L561-1)
  was retrieved and the code identity and version date (25 August 2026) confirmed. The *partie
  réglementaire* is not exposed on that page and **article R343-3, which governs the technical
  provisions of life insurers including the *provision pour risques croissants*, was not retrieved**.
  Anything said below about the PRC therefore rests on [R12], not on the code text.

---

## Extracted specifications

### 1. Product structure and legal form
- The individual French LTC product is almost always written as a *contrat d'assurance de groupe à
  adhésion facultative* — a group policy subscribed by an association or a distributor, which the
  customer joins — rather than as a stand-alone individual policy. Confirmed subscribers among the
  retrieved contracts: ANPERE for AXA [S1 §1.1.1], the Fédérations Régionales de Crédit Mutuel and
  APCAS for Suravenir [S7 p2], the Banque de France for CNP 0658 Q [S5 art. 1], the MSPP for CNP
  A063 F (compulsory variant) [S6 art. 1.1]. Antarius, BPCE Prévoyance and Sogecap are described the
  same way [S2][S3][R12 §1.2.1]. The customer therefore receives a *notice d'information*, not
  *conditions générales* in the direct-writing sense, and the *notice* is the contractual document.
- Consequence for modelling: the group contract itself is annual and tacitly renewed and can be
  terminated by either party, but an existing membership survives that termination and continues to
  run to extinction as long as premiums are paid [S1 §8.2][S5 art. 25]. The individual cover is
  *viagère* — lifelong — while the wrapper is annual.
- Branch classification: branches 1 (Accidents) and 2 (Maladie) of art. R.321-1 of the Code des
  assurances [S1 §1.1.1][S3][S6 art. 1.1]. Optional death benefits sold alongside sit in branch 20
  (Vie-Décès) [S1 §1.1.1]. There is no LTC-specific regime in the Code des assurances; LTC is best
  read as a non-life risk carrying a lifelong guarantee, the branch *agrément* is at the insurer's
  discretion, and the *participation aux bénéfices* obligation of article L331-3 does not apply
  because the risk covered is not human life [R12 §1.1.2.2]. Under Solvency II the business falls in
  the **Health-SLT** underwriting module, life techniques applying because of the long-term
  commitment [R12 §1.1.2.1].
- Benefit architecture, consistent across every retrieved contract: (a) prevention and advice
  services from inception; (b) assistance services triggered by loss of autonomy; (c) the *rente*
  once the state is consolidated; (d) an optional lump sum for equipment and home adaptation
  [R8 §2.2][S1][S2][S3][S4][S8][S10].

### 2. Eligibility, age at entry, and cessation of cover
- Age at entry, from retrieved documents:
  - AXA Entour'Age: 40 to 75 inclusive at the date of signature of the *bulletin d'adhésion*, age
    computed by *différence de millésimes* [S1 §1.1.2.1].
  - Antarius: 50 to under 75 [S2].
  - Sogecap: 50 to under 75 [R12 §1.2.1].
  - Suravenir / Crédit Mutuel: under 75 [S7 §2.1].
  - CNP 0658 Q: under 75 [S5 art. 2].
  - Groupama: subscription recommended from 40, generally not available after 77 [S8].
  - CNP A063 F (compulsory group): cover runs to age 65 for members joining after inception [S6 IPID].
- The market average age at subscription is 64 [R10 §2.3][R13 p6]; the CCSF's structural criticism is
  precisely that contracts are "peu et tardivement souscrits", which prevents wide mutualisation and
  makes the cover expensive [R9 §1].
- Cessation. The dependence cover itself does not cease at any age: "L'Assuré reste garanti quels que
  soient son âge et l'évolution de son état de santé" [S5 art. 8]; at AXA the guarantees are *viagères*
  from their effective date [S1 §1.1.5]. What does have an age limit is the *optional* death benefit —
  AXA's *Capital décès* and *Capital décès remboursement des cotisations* end at the end of the
  insurance year in which the insured turns 85 [S1 §1.1.4.1, §1.1.5], and Generali's death option
  requires death before 85 [S10].
- Cover ends on: death of the insured; renunciation within 30 days [S1 §7.6][S5 art. 8][S7 §2.5];
  resiliation by the member (annually, with 60 days' notice at AXA [S1 §1.1.4.2a], one month at
  Suravenir [S7 §4.5], notified before 1 November for a 1 January effect at CNP [S5 art. 9a]);
  non-payment of premium, subject to the reduction rules of section 11; and recognition of dependence
  during the waiting period, which voids the membership and refunds premiums [S1 §1.1.4.2c][S3]
  [S5 art. 7][S7 §3.2].
- Increases in cover are re-underwritten and restart the waiting period: AXA allows changes from the
  third full year, requires age ≤ 75 for an improvement, and applies a fresh *délai d'attente* to the
  additional cover [S1 §1.1.3]; Suravenir requires age under 75 and a negative health declaration for
  an increase, with the waiting periods reapplying [S7 §3.3]; Sogecap allows one increase a year with
  a 200 € minimum step and one unconditional decrease a year [R12 §1.2.1].

### 3. Medical underwriting
- Two-stage underwriting is universal in the retrieved documents: a short *déclaration d'état de
  santé* answered yes/no, and, if any answer is positive, a full *questionnaire de santé* assessed by
  the insurer's medical adviser, who sets the acceptance terms [S5 art. 3][S7 §2.2][S3][S4].
- AXA prices an explicit *majoration tarifaire pour risque aggravé* into the premium where the
  medical adviser requires it [S1 §1.2.1].
- The GAD label forbids medical selection before age 50, except where the applicant already has a
  disability or an *ALD* (*affection de longue durée*) [R8 §4.3 point 6][R11]. No retrieved contract
  document states the rule in its own terms, so its application to any specific contract above is
  [unverified].
- Mis-statement is dealt with under the ordinary articles L.113-8 (intentional — nullity, premiums
  retained) and L.113-9 (non-intentional — proportional reduction of the indemnity, or resiliation
  after 10 days) [S1 §1.1.2.2][S7 §2.4].

### 4. What "dependence" means — the two grids and how insurers map them
There is no single French definition of dependence in insurance. Two referentials coexist and
contracts use one, the other, or both [R8 §3.2][R12 §1.1.1].

**(a) The AGGIR grid (public).** *Autonomie Gérontologie Groupes Iso-Ressources*. Statutory, annexed
to the Code de l'action sociale et des familles as annexe 2-1 in the version created by *décret
n° 2017-882 du 9 mai 2017* art. 5 [R1]; referenced by CASF R232-3 and used by departments to award
the APA, which is restricted to GIR 1 to 4 [R2 art. R232-3, R232-4][R3]. Ten *variables
discriminantes* (cohérence, orientation, toilette, habillage, alimentation, élimination urinaire et
fécale, transferts, déplacements à l'intérieur, déplacements à l'extérieur, alerter) and seven
*variables illustratives* (gestion, cuisine, ménage, transports, achats, suivi du traitement,
activités du temps libre), each scored A / B / C [R1]. The six bands [R1][R3][R7][S7 defs][S1 §2.1.2]:

| GIR | Profile |
|---|---|
| 1 | Confined to bed or chair, mental functions gravely impaired, requires continuous attendance; or a person at end of life |
| 2 | Confined to bed or chair with mental functions not wholly impaired, requiring care for most everyday activities; or mentally impaired but able to move about, requiring permanent supervision |
| 3 | Mental autonomy retained, locomotor autonomy partly retained, needs help with bodily care several times a day |
| 4 | Cannot transfer alone but can move about indoors once up, needs help with washing and dressing; or no locomotor problem but needs help with bodily care and meals |
| 5 | Needs only occasional help with washing, meal preparation and housework |
| 6 | Still autonomous for the essential acts of everyday life |

**(b) AVQ grids (insurer-built).** Grids of 4 to 6 *actes de la vie quotidienne* built by insurers
precisely because AGGIR is applied by departments the insurer does not control, an uncertainty that
complicates rating and reserving [R8 §3.2]. The five acts of the GAD common definition are *transfert*
(moving between lying, sitting and standing), *déplacement* (moving on a flat surface indoors),
*toilette*, *habillage*, *alimentation* [R11][R12 §1.1.1.1][S1 §2.1.1]. Six-act grids add *continence*
[S4][S5 art. 12][S6][S9]. AVQ grids can be supplemented by *AIVQ* grids — instrumental activities:
using transport, the telephone, managing medication, managing a budget — aimed at mental dependence
[R8 §3.2]; no retrieved contract used AIVQ.

**(c) Cognitive testing.** The *Mini Mental State Examination* (Folstein / MMSE) is the standard
overlay for psychic dependence. Thresholds actually observed: score **below 15** certified by a
psychiatrist or neurologist at CNP [S5 art. 11][S6 art. 21.1] and at Suravenir for neuro-degenerative
conditions [S7 defs]; **≤ 10** for AXA's psychic route to total dependence and **≤ 15** for its mixed
route, with **< 15** for partial and **< 18** for light dependence [S1 §2.2]; **≤ 15** and **≤ 10**
in the Sogecap tiers [R12 §1.2.1]. The Blessed test also appears in the market [R8 §3.2].

**(d) How the retrieved contracts actually define the two states.**

| Contract | Dépendance totale | Dépendance partielle |
|---|---|---|
| AXA Entour'Age [S1 §2.2] | definitive need of a third person **and** (≥4 of 5 AVQ; or dementia with Folstein ≤10 and prompting needed for ≥2 of 5 AVQ; or dementia with Folstein ≤15 and ≥3 of 5 AVQ). AGGIR not required | AGGIR group 1, 2 **or 3** **and** (≥3 of 5 AVQ; or dementia with Folstein <15) |
| Sogecap [R12 §1.2.1] | 4 of 5 AVQ; or 3 of 5 + Folstein ≤15; or 2 of 5 + Folstein ≤10 | 3 of 5 AVQ; or 2 of 5 + Folstein ≤15 |
| CNP *Ecureuil Assistance Vie* [S4] | ≥5 of 6 AVQ | ≥4 of 6 AVQ (plus an optional *légère* tier at ≥2 of 6) |
| CNP *MSPP* A063 F [S6 art. 21] | ≥5 of 6 AVQ, functional or psychic (MMSE <15) | ≥4 of 6 AVQ, same two routes |
| CNP *Banque de France* 0658 Q [S5 art. 13] | four levels on 6 AVQ: 2/6, 3/6, 4/6, 5-or-6/6; rente from level 3, doubled at level 4 | — (severity ladder, not a two-state design) |
| BPCE *AUTONOMIS* [S3] | GIR 1 or GIR 2 | GIR 3 or GIR 4 **and** constant third-party help for ≥2 of 4 AVQ |
| Suravenir / Crédit Mutuel [S7 defs] | GIR 1 or GIR 2 | GIR 3 or GIR 4 |
| Groupama [S8][S9] | AGGIR grid with an AVQ ladder of 2/6, 3/6, 4/6, 5-or-6/6 as a complement or alternative; exact contractual trigger not published | as above; partial pays 50% |
| OCIRP (collective, points) [R13 p19–20] | GIR 1 and 2 | GIR 3 only |

The CCSF's 30-contract sample found AGGIR-only and AVQ-only about equally common, with a significant
share combining both and a very small minority using a bespoke device; and it enumerated *dépendance
lourde* being defined as GIR 1–2, as GIR 1–2–3 subject to a cognitive score, as 3 AVQ of 4, as 5 AVQ
of 6, or as 3 AVQ of 4 together with 2 AIVQ of 4 [R8 §3.2]. Variability is greater for partial than
for total dependence [R8 §3.2].

Two design points matter for a model. First, a state must be **consolidated** — "non susceptible
d'amélioration", permanent and irreversible — before it is indemnifiable [S4][S6 art. 20][S2][S1
§2.2]. Second, the insurer is expressly **not bound by the public GIR decision**: "L'Assureur n'est
pas lié par les éventuelles décisions des services publics pour déterminer l'état et le degré de
dépendance de l'assuré" [S5 art. 13][S6 art. 21.1]. Contracts keyed to GIR still have their own
medical adviser classify the insured [S3][S7 p3]. The CCSF calls this misalignment useful for
insurability but a source of incomprehension for insureds who receive APA yet are refused by their
insurer, and its 2024 recommendation would remove it by paying automatically on APA at GIR 1 or 2
[R8 §3.2][R9 §I.C].

### 5. Waiting period (délai de carence / délai d'attente)
The three-way split by cause is close to universal.

| Contract | Accident | Other illness | Neuro-degenerative / psychiatric |
|---|---|---|---|
| AXA Entour'Age [S1 §1.1.5] | none | 1 year | 3 years ("maladie neurologique, neurodégénérative ou psychiatrique") |
| Antarius [S2] | none | 1 year | 3 years |
| BPCE AUTONOMIS [S3] | none | 1 year | 3 years ("maladie neurologique ou psychique") |
| CNP Ecureuil Assistance Vie [S4] | none | 1 year (functional) | 3 years (psychic) |
| CNP Banque de France 0658 Q [S5 art. 7] | none | 1 year | 3 years (psychiatric) |
| Sogecap [R12 §1.2.1] | none | 1 year | 3 years |
| Suravenir / Crédit Mutuel [S7 §3.2] | immediate | **not stated** in the retrieved conditions | 3 years ("neurologique, neuropsychique, neurovasculaire ou psychiatrique") |
| CNP MSPP A063 F (compulsory) [S6] | — | no *délai d'attente* clause appears in the notice | — |

Market summaries agree: nil or very short for accident, about one year for illness, up to three years
for neurological disease [R8 §2.2]; France Assureurs states the range as one to three years
[R11]. The consequence of a claim inside the waiting period is severe and consistent: no benefit is
ever payable for that state, **and the membership is terminated**, with premiums refunded in full
[S1 §1.1.4.2c][S3][S5 art. 7][S7 §3.2]. AXA extends this to a dependence-causing condition merely
*diagnosed* during the waiting period [S1 §1.1.4.2c]. The waiting period restarts on any increase in
cover [S1 §1.1.3][S7 §3.3][S2 by implication].

For pricing, [R12 §3.2.1] models the waiting period as coefficients S1 ≤ S2 ≤ S3 applied to the
incidence rate over the first three contract years, with S0 = 0% and S4 = 100%, plus a
*contre-assurance* item for the premiums refunded when dependence occurs during the waiting period.

### 6. Elimination period (délai de franchise)
- Three months, absolute, counted from the insurer's recognition of the state, is the standard.
  AXA: "un délai de franchise absolue de 3 mois, soit à compter du 91e jour qui suit la date de
  reconnaissance" [S1 §4.3.1.2]. Groupama: the rente begins "à partir du 91e jour" following
  recognition [S8]. Suravenir: "Le point de départ de la rente est fixé au 91ème jour qui suit la
  date de la reconnaissance" [S7 §4.2.1]. CNP: three months [S4][S5 art. 14][S6 art. 24], described
  in the A063 F notice and IPID as "90 jours" from recognition [S6 art. 26, IPID]. Sogecap: three
  months [R12 §1.2.1]. Antarius: three months, **but the first instalment equals three monthly
  rentes**, so the franchise is economically neutral [S2].
- Accident carve-out: CNP A063 F pays from the date of recognition itself where the cause is an
  accident, with no franchise [S6 art. 24].
- Generali pays its *capital d'équipement* with no franchise delay [S10].
- Market range: 30 to 90 days [R8 §2.2]; France Assureurs states "généralement 90 jours" [R11];
  GAD-labelled products carry a three-month franchise (fr = 3 in the pricing formulae) [R12 §3.2.1].
- The recognition step itself has its own lead time: CNP's medical adviser must rule within 45 working
  days of receiving a complete file, and the recognition date cannot precede the date the insurer
  received the claim [S6 art. 23–24].

### 7. The rente
- Form: *rente mensuelle viagère*, payable for as long as the insured state persists and at the
  latest until death [S1 defs "Rente"][S11]. It is **not** a fixed-term annuity and it is **not**
  payable after recovery: payment "cesse à la date de décès de l'assuré, ou lorsque du fait de
  l'amélioration de son état de santé, il ne se trouve plus dans un état de dépendance pour lequel il
  est garanti" [S1 §4.3.1.2][S6 art. 26][S7 §4.2.1].
- Payment timing: monthly *à terme échu* (in arrears) at AXA, CNP and Suravenir [S1 §4.3.1.2]
  [S5 art. 16][S6 art. 26][S7 §4.2.1].
- Amount ranges published by insurers:

| Insurer | Total dependence rente | Partial dependence rente |
|---|---|---|
| AXA Entour'Age [S1 §1.1.2.2a] | 500 – 3,000 €/month | 50% of the chosen amount |
| Generali [S10] | 500 – 3,000 €/month | 250 – 1,500 €/month |
| Sogecap [R12 §1.2.1] | 500 – 3,000 €/month, steps of 100 € | 50% |
| CNP Ecureuil Assistance Vie [S4] | 400 – 3,000 €/month, steps of 100 € | 60% (and 30% for the light tier) |
| Antarius [S2] | 300 – 2,100 €/month | 50% |
| Groupama [S8] | 200 – 2,000 €/month | 100 – 1,000 €/month (50%) |
| AG2R La Mondiale (market statement) [S11] | 300 – 4,000 €/month "selon les contrats" | not stated |
| CNP Banque de France 0658 Q [S5 annexe 1] | five fixed levels: 158.61 / 317.22 / 475.83 / 634.44 / 951.66 €/month at level 3, **doubled** at level 4 | — |
| CNP MSPP A063 F [S6 annexe 2] | 200 €/month | 100 €/month |
| OCIRP collective (points) [R13 p19] | guaranteed minimum 200 – 750 €/month for GIR 1–2 | 50% of it, 100 – 375 €/month, for GIR 3 |

  The partial/total ratio is therefore **50% in most designs**, 60% at CNP Ecureuil, and a doubling
  of the base rente at the top tier in the CNP severity-ladder design.
- The GAD label requires a **minimum rente of 500 €/month** for *dépendance lourde* [R11 criterion 4]
  [R8 §4.3].
- Amount actually paid = guaranteed amount × the revalorisation factor accumulated between adhesion
  and recognition × (if the membership had been resiliated after at least 8 full consecutive years)
  the reduction coefficient in force at recognition [S1 §4.3.1.1]. That three-factor formula is the
  cleanest statement of the mechanics found in any retrieved document.
- Deterioration from partial to total: a new claim file is required; the new amount takes effect from
  the first day of the month following the opening of the right; the total and partial rentes are
  mutually exclusive and recognition of total dependence never opens partial-dependence rights
  [S1 §4.3.1.2]. CNP allows the level to move in either direction on a fresh medical file [S5 art. 13].
  Note that [R12 §3.1.2] models no transition from partial to total at all, for want of a transition
  law, and instead prices two separate guarantees ("dépendance totale" and "dépendance toute cause").
- Continued entitlement: proof of life and of the persisting state is required — an annual document
  at AXA, whose non-return suspends payment with retroactive settlement on receipt [S1 §4.3.1.2]; an
  annual *déclaration sur l'honneur valant certificat de vie* each 1 January at CNP MSPP, failing
  which payment is suspended [S6 art. 23]. The insurer may re-examine the state at any time and stop
  payment if the insured refuses a medical control [S6 art. 24][S7 §4.2.1].

### 8. Capital d'équipement / capital premiers frais
- A one-off lump sum, paid once per membership, intended for equipment and home adaptation, but with
  free use in most contracts [S1 §4.3.2.1].
- Amounts: AXA 3,500 € [S1 §1.1.2.2c]; Antarius 3,000 € [S2]; CNP Ecureuil 3,000 € on total or
  partial and 900 € on the light tier, the latter deducted from any later payment [S4]; BPCE
  AUTONOMIS at most 3,200 € on total and 2,400 € on partial, net of earlier payments [S3]; Groupama
  reimbursement of up to 5,000 € of adaptation and equipment costs [S8]; Generali 5,000 € or 10,000 €
  under formula 3, paid with no franchise [S10]; Sogecap 5,000 € [R12 §1.2.1]; CNP Banque de France
  1,586.10 € to 9,516.60 € by coverage level [S5 annexe 1].
- Trigger, where it differs from the rente trigger: AXA pays it on *dépendance légère* if the option
  was taken inside the total-and-partial formula [S1 §4.3.2.1]; CNP Banque de France pays it at
  severity level 2 (3 AVQ of 6), two levels below the rente trigger [S5 art. 17]; Suravenir pays half
  on partial dependence and the balance on deterioration [S7 tableau des garanties]; Antarius may pay
  it on a "Dépendance sensible" below the rente threshold [S2].
- Once paid, the guarantee is extinguished regardless of later deterioration [S1 §4.3.2.1][S2]
  [S5 art. 17].

### 9. Assistance services
- Included from inception in every retrieved individual contract and treated as a *prestation en
  nature* subject to an obligation of means, not of result [S1 §7.2.2].
- Providers observed: AXA Assistance / Inter Partner Assistance [S1], IMA Assurances [S3],
  FILASSISTANCE (a CNP subsidiary) [S5 art. 18], Europ Assistance [S10].
- Typical content, as catalogued by the CCSF across the market: information and prevention before
  onset; then teleassistance, meal delivery, medicine delivery, home help, sitting services, help
  with moving house, pet care, hairdressing at home, memory assessment and training, an
  ergotherapist's home-adaptation assessment, help finding an establishment, legal and social
  support, and carer respite [R8 annexe 2][S1 ch. 3–5][S8][S10][R13 p24].
- Assistance is the first thing lost on *mise en réduction*: "La mise en réduction des garanties met
  fin aux prestations d'assistance" [S1 §1.3]; the same at CNP [S5 art. 24.2].

### 10. Premiums — *cotisation viagère révisable*
- The premium is level for the entry age but payable **for life**, or until dependence: there is no
  premium-paying term. Rating factors are age at entry (by *différence de millésimes* at AXA), the
  covers and rente level chosen, health at entry, and the formula [S1 §1.2.1][S7 §4.4]. Payment is in
  advance, monthly, quarterly, half-yearly or annually [S1 §1.2.2][S5 art. 21][S2].
- **Exoneration on claim**: premiums cease from the premium due date following recognition of the
  state [S1 §1.2.4][S5 art. 21][S6 art. 18][S4]. Suravenir adds the symmetric rule — the premium
  becomes due again if the insured leaves the dependent state [S7 §4.4].
- **The tariff is revisable for the whole portfolio.** This is the defining feature of the product
  and it is stated plainly in the retrieved documents:
  - AXA: beyond the annual increase that follows the revalorisation of guarantees, the premium "pourra
    être modifié sur proposition du comité de gestion paritaire … en cas de modifications des
    engagements d'AXA consécutives à une décision législative, réglementaire ou fiscale, si les
    résultats techniques et/ou financiers du contrat Entour'Age le requièrent ou encore à raison des
    évolutions constatées ou projetées des statistiques nationales relatives à la dépendance"
    [S1 §1.2.3]. The counterpart protections: "Aucune modification de votre cotisation ne pourra être
    effectuée en raison de l'âge de l'assuré ou de la détérioration de son état de santé", and the
    member may refuse by cancelling optional covers or resiliating within two months of notification,
    with a possible *mise en réduction* at the same date [S1 §1.2.3].
  - CNP Banque de France, art. 22 "Révision des cotisations": "Le barème des cotisations applicable
    aux Assurés pourra aussi être révisé par l'Assureur en fonction de l'évolution des résultats",
    with the member free to modify or terminate the membership [S5 art. 22].
  - Suravenir: where a legislative or regulatory decision changes the insurer's commitments, or if the
    overall results of the contract prove loss-making, the insurer may adapt either the premium rate
    or the guarantees; in the latter case **the increase in the premium rate may not exceed 10% per
    year**, excluding revalorisation, and the member may then ask for a reduction of the guaranteed
    rente or resiliate with one month's notice [S7 §4.4]. This 10% cap is the only numerical limit on
    tariff revision found in any retrieved document.
- Discounts: 10% permanent couple discount at AXA when both spouses join within three months, lost if
  either contract is resiliated or reduced [S1 §1.2.6]; 10% on the two premiums combined at CNP Banque
  de France when a couple joins within six months [S5 art. 21]; 10% at Groupama [S8].
- Non-payment: the group-contract machinery of art. L.141-3 — a registered letter, then exclusion 40
  days after it is sent [S1 §1.2.5][S5 art. 23][S6][S7 §4.4].
- Sogecap indexes the premium annually on the growth of the *PASS* [R12 §1.2.1]; Suravenir and CNP
  Banque de France index it in the same proportion as the guarantees [S7 §3.4][S5 art. 21].

**Published premium figures.**
- CNP Banque de France 0658 Q, annual premium including tax for *couverture 1* (a rente of 158.61 €
  per month at severity level 3, doubled at level 4), by age at entry; multiply by the coverage level
  (1 to 5) and add 10.80 €/year of compulsory assistance cover [S5 annexe 1]:

  | Age at entry | Rente cover, €/yr | Rente cover, €/month | Capital "Premières Dépenses", €/yr |
  |---|---|---|---|
  | ≤50 | 99.12 | 8.26 | 15.60 |
  | 55 | 123.48 | 10.29 | 19.44 |
  | 60 | 156.60 | 13.05 | 25.56 |
  | 65 | 201.24 | 16.77 | 33.84 |
  | 70 | 263.04 | 21.92 | 46.32 |
  | 74 | 333.24 | 27.77 | 60.72 |

  The scale is published for every integer age from "50 ans ou moins" to 74. Its shape is the useful
  part: the premium roughly **3.4×** between age 50 and age 74, an average compounding of about 5.2%
  per year of entry age.
- Groupama worked example: the total-and-partial formula with a 400 €/800 € rente costs 53–76 €/month
  without the capital option and 62–89 €/month with it, for entry ages 55 to 65 [S8].
- CCSF indicative market pricing (2013): 1,000 €/month of total-dependence rente plus 500 €/month of
  partial-dependence rente for **35 €/month from age 50, 50 €/month from age 60 and 75 €/month from
  age 70** [R8 §2.2].
- Market averages 2024 for contracts whose sole and principal guarantee is dependence: **472 €/year
  (39 €/month)** for individual memberships and **106 €/year (9 €/month)** for collective ones
  [R10 §2.3][R13 p6]; GAD-labelled contracts average **584 €/year** [R10 §2.3]. Chart-read from the
  same release: about **308 €/year** for *dépendance lourde* cover alone and about **535 €/year** for
  *dépendance lourde et partielle* [R10 p14 charts].
- CNP MSPP A063 F, a compulsory group cover of 200 €/100 € per month, costs **20.40 €/year
  (1.70 €/month)** per insured person — an order of magnitude below individual pricing, which is the
  mutualisation effect the CCSF is arguing for [S6 annexe 2][R9 §1].

### 11. No surrender value; *mise en réduction* / *maintien partiel des garanties*
- **There is no surrender value.** AXA states it in one line: "Votre adhésion ne comporte pas de
  valeur de rachat" [S1 §7.3]. No retrieved contract offers a *rachat*. If the insured stays
  autonomous until death, nothing is paid and the premiums are lost — the *fonds perdu* character
  [S11].
- What replaces it is a paid-up reduction after a qualifying number of years of premiums:

| Contract | Qualifying period | Effect |
|---|---|---|
| AXA Entour'Age [S1 §1.3] | **8 full consecutive years** | on resiliation, partial maintenance of the rente dépendance and of the Capital Premiers Frais through a *barème* whose coefficients depend on the number of years already paid; amounts may be adjusted, while no claim has occurred, by the joint committee in the light of the contract's technical and financial balance; assistance benefits end |
| Antarius [S2] | **8 full years** | contract maintained with a reduced rente per the scale in force at the reduction date |
| Suravenir / Crédit Mutuel [S7 §4.6] | **8 years** | reduced guarantee on total dependence; amount determined at the claim date as a function of the amount and number of years of premiums paid; **reduced guarantees are no longer revalued**; a value quoted at the reduction date is indicative only |
| Sogecap [R12 §1.2.1] | **8 years** | before 8 years the membership is resiliated with no maintenance; after 8 years the membership is *réduite*, the capital d'équipement option is removed, and the reduced cover applies to **total dependence only** |
| CNP Banque de France 0658 Q [S5 art. 23–24.2] | **5 years** | on resiliation or non-payment the rente right is partially maintained at the initial rente × the *coefficient de maintien* of annexe 2; the *barème* is revisable annually on the same terms as premiums; the capital premières dépenses and the assistance benefits are lost |

- CNP Banque de France publishes the actual reduction scale (annexe 2, in force 1 January 2012)
  [S5 annexe 2]:

  | Years of premiums | Coefficient | Years | Coefficient | Years | Coefficient |
  |---|---|---|---|---|---|
  | 5 | 16% | 14 | 38% | 23 | 56% |
  | 6 | 18% | 15 | 40% | 24 | 58% |
  | 7 | 21% | 16 | 42% | 25 | 60% |
  | 8 | 25% | 17 | 44% | 26 | 62% |
  | 9 | 28% | 18 | 46% | 27 | 64% |
  | 10 | 30% | 19 | 48% | 28 | 66% |
  | 11 | 32% | 20 | 50% | 29 | 68% |
  | 12 | 34% | 21 | 52% | ≥30 | 70% |
  | 13 | 36% | 22 | 54% | | |

  The scale is roughly linear at about 2 percentage points per extra year from year 10, starts at 16%
  after five years and is capped at 70%. It is the only published French LTC reduction scale found.
- The GAD label requires "des conditions de maintien des droits en cas d'interruption de paiement des
  cotisations" as one of its nine criteria [R11 criterion 9][R8 §4.3]; the CCSF criticised insurers
  for not highlighting the *valeur de réduction* clearly enough [R8 §4.2].
- Contrast: the OCIRP points-based collective guarantee applies **no reduction value at all** — the
  points already bought stay bought and the cover is maintained for life even if contributions stop
  [R13 p31].

### 12. Revalorisation
Two distinct indexations must be modelled, and both are discretionary in every retrieved contract.

- **The guaranteed rente before a claim** (*revalorisation des garanties*): the amount inscribed at
  outset grows by a rate declared by the insurer, and **the premium rises in the same proportion**
  [S1 §1.2.3][S7 §3.4][S5 art. 21]. The amount actually paid at claim is the original guarantee
  multiplied by the accumulated revalorisation factor [S1 §4.3.1.1].
- **The rente in payment** (*revalorisation des prestations / des rentes en service*):
  - AXA: revalued each year, at the latest on 1 April, by decision of the joint ANPERE/AXA management
    committee [S1 §4.3.1.3, §8.1].
  - CNP Banque de France: each 1 January, by reference to the rate applied to Banque de France
    pensions — that is, the rate applied to French civil and military retirement pensions — subject
    to the availability of the *fonds de revalorisation*; and, if the group contract is resiliated, by
    reference to the change in the **AGIRC pension point** [S5 art. 15, art. 25].
  - Suravenir: each 1 January by reference to the annual change in the **AGIRC point value**, within
    the capacity of a revalorisation fund fed by **36% of any surplus** on the contract's result
    account [S7 §4.2.3].
  - CNP MSPP: only "par un accord entre l'Assureur et le Souscripteur, sous réserve des résultats du
    Contrat" [S6 art. 16].
  - Sogecap: rates for guarantees and for benefits determined from the contract's technical and
    financial results [R12 §1.2.1].
- Reduced (paid-up) guarantees are **no longer revalued** at Suravenir [S7 §4.6].
- The CCSF flagged exactly this as the market's weakest disclosure: revalorisation "en fonction des
  résultats techniques et financiers" is opaque to buyers, and consumer bodies complain that insureds
  are not warned about the monetary erosion of a promised rente, which can be substantial over fifteen
  or twenty years at 2% average inflation [R8 §3.3]. A modeller should therefore treat the
  revalorisation rate as a management action, not a contractual index.

### 13. Exclusions and territorial scope
- The recurring exclusion set: intentional acts and attempted suicide; use of narcotics or of
  medicines not medically prescribed; blood alcohol above the criminal threshold of art. L.234-1 of
  the Code de la route, and the physical or neuropsychiatric complications of chronic alcohol abuse;
  civil or foreign war, riot, insurrection, terrorism where the insured takes an active part (with
  legitimate defence and assistance to a person in danger carved back in); nuclear transmutation and
  radioactivity; motorised competitions, record attempts and their trials; and unapproved air sports
  [S1 §7.1][S3][S4][S6 art. 22][S7 §3.5]. The burden of proving an exclusion lies on the insurer
  [S1 §7.1].
- Disease-specific exclusions are rare but do exist: BPCE AUTONOMIS excludes dependence resulting
  from fibromyalgia, chronic fatigue syndrome, Ehlers-Danlos disease and fasciitis [S3].
- Territory: AXA requires the insured and the carer to reside in metropolitan France, Monaco or a DOM
  [S1 §1.1.6]; CNP Ecureuil requires principal residence in metropolitan France or DOM/TOM [S4];
  Suravenir grants cover in metropolitan France with recognition performed in France or an EU country
  by an expert doctor accepted by the insurer [S7 §3.6]; Antarius covers travel of up to three
  consecutive months elsewhere provided the state is medically established in metropolitan France
  [S2]; BPCE covers the world with stays outside France of no more than three continuous months [S3];
  CNP MSPP allows stays outside the EU of at most 90 days a year in aggregate and pays only from the
  insured's return to France, so that medical control can be exercised [S6 IPID].

### 14. Claim recognition and ongoing control
- Process: the insured or a relative obtains a claim form — CNP calls it the *attestation médicale
  d'état de dépendance* (AMED) — which is completed with the treating or hospital doctor and sent
  under confidential cover to the insurer's *médecin-conseil* [S5 art. 19][S6 art. 23].
- The insurer's medical adviser decides the state and its level, and sets the date on which the state
  reached an indemnifiable level; that date cannot precede the date the insurer received the claim
  [S6 art. 23–24]. CNP MSPP commits to 45 working days from a complete file [S6 art. 24].
- The insurer may require additional medical information or an examination by a doctor of its choice,
  at claim and at any time thereafter; refusal means refusal or cessation of benefit [S6 art. 24]
  [S1 §2.2][S7 §4.2.1].
- A medical arbitration procedure exists (each side's doctor, then a third, whose fees fall on the
  losing party) [S5 art. 20].
- Any state whose recognised date of onset precedes the effective date of the cover gives no benefit
  at all [S6 art. 24].
- Practical point flagged in every source: the insured is often no longer able to claim, so the
  contracts and the CCSF both urge that relatives be told the contract exists [S7 "Quelques
  conseils"][R8 §4.4].

### 15. Taxation
- The rente is **not** subject to income tax when the contract is written outside the *Madelin*
  framework: "En cas de vie de l'assuré, la rente versée n'est pas imposable au titre de l'imposition
  sur le revenu" [S1 §1.1.1]. Groupama makes the same statement [S8].
- If the membership is concluded under the *loi Madelin* of 11 February 1994, premiums are
  tax-deductible and the rente becomes taxable as *pensions et rentes viagères à titre gratuit*
  [S1 §1.1.1].
- Optional death capital: exempt from inheritance duty and taxation where the designated beneficiary
  is the spouse, PACS partner, or a sibling meeting the three statutory conditions (single, widowed,
  divorced or legally separated; over 50 or unable to work through infirmity; having lived with the
  deceased throughout the five years preceding death); other beneficiaries fall under CGI arts. 757 B
  and 990 I [S1 §1.1.1].

### 16. Public context — APA, prevalence, incidence
This is the demographic backdrop a French LTC model has to reproduce, and, in the absence of public
insurer experience tables, the best public proxy for incidence and continuance.

- **The public benefit.** The APA is paid to people aged 60 or over classified in GIR 1 to 4
  [R2 arts. R232-1, R232-4]. Monthly *plan d'aide* ceilings from 1 January 2026: GIR 1 **2,080.33 €**,
  GIR 2 **1,682.30 €**, GIR 3 **1,215.99 €**, GIR 4 **811.52 €** [R4]. The beneficiary contributes
  nothing up to a monthly income of 933.89 €, between 0% and 90% from 933.90 € to 3,439.31 €, and 90%
  above [R4]. For scale, the ceilings at 1 April 2013 were 1,304.84 / 1,118.43 / 838.83 / 559.22 €
  [R8 §1.2] — a rise of about 55% over roughly thirteen years.
- **Take-up and the gap.** Average amounts actually granted are well below the ceilings and are then
  reduced by the *ticket modérateur*: at 31 December 2011 the average paid was 748 / 576 / 430 /
  263 €/month for GIR 1 / 2 / 3 / 4 [R8 §1.2]. Heavy dependence at home cost about 1,800 €/month and
  in an establishment about 2,300 €/month in 2013 [R8 §1.2]; the *reste à charge* in an EHPAD was
  about **1,957 €/month** per a DREES study of July 2022, roughly 120% of the average gross pension
  and 90% of the median net salary [R9 §2].
- **Counts (DREES, end 2023)** [R7]:
  - **1,364,700** people received APA for December 2023, up 2.1% in a year: 815,800 at home and
    549,000 in establishments (40%).
  - APA spending 2023: **7,058 M€** (4,293 M€ at home, 2,693 M€ in establishments, 72 M€ other).
  - GIR distribution of beneficiaries: **at home** 2% GIR 1, 18% GIR 2, 22% GIR 3, 58% GIR 4; **in
    establishments** 13% / 44% / 19% / 24%. So 20% of home beneficiaries and 57% of establishment
    beneficiaries are in severe loss of autonomy (GIR 1–2).
- **Prevalence by age and sex (DREES, end 2023)** [R7]:
  - 7.2% of people aged 60 or over receive APA; 9.1% of women against 4.8% of men; 70% of
    beneficiaries are women.
  - Up to age 79 the rate is **2.3%**; between 80 and 89 it is **17%** (20% of women, 13% of men); at
    85 or over, **35%**; from 90, about **half** the population (54% of women, 40% of men).
  - Departmental dispersion of the 60+ rate: 3.3% to 11.3%.
  - Among home beneficiaries, the share aged 90 or over is 35% in GIR 1 against 25% in GIR 4, and the
    under-65 share runs from 0.6% (GIR 1) to 2.1% (GIR 4). In establishments the age profile is nearly
    flat across GIRs, with 45–47% aged 90 or over.
- **Duration (DREES)** [R7]: at end 2022 a person aged 60 had a life expectancy of **25.8 years**, of
  which on average **2.4 years (9.5%)** were spent as an APA beneficiary. In 2019 that was **3.4 years
  (12.2%)** for women against **1.4 years (6.0%)** for men. APA life expectancy has drifted down from
  30 months in 2010 to 29.2 months in 2022, so take-up at a given age is falling.
- **Onset and duration for heavy dependence** [R9 §2]: mean age at onset of total dependence about
  **78 for men and 84 for women**; mean duration of receipt of the allocation for heavy dependents
  (GIR 1–2) about **three years**. France Assureurs reports a mean **age at onset of 80** across
  individual contracts whose sole guarantee is dependence [R10 §2.3][R13 p6].
- **Projection** [R9 introduction, citing INSEE *Tableaux de l'économie française* 2020]: on unchanged
  trends France (excluding Mayotte) would have **4 million** seniors in loss of autonomy in 2050,
  16.4% of the 60+ against 15.3% in 2015; those in severe loss of autonomy would be 4.3% of the 60+
  against 3.7% in 2015. The earlier CCSF report gave 1.15 million dependent people in 2010 on the APA
  definition and a central scenario of a doubling by 2060 [R8 §1.1].
- Total national dependence spending is about **30 Md€**, before valuing informal carers' work at an
  estimated 7–18 Md€ (2014); the Libault report of 2019 put the additional annual funding needed by
  2030 at about **10 Md€** [R9 introduction].

### 17. Market size (France Assureurs, 2024 financial year, published July 2025)
All figures from [R10 §2.3], cross-checked against [R13 p6] because the source PDF drops the glyph
"8" from its body text (see the note on R10).

- **2.4 million** people covered against the dependence risk **by insurance companies** at end 2024,
  down **6.9%** on the year after −2.6% in 2023. Individual memberships, two thirds (66%) of the
  portfolio, fell 9.9%; collective cover was flat at −0.4%.
- Of those covered: **58%** under a contract carrying only a dependence guarantee, 17% through a
  health contract with compulsory inclusion, 23% through a contract coupling dependence with another
  guarantee, 2% other.
- Across the **whole** market (mutuelles, insurance companies and *institutions de prévoyance*)
  **6.0 million** people were insured against the dependence risk in 2024 — 56% by mutuelles, 40% by
  insurance companies, 4% by institutions de prévoyance [R13 p6].
- **28,400** new subscribers in 2024, down 13.7% after −29.5% in 2023. 82% were individual, and eight
  in ten of those took a contract whose sole and principal guarantee is dependence. Typical
  subscription age **64**.
- Premiums **618.1 M€**, down 3.0%. Individual memberships are 90% of the total; contracts whose sole
  and principal guarantee is dependence account for 88% of premiums (543 M€).
- Benefits paid **357.3 M€**, up 6.3%.
- **44,200** rentes in payment on sole-and-principal-guarantee contracts, of which **41,900** on
  individual memberships; mean age at onset **80**; **mean monthly rente in payment 583 €**.
- Technical provisions **6.4 Md€** at 31 December 2024, down 1.9% and falling for the third
  consecutive year.
- **GAD-labelled** contracts: 194,900 people covered at end 2024 (+1.3%), 8,600 new memberships
  (−16.1%), premiums 113.8 M€ (+3.4%), average annual premium 584 € (+12%). They are 14% of insureds
  holding a sole-and-principal-guarantee dependence contract but 38% of new business in that category.
- CCSF's own aggregate, spanning all three families of insurer: **814 M€** of premiums for
  **2.64 million** people covered by dependence contracts, 28% of them collective, of which
  **1.48 million** under specific dependence contracts [R9 §1].
- DREES puts dependence cover at about 1% of the premiums private insurers collect for social risks,
  inside 17.8 Md€ of "other bodily-injury guarantees" [R14].
- Consumer awareness (France Assureurs survey, 2021, quoted in [R13 p4–5]): 82% of French people think
  it important to protect against the risk, but only about **one in ten** holds a contract, a majority
  does not know the product exists, most held contracts carry a rente **below 500 €/month**, and 52%
  would like the cover to be compulsory.

### 18. Actuarial framing for a projection model
From [R12], the only actuarial document retrieved that sets out the mechanics in full.

- **State space.** Autonomous → dependent → dead. Recovery is assumed impossible (the probability of
  return to autonomy is set to zero), and no transition from partial to total dependence is modelled
  because no transition law is available; instead two guarantees are priced separately, "dépendance
  totale" and "dépendance toute cause" [R12 §3.1.1–3.1.3]. This is an important simplification to
  carry into the reference implementation, because the contracts themselves *do* provide for
  deterioration [S1 §4.3.1.2][S5 art. 13].
- **Laws required**, all by sex S and age x [R12 §3.1.3]:
  - mortality of an autonomous life who dies without entering dependence, q^{D,S}_x;
  - mortality of a dependent life t years after entry at age x, q^{D,S}_{x,t} — duration-dependent,
    which is what makes LTC a *loi de maintien* problem rather than an annuity problem;
  - incidence, i^{D,S}_x, the probability that an autonomous life enters dependence;
  - lapse, ρ, the probability that the insured stops paying premiums.
  - Survival in the autonomous state is p^{D,S}_x = (1 − q^{D,S}_x)(1 − i^{D,S}_x)(1 − ρ); survival in
    dependence is p^{D,S}_{x,t} = 1 − q^{D,S}_{x,t}.
- **Waiting period**: coefficients S1 ≤ S2 ≤ S3 scale the incidence rate over the first three contract
  years, with S0 = 0% and S4 = 100%, plus a *contre-assurance* term for premiums refunded when
  dependence occurs inside the waiting period [R12 §3.2.1].
- **Franchise**: the annuity factor for a monthly rente in arrears with a franchise of *fr* months is
  built by splitting the first year into months and dropping the instalments falling inside the
  franchise —
  a^{(m),D,S}_{x,0} = v·p^{D,S}_{x,0}·a^{(m),D,S}_{x,1} + (1/m)·Σ_{k=1..m} v^{k/m}·₁₂ₖ/ₘp^{D,S,mens}_{x,0}·1(12k/m > fr)
  — with a monthly mortality table for the first year in dependence, and Tsapbaze's approximation for
  later years [R12 §3.2.1, eq. 3.1]. GAD-labelled products take fr = 3 [R12 §3.2.1].
- **Unisex pricing** is compulsory since the 2004 EU Council directive; [R12 §3.2.1] handles it by
  assuming a male proportion α^H_x that is constant at k1 up to an age x1 and then falls by one
  percentage point per year of age.
- **Loadings**: r on the rente payments (proportion of the rente), g for the risk taker (proportion of
  the reinsurance premium), θ for management and commission (proportion of the premium)
  [R12 §3.2.1].
- **Provisions** [R12 §3.2.2]:
  - *Provision pour risques croissants* (PRC) for autonomous insureds — the present value of future
    commitments less the present value of future premiums, allowing for the waiting-period incidence
    reduction and for the counter-insurance of premiums; computed separately for the rente and the
    capital benefits.
  - *Provision mathématique des rentes* for rentes in payment.
  - A *provision d'aggravation* for partial dependents who may become total exists in principle but is
    not used under the two-guarantee model.
  - The Code des assurances article that governs the PRC (R343-3) was **not retrieved** — see R18 — so
    none of this is cited to the code.
- **Reinsurance**: quota-share treaties are usual on this risk; the Sogecap product cedes 70% (40% to
  a lead reinsurer, 30% to a follower) [R12 §1.2.1].
- **Capital**: LTC sits in the Solvency II **Health-SLT** underwriting module; [R12] projects the SCR
  through incidence and longevity shocks combined with the contractual right to increase premiums
  [R12 §1.1.2.1, ch. 4].
- **Rate sensitivity**: the acquisition values of a points-based LTC guarantee are markedly sensitive
  to the technical rate, the more so the younger the insured — which is the collective market's main
  pricing lever [R13 p29–30].

---

## Variations across insurers

| Feature | AXA *Entour'Age* [S1] | Antarius / SG [S2] | BPCE *AUTONOMIS* [S3] | CNP *Ecureuil Assistance Vie* [S4] | Suravenir / Crédit Mutuel [S7] | Groupama *Autonomie* [S8][S9] | Sogecap [S12/R12] |
|---|---|---|---|---|---|---|---|
| Trigger grid | 5 AVQ + Folstein; AGGIR only for partial/light | not published on the IPID | **GIR only** (+2 of 4 AVQ for partial) | 6 AVQ | **GIR only** (+MMSE for neuro) | AGGIR with a 6-AVQ ladder | 5 AVQ + Folstein |
| Total dependence | ≥4/5 AVQ, or dementia routes | "certains actes" (unspecified) | GIR 1–2 | ≥5/6 AVQ | GIR 1–2 | not published | 4/5, or 3/5+F≤15, or 2/5+F≤10 |
| Partial dependence | AGGIR 1–3 **and** ≥3/5 AVQ | optional, 50% | GIR 3–4 **and** ≥2/4 AVQ | ≥4/6 AVQ → **60%** | GIR 3–4 → 50% | 50% | 3/5, or 2/5+F≤15 → 50% |
| Light tier | *Dépendance légère* (capital only) | "Dépendance sensible" (capital) | — | ≥2/6 AVQ → 30% of rente + 900 € | — | — | — |
| Rente range | 500–3,000 € | 300–2,100 € | per certificate | 400–3,000 € (steps of 100 €) | per bulletin | 200–2,000 € | 500–3,000 € (steps of 100 €) |
| Capital | 3,500 € (option) | 3,000 € | ≤3,200 € total / ≤2,400 € partial | 3,000 € (900 € light) | option, half on partial | ≤5,000 € reimbursement | 5,000 € (option) |
| Age at entry | 40–75 | 50–<75 | not stated on the IPID | not stated on the IPID | <75 | from 40, generally not after 77 | 50–<75 |
| Carence (accident / illness / neuro) | 0 / 1 yr / 3 yrs | 0 / 1 yr / 3 yrs | 0 / 1 yr / 3 yrs | 0 / 1 yr / 3 yrs | 0 / **not stated** / 3 yrs | not published | 0 / 1 yr / 3 yrs |
| Franchise | 3 months (91st day) | 3 months, **first payment = 3 rentes** | not stated on the IPID | 3 months | 91st day | 91st day | 3 months |
| Reduction after | 8 full consecutive years | 8 full years | not stated on the IPID | not stated on the IPID | 8 years, reduced rente **not revalued** | not published | 8 years, **total dependence only**, capital option lost |
| Surrender value | none, stated expressly | none | none | none | none | none | none |
| Rente in payment indexed to | joint committee, by 1 April | not stated | not stated | not stated | **AGIRC point**, fund fed by 36% of surplus | not published | technical and financial results |
| Tariff revision cap | none stated | not stated | not stated | not stated | **10% per year** excluding revalorisation | not published | not stated |
| Couple discount | 10% | not stated | not stated | not stated | not stated | 10% | not stated |

Two further designs sit outside the individual-rente family and are worth recording as market
context, not as candidates for the reference implementation:

- **Severity-ladder contracts.** CNP's Banque de France contract 0658 Q pays nothing at 2 or 3 AVQ of
  6 except the equipment capital, the base rente at 4 of 6, and **double** the base rente at 5 or 6
  of 6, across five subscribed coverage levels [S5 arts. 13, 16, 17, annexe 1]. This is the same
  four-rung AVQ ladder Groupama documents [S9], monetised differently from the two-state designs.
- **Points-based collective cover.** The OCIRP guarantee is a defined-contribution deferred rente
  expressed in points: contributions buy points at an age-dependent (or mutualised) *valeur
  d'acquisition*; on recognition the rente equals points × *valeur de service*. The final rente is
  unknown at inception and keeps growing while contributions continue; contributions run at
  0.40%–1.50% of the PMSS; the guaranteed minimum is 200–750 €/month for GIR 1–2 and half of it for
  GIR 3; and — unlike every individual contract above — **no reduction value applies if contributions
  stop** [R13 p17–21, 31]. The recognition rules are also different: automatic on APA at GIR 1–2, and
  otherwise requiring inability to perform 2 or 3 of 4 everyday acts for more than three months
  [R13 p20].

**Representative design for the reference implementation.** AXA *Entour'Age* [S1] is the cleanest
representative of the individual market: group contract with facultative membership, entry 40–75,
a chosen *rente mensuelle viagère* of 500–3,000 €, a *dépendance totale* trigger on 4 of 5 AVQ with
cognitive alternatives, an optional *dépendance partielle* at 50%, an optional 3,500 € *Capital
Premiers Frais*, waiting nil/1 year/3 years by cause, a 3-month absolute franchise, monthly payment
in arrears, discretionary annual revalorisation of both the guarantee and the rente in payment, a
premium that is level for the entry age but revisable for the portfolio, no surrender value, and a
paid-up reduction after 8 years. Antarius, Sogecap, CNP Ecureuil and Generali differ mainly in
parameter bounds; BPCE and Suravenir differ structurally only in swapping the AVQ trigger for a GIR
trigger, which is a change of decrement definition rather than of cash-flow engine.

---

## Gaps and caveats

1. **ACPR could not be reached at all.** Both the news page on the lessons of ACPR's LTC supervisory
   inspections [R15] and the September 2023 *Revue de l'ACPR* article on assurance dépendance [R16]
   return HTTP 403 — twice via WebFetch each, and, for R16, also to a curl request carrying a browser
   User-Agent, Accept-Language and Referer. The host serves an HTML error page rather than the PDF.
   Nothing from either document is cited. This is the single largest hole in these notes: the
   supervisor's own view of pricing adequacy, provisioning practice and claims handling on this
   product is missing.
2. **DGCCRF fiche pratique** [R17] likewise returns HTTP 403 on economie.gouv.fr; the consumer-law
   summary of the product is therefore absent.
3. **The Code des assurances article on the *provision pour risques croissants* was not retrieved.**
   The code's identity and version were confirmed [R18] but the *partie réglementaire* is not exposed
   on that page and article R343-3 could not be reached. Everything said about the PRC in section 18
   rests on [R12], an actuarial dissertation, not on the code.
4. **No public French LTC incidence or continuance table exists in these notes.** [R12] specifies the
   structure of the laws a model needs — i_x, q_{x,t} by duration since onset, and a lapse rate — but
   its numerical bases are the insurer's own experience tables and are not disclosed (the dissertation
   carried a two-year confidentiality marking). No BCAC-style published reference table for
   *dépendance* was located, and none is asserted here. The frlib decrement tables for this product
   will have to be `[std]` proxies calibrated to public APA prevalence [R7] and to the market's own
   observed averages (mean onset age 80, mean rente 583 €/month [R10]).
5. **The Sogecap product document does not exist in these notes.** S12 is a specification read out of
   [R12], not out of a Sogecap notice; no Sogecap *notice d'information*, *conditions générales* or
   IPID was located. Every S12 fact is tagged [R12] at the point of use.
6. **Insurers named in the brief that could not be sourced.** No Malakoff Humanis, Macif or April
   dependence contract document was retrieved. The only Malakoff Humanis document found was the
   *Autonomie +* brochure (https://www.centraider.fr/wp-content/uploads/2023/11/brochure-autonomie-malakoff-humanis.pdf,
   retrieved), which describes a free Agirc-Arrco social-action service, **not** an insurance
   contract, and is therefore not used as a primary source. La Banque Postale's *Protectys Autonomie*
   is referred to by third-party comparison sites as offering 500–4,000 €/month; that range is
   **[unverified]** — no La Banque Postale or CNP document for that contract was retrieved.
7. **Two insurer sources are product web pages, not notices.** Groupama [S8][S9], Generali [S10] and
   AG2R La Mondiale [S11] are cited from insurer marketing and explanatory pages. Their figures
   (rente ranges, entry ages, premium illustrations, capital amounts) are the insurer's own published
   statements and are reliable at that level, but they are not contractual wording, and the carence,
   franchise and reduction terms of those contracts remain **unconfirmed** except where the page says
   so explicitly.
8. **The Suravenir / Crédit Mutuel conditions are of 2013-12 vintage** (the file path dates them; no
   printed edition date appears in the extracted text) and no illness waiting period other than the
   three-year neurological one appears in the retrieved text — either the contract genuinely has none
   for ordinary illness, or a bullet was lost in the two-column layout. Treat the "not stated" cell in
   the variations table literally: it means the retrieved document does not state it, not that it is
   zero.
9. **Antarius is of November 2019 vintage** [S2] and BPCE AUTONOMIS carries no visible edition date
   [S3]. Both are IPIDs, which by construction summarise and omit; neither states entry-age limits
   (BPCE) or reduction scales (BPCE) in full.
10. **The France Assureurs report drops a glyph.** Both PyMuPDF and pypdf drop the digit "8" from the
    body text of [R10] (subset font). Every affected figure quoted here was reconstructed and then
    independently confirmed against [R13], which quotes the same release. The two per-cover average
    premiums (≈308 € and ≈535 €) were read off a chart by coordinate rather than from running text and
    are flagged as such.
11. **The GAD label's own rule book was not retrieved.** The nine criteria are quoted from the
    label's publisher [R11] and from the CCSF's reproduction of them [R8 §4.3]; annexe 3 of [R8], the
    label's common vocabulary of thirteen terms, is a set of page images whose text could not be
    extracted. Whether any specific contract above is GAD-labelled is **[unverified]** — no retrieved
    notice claims the label.
12. **CCSF market structure data is from 2010–2013** [R8]. The CTIP contract-type headcount, the
    30-contract grid survey, the APA ceilings and the indicative premium points all date from that
    report and are quoted with their dates. They are used for *structure*, not for current levels;
    current levels come from [R4], [R7], [R9], [R10] and [R13].
13. **Prevalence is APA take-up, not medical prevalence.** All the [R7] figures measure receipt of the
    APA, which requires an application. DREES notes that APA life expectancy has fallen from 30 to
    29.2 months between 2010 and 2022 "traduisant un recours à cette prestation en baisse à âge
    donné" [R7] — that is, a behavioural drift, not necessarily a health improvement. Insurance
    incidence is a different quantity again, because insurer definitions are deliberately stricter
    than GIR 1–4 [R8 §3.2].
14. **No rate card is public.** The only published premium scale found is the CNP Banque de France
    annexe 1 for a specific 2018-vintage group contract [S5]; the Groupama illustration [S8] and the
    CCSF's indicative pricing [R8] are the only other price points. No insurer publishes a general
    individual LTC rate table, and none of the retrieved documents discloses a technical rate,
    loading, or profit-sharing rule.
15. **Legifrance rendering of the AGGIR annexe is partial.** The fetched view of annexe 2-1 [R1]
    returned the ten discriminant and seven illustrative variables, the A/B/C modalities and the GIR
    profiles, but did not spell out GIR 6 as a separate profile, and it did not return annexe 2-2, the
    *mode de calcul unique* that turns the variable scores into a GIR. The GIR 6 definition used above
    is taken from [R2]/[R3] and from insurer restatements [S1 §2.1.2][S7 defs].
16. **The CCSF's *Contrat Dépendance Solidaire* is a recommendation, not law** [R9]. It was adopted
    at the plenary of 16 January 2024 and published on 24 January 2024; nothing in these notes should
    be read as saying that a compulsory French LTC contract exists.
