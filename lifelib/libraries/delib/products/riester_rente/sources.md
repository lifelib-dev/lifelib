# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/riester_rente.md` (the citation ground
truth for this product) and are **frozen — never renumber**. Unused sources are omitted, so the
numbering has a gap: **R27** (the consumer, comparison and rating cluster — Stiftung Warentest /
*Finanztest*, Finanztip, the *Verbraucherzentralen*, Verivox, Check24, Handelsblatt, Morgen &
Morgen, Franke und Bornberg, Assekurata) is **not cited** by `product-spec.md` or
`technical-notes.md` and is therefore absent below. Its absence is itself the finding: that cluster
is where a normal research pass would have found the *Effektivkosten* comparisons, the
*Rentenfaktor* tables and the observed carrier spread a representative composite is built from,
**nothing from any of them was established**, and everything it would have supplied is instead a
**[std]** standardization with a stated rationale. Every other id in the research file — **S1–S16**
and **R1–R26** — is cited. Access date for all sources: **2026-08-29**. No sources were newly added
at drafting. Cross-product [REG-R#] tags are listed in their own section at the end.

**Retrieval conditions — read this before relying on a single line below.** This library was
*drafted* under one set of conditions and *verified* under another, and a reader who picks up this
file alone has to learn both from it.

**1. How it was drafted: with no research channel at all.** Direct HTTP egress was blocked by an
organisation network policy — `WebFetch` and `curl` were refused with HTTP 403 at the egress gateway
for every host outside a short package-registry allowlist, and every host that matters for this
product was tried and refused: `gesetze-im-internet.de` (the AltZertG and the EStG),
`bundesfinanzministerium.de` (the BMF *Anwendungsschreiben* and the *Fokusgruppe* report), `bmas.de`
(the quarterly Riester contract statistics), `deutsche-rentenversicherung.de` (the ZfA), `bzst.de`
(the certifying authority), `bafin.de`, `gdv.de`, `aktuar.de`, `destatis.de`, `dejure.org`,
`de.wikipedia.org`, and every insurer, fund-house and bank host named below. The session's
`WebSearch` budget — 200 calls, shared across the parallel delib researchers — was exhausted before
this product's research file was begun, so every search attempted for this product returned the
budget-exhausted message. The first draft therefore rested on the authoring model's own knowledge of
German pension and insurance law, disciplined by tagging every specific number **[std]** or
`[unverified]`, plus four items inherited from a **sibling delib research session's** searches which
say so at the point of use — the GDV *Musterbedingungen* index and its taxonomy [S3], the
"Stand: 21.07.2025" date line on the classic Riester model wording [S2], the CosmosDirekt tariff code
**LA 1005 A** [S4], and a third-party cost figure on an Allianz specimen quotation [S5]. **That
account is provenance and is kept here deliberately.** It is no longer the retrieval condition.

**2. How it was verified: against the primary documents.** The egress policy has since been lifted
and the citations re-checked. Across delib, all fifteen German instruments the library cites were
read as canonical XML from `gesetze-im-internet.de` with each law's amendment status (*Stand*)
recorded; 950 statutory section references were checked and 950 were correct; and insurer *AVB*,
*Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read. **Across
the library, 501 of 805 source entries — 62 % — now record `Retrieved: yes`.** This file sits at the
same proportion: of the **42 entries below, 26 record `Retrieved: yes` (62 %)**, two are
part-retrieved [R23] [R26], and **14 remain `Retrieved: no`**.

**What the fourteen are.** None of them is a paywall, a subscription login or a consent wall. Every
one is a document that could not be **located**, or that has no single identifiable text to fetch:
six carrier, fund, bank and *Wohn-Riester* wordings that were not found on their publisher's own
site [S5] [S7] [S8] [S11] [S12] [S13], and one second-tier insurer list with no single document
behind it to fetch [S16]; five *Bundesgesetzblatt* amending acts whose effect is
visible in the consolidated statutes but whose own text was not opened [R17]–[R21]; and the BMF
*Anwendungsschreiben* [R24] and the Riester contract statistics [R25], neither identified. Each entry
says so in its own words.

**What follows from that, entry by entry.** A `Retrieved: yes` entry means **the document was opened
and the passage the entry rests on was read**; it records the form, the size or page count, the
edition line or *Stand*, and the read date. A `Retrieved: no` entry is still **a pointer, not a
certificate** — it names the instrument a claim should be checked against and does not assert that
anyone checked it — and it is marked as one at the point of use. Nothing is guessed either way: where
no URL, document number, edition or *Zertifizierungsnummer* is available the entry says `URL: not
established`. Verbatim quotation is now given where a retrieved document supports it; German phrases
in quotation marks in an unretrieved entry are **terms of art**, not quotations. And `[unverified]`
keeps its meaning in the product documents, over a much smaller set than before: it now marks the
carrier levels, the market figures, the behavioural rates and the historic dates and vintages that
this pass could not corroborate against a document, rather than every number on the page. **Treat a
claim as sound where its entry says `Retrieved: yes`, and as provisional where it does not.**

---

## Primary product sources

Sixteen known references in four families: the **GDV model conditions** [S1]–[S3]; the **insurance
wordings** [S4]–[S8] and [S16], which are the product this model represents; the **fund and bank
wordings** [S9]–[S12], the same subsidy on a different chassis; and the **Wohn-Riester** documents
[S13], the boundary of scope. [S14] and [S15] are the statutory disclosure and certification
artefacts every one of the others carries. They are listed because a source list's job is to name
the documents a downstream claim must be checked against, and because the *kinds* of document that
exist here are themselves a finding: German Riester disclosure is split across four — the **AVB**,
the **Produktinformationsblatt**, the **Verbraucherinformation** pack and the **jährliche
Information**.

(delib-riester_rente-s1)=

### S1 — GDV, "Allgemeine Bedingungen für eine fondsgebundene Rentenversicherung mit Auszahlung des Deckungskapitals bei Tod als Altersvorsorgevertrag im Sinne des Altersvorsorgeverträge-Zertifizierungsgesetzes (AltZertG)" (Musterbedingungen)
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin; *Musterbedingungen* — model general policy conditions for a **unit-linked** Riester annuity, non-binding and optional in use
- URL: https://www.gdv.de/resource/blob/6298/8acd0b619708f236dcdea9bc74fd49a0/allgemeine-bedingungen-fuer-eine-fondsgebundene-rentenversicherung-mit-auszahlung-des-deckungskapitals-bei-tod-als-altersvorsorgevertrag-im-sinne-des-altersvorsorgevertraege-zertifizierungsgesetzes-a-0-pdf-data.pdf — reached from the GDV index [S3], which links it directly
- Retrieved: yes (PDF, 27 pp., "Stand: 21.07.2025", read 2026-08-30)
- Used for: the proposition in `product-spec.md` that the association drafts an AltZertG condition set for the **unit-linked** wrapper, which places the *fondsgebundene* Riester chassis outside this model and inside `fondsgebundene_rentenversicherung`; and, in the four-chassis table, the identification of the unit-linked form's provider and guarantee mechanism. **The title carried here before this pass was wrong**: the document is not "…nach dem AltZertG" but "…mit Auszahlung des Deckungskapitals bei Tod als Altersvorsorgevertrag im Sinne des AltZertG", and the death benefit is therefore named in the title. On the guarantee mechanism the document is now explicit and **narrower than the four-chassis table assumed**: § 1 Abs. 1 provides that "Zur Sicherstellung der Beitragserhaltungsgarantie (siehe § 2 Absatz 11) werden Beitrags- und Zulagenteile in unserem sonstigen Vermögen angelegt (Garantie-Deckungskapital)", and at *Rentenzahlungsbeginn* the units are taken out of the *Anlagestock* and their value invested in the general account. That is the **static two-pot** design, not a rebalancing algorithm; i-CPPI and the *dynamisches Hybridmodell* are carrier variants the model wording does not describe. The *Beitragserhaltungsgarantie* itself (§ 2 Abs. 11) is worded **identically** to the classic set [S2]

(delib-riester_rente-s2)=

### S2 — GDV, non-unit-linked ("klassische") Riester model conditions, "Stand: 21.07.2025"
- Publisher / doc type: GDV; *Musterbedingungen* for the **general-account** variant of the same AltZertG wrapper — the direct template for the product this model represents. Full title: "Allgemeine Bedingungen für eine Rentenversicherung mit Auszahlung des Deckungskapitals bei Tod als Altersvorsorgevertrag im Sinne des Altersvorsorgeverträge-Zertifizierungsgesetzes (AltZertG)"
- URL: https://www.gdv.de/resource/blob/6300/691e8381e0a6dce802c80f64ce78ef0f/allgemeine-bedingungen-fur-eine-rentenversicherung-mit-auszahlung-des-deckungskapitals-bei-tod-als-altersvorsorgevertrag-im-sinne-des-altersvorsorgevertrage-zertifizierungsgesetzes-0-pdf-data.pdf — reached from the GDV index [S3], which links it directly
- Retrieved: yes (PDF, 25 pp., 20 §§, "Stand: 21.07.2025" on page 1, read 2026-08-30). The date the library carried on a sibling session's authority is now read off the document itself
- Used for: **the single most productive document in this product's corpus, and the one that turns the composite's carrier half from assertion into evidence.** It carries the two propositions of the product spec's overview it always carried — that the classic Riester chassis was still being drafted by the industry association **after** the *Höchstrechnungszins* rose to 1,00 % on 1 January 2025 [R22], and that the classic and unit-linked wrappers are **separate condition sets** [S1]. Beyond that it now establishes clause content the library previously marked unestablished:
  - **the *Beitragserhaltungsgarantie*, verbatim** (§ 1 Abs. 10): "Wir garantieren, dass zum Rentenzahlungsbeginn (Beginn der Auszahlungsphase) mindestens die bis dahin gezahlten Beiträge und die uns zugeflossenen staatlichen Zulagen für die vereinbarten Leistungen zur Verfügung stehen." The guarantee therefore covers own contributions **and** Zulagen — a proposition the product documents carried as `[unverified]` and can now state as read — and § 12 Abs. 5 adds that it "gilt auch bei einer Beitragsfreistellung". It is **reduced** by an *Eigenheimbetrag* withdrawal or a *Versorgungsausgleich* deduction, which the library did not record;
  - **the 20 % biometric carve-out, in the insurer's own words**: "werden wir die auf die Deckung dieses Risikos entfallenden Beiträge von der Garantie abziehen, höchstens jedoch 20 % der Gesamtbeiträge";
  - **the death benefit** (§ 1 Abs. 6): "Wenn Sie vor dem Rentenzahlungsbeginn sterben, zahlen wir das Deckungskapital. Das Deckungskapital bilden wir, indem wir die gezahlten Beiträge und die uns zugeflossenen staatlichen Zulagen abzüglich der tariflichen Kosten mit dem Rechnungszins (Absatz 11) verzinsen." The composite's **[std]** choice of the accumulated capital as the death benefit is the model wording's own choice, and is named in the document's title;
  - **the charge base for the Zulagen** (§ 13 Abs. 2 and 3) — the permitted forms include "eines festen Prozentsatzes jedes gezahlten Beitrags sowie jeder Zulage und Zuzahlung" and "der vereinbarten Beitragssumme einschließlich Zulagen und Zuzahlung", and acquisition costs on a Zulage are taken **once at inflow** rather than spread: "Von Zulagen und Zuzahlungen ziehen wir die Abschluss- und Vertriebskosten jeweils einmalig zum Zeitpunkt des Zuflusses ab." This closes gap 14 at the model-wording level;
  - **the *Kleinbetragsrenten-Abfindung* as the provider's right** (§ 1 Abs. 3) — "können wir die Rente … abfinden" — with the four-week deferral election to 1 January of the following year, aggregation across all of the saver's contracts at that provider, and, **against the composite's ordering choice**, "Eine Abfindung erfolgt nicht, wenn die Leistung nur aufgrund einer Teilkapitalauszahlung gemäß Absatz 4 auf eine Kleinbetragsrente sinkt";
  - **the *Wechsel* notice period** (§ 11 Abs. 1): three months to the end of a calendar quarter or to the start of the payout phase, shortened to 14 days where the provider gave the pre-payout information late — closing the first limb of gap 8;
  - **the *Rentengarantiezeit*** as a drafted option with a **ten-year** worked example (§ 1 Abs. 7), which is the length the composite standardizes on;
  - and, negatively but importantly, **no *Rentenfaktor* anywhere in the document**. The annuity is agreed at inception on a *Sterbetafel* and *Rechnungszins* left blank for the carrier (§ 1 Abs. 11), and each Zulage buys an increment "nach … dem bei Abschluss des Vertrages gültigen Tarif" (§ 9). *Rechnungszins*, *Sterbetafel*, *Stornoabzug* (§ 10 Abs. 4), the acquisition-cost spreading period and every charge level are company-individual blanks, which is why the composite's carrier parameters remain **[std]** even now

(delib-riester_rente-s3)=

### S3 — GDV, "Musterbedingungen" service index
- Publisher / doc type: GDV; publisher index page listing the association's model-condition sets
- URL: https://www.gdv.de/gdv/service/musterbedingungen
- Retrieved: yes (HTML, 93.8 kB, read 2026-08-30; it is the page that carries the download links to [S1] and [S2])
- Used for: the German product taxonomy used in the scope notes of `product-spec.md` and `technical-notes.md`. The index confirms the taxonomy and **extends it**: under *Rentenversicherungen* it lists model conditions for the deferred annuity, the *Basisrente-Alter*, the immediate annuity, the fondsgebundene annuity, and **three** AltZertG sets — the deferred general-account one [S2], the deferred unit-linked one [S1] and one for a "Rentenversicherung mit sofort beginnender Rentenzahlung im Sinne des AltZertG", which the library had not recorded and which is the *Restverrentung* wrapper the fund chassis buys into. It lists *Hinterbliebenenrenten-Zusatzversicherung* sets for each of the three annuity forms, confirming the rider as a separate condition set. On the naming point the index is more precise than the library was: the **AVB** name the product by its certification statute ("als Altersvorsorgevertrag im Sinne des AltZertG"), while the two *Muster-Standmitteilungen* on the same page are named "Riester-Rentenversicherung (klassisch)" and "(hybrid)" — so the association uses the popular name for the annual statement and the statutory one for the contract terms. The page carries the disclaimer that the conditions "sind für die Versicherungsunternehmen unverbindlich. Die Verwendung ist rein fakultativ."

(delib-riester_rente-s4)=

### S4 — Cosmos Lebensversicherungs-AG (CosmosDirekt), Riester-Rentenversicherung AVB, document **LA 1005 A**, tariff **R1-A**
- Publisher / doc type: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland; "Allgemeine Bedingungen für eine Rentenversicherung mit staatlicher Förderung im Sinne des Altersvorsorgeverträge-Zertifizierungsgesetzes (AltZertG)"
- URL: https://www.cosmosdirekt.de/resource/blob/89126/787fd9133f3dd23ca956cbbbb3cf0195/allgemeine-bedingungen-riester-rente-la-1005-a--data.pdf
- Retrieved: yes (PDF, 7 pp., 19 §§, edition line "LA 1005 A (01.15)", read 2026-08-30). The companion specimen *Produktinformationsblatt* [S14] was retrieved with it
- Used for: the carrier facts in the product spec's variation section. **One correction to what the library carried**: LA 1005 A is the **conditions document number**, not the tariff code — the PIB says "Ihrer Berechnung liegt eine Klassische Riester-Rente nach **Tarif R1-A** zugrunde". The separation of the Riester wording from the house's Schicht-3 (LA 904 A) and *Basisrente* (LA 1100 A) series stands and is confirmed by the document numbering. Newly established from the clause text, all of it carrier-specific and none of it previously in this library:
  - a real ***Rechnungszins***, § 1 Abs. 2: the *Deckungskapital* is formed by accumulating "die eingezahlten Beiträge und die uns zugeflossenen staatlichen Zulagen abzüglich der tariflichen Kosten mit dem tariflichen **Garantiesatz von 1,25 Prozent p. a.**" — the *Höchstzinssatz* in force for the 01.15 vintage, so this house took the cap;
  - **a complete numbered charge basis** (§ 11): *Abschluss- und Vertriebskosten* of "**1,0 Prozent** der insgesamt … zu zahlenden **Eigenbeiträge**", spread in equal annual amounts over at least the first five contract years; *Verwaltungskosten* of "**2,1 Prozent** eines jeden Eigenbeitrags, von 2,1 Prozent des bei einer Übertragung ggf. eingehenden Kapitals sowie von **6,0 Prozent einer jeden Zuzahlung bzw. staatlichen Zulage**"; a fractionation loading adding **3,0 / 2,0 / 1,0** percentage points to the 2,1 % for monthly / quarterly / half-yearly payment; **0,13 Prozent** of the accumulated *Beitragssumme* taken monthly pro rata from the *Deckungskapital*, "auch bei ruhenden (beitragsfrei gestellten) Verträgen"; and a payout-phase *Verwaltungskosten-Rückstellung* of "**1,5 Prozent** des Jahresbetrags der Altersrente" for each year of payment. This is the first real charge basis in this corpus and it **closes gap 14** — the Zulagen are charged, and at nearly three times the rate applied to the *Eigenbeitrag*;
  - **no *Stornoabzug* and no transfer charge at all**: § 9 Abs. 1 "Für die Durchführung der Kündigung erheben wir keine Gebühren", and § 9 Abs. 8 "Übertragen Sie das gebildete Kapital auf einen anderen Altersvorsorgevertrag bei CosmosDirekt oder einem anderen Anbieter, entstehen Ihnen keine Kosten." The *Rückkaufswert* is the § 169 VVG *Deckungskapital* with the five-year cost spreading, plus allocated surplus and *Bewertungsreserven*, floored by a "bei Vertragsabschluss vereinbarten garantierten Rückkaufswert";
  - a ***flexible Altersgrenze* of 62 to 70** (§ 1 Abs. 6), which is a contractual answer to gap 10's question about an upper bound on the start of the payout phase; and a 100,- EUR charge on an *Altersvorsorge-Eigenheimbetrag* (§ 10);
  - **no *Rentenfaktor***, as in [S2]: the guaranteed annuity is recomputed "mit den Rechnungsgrundlagen der bei Abschluss des Vertrags gültigen Tarifkalkulation", and § 7 credits each Zulage as an increment of insured benefit on the tariff in force at conclusion. Gap 9 is therefore **answered differently by different houses** — see [S6];
  - and § 14 Abs. 2, "Die Abtretung von Forderungen und Rechten aus dem Versicherungsvertrag sowie seine Verpfändung sind ausgeschlossen", which is the contract-level counterpart of [R16]

(delib-riester_rente-s5)=

### S5 — Allianz Lebensversicherungs-AG, the *RiesterRente* product family
- Publisher / doc type: Allianz Lebensversicherungs-AG, Stuttgart; insurer product pages and the associated *Verbraucherinformation* / AVB packs. **The current product names, their tariff codes and which remain open to new business are still not established** (gap 12)
- URL: not established — no Allianz Riester AVB or *Verbraucherinformation* was located on the publisher's own site in this pass; the entry is kept as a known reference
- Retrieved: no — the document was not identified, so there was nothing to open. This is the one insurance entry in [S4]–[S8] that this pass did not advance
- Used for: the market-leader comparator in the variation section, and nothing else. **The claim this entry used to carry is now withdrawn.** It was described as the *single quantitative charge datum anywhere in this corpus* — total costs of at most **0,95 € per 100 €** of capital formed in a *RiesterRente* variant, inherited from a sibling session's search of third-party commentary on a specimen quotation, together with a **1 575 €** *Abschlussprovision* on a *BasisRente* specimen. Both remain `[unverified]` third-party commentary rather than a tariff sheet, and they are now also **superseded**: real, clause-level charge bases are in hand from [S4] and real disclosed *Effektivkosten* from [S9], so nothing in this library needs to lean on an unretrieved secondary figure. The [S5] numbers are retained here for traceability and are cited for no parameter

(delib-riester_rente-s6)=

### S6 — Debeka Lebensversicherungsverein a. G., Riester-Rentenversicherung, **B LV 94 (01.01.2025)** — ABAVV 01/2025
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., Koblenz; "Allgemeine Bedingungen für eine aufgeschobene Rentenversicherung mit Überschussverwendung Fonds als Altersvorsorgevertrag – Riester-Rente (ABAVV 01/2025)"
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/riester-rente/BLV94.pdf
- Retrieved: yes (PDF, 11 pp., edition line "B LV 94 (01.01.2025)", read 2026-08-30)
- Used for: the proposition it always carried — that a Debeka Riester wording is where the German market still writes this chassis, the house being the largest writer of classically guaranteed life business with a membership weighted to *Beamte*, who are *unmittelbar zulageberechtigt* [R7]. That proposition is now **confirmed with a document**: a Riester wording with a **1 January 2025** edition date, drafted after the *Höchstzinssatz* rose [R22]. What the clause text establishes, none of it previously in this library:
  - a ***Rechnungszins* of 0,9 Prozent p. a.** on the annuity from the originally agreed *Eigenbeiträge* and Zulagen and on the accumulation generally (§ 4 Abs. 2, § 1 Abs. 4) — a 2025-vintage tariff guaranteeing **below** the 1,00 % cap, which is the concrete case for the composite's footnoted proposition that the *Höchstzinssatz* caps the reserving rate and not what a policy may promise [REG-R14];
  - the annuitant table by name: "**UNI 2004 R**" (§ 4 Abs. 2) — the unisex application of the DAV 2004 R family [REG-R49];
  - **the two-*Rentenfaktor* construction, in a Riester wording** (§ 4 Abs. 3), which the product spec adopted as **[std]** and recorded as unestablished for any Riester tariff (gap 9): "Der garantierte Rentenfaktor gibt an, wie viel Rente wir Ihnen monatlich je 10.000 Euro Guthaben … zahlen", struck on "einen Rechnungszins von **0,1 Prozent p. a.** und die unternehmenseigene geschlechtsunabhängige Sterbetafel **Debeka 07/16 R (RF)**", compared at *Rentenbeginn* with the factor implied by the house's then-current immediate-annuity basis, and "**Die höhere Rente wird ausgezahlt (Günstigerprüfung).**" The denomination — euros of monthly annuity per 10 000 € — and the higher-of rule are exactly the model's construction, and the 0,1 % basis is the *Sicherheitsabschlag* made concrete. **Note that the factor applies only to the capital from further payments, the fund holding and further surplus**; the annuity from the originally agreed contributions and Zulagen is set on the inception basis, so the two-factor construction is a partial mechanic in this wording, not the whole conversion;
  - a real ***Stornoabzug***, and one of a shape the composite does not carry (§ 13 Abs. 5): a deduction of **0 / 5 / 10 / 15 %** of the *Deckungskapital* keyed to the excess of the current ten-year zero-coupon euro swap rate over its own ten-year average, falling linearly to zero over the last ten years of the deferral period — a market-value adjustment, not a flat percentage;
  - and the same **Zulagen-are-charged** rule as [S2] and [S4] (§ 14 Abs. 2): acquisition costs are a fixed percentage of the agreed *Beitragssumme*, of increase contributions, **and of "jeder Zulage und jeder Sonderzahlung"**, spread over **60 Monate** for the first two and taken "jeweils einmalig zum Zeitpunkt des Zuflusses" for the Zulagen. Transfers in, *Wohneigentum* repayments and *Versorgungsausgleich* capital bear no acquisition cost
  - **Charge levels remain unestablished**: the percentages themselves are tariff data outside the AVB, so no charge **level** in this library cites [S6]

(delib-riester_rente-s7)=

### S7 — R+V Lebensversicherung AG, Riester-Rentenversicherung
- Publisher / doc type: R+V Lebensversicherung AG, Wiesbaden; AVB and product documentation for a Riester annuity
- URL: not established — no R+V Riester AVB was located on the publisher's own site in this pass
- Retrieved: no — the document was not identified. The entry is kept as a known reference and cites nothing for a level
- Used for: the cooperative-sector comparator, and specifically the observation that this is the one group whose Riester offering spans an insurance and a fund chassis in the **same** distribution network as [S9] — which is why the product spec can set the two chassis side by side without comparing across distribution models. **No document, tariff code, vintage or clause is established**

(delib-riester_rente-s8)=

### S8 — Alte Leipziger Lebensversicherung a. G., Riester-Rentenversicherung
- Publisher / doc type: Alte Leipziger Lebensversicherung a. G., Oberursel; AVB and product documentation for a Riester annuity in a classic and a unit-linked form
- URL: not established — no Alte Leipziger Riester AVB was located on the publisher's own site in this pass
- Retrieved: no — the document was not identified. The entry is kept as a known reference and cites nothing for a level
- Used for: the broker-market comparator in the variation section, and for the proposition that a single house commonly writes both the classic and the unit-linked Riester form. **No document, tariff code, vintage or clause is established**; the house's product naming convention is `[unverified]` and is not reproduced. The general proposition that one house writes both forms is separately evidenced by the GDV maintaining both condition sets at the same *Stand* [S1] [S2]

(delib-riester_rente-s9)=

### S9 — Union Investment, *UniProfiRente* and *UniProfiRente Select*
- Publisher / doc type: Union Investment Privatfonds GmbH, Frankfurt am Main; the statutory *Muster-Produktinformationsblätter* [S14] for the two **Riester-Fondssparpläne** *UniProfiRente* and *UniProfiRente Select*. The *Vertragsbedingungen* themselves were not located
- URL: https://www.union-investment.de/dam/jcr:534340fa-bb8b-4c6b-8740-e8dc18bc1614/MusterPIB_PKzAU001_Lfz40.pdf (*Select*) and https://www.union-investment.de/dam/jcr:64a88f77-f232-4aec-9578-075d8e28ee43/MusterPIB_PKzQU001_Lfz40_neu.pdf (*UniProfiRente*)
- Retrieved: yes (two PDFs, 2 pp. each, the *Select* sheet dated "Stand 01.01.2022", read 2026-08-30). These are *Muster*-sheets under § 7 Abs. 4 AltZertG with the regulation's model customer, **not** individual offers
- Used for: the product spec's four-chassis table and its account of the fund chassis. Newly established, and it settles three things the library recorded as unestablished:
  - **real *Zertifizierungsnummern*** — **006403** (*UniProfiRente*) and **006407** (*UniProfiRente Select*) — the first in this library, answering [S15];
  - **real *Effektivkosten*** — **1,45 Prozentpunkte** and **1,33 Prozentpunkte** on the 40-year model case — and **real *Chancen-Risiko-Klassen*** — **CRK 4** and **CRK 2**. Both close the disclosure limb of gap 13. The CRK figures **contradict** the library's reading that a 100 %-guaranteed product sits at the low-risk end of the scale by construction: both products carry the statutory *Beitragserhaltungszusage* — the sheet says in terms "Riester-Produkte enthalten immer eine Beitragserhaltungszusage" — and one of them is nonetheless in CRK 4;
  - **a complete cost list in the § 2a AltZertG form**, including *Abschluss- und Vertriebskosten* of "insgesamt max. 1.896,50 Euro / Prozentsatz der eingezahlten Beiträge (**inkl. Zulagen**) max. 5,00 %" — a fourth independent confirmation that the Zulagen are a charge base (gap 14) — administration of 0,27–1,99 % p.a. of the capital plus 9,00 € a year, and *anlassbezogene* charges of **50,00 Euro** for "Kündigung (Vertragswechsel oder Auszahlung)", 54,00 € for a *Versorgungsausgleich* and 0,00 € for an *Eigenheimbetrag*. The 50,00 € is the same figure the model carries as its **[std]** transfer charge, and it sits well under the statutory 150 € ceiling [R1]
  - On the guarantee **mechanism** the sheet is thinner than the library assumed. It describes "ein Depotsteuerungskonzept" allocating contributions and Zulagen to "Fonds der **Sicherungskomponente** und/oder der **Chancenkomponente**" — a security and an opportunity component, not specifically "an equity fund and a bond fund". **The reallocation rule itself, the fund names and the new-business status remain unestablished** (gaps 11, 12), and the **cash-lock** characterisation is not in the document and keeps its `[unverified]` tag
  - The payout topology **is** confirmed: "Auszahlungsplan bis zum 85. Lebensjahr und ab dem 85. Lebensjahr eine lebenslange Rente", with up to 30 % taken at the start and a *Kleinbetragsrenten-Abfindung* under § 93 Abs. 3 EStG. The *Rentenfaktor* and the payout-phase costs are shown as "k. A. — Der Rentenfaktor steht noch nicht fest", which is itself the finding that on the fund chassis the conversion terms are **not** fixed at inception

(delib-riester_rente-s10)=

### S10 — DWS Investment GmbH, *DWS RiesterRente Premium* / *DWS TopRente*
- Publisher / doc type: DWS Investment GmbH (Deutsche Bank group), Frankfurt am Main; the *Muster-Produktinformationsblatt* [S14] for *DWS TopRente Dynamik*. The *Vertragsbedingungen* and the *RiesterRente Premium* documents were not located
- URL: https://www.dws.de/de-DE/AssetDownload/Index/?assetguid=d314b687-551a-4da0-b525-984c62f701c5
- Retrieved: yes (PDF, 2 pp., read 2026-08-30), but **thinly**: the sheet is a template whose CRK, *Effektivkosten* and cost figures are left blank ("in die CRK  eingeteilt"), so it establishes structure and not values
- Used for: the second of the three large Riester fund savings plans in the four-chassis table, and for the product spec's statement that the fund houses' withdrawal from sale is part of what closed the Riester market — **still not established** (gap 12). What the sheet does establish is the fund chassis's payout topology at a second house, and one fact the library did not carry: "Die Auszahlungsphase beginnt frühestens ab Ihrem 62., **spätestens ab Ihrem 83. Geburtstag**", an explicit contractual **upper** bound on the start of the payout phase, which is what gap 10 asks about. It also states that during the *Auszahlplan* to 85 the remaining capital is inheritable while the single premium set aside for the lifelong annuity is not — the fund chassis's answer to the death benefit. **No fee level, no *Effektivkosten*, no CRK and no new-business status is established**

(delib-riester_rente-s11)=

### S11 — Deka, *DekaBonusRente*
- Publisher / doc type: DekaBank Deutsche Girozentrale / Deka Investment GmbH, Frankfurt am Main; *Vertragsbedingungen* plus *Produktinformationsblatt* [S14] for a Riester-Fondssparplan
- URL: not established — no *DekaBonusRente* condition set or *Produktinformationsblatt* was located on the publisher's own site in this pass
- Retrieved: no — the document was not identified. The entry is kept as a known reference and cites nothing for a level
- Used for: the third of the three fund savings plans, distributed through the *Sparkassen*; same chassis, same guarantee problem, same caveats. **No document, edition or fee level is established.** The chassis-level propositions it supports are carried by [S9] and [S10], both of which were retrieved

(delib-riester_rente-s12)=

### S12 — Riester-Banksparplan *Vertragsbedingungen* (Sparkassen; Volks- und Raiffeisenbanken)
- Publisher / doc type: individual *Sparkassen* and cooperative banks — there is no single national product; deposit-contract terms for a certified Riester savings plan, typically a reference-rate-linked interest with a duration bonus scale
- URL: not established — there is no single national product to look for, and no individual *Sparkasse* or cooperative bank deposit-contract term set was located in this pass
- Retrieved: no — the document was not identified; the entry is kept as a known reference
- Used for: the analytical control case in the product spec's guarantee argument — the one certified chassis on which the 100 % *Beitragsgarantie* costs **nothing**, because a deposit balance cannot fall below the sum of deposits, which isolates the guarantee's cost as the **return forgone** rather than as a capital charge. **No individual product, rate scale, bonus scale or provider is established**

(delib-riester_rente-s13)=

### S13 — Wohn-Riester documents: Riester-*Bausparvertrag* and Riester-*Darlehen*
- Publisher / doc type: the *Bausparkassen* — Schwäbisch Hall, LBS, Wüstenrot, BHW and others; *Allgemeine Bedingungen für Bausparverträge* in a certified Riester form, and loan agreements certified as an *Altersvorsorgevertrag* in the form of a *Darlehen* [R3]
- URL: not established — no *Bausparkasse* Riester condition set was located in this pass
- Retrieved: no — the document was not identified; the entry is kept as a known reference. The statutory limb of the boundary is, however, now read: AltZertG § 1 Abs. 1a [R3] and EStG §§ 92a, 92b [R13] were retrieved
- Used for: the scope boundary in both product documents — that the delib model's exclusion of Wohn-Riester excludes **real, certified, subsidy-drawing products** rather than a curiosity, and that a contract counted as "Riester" in an official statistic may be a mortgage [R19], so this model's contract count is not comparable with a published one without adjustment. **No document, edition, rate or fee is established**

(delib-riester_rente-s14)=

### S14 — *Produktinformationsblatt* under § 7 AltZertG, in the form prescribed by the *Altersvorsorge-Produktinformationsblattverordnung* (AltvPIBV)
- Publisher / doc type: every certified provider must issue one; the form is prescribed by § 7 AltZertG [R4] and the AltvPIBV [R5], and the *Chancen-Risiko-Klasse* rests on a simulation procedure the *Zertifizierungsstelle* lays down and the *Produktinformationsstelle Altersvorsorge* is charged with by *Beleihung* (AltZertG § 3 Abs. 2 Satz 2 with § 3a). Standardised pre-contractual comparison sheet
- URL: three specimens were retrieved and are listed at their own entries — https://www.cosmosdirekt.de/resource/blob/89392/7134ff1643781db3cbb3b12c4fc921ad/pib-riester-rente-klassisch-data.pdf [S4], and the two Union Investment sheets at [S9]. The DWS template is at [S10]
- Retrieved: yes — four sheets, all of them ***Muster*** sheets under § 7 Abs. 4 AltZertG rather than individual offers (PDFs, 2–4 pp., read 2026-08-30)
- Used for: the product spec's charges and disclosure sections. **Most of what this entry recorded as unestablished is now read.** The *Effektivkosten* are indeed a reduction in yield computed for the individual offer — the CosmosDirekt sheet sets them out as "jährliche Wertentwicklung ohne Berücksichtigung der Kosten − jährliche Wertentwicklung unter Berücksichtigung der Kosten = Effektivkosten" and says "Die Höhe der Kosten (inkl. der Effektivkosten) wird Ihnen in Euro im individuellen Produktinformationsblatt vor Antragsstellung genannt". **Two real *Effektivkosten* values (1,45 and 1,33 Prozentpunkte) and two real CRK assignments (4 and 2) are now in this library** [S9], as is a real *Zertifizierungsnummer*. The sheets confirm the format is genuinely common across chassis — the insurance and the fund sheets carry the same headings — and that the cost list follows the § 2a AltZertG taxonomy line for line, including a separate line for costs "je 100 € Zulage oder Zuzahlung". **Still unestablished**: no *individual* sheet was seen, only *Muster* sheets, so no offer-specific *Effektivkosten* exist here; and the **PIA's simulation procedure** behind the CRK is not public and is not in scope — though the *return scenarios* used for the sheet's other figures are public, being prescribed in AltvPIBV § 10 [R5]

(delib-riester_rente-s15)=

### S15 — *Zertifizierungsbescheid* and *Zertifizierungsnummer*
- Publisher / doc type: the certifying authority — the **Bundeszentralamt für Steuern** (AltZertG § 3 Abs. 1), which took the function over from the **BaFin on 1 July 2010** (AltZertG § 14 Abs. 5: "Bis zum 30. Juni 2010 ist abweichend von § 3 Abs. 1 Zertifizierungsstelle die Bundesanstalt für Finanzdienstleistungsaufsicht"); the administrative act certifying a contract type, whose number every certified product carries
- URL: no *Zertifizierungsbescheid* is published; the statutory frame is read at [R2] and the numbers themselves on the sheets at [S9]
- Retrieved: yes, in the only two forms in which this artefact exists — the statute (AltZertG §§ 3, 5, 14, canonical XML [R2]) and two *Zertifizierungsnummern* on retrieved *Produktinformationsblätter*
- Used for: two structural propositions of the product spec's identity table, **both now confirmed against the statute**. Certification attaches to the **contract type**: § 5 Abs. 1 grants it on the provider's own assurance that the *Vertragsbedingungen* conform, and "Die Zertifizierung erfolgt mit der Übermittlung der Zertifizierungsnummer", under a reservation of revocation that lapses two years after the year of issue; where a certificate is revoked, "sind alle auf diesem Zertifikat beruhenden Verträge nicht mehr als Altersvorsorgeverträge zu behandeln" (§ 5 Abs. 2) — one certificate, a whole tariff's worth of contracts. And certification is **not** a quality judgement: § 3 Abs. 3 says so in terms — see the quotation at [R2]. **The 1 July 2010 hand-over date, previously `[unverified]`, is now read off § 14 Abs. 5.** And the assertion that *no certification number appears anywhere in this product's documents* **is withdrawn**: **006403** and **006407** are recorded at [S9]

(delib-riester_rente-s16)=

### S16 — The second tier of Riester insurance wordings
- Publisher / doc type: Stuttgarter; NÜRNBERGER; Continentale; HUK-COBURG; Volkswohl Bund; LV 1871; Hannoversche; Barmenia; Gothaer; Signal Iduna; Provinzial; DEVK; Universa; ERGO; AXA; Swiss Life; Zurich Deutscher Herold; Baloise; Württembergische; HDI; Generali/Dialog — AVB, *Verbraucherinformationen* and *Produktinformationsblätter* for Riester annuities
- URL: not established — no wording was located for any house named in this entry; the two houses whose wordings this pass did reach have their own entries, [S4] and [S6]
- Retrieved: no — nothing in this list was identified or opened. The entry stays what it always was: a list for a follow-up pass
- Used for: one proposition only — that a body of carrier wordings exists, and that a single life is the base design with a survivor's benefit written as a rider rather than as a second life. That proposition is now carried by documents rather than by this entry: [S2], [S4] and [S6] are all single-life wordings whose survivor's benefit is an election on the death benefit or a separate condition set [S3]. The entry remains deliberately unsplit because **nothing carrier-specific is established for any house in it** (gap 12), and the product spec's rule stands unchanged: **no parameter may cite [S16] for a level**

---

## Regulatory and actuarial references (product research numbering)

Twenty-six known references, [R1]–[R26]. **Seventeen of them record `Retrieved: yes`** — the
consolidated statutes and regulations [R1]–[R16] and [R22], every one read as canonical XML from
`gesetze-im-internet.de` with the *Stand* the XML carries quoted at the entry — and **two more are
part-retrieved on their statutory limb** [R23] [R26]. The canonical per-section URLs are no longer
marked `[unverified]`: every one tried in this pass returned the full text of its section. What each
entry supports is therefore stated in the product documents from the instrument itself, and the
paragraph numbers were checked one by one — three were wrong and are corrected at the entries.
**Seven entries stay `Retrieved: no`**: the five *Bundesgesetzblatt* amending acts [R17]–[R21],
whose effect the consolidated texts show but whose own wording was not opened, and the BMF
*Anwendungsschreiben* [R24] and the contract statistics [R25], neither of which was identified.
**Historic rates, vintages and phase-in dates keep their `[unverified]` tags for exactly that
reason**, because a consolidated statute shows the rule in force and never the sequence that
produced it.

Two structural points, stated once. **The product is defined by two statutes doing different jobs**:
the AltZertG says what a contract must contain to be certifiable, the EStG says who gets what
subsidy and how the benefit is taxed — a *product* rule is in the first, a *money* rule in the
second. And **no supervisory instrument sets Riester tariff levels**: the *Höchstrechnungszins*
[R22] binds the guarantee's discount rate and nothing else, while charges, *Rentenfaktoren* and
surplus are unregulated as to level and are disclosed rather than capped [R4] [R5].

(delib-riester_rente-r1)=

### R1 — AltZertG § 1, the criteria of a certifiable *Altersvorsorgevertrag*
- Publisher: Bundesministerium der Justiz / juris (Gesetze im Internet)
- URL: https://www.gesetze-im-internet.de/altzertg/__1.html — the human-facing per-section page, which does carry the section text; the text below was nevertheless read from the canonical XML at https://www.gesetze-im-internet.de/altzertg/xml.zip, because only the XML carries the law's *Stand*
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I Nr. 294, with amendments by Art. 5, 6 and 7 G v. 26.5.2026 I Nr. 156 textually noted but not yet fully consolidated, read 2026-08-30). **A note on the URLs in the statutory entries below**, because the library's own guidance was wrong about them: `gesetze-im-internet.de/<law>/__NNN.html` is **not** an empty frameset. Every such page tried in this pass returned the full text of its section — 26 kB for AltZertG § 1, 4 kB for the four sentences of EStG § 84. What the HTML page does **not** carry is the law's *Stand*, and that is the reason every statutory entry here was read from the canonical XML and cites the XML's *Stand* line. The per-section URL is kept as the human-facing link and is a real one.
- Used for: **the operative product statute, and the single most-cited reference in both documents.** Every specific in the list below was `[unverified]`; all of them are now read, and two of them were wrong or misplaced.
  - **Earliest *Rentenbeginn*.** § 1 Abs. 1 Satz 1 Nr. 2 requires "eine lebenslange und unabhängig vom Geschlecht berechnete Altersversorgung …, die nicht vor Vollendung des 62. Lebensjahres oder einer vor Vollendung des 62. Lebensjahres beginnenden Leistung aus einem gesetzlichen Alterssicherungssystem des Vertragspartners (Beginn der Auszahlungsphase) gezahlt werden darf". The **60th-year rule for older contracts is not in § 1** — it is a transitional provision, **§ 14 Abs. 2**, applying to contracts "die vor dem 1. Januar 2012 abgeschlossen worden sind". The library's statement of the rule was right; its citation was one section short, and both documents now cite § 14 Abs. 2 for the older limb.
  - **The *Beitragserhaltungszusage***, Nr. 3: "dass zu Beginn der Auszahlungsphase zumindest die eingezahlten Altersvorsorgebeiträge für die Auszahlungsphase zur Verfügung stehen und für die Leistungserbringung genutzt werden", with the carve-out "sofern Beitragsanteile zur Absicherung der verminderten Erwerbsfähigkeit oder Dienstunfähigkeit oder zur Hinterbliebenenabsicherung verwendet werden, sind **bis zu 20 Prozent der Gesamtbeiträge** in diesem Zusammenhang nicht zu berücksichtigen". The **20 %** cap is confirmed exactly. Note that the statute speaks of *Altersvorsorgebeiträge*, which EStG § 82 defines as what the *Zulageberechtigte* pays; **that the Zulagen also count toward the floor is not resolved by the statutory text** and is established instead from the model wording and the carrier wordings, which say so in terms [S2] [S4] [S6].
  - **Benefit form**, Nr. 4 Buchst. a: a lifelong *Leibrente* or an *Auszahlungsplan* with *Teilkapitalverrentung* from at latest the 85th year, and "die Leistungen müssen während der gesamten Auszahlungsphase gleich bleiben oder steigen". Up to twelve monthly payments may be combined into one.
  - **The 30 % cap**, same provision: "bis zu 30 Prozent des zu Beginn der Auszahlungsphase zur Verfügung stehenden Kapitals kann an den Vertragspartner außerhalb der monatlichen Leistungen ausgezahlt werden".
  - **The five-year spreading floor**, Nr. 8, with a qualifier the library did not carry: the costs must be spread "gleichmäßig mindestens auf die ersten fünf Vertragsjahre …, **soweit sie nicht als Prozentsatz von den Altersvorsorgebeiträgen abgezogen werden**". A percentage-of-contribution charge is therefore outside the spreading rule altogether — which is exactly how [S2], [S4] and [S6] treat the charge on a Zulage.
  - **The *Wechselrecht***, Nr. 10 Buchst. b: termination "mit einer Frist von drei Monaten zum Ende eines Kalendervierteljahres oder zum Beginn der Auszahlungsphase" to have the capital transferred; Buchst. a gives the right to let the contract lie dormant and Buchst. c the *Eigenheimbetrag* route.
  - **The transfer-charge cap, which closes gap 8.** § 1 Abs. 1 Satz 3: "Bei einer Übertragung des nach Satz 1 Nummer 10 Buchstabe b gekündigten Kapitals ist es unzulässig, dass der Anbieter des bisherigen Altersvorsorgevertrags dem Vertragspartner Kosten in Höhe von mehr als **150 Euro** in Rechnung stellt." Satz 4 adds that the receiving provider may take at most **50 Prozent** of the transferred subsidised capital into account when calculating its own acquisition and distribution costs. The model's **[std]** 50,00 € transfer charge therefore sits inside a now-known ceiling, and one retrieved carrier charges nothing at all [S4] while a fund provider charges exactly 50,00 € [S9].
  - **Unisex**, Nr. 2, in the words quoted above.
  - And § 1 Abs. 5, which defines *gebildetes Kapital* as the *Deckungskapital* plus allocated *Überschussanteile*, the transferable part of the *Schlussüberschussanteil* and the *Bewertungsreserven* under § 153 Abs. 1 and 3 VVG, and closes with "Abzüge, soweit sie nicht in diesem Gesetz vorgesehen sind, sind nicht zulässig" — the statutory basis for the model's transfer value being struck at full value with no *Stornoabzug*

(delib-riester_rente-r2)=

### R2 — AltZertG §§ 2, 2a, 3, 3a, 5 and 14, certification and the certifying authority
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/altzertg/ (canonical XML at https://www.gesetze-im-internet.de/altzertg/xml.zip)
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I Nr. 294, with amendments by Art. 5, 6 and 7 G v. 26.5.2026 I Nr. 156 textually noted but not yet fully consolidated, read 2026-08-30)
- Used for: the product spec's insistence that certification is an administrative act on the contract's **terms** and not a statement about the provider. **The statute says this in one sentence, and it is worth quoting rather than paraphrasing** — § 3 Abs. 3: "Die Zertifizierungsstelle prüft nicht, ob ein Altersvorsorge- oder ein Basisrentenvertrag wirtschaftlich tragfähig und die Zusage des Anbieters erfüllbar ist und ob die Vertragsbedingungen zivilrechtlich wirksam sind." The *Beitragsgarantie* is accordingly the **provider's own** and its ability to honour it is an ordinary solvency question [REG-R5] [REG-R6], and no delib document may call the product state-guaranteed. Also read here, and newly usable:
  - § 3 Abs. 1, "Zertifizierungsstelle ist das Bundeszentralamt für Steuern", with § 14 Abs. 5 dating the hand-over from the BaFin to **1 July 2010** [S15];
  - § 3 Abs. 2 Satz 2, which puts the **CRK simulation procedure** in the *Zertifizierungsstelle's* hands, and § 3a, which lets the BMF transfer that task "im Wege der Beleihung" to the *Produktinformationsstelle Altersvorsorge* — the precise route by which the PIA, a private body, assigns a statutory risk class;
  - **§ 2a *Kostenstruktur***, which the library did not cite at all and which is the statutory frame for every charge in this product: a certified contract "darf **ausschließlich** die nachfolgend genannten Kostenarten vorsehen", and the closed list is euro amounts per year or month, a percentage of the *gebildetes Kapital*, of the *Bausparsumme* or loan amount, **of the contributions or *Tilgungsleistungen***, of the *Wohnförderkonto* balance, and from the payout phase a percentage of the benefit paid — plus three *anlassbezogene* charges, for a termination with transfer or payout, for an *Eigenheimbetrag*, and for a *Versorgungsausgleich*. Every retrieved *Produktinformationsblatt* [S14] reports its costs against exactly this list;
  - and § 5 Abs. 3 to 5, which govern what happens when a certificate is amended or revoked, including a right for the saver to keep the old terms at the price of the contract ceasing to be an *Altersvorsorgevertrag*, and an obligation on the provider to refund half — or, on revocation, all — of the acquisition and distribution costs already charged

(delib-riester_rente-r3)=

### R3 — AltZertG § 1 Abs. 1a, the *Altersvorsorgevertrag* in the form of a *Darlehen*
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/altzertg/__1.html — text read from the canonical XML
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I Nr. 294, with amendments by Art. 5, 6 and 7 G v. 26.5.2026 I Nr. 156 textually noted but not yet fully consolidated, read 2026-08-30)
- Used for: the statutory hook behind the Wohn-Riester exclusion, now read. § 1 Abs. 1a treats as an *Altersvorsorgevertrag* a contract giving a right to a loan, the loan contract itself, and a contract combining a savings limb under Abs. 1 with a loan limb, the two counting as "einheitlicher Vertrag". Two conditions the library did not carry: the loan "ist für eine wohnungswirtschaftliche Verwendung im Sinne des § 92a Abs. 1 Satz 1 des Einkommensteuergesetzes einzusetzen" and "**ist spätestens bis zur Vollendung des 68. Lebensjahres des Vertragspartners zu tilgen**", and the five-year cost-spreading rule of Abs. 1 Satz 1 Nr. 8 applies to it as well. So "Riester" in German usage does cover a mortgage, and the delib documents must say which of the four chassis they represent

(delib-riester_rente-r4)=

### R4 — AltZertG §§ 7 to 7c, the *Produktinformationsblatt* and the *Chancen-Risiko-Klassen*
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/altzertg/__7.html — text read from the canonical XML
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I Nr. 294, with amendments by Art. 5, 6 and 7 G v. 26.5.2026 I Nr. 156 textually noted but not yet fully consolidated, read 2026-08-30)
- Used for: the disclosure regime in the product spec's charges and regulatory sections. **One attribution in this entry was wrong and is corrected here: the word *Effektivkosten* does not appear anywhere in the AltZertG.** The statute requires (§ 7 Abs. 1 Satz 2) the *Zertifizierungsnummer* (Nr. 3), "die auf Wahrscheinlichkeitsrechnungen beruhende Einordnung in **Chancen-Risiko-Klassen**" (Nr. 7), "eine Aufstellung der Kosten nach § 2a Satz 1 Nummer 1 Buchstabe a bis f sowie § 2a Satz 1 Nummer 2 Buchstabe a bis c, **getrennt für jeden Gliederungspunkt**" (Nr. 9) and "Angaben zum **Preis-Leistungs-Verhältnis**" (Nr. 10). The *Effektivkosten* are defined one level down, in AltvPIBV § 8 Nr. 3 — see [R5], which both product documents now cite for that term instead of this entry. Also read here:
  - a real sanction the library did not carry, § 7 Abs. 1 Satz 2 Nr. 9 third sentence: "Kosten nach § 2a Satz 1, die im individuellen Produktinformationsblatt nicht ausgewiesen sind oder auf die nicht hingewiesen wurde, **sind vom Vertragspartner nicht geschuldet**" — so on a certified contract disclosure is constitutive of the charge, which is a stronger statement than "disclosed rather than capped";
  - § 7 Abs. 2, which displaces the VVG-InfoV product sheet and **forbids** a § 154 VVG *Modellrechnung* for a certified contract;
  - § 7 Abs. 3, a two-year right of *Rücktritt* where the sheet was defective, on repayment of at least contributions and Zulagen with statutory interest;
  - § 7 Abs. 4, the ***Muster*-Produktinformationsblatt** for assumed terms of **12, 20, 30 and 40 years** — which is what all four retrieved sheets [S14] are;
  - and § 7a, § 7b and § 7c, the annual information duty, the information due before the payout phase (no later than three months before, with a shortened right of transfer where it is late) and the cost-change duty
  - **The claim that a 100 %-guaranteed product sits at the low-risk end of the CRK scale by construction is contradicted** by a retrieved sheet and is withdrawn from the product documents — see [S9]

(delib-riester_rente-r5)=

### R5 — AltvPIBV, the *Verordnung zum Produktinformationsblatt und zu weiteren Informationspflichten bei zertifizierten Altersvorsorge- und Basisrentenverträgen*
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/altvpibv/ (canonical XML at https://www.gesetze-im-internet.de/altvpibv/xml.zip)
- Retrieved: yes (canonical XML, 19 sections, Stand: zuletzt geändert durch Art. 2 Abs. 1 V v. 12.11.2021 I 4921, read 2026-08-30)
- Used for: the proposition that the *form* of the sheet is prescribed by regulation — now read, and it delivers more than the library expected of it.
  - **The *Effektivkosten* are defined here, not in the statute** (§ 8 Nr. 3): "die Minderung der Wertentwicklung des Vertrags bis zum Beginn der Auszahlungsphase durch Kosten in **Prozentpunkten** (Effektivkosten)". § 10 Abs. 5 adds "Bei der Berechnung der Effektivkosten sind alle für den Vertrag anfallenden Kosten zu berücksichtigen. Die **Produktinformationsstelle Altersvorsorge** gibt die Methodik für die Berechnung der Effektivkosten vor." So the *definition* and the *scenarios* are public and the *methodology* is not.
  - **§ 9 Abs. 3 closes gap 6.** "Bei der Berechnung ist zu unterstellen, dass die Zulagen jeweils **am 15. Mai nach dem Beitragsjahr** dem Vertrag gutgeschrieben werden." The library recorded that neither the payment month nor any convention for it was established and carried the one-year cash lag as a bare **[std]**. There is a prescribed convention, it is in the year following the contribution year, and the model's one-year lag is the annual-grid expression of it.
  - **§ 14 Abs. 1 gives the model case**, and it is the composite's own: terms of 12, 20, 30 and 40 years beginning 1 January; "ein Beginn der Auszahlungsphase mit **Vollendung des 67. Lebensjahres**"; and a monthly contribution of one twelfth of (1 200 € − *Grundzulage*), rounded — which at a 175 € *Grundzulage* is the 85,00 € a month the Union Investment sheets show [S9]. The product spec's representative *Rentenbeginn* at attained age **67**, previously **[std]** on an `[unverified]` appeal to German practice, is the regulation's own model assumption.
  - **§ 10 Abs. 1 and 2 give the return scenarios**, by CRK: 2 / 3 / 4 / 5 / 6 % before costs for CRK 1 to 5 for the *Effektivkosten* line, and four-scenario sets per class (CRK 2: 0,5 / 2 / 3 / 4 %) for the capital and benefit projections. These are public, so the library's statement that reproducing the sheet needs a non-public scenario set is **too broad**: what is not public is the PIA's classification simulation (AltZertG § 3 Abs. 2 Satz 2) and the *Effektivkosten* methodology, not the disclosed scenarios.
  - **§ 5** confirms the CRK scale — 1 to 5, "wobei CRK 1 die niedrigste und CRK 5 die höchste Chancen-Risiko-Klasse darstellt" — determined separately for each of the four terms, with the sheet showing the class for the band the planned term falls in

(delib-riester_rente-r6)=

### R6 — EStG § 10a, the *Sonderausgabenabzug* and the *Günstigerprüfung*
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__10a.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: the second subsidy route, now read. § 10a Abs. 1 Satz 1: persons compulsorily insured in the domestic statutory pension insurance "können Altersvorsorgebeiträge (§ 82) **zuzüglich der dafür nach Abschnitt XI zustehenden Zulage** jährlich bis zu **2 100 Euro** als Sonderausgaben abziehen", the list of assimilated groups following in Nrn. 1–5. The **2 100 €** ceiling and the together-with-the-Zulagen construction are confirmed; **the claim that it has not been raised since 2008 is a historical statement the consolidated text cannot support and keeps its `[unverified]` tag.** The *Günstigerprüfung* is § 10a Abs. 2 and works as the library described, by the route the library did not state: where the deduction is the better outcome, "erhöht sich die unter Berücksichtigung des Sonderausgabenabzugs ermittelte tarifliche Einkommensteuer **um den Anspruch auf Zulage**" — the Zulage is added back, so the saver keeps the larger of the two and not their sum — and "Die Günstigerprüfung wird **von Amts wegen** vorgenommen." Two refinements the library did not carry: the *Berufseinsteiger-Bonus* is left out of the comparison (Abs. 1 Satz 5), and where one spouse is only *mittelbar* eligible the deducting spouse counts both spouses' contributions and Zulagen and **the ceiling rises by 60 Euro** to 2 160 € (Abs. 3 Sätze 2–4). The proposition that a *mittelbar* eligible spouse has no deduction of their own is confirmed by that same provision. The technical notes cite it for **why the model has no cells for any of this**: only the Zulage reaches the policy, and the § 10a advantage is a personal tax refund (pitfall 5)

(delib-riester_rente-r7)=

### R7 — EStG § 79 with § 10a Abs. 1, who is *zulageberechtigt*
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__79.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: the eligibility rule that decides whether a model point can hold this contract at all. **One structural correction**: § 79 itself contains no list. Satz 1 says only "Die in § 10a Absatz 1 genannten Personen haben Anspruch auf eine Altersvorsorgezulage", so the ***unmittelbar* list lives in § 10a Abs. 1** and both product documents now cite the pair. Read there, the list is compulsory members of the domestic statutory pension insurance, plus recipients of *Besoldung* and *Amtsbezüge*, certain insurance-free and exempted employees with an equivalent *Versorgungsrecht*, *Beamte* on unpaid leave, and (Satz 3) *Landwirte* and persons in an *Anrechnungszeit*; recipients of *Arbeitslosengeld*, parents in *Kindererziehungszeiten* and *geringfügig Beschäftigte* who did not opt out reach the list through the compulsory-insurance limb rather than by name. Full *Erwerbsminderungs-* and *Dienstunfähigkeitsrentner* come in through § 10a Abs. 1 Satz 4, **with two qualifications the library did not carry**: they must have belonged to a favoured group immediately before the benefit, and "dies gilt nicht, wenn der Steuerpflichtige das **67. Lebensjahr** vollendet hat". The *mittelbar* limb is § 79 Satz 2 and is confirmed exactly as model point 5 uses it — no permanent separation, EU/EEA residence, "ein auf den Namen des anderen Ehegatten lautender Altersvorsorgevertrag besteht", "mindestens **60 Euro** geleistet" in the contribution year, and the payout phase of that contract not yet begun. The exclusion of the self-employed outside compulsory insurance and of *Versorgungswerk* members follows from the list being closed, which is why delib carries `basisrente` as a separate product. That eligibility is **annual** follows from § 88, which makes the claim arise "mit Ablauf des Kalenderjahres, in dem die Altersvorsorgebeiträge geleistet worden sind (Beitragsjahr)"

(delib-riester_rente-r8)=

### R8 — EStG §§ 82 and 83, *Altersvorsorgebeiträge* and the *Altersvorsorgezulage*
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__82.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: the definitional claim the whole reporting design rests on — **the Zulage is a contribution, not a benefit**. The claim stands, but **these two sections are not where it is established, and both product documents now cite the right provisions.** § 82 Abs. 1 defines *geförderte Altersvorsorgebeiträge* as "1. Beiträge, 2. Tilgungsleistungen, die **der Zulageberechtigte** … zugunsten eines auf seinen Namen lautenden Vertrags leistet" — i.e. what the saver pays, which on its face does **not** include the Zulage — and § 83 says only that a Zulage "in Abhängigkeit von den geleisteten Altersvorsorgebeiträgen" is paid and is made up of *Grundzulage* and *Kinderzulage*. What makes the Zulage a contract cash flow is **§ 90 Abs. 2** [R11]: the ZfA has it paid to the provider, and "Der Anbieter hat die erhaltenen Zulagen unverzüglich den begünstigten Verträgen gutzuschreiben". What makes it count toward the guarantee is the **contract wording**, not the statute [S2] [S4] [S6]. § 82 does confirm the Wohn-Riester limb — *Tilgungsleistungen* count as subsidised contributions where the loan was used for a post-2007 *wohnungswirtschaftliche Verwendung*. `zulagen` therefore remains a separate positive income column of `result_cf()`, never folded into `premiums` (pitfall 4)

(delib-riester_rente-r9)=

### R9 — EStG § 84 (*Grundzulage*, *Berufseinsteiger-Bonus*) and § 85 (*Kinderzulage*)
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__84.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: every Zulage amount in the model — *Grundzulage* **175,00 €** from contribution year 2018 (154,00 € 2008–2017, phased in from 38,00 €); the once-in-a-lifetime **200,00 €** *Berufseinsteiger-Bonus* for a saver under 25, which is model point 6; and the **185,00 € / 300,00 €** *Kinderzulage* split by whether the child was born before or from 1 January 2008. That split is a permanent **birth-cohort** rule rather than a transition, so a contract can draw both rates at once — model point 3, at 175 + 185 + 300 = 660,00 € — which is pitfall 6. Also for the fact that the *Kinderzulage* runs only while *Kindergeld* is drawn, which makes the Zulage stream a **falling step function** driven by a household variable the insurance contract does not observe, and hence why `zulage_schedule.csv` is an exogenous per-model-point schedule.
  **Every current amount is now read and every one is confirmed.** § 84 Satz 1: "Jeder Zulageberechtigte erhält eine Grundzulage; diese beträgt **ab dem Beitragsjahr 2018** jährlich **175 Euro**." Satz 2: the *Berufseinsteiger-Bonus*, for those "die zu Beginn des Beitragsjahres (§ 88) das **25. Lebensjahr** noch nicht vollendet haben, erhöht sich die Grundzulage nach Satz 1 um **einmalig 200 Euro**", granted for the first contribution year beginning after 31 December 2007 for which a Zulage is claimed. § 85 Abs. 1: "Die Kinderzulage beträgt für jedes Kind, für das gegenüber dem Zulageberechtigten Kindergeld **festgesetzt** wird, jährlich **185 Euro**. Für ein nach dem **31. Dezember 2007** geborenes Kind erhöht sich die Kinderzulage nach Satz 1 auf **300 Euro**." The *Kindergeld* link is confirmed, as is the attribution rule (§ 85 Abs. 2 — to the mother, or on a joint application to the father, for married opposite-sex parents; to the *Kindergeld* recipient for same-sex couples). **What remains `[unverified]` is the history**: the consolidated text carries only the current rates, so the 154,00 € rate for 2008–2017 and the 38,00 / 76,00 / 114,00 € and 46,00 / 92,00 / 138,00 € phase-in steps are not confirmed by it and keep their tags

(delib-riester_rente-r10)=

### R10 — EStG §§ 86 and 87 (*Mindesteigenbeitrag*, *Sockelbeitrag*)
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__86.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: the contribution engine `M(t) = max(60, min(0.04 × Y(t), 2 100) − Z*(t))`. **The whole formula is now read and every input is confirmed.** § 86 Abs. 1 Satz 2: the *Mindesteigenbeitrag* "beträgt jährlich **4 Prozent** der Summe der in dem dem Kalenderjahr **vorangegangenen** Kalenderjahr … erzielten beitragspflichtigen Einnahmen …, jedoch **nicht mehr als der in § 10a Absatz 1 Satz 1 genannte Höchstbetrag** [2 100 €], **vermindert um die Zulage** nach den §§ 84 und 85"; Satz 4, "Als Sockelbetrag sind ab dem Jahr 2005 jährlich **60 Euro** zu leisten"; Satz 5, the *Sockelbetrag* applies where it exceeds the Satz 2 amount, which is the `max(60, …)`; and Satz 6, the sentence that decides the whole behavioural design: "**Die Kürzung der Zulage ermittelt sich nach dem Verhältnis der Altersvorsorgebeiträge zum Mindesteigenbeitrag.**" The Kürzung is proportional, not a cliff — model point 7 and pitfall 3 — and the base is the previous calendar year's income, the first of the model's two lags (pitfall 1). Two further rules the library did not carry: where the spouse is *mittelbar* eligible the minimum is computed "unter Berücksichtigung der den Ehegatten insgesamt zustehenden Zulagen" (Abs. 1 Satz 2 second half, Abs. 2 Satz 1), and a non-commercial carer's income counts as **0 Euro** (Abs. 2 Satz 3). § 87 caps the subsidy at **two** contracts per *unmittelbar* eligible saver, splitting the Zulage in proportion to the contributions paid to them, and allows a *mittelbar* eligible spouse only one. The product spec's worked cases, including the 60,00 €-for-775,00 € leverage that model point 4 reproduces, are arithmetic on this text

(delib-riester_rente-r11)=

### R11 — EStG §§ 89 to 91, and the *Zentrale Zulagenstelle für Altersvermögen* (ZfA)
- Publisher: Gesetze im Internet; Deutsche Rentenversicherung Bund
- URL: https://www.gesetze-im-internet.de/estg/__89.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: the model's **timing**, now read end to end, and **gap 6 is largely closed** — partly here and partly at [R5].
  - § 89 Abs. 1: the saver applies on an official form through the provider "bis zum Ablauf des **zweiten** Kalenderjahres, das auf das Beitragsjahr (§ 88) folgt"; Abs. 1a is the ***Dauerzulageantrag***, a written authority to the provider to claim for every contribution year, revocable to the end of a contribution year.
  - § 89 Abs. 2 Satz 2 and Abs. 3: the provider transmits the data of applications received in a quarter "bis zum Ende des folgenden Monats", and under a *Dauerzulageantrag* "bis zum Ablauf des auf das Beitragsjahr folgenden Kalenderjahres". So the entitlement for year `t` cannot normally reach the contract before year `t + 1`, which is the second of the model's two lags, and the AltvPIBV's own **15 May of year `t + 1`** convention [R5] fixes the month for disclosure purposes. `zulage_pp(t) = zulage_granted_pp(t − 1)` is therefore no longer a bare **[std]**; only the exact within-year timing on an annual grid is.
  - § 90 Abs. 1 and 2: the central body determines entitlement and "veranlasst die Auszahlung **an den Anbieter** …; Der Anbieter hat die erhaltenen Zulagen **unverzüglich** den begünstigten Verträgen gutzuschreiben." No separate decision is issued unless asked for. This is the provision that makes the Zulage a contract cash flow [R8].
  - § 90 Abs. 3: the credit is indeed **provisional**. The central body may recognise up to "das Ende des **zweiten** auf die Ermittlung der Zulage folgenden Jahres" that entitlement did not exist, must reclaim within a year of doing so, "Bei bestehendem Vertragsverhältnis hat der Anbieter das Konto zu belasten", and the provider remits the quarter's reclaims "bis zum **zehnten Tag** des dem Kalendervierteljahr folgenden Monats". **The reversal frequency the library recorded as unestablished is quarterly**; what remains unestablished is the *rate* at which reversals occur, which is an experience quantity and not a statutory one (gap 16).
  - § 91 is the data match itself, against the pension insurers, the *landwirtschaftliche Alterskasse*, the *Bundesagentur für Arbeit*, the registration authorities, the *Familienkassen* and the tax offices.
  The `zulage_init_pp` column still exists only because an in-force point opens owing one Zulage, and the ZfA administration still sits inside the per-policy maintenance expense

(delib-riester_rente-r12)=

### R12 — EStG § 22 Nr. 5, the taxation of the benefit
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__22.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: the *nachgelagerte Besteuerung* rule that makes this a Schicht-2 product, now read. § 22 Nr. 5 Satz 1 brings "Leistungen aus Altersvorsorgeverträgen, Pensionsfonds, Pensionskassen und Direktversicherungen" into *sonstige Einkünfte* in full; Satz 2 carves out only the part **not** resting on § 10a / Abschnitt XI contributions or on Zulagen, and sends it to the *Ertragsanteil* for a lifelong annuity (Buchst. a, via Nr. 1 Satz 3 Buchst. a [REG-R41]) or to § 20 Abs. 1 Nr. 6 for other insurance benefits (Buchst. b [REG-R45]). The **two pools** — `pool_gefoerdert_pp` beside `pool_ungefoerdert_pp`, model point 8 — are exactly this Satz 1 / Satz 2 division. Satz 3 confirms the *schädliche Verwendung* treatment: the capital paid out counts as a Satz 2 benefit "**nach Abzug der Zulagen**", so the Zulagen are repaid and the growth on the subsidised part is taxed. **One correction**: the ***Leistungsmitteilung* is not annual.** Satz 7 requires it "Bei **erstmaligem** Bezug von Leistungen, in den Fällen des § 93 Absatz 1 sowie bei **Änderung** der im Kalenderjahr auszuzahlenden Leistung", after the end of the calendar year, with the Satz 1 to 3 amounts stated "**je gesondert**". The product documents said "annual" and now say what the statute says. Satz 13 carries the *Fünftelregelung* limb — "Für Leistungen aus Altersvorsorgeverträgen nach § 93 Absatz 3 ist § 34 Absatz 1 entsprechend anzuwenden" — and, because it names only § 93 Abs. 3, it confirms by exclusion that the **30 % *Teilkapitalauszahlung* gets no such relief** [R15]

(delib-riester_rente-r13)=

### R13 — EStG §§ 92a and 92b, Wohn-Riester and the *Wohnförderkonto*
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__92a.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: the informed exclusion of Wohn-Riester from the model. § 92a Abs. 1 Satz 1 confirms the *Altersvorsorge-Eigenheimbetrag* and adds the threshold the library did not carry: the capital may be taken in full, or in part provided "das verbleibende geförderte Restkapital mindestens **3 000 Euro** beträgt" and the amount withdrawn is itself at least 3 000 € (20 000 €, or 6 000 € within three years of acquisition, for a conversion or energy refurbishment). That is the same figure the CosmosDirekt wording cites at its § 10 [S4]. § 93 Abs. 1 Satz 4 Buchst. d confirms that no repayment obligation attaches to it. The *Wohnförderkonto* remains what the documents say it is — a notional account carrying **no cash whatsoever** — and the exclusion stands: there is no liability and no cash flow to project, while from the insurer's side an *Eigenheimbetrag* is an early full-value exit, which the model does not implement and says so. One consequence now readable in the wordings: the *Beitragserhaltungsgarantie* is **reduced** by an *Eigenheimbetrag* withdrawal [S2] [S4]

(delib-riester_rente-r14)=

### R14 — EStG §§ 93, 94 and 95, *schädliche Verwendung* and its consequences
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__93.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: the reason a Riester surrender is not an ordinary surrender, now read. § 93 Abs. 1 Satz 1 defines the *Rückzahlungsbetrag* as "die auf das ausgezahlte geförderte Altersvorsorgevermögen entfallenden **Zulagen** und die nach § 10a Absatz 4 gesondert festgestellten **Beträge**" — all Zulagen and all § 10a relief, exactly as the documents state — and § 22 Nr. 5 Satz 3 taxes the growth on the subsidised part [R12]. That is the argument behind a `lapse_rate` set materially below a Schicht-3 one. The *förderunschädliche* list from which the model's option set is built is confirmed: transfer to another certified contract in the saver's own name (Abs. 2 Satz 1), internal or external division on a *Versorgungsausgleich* (Abs. 1a), the *Eigenheimbetrag* (Abs. 1 Satz 4 Buchst. d), the *Kleinbetragsrenten-Abfindung* (Abs. 3), a *Hinterbliebenenrente* to the persons named in AltZertG § 1 Abs. 1 Satz 1 Nr. 2 (Abs. 1 Satz 4 Buchst. a), and transfer on death to a surviving spouse's own certified contract on the conditions of Abs. 1 Satz 4 Buchst. c. **§ 94 confirms the withholding mechanic and so the gross-publication convention** (pitfall 18): the provider notifies the ZfA before paying, the ZfA computes the amount, and "Der Anbieter hat den Rückzahlungsbetrag **einzubehalten**, mit der nächsten Anmeldung nach § 90 Absatz 3 anzumelden und an die zentrale Stelle **abzuführen**" — a tax collection through the insurer, not a reduction in the insurer's obligation. **§ 95 closes gap 15**: "Die §§ 93 und 94 gelten entsprechend, wenn sich der Wohnsitz oder gewöhnliche Aufenthalt des Zulageberechtigten **ab Beginn der Auszahlungsphase** außerhalb der Mitgliedstaaten der Europäischen Union und der Staaten befindet, auf die das Abkommen über den Europäischen Wirtschaftsraum anwendbar ist". So the emigration rule survives, but it bites only from the start of the payout phase and only outside the EU/EEA; the historic version that triggered on the end of unlimited tax liability is gone from the text, and the documents no longer say the current rule is unknown

(delib-riester_rente-r15)=

### R15 — EStG § 93 Abs. 3 with SGB IV § 18, the *Kleinbetragsrente*; EStG § 34, the *Fünftelregelung*
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__93.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: the commutation the model computes rather than assumes. **This entry carries the pass's flat contradiction, and it is a rate the model implements.** The documents recorded two irreconcilable readings of the trigger — 1 % of the monthly *Bezugsgröße* against 1,5 % — and chose the 1 % reading. The statute has one reading, and it is the other one. § 93 Abs. 3 Satz 2 Nr. 1: "Eine Kleinbetragsrente ist 1. eine Rente, die bei gleichmäßiger Verrentung des gesamten zu Beginn der Auszahlungsphase zur Verfügung stehenden Kapitals eine monatliche Rente ergibt, die **1,5 Prozent** der monatlichen Bezugsgröße nach § 18 des Vierten Buches Sozialgesetzbuch nicht übersteigt". On the same 3 955,00 € monthly *Bezugsgröße* the library uses — a figure itself still `[unverified]`, SGB IV not being among the cached instruments — the threshold is **59,33 €**, not 39,55 €. Satz 3 confirms the aggregation rule: "Bei der Berechnung dieses Betrags sind **alle bei einem Anbieter bestehenden Verträge** des Zulageberechtigten insgesamt zu berücksichtigen". Satz 1 confirms that an *Abfindung* at the start of the payout phase is not *schädliche Verwendung*, so no subsidy is repaid. The *Fünftelregelung* runs through § 22 Nr. 5 Satz 13 to § 34 Abs. 1 [R12], and the deferral election is in AltZertG § 1 Abs. 1 Satz 1 Nr. 4 Buchst. a — four weeks from the provider's notice to require payment on 1 January of the following year — and is drafted into the model wording at [S2]. **What the statute does not settle**, and gap 7 still records: whether the test is applied before or after an elected *Teilkapitalauszahlung*. The GDV model wording does settle it, against the composite — see [S2]. Whether commutation is the provider's right is likewise settled by the wordings, in the composite's favour: "**können wir** die Rente … abfinden" [S2], "**kann** die Leistung in Form einer einmaligen Kapitalabfindung erfolgen" [S4]

(delib-riester_rente-r16)=

### R16 — EStG § 97 (*Übertragbarkeit*), with ZPO §§ 851 and 851c for the execution limb
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__97.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/estg/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: two behavioural propositions in the technical notes. **The first is confirmed and the second was mis-cited.** § 97 is two sentences and says only: "Das nach § 10a oder Abschnitt XI geförderte Altersvorsorgevermögen einschließlich seiner Erträge, die geförderten laufenden Altersvorsorgebeiträge und der Anspruch auf die Zulage sind **nicht übertragbar**." **There is no *Pfändungsschutz* in § 97.** The protection from attachment is a consequence, not a provision: ZPO § 851 Abs. 1 (canonical XML, Stand: zuletzt geändert Art. 2 G v. 22.12.2025 I Nr. 349, read 2026-08-30) provides that "Eine Forderung ist in Ermangelung besonderer Vorschriften der Pfändung nur insoweit unterworfen, als sie **übertragbar** ist", so § 97's non-transferability carries the execution protection with it. The separate ZPO § 851c route [REG-R40] is **not** available to a contract of this shape, since its Nr. 4 requires that "die Zahlung einer Kapitalleistung … nicht vereinbart wurde" and a Riester contract with a *Teilkapitalauszahlung* has agreed one. That the capital cannot be pledged as loan collateral is separately drafted into the carrier wording — "Die Abtretung von Forderungen und Rechten aus dem Versicherungsvertrag sowie seine Verpfändung sind ausgeschlossen" [S4]. Both limbs feed the argument for a low `lapse_rate` and for *Beitragsfreistellung* being the characteristic exit

(delib-riester_rente-r17)=

### R17 — *Altersvermögensgesetz* (AVmG) and *Altersvermögensergänzungsgesetz* (AVmEG), 2001
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established — the *Bundesgesetzblatt* text of the amending act was not located in this pass; what a consolidated statute shows is the **result** of the amendment, not the act
- Retrieved: no — the act itself was not opened. The entry is kept as a known reference for the legislative history, and the propositions it supports are marked below according to whether a retrieved consolidated text evidences them
- Used for: the founding statutes in the product spec's market-role section — that the same reform **reduced the future replacement rate of the statutory pension** and **created a subsidised private product to fill the gap**, which is the whole political logic of the product; and for the two-step phase-in of the *Mindesteigenbeitrag* percentage (1 % / 2 % / 3 % / 4 %) and of the Zulagen to 2008. **All of that stays `[unverified]`.** The consolidated texts retrieved in this pass carry only the end state — 4 % and the current Zulagen [R9] [R10] — and the AltZertG's own *Ausfertigung* date of **26 June 2001** is the one datum from the period that is now read

(delib-riester_rente-r18)=

### R18 — *Alterseinkünftegesetz* (AltEinkG), 2004
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established — the *Bundesgesetzblatt* text of the amending act was not located in this pass; what a consolidated statute shows is the **result** of the amendment, not the act
- Retrieved: no — the act itself was not opened. The entry is kept as a known reference for the legislative history, and the propositions it supports are marked below according to whether a retrieved consolidated text evidences them
- Used for: the **three-layer taxonomy** every delib scope note uses — Schicht 1 *Basisversorgung*, Schicht 2 *Zusatzversorgung*, Schicht 3 *Kapitalanlageprodukte* — and for the placing of this contract in **Schicht 2**: relieved on the way in and taxed in full on the way out, alongside the *betriebliche Altersversorgung*, which is what distinguishes it from `klassische_rentenversicherung` on the same chassis. The **taxonomy is a description of the statute rather than a term in it**; the placement of this contract in Schicht 2 is directly evidenced by EStG § 22 Nr. 5 [R12], which was retrieved. The 2004 act itself was not

(delib-riester_rente-r19)=

### R19 — *Eigenheimrentengesetz* (EigRentG), 2008
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established — the *Bundesgesetzblatt* text of the amending act was not located in this pass; what a consolidated statute shows is the **result** of the amendment, not the act
- Retrieved: no — the act itself was not opened. The entry is kept as a known reference for the legislative history, and the propositions it supports are marked below according to whether a retrieved consolidated text evidences them
- Used for: the creation of Wohn-Riester [R13] and of the certifiable loan [R3], and for the 300 € *Kinderzulage* rate for children born from 2008 that produces the permanent two-rate split [R9]; and, in the product spec's market section, for the warning that a material minority of "Riester contracts" in an official count are housing contracts that will never pay an annuity. **The substance is now evidenced by the consolidated texts and the attribution to this act is not**: EStG § 85 Abs. 1 Satz 2 carries the 300 € rate for a child born after 31 December 2007, EStG § 92a the *Eigenheimbetrag* and AltZertG § 1 Abs. 1a the certifiable loan, all retrieved; that this act introduced them is `[unverified]`

(delib-riester_rente-r20)=

### R20 — *Altersvorsorge-Verbesserungsgesetz* (AltvVerbG), 2013
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established — the *Bundesgesetzblatt* text of the amending act was not located in this pass; what a consolidated statute shows is the **result** of the amendment, not the act
- Retrieved: no — the act itself was not opened. The entry is kept as a known reference for the legislative history, and the propositions it supports are marked below according to whether a retrieved consolidated text evidences them
- Used for: the administrative reform — the standardised *Produktinformationsblatt* [R4] [R5] [S14]; the cap on the provider's charge for a *Wechsel*; and the 60 € *Sockelbeitrag* for a *mittelbar* eligible spouse, the rule model point 5 sits on. **All three are now evidenced in the consolidated texts, and gap 8 closes there**: the ceiling is **150 Euro**, AltZertG § 1 Abs. 1 Satz 3 [R1], and the *Sockelbeitrag* is EStG § 79 Satz 2 Nr. 4 [R7]. AltZertG § 14 Abs. 6 dates the 2013 act's main changes to first application on **1 January 2014** and is the one piece of this entry's legislative history that a retrieved text supports

(delib-riester_rente-r21)=

### R21 — *Betriebsrentenstärkungsgesetz* (BRSG), 2017
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established — the *Bundesgesetzblatt* text of the amending act was not located in this pass; what a consolidated statute shows is the **result** of the amendment, not the act
- Retrieved: no — the act itself was not opened. The entry is kept as a known reference for the legislative history, and the propositions it supports are marked below according to whether a retrieved consolidated text evidences them
- Used for: the last substantive Riester reform — the *Grundzulage* at **175 €** from contribution year 2018 [R9]; the *Kleinbetragsrenten-Abfindung* under the *Fünftelregelung* with a deferral election [R15]; the *Freibetrag* in the *Grundsicherung im Alter*; and the removal of the double *Krankenversicherung* charge on a bAV-sourced Riester annuity. **The first two are now read in the consolidated texts** — EStG § 84 Satz 1 dates the 175 € rate to contribution year 2018, EStG § 22 Nr. 5 Satz 13 carries the § 34 Abs. 1 reference and AltZertG § 1 Abs. 1 Satz 1 Nr. 4 Buchst. a the four-week deferral election. **The last two are not**, neither SGB XII nor SGB V being read here, and they keep their tags. AltZertG § 14 Abs. 2c refers to the act of **17 August 2017** and is the only date this pass can attribute to it. The product spec's reading of the set — every one a repair rather than an extension, none touching the *Beitragsgarantie* — is an inference from the four items and stays an inference

(delib-riester_rente-r22)=

### R22 — DeckRV § 2, the *Höchstzinssatz* (*Höchstrechnungszins*)
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/deckrv_2016/__2.html — the human-facing per-section page; text and *Stand* read from the canonical XML at https://www.gesetze-im-internet.de/deckrv_2016/xml.zip
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250, read 2026-08-30)
- Used for: the rate that carries the whole of the product spec's guarantee argument. **The current value is read and one of the two is not.** § 2 Abs. 1: "Bei Versicherungsverträgen mit Zinsgarantie, die auf Euro … lauten, wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf **1 Prozent** festgesetzt." The section is headed ***Höchstzinssatz***, and it caps the rate for the *Deckungsrückstellung*, which is why the technical notes are right that it is a reserving cap and not a promise a policy must make [REG-R14]. The **0,25 %** value for 2022–24 is **not in the current text** — a consolidated regulation carries only the rate in force — and it stays cited to the rate history at [REG-R15]; the amending instrument named in the *Stand* line, the Verordnung of **19 July 2024**, is the one that set 1 %. § 2 Abs. 2 supplies a rule the notes rely on and had not cited: "Bei Versicherungsverträgen mit Zinsgarantie gilt der von einem Versicherungsunternehmen **zum Zeitpunkt des Vertragsabschlusses** verwendete Rechnungszins für die Berechnung der Deckungsrückstellung **für die gesamte Laufzeit des Vertrages**" — which is exactly why `rechnungszins` is a model point attribute and not a library constant. Two retrieved carrier wordings now supply real tariff rates under the cap: **1,25 %** on a 01.15-vintage Riester tariff [S4] and **0,9 %** on a 01.01.2025-vintage one [S6], the latter **below** the 1,00 % cap of its own vintage. § 4 Abs. 1 of the same regulation carries the *Höchstzillmersatz*: "Der Zillmersatz darf **25 Promille** der Summe aller Prämien nicht überschreiten" [REG-R16]

(delib-riester_rente-r23)=

### R23 — Unisex pricing: the AltZertG rule and *Test-Achats*
- Publisher: Gesetze im Internet; Court of Justice of the European Union
- URL: https://www.gesetze-im-internet.de/altzertg/__1.html for the AltZertG limb; no URL established for the judgment
- Retrieved: **partly**. The AltZertG limb: yes (canonical XML, read 2026-08-30). The *Test-Achats* judgment: no — it was not located or opened in this pass
- Used for: the rule that a Riester contract is priced unisex, so `sex` is a reporting-only model point column that no rate may read. **The statutory limb is now read**: AltZertG § 1 Abs. 1 Satz 1 Nr. 2 requires "eine lebenslange und **unabhängig vom Geschlecht berechnete** Altersversorgung", and both retrieved wordings implement it in terms — "Die vereinbarte Rente ist unabhängig vom Geschlecht berechnet" [S2], "die versicherte und unabhängig von Ihrem Geschlecht kalkulierte Rente" [S4] — while [S6] names a "unternehmenseigene **geschlechtsunabhängige** Sterbetafel". **The dates are not read and keep their tags**: a consolidated statute shows the rule, never the date it entered, so **1 January 2006** for the AltZertG rule and **21 December 2012** for the general German market after *Test-Achats* (C-236/09) remain `[unverified]`, as does the six-year gap the documents draw from them and the conclusion that a Riester *Rentenfaktor* is not comparable with a same-vintage Schicht-3 one for a male life

(delib-riester_rente-r24)=

### R24 — BMF *Anwendungsschreiben* on the tax treatment of subsidised private pensions
- Publisher: Bundesministerium der Finanzen
- URL: not established — no BMF *Anwendungsschreiben* was located on the ministry's own site in this pass
- Retrieved: no — the document was not identified, so its date, reference number and content remain unestablished (gap 3). The entry is kept as a known reference
- Used for: nothing substantive. It is cited once, in the product spec, to record where German practitioners actually find the consolidated administrative guidance — on the *Günstigerprüfung*, the two-pool tracking, the *Rückzahlungsbetrag* calculation and the *Wohnförderkonto* arithmetic. **Its practical importance to this library has fallen sharply in this pass**: the statutory provisions behind three of those four mechanics were retrieved and read directly [R6] [R12] [R14], so the *Anwendungsschreiben* is now the place to check the administration of rules this library has otherwise seen, rather than the only place any of them could be checked

(delib-riester_rente-r25)=

### R25 — Riester contract statistics: BMAS quarterly series; GDV statistics
- Publisher: Bundesministerium für Arbeit und Soziales; Gesamtverband der Deutschen Versicherungswirtschaft
- URL: not established — neither the BMAS quarterly series nor a GDV statistics page was located in this pass
- Retrieved: no — neither series was identified or opened. The entry is kept as a known reference, and **every market figure in the product documents keeps its `[unverified]` tag** (gap 2)
- Used for: the market section's order-of-magnitude statements — the contract count and its split by chassis, the collapse of new business, and the large minority of the book that is *beitragsfrei gestellt*, which is the fact behind the technical notes' decision to carry *Beitragsfreistellung* as a model-point switch and to warn that a book projection built from these model points needs a paid-up cohort weight. **Every figure is `[unverified]` recollection; neither series was retrieved, and there is no official statistic for the *ruhende* share at all** (gap 2). This is the largest untouched gap left after this pass: the statutory and contractual halves of the product are now documented, the **market** half is not at all

(delib-riester_rente-r26)=

### R26 — *Fokusgruppe private Altersvorsorge* (2023) and the pAV-Reform / *Altersvorsorgedepot* debate
- Publisher: Bundesministerium der Finanzen (the working group); the federal government (the bill)
- URL: not established for the *Fokusgruppe* report or the bill; the **enacted** amendments are visible in the consolidated statutes at https://www.gesetze-im-internet.de/altzertg/ and https://www.gesetze-im-internet.de/vvg_2008/
- Retrieved: **partly**. The 2023 report and the 2024 draft bill: no — neither was located or opened. The 2026 legislation: **yes, at one remove** — the canonical XML of the AltZertG and the VVG was read on 2026-08-30 and both carry the amending act in their *Stand* lines
- Used for: the product spec's closing argument that every reform proposal begins with the 100 % *Beitragsgarantie*. The 2023 working group's recommendations and the fate of the 2024 draft bill were not read and keep their `[unverified]` tags. **Gap 1 — "the position at the access date is not established" — is now largely closed, from the statutes themselves.** The AltZertG *Stand* line names three amending articles, "Änderung durch Art. 5 / Art. 6 / Art. 7 **G v. 26.5.2026 I Nr. 156**, textlich nachgewiesen, dokumentarisch noch nicht abschließend bearbeitet", and the VVG's names "Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156" — one act of **26 May 2026**, published in **BGBl. I 2026 Nr. 156**, amending both. Its content is visible in the text: AltZertG § 5 now grants certification "nach § 1 Absatz 3 **in der ab dem 1. Januar 2027 geltenden Fassung**" against "§ 1 Absatz 1, **1a, 1b, 1c oder 1d**", and EStG § 93 Abs. 3 Satz 2 Nr. 2 adds a *Kleinbetragsrente* limb for "eine monatliche Leistung **ab dem 1. Januar 2027**" under an *Auszahlungsplan*. So the reform is law, it takes effect on **1 January 2027**, and it adds contract forms the present § 1 does not yet contain. **Two cautions.** The consolidation is **incomplete** — § 5 refers to paragraphs 1b, 1c and 1d that do not appear in the retrieved § 1 — so nothing may be asserted about what those new forms contain. And the amending act is identified here **only by the *Stand* lines of the instruments it amends**; the act's own title was not read, so no delib document may name it

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen; research
provenance in `_research/regulatory-actuarial.md`). That page went through the same re-verification
as this one: **its fifty-six entries now carry their own per-entry `Retrieved:` lines, the large
majority of them `yes`**, and it records per entry what was read and what was corrected. The
statement it used to carry here — that every entry on it records `Fetched: no` — is withdrawn.
Entries cited by the Riester documents:

- **REG-R5** — VAG 2016, the statute and its Anlage 1: the supervisory frame the provider sits in, and the *Sparte* this contract is written in.
- **REG-R6** — VAG §§ 74–110 and § 40: the best-estimate-plus-risk-margin structure the published `liability_cf` feeds, and the SFCR that reports it. Nothing here discounts.
- **REG-R14** — DeckRV § 2: the *Höchstrechnungszins* as a cap on the **reserving** rate rather than on what a policy may guarantee — the distinction the model's `rechnungszins` **[std]** rests on.
- **REG-R15** — the *Höchstrechnungszins* rate history and the Sechste Verordnung of 19 July 2024: the 0,25 % and 1,00 % values used with [R22], and the 1,00 % `annuity_rechnungszins`.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: the ceiling the model's initial commission is set at, and the German counterpart to the AltZertG's five-year spreading rule.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins* and the *Zinszusatzreserve*: named in the valuation pointers as out of scope, and the reason `rechnungszins` is a model point attribute rather than a library constant.
- **REG-R18** — MindZV: the statutory minimum allocation to the *Rückstellung für Beitragsrückerstattung*, which is the floor under the declared rate this model takes as an exogenous **[std]** scenario.
- **REG-R19** — RfBV: the collective RfB behind the same declared rate, and why a declared *laufende Verzinsung* is a management decision rather than an asset return.
- **REG-R20** — LVRG 2014: the commission and cost-disclosure reform that bounds the acquisition-charge and commission **[std]** levels.
- **REG-R22** — VVG 2008, Kapitel 5 and § 171: the contract law that governs a certified Riester insurance contract exactly as it governs a Schicht-3 one, subject to the AltZertG's overrides.
- **REG-R24** — VVG § 153, *Überschussbeteiligung* and the *hälftige* participation in *Bewertungsreserven*: the basis of `bewres_pp()` at *Rentenbeginn*.
- **REG-R28** — VVG §§ 165–170: *prämienfreie Versicherung* (the statutory limb of *Beitragsfreistellung*), *Kündigung*, the *Rückkaufswert* and the agreed and appropriate *Stornoabzug* — `cv_pp` and `stornoabzug_rate`, and the five-year-spreading floor under the surrender value which this model satisfies by construction.
- **REG-R29** — VVG §§ 172–177: the *Berufsunfähigkeitsversicherung* whose premium creates the guarantee carve-out here and whose own liability lives in `berufsunfaehigkeit`.
- **REG-R31** — VVG §§ 6, 7 and 214 with the VVG-InfoV: the advice, information and cost-disclosure duties that sit alongside the AltZertG's own [R4].
- **REG-R32** — PRIIPs: the parallel European disclosure regime, named to distinguish it from the AltZertG sheet.
- **REG-R33** — the IDD as transposed: the distribution regime behind the commission assumption.
- **REG-R34** — Unisex: EuGH C-236/09 (*Test-Achats*) and the AGG — the general rule Riester preceded by six years [R23].
- **REG-R35** — BaFin Merkblatt 01/2023 (VA), *Wohlverhaltensaufsicht* and *angemessener Kundennutzen*: the conduct lens a charge basis on a subsidised product is now read under.
- **REG-R36** — the BGH line of authority on German life contracts: the case law behind the surrender-value and *Stornoabzug* limbs.
- **REG-R38** — AltEinkG and the *Drei-Schichten-Modell*: the taxonomy [R18] states, in the cross-product form every delib product uses.
- **REG-R40** — ZPO §§ 850b and 851c, *Pfändungsschutz*: the execution protection that, with [R16], argues for a low surrender assumption.
- **REG-R41** — EStG § 22 Nr. 1 Satz 3 Buchst. a and § 55 EStDV: the *Ertragsanteil* the **unsubsidised** pool falls under, against the full taxation of the subsidised one [R12].
- **REG-R42** — EStG § 10a and Abschnitt XI (§§ 79–99), the Riester subsidy machinery: **the cross-product carrier of every figure in the subsidy chain** — the Zulagen amounts, the 4 % / 2 100 € / 60 € arithmetic, the proportional Kürzung, the ZfA lag and the *Kleinbetragsrente* threshold — reported at one remove from the product-level [R6] [R9] [R10] [R11] [R15].
- **REG-R43** — AltZertG, the BZSt, the AltvPIBV and the Produktinformationsstelle Altersvorsorge: the cross-product carrier of the certification criteria, the *Beitragserhaltungszusage*, the 30 % lump-sum cap, the five-year cost spreading and the **20 % biometric carve-out** that `guar_carve_out_cap` implements.
- **REG-R44** — the Altersvorsorgereformgesetz 2026 and the *Altersvorsorgedepot*: the reform that closed this product to new business, and the source of the **1 January 2027** valuation date the whole model point table opens at.
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6: the lump-sum tax rule the unsubsidised pool falls under, for contrast with § 22 Nr. 5.
- **REG-R46** — ErbStG and SGB V §§ 226, 229 and 240: contributions on an annuity in payment, and the *Bezugsgröße*-linked figures behind the two competing readings of the *Kleinbetragsrente* threshold.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: **why the two best-estimate factors run in opposite directions** (0.80 on the death basis, 1.15 on the annuity basis), and why no DAV table is redistributed here.
- **REG-R48** — DAV 2008 T: the death-benefit basis `mort_table_accum.csv` is a **[std]** proxy for.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand: the **generational** annuity basis `annuity_mort_table.csv` is a **[std]** proxy for, and the reason a period-table proxy would understate a seventeen-year-deferred annuitisation.
- **REG-R53** — the German life market in numbers: the region declared rates sat in during the mid-2020s, which is where the `base` scenario's 2,30 % comes from, and the statement that a declared *laufende Verzinsung* **includes** the *Rechnungszins*.
- **REG-R54** — HGB §§ 341–341o, RechVersV and BerVersV: the statutory accounts these cash flows are not, named in the valuation pointers.
- **REG-R55** — IFRS 17: the other measurement frame the published cash flows feed, likewise out of scope here.

---

## Provenance note

Extraction details — one entry per source with an extended *Content* block, the mechanics sections
the product documents are written from, and the nineteen-item gaps-and-caveats register — live in
`_research/riester_rente.md`. That file is the citation ground truth for the S# and R# numbering
used here.

**This paragraph was rewritten in the 2026-08-30 provenance pass and its predecessor is no longer
accurate.** What follows is the state of the entries above after that pass. The retrieval-conditions
block at the head of this file has since been rewritten to match, so the two now agree; if they ever
disagree again, the per-entry `Retrieved:` lines are the record and the header is the summary.

**What is now read.** Of the 42 entries above, **26 carry `Retrieved: yes`** and two more are part-retrieved; 14 remain `Retrieved: no`, in three groups — five *Bundesgesetzblatt* amending acts whose effect is visible in the consolidated statutes but whose own text was not opened [R17]–[R21], seven documents that could not be located on their publisher's own site [S5] [S7] [S8] [S11] [S12] [S13] [S16], and two where no single identifiable document exists to fetch [R24] [R25]. The **statutory half of the product is
documented end to end** from canonical XML with the law's *Stand* attached: AltZertG §§ 1, 1a, 2a, 3,
3a, 5, 7–7c and 14 [R1]–[R4]; the AltvPIBV [R5]; EStG §§ 10a, 22 Nr. 5, 79, 82–87, 89–95, 97 and
§ 34 [R6]–[R16]; DeckRV §§ 2 and 4 [R22]; and, from sibling instruments, VVG §§ 165 and 169 and
ZPO §§ 851 and 851c. **The carrier half is no longer empty.** Both GDV *Musterbedingungen* were
opened at "Stand: 21.07.2025" [S1] [S2]; a CosmosDirekt Riester AVB at edition LA 1005 A (01.15)
[S4]; a Debeka Riester AVB at edition B LV 94 (01.01.2025) [S6]; and four statutory
*Produktinformationsblätter* [S14], two of them carrying real *Effektivkosten*, real
*Chancen-Risiko-Klassen* and real *Zertifizierungsnummern* [S9].

**What that changed.** Gap 8 closes: the *Wechsel* charge is capped at **150 Euro** and the notice
period is three months to a quarter end [R1] [S2]. Gap 14 closes: the Zulagen **are** a charge base,
in the model wording and at three carriers, and acquisition cost on a Zulage is taken once at inflow
[S2] [S4] [S6] [S9]. Gap 6 largely closes: the AltvPIBV prescribes crediting **on 15 May of the year
after the contribution year** [R5]. Gap 15 closes: EStG § 95 bites from the start of the payout phase
and only outside the EU/EEA [R14]. Gap 1 largely closes: an act of **26 May 2026, BGBl. I Nr. 156**
amended the AltZertG and the VVG with effect from **1 January 2027** [R26]. Gap 9 is answered for
one house: the two-*Rentenfaktor* construction with a higher-of rule is drafted into a 2025-vintage
Riester wording [S6]. And gap 13 is answered on the disclosure side, though not on the tariff side.

**What is still not established, and where the risk now sits.** **Charge levels remain [std]** — one
carrier's full numbered basis is now in hand [S4], but one observation is not a market, and the
model's levels differ from it materially in both directions. **No behavioural rate was established**
— no *Stornoquote*, no *Beitragsfreistellung* rate, no transfer-out rate, no commutation take-up — so
every rate in that class is still an argument from the statutory consequences rather than from data
(gap 16). **No market figure was established** (gap 2): the BMAS and GDV series were not located, and
this is now the largest untouched gap in the corpus. **Historic rates and dates keep their tags**: a
consolidated statute shows the rule in force, never the sequence that produced it, so the Zulagen
phase-in [R17], the 2006 unisex date [R23] and the 0,25 % *Höchstzinssatz* regime [R22] are all
`[unverified]` still. And the BMF *Anwendungsschreiben* was not identified (gap 3).

**Two retrieved documents contradict this library and are flagged where they bite.** The
*Kleinbetragsrente* threshold is **1,5 %** of the monthly *Bezugsgröße*, not 1 % [R15]. And the GDV
model wording excludes commutation where the annuity falls to a *Kleinbetragsrente* **only because
of** an elected *Teilkapitalauszahlung*, which is the opposite of the ordering the model implements
[S2]. Both are recorded in the product documents and **neither was applied to the model**, which is a
deliberate deferral, not an oversight.

The honest summary has changed. The statutory half of this product is no longer a set of hypotheses:
it is read, quoted where quotation earns its place, and cited to a *Stand*. The carrier half is
**evidenced in structure and still standardized in level** — the shapes of the guarantee, the death
benefit, the charge base, the *Wechsel* and the commutation are now documented, while the numbers
that fill them remain **[std]** with their rationale stated where each is used.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-riester_rente-r1
[R10]: #delib-riester_rente-r10
[R11]: #delib-riester_rente-r11
[R12]: #delib-riester_rente-r12
[R13]: #delib-riester_rente-r13
[R14]: #delib-riester_rente-r14
[R15]: #delib-riester_rente-r15
[R16]: #delib-riester_rente-r16
[R17]: #delib-riester_rente-r17
[R18]: #delib-riester_rente-r18
[R19]: #delib-riester_rente-r19
[R2]: #delib-riester_rente-r2
[R21]: #delib-riester_rente-r21
[R22]: #delib-riester_rente-r22
[R23]: #delib-riester_rente-r23
[R24]: #delib-riester_rente-r24
[R25]: #delib-riester_rente-r25
[R26]: #delib-riester_rente-r26
[R3]: #delib-riester_rente-r3
[R4]: #delib-riester_rente-r4
[R5]: #delib-riester_rente-r5
[R6]: #delib-riester_rente-r6
[R7]: #delib-riester_rente-r7
[R8]: #delib-riester_rente-r8
[R9]: #delib-riester_rente-r9
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R40]: #delib-reg-r40
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R6]: #delib-reg-r6
[std]: #delib-std
<!-- END generated citation links -->
