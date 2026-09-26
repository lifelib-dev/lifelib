# Fondsgebundene Rentenversicherung — research notes (Germany)

Research notes for the German **unit-linked deferred private annuity** — *fondsgebundene
Rentenversicherung* (FRV), the contract in which the accumulating capital is not a
*Deckungskapital* in the insurer's general account but a holding of *Anteileinheiten* (units) in
*Investmentfonds* selected by the policyholder, so that **the insurer guarantees the number of
units and not their value**; in which every charge is taken by cancelling units or by withholding
premium before units are bought; and in which the single hard guarantee given at inception is the
*Rentenfaktor* — a number of euro of monthly annuity per 10 000 € of *Fondsguthaben* — applied at
*Rentenbeginn* to whatever the fund is then worth.

This is the dominant German new-business savings form. It is also the product where the German
market's whole cost vocabulary is visible on one page, because PRIIPs forces it there: a
fondsgebundene contract has no *Rechnungszins* to hide charges inside, so the charge stack, the
fund's own *TER* and the *Effektivkosten* (reduction in yield) are the product.

**In scope.**

- The single-life, deferred, **Schicht 3** (unsubsidised private, third-layer) unit-linked annuity
  sold to individuals against a **level recurring monthly premium** (the *Sofortrente* and the
  single-premium form are noted where they differ), with an *Aufschubzeit* ending at a
  contractually fixed *Rentenbeginn*.
- The **unit / non-unit split**: *Fondsguthaben*, *Anteileinheiten*, *Anteilspreis*, and the
  *Beitragsverrechnung* by which a gross monthly *Beitrag* becomes units.
- The **charge stack** and its German names — *Abschluss- und Vertriebskosten*, beitragsbezogene
  and kapitalbezogene *Verwaltungskosten*, *Stückkosten*, the fund *TER*, *Kickbacks* /
  *Bestandsprovision* — and the *Effektivkosten* disclosed in the *Basisinformationsblatt*.
- The **Todesfallleistung** before *Rentenbeginn* in its four observed shapes, and the
  *Risikobeitrag* levied by unit cancellation on the net amount at risk.
- The in-force **options**: *Fondswechsel* (Shift and Switch), *Ablaufmanagement*, *Zuzahlung*,
  *Teilentnahme*, *Beitragsfreistellung*, *Beitragsdynamik*, *Kapitalwahlrecht*, the *Abrufphase*.
- The **Rentenfaktor** at *Rentenbeginn*, the guaranteed-versus-current comparison, and the
  *Treuhänder* adjustment clause.
- ***Rückkaufswert*** as a *Zeitwert* under § 169 VVG, *Storno* and the *Stornoabzug*.
- Taxation of the *Rentenphase* and of the *Kapitalwahlrecht*, and the accumulation-phase tax
  deferral that is the product's principal selling argument against a direct fund holding.

**Out of scope, and named here so the boundary is explicit.**

- **Hybrid and guarantee designs** — *statische* and *dynamische Hybride*, *Zwei-* und
  *Drei-Topf-Hybride*, **i-CPPI**, *Wertsicherungsfonds* — are named in section 13 and are
  **deliberately not implemented**. They are this same unit-linked chassis wrapped in a
  path-dependent reallocation rule whose whole content is a guarantee mechanism, and a
  deterministic projection cannot demonstrate one honestly because the rule only does anything
  along paths the projection does not generate. Section 13 says what would have to be added.
- **Indexgebundene Rentenversicherung / "Neue Klassik"** — delib `indexpolice`. A general-account
  product with an *Indexpartizipation* bought out of the surplus, not a unit-linked one.
- **Fondsgebundene Basisrente (Rürup)** and **fondsgebundene Riester-Rente** — delib `basisrente`
  and `riester_rente`, with their own subsidy, guarantee and payout rules. The Riester form is the
  reason i-CPPI was built in Germany at all, because Riester carries a **statutory 100 %
  *Beitragsgarantie***.
- **bAV**: *fondsgebundene Direktversicherung*, *Pensionskasse*, *Pensionsfonds*. Out of the
  library. **Fondsgebundene Kapitallebensversicherung** and **fondsgebundene Risikoversicherung**
  share the accumulation mechanics and differ only in the terminal event.
- **Sofortbeginnende fondsgebundene Rentenversicherung** — delib `sofortrente` owns the payout
  phase. This file carries it only as far as the *Rentenfaktor* conversion.
- **Nettopolicen / Honorartarife** are in scope as a **charge variant**, not a separate product;
  they bracket the *Effektivkosten* range from below.
- **Fondssparpläne, ETF-Sparpläne and Fondsdepots** are not insurance and are out of scope, but
  they are the competitor and the reason the tax-deferral argument of section 16 exists.

These notes are the citation ground truth for the delib `fondsgebundene_rentenversicherung`
product documents: source ids **S1..S18** and **R1..R26** below are **frozen — never renumber**.
Unused ids are simply omitted downstream, leaving gaps, and `sources.md` records which ids are
absent and why.

Access date for all citations: **2026-08-29**.

---

## Citation discipline and retrieval conditions

Read this section before reading anything else in the file. It is the difference between what this
document is and what a reader will assume it is. It has two halves. The first records how the
research was **done**, on 2026-08-29, under a policy that blocked all egress; the second records
what the **re-verification** of 2026-08-30 established once that policy was lifted. The first half
is not withdrawn — it is why the entries below read as they do — and the second is what a reader
should weigh them by.

**No document listed in this file was retrieved when it was drafted, and no web search was run for
it.** Two independent limits applied, and both were absolute rather than partial.

**Limit 1 — direct HTTP egress was blocked.** An organisation network policy refuses `WebFetch` and
`curl` with HTTP 403 at the egress gateway for every host outside a short package-registry
allowlist. Every host that matters for this product was tried in the course of building this
library and every one was refused: `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
`bundesfinanzministerium.de`, `dejure.org`, `eur-lex.europa.eu`, `de.wikipedia.org`, and every
insurer host named below. **Not one PDF of a *Bedingungswerk*, not one *Basisinformationsblatt*,
not one *Produktinformationsblatt*, not one *Verbraucherinformation* was opened.**

**Limit 2 — the session's `WebSearch` budget was already exhausted when this file was begun.** The
budget of 200 calls was shared across the parallel researchers building the ten delib products and
was consumed by the regulatory research and by the products written first. Every search attempted
for this product returned the budget-exhausted response. **There was therefore no research channel
of any kind for this file** — not even the weak one (search summaries) that the
`kapitallebensversicherung` and `klassische_rentenversicherung` files had.

What follows from that, exactly, and it is applied without exception below:

1. **Every source entry was a *known reference*, not a citation of a read document.** Each recorded
   `Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)`.
   Where a document was corroborated by search **in a sibling delib research file**, that is said
   explicitly, with the sibling's own id, and the corroboration is attributed to that file rather
   than claimed here. **No entry read `Retrieved: yes` as drafted.** Three do now, and the rest of
   what the pass opened is recorded in the section that closes this file; see *What the
   re-verification established* below.
2. **No verbatim quotation is invented.** Nothing here is presented as the wording of an instrument
   or of a *Bedingungswerk*. Where German wording appears it is a **term of art**, not a quotation.
3. **No URL, document number, edition, tariff code, page count or publication date is guessed.**
   Where a URL is not available the entry says `URL: not established`. A canonical
   `gesetze-im-internet.de` form of a statutory article is marked `[unverified]`. The few URLs that
   appear were returned by searches run for the sibling files and are attributed to them.
4. **`[unverified]` is used generously.** It is applied to **every** specific paragraph number,
   effective date, monetary amount, percentage, tariff level, product name and market figure. It is
   **not** applied to the general shape of a mechanic that is common ground in German practice —
   that the *Beitrag* is reduced by charges before units are bought, that charges in force are taken
   by cancelling units, that a *Rentenfaktor* converts capital into annuity — because tagging those
   would drown the signal. **The moment a claim becomes specific and numeric, it carries
   `[unverified]` or it becomes `[std]`.**
5. **Uncertain numbers are `[std]` parameters, not citations.** Where the mechanic is certain and
   the level is not — an *Abschlusskostensatz*, a *Verwaltungskostensatz*, a *Rentenfaktor*, a
   *Stornoquote*, a fund return — this file ships a **`[std]` value with a stated rationale and an
   argued plausible range**, and says on what arithmetic the value rests. A `[std]` number is
   honest; a `[S4]` number that no one read is not. The gaps register records every figure that had
   to be handled this way, and it is most of them.

**What the re-verification established.** The policy was lifted, and on **2026-08-30** the citations
were checked against the primary documents. Library-wide, all fifteen German instruments delib cites
were read as canonical XML from `gesetze-im-internet.de` with each law's amendment `Stand` recorded,
950 statutory section references were checked and 950 were correct, and insurer AVB,
*Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read; **501 of
the library's 805 source entries, 62 %, now read `Retrieved: yes`.** For this product the pass is
recorded in full in ***Retrieval pass, 2026-08-30*** at the foot of this file: the DEVK
*Kundeninformation* and the sixteen *Basisinformationsblätter* bound into it, VVG, VVG-InfoV,
DeckRV, MindZV, VAG and EStG as canonical XML, two BaFin publications and a DAV *Ergebnisbericht*.
**Read that section with the entries, because the two do not yet agree.** Only three of the 44
entries below had their own `Retrieved:` line rewritten — [S2] and [S15] to **yes**, [S16] to
**partly** — and the remaining 41 still carry the drafted `Retrieved: no` even where the pass table
records the document as read. **Where they conflict the pass section governs and the entry's line
does not.**

**What an entry now means.** A **`Retrieved: yes`** line, or a row in the pass table, means the
document was opened and the passage the entry rests on was read. Everywhere else the citation is
still **a pointer rather than a certificate**: it names the instrument a claim should be checked
against, not a document anyone checked. **The re-verification changed things** — seventeen findings
that contradict the drafted text are listed under *What a retrieved document contradicted*, and
they include the mortality basis, the guaranteed *Rentenfaktor* level and the PRIIPs category.
Treat a claim in this file as sound where a retrieved document backs it, and as provisional where
none does.

**The consequence for the reader.** The **mechanics** in sections 1–18 are the load-bearing part of
this file and the part that never depended on having a PDF open. They are written long and precise
and they are correct as descriptions of German market practice, subject to the corrections the pass
recorded. The **levels** were not sourced at drafting and are not presented as if they were; the
pass supplied a few and the gaps register says which.

---

## German terminology

German terms of art stay in German throughout the delib documents, italicised on first use with a
gloss, per the library's house rules. This product carries the largest vocabulary of the ten, and
much of it has no clean English equivalent because the German market invented the concepts.

| Term | Gloss |
|---|---|
| *Fondsguthaben* | fund credit — the euro value of the policy's units at a valuation date; the account value |
| *Anteileinheiten* / *Anteile* | units; the quantity the insurer guarantees, as distinct from their value |
| *Anteilspreis* / *Anteilwert* | unit price; the fund's *Rücknahmepreis* (redemption price) at the *Bewertungsstichtag* |
| *Bewertungsstichtag* | valuation date on which units are bought, cancelled or valued |
| *Beitragsverrechnung* | the allocation of a gross premium: which deductions are taken, in what order, before the remainder buys units |
| *Anlagebeitrag* / *Sparbeitrag* | the part of the premium that actually buys units, after charges and the *Risikobeitrag* |
| *Risikobeitrag* | risk premium: the charge for the death cover, levied on the *riskiertes Kapital* |
| *riskiertes Kapital* | net amount at risk: death benefit less *Fondsguthaben*, floored at zero |
| *Abschluss- und Vertriebskosten* | acquisition and distribution costs — commission, underwriting, issue |
| *Zillmerung* / *Höchstzillmersatz* | financing acquisition costs against future premiums / the statutory cap on the costs so financed |
| *Verwaltungskosten* | administration charges; split into *beitragsbezogen* and *kapitalbezogen* |
| *beitragsbezogene Kosten* | premium-based charge: a percentage of each gross premium (actuarial *β*-Kosten) |
| *kapitalbezogene Kosten* / *Gammakosten* | fund-based charge: a percentage per annum of the *Fondsguthaben* (actuarial *γ*-Kosten) |
| *Stückkosten* | per-policy fixed charge, a euro amount per month or per year regardless of premium size |
| *TER* (*Gesamtkostenquote*) | the fund's own total expense ratio, borne inside the unit price and invisible in the policy ledger |
| *Kickback* / *Bestandsprovision* | trail commission paid by the fund company to the insurer out of the TER, and normally credited back to the contract |
| *Effektivkosten* / *Effektivkostenquote* | reduction in yield (RIY): all charges expressed as the annual percentage by which they reduce the contract's return |
| *Basisinformationsblatt* (BIB) | the PRIIPs key information document (PRIIP-KID) |
| *Modellrechnung* | the statutory illustration of maturity values at prescribed assumed returns |
| *Beitragsrückgewähr* | return of premiums: a death benefit of at least the premiums paid |
| *garantierte Mindesttodesfallleistung* | a guaranteed minimum death benefit above the fund value |
| *Aufschubzeit* / *Aufschubdauer* | deferment period, inception to *Rentenbeginn* |
| *Rentenbeginn* | annuity commencement date; the boundary at which the fund is converted |
| *Abrufphase* | the window inside which the policyholder may bring the *Rentenbeginn* forward or defer it |
| *Rentenfaktor* | annuity factor: euro of monthly annuity per 10 000 € of capital at *Rentenbeginn* |
| *garantierter* / *aktueller Rentenfaktor* | the factor guaranteed at inception / the factor on the insurer's tariff at *Rentenbeginn* |
| *Treuhänder* / *Treuhänderklausel* | independent trustee / the clause permitting an adjustment of contract terms with the trustee's approval |
| *Rentengarantiezeit* | guaranteed annuity period: instalments continue to the beneficiary if the annuitant dies inside it |
| *Kapitalwahlrecht* | the option to take the capital as a lump sum instead of an annuity |
| *Fondswechsel* (*Shift* / *Switch*) | fund change: reallocating the existing *Fondsguthaben*, and/or redirecting future premiums |
| *Ablaufmanagement* | automatic phased de-risking of the fund holding in the years before *Rentenbeginn* |
| *Zuzahlung* | an additional single premium paid into an existing contract |
| *Beitragsdynamik* | contractual annual increase of the premium, with a corresponding benefit increase |
| *Beitragsfreistellung* | conversion to a paid-up contract; premiums cease, the fund stays invested |
| *Rückkaufswert* | surrender value |
| *Zeitwert* | current value: the § 169 VVG basis for a fondsgebundene surrender value |
| *Stornoabzug* | surrender deduction |
| *Überschussbeteiligung* | profit participation; in an FRV it arises from risk and cost results, not investment return |
| *Sicherungsvermögen* | the insurer's segregated general-account assets — where a hybrid's guaranteed pot sits |
| *Wertsicherungsfonds* | a fund with a contractual limit on its loss over a period, used as the middle pot of a three-pot hybrid |
| *Beitragsgarantie* | premium guarantee: the percentage of premiums paid guaranteed to be available at *Rentenbeginn* |
| *Ertragsanteil* | the taxable fraction of an annuity instalment under § 22 EStG |
| *Teilfreistellung* | the partial exemption of fund income under the *Investmentsteuergesetz* |

---

## Primary sources

Eighteen known references to primary product documents. **As originally drafted, none was
retrieved and none was corroborated by a search run for this file** (see the retrieval-conditions
section, which carries both the conditions this file was written under and what the re-verification
established). **A retrieval pass on 2026-08-30 changed that for three of the eighteen** — [S2] and, inside it,
[S15] and the *Verbraucherinformation* limb of [S16] — and opened a marketing page for [S3]. The
per-entry notes below are annotated where the pass changed what an entry establishes, and the
full result is set out in *"Retrieval pass, 2026-08-30"* at the end of this file. The remaining
fourteen still say `URL: not established`, and for those the entry's original wording stands.

Each entry answers two questions honestly: **does a document of this kind exist for this product,
and what does that kind of document establish?** Where a product name or tariff code is given
without a retrieval note it is tagged `[unverified]` — the author's recollection of the German
market, not a search result.

### S1 — GDV, Musterbedingungen for the fondsgebundene Rentenversicherung

- Publisher: Gesamtverband der Deutschen Versicherer e. V. (GDV)
- Doc type: *Musterbedingungen* — non-binding model policy conditions from which member insurers
  derive their own *Allgemeine Versicherungsbedingungen* (AVB)
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted). The
  **document type** is established indirectly: the sibling delib research on
  `klassische_rentenversicherung` corroborated by search both the GDV *Musterbedingungen* service
  index and a model-conditions set for the *Rentenversicherung mit aufgeschobener Rentenzahlung*. A
  companion set for the **fondsgebundene** form is the ordinary structure of that index; **its
  title, edition and clause numbering are `[unverified]`.**
- Content: a GDV *Musterbedingung* is **the skeleton every German insurer's AVB for the line
  follows**, clause order included, which is why insurer wordings are structurally interchangeable
  even where the numbers differ. The clauses a model needs, in their usual order: the benefits; the
  *Beitragsverrechnung* and the purchase of *Anteileinheiten* at the *Anteilspreis* on a
  *Bewertungsstichtag*; the determination of the *Fondsguthaben*; death before and after
  *Rentenbeginn*; the *Rentenfaktor* rule; *Fondswechsel*, *Zuzahlung*, *Teilentnahme*,
  *Beitragsfreistellung* and *Kündigung*; the *Rückkaufswert* and any *Stornoabzug*; the
  *Überschussbeteiligung*; the *Anpassungsklausel*. **No clause text and no numeric parameter is
  established.** This entry stands for the existence of a market-standard clause inventory, not as
  authority for any clause's content.

### S2 — DEVK, "Kundeninformation zur Fondsgebundenen Rentenversicherung", document 03101, edition 07/2024

- Publisher: DEVK Lebensversicherungsverein a. G.
- Doc type: *Kundeninformation* — the consolidated pre-contractual customer information document
  for a unit-linked annuity, carrying the AVB, the *Produktinformationsblatt* content and the
  consumer information in one file
- URL: `https://medien.devk.de/assets/content/download/produkte/altersvorsorge-leben/devk-fondsrente-kundeninfo-03101-2024-07.pdf`
  — **this URL was returned by a search run for the sibling delib research on
  `klassische_rentenversicherung` and is recorded there as its S19.** It is not a search result of
  this file's own.
- Retrieved: **yes, on 2026-08-30** (PDF, 195 pp.). *As drafted:* "no — egress blocked;
  corroborated by search in the sibling file only, not here." The `medien.devk.de` address above
  answers **HTTP 403** from its object store; the same file is served under the publisher's own
  path at
  `https://www.devk.de/media/content/download/produkte/altersvorsorge/DEVK-Fondsrente-Kundeninfo-03101-2024-07.pdf`,
  and that is where it was read.
- Content: **this is now the load-bearing document of the whole corpus, and the single fact it was
  cited for is confirmed verbatim.** § 2 Abs. 7 AVB: *"Die Todesfallleistung ist das zum Stichtag
  bei Tod … vorhandene Fondsguthaben, mindestens aber die ➜ Summe der gezahlten Beiträge
  (Beitragsrückgewähr)."* The document code **03101** and the edition **07/2024** are confirmed on
  the document itself, together with the tariff **L/N FR1**, the product name **"DEVK-Fondsrente
  vario"**, the AVB *Stand* January 2024 and the *Tarifbestimmungen* *Stand* July 2023. The
  sentence "Nothing else about the DEVK contract … is established" is **no longer true**: the
  charges, the *Rentenfaktor* values, the fund range, the option set and the entry rules are all
  in the file, and the *Basisinformationsblätter* are bound into it at pp. 71–119. The full
  extraction is set out at *"Retrieval pass, 2026-08-30"*, and the product documents' citations
  to it are the operative record.

### S3 — Allianz Lebensversicherungs-AG, AVB and *Verbraucherinformation* for the fondsgebundene Rentenversicherung ("InvestFlex")

- Publisher: Allianz Lebensversicherungs-AG, Stuttgart — the German market leader in life
- Doc type: *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung*, with the matching
  *Verbraucherinformation*, *Produktinformationsblatt* and *Basisinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the market leader sells its unit-linked annuity under the name **"InvestFlex"**
  `[unverified]`, within the *PrivatRente* family whose classic and index members the sibling
  delib research covers. Recorded because **a representative German FRV design has to be checkable
  against the largest writer's wording**, and because Allianz is the carrier at which the
  *Treuhänderklausel* dispute over the *Rentenfaktor* was publicly live in 2021 [R22]. **No
  clause, charge, factor or age limit of this contract is established here.**

### S4 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Fondsgebundene Versicherungen"

- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation* — a consolidated pre-contractual information document issued
  per product family and per *Fassung*, typically 40–50 pages
- URL: not established for the fondsgebundene series. The sibling delib research corroborated the
  **companion** series, "Verbraucherinformation für **Konventionelle** Versicherungen —
  Aufgeschobene Rentenversicherung", in four editions.
- Retrieved: no — egress blocked; no search corroboration for the fondsgebundene series
- Content: the corroborated companion's title — "für **Konventionelle** Versicherungen" — is itself
  the evidence that **a parallel fondsgebundene series exists at the same carrier**: a document that
  has to name itself "conventional" does so to distinguish itself from the unit-linked one. That is
  recorded as an inference; the parallel document's title, edition and content are `[unverified]`.
  The **document type** is why the entry is here: a *Verbraucherinformation* of that length states
  in one place the benefit definitions, the *Beitragsverrechnung*, the cost clauses, the
  *Rentenfaktor* rule, the option catalogue and the *Rückkaufswert* rule — the exact inventory a
  product-spec needs. The sibling's corroborated Zurich material also establishes the conventional
  carrier's **factor rule at *Rentenbeginn*** — a second factor is compared with the guaranteed one
  and **the higher of the two applies** — carried over in section 9 as market practice, tagged to
  the sibling's evidence rather than to a fondsgebundene document.

### S5 — Alte Leipziger Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung

- Publisher: Alte Leipziger Lebensversicherung a. G., Oberursel
- Doc type: *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung* plus *Tarifblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: a large mutual understood to offer both a commission tariff and a **Nettotarif** on the
  same unit-linked chassis `[unverified]` — the pairing that isolates what *Abschlusskosten* do to
  the *Effektivkosten*, which is why the carrier is listed. **No tariff code, charge rate, fund
  list or factor is established.**

### S6 — LV 1871, AVB for the fondsgebundene Rentenversicherung ("MeinPlan")

- Publisher: Lebensversicherung von 1871 a. G., München
- Doc type: AVB, *Produktinformationsblatt*, *Basisinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: a mid-sized specialist selling its unit-linked pension as **"MeinPlan"**
  `[unverified]`, with an ETF-capable *Fondsauswahl* and a *Nettotarif* variant `[unverified]`.
  Listed as a comparator on the **option catalogue** — *Zuzahlung*, *Teilentnahme*, flexible
  *Rentenbeginn* — the dimension on which German unit-linked contracts differ most. **No parameter
  is established.**

### S7 — Stuttgarter Lebensversicherung a. G., AVB for a hybrid fondsgebundene Rentenversicherung ("FlexRente performance-safe")

- Publisher: Stuttgarter Lebensversicherung a. G.
- Doc type: AVB for a **hybrid** unit-linked annuity, plus *Basisinformationsblatt*
- URL: not established. The sibling delib research corroborated a different Stuttgarter document
  ("Allgemeine Informationen zu einem Altersversorgungssystem"), establishing only that the
  carrier publishes pre-contractual information PDFs.
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the **hybrid comparator**. The guarantee-bearing unit-linked pension is marketed as
  **"FlexRente performance-safe"** `[unverified]`, a *dynamisches Hybrid* of the section 13 family
  in which premium and capital are reallocated periodically between the *Sicherungsvermögen*, a
  *Wertsicherungsfonds* and free funds to secure a chosen *Beitragsgarantie*. It is listed to make
  the point that **delib's no-guarantee chassis is a real market form, not a simplification of the
  only form sold** — the guarantee is an option with a price. **No reallocation rule, guarantee
  level or charge is established.**

### S8 — Volkswohl Bund Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung

- Publisher: Volkswohl Bund Lebensversicherung a. G., Dortmund
- Doc type: AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: a broker-channel carrier associated with **two-pot hybrid** designs sold alongside a
  pure fondsgebundene tariff `[unverified]`. A second hybrid comparator, so that section 13's
  taxonomy rests on more than one named carrier. **No parameter is established.**

### S9 — WWK Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung with i-CPPI guarantee

- Publisher: WWK Lebensversicherung a. G., München
- Doc type: AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the German carrier most closely identified with the **i-CPPI** implementation of a
  unit-linked guarantee, marketed under a *Protect* name `[unverified]`. It is **not** on the
  insurer list in this file's brief and is named from general knowledge rather than any search
  result; that is stated rather than hidden. Listed because section 13 must name each of the three
  guarantee technologies against a real carrier, and because the i-CPPI form's exclusion needs the
  most explicit justification. **No algorithm, multiplier, floor or charge is established.**

### S10 — Cosmos Lebensversicherungs-AG (CosmosDirekt), AVB for the fondsgebundene Rentenversicherung

- Publisher: Cosmos Lebensversicherungs-AG (Generali group), Saarbrücken; sold direct as
  CosmosDirekt
- Doc type: *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung*
- URL: not established. The sibling delib research corroborated by search the **classic** Cosmos
  AVB, tariff **LA 904 A** (its S8), together with that document's statement that the annuity
  factor fixed at inception rests on a recognised mortality table (**currently DAV 2004 R**) and
  an underlying interest rate of **currently 0 percent p.a.**
- Retrieved: no — egress blocked; no search corroboration for the fondsgebundene tariff
- Content: recorded for two reasons. First, as the **direct-writer cost comparator**: a
  no-commission direct channel is the low end of the *Effektivkosten* range and bounds it from
  below along with the *Nettotarife*. Second, because the sibling's corroborated statement of the
  **conversion basis — DAV 2004 R at 0 % p.a.** — is the single most useful number in the delib
  corpus for calibrating a *garantierter Rentenfaktor*, and section 9 uses it as the basis of the
  `[std]` factor. That statement is about the carrier's **classic** tariff; applying it to the
  fondsgebundene tariff is an inference, and it is tagged as one wherever it is used.

### S11 — NÜRNBERGER Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung

- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: AVB with a tariff code in the *NIR*/*N*-series, plus *Verbraucherinformation*
- URL: not established. The sibling delib research corroborated the classic NÜRNBERGER AVB under
  **tariff NIR3301**, establishing the carrier's document naming convention.
- Retrieved: no — egress blocked; no search corroboration for the fondsgebundene tariff
- Content: a full-range carrier publishing per-tariff AVB — the German pattern that makes tariff
  codes worth recording when they can be established and worth omitting when they cannot. **No
  fondsgebundene tariff code is asserted here**; inventing one is the failure mode the
  retrieval-conditions section forbids.

### S12 — Continentale Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung ("Rente Invest")

- Publisher: Continentale Lebensversicherung AG (Continentale Versicherungsverbund)
- Doc type: AVB plus *Produktinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: a broker-channel mutual whose unit-linked pension carries a *Rente Invest* name
  `[unverified]`. Recorded to widen the carrier set behind the variation section. **No parameter is
  established.**

### S13 — HDI Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung ("CleverInvest")

- Publisher: HDI Lebensversicherung AG (Talanx group)
- Doc type: AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: HDI's unit-linked pension is sold as **"CleverInvest"** `[unverified]` and is cited in
  the broker market as a **low-cost, ETF-capable** FRV `[unverified]`. A second low-cost
  comparator alongside [S10] and the *Nettotarife* of [S18]. **No charge level is established** —
  and the absence of any corroborated charge level anywhere in this corpus is gap 6.

### S14 — Debeka Lebensversicherungsverein a. G., AVB for the fondsgebundene Rentenversicherung

- Publisher: Debeka Lebensversicherungsverein a. G., Koblenz
- Doc type: *Bedingungswerk* in the carrier's `B LV` series
- URL: not established. The sibling delib research corroborated several Debeka *Bedingungswerke*
  (**B LV 85**, **B LV 86**, **B LV 97**) and the trade-press report that Debeka **discontinued
  its classic annuity tariff**.
- Retrieved: no — egress blocked; no search corroboration for the fondsgebundene tariff
- Content: recorded because that discontinuation, at Germany's largest life mutual by policy
  count, is **the market-structure fact that puts this product at the centre of the library**:
  when the classic tariff closes, the new-business flow goes to the fondsgebundene and hybrid
  forms. The Debeka fondsgebundene *Bedingungswerk* number, edition and content are
  `[unverified]`.

### S15 — *Basisinformationsblatt* (PRIIP-KID) for a fondsgebundene Rentenversicherung — document-type entry

- Publisher: each insurer, for each *Anlageoption* / product variant
- Doc type: *Basisinformationsblatt* under the PRIIPs Regulation [R8]; three pages, prescribed
  order and prescribed headings
- URL: not established for any fondsgebundene Rentenversicherung. The sibling delib research
  located **one** German PRIIP-BIB PDF, for an **endowment** (its S10, a three-page BIB for a
  regular-premium capital-forming product), which is the wrong product but the right document type
  and confirms the three-page format.
- Retrieved: **yes, on 2026-08-30** — sixteen sheets for the DEVK-Fondsrente vario, bound into
  [S2] at pp. 71–119, with the option-specific documents from p. 120. *As drafted:* "no — egress
  blocked; no search corroboration."
- Content: **this was the document a delib product-spec most wanted and did not have; it now has
  sixteen of them.** Confirmed against the retrieved sheets: the summary risk indicator (graded
  *"Risikoklasse 2 bis 5"* here, a range because the class follows the chosen fund); the statement
  that the product carries no protection against market falls; the costs the investor bears, split
  into *Einstiegskosten*, *laufende Kosten* and *Transaktionskosten*; and the reduction in yield —
  *"Jährliche Auswirkungen der Kosten"* — at **exactly three time points, 1 year, half the
  recommended holding period and the end of it**, which on the 30-year sheet is years **1, 15 and
  30**, as this entry predicted. Two parts of the prediction are **wrong for this product**.
  **(a)** The four graded scenarios do not appear: under *"Performance-Szenarien"* the generic
  sheet for a fund-menu product states only that performance follows the chosen funds and refers
  to the option-specific documents — the multi-option treatment under the RTS. The [R9] article
  that described the four-scenario table is itself now a 404. **(b)** No cost or RIY value was
  established here **and now several are**: at the model point matching delib's anchor cell —
  a 37-year-old, thirty annual instalments, *Aufschubzeit* 30 years — the guaranteed *Rentenfaktor*
  is **22,91 €** per 10 000 € and the reduction in yield at 30 years is **1,4 %–3,4 % p.a.**
  Gap 5 is closed for one carrier; see *"Retrieval pass, 2026-08-30"*.

### S16 — *Produktinformationsblatt* / *Verbraucherinformation* — document-type entry

- Publisher: each insurer
- Doc type: the German pre-contractual information set required by § 7 VVG together with the
  *VVG-Informationspflichtenverordnung* [R7]
- URL: the *Verbraucherinformationen* limb at
  `https://www.devk.de/media/content/download/produkte/altersvorsorge/DEVK-Fondsrente-Kundeninfo-03101-2024-07.pdf`,
  pp. 4–8. No *Produktinformationsblatt* URL was established.
- Retrieved: **partly, on 2026-08-30** — the *Verbraucherinformation* limb yes; the
  *Produktinformationsblatt* limb (DEVK calls it the *Informationsblatt zu
  Versicherungsprodukten*) **no**, and § 18 Abs. 1 AVB refers the charge levels precisely to it.
- Content: the second document class a product-spec needs. The statutory duties are read at [R7]:
  § 2 Abs. 1 Nr. 1 with Abs. 2 VVG-InfoV requires the *einkalkulierte Abschlusskosten* **in euro
  as a single total amount** and the other costs as a share of the annual premium; Nr. 7 adds a
  fondsgebundene-specific duty to describe the underlying funds and their asset types; Nr. 9 with
  Abs. 6 defines the ***Effektivkosten*** — the statute's term, not *Effektivkostenquote* —
  computed *"wie der Gesamtkostenindikator nach Anhang VI der Delegierten Verordnung (EU)
  2017/653"*. The 1 January 2015 introduction remains `[unverified]`, being absent from the
  regulation's text [R13]. **What the retrieved instance actually shows is thinner than this entry
  assumed**: the standing *Verbraucherinformation* names the cost categories and then refers the
  euro amounts to the personalised quotation, and it carries **no *Effektivkosten* figure and no
  *Rückkaufswert* table**. It does establish that *"Ausgabeaufschläge und Depotkosten fallen nicht
  an"* and prices two events at 40 € each. And the ***Modellrechnung* is not owed on this product
  at all** — § 154 Abs. 1 Satz 2 VVG excludes contracts of the § 124 Abs. 2 Satz 2 VAG kind.

### S17 — *Standmitteilung* (annual statement) — document-type entry

- Publisher: each insurer; GDV publishes a model
- Doc type: *Jährliche Mitteilung zum Stand der Versicherung*
- URL: not established. The sibling delib research corroborated a **GDV Muster-Standmitteilung for
  the kapitalbildende Lebensversicherung, edition 02/2017**, establishing that the GDV publishes
  model statements per line.
- Retrieved: no — egress blocked; no search corroboration for the fondsgebundene model
- Content: the *Standmitteilung* shows **what an in-force German unit-linked policy actually
  reports**, and therefore what a model's state variables should correspond to: units held per
  fund, the *Anteilspreis* at the statement date, the resulting *Fondsguthaben*, premiums paid in
  the year, the current *Rückkaufswert*, and the projected benefit at *Rentenbeginn*. **That list
  is the delib model's state vector almost exactly.** The fondsgebundene model statement's
  existence is inferred from the corroborated endowment one and is `[unverified]`.

### S18 — Nettotarife / Honorartarife (myLife and the net variants of full-range carriers)

- Publisher: myLife Lebensversicherung AG and the *Nettotarif* variants of full-range carriers
  ([S5], [S6], [S13] and others)
- Doc type: AVB and *Basisinformationsblatt* of a commission-free tariff
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: a *Nettotarif* (also *Honorartarif*, *Nettopolice*) is **the same unit-linked contract
  with the *Abschluss- und Vertriebskosten* removed from the tariff**, the adviser being paid a fee
  by the client under a separate *Vergütungsvereinbarung*. myLife Lebensversicherung AG is the
  German carrier built entirely on that model `[unverified]`. The class matters here for one
  modelling reason: **it isolates the acquisition-cost component of the *Effektivkosten***. The
  difference between a gross tariff's RIY and the same chassis's net RIY *is* the acquisition-cost
  load — the parameter a delib worked example most needs and that no document in this corpus
  supplies. **No net-tariff or gross-tariff RIY figure is established**; the observation that the
  gap exists is structural, not numeric.

---

## Regulatory and actuarial references

Twenty-six product-specific regulatory and actuarial references. Statutory articles carry the
canonical `gesetze-im-internet.de` form of their URL **marked `[unverified]`**, because no search
in this session returned it; the form itself is a mechanical construction from the statute's
abbreviation and the paragraph number and is given so that a reader can check the claim, not as
evidence that it resolves. Where the substance of a provision was corroborated by search **in a
sibling delib research file**, that is stated and attributed.

### R1 — VVG § 169, *Rückkaufswert* — and the *Zeitwert* branch that governs this product

- Publisher: Bundesministerium der Justiz (Versicherungsvertragsgesetz 2008)
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` `[unverified]`
- Retrieved: no — egress blocked. **The substance below was corroborated by search in the sibling
  delib research on `kapitallebensversicherung` (its R2) and on `klassische_rentenversicherung`
  (its R1)**, including the German wording of the calculation rule; it is not corroborated here.
- Content, and this is the pivot of the whole product:
  - **Scope and general rule.** The article governs the claim to a *Rückkaufswert* where the
    insurance ends, in particular by *Kündigung*, *Rücktritt* or *Anfechtung*. For a conventional
    contract the value is the *Deckungskapital* computed by recognised actuarial rules on the
    ***Rechnungsgrundlagen der Prämienkalkulation*** — the pricing basis — as at the end of the
    current *Versicherungsperiode*, floored on *Kündigung* by the ***Mindestrückkaufswert***: the
    *Deckungskapital* that results when the *angesetzte Abschluss- und Vertriebskosten* are
    **spread evenly over the first five contract years**.
  - **The branch that governs delib product 3.** For ***fondsgebundene Versicherungen*** and other
    contracts providing benefits of the corresponding kind, the *Rückkaufswert* is instead **the
    *Zeitwert* of the insurance, computed by recognised actuarial rules**. The sibling's
    corroborated entry states that branch explicitly and says of it: "That branch governs delib
    product 3." The internal paragraph designation of the *Zeitwert* branch — whether it is Abs. 3
    Satz 2 or Abs. 4 — and the cross-reference it makes into the *Versicherungsaufsichtsgesetz*
    are **`[unverified]`**; the *substance* is corroborated.
  - **What the *Zeitwert* branch removes.** For a pure unit-linked contract with no insurer-given
    benefit guarantee, the *Zeitwert* is **the value of the units held** — there is no
    discounting, no mortality basis, no *Rechnungszins* and no *Zillmerung* residue in it, because
    there is no *Deckungskapital* in the general-account sense to compute. This is the single
    largest modelling simplification in the delib library: **`Rückkaufswert(t) =
    Fondsguthaben(t)`**, less a *Stornoabzug* if one is validly agreed.
  - ***Abzug* (*Stornoabzug*).** Permissible **only if *vereinbart*, *beziffert* and
    *angemessen*** — agreed, quantified in the contract, and appropriate. A deduction **for *noch
    nicht getilgte Abschluss- und Vertriebskosten* is unwirksam**, which is what prevents an
    insurer recovering through the deduction what the five-year spreading denies it.
  - **The open question** is whether the *Mindestrückkaufswert* floor reaches the *Zeitwert*
    branch at all, or whether the same protection operates through the tariff — by limiting the
    acquisition-cost deduction to one fifth per year over five years, so the units are never
    removed in the first place. **The market implements the second**, and that is what section 4
    models; which the statute requires is `[unverified]` and is gap 2.

### R2 — VVG § 168, *Kündigung* (the policyholder's termination right)

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__168.html` `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the policyholder of a life contract with recurring premiums may terminate **for the end
  of the current *Versicherungsperiode***, which on a monthly-premium contract is a short notice
  period rather than an annual one. Paired with the § 169 valuation rule [R1] it makes *Storno* on
  a German unit-linked policy a **near-frictionless exit at fund value** — which is why
  unit-linked lapse experience differs from conventional lapse experience, and why delib treats
  *Storno* and *Beitragsfreistellung* as two decrements. **Paragraph number, notice period and any
  single-premium restriction are `[unverified]`.**

### R3 — VVG § 165, *Prämienfreie Versicherung* (*Beitragsfreistellung*)

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `klassische_rentenversicherung` (its R2) and `kapitallebensversicherung` (its R3), including the
  paid-up formula for a conventional contract.
- Content: the policyholder of a recurring-premium life contract may **demand conversion to a
  paid-up contract** for the end of the current *Versicherungsperiode*. For a conventional
  contract the paid-up benefit is computed from the *Rückkaufswert* on the pricing basis. **For a
  fondsgebundene contract the mechanic is different and simpler, and this is the point section 12
  turns on**: nothing is converted. The units stay where they are, premium payment stops, the
  *beitragsbezogene* charges stop with it because there are no more premiums to charge them on,
  and the ***kapitalbezogene* charges, the *Stückkosten* and the *Risikobeitrag* continue to be
  taken by cancelling units**. A paid-up unit-linked policy therefore **decays**: on a small
  *Fondsguthaben* the fixed *Stückkosten* can consume it. Insurers accordingly set a **minimum
  *Fondsguthaben* below which *Beitragsfreistellung* is refused and the contract is surrendered
  instead** — the level is `[unverified]` and is a `[std]` parameter.

### R4 — VVG § 163, *Anpassung der Prämie* / adjustment with a *Treuhänder*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated in the sibling delib research** on
  `klassische_rentenversicherung` (its R3), where it is the statutory successor to the
  *Treuhänderklausel*.
- Content: the statutory channel through which a life insurer may adjust a contract where the
  calculation bases have changed in a way that is permanent and was not foreseeable, subject to an
  **independent trustee's confirmation** that the conditions are met. For this product it is the
  **only remaining route by which a *garantierter Rentenfaktor* can be reduced**, the contractual
  *Treuhänderklausel* being confined to older contracts [R22]. The paragraph number and the
  conditions' exact formulation are `[unverified]`.

### R5 — VVG § 153, *Überschussbeteiligung*, and the *Bewertungsreserven*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated in the sibling delib research** on
  `kapitallebensversicherung` (its R1).
- Content: the policyholder is entitled to a share of the surplus and of the *Bewertungsreserven*
  unless profit participation is excluded by express agreement. **The application to a
  fondsgebundene contract is the point worth recording**: the investment result belongs to the
  policyholder already, by construction, so the *Überschussbeteiligung* of an FRV arises from the
  **risk result and the cost result only**, and the *Bewertungsreserven* limb has almost nothing
  to attach to because the assets backing the unit liability are the units themselves. In practice
  surplus on an FRV is credited as **additional units** or as a **reduction of charges**, plus a
  *Schlussüberschuss* at *Rentenbeginn*. Whether an insurer may exclude participation altogether
  on a unit-linked tariff, and on what conditions, is `[unverified]`.

### R6 — VVG § 152, *Widerruf*, and §§ 7–8 VVG (pre-contractual information)

- Publisher: Bundesministerium der Justiz
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__152.html` ·
  `https://www.gesetze-im-internet.de/vvg_2008/__7.html` — both `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: § 7 VVG requires the terms and the *VVG-InfoV* information [R7] in text form before the
  policyholder is bound; § 152 gives a life policyholder a **cancellation period of 30 days**
  `[unverified]`. Recorded because on a unit-linked contract the amount repayable on *Widerruf* is
  tied to the **unit value at the date of cancellation**, so it is not a full premium refund after
  a market fall. The exact rule is `[unverified]`; delib does not project the window.

### R7 — VVG-InfoV § 2 — cost disclosure, the *Effektivkosten* and the *Modellrechnung*

- Publisher: Bundesministerium der Justiz (*Verordnung über Informationspflichten bei
  Versicherungsverträgen*)
- URL: `https://www.gesetze-im-internet.de/vvg-infov/__2.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `kapitallebensversicherung` (its R9), which established the heading, the statutory basis and the
  introduction date of the *Effektivkosten*.
- Content, as corroborated there and applied here:
  - § 2 VVG-InfoV is headed *Informationspflichten bei der Lebensversicherung, der
    Berufsunfähigkeitsversicherung und der Unfallversicherung mit Prämienrückgewähr* — one
    provision covering all the savings-bearing personal lines, this product included.
  - The legal basis is **§ 7 Abs. 2 und 3 VVG i. V. m. §§ 2 und 3 VVG-InfoV**, requiring disclosure
    of the ***Abschluss- und Vertriebskosten* included in the premium, in euro amounts** — not as a
    percentage, not netted into a yield.
  - The ***Effektivkostenquote* (Reduction in Yield)** was introduced in quotations **from
    1 January 2015** `[unverified]`, following the **LVRG 2014** [R13]. It discloses **all costs —
    acquisition, ongoing and investment — as a reduction of the contract's yield**.
  - **For a fondsgebundene contract the *Effektivkosten* must include the fund's own costs**, which
    is what makes the fund's *TER* a policy parameter rather than a fund parameter. The treatment of
    *Kickbacks* credited back to the contract inside the calculation is `[unverified]` (gap 8).
  - § 2 also requires a ***Modellrechnung***. The **number of assumed rates and their level** are
    `[unverified]`; the three-rate market convention is recorded in section 17 as convention.

### R8 — PRIIPs Regulation (EU) 1286/2014 and the RTS, Delegated Regulation (EU) 2017/653 as amended

- Publisher: European Parliament and Council; European Commission
- URL: not established (EUR-Lex is among the blocked hosts)
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the regulation requiring a ***Basisinformationsblatt*** for every packaged retail and
  insurance-based investment product, a fondsgebundene Rentenversicherung being the paradigm
  German IBIP. **The regulation number 1286/2014, the RTS number 2017/653 and the amending
  regulation that reworked the performance-scenario methodology from 1 January 2023 are all
  `[unverified]`** — they are recalled, not searched. The document's **content** is not in doubt,
  because BaFin's own explanation of it was corroborated in the sibling research [R9]. The RTS's
  **categorisation** — a pure unit-linked contract in **Category 2** (linear unleveraged exposure,
  scenarios from the underlying's own return history), a profit-participating or guarantee-bearing
  one in **Category 4** (values depending partly on factors not observed in the market) — is
  `[unverified]` as to the numbers but corroborated as to Category 4's existence by [R18].

### R9 — BaFin *Fachartikel*, "PRIIPs-Verordnung: Wie Versicherer Verbraucher informieren" (2022)

- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht (BaFinJournal)
- URL: `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2207_priips_surfday.html`
  — recorded in the sibling delib research on `kapitallebensversicherung` (its R19) as a search
  result; **not a search result of this file's own**
- Retrieved: no — egress blocked; corroborated by search in the sibling file only
- Content, as corroborated there: the supervisor's own statement of what a
  *Basisinformationsblatt* must contain — a **total risk indicator**; the **possible maximum loss
  of invested capital**; **suitable performance scenarios**; the **costs the investor bears**; and
  how and where to complain. **Four graded scenarios — *Stress*, *pessimistisch*, *moderat*,
  *optimistisch* — must be given as annualised average returns in per cent**, at **three time
  points: after one year, after half the term, and at the end of the term**; **total costs and the
  *Reduction in Yield* per year are shown at those same points**, split into **one-off and ongoing
  costs**. The ***Effektivkosten* of a specimen contract must be stated in the BIB**, which must
  be **published on the insurer's website** and **provided before conclusion**. This is the most
  precisely established regulatory fact available to this file and it is the frame for section 17.

### R10 — BaFin, Merkblatt 01/2023 (VA) on *wohlverhaltensaufsichtliche Aspekte bei kapitalbildenden Lebensversicherungsprodukten*

- Publisher: BaFin; published **May 2023** `[unverified]`
- URL: `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html`
  — recorded in the sibling delib research (its R17); not a search result of this file's own
- Retrieved: no — egress blocked; corroborated by search in the sibling file only
- Content, as corroborated there, and it applies to this product with more force than to any other
  in the library because this product's charges are its whole economics:
  - **Purpose**: to ensure that *kapitalbildende Lebensversicherungsprodukte* offer an appropriate
    ***Kundennutzen*** (customer value).
  - **Cost**: the *Effektivkosten* of different providers and products **differ considerably**;
    BaFin will **closely examine** undertakings whose *Effektivkosten* are **very high compared
    with industry norms**, and whose ***Aufwendungen für Versicherungsvermittler*** are notably
    high.
  - **Return**: the manufacturer must formulate a ***Renditeziel*** for the defined target market,
    achievable with sufficient probability, and for retirement-provision products the product must
    **achieve a real investment success with sufficient probability — a return net of costs
    exceeding a justified inflation expectation**.
  - **No numerical threshold was established** — not for *Effektivkosten*, not for commission, not
    for the real return. Any figure attributed to the *Merkblatt* would be an invention.

### R11 — BaFin, *Risiken im Fokus 2026* — "Kosten von kapitalbildenden Lebensversicherungen"

- Publisher: BaFin, annual supervisory risk-focus publication, consumer-protection chapter
- URL: `https://www.bafin.de/DE/die-bafin/publikationen-daten/risiken-im-fokus/Fokusrisiken_2026/RIF_Verbraucher_3/RIF_verbraucher_lebensversicherung_node.html`
  — recorded in the sibling delib research (its R18); not a search result of this file's own
- Retrieved: no — egress blocked; corroborated by search in the sibling file only
- Content: establishes that **"Kosten von kapitalbildenden Lebensversicherungen" is a named focus
  risk in BaFin's 2026 risk agenda** — three years after the *Merkblatt* [R10], the supervisor
  still treats the charge level of this product family as an open problem. **No text of the
  chapter is established.** It is why delib treats charge levels as a **supervised** rather than a
  free parameter and states its `[std]` stack as a design decision rather than an observation.

### R12 — DeckRV, *Deckungsrückstellungsverordnung* — *Höchstrechnungszins* and *Höchstzillmersatz*

- Publisher: Bundesministerium der Justiz / Bundesministerium der Finanzen
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `kapitallebensversicherung` (its R7) and `klassische_rentenversicherung` (its R7).
- Content, and its two quite different bearings on this product:
  - **The *Höchstrechnungszins*** — the statutory maximum technical interest rate for new business
    — was **1,00 % from 1 January 2025** `[unverified]`, raised from **0,25 %**, and the DAV
    recommended the same 1,00 % for 2026. **On the accumulation phase of a pure fondsgebundene
    contract this has no effect at all**, because there is no guaranteed accumulation rate to cap.
    It bears on the product **only** through the *Rentenfaktor*, which is priced with a
    *Rechnungszins*, and through hybrid designs whose guaranteed pot sits in the general account.
    That asymmetry is worth stating explicitly, because it is the reason unit-linked new business
    grew through the low-interest decade while classic new business collapsed.
  - **The *Höchstzillmersatz*** — the cap on acquisition costs that may be financed against future
    premiums — is **25 ‰ (2,5 %) of the *Beitragssumme*** `[unverified]`, cut from 40 ‰ by the
    LVRG 2014 [R13]. The *Beitragssumme* is the sum of all premiums payable over the
    premium-paying term. **This is the single most useful number in the file**: combined with the
    five-year spreading rule of § 169 VVG [R1] it pins the shape *and* the maximum level of the
    acquisition charge in a German unit-linked tariff, and section 4 builds the `[std]` charge on
    it.

### R13 — LVRG 2014, *Lebensversicherungsreformgesetz*

- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established. **No Bundesgesetzblatt citation is given** — inventing one is exactly what
  the retrieval-conditions section forbids.
- Retrieved: no — egress blocked. Corroborated in outline by search in the sibling delib research.
- Content: the 2014 reform package that, for this product, **cut the *Höchstzillmersatz* from 40 ‰
  to 25 ‰** [R12], **introduced the *Effektivkosten* disclosure** in quotations from 1 January
  2015 [R7], and changed the *Bewertungsreserven* rules. The sibling research also recorded an
  industry study reporting that ***Abschlusskosten* fell by almost 8 % after the LVRG**
  `[unverified]`. All dates and the 8 % are `[unverified]`; the 40 ‰ → 25 ‰ cut is corroborated
  only at the level of a secondary consumer page in a sibling file, and the `[std]` acquisition
  charge rests on that and nothing stronger.

### R14 — MindZV, *Mindestzuführungsverordnung*

- Publisher: Bundesministerium der Finanzen
- URL: `https://www.gesetze-im-internet.de/mindzv/` `[unverified]`
- Retrieved: no — egress blocked. Corroborated in outline by search in the sibling delib research.
- Content: fixes the **minimum share of each surplus source credited to policyholders**. For this
  product the relevant sources are the ***Risikoergebnis*** and the ***übriges Ergebnis***,
  because a unit-linked contract's investment result is the policyholder's by construction and
  never enters the insurer's *Rohüberschuss*. The **minimum percentages — commonly given as 90 %
  of the risk result and 50 % of the other result — are `[unverified]`.** An FRV's
  *Überschussbeteiligung* is a second-order credit on a product whose first-order economics are
  fund return minus charges, and delib does not project it (section 15).

### R15 — VAG — *Sparteneinteilung*, asset congruence, and the *Zuwendungen* rules

- Publisher: Bundesministerium der Justiz (*Versicherungsaufsichtsgesetz* 2016)
- URL: `https://www.gesetze-im-internet.de/vag_2016/` `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content, three provisions, all with `[unverified]` paragraph numbers:
  - **Sparteneinteilung.** Anlage 1 to the VAG lists ***fonds- und indexgebundene
    Lebensversicherung* as a *Versicherungssparte* in its own right**, which is why German
    statistics and insurers' accounts report it separately.
  - **Asset congruence.** Assets covering unit-linked liabilities must be held **in the
    corresponding units** and not in the general *Sicherungsvermögen* pool. So the unit liability
    and the unit assets move together exactly: **a unit-linked projection has no
    investment-mismatch term**, and the whole of the insurer's economics is in the non-unit flows.
  - ***Zuwendungen*.** The IDD-derived inducement rules govern whether an insurer may retain a
    *Kickback* / *Bestandsprovision* received out of a fund's TER. German practice credits some or
    all of it to the contract; the constraint on retaining it is `[unverified]` (gap 8).

### R16 — DAV 2004 R, *Sterbetafel für Rentenversicherungen*

- Publisher: Deutsche Aktuarvereinigung e. V. (DAV)
- URL: not established
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `klassische_rentenversicherung` (its R12–R14), including its derivation document and its
  generational character.
- Content: the German annuity table, **generational** — mortality per birth cohort, including
  expected future improvement — with first-order (loaded) and second-order (best-estimate)
  versions. It is **the table on which a *Rentenfaktor* is computed**, corroborated at one
  carrier: the inception factor rests on "a recognised mortality table (currently DAV 2004 R)" at
  "currently 0 percent p.a." [S10]. **DAV tables are DAV property, are not public and are not
  redistributed by this library** (house rules §6): delib ships a `[std]` proxy, cites the table
  by name, and states what a replacement must preserve — a generational annuitant basis with a
  first-order margin.

### R17 — DAV 2008 T, *Sterbetafel für Lebensversicherungen mit Todesfallcharakter*

- Publisher: Deutsche Aktuarvereinigung e. V.
- URL: not established
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `kapitallebensversicherung` (its R14), which located the DAV derivation document by title.
- Content: the German mortality table for death-benefit business, with first- and second-order
  versions. It matters in one place: **the *Risikobeitrag* charged for a death benefit above the
  *Fondsguthaben* is a death-risk charge and is priced on a death table**, not on the annuity
  table used for the *Rentenfaktor*. **A German FRV therefore carries two mortality bases at
  once**, and a model using one for both will misprice one of them. Cited, not shipped.

### R18 — DAV, *Ergebnisbericht* — Standardverfahren PRIIP Kategorie 4 (1 July 2025)

- Publisher: Deutsche Aktuarvereinigung e. V., *Ausschuss Lebensversicherung*
- URL: `https://aktuar.de/content/PDF/Fachwissen/2025-07-01_DAV_Ergebnisbericht_LV_Standardverfahren_PRIIP_Kategorie_4.pdf`
  — recorded in the sibling delib research (its R27); not a search result of this file's own
- Retrieved: no — egress blocked; corroborated by search in the sibling file only
- Content: identified by title and date — a **profession-agreed standard method for PRIIP
  *Kategorie 4***. Its existence establishes that the scenarios in a German BIB for a
  guarantee-bearing or profit-participating contract come from a standard method rather than each
  insurer's own model, while a **pure** fondsgebundene contract's scenarios are derived from the
  funds' own return history `[unverified]`. That is why two BIBs for economically similar products
  can show very different scenario returns and why no scenario figure transfers between carriers.
  **No content of the report is established.**

### R19 — EStG § 22 — *Ertragsanteilsbesteuerung* of the annuity

- Publisher: Bundesministerium der Justiz (*Einkommensteuergesetz*)
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `klassische_rentenversicherung` (its R5).
- Content: a private annuity — including one arising from the conversion of a fondsgebundene
  contract at *Rentenbeginn* — is taxed on its ***Ertragsanteil***, the interest component deemed
  contained in each instalment, and **not** on the return of capital. The *Ertragsanteil* is a
  **statutory percentage depending on the annuitant's age at *Rentenbeginn***, falling as the age
  rises. **At age 65 it is 18 %** — the single value corroborated in the sibling research; **every
  other age is `[unverified]`** and the table is not reproduced here. The tax treatment is
  identical for a fondsgebundene and a classic annuity once the annuity is in payment, which is
  the point: **the fund wrapper affects the accumulation phase's taxation, not the payout
  phase's**.

### R20 — EStG § 20 Abs. 1 Nr. 6 — the *Kapitalwahlrecht*, the 12/62 rule and the *Teilfreistellung*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** as to the
  12/62 rule and the half-income method.
- Content:
  - Electing a **lump sum** instead of the annuity moves the contract from § 22 [R19] to § 20: the
    taxable amount is the **excess of the payment over the premiums paid**, and where the contract
    has run **at least 12 years and payment is after the completion of the 62nd year of age**,
    **only half that gain is taxable**. Otherwise the whole gain is taxable.
  - Contracts concluded **before 1 January 2005** sit in a different regime; the German in-force
    book carries **two tax cohorts**.
  - **The provision specific to this product**: for a ***fondsgebundene*** contract a
    ***Teilfreistellung*** applies to the fund income inside the wrapper — commonly stated as
    **15 %** for equity exposure `[unverified]` [R21]. The sentence number, the percentage and the
    conditions are `[unverified]` (gap 22).
  - **The accumulation-phase point, and the product's central commercial argument**: inside the
    wrapper there is **no annual taxation of fund income, no *Vorabpauschale*, and no taxable
    disposal on a *Fondswechsel***. A direct fund holding is taxed on both.

### R21 — InvStG — *Investmentsteuergesetz* and the *Teilfreistellung*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/invstg_2018/` `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the 2018 reform of German fund taxation, which taxes the fund on certain German income
  and compensates the investor with a ***Teilfreistellung*** graded by equity quota. It reaches
  this product through [R20]: the *Teilfreistellung* available inside a fondsgebundene life
  contract is set by reference to this regime. **All percentages, thresholds and the interaction
  with the insurance wrapper are `[unverified]`.** Recorded so that the 15 % figure in section 16
  is at least attached to the statute it derives from.

### R22 — The *Rentenfaktor* / *Treuhänderklausel* cluster (consumer and trade press, LG Köln)

- Publisher: Finanztip; versicherungenmitkopf.de; Versicherungswirtschaft-heute
- URLs: `https://www.finanztip.de/private-rentenversicherung/rentenfaktor/` ·
  `https://www.versicherungenmitkopf.de/treuhaenderklausel-rentenversicherung` ·
  `https://www.versicherungenmitkopf.de/rentenversicherung/rentenfaktor` — all recorded in the
  sibling delib research on `klassische_rentenversicherung` (its R16–R18); **not search results of
  this file's own**
- Retrieved: no — egress blocked; corroborated by search in the sibling file only
- Content, as corroborated there, transferring to this product **with more force than to the
  classic one**, because here the *Rentenfaktor* is the **only** guarantee the policyholder has:
  - Insurers **could previously change guaranteed *Rentenfaktoren* under a *Treuhänderklausel*,
    with the approval of an independent external *Treuhänder***, where economic conditions
    deteriorated permanently and unexpectedly, on **two triggers**: an unexpectedly strong increase
    in life expectancy, and a sustainable reduction in capital-market returns.
  - **The clause is now used only in older contracts; today the guaranteed factor can be changed
    only under § 163 VVG** [R4].
  - **The Landgericht Köln held that the low-interest phase is not a sufficient ground**, being
    entrepreneurial risk that cannot be passed to policyholders. **The case reference, date and
    parties were not established** in the sibling research either — gap 15.
  - Trade press of **4 February 2021** reports the market leader's position that customers could
    not successfully object to an adjustment — a **live commercial dispute at the largest German
    life insurer**, inside the window in which the current in-force unit-linked book was written.
  - **The consumer definition**: the *Rentenfaktor* determines **how much monthly annuity is
    received per 10 000 € of accumulated capital**, so 100 000 € at a factor of 25 yields 250 € per
    month. **The 25 is a teaching example, not a market level.**

### R23 — Rating houses and market studies: Franke und Bornberg, Morgen & Morgen, Assekurata

- Publisher: Franke und Bornberg GmbH; Morgen & Morgen GmbH; ASSEKURATA Assekuranz Rating-Agentur
  GmbH
- URL: not established for any fondsgebundene study. The sibling delib research corroborated the
  existence of Franke und Bornberg's *Rentenfaktor* and *Basisinformationsblätter* commentary and
  of Assekurata's **24. Marktstudie "Überschussbeteiligungen und Garantien 2026"**.
- Retrieved: no — egress blocked; no search corroboration for any fondsgebundene study
- Content: these three houses are **where German unit-linked cost and *Rentenfaktor* levels are
  actually published**. They are the documents this file most needed and did not have. The sibling
  research recorded that even the Franke und Bornberg article **titled** "Was bedeutet der
  Rentenfaktor und wie hoch ist er?" returned no level, range or table. **No figure from any of
  them is used anywhere in the delib documents.** Gaps 4 and 6.

### R24 — Consumer bodies and comparison portals

- Publisher: Stiftung Warentest (*Finanztest*); Verbraucherzentrale Bundesverband and the *Länder*
  *Verbraucherzentralen*; Verivox; CHECK24; Finanztip
- URL: not established for any fondsgebundene Rentenversicherung page
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the secondary literature in which German consumers meet this product, and normally the
  only public place where **price points** appear — a monthly premium, an *Effektivkosten*
  percentage, a *Rentenfaktor*, a tariff comparison at a stated model point. **Nothing from any of
  them is cited in this file**, because none of these pages was retrieved, then or in the pass of
  2026-08-30 — the Finanztip *Rentenfaktor* material that was read is carried at [R22]. Recorded so a later
  reader knows where to look first and so the gaps register can name the document that would close
  each gap.

### R25 — GDV statistics on German life new business and in-force by *Versicherungsart*

- Publisher: Gesamtverband der Deutschen Versicherer e. V.
- URL: not established. The sibling delib research corroborated the existence of the series "Die
  deutsche Lebensversicherung in Zahlen" and "Neugeschäft und Bestand der Lebensversicherer für
  die letzten zehn Geschäftsjahre".
- Retrieved: no — egress blocked; no search corroboration for any unit-linked breakdown
- Content: the series that would establish **the share of German life new business written as
  fondsgebundene Rentenversicherung** — the market figure this file's opening asserts and cannot
  source. That claim is `[unverified]` as to any number and rests on what *is* corroborated: the
  withdrawal of the classic tariff at a major carrier [S14] and the framing of the supervisor's
  cost agenda [R10] [R11]. Gap 25.

### R26 — BGH case law on *Rückkaufswert*, *Kostenverrechnung* and *Stornoabzug*

- Publisher: Bundesgerichtshof
- URL: not established. **No case number, decision date or docket is given for any decision in
  this entry.**
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: there is a long and well-known German line of authority on whether and how an insurer
  may charge acquisition costs against the early values of a life contract — from decisions on
  *Zillmerung* and on the transparency of *Rückkaufswert* clauses before the VVG 2008 reform,
  through decisions on the validity of *Stornoabzug* clauses, to decisions applying the post-2008
  rules. **This file records that the line exists and cites no decision from it.** Any statement
  in a delib document about what a court has held on a *Rückkaufswert* clause must carry
  `[unverified]` and must not carry a docket number. Gap 16.

---

## Extracted facts, by mechanic

This is the section the `product-spec.md` and `technical-notes.md` are written from. It is written
long because it is the part that does not depend on having a PDF open. **Structure is described
without hedging where it is common ground in German practice; every level is either `[std]` with a
rationale or tagged `[unverified]`.**

### 1. Product structure and the unit-linked principle

- A *fondsgebundene Rentenversicherung* is a **deferred private annuity whose accumulating value
  is a holding of units in investment funds chosen by the policyholder**. The insurer administers
  the contract, bears the biometric risk, and gives one financial guarantee — the *Rentenfaktor* —
  but **does not guarantee the value of the fund holding at any point before *Rentenbeginn***.
- The defining sentence of the product, and the one every German wording expresses in some form:
  **the insurer guarantees the number of *Anteileinheiten*, not their value.** Everything else
  follows from it. There is no *Rechnungszins* in the accumulation phase, no *Deckungskapital* in
  the general-account sense, no *Zinsüberschuss*, no *Bewertungsreserven* worth speaking of, and
  no investment mismatch between the insurer's assets and its unit liability [R15].
- **It is *Schicht 3*** — unsubsidised private provision. There is no state allowance, no
  *Sonderausgabenabzug* of the premium, and correspondingly no *Beitragsgarantie* requirement, no
  restriction on the payout form and no *Förderschädlichkeit* on surrender. The fondsgebundene
  forms of *Basisrente* and *Riester* carry all of those and are separate delib products.
- **The contract is a life insurance contract, not a fund product**, and that has three
  consequences the model must respect: the death benefit is an insurance benefit and is priced
  with a *Risikobeitrag* (section 6); the conversion at *Rentenbeginn* is a **guaranteed**
  conversion at a factor fixed at issue (section 9); and the accumulation phase is not taxed
  (section 16).

### 2. The unit / non-unit split

- The policy's value is the ***Fondsguthaben***: the number of *Anteileinheiten* held in each
  fund, multiplied by that fund's *Anteilspreis* at the *Bewertungsstichtag* [S17]. Formally, with
  `n_j(t)` the units held in fund `j` and `P_j(t)` its unit price:

  ```
  Fondsguthaben(t) = sum_j n_j(t) x P_j(t)
  ```

- **Units are the state variable; euro are derived.** Every operation on the contract is expressed
  as a purchase or a cancellation of units at a price on a date. This is what makes the product a
  clean recursion: the model carries `units(t)` and `unit_price(t)` and derives everything else.
- **The *Anteilspreis* is the fund's *Rücknahmepreis*** — its net asset value per unit. German
  insurers normally buy policy units at the *Rücknahmepreis*, i.e. **with the *Ausgabeaufschlag*
  (front-end load) waived**, because they deal with the fund company at institutional terms; the
  policy's own acquisition charge takes the place of the retail load. Whether any given tariff
  waives it in full is `[unverified]`, and the delib model assumes a **full waiver** as a `[std]`
  simplification, which is the market norm.
- **The *Bewertungsstichtag*** is the dealing date on which a premium buys units or a charge
  cancels them. Wordings typically fix it as the next fund valuation after the premium is received
  or the event occurs. **On a monthly model grid this is the month boundary** and the timing
  detail disappears; it is recorded because it is the reason a real policy's unit count and a
  model's differ by a few days' price movement.
- **The non-unit side.** Everything that is not the unit holding is a cash flow in the insurer's
  own accounts: the charges it withholds or cancels, the *Risikobeitrag* it collects, the death
  benefits it pays, its expenses and its commission. **delib projects the non-unit cash flows and
  carries the unit fund only as the base on which they are computed** — the right emphasis for a
  liability model, since the unit fund is the policyholder's money passing through.

### 3. Premium and *Beitragsverrechnung*

- **Premium form**: a level recurring *Beitrag*, most commonly **monthly** and paid by direct
  debit; quarterly, half-yearly and annual frequencies exist, normally with a
  *Ratenzahlungszuschlag* for paying more often than annually `[unverified]` as to level. **The
  delib model is monthly** (`FRV_DE_S`), which matches the dominant frequency and makes the charge
  mechanics visible.
- **The *Beitragsverrechnung* is the operative rule of the accumulation phase**: what is taken out
  of each gross premium, in what order, before the remainder buys units. The German market order [S1],
  which the delib model follows:

  1. **Gross premium** `B` received.
  2. Less the ***Abschluss- und Vertriebskosten* instalment** `alpha(t)` — non-zero only in the
     first five years (section 4).
  3. Less the ***beitragsbezogene Verwaltungskosten*** `beta x B` — a percentage of the gross
     premium, charged for the whole premium-paying term.
  4. Less the ***Stückkosten*** `SK` — a fixed euro amount per month.
  5. The remainder is the ***Anlagebeitrag***, which **buys units at the *Anteilspreis***.
  6. **Separately, and by cancelling units rather than by withholding premium**: the
     ***kapitalbezogene Verwaltungskosten*** `gamma` on the *Fondsguthaben*, and the
     ***Risikobeitrag*** on the net amount at risk.

- **The distinction between step 5 and step 6 matters and is easy to get wrong.** Premium-based
  charges are withheld *before* units exist; fund-based charges and the *Risikobeitrag* cancel
  units that already exist. A paid-up contract has no step 2–4 and a full step 6 — which is why it
  decays (section 12). A model that nets the fund-based charge out of the premium instead of
  cancelling units will produce the right answer while premiums are paid and the wrong answer the
  moment they stop.
- ***Beitragsdynamik***: an optional contractual annual increase of the premium — a fixed
  percentage or an index-linked step `[unverified]` — raising the *Beitragssumme* and therefore the
  acquisition charge on the increment. Individual increases may normally be declined. delib carries
  `dynamik_rate` as a model-point parameter with a `[std]` default of 0 %.

### 4. The charge stack, its German names, and the `[std]` levels

This is the most important table in the file, and every level in it is `[std]`. The **structure**
is German market practice; the **levels** were established nowhere in this corpus (gap 6).

| Charge | German name | Base | Timing | delib `[std]` level | Argued range |
|---|---|---|---|---|---|
| Acquisition | *Abschluss- und Vertriebskosten* (*Alpha-Kosten*) | *Beitragssumme* | spread evenly over the first 60 months | 2.5% of *Beitragssumme* | 0% (Nettotarif) to 2.5% (the statutory cap) |
| Premium admin | *beitragsbezogene Verwaltungskosten* (*Beta-Kosten*) | each gross premium | whole premium-paying term | 4.0% of each premium | 2% to 10% |
| Fund admin | *kapitalbezogene Verwaltungskosten* (*Gamma-Kosten*) | *Fondsguthaben* | monthly, by unit cancellation | 0.30% p.a. | 0.10% to 1.20% p.a. |
| Policy fee | *Stückkosten* | per policy | monthly, by withholding or cancellation | 3.00 EUR per month | 0 to 5 EUR per month |
| Risk charge | *Risikobeitrag* | *riskiertes Kapital* | monthly, by unit cancellation | q(x) based, DAV 2008 T proxy | n/a — a priced risk, not a load |
| Fund cost | *TER* / *Gesamtkostenquote* | fund assets | continuously, inside the unit price | 0.45% p.a. | 0.15% (ETF) to 2.00% (active) |
| Trail rebate | *Kickback* / *Bestandsprovision* | fund assets | credited to the *Fondsguthaben* | 0.00% p.a. | 0% to 0.50% p.a. |
| Annuity admin | *Rentenbezugskosten* | each annuity payment | in payment | 1.5% of each payment | 0% to 3% |
| Fund switch | *Fondswechselgebühr* | per switch beyond the free allowance | on election | 0 EUR (free allowance not exhausted) | 0 to 25 EUR |
| Single premium | *Zuzahlungskosten* | each *Zuzahlung* | on receipt | 2.5% of the *Zuzahlung* | 0% to 4% |

**Abschluss- und Vertriebskosten — the one charge whose level has a real anchor.**

- **The cap.** The *Höchstzillmersatz* is **25 ‰ (2,5 %) of the *Beitragssumme*** [R12], cut from
  40 ‰ by the LVRG 2014 [R13] `[unverified]`. The *Beitragssumme* is the sum of all premiums
  payable over the premium-paying term. **The delib `[std]` takes the cap as the level**, on the
  stated ground that a reference implementation should demonstrate the binding constraint rather
  than a guessed interior point, and that the cap is the only acquisition-cost number with any
  corroboration anywhere in the delib corpus.
- **The spreading.** § 169 VVG requires the *angesetzte Abschluss- und Vertriebskosten* to be
  spread **evenly over the first five contract years** [R1]. In a unit-linked tariff this is
  implemented in the *Beitragsverrechnung*: **only one fifth of the total acquisition charge may
  be withheld in each of the first five years**, so units are bought from the start rather than
  not at all.
- **The arithmetic, worked, because it is the shape the model reproduces.** Monthly premium 200 €,
  premium-paying term 30 years: *Beitragssumme* = 200 × 12 × 30 = **72 000,00 €**; acquisition
  charge at 2,5 % = **1 800,00 €**; spread over 60 months = **30,00 € per month for the first five
  years**, i.e. **15 % of each of the first 60 premiums** and **nothing thereafter**. That step —
  a large early charge that stops abruptly at month 60 — is the characteristic shape of a German
  unit-linked contract's early values and is what the worked example must show.

**Verwaltungskosten — two of them, and the German market names them by their base.**

- ***Beitragsbezogene Verwaltungskosten*** are a **percentage of each gross premium** and continue
  for the whole premium-paying term. They stop when premiums stop. In actuarial notation these are
  the *β*-Kosten.
- ***Kapitalbezogene Verwaltungskosten*** are a **percentage per annum of the *Fondsguthaben***,
  taken monthly by cancelling units. The German market also calls them *Gammakosten* or
  *Fondsguthabenkosten*. They **continue after premiums stop** and they are the charge that makes
  a paid-up unit-linked policy decay. In a long contract they are the dominant component of the
  *Effektivkosten*, because they compound against the whole accumulated fund.
- **No level for any of the three was established at any carrier.** All three are `[std]`.

**The fund's own costs, and the *Kickback*.**

- The fund's ***TER*** is borne **inside the unit price** and never appears in the policy ledger.
  A model that charges it explicitly will double-count; a model that ignores it will overstate the
  policyholder's return. **The delib model handles it by netting it off the assumed gross fund
  return**, which is exactly what it is.
- ***Kickback* / *Bestandsprovision***: the fund company pays the insurer a trail commission out
  of the fund's TER. German practice is that the insurer **credits some or all of it back to the
  contract** as additional units, so that the policyholder's effective fund cost is the TER less
  the credited rebate. The IDD-derived inducement rules bear on whether it may be retained [R15]
  `[unverified]`.

### 5. *Effektivkosten* — the metric that ties the stack together

- The ***Effektivkostenquote*** (Reduction in Yield, RIY) states **all charges as the annual
  percentage by which they reduce the contract's return**. It is required in quotations since
  1 January 2015 under § 7 VVG and the *VVG-InfoV* [R6] [R7] [S16] `[unverified]`, and in its
  PRIIPs form in the *Basisinformationsblatt* at **three time points — one year, half the
  recommended holding period, and the end of it** [R9].
- **Order-of-magnitude check on the delib `[std]` stack**, given as arithmetic and not as an
  observation: on the section 4 levels at a 200 € monthly premium over 30 years, the premium-based
  charges take roughly 5,5 % of every premium plus the 15 % early instalment, and the fund-based
  charges take about 0,75 % p.a. of the fund including the TER. The resulting reduction in yield
  is **of the order of 1 % per annum**. The technical notes must compute it exactly from the
  model's own output rather than quote this estimate.
- **Market levels are `[unverified]` in their entirety.** The commonly stated picture — that
  broker-sold commission tariffs sit materially above direct and net tariffs, with a market spread
  of more than a percentage point of annual yield — is consistent with BaFin's "differ
  considerably" [R10], but **no range, median or carrier-level figure is established
  anywhere in this corpus** [R23] [R24]. Gap 6.

### 6. *Todesfallleistung* before *Rentenbeginn*, and the *Risikobeitrag*

- **Four shapes are used in the German market.** Listed in ascending order of the risk they impose
  on the insurer:
  1. ***Fondsguthaben*** — the value of the units at the *Bewertungsstichtag* after the death is
     notified. **No net amount at risk, no *Risikobeitrag*.** The cheapest and, on a pure savings
     tariff, common.
  2. ***Beitragsrückgewähr*** — `max(Fondsguthaben, sum of premiums paid)`. **This is the shape
     corroborated at DEVK** [S2] and the one delib adopts as representative. The net amount at
     risk is positive only while the fund is below the premiums paid, i.e. **early, and after a
     market fall** — which makes the risk charge small in aggregate but strongly path-dependent.
  3. **A percentage of the *Fondsguthaben*** — commonly quoted as 100 %, 105 % or 110 %
     `[unverified]`. A percentage above 100 creates a proportional net amount at risk that grows
     with the fund.
  4. **A *garantierte Mindesttodesfallleistung*** — a stated sum insured, chosen at issue,
     independent of the fund. The most expensive, and the one that turns the contract into a
     savings-plus-term-cover package.
- **The *Risikobeitrag* is levied monthly by cancelling units.** With `TFL(t)` the death benefit
  and `FG(t)` the *Fondsguthaben*:

  ```
  riskiertes Kapital(t) = max( TFL(t) - FG(t), 0 )
  Risikobeitrag(t)      = q_mth(x + t) x riskiertes Kapital(t)
  units cancelled       = Risikobeitrag(t) / Anteilspreis(t)
  ```

  The charge is **recomputed every month** because both `TFL` and `FG` move. On the
  *Beitragsrückgewähr* shape the net amount at risk is `max(premiums paid - FG, 0)`, which is the
  quantity the model must carry: **cumulative premiums paid is a state variable of this product**,
  not a reporting convenience.
- **The mortality basis for the risk charge is a death table — DAV 2008 T** [R17] — **not** the
  annuity table used for the *Rentenfaktor* [R16]. A German FRV carries two mortality bases at
  once. A model that prices the death charge on the annuity table will understate it, because an
  annuitant table's mortality is lighter by selection and by projection.

### 7. Fund selection, *Fondswechsel*, *Ablaufmanagement*

- ***Fondswechsel*** covers **two distinct operations**, and German wordings use the English words
  *Shift* and *Switch* for them:
  - **reallocating the existing *Fondsguthaben*** from one fund to another — units are cancelled
    in the old fund and bought in the new one at the same *Bewertungsstichtag*; and
  - **redirecting future premiums** to a different fund or a different split, leaving the existing
    holding where it is.
  - **Which English word denotes which operation is not consistent across German insurers**, and
    this file does not assert a mapping. Each AVB defines its own terms. **The delib documents use
    the operations, not the labels**: `shift_existing` and `redirect_future` are the model's
    names, and the technical notes say why. Gap 11.
- ***Ablaufmanagement*** is **automatic phased de-risking in the run-up to *Rentenbeginn***: over
  the last few years the *Fondsguthaben* is moved in tranches out of equity funds into
  money-market or *Wertsicherungs* funds, or into the insurer's *Sicherungsvermögen*. It is
  normally **opt-in or opt-out with a default**, and the number of years and the tranche schedule
  are tariff parameters `[unverified]`. **A five-year monthly ramp is the shape most often
  described** `[unverified]`.
- **Why it matters to a cash-flow model**: it changes the assumed fund return in the final years,
  and therefore the *Fondsguthaben* at *Rentenbeginn* and the annuity. delib implements it as a
  **deterministic glide on the assumed return** — a `[std]` linear ramp from the equity assumption
  to a money-market assumption over the last 60 months, switchable off — because with one fund and
  a deterministic return that is the same thing as a reallocation and is the honest representation
  of what is known.

### 8. *Zuzahlungen*, *Teilentnahmen*, and the flexible *Rentenbeginn*

- ***Zuzahlung*** — an additional single premium into an existing contract, subject to a minimum
  and sometimes an annual maximum `[unverified]`, and to its own acquisition charge (section 4). It
  buys units at the *Anteilspreis* on the following *Bewertungsstichtag* and **raises the
  *Beitragssumme***. delib supports it as a model-point schedule with a `[std]` default of none.
- ***Teilentnahme* / *Entnahme*** — a partial withdrawal during the *Aufschubzeit*, subject to a
  minimum withdrawal and a minimum remaining *Fondsguthaben* `[unverified]`. It is a partial
  surrender with a partial surrender's tax consequences [R20], modelled as a unit cancellation;
  delib's `withdrawals(t)` publishes it, per the house naming rules.
- ***Abrufphase* / flexible *Rentenbeginn*** — a window, commonly a few years either side of the
  agreed date `[unverified]`, inside which the conversion may be brought forward or deferred.
  **Deferring changes the *Rentenfaktor***, which is age-dependent. Whether the *guaranteed* factor
  is restated on deferral, or only the current one, is `[unverified]` (gap 13). **delib fixes the
  *Rentenbeginn*** and records the *Abrufphase* as an unmodelled option.

### 9. The *Rentenfaktor*

**This is the product's only financial guarantee, and it is the reason the contract is
insurance.**

- **Definition and arithmetic.** The *Rentenfaktor* is the **monthly annuity per 10 000 € of
  capital at *Rentenbeginn*** [R22]:

  ```
  monthly annuity = Fondsguthaben(Rentenbeginn) / 10 000 x Rentenfaktor
  ```

  A capital of 100 000 € at a factor of 25 yields 250 € per month [R22] — **a teaching example,
  not a market level**.
- **Guaranteed at inception, on the bases then in force.** The *garantierter Rentenfaktor* is
  fixed in the contract documents and rests on the *Rechnungsgrundlagen* at the date of conclusion
  [R22]: a mortality table — **DAV 2004 R** [R16] — and a *Rechnungszins*. The insurer applies a
  ***Sicherheitsabschlag***, which is why the guaranteed factor is lower than the factor the same
  insurer would quote for an immediate annuity today.
- **The margin is quantifiable from one corroborated statement.** The sibling delib research
  established that a large direct writer computes its inception factor on "a recognised mortality
  table (currently DAV 2004 R) and an underlying interest rate of **currently 0 percent p.a.**"
  [S10]. **A zero-per-cent interest basis on a guarantee that will be honoured in thirty years is
  the *Sicherheitsabschlag* made concrete**: the factor is priced as though the insurer will earn
  nothing on the annuity fund for the whole payout phase.
- **The rule at *Rentenbeginn* is a maximum of two factors**, and this is a **guarantee with
  upside**:

  ```
  Rentenfaktor_applied = max( Rentenfaktor_garantiert, Rentenfaktor_aktuell(Rentenbeginn) )
  ```

  The sibling research corroborated this at a conventional carrier — at the start of annuity
  payments a second factor is compared with the guaranteed one and **the higher of the two is
  guaranteed for the payment period** — and at the market leader, whose current bases at
  *Rentenbeginn* are "the interest rate and mortality table that the company uses **at that time
  for immediately beginning annuities**". **A model that applies only the guaranteed factor
  understates the benefit whenever the current tariff is richer.**
- **On a fondsgebundene contract the guarantee bites differently than on a classic one.** On a
  classic contract both the capital and the factor are guaranteed, so the annuity is guaranteed.
  On this product **only the factor is** — the capital it multiplies is the market's. The
  guarantee is therefore a guarantee about the *conversion terms*, not about the *pension*, and
  any product document that implies otherwise is wrong. This is the sentence a delib
  `product-spec.md` must carry.
- **Reduction of a guaranteed factor** was historically possible under a *Treuhänderklausel* and
  today only under § 163 VVG [R4]; the triggers, the Landgericht Köln decision narrowing them and
  the 2021 dispute at the market leader are set out at [R22].
- **Modelling consequence**: the guaranteed *Rentenfaktor* is treated as **fixed for the life of
  the contract**, and § 163 VVG is recorded as a model risk rather than implemented.
- **The `[std]` level, and how it is derived rather than guessed.** No market level was
  established anywhere in this corpus (gap 4). Rather than invent one, delib derives it:

  - At a *Rechnungszins* of **0 %** [S10], a monthly annuity of `R` per month payable for an
    expected `T` years has present value `12 x T x R` per unit of capital, so `Rentenfaktor = 10
    000 / (12 x T)` before costs.
  - On a **generational** annuitant table [R16] a 67-year-old of a cohort now in mid-career has an
    expected annuity duration materially longer than a period table implies; **taking `T` in the
    range 25 to 28 years** gives a pre-cost factor between **29,8 and 33,3** € per 10 000 €.
  - Deducting the payout-phase administration charge (section 4, 1,5 % of each payment) and a
    further explicit margin for the *Sicherheitsabschlag* and for a *Rentengarantiezeit* brings
    the **guaranteed** factor materially below that.
  - **The delib `[std]` guaranteed *Rentenfaktor* is 25,00 € per month per 10 000 € of
    *Fondsguthaben* at age 67**, chosen as a round number inside the band that arithmetic
    produces, and matching the illustrative value the consumer literature uses [R22]. **It is a
    `[std]` parameter with a derivation, not a market observation**, and the technical notes must
    say so wherever it appears.
  - **The `[std]` current factor at *Rentenbeginn*** is set equal to the guaranteed one, so that
    the `max()` is exercised in the model and is visible, but does not silently inject an
    unsourced uplift.

### 10. The *Rentenphase* and the *Kapitalwahlrecht*

- **At *Rentenbeginn* the fund holding is liquidated and the proceeds are converted.** The units
  are cancelled at the *Anteilspreis*, the *Fondsguthaben* passes into the insurer's general
  account, and a **classic annuity** begins — guaranteed at the applied *Rentenfaktor*, with an
  *Überschussrente* on top from the payout-phase surplus. **The unit-linked character of the
  contract ends at *Rentenbeginn***, which is the boundary of the delib model's scope: the payout
  phase's machinery belongs to `sofortrente`.
- ***Rentengarantiezeit***: a guaranteed payment period, commonly 5, 10 or 15 years
  `[unverified]`, during which instalments continue to the beneficiary if the annuitant dies. It
  reduces the *Rentenfaktor*, because it is a second benefit paid for out of the same capital.
- ***Kapitalwahlrecht***: the option to take the *Fondsguthaben* as a lump sum at *Rentenbeginn*
  instead of the annuity, subject to a notice period `[unverified]`. **Its take-up is the largest
  behavioural unknown in the product** and it is economically live, because the two tax regimes
  are genuinely different (section 16). **No take-up rate was established** (gap 19); the delib
  `[std]` runs the annuity path and carries the lump-sum path as a switch.

### 11. *Rückkaufswert* and *Storno*

- **The surrender value of a fondsgebundene policy is the *Zeitwert*** [R1], and for a pure
  unit-linked contract with no insurer-given guarantee **the *Zeitwert* is the *Fondsguthaben***:

  ```
  Rückkaufswert(t) = Fondsguthaben(t) - Stornoabzug(t)
  ```

- **What that removes from the calculation is the whole conventional apparatus**: no discounting,
  no *Rechnungszins*, no mortality basis, no *Zillmerung* residue, no *Mindestrückkaufswert*
  computation on a second basis. It is the cleanest surrender rule of the ten delib products, and
  it is the reason this product is a good vehicle for demonstrating unit mechanics.
- **The protection for the policyholder sits earlier, in the *Beitragsverrechnung***: because the
  acquisition charge may only be taken over the first five years [R1], the *Fondsguthaben* is
  never driven to zero by an up-front deduction, and the surrender value is positive from the
  first year. **Whether the statutory *Mindestrückkaufswert* floor formally applies to the
  *Zeitwert* branch, or whether the five-year spreading in the *Beitragsverrechnung* is what
  discharges the obligation, is `[unverified]`** — gap 2. Both readings produce the same numbers
  on the delib design.
- ***Stornoabzug***: permissible **only if agreed, quantified and appropriate**, and **never for
  unamortised acquisition costs** [R1]. Many unit-linked tariffs therefore have **no *Stornoabzug*
  at all**. **The delib `[std]` is a zero *Stornoabzug***, with the parameter present and
  switchable, on the ground that a non-zero one would be an unsourced number attached to a
  contested clause.
- **Early values are nevertheless poor, for a structural reason worth stating**: at the section 4
  levels, a contract surrendered in year 3 has had 15 % of every premium taken for acquisition plus
  the ongoing charges, so the *Rückkaufswert* is well below premiums paid even in a flat market.
  **That is not a penalty and there is no deduction** — it is the acquisition charge already spent.
  The worked example must display the first five years explicitly, because that is where the
  product's economics are least intuitive.

### 12. *Beitragsfreistellung*

- The policyholder may convert to a **paid-up** contract [R3]. On a fondsgebundene contract:
  premium payment stops; the units stay; the *beitragsbezogene* charges and the *Stückkosten* that
  are withheld from premium stop with the premium; and the ***kapitalbezogene Verwaltungskosten*,
  any *Stückkosten* charged by cancellation, and the *Risikobeitrag* continue to be taken by
  cancelling units**.
- **The paid-up contract therefore decays** at the fund-based charge rate less the fund's return.
  If the death benefit is a *garantierte Mindesttodesfallleistung*, the *Risikobeitrag*
  accelerates the decay as the fund falls and the net amount at risk rises — a feedback the model
  reproduces automatically and a real product risk.
- ***Beitragsfreistellung* and *Storno* are two decrements, not one** — different triggers,
  different cash flows, different subsequent projections. Conflating them is a listed pitfall.

### 13. Hybrid and guarantee variants — named, and deliberately not implemented

German insurers wrap three distinct guarantee technologies around this same unit-linked chassis.
They are named here because a reader of the delib model must know what the model is *not* doing,
and because the vocabulary is a German market invention with no English equivalent.

- ***Statisches Hybrid* (*Zwei-Topf-Hybrid*, static form).** The premium is split **once, at
  inception**, between the *Sicherungsvermögen* — where a guaranteed pot accretes at the
  *Rechnungszins* to exactly the guaranteed amount at *Rentenbeginn* — and free funds. The split
  is computed from the guarantee level, the term and the *Rechnungszins* and does not change.
  Simple, transparent, and at a low *Rechnungszins* it consumes almost the whole premium for the
  guarantee.
- ***Dynamisches Hybrid* (*Zwei-* or *Drei-Topf-Hybrid*).** The split is **recomputed
  periodically**, normally monthly, so that the guarantee remains secured while as much as
  possible sits in the funds. The **three-pot** form adds a middle pot — a
  ***Wertsicherungsfonds***, a fund with a contractual limit on its loss over a defined period —
  between the *Sicherungsvermögen* and the free funds, so that money can be moved out of equities
  in two steps rather than one.
- ***i-CPPI*** — individual Constant Proportion Portfolio Insurance. The exposure to the risky
  fund is set, **per policy and continuously**, as a multiplier times the cushion between the
  policy value and the present value of the guarantee. The most efficient of the three and the most
  path-dependent.
- **Why the delib model implements none of them.** Each is a **rule for reallocating between a
  guaranteed pot and a risky pot along a path**, and its entire content is what it does when the
  risky pot falls. A deterministic projection has **one path, and it is a smooth one**, so a
  guarantee mechanism modelled inside it either never triggers — dead code presented as a feature —
  or triggers on a hand-chosen shock, which asserts a scenario the model has no basis for. **delib
  models the pure unit-linked chassis and states what would have to be added**: a stochastic or at
  least multi-scenario asset model, a monthly reallocation rule, a guaranteed pot accreting at a
  *Rechnungszins*, and a *Wertsicherungsfonds* return model. That is a different model, and an
  honest reference implementation says so rather than gesturing at it.
- **What the model *does* keep from the hybrid world**: the *Ablaufmanagement* glide (section 7),
  which is de-risking without a guarantee and is representable deterministically.

### 14. *Rechnungsgrundlagen* — two mortality bases, no interest basis

- **The accumulation phase has no interest basis at all.** There is no *Rechnungszins*, and the
  *Höchstrechnungszins* — 1,00 % from 2025, raised from 0,25 % [R12] `[unverified]` — **does not
  bind it**. That is the structural reason unit-linked business grew through the low-interest
  decade while classic business shrank.
- **The death charge is priced on a death table** — DAV 2008 T [R17], first order — and **the
  conversion guarantee on an annuity table** — DAV 2004 R [R16], generational, first order.
- **Best-estimate projection uses the second-order versions.** delib's cash flows are gross
  best-estimate, so the projection's decrement is second-order while the *charge* the model levies
  is the first-order one the tariff specifies. **The difference between them is the risk result**,
  and it is the source of the *Überschussbeteiligung* of section 15. A model that uses one table
  for both makes the risk result identically zero and loses the mechanic.
- **DAV tables are not redistributed by this library** (house rules §6). delib ships `[std]`
  proxies anchored so the worked example reproduces exactly, cites the tables by name, and states
  what a replacement must preserve: for DAV 2004 R, a generational annuitant basis with a
  first-order margin; for DAV 2008 T, a death-risk basis at insured-life selection levels.

### 15. *Überschussbeteiligung* on a fondsgebundene contract

- **The investment result is not a surplus source here** — it belongs to the policyholder by
  construction. The surplus sources are the ***Risikoergebnis*** and the ***übriges Ergebnis***
  (the cost result), with statutory minimum policyholder shares under the MindZV [R14]
  `[unverified]` as to percentages.
- **Credited in one of three ways** `[unverified]` as to which carrier does which: as **additional
  *Anteileinheiten*** bought for the contract; as a **reduction of the charges** taken; or
  accumulated and paid as a ***Schlussüberschuss*** at *Rentenbeginn*.
- **Second-order in size, and delib does not project it.** The first-order economics of this
  product are fund return minus charges; a risk-and-cost surplus on a contract whose death cover
  is a *Beitragsrückgewähr* is small. The model omits it, states the omission, and records that
  the omission biases the projected *Fondsguthaben* **downward** — the honest direction for a
  charge demonstration.

### 16. Taxation

- **Accumulation phase: nothing is taxed.** No annual taxation of fund income, no
  *Vorabpauschale*, and **no taxable disposal on a *Fondswechsel*** [R20]. This deferral is the
  product's principal commercial argument against holding the same funds in a *Depot*, where both
  apply. It is also the reason the *Effektivkosten* comparison against a direct ETF holding is not
  a like-for-like one.
- **Annuity: the *Ertragsanteil*** [R19]. Only the deemed interest component of each instalment is
  taxable, at a statutory percentage set by the annuitant's age at *Rentenbeginn* — **18 % at age
  65**, every other age `[unverified]`.
- **Lump sum: § 20 EStG** [R20]. Taxable amount = payment less premiums paid; **half of it** if
  the contract has run **at least 12 years and payment is after age 62**; otherwise all of it.
  ***Kapitalertragsteuer* is withheld by the insurer** `[unverified]` as to rate and surcharges.
- ***Teilfreistellung*** for the fund income inside a fondsgebundene wrapper — commonly stated as
  **15 %** for equity exposure `[unverified]` [R20] [R21]. This is the provision that makes the
  lump-sum route from a fondsgebundene contract more favourable than from a classic one, and it
  has no counterpart in the sibling products.

### 17. Fund return assumptions, PRIIPs scenarios, and the *Modellrechnung*

- **The model needs one number the market does not supply: an assumed gross fund return.** Nothing
  in this corpus establishes one, and PRIIPs deliberately does not provide one — its scenarios are
  **derived from the underlying's own return history** under the RTS methodology [R8], not chosen
  by the insurer.
- **What the *Basisinformationsblatt* shows instead** [R9]: **four scenarios — *Stress*,
  *pessimistisch*, *moderat*, *optimistisch* — as annualised average returns in per cent**, at
  **one year, half the holding period, and the end of it**, with **total costs and the RIY** at
  the same three points. For a fondsgebundene Rentenversicherung with a 30-year *Aufschubzeit*
  those points are roughly year 1, year 15 and year 30.
- **Category matters.** A pure unit-linked contract's scenarios come from the funds' history
  (Category 2 `[unverified]`); a guarantee-bearing or profit-participating one from the DAV standard
  method for Category 4 [R18]. **Two BIBs for economically similar products can therefore show very
  different scenario returns**, which is why the delib documents cite **no** scenario return.
- **The German *Modellrechnung*** required by the *VVG-InfoV* [R7] illustrates the maturity benefit
  at prescribed assumed rates; the number of rates and their levels are `[unverified]` (gap 23).
- **The delib `[std]` fund return** is a **single deterministic gross rate of 5,00 % p.a., less
  the fund TER of 0,45 % p.a., giving 4,55 % p.a. net of fund costs**, applied monthly. Rationale:
  it is a round, clearly-labelled assumption in the middle of the range a long-horizon
  equity-tilted mixed fund is generally assumed to earn; it is **not** a PRIIPs scenario, is not
  attributed to any document, and is a parameter the reader is expected to change. The
  `Ablaufmanagement` glide steps it down to a `[std]` **1,50 % p.a.** money-market rate over the
  last 60 months when switched on.
- **The projection is deterministic and the model says so.** Nothing in delib produces a
  distribution, so nothing in delib may be compared with a PRIIPs scenario.

### 18. Decrements and policyholder behaviour

- **Decrements in the *Aufschubzeit***: death (pays the *Todesfallleistung*, section 6), *Storno*
  (pays the *Rückkaufswert*, section 11), and *Beitragsfreistellung* (a change of state, not an
  exit, section 12). **Three states, not two.**
- **No German unit-linked *Stornoquote* was established** (gap 18). What is structurally true and
  worth stating: unit-linked lapse is **front-loaded** — highest in the first five years, where
  the acquisition charge is being taken and the value is furthest below premiums paid — and is
  **market-sensitive**, because the exit is at fund value on short notice [R1] [R2].
- **`[std]` behavioural defaults**, stated with their rationale rather than a source: a monthly
  lapse rate equivalent to **6 % p.a. in years 1–5, 3 % p.a. thereafter**, chosen to make the
  front-loading visible in the worked example; a **paid-up rate of 1 % p.a.**; and a
  ***Kapitalwahlrecht* take-up of 0 %** in the base run, so that the annuity path — the path the
  *Rentenfaktor* exists for — is the one the worked example demonstrates.

---

## Observed variation across insurers

**Read this first, and read it against the retrieval pass of 2026-08-30.** When this table was
written nothing carrier-specific had been observed for this product: no AVB, no
*Produktinformationsblatt*, no *Basisinformationsblatt* and no rate card had been retrieved or
searched. The pass changed that for **one** carrier — DEVK's full AVB and the sixteen
*Basisinformationsblätter* bound into its *Kundeninformation* [S2] [S15] — and for one product page
at Allianz [S3]; **no *Produktinformationsblatt* and no rate card was obtained at any carrier**, so
the table below is still **not** a table of observations across the market. It is a table of the
**dimensions along which German carriers are known to differ**, with the range argued from the
mechanics and the statutory bounds, and a companion table recording — honestly and mostly
negatively — what is actually established about each named carrier. Where the pass put a real
number against a dimension, the pass section says so and the number there governs.

### What is established, carrier by carrier

| Carrier | Established here | Source |
|---|---|---|
| DEVK | Publishes a *Kundeninformation* for a fondsgebundene Rentenversicherung, doc 03101, ed. 07/2024; death benefit before *Rentenbeginn* = fund value, at least premiums paid | [S2], via the sibling file |
| CosmosDirekt (Cosmos Leben) | Inception annuity factor computed on DAV 2004 R at an interest rate of currently 0 % p.a. — stated for the **classic** tariff | [S10], via the sibling file |
| Allianz Leben | Current bases at *Rentenbeginn* are those used at that time for immediately beginning annuities; *Treuhänderklausel* position publicly defended in Feb 2021 | [S3] [R22], via the sibling file |
| Zurich Deutscher Herold | The *Verbraucherinformation* series is titled "für Konventionelle Versicherungen", implying a fondsgebundene companion; at *Rentenbeginn* the higher of two factors applies | [S4], via the sibling file |
| Debeka | Discontinued its classic annuity tariff — the market-structure fact behind this product's dominance | [S14], via the sibling file |
| NÜRNBERGER | Publishes per-tariff AVB with codes in an `NIR`/`N` series | [S11], via the sibling file |
| Alte Leipziger, LV 1871, Continentale, HDI, Volkswohl Bund, Stuttgarter, WWK, myLife | **Nothing.** Named as real carriers of the right product with `[unverified]` product names | [S5]–[S9] [S12] [S13] [S18] |

### The dimensions of variation, and the argued range on each

| Parameter | Argued range across the German market | Where delib sits | Tag |
|---|---|---|---|
| Death benefit shape | *Fondsguthaben* / *Beitragsrückgewähr* / 100–110% of fund / guaranteed sum | *Beitragsrückgewähr* | [S2] for the shape; range [unverified] |
| Acquisition charge | 0% (Nettotarif) to 2.5% of *Beitragssumme* (the cap) | 2.5%, the cap | [R12] [R13] for the cap; interior [std] |
| Acquisition spreading | 5 years, uniform — statutory, no variation | 60 months | [R1] |
| Premium-based admin | 2% to 10% of each premium | 4.0% | [std] |
| Fund-based admin | 0.10% to 1.20% p.a. of *Fondsguthaben* | 0.30% p.a. | [std] |
| *Stückkosten* | 0 to 5 EUR per month | 3.00 EUR | [std] |
| Fund TER | 0.15% (ETF) to 2.00% p.a. (active) | 0.45% | [std] |
| *Kickback* crediting | none to full crediting of the trail | none (passive fund) | [std]; rule [unverified] |
| *Effektivkosten* | a spread BaFin calls "considerable"; no numeric range established | approx. 1% p.a. implied | [R10]; level [std] |
| Guaranteed *Rentenfaktor* | no level, range or time series established anywhere | 25.00 EUR per 10 000 EUR at 67 | [std], derived in section 9 |
| Factor rule at *Rentenbeginn* | max(guaranteed, current) — appears uniform | max(guaranteed, current) | [S4] [R22] |
| *Rentengarantiezeit* | 0, 5, 10, 15 years | 10 years, not priced separately | [std] |
| *Beitragsgarantie* | 0%, 60%, 80%, 90%, 100% of premiums | 0% — no guarantee | [std]; menu [unverified] |
| Guarantee technology | none / static hybrid / dynamic 2- or 3-pot / i-CPPI | none | section 13 |
| *Ablaufmanagement* | absent, opt-in, or opt-out default; 3 to 10-year ramps | 5-year monthly glide, switchable | [std] |
| Free fund switches | a fixed annual allowance to unlimited | unlimited within modelled behaviour | [std] |
| *Stornoabzug* | zero at many unit-linked tariffs; where present, must be quantified | zero | [R1]; level [std] |
| Minimum monthly premium | 25 to 50 EUR | 25 EUR | [unverified]; [std] |
| Entry ages | roughly 15/18 to the low 60s | 18 to 60 | [unverified]; [std] |
| *Rentenbeginn* age | commonly 62 (tax floor) to 85 | 67 | tax floor [R20]; choice [std] |

### What the corpus supports as a representative design

The representative delib contract is a **pure fondsgebundene Rentenversicherung with no
*Beitragsgarantie***: a single-life, Schicht-3, monthly-premium deferred annuity, one fund, units
bought monthly out of the premium after an acquisition instalment spread over 60 months, a
premium-based and a fund-based administration charge plus a monthly *Stückkosten*, a
*Beitragsrückgewähr* death benefit whose net amount at risk is charged monthly by unit
cancellation, a guaranteed *Rentenfaktor* applied at *Rentenbeginn* as the higher of the
guaranteed and the current factor, a *Rückkaufswert* equal to the *Fondsguthaben* with no
*Stornoabzug*, and *Fondswechsel*, *Zuzahlung*, *Teilentnahme*, *Ablaufmanagement* and
*Beitragsfreistellung* as switchable options.

**Why that design and not another**, in four points, each of which is an argument rather than an
observation because no observation was available:

1. **No guarantee**, because the guarantee technologies of section 13 cannot be demonstrated
   honestly in a deterministic projection, and because the guarantee-free form is a real and
   growing market form rather than a simplification of the only one sold.
2. ***Beitragsrückgewähr* death benefit**, because it is the only death benefit shape with
   corroboration anywhere in the delib corpus [S2], and because it is the shape that makes the
   *Risikobeitrag* mechanic non-trivial without making it dominant — the net amount at risk is
   positive early and vanishes later, so the model must compute it every month rather than once.
3. **Acquisition charge at the statutory cap, spread over five years**, because the cap [R12] and
   the spreading [R1] are the two acquisition-cost facts with corroboration, and a reference
   implementation should demonstrate the binding constraint rather than an unsourced interior
   point.
4. **A derived rather than a quoted *Rentenfaktor***, because no market level exists anywhere in
   this corpus and a quoted one would be an invention; the derivation in section 9 from a 0 %
   *Rechnungszins* [S10] and a generational annuitant table [R16] is checkable arithmetic and the
   result is labelled `[std]` at every appearance.

---

## Gaps and caveats

> **Read with the retrieval pass of 2026-08-30**, recorded at the end of this file. That pass
> closed or narrowed gaps **2, 3, 5, 9, 10, 11, 12, 13, 14, 15, 22, 23, 24, 25** and part of
> **4, 6, 7, 8, 17, 20, 27**, and it left **16, 18, 19, 21, 26** untouched. Where a gap below
> says a thing could not be established and the pass established it, the pass governs; the gaps
> are left as written because they record what was and was not known at drafting, which is the
> point of a research file.

1. **Superseded in part. No document was retrieved and no search was run for this product while it
   was written.** Both limits applied at full strength: HTTP egress was blocked for every relevant
   host, and the session's 200-call `WebSearch` budget was already exhausted before this file was
   begun. As drafted this file was therefore **weaker than its two delib siblings**, which at least
   had search summaries, and every statement of *structure* below the source list rests on the
   authoring model's knowledge of German insurance practice while every statement of *level* is
   `[std]` or `[unverified]`. **The pass of 2026-08-30 lifted that for the statutory spine and for
   one carrier**: fifteen instruments were read as canonical XML and DEVK's complete AVB and
   *Basisinformationsblätter* were read, which is what closed or narrowed the gaps listed in the
   note above. It did not lift it for the market: no rate card, no *Produktinformationsblatt* and
   no second carrier's clause text was obtained, so every *level* in this file that the pass did
   not reach is still `[std]` or `[unverified]`.

2. **Whether the *Mindestrückkaufswert* floor reaches the *Zeitwert* branch is unresolved.** § 169
   VVG expresses the five-year spreading floor on the *Deckungskapital*, and separately sends
   fondsgebundene contracts to a *Zeitwert* [R1]. The market implements the same protection inside
   the *Beitragsverrechnung*. Which of the two the statute requires, and what happens where the
   two diverge, was not established. Both readings give the same numbers on the delib design.

3. **The internal paragraph structure of § 169 VVG is unverified** — whether the *Zeitwert* rule is
   Abs. 3 Satz 2 or Abs. 4, and what it cross-refers to in the VAG since the 2016 recast. No delib
   document may cite a subsection number for it.

4. **No *Rentenfaktor* level, range or time series was established** — not for this product, not
   for the classic one in the sibling file, not from the rating house whose article is titled with
   the question [R23]. The `[std]` 25,00 € per 10 000 € at 67 is **derived arithmetic**, not a
   market observation, and a reader who needs a market level must go to a current
   *Produktinformationsblatt* or a Franke und Bornberg / Morgen & Morgen comparison.

5. **No *Basisinformationsblatt* for a fondsgebundene Rentenversicherung was located.** The one
   German PRIIP-BIB located anywhere in the delib corpus is for an endowment [S15]. Consequently
   **no performance-scenario return, no total-cost figure and no RIY value** in this file comes
   from an actual BIB. This is the single document that would close gaps 4, 6, 7 and 23 at once.

6. **No charge level of any kind was established at any carrier.** Not one *Abschlusskostenquote*,
   not one *Verwaltungskostensatz* in either form, not one *Stückkosten* amount, not one
   *Effektivkostenquote*, not one commission rate. **The entire charge stack of section 4 is
   `[std]`.** The only anchor is the 25 ‰ *Höchstzillmersatz* [R12], itself corroborated only at
   the level of a secondary consumer page in a sibling file.

7. **BaFin's "differ considerably" is qualitative** [R10]. No numeric *Effektivkosten* threshold,
   band, median or industry norm was established, in this file or in the sibling ones. The "of the
   order of 1 % per annum" in section 5 is **arithmetic on delib's own `[std]` stack**, not a
   market figure, and must never be quoted as one.

8. **The treatment of *Kickbacks* is unresolved on two axes**: whether and on what conditions an
   insurer may retain a *Bestandsprovision* under the IDD-derived inducement rules [R15], and how
   a rebate credited back to the contract is treated inside the PRIIPs cost calculation [R7] [R8].
   delib sidesteps both by using a passive fund that pays no trail.

9. **The *Ausgabeaufschlag* waiver is assumed, not established.** German insurers are understood
   to buy policy units at the *Rücknahmepreis*; no wording confirming a full waiver was seen.
   delib assumes a full waiver as `[std]`.

10. **The *Bewertungsstichtag* convention was not established** for any carrier — how many dealing
    days after premium receipt units are bought, and which price applies to a death, a surrender
    or a switch. On a monthly grid this is immaterial; on a daily one it is not.

11. **The *Shift* / *Switch* terminology is not consistent across German insurers** and this file
    asserts no mapping between the English words and the two operations. Each AVB defines its own.
    delib names the operations, not the labels. Any delib document that asserts "Shift means X"
    without a wording in front of it is wrong.

12. **Free-switch allowances, switch fees, *Zuzahlung* minima and maxima, *Teilentnahme* minima
    and the minimum remaining *Fondsguthaben* were not established** at any carrier. All are
    `[std]`.

13. **Whether deferring the *Rentenbeginn* inside the *Abrufphase* restates the guaranteed
    *Rentenfaktor* or only the current one was not established**, nor was the width of the
    *Abrufphase*. delib fixes the *Rentenbeginn* and records the option as unmodelled.

14. ***Ablaufmanagement* parameters were not established**: whether it is opt-in or a default,
    over how many years, in what tranches, and into what. The five-year monthly glide is `[std]`.

15. **The Landgericht Köln *Rentenfaktor* decision could not be identified.** No case number, no
    date, no parties — in this file or in the sibling one that reported it [R22]. Any delib
    document that mentions it must do so without a docket.

16. **No BGH decision on *Rückkaufswert*, *Kostenverrechnung* or *Stornoabzug* is cited** [R26].
    The line of authority is well known and no case reference could be established without a
    search. Nothing in delib rests on a court holding.

17. **The *Beitragsrückgewähr* fact is single-sourced**, and the source is a search summary read
    by a sibling researcher, not by this one [S2]. It is the best-evidenced fact in the file and
    it is still one summary of one carrier's document. The other three death-benefit shapes in
    section 6 are `[unverified]` in their entirety.

18. **No lapse rate, no paid-up rate and no German unit-linked *Stornoquote* was established.**
    The front-loaded and market-sensitive character of unit-linked lapse is a structural inference
    from the exit terms [R1] [R2], not an observation. All behavioural rates are `[std]`.

19. **No *Kapitalwahlrecht* take-up rate was established**, and it is the largest behavioural
    unknown in the product. delib's base run takes the annuity, which is a modelling choice made
    to exercise the *Rentenfaktor*, not an estimate of behaviour.

20. **The two-mortality-table statement is an inference from practice**, not from a wording: that
    the *Risikobeitrag* is priced on DAV 2008 T [R17] while the *Rentenfaktor* rests on DAV 2004 R
    [R16] is how German tariffs are built, but no AVB confirming it was seen. The DAV 2004 R half
    is corroborated at one carrier for the classic tariff [S10].

21. **The tax *Mindesttodesfallschutz* rule was not established for this product.** The "50 %
    rule" for contracts from 1 April 2009 is recorded in a sibling file for endowments; how it
    applies to a *Rentenversicherung* with and without a *Kapitalwahlrecht* is `[unverified]`, and
    delib's death benefit is not designed to satisfy it.

22. **The fondsgebunden *Teilfreistellung* is unverified in every particular** — the sentence
    within § 20 Abs. 1 Nr. 6 EStG, the 15 % figure, the equity-quota conditions and the
    interaction with the InvStG [R20] [R21]. The *Ertragsanteil* table is unverified except at age
    65.

23. **The *Modellrechnung* requirement was not pinned down**: how many assumed rates the VVG-InfoV
    prescribes for a fondsgebundene contract and at what levels [R7]. The three-rate market
    convention is recorded as convention.

24. **No entry-age, premium, term or sum-insured envelope was established** at any carrier. Every
    issue rule in the delib product-spec is `[std]`.

25. **The opening claim that this is the dominant German new-business savings form is unsourced.**
    No GDV new-business split by *Versicherungsart* was established [R25]. What is corroborated is
    only that a major carrier withdrew its classic tariff [S14] and that the supervisor's cost
    agenda is framed around capital-forming products generally [R10] [R11].

26. **Hybrid mechanics are named and not specified.** No reallocation rule, no CPPI multiplier, no
    *Wertsicherungsfonds* loss limit, no guarantee-pot accretion rule and no carrier's guarantee
    menu was established [S7] [S8] [S9]. Section 13's taxonomy is a description of a market, not a
    specification of any product, and delib implements none of it.

27. **The *Überschussbeteiligung* of a fondsgebundene contract is described structurally and not
    quantified.** No crediting mechanism was confirmed at any carrier, no declared rate was
    established, and the MindZV percentages are `[unverified]` [R14] [R5]. delib omits the credit
    and states the direction of the resulting bias.

28. **Living texts.** VVG, VVG-InfoV, DeckRV, MindZV, VAG, EStG and InvStG all change; the PRIIPs
    RTS was reworked with effect from 1 January 2023 `[unverified]`; the *Höchstrechnungszins*
    changed on 1 January 2025 `[unverified]`; BaFin's focus-risk agenda is annual [R11]. **Every
    paragraph number and every date in this file is `[unverified]`** and must be re-checked against
    the instrument before anything in the delib product documents relies on it.

---

## Retrieval pass, 2026-08-30

The network policy under which this file was written no longer applies. Every URL the file cites
was tried; fifteen German statutes were read as canonical XML from gesetze-im-internet; and
documents that could not be reached at a cited address were looked for once on the publisher's own
site. **The "Citation discipline and retrieval conditions" section above now carries both halves** —
the conditions of the original research, which are kept because rewriting them away would
misdescribe how the entries below were first arrived at, and a summary of this pass, which defers
to this section on detail. This section is the operative record of what changed.

### Entries that moved to `Retrieved: yes`

| Entry | What was read |
|---|---|
| **[S2]** | DEVK *Kundeninformation* 03101/07/2024, tariff **L/N FR1**, "DEVK-Fondsrente vario" — PDF, 195 pp., at `www.devk.de/media/...` after the cited `medien.devk.de` address returned 403. *Verbraucherinformationen*, *Tarifbestimmungen*, the full AVB (§§ 1–27), the *Anhang* with the calculation bases, the tax notes and the glossary |
| **[S15]** | Sixteen *Basisinformationsblätter* bound into [S2] at pp. 71–119 (L FR1 and N FR1 × 1 000 € annual / 10 000 € single × 12 / 20 / 30 / 40 years), plus the option-specific sheets from p. 120 |
| **[S16]**, in part | The *Verbraucherinformationen* limb of [S2]; the *Produktinformationsblatt* limb remains unlocated |
| **[R1] [R2] [R3] [R4] [R5] [R6]** | VVG §§ 169, 168, 165, 163, 153, 152 and 7, canonical XML, *Stand* zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156. §§ 154 and 155 read for [REG-R25] |
| **[R7]** | VVG-InfoV § 2, complete text — unlike the VVG per-section pages, this one carries it |
| **[R10]** | BaFin *Merkblatt 01/2023 (VA)*, complete, dated **08.05.2023** |
| **[R11]** | BaFin *Risiken im Fokus 2026*, "Kosten von kapitalbildenden Lebensversicherungen", complete; and the 2022 BaFinJournal survey article it refers back to, "Wenn Lebensversicherungen zu viel kosten" |
| **[R12]** | DeckRV §§ 1–6, canonical XML, *Stand* Art. 1 V v. 19.7.2024 I Nr. 250 |
| **[R14]** | MindZV §§ 1, 3, 4, 6, 7, 8, canonical XML, *Stand* Art. 1 V v. 7.7.2020 I 1688 |
| **[R15]** | VAG §§ 124, 125, 138, 139 and Anlage 1, canonical XML |
| **[R18]** | DAV *Ergebnisbericht*, PRIIP Kategorie 4, 1 July 2025 — PDF, 30 pp.; preamble, scope and section 1 |
| **[R19] [R20]** | EStG § 22 including the *Ertragsanteil* table, § 20 Abs. 1 Nr. 6 including Satz 9, and § 52 Abs. 28 |
| **[R22]** | Finanztip *Rentenfaktor* and both versicherungenmitkopf pages |

[S3] is partial: the Allianz **InvestFlex product page** was read and settles the product name and
the design menu, but the *Bedingungswerk* host answers 403, so **no Allianz clause text** was
obtained. [R21] is contents-page only.

### Entries that stay `Retrieved: no`, with the reason

**404 at the cited URL:** [R9] — BaFin's 2022 PRIIPs *Fachartikel* is gone from the address the
sibling research recorded, though BaFin's own index still lists it; no replacement was found.
**403 from the document host:** the Allianz *Bedingungswerk* behind [S3].
**Soft 404 on the publisher's site:** the one HDI address tried for [S13].
**No URL was ever established, so nothing was opened:** [S1], [S4]–[S12], [S14], [S17], [S18],
[R13], [R16], [R17], [R23]–[R26]. For [R16] and [R17] that is by nature — DAV tables are not
public — though the *use* of DAV 2004 R and of a DAV 1994 T derivative on this product is now
established from [S2].

### What a retrieved document contradicted

1. **The *Risikobeitrag* mortality basis.** This file has DAV 2008 T [R17]. DEVK prices it on
   *"einer mit 65 Prozent gewichteten geschlechtsunabhängigen Ausscheideordnung auf Basis der
   Sterbetafel DAV 1994 T"*, and uses DAV 2008 T for its underwritten *Risiko-Zusatzversicherung*.
   The two-basis structure holds; the identification does not.
2. **The guaranteed *Rentenfaktor* level and shape.** Gap 4 assumed no level existed. At delib's
   own anchor cell the real figure is **22,91 €** against the derived 25,00 €, and the real factor
   falls with the deferment (25,22 / 24,12 / 22,91 / 21,83 € at 12 / 20 / 30 / 40 years to age 67)
   where delib's is flat in it. **A model fact; not changed in this pass.**
3. **The *Modellrechnung*.** [R7] treats it as owed. § 154 Abs. 1 Satz 2 VVG excludes unit-linked
   contracts from it entirely.
4. **The PRIIPs category.** [R8] assumed a pure unit-linked contract is Category 2 with scenarios
   from the funds' own history. The DAV treats Schicht-3 annuities as **Kategorie 4**, because
   cost deductions and biometric components make the pots inseparable.
5. **The *Sparte* name.** VAG Anlage 1 Nr. 21 is *"Fondsgebundene Lebensversicherung"*, not
   *"fonds- und indexgebundene Lebensversicherung"*.
6. **The *Anlagestock*.** § 125 Abs. 5 VAG makes it *"eine Abteilung des Sicherungsvermögens"* —
   inside the *Sicherungsvermögen*, not outside it.
7. **The five-year spreading.** It is § 169 **Abs. 3**, on the *Deckungskapital* branch; Abs. 4
   sends a unit-linked contract to the *Zeitwert* and applies Abs. 3 only *"im Übrigen"*. And a
   real tariff spreads only **part** of its acquisition cost over five years, taking the rest as a
   percentage of every premium for the whole term — so the month-60 cliff is delib's, not the
   market's.
8. **"BaFin says *Effektivkosten* differ considerably between providers."** That sentence is in
   *Risiken im Fokus* [R11], not in the *Merkblatt* [R10], whose "erheblich" passage is about
   *Stückkosten* making the *Effektivkosten* vary with premium size.
9. **"No numerical threshold, band, median or sector benchmark appears."** [R11] gives a
   distribution at delib's own model point: **1,90 %** weighted mean at entry age 37 over 30
   years, quartiles **1,30 / 1,64 / 2,35 %**, insurers above **4 %** at every age-and-term
   combination.
10. **The *Kickback* range.** delib argues 0 %–0,50 % p.a.; the observed weighted mean is just
    over 0,30 % and the top of the range is **over 1,20 %**.
11. **The *Widerruf* repayment.** § 152 Abs. 3 Nr. 2 can return the first year's premiums where
    that is more favourable — not, as this file said, simply the unit value at cancellation.
12. **"No crediting mechanism was confirmed at any carrier"** (gap 27). DEVK credits a
    premium-based *Grundüberschussanteil* as units before *Rentenbeginn*, and the MindZV minima
    are 90 % / 90 % / 50 %.
13. **The 50–300 fund range.** DEVK offers **nine** funds from one house, minimum 10 % each, at
    most five per contract.
14. **The *Rentengarantiezeit* menu.** Not 0/5/10/15; DEVK's runs **5 to 25 years**.
15. **The *Beitragsgarantie* menu.** Not 0/60/80/90/100 %; Allianz's runs **10 % to 90 % in
    10-point steps**.
16. **"The LG Köln decision could not be identified"** (gap 24 / [R26]). It is **LG Köln, Urteil
    vom 8. Februar 2023, Az. 26 O 12/22**, against Zurich, reported as *rechtskräftig*.
17. **The dominance claim** (gap 25). BaFin states it: *"die im Neugeschäft dominierenden
    fondsgebundenen Produkte"*, in a market of about 59 million contracts with 2,4 million written
    in 2024.

### Standing gaps this pass did not close

No *Produktinformationsblatt* for any carrier, so no carrier's charge rates were read from the
document that is supposed to carry them — the rates in hand come from *Basisinformationsblätter*
instead. No lapse rate, paid-up rate or *Kapitalwahlrecht* take-up anywhere. No clause text from
any carrier but DEVK. No DAV table. No BGH *Rückkaufswert* decision. No GDV new-business split by
*Versicherungsart*. And, for the LVRG [R13], no Bundesgesetzblatt citation and no confirmation of
the 40 ‰ → 25 ‰ history or the 1 January 2015 date, both of which live in amending instruments
rather than in the consolidated texts read here.
