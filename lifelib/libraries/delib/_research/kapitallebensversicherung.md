# Kapitalbildende Lebensversicherung (endowment) — research notes (Germany)

Research notes for the German individual *kapitalbildende Lebensversicherung* — the classic
endowment contract that pays a guaranteed *Erlebensfallleistung* (survival benefit) at the
*Ablauf* (maturity) if the *versicherte Person* is alive, and a *Todesfallleistung* (death
benefit) if she dies before it, with both benefits increased by the *Überschussbeteiligung*
(participation in the insurer's surplus). It is the historic core product of the German life
market and the purest carrier of the *Überschussbeteiligung* machinery that the other nine delib
products reuse in modified form.

**In scope.** The individual, privately-written, *klassisch* (conventional, general-account)
endowment on a single life, with a level *Beitrag* payable over the whole term or over a shorter
*Beitragszahlungsdauer*, priced at a *Rechnungszins* not exceeding the *Höchstrechnungszins*,
reserved by a *gezillmerte* prospective *Deckungsrückstellung*, carrying a contractual
*Rückkaufswert* under § 169 VVG and a *Beitragsfreistellung* right under § 165 VVG. Both the
*gemischte Versicherung auf den Todes- und Erlebensfall* (the pure endowment-with-death-cover
form) and its close relatives with an unequal death and survival sum are treated as one chassis
parameterised by the ratio of the two benefits.

**Out of scope, and said so where it matters.** *Risikolebensversicherung* (term life, delib product
8) has no survival benefit and no *Deckungskapital* to speak of; *klassische Rentenversicherung*
(product 2) is the same *Überschussbeteiligung* chassis with an annuity rather than a lump sum at
*Ablauf*; *fondsgebundene Lebensversicherung* (product 3) is a unit-linked contract whose
*Rückkaufswert* is a *Zeitwert* of fund units, not a *Deckungskapital*. *Sterbegeldversicherung*,
*betriebliche Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung* and *private
Krankenversicherung* are outside the delib library entirely. Austrian and Swiss documents are
excluded even where a search returned them, because the VVG, the DeckRV and the MindZV do not apply
to them; one such document is recorded below only so a later reader does not mistake it for a
German source.

These notes are the **citation ground truth** for the delib `kapitallebensversicherung` product
documents. Source ids **S1..S18** and **R1..R31** below are **frozen — never renumber**; unused ids
are simply omitted downstream, leaving gaps, and `sources.md` records which are absent and why.
Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

This section has two halves. The first records how the research was **done**, on 2026-08-29, when
egress was blocked and everything rested on search summaries; the second records what the
**re-verification** of 2026-08-30 established once the policy was lifted. The first is kept because
it explains why so much of this file is written the way it is; the second is what a reader should
weigh each entry by.

**No document in this file had been retrieved when it was written.** Direct HTTP egress from the
build environment was blocked by an organisation network policy: `WebFetch` and `curl` were refused
(HTTP 403 at the egress gateway) for every host outside a short package-registry allowlist. The hosts that matter for this
product were all tried and all refused — `gesetze-im-internet.de`, `bafin.de`, `gdv.de`,
`aktuar.de`, `bundesfinanzministerium.de`, `dejure.org`, `buzer.de`, `destatis.de` and
`de.wikipedia.org`. Not one PDF of a *Bedingungswerk*, not one *Basisinformationsblatt*, not one
statutory text and not one BaFin *Merkblatt* was opened.

**Everything in the first draft rested on `WebSearch` result summaries.** The tool returns titles,
URLs and a search-engine summary of the matched pages — real evidence that does return substantive
content (several long German sentences of statutory text reproduced below came back that way), but a
*secondary summary*, never a retrieved document. Two consequences followed, stated on every source
block as drafted:

1. Every source recorded `Retrieved: no — direct HTTP egress blocked in the build environment;
   established from search-result summaries`. Where a German sentence appeared in quotation marks,
   **the quotation was of the search-result summary, not of the instrument**: it was not a verbatim
   reading of § 169 VVG, it was what the summary reported § 169 VVG to say. **This is the rule the
   re-verification changed**, and the entries now say per block which of the two a quotation is.
2. The tool **fuses several result pages into one prose summary and does not attribute each sentence
   to the URL it came from**. Where a fact could not be pinned to one document, the entry says so
   and the extracted fact carries every candidate tag. This is the single biggest quality difference
   between this file and `frlib/_research/temporaire-deces.md`, where the PDFs themselves were
   downloaded and read.

**The search budget was exhausted.** The session shared a hard cap of 200 `WebSearch` calls across
all its work, and the cap was reached after **24 searches** on this product — against a brief that
anticipated thirty to eighty. The consequence is not evenly spread. The statutory core (§§ 153, 161,
165, 169 VVG; MindZV; DeckRV; § 139 VAG; VVG-InfoV; EStG § 20 Abs. 1 Nr. 6), the supervisory material
(BaFin *Merkblatt* 01/2023, *Risiken im Fokus* 2026) and the surplus mechanics are researched to a
usable depth. The **insurer-by-insurer parameter sweep is not**: of the twenty-six carriers the brief
named, only Debeka, Allianz, Gothaer, die Bayerische, ERGO and ÖSA produced any document at all, and
only Debeka produced quantified terms. Every gap this caused is numbered in the register at the foot
of this file, and no gap was papered over with a guess.

`[unverified]` keeps its normal meaning: a claim no search result corroborated. A fact several
independent search results agree on is **not** `[unverified]`; a paragraph number, an effective date
or a figure that no search result confirmed **is**. Every URL below is one a search result actually
returned, or the obvious canonical form of one (`.../vvg_2008/__153.html` for § 153 VVG). Where there
is no URL the entry says `URL: not established` rather than guessing.

**The re-verification of 2026-08-30.** The policy was lifted and the citations were checked against
the primary documents. Library-wide, all fifteen German instruments delib cites were read as
canonical XML from `gesetze-im-internet.de` with each law's amendment `Stand` recorded, 950
statutory section references were checked and 950 were correct, and insurer AVB,
*Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read; **501
of the library's 805 source entries, 62 %, now read `Retrieved: yes`.** In this file the pass
reached **43 of the 49 entries, and those 43 carry a `Retrieved (2026-08-30):` line: 38 say yes, two
say no ([S8], a 404; [R24], HTTP 429) and three are partial ([R11], [R19], [R26])**. The remaining
six — [S12] to [S16] and [R31] — carry no such line, nothing was opened for them, and they still
rest on the search summaries described above.

**What an entry now means.** A **`Retrieved (2026-08-30): yes`** line means the document was opened
and the passage the entry rests on was read; the line records the PDF's page count and edition or
the law's `Stand`, and a German sentence quoted under it is a quotation **of the instrument**.
Everywhere else the citation is still **a pointer rather than a certificate**, and a quoted German
sentence is still a quotation of a summary. **The re-verification changed things, and in this file
it changed a lot**: nine extracted facts did not survive retrieval, six of them fusion artefacts of
the search summaries, and the corrections are written into the blocks and into the correction block
at the head of *Extracted facts*. Treat a claim here as sound where its entry says `Retrieved: yes`,
and as provisional where it does not.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on:

| Term | Gloss |
|---|---|
| *Kapitalbildende Lebensversicherung*, *Kapitallebensversicherung* (KLV) | Endowment: a life contract that builds a capital sum and pays it at maturity or on earlier death |
| *Gemischte Versicherung auf den Todes- und Erlebensfall* | The endowment proper — one contract insuring both the death and the survival event |
| *Versicherungssumme* | Sum insured; the guaranteed benefit before surplus |
| *Erlebensfallleistung* / *Todesfallleistung* | Survival benefit, paid at the *Ablauf* if the insured is then alive / death benefit, paid on death before it |
| *Ablauf*, *Ablauftermin* | Maturity, the date the survival benefit falls due |
| *Beitrag* | Premium. *Bruttobeitrag* = gross, *Nettobeitrag* / *Nettoprämie* = risk-and-savings premium before expense loadings |
| *Beitragssumme* | Premium sum: the total of all premiums payable over the agreed term. The reference base for acquisition-cost limits |
| *Beitragszahlungsdauer* | Premium-paying period, which may be shorter than the *Versicherungsdauer* |
| *Überschussbeteiligung* / *Überschussanteile* | Participation in surplus, the statutory entitlement of § 153 VVG / the amounts actually allocated to one contract |
| *Zinsüberschuss* / *Risikoüberschuss* / *Kostenüberschuss* | Interest surplus (return above the *Rechnungszins*) / mortality surplus / expense surplus |
| *Laufende Überschussbeteiligung* / *Schlussüberschussanteil* | The annually declared, annually allocated surplus / terminal bonus, allocated only at *Ablauf* or on some earlier exits |
| *Gesamtverzinsung* | Total declared return = *laufende Verzinsung* + the *Schlussüberschuss* expressed as a rate |
| *Bewertungsreserven* | Unrealised gains on the insurer's assets; policyholders share under § 153(3) VVG |
| *Sicherungsbedarf* | The reserve strengthening need on contracts with a high guaranteed rate, which cuts the *Bewertungsreserven* share |
| *Rückstellung für Beitragsrückerstattung* (RfB) / *Rohüberschuss* | The provision through which surplus is accumulated before allocation / raw surplus, before the minimum allocation to it |
| *Rechnungszins* / *Höchstrechnungszins* | The technical interest rate the contract is priced and reserved on / its statutory maximum for new business, set in the DeckRV |
| *Deckungskapital* / *Deckungsrückstellung* | The actuarial reserve of one contract / the balance-sheet provision covering it |
| *Zillmerung* / *Höchstzillmersatz* | Financing acquisition costs by writing them into the reserve, producing a negative early reserve / the statutory cap on the costs so financed |
| *Abschluss- und Vertriebskosten* / *Verwaltungskosten* | Acquisition and distribution costs / administration costs |
| *Ratenzahlungszuschlag* / *Effektivkosten* | Instalment loading for paying other than annually / reduction in yield: the annualised return give-up caused by all charges |
| *Rückkaufswert* / *Mindestrückkaufswert* | Surrender value / its statutory floor under § 169(3) VVG |
| *Stornoabzug* | The deduction the insurer may make from the surrender value |
| *Beitragsfreistellung*, *prämienfreie Versicherung* | Making the contract paid-up; the reduced sum insured that results is the *beitragsfreie Versicherungssumme* |
| *Gesundheitsprüfung* / *Risikozuschlag* | Medical underwriting / extra-mortality loading |
| *Vorvertragliche Anzeigepflicht* | The applicant's pre-contractual duty of disclosure |
| *Selbsttötung* / *Stornoquote* | Suicide, § 161 VVG / lapse rate |
| *Bezugsberechtigter* / *Versicherungsschein* | Beneficiary / the policy document |
| *Neue Klassik* | Post-2013 conventional products with a modified guarantee, contrasted with *Klassik* |

---

## Primary sources

**Retrieval status is now recorded per entry, not once for the section.** Each block below carries
a `Retrieved (2026-08-30)` line saying what was actually opened, and where the retrieved document
contradicts what the original search summary reported, the correction is written into the block and
marked. Where an entry has no such line, nothing was opened and the material still rests on the
search-result summary described in *Retrieval conditions and citation discipline* above — in which
case a quoted German sentence is a quotation of the summary and not of the document.

### S1 — GDV, "Allgemeine Bedingungen für die kapitalbildende Lebensversicherung" (Musterbedingungen)
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV). Doc type:
  *Musterbedingungen* — model AVB published by the industry association for members to adopt, adapt
  or ignore
- URLs (three distinct blob paths under the same GDV resource id 6348 were returned by two separate
  searches, consistent with more than one edition or rendering of the same document):
  https://www.gdv.de/resource/blob/6348/075948efa290a72d0bb062dec766f56f/allgemeine-bedingungen-fuer-die-kapitalbildende-lebensversicherung-pdf-data.pdf ·
  https://www.gdv.de/resource/blob/6348/4a1ebd2301be0fed4c8c7e55c4af4950/allgemeine-bedingungen-fuer-die-kapitalbildende-lebensversicherung-pdf-data.pdf ·
  https://www.gdv.de/resource/blob/6348/5827a5492cca6aa1147852c30f10247b/allgemeine-bedingungen-fuer-die-kapitalbildende-lebensversicherung-0-pdf-data.pdf ·
  index: https://www.gdv.de/gdv/service/musterbedingungen · third-party mirrors of what is
  presented as the same document:
  http://www.vbed.de/wp-content/uploads/Allgemeine-Bedingungen-Kapitalbildende-Lebensversicherung.pdf
  and a `silo.tips` copy under the same title
- **Retrieved (2026-08-30): yes.** PDF, 20 pp., `Stand: 21.07.2025`. The whole model wording arrives
  as clause text, so the note below that "no article text beyond the § 1 heading was returned" is
  superseded. What the retrieved edition adds: § 2 on the *Überschussbeteiligung* (RfB, MindZV,
  *verursachungsorientiertes Verfahren*, *Gewinnverbände*, *Bewertungsreserven*, and Abs. 7 "Die Höhe
  der künftigen Überschussbeteiligung kann also nicht garantiert werden. Sie kann auch Null Euro
  betragen."); § 5 on *Selbsttötung* at three years paying the *Rückkaufswert* without the *Abzug*;
  § 12 restating § 169 VVG including the five-year floor; § 13 computing the *beitragsfreie
  Versicherungssumme* on that value; and § 14 applying "das Verrechnungsverfahren nach § 4 der
  Deckungsrückstellungsverordnung" capped at "2,5 % der von Ihnen während der Laufzeit des Vertrages
  zu zahlenden Beiträge". **Every quantitative field is an ellipsis for the undertaking to fill** —
  the *Abzug*, the minimum sums, and (footnote 6) the *Wartezeit*, the *Bemessungsgrößen* and the
  *Rechnungsgrundlagen* — so the original conclusion holds unchanged: **no level in delib is
  attributed to S1**, only clause shape.
- Content — the closest thing the German market has to a canonical wording, and the natural spine for
  a composite specification:
  - It is a **GDV *Musterbedingung***, and the GDV states its model conditions are **unverbindlich**
    for undertakings and their use **purely optional**. That competition-law disclaimer matters: an
    S1-tagged fact is a *market template*, weaker evidence about a carrier than the same fact taken
    from that carrier's own AVB.
  - The AVB address the customer in the second person, in the question-headed style the GDV adopted
    for post-2008 VVG wordings. **§ 1 is headed "Welche Leistungen erbringen wir?"** — the benefit
    clause; the remaining section numbering was **not** established.
  - **No article text beyond the § 1 heading was returned.** Every substantive benefit, surplus,
    surrender or paid-up rule attributed below to "the model conditions" is attributed instead to the
    statute it implements [R1]–[R4] or to a named carrier's wording [S3]–[S8], never to S1.

### S2 — GDV, "Jährliche Mitteilung zum Stand Ihrer Versicherung" (Muster-Standmitteilung, kapitalbildende Lebensversicherung, 02/2017)
- Publisher: GDV. Doc type: model *Standmitteilung* — the annual statement sent to the policyholder
- URL: https://www.gdv.de/resource/blob/6302/890c551440e2d065eba74180437f6970/5-gdv-muster-standmitteilung-kapitalbildende-lebensversicherung-02-2017-data.pdf
- **Retrieved (2026-08-30): yes.** PDF, 7 pp., **dated 22 March 2018 in the document body** and
  headed "Anlage 5", although the GDV file name carries "02-2017".
- Content, **corrected against the retrieved document**. The field list is now established and it is
  **not** the four quantities inferred from the title. The statement rolls the *Garantiertes Kapital*
  forward — opening balance, plus *Beiträge*, plus *Erträge*, less the year's *Abschluss- und
  Vertriebskosten* and *Verwaltungskosten* — then adds a "Für die Zukunft nicht garantierter
  Schlussüberschuss" and a "Für die Zukunft nicht garantierte Beteiligung an Bewertungsreserven" to
  reach a *Gesamtkapital*. Four further blocks give the benefit at *Versicherungsablauf*, at death,
  at *Beitragsfreistellung* and at *vorzeitige Vertragsbeendigung*, each split into "Garantierte
  einmalige Zahlung", "Bisher erreichte einmalige Zahlung aus laufender Überschussbeteiligung", the
  *Schlussüberschuss* and the *Bewertungsreserven* share; the maturity block adds a three-column
  sensitivity at the current declaration and at ±1 percentage point. **There is no line called
  *Rückkaufswert* and none called *beitragsfreie Versicherungssumme***. Two findings beyond the field
  list: the glossary defines the *Schlussüberschuss* as assigned bindingly only at *Rentenbeginn* or
  at the end of the contract and redetermined annually; and the statement provides for a
  ***Sockelbeteiligung an Bewertungsreserven***, which is the first of three independent
  corroborations of the *Sockelbetrag* left `[unverified]` at R8.

### S3 — Debeka Lebensversicherungsverein a. G., Bedingungswerk **B LV 85** (edition 01.07.2026)
- Publisher: Debeka Lebensversicherungsverein a. G. Doc type: AVB for a kapitalbildende
  Lebensversicherung tariff, **21 pages** (the running header "B LV 85 (01.07.2026) Seite 1 von 21"
  was reproduced in the search result)
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf
- **Retrieved (2026-08-30): yes.** PDF, 21 pp., edition 01.07.2026. **The document is not an
  endowment wording.** Its title is "Allgemeine Bedingungen für eine Rentenversicherung mit
  aufgeschobener Rentenzahlung und Fondskomponenten nach Tarif CA2I (ABAR-IT 07/2026)" — a deferred
  annuity with a *garantiebasierter* and a *fondsgebundener Baustein* — and Debeka's own library files
  it under *Aufgeschobene Rentenversicherung* [S6]. Three consequences for the notes below.
  **(a) The surplus claim is contradicted.** § 30 Abs. 1 b sets *Zinsüberschussanteile*
  **monthly**, "in Prozent des Deckungskapitals" struck at the start of the month excluding the
  premium then due, and **first for the third *Versicherungsjahr***; § 30 Abs. 2 sets
  *Schlussüberschussanteile* not on the reserve but "in Prozent der Summe der während der
  Aufschubzeit für den Erwerb von Fondsanteilen verwendeten Zinsüberschussanteile". The allocated
  surplus is invested in a fund, not booked into the *Deckungskapital*. So "each fixed as a
  percentage of the *Deckungskapital* at the allocation date", "annually", and the "single most
  useful mechanical fact" reading below are all wrong as stated; the endowment evidence for the
  reserve base is at S7 and S18.
  **(b) The *Stornoabzug* is confirmed and completed.** § 34 imposes two deductions in percent of the
  *Deckungskapital*: an *Ausgleich für die Veränderungen der Ertragslage des Versichertenkollektivs*
  keyed to the 10-year zero-coupon euro swap rate less its own ten-year average — "Kapitalmarkt-
  situation 1 (Differenz von weniger als 0,5 Prozentpunkte): kein Abzug", 2: 5 %, 3: 10 %, 4: 15 % —
  and a flat *Ausgleich für kollektiv gestelltes Risikokapital* of 5 %. **Both fall linearly to 0 %
  over the last ten years of the *Aufschubzeit***, and both lapse on a *Kündigung* in the last five
  years once the life has passed 62 and the contract has run twelve years. The range therefore starts
  at nil, not at 5 %.
  **(c) The clause numbering question is answered**: the *Überschussbeteiligung* clauses are §§ 4, 30
  and 34 in this wording, and the numbers reported by the search summary belonged to several
  documents at once.
- Content — the **most recent** German endowment wording located in this research, and the only
  carrier document with quantified terms:
  - Edition date **1 July 2026**, current as at the access date, 21 pages.
  - It sits in Debeka's *Vertragsgrundlagen* library under the heading **Kapitalbildende
    Lebensversicherung** [S6], so its product classification is not inferred.
  - *Überschussbeteiligung* mechanics, reported for the Debeka endowment wordings as a family:
    ***Zinsüberschussanteile* and *Schlussüberschussanteile* are each fixed as a percentage of the
    *Deckungskapital* calculated at the allocation date.** This is the single most useful mechanical
    fact in the corpus: the declared rate multiplies a reserve, not a sum insured and not a premium.
  - **The level of future *Überschussbeteiligung* cannot be guaranteed**; it is set **annually** and
    depends on capital-market development and on the insurer's own results.
  - *Stornoabzug*: a **standard 5 % deduction** plus a **kapitalmarktabhängige Stornogebühr** whose
    size follows the capital-market situation and **can be 5 %, 10 % or 15 % of the
    *Deckungskapital***. Reported consistently by consumer bodies and the legal press [R22][R30];
    **which Debeka wording carries which figure was not established**, so the figures are attributed
    to "the Debeka endowment wordings" rather than to B LV 85 specifically.
  - The *Überschussbeteiligung* clause numbering is **tariff-dependent**: the summary reported
    sections 28, 30, 33, 36, 38, 42 and 46 across the Debeka *Bedingungswerke* without saying which
    belongs to which. Treat any specific section number as `[unverified]`.

### S4 — Debeka, Bedingungswerk **B LV 86** (edition 01.01.2025)
- Doc type: AVB for a kapitalbildende Lebensversicherung tariff, **19 pages** ("B LV 86
  (01.01.2025) Seite 1 von 19")
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV86.pdf
- **Retrieved (2026-08-30): yes.** PDF, 19 pp. — and the **edition is 01.07.2026, not 01.01.2025**:
  the URL is a current-version path whose content has rolled forward. The title is "Allgemeine
  Bedingungen für eine Rentenversicherung mit aufgeschobener Rentenzahlung und Fondskomponenten nach
  Tarif CA6I (ABAR-IG 07/2026)" — again an annuity, not an endowment.
- Content: identity and page count established. **The "three parallel endowment wordings of different
  vintages" reading is contradicted**: the three are annuity wordings, they carry the *same* edition
  date, and they differ by tariff — CA2I regular premium (S3), CA6I (S4), CA2IE single premium (S5).
  The cohort argument the vintage spread was cited for is carried instead by DeckRV § 2 Abs. 2 and
  § 4 Abs. 4, which fix the *Rechnungszins* and the *Zillmersatz* used at conclusion for the whole
  term (R7), and by the 4 % clause in the 2011 Gothaer wording (S7).

### S5 — Debeka, Bedingungswerk **B LV 97** (edition 01.01.2025)
- Doc type: AVB for a kapitalbildende Lebensversicherung tariff, **18 pages** ("B LV 97
  (01.01.2025) Seite 1 von 18")
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV97.pdf
- **Retrieved (2026-08-30): yes.** PDF, 18 pp., edition **01.07.2026** (not 01.01.2025, for the same
  reason as S4). Title: "Allgemeine Bedingungen für eine Rentenversicherung mit aufgeschobener
  Rentenzahlung und Fondskomponenten gegen Einmalbeitrag nach Tarif CA2IE (ABAR-IT-E 07/2026)".
- Content: identity and page count established; the single-premium sibling of S3. The 18–21 page
  observation is about **annuity** wordings, not endowment ones. The two endowment wordings actually
  retrieved run to 12 pp. (S7) and 26 pp. including the *Verbraucherinformationen* (S18), so the
  page-count range is wider than recorded and not a useful invariant.

### S6 — Debeka, "Vertragsgrundlagen und weitere Informationen (Bedingungswerke, Tarifbedingungen, IPID etc.)" — Kapitalbildende Lebensversicherung
- Doc type: insurer document-library index page
- URL: https://www.debeka.de/service/bedingungen/Lebensversicherung___Rentenversicherung/Lebensversicherung/Kapitalbildende_Lebensversicherung/index.html
- **Retrieved (2026-08-30): yes.** The cited path redirects to Debeka's single document library at
  `https://www.debeka.de/service/vertragsgrundlagen.html`. The retrieved index confirms the category
  and adds the finding that matters most in this file: under the live heading **Kapitalbildende
  Lebensversicherung** Debeka lists **no AVB at all** — only a *Steuermerkblatt*, a
  *Kirchensteuerinformationsblatt* and the AVB for a *Sterbegeldversicherung*. The three
  *Bedingungswerke* at S3–S5 are filed under **Aufgeschobene Rentenversicherung**, which is what
  settles their product classification against them.
- Content: establishes that **"Kapitalbildende Lebensversicherung" is a live product category in a
  major German insurer's own taxonomy** as at the access date, with its own branch of the
  contract-documents tree. The page title lists the document types published per product:
  *Bedingungswerke*, *Tarifbedingungen* and **IPID**. The presence of *IPID* is worth recording —
  the German market labels the pre-contractual product summary with the EU IDD term, the analogue
  of the French *document d'information sur le produit d'assurance*. **No IPID for a kapitalbildende
  Lebensversicherung was located**; gap 9.

### S7 — Gothaer, "Allgemeine Versicherungsbedingungen für die kapitalbildende Lebensversicherung"
- Publisher: Gothaer, served from the broker portal `partner.gothaer.de`
- URL: https://partner.gothaer.de/StreamingServlet/app/dvz/DocumentDownload/215401?scope=makler_scope
  — a broker-portal streaming endpoint with a `scope` parameter, so it may not resolve for a public
  reader even without the egress block.
- **Retrieved (2026-08-30): yes.** PDF, 12 pp., "Version: 05.12.2011", stamp `215401 - 01.12`; the
  broker endpoint serves it to a public reader. **This is one of the two genuine endowment wordings
  in the corpus** (with S18) and, being pre-LVRG, the only one written under the old ceilings. The
  fusion warning below is discharged: the document can now be read on its own, and three of the
  reported statements need correcting.
  **(a) The maturity payment is conditional on survival** in the ordinary form: § 3 I (3) "Zum Ablauf
  zahlen wir die Versicherungssumme, wenn die versicherte Person diesen Termin erlebt." The
  unconditional reading belongs to variant II, the *Kapitalversicherung auf festen Termin*.
  **(b) "No further premiums are due on death" likewise belongs to variant II** — "Bei Tod der
  versicherten Person vor dem Ablauftermin werden keine Beiträge mehr fällig" appears only there,
  because that is the one variant the death does not terminate. In variants I, III and IV "Mit der
  Auszahlung endet der Vertrag", so the premium stops because the contract does.
  **(c) The *Selbsttötung* window is two years**, not three: § 4 Abs. 1 limits liability to the
  *Rückkaufswert* on suicide "innerhalb von zwei Jahren nach Vertragsbeginn". § 161 Abs. 2 VVG allows
  only an increase, but § 171 makes § 161 *halbzwingend*, so a shorter period is lawful as more
  favourable to the policyholder.
  **What the wording adds.** § 5 II (4): "Es werden Jahresanteile zugewiesen. Diese bestehen aus
  einem Risikoanteil in Promille der Versicherungssumme und in Prozent des Risikobeitrags sowie einem
  Ertragsanteil in Prozent des maßgeblichen Deckungskapitals" — the reserve as the interest-surplus
  base, from an endowment wording, which is what S3 turned out not to supply. § 5 II (3) allocates
  annually at the *Stammtag*; § 5 II (5) defers the first allocation by three years for tariff group
  A. § 5 II (6) names the four *Überschussverwendung* systems — *Verzinsliche Ansammlung*,
  *Barauszahlung*, *Gewinnsystem BE* which "vor allem die Leistung Ihrer Versicherung im Erlebensfall
  verstärkt", and *Gewinnsystem BS*. § 5 II (7) makes the *Schlussgewinnanteil* depend on the maturity
  sum and the accumulated surplus, reduced on surrender and death. § 5 III (3) allocates the
  *Bewertungsreserven* "zur Hälfte" on termination, subject to a declared *Mindestbetrag*. § 6 Abs. 2
  applies the *Zillmerverfahren* with the amortisable amount limited "auf **4 %** der von Ihnen
  während der Laufzeit des Vertrags zu zahlenden Beiträge" — the pre-LVRG 40 ‰ ceiling in a carrier
  wording. § 7 restates § 169 VVG with the five-year floor; § 8 gives the paid-up right with a
  **1.500 EUR** minimum below which the surrender value is paid instead, which quantifies the § 165
  VVG *Mindestversicherungsleistung* branch.
- Content: the summary returned three clause-level statements for the group of documents it had
  matched, **without separating Gothaer's wording from the others in that group** (which also
  contained an Austrian ERGO document, S8's Bavarian AVB and the GDV model). Recorded with that
  warning, and now superseded by the retrieved text above:
  1. Payment of the agreed *Versicherungssumme* at the *Ablauftermin* named in the
     *Versicherungsschein*, described as due "regardless of whether the insured person reaches that
     date" — the pure-endowment reading in which the sum falls due at maturity to the survivor **or**
     earlier on death. The parenthetical is reported ambiguously and whether Gothaer's wording
     really makes the maturity payment unconditional on survival is `[unverified]`.
  2. In the *Erlebensfall* the policyholder must **submit the *Versicherungsschein*** to claim.
  3. The agreed *Versicherungssumme* can be reduced, **in whole or in part**, to a **beitragsfreie
     Versicherungssumme**; and if the insured dies before the *Ablauftermin*, **no further premiums
     are due**. The second half is the operative rule that the premium stream stops on death, which
     a projection model must implement and which is easy to get wrong.

### S8 — die Bayerische, "Allgemeine Bedingungen für die kapitalbildende Lebensversicherung", document **B 510121**
- Publisher: BL die Bayerische Lebensversicherung AG. Doc type: AVB for a *Kapital-Lebensversicherung*
- URL: https://www.diebayerische.de/dam/jcr:e5f5f192-0edc-49b1-9be8-18c3cc503ae3/510121_avb_kapital-lebensversicherung.pdf
- **Retrieved (2026-08-30): no.** HTTP 404 at the cited URL. The publisher's own site was searched
  once for a current path — the `diebayerische.de` root and its `formular-download` pages — and no
  replacement was found, the document index being script-loaded. The entry stays a known reference:
  the 404 shows only that the *cited* URL is dead, not that no such document exists, and its
  availability remains `[unverified]`.
- Content: **the existence of this document is contested within the search evidence and the
  contradiction is recorded rather than resolved.** A general search for endowment AVB returned this
  exact URL under the title "Allgemeine Bedingungen für die kapitalbildende ...". A narrower search
  for "die Bayerische … 510121" returned the sibling documents (B 510123 *Sterbegeldversicherung*,
  B 520127 *AVB gezillmert Klassikrente*, B 520136 *AVB Klassikrente*, B 660121, B 660800, B 117000)
  but **not** 510121, reporting it "may not be publicly available online". **The URL was returned by
  a search and is recorded verbatim; no content was established from it**, and its availability is
  `[unverified]`. The file name and the `51xxxx` prefix shared with the Sterbegeld AVB `510123` are
  consistent with a BL die Bayerische document series.

### S9 — die Bayerische, AVB **Klassikrente** (B 520136, 01.2025) and AVB **gezillmerte Klassikrente** (B 520127, 01.2022)
- Publisher: BL die Bayerische Lebensversicherung AG. Doc type: AVB for a *klassische
  Rentenversicherung* in a *gezillmert* and a non-*gezillmert* edition — **an annuity, not an
  endowment**, recorded as the nearest sibling wording found and the source of one directly
  transferable surplus-allocation rule
- URLs: https://www.diebayerische.de/dam/jcr:0936fd6c-71b9-453d-83f6-57ec76a76697/520136_avb_klassikrente.pdf ·
  https://www.diebayerische.de/dam/jcr:0dcd832e-9107-44b4-a967-5e504c5c6fce/520127_avb_gezillmert_klassikrente.pdf
- **Retrieved (2026-08-30): yes.** Two PDFs, 14 pp. each. **They are not a *gezillmert* /
  non-*gezillmert* pair.** Both are "Allgemeine Bedingungen für die moderne klassische
  Rentenversicherung (KlassikRente)" — B 520136 is edition 01/2025 (internal reference 25L03) and
  B 520127 edition 01/2022 (22L03), the same tariff two years apart — and **both are zillmered**:
  § 15 Abs. 2 is word-identical in the two, applying "das Verrechnungsverfahren nach § 4 der
  Deckungsrückstellungsverordnung" capped at "2,5 % der von Ihnen während der Laufzeit des Vertrages
  zu zahlenden Beiträge". The word *gezillmert* occurs only in the file name of 520127. The last
  bullet below — that the pair is direct evidence of *Zillmerung* as a published per-tariff choice —
  is therefore **contradicted and withdrawn**.
  What the retrieved text confirms and refines. *Anlage 1* (Stand 01/2025): "Der Anspruch auf
  Überschussbeteiligung beginnt sofort mit dem Versicherungsschutz"; "Während der ANSPARPHASE erhält
  Ihr Vertrag an jedem Bilanztermin (31.12. des Jahres) und zum Ablauf der ANSPARPHASE
  Zinsüberschussanteile zugeteilt und in das DECKUNGSKAPITAL des Vertrages gebucht (laufende
  Zinsüberschussanteile)"; and, new, the allocation is **annual but accrues monthly** — "dabei ist
  Zinsträger jeweils das am Anfang des Monats vorhandene DECKUNGSKAPITAL (inklusive eines ggf.
  fälligen Beitrags, abzüglich der zum Monatsbeginn fälligen Kosten)". The *Schlussüberschussanteil*
  "bemisst sich monatlich nach einem Prozentsatz der maßgebenden Größe für den Zinsüberschuss" and may
  be redetermined for past years or dropped. § 2 Abs. 1: "Die Leistung aus der Überschussbeteiligung
  kann auch Null Euro betragen." The glossary defines the *Deckungskapital* as "die verzinsten
  Sparbeiträge des Vertrags und die zugeführten laufenden Überschussanteile", and provides a
  *Mindestbeteiligung* at the *Bewertungsreserven* — the second corroboration of the *Sockelbetrag*.
  *Anlage 2* quantifies the deduction: "Der Abzug beträgt 50 EUR plus 0,15 %" of the premiums fallen
  due to the cancellation date multiplied by the years remaining to the original
  *Rentenzahlungsbeginn* — a second quantified carrier *Stornoabzug*, on a base unlike Debeka's.
- Content, and why it earns an entry despite being the wrong product:
  - **The right to *Überschussbeteiligung* begins immediately with the start of insurance cover** —
    no waiting period.
  - During the accumulation phase the contract is allocated **Zinsüberschussanteile** at each
    **Bilanzstichtag, being 31 December of the year**, and again at the end of the phase; the
    amounts are **booked into the contract's *Deckungskapital***.
  - **The level of future *Überschussbeteiligung* cannot be guaranteed and may be zero euros.**
  Together these give the *annual, balance-date, reserve-crediting* allocation convention an
  annual-step endowment model needs, and the explicit statement that the rate may be **zero** is the
  cleanest sourced justification for treating the surplus rate as insurer-discretionary. That the
  document is an annuity wording is stated wherever the fact is used.
  - The existence of a *gezillmert* and a non-*gezillmert* edition of the **same** tariff is direct
    evidence that **Zillmerung is a per-tariff design choice a German insurer makes and
    publishes**, not an invariant of German practice.

### S10 — ÖSA, "Basisinformationsblatt — ÖSA StarthilfePlus (laufende Beitragszahlung)"
- Publisher: ÖSA Versicherungen. Doc type: **PRIIP-Basisinformationsblatt (BIB)**, **3 pages**
  ("Seite 1 von 3")
- URL: https://www.oesa.de/export/sites/oesa/_resources/download/privat/service/bib/OeSA-StarthilfePlus_laufend_20.pdf
- **Retrieved (2026-08-30): yes.** PDF, 3 pp., `Stand Basisinformationsblatt 01.01.2024`, issued by
  the Öffentliche Lebensversicherung Sachsen-Anhalt.
- Content: the **only PRIIP-BIB for a German capital-forming life product in this corpus**, and the
  open questions are now answered. **Product type**: "Art: Versicherungsanlageprodukt in Form einer
  **Kapitallebensversicherung** mit garantierter Verzinsung nach deutschem Recht" — so the label is
  endowment, though the benefit is a time-limited annuity from *Rentenbeginn*, the death scenario pays
  **0,00 €** at every horizon, and death before *Rentenbeginn* continues the contract premium-free.
  It is a savings contract with a premium waiver rather than the composite delib models, and it should
  be cited as an example of BIB *content*, not of endowment *terms*.
  **Figures**, on the BIB's model case of a 47-year-old, 1.000 € annual premium, 20 years: risk
  indicator **3 of 7**; premium split "Durchschnittliche Versicherungsprämie für das abgesicherte
  Risiko: 9,40 % (94,05 €)" against "Durchschnittlicher Anlagebetrag: 90,60 % (905,95 €)", the risk
  premium reducing the return by 1,0 %; four performance scenarios at 1, 10 and 20 years (*Stress*
  12.610 €, *pessimistisch* 13.370 €, *mittleres* 15.070 €, *optimistisch* 17.110 € at 20 years,
  against 20.000 € invested); **total costs 468 € / 3.342 € / 6.216 €** with an annual cost impact of
  **5,3 % pro Jahr** at 20 years and a return "voraussichtlich 2,4 % vor Kosten und -2,9 % nach
  Kosten"; entry costs 2,2 % and ongoing administration 28,5 % "der Summe aller Anlagebeträge"; and
  the Protektor statement that a shortfall can produce "Abschlägen von bis zu 5 %". **This is the only
  product-level cost disclosure in the corpus** and materially narrows gap 7 without closing it: one
  product, one public-sector insurer, one model case.

### S11 — Allianz, "Kapitallebensversicherung: Ihr umfassender Ratgeber", with "Lebensversicherung: Arten im Überblick" and "Lebensversicherung Auszahlung: Ablauf & Steuer"
- Publisher: Allianz Lebensversicherungs-AG (German consumer site). Doc type: insurer product/guide
  pages, three URLs
- URLs: https://www.allianz.de/vorsorge/kapitallebensversicherung/ ·
  https://www.allianz.de/vorsorge/lebensversicherung/ ·
  https://www.allianz.de/vorsorge/lebensversicherung/auszahlung/
- **Retrieved (2026-08-30): yes**, all three pages. **The declared rate is not on any of them.** The
  only rate the Allianz pages state is the *Garantiezins*: "Das Bundesfinanzministerium hat den
  Garantiezins für Neuverträge seit dem 1. Januar 2025 auf 1,00 Prozent festgelegt", said twice. The
  2,7 % below is real but belongs to [R26] — procontra reporting Allianz holding the *laufende
  Verzinsung* "für die klassischen Lebens- **und** Rentenversicherungen konstant bei 2,7 Prozent" for
  **2025**, a combined book and the wrong year. The *Rückkaufswert*-below-premiums statement is also
  not on these pages; what is there is "Allerdings schmälern Storno- und Verwaltungskosten den
  Rückkaufswert". [S12] carries that statement in full instead.
  What the pages do carry: the market-role sentence, verbatim — "Die kapitalbildende
  Lebensversicherung wird heute **nur noch selten angeboten**. Viele Versicherungsunternehmen haben
  sie durch moderne private Rentenversicherungen ersetzt." — the tax summary "nur die Hälfte des
  Ertrags versteuert, sofern Ihr Vertrag mindestens 12 Jahre gelaufen ist und Sie bei Auszahlung
  mindestens 62 Jahre alt sind", the death benefit paid free of income tax, the death cover payable
  in full "schon ab der ersten Beitragszahlung", and the judgement that the classic form "eignet sich
  allerdings nur noch, wenn Sie im Alter unbedingt eine einmalige Kapitalauszahlung wünschen".
- Content — the largest German life insurer describing the product in its own words. **The bullets
  below are the original search-summary reading; the two struck through in substance by retrieval are
  marked above:**
  - The *klassisch* variant "combines a guaranteed interest rate, a savings component and death
    cover in one product" — the three-part description delib's overview mirrors.
  - **For 2026 Allianz credits its classic customers a *laufende Verzinsung* of 2,7 %** — a 2026
    figure, and the *laufende* rate before any *Schlussüberschuss*. Corroborated indirectly by trade
    reporting that **Allianz declined to raise its *Überschussbeteiligung*** for the year [R26],
    consistent with an unchanged rate.
  - On *Rückkaufswert*: on *Kündigung* the policyholder receives it, and it **can be below the
    premiums paid, especially in the early contract years**; the investment return earned and the
    *Überschussbeteiligung* are **included in** the calculation. An insurer's own confirmation that
    the surrender value is reserve-based-plus-surplus and that early durations are loss-making — the
    economic signature of *Zillmerung*.
  - Market position: the product "is rarely newly concluded today, because modern annuity insurance
    typically offers better flexibility and earnings opportunities" — an insurer saying this about
    its own historic flagship is the strongest evidence for delib's market-role paragraph.

### S12 — ERGO, "Ratgeber Kapitallebensversicherung"
- Publisher: ERGO Group. Doc type: insurer guide page.
  URL: https://www.ergo.de/de/Ratgeber/finanzielle_vorsorge/kapitallebensversicherung
- Content: matched in the typical-parameters search and contributed to the fused summary at section
  19. **No statement was separately attributable to ERGO.** A located carrier page with no
  independently established content.

### S13 — Sparkasse, "Kapitallebensversicherung — Für Rente & Familie vorsorgen"
- Publisher: Deutscher Sparkassen- und Giroverband. Doc type: distributor product/guide page.
  URL: https://www.sparkasse.de/pk/produkte/versicherung/vorsorge-und-risiko/lebensversicherung/kapitallebensversicherung.html
- Content: one of the pages behind the fused typical-parameters summary at section 19. The
  bank-channel provenance is worth noting on its own: **the German endowment is distributed through
  the savings-bank network as well as through tied agents and brokers**, and the *Vertriebsweg* is a
  driver of the acquisition-cost level.

### S14 — CosmosDirekt, "Erlebensfall: Was ist das und wie läuft die Auszahlung?"
- Publisher: CosmosDirekt (Generali Deutschland direct writer). Doc type: insurer glossary page.
  URL: https://www.cosmosdirekt.de/lebenssituation/erlebensfall/
- Content: the direct-writer treatment of the *Erlebensfall* concept. **No statement was separately
  attributable to it.** Recorded because CosmosDirekt is the market's principal direct channel and
  the *Erlebensfall* payout mechanics are its subject.

### S15 — Verivox, "Kapitallebensversicherung", "Überschussbeteiligung" and "Zillmerung"
- Publisher: Verivox GmbH (comparison portal). Doc type: three consumer explainer pages
- URLs: https://www.verivox.de/kapitallebensversicherung/ ·
  https://www.verivox.de/lebensversicherung/themen/ueberschussbeteiligung/ ·
  https://www.verivox.de/lebensversicherung/themen/zillmerung/
- Content: secondary throughout, but the *Zillmerung* page is one of the two independent statements of
  the **Höchstzillmersatz** rule: the LVRG cut the maximum *Zillmersatz* **from 40 ‰ to 25 ‰**, and
  **since 1 January 2015 it may not exceed 25 ‰ — 2,5 % — of the *Beitragssumme***; in the balance
  sheet the undertaking may accordingly recognise only 2,5 % of the premium sum as *Abschluss- und
  Vertriebskosten*. The *Überschussbeteiligung* page contributes to the four-component split at
  section 3 and the *Überschussverwendung* systems at section 4.

### S16 — Finanztip, "Überschussbeteiligung Lebensversicherung: Arten & Höhe" and "Steuer auf Lebensversicherung"
- Publisher: Finanztip Verbraucherinformation gGmbH. Doc type: two consumer-journalism explainers
- URLs: https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/ ·
  https://www.finanztip.de/lebensversicherung-versteuern/
- Content: the clearest secondary statement of the **four-component surplus split and the distribution
  quotas**: a *Zinsüberschuss* arises when the insurer earns more on the invested premiums than the
  guaranteed rate; a *Risikoüberschuss* when insureds die otherwise than as priced; a
  *Kostenüberschuss* when the book is administered more cheaply than loaded; and a
  *Schlussüberschussanteil* from long-run results not fully allocated during the term. **At least
  90 % of the *Zins-* and *Risikoüberschuss* must be passed to policyholders, and half of the
  *Kostenüberschuss***. Those quotas are corroborated independently from the MindZV at [R6], where the
  third component is the wider *übriges Ergebnis* — section 7 and gap 6. The tax page feeds section 17.

### S17 — HUK24, "Überschussbeteiligung der Risikolebensversicherung"
- Publisher: HUK24 AG (HUK-COBURG group). Doc type: insurer guide page — **about term life, not
  endowment**. URL:
  https://www.huk24.de/risikolebensversicherung/ratgeber-lebensversicherung/ueberschussbeteiligung
- **Retrieved (2026-08-30): yes.** HTML. **The four-component reading is contradicted.** The page
  does not use the names *Zins-*, *Risiko-*, *Kosten-* and *Schlussüberschuss* at all. It names three
  drivers — "Höhe der am Kapitalmarkt erwirtschafteten Gewinne", "Kostenstruktur des Versicherers",
  "Zahl der während der Vertragslaufzeit verstorbenen Versicherten" — restates the statutory duty to
  participate "verursachungsorientiert und angemessen", and then describes the two term-life
  application forms, *Todesfallbonus* and *Sofortrabatt*.
- Content: a carrier's own account of the three **sources** of surplus in the neighbouring product,
  corroborating that the interest / cost / mortality decomposition is carrier vocabulary and not only
  journalism. The four *names* rest instead on the wordings that use them — S7, S9, S18 — and on S16.
  **No endowment-specific statement is taken from it.**

### S18 — "Bedingungen und Verbraucherinformationen für die Kapital bildende Lebensversicherung" (third-party contract-clause mirror)
- Publisher: **VPV Lebensversicherungs-AG** (Vereinigte Postversicherung) — established by
  retrieval; the `lawinsider.com` record is an index stub that hosts no text and names the document's
  real location. Doc type: the customer document set for an endowment, **26 pp.**, stamp
  `2.MP.0401 01.2019 ZU`
- URL: https://www.deteassekuranz.de/wp-content/uploads/2021/05/Bedingungen-SterbegeldV-VPV.pdf
  (index record, title only: https://lawinsider.com/de/contracts/duGC9LpAVlC). **The file name says
  *SterbegeldV* and is wrong** for the document it serves
- **Retrieved (2026-08-30): yes.** PDF, 26 pp., edition 01.2019. Contents: AVB für die Kapital
  bildende Lebensversicherung (01.2019), AVB vorläufiger Versicherungsschutz, AVB
  Unfalltod-Zusatzversicherung, Besondere Bedingungen Nachversicherungsgarantie, *Steuerinformationen*,
  *Allgemeine Verbraucherinformationen*, and the *Satzung* of the Vereinigte Postversicherung VVaG.
- Content: **the second genuine endowment wording in the corpus** (with S7) and the most explicit on
  surplus, so this entry changes from "nothing substantive is cited" to one of the load-bearing ones.
  - § 2 Abs. 3 (a): "Sämtliche Verträge erhalten einen Zinsüberschussanteil. Dessen Höhe ermitteln wir
    wie folgt: **Das um ein Jahr mit dem Rechnungszins abgezinste Deckungskapital wird mit dem
    deklarierten Zinsüberschussanteilsatz multipliziert.**" Premium-paying contracts additionally get
    a *Risikoüberschussanteil* = declared rate × *Risikojahresbeitrag*. This is the clearest statement
    in the corpus that the interest surplus multiplies the **reserve**, and it pins the base to an
    opening rather than a closing balance.
  - The same clause imposes a **one-year *Wartezeit*** and allocates "jeweils zu Beginn des
    Versicherungsjahres", accumulating the amounts with interest — against S9's no-waiting-period rule
    and S7's and S3's three-year deferrals. **Carriers differ, and delib says so.**
  - § 2 Abs. 3 (b): a *Schlussüberschusskonto* fed by an annual *Schlussüberschussanteil* on "der für
    den Zinsüberschuss maßgeblichen Bezugsgröße", itself bearing a declared *Schlussüberschusszinssatz*,
    redeterminable for past years and able to fall to nil. That is the terminal-bonus accrual shape,
    from a wording.
  - § 2 Abs. 5 restates the *Sicherungsbedarf* cut-back in a carrier's own words: "Bewertungsreserven
    auf festverzinsliche Anlagen sind gemäß derzeitiger aufsichtsrechtlicher Regelung (vgl. § 139
    Abs. 3 VAG) nur insoweit zu berücksichtigen, als sie einen ggf. vorhandenen Sicherungsbedarf
    (vgl. § 139 Abs. 4 VAG) übersteigen." § 2 Abs. 6 provides a *Mindestbeteiligung an den
    Bewertungsreserven* — the third corroboration of the *Sockelbetrag* at R8.
  - § 12 Abs. 3 restates § 169 VVG with the five-year floor; § 12 Abs. 4 gives a **third quantified
    *Stornoabzug***, on yet another base: "ein Stornoabzug in Höhe von 100 € für erhöhte
    Verwaltungsaufwendungen. Zusätzlich erfolgt ein Stornoabzug in Höhe von 0,2 % der Differenz
    zwischen Versicherungssumme und dem Rückkaufswert nach Abs. 3". § 14 Abs. 2 applies the § 4 DeckRV
    method capped at 2,5 %.
  - And the original point stands: the title names the document pair the German market delivers —
    *Bedingungen* **and** *Verbraucherinformationen* — the German counterpart of the French
    *conditions générales* + *notice d'information* pair.

---

## Regulatory and actuarial references

**The blanket retrieval status these entries once carried no longer holds**, and it is no longer
stated once for the section: **every entry below carries its own `Retrieved (2026-08-30):` line**
saying what was opened, with the law's `Stand` for a statute and the edition for a publication.
As drafted the section read *"Retrieved: no — direct HTTP egress blocked in the build environment;
established from search-result summaries"*, thirty-one times over, and that is still the status of
[R31], which has no line of its own. Where an entry's line says yes, a German sentence quoted in it
is a quotation **of the instrument**; where there is no line, or the line says no or partly, a
quoted German sentence is still a quotation of a search-result summary and the entry says so.

### R1 — VVG § 153, *Überschussbeteiligung*
- Publisher: Bundesministerium der Justiz (Gesetze im Internet); mirrored by dejure.org, buzer.de,
  sozialgesetzbuch-sgb.de, juraforum.de, gesetze-in-app.de
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__153.html (canonical form) ·
  https://dejure.org/gesetze/VVG/153.html · https://www.buzer.de/153_VVG.htm
- **Retrieved (2026-08-30): yes**, as canonical XML from `gesetze-im-internet.de/vvg_2008/xml.zip`,
  `Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156`. The `__153.html` page is a ~5 kB frameset shell with no
  statutory text and is kept as the human-facing link only. The reading below is confirmed absatz by
  absatz and is now **version-pinned**, which closes gap 15 for this section. Two additions from the
  text: Abs. 2 Satz 2 leaves § 268 Abs. 8 HGB amounts out of account, and **Satz 3 of Abs. 3 now
  names its provisions** — "Aufsichtsrechtliche Regelungen zur Sicherstellung der dauernden
  Erfüllbarkeit der Verpflichtungen aus den Versicherungen, insbesondere die §§ 89, 124 Absatz 1,
  § 139 Absatz 3 und 4 und die §§ 140 sowie 214 des Versicherungsaufsichtsgesetzes bleiben
  unberührt" — so the wording left unestablished below is established. Abs. 4, which moves the
  reference date to the end of the *Ansparphase* for annuities, does not apply to this product.
- Content, absatz by absatz as the summaries report it:
  **Abs. 1** — the policyholder is entitled to a share **in the surplus and in the
  *Bewertungsreserven*** (together the *Überschussbeteiligung*), **unless the participation is
  excluded by express agreement**, and it **can only be excluded entirely**. The all-or-nothing
  character of the exclusion is explicit and is why a German endowment is either fully
  participating or not participating at all.
  **Abs. 2** — the insurer must allocate the surplus by a **verursachungsorientiertes Verfahren**
  (causation-oriented procedure); other comparable appropriate distribution principles may be
  agreed.
  **Abs. 3** — the insurer must **determine the *Bewertungsreserven* anew each year** and allocate
  them by a causation-oriented procedure; **on termination of the contract half of the amount then
  determined is allocated and paid out**, and **earlier allocation may be agreed**.
- The article sits in **Chapter 5 (Lebensversicherung) of the VVG 2008**. A separate result
  establishes **§ 153 Abs. 3 Satz 3 VVG in the version given by the Lebensversicherungsreformgesetz
  of 1 August 2014**, described as a *Vorbehalt aufsichtsrechtlicher Regelungen* — a proviso
  subordinating the determination of the *Bewertungsreserven* to supervisory rules — and as having
  been challenged as unconstitutional before the BGH. That proviso is the hinge letting the
  *Sicherungsbedarf* of § 139 VAG [R8] cut into the half share; see [R23]. **The wording of Satz 3
  was not established.**
- **No version date, no *Fassung* line and no amending statute later than the LVRG 2014 were
  returned.** See gap 15.

### R2 — VVG § 169, *Rückkaufswert*
- Publisher: Bundesministerium der Justiz; mirrored by dejure.org, lxgesetze.de, buzer.de,
  juraforum.de, sozialgesetzbuch-sgb.de
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__169.html ·
  https://dejure.org/gesetze/VVG/169.html · https://lxgesetze.de/vvg/169 ·
  https://www.buzer.de/169_VVG.htm
- **Scope.** The article governs the claim to a *Rückkaufswert* where the insurance ends, **in
  particular by *Kündigung*, *Rücktritt* or *Anfechtung***, and fixes the calculation principles, the
  limits on payment, the deduction and reduction powers and the insurer's information duties.
- **Retrieved (2026-08-30): yes**, canonical XML, `Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156`; `__169.html`
  is a 7 kB shell. The Abs. 3 sentence below, quoted from a search summary when it was written, is
  **word-for-word correct against the statute** and is now a quotation of the instrument. Two
  additions: Abs. 2 caps the payable *Rückkaufswert* at the benefit that would fall due on a claim at
  the cancellation date and directs the remainder to a *prämienfreie Versicherung* — a branch delib
  does not model; and Abs. 7 requires the already-allocated *Überschussanteile* and the
  *Schlussüberschussanteil* provided for on *Kündigung* to be paid **in addition**, which is why the
  *Überschussguthaben* is outside the *Stornoabzug* base.
- **Abs. 3, the calculation rule**, quoted from the retrieved instrument:
  > "Der Rückkaufswert ist das nach anerkannten Regeln der Versicherungsmathematik mit den
  > Rechnungsgrundlagen der Prämienkalkulation zum Schluss der laufenden Versicherungsperiode
  > berechnete Deckungskapital der Versicherung, bei einer Kündigung des Versicherungsverhält-
  > nisses jedoch mindestens der Betrag des Deckungskapitals, das sich bei gleichmäßiger
  > Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre
  > ergibt."
  Read as a specification that is five requirements: a **Deckungskapital**; computed **by recognised
  actuarial rules**; on the ***Rechnungsgrundlagen der Prämienkalkulation*** — the pricing basis, not
  a current or reserving basis; struck **at the end of the current *Versicherungsperiode***, not at
  the cancellation date; and **on *Kündigung*** floored by the *Mindestrückkaufswert*.
- **Mindestrückkaufswert.** The floor is the *Deckungskapital* obtained when the *angesetzte
  Abschluss- und Vertriebskosten* are spread **evenly over the first five contract years**; the
  summary states its purpose plainly — to protect the policyholder — and by the wording above it
  bites **on *Kündigung***.
- ***Zeitwert*.** For *fondsgebundene* and certain other classes the *Rückkaufswert* is instead a
  **Zeitwert** computed by actuarial rules. That branch governs delib product 3, **not** this one.
- ***Abzug* (*Stornoabzug*).** Permissible **only if *vereinbart*, *beziffert* and *angemessen***.
  A deduction **for *noch nicht getilgte Abschluss- und Vertriebskosten* is unwirksam** — which is
  what stops an insurer recovering through the deduction what the five-year spreading denies it.
- One summary reported the five-year spreading and a **2,5 % of *Beitragssumme*** cap as if both
  came from § 169 Abs. 3. **They do not**: the 2,5 % is the DeckRV *Höchstzillmersatz* [R7]. Gap 5.

### R3 — VVG § 165, *Prämienfreie Versicherung*
- **Retrieved (2026-08-30): yes**, canonical XML, `Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156`;
  `__165.html` is a 4 kB shell. Every limb below is confirmed verbatim, including Abs. 2's "im
  Vertrag für jedes Versicherungsjahr anzugeben" and Abs. 3's netting of *Prämienrückstände*. The
  *Mindestversicherungsleistung* is quantified in two retrieved wordings — **1.500 EUR** of sum
  insured at S7 § 8, and a monthly **25 EUR** guaranteed minimum annuity at S9 § 14 — which was
  previously unobserved. The note that *Zusatzversicherungen* are regularly lost on paid-up is
  commentary and is **not** in § 165.
- Publisher: Bundesministerium der Justiz; mirrored by buzer.de, LexMea, dejure.org, freiRecht.de,
  NWB, sozialgesetzbuch-sgb.de
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__165.html ·
  https://dejure.org/gesetze/VVG/165.html · https://www.buzer.de/165_VVG.htm
- The policyholder may **at any time, with effect for the end of the current *Versicherungsperiode*,
  demand conversion into a *prämienfreie Versicherung***, **provided the agreed
  *Mindestversicherungsleistung* is reached**.
- **If it is not reached**, the insurer must instead **pay the *Rückkaufswert* attributable to the
  insurance, including *Überschussanteile*, under § 169**. Below the minimum the paid-up election
  **becomes a surrender**; a model that offers *Beitragsfreistellung* without the test is wrong.
- The **prämienfreie Leistung** is calculated **by recognised actuarial rules, with the
  *Rechnungsgrundlagen der Prämienkalkulation*, on the basis of the *Rückkaufswert* under
  § 169 Abs. 3 bis 5**, and **must be stated in the contract for each *Versicherungsjahr***. Two
  structural consequences: the paid-up benefit is a **function of the surrender value** and
  inherits the five-year spreading floor; and the schedule of paid-up sums by year is
  **contractual and tabulated at issue**, not computed at the time of election.
- It is struck at period end **taking account of any *Prämienrückstände***. Practical note from the
  same summary: attached *Zusatzversicherungen* — a *Berufsunfähigkeits-Zusatzversicherung*, say —
  are **regularly lost** when the main contract is made paid-up.

### R4 — VVG § 161, *Selbsttötung*
- **Retrieved (2026-08-30): yes**, canonical XML, `Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156`;
  `__161.html` is a 4 kB shell. Confirmed in all three Absätze. One refinement: Abs. 2 permits the
  three-year period to be **increased** ("erhöht") by individual agreement and says nothing about
  shortening it — but § 171 makes § 161 *halbzwingend*, so a shorter window is lawful as more
  favourable to the policyholder, and S7 § 4 Abs. 1 writes **two** years. The three years are a
  ceiling on the insurer's relief, not a market constant.
- Publisher: Bundesministerium der Justiz; mirrored by dejure.org, lxgesetze.de, buzer.de,
  rewis.io, juraforum.de, NWB, gesetze-in-app.de, Haufe
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__161.html ·
  https://dejure.org/gesetze/VVG/161.html · https://rewis.io/gesetze/vvg/p/161-vvg/
- In an insurance **for the event of death** the insurer is ***leistungsfrei*** if the *versicherte
  Person* **intentionally takes her own life before three years have elapsed since conclusion of
  the contract**.
- **Exception**: not so where the act was committed **in a state excluding free determination of
  the will, caused by a *krankhafte Störung der Geistestätigkeit***.
- **The three-year period may be extended by individual agreement** — a statutory minimum window,
  extendable and by implication not shortenable.
- **Where the insurer is *leistungsfrei* it must nevertheless pay the *Rückkaufswert*, including
  *Überschussanteile*, under § 169.** The German rule is a **benefit substitution**, not a forfeiture
  — materially unlike art. L. 132-7 of the French Code des assurances, where the cover is "de nul
  effet" in the first year and there is no surrender value to fall back on. Located in **Chapter 5**.

### R5 — VVG § 19, *Vorvertragliche Anzeigepflicht*
- **Retrieved (2026-08-30): yes**, canonical XML, `Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156`;
  `__19.html` is a 6 kB shell. Confirmed. Two points the summaries did not carry: Abs. 5 makes every
  one of the insurer's rights conditional on a separate *Textform* warning, and Abs. 6 gives the
  policyholder an immediate right to cancel where a retrospective contract change raises the premium
  by more than **10 Prozent** or excludes the undisclosed risk. **The five- and ten-year limits
  recorded below are in § 21 Abs. 3 VVG, not § 19**; § 21 was not retrieved and the exact locus stays
  `[unverified]`.
- Publisher: Bundesministerium der Justiz; commentary from ra-zn.de, fairtest.de,
  versicherungsrechtsiegen.de, Kanzlei Johannsen
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__19.html (canonical form) ·
  https://www.ra-zn.de/anzeigepflicht-19-vvg · https://fairtest.de/recht/19-vvg-anzeigepflichten.html
- **Abs. 1 Satz 1** obliges the policyholder to disclose the *gefahrerhebliche Umstände* known to
  her **which the insurer has asked about in *Textform***. The duty is question-bounded.
- The provision is described as giving the insurer the right to put health questions in order to
  assess the risk and decide whether to accept **with restrictions** or **only at an increased
  premium**.
- **Remedies.** On a breach the insurer may **adjust the contract retrospectively** — **excluding the
  undisclosed risk from cover** or **raising the premium by a *Risikozuschlag*** — instead of
  refusing to perform; for simple or gross negligence this is reported as the usual outcome.
- **Time limits.** The adjust / terminate / rescind rights **lapse five years** after conclusion for
  negligent breach and **ten years** for **intentional or *arglistig*** breach.

### R6 — MindZV, *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung*
- **Retrieved (2026-08-30): yes**, canonical XML from `gesetze-im-internet.de/mindzv_2016/xml.zip`,
  `Stand: Zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688`; the consolidated `BJNR083100016.html`
  page is itself substantive. The three quotas are confirmed and located: § 6 Abs. 1 for the
  *Kapitalanlageergebnis*, § 7 for the *Risikoergebnis* (90 %), § 8 for the *übriges Ergebnis*
  (50 %), with § 4 Abs. 1 defining all three by *Versicherungsberichterstattungs-Verordnung* line
  items and requiring "Alt- und Neubestand ... getrennt betrachtet". **One correction.** What § 6
  Abs. 1 deducts before the 90 % is struck is the ***rechnungsmäßige Zinsen*** — "90 Prozent der nach
  § 3 Absatz 1 anzurechnenden Kapitalerträge abzüglich der rechnungsmäßigen Zinsen" — not the
  *Aufwand für die Diskontierung der Deckungsrückstellung* recorded below. The economic reading is
  unaffected: the guarantee is taken off the top before the policyholder's interest share is struck.
  § 6 Abs. 2 adds a 90 % minimum for the collective part of the RfB under § 140 Abs. 4 VAG.
- Publisher: Bundesministerium der Justiz; mirrored by lxgesetze.de, buzer.de, freirecht.de;
  explained by Wikipedia and ASCORE
- URLs: https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html ·
  https://lxgesetze.de/mindzv/6 · https://www.buzer.de/gesetz/12013/a198221.htm ·
  https://de.wikipedia.org/wiki/Mindestzuf%C3%BChrungsverordnung
- **§ 6 MindZV, *Kapitalanlageergebnis*.** The minimum allocation to the *Rückstellung für
  Beitragsrückerstattung* in respect of investment income for *überschussberechtigte* contracts is
  **90 % of the *anzurechnende Kapitalerträge* determined under § 3 Abs. 1**.
- **Risikoergebnis.** The minimum allocation in respect of the risk result is **90 % of the
  *Risikoergebnis* attributable to *überschussberechtigte* contracts**.
- **The aggregate test.** The total allocation must be at least **90 % of the total investment
  income attributable pro rata to policyholder liabilities, less the *Aufwand für die Diskontierung
  der Deckungsrückstellung*; plus 90 % of the *Risikoergebnis*; plus 50 % of the *übriges
  Ergebnis***. Deducting the discounting charge before the 90 % is applied is the mechanism by
  which the guaranteed interest is taken off the top before the policyholder's interest share is
  struck.
- **The minimum is computed and complied with separately for *Altbestand* and *Neubestand***; an
  endowment written today is *Neubestand*. The identifiers `mindzv_2016` and `BJNR083100016` in the
  canonical URL indicate the **2016 consolidation**.

### R7 — DeckRV, *Deckungsrückstellungsverordnung* — *Höchstrechnungszins* and *Höchstzillmersatz*
- **Retrieved (2026-08-30): yes** — the DeckRV as canonical XML (`Stand: Zuletzt geändert durch
  Art. 1 V v. 19.7.2024 I Nr. 250`) and the buzer.de amendment history as HTML. § 2 Abs. 1 Satz 1:
  "wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf **1 Prozent**
  festgesetzt". § 4 Abs. 1 Satz 2: "Der Zillmersatz darf **25 Promille der Summe aller Prämien**
  nicht überschreiten" — note the statutory base is the *Summe aller Prämien*, which the market calls
  the *Beitragssumme*. **The cohort keying is itself statutory**, which was an inference before:
  § 2 Abs. 2 Satz 1 fixes the *Rechnungszins* used at conclusion "für die gesamte Laufzeit des
  Vertrages" and § 4 Abs. 4 does the same for the *Zillmersatz*. **The dating tag is
  discharged and the date corrected**: buzer's *Fassung* line reads "Artikels 1 Sechste Verordnung zur
  Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz V. v. **19. Juli 2024** BGBl. 2024
  I Nr. 250 **m.W.v. 1. Januar 2025**" — 19 July, not 24 July, and the 1 January 2025 effective date
  is confirmed. The pre-2025 rate history and the 2015 date of the 25 ‰ cut are not in the current
  consolidated text and still rest on S15, R15, R29 and REG-R15.
- Publisher: Bundesministerium der Justiz; buzer.de carries the amendment history
- URL: https://www.buzer.de/gesetz/12006/index.htm
- **Höchstrechnungszins** raised **from 0,25 % to 1,00 % with effect from 1 January 2025**; the
  amending regulation was announced in the *Bundesgesetzblatt* on **24 July** (the year was given
  only as context and is inferred to be **2024**; `[unverified]`, gap 12).
- **History.** The rate fell continuously **from 4 % in 1994 to 0,25 % in 2022**; the 2025 increase
  is the **first increase since 1994**. Three independent results — an insurer blog, a trade
  magazine and a consumer-pensions portal — agree on the 4 %-1994 / 0,25 %-2022 / 1,0 %-2025
  sequence.
- **Process.** The DAV **recommended 1 % in November 2023**; the Bundesfinanzministerium **adopted it
  in late April 2024** and consulted on the DeckRV amendment [R15]; the GDV supported it [R16].
- **Höchstzillmersatz.** The *Zillmersatz* **may not exceed 25 ‰ of the sum of all premiums** (the
  *Beitragssumme*), cut **from 40 ‰** by the LVRG with effect from **1 January 2015**; in the
  balance sheet the undertaking may therefore recognise only **2,5 % of the *Beitragssumme*** as
  *Abschluss- und Vertriebskosten*. Corroborated by [S15] and [R29].

### R8 — VAG § 139, *Überschussbeteiligung*, and the *Sicherungsbedarf*
- **Retrieved (2026-08-30): yes**, canonical XML from `gesetze-im-internet.de/vag_2016/xml.zip`,
  `Stand: Zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81`; the dejure.org mirror was read
  too. Abs. 3 and Abs. 4 confirm the *Sicherungsbedarf* rule, and **narrow it**: the cut-back bites
  on "Bewertungsreserven aus direkt oder indirekt vom Versicherungsunternehmen gehaltenen
  **festverzinslichen Anlagen und Zinsabsicherungsgeschäften**", not on the whole of the
  *Bewertungsreserven*. Abs. 4 defines the *Sicherungsbedarf* as the sum over contracts whose
  *maßgeblicher Rechnungszins* exceeds the *Bezugszins* of the actuarially valued interest obligation
  less the *Deckungsrückstellung*. **The *Sockelbetrag* tag is discharged and the fact relocated**:
  it is not in § 139 at all, but three retrieved documents carry it as a contractual and declaratory
  minimum — the "Sockelbeteiligung an Bewertungsreserven" of the GDV Muster-Standmitteilung (S2), the
  *Mindestbeteiligung* in *Anlage 1* to S9, and S18 § 2 Abs. 6. Its **existence** is established; its
  **size** is not, and all three say it can fall away.
- Publisher: Bundesministerium der Justiz; summary obtained through dejure.org
- URL: https://dejure.org/gesetze/VAG/139.html
- Policyholders are **in principle to share in the *Bewertungsreserven* to the extent of one
  half**, subject to important restrictions.
- **Participation by exiting policyholders is permitted only to the extent that the
  *Bewertungsreserven* exceed any *Sicherungsbedarf* arising from contracts with an interest
  guarantee.**
- ***Sicherungsbedarf*** is the sum, over contracts with an **überhöhter Rechnungszins**, of the
  **actuarially valued interest obligation less the *Deckungsrückstellung***. Purpose, as reported:
  to counter the fear, fuelled by the prolonged low-interest period, that life insurers would no
  longer be able to meet the benefits they had guaranteed.
- A ***Sockelbetrag*** — a floor participation calculated under the LVRG — is mentioned by one
  weak secondary source only; its existence, base and size are `[unverified]` (gap 8).

### R9 — VVG-InfoV § 2, and the *Effektivkosten* disclosure
- **Retrieved (2026-08-30): yes** — § 2 VVG-InfoV in full from
  `gesetze-im-internet.de/vvg-infov/__2.html`, which for this small instrument serves the norm text
  rather than a frameset, plus the buzer.de mirror. Abs. 1 Nr. 1 requires the *einkalkulierte
  Abschlusskosten* "als einheitlicher Gesamtbetrag" and the other costs, *Verwaltungskosten*
  separately, as a share of the annual premium with the term; Abs. 2 puts Nr. 1, 2, 4 and 5 **in
  Euro**. Abs. 1 Nr. 4 to 6 require the *Rückkaufswerte*, the *Mindestversicherungsbetrag* for a
  conversion, and the extent to which both are guaranteed — the statutory origin of the
  *Garantiewerttabelle* that S7 and S18 refer the reader to. Abs. 1 Nr. 9 defines the *Effektivkosten*
  as "die Minderung der Wertentwicklung durch Kosten in Prozentpunkten ... bis zum Beginn der
  Auszahlungsphase", and **Abs. 6 fixes the method**: they "werden berechnet wie der
  Gesamtkostenindikator nach Anhang VI der Delegierten Verordnung (EU) 2017/653". Abs. 3, new to this
  entry, quantifies the § 154 VVG *Modellrechnung*: "dem Höchstrechnungszinssatz, multipliziert mit
  1,67", and that rate ± one percentage point. **The date the *Effektivkosten* duty was introduced is
  still not established from the instrument** and remains `[unverified]`.
- Publisher: Bundesministerium der Justiz; mirrored by buzer.de and freiRecht.de; explained by the
  Institut für Finanz- und Aktuarwissenschaften (ifa Ulm)
- URLs: https://www.gesetze-im-internet.de/vvg-infov/__2.html ·
  https://www.buzer.de/gesetz/8025/a153312.htm ·
  https://www.ifa-ulm.de/index.php?id=41&tx_ttnews%5Btt_news%5D=486&cHash=0f2266fa054d0c32b0a0c2e018ae0ed2
- **§ 2 VVG-InfoV** is headed *Informationspflichten bei der Lebensversicherung, der
  Berufsunfähigkeitsversicherung und der Unfallversicherung mit Prämienrückgewähr* — one provision
  covering all three savings-bearing personal lines. The legal basis for the cost disclosure is
  **§ 7 Abs. 2 und 3 VVG i. V. m. §§ 2 und 3 VVG-InfoV**, requiring disclosure of the ***Abschluss-
  und Vertriebskosten* included in the premium, in euro amounts**.
- The **Effektivkostenquote (Reduction in Yield, RIY)** was introduced in quotations **with effect
  from 1 January 2015**, following the **LVRG of 2014**; **later VVG-InfoV amendments closed gaps** in
  that regime (the ifa note concerns an amendment to the *Effektivkosten* calculation; **its date was
  not established**). The metric discloses **all costs — acquisition, ongoing and investment —
  expressed as a reduction of the contract's yield**.

### R10 — EStG § 20 Abs. 1 Nr. 6, and the *Einkommensteuer-Handbuch* annex
- **Retrieved (2026-08-30): yes for the statute, no for the handbook.** §§ 20 and 52 EStG were read
  as canonical XML, `Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197`; the Haufe
  commentary was read as HTML. The *Einkommensteuer-Handbuch* URL answers 200 with a Radware
  interstitial ("Verifying your browser before proceeding") and no document body, so **the annex
  itself is not retrieved**. Satz 1 and Satz 2 are confirmed word for word. **The `[unverified]` on
  the age-62 locus is resolved and the citation corrected**: it is **§ 52 Absatz 28 Satz 7** EStG —
  "§ 20 Absatz 1 Nummer 6 Satz 2 ist für Vertragsabschlüsse nach dem 31. Dezember 2011 mit der
  Maßgabe anzuwenden, dass die Versicherungsleistung nach Vollendung des 62. Lebensjahres des
  Steuerpflichtigen ausgezahlt wird" — not § 52 Abs. 36 Satz 9.
- Publisher: Bundesministerium der Finanzen (amtliches Einkommensteuer-Handbuch); commentary from
  NWB, IWW, smartsteuer, Haufe, Gonze & Schüttler
- URLs: https://esth.bundesfinanzministerium.de/esth/2024/C-Anhaenge/Anhang-22a/I/inhalt.html ·
  https://datenbank.nwb.de/Dokument/357065/ ·
  https://www.haufe.de/steuern/steuerwissen-tipps/nach-dem-31122004-abgeschlossene-lebensversicherungen_170_448252.html
- The taxable amount is the ***Unterschiedsbetrag*** between the *Versicherungsleistung* and the
  *Beiträge*.
- **The half-income rule.** Where the benefit is paid **after completion of the 60th year of life
  and after twelve years since conclusion**, **only half the *Unterschiedsbetrag*** is taxable —
  § 20 Abs. 1 Nr. 6 Satz 2 EStG.
- **The age-62 tightening.** For contracts **concluded after 31 December 2011** the required age is
  **completion of the 62nd year**, cited to **§ 52 Abs. 36 Satz 9 EStG**; EStG § 52 has been
  renumbered repeatedly and the current locus is `[unverified]`.
- **Rate.** Where the benefit accrues **from 1 January 2009** and the halving applies, the flat
  *Abgeltungsteuer* does **not** apply; the **personal marginal rate** applies to the half amount —
  **§ 32d Abs. 2 Nr. 2 EStG**.
- **Withholding.** Under **§ 43 Abs. 1 Nr. 4 Halbsatz 2 EStG** the halving is **disregarded for
  *Kapitalertragsteuer* purposes**, i.e. given effect on assessment rather than at source. The
  reading is recorded as the summary put it; the mechanism is `[unverified]`.

### R11 — BMF-Schreiben of 1 October 2009, IV C 1 - S 2252/07/0001
- **Retrieved (2026-08-30): partly.** The NWB record page was read; the Randnummern are behind a
  subscription login and **no paragraph of the text is established**. What the record adds: the
  *Bundessteuerblatt* citation **BStBl 2009 I S. 1172**, the official subject "Besteuerung von
  Versicherungserträgen im Sinne des § 20 Absatz 1 Nummer 6 EStG", and the full *Gliederung* I to
  XIV — including "IV. Kapitalversicherung mit Sparanteil / 1. Kapitalversicherung auf den Todes- und
  Erlebensfall (klassische Kapital-Lebensversicherung)", "IV. 4. Kapitalversicherung mit festem
  Auszahlungszeitpunkt (Termfixversicherung)" and "X. Hälftiger Unterschiedsbetrag / 6.
  Mindesttodesfallschutz". The guidance is therefore located precisely and the relevant section
  confirmed to exist; **nothing is quoted from it anywhere in delib**.
- Publisher: Bundesministerium der Finanzen. Doc type: *BMF-Schreiben*, binding administrative
  guidance to the tax offices
- URL: https://datenbank.nwb.de/Dokument/351401/ (NWB database record)
- Identified as the guidance on the **taxation of insurance income** covering the post-2004 regime,
  and reported by a trade journal as the instrument in which "the BMF re-regulated important points"
  for life and annuity contracts. **The reference and date were returned by the search; no paragraph
  of its text was established.**

### R12 — *Mindesttodesfallschutz*: the 50 %-rule for contracts concluded from 1 April 2009
- **Retrieved (2026-08-30): yes** for both commentaries — **and the rule itself is now read in the
  statute**, § 20 Abs. 1 Nr. 6 Satz 6 EStG, which supersedes them as the authority. The statutory
  form is narrower than the summaries: the halving is disapplied only where **both** limbs hold —
  (a) "in einem Kapitallebensversicherungsvertrag **mit vereinbarter laufender Beitragszahlung in
  mindestens gleichbleibender Höhe** bis zum Zeitpunkt des Erlebensfalls die vereinbarte Leistung bei
  Eintritt des versicherten Risikos **weniger als 50 Prozent der Summe der für die gesamte
  Vertragsdauer zu zahlenden Beiträge** beträgt", and (b) that benefit does not exceed the
  *Deckungskapital* or *Zeitwert* "**spätestens fünf Jahre nach Vertragsabschluss** ... um mindestens
  10 Prozent des Deckungskapitals, des Zeitwerts oder der Summe der gezahlten Beiträge". **The
  tag on the second limb is discharged in full**: its base is any of the three named, its
  time profile is the five-year point, and the trailing words that would not parse are its own second
  sentence — "Dieser Prozentsatz darf bis zum Ende der Vertragslaufzeit in jährlich gleichen Schritten
  auf Null sinken." § 52 Abs. 28 Satz 8 applies the provision to contracts concluded after 31 March
  2009 **or whose first premium was paid after that date**, an alternative the summaries omitted.
- Publisher: Haufe (Haufe Finance Office Premium) and IWW (*Wirtschaftsberatung aktuell*)
- URLs:
  https://www.haufe.de/finance/haufe-finance-office-premium/kapitallebensversicherungen-einkommensteuer-312-mindesttodesfallschutz-bei-lebensversicherungen_idesk_PI20354_HI8459274.html ·
  https://www.haufe.de/id/beitrag/kapitallebensversicherungen-einkommensteuer-3121-einzelheiten-der-50-regel-HI8459275.html ·
  https://www.iww.de/wvm/archiv/kapitallebensversicherungen-neuer-mindesttodesfallschutz-fuer-ab-dem-1-april-2009-abgeschlossene-vertraege-f14610
- **For contracts concluded from 1 April 2009** the *Todesfallleistung* must be **at least 50 % of
  all premiums payable over the whole term**. Two independent sources give the figure and the date;
  a third names the rule the **"50 %-Regel"**.
- **A second condition** is reported: on death, the agreed *Versicherungsleistung* must **exceed the
  *Deckungskapital* or the *Zeitwert* by at least 10 %**. The summary attaches the words "after
  five years", which does not parse as a rule. **The 10 % figure is recorded; its base, its time
  profile and the qualifier are `[unverified]`** — gap 11.
- **Failing the test** means full taxation of the earnings under the *Abgeltungsteuer* with no
  halving; meeting it opens the half-income rule subject to the conditions of [R10].

### R13 — The pre-2005 regime and the 2004/2005 boundary
- **Retrieved (2026-08-30): yes** for the Haufe and Bund-der-Steuerzahler pages. The 2005 boundary is
  now read in the statute itself — § 20 Abs. 1 Nr. 6 Satz 1 applies "wenn der Vertrag nach dem
  31. Dezember 2004 abgeschlossen worden ist" [R10]. **The conditions of the pre-2005 regime remain
  `[unverified]`**: the current statute knows the old regime only through transitional provisions, and
  the retrieved commentary states the conditions only in outline. S12 gives the outline a carrier's
  voice — a pre-2005 death benefit is tax-free only where the contract met "die damaligen
  Voraussetzungen einer steuerbegünstigten Kapitallebensversicherung ... (Mindestlaufzeit 12 Jahre,
  laufende Beitragszahlung, Mindesttodesfallschutz)" — and nothing in delib asserts them.
- Publisher: Haufe; Bund der Steuerzahler; happe.de; firmenabc.com; VLH; smartsteuer
- URLs:
  https://www.haufe.de/steuern/steuerwissen-tipps/nach-dem-31122004-abgeschlossene-lebensversicherungen_170_448252.html ·
  https://www.happe.de/steuernews_mandanten/januar_2025/kapitallebensversicherungen_vor_2005/ ·
  https://steuerzahler.de/bayern/newsticker-archiv/newsticker/news/kapitallebensversicherungen-versteuerungsregeln-sehr-differenziert/ ·
  https://www.vlh.de/kaufen-investieren/geldanlage/lebensversicherung-und-steuer-das-muessen-sie-beachten.html
- **For contracts concluded from 2005 onwards** the **difference between the amount paid out and
  the premiums paid in is taxable**, and **premiums are not deductible**. For contracts running
  since before 2004 and then sold, the proceeds were reported as not taxed.
- The 1 January 2005 boundary is the **Alterseinkünftegesetz** cut-off. **The conditions of the old
  regime — the twelve-year term, the five-year minimum premium-paying period and a minimum death
  cover expressed as a percentage of the *Beitragssumme* — were not established by any search
  result** and are `[unverified]`; they are not asserted anywhere in delib (gap 13). Bund der
  Steuerzahler characterises the rules as *sehr differenziert* — the practical warning that a German
  endowment book carries at least three tax cohorts.

### R14 — DAV, "Herleitung der Sterbetafel DAV 2008 T für Lebensversicherungen mit Todesfallcharakter"
- **Retrieved (2026-08-30): yes.** Both PDFs — the 2008 derivation paper and the *Richtlinie* of
  29 November 2022, 49 pp. **The table values themselves are not redistributed anywhere in delib.**
  Two corrections and one answer.
  **(a) The observation period is 2001 to 2004**, not 2006–2008: "Als Beobachtungszeitraum werden die
  Jahre 2001 bis 2004 zu Grunde gelegt." 2006–2008 is when the DAV working group did the work, which
  the *Richtlinie* states separately — the two were conflated. The data are the pooled portfolios of
  Gen Re, Münchener Rück, Swiss Re and the Verband öffentlicher Versicherer, **47 undertakings** and
  more than **100 million *Bestandsjahre***, read against the *Sterbetafeln des Statistischen
  Bundesamts*.
  **(b) The 60 % coverage is confirmed exactly**: "Nach dieser Bereinigung weisen die untersuchten
  Versichertendaten eine Abdeckung von 60% des deutschen Versicherungsmarktes im Bereich der
  Kapitallebensversicherungen auf; im Bereich der Risikolebensversicherungen sind es sogar 70%."
  **(c) The open question is answered: there is no separate endowment table.** DAV 2008 T is a single
  *Schlusstafel* derived from data from the sixth policy year onwards to eliminate selection; about
  91 % of the observations come from *Kapitallebensversicherungen*, and endowment mortality from the
  sixth year is 101 % of the all-tariff level. The *Sicherheitszuschläge* method is confirmed —
  *Schwankungs-*, *Irrtums-* and *Änderungsrisiko*, with the *Schwankungszuschlag* struck on a model
  portfolio of 200.000 lives aged 20 to 65 — and the suitability limit reads, verbatim: "Die
  Sterbetafel DAV 2008 T ist grundsätzlich auch für die Beitragskalkulation von Lebensversicherungen
  mit Todesfallcharakter, **ausgenommen Tarife ohne Gesundheitsprüfung**, geeignet"
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV). Doc type: *Fachgrundsatz* / *DAV-Richtlinie*,
  with a 2008 derivation paper and a 2022 restatement
- URLs:
  https://aktuar.de/de/wissen/fachinformationen/detail/herleitung-der-sterbetafel-dav-2008-t-fuer-lebensversicherungen-mit-todesfallcharakter/ ·
  https://aktuar.de/content/PDF/Fachwissen/20080708_DAV_2008_T.pdf ·
  https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf ·
  https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T_R_NR.pdf
- The DAV *Arbeitsgruppe Biometrische Rechnungsgrundlagen* investigated mortality in life insurance
  **with *Todesfallcharakter*** over **2006 to 2008**, using **German insurers' own policy data** with
  **German population statistics** and comparing against international developments. **After
  cleansing, the insured data covered 60 % of the German market in the *Kapitallebensversicherung*
  segment**; the term-life figure was truncated in the summary and is not established.
- The *Richtlinie* **regulates the methodology for deriving mortality tables for reserving and the
  procedure for setting the *Sicherheitszuschläge***. **DAV 2008 T R** and **DAV 2008 T NR** — smoker
  and non-smoker — are in principle **also suitable for premium calculation** differentiated by
  smoking status, **but not for policies written without a *Gesundheitsprüfung***.
- **First adopted as a DAV-Richtlinie on 4 December 2008**; restated as a *Fachgrundsatz* dated
  **29 November 2022**. **The table values are not public and delib does not redistribute them.**
  DAV 2008 T is a **death-benefit** table, and whether the DAV maintains a separate first-order table
  for endowment business specifically **was not established** — gap 14.

### R15 — DAV recommendations on the *Höchstrechnungszins* for 2025 and 2026
- **Retrieved (2026-08-30): yes**, both newsroom items as HTML. Nothing below is contradicted.
- Publisher: Deutsche Aktuarvereinigung e. V.
- URLs:
  https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-empfiehlt-auch-fuer-2026-einen-hoechstrechnungszins-in-hoehe-von-1-prozent/ ·
  https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-begruesst-ministeriumsvorstoss-zum-hoechstrechnungszins-2025/
- The DAV **recommends a *Höchstrechnungszins* of 1,0 % for 2026 as well** — the 1,00 % rate
  effective 1 January 2025 carried forward unchanged. The second item records the DAV welcoming the
  ministry's move on the 2025 rate. The point worth carrying into the delib specification: **the
  maximum technical rate is set by regulation but proposed by the actuarial profession**, and the
  professional recommendation was adopted in both cycles evidenced here.

### R16 — GDV, "Höchstrechnungszins-Erhöhung ist eine 'angemessene Reaktion auf gestiegene Zinsen'"
- **Retrieved (2026-08-30): yes**, HTML. Adds no independent figure, as recorded.
- Publisher: GDV (Medieninformation)
- URLs:
  https://www.gdv.de/gdv/medien/medieninformationen/hoechstrechnungszins-erhoehung-ist-eine-angemessene-reaktion-auf-gestiegene-zinsen--176848 ·
  https://www.gdv.de/gdv/medien/medieninformationen/versicherer-befuerworten-anhebung-des-hoechstrechnungszinses--157548
- The industry association's public support for the increase to 1,0 %, described as an appropriate
  reaction to risen interest rates. Corroborates [R7] and [R15]; adds no independent figure.

### R17 — BaFin, Merkblatt 01/2023 (VA), *zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden Lebensversicherungsprodukten*
- **Retrieved (2026-08-30): yes** for the *Merkblatt*, whose full text (Rn. 1 ff., sections A to D) is
  served on the page; **no** for the press release, which is HTTP 404 at the cited URL. The reading
  confirms that **the *Merkblatt* states no numerical threshold of any kind** — the "über vier
  Prozent" figure belongs to R18 and is a survey finding, not a limit. What the text adds: Rn. 2
  defines *kapitalbildende Lebensversicherungsprodukte* as classic and unit-linked life products with
  a savings component, including *Direktversicherungen* and AltZertG contracts; Rn. 15 requires
  undertakings to formulate *Renditeziele* consistent with the target market and to consider "nicht
  nur eine positive Rendite nach Kosten, sondern auch eine positive Rendite nach Kosten und Inflation",
  with the ECB medium-term inflation target as a candidate benchmark and attainment tested "mit
  geeigneten stochastischen Analysen"; Rn. 18 names the *Effektivkosten* under § 2 Abs. 1 Nr. 9
  i. V. m. § 2 Abs. 6 VVG-InfoV as the cost measure; Rn. 23 addresses *Storno*; and Rn. 52 suggests
  tying a high *Abschlussprovision* to the intermediary's own *Stornoquote*. **One qualification.**
  The *Renditeziel* duty is not flat: Rn. 16 and 17 provide that for a *sicherheitsorientiert* target
  market the value of the guarantee may take precedence and "die Formulierung eines Renditeziels ...
  ist dann gegebenenfalls entbehrlich", naming "klassische Lebensversicherungsprodukte ohne
  fondsgebundene Komponenten" — this product — as the paradigm case.
- Publisher: BaFin. Doc type: supervisory *Merkblatt*, published **May 2023**
- URLs:
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html ·
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Pressemitteilung/2023/pm_2023_05_08_Merkblatt_kapitalbildende_LV.html ·
  https://www.bafin.de/SharedDocs/Downloads/DE/Anlage/dl_mb_Wohlverhaltensaufsicht_kapitalbild_LV_Produkte_Entwurf_final.pdf?__blob=publicationFile&v=1 (consultation draft)
- **The most important supervisory document for this product**, and the reason delib treats charge
  levels as a supervised rather than a free parameter. **Purpose**: to ensure that kapitalbildende
  Lebensversicherungsprodukte offer an appropriate ***Kundennutzen***.
- **Cost.** The *Effektivkosten* of different providers and products **differ considerably**. BaFin
  will **closely examine** undertakings whose *Effektivkosten* are **very high compared with
  industry norms**, and whose ***Aufwendungen für Versicherungsvermittler*** are **notably high**.
- **Return.** The manufacturer must **formulate a *Renditeziel* for the defined target market,
  achievable with sufficient probability**, consistent with that target market's expectations and
  with product characteristics and capital-market conditions. For retirement-provision products
  BaFin requires that the product **achieve a real investment success with sufficient probability —
  a return net of costs exceeding a justified inflation expectation**.
- **No numerical threshold was established** — not for *Effektivkosten*, not for commission, not
  for the real return. Any figure attributed to the *Merkblatt* would be an invention. Gap 7.

### R18 — BaFin, *Risiken im Fokus 2026* — "Kosten von kapitalbildenden Lebensversicherungen"
- **Retrieved (2026-08-30): yes**, the full chapter text as HTML — so the note below that "no text of
  the chapter was established" is superseded, and this becomes the only source of supervisory
  quantities in the corpus. Market size: "Im Jahr 2024 gab es hierzulande rund **59 Millionen**
  kapitalbildende Lebensversicherungen. **2,4 Millionen** Verträge wurden in dem Jahr neu
  abgeschlossen" — on the *Merkblatt*'s broad definition, so classic and unit-linked together. Costs:
  a 2022 survey of first-half-2021 new business found "**In Einzelfällen beliefen sich die
  Effektivkosten auf über vier Prozent**"; a repeat survey in 2025 covering 2024 new business found
  them falling since 2021, "vor allem bei den verkaufsstarken langen Laufzeiten war im oberen Viertel
  ein Rückgang der Effektivkosten um mehr als 0,4 Prozentpunkte zu beobachten". Lapse: "Einige
  Lebensversicherungsprodukte sind mit sehr hohen Stornoquoten aufgefallen – speziell in den ersten
  Jahren nach Vertragsabschluss, in denen ein großer Teil der Kosten anfällt", high early lapse being
  treated as evidence of an inadequate *Kundennutzen*. Enforcement: products withdrawn, cost
  reductions in the in-force book, retrospective compensation, and *Verwarnungen* to individual
  *Geschäftsleiter*.
- Publisher: BaFin. Doc type: annual supervisory risk-focus publication, 2026 edition,
  consumer-protection chapter
- URLs:
  https://www.bafin.de/DE/die-bafin/publikationen-daten/risiken-im-fokus/Fokusrisiken_2026/RIF_Verbraucher_3/RIF_verbraucher_lebensversicherung_node.html ·
  https://www.bafin.de/DE/Aufsicht/Fokusrisiken/Fokusrisiken_2026/RIF_verbraucher_lebensversicherung/RIF_verbraucher_lebensversicherung_node.html
- Establishes that **"Kosten von kapitalbildenden Lebensversicherungen" is a named focus risk in
  BaFin's 2026 risk agenda** — three years after the *Merkblatt*, the supervisor still treats this
  product's charge level as an open problem. **No text of the chapter was established.**

### R19 — BaFin *Fachartikel*: "Wenn Lebensversicherungen zu viel kosten" (2022), "PRIIPs-Verordnung: Wie Versicherer Verbraucher informieren" (2022), "Kundennutzen im Fokus" (2024)
- **Retrieved (2026-08-30): partly.** The 2022 *Effektivkosten* article and the 2024 *Kundennutzen*
  article were read as HTML; **the PRIIPs *Surfday* article is HTTP 404** at the cited URL. With it
  gone, the BIB content list below is better evidenced by the retrieved BIB itself at S10, which
  prints every one of those fields.
- Publisher: BaFin (BaFinJournal / Fachartikel)
- URLs:
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2203_Effektivkosten_Versicherer.html ·
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2207_priips_surfday.html ·
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2024/bafin_fachartikel_wohlverhalten.html
- The PRIIPs article establishes the **content requirements of a *Basisinformationsblatt***: a
  **total risk indicator**; the **possible maximum loss of invested capital**; **suitable performance
  scenarios**; the **costs the investor bears**; and how and where to complain. **Four graded
  scenarios — *Stress*, *pessimistisch*, *moderat*, *optimistisch* — must be given as annualised
  average returns in per cent** at **three time points: after one year, after half the term, and at
  the end of the term**; **total costs and the *Reduction in Yield* per year are shown at those same
  points**, split into **one-off and ongoing costs**. The ***Effektivkosten* of a specimen contract
  must be stated in the BIB**, which must be **published on the insurer's website** and **provided
  before conclusion**. The 2022 cost and 2024 conduct articles corroborate [R17] without new figures.

### R20 — GDV, "Die deutsche Lebensversicherung in Zahlen 2024" and the Jahresmedienkonferenz page
- **Retrieved (2026-08-30): yes.** PDF, 40 pp., *Redaktionsschluss* 27.06.2024; the
  Jahresmedienkonferenz page as HTML. **Both *Stornoquote* figures below are corrected.** The
  publication titled *2024* reports the **2023** financial year and gives **one** measure, not two:
  "Die Stornoquote (**Anzahl**) stieg im Jahr 2023 leicht auf **2,56 %** (Vorjahr: 2,51 %)." So
  2,56 % is the **count** measure, and the 2,72 % attributed to 2024 and the separate 1,2 % count
  measure are **not in this document** and are not established anywhere in the corpus. Gap 10 is
  restated rather than closed: there are not two irreconcilable measures, there is one unsuitable
  one — a headline count over all life business, not endowment-specific and not split by duration.
  **Retrieval also supplies the endowment-specific figures the corpus lacked.** In force at
  31 December 2023 by annual premium: "Der Anteil der Kapitalversicherungen (klassisch) lag Ende 2023
  bei **15,7 %** (Vorjahr: 17,0 %)", against 61,8 % for annuity and pension business. New
  regular-premium business 2023: klassische Kapitalversicherungen **158 Mio. Euro**, a **3,9 %**
  share, up 8,2 %. Single premiums 2023: 1,1 Mrd. Euro of 24,5 Mrd. total. APE 8,9 Mrd. Euro
  (−1,1 %); *Beitragssumme des Neugeschäfts* 175,4 Mrd. Euro (2022: 170,6). And the count series for
  *eingelöster Neuzugang* of klassische Kapitalversicherungen — **1.954,9 Tsd. (26,8 %) in 2000 →
  1.354,2 (18,5 %) 2005 → 742,1 (12,1 %) 2010 → 527,2 (10,3 %) 2015 → 392,3 (8,4 %) 2020 → 325,3
  (7,4 %) 2023** — which is the quantification of the post-2005 collapse that R21 records as
  missing.
- Publisher: GDV
- URLs:
  https://www.gdv.de/resource/blob/180978/b8ae8eb0b1bf4b15e7cc3354bc231af9/die-deutsche-lebensversicherung-in-zahlen-2024-publikation-pdf-data.pdf ·
  https://www.gdv.de/gdv/statistik/jahresmedienkonferenz-zahlen-und-daten/lebensversicherung-2024-165748
- The industry statistical annual. **Superseded by retrieval — see the `Retrieved` line above.** The
  figure the publication actually gives is "Die Stornoquote (**Anzahl**) stieg im Jahr **2023** leicht
  auf **2,56 %** (Vorjahr: 2,51 %)": one **count** measure, not two, and for 2023, not 2024. The
  2,72 %/2024 and 1,2 % figures recorded here before this pass are withdrawn. What remains true is
  that the measure covers all German life business and is **neither endowment-specific nor split by
  duration** (gap 10).

### R21 — GDV statistics, "Neugeschäft und Bestand der Lebensversicherer für die letzten zehn Geschäftsjahre"
- **Retrieved (2026-08-30): yes** for the HTML index of the series; the series themselves are
  download links and the figures used in delib come from R20, the same publisher's annual, which was
  retrieved in full. **The statement below that no endowment-specific new-business or in-force figure
  was established is withdrawn** — see R20. R20 also gives the two definitions verbatim: the APE adds
  10 % of single premiums to the annual premium assuming a ten-year term, while the *Beitragssumme*
  weights regular premiums by their payment term and adds the whole single premium, and is therefore
  "sehr viel größer als das APE".
- Publisher: GDV
- URLs:
  https://www.gdv.de/gdv/statistik/statistiken-zur-deutschen-versicherungswirtschaft-uebersicht/lebensversicherung/neugeschaeft-und-bestand-der-lebensversicherer-fuer-die-letzten-zehn-geschaeftsjahre-137804 ·
  https://www.gdv.de/gdv/statistik/statistiken-zur-deutschen-versicherungswirtschaft-uebersicht/lebensversicherung/neugeschaeft-und-bestand-in-der-lebensversicherung-im-weiteren-sinne-fuer-die-letzten-zehn-geschaeftsjahre-137802 ·
  https://www.gdv.de/gdv/statistik/statistiken-zur-deutschen-versicherungswirtschaft-uebersicht/lebensversicherung
- Establishes only the **shape of the published series**: for the *Bestand*, gross written premiums
  of the financial year; for the *Neugeschäft*, the ***Beitragssumme*** and the **Annual Premium
  Equivalent (APE)**, described as the measures of sales performance. **No endowment-specific
  new-business or in-force figure was established**, and in particular **no figure quantifying the
  post-2005 collapse of endowment new business**. Gap 3.

### R22 — BGH on the Debeka *Stornoabzug*: the *Bezifferung* requirement
- **Retrieved (2026-08-30): yes**, both reports as HTML. **Both tags are discharged**:
  LTO gives the citation in full — "Urt. v. **18.03.2026**, Az. **IV ZR 184/24**" — so the docket is
  no longer an inference from a URL slug and the decision date is established. The holding: the
  clause meets "die im Versicherungsvertragsgesetz (VVG) festgelegten Anforderungen an die
  Bezifferung des Abzugs gem. § 169 Abs. 5 S. 1 VVG" and does not offend § 307 Abs. 1 Satz 2 BGB;
  "Die Vorschrift verlange nicht, dass der Abzug bereits zu Vertragsschluss als konkreter Betrag
  vereinbart werde. 'Vielmehr kann der Versicherer auch auf die Regelung eines Berechnungsverfahrens
  für den Stornoabzug zurückgreifen.'" The BGH set aside the OLG Koblenz judgment and remitted, the
  *Angemessenheit* never having been examined below. **The rider that the procedure must leave the
  insurer no *Ermessensspielraum* is not in either retrieved report and is dropped rather than
  attributed.** The vzbv collective action covers contracts concluded after 2007 and cancelled from
  1 May 2022; about 500 people had joined at the date of the report.
- Publisher: Bundesgerichtshof; reported by LTO, LTMK, t-online, Cash.
- URLs:
  https://www.lto.de/recht/nachrichten/n/bgh-ivzr18424-debeka-stornogebuehr-transparenz-zurueckverweisung-olg-angemessen ·
  https://www.lto.de/recht/hintergruende/h/bgh-debeka-kapitalmarktabhaengiger-stornoabzug-kuendigung-lebensversicherung-gdv ·
  https://www.ltmk.de/kapitalmarktabhaengiger-stornoabzug-in-der-lebensversicherung-bgh-klaert-die-anforderungen-an-die-bezifferung/ ·
  https://www.cash-online.de/a/lebensversicherungen-der-debeka-sammelklage-wegen-strittiger-stornoklauseln-710778/
- The BGH **overturned a ruling of the OLG Koblenz and remitted**, holding that the Debeka clause
  **violated neither the statutory *Bezifferung* requirement nor the *Transparenzgebot***, and
  leaving ***Angemessenheit*** to be decided on remittal.
- The holding on *Bezifferung*: the requirement that a *Stornoabzug* be **"beziffert"** does **not**
  compel a concrete euro amount at conclusion. **It suffices that an unambiguous calculation
  procedure is agreed, provided it leaves the insurer no *Ermessensspielraum* and is free of
  unilateral determination rights.** A **capital-market-dependent** *Stornoabzug* is therefore lawful
  in principle, so the surrender deduction is not necessarily a constant.
- The docket appears in the LTO URL slug as **`bgh-ivzr18424`**, reading as **IV ZR 184/24** —
  **inferred from the slug**; the decision date was not established. Both `[unverified]`.

### R23 — BGH, judgment of 20 January 2021, IV ZR 318/19 — *Bewertungsreserven* after the LVRG
- **Retrieved (2026-08-30): yes**, the full judgment text from rewis.io. The disposition of the
  parallel constitutional challenge to § 153 Abs. 3 Satz 3 VVG is still **not established** and
  remains `[unverified]`.
- Publisher: Bundesgerichtshof; reported by rewis.io, NWB, RWS-Verlag, DATEV magazin, AssCompact
- URLs: https://rewis.io/urteile/urteil/e7b-20-01-2021-iv-zr-31819/ ·
  https://datenbank.nwb.de/Dokument/847241/ ·
  https://www.rws-verlag.de/aktuell/wirtschaftsrecht-aktuell/bgh-urteil-vom-20-januar-2021-iv-zr-31819-66390/
- The leading decision on the participation of **exiting** policyholders in the *Bewertungsreserven*
  after the LVRG of 1 August 2014. It confirms the structure at [R8]: the half share of
  § 153 Abs. 3 VVG is cut back by the *Sicherungsbedarf* on contracts with interest guarantees, and
  the cut-back was held lawful. A parallel line establishes a **constitutional challenge to
  § 153 Abs. 3 Satz 3 VVG in its LVRG form** before the BGH [R1]; **its disposition was not
  established.**

### R24 — The older BGH line on *Rückkaufswert* and *Stornoabzug* clauses (2001–2007)
- **Retrieved (2026-08-30): no.** The cited rechtsportal.de page answers **HTTP 429** (rate limited),
  and no alternative locus for the 2001–2007 line was retrieved. The entry is kept as a known
  reference and everything below still rests on the search summaries.
- Publisher: Bundesgerichtshof; reported by verbraucherrecht.at, rechtsportal.de, 123recht.de,
  VorsorgeBote
- URLs:
  https://verbraucherrecht.at/aktuelles-urteil-des-bgh-unwirksamkeit-von-klauseln-ueber-den-rueckkaufswert-von-lebens-und/2667 ·
  https://www.rechtsportal.de/Rechtsprechung/Rechtsprechung/2007/BGH/Wirksamkeit-der-Klauseln-ueber-den-Stornoabzug-und-die-Hoehe-des-Rueckkaufswerts-in-der-Kapitallebensversicherung
- The case law that produced the rule now in § 169 VVG. Clauses that **failed to distinguish
  sufficiently clearly between the *Rückkaufswert* and the *Stornoabzug*** — the latter having to
  be **agreed and appropriate** — were **held void**. The deduction must be **eindeutig erkennbar,
  i.e. capable of being quantified**; one **left to the insurer's discretion, or named only after
  the *Kündigung***, fails the transparency requirement. The 2007 decision is titled as being
  specifically about the ***Kapitallebensversicherung***. This is the historical reason delib treats
  the *Stornoabzug* as a **contractual, pre-declared schedule**.

### R25 — Assekurata, 24. Marktstudie "Überschussbeteiligungen und Garantien 2026"
- **Retrieved (2026-08-30): yes**, the March 2026 press release for the 24th edition as HTML. **The
  critical caveat is confirmed by the text rather than merely suspected**: the figures are stated to
  be "in der klassischen privaten Rentenversicherung", so they are annuity averages, and that an
  endowment book shares the rate remains `[unverified]`. Verbatim: "In der klassischen privaten
  Rentenversicherung erhöht sich die laufende Verzinsung für 2026 im Branchendurchschnitt auf
  **2,62 %** (Vorjahr: 2,53 %). Inklusive Schlussüberschüssen liegt die in Aussicht gestellte
  Gesamtverzinsung bei durchschnittlich **3,23 %** (Vorjahr: 3,19 %)", with *Neue Klassik* at 2,65 %
  laufend and 3,32 % total. Two additions: the caution is attributed to "weiterhin vorhandene stille
  Lasten in den Kapitalanlagen sowie vorsichtige Prognosen zur Zinsentwicklung", and "nur noch **elf**
  der untersuchten Gesellschaften [bieten] überhaupt klassische private Rentenversicherungen im
  Neugeschäft an".
- Publisher: Assekurata Assekuranz Rating-Agentur GmbH; reported by finanzwelt
- URLs: https://www.assekurata-rating.de/2026/03/04/assekurata-marktstudie-zu-ueberschussbeteiligungen-und-garantien-2026/ ·
  https://www.assekurata-rating.de/2026/01/29/ueberschussdeklaration/ ·
  https://www.finanzwelt.de/post/assekurata-marktstudie-zu-ueberschussbeteiligungen-und-garantien-2026
- **Klassische private Rentenversicherung: *laufende Verzinsung* for 2026 rises to a market average
  of 2,62 %** (2025: **2,53 %**). **Neue Klassik: *laufende Verzinsung* averaging 2,65 %**
  currently. Business is shifting toward **capital-market-linked products with fewer guarantees**
  even as surplus participation edges up. The caution in the increases is attributed to remaining
  ***stille Lasten*** in the investment portfolios and to conservative interest forecasts.
- **Critical caveat.** Both figures are for the **annuity**, not the endowment. **No market-average
  declared rate specific to the kapitalbildende Lebensversicherung was established.** The identity of
  the two rates is plausible — the same *Sicherungsvermögen* backs both — but `[unverified]` (gap 2).

### R26 — Trade-press reporting on the 2026 declarations and the market position of *Klassik*
- **Retrieved (2026-08-30): partly.** Both procontra articles were read in full as HTML; **the
  VersicherungsJournal piece is paywalled** — its body is reserved to premium subscribers, so only
  the headline "Etwa jeder dritte Lebensversicherer erhöht die Überschussbeteiligung" and the
  standfirst of 27 January 2026, which records a survey of "fast 50 Anbieter mit rund 87 Prozent
  Marktanteil", were read. **This entry now carries the declared rate the composite runs on**, since
  S11 turned out not to: procontra reports Allianz holding the *laufende Verzinsung* "für die
  klassischen Lebens- **und** Rentenversicherungen konstant bei **2,7 Prozent**", with *Perspektive*
  at 2,8 % — a **2025** declaration for a combined book. The same piece gives Alte Leipziger at
  2,25 % laufend / 2,45 % total and LVM at 2,4 % / 3,1 %. The "Klassik wird zur Nische" article
  carries Assekurata's 2,62 % average for 2026. **The description of the 2024 *Stornoquote* as an
  eight-year high is not in either retrieved article and is not established.**
- Publisher: VersicherungsJournal, procontra, Versicherungsbote, Biallo, Versicherungsmonitor
- URLs:
  https://www.versicherungsjournal.de/markt-und-politik/etwa-jeder-dritte-lebensversicherer-erhoeht-die-ueberschussbeteiligung-154961.php ·
  https://www.versicherungsjournal.de/unternehmen-und-personen/erster-lebensversicherer-gibt-ueberschussbeteiligung-fuer-2026-bekannt-154485.php ·
  https://www.versicherungsjournal.de/markt-und-politik/stornoquote-in-der-lebensversicherung-steigt-auf-acht-jahres-hoch-153466 ·
  https://www.procontra-online.de/lebensversicherung/artikel/lebensversicherung-2026-klassik-wird-zur-nische ·
  https://www.procontra-online.de/lebensversicherung/artikel/allianz-verzichtet-auf-erhohung-der-uberschussbeteiligung ·
  https://www.versicherungsbote.de/id/4948971/Lebensversicherung-2026-Verzinsung-Garantien-und-Markttrends/ ·
  https://www.biallo.de/altersvorsorge/news/wie-lebensversicherer-2026-die-verzinsung-erhoehen/
- **About one in three life insurers raised the *Überschussbeteiligung* for 2026**; **Allianz
  declined to raise its own**; the 2024 *Stornoquote* is described as an **eight-year high**; and
  the trade characterisation of the segment is **"Klassik wird zur Nische"**. With [S11] this is
  the evidence base for delib's statement that the product is an **in-force-dominated book with
  thin new business**.

### R27 — DAV, *Ergebnisbericht des Ausschusses Lebensversicherung* — Standardverfahren PRIIP Kategorie 4 (1 July 2025); Franke und Bornberg on *Basisinformationsblätter*
- **Retrieved (2026-08-30): yes.** PDF, 30 pp., Köln, 1 July 2025; the Franke und Bornberg blog post
  as HTML. The report's preamble states its own standing — "Dieser Bericht stellt im Sinne des
  Anhangs II der RTS zu PRIIP einen 'robusten, anerkannten Branchen- oder Regulierungsstandard' dar"
  — and its scope, "ein geeignetes Standardverfahren für PRIIP der Kategorie 4 zur Ermittlung des
  Marktrisikomaßes (MRM) und der Performance-Szenarien". **One caveat retrieval adds**: it names
  *Rentenversicherungen der 3. Schicht* as the products principally in view, so its application to an
  endowment is by analogy. No figure is taken from the Franke und Bornberg piece.
- Publisher: Deutsche Aktuarvereinigung e. V.; Franke und Bornberg GmbH
- URLs:
  https://aktuar.de/content/PDF/Fachwissen/2025-07-01_DAV_Ergebnisbericht_LV_Standardverfahren_PRIIP_Kategorie_4.pdf ·
  https://www.franke-bornberg.de/blog/basisinformationsblaetter-bib-zu-anlageprodukten-welche-informationen-liefern-bibs ·
  https://www.franke-bornberg.de/blog/was-bringen-priip-verordnung-und-basisinformationsblaetter
- The DAV report is identified by title and date — a **standard method for PRIIP *Kategorie 4***,
  the category for insurance-based products whose values depend partly on factors not observed in
  the market, i.e. profit-participating life business. Its existence establishes that **the
  performance scenarios in a German endowment BIB come from a profession-agreed standard method
  rather than from each insurer's own model**. **No content of the report was established.** The
  Franke und Bornberg pieces are a rating house's critical assessment; **no figure is taken from
  them**.

### R28 — Actuarial and lexicon reference works on *Deckungskapital*, *Zillmerung* and *Überschussverwendung*
- **Retrieved (2026-08-30): yes** — the DGVFM Band 4 teaching PDF and the three lexicon pages. **No
  formula is copied from them into delib**: the prospective reserve is standard actuarial content,
  used as a `[std]` construction and cited to no source, exactly as recorded below.
- Publisher: various — DGVFM/DAV teaching series; Universität zu Köln; Universität Heidelberg;
  Deutsche Nationalbibliothek; Gabler Versicherungslexikon; VersWiki; Wikipedia
- URLs:
  https://werde-aktuar.de/content/DGVFM/PDF/Schulmaterialien/DGVFM_Band_4_Lebensversicherung.pdf ·
  http://www.mi.uni-koeln.de/wp-znikolic/wp-content/uploads/2021/02/20201204_Deckungskapital_Inan.pdf ·
  https://www.mathi.uni-heidelberg.de/~bartels/Kapitalleben.html · https://d-nb.info/1009670638/34 ·
  https://www.versicherungsmagazin.de/lexikon/gezillmerte-nettopraemie-1945423.html ·
  https://www.versicherungsmagazin.de/lexikon/ueberschussverwendung-1946877.html ·
  https://www.versicherungsmagazin.de/lexikon/ueberschussbeteiligung-1946873.html ·
  https://www.versicherungsmagazin.de/lexikon/produktinformationsblatt-1946219.html ·
  https://www.deutsche-versicherungsboerse.de/verswiki/index_dvb.php?title=Lebensversicherung%3A_Zillmerung ·
  https://www.deutsche-versicherungsboerse.de/verswiki/index_dvb.php?title=Ratenzahlungszuschlag ·
  https://de.wikipedia.org/wiki/%C3%9Cberschussbeteiligung ·
  https://de.wikipedia.org/wiki/Beteiligung_an_den_Bewertungsreserven ·
  https://de.wikipedia.org/wiki/Reduction_in_Yield ·
  https://de.wikipedia.org/wiki/Unterj%C3%A4hrige_Zahlungsweise
- Taken as a group because the search summaries fused them:
  - ***Deckungskapital* versus *Deckungsrückstellung*.** The *Deckungskapital* is the amount that
    **should** be held to provide the guaranteed benefits; the *Deckungsrückstellung* is the
    **balance-sheet quantity of the amount actually held**. delib projects the former.
  - **Prospective method.** The *prospektive Methode* is named as a method of computing the
    *Deckungsrückstellung*. **The formula itself was not returned**; the reserve as the excess of the
    present value of future benefits over that of future net premiums is standard actuarial content,
    used in delib as a `[std]` construction and cited to no source here.
  - ***Gezillmerte Nettoprämie*.** The annual premium **whose present value equals the present value
    of the insurance benefits plus the *zillmerfähige Abschlusskosten***, carrying a cost loading
    that permits **annuity-style amortisation of the acquisition costs incurred at conclusion**.
  - ***Zillmerung*.** A *Deckungskapital* formula used above all for the *Deckungsrückstellung* of
    traditional life and health business **in the commercial-law balance sheet**. The
    *Deckungskapital* is **reduced by the present value of the acquisition costs not yet recovered**,
    so **in the early years a negative *Deckungskapital* arises** — precisely why § 169 Abs. 3 VVG
    needs a *Mindestrückkaufswert*.
  - ***Überschussverwendung*** — the four application systems, at section 4 — and the
    ***Ratenzahlungszuschlag*** with its *echte* / *unechte* distinction, at section 10.

### R29 — LVRG legislative and market-impact material
- **Retrieved (2026-08-30): yes** for the Pfefferminzia and Versicherungsbote reports and the
  Bundestag *Stellungnahme* PDF. **The "almost 8 %" study is now attributed**: it is the **LV-Check of
  the magazine Procontra**, which "seit 2009 die Bilanzen der relevantesten deutschen
  Lebensversicherer im engeren Sinne untersucht", reported 20 July 2016, and the figure is **7,9 %**
  — against a *Beitragssumme des Neuzugangs* down only 5,7 % over the same period, so the fall is not
  a volume effect. **No *Stornohaftung* period was established** and none is asserted.
  **Two corrections, one consequential.** (a) Versicherungsbote states the 40 ‰ predecessor in the
  form the model needs — "In der Bilanz kann der Versicherer somit von ursprünglich **4,0 Prozent**
  nur noch 2,5 Prozent der Beitragssumme als Vertriebs- und Abschlusskosten geltend machen" — and then
  adds "**Eine Deckelung der Provisionen ist gesetzlich nicht vorgesehen.** Höhere Provisionen können
  daher von den Versicherern gezahlt werden, sind jedoch aus anderen Töpfen zu nehmen." The LVRG caps
  what may be zillmered and recognised, **not what may be paid**. (b) **The Die Stuttgarter figure is
  not in either retrieved article.** The only carrier named is **ERGO**, and only qualitatively: a
  stepwise redistribution in which "eine höhere Bestandsprovision dann eine geringere
  Abschlussprovision ausgleicht". There is therefore **no named-carrier commission figure anywhere in
  this corpus**, and `comm_init_rate` and `comm_renew_rate` are `[std]` with no observation behind
  them.
- Publisher: Deutscher Bundestag (GDV *Stellungnahme*); Pfefferminzia; Versicherungsbote;
  AssCompact; Versicherungsjournal
- URLs:
  https://www.bundestag.de/resource/blob/284406/e26d0309aa9989f59485ae83bf52bca9/08-GDV-data.pdf ·
  https://www.pfefferminzia.de/vertrieb/untersuchung-zeigt-abschlusskosten-sinken-nach-lvrg-um-fast-8-prozent-1469012604/ ·
  https://www.versicherungsbote.de/id/4804227/LVRG-Lebensversicherung-Provision-Modelle/ ·
  https://www.versicherungsbote.de/id/4799001/GDV-Nachbesserungen-Stornohaftung-Lebensversicherungsreformgesetz-LVRG-Abschlusskosten/ ·
  http://www.asscompact.de/nachrichten/ein-lv-reformpaket-mit-%C3%BCberraschungsmomenten-0
- The **Lebensversicherungsreformgesetz (LVRG)** is dated **1 August 2014** [R1] and its
  *Höchstzillmersatz* cut took effect **1 January 2015** [R7] [S15].
- **Market effect on charges**: an industry study is reported to have found ***Abschlusskosten* fell
  by almost 8 % after the LVRG**; author, sample and base year **not established**.
- **Distribution response**: **withdrawn by retrieval.** The Die Stuttgarter 25 ‰ figure is in
  neither retrieved article; the only carrier named is **ERGO**, and only qualitatively — a stepwise
  redistribution in which "eine höhere Bestandsprovision dann eine geringere Abschlussprovision
  ausgleicht". **There is no named-carrier commission figure in this corpus.** Versicherungsbote adds
  the point that matters most for the model: "**Eine Deckelung der Provisionen ist gesetzlich nicht
  vorgesehen.** Höhere Provisionen können daher von den Versicherern gezahlt werden, sind jedoch aus
  anderen Töpfen zu nehmen" — the 25 ‰ ceiling constrains what may be zillmered, not what may be paid.
  The GDV lobbied for amendments on ***Stornohaftung*** and on *Abschlusskosten*; **no *Stornohaftung*
  period was established.**

### R30 — Verbraucherzentrale material on the Debeka *Stornoabzug* collective action
- **Retrieved (2026-08-30): yes**, both pages as HTML, and the figures now match the wording read at
  S3. The vzbv FAQ states it exactly: "Neben dem üblichen Stornoabzug von 5 Prozent wurde eine
  zusätzliche Stornogebühr erhoben. Ihre Höhe richtete sich nach der jeweiligen Kapitalmarktsituation
  und konnte 5, 10 oder 15 Prozent des Deckungskapitals betragen." The cohort question is settled: the
  class action covers policyholders who took out a Debeka life or annuity contract **after 2007** and
  cancelled, "besonders betroffen" being those cancelling from **1 May 2022**. **What the consumer
  bodies omit and S3 supplies**: a fourth *Kapitalmarktsituation* carrying no deduction at all, and
  both components running linearly to nil over the last ten years before maturity — so the schedule's
  floor is 0 %, not 5 %.
- Publisher: Verbraucherzentrale Bundesverband and its Land bodies (Hamburg, Niedersachsen)
- URLs: https://www.verbraucherzentrale.de/verfahren/debeka/faq ·
  https://www.vzhh.de/themen/versicherungen/lebens-rentenversicherung/urteil-stornoabzug-der-debeka ·
  https://www.verbraucherzentrale-niedersachsen.de/themen/finanzen/geldanlage/streit-ueber-stornoabzug-der-debeka-geht-die-naechste-runde
- A **collective action against Debeka Lebensversicherungsverein a. G. over its *Stornoklauseln*** is
  running as at the access date, and it is the source of the quantified deduction structure at [S3]:
  a **standard 5 % *Stornoabzug*** plus a **capital-market-dependent additional fee of 5 %, 10 % or
  15 % of the *Deckungskapital***. The framing is adversarial and the figures are the consumer
  bodies', not Debeka's, but they are corroborated across three independent bodies and the legal
  press [R22], so they are **not** `[unverified]`. **Which tariff generation carries them remains
  unestablished.**

### R31 — Insurer statutory accounts (located, no content established)
- Publisher: Continentale group (EUROPA Lebensversicherung AG); Allianz group (Deutsche
  Lebensversicherungs-AG). Doc type: *Geschäftsberichte* for financial year 2024
- URLs:
  https://www.continentale.de/documents/39054/34685915/GB_EUROPA+Lebensversicherung+AG_2024.pdf/8ea995d9-94bd-2e32-f589-6ffca1071726 ·
  https://dlvag.allianz.de/content/dam/onemarketing/azde/dlv/pdf/geschaeftsberichte/DLVAG-Geschaeftsbericht-2024.pdf
- **No content established.** Both were returned by the *Stornoquote* search and are recorded solely
  as **known, locatable primary sources of per-undertaking *Stornoquoten*, *Verwaltungskosten-* and
  *Abschlusskostenquoten*, RfB movements and declared surplus rates** — the accounts are where the
  delib assumption set would be calibrated if a later session has the budget. **Nothing in this
  file is cited to R31.**

---

## Extracted facts, organised by mechanic

> **Corrections from retrieval, 2026-08-30 — read before using anything in this section.** The
> documents behind these extracts have since been opened (see the `Retrieved` line on each source
> block). Nine extracted facts did not survive, and the sections below are the *pre-retrieval*
> record, kept for provenance rather than for use:
>
> 1. **The surplus base and timing at [S3].** B LV 85 is a deferred annuity with fund components, not
>    an endowment. Its *Zinsüberschussanteile* are set **monthly**, on the start-of-month reserve,
>    **from the third policy year**, and its *Schlussüberschussanteile* are a percentage of the
>    accumulated interest surplus used to buy fund units, **not** of the *Deckungskapital*. The
>    reserve-as-surplus-base fact is carried instead by the two endowment wordings, [S7] and [S18].
> 2. **The Debeka triple as three endowment wordings of different vintages** [S3][S4][S5]. All three
>    are annuity wordings and all three carry the same edition date, 01.07.2026; they differ by
>    tariff, not by vintage. Debeka publishes **no** endowment AVB [S6].
> 3. **The *gezillmert* / non-*gezillmert* pair at [S9].** Both die Bayerische documents are the same
>    tariff two years apart and **both are zillmered** at 2,5 %. There is no published pair.
> 4. **Premium cessation on death as an endowment rule [S7].** The express clause belongs to the
>    *Termfixversicherung*; in the ordinary endowment the contract ends with the death payment.
> 5. **The four-component surplus vocabulary at [S17].** HUK24 names three *drivers*, not four
>    components, and does not use the four names.
> 6. **Allianz's 2,7 % as a 2026 endowment rate [S11].** Not on any Allianz page; it is [R26]'s report
>    of a **2025** declaration for a combined classic life-**and-annuity** book.
> 7. **The GDV *Stornoquote* figures [R20].** The retrieved annual gives **2,56 % for 2023** on a
>    **count** measure; the 2,72 %/2024 and 1,2 % figures are not in it.
> 8. **Die Stuttgarter's 25 ‰ *Abschlussprovision* [R29].** Not in either retrieved article; the only
>    carrier named is ERGO, qualitatively. **No carrier commission figure exists in this corpus.**
> 9. **DAV 2008 T derived over 2006–2008 [R14].** The observation period is **2001 to 2004**;
>    2006–2008 is when the working group did the work.
>
> Four claims previously `[unverified]` are now **established**: the § 52 Abs. 28 Satz 7 locus of the
> age-62 rule; the second limb of the *Mindesttodesfallschutz*, § 20 Abs. 1 Nr. 6 Satz 6 b EStG; the
> BGH citation IV ZR 184/24 of 18 March 2026; and the existence of the *Sockelbetrag*, corroborated
> by [S2], [S9] and [S18].

### 1. Product structure and legal form

- The *Kapitallebensversicherung* **combines a term-life cover that pays on death with a savings
  process whose proceeds are paid, with interest, at the end of the contract** — the supervisor's
  own one-sentence definition, reported by the search summary of BaFin's consumer page as
  "Die Kapitallebensversicherung kombiniert eine Risikolebensversicherung, die im Todesfall zahlt,
  mit einem Sparvorgang, der am Vertragsende samt Zinsen ausgezahlt wird" [R18-family]. The same
  page gives the two legs separately: "Stirbt die versicherte Person während der Laufzeit, erhält
  die oder der Bezugsberechtigte die Versicherungssumme" and "Erlebt die versicherte Person das
  Vertragsende, fließt das angesparte Kapital an sie oder eine benannte Person."
- Allianz gives the same structure from the manufacturer's side: the *klassisch* variant
  **combines a guaranteed interest rate, a savings component and death cover in one product**
  [S11].
- It is written as an **individual contract** on a single life: every carrier document located
  [S3][S4][S5][S7][S8] is an AVB attaching to an individual *Versicherungsschein*, with no
  subscribing association in the chain — a structural difference from the French corpus, where five
  of eight carriers used a *contrat de groupe à adhésion facultative*.
- The customer receives a **document pair**: *Bedingungen* (AVB plus any *Tarifbedingungen*) **and**
  *Verbraucherinformationen* [S18], with an **IPID** and a **Basisinformationsblatt (PRIIP-KID)**
  alongside [S6][S10][R19].
- **Participation is the default and all-or-nothing.** § 153 Abs. 1 VVG entitles the policyholder
  to share in the surplus and the *Bewertungsreserven* **unless excluded by express agreement**,
  and it **can only be excluded entirely** [R1]. There is no partially participating German
  endowment; every carrier document located is participating [S3][S7][S9][S11].
- **Market role.** New business is small and shrinking. Allianz says of its own product that it "is
  rarely newly concluded today, because modern annuity insurance typically offers better flexibility
  and earnings opportunities" [S11]; the trade headline for 2026 is **"Klassik wird zur Nische"**
  [R26]; Assekurata reports business shifting to capital-market-linked products with fewer
  guarantees [R25]. delib therefore models **a large in-force book with a thin new-business layer**.
  **No quantification of the shift was established** — gap 3.

### 2. The two benefits

- **Erlebensfallleistung.** The agreed *Versicherungssumme* falls due at the **Ablauftermin named
  in the *Versicherungsschein***, and the policyholder must **submit the *Versicherungsschein*** to
  claim [S7]. What is paid is the **guaranteed *Versicherungssumme* plus the accumulated
  *Überschussbeteiligung*** [S11][R1], the two reported side by side on the annual *Standmitteilung*
  [S2].
- **Todesfallleistung.** If the *versicherte Person* dies before the *Ablauf*, the
  *Bezugsberechtigter* receives the *Versicherungssumme* [R18-family], again increased by surplus.
  **On death no further premiums are due** [S7] — the premium stream terminates with the death
  benefit, the processing-order rule most easily got wrong in an endowment projection.
- **The two sums need not be equal.** Tax law forces a floor on the death sum but not equality: for
  contracts concluded from **1 April 2009** the *Todesfallleistung* must be **at least 50 % of all
  premiums payable over the whole term** [R12]. Equal sums satisfy that comfortably at any
  realistic charge level; a savings-dominant design does not. delib carries the death/survival
  ratio as an explicit parameter with the 50 %-of-*Beitragssumme* floor as a constraint.
- **The 10 % excess condition.** A second reported tax condition requires the death benefit to
  **exceed the *Deckungskapital* or the *Zeitwert* by at least 10 %** [R12]. If that is the rule it
  binds **at every duration** and is the German analogue of a corridor test. Recorded; base and
  time profile `[unverified]` (gap 11).
- **No acceleration benefit is part of the base product.** Nothing in the corpus describes a
  terminal-illness or disability acceleration as a standard feature — unlike the French PTIA. The
  German market attaches a **Berufsunfähigkeits-Zusatzversicherung** as a separate rider, and § 165
  VVG's practical note records that such riders are **regularly lost on paid-up** [R3].

### 3. Überschussbeteiligung — the four components

- The entitlement is statutory: § 153 Abs. 1 VVG [R1], restated on the supervisor's consumer page
  as "In § 153 Versicherungsvertragsgesetz ist geregelt, dass Versicherungsnehmer an den Gewinnen
  beteiligt werden müssen, die mit ihren eingezahlten Beiträgen erwirtschaftet werden"
  [R18-family].
- Carriers and commentators alike decompose the surplus into **four components**
  [S16][S15][S17][R28]:

| Component | Arises when | Minimum policyholder share |
|---|---|---|
| *Zinsüberschuss* | investment return exceeds the guaranteed *Rechnungszins* | 90 % of the *anzurechnende Kapitalerträge* after deducting the discounting charge on the *Deckungsrückstellung* [R6]; "at least 90 % of the *Zinsüberschuss*" [S16] |
| *Risikoüberschuss* | mortality experience is better than priced | 90 % of the *Risikoergebnis* [R6][S16] |
| *Kostenüberschuss* | the book is administered more cheaply than loaded | MindZV: 50 % of the *übriges Ergebnis*, of which the cost result is the main part [R6]; [S16] states it as "half of the *Kostenüberschuss*" |
| *Schlussüberschussanteil* | long-run results not fully allocated during the term | no statutory minimum established |

- The first three are the ***laufende Überschussbeteiligung***, declared and allocated annually; the
  fourth is the terminal bonus, which "arises from the long-run success of the undertaking, in
  particular from returns that were not fully allocated to the running surplus during the contract
  term", and is paid **at termination** [S16].
- **The allocation base is the contract's own reserve.** ***Zinsüberschussanteile* and
  *Schlussüberschussanteile* are each fixed as a percentage of the *Deckungskapital* calculated at
  the allocation date** [S3] — the single most useful mechanical fact in the corpus, because it
  fixes the base as the reserve, not the sum insured and not the premium.
- **The allocation timing is the balance date.** *Zinsüberschussanteile* are allocated **at each
  *Bilanzstichtag*, being 31 December**, and again at the end of the accumulation phase; allocated
  amounts are **booked into the *Deckungskapital*** [S9, an annuity wording of the same carrier].
- **Entitlement starts immediately** — the right **begins with the start of insurance cover**, with
  no qualifying period [S9].
- **The declared rate is discretionary and may be zero.** "The level of future *Überschussbeteiligung*
  cannot be guaranteed" and **"may also be zero euros"** [S9]; it is set **annually** and depends on
  capital-market development and the insurer's own results [S3]. This is the sourced basis for
  classifying the surplus rate as an **insurer-discretionary current assumption**, not a contractual
  one, in delib's three-way assumption split.
- **Allocation must be causation-oriented** — § 153 Abs. 2 VVG requires a *verursachungsorientiertes
  Verfahren*, with other comparable appropriate principles available by agreement [R1]. A model
  allocating surplus in proportion to reserve is implementing exactly that and can say so.

### 4. Überschussverwendung — how the allocated surplus is applied

Four systems are named [R28][S15]. The system is **fixed at conclusion**, and the precise rules
**are in the *Versicherungsbedingungen*, which must be attached to every contract** [R28].

1. ***Verzinsliche Ansammlung*** — the allocated *Überschussanteile* are **accumulated with the
   insurer, bear interest, and are paid at termination together with the guaranteed
   *Versicherungssumme***; they **compound** and so automatically raise the maturity benefit [R28].
   This produces a separate, visible *Überschussguthaben* alongside the guaranteed sum.
2. ***Bonussystem* (*Summenzuwachs*)** — the surplus buys **additional paid-up insurance**, so the
   sum insured itself grows. The corpus does not spell out the purchase mechanics but states the
   consequence precisely: **"compared with the *Bonussystem*, the *verzinsliche Ansammlung* leads
   to a higher payment at maturity, while the *Bonussystem* produces higher death benefits"**
   [R28]. That asymmetry is the discriminating test between the two in a projection and belongs in
   delib's pitfalls list.
3. ***Beitragsverrechnung*** — the allocation is **set off against the premium**: the policyholder
   **pays only part of the premium due, the remainder being met out of the surplus** [R28]. In a
   projection this reduces the premium cash flow rather than raising the benefit, changing the sign
   of the surplus in the cash-flow statement.
4. ***Anlage in Fondsanteilen*** — investment of the surplus in fund units. **Not established by
   any search result in this session**; `[unverified]` and gap 4.

**Market default.** "In *Renten-* und *Lebensversicherung*, as a rule **either the *verzinsliche
Ansammlung* or the *Bonussystem*** is applied" [R28] — the corpus **does not** say which is more
common. Debeka's mechanics (surplus declared as a percentage of, and booked into, the
*Deckungskapital* [S3][S9]) are the reserve-crediting form, closest to *verzinsliche Ansammlung*.
**Any statement that one system is "the market default" is `[unverified]`** (gap 4). delib models it
as the `[std]` base case and carries *Beitragsverrechnung* and the *Bonussystem* as variants.

### 5. Beteiligung an den Bewertungsreserven

- **The half share.** § 153 Abs. 3 VVG: determine the *Bewertungsreserven* **anew each year**,
  allocate by a causation-oriented procedure, and **on termination allocate and pay out half of the
  amount then determined**; **earlier allocation may be agreed** [R1]. § 139 VAG restates it [R8].
- **The *Sicherungsbedarf* cut-back.** Participation by **exiting** policyholders is permitted
  **only to the extent that the *Bewertungsreserven* exceed the *Sicherungsbedarf* from contracts
  with an interest guarantee**, that need being the sum over contracts with an **überhöhter
  Rechnungszins** of the **actuarially valued interest obligation less the *Deckungsrückstellung***
  [R8]. **Read in the instrument for the 2026-08-30 pass, § 139 Abs. 3 VAG confines the cut-back to
  "Bewertungsreserven aus ... festverzinslichen Anlagen und Zinsabsicherungsgeschäften"** — not to the
  whole of the *Bewertungsreserven* — and [S18] § 2 Abs. 5 restates exactly that in a carrier's
  wording.
- **The legal hinge** is § 153 Abs. 3 Satz 3 VVG in its **LVRG (1 August 2014)** form, a *Vorbehalt
  aufsichtsrechtlicher Regelungen* [R1], challenged as unconstitutional before the BGH [R1]; the
  leading post-LVRG decision is **BGH 20 January 2021, IV ZR 318/19** [R23].
- **Purpose**: to counter the fear, fuelled by the prolonged low-interest period, that insurers could
  no longer meet the benefits they had guaranteed [R8].
- **Modelling consequence.** In the sustained low-rate environment the *Sicherungsbedarf* has
  routinely exhausted the *Bewertungsreserven*, so the exit half share has frequently been nil. The
  corpus supports the mechanism but supplies **no figure for the amount distributed in any year**
  [R8][R23]. The delib base run sets the participation to zero as a `[std]` choice, exposes it as a
  parameter, and says exactly this. A ***Sockelbetrag*** is mentioned by one weak secondary source;
  existence, base and size `[unverified]` (gap 8).

### 6. Gesamtverzinsung and the declared rates

- The **Gesamtverzinsung** is the ***laufende Verzinsung*** plus the ***Schlussüberschuss***
  expressed as a rate. The two-part structure is stated: distribution "can take place in two ways:
  annually (*laufende Überschussbeteiligung*) or at the end of the contract (*Schlussüberschuss*)"
  [S16].
- **Declared rates established, each with its year:**

| Basis | Rate | Year | Tag |
|---|---|---|---|
| Allianz, classic book, *laufende Verzinsung* | 2.7 % | 2026 | [S11] |
| Market average, klassische private Rentenversicherung, *laufende Verzinsung* | 2.62 % | 2026 | [R25] |
| Market average, klassische private Rentenversicherung, *laufende Verzinsung* | 2.53 % | 2025 | [R25] |
| Market average, "Neue Klassik", *laufende Verzinsung* | 2.65 % | 2026 | [R25] |
| *Höchstrechnungszins* (guaranteed component) | 1.00 % | from 2025-01-01 | [R7] |
| *Höchstrechnungszins* | 0.25 % | 2022–2024 | [R7] |
| *Höchstrechnungszins* | 4.00 % | 1994 | [R7] |

- **The two market averages are for the annuity, not the endowment** [R25]. The endowment and the
  deferred annuity are normally backed by the same *Sicherungsvermögen* and normally carry the same
  declared rate, but **the corpus does not say so** and the identity is `[unverified]` (gap 2). The
  Allianz 2,7 % is explicitly for **classic customers** and is the only rate in the corpus attached
  to a classic savings book by its manufacturer.
- **Direction of travel, 2026**: about **one in three insurers raised** the *Überschussbeteiligung*
  [R26]. The caution is attributed to "weiterhin vorhandene ***stille Lasten*** in den Kapitalanlagen
  sowie vorsichtige Prognosen zur Zinsentwicklung" [R25], and only **eleven** of the companies
  Assekurata surveys still write classic private annuities as new business [R25]. **The 2,7 % figure
  is Allianz's 2025 declaration for its combined classic life-and-annuity book, reported by procontra
  [R26] — it is not on any Allianz page and it is not a 2026 rate.**
- **No *Schlussüberschuss* rate of any kind was established**, so **no *Gesamtverzinsung* figure is
  available** (gap 1). Any *Gesamtverzinsung* printed in delib is the *laufende Verzinsung* above plus
  a `[std]` terminal component with its rationale stated.

### 7. Where the surplus comes from — MindZV

- The **Rohüberschuss** reaches the ***Rückstellung für Beitragsrückerstattung* (RfB)** before it
  reaches contracts. MindZV minima [R6]: **90 %** of the *anzurechnende Kapitalerträge* under
  § 3 Abs. 1, computed on investment income attributable pro rata to the policyholder side **less
  the *Aufwand für die Diskontierung der Deckungsrückstellung***; **plus 90 %** of the
  *Risikoergebnis*; **plus 50 %** of the *übriges Ergebnis*. Computed and complied with **separately
  for *Altbestand* and *Neubestand***; a contract written today is *Neubestand*.
- Consumer-facing statements give "at least 90 % of the *Zins-* and *Risikoüberschuss*" and "half of
  the *Kostenüberschuss*" [S16]. **The framings differ** — the MindZV's third bucket is the wider
  *übriges Ergebnis*; both recorded, the MindZV framing being the one to cite (gap 6).
- **Modelling consequence.** These are minimum allocations **to a provision**, not to a contract.
  Between the RfB and the policy sits the insurer's declaration policy, described throughout as
  annual and discretionary [S3][S9]. A delib model projecting a declared rate projects the **output**
  of that policy and must not present the 90/90/50 quotas as if they determined it.

### 8. Rechnungsgrundlagen — interest and mortality

- **Rechnungszins.** The contract is priced and reserved at a *Rechnungszins* not exceeding the
  ***Höchstrechnungszins*** [R7]: **1,00 % for new business from 1 January 2025**, with the DAV
  recommending **1,0 % for 2026** as well [R15]. The rate is set by regulation on the profession's
  recommendation — DAV November 2023, BMF adoption late April 2024 [R7][R15], industry support
  [R16].
- **History the model's cohorts must reflect**: 4,00 % in 1994, falling continuously to 0,25 % by
  2022, then 1,00 % from 2025 — the first increase since 1994 [R7]. A German endowment book spans
  guaranteed rates from **4 %** down to **0,25 %** and back to **1 %**, and the *Sicherungsbedarf*
  mechanism exists precisely because of the top of that range [R8].
- **Mortality.** The reference family for death-benefit business is **DAV 2008 T**, derived from
  studies carried out 2006–2008 on **observation years 2001 to 2004** of insurers' own policy data
  and on German population statistics [R14], the cleansed
  insured data covering **60 % of the German market in the *Kapitallebensversicherung* segment**
  [R14]. Variants **DAV 2008 T R / NR** support smoker differentiation but are **not suitable for
  business written without a *Gesundheitsprüfung*** [R14]. The *Richtlinie* also fixes the method
  for the ***Sicherheitszuschläge*** [R14].
- **The DAV tables are not public and delib does not redistribute them** [R14]. Any decrement table
  shipped is a `[std]` proxy that must preserve the qualitative shape — a death-benefit basis with an
  explicit safety loading — and must be anchored so the worked example reproduces exactly. **Whether
  a distinct first-order table exists for endowment as against pure term business was not
  established** (gap 14).

### 9. Premium

- The *Beitrag* decomposes into a ***Sparanteil***, a ***Risikoanteil*** and a ***Kostenanteil***,
  the *Risikoanteil* depending on age, health status, smoking and dangerous hobbies [S11][S12][S13]
  [S15] group — the three-way split delib's technical notes publish per period.
- The premium is **level** over the *Beitragszahlungsdauer*, which may be shorter than the
  *Versicherungsdauer*; **no source states the range of abbreviated-payment options offered**, so any
  such option in delib is `[std]`. **The premium stops on death** because the death payment ends the
  contract — "Mit der Auszahlung endet der Vertrag" [S7] § 3 I (5); the express clause "Bei Tod der
  versicherten Person vor dem Ablauftermin werden keine Beiträge mehr fällig" belongs to the
  *Termfixversicherung* [S7] § 3 II, the one variant death does **not** terminate. And **on
  *Beitragsfreistellung*** [R3].
- ***Beitragssumme*** — the total of all premiums payable over the agreed term — is the **reference
  base** for the acquisition-cost cap [R7][S15] and for the tax *Mindesttodesfallschutz* test [R12],
  and is one of GDV's two headline new-business measures alongside the APE [R21]. A delib model
  must carry it as a derived quantity, not merely the annual premium.
- **Payment frequency**: annual, half-yearly, quarterly, monthly, with a *Ratenzahlungszuschlag* on
  the sub-annual forms (section 10).
- **No premium rate table, gross premium scale or tariff grid for any German endowment was located**
  — the sharpest contrast with the frlib corpus, which contained one published attained-age rate
  card. Every premium level in delib is `[std]` or computed by the model's own equivalence
  principle. Gap 16.

### 10. Charges

**Abschluss- und Vertriebskosten and the Zillmerung.**

- Insurers "usually compensate their distribution partners with an *Abschlussprovision* as a share
  of the contractually agreed ***Beitragssumme*** at conclusion of the contract, **regardless of
  whether the customer has already paid that premium sum**" [R28 family]. That mismatch — cost
  incurred at once, premium received over decades — is what *Zillmerung* finances.
- ***Zillmerung*** reduces the *Deckungskapital* **by the present value of the acquisition costs not
  yet recovered**, so **a negative *Deckungskapital* arises in the early years** [R28]. The
  ***gezillmerte Nettoprämie*** is the annual premium whose present value equals that of the benefits
  **plus** the *zillmerfähige Abschlusskosten*, carrying a loading that permits annuity-style
  amortisation of those costs [R28].
- **The statutory cap.** The *Zillmersatz* **may not exceed 25 ‰ (2,5 %) of the *Beitragssumme***,
  cut from **40 ‰** by the LVRG with effect from **1 January 2015** [R7][S15][R29]; in the balance
  sheet only 2,5 % may be recognised as *Abschluss- und Vertriebskosten* [S15].
- **Market effect.** *Abschlusskosten* are reported to have **fallen by almost 8 % after the LVRG**
  [R29]; **Die Stuttgarter** cut its *Abschlussprovision* to **25 ‰**, compensating brokers with
  *Bestandsprovision* [R29]. ***Zillmerung* is a per-tariff choice**: die Bayerische publishes a
  *gezillmert* (B 520127) and a non-*gezillmert* (B 520136) edition of the **same** tariff [S9], so
  delib must be able to run with *Zillmerung* off.

**Verwaltungskosten.**

- "It is customary in life insurance that ongoing costs are charged **annually as a percentage of
  the ongoing premium and/or as a percentage of the *Vertragsguthaben***" [R28 family].
- **This does not match the form the brief anticipated.** A per-mille-of-*Versicherungssumme* charge
  and a fixed per-policy *Stückkosten* charge were **not established by any search result**. The
  two established bases are **percentage of premium** and **percentage of the contract's fund**.
  Any other form used in delib is `[std]` and must be labelled as one. Gap 17.
- The ***Produktinformationsblatt*** must show **Einstiegskosten** (*Abschluss- und
  Vertriebskosten*), **laufende Kosten** (*Verwaltungskosten*) and **sonstige Kosten** [R28 family].

**Ratenzahlungszuschlag.**

- Typical loadings: **2 % half-yearly, 3 % quarterly, 5 % monthly** [R28]. These are the customary
  market levels, not any one insurer's tariff; **no carrier document in this corpus publishes its
  own scale**, so the three are used as a cited market range and any single value chosen is `[std]`.
- Justification: the greater administrative effort — premiums collected and processed **12 times
  rather than once** a year, with correspondingly higher dunning effort [R28].
- **The *echte* / *unechte* distinction matters.** Contracts providing for sub-annual premiums **from
  the outset** — a *Versicherungsperiode* of one month, say — carry **no** *Ratenzahlungszuschlag*;
  these are ***echte unterjährige Beiträge***, and the loading attaches only to ***unechte*** ones,
  where an annual contract is paid in instalments [R28]. A model applying a frequency loading to a
  genuinely monthly contract is wrong.
- A consumer-law challenge on the ground that the loading is undisclosed credit requiring an
  effective-interest statement is reported by one weak source; **outcome not established**.

**Effektivkosten.**

- The ***Effektivkostenquote* (Reduction in Yield, RIY)** discloses **all costs — acquisition,
  ongoing and investment — as the reduction they cause in the contract's annual yield** [R9]. Legal
  basis **§ 7 Abs. 2 und 3 VVG i. V. m. §§ 2 und 3 VVG-InfoV**; introduced by the **LVRG (2014)**
  and mandatory in quotations **from 1 January 2015** [R9].
- Under PRIIPs the ***Effektivkosten* of a specimen contract must appear in the
  *Basisinformationsblatt***, with **total costs and RIY per year at three time points — after one
  year, after half the term, and at maturity — split into one-off and ongoing costs** [R19].
- **Supervisory pressure.** BaFin says *Effektivkosten* **differ considerably** between providers and
  products and will **closely examine** high outliers on cost or on intermediary payments [R17]; cost
  is a named **2026** focus risk [R18]. **No numerical *Effektivkosten* value, range or threshold was
  established** — not from BaFin, not from any BIB, not from any carrier (gap 7). **Every charge
  level in delib is `[std]`.**

### 11. Deckungskapital and Deckungsrückstellung

- ***Deckungskapital*** is the amount that **should** be held to provide the guaranteed benefits;
  ***Deckungsrückstellung*** is the **balance-sheet quantity of the amount actually held** [R28].
  delib projects the former and references the latter without specifying it, per the library's
  scope rule.
- It is computed **prospectively** [R28], at the **Rechnungszins**, on the ***Rechnungsgrundlagen der
  Prämienkalkulation*** — the first-order basis, not a current or market basis [R2]. It is normally
  ***gezillmert*** subject to the 25 ‰ cap [R7] and is therefore **negative in the early years**
  [R28].
- Allocated *Überschussanteile* are **booked into the *Deckungskapital*** [S9], and the declared
  *Zins-* and *Schlussüberschussanteile* are **percentages of the *Deckungskapital* at the
  allocation date** [S3]. The reserve is thus both the base of the surplus declaration and its
  destination — a self-reference the model must resolve in a stated processing order.
- **The prospective reserve formula itself was not returned by any search**; it is standard
  actuarial content, used in delib as a `[std]` construction and cited to no source here.

### 12. Rückkaufswert — § 169 VVG

- **Trigger.** The claim arises on termination, **in particular by *Kündigung*, *Rücktritt* or
  *Anfechtung*** [R2]; also where the insurer is *leistungsfrei* for *Selbsttötung* [R4] and where a
  *Beitragsfreistellung* request fails the *Mindestversicherungsleistung* test [R3].
- **Calculation.** The *Rückkaufswert* is the *Deckungskapital*, computed **by recognised actuarial
  rules**, on the ***Rechnungsgrundlagen der Prämienkalkulation***, **as at the end of the current
  *Versicherungsperiode*** [R2]. All three matter: pricing basis, period-end date, reserve quantity.
- **Mindestrückkaufswert.** On ***Kündigung*** the value is **at least** the *Deckungskapital*
  obtained when the *angesetzte Abschluss- und Vertriebskosten* are spread **evenly over the first
  five contract years** [R2] — the direct answer to the negative early *gezillmert* reserve [R28].
- **The five-year spreading and the 25 ‰ cap are different rules.** § 169 Abs. 3 VVG fixes **how**
  acquisition costs are spread for the surrender floor; § 4 DeckRV fixes **how much** may be
  zillmered at all. One search summary conflated them [R2]; delib keeps them apart. Gap 5.
- ***Zeitwert*.** For *fondsgebundene* and certain other classes the *Rückkaufswert* is a *Zeitwert*
  [R2] — that branch governs delib product 3, **not** this one; a classic endowment's surrender value
  is a *Deckungskapital*.
- **What the customer gets.** On *Kündigung* the policyholder receives the *Rückkaufswert*, which
  **can be below the premiums paid, especially in the early contract years**; the investment return
  earned and the *Überschussbeteiligung* are **included in** it [S11]. It is one of the four
  quantities reported annually on the *Standmitteilung* [S2].

### 13. Stornoabzug

- **Three cumulative conditions**: the deduction must be ***vereinbart*, *beziffert* and
  *angemessen*** [R2]. **A deduction for *noch nicht getilgte Abschluss- und Vertriebskosten* is
  void** [R2] — the insurer cannot recover through it what the *Mindestrückkaufswert* denies it.
- **What *beziffert* requires.** The BGH holds that it does **not** compel a concrete euro amount at
  conclusion; **an unambiguous calculation procedure suffices, provided it leaves the insurer no
  *Ermessensspielraum* and is free of unilateral determination rights** [R22]. A
  **capital-market-dependent** *Stornoabzug* is therefore lawful in principle.
- **The older line** required the deduction to be **eindeutig erkennbar — capable of being
  quantified** — and struck down clauses that failed to separate the *Rückkaufswert* from the
  *Stornoabzug*, left it to discretion, or named it only after the *Kündigung* [R24]. The 2007
  decision is specifically about the *Kapitallebensversicherung* [R24].
- **The only quantified schedule in the corpus**: Debeka applies a **standard 5 % deduction** plus a
  **capital-market-dependent additional fee of 5 %, 10 % or 15 % of the *Deckungskapital***
  [S3][R30] — an observed total range of **5 % to 20 % of the *Deckungskapital*** for one carrier.
  The clause is the subject of a **live collective action** [R30] and of a BGH remittal on
  *Angemessenheit* [R22], so its ultimate validity is **unresolved at the access date**.
- **No other carrier's *Stornoabzug* was established.** A single-carrier range is not a market
  range; any delib base value is `[std]` with the Debeka figures given as the one observation.
  Gap 18.

### 14. Beitragsfreistellung — § 165 VVG

- **The right.** Conversion into a ***prämienfreie Versicherung* at any time, with effect for the end
  of the current *Versicherungsperiode***, **provided the agreed *Mindestversicherungsleistung* is
  reached** [R3]. **The failure branch**: if it is **not** reached, the insurer must **pay the
  *Rückkaufswert* including *Überschussanteile* under § 169** [R3] — below the minimum the paid-up
  election **becomes a surrender**. A model offering *Beitragsfreistellung* without this test is
  wrong, and this is a delib pitfall.
- **The calculation.** The ***beitragsfreie Versicherungssumme*** is computed by recognised
  actuarial rules, on the *Rechnungsgrundlagen der Prämienkalkulation*, **on the basis of the
  *Rückkaufswert* under § 169 Abs. 3 bis 5** [R3] — so it **inherits the five-year spreading
  floor**: the paid-up sum cannot be depressed below what the floored reserve will buy.
- **It is tabulated in the contract, for each *Versicherungsjahr*** [R3] — known at issue, not
  recomputed at election. ***Prämienrückstände* are netted** at the same date [R3].
- **How it differs from *Kündigung*.** Both are struck at period end and run off the same
  *Rückkaufswert* base [R2][R3]. But *Beitragsfreistellung* **keeps the contract alive** with a
  reduced sum insured, keeps the policyholder participating in surplus, and pays nothing now;
  *Kündigung* **ends** the contract, pays now, and — uniquely — attracts the **Mindestrückkaufswert
  floor**, which § 169 Abs. 3 expresses for the *Kündigung* case [R2]. The paid-up route also
  **loses attached *Zusatzversicherungen*** [R3]. The reduction may be **in whole or in part**
  [S7] — partial paid-up is available.
- **Statistical note**: GDV's main *Stornoquote* measure **counts conversion to *beitragsfrei* as
  part of the lapse rate** [R20], so that headline figure is not a surrender rate.

### 15. Underwriting

- ***Gesundheitsprüfung*.** § 19 Abs. 1 Satz 1 VVG obliges the applicant to disclose the
  *gefahrerhebliche Umstände* known to her **that the insurer has asked about in *Textform*** [R5] —
  a question-bounded duty. The provision gives the insurer the right to put health questions and
  decide whether to accept **with restrictions** or **only at an increased premium** [R5].
- ***Risikozuschlag* and exclusion.** On a breach the insurer may **adjust the contract
  retrospectively** — **excluding the undisclosed risk** or **raising the premium by a
  *Risikozuschlag*** — instead of refusing to perform; for negligent breach this is the usual outcome
  [R5]. Rights **lapse five years** after conclusion for negligence, **ten years** for intentional or
  *arglistig* breach [R5]. **Rating factors**: **age, health status, smoking and dangerous hobbies**
  [S11][S12][S13][S15] group; smoker differentiation is supported at table level by DAV 2008 T R / NR.
- **Underwriting is a precondition of the table.** DAV 2008 T R and NR are "**not** suitable for
  policies **without a *Gesundheitsprüfung***" [R14] — a simplified- or guaranteed-issue endowment
  would need a different basis.
- ***Wartezeit*.** **Nothing in this corpus establishes a waiting period for a German underwritten
  endowment.** German waiting-period constructions belong to *Sterbegeldversicherung* and to
  simplified-issue covers. The only period the corpus does establish that operates like one is the
  **three-year *Selbsttötung* window** [R4]. Any *Wartezeit* in delib is `[std]`; gap 19.
- **No underwriting threshold, age/amount grid or *Risikozuschlag* scale was established for any
  German carrier** — the same blank frlib found for France, and for the same reason: the grids are
  not public. Gap 16.

### 16. Selbsttötung — § 161 VVG

- The insurer is ***leistungsfrei*** if the *versicherte Person* **intentionally takes her own life
  before three years have elapsed since conclusion** [R4]; **not** so where the act was done **in a
  state excluding free determination of the will, caused by a *krankhafte Störung der
  Geistestätigkeit*** [R4].
- **The three-year period may be extended by individual agreement** [R4] — a statutory minimum
  window, extendable and by implication not shortenable. **Whether any carrier extends it was not
  established**; no carrier wording's suicide clause was obtained.
- **The insurer must nevertheless pay the *Rückkaufswert* including *Überschussanteile* under § 169**
  [R4]. The German rule is a **benefit substitution**, not a forfeiture: in a projection a suicide
  inside the window is a **surrender-value payment, not a nil payment** — a delib pitfall.

### 17. Taxation

- **Contracts concluded from 1 January 2005** (the *Alterseinkünftegesetz* boundary): the
  ***Unterschiedsbetrag*** — benefit less premiums paid — is **taxable**, and **premiums are not
  deductible** [R13][R10]. **The half-income rule**: benefit paid **after completion of the 60th year
  and after twelve years from conclusion** → **only half the *Unterschiedsbetrag*** is taxable,
  § 20 Abs. 1 Nr. 6 Satz 2 EStG [R10].
- **The age-62 tightening**: for contracts concluded **after 31 December 2011** the required age is
  **completion of the 62nd year**, **§ 52 Abs. 28 Satz 7 EStG** as read in the statute for the 2026-08-30
  pass [R10] (recorded here before as § 52 Abs. 36 Satz 9 EStG; current locus
  `[unverified]`).
- **Rate**: where the halving applies and the benefit accrues **from 1 January 2009**, the flat
  *Abgeltungsteuer* does **not** apply; the **personal marginal rate** applies to the half amount,
  § 32d Abs. 2 Nr. 2 EStG [R10]. **Withholding**: under § 43 Abs. 1 Nr. 4 Halbsatz 2 EStG the
  halving is **disregarded for *Kapitalertragsteuer* purposes**, i.e. given effect at assessment
  [R10] — mechanism `[unverified]`.
- ***Mindesttodesfallschutz***: for contracts concluded **from 1 April 2009** the
  *Todesfallleistung* must be **at least 50 % of all premiums payable over the whole term** (the
  **"50 %-Regel"**), with a further condition that the death benefit **exceed the *Deckungskapital*
  or *Zeitwert* by at least 10 %** [R12]. **Failing the test means full taxation under the
  *Abgeltungsteuer* with no halving** [R12]. Administrative guidance: **BMF-Schreiben of 1 October
  2009, IV C 1 - S 2252/07/0001** [R11].
- **The pre-2005 regime.** The boundary is established, and that pre-2004 contracts sold on were not
  taxed on the proceeds [R13]; but **the conditions of the old regime — twelve-year term, five-year
  minimum premium-paying period, minimum death cover as a percentage of the *Beitragssumme* — were
  not established and are `[unverified]`** (gap 13). Bund der Steuerzahler characterises the rules as
  *sehr differenziert* [R13].
- **Three tax cohorts** therefore exist in a German endowment book: **pre-2005**, **2005–2011** and
  **2012 onwards**, with the 1 April 2009 *Mindesttodesfallschutz* line cutting across the second.
  delib's composite is a **post-2011 contract**, so the operative conditions are twelve years,
  **age 62** and the *Mindesttodesfallschutz*.
- **The tax rules do not enter the projected liability cash flows** — delib publishes gross benefits —
  but they **do** fix the product's design constraints (the 50 % death-sum floor) and its typical term
  (at least twelve years), and are used that way.

### 18. Termination other than death, maturity, surrender and paid-up

- ***Kündigung*** by the policyholder is the principal voluntary exit, priced through § 169 VVG [R2].
  The corpus does **not** establish the notice mechanics, the permitted dates, or whether notice may
  be given at any time — only that the value is struck **at the end of the current
  *Versicherungsperiode*** [R2]. **§ 168 VVG, which governs the *Kündigung* right itself, was not
  researched** and nothing is asserted about it (gap 20). ***Rücktritt* and *Anfechtung*** are named
  in § 169 as triggers of the claim [R2]; § 19 VVG supplies the *Rücktritt* ground for a disclosure
  breach with its five- and ten-year limits [R5].
- ***Widerruf*** (§ 152 VVG, 30 days) **was not researched** and is not asserted. **Non-payment**:
  § 165's netting of *Prämienrückstände* [R3] implies a standing-arrears regime, but the §§ 37/38
  VVG *Mahnverfahren* **was not researched** and is not asserted. Gap 20.

### 19. Typical parameter levels

Everything here comes from a **fused consumer-page summary that did not attribute sentences to
individual URLs**; the candidate pages are [S11] [S12] [S13] [S15] and the BaFin consumer page.
Attribution is to the group, and this is the weakest section in the file.

| Parameter | Established value(s) | Year | Tag |
|---|---|---|---|
| Minimum term to obtain the tax treatment | 12 years | current | [R10] |
| Typical term as sold | 20 to 40 years | current | [S11][S12][S13][S15] group |
| Maximum *Versicherungsdauer* | 25 to 35 years | current | [S11][S12][S13][S15] group |
| Minimum term (conflicting statement) | 3 to 5 years | current | [S11][S12][S13][S15] group |
| Minimum *Versicherungssumme* | 2,500 or 5,000 EUR | current | [S11][S12][S13][S15] group |
| *Eintrittsalter* | **not established** | — | — |
| Typical *Beitrag* level | **not established** | — | — |
| Maximum *Versicherungssumme* | **not established** | — | — |

- **The two "minimum term" statements contradict each other** — 12 years against 3 to 5 — and the
  second, with the 2 500 / 5 000 EUR minimum sum, most likely belongs to a *Sterbegeldversicherung*
  or a short savings contract the same search matched; both are recorded, and **neither is used as a
  delib parameter without a `[std]` tag** (gap 21). The 20-to-40-year band and the 25-to-35-year
  maximum also overlap awkwardly; the honest reading is that the corpus supports a **long-term
  contract of the order of two to three decades**, and nothing finer.
- **No entry age, no premium level, no maximum sum insured and no rate table were established.** The
  delib model point is a `[std]` construction from the term band plus the tax minimum, and its
  rationale is stated in the product specification.

### 20. Lapse experience and market context

| Measure | Value | Year | Tag |
|---|---|---|---|
| *Stornoquote*, whole life market, main GDV measure | 2.72 % | 2024 | [R20] |
| Same measure | 2.56 % | 2023 | [R20] |
| *Stornoquote* by number of contracts (surrenders and other early terminations) | 1.2 % | 2024 | [R20] |
| Insurers raising the *Überschussbeteiligung* | about one in three | 2026 | [R26] |

- **Superseded by retrieval**: the GDV publishes one figure, "Die Stornoquote (Anzahl) ... 2,56 %"
  for 2023 [R20], a **count** measure over all life business. The two-measure account below rests on
  the pre-retrieval summaries and is kept only for provenance. The 2,72 % measure was said to **count
  contracts terminated early, surrendered, or converted to
  *beitragsfrei*, as a percentage of the *Bestand*** [R20]; the 1,2 % measure counts contracts and
  covers surrenders and other early terminations [R20]. **The two are not reconcilable from the
  search evidence** and both are recorded (gap 10). The 2024 figure is described as an **eight-year
  high** [R26].
- **No endowment-specific lapse rate, and no lapse rate by duration, was established.** A German
  endowment's lapse profile is strongly duration-dependent — the *Zillmerung* penalty falls hardest
  in the first five years — but the corpus says nothing about the shape. Every lapse assumption in
  delib is `[std]`. **The declared-rate direction for 2026 is mildly upward** [R25][R26], from a base
  far below the guarantees written in the 1990s [R7].

### 21. What a projection model needs, and what the corpus supplies

| Model input | Status | Tag |
|---|---|---|
| Guaranteed *Rechnungszins* | established, 1.00 % for new business from 2025 | [R7][R15] |
| Declared *laufende Verzinsung* | 2.62 % annuity market average for 2026 [R25]; 2.25 %–2.80 % at named carriers for **2025** [R26]. **No endowment-specific rate exists** | [R25][R26] |
| *Schlussüberschuss* rate | **not established**; mechanism established [S7][S18] | gap 1 |
| Surplus allocation base | established: percentage of the *Deckungskapital*, in four wordings | [S7][S18][S9][S3] |
| Surplus allocation timing | **varies**: 31 December *Bilanztermin* [S9]; policy *Stammtag* [S7]; start of policy year [S18]; monthly [S3] | [S7][S9][S18][S3] |
| Surplus application system | four named; **market default not established** | [R28], gap 4 |
| *Bewertungsreserven* share | mechanism established; **amount not established** | [R1][R8], gap 8 |
| Mortality basis | family and provenance established; **table values not public** | [R14] |
| Acquisition-cost cap | established, 25 ‰ of *Beitragssumme* | [R7][S15] |
| Actual acquisition-cost level | **not established** | gap 7 |
| Administration-cost form | established as % of premium and/or % of fund | [R28] |
| Administration-cost level | **not established** | gap 7 |
| *Ratenzahlungszuschlag* | established as a market range 2/3/5 % | [R28] |
| Surrender-value rule | established in full | [R2] |
| *Stornoabzug* level | **three carriers, three bases**: 0–20 % of the *Deckungskapital* [S3][R30]; 50 € + 0,15 % of premiums × years remaining [S9]; 100 € + 0,2 % of (sum insured − reserve) [S18] | gap 18 |
| Paid-up rule | established in full | [R3] |
| Suicide rule | established in full | [R4] |
| Lapse rate | market aggregate only, two irreconcilable measures | [R20], gap 10 |
| Premium rates | **none public** | gap 16 |

---

## Observed variation across insurers

The corpus is thin enough that an honest variations table is mostly a record of what could not be
compared: six carriers produced a document, and only one produced quantified terms.

| Feature | Debeka [S3][S4][S5][S6] | Allianz [S11] | Gothaer [S7] | die Bayerische [S8][S9] | ERGO [S12] | ÖSA [S10] |
|---|---|---|---|---|---|---|
| Endowment AVB located | **yes, three** (B LV 85/86/97) | no | yes | URL only, contested | no | no |
| Edition dates | 2026-07-01, 2025-01-01, 2025-01-01 | n/a | not established | 2022 / 2025 for the annuity siblings | n/a | n/a |
| Wording length | 21 / 19 / 18 pp | n/a | not established | not established | n/a | 3 pp (BIB) |
| Surplus base published | **yes** — % of *Deckungskapital* at allocation date | no | no | yes, for the annuity: booked into *Deckungskapital* | no | no |
| Surplus timing published | no | no | no | **yes** — 31 December *Bilanzstichtag* | no | no |
| Declared 2026 *laufende Verzinsung* | not established | **2.7 %** | not established | not established | not established | not established |
| *Stornoabzug* published | **yes** — 5 % + 5/10/15 % of *Deckungskapital* | no | no | no | no | no |
| *Zillmersatz* visible | no | no | **yes — 4 %**, the pre-LVRG ceiling | yes — 2,5 %, **both** editions zillmered | no | no |
| Paid-up clause visible | no | no | **yes** — full or partial reduction to the *beitragsfreie Versicherungssumme* | no | no | no |
| Premium ceases on death | no | no | **yes** | no | no | no |
| PRIIP-BIB located | no | no | no | no | no | **yes** |

Parameter ranges, where more than one observation exists:

| Parameter | Observed range | Who sits where | Tag |
|---|---|---|---|
| *Höchstrechnungszins* by cohort | 0.25 % – 4.00 %, currently 1.00 % | market-wide, by year of issue | [R7] |
| Declared *laufende Verzinsung* | 2.25 %–2.80 % at named carriers (2025) [R26]; 2.62 % annuity market average (2026) [R25] | Allianz 2.70 % at the top of the named range, Alte Leipziger 2.25 % at the bottom | [R25][R26] |
| *Höchstzillmersatz* by cohort | 40 ‰ (4 %) before 2015, 25 ‰ (2,5 %) from 1 January 2015 | Gothaer's 2011 wording at 4 %, die Bayerische and VPV at 2,5 % | [R7][S7][S9][S18] |
| *Ratenzahlungszuschlag* | 2 % half-yearly / 3 % quarterly / 5 % monthly | market convention, no carrier attribution | [R28] |
| *Stornoabzug* | three incompatible bases: 0–20 % of *Deckungskapital*; 50 € + 0,15 % of premiums × years remaining; 100 € + 0,2 % of (sum insured − reserve) | Debeka, die Bayerische, VPV | [S3][S9][S18][R30] |
| Contract term as sold | 12 years (tax minimum) to 40 years | market-wide | [R10] + consumer group |
| *Stornoquote* | 1.2 % (per contract) to 2.72 % (per the main GDV measure), 2024 | market-wide | [R20] |

**Representative design the research supports.** A single-life, individual, participating endowment
with **equal death and survival sums**; **level annual premium** over the full term; priced and
reserved at the **1,00 % *Höchstrechnungszins*** on a **DAV 2008 T-shaped, medically underwritten**
basis; **gezillmert to the 25 ‰ ceiling**; surplus declared **annually as a percentage of the
*Deckungskapital* at the 31 December balance date** and applied by ***verzinsliche Ansammlung***; a
**surrender value equal to the *gezillmert* prospective reserve floored by the five-year-spread
*Mindestrückkaufswert***, less a **contractual, pre-declared *Stornoabzug***; a **contractually
tabulated *beitragsfreie Versicherungssumme*** subject to a *Mindestversicherungsleistung* test; a
**three-year *Selbsttötung* window paying the *Rückkaufswert***; a **term of 25 to 30 years** ending
after age 62; and **no *Bewertungsreserven* participation in the base run**. Each choice is argued in
the product specification, and the ones the corpus does not source — the surplus application system,
the charge levels, the entry age, the sum insured, the *Stornoabzug* and the lapse rates — carry
`[std]` tags with the observed range beside them.

---

## Gaps and caveats

**Status after the retrieval pass of 2026-08-30 is noted on each gap.**

1. **No *Schlussüberschuss* rate of any kind was established.** *(open, better founded.)* The
   *mechanism* is now read in two endowment wordings: a *Schlussüberschusskonto* fed by an annual
   share of the interest-surplus base and itself bearing a declared rate, redeterminable for past
   years and able to fall to nil [S18]; and a *Schlussgewinnanteil* at maturity depending on the
   maturity sum and the accumulated surplus, reduced on surrender and death [S7]. **Still not one
   number**, for any insurer, in any year. Any *Schlussüberschuss* assumption in delib is `[std]`,
   and any *Gesamtverzinsung* printed in the library is a construction, not a citation.

2. **The declared-rate figures are for the annuity, not the endowment.** *(open, and worse than
   recorded.)* Assekurata states its own scope — "in der klassischen privaten Rentenversicherung"
   [R25]. **And the endowment counter-example has gone**: Allianz's pages carry no declared rate at
   all, and the 2,7 % is [R26]'s report of a **2025** declaration for a combined classic life-and-
   annuity book. So **no endowment-specific declared rate exists in the corpus**, and that the two
   products share a rate is `[unverified]`.

3. **The post-2005 collapse of endowment new business is not quantified.** *(**closed** by the
   retrieval of [R20]: the count of newly issued classic endowments runs 1.954,9 Tsd. in 2000 →
   1.354,2 in 2005 → 742,1 in 2010 → 527,2 in 2015 → 392,3 in 2020 → 325,3 in 2023, and the in-force
   share by annual premium was 15,7 % at end-2023.)* GDV publishes
   new-business *Beitragssumme* and APE series [R21], but **no endowment-specific new-business or
   in-force figure, and no time series showing the effect of the 2005 tax change, was established.**
   delib's market-role argument rests on Allianz's statement [S11] and the trade characterisation
   "Klassik wird zur Nische" [R26] — qualitative evidence.

4. **The market-default *Überschussverwendung* system is not established, and the fourth system is
   not established at all.** The corpus names *verzinsliche Ansammlung*, *Bonussystem* and
   *Beitragsverrechnung*, and says that as a rule "either the *verzinsliche Ansammlung* or the
   *Bonussystem*" applies [R28] — but not which. ***Anlage in Fondsanteilen* is not mentioned by any
   source in this corpus** and is `[unverified]`. delib's choice of *verzinsliche Ansammlung* for
   the base run is `[std]`.

5. **A search summary conflated § 169 Abs. 3 VVG with the DeckRV cap.** One summary stated that
   "according to § 169 Abs. 3 VVG the applied acquisition and distribution costs must be spread over
   at least the first five years and must not exceed 2,5 % of the contractual *Beitragssumme*". The
   five-year spreading is § 169 Abs. 3 VVG [R2]; the 2,5 % is the DeckRV *Höchstzillmersatz* [R7].
   **They are different rules with different functions and are kept apart throughout delib.** Any
   secondary source that merges them should not be followed.

6. **The MindZV's third bucket and the "*Kostenüberschuss*" of consumer sources are not the same
   thing.** MindZV requires 50 % of the ***übriges Ergebnis*** [R6]; consumer sources say "half of
   the *Kostenüberschuss*" [S16]. The *übriges Ergebnis* is wider. Both framings are recorded; **the
   MindZV framing is the one to cite**, and any statement that the cost surplus specifically carries
   a 50 % minimum is `[unverified]`.

7. **No charge level of any kind was established.** *(materially narrowed, not closed.)* Two cost
   observations now exist: BaFin's finding that in individual cases 2021 new business carried
   *Effektivkosten* "über vier Prozent", falling by more than 0,4 pp in the upper quartile at long
   durations by 2024 [R18]; and the ÖSA *Basisinformationsblatt*, which on its own model case shows
   total costs of 6.216 €, an annual cost impact of **5,3 %** at twenty years, entry costs of 2,2 %
   and ongoing administration of 28,5 % of the sum of all investment amounts [S10]. **What remains
   unestablished** is any *Abschlusskostenquote* or *Verwaltungskostenquote* for a named carrier, and
   **any commission rate at all** — the Die Stuttgarter 25 ‰ recorded here is not in the retrieved
   [R29] articles and is withdrawn. BaFin says *Effektivkosten*
   "differ considerably" and that it will examine outliers [R17], and makes cost a 2026 focus risk
   [R18], **without publishing a number in anything the searches returned**. **Every charge level in
   delib is `[std]`.** The fix is a PRIIP-BIB or a *Produktinformationsblatt*; [S10] is the one BIB
   located and its figures were not established.

8. **The *Bewertungsreserven* participation is established as a mechanism and not as an amount.**
   *(open as to amount; the *Sockelbetrag* limb is closed.)* The half share [R1][R8], the
   *Sicherungsbedarf* cut-back [R8] — which § 139 Abs. 3 VAG confines to fixed-income and
   interest-hedging reserves — and the leading case [R23] are established; **the amount actually
   distributed in any year, by any insurer, is not.** The ***Sockelbetrag*** now has **three
   independent witnesses**: the GDV Muster-Standmitteilung's "Sockelbeteiligung an
   Bewertungsreserven" [S2], die Bayerische's *Mindestbeteiligung* [S9], and [S18] § 2 Abs. 6. Its
   existence is established, it is contractual and declaratory rather than statutory, and **its size
   remains unobserved** — all three say it can fall away.

9. **No German *Produktinformationsblatt* or IPID for a kapitalbildende Lebensversicherung was
   located.** *(open; partly substituted.)* Debeka's index names IPID as a published document type
   [S6] and the regulatory content requirements are established [R9][R19], but **not one instance of
   either document was found**. The retrieved PRIIP-BIB at [S10] is the nearest substitute and does
   supply the fields a PIB would have carried — risk indicator, four performance scenarios, total
   costs, the annual cost impact and the premium split — but for a different product of one
   public-sector insurer, so entry age, sum-insured band, term band and charge levels for a classic
   endowment remain unobserved.

10. **The GDV *Stornoquote* is one unsuitable measure, not two irreconcilable ones.** *(restated by
    retrieval.)* The retrieved annual reports for **2023**: "Die Stornoquote (**Anzahl**) stieg im
    Jahr 2023 leicht auf **2,56 %** (Vorjahr: 2,51 %)" [R20]. It is a **count** measure over all
    German life business. The 2,72 %/2024 figure and the separate 1,2 % count measure recorded here
    before this pass are **not in the publication** and are withdrawn. The gap that remains is the
    one that matters: the measure is **not endowment-specific and not split by duration**, and BaFin's
    finding that lapse concentrates "in den ersten Jahren nach Vertragsabschluss" [R18] is exactly
    what an annual average cannot express.

11. **The second *Mindesttodesfallschutz* condition.** *(**closed** by reading § 20 Abs. 1 Nr. 6
    Satz 6 EStG.)* The provision reads: the halving is disapplied where, in addition to the 50 %
    limb, the benefit on the insured event does not exceed the *Deckungskapital* or *Zeitwert*
    "**spätestens fünf Jahre nach Vertragsabschluss** ... um mindestens 10 Prozent des
    Deckungskapitals, des Zeitwerts oder der Summe der gezahlten Beiträge", and "Dieser Prozentsatz
    darf bis zum Ende der Vertragslaufzeit in jährlich gleichen Schritten auf Null sinken." So the
    base is any of the three named, the time profile is the five-year point, the trailing words are
    the linear run-off to zero, and there is **no age-graded schedule**. The two limbs are cumulative,
    joined by "und".

12. **The DeckRV amendment date.** *(**closed**, and the date corrected.)* buzer's *Fassung* line
    reads "Artikels 1 Sechste Verordnung zur Änderung von Verordnungen nach dem
    Versicherungsaufsichtsgesetz V. v. **19. Juli 2024** BGBl. **2024 I Nr. 250** **m.W.v. 1. Januar
    2025**" [R7]. The announcement date is 19 July 2024, not 24 July; the year is no longer inferred;
    and the BGBl citation is established.

13. **The pre-2005 tax regime's conditions were not established.** The 1 January 2005 boundary and
    the taxation of the *Unterschiedsbetrag* on post-2004 contracts are established [R13][R10]. The
    **twelve-year term, five-year minimum premium-paying period and minimum death cover as a
    percentage of the *Beitragssumme*** the old regime required are **general knowledge, not sourced
    here**, and are `[unverified]`. delib models a post-2011 contract and does not assert them.

14. **No endowment-specific mortality table exists.** *(**answered** by reading the derivation paper
    and the *Richtlinie*.)* DAV 2008 T is a single *Schlusstafel* for death-benefit business built
    from observation years **2001 to 2004** on data from 47 undertakings; about 91 % of the
    observations are endowment data and endowment mortality from the sixth policy year is 101 % of
    the all-tariff level, so **there is no separate endowment table and no need for one** [R14]. The
    *Sicherheitszuschlag* **method** is established — *Schwankungs-*, *Irrtums-* and *Änderungsrisiko*,
    on a model portfolio of 200.000 lives aged 20 to 65 — but not its **level**. The delib decrement CSV is a `[std]` proxy
    that names DAV 2008 T and says what a replacement must preserve.

15. **No statutory version dates were established.** *(**closed**.)* Every statute the product turns
    on has since been read as canonical XML with its `Stand` attached: **§§ 19, 153, 161, 165, 168 and
    171 VVG** — *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*; **§ 139 VAG** —
    Art. 25 G v. 25.3.2026 I Nr. 81; **§§ 20 and 52 EStG** — Art. 7 G v. 29.6.2026 I Nr. 197; the
    **MindZV** — Art. 1 V v. 7.7.2020 I 1688; the **DeckRV** — Art. 1 V v. 19.7.2024 I Nr. 250, in
    force 1 January 2025. The `gesetze-im-internet.de/<law>/__NNN.html` pages are frameset shells with
    no statutory text and are kept as human-facing links only. The statutory statements in this file
    are now version-pinned.

16. **No premium rate table, no underwriting grid and no *Risikozuschlag* scale is public**, for any
    German endowment, from any carrier. This mirrors the frlib finding with one difference: frlib had
    **one** published attained-age rate card and delib has **none**. Every premium in delib is
    computed by the model's own equivalence principle on `[std]` bases, and no delib premium
    reproduces a published figure.

17. **The *Verwaltungskosten* form the brief anticipated was not confirmed.** The corpus establishes
    administration charges as **a percentage of the ongoing premium and/or a percentage of the
    *Vertragsguthaben*** [R28], and says nothing about a per-mille-of-*Versicherungssumme* charge or a
    fixed per-policy *Stückkosten* charge. Both are standard in German practice as far as general
    knowledge goes, but **neither is sourced here**; if delib uses either it is `[std]`.

18. **Three *Stornoabzug* schedules, on three incompatible bases.** *(superseded.)* Debeka: 5 % of
    the *Deckungskapital* plus 0/5/10/15 % by *Kapitalmarktsituation*, both decaying linearly to nil
    over the last ten years [S3][R30] — sub judice, a live Verbraucherzentrale collective action and
    a BGH remittal on *Angemessenheit* [R22]. Die Bayerische: 50 EUR plus 0,15 % of premiums paid
    times the years remaining to the original maturity [S9]. VPV: 100 € plus 0,2 % of the difference
    between the sum insured and the *Rückkaufswert* [S18]. **Three figures on three bases are not a
    market range either**, and no two of them can be averaged. The delib base value stays `[std]`, a
    declining percentage of the reserve, which matches one of the three shapes.

19. **The surplus *Wartezeit* varies by carrier and delib takes the shortest.** *(answered, and the
    answer is that there is no market convention.)* The retrieved wordings give three: **none** —
    "Der Anspruch auf Überschussbeteiligung beginnt sofort mit dem Versicherungsschutz" [S9]; **one
    year**, allocated at the start of the policy year [S18]; and **three years**, for Gothaer's tariff
    group A [S7] and for Debeka's *Zinsüberschussanteile* [S3]. `surplus_credit_pp` running from
    inception is therefore a `[std]` choice among three observed conventions, not a sourced fact, and
    the specification says so. The separate three-year *Selbsttötung* window [R4] is unrelated.

20. **Three statutory provisions the product depends on were never separately researched.**
    *(narrowed.)* **§ 152 VVG** (the 30-day *Widerruf* right), **§§ 37 and 38 VVG** (non-payment,
    *Mahnverfahren* and termination for arrears), and **§ 150 VVG** (insurance on the life of
    another, and the consent requirement). **§ 168 VVG has since been read** — the *Kündigung* right
    for the end of the current *Versicherungsperiode*, extended to single-premium contracts by
    Abs. 2 and excluded for certain retirement contracts by Abs. 3 — and is recorded at [R2]. Nothing is asserted about any of them anywhere in delib.
    They are named here so a later session knows exactly where the hole is.

21. **The typical-parameter section rests on one fused, unattributed summary and contains an
    internal contradiction.** A "minimum term" of 12 years and one of 3 to 5 years both appear,
    together with a minimum sum insured of 2 500 or 5 000 EUR that most likely belongs to a different
    product (section 19). **No entry age, no premium level and no maximum sum insured were
    established at all.** The delib model point is a `[std]` construction and the product
    specification says so in the table itself.

22. **Nineteen of the twenty-six named carriers produced nothing, and most of what the other seven
    produced is not an endowment wording.** *(restated by retrieval: the corpus has **two** endowment
    wordings, [S7] and [S18]; [S3]–[S5] and [S9] are annuity wordings; [S8] is a 404.)* R+V,
    Generali/Dialog, HDI, Alte
    Leipziger, LV 1871, Continentale, Nürnberger, Swiss Life, Zurich, AXA, Barmenia, Hannoversche,
    CosmosDirekt (beyond a glossary page), Württembergische, Volkswohl Bund, Baloise, Universa, DEVK,
    Signal Iduna, Provinzial and HUK-Coburg (beyond a term-life page) yielded **no endowment
    document**. The search budget ran out before their document libraries could be located, and **no
    URL was guessed for any of them.** delib's variations table is seven carriers wide against
    frlib's eight, and three of the seven publish quantified terms — Debeka, die Bayerische and
    VPV, each on a different *Stornoabzug* base.

23. **The search summaries fuse sources and do not attribute sentences** — a systematic limitation,
    not a per-entry one, and **the retrieval pass of 2026-08-30 shows how badly it bit**: of the nine
    extracted facts that did not survive retrieval (see the correction block at the head of
    *Extracted facts*), six were fusion artefacts — clauses of one document attributed to another,
    a *Termfixversicherung* rule read as an endowment rule, an annuity wording read as an endowment
    wording, a trade-press rate attributed to a manufacturer's page. Where a fact still carries
    several tags and no `Retrieved` line resolves it, it is because the summary matched several pages
    and named none. Sections 19 and 21, and the parts of section 10 tagged to the "R28 family",
    are where this still bites; those sections have not been re-derived from documents.

24. **One Austrian document was returned and is excluded.** ERGO Versicherung AG's AVB "K119 Kapital
    und Rente" (`https://ergo-versicherung.at/fileadmin/user_upload/pdf/Versicherungsbedingungen/
    K119_Kapital_und_Rente_01.pdf`) matched the AVB search. It is an **Austrian** wording: the German
    VVG, DeckRV and MindZV do not apply to it, and its *Rückkaufswert*, *Zillmerung* and surplus
    rules are governed by the Austrian VersVG and VAG. **Nothing in this file is cited to it**, and
    it is recorded only so a later reader does not mistake it for a German source. The same caution
    applies to any `.at` or `.ch` document a future search returns.
