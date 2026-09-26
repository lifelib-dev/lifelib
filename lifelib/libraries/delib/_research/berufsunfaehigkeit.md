# Selbständige Berufsunfähigkeitsversicherung (SBU) — research notes (Germany)

Research notes for the German individual *selbständige Berufsunfähigkeitsversicherung* — the
standalone occupational-disability contract that pays a monthly *BU-Rente* for as long as the
*versicherte Person* is *berufsunfähig*, waives the premium (*Beitragsbefreiung*) for the same
period, and pays nothing at all if the insured remains able to work. It is the flagship German
biometric product: the one contract the German market itself treats as indispensable, sold on a
statutory definition that is unusually favourable to the insured by international standards, and
priced on occupational classes whose spread is wider than in any other retail life product.

**In scope.** The individual, privately written, standalone (*selbständig*) BU contract on a single
life, sold by a *Lebensversicherungsunternehmen* under §§ 172–177 VVG, with a level *Bruttobeitrag*
guaranteed for the whole term, a *Zahlbeitrag* below it funded out of the *Überschussbeteiligung*,
an agreed monthly *BU-Rente*, an agreed *Endalter* for both cover and benefit, and the standard
option set (*Beitragsdynamik*, *Leistungsdynamik*, *Nachversicherungsgarantie*,
*Verlängerungsoption*, *Karenzzeit*, and — for medical occupations — the *Infektionsklausel*). The
*Berufsunfähigkeits-Zusatzversicherung* (BUZ), the same cover sold as a rider on a
*Rentenversicherung*, a *Kapitallebensversicherung* or a *Basisrente*, is treated here as a wrapper
variant of the same liability, because it is: the BU risk, the claim procedure, the *Nachprüfung*
and the *Beitragsbefreiung* are identical, and only the tax treatment and the interaction with the
host contract's premium differ.

**Out of scope, and said so where it matters.** *Erwerbsunfähigkeitsversicherung* (EU cover, keyed
to any occupation rather than the last one) and *Grundfähigkeitsversicherung* (keyed to the loss of
defined basic abilities — seeing, speaking, walking, using the hands) are different products with
different definitions and different pricing bases; they are named below only where they bound the
BU market from beneath. *Dread-disease* / *schwere Krankheiten* cover, *Unfallversicherung*,
*Krankentagegeld*, and the *Pflegerentenversicherung* (delib product 10) are separate liabilities.
*Betriebliche Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung* (including
the *Kollektiv-BU* and *bAV-BU* forms), *private Krankenversicherung* and the statutory
*Erwerbsminderungsrente* itself are outside the delib library; the last of these is nevertheless
described at length in section 24, because the German BU contract is designed as a top-up on it and
its level is the reason the private product exists at all.

These notes are the **citation ground truth** for the delib `berufsunfaehigkeit` product documents.
Source ids **S1..S16** and **R1..R31** below are **frozen — never renumber**; unused ids are simply
omitted downstream, leaving gaps, and `sources.md` records which are absent and why.
Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

This section has two halves. The first records the conditions the research was **done** under on
2026-08-29; the second records what the **re-verification** of 2026-08-30 established. The first is
not withdrawn — it is how this file came to say what it says — and the second is what a reader
should now weigh each entry by.

**No document in this file had been retrieved when it was written. Not one.** Two independent limits
applied while it was drafted, and they compounded.

**Limit 1 — direct HTTP egress was blocked.** An organisation network policy refuses `WebFetch` and
`curl` (HTTP 403 at the egress gateway) for every host outside a short package-registry allowlist.
The hosts that matter here were all tried and all refused: `gesetze-im-internet.de` (VVG, VAG,
SGB VI, EStG, DeckRV, MindZV, IfSG), `bafin.de`, `gdv.de`, `aktuar.de`,
`deutsche-rentenversicherung.de`, `bundesfinanzministerium.de`, `destatis.de`, `dejure.org`,
`buzer.de`, `bundesgerichtshof.de` and `de.wikipedia.org`. No *Bedingungswerk*, no
*Produktinformationsblatt*, no *Basisinformationsblatt*, no statutory text, no DAV *Ergebnisbericht*
and no BaFin publication was opened.

**Limit 2 — the session's `WebSearch` budget was already exhausted before this product was
reached.** The 200-call cap was shared across the whole delib build and was consumed by the
regulatory research and by the two products written before this one. **This file therefore had no
research channel at all while it was drafted — neither retrieval nor search.** Its first draft was
written from the authoring model's own knowledge of German insurance law and market practice, under
the discipline the delib house rules impose for exactly this case.

What followed, and it governed every line of the draft:

1. **An `[S#]` or `[R#]` tag was a pointer, not a certificate.** It named the document a claim must
   be checked against before it is relied on. It did **not** assert that anyone had read that
   document. Every source entry carried `Retrieved: no — direct HTTP egress blocked in the build
   environment; no search corroboration (session search budget exhausted)`, and none said otherwise.
   **This is the rule the re-verification changed**; the paragraph after the list says how far.
2. **There are no quotations.** Not one German sentence in this file is presented as verbatim
   statutory or contractual wording, because no wording was read. Substance is given in the author's
   own words, in English, with the terms of art kept in German.
3. **No URL, document number, edition date, *Bundesgesetzblatt* citation or page count is invented.**
   Where a canonical URL form is confidently known — `https://www.gesetze-im-internet.de/vvg_2008/__172.html`
   for § 172 VVG — it is given and marked `[unverified]`, because no search returned it. Everywhere
   else the entry says `URL: not established`.
4. **`[unverified]` is used generously.** Every specific paragraph number, effective date, monetary
   amount, percentage, market share, table name and statistic below carries it. It is *not* applied
   to the general shape of a well-established mechanic — that the *Nachprüfung* exists, that the
   market waives the *abstrakte Verweisung*, that the premium is quoted as a *Brutto*/*Zahlbeitrag*
   pair — because tagging those would drown the signal. The rule: the moment a claim becomes
   **specific and numeric**, it needs the tag.
5. **Uncertain levels are `[std]` parameters, not citations.** Where the mechanic is certain and the
   level is not — a lapse rate, an occupational factor, a *Beitragsverrechnung* ratio — this file
   ships a `[std]` value with a rationale and an argued range. A `[std]` number is honest about
   being a construction; a guessed `[S4]` number is not, and there are none.

**The re-verification of 2026-08-30.** The policy was lifted and the citations were checked against
the primary documents. Library-wide, all fifteen German instruments delib cites were read as
canonical XML from `gesetze-im-internet.de` with each law's amendment `Stand` recorded, 950
statutory section references were checked and 950 were correct, and insurer AVB,
*Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read; **501
of the library's 805 source entries, 62 %, now read `Retrieved: yes`.** For this product: **26 of
the 47 entries below read `Retrieved: yes` and 21 read `no`.** Eight documents were opened — the GDV
model conditions for the SBU, the BUZ and the BU-with-AU variant, and carrier wordings from Alte
Leipziger, NÜRNBERGER, VOLKSWOHL BUND, Debeka and CosmosDirekt — and every statute and statutory
instrument the product turns on was read as canonical XML. What stayed shut is named per entry, and
the reasons are not all the same kind: a carrier page that resolves but serves no document link
([S3], [S5], [S8]); a document generated per quotation, so that no specimen is published ([S13]);
DAV tables that are the association's property and appear at no public address ([R16], [R17]) — the
one status no network can change; a study or series that was not located on the publisher's site
([R18], [R20], [R21]); and, for the rest, an entry the pass did not attempt because nothing in this
product is asserted from it. Rule 1 above is superseded exactly that far and no further.

**What an entry now means.** A **`Retrieved: yes`** line means the document was opened and the
passage the entry rests on was read, and the line records the edition, page count or statutory
`Stand`. A **`Retrieved: no`** line means the entry is still **a pointer rather than a certificate**,
and it is marked as one. **The re-verification changed things**: it corrected claims the drafted
text got wrong, and the corrections sit in the entries themselves, in the *Observed variation*
table and in the gaps register. Treat a claim in this file as sound where its entry says
`Retrieved: yes`, and as provisional where it does not.

**Consequence for the downstream documents.** `product-spec.md` and `technical-notes.md` are
unusually `[std]`-heavy and unusually explicit about it, and the pass did not change that: what
remains unretrieved is every **quantitative** source — no price, no rate card, no occupational
table, no DAV table. That is the correct outcome, not a defect: the *mechanics* of the German BU
contract are well established and are set out below in full, and it is only the *levels* — rating
factors, charge loadings, decrement tables, market statistics — that this file cannot source. The
gaps register at the foot should be read before any figure is used.

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on:

| Term | Gloss |
|---|---|
| *Berufsunfähigkeit* (BU) | Occupational disability: inability to follow the **last exercised occupation**, as it was arranged before the impairment |
| *Selbständige Berufsunfähigkeitsversicherung* (SBU) | The standalone BU contract, sold on its own rather than as a rider |
| *Berufsunfähigkeits-Zusatzversicherung* (BUZ) | The same cover written as a rider on a *Renten-*, *Kapitallebens-* or *Basisrentenversicherung* |
| *BU-Rente* | The monthly disability annuity, the product's only substantive benefit |
| *Versicherte Person* / *Versicherungsnehmer* | The life insured / the policyholder — frequently the same person here, but not necessarily |
| *Zuletzt ausgeübter Beruf* | The last exercised occupation — the reference occupation for the whole test |
| *Lebensstellung* | Standing in life: the income level and social position the reference occupation conferred. The limiting concept for any *Verweisung* |
| *Abstrakte Verweisung* | Referring the insured to an occupation they *could* take up, without their actually doing so |
| *Konkrete Verweisung* | Referring the insured to an occupation they **actually** exercise |
| *Prognosezeitraum* | The forward-looking period over which the inability must be expected to last — six months in the market standard |
| *Karenzzeit* | An agreed deferment between the onset of BU and the first benefit payment |
| *Rückwirkende Leistung* | Benefit paid retroactively to the onset of BU once the claim is recognised |
| *Leistungsantrag* | The claim application |
| *Anerkenntnis* | The insurer's declaration that it accepts liability. *Befristetes Anerkenntnis* = a time-limited one |
| *Leistungsprüfung* | The insurer's assessment of the claim |
| *Nachprüfung* / *Nachprüfungsverfahren* | The periodic re-examination of a claim already accepted |
| *Einstellungsmitteilung* / *Änderungsmitteilung* | The notice by which the insurer ends benefit after a *Nachprüfung* |
| *Reaktivierung* | Recovery: the insured ceases to be *berufsunfähig* and the contract reverts to premium-paying cover |
| *Beitragsbefreiung* | Waiver of premium while the BU benefit is in payment |
| *Leistungsdauer* / *Versicherungsdauer* | The period benefits may run for / the period during which a BU may incept and be covered |
| *Endalter* / *Leistungsendalter* | The attained age at which the *Leistungsdauer* ends — 65 or 67 in the market |
| *Wiedereingliederungshilfe* | A lump sum paid to support a return to work |
| *Umorganisationspflicht* | The self-employed insured's duty to reorganise the business before claiming |
| *AU-Klausel* / *Arbeitsunfähigkeitsklausel* | Benefit triggered by a certificate of six months' *Arbeitsunfähigkeit*, without a BU determination |
| *Infektionsklausel* | Treats an official ban on practising imposed for infection reasons as BU, for medical occupations |
| *Beitragsdynamik* / *Leistungsdynamik* | Annual pre-claim escalation of premium and *BU-Rente* / annual escalation of the *BU-Rente* in payment |
| *Nachversicherungsgarantie* | The right to increase the *BU-Rente* on defined life events without renewed underwriting |
| *Verlängerungsoption* | The right to extend the *Endalter* without renewed underwriting |
| *Berufsgruppe* | Occupational rating class |
| *Gesundheitsprüfung* / *Gesundheitsfragen* | Medical underwriting / the application's health questions |
| *Risikozuschlag* / *Ausschlussklausel* | Extra-risk premium loading / exclusion of a named condition |
| *Risikovoranfrage* | Anonymous pre-application enquiry, made to avoid a recorded decline |
| *Vorvertragliche Anzeigepflicht* | The applicant's pre-contractual duty of disclosure, § 19 VVG |
| *Bruttobeitrag* (*Tarifbeitrag*) / *Zahlbeitrag* (*Nettobeitrag*) | The guaranteed maximum premium / the premium actually charged after surplus is applied |
| *Beitragsverrechnung* | Applying surplus as an immediate reduction of the premium charged — the standard *Überschussverwendung* in BU |
| *Überschussbeteiligung* | Participation in surplus, § 153 VVG, applied to BU through § 176 VVG |
| *Deckungsrückstellung* / *Rückkaufswert* | The actuarial reserve / the surrender value, § 169 VVG via § 176 |
| *Zillmerung* / *Höchstzillmersatz* | Financing acquisition costs through the reserve / its statutory cap |
| *Rechnungsgrundlagen erster / zweiter Ordnung* | Prudent (pricing and reserving) bases / best-estimate bases |
| *Invalidisierungswahrscheinlichkeit* / *Reaktivierungswahrscheinlichkeit* | Probability of becoming BU / of recovering from it |
| *Anerkennungsquote* | The proportion of decided claims the insurer accepts |
| *Erwerbsminderungsrente* (EM-Rente) | The statutory disability pension, §§ 43, 240 SGB VI — *volle* and *teilweise* |
| *Versorgungslücke* | The gap between the statutory pension and the income it has to replace |
| *Angemessenheitsgrenze* | The insurer's cap on the insurable *BU-Rente* as a fraction of income |

---

## Primary sources

**The blanket retrieval status these entries once carried no longer holds.** On 2026-08-30 the
documents were tried again and eight were read: the GDV model conditions for the SBU, the BUZ and
the BU-with-AU variant (S1, S2, and the AU variant cited at S8), and carrier wordings from Alte
Leipziger (S4), NÜRNBERGER (S6), VOLKSWOHL BUND (S9), Debeka and CosmosDirekt (S12). Each entry
below now carries its **own** `Retrieved` line and, where one was found, its URL; where the line
still says *no*, it says why. An entry that was not read remains a **known reference**: publisher,
document type, and what that class of document contains and why this product needs it. The
per-entry lines in `products/berufsunfaehigkeit/sources.md` carry the clause detail read from each. Where a
*Content* block records a specific parameter it is the author's recollection, tagged `[unverified]`,
recorded so a later reader knows **which document to open to check it**. Insurer names are real
German life insurers, all of which write BU; **tariff and product names are recalled, not
confirmed**, and every one carries `[unverified]`.

### S1 — GDV, *Allgemeine Bedingungen für die selbständige Berufsunfähigkeitsversicherung* (unverbindliche Musterbedingungen)
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin
- Doc type: *unverbindliche Musterbedingungen* — non-binding model conditions circulated to member
  undertakings, which most German insurers use as the drafting skeleton for their own AVB
- URL: `https://www.gdv.de/gdv/service/musterbedingungen` (index) → the SBU model conditions PDF given on the `Retrieved` line
- Retrieved: **yes** — PDF, 25 pp., *Stand: 21.07.2025*, read 2026-08-30 at `https://www.gdv.de/resource/blob/6326/f89f31db43116561321679a5a3b29682/01-allgemeine-bedingungen-fur-die-berufsunfahigkeits-versicherung-0-pdf-data.pdf`, linked from the GDV's own *Musterbedingungen* index
- Content: the single most important document for this product, and the one whose absence hurts
  most. The GDV maintains model AVB for the standalone BU cover; individual insurers depart from
  them in the direction of the policyholder (waiving the *abstrakte Verweisung*, shortening the
  *Prognosezeitraum*, adding an *AU-Klausel*) and rarely against. The model conditions are the
  reason the German BU market is structurally uniform: the definition of *Berufsunfähigkeit*, the
  *Anerkenntnis* and *Nachprüfung* clauses, the *Mitwirkungspflichten* and the exclusion list all
  read alike across carriers because they descend from a common model text. **Read on 2026-08-30
  (Stand 21.07.2025), which corrects two things recorded here.** The model text leaves **both** the
  degree and the prognosis period blank, footnoted "Unternehmensindividuell zu ergänzen", so neither
  the 50 % nor any period descends from it — carriers fill them, and one large carrier's prognosis
  period is three years, not six months. And the six months belongs to the **retrospective fiction**
  of § 2 Abs. 2, which is a separate clause from the prognosis limb of § 2 Abs. 1. **Note carefully**: the
  GDV model conditions are *unverbindlich* — non-binding — precisely because binding recommended
  conditions would be a cartel; every insurer's own AVB is the operative document, and a claim made
  from the model text alone is `[unverified]` against any particular contract.

### S2 — GDV, *Allgemeine Bedingungen für die Berufsunfähigkeits-Zusatzversicherung* (Muster-BUZ)
- Publisher: GDV
- Doc type: *unverbindliche Musterbedingungen* for the rider form
- URL: as S1's index → the BUZ model conditions PDF given on the `Retrieved` line
- Retrieved: **yes** — PDF, 15 pp., *Stand: 15.11.2022*, read 2026-08-30 at `https://www.gdv.de/resource/blob/6328/f54c89730c9ba9043d8e8f023f38824a/02-allgemeine-bedingungen-fuer-die-berufsunfaehigkeits-zusatzversicherung-0-pdf-data.pdf`
- Content: the rider counterpart of S1. The substantive BU definition, *Anerkenntnis* and
  *Nachprüfung* clauses are the same; the rider text adds the interaction with the host contract —
  that the *Beitragsbefreiung* covers the **whole** premium of the host contract and not merely the
  rider premium, that the rider ends when the host contract ends, that the rider may not be
  continued alone if the host is surrendered, and that a *beitragsfreie* host contract carries a
  correspondingly reduced or extinguished rider. Needed here because delib's `basisrente` product
  (product 5) and `klassische_rentenversicherung` (product 2) may both carry this rider, and because
  the tax treatment of a BUZ inside a *Basisrente* is materially different from that of an SBU
  (section 23).

### S3 — Allianz Lebensversicherungs-AG, AVB for the *selbständige Berufsunfähigkeitsversicherung*, with the associated *Produktinformationsblatt*
- Publisher: Allianz Lebensversicherungs-AG, Stuttgart — the largest German life insurer
- Doc type: AVB (*Bedingungswerk*) plus *Produktinformationsblatt*; URL: not established
- Retrieved: **no** — the Allianz BU product page resolves on 2026-08-30 and points to a document index at `https://www.allianz.de/service/dokumente/#berufsunfaehigkeits-versicherung`, which serves no BU *Bedingungswerk* in its HTML: its per-product sections are assembled client-side
- Content: the most widely read BU wording in the market. Expected to contain the standard
  50 % / six-month definition, waiver of the *abstrakte Verweisung*, a *Nachversicherungsgarantie*
  on a defined event list, a *Beitragsdynamik* option, occupational classification into a small
  number of *Berufsgruppen*, and the *Brutto*/*Zahlbeitrag* pair. Allianz also writes BU as a rider
  in its *Rentenversicherung* and *Basisrente* ranges. **No product name, tariff code, edition date
  or parameter from any Allianz document is asserted anywhere in this file.**

### S4 — Alte Leipziger Lebensversicherung a. G., AVB and *Tarifbestimmungen* for its BU range
- Publisher: Alte Leipziger Lebensversicherung a. G., Oberursel; URL: `https://www.alte-leipziger.de/privatkunden/einkommensschutz/berufsunfaehigkeitsversicherung`, the product page that links the AVB and the AU-clause sheet
- Retrieved: **yes** — AVB, PDF, 33 pp., document mark *pm 2300*, at `https://www.alte-leipziger.de/-/media/druckstuecke/allgemeine-bedingungen/pm/2300/bedingungenallgemeinebedingungenberufsunfaehigkeitsversicherungpm2300pdf/bedingungen-allgemeine-bedingungen-berufsunfaehigkeitsversicherung-pm2300.pdf`, and the AU-clause sheet *pv 483.02-12.2025*, PDF, 2 pp.; both read 2026-08-30. The *Tarifbestimmungen* were not found at a public address
- Content: one of the small group of carriers the German broker market treats as BU specialists,
  alongside Nürnberger, LV 1871, Swiss Life, HDI and Volkswohl Bund. The tariff family is recalled
  as carrying a `BV` prefix `[unverified]`. This is the class of document that would settle the
  *Berufsgruppen* count, the *Nachversicherungsgarantie* event list and caps, the
  *Verlängerungsoption* window and the *Karenzzeit* menu — none of which this file can source.

### S5 — LV 1871 (Lebensversicherung von 1871 a. G. München), AVB and PIB for its BU range
- Publisher: Lebensversicherung von 1871 a. G. München; URL: `https://www.lv1871.de/berufsunfaehigkeitsversicherung/` resolves but serves no document
- Retrieved: **no** — `https://www.lv1871.de/berufsunfaehigkeitsversicherung/` resolves on 2026-08-30 and serves no document link; the *Bedingungen* sit behind the broker portal
- Content: LV 1871 markets a BU range under a "Golden BU" family name `[unverified]`, with tiers
  differing chiefly in the option set (*Nachversicherungsgarantie* breadth, *AU-Klausel*,
  *Leistungsdynamik*) rather than in the core definition. Recorded because a tiered range on one
  risk basis is the normal German shape, and a reference implementation should model the base tariff
  and treat the enhancements as switchable options.

### S6 — NÜRNBERGER Lebensversicherung AG, AVB, *Tarifbestimmungen* and *Berufsgruppenverzeichnis*
- Publisher: NÜRNBERGER Lebensversicherung AG, Nürnberg; URL: `https://www.nuernberger.de/beruf-vorsorge/existenzsicherung/berufsunfaehigkeitsversicherung/`, the product page that links the AVB and the *Kundeninformation*
- Retrieved: **yes** for the AVB — PDF, 28 pp., document mark *GN331072_202607*, at `https://www.nuernberger.de/medien/4allportal/gn331072_p.pdf`, and the *Kundeninformation* *LV005_565_202607*, PDF, 3 pp.; both read 2026-08-30. **The *Berufsgruppenverzeichnis* was not retrieved** and the AVB never uses the word *Berufsgruppe*
- Content: historically one of the largest BU books in Germany `[unverified]`. The document class
  that matters most here is the ***Berufsgruppenverzeichnis*** — the occupational classification
  list, running to hundreds of named occupations mapped to rating classes. No German insurer's full
  list was retrievable, and the classification is the single largest driver of the premium
  (section 16). Nürnberger also insures occupations other carriers decline.

### S7 — Swiss Life AG, Niederlassung für Deutschland, AVB and PIB for its BU range
- Publisher: Swiss Life AG, Niederlassung für Deutschland, München; URL: not established
- Retrieved: **no** — not attempted; nothing in this product is asserted from Swiss Life
- Content: regarded in the broker market as a wording-quality benchmark `[unverified]`, in
  particular on the *Verweisung* clauses and on the treatment of the self-employed
  (*Umorganisationspflicht*) — the most product-specific part of the German BU definition and the
  part least visible from consumer material.

### S8 — HDI Lebensversicherung AG, AVB and PIB for its BU range
- Publisher: HDI Lebensversicherung AG, Köln (Talanx group); URL: `https://www.hdi.de/versicherungen/einkommensschutz/berufsunfaehigkeitsversicherung/` resolves but serves no document
- Retrieved: **no** — `https://www.hdi.de/versicherungen/einkommensschutz/berufsunfaehigkeitsversicherung/` resolves on 2026-08-30 and serves no document link. The *AU-Klausel*'s parameters were instead established from S4 and S12, and the GDV model conditions for the BU-with-AU variant were read (PDF, 27 pp., at `https://www.gdv.de/resource/blob/29838/8be269e678c792295c1ac6881f1c800b/allgemeine-bedingungen-fuer-die-berufsunfaehigkeits-versicherung-mit-zusaetzlicher-absicherung-bei-arbeitsunfaehigkeit-data.pdf`)
- Content: HDI markets its BU under an "EGO" family name `[unverified]`, with a tier structure and a
  strong academic/office proposition. Recorded as one of the carriers whose wording would settle the
  *AU-Klausel* parameters — the certified duration required, the maximum benefit period under the
  clause, and whether payment under it is set off against a later BU recognition (section 11).

### S9 — VOLKSWOHL BUND Lebensversicherung a. G., AVB and *Tarifbestimmungen*
- Publisher: VOLKSWOHL BUND Lebensversicherung a. G., Dortmund; URL: `https://www.volkswohl-bund.de/einkommenssicherung/berufsunfaehigkeit/`, the product page that links the AVB
- Retrieved: **yes** — PDF, 22 pp., document mark *BED.SBU.0126*, tariffs SBU, SBUJ, SBU+, SBUJ+, read 2026-08-30 at `https://druckstuecke.volkswohl-bund.de/api/products/1574/documents/Allgemeine_Bedingungen_für_die_Selbstständige_Berufsunfähigkeits-Versicherung.pdf`
- Content: a broker-channel BU specialist. Recorded because its range is one of those that prints a
  *Bruttobeitrag* and a *Zahlbeitrag* side by side in the quotation — the practice this file needs
  documented (section 18) and which no retrieved document confirms.

### S10 — Barmenia Lebensversicherung a. G., AVB and PIB for its standalone BU cover
- Publisher: Barmenia Lebensversicherung a. G., Wuppertal (Barmenia Gothaer group); URL: not established
- Retrieved: **no** — not attempted; nothing in this product is asserted from Barmenia
- Content: Barmenia has sold standalone BU under a "SoloBU" name `[unverified]`. Recorded chiefly as
  the carrier most associated with the standalone rather than the rider form, and as a reminder that
  the German word for the standalone contract — *selbständige* BU — is itself a product name in some
  ranges.

### S11 — Dialog Lebensversicherungs-AG (Generali Deutschland), AVB and *Tarifbestimmungen*
- Publisher: Dialog Lebensversicherungs-AG, Augsburg — the Generali group's broker-channel
  biometric-risk carrier; URL: not established
- Retrieved: **no** — not attempted; nothing in this product is asserted from Dialog
- Content: the German market's clearest example of a carrier writing **only** biometric risk —
  *Risikolebensversicherung* and BU — with no savings business. That makes its
  *Überschussbeteiligung* pure risk and expense surplus with no interest component, which is the
  cleanest illustration of where the *Brutto* / *Zahlbeitrag* gap in a BU tariff comes from
  (section 18). A tariff name with a "professional" suffix is recalled `[unverified]`.

### S12 — Further German BU carriers, *Bedingungswerke* and *Produktinformationsblätter* (document class)
- Publishers, all real German life insurers writing BU: R+V Lebensversicherung AG; Debeka
  Lebensversicherungsverein a. G.; Continentale Lebensversicherung AG; Gothaer Lebensversicherung
  AG; Die Stuttgarter Lebensversicherung a. G.; Zurich Deutscher Herold Lebensversicherung AG;
  ERGO Vorsorge Lebensversicherung AG; AXA Lebensversicherung AG; Hannoversche Lebensversicherung
  AG; CosmosDirekt (Generali Deutschland Lebensversicherung AG); Württembergische
  Lebensversicherung AG; Baloise Lebensversicherung AG Deutschland; die Bayerische (Bayerische Beamten
  Lebensversicherung a. G.); universa Lebensversicherung a. G.; DEVK; SIGNAL IDUNA
  Lebensversicherung a. G.; Provinzial; HUK-COBURG-Lebensversicherung AG
- Doc type: AVB, *Tarifbestimmungen*, *Produktinformationsblätter*, *Berufsgruppenverzeichnisse*
- URL: `https://www.debeka.de/service/vertragsgrundlagen.html` for the Debeka documents; `https://www.cosmosdirekt.de/berufsunfaehigkeitsversicherung/` for CosmosDirekt. Not established for the other sixteen carriers
- Retrieved: **yes, in part** — Debeka *ABBV 01/2026* (PDF, 12 pp., mark *B LV 19 (01.01.2026)*) and its BU *Steuermerkblatt* *3 L/103 (01.01.2026)* under `https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/Berufsunfähigkeit/`, and CosmosDirekt *BF SBU (10.25)* (PDF, 3 pp.); all read 2026-08-30. **No** for the other sixteen carriers named here
- Content: recorded as a class so that the breadth of the German market is on the record and so that
  a later researcher has the target list. The commercially significant split inside this list is
  **channel**, not wording: the direct writers (CosmosDirekt, Hannoversche, HUK-COBURG) and the
  bank/*Öffentliche* channels (Provinzial, Sparkassen-Versicherung, R+V through the *Volksbanken*)
  sell simpler tariffs with narrower occupational coverage and fewer options, while the broker
  channel (Alte Leipziger, LV 1871, Nürnberger, Swiss Life, HDI, Volkswohl Bund, Continentale,
  Stuttgarter, die Bayerische) sells the full option set. **Nothing quantitative is cited from any
  document in this class.**

### S13 — *Produktinformationsblatt* (PIB) for a *selbständige Berufsunfähigkeitsversicherung* (document class)
- Publisher: each insurer, for each tariff. Doc type: the short pre-contractual information sheet
  required by the *VVG-Informationspflichtenverordnung* (VVG-InfoV) `[unverified]` as to the precise
  article; URL: not established
- Retrieved: **no** — a PIB is generated per quotation for a named age, occupation, term and *BU-Rente*, and no carrier publishes a specimen with figures at a public address. Its **content** is established from R12 and S6 instead
- Content: the German retail life market's standard two-page disclosure. For a BU tariff it states
  the contract type, the insured risk (naming the 50 % and six-month criteria in a sentence), the
  *BU-Rente* and its escalation, **the *Bruttobeitrag* and the *Zahlbeitrag*** with an explicit
  warning that the *Zahlbeitrag* may rise as far as the *Bruttobeitrag*, the term and *Endalter*,
  the principal exclusions, the consequences of non-disclosure, and the surrender and paid-up
  positions. **This is the single most useful public document for a modeller**, because it is the
  only one that routinely puts a *Bruttobeitrag* and a *Zahlbeitrag* on the same page for a named
  age, occupation and *BU-Rente*. None was retrieved, and that is gap 4 in the register.

### S14 — *Basisinformationsblatt* (PRIIP-KID) — and why an SBU normally does not have one
- Publisher: each insurer, where the product is in scope; URL: not established
- Retrieved: **no** — nothing to retrieve; the premise of the entry is that the document is not produced for this product, and R12 now sources the boundary
- Content: recorded as a **negative** finding of substance. PRIIPs covers *insurance-based
  investment products* — contracts offering a maturity or surrender value exposed to market
  fluctuations — so a pure biometric protection contract falls outside it. A standalone SBU is
  therefore documented by a *Produktinformationsblatt* [S13] and **not** by a
  *Basisinformationsblatt*, the opposite of the position for delib's savings products (products
  1–7), where the *Basisinformationsblatt* is the richest public document. Where BU is written as a
  rider on a savings contract, the host's *Basisinformationsblatt* covers the package and the BU
  premium sits inside its cost figures. The precise PRIIPs scope boundary is `[unverified]`; what is
  certain is that this product family does not hand the modeller the cost table the savings products
  do.

### S15 — Comparison portals, consumer press and rating agencies (document class)
- Publishers: Verivox; CHECK24; Finanztip; Stiftung Warentest / *Finanztest*; Handelsblatt;
  MORGEN & MORGEN; Franke und Bornberg; ASSEKURATA. Doc type: comparison pages, consumer guides,
  periodical product tests and ratings — **secondary throughout**; URL: not established
- Retrieved: **no** — not attempted; the class is secondary and its figures are unusable under the house rule against reproducing a recalled number
- Content: this class is where every published German BU **price point** and every published
  **wording-quality rating** lives, and it is the class this file most needed and least could reach.
  It would supply indicative *Zahlbeiträge* by age, occupation, *BU-Rente* and *Endalter* across
  carriers; the *Brutto*/*Zahlbeitrag* ratio by carrier; the number of *Berufsgruppen* per carrier;
  scoring of the *Verweisung*, *AU-Klausel* and *Nachversicherungsgarantie* wordings; and Morgen &
  Morgen's annual analysis of the **causes of BU** (section 25). Every figure in sections 25 and 26
  is of the kind this class publishes and **none of them is sourced to it** — they are recollection,
  tagged `[unverified]`, and must be re-established before use.

### S16 — Verbraucherzentrale material on the *Berufsunfähigkeitsversicherung*
- Publisher: the *Verbraucherzentralen* and the *Verbraucherzentrale Bundesverband* (vzbv). Doc
  type: consumer-advice pages and brochures — **secondary**; URL: not established
- Retrieved: **no** — not attempted; secondary, and the behavioural claims it supports are not modelled parameters
- Content: the consumer-protection view: that the statutory *Erwerbsminderungsrente* is not a
  substitute (section 24); that incomplete *Gesundheitsfragen* are the commonest reason a claim
  later fails; that a *Risikovoranfrage* should precede any application; that **the *Bruttobeitrag*
  and not the *Zahlbeitrag* is the figure a buyer should compare across carriers**; and that
  *Karenzzeiten* and a reduced *Endalter* are the two levers that cut the premium at a real cost in
  cover. Recorded because these are the behavioural facts a lapse and option-take-up assumption has
  to reflect, and because the "compare the *Bruttobeitrag*" advice is the clearest external
  statement of why the *Brutto*/*Zahlbeitrag* pair is a modelling issue and not a presentational one.

## Regulatory and actuarial references

**The blanket retrieval status these entries once carried no longer holds.** On 2026-08-30 every
statute and statutory instrument in this section that gesetze-im-internet publishes was read as its
**canonical XML** (`https://www.gesetze-im-internet.de/<slug>/xml.zip`), which carries the law's
*Stand*: VVG, VVG-InfoV, VAG, DeckRV, MindZV, AGG, SGB VI, EStG, EStDV, IfSG and VersStG. The
`__NNN.html` addresses printed below are the human-facing links and are **not** what was read —
those per-section pages answer 200 with a frameset of a few kilobytes containing no statutory text.
Each entry now carries its own `Retrieved` line; the paragraph numbering is no longer `[unverified]`
for any provision that was read, and where a reading corrected the entry the entry says so. The
non-statutory entries (R16–R23, R26, R28, R29) were not read and say why.

### R1 — VVG § 172, *Leistung des Versicherers* (the statutory definition of *Berufsunfähigkeit*)
- Publisher: Bundesministerium der Justiz / Bundesamt für Justiz, via `gesetze-im-internet.de`
- Doc type: statute — *Gesetz über den Versicherungsvertrag* (VVG) of 2008, Kapitel 5, Teil 2,
  Abschnitt 3 (*Berufsunfähigkeitsversicherung*)
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__172.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: the anchor provision of the whole product. Three limbs, recalled and `[unverified]` as to
  numbering and wording:
  1. **Abs. 1** obliges the insurer to render the agreed benefits for a *Berufsunfähigkeit* arising
     **after inception**. That temporal condition makes BU a genuine risk contract rather than a
     health indemnity, and the *vorvertragliche Anzeigepflicht* [R7] polices the boundary.
  2. **Abs. 2** defines *berufsunfähig* as a person who, as a consequence of *Krankheit*,
     *Körperverletzung* or *mehr als altersentsprechender Kräfteverfall*, is prospectively
     permanently (*voraussichtlich auf Dauer*) unable, wholly or in part, to exercise **the last
     occupation actually exercised, as it was arranged before the impairment**. Three features drive
     everything downstream: the reference occupation is the **last one actually exercised**, not any
     occupation and not the trained one; it is taken **as actually arranged**, so the concrete
     duties, hours and physical demands of this insured's own post are the measure; and the
     impairment must be **medically caused**, which excludes economic inability to work.
  3. **Abs. 3** permits the parties to **agree as a further condition** that the insured neither
     exercises nor can exercise another activity she is in a position to take up given her training
     and abilities and which corresponds to her previous *Lebensstellung*. This is the statutory
     basis of the *abstrakte Verweisung*: **permitted but not implied**, operative only if agreed,
     and almost universally no longer agreed (section 4).
- **What is *not* in § 172**: neither the **six-month** period nor the **50 %** threshold. Both are
  contractual standards carried in the AVB [S1] and are the market's concretisation of the statutory
  words *voraussichtlich auf Dauer* and *ganz oder teilweise*. The correction is made explicitly in
  section 3, because a document attributing them to the statute would mislead everything downstream.

### R2 — VVG § 173, *Anerkenntnis*
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__173.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: on a *Leistungsantrag*, the insurer must declare in *Textform*, when the claim falls due,
  whether it acknowledges its liability. The second limb restricts the **time-limited
  acknowledgement** (*befristetes Anerkenntnis*): the acknowledgement may be limited in time **only
  once** `[unverified]` as to whether the statute frames this as "only once" or as "only once and
  only with the policyholder's agreement". The economic effect is what matters and is not in doubt:
  once an *Anerkenntnis* has been given, whether limited or not, **the insurer is bound by it and
  can escape only through the *Nachprüfung* route of § 174** [R3] — the burden of proof reverses
  from the insured to the insurer. Before the 2008 VVG reform insurers used repeated time-limited
  acknowledgements to keep that burden on the insured indefinitely; § 173 exists to stop that.

### R3 — VVG § 174, *Leistungsfreiheit* (the *Nachprüfung* and its notice period)
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__174.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: where the insurer establishes that the conditions of its liability have ceased, it
  remains obliged to pay **only to the end of the third month following receipt by the policyholder
  of the notice** to that effect. The three-month run-off is the single most model-relevant number
  in the statutory frame: a recovery does not stop the annuity on the day it happens, it stops it at
  a quarter-end measured from a notice. A second limb `[unverified]` addresses the case where the
  insured's occupational position has changed since the *Anerkenntnis* — the insurer may rely on a
  new occupation actually taken up (*konkrete Verweisung*, section 4) — and imposes on the insurer
  the duty to demonstrate a **change** relative to the state of affairs on which the *Anerkenntnis*
  was based, not merely to re-decide the original claim.

### R4 — VVG § 175, *Abweichende Vereinbarungen*
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__175.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: §§ 173 and 174 are *halbzwingend* — no departure to the disadvantage of the policyholder
  is effective. This is why the *Anerkenntnis* and *Nachprüfung* mechanics are uniform across the
  market: they are not a competitive variable. Insurers may only improve on them, and some do (for
  example by binding themselves to a longer run-off, or by waiving the *Nachprüfung* after a stated
  benefit duration).

### R5 — VVG § 176, *Anzuwendende Vorschriften*
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__176.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: applies the life-assurance provisions of the VVG **mutatis mutandis** to the
  *Berufsunfähigkeitsversicherung*. The range is recalled as **§§ 150 to 170** `[unverified]`. This
  single cross-reference is what makes an SBU a life contract in everything but its trigger, and it
  is load-bearing for the model, because it carries across:
  - § 153 *Überschussbeteiligung* [R10] — hence the *Brutto* / *Zahlbeitrag* pair;
  - § 161 *Selbsttötung* [R11] — hence the three-year suicide window, which in a BU context bites on
    a self-inflicted injury producing disability;
  - § 165 *Prämienfreie Versicherung* [R8] — hence a right to a *beitragsfreie BU-Rente*;
  - § 168 *Kündigung* and § 169 *Rückkaufswert* [R9] — hence a surrender value, and hence a
    *Deckungsrückstellung* that is genuinely material for a level-premium BU contract;
  - § 169 Abs. 3's five-year spreading of acquisition costs, and the *Mindestrückkaufswert*.
  The verification task here was precise — **confirm the range of sections § 176 imports** — and it
  is **done**. Read 2026-08-30 in the canonical XML (Stand: zuletzt geändert durch Art. 12 G v.
  26.5.2026 I Nr. 156): "Die §§ 150 bis 170 sind auf die Berufsunfähigkeitsversicherung entsprechend
  anzuwenden, soweit die Besonderheiten dieser Versicherung nicht entgegenstehen." The recalled range
  is correct. Two of the five bullets need qualifying against that reservation: § 169 Abs. 1 confers
  the surrender right only where "der Eintritt der Verpflichtung des Versicherers gewiss ist", which
  a pure SBU is not, and § 161 is a **death-cover** rule whose three-year window has no application
  to a self-inflicted impairment — the market's AVB exclude deliberate self-harm outright instead,
  with no window at all. And the *Deckungsrückstellung* is **not** "genuinely material": a carrier's
  own AVB records that the premium parts available to build it are "sehr gering" against premiums
  paid and that it is always exhausted by expiry.

### R6 — VVG § 177, *Ähnliche Versicherungsverträge*
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__177.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: **read 2026-08-30 in the canonical XML, and the reading corrects this entry twice.**
  Abs. 1: "Die §§ 173 bis 176 sind auf alle Versicherungsverträge, bei denen der Versicherer für eine
  **dauerhafte** Beeinträchtigung der Arbeitsfähigkeit eine Leistung verspricht, entsprechend
  anzuwenden." So it reaches cover of a *lasting* impairment — *Grundfähigkeits-* and
  *Erwerbsunfähigkeitsversicherung* — and **not** cover of temporary *Arbeitsunfähigkeit*: an
  *AU-Klausel* benefit (section 11) does not inherit these protections through § 177, but through
  §§ 172 ff. applying directly to the BU contract it sits inside. Abs. 2 expressly **excludes**
  accident insurance and health-insurance contracts covering impaired working capacity, so it does
  not extend the frame to accident cover either. It still marks the outer boundary of the delib
  product: everything § 177 reaches is a neighbouring product, not this one.

### R7 — VVG §§ 19–22, *Vorvertragliche Anzeigepflicht* and its consequences
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__19.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: the applicant must disclose the risk circumstances known to her which the insurer has
  asked about in *Textform*. Breach gives the insurer, graded by fault: *Rücktritt* (rescission) for
  intent or gross negligence; contract amendment (retroactive imposition of the terms the insurer
  would have required) for simple negligence; *Kündigung*; and *Anfechtung* for fraudulent
  misrepresentation. The insurer's remedies lapse **five years** after conclusion — **ten years**
  where the breach was intentional or fraudulent `[unverified]` as to both figures and to whether
  the ten-year period attaches to intent or only to fraud. This is the most practically important
  legal provision in German BU after § 172 itself, because the commonest reason an otherwise valid
  BU claim fails is an *Anzeigepflichtverletzung* discovered during the *Leistungsprüfung*. The
  market's behavioural response — the anonymous *Risikovoranfrage*, made through a broker so that a
  decline is never recorded against the applicant in the industry's *Hinweis- und
  Informationssystem* (HIS) — is a direct consequence and is described in section 17.

### R8 — VVG § 165, *Prämienfreie Versicherung* (applied via § 176)
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: the policyholder may at any time require the contract to be converted to a paid-up
  contract; the insurer computes a reduced sum insured on recognised actuarial principles, with the
  costs of the conversion deductible. For BU the reduced benefit is a **beitragsfreie BU-Rente**,
  and it is small: a BU contract's *Deckungsrückstellung* is a fraction of the present value of the
  remaining risk, so the paid-up *BU-Rente* is a small fraction of the original. § 165 also carries
  the rule that the paid-up benefit must reach a stated minimum or the contract is instead treated
  as terminated with payment of the *Rückkaufswert* `[unverified]`.

### R9 — VVG § 169, *Rückkaufswert* (applied via § 176)
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: on termination by notice the insurer must pay the surrender value, computed as the
  *Deckungsrückstellung* calculated on recognised actuarial principles; **acquisition and
  distribution costs must be spread over at least the first five years** for the purpose of the
  *Mindestrückkaufswert*; a *Stornoabzug* is permissible only if agreed, appropriate and
  **quantified in the contract** `[unverified]` as to the exact conditions. Applied to BU through
  § 176 [R5]. The practical consequence is a genuine one and is easy to get wrong: a level-premium
  SBU to age 67 **does** build a substantial reserve, because the *Invalidisierungswahrscheinlichkeit*
  rises far more steeply with age than mortality does, so the level premium heavily overcharges in
  the early years. The surrender value is nevertheless modest relative to premiums paid, because
  the reserve is a risk reserve and not a savings account, and because *Zillmerung* [R13] absorbs the
  early years of it.

### R10 — VVG § 153, *Überschussbeteiligung* (applied via § 176)
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: the policyholder is entitled to a share of the *Überschuss* and of the
  *Bewertungsreserven* unless participation is expressly excluded; the allocation must follow a
  *verursachungsorientiertes Verfahren* (a method oriented to the origin of the surplus). For BU the
  surplus is overwhelmingly **risk surplus** (actual *Invalidisierungen* below the first-order
  assumption) and **expense surplus**, with an interest component that is small because the reserve
  is small relative to the premium. § 153 is the legal reason a German BU tariff is quoted as a pair
  of numbers (section 18): the *Bruttobeitrag* is the price on first-order bases, and the
  *Zahlbeitrag* is what is actually charged after the anticipated surplus is credited in advance by
  *Beitragsverrechnung*.

### R11 — VVG § 161, *Selbsttötung* (applied via § 176)
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*. The `__NNN.html` address above is a frameset shell and carries no statutory text
- Content: in a life contract the insurer is free of liability where the insured takes her own life
  within **three years** of conclusion `[unverified]`, unless the act was committed in a state of
  pathological mental disturbance excluding free determination of will; in that case the
  *Rückkaufswert* is paid. Applied to BU via § 176, the analogue is an **intentionally self-inflicted
  impairment**: the AVB exclude BU caused by the insured's deliberate act, and the three-year window
  applies to the attempted-suicide case. `[unverified]` whether the market's AVB run the three-year
  window or exclude deliberate self-harm without a time limit; both forms are recalled.

### R12 — VVG-Informationspflichtenverordnung (VVG-InfoV)
- Publisher: Bundesministerium der Justiz
- Doc type: statutory instrument prescribing pre-contractual information duties, including the
  *Produktinformationsblatt*
- URL: `https://www.gesetze-im-internet.de/vvg-infov/` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vvg-infov/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 13 G v. 26.5.2026 I Nr. 156*. § 2 read in full
- Content: prescribes what must be given to the applicant before conclusion and mandates the
  *Produktinformationsblatt* [S13] for life and BU contracts, in a prescribed order and at a
  prescribed brevity. For a savings contract it also mandates the disclosure of *Effektivkosten*
  (reduction in yield); **for a pure risk contract there is no yield to reduce**, so a BU
  *Produktinformationsblatt* discloses costs only through the *Brutto* / *Zahlbeitrag* pair and not
  as a percentage figure. That absence is why the delib BU charge assumptions are entirely `[std]`
  (section 19) while the delib endowment's are not.

### R13 — Deckungsrückstellungsverordnung (DeckRV) — *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher: Bundesministerium der Finanzen
- Doc type: statutory instrument
- URL: `https://www.gesetze-im-internet.de/deckrv/` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/deckrv_2016/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250*. §§ 2, 4, 5a and 6 read; the consolidated HTML at `https://www.gesetze-im-internet.de/deckrv_2016/BJNR076700016.html` was also retrieved
- Content: sets the maximum technical interest rate for the *Deckungsrückstellung* of new German life
  business — and, in practice, for pricing — and caps the acquisition costs that may be zillmered
  into the reserve at **25 ‰ (2,5 %) of the *Beitragssumme*** `[unverified]`. The
  *Höchstrechnungszins* was **0,25 %** for contracts written from 2022 to 2024 and was raised to
  **1,00 %** with effect from 1 January 2025 `[unverified] on both the figures and the date`. Both
  numbers matter here: the *Rechnungszins* discounts a BU liability whose duration is long (a claim
  incepting at 45 on a contract to 67 runs 22 years), and the *Höchstzillmersatz* applied to the
  *Beitragssumme* of a 37-year BU contract produces an acquisition-cost allowance that is large in
  absolute terms even though the annual premium is small. delib's cross-product reference library
  carries the DeckRV in full; this entry exists so that the BU product's own `sources.md` can point
  at it locally.

### R14 — Mindestzuführungsverordnung (MindZV)
- Publisher: Bundesministerium der Finanzen
- Doc type: statutory instrument on the minimum allocation of surplus to policyholders
- URL: `https://www.gesetze-im-internet.de/mindzv/` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/mindzv_2016/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688*. §§ 4, 6, 7 and 8 read
- Content: prescribes the minimum share of *Rohüberschuss* that must be allocated to the
  *Rückstellung für Beitragsrückerstattung*, separately by source — interest, risk and expense. The
  **risk-result minimum allocation** is the one that governs BU, and it is recalled as **90 % of the
  risk result** `[unverified]`. This is the quantitative link between a BU book's claims experience
  and the *Zahlbeitrag* the market charges: an insurer whose *Invalidisierungen* run well below the
  first-order table must pass most of that back, and the *Beitragsverrechnung* is how it does so
  (section 18).

### R15 — VAG §§ 138, 139, 141 — *Gleichbehandlung*, *Überschussbeteiligung*, *Verantwortlicher Aktuar*
- Publisher: Bundesministerium der Justiz
- Doc type: statute — *Versicherungsaufsichtsgesetz*
- URL: `https://www.gesetze-im-internet.de/vag_2016/` as to the section numbers — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/vag_2016/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81*. §§ 138, 139 and 141 read; all three section numbers are correct. **Unisex is not in the VAG** — AGG § 33 Abs. 5 was read for it and confirms the 21 December 2012 date
- Content: § 138 requires premiums to be calculated on actuarial principles sufficient to meet the
  obligations permanently and requires **equal treatment of equal risks**; § 139 governs the
  *Überschussbeteiligung* on the supervisory side and is the counterpart of § 153 VVG; § 141 places
  the pricing and reserving bases in the hands of the *Verantwortlicher Aktuar*, who must confirm
  that the *Deckungsrückstellung* is properly calculated and that the premiums are sufficient. For
  BU the *Gleichbehandlungsgrundsatz* is what legitimises *Berufsgruppen*: differentiating price by
  occupation is not discrimination but the recognition that the risks are not equal. The same
  principle **forbids** differentiating by sex — see the unisex rule below.
- **Unisex.** Since 21 December 2012 German insurers may not differentiate premiums or benefits by
  sex, following the CJEU's *Test-Achats* judgment `[unverified]` as to the case reference and the
  transposing instrument. This bites unusually hard in BU, because the underlying
  *Invalidisierungswahrscheinlichkeiten* differ materially by sex — female incidence is higher at
  most ages `[unverified]` — so a unisex BU tariff embeds a mix assumption that the insurer bears
  the risk of. Any delib BU decrement table must be a **unisex** table for pricing, whatever the
  underlying research bases are.

### R16 — DAV 1997 I, DAV 1997 RI and DAV 1997 TI — the *Rechnungsgrundlagen* for BU
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV), Köln. Doc type: actuarial tables and the
  accompanying *Herleitung* report of the DAV working party on BU bases; URL: not established
- Retrieved: **no** — DAV property, not published at a public address. This is the one entry here whose status cannot change however good the network is
- Content: the German BU pricing and reserving standard, and — critically — **not public**. The
  package as recalled comprises three tables, `[unverified]` on the names:
  - **DAV 1997 I** — *Invalidisierungswahrscheinlichkeiten*: probability that an active life aged x
    becomes *berufsunfähig* within a year, by age and sex, before occupational loading.
  - **DAV 1997 RI** — *Reaktivierungswahrscheinlichkeiten*: probability that a disabled life
    recovers, **by age at disablement and by duration since disablement**. The duration dimension is
    essential: reactivation is concentrated in the first one to two years of a claim and falls close
    to zero thereafter.
  - **DAV 1997 TI** — *Sterbewahrscheinlichkeiten der Invaliden*: disabled-lives mortality,
    materially heavier than active mortality and itself select on duration.
  The bases are *erster Ordnung*, i.e. deliberately prudent, and are used with insurer-specific
  **occupational loading factors** and safety margins; second-order versions are derived by each
  insurer from its own experience.
- **Correction to the commissioning brief.** It attributed both entry and reactivation probabilities
  to "DAV 1997 I and DAV 1997 TI". DAV 1997 TI is the **disabled-lives mortality** table and the
  reactivation probabilities sit in a third table, recalled as DAV 1997 RI. That correction is itself
  `[unverified]` and is gap 8 in the register.
- **Is there a newer table?** No successor in general market use could be established. DAV working
  parties have published *Ergebnisberichte* on the adequacy of the 1997 bases and on drift in BU
  experience — notably the rise in psychiatric causes (section 25) — but this file cannot confirm
  that a "DAV 20xx I" exists, is homologated, or is used (gap 9).
- **Redistribution.** The tables are DAV property, are not published, and **are not redistributed by
  delib**. The model ships `[std]` proxies and states, in its `Data` docstring and in `model.md`,
  what a replacement built from the real tables must preserve: the age shape of the inception rate,
  the duration shape of reactivation, and the excess of disabled over active mortality.

### R17 — DAV 2008 T — active-lives mortality
- Publisher: Deutsche Aktuarvereinigung e. V.
- Doc type: mortality table for contracts with death-benefit character, with its *Herleitung* report
- URL: not established
- Retrieved: **no** — DAV property, not published at a public address
- Content: the first-order mortality table for German risk business. Relevant to BU as the **active
  state's** mortality decrement: an active life leaves the model by becoming BU, by lapsing, or by
  dying, and the last of these uses a *Todesfall*-character table. Not public; delib ships a `[std]`
  proxy. Also carried in the delib cross-product reference library for the
  `risikolebensversicherung` product, whose research file is the primary place it is described.

### R18 — DAV *Ergebnisberichte* and *Fachgrundsätze* on biometric bases and BU
- Publisher: Deutsche Aktuarvereinigung e. V., *Ausschuss Lebensversicherung* / working parties on
  biometric bases (*AG Biometrische Rechnungsgrundlagen*) and on *Berufsunfähigkeit*
- Doc type: *Ergebnisberichte* (results reports) and *Fachgrundsätze* (professional standards)
- URL: not established
- Retrieved: **no** — no BU-specific *Ergebnisbericht* was located on the association's site on 2026-08-30
- Content: the DAV publishes results reports on the derivation and periodic review of biometric
  bases, on the treatment of *Reaktivierung*, on *Storno* in biometric products, and on the
  best-estimate assumptions used for Solvency II technical provisions. These are the documents that
  would supply the shape of the German BU inception curve, its trend over time and the second-order
  reactivation pattern — the three things this file most lacks quantitatively. They are freely
  downloadable in normal conditions and were unreachable here.

### R19 — BaFin material on the *Berufsunfähigkeitsversicherung*
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht
- Doc type: *Merkblätter*, *Rundschreiben*, *BaFinJournal* articles, *Risiken im Fokus*
- URL: not established (`bafin.de` refused)
- Retrieved: **no** — not attempted; nothing quantitative is cited from BaFin anywhere in this product
- Content: BaFin supervises the *Leistungsprüfung* practice of German BU insurers as a conduct
  matter (*Wohlverhaltensaufsicht*) and has published on the duration of claims decisions, on the
  quality of *Nachprüfung* notices, and on the *Brutto*/*Zahlbeitrag* disclosure. It also collects
  and publishes the industry's *Beschwerdestatistik*, in which BU is persistently over-represented
  relative to its premium share `[unverified]`. Nothing specific is cited from BaFin in this file.

### R20 — GDV statistics on the *Berufsunfähigkeitsversicherung*
- Publisher: GDV
- Doc type: *Statistisches Taschenbuch der Versicherungswirtschaft*, *Die deutsche
  Lebensversicherung in Zahlen*, and GDV press material on BU
- URL: not established
- Retrieved: **no** — the general *Die deutsche Lebensversicherung in Zahlen* series is reachable on `gdv.de`; no BU-specific series was located or read, and no figure is taken from it
- Content: the source that would give the **size of the German BU market** — number of in-force
  contracts, new business, premium income, and the industry-wide *Anerkennungsquote*, which the GDV
  began publishing in recent years `[unverified]` as to the year and the figure. An order of
  magnitude often quoted is that roughly **17 million** BU contracts are in force in Germany
  `[unverified]`, counting standalone and rider forms together, against a working population of
  about 45 million — i.e. cover is far from universal, which is the market's own framing of the
  product. **None of these figures is sourced here.**

### R21 — Franke und Bornberg, *BU-Leistungspraxis* and the *BU-Rating*
- Publisher: Franke und Bornberg GmbH, Hannover
- Doc type: recurring market study of BU claims practice, based on data supplied and audited at
  participating insurers, plus the firm's ratings of BU *Bedingungen*
- URL: not established
- Retrieved: **no** — the publisher's blog is reachable, the *BU-Leistungspraxis* study itself was not located at a public address on 2026-08-30
- Content: **the usual publisher of the German *Anerkennungsquote***, and the reference this file's
  section 25 points at. The study reports, per participating insurer and in aggregate: the
  proportion of decided BU claims accepted; the breakdown of declines by reason (BU degree not
  reached, *Anzeigepflichtverletzung*, *Anfechtung*, failure to co-operate, claim withdrawn); the
  average duration of a claims decision; the proportion of decisions reached without a medical
  examination; and the proportion of disputes. It also rates BU wordings clause by clause, which is
  where the market's ranking of *Verweisung*, *AU-Klausel* and *Nachversicherungsgarantie* terms
  comes from. Every figure in section 25 attributed to an *Anerkennungsquote* should be checked
  against this study.

### R22 — Morgen & Morgen, *M&M Rating Berufsunfähigkeit* and the annual causes analysis
- Publisher: MORGEN & MORGEN GmbH, Hofheim am Taunus
- Doc type: annual rating of BU tariffs and an accompanying analysis of the **causes of BU**
- URL: not established
- Retrieved: **no** — not attempted
- Content: **the usual publisher of the German causes-of-BU distribution** — the percentages in
  section 25. The analysis groups causes into roughly six classes (*Nervenkrankheiten* including
  psychiatric conditions; *Erkrankungen des Skelett- und Bewegungsapparates*; *Krebs und andere
  bösartige Geschwülste*; *Unfälle*; *Erkrankungen des Herzens und des Gefäßsystems*; *sonstige
  Erkrankungen*) and publishes the split annually, so the series shows the long rise of the
  psychiatric share. The rating side scores tariffs on wording, on the insurer's financial strength
  and on the stability of its *Zahlbeitrag* relative to its *Bruttobeitrag* — the last of these
  being the market's own recognition that the *Brutto*/*Zahlbeitrag* gap is a risk to the buyer.

### R23 — ASSEKURATA, market studies on *Überschussbeteiligung* and on biometric products
- Publisher: ASSEKURATA Assekuranz Rating-Agentur GmbH, Köln
- Doc type: annual market studies and insurer ratings
- URL: not established
- Retrieved: **no** — not attempted
- Content: ASSEKURATA's annual study of declared *Überschussbeteiligung* is the standard reference
  for German surplus declarations. For BU the relevant content is the **stability of the
  *Beitragsverrechnung***: which insurers have had to raise the *Zahlbeitrag* toward the
  *Bruttobeitrag*, and by how much. That history is the empirical content of the risk the
  *Bruttobeitrag* represents, and it is not established in this file (gap 6).

### R24 — SGB VI § 43, *Rente wegen Erwerbsminderung*
- Publisher: Bundesministerium der Justiz
- Doc type: statute — *Sozialgesetzbuch, Sechstes Buch*
- URL: `https://www.gesetze-im-internet.de/sgb_6/__43.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/sgb_6/xml.zip`, read 2026-08-30; *Stand: zuletzt geändert durch Art. 2a G v. 24.7.2026 I Nr. 228*
- Content: the statutory disability pension the private BU contract sits on top of. Two tiers, both
  measured against the **general labour market** (*allgemeiner Arbeitsmarkt*) rather than the
  insured's own occupation:
  - **Rente wegen teilweiser Erwerbsminderung** — the insured can work at least **three but less
    than six hours** a day under normal labour-market conditions `[unverified]`.
  - **Rente wegen voller Erwerbsminderung** — the insured can work **less than three hours** a day
    `[unverified]`.
  Both require the general *Wartezeit* of **five years** of contributions and, in addition, **three
  years of compulsory contributions in the last five years** before the onset `[unverified]`.
  Pensions are normally granted for a limited period (*Zeitrente*), typically three years, renewable,
  and become permanent only in defined circumstances `[unverified]`.

### R25 — SGB VI § 240 — the abolished statutory *Berufsunfähigkeitsrente*
- Publisher: as R24
- URL: `https://www.gesetze-im-internet.de/sgb_6/__240.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML, same source and *Stand* as R24. Abs. 1 Nr. 1 reads "vor dem 2. Januar 1961 geboren", confirming the cohort date
- Content: the transitional provision preserving a *Rente wegen teilweiser Erwerbsminderung bei
  Berufsunfähigkeit* for insured persons **born before 2 January 1961** `[unverified]`. For everyone
  born on or after that date the statutory scheme contains **no occupational-disability pension at
  all** — only the general-labour-market *Erwerbsminderungsrente* of § 43. This is the historical
  fact that created the modern German private BU market: the 2001 reform removed occupational
  protection from the statutory scheme for the whole post-1960 cohort, and the private SBU is its
  replacement. Any delib document explaining why this product exists should cite this provision.

### R26 — Deutsche Rentenversicherung statistics on *Erwerbsminderungsrenten*
- Publisher: Deutsche Rentenversicherung Bund
- Doc type: *Rentenversicherung in Zahlen*, *Rentenzugangsstatistik*, and the annual press material
  on new *Erwerbsminderungsrenten*
- URL: not established (`deutsche-rentenversicherung.de` refused)
- Retrieved: **no** — not attempted; no DRV statistic is printed anywhere in this product
- Content: the source for the **average level** of the statutory disability pension — the figure
  that quantifies the *Versorgungslücke* the private product fills — and for the number of new
  awards per year, the average age at award, and the distribution of awards by diagnosis. The DRV's
  diagnosis distribution is an independent check on the insurers' causes-of-BU distribution [R22]
  and is known to show an even higher psychiatric share, because the statutory test is harder to
  meet for musculoskeletal conditions `[unverified]`. Figures quoted in section 25 are recalled and
  tagged, not sourced.

### R27 — EStG § 10 and § 22 — deductibility of the premium and taxation of the *BU-Rente*
- Publisher: Bundesministerium der Justiz
- Doc type: statute — *Einkommensteuergesetz*
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` and `.../__22.html` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — EStG canonical XML at `https://www.gesetze-im-internet.de/estg/xml.zip` and EStDV at `https://www.gesetze-im-internet.de/estdv_1955/xml.zip` (*Stand: zuletzt geändert durch Art. 2 V v. 19.12.2025 I Nr. 372*), read 2026-08-30. § 10 Abs. 1 Nr. 3a, § 10 Abs. 4, § 22 Nr. 1 Satz 3 Buchst. a and EStDV § 55 Abs. 2 read; corroborated by a carrier's own tax leaflet (S12)
- Content: two distinct regimes, and the difference between them is the main reason to write BU as a
  *Basisrente* rider rather than standalone:
  - **Standalone SBU (Schicht 3).** The premium is a *sonstige Vorsorgeaufwendung* under
    § 10 Abs. 1 Nr. 3a EStG, deductible only inside an annual ceiling — recalled as **1 900 €** for
    employees and civil servants and **2 800 €** for the self-employed `[unverified]` — which is in
    practice already exhausted by statutory health and long-term-care contributions, so the
    effective deduction is **nil** for most buyers. The *BU-Rente* is then taxed under
    § 22 Nr. 1 EStG as an *abgekürzte Leibrente* on its **Ertragsanteil**, determined by the
    annuity's **remaining term** at the time it starts rather than by the recipient's age.
  - **BU inside a *Basisrente* (Schicht 1).** The premium is an *Altersvorsorgeaufwendung* under
    § 10 Abs. 1 Nr. 2 EStG, deductible in full within the much larger *Basisrente* ceiling, provided
    the BU component satisfies the conditions of R28. The *BU-Rente* is then fully taxable as
    *sonstige Einkünfte* at the cohort *Besteuerungsanteil* — a far heavier taxation of the benefit
    in exchange for a far larger deduction of the premium.
  All specific figures here are `[unverified]`, and the *Ertragsanteil* table is reproduced in
  section 23 with the same tag.

### R28 — BMF-Schreiben on the *Basisrente* and the conditions for a BU component
- Publisher: Bundesministerium der Finanzen
- Doc type: administrative circular (*BMF-Schreiben*) on the tax treatment of *Altersvorsorge* and
  *Basisrenten* contracts
- URL: not established (`bundesfinanzministerium.de` refused)
- Retrieved: **no** — the circular itself was not sought on `bundesfinanzministerium.de` in this pass. The **statutory** side was read: EStG § 10 Abs. 1 Nr. 2 Buchst. b admits both a BU rider inside a *Basisrente* (Doppelbuchst. aa) and a standalone first-layer BU annuity for an event occurring up to age 67 (Doppelbuchst. bb). The 49 % premium-share cap is administrative and is **not** in that text
- Content: the instrument that sets the conditions a BU rider must satisfy for the whole premium to
  qualify as an *Altersvorsorgeaufwendung*. The recalled conditions are: the BU benefit must be paid
  **as an annuity**, not a lump sum; it must run at most to the end of the host contract's deferment;
  and **more than 50 % of the total premium must be attributable to the old-age provision**, i.e.
  the BU rider premium may not exceed **49 %** of the total `[unverified] on the percentage`. That
  threshold is the reason a *Basisrente* with a large BU rider must carry a correspondingly large
  savings premium, and it is a genuine product-design constraint that delib's `basisrente` product
  must respect if it ever carries this rider.

### R29 — BGH case law on *Verweisung*, *Anerkenntnis* and *Nachprüfung*
- Publisher: Bundesgerichtshof, IV. Zivilsenat (the insurance senate). Doc type: judgments.
  URL: not established; **no docket number is given anywhere in this file**, because none could be
  confirmed and inventing one is barred
- Retrieved: **no** — no judgment text was read and none is cited by number. Two of the four lines are recited in retrieved conditions: the *Lebensstellung* limit with a 20 % pay-reduction tolerance, and the self-employed insured's *Umorganisationspflicht* (S1, S12)
- Content: four settled lines, each recalled in substance and `[unverified]` in every detail:
  1. **Binding effect of the *Anerkenntnis*.** It binds the insurer, which may free itself only by
     the *Nachprüfung* route and only prospectively; it cannot re-decide the original claim.
  2. **The *Nachprüfung* requires a demonstrated change.** The insurer must compare the insured's
     state now with the state on which the *Anerkenntnis* rested and show a material improvement; a
     re-assessment of the same facts, or correction of its own earlier error, does not suffice. The
     *Einstellungsmitteilung* must set out that comparison intelligibly, and one that does not is
     ineffective — so the three-month period of § 174 never starts to run.
  3. ***Lebensstellung*.** A *Verweisungsberuf* must correspond in **income and social standing**. A
     noticeable income drop breaks the correspondence; the market's working threshold of about
     **20 %** `[unverified]` is a rule of thumb from lower-court practice, not a BGH figure.
  4. ***Umorganisation* for the self-employed.** Before being treated as *berufsunfähig* a
     self-employed insured must consider whether the business can be reorganised so she can continue
     to run it within her remaining capacity — but only where that is economically sensible and does
     not cost her a substantial part of her income or her leading position.

### R30 — Infektionsschutzgesetz (IfSG) — the basis of the *Infektionsklausel*
- Publisher: Bundesministerium der Justiz
- Doc type: statute
- URL: `https://www.gesetze-im-internet.de/ifsg/` — the human-facing link; the text was read as canonical XML (see `Retrieved`)
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/ifsg/xml.zip`, read 2026-08-30; *Stand: Zuletzt geändert durch Art. 3 Abs. 1 G v. 4.3.2026 I Nr. 60*. The provision is **§ 31, *Berufliches Tätigkeitsverbot***
- Content: empowers the competent authority to impose a *Tätigkeitsverbot* — a prohibition on
  practising — on a person who is infected, is suspected of being infected or is a carrier, where
  practising would risk transmission. For medical, dental, nursing and laboratory occupations such a
  ban ends the ability to earn without the person being ill in the sense of § 172 VVG. The
  *Infektionsklausel* (section 14) is the market's contractual answer: it deems the ban to be BU.
  The clause is essentially standard for doctors and dentists and common for nursing and medical
  assistants.

### R31 — Versicherungsteuergesetz (VersStG) § 4 — exemption of life and BU premiums
- Publisher: Bundesministerium der Justiz
- Doc type: statute
- URL: `https://www.gesetze-im-internet.de/versstg/` `[unverified]`
- Retrieved: **yes** — canonical XML at `https://www.gesetze-im-internet.de/versstg/xml.zip`, read 2026-08-30; *VersStG 2021, Neugefasst durch Bek. v. 27.4.2021 I 874*. The slug `versstg` is confirmed by retrieval, and the paragraph is **§ 4 Abs. 1 Nr. 5 Buchst. b**
- Content: German insurance premium tax exempts life-assurance premiums, and the exemption extends
  to *Berufsunfähigkeitsversicherung* written by a life insurer `[unverified]` as to the paragraph
  and the precise scope. The practical consequence for the model is simply that **the BU premium
  carries no premium tax**, unlike a German non-life premium at 19 %. This should be confirmed
  before any delib document states it as a fact; it is recorded here because a modeller coming from
  a non-life background will otherwise wonder where the tax line is.

---

## Extracted facts, organised by mechanic

This is the section `product-spec.md` and `technical-notes.md` are written from, and it carries the
file's weight: the **mechanics** are well established and set out in full, the `[S#]` / `[R#]` tags
name the document each statement must be checked against — and, since the re-verification of
2026-08-30, name a document that was actually opened wherever the entry says `Retrieved: yes` — and
every **level** is either `[std]` with a rationale or `[unverified]` with a warning. The levels are
where the pass reached least, so this section is still read against the gaps register.

### 1. Product structure and legal form

- An SBU is a **life-assurance contract** written by a *Lebensversicherungsunternehmen*, governed by
  §§ 172–177 VVG for its own mechanics and, through § 176, by the general life provisions §§ 150–170
  VVG for everything else [R1] [R5]. It is not health business and not accident business, even though
  its trigger is a health event.
- The contract is a **pure risk contract with a reserve**: it pays only on the insured event and
  returns nothing if the insured stays healthy, yet it carries a material *Deckungsrückstellung*
  because the premium is level and the risk rises steeply with age [R9]. That combination — no
  savings intent, substantial reserve — is the structural fact distinguishing BU from every other
  product in delib.
- Two commercial forms, one liability. ***Selbständige BU (SBU)*** — standalone; delib product 9 and
  the subject of this file. ***BU-Zusatzversicherung (BUZ)*** — a rider on a *Renten-*,
  *Kapitallebens-* or *Basisrentenversicherung* [S2]; the BU risk, definition, claim procedure and
  *Nachprüfung* are identical, but the *Beitragsbefreiung* waives the **whole** premium of the host
  contract and the tax treatment follows the host (section 23). A third form, the BU-Rente inside an
  occupational pension (*bAV-BU*), is out of delib's scope entirely.
- The German market's own hierarchy of biometric income protection, broadest trigger first, bounds
  the product: *Berufsunfähigkeit* (last occupation, 50 %) → *Grundfähigkeitsversicherung* (loss of
  defined basic abilities) → *Erwerbsunfähigkeit* (any occupation) → statutory
  *Erwerbsminderungsrente* (general labour market, hours-based) [R24]. BU is the **broadest and most
  expensive** of the four and is the one the market sells first.

### 2. The statutory definition — § 172 VVG

- A person is *berufsunfähig* who, **as a consequence of illness, bodily injury or more than
  age-appropriate decline in strength**, is **prospectively permanently** unable, wholly or in part,
  to exercise **the occupation last actually exercised, as it was arranged before the impairment**
  [R1].
- Four things follow, and all four are model-relevant:
  1. **The reference occupation is the last one actually exercised.** Not the trained occupation,
     not an average occupation, not "any occupation". A trained lawyer working as a warehouse
     supervisor is tested against warehouse supervision. This is why the German BU trigger is so
     much more generous than an "any occupation" disability definition, and why the price is so much
     more sensitive to the insured's actual job.
  2. **It is taken as actually arranged** (*so wie er ohne gesundheitliche Beeinträchtigung
     ausgestaltet war*). The concrete duties, working hours and physical demands of this insured's
     own post are the yardstick. Two people with the same job title can have different tests.
  3. **The cause must be medical.** Illness, bodily injury, or a decline in strength beyond what the
     age would explain. Loss of the job, loss of a licence for non-medical reasons, or an economic
     inability to find work is not BU — with the single contractual exception of the
     *Infektionsklausel* (section 14).
  4. **Prospectively permanent** — *voraussichtlich auf Dauer*. The statute does not put a number on
     it; the market does (section 3).
- **§ 172 Abs. 3 permits, but does not imply, the *abstrakte Verweisung*** [R1]. Absent an express
  agreement, the insurer may **not** refer the insured to an occupation she does not actually
  exercise. Section 4 records what the market does with that permission.

### 3. The contractual definition — six months, 50 per cent, and the two routes to a claim

**This section corrects the brief that commissioned the file.** The six-month period and the 50 %
threshold are **not** in § 172 VVG. They are contractual standards, carried in the AVB [S1] [S3]–[S12]
and near-uniform across the market, which concretise the statutory words *voraussichtlich auf Dauer*
and *ganz oder teilweise*. A downstream document that attributes them to the statute is wrong.

- **The market-standard AVB definition** (substance, not wording, `[unverified]` in every detail):
  the insured is *vollständig berufsunfähig* if, as a consequence of illness, bodily injury or more
  than age-appropriate decline in strength — **each to be demonstrated medically** — she is
  **prospectively for at least six months continuously** unable to exercise her last occupation, as
  it was arranged before the impairment, **to at least 50 %** [S1].
- **The 50 % threshold is all-or-nothing.** At 50 % or more, the **full** *BU-Rente* is payable; at
  49 %, nothing. There is no proportional benefit in the market standard. Some tariffs historically
  offered a *Staffelregelung* paying a partial *BU-Rente* between 25 % and 50 % `[unverified]`, and
  a few modern tariffs offer a "Teil-BU"; both are minority designs and delib models the
  all-or-nothing form.
- **Measuring the 50 %** is done on **working time**, on the share of the occupation's essential
  tasks the insured can still perform, or on both, depending on the AVB — in practice a medical
  report plus a detailed description of the actual job. **The burden of proof on the initial claim
  is on the insured** [R21].
- **Two routes to a claim, and both matter to the model.**
  - **The prognosis route.** A doctor certifies that the 50 % inability is expected to last at least
    six months from now. Benefit is due from the onset of BU (subject to any *Karenzzeit*), without
    waiting for the six months to elapse.
  - **The six-month fiction route.** Where the insured **has actually been** unable, continuously,
    for six months, the **continuation of that state counts as BU** without any further prognosis.
    The German market calls this the *Sechs-Monats-Regelung* or *BU-Fiktion*; it exists because a
    forward-looking prognosis is hard to obtain and easy to contest.
  - **Retroactivity separates good wordings from bad.** The modern standard pays **retroactively
    from the beginning of the six-month period**. Older and weaker wordings paid only **from the
    end**, costing the insured half a year of benefit `[unverified]` as to how much of the current
    market still does this. delib models retroactive payment from onset and records the alternative
    as a switch (section 7).
- **Prognosezeitraum variants.** Six months is standard; some tariffs shorten it to **three months**
  as a competitive feature `[unverified]`. A shorter prognosis makes a claim easier to establish and
  so raises the effective inception rate without changing the definition.

### 4. Abstrakte and konkrete Verweisung

The two *Verweisung* clauses are the most distinctive feature of German BU and the ones a
non-German modeller most often gets wrong.

- ***Abstrakte Verweisung*** — the insurer refers the insured to an occupation she **could** take up,
  given her training and abilities and corresponding to her previous *Lebensstellung*, **whether or
  not she actually does so** [R1 Abs. 3]. If agreed and applicable, no benefit is payable at all,
  however unable she is to do her own job. It is the clause that made German BU cover much less
  valuable than it looked, because almost any insured can be pointed at *some* theoretically
  available occupation.
  - **The market standard is now to waive it.** Essentially every quality tariff sold today contains
    a *Verzicht auf die abstrakte Verweisung* [S1] [S3]–[S12]. The waiver is not a legal requirement
    — § 172 Abs. 3 still permits the clause — it is a competitive standard, and a tariff retaining
    the *abstrakte Verweisung* is not sold in the broker channel. `[unverified]` as to when the
    waiver became universal; the shift is recalled as having run through the late 1990s and 2000s.
  - **Legacy books still carry it**, which is why the *Verweisung* still generates litigation. delib
    models the modern waived form and notes the legacy form as a variant.
- ***Konkrete Verweisung*** — the insurer refers the insured to another occupation she **actually
  exercises**. This is **retained** by the market, on both sides of the claim: at the initial claim,
  if she has already taken up such an occupation she is not *berufsunfähig*; and in the
  *Nachprüfung*, if she takes one up after benefit has started, the insurer may end the benefit —
  subject to the three-month run-off of § 174 [R3].
  - **The limit is *Lebensstellung***: the new occupation must correspond in **income** and in
    **social standing**. The working market threshold is that an income drop of more than about
    **20 %** breaks the correspondence `[unverified]`; that figure comes from lower-court practice
    and market wordings rather than from a fixed statutory or BGH rule [R29].
  - Some tariffs **waive the konkrete Verweisung as well**, or waive it where the new occupation
    pays materially less — a genuine competitive variable and one the *Bedingungsratings* score
    [R21] [R22].
- **Model consequence.** *Konkrete Verweisung* is not a separate decrement. In a cash-flow model it
  is **indistinguishable from recovery**: both end the benefit, both operate through the
  *Nachprüfung*, and both carry the same three-month run-off. delib therefore folds recovery and
  *konkrete Verweisung* into a single duration-dependent **claim-termination-other-than-death**
  rate, and says so rather than pretending to separate two things no public data separates.

### 5. The claim procedure — *Leistungsantrag*, *Leistungsprüfung* and *Anerkenntnis* (§ 173 VVG)

- The insured files a *Leistungsantrag* with a detailed description of the occupation as actually
  exercised, medical reports, and releases allowing the insurer to obtain records. The insurer runs
  a *Leistungsprüfung*, which routinely involves its own medical assessment and, for the
  self-employed, an analysis of the business [R21].
- **The insurer must declare in *Textform* whether it acknowledges liability** [R2]. The declaration
  is an *Anerkenntnis*.
- **The *Anerkenntnis* binds.** Once given, the insurer cannot revisit the same facts; it can only
  stop paying prospectively through a *Nachprüfung* in which the **burden of proof is on the
  insurer** [R3] [R29]. This reversal of the burden is the most valuable thing an insured obtains
  from a BU claim, and it is why § 173's restriction on the *befristetes Anerkenntnis* matters.
- ***Befristetes Anerkenntnis*.** A time-limited acknowledgement may be given **only once** [R2].
  Within the period it binds absolutely. Market practice limits it to a stated maximum, recalled as
  **6 or 12 months** `[unverified]`; a few tariffs waive the *befristetes Anerkenntnis* entirely as a
  selling point. When the period ends, the insurer must either continue paying or run a proper
  *Nachprüfung* — it cannot simply stop.
- **Time to decision.** The German market's own claims studies report an average decision time
  measured in months, with a figure of the order of **five to six months** recalled `[unverified]`,
  and a meaningful tail of much longer cases. **Model consequence**: the benefit is paid
  retroactively to onset, so a decision delay produces a **lump catch-up payment**, not a lost
  payment. A monthly cash-flow model that pays from onset and ignores the decision delay is
  understating the timing but not the amount; delib takes that simplification and records it as a
  pitfall.
- **Not every incepted BU becomes a paid claim.** The proportion accepted is the *Anerkennungsquote*
  (section 25). For a projection model this is an **acceptance factor** applied to the inception
  rate, not a separate state.

### 6. Nachprüfung, Leistungsfreiheit and Reaktivierung (§ 174 VVG)

- Once benefit is in payment the insurer may **periodically re-examine** whether its conditions still
  hold — annually or biennially in market practice, with the AVB imposing *Mitwirkungspflichten* on
  the insured to supply medical evidence, notify changes in health or occupation, and submit to
  examination `[unverified]` as to frequency.
- **What the insurer must show** is a *change* relative to the state on which the *Anerkenntnis*
  rested: either a medical improvement lifting the insured above the 50 % threshold in her old
  occupation, or a new occupation **actually taken up** satisfying *konkrete Verweisung* (section 4)
  [R3] [R29].
- **The three-month run-off.** Where the insurer establishes that the conditions have ceased it
  remains liable to the **end of the third month after the notice reaches the policyholder** [R3]; a
  defective notice does not start the period at all [R29]. **Model consequence**: a claim termination
  other than death is followed by three further monthly payments — a three-month tail on every
  reactivation, and a real cash-flow effect rather than a rounding detail, because reactivation is
  concentrated in the first two years of a claim.
- ***Reaktivierung*** — the insured recovers and the cover **revives**. The contract does not end:
  the *Beitragsbefreiung* stops, the premium resumes at the same *Zahlbeitrag*, and a fresh BU may be
  claimed later. This bidirectional structure makes BU a genuine multi-state model rather than a
  decrement model, and it is the most important structural difference from delib's
  `risikolebensversicherung`.
- **Reactivation is strongly duration-dependent**: highest in the first year of a claim, falling
  sharply over the second and third, close to zero after about five [R16]. The corollary governs the
  reserve — a claim surviving its first two years is very likely to run to the *Endalter*. Any delib
  reactivation proxy must reproduce that shape, and a flat reactivation rate is a modelling error the
  tests should catch.
- **Some tariffs waive the *Nachprüfung*** after a stated benefit duration, or promise not to invoke
  *konkrete Verweisung* after a stated period `[unverified]`. Treated as an option switch, off in the
  base run.

### 7. Karenzzeit, rückwirkende Leistung and the start of benefit

- ***Karenzzeit*** — an **agreed deferment** between the onset of BU and the first payment. It is a
  contractual option chosen at inception, not a standard feature. Menus observed in the market are
  recalled as **0, 3, 6, 12, 18 and 24 months** `[unverified]`. The standard sale is **no
  Karenzzeit**; a *Karenzzeit* is taken to cut the premium, typically by a buyer who has employer
  sick pay or a professional scheme covering the first period.
- **The *Karenzzeit* is not the six-month prognosis.** They are independent and frequently confused.
  The prognosis period is part of the **definition** of BU (section 3); the *Karenzzeit* is a
  deferment of **payment** on a BU that is already established. A contract with no *Karenzzeit* still
  needs a six-month prognosis or the six-month fiction before anything is due.
- ***Rückwirkende Leistung*** — once the claim is recognised, the benefit is paid **back to the
  onset of BU** (after any *Karenzzeit*), not from the date of the decision. Combined with the
  six-month fiction this means the first payment on a typical claim is a lump sum covering the
  elapsed months plus the current month.
- **The premium keeps being paid in the meantime**, and is **refunded** for the period covered by
  the retroactive benefit when the *Beitragsbefreiung* is applied retroactively `[unverified]` as to
  whether all AVB do this. delib models the *Beitragsbefreiung* as starting at the same date as the
  benefit and treats the interim premium and its refund as netting to zero.
- **Model consequence and the delib choice.** delib's monthly model pays the *BU-Rente* from the
  first month after onset plus the *Karenzzeit*, at a `[std]` *Karenzzeit* of **0 months** in the
  base run, and does **not** model the decision delay or the catch-up lump. That is a timing
  simplification, stated in `technical-notes.md` as a known pitfall with a test asserting that the
  benefit stream starts where the notes say it does.

### 8. Leistungsdauer, Versicherungsdauer and the Endalter

- Two ages, and they are not the same thing:
  - ***Versicherungsdauer*** — the period during which a BU can incept and be covered. A BU
    beginning after it ends is not covered at all.
  - ***Leistungsdauer*** — the period over which benefit is paid on a covered claim. Payment stops
    at the *Leistungsendalter* even if the insured is still *berufsunfähig*.
- In the market standard the two are **equal**, and both end at the agreed *Endalter*. Where they
  differ, the *Leistungsdauer* is the shorter — a cheaper design in which cover runs to 67 but
  benefit stops at, say, 60 `[unverified]` as to how common that is.
- **The *Endalter* is 65 or 67**, and the market's advice is 67 because that is the statutory
  retirement age for cohorts born from 1964 `[unverified]`. Anything earlier leaves a gap between
  the end of the *BU-Rente* and the start of the old-age pension. Lower *Endalter* — 60, 62, 63 —
  are sold as budget options and are heavily discounted, because the last years before retirement
  carry by far the highest *Invalidisierungswahrscheinlichkeiten*.
- **The premium is extremely sensitive to the *Endalter*.** Moving the *Endalter* from 67 to 60
  removes the seven most expensive years of cover and, on the shape of the DAV 1997 I curve,
  removes a large share of the expected claim cost `[unverified]` as to the magnitude. This is the
  single most effective premium lever in the product and the one consumer advice warns hardest
  against using.
- **A claim in payment at the *Leistungsendalter* simply stops.** There is no commutation, no
  residual value and no conversion to an old-age annuity in the standalone product. In a BUZ on a
  *Rentenversicherung* the host contract's annuity then begins, which is exactly why the rider form
  is sold.

### 9. Beitragsbefreiung

- While the *BU-Rente* is in payment, the **premium is waived**. This is not an option; it is part
  of the core cover in every German BU contract.
- In an **SBU** the waiver covers the SBU's own premium. In a **BUZ** it covers the **entire**
  premium of the host contract as well — which is the rider form's main attraction, because it keeps
  the retirement provision running through a disability [S2].
- The waiver starts with the benefit and ends with it, including through the three-month run-off:
  during the run-off the insured is still receiving benefit and is still premium-free `[unverified]`
  as to whether all AVB align the two exactly.
- On *Reaktivierung* the premium **resumes at the same *Zahlbeitrag***, not at a repriced one. The
  insured has not aged into a higher tariff, because the tariff is level.
- **Model consequence.** The *Beitragsbefreiung* is not a benefit cash flow; it is the **absence of
  a premium cash flow** in the disabled state. In a multi-state monthly model this falls out
  automatically once premiums are weighted by the active-state count rather than by total in-force.
  Getting it wrong — weighting premiums by all surviving policies — is the classic BU modelling
  error and is pitfall 1 in delib's `technical-notes.md`.
- The *Beitragsbefreiung* is economically **large**. On a claim incepting at age 45 on a contract to
  67, it removes 22 years of premium as well as adding 22 years of annuity. For a typical office
  tariff the waived premium is of the order of 5 % of the annuity paid `[std]`, but for a manual
  trade, where the premium is three times as large for the same *BU-Rente*, it can approach 15 %.

### 10. Wiedereingliederungshilfe and the assistance benefits

- ***Wiedereingliederungshilfe*** — a **one-off lump sum** supporting a return to work after a period
  of BU, typically a stated number of monthly *BU-Renten*, recalled as up to **six** `[unverified]`,
  payable once on *Reaktivierung* or on taking up work again.
- Related benefits in the better wordings, all small relative to the annuity and all optional or
  tariff-specific: ***Umorganisationshilfe*** for the self-employed, the commercial counterpart of
  the *Umorganisationspflicht* [R29]; ***Reha-Hilfe***; ***Soforthilfe*** paid while the
  *Leistungsprüfung* runs and set against the eventual benefit; and a ***Pflegeleistung*** add-on.
- **Model consequence and the delib choice.** delib models the *Wiedereingliederungshilfe* as a
  `[std]` lump of **6 × the monthly *BU-Rente*** paid on each *Reaktivierung*, switchable off, and
  models none of the others — it is the only one of the group both common enough to be representative
  and simple enough to attach to an existing transition; the rest are discretionary, tiny, or
  duplicate a benefit already modelled. The 6-month level is `[std]`, observed range recalled as
  **3 to 12 monthly Renten** `[unverified]`.

### 11. The Arbeitsunfähigkeits-Klausel (AU-Klausel)

- **What it does.** The *AU-Klausel* pays the full *BU-Rente* on production of a **doctor's
  certificate of continuous *Arbeitsunfähigkeit*** — inability to work in the current job — of a
  stated duration, **without the insurer determining that BU exists**. The certified duration is
  normally **six months**, either already elapsed or elapsed plus certified to continue
  `[unverified]`.
- **Why it exists.** The *Leistungsprüfung* for BU takes months (section 5) and the insured has no
  income in the meantime. The *AU-Klausel* converts a long, contested, prognosis-based assessment
  into a short, documentary one. It has become the principal wording-quality differentiator in the
  contemporary German BU market and is heavily weighted in the ratings [R21] [R22].
- **How it is bounded.** Insurers limit the exposure in three ways, and the combination varies by
  tariff `[unverified]` throughout:
  1. **A maximum benefit period under the clause** — recalled as **18, 24 or 36 months**, or in some
     tariffs an unlimited AU benefit for as long as the certificates continue.
  2. **Set-off.** Payments under the clause are set against the eventual BU decision; if BU is later
     denied, the payments are usually **not** reclaimed, which is what makes the clause valuable.
  3. **A requirement to continue pursuing the BU claim** in parallel, and to supply certificates at
     stated intervals.
- **Model consequence.** The *AU-Klausel* raises the **effective inception rate** and shifts the
  **timing** of payment forward, without changing the annuity amount. delib models it as an option
  switch that (a) multiplies the inception rate by a `[std]` factor and (b) removes any decision
  delay — and, because delib already pays from onset (section 7), in the base parameterisation the
  second effect is nil and only the first survives. The `[std]` inception uplift is set at
  **1.00 in the base run (clause off)** with the switched-on value left as a model-point parameter,
  because no public data quantifies the uplift and inventing one would be worse than declaring it
  unknown (gap 12).

### 12. Options — Beitragsdynamik and Leistungsdynamik

Two escalations, on different quantities, at different times, and routinely confused.

- ***Beitragsdynamik*** (also *Anwartschaftsdynamik*) — a **pre-claim** annual increase of the
  **premium** with a corresponding increase of the insured *BU-Rente*, **without renewed
  *Gesundheitsprüfung***. Agreed rate commonly **3 % or 5 %** a year, with menus from **1 % to 10 %**
  `[unverified]`. The *BU-Rente* increase bought by a given premium increase is **less than
  proportional and falls with age**, because the extra premium buys cover at the attained age for
  the remaining term. The policyholder may **decline** an individual increase; declining a stated
  number of consecutive increases — recalled as **two or three** `[unverified]` — extinguishes the
  option permanently, which is the insurer's protection against anti-selection. **Model
  consequence**: it makes both premium and sum at risk time-varying and introduces a take-up
  assumption; delib ships it **off** in the base run, available as a model-point switch with a
  `[std]` take-up.
- ***Leistungsdynamik*** (*Rentendynamik im Leistungsfall*) — an **in-claim** annual increase of the
  *BU-Rente* **while it is being paid**, protecting the benefit over what can be a 30-year payment
  period. Agreed rate commonly **1 %, 2 % or 3 %** a year `[unverified]`, some tariffs indexing to a
  published inflation measure instead. It is paid for in the premium from inception, not on claim.
  **This is the more important of the two for a liability projection**, because it compounds over
  the whole benefit period: on a claim incepting at 40 and running to 67, a 2 % *Leistungsdynamik*
  raises the final payment to about **1.70×** the first and the total benefit paid by roughly a
  third relative to a level annuity `[std]` — arithmetic, not a source. **delib's base run carries a
  *Leistungsdynamik* of 2 % a year** `[std]`, applied on each anniversary of the benefit start,
  because a BU model without in-claim escalation misses the product's dominant long-duration
  sensitivity. The 2 % is the midpoint of the recalled 1–3 % menu and is a `[std]` choice.

### 13. Options — Nachversicherungsgarantie and Verlängerungsoption

- ***Nachversicherungsgarantie*** — the right to **increase the insured *BU-Rente* without a fresh
  *Gesundheitsprüfung***, on a defined event. It is the single most valuable option in the German BU
  product, because it lets a healthy 25-year-old lock in insurability cheaply and build the cover as
  income grows.
  - **Event-linked triggers**, near-uniform across the market: marriage or registered partnership;
    birth or adoption of a child; completion of studies or vocational training; a first job or a
    substantial pay rise; property purchase or a mortgage; starting self-employment; and in some
    tariffs the death of a partner or a divorce. **Event-independent** windows — a right to increase
    in each of the first N years regardless of any event — exist in some tariffs `[unverified]`.
  - **Caps**, all `[unverified]` in level: a maximum per event; an aggregate cap (often that the
    *BU-Rente* may at most be **doubled**); an absolute ceiling; an age limit for exercise; and the
    *Angemessenheitsgrenze* on income (section 17).
  - **Anti-selection is controlled by the event list and a short exercise window** — typically
    **6 or 12 months** from the event `[unverified]` — not by underwriting.
  - **Model consequence.** delib ships it **off** in the base run. Any on-run needs a take-up
    assumption and an anti-selection loading on the incremental cover, and neither is sourceable. It
    is specified in `product-spec.md` and named in `technical-notes.md` as an unmodelled option,
    which is the honest treatment.
- ***Verlängerungsoption*** — the right to **extend the *Versicherungs-* and *Leistungsdauer***, for
  example 63 → 65 or 65 → 67, without renewed underwriting; sold to protect against a further rise
  in the statutory retirement age, and normally exercisable only in a window before the original
  *Endalter* `[unverified]`. Modelled by delib as a model-point parameter on the *Endalter* rather
  than as a dynamic option.

### 14. The Infektionsklausel

- **The problem it solves.** A doctor, dentist, nurse or laboratory worker who is infected or is a
  carrier may be forbidden by the competent authority to practise, under a *Tätigkeitsverbot* imposed
  under the *Infektionsschutzgesetz* [R30]. She then cannot earn in her occupation — but she is not
  necessarily unable to work in the sense of § 172 VVG, so the ordinary BU definition may not bite.
- **What the clause does.** It **deems** the official prohibition to be BU, so the *BU-Rente* becomes
  payable for as long as the ban lasts, with no 50 % medical test.
- **Who gets it.** Standard for physicians and dentists; common for nursing staff, medical and dental
  assistants, midwives and laboratory personnel; not offered outside the medical field. Some wordings
  require the ban to be **complete** rather than partial or to have lasted a stated period, and end
  the benefit when the ban is lifted — which makes the *Nachprüfung* mechanical rather than medical
  `[unverified]`.
- **Model consequence.** delib does **not** model the *Infektionsklausel* separately. It is described
  in `product-spec.md` as a rating and definition variant applying to one occupational segment, and
  its effect on the model is a higher inception rate in that segment — which is already how
  *Berufsgruppen* enter (section 16). Modelling it as a distinct trigger would need a ban-incidence
  assumption no public source supplies.

### 15. The BUZ form, and the Basisrente-BUZ

- A **BUZ** is the same BU liability written as a rider [S2]. The rider premium is quoted separately
  inside the host contract's premium, the *Beitragsbefreiung* covers the whole package, and the
  rider cannot outlive the host.
- **Inside a *Rentenversicherung* or *Kapitallebensversicherung* (Schicht 3)** the tax treatment is
  the same as an SBU's (section 23) and the rider is bought for the *Beitragsbefreiung* on the
  savings premium.
- **Inside a *Basisrente* (Schicht 1)** the economics change entirely. The whole premium — savings
  plus BU — is deductible as an *Altersvorsorgeaufwendung*, provided the BU component satisfies the
  conditions of [R28]: the BU benefit must be an **annuity**, must not run beyond the host
  contract's deferment, and must account for **no more than 49 % of the total premium**
  `[unverified]`. In exchange the *BU-Rente* is taxed **in full** at the cohort *Besteuerungsanteil*
  rather than at the small *Ertragsanteil* of an SBU.
- **The trade is not obviously favourable.** A buyer in a high marginal bracket while working and a
  low one while disabled gains; a buyer whose *BU-Rente* would be her only income and would push her
  through the basic allowance may lose. The 49 % rule also forces a large savings premium alongside
  the BU cover, so the *Basisrente*-BUZ is a poor vehicle for someone who wants BU cover alone. This
  is why the **standalone SBU remains the dominant retail form** and is delib's product 9
  `[unverified]` as to the market split between SBU and BUZ (gap 3).

### 16. Underwriting — Berufsgruppen

- **Occupation is the dominant rating factor**, ahead of age and far ahead of anything else. That
  follows from the definition: the insured event is inability to do **this** job, so a job with high
  physical demands both raises the incidence and lowers the threshold at which 50 % is reached.
- **Classification.** Each insurer maintains a *Berufsgruppenverzeichnis* mapping named occupations
  to rating classes [S6]. **Four to six** classes is the common range, with some carriers running
  ten or more and direct writers as few as three `[unverified]`. The classes are **not comparable
  across carriers** — an occupation in class 2 at one insurer may be class 3 at another — which is
  precisely why the comparison portals exist.
- **The shape of the classification**, qualitatively, since no list could be sourced: academic and
  pure office occupations at the top; qualified commercial and technical next; skilled trades with
  light physical content; skilled manual trades; heavy manual, hazardous and outdoor occupations at
  the bottom. Some occupations — roofers, scaffolders, some care roles, professional drivers, some
  artistic professions — are **declined outright** by many carriers, or offered only with a
  *Karenzzeit*, a reduced *Endalter* or a limited *Leistungsdauer*.
- **The price ratio between a *Bürotätigkeit* and a *Handwerker* tariff** is the number the brief
  asks for. The recalled market range for the same age, *BU-Rente* and *Endalter* is **about 2× to
  4×**, centred near **3×** for a mainstream skilled trade against a pure office occupation, and
  **4× to 6×** for the heaviest insurable trades `[unverified]` throughout. **delib adopts a `[std]`
  occupational factor set anchored at 1.00 for the reference office class and 3.00 for the reference
  manual class**, and states in `product-spec.md` that the ratio is a construction inside an argued
  2×–4× range, not a sourced figure.
- **Academic status and qualification** move the classification independently of the job title: the
  same technical role is priced better for a graduate engineer than for a technician, on the theory
  that the graduate's job content and *Verweisung* possibilities are more office-like `[unverified]`.
- **Students and pupils** are insurable, classified by the occupation trained for or by a special
  student class — the market's principal argument for buying young.
- **Model consequence.** The *Berufsgruppe* enters delib as a **multiplicative factor on the
  inception rate and hence on the premium**, not as a different table. That is how German pricing
  works — one base table, occupational loadings — and it keeps the data files to a single inception
  curve plus a small factor table, each row carrying its `provenance` tag as ruling 2 requires.

### 17. Underwriting — Gesundheitsprüfung, Risikozuschläge, Ausschlüsse, Angemessenheitsgrenze

- **Health questions** cover treatments, complaints, diagnoses and hospitalisations over defined
  look-back windows — recalled as **five years for outpatient and ten years for inpatient treatment
  and psychotherapy** `[unverified]` — plus height and weight, current complaints, planned
  treatments, tobacco use, and existing or refused disability cover. **Psychiatric and
  musculoskeletal history are the two areas that most often produce a loading, an exclusion or a
  decline** — exactly where the claims come from (section 25).
- **Medical examination** is required above sum and age thresholds; the recalled threshold for a
  medical report is an insured annual *BU-Rente* of the order of **€18 000–€30 000** `[unverified]`.
- **Outcomes**, in the order the market uses them: acceptance at the *Normaltarif*; acceptance with a
  ***Risikozuschlag*** — a premium loading, commonly **25 % to 100 %** and occasionally more
  `[unverified]`; acceptance with an ***Ausschlussklausel*** excluding BU caused by a named condition
  or body region (spine, knee, psyche are the classic three); *Zurückstellung*; and *Ablehnung*.
- **The proportion of BU applications not accepted on standard terms is high** — an order of
  magnitude of **a quarter to a third** is recalled `[unverified]` — which is why the
  ***Risikovoranfrage*** exists: an anonymised pre-enquiry through a broker, so that a decline is
  never recorded against the applicant in the industry's *Hinweis- und Informationssystem* (HIS) and
  need not be disclosed to the next insurer [R7] [S16].
- ***Vorvertragliche Anzeigepflicht*.** Incomplete health answers are the commonest reason a
  technically valid claim fails, because the *Leistungsprüfung* routinely obtains the full medical
  history [R7] [R21]. Remedies lapse after five years, ten for intent or fraud `[unverified]`.
- ***Angemessenheitsgrenze*.** Insurers cap the insurable *BU-Rente* at a fraction of income —
  recalled as **60–70 % of gross** or around **80 % of net** `[unverified]` — to preserve the
  incentive to return to work, applied at inception and on every *Nachversicherungsgarantie*
  exercise. It bounds the sum insured but does not enter the recursion; delib records it as an issue
  rule.
- **Smoker status** is a rating factor in *Risikolebensversicherung* but is **not** systematically
  one in BU `[unverified]`; where it appears its effect is far smaller than the occupational factor.

### 18. Premium — Bruttobeitrag, Zahlbeitrag and the Beitragsverrechnung

**This is the mechanic a German BU model must get right, and it has no counterpart in the US, UK or
French products in this repository.**

- A German BU tariff is quoted as **two numbers**: the ***Bruttobeitrag*** (*Tarifbeitrag*), computed
  on first-order bases and the **contractually guaranteed maximum** the insurer may ever charge; and
  the ***Zahlbeitrag*** (*Nettobeitrag*), what the policyholder actually pays after the anticipated
  *Überschussbeteiligung* has been applied in advance as a reduction of the premium.
- **The mechanism is *Beitragsverrechnung***, the standard *Überschussverwendung* in German
  biometric business: the surplus a contract is expected to generate — overwhelmingly **risk
  surplus**, because the first-order *Invalidisierungswahrscheinlichkeiten* are deliberately prudent,
  plus **expense surplus** — is credited immediately against the premium rather than accumulated
  [R10] [R14].
- **The gap is large.** The recalled market range for *Zahlbeitrag* / *Bruttobeitrag* is **0.50 to
  0.80**, most commonly **0.60 to 0.75** `[unverified]`. delib adopts a `[std]` ratio of **0.70**,
  the midpoint of the recalled common range, and states it as a construction.
- **The gap is also a risk to the buyer, and that is the point.** If risk experience deteriorates or
  expense surplus falls, the insurer may reduce the *Beitragsverrechnung* and raise the *Zahlbeitrag*
  — **up to the *Bruttobeitrag* and no further**. A buyer who chose on *Zahlbeitrag* alone can face
  an increase of 40 % or more with no change in cover and no right to complain. Hence the consumer
  advice to compare *Bruttobeiträge* [S16] and the ratings' scoring of *Beitragsverrechnung*
  stability [R22] [R23].
- **Alternative *Überschussverwendungen*** appear in some tariffs: a ***Bonusrente***, in which
  surplus buys additional *BU-Rente*; ***verzinsliche Ansammlung***; and an ***Überschussrente im
  Leistungsfall***, paid as an increment to the annuity while a claim runs. `[unverified]` as to
  their market shares; *Beitragsverrechnung* is dominant and is what delib models.
- **Model consequence and the delib choice.** delib projects **both** premium streams. The
  *Bruttobeitrag* is the contractual quantity, the *Zahlbeitrag* is what is collected, and **the
  difference is the modelled *Überschussbeteiligung***. There is no surplus account, no RfB and no
  declaration mechanic in this model — a deliberate simplification, correct for BU precisely because
  the surplus is applied immediately rather than accumulated, and stated as such in
  `technical-notes.md`. A model projecting only the *Zahlbeitrag* silently assumes the
  *Beitragsverrechnung* never changes; one projecting only the *Bruttobeitrag* overstates premium
  income by about 43 %.
- **Premium payment.** Monthly by SEPA direct debit is the retail norm; quarterly, half-yearly and
  annual are offered, loaded by a ***Ratenzahlungszuschlag*** whose German market convention is
  recalled as **2 % half-yearly, 3 % quarterly, 5 % monthly** `[unverified]` and carried by delib as
  `[std]`. Premiums run for the whole *Versicherungsdauer* — there is no shorter premium-paying
  option in the standard product — and stop on death, lapse, or the start of the *Beitragsbefreiung*.
- ***Stundung* and *Anwartschaft*.** Most tariffs allow the premium to be deferred or the contract
  put into a dormant *Anwartschaft* for parental leave, unemployment or further study, preserving
  insurability without full cover `[unverified]`. Not modelled; named in `product-spec.md` as an
  unmodelled feature.

### 19. Charges

**No German insurer publishes the charge structure of a BU tariff, and there is no *Effektivkosten*
disclosure for a pure risk product** [R12] [S14]. Everything here is `[std]` or `[unverified]`, and
`technical-notes.md` says so in the same words.

- ***Abschluss- und Vertriebskosten*** — financed by *Zillmerung* into the *Deckungsrückstellung* and
  capped at the *Höchstzillmersatz* of **25 ‰ of the *Beitragssumme*** [R13] `[unverified]`. For BU
  the *Beitragssumme* is large — 37 years at a monthly *Bruttobeitrag* of €100 is €44 400 — so the
  zillmered allowance is large in absolute terms though the annual premium is modest. delib's `[std]`
  acquisition assumption sits **at the cap**, because that is where German level-premium risk
  business generally sits and because a cap is at least a sourced ceiling.
- ***Verwaltungskosten*** — a percentage-of-*Bruttobeitrag* loading plus a flat annual per-policy
  amount, both `[std]`, with levels chosen so the worked example reproduces exactly and stated as
  constructions.
- ***Leistungsbearbeitungskosten*** — **claims-handling costs, a genuinely material and BU-specific
  charge**: a BU claim is expensive to assess (medical reports, occupational analysis, sometimes
  litigation) and expensive to maintain (annual *Nachprüfung*). delib carries a `[std]` one-off
  assessment cost at claim inception and a `[std]` recurring cost per month in payment, and names
  them as the charge a modeller from a term-life background will forget.
- ***Ratenzahlungszuschlag*** — section 18. **No premium tax** [R31] `[unverified]`.

### 20. Rechnungsgrundlagen and the multi-state structure

- **Three biometric bases are needed**, and the market's first-order set is the DAV 1997 family
  [R16]:
  1. ***Invalidisierungswahrscheinlichkeit*** *i(x)* — active life aged *x* becomes *berufsunfähig*
     within the year. Rises steeply with age: the curve is roughly flat and low to about 30, rises
     through the forties, and accelerates sharply from the mid-fifties. This is why the *Endalter*
     is the dominant premium lever (section 8).
  2. ***Reaktivierungswahrscheinlichkeit*** *r(x, s)* — disabled life recovers, depending on **age
     at disablement** *x* and **duration since disablement** *s*. Concentrated in the first one to
     two years; near zero after about five (section 6).
  3. ***Sterbewahrscheinlichkeit der Invaliden*** *q^i(x, s)* — mortality of disabled lives,
     materially above active mortality and itself select on duration.
  Plus **active-lives mortality** *q^a(x)* from a *Todesfall*-character table [R17], and a
  **lapse rate**.
- **All are unisex for pricing** [R15], whatever the underlying research bases are.
- **None is public.** delib ships `[std]` proxies with a `provenance` column on every row (ruling 2)
  and states in `model.md` what a replacement built from the real DAV tables must preserve: the age
  shape of *i(x)*, the duration shape of *r*, and the excess of *q^i* over *q^a*.
- **Lapse.** German BU lapse rates are lower than for savings contracts — the cover is hard to
  replace once health has changed, which is a powerful anti-lapse force and a selective one, because
  the lives who lapse are disproportionately the healthy ones. delib uses a `[std]` *Stornoquote*
  falling with duration, on the order of **4 % a year in the first two years falling to 2 %**
  `[std]`, with the selection effect **not** modelled and named as a model risk.
- **The state space.** Four states — *aktiv* (paying premium, exposed to inception, death and
  lapse), *leistungspflichtig* (receiving *BU-Rente*, premium-free, exposed to reactivation and to
  disabled mortality), *tot*, *storniert* — with a transition back from *leistungspflichtig* to
  *aktiv*. Monthly grid (`BU_DE_S`), premiums and annuity both monthly in advance, and the
  three-month run-off of § 174 [R3] attached to every reactivation.

### 21. Deckungsrückstellung, Rückkaufswert and Beitragsfreistellung

- **The reserve is real.** A level-premium BU contract to 67 overcharges heavily in the early years
  relative to *i(x)*, and the excess accumulates as *Deckungsrückstellung*. This is the *provision
  pour risques croissants* problem in German dress, and it makes BU a much better mechanics
  demonstration than a term-life contract.
- **Two reserves, not one.** A BU book carries (a) a *Deckungsrückstellung* for **active** lives —
  the prospective difference between future benefits and future premiums — and (b) a
  ***Leistungsrückstellung* / *Deckungsrückstellung für laufende Renten*** for **claims in payment**,
  which is the present value of the remaining annuity on disabled-lives bases. The second is much
  the larger per life. delib publishes **undiscounted gross cash flows only** and does not compute
  either; both are named as valuation pointers in `technical-notes.md`.
- ***Rückkaufswert*** — payable under § 169 VVG through § 176 [R5] [R9]. It exists and is not
  nominal, but it is small relative to premiums paid, is depressed by *Zillmerung* in the early
  years, and may be reduced by a contractual, quantified *Stornoabzug*. Some BU wordings state that
  the contract has no or only a minimal surrender value in the first years `[unverified]`.
- ***Beitragsfreistellung*** — § 165 VVG through § 176 [R8]. Produces a *beitragsfreie BU-Rente*,
  a small fraction of the original. It is the policyholder's alternative to surrendering when the
  premium becomes unaffordable and is the option consumer advice recommends over lapse [S16].
- **delib models neither surrender nor paid-up as a cash flow.** Lapse removes the policy from the
  in-force count and pays nothing, which is the correct treatment for a gross benefit-and-premium
  cash-flow projection and is stated as a scope limitation rather than left to be discovered.

### 22. Exclusions

- The German BU exclusion list is short by international standards and broadly uniform `[unverified]`
  as to any particular carrier: BU caused by **war or internal unrest** (with a carve-out where the
  insured is passively caught up in it); by the **deliberate execution or attempted execution of a
  crime**; by the insured's **intentional self-harm**, subject to the *Selbsttötung* rule of § 161 VVG
  through § 176 [R5] [R11]; by **nuclear energy**; and, in some wordings, by **aviation other than as
  a passenger** and defined hazardous activities, or those loaded rather than excluded.
- **What is notably *not* excluded**: illness of any kind, **including psychiatric illness** — the
  largest single cause of BU (section 25) — and ordinary accidents. A cheaper "BU ohne Psyche"
  variant exists at the margin of the market `[unverified]`; consumer advice is uniformly against it,
  since excluding the largest cause removes about a third of the cover.
- Individual ***Ausschlussklauseln*** imposed at underwriting (section 17) sit alongside the general
  list and are contract-specific.
- **Model consequence.** Exclusions are absorbed into the calibration of *i(x)*, not modelled
  separately.

### 23. Taxation

- **Premium, standalone SBU (Schicht 3).** A *sonstige Vorsorgeaufwendung* under
  § 10 Abs. 1 Nr. 3a EStG [R27], deductible only within an annual ceiling recalled as **€1 900**
  (employees, civil servants) / **€2 800** (self-employed) `[unverified]`. That ceiling is in
  practice already consumed by statutory health and long-term-care contributions, so **the effective
  deduction for most buyers is nil**. This is a real product fact, not a technicality: it is the
  main reason the *Basisrente*-BUZ exists.
- **Benefit, standalone SBU.** The *BU-Rente* is an *abgekürzte Leibrente* taxed on its
  ***Ertragsanteil*** under § 22 Nr. 1 EStG [R27]. The *Ertragsanteil* is read from a table keyed on
  the annuity's **remaining term at the start of payment**, not on the recipient's age. Recalled
  values `[unverified]` throughout: about **5 %** for a 5-year remaining term, **12 %** for 10 years,
  **16 %** for 15, **21 %** for 20, **26 %** for 25 and **30 %** for 30. A €1 500 monthly *BU-Rente*
  starting at 45 and running to 67 (22 years) therefore brings roughly €4 000 a year into taxable
  income out of €18 000 received — a light burden, and the compensation for the non-deductible
  premium.
- **Benefit, BUZ inside a *Basisrente* (Schicht 1).** Fully taxable as *sonstige Einkünfte* at the
  cohort ***Besteuerungsanteil***, against a fully deductible premium [R27] [R28] (section 15).
- **No premium tax** [R31] `[unverified]`.
- **Model consequence.** delib projects **gross, pre-tax** cash flows in every product. Taxation is
  described in `product-spec.md` and does not enter the model. It is recorded here at length because
  it is the reason two economically identical contracts are sold in two different wrappers.

### 24. The gesetzliche Erwerbsminderungsrente underneath

The German private BU contract is a top-up on a statutory benefit that deliberately does not cover
occupational disability. The design only makes sense against that background.

- **There is no statutory occupational-disability pension for anyone born on or after 2 January
  1961** [R25] `[unverified]` on the date. The statutory *Berufsunfähigkeitsrente* was closed to
  later cohorts by the 2001 reform; § 240 SGB VI preserves it only for the older ones. **That reform
  created the modern German private BU market.**
- **What remains is the *Erwerbsminderungsrente*** [R24], in two tiers, both tested against the
  **general labour market** and measured in **hours a day**, not against the insured's own
  occupation: ***volle Erwerbsminderung*** — able to work **less than three hours** a day; and
  ***teilweise Erwerbsminderung*** — **at least three but less than six**, paying about **half** the
  full benefit. Both need the five-year *Wartezeit* plus three years of compulsory contributions in
  the last five `[unverified]`; both are normally granted as a renewable *Zeitrente*.
- **Why it is not a substitute for BU**, in four points the private product answers:
  1. **The test is the general labour market, not the last occupation.** A surgeon who loses the use
     of a hand cannot operate but can answer a telephone for six hours a day: fully *berufsunfähig*,
     not at all *erwerbsgemindert*.
  2. **The threshold is far higher.** BU bites at 50 % of one's own job; full EM needs a capacity
     below three hours a day in **any** work.
  3. **The level is low.** Recalled averages `[unverified]`: a new *volle Erwerbsminderungsrente* of
     roughly **€1 000 a month gross** before deductions, and a *teilweise* one of about half that,
     against a replacement need normally put at 70–80 % of net income. *Abschläge* of up to **10.8 %**
     for early receipt reduce it; the *Zurechnungszeit* extensions of recent reforms raised it.
  4. **The self-employed are frequently not insured in the statutory scheme at all**, so for them
     the statutory floor is zero and BU is the whole cover.
- **Model consequence: none.** The statutory pension is **not** offset against the *BU-Rente* in the
  standard German contract — the *BU-Rente* is paid in addition. Offsetting products exist at the
  margin `[unverified]` and are not modelled. This section justifies the product's market role; it
  does not enter the recursion.

### 25. Statistics — causes, average benefit, age at claim, Anerkennungsquote

**Every figure in this section is `[unverified]`.** None was corroborated by any search or document,
and the year each belongs to is itself uncertain. They are recorded so a later researcher knows the
shape to expect and the publisher to check against; **no delib document should print any of them
without re-establishing it** from [R21], [R22], [R20] or [R26].

- **Causes of BU.** Usual publisher: Morgen & Morgen, annually [R22]. Recalled distribution, for a
  recent year in the **2023–2024** range `[unverified]`:

| Cause group | Recalled share | Tag |
|---|---|---|
| *Nervenkrankheiten*, including psychiatric conditions | about 33 % | `[unverified]` |
| *Erkrankungen des Skelett- und Bewegungsapparates* | about 20 % | `[unverified]` |
| *Krebs und andere bösartige Geschwülste* | about 18 % | `[unverified]` |
| *Sonstige Erkrankungen* | about 15 % | `[unverified]` |
| *Unfälle* | about 7 % | `[unverified]` |
| *Erkrankungen des Herzens und des Gefäßsystems* | about 7 % | `[unverified]` |

  The **direction of travel** is better established than the levels: the psychiatric share has risen
  over two decades from roughly a quarter to roughly a third while the musculoskeletal share has
  fallen `[unverified]`. **Accidents are a small minority — under a tenth** — which is the single
  most useful number in the table, because it answers the buyer who thinks an *Unfallversicherung*
  is a substitute.
- **Average insured *BU-Rente*** — roughly **€1 000–€1 200 a month** in new business `[unverified]`,
  against a recommended 70–80 % of net income: the market is systematically underinsured relative to
  its own advice.
- **Average age at claim** — recalled in the range **47 to 52** `[unverified]`, strongly skewed to
  the last decade before the *Endalter*, which is the actuarial content of section 8.
- ***Anerkennungsquote*** — usual publisher **Franke und Bornberg**, in its recurring
  *BU-Leistungspraxis* study [R21]; the GDV has more recently published an industry figure [R20].
  Recalled level **about 75 % to 80 %** of decided claims accepted `[unverified]`. Recalled
  composition of the declines `[unverified]`: roughly half because the **50 % BU degree is not
  reached**; a smaller share on ***Anzeigepflichtverletzung*** or *Anfechtung*; the rest on failure
  to co-operate or withdrawal. Litigation follows only a small minority of declines.
- **Model consequence.** The *Anerkennungsquote* enters delib as a `[std]` **acceptance factor on
  the inception rate**, set at **0.80**, applied to the transition rather than to the benefit,
  because a declined claim generates no annuity at all. The causes distribution does not enter the
  model; it enters `product-spec.md` as the reason not to model an accident-only variant.

### 26. Typical parameter levels

All levels `[unverified]` unless marked `[std]`; ranges are the author's recollection of the German
retail market and must be re-established before use.

| Parameter | Typical level | Recalled range | Tag |
|---|---|---|---|
| *BU-Rente* | €1 500 per month | €1 000 – €2 000; higher for high earners | `[unverified]` |
| *Endalter* (cover and benefit) | 67 | 60, 62, 63, 65, 67 | `[unverified]` |
| Entry age | 25 – 35 | 15 (pupils) – 50 | `[unverified]` |
| Term | 32 – 42 years | anything to the *Endalter* | derived |
| *Karenzzeit* | 0 months | 0, 3, 6, 12, 18, 24 | `[unverified]` |
| *Leistungsdynamik* | 2 % a year | 1 % – 3 % | `[std]` level |
| *Beitragsdynamik* | 3 % or 5 % a year, or none | 1 % – 10 % | `[unverified]` |
| *Zahlbeitrag* / *Bruttobeitrag* | 0.70 | 0.50 – 0.80 | `[std]` level |
| *Berufsgruppen* per carrier | 4 – 6 | 3 – 10+ | `[unverified]` |
| Manual : office premium ratio | 3× | 2× – 4×, up to 6× for the heaviest | `[std]` level |
| *Angemessenheitsgrenze* | 60 – 70 % of gross income | — | `[unverified]` |
| *Ratenzahlungszuschlag* | 5 % monthly, 3 % quarterly, 2 % half-yearly | — | `[std]` |

- **Price points the brief asks for.** For a **BU-Rente of €1 500 a month to age 67, entry age 30**,
  the recalled *Zahlbeitrag* is of the order of **€55 – €90 a month for a pure office occupation**
  and **€160 – €300 a month for a mainstream skilled manual trade** `[unverified]` on both. The
  corresponding *Bruttobeiträge* are those figures divided by the *Beitragsverrechnung* ratio, i.e.
  roughly **€80 – €130** and **€230 – €430**. **These are recollections, not quotations**, and they
  are the single most likely figures in this file to be materially wrong; they belong to gap 11.
- **delib's anchor model point** (`[std]` throughout, and the choices are argued in
  `product-spec.md`): entry age **30**, occupational class **office (factor 1.00)**, *BU-Rente*
  **€1 500 a month**, *Endalter* **67**, *Karenzzeit* **0**, *Leistungsdynamik* **2 %**, no
  *Beitragsdynamik*, monthly premium, *Zahlbeitrag* = 0.70 × *Bruttobeitrag*. Chosen because it is
  the market's central sale, because a 37-year term exercises the full inception curve, and because
  an office class keeps the premium in a range a reader can sanity-check.

---

## Observed variation across insurers

**This table records where the variation lies, not who sits where.** When it was written no insurer
document had been retrieved. Five were read on 2026-08-30 — Alte Leipziger (S4), NÜRNBERGER (S6),
VOLKSWOHL BUND (S9), Debeka and CosmosDirekt (S12) — together with the GDV model conditions (S1, S2
and the AU variant at S8), and the per-entry `Retrieved` lines above and the corresponding table in
`products/berufsunfaehigkeit/product-spec.md` carry what those wordings say. **No price, tariff
table, occupational factor or *Brutto*/*Zahlbeitrag* pair was obtained from any of them**, so no row
here compares carriers on cost.

| Feature | Market position | Where carriers genuinely differ | Tag |
|---|---|---|---|
| BU definition (50 %, six months, last occupation) | uniform, descended from the GDV model text | almost nowhere | [S1] [R1] |
| *Abstrakte Verweisung* | waived by essentially all current tariffs | legacy books only | [S1]–[S12] |
| *Konkrete Verweisung* | retained | whether it is waived on a material income drop; the *Lebensstellung* threshold | [S1] `[unverified]` |
| *Prognosezeitraum* | 6 months | a minority shorten it to 3 | `[unverified]` |
| Retroactive payment from onset | market standard | weaker wordings pay from the end of the six months | `[unverified]` |
| *Befristetes Anerkenntnis* | permitted once, § 173 | maximum length (6 or 12 months); some waive it entirely | [R2] `[unverified]` |
| *Nachprüfung* frequency | annual or biennial | some waive it after a stated benefit duration | `[unverified]` |
| Three-month run-off | statutory floor, § 174 | some contract for longer | [R3] |
| *Karenzzeit* menu | 0 as standard | 0/3/6/12/18/24 offered | `[unverified]` |
| *Endalter* menu | 65 or 67 | 60/62/63 as budget options | `[unverified]` |
| *AU-Klausel* | the principal differentiator | present or absent; 18/24/36-month cap or unlimited; set-off rules | `[unverified]` |
| *Nachversicherungsgarantie* | present everywhere | event list breadth, per-event and aggregate caps, event-independent windows | `[unverified]` |
| *Leistungsdynamik* | offered everywhere | 1–3 % fixed or index-linked | `[unverified]` |
| *Wiedereingliederungshilfe* | common | 3 to 12 monthly *Renten* | `[unverified]` |
| *Infektionsklausel* | standard for medical occupations | scope of occupations covered | [R30] `[unverified]` |
| *Berufsgruppen* | 4–6 typical | 3 at direct writers to 10+ at specialists; and which occupations are declined | `[unverified]` |
| *Zahlbeitrag* / *Bruttobeitrag* | 0.50 – 0.80 | the widest and least transparent variation in the product | `[unverified]` |
| Channel | broker vs direct vs bank/*Öffentliche* | option breadth and occupational appetite track the channel, not the carrier | [S12] |

**Representative design the research supports.** A **single-life, individual, standalone SBU**;
monthly grid; the market-standard definition — **last occupation, 50 %, six-month prognosis with the
six-month fiction, *abstrakte Verweisung* waived, *konkrete Verweisung* retained**; a **level
*Bruttobeitrag*** guaranteed for the term with a ***Zahlbeitrag* of 0.70 × *Bruttobeitrag*** `[std]`
representing the *Beitragsverrechnung*, so that the *Brutto*/*Zahl* gap **is** the modelled
*Überschussbeteiligung* and no surplus account is needed; a monthly ***BU-Rente*** paid in advance
from onset with **no *Karenzzeit*** and a ***Leistungsdynamik* of 2 %** `[std]`; full
***Beitragsbefreiung*** while in claim; benefit ending at **age 67**, on death, or on a
***Nachprüfung*** termination followed by the **statutory three-month run-off**; *Reaktivierung*
returning the life to the premium-paying state with a `[std]` ***Wiedereingliederungshilfe* of six
monthly Renten**; an ***Anerkennungsquote* acceptance factor of 0.80** `[std]` on the inception
rate; occupational rating as a **multiplicative factor, 1.00 for office and 3.00 for the reference
manual class** `[std]`; and **no surrender or paid-up cash flow modelled**. The options the corpus
describes but cannot quantify — *Nachversicherungsgarantie*, *Beitragsdynamik*, *AU-Klausel*,
*Verlängerungsoption*, *Infektionsklausel* — are specified in `product-spec.md` and shipped **off**,
which is the honest treatment of an option whose take-up and anti-selection loading no source
supplies.

---

## Gaps and caveats

1. **This caveat has been overtaken by the retrieval pass of 2026-08-30 and is superseded by the
   per-entry `Retrieved` lines above.** It was written when nothing had been read. Eight documents
   and nineteen statutory provisions have since been read and are recorded entry by entry; what
   remains unretrieved is every **quantitative** source — no price, no rate card, no occupational
   table, no DAV table, no rating-agency or consumer-press figure — and the DAV tables cannot be
   retrieved at all, being unpublished. The retrieval-conditions statement at the head of this file
   now carries both halves: the conditions the file was **written** under, and what the pass
   established — 26 of the 47 entries read `Retrieved: yes` and 21 read `no`.

2. **No insurer *Bedingungswerk* was opened, so no carrier-level parameter is attributed.** The
   variations table above records market positions, not carriers. Sixteen named German life
   insurers write this product [S3]–[S12]; the file names them and attributes nothing to them.

3. **The SBU / BUZ market split is unknown.** Whether the standalone or the rider form dominates
   German new business, and by how much, is not established [R20]. delib's choice of the standalone
   form as product 9 rests on the argument in section 15, not on a market-share figure.

4. **No *Produktinformationsblatt* was retrieved, so no *Brutto*/*Zahlbeitrag* pair is sourced.**
   The PIB [S13] is the one public document that routinely prints both figures for a named age,
   occupation and *BU-Rente*. Without one, the 0.70 ratio in section 18 is `[std]` and the recalled
   0.50–0.80 range is `[unverified]`. **This is the most consequential single gap in the file**,
   because the ratio drives the modelled premium income directly.

5. **No rate card of any kind was obtained.** No German BU tariff table, no occupational factor set,
   no age curve. Every premium level in section 26 is a recollection. Contrast frlib's
   `temporaire_deces`, where one carrier published a complete attained-age grid and the model
   reproduces it exactly; **delib's BU model can reproduce nothing external** and its worked example
   is internally consistent only.

6. **No history of *Zahlbeitrag* increases was established.** The risk that an insurer reduces its
   *Beitragsverrechnung* and raises the premium toward the *Bruttobeitrag* is the product's main
   consumer risk (section 18), and its empirical frequency and size are unknown [R23].

7. **The DAV 1997 tables are not public and were not seen.** delib ships `[std]` proxies for
   *i(x)*, *r(x, s)* and *q^i(x, s)* [R16]. Their **shapes** are asserted from general actuarial
   knowledge — steeply rising inception, front-loaded reactivation, disabled mortality above active
   — and their **levels** are constructions anchored so the worked example reproduces exactly.

8. **The DAV table names may be wrong.** This file states that the reactivation probabilities sit in
   a table recalled as **DAV 1997 RI** and that **DAV 1997 TI** is disabled-lives mortality,
   correcting the brief that commissioned it. That correction is itself `[unverified]` [R16]. Anyone
   citing a DAV table name in a delib document must confirm it first.

9. **Whether a successor to DAV 1997 I exists is unresolved.** No newer homologated German BU
   first-order table could be established [R16] [R18]. The file treats DAV 1997 I as current and
   flags the question rather than answering it.

10. **The statutory text was not read, so every paragraph number is `[unverified]`.** §§ 172–177 VVG
    are cited throughout on the author's recollection [R1]–[R6]. The two specific items most at risk
    are the **exact range of sections § 176 imports** — on which the surrender value, the paid-up
    right and the *Überschussbeteiligung* all depend — and the **precise wording of § 173 Abs. 2**
    on the *befristetes Anerkenntnis*.

11. **The price points in section 26 are the least reliable numbers in the file.** The recalled
    €55–€90 (office) and €160–€300 (manual) monthly *Zahlbeiträge* at age 30 for €1 500 to 67 are
    recollections of consumer-press figures, with no year attached and no source [S15]. Treat them
    as order-of-magnitude only.

12. **The *AU-Klausel*'s effect on inception is unquantified.** No public source gives the uplift in
    claim frequency a six-month *Arbeitsunfähigkeit* trigger produces (section 11), so delib ships
    the clause off and leaves the uplift as an unset model-point parameter rather than inventing one.

13. **The statistics in section 25 carry no confirmed year.** The causes distribution, the average
    *BU-Rente*, the average age at claim and the *Anerkennungsquote* are all recalled without a
    verified vintage [R20]–[R22]. The house rule that every figure carries its year is satisfied only
    by the honest answer here: **the year is not established**, and the figures are tagged
    accordingly rather than given a plausible-looking date.

14. **The *Erwerbsminderungsrente* levels are recalled, not sourced** [R26]. The €1 000-a-month
    order of magnitude for a new *volle* pension, the half-of-that for the *teilweise*, the 10.8 %
    *Abschlag* and the 2 January 1961 cohort boundary all need re-establishing before any delib
    document prints them.

15. **Tax figures are recalled.** The €1 900 / €2 800 *Vorsorgeaufwendungen* ceilings, the
    *Ertragsanteil* table and the 49 % *Basisrente* threshold are all `[unverified]` [R27] [R28].
    delib projects pre-tax cash flows, so nothing in the model depends on them, but nothing in
    `product-spec.md` should assert them either.

16. **Charges are entirely `[std]`.** No German insurer discloses BU acquisition, administration or
    claims-handling costs, and a pure risk product carries no *Effektivkosten* disclosure [R12]. The
    25 ‰ *Höchstzillmersatz* [R13] is the only sourced ceiling in the whole charge structure, and it
    is `[unverified]` as to its own figure.

17. **Lapse selection is not modelled.** BU lapse is strongly selective — the healthy leave, the
    impaired cannot — and delib's `[std]` *Stornoquote* ignores that, understating the average
    inception rate of the surviving book. Named as a model risk in `technical-notes.md` rather than
    corrected, because correcting it needs an assumption no source supplies.

18. **Living texts.** The VVG, SGB VI, EStG, DeckRV, MindZV, VAG and IfSG are all amended
    frequently, and the *Höchstrechnungszins* changes by instrument [R13]. No version date is
    asserted anywhere in this file, because none was seen. Check every provision against the current
    consolidated text before relying on it.
