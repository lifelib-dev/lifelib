# Product Specification

**Status:** Draft, 2026-08-29 (access date for every citation: 2026-08-29).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of a German **selbständige Berufsunfähigkeitsversicherung** (SBU) —
the standalone occupational-disability contract that pays a monthly *BU-Rente* for as long as the
insured is *berufsunfähig*, waives the premium for the same period (*Beitragsbefreiung*), and pays
nothing at all if the insured stays able to work. **It does not describe any single insurer's
product**, and it is not a quotation from one. Facts carrying a source tag — [S#] (primary product
documents: *Musterbedingungen*, *Allgemeine Versicherungsbedingungen*, *Tarifbestimmungen*,
*Produktinformationsblätter*, *Berufsgruppenverzeichnisse*) and [R#] (product-specific
regulatory and actuarial references), both numbered per
`_research/berufsunfaehigkeit.md` and resolved in `sources.md` (same directory; numbering frozen,
never renumbered), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) — name the
document the claim must be checked against. **[std]** marks a standardization introduced for the
reference implementation, each with a rationale and, where the research file recorded one, the
observed range; [unverified] marks a claim no retrieved document corroborates.

**Read this before any number below.** This specification was **drafted with nothing retrieved**.
Direct HTTP egress was refused by an organisation network policy for every relevant host —
`gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`, `deutsche-rentenversicherung.de`,
`bundesfinanzministerium.de` — and the session's `WebSearch` budget was exhausted before this
product was reached, so the first draft rested on the authoring model's own knowledge of German
insurance law and market practice, disciplined by **[std]** and [unverified] tags rather than by a
document. **That policy has since been lifted and the citations were re-verified against the primary
documents.** On 2026-08-30 the statutes and statutory instruments this product turns on were read as
the canonical XML gesetze-im-internet publishes for each law, each law's amendment status (*Stand*)
recorded on its entry; the GDV *Musterbedingungen* for the SBU, the BUZ and the BU-with-AU variant
and five carrier document sets were retrieved as PDFs and read. Of the **43** entries in
`sources.md`, **26 now answer `Retrieved: yes`** — twenty-five outright, and [S12] for three of the
documents it names out of eighteen carriers — and **17 still answer `no`**: 60 % of this product's
entries retrieved.
**The re-verification changed things**, and the corrections are marked where they fall: the six
months belongs to the *Sechs-Monats-Fiktion* and not to the *Prognosezeitraum*, which the GDV model
conditions leave blank [S1] [S12]; § 177 VVG extends the BU rules only to cover of a *dauerhafte*
impairment [R6]; § 161 VVG's three-year suicide window is a death-cover rule the market's AVB do not
apply to self-inflicted impairment at all [R11]; and the drafted claim that no German insurer
discloses its BU costs was wrong — VVG-InfoV § 2 requires the disclosure in euro [R12], and a
carrier's own AVB points the customer to it [S6]. **Read a claim as sound where its entry says
`Retrieved: yes` and as provisional where it does not**: there a delib citation is still a
**pointer, not a certificate**, naming the instrument a claim should be checked against without
asserting that anyone read it. What stayed out of reach is overwhelmingly **price and level** — no
rate card, no *Berufsgruppenverzeichnis*, no DAV table, no *Produktinformationsblatt* — so the
**mechanics** of the German BU contract are set out here from documents that were read, while the
**levels** are **[std]** with a stated construction or [unverified] with a warning, and there is not
one invented `[S#]` figure anywhere in this file.

**Scope boundaries.** The *Berufsunfähigkeits-Zusatzversicherung* (BUZ) — the same cover written as
a rider on a *Renten-*, *Kapitallebens-* or *Basisrentenversicherung* [S2] — carries an identical
liability and is described here as a wrapper variant, not modelled separately. The
*Erwerbsunfähigkeitsversicherung*, the *Grundfähigkeitsversicherung*, dread-disease cover,
*Krankentagegeld*, the *Pflegerentenversicherung* (delib product 10) and BU inside *betriebliche
Altersversorgung* or *Gruppenversicherung* are different products, outside this file.

---

## Product overview and market role

A German SBU is **life-assurance business**, written by a *Lebensversicherungsunternehmen* and
governed by §§ 172–177 VVG for its own mechanics and, through the cross-reference in § 176, by the
general life provisions §§ 150–170 VVG for everything else [R1] [R5] [REG-R29]. It is neither health
nor accident business, even though its trigger is a health event, and it carries no premium tax —
§ 4 Abs. 1 Nr. 5 Buchst. b VersStG exempts a premium for benefits payable "im Fall der Krankheit,
der Pflegebedürftigkeit, der Berufs- oder der Erwerbsunfähigkeit" where they serve the insured's or
her relatives' provision [R31]. Structurally it is a **pure risk contract with a levelling
reserve**: it returns nothing if the insured stays healthy, and the level *Bruttobeitrag* charged
against an *Invalidisierungswahrscheinlichkeit* that rises far more steeply with age than mortality
does builds a *Deckungsrückstellung* whose **purpose is to keep the gross premium level, not to
accumulate value** [R9]. A carrier's own AVB puts the size of it plainly: "Die Bildung eines
Kapitals ist kein Vertragszweck Ihrer Versicherung … Die für die Bildung des Deckungskapitals zur
Verfügung stehenden Beitragsteile sind gemessen an den gezahlten Beiträgen während der gesamten
Vertragslaufzeit sehr gering. Mit Ablauf der Versicherung ist das Deckungskapital deswegen stets
wieder völlig aufgebraucht" [S6]. **This corrects an earlier statement in this document that the
contract carries a "substantial" or "large" risk reserve.** The reserve is real, it is why the
contract has a *Rückkaufswert* and a *Beitragsfreistellung* right at all, and it is small.

**Why the product exists at all is a matter of statute.** The 2001 pension reform closed the
statutory *Berufsunfähigkeitsrente* to everyone born on or after 2 January 1961; § 240 Abs. 1
SGB VI preserves it only for insured persons "vor dem 2. Januar 1961 geboren" [R25]. What remains for the post-1960
population is the *Erwerbsminderungsrente* of § 43 SGB VI [R24], tested against the **general
labour market** in hours a day rather than against the insured's own occupation — *volle
Erwerbsminderung* below three hours a day, *teilweise* between three and six, both needing the
*allgemeine Wartezeit* plus three years of compulsory contributions in the five years before onset
(§ 43 Abs. 1 Nr. 2 and 3, Abs. 2 Nr. 2 and 3 SGB VI), and both assessed without regard to the state
of the labour market (Abs. 3). A surgeon who loses the use of a hand cannot operate but can answer a telephone for six
hours a day: fully *berufsunfähig*, not at all *erwerbsgemindert*. The private SBU is the
replacement for the cover the state withdrew, and it is **paid in addition to** the statutory
pension rather than offset against it — offsetting designs exist at the margin `[unverified]` and
are not modelled.

**Market size.** The GDV publishes the industry aggregates [R20]. An order of magnitude often
quoted is roughly **17 million** BU contracts in force, standalone and rider forms together, against
a working population of about 45 million `[unverified] on both figures and the year` — cover reaches
well under half the people who need it, which is the market's own framing of the product. The GDV
taxonomy does not help: rider BU falls under *Zusatzversicherungen* while the *selbständige* form is
not a separate line at all, so **the SBU/BUZ split of German new business is not established**
[REG-R53]. For scale, German life premium income (life insurers, *Pensionskassen* and
*Pensionsfonds*) was **€94.6 bn in 2024** on **80.3 million** contracts, down 1.4 % [REG-R53].

**What the market competes on.** The core definition is close to uniform, because it descends from
the GDV's *unverbindliche Musterbedingungen* — model conditions expressly **non-binding**, since
binding recommended conditions would be a cartel; the current pair is **MB BUV 22** and **MB BUZ 22**
of **15 November 2022**, succeeding a set dated 28 April 2021 [S1] [S2] [REG-R37]. Competition runs
through four other channels: the **occupational classification**, the dominant price driver and not
comparable between carriers; the ***AU-Klausel***; the breadth of the
***Nachversicherungsgarantie***; and the **stability of the *Zahlbeitrag*** relative to the
guaranteed *Bruttobeitrag*, the product's principal consumer risk [R21] [R22] [R23]. The hierarchy
the product sits in, broadest trigger first, is *Berufsunfähigkeit* (last occupation, 50 %) →
*Grundfähigkeitsversicherung* → *Erwerbsunfähigkeit* (any occupation) → statutory
*Erwerbsminderungsrente* [R24]: BU is the broadest and most expensive, and the one sold first.

---

## Representative specification

The composite is built from the market position each mechanic occupies, not from one carrier's
paper. Five carrier wordings were read for the provenance pass of 2026-08-30 — Alte Leipziger,
NÜRNBERGER, VOLKSWOHL BUND, Debeka and CosmosDirekt [S4] [S6] [S9] [S12] — and where a clause or a
cap is now attributed to one of them the tag says which. **No price was obtained from any of them**,
so no *level* in the composite comes from a carrier. Eighteen named German life insurers write this
product [S3]–[S12]; the file names them and attributes no premium, factor or rate to any of them. The anchor model
cell is defined in the last row of the first table and argued in footnote (6).

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Individual, **single-life**, standalone *selbständige Berufsunfähigkeitsversicherung*; life-assurance business under §§ 172–177 VVG; participating through *Beitragsverrechnung* only; no unit account. The *versicherte Person* and the *Versicherungsnehmer* are usually but not necessarily the same | [R1] [R5] [REG-R29] |
| Legal wrapper | Standalone contract. The rider form (BUZ) on a *Renten-*, *Kapitallebens-* or *Basisrentenversicherung* is the equally common alternative and carries the identical liability | [S1]; [S2]; choice **[std]** (1) |
| Premium form (model-point parameter) | (i) `level` — one *Bruttobeitrag* guaranteed for the whole term; (ii) `dynamik` — *Beitragsdynamik*, premium and insured *BU-Rente* escalating annually without renewed *Gesundheitsprüfung* | (i) [S1] [S3]–[S12]; (ii) [S1] [S4] [S5]; escalation levels **[std]** (2) |
| Entry ages | 15 (pupils) to 50; 25–35 is the mass market | [S1] [S4]–[S12] `[unverified]`; envelope **[std]** (3) |
| *Versicherungsdauer* ends | At the agreed *Endalter*: 67 representative, 65 the common alternative, 60/62/63 sold as budget options | [S1] [S3]–[S12] `[unverified]`; choice **[std]** (4) |
| *Leistungsdauer* ends | At the *Leistungsendalter*, equal to the *Endalter* in the market standard; a shorter *Leistungsdauer* is a cheaper minority design | [S1] `[unverified]`; both carried as separate columns **[std]** (4) |
| Age basis | *Eintrittsalter* on an age-last-birthday basis, advancing at the policy anniversary | **[std]** (5) |
| *BU-Rente* | 1 500 € per month; 1 000 – 2 000 € the retail band, higher for high earners. The *Angemessenheitsgrenze* caps the insurable *BU-Rente* at 60–70 % of gross income, or about 80 % of net | [R22] [S15] [S16] `[unverified]`; level **[std]** (6) |
| Residence, scope, currency | German residence at application; cover worldwide, with notification duties for long stays abroad; EUR | [S1] `[unverified]` |
| **Anchor model cell** | Entry age **30**, occupational class **BG1 (Bürotätigkeit)**, *BU-Rente* **1 500 €/month**, *Endalter* and *Leistungsendalter* **67**, *Karenzzeit* **0**, *Leistungsdynamik* **2 % p.a.**, no *Beitragsdynamik*, **monthly** payment, *Zahlbeitrag* = 0,70 × *Bruttobeitrag*, *Wiedereingliederungshilfe* 6 monthly *Renten* | **[std]** (6) |

Footnotes to **[std]** rows:

1. **Wrapper is a tax and packaging variable, not a liability one.** The BU risk, the definition,
   the *Leistungsprüfung*, the *Nachprüfung* and the *Beitragsbefreiung* are identical in the two
   forms [S1] [S2]. Two things differ: in a BUZ the *Beitragsbefreiung* waives the **whole**
   premium of the host contract, which is the rider form's main attraction [S2]; and inside a
   *Basisrente* the whole premium becomes deductible while the *BU-Rente* becomes fully taxable
   [R27] [R28]. The composite takes the standalone form because it isolates the BU liability from a
   savings chassis delib already models four times over, and because the standalone form's cash
   flows are the rider's cash flows plus nothing.
2. **Both premium forms are real German designs.** The base sale is a level *Bruttobeitrag*
   guaranteed for the term. The *Beitragsdynamik* option escalates premium and insured *BU-Rente*
   together each year, commonly at **3 % or 5 %**, menus recalled from 1 % to 10 %, lapsing
   permanently if two or three consecutive increases are declined `[unverified]` on every figure.
   The composite ships the level form as the base and carries `dynamik` at **3 % [std]**, the lower
   of the two commonly quoted rates.
3. Entry-age envelopes could not be compared carrier by carrier. The established shape is that
   pupils and students are insurable, classified by the occupation trained for — the market's
   principal argument for buying young — and that entry closes around 50 `[unverified]`.
4. **The two ages are separate columns because they are separate contractual terms.** The
   *Versicherungsdauer* is the period in which a BU may incept and be covered; the *Leistungsdauer*
   the period over which benefit is paid. In the market standard both end at the same *Endalter*
   [S1]; where they differ the *Leistungsdauer* is the shorter `[unverified]`. A model carrying one
   age cannot express that design at all, so the composite carries both and sets them equal in
   eleven of its thirteen model points. **67 rather than 65** because 67 is the statutory retirement
   age for cohorts born from 1964 `[unverified]` and anything earlier leaves a gap between the end
   of the *BU-Rente* and the start of the old-age pension [S16].
5. German practice uses an *Eintrittsalter* convention rather than an age-nearest one; the rounding
   rule varies by carrier and none of the retrieved wordings states one, so the composite uses age last birthday advancing
   at the policy anniversary **[std]** — worth at most one year of the inception curve.
6. **The anchor is the German market's central sale.** Entry age 30 is inside the 25–35 mass
   market; a 37-year term to 67 exercises the entire inception curve including the expensive last
   decade that dominates the liability; an office class keeps the premium where a reader can
   sanity-check it against published price points; and 1 500 € a month is the level the consumer
   press illustrates with, above the recalled 1 000–1 200 € average new-business *BU-Rente* because
   that average is itself evidence of underinsurance against the market's own 70–80 %-of-net advice
   [R22] [S15] [S16] `[unverified]`. The *Leistungsdynamik* of 2 % is the midpoint of the recalled
   1–3 % menu **[std]**, carried in the base run because a BU model without in-claim escalation
   misses the product's dominant long-duration sensitivity.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Quotation | **Two numbers, always**: the *Bruttobeitrag* (*Tarifbeitrag*), computed on first-order bases and the contractually guaranteed maximum the insurer may ever charge; and the *Zahlbeitrag* (*Nettobeitrag*), what is actually collected after the anticipated *Überschussbeteiligung* has been applied in advance | [R10] [S13] [S16] |
| Mechanism of the gap | ***Beitragsverrechnung***: the surplus the contract is expected to generate — overwhelmingly **risk surplus**, because the first-order *Invalidisierungswahrscheinlichkeiten* carry a deliberate safety margin, plus expense surplus — is credited immediately against the premium rather than accumulated | [R10] [R14] [REG-R24] [REG-R18] |
| *Zahlbeitrag* / *Bruttobeitrag* | **0,70** | recalled range 0,50 – 0,80, most commonly 0,60 – 0,75 `[unverified]`; level **[std]** (7) |
| Premium level | **Not sourced from any rate card.** The reference implementation *derives* the level annual *Bruttobeitrag* by actuarial equivalence on its own first-order basis; the model point may override it | **[std]** (8) |
| Recalled market price points | Entry age 30, *BU-Rente* 1 500 €/month to 67: *Zahlbeitrag* of the order of **55 – 90 €/month** for a pure office occupation and **160 – 300 €/month** for a mainstream skilled manual trade; the corresponding *Bruttobeiträge* are those divided by the *Beitragsverrechnung* ratio | [S15] `[unverified]` — recollections of consumer-press figures with no year attached; see (8) |
| Premium-paying term | The whole *Versicherungsdauer*. There is no shorter premium-paying option in the standard product | [S1] `[unverified]` |
| Payment frequency | Monthly by SEPA direct debit is the retail norm; quarterly, half-yearly and annual are offered | [S1] [S9] `[unverified]` |
| *Ratenzahlungszuschlag* | Annual 1,000; half-yearly **1,02**; quarterly **1,03**; monthly **1,05** | German market convention `[unverified]`; carried as **[std]** (9) |
| Premium cessation | On death, on lapse, at the end of the *Versicherungsdauer*, and — for as long as the *BU-Rente* is in payment — under the *Beitragsbefreiung* | [S1] |
| *Risikozuschlag* (model-point parameter) | `risk_factor`, a multiplier on the *Bruttobeitrag*; 1,00 at *Normaltarif*. Observed loadings commonly **25 % to 100 %**, occasionally more | [S1] [S3]–[S12] `[unverified]`; base value **[std]** |
| *Stundung*, *Anwartschaft*, premium tax | Deferral or a dormant *Anwartschaft* for parental leave, unemployment or study preserves insurability without full cover; not modelled. **No premium tax** | [S1] [R31] `[unverified]` |

7. **This is the most consequential single gap in the whole corpus.** The
   *Produktinformationsblatt* [S13] is the one public German document that routinely prints both
   figures on the same page for a named age, occupation and *BU-Rente*, and none was retrieved — a
   PIB is generated per quotation and no carrier publishes a specimen with figures. **The mechanism
   is no longer a recollection**: two carrier AVB state it, one in the exact terms *Tarifbeitrag
   (Bruttobeitrag)* against *ermäßigter Nettobeitrag* [S6] [S12]. What is missing is the ratio.
   0,70 is the midpoint of the recalled 0,60–0,75 common band: a construction, not a measurement.
   Its consequence is direct and large — **a model projecting only the *Bruttobeitrag* overstates
   collected premium by 1/0,70 − 1 = 42,9 %**, and one projecting only the *Zahlbeitrag* silently
   assumes the *Beitragsverrechnung* is permanent when the whole point of the pair is that it is not.
8. **No German BU rate card of any kind was obtained** — no tariff table, no occupational factor
   set, no age curve. Unlike frlib's `temporaire_deces`, where one carrier published a complete
   attained-age grid the model reproduces exactly, **this model can reproduce nothing external**.
   The honest response is to make the premium an *output* of a stated first-order basis rather than
   an unsourced input; the recalled price points above are then a **plausibility check on the
   construction, not its source**.
9. The 5 % / 3 % / 2 % ladder is the convention the German market is generally understood to use;
   no retrieved document states it. It loads the tariff premium, so it scales both halves of the pair.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Principal benefit | The agreed monthly *BU-Rente*, paid **monthly in advance** for as long as the insured is *berufsunfähig*, to the *Leistungsendalter* | [S1] [R1] |
| Benefit trigger | Inability, as a consequence of *Krankheit*, *Körperverletzung* or more than age-appropriate *Kräfteverfall*, to exercise the **last occupation actually exercised, as it was arranged before the impairment**, **to at least 50 %**, **prospectively on a lasting basis** | [R1] for the statutory limbs, which say only "ganz oder teilweise voraussichtlich auf Dauer"; **the 50 % and the prognosis period are AVB conventions, left blank in the GDV model conditions** [S1] and filled by each carrier [S12] |
| *Prognosezeitraum* | The period over which the inability must be expected to last. **It is not six months as a matter of course**: the model conditions leave it blank subject only to the statutory *Dauerhaftigkeit*, one large carrier requires "voraussichtlich auf Dauer (mindestens 3 Jahre)", and a shortened *Prognosezeitraum* is sold as a tier upgrade rather than being standard | [S1] [S12] |
| Degree of benefit | **All-or-nothing at 50 %.** At 50 % or more the full *BU-Rente* is payable; at 49 %, nothing — "Bei einem geringeren Grad der Berufsunfähigkeit besteht kein Anspruch auf eine Leistung" [S12]. A second and distinct route is the ***Sechs-Monats-Fiktion***: six months of actual continuous inability to that degree, after which "gilt die Fortdauer dieses Zustandes als Berufsunfähigkeit" with no prognosis at all | [S1] [S12] [REG-R37]; *Staffelregelung* and "Teil-BU" variants `[unverified]`, not modelled |
| Retroactivity | The claim arises "mit Ablauf des Monats, in dem die Berufsunfähigkeit eingetreten ist" [S1], so benefit runs from **onset** (after any *Karenzzeit*), not from the decision date; premiums are paid in full until the decision and refunded on acknowledgement. Under the *Fiktion* limb the model conditions treat only the **continuation** of the state as BU, and record that paying retroactively from an earlier date requires the conditions to be varied — full retroactivity is a carrier choice, not the model default | [S1] |
| ***Beitragsbefreiung*** | Full waiver of the premium while the *BU-Rente* is in payment. Not an option — part of the core cover in every German BU contract | [S1] [S2] |
| ***Karenzzeit*** | **0 months** representative. A *Karenzzeit* lowers the premium and defers **the pension only** — "Die Karenzzeit gilt nur für die Rente"; the *Beitragsbefreiung* starts from the month after BU begins regardless, the insured must be BU throughout it and still at its end, and a served *Karenzzeit* is credited on a recurrence from the same cause within 24 months [S4] [S9]. The **menu** of durations lives in the *Tarifbestimmungen*, which were not retrieved; 0 / 3 / 6 / 12 / 18 / 24 is recalled `[unverified]` | [S1] [S4] [S9]; choice **[std]** (10) |
| ***Leistungsdynamik*** | **2 % a year**, applied on each anniversary of the start of benefit, to the *BU-Rente* in payment | recalled menu 1 % / 2 % / 3 %, some index-linked `[unverified]`; level **[std]** (10) |
| ***Wiedereingliederungshilfe*** | A one-off lump of **6 monthly *BU-Renten*** on a return to work | recalled range 3 – 12 monthly *Renten* `[unverified]`; level **[std]** (11) |
| End of benefit | At the *Leistungsendalter*; on death; or on a *Nachprüfung* termination, followed by the statutory **three-month run-off** | [S1] [R3] [REG-R29] |
| Death, maturity and expiry benefits | **None in the modelled product, and none in the GDV model conditions**: an SBU pays nothing on death, before or during a claim; survival to the *Endalter* returns nothing; and a claim in payment at the *Leistungsendalter* stops with no commutation, no residual value and no conversion [S1]. **This is not universal.** One retrieved carrier's AVB grants a *Schlusszahlung* at expiry of the *Versicherungsdauer*, set "in Prozent der bis dahin tatsächlich gezahlten Tarifbeiträge", where no BU arose, and *Zinsüberschussanteile* during a claim converted into a *Bonusrente* [S12]; another offers a *Bonusrente* as the alternative to the *Beitragsverrechnung* [S6]. Both are surplus applications, not guarantees, and neither is modelled | [S1]; carrier variants [S6] [S12] |
| Other assistance benefits | *Umorganisationshilfe*, *Reha-Hilfe*, *Soforthilfe* set off against the eventual benefit, *Pflege* add-ons | [S1] [S5] [S8] `[unverified]`; not modelled (11) |

10. **The *Karenzzeit* is an option, not a feature, and the standard sale does not carry one.**
    It is taken to cut the premium, typically by a buyer with employer sick pay or a professional
    scheme covering the first period [S16]. The composite therefore runs at 0 and carries
    `karenz_months` as a model-point column, with two model points exercising 3, 6 and 12.
    **The *Karenzzeit* is not the six-month prognosis period**, and the two are constantly
    confused: the prognosis is part of the *definition* of BU, the *Karenzzeit* a deferment of
    *payment* on a BU that is already established.
11. Only the *Wiedereingliederungshilfe* is both common enough to be representative and simple
    enough to attach to a transition the model already carries; the rest are discretionary, small,
    or duplicate a benefit already modelled.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Dominant rating factor | **Occupation**, ahead of age and far ahead of anything else — a direct consequence of the definition, since the insured event is inability to do *this* job | [S6] [R1] |
| *Berufsgruppen* per carrier | **4 to 6** typical; 3 at some direct writers, 10 or more at specialists. **Nothing retrieved supports this.** The NÜRNBERGER AVB was read in full for the 2026-08-30 pass and never uses the word *Berufsgruppe*; the classification lives in a *Berufsgruppenverzeichnis* that is not published at a public address, and none of the five carrier wordings read states a class count | [S6] [S12] `[unverified]` — recalled, and the document that would settle it was sought and not found |
| Classification list | Each insurer maintains its own *Berufsgruppenverzeichnis* mapping named occupations to classes. **The classes are not comparable between carriers** — an occupation in class 2 at one insurer may be class 3 at another, which is precisely why the comparison portals exist | [S6] [S15] |
| Composite classification | Five classes: **BG1** academic and pure office; **BG2** qualified commercial and technical; **BG3** skilled trades with light physical content; **BG4** skilled manual trades; **BG5** heavy manual, hazardous and outdoor | shape `[unverified]` and **not** attributable to a retrieved document; five-class cut **[std]** (12) |
| Occupational factors | BG1 **1,00**; BG2 **1,40**; BG3 **2,10**; BG4 **3,00**; BG5 **4,50**, applied multiplicatively to the *Invalidisierungswahrscheinlichkeit* | recalled manual/office premium ratio 2× – 4×, centred near 3×, and 4× – 6× for the heaviest insurable trades `[unverified]`; **[std]** (12) |
| Declined occupations, academic status | Roofers, scaffolders, some care roles, professional drivers and some artistic professions are declined outright by many carriers, or offered only with a *Karenzzeit*, a reduced *Endalter* or a limited *Leistungsdauer*. Academic status moves the classification independently of the job title | [S6] [S12] `[unverified]`; absorbed into the class |
| Sex | **May not be a rating factor.** Unisex pricing has been compulsory for new contracts since **21 December 2012**, following *Test-Achats* (C-236/09, 1 March 2011) and the repeal of § 20 Abs. 2 Satz 1 AGG | [R15] [REG-R34] |
| Smoker status | **Not systematically a rating factor in BU**, unlike *Risikolebensversicherung*; where it appears its effect is far smaller than the occupational factor | `[unverified]`; the GDV model conditions and the four carrier AVB read on 2026-08-30 are silent on smoking, which is consistent with the claim but does not establish it; not modelled |
| *Gesundheitsprüfung* | Health questions over defined look-back windows — recalled as five years outpatient, ten inpatient and for psychotherapy — plus height and weight, current complaints, planned treatments, tobacco use and existing or refused disability cover; a medical report above an insured *BU-Rente* of the order of 18 000 – 30 000 € a year. **Psychiatric and musculoskeletal history are the two decisive ones**, which is exactly where the claims come from | [S1] [S16] [R22] `[unverified]` |
| Underwriting outcomes | Acceptance at *Normaltarif*; acceptance with a ***Risikozuschlag***, commonly 25 % – 100 %; acceptance with an ***Ausschlussklausel*** excluding a named condition or body region (spine, knee, psyche are the classic three); *Zurückstellung*; *Ablehnung* | [S1] `[unverified]` |
| Proportion not accepted on standard terms | A quarter to a third — which is why the ***Risikovoranfrage*** exists: an anonymised pre-enquiry through a broker, so a decline is never recorded against the applicant in the industry's *Hinweis- und Informationssystem* (HIS) | [S15] [S16] [R7] `[unverified]` |
| ***Vorvertragliche Anzeigepflicht*** | § 19 VVG: disclosure of risk circumstances the insurer asked about in *Textform*; on breach, *Rücktritt*, contract amendment, *Kündigung* or *Anfechtung* graded by fault. The remedies are extinguished by **§ 21 Abs. 3 VVG** — not by § 19 — after **five years**, "zehn Jahre" where the duty was breached intentionally or fraudulently, and **not** for claims that arose inside the period. § 21 Abs. 1 also gives the insurer one month from learning of the breach to act | [R7] [REG-R30] |
| ***Anerkennungsquote*** | About **75 % – 80 %** of decided claims accepted, roughly half of the declines because the 50 % degree is not reached | [R21] [R20] `[unverified]`; enters the model as **[std]** (13) |

12. **A five-class cut with a 1,00 / 3,00 anchor.** The corpus supports the *shape* of a German
    *Berufsgruppenverzeichnis* — academic and office at the top, heavy manual at the bottom — and a
    manual-to-office premium ratio recalled at 2× to 4×, centred near 3×. It supports no carrier's
    class count and no factor. Five classes sits inside the recalled 4–6 band while leaving room
    for the heaviest insurable trades; BG1 at 1,00 and BG4 at 3,00 are the research file's own
    representative anchors, and BG2, BG3 and BG5 are interpolated on a roughly geometric
    progression. **These are constructions inside an argued range, not sourced figures.** The
    mechanic they implement — one base inception table with multiplicative occupational loadings —
    **is** how German BU pricing works [S6], and that much is not a construction.
13. The *Anerkennungsquote* enters as an **acceptance factor of 0,80 [std] on the inception rate**,
    applied to the transition rather than to the benefit, because a declined claim generates no
    annuity at all rather than a smaller one. **The interaction with the decrement table is a
    trap**: the shipped inception proxy is **gross of declinature** by construction, so the factor
    belongs on top of it, and a user substituting a table already net of declinature must set it to
    1,00 or the effect is counted twice [REG-R53].

### Charges

**No German insurer publishes the charge structure of a BU tariff, and there is no *Effektivkosten*
disclosure for a pure risk product** — the reduction-in-yield figure that makes delib's savings
products transparent has no meaning where there is no yield [R12] [S14] [REG-R31]. Everything below
is therefore **[std]** or a statutory ceiling.

| Parameter | Representative value | Basis |
|---|---|---|
| ***Abschluss- und Vertriebskosten*** | **2,5 % of the *Beitragssumme***, charged at inception. § 4 DeckRV caps the *Zillmersatz* at **25 ‰ (2,5 %) of the *Beitragssumme***, cut from 40 ‰ with effect from 1 January 2015 by the LVRG; the rate in use at conclusion applies for the whole term | ceiling [R13] [REG-R16] [REG-R20]; level at the cap **[std]** (14) |
| ***Verwaltungskosten***, proportional | **9 % of the *Bruttobeitrag***, for the whole term | **[std]** (15) |
| ***Verwaltungskosten***, flat | **18 € per policy per year**, level in euro, not inflated | **[std]** (15) |
| ***Leistungsbearbeitungskosten***, assessment | **800 € per claim inception** | **[std]** (16) |
| ***Leistungsbearbeitungskosten***, maintenance | **12 € per month a claim is in payment** | **[std]** (16) |
| Expense inflation, commission | **No inflation** — German loadings are fixed at inception for the term. Commission is not separately modelled; it sits inside the *Abschluss- und Vertriebskosten* line, which is the German charge taxonomy | **[std]** (14) (15) |

14. **The only sourced ceiling in the entire charge structure** is the *Höchstzillmersatz*, and it
    is now sourced three times over: DeckRV § 4 Abs. 1 — "Der Zillmersatz darf 25 Promille der Summe
    aller Prämien nicht überschreiten" [R13] — and two carrier AVB that state it customer-facing as
    2,5 % of the premiums payable over the term [S1] [S6]. The base is **the sum of all premiums**,
    which settles the three renderings the reference library records [REG-R16], and § 4 Abs. 4 fixes
    the rate used at conclusion for the whole term. The composite sits **at** the cap: German level-premium risk business
    generally does, and a cap is at least a sourced ceiling. The *Beitragssumme* over 37 years is
    large even though the annual premium is modest, so this is the contract's biggest expense item.
15. Levels are round-number constructions sized so first-year outgo is of the same order as
    first-year premium income, which is the shape a level-premium risk product has. Holding the
    flat component level in euro rather than inflating it is the German practice: a
    *Verwaltungskostenzuschlag* is fixed in the tariff at conclusion, not indexed.
16. ***Leistungsbearbeitungskosten* are the charge a modeller from a term-life background will
    forget, and here they are material.** A BU claim is expensive to assess — medical reports, an
    analysis of the occupation as actually exercised, for the self-employed an analysis of the
    business, sometimes litigation — and expensive to maintain, because the *Nachprüfung* recurs
    annually or biennially [R21]. A one-off assessment cost plus a recurring per-month-in-payment
    cost is the minimum structure reflecting that; both levels are constructions.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| ***Rückkaufswert*** | **Exists, and is small.** § 169 VVG applies through § 176 and only *entsprechend*: § 169 Abs. 1 confers the right where "der Eintritt der Verpflichtung des Versicherers gewiss ist", which a pure SBU is not, so it arrives through the cross-reference and its reservation [R5] [R9]. The AVB pay it expressly — "den Rückkaufswert entsprechend § 169 des Versicherungsvertragsgesetzes (VVG)" [S1] — and VVG-InfoV § 2 requires the *Rückkaufswerte* to be disclosed for a BU contract [R12]. The mechanics are confirmed: *Deckungsrückstellung* on recognised actuarial principles, acquisition and distribution costs spread over at least five years for the *Mindestrückkaufswert*, and an *Abzug* only "wenn er vereinbart, beziffert und angemessen ist", never for unamortised acquisition costs. One retrieved carrier takes no deduction at all. **The magnitude is the point**: the parts of the premium available to build the capital are, in a carrier's own words, "sehr gering" against premiums paid, and the capital is exhausted by expiry [S6] | [R9] [R5] [R12] [R13] [S1] [S6] [REG-R28] |
| ***Beitragsfreistellung*** | A right "jederzeit für den Schluss der laufenden Versicherungsperiode" under § 165 Abs. 1 VVG through § 176, producing a **beitragsfreie *BU-Rente*** computed on the premium basis and stated in the contract for each policy year; below the agreed *Mindestversicherungsleistung* the contract is instead terminated against the *Rückkaufswert*. One retrieved carrier sets that minimum at 100,00 EUR of monthly pension [S6]. It is **small**, and the conditions say why: "wegen der benötigten Risikobeiträge gemessen an den gezahlten Beiträgen keine oder nur geringe Mittel" are available even in later years [S1]. It is nonetheless the option consumer advice recommends over lapse | [R8] [R5] [S1] [S6] [S16] [REG-R28] |
| **What the model does with both** | **Neither is modelled as a cash flow.** A lapse removes the policy from the in-force count and pays nothing | scope **[std]** (17) |
| Effect of a lapse | Cover ends. Once health has changed the cover cannot be replaced, which makes BU lapse both low and **strongly selective** | [S16]; selection not modelled — see the technical notes' model risks |
| Non-payment path | German lapse is not instantaneous: due date → *qualifizierte Mahnung* in *Textform* with an itemised statement and a **two-week** minimum period → expiry; and § 166 VVG overrides the general § 38 consequence for life business, so cover converts to *prämienfrei* rather than simply ceasing | [REG-R30] [REG-R28]; timing simplification **[std]** (17) |
| *Widerruf*, termination of right | 30-day *Widerruf* for a life-assurance contract, absorbed into the first-year lapse rate **[std]**. Rights terminate at the *Endalter*, on death and on lapse | [REG-R23] [S1] `[unverified]` |
| *Verlängerungsoption* | The right to extend the *Versicherungs-* and *Leistungsdauer* — 63 → 65, 65 → 67 — without renewed underwriting, exercisable in a window before the original *Endalter*. The option exists at carrier level (a *Verlängerungsgarantie* has its own section in one retrieved AVB [S9]); **the ages and the window are in the *Tarifbestimmungen*, which were not retrieved**, so they stay `[unverified]` | [S1] [S4] [S9]; modelled as a model-point *Endalter*, not as a dynamic option |

17. **A gross benefit-and-premium projection has no place to put a surrender value**, and inventing
    one would be worse than omitting it: the *Rückkaufswert* is the release of a reserve this model
    deliberately does not compute. The omission is a **scope limitation stated here rather than left
    to be discovered**, and its direction is known — a model paying nothing on lapse overstates net
    cash flow by the values it never pays and understates it by the reserve it never releases. The
    two-week *Mahnung* period likewise means a monthly model applying lapse in the month of the
    missed premium is early by at least a month [REG-R30]; the composite applies lapse at end of
    month and accepts the offset.

---

## Contractual mechanics

One subsection per operative rule: what the rule says, and what it does to the contract.

### The definition of Berufsunfähigkeit — § 172 VVG

**The rule.** A person is *berufsunfähig* who, as a consequence of *Krankheit*, *Körperverletzung*
or more than age-appropriate *Kräfteverfall*, is **prospectively permanently** (*voraussichtlich
auf Dauer*) unable, wholly or in part, to exercise **the occupation last actually exercised, as it
was arranged before the impairment** [R1] [REG-R29].

**What it does.** Four things, all model-relevant. **(1) The reference occupation is the last one
actually exercised** — not the trained occupation, not an average one, and emphatically not "any
occupation": a trained lawyer working as a warehouse supervisor is tested against warehouse
supervision. That is why the German trigger is so much broader than an any-occupation definition,
and why the price is so much more sensitive to the insured's actual job than to anything else about
them. **(2) It is taken as actually arranged**, so the concrete duties, hours and physical demands
of this insured's own post are the yardstick and two people with the same job title can face
different tests. **(3) The cause must be medical**: loss of the job, loss of a licence for
non-medical reasons and economic inability to find work are not BU, with the single contractual
exception of the *Infektionsklausel*. **(4) Prospectively permanent** — the statute puts no number
on it, and the market does.

**§ 172 Abs. 3 permits, but does not imply, the *abstrakte Verweisung*** [R1]. Absent an express
agreement the insurer may not refer the insured to an occupation she does not actually exercise.

### The six-month prognosis and the 50 % threshold

**The rule.** The insured is *berufsunfähig* if, as a consequence of one of the § 172 causes, each
to be demonstrated medically, she is **prospectively for at least six months continuously** unable
to exercise her last occupation as it was arranged, **to at least 50 %** [S1].

**What it does — and a correction that matters.** Neither the six-month period nor the 50 %
threshold is in § 172 VVG. **Both are contractual standards** carried in the AVB and near-uniform
because they descend from the GDV model text; they concretise the statutory words *voraussichtlich
auf Dauer* and *ganz oder teilweise* [S1] [REG-R37]. A document attributing them to the statute is
wrong. The 50 % is **all-or-nothing** — at 50 % the full *BU-Rente*, at 49 % nothing — so the
modelled object is the **incidence of a ≥ 50 % incapacity**, not a severity distribution.
Measurement is on working time, on the share of the occupation's essential tasks still performable,
or on both, and **the burden of proof on the initial claim is on the insured** [R21].

There are **two routes to a claim**, and they are two separate clauses of the AVB with two
different periods. The *prognosis route* (§ 2 Abs. 1): a doctor certifies that the 50 % inability is
expected to last for the contractual *Prognosezeitraum*, and benefit is due from onset without
waiting for it to elapse. **The GDV model conditions leave that period blank**, footnoting only that
its measure must respect "dem gesetzlichen Tatbestandsmerkmal der Dauerhaftigkeit (§ 172 Abs. 2
VVG)", and one large carrier's AVB sets it at "voraussichtlich auf Dauer (mindestens 3 Jahre)"
[S1] [S12]. The *Sechs-Monats-Fiktion* (§ 2 Abs. 2): where the insured has actually been unable,
continuously, for six months, "gilt die Fortdauer dieses Zustandes als Berufsunfähigkeit" with no
further prognosis — the fiction exists because a forward-looking prognosis is hard to obtain and
easy to contest. **Six months is the *Fiktion*'s period, not the *Prognosezeitraum*'s**; an earlier
version of this document ran the two together. A shortened *Prognosezeitraum* is sold as a tier
upgrade [S12], which raises the effective inception rate without changing the definition.

### Abstrakte and konkrete Verweisung

**The rules.** *Abstrakte Verweisung*: the insurer refers the insured to an occupation she **could**
take up given her training and abilities and corresponding to her previous *Lebensstellung*, whether
or not she does — permitted by § 172 Abs. 3 only if agreed [R1]. *Konkrete Verweisung*: it refers
her to another occupation she **actually exercises** [REG-R37].

**What they do.** The *abstrakte Verweisung*, where it applies, defeats the claim entirely however
unable the insured is to do her own job, because almost anyone can be pointed at *some*
theoretically available occupation. **The market standard is now to waive it**: essentially every
quality tariff sold today contains a *Verzicht auf die abstrakte Verweisung*, and a tariff retaining
it is not sold in the broker channel [S1] [S3]–[S12] [REG-R37]. The waiver is a competitive
standard, not a legal requirement, and legacy books still carry the clause. The *konkrete
Verweisung* is **retained**, on both sides of the claim: at the initial claim, if the insured has
already taken up such an occupation she is not *berufsunfähig*; and in the *Nachprüfung*, if she
takes one up later, the insurer may end the benefit — subject to the three-month run-off [R3]. The
limit is *Lebensstellung*: the new occupation must correspond in **income and social standing** —
"nur eine Tätigkeit, die in ihrer Vergütung und sozialen Wertschätzung nicht spürbar unter das
Niveau der bislang ausgeübten Tätigkeit absinkt" [S1] — with a working threshold of a **20 %** income
drop. That figure is now sourced from the conditions rather than recalled: the GDV model conditions
offer the sentence "Die höchstrichterliche Rechtsprechung geht zur Zeit davon aus, dass im Regelfall
eine Minderung der Vergütung in Höhe von bis zu 20 % noch zumutbar ist", and one carrier's AVB fixes
the reasonable reduction by reference to the case law "jedoch maximal 20 %" [S1] [S12] [R29].

**Model consequence, a design decision rather than a simplification.** *Konkrete Verweisung* is
**not a separate decrement**: in a cash-flow model it is indistinguishable from recovery — both end
the benefit, both operate through the *Nachprüfung*, both carry the same three-month run-off. The
composite folds the two into a single duration-dependent claim-termination-other-than-death rate
rather than pretending to separate two things no public data separates.

### Anerkenntnis — § 173 VVG

**The rule.** On a *Leistungsantrag* the insurer must declare **in *Textform***, when the claim
falls due, whether it acknowledges liability; a time-limited acknowledgement — a *befristetes
Anerkenntnis* — may be given **only once** [R2] [REG-R29].

**What it does.** The *Anerkenntnis* **binds**. Once given, the insurer cannot revisit the same
facts; it can only stop paying prospectively, through a *Nachprüfung* in which **the burden of proof
is on the insurer** [R3] [R29]. That reversal is the most valuable thing an insured obtains from a
BU claim, and § 173's restriction exists precisely because insurers previously used repeated
time-limited acknowledgements to keep the burden on the insured indefinitely. Market practice limits
the time-limited form to 6 or 12 months, and a few tariffs waive it entirely `[unverified]` — no
retrieved wording states a maximum length. What the retrieved conditions do add is a further
restriction beyond the statute: the time-limited acknowledgement is available only "wenn hierfür ein
sachlicher Grund besteht, den wir Ihnen mitteilen werden" [S1].

**Timing.** German claims studies report an average decision time measured in months — five to six
is recalled — with a long tail `[unverified]` [R21]. Because benefit is retroactive to onset, a
delay produces a **lump catch-up payment, not a lost payment**; the reference implementation pays
from onset and does **not** model the delay, understating the *timing* of the early cash flows and
not their amount, which is a numbered pitfall in the technical notes.

### Nachprüfung, the three-month run-off and Reaktivierung — § 174 VVG

**The rule.** Where the insurer establishes that the conditions of its liability have ceased, it
remains obliged to pay **only to the end of the third month following receipt by the policyholder
of a notice in *Textform*** to that effect [R3] [REG-R29]. §§ 173 and 174 are *halbzwingend* under
§ 175 — no departure to the policyholder's disadvantage is effective — which is why these mechanics
are uniform across the market and not a competitive variable; insurers may only improve on them,
and some do, by contracting for a longer run-off or by waiving the *Nachprüfung* after a stated
benefit duration [R4] `[unverified]` — none of the four wordings retrieved for this pass improves on
the statutory floor, all four reproducing the three-month period as it stands. Note also the reach
of § 175: it protects §§ 173 and 174 only, and says nothing about the definition in § 172, which is
exactly why the definition *is* a competitive variable and the run-off is not. The conditions add a
consequence the statute does not state: at the same date the run-off ends, "müssen Sie auch die
Beiträge wieder zahlen" [S1].

**What the insurer must show** is a *change* relative to the state on which the *Anerkenntnis*
rested: a medical improvement lifting the insured above the 50 % threshold in her old occupation,
or a new occupation actually taken up satisfying *konkrete Verweisung*. A re-assessment of the same
facts, or correction of the insurer's own earlier error, does not suffice, and an
*Einstellungsmitteilung* that does not set the comparison out intelligibly is ineffective — so the
three-month period never starts to run [R29].

**What it does to the cash flows, and this is the most model-relevant number in the statutory
frame.** A recovery does **not** stop the annuity on the day it happens; it stops it three months
later, measured from a notice. Every claim termination other than death is therefore followed by
**three further monthly payments**, and because reactivation is concentrated in the first one to
two years of a claim that tail is a real cash-flow effect rather than a rounding detail.

***Reaktivierung*** is the other half. The insured recovers and **the cover revives**: the contract
does not end, the *Beitragsbefreiung* stops, the premium resumes **at the same *Zahlbeitrag*** — she
has not aged into a higher tariff, because the tariff is level — and a fresh BU may be claimed
later. This bidirectional structure is what makes BU a genuine multi-state model rather than a
decrement model, and is the most important structural difference from delib's
`risikolebensversicherung`.

### Beitragsbefreiung

**The rule.** While the *BU-Rente* is in payment the premium is waived. In an SBU the waiver covers
the SBU's own premium; in a BUZ it covers the entire premium of the host contract [S1] [S2].

**What it does.** The *Beitragsbefreiung* is **not a benefit cash flow. It is the absence of a
premium cash flow in the disabled state.** In a multi-state monthly model it falls out automatically
once premiums are weighted by the premium-paying count rather than by total policies in force — and
weighting them by all surviving policies is the classic German BU modelling error. It is
economically large: on a claim incepting at 45 on a contract to 67 it removes 22 years of premium as
well as adding 22 years of annuity. For a typical office tariff the waived premium is of the order
of 5 % of the annuity paid **[std]**; for a manual trade, where the premium is three times as large
for the same *BU-Rente*, it approaches 15 %.

### Karenzzeit and rückwirkende Leistung

**The rules.** A *Karenzzeit* is an agreed deferment between the onset of BU and the first payment
[S1], and once a claim is recognised benefit is paid back to the onset (after any *Karenzzeit*)
rather than from the date of the decision.

**What they do.** Combined with the *Sechs-Monats-Fiktion*, retroactivity means the first payment
on a typical claim is a lump sum covering the elapsed months plus the current one. The premium
keeps being paid in the meantime and is refunded for the period the retroactive benefit covers when
the *Beitragsbefreiung* is applied retroactively. That is now sourced rather than assumed: "Bis zur
Entscheidung über die Leistungspflicht müssen Sie die Beiträge in voller Höhe weiter entrichten; wir
werden diese jedoch bei Anerkennung der Leistungspflicht zurückzahlen" [S1]. The composite starts
the *Beitragsbefreiung* at the benefit date and treats the interim premium and its refund as netting
to zero, which is exactly what that clause produces. A *Karenzzeit* cuts the premium at a real cost in cover, and is one
of the two levers consumer advice warns against using [S16] — the other being a reduced *Endalter*.

### Leistungsdauer, Versicherungsdauer and the Endalter

**The rule.** Two periods, not one. The *Versicherungsdauer* is the period during which a BU may
incept and be covered — a BU beginning after it ends is not covered at all — while the
*Leistungsdauer* is the period over which benefit is paid on a covered claim, stopping at the
*Leistungsendalter* even if the insured is still *berufsunfähig* [S1].

**What it does.** In the market standard the two are equal and both end at the agreed *Endalter*;
where they differ, the *Leistungsdauer* is the shorter, a cheaper design `[unverified]`. **The
premium is extremely sensitive to the *Endalter***, because the last years before retirement carry
by far the highest *Invalidisierungswahrscheinlichkeiten*: moving it from 67 to 60 removes the
seven most expensive years of cover and a large share of the expected claim cost `[unverified]` as
to magnitude. It is the single most effective premium lever in the product, and the one consumer
advice warns hardest against. **A claim in payment at the *Leistungsendalter* simply stops** — no
commutation, no residual value, no conversion into an old-age annuity; in a BUZ on a
*Rentenversicherung* the host contract's annuity then begins, which is exactly why the rider form
is sold.

### Bruttobeitrag, Zahlbeitrag and the Beitragsverrechnung

**The rule.** § 153 VVG, applied to BU through § 176, entitles the policyholder to a share of the
*Überschuss* and of the *Bewertungsreserven* unless participation is expressly excluded, allocated
by a *verursachungsorientiertes Verfahren* [R10] [R5] [REG-R24]. The MindZV prescribes the minimum
share of *Rohüberschuss* allocated to the *Rückstellung für Beitragsrückerstattung* by source; the
**risk-result minimum** is **90 %** of the risk result (MindZV § 7), and the *übriges Ergebnis* —
for a BU book essentially the expense result — carries a minimum of **50 %** (MindZV § 8) [R14]
[REG-R18]. Since a BU book's surplus is overwhelmingly risk plus expense surplus, it is that pair,
not the 90 % alone, that ties claims experience to the *Zahlbeitrag*. § 138 Abs. 1 VAG requires
premiums sufficient to meet the obligations permanently, and Abs. 2 equal treatment of equal risks —
"Bei gleichen Voraussetzungen dürfen Prämien und Leistungen nur nach gleichen Grundsätzen bemessen
werden", the principle that legitimises *Berufsgruppen* [R15] [REG-R8]. **Unisex is not in the VAG**:
it follows from § 19 Abs. 1 Nr. 2 AGG with the transitional § 33 Abs. 5 AGG, which permits
sex-differentiated premiums only for insurance relationships "die vor dem 21. Dezember 2012 begründet
werden" [REG-R34].

**What it does — the mechanic with no counterpart in the US, UK or French products in this
repository.** A German BU tariff is quoted as **two numbers**: the *Bruttobeitrag*, computed on
first-order bases and the **contractually guaranteed maximum the insurer may ever charge**; and the
*Zahlbeitrag*, what the policyholder actually pays after the anticipated surplus — overwhelmingly
**risk surplus**, because the first-order *Invalidisierungswahrscheinlichkeiten* are deliberately
prudent, plus expense surplus, with a small interest component — has been credited immediately
against the premium by *Beitragsverrechnung*.

**The gap is large and it is a risk to the buyer, and that is the point.** If risk experience
deteriorates or expense surplus falls, the insurer may reduce the *Beitragsverrechnung* and raise
the *Zahlbeitrag* — up to the *Bruttobeitrag* and no further. A buyer who chose on *Zahlbeitrag*
alone can face an increase of 40 % or more with no change in cover and no right to complain, which
is why consumer advice says to compare *Bruttobeiträge* [S16] and why the ratings score
*Beitragsverrechnung* stability [R22] [R23]. **The empirical frequency and size of such increases
is not established** and is a named gap.

Alternative *Überschussverwendungen* appear in some tariffs — a *Bonusrente* in which surplus buys
additional *BU-Rente*, *verzinsliche Ansammlung*, and an *Überschussrente im Leistungsfall* — with
market shares `[unverified]`. *Beitragsverrechnung* is dominant and is what the composite models,
and two retrieved AVB describe it directly: surplus shares assigned as a percentage of the tariff
premium and set off against it, so that "nicht der volle Tarifbeitrag (Bruttobeitrag), sondern nur
der entsprechend ermäßigte Nettobeitrag gezahlt werden muss" [S6], and "Die laufenden
Überschussanteile werden mit dem Tarifbeitrag verrechnet" [S12]. Both offer a *Bonusrente* as the
alternative form.
The reference implementation projects **both** streams: the *Bruttobeitrag* as premium income and
the *Beitragsverrechnung* as an explicit surplus-credit outgo line, so that **the gap between them
*is* the modelled *Überschussbeteiligung***. There is no surplus account, no RfB and no declaration
mechanic — a deliberate simplification which is *correct* for BU precisely because the surplus is
applied immediately rather than accumulated.

### Exclusions and the Infektionsklausel

**The rules.** The exclusion list is short by international standards and broadly uniform
`[unverified]` as to any particular carrier: BU caused by war or internal unrest, with a carve-out
where the insured is passively caught up in it; by the deliberate execution or attempted execution
of a crime; by intentional self-harm — and here a correction: § 161 VVG is a **death-cover** rule
("Bei einer Versicherung für den Todesfall …") whose three-year window has no application to a
self-inflicted *impairment*, and the market's conditions do not run a window at all. They exclude,
without any time limit, BU caused by "absichtliche Herbeiführung von Krankheit, absichtliche
Herbeiführung mehr als altersentsprechenden Kräfteverfalls, absichtliche Selbstverletzung oder
versuchte Selbsttötung" [S1] [R11] [R5]; by nuclear energy; and in some wordings by aviation other than
as a passenger and defined hazardous activities [S1]. The ***Infektionsklausel*** runs the other
way: it **deems** an official *Tätigkeitsverbot* imposed under the *Infektionsschutzgesetz* to be
BU, so a doctor, dentist, nurse or laboratory worker forbidden to practise because she is infected
or a carrier receives the *BU-Rente* with no 50 % medical test [R30] — standard for physicians and
dentists, common for nursing and medical assistants.

**What is notably *not* excluded** is illness of any kind, **including psychiatric illness** — the
largest single cause of BU, recalled at about a third of claims against under a tenth for accidents
[R22] `[unverified]`. A cheaper "BU ohne Psyche" variant exists at the margin `[unverified]`;
consumer advice is uniformly against it. **Model consequence:** exclusions are absorbed into the
calibration of the inception rate rather than modelled separately, and the *Infektionsklausel* is
treated as what it is in pricing terms — a higher inception rate in one occupational segment, which
is already how *Berufsgruppen* enter. Modelling it as a distinct trigger would need a ban-incidence
assumption no public source supplies, and the causes distribution enters this file only as the
reason not to offer an accident-only variant.

---

## Riders and options

**In scope, modelled or parameterized.**

- ***Leistungsdynamik***, the in-claim annual escalation of the *BU-Rente*, **on in the base run at
  2 % [std]**. It is the more important of the two escalations for a liability projection because it
  compounds over what can be a thirty-year payment period: on a claim incepting at 40 and running to
  67 it raises the final payment to about **1,70×** the first and the total benefit paid by roughly
  a third against a level annuity — arithmetic, not a source.
- ***Beitragsdynamik***, the pre-claim annual escalation of premium and insured *BU-Rente* without
  renewed *Gesundheitsprüfung*, carried as the second **premium form** and **off in the base run**.
  Take-up is folded into the effective escalation rate rather than modelled as a separate decision,
  which is the honest treatment of an option whose decline rules — two or three consecutive
  declines extinguish it permanently `[unverified]` — no source quantifies.
- ***Karenzzeit***, a model-point column, **0 in the base run**, with 3, 6 and 12 exercised;
  ***Wiedereingliederungshilfe***, **on at 6 monthly *Renten* [std]**, paid once on a completed
  return to work; ***Risikozuschlag***, a multiplier on the *Bruttobeitrag*, **1,00 in the base
  run**; and the ***Verlängerungsoption***, expressed as the model-point *Endalter*, because a right
  exercised in a window before the original *Endalter* changes the contract's parameters, not its
  recursion.
- ***AU-Klausel***, present as machinery and **inert**: a switch and an inception uplift, with the
  uplift shipped at **1,00 on every model point**. That is deliberate, and the reason has narrowed.
  **The clause itself is now documented.** It pays the full *BU-Rente* on a certificate of continuous
  *Arbeitsunfähigkeit* without the insurer determining that BU exists, and so raises the effective
  inception rate and brings payment forward. Its three bounding parameters are established at carrier
  level: the qualifying period is "6-monatige ununterbrochene Krankschreibung", or four months plus a
  specialist's certificate that it will run two more; the cap is "max. 24 Monate pro Vertragslaufzeit
  – auch bei mehrfacher Arbeitsunfähigkeit" at that carrier and up to 36 months at another; and
  payments are set off — "Wird rückwirkend eine BU anerkannt, werden erbrachte AU-Leistungen mit den
  BU-Leistungen verrechnet (keine Doppelzahlung)" [S4] [S6] [S8] [S12]. The GDV model conditions for
  the AU variant leave all three blank as *unternehmensindividuell*, add that the AU claim requires
  a BU claim to have been made, and forbid paying both at once. **What no retrieved document gives is
  the price**: the clause is sold "gegen einen geringen Mehrbeitrag" and no source quantifies the
  uplift, so the composite still ships the parameter unset rather than inventing one, and the model
  point that switches the clause on remains an **invariance test**: the option is present and
  demonstrably moves nothing until a user supplies a number.

**Out of scope, specified here and not modelled.**

- ***Nachversicherungsgarantie***, the right to increase the insured *BU-Rente* without a fresh
  *Gesundheitsprüfung* on a defined event — marriage or registered partnership, birth or adoption,
  completion of studies or training, a first job or substantial pay rise, property purchase or a
  mortgage, starting self-employment, and in some tariffs the death of a partner or a divorce; with
  event-independent windows in some tariffs, per-event and aggregate caps, an age limit, an exercise
  window and the *Angemessenheitsgrenze* on income. **The shape is no longer recalled.** One
  retrieved AVB gives the whole apparatus: a per-event cap of 6 000 EUR of annual *BU-Rente*, 12 000
  EUR for three income-based events, an aggregate of 18 000 EUR, 30 000 EUR including a separate
  *Berufseinsteiger* guarantee, an age limit of 50 (35 for that guarantee) and a twelve-month window
  from each event [S4]; another caps the total BU, EU and *Grundfähigkeit* entitlement — including
  other private and occupational entitlements — at "nicht mehr als 60 % des regelmäßigen jährlichen
  Bruttoeinkommens", 25 % for *Beamte*, with a 50 EUR minimum increase and the same age limit and
  window [S9]. The **event lists** and the caps differ between the two, which is where the variation
  actually lies; the "may at most be doubled" formulation was a recollection and is withdrawn [S1]
  [S4] [S9]. **It is the single
  most valuable option in the German BU product**, because it lets a healthy 25-year-old lock in
  insurability cheaply and build the cover as income grows. Any on-run needs a take-up assumption
  **and** an anti-selection loading on the incremental cover, and neither is sourceable — so it is
  specified and named as unmodelled, which is the honest treatment.
- The ***Infektionsklausel***; ***Umorganisationshilfe***, ***Reha-Hilfe***, ***Soforthilfe*** and
  *Pflege* add-ons; ***Bonusrente***, ***verzinsliche Ansammlung*** and the ***Überschussrente im
  Leistungsfall***; ***Stundung*** and ***Anwartschaft***; and a ***Staffelregelung*** or "Teil-BU"
  paying a partial *BU-Rente* between 25 % and 50 % `[unverified]`, against which the composite
  models the all-or-nothing form.

---

## Variations across insurers

**This table records where the variation lies, not who sits where.** Five insurer wordings were
retrieved and read for the provenance pass of 2026-08-30 — Alte Leipziger, NÜRNBERGER, VOLKSWOHL
BUND, Debeka and CosmosDirekt [S4] [S6] [S9] [S12] — together with the GDV model conditions for the
SBU, the BUZ and the BU-with-AU variant [S1] [S2] [S8]. Where a row now names a reading, the reading
comes from one of those documents and the tag says which. **What is still missing is price**: no
tariff table, no occupational factor and no *Brutto* / *Zahlbeitrag* pair was obtained, so no row
compares carriers on cost, and a row that would need one carries `[unverified]`.

| Feature | Market position | Where carriers genuinely differ | Composite | Tag |
|---|---|---|---|---|
| BU definition — last occupation, 50 % degree | Uniform in shape, descended from the GDV model text; the **numbers are not in the model text**, which leaves the degree and the prognosis period blank | The degree is 50 % across the retrieved wordings; the *Prognosezeitraum* is not — "auf Dauer (mindestens 3 Jahre)" at one carrier, shortened as a tier upgrade at another | Market standard, 50 % | [S1] [S12] [R1] [REG-R37] |
| *Abstrakte Verweisung* | Waived by essentially all current tariffs | Legacy books only | Waived | [S1]–[S12] [REG-R37] |
| *Konkrete Verweisung* | Retained; the *Lebensstellung* threshold is stated in the wordings and quantified at a 20 % income reduction | Whether it is waived on a material income drop; how the 20 % is applied — one carrier fixes it "je nach Lage des Einzelfalls … jedoch maximal 20 %" | Retained, folded into the termination rate | [S1] [S12] |
| *Prognosezeitraum*, retroactivity | Prognosis period set per carrier, up to three years; **six months is the *Fiktion*, not the prognosis**. The claim arises with the end of the month in which BU began | The prognosis period is a headline differentiator and a tier upgrade; whether the *Fiktion* pays back to onset or only forward | 6 months, from onset | [S1] [S12] |
| *Anerkenntnis* and *Nachprüfung* | Time limitation permitted once and only on a stated *sachlicher Grund*, § 173 and [S1]; re-examination by medical examination at most once a year under the retrieved wordings | Maximum length of a *befristetes Anerkenntnis*, some waiving it; some waive the *Nachprüfung* after a stated benefit duration — no retrieved wording states either `[unverified]` | Continuous termination rate; no acknowledged state | [R2] [R3] [S1] |
| Three-month run-off | Statutory floor, § 174 | Some contract for longer | Three months exactly | [R3] [REG-R29] |
| *Karenzzeit* menu | 0 as standard; where agreed it defers the pension only and lowers the premium | The menu of durations, which sits in the *Tarifbestimmungen* and was not retrieved `[unverified]`; whether a served *Karenzzeit* is credited on a recurrence — one carrier credits it within 24 months from the same cause | 0, with 3, 6, 12 exercised | [S4] [S9] |
| *Endalter* menu | 65 or 67 | 60 / 62 / 63 as budget options — the menu sits in the *Tarifbestimmungen*, none of which was retrieved | 67, with 60 and a split 63/67 exercised | `[unverified]` |
| *Leistungsdauer* vs *Versicherungsdauer* | Two distinct periods, defined separately in every retrieved wording; equal in the standard sale | A shorter *Leistungsdauer* as a cheaper design | Equal, with one split model point | [S1] [S9] |
| *AU-Klausel* | The principal differentiator, and now documented: full *BU-Rente*, paid on a certificate rather than on a BU determination | Present or absent; the qualifying period (6 months, or 4 plus a specialist prognosis); the cap — 24 months per contract at one carrier, up to 36 at another; whether a parallel BU claim is required; set-off against a later BU award, which one carrier applies expressly | Present, inert | [S4] [S6] [S8] [S12] |
| *Nachversicherungsgarantie* | Present everywhere; event-triggered, without renewed health questions, with an age limit of 50 and a twelve-month window in both retrieved wordings | Event-list breadth, and the caps: 6 000 EUR per event with an 18 000 / 30 000 EUR aggregate at one carrier, a 60 %-of-gross-income ceiling on total entitlement at another | Specified, not modelled | [S4] [S9] |
| *Leistungsdynamik* | Offered everywhere | 1 – 3 % fixed, or index-linked | 2 % fixed **[std]** | `[unverified]` |
| *Beitragsdynamik* | Offered everywhere | 1 – 10 %, commonly 3 % or 5 %; two or three declines extinguish it | 3 % **[std]**, off in the base run | `[unverified]` |
| *Wiedereingliederungshilfe* | Common | 3 to 12 monthly *Renten* | 6 **[std]** | `[unverified]` |
| *Infektionsklausel* | Standard for medical occupations | Scope of occupations covered | Not modelled | [R30] `[unverified]` |
| *Berufsgruppen* | 4 – 6 typical | 3 at direct writers to 10+ at specialists; which occupations are declined; **the classes are not comparable across carriers** | Five classes, 1,00 – 4,50 **[std]** | [S6] `[unverified]` |
| *Zahlbeitrag* / *Bruttobeitrag* | 0,50 – 0,80 | **The widest and least transparent variation in the product** | 0,70 **[std]** | `[unverified]` |
| Channel | Broker vs direct vs bank/*Öffentliche* | Option breadth and occupational appetite track the **channel**, not the carrier: direct and bank channels sell simpler tariffs, narrower coverage, fewer options | Broker-channel design | [S12] |

**What the composite is, in one paragraph.** A single-life individual standalone SBU on a monthly
grid; the market-standard definition — last occupation, 50 %, six-month prognosis with the
six-month fiction, *abstrakte Verweisung* waived, *konkrete Verweisung* retained; a level
*Bruttobeitrag* guaranteed for the term with a *Zahlbeitrag* of 0,70 × *Bruttobeitrag* **[std]**,
so the *Brutto*/*Zahl* gap **is** the modelled *Überschussbeteiligung* and no surplus account is
needed; a monthly *BU-Rente* in advance from onset, no *Karenzzeit*, *Leistungsdynamik* 2 %
**[std]**; full *Beitragsbefreiung* in claim; benefit ending at the *Leistungsendalter*, on death,
or on a *Nachprüfung* termination followed by the statutory three-month run-off; *Reaktivierung*
returning the life to the premium-paying state with a *Wiedereingliederungshilfe* of six monthly
*Renten* **[std]**; an acceptance factor of 0,80 **[std]** on the inception rate; occupational
rating as a multiplicative factor on that rate, 1,00 office and 3,00 reference manual **[std]**; and
no surrender or paid-up cash flow modelled.

---

## Regulatory context

**Contract law — the VVG.** The product's own chapter is §§ 172–177: § 172 the definition and the
permission to agree an *abstrakte Verweisung*; § 173 the *Anerkenntnis* and its once-only time
limitation; § 174 the *Leistungsfreiheit* and its three-month notice; § 175 making §§ 173–174
*halbzwingend*; § 176 applying §§ 150–170 *entsprechend*; and § 177 extending §§ 173–176 to every
contract promising a benefit for a ***dauerhafte*** impairment of working capacity [R1]–[R6]
[REG-R29]. **Two readings of § 177 have been corrected against the text.** It reaches only cover of
a *lasting* impairment — *Grundfähigkeits-* and *Erwerbsunfähigkeitsversicherung* — so a benefit for
temporary *Arbeitsunfähigkeit* does not come within it; an *AU-Klausel* is protected because it sits
inside a BU contract to which §§ 172 ff. apply directly. And Abs. 2 **excludes** accident insurance
and health-insurance contracts covering impaired working capacity, so it does not extend the frame
to accident cover. **§ 176's reach is no longer a gap**: it applies "die §§ 150 bis 170 … entsprechend
…, soweit die Besonderheiten dieser Versicherung nicht entgegenstehen", which is the authority for an
*Überschussbeteiligung* (§ 153) [R10] [REG-R24], a *prämienfreie Versicherung* (§ 165) [R8], a
*Kündigung* right and a *Rückkaufswert* (§§ 168–169) [R9] [REG-R28] and, subject to that reservation,
the *Selbsttötung* rule (§ 161) [R11]. The reservation matters twice over: § 169 Abs. 1 is drafted
for risks whose occurrence is certain, and § 161 for death cover. Outside it, § 19 governs the
*vorvertragliche Anzeigepflicht* and the insurer's remedies for a breach of it while **§ 21 Abs. 3**
— not § 19 — extinguishes those remedies after five years, ten on intent or fraud, and not at all
for claims that arose inside the period, § 157 the misstatement of age, and § 158 the rule that **an increase in
risk counts as such only where expressly agreed to** — which is why a German BU contract carries no
general occupation-change clause and why this model needs no reunderwriting state [R7] [REG-R30].

**Disclosure.** The VVG-InfoV mandates the *Produktinformationsblatt* for life and BU contracts
[R12] [REG-R31]. For a savings contract it also mandates the *Effektivkosten*, but **for a pure risk
contract there is no yield to reduce**, so a BU PIB discloses costs only through the
*Brutto*/*Zahlbeitrag* pair [S13]; and because PRIIPs reaches *insurance-based investment products*,
**a standalone SBU normally has no *Basisinformationsblatt* at all** [S14] [REG-R32] — the opposite
of delib's savings products, where the KID is the richest public document. Those two absences are
why every charge assumption here is **[std]** while the delib endowment's are not. Distribution sits
under the IDD and § 34d GewO, with §§ 6, 7 and 1a VVG and BaFin's *Merkblatt 01/2023 (VA)* on
*Wohlverhaltensaufsicht* above them [REG-R33] [REG-R31] [REG-R35].

**Supervision and pricing.** § 138 VAG requires premiums sufficient to meet the obligations
permanently and equal treatment of equal risks; § 139 governs the *Überschussbeteiligung* on the
supervisory side; §§ 141–143 place the bases with the *Verantwortlicher Aktuar* [R15] [REG-R8]
[REG-R9] [REG-R11]. The DeckRV fixes the *Höchstrechnungszins* — **0,25 % for contracts written
2022–2024, raised to 1,00 % from 1 January 2025** `[unverified] on both figures and the date` — and
the *Höchstzillmersatz* of 25 ‰ [R13] [REG-R14]–[REG-R16]; the MindZV prescribes the minimum
allocation of *Rohüberschuss* to the RfB by source, the risk-result minimum being the one that
governs a BU book [R14] [REG-R18] [REG-R19]. **Unisex pricing** has been compulsory since
21 December 2012 [R15] [REG-R34] and bites unusually hard here: the underlying
*Invalidisierungswahrscheinlichkeiten* differ materially by sex `[unverified]`, so a unisex tariff
embeds a portfolio mix assumption the insurer bears the risk of. BaFin supervises *Leistungsprüfung*
practice as a conduct matter and publishes the *Beschwerdestatistik*, in which BU is persistently
over-represented relative to its premium share `[unverified]` [R19].

**Actuarial bases.** The German BU standard is the **DAV 1997 family** — **DAV 1997 I** for
*Invalidisierungswahrscheinlichkeiten*, **DAV 1997 RI** for *Reaktivierungswahrscheinlichkeiten* by
age at disablement and duration since disablement, **DAV 1997 TI** for
*Sterbewahrscheinlichkeiten der Invaliden* — with a *Todesfall*-character active-lives table,
**DAV 2008 T** [R16] [R17] [REG-R50] [REG-R48]. **These are the property of the Deutsche
Aktuarvereinigung, are not public, and are not redistributed by delib.** Three findings belong on
the record: the **naming is itself uncertain**, since reading "TI" as the reactivation table would
leave disabled-life mortality unspecified, which no multi-state BU model can do [REG-R50];
**whether a successor to DAV 1997 I exists in general market use could not be established** [R16]
[R18]; and **the age of the basis is a finding in itself** — tables built in 1997 on older
experience, against a population whose causes mix has moved decisively towards psychiatric diagnoses
and whose incentives changed when the statutory *Berufsunfähigkeitsrente* closed to the post-1960
cohorts, carry a heavy safety loading, which is **why the German BU market runs a large and
persistent *Bruttobeitrag*/*Zahlbeitrag* gap** [REG-R50] [REG-R37]. The two-basis structure this
implies — *erster Ordnung* for the tariff and the *Deckungsrückstellung*, *zweiter Ordnung* for what
actually happens, with the *Sicherheitszuschlag* between them released as *Risikoüberschuss* — is
set out at [REG-R47], and the direction of prudence for a disability product is **higher incidence
and lower reactivation**.

**Reserving and prudential.** A BU book carries **two reserves, not one**: a *Deckungsrückstellung*
for **active** lives, the prospective difference between future benefits and future premiums; and a
*Leistungsrückstellung* — a *Deckungsrückstellung für laufende Renten* — for **claims in payment**,
the present value of the remaining annuity on disabled-lives bases, much the larger per life [R9]
[R21]. Above them sit the statutory accounts under §§ 341–341o HGB and the RechVersV [REG-R54],
Solvency II best estimate plus risk margin [REG-R1] [REG-R2] [REG-R4], and IFRS 17 [REG-R55].
**delib computes none of them**: it publishes gross undiscounted liability cash flows and names the
valuation layers rather than reproducing them.

**Taxation, and why the same liability is sold in two wrappers.** For a **standalone SBU
(Schicht 3)** the premium is a *sonstige Vorsorgeaufwendung* under § 10 Abs. 1 Nr. 3a EStG,
deductible only inside an annual ceiling recalled as **1 900 €** (employees, civil servants) or
**2 800 €** (self-employed) `[unverified]` — in practice already consumed by statutory health and
long-term-care contributions, so **the effective deduction for most buyers is nil**. The *BU-Rente*
is then an *abgekürzte Leibrente* taxed on its ***Ertragsanteil*** under § 22 Nr. 1 EStG, read from
a table keyed on the annuity's **remaining term at the start of payment** rather than on the
recipient's age — recalled at about 5 % for 5 years remaining, 12 % for 10, 16 % for 15, 21 % for
20, 26 % for 25 and 30 % for 30, all `[unverified]` [R27] [REG-R41]. For **BU inside a *Basisrente*
(Schicht 1)** the whole premium is an *Altersvorsorgeaufwendung* deductible within the much larger
*Basisrente* ceiling, provided the benefit is an annuity, does not run beyond the host's deferment,
and is **no more than 49 %** of the total premium `[unverified]`; in exchange the *BU-Rente* is
fully taxable at the cohort *Besteuerungsanteil* [R27] [R28] [REG-R38] [REG-R39]. The trade is not
obviously favourable, and the 49 % rule forces a large savings premium alongside the cover, which is
why the standalone SBU remains the dominant retail form. **delib projects gross, pre-tax cash flows
in every product**, so nothing in the model depends on any of these figures and nothing here asserts
them.

**Case law.** Four settled BGH lines govern the claim in practice, each recalled in substance and
`[unverified]` in every detail, with **no docket number given anywhere in this library** because
none could be confirmed: the binding effect of the *Anerkenntnis*; the *Nachprüfung*'s requirement
of a **demonstrated change** rather than a re-decision; *Lebensstellung* as the limit on any
*Verweisung*; and the self-employed insured's ***Umorganisationspflicht***, to consider whether the
business can be reorganised so she can continue within her remaining capacity — but only where that
is economically sensible and does not cost her a substantial part of her income or her leading
position [R29] [REG-R36].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-berufsunfaehigkeit-r1
[R10]: #delib-berufsunfaehigkeit-r10
[R11]: #delib-berufsunfaehigkeit-r11
[R12]: #delib-berufsunfaehigkeit-r12
[R13]: #delib-berufsunfaehigkeit-r13
[R14]: #delib-berufsunfaehigkeit-r14
[R15]: #delib-berufsunfaehigkeit-r15
[R16]: #delib-berufsunfaehigkeit-r16
[R17]: #delib-berufsunfaehigkeit-r17
[R18]: #delib-berufsunfaehigkeit-r18
[R19]: #delib-berufsunfaehigkeit-r19
[R2]: #delib-berufsunfaehigkeit-r2
[R20]: #delib-berufsunfaehigkeit-r20
[R21]: #delib-berufsunfaehigkeit-r21
[R22]: #delib-berufsunfaehigkeit-r22
[R23]: #delib-berufsunfaehigkeit-r23
[R24]: #delib-berufsunfaehigkeit-r24
[R25]: #delib-berufsunfaehigkeit-r25
[R27]: #delib-berufsunfaehigkeit-r27
[R28]: #delib-berufsunfaehigkeit-r28
[R29]: #delib-berufsunfaehigkeit-r29
[R3]: #delib-berufsunfaehigkeit-r3
[R30]: #delib-berufsunfaehigkeit-r30
[R31]: #delib-berufsunfaehigkeit-r31
[R4]: #delib-berufsunfaehigkeit-r4
[R5]: #delib-berufsunfaehigkeit-r5
[R6]: #delib-berufsunfaehigkeit-r6
[R7]: #delib-berufsunfaehigkeit-r7
[R8]: #delib-berufsunfaehigkeit-r8
[R9]: #delib-berufsunfaehigkeit-r9
[REG-R1]: #delib-reg-r1
[REG-R11]: #delib-reg-r11
[REG-R14]: #delib-reg-r14
[REG-R16]: #delib-reg-r16
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R28]: #delib-reg-r28
[REG-R29]: #delib-reg-r29
[REG-R30]: #delib-reg-r30
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R37]: #delib-reg-r37
[REG-R38]: #delib-reg-r38
[REG-R39]: #delib-reg-r39
[REG-R4]: #delib-reg-r4
[REG-R41]: #delib-reg-r41
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R50]: #delib-reg-r50
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R8]: #delib-reg-r8
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
