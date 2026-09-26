# Sofortbeginnende private Rentenversicherung — research notes (Germany)

Research notes for the German **immediate payout annuity** — *sofortbeginnende private
Rentenversicherung*, commonly *Sofortrente*: a single *Einmalbeitrag* (single premium) is paid
once, and the insurer pays a *Leibrente* (life annuity) for as long as the annuitant lives,
beginning immediately. The annuity is *monatlich vorschüssig* (monthly in advance) in the market's
standard form, is guaranteed at a level struck at inception on the tariff bases, and is topped up
by a declared, non-guaranteed *Überschussrente*. The contract normally carries a
*Rentengarantiezeit* (guarantee period), may carry a *Kapital-* or *Beitragsrückgewähr* (refund of
the unconsumed single premium on death) and may carry a *Hinterbliebenenrente* (survivor's
annuity). It is a Schicht-3 (third-layer, unsubsidised private) contract, and its distinguishing
commercial feature is that its payments are taxed only on the *Ertragsanteil* — the small
statutory income fraction of § 22 EStG — which makes it the most lightly taxed regular income a
German private investor can buy.

**In scope.** The single-life and joint-life **payout** annuity bought with a single premium
outside any state subsidy: the determination of the guaranteed annuity from the *Einmalbeitrag*;
the *Rentengarantiezeit*; the death-benefit options (*Kapital-* / *Beitragsrückgewähr*,
*Hinterbliebenenrente* and its *Anwartschaft*); payment frequency and timing; the
short-*Aufschubzeit* variant; the *Überschussbeteiligung* in the *Rentenbezugsphase* and its four
*Überschussverwendung* forms; the *Rechnungsgrundlagen* (DAV 2004 R, the *Höchstrechnungszins*);
the impossibility of surrender once the *Rentenbezug* has begun; and the *Ertragsanteil*.

**Out of scope, and named here so the boundary is explicit.**

- **The accumulation phase of a deferred annuity.** *Klassische aufgeschobene private
  Rentenversicherung* is a separate delib product (`klassische_rentenversicherung`) with its own
  research file, and everything about premium accumulation, the *Deckungskapital* recursion, the
  *Rückkaufswert*, *Beitragsfreistellung* and the *Kapitalwahlrecht* belongs there. The two
  products meet at exactly one point and it is an important one: the *aktueller Rentenfaktor* a
  deferred contract converts at is, at two carriers, explicitly **the tariff the insurer is then
  writing for immediately beginning annuities** [S3] [S7]. The immediate annuity is therefore the
  *pricing primitive* of the deferred one, and this file is where that primitive is documented.
- **Schicht 1 (*Basisrente* / Rürup) and Schicht 2 (*Riester-Rente*, bAV).** Separate delib
  products or outside the library. Their payout phases run on the same machinery but are taxed
  completely differently — full *nachgelagerte Besteuerung* under § 22 Nr. 1 Satz 3 Buchst. a
  Doppelbuchst. aa EStG for Schicht 1 and § 22 Nr. 5 EStG for Schicht 2, against the
  *Ertragsanteil* here `[unverified]` — and their annuities may not be commuted or bequeathed. The
  *Sofortrente* is the only one of the three in which the policyholder owns the capital outright
  until the moment it is annuitised.
- **Fondsgebundene** and **indexgebundene** payout annuities, including the *fondsgebundene
  Sofortrente* expressed in *Renten-Bezugseinheiten*. Separate delib products; the classic
  general-account (*konventionell*) form is what is specified here.
- **Sterbegeldversicherung**, **Pflegerentenversicherung**, **Gruppenversicherung**, **private
  Krankenversicherung**, institutional pension-risk transfer, and the **gesetzliche
  Rentenversicherung** — the last referenced only where the consumer literature compares them.

These notes are the citation ground truth for the delib `sofortrente` product documents: source
ids **S1..S15** and **R1..R25** below are **frozen — never renumber**. Unused ids are simply
omitted downstream, leaving gaps, and `sources.md` records which ids are absent and why.

Access date for all citations: **2026-08-29**.

---

## Citation discipline and retrieval conditions

A delib citation was a weaker object than a citation in the four sister libraries, and the
difference is stated rather than glossed. This section has two halves: the conditions this file was
**drafted** under on 2026-08-29, and what the **re-verification** of 2026-08-30 established. The
first is kept because it is why every entry below reads as it does; the second is recorded document
by document in `products/sofortrente/sources.md`, which is the operative record for this product.

**No document listed in this file was retrieved when it was drafted.** Direct HTTP egress from the
build environment was blocked by an organisation network policy. `WebFetch` and `curl` were refused with HTTP 403
at the egress gateway for every host outside a short package-registry allowlist. The hosts that
mattered for this product were all tried across the delib build and all refused:
`gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`, `bundesfinanzministerium.de`,
`destatis.de`, `dejure.org`, `eur-lex.europa.eu`, `de.wikipedia.org`, and every insurer host named
below (`zurich.de`, `cosmosdirekt.de`, `nuernberger.de`, `debeka.de`, `allianz.de`,
`konzern-versicherungskammer.de`). **Nothing in this file rests on a document anyone opened.**

**A second, independent limit applied to this product.** The session's `WebSearch` budget — 200
calls, shared across the parallel delib researchers — was **already exhausted before work on this
product began**. Not one search was run for the *Sofortrente*, against a brief that anticipated
thirty to eighty; it was the worst-served of the ten. This is gap 1 and everything drafted in this
file follows from it.

What that meant, exactly, and it was applied without exception below:

1. **Every source entry records `Retrieved: no — egress blocked; no search corroboration (session
   search budget exhausted)`.** Nothing in *this* file is marked retrieved, then or now: these
   lines were left at their drafted status and the pass of 2026-08-30 is recorded in
   `products/sofortrente/sources.md` instead. **Where that file and an entry's line here disagree,
   that file governs.** Where an entry *does* carry
   corroboration it is corroboration recorded by a **sibling delib research file** whose searches
   ran earlier in the session — principally `_research/klassische_rentenversicherung.md`, which
   shares this product's *Rechnungsgrundlagen*, its surplus chassis and, at two carriers, its
   tariff. Those entries say so and name the sibling file's own source id: a traceable provenance
   chain, still one step weaker than a retrieval.
2. **No document reference number, URL, edition, page count or publication date was guessed.** A
   URL recorded by a sibling file from a search result is reproduced and attributed; the obvious
   canonical `gesetze-im-internet.de` form of a statutory provision is given and marked
   `[unverified]`; everywhere else the entry reads `URL: not established`.
3. **No verbatim quotation is invented.** A phrase in quotation marks below is one a sibling file
   recorded from a search summary, attributed to that summary rather than to the document.
4. **`[unverified]` is used generously.** Every specific paragraph number, date, amount, percentage,
   tariff level and market figure no search confirmed carries the tag — not the general shape of a
   well-established mechanic, but the moment a claim becomes *specific and numeric* it carries
   either a corroborated source or the tag.
5. **Uncertain numbers are `[std]` parameters, not citations.** This is the most consequential
   rule here, because the *Sofortrente*'s entire commercial character is a number — the euros per
   month per 100 000 € of *Einmalbeitrag* — and that number could not be established at any carrier
   for any year. Rather than guess it, section 4 **constructs** it from annuity mathematics on an
   explicitly stated proxy basis, prints the construction so a reader can reproduce it, and labels
   every resulting figure `[std]`. A `[std]` number with a printed derivation is honest; a
   fabricated `[S6]` number is not.

Where the corpus establishes a mechanic and not its level — the normal case here — the mechanic is
written long and the level is `[std]` with an argued range. The gaps register at the end is a
substantial part of this file's value, and a reader who needs a market figure should start there.

**The re-verification of 2026-08-30.** The network policy was lifted and the citations were checked
against the primary documents. Library-wide, all fifteen German instruments delib cites were read as
canonical XML from `gesetze-im-internet.de` with each law's amendment `Stand` recorded, 950 statutory
section references were checked and 950 were correct, and insurer AVB, *Verbraucherinformationen* and
*Produktinformationsblätter* were retrieved as PDFs and read; **501 of the library's 805 source
entries, 62 %, now read `Retrieved: yes`.** For this product the per-entry record is
`products/sofortrente/sources.md`, **where 19 of the 32 entries read `Retrieved: yes`, 12 read `no`
and one is mixed** — every insurer document in its S section was opened, as was every statutory
provision carried under its own `[R#]` ids. The twelve that stayed shut name what happened, and none
of them is a dead link: three are document classes with no public specimen, four are DAV material
that is not on the open web, one is sold rather than published, two are publisher series that were
not located, and two are research artefacts with no single document behind them.

**What a citation now means.** Where `sources.md` records a document as retrieved, it was opened and
the passage the entry rests on was read, with the edition, page count or statutory `Stand` recorded.
Where it does not, the citation is still **a pointer rather than a certificate**: it names the
instrument a claim must be checked against and does not assert that anyone checked it. **The
re-verification changed things** — it corrected claims this drafted text got wrong, the largest being
that the GDV publishes no model conditions for an immediate annuity, which the retrieved GDV index
refutes — and every correction is recorded at the entry in `sources.md` and in that file's provenance
note. What it did not change is the hole at the centre of the product: **one carrier's annuity scale
at one vintage is still the whole of the euros-per-month-per-100 000 € the corpus holds**, so section
4's construction and its `[std]` labels stand. Treat a claim here as sound where `sources.md` records
a retrieval, and as provisional where it does not.

---

## German terminology

German terms of art stay in German throughout the delib documents, italicised on first use with a
gloss. The vocabulary this product needs, beyond the shared annuity vocabulary of
`_research/klassische_rentenversicherung.md`:

| Term | Gloss |
|---|---|
| *Sofortrente* / *sofort beginnende Rentenversicherung* | immediate annuity: annuity payments begin at once, or after a short deferment |
| *Einmalbeitrag* | single premium: the whole consideration, paid once at inception |
| *Leibrente* | life annuity: payable for as long as the annuitant lives, and not one day longer |
| *Überschussrente* | the surplus-financed increment to the annuity in payment; declared, not guaranteed |
| *Rentenfaktor* | annuity factor: monthly annuity per 10 000 € of capital. For an immediate annuity the market more often quotes *Rente je 100 000 € Einmalbeitrag* |
| *vorschüssig* / *nachschüssig* | payable in advance / in arrears |
| *Sicherheitszuschlag* | the prudential margin that turns a best-estimate basis into a first-order one |
| *Trendfunktion* | the mortality-improvement function inside a generation table |
| *Rentengarantiezeit* | annuity guarantee period: payments continue to survivors if the annuitant dies inside it |
| *Kapitalrückgewähr* / *Beitragsrückgewähr* | refund on death of the *Einmalbeitrag* less the annuity instalments already paid |
| *Hinterbliebenenrente* | survivor's annuity, payable to a named second life after the annuitant's death |
| *Aufschubzeit* | deferment period: the gap between payment of the *Einmalbeitrag* and *Rentenbeginn* |
| *Überschussbeteiligung* | profit participation: the policyholder's share of the insurer's surplus |
| *Überschussverwendung* | the *use* the declared surplus is put to — the four payout-phase forms of section 9 |
| *konstante Überschussrente* | the form in which the total annuity is set once and intended to stay level |
| *steigende* / *dynamische Überschussrente* | the form in which the annuity starts low and rises each year with declared surplus |
| *teildynamische Überschussrente* | the intermediate form: part of the surplus taken up front, part left to finance increases |
| *Bonusrente* | surplus applied as a paid-up increment of annuity, permanently added to the payment |
| *Rechnungszins* | the technical interest rate in the tariff |
| *Höchstrechnungszins* (*Garantiezins*) | the statutory maximum *Rechnungszins* for new business, set in the *Deckungsrückstellungsverordnung* |
| *Ertragsanteil* | the taxable fraction of a private life annuity under § 22 EStG |
| *Bankauszahlplan* / *Entnahmeplan* | bank payout plan: a capital drawdown with a fixed term, the *Sofortrente*'s standard comparator |

---

## Primary sources

Fifteen entries, and the `Retrieved:` lines below record their **drafted** status. Only three were
then *documents whose existence and identity a search result actually returned* — [S2], [S4] and
[S6], all recorded by the sibling file `_research/klassische_rentenversicherung.md` while search was
still available, each with a URL a search returned. The remaining twelve were **known references**:
document classes and carriers that exist and are the right kind of thing to cite here, recorded so a
later build with a working retrieval channel would know what to fetch and in what order. They carry
no URL unless a sibling file recorded one, and nothing quantitative is cited from them here.
**That later build ran on 2026-08-30**: eleven of these fifteen were opened, and
`products/sofortrente/sources.md` carries what each yielded, with its edition and page count. The
four that were not are the *Produktinformationsblatt* [S11], the *Basisinformationsblatt* [S12], the
*Standmitteilung* [S15] — three document classes of which no carrier publishes a specimen — and the
carrier census at [S13], which has no single document behind it.

### S1 — GDV, "Musterbedingungen" service index, and the immediate-annuity model conditions
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin
- Doc type: publisher index page listing the association's *Musterbedingungen* (model general
  policy conditions) — the industry's shared drafting template, which individual insurers adopt,
  adapt or ignore
- URL: `https://www.gdv.de/gdv/service/musterbedingungen` — recorded by the sibling file
  `_research/klassische_rentenversicherung.md` [S3 there] from a search result
- Retrieved: no — egress blocked; no search corroboration in this session (budget exhausted);
  URL and taxonomy carried over from the sibling file's search record
- Content, and a **negative finding that matters**. The sibling file established from the index
  that the GDV maintains model conditions for (a) the deferred annuity; (b) the *Basisrente*;
  (c) a *fondsgebundene* Riester wrapper; (d) a non-unit-linked variant of the same, "Stand:
  21.07.2025"; and (e) the *Hinterbliebenenrenten-Zusatzversicherung* rider [S9]. **No model
  condition set for a *Rentenversicherung mit sofort beginnender Rentenzahlung* appears in that
  list.** Whether the GDV maintains one under a title the index did not surface, or whether the
  market drafts from the deferred template with the *Aufschubzeit* set to zero, **was not
  established** — gap 3. [S4] points to the second reading, but it is an inference.
- The GDV's standing disclaimer applies to the whole family: "Diese Bedingungen sind
  unverbindlich" — the wording is non-binding and its use optional [S1, via the sibling file's S2].
  Model conditions establish the **shape** of German wording, never an insurer's obligation.

### S2 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Sofort beginnende Rentenversicherung", Fassung 01/2022
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation* — the consolidated pre-contractual pack a German life insurer
  must supply under the VVG-Informationspflichtenverordnung [R17]: general information, the
  *Allgemeine Versicherungsbedingungen* (AVB), the special conditions for riders and options, and
  the tax notes. Document code **521331402 2501**.
- URL:
  `https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/222202101_sofort-beginnende-rentenversicherung_verbraucherinformationen_2022_01.pdf`
  — returned by a search recorded in the sibling file [S16 there]
- Retrieved: no — egress blocked; the document's existence, title, document code, vintage and URL
  are corroborated by the sibling file's search record; **no clause content was established from
  it**
- Content: **the single most important document to fetch for this product, and the only one whose
  identity is corroborated.** It is the immediate-annuity member of Zurich Deutscher Herold's
  *Verbraucherinformation für Konventionelle Versicherungen* series, whose deferred-annuity
  editions of 01/2021, 01/2022 and 01/2026 the sibling file records [S3]. "Konventionell" is the
  market's word for the general-account, non-unit-linked chassis, so the title alone establishes
  that this is the classic product and not a *fondsgebundene Sofortrente*. Its deferred siblings
  are structured as *allgemeine Informationen*, the AVB, *Besondere Bedingungen* per option,
  *allgemeine steuerliche Hinweise* and rider conditions [S3]; the immediate edition should carry
  the same shape with the accumulation material removed — **an expectation, not a finding**.
- **Fassung 01/2022** places this edition inside the **0,25 % *Höchstrechnungszins*** regime [R7],
  so any *Rentenhöhe* in it is a 0,25 %-era figure not comparable with a current quotation. Whether
  a 2025 or 2026 edition exists **was not established**.

### S3 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung", Fassung 01/2026
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation*, deferred annuity, document code **521331262 2601**
- URL:
  `https://www.zurich.de/-/media-assets/project/zurich-headless/germany/br/documents/verbraucherinformationen/32020_aufgeschobene-rentenversicherung_verbraucherinformationen_2026_01.pdf`
  — recorded by the sibling file [S4 there] from a search result
- Retrieved: no — egress blocked; content below is the sibling file's search record, reproduced
  with attribution
- Content: two of the three payout-phase facts the delib corpus establishes at clause level come
  from this deferred-annuity document, which is why it is a primary source here:
  - **The two-factor rule at *Rentenbeginn*.** The guaranteed *Rentenfaktor* is described as
    carefully calculated, and **at the start of annuity payments a second *Rentenfaktor* is
    compared with it, the higher of the two being guaranteed for the annuity payment period**. The
    "second factor" is the carrier's then-current immediate-annuity tariff [S7] — that is,
    **this product**. The deferred contract's upside is priced off the *Sofortrente* rate card.
  - ***Bewertungsreserven* participation continues in the *Rentenbezug*.** The transition to
    annuity payment is described as a key point for participation in *Bewertungsreserven*, and
    policyholders **also participate during the annuity payment period**, in accordance with the
    applicable VVG and supervisory provisions; the summary states that **§ 153 Abs. 3 VVG currently
    provides for equal (*hälftige*) participation** [R3].
  This is the only clause-level evidence in the delib corpus that surplus participation does not
  stop at *Rentenbeginn*, and it is load-bearing for section 9.

### S4 — NÜRNBERGER Lebensversicherung AG, AVB for the *Rentenversicherung mit sofort beginnender Rentenzahlung*, publisher document id `gn331303_p`
- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: *Allgemeine Bedingungen für die Rentenversicherung mit sofort beginnender
  Rentenzahlung* — an insurer's own AVB for exactly the product in scope
- URL: `https://www.nuernberger.de/medien/4allportal/gn331303_p.pdf` — the **document id
  `gn331303_p` was returned by a search** and is recorded by the sibling file [S9 there] as a
  sibling of tariff NIR3301's AVB; the URL is the carrier's established `4allportal` path form
  applied to that id and is `[unverified]` as a working address
- Retrieved: no — egress blocked; no search corroboration in this session; **document id
  corroborated, URL constructed, no clause content established**
- Content: **the only insurer AVB in the corpus whose title names this product.** The sibling
  file's search returned three members of one NÜRNBERGER AVB family: `gn331451_p` (deferred, *mit
  Rentengarantiezeit*, NIR3301) [S5], `gn331530_p` (*fondsgebunden*) and `gn331303_p` — this
  document. That they sit in one numbered family establishes what [S1] could not: German insurers
  draft the immediate annuity as **a member of the same AVB series as the deferred one**, not as a
  separate line. Nothing inside it was established; it is the first document a later build should
  fetch after [S2].

### S5 — NÜRNBERGER Lebensversicherung AG, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung und Rentengarantiezeit nach Tarif NIR3301", document id `gn331451_p`
- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: AVB for a deferred annuity **with *Rentengarantiezeit***, tariff **NIR3301**
- URL: `https://www.nuernberger.de/medien/4allportal/gn331451_p.pdf` — recorded by the sibling file
  [S9 there] from a search result
- Retrieved: no — egress blocked; content below is the sibling file's search record
- Content: recorded for two reasons. It is the **only document in the delib corpus whose title
  names the *Rentengarantiezeit***, establishing the guarantee period as a **tariff-level design
  feature carried in the product name**, not a rider bolted on — and the guarantee period is a
  payout-phase mechanic, so the evidence belongs here. And its summary established that **the
  contract value used for annuitisation includes any *Überschussbeteiligung* and
  *Bewertungsreserven*, subject to a minimum guaranteed contract value** — the deferred contract's
  version of the *Einmalbeitrag* this product starts from. No paragraph numbering established.

### S6 — Cosmos Lebensversicherungs-AG (CosmosDirekt), "Allgemeine Bedingungen für die Rentenversicherung", tariff LA 904 A
- Publisher: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland
- Doc type: *Allgemeine Bedingungen* (AVB) for a *Rentenversicherung*, tariff code **LA 904 A**
- URL:
  `https://www.cosmosdirekt.de/resource/blob/89106/31bbdccea1c7a5a530feb9e2a3be8d1c/allgemeine-bedingungen-rentenversicherung-la-904-a--data.pdf`
  — recorded by the sibling file [S8 there] from a search result
- Retrieved: no — egress blocked; content below is the sibling file's search record, reproduced
  with attribution
- Content: **the most quantitatively load-bearing document in the delib annuity corpus, and the
  only one that names a conversion basis.** A search summary returned the clause in terms:
  **"The annuity factor determined at the beginning of the contract is calculated on the basis of
  a recognised mortality table (currently DAV 2004 R) and an underlying interest rate (currently 0
  percent p.a.)."** For this product that sentence establishes three things:
  1. the mortality basis of a German annuity tariff is **DAV 2004 R** [R10];
  2. the interest basis of a *guaranteed* annuity factor can be set **below** the statutory
     *Höchstrechnungszins* — at this carrier, at this vintage, at **0 % p.a.** — so the guarantee
     is priced as though the insurer will earn nothing on the annuity fund. That is the
     *Sicherheitszuschlag* made concrete on the interest side;
  3. the factor is fixed **at inception**, which for a *Sofortrente* means it is fixed once and
     never revisited, because inception and *Rentenbeginn* are the same date.
- The same summary returned the standard surplus disclaimer: **"the amount of profit sharing
  depends on many influences which are unpredictable and only limitedly controllable by the
  company, with the most important influencing factor being capital-market developments."**
- **The vintage of LA 904 A was not established**, and the clause is time-stamped by its own word
  *currently*. Siblings in the house numbering (LA 1204 A and LA 1201 A, both 11.22; LA 1005 A;
  LA 1311 A; LA 1100 A; LA 1081 A) make LA 904 the oldest number in the series, so the "0 percent"
  reading may belong to the 0,25 % era. See gap 6.

### S7 — Allianz Lebensversicherungs-AG — the immediate-annuity tariff statement, and the Allianz immediate-annuity product documents
- Publisher: Allianz Lebensversicherungs-AG, Stuttgart
- Doc type: (a) the "Vorsorgekonzept KomfortDynamik" product page, recorded by the sibling file
  [S13 there] from a search result; (b) Allianz's own *Sofortrente* product documents —
  *Produktinformationsblatt*, AVB, *Basisinformationsblatt* — **not established**
- URL: (a) `https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/`, recorded by the
  sibling file; (b) not established
- Retrieved: no — egress blocked; (a) is the sibling file's search record; (b) is a known
  reference only
- Content: (a) carries the second, independent statement of the fact that makes this product the
  pricing primitive of the deferred one — **"the calculation bases at *Rentenbeginn* … relate to
  the interest rate and mortality table that the company uses at that time for immediately
  beginning annuities."** Read with [S3]'s two-factor rule, the pair establishes the convention:
  the *aktueller Rentenfaktor* of any deferred German annuity **is** the carrier's current
  *Sofortrente* tariff. The same page establishes that the ***Rentengarantiezeit* "can be set to a
  minimum"** — a selectable parameter with a contractual floor.
- (b) Allianz is the largest German life writer and certainly sells an immediate annuity against
  *Einmalbeitrag*, commonly named *Allianz SofortRente* `[unverified]`; no document, tariff code,
  envelope or rate was established. Fetching its PIB and BIB is the second-highest-value action for
  a later build, after [S2].

### S8 — Debeka Lebensversicherungsverein a. G. — AVB series B LV, and the "Privatrente" product page
- Publisher: Debeka Lebensversicherungsverein a. G., Koblenz
- Doc type: AVB in the house **B LV** series (e.g. **B LV 85**, and the more recent **B LV 100**
  of 01.07.2026 and **B LV 101** of 01.01.2025, both in the *betriebliche Altersversorgung*
  folder and out of scope), plus the insurer's *Privatrente* product page
- URLs: `https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf`
  and `https://www.debeka.de/privatkunden/vorsorgensparen/zukunftalter/privatrente.html` — both
  recorded by the sibling file [S11] [S12 there] from search results
- Retrieved: no — egress blocked; content below is the sibling file's search record
- Content: two facts carry over. Debeka's own definition of the accumulation quantity — **the
  *Deckungskapital* is the sum of the contributions accumulated at the *Rechnungszins*, insofar as
  they are not required for risk and expense cover** — degenerates for a single premium to "the
  *Einmalbeitrag* less the loadings", section 2's *Nettoeinmalbeitrag*. And the tax statement from
  the product page: **if a lifelong monthly annuity is chosen, only part of the payout is taxed —
  the comparatively low *Ertragsanteil*, depending on age at *Rentenbeginn*** [R13]. **Whether
  Debeka writes a stand-alone *Sofortrente* was not established.**

### S9 — GDV, "Allgemeine Bedingungen für die Hinterbliebenenrenten-Zusatzversicherung zur Rentenversicherung"
- Publisher: GDV
- Doc type: *Musterbedingungen* for the **survivor's-annuity rider**
- URL:
  `https://www.gdv.de/resource/blob/6336/942f7b9aec6a969b486ec205279870a3/allgemeine-bedingungen-fuer-die-hinterbliebenenrenten-zusatzversicherung-zur-rentenversicherung-mit-aufgeschobener-rentenzahlung-0-pdf-data.pdf`
  — recorded by the sibling file [S10 there] from a search result. Note that the URL slug names
  the **deferred** annuity; whether a separate model set exists for the immediate annuity's
  survivor's rider was **not established**.
- Retrieved: no — egress blocked; no clause content established
- Content: establishes the single structural fact this file needs about the *Hinterbliebenenrente*:
  **the German market treats the survivor's annuity as a *Zusatzversicherung* — a rider with its
  own condition set, attached to the base contract rather than being a benefit of it.** That has a
  direct modelling consequence (section 7): the survivor's annuity is a **separate module, off in
  a reference implementation's base run**, with its own *Anwartschaft* period, its own insured life
  and its own reserve, rather than a term in the main annuity's benefit formula.

### S10 — Konzern Versicherungskammer, "Überschussverteilung 2026"
- Publisher: Konzern Versicherungskammer, the Bavarian public-sector insurance group; the `BL_`
  path prefix indicates the Bayerische Landesbrandversicherung / Bayern-Versicherung life entity
- Doc type: the annual ***Überschussverteilung*** document — how a German life insurer publishes
  its declared *Überschussanteilsätze* for a year, by tariff generation and by phase
- URL: `https://www.konzern-versicherungskammer.de/dam/jcr:acf4c857-3b53-4521-a108-d1fb9b1cec67/BL_Ueberschussbeteiligung_2026.pdf`
  — recorded by the sibling file [S15 there] from a search result
- Retrieved: no — egress blocked; **the title and the 2026 vintage are corroborated; nothing
  inside the document was established**
- Content: **the** primary source class for every surplus rate a projection of this product needs —
  the *laufende Verzinsung*, the *Grundüberschussanteil*, the *Zinsüberschussanteil* on the
  *Deckungsrückstellung* of annuities in payment, and the *Überschussrentensatz* that converts
  declared surplus into euros of monthly annuity. **No rate, no percentage and no component split
  was established, for any carrier, for any year** — gap 4, and the reason every surplus parameter
  downstream is `[std]`.

### S11 — *Produktinformationsblatt* (PIB) for a sofort beginnende Rentenversicherung — document class
- Publisher: each insurer, individually
- Doc type: the short pre-contractual product summary required by German insurance-distribution
  law [R17]. For an annuity it states on one or two pages the *Einmalbeitrag*, the *garantierte
  Rente*, the *Gesamtrente* including declared surplus, the *Rentengarantiezeit*, the death benefit
  and the costs
- URL: not established, for any carrier
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: **known reference only** — and the class that would settle almost every quantitative gap
  here at a stroke, because a PIB for a *Sofortrente* prints the guaranteed and total annuity for a
  stated *Einmalbeitrag* and age, the exact figure section 4 must construct. **Not one was
  located**; a later build should fetch three or four across carrier types first.

### S12 — *Basisinformationsblatt* (PRIIP-KID) for a sofort beginnende Rentenversicherung — document class
- Publisher: each insurer, individually
- Doc type: the three-page key information document required by the PRIIPs Regulation for
  insurance-based investment products, with its standard sections — product description; risks and
  return, carrying the *Risikoindikator* and four performance scenarios; issuer default; *Welche
  Kosten entstehen?*, carrying the *Renditeminderung* figures; and the holding period
- URL: not established, for any carrier
- Retrieved: no — egress blocked; no search corroboration
- Content: **known reference only, with a scope question attached.** Whether a classic
  *Sofortrente* falls inside PRIIPs was **not established**: it looks like an insurance-based
  investment product on the usual reading, but its payout-only character and the absence of a
  surrender value after *Rentenbeginn* [R1] make the holding-period and "what you might get back"
  sections awkward. If a BIB exists it is the **only** public document giving a cost figure in the
  standardised *Renditeminderung* form — the most useful charge datum a model could have. Gap 8.

### S13 — Carriers writing the product, recorded without documents
- Publishers: Allianz [S7]; R+V; Debeka [S8]; Generali and its direct arm CosmosDirekt [S6];
  Dialog; HDI; Alte Leipziger; LV 1871; Continentale and its direct arm Europa; NÜRNBERGER [S4]
  [S5]; Swiss Life; Zurich Deutscher Herold [S2] [S3]; ERGO; AXA; Barmenia; Hannoversche;
  Württembergische; Gothaer; Stuttgarter [S14]; Volkswohl Bund; Baloise; Universa; DEVK; Signal
  Iduna; Provinzial; HUK-Coburg; Konzern Versicherungskammer [S10]; Mecklenburgische [S14]
- Doc type: none — carrier names only
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Content: **a list of where to look, and nothing more.** The *Sofortrente* is a commodity product
  in Germany: most of the carriers above write one, and comparison portals rank them on the single
  dimension of *Rentenhöhe*. **No carrier's product name, tariff code, envelope, rate or document
  was established here**, so this file contains **no insurer-level quantitative comparison at all**
  (gap 2). Naming a carrier asserts only that it is a German life insurer of the right kind; it
  does not assert that it sells this product today.

### S14 — Stuttgarter Lebensversicherung a. G. and Mecklenburgische Lebensversicherungs-AG — further pre-contractual packs
- Publishers: Stuttgarter Lebensversicherung a. G.; Mecklenburgische Lebensversicherungs-AG
- Doc types: "Allgemeine Informationen zu einem Altersversorgungssystem" (Stuttgarter);
  "Vertragsinformationen für die Private Rentenversicherung mit flexiblem …" (Mecklenburgische,
  product "Rente flex", title truncated in the search record)
- URLs: `https://www.stuttgarter.de/documents/209195/221255/Allgemeine_Infos_Altersversorgungssystem_SLV.pdf/2657ea66-2bfa-9cec-04d2-8f72ac9731bd?t=1604038997833`
  and `https://www.mecklenburgische.de/pdfs/produkte/vertragsinformationen/Vertragsinformationen-zu-Leben/rente-flex_vertragsinformationen.pdf`
  — both recorded by the sibling file [S18] [S14 there] from search results
- Retrieved: no — egress blocked; no clause content established from either
- Content: recorded to establish that ***Verbraucherinformation*, *Vertragsinformationen* and
  *Allgemeine Informationen* are three names for the same pre-contractual pack**, so a later build
  searching for one should search for all three. The Stuttgarter URL's `?t=1604038997833` parameter
  is a millisecond timestamp corresponding to **October/November 2020**. The Mecklenburgische title
  is truncated after "mit flexiblem", so its feature — most plausibly a flexible *Rentenbeginn*,
  which would make it a neighbour of the *Aufschubzeit* variant of section 3 — is **not
  established**.

### S15 — The annual *Standmitteilung* and *Rentenanpassungsmitteilung* in the *Rentenbezug* — document class
- Publisher: each insurer; the GDV publishes a *Muster-Standmitteilung*
- Doc type: the annual statement a German life insurer must send. For a contract in the
  *Rentenbezug* it reports the *garantierte Rente*, the current *Überschussrente*, the resulting
  *Gesamtrente*, and — under a rising *Überschussverwendung* — the increase taking effect at the
  anniversary
- URL: not established for the payout form; the sibling file records the GDV
  *Muster-Standmitteilung* for the **endowment** at `_research/kapitallebensversicherung.md`
- Retrieved: no — egress blocked; no search corroboration
- Content: **known reference only**, and the direct evidence of what a *Rentenanpassung* does — up,
  flat or down — the question section 9 turns on. **No specimen was located and no anniversary
  adjustment was established, at any carrier, for any year.**

---

## Regulatory and actuarial references

Twenty-five entries, and as above the `Retrieved:` lines record their **drafted** status. The
statutory ones carry the canonical `gesetze-im-internet.de` address where that form is unambiguous,
marked `[unverified]` because no search in this session returned it; the professional and market ones
carry a URL only where a sibling delib file recorded one. **None had been retrieved when this section
was written.** A provision's *content* is stated as what it provides, in this file's own words, and
its paragraph number carries `[unverified]` unless a sibling file's search corroborated it. **The
pass of 2026-08-30 read every statutory provision this product turns on as canonical XML at a
recorded `Stand`**, and `products/sofortrente/sources.md` says which; what it could not reach is the
DAV material, which is distributed to members rather than published, and the ratings and statistical
series. Where that file records a reading, the paragraph number is no longer `[unverified]`.

### R1 — VVG § 168, *Kündigung des Versicherungsnehmers* — and the rule that ends surrender at *Rentenbeginn*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__168.html` — canonical form, `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: **the provision that decides the most important modelling question about this product.**
  § 168 VVG governs the policyholder's right to terminate a life contract. The paragraph that
  matters is **§ 168 Abs. 3 VVG**, which provides that **in a *Rentenversicherung* without a
  *Kapitalwahlrecht* the right of termination exists only up to the start of the annuity payments**
  `[unverified]` — after *Rentenbeginn* there is no right to terminate and so no *Rückkaufswert* to
  pay. For a *Sofortrente*, whose *Rentenbeginn* is at or within weeks of inception, **the contract
  is irrevocable from the outset**.
- The paragraph number, the scope of the "*ohne Kapitalwahlrecht*" qualifier and the treatment of a
  contract with a *Kapitalwahlrecht* exercisable during a short *Aufschubzeit* are `[unverified]`.
  The **substance** is not seriously in doubt: it is the uniform statement of the consumer
  literature [R21] [R23] and the economic precondition for writing life annuities at all. Gap 9.

### R2 — VVG § 169, *Rückkaufswert*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` — recorded by the sibling file
  [R1 there] as returned by a search
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: the general surrender-value provision — the insurer must pay the *Rückkaufswert* on the
  policyholder's termination; for unit-linked contracts the value is the *Zeitwert* on recognised
  actuarial rules; paragraphs 3 to 5 carry the calculation rules and the five-year spreading of
  *Abschluss- und Vertriebskosten* `[unverified]`. **Recorded for its boundary**: § 169 is displaced
  by § 168 Abs. 3 [R1] the moment the *Rentenbezug* begins, so a `Sofort_DE_S` model publishes **no
  surrender-value cells and no lapse decrement** — a specification, not an omission.

### R3 — VVG § 153, *Überschussbeteiligung*, and § 153 Abs. 3, *Beteiligung an den Bewertungsreserven*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — recorded by the sibling files
  [R4 in the RV file, R1 in the KLV file] as returned by searches
- Retrieved: no — egress blocked; content is the sibling files' search record
- Content: the statutory right to participate in surplus. The policyholder is entitled to a share
  of the *Überschuss* and of the *Bewertungsreserven* unless excluded by express agreement; the
  surplus must be determined by a method appropriate under recognised actuarial principles; and
  **§ 153 Abs. 3 currently provides for equal (*hälftige*) participation in the *Bewertungsreserven***
  [S3]. Two consequences: participation is a **statutory right, not a marketing feature**, and it
  **does not stop at *Rentenbeginn*** [S3]. Its level is at the insurer's discretion within the
  statutory minimum [R15], which is why every surplus figure downstream is `[std]`.

### R4 — VVG § 163, *Anpassung der Prämie oder der Vertragsbestimmungen*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` — canonical form, `[unverified]`
- Retrieved: no — egress blocked; established at commentary level only, from the sibling file
  [R3, R17 there]
- Content: the statutory channel by which a German life insurer may change a contract term after
  conclusion — successor to the contractual *Treuhänderklausel*. The sibling file establishes from
  commentary that **the *Treuhänderklausel* survives only in older contracts and that a guaranteed
  *Rentenfaktor* can today be changed only under § 163 VVG**, and that the **Landgericht Köln** held
  **the low-interest phase not a sufficient ground, being entrepreneurial risk that cannot be
  passed to policyholders** (case reference, date and parties **not established**). Here the
  provision is close to inert: the guaranteed annuity is struck once at inception on bases then
  fixed for life. A delib model treats the *garantierte Rente* as **immutable** and records § 163
  as a model risk.

### R5 — VVG § 165, *Prämienfreie Versicherung*, and § 166, *Kündigung des Versicherers*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` — recorded by the sibling file
  [R2 there] as returned by a search
- Retrieved: no — egress blocked
- Content: § 165 gives the policyholder of a contract with recurring premiums the right to convert
  it to a premium-free contract, the reduced benefit being derived from the surrender value on the
  premium basis and tabulated per insurance year, subject to a *Mindestversicherungsleistung*
  threshold. **Recorded purely for its boundary**: a *Sofortrente* is bought with a single
  *Einmalbeitrag*, so there is no future premium to cease and **§ 165 has no application to this
  product at all**. A reference implementation carries **no `Beitragsfreistellung` decrement**, and
  that is a specification rather than a simplification.

### R6 — VVG §§ 150, 159, 160 — *versicherte Person*, *Bezugsberechtigung*, *Auslegung der Bezugsberechtigung*
- Publisher: Bundesministerium der Justiz / juris
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__150.html`,
  `.../__159.html`, `.../__160.html` — canonical forms, all `[unverified]`
- Retrieved: no — egress blocked; no search corroboration
- Content: the provisions that make the *Rentengarantiezeit* and the *Hinterbliebenenrente* work as
  contract law. § 150 distinguishes the *Versicherungsnehmer* from the *versicherte Person* and
  requires the insured person's consent where another life is insured above a threshold; § 159
  gives the right to designate a *Bezugsberechtigter*, revocably or irrevocably; § 160 supplies
  default construction rules. All three `[unverified]` as to number and content. They matter
  because payments made *after* the annuitant's death go to a **designated beneficiary**, not
  automatically to the estate, and the designation is a live element the policyholder may change.
  A model treats the beneficiary as a pass-through.

### R7 — Deckungsrückstellungsverordnung (DeckRV) § 2 — the *Höchstrechnungszins*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/deckrv/__2.html` — recorded by the sibling file
  [R7 there] as returned by a search
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: the statutory maximum technical interest rate for new German life business. Established
  points: the rate was **0,25 %** before 2025 and is **1,00 % from 1 January 2025**, and the 2025
  increase was **the first increase since 1994** — every earlier move having been downwards. The
  DAV recommended **1,0 % for 2026 as well** [R8]. **The intermediate sequence — 4 %, 3,25 %,
  2,75 %, 2,25 %, 1,75 %, 1,25 %, 0,90 %, 0,25 % — and every effective date in it is
  `[unverified]` here**; a model point carrying a legacy *Rechnungszins* must cite the delib
  cross-product reference library rather than this file.

### R8 — DAV recommendations on the *Höchstrechnungszins* for 2025 and 2026
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV), Cologne
- URL: not established; the sibling file [R8, R9 there] records the two press items by title —
  "Deutsche Aktuarvereinigung empfiehlt auch für 2026 einen Höchstrechnungszins in Höhe von 1,0
  Prozent" and "Deutsche Aktuarvereinigung begrüßt Ministeriumsvorstoß zum Höchstrechnungszins
  2025"
- Retrieved: no — egress blocked; titles corroborated by the sibling file's search record
- Content: the profession's recommendations, which the *Bundesministerium der Finanzen* converts
  into the DeckRV figure. Establishes that **1,0 % was recommended for 2026** as well as applying
  from 2025, so a contract written in 2026 sits on the same interest basis as one written in 2025 —
  which matters here, where tariff vintage and contract vintage are the same thing. The DAV's
  methodology and any figure inside the releases are **not established**.

### R9 — GDV media information on the *Höchstrechnungszins* increase
- Publisher: GDV; and HDI, "Höchstrechnungszins in der Lebensversicherung steigt zum 01.01.2025"
- URL: not established; titles recorded by the sibling files [R10, R11 there; R16 in the KLV file]
- Retrieved: no — egress blocked
- Content: the industry's framing of the 2025 increase as "eine angemessene Reaktion auf gestiegene
  Zinsen", and a carrier's customer-facing note of the same change; both corroborate the
  **1 January 2025** effective date. **No figure for the effect on annuity levels was established
  from either** — the figure this product most needs; gap 5.

### R10 — DAV, "Herleitung der DAV-Sterbetafel 2004 R für Rentenversicherungen"
- Publisher: Deutsche Aktuarvereinigung e. V.
- Doc type: *DAV-Richtlinie* — the profession's derivation guideline for the annuity table
- URL: not established; the sibling file [R12 there] records the document and its 2023 reissue
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: **the mortality basis of this product.** Established from the sibling file:
  - DAV 2004 R is a ***Generationentafel***: mortality is given per **birth cohort**, and the
    expected future improvement is **inside the table**, not applied on top of it.
  - Its **component structure** is: a **base table of second order**; a **base table of first
    order**; a **mortality trend of second order**; a **mortality trend of first order**; and an
    **age adjustment (*Altersverschiebung*) with a base table**. The trend is therefore a named,
    separately-parameterised object — the *Trendfunktion* — and it exists in both a best-estimate
    and a prudent version.
  - **First-order probabilities are used for premiums and reserves and carry safety margins
    relative to the second-order ("realistic") probabilities, in order to assess the risk
    prudently**; the **second-order base tables represent the best estimate of period mortality in
    1999 for insured lives, as three-dimensional selection tables**. For an annuity, "prudent"
    means **lower** mortality than best estimate: the first-order basis assumes annuitants live
    longer, which raises the annuity value and lowers the annuity bought by a given
    *Einmalbeitrag*.
  - **Dates**: in use since **June 2004**, intended for new business from **2005**, the DAV
    document dated **22 February 2005**; the derivation guideline was **reissued on 28 June 2023**.
    That the profession was still maintaining DAV 2004 R in 2023 — nineteen years after first use,
    twenty-four years after its 1999 base year — is itself the evidence that **no successor annuity
    table has displaced it**.

### R11 — DAV 2004 R-Bestand and the *Rentenbestandstafel* RBx
- Publisher: Deutsche Aktuarvereinigung e. V.
- URL: not established
- Retrieved: no — egress blocked; the pairing is recorded by the sibling file [R14 there] from a
  2004 presentation titled "DAV 2004 R und RBx"
- Content: the corpus establishes **that a companion in-force table exists and nothing more.**
  DAV 2004 R is the **new-business** table; the ***Bestand*** variant is the table for the
  **existing annuity book**, reflecting the different composition and selection history of
  annuities already in payment. **The distinction between "DAV 2004 R" and "DAV 2004 R-Bestand"
  is established only as a naming pairing**; the difference in level, in trend, in age range or in
  application rule was **not established** and nothing about it may be asserted downstream — see
  gap 12. For a *Sofortrente* the distinction is nevertheless conceptually central: a contract is
  priced on the new-business table at inception and then, for the whole of its long life, sits in
  the *Bestand* to which the other table applies.

### R12 — Contemporaneous expositions of DAV 2004 R
- Publishers: Deutsche Gesellschaft für Versicherungs- und Finanzmathematik (DGVFM); General
  Reinsurance AG; the *qx-Club* actuarial seminar series
- URL: not established; the sibling file [R14 there] records presentations of **16 August 2004**,
  **14 September 2004** and a reinsurer's exposition of **27 October 2004**
- Retrieved: no — egress blocked
- Content: the profession's contemporaneous explanation of the table, where the
  *Sicherheitszuschlag* structure and the trend construction were set out for practitioners.
  **No content was established** beyond the presentations and their dates. These are what a later
  build should fetch to substantiate anything specific about the first-order margin.

### R13 — EStG § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb — the *Ertragsanteil* table
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` — recorded by the sibling file [R5
  there] as **returned directly by a search**
- Retrieved: no — egress blocked; the general content below is the sibling file's search record;
  the table values in section 15 are from general knowledge and are `[unverified]`
- Content, as established by the sibling file:
  - Payments from private annuity contracts, and from life contracts converted into a classic
    monthly *Leibrente*, are taxed on the ***Ertragsanteil*** basis.
  - **Only the "Ertrag des Rentenrechts"** — the interest component contained in the annuity from
    the beginning of the payout phase — **is subject to tax**. The return-of-capital element is not
    income at all.
  - **The *Ertragsanteil* is determined by the annuitant's age at *Rentenbeginn*.** The earlier the
    annuity begins, the longer its expected duration, and **the higher the taxable fraction**.
  - **For an annuity commencing at age 65 the *Ertragsanteil* is 18 % of the annuity.** This is
    the only value of the statutory table that any delib search corroborated.
  - The statutory address usually given for the table — **§ 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst.
    bb EStG** — was **not** confirmed by any search summary and is `[unverified]`.

### R14 — EStG § 20 Abs. 1 Nr. 6 — the *Kapitalabfindung* regime, and its boundary
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — recorded by the sibling file [R6
  there]
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: the regime that taxes a **lump sum** from a life or annuity contract. The
  *Halbeinkünfteverfahren* — half the *Ertrag* taxable, half exempt — applies where the "12/62
  rule" is met: **the contract must have run at least 12 years and the payment must occur after
  completion of the 62nd year of life**, and the contract must be one in which the capital option
  **cannot be exercised before 12 years** from conclusion. **The method applies only to lump-sum
  payments and to multiple capital withdrawals under a payout plan; it does not apply to monthly
  annuity payments.** Contracts concluded before 1 January 2005 retain the earlier treatment.
- **Recorded here for its boundary, and the boundary is sharp.** A *Sofortrente* bought at, say,
  age 65 has by construction **not** run twelve years when its first payment falls due, so § 20
  Abs. 1 Nr. 6 could never apply to it favourably even if it paid a lump sum. It pays no lump sum
  in any event. **The whole of a *Sofortrente*'s cash flow is taxed under § 22 [R13] and none of it
  under § 20** — which is precisely the tax arbitrage the product is sold on, and the reason a
  *Sofortrente* is compared with a *Bankauszahlplan* whose interest is taxed in full at the
  *Abgeltungsteuer* rate (section 17).

### R15 — Mindestzuführungsverordnung (MindZV)
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/mindzv/` — canonical form, `[unverified]`
- Retrieved: no — egress blocked; recorded at existence level by the sibling file [R6 in the KLV
  file]
- Content: the regulation fixing the **minimum share of each surplus source that must be credited
  to policyholders** — the floor beneath the insurer's discretion under § 153 VVG [R3]. It
  operates separately on the *Kapitalanlageergebnis* (investment result), the *Risikoergebnis*
  (mortality and biometric result) and the *übriges Ergebnis* (expense and other result), and it
  permits deductions for the *Sicherungsbedarf* arising from legacy guarantees [R16]. **No
  percentage in the regulation was established by any delib search** — the commonly quoted
  90 % / 90 % / 50 % structure is `[unverified]` and does not appear here as a figure. For this
  product MindZV matters because **the annuitant's *Risikoergebnis* is a longevity result**: when
  annuitants die faster than the first-order table assumed, the *Risikoüberschuss* is positive and
  a minimum share of it must flow back into the *Überschussrente*.

### R16 — VAG §§ 138–140 — *Überschussbeteiligung*, *Sicherungsbedarf*, and the *Zinszusatzreserve*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vag_2016/__139.html` — canonical form, `[unverified]`
- Retrieved: no — egress blocked; recorded at existence level by the sibling file [R8 in the KLV
  file]
- Content: the supervisory side of the surplus rules — the *Rückstellung für
  Beitragsrückerstattung* (RfB), the conditions for drawing it down, and the *Sicherungsbedarf*
  deduction; the ***Zinszusatzreserve*** built against legacy guarantees on a *Referenzzins*
  mechanism belongs to the same complex. **Nothing specific was established**: not the paragraph
  numbers, not the *Referenzzins* formula, not the ZZR's size in any year, not whether it is now
  being released. Recorded because a *Sofortrente*'s *Überschussrente* is paid from the same RfB
  the ZZR competes with, which makes the release profile a first-order driver of what a cohort of
  annuitants actually receives — and it is entirely `[unverified]` here.

### R17 — VVG-Informationspflichtenverordnung (VVG-InfoV), and the PRIIPs Regulation
- Publisher: Bundesministerium der Justiz / juris; European Union
- URLs: `https://www.gesetze-im-internet.de/vvg-infov/` — canonical form, `[unverified]`; the
  PRIIPs Regulation (Regulation (EU) No 1286/2014) `[unverified]` as to number
- Retrieved: no — egress blocked; the VVG-InfoV *Effektivkosten* point is recorded at existence
  level by the sibling file [R9 in the KLV file]
- Content: the two disclosure regimes that generate [S11] and [S12]. VVG-InfoV § 2 lists the
  pre-contractual information a German life insurer must supply — the source of the
  *Verbraucherinformation* class [S2] [S3] [S14] — and carries the ***Effektivkosten*** disclosure.
  The PRIIPs Regulation generates the *Basisinformationsblatt* [S12] with its *Risikoindikator*,
  four performance scenarios and *Renditeminderung* figures; the DAV maintains a standard method
  for category 4 products (*Ergebnisbericht* of **1 July 2025**, per the sibling KLV file).
  **Whether either regime's cost disclosure reaches a payout-only *Sofortrente* was not
  established** — gap 8 — and **no cost figure was established at any carrier.**

### R18 — BaFin material on life-insurance product oversight
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht (BaFin)
- URL: not established; the sibling KLV file [R17, R18, R19 there] records **Merkblatt 01/2023 (VA)
  *zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden Lebensversicherungsprodukten***,
  the *Risiken im Fokus 2026* section on "Kosten von kapitalbildenden Lebensversicherungen", and
  *Fachartikel* including "Wenn Lebensversicherungen zu viel kosten" (2022) and "Kundennutzen im
  Fokus" (2024)
- Retrieved: no — egress blocked
- Content: the supervisor's *Wohlverhaltensaufsicht* (conduct supervision) of life products —
  value-for-money expectations, cost scrutiny, the *Kundennutzen* framing. **All of it is addressed
  to *kapitalbildende* products, i.e. the accumulation side.** Whether BaFin has published anything
  on payout annuities, and whether it scrutinises *Rentenhöhe* or surplus declarations for value,
  **was not established**.

### R19 — GDV / dieversicherer.de, "Private Rentenversicherung: Auszahlmöglichkeiten"
- Publisher: GDV, under its consumer brand *Die Versicherer*
- URL: `https://www.dieversicherer.de/versicherer/altersvorsorge/news/auszahlung-private-rentenversicherung-141750`
  — recorded by the sibling file [R21 there] from a search result
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: the industry association's own consumer account of a private annuity's payout options,
  part of the result set behind section 9's surplus taxonomy, and the closest thing in the delib
  corpus to an authoritative German-industry statement of the annuity-versus-lump-sum choice.
  **No rate and no envelope was established from it.**

### R20 — Franke und Bornberg, "Altersvorsorge: Überschüsse im Rentenbezug — Teil 1: Die Qual der Wahl", and "Was bedeutet der Rentenfaktor und wie hoch ist er?"
- Publisher: Franke und Bornberg GmbH, Hannover — independent product-rating house
- URLs: `https://www.franke-bornberg.de/blog/altersvorsorge-ueberschuesse-im-rentenbezug-teil-1-die-qual-der-wahl`
  and `https://www.franke-bornberg.de/de/blog/was-bedeutet-rentenfaktor-wie-hoch-2021-2022` —
  recorded by the sibling file [R19 there] from search results
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: **the professional source behind section 9.** The first title is explicitly about
  ***Überschüsse im Rentenbezug*** — the exact subject of this product — and is "Teil 1" of a
  series whose further parts were not located; it is the rating house's treatment of the choice
  between the *Überschussverwendung* forms. The second is its *Rentenfaktor* article, dated by its
  slug to **2021/2022**. **Neither returned a level, a range or a table**: the question the second
  title asks — "und wie hoch ist er?" — was answered by nothing any delib search returned. Gap 5.

### R21 — Consumer-organisation material on the *Sofortrente*
- Publishers: Finanztip Verbraucherinformation gemeinnützige GmbH; Stiftung Warentest
  (*Finanztest*); the *Verbraucherzentralen*
- URLs: `https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/`
  and `https://www.finanztip.de/lebensversicherung-versteuern/` — recorded by the sibling file
  [R20 there] from search results. **Finanztip's, Stiftung Warentest's and the Verbraucherzentrale's
  *Sofortrente*-specific pages were not located and no URL for them is given.**
- Retrieved: no — egress blocked
- Content: from the two located Finanztip pages the sibling file established the surplus taxonomy
  used in section 9 — the *konstant* / *teildynamisch* / *volldynamisch* division, and the
  observation that **under the constant system the annuity can still fall, because if the insurer
  earns less than expected the surplus-financed part is reduced** — plus the 12/62 rule [R14].
  **Stiftung Warentest's periodic *Sofortrente* comparison is the single most valuable unlocated
  document for this product**: the market's standard published table of guaranteed and total
  monthly annuities per 100 000 € by carrier, which would settle gaps 2, 5 and 7 together. Its
  existence is `[unverified]`; no issue, date, price point or ranking is claimed.

### R22 — Assekurata, "Marktstudie Überschussbeteiligungen und Garantien"
- Publisher: Assekurata Assekuranz Rating-Agentur GmbH, Cologne
- URL: not established; the sibling KLV file [R25 there] records the **24. Marktstudie
  "Überschussbeteiligungen und Garantien 2026"**
- Retrieved: no — egress blocked; the title and 2026 edition number are the sibling file's search
  record
- Content: the market's annual survey of declared surplus rates — the document that aggregates
  what [S10] publishes carrier by carrier. A **24th edition** dates the series to the early 2000s
  and marks it as the standard reference. **No rate, no average, no range and no payout-phase
  breakdown was established from it.** Locating it is the third-highest-value action for a later
  build, after [S2] and Stiftung Warentest [R21].

### R23 — Comparison-portal and broker cluster specific to the *Sofortrente*
- Publishers: `vergleich-sofortrente.de`; `lifefinance.de`; Verivox; CHECK24; and the broader
  German broker-blog cluster the sibling file records as [R24] there —
  `versicherungenmitkopf.de`, `fragfina.de`, `gn-finanzpartner.de`, `finanzkueche.de`,
  `compeon.de`, `financedoor.de`, `versicherung-vergleiche.de`, LV 1871's and NÜRNBERGER's own
  wiki pages, `vr.de`, `ruv.de`
- URLs: the two product-specific hosts `vergleich-sofortrente.de` and `lifefinance.de` were
  returned inside the sibling file's [R24] publisher list; **no individual page URL for either was
  recorded**, and none is given here
- Retrieved: no — egress blocked; no search corroboration in this session
- Content: **the class of source that would supply the price points this file lacks, and did not.**
  A German *Sofortrente* portal exists precisely to rank carriers by monthly annuity per 100 000 €
  for a stated age and option set, and `vergleich-sofortrente.de` is by its domain name dedicated
  to that. **Nothing from it was established.** What the wider cluster did establish, through the
  sibling file, is this file's definitional material: the *Rentenfaktor* arithmetic and the
  guaranteed/current distinction; the *Rentengarantiezeit* mechanics, durations and cost
  illustration (section 5); the *Zinsüberschuss* definition; the *Bonusrente* mechanic; and the
  *Ertragsanteil*. Every fact drawn from it is corroborated by at least two members, and none is a
  price.

### R24 — The unisex rule: CJEU *Test-Achats* and its German application
- Publisher: Court of Justice of the European Union; the German *Allgemeines
  Gleichbehandlungsgesetz* (AGG) and the VVG's implementing provisions
- URL: not established
- Retrieved: no — egress blocked; **no delib search touched this topic at all**
- Content: **`[unverified]` in both directions, a known reference only.** The established German
  position is that tariffs written from **21 December 2012** must be **unisex** while the
  profession's tables, DAV 2004 R among them, are built **sex-distinctly**. Neither half was
  corroborated by any delib search. The tension bites hardest on this product: a *Sofortrente* is
  the purest longevity bet in the market, female annuitants are materially longer-lived, and a
  unisex tariff on sex-distinct tables must be struck on an assumed **portfolio sex mix** no
  insurer publishes. The rule belongs to
  `references/regulatory-and-actuarial-references.md` and must be cited from there. Gap 13.

### R25 — GDV statistics on *Einmalbeiträge* and the German annuity market
- Publisher: GDV
- URL: not established; the sibling KLV file [R20, R21 there] records "Die deutsche
  Lebensversicherung in Zahlen 2024" and the statistical series "Neugeschäft und Bestand der
  Lebensversicherer für die letzten zehn Geschäftsjahre"
- Retrieved: no — egress blocked
- Content: the industry statistics that would size this product. The GDV series separates
  ***Einmalbeiträge*** from *laufende Beiträge* in new business — but that line aggregates
  *Sofortrenten* with single-premium endowments, bAV contributions and *Zuzahlungen*, so even a
  retrieved figure would not isolate this product. **No figure of any kind was established**, so
  there is **no sourced number anywhere in this file for the size of the German *Sofortrente*
  market, the contracts in force, the average *Einmalbeitrag* or the average purchase age** —
  gap 7.

---

## Extracted facts, organised by mechanic

This is the section the `sofortrente` product-spec and technical-notes are written from. It is
long because the corpus establishes this product's **mechanics** well and its **levels** hardly at
all, and because the house rules direct that the weight of a delib research file goes here rather
than into the source list. Every quantitative statement below is either tagged to a source or
marked `[std]` with its derivation printed.

### 1. Product structure, legal form and the Schicht-3 placing

- A *Sofortrente* is an ordinary German **life insurance contract** (*Lebensversicherung*) under
  the VVG, written on the insurer's general account (*Sicherungsvermögen*), in the classic
  (*konventionell*) non-unit-linked form [S2] [S6]. It is not a banking product, not an investment
  fund and not a *Sparplan*, and the difference is the whole point: it transfers
  *Langlebigkeitsrisiko* to the insurer.
- **Structure in one line:** one payment in at inception; a stream of payments out until death,
  floored by the *Rentengarantiezeit* or *Kapitalrückgewähr* and lifted by the *Überschussrente*.
- **The parties.** The *Versicherungsnehmer* (policyholder) contracts and pays; the *versicherte
  Person* (annuitant) is the life the annuity depends on; a *mitversicherte Person* may be named
  for the *Hinterbliebenenrente* (section 7); a *Bezugsberechtigter* receives whatever falls due
  after death [R6]. Usually the first three are one person; where they are not, the *versicherte
  Person* must consent [R6] `[unverified]`.
- **Schicht 3.** No *Sonderausgabenabzug*, no *Zulage*, no state certification: nothing is
  deductible going in and only the *Ertragsanteil* is taxable coming out [R13]. That symmetry is
  the product's tax logic, and the reason it is bought with money already taxed — an inheritance, a
  property sale, a matured endowment, a severance payment, or a *Kapitalwahlrecht* lump sum.
- **Non-participating it is not.** The contract carries the statutory *Überschussbeteiligung* of
  § 153 VVG [R3] throughout the payout phase, *Bewertungsreserven* included [S3]. A model treating
  the annuity as a fixed guaranteed stream models less than half the payment.

### 2. The *Einmalbeitrag* and the issue rules

- **One premium, paid once, at inception.** There is no premium stream, no *Beitragsdynamik*, no
  *Ratenzahlungszuschlag* and no premium-payment decrement. A projection of this product has
  exactly one inflow, at `t = 0`.
- The insurer deducts the acquisition and administration loadings from the *Einmalbeitrag* and
  annuitises the remainder. Debeka's own definition of the accumulation quantity — **the
  *Deckungskapital* is the sum of the contributions accumulated at the *Rechnungszins*, insofar as
  those contributions are not required for risk and expense cover** [S8] — degenerates for a single
  premium to a single netting step:

  ```
  Nettoeinmalbeitrag = Einmalbeitrag x (1 - alpha)
  ```

  where `alpha` is the *Abschluss- und Vertriebskosten* charge expressed as a fraction of the
  *Einmalbeitrag*. **No value of `alpha` was established at any carrier** — see section 12 and
  gap 8.
- **Entry ages.** Nothing was established. The product is sold at and around retirement, with a
  typical purchase window in the sixties and issue into the eighties at some carriers — **all
  `[unverified]`**. A reference implementation adopts **60 to 85** as `[std]`: below 60 the
  *Ertragsanteil* is high enough (section 15) to weaken the tax case, and above 85 the
  *Rentengarantiezeit* options collapse. The boundaries claim to be no carrier's.
- **Minimum and maximum *Einmalbeitrag*.** Nothing established. The market convention is a
  five-figure minimum — the fixed per-policy administration cost would swamp a small annuity — with
  an upper limit set by reinsurance rather than tariff. `[std]`: minimum **10 000 €**, working
  range **25 000 € to 500 000 €**, representative case **100 000 €**, the last because it is the
  unit German annuities are quoted in (section 4). See gap 7.
- **Underwriting.** A *Sofortrente* is normally written **without medical underwriting**, because
  the exposure runs the wrong way — medical evidence would be used by the applicant, not the
  insurer. **Not established by any source**; `[unverified]`. Its converse, the impaired-life
  *enhanced annuity*, is **not established to exist in the German retail market** at all and
  nothing here asserts it does.

### 3. The *Aufschubzeit* variant

- The market sells a hybrid: the *Einmalbeitrag* is paid now and the annuity begins **after a short
  deferment**, typically one to fifteen years — an *aufgeschobene Rentenversicherung gegen
  Einmalbeitrag*, a *Sofortrente mit Aufschub*, or simply the *Aufschubzeit* option of the same
  tariff. **No carrier's terms were established**; the Mecklenburgische "Rente flex" [S14] is the
  corpus's only candidate and its feature is unestablished.
- **Three things happen during an *Aufschubzeit* and must not be conflated**: interest accrues at
  the *Rechnungszins*, so more capital is annuitised; **mortality accrues**, so the survivors share
  the fund of those who died — the survivorship credit that makes deferral powerful, and the reason
  the deferment death benefit is a first-order design question; and the annuity starts at an older
  age, so `ä_x` is smaller for two reasons at once.
- **The death benefit during the *Aufschubzeit* is what the variant turns on.** Two forms exist: a
  **pure deferred annuity** with no death benefit, the fund of those who die being forfeited to the
  survivors; and a *Beitragsrückgewähr* form refunding the *Einmalbeitrag* on death before
  *Rentenbeginn*, which is much the more common retail form. **Neither was established for this
  product**; the pairing carries over from the deferred-annuity file.
- **Order of magnitude of the deferral effect**, on the `[std]` proxy basis of section 4 at 1,00 %,
  purchase at exact age 65, *Einmalbeitrag* 100 000 €, monthly annuity in advance:

  | Deferment | Annuity, no death benefit in deferment | Annuity, with full *Beitragsrückgewähr* in deferment |
  |---|---|---|
  | 0 years | 407.98 € | 407.98 € |
  | 2 years | 451.43 € | 444.07 € |
  | 5 years | 532.48 € | 508.12 € |
  | 10 years | 732.64 € | 651.24 € |

  All eight figures are `[std]` (1): arithmetic on a stated proxy basis, gross of charges, and
  **not** any carrier's quotation. A five-year deferment raises the annuity by about **25 %** with
  a death benefit and **31 %** without, and the gap between the columns — 4,6 % at five years,
  11,1 % at ten — **is the price of the death benefit**, which is the honest way to show it.

### 4. *Rentenhöhe*: how the annuity is determined, and how it moves with the *Höchstrechnungszins*

**The determination.** The guaranteed monthly annuity is the *Nettoeinmalbeitrag* divided by the
value of a monthly life annuity-due on the tariff bases, with the annuity administration loading
applied:

```
R_garantiert = Einmalbeitrag x (1 - alpha) / ( 12 x a12(x, i) x (1 + beta) )

  a12(x, i)  monthly annuity-due factor at attained age x and Rechnungszins i,
             on the first-order DAV 2004 R basis for the annuitant's birth cohort  [S6] [R10]
  alpha      Abschluss- und Vertriebskosten as a fraction of the Einmalbeitrag     [std]
  beta       administration loading on each annuity payment                        [std]
```

- **The mortality basis is DAV 2004 R** and it is named in an insurer's own AVB: the annuity factor
  is calculated "on the basis of a recognised mortality table (currently DAV 2004 R)" [S6] [R10].
- **The interest basis need not be the *Höchstrechnungszins*.** The same clause continues "and an
  underlying interest rate (currently 0 percent p.a.)" [S6] — a carrier pricing a *guaranteed*
  annuity factor at zero interest while the statutory maximum was positive. For a *Sofortrente*
  that choice is less likely than for a deferred contract, because here the guarantee is given for
  a stream starting today rather than in thirty years, but the clause establishes that the tariff
  rate is the insurer's choice **at or below** the cap [R7], never automatically the cap.
- **The market's quoting unit is the euro per 100 000 €**, not the *Rentenfaktor* per 10 000 € the
  deferred market uses. The two are one number scaled by ten: a *Rentenfaktor* of 40,80 and an
  annuity of 408 € per 100 000 € say the same thing `[std]`.

**The `[std]` proxy basis.** No annuity level was established at any carrier for any year (gap 5),
so this file **constructs** one. Mortality: a Gompertz–Makeham proxy `mu(x) = A + B c^x` with
**A = 0.0002, B = 1.5e-5, c = 1.10**, calibrated so the curtate-plus-half life expectancy is
**24.29 years at 65**, 16.63 at 75 and 10.46 at 85; sample rates `q(65) = 0.00789`,
`q(75) = 0.02001`, `q(85) = 0.05078`, `q(95) = 0.12617`. That is a **prudent annuitant** shape of
the right order for a first-order German basis; it is **not** DAV 2004 R, which is not public and
is not redistributed here [R10]. Monthly-in-advance via `a12 = a_due - 11/24`. Interest at three
regimes — **0,25 %** (pre-2025), **1,00 %** (from 1 January 2025) and **1,75 %** as an illustrative
higher rate [R7] [R8]. Charges **excluded**, so the figures are gross values, not quotations.

**Annuity per 100 000 € of *Einmalbeitrag*, monthly in advance, gross of charges** `[std]` (2):

| Age at *Rentenbeginn* | i = 0,25 % | i = 1,00 % | i = 1,75 % | uplift 0,25 % → 1,00 % |
|---|---|---|---|---|
| 60 | 314.43 € | 352.08 € | 391.63 € | +12.0 % |
| 65 | 369.64 € | 407.98 € | 447.93 € | +10.4 % |
| 70 | 443.58 € | 482.84 € | 523.40 € | +8.9 % |
| 75 | 544.89 € | 585.32 € | 626.75 € | +7.4 % |
| 80 | 687.02 € | 728.86 € | 771.44 € | +6.1 % |

The corresponding annuity-due factors `a12(x, i)` at 1,00 % are 23.669, 20.426, 17.259, 14.237 and
11.433, so a reader can check any cell as `100 000 / (12 x a12)`.

**How it has moved with the *Höchstrechnungszins*.** This is the question the brief asks and the
table answers it structurally rather than empirically:

- The *Höchstrechnungszins* fell for thirty years to **0,25 %** and rose to **1,00 % on 1 January
  2025** — the first increase since 1994 [R7] — with the DAV recommending 1,0 % again for 2026
  [R8].
- On the `[std]` basis, that single step is worth about **+10 %** on the guaranteed annuity at age
  65 and **+12 %** at age 60, tapering to **+6 %** at 80: the younger the annuitant, the longer the
  stream, the more the discount rate matters. A 65-year-old buying in 2025 rather than 2024 gets,
  on this arithmetic, roughly one extra euro of guaranteed monthly annuity for every ten they
  previously got `[std]` (2).
- **The direction is not in doubt and the magnitude is `[std]`, not observed.** The mechanism is
  established from the tariff formula itself [S6] and from the statutory rate history [R7] [R8];
  **no carrier's before-and-after quotation was established** (gap 5). Real quotations will differ
  from this table in both directions because carriers price below the cap [S6], because their
  first-order mortality margin is heavier or lighter than this proxy, and because charges are
  excluded here.
- **Two forces offset the interest uplift over longer horizons**: continuing improvement inside
  the *Trendfunktion* [R10] raises annuity values for each successive cohort, and any strengthening
  of the first-order margin does the same. Two cohorts buying ten years apart at the same
  *Rechnungszins* would not get the same annuity.

**What is guaranteed.** The *garantierte Rente* computed at inception is guaranteed **for life**
and is not adjustable: § 163 VVG is the only channel, it is narrow, and the courts have narrowed it
further [R4]. Everything above the guaranteed annuity is the *Überschussrente* of section 9 and is
**not** guaranteed.

### 5. *Rentengarantiezeit*

- **Mechanic.** A guaranteed payment period running from *Rentenbeginn*. If the annuitant dies
  inside it, **the annuity continues to be paid to the beneficiaries until the agreed number of
  years has expired** — the corpus's illustration is a 10-year period with death after 6 years, the
  spouse receiving the remaining 4 [R23]. If the annuitant survives it, it lapses and the annuity
  continues for life. Afterwards nothing is payable on death unless a *Kapitalrückgewähr* (section
  6) or a *Hinterbliebenenrente* (section 7) was also bought.
- **Durations offered**: **5, 10, 15, 20, 25 or more than 30 years**; **typical durations 15 years
  for retirement ages 61–70 and 10 years for 71 and above**; **most policyholders choose 10 to
  20 years** [R23]. It is carried in the tariff name at NÜRNBERGER, whose deferred AVB is titled
  "… mit aufgeschobener Rentenzahlung **und Rentengarantiezeit** nach Tarif NIR3301" [S5], and it
  is a policyholder-selectable parameter with a contractual floor at Allianz — the guarantee period
  "can be set to a minimum" [S7]. A *Sofortrente* with **no** guarantee period is therefore a
  configuration, not the default.
- **Two settlement forms exist on death inside the period**: the instalments continue as they fall
  due, or the present value of the *Restgarantiezeit* is commuted to a lump sum. **Which form
  German carriers use, and on what basis a commutation would be struck, was not established** —
  gap 10. A reference implementation pays the instalments, the form [R23] describes.
- **Cost of the guarantee**, computed on the `[std]` proxy basis of section 4 at 1,00 % interest,
  age 65, per 100 000 € `[std]` (3):

  | *Rentengarantiezeit* | `a12` | Monthly annuity | Reduction vs no guarantee |
  |---|---|---|---|
  | none | 20.426 | 407.98 € | — |
  | 5 years | 20.530 | 405.92 € | 0.51 % |
  | 10 years | 20.897 | 398.78 € | 2.26 % |
  | 15 years | 21.624 | 385.38 € | 5.54 % |
  | 20 years | 22.821 | 365.16 € | 10.50 % |
  | 25 years | 24.591 | 338.87 € | 16.94 % |
  | 30 years | 26.972 | 308.97 € | 24.27 % |

- **The cost rises steeply with age, because the guarantee bites sooner.** On the same basis, a
  10-year guarantee costs **2.26 %** of the annuity at 65, **4.10 %** at 70 and **7.42 %** at 75; a
  20-year guarantee costs **10.50 %**, **17.20 %** and **26.71 %** at those three ages `[std]` (3).
  That is why the market's typical duration falls with age — 15 years to 70, 10 years thereafter
  [R23].
- **A cross-check.** The sibling corpus records a consumer illustration on a *deferred* contract —
  200 €/month over 30 years producing 573 €/month with no guarantee — in which a 10-year guarantee
  costs **3 €**, a 20-year **15 €** and a 30-year **46 €**, i.e. roughly **0,5 %, 2,6 % and 8,0 %**
  [R23]. Materially cheaper than the table above at every duration, which is what one would expect:
  that annuity starts at a lower age with a longer expected duration, so a fixed guarantee covers a
  smaller share of it. Consistent in shape, different in level for a stated reason; **neither is a
  tariff**.
- **Modelling consequences.** During the guarantee period the payment is **certain**, so `pols_if`
  must not be decremented against it; after it, the payment is contingent on survival. A model that
  applies survival probabilities across the whole stream understates the liability, and one that
  applies none overstates it. This is a listed pitfall for the delib `Sofort_DE_S` model.

### 6. *Kapitalrückgewähr* / *Beitragsrückgewähr* on death

- **Mechanic.** On death the insurer refunds the *Einmalbeitrag* **less the annuity instalments
  already paid**, floored at zero — so the benefit starts at the full *Einmalbeitrag* and runs to
  nothing over roughly the period in which the annuitant recovers the capital nominally: on the
  `[std]` basis of section 4, about **21,5 years** at age 65, i.e. to about age 86 `[std]` (4).
- Variants named in the German market: ***volle Beitragsrückgewähr*** (the full unconsumed
  *Einmalbeitrag*), and forms in which only a stated percentage is refunded or in which the refund
  is capped at a number of years' payments. **No carrier's variant was established.**
- **It overlaps with the *Rentengarantiezeit* and is usually an alternative to it.** Both protect
  against early death — the guarantee period with a fixed number of payments, the refund with a
  declining lump sum. A buyer who takes both pays for both. **Which carriers permit the combination
  was not established** — gap 10.
- **Cost of the refund**, on the `[std]` proxy basis of section 4 at 1,00 %, age 65, per
  100 000 €: the monthly annuity falls from **407.98 €** to **335.48 €**, a reduction of
  **17.8 %** `[std]` (5). That is a large price, materially larger than a 20-year guarantee period
  (10.5 %), and it is the honest answer to a buyer who asks why the "money-back" version pays so
  much less. The computation solves for the annuity `R` satisfying

  ```
  Einmalbeitrag = 12 x R x a12(65, i) + PV( max(Einmalbeitrag - 12 x R x t, 0) payable on death at t )
  ```

  with deaths taken at mid-year and the refund discounted from mid-year.
- **A design trap the model must respect.** Because the refund is `Einmalbeitrag − instalments
  paid`, and because a *larger* refund means a *smaller* annuity, and a smaller annuity means the
  refund runs off more slowly, the equation above is **implicit in `R`** and must be solved, not
  evaluated. An implementation that computes the plain annuity first and then subtracts a refund
  cost gets a different — and wrong — answer.
- **Whether the refund counts the *guaranteed* or the *total* annuity paid** is a live contractual
  question, **not established** at any carrier, and the two readings diverge materially over twenty
  years. A reference implementation uses the **guaranteed** annuity as `[std]` (11), on the argument
  that a guaranteed benefit cannot be defined by reference to a discretionary quantity — a
  modeller's argument, not a carrier's. Gap 10.

### 7. *Hinterbliebenenrente* and its *Anwartschaft*

- **Mechanic.** A second life — the *mitversicherte Person*, in practice the spouse or registered
  partner — is named at inception. While the annuitant lives, the main annuity is paid and the
  survivor holds an ***Anwartschaft***: a contingent, not-yet-payable entitlement. On the
  annuitant's death, if the second life is then alive, the *Hinterbliebenenrente* begins and is
  paid for the second life's remaining lifetime. If the second life predeceases the annuitant, the
  entitlement lapses and **nothing is refunded** — the cover has been consumed.
- The German market treats it as a ***Zusatzversicherung*** — a rider with its own condition set —
  and the GDV publishes model conditions for exactly that [S9]. The direct modelling consequence:
  in a reference implementation it is a **separate module with its own insured life, off in the
  base run**, not a term in the main annuity's benefit formula.
- **Typical percentages** of the main annuity: 60 % and 100 % are the market's two standard
  levels `[unverified]`; other percentages exist. **No carrier's menu was established.**
- **This makes the contract a joint-life-last-survivor annuity**: the liability runs until **both**
  lives are dead, and the second life's age and sex matter as much as the annuitant's. The second
  life is fixed at inception and generally **cannot be substituted** — a later marriage does not
  acquire the entitlement `[unverified]`.
- **Cost**, on the `[std]` proxy basis of section 4 at 1,00 %, annuitant aged 65 and second life
  aged 62 on the same mortality proxy, per 100 000 € `[std]` (6):

  | Survivor's percentage | `a12` (joint) | Monthly annuity | Reduction |
  |---|---|---|---|
  | none | 20.426 | 407.98 € | — |
  | 60 % | 23.838 | 349.58 € | 14.3 % |
  | 100 % | 26.113 | 319.12 € | 21.8 % |

  The proxy applies the same mortality to both lives and assumes independence, both of which are
  simplifications: real joint-life pricing uses sex-distinct or portfolio-mix bases (section 11)
  and a dependence allowance. **These are `[std]` illustrations, not tariff values.**

### 8. Payment frequency and timing

- **The annuity is monthly.** Every description in the delib corpus treats the private annuity as a
  monthly payment [S7] [R23], and the *Sofortrente*'s whole commercial proposition is a monthly
  income replacing a salary. Quarterly, half-yearly and annual frequencies exist as options
  `[unverified]`; no carrier's menu, and no loading or discount for choosing one, was established.
- ***Vorschüssig*** — payable **in advance**, at the start of each payment period — is the German
  market convention for annuities in payment, and every arithmetic in this file uses an
  annuity-**due**. **No source in the delib corpus states it in terms**, for this product or for
  the deferred one, and the sibling file records the same gap [gap 19 there]. It is therefore a
  `[std]` convention here with the gap stated beside it, not an established fact — see gap 11.
- **The parameter is first-order, which is why the gap matters.** Advance against arrears moves the
  annuity value by roughly half a month's interest **and** shifts every payout cash flow by one
  period. On the `[std]` basis at 1,00 %, `a12_due − a12_arrears = 1`, so the annuity per
  100 000 € at age 65 would be `100 000 / (12 x 19.426) = 428.99 €` on an arrears basis against
  `407.98 €` in advance — a **5,1 %** difference from a single convention `[std]`.
- **The first payment date** falls at or within a month of inception; **whether the convention is
  the day the *Einmalbeitrag* is received or the first of the following month was not
  established**. A reference implementation pays the first instalment at `t = 0`, as `[std]`.

### 9. *Überschussbeteiligung* in the *Rentenbezug* — the four *Überschussverwendung* forms

**The two-part payment.** The annuity paid is `garantierte Rente + Überschussrente`. Only the first
is a promise; the second is declared annually out of surplus actually earned and can move down as
well as up. The sibling corpus states the same for the deferred product's payout phase: the insurer
sets a value at the start "composed of the *Garantierente* and a surplus share projected for the
whole annuity period" [R21], and only the guaranteed part is a promise.

**The four forms.** Carriers offer a choice of ***Überschussverwendung*** for the payout phase, made
at *Rentenbeginn* — here **at inception, once, irrevocably** `[unverified]` [R19]:

| Form | Mechanic | Payment stream |
|---|---|---|
| **konstante Überschussrente** | The insurer fixes the total annuity at *Rentenbeginn* from the *garantierte Rente* plus a surplus share **projected for the whole annuity period**, and intends to hold it level [R21] | Highest at outset; flat thereafter **in intention only** |
| **steigende (volldynamische) Überschussrente** | The annuity **adjusts annually and flexibly to the actual surplus development** [R21] | Lowest at outset; rises each year that surplus is declared |
| **teildynamische Überschussrente** | Part of the expected surplus is applied under the constant system and part under the dynamic system, so the annuity rises regularly by a **fixed percentage** provided the insurer earns corresponding surpluses [R21] [R23] | Intermediate at outset; rises at a stated rate, subject to surplus |
| **Bonusrente** | Declared surplus **buys a paid-up increment of annuity**, permanently added to the payment: "the ongoing surplus shares are used partly for an age-dependent *Überschussrente* and partly for an additional premium-free annuity (*Bonusrente*)" [R23] | Ratchets: each increment, once bought, does not come back off |

- **The *Bonusrente* is the mechanism underneath the rising forms, not a fourth alternative.** That
  is the corpus's reading [R23]: what makes a *volldynamische Rente* **ratchet rather than
  fluctuate** is that its increments are bought as paid-up annuity. A carrier may market
  *Bonusrente* as an option in its own right; a model treats it as the crediting mechanism and the
  three dynamics as the profile.
- **The constant form is not actually constant, and this is the single most important thing to
  understand about the product.** The total annuity under it is set from a **projection** of
  surplus over the whole remaining lifetime; if the insurer earns less than projected, **the
  annuity is reduced** [R21]. A model that treats the *konstante Überschussrente* as a level
  guaranteed stream is wrong. Only the *garantierte Rente* inside it is guaranteed, and the gap
  between the two — on typical market designs, of the order of 15 % to 25 % of the payment
  `[unverified]` — is the amount at risk.
- **The trade-off.** All four forms distribute the same expected surplus and differ only in
  *when*: the constant form front-loads it and carries reduction risk, the volldynamic form
  back-loads it and carries the risk of dying before collecting. Franke und Bornberg titled its
  treatment "Die Qual der Wahl" [R20] — there is no dominant answer.
- ***Bewertungsreserven* participation continues throughout the payout phase** [S3] [R3], with
  § 153 Abs. 3 VVG currently providing for equal participation [S3]. This is a **separate**
  entitlement from the *Überschussrente* and is credited on the occasions the contract specifies.
- **The increase is declared, never guaranteed.** No German carrier guarantees a *Rentendynamik*
  out of surplus; the AVB disclaimer the corpus records applies verbatim — "the amount of profit
  sharing depends on many influences which are unpredictable and only limitedly controllable by the
  company" [S6]. **Any projected increase in a delib model is an insurer-discretionary current
  assumption, never a guaranteed cash flow.**
- **No rate was established, for any form, at any carrier, for any year** — not a
  *Überschussrentensatz*, not a *laufende Verzinsung*, not a dynamic percentage. [S10] establishes
  the document class that publishes them and nothing inside it; [R22] establishes the market study
  that aggregates them and nothing inside it. This is gap 4.

### 10. Where the surplus comes from

- **Three sources, and for an annuity in payment they are not equally important.**
  - ***Zinsüberschuss*** — the excess of the insurer's actual investment return over the
    *Rechnungszins* on the *Deckungsrückstellung*. For a *Sofortrente* this is the dominant source,
    because the reserve is large from day one and runs off slowly over decades.
  - ***Risikoüberschuss*** — for an annuity, a **longevity** result rather than a mortality one. It
    is positive when annuitants die **faster** than the first-order table assumed [R10], and
    negative when they live longer. It is the source that can go the wrong way for a whole cohort
    at once, and it is why annuity tariffs carry the *Sicherheitszuschlag* they do.
  - ***Kostenüberschuss*** — the excess of the loadings taken over the expenses actually incurred.
    Small in absolute terms for this product, because a *Sofortrente* has one acquisition event and
    then a long, cheap payment routine.
- **The statutory floor.** MindZV fixes a minimum share of each result that must be credited to
  policyholders — computed separately on the *Kapitalanlageergebnis*, the *Risikoergebnis* and the
  *übrige Ergebnis*, with a *Sicherungsbedarf* deduction [R15] [R16]. **No percentage was
  established** and none appears here.
- **The competition for the same money.** The *Überschussrente* is paid from the same RfB that
  financed the *Zinszusatzreserve* [R16]. The ZZR build-up suppressed declarations across the
  market; its release as rates rose should work the other way. **Neither its size nor its release
  profile was established**, and nothing quantitative is asserted — but it is the single largest
  driver of what a German annuitant's surplus will do over the next decade, and a model projecting
  a flat surplus rate is ignoring it.
- **`[std]` posture.** Model total surplus as one *Überschussrentensatz* applied to the guaranteed
  annuity, split it by source only if the notes need the split, and label the whole of it an
  **insurer-discretionary current assumption** — category (b) in the delib technical-notes
  taxonomy, never category (a).

### 11. *Rechnungsgrundlagen*: DAV 2004 R, DAV 2004 R-Bestand, the *Trendfunktion*, the *Sicherheitszuschlag*, and the unisex tariff

- **The table is DAV 2004 R**, named in an insurer's own AVB [S6] and derived in a DAV guideline
  [R10]. It is a ***Generationentafel***: mortality is given by **birth cohort**, and the expected
  future improvement is inside the table rather than applied on top of it [R10]. A 65-year-old
  born in 1961 and a 65-year-old born in 1971 are priced on **different** mortality.
- **Component structure** [R10]: a base table of second order; a base table of first order; a
  **mortality trend of second order**; a **mortality trend of first order**; and an age adjustment
  (*Altersverschiebung*) with a base table. The *Trendfunktion* therefore exists in both a
  best-estimate and a prudent version — the correct structure, because prudence in an annuity table
  must reach the **rate of improvement** as well as the level, the improvement compounding over a
  forty-year stream.
- **First against second order** [R10]: first-order probabilities are used for premiums and
  reserves and **carry safety margins relative to the second-order ("realistic") probabilities in
  order to assess the risk prudently**; the second-order base tables represent the **best estimate
  of period mortality in 1999 for insured lives, as three-dimensional selection tables**. For an
  annuity, prudent means **lighter** mortality: the *Sicherheitszuschlag* [R12] pushes `q` down,
  the annuity value **up** and the annuity bought by a given *Einmalbeitrag* **down**. **The
  size of that margin was not established** — gap 12 — and it is one of the two numbers (with the
  *Rechnungszins*) that decide the whole tariff.
- **Dates** [R10]: in use since **June 2004**, for new business from **2005**, the DAV document
  dated **22 February 2005**, the derivation guideline **reissued 28 June 2023**. The reissue is
  the evidence that **no successor annuity table has displaced DAV 2004 R** in twenty years — so
  the 1999 base year is now more than a quarter-century behind the business written on it, and the
  *Trendfunktion* carries all of that distance.
- ***DAV 2004 R-Bestand***. A companion table for the **existing annuity book**, paired with
  DAV 2004 R in a 2004 presentation "DAV 2004 R und RBx" [R11]: new business is priced on
  DAV 2004 R, the in-force portfolio reserved on the *Bestand* table. **Nothing beyond the pairing
  was established** and nothing about it may be asserted downstream. The distinction matters here
  because a *Sofortrente* is written once on the new-business basis and then spends thirty years in
  the *Bestand*.
- **Sex-distinct tables, unisex tariff.** German annuity tables are built sex-distinctly while the
  tariff sold for new business since **21 December 2012** must be unisex [R24] `[unverified]` —
  **neither half corroborated by any delib search**. The practical resolution is a **blended basis
  reflecting an assumed portfolio sex mix**, a pricing assumption no carrier publishes. Two
  consequences: a unisex annuity is a **worse deal for men and a better one for women**, so the
  realised mix drives the *Risikoergebnis* [R15]; and the delib `Sofort_DE_S` decrement table is a
  **unisex `[std]` proxy** and must be described as one.
- **What delib ships.** The DAV tables are DAV property, are not public and are **not redistributed
  here**. delib cites them by name and ships a `[std]` proxy — the Gompertz–Makeham basis of
  section 4 — anchored so the worked example reproduces exactly, with the anchor stated in the
  `Data` docstring. **A replacement must preserve the generational structure (a `q(x, cohort)`
  surface), the first-order margin, and the age-adjustment convention** [R10].

### 12. Charges

- German life insurers build charges into the tariff and disclose them, if at all, in the
  *Produktinformationsblatt* [S11] or the *Basisinformationsblatt* [S12]. **No charge parameter for
  this product was established at any carrier** [R18]: not the *Abschluss- und Vertriebskosten*,
  not the administration loading on the annuity, not the *Effektivkosten*, not a
  *Renditeminderung* figure. See gap 8.
- **The three charge points a *Sofortrente* has**, fewer than most life products: (i) an
  **acquisition and distribution charge on the *Einmalbeitrag***, taken once — `alpha` in section
  4's formula, materially lower than the *Zillmerung* of a recurring-premium contract because there
  is no premium stream to amortise against; (ii) an **administration loading on each annuity
  payment** — `beta` — covering the payment run, the annual *Standmitteilung* [S15] and the
  proof-of-life process; and (iii) an implicit **margin inside the *Rechnungsgrundlagen***, since
  pricing at 0 % when the cap is 1,00 % [S6] [R7] is a charge in economic substance whatever any
  document calls it.
- **`[std]` values**: `alpha = 2,5 %` of the *Einmalbeitrag* and `beta = 2,0 %` of each annuity
  payment `[std]` (7). Rationale: a single-premium annuity's acquisition cost is a one-off
  commission plus issue expense, which the market prices in low single figures of percent; and the
  running loading must cover a per-policy cost that is roughly constant in euros, so 2 % is of the
  right order on a 100 000 € case and too small on a 25 000 € one — which is itself why minimum
  *Einmalbeiträge* exist. **Both are the modeller's view with no observed range, because nothing
  was observed.**
- **Effect on the headline number.** Applying both `[std]` charges to section 4's gross annuity at
  age 65 and 1,00 % gives `407.98 x 0.975 / 1.02 = 389.99 €` per 100 000 € per month, and a 10-year
  *Rentengarantiezeit* takes it to about **381 €** `[std]` — the shape of a quotable guaranteed
  *Sofortrente* on this file's own arithmetic, offered as a **constructed illustration**, not a
  market rate.

### 13. No surrender in the *Rentenbezug*

- **Once the *Rentenbezug* has begun, the contract cannot be surrendered.** § 168 Abs. 3 VVG
  provides that the policyholder's right of termination in a *Rentenversicherung* without a
  *Kapitalwahlrecht* exists only **up to the start of the annuity payments** [R1] `[unverified]` as
  to the paragraph number. For a *Sofortrente* that boundary is at or within weeks of inception, so
  in practice **the contract is irrevocable from the outset**.
- **What follows for a projection model, and it is a great deal:**
  - **No `Rückkaufswert` cells.** § 169 VVG [R2] is displaced. There is no surrender-value table,
    no *Stornoabzug*, no five-year cost-spreading rule to implement.
  - **No lapse decrement.** A policyholder cannot lapse a contract they cannot terminate and on
    which no further premium is due. The only decrement in the payout phase is **death**.
  - **No `Beitragsfreistellung`.** § 165 VVG [R5] has no application: there is no premium to stop.
  - **The `[std]` behavioural assumption set is empty.** Every other delib product needs a lapse
    rate, a paid-up rate and an option take-up rate; this one needs none, which makes it the
    cleanest of the ten to project and the one whose result depends most purely on the mortality
    basis and the surplus assumption.
- **Why the rule exists, and why it is not a defect.** A surrenderable life annuity would be
  surrendered by exactly those annuitants expecting to die soon, leaving the insurer with the
  long-lived; the rule is what makes the mortality pooling — the whole product — possible. The
  consumer warning that follows is that the *Einmalbeitrag* is **irreversibly committed**, the
  first thing every German consumer page about the product says [R21] [R23].
- **One qualification.** The *Aufschubzeit* variant of section 3 has a genuine pre-*Rentenbeginn*
  window in which § 168 Abs. 3 does not yet bite, so a surrender right — and a *Rückkaufswert*
  under § 169 [R2] — may exist during the deferment. **No carrier's terms were established** and a
  reference implementation switches the deferment variant off in its base run.

### 14. Decrements and policyholder behaviour

- **One decrement: death.** In the payout phase there is no lapse, no paid-up conversion and no
  option exercise (section 13). Where a *Hinterbliebenenrente* is in force there are **two lives**
  and the liability runs to the second death (section 7).
- **The pricing basis is DAV 2004 R first order; the best-estimate basis is DAV 2004 R second
  order** [S6] [R10]. The gap between them is the *Sicherheitszuschlag* and it is the single
  largest source of expected surplus on this product (section 10).
- **Anti-selection at issue is real and is not underwritten away.** Annuities are bought
  disproportionately by people who expect to live long, and the German market does not medically
  underwrite them (section 2, `[unverified]`), so the selection sits in the tariff margin rather
  than in an individual assessment. A projection applying population mortality to an annuity book
  overstates deaths by a wide margin.

### 15. Taxation — the *Ertragsanteil*

- **The annuity is taxed on the *Ertragsanteil* under § 22 EStG** [R13]. Only the "Ertrag des
  Rentenrechts" — the interest element deemed to be contained in the annuity — is income; the
  return-of-capital element is not taxed at all. The taxable fraction is a **flat statutory
  percentage of every payment**, determined once by the annuitant's **age at *Rentenbeginn*** and
  **fixed for the whole life of the annuity** [R13].
- **The statutory table.** The values below are the *Ertragsanteil* percentages by age at annuity
  commencement as they have applied since the *Alterseinkünftegesetz* took effect on 1 January
  2005. **The whole table is `[unverified]`**: no delib search returned it, and only the single
  value **18 % at age 65** was corroborated [R13]. It is reproduced because a product-spec must
  carry the schedule and because the corroborated cell matches it exactly, which is the only
  internal check available.

  | Age at start | % | Age | % | Age | % | Age | % |
  |---|---|---|---|---|---|---|---|
  | 50 | 30 | 60–61 | 22 | 71 | 14 | 81–82 | 7 |
  | 51–52 | 29 | 62 | 21 | 72–73 | 13 | 83–84 | 6 |
  | 53 | 28 | 63 | 20 | 74 | 12 | 85–87 | 5 |
  | 54 | 27 | 64 | 19 | 75 | 11 | 88–91 | 4 |
  | 55–56 | 26 | **65–66** | **18** | 76–77 | 10 | 92–93 | 3 |
  | 57 | 25 | 67 | 17 | 78–79 | 9 | 94–96 | 2 |
  | 58 | 24 | 68 | 16 | 80 | 8 | from 97 | 1 |
  | 59 | 23 | 69–70 | 15 | | | | |

  The statutory address usually given — **§ 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb EStG** —
  is itself `[unverified]` [R13].
- **What that is worth.** On the section 12 illustration of a **389.99 €** monthly annuity from
  age 65, the taxable amount is `0.18 x 389.99 = 70.20 €` a month. At a 25 % marginal rate the tax
  is **17.55 € — 4.5 % of the annuity**; at 42 %, **29.48 €, 7.6 %** `[std]` (8). Against a
  *Bankauszahlplan*, whose interest is taxed in full, that difference is the product's main
  quantitative selling point.
- **Deferring the start lowers the fraction as well as raising the annuity**: 18 % at 65 against
  15 % at 70 `[unverified]`, on an annuity that is itself about 18 % larger on the `[std]` basis
  (section 4). The two effects compound and the combination is why the *Aufschubzeit* variant
  exists (section 3).
- **The boundary with § 20 EStG.** The *Halbeinkünfteverfahren* of § 20 Abs. 1 Nr. 6 EStG applies
  only to lump sums and payout-plan withdrawals, requires the 12/62 rule, and **does not apply to
  monthly annuity payments** [R14]. A *Sofortrente* pays no lump sum and could not satisfy the
  twelve-year test in any event. **The whole of its cash flow is § 22 and none of it is § 20.**
- **Not established, and needed downstream**: whether the *Rentengarantiezeit* payments made to a
  beneficiary after the annuitant's death keep the original *Ertragsanteil*; whether the
  *Kapitalrückgewähr* refund is taxable at all; whether the *Hinterbliebenenrente* is taxed on the
  survivor's own commencement age; the *Erbschaftsteuer* treatment of any post-death payment; and
  the *Solidaritätszuschlag*. All are gap 15.

### 16. The *Bankauszahlplan* comparison and the longevity argument

- The German consumer literature's standard comparator for a *Sofortrente* is a
  ***Bankauszahlplan*** (or *Entnahmeplan*): the same capital held at a bank and drawn down at a
  chosen monthly rate until it is exhausted. The comparison is the product's whole sales argument
  and it has three limbs.
- **Limb one — the payout plan ends.** On this file's `[std]` arithmetic, 100 000 € drawn down at
  a monthly rate in advance is exhausted after `[std]` (8):

  | Monthly withdrawal | at 0 % interest | at 2 % | at 3 % |
  |---|---|---|---|
  | 350 € | 23.8 years — age 88.8 | 32.2 years — age 97.2 | 41.1 years — age 106.1 |
  | 400 € | 20.8 years — age 85.8 | 26.9 years — age 91.9 | 32.3 years — age 97.3 |
  | 450 € | 18.6 years — age 83.6 | 23.1 years — age 88.1 | 26.8 years — age 91.8 |

  Read against section 4: an annuity of about **390 €** guaranteed for life is roughly what
  100 000 € buys at 65 on this file's `[std]` basis, and a payout plan matching that rate at 2 %
  runs out at about **age 92**. Beyond that age the annuitant has income and the drawdown investor
  has none. The probability of a 65-year-old reaching 92 on this file's proxy basis is not
  negligible — it is the reason the product exists.
- **Limb two — the *Ertragsanteil* against full taxation.** The annuity is taxed on 18 % of each
  payment [R13]; the payout plan's interest is taxable in full as *Kapitalerträge*. The comparison
  is not like-for-like on gross rates and any presentation that compares them gross is misleading.
- **Limb three — what the annuitant gives up.** The capital is irreversibly committed (section 13),
  there is no residual estate beyond the *Rentengarantiezeit* or *Kapitalrückgewähr*, and an early
  death is a poor outcome, while the *Bankauszahlplan* keeps every euro not yet drawn. The honest
  framing is that a *Sofortrente* is **insurance against outliving one's money**, priced like
  insurance: most buyers "lose" and the ones who need it are made whole.
- **No market comparison, no published payout-plan rate and no Stiftung Warentest side-by-side was
  established.** Every figure in this section is `[std]` arithmetic.

### 17. Typical *Einmalbeitrag* sizes and market context

- **Nothing quantitative was established.** No market size, no number of contracts, no average
  *Einmalbeitrag*, no average purchase age, no distribution of *Rentengarantiezeit* choices beyond
  the qualitative "most choose 10 to 20 years" [R23]. [R25] establishes the GDV statistical series
  that would carry the first four and nothing inside it, and notes that even a retrieved figure
  would aggregate *Sofortrenten* with other single-premium business.
- **What can be said structurally.** The *Sofortrente* is a **decumulation** product bought with a
  lump sum that already exists — a *Kapitalabfindung* from a matured contract, an inheritance, a
  property sale, a severance payment — so its natural size is the size of those events: a five- to
  low six-figure sum in the German retail market. The representative case of **100 000 €** `[std]`
  is the market's quoting unit, not an observation.
- **Its market position is the mirror image of the deferred annuity's.** The sibling file records
  that the classic **deferred** annuity was withdrawn by Debeka in 2016 and by Allianz, Zurich and
  Generali before it, in favour of partial-guarantee hybrids [S7] [S8]. **No equivalent retreat
  from the immediate annuity was established, and there is a structural reason not to expect one**:
  the objection to the deferred contract was a thirty-year interest guarantee, whereas an immediate
  annuity's guarantee is short-dated in interest terms and its real risk is longevity, which no
  alternative design removes — and the *Sofortrente* is the natural destination of the
  *Kapitalwahlrecht* exercised on the withdrawn contracts. **An argument, not a finding**; gap 14.

### 18. What a projection model needs, and what the corpus supplies

| Input | Needed for | Status |
|---|---|---|
| *Einmalbeitrag* | the single inflow | model-point attribute |
| Age and sex at *Rentenbeginn* | the annuity factor | model-point attribute |
| *Rechnungszins* | the annuity factor | 0,25 % / 1,00 % established as statutory maxima [R7] [R8]; the carrier's own choice may be lower [S6] — model-point attribute |
| Mortality, first order | the guaranteed annuity | DAV 2004 R named [S6] [R10]; **table not public, `[std]` proxy shipped** |
| Mortality, second order, and the *Trendfunktion* | best-estimate cash flows; the generational surface | DAV 2004 R second order named and the trend's structure established [R10]; **parameters not established, `[std]` proxy** |
| `alpha`, `beta` charges | the net annuity | **nothing established, `[std]`** (section 12) |
| *Rentengarantiezeit* | the certain-payment window | durations established [R23]; choice is a model-point attribute |
| *Kapitalrückgewähr* | the declining death benefit | mechanic established; **basis and interaction not established** |
| *Hinterbliebenenrente* % and second life | the joint-life liability | rider structure established [S9]; **percentages `[unverified]`** |
| Payment frequency and timing | every cash-flow date | monthly established [S7] [R23]; ***vorschüssig* is `[std]`** (section 8) |
| *Überschussrentensatz* and its profile | the non-guaranteed part of the payment | four forms established [R20] [R21] [R23]; **every rate `[std]`** (section 9) |
| Lapse, paid-up, option take-up | — | **not needed**: the product has none [R1] (section 13) |

The one-line summary of this file: **the mechanics are well enough established to specify the
product; the levels are not established at all, and every one of them is `[std]`.**

---

## Observed variation across insurers

**This file supports no numeric variation table.** No search was run for this product while it was
drafted (gap 1), so no carrier's *Rentenhöhe*, charge, envelope, option menu or surplus rate was
observed here, and a table with a column per carrier would have been fabrication. What this file
supports is a **structural** table and an honest statement of the parameters whose range is unknown.
**The pass of 2026-08-30 opened the carrier documents and added one annuity scale at one vintage
[S8], and no second observation of it** — so the parameters below still have no range, and
`products/sofortrente/sources.md` is where the one observation and its limits are recorded.

### Carriers in the corpus

| Carrier | Document | What it establishes for this product |
|---|---|---|
| Zurich Deutscher Herold | [S2] immediate annuity, Fassung 01/2022; [S3] deferred, Fassung 01/2026 | that a conventional immediate-annuity pack exists in the same series as the deferred one (**no clause content**); and, from [S3], the two-factor rule at *Rentenbeginn* and that *Bewertungsreserven* participation **continues in the payout phase** |
| NÜRNBERGER | [S4] AVB `gn331303_p`, *mit sofort beginnender Rentenzahlung* | that an insurer AVB for exactly this product exists, in the same numbered family as the deferred and unit-linked ones |
| NÜRNBERGER | [S5] AVB tariff NIR3301 | the *Rentengarantiezeit* as a **tariff-level feature carried in the product name** |
| CosmosDirekt (Generali) | [S6] AVB LA 904 A | the conversion basis: **DAV 2004 R**, interest **0 % p.a.** at an unestablished vintage; the surplus disclaimer |
| Allianz | [S7] KomfortDynamik page | that the current annuity factor **is the carrier's immediate-annuity tariff**; that the *Rentengarantiezeit* has a settable minimum |
| Debeka | [S8] B LV series, Privatrente page | the *Deckungskapital* definition; the *Ertragsanteil* framing from an insurer's own page |
| GDV | [S1] [S9] | the model-conditions taxonomy, the **absence** of an immediate-annuity model set from it, and the survivor's annuity as a **rider with its own conditions** |
| Konzern Versicherungskammer | [S10] Überschussverteilung 2026 | the annual surplus-declaration document class, current to 2026; **no rate** |
| Stuttgarter, Mecklenburgische | [S14] | that *Verbraucherinformation*, *Vertragsinformationen* and *Allgemeine Informationen* name the same pack |
| Twenty-plus others | [S13] | names only; **no document, no parameter** |

### Structural variation the corpus supports

| Feature | Variants that exist | Evidence |
|---|---|---|
| *Rentengarantiezeit* | 5 / 10 / 15 / 20 / 25 / 30+ years, or none; typical 15 years to age 70 and 10 years thereafter; most choose 10–20 | [R23]; tariff-level at [S5]; settable minimum at [S7] |
| Settlement inside the guarantee period | instalments continue, **or** commuted lump sum | mechanic recorded; **which carriers use which, not established** |
| Death benefit | *Rentengarantiezeit*, *Kapital-/Beitragsrückgewähr*, *Hinterbliebenenrente*, or none | sections 5–7; **no carrier's menu established** |
| Survivor's annuity | rider with its own condition set; 60 % and 100 % are the market's standard levels `[unverified]` | [S9] |
| *Überschussverwendung* in payout | konstant / steigend (volldynamisch) / teildynamisch / *Bonusrente* | [R20] [R21] [R23] |
| *Bewertungsreserven* in payout | continue, at currently equal participation | [S3] [R3] |
| Interest basis of the guarantee | at or **below** the *Höchstrechnungszins*; 0 % observed at one carrier | [S6] [R7] |
| *Aufschubzeit* | 0 years (pure *Sofortrente*) or a short deferment | section 3; **no carrier's range established** |
| Payment frequency | monthly standard; other frequencies `[unverified]` | [S7] [R23] |

### Parameters whose range is unknown

*Rentenhöhe* per 100 000 € at any age, carrier or year; the spread between the best and worst
quotation; `alpha` and `beta`; *Effektivkosten* or *Renditeminderung*; the *Einmalbeitrag* and
entry-age envelopes; every surplus rate; the split of new business between the
*Überschussverwendung* forms; the take-up of *Kapitalrückgewähr* against *Rentengarantiezeit*; the
market's size and average ticket. **Every one is a gap, not an omission**, and each appears below.

---

## Standardizations introduced in this file

The `[std]` markers used above, with their rationale. Each is a parameter or an illustration chosen
for the reference implementation where the corpus is silent; none is any carrier's value.

1. **Deferral illustration** (section 3): the section 4 proxy basis at 1,00 %, gross of charges, at
   exact age 65 — the *shape* of the deferral effect and the price of a death benefit inside it.
2. **Annuity per 100 000 €** (section 4): the Gompertz–Makeham proxy `mu(x) = 0.0002 +
   1.5e-5 x 1.10^x`, monthly-in-advance via `a12 = a_due - 11/24`, at 0,25 %, 1,00 % and 1,75 %,
   gross of charges, calibrated so life expectancy at 65 (24.29 years) is of the right order for a
   **prudent annuitant** basis. Reproducible from the printed parameters. **Not DAV 2004 R** [R10].
3. **Cost of the *Rentengarantiezeit*** (section 5): same basis, `a12` replaced by
   `annuity-certain-due(n) + n-year-deferred life annuity`; cross-checked against the corpus's own
   consumer illustration [R23], cheaper at every duration for a stated reason.
4. **Nominal capital-return duration** (sections 6, 16): `Einmalbeitrag / (12 x annuity)`, no
   interest, no mortality — the arithmetic a buyer does.
5. **Cost of the *Kapitalrückgewähr*** (section 6): solves the implicit equation printed there,
   deaths at mid-year, refund discounted from mid-year.
6. **Cost of the *Hinterbliebenenrente*** (section 7): joint-life, both lives on the same proxy and
   independent, annuitant 65 and second life 62 — a simplification on both counts.
7. **Charges `alpha = 2,5 %` and `beta = 2,0 %`** (section 12): the modeller's view, argued from a
   single-premium annuity's cost base. **No observed range exists**, because nothing was observed.
8. **Tax illustration** (section 15) and **payout-plan exhaustion** (section 16): 18 %
   *Ertragsanteil* [R13] on the section 12 annuity; monthly withdrawal in advance.
9. **Envelope** (section 2): entry ages 60–85, *Einmalbeitrag* minimum 10 000 €, working range
   25 000–500 000 €, representative case 100 000 € to match the market's quoting unit.
10. **Monthly-in-advance timing and first instalment at `t = 0`** (section 8): adopted because no
    source states the market's convention; the alternative moves every figure here by about 5 %.
11. **The *Kapitalrückgewähr* refund is measured against the *guaranteed* annuity** (section 6):
    argued from the principle that a guaranteed benefit cannot be defined by reference to a
    discretionary quantity. A modeller's argument, not a carrier's clause.

---

## Gaps and caveats

1. **No search was run for this product at all while it was drafted, and the pass of 2026-08-30
   supplied the documents instead.** The session's 200-call `WebSearch` budget, shared across the
   parallel delib researchers, was **exhausted before work on the *Sofortrente* began**, and direct
   HTTP egress was blocked throughout. The brief anticipated thirty to eighty
   German-language queries: insurer AVB and *Versicherungsbedingungen*; *Produktinformationsblätter*
   and *Basisinformationsblätter*; *Rentenhöhe* per 100 000 € from Verivox, CHECK24 and
   `vergleich-sofortrente.de`; Stiftung Warentest's and Finanztip's *Sofortrente* comparisons;
   Franke und Bornberg, Morgen und Morgen and Assekurata ratings; the *Überschussbeteiligung*
   declarations for 2025 and 2026; the *Rentengarantiezeit* and *Kapitalrückgewähr* menus at
   twenty-plus named carriers; § 168 VVG; the *Ertragsanteil* table; DAV 2004 R and
   DAV 2004 R-Bestand. **None was run.** Every source entry here is therefore either a known
   reference or a fact carried over with attribution from a sibling delib research file whose
   searches ran earlier in the session. Nothing was written to fill the hole, and no URL, figure,
   paragraph number or document code was guessed, then or since. **What the pass then reached is in
   `products/sofortrente/sources.md`: 19 of its 32 entries read `Retrieved: yes`.** It closed the
   documentary half of this gap — insurer AVB, the GDV model conditions and the statutory spine were
   all read — and left the quantitative half open, because comparison portals generate a quotation
   per enquiry rather than publish one and the ratings are sold rather than published. Gap 2 below
   is the part that stands.

2. **No insurer-level quantitative comparison exists in this file.** Twenty-eight carriers are
   named [S13] and not one has a *Rentenhöhe*, a charge, an envelope, an option menu or a surplus
   rate attached, so the "observed variation" section is structural only. A reader who needs to know
   how German carriers differ on this product will find **nothing** here and must start with [S11],
   [R21] and [R23].

3. **No GDV model conditions for the immediate annuity were established.** The GDV index as
   recorded by the sibling file lists five model-condition sets and none is the *sofort beginnende
   Rentenversicherung* [S1]. Whether the association maintains one under another title, or whether
   the market drafts from the deferred template, is unresolved. [S2] and [S4] — immediate-annuity
   documents sitting inside their carrier's deferred-annuity families — point to the second
   reading, but that is an inference and is not asserted downstream.

4. **No *Überschussbeteiligung* rate was established, for any year, at any carrier, in either
   phase.** [S10] establishes the declaration document class and its 2026 vintage; [R22] the 24th
   edition of the study that aggregates them. Nothing inside either was returned: no *laufende
   Verzinsung*, no *Zinsüberschussanteil* on the *Deckungsrückstellung* of annuities in payment, no
   *Überschussrentensatz*, no dynamic percentage, no *Bewertungsreserven* amount. **Every surplus
   figure downstream is `[std]` and must be labelled an insurer-discretionary current assumption.**

5. **No *Rentenhöhe* and no *Rentenfaktor* level was established — at any carrier, for any year, at
   any age.** This is the largest quantitative hole and it is the number the product is bought on;
   the rating house's own article "Was bedeutet der Rentenfaktor und **wie hoch ist er?**" returned
   no level [R20]. Section 4 therefore **constructs** a table from stated annuity mathematics and
   labels every cell `[std]`. Two consequences: the statement that annuity levels "moved with the
   *Höchstrechnungszins*" is **directionally** supported by the tariff formula [S6] and the
   statutory rate history [R7] [R8] and is **quantitatively `[std]`**, the +10 % at age 65 being
   this file's arithmetic and not an observation; and any *Rentenhöhe* reaching the product-spec
   must be `[std]` with its derivation printed beside it, never an `[S#]` figure.

6. **The one hard number in the corpus has no date.** [S6] reads "a recognised mortality table
   (**currently** DAV 2004 R) and an underlying interest rate (**currently** 0 percent p.a.)". Both
   are as-ats and the as-at is unknown: the AVB's vintage was not established, LA 904 is the oldest
   number in the carrier's series, and siblings in it carry 11/2022 dates. A 0 % basis is
   consistent with the 0,25 % era and would be unusually conservative in the 1,00 % era.

7. **The market is unsized and the envelope is unestablished.** No number of contracts, no premium
   volume, no average *Einmalbeitrag*, no average purchase age, no minimum or maximum
   *Einmalbeitrag*, no entry-age limits, no distribution of *Rentengarantiezeit* or
   *Überschussverwendung* choices. [R25] establishes the GDV series that would carry the first four
   and notes that even a retrieved *Einmalbeiträge* figure would not isolate this product. Every
   issue rule in the delib product-spec is `[std]`.

8. **No charge parameter was established, and the disclosure regime's application is unresolved.**
   Not `alpha`, not `beta`, not an *Effektivkosten* figure under VVG-InfoV, not a *Renditeminderung*
   under PRIIPs [R17]. Worse, **whether a payout-only *Sofortrente* is even in PRIIPs scope was not
   established** [S12], so it is not known whether the standardised cost figure exists to be found.
   No *Produktinformationsblatt* and no *Basisinformationsblatt* for this product appears in the
   corpus at all, although the brief named both as target document types. The `[std]` values of
   section 12 are the modeller's view with **no observed range**, which is weaker than a `[std]`
   with a range and is stated as such.

9. **§ 168 Abs. 3 VVG was not read at article level.** The rule ending the right of termination at
   *Rentenbeginn* [R1] — on which this product's entire "no surrender, no lapse, no paid-up"
   specification rests — is stated from general knowledge of German insurance law. Its paragraph
   number, wording, the scope of the "*ohne Kapitalwahlrecht*" qualifier and its interaction with a
   short *Aufschubzeit* are all `[unverified]`. The **substance** is corroborated indirectly — it
   is the uniform statement of the consumer literature [R21] [R23] and the economic precondition
   for writing annuities at all — but no statutory text was seen.

10. **The death-benefit options are established as mechanics and not as terms.** Unresolved:
    whether a *Rentengarantiezeit* pays the remaining instalments or a commuted lump sum, and on
    what basis a commutation would be struck; whether *Kapitalrückgewähr* and *Rentengarantiezeit*
    may be combined and at which carriers; whether the refund is measured against the guaranteed
    annuity or the total paid (this file adopts the guaranteed annuity as `[std]` (11) on an
    argument, not a clause); whether partial or capped refund variants are sold; and the percentage
    menu for the *Hinterbliebenenrente*, where 60 % and 100 % are `[unverified]`.

11. **The payment timing was not established.** No source in the delib corpus states whether a
    German annuity in payment is *vorschüssig* or *nachschüssig*, for this product or the deferred
    one. It is first-order: on this file's own basis the two conventions differ by about **5 %** of
    the annuity (section 8). Monthly-in-advance is adopted as `[std]` (10) and must be stated as a
    convention wherever it is used. Likewise unestablished: the first payment date, the treatment
    of an instalment already paid for the period of death, and the loadings attaching to
    non-monthly frequencies.

12. **DAV 2004 R is established structurally and not numerically, and DAV 2004 R-Bestand barely at
    all.** Established: generational construction, the five-component structure, the first- and
    second-order distinction and its direction, the 1999 base year, the dates, the 2023 reissue
    [R10]. **Not established**: the size of the *Sicherheitszuschlag*; the *Trendfunktion*'s form or
    parameters; the age range; the *Altersverschiebung* convention; and, for the *Bestand* table
    [R11], anything beyond the fact that it exists and is paired with the new-business table. The
    tables are DAV property, are not public and are **not redistributed by delib**; the shipped
    decrement CSV is a `[std]` proxy anchored to reproduce the worked example, and the `Data`
    docstring must say so.

13. **The unisex rule was not established at either end** [R24]. No delib search confirmed that
    DAV 2004 R is published sex-distinctly, and none reached the CJEU judgment, its case number, or
    the German application date of 21 December 2012; both halves are `[unverified]`. It matters
    more here than for any other delib product, because the contract is a pure longevity bet and a
    unisex tariff on sex-distinct tables must be struck on an assumed portfolio sex mix that no
    carrier publishes. The rule belongs to the delib cross-product reference library and must be
    cited from there.

14. **The claim that the immediate annuity has not retreated as the deferred one has is an
    argument, not a finding.** The sibling file establishes that Debeka, Allianz, Zurich and
    Generali withdrew classic **deferred** tariffs; nothing in this corpus says anything about
    their **immediate** annuities. Section 17's reasoning is plausible and unverified. Do not
    assert it downstream as market fact.

15. **The tax picture is incomplete beyond the core rule.** Established: the *Ertragsanteil* regime
    and the corroborated 18 % at age 65 [R13]; the § 20 EStG boundary [R14]. **Not established**:
    every other value of the statutory table (the schedule in section 15 is `[unverified]` in its
    entirety, with one matching cell as its only check); the statutory address of the table; the
    treatment of *Rentengarantiezeit* payments made to a beneficiary; whether a *Kapitalrückgewähr*
    refund is taxable; whether a *Hinterbliebenenrente* is re-based on the survivor's commencement
    age; the *Erbschaftsteuer* treatment of any post-death payment; and the *Solidaritätszuschlag*.

16. **No *Standmitteilung* or *Rentenanpassungsmitteilung* was located** [S15], so this file
    contains **no evidence of what a *Rentenanpassung* has actually done** at any carrier in any
    year. Section 9's central claim that the *konstante Überschussrente* can be reduced rests on
    consumer commentary [R21], not on a specimen statement.

17. **The *Aufschubzeit* variant is described from structure, not from a carrier's terms.** No
    minimum or maximum deferment, no death-benefit rule during it, no statement of whether a
    surrender right survives inside it, and no carrier's product identified — the Mecklenburgische
    "Rente flex" [S14] is a candidate whose title is truncated. Section 3's figures are `[std]`.

18. **The corpus is thin on this product specifically.** Of fifteen primary entries, exactly **two**
    are documents whose title names the immediate annuity ([S2], [S4]), and **neither** yielded a
    single clause; four are document classes with no instance located ([S11], [S12], [S13], [S15]);
    the remaining nine are deferred-annuity or shared-chassis documents used because the two
    products share their machinery. **No paragraph number, clause heading or sentence of
    contractual wording for a German *Sofortrente* appears anywhere in this file, and none may be
    invented downstream.**

19. **Living texts.** § 153, § 163, § 165, § 168, § 169 VVG, § 20 and § 22 EStG, DeckRV § 2, MindZV
    and VAG §§ 138–140 were all reached without a version date, most only through a sibling file's
    search record. The DeckRV change to 1,00 % is established as effective **1 January 2025**
    [R7] [R9], with the DAV recommending the same rate for **2026** [R8]. The DAV 2004 R derivation
    guideline was reissued **28 June 2023** [R10]. Zurich's immediate-annuity pack is **Fassung
    01/2022** [S2] and its deferred sibling **Fassung 01/2026** [S3]; the Konzern
    Versicherungskammer declaration is **2026** [S10]; Assekurata's study is in its **24th edition,
    2026** [R22]. **Check every article number, every date and every figure for later amendment
    before relying on it.**
