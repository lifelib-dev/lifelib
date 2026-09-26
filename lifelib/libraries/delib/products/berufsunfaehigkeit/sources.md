# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/berufsunfaehigkeit.md` (the citation
ground truth for this product) and are **frozen — never renumber**. Unused sources are omitted,
so the numbering has gaps. **S7** (Swiss Life AG, Niederlassung für Deutschland), **S10**
(Barmenia Lebensversicherung a. G.) and **S11** (Dialog Lebensversicherungs-AG) are named in the
research file as carriers whose wordings would settle the *Verweisung* clauses, the standalone
form and a pure-biometric *Überschussbeteiligung*, but **nothing from any of them is asserted**
in `product-spec.md` or `technical-notes.md` — those market positions are made generically from
[S12] — so citing them would attribute a claim to a document that supports no statement here.
**R26** (Deutsche Rentenversicherung Bund, *Rentenversicherung in Zahlen*) is absent for the
same reason: the statutory *Erwerbsminderungsrente* enters only through the statute [R24] [R25],
and no DRV statistic is printed anywhere, because none could be re-established and the house
rule forbids reproducing a recalled figure under a source tag. Original access date for all
sources: **2026-08-29**; the retrieval pass recorded on the entries below ran on **2026-08-30**.
No sources were newly added at drafting. Cross-product [REG-R#] tags are listed
in their own section at the end.

**Retrieval conditions — read this before relying on a single entry below.** They are not the
conditions this file was written under, and the difference is the whole of what changed.

1. **This file was drafted with nothing retrieved.** Direct HTTP egress from the build environment was blocked by an organisation network policy: `WebFetch` and `curl` were refused with HTTP 403 at the egress gateway for every host outside a short package-registry allowlist, and every host that matters here was tried and refused — `gesetze-im-internet.de` (VVG, VAG, SGB VI, EStG, DeckRV, MindZV, IfSG), `bafin.de`, `gdv.de`, `aktuar.de`, `deutsche-rentenversicherung.de`, `bundesfinanzministerium.de`, `destatis.de`, `dejure.org`, `buzer.de` and `bundesgerichtshof.de`. **There was no search channel either**: the session's `WebSearch` budget — 200 calls, shared across the delib build — was exhausted before this product was researched, and every search attempted for `berufsunfaehigkeit` returned the budget-exhausted message. So the first draft of every entry below rested on the authoring model's own knowledge of German insurance law and market practice, with no fetch, no search and no snippet behind it, disciplined by **[std]** and `[unverified]` tags rather than by a document. That is how this library was built, and it stays on the record.
2. **That policy has since been lifted and the citations were re-verified against the primary documents.** On **2026-08-30** the statutes and statutory instruments this product turns on were read as the canonical XML gesetze-im-internet publishes for each law, each law's amendment status (*Stand*) recorded on its entry and the sections it is cited for read in that XML; the GDV *Musterbedingungen* for the SBU, the BUZ and the BU-with-AU variant, four carrier *Bedingungswerke*, a carrier product summary, a carrier tax leaflet and a broker sheet were retrieved as PDFs and read. The same pass across the whole library read all fifteen German instruments delib cites as canonical XML and checked 950 statutory section references, of which 950 were correct; **501 of delib's 805 source entries — 62 % — now say `Retrieved: yes`**.
3. **Where this file ends the pass.** Of the **43** entries below, **26 say `Retrieved: yes`** — twenty-five outright, and [S12] for the three carrier documents it opened out of the eighteen carriers it names — and **17 still say `no`**, which is 60 % of this product's entries retrieved. The seventeen name what happened, and **not one of them is a paywall or a subscription login**. **Two are documents that are not published at all**: the DAV 1997 I / RI / TI family [R16] and DAV 2008 T [R17] — the one gap no network policy can close, and the reason every biometric level here is **[std]**. **Three are carrier sites that answered with a document-free body**: an index or product page that returns 200 and serves no *Bedingungswerk* — Allianz [S3], LV 1871 [S5] and HDI [S8]. **Two are document classes with no public specimen**: a *Produktinformationsblatt* is generated per quotation and none was found on any publisher's site [S13], and a standalone SBU carries no *Basisinformationsblatt* at all, so there is nothing to retrieve [S14]. **Three are documents for which no address could be established** — a BU-specific DAV *Ergebnisbericht* (R18), Franke und Bornberg's *BU-Leistungspraxis* (R21), and a BU-specific GDV series, the general publication being reachable and carrying none (R20). **Six were not attempted**, being secondary material that settles no modelled parameter: comparison portals and rating agencies [S15], the Verbraucherzentrale [S16], BaFin material (R19), Morgen & Morgen (R22), ASSEKURATA (R23) and the *Basisrente* BMF-Schreiben (R28). **One is case law read only at second hand** [R29]: no judgment text was opened, though two of its four propositions are recited in conditions that were.

What follows governs every entry below:

- **A `Retrieved: yes` entry is a certificate; a `Retrieved: no` entry is still a pointer.** Where the line says yes, the document was opened and the passage the entry rests on was read, and the edition, *Stand*, page count, document mark or quoted wording on the entry comes from the document itself. Where it says no, the entry remains a **known reference** — a document that exists and is the right kind of document — naming the instrument a claim should be checked against without asserting that anyone checked it; its address is either a canonical form carried as `[unverified]` or `URL: not established`, and **no edition, document number, *Bundesgesetzblatt* citation, page count or publication date has been invented for it**.
- **The re-verification changed things, and the changes are on the entries themselves.** The six months belongs to the *Sechs-Monats-Fiktion* and not to the *Prognosezeitraum*, which the GDV model conditions leave blank and one carrier sets at three years [S1] [S12]; § 177 VVG extends §§ 173–176 only to cover of a *dauerhafte* impairment of working capacity and expressly not to accident or health contracts [R6]; § 161 VVG's three-year suicide window is a **death-cover** rule the market's AVB do not apply to self-inflicted impairment at all [R11]; the drafted claim that no German insurer discloses its BU costs was wrong, VVG-InfoV § 2 requiring the disclosure in euro [R12]; and one carrier's conditions grant a surplus-financed *Schlusszahlung* where this library had recorded no maturity benefit anywhere [S12]. Read a claim as sound where its entry says yes and as provisional where it does not.
- **Quotation is now the normal case where an entry says yes.** The drafted file quoted nothing, because nothing had been read; the statutory and contractual wording quoted below is transcribed from the documents themselves. **Nothing is quoted on the authority of an entry that says `Retrieved: no`** — where such an entry carries wording, the wording comes from a document that *was* retrieved and the entry names it — and what those entries assert on their own account is still paraphrase of recollection.
- **`[unverified]` is used generously** in the product documents: every paragraph number, effective date, amount, percentage, table name and market figure carries it unless it is a structural fact not in dispute or a passage this pass actually read. Where a retrieved document removed a tag, the entry that removed it says so.
- **Uncertain levels became `[std]` parameters rather than citations.** Every biometric level, every charge level and the premium itself is **[std]**, each listed with its rationale in `model.md`. A `[std]` number is honest about being a construction; a fabricated `[S4]` number is not, and there are none.

---

## Primary product sources

(delib-berufsunfaehigkeit-s1)=

### S1 — GDV, *Allgemeine Bedingungen für die Berufsunfähigkeits-Versicherung* (unverbindliche Musterbedingungen)
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin; *unverbindliche Musterbedingungen* — non-binding model conditions most German insurers use as the drafting skeleton for their own AVB. Non-binding precisely because binding recommended conditions would be a cartel, so each insurer's own AVB is the operative document. The document's own first line says so: "Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ."
- URL: `https://www.gdv.de/resource/blob/6326/f89f31db43116561321679a5a3b29682/01-allgemeine-bedingungen-fur-die-berufsunfahigkeits-versicherung-0-pdf-data.pdf`, linked from the GDV's own *Musterbedingungen* index at `https://www.gdv.de/gdv/service/musterbedingungen`
- Retrieved: **yes** (PDF, 25 pp., *Stand: 21.07.2025*, read 2026-08-30). §§ 1, 2, 3, 5, 7–10, 15, 16 and 19 were read in full.
- Used for: **the most-cited document in this product**, and now the one whose clause text is on the record. What it establishes:
  - **The definition is a template with the numbers left blank.** § 2 Abs. 1 reads "infolge Krankheit, Körperverletzung oder mehr als altersentsprechenden Kräfteverfalls, die ärztlich nachzuweisen sind, voraussichtlich auf Dauer [und/oder: mindestens ...6 Monate/Jahre7] ihren zuletzt ausgeübten Beruf, so wie er ohne gesundheitliche Beeinträchtigung ausgestaltet war, nicht mehr zu mindestens …%8 ausüben kann" — both the *Prognosezeitraum* and the percentage are footnoted "Unternehmensindividuell zu ergänzen". **So the 50 % threshold and the prognosis period are conventions of each carrier's AVB, not of the model conditions and not of statute**; the model conditions add only the constraint that the period must respect "dem gesetzlichen Tatbestandsmerkmal der Dauerhaftigkeit (§ 172 Abs. 2 VVG)". Carrier levels are established at [S12] (Debeka) and [S9].
  - **The *Fiktion* is a separate limb with its own blank.** § 2 Abs. 2: a stated number of months of actual continuous inability to the stated degree, after which "gilt die Fortdauer dieses Zustandes als Berufsunfähigkeit". A 2. Bemerkung records that paying **retroactively from an earlier date than the *Fiktion*'s own effect requires an express variation** — retroactivity to onset is a carrier choice, not the model default.
  - **Waiver of the *abstrakte Verweisung* is the base text**; the abstract-referral wording is offered only as an alternative in a numbered "1. Bemerkung", which matches § 172 Abs. 3 VVG permitting but not implying it. *Lebensstellung* is defined in the base text — "nur eine Tätigkeit, die in ihrer Vergütung und sozialen Wertschätzung nicht spürbar unter das Niveau der bislang ausgeübten Tätigkeit absinkt" — with a footnote recording the case law's ~20 % pay-reduction tolerance and another inviting an *Umorganisation* clause for the self-employed.
  - **Core cover**: § 1 Abs. 1 pays the agreed *BU-Rente* and grants the *Beitragsbefreiung*, both to the *Leistungsdauer*; § 1 Abs. 7 "Die Rente zahlen wir monatlich im Voraus."; § 1 Abs. 3 "Der Anspruch auf Beitragsbefreiung und Rentenzahlung entsteht mit Ablauf des Monats, in dem die Berufsunfähigkeit eingetreten ist."; § 1 Abs. 5 requires premiums to be paid in full until the decision and refunded on acknowledgement; § 1 Abs. 4 ends the claim on recovery, death or expiry of the *Leistungsdauer*.
  - **Claim machinery**: § 8 Abs. 2 confines the *befristetes Anerkenntnis* to one grant on a stated *sachlicher Grund*; § 9 Abs. 4 gives the run-off — "Unsere Leistungen können wir mit Ablauf des dritten Monats nach Zugang unserer Erklärung bei Ihnen einstellen. **Ab diesem Zeitpunkt müssen Sie auch die Beiträge wieder zahlen.**" The second sentence is new to this library: the run-off and the resumption of premium are the same date.
  - **Exclusions** (§ 5): criminal acts, internal unrest on the side of the instigators, war and NBC risks with a passive-bystander carve-out, and — decisive for [R11] — "absichtliche Herbeiführung von Krankheit, absichtliche Herbeiführung mehr als altersentsprechenden Kräfteverfalls, absichtliche Selbstverletzung oder versuchte Selbsttötung", **with no time window at all**.
  - **Cost verrechnung** (§ 16 Abs. 2): "Der auf diese Weise zu tilgende Betrag ist nach der Deckungsrückstellungsverordnung auf 2,5 % der von Ihnen während der Laufzeit des Vertrages zu zahlenden Beiträge beschränkt." That is the DeckRV [R13] 25 ‰ ceiling in its operative contractual form.
  - **Cash values** (§ 15): the paid-up right, the *Rückkaufswert* "entsprechend § 169 des Versicherungsvertragsgesetzes (VVG)" below the stated minimum benefit, an *Abzug* on both, and no lapse while the *BU-Rente* is in payment.
  - What is **not** in the model conditions and therefore cannot be attributed to them: any *Karenzzeit* menu, any *Nachversicherungsgarantie* event list, any *Leistungsdynamik*, any *Wiedereingliederungshilfe*, any *Berufsgruppen*. The model conditions carry a *Berufsunfähigkeit infolge Pflegebedürftigkeit* limb graded by *Pflegestufe*, which this product does not model.

(delib-berufsunfaehigkeit-s2)=

### S2 — GDV, *Allgemeine Bedingungen für die Berufsunfähigkeits-Zusatzversicherung* (Muster-BUZ)
- Publisher / doc type: GDV; *unverbindliche Musterbedingungen* for the rider form.
- URL: `https://www.gdv.de/resource/blob/6328/f54c89730c9ba9043d8e8f023f38824a/02-allgemeine-bedingungen-fuer-die-berufsunfaehigkeits-zusatzversicherung-0-pdf-data.pdf`
- Retrieved: **yes** (PDF, 15 pp., *Stand: 15.11.2022*, read 2026-08-30). §§ 1, 2 and 9 read in full.
- Used for: the BUZ as a **wrapper variant of the same liability** — § 2 carries the same definition, § 5 the same *Anerkenntnis*, § 6 the same *Nachprüfung* — and for the two substantive differences, both now on the record. First, the waiver is of the **host** premium: § 1 Abs. 1 a) "Wir befreien Sie von der Beitragszahlungspflicht für die Hauptversicherung und die eingeschlossenen Zusatzversicherungen", and the *BU-Rente* itself is optional ("wenn diese mitversichert ist"), the reverse of the standalone form. Second, § 9 Abs. 1: "Die Berufsunfähigkeits-Zusatzversicherung bildet mit der Versicherung, zu der sie abgeschlossen worden ist (Hauptversicherung), eine Einheit; sie kann ohne die Hauptversicherung nicht fortgesetzt werden." A *Rückkaufswert* from the rider is payable only if the rider is surrendered together with the host. This bounds this product against delib products 2 and 5, which may carry the rider.

(delib-berufsunfaehigkeit-s3)=

### S3 — Allianz Lebensversicherungs-AG, AVB for the *selbständige Berufsunfähigkeitsversicherung*, with its *Produktinformationsblatt*
- Publisher / doc type: Allianz Lebensversicherungs-AG, Stuttgart — the largest German life insurer; AVB (*Bedingungswerk*) plus *Produktinformationsblatt*.
- URL: not established. The BU product page `https://www.allianz.de/vorsorge/berufsunfaehigkeitsversicherung/` returns 200 and points to a document index at `https://www.allianz.de/service/dokumente/#berufsunfaehigkeits-versicherung`; that index returned 200 on 2026-08-30 with no BU document in the served HTML — its per-product sections are assembled client-side.
- Retrieved: **no** — the publisher's own document index serves no BU *Bedingungswerk* in its HTML response; entry kept as a known reference.
- Used for: the most widely read BU wording in the market, cited for the market-standard shape it is expected to carry — the 50 % definition, waiver of the *abstrakte Verweisung*, a *Nachversicherungsgarantie* event list, a *Beitragsdynamik* option, occupational classification and the *Brutto* / *Zahlbeitrag* pair. **No product name, tariff code, edition date or parameter is asserted from it anywhere.** Every one of those shapes is now separately established from carrier documents that were retrieved — [S4], [S6], [S9], [S12] — so nothing in the product documents depends on this entry.

(delib-berufsunfaehigkeit-s4)=

### S4 — Alte Leipziger Lebensversicherung a. G., AVB and *Tarifbestimmungen* for its BU range
- Publisher / doc type: Alte Leipziger Lebensversicherung a. G., Oberursel; AVB and broker-channel product sheets.
- URL: AVB `https://www.alte-leipziger.de/-/media/druckstuecke/allgemeine-bedingungen/pm/2300/bedingungenallgemeinebedingungenberufsunfaehigkeitsversicherungpm2300pdf/bedingungen-allgemeine-bedingungen-berufsunfaehigkeitsversicherung-pm2300.pdf`; AU sheet `https://www.alte-leipziger.de/-/media/druckstuecke/infoblatt/pv/483/infoblatthighlightsauklauselpv483pdf/infoblatt-highlights-au-klausel-pv483.pdf`
- Retrieved: **yes** — AVB (PDF, 33 pp., document mark *pm 2300*, read 2026-08-30) and the AU-clause sheet (PDF, 2 pp., *pv 483.02-12.2025*, read 2026-08-30).
- Used for: **the entry that changes most in this pass.** It was the record of what could not be settled; three of its four items are now settled from the retrieved text, and the *Berufsgruppen* count is the one that is not.
  - ***Nachversicherungsgarantie*, event list and caps.** § 25 gives the full event list — marriage, birth or adoption, return from *Elternzeit*, divorce, majority, first degree course, first apprenticeship, completion of an academic qualification, *Meisterprüfung*, *Prokura*, becoming self-employed, exemption from compulsory pension insurance as a self-employed craftsman, ceasing to be a compulsory member of a *Versorgungswerk*, loss of occupational BU entitlement, purchase of a property costing at least 50 000 EUR or a loan of that size. The caps are stated: **at most 6 000 EUR of annual *BU-Rente* per event**, exercisable within twelve months of the event and only while the insured is not older than 50; three income-based events (crossing the *Beitragsbemessungsgrenze*, a sustained income rise of at least 10 %, a sustained profit rise of at least 30 %) allow **12 000 EUR** in one step; the **aggregate is 18 000 EUR**, or **30 000 EUR** including the separate *Berufseinsteiger* guarantee of up to 18 000 EUR for insureds not older than 35.
  - ***Karenzzeit*, and exactly what it defers.** § 2 Abs. 4: agreeing one lowers the premium and the *BU-Rente* is then first paid from the start of the month after the *Karenzzeit* ends, conditional on continuous BU throughout it and at its end — and "**Die Karenzzeit gilt nur für die Rente.**" The *Beitragsbefreiung* and the other benefits start from the month after BU begins. A *Karenzzeit* already served is credited if the insured becomes BU again within 24 months from the same cause, and it cannot be combined with a guaranteed *Rentensteigerung*. **The menu of available durations is in the *Tarifbestimmungen*, which were not retrieved**, so the model's 0 / 3 / 6 / 12 / 18 / 24 menu remains **[std]**.
  - **The *AU-Klausel*, fully parameterised.** The AU sheet settles all three parameters this library recorded as unestablished: the qualifying period is "6-monatige ununterbrochene Krankschreibung" or "4-monatige ununterbrochene Krankschreibung und Bescheinigung eines Facharztes, dass die Krankschreibung voraussichtlich weitere 2 Monate fortbestehen wird"; the AU pension equals the agreed *BU-Rente* and is paid retroactively from the onset of AU; the cap is "**Für max. 24 Monate pro Vertragslaufzeit – auch bei mehrfacher Arbeitsunfähigkeit**"; and payments **are** set off — "Wird rückwirkend eine BU anerkannt, werden erbrachte AU-Leistungen mit den BU-Leistungen verrechnet (keine Doppelzahlung)." The clause is sold "gegen einen geringen Mehrbeitrag". See the note at [S8] on why the model's inception uplift of 1,00 has not been moved.
  - **Still unestablished from this source:** the *Berufsgruppen* count and the *Verlängerungsoption* window, both of which live in the *Tarifbestimmungen* rather than the AVB.

(delib-berufsunfaehigkeit-s5)=

### S5 — LV 1871 (Lebensversicherung von 1871 a. G. München), AVB and PIB for its BU range
- Publisher / doc type: Lebensversicherung von 1871 a. G. München; AVB and *Produktinformationsblatt*, broker channel.
- URL: not established. `https://www.lv1871.de/berufsunfaehigkeitsversicherung/` returns 200 on 2026-08-30 but serves no document link in its HTML; the *Bedingungen* are behind the broker portal.
- Retrieved: **no** — the product page returns a document-free body; entry kept as a known reference.
- Used for: the **tiered range on one risk basis** — tiers differing in the option set rather than in the core definition. That claim no longer rests on this unretrieved entry: it is established from [S12] (CosmosDirekt's *Basis* and *Premium* tiers, where the *Premium* tier adds a shortened *Prognosezeitraum*, retroactive acknowledgement and a *Sofortleistung*, on top of a *Basis* tier that already waives the *abstrakte Verweisung* and pays in full from 50 %) and from [S9] (four tariff codes SBU, SBUJ, SBU+, SBUJ+ under one set of conditions). It remains why the model implements one base tariff with switchable options rather than several tariffs.

(delib-berufsunfaehigkeit-s6)=

### S6 — NÜRNBERGER Lebensversicherung AG, AVB, *Tarifbestimmungen* and *Berufsgruppenverzeichnis*
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG, Nürnberg; AVB, *Tarifbestimmungen* and the *Berufsgruppenverzeichnis* — the occupational classification list mapping named occupations to rating classes.
- URL: AVB *Selbstständige BU (Komfort-Schutz)* `https://www.nuernberger.de/medien/4allportal/gn331072_p.pdf`; customer information `https://www.nuernberger.de/medien/4allportal/lv005_565_pf.pdf`
- Retrieved: **yes** for the AVB (PDF, 28 pp., document mark *GN331072_202607*, read 2026-08-30) and the *Kundeninformation* (PDF, 3 pp., *LV005_565_202607*). **The *Berufsgruppenverzeichnis* itself was not retrieved** — it is not published on the public site, and the AVB never uses the word *Berufsgruppe*.
- Used for: two things, only one of which this entry can now carry.
  - **The *Brutto* / *Zahlbeitrag* mechanism, in the AVB's own words.** This is the clearest statement of it anywhere in this library, and it belongs here rather than at [S13]: "Für beitragspflichtige Versicherungen werden zu Beginn eines jeden Versicherungsjahres laufende Überschussanteile in Prozent der Beitragssumme eines Jahres (ohne Risikozuschläge) zugewiesen. Diese laufenden Überschussanteile werden … mit den jeweiligen Beiträgen verrechnet (Abzug vom Beitrag). Die Verrechnung hat zur Folge, dass im jeweiligen Versicherungsjahr **nicht der volle Tarifbeitrag (Bruttobeitrag), sondern nur der entsprechend ermäßigte Nettobeitrag gezahlt werden muss**." The alternative surplus form offered is a *Bonusrente* measured as a percentage of the insured *BU-Rente* at the start of the claim. § 19 Abs. 2 repeats the 2,5 % Zillmer ceiling, and § 18 Abs. 2 ends "Einen Stornoabzug nehmen wir nicht vor."
  - **The costs disclosure**, § 19 Abs. 1: "Die Höhe der einkalkulierten Abschluss- und Vertriebskosten sowie der übrigen Kosten und der darin enthaltenen Verwaltungskosten können Sie dem **Produktinformationsblatt** entnehmen." See [S13] and [R12]: this is the sentence that disproves the library's former claim that no German insurer discloses BU costs.
  - **Occupation as the dominant rating factor** remains asserted, but **not from a retrieved document**: nothing in the retrieved AVB or *Kundeninformation* names a class, a class count or a factor. The model's **[std]** BG1–BG5 cut with its 1,00 and 3,00 anchors is therefore a construction with no source, and the four-to-six-class shape recorded in `product-spec.md` stays `[unverified]`.

(delib-berufsunfaehigkeit-s8)=

### S8 — HDI Lebensversicherung AG, AVB and PIB for its BU range
- Publisher / doc type: HDI Lebensversicherung AG, Köln (Talanx group); AVB and *Produktinformationsblatt* for a tiered broker-channel range.
- URL: not established. `https://www.hdi.de/versicherungen/einkommensschutz/berufsunfaehigkeitsversicherung/` returns 200 on 2026-08-30 and serves no document link; `https://www.hdi.de/berufsunfaehigkeitsversicherung` redirects to `/404/`.
- Retrieved: **no** — the publisher's own product page carries no document body; entry kept as a known reference.
- Used for: the ***AU-Klausel***. **The three parameters this entry recorded as unestablished are now established — but from [S4], not from HDI**, and a second reading is at [S12] (CosmosDirekt: "Bei einer durchgehenden Krankschreibung von mindestens 6 Monaten zahlen wir als Zusatzleistung die vereinbarte Rente") and a third at [S6] (NÜRNBERGER's *Arbeitsunfähigkeits-Schutz*, "bis zu 36 Monate lang"). The GDV model conditions for the AU variant leave all three blank as *unternehmensindividuell*, so the spread between 24 and 36 months of benefit is a genuine market spread and not an unresolved reading. **The model still ships the clause with an inception uplift of exactly 1,00**, because the uplift is a price, and no retrieved document prices the clause — [S4] says only "gegen einen geringen Mehrbeitrag". Moving it would be a model change and is not taken here.

(delib-berufsunfaehigkeit-s9)=

### S9 — VOLKSWOHL BUND Lebensversicherung a. G., AVB and *Tarifbestimmungen*
- Publisher / doc type: VOLKSWOHL BUND Lebensversicherung a. G., Dortmund; AVB, broker-channel BU specialist.
- URL: `https://druckstuecke.volkswohl-bund.de/api/products/1574/documents/Allgemeine_Bedingungen_für_die_Selbstständige_Berufsunfähigkeits-Versicherung.pdf`
- Retrieved: **yes** (PDF, 22 pp., document mark *BED.SBU.0126*, tariff codes SBU, SBUJ, SBU+, SBUJ+, read 2026-08-30).
- Used for: the practice of **printing a *Bruttobeitrag* and a *Zahlbeitrag* side by side in the quotation**, on which the whole two-premium-stream design of the model rests. **The AVB itself does not use either word** — the mechanism is stated in the AVB at [S6], and the quotation is not a public document, so the practice is still recorded as a market fact and no figure from any quotation is asserted. What this document does add is the **income-replacement ceiling that bounds the insurable *BU-Rente***: § 17 Abs. 10 caps the total BU, EU and *Grundfähigkeit* entitlement, including other private and occupational entitlements, at "nicht mehr als 60 % des regelmäßigen jährlichen Bruttoeinkommens", and at 25 % for *Beamte*; § 17 Abs. 9 sets a 50 EUR minimum monthly increase; and § 3 carries the *AU-Klausel* and § 19 a *Verlängerungsgarantie*. It also records that *Karenzzeit* does not apply to the *Beitragsbefreiung*, which agrees with [S4].

(delib-berufsunfaehigkeit-s12)=

### S12 — Further German BU carriers, *Bedingungswerke* and *Produktinformationsblätter* (document class)
- Publisher / doc type: R+V, Debeka, Continentale, Gothaer, Die Stuttgarter, Zurich Deutscher Herold, ERGO Vorsorge, AXA, Hannoversche, CosmosDirekt, Württembergische, Baloise, die Bayerische, universa, DEVK, SIGNAL IDUNA, Provinzial and HUK-COBURG — all real German life insurers writing BU; AVB, *Tarifbestimmungen*, PIBs and *Berufsgruppenverzeichnisse*.
- URL: two members of the class were retrieved. Debeka *ABBV 01/2026* at `https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/Berufsunfähigkeit/BLV19.pdf`, its BU tax leaflet at `.../3L103.pdf`; CosmosDirekt's accessible product summary at `https://www.cosmosdirekt.de/resource/blob/600382/da56c986990d31554c1e91c8d1b87b3f/BF_SBU_1025.pdf`. No URL is established for the other sixteen.
- Retrieved: **yes, in part** — Debeka ABBV (PDF, 12 pp., document mark *B LV 19 (01.01.2026)*, edition ABBV 01/2026, read 2026-08-30), Debeka *Steuermerkblatt* (PDF, 1 p., *3 L/103 (01.01.2026)*), CosmosDirekt *BF SBU (10.25)* (PDF, 3 pp.). **No** for the remaining named carriers.
- Used for: the **breadth of the market**, the channel split, and — now — the carrier-level readings the GDV model conditions leave blank:
  - **The 50 % / six-month convention, verbatim.** Debeka § 2 Abs. 1 requires inability "voraussichtlich auf Dauer (mindestens 3 Jahre) … zu einem Grad von mindestens 50 %", and § 2 Abs. 2 is the *Fiktion*: "Ist die versicherte Person **6 Monate** ununterbrochen … zu einem Grad von mindestens 50 % außerstande gewesen …, gilt die Fortdauer dieses Zustandes als Berufsunfähigkeit." **The six months is the *Fiktion* period and the *Prognosezeitraum* at this carrier is three years** — the two are different clauses, and this library previously ran them together. CosmosDirekt sells "volle Leistung ab 50 % Berufsunfähigkeit" in its base tier and a "Verkürzung des Prognosezeitraums" as a *Premium* feature, which is the same distinction seen from the pricing side.
  - **Waiver of the *abstrakte Verweisung* as the base wording** — Debeka § 2 Abs. 1: "Auf eine abstrakte Verweisung verzichten wir." — with the *Umorganisationspflicht* stated for the self-employed and for managing directors, and the *Lebensstellung* test capped at a 20 % income reduction ("sie beträgt jedoch maximal 20 %").
  - **The *Beitragsverrechnung*.** Debeka § 3 Abs. 6: "Für beitragspflichtige Versicherungen können Sie laufende Überschussanteile in Prozent des Tarifbeitrags erhalten. Die laufenden Überschussanteile werden mit dem Tarifbeitrag verrechnet." Read with [S6], that is the model's `beitragsverrechnung` in two carriers' own words.
  - **A benefit this library recorded as absent.** Debeka § 3 Abs. 6 also provides a *Schlusszahlung* at expiry of the *Versicherungsdauer* "in Prozent der bis dahin tatsächlich gezahlten Tarifbeiträge" **if no BU has occurred**, and *Zinsüberschussanteile* during the claim converted into a *Bonusrente*. See the correction recorded at `product-spec.md`: "no maturity benefit" is true of the model, and was not true of this carrier's conditions.
  - **Nothing quantitative is cited from the unretrieved members of the class** and no parameter is attributed to any of the sixteen carriers not read.

(delib-berufsunfaehigkeit-s13)=

### S13 — *Produktinformationsblatt* (PIB) for a *selbständige Berufsunfähigkeitsversicherung* (document class)
- Publisher / doc type: each insurer, for each tariff; the pre-contractual information sheet whose content for this product is prescribed by **§ 2 Abs. 1 in Verbindung mit Abs. 4 VVG-InfoV** [R12] — the article is no longer `[unverified]`.
- URL: not established. A PIB is generated per quotation for a named age, occupation, term and *BU-Rente*; no carrier in this pass published a specimen with figures at a public address.
- Retrieved: **no** — the document class is quotation-specific and no specimen was found on any publisher's site on 2026-08-30. Its *content*, however, is established from two documents that were retrieved.
- Used for: two disclosures, both now sourced from elsewhere rather than assumed.
  - The ***Brutto* / *Zahlbeitrag* disclosure**. The mechanism is quoted at [S6] and [S12]; **no *Brutto* / *Zahlbeitrag* pair of figures was obtained**, so the 0,70 ratio remains **[std]** and the recalled 0,50–0,80 range stays `[unverified]` — still the most consequential single gap in this product, but now a gap in *levels* only, not in the mechanism.
  - **The cost table.** [S6] § 19 Abs. 1 directs the reader to the PIB for "die Höhe der einkalkulierten Abschluss- und Vertriebskosten sowie der übrigen Kosten und der darin enthaltenen Verwaltungskosten", and VVG-InfoV § 2 Abs. 1 Nr. 1 with Abs. 2 requires those figures **in euro**. So the PIB for a German BU tariff **does** carry an acquisition- and administration-cost disclosure. The charge levels in this product are **[std]** because no PIB was obtained — **not** because the disclosure does not exist.

(delib-berufsunfaehigkeit-s14)=

### S14 — *Basisinformationsblatt* (PRIIP-KID) — and why a standalone SBU normally has none
- Publisher / doc type: each insurer, where the product is in scope; PRIIPs key information document under Regulation (EU) No 1286/2014 [REG-R32].
- URL: not established; none is expected, since the premise of the entry is that the document is not produced for this product.
- Retrieved: **no** — nothing to retrieve. The boundary itself is now sourced from the German transposition rather than recalled: VVG-InfoV § 2 Abs. 1 Nr. 9 confines the *Effektivkosten* figure to "Lebensversicherungsverträgen, die Versicherungsschutz für ein Risiko bieten, bei dem der Eintritt der Verpflichtung des Versicherers **gewiss** ist", and computes it as the PRIIPs *Gesamtkostenindikator*. A pure SBU fails that test, so it carries no *Effektivkosten* figure and no *Basisinformationsblatt*.
- Used for: a **negative finding of substance** — an SBU is documented by a PIB [S13] and not by a *Basisinformationsblatt*, the opposite of delib's savings products. The operative criterion is **the certainty of the insurer's obligation**, not, as this library previously put it, the presence of a yield to reduce. The consequence for the model is smaller than was recorded: the absence of an *Effektivkosten* figure does not mean the absence of a cost disclosure — see [S13].

(delib-berufsunfaehigkeit-s15)=

### S15 — Comparison portals, consumer press and rating agencies (document class)
- Publisher / doc type: Verivox, CHECK24, Finanztip, Stiftung Warentest / *Finanztest*, Handelsblatt, MORGEN & MORGEN, Franke und Bornberg, ASSEKURATA; comparison pages, consumer guides, product tests and ratings — **secondary throughout**.
- URL: not established; no address for a BU price table or rating from any of these publishers was pursued in this pass, the class being secondary and its figures unusable under the house rule against reproducing a recalled number.
- Retrieved: **no** — not attempted; the class is secondary and no product claim would move if it were read.
- Used for: the class where every published German BU **price point** and **wording-quality rating** lives. It carries the recalled 55–90 € monthly *Zahlbeitrag* band for an office occupation at age 30 for 1 500 € to 67, against which the worked example's 62,05 € instalment is sanity-checked — a plausibility check and **not** a calibration, every input to it being **[std]**. Every figure attributed to this class remains `[unverified]`, and remains so because nothing here was read.

(delib-berufsunfaehigkeit-s16)=

### S16 — Verbraucherzentrale material on the *Berufsunfähigkeitsversicherung*
- Publisher / doc type: the *Verbraucherzentralen* and the *Verbraucherzentrale Bundesverband* (vzbv); consumer-advice pages and brochures — **secondary**.
- URL: not established; not pursued in this pass.
- Retrieved: **no** — not attempted; secondary, and the behavioural claims it supports are not modelled parameters.
- Used for: the behavioural facts the assumptions must reflect — that the ***Bruttobeitrag* and not the *Zahlbeitrag* is the figure a buyer should compare**; that incomplete *Gesundheitsfragen* are the commonest reason a claim later fails; that cover cannot be replaced once health has changed, which is why the German BU *Stornoquote* is low; that *Karenzzeit* and a reduced *Endalter* are the two premium levers; and that *Beitragsfreistellung* beats lapse. The first of these is corroborated structurally by [S6] — the *Zahlbeitrag* is the *Bruttobeitrag* less a surplus share the insurer redeclares each year — but the consumer-facing statement itself is not retrieved.

---

## Regulatory and actuarial references (product research numbering)

Statutes and statutory instruments in this section were read as the **canonical XML** that
gesetze-im-internet publishes for each law, which carries the law's *Stand*. The
`gesetze-im-internet.de/<law>/__NNN.html` addresses printed below are the human-facing links and
are **not** what was read: those per-section pages answer 200 with a frameset of a few kilobytes
containing no statutory text at all. Where an entry says `Retrieved: yes (canonical XML …)` the
section text quoted was read in that XML on 2026-08-30.

(delib-berufsunfaehigkeit-r1)=

### R1 — VVG § 172, *Leistung des Versicherers* — the statutory definition of *Berufsunfähigkeit*
- Publisher / doc type: Bundesministerium der Justiz / Bundesamt für Justiz; statute, VVG 2008.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__172.html` (frameset shell); text read from `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: **yes** (canonical XML, *Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*).
- Used for: the anchor provision. Abs. 1 fixes liability for a BU "**nach Beginn der Versicherung eingetretene**". Abs. 2 is the definition and is short enough to give whole: "Berufsunfähig ist, wer seinen zuletzt ausgeübten Beruf, so wie er ohne gesundheitliche Beeinträchtigung ausgestaltet war, infolge Krankheit, Körperverletzung oder mehr als altersentsprechendem Kräfteverfall ganz oder teilweise voraussichtlich auf Dauer nicht mehr ausüben kann." Abs. 3 permits, and does not imply, the *abstrakte Verweisung*. The correction this entry has always carried is now demonstrated rather than asserted: **the statute names neither a percentage nor a period** — it says "ganz oder teilweise" and "voraussichtlich auf Dauer". Both the 50 % threshold and any *Prognosezeitraum* are AVB conventions, left blank in the GDV model conditions [S1] and filled differently by carriers [S12].

(delib-berufsunfaehigkeit-r2)=

### R2 — VVG § 173, *Anerkenntnis*
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__173.html` (frameset shell); read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R1).
- Used for: the duty to declare in *Textform* whether liability is acknowledged, and the once-only limit. The whole of Abs. 2: "Das Anerkenntnis darf nur einmal zeitlich begrenzt werden. Es ist bis zum Ablauf der Frist bindend." The effect that matters — that once given it binds and the insurer escapes only through § 174 [R3] — follows from that second sentence read with § 174, and is reproduced in the AVB at [S1] § 8 Abs. 2, which adds a requirement of a stated *sachlicher Grund*. It is also the citation behind the model carrying **no acknowledged state**, paying from onset.

(delib-berufsunfaehigkeit-r3)=

### R3 — VVG § 174, *Leistungsfreiheit* — the *Nachprüfung* and its notice period
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__174.html` (frameset shell); read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R1).
- Used for: **the most model-relevant provision in the statutory frame**, and the wording is exact. Abs. 1: the insurer becomes free of liability "nur, wenn er dem Versicherungsnehmer diese Veränderung in Textform dargelegt hat" — a **change** must be set out, not a fresh decision on the original claim. Abs. 2: "Der Versicherer wird frühestens mit dem Ablauf des dritten Monats nach Zugang der Erklärung nach Absatz 1 beim Versicherungsnehmer leistungsfrei." That is the model's three-slot run-off ledger, its `runoff_months = 3` and its `check_runoff_roll_fwd` identity, confirmed to the word. [S1] § 9 Abs. 4 adds a fact the statute does not: at the same date the policyholder must resume paying premiums. The *konkrete Verweisung* route that lets recovery and referral be one modelled rate is in the AVB ([S1] § 9 Abs. 1), not in § 174.

(delib-berufsunfaehigkeit-r4)=

### R4 — VVG § 175, *Abweichende Vereinbarungen*
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__175.html` (frameset shell); read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R1). The section is one sentence: "Von den §§ 173 und 174 kann nicht zum Nachteil des Versicherungsnehmers abgewichen werden."
- Used for: §§ 173 and 174 being *halbzwingend* — which is why the *Anerkenntnis* and *Nachprüfung* mechanics are recorded as **uniform across the market and not a competitive variable**, and why the run-off is modelled as a statutory floor some insurers improve on. Note the reach: § 175 protects **only** §§ 173 and 174. It says nothing about the definition in § 172, which is exactly why the definition *is* a competitive variable and the run-off is not.

(delib-berufsunfaehigkeit-r5)=

### R5 — VVG § 176, *Anzuwendende Vorschriften*
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__176.html` (frameset shell); read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R1).
- Used for: the cross-reference making an SBU a life contract in everything but its trigger. **The range it imports was the first verification task the research file named, and it is now settled**: "Die §§ 150 bis 170 sind auf die Berufsunfähigkeitsversicherung entsprechend anzuwenden, soweit die Besonderheiten dieser Versicherung nicht entgegenstehen." The recalled §§ 150–170 is correct; the `[unverified]` tag on it is removed. Two things follow that were not previously recorded. The import is **entsprechend** and **subject to a reservation** — "soweit die Besonderheiten dieser Versicherung nicht entgegenstehen" — so every statement about the *Überschussbeteiligung* [R10], the suicide window [R11], the *beitragsfreie BU-Rente* [R8] and the *Rückkaufswert* [R9] is an analogous application that the peculiarities of BU can displace, and § 169 in particular is drafted for risks whose occurrence is certain (see [R9]).

(delib-berufsunfaehigkeit-r6)=

### R6 — VVG § 177, *Ähnliche Versicherungsverträge*
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__177.html` (frameset shell); read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R1).
- Used for: the **outer boundary of the product** — and the retrieved text narrows the boundary this library recorded. Abs. 1: "Die §§ 173 bis 176 sind auf alle Versicherungsverträge, bei denen der Versicherer für eine **dauerhafte** Beeinträchtigung der Arbeitsfähigkeit eine Leistung verspricht, entsprechend anzuwenden." The extension therefore reaches *Grundfähigkeits-* and *Erwerbsunfähigkeitsversicherung*, which promise a benefit for a **permanent** impairment, and it names §§ 173 **to 176**, not the *Anerkenntnis* / *Nachprüfung* frame loosely. Abs. 2 excludes accident insurance and health-insurance contracts covering the risk of impaired working capacity. **A benefit for temporary *Arbeitsunfähigkeit* is not a benefit for a *dauerhafte* impairment**, so an *AU-Klausel* does not inherit these protections through § 177; it is protected because it sits inside a BU contract to which §§ 172 ff. apply directly. The corresponding sentence in `technical-notes.md` has been corrected.

(delib-berufsunfaehigkeit-r7)=

### R7 — VVG §§ 19–22, *Vorvertragliche Anzeigepflicht* and its consequences
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__19.html` (frameset shell); §§ 19, 20, 21 and 22 read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R1).
- Used for: the underwriting section, and every element of it is confirmed. § 19 Abs. 1 limits the duty to circumstances "nach denen der Versicherer in Textform gefragt hat"; Abs. 2 to 4 grade the remedies by fault — *Rücktritt*, *Kündigung* on one month's notice where neither intent nor gross negligence is present, and contract amendment where the insurer would have written on other terms; § 22 preserves *Anfechtung* for *arglistige Täuschung*. The limitation periods are in **§ 21 Abs. 3**, not § 19: "Die Rechte des Versicherers nach § 19 Abs. 2 bis 4 erlöschen nach Ablauf von fünf Jahren nach Vertragsschluss; dies gilt nicht für Versicherungsfälle, die vor Ablauf dieser Frist eingetreten sind. Hat der Versicherungsnehmer die Anzeigepflicht vorsätzlich oder arglistig verletzt, beläuft sich die Frist auf zehn Jahre." The recalled five/ten years is confirmed and its tag removed; note the carve-out for claims that arose inside the period. § 21 Abs. 1 adds a one-month deadline on the insurer once it learns of the breach. The *Risikovoranfrage* and the industry's HIS remain behavioural consequences with no statutory text behind them, and an *Anzeigepflichtverletzung* still sits **inside** the modelled *Anerkennungsquote* rather than beside it.

(delib-berufsunfaehigkeit-r8)=

### R8 — VVG § 165, *Prämienfreie Versicherung* (applied via § 176)
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` (frameset shell); read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R1).
- Used for: the right to a **beitragsfreie *BU-Rente***. Abs. 1 gives it "jederzeit für den Schluss der laufenden Versicherungsperiode … sofern die dafür vereinbarte Mindestversicherungsleistung erreicht wird", and directs that below that minimum the *Rückkaufswert* under § 169 is paid instead; Abs. 2 requires the paid-up benefit to be computed on the premium basis and stated in the contract for each policy year. [S1] § 15 and [S6] § 18 implement both limbs, [S6] setting the minimum at 100,00 EUR of monthly pension. The scope statement stands and is now corroborated by the conditions themselves: the model prices the paid-up option **not at all**, because it is the release of a reserve the model does not compute, and that reserve is small — [S1] § 15 Abs. 3 warns that "auch in den Folgejahren stehen daher wegen der benötigten Risikobeiträge gemessen an den gezahlten Beiträgen keine oder nur geringe Mittel für die Bildung einer beitragsfreien Berufsunfähigkeitsrente zur Verfügung".

(delib-berufsunfaehigkeit-r9)=

### R9 — VVG § 169, *Rückkaufswert* (applied via § 176)
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` (frameset shell); read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R1).
- Used for: the *Rückkaufswert*, the five-year spreading and the *Stornoabzug* — all three confirmed, with one qualification and one correction.
  - **Confirmed.** Abs. 3 requires at least "der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt". Abs. 5: "Der Versicherer ist zu einem Abzug … nur berechtigt, wenn er vereinbart, beziffert und angemessen ist. Die Vereinbarung eines Abzugs für noch nicht getilgte Abschluss- und Vertriebskosten ist unwirksam." Both `[unverified]` tags are removed. [S1] § 15 Abs. 2 and Abs. 5 reproduce the *Abzug* conditions; [S6] § 18 Abs. 2 declines to take one at all ("Einen Stornoabzug nehmen wir nicht vor").
  - **Qualification.** Abs. 1 confers the right only where the insurance covers "ein Risiko …, bei dem der Eintritt der Verpflichtung des Versicherers **gewiss** ist". That is not true of a pure SBU, so the right arrives only through the *entsprechende Anwendung* of § 176 [R5] and its reservation. It does arrive: [S1] § 15 Abs. 4 pays "den Rückkaufswert entsprechend § 169 des Versicherungsvertragsgesetzes (VVG)", and VVG-InfoV § 2 Abs. 1 Nr. 4 with Abs. 4 [R12] requires the *Rückkaufswerte* to be disclosed for a BU contract.
  - **Correction.** This entry used to argue that a level *Bruttobeitrag* against a steeply rising inception rate "builds a real reserve", and that this makes the product a better reserve demonstration than term life. **The retrieved conditions contradict the magnitude.** [S6] § 18 Abs. 2: "Die Bildung eines Kapitals ist kein Vertragszweck Ihrer Versicherung. Das sogenannte Deckungskapital einer Berufsunfähigkeitsversicherung erreicht bei bestimmten Vertragsgestaltungen nie einen positiven Wert. … Das Deckungskapital dient nur dazu, die Höhe des Bruttobeitrags möglichst konstant zu halten. Die für die Bildung des Deckungskapitals zur Verfügung stehenden Beitragsteile sind gemessen an den gezahlten Beiträgen während der gesamten Vertragslaufzeit sehr gering. Mit Ablauf der Versicherung ist das Deckungskapital deswegen stets wieder völlig aufgebraucht." The *purpose* the library attributed to the reserve — levelling the gross premium — is exactly right; the *size* is not. The reserve is small relative to premiums paid, may never be positive, and is exhausted by expiry. `product-spec.md` has been corrected accordingly. The structural zero of `claims(t, "LAPSE")` is unaffected: the model does not compute the reserve either way.

(delib-berufsunfaehigkeit-r10)=

### R10 — VVG § 153, *Überschussbeteiligung* (applied via § 176)
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` (frameset shell); read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R1).
- Used for: **the legal basis of the *Brutto* / *Zahlbeitrag* pair.** Abs. 1 gives the entitlement unless excluded, and only as a whole. Abs. 2 gives the method: "Der Versicherer hat die Beteiligung an dem Überschuss nach einem **verursachungsorientierten Verfahren** durchzuführen; andere vergleichbare angemessene Verteilungsgrundsätze können vereinbart werden." Abs. 3 requires *Bewertungsreserven* to be recomputed annually and half the attributed amount paid at termination. Both retrieved AVB repeat the phrase and the mechanism: [S6] applies the current surplus share as a deduction from the *Tarifbeitrag*, [S12] as *Überschussanteile in Prozent des Tarifbeitrags* "mit dem Tarifbeitrag verrechnet". This is the citation behind `beitragsverrechnung`, behind the `surplus_credit` column, and behind carrying **no surplus account and no declaration mechanic** — the surplus is applied immediately rather than accumulated, which is what both carriers do. For BU the *Bewertungsreserven* limb is close to inert: [S1] § 3 Abs. 5 records that before a claim "keine oder allenfalls geringfügige Beträge zur Verfügung stehen, um Kapital zu bilden", so none or almost none arise.

(delib-berufsunfaehigkeit-r11)=

### R11 — VVG § 161, *Selbsttötung* (applied via § 176)
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` (frameset shell); read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R1).
- Used for: **a correction.** § 161 Abs. 1 begins "Bei einer Versicherung für den **Todesfall** ist der Versicherer nicht zur Leistung verpflichtet, wenn die versicherte Person sich vor Ablauf von drei Jahren nach Abschluss des Versicherungsvertrags vorsätzlich selbst getötet hat", with an exception for acts committed in a state excluding free will, and Abs. 3 requires the *Rückkaufswert* to be paid anyway. The three-year window is confirmed — **for completed suicide under a death cover**. The section says nothing about a self-inflicted *impairment*, which is the case that matters here, and importing it through § 176 [R5] runs straight into that section's reservation. **The question this entry recorded as unresolved is now answered from the conditions instead**: [S1] § 5 c) excludes BU caused by "absichtliche Herbeiführung von Krankheit, absichtliche Herbeiführung mehr als altersentsprechenden Kräfteverfalls, absichtliche Selbstverletzung oder versuchte Selbsttötung" — **an outright exclusion with no time limit**. The market's AVB do not run a three-year window on deliberate self-harm; they exclude it. Exclusions remain absorbed into the calibration of the inception rate, not modelled separately.

(delib-berufsunfaehigkeit-r12)=

### R12 — VVG-Informationspflichtenverordnung (VVG-InfoV)
- Publisher / doc type: Bundesministerium der Justiz; statutory instrument prescribing pre-contractual information duties.
- URL: `https://www.gesetze-im-internet.de/vvg-infov/` (contents shell); text read from `https://www.gesetze-im-internet.de/vvg-infov/xml.zip`
- Retrieved: **yes** (canonical XML, *Stand: Zuletzt geändert durch Art. 13 G v. 26.5.2026 I Nr. 156*). § 2 read in full.
- Used for: the mandate behind the PIB [S13] — the article is **§ 2, whose heading is "Informationspflichten bei der Lebensversicherung, der Berufsunfähigkeitsversicherung und der Unfallversicherung mit Prämienrückgewähr", with Abs. 4 applying Absätze 1 and 2 to BU *entsprechend*.** The `[unverified]` on the article is removed. Three findings, one of which reverses a claim this library made repeatedly.
  - **German BU insurers are required to disclose their costs, in euro.** § 2 Abs. 1 Nr. 1: "Angaben zur Höhe der in die Prämie einkalkulierten Kosten; dabei sind die einkalkulierten Abschlusskosten als einheitlicher Gesamtbetrag und die übrigen einkalkulierten Kosten als Anteil der Jahresprämie unter Angabe der jeweiligen Laufzeit auszuweisen; bei den übrigen einkalkulierten Kosten sind die einkalkulierten Verwaltungskosten zusätzlich gesondert als Anteil der Jahresprämie unter Angabe der jeweiligen Laufzeit auszuweisen" — with Abs. 2 requiring those figures in euro, and Abs. 4 extending the whole of Abs. 1 and 2 to BU. [S6] § 19 Abs. 1 points the customer to the *Produktinformationsblatt* for exactly those three numbers. **The former statement that a pure risk contract discloses its costs only through the *Brutto* / *Zahlbeitrag* pair, and that no German insurer discloses BU acquisition and administration costs, is wrong and has been corrected throughout.** The charge levels in this product are **[std]** because no PIB was obtained, not because none exists.
  - **What a BU contract does not carry is the *Effektivkosten* figure**, and for a stated reason: § 2 Abs. 1 Nr. 9 confines it to contracts "bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist", and Abs. 6 computes it as the PRIIPs *Gesamtkostenindikator*. The criterion is the certainty of the obligation, not the presence of a yield.
  - **A disclosure duty specific to this product**, not previously recorded: Abs. 4 Satz 2 requires the insurer to point out that the contractual concept of *Berufsunfähigkeit* does not coincide with the social-law concepts of *Berufsunfähigkeit* or *Erwerbsminderung* [R24] [R25], nor with the *Krankentagegeld* concept.

(delib-berufsunfaehigkeit-r13)=

### R13 — Deckungsrückstellungsverordnung (DeckRV) — *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher / doc type: Bundesministerium der Finanzen; statutory instrument.
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/BJNR076700016.html`; §§ 2, 4, 5a and 6 read from `https://www.gesetze-im-internet.de/deckrv_2016/xml.zip`
- Retrieved: **yes** (canonical XML, *Stand: Zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250*; the consolidated HTML at the address above was also retrieved, 20 kB, and gives the *Vollzitat* "Deckungsrückstellungsverordnung vom 18. April 2016 (BGBl. I S. 767), die zuletzt durch Artikel 1 der Verordnung vom 19. Juli 2024 (BGBl. 2024 I Nr. 250) geändert worden ist").
- Used for: the two model parameters, both now sourced.
  - ***Höchstrechnungszins*.** § 2 Abs. 1 Satz 1: "Bei Versicherungsverträgen mit Zinsgarantie, die auf Euro oder die nationale Währungseinheit eines an der Europäischen Wirtschafts- und Währungsunion teilnehmenden Mitgliedstaates lauten, wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf **1 Prozent** festgesetzt." The 1,00 % used as `rechnungszins` inside the premium equivalence is confirmed and its tag removed. **The date is not**: the consolidated text carries no commencement date for the 1 % figure, and the only date the retrieved document supplies is that of the amending regulation, 19 July 2024. "For contracts written from 1 January 2025" therefore keeps its `[unverified]` — the figure is sourced, the effective date is not. § 2 Abs. 2 confirms the rate used at conclusion governs the whole term.
  - ***Höchstzillmersatz*.** § 4 Abs. 1, last sentence: "Der Zillmersatz darf **25 Promille der Summe aller Prämien** nicht überschreiten." Confirmed, tag removed; and § 4 Abs. 4 fixes the rate in use at conclusion for the whole term. Both retrieved AVB state the ceiling in the customer-facing form of 2,5 % of the premiums payable over the term ([S1] § 16 Abs. 2, [S6] § 19 Abs. 2). This remains the only sourced number in the charge structure, and it is now sourced twice over.

(delib-berufsunfaehigkeit-r14)=

### R14 — Mindestzuführungsverordnung (MindZV)
- Publisher / doc type: Bundesministerium der Finanzen; statutory instrument on the minimum allocation of surplus to policyholders.
- URL: `https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html`; §§ 4, 6, 7 and 8 read from `https://www.gesetze-im-internet.de/mindzv_2016/xml.zip`
- Retrieved: **yes** (canonical XML, *Stand: Zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688*).
- Used for: the **risk-result minimum allocation** that governs a BU book. § 7: "Die Mindestzuführung zur Rückstellung für Beitragsrückerstattung in Abhängigkeit vom Risikoergebnis für die überschussberechtigten Versicherungsverträge beträgt **90 Prozent** des auf überschussberechtigte Versicherungsverträge entfallenden Risikoergebnisses". The recalled 90 % is confirmed and its tag removed. Two neighbouring rates matter here and were not previously recorded: the *übriges Ergebnis*, which for a BU book is essentially the expense result, carries a minimum of **50 Prozent** (§ 8), and the *Kapitalanlageergebnis* 90 % of the attributable investment return less the *rechnungsmäßige Zinsen* (§ 6 Abs. 1). Since a BU book's surplus is overwhelmingly risk plus expense surplus, the 90 % / 50 % pair — not 90 % alone — is the quantitative link between claims experience and the *Zahlbeitrag* charged, and sits behind `beitragsverrechnung` as the reason the credit is large and is expected to persist. § 4 Abs. 1 defines the three results by reference to the *Versicherungsberichterstattungs-Verordnung* returns, which are not public at contract level.

(delib-berufsunfaehigkeit-r15)=

### R15 — VAG §§ 138, 139, 141 — *Gleichbehandlung*, *Überschussbeteiligung*, *Verantwortlicher Aktuar*
- Publisher / doc type: Bundesministerium der Justiz; statute — *Versicherungsaufsichtsgesetz*.
- URL: `https://www.gesetze-im-internet.de/vag_2016/`; §§ 138, 139 and 141 read from `https://www.gesetze-im-internet.de/vag_2016/xml.zip`
- Retrieved: **yes** (canonical XML, *Stand: Zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81*). The section numbers were `[unverified]`; all three are correct and the tag is removed.
- Used for: the supervisory frame, with one attribution corrected.
  - **§ 138** is headed "Prämienkalkulation in der Lebensversicherung; Gleichbehandlung". Abs. 1 requires premiums calculated on appropriate actuarial assumptions and high enough to meet all obligations. Abs. 2 is the *Gleichbehandlungsgrundsatz* entire: "Bei gleichen Voraussetzungen dürfen Prämien und Leistungen nur nach gleichen Grundsätzen bemessen werden." That is what **legitimises *Berufsgruppen***: the conditions are not equal, so the bases need not be.
  - **§ 139** is the supervisory counterpart of § 153 VVG — the *Rückstellung für Beitragsrückerstattung*, and the *Sicherungsbedarf* limit on *Bewertungsreserven*. **§ 141** Abs. 5 Nr. 1 makes the *Verantwortlicher Aktuar* responsible for compliance of the premiums and the *Deckungsrückstellung* with § 138 and § 341f HGB, and Nr. 4 for proposing the surplus participation — the mechanism [S1] § 3 Abs. 4 and [S12] § 3 Abs. 5 both describe.
  - **Unisex does not live here.** The rule that sex may not enter premiums or benefits for contracts written from **21 December 2012** is in the AGG, not the VAG: § 33 Abs. 5 AGG permits sex-differentiated premiums only "Bei Versicherungsverhältnissen, die vor dem 21. Dezember 2012 begründet werden", so contracts from that date on cannot use it. Read with § 19 Abs. 1 Nr. 2 AGG and *Test-Achats* [REG-R34]. The date is confirmed; the citation for it moves to [REG-R34]. `sex` remains a reporting attribute that must not price.

(delib-berufsunfaehigkeit-r16)=

### R16 — DAV 1997 I, DAV 1997 RI and DAV 1997 TI — the *Rechnungsgrundlagen* for BU
- Publisher / doc type: Deutsche Aktuarvereinigung e. V. (DAV), Köln; actuarial tables with their *Herleitung* report — *Invalidisierungs-*, *Reaktivierungs-* and *Sterbewahrscheinlichkeiten der Invaliden*. **Not public.**
- URL: not established; the tables are DAV property and are not published at a public address, so there is nothing to retrieve.
- Retrieved: **no** — not public. This is the one entry in the section whose status cannot change however good the network is.
- Used for: the three biometric bases the model proxies, and the statement that they are **DAV property, are not published and are not redistributed by delib**. It backs the shapes the **[std]** proxies must reproduce — a steeply rising inception curve, reactivation concentrated in the first one to two claim years and near zero after about five, and disabled-lives mortality materially above active and itself select on duration — and the record that the shipped reactivation proxy carries **no age-at-disablement dimension**, which the real table does. The table names themselves remain `[unverified]`: no retrieved document names them.

(delib-berufsunfaehigkeit-r17)=

### R17 — DAV 2008 T — active-lives mortality
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; first-order mortality table for contracts with death-benefit character, with its *Herleitung* report. **Not public.**
- URL: not established; not published at a public address.
- Retrieved: **no** — not public.
- Used for: the **active state's** mortality decrement — an active life leaves by becoming *berufsunfähig*, by lapsing or by dying, and the last uses a *Todesfall*-character table rather than a population table. Cited by name and **not shipped**; the model's active column is an anchored **[std]** Gompertz proxy. The name remains `[unverified]`.

(delib-berufsunfaehigkeit-r18)=

### R18 — DAV *Ergebnisberichte* and *Fachgrundsätze* on biometric bases and BU
- Publisher / doc type: Deutsche Aktuarvereinigung e. V., *Ausschuss Lebensversicherung* and its working parties; results reports and professional standards, freely downloadable from `aktuar.de`.
- URL: not established; no BU *Ergebnisbericht* was located on the association's site in this pass.
- Retrieved: **no** — no address for a BU-specific report was established; entry kept as a known reference.
- Used for: the record of the three things the model most lacks quantitatively — the shape of the German BU inception curve, its trend over time, and the second-order reactivation pattern — and for the unresolved question of whether a homologated successor to DAV 1997 I exists at all. One datum in the neighbourhood did arrive from elsewhere: [S6]'s *Kundeninformation* attributes to a 2018 DAV analysis the claim that roughly one working person in four becomes at least temporarily *berufsunfähig* during a working life. Nothing in this product is calculated from it and it is not reproduced as a modelled figure.

(delib-berufsunfaehigkeit-r19)=

### R19 — BaFin material on the *Berufsunfähigkeitsversicherung*
- Publisher / doc type: Bundesanstalt für Finanzdienstleistungsaufsicht; *Merkblätter*, *Rundschreiben*, *BaFinJournal* articles and the industry *Beschwerdestatistik*.
- URL: not established for any BU-specific item; not pursued in this pass, nothing in the product depending on it.
- Retrieved: **no** — not attempted.
- Used for: the supervisory frame — BaFin's *Wohlverhaltensaufsicht* over the *Leistungsprüfung*, the quality of *Nachprüfung* notices and the *Brutto* / *Zahlbeitrag* disclosure. **Nothing quantitative is cited from BaFin anywhere in this product.**

(delib-berufsunfaehigkeit-r20)=

### R20 — GDV statistics on the *Berufsunfähigkeitsversicherung*
- Publisher / doc type: GDV; *Statistisches Taschenbuch der Versicherungswirtschaft*, *Die deutsche Lebensversicherung in Zahlen*, and GDV press material on BU.
- URL: not established for a BU-specific series. `https://www.gdv.de/resource/blob/180978/…/die-deutsche-lebensversicherung-in-zahlen-2024-publikation-pdf-data.pdf` is retrievable and is the general series, but it was not read for this product and no figure is taken from it.
- Retrieved: **no** — the general publication is reachable; no BU-specific series was located or read, and no figure is asserted.
- Used for: the market-size framing of the product and the existence of an industry-wide *Anerkennungsquote*, one of the two references behind the **[std]** `accept_factor = 0,80`. Every specific figure of this kind is `[unverified]` and **none is printed**.

(delib-berufsunfaehigkeit-r21)=

### R21 — Franke und Bornberg, *BU-Leistungspraxis* and the *BU-Rating*
- Publisher / doc type: Franke und Bornberg GmbH, Hannover; recurring study of BU claims practice on data supplied and audited at participating insurers, plus clause-by-clause wording ratings.
- URL: not established for the *BU-Leistungspraxis* study; the publisher's blog is reachable but the study itself was not located at a public address in this pass.
- Retrieved: **no** — no address for the study was established; entry kept as a known reference.
- Used for: the ***Anerkennungsquote*** — its usual publisher, and the principal reference behind `accept_factor = 0,80` **[std]** — with the composition of declines, the burden of proof resting on the insured at the initial claim, and the market's ranking of *Verweisung*, *AU-Klausel* and *Nachversicherungsgarantie* wordings. The recalled 75–80 % level is `[unverified]` and stays so: no retrieved document states it.

(delib-berufsunfaehigkeit-r22)=

### R22 — Morgen & Morgen, *M&M Rating Berufsunfähigkeit* and the annual causes analysis
- Publisher / doc type: MORGEN & MORGEN GmbH, Hofheim am Taunus; annual rating of BU tariffs with an accompanying analysis of the **causes of BU**.
- URL: not established; not pursued in this pass.
- Retrieved: **no** — not attempted.
- Used for: the causes-of-BU distribution — psychiatric conditions the largest group, accidents a small minority — which is why the specification argues against an accident-only variant; and the rating of ***Zahlbeitrag* stability against the *Bruttobeitrag***, the market's own recognition that the gap is a risk to the buyer. Every percentage is `[unverified]` with no confirmed year, and remains so.

(delib-berufsunfaehigkeit-r23)=

### R23 — ASSEKURATA, market studies on *Überschussbeteiligung* and biometric products
- Publisher / doc type: ASSEKURATA Assekuranz Rating-Agentur GmbH, Köln; annual market studies of declared *Überschussbeteiligung*, and insurer ratings.
- URL: not established; not pursued in this pass.
- Retrieved: **no** — not attempted.
- Used for: the **stability of the *Beitragsverrechnung*** — which insurers have had to raise the *Zahlbeitrag* toward the *Bruttobeitrag*, and by how much. That history is the empirical content of the risk the *Bruttobeitrag* represents, it is **not established**, and its absence is the stated reason `beitragsverrechnung` is held constant in the base run. What the retrieved conditions do establish is that the risk is real and contractual: [S1] § 3 Abs. 7 warns that the surplus "kann auch Null Euro betragen", and both carriers redeclare the *Überschussanteilsätze* annually on the board's decision.

(delib-berufsunfaehigkeit-r24)=

### R24 — SGB VI § 43, *Rente wegen Erwerbsminderung*
- Publisher / doc type: Bundesministerium der Justiz; statute — *Sozialgesetzbuch, Sechstes Buch*.
- URL: `https://www.gesetze-im-internet.de/sgb_6/__43.html`; text read from `https://www.gesetze-im-internet.de/sgb_6/xml.zip`
- Retrieved: **yes** (canonical XML, *Stand: zuletzt geändert durch Art. 2a G v. 24.7.2026 I Nr. 228*).
- Used for: the statutory benefit the private contract sits on top of, now with its thresholds sourced. Two tiers, both measured against "die üblichen Bedingungen des **allgemeinen Arbeitsmarktes**" in hours a day rather than against the insured's own occupation: *teilweise erwerbsgemindert* are those unable "auf nicht absehbare Zeit … mindestens sechs Stunden täglich erwerbstätig zu sein" (Abs. 1 Satz 2), *voll erwerbsgemindert* those unable to manage "mindestens drei Stunden täglich" (Abs. 2 Satz 2). Abs. 3 adds that the state of the labour market is not to be taken into account. The *Wartezeit* conditions are confirmed and their tag removed: three years of compulsory contributions in the last five years before onset, plus the *allgemeine Wartezeit* (Abs. 1 Nr. 2 and 3, Abs. 2 Nr. 2 and 3), with the five-year window extended by the periods listed in Abs. 4. It carries the market-role argument and has **no consequence for the recursion**: the statutory pension is not offset against the *BU-Rente* in the standard German contract, and none of the retrieved AVB contains an offset clause.

(delib-berufsunfaehigkeit-r25)=

### R25 — SGB VI § 240 — the abolished statutory *Berufsunfähigkeitsrente*
- Publisher / doc type: as R24; statute.
- URL: `https://www.gesetze-im-internet.de/sgb_6/__240.html` (frameset shell); read from the canonical XML.
- Retrieved: **yes** (canonical XML, same *Stand* as R24).
- Used for: **why this product exists**, and the cohort date is now exact. Abs. 1: a *Rente wegen teilweiser Erwerbsminderung* is available to insured persons who are "1. **vor dem 2. Januar 1961 geboren** und 2. berufsunfähig sind". The `[unverified]` is removed. Abs. 2 shows how far the statutory concept was from the private one even for those cohorts: it measures earning capacity against "körperlich, geistig und seelisch gesunden Versicherten mit ähnlicher Ausbildung und gleichwertigen Kenntnissen und Fähigkeiten", not against the insured's own last occupation, and sets the threshold at six hours a day. For everyone born later the statutory scheme contains no occupational-disability pension at all, and the private SBU is its replacement.

(delib-berufsunfaehigkeit-r27)=

### R27 — EStG § 10 and § 22 — deductibility of the premium and taxation of the *BU-Rente*
- Publisher / doc type: Bundesministerium der Justiz; statute — *Einkommensteuergesetz*, with the *Einkommensteuer-Durchführungsverordnung*.
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` and `.../__22.html`; text read from `https://www.gesetze-im-internet.de/estg/xml.zip` and, for the *abgekürzte Leibrente* table, `https://www.gesetze-im-internet.de/estdv_1955/xml.zip`
- Retrieved: **yes** (EStG canonical XML; EStDV canonical XML, *Stand: zuletzt geändert durch Art. 2 V v. 19.12.2025 I Nr. 372*). Corroborated by a carrier's own tax leaflet, [S12] Debeka *3 L/103 (01.01.2026)*.
- Used for: the taxation section, with the articles now exact and the tags removed.
  - **Premium.** A standalone SBU premium is a *sonstige Vorsorgeaufwendung* under **§ 10 Abs. 1 Nr. 3a EStG**, which names "Beiträge zu Versicherungen gegen Arbeitslosigkeit, zu Erwerbs- und Berufsunfähigkeitsversicherungen, die nicht unter Nummer 2 Satz 1 Buchstabe b fallen". The ceiling is **§ 10 Abs. 4**: 2 800 Euro a year, 1 900 Euro for taxpayers whose health cover is wholly or partly paid for them. That the ceiling is in practice already exhausted is not an estimate but the statute's own rule — Abs. 4 Satz 4: "Übersteigen die Vorsorgeaufwendungen im Sinne des Absatzes 1 Nummer 3 die nach den Sätzen 1 bis 3 zu berücksichtigenden Vorsorgeaufwendungen, sind diese abzuziehen und ein Abzug von Vorsorgeaufwendungen im Sinne des Absatzes 1 Nummer 3a scheidet aus." Where health and long-term-care contributions alone exceed the cap, **the BU premium is not deductible at all**.
  - **Benefit.** The *BU-Rente* is an *abgekürzte Leibrente* taxed on its *Ertragsanteil*. § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb Satz 5 refers time-limited annuities to a *Rechtsverordnung*; that is **§ 55 Abs. 2 EStDV**, whose table is keyed to the "Beschränkung der Laufzeit der Rente auf … Jahre ab Beginn des Rentenbezugs" — **the remaining term, not the recipient's age**, exactly as this library recorded. Column 3 of that table adds the qualification: above a stated attained age the ordinary age-based table of § 22 applies instead. The carrier's leaflet says the same in one sentence: "Renten aus Berufsunfähigkeits-Versicherungen sind als zeitlich begrenzte Leibrenten mit dem Ertragsanteil aus § 55 Abs. 2 Einkommensteuer-Durchführungsverordnung zu versteuern. Die Höhe des Ertragsanteils richtet sich nach der voraussichtlichen Rentendauer."
  - **Taxation does not enter the model**: delib projects gross, pre-tax cash flows.

(delib-berufsunfaehigkeit-r28)=

### R28 — BMF-Schreiben on the *Basisrente* and the conditions for a BU component
- Publisher / doc type: Bundesministerium der Finanzen; administrative circular on the tax treatment of *Altersvorsorge* and *Basisrenten* contracts.
- URL: not established; `bundesfinanzministerium.de` was not searched for the current circular in this pass.
- Retrieved: **no** — not attempted; entry kept as a known reference. The **statutory** side of the boundary was retrieved and is stronger than the entry implied: § 10 Abs. 1 Nr. 2 Buchst. b EStG permits a *Basisrente* to include "die ergänzende Absicherung des Eintritts der Berufsunfähigkeit (Berufsunfähigkeitsrente)" alongside the old-age annuity (Doppelbuchst. aa), and Doppelbuchst. bb separately admits a **standalone** BU or *Erwerbsminderung* contract to the first layer where it pays only a lifelong monthly annuity for an insured event occurring "bis zur Vollendung des 67. Lebensjahres", with the rights non-transferable, non-assignable, non-pledgeable and non-commutable. The GDV publishes model conditions for exactly this form.
- Used for: the conditions a BU rider must satisfy inside a *Basisrente* — annuity form, no benefit beyond the host's deferment, and a BU premium share capped at 49 % `[unverified]`, which is an administrative rule and not in the statutory text retrieved. It bounds this product against delib's `basisrente` and explains why the standalone SBU remains the dominant retail form.

(delib-berufsunfaehigkeit-r29)=

### R29 — BGH case law on *Verweisung*, *Anerkenntnis* and *Nachprüfung*
- Publisher / doc type: Bundesgerichtshof, IV. Zivilsenat; judgments. **No docket number is given anywhere in this product**, because none could be confirmed and inventing one is barred.
- URL: not established; no judgment was retrieved and none is cited by number.
- Retrieved: **no** — no judgment text was read. Two of the four lines are, however, **recited in retrieved conditions**, which is a weaker but real corroboration and is recorded as such.
- Used for: four settled lines. The binding effect of the *Anerkenntnis* is now statutory rather than case law on the point that matters ([R2] § 173 Abs. 2). The *Nachprüfung* requiring a **demonstrated change** is likewise in the statute ([R3] § 174 Abs. 1), leaving the requirement of an intelligible *Einstellungsmitteilung* — and hence that a defective notice never starts the three-month clock — as the case-law element, still `[unverified]`. ***Lebensstellung*** as the limit on any *Verweisung* is recited in both retrieved model conditions and one carrier's AVB, with the tolerance quantified: [S1] footnotes "Die höchstrichterliche Rechtsprechung geht zur Zeit davon aus, dass im Regelfall eine Minderung der Vergütung in Höhe von bis zu 20 % noch zumutbar ist", and [S12] Debeka § 2 Abs. 3 fixes the reduction it will treat as reasonable "unter Berücksichtigung der durch höchstrichterliche und herrschende oberlandesgerichtliche Rechtsprechung festgelegten Größe … jedoch maximal 20 %". The self-employed insured's *Umorganisationspflicht* is likewise carried in [S12] § 2 Abs. 1 and invited by a footnote in [S1]. The first two lines remain why recovery and *konkrete Verweisung* are one rate.

(delib-berufsunfaehigkeit-r30)=

### R30 — Infektionsschutzgesetz (IfSG) — the basis of the *Infektionsklausel*
- Publisher / doc type: Bundesministerium der Justiz; statute.
- URL: `https://www.gesetze-im-internet.de/ifsg/`; § 31 read from `https://www.gesetze-im-internet.de/ifsg/xml.zip`
- Retrieved: **yes** (canonical XML, *Stand: Zuletzt geändert durch Art. 3 Abs. 1 G v. 4.3.2026 I Nr. 60*).
- Used for: the *Tätigkeitsverbot* that ends a medical professional's ability to earn without her being ill in the sense of § 172 VVG. The provision is **§ 31, "Berufliches Tätigkeitsverbot"**, and its first sentence is the whole basis: "Die zuständige Behörde kann Kranken, Krankheitsverdächtigen, Ansteckungsverdächtigen und Ausscheidern die Ausübung bestimmter beruflicher Tätigkeiten ganz oder teilweise untersagen." A person who is merely *ansteckungsverdächtig* or an *Ausscheider* is not *berufsunfähig* under § 172 Abs. 2, which is precisely the gap an *Infektionsklausel* fills by deeming the ban to be BU. The clause itself is in no retrieved AVB — neither the GDV model conditions nor the three carrier AVB read here contain one — so its wording remains `[unverified]`. It is **not modelled separately**: its effect is a higher inception rate in one occupational segment, which is already how *Berufsgruppen* enter.

(delib-berufsunfaehigkeit-r31)=

### R31 — Versicherungsteuergesetz (VersStG) § 4 — exemption of life and BU premiums
- Publisher / doc type: Bundesministerium der Justiz; statute.
- URL: `https://www.gesetze-im-internet.de/versstg/`; § 4 read from `https://www.gesetze-im-internet.de/versstg/xml.zip`. **The slug `versstg` is the correct one** and is now corroborated by retrieval; the differently-spelled form printed at R16 of `products/risikolebensversicherung/sources.md` is not this address and that entry has not been touched here.
- Retrieved: **yes** (canonical XML, *VersStG 2021, Neugefasst durch Bek. v. 27.4.2021 I 874*).
- Used for: the single statement that **the BU premium carries no premium tax**, unlike a German non-life premium — recorded so a modeller from a non-life background does not look for the tax line. The paragraph is **§ 4 Abs. 1 Nr. 5 Buchst. b**, which exempts the premium for "eine Versicherung, durch die Ansprüche auf Kapital-, Renten- oder sonstige Leistungen begründet werden … b) im Fall der Krankheit, der Pflegebedürftigkeit, der **Berufs-** oder der Erwerbsunfähigkeit oder der verminderten Erwerbsfähigkeit, sofern diese Ansprüche der Versorgung der natürlichen Person, bei der sich das versicherte Risiko realisiert (Risikoperson), oder der Versorgung von deren nahen Angehörigen … dienen". The paragraph and its scope condition are confirmed and their tags removed; a carrier states the same rule and the same condition in its tax leaflet ([S12] Debeka *3 L/103*). Abs. 2 adds that the exemption begins or lapses when the circumstances change.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen;
research provenance in `_research/regulatory-actuarial.md`). **That page was drafted under the
same blocked-egress conditions and has since been re-verified in its own pass**; its per-entry
`Retrieved` lines, not this file, say what was opened there, and it has not been touched here.
Where this pass read the instrument itself, the [R#] entry above records it and the [REG-R#] tag
inherits nothing further.
Entries cited by the *Berufsunfähigkeit* documents:

- **REG-R1 / REG-R2 / REG-R4** — Solvabilität II, the Delegated Regulation and the EIOPA risk-free curves: the valuation layer that consumes `liability_cf`, cited and never computed.
- **REG-R8 / REG-R9 / REG-R11** — VAG §§ 138, 139 and 141–143: premium sufficiency and *Gleichbehandlung*, the supervisory side of the *Überschussbeteiligung*, the *Verantwortlicher Aktuar*.
- **REG-R14 / REG-R15** — the DeckRV and the *Höchstrechnungszins* rate history: the 1,00 % the premium equivalence discounts at. DeckRV § 2 Abs. 1 was read for this pass and states the 1 Prozent figure [R13]; **the 1 January 2025 commencement is not in the consolidated text and stays `[unverified]`**.
- **REG-R16 / REG-R20** — DeckRV § 4 *Höchstzillmersätze* and the LVRG cut from 40 ‰ to 25 ‰: the ceiling `acq_rate` sits at, the rate in use at conclusion applying for the whole term.
- **REG-R18 / REG-R19 / REG-R24** — MindZV, RfBV and VVG § 153: the surplus machinery behind the *Beitragsverrechnung*. MindZV §§ 7 and 8 were read for this pass [R14]: the risk-result minimum is 90 %, the *übriges Ergebnis* minimum 50 %.
- **REG-R23** — VVG §§ 8 and 152, the 14-day and 30-day *Widerrufsrechte*: absorbed into the first-year lapse rate rather than modelled.
- **REG-R28** — VVG §§ 165–170: *prämienfreie Versicherung*, *Kündigung*, *Rückkaufswert* and the *Stornoabzug* — the article-level source for the cash values this model does not price.
- **REG-R29** — VVG §§ 172–177 as a whole: the cross-product carrier for [R1]–[R6], including the three-month run-off.
- **REG-R30** — VVG §§ 19, 37, 38, 157 and 158: the *Anzeigepflicht*, and the *qualifizierte Mahnung* whose two-week period the model does not carry, so lapse falls about a month early.
- **REG-R31 / REG-R33 / REG-R35** — the VVG-InfoV cost-disclosure regime, the IDD and BaFin's *Wohlverhaltensaufsicht*: why a pure risk product has no *Effektivkosten* figure — but does have a cost disclosure. VVG-InfoV § 2 was read for this pass [R12].
- **REG-R32** — PRIIPs: why a standalone SBU normally has **no** *Basisinformationsblatt*.
- **REG-R34** — *Test-Achats* and the AGG: unisex pricing from 21 December 2012. AGG § 33 Abs. 5 was read for this pass and confirms the date [R15]; this, not the VAG, is where the rule lives.
- **REG-R36** — the BGH line of authority on German life contracts, the carrier for [R29].
- **REG-R37** — the GDV *Musterbedingungen* and German BU market practice: that page's own entry on the 50 % / six-month convention and the *BU-Fiktion*. The model conditions themselves were read for this pass [S1] and leave both numbers blank; the six months belongs to the *Fiktion*, not to the *Prognosezeitraum* [S12].
- **REG-R38 / REG-R39 / REG-R41** — the AltEinkG *Drei-Schichten-Modell*, the *Basisrente* deduction, and the *Ertragsanteil* / *Besteuerungsanteil* rules: the tax section only.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the direction-of-prudence argument behind the four first-order loads.
- **REG-R48 / REG-R50** — DAV 2008 T and the DAV 1997 I / RI / TI family: the entries stating that the tables are not public and not redistributed, and that a BU model cannot leave disabled-lives mortality unspecified.
- **REG-R53** — the German life market in numbers: market scale, and the *Anerkennungsquote* and gross-versus-net-of-declinature point behind `accept_factor`.
- **REG-R54 / REG-R55** — HGB §§ 341–341o with the RechVersV, and IFRS 17: the accounting layers the same expected-cash-flow engine feeds.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation.

---

## Provenance note

Extraction details — which fact was recorded from which document class, the twenty-six sections
of extracted mechanics, and the eighteen-item gaps-and-caveats register — live in
`_research/berufsunfaehigkeit.md`, which is the citation ground truth for the S# and R# numbering
used here and records at its head the blocked-egress conditions the research itself was done under,
before any of it was re-verified.

The caveats that most affect what these product documents can claim, in order of how much they
constrain the model. **This register was rewritten on 2026-08-30 against the documents actually
retrieved**, and the retrieval-conditions statement at the head of this file has been rewritten to
match the per-entry `Retrieved` lines above rather than the conditions this file was drafted under.

1. **Primary evidence now exists, and it is contractual and statutory rather than quantitative.** Retrieved and read: the GDV model conditions for the SBU and the BUZ and for the BU-with-AU variant [S1] [S2] [S8]; carrier AVB from Alte Leipziger, NÜRNBERGER, VOLKSWOHL BUND and Debeka, plus CosmosDirekt's product summary and Debeka's BU tax leaflet [S4] [S6] [S9] [S12]; and the canonical text of VVG §§ 19–22, 153, 161, 165, 169 and 172–177, VVG-InfoV § 2, DeckRV §§ 2 and 4, MindZV §§ 4 and 6–8, VAG §§ 138, 139 and 141, AGG §§ 19, 20 and 33, SGB VI §§ 43 and 240, EStG §§ 10 and 22 with EStDV § 55, IfSG § 31 and VersStG § 4 [R1]–[R15], [R24], [R25], [R27], [R30], [R31]. **Not** retrieved: any price, any rate card, any occupational table, any DAV table, any rating-agency or consumer-press figure.
2. **No *Produktinformationsblatt* was obtained, so no *Brutto* / *Zahlbeitrag* pair of figures is sourced** [S13]. The 0,70 ratio is **[std]** and the recalled 0,50–0,80 range `[unverified]`. This remains the most consequential single gap: the ratio drives modelled premium income directly and moves it by more than 40 % across that range. What has changed is that the **mechanism** is no longer recalled — two carriers state it in their own AVB [S6] [S12], one of them in the exact terms *Tarifbeitrag (Bruttobeitrag)* against *ermäßigter Nettobeitrag*.
3. **No rate card of any kind was obtained** — no tariff table, no occupational factor set, no age curve [S15]. The *Bruttobeitrag* is therefore an **output** of a stated first-order basis rather than an observation, and the worked example is **internally consistent only**: unlike frlib's `temporaire_deces`, this model reproduces nothing external.
4. **The DAV 1997 family and DAV 2008 T are not public and were not seen** [R16] [R17]. This is the one gap the network cannot close. Their *shapes* are asserted from general actuarial knowledge; their *levels* are constructions anchored so the worked example reproduces exactly. The table **names** may themselves be wrong, and anyone citing one must confirm it first.
5. **Five insurer *Bedingungswerke* were opened, and the parameters they state are now attributed to them by name** [S4] [S6] [S9] [S12]: the *Nachversicherungsgarantie* event list with its 6 000 / 18 000 / 30 000 EUR caps, the *Karenzzeit*'s restriction to the pension alone, the AU clause's 6-month qualification / 24-month cap / set-off against BU, the 50 % degree with a six-month *Fiktion*, the 60 % income-replacement ceiling, and the *Beitragsverrechnung*. Three of the eighteen carriers named at [S12] were read; nothing is attributed to the other fifteen, and no **price** is attributed to any of them.
6. **Every charge level is [std] — but not because the disclosure does not exist.** VVG-InfoV § 2 Abs. 1 Nr. 1 with Abs. 2 and Abs. 4 requires a German BU insurer to state, in euro, the acquisition and distribution costs calculated into the premium as a single total and the other costs, administration costs shown separately, as a share of the annual premium; [S6] § 19 Abs. 1 directs the customer to the *Produktinformationsblatt* for precisely those figures. **The earlier statement that no German insurer discloses BU acquisition, administration or claims-handling costs was wrong.** The levels here are **[std]** because no PIB was obtained [S13]. The 25 ‰ *Höchstzillmersatz* [R13] is sourced twice over — the instrument and two AVB — and no longer carries a tag.
7. **The *AU-Klausel* is now fully described and still unpriced** [S4] [S8]. Its three parameters are established from a carrier's own broker sheet; what no retrieved document gives is the **loading**, so the clause still ships switched on with an inception uplift of exactly 1,00 rather than with an invented one. Moving it would be a model change and was not taken.
8. **The statutory paragraph numbers are no longer at risk** [R1]–[R6]. § 176 VVG imports "die §§ 150 bis 170" — confirmed — and § 173 Abs. 2 confines the *befristetes Anerkenntnis* to one grant, also confirmed. Two readings had to be corrected instead: § 177 extends §§ 173–176 only to cover of a ***dauerhafte*** impairment of working capacity and expressly not to accident or health contracts, and § 161's three-year window is a **death-cover** rule that the market's AVB do not apply to self-inflicted impairment at all [R11].
9. **The VVG, VAG, SGB VI, EStG, DeckRV, MindZV, IfSG, AGG, VVG-InfoV and VersStG are living texts.** Each [R#] entry above now records the *Stand* of the text that was read, and those *Stände* differ — the VVG was read as amended to 26 May 2026, the MindZV as amended to 7 July 2020. The *Höchstrechnungszins* changes by instrument and its commencement date is still `[unverified]` [R13]. Check every provision against the current consolidated text before relying on it. **A delib citation is a pointer to a document; the `Retrieved` line says whether this library opened it.**

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
[R2]: #delib-berufsunfaehigkeit-r2
[R24]: #delib-berufsunfaehigkeit-r24
[R25]: #delib-berufsunfaehigkeit-r25
[R27]: #delib-berufsunfaehigkeit-r27
[R29]: #delib-berufsunfaehigkeit-r29
[R3]: #delib-berufsunfaehigkeit-r3
[R30]: #delib-berufsunfaehigkeit-r30
[R31]: #delib-berufsunfaehigkeit-r31
[R5]: #delib-berufsunfaehigkeit-r5
[R6]: #delib-berufsunfaehigkeit-r6
[R8]: #delib-berufsunfaehigkeit-r8
[R9]: #delib-berufsunfaehigkeit-r9
[REG-R32]: #delib-reg-r32
[REG-R34]: #delib-reg-r34
[std]: #delib-std
<!-- END generated citation links -->
