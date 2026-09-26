# Klassische aufgeschobene private Rentenversicherung — research notes (Germany)

Research notes for the German **classic deferred private annuity** — *klassische aufgeschobene
private Rentenversicherung*, the Schicht-3 (third-layer, unsubsidised private) contract in which
premiums accumulate in the *Deckungskapital* (policy reserve) of the insurer's general account at
the guaranteed *Rechnungszins* (technical interest rate) with *Überschussbeteiligung* (profit
participation), and in which the accumulated capital is converted at the *Rentenbeginn* (annuity
commencement date) into a lifelong *Leibrente* at a guaranteed *Rentenfaktor* (annuity factor), or
taken instead as a lump sum under the *Kapitalwahlrecht* (lump-sum option).

**In scope.** The single-life, deferred, general-account ("konventionell", "klassisch") private
annuity sold to individuals outside any state subsidy, against a level recurring premium or a
single premium, with a deferment period ending at a contractually fixed *Rentenbeginn*; its
accumulation-phase reserve mechanics; its death benefit before *Rentenbeginn*; the annuity
conversion at the *Rentenfaktor*; the payout-phase annuity and its surplus systems; and the
statutory options (*Rückkaufswert*, *Beitragsfreistellung*, *Kapitalwahlrecht*, *Zuzahlung*,
*Dynamik*).

**Out of scope, and named here so the boundary is explicit.**

- **Schicht 1 — Basisrente (Rürup)** and **Schicht 2 — Riester-Rente and betriebliche
  Altersversorgung (bAV)**. Both are separate delib products (`basisrente`, `riester_rente`) or
  outside the library entirely (bAV: Direktversicherung, Pensionskasse, Pensionsfonds,
  Unterstützungskasse, Direktzusage). The GDV publishes a *separate* model-condition set for the
  Basisrente [S3], and the R+V Pensionskasse AG publishes its own AVB for a *Pensionskasse*
  annuity against single premium under tariff 970 — a Schicht-2 vehicle, not this product. Neither
  is used as a source for Schicht-3 mechanics here.
- **Fondsgebundene Rentenversicherung** (unit-linked, delib `fondsgebundene_rentenversicherung`)
  and **indexgebundene / "Neue Klassik"** hybrids (delib `indexpolice`), referenced only where a
  document covers both and the classic mechanics show through the contrast — the *Rentenfaktor*
  literature is dominated by unit-linked material [R16] [R19] [R24], because in a unit-linked
  contract the *Rentenfaktor* is the **only** guarantee, and the DEVK wording [S19] is used solely
  for that contrast.
- **Sofortbeginnende Rentenversicherung** (immediate annuity, delib `sofortrente`). The payout
  phase of this product and the whole of that one are the same machinery; the Zurich *sofort
  beginnende Rentenversicherung* consumer information [S16] is recorded here because German
  insurers derive the *aktueller Rentenfaktor* of a deferred contract from the tariff they are
  then writing for immediate annuities [S13] [R23], which makes the immediate-annuity document the
  direct evidence for the deferred contract's conversion basis.
- **Kapitalbildende Lebensversicherung** (endowment, delib `kapitallebensversicherung`), which
  shares the entire *Überschussbeteiligung* and *Deckungskapital* / *Rückkaufswert* chassis; the
  difference is only what happens at the end of the accumulation phase. Shared-chassis facts are
  recorded here anyway so this file stands alone, but the endowment file is the primary home for
  the four surplus components.
- **Gruppenversicherung**, **private Krankenversicherung**, **Sterbegeldversicherung** and
  institutional pension-risk transfer.

These notes are the citation ground truth for the delib `klassische_rentenversicherung` product
documents: source ids **S1..S19** and **R1..R24** below are **frozen — never renumber**. Unused
ids are simply omitted downstream, leaving gaps, and `sources.md` records which ids are absent and
why.

Access date for all citations: **2026-08-29**.

---

## Citation discipline and retrieval conditions

This section has two halves: how the research was **done**, on 2026-08-29, and what the
**re-verification** of 2026-08-30 established. The first half is kept because it is the record of
how the file came to say what it says; the second is what a reader should weigh each entry by.

**No document listed in this file had been retrieved when it was written.** Direct HTTP egress from
the build environment was blocked by an organisation network policy. `WebFetch` and `curl` were refused with HTTP 403
at the egress gateway for every host outside a short package-registry allowlist. The hosts that
mattered for this product — `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
`bundesfinanzministerium.de`, `dejure.org`, `de.wikipedia.org`, and every insurer host named below
(`zurich.de`, `cosmosdirekt.de`, `nuernberger.de`, `debeka.de`, `allianz.de`) — are all refused.

The **only** research channel available was the `WebSearch` tool, which returns titles, URLs and
search-engine summaries. Everything in the drafted file rested on those summaries. They are real evidence
and they do return substantive content — several of the most load-bearing facts below (the
CosmosDirekt conversion basis, the Zurich two-factor comparison, the § 165 VVG paid-up formula)
came back as near-verbatim renderings of the document's own sentences — but a search summary is a
*secondary summary*, never a retrieved document.

That changed exactly two things in the draft:

1. **Every source entry recorded `Retrieved: no — direct HTTP egress blocked in the build
   environment; established from search-result summaries`.** Nothing was marked retrieved. No
   quotation was invented. Where a short phrase was given in quotation marks, it was a phrase the
   search summary itself returned, attributed to the summary rather than to the document. **This is
   the rule the re-verification changed**: every entry now carries its own `Retrieved:` line, and
   where that line says yes the entry also quotes the document itself.

2. **`[unverified]` keeps its normal meaning** — a claim that no search result corroborated. It is
   not applied to everything. A fact that several independent search results agree on is not
`[unverified]`; a paragraph number, an effective date, a tariff level or a market figure that no
search result confirmed **is**.

Every URL below is one a search result actually returned, or the obvious canonical
`gesetze-im-internet.de` form of a statutory article that several legal-database mirrors returned
(for example `https://www.gesetze-im-internet.de/vvg_2008/__169.html` for § 169 VVG). **No URL, no
document reference number, no paragraph number and no figure in this file was guessed.** Where a
URL is not available it says `URL: not established`.

**A second, harder constraint applies to this file specifically.** The session's `WebSearch`
budget was shared across fourteen parallel researchers and was **exhausted after eighteen queries
on this product**. The brief anticipated thirty to eighty. The consequence is recorded in full in
the gaps register (gap 1) and it is the single most important caveat on everything below: whole
areas the brief asked for — current *Rentenfaktor* market levels, charge levels, entry-age and
premium envelopes, the 2025/2026 *Überschussbeteiligung* declarations, the *Kapitalwahlrecht*
notice period, the *Zuzahlung* mechanics, the unisex rule — are recorded as **gaps, not as
facts**. Nothing was written to fill them.

**The re-verification of 2026-08-30.** The policy was lifted and the citations were checked against
the primary documents. Library-wide, all fifteen German instruments delib cites were read as
canonical XML from `gesetze-im-internet.de` with each law's amendment `Stand` recorded, 950
statutory section references were checked and 950 were correct, and insurer AVB,
*Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read; **501
of the library's 805 source entries, 62 %, now read `Retrieved: yes`.** For this product: **36 of
the 43 entries below read `Retrieved: yes`, three read `no` ([S17], [S19], [R23]) and four are
partial ([R12], [R13], [R14], [R19])**. What stayed shut names its wall per entry: HTTP 200 with a
212-byte shell and no page body ([S17]), HTTP 403 at the cited URL and on a direct retry ([S19]), a
paywall body in place of the article ([R23]), and, inside the partials, an HTTP 404 on the second of
two addresses ([R19]) and DAV and industry PDFs opened only at their front matter ([R12], [R13],
[R14]).

**What an entry now means.** A **`Retrieved: yes`** line means the document was opened and the
passage the entry rests on was read; the line records the PDF's page count and *Stand* or the law's
amendment status, and a German sentence quoted beneath it is a quotation **of the document**. A
**`Retrieved: no`** line means the entry is still **a pointer rather than a certificate**, and a
quoted phrase there is still a phrase a search summary returned. **The re-verification changed
things**: fifteen of the twenty-six gaps below are closed, five of them by a retrieved document
**contradicting** what the gap or its entry had said, and the register states the contradictions
rather than smoothing them over. What the budget still determines is the *market* material — current
*Rentenfaktor* levels, charge levels, the envelopes and the declarations — which no document
supplied. Treat a claim here as sound where its entry says `Retrieved: yes`, and as provisional
where it does not.

---

## German terminology

German terms of art stay in German throughout the delib documents, italicised on first use with a
gloss. The vocabulary this product needs:

| Term | Gloss |
|---|---|
| *Aufschubzeit* / *Aufschubdauer* | deferment period, from inception to *Rentenbeginn* |
| *Rentenbeginn* | annuity commencement date; the contractual boundary between accumulation and payout |
| *Rentenbezugsphase* / *Rentenphase* | payout phase, the period over which the annuity is in payment |
| *Leibrente* | life annuity: payable for as long as the annuitant lives |
| *Deckungskapital* | the policy's accumulated reserve; the per-policy quantity the recursion rolls forward |
| *Rechnungszins* | technical interest rate used in the tariff; the rate at which the *Deckungskapital* is guaranteed to accumulate |
| *Höchstrechnungszins* (*Garantiezins*) | the statutory maximum *Rechnungszins* for new business, set in the *Deckungsrückstellungsverordnung* |
| *Sparbeitrag* / *Risikobeitrag* | the savings portion of the premium — what is left after the risk and expense charges — and the risk portion |
| *Überschussbeteiligung* | profit participation: the policyholder's share of the insurer's surplus |
| *Schlussüberschussanteil* | terminal bonus, paid at *Rentenbeginn* or on earlier exit |
| *Bewertungsreserven* | unrealised capital gains in the insurer's assets; policyholders participate under § 153(3) VVG |
| *verzinsliche Ansammlung* | the surplus system in which declared surpluses are credited to a side account and accumulate with interest |
| *Ansammlungsguthaben* | the balance of that side account |
| *Bonusrente* | the surplus system in which declared surpluses buy additional paid-up annuity |
| *Beitragsverrechnung* | the surplus system in which surpluses are set against the premium due |
| *Überschussrente* | the surplus-financed part of the annuity in payment, as against the *garantierte Rente* |
| *garantierte Rente* | the guaranteed annuity, computed on the tariff bases alone |
| *Rentenfaktor* | annuity factor: the monthly annuity per 10 000 € of capital at *Rentenbeginn* |
| *garantierter Rentenfaktor* | the factor guaranteed at inception on the tariff bases, a floor |
| *aktueller Rentenfaktor* | the factor the insurer is currently applying, recomputed on current bases |
| *Treuhänderklausel* | trustee clause: a conditions clause letting the insurer change contract terms with an independent trustee's approval |
| *Rentengarantiezeit* | annuity guarantee period: the annuity keeps being paid to survivors if the annuitant dies inside it |
| *Beitragsrückgewähr* | return of premiums as the death benefit |
| *Kapitalwahlrecht* / *Kapitalabfindung* | the policyholder's option to take the accumulated capital as a lump sum instead of the annuity, and the lump sum itself |
| *Rückkaufswert* | surrender value |
| *Stornoabzug* (*Rückkaufsabschlag*) | the surrender charge deducted from the computed surrender value |
| *Zillmerung* | the reserving method that front-loads acquisition costs against the reserve |
| *Beitragsfreistellung* | conversion to a premium-free (paid-up) contract |
| *beitragsfreie Versicherungsleistung* | the reduced benefit after *Beitragsfreistellung* |
| *Zuzahlung* | an ad-hoc additional single premium into an existing contract |
| *Dynamik* / *Anpassungsversicherung* | the automatic annual premium-and-benefit increase option |
| *Ratenzahlungszuschlag* | the loading for paying the annual premium in instalments |
| *Ertragsanteil* | the taxable fraction of a private life annuity under § 22 EStG |
| *Schicht 1 / 2 / 3* | the three layers of the German retirement-provision architecture; this product is Schicht 3 |
| *Rechnungsgrundlagen* | the tariff bases: mortality table, interest rate and expense loadings |
| *Sicherungsvermögen* | the ring-fenced general account backing guarantees |

---

## Primary sources

Nineteen primary product documents and product pages. Four families dominate: the **GDV model
conditions** [S1] [S2] [S3] [S10], the industry's shared drafting template and the closest thing
German life insurance has to a canonical wording; the **Zurich Deutscher Herold
consumer-information series** [S4]–[S7] [S16] [S17], the only insurer corpus here that publishes
the *same* deferred-annuity document across several vintages, so drafting continuity is visible;
the **CosmosDirekt AVB** [S8], the only document whose conversion basis a search summary returned
explicitly; and the **Debeka** documents [S11] [S12], which matter because Debeka is the market's
largest classic-guarantee life writer and because it withdrew this exact product from sale [R22].

### S1 — GDV, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung" (Musterbedingungen)
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin
- Doc type: *Musterbedingungen* — model general policy conditions for a deferred annuity contract;
  the association's template wording, which individual insurers adopt, adapt or ignore.
- URL: https://www.gdv.de/resource/blob/6294/61b4fedd6f69db77539816e3421c7eeb/allgemeine-bedingungen-fuer-die-rentenversicherung-mit-aufgeschobener-rentenzahlung-data.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 20 pp., **Stand: 21.07.2025**, twenty §§. Clause text
  read in full; the §§ cited downstream are checkable against it.
- Content: the GDV's model condition set for exactly the product in scope — a *Rentenversicherung
  mit aufgeschobener Rentenzahlung* — whose family addresses **Beitragsrückgewähr** (return of
  premiums as the death benefit), **contract values**, **minimum guarantees**, and the
  **conditions under which the annuity is paid**. It appeared in the result set for two independent
  queries, which fixes it as the reference wording for the mechanics extracted below. **No
  paragraph numbering, no clause text and no page count were established** — gap 2.

**Retrieval note (2026-08-30).** Gap 2 is closed for this document. Twenty §§ over 20 pp., *Stand: 21.07.2025*. The disclaimer reads *"Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ. Abweichende Bedingungen können vereinbart werden."* **Correction:** the wording does **not** specify a pre-annuity death benefit — § 1 Abs. 3 reads *"zahlen wir …"* against the footnote *"Unternehmensindividuell zu ergänzen"*, and *Beitragsrückgewähr* occurs only in the footnotes to §§ 4 and 5. So the model conditions name the concept without prescribing the benefit; the base design is re-sourced to [S8] and [S9]. Newly established from it: § 1 Abs. 4 *Rentengarantiezeit* with a ten-year worked example; § 2 Abs. 5 the *Bewertungsreserven* re-measurement points, including *"für den Beginn einer Rentenzahlung"*; § 12 Abs. 3 the § 169 surrender floor; § 13 the *Beitragsfreistellung*; § 14 Abs. 2 the *Zillmer* cap at *"2,5 % der von Ihnen während der Laufzeit des Vertrages zu zahlenden Beiträge"*.

### S2 — GDV, "02 GDV-Musterbedingung LV — Rentenversicherung mit aufgeschobener Rentenzahlung" (2021 edition)
- Publisher: GDV
- Doc type: *Musterbedingungen*, 2021 edition of the same wording as [S1], on the same GDV resource
  path (blob id 6294 in both cases, distinct content hashes — two editions of one family).
- URL: https://www.gdv.de/resource/blob/6294/cacd502172fab87ad8859d194d9352c8/02-gdv-musterbedingung-lv-rentenversicherung-mit-aufgeschobener-rentenzahlung-2021-data.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 20 pp., **Stand: 21.07.2025**. The two GDV URLs serve
  one and the same file; see the retrieval note.
- Content: the search result's own title line for this document is **"Diese Bedingungen sind
  unverbindlich"** — the GDV's standing disclaimer that the wording is non-binding and its use
  purely optional. That governs how [S1] and [S2] may be used downstream: they establish the
  **shape** of the German market's wording, not any insurer's obligation. The file name dates the
  edition to **2021**, i.e. drafted under the 0,90 % *Höchstrechnungszins* regime and before the
  1,00 % regime of 2025 [R7] [R8].

**Retrieval note (2026-08-30). Correction.** Both GDV blob URLs serve **one and the same file**, *Stand: 21.07.2025*, with page-for-page identical extracted text. The `…-2021-…` in the file name is not an edition date, so the "two editions of one family" reading and the 2021 / 0,90 %-regime dating are withdrawn. The disclaimer quoted from the search title line is, in the document, *"Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ."* A GDV blob id addresses a living file, not a vintage.

### S3 — GDV, "Musterbedingungen" service index
- Publisher: GDV
- Doc type: publisher index page listing the association's model-condition sets
- URL: https://www.gdv.de/gdv/service/musterbedingungen
- Retrieved: **yes**, on 2026-08-30 — HTML index page, product list read in full.
- Content: establishes that the GDV maintains model conditions across product lines, that **their
  use is non-binding and optional**, and the **product taxonomy** used in the scope note: separate
  model conditions exist for (a) *Rentenversicherung mit aufgeschobener
  Rentenzahlung* — this product [S1] [S2]; (b) *Rentenversicherung gemäß § 10 Absatz 1 Nr. 2
  Buchstabe b Doppelbuchstabe aa EStG* — the **Basisrente (Alter)**; (c) a *fondsgebundene*
  Riester wrapper under the *Altersvorsorgeverträge-Zertifizierungsgesetz*; (d) a non-unit-linked
  variant of the same, whose search result carried the date **"Stand: 21.07.2025"**; and (e) the
  *Hinterbliebenenrenten-Zusatzversicherung* rider [S10]. The statutory reference in (b) was
  returned inside the GDV's own file name and is recorded only as this product's **boundary**: a
  Schicht-3 contract takes no § 10 deduction.

**Retrieval note (2026-08-30).** The taxonomy is confirmed off the index itself. Under *Rentenversicherungen* the GDV lists, as separate sets: the deferred annuity (this product), the *Basisrente-Alter* by its § 10 Abs. 1 Nr. 2 Buchst. b Doppelbuchst. aa EStG title, the immediate annuity, the *fondsgebundene Rentenversicherung*, and two *AltZertG* sets — one unit-linked, one not. A *Hinterbliebenenrenten-Zusatzversicherung* set exists for each of the three annuity families.

### S4 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung, Private Vorsorge (Schicht 3) und Rückdeckungsversicherung (Schicht 2)", Fassung 01/2026
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation* — the consolidated pre-contractual pack a German life insurer
  must supply: general information, the AVB, the special conditions for riders and options, and
  the tax notes. Document code **521331262 2601** appears in the search result's title line.
- URL: https://www.zurich.de/-/media-assets/project/zurich-headless/germany/br/documents/verbraucherinformationen/32020_aufgeschobene-rentenversicherung_verbraucherinformationen_2026_01.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 66 pp., document code 521331262 2601, Fassung 01/2026;
  24 §§ of AVB plus the *Anpassungsversicherung* and rider condition sets.
- Content: the **current-vintage anchor document of this file**. It is a *Verbraucherinformation für
  Konventionelle Versicherungen* — "konventionell" being the German market's word for the
  general-account, non-unit-linked chassis. Its scope line covers **"Aufgeschobene
  Rentenversicherung — Private Vorsorge (Schicht 3) und Rückdeckungsversicherung (Schicht 2)"** in
  the **Fassung 01/2026**; the *Schicht 3* label is the insurer's own placement of the product and
  is the direct source for the scope note above. Its structure is: **allgemeine Informationen**;
  the **Allgemeine Versicherungsbedingungen**; **Besondere Bedingungen für die
  Anpassungsversicherung in der Rentenversicherung** — the *Dynamik* option, therefore a documented
  contractual option with its own condition set; **allgemeine steuerliche Hinweise**; and
  **Besondere Bedingungen für die Berufsunfähigkeits-Zusatzversicherung**. On the *Rentenfaktor*:
  the guaranteed factor is described as carefully calculated, and **at the start of annuity payments
  a second *Rentenfaktor* is compared with it, the higher of the two being guaranteed for the
  annuity payment period** — the single most important mechanic in the file (section 8). On
  *Bewertungsreserven*: **the transition to annuity payment is a key point for participation**, and
  policyholders **also participate during the annuity payment period**, in accordance with the
  applicable VVG and supervisory provisions; the summary states that **§ 153 Absatz 3 VVG currently
  provides for equal (hälftige) participation**.

**Retrieval note (2026-08-30).** Clause text read. Newly established: § 1 Abs. 6, *"Die Kalkulation … basiert auf der Sterbetafel DAV 2004R (Aggregattafel); es wird ein Rechnungszins in Höhe von 1,00 % verwendet"*; § 1 Abs. 2 that without an extension death before the *Rentenzahlungsbeginn* pays nothing; § 2 Abs. 2–3 the *Kapitalwahlrecht* notice periods (three years, or twelve years / five months); § 3 Abs. 2 the *hälftige Beteiligung* and the *Übergang in den Rentenbezug* as the *maßgeblicher Zeitpunkt*; § 3 Abs. 7 the three payout-phase systems by name and the one-year promise on the RfB-financed part; § 10 Abs. 3 a *Stornoabzug* of a flat **250 EUR**; § 11 Abs. 2 the 2,5 % *Zillmer* cap; footnote 1 a *Mindestrente* of 25 EUR a month; and the *Anpassungsversicherung* conditions at pp. 19–20. **Correction:** the string *Rentenfaktor* does not occur in the 66 pages, so the `max(f_g, f_c)` rule attributed to this document is re-sourced to [S9] [S14] [S18]. **Contradiction:** § 1 Abs. 5 offers *Beitragsrückgewähr während der Rentenzahlungszeit* as an alternative to the *Rentengarantiezeit*, which contradicts gap 18.

### S5 — Zurich Deutscher Herold Lebensversicherung AG, same series, Fassung 01/2021 — 44 pages
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation für Konventionelle Versicherungen*, deferred annuity, private
  provision. Document code **521331422 1507**; title line "Seite 1 von 44" — **44 pages**.
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/330202101_aufgeschobene-rentenversicherung-private-vorsorge_verbraucherinformationen_2021_01.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 44 pp., document code 521331422 1507, **Fassung
  07/2015**, *Konsortialversicherung — Private Vorsorge*.
- Content: described as containing **"Versicherungsbedingungen für die aufgeschobene
  Rentenversicherung (Konsortialversicherung) — Private Vorsorge und Rückdeckungsversicherung"**,
  with sections on **the contract partners, the scope of cover, the design options and the
  *Überschussbeteiligung***. Same product as [S4] five years earlier; the pairing of vintages
  establishes the wording as continuously maintained. One document in the same result set was
  reported to **discuss the guarantee amounts and how the benefits are calculated at the end of the
  deferment period** — the conversion mechanic — but the summary did not say which, so it is
  recorded without a pinpoint.

**Retrieval note (2026-08-30). Two corrections.** The Fassung is **07/2015**, not 01/2021 — the `_2021_01` in the URL is a media-path slot. And the document is the **Konsortialversicherung** edition, *Private Vorsorge* wrapper. Its § 1 Abs. 6 gives *"der Sterbetafel DAV 2004R (Aggregattafel); es wird ein Rechnungszins in Höhe von 1,25 % verwendet"* — the earliest guarantee vintage in the corpus.

### S6 — Zurich Gruppe, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung (Konsortial)" — 46 pages
- Publisher: Zurich Gruppe Deutschland
- Doc type: *Verbraucherinformation*, consortium (*Konsortialversicherung*) edition. Document code
  **521331432 1507**; title line "Seite 1 von 46" — **46 pages**.
- URL: https://www.zurich.de/-/media-assets/project/zurich-headless/germany/docs/privatkunden/vorsorge-und-vermoegen/existenzsicherung/231_zurich_gruppe_vi_aufgeschobene_rentenversicherung_konsortial.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 46 pp., document code 521331432 1507, **Fassung
  07/2015**, *Konsortialversicherung — Rückdeckungsversicherung*.
- Content: the same product underwritten by a consortium rather than one carrier; two pages longer
  than [S5]. Establishes that one carrier issues the **same wording in more than one distribution
  wrapper** — a wrapper variation, not a liability variation.

**Retrieval note (2026-08-30).** Confirmed: Fassung 07/2015, *Konsortialversicherung — Rückdeckungsversicherung*, 46 pp., § 1 Abs. 6 identical to [S5]'s at 1,25 %. [S5] and [S6] are therefore the *Private Vorsorge* and *Rückdeckungsversicherung* wrappers of one consortium wording, which is the wrapper finding demonstrated rather than inferred.

### S7 — Zurich Deutscher Herold Lebensversicherung AG, same series, Fassung 01/2022
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation*, deferred annuity. Document code **521331392 2501**.
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/220202101_aufgeschobene-rentenversicherung_verbraucherinformationen_2022_01.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 58 pp., document code 521331392 2501, **Fassung
  01/2025**, *Direktversicherung nach § 3 Nr. 63 EStG (Schicht 2)*.
- Content: the third vintage. Its value is chronological: with [S5] (2021), [S7] (2022) and [S4]
  (2026) this carrier is shown writing the product **across three *Höchstrechnungszins* regimes**
  [R7] [R8] [R11]. No clause-level content established from this edition.

**Retrieval note (2026-08-30). Two corrections.** The Fassung is **01/2025**, not 01/2022 (the document code's `2501` agrees), and the edition is a ***Direktversicherung* nach § 3 Nr. 63 EStG — Schicht 2**, not the Schicht-3 private annuity. § 1 Abs. 7 gives DAV 2004R with a *Rechnungszins* of **1,00 %**.

### S8 — Cosmos Lebensversicherungs-AG (CosmosDirekt), "Allgemeine Bedingungen für die Rentenversicherung", LA 904 A
- Publisher: Cosmos Lebensversicherungs-AG (the direct-writing arm of Generali Deutschland)
- Doc type: *Allgemeine Bedingungen* (AVB) for a *Rentenversicherung*, tariff code **LA 904 A**
- URL: https://www.cosmosdirekt.de/resource/blob/89106/31bbdccea1c7a5a530feb9e2a3be8d1c/allgemeine-bedingungen-rentenversicherung-la-904-a--data.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 8 pp., **LA 904 A (01.17)**, eighteen §§.
- Content: **the most quantitatively load-bearing document in the corpus.** A search summary
  returned its conversion basis in terms: **"The annuity factor determined at the beginning of the
  contract is calculated on the basis of a recognised mortality table (currently DAV 2004 R) and an
  underlying interest rate (currently 0 percent p.a.)."** That establishes three things at once:
  the *garantierter Rentenfaktor* is fixed **at inception**; the table is **DAV 2004 R** [R12]
  [R13]; and at this document's vintage the guaranteed factor's **interest basis was 0 % p.a.** —
  below the then-current *Höchstrechnungszins*, and therefore a deliberate prudential margin rather
  than the statutory maximum. On *Überschussbeteiligung*, the standard AVB disclaimer: **"the
  amount of profit sharing depends on many influences which are unpredictable and only limitedly
  controllable by the company, with the most important influencing factor being capital-market
  developments."** The document also appeared in the result set for the death benefit before
  *Rentenbeginn*. **The vintage of LA 904 A was not established**, which matters because the
  "currently 0 percent p.a." clause is explicitly time-stamped — gap 5. Siblings fix the house
  numbering: **LA 1204 A (11.22)**, **LA 1201 A (11.22)** (8 pp.), **LA 1005 A** (Riester),
  **LA 1311 A** (FlexInvest), **LA 1100 A** and **LA 1079/936/1099 A** (Basisrente), **LA 1081 A**
  (Direktversicherung) — LA 904 being the oldest number in that list.

**Retrieval note (2026-08-30). Vintage established and the load-bearing sentence contradicted.** The edition is **LA 904 A (01.17)** — gap 5 closed. The document does **not** contain the sentence the search summary reported: the string *DAV* does not occur in it, and the only rate it names is the *"tarifliche[r] Garantiesatz von 0,90 Prozent p. a."* (§ 1 Abs. 2), not 0 percent. The *Sicherheitsabschlag* argument built on "0 percent against a positive cap" therefore has no basis here and is re-sourced to [S11]'s 0,1 % *Rentenfaktor* basis against a 1 % tariff rate. What the document does establish, and better than the summary: § 1 Abs. 1, *"Stirbt die versicherte Person während der Aufschubzeit, so zahlen wir als Todesfall-Leistung die eingezahlten Beiträge (Beitragsrückgewähr) ohne Zinsen … zurück"*; § 1 Abs. 2 the accumulation recursion with its rate; § 2 the MindZV shares 90 / 90 / 50; a *Treuhänder* clause on the *Rechnungsgrundlagen* at *Rentenbeginn*; a *Mindestrente* of 600 EUR a year; and § 7 Abs. 10, *no Stornoabzug at all*.

### S9 — NÜRNBERGER Lebensversicherung AG, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung und Rentengarantiezeit nach Tarif NIR3301"
- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: AVB for a deferred annuity **with *Rentengarantiezeit***, tariff **NIR3301**; publisher
  document id `gn331451_p`
- URL: https://www.nuernberger.de/medien/4allportal/gn331451_p.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 17 pp., edition id **GN331451_202501**, twenty-one §§.
- Content: the only document whose **title itself names the *Rentengarantiezeit***, establishing it
  as a **tariff-level design feature carried in the product name**, not merely a rider. The summary
  establishes that **the contract value used for annuitisation includes any *Überschussbeteiligung*
  and *Bewertungsreserven*, subject to a minimum guaranteed contract value stated in the general
  contract data** — the conversion input in one sentence. Siblings in the same result set:
  `gn331530_p` (fondsgebunden) and `gn331303_p` (*mit sofort beginnender Rentenzahlung*). No
  paragraph numbering established.

**Retrieval note (2026-08-30).** Edition id **GN331451_202501**. The two conversion rules are now verbatim: § 1 Abs. 1, *"wird der Vertragswert zuzüglich gegebenenfalls vorhandener Werte aus dem Schlussüberschuss und aus der Beteiligung an den Bewertungsreserven herangezogen …, mindestens aber der garantierte Vertragswert"*, and *"Wir prüfen bei jeder Monatsrente einzeln, ob die rechnungsmäßige Rente … höher ist als die garantierte Mindestrente und zahlen immer den höheren Betrag"*. Also newly established: the current factor is taken from *"vergleichbarer, dann bei uns zum Verkauf geöffneter Rentenversicherungen mit sofort beginnender Rentenzahlung"* with a *Treuhänder* review; the guaranteed basis is the carrier's own *NÜRNBERGER Tafel 2013R* at 1 % p. a.; § 1 Abs. 3 pays the contract value *"mindestens jedoch die sogenannte Beitragsrückgewähr"*, which is the `max` death-benefit shape for a **classic** product; the annuity is paid *"monatlich, jeweils zum Monatsersten"* (gap 19); § 2 Abs. 5 c) names the *dynamische Überschussrente* and the *teildynamische Bonusrente*; and § 14 Abs. 4 levies **no Stornoabzug**.

### S10 — GDV, "Allgemeine Bedingungen für die Hinterbliebenenrenten-Zusatzversicherung zur Rentenversicherung mit aufgeschobener Rentenzahlung"
- Publisher: GDV
- Doc type: *Musterbedingungen* for the **survivor's-annuity rider** attaching to this product
- URL: https://www.gdv.de/resource/blob/6336/942f7b9aec6a969b486ec205279870a3/allgemeine-bedingungen-fuer-die-hinterbliebenenrenten-zusatzversicherung-zur-rentenversicherung-mit-aufgeschobener-rentenzahlung-0-pdf-data.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 6 pp., **Stand: 14.11.2019**, four §§.
- Content: establishes that the market treats the **survivor's annuity as a *Zusatzversicherung*
  (rider) with its own condition set**, attached to the base contract rather than a benefit of it —
  so a reference implementation carries it as a module **off in the base run**. No clause content
  established.

**Retrieval note (2026-08-30).** *Stand: 14.11.2019*, 6 pp., four §§. Clause content established, and it adds a mechanic: § 1 Abs. 3 pays the *Hinterbliebenenrente* only **after** any *Rentengarantiezeit* expires, so the two post-*Rentenbeginn* death mechanics run in sequence rather than stacking; [S4] § 10 Abs. 15 makes the commutation of a guarantee period unavailable where an HZV is included. § 2: if the *mitversicherte Person* dies first the rider ends with no benefit.

### S11 — Debeka Lebensversicherungsverein a. G., "Allgemeine Bedingungen für eine Rentenversicherung mit …" (B LV 85)
- Publisher: Debeka Lebensversicherungsverein a. G., Koblenz
- Doc type: AVB, house document code **B LV 85**
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 21 pp., **B LV 85 (01.07.2026)**, Tarif CA2I
  (ABAR-IT 07/2026), 59 §§ in six parts.
- Content: the title was returned truncated ("… mit …"), so the exact product variant is **not
  established**. Siblings fix the house numbering and its currency: **B LV 100 (01.07.2026)**,
  16 pp., and **B LV 101 (01.01.2025)**, 17 pp., both in the *betriebliche Altersversorgung* folder
  and out of scope — but they establish that Debeka's AVB series was being reissued as recently as
  **1 July 2026** (gap 9). The related summary establishes Debeka's own definition of the
  accumulation quantity: **the *Deckungskapital* is the sum of the contributions accumulated at the
  *Rechnungszins*, insofar as those contributions are not required for risk and expense cover** —
  the cleanest statement of the recursion in the corpus, and the basis of section 5.

**Retrieval note (2026-08-30). The URL now serves a different document.** B LV 85 today is **(01.07.2026)**, *"Allgemeine Bedingungen für eine Rentenversicherung mit aufgeschobener Rentenzahlung und Fondskomponenten nach Tarif CA2I (ABAR-IT 07/2026)"* — the *garantiebasierter* / *fondsgebundener Baustein* successor design of [S12], not the classic chassis. **The sentence this entry called the corpus's cleanest statement of the accumulation recursion is not in it**; the recursion is re-sourced to [S8] § 1 Abs. 2 and to [R1]. What the retrieved text does give: § 52 Abs. 1, *"Der garantierte Rentenfaktor gibt an, wie viel Rente wir Ihnen monatlich je 10.000 Euro des zum Rentenbeginn zur Verfügung stehenden Fondsguthabens zahlen. Wir legen ihm einen Rechnungszins von 0,1 % p. a. und die unternehmenseigene geschlechtsunabhängige Sterbetafel „Debeka 07/16 R (RF)" zugrunde"*, against guaranteed benefits on 1 % p. a. in § 28 Abs. 2 — the *Sicherheitsabschlag* quantified; § 27 Abs. 1 the premium split; § 34 Abs. 4–5 a two-part percentage *Stornoabzug* tapering linearly to nil over the last ten years of the *Aufschubzeit*; § 38 Abs. 1 the reason the fund *Baustein* earns no *Bewertungsreserven* or *Zinsüberschussanteile* before the *Rentenbeginn*.

### S12 — Debeka, "Privatrente" product page
- Publisher: Debeka
- Doc type: insurer product page
- URL: https://www.debeka.de/privatkunden/vorsorgensparen/zukunftalter/privatrente.html
- Retrieved: **yes**, on 2026-08-30 — HTML product page.
- Content: the current-generation Debeka private annuity, and a **split-surplus design**: **"from
  the savings portion, Debeka forms a *Deckungskapital* for the guaranteed benefits; surplus shares
  of the accumulation phase are invested in an internal fund and can enable additional benefits"**,
  and **"fund holdings generally receive no *Überschussbeteiligung* from the earnings of Debeka's
  general *Sicherungsvermögen* before *Rentenbeginn*"**. On tax: **if a lifelong monthly annuity is
  chosen, only part of the payout is taxed — the comparatively low *Ertragsanteil*, depending on age
  at *Rentenbeginn*** [R5]. The insurer **no longer offers the classical annuity product**, the
  offer being the newer variants with a flexible allocation between guaranteed and fund-based
  components — corroborating [R22] from the insurer's own page.

**Retrieval note (2026-08-30).** The split-surplus design is confirmed in the carrier's own summary and matches [S11]'s clause text. **Correction:** the page does **not** carry the insurer's statement that it no longer offers the classical annuity product; that rests on [R22] alone, from a company spokesperson.

### S13 — Allianz Lebensversicherungs-AG, "Vorsorgekonzept KomfortDynamik" / PrivatRente KomfortDynamik
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: insurer product page, plus a distributed *persönlicher Vorschlag* specimen quotation for
  the BasisRente variant hosted by a broker at
  `privat.rh-insuranceservices.com/wp-content/uploads/2025/02/Berechnung-BasisRente-KomfortDyn.pdf`,
  dated by its path to **February 2025**
- URL: https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/
- Retrieved: **yes**, on 2026-08-30 — HTML product page. The broker-hosted *persönlicher
  Vorschlag* specimen was not re-swept and nothing is drawn from it.
- Content: **the successor design that replaced the classic tariff at the market leader.** Premiums
  are **split between the Allianz *Sicherungsvermögen* and the KomfortDynamik *Spezialfonds***; the
  design "combines elements of a classic life insurance with a dynamics part, so-called asset-value
  investments". **Guarantee levels at *Rentenbeginn* of 60 %, 80 % or 90 % of the premiums paid**,
  selectable, 80 % standard. Customers receive **"only modest guarantees"** at inception: retention
  of the premiums paid at the selected level **and a minimum annuity**, provided the contract is
  held to the end of the term — the *garantierter Rentenfaktor* in another guise. **"The
  calculation bases at *Rentenbeginn* … relate to the interest rate and mortality table that the
  company uses at that time for immediately beginning annuities"** — the corroborating statement,
  from a second carrier, that the *aktueller Rentenfaktor* is the carrier's then-current
  immediate-annuity tariff. The **Rentengarantiezeit** "can be set to a minimum" — a
  policyholder-selectable parameter with a floor. Two charge figures were returned by commentary in
  the same result set: an **Abschlussprovision of 1 575 €** on the specimen quotation, and, in the
  BasisRente and RiesterRente variants, **total costs relative to the capital formed of at most
  0,95 € per 100 €**. Both come from third-party analyses rather than an Allianz tariff sheet, are
  `[unverified]` as market-representative levels, and are the **only** charge figures the corpus
  **Status 2026-08-30: worse, not better.** [R23] is paywalled and [S13] does not carry either figure, so neither is established by any retrieved document. The tag stands and is now the stronger for it.
  produced.

**Retrieval note (2026-08-30). Two corrections.** The page states the guarantee ladder verbatim — *"neben einem Garantieniveau von 80 % der eingezahlten Beiträge auch ein Garantieniveau von 60 % … oder 90 %"* — but it does **not** contain the operational definition of the *aktueller Rentenfaktor* attributed to it, which is re-sourced to [S9] § 1 Abs. 1 and [S14] § 2 Abs. 5; and it does **not** contain either charge figure. The 1 575 € *Abschlussprovision* and the 0,95 € per 100 € ceiling rest on the [R23] analyst cluster, which is paywalled, so neither survives retrieval and both stay `[unverified]`.

### S14 — Mecklenburgische Versicherungsgruppe, "Vertragsinformationen für die Private Rentenversicherung mit flexiblem …" (Rente flex)
- Publisher: Mecklenburgische Lebensversicherungs-AG
- Doc type: *Vertragsinformationen* for the "Rente flex" private annuity
- URL: https://www.mecklenburgische.de/pdfs/produkte/vertragsinformationen/Vertragsinformationen-zu-Leben/rente-flex_vertragsinformationen.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 27 pp., **Version 07.2025**, condition set
  *B Privat-Rente Flex* plus riders, glossary, tax notes and a *Kostenverzeichnis*.
- Content: the title is truncated after "mit flexiblem", so the product's distinguishing feature —
  most plausibly a flexible *Rentenbeginn* — is **not established**. Recorded as a mid-sized-mutual
  data point and as evidence that *Vertragsinformationen* is a second common name for the same
  pre-contractual pack [S4]. No clause content established.

**Retrieval note (2026-08-30).** The truncated title resolves to *"Private Rentenversicherung mit flexiblem **Fondsanteil (Hybrid)**"*, **Version 07.2025**, condition set *B Privat-Rente Flex* — a hybrid, so a variation rather than a classic chassis. It states the *Rentenfaktor* per 10 000 EUR of *Gesamtkapital*, taken from the bases the carrier uses for newly written immediate annuities and re-based whenever those change (§ 2 Abs. 5), with the *garantierte Mindestrente* as a floor (§ 2 Abs. 3) and the guaranteed factor fixed at inception (§ 2 Abs. 6).

### S15 — Konzern Versicherungskammer, "Überschussverteilung 2026"
- Publisher: Konzern Versicherungskammer (the Bavarian public-sector insurance group); the `BL_`
  path prefix indicates the Bayerische Landesbrandversicherung / Bayern-Versicherung life entity
- Doc type: the annual **surplus-declaration document** — the instrument by which a German life
  insurer publishes its declared *Überschussanteilsätze* for a calendar year
- URL: https://www.konzern-versicherungskammer.de/dam/jcr:acf4c857-3b53-4521-a108-d1fb9b1cec67/BL_Ueberschussbeteiligung_2026.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 145 pp., *Überschussverteilung 2026*, publishing
  entity **Bayern-Versicherung Lebensversicherung AG**.
- Content: establishes the **existence and the current vintage (2026)** of the annual declaration
  document type, which is the primary source class for every surplus rate a model of this product
  needs. **No rate, no percentage and no surplus-component split was established from it** — the
  summary returned only the title. This is gap 4, the largest hole in the file after gap 3: the
  corpus establishes the *machinery* of the *Überschussbeteiligung* thoroughly and its *current
  levels* not at all.

**Retrieval note (2026-08-30). Gap 4 is closed.** 145 pp., publisher confirmed as Bayern-Versicherung Lebensversicherung AG. The document's own convention is that a figure in brackets is the prior year's. Section **3.1 Rentenversicherung**, *laufender Überschussanteil*, tariff generations 2015–2025: *Zinsüberschussanteil* **3 % abzüglich Rechnungszins** before the *Rentenzahlungsbeginn* and **3,35 % abzüglich Rechnungszins** during the *Rentenbezug* for 2026, against 2,25 % and 2,5 % for 2025; generations 2012–2013 at 1,25 % and 1,6 %. Total interest credited is therefore **3,00 %** for 2026. Also: the *hälftige* allotment (*"zur Hälfte dem Vertrag zugeteilt"*), the annuity *Zuteilungszeitpunkte*, no *Risiko- oder Verwaltungskostenüberschussanteil* on this line, and *"Eine Direktgutschrift wird nicht durchgeführt"*.

### S16 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation … Sofort beginnende Rentenversicherung", Fassung 01/2022
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation* for the **immediate** annuity. Document code **521331402 2501**.
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/222202101_sofort-beginnende-rentenversicherung_verbraucherinformationen_2022_01.pdf
- Retrieved: **yes**, on 2026-08-30 — PDF, 25 pp., document code 521331402 2501, **Fassung
  01/2025**, *Direktversicherung nach § 3 Nr. 63 EStG (Schicht 2)*.
- Content: the immediate-annuity sibling of [S4]–[S7] from the same carrier and series. It is in
  this file — despite belonging to delib's `sofortrente` — because [S13] establishes that the
  *aktueller Rentenfaktor* of a deferred contract is taken from the carrier's **then-current
  immediate-annuity tariff**. No clause content established from this edition.

**Retrieval note (2026-08-30). Correction.** The Fassung is **01/2025**, not 01/2022, and the edition is a *Direktversicherung nach § 3 Nr. 63 EStG (Schicht 2)*. Its § 1 Abs. 6 carries the same basis sentence as the deferred packs — DAV 2004R (Aggregattafel), *Rechnungszins* 1,00 % — so at this carrier and vintage the immediate and the deferred tariff run on identical bases.

### S17 — Zurich, "Private Rentenversicherung" product page
- Publisher: Zurich Gruppe Deutschland
- Doc type: insurer product page
- URL: https://www.zurich.de/de-de/pk/altersvorsorge/private-rentenversicherung
- Retrieved: **no** — HTTP 200 with a 212-byte shell and no page body, on 2026-08-30 and on two
  further zurich.de path forms tried once each. Kept as a known reference.
- Content: the retail presentation of the family whose conditions are [S4]–[S7]. **No parameter,
  price point or envelope was established from it.**

**Retrieval note (2026-08-30).** Not retrievable. Nothing is established from it and nothing downstream rests on it.

### S18 — Stuttgarter Lebensversicherung a. G., "Allgemeine Informationen zu einem Altersversorgungssystem"
- Publisher: Stuttgarter Lebensversicherung a. G.
- Doc type: general pre-contractual information on a retirement-provision system
- URL: https://www.stuttgarter.de/documents/209195/221255/Allgemeine_Infos_Altersversorgungssystem_SLV.pdf/2657ea66-2bfa-9cec-04d2-8f72ac9731bd?t=1604038997833
- Retrieved: **yes**, on 2026-08-30 — PDF, 23 pp.
- Content: the URL's `?t=1604038997833` parameter is a millisecond timestamp corresponding to
  **October/November 2020**, which dates the file. No clause content established. Recorded as a
  further carrier and as a second example of the *allgemeine Informationen* document type [S4].

**Retrieval note (2026-08-30).** 23 pp., and it is a ***betriebliche Altersversorgung*** document — chapter 1 is the *"Klassische Rentenversicherung als Direktversicherung nach § 3 Nr. 63 und § 100 EStG"*, for tariffs written before 2021 — so Schicht 2, a boundary marker. It states the *Rentenfaktor* in per-10 000-EUR terms with the classic scope: *"Für den Teil des Deckungskapitals, der das garantierte Kapital übersteigt, garantieren wir eine monatliche Rente je 10.000 € dieses Teils des Deckungskapitals (garantierte Rentenfaktoren)."*

### S19 — DEVK, "Kundeninformation zur Fondsgebundenen Rentenversicherung", 03101/07/2024
- Publisher: DEVK Lebensversicherungsverein a. G.
- Doc type: *Kundeninformation* for a **unit-linked** annuity, document code **03101**, **07/2024**
- URL: https://medien.devk.de/assets/content/download/produkte/altersvorsorge-leben/devk-fondsrente-kundeninfo-03101-2024-07.pdf
- Retrieved: **no** — HTTP 403 at the cited URL on 2026-08-30 and on a direct retry;
  `medien.devk.de` refuses the asset path. The obvious replacement product page answers 404.
  Kept as a known reference; nothing is established from it.
- Content: **out of scope as a product** — it is delib's `fondsgebundene_rentenversicherung` — and
  is recorded solely for the **contrast on the death benefit**: on death before *Rentenbeginn* the
  benefit is **the fund value at the date of death but at least the sum of the premiums paid
  (*Beitragsrückgewähr*)**. That `max(account value, premiums paid)` shape is the unit-linked form
  of what the classic product expresses as `max(Deckungskapital, premiums paid)` or as one or the
  other outright. It is used here as the contrast, **not** as the classic rule; see section 7.

---

**Retrieval note (2026-08-30).** Not retrievable; the death-benefit sentence attributed to it stays `[unverified]`. It no longer has to carry the `max(…)` shape alone: [S9] § 1 Abs. 3 states that shape for a **classic** deferred annuity, so gap 18's "classic analogue unestablished" is withdrawn on other evidence.

## Regulatory and actuarial references

Twenty-four product-specific regulatory and actuarial references. Statutory articles carry the
canonical `gesetze-im-internet.de` URL where several legal-database mirrors returned the article;
where the canonical slug itself was not returned by any search, the URL is recorded as not
established and the mirrors are named instead. Cross-product references that belong to the delib
reference library (VAG, MindZV, LVRG, RechVersV, Solvency II, IFRS 17, Protektor) are **not**
duplicated here; they carry `[REG-R#]` tags downstream.

### R1 — VVG § 169, Rückkaufswert
- Publisher: Bundesministerium der Justiz / juris (Gesetze im Internet)
- URL: https://www.gesetze-im-internet.de/vvg_2008/__169.html
- Retrieved: **yes**, on 2026-08-30 — canonical statutory XML, **Stand: zuletzt geändert durch
  Art. 12 G v. 26.5.2026 I Nr. 156**. The `__169.html` per-section page is a 7 kB frameset with no
  statutory text and is kept only as the human-facing link.
dates the commentary version to **1 January 2016**).
- Content, as reported: for **unit-linked** contracts the *Rückkaufswert* is to be computed
  **according to recognised rules of actuarial mathematics as the *Zeitwert* of the insurance**,
  insofar as the insurer does not guarantee a particular benefit, and **the principles of the
  calculation must be stated in the contract**. **A deduction is permitted only if it is agreed,
  quantified (*beziffert*) and appropriate (*angemessen*)**, and **an agreement of a deduction in
  respect of not-yet-amortised *Abschluss- und Vertriebskosten* is void (*unwirksam*)**. The
  computed value may be reduced by a **contractually agreed and appropriate *Stornoabzug*
  (*Rückkaufsabschlag*)**; the result is the **statutory minimum surrender value**, below which a
  contractually agreed value may not fall. **§ 169 Abs. 6 VVG permits the insurer, in defined
  cases, to reduce surrender values that are to be paid out.** The **five-year spreading of
  *Abschluss- und Vertriebskosten*** that commentary associates with § 169 Abs. 3 was **not**
  returned by any summary and is `[unverified]` at article level; see gap 12.
  **Resolved 2026-08-30: confirmed at article level** — § 169 Abs. 3 Satz 1 carries the five-year spreading verbatim; tag withdrawn.

**Retrieval note (2026-08-30). Gap 12 is closed.** § 169 Abs. 3 Satz 1 contains the five-year spreading at article level: *"bei einer Kündigung des Versicherungsverhältnisses jedoch mindestens der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt; die aufsichtsrechtlichen Regelungen über Höchstzillmersätze bleiben unberührt."* Abs. 5 and Abs. 6 read as reported. **A refinement:** the inference that the *Stornoabzug* must be flat and duration-free does not follow from Abs. 5 — the retrieved wordings show none at all [S8] [S9], a flat 250 EUR [S4] and duration-tapering percentages [S11].

### R2 — VVG § 165, Prämienfreie Versicherung (Beitragsfreistellung)
- Publisher: Bundesministerium der Justiz / juris
- URL: https://www.gesetze-im-internet.de/vvg_2008/__165.html — **returned directly by the search**
- Retrieved: **yes**, on 2026-08-30 — canonical statutory XML, **Stand: Art. 12 G v. 26.5.2026
  I Nr. 156**; the `__165.html` page is a 4 kB frameset.
- Content, as reported:
  - **The policyholder may at any time demand, for the end of the current insurance period, that
    the insurance be converted into a premium-free insurance, provided the agreed minimum
    insurance benefit is reached.**
  - **If that minimum benefit is not reached, the insurer must pay the surrender value
    attributable to the insurance, including profit shares, under § 169.**
  - **The premium-free benefit is calculated according to recognised principles of actuarial
    mathematics, using the calculation basis of the premium calculation, on the basis of the
    surrender value under § 169 paragraphs 3 to 5, and must be stated in the contract for each
    insurance year.**
  - Applied to this product: **the policyholder always has the right to convert a running annuity
    contract into a premium-free annuity contract** — the conversion right is statutory, not a
    tariff concession, and it is exercisable at the end of the then-current insurance period.

**Retrieval note (2026-08-30).** Both branches read at article level. Abs. 2 refers to *"des Rückkaufswertes nach § 169 Abs. 3 bis 5"* — so the Abs. 5 deduction is inside the reference, although [S4] § 10 Abs. 9 and [S8] § 7 Abs. 7 waive it on the paid-up route. **Gap 22 is partly closed:** the *Mindestversicherungsleistung* is contractual and three carrier levels are on the record — 25,00 € a month [S4] [S9], 600,00 € a year for a partial surrender [S8].

### R3 — VVG § 163, Anpassung der Prämie / Bedingungsanpassung
- Publisher: Bundesministerium der Justiz / juris
- URL: https://www.gesetze-im-internet.de/vvg_2008/__163.html (canonical form; the article was
  reached in this session through commentary rather than through a statute mirror)
- Retrieved: **yes**, on 2026-08-30 — canonical statutory XML, **Stand: Art. 12 G v. 26.5.2026
  I Nr. 156**; the `__163.html` page is a 6 kB frameset.
- Content: the summaries establish § 163 VVG as **the operative statutory basis on which a German
  life insurer may today change a guaranteed *Rentenfaktor***, having replaced the contractual
  *Treuhänderklausel* route for new business. The two triggers the commentary attributes to the
  clause family are: **an unexpectedly strong increase in life expectancy, requiring an adjustment
  of the mortality bases**, and **a sustained reduction in capital-market returns, permitting an
  adjustment of the interest basis**. The commentary that carried this is
  `bavprofis.de/news-lesen/rentenfaktor-altersvorsorge-rente.html`, headed "RENTENFAKTOR ENTHÜLLT
  | DIE MACHT DES § 163 VVG", corroborated by [R17]. **The article's own paragraph structure and
its procedural requirements (trustee review, notice) were not established** — see gap 6.

**Retrieval note (2026-08-30). Gap 6 is closed and the entry's heading corrected.** The article is titled ***Prämien- und Leistungsänderung*** and has four *Absätze*. Abs. 1 permits a **premium** re-setting on three cumulative conditions, the third being confirmation by *"ein unabhängiger Treuhänder"*, and excludes it where the original calculation was inadequate and a careful actuary should have seen it. Abs. 2 lets the policyholder demand a benefit reduction instead, and gives the insurer a unilateral reduction power only *"bei einer prämienfreien Versicherung"*. Abs. 3 fixes the effective date; Abs. 4 drops the trustee where supervisory approval is required. **Refinement:** the trustee is *inside* the statutory route, so § 163 did not replace a trustee mechanism — it supplies the conditions the contractual clause must meet.

### R4 — VVG § 153, Überschussbeteiligung, and § 153 Abs. 3, Beteiligung an den Bewertungsreserven
- Publisher: Bundesministerium der Justiz / juris
- URL: https://www.gesetze-im-internet.de/vvg_2008/__153.html (canonical form)
- Retrieved: **yes**, on 2026-08-30 — canonical statutory XML, **Stand: Art. 12 G v. 26.5.2026
  I Nr. 156**; the `__153.html` page is a 5 kB frameset.
- Content: the Zurich consumer-information summary [S4] [S5] states that **§ 153 Absatz 3 VVG
  currently provides for an equal (*hälftige*) participation in the *Bewertungsreserven***, and
  that the participation must be given effect "according to the legal and supervisory provisions".
  The same summary establishes two product-specific consequences: **the transition to annuity
  payment is a key point for the *Bewertungsreserven* participation**, and **policyholders also
  participate in the *Bewertungsreserven* during the annuity payment period**. The remainder of §
  153 — the *verursachungsorientiertes Verfahren* (cause-oriented allocation), the opt-out in §
  153 Abs. 1, and the LVRG 2014 *Sicherungsbedarf* restriction on the *Bewertungsreserven* share —
  was **not** established by any summary in this session and is `[unverified]` *(withdrawn 2026-08-30)* here; it belongs to
  **Resolved 2026-08-30: confirmed at article level** — § 153 Abs. 1 carries the all-or-nothing opt-out, Abs. 2 the *verursachungsorientiertes Verfahren*, Abs. 3 Satz 3 the *Sicherungsbedarf* reservation. Tag withdrawn; Abs. 4, the annuity-specific crystallisation point, was not in the summary at all.
  the delib cross-product reference library.

**Retrieval note (2026-08-30).** Read at article level. Abs. 1 gives the all-or-nothing opt-out; Abs. 2 the *verursachungsorientiertes Verfahren*; Abs. 3 Satz 2 the *hälftige* allotment at contract termination; Abs. 3 Satz 3 the supervisory reservation. **The decisive new sentence is Abs. 4**: *"Bei Rentenversicherungen ist die Beendigung der Ansparphase der nach Absatz 3 Satz 2 maßgebliche Zeitpunkt."* The crystallisation at the *Rentenbeginn* is therefore a **statutory rule specific to annuities**, not a carrier's paraphrase. Continued participation during the payout phase is **not** in § 153; it is the carriers' own promise [S4] [S9] [S15].

### R5 — EStG § 22, Ertragsanteilsbesteuerung der Leibrente
- Publisher: Bundesministerium der Justiz / juris
- URL: https://www.gesetze-im-internet.de/estg/__22.html — **returned directly by the search**
- Retrieved: **yes**, on 2026-08-30 — canonical statutory XML, **Stand: zuletzt geändert durch
  Art. 7 G v. 29.6.2026 I Nr. 197**.
- Content, as reported:
  - Payments from private annuity contracts, and from life contracts converted into a classic
    monthly *Leibrente*, are taxed on the ***Ertragsanteil*** basis.
  - **Only the "Ertrag des Rentenrechts"** — the interest component contained in the annuity from
    the beginning of the payout phase — **is subject to tax**.
  - **The *Ertragsanteil* is determined by the annuitant's age at *Rentenbeginn*.** The earlier
    the annuity begins, the longer the remaining life expectancy and hence the annuity's duration,
    and **the higher the taxable *Ertragsanteil***.
  - **For an annuity commencing at age 65 the *Ertragsanteil* is 18 % of the annuity.** This is
    the only value on the statutory table that any summary in this session returned; every other
    age's percentage is `[unverified]` *(withdrawn 2026-08-30)* here (gap 8).
  **Resolved 2026-08-30: confirmed and extended** — the whole § 22 table is read; 18 % is the value at 65 *or 66*. Tag withdrawn.
  - The precise statutory address usually given for the table — § 22 Nr. 1 Satz 3 Buchst. a
    Doppelbuchst. bb EStG — was **not** confirmed by any summary and is `[unverified]` *(withdrawn 2026-08-30)*.
  **Resolved 2026-08-30: confirmed** — the address is § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb EStG, in the statute and in [S4]'s tax notes. Tag withdrawn.

**Retrieval note (2026-08-30). Gap 8 is closed, and so is the address.** The provision is **§ 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb EStG**, the form [S4]'s tax notes use. Satz 4 supplies the whole table, read off the age completed at the start of the annuity: 22 % at 60–61, 21 % at 62, 20 % at 63, 19 % at 64, **18 % at 65–66**, 17 % at 67, 16 % at 68, 15 % at 69–70, 14 % at 71, down to 1 % from 97. The Schicht-1 limb (Doppelbuchst. aa) is a different table keyed to the **year** of *Rentenbeginn*, 84,0 % for 2026 rising to 100,0 % in 2058.

### R6 — EStG § 20 Abs. 1 Nr. 6, taxation of a Kapitalabfindung (the 12/62 rule and the Halbeinkünfteverfahren)
- Publisher: Bundesministerium der Justiz / juris
- URL: https://www.gesetze-im-internet.de/estg/__20.html (canonical form; reached in this session
  through tax commentary rather than a statute mirror)
- Retrieved: **yes**, on 2026-08-30 — canonical statutory XML, **Stand: Art. 7 G v. 29.6.2026
  I Nr. 197**, together with § 52 Abs. 28 EStG for the transitional rules.
- Content, as reported, and corroborated across five independent commentaries — IWW's *AStW*
  (`iww.de/astw/einkommensteuer/20-estg-rentenzahlungen-aus-einem-vor-dem-112005-abgeschlossenen-beguenstigten-versicherungsvertrag-mit-kapitalwahlrecht-f141638`),
  LV 1871 [R24], Finanzküche, GN Finanzpartner and Finanztip [R20]: **annuity contracts with a
  *Kapitalwahlrecht* against ongoing premium payments fall under § 20 EStG if the capital option
  cannot be exercised before 12 years from contract conclusion**; **the "12/62 rule" — at least
  12 years of contract duration and payment after completion of the 62nd year of life**; **where
  the rule is met only half of the gain (*Ertrag*) is taxable — the *Halbeinkünfteverfahren* — and
  it applies only to lump-sum payments and to multiple capital withdrawals on a payout plan, not
  to monthly annuity payments**; and **for contracts concluded before 1 January 2005 the
  half-income treatment of the lump sum is retained, while annuity payments continue uniformly to
  be taxed on the *Ertragsanteil* basis** [R5]. The *Mindesttodesfallschutz* condition that
  § 20 Abs. 1 Nr. 6 imposes on endowment contracts was not returned by any summary and is
  `[unverified]` here; it belongs to the delib `kapitallebensversicherung` file.
  **Resolved 2026-08-30: confirmed at article level** — § 20 Abs. 1 Nr. 6 Satz 6 sets it out for a
  *Kapitallebensversicherungsvertrag*: the death benefit must reach 50 % of the premiums payable over
  the whole term, and must exceed the *Deckungskapital* or *Zeitwert* by at least 10 % no later than
  five years after conclusion, that percentage being allowed to fall in equal annual steps to nil.
  Tag withdrawn; the condition is by its terms an endowment test and does not reach this product.

**Retrieval note (2026-08-30). The rule's statutory home is more complicated than "12/62".** § 20 Abs. 1 Nr. 6 Satz 2 as enacted reads *"nach Vollendung des **60.** Lebensjahres"*; the 62 comes from **§ 52 Abs. 28 Satz 7 EStG**, *"für Vertragsabschlüsse nach dem 31. Dezember 2011"*. Satz 1 excludes the annuity from the charge — *"soweit nicht die lebenslange Rentenzahlung gewählt und erbracht wird"*. The **pre-2005 cohort rule** is confirmed at § 52 Abs. 28 Satz 5, which keeps the 31 December 2004 version in force for those contracts *"auch in allen offenen Fällen"*; that version's own conditions are incorporated by reference to a repealed text and stay `[unverified]`.

### R7 — Deckungsrückstellungsverordnung (DeckRV), § 2 — Höchstrechnungszins
- Publisher: Bundesministerium der Justiz / juris (instrument); Bundesministerium der Finanzen
  (amendment)
- URL: **not established.** No search result in this session returned a `gesetze-im-internet.de`
  address for the DeckRV, and no URL was guessed. The instrument is established instead from the
  four news and trade sources [R8] [R9] [R10] [R11].
- Retrieved: **yes**, on 2026-08-30 — canonical statutory XML of the DeckRV, §§ 2 and 4,
  **Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250**. **The URL is now established**:
  https://www.gesetze-im-internet.de/deckrv_2016/__2.html .
- Content, corroborated across five independent sources:
  - The *Höchstrechnungszins*, **also commonly called the *Garantiezins***, is **the maximum
    interest rate a life insurer may guarantee to customers on the savings portions of their
    premiums**. It is set in the **Deckungsrückstellungsverordnung**.
  - **With effect from 1 January 2025 it was raised from 0,25 % to 1,00 %** by an amendment of the
    DeckRV, announced in the *Bundesgesetzblatt* on **24 July** [R11] (the year is 2024 by
    construction but was not itself stated in the summary). **This is the first increase since
    1994**; every prior movement was downward.
  - **The increase applies to new contracts with guarantees concluded from the date of the increase
    onwards**; existing contracts keep the *Rechnungszins* they were written on. This is the single
    most important consequence for a model: a German life book is a **layered stack of guarantee
    vintages**, not one rate.
  - Process: the **DAV recommended in November 2023** that the rate be raised to 1 % as of 2025
    [R9]; the **Bundesministerium der Finanzen adopted the recommendation in late April 2024**
    [R9]; the **DAV recommends 1,0 % for 2026 as well** [R8].
  - **The full history of the rate — 4 % to 1994, then 3,25 %, 2,75 %, 2,25 %, 1,75 %, 1,25 %,
    0,90 % and 0,25 % from 2022 — was not established**; every figure in that sequence other than
    the 0,25 % and the 1,00 % is `[unverified]` here. See gap 7.
  **Resolved 2026-08-30: partly** — [R11] gives the endpoints, 4 % in 1994 to 0,25 % in 2022; the intermediate steps are still unconfirmed and the tag stands for them.

**Retrieval note (2026-08-30). The URL is established** — https://www.gesetze-im-internet.de/deckrv_2016/__2.html — and the ordinance read as canonical XML. § 2 Abs. 1 Satz 1 sets the *Höchstzinssatz* at **1 Prozent**. **§ 2 Abs. 2 Satz 1 is stronger than the press restatement this entry rested on**: *"Bei Versicherungsverträgen mit Zinsgarantie gilt der von einem Versicherungsunternehmen zum Zeitpunkt des Vertragsabschlusses verwendete Rechnungszins für die Berechnung der Deckungsrückstellung für die gesamte Laufzeit des Vertrages."* § 4 Abs. 1 Satz 2 carries the *Höchstzillmersatz*: *"Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten"*, with Abs. 4 fixing it for the whole term. Gap 7 stands: the ordinance states only the rate now in force.

### R8 — DAV, "Deutsche Aktuarvereinigung empfiehlt auch für 2026 einen Höchstrechnungszins in Höhe von 1,0 Prozent"
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV), Köln
- URL: https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-empfiehlt-auch-fuer-2026-einen-hoechstrechnungszins-in-hoehe-von-1-prozent/
- Retrieved: **yes**, on 2026-08-30 — HTML.
- Content: the DAV's recommendation that the *Höchstrechnungszins* remain at **1,0 % for 2026**.
  Establishes that the rate applicable to new business at the access date of this file
  (2026-08-29) is **1,0 %**, on the profession's own recommendation, and that the recommendation
  mechanism — DAV recommends, BMF legislates — is the standing process [R9].

**Retrieval note (2026-08-30).** Confirmed verbatim, including a caveat worth keeping: the *Höchstrechnungszins* *"gibt … eine Obergrenze. Er sollte als gesetzlicher Höchstwert dienen, ist aber keine Empfehlung für eine Festlegung durch die Unternehmen."* The release also dates the 2025 rise as *"der erste Anstieg seit über dreißig Jahren"*.

### R9 — DAV, "Deutsche Aktuarvereinigung begrüßt Ministeriumsvorstoß zum Höchstrechnungszins 2025"
- Publisher: DAV
- URL: https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-begruesst-ministeriumsvorstoss-zum-hoechstrechnungszins-2025/
- Retrieved: **yes**, on 2026-08-30 — HTML.
- Content: the DAV's statement on the BMF's move for 2025. Establishes the **November 2023 DAV
  recommendation** and the **late-April 2024 BMF adoption**, i.e. the roughly 14-month lead time
  between the profession's recommendation and the rate taking effect. This lead time is what makes
  the *Rechnungszins* of a tariff a **known-in-advance** parameter for pricing.

**Retrieval note (2026-08-30).** Confirmed: *"Ende November 2023"* for the DAV recommendation and the BMF's announcement that it would follow. **The "late-April 2024" dating of the BMF adoption is not in the release** and stays `[unverified]`; the ordinance itself is dated 19 July 2024 [R7].

### R10 — GDV, media information on the Höchstrechnungszins increase (two releases)
- Publisher: GDV
- URLs:
  - https://www.gdv.de/gdv/medien/medieninformationen/hoechstrechnungszins-erhoehung-ist-eine-angemessene-reaktion-auf-gestiegene-zinsen--176848
  - https://www.gdv.de/gdv/medien/medieninformationen/versicherer-befuerworten-anhebung-des-hoechstrechnungszinses--157548
- Retrieved: **yes**, on 2026-08-30 — both releases, HTML.
- Content: the industry association's statements supporting the increase, headed
  "Höchstrechnungszins-Erhöhung ist eine 'angemessene Reaktion auf gestiegene Zinsen'" and
  "Versicherer befürworten Anhebung des Höchstrechnungszinses". The lower media id (157548) is the
  earlier, pre-legislation release; the higher (176848) follows the decision. Together they
  corroborate [R7] on the increase and its rationale. No figure beyond the 1,0 % was established.

**Retrieval note (2026-08-30). One correction the whole file uses.** Both releases carry the GDV's standing note: *"Der Höchstrechnungszins ist eine Obergrenze für den maximal zulässigen Rechnungszins, den Lebensversicherer bei der Berechnung ihrer Rückstellungen nutzen dürfen. Er ist nicht mit dem Garantiezins gleichzusetzen, den Lebensversicherer individuell auf ihre Produkte gewähren."* The gloss "also commonly called the *Garantiezins*" is withdrawn. Release 176848 also gives the reference rate the increase was judged against — the ten-year euro zero-coupon swap, *"Ende März 2024 betrug er 2,57 Prozent"*.

### R11 — HDI, "Höchstrechnungszins in der Lebensversicherung steigt zum 01.01.2025"
- Publisher: HDI Lebensversicherung AG (press/blog)
- URL: https://pm.hdi.de/blog/h%C3%B6chstrechnungszins-in-der-lebensversicherung-steigt-zum-01.01.2025
- Retrieved: **yes**, on 2026-08-30 — HTML.
- Content: an **insurer's own** statement of the change, and the source of the wording "zum
  01.01.2025 wird der Höchstrechnungszins gemäß Deckungsrückstellungsverordnung von 0,25 % auf
  1,00 % angehoben", together with the *Bundesgesetzblatt* announcement date of **24 July**. Third
  independent corroboration of [R7], and the one that names the instrument.

**Retrieval note (2026-08-30).** Confirmed verbatim, including the 24 July *Bundesgesetzblatt* date, and it adds the endpoints of the decline: *"seit 1994 von vier Prozent kontinuierlich auf 0,25 Prozent in 2022 abgeschmolzen"*. The intermediate steps remain unestablished (gap 7).

### R12 — DAV, "Herleitung der DAV-Sterbetafel 2004 R für Rentenversicherungen" (DAV-Richtlinie)
- Publisher: Deutsche Aktuarvereinigung e. V.
- Doc type: **DAV-Richtlinie** (professional guideline). The file name carries the date
  **2023-06-28**, so the guideline was reissued or last revised on **28 June 2023** — nineteen
  years after the table itself.
- URL: https://aktuar.de/content/PDF/Fachwissen/2023-06-28_DAV-Richtlinie_Herleitung_DAV2004R.pdf
- Retrieved: **partially**, on 2026-08-30 — PDF, 134 pp., cover, preamble and table of contents
  read; the transfer was capped at 3 MB and the extractor's character mapping is defective on this
  file (doubled consonants and some zeros drop out). **Nothing is quoted from it.**
- Content: the profession's derivation document for the table this product is priced on. The
  summaries establish the **component structure** — a **base table of second order**, a **base
  table of first order**, a **mortality trend of second order**, a **mortality trend of first
  order**, and an **age adjustment (*Altersverschiebung*) with a base table** — and that
  **first-order probabilities carry safety margins relative to the second-order ("realistic")
  probabilities, in order to assess the risk prudently**, the **second-order base tables
  representing the best estimate of period mortality in 1999 for insured lives, as
  three-dimensional selection tables**. The 2023 reissue date is significant on its own:
  DAV 2004 R was still the profession's maintained annuity basis **twenty years after its base
  year** — the fact behind the longevity trigger of the § 163 VVG adjustment right [R3].

**Retrieval note (2026-08-30).** Cover confirmed: *Fachgrundsatz der Deutschen Aktuarvereinigung e. V., "Herleitung der DAV-Sterbetafel 2004 R für Rentenversicherungen", Richtlinie, Köln, 28. Juni 2023*, 134 pp. The table of contents confirms the component structure the proxy imitates — *Periodentafeln und Generationentafeln*, *Basistafeln*, *Sterblichkeitstrend*, *Altersverschiebung als Näherungsverfahren*, and §§ 4.1–4.2 on the second-order trend, its damping and the loadings that make the first-order basis.

### R13 — DAV, "DAV 2004 R: Stand 22.02.2005"
- Publisher: DAV
- Doc type: the table document itself. The title line returned reads **"- 1 - DAV 2004 R: Stand
  22.02.2005"**; the file name carries **2005-09-14**, so the document is **dated 22 February 2005
  and published (or re-posted) on 14 September 2005**.
- URL: https://aktuar.de/content/PDF/Fachwissen/2005-09-14-DAV_2004_R.pdf
- Retrieved: **partially**, on 2026-08-30 — PDF, 134 pp., header, contents and §§ 1.2 and 4.2
  read, under the same cap and the same defective mapping as [R12]. **Nothing is quoted from it.**
  Confirmed distinct from [R12]: this is the 2005 derivation by the *DAV-Unterarbeitsgruppe
  Rentnersterblichkeit*, [R12] the 2023 *Richtlinie*.
- Content: **DAV 2004 R is a *Generationentafel* used for annuity insurance calculations in
  Germany**; generation tables **contain mortality by birth cohort, including the expected future
  change in mortality** — the improvement is built into the table rather than applied on top of it.
  **It was intended for new business from 2005 onwards and has been in use since June 2004.** The
  numeric content is **not** in this file: the DAV tables are the property of the Deutsche
  Aktuarvereinigung, are not public, and are **not redistributed by delib**.

**Retrieval note (2026-08-30).** Header confirmed as *"DAV 2004 R: Stand 22.02.2005"*, authored by the *DAV-Unterarbeitsgruppe Rentnersterblichkeit*, 134 pp., and distinct from [R12]. § 1.2 rejects period tables for annuity pricing and defines a generation table as carrying mortality per birth cohort **including the expected future change** — the fact behind `mort_rate_guar(t)` depending on `calendar_year(t)`. § 4.2 quantifies the first-order margins: a model-risk loading equivalent to dropping the trend damping, and an additive margin on the annual improvements calibrated to raise the *Deckungsrückstellung* by about 2 % on the working portfolio.

### R14 — Contemporaneous expositions of DAV 2004 R (DGVFM, Gen Re, qx-Club)
- Publishers: Deutsche Gesellschaft für Versicherungs- und Finanzmathematik, in *Blätter der
  DGVFM* (hosted by Springer); General Reinsurance ("A Berkshire Hathaway Company"), presented to
  the Aktuarvereinigung Österreichs on **27 October 2004**; qx-Club Berlin, **16 August 2004**;
  qx-Club (Helmert), **14 September 2004**
- URLs:
  - https://link.springer.com/article/10.1007/BF02808312
  - https://www.avoe.at/archiv/nachlese-20041027.pdf
  - http://www.qx-club-berlin.de/material/pdf/20040816-qx-Club-Sterbetafel-DAV2004R.pdf
  - https://www.qx-club.de/.cm4all/uproc.php/0/Vortr%C3%A4ge/vortrag_helmert_14092004.pdf?_=173ca294dfb&cdp=a
- Retrieved: **two of four**, on 2026-08-30 — the Gen Re / AVÖ deck (PDF, 93 slides, Wien,
  27. Oktober 2004, Esther U. Schütz) and the Helmert deck (PDF, 41 slides, qx-Club **Köln**,
  September 2004, *DAV2004R und R-Bx*). The Springer article answers 200 with a bot-challenge page
  and no abstract; the qx-Club Berlin PDF fails TLS host verification.
- Content: the peer-reviewed publication of the derivation, plus three practitioner accounts from
  **August to October 2004** — between the table's June 2004 first use and its 2005 general
  application [R13] — which date the market's adoption. The Helmert presentation is titled
  **"DAV 2004 R und RBx"**, RBx being the *Rentenbestandstafel* for the **existing annuity book**
  as against new business: the only evidence in the corpus that DAV 2004 R has a **companion
  in-force table**. Slide and abstract content were not established.

**Retrieval note (2026-08-30). Two corrections.** The Helmert presentation was given to the qx-Club **Köln**, not Berlin, and the companion in-force table is written **R-Bx**. The Gen Re / AVÖ deck adds a figure worth having: the industry-wide reserve strengthening for the 2004 financial year was **about 4 bn euro**, and the table was adopted as a DAV *Fachgrundsatz* by an accelerated procedure so as to bite on the 2004 balance sheet.

### R15 — Wikipedia (German), "Sterbetafel"
- Publisher: Wikimedia Foundation
- URL: https://de.wikipedia.org/wiki/Sterbetafel
- Retrieved: **yes**, on 2026-08-30 — HTML.
- Content: the general-encyclopaedia definition corroborating the generational characterisation of
  DAV 2004 R [R13]: **generation tables contain mortality per birth cohort including the expected
  future change in mortality**. A corroborating secondary source only; nothing in this file rests
  on it alone.

**Retrieval note (2026-08-30).** Confirmed: *"Generationensterbetafel … bei der die Sterblichkeit nicht nur vom Alter … sondern zusätzlich vom Geburtsjahrgang abhängt … Generationentafeln liegen daher der Kalkulation von Rentenversicherungen zugrunde."* It also distinguishes a *Kohortensterbetafel* — observed extinction, unusable for pricing — from the projected object.

### R16 — Finanztip, "Urteil zum Rentenfaktor: Rentenkürzung verhindern"
- Publisher: Finanztip Verbraucherinformation gemeinnützige GmbH
- URL: https://www.finanztip.de/private-rentenversicherung/rentenfaktor/
- Retrieved: **yes**, on 2026-08-30 — HTML.
- Content: the consumer organisation's account of the *Rentenfaktor* and of the litigation over
  its reduction; with [R17] and [R18] it establishes the *Treuhänderklausel* story of section 8. A
  companion consumer-press item in the same result set
  (`gegen-hartz.de/news/rente-nachtraegliche-absenkung-des-rentenfaktors-kann-rechtswidrig-sein-urteil`)
  reports that **a subsequent reduction of the *Rentenfaktor* can be unlawful**.

**Retrieval note (2026-08-30). Gap 10 is closed, and a decision new to this file appears.** The article gives both authorities: *"Die Absenkung des Rentenfaktors in Verträgen der Allianz ist nach einem Urteil des Bundesgerichtshof nicht rechtens (BGH, 10.12.2025, Az. IV ZR 34/25). Gegen die Zurich Versicherung gab es ebenfalls bereits eine Entscheidung (LG Köln, 08.02.2023, Az. 26 O 12/22)."* The BGH decision post-dates this file's drafting research.

### R17 — versicherungenmitkopf.de, pages on the Treuhänderklausel, the Rentenfaktor, the Rentengarantiezeit and the Ertragsanteil
- Publisher: versicherungenmitkopf.de (independent broker's consumer pages)
- URLs:
  - https://www.versicherungenmitkopf.de/treuhaenderklausel-rentenversicherung
  - https://www.versicherungenmitkopf.de/rentenversicherung/rentenfaktor
  - https://www.versicherungenmitkopf.de/rente/rentengarantiezeit-rentenversicherung-riester-und-co
  - https://www.versicherungenmitkopf.de/ertragsanteilsbesteuerung
  - https://www.versicherungenmitkopf.de/rentenversicherung/besteuerung-private-rentenversicherung-wie-viel-bleibt-uebrig
- Retrieved: **yes** for the *Treuhänderklausel* page, on 2026-08-30 — HTML. The four sibling
  paths were not re-swept.
- Content: the densest secondary account in the corpus, and the source of the *Treuhänderklausel*
  narrative. **Insurers could previously change guaranteed *Rentenfaktoren* on the basis of a
  *Treuhänderklausel* contained in the insurance conditions, with the approval of an independent
  external *Treuhänder* (trustee)**; **that clause is now used only in older contracts, and today
  the guaranteed *Rentenfaktor* can be changed only on the basis of § 163 VVG** [R3]. **The clause
  allows the insurer to change essential contract components such as the *Rentenfaktor* if economic
  conditions deteriorate permanently and unexpectedly**, subject to the trustee's review and
  approval, on **two explicit triggers**: an **unexpectedly strong increase in life expectancy**
  (requiring adjustment of the mortality tables) and a **sustainable reduction in capital-market
  returns** (permitting adjustment of the interest rate). **The Landgericht Köln clarified that the
  low-interest phase is not sufficient ground for such an adjustment, because it must be treated as
  entrepreneurial risk that cannot be passed on to policyholders** — **the case reference, decision
  date and party names were not established** (gap 10). It is also the source, jointly with [R24],
  for the *Rentengarantiezeit* material in section 9 and, jointly with [R5] [R24], for the tax
  material in section 15.

**Retrieval note (2026-08-30). Gap 10 is closed here too**: *"das Landgericht Köln [hat] aber bereits im Februar 2023 geurteilt, dass schwankende Zinsen zum unternehmerischen Risiko des Versicherers gehören … (Az. 26 O 12/22)"*. The page also carries a **specimen clause**, attributed to Allianz *E 202 von Juni 2006*, naming both triggers and expressing the remedy as a reduction of *"die monatliche Rente für je 10.000 € Policenwert"*, and it sets out three conditions matching § 163 Abs. 1 Nr. 1–3 VVG point for point.

### R18 — Versicherungswirtschaft-heute, "Treuhänderklausel: Allianz glaubt nicht, dass Kunden einer Anpassung des Rentenfaktors erfolgreich widersprechen können" (4 February 2021)
- Publisher: Versicherungswirtschaft-heute (trade press)
- URL: https://versicherungswirtschaft-heute.de/unternehmen-und-management/2021-02-04/treuhaenderklausel-allianz-glaubt-nicht-dass-kunden-einer-anpassung-des-rentenfaktors-erfolgreich-widersprechen-koennen/
- Retrieved: **yes**, on 2026-08-30 — HTML, dated 4. Februar 2021 on the page.
- Content: dated **4 February 2021** by its own URL path. Establishes that the *Treuhänderklausel*
  question was a **live commercial dispute at the market leader in 2021** — not a historical
  curiosity, but a mechanic carriers were actively defending inside the window in which the
  current in-force book was written. Body content beyond the headline was not established.

**Retrieval note (2026-08-30).** The body, previously unestablished, gives the scale: *"Die Allianz kürzt unter Nutzung der Treuhänderklausel die Rentenfaktoren in bestehenden Verträgen. Betroffen sind rund 750.000 Versicherte … Schon in den Jahren 2005 und 2017 hatte die Allianz von der Treuhänderklausel Gebrauch gemacht."*

### R19 — Franke und Bornberg, "Was bedeutet der Rentenfaktor und wie hoch ist er?" and "Altersvorsorge: Überschüsse im Rentenbezug Teil 1 — Die Qual der Wahl"
- Publisher: Franke und Bornberg GmbH (independent product-rating house)
- URLs:
  - https://www.franke-bornberg.de/de/blog/was-bedeutet-rentenfaktor-wie-hoch-2021-2022
  - https://www.franke-bornberg.de/blog/altersvorsorge-ueberschuesse-im-rentenbezug-teil-1-die-qual-der-wahl
- Retrieved: **the first, yes**, on 2026-08-30 — HTML. The second answers **HTTP 404** on the
  cited path and on the `/de/blog/…` form the live site uses; no replacement was found.
- Content: the rating house's treatment of the *Rentenfaktor* and of **surplus use in the payout
  phase** — the professional source behind section 9's three-system taxonomy. The first URL's slug
  dates that analysis to the **2021/2022** window; the second is explicitly "Teil 1" of a series.
  **No *Rentenfaktor* level, range or table was returned by the summary** — the very question the
  first title asks was not answered by anything the search returned. This is gap 3, the largest
  quantitative hole in the file.

**Retrieval note (2026-08-30). Gap 3 is contradicted by the very article the gap was written about.** Franke und Bornberg compare the *aktueller Rentenfaktor* across carriers: the average fell from **29,09 €** in 2021 to **25,97 €** in 2022, a drop of 3,12 € or 10,73 %; the highest was Condor at **26,61 €**, the lowest Bayerische / Pangaea Life at **20,43 €**. The article also sets out the three-way *aktuell* / *garantiert* / *hart garantiert* distinction. The second URL answers **HTTP 404**, so the payout-phase surplus material is re-sourced to [R20], [S4] § 3 Abs. 7 and [S9] § 2 Abs. 5 c).

### R20 — Finanztip, "Überschussbeteiligung Lebensversicherung: Arten & Höhe" and "Steuer auf Lebensversicherung"
- Publisher: Finanztip Verbraucherinformation gemeinnützige GmbH
- URLs:
  - https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/
  - https://www.finanztip.de/lebensversicherung-versteuern/
- Retrieved: **yes**, on 2026-08-30 — both articles, HTML.
- Content: the consumer organisation's account of surplus participation and of life-insurance
  taxation. Source, jointly with [R19] [R21] [R24], of the **three payout-phase surplus systems**
  (*konstant*, *teildynamisch*, *volldynamisch*) recorded in section 9, including the observation
  that **under the constant system the annuity can still fall, because if the insurer earns less
  than expected the surplus-financed part is reduced**. Also a corroborating source for the 12/62
  rule [R6].

**Retrieval note (2026-08-30).** Confirmed, and the load-bearing sentence exactly: *"In der Praxis kann Deine Rente aber durchaus schwanken. Denn wenn der Anbieter weniger verdient als erwartet, sinkt Deine Rente. Die Summe, die anfänglich festgelegt wird, ist nicht garantiert. Daher ist der Begriff „konstante Rente" etwas irreführend."* [S4] § 3 Abs. 7 says the same thing contractually: the RfB-financed part is promised *"jeweils nur für ein Versicherungsjahr"*.

### R21 — GDV / dieversicherer.de, "Private Rentenversicherung: Auszahlmöglichkeiten"
- Publisher: GDV, under its consumer brand *Die Versicherer*
- URL: https://www.dieversicherer.de/versicherer/altersvorsorge/news/auszahlung-private-rentenversicherung-141750
- Retrieved: **yes**, on 2026-08-30 — HTML.
- Content: **the industry association's own consumer account of the payout options** of a private
  annuity — the closest thing in the corpus to an authoritative statement of the
  *Kapitalwahlrecht*-versus-annuity choice, and part of the result set that established the three
  payout-phase surplus systems. **The notice period for exercising the *Kapitalwahlrecht* was not
  established from it** — gap 11.

**Retrieval note (2026-08-30).** The article is about the choice **between annuity models**, not the *Kapitalwahlrecht*: *"Dynamisch, teildynamisch oder flexibel? … haben Versicherte oft die Wahl zwischen verschiedenen Rentenmodellen."* It supplies *flexibel* as a third name for the constant model, which [S8] § 2 also uses. **Gap 11 closes elsewhere**: notice periods are in [S4] § 2 Abs. 2–3 (three years, or twelve years / five months), [S8] § 1 Abs. 2 (twelve years) and [S14] § 2 Abs. 7 (two months).

### R22 — Versicherungsbote, "Debeka stellt klassische Rentenversicherung ein"
- Publisher: Versicherungsbote Verlag (trade press)
- URL: https://www.versicherungsbote.de/id/4842718/Debeka-Rentenversicherung-Garantiezins/
- Retrieved: **yes**, on 2026-08-30 — HTML.
- Content: **the market-structure fact this whole file has to be read against.** **Debeka
  Lebensversicherung will no longer sell classic annuity insurance**, confirmed by a company
  spokesperson. **From 1 July 2016 Debeka introduced a new private-provision portfolio with five
  tariff variants under the name "Chance"**; in the safest variant **0,5 % interest is
  guaranteed**, and the riskiest variant is **effectively a fund policy with no guarantees**.
  **The decision was part of a broader industry trend: Allianz, Zurich and Generali had already
  stopped distributing classic annuity insurance before it.** The 0,5 % guarantee is a rare hard
  figure and sits **below** the *Höchstrechnungszins* then in force — a deliberately de-risked
  guarantee. A companion item in the same result set,
  `versicherungsbote.de/id/4949977/…/Lebensversicherung-Die-Marktfuehrer-im-Solvenzcheck-Teil-2/`,
  characterises the **Debeka group as "klassisches Garantiegeschäft"** in a solvency review, which
  is what makes its withdrawal from this product significant.

**Retrieval note (2026-08-30).** Confirmed in detail, including the spokesperson, the 1 July 2016 date, the five *Chance* variants and the 0,5 % guarantee *"nach Abzug von Kosten und Risikobeiträgen"*. **One refinement:** of Allianz the article says only that it *"wolle … nur noch dann derartige Produkte anbieten, wenn dies ausdrücklich vom Kunden gewünscht werde"* — withdrawal from active distribution, not from sale. Read with [S4]'s Fassung 01/2026 this narrows gap 9: the classic chassis left the front of the shelf and stayed available.

### R23 — Versicherungsjournal, "Allianz 'KomfortDynamik': Noch immer eine Rentenversicherung?"
- Publisher: Versicherungsjournal Verlag (trade press)
- URL: https://www.versicherungsjournal.de/versicherungen-und-finanzen/allianz-komfortdynamik-noch-immer-eine-rentenversicherung-123163.php
- Retrieved: **no** — HTTP 200 but the body is a **paywall**: *"Dieser Artikel ist nur für
  Premium-Abonnenten des VersicherungsJournals frei zugänglich."* Public are the headline, the
  byline (a guest contribution by the broker Philip Wenzel) and the date **17.8.2015**.
- Content: the trade press's framing of the successor design — the headline itself asks whether
  the replacement is still an annuity contract in the classic sense. Corroborates [S13] on the
  KomfortDynamik construction and on the **60 / 80 / 90 % guarantee ladder**. Companion analyses
  in the same result set are
  `levelv-finanz.de/allianz-privatrente-komfortdynamik-im-test-finanzmathematische-analyse/`,
  `bsc-gmbh.com/blog/komfort-dynamik-der-allianz/`,
  `vorsorgekampagne.de/test-allianz-rentenversicherung-komfortdynamik/`,
  `hauke-simonsen.de/allianz-komfortdynamik-lohnt-sich-diese-rentenversicherung/` and
  `expertenmarkt.de/magazin/lohnt-sich-allianz-komfort-dynamik-was-die-betriebliche-altersvorsorge-wirklich-bringt`;
  the two Allianz charge figures recorded under [S13] come from that cluster and are
  `[unverified]` as market-representative levels.
  **Status 2026-08-30:** unchanged — see the note at [S13] and gap 14. Neither figure survives retrieval.

**Retrieval note (2026-08-30). Not retrievable — paywalled.** Public are the headline, the byline and the date 17.8.2015. **Neither charge figure nor the 60/80/90 ladder can be attributed to it**; the ladder is re-sourced to [S13], the carrier's own page, and the two charge figures are established by **no** retrieved document in this corpus.

### R24 — Consumer and comparison-portal cluster on the Rentenfaktor, the Rentengarantiezeit, the Überschussbeteiligung and the death benefit
- Publishers: LV 1871; NÜRNBERGER; Verivox; Gabler *Versicherungslexikon* and Gabler
  *Wirtschaftslexikon*; Wikipedia (German); Deutsche Rentenversicherung; fragfina.de;
  gn-finanzpartner.de; Finanzküche; Compeon; versicherung-vergleiche.de; Pensionskasse der
  Genossenschaftsorganisation; financedoor.de; prolife-gmbh.de; Volksbanken Raiffeisenbanken
  (vr.de); biac-vorsorgespezialist.de; R+V; lifefinance.de; vergleich-sofortrente.de
- URLs (a representative subset of what the searches returned; cited collectively as [R24] because
  no single member is load-bearing and every fact drawn from the cluster is corroborated by at
  least one other member — the omitted members are further pages of the same publishers):
  - https://www.lv1871.de/fondsgebundene-rentenversicherung/fragen/rentenfaktor/
  - https://www.lv1871.de/private-rentenversicherung/wiki/ertragsanteilsbesteuerung/
  - https://www.lv1871.de/private-rentenversicherung/fragen/todesfall/
  - https://www.lv1871.de/fondsgebundene-rentenversicherung/fragen/beitragsfreistellung/
  - https://www.nuernberger.de/themenwelt/beruf-vorsorge/rentenfaktor/
  - https://www.verivox.de/lebensversicherung/themen/ueberschussbeteiligung/
  - https://wirtschaftslexikon.gabler.de/definition/ueberschussbeteiligung-48786
  - https://de.wikipedia.org/wiki/%C3%9Cberschussbeteiligung
  - https://www.deutsche-rentenversicherung.de/SharedDocs/Glossareintraege/DE/E/ertragsanteil
  - https://www.fragfina.de/ratgeber/ueberschussbeteiligung-nach-rentenbeginn/
  - https://www.fragfina.de/research/rentenfaktor-check-2025/
  - https://www.gn-finanzpartner.de/blog/rentenfaktor-richtig-berechnen
  - https://www.finanzkueche.de/blog/garantierter-rentenfaktor
  - https://www.compeon.de/glossar/rentengarantiezeit/
  - https://www.versicherung-vergleiche.de/private_altersvorsorge/versprechen.htm
  - https://www.financedoor.de/blog/2025/10/der-garantierte-rentenfaktor/
  - https://www.vr.de/privatkunden/produkte/altersvorsorge/private-rentenversicherung/ueberschussbeteiligung.html
  - https://www.ruv.de/altersvorsorge/was-passiert-mit-versicherungen-im-todesfall
- Retrieved: **yes** for the six representative members (lv1871, nuernberger, Gabler, fragfina,
  Finanzküche, Compeon), on 2026-08-30 — HTML. The rest of the cluster was not re-swept.
- Content: the source of the *definitional* material in sections 5, 6, 7, 8, 9 and 15 — the
  *Rentenfaktor* arithmetic and the guaranteed/current distinction; the *Zinsüberschuss*
  hurdle-rate definition; the *verzinsliche Ansammlung* and *Bonusrente* mechanics; the surplus
  systems in both phases; the *Rentengarantiezeit* mechanics, durations and cost illustration; the
  three death-benefit forms before *Rentenbeginn*; and the *Ertragsanteil*. One member,
  `financedoor.de/blog/2025/10/der-garantierte-rentenfaktor/`, carries a **2025-10** date in its
  path, placing it inside the current *Höchstrechnungszins* regime; another,
  `fragfina.de/research/rentenfaktor-check-2025/`, is titled a **2025 *Rentenfaktor* check with
  data and analysis** and is the single most likely public source of the market range this file
  could not establish (gap 3).

**Retrieval note (2026-08-30). Gap 3 is closed by this cluster.** fragfina's *Rentenfaktor-Check 2025* publishes, for six deferment terms all to attained age 67, the highest and average current and guaranteed factors: at 40 years 29,47 / 27,27 / 27,31 / 24,33; at 30 years 30,69 / 28,41 / 28,42 / 25,37; at 20 years 32,06 / 29,69 / 29,67 / 26,54; at 15 years 32,81 / 30,40 / 30,36 / 27,18 — with a lowest current factor of 21,41 and a lowest guaranteed of 17,72 at 40 years. The gap between the average current and average guaranteed factor, about 11 % at forty years, is the *Sicherheitsabschlag* measured. The per-10 000-EUR arithmetic is confirmed here (*"Angespartes Kapital / 10.000 x Rentenfaktor = Monatliche Rente"*) and, more usefully, in contracts at [S11] § 52 Abs. 1, [S14] § 2 Abs. 5 and [S18].

## Extracted facts, by mechanic

### 1. Product structure, legal form and the Schicht-3 placing

- The product is a **life insurance contract** under the VVG, on a single life, in which the
  insurer's obligation is **an annuity payable for the annuitant's lifetime beginning at a
  contractually fixed date**, with an accumulation period before it [S1] [S4] [S8] [S9].
- The insurer's own placement is **Schicht 3 — "Private Vorsorge"**: the Zurich scope line is
  "Aufgeschobene Rentenversicherung — **Private Vorsorge (Schicht 3)** und Rückdeckungsversicherung
  (Schicht 2)" [S4]. Schicht 3 is the unsubsidised layer: no § 10 EStG deduction, no *Zulage*, no
  certification under the *Altersvorsorgeverträge-Zertifizierungsgesetz*.
- The boundary is visible in the GDV's own taxonomy: **separate** model conditions exist for the
  *Basisrente* (titled by reference to § 10 Abs. 1 Nr. 2 Buchst. b Doppelbuchst. aa EStG) and for
  *Altersvorsorgeverträge* under the certification act [S3]. This product is the one **without** a
  statutory qualification clause in its title [S1] [S2].
- **The GDV model conditions are non-binding.** "Diese Bedingungen sind unverbindlich" heads the
  set [S2] and the association's index states that use is optional [S3]. German AVB for this
  product are therefore **structurally very similar and textually distinct** — which is why a
  delib composite is the right unit of description and why no single carrier's wording is adopted
  wholesale.
- The German pre-contractual pack is issued under several names — *Verbraucherinformation* [S4]–
  [S7], *Vertragsinformationen* [S14], *Kundeninformation* [S19], *Allgemeine Informationen zu
  einem Altersversorgungssystem* [S18] — and is one object: general information, the AVB, the
  special conditions for options and riders, and the tax notes [S4].
- **The structure of that pack, from [S4], is the template for the delib documents**: (i)
  allgemeine Informationen; (ii) Allgemeine Versicherungsbedingungen; (iii) Besondere Bedingungen
  für die Anpassungsversicherung in der Rentenversicherung (*Dynamik*); (iv) allgemeine
  steuerliche Hinweise; (v) Besondere Bedingungen für die Berufsunfähigkeits-Zusatzversicherung.
- **The survivor's annuity is a rider, not a base benefit**: the GDV publishes it as a separate
  *Hinterbliebenenrenten-Zusatzversicherung* model condition set attaching to the deferred annuity
  [S10]. A reference implementation carries it as a module **off in the base run**. The **BUZ** is
  likewise a rider with its own special conditions inside the same pack [S4], and is delib's
  `berufsunfaehigkeit` product in its standalone form.
- One carrier issues the contract in more than one distribution wrapper — an ordinary edition [S4]
  [S5] [S7] and a *Konsortialversicherung* edition [S6]. Wrapper differences change the parties,
  not the cash flows.

### 2. The accumulation and payout phases, and the Rentenbeginn boundary

- The contract has **two phases separated by the *Rentenbeginn***: the *Aufschubzeit*, over which
  premiums are paid and the *Deckungskapital* accumulates, and the *Rentenbezugsphase*, over which
  the annuity is paid [S1] [S4] [S8] [S11]. **"Eine Aufschubzeit gibt es nur bei aufgeschobenen
  Rentenversicherungen"** — a deferment period exists only in a deferred annuity contract, the
  definitional line separating this product from delib's `sofortrente` [R24].
- The *Rentenbeginn* is **the pivot of the whole contract**, and three distinct things happen at
  it, all of which a model must sequence explicitly: (1) the accumulated value is struck, including
  surplus and *Bewertungsreserven* [S9]; (2) the *Rentenfaktor* to be applied is determined, by
  comparing the guaranteed factor with the then-current one [S4] [S13]; (3) the policyholder's
  *Kapitalwahlrecht* election, if any, takes effect [S12] [R21].
- **The transition to annuity payment is explicitly identified as a key point for the
  *Bewertungsreserven* participation** [S4]: the share is not a smooth accrual, it is crystallised
  at the boundary.
- **The participation in *Bewertungsreserven* does not stop at the *Rentenbeginn*.** Policyholders
  **also participate during the annuity payment period**, in accordance with the applicable VVG
  and supervisory provisions [S4] [R4]. A model that treats the payout phase as a closed,
  non-participating run-off is therefore wrong for this product.

### 3. Premium

- Two premium forms exist: a **laufender Beitrag** (level recurring premium over the
  *Aufschubzeit*) and an **Einmalbeitrag** (single premium); the recurring form is the one the
  accumulation mechanics in [S11] describe. **No search result established the market split, the
  minimum or maximum premium at any carrier, or the permitted range of the *Aufschubdauer*** — see
  gap 13.
- The premium is decomposed, in the insurer's own words, into the portion **required for risk and
  expense cover** and the remainder, the ***Sparbeitrag***, which is what accumulates: the
  *Deckungskapital* is "the sum of the contributions accumulated at the *Rechnungszins*, **insofar
  as these are not intended for risk and cost coverage**" [S11] — one sentence fixing the premium
  decomposition and the reserve recursion together. Debeka states the same split in the other
  direction: **"from the savings portion, Debeka forms a *Deckungskapital* for the guaranteed
  benefits"** [S12].
- **Payment frequency and the *Ratenzahlungszuschlag*.** German life tariffs load the annual
  premium for monthly, quarterly or half-yearly payment; **no loading percentage was established at
  any carrier** (gap 14), so any figure a delib document uses will be `[std]`.
- ***Zuzahlung*** — an ad-hoc additional single premium into a running contract — is a standard
  German option, but **nothing in the eighteen search results named it**; it is recorded as a gap,
  not a fact (gap 15).
- ***Dynamik* / *Anpassungsversicherung*** — the automatic annual increase of premium and benefit
  — **is established from a primary document**: the Zurich pack contains ***"Besondere Bedingungen
  für die Anpassungsversicherung in der Rentenversicherung"*** as a named section [S4], so the
  option exists, is documented at clause level, and has its own condition set. **Its parameters —
  the increase percentage, its basis, whether fresh underwriting applies, the number of refusals
  that end the option — were not established** (gap 15).

### 4. The Rechnungszins and the guarantee vintage stack

- The ***Rechnungszins*** is the rate at which the *Sparbeitrag* is guaranteed to accumulate in
  the *Deckungskapital* [S11]. It is capped for new business by the statutory
  ***Höchstrechnungszins***, set in the **Deckungsrückstellungsverordnung** [R7] [R11].
- The *Höchstrechnungszins* is **also commonly called the *Garantiezins*** and is defined as **the
  maximum interest rate a life insurer may guarantee on the savings portions of the premium** [R7]
  [R11].
- **From 1 January 2025 the *Höchstrechnungszins* is 1,00 %**, raised from **0,25 %** by an
  amendment to the DeckRV announced in the *Bundesgesetzblatt* on **24 July** [R7] [R10] [R11].
- **This was the first increase since 1994**; every movement in the intervening thirty years was
  downward [R7] [R11].
- **The DAV recommends 1,0 % for 2026 as well** [R8]. At this file's access date the rate
  applicable to new business is therefore **1,0 %**.
- The mechanism is: **DAV recommends → BMF legislates.** The DAV recommended the 1 % rate in
  **November 2023**; the **Bundesministerium der Finanzen adopted the recommendation in late April
  2024**; it took effect **1 January 2025** [R9]. The roughly fourteen-month lead time makes the
  *Rechnungszins* of a tariff a parameter that is known well before it binds.
- **The increase applies only to new contracts with guarantees concluded from the date of the
  increase onwards** [R7]. Existing contracts keep the rate they were written on. **The modelling
  consequence is decisive: a German life book is a layered stack of guarantee vintages, and the
  *Rechnungszins* is a model-point attribute, not a global assumption.**
- The full historical sequence of the rate is **not established here**; the only two levels any
  search confirmed are **0,25 %** (the immediately preceding rate) and **1,00 %** (from 2025),
  plus the fact that **4 %** applied until the 1994 change is `[unverified]` and comes from the
  **Status 2026-08-30: partly resolved** — [R11] states *"seit 1994 von vier Prozent kontinuierlich auf 0,25 Prozent in 2022 abgeschmolzen"*, so the 4 % starting point is confirmed; the intermediate steps are not.
  bare phrase "first increase since 1994" [R7]. See gap 7.
- **An insurer may, and does, guarantee less than the statutory maximum.** Two independent data
  points establish this and both are hard figures:
  - **CosmosDirekt's *Rentenfaktor* is calculated on "an underlying interest rate (currently 0
    percent p.a.)"** [S8] — a zero interest basis for the conversion guarantee.
  - **Debeka's safest "Chance" variant guarantees 0,5 %** [R22]. Both sit below the
    *Höchstrechnungszins* in force at their vintage. A model must not assume the guaranteed rate
    equals the statutory cap.

### 5. The Aufschubphase: the Deckungskapital recursion

- **The definitional statement, from an insurer:** the *Deckungskapital* is **"the sum of the
  contributions accumulated at the *Rechnungszins*, insofar as these are not intended for risk and
  cost coverage"** [S11].
- Unpacked into the recursion a model implements — and this is a **reading** of [S11], not a
  clause the corpus supplied in this form:

  ```
  Deckungskapital(t) = ( Deckungskapital(t-1) + Sparbeitrag(t) ) x (1 + Rechnungszins)
  Sparbeitrag(t)     = Beitrag(t) - Risikobeitrag(t) - Kostenbeitrag(t)
  ```

  The ordering of premium credit, charge deduction and interest accrual within a period is **not
  established by any source in this corpus** and is a `[std]` decision for the delib
  implementation, stated explicitly in the processing order of `technical-notes.md`.
- **The *Deckungskapital* is the quantity everything else is defined off**: the death benefit in
  one of the two common designs (section 7), the basis of the *Rückkaufswert* (section 12) and of
  the *beitragsfreie Versicherungsleistung* (section 13), and — with surplus and
  *Bewertungsreserven* added — the capital the *Rentenfaktor* applies to (section 8).
- The conversion input is stated cleanly by NÜRNBERGER: **the contract value used for
  annuitisation includes any *Überschussbeteiligung* and *Bewertungsreserven*, subject to a
  minimum guaranteed contract value stated in the general contract data** [S9]. In model terms:

  ```
  Kapital(Rentenbeginn) = max( garantiertes Vertragsguthaben,
                               Deckungskapital + Ueberschussguthaben + Bewertungsreserven )
  ```

- The *Zinsüberschuss* — the interest surplus — arises **when the insurer's investment income
  exceeds the *Rechnungszins***: "when investment income exceeds the calculation rate, the
  insurance company generates surpluses in the form of interest gains" [R24]. This is the direct
  statement that the *Rechnungszins* is the **hurdle rate** of the surplus mechanism, not merely a
  discount rate.

### 6. Überschussbeteiligung in the Aufschubphase

- ***Überschussbeteiligung*** is the **participation of policyholders in the surpluses of the
  insurance undertaking** [R24]. Its magnitude is, in an insurer's own contractual words, dependent
  on "many influences which are unpredictable and only limitedly controllable by the company, with
  the most important influencing factor being capital-market developments" [S8]. That disclaimer is
  why surplus is modelled as a **declaration** — an insurer-discretionary current assumption — and
  never as a guarantee.
- **The declaration instrument is an annual document**: the Konzern Versicherungskammer publishes
  its *"Überschussverteilung 2026"* as a standalone PDF [S15], and every German life insurer
  publishes an equivalent. **No rate from any such document was established** — gap 4.
- **Surplus systems in the accumulation phase.** Three are established, two in-scope designs and
  one successor design:
  1. ***Verzinsliche Ansammlung*** — the classic default. Declared surpluses are invested and bear
     interest, "similar to a classic capital life insurance or private pension insurance" [R24].
     The mechanics are explicit: **"the ongoing surplus portions are credited to the
     *Ansammlungsguthaben* and accrued with interest, with the interest credited at the end of each
     insurance year and upon termination of the insurance"** [R24]. The accumulation account is a
     **second, parallel account** to the *Deckungskapital*, with its own credited rate, settling at
     year end and at exit.
  2. ***Bonusrente* / *Bonussystem*** — declared surpluses buy **additional premium-free annuity**
     [R24]; in the payout phase the split is explicit (section 9).
  3. **Investment of surplus in an internal fund** — the successor design. Debeka: "surplus shares
     of the accumulation phase are invested in an internal fund and can enable additional
     benefits", and "fund holdings generally receive no *Überschussbeteiligung* from the earnings
     of Debeka's general *Sicherungsvermögen* before *Rentenbeginn*" [S12]. Guarantees on the
     general account, declared surplus on a fund — a **departure from the classic product**, and
     therefore a variation, not the representative design.
- ***Beitragsverrechnung*** — surplus applied to reduce the premium due — is the fourth system the
  German market uses. **No source in this corpus named it for this product** (gap 16).
- **Bewertungsreserven.** Under **§ 153 Abs. 3 VVG** policyholders participate **equally
  (*hälftig*)**, as restated by an insurer's own consumer information [S4] [R4]. Two
  product-specific consequences from the same source: the ***Rentenbeginn* is a key point for that
  participation**, and **participation continues during the payout phase**.
- **The four-component decomposition of surplus** — *Zinsüberschuss*, *Risikoüberschuss*,
  *Kostenüberschuss*, *Schlussüberschussanteil* — is **only partly established here**. The
  *Zinsüberschuss* is established directly ("when investment income exceeds the calculation rate …"
  [R24]); the other three were not named by any summary and are `[unverified]` *(withdrawn 2026-08-30)* (gap 17). They are
  **Resolved 2026-08-30: confirmed** — [S8] § 2 names all three surplus sources with their MindZV minima and [S4] § 3 Abs. 4–5 names the *Grundüberschuss-*, *Beitragsüberschuss-* and *Schlussüberschussanteil*. Tag withdrawn.
  the primary subject of the delib `kapitallebensversicherung` file, which shares this chassis.

### 7. Todesfallleistung before Rentenbeginn

- On death of the insured **during the *Aufschubzeit***, the contract pays a death benefit and
  ends. The corpus establishes **three distinct designs**, all in use [R24]:
  1. ***Beitragsrückgewähr*** — **"the insurer refunds all paid premiums after the death"**, with
     an optional extension: **"if the insured dies during the *Aufschubzeit*, repayment of the
     premiums plus the *Überschussbeteiligung* attributable to them can be agreed"**. So it comes
     in a bare form and a with-surplus form, and the choice is contractual.
  2. **Payment of the accumulated *Deckungskapital*** — "during the *Aufschubzeit*, the
     *Deckungskapital* accumulated up to that point is paid out".
  3. **A *Hinterbliebenenrente*** — survivors may receive, **depending on the contractual
     arrangement, a *Beitragsrückgewähr*, the accumulated capital, or a *Hinterbliebenenrente***.
     The survivor's annuity has its own GDV model condition set [S10] and is properly a rider.
- **The *Beitragsrückgewähr* is named in the GDV model conditions for this product** [S1] — the
  model wording's own term, not a marketing label.
- **The `max(...)` form is established for the unit-linked sibling, not for the classic product.**
  DEVK: the death benefit is "the fund value at the date of death, **but at least the sum of the
  premiums paid (*Beitragsrückgewähr*)**" [S19]. The classic analogue —
  `max(Deckungskapital, premiums paid)` — is the obvious counterpart, but **no classic-product
  document in this corpus stated it in that form**; it is `[unverified]` *(withdrawn 2026-08-30)* as the classic rule, and a
  **Resolved 2026-08-30: CONTRADICTED** — [S9] § 1 Abs. 3 states the `max` form for a **classic** deferred annuity, *"mindestens jedoch die sogenannte Beitragsrückgewähr"*. Tag withdrawn.
  representative design that adopts it must tag it `[std]`.
- **What the death benefit is *not*:** there is no separate sum insured. It is defined off the
  premiums paid or off the accumulated fund, never off an independently chosen *Versicherungssumme*
  [S19] [R24] — the structural difference from delib's `kapitallebensversicherung` and
  `risikolebensversicherung`.
- **Whether the benefit falls at the date of death or at the next policy anniversary, and whether
  the with-surplus form includes the *Ansammlungsguthaben* in full, were not established** — gap 18.

### 8. The Rentenfaktor

This is the mechanic the whole product turns on, and it is the best-evidenced thing in the file.

**Definition and arithmetic.** The *Rentenfaktor* **determines how much monthly annuity is
received per 10 000 € of accumulated capital** — "wie hoch die ausgezahlte monatliche Rente pro
10 000 Euro angespartem Vermögen ausfällt" [R24]. The arithmetic, as given: **capital of 100 000 €
with a *Rentenfaktor* of 25 yields 250 € per month**, computed as `100 000 / 10 000 × 25` [R24].
The factor 25 in that illustration is a **teaching example, not a market level** — see gap 3. In
model notation:

```
monthly_annuity = Kapital(Rentenbeginn) / 10 000 x Rentenfaktor
```

**Guaranteed at inception, on the tariff bases.**

- **The *garantierter Rentenfaktor* is fixed in the contract documents and rests on the
  *Rechnungsgrundlagen* as at the date of contract conclusion** [R24] — a guarantee given at issue
  about a conversion that will happen decades later.
- **The insurer applies a *Sicherheitsabschlag* in calculating it, which is why it comes out lower
  than the current factor** [R24].
- **The margin is quantifiable from one carrier.** CosmosDirekt: "the annuity factor determined at
  the beginning of the contract is calculated on the basis of a recognised mortality table
  (currently DAV 2004 R) and an underlying interest rate (**currently 0 percent p.a.**)" [S8]. A
  zero-percent interest basis, against a *Höchstrechnungszins* that has been positive throughout,
  is the *Sicherheitsabschlag* made concrete: the guaranteed factor is priced as though the insurer
  will earn nothing on the annuity fund.
- Allianz expresses the same guarantee as **"a minimum annuity"** available at inception [S13] —
  the *garantierter Rentenfaktor* stated as an amount rather than a factor.

**Current factor, and the comparison at Rentenbeginn.**

- **The *aktueller Rentenfaktor* is influenced by economic factors such as the interest level and
  the life expectancy of the insured person** [R24], and is recomputed on the bases in force when
  it is quoted.
- **Allianz states what "current" means operationally**: the calculation bases at *Rentenbeginn*
  "relate to the interest rate and mortality table that the company uses **at that time for
  immediately beginning annuities**" [S13]. The current factor is the carrier's then-current
  immediate-annuity tariff — which is why [S16] belongs in this file.
- **The rule at *Rentenbeginn* is a maximum of two factors.** Zurich: the guaranteed *Rentenfaktor*
  is carefully calculated, and **at the start of annuity payments a second *Rentenfaktor* is
  compared with it, the higher of the two being guaranteed for the annuity payment period** [S4].
  The consumer literature states the same rule from the other side: **the guaranteed factor is a
  floor and comes into play only if the current factor at *Rentenbeginn* is lower; otherwise the
  annuity is computed on the then-current factor** [R24]. In model notation:

  ```
  Rentenfaktor_applied = max( Rentenfaktor_garantiert, Rentenfaktor_aktuell(Rentenbeginn) )
  ```

  This is a **guarantee with upside**, and a model that applies only the guaranteed factor
  understates the benefit whenever the current tariff is richer.

**Movement with the Höchstrechnungszins.** The factor moves with the *Rechnungszins* and with the
mortality basis, because those are the two things it is computed from [S8] [S13] [R24]. The
*Höchstrechnungszins* history therefore maps onto it: the thirty-year decline to 0,25 % [R7]
compressed guaranteed factors, and the 2025 increase to 1,00 % [R7] [R8] should have relieved that
compression for new business. **The magnitude was not established** — no search returned a level,
range or time series, not even from the rating house whose article asks "wie hoch ist er?" [R19].
See gap 3: a representative *Rentenfaktor* is the one parameter a delib worked example cannot
avoid choosing, and it will be `[std]`.

**Reduction of a factor: the Treuhänderklausel and § 163 VVG.**

- **Historically:** insurers could change guaranteed *Rentenfaktoren* on the basis of a
  ***Treuhänderklausel*** in the conditions, **with the approval of an independent external
  *Treuhänder***, where economic conditions deteriorated permanently and unexpectedly [R17].
- **Two explicit triggers**: an **unexpectedly strong increase in life expectancy**, requiring
  adjustment of the mortality tables, and a **sustainable reduction in capital-market returns**,
  permitting adjustment of the interest rate [R17].
- **Currently:** the clause **is used only in older contracts; today the guaranteed *Rentenfaktor*
  can be changed only on the basis of § 163 VVG** [R17] [R3].
- **The courts have narrowed it.** The **Landgericht Köln** held that **the low-interest phase is
  not a sufficient ground, because it must be assessed as entrepreneurial risk that cannot be
  passed on to policyholders** [R17]; consumer press reports that a subsequent reduction **can be
  unlawful** [R16]. **The case reference and decision date were not established** — gap 10.
- **It was a live commercial dispute at the market leader in 2021**: trade press of 4 February 2021
  reports Allianz's position that customers could not successfully object to an adjustment [R18].
- **Modelling consequence.** The guaranteed *Rentenfaktor* is a contractual guarantee with a
  narrow, contested statutory adjustment channel. A delib model treats it as **fixed for the life
  of the contract** and records § 163 VVG as a model risk rather than implementing it.

### 9. The Rentenphase

- The annuity in payment is **the sum of a *garantierte Rente* and an *Überschussrente***: the
  insurer sets a value at the start of the payout phase "composed of the *Garantierente* and a
  surplus share projected for the whole annuity period" [R20]. Only the guaranteed part is a
  promise.
- **Three *Überschussverwendung* systems exist in the payout phase**, and the choice is the
  policyholder's [R19] [R20] [R24]:

  | System | Mechanic |
  |---|---|
  | **konstante Rente** | The payout stays the same over the whole term. The insurer fixes a value at the start of the payout phase from the *Garantierente* plus a surplus share **projected for the whole annuity period**. In practice it can still fluctuate: **if the provider earns less than expected, the annuity falls** [R20]. |
  | **teildynamische Rente** | The annuity rises regularly by a **fixed percentage**, provided the insurer earns corresponding surpluses. It is **a combination of the constant and the dynamic system**: part of the expected surplus is used under the constant system and part under the dynamic system to form an additional annuity [R20] [R24]. |
  | **volldynamische (steigende) Rente** | The annuity **adjusts annually and flexibly to the actual surplus development** [R20]. It starts lowest and rises fastest. |

- The ***Bonusrente*** is the mechanism underneath the rising forms: "the ongoing surplus shares
  are used partly for an age-dependent *Überschussrente* and partly for an additional premium-free
  annuity (*Bonusrente*)" [R24]. The increment, once bought, is **premium-free and permanent** —
  which is what makes a *volldynamische Rente* ratchet rather than fluctuate.
- **The constant form is not actually constant.** Under it the annuity is set from a
  **projection**, and **if the insurer earns less than projected the annuity is reduced** [R20]. A
  model that treats the *konstante Rente* as a level guaranteed stream is wrong; only the
  *garantierte Rente* inside it is guaranteed.
- **Participation in *Bewertungsreserven* continues during the payout phase** [S4] [R4].
- ***Rentengarantiezeit***, established in detail [R17] [R24]: a guaranteed payment period
  beginning at *Rentenbeginn*; if the annuitant dies inside it, **the annuity continues to be paid
  to the survivors until the agreed years have expired** (worked illustration: a 10-year period,
  death after 6 years, **the spouse receives the remaining 4 years**). **Durations offered: 5, 10,
  15, 20, 25 or more than 30 years**; **typical durations 15 years for retirement ages 61–70 and
  10 years for 71 and above**; **most policyholders choose 10 to 20 years**. It is a selectable
  parameter with a floor at Allianz [S13] and a tariff-level feature carried in the product name at
  NÜRNBERGER [S9]. **It costs annuity**: on the corpus's own illustration — 200 € monthly premium
  over 30 years producing 573 € per month with no guarantee period — a 10-year guarantee costs
  **3 €** per month, a 20-year guarantee **15 €**, a 30-year guarantee **46 €** [R24], that is
  roughly 0,5 %, 2,6 % and 8,0 % of the annuity (arithmetic performed here on the source's own
  figures, offered as an order of magnitude, not a tariff).
- ***Beitragsrückgewähr* in the *Rentenbezugsphase*** — a refund on death after *Rentenbeginn* of
  premiums paid less annuity instalments received — **was not established by any source in this
  corpus** (gap 18) and must not be asserted downstream. What the corpus does establish for
  post-*Rentenbeginn* death is the *Rentengarantiezeit* [R24] and the survivor's-annuity rider
  [S10].
- **Payment timing.** The annuity is described throughout as **monthly** [S13] [R24]. **Whether it
  is payable in advance (*vorschüssig*) or in arrears was not established** (gap 19), despite being
  a first-order modelling parameter. A delib model adopts monthly-in-advance as a `[std]`
  convention with the gap stated beside it.

### 10. The Kapitalwahlrecht

- The ***Kapitalwahlrecht*** is the policyholder's right to take **the accumulated capital as a
  lump sum instead of the lifelong annuity** at *Rentenbeginn* [S12] [R6] [R21].
- It is exercised **at or before *Rentenbeginn***, and it is the third of the three things that
  happen at that boundary (section 2).
- **The notice period was not established.** The German market convention is a declaration a set
  period before *Rentenbeginn*, but **no document or search summary in this corpus named a period
  at any carrier** — gap 11. Downstream this is `[std]`.
- **The tax consequence of electing it is total, and it is established.** Electing the lump sum
  moves the contract from the ***Ertragsanteil*** regime of § 22 EStG [R5] to the **§ 20 EStG**
  regime [R6]:
  - **The *Halbeinkünfteverfahren* applies only to lump-sum payments and to multiple capital
    withdrawals under a payout plan; it does not apply to monthly annuity payments** [R6].
  - **It requires the "12/62 rule": the contract must have run at least 12 years and the payment
    must occur after completion of the 62nd year of life** [R6].
  - **Where the rule is met, half the *Ertrag* is taxable**; the other half is exempt [R6].
  - **The contract must be one in which the capital option cannot be exercised before 12 years
    from contract conclusion** for § 20 EStG to apply in this way [R6].
- Debeka states the annuity side of the same choice from the insurer's page: **if a lifelong
  monthly annuity is chosen at *Rentenbeginn*, only part of the payout is taxed — the
  comparatively low *Ertragsanteil*, depending on age at *Rentenbeginn*** [S12].
- **Modelling consequence.** The *Kapitalwahlrecht* is a **policyholder election at a single known
  date**, not a continuous option. In a reference implementation it is a model-point switch that
  changes the entire post-*Rentenbeginn* cash-flow shape from an annuity stream to a single
  payment, and the take-up rate is a behavioural assumption with **no public evidence in this
  corpus** (gap 20).

### 11. The Rechnungsgrundlagen: DAV 2004 R, generational, sex-distinct, unisex tariff

- **The mortality basis is DAV 2004 R.** CosmosDirekt names it in its own AVB: the *Rentenfaktor*
  is calculated "on the basis of a recognised mortality table (**currently DAV 2004 R**)" [S8].
- **DAV 2004 R is a *Generationentafel*** used for annuity insurance calculations in Germany
  [R13]; generation tables **contain mortality per birth cohort, including the expected future
  change in mortality** [R13] [R15] — the trend is inside the table.
- **Component structure** [R12]: a base table of second order; a base table of first order; a
  mortality trend of second order; a mortality trend of first order; and an age adjustment
  (*Altersverschiebung*) with a base table.
- **First against second order** [R12]: **first-order probabilities are used for premiums and
  reserves and carry safety margins relative to the second-order ("realistic") probabilities, in
  order to assess the risk prudently**; the **second-order base tables represent the best estimate
  of period mortality in 1999 for insured lives, as three-dimensional selection tables**.
- **Dates** [R13] [R14]: in use **since June 2004**, **intended for new business from 2005**, the
  DAV document itself dated **22 February 2005**; practitioner presentations of 16 August and
  14 September 2004 and a reinsurer's exposition of 27 October 2004 date the market's adoption.
- **The DAV reissued the derivation guideline on 28 June 2023** [R12] — nineteen years after first
  use and twenty-four after the 1999 base year. That the profession was still maintaining
  DAV 2004 R in 2023 is itself the evidence that no successor annuity table has displaced it.
- **A companion in-force table exists**: a 2004 presentation titled "DAV 2004 R und RBx" [R14],
  RBx being the *Rentenbestandstafel* for the existing annuity book as against new business. The
  corpus establishes the pairing and nothing more.
- **The table is not public and is not redistributed by delib.** delib cites it by name, ships a
  `[std]` proxy anchored so its own worked example reproduces exactly, and states the anchor in the
  `Data` docstring. A replacement must preserve the **generational structure** (a `q(x, cohort)`
  surface, not a period table), the **first-order margin over second order**, and the
  **age-adjustment convention** [R12] [R13].
- **Sex-distinct tables against a unisex tariff.** German annuity tables are constructed
  sex-distinctly while the tariff sold since *Test-Achats* must be unisex. **Neither half of that
  sentence was established by any search in this session**: no summary confirmed that DAV 2004 R is
  published by sex, and no summary touched the unisex rule, the ECJ case or the 21 December 2012
  German application date. Both are `[unverified]` here (gap 21); the unisex rule belongs to the
  **Status 2026-08-30: half resolved** — [S11] § 52 Abs. 1 and § 28 Abs. 2 name *geschlechtsunabhängige* company tables, which is the unisex rule in a tariff. That DAV 2004 R is published sex-distinctly is still unconfirmed.
  delib cross-product reference library.

### 12. Rückkaufswert (§ 169 VVG)

- **The surrender right exists** and its value is governed by § 169 VVG [R1].
- **For unit-linked contracts** the *Rückkaufswert* is computed **as the *Zeitwert* of the
  insurance according to recognised rules of actuarial mathematics**, insofar as the insurer does
  not guarantee a particular benefit, and **the principles of the calculation must be stated in the
  contract** [R1]. For the classic contract the guaranteed benefit exists, so the *Zeitwert* clause
  is the boundary rather than the rule; **what the classic surrender value is computed as was not
  established at article level** (gap 12).
- **A deduction is permitted only if it is agreed, quantified (*beziffert*) and appropriate
  (*angemessen*)** — three cumulative conditions — and **a deduction for not-yet-amortised
  *Abschluss- und Vertriebskosten* is void (*unwirksam*)** [R1]. That is the statutory answer to
  *Zillmerung*: the front-loading may not be recovered from the surrendering policyholder as a
  named deduction.
- **The computed value may be reduced by a contractually agreed and appropriate *Stornoabzug*
  (*Rückkaufsabschlag*)**; the result is the **statutory minimum surrender value**, below which a
  contractually agreed value may not fall [R1]. **§ 169 Abs. 6 VVG permits the insurer, in defined
  cases, to reduce surrender values that are to be paid out** [R1] — a solvency valve, not an
  ordinary charge.
- **The five-year spreading of *Abschluss- und Vertriebskosten*** associated with § 169 Abs. 3 VVG
  was **not returned by any summary** and is `[unverified]` *(withdrawn 2026-08-30)*, even though § 165 VVG's own text refers
  **Resolved 2026-08-30: confirmed at three carriers** — 25,00 € a month [S4] [S9], 600,00 € a year for a partial surrender [S8]. The threshold is contractual, not statutory. Tag withdrawn.
  to "§ 169 paragraphs 3 to 5" [R2] — which independently establishes that those paragraphs carry
  the calculation rules on which both the surrender value and the paid-up value are built. **No
  *Stornoabzug* percentage, surrender-value table or charge-recovery schedule was established at
  any carrier** (gap 12).

### 13. Beitragsfreistellung (§ 165 VVG)

- **The policyholder may at any time demand, for the end of the current insurance period, that the
  insurance be converted into a premium-free insurance, provided the agreed minimum insurance
  benefit is reached** [R2]. The right is statutory and unconditional apart from that threshold.
- **If the minimum benefit is not reached, the insurer must instead pay the surrender value
  attributable to the insurance, including profit shares, under § 169** [R2] — a small contract
  cannot be made paid-up; it is cashed out.
- **The premium-free benefit is calculated according to recognised principles of actuarial
  mathematics, using the calculation basis of the premium calculation, on the basis of the
  surrender value under § 169 paragraphs 3 to 5, and must be stated in the contract for each
  insurance year** [R2]. Three consequences: the paid-up value is **derived from the surrender
  value**; it uses the **premium basis**, not a current basis; and it must be **tabulated per
  insurance year in the policy document**.
- Applied to this product: **the policyholder always has the right to convert a running annuity
  contract into a premium-free annuity contract** [R2] — the contract does not lapse, it continues
  with a reduced guaranteed annuity. **The *Mindestversicherungsleistung* threshold was not
  established at any carrier** (gap 22) and will be `[std]`.
- **The difference from *Kündigung*** matters: *Beitragsfreistellung* keeps the contract, its
  guarantee vintage and its guaranteed *Rentenfaktor* alive on a reduced benefit; *Kündigung* ends
  it for the *Rückkaufswert* [R1] [R2]. Where old contracts carry a high legacy *Rechnungszins* and
  old guaranteed *Rentenfaktoren*, that difference is worth a great deal, and it is why paid-up
  conversion and lapse must be **separate decrements**.
- **Wiederinkraftsetzung** — reinstatement of a paid-up contract — appears in the corpus only as a
  Debeka specimen endorsement file name (`Muster-NachtragWiederinkraftsetzung…`). Its existence as
  a documented process is established at that level and nothing more.

### 14. Charges

The weakest area of the corpus.

- **The premium is split, with a portion "intended for risk and cost coverage" deducted before the
  *Sparbeitrag*** [S11]: charges are **premium-based deductions**, not asset-based ones, in the
  classic chassis.
- **Two Allianz figures, both from third-party analysis of a specimen quotation** [S13] [R23]: an
  **Abschlussprovision of 1 575 €**, and **in the BasisRente and RiesterRente variants total costs
  relative to the capital formed of at most 0,95 € per 100 €**. Both are `[unverified]` as
  **Status 2026-08-30:** unchanged — see gap 14. Neither figure is established by any retrieved document.
  representative levels; neither is for the Schicht-3 tariff.
- **§ 169 VVG forbids recovering unamortised acquisition costs as a named surrender deduction**
  [R1], which constrains how *Zillmerung* is expressed but not how it is charged.
- **Not established, at any carrier**: the *Abschluss- und Vertriebskosten* rate; the
  *Höchstzillmersatz* (the 25 ‰ of *Beitragssumme* ceiling introduced by the LVRG 2014 is
  `[unverified]` *(withdrawn 2026-08-30)* here and belongs to the cross-product reference library); the *Verwaltungskosten*
  **Resolved 2026-08-30: confirmed** — § 4 Abs. 1 Satz 2 DeckRV, *"Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten"*, restated by four carriers as "2,5 % der Beiträge". Tag withdrawn for the ceiling; the *Verwaltungskosten* tag stands.
  in any form; the *Ratenzahlungszuschlag*; the payout-phase administration charge; and the
  *Effektivkosten* disclosure. See gaps 13 and 14. **Every charge figure in the delib product
  documents will therefore be `[std]`.**

### 15. Taxation

- **The annuity is taxed on the *Ertragsanteil* under § 22 EStG** [R5] [R24]. Payments from private
  annuity contracts, and from life contracts converted into a classic monthly *Leibrente*, fall
  under this regime, and **only the "Ertrag des Rentenrechts" is taxed** — the interest component
  contained in the annuity from the beginning of the payout phase, not the return of capital [R5].
- **The *Ertragsanteil* depends on the annuitant's age at *Rentenbeginn***; the earlier the annuity
  begins, the longer the expected duration and the **higher** the taxable fraction [R5] [R24].
  **At age 65 it is 18 %** [R5] — the only value on the statutory table this session established;
  every other age is `[unverified]` *(withdrawn 2026-08-30)* (gap 8).
  **Resolved 2026-08-30: confirmed and extended** — the whole § 22 table is read. Tag withdrawn.
- **Electing the *Kapitalabfindung* moves the contract to § 20 EStG** and the
  *Halbeinkünfteverfahren*, subject to the **12/62 rule** and to the condition that **the capital
  option cannot be exercised before 12 years from contract conclusion** [R6]. **Half the gain is
  taxable**, and the method applies **only to lump sums and payout-plan withdrawals, not to monthly
  annuities** [R6].
- **Contracts concluded before 1 January 2005 retain the half-income treatment of the lump sum, and
  annuity payments continue uniformly to be taxed on the *Ertragsanteil* basis** [R6]. The
  1 January 2005 boundary is the *Alterseinkünftegesetz* watershed: a German in-force book carries
  **two tax cohorts**.
- **The two regimes are why the *Kapitalwahlrecht* is an economically live choice**, not a
  formality: the annuitant compares 18 % of each annuity instalment taxed at the marginal rate [R5]
  against half of the total gain taxed once [R6].
- **Not established:** the rate applied to the taxable half (personal or flat), the
  *Solidaritätszuschlag*, the inheritance-tax treatment of the death benefit, and the
  *Kleinbetragsrente* commutation threshold. See gap 23.

### 16. Decrements and policyholder behaviour

- **Mortality** in the accumulation phase pays the death benefit of section 7; in the payout phase
  it terminates the annuity. The pricing basis is DAV 2004 R first order [S8] [R12], the
  best-estimate basis DAV 2004 R second order [R12].
- **The two phases use the same table**, which is a German peculiarity worth stating: an annuity
  table is used to price a death benefit before *Rentenbeginn*, so that benefit is systematically
  **under**-reserved relative to a population basis — and the *Beitragsrückgewähr* design [R24]
  exists partly because it makes the mismatch immaterial, the benefit being the premiums rather
  than a sum insured.
- **Lapse (*Storno*)** produces the *Rückkaufswert* [R1]; **paid-up conversion** is a separate
  decrement producing a reduced benefit [R2]. They must not be modelled as one.
- **No lapse rate, no paid-up rate, no *Kapitalwahlrecht* take-up rate and no German life-market
  *Stornoquote* was established** (gap 20). Every behavioural assumption in the delib documents
  will be `[std]` and labelled a modeller's view.

### 17. Market context: the retreat from the classic tariff

- **The classic deferred annuity has been withdrawn from sale by several of the largest German
  writers.** Debeka "will no longer offer classical annuity insurance", confirmed by a company
  spokesperson [R22], and its own page states that the offer is now the newer variants with a
  flexible allocation between guaranteed and fund-based components [S12].
- **Debeka's replacement**: from **1 July 2016**, five tariff variants under the name **"Chance"**,
  the safest guaranteeing **0,5 % interest** and the riskiest **effectively a fund policy with no
  guarantees** [R22]. **Debeka was following, not leading: Allianz, Zurich and Generali had already
  stopped distributing classic annuity insurance** [R22].
- **Allianz's replacement is KomfortDynamik** [S13] [R23]: premiums split between the
  *Sicherungsvermögen* and a *Spezialfonds*; **guarantee levels of 60 %, 80 % or 90 % of the
  premiums paid** at *Rentenbeginn*, selectable, 80 % standard; and, at inception, "only modest
  guarantees" — the premium-retention level and **a minimum annuity** [S13]. The trade-press
  headline asks whether it is "noch immer eine Rentenversicherung" [R23].
- **Zurich, by contrast, still publishes a *Verbraucherinformation für Konventionelle
  Versicherungen* for the deferred annuity in the Fassung 01/2026** [S4], and CosmosDirekt still
  publishes AVB whose *Rentenfaktor* is fixed at inception on DAV 2004 R [S8]. **The two
  statements are in tension** with [R22]'s report that Zurich stopped distributing the classic
  annuity. The likely reconciliation — that the withdrawal was of a specific classic tariff family
  and not of the conventional chassis — **was not resolved** (gap 9), and it is why the delib
  representative design is a composite of a chassis rather than a currently-purchasable product.
- **The consequence for delib.** The classic deferred annuity is best described as **the German
  market's reference chassis** — the design every successor product is a modification of, and the
  design the large in-force book still runs on — rather than as a live new-business product. That
  is the role lifelib reference models are for, and it is the framing the product-spec adopts.

## Observed variation across insurers

The corpus supports **structural** variation tables. It does **not** support quantitative range
tables for the parameters that matter most — *Rentenfaktor* levels, charges, entry ages, premium
envelopes and surplus rates — because no search in this session returned a number for any of them
at any carrier. Where a row reads "not established", that is the finding, not an omission.

### Carriers in the corpus

| Carrier | Document(s) | Status of the classic deferred annuity |
|---|---|---|
| GDV (industry model wording) | [S1] [S2] [S3] [S10] | Model conditions maintained; 2021 edition seen; expressly non-binding [S2] |
| Zurich Deutscher Herold | [S4] [S5] [S6] [S7] [S16] [S17] | *Verbraucherinformation* published 2021, 2022 and **01/2026** [S4]; but reported among the carriers that stopped [R22] — unresolved, gap 9 |
| CosmosDirekt (Cosmos Leben, Generali) | [S8] | AVB LA 904 A published; vintage not established; Generali reported among those that stopped [R22] |
| NÜRNBERGER | [S9] | AVB for tariff NIR3301, *mit Rentengarantiezeit* |
| Debeka | [S11] [S12] | **Withdrawn.** Replaced from 1 July 2016 by five "Chance" variants [R22] [S12] |
| Allianz | [S13] | **Withdrawn.** Replaced by KomfortDynamik, a 60/80/90 % premium-guarantee hybrid [S13] [R22] [R23] |
| Mecklenburgische | [S14] | *Vertragsinformationen* for "Rente flex"; product feature not established |
| Konzern Versicherungskammer | [S15] | Annual *Überschussverteilung 2026*; rates not established |
| Stuttgarter | [S18] | *Allgemeine Informationen* pack dated 2020 |
| DEVK | [S19] | Unit-linked only; used for the death-benefit contrast |

### Death benefit before Rentenbeginn, and Rentenfaktor determination

| Item | Observation | Source |
|---|---|---|
| *Beitragsrückgewähr*, premiums only | named in the GDV model wording | [S1] [R24] |
| *Beitragsrückgewähr* plus attributable surplus | "can be agreed" — a contractual election | [R24] |
| Accumulated *Deckungskapital* | the alternative classic design | [R24] |
| *Hinterbliebenenrente* | own GDV model condition set — a rider | [S10] [R24] |
| `max(fund value, premiums paid)` | unit-linked wording [S19]; **the classic analogue is established** — contract value plus final surplus and *Bewertungsreserven*, *"mindestens jedoch die sogenannte Beitragsrückgewähr"* | [S9] § 1 Abs. 3; [S14] § 2 Abs. 9 a) |
| Guaranteed *Rentenfaktor* fixed at inception | yes | [S8] [R24] |
| Its mortality basis | **DAV 2004 R** | [S8] |
| Its interest basis | **0 % p.a.** at one carrier, at an unestablished vintage | [S8] |
| A *Sicherheitsabschlag* makes it lower than the current factor | yes | [R24] |
| Current factor = carrier's then-current immediate-annuity tariff | yes | [S13] |
| Rule at *Rentenbeginn* | **higher of the two** | [S4] [R24] |
| Typical level in € per 10 000 €, and its movement since 2025 | **not established** | gap 3 |

### Rentengarantiezeit, and the surplus systems

| Item | Observation | Source |
|---|---|---|
| Durations offered | 5, 10, 15, 20, 25, 30+ years | [R24] |
| Typical, retirement age 61–70 / 71+ | 15 years / 10 years | [R24] |
| Most commonly chosen | 10–20 years | [R24] |
| Cost (200 €/month, 30 years, 573 €/month base) | 10 y: −3 €; 20 y: −15 €; 30 y: −46 € per month | [R24] |
| Carried in the tariff name | NÜRNBERGER NIR3301 | [S9] |
| Policyholder-selectable with a floor | Allianz PrivatRente KomfortDynamik | [S13] |
| Accumulation: *verzinsliche Ansammlung* (*Ansammlungsguthaben*, interest at each year end and at exit) | established | [R24] |
| Accumulation: *Bonusrente* / *Bonussystem* | established | [R24] |
| Accumulation: surplus invested in an internal fund | established — Debeka's successor design | [S12] |
| Accumulation: *Beitragsverrechnung* | **not established** | gap 16 |
| Declared rates for any year | **not established** | gap 4 |
| Payout: *konstante Rente* | set from a whole-period projection; **falls if the insurer earns less** | [R20] |
| Payout: *teildynamische Rente* | rises by a fixed percentage if surpluses permit; part constant, part dynamic | [R20] [R24] |
| Payout: *volldynamische (steigende) Rente* | adjusts annually to actual surplus development | [R20] |
| Payout: *Bewertungsreserven* participation continues | yes | [S4] [R4] |

### Guarantee level at Rentenbeginn — classic against successor designs

| Design | Guarantee at *Rentenbeginn* | Source |
|---|---|---|
| Classic (this product) | *Sparbeiträge* accumulated at the *Rechnungszins*, ≥ 100 % by construction | [S11] |
| Debeka "Chance", safest variant (from 1 July 2016) | 0,5 % guaranteed interest | [R22] |
| Debeka "Chance", riskiest variant | none — effectively a fund policy | [R22] |
| Allianz KomfortDynamik | **60 %, 80 % or 90 % of premiums paid**, selectable, 80 % standard | [S13] [R23] |

### What the corpus supports as a representative design

1. A **single-life deferred annuity on the general account**, Schicht 3, against a level recurring
   premium over a fixed *Aufschubzeit* [S4] [S11].
2. A ***Deckungskapital* accumulating the *Sparbeitrag* at a contract-vintage *Rechnungszins***,
   the *Sparbeitrag* being the premium net of the risk and expense portions [S11]; the
   *Rechnungszins* a **model-point attribute**, not a global assumption [R7].
3. ***Verzinsliche Ansammlung*** as the accumulation-phase surplus system, with a separate
   ***Ansammlungsguthaben*** crediting interest at each year end [R24]; the credited rates `[std]`.
4. A ***Beitragsrückgewähr*** death benefit before *Rentenbeginn*, in the premiums-only form named
   by the GDV model wording [S1] [R24], with the *Deckungskapital* form available as a switch.
5. Conversion at *Rentenbeginn* of `max(guaranteed contract value, Deckungskapital +
   Ansammlungsguthaben + Bewertungsreserven)` [S9] at
   `max(garantierter Rentenfaktor, aktueller Rentenfaktor)` [S4] [R24], the guaranteed factor
   struck at inception on **DAV 2004 R** and a conservative interest basis [S8].
6. A payout phase of ***garantierte Rente* plus *Überschussrente***, monthly, with the three
   surplus systems selectable and **the constant system explicitly not level** [R20], and a
   ***Rentengarantiezeit*** of 10 to 20 years [R24].
7. A ***Kapitalwahlrecht*** at *Rentenbeginn* [R6] [R21], with the notice period and take-up rate
   `[std]`.

8. ***Rückkaufswert*** under § 169 VVG [R1] and ***Beitragsfreistellung*** under § 165 VVG [R2] as
   **separate decrements**, the paid-up value derived from the surrender value on the premium
   basis and tabulated per insurance year [R2].

9. ***Dynamik*** (*Anpassungsversicherung*) as a documented but parameter-less option [S4], off in
   the base run.
10. Taxation on the ***Ertragsanteil*** for the annuity, **18 % at age 65** [R5], and the
    ***Halbeinkünfteverfahren*** under the 12/62 rule for the *Kapitalabfindung* [R6].

Every number in that design that is not tagged above is `[std]`, for one reason: **the corpus
establishes the mechanics of this product thoroughly and its levels barely at all.**

---

## Gaps and caveats

> **Retrieval pass, 2026-08-30.** This register was written when nothing could be opened. Every
> cited URL has since been tried and the body kept, and the statutes read as canonical XML. The
> numbered gaps are **kept verbatim** — they are the record of what the search phase established —
> and each now carries a **status line** saying what the retrieval did to it. Where a gap is closed,
> the closing evidence is named; where a retrieval **contradicted** what the gap or the entry said,
> that is stated as a contradiction and not smoothed over. **Fifteen of the twenty-six are closed**
> — five of them by a retrieved document contradicting what the gap or its entry said (3, 5, 12, 18,
> 25) — five are narrowed or half-closed (7, 9, 15, 21, 23), five stand (1, 13, 14, 20, 24), and the
> last, *living texts*, now carries its versions.

1. **The research budget was exhausted after eighteen queries.** This file's `WebSearch` budget was
   shared across fourteen parallel researchers and ran out mid-session; the brief anticipated
   thirty to eighty queries and eighteen were available. The queries that *were* run covered:
   classic deferred-annuity AVB; the *Rentenfaktor* (twice); GDV *Musterbedingungen*; the
   *Höchstrechnungszins*; *Überschussbeteiligung* in accumulation and in payout; the
   *Treuhänderklausel*; DAV 2004 R; the *Ertragsanteil*; the *Kapitalwahlrecht*; § 169 VVG;
   § 165 VVG; Allianz; Debeka; the *Rentengarantiezeit*; the death benefit before *Rentenbeginn*;
   Zurich; NÜRNBERGER; CosmosDirekt. The queries that were **not** run, and would have been next:
   current *Rentenfaktor* levels and the Franke und Bornberg / Morgen und Morgen / Assekurata
   ratings; the 2025 and 2026 *Überschussbeteiligung* declarations; charge and *Effektivkosten*
   levels; entry-age, premium and *Aufschubdauer* envelopes; unisex and *Test-Achats*; the
   *Zuzahlung*; the *Kapitalwahlrecht* notice period; *Beitragsrückgewähr in der
   Rentenbezugsphase*; *Stornoquoten*; and twenty further named carriers (R+V, HDI, Alte
   Leipziger, LV 1871, Continentale, Swiss Life, ERGO, AXA, Barmenia, Hannoversche,
   Württembergische, Gothaer, Stuttgarter, Volkswohl Bund, Baloise, Universa, Signal Iduna,
   Provinzial, HUK-Coburg, Dialog). **Everything below follows from this one gap.** Nothing was
   written to fill it and no URL, figure or paragraph number was guessed.

    **Status 2026-08-30: stands, with reduced consequence.** No new queries were run and no source was added. What the budget no longer determines is *how much each listed document yields*: seventeen of the nineteen primary sources and all but three references are now retrieved.

2. **No clause-level text was established from any primary document.** Not one AVB paragraph
   number, section heading or sentence of contractual wording was returned. [S1] [S2] [S4]–[S7]
   [S9] [S11] are established as *documents that exist and address named topics*, and in three
   cases ([S8] [S9] [S11]) as documents whose summary returned one or two substantive sentences.
   **There is no § numbering anywhere in this file for any AVB, and none may be invented
   downstream.**

    **Status 2026-08-30: CLOSED.** Clause-level text is read from eleven primary documents — [S1] [S4] [S5] [S6] [S7] [S8] [S9] [S10] [S11] [S14] [S16] — with their § numbering intact. Paragraph references in the delib product documents are checkable against them.

3. **No *Rentenfaktor* level, range or time series was established — at any carrier, for any
   year.** The only number in the corpus is the teaching illustration "*Rentenfaktor* 25 on
   100 000 € gives 250 € per month" [R24], which is arithmetic, not a market level. The rating
   house's own article "Was bedeutet der Rentenfaktor und wie hoch ist er?" [R19] returned no
   level, and the "Rentenfaktor-Check 2025" [R24] is titled as data and analysis but returned
   none. **Every *Rentenfaktor* downstream will be `[std]`**, anchored so the worked example
   reproduces exactly rather than presented as a market rate. That current factors "have moved
   with the *Höchstrechnungszins*" is directionally supported by the mechanics [S8] [S13] [R7] and
   is quantitatively `[unverified]`.

    **Status 2026-08-30: CONTRADICTED and closed.** The two articles the gap named do carry levels. [R19] gives an average *aktueller Rentenfaktor* of **29,09 €** for 2021 and **25,97 €** for 2022, a fall of 10,73 %, with a high of 26,61 (Condor) and a low of 20,43 (Bayerische / Pangaea Life). [R24]'s *Rentenfaktor-Check 2025* gives a full table by deferment term to age 67 — average guaranteed 24,33 (40 yrs) to 27,18 (15 yrs), average current 27,27 to 30,40, lowest guaranteed 17,72. The model's factors are unchanged and remain `[std]`; the divergence is recorded in `model.md`.

4. **No *Überschussbeteiligung* rate was established, for any year, at any carrier.** The corpus
   establishes the declaration document type and its 2026 vintage [S15] and nothing inside it: no
   *laufende Verzinsung*, no *Gesamtverzinsung*, no *Schlussüberschuss* rate, no
   *Bewertungsreserven* amount, no *Überschussrentensatz*. Every surplus rate downstream is
   `[std]` and must be labelled an insurer-discretionary current assumption.

    **Status 2026-08-30: CLOSED.** [S15] is read in full and its annuity section declares the *Zinsüberschussanteil* for tariff generations 2015–2025 as **3 % abzüglich Rechnungszins** before the *Rentenzahlungsbeginn* and **3,35 %** during the *Rentenbezug* for 2026 (2025: 2,25 % and 2,5 %), i.e. a total credited interest of **3,00 %**. It also carries the *hälftige* allotment rule and the annuity *Zuteilungszeitpunkte*. `decl_rate_table.csv` is unchanged and stays `[std]`.

5. **The CosmosDirekt AVB vintage is not established, and its "currently 0 percent p.a." clause is
   explicitly time-stamped.** [S8] reads "a recognised mortality table (**currently** DAV 2004 R)
   and an underlying interest rate (**currently** 0 percent p.a.)". The word *currently* means the
   figure is an as-at, and the as-at is unknown. Siblings in the same AVB series carry **11/2022**
   dates, so a vintage in or after 2022 is plausible; the LA 904 numbering is the oldest in the
   series, so an earlier vintage is equally plausible. **The hardest figure in the file has no
   date.**

    **Status 2026-08-30: CLOSED, and the clause it concerned CONTRADICTED.** The edition is **LA 904 A (01.17)**. But the sentence this gap was about is not in the document: the string *DAV* does not occur in [S8], and the only rate it names is the *"tarifliche[r] Garantiesatz von 0,90 Prozent p. a."*. There is no "currently 0 percent" clause to date.

6. **§ 163 VVG was not read at article level.** Its role as the operative adjustment channel is
   established from commentary [R3] [R17]; its paragraph structure, procedural conditions, trustee
   role and notice requirements are all `[unverified]`.

    **Status 2026-08-30: CLOSED.** § 163 VVG read at article level, *Stand: Art. 12 G v. 26.5.2026 I Nr. 156*. Title ***Prämien- und Leistungsänderung***; four *Absätze*; the three cumulative conditions of Abs. 1 including *"ein unabhängiger Treuhänder"*; the exclusion for original mispricing; the policyholder's election under Abs. 2 and the insurer's unilateral reduction power confined to premium-free contracts; the effective date at the start of the second month after reasoned notice (Abs. 3); the trustee dropped where supervisory approval is needed (Abs. 4).

7. **The *Höchstrechnungszins* history is established only at its two most recent points.** 0,25 %
   before 2025 and 1,00 % from 1 January 2025 [R7] [R10] [R11], plus "the first increase since
   1994" [R7] and the DAV's 1,0 % recommendation for 2026 [R8]. The intermediate sequence — 4 %,
   3,25 %, 2,75 %, 2,25 %, 1,75 %, 1,25 %, 0,90 % — and every effective date in it is
   `[unverified]` here. A model point carrying a legacy *Rechnungszins* must cite the
   cross-product reference library, not this file.

    **Status 2026-08-30: narrowed.** The DeckRV is read at article level [R7] and states the rate now in force (1 Prozent) plus the whole-term lock in § 2 Abs. 2. [R11] adds the endpoints of the decline, 4 % in 1994 to 0,25 % in 2022. The intermediate sequence and its effective dates are still `[unverified]` here.

8. **Only one value of the *Ertragsanteil* table was established:** 18 % at age 65 [R5]. Every
   other age is `[unverified]`, as is the precise statutory address of the table within § 22 EStG.

    **Status 2026-08-30: CLOSED.** The whole table is read from § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb EStG, *Stand: Art. 7 G v. 29.6.2026 I Nr. 197* — and that is also the precise statutory address, confirmed by [S4]'s own tax notes. 18 % is the value at **65 or 66**.

9. **Zurich's status is contradictory and unresolved.** [R22] reports Zurich among the carriers
   that stopped distributing classic annuity insurance before Debeka's 2016 withdrawal; [S4] is a
   Zurich *Verbraucherinformation für Konventionelle Versicherungen* for the deferred annuity in
   the **Fassung 01/2026**. Both cannot be read literally at once. The likely reconciliation —
   withdrawal of a specific classic tariff family rather than of the conventional chassis — **was
   not confirmed**, and the delib documents must not assert either reading.

    **Status 2026-08-30: narrowed and reconcilable.** [R22] retrieved in full says the carriers *stopped distributing* the classic form, and of Allianz only that it would offer it *"wenn dies ausdrücklich vom Kunden gewünscht werde"*. [S4], [S7] and [S16] are Zurich packs for this chassis in Fassung 01/2025 and 01/2026, on DAV 2004R at 1,00 %, and [S5] and [S6] are the 07/2015 vintage at 1,25 %. A wording reissued across three vintages is maintained, not withdrawn. The reading the delib documents may state is: withdrawn from active distribution, retained as a chassis.

10. **The Landgericht Köln *Rentenfaktor* decision has no case reference.** The holding — that the
    low-interest phase is entrepreneurial risk and not a ground for adjustment — is established
    from consumer material [R17] and corroborated at headline level by [R16]. **Case number,
    decision date, parties and appeal history are all unestablished.** No citation may be made
    beyond "a Landgericht Köln decision reported by [R17]".

    **Status 2026-08-30: CLOSED, and a later decision found.** The Landgericht Köln decision is ***LG Köln, 08.02.2023, Az. 26 O 12/22***, against Zurich [R16] [R17]. Above it there is now a Bundesgerichtshof decision holding the Allianz clause ineffective: ***BGH, 10.12.2025, Az. IV ZR 34/25*** [R16]. [R18] retrieved in full adds the scale of the 2021 exercise — about **750 000** contracts, with earlier exercises in 2005 and 2017.

11. **The *Kapitalwahlrecht* notice period was not established** at any carrier, including from the
    GDV's own consumer page on payout options [R21]. The brief asked for it specifically.
    Downstream it is `[std]`.

    **Status 2026-08-30: CLOSED, from the AVB rather than from [R21].** [S4] § 2 Abs. 2–3 requires the application *"wenigstens drei Jahre vor Rentenzahlungsbeginn"* where the payout phase carries no death cover, and otherwise not before the twelfth policy year or five months before the first annuity date; [S8] § 1 Abs. 2 ties it to the twelve-year line; [S14] § 2 Abs. 7 asks two months. [S1] § 1 Abs. 2 leaves the period to the carrier and notes that § 309 Nr. 13 BGB forbids requiring more than *Textform*.

12. **§ 169 VVG paragraphs 3 to 5 were not read.** § 165 VVG's text refers to them [R2], which
    establishes that they carry the calculation rules for both the surrender value and the paid-up
    value; their content — including the five-year spreading of *Abschluss- und Vertriebskosten* —
    is `[unverified]`. No *Stornoabzug* percentage, surrender-value table or charge-recovery
    schedule was established at any carrier, and what the *classic* (as against unit-linked)
    surrender value is computed as, at article level, is likewise unestablished.

    **Status 2026-08-30: CLOSED.** § 169 Abs. 3 to 5 read at article level. Abs. 3 Satz 1 carries the five-year spreading and the *Höchstzillmersätze* reservation; Abs. 5 the three conditions and the voidness of a deduction for unamortised acquisition costs. The classic surrender value is the *Deckungskapital* on the premium bases at the end of the current insurance period. **Four carrier *Stornoabzug* practices are now known and they disagree** — none [S8] [S9], a flat 250 EUR [S4], tapering percentages [S11] — so the earlier inference that Abs. 5 requires a flat, duration-free deduction is withdrawn.

13. **The premium, duration and age envelope is entirely unestablished.** Minimum and maximum
    premium; single- versus recurring-premium market split; minimum and maximum *Aufschubdauer*;
    minimum and maximum entry age; minimum and maximum *Rentenbeginn* age. None was returned at
    any carrier. Every issue rule in the delib product-spec will be `[std]`.

    **Status 2026-08-30: stands.** No retrieved document publishes a premium, duration or age envelope. Fragments only: a *Mindestbeitrag* scale of 10 / 15 / 30 / 60 EUR by payment frequency and a maximum *Rentenbeginnalter* of 85 at [S4]; the same maximum at [S8]; a minimum partial payout of 2 500 EUR at [S4].

14. **No charge parameter was established for this product at any carrier** — not the *Abschluss-
    und Vertriebskosten* rate, the *Höchstzillmersatz*, the *Verwaltungskosten* in any form, the
    *Ratenzahlungszuschlag*, the payout-phase administration charge, or the *Effektivkosten*. The
    only two figures in the corpus — an Abschlussprovision of 1 575 € and a maximum of 0,95 € per
    100 € of capital formed — come from third-party analyses of an Allianz specimen quotation for
    **Schicht-1 and Schicht-2** variants [S13] [R23] and are `[unverified]` as Schicht-3 levels.
    No *Produktinformationsblatt* and no *Basisinformationsblatt* (PRIIP-KID) for a classic
    deferred annuity appears in the corpus at all, although the brief listed both as target
    document types.

    **Status 2026-08-30: stands, and is now known to be structural.** No retrieved wording publishes a charge level. All four AVB refer the amounts to the *Kostenausweis nach § 2 VVG-InfoV* or the *Persönlicher Vorschlag* [S1] § 14 Abs. 1, [S4] § 11 Abs. 1, [S8] § 8 Abs. 1, [S9] § 16 Abs. 1 — documents that are per-contract and not public. **The two figures the gap cites got worse, not better**: [R23] is paywalled and [S13] does not carry them, so neither is established by any retrieved document. What *is* established is the charging mechanism and its statutory ceiling, § 4 Abs. 1 Satz 2 DeckRV [R7].

15. **The *Zuzahlung* was not established at all, and the *Dynamik* only as a heading.** The Zurich
    pack contains "Besondere Bedingungen für die Anpassungsversicherung in der Rentenversicherung"
    [S4], which establishes that the option exists and has its own condition set — and nothing
    about its percentage, its basis, its underwriting or its termination rules. No source named
    the *Zuzahlung*. The brief asked for both.

    **Status 2026-08-30: half closed.** The *Dynamik* is now read in full — [S4] pp. 19–20, *Besondere Bedingungen für die Anpassungsversicherung*, six §§: a fixed percentage on the previous year's premium at each policy anniversary until the end of the premium-paying term, benefits re-priced on the inception bases or, with notice, on current ones, opposable within three months and suspendable at will. The ***Zuzahlung*** is named at [S4] § 10 Abs. 3 and [S9] § 16 Abs. 2 as a top-up whose acquisition costs are taken at once, but no amount, limit or frequency is given.

16. **The *Beitragsverrechnung* surplus system was not established for this product.** Three
    systems are evidenced [R24] [S12]; the fourth, in which surplus is set against the premium
    due, was not named by any summary. Its absence here is a gap in the corpus, not evidence that
    it does not exist.

    **Status 2026-08-30: CLOSED.** *Beitragsverrechnung* is [S4] § 3 Abs. 6, where surpluses are set against the premium due and any excess paid out as a *Barausschüttung*, available only within a *Rückdeckungsversicherung*. [S15] adds *Erlebensfallbonus* and *Bonussumme* as further accumulation-phase forms.

17. **The four-component surplus decomposition is only one-quarter established.** The
    *Zinsüberschuss* is established from its definition — surplus arises when investment income
    exceeds the *Rechnungszins* [R24]. The *Risikoüberschuss*, the *Kostenüberschuss* and the
    *Schlussüberschussanteil* were **not** named by any summary. They are the primary subject of
    the delib `kapitallebensversicherung` file, which shares this chassis; anything about them
    here must cite that file or be `[unverified]`.

    **Status 2026-08-30: CLOSED for this product.** [S8] § 2 names all three sources and their MindZV minima — *"Erträge der Kapitalanlagen"* at *"grundsätzlich 90 Prozent"*, the *Risikoergebnis* at 90 %, the *übriges Ergebnis* at 50 %. [S4] § 3 Abs. 4–5 names the *Grundüberschussanteil*, the *Beitragsüberschussanteil* and the *Schlussüberschussanteil* with their *Bezugsgrößen*. [S15] declares them separately.

18. **Death-benefit timing, composition and post-*Rentenbeginn* refund are unestablished.**
    Whether the benefit falls at the date of death or the next policy anniversary; whether the
    with-surplus *Beitragsrückgewähr* includes the whole *Ansammlungsguthaben*; whether the
    classic product uses the `max(Deckungskapital, premiums paid)` form the unit-linked wording
    uses [S19]; and, separately, the ***Beitragsrückgewähr in der Rentenbezugsphase*** — the
    refund of premiums less annuity instalments on death after *Rentenbeginn*, which the brief
    asked for and which **no source in this corpus mentions**. It must not be asserted downstream.
    What *is* established for post-*Rentenbeginn* death is the *Rentengarantiezeit* [R24] and the
    survivor's-annuity rider [S10].

    **Status 2026-08-30: CONTRADICTED in its most important limb.** ***Beitragsrückgewähr in der Rentenbezugsphase* is in the corpus**: [S4] § 1 Abs. 5 offers it as an alternative to the *Rentengarantiezeit* — premiums paid less rider premiums and less annuities already received at their inception-guaranteed level, the claim lapsing once instalments exceed premiums — with § 2 Abs. 7 allowing it to be increased at the *Rentenbeginn* and § 3 Abs. 7 accumulating the attributable surplus at interest. The `max(Deckungskapital, premiums paid)` form is also established for a **classic** product, [S9] § 1 Abs. 3. Timing is on death, with the *Bewertungsreserven* struck for the month of or before notification [S15]. **The reference model still pays no post-*Rentenbeginn* death benefit; that is now a known omission and is recorded as one in `model.md`.**

19. **The annuity payment timing was not established.** Every source describes the annuity as
    monthly [S13] [R24]; **none states whether it is payable in advance or in arrears**. This is a
    first-order modelling parameter — it moves the annuity value by roughly half a month's
    interest and shifts every payout cash flow by one period. The model must adopt
    monthly-in-advance as an explicit `[std]` convention and state this gap beside it.

    **Status 2026-08-30: CLOSED at one carrier.** [S9] § 1 Abs. 1: *"Wir zahlen die Rente monatlich, jeweils zum Monatsersten"* — monthly in advance. [S1] § 1 Abs. 1 leaves the frequency to agreement, yearly to monthly. What the model standardizes is the annual-grid compression, not the basis.

20. **No behavioural assumption is evidenced.** No lapse rate, no *Beitragsfreistellung* rate, no
    *Kapitalwahlrecht* take-up rate, no market *Stornoquote*, no annuitisation-versus-lump-sum
    split. All are `[std]` and all are the modeller's view.

    **Status 2026-08-30: stands.** No retrieved document publishes a lapse rate, a *Beitragsfreistellung* rate, a take-up rate or a *Stornoquote*. All remain `[std]` and the modeller's view.

21. **The sex-distinct table / unisex tariff pairing was not established at either end.** No
    summary confirmed that DAV 2004 R is published sex-distinctly, and no search touched the ECJ
    *Test-Achats* judgment, the German unisex application date, or the AGG. Both halves are
    `[unverified]` here; the unisex rule belongs to the delib cross-product reference library and
    must be cited from there.

    **Status 2026-08-30: half closed.** [S11] § 52 Abs. 1 and § 28 Abs. 2 name *unternehmenseigene **geschlechtsunabhängige** Sterbetafeln*, which is the unisex rule visible in a tariff. That DAV 2004 R is published sex-distinctly is still `[unverified]` here; *Test-Achats* and the AGG belong to the cross-product library.

22. **The *Mindestversicherungsleistung* threshold for *Beitragsfreistellung* was not
    established.** § 165 VVG makes the paid-up right conditional on it [R2] and no carrier's
    threshold was returned. It is a tariff parameter and will be `[std]`.

    **Status 2026-08-30: CLOSED as to level, with the point that it is contractual.** § 165 VVG makes the right conditional on the *vereinbarte* minimum; three carrier levels are on the record — **25,00 € a month** [S4] footnote 1 and [S9] § 1 Abs. 1, **600,00 € a year** for a partial surrender [S8] § 7 Abs. 2. The model's 30,00 € is unchanged and stays `[std]`.

23. **The tax picture is incomplete beyond the two regimes.** Not established: the rate at which
    the taxable half of a *Kapitalabfindung* is charged (personal rate or flat rate), the
    *Solidaritätszuschlag*, the inheritance-tax treatment of the death benefit, and the
    *Kleinbetragsrente* commutation threshold. The two regimes themselves — § 22 EStG
    *Ertragsanteil* [R5] and § 20 EStG *Halbeinkünfteverfahren* under 12/62 [R6] — are
    well-corroborated.

    **Status 2026-08-30: narrowed.** [S4]'s *Allgemeine Steuerhinweise* add: the *Kapitalertragsteuer* is withheld at 25 % plus *Solidaritätszuschlag* and any *Kirchensteuer*; where the 12/62 conditions are met the half difference is assessed at the personal tariff rate with the withheld amounts credited; returns earned during the *Aufschubzeit* are not taxable; death benefits in the *Aufschubzeit* are income-tax free; and annuities continuing under a *Rentengarantiezeit* stay on the *Ertragsanteil* basis. Inheritance tax and the *Kleinbetragsrente* threshold are still unestablished, although [S8] § 7 Abs. 3 and [S14] § 2 Abs. 3 both key the threshold to § 93 Abs. 3 EStG.

24. **The corpus is carrier-thin and skewed to withdrawn products.** Nine carriers appear, of
    which **two — Allianz and Debeka — are evidenced principally by the products that replaced the
    classic tariff** [S12] [S13] [R22] [R23], and one — DEVK — appears only through a unit-linked
    document [S19]. The variation tables therefore describe **structural** variation reliably and
    **parameter** variation not at all.

    **Status 2026-08-30: stands, and one entry moved.** [S11] is now known to be the *Fondskomponenten* successor design rather than a classic AVB, so Debeka is evidenced **only** by replacement products; [S14] is a hybrid; [S18] is a Schicht-2 *Direktversicherung*; [S19] is not retrievable. The classic chassis is carried by [S1], [S4]–[S7], [S8], [S9] and [S16].

25. **The GDV model conditions are non-binding and their edition history is only partly known.**
    "Diese Bedingungen sind unverbindlich" [S2]; use is optional [S3]. One edition is dated 2021
    by its file name [S2] and a sibling Riester model condition carries "Stand: 21.07.2025" [S3].
    The current edition date of the deferred-annuity model conditions themselves was **not
    established**, so nothing downstream may date [S1].

    **Status 2026-08-30: CLOSED, and the earlier dating CONTRADICTED.** Both GDV blob URLs serve one file, ***Stand: 21.07.2025***, 20 pp., twenty §§. The `2021` in the [S2] file name is not an edition date. The disclaimer reads *"Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ."* The *Hinterbliebenenrenten-Zusatzversicherung* set [S10] carries *Stand: 14.11.2019*.

26. **Living texts.** § 169 VVG was reached through a commentary version dated **1 January 2016**
    [R1]; § 165, § 163, § 153 VVG and § 22, § 20 EStG were reached without any version date at all
    [R2]–[R6]. The DeckRV amendment is established as effective **1 January 2025** [R7] [R11] and
    the DAV's recommendation extends the 1,0 % rate to **2026** [R8]. The DAV 2004 R derivation
    guideline was reissued **28 June 2023** [R12]. Zurich's current pack is **Fassung 01/2026**
    [S4]; the Konzern Versicherungskammer declaration is **2026** [S15]; a Debeka AVB sibling is
    dated **1 July 2026** [S11]. **Check every article number and every figure for later amendment
    before relying on it.**

    **Status 2026-08-30: versions now attached.** VVG §§ 153, 163, 165, 169 and 21 read at *Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*; EStG §§ 20, 22 and 52 at *Art. 7 G v. 29.6.2026 I Nr. 197*; DeckRV §§ 2 and 4 at *Art. 1 V v. 19.7.2024 I Nr. 250*. Document editions: GDV 21.07.2025 and 14.11.2019, Zurich 07/2015, 01/2025 and 01/2026, NÜRNBERGER GN331451_202501, Cosmos LA 904 A (01.17), Debeka B LV 85 (01.07.2026), Mecklenburgische 07.2025, Bayern-Versicherung 2026. **Five of the URLs in this file are living paths whose file names no longer match their contents** ([S2] [S5] [S7] [S11] [S16]), which is a caveat the original register did not anticipate.
