# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/klassische_rentenversicherung.md` (the
citation ground truth for this product) and are **frozen — never renumber**. Unused ids are
omitted downstream, leaving gaps; **this product has none.** All nineteen primary sources
**S1–S19** and all twenty-four product-specific references **R1–R24** are cited by
`product-spec.md`, and the subset the model itself rests on is cited again in
`technical-notes.md` and `model.md`, so the numbering below runs unbroken. No source was newly
added at drafting. Access dates: **2026-08-29** at drafting, when this list was assembled without
opening a document, and **2026-08-30** for the re-verification pass each entry below records.
Cross-product [REG-R#] tags are listed in their own section at the end.

**Retrieval conditions — read this before reading anything below.** This file was drafted under
one set of conditions and re-verified under another. Both belong in the record and both are
stated here rather than glossed.

1. **How it was drafted.** Direct HTTP egress from the build environment was blocked by an
   organisation network policy: `WebFetch` and `curl` were refused with HTTP 403 at the egress
   gateway for every host outside a short package-registry allowlist, and every host that matters
   for this product — `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`, `dejure.org`,
   `de.wikipedia.org`, and every insurer host named below (`zurich.de`, `cosmosdirekt.de`,
   `nuernberger.de`, `debeka.de`, `allianz.de`) — was tried and refused. The only research channel
   was `WebSearch`, which returns titles, URLs and search-engine summaries: real evidence, and
   several of the load-bearing facts below first came back as near-verbatim renderings of a
   document's own sentences, but a *secondary summary* and never the document itself. Its session
   budget, shared across fourteen parallel researchers, was **exhausted after eighteen queries on
   this product**. **Not one document listed here had been opened when these entries were first
   written**, and the draft rested on the authoring model's own knowledge of German insurance law
   and practice, disciplined by `[std]` on every level it standardized and `[unverified]` on every
   specific it could not confirm.
2. **How it stands now.** That policy has been lifted and the citations were re-verified against
   the primary documents on 2026-08-30. **Thirty-six of the forty-three entries below read
   `Retrieved: yes`**, which means one thing exactly: the document was opened and the passage the
   entry rests on was read — the AVB, *Verbraucherinformationen*, *Kundeninformationen* and the
   surplus declaration as PDFs with their § numbering, page counts, document codes and *Fassungen*
   intact, and the statutes [R1]–[R7] as canonical XML from gesetze-im-internet with each law's
   amendment *Stand* recorded on the entry. **Four entries were reached only in part.** [R12] and
   [R13], the DAV *Sterbetafel* documents, came through a 3 MB transfer cap and a defective
   character mapping, so their structure is read and nothing is quoted from them; [R14] holds four
   URLs, of which two conference decks were retrieved while a Springer article answered with a
   bot-challenge page and a qx-Club PDF failed TLS host verification; [R19] holds two, of which
   the second answers HTTP 404. **Three could not be opened at all**: [S17], a Zurich product page
   that answers HTTP 200 with a 212-byte shell and no page body; [S19], a DEVK asset path that
   answers HTTP 403 to the cited URL and to a retry; and [R23], a VersicherungsJournal article
   whose body sits behind a premium paywall. All seven are kept as known references, and each
   states its own failure on its own line.

Library-wide, the same pass leaves **501 of delib's 805 source entries (62 %) at `Retrieved:
yes`**; all fifteen German instruments the library cites were read as canonical XML with their
*Stand* recorded, and of 950 statutory section references checked across delib, 950 were correct.
This product's share of that is forty of its forty-three entries reached in whole or in part.

What follows from it cuts two ways. Where an entry reads `Retrieved: yes`, the § numbers,
*Fassungen*, page counts and quoted sentences below were transcribed from the document itself.
Where it does not, **a delib citation is still a pointer, not a certificate**: it names the
instrument a claim should be checked against and does not assert that anyone checked it, and the
entry says so. Nothing was invented under either regime — no URL, no document reference number, no
paragraph number and no figure was guessed; where a URL was not established the entry reads
`URL: not established`; and where a phrase appears in quotation marks it is either transcribed
from a retrieved document or attributed to the search summary that returned it. **The
re-verification changed things**, and the entries record what it changed: [S8] does not contain
the DAV 2004 R sentence the corpus once leaned on hardest, [S11]'s living URL now serves a
successor design rather than the classic chassis, [S1] leaves the pre-annuity death benefit blank,
and [S4] carries a post-*Rentenbeginn* death benefit the library had recorded as unmentioned by
any source. `[unverified]` keeps its meaning and is now the narrower claim: a specific paragraph
number, effective date, tariff level or market figure that no retrieved document confirms. And
**every quantitative parameter of the reference implementation that the corpus did not establish
is a `[std]` standardization with a stated rationale**, never a number attributed to a source that
does not carry it. The corpus still establishes the *mechanics* of this product far more
thoroughly than its *levels* — the pass added *Rentenfaktor* ranges [R19] [R24] and one carrier's
declaration [S15], and no charge, expense or behavioural level at all — which is why `model.md`'s
standardization table is as long as it is, and why `model.md` now also records where the shipped
levels diverge from what was read.

---

## Primary product sources

(delib-klassische_rentenversicherung-s1)=

### S1 — GDV, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung" (Musterbedingungen)
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin; *Musterbedingungen* — the association's model general policy conditions for a deferred annuity contract, which individual insurers adopt, adapt or ignore
- URL: https://www.gdv.de/resource/blob/6294/61b4fedd6f69db77539816e3421c7eeb/allgemeine-bedingungen-fuer-die-rentenversicherung-mit-aufgeschobener-rentenzahlung-data.pdf
- Retrieved: yes (PDF, 20 pp., **Stand: 21.07.2025**, twenty §§, read 2026-08-30)
- Used for: the model wording for **exactly the product in scope**, and hence the composite representative design. **The clause text is now read, and it revises what this entry could previously claim.** The disclaimer is the document's own first line — *"Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ. Abweichende Bedingungen können vereinbart werden."* (Stand 21.07.2025) — which is the argument for describing a **composite** rather than adopting one carrier's wording wholesale. What the wording fixes: the life annuity and its payment frequencies (§ 1 Abs. 1); the *Kapitalabfindung* at the first annuity due date, with the notice period left to the carrier (§ 1 Abs. 2); the ***Rentengarantiezeit*** in the exact shape the model implements — *"Wir zahlen die vereinbarte Rente auch bei Tod der versicherten Person bis zum Ende der Rentengarantiezeit"* with a worked ten-year example (§ 1 Abs. 4); the *Überschussbeteiligung* machinery, the *verursachungsorientiertes Verfahren*, the *Gewinnverband* and the annual *Überschussdeklaration* by the board on the *Verantwortlicher Aktuar*'s proposal (§ 2 Abs. 2–4); the *Bewertungsreserven* re-measured annually **and additionally at contract termination before the annuity, at the start of annuity payment, and at each year end during the annuity** (§ 2 Abs. 5), allocated at the *Beendigung der Ansparphase* by death, surrender or survival to the *Rentenzahlungsbeginn* (§ 2 Abs. 6); the surrender machinery (§ 12) and the *Beitragsfreistellung* (§ 13) that [R1] and [R2] are read into; and the **acquisition-cost charging rule** in § 14 Abs. 2 — *"Der auf diese Weise zu tilgende Betrag ist nach der Deckungsrückstellungsverordnung auf 2,5 % der von Ihnen während der Laufzeit des Vertrages zu zahlenden Beiträge beschränkt"* — the 25 ‰-of-*Beitragssumme* ceiling in the carrier's own words [R7] [REG-R16]. **Correction.** The previous entry recorded that *Beitragsrückgewähr* is "the model wording's own term", which the retrieved text only half supports: **§ 1 Abs. 3, the death benefit before the *Rentenzahlungsbeginn*, is left blank** — *"zahlen wir …"* against a footnote reading *"Unternehmensindividuell zu ergänzen"* — and the word *Beitragsrückgewähr* appears only in the footnotes to §§ 4 and 5, as the benefit form the wording assumes a carrier will fill in. So the model conditions **name** the concept but **do not specify the pre-annuity death benefit at all**; `death_benefit_form = prem_refund` rests on the carrier wordings [S8] [S9] and not on this one. Gap 2 is closed for this document: the § numbering, clause text and page count are established

(delib-klassische_rentenversicherung-s2)=

### S2 — GDV, "02 GDV-Musterbedingung LV — Rentenversicherung mit aufgeschobener Rentenzahlung" (second GDV resource path)
- Publisher / doc type: GDV; *Musterbedingungen*, second content hash under the same GDV resource path as [S1] (blob id 6294 in both)
- URL: https://www.gdv.de/resource/blob/6294/cacd502172fab87ad8859d194d9352c8/02-gdv-musterbedingung-lv-rentenversicherung-mit-aufgeschobener-rentenzahlung-2021-data.pdf
- Retrieved: yes (PDF, 20 pp., **Stand: 21.07.2025**, read 2026-08-30)
- Used for: **nothing that [S1] does not already carry, and one correction.** The previous entry took the `…-2021-…` in the file name for an edition date and described this as the 2021 vintage of the family, placing it under the 0,90 % *Höchstrechnungszins*. Both GDV URLs in fact serve **one and the same document** — page for page identical extracted text, *Stand: 21.07.2025* — so the "two editions of one family" reading is withdrawn, and with it the 2021 dating. The disclaimer previously quoted from a search summary as *"Diese Bedingungen sind unverbindlich"* reads, in the document itself, *"Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ"*; it is quoted from [S1]. The entry is kept because the id is frozen and because the duplicate path is itself worth recording: a GDV blob id addresses a living file, not a vintage

(delib-klassische_rentenversicherung-s3)=

### S3 — GDV, "Musterbedingungen" service index
- Publisher / doc type: GDV; publisher index page listing the association's model-condition sets
- URL: https://www.gdv.de/gdv/service/musterbedingungen
- Retrieved: yes (HTML index, read 2026-08-30)
- Used for: the **product taxonomy that fixes this product's boundary**, now read off the index itself. Under *Rentenversicherungen* the association publishes, as separate condition sets: *"Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung"* — this product [S1] [S2]; *"… für die Rentenversicherung gemäß § 10 Absatz 1 Nr. 2 Buchstabe b Doppelbuchstabe aa EStG (Basisrente-Alter)"*; *"… für die Rentenversicherung mit sofort beginnender Rentenzahlung"* — delib's `sofortrente`; *"… für die fondsgebundene Rentenversicherung"*; and two *Altersvorsorgevertrag*-qualified sets under the *Altersvorsorgeverträge-Zertifizierungsgesetz*, one unit-linked and one not. A parallel *Hinterbliebenenrenten-Zusatzversicherung* set exists for each of the three annuity families, the deferred-annuity one being [S10]. This product's model conditions are the only annuity set **without a statutory qualification in the title**, which is the Schicht-3 placing in the product spec's scope note; the optional character of the wording is [S1]'s own first line

(delib-klassische_rentenversicherung-s4)=

### S4 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung, Private Vorsorge (Schicht 3) und Rückdeckungsversicherung (Schicht 2)", Fassung 01/2026
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation* — the consolidated pre-contractual pack (general information, AVB, special conditions for riders and options, tax notes). Document code **521331262 2601** appears in the search result's title line
- URL: https://www.zurich.de/-/media-assets/project/zurich-headless/germany/br/documents/verbraucherinformationen/32020_aufgeschobene-rentenversicherung_verbraucherinformationen_2026_01.pdf
- Retrieved: yes (PDF, 66 pp., document code 521331262 2601, Fassung 01/2026, twenty-four §§ of AVB plus six of *Anpassungsversicherung* conditions, read 2026-08-30)
- Used for: **the current-vintage anchor document of the whole corpus**, and now for clause content rather than for its existence. The insurer's own *Schicht 3* placing and the word *konventionell* are on the cover; the pack structure the product spec follows is its table of contents. What the AVB fix:
  - ***the calculation basis, in one sentence*** — § 1 Abs. 6: *"Die Kalkulation der bei Vertragsbeginn im Versicherungsschein genannten Leistungen basiert auf der Sterbetafel DAV 2004R (Aggregattafel); es wird ein Rechnungszins in Höhe von 1,00 % verwendet."* This is the corpus's **primary-source establishment of DAV 2004 R as the tariff table** [R12] [R13] and of the 1,00 % *Rechnungszins* of a 2026-issue contract [R7] [R8].
  - **the base design and its two extensions**: without an extension the contract simply lapses on death before the *Rentenzahlungsbeginn* (§ 1 Abs. 2); *Beitragsrückgewähr in der Aufschubzeit* refunds the premiums paid net of rider premiums (§ 1 Abs. 3); a *Rentengarantiezeit* pays *"die garantierte Rente zuzüglich zugewiesener Überschüsse mindestens bis zum Ablauf der Rentengarantiezeit"* (§ 1 Abs. 4).
  - **the *Kapitalwahlrecht* notice period** (§ 2 Abs. 2–3): where the payout phase carries no death cover the application must reach the insurer *"wenigstens drei Jahre vor Rentenzahlungsbeginn"*; where it does, at a twelve-year *Aufschubzeit* not earlier than five months before the first annuity date, and at a longer one not before the twelfth policy year has run. A partial commutation needs a residual annuity above the *Mindestrente* and a payout of at least 2 500 EUR (§ 2 Abs. 4).
  - **the *Dynamik*** as a documented option with its own condition set, ***"Besondere Bedingungen für die Anpassungsversicherung in der Rentenversicherung"*** (pp. 19–20), which is what makes `dynamik_rate` a module rather than an invention: a fixed percentage on the previous year's premium, at each policy anniversary, until the end of the premium-paying term, opposable by the policyholder within three months.
  - **the *Bewertungsreserven*** (§ 3 Abs. 2): *"Derzeit sieht § 153 Absatz 3 VVG eine hälftige Beteiligung an den Bewertungsreserven vor"*; *"Bei Rentenversicherungen ist neben Tod und Rückkauf während der Ansparphase der Übergang in den Rentenbezug maßgeblicher Zeitpunkt für die Beteiligung an den Bewertungsreserven"*; and participation continues during the payout phase — all three cited, the first two modelled and the third deliberately not [R4].
  - **the payout-phase surplus systems**, named (§ 3 Abs. 7): *Garantie-PLUS-Rente* (a level supplementary annuity), *Bonusrente* (all surplus to increasing the annuity) and *Bonus-PLUS-Rente* (part level, part increasing) — the *konstant* / *volldynamisch* / *teildynamisch* taxonomy of [R19] [R20] in a carrier's own terms, with the warning that for the RfB-financed part *"wird die Rentenhöhe jeweils nur für ein Versicherungsjahr zugesagt"*.
  - **the surrender and paid-up rules** (§ 10) with a *Stornoabzug* that is **a flat 250 EUR**, waived at attained age 62 or after twenty years, plus a 10 % deduction on any excess of the surrender value over the death benefit; and the five-year spreading floor with the *Höchstzillmersätze* reserved (§ 10 Abs. 3), the 2,5 %-of-*Beitragssumme* cap being § 11 Abs. 2.
  - **a *Mindestrente*** of *"25 EUR bei monatlicher Rentenzahlungsweise"* (footnote 1), the first carrier level the corpus has for the § 165 *Mindestversicherungsleistung* threshold [R2].
  - **the *Ertragsanteil* address**, § 22 Nr. 1 Satz 3 a) bb) EStG, and the 12/62 rule, both in the *Allgemeine Steuerhinweise* [R5] [R6].

  **Correction.** The *Rentenfaktor* conversion rule previously attributed to this document is **not in it**: the string *Rentenfaktor* does not occur anywhere in the 66 pages, and the AVB express the payout-phase increase in *Renten* rather than in factors. `annuity_rate_appl() = max(f_g, f_c)` is re-sourced to [S9] and [S14], which state it in terms, and to [S18] and [S11] for the per-10 000-EUR arithmetic.

  **Contradiction.** § 1 Abs. 5 offers ***Beitragsrückgewähr während der Rentenzahlungszeit*** as an alternative to the *Rentengarantiezeit*: on death after the *Rentenzahlungsbeginn* the premiums paid are refunded less rider premiums and less annuities already received, the deduction being taken *"nur in Höhe der zu Vertragsbeginn garantierten Renten"*, and the claim lapses once instalments received exceed premiums paid. The library recorded (gap 18) that no source in this corpus mentions this benefit. That is now false, and it is the one place where a retrieved document reaches a **modelled** fact: `claims_death(t)` is zero for every `t` after the *Rentenbeginn*. The model is unchanged in this pass and the divergence is stated in `model.md`

(delib-klassische_rentenversicherung-s5)=

### S5 — Zurich Deutscher Herold Lebensversicherung AG, same series, **Fassung 07/2015 (Konsortialversicherung — Private Vorsorge)** — 44 pages
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung (Konsortialversicherung), Private Vorsorge*. Document code **521331422 1507**; title line "Seite 1 von 44"
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/330202101_aufgeschobene-rentenversicherung-private-vorsorge_verbraucherinformationen_2021_01.pdf
- Retrieved: yes (PDF, 44 pp., document code 521331422 1507, Fassung 07/2015, read 2026-08-30)
- Used for: **the earliest vintage of the [S4] wording family and the hard end of the guarantee-vintage chronology.** Its § 1 Abs. 6 is [S4]'s sentence with one number changed — the same *"Sterbetafel DAV 2004R (Aggregattafel)"*, *"es wird ein Rechnungszins in Höhe von 1,25 % verwendet"*. With [S7] and [S16] at 1,00 % (Fassung 01/2025) and [S4] at 1,00 % (Fassung 01/2026), one carrier's own AVB carry **three *Höchstrechnungszins* levels across eleven years on an otherwise stable wording**, which is the documentary basis for treating `int_rate_guar` as a model-point attribute and for the product spec's guarantee-vintage discussion. The document code's `1507` suffix is the edition month, and the pack's section list — contract partners, scope of cover, design options, *Überschussbeteiligung* — is as the product spec describes it.
- **Two corrections.** The previous entry dated this *Fassung 01/2021*, reading the `…_2021_01.pdf` in the URL as an edition; the file itself says *in der Fassung 07/2015*, so a Zurich media path names a slot and not a vintage. And it is the **Konsortialversicherung** edition, which is the characteristic the previous entry attributed only to [S6]; [S5] and [S6] are the *Private Vorsorge* and *Rückdeckungsversicherung* wrappers of one consortium wording

(delib-klassische_rentenversicherung-s6)=

### S6 — Zurich Gruppe, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung (Konsortialversicherung), **Rückdeckungsversicherung**" — 46 pages
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation*, consortium (*Konsortialversicherung*) edition, *Rückdeckungsversicherung* wrapper. Document code **521331432 1507**; title line "Seite 1 von 46"
- URL: https://www.zurich.de/-/media-assets/project/zurich-headless/germany/docs/privatkunden/vorsorge-und-vermoegen/existenzsicherung/231_zurich_gruppe_vi_aufgeschobene_rentenversicherung_konsortial.pdf
- Retrieved: yes (PDF, 46 pp., document code 521331432 1507, Fassung 07/2015, read 2026-08-30)
- Used for: the product spec's variation section, and the same one finding — **one carrier issues the same wording in more than one distribution wrapper** — which the retrieval now demonstrates rather than infers. [S5] and [S6] are the same Fassung 07/2015 consortium wording issued as *Private Vorsorge* and as *Rückdeckungsversicherung*; their § 1 Abs. 6 is character-for-character the same sentence, DAV 2004R (Aggregattafel) at a *Rechnungszins* of 1,25 %, and the two packs differ by two pages of wrapper-specific notes. The wrapper changes the parties to the contract and **not the cash flows**, which is why the model carries no wrapper attribute

(delib-klassische_rentenversicherung-s7)=

### S7 — Zurich Deutscher Herold Lebensversicherung AG, same series, **Fassung 01/2025 — Direktversicherung nach § 3 Nr. 63 EStG (Schicht 2)**
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation für Direktversicherungen nach § 3 Nr. 63 EStG — Aufgeschobene Rentenversicherung (Schicht 2)*. Document code **521331392 2501**
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/220202101_aufgeschobene-rentenversicherung_verbraucherinformationen_2022_01.pdf
- Retrieved: yes (PDF, 58 pp., document code 521331392 2501, Fassung 01/2025, read 2026-08-30)
- Used for: the chronology, now with the number attached. Its § 1 Abs. 7 is [S4]'s and [S5]'s sentence again — DAV 2004R (Aggregattafel), *"es wird ein Rechnungszins in Höhe von 1,00 % verwendet"* — so with [S5] at 1,25 % (07/2015) and [S4] at 1,00 % (01/2026) the carrier's own packs date the guarantee vintages the model layers.
- **Two corrections.** The Fassung is **01/2025**, not 01/2022; the document code's `2501` suffix agrees with the document and not with the URL slug. And this edition is a ***Direktversicherung* under § 3 Nr. 63 EStG — Schicht 2, occupational**, not the Schicht-3 private annuity of [S4]. The wording is the same chassis in a different tax layer, which is why the *Rechnungszins* sentence transfers; nothing layer-specific is drawn from it, and the product spec's scope note stays with [S4]

(delib-klassische_rentenversicherung-s8)=

### S8 — Cosmos Lebensversicherungs-AG (CosmosDirekt), "Allgemeine Bedingungen für die Rentenversicherung", LA 904 A
- Publisher / doc type: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland; *Allgemeine Bedingungen* (AVB) for a *Rentenversicherung*, tariff code **LA 904 A**, edition **(01.17)** printed on every page
- URL: https://www.cosmosdirekt.de/resource/blob/89106/31bbdccea1c7a5a530feb9e2a3be8d1c/allgemeine-bedingungen-rentenversicherung-la-904-a--data.pdf
- Retrieved: yes (PDF, 8 pp., LA 904 A (01.17), eighteen §§, read 2026-08-30)
- Used for: **the base-design death benefit and the guarantee-below-the-cap finding**, both now from clause text. § 1 Abs. 1: *"Stirbt die versicherte Person während der Aufschubzeit, so zahlen wir als Todesfall-Leistung die eingezahlten Beiträge (Beitragsrückgewähr) ohne Zinsen und ohne die Beiträge etwa eingeschlossener Zusatzversicherungen zurück."* That is `death_benefit_form = prem_refund` with `db_incl_surplus = False`, in one sentence, and it is the wording behind the base design that [S1] leaves blank. § 1 Abs. 2 fixes the accumulation in the same breath: *"Dieses bilden wir, indem wir die eingezahlten Beiträge abzüglich der tariflichen Kosten und Risikobeiträge mit dem tariflichen Garantiesatz von 0,90 Prozent p. a. verzinsen"* — premium less charges and risk cost, rolled at the guaranteed rate, which is the *Deckungskapital* recursion the model implements. Also: the three surplus sources and their MindZV shares, *"grundsätzlich 90 Prozent"* of net investment return, 90 % of the risk result and 50 % of the *übriges Ergebnis* [REG-R18]; a **Treuhänder clause** on the *Rechnungsgrundlagen* used for the surplus annuity at *Rentenbeginn* [R3] [R17]; a *Mindestrente* of 600,00 EUR a year for a partial surrender; and § 7 Abs. 10, *"Bei einer Kündigung oder Beitragsfreistellung bzw. einer Reduzierung der Beitragshöhe Ihrer Versicherung erheben wir keine Stornoabzüge bzw. sonstigen Gebühren"*.
- **Vintage established** (closing gap 5): **01.17**, January 2017, which is inside the 0,90 % *Höchstrechnungszins* regime and makes the 0,90 % *Garantiesatz* the statutory maximum of its day rather than a discount to it.
- **Contradiction.** The previous entry took from a search summary that this document states the annuity factor to be calculated on *"a recognised mortality table (currently DAV 2004 R) and an underlying interest rate (currently 0 percent p.a.)"*, and made it the corpus's most load-bearing sentence. **Neither element survives retrieval.** The string *DAV* does not occur in LA 904 A; the only rate it names is the 0,90 % *tariflicher Garantiesatz*; and the *Sicherheitsabschlag* argument built on "0 percent against a higher cap" therefore has no basis here. DAV 2004 R is re-sourced to [S4] [S5] [S6] [S7] [S16], which name it in terms; a guaranteed basis materially below the current *Höchstrechnungszins* is re-sourced to [S11], whose *Rentenfaktor* runs on 0,1 % against a tariff *Rechnungszins* of 1 %, and to [R22]'s 0,5 %

(delib-klassische_rentenversicherung-s9)=

### S9 — NÜRNBERGER Lebensversicherung AG, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung und Rentengarantiezeit nach Tarif NIR3301"
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; AVB for a deferred annuity **with *Rentengarantiezeit***, tariff **NIR3301**, publisher document id `gn331451_p`, internal edition id **GN331451_202501** (January 2025) printed on every page
- URL: https://www.nuernberger.de/medien/4allportal/gn331451_p.pdf
- Retrieved: yes (PDF, 17 pp., GN331451_202501, twenty-one §§, read 2026-08-30)
- Used for: **the two conversion rules the model implements, both now verbatim, and the payout-phase mechanics.**
  - *Conversion input* (§ 1 Abs. 1): *"Bei der damit erfolgenden Verrentung wird der Vertragswert zuzüglich gegebenenfalls vorhandener Werte aus dem Schlussüberschuss und aus der Beteiligung an den Bewertungsreserven herangezogen …, mindestens aber der garantierte Vertragswert."* That is `capital_conv_pp() = max(guar_capital_pp, av + av_sur + val_reserve)`, and it is the reason the commuting policyholders receive the same amount.
  - *`max(f_g, f_c)`* (§ 1 Abs. 1): *"Wir prüfen bei jeder Monatsrente einzeln, ob die rechnungsmäßige Rente samt den in der Aufschubdauer und im Rentenbezug entstandenen Überschüssen höher ist als die garantierte Mindestrente und zahlen immer den höheren Betrag."* The corpus's clearest statement of `annuity_rate_appl() = max(f_g, f_c)`, and stronger than the model's implementation: the test is re-run at **every monthly instalment**, not once at the *Rentenbeginn*.
  - *What the current factor is taken from* — the *Rentenfaktor* is set at the *Rentenzahlungsbeginn* from the carrier's then-current interest rate and own annuity table, and *"maßgeblich sind Rechnungszins und Sterbetafel in der Beitragskalkulation vergleichbarer, dann bei uns zum Verkauf geöffneter Rentenversicherungen mit sofort beginnender Rentenzahlung"*, with a named comparable tariff (NR3303), a most-favourable rule where several comparables exist, and an independent *Treuhänder* review. This is the primary-source basis for indexing `rentenfaktor_table.csv` by attained age at *Rentenbeginn* and for [S16]'s presence in this file.
  - *The guaranteed basis*: the *garantierte Mindestrente* is computed on *"die Rententafel NÜRNBERGER Tafel 2013R mit einem garantierten Rechnungszins von 1 % p. a."* — a carrier's **own** annuity table rather than DAV 2004 R itself, which is what [R12]'s *Rechnungsgrundlagen erster Ordnung* discipline looks like in a contract.
  - *Death before the annuity* (§ 1 Abs. 3): the benefit is the contract value plus final surplus and *Bewertungsreserven*, **at least the *Beitragsrückgewähr*** — the `max(Deckungskapital, premiums paid)` shape that gap 18 recorded as unestablished for the classic product. It is established here.
  - *Payment timing* (§ 1 Abs. 1): *"Wir zahlen die Rente monatlich, jeweils zum Monatsersten"* — monthly in advance, which is the convention `model.md` adopts as `[std]` (gap 19 is closed at one carrier).
  - *The payout-phase surplus systems* (§ 2 Abs. 5 c): *dynamische Überschussrente*, where the level reached *"kann nicht mehr sinken"*, and *teildynamische Bonusrente* — the *volldynamisch* / *teildynamisch* pair of [R19] [R20] in a carrier's own words.
  - *No Stornoabzug*: § 14 Abs. 4 is headed *"Kein Abzug"* — *"Von dem nach Absatz 3 ermittelten Wert nehmen wir keinen sogenannten Stornoabzug (§ 169 Absatz 5 VVG) vor."* — and § 16 Abs. 3–4 restate the *Zillmerverfahren* cap at *"2,5 % der von Ihnen während der Laufzeit des Vertrags zu zahlenden Beiträge"* and the five-year *Mindestwert*, the third carrier in this file to do so.
  - The ***Rentengarantiezeit* as a tariff-level design feature carried in the product name** stands, and § 1 Abs. 5 carries the same ten-year worked example as [S1]; a *Mindestrente* of 25,00 EUR a month agrees with [S4]. Paragraph numbering is now established throughout

(delib-klassische_rentenversicherung-s10)=

### S10 — GDV, "Allgemeine Bedingungen für die Hinterbliebenenrenten-Zusatzversicherung zur Rentenversicherung mit aufgeschobener Rentenzahlung"
- Publisher / doc type: GDV; *Musterbedingungen* for the **survivor's-annuity rider** attaching to this product
- URL: https://www.gdv.de/resource/blob/6336/942f7b9aec6a969b486ec205279870a3/allgemeine-bedingungen-fuer-die-hinterbliebenenrenten-zusatzversicherung-zur-rentenversicherung-mit-aufgeschobener-rentenzahlung-0-pdf-data.pdf
- Retrieved: yes (PDF, 6 pp., **Stand: 14.11.2019**, four §§, read 2026-08-30)
- Used for: the finding that the market treats the **survivor's annuity as a *Zusatzversicherung* with its own condition set** — which the retrieved document settles: four paragraphs, opening *"Die Hinterbliebenenrenten-Zusatzversicherung ergänzt die als Hauptversicherung abgeschlossene Rentenversicherung"*, and carrying its own *Überschussbeteiligung* clause (§ 3) rather than sharing the main contract's. That is why the reference implementation carries it as a **module that is off**. Clause content is now established, and it adds one mechanic the previous entry could not see: **the rider and the *Rentengarantiezeit* do not stack.** § 1 Abs. 3 — *"Wenn die versicherte Person nach dem Rentenzahlungsbeginn der Hauptversicherung stirbt, und für diese eine Rentengarantiezeit vereinbart ist, zahlen wir die Hinterbliebenenrente erst nach Ablauf der Rentengarantiezeit"* — so the two post-*Rentenbeginn* death mechanics the corpus establishes run in sequence, the guarantee period first. § 2: if the *mitversicherte Person* dies first the rider simply ends with no benefit. [S4] carries the same rider as *Besondere Bedingungen für die Hinterbliebenenrenten-Zusatzversicherung (HZV)* at pp. 53–54, and its § 10 Abs. 15 makes the commutation of a *Rentengarantiezeit* unavailable where an HZV is included

(delib-klassische_rentenversicherung-s11)=

### S11 — Debeka Lebensversicherungsverein a. G., "Allgemeine Bedingungen für eine Rentenversicherung mit aufgeschobener Rentenzahlung und **Fondskomponenten** nach Tarif CA2I" (B LV 85)
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., Koblenz; AVB, house document code **B LV 85 (01.07.2026)**, tariff **CA2I (ABAR-IT 07/2026)**, fifty-nine §§ in six parts
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf
- Retrieved: yes (PDF, 21 pp., B LV 85 (01.07.2026), read 2026-08-30)
- Used for: **the *Rentenfaktor* arithmetic and a guaranteed basis far below the tariff's own**, both from clause text. § 52 Abs. 1: *"Der garantierte Rentenfaktor gibt an, wie viel Rente wir Ihnen monatlich je 10.000 Euro des zum Rentenbeginn zur Verfügung stehenden Fondsguthabens zahlen. Wir legen ihm einen Rechnungszins von 0,1 % p. a. und die unternehmenseigene geschlechtsunabhängige Sterbetafel „Debeka 07/16 R (RF)" zugrunde."* Against § 28 Abs. 2, where the **guaranteed benefits** run on *"einen Rechnungszins von 1 % p. a."* with the tables *Debeka 01/17 TL* in the *Aufschubzeit* and *Debeka 01/21 R* in the payout phase, that is the ***Sicherheitsabschlag* made concrete**: the same carrier guarantees a conversion factor on 0,1 % while pricing the contract on 1,0 %. It also carries: the premium split — costs and risk premium out of the *Beitragsanteil*, the *Sparanteil* forming the *Deckungskapital* (§ 27 Abs. 1) — which is `prem_to_av_pp = prem_pp − charge_from_prem_pp`; and a **duration-tapered percentage *Stornoabzug*** in two parts, 5 % of the *Deckungskapital* for collectively provided risk capital and 0 / 5 / 10 / 15 % keyed to the gap between the ten-year euro zero-coupon swap rate and its own ten-year average, **each falling linearly to 0 % over the last ten years of the *Aufschubzeit*** (§ 34 Abs. 4–5).
- **Correction, and it is a substantial one.** The URL is a living path and the file it now serves is **not the document this entry described**. B LV 85 today is the ***Fondskomponenten*** successor design — the garantiebasierter and fondsgebundener *Baustein* construction of [S12] — reissued **1 July 2026**, which incidentally settles the reissue date the previous entry could only infer from sibling file names. The sentence the entry called *"the cleanest statement of the accumulation recursion in the corpus"* — the *Deckungskapital* as contributions accumulated at the *Rechnungszins* insofar as not needed for risk and expense cover — **is not in the retrieved text**. The recursion is re-sourced to [S8] § 1 Abs. 2, which states it with the rate attached, and to [S1] § 12 Abs. 3 and [R1] for the *Deckungskapital* definition itself. Because B LV 85 is now a hybrid, it is a **variation** in the product spec's sense and no longer evidence for the classic chassis

(delib-klassische_rentenversicherung-s12)=

### S12 — Debeka, "Privatrente" product page
- Publisher / doc type: Debeka; insurer product page
- URL: https://www.debeka.de/privatkunden/vorsorgensparen/zukunftalter/privatrente.html
- Retrieved: yes (HTML, read 2026-08-30)
- Used for: the **split-surplus successor design**, in the carrier's own summary and matching [S11]'s clause text: *"Garantiebasierter Baustein: Aus dem Sparanteil bildet die Debeka ein Deckungskapital für die garantierten Leistungen; Überschussanteile der Ansparphase werden in einen interne Fonds angelegt und können zusätzliche Leistungen ermöglichen."* [S11] § 38 Abs. 1 gives the reason fund holdings receive no *Überschussbeteiligung* from the general *Sicherungsvermögen* before the *Rentenbeginn* — the internal funds are *"gesonderte Abteilungen des Sicherungsvermögens"* and so *"können für den fondsgebundenen Baustein vor dem Rentenbeginn keine Beteiligung an den Bewertungsreserven und keine Zinsüberschussanteile fällig werden"*. The design is recorded in the product spec as a **variation, not the representative design**. Also the annuity side of the tax choice: a lifelong monthly annuity is taxed *"nur ein Teil der Auszahlung (abhängig vom Alter bei Rentenbeginn) mit dem vergleichsweise geringen Ertragsanteil"*, against a lump sum taxed on the gain and halved at twelve years and attained age 62 [R5] [R6].
- **Correction.** The page does **not** contain the carrier's own statement that it no longer offers the classical annuity product; it presents the *Privatrente* as a choice between the two *Bausteine* and says nothing about what was withdrawn. That claim rests on [R22] alone, which has it from a company spokesperson

(delib-klassische_rentenversicherung-s13)=

### S13 — Allianz Lebensversicherungs-AG, "Vorsorgekonzept KomfortDynamik" / PrivatRente KomfortDynamik
- Publisher / doc type: Allianz Lebensversicherungs-AG; insurer product page, plus a distributed *persönlicher Vorschlag* specimen quotation for the BasisRente variant hosted by a broker and dated by its path to **February 2025**
- URL: https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/
- Retrieved: yes (HTML, read 2026-08-30)
- Used for: **the guarantee ladder of the successor design that replaced the classic tariff at the market leader**, now verbatim from the carrier's page: *"Dafür stehen zum Rentenbeginn neben einem Garantieniveau von 80 % der eingezahlten Beiträge auch ein Garantieniveau von 60 % für noch höhere Chancen oder 90 % für noch höhere Sicherheit zur Verfügung."* — 80 % standard, 60 % and 90 % selectable, and the *StartUp* variants at 60 %. That is the product spec's account of what the classic chassis was replaced by.
- **Two corrections.** The **operational definition of the *aktueller Rentenfaktor*** — that the bases at *Rentenbeginn* are those the company then uses for immediately beginning annuities — is **not on this page**. It is re-sourced to [S9] § 1 Abs. 1, which states it in terms and names a comparable immediate-annuity tariff, and to [S14] § 2 Abs. 5; those are also the reason `rentenfaktor_table.csv` is indexed by attained age at *Rentenbeginn* and the reason an immediate-annuity document [S16] belongs in this file. And **neither of the two charge figures is on this page** — the *Abschlussprovision* of 1 575 € and the ceiling of 0,95 € per 100 € of capital formed come from the third-party analyst cluster at [R23], of a Schicht-1/Schicht-2 quotation; they stay `[unverified]` as Schicht-3 levels and remain the reason every charge in the model is `[std]`. The *Rentengarantiezeit* as a policyholder-selectable parameter is [S4] and [S9]

(delib-klassische_rentenversicherung-s14)=

### S14 — Mecklenburgische Versicherungsgruppe, "Vertragsinformationen für die Private Rentenversicherung mit flexiblem **Fondsanteil (Hybrid)**" (B Privat-Rente Flex)
- Publisher / doc type: Mecklenburgische Lebensversicherungs-Aktiengesellschaft, Hannover; *Vertragsinformationen*, **Version 07.2025**, condition set *B Privat-Rente Flex* plus two BU riders, an accident rider, a glossary, tax notes and a *Kostenverzeichnis*
- URL: https://www.mecklenburgische.de/pdfs/produkte/vertragsinformationen/Vertragsinformationen-zu-Leben/rente-flex_vertragsinformationen.pdf
- Retrieved: yes (PDF, 27 pp., Version 07.2025, read 2026-08-30)
- Used for: the product spec's carrier table, as a **mid-sized data point**, and for the finding that *Vertragsinformationen* is a second common name for the same pre-contractual pack [S4]. The truncated title is resolved: the distinguishing feature is a **flexible fund component (Hybrid)**, not a flexible *Rentenbeginn*, so this is a hybrid variation rather than a classic chassis. Clause content now supports two things the model rests on. § 2 Abs. 5: *"Der Rentenfaktor gibt an, wie viel Rente wir Ihnen je 10.000 Euro Gesamtkapital zahlen. Wir ermitteln den Rentenfaktor aus den zum Zeitpunkt des Rentenzahlungsbeginns gültigen Rechnungsgrundlagen"* — and those bases are, expressly, *"diejenigen, mit denen wir neu abgeschlossene, sofort beginnende Rentenversicherungen kalkulieren"*, changing with the carrier's immediate-annuity new business. § 2 Abs. 3 and Abs. 6 give the floor: *"Wenn die so berechnete Rente geringer ist als die garantierte Mindestrente …, zahlen wir die garantierte Mindestrente"* and *"Mindestens legen wir für die Berechnung der Rente den garantierten Rentenfaktor zugrunde"*, the guaranteed factor being fixed at inception on the premiums then agreed. Third carrier for `max(f_g, f_c)`, after [S9] and [S18]

(delib-klassische_rentenversicherung-s15)=

### S15 — Konzern Versicherungskammer, "Überschussverteilung 2026"
- Publisher / doc type: Konzern Versicherungskammer, the Bavarian public-sector insurance group (the `BL_` path prefix indicates the Bayerische Landesbrandversicherung / Bayern-Versicherung life entity); the annual **surplus-declaration document**, the instrument by which a German life insurer publishes its declared *Überschussanteilsätze* for a calendar year
- URL: https://www.konzern-versicherungskammer.de/dam/jcr:acf4c857-3b53-4521-a108-d1fb9b1cec67/BL_Ueberschussbeteiligung_2026.pdf
- Retrieved: yes (PDF, 145 pp., *Überschussverteilung 2026*, publishing entity **Bayern-Versicherung Lebensversicherung AG**, read 2026-08-30)
- Used for: **the declaration document type, and now its content.** The publisher inferred from the `BL_` path prefix is confirmed on every page footer. The document opens with the convention that governs every figure in it — *"Im Kalenderjahr 2025 galten die gleichen Überschussanteilsätze, falls nicht in Klammern andere Werte angegeben wurden"* — so each rate carries its own prior year in brackets. For section **3.1 Rentenversicherung**, *laufender Überschussanteil*, tariff generations 2015 through 2025:

  | | before the *Rentenzahlungsbeginn* | during the *Rentenbezug* |
  |---|---|---|
  | *Zinsüberschussanteil* 2026 | **3 %** less the *Rechnungszins* | **3,35 %** less the *Rechnungszins* |
  | *Zinsüberschussanteil* 2025 | 2,25 % less the *Rechnungszins* | 2,5 % less the *Rechnungszins* |

  Tariff generations 2012–2013 stand at 1,25 % (2025: 0,5 %) and 1,6 % (2025: 0,75 %). Expressing the *Zinsüberschussanteil* as a figure **less the *Rechnungszins*** is the German construction `model.md` calls "the declared rate contains the guarantee": the total interest credited to the *Deckungskapital* is **3,00 % for 2026** and 2,25 % for 2025, whatever guarantee the contract was written on. The declaration also confirms, in a carrier's operative rules rather than a restatement: the *hälftige* allocation — *"Dieser wird gemäß dem ermittelten Verteilungsschlüssel zur Hälfte dem Vertrag zugeteilt"*; the *Zuteilungszeitpunkte* for annuities — *"bei Beginn der Rentenzahlung oder Auszahlung der Kapitalabfindung sowie bei Beendigung des Vertrags vor Beginn der Rentenzahlung durch Tod oder Kündigung"*, and thereafter at each policy year end during the payout phase [R4]; that no *Risiko- oder Verwaltungskostenüberschussanteil* is granted on this line at all; and *"Eine Direktgutschrift wird nicht durchgeführt"*.
- **This closes gap 4.** A declared rate for annuity business, current and carrier-attributed, is now on the record. `decl_rate_table.csv` is **unchanged in this pass** and still ships a `[std]` scenario path with a `base` of 2,55 %; that figure now sits between this carrier's 2025 (2,25 %) and 2026 (3,00 %) declarations rather than beside nothing, and the divergence is stated in `model.md`

(delib-klassische_rentenversicherung-s16)=

### S16 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation … Sofort beginnende Rentenversicherung", **Fassung 01/2025 — Direktversicherung nach § 3 Nr. 63 EStG (Schicht 2)**
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation* for the **immediate** annuity as a *Direktversicherung*. Document code **521331402 2501**
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/222202101_sofort-beginnende-rentenversicherung_verbraucherinformationen_2022_01.pdf
- Retrieved: yes (PDF, 25 pp., document code 521331402 2501, Fassung 01/2025, read 2026-08-30)
- Used for: one structural point, in the product spec and in `model.md`'s account of the *Rentenfaktor* — because the *aktueller Rentenfaktor* of a deferred contract is taken from the carrier's **then-current immediate-annuity tariff** [S9] [S14], the immediate-annuity document is direct evidence for the deferred contract's conversion basis. The retrieval makes that concrete: its § 1 Abs. 6 carries the same sentence as the deferred packs — DAV 2004R (Aggregattafel), *"es wird ein Rechnungszins in Höhe von 1,00 % verwendet"* — so at this carrier, in this vintage, the immediate and the deferred tariff run on the **same** two bases, which is what makes a guaranteed factor struck at inception and a current factor struck at conversion comparable at all. It also marks the boundary with delib's `sofortrente`, whose product this is.
- **Correction.** The Fassung is **01/2025**, not 01/2022, and this edition is a *Direktversicherung* under § 3 Nr. 63 EStG (Schicht 2); the URL slug's `2022_01` is a media-path slot, as at [S5] and [S7]

(delib-klassische_rentenversicherung-s17)=

### S17 — Zurich, "Private Rentenversicherung" product page
- Publisher / doc type: Zurich Gruppe Deutschland; insurer product page
- URL: https://www.zurich.de/de-de/pk/altersvorsorge/private-rentenversicherung
- Retrieved: **no** — the URL answers HTTP 200 on 2026-08-30 with a 212-byte shell containing no page body. The publisher's own site was checked for a current address and none was found that serves this path's content, so the entry is kept as a known reference and nothing is claimed from it
- Used for: the retail presentation of the family whose conditions are [S4]–[S7], in the product spec's market-role section. **No parameter, price point or envelope is established from it**, and the entry now exists mainly to record that a carrier's marketing page is not a source. Everything the product spec says about this family comes from the *Verbraucherinformationen* themselves

(delib-klassische_rentenversicherung-s18)=

### S18 — Stuttgarter Lebensversicherung a. G., "Allgemeine Informationen zu einem Altersversorgungssystem"
- Publisher / doc type: Stuttgarter Lebensversicherung a. G.; general pre-contractual information on a retirement-provision system, organised as one chapter per tariff family. The URL's `?t=1604038997833` parameter is a millisecond timestamp corresponding to **October/November 2020**, and the document's own text — *"gelten für Tarife, die vor 2021 abgeschlossen wurden"* — agrees with it
- URL: https://www.stuttgarter.de/documents/209195/221255/Allgemeine_Infos_Altersversorgungssystem_SLV.pdf/2657ea66-2bfa-9cec-04d2-8f72ac9731bd?t=1604038997833
- Retrieved: yes (PDF, 23 pp., read 2026-08-30)
- Used for: a further carrier in the product spec's variation table, and a second example of the *allgemeine Informationen* document type that opens the German pre-contractual pack [S4]. Two things it adds. It is a ***betriebliche Altersversorgung*** document — chapter 1 is the *"Klassische Rentenversicherung als Direktversicherung nach § 3 Nr. 63 und § 100 EStG"* — so it sits in Schicht 2 and is a boundary marker rather than a Schicht-3 data point. And it states the *Rentenfaktor* in the same per-10 000-EUR terms as [S11], [S14] and [R24], with the scope the classic chassis gives it: *"Für den Teil des Deckungskapitals, der das garantierte Kapital übersteigt, garantieren wir eine monatliche Rente je 10.000 € dieses Teils des Deckungskapitals (garantierte Rentenfaktoren)."* The guaranteed factor is applied to the **excess over the guaranteed capital**, the guaranteed capital carrying its own guaranteed annuity — which is the two-limb structure `capital_conv_pp = max(guar_capital_pp, …)` and `annuity_rate_appl = max(f_g, f_c)` approximate on one grid

(delib-klassische_rentenversicherung-s19)=

### S19 — DEVK, "Kundeninformation zur Fondsgebundenen Rentenversicherung", 03101/07/2024
- Publisher / doc type: DEVK Lebensversicherungsverein a. G.; *Kundeninformation* for a **unit-linked** annuity, document code **03101**, **07/2024**
- URL: https://medien.devk.de/assets/content/download/produkte/altersvorsorge-leben/devk-fondsrente-kundeninfo-03101-2024-07.pdf
- Retrieved: **no** — HTTP 403 at the cited URL on 2026-08-30, and again on a direct retry; `medien.devk.de` refuses the whole asset path. The publisher's own site was checked for a replacement address and the obvious product path answers 404, so the entry is kept as a known reference
- Used for: **the death-benefit contrast, and nothing else** — that on death before the *Rentenbeginn* the unit-linked benefit is the fund value at the date of death but at least the sum of the premiums paid (*Beitragsrückgewähr*). That claim now rests on a search summary and **is not confirmed by a retrieved document**; it is `[unverified]` and marked so wherever it is used. It no longer has to carry the `max(…)` shape on its own, however: [S9] § 1 Abs. 3 states exactly that shape for a **classic** deferred annuity — contract value plus final surplus and *Bewertungsreserven*, *"mindestens jedoch die sogenannte Beitragsrückgewähr"* — and [S14] § 2 Abs. 9 a) states it for a hybrid. So `death_benefit_form = max` is established for this product from primary sources, and gap 18's "classic analogue unestablished" is withdrawn. The DEVK product itself is out of scope; it is delib's `fondsgebundene_rentenversicherung`

---

## Regulatory and actuarial references (product research numbering)

(delib-klassische_rentenversicherung-r1)=

### R1 — VVG § 169, Rückkaufswert
- Publisher / doc type: Bundesministerium der Justiz / juris (Gesetze im Internet); statutory article
- URL: https://www.gesetze-im-internet.de/vvg_2008/__169.html — the human-facing link; the per-section page is a 7 kB frameset with no statutory text, so the article was read from the canonical XML at `gesetze-im-internet.de/vvg_2008/xml.zip`
- Retrieved: yes (canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read 2026-08-30)
- Used for: the surrender machinery of `cv_pp`, now from the article. Abs. 5: *"Der Versicherer ist zu einem Abzug von dem nach Absatz 3 oder 4 berechneten Betrag nur berechtigt, wenn er vereinbart, beziffert und angemessen ist. Die Vereinbarung eines Abzugs für noch nicht getilgte Abschluss- und Vertriebskosten ist unwirksam."* Abs. 6 is the solvency valve — an appropriate reduction where the *dauernde Erfüllbarkeit* is at risk, *"jeweils auf ein Jahr befristet"* — named and not modelled. Abs. 7 adds the already-allotted surplus shares and the AVB's surrender *Schlussüberschussanteil* on top of the computed value, which is why `cv_pp` is a floor on the *Deckungskapital* and not the whole payout.
- **Gap 12 is closed.** The **five-year spreading** the previous entry could only attribute to commentary is in the article, in Abs. 3 Satz 1: *"bei einer Kündigung des Versicherungsverhältnisses jedoch mindestens der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt; die aufsichtsrechtlichen Regelungen über Höchstzillmersätze bleiben unberührt."* The same sentence appears almost word for word in [S1] § 12 Abs. 3, [S4] § 10 Abs. 3, [S8] § 7 Abs. 3, [S9] § 16 Abs. 4 and [S11] § 34 Abs. 2, so `alpha_spread_years = 5` is statutory and carrier-confirmed five times over.
- **On the *Stornoabzug*'s shape.** The previous entry inferred a **flat percentage with no duration term** from Abs. 5's prohibition on charging unamortised acquisition costs. The market wordings do not support the inference: [S8] and [S9] levy **no *Stornoabzug* at all**, [S4] levies **a flat 250 EUR** (waived at attained age 62 or after twenty years), and [S11] levies **percentages of the *Deckungskapital* that taper linearly to nil over the last ten years of the *Aufschubzeit***. A duration term is therefore common and is not what Abs. 5 forbids; what it forbids is basing the deduction on unamortised acquisition cost. The model's flat `surr_charge_pp` is unchanged in this pass and is now a `[std]` simplification of a documented spread rather than a reading of the statute

(delib-klassische_rentenversicherung-r2)=

### R2 — VVG § 165, Prämienfreie Versicherung (Beitragsfreistellung)
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory article
- URL: https://www.gesetze-im-internet.de/vvg_2008/__165.html — the human-facing link; the per-section page is a 4 kB frameset with no statutory text, so the article was read from the canonical XML
- Retrieved: yes (canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read 2026-08-30)
- Used for: **both branches of the *Beitragsfreistellung* the model implements**, now word for word. Abs. 1: *"Der Versicherungsnehmer kann jederzeit für den Schluss der laufenden Versicherungsperiode die Umwandlung der Versicherung in eine prämienfreie Versicherung verlangen, sofern die dafür vereinbarte Mindestversicherungsleistung erreicht wird. Wird diese nicht erreicht, hat der Versicherer den auf die Versicherung entfallenden Rückkaufswert einschließlich der Überschussanteile nach § 169 zu zahlen."* — the right behind `pup_year` and `paid_up(t)`, and the cash-out branch of `pup_cashout()` and model point 8. Abs. 2: *"Die prämienfreie Leistung ist nach anerkannten Regeln der Versicherungsmathematik mit den Rechnungsgrundlagen der Prämienkalkulation unter Zugrundelegung des Rückkaufswertes nach § 169 Abs. 3 bis 5 zu berechnen und im Vertrag für jedes Versicherungsjahr anzugeben."* — which is `pup_value_pp()`, and note the drafting: **Abs. 3 to 5**, so the *Stornoabzug* of Abs. 5 is inside the reference. [S4] § 10 Abs. 9 and [S8] § 7 Abs. 7 both nevertheless waive it on the paid-up route (*"Bei der Beitragsfreistellung wird kein Abzug erhoben"*), which is what the model does; [S1] § 13 Abs. 2 and [S11] leave it in. Abs. 3 keeps the surplus entitlement untouched, which is the reason the paid-up contract stays overschussberechtigt.
- **Gap 22 is partly closed.** The ***Mindestversicherungsleistung*** is contractual, not statutory, and three carrier levels are now on the record: **25,00 EUR a month** at [S4] (footnote 1) and at [S9] (§ 1 Abs. 1), and **600,00 EUR a year** for a partial surrender at [S8] (§ 7 Abs. 2). The model's `min_annuity_mth` of 30,00 € a month stays `[std]` and unchanged in this pass; it now sits just above two observed carrier levels rather than beside none

(delib-klassische_rentenversicherung-r3)=

### R3 — VVG § 163, **Prämien- und Leistungsänderung**
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory article
- URL: https://www.gesetze-im-internet.de/vvg_2008/__163.html — the human-facing link; the per-section page is a 6 kB frameset with no statutory text, so the article was read from the canonical XML
- Retrieved: yes (canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read 2026-08-30)
- Used for: § 163 as the statutory adjustment channel a guaranteed *Rentenfaktor* would have to pass through. **Gap 6 is closed** and the entry's own heading corrected: the article is titled ***Prämien- und Leistungsänderung***, not "Anpassung der Prämie / Bedingungsanpassung", and it has four *Absätze*. Abs. 1 lets the insurer **re-set the premium** on three cumulative conditions — a change in the *Leistungsbedarf* that is *"nicht nur vorübergehend und nicht voraussehbar"* against the bases of the agreed premium; a new premium that is *"angemessen und erforderlich …, um die dauernde Erfüllbarkeit der Versicherungsleistung zu gewährleisten"*; and confirmation by *"ein unabhängiger Treuhänder"* — with re-setting excluded where the original calculation was inadequate and a careful actuary should have seen it. Abs. 2 is the limb that reaches benefits: the policyholder may demand a **benefit reduction instead of** a premium increase, and *"bei einer prämienfreien Versicherung ist der Versicherer unter den Voraussetzungen des Absatzes 1 zur Herabsetzung der Versicherungsleistung berechtigt"*. Abs. 3 fixes the effective date at the start of the second month after notice with reasons; Abs. 4 drops the trustee where supervisory approval is required.
- **Two refinements this forces.** First, the previous entry described § 163 as *having replaced* the contractual *Treuhänderklausel* route; the article shows the trustee is **inside** the statutory route (Abs. 1 Nr. 3), so what changed is the source of the power, not the presence of a trustee. Second, on a premium-paying contract § 163 gives the insurer no unilateral power to cut a guaranteed benefit — Abs. 2 Satz 1 puts that election with the policyholder, and Abs. 2 Satz 2's unilateral limb is confined to premium-free contracts. The two triggers the clause family cites — a stronger-than-assumed rise in life expectancy and a sustained fall in investment returns — are the *Leistungsbedarf* limb of Abs. 1 Nr. 1, and [R17] supplies a specimen contractual clause naming both. The modelling consequence is unchanged: the guaranteed factor is **fixed for the life of the contract** and § 163 is recorded as a model risk rather than implemented

(delib-klassische_rentenversicherung-r4)=

### R4 — VVG § 153, Überschussbeteiligung, and § 153 Abs. 3, Beteiligung an den Bewertungsreserven
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory article
- URL: https://www.gesetze-im-internet.de/vvg_2008/__153.html — the human-facing link; the per-section page is a 5 kB frameset with no statutory text, so the article was read from the canonical XML
- Retrieved: yes (canonical XML, **Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156**, read 2026-08-30)
- Used for: the whole of § 153, which the previous entry could reach only through an insurer's restatement. Abs. 1 gives the entitlement and its **all-or-nothing opt-out** — *"es sei denn, die Überschussbeteiligung ist durch ausdrückliche Vereinbarung ausgeschlossen; die Überschussbeteiligung kann nur insgesamt ausgeschlossen werden"*. Abs. 2 requires the ***verursachungsorientiertes Verfahren***. Abs. 3 Satz 2 is the ***hälftige* participation** `val_reserve_pp` stands for: *"Bei der Beendigung des Vertrags wird der für diesen Zeitpunkt zu ermittelnde Betrag zur Hälfte zugeteilt und an den Versicherungsnehmer ausgezahlt; eine frühere Zuteilung kann vereinbart werden."* Abs. 3 Satz 3 is the *Sicherungsbedarf* reservation, by cross-reference to §§ 89, 124 Abs. 1, 139 Abs. 3 und 4, 140 und 214 VAG.
- **The decisive new sentence is Abs. 4**: *"Bei Rentenversicherungen ist die Beendigung der Ansparphase der nach Absatz 3 Satz 2 maßgebliche Zeitpunkt."* The crystallisation of the *Bewertungsreserven* at the *Rentenbeginn* — which the model implements and the library previously supported with a carrier's paraphrase — is **a statutory rule specific to annuities**, and that is why the model crystallises there and nowhere else. [S4] § 3 Abs. 2 and [S15] apply it in the same terms, [S15] listing the annuity *Zuteilungszeitpunkte* as the start of annuity payment or the commutation, and termination before it by death or surrender.
- Continued participation **during the payout phase** is *not* in § 153; it is the carriers' own promise, at [S4] (*"Darüber hinaus beteiligen wir Sie während der Rentenzahlungszeit … an den Bewertungsreserven"*), at [S9] § 2 Abs. 5 c) and at [S15], and it remains cited and deliberately not implemented

(delib-klassische_rentenversicherung-r5)=

### R5 — EStG § 22, Ertragsanteilsbesteuerung der Leibrente
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory article
- URL: https://www.gesetze-im-internet.de/estg/__22.html — the human-facing link; the article was read from the canonical XML at `gesetze-im-internet.de/estg/xml.zip`
- Retrieved: yes (canonical XML, **Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197**, read 2026-08-30)
- Used for: the taxation half of the *Kapitalwahlrecht* comparison the product spec sets out and the model deliberately does not compute.
- **Gap 8 is closed, and so is the address.** The provision is **§ 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb EStG** — the residual limb for annuities that are *not* Schicht-1, *"bei denen in den einzelnen Bezügen Einkünfte aus Erträgen des Rentenrechts enthalten sind"* — and [S4]'s *Allgemeine Steuerhinweise* cite it in exactly that form. Satz 3 of that limb defines the *Ertrag des Rentenrechts* as the excess of the annual annuity over the level spreading of its capital value across its expected term; Satz 4 supplies the table, read off by the **age completed at the start of the annuity**, and the whole of it is now on the record. Its shape, at the ages this product reaches: 22 % at 60–61, 21 % at 62, 20 % at 63, 19 % at 64, **18 % at 65–66**, 17 % at 67, 16 % at 68, 15 % at 69–70, 14 % at 71 — falling to 1 % from age 97. The 18 % the previous entry had from a search summary is confirmed and is the value at **65 or 66**, not at 65 alone.
- Two boundaries the same article fixes, and the spec uses: the Schicht-1 limb (Doppelbuchst. aa) is a different table keyed to the **year** of *Rentenbeginn*, not the age — 84,0 % for a 2026 start, rising to 100,0 % in 2058 — which is what separates this product from delib's `basisrente`; and Satz 9 of that limb, applied by Doppelbuchst. bb Satz 6, attributes the annuity of the month of death to the deceased

(delib-klassische_rentenversicherung-r6)=

### R6 — EStG § 20 Abs. 1 Nr. 6, taxation of a Kapitalabfindung (the 12/62 rule and the Halbeinkünfteverfahren)
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory article, reached through tax commentary rather than a statute mirror
- URL: https://www.gesetze-im-internet.de/estg/__20.html — the human-facing link; the article was read from the canonical XML
- Retrieved: yes (canonical XML, **Stand: zuletzt geändert durch Art. 7 G v. 29.6.2026 I Nr. 197**, read 2026-08-30, together with § 52 Abs. 28 for the transitional rules)
- Used for: the other half of that comparison. Abs. 1 Nr. 6 Satz 1 taxes *"der Unterschiedsbetrag zwischen der Versicherungsleistung und der Summe der auf sie entrichteten Beiträge (Erträge) im Erlebensfall oder bei Rückkauf des Vertrags bei Rentenversicherungen mit Kapitalwahlrecht, **soweit nicht die lebenslange Rentenzahlung gewählt und erbracht wird**"*, for contracts concluded after 31 December 2004 — so the charge falls on the commutation and the surrender and **not** on the annuity, which is the fork the product spec describes and `kapitalwahl_rate` parameterises.
- **A correction to the rule's name.** Satz 2 as enacted reads *"Wird die Versicherungsleistung nach Vollendung des **60.** Lebensjahres des Steuerpflichtigen und nach Ablauf von zwölf Jahren seit dem Vertragsabschluss ausgezahlt, ist die Hälfte des Unterschiedsbetrags anzusetzen."* The **62** of the "12/62 rule" is not in § 20 at all: it comes from **§ 52 Abs. 28 Satz 7 EStG** — *"§ 20 Absatz 1 Nummer 6 Satz 2 ist für Vertragsabschlüsse nach dem 31. Dezember 2011 mit der Maßgabe anzuwenden, dass die Versicherungsleistung nach Vollendung des 62. Lebensjahres des Steuerpflichtigen ausgezahlt wird."* So the rule is 12/60 for a 2005–2011 contract and 12/62 for one written after that, and the correct citation is § 20 Abs. 1 Nr. 6 Satz 2 **read with** § 52 Abs. 28 Satz 7. [S4]'s tax notes give 62, consistent with a current contract.
- The **pre-2005 cohort rule** is confirmed at § 52 Abs. 28 Satz 5: for contracts concluded before 1 January 2005, § 20 Abs. 1 Nr. 6 *"in der am 31. Dezember 2004 geltenden Fassung"* continues to apply, *"auch in allen offenen Fällen"*, with annuity payments from those contracts falling under § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb. The predecessor regime's own conditions are still `[unverified]` — the retrieved text incorporates them by reference to a repealed version rather than reproducing them — and nothing in delib asserts them. The **duration-12 step in `lapse_table.csv`** keeps its argued shape and its `[std]` levels

(delib-klassische_rentenversicherung-r7)=

### R7 — Deckungsrückstellungsverordnung (DeckRV), § 2 — Höchstrechnungszins
- Publisher / doc type: Bundesministerium der Justiz / juris (instrument); Bundesministerium der Finanzen (amendment)
- URL: https://www.gesetze-im-internet.de/deckrv_2016/__2.html — **now established.** The per-section page is a frameset, so the article was read from the canonical XML at `gesetze-im-internet.de/deckrv_2016/xml.zip`
- Retrieved: yes (canonical XML, **Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250**, read 2026-08-30)
- Used for: the *Höchstzinssatz* itself and the vintage rule, both now from the instrument rather than from press coverage. § 2 Abs. 1 Satz 1: *"Bei Versicherungsverträgen mit Zinsgarantie, die auf Euro oder die nationale Währungseinheit eines an der Europäischen Wirtschafts- und Währungsunion teilnehmenden Mitgliedstaates lauten, wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf 1 Prozent festgesetzt."* The amending *Stand* — Art. 1 V v. 19.7.2024 — is the *Bundesgesetzblatt* instrument [R11] dates to 24 July, and the 1 Prozent is the rate [R8] recommends for 2026 and [S4] applies in its Fassung 01/2026.
- **The decisive point for the model is § 2 Abs. 2 Satz 1**, and it is stronger than the press restatement the entry previously rested on: *"Bei Versicherungsverträgen mit Zinsgarantie gilt der von einem Versicherungsunternehmen zum Zeitpunkt des Vertragsabschlusses verwendete Rechnungszins für die Berechnung der Deckungsrückstellung für die gesamte Laufzeit des Vertrages."* The rate is not merely *permitted* to persist; it is **fixed for the whole term by the ordinance**. That is why `int_rate_guar` is a model-point attribute and points 1, 6 and 14 credit three different rates in one run, and [S5] (1,25 %, Fassung 07/2015) beside [S4] (1,00 %, Fassung 01/2026) is the same rule seen in one carrier's paper.
- The same ordinance carries the *Höchstzillmersatz* the charge table uses: **§ 4 Abs. 1 Satz 2, *"Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten"***, with § 4 Abs. 4 fixing the inception Zillmersatz for the whole term as Abs. 2 does the interest rate [REG-R16]. [S1] § 14 Abs. 2, [S4] § 11 Abs. 2, [S8] § 8 Abs. 2 and [S9] § 16 Abs. 3 all restate it as *"2,5 % der … zu zahlenden Beiträge"*.
- **The full rate history is still not established** (gap 7) — the ordinance states only the rate now in force, and the 0,25 % it replaced is read from [R11] and [R8]. A legacy vintage cites the cross-product library instead

(delib-klassische_rentenversicherung-r8)=

### R8 — DAV, "Deutsche Aktuarvereinigung empfiehlt auch für 2026 einen Höchstrechnungszins in Höhe von 1,0 Prozent"
- Publisher / doc type: Deutsche Aktuarvereinigung e. V. (DAV), Köln; association news release
- URL: https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-empfiehlt-auch-fuer-2026-einen-hoechstrechnungszins-in-hoehe-von-1-prozent/
- Retrieved: yes (HTML, read 2026-08-30)
- Used for: the rate applicable to new business **at this file's access date — 1,0 %** — on the profession's own recommendation, which is the `int_rate_guar` of the eleven 2026-issue model points. The release states it directly: *"Die DAV empfiehlt daher auch für das Jahr 2026 einen Höchstrechnungszins für die handelsrechtliche Deckungsrückstellung von Lebensversicherungsverträgen mit Zinsgarantie (kurz HRZ) in Höhe von 1,0 Prozent."* It also states the recommendation mechanism — the BMF set 1,0 % from January 2025 on the DAV's prior-year recommendation [R9] — and, usefully for the vintage stack, that the 2025 increase was *"der erste Anstieg seit über dreißig Jahren"*. One caveat the release makes explicitly and the product spec should keep: the *Höchstrechnungszins* *"gibt … eine Obergrenze. Er sollte als gesetzlicher Höchstwert dienen, ist aber keine Empfehlung für eine Festlegung durch die Unternehmen"* — which is why a carrier may and does price below it [S11] [R22]

(delib-klassische_rentenversicherung-r9)=

### R9 — DAV, "Deutsche Aktuarvereinigung begrüßt Ministeriumsvorstoß zum Höchstrechnungszins 2025"
- Publisher / doc type: DAV; association news release
- URL: https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-begruesst-ministeriumsvorstoss-zum-hoechstrechnungszins-2025/
- Retrieved: yes (HTML, read 2026-08-30)
- Used for: the process and its timing, confirmed in the release's opening sentence — *"Die Deutsche Aktuarvereinigung e.V. (DAV) hat Ende November 2023 eine Empfehlung für eine Anpassung des Höchstrechnungszinses in der Lebensversicherung auf 1,0 % ab 2025 gegeben. Das Bundesministerium der Finanzen (BMF) hat nun angekündigt, dieser Empfehlung zu folgen."* With the ordinance's own date of 19 July 2024 [R7] the lead time from recommendation to legislation is about eight months and to effect about fourteen, which is the product spec's point that a tariff's *Rechnungszins* is a **known-in-advance** pricing parameter. The release also names the reasoning the model's guarantee margin reflects: *"Ein nach wie vor mit Sicherheitsabschlag kalkulierter Höchstrechnungszins von 1,0 % ergibt daher Sinn."* The **late-April 2024** dating of the BMF adoption is not in the release, which says only *"nun angekündigt"*; it stays `[unverified]`

(delib-klassische_rentenversicherung-r10)=

### R10 — GDV, media information on the Höchstrechnungszins increase (two releases)
- Publisher / doc type: GDV; two *Medieninformationen*, ids 176848 and 157548 — the lower being the earlier, pre-legislation release
- URL: https://www.gdv.de/gdv/medien/medieninformationen/hoechstrechnungszins-erhoehung-ist-eine-angemessene-reaktion-auf-gestiegene-zinsen--176848 and https://www.gdv.de/gdv/medien/medieninformationen/versicherer-befuerworten-anhebung-des-hoechstrechnungszinses--157548
- Retrieved: yes (both, HTML, read 2026-08-30)
- Used for: industry corroboration of [R7] on the increase and its rationale, in the product spec's regulatory-context section — release 157548 on the DAV recommendation, release 176848 on the BMF's decision, both quoting GDV-Hauptgeschäftsführer Jörg Asmussen calling the rise *"eine angemessene Reaktion auf das seit 2021 stark gestiegene Zinsniveau"*. Two things beyond the 1,0 % are now established, and one of them is a **correction**:
  - **The *Höchstrechnungszins* is not the *Garantiezins*.** Both releases carry the same standing note: *"Der Höchstrechnungszins ist eine Obergrenze für den maximal zulässigen Rechnungszins, den Lebensversicherer bei der Berechnung ihrer Rückstellungen nutzen dürfen. Er ist nicht mit dem Garantiezins gleichzusetzen, den Lebensversicherer individuell auf ihre Produkte gewähren."* The library's earlier gloss — the *Höchstrechnungszins* "also commonly called the *Garantiezins*" — is withdrawn wherever it appeared. The distinction is exactly what [S11] shows in a contract: a tariff *Rechnungszins* of 1 % beside a *Rentenfaktor* basis of 0,1 %, both under one cap.
  - **The margin the profession priced against**: release 176848 gives the reference rate — the ten-year euro zero-coupon swap, *"Ende März 2024 betrug er 2,57 Prozent"*, against a then-current cap of 0,25 % — so the *Sicherheitsabschlag* [R9] speaks of was more than two percentage points wide at the moment of the increase. The same swap rate is what [S11] § 34 Abs. 4 keys its capital-market *Stornoabzug* to

(delib-klassische_rentenversicherung-r11)=

### R11 — HDI, "Höchstrechnungszins in der Lebensversicherung steigt zum 01.01.2025"
- Publisher / doc type: HDI Lebensversicherung AG; insurer press/blog item
- URL: https://pm.hdi.de/blog/h%C3%B6chstrechnungszins-in-der-lebensversicherung-steigt-zum-01.01.2025
- Retrieved: yes (HTML, read 2026-08-30)
- Used for: an **insurer's own** statement of the change, verbatim: *"Zum 01.01.2025 wird der Höchstrechnungszins gem. Deckungsrückstellungsverordnung von 0,25 % auf 1,00 % angehoben; die Änderung wurde am 24. Juli im Bundesgesetzblatt verkündet."* The 24 July announcement agrees with the ordinance's own *Stand* line — Art. 1 V v. 19.7.2024 [R7]. Third independent corroboration, and the one that names the instrument. It is also the source for the **shape of the decline** the vintage stack sits on: *"Nachdem der Höchstrechnungszins seit 1994 von vier Prozent kontinuierlich auf 0,25 Prozent in 2022 abgeschmolzen wurde …"* — 4 % in 1994 down to 0,25 % in 2022. That is the endpoints only; the intermediate steps are still unestablished (gap 7) and the model's 2,75 % and 0,90 % legacy vintages cite the cross-product library

(delib-klassische_rentenversicherung-r12)=

### R12 — DAV, "Herleitung der DAV-Sterbetafel 2004 R für Rentenversicherungen" (DAV-Richtlinie)
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; **Fachgrundsatz der DAV, Richtlinie**, titled on its cover as the derivation of the DAV-Sterbetafel 2004 R for annuity insurance, **Köln, 28. Juni 2023** (the title is reported, not transcribed — see the retrieval note on the extraction defect)
- URL: https://aktuar.de/content/PDF/Fachwissen/2023-06-28_DAV-Richtlinie_Herleitung_DAV2004R.pdf
- Retrieved: **partially** — PDF, 134 pp., cover, preamble and full table of contents read 2026-08-30, but the sweep capped the transfer at 3 MB and the extractor's character mapping is defective on this file (doubled consonants and some zeros are dropped, so "2004" renders "204"). **Nothing is quoted from it**, and only structure and headings are relied on
- Used for: **what a replacement mortality table must preserve**, which is the whole content of the `mort_table.csv` proxy note. The retrieved table of contents settles the component structure the proxy imitates: *Periodentafeln und Generationentafeln* (§ 1.2), *Basistafeln* (§ 1.3), *Sterblichkeitstrend* (§ 1.4) and *Altersverschiebung als Näherungsverfahren* (§ 1.5), with §§ 4.1–4.2 separating the trend of second order, its linear damping, and the safety loadings that turn it into the first-order basis. That **first-order probabilities carry safety margins over the second-order ("realistic") probabilities** is the subject of § 4.2, which is why `mort_be_factor` is **above one** for an annuity and why the model runs two bases. The date on the cover — 28 June 2023 — confirms that DAV 2004 R was still the profession's maintained annuity basis nineteen years after its base year, the fact behind the longevity trigger of § 163 VVG [R3]; [S4]'s Fassung 01/2026 shows it still in a tariff

(delib-klassische_rentenversicherung-r13)=

### R13 — DAV, "DAV 2004 R: Stand 22.02.2005"
- Publisher / doc type: DAV; the 2005 derivation document, header line "DAV 2004 R: Stand 22.02.2005", authored by the *DAV-Unterarbeitsgruppe Rentnersterblichkeit*; the file name carries 2005-09-14
- URL: https://aktuar.de/content/PDF/Fachwissen/2005-09-14-DAV_2004_R.pdf
- Retrieved: **partially** — PDF, 134 pp., header, contents and §§ 1.2 and 4.2 read 2026-08-30, under the same 3 MB cap and the same defective character mapping as [R12]. **Nothing is quoted from it**; the sentences below are reported, not transcribed. The two URLs serve **distinct** documents, the 2005 derivation here and the 2023 *Richtlinie* at [R12]
- Used for: that **DAV 2004 R is a *Generationentafel*** — § 1.2 rejects period tables for annuity pricing because they do not carry the improvement trend, and says generation tables give mortality per birth cohort **including the expected future change**, so the improvement is built into the table rather than applied on top of it. That is the reason `mort_rate_guar(t)` depends on `calendar_year(t)` as well as `age(t)`, and the tenth listed modeling pitfall. § 1.5 and § 4.3 describe the *Altersverschiebung* approximation that collapses the two-dimensional surface onto one base table, which is the construction the proxy deliberately does **not** use. § 4.2 quantifies the first-order margins the proxy imitates only in level — a model-risk loading equivalent to dropping the trend damping, and an additive safety margin on the annual improvements calibrated to raise the *Deckungsrückstellung* by about 2 % on the working portfolio. It was **intended for new business from 2005**, which is the proxy's `mort_base_year`. The numeric content is **not** here and is not shipped: the DAV tables are the property of the Deutsche Aktuarvereinigung, are not public, and delib cites them by name and ships an anchored `[std]` proxy instead

(delib-klassische_rentenversicherung-r14)=

### R14 — Contemporaneous expositions of DAV 2004 R (DGVFM, Gen Re, qx-Club)
- Publisher / doc type: Deutsche Gesellschaft für Versicherungs- und Finanzmathematik in *Blätter der DGVFM* (Springer); General Reinsurance, presented to the Aktuarvereinigung Österreichs on 27 October 2004; qx-Club Berlin, 16 August 2004; qx-Club (Helmert), September 2004
- URL: https://link.springer.com/article/10.1007/BF02808312 , https://www.avoe.at/archiv/nachlese-20041027.pdf , http://www.qx-club-berlin.de/material/pdf/20040816-qx-Club-Sterbetafel-DAV2004R.pdf , https://www.qx-club.de/.cm4all/uproc.php/0/Vortr%C3%A4ge/vortrag_helmert_14092004.pdf?_=173ca294dfb&cdp=a
- Retrieved: **two of four.** The Gen Re / AVÖ deck is retrieved (PDF, 93 slides, *"Die neue deutsche Rentensterbetafel DAV 2004 R"*, Esther U. Schütz, Wien, 27. Oktober 2004) and the Helmert deck is retrieved (PDF, 41 slides, titled for **DAV 2004 R and R-Bx** and their implementation for new business and the in-force book, qx-Club **Köln**, September 2004). The Springer article answers 200 with a 3 kB bot-challenge page and no abstract, and the qx-Club Berlin PDF fails TLS host verification; both are kept as known references and nothing is claimed from them
- Used for: the **dating and the scale of the market's adoption** of DAV 2004 R, in the product spec's *Rechnungsgrundlagen* section. The Gen Re deck records that the predecessor DAV 1994 R was being reviewed regularly, that the new table was built on the pooled Munich Re and Gen Re insured-lives data, that it was adopted as a DAV *Fachgrundsatz* by an accelerated procedure so as to bite on the 2004 balance sheet with the regular consultation running to mid-November 2004, and that the industry-wide reserve strengthening for the 2004 financial year was **about 4 bn euro** — the concrete measure of what a table change costs, which is why the model runs a two-basis discipline at all. The **companion in-force table** is confirmed and correctly named: **R-Bx**, on the Helmert deck's own title, presented for *Neugeschäft und Bestand* together with the transition method
- **Two corrections:** the Helmert presentation was given to the qx-Club **Köln**, not Berlin (the Berlin item is the separate August 2004 talk), and the in-force table is written **R-Bx**, not RBx

(delib-klassische_rentenversicherung-r15)=

### R15 — Wikipedia (German), "Sterbetafel"
- Publisher / doc type: Wikimedia Foundation; general-encyclopaedia article — **secondary**, not a professional or statutory source
- URL: https://de.wikipedia.org/wiki/Sterbetafel
- Retrieved: yes (HTML, read 2026-08-30)
- Used for: corroboration only, of the generational characterisation of DAV 2004 R [R13]: *"Unter einer Generationensterbetafel versteht man eine Sterbetafel, bei der die Sterblichkeit nicht nur vom Alter (und eventuell vom Geschlecht), sondern zusätzlich vom Geburtsjahrgang abhängt. … Generationentafeln liegen daher der Kalkulation von Rentenversicherungen zugrunde."* It also states the *Altersverschiebung* collapse to one dimension that [R13] § 1.5 describes, and distinguishes a *Kohortensterbetafel* — observed cohort extinction, unusable for pricing because of the observation span — from a *Generationensterbetafel*, which is the projected object. **Nothing in these documents rests on it alone**; it is a secondary encyclopaedia article and is cited as one

(delib-klassische_rentenversicherung-r16)=

### R16 — Finanztip, "Urteil zum Rentenfaktor: Rentenkürzung verhindern"
- Publisher / doc type: Finanztip Verbraucherinformation gemeinnützige GmbH; consumer-organisation article — secondary
- URL: https://www.finanztip.de/private-rentenversicherung/rentenfaktor/
- Retrieved: yes (HTML, read 2026-08-30)
- Used for: the *Treuhänderklausel* narrative in the product spec, and it now supplies the two decisions the library previously had only as a headline (gap 10 closed jointly with [R17]): *"Die Absenkung des Rentenfaktors in Verträgen der Allianz ist nach einem Urteil des Bundesgerichtshof nicht rechtens (BGH, 10.12.2025, Az. IV ZR 34/25). Gegen die Zurich Versicherung gab es ebenfalls bereits eine Entscheidung (LG Köln, 08.02.2023, Az. 26 O 12/22)."* The BGH decision — on a unit-linked Riester contract, where the clause the insurer relied on was held ineffective — post-dates the library's drafting research and is **new to this entry**. It is the strongest support the corpus has for the model's treatment of the guaranteed factor as **fixed** rather than adjustable, and it makes the § 163 route [R3] rather than a contractual clause the only live channel. The article is a consumer-organisation piece and is cited as secondary; the two case references are checkable and are given as it gives them

(delib-klassische_rentenversicherung-r17)=

### R17 — versicherungenmitkopf.de, pages on the Treuhänderklausel, the Rentenfaktor, the Rentengarantiezeit and the Ertragsanteil
- Publisher / doc type: versicherungenmitkopf.de, an independent broker's consumer pages — secondary, and the densest such account in the corpus
- URL: https://www.versicherungenmitkopf.de/treuhaenderklausel-rentenversicherung , /rentenversicherung/rentenfaktor , /rente/rentengarantiezeit-rentenversicherung-riester-und-co , /ertragsanteilsbesteuerung , /rentenversicherung/besteuerung-private-rentenversicherung-wie-viel-bleibt-uebrig
- Retrieved: yes for the *Treuhänderklausel* page (HTML, read 2026-08-30); the four sibling paths were not re-swept and nothing new is drawn from them
- Used for: the ***Treuhänderklausel* story**, now with its authority attached. **Gap 10 is closed**: the holding is *"das Landgericht Köln [hat] aber bereits im Februar 2023 geurteilt, dass schwankende Zinsen zum unternehmerischen Risiko des Versicherers gehören. Sie dürfen nicht im Rahmen der Treuhänderklausel auf Versicherte abgewälzt werden (Az. 26 O 12/22)"* — dated 08.02.2023 by [R16]. The page also supplies a **specimen clause**, attributed to Allianz *"Allgemeine Versicherungsbedingungen für den Baustein zur fondsgebundenen Altersvorsorge: FondsRente ('RiesterRente mit Fonds') – E 202 von Juni 2006"*, which names the two triggers in the form the library reports them — an unforeseeable, sustained rise in life expectancy or fall in investment return, with the remedy being to reduce *"die monatliche Rente für je 10.000 € Policenwert"*. That is the *Rentenfaktor* arithmetic again, in a clause rather than a glossary. And it sets out the three conditions the statute imposes on any use of such a clause, which match § 163 Abs. 1 Nr. 1–3 VVG [R3] point for point — so the entry's earlier framing, that the clause route was *replaced* by § 163, is refined: the contractual clause is the vehicle and § 163 supplies the conditions. Jointly with [R24] it remains the source for the *Rentengarantiezeit* material — that inside the guaranteed period the instalment is due whether the annuitant lives or not, which is `pols_annuity(t)` and the fourth listed pitfall — although [S1] § 1 Abs. 4 and [S9] § 1 Abs. 5 now state that at primary level

(delib-klassische_rentenversicherung-r18)=

### R18 — Versicherungswirtschaft-heute, "Treuhänderklausel: Allianz glaubt nicht, dass Kunden einer Anpassung des Rentenfaktors erfolgreich widersprechen können" (4 February 2021)
- Publisher / doc type: Versicherungswirtschaft-heute; trade press, dated 4 February 2021 by its own URL path
- URL: https://versicherungswirtschaft-heute.de/unternehmen-und-management/2021-02-04/treuhaenderklausel-allianz-glaubt-nicht-dass-kunden-einer-anpassung-des-rentenfaktors-erfolgreich-widersprechen-koennen/
- Retrieved: yes (HTML, dated 4. Februar 2021 on the page itself, read 2026-08-30)
- Used for: the product spec's point that the *Treuhänderklausel* question was a **live commercial dispute at the market leader in 2021** — not a historical curiosity but a mechanic carriers were actively defending inside the window in which the current in-force book was written. The body, previously unestablished, gives the scale and the history: *"Die Allianz kürzt unter Nutzung der Treuhänderklausel die Rentenfaktoren in bestehenden Verträgen. Betroffen sind rund 750.000 Versicherte … Schon in den Jahren 2005 und 2017 hatte die Allianz von der Treuhänderklausel Gebrauch gemacht."* Three exercises of the clause at one carrier — 2005, 2017 and 2021 — over roughly 750 000 contracts is the reason the model records § 163 as a **named model risk** rather than a remote one, and the BGH decision of 10 December 2025 [R16] is how that dispute ended

(delib-klassische_rentenversicherung-r19)=

### R19 — Franke und Bornberg, "Was bedeutet der Rentenfaktor und wie hoch ist er?" and "Altersvorsorge: Überschüsse im Rentenbezug Teil 1 — Die Qual der Wahl"
- Publisher / doc type: Franke und Bornberg GmbH, an independent product-rating house; two analyst articles, the first dated 2021/2022 by its slug
- URL: https://www.franke-bornberg.de/de/blog/was-bedeutet-rentenfaktor-wie-hoch-2021-2022 and https://www.franke-bornberg.de/blog/altersvorsorge-ueberschuesse-im-rentenbezug-teil-1-die-qual-der-wahl
- Retrieved: **the first, yes** (HTML, read 2026-08-30). The second answers **HTTP 404**, on the cited path and on the `/de/blog/…` form the live site uses; no replacement was found on the publisher's own site, so it is kept as a known reference and the surplus-system material is re-sourced to [R20], [S4] § 3 Abs. 7 and [S9] § 2 Abs. 5 c)
- Used for: the analyst treatment of the *Rentenfaktor*, which turns out to be considerably richer than the previous entry could see. It sets out the three-way distinction the product spec uses — the **aktueller** factor, computed on today's bases and not guaranteed; the **garantierter** factor, computed at inception with a *Sicherheitsabschlag*; and the **hart garantierter** factor, where the carrier waives the adjustment clause — and it notes the transparency problem the model's `[std]` factors stand in for, that not every company discloses a current factor at all.
- **Gap 3 is contradicted, not confirmed.** The article that asks *"wie hoch ist er?"* answers it. Franke und Bornberg's own analysis compares the **aktueller Rentenfaktor** across carriers for 2021 and 2022: the average fell from **29,09 €** to **25,97 €**, a drop of 3,12 € or 10,73 %; the highest was Condor Lebensversicherung at **26,61 €** (2021: 29,83 €) and the lowest Bayerische / Pangaea Life at **20,43 €**. Read with [R24]'s fragfina table for 2025, the corpus now carries a market range for both the current and the guaranteed factor. **`rentenfaktor_table.csv` is unchanged in this pass** — its anchors are 32,00 / 25,50 / 35,00 at age 67 — and its `base` of 32,00 now sits **above** every observed market average; the divergence is stated in `model.md` and is a decision for a later pass, not this one

(delib-klassische_rentenversicherung-r20)=

### R20 — Finanztip, "Überschussbeteiligung Lebensversicherung: Arten & Höhe" and "Steuer auf Lebensversicherung"
- Publisher / doc type: Finanztip Verbraucherinformation gemeinnützige GmbH; two consumer-organisation articles — secondary
- URL: https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/ and https://www.finanztip.de/lebensversicherung-versteuern/
- Retrieved: yes (both, HTML, read 2026-08-30)
- Used for: the **three payout-phase surplus systems and their directions**, which the article names as *konstant*, *teildynamisch* and *volldynamisch* and describes in the terms `payout_system` implements. The finding the product spec leans on is stated outright and is worth having exactly: **under the constant system the annuity can still fall** — *"In der Praxis kann Deine Rente aber durchaus schwanken. Denn wenn der Anbieter weniger verdient als erwartet, sinkt Deine Rente. Die Summe, die anfänglich festgelegt wird, ist nicht garantiert. Daher ist der Begriff „konstante Rente" etwas irreführend."* That is why the product spec says only the *garantierte Rente* inside the constant annuity is guaranteed, and [S4] § 3 Abs. 7 says the same thing in a contract: for the RfB-financed part *"wird die Rentenhöhe jeweils nur für ein Versicherungsjahr zugesagt"*. The teildynamisch description — a slowly rising, guaranteed part beside a level part financed out of projected future surplus — is the two-limb shape `sur_ann_theta` splits. Also corroboration of the 12/62 rule [R6]. **No level, rate or split is established for any of the three systems**, so `sur_ann_rate`, `sur_ann_growth` and `sur_ann_theta` remain `[std]`

(delib-klassische_rentenversicherung-r21)=

### R21 — GDV / dieversicherer.de, "Private Rentenversicherung: Auszahlmöglichkeiten"
- Publisher / doc type: GDV under its consumer brand *Die Versicherer*; industry-association consumer article
- URL: https://www.dieversicherer.de/versicherer/altersvorsorge/news/auszahlung-private-rentenversicherung-141750
- Retrieved: yes (HTML, read 2026-08-30)
- Used for: the industry association's own account of the **payout options**, which on retrieval turns out to be about the choice **between annuity models** — *"Dynamisch, teildynamisch oder flexibel? Steht die private Rentenversicherung vor der Auszahlung, haben Versicherte oft die Wahl zwischen verschiedenen Rentenmodellen"* — rather than about the *Kapitalwahlrecht*. It is therefore corroboration for the three payout-phase surplus systems, alongside [R19] [R20] [R24], and it supplies the third common name for the constant model, *flexibel*, which is also what [S8] § 2 calls it (*"Zusatzrente (flexible Rente)"*). The *Kapitalwahlrecht* material the entry previously carried is re-sourced to [S1] § 1 Abs. 2, [S4] § 2 and [S8] § 1 Abs. 2, which are contracts rather than commentary.
- **Gap 11 is closed, elsewhere.** The **notice period for exercising the *Kapitalwahlrecht*** is not in this article, but three carriers now state one: [S4] § 2 Abs. 2–3 requires the application *"wenigstens drei Jahre vor Rentenzahlungsbeginn"* where the payout phase carries no death cover, and otherwise not before the twelfth policy year or, at a twelve-year *Aufschubzeit*, not earlier than five months before the first annuity date; [S8] § 1 Abs. 2 requires it after twelve years, and five months before at a twelve-year term; [S14] § 2 Abs. 7 requires two months. The model still treats the election as a **decision at a single known date with no notice mechanic**, which is now a `[std]` simplification of a documented rule rather than a gap

(delib-klassische_rentenversicherung-r22)=

### R22 — Versicherungsbote, "Debeka stellt klassische Rentenversicherung ein"
- Publisher / doc type: Versicherungsbote Verlag; trade press
- URL: https://www.versicherungsbote.de/id/4842718/Debeka-Rentenversicherung-Garantiezins/
- Retrieved: yes (HTML, read 2026-08-30)
- Used for: **the market-structure fact the whole product spec has to be read against**, and the retrieval confirms every element of it. Debeka *"will ebenfalls keine klassischen Rentenversicherungen mehr anbieten. Das bestätigte ein Unternehmenssprecher auf Anfrage."* From **1 July 2016** it offered five *Chance* variants — *"Während bei der sichersten Variante – nach Abzug von Kosten und Risikobeiträgen – 0,5 Prozent Zinsen und eine lebenslange Rente garantiert sind, können Kunden auch ganz auf einen Garantieanteil verzichten"* — the safest at **0,5 %** and the riskiest effectively a fund policy, with surplus and the unit-linked premium share going into an internal ETF fund. That construction is what [S11] and [S12] describe ten years on, so the 2016 announcement and the 2026 AVB are the same design at two dates. The 0,5 % guarantee sits **below** the then-current *Höchstrechnungszins* of 1,25 %, which is the point [R10] makes in principle — cap and *Garantiezins* are not the same thing — and [S11] shows in a current contract.
- **Two refinements.** The report on the other carriers is narrower than the previous entry made it: *"Bereits im vergangenen Jahr reagierten einige Unternehmen und stoppten den Vertrieb von klassichen [sic] Rentenversicherungen. Dazu zählten unter anderem Allianz, Zurich und Generali. So wolle etwa die Allianz nur noch dann derartige Produkte anbieten, wenn dies ausdrücklich vom Kunden gewünscht werde."* Allianz withdrew the product from **active distribution**, not from sale. And **gap 9's tension with [S4] is now resolvable on the documents**: [S4] is a Zurich *Verbraucherinformation* in Fassung **01/2026** for a *konventionell* deferred annuity in Schicht 3 and Schicht 2, priced on DAV 2004R at 1,00 %, and [S7] and [S16] are its Fassung 01/2025 siblings. A wording maintained and reissued across three vintages is not a withdrawn product; the reconcilable reading is that the classic chassis left the **front of the shelf** in 2015–2016 and stayed available. The product spec's description of it as the German market's **reference chassis** stands, and the flat statement that Zurich stopped selling it should not be repeated without this qualification

(delib-klassische_rentenversicherung-r23)=

### R23 — Versicherungsjournal, "Allianz 'KomfortDynamik': Noch immer eine Rentenversicherung?"
- Publisher / doc type: Versicherungsjournal Verlag; trade press, with a cluster of companion third-party analyses in the same result set
- URL: https://www.versicherungsjournal.de/versicherungen-und-finanzen/allianz-komfortdynamik-noch-immer-eine-rentenversicherung-123163.php
- Retrieved: **no** — the page answers 200 but the body is a **paywall**: *"Dieser Artikel ist nur für Premium-Abonnenten des VersicherungsJournals frei zugänglich."* What is public is the headline, the byline (a guest contribution by the broker Philip Wenzel), the date **17.8.2015** and a two-line standfirst on the industry's exit from the *Klassische* and its success in selling the new guarantee concepts. The entry is kept as a known reference
- Used for: the **date and framing** only — that by August 2015 the withdrawal of the classic annuity and its replacement by guarantee concepts was being debated in the trade press, which brackets [R22]'s July 2016 Debeka announcement. **Corroboration of the 60 / 80 / 90 % guarantee ladder is not available from this article** and is re-sourced to [S13], the carrier's own page, which states it. The **two Allianz charge figures** — an *Abschlussprovision* of 1 575 € and total costs of at most 0,95 € per 100 € of capital formed — are **not established by any retrieved document in this corpus**. They came from search summaries of third-party analyses of a Schicht-1/Schicht-2 quotation, they stay `[unverified]`, and they remain the reason every charge in the model is `[std]`

(delib-klassische_rentenversicherung-r24)=

### R24 — Consumer and comparison-portal cluster on the Rentenfaktor, the Rentengarantiezeit, the Überschussbeteiligung and the death benefit
- Publisher / doc type: LV 1871; NÜRNBERGER; Verivox; Gabler *Versicherungslexikon* and *Wirtschaftslexikon*; Wikipedia (German); Deutsche Rentenversicherung; fragfina.de; gn-finanzpartner.de; Finanzküche; Compeon; versicherung-vergleiche.de; financedoor.de; R+V; vr.de and others — **cited collectively, because no single member is load-bearing and every fact drawn from the cluster is corroborated by at least one other member**
- URL: representative members include https://www.lv1871.de/private-rentenversicherung/fragen/todesfall/ , https://www.nuernberger.de/themenwelt/beruf-vorsorge/rentenfaktor/ , https://wirtschaftslexikon.gabler.de/definition/ueberschussbeteiligung-48786 , https://www.fragfina.de/research/rentenfaktor-check-2025/ , https://www.finanzkueche.de/blog/garantierter-rentenfaktor , https://www.compeon.de/glossar/rentengarantiezeit/
- Retrieved: yes for the six representative members listed above (HTML, read 2026-08-30); the rest of the cluster was not re-swept and nothing new is drawn from it
- Used for: most of the **definitional** material the technical notes formalise. The *Rentenfaktor* arithmetic is confirmed in the cluster's own words — NÜRNBERGER states it as *"Angespartes Kapital / 10.000 x Rentenfaktor = Monatliche Rente"* with the worked illustration *"100.000 EUR / 10.000 x 30 = 300 EUR monatliche Rente"* — and, more usefully, it is now confirmed in **contracts**: [S11] § 52 Abs. 1, [S14] § 2 Abs. 5 and [S18] all state the per-10 000-EUR form. The guaranteed/current distinction with its *Sicherheitsabschlag* is confirmed here and quantified below; the guaranteed factor as a **floor** with the current factor applying when higher is the other side of [S9]'s rule. The *Zinsüberschuss* definition that makes the *Rechnungszins* the **hurdle rate** rather than merely a discount rate is confirmed by [S15]'s declaration, which literally expresses the *Zinsüberschussanteil* as a percentage *"abzüglich Rechnungszins"*. The ***verzinsliche Ansammlung*** mechanics — surplus credited to an *Ansammlungsguthaben* and accrued with interest, settling at the end of each insurance year and on termination — are now also in [S15]'s own definition and in [S4] § 3 Abs. 6, which is `av_sur_pp_at(t, "AFT_INT")`; so is the *Bonusrente* alternative. The ***Rentengarantiezeit*** durations and cost illustration stay with this cluster; the mechanic itself is [S1] § 1 Abs. 4. The **three death-benefit forms before *Rentenbeginn*** — *Beitragsrückgewähr* with or without attributable surplus, the accumulated *Deckungskapital*, or a *Hinterbliebenenrente* — are `death_benefit_form` and `db_incl_surplus`, and each is now attested by a contract: [S8] § 1 Abs. 1 for the refund without interest, [S9] § 1 Abs. 3 for the `max` of contract value and refund, [S10] for the survivor's annuity.
- **Gap 3 is closed by this cluster, not left open by it.** fragfina's *Rentenfaktor-Check 2025* publishes a market table for six deferment terms, all to attained age 67, of the highest and average **current** and **guaranteed** factors:

  | term | highest current | average current | highest guaranteed | average guaranteed |
  |---|---|---|---|---|
  | 40 years | 29,47 | 27,27 | 27,31 | 24,33 |
  | 30 years | 30,69 | 28,41 | 28,42 | 25,37 |
  | 20 years | 32,06 | 29,69 | 29,67 | 26,54 |
  | 15 years | 32,81 | 30,40 | 30,36 | 27,18 |

  with the lowest current factor at a 40-year term 21,41 and the lowest guaranteed 17,72. The gap between the average current and the average guaranteed factor — about **11 %** at a 40-year term — is the *Sicherheitsabschlag* the cluster describes, measured. Read with [R19]'s 2021/2022 averages of 29,09 and 25,97 this is a market level, a range and a time series, all three of which the library previously recorded as unestablished. **The model's factors are unchanged in this pass** and remain `[std]`; the divergence is stated in `model.md`. The teaching illustrations in the cluster remain arithmetic and are still not used as levels

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen;
research provenance in `_research/regulatory-actuarial.md`). Every entry in that library carries
**its own** retrieval status, recorded there; that library was drafted under the same
blocked-egress conditions as this file, so read each REG-R entry's status where it stands rather
than carrying this file's tally across. Entries cited by the klassische-Rentenversicherung
documents, and what each gave them:

- **REG-R1** — Richtlinie 2009/138/EG (Solvabilität II): the framework the undiscounted cash flows feed, named and not implemented.
- **REG-R2** — Delegierte Verordnung (EU) 2015/35: contract boundaries and the best-estimate definition, in the valuation pointers.
- **REG-R4** — EIOPA risk-free term structures: the curve a valuation layer would discount `liability_cf` on.
- **REG-R5**, **REG-R6** — VAG 2016 and §§ 74–110: the supervisory frame, the best estimate and the risk margin.
- **REG-R10** — VAG §§ 140, 145: the *Rückstellung für Beitragsrückerstattung*, the reservoir a declaration is paid out of.
- **REG-R11** — VAG §§ 141–143: the *Verantwortlicher Aktuar* and the *Treuhänder*, who signs off a declaration.
- **REG-R12** — VAG §§ 221–236 and Protektor: the *Sicherungsfonds*, in the product spec's counterparty section.
- **REG-R14**, **REG-R15** — DeckRV and the *Höchstrechnungszins* history: the article-level home of the rate whose vintage stack the model carries, and the 1,00 % of the 2026 points.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: the **25 ‰ / 40 ‰ ceilings** and the *Beitragssumme* base — the two `charge_id` sets and `alpha_total_pp`.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Zinszusatzreserve* and the *Korridormethode*: cited in the reserve pointers, not modelled.
- **REG-R18**, **REG-R19** — MindZV and RfBV: the minimum allocation to the RfB and its collective part, behind the statement that a declaration is constrained rather than free.
- **REG-R20** — LVRG 2014: the reform that lowered the *Höchstzillmersatz* to 25 ‰ and restricted the *Bewertungsreserven* share.
- **REG-R21** — BaFin, the MaGo and the *Auslegungsentscheidungen*: the supervisory expectations on model governance.
- **REG-R22** — VVG 2008 and § 171 (*halbzwingende Vorschriften*): why §§ 165 and 169 cannot be contracted away to the policyholder's detriment.
- **REG-R23** — VVG §§ 8 and 152, the 14-day and 30-day *Widerrufsrechte*: the *Widerruf* that sits inside the year-1 lapse rate.
- **REG-R24** — VVG § 153 at article level: the *Überschussbeteiligung* obligation and the *hälftige* participation, the cross-product home of [R4].
- **REG-R25** — VVG §§ 154, 155: *Modellrechnung* and *Standmitteilung*, the disclosure duties around a declaration.
- **REG-R26** — VVG §§ 150, 159–162: *Bezugsberechtigung* and *Selbsttötung*, in the product spec's benefit provisions.
- **REG-R27** — VVG § 163 at article level: the adjustment channel [R3] is read against.
- **REG-R28** — VVG §§ 165–170: the **five-year spreading of acquisition costs** the § 169 Abs. 3 floor rests on, and the *Stornoabzug* conditions — `alpha_spread_years`, `cv_floor_pp` and `surr_charge_pp`.
- **REG-R30** — VVG §§ 19, 37, 38, 157, 158: *Anzeigepflicht* and *Zahlungsverzug*, which make German lapse a three-way decrement the model does not split.
- **REG-R31** — VVG §§ 6, 7, 1a, 7b, 7c and the VVG-InfoV: cost disclosure and *Effektivkosten*, none of which the corpus produced for this product.
- **REG-R33** — IDD and § 34d GewO: the distribution frame, in the product spec's market-role section.
- **REG-R34** — Unisex, EuGH C-236/09 (*Test-Achats*) and §§ 19, 20, 33 AGG: **the sixteenth pitfall** — `sex` reaches the mortality basis and never the tariff.
- **REG-R35** — BaFin Merkblatt 01/2023 (VA), *Wohlverhaltensaufsicht*: the *angemessener Kundennutzen* test on charges.
- **REG-R36** — the BGH line of authority on German life contracts: the case law behind the *Zillmerung* and surrender-value discussion.
- **REG-R38** — AltEinkG and the *Drei-Schichten-Modell*: the layer architecture that places this product in Schicht 3.
- **REG-R41** — EStG § 22 Nr. 1 Satz 3 Buchst. a and § 55 EStDV: the *Ertragsanteil* at article level, the cross-product home of [R5].
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6: the *Unterschiedsbetrag* and the 12/62 rule at article level — the argued shape of the **duration-12 lapse step**.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the two-basis discipline `mort_rate_guar` / `mort_rate` implements, and the licensing reason the tables are cited and not shipped.
- **REG-R48** — DAV 2008 T: named only to mark the boundary — this product's death benefit before *Rentenbeginn* is priced on the **annuity** table, which is a German peculiarity the notes state explicitly.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand: the generational annuity tables, and what the shipped proxy must preserve of them.
- **REG-R52** — Destatis *Sterbetafeln* and *Generationensterbetafeln*, with the reuse licence: the intended base for a user-supplied replacement decrement table.
- **REG-R53** — the German life market in numbers: the only public declared-rate pair the library has (2,53 % Klassik / 2,58 % Neue Klassik for 2025), which is what the `base` declared path of 2,55 % sits inside, and the statement that **the declared rate contains the guarantee**.
- **REG-R54** — HGB §§ 341–341o, RechVersV, BerVersV: the statutory accounts the *Deckungsrückstellung* is reported in, in the reserve pointers.
- **REG-R55** — IFRS 17 and the Variable Fee Approach: named as the measurement model a participating contract falls under, and not implemented.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional standard the model documentation sits under.

---

## Provenance note

Extraction details — which fact was read from which document, the section-level notes organised
by mechanic, and the **twenty-six-item gaps-and-caveats register** — live in
`_research/klassische_rentenversicherung.md`. That file is the citation ground truth for the S#
and R# numbering used here.

**The gaps register was written before any document could be opened, and a retrieval pass on
2026-08-30 has now opened most of them.** The caveat list below is restated against what was
actually read; where a gap has closed it says so, and where it stands it says why.

- **The research budget ran out after eighteen queries** (gap 1). That shaped which documents are
  *listed* here, and this pass did not add any. What it no longer determines is how much each
  listed document yields: eighteen of the nineteen primary sources and most of the references are
  now retrieved in full.
- **Clause-level text is now established from nine primary documents** (gap 2 closed for those).
  [S1], [S4], [S5], [S6], [S7], [S8], [S9], [S10], [S11], [S14] and [S16] are read as PDFs with
  their § numbering intact, and paragraph references in these documents are checkable against
  them. Nothing was invented before and nothing is invented now; the difference is that the
  references are now specific.
- ***Rentenfaktor* levels and a current *Überschussbeteiligung* declaration are now established**
  (gaps 3 and 4 closed). [R24] carries a 2025 market table of guaranteed and current factors by
  term, [R19] the 2021/2022 averages, and [S15] a carrier's *Überschussverteilung 2026* with a
  total credited interest of **3,00 %** for 2026 (2,25 % for 2025) before the *Rentenbeginn*.
  `rentenfaktor_table.csv` and `decl_rate_table.csv` are **unchanged in this pass** and still ship
  anchored `[std]` scenario paths; they now diverge from observable market levels in a stated
  direction rather than standing beside nothing, and `model.md` records where.
- **Charge and behavioural levels remain largely unestablished** (gaps 13, 14, 20). No carrier
  publishes an acquisition or administration loading for this product, and no *Stornoquote* was
  found. Two *Stornoabzug* levels now are on the record — a flat 250 EUR at [S4] and a tapering
  5 % of the *Deckungskapital* at [S11], against none at [S8] and [S9] — and the *Höchstzillmersatz*
  ceiling is statutory [R7]. Every charge, expense, lapse and take-up level in the model stays
  `[std]` and labelled the modeller's view.
- **The DAV tables are not public and are not redistributed** [R12] [R13] [REG-R47] [REG-R49].
  Both DAV documents are now retrieved in part, and both confirm the structure without releasing
  the values. `mort_table.csv` is an anchored `[std]` proxy that keeps the generational structure
  and none of the values.
- **The annuity payment timing is established at one carrier** (gap 19 closed there): [S9] § 1
  Abs. 1, *"Wir zahlen die Rente monatlich, jeweils zum Monatsersten"* — monthly in advance. The
  model's monthly-in-advance convention compressed onto the annual grid remains an explicit
  `[std]` simplification of the grid, not of the timing.
- ***Beitragsrückgewähr in der Rentenbezugsphase* is established and is not modelled** (gap 18
  contradicted). [S4] § 1 Abs. 5 offers it as an alternative to the *Rentengarantiezeit*.
  `claims_death(t)` is still zero for every `t` after the *Rentenbeginn*; that is now a **known
  omission** rather than an absence of evidence, and `model.md` states it as one.
- **Zurich's status is reconcilable on the documents** (gap 9 narrowed). [R22] reports Zurich among
  carriers that stopped *distributing* the classic product in 2015, and says of Allianz that it
  would offer it only on explicit customer request. [S4], [S7] and [S16] are Zurich packs for this
  chassis in Fassung 01/2025 and 01/2026. A wording reissued across vintages is maintained, not
  withdrawn; the representative design is still described as **the German market's reference
  chassis** rather than as a shelf product.
- **Living texts** (gap 26), now with the versions attached. VVG §§ 153, 163, 165 and 169 were read
  as canonical XML at *Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*; EStG §§ 20,
  22 and 52 at *Art. 7 G v. 29.6.2026 I Nr. 197*; DeckRV §§ 2 and 4 at *Art. 1 V v. 19.7.2024
  I Nr. 250*. The GDV model conditions carry *Stand: 21.07.2025* and the survivor's-annuity rider
  *Stand: 14.11.2019*; Zurich's pack is Fassung 01/2026, NÜRNBERGER's GN331451_202501, Cosmos's
  LA 904 A (01.17), Debeka's B LV 85 (01.07.2026), Mecklenburgische's Version 07.2025 and Bayern-
  Versicherung's declaration is for 2026. **Check every article number and every figure for later
  amendment before relying on it** — and note that five of the URLs in this file proved to be
  living paths whose file names no longer match their contents ([S2], [S5], [S7], [S11], [S16]).

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-klassische_rentenversicherung-r1
[R10]: #delib-klassische_rentenversicherung-r10
[R11]: #delib-klassische_rentenversicherung-r11
[R12]: #delib-klassische_rentenversicherung-r12
[R13]: #delib-klassische_rentenversicherung-r13
[R14]: #delib-klassische_rentenversicherung-r14
[R16]: #delib-klassische_rentenversicherung-r16
[R17]: #delib-klassische_rentenversicherung-r17
[R19]: #delib-klassische_rentenversicherung-r19
[R2]: #delib-klassische_rentenversicherung-r2
[R20]: #delib-klassische_rentenversicherung-r20
[R22]: #delib-klassische_rentenversicherung-r22
[R23]: #delib-klassische_rentenversicherung-r23
[R24]: #delib-klassische_rentenversicherung-r24
[R3]: #delib-klassische_rentenversicherung-r3
[R4]: #delib-klassische_rentenversicherung-r4
[R5]: #delib-klassische_rentenversicherung-r5
[R6]: #delib-klassische_rentenversicherung-r6
[R7]: #delib-klassische_rentenversicherung-r7
[R8]: #delib-klassische_rentenversicherung-r8
[R9]: #delib-klassische_rentenversicherung-r9
[REG-R16]: #delib-reg-r16
[REG-R18]: #delib-reg-r18
[REG-R47]: #delib-reg-r47
[REG-R49]: #delib-reg-r49
<!-- END generated citation links -->
