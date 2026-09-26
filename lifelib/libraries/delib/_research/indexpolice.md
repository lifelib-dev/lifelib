# Indexgebundene Rentenversicherung (*Indexpolice*, "Neue Klassik") — research notes (Germany)

Research notes for the German individual *indexgebundene Rentenversicherung* — the deferred private
annuity, marketed as an *Indexpolice*, in which the accumulated capital sits in the insurer's
*Sicherungsvermögen* (the general-account cover pool) under a guarantee, and the annually declared
*Überschuss* (surplus) is **not credited as interest** but spent as an **option budget** buying a
one-year participation in a share index. The participation is bounded above by a **Cap** on each
month's index return or by a **Partizipationsquote** on the year's return; the capped monthly
returns are **summed** over the *Indexjahr*, with negative months entering **in full and uncapped**;
the year's credit can never be negative; whatever is credited is **locked in** (*Ratchet*,
*Höchststandsicherung*); and the policyholder holds an **annual Wahlrecht** to switch between
*Indexbeteiligung* and *sichere Verzinsung* for the coming year.

**In scope.** The individual, privately written *aufgeschobene Rentenversicherung* of *Schicht 3*
whose *Überschussverwendung* is an index participation: single life, level *Beitrag* over a
*Beitragszahlungsdauer*, capital held in the general account and not in an *Anlagestock*, a
*Beitragsgarantie* or guaranteed capital falling due at *Rentenbeginn*, conversion into a lifelong
*Leibrente* at a *Rentenfaktor*, with a *Kapitalwahlrecht*. The same index module is written on the
*Basisrente* and *Riester* chassis and, in the market, on *Direktversicherung*; those wrappers are
named here only where the wrapper changes the index mechanics (it changes the guarantee level, and
that matters).

**Out of scope, and said so where it matters.**
- The *fondsgebundene Rentenversicherung* (delib product 3) is a genuinely unit-linked contract:
  the policyholder's money buys fund units in an *Anlagestock*, the *Rückkaufswert* is a *Zeitwert*
  of units, and the investment risk sits with the policyholder. **An Indexpolice is not that**, and
  the single most common misunderstanding of the product is to treat it as one.
- The *klassische Rentenversicherung* (product 2) is the same chassis with the surplus credited as
  interest. This file treats product 2's accumulation phase, *Rentenfaktor* and *Rentenphase* as
  the inherited chassis and documents only the delta.
- Structured retail products with the same payoff shape sold outside an insurance wrapper
  (*Indexzertifikate*, *Aktienanleihen*, *Bonuszertifikate*) are outside the library.
- *Betriebliche Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung*, *private
  Krankenversicherung* and *Sterbegeldversicherung* are outside the delib library entirely.
- Austrian and Swiss index products are excluded: the VVG, the DeckRV, the MindZV and the AltZertG
  do not apply to them.

These notes are the **citation ground truth** for the delib `indexpolice` product documents
(`product-spec.md`, `technical-notes.md`, `model.md`, `sources.md`). Source ids **S1..S16** and
**R1..R22** below are **frozen — never renumber**; unused ids are simply omitted downstream, leaving
gaps, and `sources.md` records which are absent and why.

Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

Read this before reading anything else in the file, because it changes what every citation below
means. It has two halves: the conditions the research was **done** under on 2026-08-29, and what the
**re-verification** of 2026-08-30 established. The first is kept because it is how this file came to
say what it says; the second is what a reader should weigh each entry by.

**No document in this file had been retrieved when it was written.** Direct HTTP egress from the
build environment was blocked by an organisation network policy: `WebFetch` and `curl` were refused
with HTTP 403 at the egress gateway for every host outside a short package-registry allowlist. The hosts that matter for
this product were tried and refused: `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
`bundesfinanzministerium.de`, `dejure.org`, `buzer.de`, `destatis.de`, `de.wikipedia.org`. No
*Bedingungswerk*, no *Produktinformationsblatt*, no *Basisinformationsblatt*, no statutory text, no
BaFin *Merkblatt* and no index rulebook was opened.

**The session's `WebSearch` budget was exhausted before this product was researched.** The library
shares a hard cap of 200 search calls; the cap had been reached during the regulatory and
contract-law research and during products 1 and 2. Every search attempted for this product returned
the budget-exhausted message. **This file therefore had no research channel at all while it was
drafted**: its first draft rested on the authoring model's own knowledge of German insurance law,
German life-insurance product design and German market practice, disciplined by the rules below.

What that meant for every claim in the draft:

1. **Source entries were known references, not evidence.** Each `S#` and `R#` below names a document
   that exists and is the right kind of document for this product — an insurer's *Allgemeine
   Versicherungsbedingungen*, a *Produktinformationsblatt*, a PRIIP *Basisinformationsblatt*, a
   statutory instrument, a supervisory *Merkblatt*. The entry records publisher and document type,
   says `URL: not established` unless the canonical form is one this author is confident of, and
   recorded `Retrieved: no — direct HTTP egress blocked; no search corroboration (session search
   budget exhausted)`. **No document number, edition date, page count or publication date was
   asserted anywhere in the drafted file**, because none could be established, and none was guessed.
   **This is the rule the re-verification overtook**: the entries now carry editions, `Stand` lines
   and page counts for the documents that were opened, and only for those.
2. **No verbatim quotation appears anywhere in this file.** Statutory and contractual content is
   described in this author's own words as *what the instrument provides*; no sentence is placed in
   quotation marks and attributed to any *Bedingungswerk*, statute or supervisory document, because
   there is neither a retrieval nor a search summary to attribute one to. That is the sharpest
   difference from `frlib/_research/temporaire-deces.md`, whose PDFs were downloaded and read, and
   from the two sibling delib files, whose search summaries reproduced German sentences.
3. **`[unverified]` is used generously.** Every specific paragraph number, effective date, amount,
   percentage, cap level, participation rate, product name and market figure is tagged unless it is
   a structural fact of the product that is not in dispute. The general shape of a well-established
   mechanic — surplus finances an option, monthly returns are capped and summed, the year cannot end
   negative — is *not* tagged, because tagging it would drown the signal.
4. **Uncertain numbers become `[std]` parameters, not citations.** Where the mechanic is certain and
   the level is not — the Cap, the *Partizipationsquote*, the *Beitragsgarantie*, the
   *Rentenfaktor*, the charges, the lapse rate — the file states a `[std]` value with a rationale and
   an argued range. **A `[std]` number is honest; a fabricated `[S4]` number is not.** `indexpolice`
   carries a higher proportion of `[std]` parameters than any other delib product, and section 22
   and the gaps register say exactly which.
5. **Product names are the weakest class of claim here.** Every carrier product name below is
   recalled from general market knowledge and tagged `[unverified]`; gap 2 records this as the
   file's largest single defect. **No downstream document may present one as established.**

**What the re-verification established.** The policy was lifted, and on **2026-08-30** the citations
were checked against the primary documents. Library-wide, all fifteen German instruments delib cites
were read as canonical XML from `gesetze-im-internet.de` with each law's amendment `Stand` recorded,
950 statutory section references were checked and 950 were correct, and insurer AVB,
*Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read; **501
of the library's 805 source entries, 62 %, now read `Retrieved: yes`.** For this product: **32 of
the 38 entries below read `Retrieved: yes`, five read `no` ([S3], [S5], [S13], [S15], [R21]) and one
is mixed ([R10])** — the best-served file of the eleven. Two carrier *Bedingungswerke* were read in
full, which is what this file had called its central gap, together with a PRIIP KID, a *Neue
Klassik* comparator's KID, the GDV chassis wording and its *Muster-Standmitteilung*, an AltZertG
*Produktinformationsblatt* and a Zurich *Verbraucherinformation*. The five that stayed shut say
which wall they hit: a paywalled *Finanztest* [S13], comparison portals answering HTTP 403 [S15],
rating results kept behind the houses' own paid tools with the cited addresses answering HTTP 404
[R21], a document class that no one publishes at all [S5], and one entry naming a document class
that does not exist for this product [S3].

**What an entry now means.** A **`Retrieved: yes`** line means the document was opened and the
passage the entry rests on was read, and the line records the edition, page count or statutory
`Stand`. Where the line says **no**, a delib `indexpolice` citation is still a **pointer, not a
certificate**: it names the instrument a claim should be checked against and does not assert that
anyone checked it. **The re-verification changed things** — the gaps register below is
re-adjudicated item by item against the retrieved documents, and where a document contradicted the
drafted text the contradiction is stated rather than smoothed over. Treat a claim here as sound
where its entry says `Retrieved: yes`, and as provisional where it does not.

**What the file was nevertheless worth before any of that.** The mechanics of an *Indexpolice* are not in doubt and do
not depend on having a PDF open: the financing identity between declared surplus and option budget,
the sum-of-capped-monthly-returns payoff with uncapped negative months, the zero floor, the annual
lock-in, the annual *Wahlrecht*, and the way each lands in a cash-flow projection. The weight of the
file is deliberately in the extracted-facts-by-mechanic sections and the two constructed worked
examples, which is where a research file written under those conditions earned its place — and it is
those sections the retrieved wordings were then checked against.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on, over and above the vocabulary inherited from products 1 and 2:

| Term | Gloss |
|---|---|
| *Indexpolice*, *Indexrente*, *indexgebundene Rentenversicherung* | The market's names for this product: a general-account annuity whose surplus buys an index participation |
| *Indexbeteiligung*, *Indexpartizipation* | Index participation: the form of *Überschussverwendung* in which the year's surplus is spent on an index-linked payoff |
| *Sichere Verzinsung*, *klassische Verzinsung*, *Zinsvariante* | The alternative use of the same surplus: credit it as interest to the *Deckungskapital*, guaranteed once credited |
| *Wahlrecht*, *Umschichtungsrecht*, *jährliches Wechselrecht* | The policyholder's annual right to elect between the two, for the coming *Indexjahr* |
| *Indexjahr* | The twelve-month observation period over which the index participation is measured |
| *Indexstichtag*, *Beobachtungstag*, *Bewertungstag* | The date at which the index level is read — one at the start of the *Indexjahr* and one per month |
| *Cap*, *Höchstgrenze*, *Obergrenze der monatlichen Indexveränderung* | The ceiling applied to each month's index return before the twelve are summed |
| *Partizipationsquote*, *Partizipationsrate*, *Indexquote* | The alternative design: a fixed fraction of the year's index movement, without a monthly cap |
| *Indexrendite*, *Indexbeteiligungssatz* | The rate resulting from the payoff formula, applied to the participating capital |
| *Höchststandsicherung*, *Lock-in*, *jährliche Sicherung*, *Ratchet* | The rule that a credited index amount is permanently added and can never be lost |
| *Optionsbudget*, *Risikobudget* | The insurer's internal name for the amount of surplus spent on the option package |
| *Sicherungsvermögen* | The ring-fenced cover pool backing the insurer's guaranteed obligations; the general account |
| *Anlagestock* | The separate unit-linked asset pool of a *fondsgebundene* contract — what an Indexpolice does **not** use |
| *Neue Klassik* | Post-2013 conventional designs with a modified guarantee: the guarantee is due at *Rentenbeginn* rather than accruing year by year |
| *Beitragsgarantie*, *Beitragserhalt*, *Garantieniveau* | The guarantee expressed as a percentage of premiums paid, due at *Rentenbeginn* |
| *Garantiekapital*, *garantiertes Kapital zu Rentenbeginn* | The guaranteed capital at the end of the accumulation phase |
| *Rechnungszins*, *Höchstrechnungszins* | The technical interest rate the guarantee is priced and reserved on / its statutory maximum |
| *Überschussbeteiligung*, *Überschussanteile* | The statutory entitlement to a share of surplus / the amounts allocated to one contract |
| *Zinsüberschuss*, *Risikoüberschuss*, *Kostenüberschuss* | Interest, mortality and expense surplus |
| *Schlussüberschussanteil*, *Bewertungsreserven* | Terminal bonus / unrealised gains, shared under § 153 Abs. 3 VVG |
| *Deckungskapital*, *Deckungsrückstellung* | The contract's actuarial reserve / the balance-sheet provision |
| *Rentenfaktor* | Monthly annuity per 10 000 € of capital at *Rentenbeginn* |
| *Rentenbeginn*, *Aufschubphase*, *Rentenphase* | Annuity commencement / accumulation phase / payout phase |
| *Kapitalwahlrecht* | The right to take a lump sum instead of the annuity |
| *Rückkaufswert*, *Stornoabzug*, *Beitragsfreistellung* | Surrender value / the deduction from it / making the contract paid-up |
| *Ersatzindex*, *Indexanpassung* | The replacement index, and the clause permitting the substitution |
| *Treuhänder*, *Treuhänderklausel* | The independent trustee whose approval some contractual adjustments require |
| *Billiges Ermessen* | Reasonable discretion, § 315 BGB: the standard against which a discretionary determination such as a Cap is reviewable |
| *Preisindex*, *Kursindex* / *Performanceindex* | Price index (dividends excluded) / total-return index (dividends reinvested) — the distinction that decides how much of the equity return reaches the policyholder |
| *Multi-Asset-Index*, *Volatilitätssteuerung*, *Excess-Return-Index* | The house index families that replaced the EURO STOXX 50 in many tariffs |
| *Chancen-Risiko-Klasse* (CRK) | The 1-to-5 risk class assigned to certified *Basisrente* and *Riester* products by the *Produktinformationsstelle Altersvorsorge* |
| *Basisinformationsblatt* (PRIIP-KID), *Produktinformationsblatt* (PIB) | The EU key information document / the German pre-contractual product summary |
| *Standmitteilung* | The annual statement to the policyholder; the document in which an *Indexjahr* result is reported |

---

## Primary sources

**The uniform retrieval status this section once declared no longer holds, and each entry now
carries its own.** On **2026-08-30** the documents were tried again with a working network. Eleven of
the sixteen were retrieved and read — including the two carrier AVB [S2] [S7] that this file called
its central gap, a PRIIP KID [S4], the *Neue Klassik* comparator's KID [S6], the GDV chassis wording
and its *Muster-Standmitteilung* [S1] [S10], an AltZertG *Produktinformationsblatt* with a
*Chancen-Risiko-Klasse* for an index variant [S11], the Zurich *Verbraucherinformation* [S9] and
three secondary sources [S8] [S12] [S14] [S16]. Four were not: *Finanztest* is paywalled [S13], the
comparison portals answer HTTP 403 [S15], Stuttgarter does not publish its AVB [S8], and no
policyholder-facing annual notification is published at all [S5]. **One entry names a document class
that does not exist for this product** [S3]. Each entry states what was opened, in which edition, and
what it settled; where a `Content` block still records what a document of that kind *would* settle
rather than what it says, it says so, and the `[unverified]` tags that remain now carry a reason.

### S1 — GDV, *Musterbedingungen* for the *Rentenversicherung mit aufgeschobener Rentenzahlung*
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV)
- Doc type: *Musterbedingungen* — model AVB published by the industry association for members to
  adopt, adapt or ignore. They are not binding and are not a regulation.
- URL:
  `https://www.gdv.de/resource/blob/6294/61b4fedd6f69db77539816e3421c7eeb/allgemeine-bedingungen-fuer-die-rentenversicherung-mit-aufgeschobener-rentenzahlung-data.pdf`,
  from the *Musterbedingungen* index at `https://www.gdv.de/gdv/service/musterbedingungen`.
- Retrieved: **yes** — PDF, 20 pp., Stand 21.07.2025, read 2026-08-30; the index page read the same
  day. The model wording states its own status on page 1: "Diese Bedingungen sind für die Versicherer
  unverbindlich; ihre Verwendung ist rein fakultativ. Abweichende Bedingungen können vereinbart
  werden."
- Content — the chassis, and a finding about what is *not* in it, **both now read**:
  - The GDV model wording supplies the clause skeleton every German deferred annuity shares and the
    Indexpolice inherits unchanged: the *Erlebensfall* obligation at *Rentenbeginn*, the
    *Todesfallleistung* in the *Aufschubphase*, the *Überschussbeteiligung* clause, *Rückkaufswert*
    and *Beitragsfreistellung*, the *Rentenphase* clauses including *Rentengarantiezeit*, the duty of
    disclosure, and *Selbsttötung*.
  - **The GDV publishes no *Musterbedingungen* for an index participation module.** The
    *Indexbeteiligung* clause set is a carrier-specific construction throughout the market — the
    structural reason the wording varies more across insurers here than for any other delib product,
    and why no industry-standard formulation of the Cap mechanic exists to be cited. **Confirmed by
    reading the catalogue**: eleven life *Musterbedingungen* (kapitalbildende LV, aufgeschobene /
    sofort beginnende / fondsgebundene *Rentenversicherung*, the two AltZertG variants, *Basisrente*,
    *Risiko-* and *Restkredit-LV*, three *Zusatzversicherungen*) and nine *Muster-Standmitteilungen*,
    and not one is an index module. The tag comes off.
  - Consequence: the *Indexbeteiligung* clauses in the delib product specification are a
    **composite** reconstructed from the mechanics sections below, labelled as such and attributed to
    no carrier.

### S2 — Allianz Lebensversicherungs-AG, *Allgemeine Versicherungsbedingungen* / *Bedingungswerk* for **Allianz IndexSelect**
- Publisher: Allianz Lebensversicherungs-AG, Stuttgart
- Doc type: AVB / *Bedingungswerk* for a deferred annuity tariff with *Indexbeteiligung*
- URL: `https://goa-eportale.allianz.de/dlc_app/Intranet/dlc?nr=E----0025Z0&m=d`, linked as
  "Versicherungsbedingungen (PDF)" from `https://www.allianz.de/vorsorge/vorsorgekonzept/indexselect/`.
- Retrieved: **yes** — PDF, 42 pp., *Versicherungsbedingungen*, Teil A *Baustein Altersvorsorge —
  Zukunftsrente IndexSelect (Plus) E25*, form `E---A0025Z0 (014) 12/2025`, read 2026-08-30.
- Content — **the document this file called its single most important gap, now read**:
  - The product name is **Allianz Zukunftsrente IndexSelect (Plus)**, marketed as *Vorsorgekonzept
    IndexSelect*; the tag comes off. Allianz's own press release dates it to a 2007/2008 launch and
    puts the in-force count above 500.000 [S16], and the carrier's document catalogue shows the same
    module on the *Zukunftsrente*, *KinderPolice* and *StartPolice* chassis [S4].
  - **What the AVB settles, at Teil A Ziffer 3 (*Indexpartizipation und sichere Verzinsung*).** The
    payoff, Ziffer 3.3 Absatz 2 a): "die negativen monatlichen Wertentwicklungen und die mit dem
    jeweiligen →Cap … gedeckelten positiven, monatlichen Wertentwicklungen am Ende eines →Indexjahres
    aufsummiert … Ergibt sich nach der Aufsummierung eine negative jährliche Summe, setzen wir diese
    auf null." Monthly movements are "die prozentuale Veränderung des Index zwischen 2
    Bewertungsstichtagen, die wir Ihnen jährlich mitteilen" — closing levels, not an average. The
    base, Absatz 2 e): "Bezugsgröße für die →Indexpartizipation ist der →Policenwert zu Beginn des
    →Indexjahres", excluding that year's premiums, *Zuzahlungen* and the daily surplus on them. The
    *Wahlrecht*, Ziffer 3.1: parameters notified at least **3 weeks** before the *Indexstichtag*, the
    election due at latest **7 days** before, splits in 25-percent steps across indices and the
    *sichere Verzinsung*; Ziffer 3.2 sets the default on silence, which rolls the previous split over
    only if index participation was at least 50 % and otherwise moves the contract **to** 50 %. The
    *Cap-Festlegung*, Absatz 2 b): set annually "auf der Grundlage von Angeboten mehrerer
    Finanzinstitute", on the surplus, the *Bewertungsreserven* *Sockelbetrag* and "Faktoren des
    Kapitalmarkts wie der Volatilität und der Dividendenrendite des jeweiligen Index" — and **there
    is no *Mindest-Cap* clause**. Ziffer 3.5 excludes the participation for a year in which the
    *Policenwert* does not exceed the *Deckungsrückstellung* required for the guarantee. Ziffer 3.7
    is the *Ersatzindex* clause, with **no *Treuhänder*** and no *Sonderkündigungsrecht*. Gaps 1
    and 2 close for this carrier.
  - **One structural finding for the model.** Allianz applies a monthly Cap **and** a
    *Partizipationssatz* to the capped sum: "Die →Indexpartizipation ermitteln wir, indem wir die
    maßgebliche Jahresrendite … mit dem →Partizipationssatz … multiplizieren." delib's `cap` payoff
    form has no participation factor and its `quote` form has no cap, so this tariff is not directly
    representable; recorded in `model.md`, not acted on.
  - **A worked *Indexjahr* pair is published on the product page** at an exemplary Cap of 3,2 % and
    *Partizipationssatz* of 75,00 %: 2020/2021 sums to **15,90 %** and credits **11,92 %** against a
    point-to-point index gain of 43,69 %; 2021/2022 sums to **−26,96 %** and credits **0 %**. That is
    gap 4's evidence, from the insurer.

### S3 — Allianz Lebensversicherungs-AG, *Produktinformationsblatt* / IPID for **Allianz IndexSelect**
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: *Produktinformationsblatt* (the German pre-contractual product summary required by
  VVG-InfoV, in the market also labelled with the EU IDD term **IPID**)
- URL: not established, and **no such document exists to establish**.
- Retrieved: **no — the document class does not exist for this product.** VVG-InfoV § 4 creates an
  *Informationsblatt zu Versicherungsprodukten* (the IPID of Durchführungsverordnung (EU) 2017/1469),
  and § 4 Abs. 3 excludes it: "Diese Regelung gilt nicht für **Versicherungsanlageprodukte** im Sinne
  der Verordnung (EU) Nr. 1286/2014" (canonical XML, Stand: zuletzt geändert durch Art. 13 G v.
  26.5.2026; read 2026-08-30). An Indexpolice is a *Versicherungsanlageprodukt*, so it gets a
  *Basisinformationsblatt* [S4] and not an IPID. The standardised, published *Produktinformationsblatt*
  exists only under the AltZertG — that is [S11], and it was retrieved.
- Content: the entry is kept at its frozen number as the record of a mis-specified source. The
  commercial envelope it was cited for is partly supplied elsewhere: [S4] carries Allianz's model
  case and its 12/20/30/40-year term and 80 %/90 % *Garantieniveau* menus, and [S11] a competitor's
  full envelope including a guaranteed *Rentenfaktor*. What is still unpublished for Allianz is the
  *Eintrittsalter* band and the minimum *Beitrag*. Gap 5, narrowed.

### S4 — Allianz Lebensversicherungs-AG, *Basisinformationsblatt* (PRIIP-KID) for **Allianz IndexSelect**
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: *Basisinformationsblatt* under Regulation (EU) No 1286/2014 [R10] — three pages, fixed
  structure, with four performance scenarios and the full cost table including the *Reduktion der
  Wertentwicklung* (reduction in yield)
- URL: `https://goa-eportale.allianz.de/dlc_app/Intranet/dlc?nr=JLRIP9030Z0&m=d` (30 years), with
  `…JLRIP9020Z0…` (20 years) and `…JLRIU8030Z0…` (*IndexSelect Plus*) beside it, indexed at
  `https://www.allianz.de/service/dokumente/basisinformation-bib-zukunftsvorsorge/`.
- Retrieved: **yes** — PDF, *Datum der Erstellung des Basisinformationsblatts: 01.11.2025*, three
  editions compared, read 2026-08-30.
- Content: the **only public document class that puts a number on the cost of a German Indexpolice**
  and on its modelled return distribution — and it is now read. Product line "Allianz Zukunftsrente
  IndexSelect (mind. 90 % Garantie)"; **risk indicator 1 of 7** at 30 years (2 at 20 years, 2 for
  *IndexSelect Plus* at 80 % Garantie). Model case: 37-year-old, 30 × 1.000 EUR. **Performance
  scenarios at 30 years**: stress 27.830 EUR (−0,5 % a year), pessimistic 31.730 EUR (+0,4 %),
  moderate 42.160 EUR (**+2,1 %**), optimistic 66.880 EUR (+4,8 %); death 42.160 EUR. **Costs**:
  *Einstiegskosten* "2,5% der kumulierten Anlagen" plus 1,5 % of the annual payment from year 6;
  *Verwaltungsgebühren* 3,5 % of the payment a year plus 1,0 % of value a year; *Transaktionskosten*
  0,1 %; **1,6 % a year** in total at 30 years, turning 3,7 % before costs into 2,1 % after. It also
  confirms the capital is in the *Sicherungsvermögen*, that the surplus finances the participation,
  and that surrender pays the *Rückkaufswert* "abzüglich eines Stornoabzugs". The Category 4
  classification is sourced separately at [R11]. **Gap 6 closes for one carrier**: delib's 2,5 %
  acquisition charge is Allianz's own figure; `β` and `γ` remain `[std]` with a published comparator.

### S5 — Allianz Lebensversicherungs-AG, annual customer notification of the *Indexbeteiligung* parameters for the coming *Indexjahr*
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: annual policyholder letter / online customer-portal notice announcing, before the start
  of each *Indexjahr*, the **Cap** (or the *Partizipationsquote*) that will apply and inviting the
  *Wahlrecht* election
- URL: not established — no instance is published.
- Retrieved: **no instance** — the notice is sent to policyholders, and none was reachable on
  2026-08-30. **Its content and timing are, however, now settled from the AVB that mandates it**
  [S2] Ziffer 3.1: indices, *Caps*, *Partizipationssatz*, the year's surplus net of
  *Verwaltungskosten* and the *Bewertungsreserven* *Sockelbetrag*, at latest 3 weeks before the
  *Indexstichtag*.
- Content: the document class in which the **actual Cap level for a named insurer and a named year**
  lives. **Cap and quota levels turned out to be reachable by two other routes**: Allianz publishes a
  worked illustration at a Cap of **3,2 %** with a *Partizipationssatz* of **75,00 %**, expressly
  "exemplarisch gewählt" [S2], and Stuttgarter **publishes** its current *Partizipationsquote* —
  70 %, or 120 % / 172 % with the *Index-Turbo* options — for all *Indexstichtage* from 1.2.2026 to
  31.1.2027 [S8]. What is still missing is a market **panel** [R21]. Gap 3, much reduced.

### S6 — Allianz Lebensversicherungs-AG, **Allianz Perspektive** documents (the *Neue Klassik* comparator)
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: AVB, *Produktinformationsblatt* and *Basisinformationsblatt* for a *Neue Klassik*
  deferred annuity **without** index participation
- URL: `https://goa-eportale.allianz.de/JLR/SK1/JLRSK1-30Z0.pdf.download.pdf`, indexed with the
  12/20/40-year editions at `https://www.allianz.de/service/dokumente/basisinformation-bib-zukunftsvorsorge/`.
- Retrieved: **yes, for the *Basisinformationsblatt*** — PDF, 3 pp., *Datum der Erstellung des
  Basisinformationsblatts: 01.11.2025*, read 2026-08-30. The AVB was not separately retrieved. The
  product name **Allianz Zukunftsrente Perspektive** is confirmed and the tag comes off. The KID
  states the guarantee in the *Neue Klassik* form — "Sie haben Anspruch darauf, mindestens 90 % Ihres
  Kapitals zurückzuerhalten … Dieser Schutz vor künftigen Marktentwicklungen gilt jedoch **nicht,
  wenn Sie vor dem vereinbarten Rentenbeginn einlösen**" — and makes the comparison quantitative:
  on the same model case and cost structure, Perspektive's moderate scenario is 40.900 EUR (1,9 % a
  year) against IndexSelect's 42.160 EUR (2,1 %) [S4], both in risk class 1.
- Content: **Perspektive** is the reference point for what *Neue Klassik* means
  without the index module — a guarantee falling due at *Rentenbeginn* rather than accruing as an
  annual guaranteed rate on the reserve, permitting a riskier asset mix behind it. The Indexpolice is
  the same guarantee architecture with the surplus spent on an option instead of credited. The
  product specification must draw exactly that distinction rather than blur the two.

### S7 — R+V Lebensversicherung AG, AVB and product documents for **R+V-IndexInvest**
- Publisher: R+V Lebensversicherung AG, Wiesbaden
- Doc type: AVB / *Bedingungswerk*, *Produktinformationsblatt* and *Basisinformationsblatt* for a
  deferred annuity with *Indexbeteiligung*
- URL: `https://www.ruv.de/dam/jcr:038d2022-558e-46d7-b161-e37647ff9a2d/PLG0426.2026-04-30-12-59-13.pdf`,
  linked from `https://www.ruv.de/altersvorsorge/private-rentenversicherung/privat-rente-indexinvest`.
- Retrieved: **yes** — *Allgemeine Versicherungsbedingungen für die R+V-IndexInvest-Rentenversicherung*
  (**IL55**), Stand 01.07.2025, pages 61–81 of the 603-page *Bedingungsheft* `PLG0426`, read in full
  2026-08-30. The name **R+V-PrivatRente IndexInvest** is confirmed and the tag comes off.
- Content — **the second carrier wording, and it is not the first one.** § 3 Ziffer 2: the
  participation is "die Bezugsgröße … mit der **jährlichen Wertentwicklung** des Index und mit der
  jährlich festgelegten **Beteiligungsquote** multipliziert", the year's movement being "die
  prozentuale Veränderung des Index innerhalb eines Versicherungsjahres" with the *Bewertungsstichtag*
  the last Frankfurt trading day (§ 3 Ziffer 3) — **a quota on the point-to-point year return, with
  no monthly cap anywhere in the tariff**. The underlying is a house index, the *Solactive Multi
  Anlage Stabil Index* (**SOMAS**). The *Bezugsgröße* is the *Policenwert* present for the whole
  *Versicherungsjahr*, excluding that year's premiums; the election runs to **7 days** before the
  *Versicherungsjahrestag* with index participation the default (§ 2); the *Turbo* stakes 2 % of the
  *Policenwert* and can be wholly lost (§ 3 Ziffer 8); the participation is excluded for a year in
  which the *Policenwert* does not exceed the guarantee's *Deckungsrückstellung* (§ 2 Ziffer 1); and
  the *Ersatzindex* clause (§ 3 Ziffer 11) has **no *Treuhänder***, with a separate suspension clause
  (§ 3 Ziffer 10) where no suitable instrument can be bought. § 1 gives a 90 % *Garantiekapital* at
  *Rentenbeginn*, a death benefit of the *Policenwert* subject to the same 90 % floor, the max-of-two
  *Rentenfaktor* rule, and the factor's bases — a *Rechnungszins* of 0,1 % p. a. and a company table
  derived from DAV 2004 R. **Gap 2 closes**: statements of the form "the market does X" are now
  possible, and the first of them is that the market does **not** do one thing.

### S8 — Stuttgarter Lebensversicherung a. G., AVB and product documents for **Stuttgarter index-safe**
- Publisher: Stuttgarter Lebensversicherung a. G.
- Doc type: AVB / *Bedingungswerk*, *Produktinformationsblatt* and *Basisinformationsblatt* for a
  deferred annuity with *Indexbeteiligung*
- URL:
  `https://daten.vermittler-stuttgarter.de/Downloadcenter/Stuttgarter/01_Leben/16_Tarifuebergreifend/02_indexsafe/12_3_001_PS_index-safe.pdf`
  (*Produkt-Steckbrief*, `12.3.001 – Stand 1/2025`) and `https://www.stuttgarter.de/service/index`
  (current parameters, Stand 04. August 2026).
- Retrieved: **yes for those two**, read 2026-08-30; **no for the AVB**, which Die Stuttgarter does
  not publish — the *Downloadcenter* directory answers HTTP 403 and no *Bedingungen* PDF is linked
  from either the customer or the intermediary site. The name **index-safe** is confirmed.
- Content: Die Stuttgarter is a mid-sized carrier with a long-standing index family. The house-index
  observation is **confirmed and the indices are named**: the *Stuttgarter M-A-X Multi-Asset Index*
  and the *Stuttgarter Grüne Zukunft Index*, the M-A-X described as investing "in mehreren
  Anlageklassen, um eine kontinuierliche Wertentwicklung zu erzielen". The design is a quota on the
  year, like [S7] and unlike [S2]. **The current parameters are published**, which no other carrier
  in this file does: *Partizipationsquote* **70 %**, *Index-Turbo* 120 %, *Index-Turbo Plus* 172 %,
  and a *sichere Verzinsung* of **2,16 %**, all "für alle Indexstichtage vom 1.2.2026 bis 31.1.2027"
  — so the *Indexjahr* is a common calendar window rather than the policy year. **No volatility
  target and no index-level fee is published for either house index**, so the argument at section 9
  that a low-volatility bespoke index buys a higher quota out of a smaller budget is unsupported at
  the level of a number, and the one published house-index quota (70 %) is below the equity
  illustration at [S2] (75 %).

### S9 — Zurich Deutscher Herold Lebensversicherung AG, *Verbraucherinformation* series for konventionelle Rentenversicherungen
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation* — a long combined document (AVB plus the VVG-InfoV § 1
  pre-contractual information) covering a family of conventional annuity tariffs
- URL: not established.
- URL:
  `https://www.zurich.de/-/media-assets/project/zurich-headless/germany/br/documents/verbraucherinformationen/32020_aufgeschobene-rentenversicherung_verbraucherinformationen_2026_01.pdf`
- Retrieved: **yes** — PDF, 66 pp., *Verbraucherinformation für Konventionelle Versicherungen —
  Aufgeschobene Rentenversicherung – Private Vorsorge (Schicht 3) und Rückdeckungsversicherung
  (Schicht 2)*, in der Fassung 01 / 2026, document `521331262 2601`, read 2026-08-30.
- Content: the chassis, **and one correction that matters**. The open question is answered
  negatively: the 2026 edition contains **no index variant** — the string "Index" does not occur in
  it once. And the death-benefit claim this file attached to the series is **wrong**. § 1 Abs. 2:
  "Ist keine der folgenden Erweiterungsmöglichkeiten des Versicherungsgrundschutzes eingeschlossen,
  so **erlischt im Falle des Todes der versicherten Person die Versicherung, ohne dass eine Leistung
  fällig wird**"; where cover is agreed the standard form is *Beitragsrückgewähr*, returning
  **premiums** (§ 1 Abs. 3), not the accumulated capital. The return-of-capital shape delib models is
  [S7]'s, not this series'. The consequences drawn from it — a small *Risikoüberschuss*, light
  underwriting, § 161 VVG close to inoperative — survive on the [S7] wording; the citation does not.

### S10 — GDV, *Muster-Standmitteilung* for a *Rentenversicherung*, and carriers' own *Standmitteilungen*
- Publisher: GDV (model), individual carriers (actual)
- Doc type: annual statement of contract status
- URL:
  `https://www.gdv.de/resource/blob/6306/999e4633ea996ddc885f1153ca6312fa/6v1-gdv-muster-standmitteilung-private-rentenversicherung-klassik1-02-2017-data.pdf`
- Retrieved: **yes for the GDV model** — PDF, 9 pp., "Rentenversicherung (klassisch 1)", version
  22 March 2018, read 2026-08-30; **no for any carrier instance**, none being published.
- Content: where an *Indexjahr* result is reported to the policyholder. The retrieved model settles
  what the standardised layout does **not** contain: *Garantiertes Kapital* opening and closing,
  premiums, *Erträge*, acquisition and administration costs for the year, *Schlussüberschuss*, the
  *Bewertungsreserven* share, *Gesamtkapital*, and a three-column *Überschussbeteiligung* sensitivity
  — **no cap row, no *Indexrendite* row, no locked-in-credit row**, and none of the nine GDV
  *Muster-Standmitteilungen* is an index variant [S1]. **Gap 4's evidence came from elsewhere**:
  Allianz publishes two worked *Indexjahre* with their twelve monthly movements, the capped series
  and the resulting participation [S2]. No real contract's *Standmitteilung* was obtained, so the
  constructed examples in sections 19 and 20 stay `[std]`.

### S11 — *Produktinformationsblatt* under the AltZertG, with the *Chancen-Risiko-Klasse*, for a *Basisrente* or *Riester* index variant
- Publisher: the certifying carrier; the class assignment by the *Produktinformationsstelle
  Altersvorsorge gGmbH* (PIA)
- Doc type: the standardised *Produktinformationsblatt* prescribed for certified *Altersvorsorge*
  products, carrying the product's **Chancen-Risiko-Klasse** on a scale of 1 to 5 [R12]
- URL:
  `https://nextcloud.stuttgarter.de/s/iAR6cfRLwJBSGse/download?path=%2F01_Leben%2F18_Muster_PIB%2F01_BasisRente%2F01_indexsafe&files=Muster_Produktinformationsblatt_Basisrente_index_safe_69_mitTurboPlus_LZ30.pdf`,
  indexed at `https://www.stuttgarter.de/muster-produktinformationsblaetter`.
- Retrieved: **yes** — PDF, 2 pp., *Muster-Produktinformationsblatt* "BasisRente index-safe"
  (Stuttgarter Lebensversicherung a. G., Tarif 69 mit Turbo Plus, 30-year term), Stand 01.01.2026,
  form `V69-202606`, *Zertifizierungsnummer* 006604, read 2026-08-30.
- Content: the German market's one standardised, mandatory, comparable product disclosure, **for an
  index variant, and it settles both things this entry was cited for**. The **Chancen-Risiko-Klasse
  is 4** — "renditeorientierte Anlage mit höheren Ertragschancen" — which **contradicts the guess
  above** that index products sit low on the scale; that tag comes off with the guess. The
  ***Effektivkosten* are 1,80 Prozentpunkte**, turning an illustrative 5,00 % into 3,20 %. The full
  envelope: 100,00 EUR a month for 30 years from age 37 to 67, 36.000 EUR paid in, *Garantiertes
  Kapital für Verrentung* 30.600,00 EUR (**85 %**), garantierte monatliche Altersleistung 92,57 EUR,
  and a **guaranteed *Rentenfaktor* of 25,74 EUR per 10.000 EUR** — against delib's `[std]` 25,00.
  Itemised charges: *Abschluss- und Vertriebskosten* **2,50 % der vereinbarten Beiträge** (900,00
  EUR), *Verwaltungskosten* 9,00 % of premiums plus 0,04 % of capital monthly, and 1,50 % of each
  payment in the *Auszahlungsphase*. Gap 7 closes.

### S12 — Finanztip, guidance pages on *Indexpolicen* / index-linked annuities
- Publisher: Finanztip Verbraucherinformation gGmbH — **secondary**, not a product document
- Doc type: consumer guidance page
- URL: `https://www.finanztip.de/presse/pm-finanztip-indexpolicen/` — press release "Indexpolicen
  lohnen sich nicht", Berlin, 21 October 2016. Finanztip's current guidance pages on the topic return
  HTTP 404, so this ten-year-old release is the reachable Finanztip statement.
- Retrieved: **yes** — HTML, dated 21 October 2016, read 2026-08-30.
- Content: the standing consumer argument, now quotable. Returns "von mehr als 4 Prozent sind aber
  nur schwer zu erreichen", with "nach Abzug aller Kosten Werte von 0,5 bis 2,5 Prozent" more likely;
  "Verbraucher können oft nicht wirklich nachvollziehen, was sie da eigentlich kaufen". It
  independently confirms that **both payoff designs exist in the market** — "Bei manchen Optionen sind
  die Gewinnmöglichkeiten durch einen sogenannten **Cap** gedeckelt. Bei anderen Optionen wird ein
  festgelegter Prozentsatz ausgeschüttet – die sogenannte **Quote**" — and supplies a segment count
  [R19] does not: 400.000 Allianz contracts in October 2016. The criticisms stay **arguments** in
  mechanics section 21; the 0,5–2,5 % figure is a 2016 consumer-body estimate and is not a model
  input.

### S13 — Stiftung Warentest / *Finanztest*, comparative tests of *Indexpolicen*
- Publisher: Stiftung Warentest — **secondary**
- Doc type: comparative product test with scoring and a cost analysis
- URL: not established. `test.de/Indexpolicen-im-Test/` returns HTTP 404 and the *Finanztest* tests
  of this class are behind the paywall; only trade-press reports of them are reachable [S16].
- Retrieved: **no** — paywalled at the publisher, and no landing page for the test was located on
  2026-08-30. Kept as a known reference.
- Content: a comparative test of this class would supply cap levels, cost quotas and modelled
  outcomes for a named panel of carriers in a named year — precisely the evidence gaps 3 and 6
  record, and **the one class of document this pass could not reach**. **Nothing cited**, including
  the average-return figures the trade press attributes to it.

### S14 — Verbraucherzentrale (federal association and Länder consumer centres), pages on *Indexpolicen*
- Publisher: Verbraucherzentrale Bundesverband e. V. and the Länder centres — **secondary**
- Doc type: consumer-advice pages
- URL: `https://www.vzhh.de/presse/gericht-stoppt-etikettenschwindel-bei-allianz-index-select-rente`
  — Verbraucherzentrale **Hamburg**, press release of 4 April 2018. No vzbv or Länder-centre page on
  *Indexpolicen* was located.
- Retrieved: **yes** — HTML, dated 4 April 2018, read 2026-08-30.
- Content: the sector's standing criticisms, attributable to a named body in its own words, **and
  litigation that was actually brought**. The vzhh sued Allianz under the UWG over the IndexSelect web
  advertising and won at first instance — LG München I, Urteil vom **23. März 2018, Az. 37 O
  12326/17**, recorded as *nicht rechtskräftig* — the court finding that "Beteiligung an der
  Wertentwicklung des EUROSTOXX 50" and "Indexpartizipation" mislead because "eine Korrelation des
  Renditeversprechens (…) mit der Wertentwicklung des Aktienindexes nur sehr eingeschränkt besteht".
  The release states this file's own characterisation from the other side — the participation runs
  "nicht über die eingezahlten Beiträge, sondern ausschließlich über die … jährlich zu ermittelnde
  Überschussbeteiligung" — and the monthly-measurement point exactly: the annual outcome can fall
  short of the index "selbst dann …, wenn der Cap in der Jahresbetrachtung gar nicht überschritten
  wird", which is section 20's Example B argued by a consumer body. **The judgment did not stand**:
  the OLG München dismissed the claim on 4 April 2019, no *Revision* admitted [S16]. Recorded as
  **positions** with their outcome in section 21, not as findings.

### S15 — Comparison portals: Verivox, Check24
- Publisher: Verivox GmbH; CHECK24 Vergleichsportal GmbH — **secondary**
- Doc type: product-comparison and explainer pages
- URL: not established. `verivox.de/altersvorsorge/themen/indexpolice/` answers **HTTP 403** to a
  plain request, and no Check24 page on this product class was located on 2026-08-30.
- Retrieved: **no** — bot-blocked at the publisher. Kept as a known reference.
- Content: the usual public fallback for the commercial envelope when carrier disclosures are not
  reachable. **The fallback was not needed**: [S11] supplies a complete published envelope for one
  carrier and [S4] the model case and term menu for another. The envelope parameters in section 22
  stay `[std]` because they are delib's own construction, not because nothing could be found.

### S16 — German insurance trade press: *procontra*, *Versicherungsbote*, *Versicherungsjournal*, *Cash.Online*, *Versicherungswirtschaft*, *Handelsblatt*
- Publisher: various — **secondary**
- Doc type: trade and financial press reporting
- URL: `https://www.allianz.de/presse/mitteilungen/olg-weist-klage-zu-allianz-indexselect-ab/` —
  what was reachable is not the trade press but the **carrier's own release**, "OLG weist Klage zu
  Allianz IndexSelect ab", 9 May 2019. `versicherungsbote.de` answers **HTTP 403** to every article on
  this product, and *procontra* and *Cash.Online* carry nothing on index tariffs in the swept set.
- Retrieved: **yes for the Allianz release**, read 2026-08-30; **no** for *Versicherungsbote*,
  *procontra*, *Versicherungsjournal*, *Cash.Online*, *Versicherungswirtschaft* and *Handelsblatt*,
  which stay known references.
- Content: the outcome of the [S14] litigation, from the winning party — "Das Oberlandesgericht (OLG)
  München hat bereits am 4. April [2019] eine Klage der Verbraucherzentrale Hamburg … abgewiesen.
  Eine Revision wurde nicht zugelassen." It also dates the product ("seit über elf Jahren", so a
  2007/2008 launch) and puts the in-force count at "über 500.000 Kunden", the only segment-size
  figure available to this file at all [R19]. **The record of where cap changes and index switches
  are reported stays a gap**: no trade-press account of one was retrieved, and every cap figure in
  this file comes from a carrier document.

---

## Regulatory and actuarial references

**The statutory references were read on 2026-08-30, and the tags below are adjudicated one by one.**
Where a URL is given it is the address on `gesetze-im-internet.de` and is the **human-facing link,
not the evidence**: the per-section pages `…/<law>/__NNN.html` answer HTTP 200 with a four-to-seven
kilobyte frameset carrying **no statutory text**, so a 200 on one of them is not retrieval. The text
was read from the **canonical XML** each law publishes at `…/<law>/xml.zip`, which carries the law's
`Stand`; each entry below records the `Stand` it was read at, and the section numbering is confirmed
against it. Statutory content is still described in this author's own words except where a short
exact quotation earns its place, in which case it is copied character for character. Sixteen of the
twenty-two entries are now retrieved; the six that are not say why.

### R1 — VVG § 153, *Überschussbeteiligung*
- Publisher: Bundesministerium der Justiz / juris (Gesetze im Internet)
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` (frameset, 4,9 kB, no text)
- Retrieved: **yes** — canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156,
  read 2026-08-30.
- Content: the statutory hinge of this product. § 153 Abs. 1 gives the policyholder an entitlement
  to participate in the surplus and in the *Bewertungsreserven* unless participation is excluded by
  agreement. Abs. 2 requires the insurer to allocate the surplus by a **verursachungsorientiertes
  Verfahren** — a causation-oriented procedure — or by another comparable appropriate method agreed
  in the contract. Abs. 3 governs the *Bewertungsreserven*: they are determined annually, allocated
  by a causation-oriented procedure, and half of the amount so determined is paid out on
  termination, subject to a proviso for supervisory rules introduced by the LVRG. **One correction
  the retrieved text forces**: Abs. 4 reads "Bei Rentenversicherungen ist die **Beendigung der
  Ansparphase** der nach Absatz 3 Satz 2 maßgebliche Zeitpunkt" — for a *Rentenversicherung* the
  half-share falls due at *Rentenbeginn*, not at the end of the contract. Abs. 1 also limits the
  exclusion: "die Überschussbeteiligung kann nur insgesamt ausgeschlossen werden".
- Why it matters here, and it matters more than for any other delib product: **the index
  participation is a form of *Überschussverwendung*, not a separate investment.** What the
  policyholder is legally entitled to is a share of the insurer's surplus; the AVB then say how that
  share is applied, and this product's AVB say it is applied by buying a bounded index-linked payoff
  for one year. The *Wahlrecht* is therefore an *Überschussverwendungswahlrecht*, and the
  *Indexbeteiligung* has no independent statutory footing — it stands or falls on the contract
  clause. **This is the correct legal characterisation of the product and it is not in doubt** — and
  all three carrier documents now state it in their own words ([S2] Ziffer 3.3, [S7] § 3 Ziffer 9,
  [S11]). The subsection numbering is confirmed and the tag comes off. Both AVB add a component this
  file did not carry: the budget is the declared surplus **plus** the year's minimum share of the
  *Bewertungsreserven*, and at Allianz net of *Verwaltungskosten*.
- A consequence a model must respect: because the *Überschuss* is discretionary and may be zero
  [R8][R16], the **option budget may be zero**, in which case the *Indexbeteiligung* for that year
  buys nothing and the year's credit is necessarily zero regardless of what the index does. Both AVB
  say so — "Im ungünstigsten Fall kann die Überschussbeteiligung Ihres Vertrags der Höhe nach null
  sein" [S2] Ziffer 2.1; "Diese können auch Null sein" [S7] § 13 Ziffer 1 — and both go further,
  **switching the participation off entirely** for a year in which the *Policenwert* does not exceed
  the *Deckungsrückstellung* required for the guarantee ([S2] Ziffer 3.5, [S7] § 2 Ziffer 1).

### R2 — VVG § 169, *Rückkaufswert*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` (frameset, 7,0 kB, no text)
- Retrieved: **yes** — canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr.
  156, read 2026-08-30. Abs. 3 confirms the five-year spread verbatim; Abs. 5 the "vereinbart,
  beziffert und angemessen" test; Abs. 7 that already-allocated *Überschussanteile* are paid on
  top, which is what puts locked-in credits inside the surrender value as a matter of statute.
  Abs. 4 puts the *Zeitwert* rule on the § 124 Abs. 2 Satz 2 VAG class and **not** on this
  product, which is half the not-unit-linked argument [R15]. Tag off.
- Content: on termination by *Kündigung* the insurer owes the *Rückkaufswert*, computed as the
  *Zeitwert* / the actuarial reserve on recognised actuarial principles; acquisition and
  distribution costs must be spread over **at least the first five years** so that an early
  surrender value cannot be extinguished by front-loaded costs (the *Mindestrückkaufswert*); a
  *Stornoabzug* is permitted only if it is agreed, appropriate and **quantified in the contract**.
- Delta: the *Rückkaufswert* of an Indexpolice is a **general-account reserve**, not a unit value.
  It includes index credits already locked in, because those have become guaranteed capital, and it
  does **not** include an accrued fraction of the running *Indexjahr*, whose payoff is determined
  only at the year end. Whether the contract instead refunds the unspent option budget **is not
  established**. Gap 12.

### R3 — VVG § 165, *Prämienfreie Versicherung*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` (frameset, 4,5 kB, no text)
- Retrieved: **yes** — canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr.
  156, read 2026-08-30. Two things the text adds: the right is conditional on reaching "die dafür
  vereinbarte **Mindestversicherungsleistung**" (Abs. 1), which [S7] § 11 Ziffer 9 sets at a
  *Policenwert* of 2.500 EUR, and the paid-up benefit must be stated in the contract for every
  *Versicherungsjahr* (Abs. 2). Abs. 3 Satz 2 — "Die Ansprüche des Versicherungsnehmers aus der
  **Überschussbeteiligung bleiben unberührt**" — is why a paid-up Indexpolice keeps its
  participation, which this file previously inferred. Tag off.
- Content: the policyholder may at any time demand conversion of the contract to a paid-up
  (*prämienfrei*) contract for the reduced insured benefit computed on recognised actuarial
  principles for the end of the current insurance period; the same *Stornoabzug* discipline applies.
- Delta: a paid-up Indexpolice **keeps its index participation** on the capital already accumulated
  and the *Wahlrecht* survives, because the participation attaches to the capital and not to the
  premium — **and § 165 Abs. 3 Satz 2 says so directly**: "Die Ansprüche des Versicherungsnehmers aus
  der Überschussbeteiligung bleiben unberührt." Since the index participation *is* a form of
  *Überschussverwendung* [R1], the tag comes off. Two conditions the retrieved text adds: the right
  is contingent on reaching "die dafür vereinbarte **Mindestversicherungsleistung**" (Abs. 1),
  failing which the *Rückkaufswert* is paid instead — [S7] § 11 Ziffer 9 sets that at a *Policenwert*
  of 2.500 EUR — and the paid-up benefit must be stated in the contract for every *Versicherungsjahr*
  (Abs. 2).

### R4 — VVG § 163 (*Anpassung der Prämie*) and § 164 (*Ersetzung von Bedingungen*)
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html`, `.../__164.html` (both framesets, no text)
- Retrieved: **yes** — canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr.
  156, read 2026-08-30. **Three corrections.** The marginal headings are *Prämien- und
  Leistungsänderung* and *Bedingungsanpassung*, not *Anpassung der Prämie* and *Ersetzung von
  Bedingungen*. The § 163 trigger is that "sich der **Leistungsbedarf** nicht nur vorübergehend
  und nicht voraussehbar gegenüber den Rechnungsgrundlagen der vereinbarten Prämie geändert hat",
  not that the calculation bases have changed; Abs. 2 gives the **policyholder** the right to a
  reduced benefit instead of a higher premium. And § 164 is **not** "on the same footing": it
  requires the clause to have been declared ineffective "durch höchstrichterliche Entscheidung
  oder durch bestandskräftigen Verwaltungsakt" and involves **no *Treuhänder* at all**. Tag off.
- Content: § 163 permits an adjustment of the premium, or of the benefit at unchanged premium, for
  life contracts where the calculation bases have changed in a way that is not merely temporary and
  the change was unforeseeable, **with the confirmation of an independent trustee** (*unabhängiger
  Treuhänder*). § 164 permits an ineffective clause to be replaced by a new one, again with the
  trustee's confirmation, where the gap would otherwise not be closable.
- Why it matters here: these are the two statutory channels through which an Indexpolice's terms can
  be changed against the policyholder's will after issue. **The annual redetermination of the Cap is
  not one of them** — the Cap is not an adjustment of the contract but the exercise of a discretion
  the contract confers, governed by § 315 BGB [R22], not § 163 VVG. Keeping the two apart is the most
  important legal distinction in this product and downstream documents must not blur it. The
  *Treuhänder* does appear elsewhere here — **but not where this entry guessed.** Both retrieved
  *Ersatzindex* clauses operate **without any trustee** ([S2] Ziffer 3.7, [S7] § 3 Ziffer 11), so the
  guess is contradicted and the tag goes with it. Where a *Treuhänder* does appear in a retrieved AVB
  is on the ***Rentenfaktor***: Allianz must, where no comparable annuity is on sale at
  *Rentenbeginn*, set the factor on recognised actuarial principles and bring in "einen unabhängigen
  Treuhänder, der den Rentenfaktor zu prüfen und dessen Angemessenheit zu bestätigen hat" [S2]
  Ziffer 1 — the historic *Treuhänderklausel* inherited from product 2, confirmed.

### R5 — VVG § 154 (*Modellrechnung*) and VVG-InfoV § 2 (pre-contractual information)
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__154.html` (frameset, no text);
  `https://www.gesetze-im-internet.de/vvg-infov/__2.html` (this one **does** return the full text,
  10,2 kB)
- Retrieved: **yes for both** — VVG § 154 from canonical XML, Stand: zuletzt geändert durch Art. 12 G
  v. 26.5.2026 I Nr. 156; VVG-InfoV § 2 read from the section page and re-read from canonical XML,
  Stand: zuletzt geändert durch Art. 13 G v. 26.5.2026 I Nr. 156; both 2026-08-30. VVG-InfoV § 2
  Abs. 3 fixes the three rates as the *Höchstrechnungszinssatz* × **1,67**, that rate **plus** one
  point and that rate **minus** one point — 1,67 % / 2,67 % / 0,67 % at 1,00 %. Abs. 1 Nr. 9 defines
  the *Effektivkosten* as "die Minderung der Wertentwicklung durch Kosten in Prozentpunkten … bis zum
  Beginn der Auszahlungsphase", and Abs. 6 computes them like the *Gesamtkostenindikator* of Anhang VI
  of Delegated Regulation (EU) 2017/653, with AltZertG products carved out. § 154 Abs. 1 Satz 2
  exempts only the § 124 Abs. 2 Satz 2 VAG class, so **the duty does apply to an Indexpolice** — one
  more consequence of the classification at [R15]. Tags off.
- Content: § 154 requires, where the insurer quotes possible benefits beyond the contractually
  agreed ones, a *Modellrechnung* on three prescribed interest assumptions, with a warning that it
  is only a model and that the values are not guaranteed. VVG-InfoV § 2 sets out the catalogue of
  pre-contractual information the insurer must supply, which for life insurance includes the
  benefits and their guarantee status, the surrender and paid-up values, the costs, and — the item
  that matters most for cost transparency — the ***Effektivkosten*** (reduction in yield).
- Why it matters here: a *Modellrechnung* for an Indexpolice is intrinsically awkward, because the
  interest assumption drives the **option budget**, which drives the **Cap**, which drives the payoff
  non-linearly. How carriers discharge § 154 for this product **is still not established**: neither
  retrieved AVB reproduces one, and the *Versicherungsinformationen* document that would carry it is
  contract-specific and unpublished [S2] [S3]. Gap 13 stands.

### R6 — VVG § 161, *Selbsttötung*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` (frameset, 4,1 kB, no text)
- Retrieved: **yes** — canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr.
  156, read 2026-08-30. The text matches this entry exactly: three years from conclusion, the
  *freie Willensbestimmung* exception (Abs. 1), extension by individual agreement (Abs. 2), and
  the *Rückkaufswert* including *Überschussanteile* under § 169 owed where the exclusion bites
  (Abs. 3). Tag off.
- Content: where death is caused by suicide, the insurer is not liable on a death cover within
  **three years** of the conclusion (or reinstatement) of the contract; where the exclusion applies,
  the insurer owes the *Rückkaufswert*.
- Relevance: inherited unchanged from products 1 and 2, and close to inoperative in economic terms,
  because the *Aufschubphase* death benefit is normally a return of capital rather than a sum at
  risk. Recorded so the delib documents can say so rather than leave it out.

### R7 — *Deckungsrückstellungsverordnung* (DeckRV): *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` (contents page)
- Retrieved: **yes** — canonical XML, §§ 2 and 4, Stand: zuletzt geändert durch Art. 1 V v.
  19.7.2024 I Nr. 250, read 2026-08-30. § 2 (marginal heading ***Höchstzinssatz***, not
  *Höchstrechnungszins*) Abs. 1 sets it "auf **1 Prozent**"; Abs. 2 is the statutory reason the
  cohorts exist — the rate used at conclusion "gilt … für die gesamte Laufzeit des Vertrages". § 4
  Abs. 1: "Der Zillmersatz darf **25 Promille der Summe aller Prämien** nicht überschreiten." Tags
  off for both. **The rate history is only half-confirmed**: the XML carries the current *Stand*
  only, and the DAV's November 2025 statement supplies 0,25 % for 2022–2024 and the 2025 rise to
  1,0 % [R18]; the **0,90 % for 2017–2021 stays `[unverified]`**.
- Content: the DeckRV caps the technical interest rate used in the *Deckungsrückstellung*, and hence
  in practice the rate a new contract's guarantee may be priced on, and caps the acquisition costs
  that may be zillmerised into the reserve (the *Höchstzillmersatz*, **25 ‰ of the *Beitragssumme***
  `[unverified]`).
- The rate history, **entirely `[unverified]` at the level of individual steps**, as this author
  recalls it: 4,00 % to mid-2000; 3,25 %; 2,75 %; 2,25 %; 1,75 %; 1,25 %; 0,90 %; **0,25 % for
  2022–2024**; **1,00 % from 1 January 2025**. The sibling delib research files establish the
  0,25 % → 1,00 % move and the 1,00 % level for 2025 and 2026 from search evidence; the earlier
  steps are recalled and tagged.
- **Why the rate history is the reason this product exists.** At a *Höchstrechnungszins* of 0,25 %
  the guaranteed component of a conventional annuity's return is negligible and the discretionary
  component is the whole story. An Indexpolice takes that same discretionary component and, instead
  of crediting it as a modest certain interest amount, converts it into a bounded lottery on an
  index. **The product is a direct commercial response to a near-zero guaranteed rate.** The 2025
  rise to 1,00 % raises the guaranteed component again and makes the *sichere Verzinsung* arm
  relatively more attractive; whether that has shifted observed elections is `[unverified]`.

### R8 — *Mindestzuführungsverordnung* (MindZV)
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html` — the full-text page,
  which returns the whole regulation (52,6 kB); the earlier `/mindzv/` form is a **404**
- Retrieved: **yes** — full-text page read 2026-08-30, and §§ 3, 4, 6, 7, 8 re-read from canonical
  XML, Stand: zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688. The three minima are § 6 Abs. 1
  (90 % of the anzurechnende *Kapitalerträge* "abzüglich der rechnungsmäßigen Zinsen"), § 7 (90 %
  of the *Risikoergebnis*) and § 8 (50 % of the *übrige Ergebnis*), each floored at zero and taken
  separately for Alt- and Neubestand. [S7] § 13 Ziffer 2 states the same rule in the AVB. Tag off.
- Content: prescribes the minimum share of each source of surplus that must be allocated to the
  policyholders, through the *Rückstellung für Beitragsrückerstattung* (RfB). The shares, as
  established in the sibling delib files: **90 % of the *anzurechnende Kapitalerträge*** after the
  charge for discounting the *Deckungsrückstellung*; **90 % of the *Risikoergebnis***; and **50 % of
  the *übriges Ergebnis***.
- Why it matters here: **this is where the option budget comes from.** The insurer earns a return on
  the *Sicherungsvermögen*, the MindZV forces at least 90 % of the excess over the guarantee into the
  policyholders' share, the insurer declares an *Überschussanteilsatz* out of that, and a contract in
  the index arm has that declared amount spent on options instead of credited. **The option budget is
  therefore bounded by the same investment performance and the same statutory minimum that bound a
  classic contract's declared rate.** This is the most under-appreciated fact about the product and
  it belongs on the product specification's first page.

### R9 — VAG § 139 (*Überschussbeteiligung*, *Sicherungsbedarf*), § 124 (*Anlagegrundsatz*), and the *Sicherungsvermögen* provisions
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vag_2016/` (contents page, 88,5 kB)
- Retrieved: **yes** — canonical XML, §§ 124, 125 and 139, Stand: zuletzt geändert durch Art. 25 G
  v. 25.3.2026 I Nr. 81, read 2026-08-30. § 124 Abs. 1 Nr. 5 permits derivatives "sofern diese zur
  Verringerung von Risiken oder zur Erleichterung einer effizienten Portfolioverwaltung
  beitragen"; § 139 Abs. 3 and 4 carry the *Sicherungsbedarf* restriction. Section numbering
  confirmed; tag off.
- Content: § 139 VAG governs the surplus participation from the supervisory side and contains the
  *Sicherungsbedarf* rule that limits exiting policyholders' share of the *Bewertungsreserven* to
  the excess over the reserve strengthening need on contracts with a high guaranteed rate. § 124
  states the **prudent person** investment principle; the derivative provisions of the same part
  permit derivatives only "sofern diese zur **Verringerung von Risiken oder zur Erleichterung einer
  effizienten Portfolioverwaltung** beitragen", excluding pure trading positions and short sales
  (§ 124 Abs. 1 Nr. 5). Section numbering confirmed; tag off.
- Why it matters here: buying index options to back an index-participation obligation is the
  paradigm of a derivative **hedging a liability the insurer has itself written** — liability and
  hedge matched by construction, month for month and cap for cap. The insurer does **not** take an
  equity view for the policyholder; it buys the exact payoff it promised, and the Cap is whatever
  level makes that purchase cost the option budget. Sections 3 and 8 develop this — and **both
  retrieved AVB confirm it in terms**: the Cap is set "auf der Grundlage von Angeboten mehrerer
  Finanzinstitute" ([S2] Ziffer 3.3 Absatz 2 b)), the *Beteiligungsquote* "auf der Grundlage von
  Angeboten mehrerer Banken für geeignete Kapitalmarktinstrumente (z. B. Index Warrants, Optionen,
  Futures, Fondsanteile)" ([S7] § 3 Ziffer 4). Tag off.

### R10 — PRIIPs: Regulation (EU) No 1286/2014 and Delegated Regulation (EU) 2017/653
- Publisher: EUR-Lex
- URL: `https://eur-lex.europa.eu/legal-content/DE/ALL/?uri=CELEX:32017R0653`, with the 2021/2268
  amendment at `…?uri=CELEX:32021R2268`.
- Retrieved: **partly** — the EUR-Lex landing pages return substantive bodies and were read on
  2026-08-30, but the **Anhang II categorisation text was read at second hand**, from [R11], which
  quotes it, and from [S4], a KID drawn up under it. The annexes were not read directly, so the
  category rule below is sourced to [R11] rather than to the regulation itself.
- Content: requires a three-page *Basisinformationsblatt* for every packaged retail investment and
  insurance-based investment product, with a prescribed structure: what the product is, the risk
  indicator on a 1-to-7 scale, four performance scenarios (stress, unfavourable, moderate,
  favourable), the costs over time and the composition of costs including the reduction in yield,
  and the recommended holding period. The delegated regulation prescribes the methodology and the
  **product categories** that determine how scenarios are computed.
- Why it matters here: an Indexpolice is a **Category 4** PRIIP — its value depends in part on a
  factor not observed in the market, the insurer's discretionary surplus declaration — rather than a
  Category 3 derivative product. [R11] states the rule in terms: "Gemäß Ziffer 7 Anhang II RTS zur
  PRIIP-Verordnung sind Versicherungsanlageprodukte, deren Wertentwicklung teilweise von nicht am
  Markt beobachteten Faktoren abhängt, … der sogenannten Kategorie 4 zuzuordnen." One carrier's KID
  is now in hand [S4] and the tag comes off; no carrier's KID *states* its own category. Category 4
  permits
  the insurer's own model for the discretionary component, which is why two Indexpolicen with
  similar mechanics can publish very different favourable scenarios.

### R11 — DAV, *Ergebnisbericht* of the *Ausschuss Lebensversicherung* on the PRIIP Category 4 *Standardverfahren*
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV)
- URL:
  `https://aktuar.de/content/PDF/Fachwissen/2025-07-01_DAV_Ergebnisbericht_LV_Standardverfahren_PRIIP_Kategorie_4.pdf`
- Retrieved: **yes** — PDF, 30 pp., *Ergebnisbericht des Ausschusses Lebensversicherung*, "Ein
  Standardverfahren für PRIIP der Kategorie 4", Köln, verabschiedet 1. Juli 2025, read 2026-08-30.
- Content: the German actuarial profession's standard procedure for the MRM and the performance
  scenarios of Category 4 products — exactly the discretionary-surplus component that makes an
  Indexpolice one. The report states its own status: it "stellt im Sinne des Anhangs II der RTS zu
  PRIIP einen 'robusten, anerkannten Branchen- oder Regulierungsstandard' dar", while adding that it
  "stellt keine berufsständisch legitimierte Position der DAV dar". Its capital-market model is
  deliberately aligned with the **PIA-Standard** used for the *Chancen-Risiko-Klassifizierung* of
  certified products, so that Kategorie-4 PRIIPs "(insbesondere Rentenversicherungen der 3. Schicht)"
  and AltZertG products are assessed comparably — the bridge between [S4] and [S11]. **Gap 14 is now
  answered negatively rather than left open**: the procedure is generic to Category 4 and says
  nothing specific about index-participation mechanics, so how a German Indexpolice's disclosed
  scenarios treat a cap or a quota is not derivable from it.

### R12 — *Altersvorsorgeverträge-Zertifizierungsgesetz* (AltZertG), and the *Produktinformationsstelle Altersvorsorge*
- Publisher: Gesetze im Internet (statute); Produktinformationsstelle Altersvorsorge gGmbH (the
  classification body)
- URL: `https://www.gesetze-im-internet.de/altzertg/` (contents page, 8,7 kB)
- Retrieved: **yes** — canonical XML, § 1, Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I
  Nr. 294 (three 26.5.2026 amendments noted as not yet consolidated), read 2026-08-30. § 1 Abs. 1
  Nr. 3 is the *Beitragserhaltungszusage*: "zumindest die eingezahlten **Altersvorsorgebeiträge**"
  must be available at the start of the payout phase, with **up to 20 % of the *Gesamtbeiträge*
  disregarded** where they buy occupational-disability or survivor cover — a carve-out this file
  did not have. The statutory phrase names *Altersvorsorgebeiträge*, which EStG § 82 Abs. 1
  defines as *Beiträge* and *Tilgungsleistungen*, so the formulation "contributions and
  allowances" used elsewhere goes beyond the text. § 1 Abs. 1 Nr. 2 fixes the earliest payout at
  the 62. Lebensjahr. Tag off.
- Content: the AltZertG defines the criteria a *Riester* or *Basisrente* contract must satisfy to be
  certified. For *Riester*, the decisive one is the ***Beitragserhaltungszusage***: the provider must
  undertake that at the start of the payout phase **at least the *eingezahlte Altersvorsorgebeiträge*
  are available** — a **100 % nominal guarantee** of those contributions, § 1 Abs. 1 Nr. 3, with up
  to 20 % of the *Gesamtbeiträge* disregarded where they buy biometric cover. The subsection is
  confirmed and the tag comes off; the parenthesis "including the state allowances" is not in the
  statutory phrase and is dropped. For *Basisrente* there is no equivalent statutory guarantee requirement. The AltZertG
  also mandates the standardised *Produktinformationsblatt* [S11], on which the PIA's
  **Chancen-Risiko-Klasse** (1 to 5) appears.
- Why it matters here, and it is the sharpest single fact in this file about guarantee levels:
  **the guarantee level of an index product is set by its wrapper, not by its index module.** A
  *Schicht 3* Indexpolice may be sold with an 80 % or 90 % *Beitragsgarantie*; a *Riester*
  Indexpolice may not, because 100 % is statutory. That difference is the reason a *Riester* index
  variant has a structurally smaller option budget than a *Schicht 3* one of the same vintage and
  term. It is also the reason the *Riester* market effectively closed to new business when the
  *Höchstrechnungszins* fell to 0,25 % in 2022: at that rate a 100 % nominal guarantee over a normal
  term could not be calculated with room left for costs, let alone for an option budget
  `[unverified]` as to the year and the extent of the withdrawal, though the episode itself is
  well-established market history.

### R13 — EStG § 22 Nr. 1 Satz 3, *Ertragsanteilsbesteuerung* of a *Leibrente*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` — this section page returns the **full
  text** (47,9 kB), not a frameset
- Retrieved: **yes** — section page and canonical XML, Stand: zuletzt geändert durch Art. 7 G v.
  29.6.2026 I Nr. 197, read 2026-08-30. The precise citation is § 22 Nr. 1 Satz 3 Buchst. a
  Doppelbuchst. bb, with the table in Satz 4, which gives **exactly 17 %** at age 67 (18 % at
  65–66, 16 % at 68). Tag off, and the hedge "about" with it.
- Content: a *Leibrente* from a privately funded *Schicht 3* annuity is taxed only on its
  ***Ertragsanteil*** — a fixed percentage of the annuity determined once and for all by the
  annuitant's age at *Rentenbeginn* and set out in a statutory table. Values read from the statutory
  table (§ 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb Satz 4), exact: **22 % at 60–61, 20 % at 63,
  18 % at 65–66, 17 % at 67, 16 % at 68**. Tags off.
- Relevance: identical to product 2; the index mechanic does not change the annuity's tax treatment,
  the credits having been absorbed into the capital before conversion.

### R14 — EStG § 20 Abs. 1 Nr. 6, taxation of a *Kapitalabfindung*, and the *Mindesttodesfallschutz*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — this section page returns the **full
  text** (32,6 kB); the transitional rules are at `.../estg/__52.html`
- Retrieved: **yes** — section page and canonical XML for §§ 20 and 52, Stand: zuletzt geändert
  durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30. **Two citation corrections.** § 20 Abs.
  1 Nr. 6 Satz 2 as enacted says the **60.** Lebensjahr; the **62** comes from § 52 Abs. 28 Satz
  7, which applies Satz 2 "für Vertragsabschlüsse nach dem 31. Dezember 2011 mit der Maßgabe …,
  dass die Versicherungsleistung nach Vollendung des 62. Lebensjahres … ausgezahlt wird". § 52
  Abs. 28 Satz 8 confirms the *Mindesttodesfallschutz* commencement — contracts concluded "nach
  dem 31. März 2009". **And the condition is narrower than this file states**: Satz 6 Buchst. a is
  written for a "**Kapitallebensversicherungsvertrag**", not for the *Rentenversicherung mit
  Kapitalwahlrecht* that Satz 1 also covers, so reading its 50 % across to this product is an
  inference and the tag on `death_min_rate` stays.
- Content: where the *Kapitalwahlrecht* is exercised, the difference between the payment and the sum
  of premiums paid is investment income. If the contract has run at least **twelve years** and the
  payment is taken after the policyholder's **62nd** birthday (60th for contracts concluded before
  2012), **only half the difference is taxable** and it is taxed at the personal rate rather than by
  final withholding — the ages and the boundary confirmed against § 20 Abs. 1 Nr. 6 Satz 2 and § 52
  Abs. 28 Satz 7, and the tags come off. For contracts concluded after **31 March 2009** (§ 52
  Abs. 28 Satz 8) the favourable treatment additionally requires a minimum death cover
  (*Mindesttodesfallschutz*) of at least **50 %** of the premiums payable over the term — but Satz 6
  Buchst. a states that condition for a "*Kapitallebensversicherungsvertrag*", so its application to
  a *Rentenversicherung mit Kapitalwahlrecht* is an inference and **that** tag stays `[unverified]`.
- Relevance and delta: identical to product 2, with one wrinkle. Exercising the annual *Wahlrecht*
  is not a change of contract and does not restart the twelve-year clock `[unverified]`, whereas a
  *Vertragsänderung* that materially alters the contract can. **The tag stays and now has a reason**:
  neither § 20 nor § 52 addresses the point, and neither retrieved AVB does either.

### R15 — RechVersV and the VAG *Sparten*: what "indexgebundene Lebensversicherung" means in regulation
- Publisher: Gesetze im Internet (VAG, RechVersV)
- URL: `https://www.gesetze-im-internet.de/vag_2016/` for VAG §§ 124 and 125; the RechVersV
  *Formblätter* were not read.
- Retrieved: **yes for the statutory hinge** — canonical XML, VAG §§ 124 and 125, Stand: zuletzt
  geändert durch Art. 25 G v. 25.3.2026 I Nr. 81, read 2026-08-30; **no** for the RechVersV
  *Formblätter* and the Solvency II line-of-business table, which stay `[unverified]`. **The reading
  is now the statute's.** § 124 Abs. 2 scopes the class by whether "das Anlagerisiko vom
  Versicherungsnehmer getragen wird", its Satz 2 Nr. 2 covering benefits "**direkt** an einen
  Aktienindex oder an einen anderen … Referenzwert gebunden"; § 125 Abs. 5 Nr. 4 requires an
  *Anlagestock* only where contracts "**direkt an einen Aktienindex oder andere Bezugswerte binden**".
  An Indexpolice is in neither limb. Two other retrieved provisions cross-check it: VVG § 169 Abs. 4
  puts the *Zeitwert* rule only on that class [R2], and VVG § 154 Abs. 1 Satz 2 exempts only that
  class from the *Modellrechnung* [R5]. Both AVB and both KIDs put the capital in the
  *Sicherungsvermögen* in terms [S2] [S4] [S7].
- Content, and this is a terminological trap that a careless downstream document will fall into:
  in the regulatory and accounting vocabulary, **"Lebensversicherungen, bei denen das Anlagerisiko
  vom Versicherungsnehmer getragen wird"** — the class that contains *fondsgebundene* and
  *indexgebundene* life insurance in the balance-sheet sense — means contracts where the
  **policyholder bears the investment risk**. An *Indexpolice* of the kind this file describes
  **does not belong there**: the capital is in the *Sicherungsvermögen*, the guarantee is the
  insurer's, and the policyholder's downside is limited to forgoing one year's surplus. It is booked
  and reserved as a **conventional profit-participating contract**. In the Solvency II lines of
  business the same distinction appears as *insurance with profit participation* versus
  *index-linked and unit-linked insurance*, and an Indexpolice sits in the former `[unverified]` as
  to the line-of-business numbering.
- Consequence for delib: the market word *indexgebunden* and the regulatory word *indexgebunden*
  denote different things. The delib documents use *Indexpolice* / *Indexbeteiligung* for the
  product and reserve *indexgebunden* in its regulatory sense, and say so.

### R16 — BaFin, *Merkblatt* 01/2023 (VA) on conduct-supervision aspects of capital-forming life insurance products
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht (BaFin)
- URL:
  `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html`
- Retrieved: **yes** — HTML, full text of Merkblatt 01/2023 (VA), read 2026-08-30. **The open
  question is answered negatively**: the *Merkblatt* does **not** name index products — the word
  "Index" does not occur in it — so it bites on an Indexpolice as a *kapitalbildendes
  Lebensversicherungsprodukt* and not as a class of its own. It makes the *Effektivkosten* the
  measure of cost, computed by "die Methodik …, welche die LVU für Produkte im Sinne von § 2 Abs. 1
  Nr. 9 VVG-InfoV i.V.m. § 2 Abs. 6" apply, tying this entry to [R5]; and it requires the annuity
  phase and each significant biometric cover to be assessed for customer benefit in their own right.
  Gap 15 closes.
- Content: BaFin's statement of what it expects of the product-governance and value-for-money of
  capital-forming life products — established as existing by the sibling `kapitallebensversicherung`
  research file, where it supported the propositions that *Effektivkosten* differ considerably
  across the market and that BaFin will examine outliers.
- Relevance: an Indexpolice is squarely within scope and raises the *Kundennutzen* question in its
  sharpest form — a design that credits zero in a substantial fraction of years while carrying a full
  acquisition-cost load is what a value-for-money regime exists to interrogate. **Whether the
  *Merkblatt* names index products is not established.** Gap 15.

### R17 — BaFin, *Risiken im Fokus* (annual risk report) and BaFin *Fachartikel* on costs and PRIIPs
- Publisher: BaFin
- URL:
  `https://www.bafin.de/DE/die-bafin/publikationen-daten/risiken-im-fokus/Fokusrisiken_2026/RIF_Verbraucher_3/RIF_verbraucher_lebensversicherung_node.html`
- Retrieved: **yes** — HTML, *Risiken im Fokus 2026*, "Kosten von kapitalbildenden
  Lebensversicherungen", read 2026-08-30.
- Content: BaFin measures the risk by the *Effektivkosten*. Its 2022 survey of 2021 new business
  found they "unterscheiden sich erheblich" and that "in Einzelfällen beliefen sich die
  Effektivkosten auf **über vier Prozent**", above which "erscheint ein angemessener Kundennutzen
  zweifelhaft"; a repeat survey in 2025 of 2024 new business found them falling, by more than 0,4
  points in the upper quartile at long terms, chiefly on fund-linked products. **High early-duration
  lapse rates are named as a second indicator** of an inadequate customer benefit. Providers withdrew
  products and made retrospective compensation.
- Relevance: context for the charge discussion in section 13, where every level is `[std]` — and now
  a threshold to place them against: both retrieved index tariffs disclose total costs well below
  four points (1,6 % a year [S4]; 1,80 points [S11]).

### R18 — DAV recommendations on the *Höchstrechnungszins*
- Publisher: Deutsche Aktuarvereinigung e. V.
- URL:
  `https://aktuar.de/de/newsroom/detail/dav-empfiehlt-auch-fuer-2027-einen-hoechstrechnungszins-fuer-lebensversicherungs-neuvertraege-in-hoehe-von-10-prozent/`,
  with the 2026 recommendation at `…/deutsche-aktuarvereinigung-empfiehlt-auch-fuer-2026-einen-hoechstrechnungszins-in-hoehe-von-1-prozent/`.
- Retrieved: **yes** — HTML, DAV press release of 26.11.2025 recommending 1,0 % for 2027, and the
  corresponding 2026 release, read 2026-08-30.
- Content: the DAV recommends a *Höchstrechnungszins* to the Bundesfinanzministerium, which sets it
  by regulation. **1,0 %** is recommended for 2026 and again for 2027 — no longer a cross-reference
  from a sibling file. The release also supplies the rate history the regulation's current *Stand*
  cannot give: "Von 2022 bis 2024 lag der Höchstrechnungszins … bei 0,25 Prozent. Im Jahr 2025 wurde
  er auf 1,0 Prozent angehoben." Its derivation is five-year smoothed returns on a representative
  new-money portfolio with a 40 % *Sicherheitsabschlag* floored at 0,4 points. **A caveat the cohort
  structure depends on**: the figure is "eine Empfehlung für eine gesetzliche **Obergrenze**", each
  insurer setting the rate it offers within it — [S7] § 1 Ziffer 3 prices its guaranteed
  *Rentenfaktor* at a *Rechnungszins* of 0,1 % p. a.
- Relevance: fixes the guarantee basis for a contract issued at the access date, and so the split
  between the guaranteed and discretionary components of the return — here, between the guaranteed
  capital and the option budget.

### R19 — GDV statistics: *Die deutsche Lebensversicherung in Zahlen*, and the new-business and in-force series
- Publisher: GDV
- URL:
  `https://www.gdv.de/resource/blob/180978/b8ae8eb0b1bf4b15e7cc3354bc231af9/die-deutsche-lebensversicherung-in-zahlen-2024-publikation-pdf-data.pdf`
- Retrieved: **yes** — PDF, 40 pp., *Die deutsche Lebensversicherung in Zahlen 2024*, read
  2026-08-30.
- Content: the industry association's annual statistics. The in-force split at 31.12.2023 is
  *Renten- und Pensionsversicherungen* 61,8 %, *Kapitalversicherungen (klassisch)* 15,7 %,
  *Invaliditätsversicherungen* 9,2 %, *Risikoversicherungen* 6,5 %. The *Stornoquote* by count is
  **2,56 % in 2023** (2,51 % in 2022), for all *Hauptversicherungen* together.
- Relevance, and the limitation is now **confirmed by reading the publication**: **the GDV product
  split does not isolate Indexpolicen** — there is no index line, and the word "Index" occurs nowhere
  in the forty pages except the publication's own table-of-contents index. They are counted within
  conventional annuity business, because that is what they are [R15]. There is therefore **no
  published figure for the size of the German index-participation segment**; the only counts in this
  file are one carrier's own press statements, 400.000 in 2016 [S12] and over 500.000 in 2019 [S16].
  The *Stornoquote* is likewise a single undifferentiated number, so no index-specific or
  duration-split rate can be derived from it. Gap 8 stands, better documented.

### R20 — Assekurata, *Marktstudie* on *Überschussbeteiligungen und Garantien*
- Publisher: Assekurata Assekuranz Rating-Agentur GmbH
- URL:
  `https://www.assekurata-rating.de/2026/03/04/assekurata-marktstudie-zu-ueberschussbeteiligungen-und-garantien-2026/`
- Retrieved: **yes for the press summary** of the 24th *Marktstudie*, March 2026, read 2026-08-30;
  **no** for the study itself, which is a paid publication.
- Content: the annual survey of declared surplus rates and guarantee designs. **It reports the index
  segment separately, which this file did not expect it to**: the study covers "die Produktsegmente
  Klassik, Neue Klassik, **Index-** und Fondspolicen", and for 2026 gives *Indexpolicen* an average
  declared *laufender Überschusszins* of **3,07 %** ("etwa dem Vorjahresniveau"), against **2,62 %**
  for classic private annuities (Gesamtverzinsung 3,23 %), **2,65 %** for *Neue Klassik* (3,32 %) and
  2,49 % for guaranteed fund policies. The 2,62 % and 2,65 % this file carried as `[unverified]`
  cross-references are confirmed; the tags come off.
- Relevance: the declared surplus rate **is** the option budget [R8], so this is the closest public
  proxy for its size — and delib's `surplus_rate` of 2,50 % sits **below every figure in the survey**,
  the index-segment average by more than half a point. It also qualifies the corollary at [R8]: the
  MindZV minimum is the same for both product families, but the **declared** rate is not —
  "Indexpolicen bieten weiterhin eine deutlich höhere Überschussbeteiligung als klassische Produkte",
  index tariffs sitting in their own *Bestandsgruppen* and *Überschussverbände* ([S7] § 13 Ziffer 3).
  Whether Assekurata publishes cap levels as such is **still not established**: the summary reports
  declared rates, not caps.

### R21 — Rating houses on *Indexpolicen*: Institut für Vorsorge und Finanzplanung (IVFP), Franke und Bornberg, Morgen & Morgen
- Publisher: IVFP GmbH; Franke und Bornberg GmbH; MORGEN & MORGEN GmbH
- URL: not established. `ivfp.de/rating/indexpolicen/` answers HTTP 200 but is a **press archive**,
  not a rating with results; `franke-bornberg.de/de/blog/indexpolicen` and the Morgen & Morgen
  annuity-rating path both return **HTTP 404**.
- Retrieved: **no** — the rating houses publish results behind their own tools and paid reports, and
  no rating carrying cap or participation levels for a named panel was located on 2026-08-30. Kept as
  a known reference.
- Content: the three German houses that rate retirement-savings products. A rating of index-linked
  annuities is the only systematic public compilation this author is aware of that puts **cap levels
  and participation rates for a panel of named carriers side by side**.
- Relevance, now narrowed: gaps 2 and 9 closed from carrier documents instead — three product names
  established [S2] [S7] [S8], and levels for two of them [S5] [S8]. **What is still missing is the
  panel**: a single year's cap and quota levels across the market, which would let delib's 3,00 %
  `[std]` be placed in a distribution rather than beside two points. Gap 3, residual.

### R22 — BGB § 315, *Bestimmung der Leistung durch eine Partei* (*billiges Ermessen*)
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/bgb/__315.html` (frameset, 4,0 kB, no text)
- Retrieved: **yes** — canonical XML, Stand: zuletzt geändert durch Art. 2 G v. 2.7.2026 I Nr.
  198, read 2026-08-30. Abs. 1 "nach **billigem Ermessen**", Abs. 3 "nur verbindlich, wenn sie der
  Billigkeit entspricht. Entspricht sie nicht der Billigkeit, so wird die Bestimmung durch Urteil
  getroffen". The description in this entry is accurate; tag off.
- Content: where a contract leaves the determination of a term to one party, that party must in case
  of doubt exercise the determination according to **reasonable discretion** (*billiges Ermessen*);
  a determination made otherwise is not binding and, on application, is made by the court.
- Why it matters here: the annual **Cap-Festlegung** is a unilateral determination by the insurer of
  a term that decides the policyholder's return for the coming year. It is therefore reviewable
  under § 315 BGB, and the standard the insurer must meet is that the Cap be set on the basis it
  says it is set on — the option budget and the market price of the option package — rather than
  arbitrarily. **No German decision on the Cap-Festlegung of an Indexpolice is known to this author,
  and none was established.** Gap 16. The legal frame is nevertheless clear enough to state, and it
  is the correct frame: § 315 BGB, not § 163 VVG [R4].

---

## Extracted facts, organised by mechanic

This is the section the delib `indexpolice` product specification and technical notes are written
from. The mechanics of the product are not in dispute; the levels are. **The sections below were
written from knowledge of the design family and are now annotated against the two carrier AVB, the
two KIDs, the AltZertG *Produktinformationsblatt* and the statutes retrieved on 2026-08-30**: where
a retrieved document confirms a statement the tag comes off and the clause is cited, where one
contradicts it the correction is marked, and where none reaches the point the tag stays with a
reason. Structural statements are made plainly; levels are either sourced, `[unverified]` or
`[std]`.

### 1. Product structure and legal form

- An *Indexpolice* is a **deferred annuity contract** (*aufgeschobene Rentenversicherung*) on a
  single life, with an *Aufschubphase* running from inception to *Rentenbeginn* and a *Rentenphase*
  paying a lifelong *Leibrente* thereafter. Everything about the chassis — premium, reserve, death
  benefit before *Rentenbeginn*, *Rückkaufswert*, *Beitragsfreistellung*, *Rentenfaktor*,
  *Kapitalwahlrecht*, *Rentengarantiezeit* — is the chassis of delib product 2 and is documented
  there [S9].
- **The delta is one clause set**: how the annually declared *Überschuss* is applied. In product 2 it
  is credited as interest to the *Deckungskapital*. In an Indexpolice the policyholder may elect,
  each year, to have it spent on a one-year index-linked payoff instead.
- Legally it is a form of ***Überschussverwendung*** under § 153 VVG [R1] with **no independent
  statutory footing**: the policyholder's statutory right is to a share of surplus, the contract says
  how that share is applied, and the index formula is a contract term, reviewable as such.
- The contract is a **conventional profit-participating contract** in regulation and accounting, not
  an *indexgebundene Lebensversicherung* in the balance-sheet sense, because the policyholder does
  not bear the investment risk [R15]. This classification decides how it is reserved, how it is
  reported, and which Solvency II line of business it falls in.
- **Wrappers.** The same index module is written on four chassis: *Schicht 3* private annuity (the
  delib scope), *Basisrente* (product 5), *Riester* (product 6) and *Direktversicherung* in *bAV*
  (out of scope). The wrapper changes the guarantee requirement [R12], the tax treatment [R13][R14]
  and the accessibility of the capital, and **not the index mechanics**.

### 2. Where the money sits — *Sicherungsvermögen*, not *Anlagestock*

- **The accumulated capital of an Indexpolice sits in the insurer's *Sicherungsvermögen*** — the
  ring-fenced general-account cover pool that backs all of the insurer's guaranteed obligations —
  in exactly the same way as the capital of a *klassische Rentenversicherung*. There is no
  *Anlagestock*, no unit account, no fund, and no policyholder-level asset allocation.
- The policyholder therefore owns a **claim on the insurer measured in euros**, not a number of
  units. The reserve is a *Deckungskapital* and rolls forward by a recursion, not by a unit price.
- **What the index does is define a payoff, not an investment.** The policyholder is not invested in
  the index at any moment. The insurer buys the option package that hedges the payoff it has
  promised [R9]; the policyholder never holds it.
- Three consequences a modeller who thinks of the product as unit-linked will get wrong:
  (i) **the capital cannot fall** — there is no mark-to-market of an account, a bad year credits zero
  rather than taking anything away; (ii) **there is no unit-pricing timing** — values are struck at
  the *Indexjahr* boundary, annually, which is why the delib model is on an **annual** grid
  (`Index_DE_S`) while the genuinely unit-linked product 3 is monthly; (iii) **the surrender value is
  a reserve, not a unit value** [R2].
- **What the policyholder actually risks is the opportunity cost of one year's surplus**: if the
  *Indexjahr* ends at or below zero, the surplus that would have been credited under the *sichere
  Verzinsung* is gone, spent on an option that expired worthless. That, and nothing more, is the
  downside — and stating it precisely is the antidote to both usual misreadings, that the product can
  lose capital and that it is a cheap way to be long equities.

### 3. The financing identity — the *Überschuss* as an option budget

This is the mechanical core of the product and everything else follows from it.

- Each year the insurer declares an *Überschussanteilsatz* out of the surplus the MindZV [R8] and its
  own results permit. For a contract in the *sichere Verzinsung* arm, that declared rate is credited
  to the *Deckungskapital* as interest, on top of the guaranteed *Rechnungszins*, exactly as in
  product 2.
- For a contract in the *Indexbeteiligung* arm, **the same amount is not credited. It is spent.** It
  becomes the ***Optionsbudget*** with which the insurer buys, for the coming *Indexjahr*, the option
  package that replicates the promised index payoff.
- Written as an identity, with `G` the participating capital at the start of the *Indexjahr* and `b`
  the declared surplus rate for that year:

  ```
  option budget          =  b x G
  price of the promised   =  b x G          <-- the Cap (or the Partizipationsquote) is set to
    index payoff on G                            make this equation hold
  ```

- **The Cap is not a marketing parameter. It is the solution of a pricing equation.** Given the
  option budget, the index's forward level, its implied volatility, its dividend yield and the
  interest rate, there is exactly one Cap at which the twelve-month capped-sum payoff costs the
  budget. That is why caps move from year to year without any change in the contract, and why they
  move in the directions described in section 8.
- Two corollaries that belong on the first page of any honest description of the product:
  (i) **an Indexpolice does not have a larger risk budget than a *Klassik* contract of the same
  vintage** — it has the identical budget, the same declared surplus from the same
  *Sicherungsvermögen* under the same MindZV minimum, and spends it differently; (ii) **priced
  risk-neutrally, the index arm is worth exactly what the safe arm is worth** — the whole difference
  between them is the equity risk premium earned on the option's delta, less dealing costs. The
  product is a redistribution of one year's surplus across states of the world, not extra return.
- **The budget can be zero.** If the insurer declares no surplus for a year, there is nothing to buy
  an option with, and the *Indexbeteiligung* for that year is worthless whatever the index does
  [R1][R8]. No German carrier's AVB, as far as this author knows, guarantees a minimum option
  budget; some guarantee a minimum Cap, which is a different and weaker promise (section 8). Gap 10.

### 4. The annual *Wahlrecht*

- **The policyholder elects, once a year and for the coming *Indexjahr* only, between
  *Indexbeteiligung* and *sichere Verzinsung*.** The election is a contractual right, exercisable
  without the insurer's consent, without medical evidence and without charge.
- **What each arm delivers**:

  | Arm | The year's surplus is | Outcome |
  |---|---|---|
  | *Sichere Verzinsung* | credited to the *Deckungskapital* as interest | certain, positive, immediately guaranteed |
  | *Indexbeteiligung* | spent on the index option package | zero in a bad year; a multiple of the surplus in a good one; never negative |

- **Timing — established, and shorter than assumed.** The election must reach the insurer
  **7 days** before the *Indexstichtag* at Allianz ([S2] Ziffer 3.1) and 7 days before the
  *Versicherungsjahrestag* at R+V ([S7] § 2 Ziffer 3), not the four to six weeks this author
  supposed; the tag comes off with the estimate. **Doing nothing does not simply leave the
  policyholder where they were**: R+V's contract "nimmt grundsätzlich an der Indexpartizipation
  teil", while Allianz rolls the previous split over only if index participation was at least 50 %
  and otherwise moves the contract **to** 50 % ([S2] Ziffer 3.2). Gap 11 closes.
- **The interaction with the Cap announcement decides whether the *Wahlrecht* is an informed choice
  or a blind one — and it is informed.** Allianz notifies the indices, "die Höhe der →Caps der
  jeweiligen Indizes", the *Partizipationssatz*, the year's surplus net of *Verwaltungskosten* and
  the *Bewertungsreserven* *Sockelbetrag* "**spätestens 3 Wochen vor dem Indexstichtag**", against an
  election deadline of 7 days ([S2] Ziffer 3.1); R+V informs "jeweils rechtzeitig vor Beginn eines
  Versicherungsjahres" ([S7] § 2 Ziffer 1). delib's assumption is the carriers' rule. Gap 11 closes.
- **Partial election — established.** Allianz permits the split "in **25-Prozentschritten** …, wobei
  die Summe 100 Prozent ergeben muss", across indices and the *sichere Verzinsung* alike, and the
  annual election is expressly also the occasion to choose the index or indices ([S2] Ziffer 3.1);
  R+V's third option is the *Turbo* rather than a second index, and it offers to substitute a
  different index only on notice ([S7] § 3 Ziffer 1). delib's continuous fraction `w` in [0, 1] is
  therefore a **relaxation of a discrete 25-percent menu**, not a generalisation of an all-or-nothing
  choice; the tags come off and the simplification is named.
- **Survival of the right.** The *Wahlrecht* attaches to the capital, so it survives
  *Beitragsfreistellung* [R3] and persists to *Rentenbeginn*; it normally ceases in the *Rentenphase*,
  where surplus is applied to the annuity in payment. **Confirmed for Allianz**, whose participation
  runs "vor Beginn der Rentenzahlung" only ([S2] Ziffer 3.3); whether any other carrier offers it in
  the payout phase is still not established. Gap 17, narrowed.
- **Modelling.** The *Wahlrecht* is a **policyholder election**, which in delib's three-way
  assumption split makes it a *behavioural* assumption, not a contractual or an insurer-discretionary
  one. The delib base run sets `w = 1` (full index participation every year) as a `[std]` choice,
  because the product exists to demonstrate the index mechanic and a base run in the safe arm would
  reduce it to product 2. The specification exposes `w` per year and the technical notes list
  "election path assumed constant" as a model risk.

### 5. The Cap mechanic — the sum of capped monthly returns

**This is the single most important and most misunderstood feature of the product, and it deserves
to be stated in full and without hedging.** It is now also quotable. Allianz's AVB [S2] Ziffer 3.3
Absatz 2 a) defines the *maßgebliche Jahresrendite*:

> "Sie bestimmt sich dadurch, dass die negativen monatlichen Wertentwicklungen und die mit dem
> jeweiligen →Cap (siehe Absatz b)) des gewählten Index gedeckelten positiven, monatlichen
> Wertentwicklungen am Ende eines →Indexjahres aufsummiert werden. Die monatlichen Wertentwicklungen
> entsprechen dabei der prozentualen Veränderung des Index zwischen 2 Bewertungsstichtagen, die wir
> Ihnen jährlich mitteilen. Ergibt sich nach der Aufsummierung eine negative jährliche Summe, setzen
> wir diese auf null."

Negative months in full, positive months capped, the twelve summed, the sum floored once at zero —
the four lines below, clause for clause. **Allianz then multiplies by a *Partizipationssatz*, which
the delib model does not carry in its Cap arm** (section 7).

**Allianz's own worked *Indexjahr* pair**, published beside the clause at an exemplary Cap of 3,2 %
and *Partizipationssatz* of 75,00 %:

| Month | 2020/2021 EURO STOXX 50 | capped at 3,2 % | 2021/2022 EURO STOXX 50 | capped at 3,2 % |
|---|---|---|---|---|
| Nov | 18,06 % | **3,20 %** | −4,41 % | −4,41 % |
| Dez | 2,26 % | 2,26 % | 5,98 % | **3,20 %** |
| Jan | −2,52 % | −2,52 % | −3,05 % | −3,05 % |
| Feb | 4,45 % | **3,20 %** | −6,00 % | −6,00 % |
| Mär | 7,78 % | **3,20 %** | −0,55 % | −0,55 % |
| Apr | 1,42 % | 1,42 % | −2,55 % | −2,55 % |
| Mai | 1,63 % | 1,63 % | −0,36 % | −0,36 % |
| Jun | 0,61 % | 0,61 % | −8,82 % | −8,82 % |
| Jul | 0,62 % | 0,62 % | 7,33 % | **3,20 %** |
| Aug | 2,62 % | 2,62 % | −5,15 % | −5,15 % |
| Sep | −3,53 % | −3,53 % | −5,66 % | −5,66 % |
| Okt | 5,00 % | **3,20 %** | 9,02 % | **3,20 %** |
| **Summe** | | **15,90 %** | | **−26,96 %** |
| **Maßgebliche Jahresrendite** | | **15,90 %** | | **0 %** |
| **Indexpartizipation (× 75 %)** | | **11,92 %** | | **0 %** |

against point-to-point index movements of **+43,69 %** and **−14,89 %** respectively. Allianz's own
footnote states this file's pitfall for it: "Die Wertentwicklung des EURO STOXX 50® ergibt sich aus
der Differenz der Kurse zu Beginn und zum Ende des Betrachtungszeitraumes, **nicht aus der Summe der
monatlichen Wertentwicklungen**." Gap 4's evidence, from the insurer.

- The *Indexjahr* is divided into **twelve monthly observation periods**. For each month `m` the
  index level is read at the two *Beobachtungstage* bounding the month, and the month's return is

  ```
  r_m = I(m) / I(m-1) - 1
  ```

- Each month's return is then **capped above at the Cap `C`**, and **not floored below**:

  ```
  x_m = min(r_m, C)
  ```

- The twelve capped monthly returns are **summed, not compounded**:

  ```
  S = sum over m = 1..12 of x_m
  ```

- The *Indexrendite* credited for the year is the sum **floored at zero**:

  ```
  Indexrendite = max(S, 0)
  ```

- The credit is that rate applied to the participating capital at the start of the *Indexjahr*:

  ```
  Indexgutschrift = max(S, 0) x G
  ```

- **The three features that together define the payoff, and that must never be separated**:
  1. **Upside is capped monthly.** A month in which the index rises 8 % contributes `C`, not 8 %.
  2. **Downside is not capped at all.** A month in which the index falls 8 % contributes the whole
     −8 %. There is no floor on `x_m`, only on `S`.
  3. **The twelve are summed, not compounded.** Summation is close to compounding for small numbers,
     but it is not the same, and the contractual formula is a sum.
- **Why the asymmetry is the whole story.** The payoff is a *capped cliquet*: the policyholder is
  long the index's monthly returns, short a strip of twelve monthly calls struck at `C`, with an
  annual floor. Truncating each month's right tail while leaving its left tail intact removes far
  more expected return than the cap level suggests, because monthly equity returns are volatile: at a
  monthly standard deviation of 5 % — about 17 % annualised, ordinary for a broad European equity
  index — a 3 % cap gives away roughly **one percentage point of expected return per month**, twelve
  times a year, against an expected monthly return well under 1 %. Section 20 does the arithmetic.
- **The floor is what makes it a life-insurance product rather than a bet**, and it is genuine: the
  worst imaginable *Indexjahr* credits zero and leaves the capital untouched.
- **A trap for the modeller and the reader.** The `max(S, 0)` floor operates on the *sum*, not on
  each month, so it is **not** true that a year with more up-months than down-months credits
  something: it is perfectly ordinary for a year in which the index finished **higher** to credit
  **zero**. Example B in section 19 is that case, and a delib test must assert it.
- **Interpretation questions the corpus does not settle**, each a carrier-level clause and each
  changing a credited amount: whether the monthly observation dates are calendar month-ends or
  monthly recurrences of the *Indexstichtag*, and whether the level used is a closing level or an
  average (an Asian reading lowers the effective volatility and so buys a higher cap) — gap 18;
  whether `G` is the whole *Deckungskapital* at the start of the year, a defined index-participating
  sub-account, or the accumulated *Überschussguthaben* alone — gap 19, with delib taking the whole
  accumulated capital as `[std]`; and whether a contract beginning or ending mid-*Indexjahr*
  participates pro rata or not at all — gap 12.

### 6. The floor and the annual lock-in — *Höchststandsicherung*

- **An *Indexjahr* can never end below zero.** `max(S, 0)` is contractual, universal in this product
  family, and is the feature the product is sold on.
- **Whatever is credited is locked in.** At the end of the *Indexjahr* the *Indexgutschrift* is added
  to the capital and becomes **part of the guaranteed capital**: it is no longer at risk in any later
  year, it earns the guaranteed *Rechnungszins* thereafter like any other part of the
  *Deckungskapital*, and it enters the base `G` of every subsequent *Indexjahr*. This is the
  ***Höchststandsicherung*** / *Lock-in* / ratchet, and it is what makes the year-by-year floor add
  up to a path-independent guarantee.
- Formally, with `K(t)` the accumulated capital at the end of policy year `t`, `P(t)` the premium
  allocated, `i_g` the guaranteed rate and `b(t)` the declared surplus rate:

  ```
  index arm :  K(t) = ( K(t-1) + P(t) ) x (1 + i_g)  +  max( S(t), 0 ) x G(t)
  safe arm  :  K(t) = ( K(t-1) + P(t) ) x (1 + i_g + b(t))
  ```

  with `G(t)` the participating capital at the start of the *Indexjahr* (section 5). The monotonicity
  `K(t) >= K(t-1)` holds in both arms and is the invariant a delib `check_*()` should assert.
- **A monthly *Höchststandsicherung* is a different and rarer feature.** Some designs in the wider
  European market lock in the highest index level reached *within* the year rather than only the
  year-end sum. **Neither retrieved AVB contains one** ([S2] Ziffer 3.3, [S7] § 3), which is
  consistent with this entry but is not positive evidence about the rest of the market; it should
  still not be assumed. Gap 20.
- **What the lock-in costs.** The ratchet is not free: each year's option package is a fresh strip on
  a *larger* base whenever the previous year credited something. It finances itself automatically,
  because the surplus is declared as a rate on that same larger base — which is why the financing
  identity of section 3 is written in rates, not amounts.
- **The guarantee is a floor on the path, not only on the maturity value.** Under a plain maturity
  guarantee the insurer can recover a bad year with a good one; here every credited amount is
  permanent, so the guarantee's cost rises with every good year. That belongs in the reserving
  discussion.

### 7. The *Partizipationsquote* alternative, and other payoff variants

The Cap is the classic design. It is not the only one, and by the 2020s it was not obviously the
dominant one.

- ***Partizipationsquote* (participation rate).** Instead of capping each month, the contract credits
  a fixed fraction `q` of the *year's* index movement, floored at zero:

  ```
  Indexrendite = max( q x ( I(12)/I(0) - 1 ), 0 )
  ```

  There is no monthly cap and no monthly asymmetry: a down-month is not penalised relative to an
  up-month, because only the year's net movement matters. The whole of the give-up is in `q`.
- **The two designs are not equivalent and fail differently.** The Cap design gives away the *large*
  monthly moves and is hurt by volatility even when the year ends well; the *Quote* design gives away
  a constant fraction in every state. The *Quote* design is far easier for a policyholder to compare
  with a direct investment; the Cap design has historically bought a higher headline out of the same
  budget, a strip of monthly caps being cheaper than a fraction of a one-year call at high
  volatility.
- **Typical levels, all `[unverified]` and all `[std]` downstream**: participation rates on a broad
  price index of the order of **50 % to 80 %**; participation rates on a low-volatility house
  multi-asset index (section 9) of the order of **80 % to above 100 %**, the latter being possible
  precisely because the index is engineered to be cheap to buy options on. Gap 9.
- **Other variants in this product family**, and the retrieved AVB settle three of the four.
  **Cap and Quote in combination** — monthly returns capped *and* the sum multiplied by a
  participation rate — **is Allianz's actual design**, not a hypothetical variant: "Die
  →Indexpartizipation ermitteln wir, indem wir die maßgebliche Jahresrendite … mit dem
  →Partizipationssatz … multiplizieren" ([S2] Ziffer 3.3 Absatz 2), the *Partizipationssatz* being
  "jährlich für die Dauer eines →Indexjahres festgelegt". The tag comes off, and **delib's model
  cannot express it**: the `cap` form has no participation factor and the `quote` form has no cap
  (see the note in `model.md`). **A choice of variant each year** exists in the shape of Allianz's
  25-percent splits across two indices and the safe arm, and of R+V's and Stuttgarter's *Turbo*
  options, each of which stakes 2 % of the capital for a higher quota ([S7] § 3 Ziffer 2, [S8]).
  A ***Mindest-Cap*** **appears in neither AVB** (gap 10, closed negatively). **Averaging** is
  likewise absent: both carriers read closing levels between stated *Bewertungsstichtage*, so the
  Asian reading is ruled out for them.
- **delib's choice.** The reference implementation carries the **Cap design as the base** — because
  it is the design the product's reputation and its criticism both rest on, and because it is the one
  whose mechanic a model can demonstrate non-trivially — and the *Partizipationsquote* as a
  switchable variant. Both are `[std]` in their levels.

### 8. The *Cap-Festlegung* — who sets it, when, and on what

- **The Cap is fixed by the insurer, for one *Indexjahr* at a time, before that *Indexjahr* begins,
  and is then binding for its whole length.** It is not adjustable during the year, and a change in
  market conditions during the year does not change it.
- **The determination is a pricing calculation, not a discretion in substance** (section 3): the Cap
  is the level at which the option package costs the option budget, given that budget, the index's
  implied volatility and dividend yield, the risk-free rate and the insurer's dealing spread.
- **The directions of movement follow from that, and they are the useful part**:

  | If this rises | the Cap | because |
  |---|---|---|
  | the declared surplus rate (option budget) | rises | more money buys more upside |
  | the index's implied volatility | falls | monthly caps are strips of options; volatility makes them dearer |
  | the index's dividend yield | falls | options are on the price index; a higher dividend yield lowers the forward |
  | the risk-free rate | rises, indirectly | it raises the investment return and hence the surplus available |

- **Historical direction of travel**, qualitative because no level is established: caps compressed
  hard through the low-interest decade to the early 2020s as the surplus available to buy them shrank
  [R7], then recovered room as rates rose from 2022 and the *Höchstrechnungszins* went to 1,00 % for
  2025 [R18]. **Two levels are now on record and neither is a declared cap for a named year**:
  Allianz's own worked illustration runs at a Cap of **3,2 %** with a *Partizipationssatz* of
  **75,00 %**, both "exemplarisch gewählt" ([S2]), and the 2018 litigation records a cap of 3,3 %
  then in force ([S14]). Stuttgarter **publishes** an actual *Partizipationsquote* of **70 %** for
  1.2.2026–31.1.2027 ([S8]) — a declared level for a named insurer and a named year, though for a
  quota design rather than a cap one. Gap 3, narrowed to the missing market panel.
- **The plausible range, as a `[std]` band with a rationale**: monthly caps in this family have been
  seen over the 2010s and 2020s between roughly **1,5 % and 5,0 %**, typically **2,5 % to 4,0 %**
  `[unverified]`. delib uses **`Cap = 3,0 % per month`** as `[std]`, the midpoint, and the technical
  notes must run the worked example across the band rather than present the midpoint as a fact.
- **Announcement — established.** The Cap is communicated in the annual notification [S5], whose
  content and deadline the AVB prescribes: the indices, "die Höhe der →Caps der jeweiligen Indizes",
  the *Partizipationssatz*, the year's surplus net of *Verwaltungskosten* and the *Bewertungsreserven*
  *Sockelbetrag*, "spätestens 3 Wochen vor dem Indexstichtag" ([S2] Ziffer 3.1). No instance of the
  notification and no carrier *Standmitteilung* was located, but the GDV's model *Standmitteilung*
  was, and it has **no cap row** [S10]. One carrier publishes its parameters openly instead of
  notifying them privately: Stuttgarter's current quota and safe rate are on its website [S8].
- **Legal review.** The *Cap-Festlegung* is a unilateral determination of a contractual term,
  reviewable under § 315 BGB for *billiges Ermessen* [R22] — not under § 163 VVG, which governs
  adjustments of the contract itself [R4]. An insurer setting caps below what its option budget
  bought would be exposed under § 315 BGB, and that, rather than any supervisory rule, is the
  discipline on the determination. **No decided German case on the point is known.** Gap 16.

### 9. The index — EURO STOXX 50, and the move to house multi-asset indices

- **The classic underlying is the EURO STOXX 50**, the euro area's blue-chip index and the
  underlying of the first German index-participation products — **confirmed as Allianz's**, alongside
  the **S&P 500**, whose non-euro quotation brings in a *Währungsfaktor* applied to the year return
  ([S2] Ziffer 3.3 Absatz 2 c)); a policyholder may hold both in 25-percent steps. Two of its properties drive the
  economics: (i) **it is quoted and used as a *price index*** (*Kursindex*), with dividends excluded,
  and options are written on the price index — so the euro-area dividend yield, of the order of
  **3 % per year** `[unverified]`, never reaches the policyholder in any state of the world, a
  permanent structural give-up on top of the cap and invisible to a purchaser comparing the product
  to "the index"; (ii) **it is volatile**, of the order of 18 % to 22 % annualised in ordinary
  conditions `[unverified]`, which makes the monthly cap strip expensive and forces the Cap down.
- **The shift to house indices.** From the mid-2010s a substantial part of the German market replaced
  the EURO STOXX 50 in these tariffs with **bespoke multi-asset indices** built for the insurer by an
  investment bank or index provider. Their common features: **multi-asset** composition (equities,
  bonds, sometimes commodities and money market) so that volatility is structurally lower than an
  equity index's; **volatility targeting**, a rule scaling exposure to hold realised volatility at a
  target often around **5 %** `[unverified]` — the decisive engineering step, because at a 5 % target
  the option package costs a fraction of what it costs on a 20 %-volatility equity index, so the same
  budget buys a **participation rate near or above 100 %**, a far better headline than 55 % of the
  EURO STOXX 50; an **excess-return construction with an embedded fee**, the index defined net of a
  funding rate and net of an index-level deduction of the order of **0,5 % to 1,5 % per year**
  `[unverified]`, which reduces the policyholder's return without appearing in any cost disclosure;
  and **a short live history behind a long backtest**, which makes published "historical" performance
  of the product weaker evidence than it appears.
- **The honest summary of the shift**: it moved the give-up from somewhere the purchaser can see — a
  55 % participation rate, a 3 % cap — to somewhere they cannot: an index rule, a volatility target,
  a fee inside the index level, a backtest. Headline numbers improved; expected outcomes did not
  necessarily improve with them, because the section-3 identity still binds — **the payoff still
  costs the option budget, whatever the underlying is called.**
- **Two German house indices are now named from carrier documents**, and the qualitative claim above
  is confirmed at the level of existence and composition: R+V's ***Solactive Multi Anlage Stabil
  Index* (SOMAS)**, built for the tariff by R+V and Solactive and described by the carrier as
  combining equities, bonds and gold under a "Stabilitätsmechanismus" ([S7] § 3 Ziffer 1), and the
  ***Stuttgarter M-A-X Multi-Asset Index***, beside a *Stuttgarter Grüne Zukunft Index* ([S8]).
  **But not one of the quantitative claims above is confirmed**: neither carrier publishes a
  volatility target, an excess-return construction or an index-level fee on the pages that describe
  its index, so the 5 % target and the 0,5–1,5 % embedded fee stay `[unverified]`. **And one
  quantitative claim is put in doubt**: Stuttgarter's published *Partizipationsquote* on its house
  index is **70 %** ([S8]), not the "near or above 100 %" the volatility-target argument predicts —
  below even Allianz's 75,00 % illustration on the EURO STOXX 50. Gap 21, half closed.
- **No index is named in any shipped delib input file**, and the model still parameterises the
  underlying by drift and volatility rather than by name.
- **Modelling consequence.** delib parameterises the index by an assumed annualised volatility and
  drift, both `[std]`, and by an explicit monthly return path in an external CSV, showing the
  high-volatility equity and low-volatility multi-asset cases side by side — the honest way to
  represent a fact established qualitatively and not quantitatively.

### 10. Index substitution, *Ersatzindex* and adjustment clauses

- Every contract of this family needs a clause for what happens if the index ceases to be published,
  is materially restructured, or ceases to be available on terms on which the insurer can buy the
  hedge. The standard solution is an ***Ersatzindex*** clause: the insurer may substitute a
  comparable index, on notice to the policyholder.
- **Both questions are now answered, and both answers are the opposite of the guess** (gap 22).
  Neither retrieved clause requires an **unabhängiger Treuhänder**, and neither gives the
  policyholder a *Sonderkündigungsrecht*. Allianz may replace an index "mit Wirkung zu Beginn des
  nächsten →Indexjahres" where material changes it is not responsible for affect the index or the
  instruments referencing it, may adapt the determination procedure to the new index, and — if it
  cannot replace one — **may exclude the participation for subsequent *Indexjahre* altogether**
  ([S2] Ziffer 3.7). R+V replaces the index at the next *Indexstichtag* with one that "dem zu
  ersetzenden Index weitestgehend entspricht", at no cost to the policyholder, and lets the
  policyholder decide whether to continue on it ([S7] § 3 Ziffer 11); it also carries a separate
  **suspension** clause where no suitable capital-market instrument can be bought, the budget then
  going to the *Verzinsung* arm (§ 3 Ziffer 10).
- The distinction from § 163 VVG matters again here — and the retrieved statutes sharpen it.
  § 163 VVG (*Prämien- und Leistungsänderung*) is about a changed *Leistungsbedarf* and needs a
  trustee; § 164 VVG (*Bedingungsanpassung*) needs the clause to have been declared ineffective "durch
  höchstrichterliche Entscheidung oder durch bestandskräftigen Verwaltungsakt" and needs **no**
  trustee. **Index substitution is neither**: it is an express contractual power the AVB reserves,
  exercised on stated conditions, and it stands or falls on that clause and on § 307 BGB, not on
  § 163 or § 164 [R4][R22].
- **Modelling consequence**: none directly, but it belongs in the model-risk list — a model
  projecting thirty *Indexjahre* on one index rule assumes no substitution over a period in which the
  market has already substituted once.

### 11. The guarantee at *Rentenbeginn*, and *Beitragsgarantie* levels below 100 %

- **The guarantee of an Indexpolice is an end-of-accumulation guarantee.** What the contract promises
  is a *garantiertes Kapital zu Rentenbeginn*, normally expressed as a percentage of the premiums
  paid — the ***Beitragsgarantie*** or *Garantieniveau* — plus every index credit locked in along the
  way (section 6), and a *garantierter Rentenfaktor* converting that capital into an annuity.
- **It is not a guaranteed annual interest rate on the reserve.** That is the defining feature of
  ***Neue Klassik*** and the reason index products are grouped under that label [S6]: by owing the
  guarantee only at one future date rather than at every balance date, the insurer can hold a
  materially riskier asset mix behind it and generate the surplus that becomes the option budget.
  A model that reserves an Indexpolice as though it guaranteed `i_g` every year overstates the
  guarantee.
- **Why guarantee levels fell below 100 %.** A 100 % nominal guarantee of gross premiums over 30
  years is trivially affordable at a 3,5 % technical rate and close to impossible at 0,25 % once
  acquisition and administration costs come out of the same premiums. Through the 0,90 % and 0,25 %
  years [R7] carriers offered a **choice of *Garantieniveau***. Three levels are now observed in
  retrieved documents — **90 %** and **80 %** at Allianz (IndexSelect and IndexSelect Plus, [S4]),
  **90 %** at R+V ([S7] § 1 Ziffer 2), **85 %** for the Stuttgarter *Basisrente* variant ([S11]) —
  with 90 % the modal level; the older 60 % rung stays this author's recollection and
  `[unverified]`. The arithmetic explains the
  whole design generation: **every euro of guarantee not promised is a euro that can back risk
  assets, and therefore a larger option budget.**
- **The wrapper decides the floor** [R12]: a *Riester* variant must undertake that "zumindest die
  eingezahlten Altersvorsorgebeiträge" are available at the start of the payout phase — up to 20 % of
  the *Gesamtbeiträge* disregarded where they buy biometric cover, AltZertG § 1 Abs. 1 Nr. 3 — and so
  has the smallest option budget of the four; the formulation "contributions **and allowances**" used
  earlier in this file goes beyond the statutory phrase and is dropped; *Basisrente* and *Schicht 3* may
  guarantee less; *Direktversicherung* has its own statutory floor and is out of scope.
- **`[std]` for delib**: *Garantieniveau* **90 % of *Beitragssumme***, the level at which a 1,00 %
  contract can still finance a visible option budget over a 30-year term — **and the modal level in
  the retrieved documents**. The technical notes show the option budget as a function of it — the most
  instructive single sensitivity this product has.
- **Interaction with the lock-in.** The effective guarantee is
  `max( Beitragsgarantie, guaranteed capital including all locked-in index credits )`, the second
  term dominating after a few good years. A projection must carry both, and a test should assert that
  the guaranteed capital is monotone non-decreasing.

### 12. Premium

- **Level *Beitrag*, payable monthly, quarterly, half-yearly or annually** over a
  *Beitragszahlungsdauer* that may be shorter than the *Aufschubdauer*; *Einmalbeitrag* versions
  exist and *Zuzahlungen* are commonly permitted.
- A ***Ratenzahlungszuschlag*** applies for paying other than annually; the market convention
  recorded in the sibling delib file is of the order of **2 % half-yearly, 3 % quarterly, 5 %
  monthly** `[unverified]`, and delib carries it as `[std]`.
- A ***Dynamik*** option — automatic annual premium increase with a matching benefit increase and a
  right to decline — is normal on this chassis; each increment is a new tranche with its own
  guarantee basis `[unverified]`.
- **The premium does not enter the index formula.** Premiums build the capital `K`; the payoff is
  struck on `G`, the participating capital at the *start* of the *Indexjahr*, so on the natural
  reading premiums paid during a year participate only from the following one. **Whether carriers
  pro-rate them is not established** (gap 12); delib adopts the natural reading as `[std]`.
- **`[std]` model point**: *Beitrag* **200 € per month**, entry age **40**, *Aufschubdauer* **27
  years** to *Rentenbeginn* at **67**, premiums payable throughout. Rationale in section 22.

### 13. Charges

Nothing about the charge structure of an Indexpolice is special; nothing about its levels is
established.

- **Abschluss- und Vertriebskosten**, financed by *Zillmerung*, capped by the DeckRV
  *Höchstzillmersatz* — DeckRV § 4 Abs. 1: "Der Zillmersatz darf **25 Promille der Summe aller
  Prämien** nicht überschreiten" [R7], tag off, **and both retrieved carrier disclosures charge
  exactly 2,50 % of premiums** ([S4], [S11]) — and required by
  § 169 VVG to be spread over at least the first five years for the purpose of the
  *Mindestrückkaufswert* [R2]. The two rules are different rules with different functions and delib
  keeps them apart.
- **Verwaltungskosten**, typically a percentage of each premium (`β`) plus a percentage of the
  *Deckungskapital* (`γ`), sometimes with a fixed *Stückkosten* amount per year.
- **The index-specific charges are the ones that do not appear in the charge tables**:
  - the **dealing cost and spread** on the option package, which is inside the Cap rather than in a
    charge line — a wider spread simply produces a lower Cap;
  - for house indices, the **index-level deduction and the volatility-target drag** (section 9),
    which are inside the index and therefore inside neither the Cap nor the disclosed costs;
  - the **dividend yield of a price index** (section 9), which is not a charge at all but is a
    permanent give-up of the same order of magnitude as one.
  Together these mean the disclosed *Effektivkosten* **understate** the economic give-up relative to
  holding the index, by an amount disclosed nowhere. That is a structural fact, not a claim about any
  carrier, and it is the most substantive fair-criticism point in the file.
- **No charge level of any kind is established for any German index product.** Every charge in delib
  is `[std]`. The `[std]` set the reference implementation uses, with the sibling files' reasoning:
  *Abschlusskosten* **2,5 % of *Beitragssumme*** zillmerised over five years; *Verwaltungskosten*
  **β = 3 % of each premium** and **γ = 0,25 % of the *Deckungskapital* per year**. Gap 6.

### 14. *Rückkaufswert* and *Beitragsfreistellung*

- **Surrender** delivers the *Rückkaufswert* under § 169 VVG [R2]: the actuarial reserve, floored by
  the five-year-spread *Mindestrückkaufswert*, less any contractually quantified *Stornoabzug*.
- **Locked-in index credits are inside the reserve** and are therefore inside the surrender value —
  they are guaranteed capital by then (section 6), not a contingent entitlement.
- **The running *Indexjahr* is not.** A surrender in month 7 of an *Indexjahr* forfeits that year's
  option payoff, because the payoff exists only at the year end. Whether the unspent option budget is
  refunded, whether a pro-rata payoff is computed, or whether the policyholder simply loses it, is a
  carrier-level clause and **is not established**. Gap 12. delib's `[std]` is the simple and, in this
  author's understanding, usual treatment: **no index credit in the year of exit**.
- **A real behavioural incentive, and it belongs in the lapse discussion**: the product rewards
  surrendering just after an *Indexjahr* end and penalises surrendering just before one. An annual
  grid with exits at year end implicitly assumes the favourable convention; the notes must say so.
- **Beitragsfreistellung** under § 165 VVG [R3] leaves the capital in place, continues the index
  participation on it, preserves the *Wahlrecht* (section 4), and converts the contract to a reduced
  guaranteed benefit computed on recognised actuarial principles.
- **Stornoabzug** must be agreed, appropriate and quantified [R2]; the sibling KLV file records one
  carrier's structure of a **5 % base deduction plus a capital-market-dependent component of 5 %,
  10 % or 15 % of the *Deckungskapital*** `[unverified]`, established there by search. delib's
  `[std]` is a **flat 2 % of the *Deckungskapital*, floored so the *Mindestrückkaufswert* is never
  breached**, with the observed range recorded beside it.

### 15. The death benefit before *Rentenbeginn*

- The *Todesfallleistung* delib models in the *Aufschubphase* is the **return of the accumulated
  capital** rather than a sum at risk. **That is one of two shapes in the market, and the retrieved
  documents show both.** R+V's index tariff pays "der Policenwert, mindestens jedoch 90 % der Summe
  der gezahlten Beiträge" ([S7] § 1 Ziffer 5), and Allianz's KID shows the same amount in the death
  and survival scenarios ([S4]) — the shape delib models. But the [S9] chassis, retrieved in its
  2026 edition, provides **no death benefit at all** unless an extension is agreed, and where one is,
  the standard form is *Beitragsrückgewähr* — a return of **premiums**, not of capital (§ 1 Abs. 2
  and 3). The claim this file attached to [S9] was wrong and the citation is moved to [S7].
- **Index-specific point**: death mid-*Indexjahr* attracts **no** pro-rata index credit, as for
  surrender (gap 12, now closed) — R+V computing the *Policenwert* "zum Ende des Monats, in dem der
  Todestag der versicherten Person liegt" with no index element for the incomplete year ([S7] § 1
  Ziffer 5).
- Because the sum at risk is close to zero the *Risikoüberschuss* is small, underwriting is light
  (section 17) and § 161 VVG [R6] is close to inoperative. The **50 % *Mindesttodesfallschutz***
  condition of the tax rules [R14] bites on the *Kapitalwahlrecht* treatment, not on the annuity, and
  is why some tariffs carry a death benefit above the plain return of capital — R+V's 90 %-of-premiums
  floor being an instance well above the 50 % the tax rule names ([S7] § 1 Ziffer 5). **The tax rule
  itself is narrower than this file states**: EStG § 20 Abs. 1 Nr. 6 Satz 6 Buchst. a is written for
  a "*Kapitallebensversicherungsvertrag*", so applying its 50 % to a *Rentenversicherung mit
  Kapitalwahlrecht* is an inference [R14].

### 16. The *Rentenphase* — *Rentenfaktor* and *Kapitalwahlrecht*

Inherited wholesale from delib product 2; recorded here only as the delta.

- At *Rentenbeginn* the accumulated capital `K` — guaranteed capital plus all locked-in index credits
  plus any *Schlussüberschuss* and *Bewertungsreserven* share — is converted at the *Rentenfaktor*:

  ```
  monthly annuity = K / 10 000 x Rentenfaktor
  ```

- The applied factor is the **maximum of the guaranteed factor fixed at issue and the insurer's
  current factor at *Rentenbeginn***, a guarantee with upside, established for the chassis in
  product 2's research from two independent carrier documents.
- **The index mechanic ends at *Rentenbeginn***: the capital is fixed, the *Wahlrecht* lapses, and
  surplus in the *Rentenphase* is applied to the annuity in payment by whichever payout surplus
  system the contract uses. Whether any carrier offers index participation in payment is **not
  established**; gap 17.
- The ***Kapitalwahlrecht*** — taking the capital as a lump sum instead of the annuity, normally
  exercisable in a window before *Rentenbeginn* — applies unchanged, with the tax consequence in
  [R14].
- **`[std]` for delib**: a *garantierter Rentenfaktor* of **25,00 € per 10 000 € per month** at
  *Rentenbeginn* 67, taken over from product 2's `[std]`, with the current factor set equal to it in
  the base run so the max-of-two rule is exercised by a test rather than by the base path.

### 17. Decrements, underwriting and policyholder behaviour

- **Underwriting is light or absent**, the sum at risk before *Rentenbeginn* being close to zero, so
  the contract is normally issued on a short declaration or none `[unverified]`. The accumulation
  mortality basis matters little; the *Rentenphase* basis matters greatly and is **DAV 2004 R**, the
  generational annuitant table, documented in product 2's research.
- **DAV tables are the property of the Deutsche Aktuarvereinigung, are not public and are not
  redistributed in this library.** delib ships `[std]` proxies anchored so the worked example
  reproduces exactly, and says what a replacement must preserve.
- **Lapse.** No index-product-specific *Stornoquote* is established. The market-wide GDV measures
  recorded in the sibling file are of the order of **2,7 % on the main measure and 1,2 % per contract
  for 2024** `[unverified]`, and the two are not reconcilable from the available evidence. delib's
  lapse assumption is `[std]`, with the section-14 timing incentive noted as a model risk.
- **The election path is the behavioural assumption unique to this product** (section 4). Real
  policyholders in this product family are widely believed to be inert — to elect once at inception
  and never revisit — which if true makes the annual *Wahlrecht* far less valuable than its
  description suggests. **This is not established** and is flagged as `[unverified]`; delib's base
  run assumes full index participation in every year and treats the alternative as a sensitivity.

### 18. Taxation

- ***Schicht 3* annuity**: taxed on the *Ertragsanteil* only, by age at *Rentenbeginn* [R13] — about
  17 % of the annuity at age 67 `[unverified]`.
- **Lump sum under the *Kapitalwahlrecht***: the excess over premiums paid is investment income, and
  if the contract has run twelve years and the payment falls after age 62, **half the difference** is
  taxable at the personal rate, subject to the *Mindesttodesfallschutz* condition for contracts from
  1 April 2009 [R14]. All figures `[unverified]`.
- **The index credits are not separately taxed**: they are absorbed into the capital as credited, so
  there is no annual tax event, no *Abgeltungsteuer* on the year's index gain and no
  *Teilfreistellung* under the *Investmentsteuergesetz* — the last because there is no fund. This
  **tax deferral is one of the two genuine advantages over holding an index fund directly**, the
  other being the guarantee, and the product specification must state it alongside section 21.
- *Basisrente* and *Riester* wrappers change the tax treatment entirely (full deductibility of
  contributions and full taxation of the annuity; allowances and *Sonderausgabenabzug* respectively)
  and are documented under delib products 5 and 6.
- No German tax rule turns on the index mechanic itself. delib's model publishes gross cash flows and
  does not compute tax; the tax section of the product specification is context.

### 19. Two worked *Indexjahre* — constructed, `[std]` throughout

**The brief asked for a documented worked example of an *Indexjahr* from insurer material or the
consumer press, with the twelve monthly index movements and the resulting credit. One was found on
2026-08-30** — Allianz publishes two, for 2020/2021 and 2021/2022, and they are set out in full at
section 5 [S2]. **The examples below are nevertheless kept as they are, and remain constructed**:
they are the anchors of the delib worked example and of its golden tests, they run at delib's own
Cap of 3,00 % rather than Allianz's illustrative 3,2 %, and they carry a *Quote* comparison the
carrier's table does not. Every number in them is `[std]`, and they are not evidence about any
carrier or any year — for which read section 5. The relationship between the two is worth stating
plainly: **the carrier's table validates the mechanic these examples assert**, and re-running it
through the delib model at `cap = 0,032` would reproduce 15,90 % and 0 %. They are, however, arithmetically exact, and they are the pattern the delib
worked example and its tests should follow.

Common assumptions, all `[std]`: participating capital at the start of the *Indexjahr*
`G = 50,000.00 €`; monthly Cap `C = 3.00 %`; declared surplus rate (option budget) `b = 2.50 %`;
guaranteed rate `i_g = 1.00 %`; *Partizipationsquote* variant `q = 60 %`.

**Example A — a strong year. The cap costs 4,20 points and the year still credits well.**

| Month | Index return `r_m` (%) | Capped `x_m = min(r_m, 3.00)` (%) | Given away (%) |
|---|---|---|---|
| 1 | 1.80 | 1.80 | 0.00 |
| 2 | -2.40 | -2.40 | 0.00 |
| 3 | 4.60 | 3.00 | 1.60 |
| 4 | 0.90 | 0.90 | 0.00 |
| 5 | -3.70 | -3.70 | 0.00 |
| 6 | 2.20 | 2.20 | 0.00 |
| 7 | 3.40 | 3.00 | 0.40 |
| 8 | -1.10 | -1.10 | 0.00 |
| 9 | 0.40 | 0.40 | 0.00 |
| 10 | 5.20 | 3.00 | 2.20 |
| 11 | -0.80 | -0.80 | 0.00 |
| 12 | 2.60 | 2.60 | 0.00 |
| **Sum** | **13.10** | **8.90** | **4.20** |

- Sum of capped monthly returns `S = +8.90 %`; positive, so `Indexrendite = 8.90 %`.
- ***Indexgutschrift* = 8.90 % x 50,000.00 = 4,450.00 €**, credited and locked in.
- Cross-checks a reader can do with a calculator:
  - the **compounded** index return over the year is `prod(1 + r_m) - 1 = +13.4548 %`, against the
    **sum** of `+13.10 %` — the two differ by 0.35 points, which is the compounding effect the
    contractual formula does not give;
  - the cap bound in exactly three months and cost **4.20 points**, which is `13.10 - 8.90`;
  - the *sichere Verzinsung* arm would have credited `b x G = 2.50 % x 50,000.00 = 1,250.00 €`. The
    index arm therefore paid **3.56 times** the safe arm in this year;
  - the *Partizipationsquote* variant would have credited
    `max(60 % x 13.4548 %, 0) x 50,000.00 = 4,036.44 €` — **less** than the cap variant here,
    because the cap variant's give-up was concentrated in three months.

**Example B — the case the product is criticised for. The index rises 6,44 % and the credit is zero.**

| Month | Index return `r_m` (%) | Capped `x_m = min(r_m, 3.00)` (%) | Given away (%) |
|---|---|---|---|
| 1 | 6.50 | 3.00 | 3.50 |
| 2 | -2.10 | -2.10 | 0.00 |
| 3 | 5.80 | 3.00 | 2.80 |
| 4 | -1.90 | -1.90 | 0.00 |
| 5 | -2.40 | -2.40 | 0.00 |
| 6 | 4.20 | 3.00 | 1.20 |
| 7 | -3.10 | -3.10 | 0.00 |
| 8 | 0.60 | 0.60 | 0.00 |
| 9 | -2.80 | -2.80 | 0.00 |
| 10 | 5.10 | 3.00 | 2.10 |
| 11 | -1.70 | -1.70 | 0.00 |
| 12 | -1.20 | -1.20 | 0.00 |
| **Sum** | **7.00** | **-2.60** | **9.60** |

- Sum of capped monthly returns `S = -2.60 %`; negative, so `Indexrendite = max(-2.60 %, 0) = 0`.
- ***Indexgutschrift* = 0.00 €.** Nothing is credited, nothing is lost, the capital is untouched, and
  the year's surplus of 1,250.00 € has been spent on options that expired worthless.
- Cross-checks:
  - the **compounded index return for the year was `+6.4402 %`** and the sum of raw monthly returns
    was `+7.00 %` — **the index rose, and the credit was zero**;
  - the cap bound in four months and cost **9.60 points**, which is `7.00 - (-2.60)`;
  - the *sichere Verzinsung* arm would have credited **1,250.00 €**;
  - the *Partizipationsquote* variant would have credited
    `max(60 % x 6.4402 %, 0) x 50,000.00 = 1,932.06 €` — **more than the safe arm and infinitely more
    than the cap variant**, which is the cleanest possible demonstration that the two designs are not
    interchangeable.
- **This example is the delib pitfall test.** An implementation that floors each month at zero, or
  that compounds rather than sums, or that applies the floor to the compounded return rather than to
  the sum of capped returns, will credit something here. The correct answer is zero, and a test must
  assert it.

**The two years together.** On an unchanged base of 50,000.00 € the index arm credits
`4,450.00 + 0.00 = 4,450.00 €` and the safe arm `1,250.00 + 1,281.25 = 2,531.25 €` (the second
year's 2,50 % struck on 51,250.00 €) — the index arm ahead by **1,918.75 €**, entirely on the
strength of one year at three-and-a-half times the safe rate while losing the other outright. That
shape, a minority of large years carrying a majority of zero years, is the product's real return
distribution, and section 20 puts a number on it.

### 20. What the cap costs — an expected-value calculation, `[std]` throughout

The single most useful thing this file can supply downstream, given that no market cap level or
outcome distribution could be established, is the arithmetic that turns an assumed volatility and an
assumed cap into an expected credit. It is elementary and it is decisive.

**Assumptions, all `[std]`, and all of them exposed as parameters in the delib technical notes**:
monthly index returns independent and normally distributed; monthly mean `mu = 0.60 %` (an
arithmetic 7,2 % per year, a plausible real-world equity drift on a price index); monthly standard
deviation `sigma = 5.00 %` (an annualised 17,3 %, ordinary for a broad European equity index);
monthly Cap `C = 3.00 %`.

**Step 1 — what one month gives away.** With `d = (C - mu) / sigma = 0.48`:

```
E[ max(r - C, 0) ]  =  sigma x phi(d)  -  (C - mu) x (1 - Phi(d))
                    =  5.00 x 0.35551  -  2.40 x 0.31561
                    =  1.7776 - 0.7575  =  1.0201 %
```

**Step 2 — what one month is worth after the cap.**

```
E[ min(r, C) ]  =  mu - E[ max(r - C, 0) ]  =  0.60 - 1.02  =  -0.42 % per month
```

**Read that line twice.** With a 3 % monthly cap and a 17 % index, **the expected value of a capped
month is negative**, because the cap removes more expected return than the month has. The
policyholder's expected sum over the year is `12 x (-0.42) = -5.04 %`.

**Step 3 — what the annual floor is worth.** The floor is the only reason the product has a positive
expectation at all. With `Var[min(r, C)] = 13.62` per month and independence, `S` has mean `-5.04 %`
and standard deviation `sqrt(12 x 13.62) = 12.79 %`, and

```
E[ max(S, 0) ]  =  mu_S x Phi(mu_S / sigma_S)  +  sigma_S x phi(mu_S / sigma_S)
                =  -5.04 x 0.3467  +  12.79 x 0.36912
                =  -1.747 + 4.719  =  2.97 % per year

P( S <= 0 )     =  Phi( 5.04 / 12.79 )  =  0.65
```

**The three numbers to carry downstream**, all `[std]` and all conditional on the assumptions above:

| Quantity | Value | Meaning |
|---|---|---|
| Expected annual credit | about 2.97 % | what the index arm is worth per year |
| Probability of a zero year | about 65 % | roughly two years in three credit nothing |
| The safe arm | 2.50 % | what the same surplus credits with certainty |

- **The index arm's expected credit exceeds the safe arm's by a modest margin and does so with a very
  high probability of zero.** That is the product's true risk-return profile under these assumptions,
  and it is very far from how it is normally described. The excess over the safe arm is not free
  money: it is the **equity risk premium earned on the option package's delta**, and it is the only
  economic reason the index arm can be worth more than the safe arm at all (section 3).
- **A consistency check the delib technical notes must run, and which is instructive because it
  fails at these numbers.** Repeating the calculation under a risk-neutral drift on a price index —
  drift `r - q`, with a 2,5 % risk-free rate and a 3 % dividend yield, so `mu = -0.04 %` per month —
  gives an option-package value of the order of **1,7 % of `G`**. That is **below** the assumed
  option budget of 2,5 %, which means the assumed pair (`C = 3,0 %`, `b = 2,5 %`) is **not mutually
  consistent**: at that volatility, a 2,5 % budget would buy a cap somewhat **above** 3,0 %.
- **The instruction that follows is the important one.** A delib model must **calibrate the Cap to
  the option budget**, not choose the two independently, or it will publish a product that is either
  free money or a swindle depending on which way the inconsistency falls. The technical notes are
  required to state the calibration explicitly, to run it, and to report the calibrated cap beside
  the `[std]` 3,0 % headline.
- **Sensitivity, which is the real point**: volatility enters twice — it makes the cap bind more
  often, lowering the expectation, and it makes the floor worth more, raising it. At the 5 %
  annualised volatility of the house-index case (section 9) the cap almost never binds and the payoff
  approaches the index return; at 25 % the expected credit is dominated by the floor. **Any expected
  return quoted for this product without its volatility assumption is meaningless.**

### 21. Criticism of the product

Recorded as arguments, with their strength assessed. **Two of the four consumer publishers were
retrieved on 2026-08-30 and are quoted below** — Finanztip's 2016 press release [S12] and the
Verbraucherzentrale Hamburg's 2018 release [S14] — together with the carrier's own account of the
litigation that followed [S16]. *Finanztest* remains paywalled [S13] and nothing is taken from it.
Quoting a consumer body is not adopting its position; the arguments are still assessed here.

1. **The cap's effect on the expected credit is large and is not disclosed in a usable form.**
   Section 20 quantifies it: at ordinary equity volatility a 3 % monthly cap makes a capped month's
   expected value negative, and the product's positive expectation then rests entirely on the annual
   floor. The purchaser is told the cap, is not told the volatility, and cannot do the calculation.
   **This is the strongest criticism and it is structural, not a matter of any carrier's conduct.**
2. **Negative months are uncapped, and that is genuinely counter-intuitive.** A symmetric-sounding
   description — the index's monthly moves, up to 3 % a month — conceals an asymmetry running
   entirely one way. Example B in section 19 is the demonstration: the index rose 6,44 % and the
   credit was zero. **This is the feature most often misdescribed in secondary material** — and
   **the insurer's own published example makes the point better than this file's constructed one**:
   in the *Indexjahr* 2021/2022 the capped monthly sum was −26,96 % and the credit 0 %, while the
   EURO STOXX 50 fell 14,89 % point to point [S2]. The Verbraucherzentrale Hamburg put the same
   asymmetry as its central complaint: the annual outcome can fall short of the index "selbst dann
   …, wenn der Cap in der Jahresbetrachtung gar nicht überschritten wird" [S14].
3. **Against a direct index investment the product loses on every axis but two.** A total-return
   index fund receives the dividends (some 3 % per year on euro-area equity `[unverified]`), has no
   cap, no participation rate and charges of a few basis points; the Indexpolice gives up the
   dividends, gives up the tail of every good month, and adds acquisition, administration and
   possibly index-level costs. **What it gives back is real**: the capital cannot fall, credits lock
   in permanently, the guarantee is the insurer's, and the accumulation is tax-deferred with a
   favourable exit [R14]. A fair statement puts both sides and the product specification must.
4. **The Cap is redetermined annually at the insurer's discretion**, so the purchaser signs a
   contract whose economic terms for year 12 will be set by the counterparty. § 315 BGB [R22]
   constrains that in principle; **no decided case tests it** (gap 16), and **neither retrieved AVB
   contains a *Mindest-Cap*** (gap 10). The one point the AVB do settle in the policyholder's favour
   is that the parameters are announced **before** the election deadline ([S2] Ziffer 3.1), so the
   discretion is exercised before the choice is made rather than after it.
   **The litigation, and it was not about this.** The Verbraucherzentrale Hamburg sued Allianz under
   the UWG over how IndexSelect was advertised, arguing that "Beteiligung an der Wertentwicklung des
   EUROSTOXX 50" and "Indexpartizipation" mislead because the participation runs "nicht über die
   eingezahlten Beiträge, sondern ausschließlich über die … jährlich zu ermittelnde
   Überschussbeteiligung" — which is section 3's financing identity, put as a complaint. It won at
   first instance (LG München I, 23.03.2018, Az. 37 O 12326/17) and lost on appeal, the OLG München
   dismissing the claim on 04.04.2019 with no *Revision* admitted [S14][S16]. **No court has reviewed
   a *Cap-Festlegung*.**
5. **The move to house indices moved the give-up out of sight** (section 9): a high participation
   on a volatility-targeted excess-return index with an embedded fee is not obviously better than
   55 % of the EURO STOXX 50, and is much harder to evaluate. **The retrieved evidence supports the
   opacity and undercuts the "near-100 %" premise**: two house indices are named ([S7] SOMAS, [S8]
   M-A-X) and **neither publishes a volatility target or an index-level fee**, while the one
   published house-index quota is **70 %** [S8] — lower than Allianz's 75,00 % illustration on the
   EURO STOXX 50 [S2].
6. **Complexity is itself a defect.** A retail product whose payoff requires a strip of capped
   monthly returns, an annual floor, an option budget financed by a discretionary declaration and an
   annual election is one most purchasers cannot evaluate — Finanztip: "Verbraucher können oft nicht
   wirklich nachvollziehen, was sie da eigentlich kaufen" [S12]. It is a conduct concern in BaFin's
   value-for-money terms [R16][R17], though the *Merkblatt* addresses cost rather than comprehensibility
   and does not name index products at all [R16]. **The German courts have looked at the point and
   split**: the LG München I held the advertising misleading in 2018, the OLG München held it was not
   in 2019 [S14][S16]. It is the reason this product above all deserves a mechanically exact
   reference implementation.
7. **The counter-argument, fairly stated.** The relevant benchmark for most purchasers is not an
   index fund but the *sichere Verzinsung* arm of the same contract. Against that, the index arm has
   a higher expected value (section 20), cannot do worse than zero in any year, costs nothing extra,
   and can be abandoned at any anniversary. On that comparison the product is defensible.

### 22. Typical parameter levels

**Every level in this section was `[unverified]` or `[std]` when it was written; the Basis column
now records which of them a retrieved document reaches.** Six are placed against carrier or survey
figures on 2026-08-30; the rest remain this author's assessment of the plausible market band and
stay `[unverified]`. The `[std]` column is what the delib reference implementation uses, and **no
value in it has been changed** — these are shipped inputs behind a worked example and golden
tests.

| Parameter | `[std]` for delib | Plausible market range | Basis for the choice |
|---|---|---|---|
| Monthly Cap | 3.00 % | 1.5 % – 5.0 % `[unverified]` | midpoint of the band; must be calibrated to the budget (section 20). **Allianz's own illustration runs at 3,2 %** [S2][S5]; no market panel [R21] |
| *Partizipationsquote*, equity price index | 60 % | 50 % – 80 % `[unverified]` | midpoint. **Allianz illustrates 75,00 %** [S2], so the shipped rate is low |
| *Partizipationsquote*, house multi-asset index | 100 % | 80 % – 120 % `[unverified]` | the design's selling point (section 9). **Stuttgarter publishes 70 %** on its M-A-X index [S8], below the band and well below the shipped rate |
| Declared surplus rate = option budget `b` | 2.50 % | 2.0 % – 3.0 % | **below the 2026 evidence**: Assekurata gives the index segment **3,07 %** and classic private annuities 2,62 % [R20]; Stuttgarter publishes 2,16 % for its own safe arm [S8] |
| Guaranteed rate `i_g` | 1.00 % | 0.25 % – 1.00 % by cohort | the *Höchstrechnungszins* for 2025–2026 [R7][R18] |
| *Garantieniveau* (*Beitragsgarantie*) | 90 % of *Beitragssumme* | 80 %, 85 %, 90 % observed; 60 % `[unverified]` | **the modal retrieved level**: Allianz 90 % / 80 % [S4], R+V 90 % [S7], Stuttgarter 85 % [S11]; 100 % is statutory for *Riester* [R12] |
| Index volatility (annualised) | 17.3 % | 15 % – 22 % equity; 5 % – 8 % house index `[unverified]` | section 9 and section 20. **No volatility target is published for either named house index** [S7][S8] |
| Dividend yield forgone (price index) | 3.0 % | 2.5 % – 3.5 % | euro-area equity; section 9 |
| *Beitrag* | 200.00 € per month | 50 € – 1,000 € | a plausible mass-market monthly savings premium |
| *Eintrittsalter* | 40 | 25 – 55 | mid-career, the segment this product is sold into |
| *Rentenbeginn* | 67 | 62 – 70 | the German statutory retirement age; 62 is the tax boundary [R14] |
| *Aufschubdauer* | 27 years | 12 – 40 years | 12 is the tax minimum [R14]; 27 follows from 40 to 67 |
| *Rentenfaktor*, guaranteed | 25.00 € per 10,000 € per month | **25,74 € published** for one index tariff | inherited `[std]` from delib product 2, and within 3 % of Stuttgarter's disclosed guaranteed factor [S11] |
| *Abschlusskosten* | 2.5 % of *Beitragssumme* | ceiling 25 ‰ [R7]; **2,50 % charged by both retrieved carriers** | at the *Höchstzillmersatz*, and equal to Allianz's "2,5% der kumulierten Anlagen" [S4] and Stuttgarter's 2,50 % of premiums [S11] |
| *Verwaltungskosten* | 3 % of premium + 0.25 % of reserve p.a. | **below both retrieved carriers** | inherited `[std]`; Allianz charges 3,5 % of the payment + 1,0 % of value p.a. + 0,1 % transaction costs [S4], Stuttgarter 9,00 % of premiums + 0,04 % of capital monthly [S11] |
| *Ratenzahlungszuschlag* | 5 % monthly | 2 % / 3 % / 5 % | market convention `[unverified]` |
| *Stornoabzug* | 2 % of *Deckungskapital* | 0 % – 20 % | inherited `[std]`; observed range at [R2] discussion |
| *Stornoquote* | 3 % per year, level | **2,56 % (2023), 2,51 % (2022)**, all *Hauptversicherungen* by count | inherited `[std]`; the GDV publishes one undifferentiated number with no product or duration split, and **no index-specific rate exists** [R19] |
| *Wahlrecht* election `w` | 1.00 (full index) every year | 0.00 – 1.00 | the product exists to demonstrate the index arm |

- **The one parameter that cannot be chosen freely is the Cap**, being determined by the budget
  (sections 3, 8, 20): delib's 3,00 % is the headline, the calibrated value is what the model must
  use, and the technical notes must publish both. Both retrieved AVB say the same in their own words,
  the Cap and the *Beteiligungsquote* being set on quotes from banks given the surplus, the
  *Bewertungsreserven* share and market volatility [S2] Ziffer 3.3 Absatz 2 b), [S7] § 3 Ziffer 4.
  **The *Eintrittsalter*, the *Beitrag* and the term remain pure `[std]` construction**, but no
  longer for want of any published envelope: [S11] publishes a complete one (100 € a month, 30 years,
  age 37 → 67) and [S4] Allianz's model case and term menu. What no carrier publishes is an
  entry-age band or a minimum premium. Gap 5, narrowed.

### 23. Market context

- **No industry figure for the size of the German index-participation segment exists**, and reading
  the GDV's *Die deutsche Lebensversicherung in Zahlen 2024* confirms why: the in-force split has no
  index line and the word "Index" occurs nowhere in its forty pages except its own table-of-contents
  index, because these contracts are counted within conventional annuity business [R15][R19]. **The
  only counts available are one carrier's own press statements** — Allianz reported 400.000
  IndexSelect contracts in October 2016 [S12] and "über 500.000" in May 2019 [S16]. Those are a
  single carrier's marketing figures, not a market statistic. Gap 8.
- What can be said qualitatively, and is not in doubt: the product family emerged in the second half
  of the 2000s, grew through the low-interest decade as the guaranteed component of a conventional
  contract shrank towards nothing [R7], became a standard offering across the large and mid-sized
  carriers, and was one of the main vehicles of the ***Neue Klassik*** generation of designs that
  replaced the annually-accruing guarantee with a *Rentenbeginn* guarantee [S6].
- **The rise in interest rates from 2022 and the *Höchstrechnungszins* increase to 1,00 % for 2025
  changed the product's relative position** [R7][R18]: a larger guaranteed component makes the safe
  arm of the *Wahlrecht* more attractive and reduces the pressure that created the product. Whether
  index tariffs have lost share as a result **is not established** `[unverified]`.
- **Carrier inventory.** Three products are now **established from carrier documents** — **Allianz
  Zukunftsrente IndexSelect (Plus)** [S2], **R+V-PrivatRente IndexInvest** (tariff IL55) [S7] and
  **Stuttgarter index-safe** [S8][S11] — and the tags come off. Allianz's release dates its own
  product to a 2007/2008 launch [S16], and the module appears on the *Zukunftsrente*, *KinderPolice*
  and *StartPolice* chassis in its own catalogue [S4]. **The rest of the inventory the brief asked
  for still could not be assembled**: for the other twenty-three named carriers this file cannot say
  whether they write the product, and inventing names would be worse than admitting it. Gap 2,
  narrowed to the inventory.

### 24. What a projection model needs, and what this file supplies

| The model needs | Status | Where it comes from |
|---|---|---|
| Contract chassis (premium, reserve, death benefit, surrender, paid-up, annuitisation) | established | delib product 2, inherited unchanged |
| The payoff formula `max(sum of min(r_m, C), 0) x G` | **established**, structurally certain | section 5 |
| The annual lock-in and the guarantee architecture | **established** | sections 6, 11 |
| The financing identity between surplus and option budget | **established** | section 3 |
| The annual *Wahlrecht* as a policyholder election | **established** as a mechanic | section 4 |
| The Cap level | **not established** — `[std]` 3,00 %, band 1,5–5,0 % | sections 8, 22 |
| The declared surplus rate | **not established** — `[std]` 2,50 % | sections 3, 22 |
| The *Garantieniveau* | **not established** — `[std]` 90 % | sections 11, 22 |
| The base `G` of the participation | **not established** — `[std]` whole capital at year start | section 5 |
| The mid-year exit treatment | **not established** — `[std]` no credit in the year of exit | sections 5, 14 |
| Charges, lapse rates, entry age, premium, term | **not established** — all `[std]` | sections 13, 17, 22 |
| A real *Indexjahr* to reproduce | **not established** — constructed | section 19 |

**The design recommendation this research leads to.** Because no real *Indexjahr* could be obtained,
the delib model must **not** model the index credit as an assumed rate. It should **implement the
contractual formula literally against an explicit table of monthly index returns supplied as an
external CSV** beside the model — one row per projection year, twelve monthly-return columns, the
`provenance` column recording the path as `[std]` — and cap, sum, floor and credit each year from it.
That way the mechanic is reproduced exactly rather than approximated; the worked example of section
19 becomes the anchor cell and is asserted cell by cell; the Example B pitfall (index up, credit
zero) becomes a test rather than a remark; every unestablished level stays a visible `[std]`
parameter instead of being buried in an assumed credit rate; and the volatility sensitivity of
section 20 is demonstrable by swapping the CSV. That was the strongest thing this file could hand
downstream while it had no research channel: not the numbers it could not obtain, but the exact
arithmetic those numbers would have gone into. The retrieval pass of 2026-08-30 has since supplied
two carriers' clause wording and two published parameter sets for that arithmetic to be run
against; it did not supply a monthly index series, so the CSV design stands.

---

## Observed variation across insurers

**This table is now a comparison rather than a record of what could not be compared.** Two carrier
AVB were retrieved in full [S2] [S7] and Stuttgarter's published product documents and current
parameters were read, though **its AVB is not published** and its column is correspondingly thin
[S8] [S11]. A cell reading "not established" now means exactly that.

| Feature to compare | Allianz [S2][S4][S5] | R+V [S7] | Die Stuttgarter [S8][S11] | Anyone else | delib `[std]` |
|---|---|---|---|---|---|
| Index AVB located | **yes**, E25, ed. 12/2025 | **yes**, IL55, Stand 01.07.2025 | no (AVB unpublished) | no | composite [S1] |
| Product name | **Zukunftsrente IndexSelect (Plus)** | **PrivatRente IndexInvest** | **index-safe** | not established | n/a |
| Payoff design (Cap / Quote / both) | **monthly Cap *and* a *Partizipationssatz* on the capped sum** | ***Beteiligungsquote* on the year return; no cap** | **quota on the year return; no cap** | not established | Cap, Quote as variant |
| Cap / quota level, current | Cap **3,2 %**, *Partizipationssatz* **75,00 %**, both illustrative | not published | *Partizipationsquote* **70 %** (Turbo 120 % / 172 %), 1.2.2026–31.1.2027 | not established | 3,00 % monthly; `q` 60 % / 100 % |
| *Mindest-Cap* guaranteed | **none in the AVB** | **none in the AVB** | not established | not established | none |
| Underlying index | EURO STOXX 50; S&P 500 with a *Währungsfaktor* | **SOMAS** (Solactive Multi Anlage Stabil) | **M-A-X Multi-Asset**; *Grüne Zukunft* | not established | generic, by volatility |
| *Wahlrecht* notice period | **7 days** before the *Indexstichtag*; splits in 25 % steps | **7 days** before the *Versicherungsjahrestag* | annual | not established | annual, at year end |
| Cap announced before the election deadline | **yes**, parameters notified ≥ 3 weeks before | **yes**, "rechtzeitig vor Beginn" | quota published in advance | not established | assumed yes — **correct** |
| Base `G` of the participation | **the *Policenwert* at the start of the *Indexjahr***, ex that year's premiums | **the *Policenwert* present the whole year**, ex that year's premiums | not stated (the *budget* is 100 % of *laufende Überschüsse*) | not established | whole capital at the year start |
| *Garantieniveau* choices | **90 %**; 80 % for IndexSelect Plus | **90 %** | **85 %** (*BasisRente* variant) | not established | 90 % |
| Mid-year exit treatment | **no index credit**; pro-rata *Schlussüberschuss* + *Sockelbetrag* only | **no index credit** | not established | not established | no credit |
| Charges / *Effektivkosten* | **1,6 % a year** over 30 years; entry 2,5 % of cumulative payments | not retrieved | **1,80 points**; entry 2,50 % of premiums | not established | `[std]`, section 13 |
| *Indexjahr* aligned with the policy year | **not necessarily** | **yes** | **no** — a common 1.2.–31.1. window | not established | aligned |

Parameter bands, restated. Two rows are now placed against carrier figures; the rest remain this
author's assessments and `[unverified]`, which is why section 22 exists:

| Parameter | Band | Who sits where |
|---|---|---|
| Monthly Cap | 1,5 % – 5,0 %, typically 2,5 % – 4,0 % `[unverified]` | Allianz illustrates **3,2 %**; 3,3 % recorded in 2018 [S14]; **no panel** [R21] |
| *Partizipationsquote* | 50 % – 80 % equity; 80 % – 120 % house index `[unverified]` | Allianz illustrates **75,00 %** on equity; Stuttgarter publishes **70 %** on a house index — **below the band** |
| *Garantieniveau* | 80 % / 85 % / 90 % observed; 60 % and 100 % `[unverified]` | Allianz 90 % / 80 %, R+V 90 %, Stuttgarter 85 %; 100 % statutory for *Riester* [R12] |
| Declared surplus rate 2026 | **3,07 % index segment**; 2,62 % Klassik; 2,65 % Neue Klassik | Assekurata survey averages [R20]; Stuttgarter publishes 2,16 % [S8] |
| *Höchstrechnungszins* by cohort | 0,25 % (2022–2024) – 4,00 %; **1,00 % from 2025**, recommended again for 2027 | market-wide [R7][R18] |
| Underlying | EURO STOXX 50 and S&P 500 at Allianz; house multi-asset indices at R+V and Stuttgarter | **all three placed**; no volatility target or index fee published for either house index |

**Representative design the research supports.** A single-life *Schicht 3* deferred annuity, capital
in the *Sicherungsvermögen*, guaranteed at the 1,00 % *Höchstrechnungszins* with a **90 %
*Beitragsgarantie* falling due at *Rentenbeginn*** and no annually accruing guarantee beyond the
technical rate; the annually declared *Überschuss* spent, at the policyholder's **annual election**,
as an **option budget** buying a one-year index participation; the credit computed as the **sum of
twelve monthly index returns each capped at a monthly Cap, with negative months entering in full,
floored at zero**, applied to the accumulated capital at the start of the *Indexjahr*; the credit
**locked in permanently** into the guaranteed capital; a *Partizipationsquote* design available as a
switchable variant; conversion at *Rentenbeginn* at the **greater of the guaranteed and the current
*Rentenfaktor***; *Rückkaufswert* and *Beitragsfreistellung* on the ordinary § 169 / § 165 VVG
footing, with **no index credit in the year of exit**. Every level in that design is `[std]` and is
listed in section 22.

---

## Gaps and caveats

This register was written under the old retrieval conditions and is **re-adjudicated here against
the documents retrieved on 2026-08-30**. Each item says what it now stands at: **closed**, **narrowed**
or **open**. Numbering is frozen; nothing is dropped.

1. **CLOSED for two carriers.** Two index *Bedingungswerke* are in hand — Allianz *Zukunftsrente
   IndexSelect (Plus) E25*, edition 12/2025 [S2], and R+V *IndexInvest-Rentenversicherung* IL55,
   Stand 01.07.2025 [S7]. Between them they settle the *Indexjahr* definition, the observation dates,
   the payoff wording, the base of the participation, the *Wahlrecht* timing and notice period, the
   *Cap-Festlegung* clause and the *Ersatzindex* clause. **Open residue**: Stuttgarter publishes no
   AVB, and no wording outside these three carriers was seen.

2. **CLOSED.** Three product names are established from carrier documents: **Allianz Zukunftsrente
   IndexSelect (Plus)** [S2], **R+V-PrivatRente IndexInvest** (tariff IL55) [S7] and **Stuttgarter
   index-safe** [S8] [S11]. The tags come off. **Open residue**: the brief named twenty-six carriers,
   and for the other twenty-three this file still cannot say whether they write the product. No
   downstream document may add a fourth.

3. **NARROWED.** Two levels are on record: Allianz's own worked illustration at a **Cap of 3,2 %**
   with a *Partizipationssatz* of **75,00 %**, expressly exemplary [S2] [S5], and Stuttgarter's
   **published** *Partizipationsquote* of **70 %** (Turbo 120 %, Turbo Plus 172 %) for all
   *Indexstichtage* from 1.2.2026 to 31.1.2027 [S8]. The 2018 litigation records a cap of 3,3 % then
   in force [S14]. **Open residue, and it is the substantive one**: no **panel** — a single year's
   levels across named carriers side by side — was found [R21], so the 1,5–5,0 % band remains this
   author's recollection and `[unverified]`, and delib's 3,00 % remains `[std]`.

4. **CLOSED, from the insurer rather than the policyholder.** Allianz publishes two worked
   *Indexjahre* on the EURO STOXX 50 at Cap 3,2 % and *Partizipationssatz* 75,00 %: 2020/2021 with
   twelve monthly movements summing to **15,90 %** and crediting **11,92 %** against a point-to-point
   index gain of 43,69 %, and 2021/2022 summing to **−26,96 %** and crediting **0 %** [S2].
   **Open residue**: no real contract's *Standmitteilung* was obtained [S10], and the GDV's nine
   *Muster-Standmitteilungen* contain no index variant, so the two examples in section 19 stay
   **constructed** and `[std]` in every cell.

5. **NARROWED.** [S11] publishes a complete envelope for one carrier — 100,00 € a month for 30 years
   from age 37 to 67, 85 % *Garantieniveau*, a guaranteed *Rentenfaktor* of **25,74 € per 10.000 €**
   and *Effektivkosten* of 1,80 points — and [S4] gives Allianz's model case, its 12/20/30/40-year
   term menu and its 80 %/90 % *Garantieniveau* menu. **Open residue**: entry-age bands and minimum
   premiums are published by no carrier reached here, and [S3]'s document class does not exist for
   this product at all.

6. **NARROWED, and delib's acquisition charge is confirmed.** Both [S4] and [S11] disclose
   *Abschluss- und Vertriebskosten* of **2,50 % of premiums** — delib's `[std]` value exactly, at the
   DeckRV § 4 ceiling — with total cost disclosed at 1,6 % a year [S4] and 1,80 points [S11]. `β` and
   `γ` remain `[std]` and are **below** both carriers' levels. **Open residue**: the three
   index-specific give-ups — dealing spread inside the Cap, index-level fee inside a house index,
   volatility-target drag — are still **structurally invisible in any disclosure**, though [S2]
   Ziffer 3.3 Absatz 2 b) at least names the *Dividendenrendite* as a determinant of the Cap.

7. **CLOSED.** The Stuttgarter *Muster-Produktinformationsblatt* for *BasisRente index-safe* (Tarif 69
   mit Turbo Plus, LZ30, Stand 01.01.2026, *Zertifizierungsnummer* 006604) was retrieved [S11]. It
   carries **Chancen-Risiko-Klasse 4**, *Effektivkosten* of 1,80 points, the full envelope and the
   itemised charges. **It also contradicts this file**: the CRK is 4, not the low class section 22
   guessed for a product with a guarantee and a bounded upside.

8. **OPEN, and now documented as such.** The GDV's *Die deutsche Lebensversicherung in Zahlen 2024*
   was read: the in-force split has no index line and the word "Index" occurs nowhere in its forty
   pages except its own table-of-contents index [R19]. The only counts available are one carrier's
   press statements — 400.000 in 2016 [S12], over 500.000 in 2019 [S16]. Any statement about the
   segment's size or movement stays `[unverified]`.

9. **NARROWED.** Two participation levels are observed — 75,00 % illustrative on an equity index
   [S2] and **70 % published** on a house multi-asset index [S8]. The second sits **below** this
   file's 80–120 % band for a house index, which is a caution against the volatility-target argument
   in section 9. The bands themselves remain this author's assessment and `[unverified]`.

10. **CLOSED, negatively.** **Neither retrieved AVB contains a *Mindest-Cap* clause or a minimum-budget
    promise.** Both instead carry the opposite provision: the participation is **excluded** for a year
    in which the *Policenwert* does not exceed the *Deckungsrückstellung* required for the guarantee
    ([S2] Ziffer 3.5, [S7] § 2 Ziffer 1). delib's assumption of neither is right, and the reason is
    stronger than assumed.

11. **CLOSED, in delib's favour.** Allianz notifies the *Caps*, the *Partizipationssatz*, the year's
    surplus net of *Verwaltungskosten* and the *Bewertungsreserven* *Sockelbetrag* "spätestens
    3 Wochen vor dem Indexstichtag", and the election is due "spätestens 7 Tage" before it [S2]
    Ziffer 3.1; R+V informs "rechtzeitig vor Beginn eines Versicherungsjahres" and takes the election
    up to 7 days before [S7] § 2. **The Cap is announced before the election deadline**, so the annual
    election is informed. Allianz's default on silence is not neutral, however: it rolls the previous
    split over only if index participation was at least 50 %, and otherwise moves the contract **to**
    50 % [S2] Ziffer 3.2 — a nudge delib does not model.

12. **CLOSED, and delib's `[std]` is the carriers'.** The participation is credited only "zu Beginn
    des folgenden →Indexjahres" ([S2] Ziffer 3.3, [S7] § 3 Ziffer 5); R+V's *Bezugsgröße* is by
    definition the value present for the whole year; and on surrender Allianz adds only a pro-rata
    *Schlussüberschussanteil* and *Sockelbetrag* [S2] Ziffer 9.2 Absatz 4. **No pro-rata index credit,
    no refund of the unspent budget** [R2]. The lapse-timing incentive in section 14 stands.

13. **OPEN.** Neither retrieved AVB reproduces a *Modellrechnung*, and the *Versicherungsinformationen*
    that would carry it is contract-specific and unpublished [R5] [S3]. The prescribed three rates are
    now exact — *Höchstrechnungszins* × 1,67, ±1 point, so 1,67 % / 2,67 % / 0,67 % at 1,00 % — but
    how a carrier applies them to a payoff mediated by the option budget and the Cap is not known.

14. **CLOSED, negatively.** The DAV *Ergebnisbericht* "Ein Standardverfahren für PRIIP der Kategorie 4"
    of 1 July 2025 was retrieved [R11]. It supplies the Category 4 rule (Ziffer 7 Anhang II RTS) and a
    capital-market model aligned with the PIA standard, and it says **nothing specific about
    index-participation mechanics** — so how a German Indexpolice's disclosed scenarios treat a cap or
    a quota is not derivable from it.

15. **CLOSED, negatively.** BaFin's *Merkblatt* 01/2023 (VA) was read in full [R16]: **the word
    "Index" does not occur in it.** It bites on an Indexpolice as a *kapitalbildendes
    Lebensversicherungsprodukt* and makes the *Effektivkosten* the measure of cost. *Risiken im Fokus
    2026* adds a threshold — *Effektivkosten* "über vier Prozent" make an appropriate customer benefit
    "zweifelhaft" [R17] — and names high early-duration lapse as a second indicator.

16. **OPEN on the point, but the litigation is not what this entry assumed.** German litigation over
    an Indexpolice exists and was retrieved: the Verbraucherzentrale Hamburg sued Allianz under the
    UWG over the IndexSelect web advertising and won at first instance (LG München I, **23.03.2018,
    Az. 37 O 12326/17**, *nicht rechtskräftig*), and the **OLG München dismissed the claim on
    04.04.2019** with no *Revision* admitted [S14] [S16]. That was about **how the participation was
    described**, not a § 315 BGB review of a cap determination, so **no decided German case on the
    *Cap-Festlegung* itself is known** [R22]. Likewise none on an *Ersatzindex* substitution.

17. **CLOSED for one carrier.** Allianz's participation runs "**vor Beginn der Rentenzahlung**" only
    [S2] Ziffer 3.3, so the *Wahlrecht* lapses at *Rentenbeginn*, as delib assumes. Whether any other
    carrier offers it in the *Rentenphase* is still not established.

18. **CLOSED on the level convention, and it turns out to vary on the alignment.** Monthly movements
    are "die prozentuale Veränderung des Index zwischen 2 Bewertungsstichtagen" [S2] Ziffer 3.3
    Absatz 2 a) and R+V's *Bewertungsstichtag* is "der letzte Börsentag eines Versicherungsjahres in
    Frankfurt am Main" [S7] § 3 Ziffer 3 — **closing levels, no averaging**, so the Asian reading is
    ruled out and the fair-Cap question with it. **The alignment does vary**: R+V's *Indexjahr* is the
    *Versicherungsjahr*, Allianz's need not be ([S2] Ziffer 3.5), and Stuttgarter runs a common
    1.2.–31.1. window for all contracts [S8]. delib's alignment with the policy year is R+V's rule and
    a simplification against the other two.

19. **CLOSED, and delib's reading is the carriers'.** "Bezugsgröße für die →Indexpartizipation ist
    der →Policenwert zu Beginn des →Indexjahres" [S2] Ziffer 3.3 Absatz 2 e), excluding that year's
    premiums and *Zuzahlungen*; [S7] § 3 Ziffer 2 to the same effect. The whole capital at the year
    start — not a sub-account, not the accumulated *Überschussguthaben*. This was the file's largest
    unquantified uncertainty; it is no longer one.

20. **OPEN.** No within-year monthly *Höchststandsicherung* appears in either retrieved AVB, which is
    consistent with this entry but is not positive evidence about the rest of the market. delib
    implements the annual lock-in only.

21. **CLOSED on the names, OPEN on the parameters.** Two German house multi-asset indices are named
    from carrier documents: the *Solactive Multi Anlage Stabil Index* (**SOMAS**), built for R+V by
    Solactive [S7], and the *Stuttgarter M-A-X Multi-Asset Index*, beside a *Stuttgarter Grüne Zukunft
    Index* [S8]. **No rulebook, volatility target or fee level is published for either**, so section
    9's 5 % target and 0,5–1,5 % embedded fee remain `[unverified]` and no index is named in any
    shipped delib input file.

22. **CLOSED, and the previous guess was wrong.** Both *Ersatzindex* clauses operate **without a
    *Treuhänder*** and **without a *Sonderkündigungsrecht***: Allianz may replace an index on material
    changes it is not responsible for, with effect from the next *Indexjahr*, and may exclude the
    participation entirely if it cannot ([S2] Ziffer 3.7); R+V replaces the index at the next
    *Indexstichtag* with one that "dem zu ersetzenden Index weitestgehend entspricht", at no cost, and
    lets the policyholder decide whether to continue ([S7] § 3 Ziffer 11). R+V also carries a
    **suspension** clause delib does not model (§ 3 Ziffer 10). The *Treuhänder* does appear in a
    retrieved AVB, but on the ***Rentenfaktor***: Allianz must bring one in where no comparable
    annuity is on sale at *Rentenbeginn* [S2] Ziffer 1.

23. **SUPERSEDED.** This file now quotes retrieved statutory and contractual wording where a short
    exact quotation earns its place, attributed to the instrument with its `Stand` or to the carrier
    with its edition. Sixteen statutory sections were read as canonical XML and eleven documents as
    PDF or HTML. What remains unquoted is what remains unretrieved, and each entry says which.

24. **Living texts.** The VVG, the DeckRV, the MindZV, the VAG, the AltZertG, the EStG and the PRIIPs
    delegated regulation all change, and each entry above now records the `Stand` it was read at. The
    *Höchstrechnungszins* is **1 Prozent** under DeckRV § 2 Abs. 1 (Stand: 19.7.2024), was 0,25 % from
    2022 to 2024, and the DAV recommends 1,0 % again for 2027 [R7] [R18]. Every date, rate and
    paragraph number must still be re-checked against the instrument before it is relied on. **A delib
    citation is a pointer to a document; where the entry says `Retrieved: yes`, it is also a record
    that this author opened it.**
