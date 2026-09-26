# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/indexpolice.md` (the citation ground
truth for this product) and are **frozen — never renumber**. **No id is absent from this file, and
the numbering has no gaps**: all sixteen primary sources **S1–S16** and all twenty-two
product-level references **R1–R22** are cited by `product-spec.md`, and thirteen of them again by
`technical-notes.md`. That completeness was not evidential strength when it was written: under the
drafting conditions below **no document here had been opened**, so nothing could be dropped for
saying too little, and every entry was cited for what it *would* settle and for the fact that it did
not. **Most of them have since been opened**, and each entry's `Retrieved` line says which. Where a
sibling library's `sources.md` records omitted ids, this one records absences of a different kind,
in that same place. Sources were assembled on **2026-08-29** and retrieved on **2026-08-30**; each
`Retrieved` line records the edition, page count or statutory `Stand` of what was read. No source id
was added or renumbered at either date. Cross-product [REG-R#] tags are listed in their own section
at the end.

**Retrieval conditions — read before any entry below.** They have two halves, a drafting half and
a verification half, and both belong in the record.

**How this file was drafted.** Two independent limits applied, and both bound this product hardest.
**(1) Direct HTTP egress was blocked** by an organisation default-deny network policy: `WebFetch`
and `curl` were refused with HTTP 403 at the egress gateway for every host outside a short
package-registry allowlist. `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
`bundesfinanzministerium.de`, `dejure.org`, `buzer.de`, `destatis.de`, `eur-lex.europa.eu` and
`de.wikipedia.org` were all tried and all refused, so **not one document cited in this file had been
opened** — no *Bedingungswerk*, no *Produktinformationsblatt*, no *Basisinformationsblatt*, no
statutory text, no BaFin *Merkblatt*, no index rulebook. **(2) The session's `WebSearch` budget —
200 calls, shared across the library — was exhausted before this product was researched**, during
the regulatory and contract-law work and during delib products 1 and 2. Every search attempted here
returned the budget-exhausted message, so the first draft had **no research channel at all**: it
rested on the authoring model's own knowledge of German insurance law and actuarial practice,
disciplined by **[std]** tags on constructed levels and `[unverified]` tags on uncorroborated
claims. That is how this product's documents were written, and it is part of their provenance.

**How it was verified.** That policy has since been lifted and the citations re-verified against the
primary documents. Across delib, all fifteen German instruments the library cites were read as
**canonical XML** from `gesetze-im-internet.de`, each law's amendment `Stand` recorded; **950
statutory section references were checked and 950 were correct**; and insurer AVB,
*Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read.
**Across the library, 501 of 805 source entries — 62 % — now read `Retrieved: yes`**, and the rest
name what stopped them: an HTTP 404 at the cited URL, a consent or JavaScript wall, a paywall, or a
subscription login.

**In this file, 32 of the 38 entries below read `Retrieved: yes`**, one — [R10], the PRIIPs
delegated regulation — reads `partly`, its landing pages read but the Anhang II categorisation only
at second hand, and **five read `no`**. The five are not one failure repeated. [S3] is a document
class that **does not exist** for a *Schicht 3* Indexpolice, and the retrieved VVG-InfoV § 4 Abs. 3
is what says so; [S5] is the annual parameter notice, which insurers send to policyholders and do
not publish; [S13] (*Finanztest*) is behind the publisher's paywall; [S15] (Verivox, Check24) is
bot-blocked; and [R21] (the rating houses) publishes behind its own tools and paid reports. Two of
the five are therefore unpublishable rather than merely unreached, and each of the five is kept at
its frozen number as the record of what could not be had.

What follows from that, stated plainly. **A `Retrieved: yes` line means the document was opened and
the passage the entry rests on was read** — with its edition, page count or statutory `Stand`
recorded beside it, and where the entry quotes, the quotation is exact. **Any other `Retrieved` line
means the entry is still a pointer, not a certificate**: it names the instrument a claim should be
checked against and does not assert that anyone checked it. Every entry says which of the two it is,
so read the line before relying on the claim. **The re-verification changed things.** It closed this
file's central gap — two carrier AVB read in full [S2] [S7], with a third carrier's published
parameters beside them [S8]; it corrected a death-benefit claim that had been attributed to the
wrong carrier series [S9]; and it settled the base of the participation and the mid-year exit
treatment, which stop being standardizations in `model.md`. It did not verify everything. The
cap-level band, the entry-age bands, the minimum premiums and the house indices' volatility targets
and index-level fees remain unestablished; uncertain numbers are still **[std]** parameters rather
than citations, `indexpolice` carrying a higher proportion of them than any other delib product; and
`model.md`'s standardization table lists every one, with what the retrieved evidence does to it.

---

## Primary product sources

(delib-indexpolice-s1)=

### S1 — GDV, *Musterbedingungen* for the *Rentenversicherung mit aufgeschobener Rentenzahlung*
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV); *Musterbedingungen* — model AVB published by the industry association for members to adopt, adapt or ignore. Not binding, not a regulation
- URL: `https://www.gdv.de/resource/blob/6294/61b4fedd6f69db77539816e3421c7eeb/allgemeine-bedingungen-fuer-die-rentenversicherung-mit-aufgeschobener-rentenzahlung-data.pdf`, reached from the *Musterbedingungen* index at `https://www.gdv.de/gdv/service/musterbedingungen`
- Retrieved: **yes** (PDF, 20 pp., Stand 21.07.2025, read 2026-08-30; the *Musterbedingungen* index page read the same day)
- Used for: the clause skeleton every German deferred annuity shares and the Indexpolice inherits unchanged, now read rather than recalled — § 1 *Welche Leistungen erbringen wir?* (the *Erlebensfall* obligation at *Rentenzahlungsbeginn*, the *Kapitalabfindung* option, the *Todesfallleistung* in the *Aufschubzeit*), § 2 *Überschussbeteiligung*, § 5 *Selbsttötung*, § 11 premium default, § 12 *Kündigung* and *Rückkaufswert*, § 13 *Beitragsfreistellung*, § 14 cost offsetting. The non-binding character is stated on the first page: "**Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ. Abweichende Bedingungen können vereinbart werden.**" And — the finding that matters most, now **confirmed by reading the index rather than inferred** — the GDV's life catalogue runs to eleven *Musterbedingungen* (kapitalbildende LV, aufgeschobene / sofort beginnende / fondsgebundene *Rentenversicherung*, the two AltZertG variants, *Basisrente*, *Risiko-* and *Restkredit-LV*, the three *Zusatzversicherungen*) and nine *Muster-Standmitteilungen*, and **not one of them is an index-participation module**. That is why `product-spec.md` labels its *Indexbeteiligung* clause set a **composite** attributed to no carrier — and why the two carrier wordings now retrieved at [S2] and [S7] differ from each other as much as they do

(delib-indexpolice-s2)=

### S2 — Allianz Lebensversicherungs-AG, AVB / *Bedingungswerk* for **Allianz IndexSelect**
- Publisher / doc type: Allianz Lebensversicherungs-AG, Stuttgart; AVB / *Bedingungswerk*, Teil A *Baustein Altersvorsorge — Zukunftsrente IndexSelect (Plus) E25*, document number `E---A0025Z0 (014) 12/2025`
- URL: `https://goa-eportale.allianz.de/dlc_app/Intranet/dlc?nr=E----0025Z0&m=d`, linked as "Versicherungsbedingungen (PDF)" from `https://www.allianz.de/vorsorge/vorsorgekonzept/indexselect/`
- Retrieved: **yes** (PDF, 42 pp., edition `E---A0025Z0 (014) 12/2025`, read 2026-08-30). **This entry closes the central gap.** The product name is **Allianz Zukunftsrente IndexSelect (Plus)** — the marketing name *Vorsorgekonzept IndexSelect* — and is no longer `[unverified]`
- Used for: the *Indexbeteiligung* clause set, read at Teil A Ziffer 3 (*Indexpartizipation und sichere Verzinsung*). Every point `product-spec.md`'s first numbered caveat listed as unsettled is settled here for this carrier. **The payoff**, Ziffer 3.3 Absatz 2 a): "Sie bestimmt sich dadurch, dass die negativen monatlichen Wertentwicklungen und die mit dem jeweiligen →Cap … gedeckelten positiven, monatlichen Wertentwicklungen am Ende eines →Indexjahres aufsummiert werden. … Ergibt sich nach der Aufsummierung eine negative jährliche Summe, setzen wir diese auf null." — that is `x = min(r, C)`, summed and not compounded, floored once at the year, with **no floor on the month**. **The base**, Ziffer 3.3 Absatz 2 e): "Bezugsgröße für die →Indexpartizipation ist der →Policenwert zu Beginn des →Indexjahres", excluding that year's premiums and *Zuzahlungen*. **The *Wahlrecht***, Ziffer 3.1: the insurer notifies the *Caps*, the *Partizipationssatz*, the surplus and the *Bewertungsreserven* *Sockelbetrag* at least **3 weeks** before the *Indexstichtag*; the policyholder's election, in 25-percent steps across indices and the *sichere Verzinsung*, must arrive at latest **7 days** before it. **The *Cap-Festlegung***, Ziffer 3.3 Absatz 2 b): set annually "auf der Grundlage von Angeboten mehrerer Finanzinstitute", depending on the surplus, the *Sockelbetrag* and market factors "wie der Volatilität und der **Dividendenrendite** des jeweiligen Index" — **no *Mindest-Cap* clause exists**. **The exclusion**, Ziffer 3.5: index participation is excluded when the *Policenwert* at the *Indexstichtag* does not exceed the *Deckungsrückstellung* required for the guarantee. **The *Ersatzindex* clause**, Ziffer 3.7 — replacement on material change, with **no *Treuhänder***. See [R4]

(delib-indexpolice-s3)=

### S3 — Allianz Lebensversicherungs-AG, *Produktinformationsblatt* / IPID for **Allianz IndexSelect**
- Publisher / doc type: as originally described — *Produktinformationsblatt*, in the market also labelled with the IDD term **IPID**. **That description is wrong for this product class, and the retrieved regulation says so.** VVG-InfoV § 4 creates an *Informationsblatt zu Versicherungsprodukten* (the IPID of Durchführungsverordnung (EU) 2017/1469), and § 4 Abs. 3 excludes it: "Diese Regelung gilt nicht für **Versicherungsanlageprodukte** im Sinne der Verordnung (EU) Nr. 1286/2014" (canonical XML, Stand: zuletzt geändert durch Art. 13 G v. 26.5.2026). An Indexpolice is a *Versicherungsanlageprodukt*, so **no IPID is issued for it**; the *Basisinformationsblatt* [S4] takes its place, and the VVG-InfoV § 2 catalogue reaches the customer as the contract-specific document Allianz's AVB calls "Versicherungsinformationen" [S2], which is not published. A standardised, published *Produktinformationsblatt* exists only under the AltZertG, for *Schicht 1* and *Schicht 2* — that is [S11], and it was retrieved
- URL: not established, and **no such document exists to establish** — see above
- Retrieved: **no** — the document class does not exist for a *Schicht 3* Indexpolice. The entry is kept at its frozen number as the record of a mis-specified source
- Used for: the **commercial envelope**, which is no longer entirely unestablished. The retrieved [S4] carries Allianz's own model case (37-year-old, 30 annual payments of 1.000 EUR, 30-year *Aufschubdauer*, *Aufschubdauern* of 12/20/30/40 years published) and its *Garantieniveau* menu (90 % for IndexSelect, 80 % for IndexSelect Plus); the retrieved [S11] carries a full envelope for a competitor including a guaranteed *Rentenfaktor*. What is still not established for **Allianz** is the entry-age band, the minimum and maximum *Beitrag* and the guaranteed *Rentenfaktor*, none of which appears in a published document. `product-spec.md` cites this entry at its second numbered caveat for that residue, and for the fact that the anchor cell's 200,00 € a month and its 40 → 67 term remain **[std]** choices

(delib-indexpolice-s4)=

### S4 — Allianz Lebensversicherungs-AG, *Basisinformationsblatt* (PRIIP-KID) for **Allianz IndexSelect**
- Publisher / doc type: Allianz Lebensversicherungs-AG; *Basisinformationsblatt* under Regulation (EU) No 1286/2014 [R10] — risk indicator, four performance scenarios, and the cost table with the *Reduktion der Wertentwicklung*
- URL: `https://goa-eportale.allianz.de/dlc_app/Intranet/dlc?nr=JLRIP9030Z0&m=d` (*Zukunftsrente IndexSelect*, 30 years), with `…JLRIP9020Z0…` (20 years) and `…JLRIU8030Z0…` (*IndexSelect Plus*) beside it, indexed at `https://www.allianz.de/service/dokumente/basisinformation-bib-zukunftsvorsorge/`
- Retrieved: **yes** (PDF, edition *Datum der Erstellung des Basisinformationsblatts: 01.11.2025*, read 2026-08-30; three editions compared)
- Used for: **the numbers this file previously recorded as unreachable**. Product line "Allianz Zukunftsrente IndexSelect (mind. 90 % Garantie)"; **risk indicator 1 of 7** at 30 years, 2 at 20 years, 2 for *IndexSelect Plus* (80 % Garantie). Model case 30 × 1.000 EUR from age 37. **Performance scenarios at 30 years**: stress and pessimistic 27.830 / 31.730 EUR (−0,5 % / +0,4 % p.a.), moderate 42.160 EUR (**+2,1 %**), optimistic 66.880 EUR (+4,8 %); death 42.160 EUR. **Costs**: *Einstiegskosten* "**2,5% der kumulierten Anlagen**" plus 1,5 % of the annual payment from year 6; *Verwaltungsgebühren* 3,5 % of the payment a year plus 1,0 % of the value a year; *Transaktionskosten* 0,1 %; total **1,6 % a year** at 30 years (2,6 % at 15, 32,4 % at 1), turning 3,7 % before costs into 2,1 % after. It also states that surrender pays "den … Rückkaufswert **abzüglich eines Stornoabzugs**". The *Abschlusskosten* charge delib ships as **[std]** at 2,5 % of the *Beitragssumme* is therefore the carrier's own number; `β` and `γ` remain **[std]** but now have a published comparator, and `model.md` records the comparison rather than the absence

(delib-indexpolice-s5)=

### S5 — Allianz Lebensversicherungs-AG, annual notification of the *Indexbeteiligung* parameters for the coming *Indexjahr*
- Publisher / doc type: Allianz Lebensversicherungs-AG; annual policyholder letter or customer-portal notice announcing, before each *Indexjahr* begins, the **Cap** (or the *Partizipationsquote*) that will apply, and inviting the *Wahlrecht* election
- Retrieved: **no instance** — the notice is sent to policyholders and is not published, so none could be reached on 2026-08-30. **But its contents and timing are now settled from the AVB that mandates it** [S2], and cap and quota levels turned out to be reachable by two other routes, so the entry no longer stands for a total absence
- URL: not established (no published instance)
- Used for: the mechanic — **the Cap is fixed by the insurer for one *Indexjahr* at a time, before it begins, and is then binding for its whole length**. [S2] Ziffer 3.1 prescribes the notice, its content (indices, *Caps*, *Partizipationssatz*, the year's surplus net of *Verwaltungskosten*, the *Bewertungsreserven* *Sockelbetrag*) and its deadline (at latest **3 weeks** before the *Indexstichtag*), so the specification's *Indexjahr* row and `technical-notes.md`'s payoff row now rest on a retrieved clause rather than on this unreached document. And for the levels, which are no longer wholly unestablished: Allianz's own worked illustration runs at a **Cap of 3,2 %** with a *Partizipationssatz* of **75,00 %**, expressly "exemplarisch gewählt" (see [S16] for the 3,3 % figure recorded in the 2018 litigation), and Stuttgarter **publishes** its current quota — 70 %, or 120 % / 172 % with the *Index-Turbo* options, for all *Indexstichtage* from 1.2.2026 to 31.1.2027 [S8]. delib's 3,00 % monthly Cap stays **[std]** and is now bracketed by a carrier's own illustration rather than by recollection

(delib-indexpolice-s6)=

### S6 — Allianz Lebensversicherungs-AG, **Allianz Perspektive** documents (the *Neue Klassik* comparator)
- Publisher / doc type: Allianz Lebensversicherungs-AG; *Basisinformationsblatt* for **Allianz Zukunftsrente Perspektive**, a *Neue Klassik* deferred annuity **without** index participation. Its AVB was not separately retrieved
- URL: `https://goa-eportale.allianz.de/JLR/SK1/JLRSK1-30Z0.pdf.download.pdf` (30 years), indexed with the 12/20/40-year editions at `https://www.allianz.de/service/dokumente/basisinformation-bib-zukunftsvorsorge/`
- Retrieved: **yes** (PDF, 3 pp., *Datum der Erstellung des Basisinformationsblatts: 01.11.2025*, read 2026-08-30). The product name **Allianz Zukunftsrente Perspektive** is confirmed and is no longer `[unverified]`
- Used for: the ***Neue Klassik* guarantee architecture** the whole product rests on — a guarantee falling due at *Rentenbeginn* rather than accruing as an annual guaranteed rate on the reserve, which is what permits the riskier asset mix that generates the surplus that becomes the option budget. The retrieved KID states the guarantee in exactly that form — "Sie haben Anspruch darauf, mindestens 90 % Ihres Kapitals zurückzuerhalten … Dieser Schutz vor künftigen Marktentwicklungen gilt jedoch **nicht, wenn Sie vor dem vereinbarten Rentenbeginn einlösen**" — which is `technical-notes.md`'s pitfall 11 stated by the carrier. It also makes the comparator quantitative and **the comparison is closer than the marketing of either product suggests**: on the same model case and the same cost structure (*Einstiegskosten* 2,5 % of cumulative payments), Perspektive's moderate scenario is 40.900 EUR (1,9 % a year) against IndexSelect's 42.160 EUR (2,1 %) [S4], and both sit in risk class 1. The specification's design-type row and its account of why guarantee levels fell below 100 % rest on this entry

(delib-indexpolice-s7)=

### S7 — R+V Lebensversicherung AG, AVB and product documents for **R+V-IndexInvest**
- Publisher / doc type: R+V Lebensversicherung AG, Wiesbaden; *Allgemeine Versicherungsbedingungen für die R+V-IndexInvest-Rentenversicherung* (**IL55**), Stand 01.07.2025, at pages 61–81 of the 603-page *Bedingungsheft* `PLG0426`. The *Basisinformationsblatt* sits behind a tariff selector at `ruv-bib.de` and was not retrieved
- URL: `https://www.ruv.de/dam/jcr:038d2022-558e-46d7-b161-e37647ff9a2d/PLG0426.2026-04-30-12-59-13.pdf`, linked from `https://www.ruv.de/altersvorsorge/private-rentenversicherung/privat-rente-indexinvest`
- Retrieved: **yes** (PDF, tariff IL55 read in full, Stand 01.07.2025, read 2026-08-30). The carrier product name **R+V-PrivatRente IndexInvest** is confirmed and is no longer `[unverified]`
- Used for: **the second carrier wording, and therefore the first evidence in this file that the market varies rather than converges.** R+V's design is not Allianz's. § 3 Ziffer 2: "Die Höhe der Indexpartizipation eines Versicherungsjahres wird bestimmt, indem die Bezugsgröße für die Indexpartizipation mit der **jährlichen Wertentwicklung** des Index und mit der jährlich festgelegten **Beteiligungsquote** multipliziert wird" — a participation quota on the point-to-point year return (§ 3 Ziffer 3: "die prozentuale Veränderung des Index innerhalb eines Versicherungsjahres", *Bewertungsstichtag* the last Frankfurt trading day of the *Versicherungsjahr*), **with no monthly cap anywhere in the tariff**. The underlying is a house index, the *Solactive Multi Anlage Stabil Index* (**SOMAS**), built for R+V by Solactive. The *Wahlrecht* runs to **7 days** before the *Versicherungsjahrestag*, index participation is the default, and the *Turbo* stakes 2 % of the *Policenwert*. It is the retrieved counterpart to delib's `payoff_form = "quote"` exactly as [S2] is to `payoff_form = "cap"`, and it is what lets `product-spec.md`'s variations table be filled in. See [R1], [R2], [R3], [R8] and [R9] for the clauses of this AVB that carry them. **Superseded use**: this entry previously carried the reason no statement of the form "the market does X" appeared anywhere in this product's documents — a second carrier wording being the minimum before such a statement can be made. Two are now in hand, and the specification's first numbered caveat is narrowed accordingly rather than carried jointly with [S2] and [S8]

(delib-indexpolice-s8)=

### S8 — Stuttgarter Lebensversicherung a. G., AVB and product documents for **Stuttgarter index-safe**
- Publisher / doc type: Stuttgarter Lebensversicherung a. G.; two published documents were reached — the *Produkt-Steckbrief* **index-safe** (`12.3.001 – Stand 1/2025`, a *Werbemitteilung* by its own legal notice) and the *Stuttgarter Index* service page carrying the current *Partizipationsquote*. The **AVB is not published**: the *Downloadcenter* directory refuses listing (HTTP 403) and no *Bedingungen* PDF is linked from either the customer or the intermediary site. The carrier's AltZertG *Produktinformationsblatt* is [S11]
- URL: `https://daten.vermittler-stuttgarter.de/Downloadcenter/Stuttgarter/01_Leben/16_Tarifuebergreifend/02_indexsafe/12_3_001_PS_index-safe.pdf` and `https://www.stuttgarter.de/service/index`
- Retrieved: **yes, for those two** (PDF, 1 p., Stand 1/2025; and the service page, Stand 04. August 2026, both read 2026-08-30). **No** for the AVB — see above. The carrier product name **Stuttgarter index-safe** is confirmed and is no longer `[unverified]`
- Used for: **the house-index observation, now named**, and **the only current, carrier-published participation level in this file**. The underlyings are the *Stuttgarter M-A-X Multi-Asset Index* and the *Stuttgarter Grüne Zukunft Index*, both built for the tariff; the *Steckbrief* describes the M-A-X as investing "in mehreren Anlageklassen, um eine kontinuierliche Wertentwicklung zu erzielen". The service page publishes, for **all *Indexstichtage* from 1.2.2026 to 31.1.2027**: *Partizipationsquote* **70 %**, with *Index-Turbo* 120 % and *Index-Turbo Plus* 172 %, and a *sichere Verzinsung* of **2,16 %** — the first published number in this file directly comparable to delib's `surplus_rate` **[std]** of 2,50 %. The design is a quota on the year, like [S7] and unlike [S2]. **No volatility target and no index-level fee is published for the M-A-X**, and none is asserted; that half of the gap stands. The shipped `houseidx_vol5` path with its 6,00 % Cap and 100 % *Partizipationsquote* remains **[std]**, and its quota now sits above a published 70 %

(delib-indexpolice-s9)=

### S9 — Zurich Deutscher Herold Lebensversicherung AG, *Verbraucherinformation* series for konventionelle Rentenversicherungen
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung – Private Vorsorge (Schicht 3) und Rückdeckungsversicherung (Schicht 2)*, in der Fassung 01 / 2026, document `521331262 2601`
- URL: `https://www.zurich.de/-/media-assets/project/zurich-headless/germany/br/documents/verbraucherinformationen/32020_aufgeschobene-rentenversicherung_verbraucherinformationen_2026_01.pdf`
- Retrieved: **yes** (PDF, 66 pp., Fassung 01/2026, read 2026-08-30)
- Used for: **the inherited chassis, and one correction.** The document confirms the *Aufschubzeit* / *Rentenzahlungszeit* structure and the *Überschussbeteiligung* machinery product 2 takes from this series, and it settles the open question: the 2026 edition contains **no index variant** — the string "Index" does not occur in it once. **It contradicts the claim this entry was cited for.** § 1 Abs. 2 reads: "Ist keine der folgenden Erweiterungsmöglichkeiten des Versicherungsgrundschutzes eingeschlossen, so **erlischt im Falle des Todes der versicherten Person die Versicherung, ohne dass eine Leistung fällig wird**." The default deferred-phase death benefit on this chassis is therefore **nothing**, and where cover is agreed the standard form is *Beitragsrückgewähr* — a return of **premiums paid**, not of the accumulated capital (§ 1 Abs. 3). delib's "return of the accumulated capital" is the shape of [S7] § 1 Ziffer 5 (*Policenwert*, at least 90 % of premiums) and of [S4]'s death scenario, not of this series, and `product-spec.md` and `technical-notes.md` are corrected to cite it accordingly. The consequences drawn from it — a small *Risikoüberschuss*, light underwriting, § 161 VVG close to inoperative — survive on the [S7] wording; the citation does not

(delib-indexpolice-s10)=

### S10 — GDV *Muster-Standmitteilung* for a *Rentenversicherung*, and carriers' own *Standmitteilungen*
- Publisher / doc type: GDV *Muster-Standmitteilung* "Rentenversicherung (klassisch 1)", version 22 March 2018 (model); individual carriers' actual statements
- URL: `https://www.gdv.de/resource/blob/6306/999e4633ea996ddc885f1153ca6312fa/6v1-gdv-muster-standmitteilung-private-rentenversicherung-klassik1-02-2017-data.pdf`
- Retrieved: **yes for the GDV model** (PDF, 9 pp., version 22 March 2018, read 2026-08-30); **no for any carrier instance** — a *Standmitteilung* is sent to policyholders and none is published
- Used for: the document class in which an *Indexjahr* result reaches the policyholder. The retrieved model settles what the standardised layout does **not** contain: it reports *Garantiertes Kapital* opening and closing, premiums, *Erträge*, *Abschluss-/Vertriebskosten* and *Verwaltungskosten* for the year, then *Schlussüberschuss*, the *Bewertungsreserven* share and *Gesamtkapital*, and a three-column *Überschussbeteiligung* sensitivity — **and it carries no cap row, no *Indexrendite* row and no locked-in-credit row**. The GDV publishes nine *Muster-Standmitteilungen* and none of them is an index variant [S1], so no standardised reporting format for an *Indexjahr* exists at all. **The absence this entry recorded is now partly filled from elsewhere**: [S2]'s own worked *Indexjahr* table publishes twelve monthly index movements, the capped series and the resulting participation for 2020/2021 and 2021/2022, which is the evidence a *Standmitteilung* would have supplied. The model's constructed *Indexjahre* at `t = 9` and `t = 10` stay **[std]**, but they are no longer the only worked examples in the file

(delib-indexpolice-s11)=

### S11 — AltZertG *Produktinformationsblatt* with the *Chancen-Risiko-Klasse*, for a *Basisrente* or *Riester* index variant
- Publisher / doc type: Stuttgarter Lebensversicherung a. G. as certifying carrier, with the class assignment by the *Produktinformationsstelle Altersvorsorge gGmbH*; *Muster-Produktinformationsblatt* **BasisRente index-safe** (Tarif 69 mit Turbo Plus, 30-year term), Stand 01.01.2026, form `V69-202606`, *Zertifizierungsnummer* 006604 [R12] [REG-R43]
- URL: `https://nextcloud.stuttgarter.de/s/iAR6cfRLwJBSGse/download?path=%2F01_Leben%2F18_Muster_PIB%2F01_BasisRente%2F01_indexsafe&files=Muster_Produktinformationsblatt_Basisrente_index_safe_69_mitTurboPlus_LZ30.pdf`, indexed at `https://www.stuttgarter.de/muster-produktinformationsblaetter`
- Retrieved: **yes** (PDF, 2 pp., Stand 01.01.2026, read 2026-08-30)
- Used for: **the standardised disclosure this entry recorded as unobtained — for an index variant, and it settles both things it was cited for.** The **Chancen-Risiko-Klasse is 4** ("renditeorientierte Anlage mit höheren Ertragschancen"), assigned by the PIA over a 30-year *Ansparphase*. The ***Effektivkosten* are 1,80 Prozentpunkte**, turning an illustrative 5,00 % into an *Effektivrendite* of 3,20 %. The full **commercial envelope** for the *Musterkunde* is published: 100,00 EUR a month for 30 years from age 37 to 67, 36.000 EUR paid in, *Garantiertes Kapital für Verrentung* 30.600,00 EUR (**85 %**), garantierte monatliche Altersleistung 92,57 EUR and a **guaranteed *Rentenfaktor* of 25,74 EUR per 10.000 EUR** — against delib's **[std]** 25,00. The itemised charges are *Abschluss- und Vertriebskosten* **2,50 % der vereinbarten Beiträge** (900,00 EUR), *Verwaltungskosten* 9,00 % of premiums plus 0,04 % of the accumulated capital monthly, and 1,50 % of each payment in the *Auszahlungsphase*. On the base of the participation it says: "Es werden 100 % der laufenden Überschüsse für die Indexbeteiligung verwendet. Sie können jährlich festlegen, ob Sie dies beibehalten wollen …" — the budget, not the base

(delib-indexpolice-s12)=

### S12 — Finanztip, guidance pages on *Indexpolicen*
- Publisher / doc type: Finanztip Verbraucherinformation gGmbH — **secondary**, not a product document; press release "Indexpolicen lohnen sich nicht", Berlin, 21 October 2016. Finanztip's current guidance pages on *Indexpolicen* return HTTP 404, so this is the reachable Finanztip statement, and it is ten years old
- URL: `https://www.finanztip.de/presse/pm-finanztip-indexpolicen/`
- Retrieved: **yes** (HTML, dated 21 October 2016, read 2026-08-30)
- Used for: the standing consumer critique, now quoted rather than characterised — that returns "von mehr als 4 Prozent sind aber nur schwer zu erreichen", with "nach Abzug aller Kosten Werte von 0,5 bis 2,5 Prozent" more likely, and that "Verbraucher können oft nicht wirklich nachvollziehen, was sie da eigentlich kaufen". It also independently confirms **the two payoff designs delib ships**: "Bei manchen Optionen sind die Gewinnmöglichkeiten durch einen sogenannten **Cap** gedeckelt. Bei anderen Optionen wird ein festgelegter Prozentsatz ausgeschüttet – die sogenannte **Quote**." And it supplies a segment-size datum [R19] says does not exist in the GDV statistics: 400.000 Allianz contracts as at October 2016 (over 500.000 by 2019, per Allianz's own release [S16]). `product-spec.md` still reproduces the criticisms as **positions with their strength assessed**, not as findings; the 0,5–2,5 % figure is a 2016 estimate by a consumer body and is not used as a model input

(delib-indexpolice-s13)=

### S13 — Stiftung Warentest / *Finanztest*, comparative tests of *Indexpolicen*
- Publisher / doc type: Stiftung Warentest — **secondary**; comparative product test with scoring and a cost analysis
- URL: not established. `test.de/Indexpolicen-im-Test/` returns HTTP 404 and the *Finanztest* tests of this class are behind the paywall; the only reachable accounts are trade-press reports of them [S16]
- Retrieved: **no** — paywalled at the publisher, and no landing page for the test was located on 2026-08-30. The entry is kept as a known reference
- Used for: the same disclosure as [S12]. A comparative test of this class would supply cap levels, cost quotas and modelled outcomes for a named panel of carriers in a named year — precisely the evidence the specification's cap and charge gaps record as missing, and the one class of document this pass could not reach. **Nothing is cited from it**, including the average-return figures the trade press attributes to it

(delib-indexpolice-s14)=

### S14 — Verbraucherzentrale Bundesverband e. V. and the Länder consumer centres, pages on *Indexpolicen*
- Publisher / doc type: Verbraucherzentrale **Hamburg** — **secondary**; press release of 4 April 2018, "Gericht stoppt Etikettenschwindel bei Allianz Index Select Rente". The vzbv and other Länder centres' pages on *Indexpolicen* were not located
- URL: `https://www.vzhh.de/presse/gericht-stoppt-etikettenschwindel-bei-allianz-index-select-rente`
- Retrieved: **yes** (HTML, dated 4 April 2018, read 2026-08-30)
- Used for: the sector's standing criticisms, now attributable to a named body in its own words, and to **litigation that was actually brought**. The vzhh sued Allianz under the UWG over the IndexSelect web advertising and won at first instance — LG München I, Urteil vom **23. März 2018, Az. 37 O 12326/17**, recorded in the release as *nicht rechtskräftig* — the court holding that "Beteiligung an der Wertentwicklung des EUROSTOXX 50" and "Indexpartizipation" create the impression of an investment tracking the index while "eine Korrelation des Renditeversprechens (…) mit der Wertentwicklung des Aktienindexes nur sehr eingeschränkt besteht". The release states delib's own central characterisation from the other side: the participation runs "nicht über die eingezahlten Beiträge, sondern ausschließlich über die … jährlich zu ermittelnde Überschussbeteiligung". It also states the monthly-measurement point precisely — the annual outcome can fall short of the index "selbst dann …, wenn der Cap in der Jahresbetrachtung gar nicht überschritten wird", which is delib's Example B argued by a consumer body. **The judgment did not stand**: the OLG München dismissed the claim on 4 April 2019 with no *Revision* admitted [S16]. `product-spec.md` records the criticisms as **positions** and the litigation with its outcome, not as a finding against the product

(delib-indexpolice-s15)=

### S15 — Comparison portals: Verivox, Check24
- Publisher / doc type: Verivox GmbH and CHECK24 Vergleichsportal GmbH — **secondary**; product-comparison and explainer pages
- URL: not established. `verivox.de/altersvorsorge/themen/indexpolice/` answers **HTTP 403** to a plain request, and no Check24 page on this product class was located on 2026-08-30
- Retrieved: **no** — bot-blocked at the publisher. The entry is kept as a known reference
- Used for: the usual fallback for the commercial envelope — minimum premium, entry ages, term bands — when carrier disclosures are unreachable. **The fallback was not needed in the end**: [S11] supplies a complete published envelope for one carrier and [S4] the model case and term menu for another, so the specification's envelope gap is now a gap about *Allianz's* entry-age and premium bands rather than about the product class. The thirteen shipped model points remain **[std]** construction, and the anchor cell is not taken from any of these sources

(delib-indexpolice-s16)=

### S16 — German insurance trade press: *procontra*, *Versicherungsbote*, *Versicherungsjournal*, *Cash.Online*, *Versicherungswirtschaft*, *Handelsblatt*
- Publisher / doc type: various — **secondary**; trade and financial press reporting. What was reached on 2026-08-30 is not the trade press but the **carrier's own press release** answering it: Allianz Deutschland AG, "OLG weist Klage zu Allianz IndexSelect ab", 9 May 2019. `versicherungsbote.de` answers **HTTP 403** (bot wall) to every article on this product, and *procontra* and *Cash.Online* carry nothing on index tariffs in the swept set
- URL: `https://www.allianz.de/presse/mitteilungen/olg-weist-klage-zu-allianz-indexselect-ab/`
- Retrieved: **yes for the Allianz release** (HTML, dated 9 May 2019, read 2026-08-30); **no** for *Versicherungsbote*, *procontra*, *Versicherungsjournal*, *Cash.Online*, *Versicherungswirtschaft* and *Handelsblatt*, which stay known references
- Used for: the outcome of the [S14] litigation, from the winning party: "Das Oberlandesgericht (OLG) München hat bereits am **4. April** [2019] eine Klage der Verbraucherzentrale Hamburg gegen die Allianz Deutschland wegen der Internet-Werbung für das Vorsorgekonzept IndexSelect abgewiesen. **Eine Revision wurde nicht zugelassen.**" It also dates the product — "seit über elf Jahren", so a 2007/2008 launch — and puts the in-force count at "über 500.000 Kunden". This is the only route by which a segment-size figure reaches this file at all [R19]. The record of where **cap changes and index switches** are reported stands as a gap: no trade-press account of one was retrieved, and every cap figure in this file comes from a carrier document [S2] [S5] [S8]

---

## Regulatory and actuarial references (product research numbering)

Where a URL appears below it is the address on `gesetze-im-internet.de`, and it is the
**human-facing link, not the evidence**. The per-section pages `…/<law>/__NNN.html` answer HTTP 200
with a frameset of four to seven kilobytes carrying **no statutory text at all**, so a 200 on one of
them is not retrieval and none is recorded as such. The statutory text below was read from the
**canonical XML** each law publishes at `…/<law>/xml.zip`, which carries the law's `Stand`; every
entry records the `Stand` it was read at. Where an entry still says `[unverified]`, it now says why.

(delib-indexpolice-r1)=

### R1 — VVG § 153, *Überschussbeteiligung*
- Publisher / doc type: Bundesministerium der Justiz / juris (Gesetze im Internet); federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` (human-facing link; the section page is a 4,9 kB frameset with no text)
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: **the statutory hinge of this product**, and the most load-bearing citation in its documents. Abs. 1 gives the entitlement to a share of the *Überschuss* and the *Bewertungsreserven* unless excluded in whole by express agreement; Abs. 2 requires a *verursachungsorientiertes Verfahren*, "andere vergleichbare angemessene Verteilungsgrundsätze können vereinbart werden"; Abs. 3 has the *Bewertungsreserven* determined annually, half of the amount assigned at the end of the contract, subject to the supervisory proviso. **One correction the text forces**: Abs. 4 reads "Bei Rentenversicherungen ist die **Beendigung der Ansparphase** der nach Absatz 3 Satz 2 maßgebliche Zeitpunkt" — for this product the half-share falls due at *Rentenbeginn*, not at termination, and the documents now say so. From it `product-spec.md` takes the **legal characterisation** — the index participation is a form of *Überschussverwendung* with **no independent statutory footing** — which the two retrieved AVB state as their own financing rule ([S2] Ziffer 3.3, [S7] § 3 Ziffer 9), each naming the annual *Überschussanteile* **and** the *Bewertungsreserven* share as what buys the option. That the budget may be zero is likewise in both: "Im ungünstigsten Fall kann die Überschussbeteiligung Ihres Vertrags der Höhe nach null sein" [S2] Ziffer 2.1; "Diese können auch Null sein" [S7] § 13 Ziffer 1

(delib-indexpolice-r2)=

### R2 — VVG § 169, *Rückkaufswert*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` (human-facing link; the section page is a 7,0 kB frameset with no text)
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: the surrender machinery and three separate model facts, all now read. Abs. 3: the *Rückkaufswert* is the *Deckungskapital* computed on recognised actuarial principles with the premium-calculation bases, "bei einer Kündigung des Versicherungsverhältnisses jedoch mindestens der Betrag des Deckungskapitals, das sich bei **gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre** ergibt" — which is `min_surr_pp(t)` and the shadow account behind it, and which [S2] Ziffer 9.2 reproduces with the addition "höchstens jedoch auf die Beitragszahlungsdauer". Abs. 4 puts the *Zeitwert* rule on *fondsgebundene* contracts and those with benefits of the § 124 Abs. 2 Satz 2 VAG kind, **not on this one** — so the general-account reading is a consequence of Abs. 3 applying and Abs. 4 not, which is half of the not-unit-linked argument [R15], and [S7] § 11 Ziffer 2 says exactly that ("Der Rückkaufswert ist der zum Kündigungszeitpunkt berechnete Policenwert", "nach § 169 Absatz 3 VVG"). Abs. 5: "Der Versicherer ist zu einem Abzug … nur berechtigt, wenn er **vereinbart, beziffert und angemessen** ist" — which is why `surr_charge_on` is a model-point column, and both retrieved AVB put the amount in a separate contract document rather than in the AVB. **Two readings previously [std] are now settled by clause.** Abs. 7 requires already-allocated *Überschussanteile* to be paid on top, so locked-in credits are inside the surrender value as a matter of statute; and the running *Indexjahr* is **not**, because both AVB credit the participation only "zu Beginn des folgenden Indexjahres" ([S2] Ziffer 3.3, [S7] § 3 Ziffer 5) and neither refunds the unspent option budget — [S2] Ziffer 9.2 Absatz 4 adds only a pro-rata *Schlussüberschussanteil* and *Sockelbetrag*

(delib-indexpolice-r3)=

### R3 — VVG § 165, *Prämienfreie Versicherung*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` (human-facing link; the section page is a 4,5 kB frameset with no text)
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: the *Beitragsfreistellung* right — conversion at any time for the end of the current insurance period, on recognised actuarial principles with the premium-calculation bases and on the *Rückkaufswert* of § 169 Abs. 3 **bis 5**, so under the same *Stornoabzug* discipline (Abs. 2). Two things the text adds that the entry did not have: the right is conditional on reaching "die dafür vereinbarte **Mindestversicherungsleistung**", failing which the insurer pays the *Rückkaufswert* instead (Abs. 1) — [S7] § 11 Ziffer 9 sets that minimum at a *Policenwert* of 2.500 EUR — and the paid-up benefit must be stated in the contract for every *Versicherungsjahr* (Abs. 2). **The index-specific delta is no longer an inference.** Abs. 3 Satz 2: "Die Ansprüche des Versicherungsnehmers aus der **Überschussbeteiligung bleiben unberührt**" — and since the index participation *is* a form of *Überschussverwendung* [R1], a paid-up Indexpolice keeps it on the capital already accumulated and the *Wahlrecht* survives. `technical-notes.md` still records *Beitragsfreistellung* as deliberately **not modeled**: the paid-up account diverges at conversion and tracking it needs a conversion-cohort ledger

(delib-indexpolice-r4)=

### R4 — VVG § 163 (*Prämien- und Leistungsänderung*) and § 164 (*Bedingungsanpassung*)
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` and `.../__164.html` (human-facing links; both section pages are framesets with no text)
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: **the most important legal distinction in this product** — and the retrieved text corrects three things this entry said. **(a) The marginal headings are wrong above**: § 163 is *Prämien- und Leistungsänderung* and § 164 is *Bedingungsanpassung*, and the entry's heading is corrected. **(b) The § 163 trigger is not "the calculation bases have changed"**: Abs. 1 Nr. 1 requires that "sich der **Leistungsbedarf** nicht nur vorübergehend und nicht voraussehbar gegenüber den Rechnungsgrundlagen der vereinbarten Prämie geändert hat", the new premium be appropriate and necessary for *dauernde Erfüllbarkeit*, and an *unabhängiger Treuhänder* confirm both; Abs. 2 gives the **policyholder** the right to take a reduced benefit instead of a higher premium, and the insurer that right only on a paid-up contract; Abs. 4 drops the trustee where supervisory approval is required. **(c) § 164 is not "on the same footing"**: it needs the clause to have been declared ineffective "durch **höchstrichterliche Entscheidung** oder durch **bestandskräftigen Verwaltungsakt**", the replacement to be necessary and to respect the contract's aim, and it involves **no *Treuhänder* at all**. The conclusion stands and is sharpened: the annual *Cap-Festlegung* is neither — it is the exercise of a discretion the contract confers, governed by § 315 BGB [R22]. **The *Treuhänder* claim about the *Ersatzindex* clause is contradicted.** Both retrieved AVB let the insurer replace the index with no trustee at all ([S2] Ziffer 3.7, [S7] § 3 Ziffer 11). Where the *Treuhänder* does appear in a retrieved AVB is on the *Rentenfaktor*: [S2] Ziffer 1 obliges Allianz, where no comparable annuity exists at *Rentenbeginn*, to set the factor on recognised actuarial principles and to bring in "einen unabhängigen Treuhänder, der den Rentenfaktor zu prüfen und dessen Angemessenheit zu bestätigen hat"

(delib-indexpolice-r5)=

### R5 — VVG § 154 (*Modellrechnung*) and VVG-InfoV § 2 (pre-contractual information)
- Publisher / doc type: Gesetze im Internet; federal statute and federal regulation
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__154.html` (frameset, no text); `https://www.gesetze-im-internet.de/vvg-infov/__2.html` (this one **does** carry the full text, 10,2 kB)
- Retrieved: **yes** for both (VVG § 154 from canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156; VVG-InfoV § 2 read from the section page and re-read from canonical XML, Stand: zuletzt geändert durch Art. 13 G v. 26.5.2026 I Nr. 156; both read 2026-08-30)
- Used for: the *Modellrechnung* duty and the pre-contractual catalogue, both now exact. § 154 Abs. 1 attaches the duty to any "bezifferte Angaben zur Höhe von möglichen Leistungen über die vertraglich garantierten Leistungen hinaus", requires the *Ablaufleistung* on the premium-calculation bases "mit **drei verschiedenen Zinssätzen**", and Abs. 2 the warning that it is a model with fictitious assumptions conferring no contractual claim. **The exemption in Satz 2 is itself evidence for [R15]**: the duty does not apply to contracts with benefits of the § 124 Abs. 2 Satz 2 VAG kind, and an Indexpolice is not one, so the duty **does** apply to it. VVG-InfoV § 2 Abs. 3 fixes the three rates as the *Höchstrechnungszinssatz* × 1,67, that rate plus one point and that rate minus one point — **1,67 % / 2,67 % / 0,67 %** at a 1,00 % *Höchstrechnungszins*, which is what `product-spec.md` reports, and the tag comes off. § 2 Abs. 1 Nr. 9 defines the ***Effektivkosten*** as "die Minderung der Wertentwicklung durch Kosten in Prozentpunkten … bis zum Beginn der Auszahlungsphase", and Abs. 6 computes them like the *Gesamtkostenindikator* of Anhang VI of Delegated Regulation (EU) 2017/653 [R10] — with the *Altersvorsorge-* and *Basisrentenverträge* of the AltZertG carved out, which is why [S11]'s 1,80 Prozentpunkte is an AltvPIBV figure and not this one. **How carriers discharge § 154 for this product is still not established**: neither retrieved AVB reproduces a *Modellrechnung*, and the observation that one is intrinsically awkward here — the interest assumption reaching the payoff only through the option budget and then the Cap, non-linearly — stays an argument

(delib-indexpolice-r6)=

### R6 — VVG § 161, *Selbsttötung*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` (human-facing link; the section page is a 4,1 kB frameset with no text)
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30). The text matches this entry exactly: no liability where the insured deliberately took their own life within three years of conclusion (Abs. 1, with the *freie Willensbestimmung* exception), the period extendable by individual agreement (Abs. 2), and the *Rückkaufswert* including *Überschussanteile* under § 169 owed where the exclusion bites (Abs. 3)
- Used for: the three-year suicide exclusion on a death cover, with the *Rückkaufswert* owed where it applies — carried in the specification's termination table and cited in `technical-notes.md` as a clause **deliberately not modeled**, because it is close to inoperative in economic terms here: the *Aufschubphase* death benefit is a return of capital rather than a sum at risk, so suppressing it changes almost nothing. Recorded so the documents can say that rather than leave it out

(delib-indexpolice-r7)=

### R7 — *Deckungsrückstellungsverordnung* (DeckRV): *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher / doc type: Gesetze im Internet; federal regulation
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` (contents page; the text was read from canonical XML)
- Retrieved: **yes** (canonical XML, §§ 2 and 4, Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250, read 2026-08-30)
- Used for: two model parameters and one explanation, two of the three now sourced verbatim. § 2 (marginal heading ***Höchstzinssatz***, not *Höchstrechnungszins*) Abs. 1: "wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf **1 Prozent** festgesetzt" — the anchor cell's `guar_rate = 0,0100`, confirmed. § 2 Abs. 2 is the **statutory reason the cohorts exist**: "Bei Versicherungsverträgen mit Zinsgarantie gilt der von einem Versicherungsunternehmen zum Zeitpunkt des Vertragsabschlusses verwendete Rechnungszins … **für die gesamte Laufzeit des Vertrages**", which is why a book of this product cannot be projected on one rate and why three cohorts ship. § 4 Abs. 1: "Der Zillmersatz darf **25 Promille der Summe aller Prämien** nicht überschreiten" — the ceiling delib's 2,5 % acquisition charge sits at, and the tag comes off; [S4] and [S11] both charge exactly 2,5 % of premiums. **The rate history is now half-confirmed and half not.** The canonical XML carries only the current *Stand*, so the earlier steps cannot be read off the regulation; but the DAV's own November 2025 statement [R18] records that "Von 2022 bis 2024 lag der Höchstrechnungszins … bei **0,25 Prozent**. Im Jahr 2025 wurde er auf **1,0 Prozent** angehoben", which settles the 2022–2024 cohort. The **0,90 % for a 2017–2021 cohort stays `[unverified]`**: no retrieved document states it. The explanation that at 0,25 % the guaranteed component of a conventional annuity's return is negligible, so an Indexpolice converts the discretionary component into a bounded lottery, is an argument and is labelled as one

(delib-indexpolice-r8)=

### R8 — *Mindestzuführungsverordnung* (MindZV)
- Publisher / doc type: Gesetze im Internet; federal regulation
- URL: `https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html` — the full-text page, which returns the whole regulation (52,6 kB) rather than a frameset
- Retrieved: **yes** (full-text page read 2026-08-30, and §§ 3, 4, 6, 7 and 8 re-read from canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 7.7.2020 I 1688)
- Used for: **where the option budget comes from**, now with the sections named. § 6 Abs. 1: the minimum allocation is "**90 Prozent** der nach § 3 Absatz 1 anzurechnenden Kapitalerträge **abzüglich der rechnungsmäßigen Zinsen**"; § 7: **90 Prozent** of the *Risikoergebnis*; § 8: **50 Prozent** of the *übrige Ergebnis*; each floored at zero, and Alt- and Neubestand taken separately. [S7] § 13 Ziffer 2 states the same rule in the AVB: "Von den Nettoerträgen der Kapitalanlagen … (§ 3 der Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung) erhalten alle Versicherungsnehmer insgesamt mindestens den in dieser Verordnung genannten Prozentsatz. In der derzeitigen Fassung der Verordnung sind 90 % vorgeschrieben." From it both product documents take the corollary that **an Indexpolice has exactly the same risk budget as a classic contract of the same vintage and spends it differently**, and the model keeps its stated limitation: it consumes a **declared** rate and does not close the MindZV loop, so changing an expense assumption moves `net_cf` without moving what the policyholder receives

(delib-indexpolice-r9)=

### R9 — VAG § 139 (*Überschussbeteiligung*, *Sicherungsbedarf*), § 124 (*Anlagegrundsatz*) and the *Sicherungsvermögen* provisions
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vag_2016/` (contents page, 88,5 kB; the sections were read from canonical XML)
- Retrieved: **yes** (canonical XML, §§ 124 and 139, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81, read 2026-08-30). The section numbering is confirmed and the tag comes off
- Used for: the supervisory side of the surplus participation and the investment principles. § 139 Abs. 3 restricts the *Bewertungsreserven* share from fixed-income holdings and interest hedges to the excess over the *Sicherungsbedarf*, which Abs. 4 defines by reference to the *Euro-Zinsswapsatz*. § 124 Abs. 1 states the *Grundsatz der unternehmerischen Vorsicht*, and Nr. 5 permits derivatives "sofern diese zur **Verringerung von Risiken oder zur Erleichterung einer effizienten Portfolioverwaltung** beitragen" while excluding pure trading positions and short sales. `product-spec.md`'s proposition that buying index options to back an index-participation obligation is **the paradigm of a derivative hedging a liability the insurer has itself written** is now corroborated by both AVB, which say the insurer prices the parameter off the hedge: the Cap is set "auf der Grundlage von **Angeboten mehrerer Finanzinstitute**" [S2] Ziffer 3.3 Absatz 2 b), the *Beteiligungsquote* "auf der Grundlage von Angeboten mehrerer Banken für geeignete Kapitalmarktinstrumente (z. B. Index Warrants, Optionen, Futures, Fondsanteile)" [S7] § 3 Ziffer 4 — "Je niedriger der Preis der Kapitalmarktinstrumente und je höher die Überschussbeteiligung …, umso höher ist die Beteiligungsquote"

(delib-indexpolice-r10)=

### R10 — PRIIPs: Regulation (EU) No 1286/2014 and Delegated Regulation (EU) 2017/653
- Publisher / doc type: EUR-Lex; EU regulation and delegated regulation
- URL: `https://eur-lex.europa.eu/legal-content/DE/ALL/?uri=CELEX:32017R0653` (Delegated Regulation (EU) 2017/653), with the 2021/2268 amendment at `…?uri=CELEX:32021R2268`
- Retrieved: **partly.** The EUR-Lex landing pages return substantive bodies and were read on 2026-08-30, but the **Anhang II categorisation text was read at second hand**, from the DAV *Ergebnisbericht* [R11] which quotes it, and from [S4] which is a KID drawn up under it. The delegated regulation's annexes were not read directly
- Used for: the *Basisinformationsblatt* duty and its prescribed structure — risk indicator, four performance scenarios, costs over time and their composition, recommended holding period — every element of which is visible in the retrieved [S4]. And the **product categorisation**, which [R11] states in terms: "Gemäß Ziffer 7 Anhang II RTS zur PRIIP-Verordnung sind Versicherungsanlageprodukte, **deren Wertentwicklung teilweise von nicht am Markt beobachteten Faktoren abhängt**, für die Bestimmung ihres Marktrisikomaßes (MRM) … der sogenannten **Kategorie 4** zuzuordnen. Für Produkte dieser Kategorie erfolgt die Ermittlung des MRM gemäß Ziffer 27 Anhang II RTS mit Hilfe eines anerkannten Branchen- oder Regulierungsstandards." That is delib's reading, sourced. The consequence — that Category 4 admits the firm's own model, so two Indexpolicen with similar mechanics can publish very different favourable scenarios — is an argument, and [S4] is now one concrete instance of the output rather than none

(delib-indexpolice-r11)=

### R11 — DAV, *Ergebnisbericht* of the *Ausschuss Lebensversicherung* on the PRIIP Category 4 *Standardverfahren*
- Publisher / doc type: Deutsche Aktuarvereinigung e. V., Ausschuss Lebensversicherung, AG Verbraucherschutz; *Ergebnisbericht* "Ein Standardverfahren für PRIIP der Kategorie 4", Köln, 1. Juli 2025
- URL: `https://aktuar.de/content/PDF/Fachwissen/2025-07-01_DAV_Ergebnisbericht_LV_Standardverfahren_PRIIP_Kategorie_4.pdf`
- Retrieved: **yes** (PDF, 30 pp., verabschiedet 1. Juli 2025, read 2026-08-30)
- Used for: the profession-wide standard procedure for the MRM and the performance scenarios of exactly the discretionary-surplus component that makes an Indexpolice a Category 4 product. The report states its own status — "Dieser Bericht stellt im Sinne des Anhangs II der RTS zu PRIIP einen 'robusten, anerkannten Branchen- oder Regulierungsstandard' dar" — while adding that it "stellt keine berufsständisch legitimierte Position der DAV dar". Its capital-market model is deliberately aligned with the **PIA-Standard** used for the *Chancen-Risiko-Klassifizierung* of certified products, so that Kategorie-4 PRIIPs "(insbesondere Rentenversicherungen der 3. Schicht)" and AltZertG products are assessed comparably — which is the bridge between [S4] and [S11]. **The open point is now settled negatively rather than left open**: the procedure is generic to Kategorie-4 products and the report says **nothing specific about index-participation mechanics**, so how a German Indexpolice's disclosed scenarios treat the cap or the quota is not derivable from it

(delib-indexpolice-r12)=

### R12 — *Altersvorsorgeverträge-Zertifizierungsgesetz* (AltZertG) and the *Produktinformationsstelle Altersvorsorge*
- Publisher / doc type: Gesetze im Internet (statute); Produktinformationsstelle Altersvorsorge gGmbH (the classification body)
- URL: `https://www.gesetze-im-internet.de/altzertg/` (contents page, 8,7 kB; the text was read from canonical XML)
- Retrieved: **yes** (canonical XML, § 1, Stand: zuletzt geändert durch Art. 5 G v. 25.10.2023 I Nr. 294, with three 26.5.2026 amendments noted as not yet consolidated; read 2026-08-30)
- Used for: **the sharpest single fact in this product's documents about guarantee levels** — that the guarantee level of an index product is set by its **wrapper**, not by its index module. § 1 Abs. 1 Nr. 3 is the *Beitragserhaltungszusage*: the provider must undertake "dass zu Beginn der Auszahlungsphase **zumindest die eingezahlten Altersvorsorgebeiträge** für die Auszahlungsphase zur Verfügung stehen und für die Leistungserbringung genutzt werden", with **up to 20 % of the *Gesamtbeiträge* disregarded** where they buy occupational-disability or survivor cover — a carve-out this entry did not have. The statutory phrase is *Altersvorsorgebeiträge*, which EStG § 82 Abs. 1 defines as *Beiträge* and *Tilgungsleistungen*; the entry's earlier "contributions **and allowances**" goes beyond the text and is dropped. § 1 Abs. 1 Nr. 2 also fixes the earliest payout at the **62. Lebensjahr**. **The wrapper effect is now visible in retrieved documents**: a *Schicht 3* Indexpolice runs at 80 % or 90 % [S4], a *Basisrente* index variant at 85 % [S11], and a *Riester* variant cannot go below 100 %. The AltZertG mandates the standardised *Produktinformationsblatt* of [S11] — which was retrieved, and which carries the *Chancen-Risiko-Klasse* 4 for an index variant

(delib-indexpolice-r13)=

### R13 — EStG § 22 Nr. 1 Satz 3, *Ertragsanteilsbesteuerung* of a *Leibrente*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` — this section page returns the full text (47,9 kB), not a frameset
- Retrieved: **yes** (section page and canonical XML, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30). The precise citation is **§ 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb**, with the table in Satz 4
- Used for: the taxation of a privately funded *Schicht 3* annuity on its ***Ertragsanteil*** only, a percentage fixed once and for all by the age reached at *Rentenbeginn*. The statutory table gives **exactly 17 %** at age 67 — 18 % at 65–66, 16 % at 68 — so the tag comes off and the hedge "about" goes with it. `product-spec.md` cites it in the tax section to record that **the index mechanic does not change the annuity's tax treatment**, the credits having been absorbed into the capital before conversion, and that a *Basisrente* or *Riester* wrapper changes it entirely. No tax is computed anywhere in this model

(delib-indexpolice-r14)=

### R14 — EStG § 20 Abs. 1 Nr. 6, the *Kapitalabfindung* and the *Mindesttodesfallschutz*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — this section page returns the full text (32,6 kB), not a frameset. The transitional rules are in `.../estg/__52.html`
- Retrieved: **yes** (section page and canonical XML for §§ 20 and 52, Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197, read 2026-08-30)
- Used for: **three quantitative facts the model actually uses, and the citation for two of them was incomplete.** (a) The half-income treatment: § 20 Abs. 1 Nr. 6 Satz 2 as enacted reads "nach Vollendung des **60.** Lebensjahres … und nach Ablauf von **zwölf Jahren** seit dem Vertragsabschluss". The **62** delib uses is right but comes from elsewhere — **§ 52 Abs. 28 Satz 7**: "§ 20 Absatz 1 Nummer 6 Satz 2 ist für Vertragsabschlüsse **nach dem 31. Dezember 2011** mit der Maßgabe anzuwenden, dass die Versicherungsleistung nach Vollendung des 62. Lebensjahres des Steuerpflichtigen ausgezahlt wird." The tag comes off and the citation is completed. This is why the *Aufschubdauer* band starts at 12. (b) The ***Mindesttodesfallschutz***: § 52 Abs. 28 Satz 8 confirms the commencement — Satz 6 applies to contracts concluded "nach dem 31. März 2009" or first funded after that date, so delib's "from 1 April 2009" is exact. **But the condition is narrower than delib states.** Satz 6 Buchst. a disapplies the half-income rule where, "in einem **Kapitallebensversicherungsvertrag** mit vereinbarter laufender Beitragszahlung in mindestens gleichbleibender Höhe …, die vereinbarte Leistung bei Eintritt des versicherten Risikos weniger als 50 Prozent der Summe der für die gesamte Vertragsdauer zu zahlenden Beiträge beträgt" — it is written for a *Kapitallebensversicherung*, not for the *Rentenversicherung mit Kapitalwahlrecht* that Satz 1 also covers, and delib's `death_min_rate = 0,50` floor under `db_pp(t)` rests on reading it across. The tag stays, with that as the reason. (c) The **duration-12 step in the lapse table** follows from (a). `product-spec.md`'s statement that exercising the annual *Wahlrecht* is not a change of contract and does not restart the twelve-year clock stays `[unverified]`: neither § 20 nor § 52 addresses it, and neither retrieved AVB does

(delib-indexpolice-r15)=

### R15 — RechVersV and the VAG *Sparten*: what "indexgebundene Lebensversicherung" means in regulation
- Publisher / doc type: Gesetze im Internet (VAG, RechVersV); federal statute and regulation
- URL: `https://www.gesetze-im-internet.de/vag_2016/` for VAG § 124; the RechVersV *Formblätter* were not read
- Retrieved: **yes for the statutory hinge** (VAG § 124 from canonical XML, Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81, read 2026-08-30); **no** for the RechVersV *Formblätter* and the Solvency II line-of-business numbering, which stay `[unverified]`
- Used for: **a terminological trap a careless document falls into, and the classification the whole product rests on** — and the statute now carries it rather than an assertion. **VAG § 124 Abs. 2 defines the class by risk-bearing, not by the presence of an index**: "Absatz 1 Nummer 5 bis 8 findet auf Lebensversicherungsverträge, **bei denen das Anlagerisiko vom Versicherungsnehmer getragen wird**, … keine Anwendung", and Satz 2 Nr. 2 covers contracts whose benefits are "**direkt** an einen Aktienindex oder an einen anderen … Referenzwert gebunden", requiring the technical provisions to be represented by the units or assets underlying that reference value. An Indexpolice of this kind is not in that class on either limb: the policyholder bears no investment risk, the benefits are not directly bound to the index, the capital is in the *Sicherungsvermögen* ([S2] KID: "Die Kapitalanlage erfolgt … vollständig durch das Versicherungsunternehmen im Sicherungsvermögen"; [S7] website: "Ihr Policenwert ist Teil des Sicherungsvermögens"), and the downside is limited to forgoing one year's surplus. Two other retrieved provisions cross-check the reading: VVG § 169 Abs. 4 puts the *Zeitwert* rule only on that class [R2], and VVG § 154 Abs. 1 Satz 2 exempts only that class from the *Modellrechnung* [R5]. The Solvency II line-of-business placement in *insurance with profit participation* stays `[unverified]` — no line-of-business table was read. This entry carries the specification's design-type and where-the-capital-sits rows, `technical-notes.md`'s pitfall 1, and the delib convention that these documents use *Indexpolice* / *Indexbeteiligung* for the product and reserve *indexgebunden* for its regulatory sense

(delib-indexpolice-r16)=

### R16 — BaFin, *Merkblatt* 01/2023 (VA) on conduct supervision of capital-forming life insurance products
- Publisher / doc type: Bundesanstalt für Finanzdienstleistungsaufsicht; supervisory *Merkblatt*
- URL: `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html`
- Retrieved: **yes** (HTML, full text of Merkblatt 01/2023 (VA), read 2026-08-30)
- Used for: BaFin's expectations on product governance and *angemessener Kundennutzen*. The *Merkblatt* makes the *Effektivkosten* the measure: producers must examine the interplay of "Kosten" and "Rendite (vor Kosten)", and "Eine geeignete Größe zur Messung der insgesamt anfallenden Kosten eines kapitalbildenden Lebensversicherungsproduktes sind die **Effektivkosten**, die nach der Methodik berechnet werden, welche die LVU für Produkte im Sinne von § 2 Abs. 1 Nr. 9 VVG-InfoV i.V.m. § 2 Abs. 6 [VVG-InfoV]" apply — which ties this entry directly to [R5]. It also requires an annuitisation phase and each significant biometric cover to be assessed for customer benefit in their own right. **The open question is now answered, negatively**: the *Merkblatt* does **not** name index products — the word *Index* does not occur in it — so it bites on an Indexpolice as a *kapitalbildendes Lebensversicherungsprodukt* and not as a class of its own. `product-spec.md`'s observation that this design raises the value-for-money question in its sharpest form (zero credited in a substantial fraction of years against a full acquisition-cost load) remains an argument, and is now testable against the two retrieved cost quotas: 1,6 % a year [S4] and 1,80 Prozentpunkte [S11],
both well below the "über vier Prozent" at which BaFin says an appropriate customer benefit
"erscheint zweifelhaft" [R17]

(delib-indexpolice-r17)=

### R17 — BaFin, *Risiken im Fokus* and the BaFin *Fachartikel* series on costs and PRIIPs
- Publisher / doc type: BaFin, *Risiken im Fokus 2026*, "Kosten von kapitalbildenden Lebensversicherungen"
- URL: `https://www.bafin.de/DE/die-bafin/publikationen-daten/risiken-im-fokus/Fokusrisiken_2026/RIF_Verbraucher_3/RIF_verbraucher_lebensversicherung_node.html`
- Retrieved: **yes** (HTML, *Risiken im Fokus 2026*, read 2026-08-30)
- Used for: the context that the cost of capital-forming life insurance is a **named supervisory focus risk** — and it now carries three findings rather than none. BaFin measures the risk by the *Effektivkosten*; its 2022 survey of 2021 new business found that these "unterscheiden sich erheblich" and that "in Einzelfällen beliefen sich die Effektivkosten auf **über vier Prozent**", above which "erscheint ein angemessener Kundennutzen zweifelhaft". A repeat survey in 2025 of 2024 new business found them falling, "insbesondere bei den im Neugeschäft dominierenden fondsgebundenen Produkten", by more than 0,4 points in the upper quartile at long terms. **High early-duration lapse rates are named as a second indicator** of an inadequate customer benefit, which is the supervisory counterpart of delib's duration-12 lapse step [R14] and of its *Zillmer* strain. Individual providers withdrew products and made retrospective compensation. `product-spec.md` cites it beside [R16] to place the **[std]** charge levels against a supervisory frame; the four-percent figure is a supervisory observation about the whole class, not about index tariffs, and no charge level is taken from it

(delib-indexpolice-r18)=

### R18 — DAV recommendations on the *Höchstrechnungszins*
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; annual professional recommendation to the Bundesministerium der Finanzen, which sets the rate by regulation
- URL: `https://aktuar.de/de/newsroom/detail/dav-empfiehlt-auch-fuer-2027-einen-hoechstrechnungszins-fuer-lebensversicherungs-neuvertraege-in-hoehe-von-10-prozent/`, with the 2026 recommendation at `…/deutsche-aktuarvereinigung-empfiehlt-auch-fuer-2026-einen-hoechstrechnungszins-in-hoehe-von-1-prozent/`
- Retrieved: **yes** (HTML, DAV press release of 26.11.2025 recommending 1,0 % for 2027, and the corresponding 2026 release; read 2026-08-30)
- Used for: the **1,00 %** rate. It is no longer a cross-reference from a sibling file: the DAV recommends 1,0 % for 2026 and again for 2027, and DeckRV § 2 Abs. 1 currently sets it at 1 Prozent [R7]. The release also supplies the rate history this file could not read off the regulation — 0,25 % from 2022 to 2024, raised to 1,0 % in 2025 — and the derivation: five-year smoothed returns on a representative new-money portfolio with a 40 % *Sicherheitsabschlag*, floored at 0,4 percentage points. It fixes the guarantee basis of a contract issued at the access date and hence the split between the guaranteed capital and the option budget; it carries the anchor cell's `guar_rate = 0,0100` in both product documents. Note the release's own caveat, which delib's cohort structure depends on: the recommendation is "eine Empfehlung für eine gesetzliche **Obergrenze**", and each insurer sets the rate it actually offers within it — so a carrier's `guar_rate` may be below the cohort ceiling, and [S7] § 1 Ziffer 3 prices its guaranteed *Rentenfaktor* at a *Rechnungszins* of **0,1 % p. a.**

(delib-indexpolice-r19)=

### R19 — GDV statistics: *Die deutsche Lebensversicherung in Zahlen*, and the new-business and in-force series
- Publisher / doc type: GDV, *Die deutsche Lebensversicherung in Zahlen 2024*; annual industry statistics
- URL: `https://www.gdv.de/resource/blob/180978/b8ae8eb0b1bf4b15e7cc3354bc231af9/die-deutsche-lebensversicherung-in-zahlen-2024-publikation-pdf-data.pdf`
- Retrieved: **yes** (PDF, 40 pp., edition 2024, read 2026-08-30)
- Used for: two negatives both product documents state rather than gloss, **and reading the publication turns both from assumptions into findings**. The in-force split at 31.12.2023 runs *Renten- und Pensionsversicherungen* 61,8 %, *Kapitalversicherungen (klassisch)* 15,7 %, *Invaliditätsversicherungen* 9,2 %, *Risikoversicherungen* 6,5 % — **no index line anywhere**, and the only occurrence of the word "Index" in the whole publication is its own table-of-contents index. Indexpolicen are counted inside conventional annuity business because that is what they are [R15], so **there is no published figure for the size of the German index-participation segment**; the only counts this file has are a carrier's own ([S12], [S16]). On the *Stornoquote* the publication gives one market-wide number by count — **2,56 % in 2023, 2,51 % in 2022** — for all *Hauptversicherungen* together, with **no index-specific rate and no split by duration**, which is why `lapse_table.csv` is **[std]** in level and shaped only by the tax threshold of [R14]

(delib-indexpolice-r20)=

### R20 — Assekurata, *Marktstudie* on *Überschussbeteiligungen und Garantien*
- Publisher / doc type: Assekurata Assekuranz Rating-Agentur GmbH; press summary of the 24th *Marktstudie zu Überschussbeteiligungen und Garantien*, March 2026. The study itself is a paid publication and was not obtained
- URL: `https://www.assekurata-rating.de/2026/03/04/assekurata-marktstudie-zu-ueberschussbeteiligungen-und-garantien-2026/`
- Retrieved: **yes for the press summary** (HTML, dated March 2026, read 2026-08-30); **no** for the study
- Used for: the **declared surplus rate**, which for this product *is* the option budget [R8]. **The summary reports the index segment separately, which this entry did not expect it to**: it covers "die Produktsegmente Klassik, Neue Klassik, **Index-** und Fondspolicen", and for 2026 gives *Indexpolicen* an average declared *laufender Überschusszins* of **3,07 %** ("etwa dem Vorjahresniveau"), against **2,62 %** for classic private annuities (Gesamtverzinsung 3,23 %), **2,65 %** for *Neue Klassik* (3,32 %) and 2,49 % for guaranteed fund policies. **Two consequences for this file.** delib's `surplus_rate = 2,50 %` **[std]** is below every one of those, and below the index-segment average by more than half a point — a calibration finding recorded in `model.md` and not acted on, because the rate is a shipped input [§ model change]. And the corollary drawn at [R8] — that an Indexpolice has the same risk budget as a classic contract of the same vintage — holds for the **statutory minimum** but not for the **declared** rate: "Indexpolicen bieten weiterhin eine deutlich höhere Überschussbeteiligung als klassische Produkte", and both product documents are corrected to say which of the two they mean. **Whether Assekurata publishes cap levels as such is still not established**: the summary reports declared rates, not caps

(delib-indexpolice-r21)=

### R21 — Rating houses on *Indexpolicen*: IVFP, Franke und Bornberg, Morgen & Morgen
- Publisher / doc type: Institut für Vorsorge und Finanzplanung GmbH; Franke und Bornberg GmbH; MORGEN & MORGEN GmbH; product ratings of retirement-savings contracts
- URL: not established. `ivfp.de/rating/indexpolicen/` answers HTTP 200 but is a **press archive**, not a rating with results; `franke-bornberg.de/de/blog/indexpolicen` and the Morgen & Morgen annuity-rating path both return HTTP 404. No rating carrying cap or participation levels for a named panel was located on 2026-08-30
- Retrieved: **no** — the rating houses publish results behind their own tools and paid reports. The entry is kept as a known reference
- Used for: the record of **the one document class that would still close a gap at a stroke** — a rating of index-linked annuities being the only systematic public compilation this author is aware of that puts cap levels and participation rates for a panel of named carriers side by side. **What it was cited for has narrowed sharply.** Three carrier product names are now established from carrier documents [S2] [S7] [S8], and levels are established for two of them — Allianz's illustrative Cap 3,2 % / *Partizipationssatz* 75,00 % [S5] and Stuttgarter's published 70 % quota for 1.2.2026–31.1.2027 [S8]. What is still missing is the **panel**: a single year's cap and quota levels across the market side by side, so that delib's 3,00 % **[std]** could be placed in a distribution rather than beside two points. The 1,5–5,0 % band quoted throughout stays recollection and `[unverified]`

(delib-indexpolice-r22)=

### R22 — BGB § 315, *Bestimmung der Leistung durch eine Partei* (*billiges Ermessen*)
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/bgb/__315.html` (human-facing link; the section page is a 4,0 kB frameset with no text)
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 2 G v. 2.7.2026 I Nr. 198, read 2026-08-30). The three sentences the entry relies on are Abs. 1 ("so ist im Zweifel anzunehmen, dass die Bestimmung nach **billigem Ermessen** zu treffen ist"), Abs. 2 (declaration to the other party) and Abs. 3 ("so ist die getroffene Bestimmung für den anderen Teil nur verbindlich, wenn sie **der Billigkeit entspricht**. Entspricht sie nicht der Billigkeit, so wird die Bestimmung durch Urteil getroffen") — the description above is accurate and the tag comes off
- Used for: **the correct legal frame for the annual *Cap-Festlegung***, the point on which this product's documents most needed to be right. The Cap is a unilateral determination of a term deciding the policyholder's return for the coming year, so it is reviewable under § 315 BGB — **not** under § 163 VVG, which governs changes to the premium or the benefit on changed *Leistungsbedarf* [R4]. Both retrieved AVB confirm the premise that the determination is unilateral and annual, and neither submits it to a trustee or to any external check ([S2] Ziffer 3.3 Absatz 2 b), [S7] § 3 Ziffer 4). **The "no German decision" statement is refined rather than withdrawn.** German litigation over an Indexpolice does exist and was retrieved: LG München I, 23.03.2018, Az. 37 O 12326/17, reversed by OLG München on 04.04.2019 with no *Revision* admitted [S14] [S16]. But that was a **UWG advertising** case about how the participation was described, not a § 315 BGB review of a cap determination, so **no decided German case on the *Cap-Festlegung* itself is known to this author and none was established**

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen; research
provenance in `_research/regulatory-actuarial.md`). **The retrieval status of that library is its own
and is not upgraded here**: where a [REG-R#] entry there still records that no document was fetched,
that record stands until that file is worked over in its turn. Where an instrument appears both
there and in this file's own R# list, **the R# entry above is the one that now carries a retrieved
text and its `Stand`**, and it is the one to read. Entries cited by the `indexpolice`
documents, or by the `provenance` column of a shipped input file — which is why [REG-R47] is
listed although no prose in this product cites it:

- **REG-R1** — Directive 2009/138/EC (Solvency II): the best-estimate-plus-risk-margin frame the projected cash flows feed.
- **REG-R2** — Delegated Regulation (EU) 2015/35: contract boundaries, future discretionary benefits and management actions — none read from a retrieved text, so every such figure would be `[unverified]`.
- **REG-R4** — EIOPA risk-free term structures, the UFR and the *Volatilitätsanpassung*: the curve a valuation layer would discount `liability_cf` on. Nothing here discounts.
- **REG-R7** — VAG §§ 124–125, *Anlagegrundsätze*, *Sicherungsvermögen* and *Anlagestock*: the statutory pair behind the specification's central distinction — this capital is in the *Sicherungsvermögen* and there is no *Anlagestock*.
- **REG-R9** — VAG § 139, *Überschussbeteiligung* and the *Sicherungsbedarf* test on *Bewertungsreserven*: the supervisory side of [R1], and why the *Bewertungsreserven* share is referenced and not modeled.
- **REG-R10** — VAG §§ 140 and 145, the *Rückstellung für Beitragsrückerstattung*: where the declared rate comes out of.
- **REG-R13** — VAG §§ 351–353, the Solvency II transitional measures: context only.
- **REG-R14** — DeckRV and its § 2, the *Höchstrechnungszins*: the reserving rate cap behind `guar_rate`.
- **REG-R15** — the *Höchstrechnungszins* rate history and the 2024 regulation setting 1,00 % from 1 January 2025: the anchor cell's guaranteed rate and the three shipped cohorts.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: the 25 ‰ ceiling the 2,5 % acquisition charge sits at, and half of pitfall 13.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins* and the *Zinszusatzreserve*: referenced as a reserving layer this library does not compute.
- **REG-R18** — MindZV: the statutory minimum allocation that bounds the option budget, cited with [R8] wherever the financing identity is stated.
- **REG-R20** — LVRG 2014: the reform that cut the *Höchstzillmersatz* to 25 ‰ and reshaped the *Bewertungsreserven* rule.
- **REG-R23** — VVG §§ 8 and 152, the *Widerrufsrechte*: the withdrawal window, absorbed into the first-year lapse rate and not modeled separately.
- **REG-R24** — VVG § 153: the cross-product entry behind [R1], carrying the *verursachungsorientiertes Verfahren* and the half-share of *Bewertungsreserven*.
- **REG-R25** — VVG §§ 154–155, *Modellrechnung* and *Standmitteilung*: the statutory basis of the document class [S10] belongs to, and the three prescribed interest rates the specification reports.
- **REG-R26** — VVG §§ 150, 159–162: *Selbsttötung* and the beneficiary machinery, behind [R6].
- **REG-R27** — VVG § 163: the cross-product entry behind [R4] and its *Treuhänder* requirement.
- **REG-R28** — VVG §§ 165–170: the exit machinery — *prämienfreie Versicherung*, *Kündigung*, *Rückkaufswert*, *Stornoabzug* — behind [R2] and [R3], and the other half of pitfall 13.
- **REG-R30** — VVG §§ 19, 37, 38, 157, 158: *Anzeigepflicht*, *Zahlungsverzug* and the age-error rule; context for the termination table.
- **REG-R31** — VVG §§ 6, 7, 1a and the VVG-InfoV: advice, information and the *Effektivkosten* disclosure duty, cited with [R5].
- **REG-R32** — PRIIPs Regulation and the delegated technical standards: the cross-product entry behind [R10] and the Category 4 classification.
- **REG-R34** — Unisex: CJEU C-236/09 (*Test-Achats*) and §§ 19, 20, 33 AGG — why `sex` selects a best-estimate mortality row and never a premium, a charge or a benefit.
- **REG-R35** — BaFin *Merkblatt* 01/2023 (VA), *Wohlverhaltensaufsicht* and *angemessener Kundennutzen*: the cross-product entry behind [R16].
- **REG-R41** — EStG § 22 Nr. 1 Satz 3 Buchst. a: *Besteuerungsanteil* and *Ertragsanteil*, behind [R13].
- **REG-R43** — AltZertG, the BZSt, the AltvPIBV and the Produktinformationsstelle Altersvorsorge: the entry behind [R12] and [S11], and the source of the statutory 100 % *Riester* guarantee.
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6: the *Unterschiedsbetrag*, the 12/62 rule and the *Mindesttodesfallschutz*, behind [R14] and behind `death_min_rate = 0,50`.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the licensing reason no DAV table is redistributed here, and the distinction that says what the shipped **[std]** Gompertz proxy *is* — a single **second-order** best-estimate basis, since this model prices no mortality guarantee of its own and takes the *Rentenfaktor* as an input. It is cited only in the `provenance` column of `mort_table.csv`, on every row, beside [REG-R48] and [REG-R49]; no prose claim in this product rests on it.
- **REG-R48** — DAV 2008 T: the death-benefit mortality basis, **cited by name and never shipped**.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand: the generational annuity tables, **cited by name and never shipped** — and why the *Rentenfaktor* is a **[std]** input rather than a computed quantity.
- **REG-R53** — the German life market in numbers (GDV, BaFin, Assekurata, Map-Report, Morgen & Morgen, Franke und Bornberg): the 2026 declared-rate averages behind `surplus_rate = 2,50 %`, the sector *Verwaltungskostenquote* band, and the *Neue Klassik* context.
- **REG-R54** — HGB §§ 341–341o, RechVersV and BerVersV: the statutory *Deckungsrückstellung*, including **profit shares already allocated** — the phrase that makes every locked-in index credit part of the reserve from the moment it is credited.
- **REG-R55** — IFRS 17 and the Variable Fee Approach: the measurement model this contract is the archetype of; its mechanics were not read and are `[unverified]`.

---

## Provenance note

Extraction details — which fact would be settled by which document, the mechanics sections the
product documents are actually written from, the two constructed *Indexjahre*, the expected-value
arithmetic behind the cap, and the twenty-four-item gaps-and-caveats register — live in
`_research/indexpolice.md`. That file is the citation ground truth for the S# and R# numbering used
here, and it states at its head the blocked-egress conditions this product was researched under.

The caveats that most constrain what these product documents can claim, in order of how much they
constrain the model:

1. **Two carrier *Bedingungswerke* for index tariffs are now in hand** [S2] [S7], and the caveat
   that stood first is closed for the points it listed: the *Indexjahr* definition, the observation
   dates, the payoff wording, the base of the participation, the *Wahlrecht* timing and notice
   period, the *Cap-Festlegung* clause and the *Ersatzindex* clause are all read. Two findings
   replace it. **(a)** There is no *Mindest-Cap* clause in either AVB. **(b)** The two designs are
   not variants of one wording: Allianz caps each month and applies a *Partizipationssatz* to the
   capped sum; R+V applies a *Beteiligungsquote* to the point-to-point year return of a house index
   and has no cap at all; Stuttgarter is a quota design too [S8]. **What remains open is the third
   carrier's AVB** — Stuttgarter does not publish one — and any wording outside these three.
2. **Cap and quota levels are established for two carriers, not for a market.** Allianz's own
   worked illustration runs at a **Cap of 3,2 %** with a *Partizipationssatz* of **75,00 %**,
   expressly exemplary [S5]; Stuttgarter **publishes** a current *Partizipationsquote* of **70 %**
   for 1.2.2026–31.1.2027 [S8]. No panel putting a year's levels side by side across the market was
   found [R21]. The 1,5–5,0 % band remains recollection and `[unverified]`; the shipped 3,00 % is
   **[std]** and now sits beside a carrier's own figure rather than beside nothing.
3. **A documented worked *Indexjahr* was found — two of them, from the insurer** [S2]. Allianz
   publishes twelve monthly EURO STOXX 50 movements, the capped series and the resulting
   participation for 2020/2021 (sum **15,90 %**, credit 11,92 % after the 75 % *Partizipationssatz*)
   and 2021/2022 (sum **−26,96 %**, *maßgebliche Jahresrendite* **0 %**). No *Standmitteilung*
   showing a real contract's *Indexjahr* was obtained [S10], and the two *Indexjahre* the model
   reproduces at `t = 9` and `t = 10` remain **constructed** and **[std]**.
4. **The commercial envelope is established for one carrier and partly for another.** [S11] gives a
   complete published envelope — 100,00 € a month, 30 years, age 37 → 67, 85 % *Garantieniveau*, a
   guaranteed *Rentenfaktor* of **25,74 € per 10.000 €** and *Effektivkosten* of 1,80 points; [S4]
   gives Allianz's model case, its 12/20/30/40-year term menu and an 80 %/90 % *Garantieniveau*
   menu. Entry-age bands and minimum premiums are still unpublished [S3] [S15], and the thirteen
   shipped model points remain construction rather than observation.
5. **Charge levels are established, and delib's acquisition charge is the market's.** Both [S4] and
   [S11] charge **2,50 % of premiums** in *Abschluss- und Vertriebskosten* — delib's **[std]** value
   exactly, and the DeckRV § 4 ceiling [R7]. Total cost is disclosed at 1,6 % a year [S4] and 1,80
   points [S11]. The three index-specific give-ups — the dealing spread inside the Cap, a house
   index's level fee and volatility-target drag, and the forgone dividend yield of a price index —
   remain **structurally invisible in any disclosure**, though [S2] Ziffer 3.3 Absatz 2 b) at least
   names the *Dividendenrendite* as a determinant of the Cap. That invisibility is a finding; their
   magnitude is still a gap.
6. **The base `G` of the participation is settled, and delib's [std] reading is the carriers'.**
   [S2] Ziffer 3.3 Absatz 2 e): "Bezugsgröße für die →Indexpartizipation ist der →Policenwert zu
   Beginn des →Indexjahres", excluding the year's premiums; [S7] § 3 Ziffer 2 to the same effect.
   It is the whole capital at the year start, not a sub-account and not the accumulated
   *Überschussguthaben*. This is no longer the largest unquantified uncertainty in the product.
7. **The mid-year exit treatment is settled, and delib's [std] reading is the carriers'.** Both AVB
   credit the participation only at the start of the following *Indexjahr* ([S2] Ziffer 3.3, [S7]
   § 3 Ziffer 5), and [S2] Ziffer 9.2 adds on surrender only a pro-rata *Schlussüberschussanteil*
   and *Sockelbetrag* — **no pro-rata index credit and no refund of the unspent option budget** [R2].
8. **No decided German case on the *Cap-Festlegung* is known** [R22]. There is German litigation
   over an Indexpolice — LG München I, 23.03.2018, Az. 37 O 12326/17, reversed by OLG München on
   04.04.2019 [S14] [S16] — but it was a UWG advertising case, not a § 315 BGB review. Two house
   multi-asset indices are now named from carrier documents: the *Solactive Multi Anlage Stabil
   Index* (**SOMAS**) [S7] and the *Stuttgarter M-A-X Multi-Asset Index* [S8]. **No volatility
   target or index-level fee is published for either**, so that half of the gap stands.
9. **Most of this file was retrieved, and where it is quoted the quotation is exact.** Fifteen
   statutory sections were read as canonical XML with their `Stand`, and eleven documents as PDF or
   HTML with their edition dates. The VVG, the DeckRV, the MindZV, the VAG, the AltZertG, the EStG
   and the PRIIPs delegated regulation are living texts and the *Höchstrechnungszins* is reset by
   regulation, so every date and rate must still be re-checked against the instrument before it is
   relied on — but the per-entry `Retrieved` line now says which of them this author actually
   opened, and which he did not.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-indexpolice-r1
[R10]: #delib-indexpolice-r10
[R11]: #delib-indexpolice-r11
[R12]: #delib-indexpolice-r12
[R13]: #delib-indexpolice-r13
[R14]: #delib-indexpolice-r14
[R15]: #delib-indexpolice-r15
[R16]: #delib-indexpolice-r16
[R17]: #delib-indexpolice-r17
[R18]: #delib-indexpolice-r18
[R19]: #delib-indexpolice-r19
[R2]: #delib-indexpolice-r2
[R21]: #delib-indexpolice-r21
[R22]: #delib-indexpolice-r22
[R3]: #delib-indexpolice-r3
[R4]: #delib-indexpolice-r4
[R5]: #delib-indexpolice-r5
[R6]: #delib-indexpolice-r6
[R7]: #delib-indexpolice-r7
[R8]: #delib-indexpolice-r8
[R9]: #delib-indexpolice-r9
[REG-R43]: #delib-reg-r43
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[std]: #delib-std
<!-- END generated citation links -->
