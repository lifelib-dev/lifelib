# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/fondsgebundene_rentenversicherung.md`
(the citation ground truth for this product) and are **frozen — never renumber**. Unused ids
are normally omitted, leaving gaps; **this product has none.** All eighteen primary sources
S1–S18 and all twenty-six product-specific references R1–R26 are cited at least once by
`product-spec.md` or `technical-notes.md`, so the numbering below is unbroken. At drafting that
was a property of a small, deliberately-assembled corpus and no sign of thoroughness: nothing
had been dropped because nothing in the list was a document anyone had read, so no entry could
fail on inspection. The forty-four entries have since been put to exactly that test, and the
numbering still holds — none was withdrawn — but several are corrected below and two are now
known to have described this product wrongly [R8] [R9]. Access date at drafting: **2026-08-29**;
the re-verification pass read on **2026-08-30**, and every entry carries its own result. No
sources were newly added at drafting. Cross-product [REG-R#] tags are listed in their own
section at the end.

**Retrieval conditions — read this before relying on a single line below, because they changed
after this file was written.**

1. **delib was drafted with direct HTTP egress blocked by an organisation network policy.**
   `WebFetch` and `curl` were refused with HTTP 403 at the egress gateway for every host
   outside a short package-registry allowlist. `gesetze-im-internet.de`, `bafin.de`, `gdv.de`,
   `aktuar.de`, `bundesfinanzministerium.de`, `dejure.org`, `eur-lex.europa.eu`,
   `de.wikipedia.org` and every insurer host named below were tried in the course of building
   this library and every one was refused. **Not one *Bedingungswerk*, not one
   *Basisinformationsblatt*, not one *Produktinformationsblatt*, not one
   *Verbraucherinformation* was opened.**
2. **There was no search channel either.** The session's `WebSearch` budget — 200 calls, shared
   across the ten delib products — was already exhausted when this product's research began.
   Every search attempted for it returned the budget-exhausted response, so there was **no
   research channel of any kind** for this file: not even the weak one, search summaries, that
   the `kapitallebensversicherung` and `klassische_rentenversicherung` files had. The first
   draft therefore rested on the authoring model's own knowledge of German insurance law and
   practice, disciplined by the [std] and [unverified] tags, and the handful of facts
   corroborated at one remove came from searches run for **sibling** delib research files and
   are attributed to the sibling rather than claimed here.
3. **That policy has since been lifted, and these citations were re-verified against the primary
   documents on 2026-08-30.** Of the forty-four entries below, **eighteen — 41 % — now say
   `Retrieved: yes`**, **two say `partly`**, and **twenty-four say `no`**. What arrived is worth
   more than the ratio: one complete German unit-linked *Bedingungswerk* read end to end,
   DEVK's 195-page *Kundeninformation* 03101/07/2024 with its *Tarifbestimmungen*, its
   *Rechnungsgrundlagen* and sixteen *Basisinformationsblätter* [S2] [S15], which is the only
   clause text in this file; the statutory core as canonical XML from `gesetze-im-internet.de`
   with each instrument's amendment status (`Stand`) recorded — the VVG at [R1] to [R6], the
   DeckRV [R12], the MindZV [R14], the VAG [R15] and the EStG [R19] [R20], with the VVG-InfoV
   read as complete section text in HTML [R7]; and BaFin's *Merkblatt* 01/2023 [R10], its
   *Risiken im Fokus 2026* cost survey [R11], the DAV's PRIIPs *Ergebnisbericht* [R18] and the
   Finanztip *Rentenfaktor* material [R22], each read in full.
4. **What the twenty-four failures are**, because their shape matters more than the count.
   **Nineteen are addresses that were never established**: for ten named carriers no address for
   a fondsgebundene wording could be found on the publisher's own site [S4]–[S12] [S14], and the
   same is true of the GDV *Musterbedingungen* [S1] and *Muster-Standmitteilung* [S17], the
   *Nettotarif* wordings [S18], the PRIIPs Regulation and its RTS at EUR-Lex [R8], the LVRG
   [R13], the rating studies [R23], the consumer bodies and comparison portals beyond Finanztip
   [R24], the GDV new-business split [R25] and the BGH line on the *Rückkaufswert* [R26]. **Two
   are 404s**: the one HDI address tried answers 200 with the site's own 404 page [S13], and the
   BaFin *Fachartikel* is a hard 404 that BaFin's search index still lists [R9]. **Two are
   documents that are not public at all** — the DAV mortality tables [R16] [R17], which are
   Deutsche Aktuarvereinigung property, cited by name and never shipped. **One was opened only
   at its contents page**, so no section of it was read [R21]. No paywall and no consent wall is
   among them. The two `partly` entries name their own halves: Allianz's product page was read,
   but `goa-eportale.allianz.de` answers HTTP 403 to the *Bedingungswerk*, so no clause text
   comes from Allianz [S3]; and the *Verbraucherinformation* limb of [S16] arrived bound into
   [S2] while the *Produktinformationsblatt* limb was not located.

**So read the `Retrieved:` line before relying on the entry above it.** `Retrieved: yes` means
the document was opened and the passage the entry rests on was read; a German sentence quoted
in such an entry is quoted from the instrument. **Anything else leaves the entry a pointer, not
a certificate** — it names the instrument a claim should be checked against; it does not assert
that anyone checked it. No verbatim quotation is invented, and no URL, document number,
edition, tariff code, page count or publication date is guessed: where no address was
established the entry says `URL: not established`, and a canonical `gesetze-im-internet.de`
form that was never opened stays `[unverified]`. Re-verification was not a formality — it
contradicted the death table this library names [R17], reversed the PRIIPs category assignment
[R8] [R9], put a real guaranteed *Rentenfaktor* about 9 % below the one shipped [S15], and gave
the composite's charge stack a market comparator it had never had [R11]. Across delib as a
whole **501 of 805 entries — 62 % — are now `Retrieved: yes`**; this product sits below that,
and the carrier sweep rather than the statutory core is the reason.

**What is still almost entirely `[std]` is the levels.** Outside the one carrier that could be
read, not one *Abschlusskostenquote*, not one *Verwaltungskostensatz*, not one *Stückkosten*
amount, not one *Effektivkostenquote* and not one *Rentenfaktor* was established at any
carrier, and no German unit-linked *Stornoquote* was established anywhere. The **mechanics** in
the product documents are common ground in German practice, several of them now read in a real
wording, and are written without hedging.

---

## Primary product sources

(delib-fondsgebundene_rentenversicherung-s1)=

### S1 — GDV, *Musterbedingungen* for the fondsgebundene Rentenversicherung
- Publisher / doc type: Gesamtverband der Deutschen Versicherer e. V.; *Musterbedingungen* — non-binding model policy conditions from which member insurers derive their own *Allgemeine Versicherungsbedingungen*
- URL: not established
- Retrieved: **no** — no address for a GDV model-conditions set for the *fondsgebundene* form could be found on the publisher's own site on 2026-08-30; the entry is kept as a known reference. The **document type** is established indirectly: the sibling delib research on `klassische_rentenversicherung` corroborated the GDV *Musterbedingungen* index and a model-conditions set for the *Rentenversicherung mit aufgeschobener Rentenzahlung*; a companion set for the fondsgebundene form is the ordinary structure of that index, and its title, edition and clause numbering remain `[unverified]`
- Used for: the market-standard **clause inventory** the specification is organised around — that the insurer guarantees the number of *Anteileinheiten* and not their value; the *Beitragsverrechnung* order and the purchase of units at the *Anteilspreis* on a *Bewertungsstichtag*; the *Risikobeitrag* on the net amount at risk; the *garantierte Mindesttodesfallleistung* as one of the four death-benefit shapes; the *Beitragsdynamik* mechanic; and the structural interchangeability of German insurer wordings. **No clause text and no numeric parameter rests on it.** Its load is now much lighter than it was: every item in that inventory except the *garantierte Mindesttodesfallleistung* has since been read verbatim in a real carrier wording [S2], so [S1] stands for the *generality* of the pattern and no longer for its existence.

(delib-fondsgebundene_rentenversicherung-s2)=

### S2 — DEVK, "Kundeninformation zur Fondsgebundenen Rentenversicherung", document 03101, edition 07/2024
- Publisher / doc type: DEVK Deutsche Eisenbahn Versicherung Lebensversicherungsverein a. G. and DEVK Allgemeine Lebensversicherungs-AG, Riehler Straße 190, 50735 Köln; *Kundeninformation* — the consolidated pre-contractual document carrying the *Verbraucherinformationen*, the *Tarifbestimmungen*, the AVB, the tax notes, the glossary **and the product's own *Basisinformationsblätter*** in one file. Tariff **L/N FR1**, product name **"DEVK-Fondsrente vario"**
- URL: `https://www.devk.de/media/content/download/produkte/altersvorsorge/DEVK-Fondsrente-Kundeninfo-03101-2024-07.pdf`. The address recorded in the sibling delib research on `klassische_rentenversicherung` (`medien.devk.de/assets/content/download/produkte/altersvorsorge-leben/devk-fondsrente-kundeninfo-03101-2024-07.pdf`) answers **HTTP 403** from its object store; the file itself is served under the publisher's own `www.devk.de/media/...` path, and that is the address recorded here
- Retrieved: **yes** (PDF, 195 pp., document code 03101/07/2024, AVB *Stand* Januar 2024, *Tarifbestimmungen* *Stand* Juli 2023, *Basisinformationsblätter* *Stand* 01.01.2024 with *Erstellungsdatum* 03.11.2023; read 2026-08-30)
- Used for: **by a wide margin the most load-bearing document in this corpus — it is the one full German unit-linked *Bedingungswerk* the library has read, and most of what the specification asserts as "German market practice" is now checkable against it.** Specifically:
  - **the death benefit** — § 2 Abs. 7 AVB: *"Die Todesfallleistung ist das zum Stichtag bei Tod (siehe § 1 Absatz 5) vorhandene Fondsguthaben, mindestens aber die ➜ Summe der gezahlten Beiträge (Beitragsrückgewähr)."* That is `max(Fondsguthaben, Summe der gezahlten Beiträge)` exactly, and it is why `db_form = prem_return` is the composite and `cum_prem_pp` a state variable. The same clause adds a rule delib does **not** implement: *"Etwaige vorherige Kapitalentnahmen aus dem Fondsguthaben (siehe Absatz 9) vermindern die Beitragsrückgewähr entsprechend."*
  - **the *Rentenfaktor* rule** — § 2 Abs. 2: *"Der tatsächliche Rentenfaktor ist der höhere Wert aus dem zu Rentenbeginn ➜ aktuellen Rentenfaktor und dem zu Vertragsbeginn ➜ garantierten Rentenfaktor."* The `max(guaranteed, current)` the model implements, read at last in a fondsgebundene wording rather than inferred from a conventional one [S4]. § 2 Abs. 3 adds the basis of the current factor — *"die Rechnungsgrundlagen eines zu dem Zeitpunkt im Neugeschäft offenen sofortbeginnenden Rententarifs"* — and that the factors depend on the payment frequency, the chosen death benefit and the age at *Rentenbeginn*.
  - **the *Beitragsverrechnung*** — § 14 Abs. 1: premiums and *Zuzahlungen* less *Abschluss- und Vertriebskosten* and *beitragsbezogene Verwaltungskosten* are the *Sparbeiträge*, converted into units at the *Rücknahmepreis*; *"Die zur Deckung des Todesfallrisikos bestimmten … Risikobeiträge, die fixen Verwaltungskosten (Stückkosten) und die vom Fondsguthaben abhängigen Verwaltungskosten entnehmen wir dem Fondsguthaben zu Beginn eines jeden Monats."* Both halves of the model's charge split, including the composite's contested choice to take the *Stückkosten* **by unit cancellation**.
  - **the *Rückkaufswert*** — § 17 Abs. 3: *"Bei Kündigung zahlen wir nach § 169 des Versicherungsvertragsgesetzes (VVG) den Rückkaufswert. Der Rückkaufswert ist das zum Kündigungstermin vorhandene ➜ Fondsguthaben."* And § 17 Abs. 1, that the contract may be terminated *"jederzeit zum Schluss eines Monats in Textform"*.
  - **the decay of a paid-up contract** — § 14 Abs. 2, that on single-premium and paid-up contracts the monthly deductions *"dazu führen [können], dass das gesamte Fondsguthaben vor Rentenbeginn aufgebraucht ist und der Versicherungsschutz damit erlischt"*; and § 16 Abs. 4, that where the fund falls below the tariff minimum the *Rückkaufswert* is paid instead.
  - **the absence of *Bewertungsreserven*** — § 3 Abs. 5: *"Vor Rentenbeginn entstehen bei der Fondsgebundenen Rentenversicherung keine Bewertungsreserven."*
  - **the acquisition-charge shape, which is *not* the shape delib models** — § 18 Abs. 2 splits the *Abschluss- und Vertriebskosten* in two: *"einen Teil … in gleichmäßigen Beträgen über einen Zeitraum von fünf Jahren"* and *"[d]en anderen Teil … als Prozentsatz während der gesamten Beitragszahlungsdauer"*. See the note under [R1]. On an *Einmalbeitrag* and on a *Zuzahlung*, *"entnehmen wir alle Abschluss- und Vertriebskosten sofort dem Beitrag oder der Zuzahlung"* — which is the composite's treatment exactly.
  - **levels, established for the first time anywhere in this corpus.** *Tarifbestimmungen*: minimum premium 25 € monthly / 300 € annual / 1 500 € single; *Aufschubzeit* at least 10 years; *Rentenbeginn* 62 to 85; *Mindestrente* 50 € monthly; *Rentengarantiezeit* 5 to 25 years; *Zuzahlung* minimum 500 €; *Teilauszahlung* minimum 500 € with 1 000 € (premium-paying) / 2 500 € (paid-up) left in the fund and a 40 € fee; minimum *Fondsguthaben* for *Beitragsfreistellung* 2 500 €; *Beitragsdynamik* a fixed 3 % to 10 %; *Stornoabzug* **150 €**, a fixed euro amount, on *Kündigung*, on full *Beitragsfreistellung* and on an early *Rentenbeginn*; *Fondsshift* and *Fondsswitch* free; *Ablaufmanagement* a **default** (opt-out) five-year monthly glide into a low-risk target fund; nine Monega funds, at least 10 % each, at most five per contract; *"Ausgabeaufschläge und Depotkosten fallen nicht an."*
  - **the calculation bases** (Anhang, *Versicherungsmathematische Hinweise*): *"Bei der Kalkulation der zu Vertragsbeginn garantierten Verpflichtungen haben wir einen Zinssatz von 0,25 Prozent verwendet. Abweichend hierzu verwenden wir bei der Kalkulation der zu Vertragsbeginn garantierten Rentenfaktoren der DEVK-Fondsrente vario einen Zinssatz von 0,0 Prozent."* — the 0 % *Rechnungszins* the composite's *Rentenfaktor* derivation is built on, now established for a fondsgebundene tariff. Annuity basis **DAV 2004 R**; the *Risikobeitrag* basis is a unisex order at **65 % of DAV 1994 T**, **not** DAV 2008 T (see [R17]).
  - **the *Basisinformationsblätter*** — see [S15], which they discharge, and [R11] for what their cost figures mean.
  - **the tax notes** (section 4) restate the 12/62 rule, the 15 % *Teilfreistellung* and the *Ertragsanteil* — see [R19] [R20].
  What the document does **not** carry is the charge *levels* in the AVB text: § 18 Abs. 1 refers them to the *Informationsblatt zu Versicherungsprodukten*, which is not in the file. They arrive instead through the *Basisinformationsblätter* [S15].

(delib-fondsgebundene_rentenversicherung-s3)=

### S3 — Allianz Lebensversicherungs-AG, AVB and *Verbraucherinformation* for the fondsgebundene Rentenversicherung ("InvestFlex")
- Publisher / doc type: Allianz Lebensversicherungs-AG, Stuttgart — the German market leader in life; *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung* with the matching *Verbraucherinformation*, *Produktinformationsblatt* and *Basisinformationsblatt*
- URL: `https://www.allianz.de/vorsorge/vorsorgekonzept/invest-flex/` — the publisher's own product page for the *Vorsorgekonzept* **InvestFlex**, found on allianz.de on 2026-08-30. The *Bedingungswerk* itself sits behind `goa-eportale.allianz.de`, which answers **HTTP 403** to a direct request
- Retrieved: **partly.** The **product page** was retrieved (HTML, read 2026-08-30) and settles the product name and the design menu; **the AVB, *Verbraucherinformation* and *Basisinformationsblatt* this entry names were not** — the document host refuses, so **no clause text at all comes from Allianz**
- Used for: the design type; and — now from the retrieved page rather than by inference — that **"InvestFlex" is a real Allianz *Vorsorgekonzept* for a fondsgebundene Rentenversicherung**, that the tag no longer carries `[unverified]`, that it is offered in **two variants on one chassis**, a pure fund-linked form and a form with a *Garantieniveau* backed by the *Sicherungsvermögen*, that the *Garantieniveau* menu runs **10 % to 90 % of premiums paid in 10-percentage-point steps** (10–60 % on the *Basisrente*, a statutory 100 % on the *Riester-Rente*), that fund and strategy switching is free and unlimited, and that *Ablaufmanagement* is **optional** and runs over the **last three years** — against DEVK's five-year default [S2], which is the variation the specification's *Ablaufmanagement* row now rests on. The rule that the bases applied at *Rentenbeginn* are those the company uses at that time for immediately beginning annuities is **no longer sourced here**: it is read verbatim in the DEVK AVB [S2] § 2 Abs. 3. Also one of the eleven carriers behind the finding that **no charge level was established at any carrier other than DEVK** [S3]–[S14].

(delib-fondsgebundene_rentenversicherung-s4)=

### S4 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Fondsgebundene Versicherungen"
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation* — a consolidated pre-contractual document issued per product family and per *Fassung*, typically 40–50 pages
- URL: not established for the fondsgebundene series. The sibling delib research corroborated the **companion** series, "Verbraucherinformation für **Konventionelle** Versicherungen — Aufgeschobene Rentenversicherung", in four editions
- Retrieved: **no** — no address for the fondsgebundene series was found on the publisher's own site on 2026-08-30; the entry is kept as a known reference and its title, edition and content stay `[unverified]`
- Used for: the ***Rentenfaktor* rule at *Rentenbeginn*** — that a second, current factor is compared with the guaranteed one and **the higher of the two applies**. **This entry is no longer the support for that rule**: it is now read verbatim in a fondsgebundene AVB at [S2] (§ 2 Abs. 2), so the transfer from Zurich's *conventional* series that this entry once carried is redundant and the inference behind it is retired. What [S4] still stands for is Zurich as a second carrier of the same rule, and — through [R22] — as the defendant in **LG Köln, Urteil vom 8. Februar 2023, Az. 26 O 12/22**, the first-instance decision on the *Treuhänderklausel* that the specification cites.

(delib-fondsgebundene_rentenversicherung-s5)=

### S5 — Alte Leipziger Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung
- Publisher / doc type: Alte Leipziger Lebensversicherung a. G., Oberursel; *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung* plus *Tarifblatt*
- URL: not established
- Retrieved: **no** — no document was sought at a URL, because none was ever established for this entry; nothing was opened. The entry is kept as a known reference
- Used for: one row of the specification's carrier table, and there **only negatively** — a large mutual understood to offer both a commission tariff and a *Nettotarif* on the same unit-linked chassis `[unverified]`, the pairing that would isolate what the *Abschlusskosten* do to the *Effektivkosten*. **Nothing is established: no tariff code, no charge rate, no fund list, no factor.**

(delib-fondsgebundene_rentenversicherung-s6)=

### S6 — LV 1871, AVB for the fondsgebundene Rentenversicherung ("MeinPlan")
- Publisher / doc type: Lebensversicherung von 1871 a. G., München; AVB, *Produktinformationsblatt*, *Basisinformationsblatt*
- URL: not established
- Retrieved: **no** — no URL for an LV 1871 fondsgebundene *Bedingungswerk* was established, so nothing was opened. The entry is kept as a known reference
- Used for: the **option catalogue** as a mechanic — a *Zuzahlung* subject to a minimum, a *Teilentnahme* subject to a minimum and to a minimum remaining *Fondsguthaben*, a *Beitragsdynamik*, and a flexible *Rentenbeginn*. **Every one of those options has since been read, with its levels, in the DEVK wording [S2]**, so this entry no longer carries the mechanic; it stands only for the claim that the catalogue is general across the market, which remains `[unverified]`. The 50–300 fund range asserted here and at [S13] is **contradicted at the only carrier that could be checked**: DEVK's tariff offers **nine** funds from one house, at least 10 % each and at most five per contract [S2]; the wide-menu claim is retained as `[unverified]` and is now known not to describe every tariff. The product name "MeinPlan" is `[unverified]`.

(delib-fondsgebundene_rentenversicherung-s7)=

### S7 — Stuttgarter Lebensversicherung a. G., AVB for a hybrid fondsgebundene Rentenversicherung ("FlexRente performance-safe")
- Publisher / doc type: Stuttgarter Lebensversicherung a. G.; AVB for a **hybrid** unit-linked annuity, plus *Basisinformationsblatt*
- URL: not established. The sibling delib research corroborated a different Stuttgarter document, establishing only that the carrier publishes pre-contractual information PDFs
- Retrieved: **no** — no URL for a Stuttgarter hybrid *Bedingungswerk* was established, so nothing was opened. The entry is kept as a known reference
- Used for: the **hybrid comparator** in the riders-and-options section — a *dynamisches Hybrid* in which premium and capital are reallocated periodically between the *Sicherungsvermögen*, a *Wertsicherungsfonds* and free funds to secure a chosen *Beitragsgarantie* — and, with [S8] and [S9], for the point that **delib's no-guarantee chassis is a real market form and not a simplification of the only form sold**. That last point is now independently supported: Allianz publishes InvestFlex in a pure fund-linked variant alongside the guarantee variant [S3], and DEVK's L/N FR1 carries no *Beitragsgarantie* at all [S2]. The product name is `[unverified]`; **no reallocation rule, guarantee level or charge is established here** and none is implemented — the one guarantee menu now established is Allianz's 10 %–90 % ladder [S3], and it is not this carrier's.

(delib-fondsgebundene_rentenversicherung-s8)=

### S8 — Volkswohl Bund Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung
- Publisher / doc type: Volkswohl Bund Lebensversicherung a. G., Dortmund; AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: **no** — no URL for a Volkswohl Bund fondsgebundene *Bedingungswerk* was established, so nothing was opened. The entry is kept as a known reference
- Used for: the second named carrier behind the **two-pot hybrid** entry in the guarantee taxonomy, so that the taxonomy rests on more than one carrier, and one row of the negative carrier table. **No parameter is established.**

(delib-fondsgebundene_rentenversicherung-s9)=

### S9 — WWK Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung with i-CPPI guarantee
- Publisher / doc type: WWK Lebensversicherung a. G., München; AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: **no** — no URL for a WWK i-CPPI *Bedingungswerk* was established, so nothing was opened. The carrier is named **from general knowledge rather than from any retrieved or searched document**, and that is stated rather than hidden
- Used for: the **i-CPPI** entry in the guarantee taxonomy — exposure to the risky fund set per policy and continuously as a multiplier times the cushion between the policy value and the present value of the guarantee, the most efficient of the three technologies and the most path-dependent. It is the entry whose **exclusion** from the model needs the most explicit justification, which the specification and `model.md` give. **No algorithm, multiplier, floor or charge is established.**

(delib-fondsgebundene_rentenversicherung-s10)=

### S10 — Cosmos Lebensversicherungs-AG (CosmosDirekt), AVB for the fondsgebundene Rentenversicherung
- Publisher / doc type: Cosmos Lebensversicherungs-AG (Generali group), Saarbrücken, sold direct as CosmosDirekt; *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung*
- URL: not established. The sibling delib research corroborated by search the **classic** Cosmos AVB, tariff LA 904 A, recorded there as its S8
- Retrieved: **no** — no URL for a Cosmos fondsgebundene *Bedingungswerk* was established, so nothing was opened. The entry is kept as a known reference
- Used for: **the conversion basis behind the whole *Rentenfaktor* derivation** — the corroborated statement that the annuity factor fixed at inception rests on a recognised mortality table (currently DAV 2004 R) and an underlying interest rate of **currently 0 percent p.a.** **That inference is no longer needed and no longer load-bearing**: the DEVK Anhang states, for a *fondsgebundene* tariff and in terms, that the guaranteed *Rentenfaktoren* are calculated at *"einen Zinssatz von 0,0 Prozent"* on DAV 2004 R [S2]. This entry is retained as the second, independent instance of the same 0 % convention, and as the direct-writer cost comparator that bounds the *Effektivkosten* range from below with [S13] and [S18].

(delib-fondsgebundene_rentenversicherung-s11)=

### S11 — NÜRNBERGER Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; AVB with a tariff code in the *NIR*/*N* series, plus *Verbraucherinformation*
- URL: not established. The sibling delib research corroborated the classic NÜRNBERGER AVB under tariff NIR3301, establishing the carrier's document naming convention
- Retrieved: **no** — no URL for a NÜRNBERGER fondsgebundene *Bedingungswerk* was established, so nothing was opened. The entry is kept as a known reference
- Used for: one row of the carrier table, recording that the carrier publishes **per-tariff AVB** with codes in an `NIR`/`N` series — the German pattern that makes a tariff code worth recording when it can be established and worth omitting when it cannot. **No NÜRNBERGER fondsgebundene tariff code is asserted anywhere in these documents.** The pattern itself is now confirmed at a second carrier: DEVK's fondsgebundene tariff is **L/N FR1**, with the leading letter distinguishing the mutual from the AG, plus suffixes `E` for the *Einmalbeitrag*, `D` for the *Dynamik* and `S` for the *Abruftarif* [S2].

(delib-fondsgebundene_rentenversicherung-s12)=

### S12 — Continentale Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung ("Rente Invest")
- Publisher / doc type: Continentale Lebensversicherung AG (Continentale Versicherungsverbund); AVB plus *Produktinformationsblatt*
- URL: not established
- Retrieved: **no** — no URL for a Continentale fondsgebundene *Bedingungswerk* was established, so nothing was opened. The entry is kept as a known reference
- Used for: one row of the negative carrier table, widening the carrier set behind the variation section. The product name "Rente Invest" is `[unverified]`. **No parameter is established.**

(delib-fondsgebundene_rentenversicherung-s13)=

### S13 — HDI Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung ("CleverInvest")
- Publisher / doc type: HDI Lebensversicherung AG (Talanx group); AVB plus *Basisinformationsblatt*
- URL: not established. `https://www.hdi.de/privatkunden/altersvorsorge/cleverinvest`, tried on 2026-08-30, answers 200 with the site's **404 page**
- Retrieved: **no** — the one address tried on the publisher's own site is a soft 404 and carries no product document. The entry is kept as a known reference
- Used for: the **low-cost, ETF-capable** comparator beside [S10] and the *Nettotarife* of [S18] — the reason `std_low` and the `etf` fund path ship at all. The 50–300 fund range asserted here and at [S6] is **not confirmed and is contradicted at the one tariff that could be read** [S2]; what *is* now established, from the Allianz product page, is that a large carrier's unit-linked menu contains **ETFs as well as managed funds** [S3], which is enough to justify shipping the `etf` path. The product name and the low-cost characterisation are both `[unverified]`; **no HDI charge level is established.**

(delib-fondsgebundene_rentenversicherung-s14)=

### S14 — Debeka Lebensversicherungsverein a. G., AVB for the fondsgebundene Rentenversicherung
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., Koblenz; *Bedingungswerk* in the carrier's `B LV` series
- URL: not established. The sibling delib research corroborated several Debeka *Bedingungswerke* (B LV 85, B LV 86, B LV 97) and the trade-press report that Debeka **discontinued its classic annuity tariff**
- Retrieved: **no** — no URL for a Debeka fondsgebundene *Bedingungswerk* was established, so nothing was opened. The entry is kept as a known reference
- Used for: **the market-structure fact in the specification's opening** — that Germany's largest life mutual by policy count withdrew its classic annuity tariff, which is what puts the unit-linked and hybrid forms at the centre of German new business. **This entry is no longer the main support for the dominance claim, and the claim is no longer `[unverified]`**: BaFin states it directly in *Risiken im Fokus 2026*, describing *"die im Neugeschäft dominierenden fondsgebundenen Produkte"* [R11]. [S14] now corroborates the mechanism behind that dominance rather than standing in for the fact. The Debeka fondsgebundene *Bedingungswerk* number, edition and content are `[unverified]`.

(delib-fondsgebundene_rentenversicherung-s15)=

### S15 — *Basisinformationsblatt* (PRIIP-KID) for a fondsgebundene Rentenversicherung — document-type entry
- Publisher / doc type: each insurer, for each *Anlageoption* / product variant; *Basisinformationsblatt* under the PRIIPs Regulation [R8] — three pages, prescribed order and prescribed headings
- URL: `https://www.devk.de/media/content/download/produkte/altersvorsorge/DEVK-Fondsrente-Kundeninfo-03101-2024-07.pdf`, pp. 71–119 — **sixteen *Basisinformationsblätter* for the DEVK-Fondsrente vario** (tariffs L FR1 and N FR1; annual premium 1 000 € and *Einmalbeitrag* 10 000 €; *Aufschubzeit* 12, 20, 30 and 40 years), followed from p. 120 by the option-specific documents for the *Anlageoptionen*. They are bound into [S2] rather than published separately
- Retrieved: **yes** (PDF, the BIB block within a 195-page file, *Stand* 01.01.2024, *Erstellungsdatum* 03.11.2023, read 2026-08-30)
- Used for: **the disclosure frame, no longer as a description of what such a document would contain but as the document itself.** Confirmed from the retrieved sheets: the summary risk indicator (this product is graded *"Risikoklasse 2 bis 5"* on the 1–7 scale, a range because the class depends on the chosen fund); the statement that the product carries no protection against market falls; the costs the investor bears, split into *Einstiegskosten*, *laufende Kosten* and *Transaktionskosten*; the *"Jährliche Auswirkungen der Kosten"* — the reduction in yield — and, decisively, its presentation at **exactly three time points, 1 year, half the recommended holding period and the end of it**, which on the 30-year sheet is **years 1, 15 and 30**, precisely as the specification predicted. The recommended holding period is stated as running to the *gesetzlicher Rentenbeginn* at 67.
  Two corrections this document forces. **(a)** The four graded scenarios *Stress / pessimistisch / moderat / optimistisch* that [R9] describes **do not appear on these sheets**: under *"Performance-Szenarien"* the generic sheet for a fund-menu product states only that performance follows the chosen funds and refers the reader to the option-specific documents, which is the multi-option treatment under the RTS. A specification that says a German unit-linked BIB shows four scenario returns is describing the single-option case. **(b)** The sheets carry **real figures**, so the statement that no cost or reduction-in-yield value in these documents comes from an actual BIB is no longer true where those figures are now quoted — see [R11] and the specification's cost section. The one number that matters most: on the sheet whose model point is delib's own anchor cell — *"eine 37 Jahre alte versicherte Person"*, 30 annual instalments, *Aufschubzeit* 30 years — the **guaranteed *Rentenfaktor* is 22,91 € per 10 000 €** and the reduction in yield at 30 years is **1,4 % to 3,4 % p.a.**
  `reduction_in_yield()` remains a **delib-defined** measure: it is not computed on Annex VI and it is not the statutory *Effektivkosten*. That distinction is now sharper, not weaker, because the statutory figure can at last be seen beside it.

(delib-fondsgebundene_rentenversicherung-s16)=

### S16 — *Produktinformationsblatt* / *Verbraucherinformation* — document-type entry
- Publisher / doc type: each insurer; the German pre-contractual information set required by § 7 VVG with the *VVG-Informationspflichtenverordnung* [R7]
- URL: `https://www.devk.de/media/content/download/produkte/altersvorsorge/DEVK-Fondsrente-Kundeninfo-03101-2024-07.pdf`, pp. 4–8 — the *Verbraucherinformationen* section of [S2]
- Retrieved: **partly.** The ***Verbraucherinformation*** limb was retrieved as part of [S2] and read on 2026-08-30. The ***Produktinformationsblatt*** limb — DEVK calls it the *Informationsblatt zu Versicherungsprodukten*, and § 18 Abs. 1 AVB refers the charge levels to it — is **not bound into the file and was not located**, which is why the AVB names no charge rate
- Used for: the second disclosure class the specification's cost section rests on. What the retrieved *Verbraucherinformation* actually gives is thinner than this entry once claimed and worth stating exactly: it names the cost **categories** (*Abschlusskosten* and *übrige Kosten*, the latter mainly administration), then says *"Die genaue Höhe der vorgenannten Kosten in Euro können Sie den Ihnen zusammen mit dem Antrag ausgehändigten Unterlagen entnehmen"* — the euro disclosure required by § 2 Abs. 1 Nr. 1 and Abs. 2 VVG-InfoV [R7] is made in the personalised quotation, not in the standing document. It does establish two things delib relies on: that the fund's own costs are separate and lie in the fund prospectus, and — in terms — *"Ausgabeaufschläge und Depotkosten fallen nicht an."* It also prices two events the composite carries at zero: a *Vertragsumwandlung* at 40 € and a *Teilauszahlung* at 40 €. **No *Effektivkostenquote* appears in it**; that figure reaches this library through the *Basisinformationsblätter* [S15] and BaFin's survey [R11] instead.

(delib-fondsgebundene_rentenversicherung-s17)=

### S17 — *Standmitteilung* (annual statement) — document-type entry
- Publisher / doc type: each insurer, with a GDV model; *Jährliche Mitteilung zum Stand der Versicherung*
- URL: not established. The sibling delib research corroborated a **GDV Muster-Standmitteilung for the kapitalbildende Lebensversicherung, edition 02/2017**, establishing that the GDV publishes model statements per line
- Retrieved: **no** — no GDV *Muster-Standmitteilung* for the fondsgebundene form was located; the entry is kept as a known reference and the existence of a fondsgebundene model statement stays `[unverified]`. **Its statutory content, however, is now read rather than inferred**: § 155 VVG, canonical XML (*Stand*: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156) — see [REG-R25]
- Used for: **the model's state vector, and the definition of the *Fondsguthaben***. § 155 Abs. 1 VVG requires, on a profit-participating contract, the benefit on a claim, the benefit at *Rentenbeginn* on continued payment, the benefit at *Rentenbeginn* on a paid-up basis, *"den Auszahlungsbetrag bei Kündigung des Versicherungsnehmers"* and — for contracts concluded from 1 July 2018 — *"die Summe der gezahlten Prämien"*. That last item is the statutory reason `cum_prem_pp` is reported and not merely held, and the list as a whole is close to the column set of `result_fund()`. Two details this entry previously asserted are **not** in § 155 and are dropped: the statement reports the **cumulative** premiums paid, not the premiums paid in the year, and neither the unit count nor the *Anteilspreis* is a statutory item — they are what a unit-linked insurer adds under § 155 Abs. 2 (*"Weitere Angaben bleiben dem Versicherer unbenommen"*). DEVK's own § 21 AVB is headed *"Wie können Sie den Wert Ihrer Versicherung erfahren?"* [S2].

(delib-fondsgebundene_rentenversicherung-s18)=

### S18 — *Nettotarife* / *Honorartarife* (myLife and the net variants of full-range carriers)
- Publisher / doc type: myLife Lebensversicherung AG and the *Nettotarif* variants of full-range carriers ([S5], [S6], [S13] and others); AVB and *Basisinformationsblatt* of a commission-free tariff
- URL: not established
- Retrieved: **no** — no URL for a myLife or other *Nettotarif* *Bedingungswerk* was established, so nothing was opened. The entry is kept as a known reference and myLife's business model stays `[unverified]`
- Used for: **the `std_netto` charge scale and what its existence proves** — that a *Nettotarif* is the same unit-linked contract with the *Abschluss- und Vertriebskosten* removed from the tariff, the adviser being paid a fee by the client under a separate *Vergütungsvereinbarung*, so that **the difference between a gross tariff's reduction in yield and the same chassis's net one is the acquisition load**. The *category* is now confirmed by the supervisor rather than assumed: BaFin's *Merkblatt 01/2023 (VA)* addresses *"Nettoprodukte", bei denen dem Versicherungsnehmer für den Vertriebsaufwand Kosten entstehen, die nicht durch seine an das LVU gezahlten Beiträge gedeckt sind (und nicht in die Effektivkosten einfließen)* and requires insurers to allow for that burden in the product test anyway [R10] — which also settles a point the technical notes should carry: **a net tariff's advertised *Effektivkosten* excludes the fee the client pays separately**, so a net-versus-gross comparison of the published figure overstates the saving. **No net-tariff or gross-tariff RIY figure is established**, and the four-tariff comparison still displays the gap rather than quoting a level.

---

## Regulatory and actuarial references (product research numbering)

(delib-fondsgebundene_rentenversicherung-r1)=

### R1 — VVG § 169, *Rückkaufswert*, and the *Zeitwert* branch
- Publisher: Bundesministerium der Justiz (Versicherungsvertragsgesetz 2008)
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` — the human-facing link. That page answers 200 with a ~7 kB frameset containing **no statutory text**; the text below was read from the canonical XML at `https://www.gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: **yes** (canonical XML, *Stand*: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; read 2026-08-30)
- Used for: **the pivot of the whole product**, and every subsection designation the library previously withheld is now given.
  - **The *Zeitwert* branch is § 169 Abs. 4**, and it reads: *"Bei fondsgebundenen Versicherungen und anderen Versicherungen, die Leistungen der in § 124 Absatz 2 Satz 2 des Versicherungsaufsichtsgesetzes bezeichneten Art vorsehen, ist der Rückkaufswert nach anerkannten Regeln der Versicherungsmathematik als Zeitwert der Versicherung zu berechnen, soweit nicht der Versicherer eine bestimmte Leistung garantiert; im Übrigen gilt Absatz 3."* On a pure unit-linked contract with no insurer-given guarantee the *Zeitwert* is the *Fondsguthaben* — which is exactly what a real wording says [S2] § 17 Abs. 3 — so `claims(t, "LAPSE")` has no discounting, no *Rechnungszins*, no mortality basis and no second-basis *Mindestrückkaufswert* behind it. The `[unverified]` tag on the subsection designation is **removed**.
  - **The five-year spreading is § 169 Abs. 3, not Abs. 4**, and the statute puts it in the *Deckungskapital* branch: the *Rückkaufswert* is *"bei einer Kündigung des Versicherungsverhältnisses jedoch mindestens der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt"*. **It reaches a pure unit-linked contract only through Abs. 4's closing words *"im Übrigen gilt Absatz 3"*, i.e. to the extent a benefit is guaranteed.** delib's `alpha_spread_months = 60` is therefore best described as market practice matching the statutory shape rather than as a rule § 169 imposes on this contract; the practice itself is confirmed — [S2] § 18 Abs. 2 spreads *"einen Teil"* of the acquisition cost *"in gleichmäßigen Beträgen über einen Zeitraum von fünf Jahren"*. **That same clause contradicts the model's shape in one respect**: the real tariff takes *"[d]en anderen Teil … als Prozentsatz während der gesamten Beitragszahlungsdauer"*, so the acquisition charge does **not** fall to zero at month 61. delib's total premium deduction has the same two-part arithmetic — a 60-month instalment plus a whole-term percentage — but calls the second part *beitragsbezogene Verwaltungskosten*. No model change is made here; see the report.
  - **The *Stornoabzug* conditions are § 169 Abs. 5**: *"Der Versicherer ist zu einem Abzug von dem nach Absatz 3 oder 4 berechneten Betrag nur berechtigt, wenn er vereinbart, beziffert und angemessen ist. Die Vereinbarung eines Abzugs für noch nicht getilgte Abschluss- und Vertriebskosten ist unwirksam."* Note what the statute does **not** say: the burden of proof on the insurer is a contractual undertaking, not a statutory one — [S2] § 17 Abs. 4 adds *"Die Angemessenheit ist im Zweifel von uns nachzuweisen"* of its own motion. And a real *Stornoabzug* on this product is a **fixed euro amount** — 150 € at DEVK, justified by the change in the risk profile of the remaining portfolio and by administration cost, never by unamortised acquisition cost — where `stornoabzug_pp(t)` is a percentage of the fund. Also § 169 Abs. 6, the temporary reduction power, which [S2] § 17 Abs. 5 reproduces verbatim.

(delib-fondsgebundene_rentenversicherung-r2)=

### R2 — VVG § 168, *Kündigung*
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__168.html` — human-facing link; the page is a ~5 kB frameset with no statutory text, and the text was read from the canonical XML
- Retrieved: **yes** (canonical XML, *Stand*: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; read 2026-08-30)
- Used for: the policyholder's right to terminate. § 168 Abs. 1: *"Sind laufende Prämien zu zahlen, kann der Versicherungsnehmer das Versicherungsverhältnis jederzeit für den Schluss der laufenden Versicherungsperiode kündigen."* On a monthly-premium contract that is a short notice period, and a real tariff is shorter still — [S2] § 17 Abs. 1 allows termination *"jederzeit zum Schluss eines Monats in Textform"*. Paired with [R1] it is what makes *Storno* on a German unit-linked policy a near-frictionless exit at fund value, and it is the structural basis — not an observation — for the front-loaded lapse shape the `[std]` `lapse_table.csv` carries and for the dynamic-lapse module. Two `[unverified]` tags are **removed** and one claim corrected: there is **no single-premium restriction** — Abs. 2 extends the right to a single-premium contract where the insurer's obligation is certain. The restriction that does exist is Abs. 3, which disapplies the right to a certified *Basisrentenvertrag* whose realisation has been excluded and to contracts protected under §§ 851c/851d ZPO; **neither reaches this Schicht-3 product**, and that is why the exit is frictionless here and is not on delib `basisrente`.

(delib-fondsgebundene_rentenversicherung-r3)=

### R3 — VVG § 165, *Prämienfreie Versicherung* (*Beitragsfreistellung*)
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` — human-facing link; the page is a ~4 kB frameset with no statutory text, and the text was read from the canonical XML
- Retrieved: **yes** (canonical XML, *Stand*: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; read 2026-08-30)
- Used for: the right to demand conversion to a paid-up contract — § 165 Abs. 1: *"Der Versicherungsnehmer kann jederzeit für den Schluss der laufenden Versicherungsperiode die Umwandlung der Versicherung in eine prämienfreie Versicherung verlangen, sofern die dafür vereinbarte Mindestversicherungsleistung erreicht wird. Wird diese nicht erreicht, hat der Versicherer den auf die Versicherung entfallenden Rückkaufswert einschließlich der Überschussanteile nach § 169 zu zahlen."* Two things follow that the library previously left open. **The minimum is statutory in kind and contractual in level** — the *Mindestversicherungsleistung* is *"vereinbart"*, disclosed under § 2 Abs. 1 Nr. 5 VVG-InfoV [R7], and it is 2 500 € of *Fondsguthaben* at DEVK [S2]; the `[unverified]` tag on its existence goes, the level stays `[std]`. **And the statute itself routes a below-minimum request to surrender**, which is what [S2] § 16 Abs. 4 does. The point the model turns on — that on a fondsgebundene contract **nothing is converted**, the units stay, the premium-based charges stop and the *kapitalbezogene* charges, the *Stückkosten* and the *Risikobeitrag* continue by cancelling units — is **not** in § 165, whose Abs. 2 assumes a conventional recomputation *"unter Zugrundelegung des Rückkaufswertes nach § 169 Abs. 3 bis 5"*; it is a contractual consequence, and it is now read in one: [S2] § 14 Abs. 1 and Abs. 2. That is model point 7 exactly, and it is why the fund-based charge must cancel units rather than be netted out of the premium.

(delib-fondsgebundene_rentenversicherung-r4)=

### R4 — VVG § 163, *Anpassung der Prämie* / adjustment with a *Treuhänder*
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` — human-facing link; the page is a ~6 kB frameset with no statutory text, and the text was read from the canonical XML
- Retrieved: **yes** (canonical XML, *Stand*: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; read 2026-08-30)
- Used for: the statutory channel through which a life insurer may adjust a contract. § 163 Abs. 1 requires **all three** of: a change in the *Leistungsbedarf* that is *"nicht nur vorübergehend und nicht voraussehbar"* against the bases of the agreed premium; a re-set premium that is *"angemessen und erforderlich … um die dauernde Erfüllbarkeit der Versicherungsleistung zu gewährleisten"*; and confirmation by an independent *Treuhänder*. Abs. 1 Satz 2 bars the route where the benefits were under-calculated at the outset and a careful actuary should have seen it. Reading the section corrects the library's characterisation of it in one respect that matters: **§ 163 is primarily a power to re-set the *premium*, not the benefit.** Abs. 2 Satz 1 gives the *policyholder* the option of a benefit reduction instead of a premium increase; only Abs. 2 Satz 2 gives the insurer a direct power to reduce the benefit, and only *"[b]ei einer prämienfreien Versicherung"*. So on a premium-paying contract § 163 is a narrower route to a lower *Rentenfaktor* than "the only remaining route" suggests. The model treats the guaranteed factor as fixed for the life of the contract and records § 163 as a model risk rather than implementing it; the `[unverified]` tags on the paragraph number and the conditions are **removed**.

(delib-fondsgebundene_rentenversicherung-r5)=

### R5 — VVG § 153, *Überschussbeteiligung* and the *Bewertungsreserven*
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — human-facing link; the page is a ~5 kB frameset with no statutory text, and the text was read from the canonical XML
- Retrieved: **yes** (canonical XML, *Stand*: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; read 2026-08-30)
- Used for: the entitlement to a share of the surplus and of the *Bewertungsreserven*. § 153 Abs. 1: *"Dem Versicherungsnehmer steht eine Beteiligung an dem Überschuss und an den Bewertungsreserven (Überschussbeteiligung) zu, es sei denn, die Überschussbeteiligung ist durch ausdrückliche Vereinbarung ausgeschlossen; die Überschussbeteiligung kann nur insgesamt ausgeschlossen werden."* That answers this entry's open question: **exclusion is permitted, but only in its entirety — an insurer may not exclude the investment limb and keep the rest.** The `[unverified]` tag goes. Abs. 2 requires a *verursachungsorientiertes Verfahren*; Abs. 3 Satz 2 allocates half the *Bewertungsreserven* determined at termination; and **Abs. 4 is the provision that matters most for this product** — *"Bei Rentenversicherungen ist die Beendigung der Ansparphase der nach Absatz 3 Satz 2 maßgebliche Zeitpunkt"*, so the *Bewertungsreserven* allocation point on an annuity is *Rentenbeginn*, not death or surrender. The *Bewertungsreserven* limb having almost nothing to attach to before then is now a read fact rather than an inference: [S2] § 3 Abs. 5 states *"Vor Rentenbeginn entstehen bei der Fondsgebundenen Rentenversicherung keine Bewertungsreserven."* It remains the authority behind the model's stated omission of the surplus credit and behind the statement that the omission biases the projected *Fondsguthaben* downward.

(delib-fondsgebundene_rentenversicherung-r6)=

### R6 — VVG § 152, *Widerruf*, and §§ 7–8 VVG (pre-contractual information)
- Publisher: Bundesministerium der Justiz
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__152.html` (frameset shell, ~6 kB, no statutory text) · `https://www.gesetze-im-internet.de/vvg_2008/__7.html` (this one **does** carry the text, 8.8 kB)
- Retrieved: **yes** (canonical XML for both, *Stand*: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; read 2026-08-30)
- Used for: § 7 Abs. 1, that the insurer must supply *"seine Vertragsbestimmungen einschließlich der Allgemeinen Versicherungsbedingungen sowie die in einer Rechtsverordnung nach Absatz 2 bestimmten Informationen in Textform"* in good time before the policyholder's declaration — the statutory hook under which the *Effektivkosten* disclosure sits [R7]; and § 7 Abs. 2 Nr. 2, which is the specific enabling power for the life-insurance cost information, naming *"die Abschluss- und Vertriebskosten und die Verwaltungskosten, soweit eine Verrechnung mit Prämien erfolgt"* — the statutory origin of delib's alpha/beta distinction. **The 30-day period is confirmed and its tag removed**: § 152 Abs. 1, *"Abweichend von § 8 Absatz 1 Satz 1 beträgt die Widerrufsfrist 30 Tage."* One claim is **corrected**. The amount repayable is not simply the unit value: § 152 Abs. 2 Nr. 2 gives the *Rückkaufswert* nach § 169 plus the unearned premium, and Abs. 3 Nr. 2 — where the policyholder was not told cover had begun — gives *"den Rückkaufswert … oder, wenn dies für den Versicherungsnehmer günstiger ist, die für das erste Jahr gezahlten Prämien"*. So after a market fall the statute can in fact return the first year's premiums, which is the opposite of what this entry previously said. delib does not project the window; it is absorbed into the year-1 lapse rate, and that treatment is unaffected.

(delib-fondsgebundene_rentenversicherung-r7)=

### R7 — VVG-InfoV § 2 — cost disclosure, the *Effektivkosten* and the *Modellrechnung*
- Publisher: Bundesministerium der Justiz (*Verordnung über Informationspflichten bei Versicherungsverträgen*)
- URL: `https://www.gesetze-im-internet.de/vvg-infov/__2.html` — unlike the VVG per-section pages this one returns the **full text** (10.2 kB)
- Retrieved: **yes** (HTML, complete section text, read 2026-08-30)
- Used for: four things, three of which were open questions.
  - **The euro disclosure**, Abs. 1 Nr. 1 with Abs. 2: the *"einkalkulierten Abschlusskosten als einheitlicher Gesamtbetrag"* and the other costs *"als Anteil der Jahresprämie unter Angabe der jeweiligen Laufzeit"*, with administration costs shown separately, and *"[d]ie Angaben nach Absatz 1 Nr. 1, 2, 4 und 5 haben in Euro zu erfolgen"*. Also Nr. 5, the *Mindestversicherungsbetrag* for a paid-up conversion [R3], and Nr. 7, the fondsgebundene-specific duty to state *"die der Versicherung zugrunde liegenden Fonds und die Art der darin enthaltenen Vermögenswerte"*.
  - **The *Effektivkosten* — the statutory term is *Effektivkosten*, not *Effektivkostenquote*.** Abs. 1 Nr. 9 defines them, for contracts where the insurer's obligation is certain, as *"die Minderung der Wertentwicklung durch Kosten in Prozentpunkten (Effektivkosten) bis zum Beginn der Auszahlungsphase"*. **Abs. 6 settles the fund-cost question outright**: they are *"berechnet wie der Gesamtkostenindikator nach Anhang VI der Delegierten Verordnung (EU) 2017/653"*, with the contract's own parameters — so the fund's costs enter because Annex VI's total-cost indicator includes them, which is what makes the TER a policy parameter and why the model nets it off the return. The `[unverified]` tag on the fund-cost point is **removed**; the 1 January 2015 introduction date is **not** in this text and keeps its tag.
  - **The *Modellrechnung* rates are now exact** — Abs. 3: the *Höchstrechnungszinssatz* multiplied by 1,67, that rate plus one percentage point, and that rate minus one percentage point. Three rates, defined, not `[unverified]` any more. **But see the correction under [REG-R25]: § 154 Abs. 1 Satz 2 VVG excludes unit-linked contracts from the *Modellrechnung* altogether**, so this requirement does not apply to this product.
  - The statement that `reduction_in_yield()` **is not** the statutory figure. Abs. 6 makes that sharper rather than weaker: the statutory figure is an Annex VI calculation on a prescribed pre-cost return, and delib computes neither.

(delib-fondsgebundene_rentenversicherung-r8)=

### R8 — PRIIPs Regulation (EU) 1286/2014 and the RTS, Delegated Regulation (EU) 2017/653 as amended
- Publisher: European Parliament and Council; European Commission
- URL: not established. The regulations themselves were not opened at EUR-Lex; the citations below are read from two documents that quote them in full — the DAV *Ergebnisbericht* [R18] and § 2 Abs. 6 VVG-InfoV [R7]
- Retrieved: **no** — the instruments were not retrieved. **The citation data is no longer `[unverified]`**, being taken from two retrieved documents that reproduce it
- Used for: the requirement of a ***Basisinformationsblatt*** for every packaged retail and insurance-based investment product, a fondsgebundene Rentenversicherung being the paradigm German IBIP — and a real one is now in hand [S15]. **The numbers are established**: Verordnung (EU) Nr. 1286/2014 of 26 November 2014, and the RTS, Delegierte Verordnung (EU) 2017/653 of 8 March 2017, amended by (EU) 2019/1866 (so cited in § 2 Abs. 6 VVG-InfoV) and by **(EU) 2021/2268** (so cited by the DAV [R18]). **The category assignment is contradicted where the specification guessed it.** delib assumed a pure unit-linked contract falls in Category 2 and takes its scenarios from the funds' own return history. The DAV report says the opposite for German practice: a *Versicherungsanlageprodukt* whose pots are inseparably linked *"über einen oder mehrere der Mechanismen Wertsicherungsalgorithmus, Überschussbeteiligung, **Kostenentnahmen** und ggf. **biometrische Komponenten**"* cannot be decomposed under Ziffer 27 Anhang II RTS and is a **Kategorie 4** product — and it names *"Rentenversicherungen der 3. Schicht"* as the leading instance. A contract with monthly cost deductions and a *Risikobeitrag* is exactly that. The consequence for delib is unchanged and if anything stronger: the `[std]` 5,00 % fund path is a labelled assumption and **nothing this model produces may be compared with a PRIIPs scenario**.

(delib-fondsgebundene_rentenversicherung-r9)=

### R9 — BaFin *Fachartikel*, "PRIIPs-Verordnung: Wie Versicherer Verbraucher informieren" (2022)
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht (BaFinJournal)
- URL: `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2207_priips_surfday.html` — recorded in the sibling delib research on `kapitallebensversicherung`
- Retrieved: **no** — **HTTP 404** at the cited URL on 2026-08-30. The article is still listed under that address in BaFin's own search index but the page has been withdrawn; no replacement address was found on bafin.de. The entry is kept as a known reference
- Used for: the frame of the specification's disclosure section — a total risk indicator, the possible maximum loss, four graded scenarios (*Stress*, *pessimistisch*, *moderat*, *optimistisch*), the costs the investor bears at three time points split into one-off and ongoing, and the *Effektivkosten* of a specimen contract published on the insurer's website. **This entry is no longer the source of any of it, and two parts of it are now known to be wrong for this product.** A real fondsgebundene *Basisinformationsblatt* has been read [S15]: it confirms the risk indicator, the three time points and the cost split, but **it shows no four-scenario table** — for a fund-menu product the generic sheet points to the option-specific documents instead — and it states the reduction in yield rather than an *Effektivkosten* figure. The specimen-contract *Effektivkosten* duty is [R7] Abs. 1 Nr. 9. Everything the disclosure section says should now be read against [S15], [R7] and [R11] rather than against this entry.

(delib-fondsgebundene_rentenversicherung-r10)=

### R10 — BaFin, Merkblatt 01/2023 (VA) on *wohlverhaltensaufsichtliche Aspekte bei kapitalbildenden Lebensversicherungsprodukten*
- Publisher: BaFin; published **8 May 2023** — the date is on the retrieved page and the `[unverified]` tag is removed
- URL: `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html`
- Retrieved: **yes** (HTML, complete text of sections A–D, read 2026-08-30)
- Used for: the supervisory frame this product's charge stack sits in, now quoted rather than summarised.
  - ***Renditeziel*** — Rn. 15: *"Ein angemessener Kundennutzen setzt voraus, dass das formulierte Renditeziel mit hinreichender Wahrscheinlichkeit erreicht wird. Dies ist im Rahmen der Produktprüfung mit geeigneten stochastischen Analysen zu prüfen."* Rn. 14 requires the insurer to test whether the target market seeks *"nicht nur eine positive Rendite nach Kosten, sondern auch eine positive Rendite nach Kosten und Inflation"* — the *"realer Anlageerfolg"*, benchmarked against the ECB's medium-term inflation target. Rn. 17 says the exercise is generally indispensable for *"[r]ein fondsgebundene Produkte und Hybridprodukte"* and may be dispensable for classic ones.
  - **The measure** — Rn. 18: the *Effektivkosten* computed *"nach der Methodik … welche die LVU für Produkte im Sinne von § 2 Abs. 1 Nr. 9 VVG-InfoV i.V.m. § 2 Abs. 6 VVG-InfoV … zu verwenden haben"* [R7].
  - ***Stückkosten*, and this bears directly on delib's 3,00 €/month** — Rn. 21: *"Setzt ein LVU in der Beitragskalkulation z.B. in erheblichem Maße Stückkosten in Form eines absoluten jährlichen Euro-Betrages an, so kann dies dazu führen, dass sich die Effektivkosten in Abhängigkeit von der Höhe des jährlichen Beitrages erheblich unterscheiden."* **This is the "differ considerably" sentence, and it is about premium size, not about providers.** The claim that *Effektivkosten* differ considerably *between providers and products* is a real BaFin finding but it belongs to [R11], not here; attributing it to the *Merkblatt* was a misreading and is corrected wherever it appeared.
  - **Lapse** — Rn. 24: where a material share of the target market will terminate early, *"[e]s reicht dann nicht, den Kundennutzen nur auf das Ende der vertraglichen Ansparphase zu beziehen"*, and *"[e]in wesentlicher Anteil … dürfte in jedem Fall die Hälfte der Angehörigen des Zielmarkts sein"*.
  - **The annuity conversion is supervised** — Rn. 9: *"Auch ein vorgesehener Rentenbezug … unterliegt als Produkteigenschaft der Prüfung eines angemessenen Kundennutzens. Anknüpfungspunkt ist insbesondere das Verhältnis zwischen dem am Ende der Ansparphase zur Verfügung stehenden Kapital und den vom Kunden voraussichtlich bezogenen Rentenleistungen."* That is the *Rentenfaktor*, named as a *Kundennutzen* parameter.
  - ***Kickback*** — Rn. 31–34: insurers do receive *Rückvergütungen* out of the fund's *Verwaltungsvergütung*; they must test for *Fehlanreize*; and they must consider compensating for them by reducing the calculated costs, by an RfB allocation above the MindZV minimum, by a *Kostenüberschussanteil* or by *"einen besonderen Überschussanteil zur Erstattung von Rückvergütungen"*. That is a large part of the answer delib recorded as unresolved.
  - ***Nettotarife*** — the *Merkblatt* addresses *"Nettoprodukte"* whose distribution cost falls outside the premium *"(und nicht in die Effektivkosten einfließen)"*; see [S18].
  **No numerical threshold appears in the *Merkblatt*** and none is quoted from it; the numbers come from [R11].

(delib-fondsgebundene_rentenversicherung-r11)=

### R11 — BaFin, *Risiken im Fokus 2026* — "Kosten von kapitalbildenden Lebensversicherungen"
- Publisher: BaFin; annual supervisory risk-focus publication, consumer-protection chapter. **Two documents are read under this entry**: the chapter itself, and the underlying survey it refers back to — BaFinJournal, *"Wenn Lebensversicherungen zu viel kosten"* (2022), `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2203_Effektivkosten_Versicherer.html`
- URL: `https://www.bafin.de/DE/die-bafin/publikationen-daten/risiken-im-fokus/Fokusrisiken_2026/RIF_Verbraucher_3/RIF_verbraucher_lebensversicherung_node.html`
- Retrieved: **yes** (HTML, both documents complete, read 2026-08-30)
- Used for: **this is where the specification's market numbers now come from, and it changes several of them.** The chapter is still a named 2026 focus risk, three years after the *Merkblatt* [R10]. What it adds:
  - **The dominance claim, which the specification carried as `[unverified]`, is stated by the supervisor**: a 2025 survey of 2024 new business showed *Effektivkosten* falling since 2021 *"insbesondere bei den im Neugeschäft **dominierenden fondsgebundenen** Produkten"*, with a fall of more than **0,4 percentage points** in the upper quartile at the long, high-volume terms. The tag can go.
  - **Scale**: *"Im Jahr 2024 gab es hierzulande rund 59 Millionen kapitalbildende Lebensversicherungen. 2,4 Millionen Verträge wurden in dem Jahr neu abgeschlossen."*
  - ***"Die Effektivkosten der verschiedenen Anbieter und Produkte unterscheiden sich erheblich."*** — the between-provider finding, which belongs here and not to [R10]; and *"In Einzelfällen beliefen sich die Effektivkosten auf über vier Prozent."*
  - **The 2022 survey gives a distribution at delib's own anchor model point.** For an entry age of **37** and a term of **30 years**, the most-sold fondsgebundene products' *Effektivkosten* are **1,90 % weighted mean**, with quartiles at **1,30 % / 1,64 % / 2,35 %**. Also: *Effektivkosten* rise as the term shortens; they lie *"signifikant über den Werten der klassischen Lebensversicherung"*; and *"[b]ei allen Eintrittsalter-Laufzeit-Kombinationen gibt es Lebensversicherer, bei denen die Effektivkosten … oberhalb von 4 Prozent liegen"*. **The statement that no numerical threshold, band, median or sector benchmark was established is no longer true** — there is now a market distribution at the exact cell delib projects.
  - ***Kickback* levels, which contradict delib's argued range.** On about a third of the most-sold fondsgebundene new business the fund houses pay rebates to the insurer, *"im gewichteten Mittel pro Jahr bei knapp über 0,30 Prozent des Fondsguthabens"* and *"in der Spitze bis über 1,20 Prozent"*. Of that, about 80 % of the business carries a special *Überschussanteil* returning on average **52 %** of the rebate, and a quarter of those products return it in full. A further **19 %** of the business has rebates paid straight to the intermediary, averaging about **0,50 %**. delib's variation table gives the *Kickback* range as 0 %–0,50 % p.a.; the observed range runs to over 1,20 %.
  - **The TER is inside the *Effektivkosten*** — *"Die Fondsmanagementgebühren … gehören zwar zu den Effektivkosten"*, though not to the *einkalkulierte Abschlusskosten* disclosed under § 2 Abs. 1 Nr. 1 VVG-InfoV. And *"[d]em überwiegenden Teil der fondsgebundenen Verträge liegen Aktienfonds zugrunde."*
  - **A finding that supports delib's omission of the surplus credit**: a 2025 BaFin survey found *"dass mehr als die Hälfte der Lebensversicherer derzeit auch bei neueren, auskömmlich kalkulierten Produkten keine Risikoüberschussbeteiligung deklariert hat."*
  - Early *Storno* is itself a supervisory signal: *"Bei Produkten mit einer hohen Frühstornoquote dürfte der Kundennutzen unangemessen sein."*

(delib-fondsgebundene_rentenversicherung-r12)=

### R12 — DeckRV — *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher: Bundesministerium der Justiz / Bundesministerium der Finanzen (*Deckungsrückstellungsverordnung*)
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` — the table-of-contents page (a ~6 kB shell with no section text); the sections were read from the canonical XML at `https://www.gesetze-im-internet.de/deckrv_2016/xml.zip`
- Retrieved: **yes** (canonical XML, *Stand*: Zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250; read 2026-08-30)
- Used for: **the one anchor in the charge stack that was already numeric, now quoted exactly** — § 4 Abs. 1 Satz 2: *"Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten."* Note the base: the statute says *Summe aller Prämien*, which is what delib calls the *Beitragssumme*. The tag is **removed**. § 4 Abs. 4 confirms that the *Zillmersatz* used at conclusion applies for the whole term. The cut from 40 ‰ is not in this text and stays with [R13].
  **And the asymmetry, which the statute makes textual rather than inferential.** § 2 Abs. 1 is expressly confined to guaranteed-interest contracts — *"Bei Versicherungsverträgen **mit Zinsgarantie** … wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf 1 Prozent festgesetzt"* — so a pure fondsgebundene accumulation phase, having no *Zinsgarantie*, is outside the section altogether. The **1 Prozent** figure is confirmed as the rate now in force; **the 1 January 2025 commencement date is not in the DeckRV text** (it is in the amending *Verordnung* of 19 July 2024) and keeps its `[unverified]` tag. The rate reaches this product only through the *Rentenfaktor* and through hybrid designs — and even there an insurer may use less: DEVK calculates its guaranteed *Rentenfaktoren* at **0,0 %** and its other guaranteed obligations at 0,25 % [S2].

(delib-fondsgebundene_rentenversicherung-r13)=

### R13 — LVRG 2014, *Lebensversicherungsreformgesetz*
- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established. **No Bundesgesetzblatt citation is given** — inventing one is exactly what the retrieval conditions forbid
- Retrieved: **no** — no address for the Act or its Bundesgesetzblatt page was established, so nothing was opened; the entry is kept as a known reference. Note that both facts it carries are visible in their *results*: the 25 ‰ cap now in force is read at [R12], and the *Effektivkosten* duty at [R7]. **What remains unverified is the reform history** — that the cap was 40 ‰ before, and that the duty began on 1 January 2015
- Used for: the reform that **cut the *Höchstzillmersatz* from 40 ‰ to 25 ‰** [R12] and **introduced the *Effektivkosten* disclosure** in quotations from 1 January 2015 [R7] — the two facts the `[std]` acquisition charge and the cost-disclosure section rest on. All dates are `[unverified]`, and the 40 ‰ → 25 ‰ cut is corroborated only at the level of a secondary consumer page in a sibling file; the reported post-LVRG fall in *Abschlusskosten* is `[unverified]` and is not used.

(delib-fondsgebundene_rentenversicherung-r14)=

### R14 — MindZV, *Mindestzuführungsverordnung*
- Publisher: Bundesministerium der Finanzen
- URL: `https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html` — this address returns the **full consolidated text** (52.6 kB), unlike the per-section VVG pages. The bare `/mindzv/` form recorded elsewhere in the library is a **404**
- Retrieved: **yes** (canonical XML for the sections quoted, *Stand*: Zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688; read 2026-08-30)
- Used for: the minimum share of each surplus source credited to policyholders. **The percentages are now established and the `[unverified]` tag is removed**: § 6 Abs. 1, **90 %** of the creditable investment income less the *rechnungsmäßige Zinsen*; § 7, **90 %** of the *Risikoergebnis*; § 8, **50 %** of the *übriges Ergebnis*. **And the claim that a unit-linked contract's investment result never enters the *Rohüberschuss* is confirmed textually**: § 3 Abs. 1 computes the creditable investment income from the total investment result *"**ohne die der Lebensversicherung für Rechnung und Risiko der Versicherungsnehmer zuzuordnenden Erträge und Aufwendungen**"* — the unit-linked result is excluded by the definition itself, so for this product only §§ 7 and 8 can bite. With [R5] it is the authority behind the model's decision to compute the risk result and credit none of it back. The 50 % floor on the *übriges Ergebnis* is also the mechanism BaFin points to for uncompensated fund rebates [R11].

(delib-fondsgebundene_rentenversicherung-r15)=

### R15 — VAG — *Sparteneinteilung*, asset congruence and the *Zuwendungen* rules
- Publisher: Bundesministerium der Justiz (*Versicherungsaufsichtsgesetz* 2016)
- URL: `https://www.gesetze-im-internet.de/vag_2016/` — the table-of-contents page (88.5 kB); the sections and Anlage 1 were read from the canonical XML
- Retrieved: **yes** (canonical XML, read 2026-08-30)
- Used for: three things, and **the first two need correcting**.
  - **The *Sparte* is named "Fondsgebundene Lebensversicherung", Nr. 21 of Anlage 1** (*Einteilung der Risiken nach Sparten*, Fundstelle BGBl. I 2015, 555–556). It is **not** called *"fonds- und indexgebundene Lebensversicherung"*, which is how this library has been describing it; index-linked business is not separately listed. The correction is made in the specification and in the [REG-R5] gloss below.
  - **The *Anlagestock* is a division *of* the *Sicherungsvermögen*, not something held outside it.** § 125 Abs. 5: *"Für jede Anlageart ist eine **Abteilung des Sicherungsvermögens (Anlagestock)** zu bilden, soweit Lebensversicherungsverträge Versicherungsleistungen … in Anteilen an einem offenen Investmentvermögen … vorsehen"*. The congruence rule itself is § 124 Abs. 2 Satz 2 Nr. 1 — for benefits tied to fund units, *"die versicherungstechnischen Rückstellungen für diese Leistungen so genau wie möglich durch die betreffenden Anteile … abzubilden"*. That is what removes the investment-mismatch term from the model, and it is intact; what changes is the description of where the *Anlagestock* sits. § 124 Abs. 2 Satz 1 also disapplies the mixing and spreading rules of Abs. 1 Nr. 5–8 to unit-linked contracts — except, under Nr. 3, for the assets backing a guarantee, which is the prudential reason a hybrid's guaranteed pot behaves like general-account money.
  - The IDD-derived ***Zuwendungen*** rules behind the *Kickback* question: the *Merkblatt* [R10] cites § 23 Abs. 1a–1c and § 48a VAG as the national implementation, and Rn. 31–34 there is now the substantive answer the model sidesteps with a passive fund. § 138 VAG (prudent premium calculation and equal treatment) and § 139 (RfB, and the *Sicherungsbedarf* limb of the *Bewertungsreserven*) were also read.

(delib-fondsgebundene_rentenversicherung-r16)=

### R16 — DAV 2004 R, *Sterbetafel für Rentenversicherungen*
- Publisher: Deutsche Aktuarvereinigung e. V.
- URL: not established
- Retrieved: **no** — the table itself is not public and was not retrieved; **its use on this product is now established** at first hand. The DEVK Anhang names, *"für die Rentenleistungen der Fondsgebundenen Rentenversicherung: Sterbetafel DAV 2004 R"*, applied through a *"geschlechtsunabhängige Ausscheideordnung"* [S2]
- Used for: the **annuity** basis behind the *Rentenfaktor* — generational, per birth cohort, with first- and second-order versions — and therefore the second of the product's two mortality bases. **Its generational character is now visible in the numbers rather than asserted**: on the same tariff, the same *Rentenbeginn* age of 67 and the same 0 % *Rechnungszins*, DEVK's guaranteed *Rentenfaktor* falls with the length of the deferment — **25,22 / 24,12 / 22,91 / 21,83 €** per 10 000 € at 12 / 20 / 30 / 40 years — which is a later birth cohort living longer at 67 and nothing else [S15]. That is also a shape delib does **not** reproduce: `rentenfaktor_table.csv` varies the factor with the annuity age alone. **DAV tables are DAV property, are not public and are not redistributed by this library**: the table is cited by name, a `[std]` proxy ships in its place, and what a replacement must preserve — a generational annuitant basis with a first-order margin — is stated in the `Data` docstring.

(delib-fondsgebundene_rentenversicherung-r17)=

### R17 — DAV 2008 T, *Sterbetafel für Lebensversicherungen mit Todesfallcharakter*
- Publisher: Deutsche Aktuarvereinigung e. V.
- URL: not established
- Retrieved: **no** — the table itself is not public and was not retrieved
- Used for: the **death** basis on which the *Risikobeitrag* is priced — and here a retrieved document **contradicts the library**. delib asserts that the *Risikobeitrag* of a German FRV is priced on **DAV 2008 T**. The one carrier whose bases can now be read prices it on something else: the DEVK Anhang states that *"[d]ie aus dem Fondsguthaben während der Aufschubzeit monatlich zu entnehmenden Risikobeiträge kalkulieren wir mit einer mit **65 Prozent gewichteten** geschlechtsunabhängigen Ausscheideordnung auf Basis der **Sterbetafel DAV 1994 T**"*, and reserves DAV 2008 T for its underwritten *Risiko-Zusatzversicherung* [S2]. **The structural claim survives and is confirmed** — the tariff really does carry two mortality bases at once, an annuity table for the conversion and a death table for the risk charge, and a model pricing the death charge on the annuity table would misprice it. **The identification of the death table does not**, and the specification and notes now say DAV 2008 T *or a weighted older death table such as DAV 1994 T*. `mort_table.csv` is unaffected: it is a `[std]` Gompertz proxy anchored at `q(37) = 0.00080` so the worked example reproduces, the table is cited and not shipped, and a replacement must preserve an insured-lives gradient and a first-order margin **above** best estimate — the 65 % weighting DEVK applies is a reminder that "first order" on a *Beitragsrückgewähr* cover can mean a heavy old table scaled down, not a modern table loaded up.

(delib-fondsgebundene_rentenversicherung-r18)=

### R18 — DAV, *Ergebnisbericht* — Standardverfahren PRIIP Kategorie 4 (1 July 2025)
- Publisher: Deutsche Aktuarvereinigung e. V., *Ausschuss Lebensversicherung*
- URL: `https://aktuar.de/content/PDF/Fachwissen/2025-07-01_DAV_Ergebnisbericht_LV_Standardverfahren_PRIIP_Kategorie_4.pdf`
- Retrieved: **yes** (PDF, 30 pp., adopted 1 July 2025, read 2026-08-30 — the preamble, the *Inhalt und Anwendungsbereich* and section 1 *Einleitung*; the capital-market model in the annexes was not worked through)
- Used for: the **profession-agreed standard method for PRIIP *Kategorie 4***, and it now says something sharper than the specification assumed. The report presents itself as *"im Sinne des Anhangs II der RTS zu PRIIP einen 'robusten, anerkannten Branchen- oder Regulierungsstandard'"* for products assigned to Kategorie 4 under Ziffer 7 Anhang II RTS — those *"deren Wertentwicklung teilweise von nicht am Markt beobachteten Faktoren abhängt"*. It borrows the PIA standard used for certified *Riester*- and *Basisrenten* so that all retirement products are treated comparably. **The assignment the specification guessed is wrong**: the report treats *"Rentenversicherungen der 3. Schicht"* as the leading Kategorie 4 case and holds that decomposition into components is *"im Regelfall nicht möglich"* where the pots are inseparably linked by a *Wertsicherungsalgorithmus*, an *Überschussbeteiligung*, **Kostenentnahmen** or biometric components — which describes a plain fondsgebundene Rentenversicherung with monthly charge deductions and a *Risikobeitrag*, not only a guarantee-bearing one. The conclusion the specification drew stands and is now better founded: two *Basisinformationsblätter* for economically similar products can show very different scenario returns, and **no scenario return is cited anywhere in these documents**. The report also supplies the PRIIPs citation data recorded at [R8].

(delib-fondsgebundene_rentenversicherung-r19)=

### R19 — EStG § 22 — *Ertragsanteilsbesteuerung* of the annuity
- Publisher: Bundesministerium der Justiz (*Einkommensteuergesetz*)
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` — this page returns the **full section text** (47.9 kB)
- Retrieved: **yes** (canonical XML including the *Ertragsanteil* table, read 2026-08-30)
- Used for: that a private annuity arising from the conversion of a fondsgebundene contract is taxed on its ***Ertragsanteil***, a statutory percentage read from the table in § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb by the annuitant's completed age at the start of the annuity. **The tag is removed and one value is added that the library needs**: **18 % at 65–66** — confirmed, and restated in DEVK's own tax notes with the worked figure *"[w]ird zum Beispiel im Alter von 65 Jahren erstmalig eine Jahresrente in Höhe von 10.000 Euro gezahlt, dann beträgt der steuerpflichtige Anteil dieser Rente lediglich 1.800 Euro"* [S2] — and **17 % at 67**, which is delib's own *Rentenbeginn* and therefore the figure any tax gloss on the anchor cell should use. The full table runs from 59 % at age 0–1 to 1 % from 97. The point the specification draws from it is unchanged: the treatment is **identical** for a fondsgebundene and a classic annuity once in payment. Nothing in the model computes tax; the rules enter only through the lapse shape and through the `kapitalwahl` reporting split.

(delib-fondsgebundene_rentenversicherung-r20)=

### R20 — EStG § 20 Abs. 1 Nr. 6 — the *Kapitalwahlrecht*, the 12/62 rule and the *Teilfreistellung*
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — full section text (32.6 kB)
- Retrieved: **yes** (canonical XML, read 2026-08-30; § 52 Abs. 28 for the transitional, and [S2] section 4 for the carrier's own restatement)
- Used for: **the behavioural driver the lapse assumption is shaped around**, now verbatim. § 20 Abs. 1 Nr. 6 Satz 1 taxes *"der Unterschiedsbetrag zwischen der Versicherungsleistung und der Summe der auf sie entrichteten Beiträge (Erträge) im Erlebensfall oder bei Rückkauf des Vertrags"* — surrender included, which is what makes it a lapse driver. **The 12/62 rule needs one correction of detail that the library should carry.** Satz 2 as enacted says the **60th** year of age; the 62 comes from § 52 Abs. 28, *"Absatz 1 Nummer 6 Satz 2 ist für Vertragsabschlüsse **nach dem 31. Dezember 2011** mit der Maßgabe anzuwenden, dass die Versicherungsleistung nach Vollendung des 62. Lebensjahres des Steuerpflichtigen ausgezahlt wird"*. So "12/62" is right for anything delib models and "12/60" for older contracts, and the rule's `[unverified]` tag is removed. That is the `lapse_tax_step` of ×2.5 in the policy year `max(13, 62 − entry_age + 1)`, and it is why keying the step on duration alone is a listed pitfall. **The *Teilfreistellung* is in this section, not in the InvStG**, and is exact — Satz 9: *"Bei fondsgebundenen Lebensversicherungen sind 15 Prozent des Unterschiedsbetrages steuerfrei oder dürfen nicht bei der Ermittlung der Einkünfte abgezogen werden, soweit der Unterschiedsbetrag aus Investmenterträgen stammt"*; DEVK adds the transitional limb, that the investment income must have arisen after 31 December 2017 [S2]. The 15 % tag is removed. The accumulation-phase point — no annual taxation of fund income, no *Vorabpauschale*, no taxable disposal on a *Fondswechsel* — is **not** in this section and keeps its tag; it is an absence, and an absence cannot be quoted.

(delib-fondsgebundene_rentenversicherung-r21)=

### R21 — InvStG — *Investmentsteuergesetz* and the *Teilfreistellung*
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/invstg_2018/` — the table-of-contents page (18.4 kB), which confirms the Act's structure and section headings
- Retrieved: **no** — only the contents page was opened; **no section of the InvStG was read**, so nothing substantive rests on this entry
- Used for: nothing quantitative, and **less than it used to claim**. The 15 % figure the specification quotes is **not derived from the InvStG at all**: it is enacted directly in EStG § 20 Abs. 1 Nr. 6 Satz 9 as the insurance-wrapper analogue of the fund-level *Teilfreistellung*, and that is where [R20] now cites it. This entry survives as the pointer to the 2018 regime the analogue was modelled on — the fund taxed on certain German income, the investor compensated by a partial exemption graded by equity quota. **All InvStG percentages, thresholds and the interaction with the insurance wrapper remain `[unverified]`.**

(delib-fondsgebundene_rentenversicherung-r22)=

### R22 — The *Rentenfaktor* / *Treuhänderklausel* cluster (consumer and trade press, LG Köln)
- Publisher: Finanztip; versicherungenmitkopf.de; Versicherungswirtschaft-heute
- URLs: `https://www.finanztip.de/private-rentenversicherung/rentenfaktor/` (now titled *"Urteil zum Rentenfaktor: Rentenkürzung verhindern"*) · `https://www.versicherungenmitkopf.de/treuhaenderklausel-rentenversicherung` · `https://www.versicherungenmitkopf.de/rentenversicherung/rentenfaktor`
- Retrieved: **yes** (all three, HTML, read 2026-08-30)
- Used for: **the consumer definition the whole conversion section is built on** — the *Rentenfaktor* as the monthly annuity per 10 000 € of capital; versicherungenmitkopf's worked example is *"bei einem Rentenfaktor von 25 eine monatliche Rente von 25 Euro je 10.000 Euro Fondsguthaben"*, and Finanztip's uses 30 against 20. **They remain teaching examples**, which is the status the `[std]` 25,00 carries — though note that delib's 25,00 is close to a real guaranteed factor at short deferments and well above one at long ones [S15]. Three things this entry could not previously supply and now can:
  - **The docket the library said it could not establish.** *"Zuvor hatte das Landgericht Köln in einem ähnlichen Fall gegen die Zurich geurteilt (08.02.2023, Az. 26 O 12/22) … Das Gericht entschied zudem, dass die Zurich die Niedrigzinsphase nicht als Argument für die Herabsetzung von Rentenfaktoren heranziehen darf. Das Urteil ist rechtskräftig."* **LG Köln, Urteil vom 8. Februar 2023, Az. 26 O 12/22**, against Zurich [S4]. Finanztip also names **AG Reinbek, 10.07.2024, Az. 14 C 473/23** against Allianz. The statement in the specification that no reference could be established is withdrawn.
  - **The BGH decision, with the clause it struck down.** IV ZR 34/25 of 10 December 2025 concerned a fondsgebundene **Riester**-Rentenversicherung of the Allianz — a detail the specification did not have — and the void clause reads: *"Wenn aufgrund von Umständen, die bei Vertragsabschluss nicht vorhersehbar waren, die Lebenserwartung der Versicherten sich so stark erhöht oder die Rendite der Kapitalanlagen … nicht nur vorübergehend so stark sinken sollte, dass die in Satz 1 genannten Rechnungsgrundlagen voraussichtlich nicht mehr ausreichen, um unsere Rentenzahlungen auf Dauer zu sichern, sind wir berechtigt, die monatliche Rente für je 10.000 Euro Policenwert so weit herabzusetzen, dass wir die Rentenzahlung bis zu Ihrem Tode garantieren können."* Allianz is reported to have used it in fondsgebundene contracts **concluded before 2007**, replacing it thereafter with a clause providing for an increase in better conditions. Reported reductions: Allianz 2017, 700 000 contracts from July 2001–December 2011; Allianz 2021, a **9 %** cut across tariffs *Invest*, *InvestGarantie*, *Invest alpha-Balance*, *IndexSelect* and the index and portfolio policies; AXA 2017, about 100 000 contracts; R+V 2017, about 4 000; also VHV and Zurich. Consumer bodies warned AXA and LPV in January 2024.
  - **The shape of a guaranteed factor against a current one.** versicherungenmitkopf: *"Es gibt viele Versicherer, die nur 50% oder 70% des Rentenfaktors garantieren"*, and Finanztip's illustration pairs a current 30 with a guaranteed 15. delib's base run sets the current factor **equal** to the guaranteed one, which is the conservative end of that spread and is a `[std]` choice, not an observation. The same page gives the *Abrufphase* answer the specification could not find: *"Verlegst Du den Beginn der Rentenauszahlung, kann der Versicherer im Rahmen der Neuberechnung Deiner Rente den garantierten Rentenfaktor ändern. Dieser gilt nämlich nur für das in Deinem Vertrag ursprünglich festgelegte Ablaufdatum."*
  These are **consumer and trade sources, not primary law**; the dockets they give are used as pointers to decisions, and no delib document reasons from a holding it has read in the original.

(delib-fondsgebundene_rentenversicherung-r23)=

### R23 — Rating houses and market studies: Franke und Bornberg, Morgen & Morgen, Assekurata
- Publisher: Franke und Bornberg GmbH; Morgen & Morgen GmbH; ASSEKURATA Assekuranz Rating-Agentur GmbH
- URL: not established for any fondsgebundene study. The sibling delib research corroborated the existence of Franke und Bornberg's *Rentenfaktor* and *Basisinformationsblätter* commentary and of Assekurata's 24th *Marktstudie*
- Retrieved: **no** — no address for any fondsgebundene rating study was established, so nothing was opened. The entry is kept as a known reference
- Used for: **a negative finding that this pass has partly discharged from elsewhere.** These are the houses where German unit-linked cost and *Rentenfaktor* levels are normally published, and the specification cited them to say that neither was available. **Both are now available**, from primary and supervisory sources rather than from a rating house: guaranteed *Rentenfaktoren* of 21,83–25,22 € per 10 000 € by deferment at one carrier [S15], and an *Effektivkosten* distribution across the market at delib's own model point [R11]. What this entry still stands for is that **no rating-house figure of any kind is used anywhere in these documents**, and for the market fact that German AVB are structurally interchangeable because they follow the GDV skeleton [S1] — a claim the DEVK wording is consistent with but cannot establish on its own.

(delib-fondsgebundene_rentenversicherung-r24)=

### R24 — Consumer bodies and comparison portals
- Publisher: Stiftung Warentest (*Finanztest*); Verbraucherzentrale Bundesverband and the *Länder* *Verbraucherzentralen*; Verivox; CHECK24; Finanztip
- URL: not established for any fondsgebundene Rentenversicherung page other than the Finanztip *Rentenfaktor* page already carried at [R22]
- Retrieved: **no** — apart from the Finanztip page at [R22], no consumer-body or comparison-portal page for this product was opened. The entry is kept as a known reference
- Used for: the same finding as [R23], with the same qualification. **One consumer source is now retrieved and cited** — Finanztip, at [R22], for the *Rentenfaktor* dockets and the guaranteed-versus-current spread. Everything else remains uncited: no monthly premium, no *Effektivkostenquote*, no tariff comparison at a stated model point comes from a portal or a consumer body. It remains one of the two references behind the statement that `reduction_in_yield()` **must never be quoted as a market figure** — a statement that matters more now, not less, because a real market distribution is finally available to be confused with it [R11].

(delib-fondsgebundene_rentenversicherung-r25)=

### R25 — GDV statistics on German life new business and in-force by *Versicherungsart*
- Publisher: Gesamtverband der Deutschen Versicherer e. V.
- URL: not established. The sibling delib research corroborated the existence of the series "Die deutsche Lebensversicherung in Zahlen" and "Neugeschäft und Bestand der Lebensversicherer für die letzten zehn Geschäftsjahre"
- Retrieved: **no** — no address for a GDV new-business breakdown by *Versicherungsart* was established, so nothing was opened. The entry is kept as a known reference
- Used for: the series that **would** establish the share of German life new business written as fondsgebundene Rentenversicherung. **The claim it was standing in for no longer needs it**: BaFin states that fondsgebundene products dominate new business, and gives the market's size — about 59 million *kapitalbildende* contracts in force in 2024 and 2,4 million written that year [R11]. The `[unverified]` tag on the dominance claim is removed and the claim is attributed to BaFin. What is still missing, and what only this series would give, is the **split by *Versicherungsart* and the share expressed as a number**; **no such number is taken from this entry.**

(delib-fondsgebundene_rentenversicherung-r26)=

### R26 — BGH case law on *Rückkaufswert*, *Kostenverrechnung* and *Stornoabzug*
- Publisher: Bundesgerichtshof
- URL: not established. **No case number, decision date or docket is given for any *Rückkaufswert* decision in this entry**
- Retrieved: **no** — no BGH decision was retrieved from any source; the entry is kept as a known reference
- Used for: recording that a long and well-known German line of authority exists — on *Zillmerung*, on the transparency of *Rückkaufswert* clauses before the VVG 2008 reform, on the validity of *Stornoabzug* clauses, and on the post-2008 rules — and that **no decision from it is cited**. The position is unchanged for the *Rückkaufswert* line. It has changed for the *Rentenfaktor* line, which is [R22]'s and [REG-R36]'s: **BGH 10 December 2025 — IV ZR 34/25** and **LG Köln 8 February 2023 — 26 O 12/22** are now cited with dockets, from consumer reporting rather than from the decisions themselves. Any statement in these documents about what a court has held is therefore attributed to that reporting, **no delib document reasons from a holding it has read in the original, and nothing in the model rests on a court holding.**

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen;
research provenance in `_research/regulatory-actuarial.md`). That library is upgraded on its own
schedule and its entries are **not** re-adjudicated here; what follows is this product's gloss on
each, and where a document read for *this* file corrects a gloss, the correction is made and
marked. Four are corrected below — REG-R5, REG-R7, REG-R25 and REG-R48 — on the authority of
statutes and a carrier wording read on 2026-08-30. Entries cited by the fondsgebundene
Rentenversicherung documents:

- **REG-R1** — Richtlinie 2009/138/EG (Solvabilität II): the frame in which the projected cash flows would be discounted, and the statement that this library does not discount.
- **REG-R2** — Delegierte Verordnung (EU) 2015/35: contract boundaries and the standard formula, referenced and never applied.
- **REG-R3** — Richtlinie (EU) 2025/2, the Solvency II review: recorded as a live change to the valuation frame.
- **REG-R4** — EIOPA risk-free term structures, the UFR and the *Volatilitätsanpassung*: the curve a valuation layer would supply to `liability_cf`.
- **REG-R5** — VAG 2016 and Anlage 1: **"Fondsgebundene Lebensversicherung", Nr. 21 of Anlage 1, a *Sparte* of its own**, which is why German statistics report it separately. *Corrected 2026-08-30 against the canonical VAG text: the *Sparte* is not named "fonds- und indexgebundene Lebensversicherung", and index-linked business has no separate line in Anlage 1.*
- **REG-R6** — VAG §§ 74–110: best estimate plus risk margin, and the shape of the liability this model's output feeds.
- **REG-R7** — VAG §§ 124 and 125, the *Anlagestock*: **the asset-congruence rule that removes the investment-mismatch term from the model.** *Corrected 2026-08-30: § 125 Abs. 5 makes the *Anlagestock* "eine Abteilung des Sicherungsvermögens" — a ring-fenced division **within** the *Sicherungsvermögen*, not an asset pool held outside it. The congruence duty is § 124 Abs. 2 Satz 2 Nr. 1, and § 124 Abs. 2 Satz 2 Nr. 3 brings the ordinary mixing rules back for the assets covering any guarantee.*
- **REG-R8** — VAG § 138, *Prämienkalkulation* and *Gleichbehandlung*: the pricing frame the charge stack sits in.
- **REG-R9** — VAG § 139, *Überschussbeteiligung*: with [R5], why an FRV's surplus is a risk-and-cost result only.
- **REG-R11** — VAG §§ 141–143, *Verantwortlicher Aktuar* and *Treuhänder*: the office behind the § 163 adjustment route.
- **REG-R14** — DeckRV and its § 2, the *Höchstrechnungszins*: the rate that does **not** bind this product's accumulation phase.
- **REG-R15** — the *Höchstrechnungszins* rate history: the low-interest decade that unit-linked new business grew through.
- **REG-R16** — **DeckRV § 4, the *Höchstzillmersätze*: the cross-product carrier of the 25 ‰ cap that `alpha_rate` takes.**
- **REG-R17** — DeckRV § 5 Abs. 3, the *Zinszusatzreserve*: a general-account mechanic this product does not have, recorded to say so.
- **REG-R18** — MindZV: with [R14], the minimum allocation of the risk and cost results.
- **REG-R20** — LVRG 2014: the cross-product carrier of the 40 ‰ → 25 ‰ cut and the *Effektivkosten* introduction.
- **REG-R23** — VVG §§ 8 and 152, the *Widerrufsrechte*: the 30-day window absorbed into the year-1 lapse rate.
- **REG-R24** — VVG § 153: the cross-product carrier of the *Überschussbeteiligung* entitlement.
- **REG-R25** — VVG §§ 154 and 155, *Modellrechnung* and *Standmitteilung*: what an in-force policy must be told, which is [S17]'s statutory basis. *Corrected 2026-08-30 — and this is the correction with the most bite for this product.* **§ 154 Abs. 1 Satz 2 excludes it**: the *Modellrechnung* duty *"gilt nicht für Risikoversicherungen und Verträge, die Leistungen der in § 124 Absatz 2 Satz 2 des Versicherungsaufsichtsgesetzes bezeichneten Art vorsehen"* — the same formula § 169 Abs. 4 uses for unit-linked business. **A fondsgebundene Rentenversicherung owes no three-rate *Modellrechnung* at all**; the *Basisinformationsblatt* is what a prospective policyholder gets instead [S15]. § 155 does apply, and its item list is set out at [S17].
- **REG-R27** — VVG § 163, *Prämien- und Leistungsänderung*: the only route by which a guaranteed *Rentenfaktor* may now be reduced.
- **REG-R28** — **VVG §§ 165–170: the cross-product carrier of the *Zeitwert* branch, the five-year spreading, the *Kündigung* right and the *Stornoabzug* conditions.**
- **REG-R31** — VVG §§ 6, 7 and the VVG-InfoV: advice, information, cost disclosure and the *Effektivkosten*.
- **REG-R32** — **PRIIPs and the delegated technical standards: why the TER is a return item and why nothing here may be compared with a performance scenario.**
- **REG-R33** — IDD and § 34d GewO: the inducement rules behind the *Kickback* question.
- **REG-R34** — Unisex, EuGH C-236/09 (Test-Achats) and the AGG: why `sex` reaches neither the tariff nor the *Rentenfaktor*.
- **REG-R35** — BaFin Merkblatt 01/2023, *angemessener Kundennutzen*: the cross-product carrier of the supervisory cost agenda.
- **REG-R36** — the BGH line of authority: the cross-product carrier for the *Stornoabzug* prohibition, cited without a docket, and for **BGH 10 December 2025 — IV ZR 34/25**, which voids an asymmetric *Rentenfaktor*-Anpassungsklausel under § 308 Nr. 4 BGB and § 307 Abs. 1 Satz 1 BGB and is the authority for this model's fixed guaranteed *Rentenfaktor*.
- **REG-R37** — GDV-Musterbedingungen and market practice: why insurer wordings are structurally interchangeable.
- **REG-R41** — EStG § 22 and § 55 EStDV, *Ertragsanteil*: the payout-phase tax treatment the *Kapitalwahlrecht* is compared against.
- **REG-R45** — **EStG § 20 Abs. 1 Nr. 6, the 12/62 rule: the reference library's statement that the tax threshold is the strongest single driver of German surrender behaviour, which is why `lapse_tax_step` exists.**
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*: the first-order / second-order distinction that makes the *Risikoergebnis* a number rather than zero.
- **REG-R48** — **DAV 2008 T: a death basis for German life business, cited and not shipped.** *Corrected 2026-08-30: the only fondsgebundene tariff whose bases could be read prices its *Risikobeitrag* on a unisex order at 65 % of **DAV 1994 T**, and uses DAV 2008 T for an underwritten *Risiko-Zusatzversicherung* instead [S2]. The two-table structure holds; the identification of the death table does not.*
- **REG-R49** — **DAV 2004 R: the generational annuity basis behind the *Rentenfaktor*, cited and not shipped.**
- **REG-R52** — Destatis *Sterbetafeln* and the reuse licence: the intended base for a user-supplied replacement decrement table, and the reason a population proxy overstates insured-lives claims.
- **REG-R53** — the German life market in numbers: the series that would size the unit-linked segment, and does not.
- **REG-R54** — HGB §§ 341–341o and RechVersV: the statutory-accounts layer this projection feeds and does not compute.
- **REG-R55** — IFRS 17 and the **Variable Fee Approach**: the measurement model a unit-linked contract falls into, referenced and not implemented.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional-standards frame.

---

## Provenance note

Extraction details — which fact was read from which document, the eighteen-section mechanics
account written from the author's knowledge of German practice, and the twenty-eight-item gaps
and caveats register — live in `_research/fondsgebundene_rentenversicherung.md`. That file is
the citation ground truth for the S# and R# numbering used here.

The caveats that most affect what these product documents can claim, restated after the
provenance pass of 2026-08-30, in the order they bite.

**What is now settled.** One full German unit-linked *Bedingungswerk* has been read end to end
[S2], and with it the product's own *Basisinformationsblätter* [S15]; fifteen statutory
sections have been read in the canonical text rather than cited from memory; and BaFin's cost
survey supplies a market distribution at delib's own model point [R11]. The consequences: the
*Beitragsrückgewähr* death benefit, the `max(guaranteed, current)` factor rule, the
*Beitragsverrechnung* split, the *Zeitwert* *Rückkaufswert* and the decay of a paid-up contract
are **read in a real wording**, not inferred; the *Zeitwert* branch is **§ 169 Abs. 4**, the
five-year rule **Abs. 3** and the *Stornoabzug* conditions **Abs. 5**; the MindZV percentages
are 90 / 90 / 50; the *Teilfreistellung* is 15 % under EStG § 20 Abs. 1 Nr. 6 Satz 9; the
12/62 rule is confirmed with its § 52 transitional; the 30-day *Widerruf* is § 152 Abs. 1;
the LG Köln docket is **26 O 12/22**; and a real guaranteed *Rentenfaktor* at delib's anchor
cell is **22,91 €** per 10 000 €.

**What is still open, and what changed under the library's feet.** **The charge levels of ten
of the eleven named carriers are still unestablished**, and the one carrier that could be read
publishes its rates only in the *Basisinformationsblatt*, not in the AVB — so the stack is
still `[std]`, though it is now `[std]` *with a comparator* rather than `[std]` in the dark.
**No lapse rate, paid-up rate or *Kapitalwahlrecht* take-up was established**, so every
behavioural assumption remains `[std]`; the nearest thing to evidence is BaFin's remark that a
material share of a target market terminates early [R10] [R11]. **The DAV tables are cited and
never shipped**, so both mortality bases in the model are still `[std]` proxies — and the
*death* table delib names is now known to be the wrong one at the carrier that could be checked
[R17]. **No GDV new-business split by *Versicherungsart* was obtained** [R25], though the
dominance claim no longer needs one [R11]. **The BGH *Rückkaufswert* line is still uncited**
and no delib document reasons from a holding it has read in the original [R26]. And **every
statute cited is a living text**: the VVG read here carries *Stand* 26 May 2026, the DeckRV
19 July 2024, the MindZV 7 July 2020, and the PRIIPs RTS has been amended at least twice
(2019/1866, 2021/2268) — so every paragraph number and date should still be re-checked against
the instrument, but it can now be re-checked against a text this library has actually opened.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-fondsgebundene_rentenversicherung-r1
[R10]: #delib-fondsgebundene_rentenversicherung-r10
[R11]: #delib-fondsgebundene_rentenversicherung-r11
[R12]: #delib-fondsgebundene_rentenversicherung-r12
[R13]: #delib-fondsgebundene_rentenversicherung-r13
[R14]: #delib-fondsgebundene_rentenversicherung-r14
[R15]: #delib-fondsgebundene_rentenversicherung-r15
[R16]: #delib-fondsgebundene_rentenversicherung-r16
[R17]: #delib-fondsgebundene_rentenversicherung-r17
[R18]: #delib-fondsgebundene_rentenversicherung-r18
[R19]: #delib-fondsgebundene_rentenversicherung-r19
[R20]: #delib-fondsgebundene_rentenversicherung-r20
[R21]: #delib-fondsgebundene_rentenversicherung-r21
[R22]: #delib-fondsgebundene_rentenversicherung-r22
[R23]: #delib-fondsgebundene_rentenversicherung-r23
[R24]: #delib-fondsgebundene_rentenversicherung-r24
[R25]: #delib-fondsgebundene_rentenversicherung-r25
[R26]: #delib-fondsgebundene_rentenversicherung-r26
[R3]: #delib-fondsgebundene_rentenversicherung-r3
[R5]: #delib-fondsgebundene_rentenversicherung-r5
[R6]: #delib-fondsgebundene_rentenversicherung-r6
[R7]: #delib-fondsgebundene_rentenversicherung-r7
[R8]: #delib-fondsgebundene_rentenversicherung-r8
[R9]: #delib-fondsgebundene_rentenversicherung-r9
[REG-R25]: #delib-reg-r25
[REG-R36]: #delib-reg-r36
[REG-R5]: #delib-reg-r5
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
