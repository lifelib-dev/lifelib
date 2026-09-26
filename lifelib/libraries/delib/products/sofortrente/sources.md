# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/sofortrente.md` (the citation ground
truth for this product) and are **frozen — never renumber**. All fifteen primary sources
**S1–S15** are cited by `product-spec.md` or `technical-notes.md` and appear below. An entry appears
here if **any** document or shipped input file of this product cites it, which is why the R section
also carries **R12**: no specification document cites it, but `model.md` does and so does every row
of `improvement_table.csv`. Eight of the twenty-five product-level references are cited by no
document and no input file and are therefore absent, leaving gaps in the R numbering: **R3**
(VVG § 153, *Überschussbeteiligung*), **R7**
(DeckRV § 2, the *Höchstrechnungszins*), **R15** (MindZV), **R16** (VAG §§ 138–140 and the
*Zinszusatzreserve*), **R17** (VVG-InfoV and the PRIIPs Regulation) and **R24** (the unisex
rule) are each carried by the cross-product reference library under a frozen [REG-R#] id — as
[REG-R24], [REG-R14] / [REG-R15], [REG-R18], [REG-R9] / [REG-R10] / [REG-R17], [REG-R31] /
[REG-R32] and [REG-R34] respectively — and the product documents cite them from there, because
library-wide numbering is what lets a reader compare ten products against one instrument;
**R6** (VVG §§ 150, 159, 160, the *Bezugsberechtigung*) is likewise carried at [REG-R26], and
the beneficiary is in any event a pass-through that no cell in the model reads; and **R9** (GDV
and HDI media items on the 2025 rate increase) supported no claim the two documents make that
[REG-R15] does not carry with a statutory instrument behind it. Sources were assembled on
**2026-08-29** and **retrieved on 2026-08-30**; each entry's `Retrieved` line records what was
actually opened on that date, with the edition, page count or statutory `Stand` of what was
read. No source id was added or renumbered at either date; where retrieval located a further
document from the same publisher — the GDV's immediate-annuity model conditions, Allianz's
*PrivatSofortRente* page, Debeka's *Sofortrente* page — it is recorded inside the existing
entry rather than given a new id. Cross-product [REG-R#] tags are listed in their own section
at the end.

**Retrieval conditions — read before any entry below.** They changed between the two dates
above, and both halves belong in the record.

**(1) How this file was drafted.** On 2026-08-29 a default-deny network policy blocked all
egress: `WebFetch` and `curl` were refused with HTTP 403 at the egress gateway for every host
outside a short package-registry allowlist — `gesetze-im-internet.de`, `bafin.de`, `gdv.de`,
`aktuar.de`, `bundesfinanzministerium.de`, `destatis.de`, `dejure.org`, `eur-lex.europa.eu`,
`de.wikipedia.org` and every insurer host named below were tried across the delib build and all
refused — and the session's `WebSearch` budget, 200 calls shared across the library, was
exhausted *before* work on the *Sofortrente* began, against a brief that anticipated thirty to
eighty searches. **Not one search was run for this product**, which was the worst-served of the
ten. The draft therefore rested on the authoring model's own knowledge of German insurance law
and practice, disciplined by **[std]** and `[unverified]` tags, and on facts carried over with
attribution from a **sibling delib research file** whose searches had run earlier in the session
— principally `_research/klassische_rentenversicherung.md`, which shares this product's
*Rechnungsgrundlagen* and, at two carriers, its tariff. Where an entry below still rests on that
chain it says so and names the sibling file's own source id: traceable provenance, and one step
weaker than a retrieval. **No document number, URL, edition, page count or publication date was
ever guessed**, then or now.

**(2) How it was re-verified.** The policy was lifted, and on **2026-08-30** the citations were
checked against the primary documents. Library-wide, all fifteen German instruments delib cites
were read as canonical XML from `gesetze-im-internet.de` with each law's amendment `Stand`
recorded, 950 statutory section references were checked and 950 were correct, and insurer AVB,
*Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read;
**501 of the library's 805 source entries, 62 %, now read `Retrieved: yes`.** For this product:
**19 of the 32 entries below read `Retrieved: yes` and 12 read `no`**, one ([R20]) being mixed —
61 % of the thirty-one that resolve either way. Every insurer document in the S section was
opened, as was every statutory provision carried under this file's own [R#] ids.

**What that means for a reader of an entry.** **A `Retrieved: yes` line means the document was
opened and the passage the entry rests on was read**, and the line records the edition, page
count or statutory `Stand` of what was read. **A `Retrieved: no` line means the entry is still a
pointer, not a certificate**: it names the instrument a claim should be checked against and does
not assert that anyone checked it, and it says so in those terms. The twelve name what happened,
and not one of them is a dead link — this file's only HTTP 404 sits inside the mixed entry
[R20]. Three are document classes with no public specimen: the *Produktinformationsblatt* [S11]
and the *Basisinformationsblatt* [S12], of which no carrier publishes an instance, and the
*Standmitteilung* [S15], which an insurer sends to a policyholder rather than publishes. Four
are DAV material that is not on the open web at all: the *Höchstrechnungszins* recommendations
[R8], the derivations of DAV 2004 R and of its *Bestand* companion [R10] [R11], and the
conference and seminar expositions of them [R12]. One is sold rather than published, Assekurata's
market study [R22], and two are publisher series that were not located at any address, BaFin's
[R18] and the GDV's statistics [R25]. The last two, [S13] and [R23], are research artefacts — a
carrier census and a comparison-portal cluster — with no single document behind them at all.
Where an entry was not retrieved it reads `URL: not established` or attributes its URL to the
sibling file that recorded it, and every paragraph number, date, amount and percentage that no
document confirms still carries `[unverified]`. **The re-verification changed things**: it
corrected claims the drafted text got wrong, and those corrections are recorded in the entries
themselves and in the provenance note at the end rather than summarised away here. What it did
not change is why `model.md`'s standardization table is longer for this product than for any
other in the library — **the entire commercial character of a *Sofortrente* is a number, the
euros per month per 100 000 € of *Einmalbeitrag*, and one carrier's scale at one vintage [S8] is
the whole of that number the corpus holds**.

---

## Primary product sources

(delib-sofortrente-s1)=

### S1 — GDV, *Musterbedingungen* service index, and the immediate-annuity model conditions
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin; publisher index page listing the association's *Musterbedingungen* — model general policy conditions members may adopt, adapt or ignore. Not binding, not a regulation
- URL: `https://www.gdv.de/gdv/service/musterbedingungen` — recorded by the sibling file `_research/klassische_rentenversicherung.md` [S3 there] from a search result. The immediate-annuity model conditions it links are at `https://www.gdv.de/resource/blob/6296/52389f06e484287cd23f26219e5ed77f/allgemeine-bedingungen-fur-die-rentenversicherung-mit-sofort-beginnender-rentenzahlung-data.pdf`
- Retrieved: yes (index page read 2026-08-30, and the linked *Allgemeine Bedingungen für die Rentenversicherung mit sofort beginnender Rentenzahlung* retrieved as a PDF, 10 pp., **Stand: 21.07.2025**, read 2026-08-30)
- Used for: **the entry's original negative finding is withdrawn — the retrieved index refutes it.** Under *Rentenversicherungen* the index lists, alongside the deferred annuity, the *Basisrente* and the two AltZertG wrappers, an *"Allgemeine Bedingungen für die Rentenversicherung mit sofort beginnender Rentenzahlung"* and a second set for the AltZertG version of it; under the rider heading it lists a *Hinterbliebenenrenten-Zusatzversicherung* **zur Rentenversicherung mit sofort beginnender Rentenzahlung** as well as the deferred one carried at [S9]. **The GDV does publish an association template for exactly this product**, and `product-spec.md`'s statement that it does not is corrected accordingly (research gap 3 closes). The template itself is now the entry's substantive content: it is non-binding on its face — "Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ" — and its § 9 is the cleanest statement in the corpus of this product's defining term: "Sie können Ihren Vertrag nicht kündigen. Die Rückzahlung des Einmalbeitrages können Sie nicht verlangen." Its § 1 Abs. 1 pays "je nach Vereinbarung jährlich, halbjährlich, vierteljährlich oder monatlich an den vereinbarten Fälligkeitstagen" and Abs. 2 carries the *Rentengarantiezeit* with the worked illustration reproduced at [S4]; § 2 Abs. 6 carries the surplus disclaimer and § 2 Abs. 8 the annual statement behind [S15]. Cited with [S9] for the association's treatment of the survivor's annuity as a rider

(delib-sofortrente-s2)=

### S2 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Direktversicherungen nach § 3 Nr. 63 EStG — Sofort beginnende Rentenversicherung", Fassung 01/2025
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation*, the consolidated pre-contractual pack a German life insurer must supply — general information, the AVB, the *Besondere Bedingungen* per option and the tax notes. Document code **521331402 2501**
- URL: `https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/222202101_sofort-beginnende-rentenversicherung_verbraucherinformationen_2022_01.pdf` — returned by a search recorded as S16 in `_research/klassische_rentenversicherung.md`
- Retrieved: yes (PDF, 25 pp., document code 521331402 2501, read 2026-08-30). **Two corrections the retrieval forces.** The title recorded from the search summary was wrong in both halves: the pack is *für Direktversicherungen nach § 3 Nr. 63 EStG*, not *für Konventionelle Versicherungen*, and its own cover reads "in der Fassung 01 / 2025", not 01/2022 — the URL slug's `2022_01` is stale. The document is therefore a **Schicht-2 *Direktversicherung*** wrapper on the immediate annuity, not the Schicht-3 private contract this product specifies; it nevertheless carries, at pages 16–17, "Allgemeine Steuerhinweise für die sofort beginnende Rentenversicherung – Private Vorsorge (Schicht 3)" (Stand 07/2024), which is Schicht-3 material from the carrier's own pen
- Used for: **clause-level content, where before it carried only the product's identity.** Its AVB § 1 Abs. 6 states the *Rechnungsgrundlagen* in terms: "Die Kalkulation der bei Vertragsbeginn im Versicherungsschein genannten Leistungen basiert auf der Sterbetafel DAV 2004R (Aggregattafel); es wird ein Rechnungszins in Höhe von 1,00 % verwendet." — the corpus's first retrieved statement of an annuity tariff basis, naming the DAV table and putting the rate **at** the 2025 *Höchstrechnungszins* rather than below it [REG-R15]. § 6 reads "Zu Lebzeiten der versicherten bzw. mitversicherten Person ist eine Kündigung der Versicherung ausgeschlossen" and "Die Rückzahlung des Einmalbeitrags können Sie nicht verlangen", which is [R1]'s substance in an insurer's own words; § 7 puts the *Abschluss- und Vertriebskosten* "pauschal bei der Tarifkalkulation" rather than in a separate charge; § 8 Abs. 2 carries the proof-of-life routine "auf unsere Kosten"; and § 2 carries the payout-phase surplus machinery used at [S10]. It remains the citation in `product-spec.md`'s first table for "single-premium immediate life annuity on the general account, *konventionell*, profit-participating" and for the single *Einmalbeitrag*

(delib-sofortrente-s3)=

### S3 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung", Fassung 01/2026
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation*, deferred annuity. Document code **521331262 2601**
- URL: `https://www.zurich.de/-/media-assets/project/zurich-headless/germany/br/documents/verbraucherinformationen/32020_aufgeschobene-rentenversicherung_verbraucherinformationen_2026_01.pdf` — recorded by the sibling file [S4 there] from a search result
- Retrieved: yes (PDF, 66 pp., document code 521331262 2601, Fassung 01/2026, read 2026-08-30)
- Used for: **the clause evidence that surplus participation does not stop at *Rentenbeginn***, which is load-bearing for this product, now read rather than reported. Its § 2 states: "An vorhandenen Bewertungsreserven werden Sie während der Rentenzahlungszeit nach den jeweils geltenden versicherungsvertraglichen und aufsichtsrechtlichen Bestimmungen beteiligt. Derzeit sieht § 153 Absatz 3 VVG eine hälftige Beteiligung an den Bewertungsreserven vor" [REG-R24] — the sentence `product-spec.md` and `technical-notes.md` both cite. It is no longer the corpus's *only* such evidence: [S2] carries the same clause for the immediate annuity, [S4] and [S10] carry the payout-phase mechanics at two further carriers. `technical-notes.md` cites it in class (a) for the *Überschussbeteiligung* as a statutory entitlement whose method is not prescribed and again under *Model scope* for the *Bewertungsreserven* share being **explicitly excluded** from the projection. Its § 1 Abs. 6 repeats [S2]'s *Rechnungsgrundlagen* clause verbatim — DAV 2004R (Aggregattafel), *Rechnungszins* 1,00 % — so the carrier prices the deferred and immediate forms on one basis. It also carries the **two-factor rule at *Rentenbeginn***: under *Verzinsliche Ansammlung* the accumulated surplus is converted "unter Zugrundelegung von Rechnungszins und Sterbetafel, die zum Zeitpunkt des Übergangs in die Rentenzahlung für diese dann vorgesehen sind" — the bases in force for the annuity at conversion, not those of the deferred contract. That is the pricing-primitive statement `product-spec.md` had attributed to [S7]; [S5] states it far more explicitly still

(delib-sofortrente-s4)=

### S4 — NÜRNBERGER Lebensversicherung AG, *Allgemeine Bedingungen für die Rentenversicherung mit sofort beginnender Rentenzahlung und Rentengarantiezeit nach Tarif NR3303*, publisher document id `gn331303_p`
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; an insurer's own AVB for exactly the product in scope. Edition **GN331303_202501**, tariff **NR3303**
- URL: `https://www.nuernberger.de/medien/4allportal/gn331303_p.pdf` — the document id was returned by a search and is recorded by the sibling file [S9 there]; the URL was constructed from the carrier's `4allportal` path form and **is confirmed working**
- Retrieved: yes (PDF, 7 pp., edition GN331303_202501, read 2026-08-30). The title recorded from the search summary was truncated: the AVB names the *Rentengarantiezeit* and the tariff code as well
- Used for: **the richest single document in this file, and the one that turns most of the product's mechanics from reported to read.** Five things rest on it. (i) *Rechnungsgrundlagen*: "Um die in den Allgemeinen Vertragsdaten genannte garantierte Rente zu berechnen, verwenden wir die anerkannte Rententafel NÜRNBERGER Tafel 2013 R mit einem garantierten Rechnungszins von 1 % p. a." — **a company table, not DAV 2004 R**, which is why `product-spec.md` no longer asserts DAV 2004 R as *the* German annuity basis but as the profession's reference behind carriers' own first-order tables. (ii) *Rentengarantiezeit*: "Stirbt die versicherte Person während der Rentengarantiezeit, so wird die monatliche Rente bis zum Ablauf der Rentengarantiezeit weiter gezahlt", with the illustration of a ten-year period and death after three, and an option to commute the remaining instalments to "eine einmalige Kapitalleistung" — the certain floor behind `certain_floor` and `check_guarantee_certain`, and the second settlement form the model does not implement. The period runs "ab Versicherungsbeginn". (iii) **Payment timing**: "Die erste Rente wird einen Monat nach dem vereinbarten Versicherungsbeginn gezahlt. Die garantierte monatliche Rente wird an jedem Monatsersten gezahlt" — **monthly in arrears**, which contradicts the model's *vorschüssig* [std] convention; see the note at the end of this file. (iv) *Überschussverwendung*: a *dynamische Überschussrente* whose "jeweils erreichte Rentenhöhe kann nicht mehr sinken" and a *teildynamische Bonusrente* whose additional amount "ändert sich, wenn sich der hierfür maßgebende Überschussanteilsatz ändert", increasing "erstmals zum Ende des ersten Versicherungsjahres" — the anniversary step behind `check_annuity_roll_fwd` and pitfall 14 — and "Ein Wechsel der Überschussverwendungsarten ist ausgeschlossen", the irrevocability `product-spec.md` had tagged [unverified]. (v) **Charge structure**: "Bei Verträgen gegen Einmalbeitrag werden von uns die Abschluss- und Vertriebskosten vollständig zu Vertragsbeginn mit diesem verrechnet. Die übrigen Kosten werden von uns über die gesamte Vertragslaufzeit verteilt" — exactly the α-once-plus-β-running shape the model implements, though **no level is given**. § 13 supplies the no-surrender clause: "Eine sofort beginnende Rentenversicherung können Sie nicht kündigen."

(delib-sofortrente-s5)=

### S5 — NÜRNBERGER Lebensversicherung AG, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung und Rentengarantiezeit nach Tarif NIR3301", document id `gn331451_p`
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; AVB for a deferred annuity **with *Rentengarantiezeit***, tariff **NIR3301**
- URL: `https://www.nuernberger.de/medien/4allportal/gn331451_p.pdf` — recorded by the sibling file [S9 there] from a search result
- Retrieved: yes (PDF, 17 pp., edition GN331451_202501, read 2026-08-30)
- Used for: two things, the second far more important than the entry previously claimed. **(i) The *Rentengarantiezeit* as a tariff-level design feature carried in the product's own name**, not a rider bolted on; `product-spec.md` cites it in the *Rentengarantiezeit* row and `technical-notes.md` in class (a) for `guar_years × payment_freq` instalments being payable **regardless of survival** from *Rentenbeginn* — the fact behind `certain_floor`, `check_guarantee_certain` and pitfalls 2 and 3. Its § 1 pays "die Rente monatlich, jeweils zum Monatsersten". **(ii) The pricing-primitive claim, stated in the strongest terms anywhere in the corpus.** § 1 Abs. 1 fixes the conversion factor at *Rentenbeginn* "nach anerkannten Regeln der Versicherungsmathematik mit unserem dann aktuellen Rechnungszins und unserer dann aktuellen unternehmenseigenen anerkannten Sterbetafel … maßgeblich sind Rechnungszins und Sterbetafel in der Beitragskalkulation vergleichbarer, dann bei uns zum Verkauf geöffneter Rentenversicherungen **mit sofort beginnender Rentenzahlung**", and names the comparable tariff outright: "Beispiel: Zum Zeitpunkt des Abschlusses Ihres Vertrags war in diesem Sinne der Tarif NR3303 vergleichbar" — that is [S4]. A deferred German annuity converts on the bases of the carrier's own *Sofortrente* tariff, by the deferred contract's own terms. This is the clause `product-spec.md` should cite for the *Sofortrente* being the pricing primitive of every deferred German annuity, in place of the paraphrase it had attributed to [S7]

(delib-sofortrente-s6)=

### S6 — Cosmos Lebensversicherungs-AG (CosmosDirekt), "Allgemeine Bedingungen für die Rentenversicherung", tariff LA 904 A (01.17)
- Publisher / doc type: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland; *Allgemeine Bedingungen* (AVB), tariff code **LA 904 A**, edition **01.17** — January 2017, which resolves research gap 6
- URL: `https://www.cosmosdirekt.de/resource/blob/89106/31bbdccea1c7a5a530feb9e2a3be8d1c/allgemeine-bedingungen-rentenversicherung-la-904-a--data.pdf` — recorded by the sibling file [S8 there] from a search result
- Retrieved: yes (PDF, 8 pp., edition LA 904 A (01.17), read 2026-08-30)
- Used for: **two of the three claims this entry carried are withdrawn; the document does not contain them.** The phrases the library had attributed to it came from an English-language search summary, and reading the AVB shows what it actually says. (i) **DAV 2004 R does not appear in this document at all** — the string "DAV" and the year 2004 are absent from all eight pages. The mortality basis of a German annuity tariff is now evidenced instead by [S2] and [S3], which name DAV 2004R (Aggregattafel) in terms, and qualified by [S4], which names a company table. (ii) **"an underlying interest rate (currently 0 percent p.a.)" is not in the document.** The only tariff rate it states is "der tarifliche Garantiesatz von **0,90 Prozent p. a.**", in § 1 Abs. 2 on the *Deckungskapital* accumulated for a *Kapitalabfindung* — and 0,90 % was precisely the *Höchstrechnungszins* in force when this 01/2017 edition was written [REG-R15], so the document shows a carrier pricing **at** the cap, not below it. No retrieved delib document shows below-cap pricing; `check_tariff_int_rate` remains an inequality because § 2 DeckRV sets a **cap** [REG-R14], which is the right reason for it, and not because a carrier was observed under it. (iii) What the document does carry, and carries well: the ***Kapitalrückgewähr*** definition, "wird der gezahlte Einmalbeitrag … abzgl. der bis zum Todeszeitpunkt gezahlten garantierten Renten geleistet", with the entitlement extinguished once cumulative guaranteed instalments reach the *Einmalbeitrag* — [R23]'s mechanic in an insurer's own words, including that it is measured on the **guaranteed** annuity, which `product-spec.md` had adopted as a [std] argument. The ***Rentengarantiezeit*** with a commutation alternative: "Alternativ steht dem Bezugsberechtigten die Möglichkeit offen, das für die Rentengarantiezeit zum Todeszeitpunkt zur Verfügung stehende Deckungskapital in einer Summe ausgezahlt zu erhalten." The **standard surplus disclaimer**, verbatim: "Die Höhe der Überschussbeteiligung hängt von vielen Einflüssen ab. Diese sind nicht vorhersehbar und von uns nur begrenzt beeinflussbar." That the *konstante* form (its *Zusatzrente*) is **reducible** — "Falls wir in einem Jahr nicht ausreichend Überschüsse erwirtschaften, kann die Zusatzrente reduziert werden" — which is [R21]'s central claim at clause level. And the MindZV shares in the carrier's own summary: "mindestens 90 Prozent" of the *Risikoergebnis*, "mindestens 50 Prozent" of the *übrige Ergebnis* [REG-R18]. Finally, **the immediate annuity is inside this AVB's scope**: § 1 Abs. 1 covers "Leibrentenversicherungen mit sofort beginnender Rentenzahlung gegen Einmalbeitrag", for which "wird die erste Rente je nach vereinbarter Rentenzahlungsweise ein Jahr, ein halbes Jahr, ein viertel Jahr oder einen Monat nach dem vereinbarten Versicherungsbeginn gezahlt" — a second carrier paying **in arrears**; see the note at the end of this file

(delib-sofortrente-s7)=

### S7 — Allianz Lebensversicherungs-AG — the immediate-annuity tariff statement, and the Allianz immediate-annuity product documents
- Publisher / doc type: Allianz Lebensversicherungs-AG, Stuttgart; (a) the "Vorsorgekonzept KomfortDynamik" product page, recorded by the sibling file [S13 there] from a search result; (b) the carrier's ***PrivatSofortRente*** product page, located on the publisher's own site from (a) on 2026-08-30; (c) Allianz's own *Sofortrente* contract documents — PIB, AVB, BIB — still **not established**
- URL: (a) `https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/`; (b) `https://www.allianz.de/vorsorge/sofortrente/`; (c) not established
- Retrieved: yes for (a) and (b) (both read 2026-08-30); no for (c) — no document URL was found on the publisher's site
- Used for: **all three claims previously attributed to (a) are withdrawn — none of them is on that page.** KomfortDynamik is a deferred hybrid savings product page whose quantitative content is a choice of *Garantieniveau* at 60 %, 80 % or 90 % of premiums paid; it does not mention the *Rentengarantiezeit*, does not describe monthly payment, and contains no sentence about the calculation bases at *Rentenbeginn*. The paraphrase `product-spec.md` printed in quotation marks as Allianz's — that the bases "relate to the interest rate and mortality table that the company uses at that time for immediately beginning annuities" — appears nowhere in it and has been removed; **[S5] carries that proposition as an actual contract clause** and now bears it. What (b) does establish, and it is the first carrier-level product detail in this file: the product exists under the name ***PrivatSofortRente***; the *Auszahlungsturnus* is "wahlweise monatlich, viertel-, halbjährlich oder jährlich"; the *Mindesteinmalbeitrag* is **3.000 €**; the *Höchsteintrittsalter* is **85 Jahre** for the lifelong form; a *Todesfallleistung ab Rentenbeginn* is available in variants; and buying a *Rentengarantiezeit* or *Hinterbliebenenrente* means accepting "eine geringere monatliche Rente". The page states the annuity is taxed on the *Ertragsanteil* [R13] and prints **no rate**. (c) still supports only the disclosure that no Allianz immediate-annuity tariff code or quotation was established, and the observation cited with [S8] that the classic *deferred* tariff was withdrawn at four large carriers

(delib-sofortrente-s8)=

### S8 — Debeka Lebensversicherungsverein a. G. — AVB series B LV, the "Privatrente" page, and the *Sofortrente* page
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., Koblenz; AVB in the house **B LV** series — the retrieved instance is **B LV 85 (01.07.2026)**, *Allgemeine Bedingungen für eine Rentenversicherung mit aufgeschobener Rentenzahlung und Fondskomponenten nach Tarif CA2I* — plus the insurer's *Privatrente* and *Sofortrente* product pages
- URL: `https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf` and `https://www.debeka.de/privatkunden/vorsorgensparen/zukunftalter/privatrente.html` — both recorded by the sibling file [S11] [S12 there]; and `https://www.debeka.de/privatkunden/vorsorgensparen/zukunftalter/sofortrente.html`, located from the *Privatrente* page on the publisher's own site on 2026-08-30
- Retrieved: yes — all three read 2026-08-30 (B LV 85 as a PDF, 21 pp.)
- Used for: **the single most consequential retrieval in this file, because the *Sofortrente* page carries an annuity rate table and the corpus had none.** Under "Berechnungsbeispiel", *"Exemplarisches Beispiel für eine sofort beginnende Rentenversicherung nach Tarif **S1**, einmaliger Beitrag: **50.000 Euro**"*, with a 20-year *Rentengarantiezeit* and **Stand: 01.01.2025**, the guaranteed monthly annuity by age at *Rentenbeginn* is 60 → 133 €, 61 → 136 €, 62 → 140 €, 63 → 143 €, 64 → 147 €, **65 → 151 €**, 66 → 155 €, 67 → 159 €. The same panel states the payout-phase increase actually granted: "Im Jahr 2024 beträgt die Steigerung der Rente 0,75 Prozent." So a carrier's tariff code (**S1**), a quoted *Rentenhöhe* and a realised *Rentenanpassung* are all now in the corpus, and the blanket disclosures that none of the three was established anywhere are withdrawn (research gaps 4, 5 and 16 narrow to "one carrier, one vintage"). The page also confirms that **Debeka does write a stand-alone *Sofortrente***, the question this entry previously left open; gives the *Rentengarantiezeit* illustration "Bei einer Rentengarantiezeit von 20 Jahren wird die Rente im Fall des Todes nach 12 Jahren noch 8 weitere Jahre an eine begünstigte Person ausgezahlt"; and states the *Ertragsanteil* in the insurer's own words with the corroborated cell — "Das sind zum Beispiel 18 % bei Rentenbeginn mit Vollendung des 65. Lebensjahrs" [R13]. **The *Deckungskapital* definition this entry was cited for is not in B LV 85 in the form the library reproduced**: that AVB is a *fondsgebunden* deferred tariff, and its § 34 forms the *Deckungskapital* out of the *Sparanteil* left after costs and the risk contribution — the same idea, but stated for a premium stream and a *garantiebasierter Baustein*, not as the general definition. `product-spec.md` and `technical-notes.md` keep the netting step `Nettoeinmalbeitrag = Einmalbeitrag × (1 − α)`, now cited to [S4]'s explicit single-premium charge clause instead. With [S7], the entry still carries the withdrawal of classic deferred tariffs

(delib-sofortrente-s9)=

### S9 — GDV, "Allgemeine Bedingungen für die Hinterbliebenenrenten-Zusatzversicherung zur Rentenversicherung"
- Publisher / doc type: GDV; *Musterbedingungen* for the **survivor's-annuity rider**
- URL: `https://www.gdv.de/resource/blob/6336/942f7b9aec6a969b486ec205279870a3/allgemeine-bedingungen-fuer-die-hinterbliebenenrenten-zusatzversicherung-zur-rentenversicherung-mit-aufgeschobener-rentenzahlung-0-pdf-data.pdf` — recorded by the sibling file [S10 there]. The slug names the **deferred** annuity, and a separate set for the immediate one **does** exist: the [S1] index links `https://www.gdv.de/resource/blob/6334/5fd00dfe4be51e918d69159d74a75998/allgemeine-bedingungen-fuer-die-hinterbliebenenrenten-zusatzversicherung-zur-rentenversicherung-mit-sofort-beginnender-rentenzahlung-0-pdf-data.pdf`
- Retrieved: yes (PDF, 6 pp., **Stand: 14.11.2019**, read 2026-08-30)
- Used for: the structural fact the documents need about the *Hinterbliebenenrente* — that **the German market treats it as a *Zusatzversicherung*, a rider with its own condition set, attached to the base contract rather than being a benefit of it** — which the retrieved template confirms from its title down: "Die Hinterbliebenenrenten-Zusatzversicherung ergänzt die als Hauptversicherung abgeschlossene Rentenversicherung." `product-spec.md` cites it in the lives-basis and survivor-annuity rows, and `technical-notes.md` for the direct modelling consequence: a **separate gated leg with its own insured life, off in the base run**. Two mechanics the retrieval adds. The rider pays "solange die mitversicherte Person lebt", at the main annuity's own *Fälligkeitstage*, "erstmals an dem Fälligkeitstag, der auf den Tod der versicherten Person folgt"; and if the *mitversicherte Person* dies first, "erbringen wir keine Leistung aus der Zusatzversicherung, und diese endet" — the lapse-without-refund the specification describes. Its § 1 Abs. 3 settles the **interaction with the *Rentengarantiezeit***, which the model must respect and the specification had not stated: where the annuitant dies inside the guarantee period, "zahlen wir die Hinterbliebenenrente erst nach Ablauf der Rentengarantiezeit" — the two floors run in sequence, not in parallel. The 60 % and 100 % levels attributed to the market remain `[unverified]`: the model conditions state no percentage at all, leaving the level to the individual contract, so the source is now known to be silent on the point rather than merely unread

(delib-sofortrente-s10)=

### S10 — Konzern Versicherungskammer, "Überschussverteilung 2026"
- Publisher / doc type: Konzern Versicherungskammer, the Bavarian public-sector insurance group; the annual ***Überschussverteilung*** document — how a German life insurer publishes its declared *Überschussanteilsätze* for a year, by tariff generation and by phase
- URL: `https://www.konzern-versicherungskammer.de/dam/jcr:acf4c857-3b53-4521-a108-d1fb9b1cec67/BL_Ueberschussbeteiligung_2026.pdf` — recorded by the sibling file [S15 there] from a search result
- Retrieved: yes (PDF, 145 pp., *Überschussverteilung 2026*, read 2026-08-30; the sections used are Bayern-Versicherung Lebensversicherung AG's)
- Used for: **the disclosure this entry carried is withdrawn — the document does contain rates, a component split and two rules specific to this product.** For *Einzel-Rentenversicherungen* (§ 3.1.1), the *Zinsüberschussanteil* **während des Rentenbezugs** is, for tariff generations 2015 through 2025, **"3,35 % (2,5 %) abzüglich Rechnungszins"**, the bracketed figure being the 2025 declaration and the unbracketed one 2026; the corresponding accumulation-phase rate is "3 % (2,25 %) abzüglich Rechnungszins". Against a 1,00 % tariff rate that is a **2,35 % interest surplus for 2026**. The component split is stated outright: in the payout phase the surplus is "Zinsüberschussanteil in Prozent des Deckungskapitals" and "**Ein Risiko- oder Verwaltungskostenüberschussanteil wird nicht gewährt**" — at this carrier the payout-phase annuity increase is funded from interest surplus alone. Timing and use: "Der laufende Überschussanteil wird am Ende des Versicherungsjahres zugeteilt", with the forms "während des Rentenbezugs: Bonusrente oder Überschussrente" — the anniversary step [S15] and the two payout forms. Two rules bear on the *Sofortrente* specifically: "Rentenversicherungen mit sofort beginnender Rentenzahlung erhalten **keine Schlussüberschussbeteiligung**" and "Rentenversicherungen mit sofort beginnender Rentenzahlung erhalten **keine Mindestbeteiligung**" at the *Bewertungsreserven*. The *Bewertungsreserven* themselves are allotted "zur Hälfte dem Vertrag" [REG-R24] and measured, in payment, "jeweils für den Monat vor dem Jahrestag der Versicherung". `product-spec.md` and `technical-notes.md` keep every figure in `surplus_scale_table.csv` as **[std]** — the shipped scale is not this carrier's and was not calibrated to it — but they no longer say that no rate was established anywhere, and the class (b) label is now supported by a declaration rather than only by argument

(delib-sofortrente-s11)=

### S11 — *Produktinformationsblatt* (PIB) for a sofort beginnende Rentenversicherung — document class
- Publisher / doc type: each insurer individually; the short pre-contractual product summary required by German insurance-distribution law [REG-R31] [REG-R33]. For an annuity it states the *Einmalbeitrag*, the *garantierte Rente*, the *Gesamtrente* including declared surplus, the *Rentengarantiezeit*, the death benefit and the costs
- URL: not established, for any carrier
- Retrieved: no — **no instance was located on any carrier's site on 2026-08-30.** The two carrier product pages retrieved for this product ([S7] Allianz, [S8] Debeka) link a *Beratung* funnel and, at Debeka, the AVB, but neither publishes a specimen PIB
- Used for: **known reference only**, and cited in `product-spec.md` for the disclosure that the class which would settle almost every remaining quantitative gap at a stroke — because a PIB for a *Sofortrente* prints the guaranteed **and** total annuity for a stated *Einmalbeitrag* and age, and the *Effektivkosten* with them — is the class of which not one instance was located. [S8]'s *Berechnungsbeispiel* now supplies the guaranteed half of that for one carrier at one vintage; **no total annuity including declared surplus, and no charge parameter, was established at any carrier** (research gap 8)

(delib-sofortrente-s12)=

### S12 — *Basisinformationsblatt* (PRIIP-KID) for a sofort beginnende Rentenversicherung — document class
- Publisher / doc type: each insurer individually; the three-page key information document required by the PRIIPs Regulation [REG-R32], with its *Risikoindikator*, four performance scenarios and *Renditeminderung* cost figures
- URL: not established, for any carrier
- Retrieved: no — **no instance was located on any carrier's site on 2026-08-30**, and none of the five insurer packs retrieved for this product ([S2] [S3] [S4] [S5] [S6]) contains or reproduces a *Basisinformationsblatt*
- Used for: **known reference only, with the scope question still open.** `product-spec.md` cites it for two things: that if a BIB exists it is the **only** public document giving a cost figure in the standardised *Renditeminderung* form, and that **whether a payout-only *Sofortrente* is within PRIIPs scope at all was not established** — its payout-only character and the absence of a surrender value after *Rentenbeginn* [R1] make the holding-period and "what you might get back" sections awkward. Retrieval does not settle it: [S4]'s cost clause points the reader to "dem Kostenausweis nach § 2 VVG-InfoV" [REG-R31] and says nothing about PRIIPs (research gap 8)

(delib-sofortrente-s13)=

### S13 — Carriers writing the product, recorded without documents
- Publisher / doc type: none — carrier names only: Allianz [S7]; R+V; Debeka [S8]; Generali and CosmosDirekt [S6]; Dialog; HDI; Alte Leipziger; LV 1871; Continentale and Europa; NÜRNBERGER [S4] [S5]; Swiss Life; Zurich Deutscher Herold [S2] [S3]; ERGO; AXA; Barmenia; Hannoversche; Württembergische; Gothaer; Stuttgarter [S14]; Volkswohl Bund; Baloise; Universa; DEVK; Signal Iduna; Provinzial; HUK-Coburg; Konzern Versicherungskammer [S10]; Mecklenburgische [S14]
- URL: not established as a list; three of the named carriers now have retrieved documents or product pages of their own — Allianz [S7], Debeka [S8], NÜRNBERGER [S4] [S5] — and two more have retrieved AVB, Zurich Deutscher Herold [S2] [S3] and CosmosDirekt [S6]
- Retrieved: no — the list itself is a research artefact with no document behind it, and no carrier census was retrieved
- Used for: the *Sofortrente*'s character as a **commodity product** ranked by comparison portals on the single dimension of *Rentenhöhe*, and for the disclosure carried in `product-spec.md`'s variation section that the observed-variation table is **structural**, not a rate comparison. That disclosure is narrowed rather than withdrawn: **two** carrier product names are now established — Allianz's *PrivatSofortRente* [S7] and Debeka's *Sofortrente* on tariff **S1** [S8] — with one quoted rate scale and one *Mindesteinmalbeitrag* between them, and five carriers have a retrieved AVB. What remains unestablished, and is what a variation table would need, is any **comparison**: no two carriers' quotations on the same case, no spread, no charge at any of them (research gap 2). Naming any of the other twenty-three carriers here asserts that it is a German life insurer of the right kind and nothing more

(delib-sofortrente-s14)=

### S14 — Stuttgarter Lebensversicherung a. G. and Mecklenburgische Lebensversicherungs-AG — further pre-contractual packs
- Publisher / doc type: Stuttgarter Lebensversicherung a. G., "Allgemeine Informationen zu einem Altersversorgungssystem"; Mecklenburgische Lebensversicherungs-AG, "Vertragsinformationen für die **Private Rentenversicherung mit flexiblem Fondsanteil (Hybrid)**", Version 07.2025, product *B Privat-Rente Flex* — the truncated title is now complete
- URL: `https://www.stuttgarter.de/documents/209195/221255/Allgemeine_Infos_Altersversorgungssystem_SLV.pdf/2657ea66-2bfa-9cec-04d2-8f72ac9731bd?t=1604038997833` and `https://www.mecklenburgische.de/pdfs/produkte/vertragsinformationen/Vertragsinformationen-zu-Leben/rente-flex_vertragsinformationen.pdf` — both recorded from search results in `_research/klassische_rentenversicherung.md`, as S18 and S14 respectively
- Retrieved: yes — both read 2026-08-30 (PDFs of 23 and 27 pp.)
- Used for: **both claims this entry carried need correcting.** The naming fact is only half right. The Mecklenburgische document is indeed the VVG-InfoV pre-contractual pack under another name and says so, listing itself among "den weiteren Informationen, die nach VVG-Informationspflichten-verordnung zur Verfügung zu [stellen sind]" [REG-R31]. The Stuttgarter document is **not** the same class: it is a *betriebliche Altersversorgung* scheme document — "Die betriebliche Altersversorgung beruht auf einer arbeitsrechtlichen Zusage zwischen Arbeitgeber und Arbeitnehmer" — and never invokes the VVG-InfoV. So *Verbraucherinformation* and *Vertragsinformationen* are two names for the pre-contractual pack; *Allgemeine Informationen zu einem Altersversorgungssystem* is a bAV document, and a later build should not search for it as a synonym. The *Aufschubzeit* claim goes entirely: "Rente flex" is a **hybrid unit-linked deferred annuity**, not a short-deferment immediate one, so it is not a candidate for that variant and the corpus has none — research gap 17 closes as a negative, no carrier's short-deferment *Sofortrente* terms having been located

(delib-sofortrente-s15)=

### S15 — The annual *Standmitteilung* and *Rentenanpassungsmitteilung* in the *Rentenbezug* — document class
- Publisher / doc type: each insurer; the GDV publishes a *Muster-Standmitteilung*. For a contract in the *Rentenbezug* the statement reports the *garantierte Rente*, the current *Überschussrente*, the resulting *Gesamtrente*, and the increase taking effect at the anniversary under a rising *Überschussverwendung* [REG-R25]
- URL: not established for the payout form; **no specimen *Standmitteilung* or *Rentenanpassungsmitteilung* was located at any carrier on 2026-08-30**
- Retrieved: no for the statement itself — the document class is one an insurer sends to a policyholder rather than publishes. The **rules** behind it, however, are now retrieved from the AVB and the declaration that generate it, so the entry's substance no longer rests on the unretrieved specimen
- Used for: the **increase date**, which is now established four times over rather than assumed. [S4] increases the annuity "erstmals zum Ende des ersten Versicherungsjahres"; [S2] "frühestens im zweiten Versicherungsjahr"; [S10] allots the running surplus "am Ende des Versicherungsjahres" and measures the *Bewertungsreserven* in payment "jeweils für den Monat vor dem Jahrestag der Versicherung"; and [S6] credits at "jedem Versicherungsjahrestag". `product-spec.md` and `technical-notes.md` cite this for the *Überschussrente* stepping at the **policy anniversary** rather than on a calendar date — the fact behind `check_annuity_roll_fwd` and pitfall 14 — and for the running expense the annual statement and proof-of-life routine represent, the latter now clause-level at [S2] § 8 Abs. 2 and [S4] § 7 Abs. 1, both "auf unsere Kosten". Two disclosures change. Model point 10's `annuity_pp_init` stays **[std]** because no *Standmitteilung* was located, but the corpus is **no longer without evidence of what a *Rentenanpassung* has done**: [S8] reports "Im Jahr 2024 beträgt die Steigerung der Rente 0,75 Prozent" for its own *Sofortrente*, and [S10] declares the 2026 payout-phase *Zinsüberschussanteil* that drives one (research gap 16 narrows to one carrier, one year)

---

## Regulatory and actuarial references (product research numbering)

(delib-sofortrente-r1)=

### R1 — VVG § 168, *Kündigung des Versicherungsnehmers* — the rule that ends surrender at *Rentenbeginn*
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__168.html` — the canonical human-facing link; the page itself is a 5 kB frameset carrying no statutory text, so it is kept as a pointer and is not what was read
- Retrieved: yes (canonical XML from `gesetze-im-internet.de/vvg_2008/xml.zip`, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: **the provision on which this product's "no surrender, no lapse, no paid-up" specification rests — and reading it shows the library had the mechanism wrong.** § 168 Abs. 3 does **not** confine termination in a *Rentenversicherung ohne Kapitalwahlrecht* to the period before payments start. It disapplies Abs. 1 and 2 only for a pension contract in two cases: a *Basisrentenvertrag* certified under § 5a AltZertG where the parties excluded realisation of the claim, and where realisation was irrevocably excluded to obtain the *Pfändungsschutz* of § 851c or § 851d ZPO. Neither reaches a Schicht-3 *Sofortrente*, so **the discrepancy `product-spec.md` recorded between this entry and [REG-R28] resolves in [REG-R28]'s favour** and gap 9 closes. The correct route to the same conclusion is Abs. 1 and Abs. 2 themselves: Abs. 1 gives a termination right only where "laufende Prämien zu zahlen" sind, and a *Sofortrente* has none; Abs. 2 extends it to a single-premium contract only "bei einer Versicherung, die Versicherungsschutz für ein Risiko bietet, bei dem der Eintritt der Verpflichtung des Versicherers **gewiss** ist" — and on a pure *Leibrente* the insurer's obligation is not certain, the annuitant may die at once. So **no statutory termination right arises at all**, which is exactly what the AVB implement: "Eine sofort beginnende Rentenversicherung können Sie nicht kündigen" [S4], "Zu Lebzeiten der versicherten bzw. mitversicherten Person ist eine Kündigung der Versicherung ausgeschlossen" [S2], and the GDV template's "Sie können Ihren Vertrag nicht kündigen" [S1]. The entry keeps its role in `product-spec.md` for the absence of a capital option, of a *Rückkaufswert* and of any lapse, and in `technical-notes.md` for the empty behavioural class — the conclusion was right throughout; only the citation was wrong. The one qualification stands: a surrender right **may** exist inside an *Aufschubzeit*, on terms no carrier's document established, which is why the base run switches the deferment off

(delib-sofortrente-r2)=

### R2 — VVG § 169, *Rückkaufswert*
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` — the canonical human-facing link; the page is a frameset shell and is kept as a pointer only
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: **its boundary, which is the point — and the boundary runs where the section itself draws it, not where [R1] was said to draw it.** § 169 Abs. 1 imposes the duty to pay a *Rückkaufswert* only where the contract "Versicherungsschutz für ein Risiko bietet, bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist" — the same gateway as § 168 Abs. 2. A pure life annuity is not such a contract, so **§ 169 never engages**; it is inapplicable by its own terms rather than "displaced by § 168 Abs. 3", which is how `product-spec.md` had it. The two rules the entry flagged `[unverified]` are confirmed and can now be stated exactly: Abs. 3 sets the surrender value as the *Deckungskapital* computed on the premium bases, "bei einer Kündigung des Versicherungsverhältnisses jedoch mindestens der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt" — the five-year spreading floor; and Abs. 5 permits a deduction "nur … wenn er vereinbart, beziffert und angemessen ist", with any deduction for unamortised acquisition costs void. Consequently `Sofort_DE_S` publishes **no surrender-value cells, no *Stornoabzug* and no five-year cost-spreading rule** — a specification rather than an omission, stated in that form in both documents and asserted by the test module's absent-names check

(delib-sofortrente-r4)=

### R4 — VVG § 163, *Anpassung der Prämie oder der Vertragsbestimmungen*
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision, with commentary
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` — the canonical human-facing link; the page is a frameset shell and is kept as a pointer only
- Retrieved: yes (canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, read 2026-08-30)
- Used for: the **immutability of the *garantierte Rente***, cited with [REG-R27], whose three cumulative conditions can now be stated from the section rather than from commentary: a change in the *Leistungsbedarf* that is "nicht nur vorübergehend und nicht voraussehbar", a re-set premium "angemessen und erforderlich …, um die dauernde Erfüllbarkeit der Versicherungsleistung zu gewährleisten", and confirmation by "ein unabhängiger Treuhänder" — with adjustment excluded "insoweit, als die Versicherungsleistungen zum Zeitpunkt der Erst- oder Neukalkulation unzureichend kalkuliert waren". Reading it sharpens the point for this product: Abs. 1 authorises a re-set of the **premium**, of which a *Sofortrente* has none after inception, and only Abs. 2 Satz 2 reaches the benefit — "Bei einer prämienfreien Versicherung ist der Versicherer unter den Voraussetzungen des Absatzes 1 zur Herabsetzung der Versicherungsleistung berechtigt" — so the channel is narrower here than the general commentary suggests. **The Landgericht Köln decision remains unestablished**: no case reference, date or parties, and the statute is silent on the point; the claim that a low-interest phase is entrepreneurial risk that cannot be passed on is kept as commentary and tagged accordingly. The model treats `annuity_guar_pp(t)` as level for life and records § 163 as a model risk

(delib-sofortrente-r5)=

### R5 — VVG § 165, *Prämienfreie Versicherung*, and § 166, *Kündigung des Versicherers*
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provisions
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` — the canonical human-facing link; the page is a frameset shell and is kept as a pointer only
- Retrieved: yes — both sections read as canonical XML, Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, 2026-08-30
- Used for: **a boundary again, and the reading holds.** § 165 Abs. 1: "Der Versicherungsnehmer kann jederzeit für den Schluss der laufenden Versicherungsperiode die Umwandlung der Versicherung in eine prämienfreie Versicherung verlangen, sofern die dafür vereinbarte Mindestversicherungsleistung erreicht wird." A *Sofortrente* is bought with a single *Einmalbeitrag* and is premium-free from the moment it is paid, so **there is no future premium to cease and the conversion has nothing to operate on.** § 166 Abs. 1 converts on the insurer's termination and refers back to § 165, so it is inert here for the same reason. Note that neither section says "laufende Prämien" in terms — the restriction is functional, not textual, and the entry states it that way now. Both documents cite this for the absence of a `Beitragsfreistellung` decrement being a specification rather than a simplification

(delib-sofortrente-r8)=

### R8 — DAV recommendations on the *Höchstrechnungszins* for 2025 and 2026
- Publisher / doc type: Deutsche Aktuarvereinigung e. V. (DAV), Cologne; press items, recorded by title as R8 and R9 in the sibling file `_research/klassische_rentenversicherung.md`
- URL: not established — no DAV press item was located on `aktuar.de` or elsewhere on 2026-08-30, and the two titles remain the sibling file's search record
- Retrieved: no — the DAV documents themselves were not found. **The proposition they were cited for is now independently retrieved**, which is the material change: three insurer AVB of 2025 and 2026 vintage state a *Rechnungszins* of **1,00 %** — [S2] and [S3] as "ein Rechnungszins in Höhe von 1,00 %", [S4] as "einem garantierten Rechnungszins von 1 % p. a." — and [R21] records "Seit 2025 liegt er wieder bei einem Prozent"
- Used for: the single point that a contract written in 2026 sits on the **same interest basis** as one written in 2025, which matters here because tariff vintage and contract vintage are the same date. The attribution shifts from the DAV recommendation, which was not read, to the tariffs that implement it. Cited in `product-spec.md` beside [REG-R15] and [REG-R56]; the closing row of `hoechstrechnungszins_table.csv` carries it in its `provenance` tag

(delib-sofortrente-r10)=

### R10 — DAV, "Herleitung der DAV-Sterbetafel 2004 R für Rentenversicherungen"
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; *DAV-Richtlinie*, the profession's derivation guideline for the annuity table. In use since June 2004, for new business from 2005, the DAV document dated 22 February 2005, the derivation guideline reissued 28 June 2023
- URL: not established — no DAV derivation document was located on 2026-08-30; the document and its 2023 reissue remain the sibling file's search record
- Retrieved: no — the *Herleitung* is a DAV members' document, not published on the open web, so this is a permanent rather than a temporary condition. **DAV 2004 R is DAV property, is not public and is not redistributed by delib.** What retrieval adds is external corroboration that the table is in live use and how: [S2] and [S3] name "die Sterbetafel DAV 2004R (**Aggregattafel**)" as the basis of a 2025/2026 annuity tariff — the first time the corpus can attach a named variant to it — while [S4] shows a carrier pricing the same product on its own "NÜRNBERGER Tafel 2013 R" instead. **DAV 2004 R is therefore the profession's reference table, not a universal tariff basis**, and `product-spec.md` no longer asserts it as the mortality basis of *every* German annuity
- Used for: **the mortality basis of this product, structurally.** Four claims rest on it and each shapes the model. That DAV 2004 R is a ***Generationentafel***, mortality given per birth cohort with the expected improvement **inside** the table — which is why `birth_year` is a model point attribute, why `mort_rate_gen` takes a cohort, and why a period proxy is pitfall 8. That its component structure carries a **mortality trend in both a first- and a second-order version** — which is why the shipped proxy's first-order margin reaches the trend as well as the level and why collapsing them is pitfall 9. That first-order probabilities carry safety margins relative to the second-order realistic ones, and that for an annuity prudent means **lighter** mortality. And that the table carries an *Altersverschiebung* whose **convention was not established**, which `technical-notes.md` records as a condition on any replacement table (research gap 12)

(delib-sofortrente-r11)=

### R11 — DAV 2004 R-Bestand and the *Rentenbestandstafel* RBx
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; the companion table for the existing annuity book, paired with the new-business table in a 2004 presentation titled "DAV 2004 R und RBx"
- URL: not established — no DAV presentation or table was located on 2026-08-30; the pairing remains the sibling file's search record
- Retrieved: no — like [R10] a DAV members' document, not published; and none of the five insurer AVB retrieved for this product mentions a *Bestand* table, so the retrieved corpus is silent on it as well as unable to reach it
- Used for: **the pairing and nothing else.** `product-spec.md` cites it for the fact that a *Sofortrente* is priced on the new-business table at inception and then spends thirty years in the *Bestand* to which the other table applies, and — explicitly — for the disclosure that **the difference in level, in trend, in age range and in application rule between the two was not established**, so nothing about it is asserted downstream (research gap 12). `mort_table.csv`'s `provenance` names both tables as cited-not-shipped

(delib-sofortrente-r12)=

### R12 — Contemporaneous expositions of DAV 2004 R (DGVFM, General Re, *qx-Club*)
- Publisher / doc type: Deutsche Gesellschaft für Versicherungs- und Finanzmathematik (DGVFM); General Reinsurance AG; the *qx-Club* actuarial seminar series — the profession's own explanation of the table to practitioners, where the *Sicherheitszuschlag* structure and the trend construction were set out
- URL: not established. `_research/sofortrente.md` records, from the sibling file `_research/klassische_rentenversicherung.md` (R14 there), presentations of **16 August 2004** and **14 September 2004** and a reinsurer's exposition of **27 October 2004**; all three dates are `[unverified]`
- Retrieved: no — no DGVFM, General Re or *qx-Club* item was located on 2026-08-30; these are conference and seminar materials with no stable public address, and **no content was established beyond the existence of the presentations and their dates**, which remain `[unverified]`
- Used for: **nothing affirmative, and that is the whole of its role here.** It is the entry the documents point at where they say what could *not* be established, and it is cited only outside the two specification documents: `model.md` names it beside [R10] at the two places where the shipped *Trendfunktion* is declared **[std]** — in the input-file table and in the standardization table — and `improvement_table.csv` carries it in the `provenance` tag of every row, to record that **DAV 2004 R's own trend is not public** and that these are the documents a later build should fetch to substantiate the first-order margin. No number in this library rests on it

(delib-sofortrente-r13)=

### R13 — EStG § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb — the *Ertragsanteil* table
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` — this one **does** return the full section text, not a frameset, and is both the human-facing link and a usable source
- Retrieved: yes (canonical XML from `gesetze-im-internet.de/estg/xml.zip`, and the HTML page as a cross-check, read 2026-08-30)
- Used for: the product's tax logic, which is its main commercial argument, **and the whole schedule is now read rather than inferred.** The statutory address is confirmed exactly as the library gives it: § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb, whose Satz 4 reads "Der Ertrag des Rentenrechts (Ertragsanteil) ist aus der nachstehenden Tabelle zu entnehmen", the table being indexed by "Bei Beginn der Rente vollendetes Lebensjahr des Rentenberechtigten". Satz 3 fixes it "für die gesamte Dauer des Rentenbezugs", which is the "never changed" the documents rely on. The two cells the specification prints check against it: **60 bis 61 → 22 %** and **65 bis 66 → 18 %**; neither carries `[unverified]` any longer, and nor does the schedule as a whole, which runs 59 % at ages 0–1 down to 1 % from 97. Satz 5 refers annuities depending on another person's life, or limited in time, to a *Rechtsverordnung* — § 55 EStDV — which is where a *Hinterbliebenenrente* and a *Rentengarantiezeit* continuation would be measured, and is the part of gap 15 that stays open. Taxation falls on the annuitant and **is not a cash flow in this model** [REG-R41]

(delib-sofortrente-r14)=

### R14 — EStG § 20 Abs. 1 Nr. 6 — the *Kapitalabfindung* regime, and its boundary
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — returns the full section text; both the human-facing link and a usable source
- Retrieved: yes (canonical XML, plus § 52 for the *Anwendungsvorschrift*, read 2026-08-30)
- Used for: **a sharp boundary, now read — with one precision the library owed the reader.** § 20 Abs. 1 Nr. 6 Satz 1 reaches the *Unterschiedsbetrag* "bei Rentenversicherungen mit Kapitalwahlrecht, soweit nicht die lebenslange Rentenzahlung gewählt und erbracht wird, und bei Kapitalversicherungen mit Sparanteil", and Satz 4 extends it to "Erträge bei Rückkauf des Vertrages bei Rentenversicherungen ohne Kapitalwahlrecht". A *Sofortrente* has no *Kapitalwahlrecht*, pays a lifelong annuity and cannot be surrendered [R1], so **none of the three gateways opens** and the whole cash flow is taxed under § 22 [R13] [REG-R45] — the arbitrage against a *Bankauszahlplan* the product is sold on. The precision: the half-taxation rule in Satz 2 is written as **12 years and the 60th birthday**, not 62. The 62 the library prints comes from § 52, which applies Satz 2 "für Vertragsabschlüsse nach dem 31. Dezember 2011 mit der Maßgabe …, dass die Versicherungsleistung nach Vollendung des 62. Lebensjahres des Steuerpflichtigen ausgezahlt wird". So "12/62" is right for a contract written today and wrong as a citation to § 20 alone; both documents now cite the pair

(delib-sofortrente-r18)=

### R18 — BaFin material on life-insurance product oversight
- Publisher / doc type: Bundesanstalt für Finanzdienstleistungsaufsicht (BaFin); *Merkblatt* 01/2023 (VA) on conduct supervision, the *Risiken im Fokus* cost section and the *Fachartikel* series, all recorded as R17–R19 in the sibling file `_research/kapitallebensversicherung.md`
- URL: not established — no BaFin item was located on 2026-08-30; the titles remain the sibling file's search record
- Retrieved: no — the *Merkblatt*, the *Risiken im Fokus* cost section and the *Fachartikel* series were not reached at any address
- Used for: one disclosure only, and it is unchanged by this pass. All of the supervisor's *Wohlverhaltensaufsicht* material in the corpus is addressed to *kapitalbildende* products, i.e. the accumulation side, and **whether BaFin has published anything on payout annuities, or scrutinises *Rentenhöhe* or surplus declarations for value, remains unestablished** — which is what `product-spec.md` cites at the point where it would otherwise have reported a value-for-money expectation for this product [REG-R35]

(delib-sofortrente-r19)=

### R19 — GDV / dieversicherer.de, "Private Rentenversicherung: Auszahlmöglichkeiten"
- Publisher / doc type: GDV under its consumer brand *Die Versicherer*; consumer article
- URL: `https://www.dieversicherer.de/versicherer/altersvorsorge/news/auszahlung-private-rentenversicherung-141750`
- Retrieved: yes (article read 2026-08-30)
- Used for: the industry association's own account of a private annuity's payout options — **and the retrieved taxonomy is three forms, not the four the library printed.** The article's headings are "Die dynamische Rente", "Die flexible Rente" and "Die teildynamische Rente"; *Bonusrente* does not appear, being a carrier's name for the crediting mechanic rather than an association category ([S2] offers *Bonusrente*, *Bonus-PLUS-Rente* and *Garantie-PLUS-Rente*; [S4] offers a *dynamische Überschussrente* and a *teildynamische Bonusrente*; [S10] offers "Bonusrente oder Überschussrente"). The mechanics are stated precisely: the dynamic form's additional annuity "erhöht dauerhaft die ursprüngliche Garantierente und kann nicht sinken"; the flexible form spreads projected surplus evenly so that it "bleibt über die gesamte Rentenzahlungsdauer konstant, so lange die Überschüsse so hoch sind, wie bei Rentenbeginn prognostiziert"; and the teildynamic form is the mixture, of which "Entwickeln sich die Überschüsse deutlich schlechter als erwartet, können teildynamische Überschussrenten auch sinken". One sentence of the article **conflicts with the contracts** and is not adopted: "Auch bei der flexiblen und der teildynamischen Rente gilt, dass ihre Höhe nie unter das zu Rentenbeginn erreichte Niveau fallen kann" — [S6] and [S2] both permit the surplus component to be reduced, and the AVB control. **No rate and no envelope was established from it**

(delib-sofortrente-r20)=

### R20 — Franke und Bornberg, "Altersvorsorge: Überschüsse im Rentenbezug — Teil 1: Die Qual der Wahl", and "Was bedeutet der Rentenfaktor und wie hoch ist er?"
- Publisher / doc type: Franke und Bornberg GmbH, Hannover — independent product-rating house; two blog articles, the second dated by its slug to 2021/2022
- URL: `https://www.franke-bornberg.de/blog/altersvorsorge-ueberschuesse-im-rentenbezug-teil-1-die-qual-der-wahl` and `https://www.franke-bornberg.de/de/blog/was-bedeutet-rentenfaktor-wie-hoch-2021-2022` — recorded as R19 in the sibling file `_research/klassische_rentenversicherung.md` from search results
- Retrieved: **mixed.** "Die Qual der Wahl" — **no**: HTTP 404 at the cited URL on 2026-08-30, and it is not on the publisher's current blog index under that or an adjacent slug, so the entry keeps it as a known reference and nothing is claimed from it beyond its title. "Was bedeutet der Rentenfaktor und wie hoch ist er?" — **yes** (article read 2026-08-30)
- Used for: **the disclosure this entry carried is withdrawn — the *Rentenfaktor* article does return levels.** It defines the quantity, "wird pro 10.000 Euro angegeben … Bei einem Rentenfaktor von 30 erhält man zum vereinbarten Termin aus 100.000 Euro eine lebenslange monatliche Rente von 300 Euro", and then reports the rating house's own analysis: the average *aktueller Rentenfaktor* across carriers fell from **29,09 €** in 2021 to **25,97 €** in 2022, "ein Rückgang von 3,12 Euro oder 10,73 Prozent", with Condor highest at **26,61 €** (from 29,83 €). Two cautions travel with the figures and both matter here: they are **deferred-tariff conversion factors**, not *Sofortrente* quotations, though [S5] makes those the same bases; and they are struck in the **0,25 % *Höchstrechnungszins*** era, so they are a floor for a contract written at 1,00 % rather than a comparator [REG-R15]. They are not used to calibrate anything — the model's annuity table stays **[std]** — but the library no longer says no *Rentenfaktor* level exists in the corpus (research gap 5 narrows). The article also supports the § 163 model risk: "Auch ein garantierter Rentenfaktor ist nicht immer in Stein gemeißelt" [R4]. The professional treatment of the choice between *Überschussverwendung* forms rests on the 404'd article and is therefore carried by its title alone; it also stands behind `surplus_scale_table.csv`'s `provenance` tags

(delib-sofortrente-r21)=

### R21 — Consumer-organisation material on the *Sofortrente*
- Publisher / doc type: Finanztip Verbraucherinformation gemeinnützige GmbH; Stiftung Warentest (*Finanztest*); the *Verbraucherzentralen*
- URL: `https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/` and `https://www.finanztip.de/lebensversicherung-versteuern/`. **The *Sofortrente*-specific pages of all three publishers were still not located on 2026-08-30 and no URL for them is given**
- Retrieved: yes for the two Finanztip pages (read 2026-08-30); no for Stiftung Warentest and the *Verbraucherzentralen*, whose *Sofortrente* material was not found
- Used for: **the single most important qualitative claim in this product's documents, and the retrieval confirms it in terms.** On the constant form: "In der Praxis kann Deine Rente aber durchaus schwanken. Denn wenn der Anbieter weniger verdient als erwartet, sinkt Deine Rente. Die Summe, die anfänglich festgelegt wird, ist nicht garantiert. Daher ist der Begriff „konstante Rente" etwas irreführend." The `[unverified]` tag on the *Überschussrente* being declared, non-guaranteed and **reducible** therefore comes off; [S6] and [S2] carry the same at clause level. The taxonomy here is the same three forms as [R19] — konstant, teildynamisch, (voll)dynamisch. **The 15–25 % share of the payment at risk is not in either page and stays `[unverified]`**: no source in the corpus quantifies the gap between guaranteed and total annuity, which is what makes `surplus_init_pct` a **[std]**. Two figures the pages do supply, both cross-product rather than product-specific: the *Höchstrechnungszins* history — four per cent at the end of the 1990s, 0,25 % at the trough, "Seit 2025 liegt er wieder bei einem Prozent" [REG-R15] — and a *laufende Verzinsung* for 2026 at five of the ten largest carriers, Allianz 2,7 %, Alte Leipziger 2,4 %, AXA 3,0 %, Proxalto 2,7 %, Nürnberger 2,95 %, sourced to Assekurata [R22], with the note that R+V, Generali, Debeka, Zurich and Bayern-Versicherung "geben die laufende Überschussbeteiligung nicht öffentlich bekannt". `product-spec.md` still records that **Stiftung Warentest's periodic *Sofortrente* comparison is the single most valuable unlocated document for this product**, its existence still `[unverified]`

(delib-sofortrente-r22)=

### R22 — Assekurata, "Marktstudie Überschussbeteiligungen und Garantien"
- Publisher / doc type: Assekurata Assekuranz Rating-Agentur GmbH, Cologne; the market's annual survey of declared surplus rates, in its **24th edition, 2026**, per the search record at R25 in the sibling file `_research/kapitallebensversicherung.md`
- URL: not established — the study is sold, not published, and no copy or press summary was located on 2026-08-30; the title and edition number remain the sibling file's search record
- Retrieved: no — paywalled. What has changed is that the study is no longer the only route to the numbers: [S10] publishes one carrier group's full declaration including the payout-phase *Zinsüberschussanteil*, [S8] one carrier's realised *Rentenanpassung*, and [R21] reproduces five carriers' *laufende Verzinsung* for 2026 from Assekurata's own data
- Used for: the disclosure, wherever the documents state that every surplus parameter is **[std]**, that the aggregated market study itself yielded **no rate, no average, no range and no payout-phase breakdown** — true of the study, no longer true of the corpus (research gap 4 narrows). Locating it remains a high-value action for a later build, now for the **spread** rather than for a first number

(delib-sofortrente-r23)=

### R23 — Comparison-portal and broker cluster specific to the *Sofortrente*
- Publisher / doc type: `vergleich-sofortrente.de`; `lifefinance.de`; Verivox; CHECK24; and the German broker-blog cluster recorded as R24 in the sibling file `_research/klassische_rentenversicherung.md`. **No individual page URL was recorded for any member** and none is given here
- URL: not established — no individual page URL was recorded for any member of the cluster and none was located on 2026-08-30
- Retrieved: no — the cluster has no document behind it, only the sibling file's record of search summaries, each fact corroborated by at least two members, and **none of them is a price**
- Used for: most of this product's **definitional mechanics** — and this pass moves the load off it, because primary documents now carry the same facts. The *Rentengarantiezeit* continuing to the beneficiaries until the agreed term expires is [S4] § 1 Abs. 2, [S6] § 1 Abs. 1 and the GDV template's § 1 Abs. 2 [S1]; the *Kapitalrückgewähr* as the *Einmalbeitrag* less the instalments already paid, measured on the **guaranteed** annuity, is [S6] § 1 Abs. 1 and [S2] § 1 Abs. 5; the ratchet — surplus buying a permanent increment that "kann nicht mehr sinken" — is [S4] § 2 Abs. 5; monthly payment is [S4], [S5] and [S7]; the *Ertragsanteil* framing is [S8] and [R13]. What still rests on the cluster alone, and therefore stays weakly sourced, is the **market envelope**: the durations offered (5 / 10 / 15 / 20 / 25 / 30+), the typical choices (15 years to retirement age 70, 10 years thereafter, most policyholders choosing 10 to 20), and the illustration of a 10-year period with death after 6 — for which the corpus now has two primary alternatives, [S4]'s ten years with death after three and [S8]'s twenty years with death after twelve. **No price point and no charge was established from the cluster** (research gap 5); the one *Rentenhöhe* the corpus holds comes from [S8], not from here

(delib-sofortrente-r25)=

### R25 — GDV statistics on *Einmalbeiträge* and the German annuity market
- Publisher / doc type: GDV; "Die deutsche Lebensversicherung in Zahlen" and the statistical series "Neugeschäft und Bestand der Lebensversicherer für die letzten zehn Geschäftsjahre", recorded as R20 and R21 in the sibling file `_research/kapitallebensversicherung.md`
- URL: not established — neither statistical series was located at a GDV address on 2026-08-30
- Retrieved: no — the two series were not reached, and the disclosure they support is unchanged
- Used for: the disclosure that there is **no sourced number anywhere in this product's documents for the size of the German *Sofortrente* market, the contracts in force, the average *Einmalbeitrag* or the average purchase age** (research gap 7). `product-spec.md` cites it with the reason that matters and that retrieval would not have removed: the GDV series separates *Einmalbeiträge* from *laufende Beiträge*, but that line aggregates *Sofortrenten* with single-premium endowments, bAV contributions and *Zuzahlungen*, so **even a retrieved figure would not isolate this product**. The one ticket-size datum the corpus now holds is a carrier minimum, not a market average: Allianz's *Mindesteinmalbeitrag* of 3.000 € [S7]

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen;
research provenance in `_research/regulatory-actuarial.md`). That library is outside this
product's scope and is upgraded on its own pass; **the [REG-R#] entries below therefore carry
whatever retrieval status that file records, which is not this file's**, and a [REG-R#] tag
should be read against the entry it resolves to rather than against the retrievals recorded
above. Where a cross-product proposition is also carried by a document retrieved for this
product, the entry below says so. Entries cited by the `sofortrente` documents:

- **REG-R1** — Directive 2009/138/EC (Solvency II): the best-estimate-plus-risk-margin frame the projected `liability_cf` feeds.
- **REG-R2** — Delegated Regulation (EU) 2015/35: contract boundaries and the treatment of future discretionary benefits, which is where a *Sofortrente*'s *Überschussrente* would sit in a valuation.
- **REG-R3** — Directive (EU) 2025/2, the Solvency II review: context for the framework these cash flows will be measured under.
- **REG-R4** — EIOPA risk-free term structures, the UFR and the *Volatilitätsanpassung*: the curve a valuation layer discounts on, and the reason pitfall 16 insists the tariff *Rechnungszins* is not that curve.
- **REG-R5** — VAG 2016 and its Anlage 1 *Sparten*: the statutory classification of the contract.
- **REG-R6** — VAG §§ 74–110: valuation, best estimate and risk margin, cited in the valuation pointers.
- **REG-R7** — VAG §§ 124–125, *Anlagegrundsätze* and *Sicherungsvermögen*: the annuity fund is general-account capital, not an *Anlagestock*.
- **REG-R8** — VAG § 138, *Prämienkalkulation* and equal treatment: the supervisory frame around the tariff.
- **REG-R9** — VAG § 139, *Überschussbeteiligung* and the *Sicherungsbedarf* test on *Bewertungsreserven*: why the *Bewertungsreserven* share is referenced and not modelled.
- **REG-R10** — VAG §§ 140 and 145, the *Rückstellung für Beitragsrückerstattung*: where a declared *Überschussrente* is paid from.
- **REG-R11** — VAG §§ 141–143, the *Verantwortlicher Aktuar* and the 1994 deregulation: who signs the tariff bases off.
- **REG-R12** — VAG §§ 221–236 and Protektor, the *Sicherungsfonds*: what stands behind a lifelong promise, referenced in the product's risk section.
- **REG-R14** — DeckRV and its § 2, the *Höchstrechnungszins*: the reserving-rate cap `check_tariff_int_rate` tests against.
- **REG-R15** — the *Höchstrechnungszins* rate history and the regulation setting **1,00 % from 1 January 2025**, the first increase since 1994: the source of `hoechstrechnungszins_table.csv` and of the anchor cell's `tariff_int_rate`.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: cited for its **inapplicability** — there is no premium stream to zillmer against.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins* and the *Zinszusatzreserve*: the reserve that competes with the *Überschussrente* for the same RfB, referenced as a driver and never computed.
- **REG-R18** — MindZV: the statutory minimum share of each result that must reach policyholders, which bounds the discretion behind every **[std]** surplus figure — and, for an annuity, the floor under the *Risikoüberschuss* that longevity experience generates.
- **REG-R19** — RfBV, the collective part of the RfB: the mechanics behind the declaration.
- **REG-R20** — LVRG 2014: the reform that reshaped the *Bewertungsreserven* rule this product's payout phase participates in.
- **REG-R22** — VVG 2008, Kapitel 5 and § 171 (*halbzwingende Vorschriften*): the statute the product's contract-law facts come from, and the reason § 168 Abs. 3 [R1] cannot be contracted around to the policyholder's disadvantage.
- **REG-R23** — VVG §§ 8 and 152, the *Widerrufsrechte*: the withdrawal window, which is not modelled because a *Sofortrente* has no lapse machinery to absorb it into.
- **REG-R24** — VVG § 153: the cross-product entry behind the statutory *Überschussbeteiligung* and the *hälftige* share of *Bewertungsreserven* that [S3] evidences continuing into the payout phase.
- **REG-R25** — VVG §§ 154–155, *Modellrechnung* and *Standmitteilung*: the statutory basis of the document class [S15] belongs to, and what makes its absence here a real gap.
- **REG-R26** — VVG §§ 150, 159–162: consent of the *versicherte Person* and the *Bezugsberechtigung* machinery that makes the *Rentengarantiezeit* and the *Hinterbliebenenrente* work as contract law. The beneficiary is a pass-through in the model.
- **REG-R27** — VVG § 163, *Prämien- und Leistungsänderung*: cited with [R4] wherever the documents state that the *garantierte Rente* is immutable.
- **REG-R28** — VVG §§ 165–170: the cross-product entry behind [R1], [R2] and [R5] — *prämienfreie Versicherung*, *Kündigung*, *Rückkaufswert* and the *Stornoabzug*, none of which this product has.
- **REG-R30** — VVG §§ 19, 37, 38, 157: the *Altersangabe* correction rule, which matters here because the annuity is priced entirely off an age.
- **REG-R31** — VVG §§ 6, 7 and the VVG-InfoV: the disclosure regime that generates the *Verbraucherinformation* class [S2] [S3] [S14] and the *Effektivkosten* figure that was not established.
- **REG-R32** — PRIIPs, Regulation (EU) No 1286/2014: the regime behind [S12], and the source of the *Renditeminderung* form no instance of which was located.
- **REG-R33** — IDD and § 34d GewO: the distribution regime behind the *Produktinformationsblatt* class [S11].
- **REG-R34** — Unisex: CJEU C-236/09 (*Test-Achats*) and §§ 19, 20, 33 AGG. **The single most consequential cross-product entry for this model**: it is why `mort_rate_tariff` reads the blended `"U"` series and never the model point's own `sex`, and why pitfall 10 exists.
- **REG-R35** — BaFin *Merkblatt* 01/2023 (VA), *Wohlverhaltensaufsicht* and *angemessener Kundennutzen*: cited with [R18] for what is addressed to accumulation products and not to payout annuities.
- **REG-R36** — the BGH line of authority on German life contracts: the interpretive background to the AVB facts, and to the narrowing of § 163 [R4].
- **REG-R37** — GDV *Musterbedingungen* and German market practice: the cross-product entry behind [S1] and [S9].
- **REG-R38** — AltEinkG and the *Drei-Schichten-Modell*: what places this contract in **Schicht 3** — no deduction going in, *Ertragsanteil* coming out.
- **REG-R41** — EStG § 22 Nr. 1 Satz 3 Buchst. a: the cross-product carrier of the *Ertragsanteil* rule behind [R13], and the entry the documents cite for taxation falling on the annuitant rather than on the insurer's liability.
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6, the 12/62 rule: cited with [R14] for the boundary a *Sofortrente* can never cross.
- **REG-R46** — ErbStG and SGB V §§ 226, 229, 240: the *Erbschaftsteuer* treatment of a post-death payment and social-contribution treatment of an annuity in payment, both **not established** for this product (research gap 15).
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the entry behind the two-dimensional *Sicherheitszuschlag* — lighter level **and** stronger trend — and behind the statement that the DAV tables are not redistributed here.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand, the generational annuity tables: the cross-product entry behind [R10] and [R11], and the authority for the generational structure a replacement table must preserve.
- **REG-R52** — Destatis *Sterbetafeln* and *Generationensterbetafeln*, with their reuse licence: the intended base for a user-supplied replacement decrement table, and the comparator for the statement that population mortality overstates deaths in an annuity book.
- **REG-R53** — the German life market in numbers (GDV, BaFin, Assekurata, Map-Report, Morgen & Morgen, Franke und Bornberg): the cross-product carrier of the market statistics [R25] and [R22] could not supply.
- **REG-R54** — HGB §§ 341–341o and RechVersV: the statutory accounts in which the *Bewertungsreserven* the model excludes are measured.
- **REG-R55** — IFRS 17 and the Variable Fee Approach: one of the two liability measures these cash flows feed; not computed here.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional standard this documentation sits under, and the cross-product carrier of [R8].

---

## Provenance note

Extraction details — which fact was read from which document, the section-by-section
mechanics, and the nineteen-item gaps-and-caveats register — live in
`_research/sofortrente.md`, which is the citation ground truth for the S# and R# numbering
used here. That file is frozen and is not amended; where this pass has contradicted it, the
correction is recorded in the entry above and in `technical-notes.md`, not in the research
file. What follows is what the entries above now support, and it is materially different from
what the same note said before the documents were opened.

**Nineteen of this file's thirty-two entries now read `Retrieved: yes` and twelve read `no`**,
one being mixed; the retrieved set includes every insurer document in the S section. Of the two entries whose titles name the immediate annuity, **both
now yield clauses**: [S4] is NÜRNBERGER's AVB for tariff NR3303 in full, and [S2] is Zurich
Deutscher Herold's *Verbraucherinformation* — though the retrieval showed that entry's recorded
title and vintage to be wrong, and the pack to be a Schicht-2 *Direktversicherung* wrapper. The
GDV publishes an **association template for exactly this product** ([S1], Stand 21.07.2025) and
a matching survivor's-annuity rider set; the earlier finding that it does not is withdrawn, and
research gap 3 closes.

**Paragraph numbers, clause headings and sentences of German contractual wording for a
*Sofortrente* now appear throughout this file**, quoted from the documents. The load-bearing
ones are the no-termination clause at three carriers and in the GDV template; the
*Rechnungsgrundlagen* clauses naming DAV 2004R (Aggregattafel) at 1,00 % [S2] [S3] and
NÜRNBERGER Tafel 2013 R at 1 % [S4]; [S5]'s statement that a deferred tariff converts on the
carrier's own *Sofortrente* bases, naming tariff NR3303; and [S6]'s *Kapitalrückgewähr* and
reducible-*Zusatzrente* clauses.

**Three claims the library made are contradicted by the documents and have been corrected
here.** [S6] contains neither "DAV 2004 R" nor the "0 percent p.a." interest rate the library
quoted from a search summary; its only tariff rate is 0,90 %, which was the *Höchstrechnungszins*
of its own 01/2017 vintage, so **no retrieved document shows a carrier pricing below the cap**.
The Allianz KomfortDynamik page [S7] carries none of the three propositions attributed to it.
And **§ 168 Abs. 3 VVG does not say what [R1] said it says** — the *Sofortrente*'s
irrevocability follows from § 168 Abs. 1 and Abs. 2 not engaging at all, and § 169 from its own
Abs. 1 gateway; gap 9 closes on [REG-R28]'s reading.

**The quantitative hole is no longer total.** [S8] prints a carrier's own rate scale — tariff
S1, 50.000 € single premium, 20-year *Rentengarantiezeit*, Stand 01.01.2025, **151 € a month at
65** — together with a realised *Rentenanpassung* of 0,75 % for 2024; [S10] declares a
payout-phase *Zinsüberschussanteil* of 3,35 % less the *Rechnungszins* for 2026, funded from
interest surplus alone; [R20] gives market-average *Rentenfaktoren* of 29,09 € and 25,97 € per
10.000 € for 2021 and 2022; [R21] gives five carriers' *laufende Verzinsung* for 2026; and [S7]
gives a 3.000 € minimum and an 85-year maximum entry age. **None of these is used to calibrate
the model**, whose annuity, charge and surplus tables remain **[std]** and are anchored to
reproduce the worked example; they are recorded as benchmarks a later build should price
against, and the divergence between them and the [std] scale is stated in `technical-notes.md`
rather than resolved.

**What is still not established.** No *Produktinformationsblatt* [S11] and no
*Basisinformationsblatt* [S12] was located for any carrier, so **no total annuity including
declared surplus and no charge parameter of any kind** was read — α, β, *Effektivkosten* and
*Renditeminderung* remain **[std]** with no observed range, and whether a payout-only
*Sofortrente* is within PRIIPs scope is unresolved. No *Standmitteilung* specimen was found
[S15]. DAV 2004 R remains DAV property, established structurally and not numerically [R10], its
*Bestand* companion barely at all [R11], so the shipped decrement CSV is still a **[std]** proxy
and the `Data` docstring still says so. No carrier's short-deferment variant was located, "Rente
flex" having turned out to be a hybrid unit-linked deferred annuity [S14], so gap 17 closes as a
negative. And the *Hinterbliebenenrente* percentages stay `[unverified]`: the GDV rider template
states no level at all [S9].

**One retrieved fact contradicts a modelled convention and is deliberately not acted on here.**
The model pays *vorschüssig*, first instalment at inception, as a **[std]** convention adopted
because nothing had been read. Two carriers' AVB now say otherwise: [S4] — "Die erste Rente wird
einen Monat nach dem vereinbarten Versicherungsbeginn gezahlt" — and [S6], which pays the first
instalment "ein Jahr, ein halbes Jahr, ein viertel Jahr oder einen Monat nach dem vereinbarten
Versicherungsbeginn" according to frequency. **The German market convention for a *Sofortrente*
is payment in arrears.** Changing it moves the worked example and its golden tests, so it is
reported and not made; `technical-notes.md` carries the finding beside model point 9, which
already measures the alternative. The research file's own estimate of what the timing is worth
remains wrong by a factor of twelve — an annual-annuity identity applied to a monthly annuity —
and that correction, recorded at 0,34 % from model points 1 and 9, stands.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-sofortrente-r1
[R10]: #delib-sofortrente-r10
[R11]: #delib-sofortrente-r11
[R12]: #delib-sofortrente-r12
[R13]: #delib-sofortrente-r13
[R14]: #delib-sofortrente-r14
[R18]: #delib-sofortrente-r18
[R19]: #delib-sofortrente-r19
[R2]: #delib-sofortrente-r2
[R20]: #delib-sofortrente-r20
[R21]: #delib-sofortrente-r21
[R22]: #delib-sofortrente-r22
[R23]: #delib-sofortrente-r23
[R25]: #delib-sofortrente-r25
[R4]: #delib-sofortrente-r4
[R5]: #delib-sofortrente-r5
[R8]: #delib-sofortrente-r8
[REG-R10]: #delib-reg-r10
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R24]: #delib-reg-r24
[REG-R25]: #delib-reg-r25
[REG-R26]: #delib-reg-r26
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R56]: #delib-reg-r56
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
