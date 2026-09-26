# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/risikolebensversicherung.md` (the
citation ground truth for this product) and are **frozen — never renumber**. **No id is absent
from this file and the numbering has no gaps**: all seventeen primary sources **S1–S17** and all
twenty-three product-level references **R1–R23** are cited by `product-spec.md`, eighteen of the
R-entries again by `technical-notes.md`, and sixteen again by `model.md`. When these entries were
first written that completeness was not evidential strength but its opposite: **no document among
them had been opened**, so nothing could be dropped for saying too little, and every entry was
cited for what it *would* settle and for the fact that it did not. Twenty-two of the forty now
settle it. Where a sibling library's `sources.md` records omitted ids — frlib drops three for
returning nothing citable — this one records absences of a different kind, in each entry's
`Retrieved` line and in the closing register. Access dates: **2026-08-29** at drafting, when this
list was assembled without opening a document, and **2026-08-30** for the re-verification pass
each entry below records. No sources were newly added at drafting. Cross-product [REG-R#] tags are
listed in their own section at the end.

**Retrieval conditions — read before any entry below.** This file was drafted under one set of
conditions and re-verified under another. Both belong in the record, and this product sat at the
worse end of the first.

1. **How it was drafted.** Two independent limits applied. **Direct HTTP egress was blocked** by an
   organisation network policy: `WebFetch` and `curl` were refused with HTTP 403 at the egress
   gateway for every host outside a short package-registry allowlist, and `gesetze-im-internet.de`,
   `bafin.de`, `gdv.de`, `aktuar.de`, `bundesfinanzministerium.de`, `dejure.org`, `buzer.de`,
   `destatis.de` and `de.wikipedia.org` were all tried and all refused. And **the session's
   `WebSearch` budget — 200 calls, shared across the library — was exhausted *before* this
   product's research began**, during the regulatory and contract-law work and during delib
   products 1 and 2, so every search attempted for this product returned the budget-exhausted
   message and it had **no research channel at all**. **Not one document listed here had been
   opened when these entries were first written** — no AVB, no *Produktinformationsblatt*, no
   *Verbraucherinformation*, no statutory text, no rate card, no comparison-portal result. The
   draft rested instead on the authoring model's own knowledge of German insurance law and
   practice, disciplined by **[std]** on every level it standardized and `[unverified]` on every
   specific it could not confirm. Nothing was invented under that regime: no edition, tariff code,
   document number, page count or publication date was guessed, and an entry read
   `URL: not established` wherever the canonical form was not one this author was confident of.

2. **How it stands now.** That policy has been lifted and the citations were re-verified against
   the primary documents on 2026-08-30. **Twenty-two of the forty entries below read
   `Retrieved: yes` and eighteen read `no` — 55 %**, against 501 of delib's 805 source entries
   (62 %) library-wide, where all fifteen German instruments the library cites were read as
   canonical XML with each law's amendment status (`Stand`) recorded and, of 950 statutory section
   references checked, 950 were correct. `Retrieved: yes` means one thing exactly: **the document
   was opened and the passage the entry rests on was read.** Here that is ten instruments — the
   VVG, the MindZV, the DeckRV, the VAG, the AGG, the EStG, the ErbStG, the VVG-InfoV and the HGB
   as canonical XML from `gesetze-im-internet.de`, each entry carrying the `Stand` it was read at,
   and the VersStG 2021 from one of the few per-section pages that serves text rather than a
   frameset — together with three wordings and two premium specimens as PDFs: the GDV
   *Musterbedingungen*, Stand 21.07.2025; CosmosDirekt **LA 803 A (04.26)** with its *Besondere
   Bedingungen*; Hannoversche **T25**, Stand 09/2025, in a 32-page pack; the two Cosmos
   *Informationsblatt* specimens; and one carrier surplus guide in HTML.

3. **What the eighteen `no` entries are.** They are the carrier sweep and the secondary
   literature, and most name their own failure on their own line. **HTTP 404 at the cited URL** and a
   **JavaScript wall** behind it: [S6], where the Debeka path this library carried is gone and the
   replacement *Vertragsgrundlagen* library injects its document links client-side, so no PDF
   address is in the served HTML — the same wall that leaves [S8] and [S11] with a product page
   and no conditions file, the wording being reached through a quote flow. **A distribution-channel
   wall**: [S7], whose wordings sit behind the broker channel, which is itself the fact that entry
   records. **Not searched for in this pass**: [S9], [S10], [S12] and [S13], once [S1], [S3] and
   [S4] had settled the clause questions they would have been read for; [S13] is cited for nothing
   beyond the existence of the carriers it names. **Paywall and subscription**: [S16], *Finanztest*,
   published with a free summary and the test itself paid; [S17] and [R20], the rating houses'
   *Bedingungsanalysen*. **Nothing published to retrieve**: [S14], where a comparison result is
   generated per query and is not a document at all. **Located but not read**: [R12], whose four
   DAV addresses were opened on 2026-08-30 and confirmed live, public and of the size and kind the
   entry describes, but whose text was not read, so its substantive claims stay inherited. **Nothing
   product-specific found**: [R18] and [R19], no GDV term-segment series and no BaFin item reaching
   a pure protection contract; [R22]; and [R23], where **no decision is cited by date or file
   number anywhere in this product's documents**. The four secondary entries [S14] to [S17] still
   carry the drafting-time reason on their `Retrieved` lines, and none of them was given a URL.

What follows from that, stated plainly, and it now cuts two ways. Where an entry says
`Retrieved: yes`, the § numbers, editions, page counts and quoted German sentences below were
transcribed from the document itself, and the claim the entry carries can be treated as sound.
Where it says `no`, **a delib citation is still a pointer, not a certificate**: it names the
instrument a claim should be checked against and does not assert that anyone checked it, the entry
is a **known reference** — a document that exists and is the right kind of document for the claim
beside it — and it says so. **Re-verification was not a formality.** It overturned this product's
flat denial of any *Rückkaufswert*, corrected the claim that German term-life charge levels are
structurally undisclosed, replaced a guessed *Nachversicherung* event list with a carrier's own and
re-titled § 163 VVG; the closing register records each correction and which document forced it.

One thing here was evidence before any document was opened, and it is second-hand. Several
instruments this product turns on were **search-corroborated for the two sibling products while
budget remained**, and their findings are recorded in `_research/kapitallebensversicherung.md` and
`_research/klassische_rentenversicherung.md`. Where an entry below says **"inherited
corroboration"**, someone checked something — for the sibling's purpose, not for this one. That
chain covers §§ 161, 169, 165, 19 and 153 VVG, the MindZV percentages, the DeckRV rate history and
the DAV 2008 T *Richtlinie*, and at drafting it was the strongest thing in this file. It now sits
**behind** the instruments themselves everywhere the XML settled the point, and it remains the only
support the file has for [R12], which was located but not read. **Levels, though, are still not
observed.** Uncertain numbers became **[std]** parameters rather than citations: apart from one
direct writer's published model case [S2], not one *Bruttobeitrag*, *Zahlbeitrag*, spread ratio,
smoker ratio, charge, commission scale or lapse rate in this product's documents is an observation,
and `model.md`'s standardization table lists every one.

---

## Primary product sources

(delib-risikolebensversicherung-s1)=

### S1 — GDV, "Allgemeine Bedingungen für die Risikolebensversicherung" (*Musterbedingungen*)
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V.; *Musterbedingungen* — model AVB published by the industry association for members to adopt, adapt or ignore. Expressly *unverbindlich* and optional, which is a competition-law disclaimer and is load-bearing for citation weight
- URL: `https://www.gdv.de/resource/blob/6324/13d86b44ff6f4d6800e9ddeb7bc17476/allgemeine-bedingungen-fur-die-risikolebensversicherung-data.pdf`, reached from the *Musterbedingungen* index at `https://www.gdv.de/gdv/service/musterbedingungen`. The document's own title is ***Allgemeine Bedingungen für die Risikolebensversicherung*** — not "für die Risikoversicherung", which is the carriers' usual heading
- Retrieved: **yes** (PDF, 18 pp., Stand: 21.07.2025, read 2026-08-30; the index page also retrieved, OK). The *unverbindlich* disclaimer is on its face: "Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ. Abweichende Bedingungen können vereinbart werden."
- Used for: **the industry model wording, now read.** The question-headed second-person drafting style is confirmed on every section heading ("Wie erfolgt die Überschussbeteiligung?", "Wann können Sie Ihren Vertrag beitragsfrei stellen oder kündigen?"), which `product-spec.md`'s overview describes. Four substantive things now come from S1 rather than from inference: the *Selbsttötung* three-year clock **restarts for the increased or reinstated part** on a contract change (§ 5 Abs. 3 — gap 9, closed); *Kündigung* **converts the contract into a *beitragsfreie Versicherung*** and pays a *Rückkaufswert* under § 169 VVG only where the paid-up sum fails a carrier-set minimum (§ 13 Abs. 8 — which **contradicts** the "nothing is paid, ever" reading this product was built on, see [R2]); the § 4 DeckRV *Verrechnungsverfahren* is applied with the **2,5 %** ceiling and the **remainder of the acquisition cost spread over the whole premium-paying period** (§ 14 Abs. 2–3); and surplus is allocated per ***Bestandsgruppe*** and ***Gewinnverband*** by a *verursachungsorientiertes Verfahren* (§ 2 Abs. 2–3). Footnote 28 records that the Zillmer clause "ist nur bei der Verwendung des Zillmerverfahrens aufzunehmen" — **Zillmerung is optional on this line**, which bears directly on `model.md`'s [std] α (gap 8). An `[S1]` tag now means "the industry model wording says this", and where a carrier wording is cited beside it the two are compared

(delib-risikolebensversicherung-s2)=

### S2 — GDV, *Produktinformationsblatt* pattern for the *Risikoversicherung*
- Publisher / doc type: GDV; model *Produktinformationsblatt* (PIB) — the short pre-contractual product summary. **The name has moved on**: since the IDD implementation the document § 4 VVG-InfoV requires is the ***Informationsblatt zu Versicherungsprodukten*** (IPID, Durchführungsverordnung (EU) 2017/1469), and carriers now issue that; "PIB" survives as the market's older name and as some carriers' file naming [R17]
- URL: no GDV model PIB for this line is published on the *Musterbedingungen* index. **A carrier specimen was retrieved instead** and is cited in its place: Cosmos Lebensversicherungs-AG, *Muster-Informationsblatt zu Versicherungsprodukten*, `https://www.cosmosdirekt.de/resource/blob/15750/ce3439de3bbf09d3d5fee7889a3cd235/vib-crc-risikolebensversicherung-data.pdf`, and the older *Produktinformationsblatt* pattern `https://www.cosmosdirekt.de/resource/blob/89394/91ebf9428a54446bc0e61e17723c3332/pib-risiko-lebensversicherung-data.pdf`
- Retrieved: **yes** for the carrier specimens (PDF, 2 pp., edition Muster-VIB CR_CRC (12.20); PDF, 5 pp., edition PIB_CRB/CRCB_Berechnung (01.2018); both read 2026-08-30). **No GDV model PIB exists to retrieve** — the association publishes model *Bedingungen* and *Standmitteilungen* for life, not a model PIB
- Used for: **the single largest change this pass makes.** The inference that a carrier states the *Bruttobeitrag* and the *Zahlbeitrag* side by side in this document was right, and the specimen states them: for a model case of **Eintrittsalter 41, Vertragsdauer 19 Jahre, Bankkaufmann, Versicherungssumme 100 000 €**, tariff CRB2, a monthly ***Tarifbeitrag* of 18,21 EUR** against a first-year ***Zahlbeitrag* of 8,20 EUR** — and it goes further than expected, giving the acquisition cost in euro and as a percentage of the *Tarifbeitragssumme*. That closes gap 1 and gap 8 for one carrier, and the figures and what follows from them are set out in `product-spec.md`'s premium section and `model.md`'s two-premium section. **The figures are observations of one direct writer's model case and are not generalised**: no [S2] figure is used as a model parameter, and the [std] scale is unchanged

(delib-risikolebensversicherung-s3)=

### S3 — CosmosDirekt (Cosmos Lebensversicherungs-AG), *Risikolebensversicherung*
- Publisher / doc type: Cosmos Lebensversicherungs-AG; *Allgemeine Bedingungen für die Risiko-Lebensversicherung*, *Besondere Bedingungen*, *Informationsblatt zu Versicherungsprodukten*, *Produktinformationsblatt*, product page
- URL: AVB `https://www.cosmosdirekt.de/resource/blob/7944/7b400325610aa816ee0ed2e1deda323d/allgemeine-bedingungen-risikoversicherung-la-803-a--data.pdf` · *Besondere Bedingungen* `https://www.cosmosdirekt.de/resource/blob/611396/6d70b9698c9fc73321e55cb81a98c9e1/besondere-bedingungen-fuer-die-risiko-lebensversicherung-la-804-a--data.pdf` · the carrier's whole *Versicherungsbedingungen* library at `https://www.cosmosdirekt.de/services/vertragsservice/vertragsservice-versicherungsbedingungen/`. The `LA <number> <letter>` convention was right: the term-assurance codes are **LA 803 A** and **LA 804 A**
- Retrieved: **yes** (AVB: PDF, 11 pp., edition **LA 803 A (04.26)**; *Besondere Bedingungen*: PDF, 6 pp., edition **LA 804 A (04.26)**; both read 2026-08-30). The two *Informationsblatt*/PIB specimens are at [S2]
- Used for: **the primary carrier wording of this product**, and the entry that changed most. It establishes: the *Beitragsverrechnung* mechanic in the carrier's own words — "Die Überschussanteile (Sofortrabatt) werden **in Prozent des Bruttobeitrags** festgesetzt und mit den laufenden Beiträgen verrechnet" (§ 3 Abs. 2 b) — which is the exact shape `technical-notes.md` derives `v_d` in; that on a constant sum insured "bleibt Ihre Absicherung sowie der vereinbarte **Bruttobeitrag** über die gesamte Versicherungsdauer unverändert"; the *Selbsttötung* three-year clock and its **restart for the changed or reinstated part** (§ 2 Abs. 4 — gap 9, closed); the *Nachversicherungsgarantie* event list, the twelve-month window, the **20 % / 50 000 € per-event cap**, the **five-occasion cumulative cap** and the **age-50 limit** (§ 13 — gap 7, closed); the twelve-month smoker qualifying period and the fact that a switch to smoking is a *Gefahrerhöhung* (§ 18 — gap 22, partly closed); and the § 4 DeckRV *Verrechnungsverfahren* with its **2,5 %** ceiling (§ 16 Abs. 2). Two things it establishes **against** the library: on this carrier full *Kündigung* really does pay nothing — "Bei einer vollständig gekündigten Versicherung fällt kein Rückkaufswert an und Ihre Versicherung erlischt" (§ 15 Abs. 10) — but *Beitragsfreistellung* on a constant sum insured is a live right that produces a real paid-up sum, and only the **falling**-sum variant has no *Deckungskapital* at all (§ 15 Abs. 1–4); and the tariff runs at a ***Rechnungszins* of 0,25 Prozent**, not at the DeckRV maximum the model assumes [R10]. The direct-channel spread argument is still structural, not sourced — but the [S2] figures now measure it for this carrier

(delib-risikolebensversicherung-s4)=

### S4 — Hannoversche Lebensversicherung AG (VHV group), *Risikolebensversicherung*
- Publisher / doc type: Hannoversche Lebensversicherung AG; *Bedingungen und Informationen — Risikoversicherung*, a single pack containing the *Allgemeine Bedingungen für die Risikoversicherung / T25*, the BUZ and UZ riders, the *Steuer-Informationen*, a *Lexikon* and the *Merkblatt zur Anzeigepflichtverletzung*
- URL: `https://www.hannoversche.de/dam/risiko/bedingungen/bedingungen-risikolebensversicherung-aktuell.pdf`
- Retrieved: **yes** (PDF, 32 pp., document 700.0005.35, **Stand 09/2025**, AVB **T25**, read 2026-08-30)
- Used for: **the second carrier wording, and the one that disproves the library's strongest claim.** It corroborates [S3] independently on the two mechanics that matter: the declared surplus is fixed "in Prozent des **Tarifbeitrags**" and credited as a *Sofortgutschrift* against each instalment (§ 20 Abs. 3 b aa–bb), and it "kann auch **Null Euro** betragen" — which is the asymmetry `product-spec.md` describes, stated by the carrier. The *Selbsttötung* clock and its restart on an increase are word-for-word the [S1] model wording (§ 19). But its § 13 says that *Kündigung* **converts the contract into a *beitragsfreie Versicherung*** (minimum sum 2 500 €), and where that minimum is not reached "wird das Deckungskapital abzüglich des oben beschriebenen Abzugs ausgezahlt und der Vertrag erlischt", the *Abzug* being **60 % des Deckungskapitals** — with a *Rückkaufswerte* table annexed to the *Versicherungsschein* for every tariff **except T3 and T4**, the falling-sum tariffs that build no *Deckungskapital*. So a German term assurance **can** carry a surrender value; see [R2] and the register below. It also cites § 88 VAG and §§ 341e, 341f HGB as the *Deckungsrückstellung* basis, which is [R21]'s pointer confirmed from the contract side

(delib-risikolebensversicherung-s5)=

### S5 — HUK-COBURG / HUK24, *Risikolebensversicherung* and the *Überschussbeteiligung* guide
- Publisher / doc type: HUK-COBURG / HUK24; insurer guide page **about term assurance specifically**, plus the product pages
- URL: `https://www.huk24.de/risikolebensversicherung/ratgeber-lebensversicherung/ueberschussbeteiligung`
- Retrieved: **yes** (HTML, ~66 kB, page titled *Überschussbeteiligung der Risikolebensversicherung*, read 2026-08-30)
- Used for: the characterisation the entry was cited for, now read rather than inferred — a carrier's own page devoted to surplus participation **on term assurance**, so the carrier does treat it as central. Two things it gives that the library did not have. **The two surplus forms**: "In der Praxis bieten Versicherer bei Risikolebensversicherungen für die Überschussbeteiligung wiederum meist eines von zwei Modellen an: den **Todesfallbonus** und den **Sofortrabatt**" — and [S1], [S3] and [S4] all carry exactly that pair, *Sofortrabatt* while premiums are paid and *Todesfallbonus* once paid up. **And the asymmetry, stated plainly**: the *Tarifbeitrag* agreed at inception "ist der **maximal zu leistende Versicherungsbeitrag**", and if the insurer earns less surplus "steigt der Beitrag für den Versicherten höchstens bis zu dieser Höhe an" — which is `product-spec.md`'s asymmetry section in the carrier's own words; `technical-notes.md` cites it in the contractual-elements table beside the *Zahlbeitrag* row. **Correction:** the entry previously claimed this page for a four-component surplus vocabulary — *Zins-*, *Risiko-*, *Kosten-* and *übrige Überschüsse*. It uses no such vocabulary; it names **three** factors — the capital-market result, the insurer's cost structure, and the number of deaths — which is the MindZV three of [R9] and the three [S3]'s § 3 lists. The four-component form belongs to the endowment product, not here, and has been corrected in `product-spec.md`. **No rate, no *Beitragsverrechnung* percentage and no spread ratio is on this page** — those come from [S2] instead

(delib-risikolebensversicherung-s6)=

### S6 — Debeka Lebensversicherungsverein a. G., *Bedingungswerk* for the *Risikoversicherung*
- Publisher / doc type: Debeka Lebensversicherungsverein a. G.; *Bedingungswerk* (Debeka's name for its AVB booklets) in the carrier's public *Vertragsgrundlagen* library
- URL: the path pattern the library carried, `https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/`, now returns **HTTP 404**. The carrier's current *Vertragsgrundlagen* library is at `https://www.debeka.de/service/vertragsgrundlagen.html`, which retrieves and lists a *Risikolebensversicherung* section — but the per-document links are injected client-side and are **not in the served HTML**, so no term-assurance PDF address could be reached
- Retrieved: **no** — the cited path 404s and the replacement library page returns its index without document links (checked 2026-08-30). Entry kept as a known reference
- Used for: the largest German life mutual by contract count in `product-spec.md`'s variations table, and for two inherited cautions the specification repeats rather than hides — **both of which this pass confirmed from other carriers' documents**. A carrier does maintain several parallel wordings within one product family: [S3] ships an AVB and two sets of *Besondere Bedingungen* over three product variants, and [S4] runs eight term tariffs T1–T8 under one AVB. And *Überschussbeteiligung* clause numbering is indeed carrier- and tariff-dependent — the same clause is **§ 2** in the [S1] model wording, **§ 3** at [S3] and **§ 20** at [S4] — so the caution stands and its tag is removed: **a section number in a German AVB must be cited with the wording it comes from**, which every AVB citation in this file now is. **No Debeka term-assurance figure is asserted**

(delib-risikolebensversicherung-s7)=

### S7 — Dialog Lebensversicherungs-AG (Generali group), *Risikolebensversicherung*
- Publisher / doc type: Dialog Lebensversicherungs-AG; AVB, *Verbraucherinformation*, broker-facing tariff material
- URL: not established. `dialog-versicherung.de` returned an HTTP error and `dialog-leben.de` serves a broker portal whose only public route is a *Risikovoranfrage* form; no public conditions library was reachable (checked 2026-08-30)
- Retrieved: **no** — the carrier publishes its wordings behind the broker channel, which is itself the fact this entry records. Entry kept as a known reference
- Used for: the German market's specialist term-life carrier for the broker channel, in `product-spec.md`'s variations and distribution sections, and for one argument that reaches the mechanics: a **monoline's *Risikoergebnis* is its entire technical result**, so the MindZV minimum allocation [R9] binds its surplus policy directly rather than competing with an investment result. The positioning is asserted from market knowledge; **no wording, tariff, rate, *Berufsgruppen* table or surplus declaration is asserted** (gap 5)

(delib-risikolebensversicherung-s8)=

### S8 — Allianz Lebensversicherungs-AG, *Risikolebensversicherung*
- Publisher / doc type: Allianz Lebensversicherungs-AG; AVB, *Produktinformationsblatt*, product page
- URL: not established. The carrier's *Risikolebensversicherung* product page retrieves but carries **no document links in the served HTML** — the conditions are reached through a quote flow, not published as files (checked 2026-08-30)
- Retrieved: **no** — no term-assurance document address could be reached. Entry kept as a known reference
- Used for: the market leader by premium income and the tied-agent end of the distribution range in `product-spec.md`'s variations table, and as the natural reference for the **narrow-spread** end of the *Brutto*/*Zahlbeitrag* distribution — a structural argument, not an observation (gap 1). One inherited fact about the family of Allianz life wordings is recorded and then set aside: a declared *laufende Verzinsung* for 2026 of **2,70 %** on the classic book [inherited: `kapitallebensversicherung.md` S11], a **savings-side** rate of no use here, where the *Zinsüberschuss* is negligible

(delib-risikolebensversicherung-s9)=

### S9 — R+V Lebensversicherung AG, *Risikolebensversicherung*
- Publisher / doc type: R+V Lebensversicherung AG; AVB, *Produktinformationsblatt*, product page
- URL: not established; not searched for in this pass, the two direct writers [S3] [S4] and the model wording [S1] having settled the clause questions this entry would have been read for
- Retrieved: **no**. Entry kept as a known reference
- Used for: the cooperative-bank channel comparator in `product-spec.md`'s variations and distribution sections. **Nothing about its wording, rating structure or surplus declaration is asserted**

(delib-risikolebensversicherung-s10)=

### S10 — NÜRNBERGER Lebensversicherung AG, *Risikolebensversicherung*
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; AVB, *Verbraucherinformation*
- URL: not established. The carrier's tariff-code convention is visible in the sibling research, which recorded an annuity wording headed "…nach Tarif NIR3301" [inherited: `klassische_rentenversicherung.md` S9]; **the term-assurance code is not established**
- Retrieved: **no**; not searched for in this pass, for the reason given at [S9]. Entry kept as a known reference
- Used for: a broker-channel carrier with a long biometric-risk book, in `product-spec.md`'s variations table only. **No parameter is asserted**

(delib-risikolebensversicherung-s11)=

### S11 — LV 1871 (Lebensversicherung von 1871 a. G.), *Risikolebensversicherung*
- Publisher / doc type: Lebensversicherung von 1871 a. G.; AVB, *Produktinformationsblatt*
- URL: not established. The carrier's *Risikolebensversicherung* page retrieves but publishes no conditions PDF in its served HTML (checked 2026-08-30)
- Retrieved: **no**. Entry kept as a known reference
- Used for: the carrier whose range emphasises *Nachversicherungsgarantien* and occupational differentiation, cited in `product-spec.md`'s riders-and-options section and in `model.md`'s provenance table for `nvg_schedule.csv`. The emphasis is still asserted from market knowledge and nothing of LV 1871's own is read. **But gap 7 is no longer open**: [S3] § 13 now supplies a complete event list, a twelve-month exercise window, a 20 % / 50 000 € per-event cap, a five-occasion cumulative cap and an age-50 limit from a carrier wording, and `model.md` records how `nvg_schedule.csv`'s **[std]** parameters compare. The option remains **off in the base run**

(delib-risikolebensversicherung-s12)=

### S12 — Continentale Lebensversicherung a. G. and Europa Lebensversicherung AG, *Risikolebensversicherung*
- Publisher / doc type: Continentale Lebensversicherung a. G. and Europa Lebensversicherung AG; AVB, *Produktinformationsblätter*, product pages. Deliberately a **single entry**, because the pair is one group running a broker-channel and a direct-channel carrier side by side in the same product
- URL: not established for either; the natural-experiment comparison this entry proposes was not run in this pass either
- Retrieved: **no**. Entry kept as a known reference
- Used for: `product-spec.md`'s variations section, as **the cleanest natural experiment available** for isolating the channel effect on the *Brutto*/*Zahlbeitrag* spread with underwriting and reserving basis held constant — and for the record that **it was not run** (gap 5). Cited jointly with [S3] in `technical-notes.md` and `model.md` wherever the **[std]** acquisition cost at the Zillmer ceiling is flagged as the charge most likely to be overstated

(delib-risikolebensversicherung-s13)=

### S13 — Further carriers selling a *Risikolebensversicherung* in Germany
- Publisher / doc type: Alte Leipziger; Volkswohl Bund; Swiss Life Deutschland; Zurich Deutscher Herold; ERGO Vorsorge; AXA; Barmenia; Württembergische; Gothaer; Die Stuttgarter; Baloise (Deutschland); uniVersa; DEVK; SIGNAL IDUNA; Provinzial; Generali Deutschland; HDI — AVB and *Produktinformationsblätter*
- URL: not established for any of them
- Retrieved: **no**; none was searched for, and none may be cited for anything beyond its own existence. Entries kept as known references
- Used for: **one thing only** — that each of these carriers offers an individual *Risikolebensversicherung* in Germany, so `product-spec.md`'s variations section can state honestly that a market of this breadth exists and that **none of it was sampled**. **No `[S13]` tag appears on any parameter anywhere in the delib library**, and none may be added. Two of these carriers appear in the sibling research with located documents in *other* product families — Zurich Deutscher Herold [inherited: `klassische_rentenversicherung.md` S4–S7] and Gothaer [inherited: `kapitallebensversicherung.md` S7] — which establishes that their document libraries are public and nothing whatever about their term-assurance wordings

(delib-risikolebensversicherung-s14)=

### S14 — Comparison portals: Check24, Verivox, Tarifcheck — **secondary**
- Publisher / doc type: Check24, Verivox, Tarifcheck; price-comparison result pages and accompanying *Ratgeber* articles. Secondary, not product documents
- URL: not established for the term-assurance pages. The sibling research recorded Verivox *Ratgeber* pages on `Kapitallebensversicherung`, `Überschussbeteiligung` and `Zillmerung` [inherited: `kapitallebensversicherung.md` S15], establishing that the portal publishes explanatory pages of this kind and nothing about its term-assurance pages
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the finding that the portals are **the only public source of German RLV price points**, because no German carrier publishes a rate card and the PIB quotes only the applicant's own premium — and for **why none could be obtained even in principle**: a comparison result is generated per query and is not a published document. `product-spec.md` cites it in the premium section and the market-context section for that; `model.md` cites it in the mechanics-demonstration warning. **No price point of any kind is recorded from it** (gap 1)

(delib-risikolebensversicherung-s15)=

### S15 — Finanztip, "Risikolebensversicherung" — **secondary**
- Publisher / doc type: Finanztip; consumer guide article with a periodically refreshed carrier recommendation. Secondary
- URL: not established. The sibling research recorded Finanztip articles on `Überschussbeteiligung Lebensversicherung` and `Steuer auf Lebensversicherung` [inherited: `kapitallebensversicherung.md` S16], establishing coverage of the subject area and nothing about this article
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the German consumer publication that most consistently makes the ***Brutto*/*Zahlbeitrag* distinction the headline of its term-life advice** — compare the *Bruttobeitrag*, because the *Zahlbeitrag* is what you pay and the *Bruttobeitrag* what you can be made to pay. `product-spec.md` cites it in its overview and in the asymmetry section; `technical-notes.md` cites it beside the benefit rows for the plain statement that nothing is paid on survival or on *Kündigung*; `model.md` cites it for the three sum-insured shapes being structural. **No figure, ranking or spread statistic is asserted** (gap 1)

(delib-risikolebensversicherung-s16)=

### S16 — Stiftung Warentest / *Finanztest*, term-life comparison tests — **secondary**
- Publisher / doc type: Stiftung Warentest; periodic comparison test of RLV tariffs, paywalled with a free summary. Secondary
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the market's most influential comparison test, cited in `product-spec.md`'s variations and market-role sections and in `model.md`'s warning — and cited above all for **its design**, which is why it matters: *Finanztest* rates on the ***Zahlbeitrag* for defined model customers** at a stated age, sum, term and smoking status **and separately reports the *Bruttobeitrag***, so a published test is the one German document type that would supply exactly the paired figures this product lacks. **No edition, date, model-customer definition or premium figure is asserted** (gap 1)

(delib-risikolebensversicherung-s17)=

### S17 — Franke und Bornberg, MORGEN & MORGEN, ASSEKURATA — **secondary**
- Publisher / doc type: Franke und Bornberg; MORGEN & MORGEN; ASSEKURATA; tariff ratings (`FB-Unternehmensrating`, `M&M Rating Risikoleben`), market studies and *Bedingungsanalysen*. Secondary
- URL: not established for any term-life rating. The sibling research located Assekurata's "24. Marktstudie *Überschussbeteiligungen und Garantien 2026*" and Franke und Bornberg commentary on *Basisinformationsblätter* [inherited: `kapitallebensversicherung.md` R25, R27], establishing that these houses publish in this field and nothing about their term-life work
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: two market-design facts no statute supplies, both `[unverified]` and both structural rather than numeric: that the ***Brutto*/*Zahlbeitrag* spread is itself a rated criterion**, because it measures the insurer's unilateral headroom to raise the billed premium — which is why `product-spec.md`'s asymmetry section and `model.md`'s two-premium section can say the German market treats the spread as a quality signal — and that the ***Nachversicherungsgarantie* event list, caps and age limit are rated criteria**, which is why the market has converged on a recognisable list. **Neither is used as a numeric parameter anywhere**

---

## Regulatory and actuarial references (product research numbering)

The statutes below were read from the **canonical XML** that `gesetze-im-internet.de` publishes for
each instrument, which carries the law's `Stand`. That is what `Retrieved: yes` means in this
section, and each entry records the `Stand` it was read at. The `.../<law>/__NNN.html` addresses are
kept as the **human-facing link** and nothing more: they answer 200 with a frameset of a few
kilobytes containing **no statutory text**, so a section cited only through one of them is not
retrieved. Where a section is load-bearing the entry now **quotes it exactly**, in German, from that
XML; every other statement about a section is still this author's paraphrase, and paragraph numbers
that were not read are still marked `[unverified]`.

(delib-risikolebensversicherung-r1)=

### R1 — VVG § 161, *Selbsttötung*
- Publisher / doc type: Bundesministerium der Justiz (Versicherungsvertragsgesetz 2008); federal statute, Kapitel 5
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` (human-facing link; that page is a 4 kB frameset with no statutory text). Read from `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: **the strongest single item in this product's corpus, and now quoted rather than paraphrased.** Abs. 1: "Bei einer Versicherung für den Todesfall ist der Versicherer nicht zur Leistung verpflichtet, wenn die versicherte Person sich **vor Ablauf von drei Jahren nach Abschluss des Versicherungsvertrags** vorsätzlich selbst getötet hat. Dies gilt nicht, wenn die Tat in einem die freie Willensbestimmung ausschließenden Zustand krankhafter Störung der Geistestätigkeit begangen worden ist." Abs. 2 makes the period extendable by individual agreement — "Die Frist nach Absatz 1 Satz 1 kann durch Einzelvereinbarung erhöht werden" — and Abs. 3 requires payment of "den Rückkaufswert einschließlich der Überschussanteile nach § 169". `product-spec.md` builds its *Selbsttötung* section and its Germany/France comparison on it; `technical-notes.md` makes it the § 161 benefit switch, `suicide_years = 3`, applied to death claims only and tranche by tranche; `model.md` states the switch and its per-increment restart. **Gap 9 is closed, and not by the statute**: § 161 Abs. 1 runs the clock from *Abschluss des Versicherungsvertrags* and is silent on increases, but the **contract** wordings are not, and three of them agree in near-identical terms — [S1] § 5 Abs. 3, [S3] § 2 Abs. 4 and [S4] § 19 Abs. 3 all restart the three years "bezüglich des geänderten oder wiederhergestellten Teils". The model's per-increment restart is market practice; it is now sourced to [S1] [S3] [S4] rather than to [R1], and the `[unverified]` tag is removed

(delib-risikolebensversicherung-r2)=

### R2 — VVG § 169, *Rückkaufswert*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` (human-facing link). Read from `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: **the entry this pass changed most, and it moved in both directions.** The scope limitation is **confirmed word for word**, so gap 2's tag — the one the file called the most consequential in this product — is removed. Abs. 1: "Wird eine Versicherung, die Versicherungsschutz für ein Risiko bietet, bei dem **der Eintritt der Verpflichtung des Versicherers gewiss ist**, durch Kündigung des Versicherungsnehmers oder durch Rücktritt oder Anfechtung des Versicherers aufgehoben, hat der Versicherer den Rückkaufswert zu zahlen." A term assurance's insured event is not *gewiss*, so **the Abs. 1 duty does not attach on *Kündigung***. Abs. 3's *Mindestrückkaufswert* — the *Deckungskapital*, but at least what results "bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre" — and Abs. 5's *Abzug* test, including "Die Vereinbarung eines Abzugs für noch nicht getilgte Abschluss- und Vertriebskosten ist unwirksam", are confirmed as well. **But the conclusion the library drew from Abs. 1 went further than the section allows, and the retrieved wordings contradict it.** § 169 *defines* the *Rückkaufswert*; it does not abolish it for this product, and §§ 152 Abs. 2, **161 Abs. 3** and **165 Abs. 1 Satz 2** each route a term contract to it. The market then pays it: [S1] § 13 Abs. 8 and [S4] § 13 both make *Kündigung* **convert the contract into a *beitragsfreie Versicherung***, and where the paid-up sum fails a carrier-set minimum they pay "den Rückkaufswert entsprechend § 169 des Versicherungsvertragsgesetzes (VVG)" — at [S4] the *Deckungskapital* less an *Abzug* of **60 %**, with a *Rückkaufswerte* table annexed to the *Versicherungsschein* for every tariff but the two falling-sum ones. Only [S3] § 15 Abs. 10 says flatly "Bei einer vollständig gekündigten Versicherung fällt kein Rückkaufswert an und Ihre Versicherung erlischt". So **"no cash value anywhere" is a claim about magnitude, not about contract design**, and "corroborated by uniform market practice" was wrong — the practice is not uniform. What *is* uniform is the magnitude, and both model and carrier wordings say it in the same words: the *Kostenverrechnung* leaves "keine oder nur geringe Mittel" ([S1] § 14 Abs. 4, [S3] § 16 Abs. 4). `product-spec.md` and `technical-notes.md` are corrected accordingly; `model.md`'s `claims_lapse = 0` is **unchanged** and is now carried as a best-estimate approximation of a nil-or-nominal amount rather than as a structural identity

(delib-risikolebensversicherung-r3)=

### R3 — VVG § 165, *Prämienfreie Versicherung* (*Beitragsfreistellung*)
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` (human-facing link). Read from `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: the right the library called **empty in substance** — which is half right, and the half that is wrong matters. Abs. 1 confirmed: "Der Versicherungsnehmer kann jederzeit für den Schluss der laufenden Versicherungsperiode die Umwandlung der Versicherung in eine prämienfreie Versicherung verlangen, sofern die dafür vereinbarte Mindestversicherungsleistung erreicht wird. Wird diese nicht erreicht, hat der Versicherer den auf die Versicherung entfallenden Rückkaufswert einschließlich der Überschussanteile nach § 169 zu zahlen." Abs. 2 computes the paid-up benefit "nach anerkannten Regeln der Versicherungsmathematik mit den Rechnungsgrundlagen der Prämienkalkulation unter Zugrundelegung des Rückkaufswertes nach § 169 Abs. 3 bis 5" — which is where the *Stornoabzug* enters, by reference to § 169 Abs. 5 and not from § 165 itself. **The open question of gap 2 is answered: § 165 carries no *gewiss* limitation of its own.** The right therefore exists in full on a term contract, and the retrieved wordings show it being exercised: [S3] § 15 Abs. 1 sets the paid-up sum from the *Deckungskapital* with the § 169 Abs. 3 five-year floor and ends the contract only below a **300 €** minimum; [S4] § 13 Abs. 3 uses a **2 500 €** minimum. **So the claim that the paid-up right is empty is wrong as stated.** It is empty on a **falling** sum insured, where [S3] says "kalkulationsbedingt kein Deckungskapital" is built and "eine Beitragsfreistellung nicht möglich" is the result; on a **constant** sum insured it produces a real, small paid-up cover. `product-spec.md`'s termination section has been corrected. `technical-notes.md`'s `claims(t, "LAPSE") = 0` is unaffected, because a *Beitragsfreistellung* pays nothing at the time — it converts

(delib-risikolebensversicherung-r4)=

### R4 — VVG §§ 19–22, *Vorvertragliche Anzeigepflicht* and *Anfechtung*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__19.html`, `__20.html`, `__21.html`, `__22.html` (human-facing links). Read from `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: **yes** for §§ 19, 21 and 22 (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30). § 20 (*Vertreter des Versicherungsnehmers*) was not read and is not relied on
- Used for: the whole of `product-spec.md`'s underwriting-and-rating section, now verified. § 19 Abs. 1 is **question-bounded** in terms: the policyholder must disclose the *Gefahrumstände* known to him that are material "und **nach denen der Versicherer in Textform gefragt hat**" — there is no free-standing duty to volunteer. § 19 Abs. 5's warning requirement ("nur ... wenn er den Versicherungsnehmer durch gesonderte Mitteilung in Textform auf die Folgen einer Anzeigepflichtverletzung hingewiesen hat"), § 21 Abs. 2's causation defence and § 22's preservation of *Anfechtung wegen arglistiger Täuschung* are confirmed, and their `[unverified]` tags are removed. **§ 21 Abs. 3 confirmed exactly**, including that the periods sit there and not in § 19: "Die Rechte des Versicherers nach § 19 Abs. 2 bis 4 erlöschen nach Ablauf von fünf Jahren nach Vertragsschluss ... Hat der Versicherungsnehmer die Anzeigepflicht vorsätzlich oder arglistig verletzt, beläuft sich die Frist auf zehn Jahre." **One correction.** The entry said § 19 "gives the insurer the right to accept with restrictions or only at an increased premium". It does not: pre-contractual underwriting terms come from freedom of contract. What § 19 Abs. 4 Satz 2 gives is the **retrospective** route after a breach — the other terms "werden auf Verlangen des Versicherers rückwirkend ... Vertragsbestandteil" — and that is where a retrospective *Risikozuschlag* or *Leistungsausschluss* comes from. **One addition**: Abs. 6 lets the policyholder terminate without notice within a month where such a change raises the premium by more than 10 % or excludes the undisclosed risk — and [S3] § 18 Abs. 6 carries the same 10 % right for a smoking *Gefahrerhöhung*. **Still not cited by `technical-notes.md` or `model.md`**: underwriting is a specification fact, and the model carries only its numeric residue, `rating_factor`

(delib-risikolebensversicherung-r5)=

### R5 — VVG § 153, *Überschussbeteiligung*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` (human-facing link). Read from `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: the statutory footing of the central mechanic, now read. Abs. 1: "Dem Versicherungsnehmer steht eine Beteiligung an dem Überschuss und an den Bewertungsreserven (Überschussbeteiligung) zu, es sei denn, die Überschussbeteiligung ist durch **ausdrückliche Vereinbarung** ausgeschlossen; die Überschussbeteiligung **kann nur insgesamt ausgeschlossen** werden." Abs. 2 requires a *verursachungsorientiertes Verfahren*. That last clause of Abs. 1 is new to the library and is the reason `surplus_form = keine` at model point 12 is an **all-or-nothing** switch and not a partial exclusion. Both carrier wordings open their surplus clause by citing the section — [S3] § 3 and [S4] § 20 Abs. 1 both begin "Sie erhalten gemäß § 153 des Versicherungsvertragsgesetzes (VVG) eine Überschussbeteiligung" — and both then allocate by *Bestandsgruppe*, [S1] § 2 Abs. 3 adding the *Gewinnverband* as the unit inside it. On a product with no account to credit the cause-oriented allocation returns the RLV book's own margin **as a reduction of the premium**, which is *Beitragsverrechnung*; `product-spec.md`, `technical-notes.md`'s derivation of `v_d` and `model.md`'s two-premium section all rest on that. **The *Bewertungsreserven* tag is removed and the claim strengthened**: Abs. 3 grants the half-share, but [S3] § 3 Abs. 1 c states the premiums leave no capital to hold, so "daher entstehen dem Grunde nach **keine Bewertungsreserven**, welche den Verträgen zugeordnet werden könnten" — not merely negligible, but none

(delib-risikolebensversicherung-r6)=

### R6 — VVG § 163, *Prämien- und Leistungsänderung* (the *Treuhänder* clause)
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` (human-facing link). Read from `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: **the single most important legal fact about the German term-life premium**, and it is a fact about what § 163 does *not* reach — which survives, with the entry's own heading corrected. The section is titled ***Prämien- und Leistungsänderung***, not "Anpassung der Prämie". Abs. 1 permits a *Neufestsetzung* of the premium on three cumulative conditions: that "sich der **Leistungsbedarf** nicht nur vorübergehend und nicht voraussehbar gegenüber den Rechnungsgrundlagen der vereinbarten Prämie geändert hat"; that the new premium is "angemessen und erforderlich" to guarantee *dauernde Erfüllbarkeit*; and that "ein unabhängiger Treuhänder" has checked and confirmed both — with re-setting excluded where the original calculation was inadequate and a careful actuary should have seen it. Abs. 2 lets the policyholder demand a benefit reduction instead; Abs. 4 drops the *Treuhänder* where supervisory approval is required. On a German RLV that route is essentially never used, the *Bruttobeitrag* being guaranteed for the term — [S3] states the guarantee ("bleibt Ihre Absicherung sowie der vereinbarte Bruttobeitrag über die gesamte Versicherungsdauer unverändert") and [S5] states its consequence, that the *Tarifbeitrag* "ist der maximal zu leistende Versicherungsbeitrag". What moves the customer's bill is the ***Überschussdeklaration***: cutting the *Beitragsverrechnung* raises the *Zahlbeitrag* toward the *Bruttobeitrag* with **no § 163 procedure, no *Treuhänder* and no policyholder remedy**, because no guaranteed term has changed — and [S4] § 20 Abs. 4 says the declaration "kann auch Null Euro betragen", which is the whole of the asymmetry in one carrier sentence. `product-spec.md`'s asymmetry section, `technical-notes.md`'s `decl_scale` stress and `model.md`'s two-premium argument all cite it. The `[unverified]` tag on "§ 163 is not used in practice on RLV *Bruttobeiträge*" is **kept**: it is a statement about practice that no retrieved document reports either way

(delib-risikolebensversicherung-r7)=

### R7 — VVG §§ 150, 159, 162 — *Versicherte Person*, *Bezugsberechtigung*, *Tötung durch Leistungsberechtigten*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `.../vvg_2008/__150.html`, `__159.html`, `__162.html` (human-facing links). Read from `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: `product-spec.md`'s three-roles paragraph, its *verbundene Leben* section and its *Über-Kreuz* section — all three sections verified, and the tags removed. § 150 Abs. 1 permits insurance on the life of another; Abs. 2 requires that person's consent in terms: "Wird die Versicherung für den Fall des Todes eines anderen genommen und übersteigt die vereinbarte Leistung den Betrag der gewöhnlichen Beerdigungskosten, ist zur Wirksamkeit des Vertrags die **schriftliche Einwilligung** des anderen erforderlich" — with an exception for *betriebliche Altersversorgung*, a special rule in Abs. 3 for a parent insuring a minor child, and Abs. 4 leaving the *Beerdigungskosten* ceiling to the supervisor. This is the provision every *verbundene Leben* and *Über-Kreuz* arrangement runs on. § 159 Abs. 2 and Abs. 3 fix when the beneficiary's right arises — on the insured event for a revocable designation, on designation itself for an *unwiderruflich* one — which is why the benefit reaches the beneficiary outside the estate. **The entry's heading was wrong** and is corrected: § 162 is titled ***Tötung durch Leistungsberechtigten***, not *Herbeiführung des Versicherungsfalles* (which is § 81, in the general part). Its substance is as stated: the insurer is *leistungsfrei* where the policyholder intentionally and unlawfully brings about the death of the insured person, and a beneficiary who does so is treated as never designated. **Not modelled**: the forfeitures are not best-estimate events

(delib-risikolebensversicherung-r8)=

### R8 — VVG § 152 (*Widerruf des Versicherungsnehmers*), § 166 (*Kündigung des Versicherers*), § 168 (*Kündigung des Versicherungsnehmers*)
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `.../vvg_2008/__152.html`, `__166.html`, `__168.html`, and `__12.html` and `__38.html` for the two rules the entry had misattributed (human-facing links). Read from `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: **yes** for §§ 12, 38, 152, 166, 168 and 171 (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: the exit machinery, in `product-spec.md`'s termination section and in `technical-notes.md`'s lapse and no-cash-value conventions — **with two errors found and fixed**. § 152 Abs. 1 confirmed exactly: "Abweichend von § 8 Absatz 1 Satz 1 beträgt die **Widerrufsfrist 30 Tage**", which delib absorbs into the year-one lapse rate **[std]** rather than modelling separately. **Error one**: § 166 is titled *Kündigung des Versicherers*, not *Beitragsverzug*, and it does not impose a *Textform* demand — Abs. 1 says only that where the **insurer** terminates, "wandelt sich mit der Kündigung die Versicherung in eine prämienfreie Versicherung um", with § 165 applying. **Error two**: the *Textform* demand belongs to **§ 38 Abs. 1**, and its minimum period is **two weeks, not a month** — "eine Zahlungsfrist bestimmen, die mindestens zwei Wochen betragen muss". (The month is § 38 Abs. 3 Satz 3's cure period after termination.) § 168 Abs. 1 confirmed: "Sind laufende Prämien zu zahlen, kann der Versicherungsnehmer das Versicherungsverhältnis jederzeit für den Schluss der laufenden Versicherungsperiode kündigen" — and **§ 12 supplies the period**: "Als Versicherungsperiode gilt, falls nicht die Prämie nach kürzeren Zeitabschnitten bemessen ist, der Zeitraum eines Jahres." So a monthly-paying contract is terminable monthly, as the entry said, and the carriers go further still: [S3] § 15 Abs. 9 and [S4] § 13 Abs. 1 both allow termination "jederzeit zum Ende des laufenden Monats" whatever the *Zahlweise*, [S3] refunding the unexpired part of a prepaid premium. That makes `technical-notes.md`'s annual-grid anniversary-only exits **more** of an approximation than the entry claimed, not less. Worth recording alongside: **§ 168 Abs. 2 confines the single-premium termination right to a *gewiss* risk**, the same test as § 169 Abs. 1, so a single-premium term assurance has no § 168 right at all — not a case this product models. § 171 confirms the *halbzwingend* range: "Von § 152 Absatz 1 bis 4 und den §§ 153 bis 155, 157, 158, 161 und 163 bis 170 kann nicht zum Nachteil des Versicherungsnehmers ... abgewichen werden"

(delib-risikolebensversicherung-r9)=

### R9 — MindZV, *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung*
- Publisher / doc type: Bundesministerium der Finanzen; federal regulation
- URL: `https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html` (retrieves in full, OK, ~53 kB) · `https://www.buzer.de/gesetz/12013/a198221.htm` (OK). Read from `https://www.gesetze-im-internet.de/mindzv_2016/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688, read 2026-08-30)
- Used for: **the engine of the German term product** — and **gap 4 is closed**: the section attribution the file refused to guess is settled, and the three percentages sit in three consecutive sections. **§ 7 (*Risikoergebnis*)**: "Die Mindestzuführung zur Rückstellung für Beitragsrückerstattung in Abhängigkeit vom Risikoergebnis für die überschussberechtigten Versicherungsverträge beträgt **90 Prozent** des auf überschussberechtigte Versicherungsverträge entfallenden Risikoergebnisses". **§ 8 (*Übriges Ergebnis*)**: **50 Prozent**. **§ 6 Abs. 1 (*Kapitalanlageergebnis*)**: **90 Prozent** of the *anzurechnende Kapitalerträge* "abzüglich der rechnungsmäßigen Zinsen" — the entry's paraphrase, "after the *Deckungsrückstellung* discounting charge", is right but the regulation's own words are tighter. § 4 Abs. 1 and § 7 Satz 2 confirm the separate *Alt-*/*Neubestand* computation. One refinement the library did not have: each of the three is **floored at zero** — "Ergeben sich rechnerisch negative Beträge ..., werden sie durch Null ersetzt" — so the 90 % is a one-way minimum, not a sharing rule. An RLV's technical outcome is almost entirely *Risikoergebnis*, so 90 % of the tariff's mortality margin must go back, and *Beitragsverrechnung* is the only route on a product with no account to credit. **Both carrier wordings cite the regulation and both state the percentages**: [S3] § 3 Abs. 1 a gives 90 % / 50 % / 90 % in the same order, and [S4] § 20 the same. `technical-notes.md` derives `v_d` from it with `surplus_share = 0.90`; `model.md` names it as the reason the spread is wide and the reason the *Zahlbeitrag* is derived rather than assumed. **MindZV section numbers may now be cited**

(delib-risikolebensversicherung-r10)=

### R10 — DeckRV, *Deckungsrückstellungsverordnung* — *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher / doc type: Bundesministerium der Finanzen; federal regulation
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` · `https://www.buzer.de/gesetz/12006/index.htm` (OK, used for the amendment history). Read from `https://www.gesetze-im-internet.de/deckrv_2016/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 1 V v. **19.7.2024** I Nr. 250 — the *Sechste Verordnung* itself, so the current rate is read at the instrument that set it, read 2026-08-30)
- Used for: the two bounds the tariff is struck inside, both now read, and **gap 11's first half closed**. **§ 2 Abs. 1** — the regulation's own term is ***Höchstzinssatz***, not *Höchstrechnungszins* — "wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf **1 Prozent** festgesetzt", and Abs. 2 fixes it for the whole term of the contract. **§ 4 Abs. 1**, titled *Höchstzillmersätze und versicherungsmathematische Berechnungsmethode*: "Der Zillmersatz darf **25 Promille der Summe aller Prämien** nicht überschreiten" — the base is the sum of all premiums, which is the *Beitragssumme*. **Whether the cap reaches a term product is no longer open**: § 4 draws no product distinction, and both [S1] § 14 Abs. 2 and [S3] § 16 Abs. 2 apply "das Verrechnungsverfahren nach § 4 der Deckungsrückstellungsverordnung" to a *Risikolebensversicherung* and quote the ceiling as **2,5 Prozent** of the premiums payable over the term. **But two things the entry assumed are wrong.** First, § 4 Abs. 1 caps the *zillmerbare* part twice over — at 25 ‰ *and* at the "höchstmöglichen Prämienteile", the parts of the premium needed neither for benefits nor for running costs, which on a term product is the binding constraint. Second, and more consequential for `model.md`, the 25 ‰ is **not the acquisition cost**: [S1] § 14 Abs. 3 and [S3] § 16 Abs. 3 both say "Die restlichen Abschluss- und Vertriebskosten werden über die gesamte Beitragszahlungsdauer verteilt", so total acquisition cost **exceeds** the ceiling and the ceiling bounds only the part recovered by *Zillmerung*. [S2] measures it for one carrier at **2,41 % of the *Tarifbeitragssumme***, just inside the cap. `technical-notes.md` sets `rechnungszins = 0.01` and `zillmer_rate = 0.025` from this entry — but see the register: [S3] prices at a *Rechnungszins* of **0,25 %**, not at the maximum, and [S1] footnote 28 records that the Zillmer clause is included "nur bei der Verwendung des Zillmerverfahrens", so *Zillmerung* on this line is optional. The *Nullstellung* question (gap 11's second half) is still **unresolved** — neither § 4 nor § 341f HGB addresses it — and stays `[unverified]`

(delib-risikolebensversicherung-r11)=

### R11 — VAG §§ 138–140 — *Gleichbehandlung*, *Überschussbeteiligung*, RfB
- Publisher / doc type: Bundesministerium der Justiz (Versicherungsaufsichtsgesetz 2016); federal statute
- URL: `https://www.gesetze-im-internet.de/vag_2016/__138.html`, `__139.html`, `__140.html` (human-facing links) · `https://dejure.org/gesetze/VAG/139.html` (OK). Read from `https://www.gesetze-im-internet.de/vag_2016/xml.zip`
- Retrieved: **yes** for §§ 138 and 140 (canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81, read 2026-08-30). § 139 was not re-read from the XML in this pass and stays as the sibling's inherited item
- Used for: `product-spec.md`'s regulatory context and — the part that reaches the model — the *Gleichbehandlungsgrundsatz*, whose tag is now removed. § 138 is titled *Prämienkalkulation in der Lebensversicherung; Gleichbehandlung*, and Abs. 2 is one sentence: "**Bei gleichen Voraussetzungen dürfen Prämien und Leistungen nur nach gleichen Grundsätzen bemessen werden.**" Note what it says and does not: equal **principles** of measurement for premiums **and benefits** in equal circumstances — not equal amounts, and not in terms a rule about surplus allocation, though *Leistungen* reaches it. That is why an insurer declares one rate per collective rather than negotiating individual discounts, and therefore why `technical-notes.md` can model the *Zahlbeitrag* as a deterministic function of the *Bruttobeitrag* and a declared rate. **The collective's name is now known**: not "tariff generation and rating cell" but the ***Bestandsgruppe*** and, inside it, the ***Gewinnverband*** — [S1] § 2 Abs. 2–3, with [S3] naming *Bestandsgruppe 112* for its term book and [S4] *Bestandsgruppe G* for its collective business. § 138 Abs. 1 adds the prudence requirement the two-order structure implements: premiums must be calculated on "angemessene versicherungsmathematische Annahmen" and be high enough that the insurer can meet all its obligations. § 140 Abs. 1 confirms that RfB funds "dürfen nur für die Überschussbeteiligung der Versicherten ... verwendet werden", with the three supervisory exceptions both carrier wordings reproduce. § 139's *Bewertungsreserven* mechanics are recorded and are **economically empty** here — [S3] § 3 Abs. 1 c says no *Bewertungsreserven* arise on this product at all [R5]

(delib-risikolebensversicherung-r12)=

### R12 — DAV, "Herleitung der Sterbetafel DAV 2008 T für Lebensversicherungen mit Todesfallcharakter"
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; *DAV-Richtlinie* / *Fachgrundsatz*, with a 2008 derivation paper and a 2022 restatement
- URL: `https://aktuar.de/de/wissen/fachinformationen/detail/herleitung-der-sterbetafel-dav-2008-t-fuer-lebensversicherungen-mit-todesfallcharakter/` · `https://aktuar.de/content/PDF/Fachwissen/20080708_DAV_2008_T.pdf` · `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf` · `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T_R_NR.pdf` — **all returned by a search during the sibling research** [inherited: `kapitallebensversicherung.md` R14]
- Retrieved: **no**, on this file's own bar. All four addresses are live and were opened on 2026-08-30 — the *Fachinformation* landing page (HTML, ~53 kB) and three PDFs: the 2008 derivation paper `20080708_DAV_2008_T.pdf` (1,09 MB), and the 2022 *Richtlinie* documents `2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf` (1,14 MB) and `..._R_NR.pdf` (1,67 MB) — **but their text was not read**, so the entry's substantive claims about the derivation, the *Sicherheitszuschlag* procedure and the suitability statements remain the sibling's inherited corroboration. What is newly established is that the documents are public, reachable at the cited addresses, and of the size and kind the entry describes. **A later pass reading them would close gaps 6 and 12**
- Used for: **the mortality basis of this product.** Derived by the DAV *Arbeitsgruppe Biometrische Rechnungsgrundlagen* over **2006 to 2008** from German insurers' own policy data with German population statistics; the *Richtlinie* **regulates the derivation methodology and the procedure for setting the *Sicherheitszuschläge***, not their level; ***DAV 2008 T R*** and ***DAV 2008 T NR*** are in principle **suitable for premium calculation** differentiated by smoking status but **not for policies written without a *Gesundheitsprüfung***; adopted 4 December 2008, restated as a *Fachgrundsatz* dated 29 November 2022. From it the documents take four things: the German first-order basis is DAV 2008 T; the *Sicherheitszuschlag* is part of the table's construction, so first- and second-order are two levels of one framework and the model must publish both; the smoker split is **actuarially sanctioned for pricing**, which is why the market rates on it; and it is not available without underwriting, which is why simplified-issue German death covers are aggregate-rated. **The table values are not public and delib does not redistribute them** — `mort_table.csv` is a **[std]** proxy and `model.md` states the three anchors a replacement must preserve. **The magnitude of the loading was not established** (gap 6); the term-segment data coverage was truncated in the sibling's search summary (gap 12). **One carrier-side corroboration is new**: [S3]'s AVB states its *Rechnungsgrundlagen* as "einer unternehmenseigenen Sterbetafel **auf Basis der DAV 2008T**" — so the table is the base and the carrier's own table is built on it, which is exactly the first- and second-order framework `model.md` publishes both levels of. The *Sicherheitszuschlag* level is still not public (gap 6) and stays `[unverified]`; **DeckRV § 5 Abs. 1 now supplies the legal reason it must exist**: "Die Ableitung von Rechnungsgrundlagen auf der Basis eines besten Schätzwertes genügt nicht. Die Abschätzung künftiger Verhältnisse muss eine nachteilige Abweichung der relevanten Faktoren ... beinhalten" [R10]

(delib-risikolebensversicherung-r13)=

### R13 — Unisex pricing: the EU Gender Directive, CJEU C-236/09 (*Test-Achats*), AGG § 20
- Publisher / doc type: Court of Justice of the European Union; Bundesministerium der Justiz; judgment and federal statute
- URL: `https://www.gesetze-im-internet.de/agg/__19.html`, `__20.html`, `__33.html` (human-facing links). Read from `https://www.gesetze-im-internet.de/agg/xml.zip`. No URL is established for the Directive or for CJEU C-236/09, and none is guessed
- Retrieved: **yes** for the German implementation, §§ 19, 20 and 33 AGG (canonical XML, Stand: zuletzt geändert durch Art. 15 G v. 22.12.2023 I Nr. 414, read 2026-08-30). **No** for the Directive and the judgment — neither was retrieved, and nothing is asserted from either beyond what the AGG text carries
- Used for: the rule that **sex may not enter the premium for contracts concluded from 21 December 2012** — and the date, which the entry could only corroborate obliquely through `frlib`, is now **read in the German statute**. **AGG § 33 Abs. 5**: "Bei Versicherungsverhältnissen, die **vor dem 21. Dezember 2012** begründet werden, ist eine unterschiedliche Behandlung wegen des Geschlechts im Falle des § 19 Absatz 1 Nummer 2 bei den Prämien oder Leistungen nur zulässig, wenn dessen Berücksichtigung bei einer auf relevanten und genauen versicherungsmathematischen und statistischen Daten beruhenden Risikobewertung ein bestimmender Faktor ist." The transitional carve-out runs to that date and no further. **And § 20 Abs. 2 shows the shape of the prohibition from the other side**: the risk-adequate-calculation justification it preserves is available for "Religion, einer Behinderung, des Alters oder der sexuellen Identität" — **sex is absent from the list**, so no actuarial justification is open for it at all. § 19 Abs. 1 Nr. 2 brings private insurance inside the prohibition. `product-spec.md` states the rule and its consequence; `technical-notes.md` resolves the tension with sex-distinct DAV 2008 T [R12] the only way § 138 VAG allows — the tariff blends the two tables and the projection uses the policy's own sex; `model.md`'s unisex section reports the resulting cross-subsidy between model points 1 and 2. **The mixing ratio is still disclosed by nobody**, so `sex_mix_male = 0.50` remains **[std]**, and that female mortality at these ages is roughly half male remains `[unverified]` — no retrieved document states a ratio

(delib-risikolebensversicherung-r14)=

### R14 — EStG § 20 Abs. 1 Nr. 6 and § 10 Abs. 1 Nr. 3a — income tax and premium deductibility
- Publisher / doc type: Bundesministerium der Justiz (Einkommensteuergesetz); federal statute
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` (OK, ~33 kB) · `https://www.gesetze-im-internet.de/estg/__10.html` · `https://www.gesetze-im-internet.de/estg/__52.html` (human-facing links). Read from `https://www.gesetze-im-internet.de/estg/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: neugefasst durch Bek. v. 8.10.2009 I 3366, 3862, zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: **the section that does not apply — now shown not to apply, twice over, and gap 16's tag removed.** § 20 Abs. 1 Nr. 6 Satz 1 taxes the *Unterschiedsbetrag* "**im Erlebensfall oder bei Rückkauf des Vertrags** bei Rentenversicherungen mit Kapitalwahlrecht ... und bei **Kapitalversicherungen mit Sparanteil**, wenn der Vertrag nach dem 31. Dezember 2004 abgeschlossen worden ist". A pure *Risikolebensversicherung* fails both limbs: it pays on death and not on survival or surrender, and it has no *Sparanteil*. So the *Todesfallleistung* is not investment income of the policyholder and the tax question moves entirely to the *Erbschaftsteuer* [R15]. Satz 2's half-income rule is confirmed at the 60th year, with § 52 raising it to the **62nd** "für Vertragsabschlüsse nach dem 31. Dezember 2011". The **50 % *Mindesttodesfallschutz*** of Satz 6 is confirmed verbatim — the benefit on the insured risk must not be "weniger als 50 Prozent der Summe der für die gesamte Vertragsdauer zu zahlenden Beiträge" — and § 52 applies it to contracts concluded after **31 March 2009**, which is the entry's 1 April 2009 date. **Gap 17 is closed too, and the claim confirmed.** § 10 Abs. 1 Nr. 3a names this product expressly among the *sonstige Vorsorgeaufwendungen*: contributions "zu **Risikoversicherungen, die nur für den Todesfall eine Leistung vorsehen**". § 10 Abs. 4 sets the ceiling at **2 800 Euro** a year for Nr. 3 and Nr. 3a together, or **1 900 Euro** for anyone whose health cover is wholly or partly paid for by someone else — and Satz 4 is decisive: where the basic health and long-term-care contributions of Nr. 3 already exceed the ceiling, they are deducted in full and "ein Abzug von Vorsorgeaufwendungen im Sinne des Absatzes 1 Nummer 3a **scheidet aus**". The entry's claim that the effective deduction is nil for most policyholders is therefore **statute, not inference**, and the ceiling figures may now be stated. **Nothing here is modelled**

(delib-risikolebensversicherung-r15)=

### R15 — ErbStG §§ 3, 15, 16, 19 — the *Erbschaftsteuer* treatment of the death benefit
- Publisher / doc type: Bundesministerium der Justiz (Erbschaftsteuer- und Schenkungsteuergesetz); federal statute
- URL: `https://www.gesetze-im-internet.de/erbstg_1974/` (OK, table of contents) · per-section `.../erbstg_1974/__3.html`, `__15.html`, `__16.html`, `__19.html` (human-facing links). Read from `https://www.gesetze-im-internet.de/erbstg_1974/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: neugefasst durch Bek. v. 27.2.1997 I 378, zuletzt geändert durch Art. 10 G v. 22.6.2026 I Nr. 192, read 2026-08-30)
- Used for: **the only tax that reaches this product — every figure now read, and every one of them right.** § 3 Abs. 1 Nr. 4 is the limb that catches the death benefit, and it is worth quoting because it never mentions insurance: "**jeder Vermögensvorteil, der auf Grund eines vom Erblasser geschlossenen Vertrags bei dessen Tode von einem Dritten unmittelbar erworben wird**". § 15 Abs. 1 puts "alle übrigen Erwerber" in *Steuerklasse III*, which is where an unmarried partner falls. § 16 Abs. 1's *Freibeträge* are confirmed exactly as the entry had them — **500 000 €** spouse or *Lebenspartner*, **400 000 €** children, **200 000 €** grandchildren, **100 000 €** the remaining class I, **20 000 €** classes II and III. § 19 Abs. 1's table confirms the rates: class I opens at **7 %** to 75 000 €, class III at **30 %** and flat to 600 000 €. **The worked illustration checks out against the statute**: on 300 000 € to a spouse the charge is nil; to an unmarried partner it is (300 000 − 20 000) × 30 % = **84 000 €** — the entry's figure, to the euro. The `[unverified]` tags on all of these are removed. They remain **[std]** illustrations downstream and are still not citations of a tariff. `model.md` cites the entry once, to say the *Über-Kreuz* structure changes the tax outcome and **nothing in the cash flows**

(delib-risikolebensversicherung-r16)=

### R16 — VersStG 2021 § 4 Abs. 1 Nr. 5 — *Versicherungsteuer* exemption for life insurance
- Publisher / doc type: Bundesministerium der Justiz (Versicherungsteuergesetz); federal statute
- URL: `https://www.gesetze-im-internet.de/versstg/__4.html`. **The cited address was wrong**: `.../verststg_1996/__4.html` returns HTTP 404 — the slug is `versstg`, not `verststg`, and the consolidated law is now cited as **VersStG 2021**
- Retrieved: **yes** (HTML, ~12 kB — this is one of the few `gesetze-im-internet` per-section pages that serves the text rather than a frameset; read 2026-08-30)
- Used for: the absence of a premium-tax line, now sourced precisely rather than asserted, and the tag removed. The section is titled *Ausnahmen von der Besteuerung*, and the limb that matters is **Abs. 1 Nr. 5 Buchst. a**: exempt is the payment of the *Versicherungsentgelt* "für eine Versicherung, durch die Ansprüche auf Kapital-, Renten- oder sonstige Leistungen begründet werden ... **im Fall des Todes**, des Erlebens oder des Alters". A German RLV premium is therefore billed **without insurance premium tax**, unlike a French *cotisation* quoted "TTC". The entry cited "§ 4" as a whole; the correct citation is § 4 Abs. 1 Nr. 5 Buchst. a, and Satz 2 of that number is worth knowing for the riders — the exemption "gilt nicht für die Unfallversicherung, die Haftpflichtversicherung und sonstige Sachversicherungen", so a UZ rider is not covered by it. `product-spec.md` states it in the premium section, `technical-notes.md` in its contractual-elements table, and `model.md` in the standardizations closing paragraph — recorded in all three **so a reader does not conclude the line was forgotten** (gap 19)

(delib-risikolebensversicherung-r17)=

### R17 — VVG-InfoV, and the PRIIP boundary for a pure protection product
- Publisher / doc type: Bundesministerium der Justiz (VVG-Informationspflichtenverordnung); federal regulation
- URL: `https://www.gesetze-im-internet.de/vvg-infov/` (table of contents; the per-section pages are framesets). Read from `https://www.gesetze-im-internet.de/vvg-infov/xml.zip`
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 13 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: **the entry with the largest correction in this file.** Two of its three claims are confirmed, and the third — the one `model.md` leaned on hardest — is **wrong**. **Confirmed, and better than asserted.** The *Effektivkosten* duty of § 2 Abs. 1 Nr. 9 is owed only "bei Lebensversicherungsverträgen, die Versicherungsschutz für ein Risiko bieten, **bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist**" — the same *gewiss* test as § 169 Abs. 1 VVG [R2]. So there is no *Effektivkosten* figure for a term product, and the reason is not merely that a reduction in yield presupposes a yield: the regulation says so on its face. **Confirmed.** § 4 Abs. 3 disapplies the *Informationsblatt* regime for *Versicherungsanlageprodukte* under Regulation (EU) No 1286/2014, which is the boundary the entry describes — a pure protection contract is not a PRIIP and gets no *Basisinformationsblatt*. (The PRIIPs Regulation itself was **not retrieved**, so the exclusion of death-only contracts from its scope is still `[unverified]`.) **Wrong, and corrected everywhere it appears.** The entry concluded that German term-life charge levels are "**structurally undisclosed, not merely unretrieved**". They are not. § 2 Abs. 1 Nr. 1 requires the insurer to state, for a life contract, "Angaben zur Höhe der in die Prämie einkalkulierten Kosten; dabei sind die einkalkulierten **Abschlusskosten als einheitlicher Gesamtbetrag** und die übrigen einkalkulierten Kosten als **Anteil der Jahresprämie** ... auszuweisen", with the *Verwaltungskosten* shown separately again — and § 2 Abs. 2 requires those figures **in Euro**. § 4 Abs. 2 Satz 2 repeats the duty on the face of the *Informationsblatt zu Versicherungsprodukten* itself, under the heading "Prämie; Kosten" as the last item. Both carrier wordings point the customer there — [S1] § 14 Abs. 1 and [S3] § 16 Abs. 1 — and [S2]'s specimen **prints the figures**. So the charges are disclosed **per contract to the applicant**, and only the *published rate card* is missing. `product-spec.md`'s charges section and `model.md`'s charge-parameter rationale have been corrected; the charge parameters stay **[std]**, because one carrier's model case is not a market

(delib-risikolebensversicherung-r18)=

### R18 — GDV, *Die deutsche Lebensversicherung in Zahlen* and the *Risikoversicherung* statistics
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V.; annual statistical volume and a ten-year *Neugeschäft und Bestand* series
- URL: not established for the term-assurance breakdown. The sibling research located the statistics landing page and the ten-year series [inherited: `kapitallebensversicherung.md` R20, R21]
- Retrieved: **no** — no GDV statistical volume or *Neugeschäft und Bestand* series was retrieved in this pass, and the inherited whole-market *Stornoquote* figures are still second-hand. Entry kept as a known reference
- Used for: a figure the documents **deliberately do not use**. The inherited whole-market *Stornoquote* is **2,72 % (2024)** and **2,56 % (2023)** on the main GDV measure, with a second irreconcilable measure at **1,2 % (2024)**; both are recorded in `product-spec.md`. `technical-notes.md` and `model.md` cite it to say the book average is dominated by long-dated savings contracts and is **not** the term-life lapse assumption, which is argued from structure instead and is **[std]** at 6 % / 4 % / 3 % — a listed modeling pitfall with a test of its own. **The size of the German *Risikoversicherung* segment is not established at all**: no contract count, new business, premium income, aggregate *versicherte Summe*, average sum insured, average premium or segment lapse rate (gap 13)

(delib-risikolebensversicherung-r19)=

### R19 — BaFin supervisory material on life insurance conduct and product governance
- Publisher / doc type: Bundesanstalt für Finanzdienstleistungsaufsicht; *Merkblätter*, *Auslegungsentscheidungen* and risk reports
- URL: not established for any term-life-specific item. The sibling research located **Merkblatt 01/2023 (VA)** *zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden Lebensversicherungsprodukten*, published May 2023, and the *Risiken im Fokus 2026* item on the cost of *kapitalbildende* products [inherited: `kapitallebensversicherung.md` R17, R18]
- Retrieved: **no** — no BaFin item was retrieved; the *Merkblatt* 01/2023 (VA) and the *Risiken im Fokus 2026* entry remain inherited from the sibling research, and **no supervisory literature specific to German term assurance was located** in this pass either (gap 14, still open). Entry kept as a known reference
- Used for: a boundary, in `product-spec.md`'s regulatory context. The *Merkblatt*'s subject is expressly ***kapitalbildende*** life products and its concern is that costs be justified by customer value; **a pure *Risikolebensversicherung* is outside its stated subject matter**. It is cited so that a reader does not import an endowment-conduct standard into a term product, and so that the absence is on the record: **no supervisory literature specific to German term assurance was located** (gap 14)

(delib-risikolebensversicherung-r20)=

### R20 — Rating and analysis houses on German term-life tariff design
- Publisher / doc type: Franke und Bornberg; MORGEN & MORGEN; ASSEKURATA — the same corpus as [S17], seen from the product side; tariff ratings and market studies
- URL: not established
- Retrieved: **no**; the same corpus as [S17], and no term-life rating was read. Entry kept as a known reference
- Used for: the reference class behind two market-design facts no statute supplies, both `[unverified]` and both cited jointly with [S17] in `product-spec.md`: that the ***Brutto*/*Zahlbeitrag* spread is a rated criterion**, and that the ***Nachversicherungsgarantie* event list, caps and age limits are rated criteria**. **No rating, criterion weight or observed distribution is asserted**

(delib-risikolebensversicherung-r21)=

### R21 — HGB § 341f and RechVersV — statutory reserving for a term contract
- Publisher / doc type: Bundesministerium der Justiz (Handelsgesetzbuch; Versicherungsunternehmens-Rechnungslegungsverordnung); federal statute and regulation
- URL: `https://www.gesetze-im-internet.de/hgb/__341f.html` (human-facing link). Read from `https://www.gesetze-im-internet.de/hgb/xml.zip`. The RechVersV was **not** read
- Retrieved: **yes** for HGB § 341f (canonical XML, Stand: zuletzt geändert durch Art. 4 G v. 4.2.2026 I Nr. 33, read 2026-08-30). **No** for the RechVersV
- Used for: `technical-notes.md`'s valuation-and-reserve pointers and `model.md`'s statement that `res_pp_at` is a **pricing diagnostic and not a provision** — both of which stand, but **the entry's description of § 341f did not, and is corrected**. Abs. 1 requires the *Deckungsrückstellung* to be formed "in Höhe ihres versicherungsmathematisch errechneten Wertes einschließlich bereits zugeteilter Überschußanteile ... und nach Abzug des versicherungsmathematisch ermittelten Barwerts der künftigen Beiträge (**prospektive Methode**)", with a retrospective fallback where a prospective value cannot be determined, and Abs. 2 adds the interest-guarantee test that drives the *Zinszusatzreserve*. That is all. **The section says nothing about "the bases used to determine the premium", nothing about "a prudent margin", and nothing about future administration costs where the premium-paying period is shorter than the cover period** — those belong to the DeckRV (§ 5 Abs. 1, quoted at [R10]) and to the RechVersV, which was not read and stays `[unverified]`. [S4] gives the carrier-side citation chain in full: the *Deckungsrückstellung* "wird nach § 88 VAG und § 341e und § 341f HGB sowie den dazu erlassenen Rechtsverordnungen berechnet". The ***Nullstellung*** question — whether a negative individual reserve arising from *Zillmerung* must be floored at zero — is **still not established** (gap 11) and stays `[unverified]`; because no reserve of any kind enters `result_cf()` it does not reach these cash flows. **R21 remains a pointer, not a model input**

(delib-risikolebensversicherung-r22)=

### R22 — Solvency II and the German prudential layer
- Publisher / doc type: EIOPA; BaFin; directive, delegated regulation and supervisory material
- URL: not established
- Retrieved: **no** — nothing product-specific for German term assurance was located, and no directive, delegated act or supervisory text was retrieved in this pass. Entry kept as a known reference, on the same posture as before
- Used for: a pointer only, on the same posture as [R21], in `product-spec.md`'s regulatory context and `technical-notes.md`'s valuation pointers. Nothing product-specific for German term assurance was located, and **no capital, risk-margin, contract-boundary or standard-formula stress figure appears anywhere in this product's documents**. The library publishes gross liability cash flows, undiscounted; the valuation layers consume them and are cited, never reproduced

(delib-risikolebensversicherung-r23)=

### R23 — German case law on *vorvertragliche Anzeigepflicht* and *Selbsttötung* in life insurance
- Publisher / doc type: Bundesgerichtshof and the *Oberlandesgerichte*; decided cases
- URL: not established. **No decision is cited by date or file number anywhere in this product's documents, and none is invented**
- Retrieved: **no** — **no decision was retrieved, and none is cited by date or file number anywhere in this product's documents**. Entry kept as a known reference class, and gap 20 stays open
- Used for: a known reference class rather than a source. German term-life litigation clusters on whether the applicant's answers to the *Gesundheitsfragen* were complete and whether the insurer complied with the § 19 Abs. 5 warning requirement [R4], and on whether a *Selbsttötung* inside the three-year window was committed in a state excluding free will [R1]. `technical-notes.md` and `model.md` cite it for one consequence: **the mental-illness exception is the ground on which German suicide claims are actually litigated, so § 161 is not a clean contractual switch, and a best-estimate cash-flow model cannot represent that** — delib applies the rule as a benefit switch and records the exception as a known simplification. The sibling research located BGH authority on adjacent life questions — the *Stornoabzug* *Bezifferung* requirement and the *Bewertungsreserven* judgment of 20 January 2021, IV ZR 318/19 [inherited: `kapitallebensversicherung.md` R22, R23] — establishing that the court decides this area regularly and nothing about term assurance. **No holding is asserted** (gap 20)

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen; research
provenance in `_research/regulatory-actuarial.md`). **That library was drafted under the same
blocked-egress conditions as this file and re-verified in the same pass**: its head still carries
the drafting account, and each entry now records its own retrieval status on its own line, most of
them `Retrieved: yes` from the canonical XML. Entries cited by the `risikolebensversicherung`
documents:

- **REG-R1** — Directive 2009/138/EC (Solvency II): the best-estimate-plus-risk-margin frame the projected cash flows feed. Nothing here computes it.
- **REG-R2** — Delegated Regulation (EU) 2015/35: contract boundaries and management actions. Cited to record that this product's boundary is *easier* than frlib's revisable one — the *Bruttobeitrag* is guaranteed for the term.
- **REG-R3** — Directive (EU) 2025/2, the Solvency II review, effective 30 January 2027: cited once, to say nothing here implements a 2027 basis.
- **REG-R6** — VAG §§ 74–110 and § 40, valuation, best estimate, risk margin and the SFCR: the German route by which Solvency II reaches this business.
- **REG-R8** — VAG § 138, *Prämienkalkulation* and *Gleichbehandlung*: the cross-product entry behind [R11], and why one declared rate applies per tariff generation and rating cell.
- **REG-R9** — VAG § 139, *Überschussbeteiligung* and the *Sicherungsbedarf* test: cited to say the *Bewertungsreserven* share is **economically empty** on a product whose reserve is nil or nominal.
- **REG-R10** — VAG §§ 140 and 145, the RfB: where a declared *Beitragsverrechnung* comes out of. The model's `prem_rebate` is the contract-level consequence, not the allocation itself.
- **REG-R11** — VAG §§ 141–143, *Verantwortlicher Aktuar* and *Treuhänder*: the office § 163 VVG's procedure runs through [R6], and the office that certifies the tariff bases.
- **REG-R14** — DeckRV and its § 2, the *Höchstrechnungszins*: the cap behind `rechnungszins = 0.01`.
- **REG-R15** — the *Höchstrechnungszins* history and the *Sechste Verordnung* of 19 July 2024 setting 1,00 % from 1 January 2025: the anchor cell's pricing rate, and the reason the notes say it **barely matters** here.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: the 25 ‰ ceiling `zillmer_rate = 0.025` sits at, and half of the reason a *gezillmertes Deckungskapital* is negative for much of a term contract.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins* and the *Zinszusatzreserve*: cited to say it reaches this product **only nominally**, a reader expecting the discussion that dominates the endowment and annuity products will not find one, and that is a product fact.
- **REG-R18** — MindZV: the cross-product entry behind [R9], carrying the 90 % minimum from the *Risikoergebnis* that `surplus_share` is set to.
- **REG-R19** — RfBV, the collective part of the RfB: cited once, to say the MindZV minimum binds on the HGB accounts and is a transfer to the RfB rather than a payout.
- **REG-R20** — LVRG 2014: the reform that cut the *Höchstzillmersatz* to 25 ‰ with effect from 1 January 2015.
- **REG-R22** — VVG 2008, Kapitel 5 and § 171 (*halbzwingende Vorschriften*): the chapter this contract sits in, and the reason §§ 161, 165, 168 and 169 cannot be contracted around to the policyholder's detriment.
- **REG-R23** — VVG §§ 8 and 152, the *Widerrufsrechte*: the 30-day window, absorbed into the year-one lapse rate **[std]** and not modelled separately.
- **REG-R24** — VVG § 153: the cross-product entry behind [R5], carrying the *verursachungsorientiertes Verfahren* and the half-share of *Bewertungsreserven*.
- **REG-R26** — VVG §§ 150, 159, 160, 161 and 162: the cross-product entry behind [R1] and [R7] — the *Einwilligung* every *verbundene Leben* and *Über-Kreuz* arrangement needs, the *Bezugsberechtigung*, and the three-year *Selbsttötung* window the model implements as `suicide_years = 3`.
- **REG-R27** — VVG § 163: the cross-product entry behind [R6], and the section the declaration cut does **not** engage.
- **REG-R28** — VVG §§ 165–170: the cross-product entry behind [R2], [R3] and [R8] — *prämienfreie Versicherung*, *Kündigung*, *Rückkaufswert* and the *Stornoabzug*, all of which terminate in nil here.
- **REG-R29** — VVG §§ 172–177, Kapitel 6, *Berufsunfähigkeitsversicherung*: cited to place the BUZ rider outside this product and inside delib product 9.
- **REG-R30** — VVG §§ 19, 37, 38, 157 and 158: the cross-product entry behind [R4], carrying the question-bounded *Anzeigepflicht* and the *Altersangabe* rule.
- **REG-R31** — VVG §§ 6, 7 and 7b with the VVG-InfoV: the cross-product entry behind [R17], and the source of the *Effektivkosten* duty that has **no application** to a product with no yield.
- **REG-R32** — PRIIPs, Regulation (EU) No 1286/2014: cited for the boundary — a pure protection contract is **not** a PRIIP, so no *Basisinformationsblatt* exists for it.
- **REG-R33** — IDD and § 34d GewO: the distribution frame behind the three-channel market of the variations section.
- **REG-R34** — Unisex, CJEU C-236/09 and §§ 19, 20 and 33 AGG: the cross-product entry behind [R13], and the rule `sex_mix_male` exists to satisfy.
- **REG-R35** — BaFin *Merkblatt* 01/2023 (VA): the cross-product entry behind [R19], cited for its **limit** — it is about *kapitalbildende* products and does not reach a pure protection contract.
- **REG-R36** — the BGH line of authority on German life contracts: the cross-product companion to [R23], cited for the same reason and with no holding asserted about term assurance.
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6, the *Unterschiedsbetrag*, the 12/62 rule and the *Mindesttodesfallschutz*: the cross-product entry behind [R14], cited for the section's **non-application** to a pure death benefit.
- **REG-R46** — ErbStG and the SGB V contribution rules: the cross-product entry behind [R15], and the tax fact the *Über-Kreuz-Versicherung* exists to change.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the framework `mort_rate_tar` and `mort_rate` implement, and the reason the model publishes both orders.
- **REG-R48** — DAV 2008 T and its predecessors: the cross-product entry behind [R12] — **the** table for this product, cited by name and never shipped.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand: cited once, to say the annuity family is **not** the basis for a death-benefit contract.
- **REG-R52** — Destatis *Sterbetafeln* and the reuse licence: cited to say a population table is the **wrong starting point** for a replacement decrement basis — without a selection adjustment it overstates claims by a wide margin at the issue ages this product is sold at.
- **REG-R53** — the German life market in numbers (GDV, BaFin, Assekurata, Map-Report, Morgen & Morgen, Franke und Bornberg): the cross-product companion to [R18] and [R20], and the entry that records that **no term-segment figure was established**.
- **REG-R54** — HGB §§ 341–341o, RechVersV and BerVersV: the cross-product entry behind [R21], and the frame in which the *Nullstellung* question sits.
- **REG-R55** — IFRS 17, effective 1 January 2023 with no German carve-out: cited once in the valuation pointers; grouping, CSM and risk adjustment are out of scope.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional standard this model's documentation sits under.

---

## Provenance note

Extraction details — which fact would be settled by which document, the twenty mechanics sections
the product documents are actually written from, the `[std]` premium-scale construction of
mechanic 16 with its arithmetic shown, and the twenty-three-item gaps-and-caveats register — live
in `_research/risikolebensversicherung.md`. That file is the citation ground truth for the S# and
R# numbering used here; its head records the blocked-egress conditions the research was done under,
and its entries record the same 2026-08-30 re-verification these do.

The caveats that most constrain what these product documents can claim, in order of how much they
constrain the model. **Four of the nine were closed or overturned by this pass and are marked so.**

1. ~~**No price point of any kind was obtained — the largest gap.**~~ **CLOSED for one carrier**
   [S2]. § 2 Abs. 1 Nr. 1 and § 4 Abs. 2 VVG-InfoV make the pre-contractual *Informationsblatt*
   carry the premium and the costs in euro, and a carrier publishes a *Muster* specimen of it. For
   a model case at **age 41, 19 years, 100 000 €**, Cosmos tariff CRB2 shows a monthly
   ***Tarifbeitrag* of 18,21 EUR** against a first-year ***Zahlbeitrag* of 8,20 EUR** — a
   *Beitragsverrechnung* of about **55 %** — and the Comfort tariff CRCB2 gives 23,68 against 10,66
   at the **same rate**, which is § 138 VAG's *Gleichbehandlung* visible in two numbers. An older
   specimen repeats it at 19,75 / 8,89. **These are observations of one direct writer and are not
   generalised**: no [S2] figure is a model parameter, and the [std] scale is unchanged.
2. ~~**No carrier AVB was obtained.**~~ **CLOSED.** Three wordings were read in full — the GDV
   model *Allgemeine Bedingungen für die Risikolebensversicherung*, Stand 21.07.2025 [S1]; Cosmos
   **LA 803 A (04.26)** [S3]; Hannoversche **T25**, Stand 09/2025 [S4]. Between them they settle the
   *Nachversicherungsgarantie* event list, window, caps and age limit (gap 7), the *Kriegsklausel*
   and ABC-clause wording, and the smoker qualifying period at **twelve months** with a switch to
   smoking treated as a *Gefahrerhöhung* (gap 22). Still unsettled from an AVB: the *Berufsgruppen*
   structure, the health-question look-back periods and the medical-examination thresholds.
3. ~~**The statutory basis for the absence of a *Rückkaufswert* is `[unverified]`.**~~
   **VERIFIED — and the conclusion drawn from it OVERTURNED** [R2]. § 169 Abs. 1 does confine the
   duty to a risk "bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist", word for
   word. But the sentence that followed it here — that nothing paid on *Kündigung* is "corroborated
   by uniform market practice and is not in doubt" — is **wrong**. [S1] § 13 Abs. 8 and [S4] § 13
   both convert the contract to a *beitragsfreie Versicherung* on *Kündigung* and pay a
   *Rückkaufswert* under § 169 VVG, less a *Stornoabzug*, where the paid-up sum fails a minimum;
   only [S3] pays nothing at all. **The amount is nil or nominal; the design is not.** This is the
   most important thing this pass found, and it is the one open item that reaches the model.
4. **The *Sicherheitszuschlag* level is not public** [R12] — **still open**, the *Richtlinie*
   regulating the procedure and not the level, though **DeckRV § 5 Abs. 1 now supplies the legal
   reason a loading must exist**: "Die Ableitung von Rechnungsgrundlagen auf der Basis eines besten
   Schätzwertes genügt nicht" [R10]. It sets the *Brutto*/*Zahlbeitrag* spread almost by itself, and
   it ships as **[std]** `m = 1.25` with its calibration and sensitivity stated in full — moving it
   across 1.0 to 1.5 moves the *Bruttobeitrag* 22,5 % and the *Zahlbeitrag* 6,0 %. [S2]'s observed
   ratio of about 2,22 between the two premiums is now a check against it.
5. ~~**German term-life charge levels are structurally undisclosed.**~~ **WRONG, and corrected**
   [R17]. § 2 Abs. 1 Nr. 1 VVG-InfoV requires the *Abschlusskosten* as a single total and the other
   costs as a share of the annual premium, § 2 Abs. 2 requires them **in Euro**, and § 4 Abs. 2 puts
   them on the *Informationsblatt* under "Prämie; Kosten". What is missing is a **published rate
   card**, not disclosure. [S2] prints, for its model case, acquisition cost of **99,98 EUR** =
   **2,41 % of the *Tarifbeitragssumme***, other annual costs of **48,52 EUR** of which **35,20 EUR**
   administration. The **[std]** α at the 25 ‰ ceiling is therefore **close to right for this
   carrier and mis-typed**: [S1] § 14 Abs. 3 and [S3] § 16 Abs. 3 both spread the *remaining*
   acquisition cost over the premium term, so 25 ‰ bounds the *zillmerbare* part, not the total
   [S3] [S12].
6. **No term-segment market or lapse figure exists in the corpus** [R18] — **still open**. The
   whole-market *Stornoquote* is a book average dominated by long-dated savings contracts and is
   deliberately **not used**; the shipped 6 % / 4 % / 3 % is argued from structure and **no German
   figure supports any of it**. The structural argument is now stronger, not weaker: [S3] and [S4]
   both let the policyholder terminate **at the end of any month** whatever the *Zahlweise*.
7. **The unisex mixing ratio is proprietary everywhere** [R13] — **still open**. The mechanism is
   law and the date is now read in AGG § 33 Abs. 5; the ratio is a carrier's own new-business mix,
   disclosed by nobody, and it moves the tariff a great deal.
8. **No case law is named** [R23] and **no BaFin material specific to term assurance was located**
   [R19] — **both still open**. The absences are recorded rather than papered over, and the
   endowment conduct standard must not be imported here.
9. **What was read, and what that changes.** Fifteen statutory sections were read from the
   canonical XML with their `Stand`, three carrier or model wordings and two premium specimens from
   the publishers' own sites; where a rule is load-bearing it is now **quoted exactly** rather than
   paraphrased. The VVG, the DeckRV, the MindZV, the VAG, the EStG, the ErbStG and the DAV
   *Fachgrundsätze* remain living texts and the *Höchstzinssatz* is reset by regulation, so every
   date and rate still carries the `Stand` it was read at and must be re-checked against the
   instrument before it is relied on. **A delib citation is no longer only a pointer where the
   entry says `Retrieved: yes` — but it is still a pointer everywhere it says `no`.**

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-risikolebensversicherung-r1
[R10]: #delib-risikolebensversicherung-r10
[R11]: #delib-risikolebensversicherung-r11
[R12]: #delib-risikolebensversicherung-r12
[R13]: #delib-risikolebensversicherung-r13
[R14]: #delib-risikolebensversicherung-r14
[R15]: #delib-risikolebensversicherung-r15
[R17]: #delib-risikolebensversicherung-r17
[R18]: #delib-risikolebensversicherung-r18
[R19]: #delib-risikolebensversicherung-r19
[R2]: #delib-risikolebensversicherung-r2
[R20]: #delib-risikolebensversicherung-r20
[R21]: #delib-risikolebensversicherung-r21
[R22]: #delib-risikolebensversicherung-r22
[R23]: #delib-risikolebensversicherung-r23
[R3]: #delib-risikolebensversicherung-r3
[R4]: #delib-risikolebensversicherung-r4
[R5]: #delib-risikolebensversicherung-r5
[R6]: #delib-risikolebensversicherung-r6
[R7]: #delib-risikolebensversicherung-r7
[R8]: #delib-risikolebensversicherung-r8
[R9]: #delib-risikolebensversicherung-r9
[std]: #delib-std
<!-- END generated citation links -->
