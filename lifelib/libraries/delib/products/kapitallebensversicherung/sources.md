# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/kapitallebensversicherung.md` (the
citation ground truth for this product) and are **frozen — never renumber**. Unused sources are
omitted, so the numbering has gaps: **S14** (CosmosDirekt, "Erlebensfall: Was ist das und wie
läuft die Auszahlung?" — located, but the fused search summary attributed no statement to it, so
nothing in the product documents rests on it) and **R31** (the EUROPA Lebensversicherung and
Deutsche Lebensversicherungs-AG *Geschäftsberichte* 2024 — recorded in the research file as
locatable primary sources of per-undertaking *Stornoquoten* and cost ratios, with **no content
established**) are **not cited** by `product-spec.md`, `technical-notes.md` or `model.md` and are
therefore absent below. Access date at drafting: **2026-08-29**; the re-verification pass read on
**2026-08-30**, and each entry carries its own read date. No sources were newly added at drafting.
Cross-product [REG-R#] tags are listed in their own section at the end.

**The retrieval conditions, stated plainly, because they changed after this file was first
written.** delib was **drafted** under two limits, and both shaped every entry below. First,
**direct HTTP egress was blocked by an organisation network policy**: `WebFetch` and `curl` were
refused (HTTP 403 at the egress gateway) for every host outside a short package-registry allowlist,
and `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`, `bundesfinanzministerium.de`,
`dejure.org`, `buzer.de`, `destatis.de` and `de.wikipedia.org` were all tried and all refused, so
not one document listed here was retrieved — not a *Bedingungswerk*, not a
*Basisinformationsblatt*, not a statutory text, not a BaFin *Merkblatt*. Second, the session's
shared `WebSearch` budget of 200 calls was exhausted after **24 searches** on this product. The
first draft therefore rested on search-result summaries and on the authoring model's own knowledge
of German insurance law and practice, disciplined by the [std] and [unverified] tags — which is
why the statutory and supervisory core was researched to a usable depth and the insurer-by-insurer
parameter sweep was not.

**That policy has since been lifted, and these citations were re-verified against the primary
documents on 2026-08-30.** Of the forty-seven entries below, **forty-five now rest on a document
that was opened and read — 96 %** — and **two do not**. The statutory core arrives as canonical
XML from `gesetze-im-internet.de`, each instrument with its amendment status recorded: the VVG
[R1] to [R5], the MindZV [R6], the DeckRV [R7], the VAG [R8], the VVG-InfoV [R9] and the EStG
[R10]. The carrier material arrives as PDF — six *Bedingungswerke*, the GDV *Musterbedingungen*
[S1] and *Muster-Standmitteilung* [S2], the *Verbraucherinformationen* bound into the VPV wording
[S18] and one PRIIP-*Basisinformationsblatt* [S10] — and the consumer, trade-press and supervisory
material as HTML. Several entries cover a group of documents and record one of the group as
missing — [R11] a subscription login, [R19] a 404 on one article of three, [R26] a paywall, [R10]
the *Einkommensteuer-Handbuch* behind a bot interstitial, [R17] a press release — and the
`Retrieved:` line always names which. **The two failures are [S8]**, HTTP 404 at the cited die Bayerische URL with
no replacement found on that carrier's script-loaded document index, **and [R24]**, whose
rechtsportal.de report of the 2001–2007 BGH line answers HTTP 429; both are kept as known
references and nothing quantitative rests on either.

**So read a `Retrieved:` line before you rely on the entry above it.** `Retrieved: yes` means the
document was opened and the passage the entry rests on was read; a German sentence quoted in such
an entry is quoted from the instrument. Anything else leaves the entry a **pointer, not a
certificate** — it names the instrument a claim should be checked against, it does not assert that
anyone checked it — and a German sentence quoted there is quoted from a **search-result summary**.
Re-verification was not a formality: several entries below record a claim the drafted text got
wrong and now correct, among them the surplus base at [S3], the Debeka edition dates at [S4] and
[S5], the *Standmitteilung* field list at [S2] and the lapse figures at [R20]. Across delib as a
whole the coverage is materially thinner than it is here — roughly three entries in five are
`Retrieved: yes`, the rest naming what happened: a 404, a consent or JavaScript wall, a paywall, a
subscription login — so this product is one of the better-covered ones, and each sibling gives its
own count. Every URL below was retrieved directly, returned by a search, or is the obvious
canonical form of one; where there is none, the entry says `URL: not established` rather than
guessing.

---

## Primary product sources

(delib-kapitallebensversicherung-s1)=

### S1 — GDV, "Allgemeine Bedingungen für die kapitalbildende Lebensversicherung" (Musterbedingungen)
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V.; *Musterbedingungen* — model AVB published by the industry association for members to adopt, adapt or ignore, the GDV stating their use to be **unverbindlich** and purely optional
- URL: https://www.gdv.de/resource/blob/6348/075948efa290a72d0bb062dec766f56f/allgemeine-bedingungen-fuer-die-kapitalbildende-lebensversicherung-pdf-data.pdf (index: https://www.gdv.de/gdv/service/musterbedingungen)
- Retrieved: **yes** (PDF, 20 pp., `Stand: 21.07.2025`, read 2026-08-30) — the whole model wording, §§ 1–20, arrives as clause text
- Used for: the existence of a market-wide model wording, the second-person, question-headed drafting style of post-2008 VVG AVB (§ 1 is headed "Welche Leistungen erbringen wir?"), and the GDV's own competition-law disclaimer, printed above the title of the retrieved edition: "Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ." Now that the text is readable it is also the market template for the **clause shape** this library models — § 12 Abs. 3 restating the § 169 VVG surrender construction including the five-year spread floor; § 13 Abs. 1 computing the *beitragsfreie Versicherungssumme* "unter Zugrundelegung des Rückkaufswertes nach § 12 Absatz 3"; § 14 Abs. 2 applying "das Verrechnungsverfahren nach § 4 der Deckungsrückstellungsverordnung", with the amount so amortised "auf 2,5 % der von Ihnen während der Laufzeit des Vertrages zu zahlenden Beiträge beschränkt"; and § 2 Abs. 7, "Die Höhe der künftigen Überschussbeteiligung kann also nicht garantiert werden. Sie kann auch Null Euro betragen." **S1 still fixes no level, and no rate anywhere in delib is attributed to it.** Every quantitative field in the model wording is an ellipsis for the undertaking to fill: the *Abzug* in §§ 12 Abs. 4 and 13 Abs. 2, the minimum sums in § 13 Abs. 4, and — footnote 6 — the *Wartezeit*, the *Bemessungsgrößen für die Überschussanteile* and the *Rechnungsgrundlagen*, all relegated to "unternehmensindividuelle Angaben"

(delib-kapitallebensversicherung-s2)=

### S2 — GDV, "Jährliche Mitteilung zum Stand Ihrer Versicherung" (Muster-Standmitteilung, kapitalbildende Lebensversicherung, 02/2017)
- Publisher / doc type: GDV; model *Standmitteilung*, the annual statement sent to the policyholder. The GDV file name carries "02-2017"; **the retrieved document is dated 22 March 2018 in its own body** and is headed "Anlage 5"
- URL: https://www.gdv.de/resource/blob/6302/890c551440e2d065eba74180437f6970/5-gdv-muster-standmitteilung-kapitalbildende-lebensversicherung-02-2017-data.pdf
- Retrieved: **yes** (PDF, 7 pp., dated 22 March 2018 in the document body, read 2026-08-30) — the full field list, the glossary and the footnote apparatus
- Used for: the field list of the German annual statement — **and the retrieved document contradicts the four-quantity description this entry previously carried.** What the Muster-Standmitteilung actually reports is a roll-forward of the *Garantiertes Kapital* (opening balance, plus premiums, plus *Erträge*, less the year's *Abschluss- und Vertriebskosten* and *Verwaltungskosten*), then a "Für die Zukunft nicht garantierter Schlussüberschuss" and a "Für die Zukunft nicht garantierte Beteiligung an Bewertungsreserven" added to give a *Gesamtkapital*; separate blocks give the benefit at *Versicherungsablauf*, at death, at *Beitragsfreistellung* and at *vorzeitige Vertragsbeendigung*, each split into a guaranteed part and those same two non-guaranteed parts, with a three-column sensitivity at the current declaration and at ±1 percentage point. **There is no line called *Rückkaufswert* and none called *beitragsfreie Versicherungssumme***: the surrender figure appears as "Gesamte einmalige Zahlung" under *vorzeitige Vertragsbeendigung*, the paid-up figure as a maturity benefit computed on a paid-up basis. The document also names a ***Sockelbeteiligung an Bewertungsreserven***, which is the corroboration the *Sockelbetrag* at [R8] previously lacked; and it is the statutory *Standmitteilung* duty in the specification's regulatory context

(delib-kapitallebensversicherung-s3)=

### S3 — Debeka Lebensversicherungsverein a. G., Bedingungswerk **B LV 85** (edition 01.07.2026)
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., **21 pp.**, running header "B LV 85 (01.07.2026) Seite 1 von 21". **Not an endowment wording.** The retrieved document is titled "Allgemeine Bedingungen für eine Rentenversicherung mit aufgeschobener Rentenzahlung und Fondskomponenten nach Tarif CA2I (ABAR-IT 07/2026)" — a deferred annuity with a *garantiebasierter* and a *fondsgebundener Baustein*. Debeka's own document library [S6] files it under *Aufgeschobene Rentenversicherung*
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf
- Retrieved: **yes** (PDF, 21 pp., edition 01.07.2026, read 2026-08-30)
- Used for: **the quantified *Stornoabzug*, and nothing about endowment surplus.** § 34 imposes two deductions, both "in Prozent des Deckungskapitals": an *Ausgleich für die Veränderungen der Ertragslage des Versichertenkollektivs* keyed to the difference between the 10-year zero-coupon euro swap rate published by the Bundesbank three months before termination and its own ten-year average — "Kapitalmarktsituation 1 (Differenz von weniger als 0,5 Prozentpunkte): kein Abzug", 2 (0,5 to under 1 pp): 5 %, 3 (1 to under 1,5 pp): 10 %, 4 (from 1,5 pp): 15 % — and a flat *Ausgleich für kollektiv gestelltes Risikokapital* of "5 % des Deckungskapitals". **Both fall linearly to 0 % over the last ten years of the *Aufschubzeit***, and both lapse entirely on a *Kündigung* in the last five years once the life has passed 62 and the contract has run twelve years. That is the observation the [std] `storno_rate` schedule is set against, and it is a schedule on the reserve — but note that the range starts at nil, not at 5 %, and decays with duration, neither of which a flat schedule reproduces
- **Contradicted by retrieval, and corrected downstream.** The load-bearing surplus claim this entry previously carried is not in the document. § 30 Abs. 1 b sets *Zinsüberschussanteile* **monthly**, "in Prozent des Deckungskapitals" struck at the start of the month excluding the premium then due, and **first from the third *Versicherungsjahr***, not annually and not from inception; and § 30 Abs. 2 sets *Schlussüberschussanteile* not on the reserve at all but "in Prozent der Summe der während der Aufschubzeit für den Erwerb von Fondsanteilen verwendeten Zinsüberschussanteile". The allocated surplus is invested in a fund, not booked into the *Deckungskapital*. The reserve-as-surplus-base fact the model rests on is therefore now carried by [S18] and [S7], which are endowment wordings; S3 corroborates only that a German carrier declares interest surplus as a percentage of the reserve

(delib-kapitallebensversicherung-s4)=

### S4 — Debeka, Bedingungswerk **B LV 86** (edition 01.07.2026)
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., **19 pp.** Also **not an endowment wording**: "Allgemeine Bedingungen für eine Rentenversicherung mit aufgeschobener Rentenzahlung und Fondskomponenten nach Tarif CA6I (ABAR-IG 07/2026)"
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV86.pdf
- Retrieved: **yes** (PDF, 19 pp., edition 01.07.2026, read 2026-08-30). **The edition recorded here before this pass — 01.01.2025 — was wrong**: the URL is a current-version path and the document behind it now carries 01.07.2026
- Used for: the evidence that one insurer maintains **three parallel wordings for one product family**, which is the specification's variation argument. **Retrieval corrects what the three vary by.** They are not endowment wordings of different vintages: all three carry the *same* edition date, 01.07.2026, and differ by tariff — CA2I regular premium (S3), CA6I (S4), CA2IE single premium (S5). The cohort argument for `rechnungszins` and the two DeckRV ceilings survives, but it now rests on DeckRV § 2 Abs. 2 and § 4 Abs. 4 at [R7], which lock both to the rate used at conclusion for the whole term, and on the 4 %-era wording at [S7]

(delib-kapitallebensversicherung-s5)=

### S5 — Debeka, Bedingungswerk **B LV 97** (edition 01.07.2026)
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., **18 pp.** Likewise not an endowment wording: "Allgemeine Bedingungen für eine Rentenversicherung mit aufgeschobener Rentenzahlung und Fondskomponenten gegen Einmalbeitrag nach Tarif CA2IE (ABAR-IT-E 07/2026)"
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV97.pdf
- Retrieved: **yes** (PDF, 18 pp., edition 01.07.2026, read 2026-08-30); the 01.01.2025 edition recorded before this pass was wrong for the same reason as at [S4]
- Used for: the third member of the 85 / 86 / 97 triple — the single-premium sibling — and, still, for the disclosure in the specification and in `model.md` that **no carrier wording in this corpus publishes a mortality basis, an expense loading or a commission scale**. That holds after retrieval: none of the six carrier documents now read states a first-order mortality table, a *Verwaltungskostensatz* or a commission rate, so every such level in the model remains [std]

(delib-kapitallebensversicherung-s6)=

### S6 — Debeka, "Vertragsgrundlagen und weitere Informationen (Bedingungswerke, Tarifbedingungen, IPID etc.)" — Kapitalbildende Lebensversicherung
- Publisher / doc type: Debeka; insurer document-library index page
- URL: https://www.debeka.de/service/bedingungen/Lebensversicherung___Rentenversicherung/Lebensversicherung/Kapitalbildende_Lebensversicherung/index.html
- Retrieved: **yes** (HTML, read 2026-08-30). The cited path redirects to Debeka's single document library at `https://www.debeka.de/service/vertragsgrundlagen.html`, headed "Vertragsgrundlagen, Tarifbedingungen, IPID etc."
- Used for: the fact that **"Kapitalbildende Lebensversicherung" is a live heading in a major German insurer's own taxonomy** at the access date — it is there, under *Lebensversicherung*, in the retrieved index — which is the specification's market-role anchor on the manufacturer side; and the document types a German carrier publishes per product, the index offering *Bedingungswerke*, *Tarifbedingungen*, *Merkblätter* and an **IPID**, the German market labelling the pre-contractual summary with the EU IDD term. **Retrieval adds the sharper finding**: under that heading Debeka lists **no AVB at all** — only a *Steuermerkblatt*, a *Kirchensteuerinformationsblatt* and the AVB for a *Sterbegeldversicherung*. The three *Bedingungswerke* at [S3]–[S5] sit under *Aufgeschobene Rentenversicherung*. So the category is live in the taxonomy and empty of wordings: Debeka publishes no endowment AVB

(delib-kapitallebensversicherung-s7)=

### S7 — Gothaer, "Allgemeine Versicherungsbedingungen für die kapitalbildende Lebensversicherung"
- Publisher / doc type: Gothaer Lebensversicherung AG; AVB for the kapitalbildende Lebensversicherung, **12 pp.**, "Version: 05.12.2011", document stamp `215401 - 01.12`, served from the broker portal `partner.gothaer.de` through a streaming endpoint carrying a `scope` parameter. **One of the two genuine endowment wordings in the corpus** (with [S18]) — and, being pre-LVRG, the only one written under the old ceilings
- URL: https://partner.gothaer.de/StreamingServlet/app/dvz/DocumentDownload/215401?scope=makler_scope
- Retrieved: **yes** (PDF, 12 pp., version 05.12.2011, read 2026-08-30) — the endpoint serves the document to a public reader
- Used for: the benefit shape — § 3 I pays the *Versicherungssumme* at the *Ablauf* on survival and on death before it, "Mit der Auszahlung endet der Vertrag" in both branches; § 8 the reduction of the sum insured in whole or in part to a *beitragsfreie Summe*, with a floor of **1.500 EUR** below which § 7 Abs. 2 and 3 are paid instead and the contract ends — the quantified form of the § 165 VVG *Mindestversicherungsleistung* branch at [R3]; and **the surplus base, which S3 turned out not to supply**: § 5 II (4) "Es werden Jahresanteile zugewiesen. Diese bestehen aus einem Risikoanteil in Promille der Versicherungssumme und in Prozent des Risikobeitrags sowie einem Ertragsanteil in Prozent des maßgeblichen Deckungskapitals." That is `surplus_base_pp` — the reserve for the interest component, the sum insured and the risk premium for the risk component — from an endowment wording of a named carrier. Also the four *Überschussverwendung* systems by name (*Verzinsliche Ansammlung*, *Barauszahlung*, *Gewinnsystem BE* which "vor allem die Leistung Ihrer Versicherung im Erlebensfall verstärkt", *Gewinnsystem BS*), the *Schlussgewinnanteil* at *Ablauf* with a reduced amount on surrender and death, the half share of the *Bewertungsreserven* on termination subject to a declared *Mindestbetrag*, and the *Zillmerverfahren* at § 6 Abs. 2 with the amortisable amount limited "auf **4 %** der von Ihnen während der Laufzeit des Vertrags zu zahlenden Beiträge" — the pre-LVRG 40 ‰ ceiling, in a carrier wording, which is the primary evidence that `deckrv_table.csv`'s Zillmer column is a cohort fact
- **Two corrections retrieval forces.** First, "on death before the *Ablauftermin* no further premiums are due" is **not a rule of the ordinary endowment here**: it appears only in variant II, the *Kapitalversicherung auf festen Termin*, where the sum insured falls due at the fixed date irrespective of survival, so premiums must be stopped expressly. In variants I, III and IV the contract simply ends with the death payment. `prem_charged_pp`'s cessation rule and pitfall 11 are correct for a *Termfixversicherung* and are a consequence of contract termination otherwise. Second, § 4 Abs. 1 limits the insurer's liability to the *Rückkaufswert* on suicide "innerhalb von **zwei** Jahren nach Vertragsbeginn" — shorter than the three years of § 161 VVG, which § 171 VVG permits because it favours the policyholder, and a working illustration that the statutory period is a ceiling on the insurer's relief, not a market constant

(delib-kapitallebensversicherung-s8)=

### S8 — die Bayerische, "Allgemeine Bedingungen für die kapitalbildende Lebensversicherung", document **B 510121**
- Publisher / doc type: BL die Bayerische Lebensversicherung AG; AVB for a *Kapital-Lebensversicherung*. **The existence of this document is contested within the search evidence**: one search returned the URL under this title, a narrower search returned its sibling documents but not it and reported it "may not be publicly available online"
- URL: https://www.diebayerische.de/dam/jcr:e5f5f192-0edc-49b1-9be8-18c3cc503ae3/510121_avb_kapital-lebensversicherung.pdf
- Retrieved: **no** — HTTP 404 at the cited URL on 2026-08-30. The publisher's own site was searched once for a current path (`diebayerische.de` root and the `formular-download` pages); no replacement URL was found, the document index being script-loaded. The entry is kept as a known reference: **no content has ever been established from it**, and whether the document is public remains [unverified]
- Used for: nothing substantive. It is cited in the specification only to record the contradiction in the search evidence rather than resolve it, and to count a fourth carrier in the variations table with the note that no term of the wording is known. The 404 settles the availability question in one direction only — the *cited* URL is dead — and does not show that no such document exists

(delib-kapitallebensversicherung-s9)=

### S9 — die Bayerische, AVB **KlassikRente** (B 520136, 01.2025) and (B 520127, 01.2022)
- Publisher / doc type: BL die Bayerische Lebensversicherung AG; **two editions of one wording**, "Allgemeine Bedingungen für die moderne klassische Rentenversicherung (KlassikRente)", 14 pp. each — B 520136 (01.2025), internal reference 25L03, and B 520127 (01.2022), reference 22L03. **An annuity, not an endowment**, recorded as the nearest sibling wording found and used only where the rule transfers, which is said wherever the fact is used
- URL: https://www.diebayerische.de/dam/jcr:0936fd6c-71b9-453d-83f6-57ec76a76697/520136_avb_klassikrente.pdf and https://www.diebayerische.de/dam/jcr:0dcd832e-9107-44b4-a967-5e504c5c6fce/520127_avb_gezillmert_klassikrente.pdf
- Retrieved: **yes** (two PDFs, 14 pp. each, editions 01/2025 and 01/2022, read 2026-08-30)
- Used for: **the surplus allocation timing**, now verbatim from *Anlage 1* to the 01/2025 edition: "Während der ANSPARPHASE erhält Ihr Vertrag an jedem Bilanztermin (31.12. des Jahres) und zum Ablauf der ANSPARPHASE Zinsüberschussanteile zugeteilt und in das DECKUNGSKAPITAL des Vertrages gebucht (laufende Zinsüberschussanteile)." That is the model's annual, period-end, reserve-crediting convention and the [std] shift of the *Bilanztermin* to the policy-year end. The same *Anlage* refines it: the allocation is annual but **accrues monthly**, "dabei ist Zinsträger jeweils das am Anfang des Monats vorhandene DECKUNGSKAPITAL (inklusive eines ggf. fälligen Beitrags, abzüglich der zum Monatsbeginn fälligen Kosten)", so the base is the start-of-month reserve **including** the premium then due — a convention the annual model approximates rather than reproduces. Also **entitlement beginning with the start of cover**: "Der Anspruch auf Überschussbeteiligung beginnt sofort mit dem Versicherungsschutz", which is why `surplus_credit_pp` runs from `t_start()`; the glossary definition "Das Deckungskapital setzt sich zusammen aus den verzinsten Sparbeiträgen des Vertrags und den zugeführten laufenden Überschussanteilen"; § 2 Abs. 1 "Die Leistung aus der Überschussbeteiligung kann auch Null Euro betragen", which is the `nil` scenario made runnable; and a *Schlussüberschussanteil* that "bemisst sich monatlich nach einem Prozentsatz der maßgebenden Größe für den Zinsüberschuss" and may be redetermined for past years or dropped entirely
- **Contradicted by retrieval.** There is **no *gezillmerte* / non-*gezillmerte* pair.** Both documents are the same tariff, KlassikRente, in two editions two years apart, and **both are zillmered**: § 15 Abs. 2 is word-identical in the two, applying "das Verrechnungsverfahren nach § 4 der Deckungsrückstellungsverordnung" with the amortisable amount "auf 2,5 % der von Ihnen während der Laufzeit des Vertrages zu zahlenden Beiträge beschränkt". The file name `520127_avb_gezillmert_klassikrente.pdf` is the only place the word appears. `zillmer_on` and model point 13 are therefore **not** evidenced by a carrier pair; they remain a modelling device for the *Höchstzillmersatz* ceiling being a maximum and not a mandate, and this entry no longer supports them. *Anlage 2* to the 01/2025 edition does supply a **second quantified carrier deduction** — "Der Abzug beträgt 50 EUR plus 0,15 %" of the premiums fallen due to the cancellation date multiplied by the whole and part years remaining to the originally agreed *Rentenzahlungsbeginn*

(delib-kapitallebensversicherung-s10)=

### S10 — ÖSA, "Basisinformationsblatt — ÖSA StarthilfePlus (laufende Beitragszahlung)"
- Publisher / doc type: Öffentliche Lebensversicherung Sachsen-Anhalt (ÖSA Versicherungen); **PRIIP-Basisinformationsblatt**, 3 pp., `Stand Basisinformationsblatt 01.01.2024`, for a regular-premium variant of a product named *StarthilfePlus*
- URL: https://www.oesa.de/export/sites/oesa/_resources/download/privat/service/bib/OeSA-StarthilfePlus_laufend_20.pdf
- Retrieved: **yes** (PDF, 3 pp., Stand 01.01.2024, read 2026-08-30)
- Used for: the fact that it is the **only PRIIP-BIB for a German capital-forming life product in this corpus** — and, now that it is open, for figures rather than for their absence. The product type is settled: "Art: Versicherungsanlageprodukt in Form einer **Kapitallebensversicherung** mit garantierter Verzinsung nach deutschem Recht", though the benefit is a time-limited annuity from *Rentenbeginn*, the death scenario pays **0,00 €** at every horizon and the contract is continued premium-free on death before *Rentenbeginn*, so it is a savings contract with a premium waiver rather than the composite this library models. Its figures, for a 47-year-old with a 1.000 € annual premium over 20 years: risk indicator **3 of 7**; premium split "Durchschnittliche Versicherungsprämie für das abgesicherte Risiko: 9,40 % (94,05 €)" against "Durchschnittlicher Anlagebetrag: 90,60 % (905,95 €)"; total costs 468 € / 3.342 € / 6.216 € at 1, 10 and 20 years, with the annual cost impact **5,3 % pro Jahr** at 20 years, and an average return "voraussichtlich 2,4 % vor Kosten und -2,9 % nach Kosten"; entry costs 2,2 % and ongoing administration 28,5 % "der Summe aller Anlagebeträge"; and the Protektor statement that a shortfall can lead to "Abschlägen von bis zu 5 %". **This closes the corpus's absolute silence on charges** — one *Effektivkosten*-style figure now exists, for one product of one public-sector insurer, on the BIB's own model case. It is far too narrow to calibrate against, so every charge level in the model stays [std]; the specification cites it as an order of magnitude and as evidence of how wide the *Effektivkosten* range is, alongside [R18]

(delib-kapitallebensversicherung-s11)=

### S11 — Allianz, "Kapitallebensversicherung: Ihr umfassender Ratgeber", with "Lebensversicherung: Arten im Überblick" and "Lebensversicherung Auszahlung: Ablauf & Steuer"
- Publisher / doc type: Allianz Lebensversicherungs-AG; three insurer product and guide pages on the German consumer site
- URLs: https://www.allianz.de/vorsorge/kapitallebensversicherung/ · https://www.allianz.de/vorsorge/lebensversicherung/ · https://www.allianz.de/vorsorge/lebensversicherung/auszahlung/
- Retrieved: **yes** (three HTML pages, read 2026-08-30)
- Used for: the manufacturer-side market-role finding, verbatim from the *Arten im Überblick* page — "Die kapitalbildende Lebensversicherung wird heute **nur noch selten angeboten**. Viele Versicherungsunternehmen haben sie durch moderne private Rentenversicherungen ersetzt." — and the *Garantiezins*, which the *Kapitallebensversicherung* page states twice: "Das Bundesfinanzministerium hat den Garantiezins für Neuverträge seit dem 1. Januar 2025 auf 1,00 Prozent festgelegt", corroborating [R7] from the manufacturer side; the description of the product as a death cover combined with a savings process carrying a guaranteed minimum rate; the tax summary "nur die Hälfte des Ertrags versteuert, sofern Ihr Vertrag mindestens 12 Jahre gelaufen ist und Sie bei Auszahlung mindestens 62 Jahre alt sind", with the death benefit paid free of income tax, which is [R10] restated by a manufacturer; and the death cover being payable in full "schon ab der ersten Beitragszahlung"
- **Contradicted by retrieval, and consequential.** **The 2,70 % *laufende Verzinsung* is not on any of the three pages.** The only rate Allianz states there is the 1,00 % *Garantiezins*. The figure exists — [R26] reports Allianz holding the *laufende Verzinsung* "für die klassischen Lebens- und Rentenversicherungen konstant bei **2,7 Prozent**" — but it is trade-press reporting of the **2025** declaration for a combined classic life-and-annuity book, not a manufacturer statement about an endowment book for 2026. `decl_rate` on the `base` scenario and the anchor cell's interest surplus are therefore anchored to [R26], one year older than recorded and not endowment-specific, and the surrounding band is [R25]'s annuity average. The statement that the *Rückkaufswert* can fall below the premiums paid in the early years is also not on the Allianz pages; it is now carried by [S12], which says it in terms

(delib-kapitallebensversicherung-s12)=

### S12 — ERGO, "Ratgeber Kapitallebensversicherung"
- Publisher / doc type: ERGO Group; insurer guide page
- URL: https://www.ergo.de/de/Ratgeber/finanzielle_vorsorge/kapitallebensversicherung
- Retrieved: **yes** (HTML, read 2026-08-30) — the page is now separately attributable, which it was not before
- Used for: the **premium decomposition**, which ERGO states directly: "Der Beitrag für eine Kapitallebensversicherung lässt sich in 3 Teile untergliedern" — a *Risikoanteil* that "gleicht das Risiko vorzeitiger Versicherungsfälle aus", a *Kostenanteil* for one-off acquisition and ongoing administration costs, and a *Sparanteil* that "wird verzinslich angesammelt"; the **twelve-year minimum term** ("Die Vertragsdauer beträgt mindestens 12 Jahre"), stated there as the tax condition rather than as a tariff limit, together with maturity after completion of the 62nd year; the *Abgeltungsteuer* mechanics — 25 % *Kapitalertragsteuer* withheld on the full *Ertrag*, the halving claimed in the assessment and the withheld tax credited; and the surrender signature the Allianz pages turned out not to carry: "Der Auszahlungsbetrag kann unter anderem bei vorzeitiger Kündigung sogar geringer ausfallen als die eingezahlten Beiträge. Vor allem zu Beginn der Laufzeit ist das der Fall, da die erhobenen Abschlusskosten durch die eingezahlten Beiträge noch nicht gedeckt sind." **The minimum sum insured is not on the page**, so that row of the specification's typical-parameter table has no source in this corpus and is [std] with no observation behind it

(delib-kapitallebensversicherung-s13)=

### S13 — Sparkasse, "Kapitallebensversicherung — Für Rente & Familie vorsorgen"
- Publisher / doc type: Deutscher Sparkassen- und Giroverband; distributor product and guide page
- URL: https://www.sparkasse.de/pk/produkte/versicherung/vorsorge-und-risiko/lebensversicherung/kapitallebensversicherung.html
- Retrieved: **yes** (HTML, read 2026-08-30)
- Used for: the distribution finding that the German endowment is sold through the **savings-bank network** as well as through tied agents and brokers — the page carries no terms of its own and routes the reader to a local *Sparkasse* ("Mehr Informationen und konkrete Konditionen finden Sie bei Ihrer Sparkasse"), which is itself the evidence that pricing is set at the level of the distributing institution. That is what the specification uses to argue that the *Vertriebsweg* drives the acquisition-cost level and that a single [std] commission scale stands for a range this library cannot observe. It corroborates [S12]'s twelve-year minimum ("durch die mindestens zwölfjährige Laufzeit") and states no other parameter

(delib-kapitallebensversicherung-s15)=

### S15 — Verivox, "Kapitallebensversicherung", "Überschussbeteiligung" and "Zillmerung"
- Publisher / doc type: Verivox GmbH, a comparison portal — **secondary**, not a product document; three consumer explainer pages
- URLs: https://www.verivox.de/kapitallebensversicherung/ · https://www.verivox.de/lebensversicherung/themen/ueberschussbeteiligung/ · https://www.verivox.de/lebensversicherung/themen/zillmerung/
- Retrieved: **yes** (three HTML pages, read 2026-08-30)
- Used for: the consumer-facing statement of the ***Höchstzillmersatz*** rule, now verbatim from the *Zillmerung* page: "Angaben zum möglichen Höchstzillmersatz lassen sich in Paragraph 4, Abschnitt 1 der Deckungsrückstellungsverordnung (DeckRV) finden. Seit dem 1. Januar 2015 darf der Zillmersatz 25 Promille – also 2,5 Prozent – der gezahlten Prämien nicht überschreiten, die nicht dem Versicherungsschutz und der Deckung der Verwaltungskosten dienen." That is `deckrv_table.csv`'s second column and `check_zillmer_cap()`, with the effective date [R7] does not itself carry; the page also works a numerical example (25-year term, 100 € monthly, 30.000 € *Beitragssumme*, 750 € zillmered cost spread over 300 months). **The 40 ‰ predecessor is not on the retrieved page** — the cut from 40 ‰ is carried by [R29] and, primarily, by the 4 % ceiling written into the 2011 wording at [S7]. Also used for the *Überschussbeteiligung* and *Überschussverwendung* material in the specification's mechanics sections

(delib-kapitallebensversicherung-s16)=

### S16 — Finanztip, "Überschussbeteiligung Lebensversicherung: Arten & Höhe" and "Steuer auf Lebensversicherung"
- Publisher / doc type: Finanztip Verbraucherinformation gGmbH — **secondary**, consumer journalism; two explainers
- URLs: https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/ · https://www.finanztip.de/lebensversicherung-versteuern/
- Retrieved: **yes** (two HTML pages, read 2026-08-30)
- Used for: the clearest secondary statement of the surplus split into a *laufende Überschussbeteiligung* and a *Schlussüberschuss*, and the consumer-facing quotas: the insurer must pass on "90 Prozent des Zins- und Risikoüberschusses an Dich weitergeben (§§ 6, 7 MindZV). Beim Kostenüberschuss ist es die Hälfte (§ 153 Abs. 3 VVG)", with the *Bewertungsreserven* released "zu 50 Prozent". The specification records these **beside** the MindZV framing at [R6] and expressly does not treat them as the same rule, and retrieval shows why that caution was right: Finanztip's citation for the 50 % is **wrong** — the half share of the *übriges Ergebnis* is § 8 MindZV, while § 153 Abs. 3 VVG is the half share of the *Bewertungsreserven* at contract end, a different rule with a different base. Also used for the point that the *Schlussüberschuss* is paid at termination and is lost on early surrender, which is `term_bonus_pp`'s accrual shape

(delib-kapitallebensversicherung-s17)=

### S17 — HUK24, "Überschussbeteiligung der Risikolebensversicherung"
- Publisher / doc type: HUK24 AG (HUK-COBURG group); insurer guide page — **about term life, not endowment**
- URL: https://www.huk24.de/risikolebensversicherung/ratgeber-lebensversicherung/ueberschussbeteiligung
- Retrieved: **yes** (HTML, read 2026-08-30). **No endowment-specific statement is taken from it**
- Used for: the corroboration that the **sources** of surplus are described the same way across product lines by carriers themselves. **Retrieval narrows this.** The page does *not* use the four-component vocabulary: it names three drivers — "Höhe der am Kapitalmarkt erwirtschafteten Gewinne", "Kostenstruktur des Versicherers" and "Zahl der während der Vertragslaufzeit verstorbenen Versicherten" — and describes the two term-life application forms, *Todesfallbonus* and *Sofortrabatt*. So it corroborates the three *sources* (interest, cost, mortality) and the statutory obligation to participate "verursachungsorientiert und angemessen", but it is **not** a carrier use of the names *Zins-*, *Risiko-*, *Kosten-* and *Schlussüberschuss*. Those four names as market vocabulary now rest on the carrier wordings that use them — [S7], [S9] and [S18] — and on [S16]

(delib-kapitallebensversicherung-s18)=

### S18 — VPV Lebensversicherungs-AG, "Bedingungen und Verbraucherinformationen für die Kapital bildende Lebensversicherung" (01.2019)
- Publisher / doc type: **VPV Lebensversicherungs-AG** (Vereinigte Postversicherung); the customer document set for an endowment, **26 pp.**, stamp `2.MP.0401 01.2019 ZU`, containing the AVB für die Kapital bildende Lebensversicherung (01.2019), AVB vorläufiger Versicherungsschutz, AVB Unfalltod-Zusatzversicherung, Besondere Bedingungen Nachversicherungsgarantie, *Steuerinformationen*, *Allgemeine Verbraucherinformationen* and the *Satzung* of the Vereinigte Postversicherung VVaG. The `lawinsider.com` record that this entry originally cited is a stub that hosts no text and names the document's real location
- URL: https://www.deteassekuranz.de/wp-content/uploads/2021/05/Bedingungen-SterbegeldV-VPV.pdf (index record, title only: https://lawinsider.com/de/contracts/duGC9LpAVlC). **The file name says *SterbegeldV* and is wrong**; the document behind it is the endowment set named above
- Retrieved: **yes** (PDF, 26 pp., edition 01.2019, read 2026-08-30). The lawinsider record itself is a stub: it carries the title and the contract-type label and points at the URL above
- Used for: the **document pair** the German market delivers to a customer, *Bedingungen* **and** *Verbraucherinformationen*, which is the vocabulary the specification uses for the contract documentation set — and, since retrieval, for far more than that. This is **the second genuine endowment wording in the corpus** (with [S7]) and the most explicit one on surplus. § 2 Abs. 3 (a) states the interest surplus as a formula: "Das um ein Jahr mit dem Rechnungszins abgezinste Deckungskapital wird mit dem deklarierten Zinsüberschussanteilsatz multipliziert", with a *Risikoüberschussanteil* for premium-paying contracts equal to "des deklarierten Risikoüberschussanteilsatzes mit dem Risikojahresbeitrag" — the clearest carrier statement in the corpus that `surplus_base_pp` is the reserve, and that the base is the reserve discounted back one year at the technical rate. The same clause imposes a **one-year *Wartezeit*** and allocates "jeweils zu Beginn des Versicherungsjahres", against the no-waiting-period rule at [S9] and the three-year deferral at [S3] and [S7] tariff group A — the carriers differ, and the specification says so. § 2 Abs. 3 (b) runs a *Schlussüberschusskonto* fed by an annual *Schlussüberschussanteil* on the same base as the interest surplus, itself bearing a declared *Schlussüberschusszinssatz*, redeterminable for past years and able to fall to nil, which is `term_bonus_pp`'s accrual shape from a wording. § 2 Abs. 5 restates the *Sicherungsbedarf* cut-back in a carrier's own words — "Bewertungsreserven auf festverzinsliche Anlagen sind gemäß derzeitiger aufsichtsrechtlicher Regelung (vgl. § 139 Abs. 3 VAG) nur insoweit zu berücksichtigen, als sie einen ggf. vorhandenen Sicherungsbedarf (vgl. § 139 Abs. 4 VAG) übersteigen" — and § 2 Abs. 6 a *Mindestbeteiligung an den Bewertungsreserven*, the third independent witness to the *Sockelbetrag* at [R8]. § 12 Abs. 4 gives a **third quantified *Stornoabzug***, on a base unlike either of the others: "ein Stornoabzug in Höhe von 100 € für erhöhte Verwaltungsaufwendungen. Zusätzlich erfolgt ein Stornoabzug in Höhe von 0,2 % der Differenz zwischen Versicherungssumme und dem Rückkaufswert nach Abs. 3"

---

## Regulatory and actuarial references (product research numbering)

(delib-kapitallebensversicherung-r1)=

### R1 — VVG § 153, *Überschussbeteiligung*
- Publisher: Bundesministerium der Justiz (Gesetze im Internet); mirrored by dejure.org and buzer.de
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__153.html · https://dejure.org/gesetze/VVG/153.html
- Retrieved: **yes** (canonical XML from `gesetze-im-internet.de/vvg_2008/xml.zip`, `Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156`, read 2026-08-30). The `__153.html` page is a ~5 kB frameset shell carrying no statutory text and is kept only as the human-facing link; the reading is now **version-pinned**, which closes gap 15 for this section
- Used for: Abs. 1 — the entitlement to share in the surplus **and** the *Bewertungsreserven* "es sei denn, die Überschussbeteiligung ist durch ausdrückliche Vereinbarung ausgeschlossen; die Überschussbeteiligung kann nur insgesamt ausgeschlossen werden", which is why the specification says there is no partially participating German endowment; Abs. 2 — the *verursachungsorientiertes Verfahren*, which allocation in proportion to reserve implements, with § 268 Abs. 8 HGB amounts left out of account; Abs. 3 — annual redetermination of the *Bewertungsreserven* and, on termination, "wird der für diesen Zeitpunkt zu ermittelnde Betrag zur Hälfte zugeteilt und an den Versicherungsnehmer ausgezahlt", which is `bwr_rate`'s mechanism, together with the Satz 3 proviso that now names its provisions expressly — "insbesondere die §§ 89, 124 Absatz 1, § 139 Absatz 3 und 4 und die §§ 140 sowie 214 des Versicherungsaufsichtsgesetzes bleiben unberührt". Abs. 4, which moves the reference date to the end of the *Ansparphase* for annuities, does not apply to this product

(delib-kapitallebensversicherung-r2)=

### R2 — VVG § 169, *Rückkaufswert*
- Publisher: Bundesministerium der Justiz; mirrored by dejure.org, lxgesetze.de and buzer.de
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__169.html · https://dejure.org/gesetze/VVG/169.html
- Retrieved: **yes** (canonical XML, `Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156`, read 2026-08-30); the `__169.html` page is a 7 kB frameset shell and is kept as the human-facing link only
- Used for: **the whole surrender construction**, now quotable exactly. Abs. 3 Satz 1: "Der Rückkaufswert ist das nach anerkannten Regeln der Versicherungsmathematik mit den Rechnungsgrundlagen der Prämienkalkulation zum Schluss der laufenden Versicherungsperiode berechnete Deckungskapital der Versicherung, bei einer Kündigung des Versicherungsverhältnisses jedoch mindestens der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt; die aufsichtsrechtlichen Regelungen über Höchstzillmersätze bleiben unberührt." Those are `res_guar_pp`'s design decisions, including its reading of the reserve at `t + 1`, and `res_min_pp` is the floor in the same sentence. Abs. 4 puts the *Zeitwert* branch on *fondsgebundene* contracts and expressly not on this one. Abs. 5: "Der Versicherer ist zu einem Abzug ... nur berechtigt, wenn er vereinbart, beziffert und angemessen ist. Die Vereinbarung eines Abzugs für noch nicht getilgte Abschluss- und Vertriebskosten ist unwirksam." Abs. 7 adds the already-allocated *Überschussanteile* and the *Schlussüberschussanteil* provided for on *Kündigung*. Abs. 2, not previously recorded, caps the payable *Rückkaufswert* at the benefit that would fall due on a claim at the date of cancellation and directs the remainder to a *prämienfreie Versicherung* — a branch this library does not model and the specification now names

(delib-kapitallebensversicherung-r3)=

### R3 — VVG § 165, *Prämienfreie Versicherung*
- Publisher: Bundesministerium der Justiz; mirrored by buzer.de, LexMea and dejure.org
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__165.html · https://dejure.org/gesetze/VVG/165.html
- Retrieved: **yes** (canonical XML, `Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156`, read 2026-08-30); `__165.html` is a 4 kB shell
- Used for: the *Beitragsfreistellung* right at the end of the current *Versicherungsperiode* "sofern die dafür vereinbarte Mindestversicherungsleistung erreicht wird", and the failure branch — "Wird diese nicht erreicht, hat der Versicherer den auf die Versicherung entfallenden Rückkaufswert einschließlich der Überschussanteile nach § 169 zu zahlen" — the two branches `is_paid_up` and `lapse_rate` implement and model points 11 and 12 exercise; Abs. 2, the paid-up sum computed "mit den Rechnungsgrundlagen der Prämienkalkulation unter Zugrundelegung des Rückkaufswertes nach § 169 Abs. 3 bis 5 ... und im Vertrag für jedes Versicherungsjahr anzugeben", which is `bfz_si_pp`, why the paid-up sum inherits the five-year floor, and why the schedule is contractual and tabulated; and Abs. 3, which computes it net of *Prämienrückstände* and leaves the surplus entitlement untouched. The *Mindestversicherungsleistung* is quantified in two of the wordings read: **1.500 EUR** of sum insured at [S7] and a monthly **25 EUR** guaranteed minimum annuity at [S9]. The practical note that attached *Zusatzversicherungen* are regularly lost on paid-up is commentary, not statute, and is not in § 165

(delib-kapitallebensversicherung-r4)=

### R4 — VVG § 161, *Selbsttötung*
- Publisher: Bundesministerium der Justiz; mirrored by dejure.org, lxgesetze.de and rewis.io
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__161.html · https://rewis.io/gesetze/vvg/p/161-vvg/
- Retrieved: **yes** (canonical XML, `Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156`, read 2026-08-30); `__161.html` is a 4 kB shell
- Used for: the insurer not being liable "wenn die versicherte Person sich vor Ablauf von drei Jahren nach Abschluss des Versicherungsvertrags vorsätzlich selbst getötet hat", the exception "wenn die Tat in einem die freie Willensbestimmung ausschließenden Zustand krankhafter Störung der Geistestätigkeit begangen worden ist", Abs. 2 allowing the period to be **increased** by individual agreement, and — the rule the model turns on — Abs. 3, "Ist der Versicherer nicht zur Leistung verpflichtet, hat er den Rückkaufswert einschließlich der Überschussanteile nach § 169 zu zahlen", so the German rule is a benefit **substitution** and not a forfeiture. That is `benefit_death_pp`'s first-three-years branch and pitfall 7. Abs. 2 permits only an increase, but § 171 makes § 161 *halbzwingend*, so a shorter period is lawful because it favours the policyholder — and [S7] § 4 Abs. 1 writes **two** years, which is why the three years are a statutory ceiling on the insurer's relief and not a market constant

(delib-kapitallebensversicherung-r5)=

### R5 — VVG § 19, *Vorvertragliche Anzeigepflicht*
- Publisher: Bundesministerium der Justiz; commentary from ra-zn.de and fairtest.de
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__19.html · https://www.ra-zn.de/anzeigepflicht-19-vvg
- Retrieved: **yes** (canonical XML, `Stand: Zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156`, read 2026-08-30); `__19.html` is a 6 kB shell
- Used for: the question-bounded disclosure duty — Abs. 1 covers the circumstances known to the policyholder that are material and "nach denen der Versicherer in Textform gefragt hat"; the remedy ladder of Abs. 2 to 4, ending in Abs. 4 Satz 2 with the *anderen Bedingungen* becoming part of the contract retrospectively on the insurer's demand, which is the statutory home of the exclusion or ***Risikozuschlag*** `rating_factor` represents; Abs. 5, under which none of the rights exists unless the insurer gave a separate *Textform* warning; and Abs. 6, giving the policyholder an immediate right to cancel if a contract change raises the premium by more than **10 Prozent** or excludes the undisclosed risk. **One correction**: the five- and ten-year limits are in § 21 Abs. 3 VVG, not § 19, and § 21 was not researched, so the specification's underwriting section attributes them to the VVG generally and the exact locus stays [unverified]

(delib-kapitallebensversicherung-r6)=

### R6 — MindZV, *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung*
- Publisher: Bundesministerium der Justiz; mirrored by lxgesetze.de and buzer.de
- URLs: https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html · https://lxgesetze.de/mindzv/6
- Retrieved: **yes** (canonical XML from `gesetze-im-internet.de/mindzv_2016/xml.zip`, `Stand: Zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688`, read 2026-08-30). The consolidated `BJNR083100016.html` page is itself substantive, unlike the per-section shells
- Used for: the minimum allocations to the *Rückstellung für Beitragsrückerstattung*, now section by section: § 6 Abs. 1 — "90 Prozent der nach § 3 Absatz 1 anzurechnenden Kapitalerträge **abzüglich der rechnungsmäßigen Zinsen**"; § 7 — "90 Prozent des auf überschussberechtigte Versicherungsverträge entfallenden Risikoergebnisses"; § 8 — "50 Prozent des ... übrigen Ergebnisses"; with § 4 Abs. 1 defining the three results by reference to the *Versicherungsberichterstattungs-Verordnung* line items and directing that "Alt- und Neubestand ... getrennt betrachtet" werden. The specification presents this as the **origin** of the surplus and expressly not as what determines a declared rate
- **One correction from the text.** What § 6 Abs. 1 deducts before striking the 90 % is the ***rechnungsmäßige Zinsen*** — the technical interest already owed to the contracts — not, as this entry previously recorded, the *Aufwand für die Diskontierung der Deckungsrückstellung*. The distinction matters to the specification's account of where the interest surplus comes from: the minimum allocation is a quota of investment income **in excess of** the guarantee, which is exactly why a declared *laufende Verzinsung* is the guarantee plus a surplus and not a separate rate

(delib-kapitallebensversicherung-r7)=

### R7 — DeckRV — *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher: Bundesministerium der Justiz; buzer.de carries the amendment history
- URL: https://www.buzer.de/gesetz/12006/index.htm
- Retrieved: **yes** — the DeckRV as canonical XML (`Stand: Zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250`) and the buzer amendment history as HTML, both read 2026-08-30
- Used for: **the two cohort ceilings the model keys on `issue_year`**, both now read in the instrument. § 2 Abs. 1 Satz 1: "wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf **1 Prozent** festgesetzt". § 4 Abs. 1 Satz 2: "Der Zillmersatz darf **25 Promille der Summe aller Prämien** nicht überschreiten" — note the statutory base is the *Summe aller Prämien*, which the market and this library call the *Beitragssumme*. Those are `deckrv_table.csv`'s two value columns, `check_rechnungszins_cap()` and `check_zillmer_cap()`, and `alpha_rate` sitting at the ceiling. **The cohort keying is itself statutory**, which was previously an inference: § 2 Abs. 2 Satz 1 fixes the *Rechnungszins* used at conclusion "für die gesamte Laufzeit des Vertrages", and § 4 Abs. 4 does the same for the *Zillmersatz*
- **The dating tag is discharged, and the date corrected.** buzer's *Fassung* line reads "Text in der Fassung des Artikels 1 Sechste Verordnung zur Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz V. v. **19. Juli 2024** BGBl. 2024 I Nr. 250 **m.W.v. 1. Januar 2025**". The announcement date is 19 July 2024, not 24 July, and the 1 January 2025 effective date is confirmed. The rate history before 2025 and the 2015 date of the 25 ‰ cut are not in the current consolidated text and rest on [S15], [R15], [R29] and [REG-R15]

(delib-kapitallebensversicherung-r8)=

### R8 — VAG § 139, *Überschussbeteiligung*, and the *Sicherungsbedarf*
- Publisher: Bundesministerium der Justiz; summary obtained through dejure.org
- URL: https://dejure.org/gesetze/VAG/139.html
- Retrieved: **yes** (canonical XML from `gesetze-im-internet.de/vag_2016/xml.zip`, `Stand: Zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81`, read 2026-08-30); the dejure.org mirror was read as well
- Used for: the restriction that decides `bwr_rate`. Abs. 3, in full: "Bewertungsreserven aus direkt oder indirekt vom Versicherungsunternehmen gehaltenen **festverzinslichen Anlagen und Zinsabsicherungsgeschäften** sind bei der Beteiligung der Versicherungsnehmer an den Bewertungsreserven gemäß § 153 des Versicherungsvertragsgesetzes nur insoweit zu berücksichtigen, als sie einen etwaigen Sicherungsbedarf aus den Versicherungsverträgen mit Zinsgarantie gemäß Absatz 4 überschreiten." Abs. 4 defines the *Sicherungsbedarf* as the sum over contracts whose *maßgeblicher Rechnungszins* exceeds the *Bezugszins* of the actuarially valued interest obligation less the *Deckungsrückstellung*. **Retrieval narrows the rule**: the cut-back bites on fixed-income and hedging reserves, not on the whole of the *Bewertungsreserven*, which is why `bwr_rate = 0` is the base run for a book of guaranteed contracts in a rate-driven reserve position and not a universal statement. Abs. 2 Satz 3 adds that a *Bilanzgewinn* may be distributed only so far as it exceeds the *Sicherungsbedarf*
- **The *Sockelbetrag* tag is discharged, and the fact relocated.** It is **not** in § 139 VAG. It is a contractual and declaratory minimum, and three independent retrieved documents now carry it: the GDV Muster-Standmitteilung's "Sockelbeteiligung an Bewertungsreserven" [S2], the *Mindestbeteiligung* in *Anlage 1* to [S9], and [S18] § 2 Abs. 6 — "Sie erhalten jedoch einen Mindestwert als Beteiligung an den Bewertungsreserven. Diese Mindestbeteiligung an den Bewertungsreserven wird als zusätzlicher Schlussgewinn festgelegt." Its **existence** is therefore established and its **size** remains unobserved: every carrier sets it annually and every one of the three says it can fall away

(delib-kapitallebensversicherung-r9)=

### R9 — VVG-InfoV § 2, and the *Effektivkosten* disclosure
- Publisher: Bundesministerium der Justiz; mirrored by buzer.de; explained by the Institut für Finanz- und Aktuarwissenschaften (ifa Ulm)
- URLs: https://www.gesetze-im-internet.de/vvg-infov/__2.html · https://www.buzer.de/gesetz/8025/a153312.htm
- Retrieved: **yes** — § 2 VVG-InfoV in full from `gesetze-im-internet.de/vvg-infov/__2.html`, which for this small instrument serves the norm text rather than a frameset, read 2026-08-30; the buzer.de mirror was read as well
- Used for: the cost-disclosure duty, now precise. Abs. 1 Nr. 1 requires the *einkalkulierte Abschlusskosten* "als einheitlicher Gesamtbetrag" and the other costs, with the *Verwaltungskosten* separately, as a share of the annual premium with the relevant term; Abs. 2 requires Nr. 1, 2, 4 and 5 to be given **in Euro**, which is the euro-amount duty this entry recorded. Abs. 1 Nr. 4, 5 and 6 require the *Rückkaufswerte*, the *Mindestversicherungsbetrag* for a conversion to a paid-up or reduced contract, and the extent to which both are guaranteed — the statutory origin of the *Garantiewerttabelle* the wordings at [S7] and [S18] refer the reader to. Abs. 1 Nr. 9 defines the ***Effektivkosten*** as "die Minderung der Wertentwicklung durch Kosten in Prozentpunkten ... bis zum Beginn der Auszahlungsphase", and **Abs. 6 fixes the method**: they "werden berechnet wie der Gesamtkostenindikator nach Anhang VI der Delegierten Verordnung (EU) 2017/653". That is why the technical notes treat the figure as a **validation target rather than an input** — reproducing one needs Annex VI and a holding period, neither of which this library implements. Abs. 3, not previously recorded, quantifies the § 154 VVG *Modellrechnung*: it must be shown at "dem Höchstrechnungszinssatz, multipliziert mit 1,67" and at that rate plus and minus one percentage point — at today's ceiling, 1,67 % with a 0,67 %–2,67 % band
- The date on which the *Effektivkosten* duty was introduced is still not established from the instrument: the current § 2 Abs. 6 refers to a 2017 delegated regulation as amended in 2019, while the 1 January 2015 start date rests on [S15], [R19] and [R29]. That much remains [unverified]

(delib-kapitallebensversicherung-r10)=

### R10 — EStG § 20 Abs. 1 Nr. 6, and the *Einkommensteuer-Handbuch* annex
- Publisher: Bundesministerium der Finanzen (amtliches Einkommensteuer-Handbuch); commentary from NWB and Haufe
- URLs: https://esth.bundesfinanzministerium.de/esth/2024/C-Anhaenge/Anhang-22a/I/inhalt.html · https://www.haufe.de/steuern/steuerwissen-tipps/nach-dem-31122004-abgeschlossene-lebensversicherungen_170_448252.html
- Retrieved: **yes for the statute, no for the handbook.** § 20 and § 52 EStG were read as canonical XML (`Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197`) on 2026-08-30. The *Einkommensteuer-Handbuch* URL answers 200 with a Radware interstitial — "Verifying your browser before proceeding" — and no document body, so **the handbook annex itself is not retrieved**; the Haufe commentary was read
- Used for: the ***Unterschiedsbetrag*** and the half-income rule, now from the instrument. § 20 Abs. 1 Nr. 6 Satz 1 taxes "der Unterschiedsbetrag zwischen der Versicherungsleistung und der Summe der auf sie entrichteten Beiträge (Erträge) im Erlebensfall oder bei Rückkauf des Vertrags ... bei Kapitalversicherungen mit Sparanteil, wenn der Vertrag nach dem 31. Dezember 2004 abgeschlossen worden ist"; Satz 2 halves it where the benefit is paid "nach Vollendung des 60. Lebensjahres des Steuerpflichtigen und nach Ablauf von zwölf Jahren seit dem Vertragsabschluss". **The age-62 locus tag is discharged and the citation corrected**: it is **§ 52 Absatz 28 Satz 7 EStG** — "§ 20 Absatz 1 Nummer 6 Satz 2 ist für Vertragsabschlüsse nach dem 31. Dezember 2011 mit der Maßgabe anzuwenden, dass die Versicherungsleistung nach Vollendung des 62. Lebensjahres des Steuerpflichtigen ausgezahlt wird" — not § 52 Abs. 36 Satz 9. The personal marginal rate rather than the *Abgeltungsteuer* where the halving applies is commentary, corroborated by [S12], which describes the 25 % withholding on the full *Ertrag* and the halving claimed back in the assessment. **The tax rules do not enter the projected cash flows**: they fix the anchor cell's twenty-five-year term ending at attained age 62, and the lapse table's twelve-year shape

(delib-kapitallebensversicherung-r11)=

### R11 — BMF-Schreiben of 1 October 2009, IV C 1 - S 2252/07/0001
- Publisher: Bundesministerium der Finanzen; *BMF-Schreiben*, binding administrative guidance to the tax offices
- URL: https://datenbank.nwb.de/Dokument/351401/ (NWB database record)
- Retrieved: **partly** — the NWB record page was read on 2026-08-30 (HTML) and yields the full citation, subject and *Gliederung*; **the Randnummern themselves are behind a subscription login and are still not established**
- Used for: naming the administrative guidance under which the *Mindesttodesfallschutz* test at [R12] is applied. Retrieval adds the **Bundessteuerblatt citation, BStBl 2009 I S. 1172**, the official subject "Besteuerung von Versicherungserträgen im Sinne des § 20 Absatz 1 Nummer 6 EStG", and the section structure — I to XIV, with "IV. Kapitalversicherung mit Sparanteil / 1. Kapitalversicherung auf den Todes- und Erlebensfall (klassische Kapital-Lebensversicherung)" and "X. Hälftiger Unterschiedsbetrag / 6. Mindesttodesfallschutz". So the guidance is now located precisely and its relevant section confirmed to exist; **no sentence of its text is quoted anywhere in delib**

(delib-kapitallebensversicherung-r12)=

### R12 — *Mindesttodesfallschutz*: the 50 %-rule for contracts concluded from 1 April 2009
- Publisher: Haufe (Haufe Finance Office Premium) and IWW (*Wirtschaftsberatung aktuell*) — secondary commentary
- URLs: https://www.haufe.de/id/beitrag/kapitallebensversicherungen-einkommensteuer-3121-einzelheiten-der-50-regel-HI8459275.html · https://www.iww.de/wvm/archiv/kapitallebensversicherungen-neuer-mindesttodesfallschutz-fuer-ab-dem-1-april-2009-abgeschlossene-vertraege-f14610
- Retrieved: **yes** for both commentaries (HTML, read 2026-08-30) — **and the rule itself is now read in the statute**, § 20 Abs. 1 Nr. 6 Satz 6 EStG, which supersedes both as the authority
- Used for: the **50 %-Regel**, whose statutory form is narrower than the summary this entry carried. Satz 6 disapplies the halving where **both** limbs hold: (a) "in einem Kapitallebensversicherungsvertrag **mit vereinbarter laufender Beitragszahlung in mindestens gleichbleibender Höhe** bis zum Zeitpunkt des Erlebensfalls die vereinbarte Leistung bei Eintritt des versicherten Risikos **weniger als 50 Prozent der Summe der für die gesamte Vertragsdauer zu zahlenden Beiträge** beträgt", and (b) the benefit on the insured event does not exceed the *Deckungskapital* or *Zeitwert* "**spätestens fünf Jahre nach Vertragsabschluss** ... um mindestens 10 Prozent des Deckungskapitals, des Zeitwerts oder der Summe der gezahlten Beiträge". That is the constraint on `death_ratio`, checked when the model point table is built rather than being a model formula
- **The tag on the second limb is discharged in full.** Its base is any of the three named — *Deckungskapital*, *Zeitwert* or premiums paid; its time profile is "at the latest five years after conclusion"; and the trailing qualifier that would not parse is Satz 6 Satz 2: "Dieser Prozentsatz darf bis zum Ende der Vertragslaufzeit in jährlich gleichen Schritten auf Null sinken." Retrieval also sharpens the application date: § 52 Abs. 28 Satz 8 applies the provision to contracts concluded after 31 March 2009 **or where the first premium was paid after that date**

(delib-kapitallebensversicherung-r13)=

### R13 — The pre-2005 regime and the 2004/2005 boundary
- Publisher: Haufe; Bund der Steuerzahler; VLH; smartsteuer — secondary commentary
- URLs: https://www.haufe.de/steuern/steuerwissen-tipps/nach-dem-31122004-abgeschlossene-lebensversicherungen_170_448252.html · https://steuerzahler.de/bayern/newsticker-archiv/newsticker/news/kapitallebensversicherungen-versteuerungsregeln-sehr-differenziert/
- Retrieved: **yes** for the Haufe and Bund-der-Steuerzahler pages (HTML, read 2026-08-30)
- Used for: the 1 January 2005 boundary and the taxation of the *Unterschiedsbetrag* on post-2004 contracts, which § 20 Abs. 1 Nr. 6 Satz 1 EStG at [R10] now states directly ("wenn der Vertrag nach dem 31. Dezember 2004 abgeschlossen worden ist"). That is what makes the specification's book **three tax cohorts** — pre-2005, 2005–2011 and 2012 onwards — and what fixes delib's composite as a post-2011 contract. **The conditions of the pre-2005 regime remain [unverified]**: they are not in the current statute, which knows the old regime only through transitional provisions, and the retrieved commentary states them only in outline. [S12] gives the outline a carrier's voice — a pre-2005 contract's death benefit is tax-free only if it met "die damaligen Voraussetzungen einer steuerbegünstigten Kapitallebensversicherung ... (Mindestlaufzeit 12 Jahre, laufende Beitragszahlung, Mindesttodesfallschutz)" — and nothing in delib asserts them

(delib-kapitallebensversicherung-r14)=

### R14 — DAV, "Herleitung der Sterbetafel DAV 2008 T für Lebensversicherungen mit Todesfallcharakter"
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; *Fachgrundsatz* / *DAV-Richtlinie*, with a 2008 derivation paper and a 2022 restatement
- URLs: https://aktuar.de/content/PDF/Fachwissen/20080708_DAV_2008_T.pdf · https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf
- Retrieved: **yes** (two PDFs: the 2008 derivation paper and the *Richtlinie* of 29 November 2022, 49 pp., read 2026-08-30). **The table values themselves are not redistributed here**
- Used for: the name and provenance of the first-order basis the shipped `mort_table.csv` **stands in for**, and the market-coverage figure, which the derivation paper states exactly: "Nach dieser Bereinigung weisen die untersuchten Versichertendaten eine Abdeckung von **60% des deutschen Versicherungsmarktes im Bereich der Kapitallebensversicherungen** auf; im Bereich der Risikolebensversicherungen sind es sogar 70%." The data are the pooled portfolios of Gen Re, Münchener Rück, Swiss Re and the Verband öffentlicher Versicherer — 47 undertakings, more than 100 million *Bestandsjahre* — read against the *Sterbetafeln des Statistischen Bundesamts*. The *Richtlinie* fixes the method for the *Sicherheitszuschläge* — the *Schwankungs-*, *Irrtums-* and *Änderungsrisiko*, with the *Schwankungszuschlag* struck on a model portfolio of 200.000 lives aged 20 to 65 — which is what `mort_be_factor = 0.75` represents. And the suitability limit, verbatim: "Die Sterbetafel DAV 2008 T ist grundsätzlich auch für die Beitragskalkulation von Lebensversicherungen mit Todesfallcharakter, **ausgenommen Tarife ohne Gesundheitsprüfung**, geeignet", so the whole basis presupposes the underwriting the specification describes
- **Two corrections from the documents.** The **observation period is 2001 to 2004**, not 2006–2008: "Als Beobachtungszeitraum werden die Jahre 2001 bis 2004 zu Grunde gelegt." 2006–2008 is when the DAV working group did the work, which the *Richtlinie* states separately. And the open question is answered: **there is no distinct first-order table for endowment as against term business.** DAV 2008 T is a single *Schlusstafel* built from data from the sixth policy year onwards to eliminate selection; about 91 % of the observations behind it come from *Kapitallebensversicherungen*, and endowment mortality from the sixth year sits at 101 % of the all-tariff level, which the paper calls marginal

(delib-kapitallebensversicherung-r15)=

### R15 — DAV recommendations on the *Höchstrechnungszins* for 2025 and 2026
- Publisher: Deutsche Aktuarvereinigung e. V.; two newsroom items
- URLs: https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-empfiehlt-auch-fuer-2026-einen-hoechstrechnungszins-in-hoehe-von-1-prozent/ · https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-begruesst-ministeriumsvorstoss-zum-hoechstrechnungszins-2025/
- Retrieved: **yes** (two HTML newsroom items, read 2026-08-30)
- Used for: the DAV recommending **1,0 % for 2026 as well**, which is the basis for holding `deckrv_table.csv` flat at 1,00 % for issue years after 2026 **[std]**; and the specification's point that the maximum technical rate is **set by regulation but proposed by the actuarial profession**, the recommendation having been adopted in both cycles evidenced here

(delib-kapitallebensversicherung-r16)=

### R16 — GDV, "Höchstrechnungszins-Erhöhung ist eine 'angemessene Reaktion auf gestiegene Zinsen'"
- Publisher: GDV; *Medieninformation*
- URL: https://www.gdv.de/gdv/medien/medieninformationen/hoechstrechnungszins-erhoehung-ist-eine-angemessene-reaktion-auf-gestiegene-zinsen--176848
- Retrieved: **yes** (HTML, read 2026-08-30). **Adds no independent figure**
- Used for: the industry association's public support for the increase to 1,0 %, cited in the specification's regulatory context to corroborate [R7] and [R15] and to show that the 2025 change was uncontested across the profession, the ministry and the industry

(delib-kapitallebensversicherung-r17)=

### R17 — BaFin, Merkblatt 01/2023 (VA), *zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden Lebensversicherungsprodukten*
- Publisher / doc type: BaFin; supervisory *Merkblatt*, published May 2023 — **the most important supervisory document for this product**
- URLs: https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html · https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Pressemitteilung/2023/pm_2023_05_08_Merkblatt_kapitalbildende_LV.html
- Retrieved: **yes** for the *Merkblatt*, whose full text (Rn. 1 ff., sections A to D) is served on the page and was read 2026-08-30; **no** for the press release, which is HTTP 404 at the cited URL. **The reading confirms that the *Merkblatt* itself states no numerical threshold** — not for *Effektivkosten*, not for commission, not for the real return; the "über vier Prozent" observation belongs to [R18], and is a BaFin survey finding rather than a *Merkblatt* limit
- Used for: the scope — Rn. 2 defines *kapitalbildende Lebensversicherungsprodukte* as classic and unit-linked life products with a savings component, including *Direktversicherungen* and AltZertG contracts; the ***Renditeziel*** duty at Rn. 15, under which undertakings must formulate return targets consistent with their target market and "auch prüfen, ob die Angehörigen des Zielmarktes nicht nur eine positive Rendite nach Kosten, sondern auch eine positive Rendite nach Kosten und Inflation anstreben", with the ECB medium-term inflation target named as a candidate benchmark and attainment to be tested "mit geeigneten stochastischen Analysen"; the cost-and-return interaction at Rn. 18, which names the *Effektivkosten* computed under § 2 Abs. 1 Nr. 9 i. V. m. § 2 Abs. 6 VVG-InfoV as the measure of total cost; and the *Storno* limb at Rn. 23 with the distribution-remuneration limb at Rn. 52, where BaFin suggests tying a high *Abschlussprovision* to the intermediary's own *Stornoquote*. This is why the specification treats charge levels as a **supervised rather than a free** parameter, while shipping every one of them as [std]
- **One qualification retrieval forces.** The *Renditeziel* duty is **not** flat across products. Rn. 16 and 17 provide that where the target market is *sicherheitsorientiert* the value of the guarantee may take precedence and "die Formulierung eines Renditeziels und die Prüfung, ob dieses mit hinreichender Wahrscheinlichkeit erreicht wird, ist dann gegebenenfalls entbehrlich" — and Rn. 17 names "klassische Lebensversicherungsprodukte ohne fondsgebundene Komponenten", which is exactly this product, as the paradigm case

(delib-kapitallebensversicherung-r18)=

### R18 — BaFin, *Risiken im Fokus 2026* — "Kosten von kapitalbildenden Lebensversicherungen"
- Publisher / doc type: BaFin; annual supervisory risk-focus publication, 2026 edition, consumer-protection chapter
- URL: https://www.bafin.de/DE/die-bafin/publikationen-daten/risiken-im-fokus/Fokusrisiken_2026/RIF_Verbraucher_3/RIF_verbraucher_lebensversicherung_node.html
- Retrieved: **yes** (HTML, full chapter text, read 2026-08-30)
- Used for: the fact that the product's charge level is a **named focus risk in BaFin's 2026 risk agenda**, three years after the *Merkblatt* — and now for the chapter's figures, which are the only supervisory quantities in the corpus. Market size: "Im Jahr 2024 gab es hierzulande rund **59 Millionen** kapitalbildende Lebensversicherungen. **2,4 Millionen** Verträge wurden in dem Jahr neu abgeschlossen", on the *Merkblatt*'s broad definition, so classic and unit-linked together. Costs: a 2022 survey of first-half-2021 new business found that "**In Einzelfällen beliefen sich die Effektivkosten auf über vier Prozent**", and a repeat survey in 2025 covering 2024 new business found them falling since 2021 — "vor allem bei den verkaufsstarken langen Laufzeiten war im oberen Viertel ein Rückgang der Effektivkosten um mehr als 0,4 Prozentpunkte zu beobachten". Lapse: "Einige Lebensversicherungsprodukte sind mit sehr hohen Stornoquoten aufgefallen – speziell in den ersten Jahren nach Vertragsabschluss, in denen ein großer Teil der Kosten anfällt", a high early-lapse rate being treated as evidence of an inadequate *Kundennutzen*. And the enforcement record: products withdrawn from the market, cost reductions in the in-force book, retrospective compensation, and *Verwarnungen* issued to individual *Geschäftsleiter*. This is the evidence for the specification's treatment of early-duration lapse as a supervised quantity and of the *Effektivkosten* as the measure a German endowment is judged by. The one-sentence product definition the specification's overview follows is not on this page and comes from the associated BaFin consumer page in the same result family, which was not separately retrieved

(delib-kapitallebensversicherung-r19)=

### R19 — BaFin *Fachartikel*: "Wenn Lebensversicherungen zu viel kosten" (2022), "PRIIPs-Verordnung" (2022), "Kundennutzen im Fokus" (2024)
- Publisher: BaFin (BaFinJournal / Fachartikel)
- URLs: https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2203_Effektivkosten_Versicherer.html · https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2207_priips_surfday.html · https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2024/bafin_fachartikel_wohlverhalten.html
- Retrieved: **partly** — "Wenn Lebensversicherungen zu viel kosten" (2022) and "Kundennutzen im Fokus" (2024) were read as HTML on 2026-08-30; the PRIIPs *Surfday* article is **HTTP 404** at the cited URL
- Used for: the **content requirements of a *Basisinformationsblatt*** — total risk indicator, maximum loss, four graded performance scenarios (*Stress*, *pessimistisch*, *moderat*, *optimistisch*) as annualised returns at three time points, and total costs with the Reduction in Yield split into one-off and ongoing — which the technical notes cite when explaining why the *Effektivkosten* is a validation target the model does not compute. With the PRIIPs article gone, that list is now best evidenced not by BaFin but by the retrieved BIB itself at [S10], which prints every one of those fields, and by the Franke und Bornberg piece at [R27]

(delib-kapitallebensversicherung-r20)=

### R20 — GDV, "Die deutsche Lebensversicherung in Zahlen 2024"
- Publisher: GDV; industry statistical annual and the Jahresmedienkonferenz page
- URLs: https://www.gdv.de/resource/blob/180978/b8ae8eb0b1bf4b15e7cc3354bc231af9/die-deutsche-lebensversicherung-in-zahlen-2024-publikation-pdf-data.pdf · https://www.gdv.de/gdv/statistik/jahresmedienkonferenz-zahlen-und-daten/lebensversicherung-2024-165748
- Retrieved: **yes** (PDF, 40 pp., *Redaktionsschluss* 27.06.2024, read 2026-08-30; the Jahresmedienkonferenz page as HTML)
- Used for: the ***Stornoquote*** — **and retrieval corrects both figures and both descriptions.** The publication titled *2024* reports the **2023** financial year, and gives one measure, not two: "Die Stornoquote (**Anzahl**) stieg im Jahr 2023 leicht auf **2,56 %** (Vorjahr: 2,51 %)." So 2,56 % is the **count** measure, not a premium- or *Bestand*-weighted one; the 2,72 % attributed to 2024 and the separate 1,2 % count measure are **not in this document** and are not established anywhere in the corpus. The substantive point survives intact and is now better founded: the GDV measure is a headline *Stornoquote* over all life business, is not endowment-specific and is not split by duration, which is the evidence base for pitfall 10 and for `lapse_table.csv` being **[std]** rather than calibrated
- Also used, and new to this pass, for the **endowment-specific market figures** the corpus previously lacked. In-force at 31 December 2023 by annual premium: "Der Anteil der Kapitalversicherungen (klassisch) lag Ende 2023 bei **15,7 %** (Vorjahr: 17,0 %)", against 61,8 % for annuity and pension business. New business 2023 with regular premiums: klassische Kapitalversicherungen **158 Mio. Euro**, a **3,9 %** share, up 8,2 %. Single premiums 2023: 1,1 Mrd. Euro of the 24,5 Mrd. total. And the count series for *eingelöster Neuzugang* of klassische Kapitalversicherungen, which quantifies the collapse [R21] said was unquantified: **1.954,9 Tsd. (26,8 %) in 2000 → 1.354,2 (18,5 %) in 2005 → 742,1 (12,1 %) in 2010 → 527,2 (10,3 %) in 2015 → 392,3 (8,4 %) in 2020 → 325,3 (7,4 %) in 2023**

(delib-kapitallebensversicherung-r21)=

### R21 — GDV statistics, "Neugeschäft und Bestand der Lebensversicherer für die letzten zehn Geschäftsjahre"
- Publisher: GDV; statistical series pages
- URL: https://www.gdv.de/gdv/statistik/statistiken-zur-deutschen-versicherungswirtschaft-uebersicht/lebensversicherung/neugeschaeft-und-bestand-der-lebensversicherer-fuer-die-letzten-zehn-geschaeftsjahre-137804
- Retrieved: **yes** (HTML index of the statistical series, read 2026-08-30). The series pages themselves are download links; **the numbers used below come from [R20]**, which is the same publisher's annual and was retrieved in full
- Used for: the **shape** of the published series — gross written premiums for the *Bestand*, and the ***Beitragssumme*** and Annual Premium Equivalent for the *Neugeschäft* — which is why the specification treats the *Beitragssumme* as a headline market measure and why the model publishes `beitragssumme()` as a derived quantity rather than only the annual premium. [R20] supplies the definitions verbatim: the APE adds 10 % of single premiums to the annual premium, assuming a ten-year term for single-premium contracts, while the *Beitragssumme* weights regular premiums by their payment term and adds the whole single premium, and is therefore "sehr viel größer als das APE". For 2023 the APE was 8,9 Mrd. Euro (−1,1 %) and the *Beitragssumme des Neugeschäfts* 175,4 Mrd. Euro (2022: 170,6). **The statement that no endowment-specific figure was established is withdrawn** — see [R20]

(delib-kapitallebensversicherung-r22)=

### R22 — BGH on the Debeka *Stornoabzug*: the *Bezifferung* requirement
- Publisher: Bundesgerichtshof; reported by LTO, LTMK and Cash.
- URLs: https://www.lto.de/recht/nachrichten/n/bgh-ivzr18424-debeka-stornogebuehr-transparenz-zurueckverweisung-olg-angemessen · https://www.ltmk.de/kapitalmarktabhaengiger-stornoabzug-in-der-lebensversicherung-bgh-klaert-die-anforderungen-an-die-bezifferung/
- Retrieved: **yes** (both HTML reports, read 2026-08-30). **Both tags are discharged**: the LTO report gives the citation in full — "Urt. v. **18.03.2026**, Az. **IV ZR 184/24**" — so the docket is no longer an inference from a URL slug and the decision date is established
- Used for: the holding that ***beziffert*** does **not** require a concrete euro amount at conclusion. LTO: the clause satisfies "die im Versicherungsvertragsgesetz (VVG) festgelegten Anforderungen an die Bezifferung des Abzugs gem. § 169 Abs. 5 S. 1 VVG", is not void for want of transparency under § 307 Abs. 1 Satz 2 BGB, and "Die Vorschrift verlange nicht, dass der Abzug bereits zu Vertragsschluss als konkreter Betrag vereinbart werde. 'Vielmehr kann der Versicherer auch auf die Regelung eines Berechnungsverfahrens für den Stornoabzug zurückgreifen.'" So a **capital-market-dependent** *Stornoabzug* is lawful in principle and the deduction need not be constant. The BGH set aside the OLG Koblenz judgment and remitted, the *Angemessenheit* question never having been examined below, which is why the specification records the Debeka schedule as **unresolved at the access date**. The rider that the procedure must leave the insurer no *Ermessensspielraum* is **not** in either retrieved report; it is dropped rather than attributed

(delib-kapitallebensversicherung-r23)=

### R23 — BGH, judgment of 20 January 2021, IV ZR 318/19 — *Bewertungsreserven* after the LVRG
- Publisher: Bundesgerichtshof; reported by rewis.io, NWB and RWS-Verlag
- URL: https://rewis.io/urteile/urteil/e7b-20-01-2021-iv-zr-31819/
- Retrieved: **yes** (HTML, full judgment text from rewis.io, read 2026-08-30). The disposition of the parallel constitutional challenge to § 153 Abs. 3 Satz 3 VVG is still **not established** and remains [unverified]
- Used for: the leading post-LVRG authority confirming that the half share of § 153 Abs. 3 VVG is **cut back by the *Sicherungsbedarf*** on contracts with interest guarantees and that the cut-back is lawful — the case law behind `bwr_rate = 0` and behind the specification's statement that the exit half share has frequently been nil

(delib-kapitallebensversicherung-r24)=

### R24 — The older BGH line on *Rückkaufswert* and *Stornoabzug* clauses (2001–2007)
- Publisher: Bundesgerichtshof; reported by verbraucherrecht.at and rechtsportal.de
- URL: https://www.rechtsportal.de/Rechtsprechung/Rechtsprechung/2007/BGH/Wirksamkeit-der-Klauseln-ueber-den-Stornoabzug-und-die-Hoehe-des-Rueckkaufswerts-in-der-Kapitallebensversicherung
- Retrieved: **no** — the cited rechtsportal.de page answers **HTTP 429** (rate limited) on 2026-08-30, and no alternative locus for the 2001–2007 line was retrieved; the entry is kept as a known reference and everything below stands on the earlier search summaries
- Used for: the case law that produced the present § 169 — clauses failing to distinguish clearly between the *Rückkaufswert* and the *Stornoabzug* held void, and a deduction left to the insurer's discretion or named only after the *Kündigung* failing the transparency requirement. This is why the model treats `storno_rate` as a **contractual, pre-declared schedule** read from a table rather than as a decision taken at the exit

(delib-kapitallebensversicherung-r25)=

### R25 — Assekurata, 24. Marktstudie "Überschussbeteiligungen und Garantien 2026"
- Publisher: Assekurata Assekuranz Rating-Agentur GmbH; market study, reported by finanzwelt
- URL: https://www.assekurata-rating.de/2026/03/04/assekurata-marktstudie-zu-ueberschussbeteiligungen-und-garantien-2026/
- Retrieved: **yes** (HTML press release for the 24th edition, published March 2026, read 2026-08-30). **The critical caveat is confirmed by the text, not merely suspected**: Assekurata's figures are stated "in der klassischen privaten Rentenversicherung", so they are annuity averages, and that an endowment book shares the rate remains [unverified]
- Used for: the market-average *laufende Verzinsung*, verbatim: "In der klassischen privaten Rentenversicherung erhöht sich die laufende Verzinsung für 2026 im Branchendurchschnitt auf **2,62 %** (Vorjahr: 2,53 %). Inklusive Schlussüberschüssen liegt die in Aussicht gestellte Gesamtverzinsung bei durchschnittlich **3,23 %** (Vorjahr: 3,19 %)", with *Neue Klassik* at 2,65 % laufend and 3,32 % total. The specification prints this beside the 2,7 % Allianz declaration — which, after this pass, comes from [R26] and is the 2025 rate — to show that the anchor cell sits at the top of a narrow band. Also the attribution of the caution to "weiterhin vorhandene **stille Lasten** in den Kapitalanlagen sowie vorsichtige Prognosen zur Zinsentwicklung", which is why `decl_rate` is held level rather than trended, and the new-business finding that "nur noch **elf** der untersuchten Gesellschaften überhaupt klassische private Rentenversicherungen im Neugeschäft anbieten"

(delib-kapitallebensversicherung-r26)=

### R26 — Trade-press reporting on the 2026 declarations and the market position of *Klassik*
- Publisher: VersicherungsJournal, procontra, Versicherungsbote, Biallo, Versicherungsmonitor
- URLs: https://www.versicherungsjournal.de/markt-und-politik/etwa-jeder-dritte-lebensversicherer-erhoeht-die-ueberschussbeteiligung-154961.php · https://www.procontra-online.de/lebensversicherung/artikel/lebensversicherung-2026-klassik-wird-zur-nische · https://www.procontra-online.de/lebensversicherung/artikel/allianz-verzichtet-auf-erhohung-der-uberschussbeteiligung
- Retrieved: **partly** — the two procontra articles were read in full as HTML on 2026-08-30; the VersicherungsJournal piece is **paywalled**, its body reserved to premium subscribers, so only the headline and the standfirst were read
- Used for: **the declared rate the anchor cell rests on**, which after this pass is sourced here rather than at [S11]: procontra reports Allianz holding the *laufende Verzinsung* "für die klassischen Lebens- und Rentenversicherungen konstant bei **2,7 Prozent**", with *Perspektive* at 2,8 % — a **2025** declaration for a combined classic life-and-annuity book, and the nearest thing in the corpus to a manufacturer figure for an endowment. The same piece gives Alte Leipziger at 2,25 % laufend / 2,45 % total and LVM at 2,4 % / 3,1 %, which is the band the specification prints. Also **about one in three life insurers raising the *Überschussbeteiligung* for 2026** — the VersicherungsJournal headline of 27 January 2026, whose standfirst records a survey of "fast 50 Anbieter mit rund 87 Prozent Marktanteil" but whose figures are behind the paywall — and the trade characterisation "Klassik wird zur Nische", which with [S11]'s "nur noch selten angeboten" is the evidence base for the specification modelling **a large in-force book with a thin new-business layer**. The description of the 2024 *Stornoquote* as an eight-year high is **not** in the retrieved articles and is not established

(delib-kapitallebensversicherung-r27)=

### R27 — DAV, *Ergebnisbericht* — Standardverfahren PRIIP Kategorie 4 (1 July 2025); Franke und Bornberg on *Basisinformationsblätter*
- Publisher: Deutsche Aktuarvereinigung e. V.; Franke und Bornberg GmbH
- URLs: https://aktuar.de/content/PDF/Fachwissen/2025-07-01_DAV_Ergebnisbericht_LV_Standardverfahren_PRIIP_Kategorie_4.pdf · https://www.franke-bornberg.de/blog/basisinformationsblaetter-bib-zu-anlageprodukten-welche-informationen-liefern-bibs
- Retrieved: **yes** (PDF, 30 pp., Köln, 1 July 2025, read 2026-08-30; the Franke und Bornberg blog post as HTML). No figure is taken from the Franke und Bornberg piece
- Used for: the existence of a **profession-agreed standard method** for PRIIP *Kategorie 4* — and the report says in its own preamble why that matters: "Dieser Bericht stellt im Sinne des Anhangs II der RTS zu PRIIP einen 'robusten, anerkannten Branchen- oder Regulierungsstandard' dar", and it works "ein geeignetes Standardverfahren für PRIIP der Kategorie 4 zur Ermittlung des Marktrisikomaßes (MRM) und der Performance-Szenarien" using recognised standard capital-market models. That is what the specification cites for the point that a German BIB's risk indicator and performance scenarios come from a common method rather than from each insurer's own model, and hence that reproducing one is out of this library's scope. **One caveat retrieval adds**: the report names *Rentenversicherungen der 3. Schicht* as the products it has principally in view, so its application to an endowment is by analogy

(delib-kapitallebensversicherung-r28)=

### R28 — Actuarial and lexicon reference works on *Deckungskapital*, *Zillmerung* and *Überschussverwendung*
- Publisher: various — DGVFM/DAV teaching series; Universität zu Köln; Universität Heidelberg; Gabler/Versicherungsmagazin lexicon; VersWiki; Wikipedia. **Secondary throughout**, and the search summaries **fused them**, so attribution is to the group
- URLs: https://werde-aktuar.de/content/DGVFM/PDF/Schulmaterialien/DGVFM_Band_4_Lebensversicherung.pdf · https://www.versicherungsmagazin.de/lexikon/gezillmerte-nettopraemie-1945423.html · https://www.deutsche-versicherungsboerse.de/verswiki/index_dvb.php?title=Lebensversicherung%3A_Zillmerung · https://www.deutsche-versicherungsboerse.de/verswiki/index_dvb.php?title=Ratenzahlungszuschlag
- Retrieved: **yes** (the DGVFM Band 4 teaching PDF and the three lexicon pages, read 2026-08-30). **No formula is copied from them into delib**: the prospective reserve is standard actuarial content, used as a [std] construction and cited to no source
- Used for: the ***Deckungskapital*** / ***Deckungsrückstellung*** distinction, which is why this library projects the former and references the latter; the ***gezillmerte Nettoprämie*** and *Zillmerung* reducing the reserve by the present value of unrecovered acquisition costs so that **a negative *Deckungskapital* arises in the early years**, which is `res_zill_pp(1) = -alpha_cost`; the four *Überschussverwendung* systems and — the discriminating fact the model turns on — that the *verzinsliche Ansammlung* gives a **higher payment at maturity** while the *Bonussystem* gives **higher death benefits**; and the ***Ratenzahlungszuschlag*** at 2 % half-yearly, 3 % quarterly and 5 % monthly, with the ***echte*** / ***unechte*** distinction that makes the loading inert on a genuine sub-annual *Versicherungsperiode*

(delib-kapitallebensversicherung-r29)=

### R29 — LVRG legislative and market-impact material
- Publisher: Deutscher Bundestag (GDV *Stellungnahme*); Pfefferminzia; Versicherungsbote; AssCompact
- URLs: https://www.bundestag.de/resource/blob/284406/e26d0309aa9989f59485ae83bf52bca9/08-GDV-data.pdf · https://www.pfefferminzia.de/vertrieb/untersuchung-zeigt-abschlusskosten-sinken-nach-lvrg-um-fast-8-prozent-1469012604/ · https://www.versicherungsbote.de/id/4804227/LVRG-Lebensversicherung-Provision-Modelle/
- Retrieved: **yes** for the Pfefferminzia and Versicherungsbote reports and the Bundestag *Stellungnahme* PDF, all read 2026-08-30. **The "almost 8 %" study is now attributed**: it is the **LV-Check of the magazine Procontra**, which "seit 2009 die Bilanzen der relevantesten deutschen Lebensversicherer im engeren Sinne untersucht", reported on 20 July 2016, and the figure is **7,9 %**, with the *Beitragssumme des Neuzugangs* down only 5,7 % over the same period so the fall is not a volume effect. **No *Stornohaftung* period was established** and none is asserted
- Used for: the *Lebensversicherungsreformgesetz* and its *Höchstzillmersatz* cut, which Versicherungsbote states in the form the model needs: "Für die Zillmerung bei Lebensversicherungspolicen sieht das LVRG eine Höchstgrenze von 25 Promille der Prämien ab dem kommenden Jahr vor. In der Bilanz kann der Versicherer somit von ursprünglich **4,0 Prozent** nur noch 2,5 Prozent der Beitragssumme als Vertriebs- und Abschlusskosten geltend machen." That is the 40 ‰ predecessor, corroborating the 4 % ceiling written into the 2011 wording at [S7]; and the reported 7,9 % fall in *Abschlusskosten*
- **Two corrections retrieval forces, one of them consequential.** First, the same sentence continues: "**Eine Deckelung der Provisionen ist gesetzlich nicht vorgesehen.** Höhere Provisionen können daher von den Versicherern gezahlt werden, sind jedoch aus anderen Töpfen zu nehmen." The LVRG caps what may be *zillmered and recognised*, not what may be *paid* — so the ceiling constrains `alpha_rate`, and it does not constrain `comm_init_rate` at all. Second, **the Die Stuttgarter figure is not in either retrieved article.** The only carrier named is **ERGO**, and only qualitatively: a stepwise redistribution in which "eine höhere Bestandsprovision dann eine geringere Abschlussprovision ausgleicht". There is therefore **no named-carrier commission figure anywhere in this corpus**, and `comm_init_rate = 2.5 %` and `comm_renew_rate = 1.5 %` are [std] with no observation behind them — which is what the specification and `model.md` now say

(delib-kapitallebensversicherung-r30)=

### R30 — Verbraucherzentrale material on the Debeka *Stornoabzug* collective action
- Publisher: Verbraucherzentrale Bundesverband and its Land bodies (Hamburg, Niedersachsen)
- URLs: https://www.verbraucherzentrale.de/verfahren/debeka/faq · https://www.vzhh.de/themen/versicherungen/lebens-rentenversicherung/urteil-stornoabzug-der-debeka
- Retrieved: **yes** (both HTML pages, read 2026-08-30). The framing is adversarial and the figures are the consumer bodies', not Debeka's, but they now match the wording read at [S3] and the legal press at [R22]
- Used for: the running **collective action over the *Stornoklauseln***, and the quantified deduction structure, which the vzbv FAQ states in terms: "Neben dem üblichen Stornoabzug von 5 Prozent wurde eine zusätzliche Stornogebühr erhoben. Ihre Höhe richtete sich nach der jeweiligen Kapitalmarktsituation und konnte 5, 10 oder 15 Prozent des Deckungskapitals betragen." The observed total range for that carrier is 5 % to **20 %**, which is the observation the [std] `storno_rate` schedule is set against, and the specification says so in the table itself. Retrieval settles the cohort question the entry left open: the class action covers policyholders who took out a Debeka life or annuity contract **after 2007** and cancelled it, "besonders betroffen" being those cancelling from **1 May 2022**; the vzhh page adds that the OLG Koblenz had prohibited the clause and the BGH reversed. And [S3] supplies what the consumer bodies omit — a fourth *Kapitalmarktsituation* carrying **no** deduction at all, and both components running linearly to nil over the last ten years before maturity, so the schedule's floor is 0 % rather than 5 %

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen; research
provenance in `_research/regulatory-actuarial.md`). **The [REG-R#] entries were not re-checked in
this pass**, which upgraded the product-level S# and R# entries above; their retrieval status is
whatever `references/regulatory-and-actuarial-references.md` records. Where a [REG-R#] tag restates
a product-level entry — REG-R9 for [R8], REG-R14 to REG-R16 for [R7], REG-R18 for [R6], REG-R24 for
[R1], REG-R28 for [R2] and [R3], REG-R45 for [R10] and [R12] — the retrieved statutory text is the
one above, and that is what the specification and the technical notes cite. Entries cited by the
kapitalbildende Lebensversicherung documents:

- **REG-R1** — Richtlinie 2009/138/EG (Solvabilität II): the framework the projected cash flows feed and which this library does not implement.
- **REG-R2** — Delegierte Verordnung (EU) 2015/35: the same, at the level of the standard formula and contract boundaries.
- **REG-R3** — Richtlinie (EU) 2025/2, the Solvency II review: named in the specification's regulatory context as pending.
- **REG-R4** — EIOPA risk-free term structures, the UFR and the *Volatilitätsanpassung*: the discount curves a valuation layer would apply to `liability_cf`.
- **REG-R5** — VAG 2016, its architecture and Anlage 1: the *Sparte* this product is written in.
- **REG-R6** — VAG §§ 74–110 and § 40: best estimate, risk margin, SCR/MCR and the SFCR — cited as the layer above this one.
- **REG-R8** — VAG § 138, *Prämienkalkulation* and *Gleichbehandlung*: the statutory frame for the first-order pricing basis.
- **REG-R9** — VAG § 139 and the *Sicherungsbedarf* test on *Bewertungsreserven*: the cross-product statement of the rule at [R8], and the argument for `bwr_rate = 0`.
- **REG-R10** — VAG §§ 140 and 145, the RfB and the *Verordnungsermächtigung*: the provision the declared surplus is paid out of, and which the model does not carry.
- **REG-R11** — VAG §§ 141–143, the *Verantwortlicher Aktuar* and the 1994 deregulation: why a German tariff is no longer approved in advance.
- **REG-R12** — VAG §§ 221–236 and § 314, Protektor and the supervisor's crisis powers: the § 314 write-down the specification names as out of scope.
- **REG-R14** — DeckRV and its § 2: the *Höchstrechnungszins* as a reserving-regulation quantity, keyed by cohort.
- **REG-R15** — the *Höchstrechnungszins* rate history and the Sechste Verordnung of 19 July 2024: the source of `deckrv_table.csv`'s first column, and of its two split-year [std] entries.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: the source of the second column, and of `check_zillmer_cap()`.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins*, the *Zinszusatzreserve* and the *Korridormethode*: named and expressly not modelled.
- **REG-R18** — MindZV, the minimum allocation to the RfB: the cross-product statement of [R6].
- **REG-R19** — RfBV, the collective part of the RfB: cited for the *Schlussüberschussanteilfonds* the model does not carry.
- **REG-R20** — LVRG 2014: the statute behind the 25 ‰ cut and the *Effektivkosten* disclosure.
- **REG-R21** — BaFin, the FinDAG, the MaGo and the *Auslegungsentscheidungen*: the supervisory frame around [R17] and [R18].
- **REG-R22** — VVG 2008, Kapitel 5 and § 171 (*halbzwingende Vorschriften*): why §§ 153, 161, 165 and 169 cannot be contracted around to the policyholder's detriment.
- **REG-R24** — VVG § 153 and the *hälftige Beteiligung*: the cross-product statement of [R1].
- **REG-R25** — VVG §§ 154 and 155, *Modellrechnung* and *Standmitteilung*: the statutory duty behind [S2].
- **REG-R26** — VVG §§ 150, 159–162: *Einwilligung*, *Bezugsberechtigung* and the *Selbsttötung* rule at [R4].
- **REG-R27** — VVG § 163, *Prämien- und Leistungsänderung*: cited in pitfall 16 for what a *Beitragsverrechnung* offset is **not** — a discretionary rebate rather than a price change.
- **REG-R28** — VVG §§ 165–170: the cross-product statement of [R2] and [R3], and of the *Stornoabzug* conditions.
- **REG-R30** — VVG §§ 19, 37, 38, 157 and 158: the *Anzeigepflicht* at [R5]; §§ 37 and 38 are named as **not researched** and nothing is asserted about them.
- **REG-R31** — VVG §§ 6, 7, 1a, 7b, 7c and 214 with the VVG-InfoV: advice, information and the *Effektivkosten* at [R9].
- **REG-R32** — PRIIPs, Verordnung (EU) Nr. 1286/2014 and its technical standards: the BIB regime at [R19] and [R27].
- **REG-R33** — IDD, Richtlinie (EU) 2016/97 and § 34d GewO: the distribution frame behind the IPID at [S6].
- **REG-R34** — Unisex: EuGH C-236/09 (Test-Achats) and §§ 19, 20 and 33 AGG. **The hard constraint behind `mort_rate_at_age`** — new business unisex from 21 December 2012, so `sex` may not enter the premium (pitfall 17).
- **REG-R35** — BaFin Merkblatt 01/2023 and *angemessener Kundennutzen*: the cross-product statement of [R17].
- **REG-R36** — the BGH line of authority on German life contracts: the cross-product frame for [R22], [R23] and [R24].
- **REG-R38** — AltEinkG and the *Drei-Schichten-Modell*: where a *kapitalbildende Lebensversicherung* sits (Schicht 3), and the 2005 boundary at [R13].
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6: the *Unterschiedsbetrag*, the 12/62 rule and the *Mindesttodesfallschutz* — the cross-product statement of [R10] and [R12], and the reason the anchor cell matures at attained age 62.
- **REG-R46** — ErbStG and SGB V §§ 226, 229 and 240: the treatment of a death benefit, named and not modelled.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables. The frame for the model's two mortality bases, for the *Sicherheitszuschlag* whose release **is** the *Risikoüberschuss*, and for the fact that the direction of prudence forks between the death and the survival leg (pitfalls 13 and 14).
- **REG-R48** — DAV 2008 T and its predecessors: the cross-product statement of [R14], including the selection factors the shipped proxy does **not** carry.
- **REG-R52** — Destatis *Sterbetafeln* and the reuse licence: the population benchmark an insured-lives replacement table must sit below.
- **REG-R53** — the German life market in numbers (GDV, BaFin, Assekurata, Map-Report, Franke und Bornberg): the source of the statement that the *laufende Verzinsung* **is** the guarantee plus the interest surplus, which is pitfall 1 and the single most load-bearing line in the model.
- **REG-R54** — HGB §§ 341–341o, RechVersV and BerVersV: § 341f forming the *Deckungsrückstellung* **excluding verzinslich angesammelte Überschussanteile**, which is why `av_sur_pp` is a cells of its own and not part of `res_pp`; and § 28 RechVersV naming the declared rate as a published quantity.
- **REG-R55** — IFRS 17 and the Variable Fee Approach: named as the other measurement basis these cash flows feed.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional standard this documentation sits under, and the frame for [R15].

---

## Provenance note

Extraction details — which fact was read from which search summary, section-level notes organised
by mechanic, and the **twenty-four-item gaps and caveats register** — live in
`_research/kapitallebensversicherung.md`. That file is the citation ground truth for the S# and R#
numbering used here.

**What this pass changed.** Every entry above now records what was actually opened. Of the
forty-seven product-level entries, **forty-one are `Retrieved: yes`**, four are partly retrieved
(R10, whose *Einkommensteuer-Handbuch* URL answers with a bot interstitial; R11, whose body is
behind a subscription login; R19, one of whose three articles is a 404; and R26, whose
VersicherungsJournal piece is paywalled), and **two are not retrieved at all** — S8 (HTTP 404 at
the cited URL, no replacement found on the publisher's site) and R24 (HTTP 429). The statutory
core is now read as canonical XML with its `Stand` attached, so **gap 15 is closed for §§ 19, 153, 161, 165, 168, 169 and 171 VVG (Stand: zuletzt
geändert durch Art. 12 G v. 26.5.2026 I Nr. 156), § 139 VAG (Art. 25 G v. 25.3.2026 I Nr. 81),
§§ 20 and 52 EStG (Art. 7 G v. 29.6.2026 I Nr. 197), the MindZV (Art. 1 V v. 7.7.2020 I 1688) and
the DeckRV (Art. 1 V v. 19.7.2024 I Nr. 250, in force 1 January 2025)** — those statements are
version-pinned and no longer "current in substance as reported".

The caveats that survive, and which the specification and the technical notes repeat rather than
leave here: **no *Schlussüberschuss* rate of any kind is established**, for any insurer, in any
year — [S18] and [S7] give the *mechanism* and the base, none of the six carrier documents gives a
level — so `term_rate` is wholly [std] (gap 1); **the declared-rate market averages are for the
annuity**, not the endowment, which [R25] states in terms, and the one manufacturer figure, 2,7 %,
is [R26]'s report of a **2025** declaration for a combined classic life-and-annuity book (gap 2);
**one charge figure now exists** — the ÖSA BIB at [S10], with total costs of 6.216 € and a 5,3 %
annual cost impact at twenty years on its own model case, beside BaFin's finding at [R18] of
*Effektivkosten* "über vier Prozent" in individual cases — but no *Abschlusskostenquote*,
*Verwaltungskostenquote* or commission rate is established for any carrier, so every charge in the
model stays [std] (gap 7, materially narrowed); **no German *Produktinformationsblatt* or IPID for
this product was located**, though [S10] supplies the PRIIP-BIB fields it would have carried
(gap 9); **the GDV *Stornoquote* is a single headline count measure — 2,56 % for 2023 — and is
neither endowment-specific nor split by duration**, so it is still not a surrender rate a decrement
can be calibrated to (gap 10, restated: there are not two irreconcilable measures, there is one
unsuitable one); **no premium rate table, underwriting grid or *Risikozuschlag* scale is public for
any German endowment**, so every premium here is computed by the model's own equivalence principle
(gap 16); **the DAV tables are cited and never shipped**, so every decrement in the model is a [std]
proxy (gap 14); **three carrier *Stornoabzug* schedules are now in the corpus, on three different
bases** — a percentage of the *Deckungskapital* [S3], a euro amount plus a percentage of premiums
paid times the years remaining [S9], and a euro amount plus a percentage of the gap between sum
insured and reserve [S18] — so `storno_rate` as a flat percentage of the reserve is one observed
shape of three, and the Debeka schedule remains sub judice after [R22] (gap 18, superseded);
**four statutory provisions the product depends on were never separately researched** — §§ 152, 37,
38 and 150 VVG — and nothing is asserted about any of them; § 168 has since been read and is
recorded at [R2] (gap 20, narrowed); and **the variations table is six carriers wide**, of which
[S7] and [S18] are genuine endowment wordings, [S3]–[S5] and [S9] are annuity wordings used only
where the rule transfers, and [S8] produced no document at all (gap 22). One Austrian wording was
returned by a search and is **excluded**: the VVG, the DeckRV and the MindZV do not apply to it, and
nothing anywhere in delib is cited to it (gap 24).

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-kapitallebensversicherung-r1
[R10]: #delib-kapitallebensversicherung-r10
[R11]: #delib-kapitallebensversicherung-r11
[R12]: #delib-kapitallebensversicherung-r12
[R13]: #delib-kapitallebensversicherung-r13
[R14]: #delib-kapitallebensversicherung-r14
[R15]: #delib-kapitallebensversicherung-r15
[R17]: #delib-kapitallebensversicherung-r17
[R18]: #delib-kapitallebensversicherung-r18
[R19]: #delib-kapitallebensversicherung-r19
[R2]: #delib-kapitallebensversicherung-r2
[R20]: #delib-kapitallebensversicherung-r20
[R21]: #delib-kapitallebensversicherung-r21
[R22]: #delib-kapitallebensversicherung-r22
[R23]: #delib-kapitallebensversicherung-r23
[R24]: #delib-kapitallebensversicherung-r24
[R25]: #delib-kapitallebensversicherung-r25
[R26]: #delib-kapitallebensversicherung-r26
[R27]: #delib-kapitallebensversicherung-r27
[R29]: #delib-kapitallebensversicherung-r29
[R3]: #delib-kapitallebensversicherung-r3
[R4]: #delib-kapitallebensversicherung-r4
[R5]: #delib-kapitallebensversicherung-r5
[R6]: #delib-kapitallebensversicherung-r6
[R7]: #delib-kapitallebensversicherung-r7
[R8]: #delib-kapitallebensversicherung-r8
[R9]: #delib-kapitallebensversicherung-r9
[REG-R15]: #delib-reg-r15
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
