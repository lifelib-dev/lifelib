# Pflegerentenversicherung (private LTC annuity) — research notes (Germany)

Research notes for the German individual *Pflegerentenversicherung* — the private long-term-care
top-up written **as a life-insurance contract**, which pays a monthly *Pflegerente* for as long as
the *versicherte Person* holds a contractual *Pflegegrad*, graded by *Pflegegrad*, with
*Beitragsbefreiung im Leistungsfall* (waiver of premium in claim), a level *Beitrag* calculated
*nach Art der Lebensversicherung* against a *Deckungskapital* that performs the economic function of
an *Alterungsrückstellung*, and frequently a *Todesfallleistung* or *Beitragsrückgewähr*.

**In scope.** The individual, privately-written, single-life *Pflegerentenversicherung* sold by a
*Lebensversicherer*: a stand-alone contract (not a rider on an endowment or an annuity), with a
*vereinbarte Pflegerente* graded across the five *Pflegegrade* of SGB XI, a level lifelong or
term-limited *Beitrag* that the insurer may not re-rate, a prospective *Deckungsrückstellung*, a
*Rückkaufswert* under § 169 VVG and a *Beitragsfreistellung* right under § 165 VVG, an
*Überschussbeteiligung* under § 153 VVG, and a benefit trigger defined by reference to the
*Pflegegrad* determined under §§ 14, 15 SGB XI.

**Out of scope, and said so where it matters.**

- The **soziale Pflegeversicherung** of SGB XI itself, and the **private Pflegepflichtversicherung**
  (PPV) of § 23 SGB XI, are the compulsory first layer. They are not modelled. They are researched
  here in detail because the private product is sized against the gap they leave, and because the
  private product's benefit trigger is defined by reference to them.
- **Pflegetagegeldversicherung** and **Pflegekostenversicherung** are the other two private forms.
  They are written as *private Krankenversicherung*, not as *Lebensversicherung*, and their premium
  can be re-rated under § 203 VVG. They are researched here as contrast documents — the difference
  between them and the *Pflegerente* is the single most important structural fact about this product
  — but neither is the delib model.
- **Pflege-Bahr**, the state-subsidised cover of § 127 SGB XI, is confined by statute to the
  *Pflegetagegeld* form. It is researched here in full because the brief requires it and because it
  fixes a statutory minimum benefit grid that the private market reuses, but **a Pflegerente cannot
  be a geförderter Tarif** and the delib model does not implement the *Zulage*.
- *Berufsunfähigkeitsversicherung* (delib product 9) is the neighbouring biometric-risk product; it
  shares the *nach Art der Lebensversicherung* chassis, the *Beitragsbefreiung im Leistungsfall*, the
  *Nachprüfung* and the multi-state modelling problem, and differs in trigger, in duration and in
  the age at which the risk bites. It is referenced where the two diverge.
- *Betriebliche Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung*, the
  *private Krankenversicherung* proper, *Sterbegeldversicherung* and institutional risk transfer are
  outside the delib library entirely.
- *Pflegerente gegen Einmalbeitrag* — the single-premium form sold to people already close to, or
  already in, care — is recorded as a market variant and is **not** the base model.
- Austrian and Swiss LTC products are excluded: SGB XI, the VVG, the VAG and the DeckRV do not
  apply to them, and neither does the *Pflegegrad* concept.

These notes are the **citation ground truth** for the delib `pflegerentenversicherung` product
documents. Source ids **S1..S16** and **R1..R24** below are **frozen — never renumber**; unused ids
are simply omitted downstream, leaving gaps, and `sources.md` records which are absent and why.

Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

This section has two halves. The first records the conditions the research was **done** under on
2026-08-29; the second records what the **re-verification** of 2026-08-30 established. The first is
kept because it is how this file came to say what it says, and the second is set out entry by entry
in *Provenance pass of 2026-08-30* at the foot of this file, which is the operative record.

**No document in this file had been retrieved when it was written.** Direct HTTP egress from the
build environment was blocked by an organisation network policy. `WebFetch` and `curl` were refused with HTTP 403 at
the egress gateway for every host outside a short package-registry allowlist. The hosts that mattered
for this product were all tried and all refused:

Every host that would have supplied a document for this product was tried and refused with HTTP
403: `gesetze-im-internet.de` (SGB XI, VVG, VAG, EStG, SGB XII, DeckRV, KVAV), `bafin.de`,
`gdv.de`, `aktuar.de` (the DAV 2008 P derivation), `pkv.de` (the PKV-Verband statistics and the
MB/EPV), `destatis.de` (the *Pflegestatistik*), `bundesgesundheitsministerium.de`, `vdek.com`
(the *Eigenanteil* series) and `de.wikipedia.org`.

Not one *Bedingungswerk*, not one *Produktinformationsblatt*, not one *Basisinformationsblatt*, not
one statutory text, not one DAV paper and not one statistical release was opened.

**The session `WebSearch` budget was already exhausted when this product was started.** The session
shared a hard cap of 200 `WebSearch` calls across all delib work, and the cap had been reached
before the first query for this product could be issued. **This file therefore had no research
channel at all while it was drafted** — neither retrieval nor search. Its first draft rested on the
authoring model's own knowledge of German insurance law and German actuarial practice, under the
discipline that house rule 3 imposes for exactly this case.

What that discipline meant here, concretely:

1. **Every source entry was a *known reference*, never a read document.** Each recorded
   `Retrieved: no — direct HTTP egress blocked in the build environment; no search corroboration
   (session search budget exhausted)`, names a publisher and a document type that exist and are
   the right kind of document for this product, and asserted nothing about any particular edition,
   document number, page count or date, because none had been checked. **This is the rule the
   re-verification changed**, and the pass section at the foot of this file records how far.
2. **No URL is invented and no instrument is quoted.** Where a canonical form is well known —
   `.../sgb_11/__15.html` for § 15 SGB XI — it is given and marked `[unverified]`; elsewhere the
   entry says `URL: not established`. There is not one German sentence in quotation marks
   attributed to a statute or to a *Bedingungswerk* anywhere in this file, because there is no
   summary and no PDF behind one; statutory rules are described in English, in the author's own
   words, as *what the instrument provides*.
3. **`[unverified]` is used generously.** Every specific paragraph number, date, amount, percentage,
   threshold and market figure below carries it. The general *shape* of a well-established mechanic
   is not tagged, because tagging it would drown the signal; the moment a claim becomes **specific
   and numeric**, it is tagged.
4. **Uncertain levels are `[std]` parameters, not citations**, each with a stated rationale and an
   argued range, and section 23 shows the arithmetic behind the premium band rather than asserting
   a figure. A guessed `[S4]` number would not be honest; a `[std]` one is.
5. **The weight of the file is in the mechanics.** Sections 1 to 23 are what the product
   specification and technical notes will be written from, and they do not depend on having a PDF
   open. The source list is thinner in its claims than an frlib source list, and the gaps register
   at the foot is longer.

**What the re-verification established.** The policy was lifted, and on **2026-08-30** every source
in this file was tried again and the citations were checked against the primary documents.
Library-wide, all fifteen German instruments delib cites were read as canonical XML from
`gesetze-im-internet.de` with each law's amendment `Stand` recorded, 950 statutory section
references were checked and 950 were correct, and insurer AVB, *Verbraucherinformationen* and
*Produktinformationsblätter* were retrieved as PDFs and read; **501 of the library's 805 source
entries, 62 %, now read `Retrieved: yes`.** For this product the record is the table in *Provenance
pass of 2026-08-30* below, not a line on each entry: the entries and their numbering are frozen and
are left as drafted, and the table records **thirty of the forty as read**, of which [S5] and [S10] only
in part; **eight as not retrieved with the reason** — [S3], [S6], [S8], [S9], [S13], [S15], [R16]
and [R17] — and two amending acts, [R9] and [R10], as not opened as acts. The per-entry `Retrieved`
lines in `products/pflegerentenversicherung/sources.md` carry the same result document by document
and are the more current of the two files on retrieval.

**What a citation now means.** Where the pass table records a document as read, it was opened and
the passage relied on was read, with the statute's `Stand` or the document's edition and page count
recorded. Everywhere else **a delib citation is still a pointer, not a certificate**: `[R2]` beside
a statement about § 15 SGB XI means *this is the instrument the statement should be checked
against*, and it does not mean anyone checked it. **The re-verification changed things** — eight
statements in this file are contradicted by a document retrieved on 2026-08-30, four gaps are closed
and two narrowed, and all of that is set out in the pass section rather than folded back into the
text above. Treat a claim here as sound where the pass records the document as read, and as
provisional where it does not.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on:

| Term | Gloss |
|---|---|
| *Pflegebedürftigkeit* | The insured event: a state of dependency on help with the ordinary business of living, defined in § 14 SGB XI by loss of *Selbstständigkeit* rather than by hours of care |
| *Pflegegrad* (1–5) | The five statutory degrees of *Pflegebedürftigkeit* in force since 1 January 2017; the benefit trigger and benefit scale of every private product |
| *Pflegestufe* (I–III, Härtefall) | The three pre-2017 degrees, replaced by the *Pflegegrade*; still cited in older wordings and older statistics |
| *Soziale Pflegeversicherung* (SPV) | The statutory LTC insurance of SGB XI, the fifth pillar of German social insurance |
| *Private Pflegepflichtversicherung* (PPV) | The compulsory private equivalent for people insured in the *private Krankenversicherung*, § 23 SGB XI |
| *Neues Begutachtungsassessment* (NBA) | The assessment instrument introduced with the five *Pflegegrade*; scores six *Module* and converts them into *gewichtete Punkte* |
| *Medizinischer Dienst* (MD, formerly MDK) / MEDICPROOF | The assessor for the SPV / the assessor for the PPV |
| *Pflegegeld* / *Pflegesachleistung* | The cash benefit for care given informally at home / the benefit in kind for a professional *Pflegedienst* |
| *Vollstationäre Pflege* | Care in a *Pflegeheim*; the setting in which the funding gap is largest |
| *Eigenanteil*, *einrichtungseinheitlicher Eigenanteil* (EEE) | The resident's own share of the cost of a *Pflegeheim* / the care-related part of it, equal for *Pflegegrade* 2 to 5 within one facility since 2017 |
| *Leistungszuschlag* | The duration-dependent statutory subsidy that reduces the *EEE* the longer the resident has been in the facility, § 43c SGB XI |
| *Pflegetagegeldversicherung* / *Pflegekostenversicherung* / *Pflegerentenversicherung* | Daily-cash form (a *Summenversicherung*) / indemnity form / annuity form written as life assurance |
| *Pflege-Bahr* | The state-subsidised *Pflegetagegeld* of § 127 SGB XI, from the 2013 reform, carrying a monthly *Zulage* |
| *Vereinbarte Pflegerente* | The contractual monthly annuity at the top *Pflegegrad*, the scaling constant of the whole benefit schedule |
| *Leistungsstaffel* | The schedule of benefit percentages by *Pflegegrad* |
| *Beitragsbefreiung im Leistungsfall* | Waiver of premium while the benefit is payable |
| *Wartezeit* / *Karenzzeit* | Qualifying period from inception before cover attaches / deferred period from the onset of *Pflegebedürftigkeit* before the annuity starts |
| *Nachprüfung* / *Herabstufung* | The insurer's periodic re-verification that the trigger still holds / a reduction of the *Pflegegrad*, which reduces or ends the annuity |
| *Dynamik* | Contractual indexation: *Beitragsdynamik* raises premium and cover before claim, *Leistungsdynamik* raises the annuity in payment |
| *Todesfallleistung* / *Beitragsrückgewähr* | Death benefit / return of premiums paid, the common form of it here |
| *Nach Art der Lebensversicherung* | Calculated on life-assurance principles: level premium, prospective reserve, ageing provision, no ordinary re-rating |
| *Alterungsrückstellung* | The ageing provision of *private Krankenversicherung*; the economic function the *Pflegerente*'s *Deckungskapital* performs |
| *Deckungskapital* / *Deckungsrückstellung* | The actuarial reserve of one contract / the balance-sheet provision covering it |
| *Rechnungszins* / *Höchstrechnungszins* | The technical interest rate the contract is priced and reserved on / its statutory maximum for new business, set in the DeckRV |
| *Rückkaufswert* / *Stornoabzug* | Surrender value / the deduction the insurer may make from it |
| *Beitragsfreistellung* | Conversion to a paid-up contract on the policyholder's demand, § 165 VVG |
| *Überschussbeteiligung* | Participation in the insurer's surplus, § 153 VVG |
| *Gesundheitsprüfung* / *Risikozuschlag* / *Leistungsausschluss* | Medical underwriting / extra-risk loading / an exclusion written into the individual contract |
| *Vorvertragliche Anzeigepflicht* | The applicant's pre-contractual duty of disclosure, § 19 VVG |
| *Reaktivierung* | Recovery from *Pflegebedürftigkeit* back to the active state; in this product a decrement out of the paying state |

---

## Primary sources

**The blanket retrieval status these entries were drafted under no longer holds, and no entry below
carries a per-entry line to replace it.** As drafted, all sixteen read **Retrieved: no — direct HTTP
egress blocked in the build environment; no search corroboration (session search budget
exhausted)**, and each named a document that exists and is the right kind of document for this
product without asserting that a particular edition, document number, page count or date was
correct. **Ten of the sixteen were opened on 2026-08-30** — [S1], [S2], [S4], [S5], [S7], [S10],
[S11], [S12], [S14] and [S16] — and what each yielded, with its edition and page count, is in
*Provenance pass of 2026-08-30* at the foot of this file and entry by entry in
`products/pflegerentenversicherung/sources.md`. The other six were not, and for them the drafted
status stands. **Where the pass and an entry below disagree, the pass governs.**

### S1 — PKV-Verband, *Musterbedingungen für die private Pflegepflichtversicherung* (MB/PPV)
- Publisher: Verband der Privaten Krankenversicherung e. V. (PKV-Verband), Köln
- Doc type: *Musterbedingungen* — model conditions for the compulsory private LTC cover of § 23
  SGB XI, adopted with variations by every private health insurer
- URL: not established
- Content and why it is here: the MB/PPV is the document in which the private sector's rendering of
  *Pflegebedürftigkeit* and of the five *Pflegegrade* is written down, mirroring §§ 14, 15 SGB XI
  [R2] and the benefit catalogue of §§ 36 ff. SGB XI [R3][R4]. It matters to a *Pflegerente* for one
  structural reason: **private top-up wordings normally define their own trigger by reference to the
  *Pflegegrad* established under SGB XI or the MB/PPV, rather than by writing an independent
  medical definition.** That reference is what makes the product cheap to administer and what ties
  its incidence experience to the statutory assessment regime, including every future change to it.
  An edition designation of the form "MB/PPV 2017" — the recension carrying the five *Pflegegrade*
  — is `[unverified]`; the current edition was not established.

### S2 — PKV-Verband, *Musterbedingungen für die ergänzende Pflegekrankenversicherung* (MB/EPV)
- Publisher: PKV-Verband
- Doc type: *Musterbedingungen* for the **top-up** LTC cover written as *private Krankenversicherung*
  — the *Pflegetagegeld* and *Pflegekosten* forms
- URL: not established
- Content and why it is here: this is the contrast document for the whole file. A *Pflegetagegeld*
  written on MB/EPV lines is a **health-insurance** contract: it is supervised under the health
  rules, it may carry a *Beitragsanpassung* clause under § 203 VVG, and where it is written *nach
  Art der Lebensversicherung* its ageing provision is an *Alterungsrückstellung* under § 146 VAG and
  the KVAV [R14]. A *Pflegerente* on the same risk is a **life** contract with a *Deckungsrückstellung*
  under the DeckRV [R13] and no ordinary re-rating power. Everything a customer is told about the
  two products' relative merits reduces to that difference. Edition designations are `[unverified]`.

### S3 — GDV, *Musterbedingungen* for life-assurance products
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV)
- Doc type: *Musterbedingungen* — model AVB published by the industry association for members to
  adopt, adapt or ignore, expressly *unverbindlich*
- URL: not established (the GDV maintains a public *Musterbedingungen* index; the index URL was not
  established)
- Content: the GDV publishes model AVB for the main life-assurance product families in the
  question-headed style adopted for post-2008 VVG wordings ("Welche Leistungen erbringen wir?").
  **Whether the GDV publishes a *Musterbedingung* specifically for the *Pflegerentenversicherung*
  was not established, and this file does not assume it does.** No benefit, premium, surrender or
  paid-up rule anywhere below is attributed to S3. The entry is retained because the model-conditions
  library is the first document a reader with a working network should look for, and because a GDV
  *Musterbedingung*, if one exists, would be the natural spine of a composite specification. An
  S3-tagged fact would in any case be a *market template*, weaker evidence about any carrier than
  that carrier's own AVB.

### S4 — *Allgemeine Bedingungen für die Pflegerentenversicherung* (AVB), as a document class
- Publisher: an individual German *Lebensversicherer* (no carrier's wording was located)
- Doc type: *Allgemeine Versicherungsbedingungen* / *Bedingungswerk* for a *Pflegerenten* tariff,
  typically bundled with *Tarifbedingungen* and delivered with the *Versicherungsschein*
- URL: not established
- Content — what a wording of this class contains, stated as a document-class description and not as
  a reading of any instance. The clause inventory is stable across the German life market and is the
  skeleton the delib product specification follows:
  - **Benefit clause** — the *vereinbarte Pflegerente*, the *Leistungsstaffel* by *Pflegegrad*,
    whether grade 1 is insured, whether the annuity differs between care at home and
    *vollstationäre* care, and whether it is payable for life.
  - **Trigger clause** — how *Pflegebedürftigkeit* is established: normally by the *Pflegegrad*
    determined by the SPV or the PPV, with a fallback assessment by a physician the insurer
    appoints where the insured is covered by neither.
  - **Waiting and deferred periods** — *Wartezeit* from inception, *Karenzzeit* from onset, and
    whether either is waived where *Pflegebedürftigkeit* follows an accident.
  - **Waiver clause** — *Beitragsbefreiung im Leistungsfall*: from which grade, from which month,
    and whether full or proportionate.
  - **Re-verification clause** — *Nachprüfung*, and the consequences of a *Herabstufung*.
  - **Death-benefit clause** where one is written: *Beitragsrückgewähr*, a fixed sum, or the
    *Deckungskapital*. **Indexation clause** — *Beitragsdynamik* and *Leistungsdynamik*.
    **Surplus clause** [R11]. **Surrender and paid-up clauses** under §§ 169 and 165 VVG, with the
    *Stornoabzug*. **Disclosure and exclusion clauses** — § 19 VVG, and exclusions for care caused
    by war, by the insured's intentional act and, variably, by addiction or by a condition
    disclosed and excluded at underwriting. **Territorial clause** — whether the annuity survives
    care given outside Germany or the EEA.
  No page count, no edition date and no clause number for any carrier's wording is asserted; every
  such specific is `[unverified]` and is recorded as gap 14.

### S5 — *Produktinformationsblatt* (PIB) / *Informationsblatt zu Versicherungsprodukten* (IPID)
- Publisher: an individual German *Lebensversicherer*
- Doc type: the short pre-contractual product summary. The German market uses both the national
  *Produktinformationsblatt* required by § 4 VVG-InfoV for certain life products and the EU IDD
  *Insurance Product Information Document* [R11][unverified as to which applies to this product]
- URL: not established
- Content: the document class that would have supplied, on one or two pages, exactly the parameters
  this file has to standardise — entry-age band, *vereinbarte Rente* band, the *Leistungsstaffel*,
  the *Wartezeit*, the *Karenzzeit*, the premium for a named specimen, and the charges. **Not one
  instance was located**, and this is the single most valuable missing document class in the file
  (gap 1).

### S6 — *Basisinformationsblatt* (PRIIP-KID)
- Publisher: an individual German *Lebensversicherer*
- Doc type: the three-page key information document required by Regulation (EU) No 1286/2014 [R25]
- URL: not established
- Content, and a genuine structural question the delib documents must answer rather than assume:
  **whether a *Pflegerentenversicherung* is a PRIIP at all depends on its own design.** The
  Regulation excludes life-insurance contracts whose benefits are payable only on death or in
  respect of incapacity due to injury, sickness or infirmity [R25][unverified as to the article]. A
  **pure-risk *Pflegerente* with no surrender value and no death benefit falls squarely inside that
  exclusion and needs no *Basisinformationsblatt***. A *Pflegerente* **with** *Beitragsrückgewähr*,
  or with a material *Rückkaufswert*, pays on events other than incapacity and death-in-claim and is
  much more likely to be an insurance-based investment product requiring one. The consequence for
  delib: the presence or absence of a *Basisinformationsblatt* in a carrier's document library is
  evidence about the tariff's design, and the delib base run — pure risk, no *Beitragsrückgewähr* —
  is the variant for which no KID would be expected. All of this is `[unverified]` and is recorded
  as gap 16.

### S7 — *Verbraucherinformationen* / *Vertragsinformationen* under the VVG-InfoV
- Publisher: an individual German *Lebensversicherer*
- Doc type: the pre-contractual information package required by § 7 VVG and the VVG-InfoV [R11]
- URL: not established
- Content: the package in which, for a life product, the *Abschluss- und Vertriebskosten* and the
  *Verwaltungskosten* must be disclosed in euro amounts, and in which the *Effektivkosten* (reduction
  in yield) appears for products with a savings element. For a biometric-risk product the euro
  disclosure of acquisition and administration costs is the operative one. **No instance was
  located**; every charge level in delib is therefore `[std]` (gap 2).

### S8 — *Jährliche Mitteilung zum Stand Ihrer Versicherung* (Standmitteilung)
- Publisher: an individual German *Lebensversicherer*; a GDV model exists for other life products
- Doc type: the annual statement owed to the policyholder under § 155 VVG [R11][unverified]
- URL: not established
- Content: the document reporting the guaranteed benefit, the accumulated *Überschussbeteiligung*,
  the current *Rückkaufswert* and the current *beitragsfreie* benefit side by side — i.e. it names
  the state variables a projection model must carry. For a *Pflegerente* the guaranteed benefit is
  the *vereinbarte Pflegerente* at the top *Pflegegrad*, not a sum
  insured. **No instance was located and the field list is `[unverified]`.**

### S9 — *Tarifblatt* / *Beitragstabelle* for a *Pflegerenten* tariff
- Publisher: an individual German *Lebensversicherer*
- Doc type: the rate card — premium per unit of *vereinbarte Rente*, by entry age, sex, smoker
  status where used, *Beitragszahlungsdauer* and option set
- URL: not established
- Content: **no German insurer publishes a *Pflegerenten* rate card**, on the evidence available to
  this file, and none was located. This is the difference between this file and
  `frlib/_research/temporaire-deces.md`, where one insurer's complete attained-age grid was read off
  a retrieved PDF and became the reference implementation's premium basis. delib's
  `pflegerentenversicherung` model has **no published premium to reproduce**; its premium is struck
  by equivalence on `[std]` bases and its level is sanity-checked against the argued band in
  section 23 (gap 3).

### S10 — Stiftung Warentest / *Finanztest*, comparative tests of *Pflegezusatzversicherung*
- Publisher: Stiftung Warentest — **secondary**, not a product document
- Doc type: comparative product test with a scored ranking and a price table
- URL: not established
- Content: Stiftung Warentest has tested German *Pflegezusatzversicherung* repeatedly, and its tests
  are the most-cited public price source for the sector. Two things about the tests matter here and
  are structural rather than numeric: **the tests concentrate on *Pflegetagegeld***, because that is
  the dominant form by contract count, and **the tests are consistently critical of *Pflege-Bahr***
  for the ratio between the benefit it buys and the *Versorgungslücke* it is meant to close. No
  score, no price and no test date is asserted; every such specific is `[unverified]` (gap 4).

### S11 — Verbraucherzentrale, consumer guidance on *Pflegezusatzversicherung*
- Publisher: Verbraucherzentrale Bundesverband and the *Länder* consumer centres — **secondary**
- Doc type: consumer guidance pages
- URL: not established
- Content: the consumer-body view, which is where the three private forms are set against each
  other for a lay reader. The recurring points, stated as the sector's settled consumer-advice
  position rather than as a reading of any page: the *Pflegerente* is the most expensive of the
  three per euro of benefit but the only one with a premium the insurer cannot re-rate; the
  *Pflegetagegeld* is the cheapest to start and carries re-rating risk; the *Pflegekosten* form is
  effectively obsolete; and a *Pflegetagegeld* written **not** *nach Art der Lebensversicherung*
  (i.e. *nach Art der Schadenversicherung*, with no ageing provision) is the form to avoid, because
  its premium rises with attained age. `[unverified]` throughout.

### S12 — Finanztip, guidance on *Pflegezusatzversicherung*
- Publisher: Finanztip — **secondary**. Doc type: consumer guidance. URL: not established
- Content: same class of evidence as S11, retained separately because Finanztip publishes explicit
  sizing advice — that a top-up should be sized against the *Eigenanteil* in a *Pflegeheim* rather
  than against a round number — which is the reasoning delib's `[std]` *vereinbarte Rente* of
  1 000 € per month follows. Any specific recommended amount is `[unverified]`.

  `[unverified]`.

### S13 — Comparison portals: Verivox, Check24
- Publisher: Verivox GmbH; CHECK24 Vergleichsportal GmbH — **secondary**. Doc type: quote engines.
  URL: not established
- Content: the only public sources that produce a premium for a named age, benefit and option set
  on demand, and therefore the natural corroboration for section 23's premium band. **None was
  queried** — no egress and no search when this file was drafted, and deliberately not queried in
  the pass of 2026-08-30 either, a portal quotation being generated per enquiry rather than
  published — so that band rests on the arithmetic set out there and is `[std]`, not `[S13]`. Portals cover *Pflegetagegeld* far more thoroughly than *Pflegerente*;
  whether either portal quotes *Pflegerente* at all was not established (gap 5).

### S14 — Ratings agencies: Morgen & Morgen, Franke und Bornberg, Assekurata
- Publisher: MORGEN & MORGEN GmbH; Franke und Bornberg GmbH; ASSEKURATA Assekuranz Rating-Agentur
  GmbH — **secondary**
- Doc type: product ratings and market studies
- URL: not established
- Content: the three agencies that rate German biometric and life products and publish the ratings
  the market quotes. Franke und Bornberg and Morgen & Morgen rate *Pflegezusatzversicherung*
  wordings clause by clause and are therefore the best public route to the observed **range** of
  *Leistungsstaffel*, *Wartezeit*, *Karenzzeit* and *Nachprüfung* terms — precisely the ranges this
  file has to standardise. Assekurata publishes the annual *Überschussbeteiligung* market study that
  fixes declared rates. **Nothing from any of them was retrieved**, and the ranges in the variation
  table below are `[std]`/`[unverified]` reconstructions, not rating data (gap 6).

### S15 — *Pflege-Bahr* tariff conditions of a *geförderter Tarif*
- Publisher: an individual German *Krankenversicherer*
- Doc type: the AVB and *Tarifbedingungen* of a state-subsidised *Pflegetagegeld* tariff, which must
  satisfy § 127 SGB XI to attract the *Zulage* [R8]
- URL: not established
- Content: the document class in which the statutory minimum design of § 127 SGB XI appears as
  contract terms — no *Gesundheitsprüfung*, no *Risikozuschlag*, no *Leistungsausschluss*, a
  *Wartezeit*, and a benefit grid whose top step is at least 600 € per month with the lower
  *Pflegegrade* at fixed fractions of it. This is the **only** place in German private LTC where a
  *Leistungsstaffel* is prescribed by statute, which is why it anchors the ranges in section 7 even
  though it belongs to a different product form. Every figure attributed to it is `[R8][unverified]`.

### S16 — PKV-Verband, *Zahlenbericht der privaten Krankenversicherung* and the association's
  *Pflegezusatzversicherung* statistics
- Publisher: PKV-Verband — **secondary for product terms, primary for market counts**
- Doc type: annual statistical report and standing statistics pages
- URL: not established
- Content: the only public counting of German private LTC top-up contracts, split between
  *geförderte* (*Pflege-Bahr*) and *ungeförderte* business. Two cautions matter more than any
  number: it counts **health-insurance** contracts, so *Pflegetagegeld* and *Pflegekosten* are in
  and ***Pflegerentenversicherung*, written by *Lebensversicherer*, is not**; and it counts
  contracts, not insured persons. Any figure of this class is `[unverified]` (gap 7).

---

## Regulatory and actuarial references

Same drafting conditions as the primary sources, and the same two-stage record: the entries are
left as written, and the pass of 2026-08-30 is recorded at the foot of this file. **Twenty of the
twenty-four were read on that date** — SGB XI, VVG and VVG-InfoV, VAG and HGB, DeckRV, KVAV, EStG
and SGB XII as canonical XML with each law's `Stand`, and the DAV, Destatis, vdek, PKV and GDV
material as PDFs or HTML. [R16] and [R17] were not; [R9] and [R10] are amending acts that were not
opened as acts. Canonical URLs are given where the form is well known and marked `[unverified]`;
elsewhere `URL: not established`. **Where a retrieved document contradicts an entry, the pass
section says so and governs.**

### R1 — SGB XI, *Elftes Buch Sozialgesetzbuch — Soziale Pflegeversicherung*
- Publisher: Bundesministerium der Justiz / juris, via `gesetze-im-internet.de`
- URL: `https://www.gesetze-im-internet.de/sgb_11/` `[unverified]`
- Content: the statute that creates the *soziale Pflegeversicherung* as the fifth pillar of German
  social insurance. Enacted by the *Pflege-Versicherungsgesetz* (PflegeVG); benefits for care at
  home began in **April 1995** and for *vollstationäre* care in **July 1996** `[unverified]`. Two
  design principles govern everything downstream and are not `[unverified]`, because they are the
  statute's structure rather than a figure: **membership follows health insurance** — everyone in
  the *gesetzliche Krankenversicherung* is in the SPV, everyone in the *private Krankenversicherung*
  must hold the PPV of § 23 [R7] — and the scheme is a **Teilleistungssystem**: it pays defined
  amounts per *Pflegegrad*, not the cost of care, and the residue falls on the insured person. The
  private market this file describes exists entirely because of the second principle.
- Contribution rate: **3,6 %** of assessable earnings from 1 January 2025, shared between employer
  and employee, with a childless surcharge of **0,6** percentage points and reductions of **0,25**
  percentage points per child for the second to the fifth child `[unverified]` — the reductions and
  the surcharge in their present shape date from the PUEG of 2023 [R10]. **Whether the rate changed
  again with effect from 1 January 2026 was not established** (gap 8). Saxony's employer/employee
  split differs `[unverified]`.

### R2 — SGB XI § 14 (*Begriff der Pflegebedürftigkeit*) and § 15 (*Ermittlung des Grades der
  Pflegebedürftigkeit*, the *Pflegegrade*)
- URL: `https://www.gesetze-im-internet.de/sgb_11/__14.html`,
  `https://www.gesetze-im-internet.de/sgb_11/__15.html` `[unverified]`
- Content: the two provisions that define the insured event of every German LTC product, public or
  private.
  - **§ 14** defines *Pflegebedürftigkeit* as a health-related impairment of *Selbstständigkeit* or
    of abilities requiring help from others and expected to last **at least six months**
    `[unverified]`. The decisive reform of 2017 [R9] replaced the old measure — minutes of care
    time — with a measure of **independence across six areas of life**, bringing cognitive and
    psychiatric impairment, above all dementia, into the assessment on equal terms with physical
    impairment. That is why recognised *Pflegebedürftige* rose sharply after 2017 and why pre-2017
    incidence data cannot be used for pricing without adjustment.
  - **§ 15** converts the assessment into a *Pflegegrad*. Six *Module* are scored, weighted and
    summed to *gewichtete Punkte* on a 0-to-100 scale, and the *Pflegegrad* follows from the total.
    Module weights `[unverified]`: *Mobilität* **10 %**; *kognitive und kommunikative Fähigkeiten*
    together with *Verhaltensweisen und psychische Problemlagen* **15 %** — the two are assessed
    separately and the **higher** of the two enters the total; *Selbstversorgung* **40 %**;
    *Bewältigung von und selbständiger Umgang mit krankheits- oder therapiebedingten Anforderungen
    und Belastungen* **20 %**; *Gestaltung des Alltagslebens und sozialer Kontakte* **15 %**. Two
    further areas — *außerhäusliche Aktivitäten* and *Haushaltsführung* — are assessed for care
    planning but **do not enter the score** `[unverified]`.
  - Thresholds on the weighted 0-to-100 scale `[unverified]`: *Pflegegrad* **1** from **12,5** to
    under **27** points (*geringe Beeinträchtigung der Selbstständigkeit*); **2** from **27** to
    under **47,5** (*erhebliche*); **3** from **47,5** to under **70** (*schwere*); **4** from **70**
    to under **90** (*schwerste*); **5** from **90** to **100** (*schwerste Beeinträchtigung mit
    besonderen Anforderungen an die pflegerische Versorgung*).
  - A separate route to *Pflegegrad* 5 exists for people with *besondere Bedarfskonstellationen*
    irrespective of the point total `[unverified]`.

### R3 — SGB XI §§ 36, 37, 38 (*Pflegesachleistung*, *Pflegegeld*, *Kombinationsleistung*)
- URL: `https://www.gesetze-im-internet.de/sgb_11/__36.html`, `.../__37.html`, `.../__38.html`
  `[unverified]`
- Content: the benefits for care **at home**, where roughly five in six *Pflegebedürftige* are cared
  for. § 36 provides *Pflegesachleistung* — professional care bought from an approved
  *Pflegedienst*, capped in euro per month by *Pflegegrad*. § 37 provides *Pflegegeld* — a cash sum
  paid to the *Pflegebedürftige* to pass on to whoever cares for them informally, at roughly 44 %
  of the corresponding *Sachleistung* `[unverified]`, conditional on periodic advisory visits.
  § 38 allows the two to be **combined pro rata**: drawing x % of the *Sachleistung* entitlement
  leaves (100 − x) % of the *Pflegegeld*. ***Pflegegrad* 1 receives neither** `[unverified]`. The
  amounts in force are tabulated in section 3 below.

### R4 — SGB XI § 43 (*vollstationäre Pflege*) and § 43c (*Leistungszuschläge*)
- URL: `https://www.gesetze-im-internet.de/sgb_11/__43.html`, `.../__43c.html` `[unverified]`
- Content: § 43 sets the monthly amount the SPV pays towards care in a *Pflegeheim*, by
  *Pflegegrad*, with *Pflegegrad* 1 receiving only a small flat contribution. The amount is a
  **contribution to the care-related cost only**: *Unterkunft und Verpflegung*, *Investitionskosten*
  and any *Ausbildungsumlage* are the resident's in full, and so is whatever care-related cost the
  contribution does not meet. Since 2017 [R9] the care-related residue is the
  **einrichtungseinheitlicher Eigenanteil (EEE)** — *identical for* Pflegegrade *2 to 5 within one
  facility*, so that a resident's own payment no longer rises when their condition worsens
  `[unverified]`. § 43c, in force since **1 January 2022** `[unverified]`, adds duration-dependent
  *Leistungszuschläge* that reduce the EEE the longer the resident has been in the facility; the
  steps were raised from **1 January 2024** to **15 %** in the first twelve months, **30 %** in
  months 13–24, **50 %** in months 25–36 and **75 %** from month 37 `[unverified]`, against
  originally 5 / 25 / 45 / 70 % `[unverified]`. The EEE and these *Zuschläge* together are the
  arithmetic of the *Versorgungslücke* (section 4).

### R5 — SGB XI § 45b (*Entlastungsbetrag*), § 39 (*Verhinderungspflege*), § 42 (*Kurzzeitpflege*),
  and the *gemeinsamer Jahresbetrag*
- URL: `https://www.gesetze-im-internet.de/sgb_11/__45b.html`, `.../__39.html`, `.../__42.html`
  `[unverified]`
- Content: the secondary benefit heads. The *Entlastungsbetrag* is a small monthly earmarked amount
  available in **every** *Pflegegrad* including 1, usable for approved relief services rather than
  paid in cash `[unverified]`. *Verhinderungspflege* funds substitute care when the informal carer
  is unavailable; *Kurzzeitpflege* funds short residential stays. From **1 July 2025** the two were
  merged into a single **gemeinsamer Jahresbetrag** for *Pflegegrade* 2 to 5 `[unverified]`, which
  removed the previous rules on transferring budget between them. These heads do not close the
  residential funding gap and are recorded for completeness rather than for the model.

### R6 — SGB XI § 18 (*Begutachtung*) and the *Begutachtungs-Richtlinien* (BRi) of the
  GKV-Spitzenverband
- URL: not established
- Content: § 18 requires the *Pflegekasse* to have *Pflegebedürftigkeit* assessed, in the SPV by the
  **Medizinischer Dienst (MD)**, formerly *MDK*, and in the PPV by **MEDICPROOF GmbH**, the
  assessment service the private sector maintains `[unverified]`. The operational instrument is the
  **Neues Begutachtungsassessment (NBA)**, standardised in the *Begutachtungs-Richtlinien* issued by
  the GKV-Spitzenverband, which prescribe the questions, the scoring of each *Modul*, the conversion
  to *gewichtete Punkte* and the resulting *Pflegegrad*. Four facts about the assessment are
  load-bearing for a private product and are structural rather than numeric:
  1. The assessment is done by a body that is **not the private insurer**, and the private insurer
     ordinarily accepts its result. That makes the private product's claim decision cheap, and it
     also means the private insurer carries **assessment-regime risk**: any loosening of the BRi or
     of § 15 raises the private product's incidence with no contractual change.
  2. Statutory decision deadlines apply to the *Pflegekasse* `[unverified]`, so the lag between
     onset and a determined *Pflegegrad* is measured in weeks, not years — which is why a
     *Karenzzeit* longer than a few months would be a real benefit reduction and not an
     administrative convenience.
  3. A *Höherstufung* is applied for by the insured person and re-assessed; a *Herabstufung* can
     follow a routine re-assessment. Both propagate straight into a private annuity graded by
     *Pflegegrad*.
  4. Assessment is **not** re-done by grade thresholds in continuous time: a person sits at a grade
     until re-assessed, which makes the discrete-state, discrete-time Markov representation of
     section 17 a good match for how the benefit actually behaves.

### R7 — SGB XI § 23 (*private Pflegepflichtversicherung*)
- URL: `https://www.gesetze-im-internet.de/sgb_11/__23.html` `[unverified]`
- Content: everyone insured in the *private Krankenversicherung* must hold a private LTC cover whose
  benefits are **at least equivalent** to the SPV's, on terms including a *Kontrahierungszwang* and
  a premium cap `[unverified]`. Its relevance here is entirely definitional: it means the *first
  layer* is the same size for a privately insured person as for a statutorily insured one, so **the
  *Versorgungslücke* the *Pflegerente* addresses is the same for both populations**, and the delib
  model needs no separate PPV variant.

### R8 — SGB XI §§ 126 to 130, in particular § 127 (*Pflege-Bahr*)
- URL: `https://www.gesetze-im-internet.de/sgb_11/__127.html` `[unverified]`
- Content: the state-subsidised private LTC top-up introduced by the *Pflege-Neuausrichtungs-Gesetz*
  (PNG) with effect from **1 January 2013** `[unverified]`, universally called ***Pflege-Bahr*** after
  the then health minister. The scheme, as the statute and the associated *Förderbedingungen*
  provide `[unverified]` throughout:
  - **Zulage** **5 €** per month, **60 €** per year, paid to the insurer and credited to the
    contract, administered through the *Zentrale Zulagenstelle für Altersvermögen* `[unverified]`.
  - **Minimum own contribution 10 €** per month, so a subsidised contract costs at least **15 €**.
  - **No underwriting**: no *Gesundheitsprüfung*, no *Risikozuschlag*, no *Leistungsausschluss*, and
    a *Kontrahierungszwang* — anyone aged **18** or over who is not already *pflegebedürftig* must
    be accepted. **Wartezeit** at most **five years**, shortened for care following an accident.
  - **Minimum benefit grid**: at least **600 €** per month in the top *Pflegegrad*, with grades 1
    to 4 at at least **10 / 20 / 30 / 40 %** of it. This is the only *Leistungsstaffel* fixed by
    German statute.
  - **Form restriction**: the subsidised contract must be a **Pflegetagegeld** conducted *nach Art
    der Lebensversicherung* with an ageing provision. ***A Pflegerentenversicherung written by a
    Lebensversicherer cannot be a geförderter Tarif*** — the *Zulage* is not available to the
    modelled product and delib does not implement it.
  - The combination of no underwriting with a fixed 5 € subsidy is the design tension the market
    identifies: the subsidy is small relative to the anti-selection the *Kontrahierungszwang*
    creates, so insurers price the residual defensively and the resulting cover is thin.

### R9 — *Zweites Pflegestärkungsgesetz* (PSG II)
- URL: not established
- Content: the reform act that replaced the three *Pflegestufen* with the five *Pflegegrade*,
  replaced the time-based assessment with the NBA, and introduced the *einrichtungseinheitlicher
  Eigenanteil*, with the operative changes taking effect on **1 January 2017** `[unverified]`. The
  act's own date is given in secondary literature as **21 December 2015** `[unverified]`. Three
  consequences for this product:
  1. **A structural break in every time series.** Counts of *Pflegebedürftige*, incidence rates and
     average durations before and after 2017 are not comparable. Any pricing basis calibrated on
     pre-2017 data — which includes any table derived from experience before that date — needs a
     stated mapping from *Pflegestufen* to *Pflegegrade*.
  2. **A broad transitional mapping** moved existing recipients into the new grades without
     re-assessment, generally *Pflegestufe* I → *Pflegegrad* 2, II → 3, III → 4, with a further step
     for people with recognised *eingeschränkte Alltagskompetenz* `[unverified]`. Older private
     wordings written on *Pflegestufen* had to be mapped by the insurer, and a *Pflegerente* sold
     before 2017 and still in force carries that mapping in its terms.
  3. **The population in cover widened**, because cognitive impairment now scores on equal terms.

### R10 — *Pflegeunterstützungs- und -entlastungsgesetz* (PUEG)
- URL: not established
- Content: the 2023 financing and benefit act `[unverified]`. It raised the contribution rate, put
  the childless surcharge and the per-child reductions into their present shape, uprated the benefit
  amounts in two steps — a first increase with effect from **1 January 2024** and a further
  **4,5 %** with effect from **1 January 2025** `[unverified]` — and legislated the merger of
  *Verhinderungspflege* and *Kurzzeitpflege* into a *gemeinsamer Jahresbetrag* from **1 July 2025**
  `[unverified]`. It also provided for regular future *Dynamisierung* of the amounts `[unverified]`.
  **Whether any further uprating took effect on 1 January 2026 was not established**; every benefit
  figure in section 3 is therefore stamped **2025** and gap 8 records the exposure.

### R11 — VVG — the contract-law provisions this product runs on
- Publisher: Bundesministerium der Justiz / juris
- URLs of the canonical form `https://www.gesetze-im-internet.de/vvg_2008/__169.html` etc.
  `[unverified]`
- Content, provision by provision, described in substance and never quoted:
  - **§ 7 and the VVG-InfoV** — pre-contractual information duties; the source of S5 and S7.
  - **§ 19** — *vorvertragliche Anzeigepflicht*. Remedies for breach are graded by fault and are
    time-barred, generally after five years and ten in cases of intent `[unverified]`. On a
    product whose claims arrive forty years after underwriting, the time bar is what confines the
    *Gesundheitsprüfung*'s effect on incidence to the first decade.
  - **§ 153** — *Überschussbeteiligung*, on a *verursachungsorientiert* method. A biometric-risk
    product's surplus is dominated by the *Risikoergebnis*, not the *Zinsergebnis*.
  - **§ 163** — the narrow route by which a life insurer may adjust a premium: a non-temporary
    change in a calculation basis, with an independent trustee's agreement. **This is the whole of
    a *Lebensversicherer*'s re-rating power.**
  - **§ 165** — *Beitragsfreistellung*: conversion to a paid-up contract at any premium due date,
    the reduced benefit computed from the reserve less any agreed *Stornoabzug*.
  - **§ 169** — *Rückkaufswert*: the actuarial reserve on the tariff bases, acquisition costs
    spread over at least the first **five** years `[unverified]`, and a *Stornoabzug* admissible
    only if agreed, appropriate and **quantified in the contract**. The provision excepts covers
    paying only on death within a defined period, which is why a *Risikolebensversicherung* has no
    surrender value. **Whether that exception reaches a pure-risk *Pflegerente* was not established
    and is gap 9.**
  - **§ 155** — the annual statement (S8) `[unverified]`.
  - **§ 203** — *Beitragsanpassung*, and the point of the whole comparison: **it applies to health
    insurance, not to life insurance.**

### R12 — VAG §§ 138, 139, 146, and § 341f HGB
- URL: `https://www.gesetze-im-internet.de/vag_2016/` `[unverified]`
- Content:
  - **§ 138 VAG** — *Rechnungsgrundlagen*: premiums in life assurance must be calculated on
    prudently chosen assumptions and must be sufficient to meet the undertaking's obligations
    permanently `[unverified]`. For a *Pflegerente* the prudence requirement bites hardest on the
    *Pflegewahrscheinlichkeiten*, which are the least stable of the biometric bases.
  - **§ 139 VAG** — *Überschussbeteiligung* and the *Sicherungsbedarf* mechanics on the
    *Bewertungsreserven* `[unverified]`.
  - **§ 146 VAG** — the *substitutive Krankenversicherung* regime: calculation *nach Art der
    Lebensversicherung*, an *Alterungsrückstellung*, and the § 203 VVG adjustment machinery. Cited
    here only to locate the boundary the *Pflegerente* sits on the other side of.
  - **§ 341f HGB** — the *Deckungsrückstellung* in the commercial accounts, computed prospectively
    on the tariff bases `[unverified]`.

### R13 — DeckRV, *Deckungsrückstellungsverordnung*
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` `[unverified]`
- Content: the regulation that fixes the **Höchstrechnungszins** — the maximum technical interest
  rate for new business — and the **Höchstzillmersatz**, the cap on acquisition costs that may be
  financed through the reserve, expressed as a per-mille of the *Beitragssumme*. The rate applies to
  the cohort at issue and is then locked for the life of the contract. The German sequence
  `[unverified]` throughout: **4,00 %** to mid-2000, **3,25 %** to 2003, **2,75 %** 2004–2006,
  **2,25 %** 2007–2011, **1,75 %** 2012–2014, **1,25 %** 2015–2016, **0,90 %** 2017–2021,
  **0,25 %** 2022–2024, and **1,00 %** for new business from **1 January 2025**. The
  *Höchstzillmersatz* is **25 ‰** of the *Beitragssumme* `[unverified]`. Both are load-bearing for
  this product: a *Pflegerente* discounts benefits that fall on average some thirty-five years after
  issue, so its premium is more interest-sensitive than any other biometric product in delib, and
  its reserve is *gezillmert* like any other level-premium life contract.

### R14 — KVAV, *Krankenversicherungsaufsichtsverordnung*
- URL: not established
- Content: the calculation regulation for private health insurance — the *Alterungsrückstellung*, the
  *Sicherheitszuschlag*, the *Rechnungszins* ceiling for health business, and the auslösende Faktoren
  that trigger a § 203 VVG *Beitragsanpassung* `[unverified]`. Cited here as the regime the
  *Pflegetagegeld* comparison sits under, never as a rule applying to the modelled product.

### R15 — DAV 2008 P — the German *Pflegetafel*
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV)
- Doc type: standard biometric table with a published derivation paper (*Herleitung*), issued by the
  responsible DAV committee
- URL: not established
- Content — the single most important actuarial reference for this product, and the one whose
  contents this library **cannot and does not redistribute**:
  - **DAV 2008 P is the German market's standard table for LTC business calculated *nach Art der
    Lebensversicherung***, covering the *Pflegerente* written by life insurers and the
    *Pflegetagegeld* written on the life chassis by health insurers `[unverified]`.
  - It is a **multi-state** table, not a single decrement series: it has to supply
    *Pflegewahrscheinlichkeiten* by sex, attained age and grade of entry; transition probabilities
    between grades; *Reaktivierungswahrscheinlichkeiten*; and — decisively — **separate mortality
    for active lives and for lives in care, by grade**.
  - It was constructed on the pre-2017 *Pflegestufen* `[unverified]`, so applying it to the five
    *Pflegegrade* requires a mapping and any post-2017 recalibration is the insurer's own work.
    **This is the largest single source of basis risk in the product** and is gap 10.
  - **The table is the property of the DAV, is not public, and is not redistributed by this
    library.** delib cites it by name, states what a replacement must preserve (section 17), and
    ships a `[std]` proxy anchored so the worked example reproduces exactly — the same posture
    uklib takes about CMI tables and frlib takes about TH00-02/TF00-02.
  - No effective date, no committee name, no *Sicherheitszuschlag* level and no numeric value from
    the table is asserted anywhere in this file.

### R16 — DAV 2008 T and DAV 2004 R
- Publisher: DAV
- URL: not established
- Content: the standard German mortality tables for covers with a death character (DAV 2008 T) and
  for annuities (DAV 2004 R, with its *Bestand* variant) `[unverified]`. They enter this product in
  two narrow places: the **mortality of active lives** before the LTC risk bites, where the DAV
  2008 P active-life mortality is the primary basis but a DAV 2008 T shape is the natural sanity
  check; and the **Todesfallleistung**, where a death benefit written into a *Pflegerente* is a
  death cover and is priced as one. **Neither table is redistributed here.** DAV 2004 R matters as a
  contrast: an annuity table is built to be prudent about people living *longer*, whereas the
  annuity in payment on a *Pflegerente* is paid to a heavily impaired population whose mortality is
  a multiple of the general population's, so **using an annuity table for a Pflegerente in payment
  would be prudent in the wrong direction and materially overprice the benefit**.

### R17 — BaFin supervisory material on life and LTC business
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht
- URL: not established (`bafin.de` refused)
- Content: BaFin supervises German life and health insurers, approves the responsible actuary's
  function, and publishes *Merkblätter*, *Rundschreiben*, *Fachartikel* and its annual risk review;
  its *Wohlverhaltensaufsicht* strand has concentrated on product cost and customer value.
  **Nothing product-specific to *Pflegerentenversicherung* was located**, and no BaFin statement of
  any kind is cited in this file (gap 11). A reader with a working network should look here first
  for a supervisory expectation about *Pflegetafel* prudence or about the *Nachprüfung*.

### R18 — Destatis, *Pflegestatistik*
- Publisher: Statistisches Bundesamt (Destatis)
- Doc type: biennial statutory statistics under SGB XI, reference date in December of the survey
  year, published with a lag
- URL: not established
- Content: the authoritative count of *Pflegebedürftige* in Germany, broken down by *Pflegegrad*, by
  care setting (*zu Hause* versus *vollstationär*), by age and by sex, together with counts of
  *Pflegeheime*, *Pflegedienste* and staff. Figures used in section 21 are `[unverified]`
  reconstructions from memory of this series and are **not** to be treated as read from it. Two
  cautions attach to the series itself and are structural: it counts **people receiving benefits**,
  which after 2017 includes a large *Pflegegrad* 1 population receiving almost nothing in cash; and
  its 2017 break [R9] makes it discontinuous.

### R19 — Destatis, *Pflegevorausberechnung*
- Publisher: Destatis
- URL: not established
- Content: the official projection of the number of *Pflegebedürftige* under stated assumptions
  about prevalence and demography. Its qualitative result is not in doubt and is the whole
  commercial case for the product: **the number of *Pflegebedürftige* rises materially over the next
  three decades, driven by the baby-boom cohorts reaching the ages at which prevalence is high**,
  with the steepest increase in the very oldest ages where prevalence exceeds one in two. Specific
  projected counts and dates are `[unverified]` and appear in section 21 with that tag.

### R20 — vdek and BMG material on the *Eigenanteil* in *Pflegeheimen*
- Publisher: Verband der Ersatzkassen e. V. (vdek); Bundesministerium für Gesundheit
- Doc type: the twice-yearly vdek series on the average resident payment, split into the
  care-related *EEE*, *Unterkunft und Verpflegung*, *Investitionskosten* and *Ausbildungsumlage*,
  by *Bundesland*
- URL: not established
- Content: this is the number the private product is sold against, and the series that shows it
  rising faster than the statutory benefit. Its structure matters as much as its level: **only the
  *EEE* component is reduced by the § 43c *Leistungszuschläge* [R4], and only the *EEE* is equalised
  across *Pflegegrade* 2 to 5** — *Unterkunft und Verpflegung* and *Investitionskosten* are neither
  capped nor subsidised and are the fastest-growing components. Levels are `[unverified]` and appear
  in section 4.

### R21 — PKV-Verband statistics on *Pflegezusatzversicherung* and *Pflege-Bahr*
- Publisher: PKV-Verband
- URL: not established
- Content: as S16, from the regulatory-reference side: the annual counts of subsidised and
  unsubsidised private LTC top-up contracts, the *Zulage* volume, and the associated commentary.
  The **structural** finding, which does not depend on a figure, is that *Pflege-Bahr* take-up rose
  quickly in its first three or four years and then **stopped growing**, and that the unsubsidised
  market is several times larger. Section 22 records the reasons.

### R22 — GDV life-market statistics
- Publisher: GDV
- URL: not established
- Content: the annual life-market series — new business and in-force by product family, premium
  income, and the *Stornoquote*. Its relevance here is entirely negative and worth stating plainly:
  **the GDV series does not carve out *Pflegerentenversicherung* as a reported product family** on
  the evidence available to this file, so **there is no sourced count of German *Pflegerente*
  contracts in force anywhere in this research** (gap 12). The market-size statement in section 22
  is therefore qualitative.

### R23 — EStG — the tax provisions
- Publisher: Bundesministerium der Justiz; BMF for the administrative guidance
- URL: `https://www.gesetze-im-internet.de/estg/` `[unverified]`
- Content, provision by provision, all `[unverified]` as to numbering:
  - **§ 10 Abs. 1 Nr. 3 and Nr. 3a EStG** — *Vorsorgeaufwendungen*. Contributions to the statutory
    LTC scheme and to a *Basiskrankenversicherung* are deductible in full under Nr. 3; contributions
    to a **private LTC top-up**, including a *Pflegerente*, fall under Nr. 3a as *sonstige
    Vorsorgeaufwendungen* and are deductible only within an annual ceiling of **1 900 €** for
    employees and pensioners and **2 800 €** for the self-employed `[unverified]`. Because the Nr. 3
    contributions are counted first and usually exhaust that ceiling on their own, **the deduction
    is worthless for most buyers in practice**. This is the honest statement the product
    specification must carry, and it is the reason the *Pflege-Bahr* *Zulage* [R8] was designed as a
    direct subsidy rather than as a further deduction.
  - **§ 3 Nr. 1a EStG** — exemption for benefits from a *Krankenversicherung*, a *Pflegeversicherung*
    and the statutory accident insurance `[unverified]`. This is what makes *Pflegetagegeld*
    benefits tax-free. **Whether it reaches a *Pflegerente* paid by a *Lebensversicherer* was not
    established and is gap 13** — the competing analysis taxes a lifelong care annuity at the
    *Ertragsanteil* under § 22 EStG, as a *Berufsunfähigkeitsrente* is taxed.
  - **§ 22 Nr. 1 EStG** — the *Ertragsanteil* taxation of *Leibrenten*, the competing analysis just
    described `[unverified]`.
  - **§ 20 Abs. 1 Nr. 6 EStG** — the taxation of life-assurance benefits, relevant only to a
    *Todesfallleistung* or a surrender payment out of a *Pflegerente* `[unverified]`. Death benefits
    are ordinarily outside income tax; *Erbschaftsteuer* may apply where the benefit passes to
    someone other than the policyholder's estate.

### R24 — SGB XII §§ 61 to 66 (*Hilfe zur Pflege*) and the *Angehörigen-Entlastungsgesetz*
- URL: `https://www.gesetze-im-internet.de/sgb_12/` `[unverified]`
- Content: the means-tested backstop that pays what the resident cannot, after income and all but a
  small *Schonvermögen* are used up. Two facts make it directly relevant. **A private *Pflegerente*
  with a *Rückkaufswert* is realisable assets** in the means test before the claim, and the annuity
  is **income** during it `[unverified]`, so a contract with no surrender value is on that reasoning
  the more robust design for a buyer whose likely destination is social assistance — an argument for
  the pure-risk variant that has nothing to do with price. And the **Angehörigen-Entlastungsgesetz**,
  in force from **1 January 2020** `[unverified]`, limits adult children's *Elternunterhalt*
  liability to children with annual gross income above **100 000 €** `[unverified]`, removing the
  most commonly cited motive for buying private LTC cover from all but high-earning families and
  shifting the sales argument to protecting the buyer's own assets. Any statement about the effect
  on sales volumes is `[unverified]`.

---

## Extracted facts, organised by mechanic

Every figure below carries its year and a tag. Where the mechanic is certain and the level is not,
the level is a `[std]` parameter with its rationale stated, never a citation.

### 1. Where the product sits: the three layers of German LTC funding

- German long-term care is funded in **three layers**, and the *Pflegerentenversicherung* is the
  third: **compulsory statutory cover** — the SPV of SGB XI [R1], or the PPV of § 23 SGB XI for
  the privately health-insured [R7] — paying **defined amounts per *Pflegegrad***, not the cost of
  care; **the insured person's own resources**; and **voluntary private top-up** or, failing that,
  means-tested *Hilfe zur Pflege* [R24].
- The first layer is a ***Teilleistungssystem*** by design [R1]: it was legislated in 1994 as a
  partial cover and no amendment since has changed that. It is the scheme's constitutive choice,
  and it is the reason the third layer exists as a market at all.
- **The gap is largest in *vollstationäre* care** [R4][R20]. At home, *Pflegegeld* plus family
  labour meets much of the need; in a *Pflegeheim* the resident pays a four-figure monthly sum
  indefinitely (section 4).
- The *Pflegerente* is therefore an income-replacement-shaped product aimed at a **cost** that
  arises very late in life, lasts years rather than decades, and ends on death. That combination —
  late onset, short duration, high mortality in the paying state — makes its actuarial shape
  unlike every other product in delib.

### 2. The statutory trigger: *Pflegebedürftigkeit* and the five *Pflegegrade*

- **Since 1 January 2017 there are five *Pflegegrade***, replacing the three *Pflegestufen* plus
  *Härtefall* of the old regime [R9]`[unverified]` as to the date. Every private LTC wording written
  since then grades its benefit on them.
- **The concept measures *Selbstständigkeit*, not care minutes** [R2]. § 14 SGB XI defines
  *Pflegebedürftigkeit* as a health-related impairment of independence or of abilities that requires
  help from others and is expected to last at least **six months** `[R2][unverified]`.
- **The assessment instrument is the *Neues Begutachtungsassessment* (NBA)** [R6], applied by the
  *Medizinischer Dienst* for the SPV and by MEDICPROOF for the PPV `[R6][unverified]`.
- **Module and weights** `[R2][unverified]`:

| Modul | Content | Weight in the total |
|---|---|---|
| 1 | *Mobilität* | 10% |
| 2 | *Kognitive und kommunikative Fähigkeiten* | 15% — modules 2 and 3 are scored separately and only the **higher** enters |
| 3 | *Verhaltensweisen und psychische Problemlagen* | (shares the 15% with module 2) |
| 4 | *Selbstversorgung* | 40% |
| 5 | *Bewältigung von und selbständiger Umgang mit krankheits-/therapiebedingten Anforderungen* | 20% |
| 6 | *Gestaltung des Alltagslebens und sozialer Kontakte* | 15% |
| 7 | *Außerhäusliche Aktivitäten* | assessed, **not scored** |
| 8 | *Haushaltsführung* | assessed, **not scored** |

- **Thresholds on the weighted 0-to-100 point scale** `[R2][unverified]`:

| *Pflegegrad* | Weighted points | Description |
|---|---|---|
| 1 | 12.5 to under 27 | *geringe Beeinträchtigung der Selbstständigkeit* |
| 2 | 27 to under 47.5 | *erhebliche Beeinträchtigung* |
| 3 | 47.5 to under 70 | *schwere Beeinträchtigung* |
| 4 | 70 to under 90 | *schwerste Beeinträchtigung* |
| 5 | 90 to 100 | *schwerste Beeinträchtigung mit besonderen Anforderungen an die pflegerische Versorgung* |

- A separate route to *Pflegegrad* 5 exists for defined *besondere Bedarfskonstellationen*
  irrespective of the point total `[R2][unverified]`.
- **Module 4, *Selbstversorgung*, carries 40 % of the weight on its own** — washing, dressing,
  feeding, continence. A reader coming from a US or UK LTC product will recognise the ADL trigger
  inside the German scoring but should not equate them: the instrument reaches grade 2 on moderate
  impairments spread across several modules that no two-ADL-failure trigger would catch, and it
  scores dementia through modules 2, 3 and 5 with no physical impairment at all.
- **Consequences for a private product, all structural:** the private insurer does **not** define
  the insured event — the state does, and re-defines it [R9], so the insurer carries **definition
  risk** no wording can hedge; the private insurer does **not** assess the claim, the MD or
  MEDICPROOF does [R6], which makes claims administration cheap and disputes rare compared with
  *Berufsunfähigkeit*; and a *Pflegegrad* is a **step function of a continuous state**, re-assessed
  episodically [R6], which is exactly a discrete-state, discrete-time Markov chain and is why the
  model of section 17 is the natural representation rather than an approximation.

### 3. Statutory benefit amounts by *Pflegegrad* — the first layer, quantified

All amounts **as in force from 1 January 2025**, per calendar month unless stated, and all
`[unverified]`: no figure below was confirmed by any retrieved document or search result, and
whether any of them changed on 1 January 2026 was not established (gap 8).

**Care at home** `[R3][unverified]`:

| *Pflegegrad* | *Pflegegeld* (cash, informal care) | *Pflegesachleistung* (benefit in kind) |
|---|---|---|
| 1 | none | none |
| 2 | 347.00 EUR | 796.00 EUR |
| 3 | 599.00 EUR | 1,497.00 EUR |
| 4 | 800.00 EUR | 1,859.00 EUR |
| 5 | 990.00 EUR | 2,299.00 EUR |

**Care in a *Pflegeheim*** — the SPV's contribution to the **care-related** cost only
`[R4][unverified]`:

| *Pflegegrad* | SPV contribution, *vollstationär* |
|---|---|
| 1 | 125.00 EUR (a flat contribution, not a graded benefit) |
| 2 | 805.00 EUR |
| 3 | 1,319.00 EUR |
| 4 | 1,855.00 EUR |
| 5 | 2,096.00 EUR |

**Secondary heads** `[R5][unverified]`: *Entlastungsbetrag* **131,00 €** per month in every grade
including 1, earmarked and not payable in cash; *Verhinderungspflege* and *Kurzzeitpflege* merged
into a **gemeinsamer Jahresbetrag** of the order of **3 500 €** a year for grades 2 to 5 from
1 July 2025; consumable *Pflegehilfsmittel* of the order of **40 €** a month.

Three readings of these tables that the product specification needs:

1. ***Pflegegrad* 1 is, for cash purposes, uninsured by the state** — 125 € towards a *Pflegeheim*
   and an earmarked 131 € *Entlastungsbetrag*, nothing else `[R3][R4][R5][unverified]`. That is why
   most private *Leistungsstaffeln* also pay nothing, or a token, at grade 1 (section 7).
2. **The *Pflegegeld* is roughly 44 % of the corresponding *Sachleistung*** at every grade
   `[R3][unverified]` — 43.6 %, 40.0 %, 43.0 %, 43.1 % across grades 2 to 5. The state pays
   informal carers substantially less than professional ones, which is what makes the
   *Angehörigenpflege* model viable and why five in six *Pflegebedürftige* are cared for at home.
3. **The residential contribution at grade 5 (2 096 €) is *lower* than the home *Sachleistung* at
   grade 5 (2 299 €)** `[R3][R4][unverified]`. The scheme does not scale its residential
   contribution to the price of a *Pflegeheim*; the facility sets the price and the residue falls
   on the resident. That asymmetry is the *Versorgungslücke*.

### 4. The *Eigenanteil* and the *Versorgungslücke* — the number the product is sized against

- A resident of a German *Pflegeheim* pays **four separate components** `[R4][R20]`: the
  ***einrichtungseinheitlicher Eigenanteil* (EEE)**, the care-related cost the SPV contribution
  does not meet, **identical for *Pflegegrade* 2 to 5 within one facility** since 2017 [R9];
  ***Unterkunft und Verpflegung***; ***Investitionskosten***; and an ***Ausbildungsumlage*** where
  levied. The last three are met by the resident in full.
- Only component 1 is reduced by the § 43c ***Leistungszuschläge***, and only by duration of stay:
  **15 % / 30 % / 50 % / 75 %** in months 1–12, 13–24, 25–36 and from 37 respectively, on the 2024
  step-up `[R4][unverified]`. Components 2, 3 and 4 are neither capped nor subsidised, and are the
  fastest-growing part of the bill `[R20][unverified]`.
- **Level.** The average total monthly payment by a resident in the **first year** of a stay was of
  the order of **2 900 € to 3 200 €** during 2025, with the EEE component of the order of
  **1 300 € to 1 500 €**, board and lodging of the order of **900 €** and investment costs of the
  order of **500 €** `[R20][unverified]`. Regional dispersion is wide — Nordrhein-Westfalen and
  Baden-Württemberg at the top and several eastern *Länder* several hundred euro below
  `[R20][unverified]`. **These are the least reliable figures in this file** and are recorded as
  gap 15; they are used only to argue the order of magnitude of the `[std]` *vereinbarte Rente*.
- **The gap arithmetic**, worked at the order of magnitude and tagged as the construction it is:

| Line | Amount, 2025 | Tag |
|---|---|---|
| Average total resident payment, *Pflegeheim*, first year of stay | about 3,000.00 EUR/month | [R20][unverified] |
| Less: net *gesetzliche Rente* of a median new retiree | of the order of 1,200.00 to 1,600.00 EUR/month | [unverified] |
| **Residual funded from savings, family or *Hilfe zur Pflege*** | **of the order of 1,400.00 to 1,800.00 EUR/month** | [std] arithmetic on the two lines above |

- That residual is why the market sells *Pflegerenten* of **1 000 € to 1 500 €** per month, and it
  is the rationale for delib's `[std]` *vereinbarte Rente* of **1 000 € per month** (section 23):
  a round number at the lower end of the band, defensible as the amount that closes most of the gap
  for a resident with an average pension, and small enough that the resulting premium is
  recognisably a mass-market figure.
- **The gap widens over time.** The statutory amounts are uprated episodically by legislation
  [R10] while the *Eigenanteil* rises with care-sector wage costs every year `[R20][unverified]`;
  every uprating is a one-off catch-up against a continuous drift. This is the structural argument
  for the ***Leistungsdynamik*** option (section 11) and against a level annuity in payment.
- **The duration matters as much as the level.** Because the § 43c *Zuschläge* rise with length of
  stay, the *Eigenanteil* is **highest in the first year** and falls thereafter `[R4][unverified]`,
  so a constant annuity progressively over-covers the gap. No German wording is known to offer a
  decreasing care annuity, and delib does not model one; the product specification says why.

### 5. The three private forms, and why the *Pflegerente* is one of them

| | *Pflegetagegeldversicherung* | *Pflegekostenversicherung* | *Pflegerentenversicherung* |
|---|---|---|---|
| Legal branch | private Krankenversicherung | private Krankenversicherung | **Lebensversicherung** |
| Benefit form | agreed daily/monthly cash amount per *Pflegegrad*, no proof of spend | reimbursement of a percentage of residual actual cost, invoices required | agreed **monthly annuity** per *Pflegegrad*, no proof of spend |
| Legal character | *Summenversicherung* | indemnity | *Summenversicherung* |
| Premium re-rating | **possible** under § 203 VVG on a trustee-approved trigger | possible | **not possible** save under the narrow § 163 VVG route |
| Ageing provision | *Alterungsrückstellung* where written *nach Art der Lebensversicherung*; **none** where written *nach Art der Schadenversicherung* | as *Pflegetagegeld* | ***Deckungsrückstellung*** always |
| Surrender value | none in substance | none | **yes**, § 169 VVG, subject to gap 9 |
| Waiver of premium in claim | usual | usual | **usual, and contractual** |
| Death benefit | rare | none | **common option** |
| *Pflege-Bahr* eligible | **yes — the only eligible form** | no | **no** |
| Market share by contracts | **dominant** | negligible | small |
| Average premium | lowest | — | **highest** |

Tags: the branch, benefit-form, re-rating and *Pflege-Bahr* rows follow from [R11][R14][R8] and are
structural, not `[unverified]`. The market-share and average-premium rows are `[unverified]`.

- **The load-bearing difference is the re-rating power.** A *Pflegetagegeld* is health business: on
  a deviation beyond the *auslösender Faktor* the insurer may raise the premium with a trustee's
  agreement under § 203 VVG [R11][R14]. A *Pflegerente* is life business: the premium is fixed at
  issue and the only route is § 163 VVG, which requires a permanent, unforeseeable change in a
  calculation basis and is used very rarely [R11]. **A buyer at 45 who wants to know what the cover
  will cost at 80 gets an answer from a *Pflegerente* and does not from a *Pflegetagegeld*.** Every
  consumer comparison of the two reduces to that trade, and so does the price difference: the
  *Pflegerente* costs more because the insurer, not the policyholder, carries the basis risk on a
  fifty-year view of a biometric table built on a superseded assessment regime [R15].
- **The second difference is the ageing provision.** A *Pflegetagegeld* written *nach Art der
  Schadenversicherung* has **none**, so its premium follows attained-age risk upward and becomes
  unaffordable at exactly the ages the cover is needed; consumer bodies single that form out as the
  one to avoid [S11]`[unverified]`. A *Pflegerente* cannot take it: as a *Lebensversicherung* it is
  calculated with a prospective reserve by construction (section 14).
- **The third is the surrender value**, which cuts both ways: it is the only one of the three from
  which a policyholder recovers anything on lapse [R11], and it makes the contract realisable
  assets in a *Hilfe zur Pflege* means test [R24].

### 6. *Pflege-Bahr*: what it is, why it matters here, and why it is not this product

- **Design** [R8], every figure `[unverified]`: a **5 €** monthly *Pflegevorsorgezulage* on top of a
  minimum own contribution of **10 €**; no *Gesundheitsprüfung*, no *Risikozuschlag*, no
  *Leistungsausschluss* and a *Kontrahierungszwang*; entry from age **18**; the applicant must not
  already be *pflegebedürftig*; a *Wartezeit* of at most **five years**; a benefit of at least
  **600 €** per month at the top *Pflegegrad* with the lower grades at at least **10 / 20 / 30 /
  40 %** of it; and the contract must be a *Pflegetagegeld* conducted *nach Art der
  Lebensversicherung*.
- **Why it matters to a *Pflegerente* file** even though a *Pflegerente* cannot be one. It is the
  **only statutory *Leistungsstaffel*** in German private LTC, and the 10/20/30/40/100 grid is the
  reference point every private grid is read against; several unsubsidised *Pflegetagegeld* tariffs
  adopt it outright. It fixes a **statutory floor benefit of 600 € per month** at the top grade,
  about **one fifth** of the *Eigenanteil* of section 4 (`[std]` arithmetic on
  `[R8][R20][unverified]`), which is the whole critique of the scheme. And its no-underwriting
  design is the **natural experiment on anti-selection** in German LTC: the *Kontrahierungszwang*
  fills the subsidised pool with everyone who chose to join, the *Wartezeit* is the only screen,
  and the 5 € subsidy does not compensate.
- **Why take-up stalled.** No statement here is sourced; each is a reasoned market observation
  `[unverified]`. The **subsidy is fixed in nominal terms** at 5 € per month since 2013 and has
  never been uprated, while the *Eigenanteil* it helps meet has risen by well over half [R20]. The
  **benefit is too small to change a decision**: 600 € against a gap of roughly 1 500 € leaves the
  buyer needing further cover anyway, at which point the underwritten tariff is better value per
  euro. The **five-year *Wartezeit*** deters exactly the older buyers for whom the product is most
  relevant. **No underwriting** removes risk selection as a competitive dimension and with it the
  incentive to promote the scheme. Consumer testing has been unenthusiastic [S10]`[unverified]`,
  and distribution economics on a 15 €-per-month contract are negligible. Take-up rose quickly to
  the order of **0,8 to 0,9 million** contracts within the scheme's first three or four years and
  has been **broadly flat since** [R21]`[unverified]`.
- **delib does not implement the *Zulage*.** The *Pflege-Bahr* parameters are recorded because they
  bound the observed range of the *Leistungsstaffel* (section 7) and because the product
  specification must explain, in one paragraph, why a state subsidy that exists for LTC cover is not
  available to the modelled product.

### 7. Benefit structure — the *Leistungsstaffel*

- The contract fixes one number, the ***vereinbarte Pflegerente*** — the monthly annuity payable at
  the **top** *Pflegegrad* — and a **schedule of percentages** of it by grade. Everything else in the
  benefit design is a modifier on that schedule.
- **The observed range across the German market**, reconstructed from market knowledge and **not**
  from any wording; every cell `[unverified]`:

| *Pflegegrad* | Common low | Common high | Notes |
|---|---|---|---|
| 1 | 0% | 10% | Most tariffs insure nothing at grade 1; a minority pay a token step |
| 2 | 10% | 30% | The widest dispersion in the schedule |
| 3 | 30% | 50% | |
| 4 | 60% | 75% | |
| 5 | 100% | 100% | The scaling constant; universally 100% |

- Two grid shapes recur `[unverified]`:
  - the **statutory *Pflege-Bahr* shape**, 10 / 20 / 30 / 40 / 100 [R8], borrowed by tariffs that
    want to say they match the subsidised minimum; and
  - a **flatter, higher shape** in the 0 / 30 / 50 / 75 / 100 region, which is the one a
    *Pflegerente* aimed at the residential gap tends to use, because grades 3 to 5 are where
    residential care actually happens.
- **Setting-dependent benefits.** Older wordings paid the full annuity only for *vollstationäre*
  care and a reduced one for care at home `[unverified]`. Modern practice is to pay **irrespective
  of the care setting**, which is what makes the product a *Summenversicherung* and removes the
  administrative burden of proving where care is given. delib models the setting-independent form
  and says so.
- **delib's `[std]` schedule** and its rationale:

| *Pflegegrad* | delib `[std]` | Rationale |
|---|---|---|
| 1 | 0% | Grade 1 is not a funding event in the statutory scheme either (section 3); insuring it would add incidence-heavy, low-severity claims that dominate the count and not the cost |
| 2 | 30% | Upper end of the observed range: grade 2 is where care at home begins in earnest and where the *Pflegegeld* is smallest relative to need |
| 3 | 50% | Mid-range and the modal market value |
| 4 | 75% | Mid-range |
| 5 | 100% | The scaling constant, universal |

  Tag: **[std]**, observed range as tabulated above `[unverified]`. The schedule is a model
  parameter, read from a CSV with a `provenance` column, so a user with a real *Tarifblatt* can
  substitute a carrier's grid without touching a formula.
- **What the schedule does to the liability.** Time spent at each grade is very unequal: a person
  entering at grade 2 and deteriorating spends most of the spell at grades 2 and 3 and only the
  final months at grade 5 `[unverified]`. The **time-weighted average benefit percentage over a
  spell is therefore far below 100 %** — about **50 %** on the profile of section 23. Two tariffs
  with the same 100 % top step and different middle steps differ in expected cost by more than the
  headline suggests, so comparing on the *vereinbarte Rente* alone is misleading.

### 8. The benefit trigger and its administration

- **The trigger is the *Pflegegrad*** determined under §§ 14, 15 SGB XI [R2], normally established
  by the MD for the statutorily insured or by MEDICPROOF for the privately insured [R6]. Wordings
  provide a fallback assessment by a physician the insurer appoints where the insured is covered by
  neither `[S4][unverified]`.
- **Payment starts** from the beginning of the month in which the *Pflegegrad* takes effect, or from
  the month after, subject to any *Karenzzeit* `[S4][unverified]`. Because the statutory decision
  itself is often backdated to the date of application, a wording that keys off the *effective date*
  of the *Pflegegrad* rather than the *decision date* pays earlier; which of the two a tariff uses is
  a real term difference and was not established.
- ***Nachprüfung*.** The insurer may require periodic evidence that the *Pflegegrad* persists
  `[S4][unverified]`. In practice the evidence is the statutory determination itself, so the
  *Nachprüfung* is a documentation exercise rather than the adversarial re-assessment that
  characterises *Berufsunfähigkeit*. This is the second reason (after section 2) that
  *Pflegerente* claims management is light.
- ***Herabstufung*.** If the *Pflegegrad* falls, the annuity falls to the lower step of the
  *Leistungsstaffel*, and if it falls below the insured threshold the annuity **stops** and the
  premium obligation **revives** `[S4][unverified]`. Some tariffs guarantee that an annuity once
  granted will not be reduced; whether such a guarantee is common was not established (gap 17).
- **Modelling consequence, and a pitfall.** The paying state has **three** exits, not one: death,
  *Herabstufung* to an uninsured grade, and *Herabstufung* to a lower insured grade. Only the first
  is absorbing. A model that treats "in claim" as a single state exited only by death **overstates**
  the liability, and a model that treats every downgrade as a termination **understates** it. The
  delib model carries the grade explicitly for exactly this reason (section 17).

### 9. *Wartezeit* and *Karenzzeit*

- The two are different devices and are routinely confused in consumer material.
  - ***Wartezeit*** runs from **inception of the contract**. Care beginning inside it is not
    covered at all, or is covered only if caused by an accident.
  - ***Karenzzeit*** runs from **the onset of *Pflegebedürftigkeit***. The claim is admitted but the
    annuity does not start until the deferred period has run; some wordings then pay retroactively
    to onset and some do not.
- **Observed levels**, `[unverified]` throughout:

| Device | Underwritten *Pflegerente* | *Pflege-Bahr* [R8] |
|---|---|---|
| *Wartezeit* | commonly **none**; where present, up to **3 years**, and usually waived for accident | up to **5 years** |
| *Karenzzeit* | commonly **none**; where present, **3** or **6** months | not the operative screen |

- **Why the underwritten product usually has no *Wartezeit*.** The *Gesundheitsprüfung* does the
  screening that the *Wartezeit* does in the subsidised product, so where both exist the
  *Wartezeit* is a competitive disadvantage doing very little work. The pairing is near
  deterministic: **no underwriting implies a long *Wartezeit*; underwriting implies none**.
- **delib `[std]`: *Wartezeit* = 0, *Karenzzeit* = 0 in the base run**, both switchable. Rationale:
  the base run models the underwritten mainstream form, in which neither is standard; and a
  *Karenzzeit* of three or six months on a benefit whose expected duration is of the order of four
  years is a second-order effect on the liability (of the order of 6 % to 12 % of the annuity's
  duration) that would obscure the mechanics the model is built to demonstrate. Both are exposed as
  model parameters so a user can switch them on and see the effect, and the technical notes list the
  interaction between a *Karenzzeit* and the high early mortality of section 17 as a modelling
  pitfall: **a deferred period on a population with elevated mortality removes disproportionately
  more claims than the same period would on a healthy population**, because a material share of new
  claimants die inside it.

### 10. *Beitragsbefreiung im Leistungsfall*

- **Premiums are waived while the annuity is payable.** This is standard in the German market for
  *Pflegerenten* and is contractual, not discretionary `[S4]`.
- The details that vary and were not established `[unverified]`:
  - **From which *Pflegegrad*** the waiver runs — usually the lowest grade at which a benefit is
    paid, so that waiver and benefit start together, but some tariffs waive only from a higher grade
    than the one at which the annuity begins.
  - **Whether the waiver is full or proportionate** to the benefit percentage. Full waiver is the
    normal design; a proportionate waiver at grade 2 would be unusual.
  - **Whether the premium revives on *Herabstufung*** below the trigger. It ordinarily does, since
    the waiver is an incident of the claim.
- **delib `[std]`: full waiver, from the first month in which any annuity is payable, revived on
  exit from the paying state.** Rationale: it is the market-standard design, it keeps waiver and
  benefit on one trigger, and it makes the premium stream a function of the same state variable as
  the benefit stream, which is what allows the model to publish a single `check_net_cf()` identity
  reconciling both.
- **The waiver is not a cosmetic term.** On a level-premium contract issued at 45 and claiming at
  82, the waiver removes the remaining premium stream for the whole of the paying period — of the
  order of four years of premium, of the same order as one year of benefit at the modelled levels.
  Its cost sits inside the level premium and is one of the reasons a *Pflegerente* is dearer than a
  *Pflegetagegeld* of nominally equal benefit, where waiver is common but not universal.

### 11. *Dynamik* — indexation before and during claim

- Two distinct options, both offered in the German market, and not to be conflated `[unverified]`:
  ***Beitragsdynamik*** raises the premium before claim by an agreed **3 % to 5 %** a year, buying
  whatever additional *vereinbarte Rente* that premium buys at the attained age without renewed
  underwriting, with a right to decline that lapses permanently after two or three refusals; and
  ***Leistungsdynamik im Leistungsbezug*** raises the annuity in payment by an agreed **1 % to 3 %**
  a year to track care-cost inflation.
- **The second is the economically important one for this product**, and the reasoning is section 4:
  the *Eigenanteil* rises continuously while the statutory benefit is uprated episodically, so a
  level annuity loses ground against the gap it was bought to close throughout a care spell that may
  last a decade. A *Leistungsdynamik* is the only contractual answer.
- **Its cost is much smaller than it looks**, and this is worth stating because it is
  counter-intuitive: the annuity is paid to a population with heavily elevated mortality
  (section 17), so the duration over which the escalation compounds is short. A 2 % escalation on an
  annuity with an expected duration of about four years costs of the order of **4 %** of the
  annuity's value, not the 15 % or 20 % the same escalation would cost on a healthy-life pension.
- **delib `[std]`: both dynamics off in the base run**, both exposed as parameters. Rationale: the
  base run must demonstrate the multi-state benefit machinery cleanly, and a *Beitragsdynamik*
  introduces a second, behaviourally driven premium path (the acceptance rate on each offer) for
  which this corpus supplies no evidence at all. The technical notes carry the *Leistungsdynamik*
  as a switchable escalation and list "escalating the annuity at general-population duration rather
  than at impaired-life duration" as a modelling pitfall.

### 12. *Todesfallleistung* and *Beitragsrückgewähr*

- Many German *Pflegerenten* carry a death benefit, most often in the form of a
  ***Beitragsrückgewähr*** — return of the premiums paid, usually **without interest** and usually
  **net of any annuity already paid** `[S4][unverified]`. Other forms found in the market are a
  fixed *Todesfallsumme* and a benefit equal to the *Deckungskapital* `[unverified]`.
- **What it does to the product, and this is the fact that matters most for delib:**
  - It converts a **pure biometric risk cover into a savings-bearing contract**. The reserve
    required to fund a return of premiums on death at any time is close to the accumulated premium
    itself, so the *Deckungskapital* becomes an order of magnitude larger than the risk reserve
    (section 14).
  - It very likely brings the contract **inside the PRIIPs perimeter**, the benefit no longer being
    payable only on death or incapacity [R25]`[unverified]` (S6, gap 16).
  - It **roughly doubles or more the premium** for the same annuity `[std]` estimate, because the
    death benefit is close to certain to be paid whereas the annuity is not.
  - It makes the *Rückkaufswert* substantial, with the consequences for a *Hilfe zur Pflege* means
    test noted at [R24].
- **delib `[std]`: no *Todesfallleistung* in the base run**, with a *Beitragsrückgewähr* available as
  a switchable option. Rationale: the base run should demonstrate the LTC mechanics, and a return of
  premiums would make the model's cash flows dominated by a savings roll-forward that
  `kapitallebensversicherung` already demonstrates far better. Turning the option on is the model's
  way of showing how large the effect is.

### 13. Premium: level, guaranteed, and the payment-period choice

- **The *Beitrag* is level and is guaranteed for the life of the contract**, subject only to the
  narrow § 163 VVG route [R11]. This is the product's defining commercial property (section 5).
- **Premium-paying period.** Three forms are sold `[unverified]`: **lifelong** payment until death
  or claim; payment to a fixed age, typically **65** or **85**; and a **single premium**
  (*Einmalbeitrag*), used to convert capital into cover. A shortened *Beitragszahlungsdauer* raises
  the level premium and the reserve, and best matches a buyer's earning life.
- **delib `[std]`: level monthly premium payable for life, waived in claim, no
  *Ratenzahlungszuschlag* modelled separately.** Rationale: the monthly grid (`Pflege_DE_S`) makes a
  monthly premium the natural unit; a lifelong period is the form that shows the *Deckungskapital*
  building and running off across the whole of the risk period; and folding the instalment loading
  into the single expense assumption avoids shipping a charge level that no source supports.
- **The premium is struck by equivalence** on the `[std]` bases: the expected present value of
  benefits, waived premiums and expenses equals the expected present value of premiums, at the
  *Rechnungszins*. There is **no published rate card to reproduce** (S9, gap 3), so the model's
  premium is a computed quantity and the notes must sanity-check it against the argued band of
  section 23 rather than against a citation.

### 14. *Deckungskapital*: the ageing-reserve function on a life chassis

- The contract is calculated ***nach Art der Lebensversicherung***: level premium, prospective
  reserve, no ordinary re-rating [R11][R12]. The reserve is a ***Deckungsrückstellung*** under
  § 341f HGB and the DeckRV [R12][R13] — **not** an *Alterungsrückstellung*, which is the private
  health insurance object of § 146 VAG [R12].
- **The economic function is nevertheless identical to an ageing reserve.** The annual probability
  of entering care is negligible before 60, small to 75, and rises steeply thereafter; the level
  premium is far above the risk premium for the first three or four decades and far below it
  afterwards, and the difference accumulates. The precise words to use, and the product
  specification should use them: *the* Deckungskapital *of a* Pflegerente *is an ageing reserve in
  economic function and a* Deckungsrückstellung *in law and in the accounts*.
- **Shape of the reserve.** Issued at 45 with lifelong level premiums, the *Deckungskapital* rises
  monotonically for roughly thirty-five years, **peaks somewhere in the early eighties** where the
  incidence curve crosses the level premium, and then runs off as claims are paid and the survivors
  thin `[std]` reasoning on `[R15][unverified]` incidence shape. Compared with an endowment's
  reserve it is later-peaking and smaller relative to premiums paid; compared with a
  *Risikolebensversicherung*'s it is very much larger, because the risk is back-loaded rather than
  spread.
- ***Zillmerung*** applies as it does to any level-premium life contract: acquisition costs are
  financed through the reserve up to the *Höchstzillmersatz* of **25 ‰** of the *Beitragssumme*
  `[R13][unverified]`, producing a negative reserve in the earliest years. On a lifelong-premium
  *Pflegerente* the *Beitragssumme* is large, so the absolute *Zillmerung* allowance is large and the
  early-duration surrender value is correspondingly poor.
- **Consequences the technical notes must carry.** **Interest sensitivity is the highest in delib**,
  because benefits fall on average some thirty-five years after issue, so a 100 bp change in the
  *Rechnungszins* moves the premium far more than on a term assurance or an endowment. **Lapse is
  profitable early and expensive late**: the reserve released on an early lapse exceeds the
  surrender value paid, and a lapse at 70 removes a policyholder who paid for twenty-five years and
  never reached the risk period — so lapse feeds the premium through the equivalence principle, and
  the notes must state whether the pricing basis is lapse-dependent (delib's is not, per the
  acyclicity rule of the house style). And **the reserve is the object the *Überschussbeteiligung*
  is declared on (section 19) and the object the *Rückkaufswert* is computed from (section 15)**.

### 15. *Rückkaufswert*, *Beitragsfreistellung* and *Stornoabzug*

- **§ 169 VVG** entitles the policyholder to a surrender value on termination, computed as the
  actuarial reserve on the tariff bases, with acquisition costs spread over at least the first five
  years and any *Stornoabzug* admissible only if agreed, appropriate and **quantified in the
  contract** [R11]`[unverified]` as to the five-year rule. **§ 165 VVG** gives an independent right
  to *Beitragsfreistellung*, converting the contract to a paid-up *Pflegerente* at a reduced
  *vereinbarte Rente* computed from the reserve, less any *Stornoabzug* [R11].
- **The open legal question** is whether a **pure-risk** *Pflegerente* — no death benefit, no
  survival benefit — falls inside the § 169 exception for covers paying only on death within a
  defined period. The exception's plain target is *Risikolebensversicherung*; a *Pflegerente* pays on
  an uncertain event that is not death and **does** build a substantial reserve, which argues for
  full § 169 treatment. **This was not established and is gap 9.** delib's posture: model a
  *Rückkaufswert* equal to the *gezillmert* prospective reserve, floored at zero and reduced by a
  contractual *Stornoabzug*, and say in the product specification that the statutory question is
  open and that a carrier's own wording settles it for that carrier.
- **Levels are unsourced.** No *Stornoabzug* for any German *Pflegerenten* tariff was established;
  the German life-market range runs from nil to the order of **5 %** of the *Deckungskapital*,
  sometimes with a capital-market-dependent supplement `[unverified]`. delib ships **`[std]`
  *Stornoabzug* = 0 in the base run** — a non-zero deduction requires a contractual quantification
  this file cannot supply — with the parameter exposed.
- **Practical size.** Because the *Zillmerung* allowance is large and the risk premium in the early
  years is small, the *Rückkaufswert* of a *Pflegerente* is **near zero for the first several years**
  and remains well below premiums paid for a long time. That is the honest thing to tell a buyer, and
  it is the strongest argument for the *Beitragsrückgewähr* option (section 12).

### 16. Charges

- **No charge level of any kind was established for any German *Pflegerenten* tariff.** No
  *Produktinformationsblatt* (S5), no *Verbraucherinformation* (S7) and no *Tarifblatt* (S9) was
  located, and the search channel was unavailable. **Every charge in delib is `[std]`** (gap 2).
- The **structure** is nevertheless certain, because it is the German life-market structure:
  - ***Abschluss- und Vertriebskosten***, a per-mille of the *Beitragssumme*, capped at the
    *Höchstzillmersatz* for the part financed through the reserve `[R13][unverified]` and amortised
    over at least five years for surrender-value purposes [R11].
  - ***Verwaltungskosten***, as a percentage of premium and sometimes of the reserve, plus a
    per-policy element; and a ***Ratenzahlungszuschlag*** for other than annual payment.
  - **Claims administration cost** during the paying period, small here because the trigger is
    determined by a third party (section 8) — materially smaller than on a
    *Berufsunfähigkeitsrente*, where the insurer runs its own *Nachprüfung*.
- **delib `[std]` charge set**, each with its rationale, to be set out in full in the technical
  notes: an acquisition cost expressed as a per-mille of *Beitragssumme* **at or below the 25 ‰
  ceiling**, so that the ceiling binds visibly; a percentage-of-premium administration cost; and a
  small per-annuity-payment claims cost. All three are read from a CSV carrying a `provenance`
  column marking them `[std]`.

### 17. *Rechnungsgrundlagen*: DAV 2008 P and the multi-state model

- **The table.** DAV 2008 P is the German standard basis for LTC business on the life chassis [R15].
  It is a **multi-state** table and it is **not public**; this library cites it and does not
  redistribute it.
- **The state space** a faithful implementation needs:

```
  aktiv  ──►  PG1 ──►  PG2 ──►  PG3 ──►  PG4 ──►  PG5
    │          │        │        │        │        │
    └──────────┴────────┴────────┴────────┴────────┴──►  tot
                    (and, rarely, backwards: Reaktivierung / Herabstufung)
```

- **What the table has to supply** [R15]:
  1. **Pflegewahrscheinlichkeiten** — the probability that an active life aged *x* enters care in
     the year, by sex, by attained age **and by the grade entered**; entry is not uniformly at the
     lowest grade, since a stroke or a fracture can enter directly at grade 3 or 4.
  2. **Deterioration probabilities** between grades, the main driver of the benefit's growth over a
     spell, and **Reaktivierung** — recovery to a lower grade or to the active state, small at the
     ages that matter and non-negligible after acute events at younger ages.
  3. **State-dependent mortality** — separate *q(x)* for active lives and for lives in each grade.
- **The single most load-bearing biometric fact in this file:** the mortality of a
  *Pflegebedürftiger* is a **large multiple** of the mortality of an active life of the same age,
  rising sharply with the grade — of the order of **two to three times at grade 2** and **five to
  ten times at grade 5** `[std]` order-of-magnitude reasoning, `[unverified]` as to any number.
  Three consequences follow, and each is a modelling pitfall:
  - **The annuity in payment is short** — of the order of **three to five years** (section 21), not
    the fifteen to twenty of a healthy-life pension at the same age. Pricing it on **DAV 2004 R**
    [R16] would be prudent in exactly the wrong direction and would overprice the benefit.
  - **Mortality is highest immediately after onset**, especially at grades 4 and 5. That is
    selection *at onset*, not at underwriting, and it makes a *Karenzzeit* bite harder than its
    length suggests (section 9).
  - **Grade and mortality are correlated**, so the model must not apply an average benefit
    percentage to a survival curve computed at an average mortality: the highest-paying state is
    also the shortest-lived. This is the pitfall the technical notes should list first.
- **Selection at underwriting** is a separate effect: the *Gesundheitsprüfung* depresses incidence
  for the first years and decays. On a product whose claims arrive thirty to forty years after
  issue, **underwriting selection is essentially irrelevant to the cost of the benefit** and
  matters only to the early-duration reserve — the opposite of *Berufsunfähigkeit*, where selection
  is a first-order pricing effect.
- **The 2017 break.** DAV 2008 P was built on *Pflegestufen* [R15]`[unverified]`; the trigger it is
  applied to is *Pflegegrade* [R9]. The mapping is the insurer's own work, and the widening of the
  definition in 2017 raised incidence at the lower grades in a way a pre-2017 table cannot capture.
  **This is the largest single basis risk in the product** and is gap 10.
- **delib's proxy.** The model ships a `[std]` transition-rate table with the shape the mechanics
  require — incidence rising steeply above 70, entry distributed across grades, deterioration
  dominant over recovery, and state-dependent mortality as a multiple of an active-life Gompertz
  base — anchored so that the worked example reproduces exactly. The `Data` docstring states the
  anchor. **A replacement table must preserve four properties**: (a) incidence by attained age, sex
  and grade of entry; (b) deterioration dominating recovery above age 75; (c) mortality in care as a
  grade-increasing multiple of active mortality; and (d) rows that sum to one over the state space.

### 18. Underwriting

- **Full *Gesundheitsprüfung*** on the underwritten product `[S4][unverified]`. The question
  catalogue is materially **shorter than a *Berufsunfähigkeit* application's**, because the risk is
  driven by conditions that predict dependency in old age — cardiovascular and cerebrovascular
  disease, diabetes, neurological and psychiatric conditions, early cognitive impairment,
  musculoskeletal disease — rather than by occupation, and **occupation is not a rating factor at
  all**, which is the sharpest single contrast with BU.
- **Outcomes**: acceptance at standard rates; acceptance with a *Risikozuschlag*; acceptance with a
  *Leistungsausschluss* for a named condition; deferral; decline. Existing *Pflegebedürftigkeit* is
  an absolute bar (section 8). **No *Risikozuschlag* scale was established.**
- **Entry ages.** The observed market band is of the order of **18 to 65** at entry, with some
  tariffs writing to **70** and a few, mostly single-premium, beyond `[unverified]`. **Purchase
  behaviour clusters much later than the permitted band**: the product is bought predominantly
  between **45 and 60** `[unverified]`, when the buyer has seen a parent go into care.
- **Sex.** Unisex pricing has been compulsory for EU contracts concluded from **21 December 2012**
  `[unverified]`, and it matters more here than on any other delib product: **women have materially
  higher LTC incidence and materially longer care durations than men**, so the unisex premium
  embeds a cross-subsidy whose size depends on the sex mix written, and that mix is itself
  endogenous to price. The notes carry the basis as a **blended** rate set with a stated `[std]`
  mix and list "pricing unisex on a 50/50 mix while writing 60/40" as a model risk.
- **delib `[std]`: unisex bases blended at 50/50, no *Risikozuschlag*, no *Leistungsausschluss*,
  entry age 45 for the anchor model point.** Rationale for the entry age: it sits at the lower edge
  of the observed purchase cluster, it gives a long enough pre-claim period for the
  *Deckungskapital* to be the interesting object it is, and it makes the worked example's premium
  comparable with the band argued in section 23.

### 19. *Überschussbeteiligung*

- The contract participates in surplus under § 153 VVG [R11] and § 139 VAG [R12] like any other
  German life contract, unless participation is excluded by agreement.
- **The composition is different from an endowment's.** On a *Kapitallebensversicherung* the surplus
  is dominated by the *Zinsergebnis*. On a *Pflegerente* the reserve is smaller relative to the risk
  and the biometric basis is the prudent one, so the ***Risikoergebnis*** — the difference between
  the incidence and mortality assumed and the incidence and mortality experienced — **is the
  dominant component**, with the *Zinsergebnis* second and the *Kostenergebnis* third.
- **Application forms** used in the German market `[unverified]`: *Beitragsverrechnung* (the
  declared surplus reduces the premium called — the dominant form on biometric-risk products);
  *verzinsliche Ansammlung*; and a *Bonus* form raising the *vereinbarte Rente*. On
  *Berufsunfähigkeit* the *Beitragsverrechnung* form is so dominant that the market quotes a
  *Bruttobeitrag* and a *Zahlbeitrag* side by side; **whether the *Pflegerente* market does the
  same was not established** (gap 18), though the structural similarity is strong.
- **delib `[std]`: no *Überschussbeteiligung* in the base run.** Rationale: the delib library
  publishes **gross best-estimate-style, undiscounted** cash flows; the surplus chassis is
  demonstrated in full by `kapitallebensversicherung`; and modelling a discretionary
  *Beitragsverrechnung* on this product would require a declared-rate assumption for which this
  corpus supplies nothing at all. The product specification records the mechanic and says the model
  omits it deliberately.

### 20. Taxation

- **Premiums.** A *Pflegerente* premium is a *sonstige Vorsorgeaufwendung* under § 10 Abs. 1 Nr. 3a
  EStG, deductible only within an annual ceiling of the order of **1 900 €** (employees, pensioners)
  or **2 800 €** (self-employed) `[R23][unverified]` — a ceiling that the compulsory health and LTC
  contributions of Nr. 3 normally exhaust on their own. **In practice, for most buyers, the premium
  is not deductible at all.** The product specification must say so plainly rather than repeat the
  formal rule.
- **Benefits.** Two competing analyses, and **this file cannot settle which applies** (gap 13):
  **tax-free** under § 3 Nr. 1a EStG as a benefit from a *Pflegeversicherung* `[R23][unverified]` —
  the analysis universally applied to *Pflegetagegeld*; or **taxed at the *Ertragsanteil*** under
  § 22 EStG as a *Leibrente* `[R23][unverified]` — the analysis applied to a
  *Berufsunfähigkeitsrente*, and the one the *Pflegerente*'s life-assurance form argues for.
  The distinction is worth several percent of the product's after-tax value and **delib does not
  model taxation of the benefit**, stating the open question instead.
- ***Todesfallleistung*** from a *Pflegerente* follows the ordinary life-assurance treatment: outside
  income tax as a death benefit `[R23][unverified]`, with *Erbschaftsteuer* possible depending on the
  beneficiary designation.
- The ***Pflege-Bahr* Zulage** is a direct subsidy, not a deduction [R8], and is unavailable here.

### 21. Statistics: prevalence, incidence, duration, projection

All figures `[unverified]` and all reconstructions of the Destatis series [R18][R19] from memory,
**not** read from it. Every one carries its year.

| Measure | Value | Year | Tag |
|---|---|---|---|
| *Pflegebedürftige* in Germany | about 5.7 million | end-2023 | [R18][unverified] |
| Same, previous survey | about 5.0 million | end-2021 | [R18][unverified] |
| Share cared for at home | about 84% to 86% | 2023 | [R18][unverified] |
| Share in *vollstationäre Dauerpflege* | about 14% to 16%, roughly 0.8 million people | 2023 | [R18][unverified] |
| Projected *Pflegebedürftige* | of the order of 6.8 million | 2055 | [R19][unverified] |

**Approximate distribution across *Pflegegrade*** `[R18][unverified]`, given as shares because the
counts are less reliable than the shape: grade 1 about **9 %**; grade 2 about **44 %**; grade 3
about **27 %**; grade 4 about **14 %**; grade 5 about **6 %**. The distribution is heavily weighted
to the lower grades — which is exactly why the *Leistungsstaffel*'s middle steps drive the cost
(section 7).

**Age-specific prevalence** `[R18][unverified]`, the shape that matters more than the levels: under
1 % below 60; a few per cent in the sixties; of the order of **10 %** at 75–79; of the order of
**20 %** at 80–84; of the order of **40 %** at 85–89; and of the order of **70 %** or more at 90
and above. **Prevalence roughly doubles every five years of age above 75.** That is the curve the
whole product is built on, and it is the reason a level premium from 45 accumulates for thirty-five
years before it starts paying.

**Lifetime risk and duration** `[unverified]`: of the order of one in two women and two in five men
alive at 60 will be *pflegebedürftig* at some point; the average duration conditional on onset is
of the order of **three to five years**, longer for women; the duration in *vollstationäre* care is
shorter, of the order of **two years**, with a substantial share of residents dying within the
first year of admission. **Duration is the weakest-evidenced quantity in this file** (gap 19): it
is the direct multiplier on the liability, and no figure here is sourced.

**Why the count grows** [R19]: the baby-boom cohorts born in the late 1950s and early 1960s reach
the high-prevalence ages from the 2030s, and prevalence at a given age has not fallen enough to
offset it. The growth is qualitatively certain; its size turns on a morbidity-compression
assumption the projections vary.

### 22. Market: how much private LTC cover is actually in force

- **Private LTC top-up contracts** counted by the PKV-Verband — *Pflegetagegeld* and
  *Pflegekosten* only — number of the order of **3,5 to 4,5 million**, of which of the order of
  **0,8 to 0,9 million** are subsidised *Pflege-Bahr* `[R21][unverified]`. Against 84 million
  residents and 5,7 million *Pflegebedürftige* [R18], **private top-up cover reaches only a small
  minority of the population at risk** — the settled characterisation of the market.
- ***Pflegerentenversicherung* is not in that count**, because it is life business [R22]. **No
  sourced count of German *Pflegerente* contracts in force exists anywhere in this research**
  (gap 12). The qualitative position, `[unverified]`: it is the **smallest of the three forms by
  contract count and the largest by average premium**, it is sold overwhelmingly through advised
  channels rather than direct, and a number of *Lebensversicherer* have entered and left the segment.
- **Why penetration is low**, as reasoned market observations `[unverified]`: the risk is distant
  and easy to discount; *Hilfe zur Pflege* [R24] is a visible backstop that reduces the perceived
  downside; the *Angehörigen-Entlastungsgesetz* removed the *Elternunterhalt* motive for all but
  high earners from 2020 [R24]; the premium at the ages people actually buy is a three-figure
  monthly sum; and the products are hard to compare because the *Leistungsstaffel*, the
  *Wartezeit* and the *Karenzzeit* interact.

### 23. Typical parameter levels, and the arithmetic behind delib's `[std]` premium band

**No German *Pflegerenten* premium was established from any source** (S9, gap 3). Rather than guess a
figure and dress it as a citation, this section derives an order of magnitude from the mechanics
above and ships the result as `[std]` with the arithmetic shown, so a reader can see exactly which
assumption to change.

**Inputs**, each tagged:

| Input | Value used | Tag |
|---|---|---|
| *Vereinbarte Pflegerente* (grade 5) | 1,000.00 EUR/month | [std], from the gap arithmetic of section 4 |
| *Leistungsstaffel* | 0 / 30 / 50 / 75 / 100% | [std], section 7 |
| Lifetime probability of reaching *Pflegegrad* 2 or above | about 45% | [unverified], section 21 |
| Mean age at first insured *Pflegegrad* | about 82 | [unverified], section 21 |
| Mean duration of the insured spell | about 4 years | [unverified], section 21 |
| Grade mix over the spell, weighted by time | 40 / 30 / 20 / 10% across grades 2 / 3 / 4 / 5 | [std], section 7 |
| *Rechnungszins* | 1.00% | [R13][unverified] |
| Entry age | 45 and 55 | [std], section 18 |

**The arithmetic**, at the level of precision the inputs deserve:

1. **Time-weighted average benefit percentage** over a spell: 0.40 x 30 + 0.30 x 50 + 0.20 x 75 +
   0.10 x 100 = **52 %**, i.e. about **520 € per month** on a 1 000 € contract.
2. **Expected nominal benefit per claim**: 520 x 12 x 4 = about **25 000 €**.
3. **Expected nominal benefit per policy at issue**: 0.45 x 25 000 = about **11 200 €**, falling
   due on average around age 82.
4. **Discounted at 1 %** from 45 to 82 (37 years, factor about 0.69) that is about **7 700 €**; from
   55 (27 years, factor about 0.76) about **8 500 €** — higher at 55, because less discounting
   outweighs the smaller survival probability to 82.
5. **Premium annuity**, with survival to death and waiver in claim: of the order of **27 years'**
   worth of discounted monthly premiums from 45 and **19 years'** worth from 55 `[std]`.
6. **Net level premium**: 7 700 / (27 x 12) = about **24 €/month at 45**; 8 500 / (19 x 12) = about
   **37 €/month at 55**.
7. **Gross-up.** A tariff uses **prudent** incidence and durations (§ 138 VAG [R12]), carries
   acquisition and administration costs (section 16), funds the waiver, and holds a margin for the
   DAV 2008 P basis risk of section 17. A gross-to-net ratio between **2 and 3** is the reasonable
   band for a biometric product of this basis-risk profile `[std]`.

**Result — delib's `[std]` premium band**, for 1 000 € *vereinbarte Rente*, 0/30/50/75/100 grid,
lifelong level monthly premium, waiver in claim, no death benefit, no dynamics:

| Entry age | `[std]` band, monthly | Tag |
|---|---|---|
| 45 | about 50.00 to 100.00 EUR | [std], from the arithmetic above |
| 55 | about 80.00 to 160.00 EUR | [std], from the arithmetic above |

**How to read this band.** It is not a market observation and must never be cited as one. It says
that a model premium falling well outside it indicates an error in the bases, and that one inside
it is not thereby validated. The technical notes print the model's own equivalence premium beside
the band and say which end it lands at and why. **Gap 3 stands** until a real *Tarifblatt* or
portal quotation replaces it.

**Other typical parameter levels** `[unverified]` throughout: *vereinbarte Rente* as sold, **1 000 €
to 1 500 €** per month; entry ages permitted **18 to 65**, occasionally to 70; purchase cluster
**45 to 60**; *Beitragsdynamik* **3 % to 5 %**; *Leistungsdynamik* **1 % to 3 %**.

---

## Observed variation across insurers

**No carrier's *Pflegerenten* document was located, so there is no carrier-attributed variation
table in this file** (gap 14). Naming carriers against parameter values that no source supplied
would be exactly the fabrication house rule 3 forbids, and it is not done here. What can be given
instead is the **parameter range the German market is understood to write**, with its tag and an
explicit statement of who, if anyone, is attributed:

| Parameter | Range | Attribution | Tag |
|---|---|---|---|
| *Leistungsstaffel*, grade 1 | 0% to 10% | none established | [unverified] |
| *Leistungsstaffel*, grade 2 | 10% to 30% | none established; 20% is the *Pflege-Bahr* statutory step | [unverified], [R8] for the 20% |
| *Leistungsstaffel*, grade 3 | 30% to 50% | none established; 30% statutory in *Pflege-Bahr* | [unverified], [R8] |
| *Leistungsstaffel*, grade 4 | 60% to 75% | none established; 40% statutory in *Pflege-Bahr* | [unverified], [R8] |
| *Leistungsstaffel*, grade 5 | 100% | universal | [unverified] |
| *Wartezeit*, underwritten | 0 to 3 years | none established | [unverified] |
| *Karenzzeit* | 0, 3 or 6 months | none established | [unverified] |
| Entry age | 18 to 65, some to 70 | none established | [unverified] |
| *Beitragsdynamik* | 3% to 5% p.a. | none established | [unverified] |
| *Leistungsdynamik* in payment | 1% to 3% p.a. | none established | [unverified] |
| *Todesfallleistung* | none / *Beitragsrückgewähr* / fixed sum / *Deckungskapital* | none established | [unverified] |
| *Stornoabzug* | 0% to about 5% of *Deckungskapital* | none established | [unverified] |

**Carriers that write German LTC top-up business.** The delib brief names twenty-six German
carriers. **This file establishes nothing about any of them** — not one wording, rate card,
product name or parameter — and therefore names none of them against any figure. The one
structural statement it can make without a source, because it follows from section 5, is that
***Pflegetagegeld* is written by the *Krankenversicherer* in that list and *Pflegerente* by the
*Lebensversicherer***; which undertakings currently offer a *Pflegerente* was not established
(gap 14).

**Representative design the research supports.** A single-life, individual, underwritten
*Pflegerentenversicherung* on a **monthly** grid; benefit trigger the statutory *Pflegegrad* of
§§ 14, 15 SGB XI [R2]; a *Leistungsstaffel* of **0 / 30 / 50 / 75 / 100 %** of a *vereinbarte
Pflegerente* of **1 000 € per month** `[std]`; **no *Wartezeit* and no *Karenzzeit*** in the base
run `[std]`; **full *Beitragsbefreiung*** from the first month any annuity is payable `[std]`; a
**level lifelong monthly *Beitrag*** struck by equivalence, guaranteed against re-rating [R11]; a
prospective ***Deckungskapital*** *gezillmert* to the **25 ‰** ceiling `[R13][unverified]` and
priced at the **1,00 %** *Höchstrechnungszins* `[R13][unverified]`; a **multi-state benefit engine**
over {aktiv, PG1..PG5, tot} with **state-dependent mortality** and explicit **deterioration and
*Herabstufung*** transitions, on a `[std]` proxy shaped on DAV 2008 P and anchored to the worked
example [R15]; **no *Todesfallleistung*, no *Dynamik*, no *Überschussbeteiligung* and no *Stornoabzug*
in the base run**, each exposed as a switchable option `[std]`; and a ***Rückkaufswert*** equal to
the floored prospective reserve, with the open § 169 VVG scope question stated rather than assumed
away [R11].

Each `[std]` choice is argued where it is made, and the ones this corpus cannot source — the
*Leistungsstaffel* levels, the *Karenzzeit*, every charge, the *Stornoabzug*, the lapse rates, the
premium level and every transition rate — carry the observed or argued range beside them.

---

## Gaps and caveats

1. **No *Produktinformationsblatt*, IPID or *Basisinformationsblatt* for any German
   *Pflegerentenversicherung* was located.** This is the single most valuable missing document class:
   one such document would have supplied the entry-age band, the *vereinbarte Rente* band, the
   *Leistungsstaffel*, the *Wartezeit*, the *Karenzzeit*, a specimen premium and the charges, on two
   pages. Everything sections 7, 9, 13, 16 and 23 standardise would have been sourced instead of
   `[std]`.

2. **No charge level of any kind was established.** Not one *Abschlusskostensatz*, not one
   administration-cost rate, not one *Ratenzahlungszuschlag* and not one *Effektivkosten* value for
   any *Pflegerenten* tariff. Only the statutory **ceiling** (25 ‰ of *Beitragssumme*) is known, and
   only `[unverified]`. **Every charge in delib is `[std]`.**

3. **No premium was established, and no rate card exists in this corpus.** frlib's `temporaire_deces`
   had a complete published attained-age grid to reproduce; delib's `pflegerentenversicherung` has
   nothing. Section 23's band is derived arithmetic tagged `[std]`, not an observation, and it must
   never be cited as a market figure. A single portal quotation or *Tarifblatt* would close this gap.

4. **No Stiftung Warentest / *Finanztest* result was retrieved.** The characterisations at S10 are
   recalled market knowledge, `[unverified]`, with no score, price or test date behind them.

5. **No comparison-portal quotation was obtained**, and it was not even established whether Verivox
   or Check24 quote *Pflegerente* at all as opposed to *Pflegetagegeld* only [S13].

6. **No rating-agency wording analysis was retrieved** [S14]. Franke und Bornberg and Morgen & Morgen
   publish exactly the clause-by-clause comparisons that would have turned the `[unverified]` ranges
   of the variation table into sourced ranges. Every range in that table is a reconstruction.

7. **Market counts are unsourced and structurally incomplete.** The PKV-Verband count [S16][R21]
   excludes *Pflegerentenversicherung* by construction, because that product is life business; and no
   figure from it was retrieved in any case.

8. **The statutory benefit amounts are 2025 values and the 2026 position was not established.** Every
   figure in section 3 is stamped 2025 and tagged `[unverified]`. Whether the PUEG's *Dynamisierung*
   [R10], or any later act, changed the amounts, the *Beitragssatz* or the *Leistungszuschläge* with
   effect from 1 January 2026 is unknown. **Any downstream document must re-check the year.**

9. **The § 169 VVG scope question is open.** Whether a **pure-risk** *Pflegerente* — no death
   benefit, no survival benefit — falls inside the statutory exception that denies a
   *Risikolebensversicherung* its surrender value was not established. delib models a
   *Rückkaufswert* and states the question; a carrier's own wording settles it for that carrier.

10. **DAV 2008 P is cited and not read, and it was built on the superseded *Pflegestufen*.** No value
    from the table appears anywhere in this library, and none may. Two distinct problems compound:
    the table's contents are unavailable, and the trigger it is applied to was redefined in 2017 [R9]
    in a way that widened the insured population. **This is the largest basis risk in the product**
    and every delib transition rate is a `[std]` proxy with a stated shape rather than a calibration.

11. **No BaFin material specific to LTC was located** [R17]. There is therefore no supervisory
    statement in this file about *Pflegetafel* prudence, about the *Nachprüfung*, or about product
    value for this class.

12. **There is no count of German *Pflegerente* contracts in force.** The GDV life series does not
    carve the product out as a reported family on the evidence available [R22], and the PKV series
    excludes it [R21]. The market-size statements in section 22 are qualitative.

13. **The taxation of the benefit is unresolved.** Section 20 sets out two competing analyses —
    exemption under § 3 Nr. 1a EStG and *Ertragsanteil* taxation under § 22 EStG — and this file
    cannot say which governs a *Pflegerente* paid by a *Lebensversicherer*. delib does not model
    benefit taxation and says so.

14. **Not one carrier document, product name or parameter was established for any of the
    twenty-six insurers the brief named.** No wording, no *Tarifblatt*, no product page. The
    variation table above is therefore a market-range table with no attribution. This is the
    largest single difference between
    this file and its frlib counterpart, where eight carriers' contracts were read in full.

15. **The *Eigenanteil* figures are the least reliable numbers in the file.** Section 4's
    2 900–3 200 € range, its component split and its regional dispersion are recalled from the vdek
    series [R20] and confirmed by nothing. They are used only to argue an order of magnitude for the
    `[std]` *vereinbarte Rente* and must not be quoted as data.

16. **Whether a *Pflegerentenversicherung* is a PRIIP was not established** [S6][R25]. The reasoning
    in S6 — that a pure-risk form is excluded and a *Beitragsrückgewähr* form probably is not — is
    the author's reading of the Regulation's exclusions, not a retrieved text, and the article
    numbering is `[unverified]`.

17. **Whether a *Herabstufung* guarantee ("the annuity once granted will not be reduced") is common
    was not established.** It changes the paying state's exit structure materially: with such a
    guarantee the paying state is exited only by death, and the model of section 17 simplifies. delib
    models the ungaranteed form, which is the more general one.

18. **The *Überschussbeteiligung* application form is not established for this product.** Whether the
    *Pflegerente* market quotes a *Bruttobeitrag* and a *Zahlbeitrag* as the *Berufsunfähigkeit*
    market does, and at what discount, is unknown. delib's base run omits surplus entirely.

19. **Every duration and incidence figure in section 21 is unsourced**, and duration is the direct
    multiplier on the liability. The three-to-five-year spell, the roughly two-year residential stay
    and the high first-year mortality are recalled orders of magnitude. **A change from four years
    to five in the mean spell changes the premium by about a quarter**, so this gap is quantitatively
    the most expensive one in the file after gap 10.

20. **No lapse rate for this product, at any duration, was established.** A *Pflegerente*'s lapse
    profile should be strongly duration-dependent — *Zillmerung* makes early lapse costly to the
    policyholder, and a lapse after 60 forfeits the whole accumulated position — but nothing in this
    corpus describes the shape. Every lapse assumption in delib is `[std]`.

21. **Overtaken by the provenance pass, and left standing as the record of the drafting.** No search
    corroboration existed for anything in this file when it was written: the other two delib
    research files, written before the budget ran out, record per fact what a search summary
    established, and this one could not. Everything above rested on the authoring model's knowledge
    of German insurance law and practice under the discipline of house rule 3, and the
    `[unverified]` tags are the honest record of that. **The checklist this item asked a reader to
    work through has since been worked through**: thirty of the forty entries were opened on
    2026-08-30, eight statements above are contradicted by what was read, and the results are in
    *Provenance pass of 2026-08-30* below and in `products/pflegerentenversicherung/sources.md`.
    Where an entry was not opened, this item still governs it.

---

## Provenance pass of 2026-08-30 — what was retrieved, and what it contradicts

The network policy that produced the retrieval conditions above was lifted, and every source in this
file was tried again on **2026-08-30**. **The entries and their numbering are frozen and are left as
written**; this section records, per entry, what was opened and what the opened document says. Where
a document contradicts a fact stated above, the correction is carried into
`products/pflegerentenversicherung/sources.md`, which is the operative record for the product
documents. Nothing in the model was changed.

**Retrieved and read** (statutes as canonical XML with the law's `Stand`; documents as PDF or HTML):

| Entry | Document | Note |
|---|---|---|
| S1 | *AVB/PPV* with MB/PPV 2026, 56 pp., pkv.de | § 1 Abs. 2 and Abs. 6 **copy** §§ 14, 15 SGB XI into the conditions |
| S2 | *MB/EPV 2017*, Stand Nov. 2022, 15 pp., pkv.de | § 1a writes its own trigger; § 8b is the annual *Beitragsanpassung* comparison |
| S4 | IDEAL *PflegeRente Exklusiv*, conditions **AB-IPR-2022A** + 4 *EB*, 67 pp., ideal-versicherung.de | the first carrier wording read for this product |
| S5 | IDEAL *Produktbeschreibung* `pb_ipr_1124`, 4 pp. | the *Informationsblatt* itself is quotation-specific and stays unretrieved |
| S7 | *Versicherer- und Verbraucherinformationen* inside the S4 pack; VVG-InfoV § 2 as XML | § 2 Abs. 1 Nr. 9 confines *Effektivkosten* to covers where the obligation is certain |
| S10 | test.de landing page for the *Pflegetagegeld* comparison | 70 tariffs, 24 health insurers, Stand Mai 2023; **scores paywalled** |
| S11 | verbraucherzentrale.de, *Ist eine Pflegezusatzversicherung sinnvoll?* | *"etwa zwei- bis dreimal so hoch"* for the annuity form |
| S12 | finanztip.de, *Pflegezusatzversicherung* | level premium against re-ratable premium, in consumer terms |
| S14 | Assekurata, *Wege zur Pflegevollversicherung*, 45 pp., April 2026, via pkv.de | market counts, durations, *Pflegetagegeld* premiums |
| S16 | PKV *Zahlenbericht 2024*; the association's *Pflegezusatzversicherung* page | taxonomy has no annuity line |
| R1–R8 | SGB XI, canonical XML, Stand 24.7.2026 | §§ 14, 15, 17, 18, 23, 30, 36, 37, 39, 42a, 43, 43c, 45b, 126–130, 140 |
| R9 | not opened as an act; its citation and effect recited by the BGH and by the DAV | *vom 21.12.2015, BGBl. I S. 2424* |
| R11 | VVG and VVG-InfoV, canonical XML, Stand 26.5.2026 | §§ 7, 19, 21, 152, 153, 155, 163, 165, 169, 176 |
| R12 | VAG (Stand 25.3.2026) and HGB, canonical XML | §§ 138, 139, 146 VAG; § 341f HGB |
| R13 | DeckRV, canonical XML, Stand 19.7.2024 | § 2 Abs. 1 and Abs. 2; § 4 Abs. 1 |
| R14 | KVAV, canonical XML, 32 sections | |
| R15 | DAV *Ergebnisberichte* of 15 Jan. 2025, 122 pp. and 75 pp., aktuar.de | derivation **and** the *Pflegegrad* re-derivation, both free |
| R18 | Destatis press release PD24_478_224 and the *Pflegegrade* table (Stand 18.12.2024); *Pflegequoten* by age via GENESIS | |
| R19 | Destatis press release PD23_124_12, *Pflegevorausberechnung 2023* | |
| R20 | vdek press release of 22 Jan. 2026, 4 pp. | *Eigenanteil* as at 1.1.2026 |
| R21 | via S14, cited there to the PKV-Verband | |
| R22 | GDV, *Die deutsche Lebensversicherung in Zahlen 2024* | |
| R23 | EStG, canonical XML | § 3 Nr. 1a; § 10 Abs. 1 Nr. 3a and Abs. 4 |
| R24 | SGB XII, canonical XML, Stand 24.7.2026, 197 sections | §§ 61, 61a, 64, 66 |
| REG-R36 | BGH, *Urteil vom 30. April 2025 — IV ZR 126/23*, 19 pp. | on the *Pflegestufen*/*Pflegegrade* break in a *Pflegerenten* promise |

**Not retrieved, with the reason** — S3, S6, S9, S13, S15, R16, R17, and the *Informationsblatt* half
of S5, the *Standmitteilung* specimen at S8 and the scored half of S10. Two of those reasons changed:
**S9** is now known to be unretrievable because no German insurer publishes a *Pflegerenten* rate
card, not because the network refused; **S13** was deliberately not queried, a portal quotation being
generated per enquiry rather than published.

**Eight statements in this file are contradicted by a document retrieved on 2026-08-30.** Each is
corrected in `products/pflegerentenversicherung/sources.md` at the entry named.

1. **§ 127 SGB XI fixes no 10 / 20 / 30 / 40 / 100 % *Pflege-Bahr* grid** (section 6, R8, S15, gap
   register). Abs. 2 Nr. 4 requires a *Geldleistung* at every *Pflegegrad*, at least 600 € at grade 5,
   capped at the SGB XI benefit level; the percentage schedule belongs to the PKV-Verband's
   *brancheneinheitliche Vertragsmuster* under Abs. 2 Satz 2. Nor does § 127 say *Pflegetagegeld*:
   the eligibility test is § 146 Abs. 1 Nrn. 1 and 2 VAG, i.e. health business with an
   *Alterungsrückstellung*. The conclusion that a *Pflegerente* cannot be a *geförderter Tarif*
   survives on that ground.
2. **The GDV reports *Pflegerentenversicherungen* as its own product family** (R22, gap 12):
   242 000 stand-alone contracts in force at 31.12.2023 with 177 Mio. € of annual premium, plus
   762 400 written as riders, and 5 499 new policies in 2023.
3. **DAV 2008 P is published, and has been re-derived for the *Pflegegrade*** (R15, gap 10). The
   derivation carries the bases in Anhänge 1 to 3; a companion *Ergebnisbericht* adjusts the
   *Ausscheidewahrscheinlichkeiten* to the new *Pflegebedürftigkeitsbegriff*, on a *Stufenmodell*
   structure, and publishes prudence loadings for the risk (gap: "no *Sicherheitszuschlag* level was
   established" is withdrawn).
4. **§ 43 Abs. 3 SGB XI sets the grade-1 residential *Zuschuss* at 131 €, not 125 €** (section 3).
5. **The *Pflegegrad* stock distribution is 13,8 / 40,4 / 29,6 / 11,8 / 4,3 %**, not 9 / 44 / 27 /
   14 / 6 %, and the age-specific *Pflegequoten* are materially higher than section 21 records —
   16,4 % at 75–80, 30,8 % at 80–85, 53,7 % at 85–90, 80,2 % at 90–95 (R18).
6. **§ 169 Abs. 1 VVG is a positive scope test, not an exception for death-only covers** (R11,
   gap 9): the value is owed where *"der Eintritt der Verpflichtung des Versicherers gewiss ist"*.
   The same test governs the *Effektivkosten* duty of § 2 Abs. 1 Nr. 9 VVG-InfoV.
7. **The market *Stornoabzug* is not "nil to about 5 %"** (section 15): the one *Pflegerenten*
   wording read agrees **25 %**, rising to 50 % after a partial withdrawal.
8. **Definition risk is hedgeable and is hedged** (section 2, section 8): MB/PPV and MB/EPV copy the
   statutory test into the conditions, and AB-IPR-2022A pins it to *"den Stand vom 28.03.2021"*.
   What is unhedged is drift in assessment practice under a fixed text.

**Four gaps are closed and two are narrowed.** Closed: gap 8 (the 2026 position — § 30 SGB XI
uprated on 1.1.2025 and next uprates on 1.1.2028, so the 2025 amounts stood through 2026); gap 12
(the *Pflegerente* count); gap 15 (the *Eigenanteil*, now read from the vdek evaluation as at
1.1.2026 — 3 245 € in the first year of a stay, of which EEE 1 685 €, *Unterkunft und Verpflegung*
1 046 € and *Investitionskosten* 514 €); and the *Sicherheitszuschlag* limb of gap 10. Narrowed:
gap 19, the overall spell now sourced at about five years for onset after 60 — 4,0 for men and 5,7
for women — while the **per-grade** sojourn times remain unavailable, Assekurata saying in terms that
no such information exists; and gap 14, one carrier's wording read where none had been. Gaps 1 to 7,
11, 13, 16 to 18, 20 and 21 stand, and gap 3 (no premium) is now known to reflect market practice
rather than a retrieval failure.
