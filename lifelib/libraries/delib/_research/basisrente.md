# Basisrente (Rürup-Rente), Schicht 1 — research notes (Germany)

Research notes for the German **Basisrente** — the *Basisrentenvertrag* of § 10 Abs. 1 Nr. 2
Buchstabe b EStG, created by the *Alterseinkünftegesetz* of 2004 and sold under the popular name
*Rürup-Rente* after Bert Rürup, who chaired the commission that proposed it. It is the first layer
(*Schicht 1*) of the German three-layer retirement architecture: a privately written, funded,
individually owned contract that is nevertheless treated for tax purposes like the *gesetzliche
Rentenversicherung* — contributions deductible as *Sonderausgaben* on the way in, benefits taxed
as *sonstige Einkünfte* on the way out, at a *Besteuerungsanteil* fixed by the cohort year of
*Rentenbeginn*.

**The product is defined by prohibitions, not by benefits.** Its accumulation and payout mechanics
are those of an ordinary German deferred annuity — the same *Deckungskapital* recursion, the same
*Überschussbeteiligung*, the same *Rentenfaktor*, the same DAV 2004 R basis as the delib
`klassische_rentenversicherung` product. What makes it a distinct product, and what a projection
model has to get right, is a closed list of things it may **not** do: the entitlement may not be
inherited, transferred, charged as security, sold or turned into capital, and no *Rückkaufswert*
may be paid on termination. Everything else in this file follows from that sentence.

**In scope.** The individual, privately written *Basisrentenvertrag (Alter)* on a single life
against a *laufender Beitrag*, a *Zuzahlung* or a *Einmalbeitrag*, certified under § 5a AltZertG,
in all three of its asset forms — *klassisch* (general account), *fondsgebunden* (unit-linked) and
*fondsgebunden mit Beitragsgarantie* (hybrid) — together with the two riders the statute permits
inside the same contract: *Hinterbliebenenabsicherung* and *Berufsunfähigkeits-Zusatzversicherung*.

**Out of scope, and said so where it matters.**

- **The other two layers.** *Riester-Rente* (Schicht 2, delib product 6) shares the AltZertG
  certification regime but has a different subsidy (*Zulage* plus § 10a EStG), a mandatory
  *Beitragserhaltungsgarantie*, a permitted 30 % *Teilkapitalauszahlung* and a *Kleinbetragsrenten*
  commutation — of which the first three the Basisrente does not have, while the fourth it does
  have (mechanic 19) and this model does not implement. *Klassische private Rentenversicherung*
  (Schicht 3, delib product 2) has the same chassis with none of the constraints: full
  *Kapitalwahlrecht*, a *Rückkaufswert*, free beneficiary designation, and *Ertragsanteil* taxation.
  Both are separate delib products and are referenced here only as contrasts.
- **The competing Schicht-1 vehicles.** The *gesetzliche Rentenversicherung*, the
  *berufsständische Versorgungswerke* and the *landwirtschaftliche Alterskasse* sit in
  § 10 Abs. 1 Nr. 2 **Buchstabe a** EStG and share the **same annual *Höchstbetrag*** as the
  Basisrente. They are not modelled, but the shared ceiling is a first-order fact about the product
  and is treated in mechanic 6.
- **The *Fonds-Basisrente*.** A Basisrentenvertrag may also be written by a
  *Kapitalverwaltungsgesellschaft* as a fund savings plan whose payout phase is bought in from a
  life insurer. It meets the same § 10 and § 5a AltZertG tests and competes for the same buyer, but
  its accumulation phase is not an insurance liability and delib does not model it.
- **Betriebliche Altersversorgung** in all five *Durchführungswege*, *Gruppenversicherung*, *private
  Krankenversicherung* and *Sterbegeldversicherung* are outside the delib library entirely.
- Austrian and Swiss documents are excluded even where a search would return them: the EStG, the
  AltZertG and the DeckRV do not apply to them.

These notes are the **citation ground truth** for the delib `basisrente` product documents. Source
ids **S1..S16** and **R1..R24** below are **frozen — never renumber**; unused ids are simply
omitted downstream, leaving gaps, and `sources.md` records which are absent and why.

Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

Read this before reading anything else in the file. It is what separates a delib citation from an
frlib one. It has two halves, because the conditions changed after the file was drafted: how the
research was **done** on 2026-08-29, and what the **re-verification** of 2026-08-30 established. Both
belong in the record, and neither replaces the other.

**How this file was drafted.** **No document in this file was retrieved when it was written.** Direct
HTTP egress from the build environment was blocked by an organisation network policy. `WebFetch` and
`curl` were refused at the egress gateway for every host outside a short package-registry
allowlist. The hosts that matter for this product were tried again while writing this file and
every one of them was refused with the identical
error — `curl: (56) CONNECT tunnel failed, response 403`: **`gesetze-im-internet.de`** (EStG § 10
and § 22, AltZertG, ZPO § 851c, VVG, DeckRV), **`bafin.de`**, **`gdv.de`**, **`aktuar.de`**,
**`bundesfinanzministerium.de`**, **`bzst.de`** — the authority that certifies Basisrentenverträge —
and **`de.wikipedia.org`**.

Not one *Bedingungswerk*, not one *Produktinformationsblatt*, not one *Basisinformationsblatt*, not
one statutory text, not one BMF-Schreiben and not one insurer *Verbraucherinformation* was opened.

**There was also no search channel.** The session's `WebSearch` budget — a hard cap of 200 calls
shared across all delib work — was **exhausted before this product was reached**. The two delib
research files written earlier (`kapitallebensversicherung.md`, `klassische_rentenversicherung.md`)
consumed it. This file was therefore written with **no research channel of any kind**: no fetch, no
search, no snippet, no summary. That is a materially weaker evidential position than either sibling
file, and it is stated on every source entry rather than glossed.

What followed from that, exactly, and it was applied without exception when this file was written:

1. **Every source entry carried the honest retrieval line.** The standard line was
   `Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)`. A
   small number of entries carried a stronger line because their **identity** was established in a
   sibling delib research file while search was still available; those say so and name the file.
   `Retrieved: yes` appeared nowhere in the drafted document. **It does now, and rule 1 is the one
   rule below that the re-verification overtook** — see *What the re-verification changed*.
2. **Nothing was quoted.** Not one sentence of German statutory or contractual wording appears here
   in quotation marks as though it were read. Where the substance of a provision is given, it is
   given in English, in this file's own words, as *what the provision does*. A reader who needs the
   wording must go to the instrument.
3. **No URL, document number, edition, page count or publication date is invented.** Where a
   canonical `gesetze-im-internet.de` form is obvious — `.../estg/__10.html` for § 10 EStG — it is
   offered and marked `[unverified]`. Everywhere else the entry says `URL: not established`. No
   *Bundesgesetzblatt* citation and no BMF-Schreiben file number appears anywhere in this file,
   because none could be confirmed.
4. **`[unverified]` is used generously and means what it always means.** Every specific paragraph
   number, every effective date, every monetary amount, every percentage and every market figure in
   this file carries it, because no search result confirmed any of them. The general *shape* of a
   well-established mechanic — that a Basisrente cannot be surrendered, that contributions are
   deductible, that the annuity is taxed on a cohort percentage — is not tagged, because tagging it
   would drown the signal. **The moment a claim becomes specific and numeric, it is tagged.**
5. **Uncertain numbers became `[std]` parameters, not citations.** Where the mechanic is certain and
   the level is not — a charge, a *Rentenfaktor*, a *Beitragsfreistellung* rate, a market share —
   this file ships a `[std]` value with a stated rationale and an argued plausible range rather than
   a fabricated source tag. A `[std]` number is honest. A guessed `[S4]` number is not.
6. **The weight of the file is in the mechanics.** Sections 1 to 22 below do not depend on having a
   PDF open and are written long and precise; the source blocks are correspondingly short.

**What the re-verification changed.** The network policy was lifted, and on **2026-08-30** the
citations were checked against the primary documents. Library-wide, all fifteen German instruments
delib cites were read as canonical XML from `gesetze-im-internet.de` with each law's amendment
`Stand` recorded, 950 statutory section references were checked and 950 were correct, and insurer
AVB, *Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read;
**501 of the library's 805 source entries, 62 %, now read `Retrieved: yes`.** In this file the pass
reached **21 of the 40 entries below, and those 21 now carry their own `Retrieved:` line: 17 say
yes, three say no with the reason ([S2], [S5], [R7]) and one is mixed ([S14])**. The other nineteen
carry no per-entry line at all, and for those the drafted position above still governs: they were
not opened, then or since. What was read is set out at the head of *Primary sources* and of
*Regulatory and actuarial references*, and item by item in the gaps register.

**What an entry now means.** A **`Retrieved: yes`** line means the document was opened and the
passage the entry rests on was read; the line records the edition, page count or statutory `Stand`
of what was read, and where the document contradicted the drafted text the entry says so. Where
there is a `Retrieved: no` line or no line at all, **the citation is still a pointer, not a
certificate**: an `[R1]` tag on a sentence about § 10 Abs. 1 Nr. 2 Buchst. b EStG means *this is the
instrument this claim must be checked against*, not that anyone read it, and downstream documents
must not upgrade that. **The re-verification also changed things** — it corrected claims the drafted
text got wrong, in the entries themselves and in the register at the foot of this file. Treat a
claim here as sound where its entry says `Retrieved: yes`, and as provisional where it does not.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on:

| Term | Gloss |
|---|---|
| *Basisrente*, *Rürup-Rente*, *Basisrentenvertrag* | The Schicht-1 private pension of § 10 Abs. 1 Nr. 2 Buchst. b EStG. "Rürup" is a market nickname; the statute and the certifying authority say *Basisrentenvertrag* |
| *Schicht 1 / 2 / 3* | The three layers of German retirement provision: basic (GRV, Versorgungswerk, Basisrente); subsidised supplementary (Riester, bAV); unsubsidised private |
| *Alterseinkünftegesetz* (AltEinkG) | The 2004 statute that created the layer architecture, the *nachgelagerte Besteuerung* and the Basisrente |
| *Sonderausgabenabzug* | Deduction of contributions from taxable income as *Sonderausgaben* under § 10 EStG |
| *Höchstbetrag* | The annual ceiling on deductible Schicht-1 contributions, pegged to the maximum contribution to the *knappschaftliche Rentenversicherung* |
| *Beitragsbemessungsgrenze* (BBG) | Contribution assessment ceiling of a social-insurance branch; the *knappschaftliche* BBG is what the *Höchstbetrag* tracks |
| *Besteuerungsanteil* | The percentage of the annuity that is taxable, fixed by the calendar year of *Rentenbeginn* and constant for life |
| *Rentenfreibetrag* | The euro complement of the *Besteuerungsanteil*, frozen in the year after *Rentenbeginn* and never re-indexed |
| *Ertragsanteil* | The much lower taxable fraction applied to Schicht-3 annuities under § 22 EStG — the comparator, not this product's rule |
| *Vererblichkeit*, *Übertragbarkeit*, *Beleihbarkeit*, *Veräußerbarkeit*, *Kapitalisierbarkeit* | The five properties a Basisrente entitlement must **not** have |
| *Hinterbliebenenabsicherung* | Survivor cover; permitted only for the spouse or registered partner and for children while *Kindergeld* runs |
| *Beitragsrückgewähr* | Return of contributions on death; in Schicht 1 it can only fund a survivor's annuity, never a lump sum |
| *Rentengarantiezeit* | Guaranteed payment period after *Rentenbeginn*; in Schicht 1 payable only to permitted survivors |
| *Berufsunfähigkeits-Zusatzversicherung* (BUZ) | Occupational-disability rider written inside the main contract |
| *Berufsunfähigkeit* / *verminderte Erwerbsfähigkeit* | Occupational disability / reduced earning capacity — the two disability risks the statute permits inside a Basisrente |
| *Beitragsfreistellung* | Making the contract paid-up; the Basisrente's only exit |
| *Kündigung* / *Rückkaufswert* | Termination / surrender value — both effectively unavailable on this product |
| *Zuzahlung* / *Einmalbeitrag* | A one-off top-up into an existing contract / a single-premium contract |
| *Rentenbeginn* | Vesting date; the boundary at which the accumulated capital becomes an annuity |
| *Aufschubphase* / *Rentenphase*, *Rentenbezugsphase* | Deferment (accumulation) phase / payout phase |
| *Rentenfaktor* | Monthly annuity per 10 000 € of capital at *Rentenbeginn* |
| *Rechnungszins* / *Höchstrechnungszins* | The technical interest rate the contract is priced and reserved on / its statutory maximum for new business |
| *Überschussbeteiligung* / *Schlussüberschussanteil* | Participation in surplus / terminal bonus |
| *Effektivkosten* | Reduction in yield: the annualised return give-up caused by all charges, disclosed on the *Produktinformationsblatt* |
| *Chancen-Risiko-Klasse* (CRK) | The standardised risk class shown on the *Produktinformationsblatt* |
| *Pfändungsschutz* | Protection from attachment by creditors; § 851c ZPO for this product |
| *Zertifizierung* | Certification of the contract by the *Bundeszentralamt für Steuern* under AltZertG |
| *Produktinformationsblatt* (PIB) | The standardised pre-sale document required for certified contracts |
| *Versorgungsausgleich* | Pension rights sharing on divorce — the one transfer the statute permits |
| *Kleinbetragsrente* | A trivially small annuity; commutable at the start of the payout phase in Schicht 2 **and** in Schicht 1, the latter by the express exception in § 10 Abs. 1 Nr. 2 Satz 3 EStG |

---

## Primary sources

**A retrieval pass was run over this section on 2026-08-30, after the network policy that shaped
the file was lifted.** Each entry now carries its own `Retrieved:` line saying what was opened and
what was not; where an entry still says no, it says why. The blanket status the section opened with
— "egress blocked; no search corroboration" — no longer applies to the entries that were upgraded,
and the per-entry line governs. Where an entry establishes something, it says what and from where;
where it establishes nothing beyond the document's existence and kind, it says that too.

What was opened: **[S1]** two of CosmosDirekt's Basisrente wordings and both of its *Muster*-PIBs;
**[S4]** one Alte Leipziger wording; **[S12]** the GDV's Basisrente and BUZ *Musterbedingungen* and
a *Muster-Standmitteilung*, which the file had recorded as possibly not existing at all; **[S13]**
two carriers' filled-in *Muster-Produktinformationsblätter*; **[S16]** an independent
*Effektivkosten* study; and product pages at **[S2]**, **[S7]** and **[S9]**. What was not: any
*Verbraucherinformation*, any individual PIB, any AVB of the carriers at [S3], [S5], [S6], [S8],
[S10] or [S11], and anything at all from Swiss Life, whose host refuses this environment.

### S1 — Cosmos Lebensversicherungs-AG (CosmosDirekt), *Allgemeine Bedingungen* for the Basisrente — tariffs **LA 1100 A** and **LA 1079 A / LA 936 A / LA 1099 A**
- Publisher: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland
- Doc type: *Allgemeine Versicherungsbedingungen* (AVB) for Basisrente tariffs, in the carrier's
  `LA nnnn A` house numbering
- URL: **established 2026-08-30.** LA 1079 A (*klassisch*) at
  `https://www.cosmosdirekt.de/resource/blob/88924/af678e39611b9b44f5dfb3b0cebb895c/allgemeine-bedingungen-basisrente-la-1079-a--data.pdf`
  and LA 1100 A (*fondsgebunden*) at
  `https://www.cosmosdirekt.de/resource/blob/88926/1c398c12d5d98869dc0f23218bf20bf3/allgemeine-bedingungen-fondsgebundene-basisrente-la-1100-a--data.pdf`,
  under the expected `resource/blob` scheme. Also under it: LA 1080 A (*Hinterbliebenen-Zusatz­
  versicherung*, blob 89028) and the two *Muster*-PIBs (blobs 89376 and 89378). **LA 936 A and
  LA 1099 A were not located**
- Retrieved: **yes** — LA 1079 A and LA 1100 A (PDF, 7 pp. each, both edition (10.15)), read in
  full 2026-08-30, together with the *klassisch* *Muster*-PIB (4 pp., 06.2016)
- Content:
  - **Four tariff codes are attributed to the Basisrente** in the carrier's own numbering —
    **LA 1100 A**, **LA 1079 A**, **LA 936 A**, **LA 1099 A** — against LA 1005 A (Riester),
    LA 1311 A (unit-linked *FlexInvest*), LA 1081 A (*Direktversicherung*) and LA 904 A / LA 1201 A
    / LA 1204 A (Schicht-3 annuity). This is the single most useful structural fact the corpus
    yields about the product's market form: **one direct writer maintains at least four parallel
    Basisrente wordings**, which is what a tariff family looks like when *klassisch*, *fondsgebunden*
    and vintage editions coexist.
  - **Two of the four wordings were located and read**, both edition (10.15), 7 pp. each. LA 936 A
    and LA 1099 A were not found, and the entry no longer asserts that four exist — two do.
  - **Clause content now established from LA 1079 A**: the 50 % rule stated to the customer ("*In
    jedem Fall ist sichergestellt, dass mehr als 50 Prozent der von Ihnen geleisteten Beiträge für
    Ihre Altersversorgung aufgewendet werden*"); tariffs RBA/RBAE without a death benefit beside
    RBH/RBHE with a spouse or registered-partner annuity funded from the *garantiertes
    Deckungskapital*; § 1 Abs. 11 "*Ein Kapitalwahlrecht existiert nicht*"; § 1 Abs. 2's
    *Kleinbetragsrenten-Abfindung*; § 1 Abs. 3's flexible *Rentenbeginn*, forward by up to ten years
    but never before 62 and deferrable once by five; § 2's surplus system (*Zins-* and
    *Grund-Überschussanteil*, a *Bonussumme* in the *Aufschubzeit*, *Schluss-Überschussanteil* and
    *Bewertungsreserven* on the *Bonus-Deckungskapital*, *dynamische Rente* or *Zusatzrente* after
    *Rentenbeginn*); § 7's *Kündigung* that converts to paid-up with no *Rückkaufswert*, the
    single-premium contract that is "*auf Grund der gesetzlichen Restriktionen ... nicht kündbar*",
    and a **free transfer to another § 10 Abs. 1 Nr. 2 b) contract** on three months' notice;
    and § 8's five-year cost spreading and administration-charge shape.
  - **The 0 % conversion basis is wrong for this product and is withdrawn.** It came from the
    carrier's Schicht-3 sibling LA 904 A. The Basisrente wording itself says the guaranteed
    *Rentenfaktor* is computed "*auf Grundlage einer anerkannten Sterbetafel (DAV 2004R) sowie des
    tariflichen Garantiesatzes (Rechnungszins) von **1,25 Prozent p. a.***" — the tariff's own rate,
    which for a 10.15 wording is that year's *Höchstrechnungszins* [R16] [R17] (gap 4).

### S2 — Allianz Lebensversicherungs-AG, **BasisRente KomfortDynamik** — specimen *persönlicher Vorschlag*
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: a distributed specimen quotation ("Berechnung BasisRente KomfortDyn"), hosted by a
  broker rather than by the carrier, dated by its path to **February 2025** `[unverified]`; together
  with the Allianz *Vorsorgekonzept KomfortDynamik* product page
- URL: page `https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/`; the specimen at
  `privat.rh-insuranceservices.com/wp-content/uploads/2025/02/Berechnung-BasisRente-KomfortDyn.pdf`
- Retrieved: no — egress blocked; **no search corroboration in this file (budget exhausted)**;
  identity and the two figures below carried over from
  `_research/klassische_rentenversicherung.md` [S13]
- Content — **the only Basisrente-specific charge evidence in the delib corpus**:
  - The **BasisRente is a variant of the KomfortDynamik chassis**, not a separate product line: the
    same design is sold as PrivatRente (Schicht 3), BasisRente (Schicht 1) and RiesterRente
    (Schicht 2). That is the German market's normal arrangement and it is worth stating plainly —
    **the layer is a wrapper around a common chassis**, and an insurer's Basisrente shares its
    fund range, its guarantee mechanics and its *Rentenfaktor* machinery with its Schicht-3 sibling.
  - The chassis: premiums **split between the Allianz *Sicherungsvermögen* and a *Spezialfonds***;
    selectable guarantee levels of **60 %, 80 % or 90 % of premiums paid** at *Rentenbeginn*, 80 %
    standard `[unverified]`; at inception the customer is given only the premium-retention level and
    a **minimum annuity** — a *garantierter Rentenfaktor* expressed as an amount.
  - Two charge figures were returned by third-party commentary in the same result set: an
    **Abschlussprovision of 1 575 €** on the specimen quotation, and, **in the BasisRente and
    RiesterRente variants, total costs relative to the capital formed of at most 0,95 € per 100 €**
    `[unverified]`. Both come from third-party analyses rather than an Allianz tariff sheet. The
    second is the more useful: expressed as a reduction-in-yield-like ratio it is of the order of
    **0,95 %** of the capital formed, which is consistent with the *Effektivkosten* band a
    *Produktinformationsblatt* would show for a hybrid Basisrente [S13], and it is the only number
    in this file that behaves like a charge level rather than a guess.

### S3 — Allianz Lebensversicherungs-AG, the **BasisRente** product family
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: AVB, *Produktinformationsblätter* and *Verbraucherinformationen* for the carrier's
  Basisrente tariffs — marketed as **BasisRente Klassik**, **BasisRente Perspektive** (the
  "Neue Klassik" design) and **BasisRente InvestFlex** (unit-linked) `[unverified]` as to the exact
  current line-up
- URL: not established
- Content: **nothing established beyond the family's existence.** Named because Allianz is the
  largest German life writer, so its Basisrente wordings are the most consequential documents this
  file could not reach. Any downstream statement about them must be sourced to [S2] or dropped.

### S4 — Alte Leipziger Lebensversicherung a. G., **AL_RoyalBasisRente** (Klassik and Fonds)
- Publisher: Alte Leipziger Lebensversicherung a. G., Oberursel
- Doc type: AVB, *Produktinformationsblatt*, *Verbraucherinformation*
- URL: not established
- Content: **nothing established beyond existence.** Alte Leipziger is repeatedly placed at the top
  of independent Basisrente ratings [R24] and is the natural first target for a checker with a
  working network. Product names are `[unverified]`.

### S5 — NÜRNBERGER Lebensversicherung AG, **Basis-Rente** with **Berufsunfähigkeits-Zusatzversicherung**
- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: AVB for the Basisrente main contract and separate AVB for the BUZ rider
- URL: not established. The carrier's Schicht-3 wordings were returned in a sibling delib file under
  `https://www.nuernberger.de/medien/4allportal/gn331451_p.pdf` and siblings `gn331530_p`,
  `gn331303_p`, so its Basisrente wordings sit in the same `4allportal` document scheme; **no
  Basisrente document id was returned and none is guessed**
- Retrieved: no — egress blocked; no search corroboration; the `4allportal` scheme carried over from
  `_research/klassische_rentenversicherung.md` [S9]
- Content: **nothing established beyond existence and the document scheme.** Named because
  NÜRNBERGER is one of the German market's principal *Berufsunfähigkeit* writers and therefore the
  natural place to look for a **BUZ written inside a Basisrente** and for the 50 % *Beitragsanteil*
  constraint expressed in contractual terms (mechanic 13). That wording is the single most valuable
  document this file could not reach.

### S6 — Volkswohl Bund Lebensversicherung a. G., **Basisrente**
- Publisher: Volkswohl Bund Lebensversicherung a. G., Dortmund
- Doc type: AVB, *Produktinformationsblatt*
- URL: not established
- Content: **nothing established beyond existence.** A broker-channel carrier with a large
  Basisrente book [R24]; the broker channel is where this product is sold (mechanic 21).

### S7 — LV 1871 (Lebensversicherung von 1871 a. G.), Basisrente
- Publisher: Lebensversicherung von 1871 a. G., München
- Doc type: AVB, *Produktinformationsblatt*. Marketed under the names **Golden Basic** and
  **MeinPlan Basis** `[unverified]`
- URL: not established
- Content: **nothing established beyond existence.** Named because LV 1871's Basisrente is the
  market's best-known example of a **fondsgebundene Basisrente with an open fund and ETF universe
  and no *Beitragsgarantie*** `[unverified]` — the form mechanic 9 argues is the commercial default
  of the modern Schicht-1 market, and therefore the form a checker should verify first.

### S8 — Swiss Life Deutschland, Basisrente (**Swiss Life Maximo** family)
- Publisher: Swiss Life AG, Niederlassung für Deutschland
- Doc type: AVB, *Produktinformationsblatt*
- URL: not established
- Content: **nothing established beyond existence.** A large broker-channel Schicht-1 writer whose
  *Maximo* line is a hybrid with a selectable guarantee level — the third asset form of mechanic 9.
  Product name `[unverified]`.

### S9 — Continentale Lebensversicherung AG, Basisrente (**Rente Invest Basis** family)
- Publisher: Continentale Lebensversicherung AG, Dortmund
- Doc type: AVB, *Produktinformationsblatt*
- URL: not established
- Content: **nothing established beyond existence.** Product name `[unverified]`.

### S10 — Stuttgarter Lebensversicherung a. G., Basisrente
- Publisher: Stuttgarter Lebensversicherung a. G.
- Doc type: AVB, *Produktinformationsblatt*. Marketed in *performance-safe* and *index-safe*
  variants `[unverified]`
- URL: not established
- Content: **nothing established beyond existence.** If the *index-safe* name is right it would be
  an **index-linked Basisrente** — a fourth asset form beyond the three of mechanic 9 and a bridge
  to delib product 4 (`indexpolice`). That this could not be checked is gap 12.

### S11 — The carriers for which nothing whatever was established
- Publishers: **Debeka**, **R+V**, **HDI**, **Gothaer**, **Zurich Deutscher Herold**, **ERGO**,
  **AXA**, **Generali / Dialog**, **Barmenia**, **Universa**, **Württembergische**,
  **Signal Iduna**, **Baloise**, **DEVK**, **Provinzial**, **HUK-Coburg**, **Hannoversche**,
  **CosmosDirekt** (beyond [S1]), **die Bayerische**, **Condor**
- Doc type: each of these carriers writes, or has written, a Basisrente and therefore publishes AVB,
  a *Produktinformationsblatt* and a *Verbraucherinformation* for it
- URL: not established for any of them
- Content: **nothing.** This entry exists so that the corpus's coverage is stated as a fact rather
  than implied by omission: **twenty named German life writers whose Basisrente documents exist were
  not reached, and not one of them contributes a single fact to this file.** Naming them without
  attaching claims is the honest form. See gap 1.

### S12 — GDV, *Musterbedingungen* service index
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV)
- Doc type: the association's index of model conditions
- URL: `https://www.gdv.de/gdv/service/musterbedingungen`, from which four Basisrente documents
  resolve under `gdv.de/resource/blob/…`: the Basisrente AVB (blob 6292), the BUZ zur Basisrente
  (blob 6330), the Hinterbliebenenrenten-Zusatzversicherung zur Basisrente (blob 6338) and the
  *Muster-Standmitteilungen* for a *Basisrentenversicherung (klassisch)* (blob 6314) and *(mit BUZ)*
  (blob 6310)
- Retrieved: **yes** — the index (HTML, ~94 kB), the Basisrente AVB (PDF, 18 pp., **Stand:
  21.07.2025**), the BUZ AVB (PDF, 11 pp., **Stand: 15.11.2022**) and the *klassisch*
  *Muster-Standmitteilung* (PDF, 8 pp.), all read 2026-08-30
- Content: **gap 5 is closed, and in the affirmative.** The GDV does publish a Basisrente model
  condition set, titled *Allgemeine Bedingungen für die Rentenversicherung gemäß § 10 Absatz 1
  Nr. 2 Buchstabe b Doppelbuchstabe aa EStG (Basisrente-Alter)*, and a matching BUZ set. Between
  them they supply: the payout shape and the 62 floor (§ 1 Abs. 1); the combination of **up to
  twelve monthly annuities into one payment** below an agreed amount (§ 1 Abs. 2); the
  *Kleinbetragsrente* commutation as the **insurer's** right — "*Wir sind allerdings berechtigt*" —
  at a threshold the July 2025 text still gives as **1 %** of the monthly *Bezugsgröße* (§ 1
  Abs. 3); "*Bei Ihrem Tod erbringen wir keine Leistung, und der Vertrag endet*" as the base design
  (§ 1 Abs. 5); a *Kündigung*, whole or partial, that converts to paid-up and pays no
  *Rückkaufswert*, with a single-premium contract simply continuing (§ 9); the paid-up benefit
  computed on a **five-year spreading of acquisition and distribution costs**, or the premium term
  if shorter (§ 10 Abs. 1); the closed charge menu of AltZertG § 2a with the DeckRV § 4
  *Verrechnungsverfahren* capped at "*2,5 % der ... zu zahlenden Beiträge*" (§ 11); the annual
  information field list (§ 14); and, in the BUZ set, **"*Die Zusatzversicherung ist so gestaltet,
  dass stets mehr als 50 % der Beiträge auf Ihre Hauptversicherung entfallen*"** (§ 9 Abs. 2), which
  is gap 18's missing document. Two things about GDV model conditions still matter for weighting:
  they are expressly **unverbindlich** and their use is **optional**, so a GDV-tagged fact is
  evidence about a market template and weaker evidence about any particular carrier.

### S13 — *Produktinformationsblatt* under § 7 AltZertG (the standardised PIB)
- Publisher: each provider, on a form and a computational method prescribed by law and administered
  by the **Produktinformationsstelle Altersvorsorge gGmbH (PIA)**, Kaiserslautern
- Doc type: the mandatory two-page pre-sale document for a certified Basisrentenvertrag
- URL: the *individual* PIB is quotation-specific and never public, but § 7 Abs. 4 AltZertG
  requires a ***Muster*-PIB** for assumed terms of **12, 20, 30 and 40 years** on each provider's own
  site. Two were retrieved: NÜRNBERGER `https://www.nuernberger.de/medien/4allportal/lv052_030_p.pdf`
  and WWK
  `https://www.wwk.de/medien/dokumente/produktinformationsblaetter/basisrente-invest-protect-50/fvg22_eb_lz20_50bg.pdf`
- Retrieved: **yes, two *Muster*-PIBs** (NÜRNBERGER, 2 pp., certification number 006590, Stand
  01.01.2025; WWK, 2 pp., certification number 006421, Stand 03.01.2024), read 2026-08-30. **No
  individual PIB was obtained and none can be**
- Content — **gap 2 and gap 7 are both closed.** The individual PIB is quotation-specific; the
  *Muster*-PIB is the same form on stylised data. The **CRK scale is 1 to 5**; the *Effektivkosten*
  are the reduction in yield in percentage points against a reference gross return fixed by the CRK
  (2 / 3 / 4 / 5 / 6 % for CRK 1–5), and the benefit scenarios run on four returns per CRK (for
  CRK 4: −1 %, 2 %, 5 % and 6 %) — AltvPIBV §§ 5, 8 and 10 [R11].
  **The NÜRNBERGER sheet is the corpus's first quantified Basisrente.** *Musterkunde* born 1988,
  30 years to 67, 100 € a month, 36 000 € paid, CRK 4. ***Effektivkosten* 1,77 percentage points**
  (5,00 % → 3,23 %). *Garantiertes Kapital für Verrentung* 18 000,00 €; **garantierte monatliche
  Altersleistung 44,89 €** at a **guaranteed *Rentenfaktor* of 24,94 € per 10 000 €** — the first
  *Rentenfaktor* level anywhere in this corpus, which is gap 4. Charges: *Abschluss- und
  Vertriebskosten* **900,00 € = 2,50 % der vereinbarten Beiträge** and 2,50 % per *Zuzahlung*;
  *Verwaltungskosten* **7,00 % der eingezahlten Beiträge**, up to **3,80 % p.a. of the fund**
  (fund charges included; current burden 1,10 %), **1,50 % of the annuity p.a.** in the payout
  phase; *Versorgungsausgleich* up to 500,00 €; "*Ein Anbieterwechsel ist bei diesem Produkt
  ausgeschlossen*". The WWK sheet — 20 years, single premium, 50 % *Beitragsgarantie*, CRK 4 —
  gives *Effektivkosten* of **4,95 percentage points** and likewise excludes an *Anbieterwechsel*.
  **Read a *Muster*-PIB figure as a ceiling**: it is computed on maximum permitted charges, and the
  study at [S16] puts realistic figures for the same product class at 1 – 1,5 pp.

### S14 — *Basisinformationsblatt* (PRIIP key information document)
- Publisher: each provider
- Doc type: the PRIIPs KID for an insurance-based investment product
- URL: not established **for a Basisrente**. A carrier's *Basisinformationsblatt* index was reached
  (`https://www.lv1871.de/service/kundenservice/basisinformationsblaetter/`) and one KID was
  retrieved in full — NÜRNBERGER `https://www.nuernberger.de/medien/4allportal/gn339322_p.pdf`,
  tariff NR3361DV, Stand 01.01.2026 — but **that document is a Schicht-3 contract with a
  *Kapitalwahlrecht*, not a Basisrente**
- Retrieved: **one specimen of the document type, yes; none for a Basisrente, no**
- Content: the retrieved specimen establishes the form — purpose statement, product type,
  recommended holding period, a **summary risk indicator on a scale of 1 to 7**, performance
  scenarios and a cost table. **Gap 6 is narrowed, not closed.** § 7 Abs. 2 AltZertG establishes
  that the individual PIB "*ersetzt das Informationsblatt zu Versicherungsprodukten nach § 4 der
  VVG-Informationspflichtenverordnung*" and that **no § 154 VVG *Modellrechnung* is to be performed
  or attached** for a certified contract [R11] — so it displaces at least one neighbouring
  disclosure. Whether it also displaces the PRIIPs KID is **still not established**: no Basisrente
  KID was found at any carrier, which is consistent with the product sitting outside PRIIPs but does
  not prove it. Nothing downstream may assert either arrangement.

### S15 — Annual statement to the policyholder (*jährliche Information*, § 7a AltZertG)
- Publisher: each provider
- Doc type: the statutory annual information for a certified contract
- URL: the statute itself, `https://www.gesetze-im-internet.de/altzertg/__7a.html`; the GDV
  *Muster-Standmitteilung* for a *Basisrentenversicherung (klassisch)* at [S12]
- Retrieved: **yes** — § 7a AltZertG as canonical XML (Stand: zuletzt geändert durch Art. 5 G v.
  25.10.2023 I Nr. 294) and the GDV *Muster-Standmitteilung* (PDF, 8 pp.), read 2026-08-30. **The
  paragraph address § 7a is correct**
- Content: **the field list is established and is the statute's own.** § 7a Abs. 1 requires annual
  information on (1) the use made of the contributions paid, (2) the amount of capital built up,
  (3) the actual costs incurred in the past contribution year, (4) the investment return earned and
  (5), until the payout phase begins, the capital expected at its start after costs — projected on
  the contributions actually paid and the *Wertentwicklungen* of the individual PIB — plus a
  statement on ethical, social and environmental considerations. The GDV model conditions restate it
  at § 14 and add that the capital figure is a *Gesamtkapital* including allocated surplus,
  non-guaranteed *Schlussüberschüsse* and the non-guaranteed *Bewertungsreserven*-share. That is the
  same state-variable list `result_pols()` publishes.

### S16 — Consumer, comparison and rating material
- Publishers: **Finanztip**, **Stiftung Warentest / Finanztest**, the **Verbraucherzentralen**,
  **Verivox**, **CHECK24**, **Handelsblatt**, and the rating houses at [R24]
- Doc type: consumer guides, comparison-portal pages, product ratings — **secondary in every case**,
  and in frlib's convention they would still be S-numbered because they describe the product rather
  than regulate it
- URL: not established for any of them
- Content: **nothing established.** These are the sources that in a normal research session would
  supply price points, market variation and the buyer profile. **None was reached.** Every price
  point, every market share and every buyer-profile statement in this file is therefore either
  general knowledge marked `[unverified]` or a `[std]` construction, and is marked as such at the
  point of use.

---

## Regulatory and actuarial references

**Retrieval pass, 2026-08-30.** Every German statute and regulation in this section was retrieved as
canonical XML from gesetze-im-internet with the law's *Stand* attached and read at the section the
entry relies on — EStG §§ 10, 22 and 93; AltZertG §§ 1, 2, 2a, 5a, 7 and 7a with the AltvPIBV; VVG
§§ 153, 165, 168 and 169; ZPO §§ 851c and 851d; DeckRV §§ 2 and 4; and the
*Sozialversicherungsrechengrößen-Verordnungen* for 2025 and 2026. The consolidated BMF-Schreiben
[R18] and one of the 2021 BFH judgments [R19] were also retrieved. **Two cautions.** The per-section
HTML page `gesetze-im-internet.de/<law>/__NNN.html` is a ~5 kB frameset shell carrying **no
statutory text**; it is kept below as the human-facing link and is not what was read. And the entries
that are **not** consolidated instruments — the amending acts at [R5]–[R8], the BaFin material at
[R21] and the statistics at [R22] — were **not** retrieved and say so individually. Where a figure
is still `[unverified]` the entry now says why.

### R1 — EStG § 10 Abs. 1 Nr. 2 Buchst. b — the definition of a Basisrentenvertrag
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` — canonical form, `[unverified]`
- Retrieved: **yes** (canonical XML, Stand: neugefasst durch Bek. v. 8.10.2009 I 3366, 3862, zuletzt
  geändert durch Art. 7 G v. 29.6.2026 I Nr. 197; § 10 read in full 2026-08-30). The five prohibitions
  are Satz 2 verbatim — "*Die Ansprüche nach Buchstabe b dürfen nicht vererblich, nicht übertragbar,
  nicht beleihbar, nicht veräußerbar und nicht kapitalisierbar sein.*" — the payout shape and the 62
  floor are Doppelbuchst. aa, and **the 60/62 split is § 10 Abs. 6**, so both floors and their boundary
  date are confirmed. Satz 3 carries the twelve-payment combination and the *Kleinbetragsrente*
  commutation; Satz 5 shuts the door on any other payout form. **Correction: the 50 % majority test is
  not in this section** — the statute requires only that a supplementary cover be *ergänzend*, and the
  50 % test is administrative, at [R18] Rz. 38
- Content — **the single most important instrument for this product, and the source of every
  constraint in it**:
  - The provision makes deductible, as *Sonderausgaben*, the taxpayer's own contributions **to
    build a funded old-age provision of the taxpayer's own**, where the contract provides for the
    payment of a **monthly, lifelong annuity on the life of the taxpayer**, not commencing before
    the completion of a stated year of life; and, as permitted supplements, cover against
    **Berufsunfähigkeit**, against **verminderte Erwerbsfähigkeit**, and for **Hinterbliebene**.
  - The **age floor is the completion of the 62nd year of life**, applying to contracts concluded
    **after 31 December 2011**; contracts concluded on or before that date retain the earlier floor
    of the **completion of the 60th year of life** [R8]. `[unverified]` as to both the paragraph
    address and the transition date, but the substance — 62 now, 60 for the older cohort — is a
    settled point of German practice. **It is not 63; see gap 22, which records a contrary
    statement in this file's own commissioning brief and resolves it against 60.**
  - **The five prohibitions.** The entitlements arising under the contract must be **nicht
    vererblich** (not inheritable), **nicht übertragbar** (not transferable), **nicht beleihbar**
    (not chargeable as security or borrowable against), **nicht veräußerbar** (not saleable) and
    **nicht kapitalisierbar** (not convertible into capital). This five-limb sentence is the
    definition of the product. Each limb has a direct modelling consequence and they are worked
    through one at a time in mechanic 3.
  - The permitted *Hinterbliebenenabsicherung* is confined to the **spouse or registered partner**
    and to **children for so long as the taxpayer is entitled to *Kindergeld* or to the
    *Kinderfreibetrag*** in respect of them. No other beneficiary may be named — not a cohabiting
    partner, not a sibling, not an estate. `[unverified]` as to the statutory address; settled as
    substance.
  - The supplementary covers are subject to a **majority test**: the contributions are deductible
    under this provision only if **more than 50 % of the total contribution is attributable to the
    old-age provision**, i.e. the disability and survivor components together must stay **below
    50 %**. `[unverified]` as to whether the test sits in § 10 itself or in the administrative
    guidance at [R18]; the 50 % level itself is settled market practice and is the constraint
    mechanic 13 is built on.

### R2 — EStG § 10 Abs. 3 — the Höchstbetrag, its peg, and the reductions for employees
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` — canonical form, `[unverified]`
- Retrieved: **yes** (canonical XML, same *Stand* as [R1]; § 10 Abs. 3 read 2026-08-30). Satz 1 and 2
  verbatim: "*Vorsorgeaufwendungen nach Absatz 1 Nummer 2 sind bis zu dem Höchstbeitrag zur
  knappschaftlichen Rentenversicherung, aufgerundet auf einen vollen Betrag in Euro, zu berücksichtigen.
  Bei zusammenveranlagten Ehegatten verdoppelt sich der Höchstbetrag.*" — which confirms the peg, the
  doubling **and** the rounding convention the *Höchstbetrag* series depends on. The employee reductions
  are Satz 3, the tax-free employer share is Satz 5, and the phase-in is Sätze 4 and 6
- Content:
  - Contributions under § 10 Abs. 1 Nr. 2 — **letters a and b together**, i.e. statutory pension,
    *Versorgungswerk*, *Alterskasse* **and** Basisrente — are deductible up to a **single annual
    *Höchstbetrag***, doubled for spouses assessed jointly.
  - **The ceiling is not a fixed euro figure.** Since 2015 it tracks the **maximum annual
    contribution to the *knappschaftliche Rentenversicherung*** — the miners' branch, which has both
    a higher *Beitragsbemessungsgrenze* and a higher contribution rate than the general branch. The
    ceiling therefore moves every year with the *Sozialversicherungsrechengrößen-Verordnung* [R20],
    which is what makes a Basisrente premium a **naturally indexed** stream (mechanic 7).
  - The arithmetic is `Höchstbetrag = BBG_knappschaftlich(year) × Beitragssatz_knappschaftlich(year)`,
    rounded. The inputs and results are tabulated in mechanic 6; every figure there is
    `[unverified]`.
  - **The deductible percentage.** From 2005 the deductible share of the (capped) contributions rose
    from 60 % by two percentage points a year, and was scheduled to reach 100 % in 2025. The
    **Jahressteuergesetz 2022 brought the 100 % forward to the assessment period 2023** [R7], so
    **for 2023 onwards the capped contribution is deductible in full**. `[unverified]` as to the
    instrument; settled as substance.
  - **The employee reductions, which are what make this a self-employed product.** Two distinct
    mechanisms operate and they must not be conflated:
    1. **Consumption of the ceiling.** An employee's own *and* employer's contributions to the
       *gesetzliche Rentenversicherung* count **against the same ceiling**. A Basisrente contribution
       is deductible only inside whatever headroom is left.
    2. **Subtraction of the tax-free employer share.** The employer's contribution to the GRV is
       already tax-free in the employee's hands, so it is **deducted from the resulting deductible
       amount** rather than being relieved twice. `[unverified]` as to the paragraph; the
       double-mechanism structure is settled.
  - **A third reduction applies to taxpayers with a non-contributory pension entitlement** —
    *Beamte*, judges, soldiers, and controlling shareholder-directors with a *Pensionszusage*. For
    them the ceiling is reduced by a **notional total contribution** to the general statutory scheme
    computed on their remuneration up to the general BBG. `[unverified]` as to the address; settled
    as substance, and it is why a *Beamter* has very little Basisrente headroom.

### R3 — EStG § 10 Abs. 2 and Abs. 2a — certification and data transmission as conditions of relief
- Publisher: Bundesministerium der Justiz / juris
- URL: not established
- Content: the *Sonderausgabenabzug* for a Basisrente is conditional on the contract being
  **certified under the AltZertG** [R9] and on the provider **transmitting the contribution data
  electronically** to the tax administration, which requires the taxpayer's consent. Two
  consequences: an uncertified contract, however economically identical, gets **no relief at all**;
  and the *Zertifizierungsnummer* printed on the *Versicherungsschein* is the operative link between
  the contract and the deduction. `[unverified]` as to the paragraph addresses.

### R4 — EStG § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. aa — the Besteuerungsanteil
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` — canonical form, `[unverified]`
- Retrieved: **yes** (canonical XML, same *Stand* as [R1]; § 22 Nr. 1 Satz 3 Buchst. a read in full,
  including the statutory cohort table, 2026-08-30). **Every percentage in the delib schedule matches
  the statute**: 2020 80,0; 2021 81,0; 2022 82,0; 2023 82,5; 2024 83,0; 2025 83,5; 2026 84,0; 2040
  91,0; 2058 100,0. The *Rentenfreibetrag* is Sätze 4–7, and Satz 7 is the one that matters for the
  payout-phase surplus system: "*Regelmäßige Anpassungen des Jahresbetrags der Rente führen nicht zu
  einer Neuberechnung und bleiben bei einer Neuberechnung außer Betracht*"
- Content — **the payout-side rule, and the second defining feature of the layer**:
  - Annuities and other benefits from a Basisrentenvertrag, and from the statutory scheme and the
    *Versorgungswerke*, are *sonstige Einkünfte* taxed on a ***Besteuerungsanteil*** — a percentage
    of the annuity fixed by the **calendar year in which the annuity begins**, not by the taxpayer's
    age, income or contribution history. This is the *Kohortenprinzip*.
  - **The complement is frozen in euro.** The untaxed part is computed once, in the **first full
    calendar year of receipt**, as a euro amount — the ***Rentenfreibetrag*** — and then stays at
    that euro amount for life. Every later increase in the annuity is therefore **fully taxable**.
    This is the mechanic most often got wrong and it matters for delib: the model's tax overlay, if
    it ever has one, must freeze an amount, not a percentage.
  - The cohort schedule and its 2058 endpoint are set out in mechanic 15. The schedule's construction
    — 50 % for 2005, rising two points a year to 80 % for 2020, then one point a year, then **half a
    point a year from 2023** after the amendment at [R6] — is settled as substance; **every
    individual percentage in the table is `[unverified]`**.
  - The same provision catches a **Berufsunfähigkeitsrente paid out of a Basisrentenvertrag**, which
    is why a BUZ inside a Basisrente is taxed far more heavily than a standalone *selbständige
    Berufsunfähigkeitsversicherung* (mechanic 13). `[unverified]`, and gap 16.

### R5 — Alterseinkünftegesetz (AltEinkG), 2004
- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established. **No Bundesgesetzblatt citation is given, because none could be confirmed.**
- Content: the enabling statute. It responded to the *Bundesverfassungsgericht*'s 2002 decision that
  the unequal taxation of *Beamtenpensionen* and statutory pensions was unconstitutional
  `[unverified]` as to the year and the case, and it did three things at once: it introduced
  ***nachgelagerte Besteuerung*** for the first layer, it built the three-layer architecture, and it
  created the **Basisrente** as the private, funded member of the first layer, so that the
  self-employed — who have no access to the statutory scheme — would have a vehicle with the same
  tax treatment. **Effective 1 January 2005**, which is the boundary that divides the German life
  book into two tax cohorts for every product in delib. The commission whose report it followed was
  chaired by **Bert Rürup**, from which the market name.

### R6 — Wachstumschancengesetz (2024) — the half-point step and the move of the 100 % year to 2058
- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established
- Content: the amendment that **reduced the annual increase in the *Besteuerungsanteil* from one
  percentage point to half a percentage point**, with effect from the cohort year **2023**, and
  thereby moved the year in which the *Besteuerungsanteil* first reaches **100 %** from **2040 to
  2058**. It was enacted in **2024** and applied **retrospectively to the 2023 cohort**, which is
  the reason the 2023 figure is **82,5 %** rather than the 83 % the original schedule would have
  given. `[unverified]` as to the instrument's name and date; the substance — the half-point step,
  the retrospective 2023 start and the 2058 endpoint — is settled and is corroborated by simple
  arithmetic on the schedule itself (mechanic 15).
- The motive matters for delib's framing: the change, together with [R7], was the legislator's
  response to the *Doppelbesteuerung* litigation at [R19]. It is a **slowing of the transition, not
  a change of principle**: full *nachgelagerte Besteuerung* is still the destination.

### R7 — Jahressteuergesetz 2022 — the full Sonderausgabenabzug from 2023
- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established
- Retrieved: **no** as to the amending act; **its effect was read in § 10 Abs. 3 EStG** on
  2026-08-30 — Satz 4 sets 2013 at 76 %, and Satz 6 reads "*Der Prozentsatz in Satz 4 erhöht sich in
  den folgenden Kalenderjahren bis zum Kalenderjahr 2022 um je 2 Prozentpunkte je Kalenderjahr; ab
  dem Kalenderjahr 2023 beträgt er 100 Prozent*"
- Content: brought forward the **100 % deductibility of Schicht-1 contributions** from the scheduled
  2025 to the assessment period **2023**, two years early. **Correction:** this entry read "94 % in
  2021 and 96 % in 2022"; on the statutory schedule the shares are **92 % in 2021 and 94 % in 2022**
  (76 % in 2013 plus two points a year). The old pair was the original schedule's 2023 and 2024
  values shifted two years. Same motive as [R6]: closing the double-taxation
  gap from the contribution side. **For any delib model point written at 2023 or later, the
  deductible share is 100 % of the capped contribution and no phase-in factor is needed** — which
  is a genuine simplification of the product-spec's tax section relative to how it would have had
  to be written five years earlier.

### R8 — Jahressteuergesetz 2007 — the age floor from 60 to 62
- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established
- Content: raised the earliest permitted *Rentenbeginn* for a Basisrentenvertrag from the completion
  of the **60th** to the completion of the **62nd** year of life, **for contracts concluded after
  31 December 2011**. The same amendment made the parallel change to the § 20 EStG "12/62" rule for
  Schicht-3 capital payments, which is why 62 appears in two unrelated places in German life tax law.
  `[unverified]` as to the instrument and its year; the **60/62 split at the end of 2011** is settled
  and is the answer to the question the commissioning brief put (gap 22).

### R9 — AltZertG § 5a — certification of Basisrentenverträge
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/altzertg/__5a.html` — canonical form, `[unverified]`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I Nr. 294;
  §§ 5a, 2 and 2a read 2026-08-30). § 5a in full: "*Die Zertifizierungsstelle erteilt die Zertifizierung
  nach § 2 Abs. 3, wenn ihr die nach diesem Gesetz erforderlichen Angaben und Unterlagen vorliegen sowie
  die Vertragsbedingungen des Basisrentenvertrags dem § 2 Absatz 1 oder Absatz 1a sowie dem § 2a
  entsprechen und der Anbieter den Anforderungen des § 2 Absatz 2 entspricht.*" **So the imported
  conditions are § 2 Abs. 1/1a and § 2a only**, and the Riester *Beitragserhaltungsgarantie* of § 1
  Abs. 1 Satz 1 Nr. 3 is demonstrably not among them. **The 1 January 2010 start date is not in the
  retrieved text and stays `[unverified]`**
- Content:
  - **§ 5a is the Basisrente's certification provision.** The *Altersvorsorgeverträge-
    Zertifizierungsgesetz* was written for Riester; § 5a was inserted later to bring Basisrenten-
    verträge into the same certification machinery, with effect for contracts concluded from
    **1 January 2010** `[unverified]` as to that date.
  - The certifying authority is the **Bundeszentralamt für Steuern (BZSt)**. Certification is a
    **formal conformity check** — does the contract meet the § 10 Abs. 1 Nr. 2 Buchst. b conditions
    and the AltZertG's own information requirements — and each certified tariff receives a
    *Zertifizierungsnummer*.
  - **What § 5a does not import from § 1 is as important as what it does.** The Riester
    requirements at [R10] — above all the **guarantee that at least the nominal contributions and
    *Zulagen* are available at the start of the payout phase** — **do not apply to a
    Basisrentenvertrag**. That single omission is why a Basisrente may be sold as a pure unit-linked
    contract with no guarantee at all, and it is the most consequential structural difference
    between the two subsidised layers (mechanic 9). `[unverified]` as to the drafting mechanism;
    settled as substance and universally relied on by the market.

### R10 — AltZertG § 1 and § 2 Abs. 2 — what certification is, and the Riester guarantee it does not extend
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/altzertg/__1.html` — canonical form, `[unverified]`
- Retrieved: **yes** (canonical XML, same *Stand* as [R9]; §§ 1, 2 and 2a read 2026-08-30). The
  *Beitragserhaltungsgarantie* is **§ 1 Abs. 1 Satz 1 Nr. 3** and the five-year cost spreading is
  **§ 1 Abs. 1 Satz 1 Nr. 8** — "*die vorsieht, dass die angesetzten Abschluss- und Vertriebskosten
  gleichmäßig mindestens auf die ersten fünf Vertragsjahre verteilt werden*" — both in the
  *Altersvorsorgevertrag* definition, and **§ 5a reaches neither**. § 2a is the closed charge menu that
  a Basisrentenvertrag may use. Note that the entry's heading is imprecise: what certification *is* is
  defined in **§ 2 Abs. 3**, not § 2 Abs. 2, which is the list of permitted providers
- Content:
  - § 1 lists the conditions a **Riester** *Altersvorsorgevertrag* must satisfy, including the
    **Beitragserhaltungsgarantie** (nominal preservation of contributions and *Zulagen* at the start
    of the payout phase), a payout phase in the form of a lifelong annuity or an instalment plan with
    a subsequent annuity, an **earliest payout age**, and the **spreading of acquisition and
    distribution costs over at least five years** `[unverified]` as to which of these § 5a picks up
    for the Basisrente — and gap 8 records that the five-year spreading question was not resolved.
  - § 2 Abs. 2, or a provision to that effect, states expressly that **certification is not a seal of
    quality**: it says nothing about the economic soundness of the product, the level of its charges,
    or the financial standing of the provider. Downstream documents must repeat that; a
    *Zertifizierungsnummer* on a *Versicherungsschein* is a tax fact, not a value judgement.

### R11 — AltZertG § 7 and the *Produktinformationsstelle Altersvorsorge*
- Publisher: Bundesministerium der Justiz / juris; Produktinformationsstelle Altersvorsorge gGmbH
  (PIA), Kaiserslautern
- URL: `https://www.gesetze-im-internet.de/altzertg/__7.html` — canonical form, `[unverified]`
- Retrieved: **yes** — § 7 and § 7a AltZertG (canonical XML, same *Stand* as [R9]) and the implementing
  **AltvPIBV** (`https://www.gesetze-im-internet.de/altvpibv/BJNR141300015.html`), read 2026-08-30.
  § 7 Abs. 1 lists fifteen mandatory PIB fields; § 7 Abs. 4 requires a ***Muster*-PIB at 12, 20, 30 and
  40 years** published on the provider's own site; § 7 Abs. 2 adds that the PIB replaces the VVG-InfoV
  sheet and that **no § 154 VVG *Modellrechnung* is to be performed or attached**. AltvPIBV § 5 puts the
  contract in **CRK 1 to 5**; § 8 Nr. 3 defines the *Effektivkosten*; § 10 fixes the reference returns —
  2/3/4/5/6 % by CRK for the *Effektivkosten*, and four scenarios per CRK for the projections
- Content: the pre-sale information regime for certified contracts. It requires the provider to hand
  over a **standardised *Produktinformationsblatt*** before conclusion [S13], on a common form, so
  that products can be compared across providers and across product types. The **PIA** computes and
  maintains the two standardised comparators — the ***Chancen-Risiko-Klasse*** and the projection
  methodology behind the scenarios — using a common capital-market model, and the provider computes
  the ***Effektivkosten***. **The current statutory field list, the number of risk classes and the
  scenario set were not established** and are gap 7. What is settled and load-bearing for delib is
  that a comparable total-charge figure for this product **exists and is public per quotation**, and
  that delib could not obtain one.

### R12 — ZPO § 851c — Pfändungsschutz bei Altersrenten
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/zpo/__851c.html` — canonical form, `[unverified]`
- Retrieved: **yes** (canonical XML, Stand: neugefasst durch Bek. v. 5.12.2005 I 3202, zuletzt geändert
  Art. 2 G v. 22.12.2025 I Nr. 349; §§ 851c and 851d read 2026-08-30). Abs. 1's four conditions are
  confirmed verbatim, including "*nicht vor Vollendung des 60. Lebensjahres*". **Abs. 2 now yields the
  amounts this file declined to print**: **6 000 €** a year to the completed 27th year of life and
  **7 000 €** to the completed 67th, an aggregate ceiling of **340 000 €**, three tenths of any excess
  *Rückkaufswert* protected on top, and a five-yearly re-set on 1 July — which is why the practitioner
  ladders contradicted each other (gap 9, closed)
- Content — **the third leg of the product, alongside the tax relief and the prohibitions**:
  - The provision gives **attachment protection to private pension entitlements** that satisfy a
    set of conditions closely modelled on the § 10 EStG definition: the benefit must be payable
    **periodically and for life**, not before a stated age or on the occurrence of disability; the
    entitlement must **not be disposable**; **third parties may not be named as beneficiaries other
    than survivors**; and **no capital payment other than a death benefit may be agreed**. A
    compliant contract's **income stream is then attachable only on the scale that applies to
    earnings**, i.e. with the *Pfändungsfreigrenzen*.
  - **The age condition in § 851c is the completion of the 60th year of life**, not 62. Because the
    EStG floor for post-2011 contracts is 62, a Basisrente written today **clears the § 851c age
    condition with room to spare**; but the two thresholds are genuinely different provisions with
    different histories and a reader must not assume they were harmonised. `[unverified]` on the 60,
    and gap 10.
  - **A second limb protects the accumulated capital, not merely the income.** The provision allows
    the debtor to have accumulated a capped amount free of attachment, on an **age-graduated annual
    allowance** — a small allowance in the twenties rising in steps to a larger one in the early
    sixties — subject to an **overall ceiling**. **The individual annual allowances and the overall
    ceiling are `[unverified]` and are deliberately not reproduced in this file**: practitioner
    sources give a schedule in six age bands and an overall cap in the low hundreds of thousands of
    euro, and this file could not confirm a single one of those numbers. See gap 9. What is settled,
    and what the product-spec needs, is the **shape**: protection of the fund is capped, the cap is
    age-graduated, and it is not unlimited.
  - **This is the reason the product is sold to the self-employed.** A Schicht-3 annuity with a
    *Rückkaufswert* is realisable and therefore attachable; a Basisrente is not, because there is
    nothing to realise. The protection is a **by-product of the prohibitions**, not an add-on.

### R13 — ZPO § 851d, SGB II § 12, SGB XII § 90 — insolvency and means-testing
- Publisher: Bundesministerium der Justiz / juris
- URL: not established
- Content: the surrounding protection. **§ 851d ZPO** extends comparable protection to Riester
  *Altersvorsorgevermögen*; **§ 12 SGB II** (*Bürgergeld*, formerly Hartz IV) and **§ 90 SGB XII**
  exempt from the means test old-age provision whose realisation is contractually excluded. The
  practical claim the market makes — that a Basisrente is *Hartz-IV-fest* and *insolvenzfest* — rests
  on these provisions together with [R12]. **All three paragraph addresses are `[unverified]`** and
  the precise conditions were not established (gap 9). The **direction** is not in doubt and it is a
  first-order selling point of the product.

### R14 — VVG § 165 (Beitragsfreistellung), § 168 (Kündigung), § 169 (Rückkaufswert)
- Publisher: Bundesministerium der Justiz / juris
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__165.html`, `.../__168.html`, `.../__169.html`
  — human-facing links only; §§ 165 and 153 answer as ~5 kB frameset shells with no statutory text
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156;
  §§ 153, 163, 165, 168, 169 and 171 read 2026-08-30)
- Content — **the provisions that would give an ordinary German life contract its exits, and what
  becomes of them here**:
  - **§ 165 — *Beitragsfreistellung*.** The policyholder of a contract with periodic premiums may at
    any time, for the end of the current premium period, demand conversion into a **premium-free
    contract with a reduced benefit**, provided the reduced benefit reaches a
    *Mindestversicherungsleistung* agreed in the contract. **This right survives intact in a
    Basisrente** and is the product's only real exit (mechanic 17).
  - **§ 168 — *Kündigung*. Corrected: the right does not survive.** This entry read "the right
    survives, but it has nothing to pay out". § 168 Abs. 3 as retrieved says otherwise: "*Die Absätze
    1 und 2 sind nicht auf einen für die Altersvorsorge bestimmten Versicherungsvertrag anzuwenden,
    1. wenn die Vertragsparteien bei einem nach § 5a des Altersvorsorgeverträge-Zertifizierungsgesetzes
    zertifizierten Basisrentenvertrag die Verwertung der Ansprüche gemäß § 10 Absatz 1 Nummer 2 Satz 1
    Buchstabe b des Einkommensteuergesetzes ausgeschlossen haben*". The **outcome** the file describes
    is nonetheless what happens, because carriers grant a *contractual* termination and word it as a
    conversion: GDV model conditions § 9 Abs. 3 and CosmosDirekt LA 1079 A § 7 Abs. 1 both convert to
    paid-up and pay no *Rückkaufswert* [S12] [S1]. Where the statutory disapplication shows on the
    face of a contract is the single-premium case, which LA 1079 A § 7 Abs. 2 declares "*auf Grund
    der gesetzlichen Restriktionen ... über die gesamte Vertragsdauer nicht kündbar*". **No longer
    `[unverified]` as to AVB wording** — two were read, and both also allow a *partial* termination
    or premium-freeze above an agreed minimum annuity.
  - **§ 169 — *Rückkaufswert*.** The statutory surrender-value regime — the *Zeitwert* rule, the
    *Mindestrückkaufswert* "*bei gleichmäßiger Verteilung der angesetzten Abschluss- und
    Vertriebskosten auf die ersten fünf Vertragsjahre*" (Abs. 3), the requirement that a *Stornoabzug*
    be agreed, appropriate and quantified (Abs. 5). **It is inoperative on this product as a
    payment.** A Basisrente has a *Deckungskapital* but no *Rückkaufswert* cash flow at any duration.
    **But Abs. 3 is very much operative as a *measure*, and that is what closes gap 8**: § 165 Abs. 2
    computes the premium-free benefit "*unter Zugrundelegung des Rückkaufswertes nach § 169 Abs. 3 bis
    5*", so the five-year spreading binds this product through the only exit it has. The distinction —
    inoperative as a payment, operative as a yardstick — is the thing a modeller coming from the delib
    endowment or Schicht-3 chassis has to learn rather than merely unlearn (mechanic 17).

### R15 — VVG § 153 — Überschussbeteiligung
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — canonical form; established by
  search in `_research/kapitallebensversicherung.md` [R1]
- Content: the policyholder's statutory entitlement to a share of the *Überschuss* and of the
  *Bewertungsreserven*, unless participation is expressly excluded. **A Basisrente participates on
  exactly the same terms as any other German life contract** — the layer changes the tax and the
  exits, not the surplus machinery. The four surplus sources (*Zins-*, *Risiko-*, *Kosten-* and
  *übriger Überschuss*), the *RfB*, the MindZV minimum allocation and the *Bewertungsreserven* share
  are all as established for the endowment chassis in the sibling file and are not re-derived here;
  mechanic 11 records only what is different for this product.

### R16 — Deckungsrückstellungsverordnung (DeckRV) — Höchstrechnungszins and Höchstzillmersatz
- Publisher: Bundesministerium der Justiz / juris; amendment by the Bundesministerium der Finanzen
- URL: **established 2026-08-30**: `https://www.gesetze-im-internet.de/deckrv_2016/`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250;
  §§ 2 and 4 read). § 2 Abs. 1: "*wird der Höchstzinssatz für die Berechnung der
  Deckungsrückstellungen auf 1 Prozent festgesetzt*". § 2 Abs. 2 Satz 1: "*Bei Versicherungsverträgen
  mit Zinsgarantie gilt der von einem Versicherungsunternehmen zum Zeitpunkt des Vertragsabschlusses
  verwendete Rechnungszins ... für die gesamte Laufzeit des Vertrages*". § 4 Abs. 1 Satz 2: "*Der
  Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten*". **What the retrieved
  text does not carry, and so stays `[unverified]`:** the 1 January 2025 effective date, the DAV's
  2026 recommendation, the pre-2015 40 ‰ and the full vintage ladder
- Content, carried over from `_research/klassische_rentenversicherung.md` [R7]–[R11], where it was
  corroborated across five independent search results:
  - The ***Höchstrechnungszins*** — the maximum rate a German life insurer may guarantee on the
    savings part of the premium — **rose from 0,25 % to 1,00 % with effect from 1 January 2025**,
    the first increase since 1994; the DAV has recommended **1,0 % for 2026** as well, so the rate
    applicable to new business at this file's access date is **1,00 %**.
  - **The increase applies only to new contracts.** A German life book is a **layered stack of
    guarantee vintages**, and a Basisrente book written since 2005 spans the whole of the decline
    from 2,75 % to 0,25 % and the 2025 recovery. The full ladder — 2,75 %, 2,25 %, 1,75 %, 1,25 %,
    0,90 %, 0,25 %, 1,00 % — is `[unverified]` in delib except for the 0,25 % and the 1,00 %.
  - The ***Höchstzillmersatz*** caps the acquisition costs that may be written into the reserve at
    **25 ‰ of the *Beitragssumme***, reduced from 40 ‰ by the LVRG in 2015 `[unverified]`. On a
    Basisrente the *Beitragssumme* of a long-dated contract with a *Beitragsdynamik* is large, so
    this cap binds in euro terms far above what the same percentage would allow on a short contract.

### R17 — DAV 2004 R — the annuity table
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV), Köln
- URL: not established; the DAV's own host refuses this environment
- Content, carried over from `_research/klassische_rentenversicherung.md` [R12]–[R14], where it was
  corroborated by search:
  - **DAV 2004 R is the German annuity table** and is a ***Generationentafel*** — mortality by birth
    cohort, with the improvement trend inside the table rather than applied on top of it. In use
    since June 2004, intended for new business from 2005, and the derivation guideline was
    **reissued on 28 June 2023** — evidence that no successor has displaced it.
  - Component structure: a second-order base table, a first-order base table, second- and
    first-order trends, and an *Altersverschiebung* convention. **First-order probabilities carry
    prudential margins and are used for premiums and reserves**; second-order is the best estimate.
  - **The table is not public and delib does not redistribute it.** A `[std]` proxy is shipped,
    anchored so the worked example reproduces exactly, and a replacement must preserve the
    generational structure, the first-order margin and the age-adjustment convention.
  - **The Basisrente uses the same table as every other German annuity.** There is no Schicht-1
    mortality basis. What differs is the **selection**: mechanic 12 argues that a Basisrente
    portfolio should be expected to be somewhat *lighter* than a Schicht-3 portfolio on mortality,
    because it cannot be surrendered and cannot be commuted, so nobody in poor health has any reason
    to leave it — but **no evidence for that was found and it is a `[std]` view**.

### R18 — BMF-Schreiben on the income-tax treatment of Vorsorgeaufwendungen and Altersbezüge
- Publisher: Bundesministerium der Finanzen
- URL: `https://amtliche-handbuecher.bundesfinanzministerium.de/esth/2024/C-Anhaenge/Anhang-01a/II/inhalt.html`
  — the circular as reproduced in the *Amtliches Einkommensteuer-Handbuch* 2024, Anhang 1a II. The
  `esth.` and `ao.` mirrors answer with a bot-check page and are unusable
- Identity: **BMF vom 24.05.2017 (BStBl I S. 820), IV C 3 – S 2221/16/10001 :004 – 2017/0392623**,
  *Einkommensteuerrechtliche Behandlung von Vorsorgeaufwendungen*, as amended by BMF v. 06.11.2017
  (BStBl I S. 1455), v. 28.09.2021 (BStBl I S. 1833), v. 16.12.2021 (BStBl I 2022 S. 155) and
  v. 28.12.2023 (BStBl I 2024 S. 209)
- Retrieved: **yes** (HTML, ~1,15 MB, read 2026-08-30; Rz. 16–34 and the *ergänzende Absicherung*
  block read closely)
- Content: the practitioner's circular on the deduction of *Vorsorgeaufwendungen* under § 10 EStG. It
  is where the operational detail lives that the statute does not spell out, and **three of the four
  points this entry listed as unestablished are now read**:
  - **The 50 % test and how it is computed** (Rz. 38): "*Die ergänzende Absicherung ist nur dann
    unschädlich, wenn mehr als 50 % der Beiträge auf die eigene Altersversorgung des Steuerpflichtigen
    entfallen. Für das Verhältnis der Beitragsanteile zueinander ist regelmäßig auf den konkret vom
    Steuerpflichtigen zu zahlenden (Gesamt‑)Beitrag abzustellen. Dabei dürfen die Überschussanteile
    aus den entsprechenden Risiken die darauf entfallenden Beiträge mindern.*" Rz. 42 requires the
    old-age cover and the supplementary covers to sit in **one contract**; Rz. 39 assigns a
    *Beitragsbefreiung* on disability to the old-age side; Rz. 41 does the same for a survivor's
    annuity funded solely out of the residual old-age capital.
  - **A change of provider** (Rz. 29): permitted if the contract allows it, only within the same
    product group, tax-free under § 3 Nr. 55d EStG, and the transferred capital is not a fresh
    contribution. Gap 13.
  - **The administrative tolerance for a small annuity** (Rz. 16): up to twelve monthly payments may
    be combined into one; with the *Kleinbetragsrente* commutation at Rz. 34, available only from the
    start of the payout phase and no earlier than the age floor. Gap 19.
  - Also read: Rz. 18's prohibition on a planned decline in the annuity, with the floor set by the
    annuity computed at the start of the payout phase on guaranteed capital plus irrevocably allocated
    surplus; Rz. 19's requirement that the contract oblige the provider to fix the mortality table and
    the interest factor before *Rentenbeginn*; and Rz. 21–22, which exclude an *Auszahlungsplan*, and
    an *Auszahlungsplan* followed by partial annuitisation, from being a lifelong annuity at all.
  - **Still not read: the *Rentenfreibetrag* mechanics**, which are in a different circular on § 22.

### R19 — BFH, 19 May 2021 — the Doppelbesteuerung judgments
- Publisher: Bundesfinanzhof
- URL: `https://www.bundesfinanzhof.de/en/entscheidungen/entscheidungen-online/decision-detail/STRE202110106/`
  for X R 33/19; the companion at `.../STRE202110105/`
- Retrieved: **yes** for X R 33/19 (HTML, ~130 kB, *Leitsätze* and grounds read 2026-08-30;
  ECLI:DE:BFH:2021:U.190521.XR33.19.0); the companion was located but only its file number taken.
  **Both file numbers and the date are confirmed.** The appeal was dismissed as unfounded and the
  appellant was a *Freiberufler* who had paid at the ceiling since 1984 — this product's own buyer.
  **One qualification**: the proposition that later cohorts will be caught is *not* in the
  *Leitsätze*; it is the court's press framing of what its method implies
- Content: two decisions of the same day, **X R 33/19** and **X R 20/19**,
  in which the court accepted **in principle** that a
  double taxation of pensions is unconstitutional where the contributions were made from taxed
  income and the benefits are taxed again, and set out a **nominal-value comparison method** for
  testing it: the sum of the tax-free parts of the expected benefits against the sum of the
  contributions paid from taxed income. On the facts before it the court found no double taxation,
  but it identified the transition schedule as capable of producing one for later cohorts —
  particularly for **self-employed taxpayers whose contributions during the phase-in were only
  partly deductible**, which is precisely the Basisrente's own buyer. The legislative response was
  [R7] and [R6]. **The case numbers, the date and the method are confirmed** from the retrieved
  judgment; what is *not* in the *Leitsätze* is the later-cohorts proposition, which is the court's
  press framing of what its method implies. The substance — that a court-driven concern about double
  taxation is why the schedule was twice softened — is the correct framing for the product-spec's tax
  section.

### R20 — Sozialversicherungsrechengrößen-Verordnung — the BBG series
- Publisher: Bundesministerium für Arbeit und Soziales, with the consent of the Bundesrat
- URL: **established 2026-08-30** — `https://www.gesetze-im-internet.de/svbezgrv_2026/BJNR1160A0025.html`
  and `https://www.gesetze-im-internet.de/svbezgrv_2025/BJNR16D0A0024.html`
- Retrieved: **yes**, both. § 3 Abs. 1 of the 2026 regulation sets the *Beitragsbemessungsgrenze*
  "*in der knappschaftlichen Rentenversicherung auf **124 800 Euro** jährlich; umgerechnet auf den
  Monat ergeben sich 10 400 Euro*"; the 2025 regulation gives **118 800 Euro**. With the 24,7 %
  *knappschaftlicher Beitragssatz* and the statutory rounding-up of § 10 Abs. 3 Satz 1 EStG those give
  the 2025 and 2026 *Höchstbeträge* of **29 344 €** and **30 826 €** exactly. The 2023 and 2024 inputs
  were not retrieved. **That the ceilings are uniform across the former East and West from 2025 is not
  in the retrieved sections and stays `[unverified]`** — they give one national figure for the
  *knappschaftliche* branch, which is consistent with it but does not say it
- Content: the annual regulation that sets the *Beitragsbemessungsgrenzen* and other social-insurance
  parameters for the following calendar year, made in the autumn of the preceding year. It is the
  instrument that moves the Basisrente *Höchstbetrag* [R2], and it therefore has to be re-read every
  year for this product in a way that is not true of any other delib product. From 2025 the general
  and *knappschaftliche* ceilings are **uniform across the former East and West** `[unverified]`,
  which removed a distinction that had complicated the *Höchstbetrag* for two decades. The series
  itself is tabulated in mechanic 6 and every figure there is `[unverified]`.

### R21 — BaFin — Wohlverhaltensaufsicht and value for money
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht
- URL: not established; the host refuses this environment
- Content, carried over from `_research/kapitallebensversicherung.md` [R17]–[R19]: BaFin's
  **Merkblatt 01/2023 (VA)** on conduct-supervision aspects of capital-forming life insurance
  products, its *Risiken im Fokus* treatment of the cost of such products, and its published
  articles on excessive costs and on PRIIPs disclosure. **A Basisrente is squarely within that
  supervisory perimeter** — it is a capital-forming life product sold overwhelmingly through
  intermediaries with a commission attached — and the *Effektivkosten* on the § 7 AltZertG
  *Produktinformationsblatt* [S13] is the number the supervision runs on. **Nothing
  Basisrente-specific was established** and gap 15 records it.

### R22 — GDV and BMF statistics on the Basisrente stock and new business
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft; Bundesministerium der Finanzen
- URL: not established
- Content: the GDV publishes annual *Bestand* and *Neugeschäft* statistics for German life insurance
  broken down by product line, including the Basisrente, and the BMF publishes subsidy statistics
  for the certified layers. **No figure from either was established in this session.** The
  order-of-magnitude statements in mechanic 21 are general knowledge, are tagged `[unverified]`
  individually, and are the weakest material in this file. See gap 3.

### R23 — EStG § 93 Abs. 3 — the Kleinbetragsrente, and its reach into Schicht 1
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__93.html` — human-facing link only
- Retrieved: **yes** (canonical XML, same *Stand* as [R1]; § 93 Abs. 3 read 2026-08-30)
- Content — **corrected on review, and now read**:
  - § 93 Abs. 3 Satz 1: "*Auszahlungen zur Abfindung einer Kleinbetragsrente zu Beginn der
    Auszahlungsphase gelten nicht als schädliche Verwendung.*" Satz 2 Nr. 1 defines the threshold:
    an annuity which, on an even annuitisation of the whole capital available at the start of the
    payout phase, "*eine monatliche Rente ergibt, die **1,5 Prozent** der monatlichen Bezugsgröße
    nach § 18 des Vierten Buches Sozialgesetzbuch nicht übersteigt*", aggregating all of the
    taxpayer's contracts at that provider (Satz 3). **The 1 % / 1,5 % contest is resolved in favour
    of 1,5 %, and both readings were right at different times**: the GDV model conditions of
    21 July 2025 still print 1 % [S12], and the 2026 amendment that raised it also added the
    *Auszahlungsplan* limb of Satz 2 Nr. 2 for payouts from 1 January 2027 [REG-R44].
  - **Schicht 1 has the same relief, and the cross-reference is corrected.** § 10 Abs. 1 Nr. 2
    Satz 3 EStG permits the commutation of "*eine Kleinbetragsrente im Sinne von § 93 Absatz 3
    Satz 2 **oder 4***" — **not "Satz 2 and 3"**, which is what this entry said. The older form
    survives in the documents that pin an earlier version: BMF Rz. 34 says "*in Anlehnung an § 93
    Absatz 3 Satz 2 und 3 EStG*" [R18], and CosmosDirekt's 2015 wording pins "*die im Jahr 2009
    geltende Fassung*" [S1]. § 93 Abs. 3 Satz 4 extends the treatment to an annuity pushed below the
    threshold **during** the payout phase by a *Versorgungsausgleich*; **which amending statute did
    that was not established** and stays `[unverified]`. Two further points from the retrieved
    documents: the commutation is available only from the start of the payout phase and no earlier
    than the age floor (BMF Rz. 34), and the GDV model conditions draft it as the **insurer's** right
    and not the policyholder's [S12]. Mechanic 19 works through the consequence.
  - **This entry originally read "there is no Schicht-1 equivalent ... admits no de-minimis".** That
    is withdrawn. It was reasoned from the unqualified wording of Buchst. b alone, and Buchst. b is
    not the whole of Nr. 2.

### R24 — Independent rating and market-analysis houses
- Publishers: **Institut für Vorsorge und Finanzplanung (IVFP)**, Altenstadt; **Franke und
  Bornberg**, Hannover; **Morgen & Morgen**, Hofheim; **Assekurata**, Köln
- URL: not established for any of them
- Content: these four are the German market's standing sources for comparative product analysis in
  this layer. The IVFP publishes the best-known **Basisrente rating**, scoring tariffs on company
  strength, flexibility, transparency, cost and return; Franke und Bornberg rates old-age provision
  products and analyses *Basisinformationsblätter*; Morgen & Morgen rates and models; Assekurata
  publishes the annual *Überschussbeteiligungen und Garantien* market study, whose 2026 edition was
  established in a sibling delib file. **Not one rating, score, ranking or figure was established
  for the Basisrente.** They are named so a checker knows where to go, and so that no downstream
  document invents a ranking.

---

## Extracted facts, organised by mechanic

This is the part of the file that does not depend on having a document open, and it is written
long. Every claim carries an `[S#]` or `[R#]` pointer to the instrument it must be checked against;
every specific number carries `[unverified]` or a `[std]` tag. Where a mechanic is shared with
another delib product it is stated once and cross-referenced rather than re-derived.

### 1. Product structure, legal form and the Schicht-1 placing

- A Basisrente is an **ordinary German life insurance contract governed by the VVG** [R14] [R15],
  written on a single life, which additionally satisfies the definitional conditions of
  § 10 Abs. 1 Nr. 2 Buchst. b EStG [R1] and holds a certificate under § 5a AltZertG [R9]. It is not
  a separate legal species. Everything that is true of a German deferred annuity is true of it
  unless the § 10 conditions displace it.
- **The layer, precisely.** German retirement provision is conventionally described in three layers.
  Layer 1 — *Basisversorgung* — contains the *gesetzliche Rentenversicherung*, the
  *berufsständische Versorgungswerke*, the *landwirtschaftliche Alterskasse* (all
  § 10 Abs. 1 Nr. 2 Buchst. **a**) and the **Basisrente** (Buchst. **b**) [R1]. Layer 2 —
  *Zusatzversorgung* — contains *Riester* and *betriebliche Altersversorgung*. Layer 3 is
  unsubsidised private provision, the delib `klassische_rentenversicherung` and
  `fondsgebundene_rentenversicherung` products.
- **The layer is a tax wrapper, not a chassis.** [S2] is the direct evidence: one insurer sells the
  same design — the same premium split, the same guarantee levels, the same *Rentenfaktor*
  machinery — as PrivatRente, BasisRente and RiesterRente, differing only in the wrapper. A delib
  reader should expect the Basisrente model to reuse the Schicht-3 chassis with the constraint set
  bolted on, and mechanic 22 argues exactly that.
- **The defining sentence** is the five-limb prohibition of [R1]: entitlements under the contract
  must be **not inheritable, not transferable, not chargeable, not saleable and not capitalisable**.
  Mechanic 3 takes them one at a time.
- **Providers.** Life insurers dominate. A Basisrentenvertrag may also be written by a
  *Kapitalverwaltungsgesellschaft* as a fund savings plan with an insurance-backed payout phase —
  the *Fonds-Basisrente*, out of delib scope, `[unverified]` as to its current market presence.

### 2. The two phases and the Rentenbeginn boundary

- The contract has an ***Aufschubphase*** (deferment) and a ***Rentenphase*** (payout), separated by
  the ***Rentenbeginn***. This is identical in shape to the delib Schicht-3 annuity, and the
  recursions there transfer unchanged.
- **Three things happen at *Rentenbeginn*, and only two of them survive into Schicht 1**:
  1. the accumulated capital is converted into an annuity at a *Rentenfaktor* (mechanic 10) —
     **survives**;
  2. the *Überschussverwendung* system for the payout phase is fixed (mechanic 11) — **survives**;
  3. the *Kapitalwahlrecht* is exercised or allowed to lapse — **does not exist here** [R1],
     mechanic 18.
- **The earliest permitted *Rentenbeginn*** is the completion of the **62nd year of life** for
  contracts concluded after 31 December 2011, and the completion of the **60th** for contracts
  concluded on or before that date [R1] [R8] `[unverified]` as to both figures and the transition
  date. A German in-force Basisrente book therefore carries **two age cohorts** as well as two tax
  cohorts, and a model of the book — as against a model of one contract — must carry the contract's
  conclusion year as a model-point attribute.
- **There is no statutory latest *Rentenbeginn*.** Contracts commonly allow deferral well past the
  statutory retirement age, and the buyer's tax position often makes deferral attractive because it
  raises the *Besteuerungsanteil* cohort year but shortens the payout period. **No carrier's
  permitted range was established** and it is `[std]` downstream.
- **The annuity must be monthly and lifelong and on the taxpayer's own life** [R1]. Three
  consequences: no term-certain annuity; no annuity on a second life other than the permitted
  survivor cover (mechanic 14); and no instalment plan of the Riester type. A Riester contract may
  pay an *Auszahlungsplan* until 85 with an annuity thereafter; a Basisrente may not.

### 3. The five prohibitions, taken one at a time

This section is the product. Each limb of [R1] is stated, then what it forbids, then what it means
for a cash-flow model.

| Limb | What it forbids | Modelling consequence |
|---|---|---|
| **nicht vererblich** | The entitlement forms no part of the estate. On death, capital does not pass to heirs | With no rider, **death before *Rentenbeginn* pays nothing**; the reserve is released to the *Versichertengemeinschaft* as a mortality profit |
| **nicht übertragbar** | The entitlement may not be assigned to a third party | No assignment decrement; no third-party-interest complication; the only permitted transfer is on divorce, mechanic 3 below |
| **nicht beleihbar** | The entitlement may not be pledged, mortgaged or used as loan security | **No policy loan** — the delib retired name `loan_bal` must not reappear on this product |
| **nicht veräußerbar** | The contract may not be sold | No secondary market. The German life secondary market, which exists for Schicht-3 endowments, cannot touch this product |
| **nicht kapitalisierbar** | The entitlement may not be turned into capital | **No *Rückkaufswert*, no *Kapitalwahlrecht*, no *Teilkapitalauszahlung***, mechanics 17 to 19. The one express statutory exception is the *Kleinbetragsrenten-Abfindung*, § 10 Abs. 1 Nr. 2 Satz 3 EStG, mechanic 19 |

- **The prohibitions bind the insurer's product design, not merely the policyholder's rights.** A
  contract offering any of these features is not a Basisrentenvertrag, cannot be certified [R9],
  and attracts no relief [R3]. This is stronger than a contractual restriction: it is a condition
  of the tax status of the whole contract.
- **The one permitted transfer is the *Versorgungsausgleich***. On divorce, German pension-sharing
  law splits entitlements acquired during the marriage and a Basisrente is within its scope; the
  receiving spouse's entitlement remains subject to the same prohibitions, so the product's
  character is preserved. **The mechanism — *interne* or *externe Teilung* — was not established**
  (gap 14) and delib does not model it.
- **A change of provider is a separate question from transferability** and was not resolved. A
  transfer to another *Basisrentenvertrag of the same person* is generally understood not to lose
  the tax status, the entitlement not passing to a third party, but **the conditions live in the
  guidance at [R18] and could not be established** (gap 13). Downstream this must not be asserted.
- **What *nicht vererblich* does not mean.** It does not mean the contract may not pay on death; it
  means the entitlement is not part of the estate and may not be directed by will. Within the narrow
  channel of mechanic 14 a death benefit is permitted, provided it is itself paid **as an annuity**.

### 4. Certification under § 5a AltZertG

- Certification by the **Bundeszentralamt für Steuern** is a **condition of the relief**, not of the
  contract's validity [R3] [R9]; required from 1 January 2010 `[unverified]`.
- Certification is a **formal conformity check** and expressly **not a quality mark** [R10]: it says
  nothing about charges, investment quality or the provider's strength, and every delib document
  mentioning it must repeat that.
- **What § 5a does not import is the load-bearing fact** [R9] [R10]: the Riester
  ***Beitragserhaltungsgarantie*** — the promise that at least the nominal contributions and
  *Zulagen* are available at the start of the payout phase — **has no Schicht-1 counterpart.** A
  Basisrente may be sold with a 100 % *Beitragsgarantie*, a partial one, or **none at all**. This is
  the reason the two subsidised layers have diverged so sharply in product design since the
  interest-rate collapse: Riester writers had to hold a nominal guarantee that became unaffordable
  at a 0,25 % *Höchstrechnungszins* and withdrew from the market; Basisrente writers simply dropped
  the guarantee and kept selling. Mechanic 9.
- The certification regime also carries the pre-sale information obligations at [R11], which is
  where the *Produktinformationsblatt* [S13] and its *Effektivkosten* come from.

### 5. Pfändungsschutz, insolvency and means-testing

- **§ 851c ZPO** protects a compliant private pension entitlement from attachment: the income stream
  is attachable only on the earnings scale, and the accumulated fund is protected up to an
  **age-graduated, capped allowance** [R12].
- **The § 851c conditions mirror the § 10 conditions but are not identical.** The most visible
  difference is the age: **§ 851c names the completion of the 60th year of life**, while
  § 10 Abs. 1 Nr. 2 Buchst. b names 62 for post-2011 contracts `[unverified]` on both. A contract
  written to the EStG standard therefore satisfies § 851c comfortably, but the two must not be
  treated as one provision. Gap 10.
- **The annual allowances and the overall cap are not reproduced in this file.** Practitioner
  sources give a six-band age schedule and an overall ceiling; **not one of those figures could be
  confirmed** and inventing them would be exactly the failure this library's house rules forbid.
  Gap 9. What the product-spec may say is the shape: *age-graduated annual allowance, overall
  ceiling, both `[unverified]` as to level*.
- **§ 12 SGB II and § 90 SGB XII** exempt from means-testing old-age provision whose realisation is
  contractually excluded [R13]. Taken together with § 851c this is the market's *insolvenzfest* /
  *Hartz-IV-fest* claim, and it is the principal non-tax reason a self-employed person buys the
  product.
- **The protection is a consequence of the prohibitions, not an added feature**: there is nothing to
  attach because there is nothing to realise. The same clause that makes the product illiquid for
  the owner makes it invisible to the owner's creditors.

### 6. The Förderung — the Höchstbetrag and the knappschaftliche peg

- Contributions under § 10 Abs. 1 Nr. 2 letters **a and b together** are deductible up to one
  annual ***Höchstbetrag***, doubled on joint assessment [R2].
- **The peg.** Since 2015 the ceiling equals the **maximum annual contribution to the
  *knappschaftliche Rentenversicherung***:

  ```
  Hoechstbetrag(year) = BBG_knappschaftlich(year) x Beitragssatz_knappschaftlich(year)
  ```

  The *knappschaftliche* branch is used, rather than the general one, because it has both a higher
  ceiling and a higher contribution rate, so the Basisrente ceiling is materially above the general
  BBG contribution. The inputs come from the annual
  *Sozialversicherungsrechengrößen-Verordnung* [R20].
- **The series, with every figure `[unverified]`** and offered so that the arithmetic can be checked
  rather than as a citation:

  | Year | BBG knappschaftlich, EUR p.a. | Beitragssatz knappschaftlich | Höchstbetrag, single, EUR | Höchstbetrag, joint, EUR | Tag |
  |---|---|---|---|---|---|
  | 2005–2014 | (not pegged) | — | 20,000 fixed | 40,000 | [unverified] |
  | 2015 | 89,400 | 24.8 % | 22,172 | 44,344 | [unverified] |
  | 2023 | 107,400 | 24.7 % | 26,528 | 53,056 | [unverified] |
  | 2024 | 111,600 | 24.7 % | 27,566 | 55,132 | [unverified] |
  | 2025 | 118,800 | 24.7 % | 29,344 | 58,688 | [unverified] |
  | 2026 | 124,800 | 24.7 % | 30,826 | 61,652 | [unverified] |

  Each line reproduces: 89 400 × 24,8 % = 22 171,20, rounded to 22 172; 107 400 × 24,7 % =
  26 527,80 → 26 528; 111 600 × 24,7 % = 27 565,20 → 27 566; 118 800 × 24,7 % = 29 343,60 →
  29 344; 124 800 × 24,7 % = 30 825,60 → 30 826. **The rounding convention (up to the next full
  euro) is inferred from the arithmetic and is itself `[unverified]`.** The 2026 line is the least
  secure of the six and is flagged separately in gap 11.
- **From 2025 the ceilings are uniform across the former East and West** `[unverified]`, which
  removed a two-decade complication from this calculation [R20].
- **The deductible share is 100 % from 2023** [R7]. The phase-in — 60 % in 2005 rising two points a
  year — is history for any contract a delib model point would represent, and the product-spec need
  carry only the current rule plus a note that pre-2023 cohorts differ.
- **The ceiling is shared, and that is the constraint that bites.** A *Freiberufler* in a
  *Versorgungswerk*, or a *Handwerker* with compulsory GRV membership, has most of it consumed under
  letter a before any Basisrente contribution is considered; the buyer with the whole ceiling free is
  the **genuinely non-insured self-employed person**, the product's core market (mechanic 21).
- **The ceiling moves every year, and so should the premium.** It is indexed to a wage-driven
  social-insurance parameter, which is why *Beitragsdynamik* and year-end *Zuzahlungen* are far more
  prominent here than on a Schicht-3 annuity (mechanic 8).

### 7. The Förderung — the interaction with the gesetzliche Rentenversicherung for employees

- Two distinct mechanisms operate on an employee and they are routinely confused [R2]:
  1. **The GRV contributions consume the ceiling.** Employee and employer contributions to the
     statutory scheme both count toward the same *Höchstbetrag*.
  2. **The tax-free employer share is then subtracted from the deductible amount**, because it was
     never taxed in the employee's hands and may not be relieved twice.
- In model notation, with all figures for one calendar year:

  ```
  base       = min( GRV_employee + GRV_employer + Basisrente_contribution , Hoechstbetrag )
  deductible = base x 1.00                      # 100 % from 2023  [R7]
  allowed    = deductible - GRV_employer        # the tax-free employer share  [R2]
  ```

- **A worked illustration, `[std]` throughout, using the 2025 ceiling** [unverified]. Employee with
  gross pay of 60 000 €, general GRV contribution rate 18,6 % split evenly `[unverified]`, paying
  5 000 € into a Basisrente:

  | Component | EUR | Note |
  |---|---|---|
  | GRV employee share | 5,580.00 | 60,000 x 9.3 % |
  | GRV employer share | 5,580.00 | 60,000 x 9.3 % |
  | Basisrente contribution | 5,000.00 | the model point |
  | Sum | 16,160.00 | below the 29,344 ceiling |
  | Deductible at 100 % | 16,160.00 | [R7] |
  | Less tax-free employer share | −5,580.00 | [R2] |
  | **Sonderausgabenabzug** | **10,580.00** | |

  The whole of the 5 000 € Basisrente contribution is relieved here, because the ceiling is not
  reached. **The arithmetic is this file's own, on `[unverified]` inputs, and is offered as an
  illustration of the mechanism rather than as tax advice.**

- **Where the ceiling does bite.** An employee at the 2025 general BBG of 96 600 € `[unverified]`
  pays GRV contributions of 96 600 × 18,6 % = 17 967,60 €, leaving 29 344 − 17 968 = **11 376 €** of
  headroom — a real but bounded amount, and the product's second market (mechanic 21). **A
  self-employed person outside the statutory scheme has the entire ceiling free**, 29 344 € in 2025
  and 58 688 € jointly `[unverified]`. That asymmetry, not the product's investment merits, is why
  the Basisrente is called the self-employed person's pension.
- **The third reduction, for taxpayers with a non-contributory entitlement** — *Beamte* and
  shareholder-directors with a *Pensionszusage* — subtracts a **notional** GRV contribution computed
  on their remuneration, leaving very little headroom [R2] `[unverified]`. This is why the product is
  effectively closed to *Beamte* even though nothing forbids them buying it.
- **None of this is a liability cash flow.** The relief accrues to the policyholder through the tax
  system, never through the insurer. Its place in a delib model is upstream of the model point: it
  determines **how large the premium is** and **why it is shaped the way it is**, and it belongs in
  the product-spec's market-role section, not in the projection.

### 8. Premium — forms, flexibility, and why this is the self-employed product

- Three premium forms exist and all three are common [S1] `[unverified]` as to any carrier's actual
  offering:
  - ***laufender Beitrag*** — a level recurring premium, monthly, quarterly, half-yearly or annually;
  - ***Zuzahlung*** — a one-off top-up into an existing contract, typically made at the year end once
    the year's profit is known;
  - ***Einmalbeitrag*** — a single-premium contract, used for a one-off tax event.
- ***Beitragsflexibilität* is the product's defining commercial feature**, and the reason it fits a
  self-employed income. A typical contract is written with a **small mandatory recurring premium**
  and an **open capacity for *Zuzahlungen*** up to the year's *Höchstbetrag*. In a good year the
  buyer tops up to the ceiling; in a bad year the buyer pays the minimum, or suspends. **No carrier's
  minimum premium, maximum *Zuzahlung* or suspension rule was established** and all are `[std]`
  downstream. The observed market convention for the minimum recurring premium is of the order of
  **25 € per month** `[unverified]`.
- ***Beitragsdynamik*** — a contractual annual escalation with a right to decline individual
  increases — appears here as on every German life contract, but with a **rationale it lacks
  elsewhere**: the *Höchstbetrag* itself rises every year with the *knappschaftliche* BBG [R2] [R20],
  so a static premium loses relief capacity each year.
- **Premium may be reduced, suspended and resumed.** Suspension is a *Beitragsfreistellung*
  (mechanic 17); resumption is a *Wiederinkraftsetzung*, usually within a stated window and possibly
  with renewed underwriting if a BUZ is attached. **No carrier's window was established.**
- **Modelling consequence.** The delib Schicht-3 annuity carries a level premium; the Basisrente
  should carry a **premium stream** — a level base plus an annual *Zuzahlung* — because that is the
  product's actual shape and it makes the *Höchstbetrag* indexation visible. The split is `[std]`.

### 9. Asset forms — klassisch, fondsgebunden, fondsgebunden mit Beitragsgarantie

- **All three forms are sold, and the absence of a statutory *Beitragsgarantie* [R9] [R10] is what
  makes the third one optional rather than mandatory.** This is the single sharpest structural
  contrast with Riester and it should open the product-spec's section on product variants.

| Form | Where the money sits | Guarantee at Rentenbeginn | Rentenfaktor |
|---|---|---|---|
| **klassisch** | *Sicherungsvermögen* (general account) | Guaranteed capital built at the *Rechnungszins*, currently 1.00 % [R16] | Guaranteed at inception |
| **fondsgebunden ohne Garantie** | Policyholder-selected funds | **None** — the value is the fund value | Guaranteed as a factor, applied to whatever fund value arrives |
| **fondsgebunden mit Beitragsgarantie** (hybrid) | Split between *Sicherungsvermögen* and funds, statically or dynamically | A selected percentage of contributions paid — [S2] reports **60 %, 80 % or 90 %**, 80 % standard `[unverified]` | Guaranteed as a factor |

- **The hybrid mechanics.** Two-pot and three-pot designs, *statische* and *dynamische Hybride*, and
  i-CPPI allocation all appear in the German market. [S2] is the corpus's only direct evidence and
  describes a split between the insurer's *Sicherungsvermögen* and a *Spezialfonds* with a
  selectable guarantee level. **The allocation rule was not established** for any carrier.
- **Which is sold most.** The market's centre of gravity has moved decisively from *klassisch* to
  *fondsgebunden* since the *Höchstrechnungszins* fell below 1 % [R16], and on a Schicht-1 contract
  there is nothing to stop a writer selling a pure unit-linked policy. The judgement that
  ***fondsgebundene* Basisrenten, with or without a partial guarantee, are the dominant new-business
  form and that pure *klassisch* is residual** is **general knowledge, `[unverified]`, and
  unsupported by any figure in this corpus** (gap 3). It is nevertheless the judgement the
  product-spec should adopt, with the tag: the alternative is contradicted by the same market
  evidence that led three of the largest German writers to withdraw the classic Schicht-3 tariff
  altogether, which a sibling delib file did establish by search.
- **What delib should model, and why.** The **klassisch** form, on an annual grid. The reasons are
  stated in mechanic 22; the short version is that the Schicht-1 *constraints* are the subject of
  this product and they are clearest against a general-account chassis whose reserve recursion the
  library already has, while the unit-linked machinery is already carried by delib product 3.
- A fourth form — an **index-linked Basisrente** — is plausible from the naming of at least one
  carrier's tariff family [S10] but **was not established**; gap 12.

### 10. The Rentenfaktor and the conversion at Rentenbeginn

- The mechanic is identical to the Schicht-3 annuity and is established in detail in the sibling
  delib file, which corroborated it across a carrier AVB, a product page and a consumer cluster.
  Restated here with pointers rather than a re-derivation:

  ```
  monthly_annuity = Kapital(Rentenbeginn) / 10 000 x Rentenfaktor
  Rentenfaktor_applied = max( Rentenfaktor_garantiert , Rentenfaktor_aktuell(Rentenbeginn) )
  ```

- The ***garantierter Rentenfaktor*** is fixed at inception on the *Rechnungsgrundlagen* then in
  force, with a deliberate prudential margin. **Corrected:** the 0 % interest basis this section
  carried was a Schicht-3 observation. The carrier's own **Basisrente** wording computes the factor
  "*auf Grundlage einer anerkannten Sterbetafel (DAV 2004R) sowie des tariflichen Garantiesatzes
  (Rechnungszins) von 1,25 Prozent p. a.*" — the tariff's own rate, which moves with the guarantee
  vintage [S1] [R16] [R17]. **One market level now exists**: a guaranteed 24,94 € per 10 000 € at 67
  on a 2025 fund-linked contract [S13]. The ***aktueller Rentenfaktor*** is the carrier's
  then-current immediate-annuity tariff, and the **higher of the two applies** — a guarantee with
  upside.
- **Nothing in Schicht 1 changes this.** The tax layer does not touch the conversion. What it does
  change is the **consequence of the conversion being the only outcome**: in Schicht 3 a
  policyholder facing a poor *Rentenfaktor* can take the *Kapitalwahlrecht* instead; a Basisrente
  policyholder cannot [R1]. **The guaranteed *Rentenfaktor* is therefore worth materially more on
  this product than on its Schicht-3 sibling**, because it is the only protection against a bad
  conversion, and a product-spec that treats the two as equivalent has missed the point.
- **No *Rentenfaktor* level, range or time series was established anywhere in the delib corpus**, for
  any product. The delib worked example must choose one and it will be `[std]`.
- The **§ 163 VVG adjustment channel** and the historic *Treuhänderklausel*, both narrowed by the
  courts, apply here as they do in Schicht 3. delib treats the guaranteed factor as fixed for the
  life of the contract and records the channel as a model risk.

### 11. Überschussbeteiligung

- **The surplus machinery is unchanged by the layer** [R15]. The four surplus sources, the *RfB*,
  the MindZV minimum allocation, the *Bewertungsreserven* share under § 153 Abs. 3 VVG, the annual
  declaration at the balance date, and the three payout-phase systems — *konstante*,
  *teildynamische* and *volldynamische Rente* — are all as established for the endowment and
  Schicht-3 chassis in the sibling delib files. They are not re-derived here.
- **Two things are different, and both follow from the prohibitions**:
  1. **The *Überschussverwendung* options are narrower in the *Aufschubphase*.** Systems that pay
     surplus out in cash sit awkwardly with the *nicht kapitalisierbar* rule; *verzinsliche
     Ansammlung* and *Bonusrente*, which keep the value inside the contract and convert it into
     annuity at *Rentenbeginn*, are the natural forms. **No carrier's option list was established**
     (gap 17).
  2. **The *Schlussüberschussanteil* has no early-exit trigger.** On an endowment a terminal bonus
     is allocated at maturity and, partly, on surrender; a Basisrente has no surrender, so it is
     allocated **only at *Rentenbeginn***, a cleaner single-date cash flow than anywhere else in
     delib.
- **No declared rate specific to a Basisrente was established.** The market-average declared rates
  carried in the sibling files are Schicht-3 and endowment figures and must not be relabelled.

### 12. Rechnungsgrundlagen and decrements

- **Interest.** The *Höchstrechnungszins* for new business is **1,00 %** from 1 January 2025 and is
  recommended to remain at 1,00 % for 2026 [R16]. An in-force Basisrente book written since 2005
  spans the guarantee vintages from 2,75 % down to 0,25 % and back to 1,00 %.
- **Mortality.** DAV 2004 R, generational, first order for pricing and reserving, second order for
  best estimate [R17]. The same table serves both phases, which means the *Aufschubphase* death
  decrement is priced on an annuitant table — but on this product that mismatch is **immaterial in
  the base design**, because with no *Hinterbliebenenschutz* there is no death benefit at all
  (mechanic 14). That is a genuine simplification relative to the Schicht-3 sibling, where the
  *Beitragsrückgewähr* death benefit is standard.
- **The decrement set is unusual and it is the heart of the modelling story**:

  | Decrement | Present? | What it pays | Note |
  |---|---|---|---|
  | Death in *Aufschubphase* | yes | **nothing** in the base design | With a rider: a survivor's annuity, mechanic 14 |
  | Death in *Rentenphase* | yes | ends the annuity | With a *Rentengarantiezeit*: continues to eligible survivors only |
  | Surrender | **no** | — | Forbidden [R1]; there is no *Rückkaufswert* cash flow at any duration |
  | *Beitragsfreistellung* | yes | nothing; reduces future premium and benefit | **The dominant exit**, mechanic 17 |
  | Transfer to another provider | possibly | moves the *Deckungskapital* out | Conditions not established, gap 13 |
  | *Berufsunfähigkeit* | only with a BUZ | a disability annuity plus premium waiver | Mechanic 13 |

- **A model of this product has no surrender decrement** — the most important design instruction in
  this file. A modeller reusing the delib endowment or Schicht-3 chassis will carry a `surr_rate`
  and a *Rückkaufswert* cell across by habit; both must go, and delib's retired-name register
  already bars the column `claims_surr` from `result_cf()`.
- **Selection.** A Basisrente cannot be surrendered or commuted, so a policyholder in poor health
  has no exit — which argues for **lighter mortality than a comparable Schicht-3 portfolio**, where
  the *Kapitalwahlrecht* lets an impaired life leave the annuitant pool. **No evidence for this was
  found**; it is a `[std]` view and a stated model risk.
- **No lapse rate, no *Beitragsfreistellung* rate and no market *Stornoquote* specific to the
  Basisrente was established.** Every behavioural assumption downstream is `[std]` and labelled a
  modeller's view. The *Beitragsfreistellung* rate on this product should nevertheless be expected
  to be **higher than a Schicht-3 lapse rate at short durations** — the buyer's income is volatile
  by construction, and going premium-free is free of penalty and reversible — and **lower at long
  durations**, because there is no realisable value to tempt anyone out. That shape is `[std]`.

### 13. Berufsunfähigkeits-Zusatzversicherung inside the contract, and the 50 % rule

- **§ 10 Abs. 1 Nr. 2 Buchst. b permits, inside the same contract, cover against *Berufsunfähigkeit*
  and against *verminderte Erwerbsfähigkeit*** [R1]. The premium for that cover is then deductible
  **inside the Schicht-1 *Höchstbetrag*** at 100 % [R2] [R7].
- **The 50 % rule.** The contributions qualify under this provision only if **more than half of the
  total contribution is attributable to the old-age provision**; the supplementary covers —
  disability and survivor together — must stay **below 50 %** of the total `[unverified]` as to the
  statutory address, settled as substance and universally applied. Consequences:
  - **A standalone Basisrenten-BU does not exist.** The disability cover must ride on an old-age
    contract that is itself more than half the premium.
  - The rule **caps the achievable disability annuity** for a given total premium. A buyer wanting a
    large *BU-Rente* must buy at least as much old-age provision alongside it, which is exactly the
    legislator's intention.
  - It is a hard constraint on a delib model point: `bu_premium_share < 0.50` is an invariant the
    test module should assert.
- **Why anyone does this.** The premium for a *selbständige Berufsunfähigkeitsversicherung* (delib
  product 9) falls into *sonstige Vorsorgeaufwendungen* under § 10 Abs. 1 Nr. 3a EStG, whose small
  ceiling is in practice already exhausted by health and long-term-care contributions, so it is
  **effectively not deductible at all**; the same cover as a BUZ inside a Basisrente is deductible
  in full inside a much larger ceiling.
- **The counterweight is the tax on the benefit.** A *BU-Rente* paid out of a Basisrentenvertrag is
  a benefit from that contract and is taxed under § 22 with the **full cohort *Besteuerungsanteil***
  [R4], not at the low *Ertragsanteil* that applies to the temporary annuity from a standalone SBU
  `[unverified]`, and gap 16. **A buyer is therefore trading relief now for a heavily taxed benefit
  later, at a moment — disability — when income has collapsed and the marginal rate may be low.**
  That trade is the whole of the BUZ-versus-SBU argument and the product-spec should state it as a
  trade rather than as an advantage.
- **Further constraints, `[unverified]` in every particular**: the disability cover ends at the
  latest at the main contract's *Rentenbeginn*; the *BU-Rente* is itself subject to the
  non-capitalisation rule, so no lump-sum settlement is possible; and a premium waiver
  (*Beitragsbefreiung*) is the normal companion cover. **No carrier's BUZ wording was reached** [S5]
  — gap 18.
- **Modelling.** delib's `basisrente` model should carry the BUZ as an **off-in-the-base-run module**
  with its own decrement and its own premium share, and delib product 9 owns the disability
  mechanics proper. The one thing the Basisrente model must own is the **50 % constraint**.

### 14. Hinterbliebenenschutz — what may be added, and the narrow channel it runs in

- **The permitted beneficiaries are closed** [R1]: the **spouse or registered partner**, and
  **children for so long as *Kindergeld* or the *Kinderfreibetrag* runs** in respect of them —
  in practice to the completion of the 18th year, or to the 25th while in education or training
  `[unverified]` on the ages. **Nobody else.** Not a cohabiting partner, not a parent, not a
  sibling, not the estate. This is the operative content of *nicht vererblich*.
- **Everything paid to a survivor must be paid as an annuity.** A Basisrente may not pay a lump sum
  to anyone at any time [R1]. That converts the two familiar German death-benefit designs into
  something different:

| Design | In Schicht 3 | In Schicht 1 |
|---|---|---|
| ***Beitragsrückgewähr*** in the *Aufschubphase* | Premiums paid, or the *Deckungskapital*, returned as a **lump sum** to any named beneficiary | The same amount must **buy a survivor's annuity** for an eligible survivor; with no eligible survivor, **nothing is paid** |
| ***Rentengarantiezeit*** in the *Rentenphase* | Remaining instalments continue to any named beneficiary, often commutable | Remaining instalments continue **only to an eligible survivor**, and are **not commutable**; with none, payments cease |
| **Spouse's / survivor's annuity** | An optional rider on a freely chosen life | The **natural** form here, because it is the only form that fits the channel |

- **The consequence for a model is a conditional probability, not a benefit.** The value of any
  Hinterbliebenenschutz on a Basisrente is the value of the benefit **multiplied by the probability
  that an eligible survivor exists at the moment of death** — a spouse alive and still married, or a
  child still inside the *Kindergeld* window. On a contract taken at 45 and running to 67 the child
  channel has usually closed long before *Rentenbeginn*, so in practice the cover is a **spouse
  cover**. That probability is a `[std]` assumption with no evidence behind it, and it is one of the
  more consequential `[std]` choices in the whole delib library.
- **The cover costs annuity.** Every euro of survivor cover reduces the *Rentenfaktor* or raises the
  premium. The sibling corpus's Schicht-3 illustration put a 10-year *Rentengarantiezeit* at roughly
  0,5 % of the annuity, 20 years at 2,6 % and 30 years at 8,0 % — `[unverified]`, **Schicht-3
  figures, not transferable**. **No Basisrente-specific cost was established.**
- **Base design.** Because the channel is so narrow, the honest base run for a delib reference model
  is **no *Hinterbliebenenschutz***: death before *Rentenbeginn* pays nothing, death in payment ends
  the annuity. The rider is then an explicit module the reader can switch on, with the
  eligible-survivor probability exposed as the `[std]` parameter it is. That ordering — pure product
  first, rider second — is also the ordering the statute itself uses.

### 15. Taxation of the Rentenphase — the Besteuerungsanteil cohort table

- Benefits from a Basisrentenvertrag are *sonstige Einkünfte* taxed on a ***Besteuerungsanteil***
  fixed by the **calendar year of *Rentenbeginn*** [R4]. The taxpayer's age, income and contribution
  history are irrelevant to the percentage.
- **The schedule, and how it is built.** 50 % for annuities beginning in 2005 or earlier; **+2
  percentage points per cohort year to 80 % for 2020**; **+1 point per year for 2021 and 2022**; and
  **+0,5 points per year from 2023**, after the amendment at [R6], reaching **100 % for 2058**.
  **The construction is settled; every individual percentage below is `[unverified]`:**

  | Cohort year of Rentenbeginn | Besteuerungsanteil | Rentenfreibetrag | Tag |
  |---|---|---|---|
  | 2005 and earlier | 50.0 % | 50.0 % | [unverified] |
  | 2010 | 60.0 % | 40.0 % | [unverified] |
  | 2015 | 70.0 % | 30.0 % | [unverified] |
  | 2020 | 80.0 % | 20.0 % | [unverified] |
  | 2021 | 81.0 % | 19.0 % | [unverified] |
  | 2022 | 82.0 % | 18.0 % | [unverified] |
  | 2023 | 82.5 % | 17.5 % | [unverified] |
  | 2024 | 83.0 % | 17.0 % | [unverified] |
  | 2025 | 83.5 % | 16.5 % | [unverified] |
  | **2026** | **84.0 %** | **16.0 %** | [unverified] |
  | 2030 | 86.0 % | 14.0 % | [unverified] |
  | 2040 | 91.0 % | 9.0 % | [unverified] |
  | 2050 | 96.0 % | 4.0 % | [unverified] |
  | 2057 | 99.5 % | 0.5 % | [unverified] |
  | **2058 and later** | **100.0 %** | **0.0 %** | [unverified] |

  The table is internally consistent: 82,5 + 35 × 0,5 = 100,0 for 2058, and 82,5 + 17 × 0,5 = 91,0
  for 2040. That arithmetic is the only corroboration this file can offer for it.
- **The 2023 change is the one to state explicitly.** Before the *Wachstumschancengesetz* [R6] the
  step was a full percentage point and the 100 % year was **2040**. The amendment halved the step
  **with retrospective effect for the 2023 cohort** — which is why 2023 is 82,5 % and not 83 % —
  and pushed the 100 % year out to **2058**. The purpose was to reduce the risk of double taxation
  identified in the 2021 case law [R19], together with the parallel change on the contribution side
  [R7].
- ***Der Rentenfreibetrag ist ein Euro-Betrag.*** The untaxed part is computed **once**, in the
  first full calendar year of receipt, as a euro amount, and is then **frozen for life** [R4]. Two
  consequences that a product-spec must state:
  1. **Every subsequent increase in the annuity is fully taxable.** A *volldynamische Rente*, whose
     whole point is that it rises, is taxed at an effective rate that climbs towards 100 % of the
     increment.
  2. **The choice of *Überschussverwendung* system in the payout phase has a tax dimension** that it
     does not have in Schicht 3. A rising annuity is worth less after tax than the same present
     value delivered flat. Nothing in the corpus discusses this, and it is offered as an analytic
     consequence of [R4] rather than as a sourced claim.
- **A delib model does not compute tax.** The *Besteuerungsanteil* belongs in the product-spec, not
  in the projection: delib models publish gross best-estimate liability cash flows. Its role is to
  explain the product's economics and to justify the model point.

### 16. Taxation — the remaining pieces

- **The contribution side** is mechanics 6 and 7: 100 % of the capped contribution from 2023 [R7],
  inside a shared ceiling pegged to the *knappschaftliche* BBG [R2].
- **A *BU-Rente* from a Basisrentenvertrag** is taxed with the same cohort *Besteuerungsanteil* as
  the old-age annuity [R4] `[unverified]`, not at the *Ertragsanteil* of an *abgekürzte Leibrente*.
  Gap 16.
- **A *Hinterbliebenenrente* from a Basisrentenvertrag** is taxed in the survivor's hands on the
  same basis `[unverified]`, with the cohort year determined by the start of that annuity rather
  than the deceased's. **Not established**; gap 20.
- **Social-insurance contributions on the annuity in payment.** A private annuity is not a
  *Versorgungsbezug*, so for a pensioner compulsorily insured in the *Krankenversicherung der
  Rentner* it is generally **not** subject to health and long-term-care contributions, while a
  **voluntarily insured** pensioner pays on it. `[unverified]` in every particular; gap 21. The
  difference is large enough — of the order of 18 % of the annuity — that a product-spec should
  flag it as a driver of the after-tax comparison, without asserting the rule.
- The 102 € *Werbungskosten-Pauschbetrag* `[unverified]` reduces the taxable amount trivially.
  **Nothing on the payout side is a liability cash flow**; all of it is context for the model point.

### 17. Beitragsfreistellung against Kündigung — the exits

- **There is no exit that pays money.** That is the operative summary and it should be the first
  sentence of the product-spec's termination section.
- ***Kündigung*. Corrected: the statutory right does not survive.** § 168 Abs. 3 Nr. 1 VVG
  disapplies Abs. 1 and 2 to a certified *Basisrentenvertrag* whose *Verwertung* is excluded [R14].
  Carriers nonetheless grant a **contractual** termination and word it as a conversion: the GDV model
  conditions and CosmosDirekt's LA 1079 A both turn the contract paid-up and pay no *Rückkaufswert*
  [S12] [S1], so the outcome this file describes is what happens. Where the statutory disapplication
  shows on the face of a contract is the single-premium case, which LA 1079 A § 7 Abs. 2 declares not
  terminable at all. **No longer `[unverified]` as to AVB wording**: two were read, and both also allow
  a *partial* termination or premium-freeze above an agreed minimum annuity.
- ***Rückkaufswert*.** § 169 VVG is inoperative [R14] [R1]. There is a *Deckungskapital* — the
  contract has a reserve like any other — but **there is no duration at which any part of it is
  payable to the policyholder as capital**. A delib model of this product publishes no surrender
  benefit and carries no *Stornoabzug*.
- ***Beitragsfreistellung*** under § 165 VVG survives intact [R14] and is the product's real exit:
  - Exercisable **at any time**, effective at the end of the current premium period.
  - Converts to a **premium-free entitlement** to a reduced annuity, the reduction computed from the
    *Deckungskapital* reached, less any agreed deduction.
  - Conditional on the reduced benefit reaching the contract's *Mindestversicherungsleistung*
    `[unverified]`; **no carrier's threshold was established** and it is `[std]` downstream.
  - **Reversible.** Premiums can normally be resumed within a stated window
    (*Wiederinkraftsetzung*); **no window was established**.
- **Why this matters more here than anywhere else in delib.** Elsewhere *Kündigung* and
  *Beitragsfreistellung* are two exits competing for the same policyholder and a model must not
  merge them; here **there is only one**, and the policyholder facing a cash crisis has one lever.
  That should put the *Beitragsfreistellung* rate above a Schicht-3 lapse rate at short durations
  and make the paid-up cohort a large permanent part of the book rather than a residue.
- **A paid-up Basisrente is still a Basisrente**: still certified, still protected, still taxed on
  the *Besteuerungsanteil*, still payable only as an annuity from 62 at the earliest. Nothing about
  going premium-free releases the constraints.

### 18. The ban on Kapitalwahl and Teilkapitalauszahlung

- **There is no *Kapitalwahlrecht*.** [R1]'s *nicht kapitalisierbar* forbids it outright. The
  policyholder has no election at *Rentenbeginn*: the capital becomes a monthly lifelong annuity and
  that is the whole of it.
- **There is no *Teilkapitalauszahlung* either.** A Riester contract may pay up to **30 %** of the
  capital as a lump sum at the start of the payout phase `[unverified]`; a Schicht-3 contract may
  pay 100 %. A Basisrente may pay **nothing**.
- **Three consequences for a model, and they are all simplifications**:
  1. **No election switch.** The Schicht-3 model carries the *Kapitalwahlrecht* as a model-point
     switch that reshapes the whole payout phase, plus an unevidenced take-up assumption. The
     Basisrente model carries **neither**; the payout phase has exactly one shape.
  2. **No notice-period parameter.** The Schicht-3 chassis needs a declaration window before
     *Rentenbeginn*; this product does not.
  3. **The § 20 EStG tax regime never engages.** The *Halbeinkünfteverfahren* and the 12/62 rule are
     Schicht-3 mechanics that reach a Basisrente at no point in its life.
- **The economic price of the ban** is that the policyholder bears conversion risk with no way out —
  which is what makes the guaranteed *Rentenfaktor* the product's most valuable guarantee
  (mechanic 10) — and that the contract is worth nothing to anyone needing liquidity.

### 19. Kleinbetragsrente — the answer is yes, and an earlier draft of this file said no

The commissioning brief asks whether a *Kleinbetragsrenten-Abfindung* is possible in Schicht 1, and
what the answer actually is. It is:

- **Yes.** § 10 Abs. 1 Nr. 2 Buchst. b [R1] forbids capitalisation in unqualified words, but
  Buchst. b is not the whole of Nr. 2: **§ 10 Abs. 1 Nr. 2 Satz 3 EStG** carries an express
  de-minimis exception, making an *Abfindung* of a *Kleinbetragsrente* — on the § 93 Abs. 3 Satz 2
  and 3 mechanics [R23] — harmless to the contract's Schicht-1 status at the start of the payout
  phase, and, since the *Wachstumschancengesetz*, also where a *Versorgungsausgleich* takes the
  annuity below the threshold during the payout phase. **All of this is `[unverified]`**: this
  product was researched with no fetch and no search. **[REG-R42], written while search was still
  available, records the same parity — "for Riester and Basisrente alike" — and is the better
  authority.**
- **An earlier draft of this mechanic answered "No", reasoning from Buchst. b alone.** That answer
  is withdrawn; it is recorded here rather than deleted because it propagated into
  `product-spec.md`, `sources.md`, `model.md`, the model docstrings and a test comment, all of
  which have been corrected.
- **The contrast is not one of threshold either: the same threshold governs both.** § 93 Abs. 3
  Satz 2 Nr. 1 EStG as retrieved sets it at **1,5 % of the monthly *Bezugsgröße* of § 18 SGB IV**,
  and § 10 Abs. 1 Nr. 2 Satz 3 imports it for a *Basisrentenvertrag* without variation [R1] [R23].
  The **1 %** this file carried is the older figure and still stands in the GDV model conditions of
  July 2025 [S12]. And a carrier's AVB **does** offer the *Abfindung* — CosmosDirekt LA 1079 A § 1
  Abs. 2 [S1] — while the GDV model conditions make it the **insurer's** election, not the
  policyholder's [S12], which is the answer to "on whose election" and the reason a projection model
  cannot assume take-up.
- **What the market does instead** — and every item here is `[unverified]`, because no carrier
  document was reached:
  - **Minimum premiums**, so that a contract cannot easily reach *Rentenbeginn* with a trivial
    capital.
  - **Minimum annuity thresholds in the AVB**, below which the insurer may pay at **longer
    intervals** — quarterly or annually instead of monthly. Whether that is compatible with the
    statutory requirement of a *monatliche* annuity is an administrative question whose answer lives
    in the BMF guidance at [R18] and **was not established**. Gap 19.
  - **Consolidation before *Rentenbeginn*** into one contract, which depends on gap 13.
- **The modelling consequence is a decision, not a deduction.** `Basis_DE_S` does **not** implement
  the commutation branch: the threshold level is contested, whether an AVB offers the *Abfindung*
  was not established (gap 19), and `Riester_DE_S` already carries the mechanic with the test
  computed rather than assumed. So every model point annuitises its whole capital, model point 10 —
  300,00 € a year — included, and that is what the test module asserts. **It is a `[std]`
  simplification and a named model risk, and must not be presented as a prohibition.**

### 20. Charges

- **The charge structure is that of any German life contract** and is not modified by the layer:
  *Abschluss- und Vertriebskosten* financed by *Zillmerung* subject to the **25 ‰ of *Beitragssumme***
  cap [R16] `[unverified]`; *Verwaltungskosten* as a percentage of premium and a percentage of the
  fund or reserve, plus *Stückkosten*; a *Ratenzahlungszuschlag* for paying other than annually;
  and, on unit-linked forms, the fund's own TER on top.
- **Two Basisrente-specific points.**
  1. **The *Beitragssumme* is large.** A long-dated contract with a *Beitragsdynamik* and regular
     *Zuzahlungen* accumulates a big *Beitragssumme*, so a 25 ‰ cap permits a large euro amount of
     acquisition cost. **How *Zuzahlungen* enter the *Beitragssumme* for the cap — at all, or on a
     separate charge basis — was not established** and is gap 8.
  2. **The comparable disclosure exists and delib could not obtain it.** The § 7 AltZertG
     *Produktinformationsblatt* [S13] [R11] states the ***Effektivkosten*** — the total charge
     burden as a single annualised reduction in yield — for this product, per quotation. Not one was
     reached. Gap 2.
- **The one charge datum in the corpus** is [S2]: **total costs relative to the capital formed of at
  most 0,95 € per 100 €** in the BasisRente and RiesterRente variants of one carrier's hybrid
  chassis, and an **Abschlussprovision of 1 575 €** on a specimen quotation, both `[unverified]` and
  both from third-party commentary rather than a tariff sheet. Read as a reduction in yield, the
  first is of the order of **0,95 % p.a.**
- **Every charge level downstream is `[std]`**, with the following argued plausible ranges, offered
  as the reference implementation's rationale and **not** as sourced figures:

  | Charge | `[std]` range for a Basisrente | Rationale |
  |---|---|---|
  | *Effektivkosten*, klassisch | 0.6 % – 1.2 % p.a. | Below the unit-linked forms; no fund layer |
  | *Effektivkosten*, fondsgebunden with commission | 1.0 % – 1.8 % p.a. | Adds a fund TER and a larger acquisition load |
  | *Effektivkosten*, *Nettotarif* (fee-based) | 0.3 % – 0.8 % p.a. | No *Abschlussprovision*; a real and growing segment on this product |
  | *Abschlusskosten* | at or near the 25 ‰ cap | [R16] caps it; [S2]'s 1 575 € specimen is consistent with a cap-binding design |
  | *Verwaltungskosten*, % of premium | 5 % – 10 % | Market convention across German life |
  | *Verwaltungskosten*, % of reserve or fund | 0.2 % – 0.6 % p.a. | Market convention |
  | *Ratenzahlungszuschlag* | 2 % half-yearly / 3 % quarterly / 5 % monthly | Carried from the sibling delib corpus as a market convention |

  **The whole table is `[std]`.** It is the reference implementation's parameter set with its
  reasoning attached, not a market survey, and it must be labelled that way wherever it is reused.

### 21. Market size, new business and the buyer

**This is the weakest section in the file and every figure in it is `[unverified]` general knowledge.
No statistic from [R22] or from any consumer or comparison source [S16] was established.** It is
included because the product-spec needs a market-role paragraph and because saying "not established"
with an order of magnitude beside it is more useful than saying nothing — provided the tag is
carried. Gap 3 records the whole of it.

- **Stock.** The number of Basisrente contracts in force in Germany is of the order of **two and a
  half million** `[unverified]`. For scale, Riester is of the order of **fifteen to sixteen million**
  `[unverified]` and declining. Basisrente is therefore a **large but minority** part of the
  subsidised market by contract count.
- **New business.** Of the order of **a hundred thousand new Basisrente contracts a year**
  `[unverified]`, on a declining trend in count. Its share of new life business by **premium** is
  much higher than its share by count, because the average contribution is several times a Riester
  contribution — the ceiling is fifteen to thirty times larger and the buyer is a higher earner.
- **Average contribution.** Of the order of **two to four thousand euro a year** `[unverified]`,
  against roughly eight hundred for a Riester contract `[unverified]`.
- **The buyer.** Two distinct populations, and the product-spec should describe both. First, **the
  self-employed person with no compulsory scheme** — the buyer the product was designed for: the
  entire *Höchstbetrag* is free (mechanic 7), the *Pfändungsschutz* (mechanic 5) matters as much as
  the relief, the income is volatile, which is what the *Zuzahlung* structure is for (mechanic 8),
  and there is often no other pension at all. Second, **the high-earning employee or partner using
  residual headroom** as a late-career deferral vehicle, frequently by *Einmalbeitrag* in a
  high-income year, entering at 50 or later with a short deferment. In both cases the entry age is
  **materially higher than for a Riester or Schicht-3 contract** — the mid-forties rather than the
  early thirties `[unverified]` — because the product only makes sense once income is high enough
  for the relief to be worth the illiquidity. **Distribution** is predominantly through **brokers
  and independent advisers** `[unverified]`, and the fee-based *Nettotarif* segment is more
  developed here than on most German life products.
- **The product's fundamental commercial problem**: the relief is real and large, but **the product
  is irreversible**. A buyer who commits at 45 and needs the money at 55 cannot have it. That is not
  a defect to be engineered away; it is the consideration for the *Pfändungsschutz* and the relief.

### 22. What a projection model needs, and what the corpus supplies

| Model input | Status | Tag |
|---|---|---|
| Product definition and the five prohibitions | established as substance; addresses unconfirmed | [R1] |
| Earliest *Rentenbeginn* (62 / 60 by cohort) | established as substance | [R1] [R8] |
| Ban on *Kapitalwahl* and *Teilkapital* | established | [R1] |
| Absence of a *Rückkaufswert* | established | [R1] [R14] |
| *Beitragsfreistellung* right | established | [R14] |
| Permitted survivor beneficiaries | established as substance | [R1] |
| 50 % rule for supplementary covers | established as substance; address unconfirmed | [R1] |
| *Höchstbetrag* level, 2023–2026 | **[unverified]**, arithmetic reproducible | gap 11 |
| Deductible share 100 % from 2023 | established as substance | [R7] |
| *Besteuerungsanteil* schedule and the 2058 endpoint | construction established; values **[unverified]** | [R4] [R6] |
| *Höchstrechnungszins* 1.00 % | established, carried from a sibling delib file | [R16] |
| Mortality basis DAV 2004 R | established, carried; table not public | [R17] |
| *Rentenfaktor* level | **not established anywhere in delib** | gap 4 |
| *Effektivkosten* level | **not established** | gap 2 |
| Acquisition-cost cap 25 ‰ | established, carried | [R16] |
| Actual charge levels | **not established** | gap 2 |
| Minimum premium, minimum annuity | **not established** | gap 8 |
| *Beitragsfreistellung* rate | **not established** | gap 3 |
| Mortality selection on a non-surrenderable annuity | **not established** | `[std]` view |
| Eligible-survivor probability | **not established** | `[std]` view |
| Market size, new business, buyer profile | **not established**; order of magnitude only | gap 3 |
| Carrier parameter ranges | **not established for any carrier** | gap 1 |

---

## Observed variation across insurers

**An honest variations table for this product is almost entirely a record of what could not be
compared.** Two carriers produced any artefact at all, and neither produced a term. Presenting a
rich table here would be a fabrication, so what follows is the real state of the evidence.

| Feature | CosmosDirekt [S1] | Allianz [S2] [S3] | The other 19 carriers [S4]–[S11] |
|---|---|---|---|
| Basisrente wording located | **yes — and read**: LA 1079 A (*klassisch*), LA 1100 A (*fondsgebunden*); LA 936 A and LA 1099 A were not located | no; the product page was read, the broker-hosted specimen was not re-found | **one read**: Alte Leipziger pm 2401, Tarif FR70 [S4] |
| Edition date | **10.15** for both | product page read 2026-08-30; specimen dated by its path to 02/2025 [unverified] | pm 2401 – 06.2026 |
| Asset form | **both** — general account and *Anlagestöcke* | hybrid: *Sicherungsvermögen* plus *Spezialfonds* | *fondsgebunden* |
| Guarantee level published | no | **yes** — 60 / 80 / 90 % of premiums paid, 80 % standard, quoted from the carrier's own page | 80 % on the variants named at [S16] |
| *Rentenfaktor* basis published | **yes** — DAV 2004 R at the tariff's *Rechnungszins*, 1,25 % p.a. on the 10.15 wording | expressed as a minimum annuity | a guaranteed factor of 24,94 € at 67 on NÜRNBERGER's *Muster*-PIB [S13] |
| Charge figure published | ***Muster*-PIB yes; its levels are template placeholders** | **yes** — 1 575 € *Abschlussprovision*; ≤ 0,95 € per 100 € of capital formed [unverified] | **yes** — NÜRNBERGER's full schedule and *Effektivkosten* of 1,77 pp [S13] |
| Layer sold on a common chassis | not established | **yes** — PrivatRente / BasisRente / RiesterRente are one design | not established |
| *Produktinformationsblatt* obtained | *Muster*-PIB yes, individual PIB no | no | *Muster*-PIB yes for NÜRNBERGER and WWK [S13] |

A range table needs two observations of one parameter, and after the retrieval pass the corpus has
two or three of several. What it had when this table was drafted was one:
**at least four Basisrente tariff wordings maintained in parallel at one carrier** [S1]
`[unverified]`. Everything else a variations table would normally carry — entry ages, minimum premiums, maximum
*Zuzahlung*, permitted *Rentenbeginn* range, *Rentengarantiezeit* durations, survivor-cover forms,
BUZ terms, *Effektivkosten*, guarantee levels beyond one carrier, *Mindestversicherungsleistung*,
fund universes — **has no observation at all in this corpus.** Gap 1.

**Representative design the research supports.** A single-life, individual, **klassisch**
Basisrentenvertrag on an annual grid, certified under § 5a AltZertG [R9]; premium a **level base
*Beitrag* plus an annual *Zuzahlung*** sized against the *Höchstbetrag* and rising with it
[R2] [R20]; priced and reserved at the **1,00 % *Höchstrechnungszins*** [R16] on a **DAV 2004 R**
first-order basis [R17]; *gezillmert* toward the **25 ‰** cap [R16]; surplus declared annually and
applied so that it stays inside the contract, with the terminal component allocated **only at
*Rentenbeginn*** [R15]; ***Rentenbeginn* at 67, floored at 62*** [R1] [R8]; conversion at
`max(garantierter, aktueller) Rentenfaktor` [R17]; a **monthly lifelong annuity and nothing else** —
**no *Kapitalwahlrecht*, no *Teilkapitalauszahlung*, no
*Rückkaufswert*, no policy loan, no assignment** [R1], and the *Kleinbetragsrenten-Abfindung* the
statute does allow left unimplemented as a `[std]` decision (mechanic 19); **death before *Rentenbeginn* pays nothing**
in the base run [R1]; and ***Beitragsfreistellung* as the only exit** [R14]. The optional modules,
off in the base run, are a **survivor's annuity** limited to spouse and *Kindergeld*-eligible
children [R1] and a **BUZ constrained to below 50 % of the total premium** [R1]. Every level the
corpus does not source — the *Rentenfaktor*, the charge levels, the minimum premium and annuity, the
*Beitragsfreistellung* rate, the eligible-survivor probability, the *Zuzahlung* share of the premium
— carries a `[std]` tag with its rationale beside it.

---

## Gaps and caveats

**Status after the retrieval pass of 2026-08-30.** Ten of the twenty-five items below were closed by
a retrieved document and four narrowed; each says so in its own words, and the item is kept rather
than deleted so that the history of the reading stays legible. The items still open are 12, 14, 15,
20, 21 and the parts of 1, 3, 6, 8, 11 and 23 that each identifies.

1. **Narrowed — four wordings now read, sixteen carriers still unreached.** Twenty named German life
   writers [S11] publish AVB, *Produktinformationsblätter* and *Verbraucherinformationen* for this
   product and **none of those twenty was reached**. What has been read since is two carriers'
   Basisrente AVB [S1] [S4], the GDV's Basisrente and BUZ *Musterbedingungen* [S12] and two
   filled-in *Muster*-PIBs [S13]. **No *Verbraucherinformation* of any carrier was opened.** Every
   parameter in the delib `basisrente` product-spec that would normally be sourced to a carrier is
   still `[std]` — the retrieval pass recorded evidence, it did not re-calibrate levels — and the
   variations table above is now a thin record of variation rather than a record of absence.

2. **Closed.** An *Effektivkosten* figure and a full charge schedule were both obtained. NÜRNBERGER's
   *Muster*-PIB gives *Effektivkosten* of **1,77 percentage points** and a complete charge schedule;
   WWK's gives **4,95** [S13]; and the Fraunhofer ITWM study puts realistic *Effektivkosten* for five
   large carriers' fund-linked Basisrenten at **1,0 – 1,5 pp** without a guarantee and **1 – 2,3 pp**
   with an 80 % one, against *Muster*-PIB figures of **3,0 – 4,6** [S16]. The distinction between the
   two — the *Muster*-PIB is computed on maximum permitted charges — is the substance of this item
   now. The charge table in mechanic 20 remains `[std]` because it was not re-derived.

3. **No market statistic of any kind was established.** Contract stock, new business, average
   contribution, the *klassisch*/*fondsgebunden* split, the *Beitragsfreistellung* rate, the buyer's
   age distribution and the distribution-channel split are all `[unverified]` general knowledge in
   mechanics 9 and 21, given as orders of magnitude. **Nothing downstream may cite a delib figure
   for the size of the Basisrente market.**

4. **Closed as to existence, open as to range.** One guaranteed *Rentenfaktor* level now exists in
   the corpus: **24,94 €** of monthly annuity per 10 000 € of capital at 67, on a 2025 fund-linked
   contract [S13]. No range and no time series exists, for this or any other delib product, so the
   worked example's choice stays `[std]`. **The 0 % conversion basis is withdrawn**: it was a
   Schicht-3 observation, and this carrier's own Basisrente wording strikes the factor on DAV 2004 R
   at the **tariff's** *Rechnungszins*, 1,25 % p.a. on the 10.15 edition [S1].

5. **Closed, in the affirmative.** The GDV publishes *Allgemeine Bedingungen für die
   Rentenversicherung gemäß § 10 Absatz 1 Nr. 2 Buchstabe b Doppelbuchstabe aa EStG
   (Basisrente-Alter)*, Stand 21.07.2025, a matching BUZ set and two *Muster-Standmitteilungen*, and
   all were retrieved [S12]. They are the spine this file was written without.

6. **Narrowed, not closed.** § 7 Abs. 2 AltZertG establishes that the individual PIB replaces the
   VVG-InfoV product information sheet and that **no § 154 VVG *Modellrechnung* is to be performed or
   attached** for a certified contract [R11]. Whether it also displaces the PRIIPs
   *Basisinformationsblatt* is **still not established**: no Basisrente KID was found at any carrier,
   which is consistent with the product sitting outside PRIIPs but does not prove it [S14].

7. **Closed.** § 7 Abs. 1 AltZertG lists fifteen mandatory PIB fields and § 7 Abs. 4 requires a
   *Muster*-PIB at 12, 20, 30 and 40 years; AltvPIBV § 5 puts the contract in **CRK 1 to 5** and § 10
   fixes the returns — 2/3/4/5/6 % for the *Effektivkosten* by CRK, and four scenarios per CRK for
   the projections (CRK 4: −1 %, 2 %, 5 %, 6 %) [R11]. Two filled-in sheets confirm the layout [S13].

8. **Narrowed.** **Whether the five-year spreading reaches a Basisrentenvertrag is answered**: the
   AltZertG's own rule (§ 1 Abs. 1 Satz 1 Nr. 8) does not reach it, but VVG § 165 Abs. 2 with § 169
   Abs. 3 does, and two wordings state it [R10] [R14] [S1] [S12] — with the qualification that a
   premium term shorter than five years shortens the spread. Still unsourced: the minimum recurring
   premium, the maximum *Zuzahlung*, whether *Zuzahlungen* enter the *Beitragssumme* for the 25 ‰
   cap, the *Mindestversicherungsleistung* that gates *Beitragsfreistellung*, the
   *Wiederinkraftsetzung* window and the permitted *Rentenbeginn* range. All `[std]`.

9. **Closed.** § 851c Abs. 2 ZPO as retrieved has **two** bands, not six: **6 000 €** a year to the
   completed 27th year of life and **7 000 €** to the completed 67th, with an aggregate ceiling of
   **340 000 €** and three tenths of any excess *Rückkaufswert* protected on top [R12]. The
   practitioner ladders contradicted each other because the graduated ladder was replaced by these
   two bands; the amounts are re-set every fifth year on 1 July, so any printed figure has a shelf
   life. The § 12 SGB II and § 90 SGB XII conditions are **still** unestablished [R13].

10. **Confirmed, and the caution stands.** § 851c Abs. 1 Nr. 1 ZPO reads "*nicht vor Vollendung des
    60. Lebensjahres*"; § 10 Abs. 1 Nr. 2 Buchst. b aa EStG reads "*nicht vor Vollendung des 62.
    Lebensjahres*", with § 10 Abs. 6 giving 60 for pre-2012 contracts [R1] [R12]. Different
    provisions, different histories; a downstream document must not merge them into one age.

11. **Narrowed.** The 2025 and 2026 *knappschaftliche* ceilings were read off the
    *Sozialversicherungsrechengrößen-Verordnungen* — **118 800 €** and **124 800 €** [R20] — and the
    rounding convention is the statute's own, § 10 Abs. 3 Satz 1 EStG's "*aufgerundet auf einen
    vollen Betrag in Euro*" [R2]. **The 2026 line is now the best-attested, not the least secure.**
    The 2023 and 2024 inputs were not retrieved and those two lines are still arithmetic alone.

12. **A possible fourth asset form — an index-linked Basisrente — was not established** [S10]. If it
    exists it is a bridge to delib product 4; acknowledge the possibility without asserting it.

13. **Closed.** BMF-Schreiben v. 24.05.2017 Rz. 29: "*Der Vertrag **darf zulassen**, dass die
    Ansprüche des Leistungsempfängers aus dem Vertrag unmittelbar auf einen nach § 5a AltZertG
    zertifizierten Vertrag ... des Leistungsempfängers auch bei einem anderen Unternehmen übertragen
    werden. Dabei ist lediglich die Übertragung innerhalb der jeweiligen Produktgruppe ... zulässig.
    Dieser Vorgang ist steuerfrei nach § 3 Nummer 55d EStG*" [R18]. So a transfer is **permitted but
    not compulsory**, tax-free, confined to the same product group, and the transferred capital is
    not a fresh contribution. Both market answers were observed: CosmosDirekt grants it free of charge
    on three months' notice [S1]; NÜRNBERGER and WWK exclude it on their PIBs [S13]. **It is a
    contract term, and downstream must say so rather than asserting a right.**

14. **The *Versorgungsausgleich* mechanism was not established** [R1]. Whether the division on
    divorce is effected by *interne* or *externe Teilung*, and what happens to the receiving
    spouse's entitlement, is unresolved. delib does not model it.

15. **Nothing Basisrente-specific was established from BaFin** [R21]. The product sits squarely in
    the conduct-supervision perimeter for capital-forming life products, and the supervisory
    material carried over from a sibling delib file is about the endowment chassis, not this layer.

16. **Closed on the reading, open on nothing that matters.** § 22 Nr. 1 Satz 3 Buchst. a
    Doppelbuchst. aa EStG applies to "*Rentenversicherungen im Sinne des § 10 Absatz 1 Nummer 2
    Buchstabe b*" without distinguishing Doppelbuchst. aa from bb, so a *BU-Rente* out of a
    *Basisrentenvertrag* is on the full cohort *Besteuerungsanteil*, not the *Ertragsanteil* of an
    *abgekürzte Leibrente* [R4]. That is the substance of the BUZ-versus-standalone-SBU comparison.

17. **Closed by observation.** The inference in mechanic 11 is now an observation at one carrier:
    CosmosDirekt's LA 1079 A applies the annual surplus to a *Bonussumme* through the whole
    *Aufschubzeit*, offers no cash-paying system before *Rentenbeginn*, and offers exactly two
    payout-phase systems — *jährliche Rentensteigerung (dynamische Rente)* and *Zusatzrente (flexible
    Rente)* [S1]. VVG § 153 Abs. 4 adds the statutory reason the terminal component falls at the end
    of the accumulation phase [R15].

18. **Closed — by the model conditions rather than by a carrier.** The GDV's BUZ *Musterbedingungen*
    for a Basisrente were retrieved [S12]. § 9 Abs. 2: "*Die Zusatzversicherung ist so gestaltet,
    dass stets mehr als 50 % der Beiträge auf Ihre Hauptversicherung entfallen*". § 9 Abs. 1: the
    rider forms a unit with the main contract and "*Spätestens mit dem vereinbarten
    Rentenzahlungsbeginn endet die Zusatzversicherung*". § 9 Abs. 3: a BUZ *Rückkaufswert* is never
    paid out but raises the main contract's benefits. **No carrier's own BUZ wording was reached.**

19. **Closed.** § 10 Abs. 1 Nr. 2 Satz 3 EStG expressly permits a contract to provide that "*bis zu
    zwölf Monatsleistungen in einer Auszahlung zusammengefasst werden*"; BMF Rz. 16 repeats it; the
    GDV model conditions § 1 Abs. 2 implement it as an insurer's right below an agreed monthly amount
    [R1] [R18] [S12]. The *Kleinbetragsrente* threshold is **1,5 % of the monthly *Bezugsgröße* of
    § 18 SGB IV** in the statute as amended in 2026, against the **1 %** the GDV text of July 2025
    still prints [R23] [S12] — both readings were right at different times. And a carrier does offer
    the *Abfindung*: CosmosDirekt LA 1079 A § 1 Abs. 2 [S1].

20. **Two further payout-side tax questions are unresolved** [R4]: the taxation of a
    *Hinterbliebenenrente* in the survivor's hands, including which cohort year fixes its
    *Besteuerungsanteil*; and the social-insurance treatment of the annuity in payment, where the
    difference between a compulsorily and a voluntarily insured pensioner is of the order of 18 % of
    the annuity and is stated in mechanic 16 without a source.

21. **No German market convention for the payment timing of the annuity was established** — whether
    the monthly instalment is *vorschüssig* or *nachschüssig*. The sibling delib file records the
    same gap for the Schicht-3 annuity. delib adopts monthly-in-advance as a `[std]` convention.

22. **The commissioning brief for this file stated the pre-2012 *Rentenbeginn* floor as 63; this
    file resolves it against 60.** The rule established here is: **62 for contracts concluded after
    31 December 2011, 60 for contracts concluded on or before that date** [R1] [R8]. Both figures
    are `[unverified]` in the sense that no source in this session confirmed them, but the 60/62
    split is settled German practice and 63 corresponds to no threshold in this statute. Recorded
    explicitly so that the discrepancy is resolved once, here, rather than propagating.

23. **Half closed.** The BMF circular is identified: **BMF vom 24.05.2017 (BStBl I S. 820), IV C 3 –
    S 2221/16/10001 :004 – 2017/0392623**, as amended by BMF v. 06.11.2017, 28.09.2021, 16.12.2021
    and 28.12.2023 [R18]. The BFH judgments are identified: **X R 33/19**
    (ECLI:DE:BFH:2021:U.190521.XR33.19.0) and **X R 20/19**, both of 19 May 2021 [R19]. **No
    *Bundesgesetzblatt* citation appears for the *Alterseinkünftegesetz* [R5], the
    *Wachstumschancengesetz* [R6], the *Jahressteuergesetz 2022* [R7] or the *Jahressteuergesetz
    2007* [R8]** — those are amending acts with no consolidated page of their own, none was retrieved,
    and none is guessed. Their **effects** are all now read in the consolidated law instead.

24. **Living texts.** DeckRV § 2 Abs. 1 as retrieved reads **1 Prozent** [R16]; the
    *Besteuerungsanteil* for a 2026 cohort is **84,0 %** from the statutory table [R4]; the
    *Höchstbetrag* for 2026 is **30 826 €** from the *Sozialversicherungsrechengrößen-Verordnung 2026*
    [R2] [R20]; the deductible share has been 100 % since 2023 on § 10 Abs. 3 Satz 6 [R7]; the
    full-taxation year is 2058 [R4]. **Every one of those moves.** A third mover was caught in the act
    by this pass: the *Kleinbetragsrente* threshold of § 93 Abs. 3 EStG stood at 1 % in model
    conditions of July 2025 and reads 1,5 % in the statute as amended in 2026 [R23]. Check all of
    them, and every paragraph number in this file, before relying on anything here.

25. **Narrowed — this file had no research channel while it was written, and has had one since.**
    Egress was blocked and the session's `WebSearch` budget was already exhausted when the product
    was reached. Two sibling delib research files, written while search was available, supplied
    [S1], [S2], and the carried-over material in [R14] through [R17] and [R21]; everything else in
    the drafted text rested on general knowledge, disciplined by the tagging rules in the
    retrieval-conditions section and by this register. **The pass of 2026-08-30 reached 21 of the 40
    entries and 17 of those now read `Retrieved: yes`** — every statute and regulation the product
    turns on, four carrier wordings and two *Muster*-PIBs — which is what closed or narrowed the
    fourteen items above. The nineteen entries with no `Retrieved:` line were not reached, and for
    them this item stands unaltered. **A reader who needs a figure in this file to be right must
    still check it against the instrument named beside it wherever the entry does not say
    `Retrieved: yes`.**
