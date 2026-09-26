# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/pflegerentenversicherung.md` (the
citation ground truth for this product) and are **frozen — never renumber**. Unused sources are
omitted, so the numbering has gaps. **S3** (GDV *Musterbedingungen* for life-assurance products)
is absent because the research file could not establish that the GDV publishes a model condition
for the *Pflegerentenversicherung* at all, and no benefit, premium, surrender or paid-up rule
anywhere in `product-spec.md` or `technical-notes.md` is attributed to it — citing it would
attribute a claim to a document that may not exist. **S6** (*Basisinformationsblatt* / PRIIP-KID)
is absent because the PRIIPs perimeter question the research file raises there is carried in the
product documents from the cross-product entry [REG-R32], which states the Regulation at article
level, rather than from a document class of which not one instance was located; the research
file's own `[R25]` pointer inside that entry is likewise not part of the frozen `R1..R24` range
and appears nowhere here. **S15** (*Pflege-Bahr* tariff conditions of a *geförderter Tarif*) is
absent because the *Pflege-Bahr* parameters the documents print — the *Zulage*, the minimum
contribution, the *Kontrahierungszwang*, the five-year *Wartezeit* — are cited to the statute [R8]
and not to a carrier's tariff conditions, none of which was located. **The 10 / 20 / 30 / 40 / 100 %
grid is not among them**: § 127 SGB XI fixes no percentage schedule, only a benefit at every
*Pflegegrad* with a floor of 600 € at grade 5, so the `bahr` schedule is a market convention and
not a statutory one — see [R8]. **R17** (BaFin supervisory material on
life and LTC business) is absent because **nothing product-specific to *Pflegerentenversicherung*
was located at BaFin**, so no BaFin statement of any kind is cited; the supervisor enters the
product documents only through the cross-product entry [REG-R35]. Access date at
drafting: **2026-08-29**; the re-verification pass that set the `Retrieved` lines below read the
documents on **2026-08-30**. No sources were newly added in either pass. Cross-product [REG-R#] tags
are listed in their own section at the end.

**Retrieval conditions, stated plainly.** They changed between the drafting of this product and the
state of the file you are reading, and both halves belong in the record.

1. **How this product was drafted.** `delib` was written under a default-deny network policy. Direct HTTP egress from the build environment was refused with HTTP 403 at the gateway for every host outside a short package-registry allowlist — `gesetze-im-internet.de` (SGB XI, VVG, VAG, EStG, SGB XII, DeckRV, KVAV), `bafin.de`, `gdv.de`, `aktuar.de`, `pkv.de`, `destatis.de`, `bundesgesundheitsministerium.de` and `vdek.com` among them — and the session's shared `WebSearch` budget was exhausted before this product was started. This was therefore the one product in `delib` reached with **neither** research channel open: its first draft rested on the authoring model's own knowledge of German insurance law and German actuarial practice, disciplined by the `[std]` and `[unverified]` tags the house brief imposes for exactly that case. That is how the file came to exist and it is not deleted here.
2. **What has since been done.** The policy was lifted and the citations were re-verified against the primary documents on **2026-08-30**. Every German instrument cited below was read as canonical XML from `gesetze-im-internet.de`, with each law's amendment status (`Stand`) recorded on its entry; insurer *AVB*, *Verbraucherinformationen* and the *Produktinformationsblatt* class were pursued as PDFs and read where they are published. Across `delib` as a whole the pass ends with **501 of 805 source entries (62 %) marked `Retrieved: yes`**, the rest naming what stopped them — HTTP 404 at the cited URL, a consent or JavaScript wall, a paywall, or a subscription login.
3. **Where this product ends up.** Of the **thirty-six** [S#] and [R#] entries below, **twenty-seven read `Retrieved: yes`** and **five read `Retrieved: no`**. The remaining four are partial and say so on their own lines: **S5** and **S10** (part of the document read, part behind an offer or a paywall), **R6** (statute yes, the *Begutachtungs-Richtlinien* no) and **R9** (the act itself not opened, its citation and effect read in two documents that recite them). Counting only the entries that resolve cleanly one way or the other, **27 of 32 — 84 % — are retrieved.**
4. **The five still marked `no`, and why.** Not one of them is a network failure; every one is a property of the document. **S9** — no German *Pflegerenten* rate card is published at all, the carriers publishing conditions and withholding the tariff. **S13** — the comparison portals were deliberately not queried, a quotation being generated per enquiry and not a document that can be cited. **S8** — no *Standmitteilung* specimen is public, the statement being issued to a named policyholder; the § 155 VVG field list is read instead. **R10** — the PUEG was not opened as an act, its operative content being read where it now lives, in SGB XI as consolidated. **R16** — the DAV 2008 T derivation was located but not opened and nothing was located for DAV 2004 R, and this product uses neither table.

What follows, and it governs every entry below:

- **A `Retrieved: yes` entry is a record; a `Retrieved: no` entry is still a pointer, not a certificate.** Where the line says `yes`, the document was opened and the passage the entry rests on was read on the stated date. Where it does not, `[R2]` beside a statement about § 15 SGB XI means *this is the instrument the statement should be checked against*, and asserts nothing more. **Read the `Retrieved` line before relying on the tag**: treat a claim as sound where its entry says `yes`, and as provisional where it does not.
- **The re-verification changed things, and the changes are reported rather than quietly applied.** It corrected claims the drafted text got wrong — the `bahr` *Leistungsstaffel* lost its statutory citation, the *Stornoabzug* market range was out by a factor of five, the § 155 VVG field list is five items and not four, the grade-1 residential *Zuschuss* is 131 € and not 125 € — and each is written up in the provenance note and in the findings section at the end of this file.
- **Retrieved entries now carry an edition, a `Stand`, a page count and a read date.** Entries still marked `no` carry `URL: not established` unless the canonical form is one this author is confident of, and they assert **no edition, no document number, no *Bundesgesetzblatt* citation and no publication date**, because none was checked.
- **German is quoted only out of documents that were opened.** Where a statute or a *Bedingungswerk* is quoted in this product's documents the quotation comes from the retrieved text and the entry says which; elsewhere the rule is described in English, in the author's own words, as *what the instrument provides*.
- **`[unverified]` is still used generously** in the product documents, and has been lifted only where a retrieved document carries the fact. Every remaining paragraph number, effective date, amount, percentage, threshold and market figure keeps the tag unless a `Retrieved: yes` entry supports it or it is a structural fact not in dispute.
- **Uncertain levels remain `[std]` parameters rather than citations.** Every biometric rate, every charge, every lapse rate, the *Leistungsstaffel* levels, the *Stornoabzug* and the premium itself are **[std]**, each listed with its rationale in `model.md`. A `[std]` number is honest about being a construction; a fabricated `[S9]` premium would not be, and there is none.

---

## Primary product sources

(delib-pflegerentenversicherung-s1)=

### S1 — PKV-Verband, *Musterbedingungen für die private Pflegepflichtversicherung* (MB/PPV)
- Publisher / doc type: Verband der Privaten Krankenversicherung e. V. (PKV-Verband), Köln; *Musterbedingungen* — model conditions for the compulsory private LTC cover of § 23 SGB XI, adopted with variations by every private health insurer.
- URL: `https://www.pkv.de/fileadmin/user_upload/PKV/3_PDFs/ABV_und_MB/AVB-PPV.pdf`
- Retrieved: **yes** (PDF, 56 pp., *AVB/PPV* — Teil I MB/PPV 2026, Teil II Zusatzvereinbarungen, Teil III Tarifbedingungen Tarif PV with Tarifstufen PVN and PVB, Teil IV the § 140 SGB XI *Überleitungsregelungen*; read 2026-08-30).
- Used for: the one structural fact that matters to a *Pflegerente* — **private wordings do not write an independent medical definition of the insured event; they carry the SGB XI definition itself**. § 1 Abs. 2 MB/PPV 2026 opens *"Versicherungsfall ist die Pflegebedürftigkeit einer versicherten Person"* and then reproduces § 14 SGB XI's test word for word, down to *"auf Dauer, voraussichtlich für mindestens sechs Monate"*; § 1 Abs. 6 reproduces the § 15 SGB XI point bands (12,5 / 27 / 47,5 / 70 / 90) and Abs. 7 the *besondere Bedarfskonstellationen* route. **The reading this changes:** the wording does not *refer* to the live statute, it **copies** it, so the private sector's rendering of the trigger is fixed at the edition of the conditions and moves only when the conditions are re-issued. That is the same version-pinning device the retrieved life wording uses [S4], and it is why the "definition risk no wording can hedge" framing this product's documents used to carry has been corrected.

(delib-pflegerentenversicherung-s2)=

### S2 — PKV-Verband, *Musterbedingungen für die ergänzende Pflegekrankenversicherung* (MB/EPV)
- Publisher / doc type: PKV-Verband; *Musterbedingungen* for the **top-up** LTC cover written as *private Krankenversicherung* — the *Pflegetagegeld* and *Pflegekosten* forms.
- URL: `https://www.pkv.de/fileadmin/user_upload/PKV/3_PDFs/ABV_und_MB/MB-EPV.pdf`
- Retrieved: **yes** (PDF, 15 pp., *MB/EPV 2017*, Stand November 2022, §§ 1–19; read 2026-08-30).
- Used for: **the contrast document of the whole product specification**, and it does the job better than the entry assumed. Three clauses carry it. § 1 Abs. 1 offers *Ersatz von Aufwendungen für Pflege* or *ein Pflegetagegeld* — the two health-branch forms, and no annuity. § 1a writes the trigger out in full inside the conditions, on the same six-*Bereiche* criteria as SGB XI, again by copying rather than by reference. And § 8b is the clause a *Pflegerente* has no counterpart to: the insurer compares required against calculated *Versicherungsleistungen und Sterbewahrscheinlichkeiten* **at least annually** for each tariff, and on a deviation beyond the *gesetzlich oder tariflich festgelegte[r] Vomhundertsatz* **all** premiums of that observation unit are recalculated — with a policyholder right of termination within two months of the notice (§ 13 Abs. 4). § 1 Abs. 6 carries the *Alterungsrückstellung* and its transfer on a tariff change. Together those are the health-insurance regime — § 203 VVG re-rating [R11] and the § 146 VAG / KVAV ageing provision [R12] [R14] — against which a *Pflegerente* is a **life** contract with a *Deckungsrückstellung* and no ordinary re-rating power. The product specification's competing-forms section and its "why the *Pflegerente* costs more" argument reduce to that difference.

(delib-pflegerentenversicherung-s4)=

### S4 — *Allgemeine Bedingungen für die Pflegerentenversicherung* (AVB) — IDEAL Lebensversicherung a.G., *IDEAL PflegeRente Exklusiv*
- Publisher / doc type: IDEAL Lebensversicherung a.G., Berlin; the complete offer pack for a stand-alone *Pflegerentenversicherung* — *Versicherer- und Verbraucherinformationen* under §§ 1 and 2 VVG-InfoV, the *Allgemeine Versicherungsbedingungen* **AB-IPR-2022A** (§§ 1–22), and the *Ergänzende Versicherungsbedingungen* EB-IPR-RENTENDYN-2022A, EB-IPR-RGZ-2022A, EB-IPR-SOFORT-2022A and EB-IPR-TOD-2022A. A carrier's own *Produktbeschreibung* (`pb_ipr_1124`) is retrieved beside it.
- URL: `https://www.ideal-versicherung.de/idam2.0/Dokumente/Produkte/IPR/Bedingungen_IDEAL_PflegeRente.pdf` (conditions, 67 pp.); `https://www.ideal-versicherung.de/idam2.0/Dokumente/Produkte/IPR/Produktbeschreibung_IDEAL_PflegeRente.pdf` (4 pp.).
- Retrieved: **yes** (both PDFs, from the insurer's own site; conditions pack stamped 18.11.2024, AVB edition AB-IPR-2022A, *Produktbeschreibung* edition `pb_ipr_1124`; read 2026-08-30).
- Used for: **the most-cited entry in this product, and the one this pass changes most.** It is no longer a document-class description: one carrier's complete wording has been read, and the clause inventory the representative specification follows is now checked against it clause by clause. What the wording establishes, with the clause: the *vereinbarte Pflegerente* paid **monthly in advance** for as long as the insured grade holds and only for a *versicherter und anerkannter Pflegegrad* (§ 1 Abs. 1); entitlement dated from the **month the assessment fixes as onset**, not the decision month, backdated up to three years (§ 1 Abs. 1 a); full *Beitragsbefreiung* while the annuity runs, optionally extended to *ab Pflegegrad 2* (§ 1 Abs. 1 c); a **lock-in** after twelve months at grade 4 or 5 (premiums cease permanently) and after twenty-four (the annuity is paid for life even if the grade falls away entirely) (§ 1 Abs. 1 d); the trigger, on the § 14 SGB XI test with the § 15 point bands **pinned to the statute's Stand of 28.03.2021**, or alternatively on a self-contained *Punktesystem* (§ 8); *Wartezeit* **keine**; the § 163 VVG re-rating clause recited almost verbatim, trustee and actuary's-error exclusion included (§ 11 Abs. 7); the § 169 VVG *Rückkaufswert* with the five-year cost-spread floor **and a 25 % *Stornoabzug***, rising to 50 % after a withdrawal (§ 13 Abs. 6); *Beitragsfreistellung* at the same value and with **no** *Stornoabzug* (§ 13 Abs. 11); the § 4 DeckRV *Zillmerung* at **2,5 % der von Ihnen während der Laufzeit des Vertrags zu zahlenden Beiträge**, with post-annuity administration charged as a percentage of the annuity paid (§ 17); and a territorial clause that is worldwide for cover but requires the assessment — and every *Nachprüfung* — to take place **in the EU, Switzerland or Norway**, failing which the contract ends (§ 6). Where the composite specification departs from this wording it now says so and why.

(delib-pflegerentenversicherung-s5)=

### S5 — *Produktinformationsblatt* (PIB) / *Informationsblatt zu Versicherungsprodukten* (IPID)
- Publisher / doc type: an individual German *Lebensversicherer*; the short pre-contractual product summary. The German market uses both the national *Produktinformationsblatt* and the EU IDD *Informationsblatt zu Versicherungsprodukten* [REG-R31] [REG-R33]; the retrieved pack settles which for this product — its § 5 b names *"dem Informationsblatt zu Versicherungsprodukten"*, the IDD document, and no national *Produktinformationsblatt*.
- URL: named but not separately published: `https://www.ideal-versicherung.de/idam2.0/Dokumente/Produkte/IPR/Produktbeschreibung_IDEAL_PflegeRente.pdf` is the carrier's public substitute.
- Retrieved: **partly.** The *Informationsblatt zu Versicherungsprodukten* itself is **not** retrieved — it is quotation-specific and is issued with an offer, and the conditions pack refers every cost figure to it (§ 17 Abs. 1, 2 a, 2 b) without reproducing one. What **is** retrieved (PDF, 4 pp., edition `pb_ipr_1124`, read 2026-08-30) is the carrier's public *Produktbeschreibung*, which supplies the same parameter list minus the money.
- Used for: **the entry no longer records a pure absence.** From the *Produktbeschreibung*: entry ages **18 to 75**; *vereinbarte Rente* **250 € to 4 000 €** a month, minimum premium 60 € a year; *Wartezeit* **keine**; premium payable monthly, quarterly, half-yearly, annually, as an *Einmalbeitrag* or as a combination, lifelong or abgekürzt with a five-year minimum; benefit and cover **lebenslang**; *Todesfallleistung* as an optional *Beitragsrückgewähr* of 50–80 % of premiums paid (50–100 % on a single premium); *Dynamik* before the claim of 10 % every three years or 1–5 % a year, ending after the **third consecutive** refusal, and a *Rentendynamik* of 1–5 % a year for the first ten years of the annuity. **What is still not established is every euro cost figure** — the *Abschluss- und Vertriebskosten* total, the *Verwaltungskosten* share of the annual premium and the post-annuity administration percentage all live in the un-retrieved *Informationsblatt*, so every charge in delib stays **[std]**.

(delib-pflegerentenversicherung-s7)=

### S7 — *Verbraucherinformationen* / *Vertragsinformationen* under the VVG-InfoV
- Publisher / doc type: an individual German *Lebensversicherer*; the pre-contractual information package required by § 7 VVG and the VVG-InfoV [R11] [REG-R31]. The retrieved instance is IDEAL's *Versicherer- und Verbraucherinformationen* (3 pp.) together with the *Widerrufsbelehrung* and the reproduced VVG-InfoV text (4 pp.), both inside the [S4] pack.
- URL: `https://www.ideal-versicherung.de/idam2.0/Dokumente/Produkte/IPR/Bedingungen_IDEAL_PflegeRente.pdf` (pp. 1–7 of the pack).
- Retrieved: **yes** (PDF, within the 67-pp. pack stamped 18.11.2024; read 2026-08-30). The regulation behind it is read separately as canonical XML: VVG-InfoV § 2, Stand *zuletzt geändert durch Art. 13 G v. 26.5.2026 I Nr. 156*.
- Used for: the **disclosure obligation**, and the pass sharpens it to the exact statutory reason. § 2 Abs. 1 Nr. 1 VVG-InfoV requires the *einkalkulierte Abschlusskosten* as a single total and the *übrige* and *Verwaltungskosten* as shares of the annual premium; Abs. 2 requires Nrn. 1, 2, 4 and 5 to be given **in Euro**. The *Effektivkosten* of Nr. 9 are owed only *"bei Lebensversicherungsverträgen, die Versicherungsschutz für ein Risiko bieten, bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist"* — the same certainty test § 169 Abs. 1 VVG uses. **A pure-risk *Pflegerente* therefore carries the euro disclosures and no *Effektivkosten* figure**, which is what this entry always asserted and can now cite. The retrieved instance also confirms the carrier's own practice: § 6 of the pack refers the *Gesamtpreis* to the *Allgemeine Vertragsdaten* and every cost level to the *Informationsblatt* [S5]. **No charge level is retrieved, so every charge in delib remains `[std]`.**

(delib-pflegerentenversicherung-s8)=

### S8 — *Jährliche Mitteilung zum Stand Ihrer Versicherung* (Standmitteilung)
- Publisher / doc type: an individual German *Lebensversicherer*; the annual statement owed to the policyholder under § 155 VVG [R11] [REG-R25]. The carrier's name for it in the retrieved wording is the ***Mitteilung der Wertentwicklung***, which the AVB make the reference for the guaranteed *Rückkaufswert*, the *Stornoabzug*, the resulting *Auszahlungsbetrag* and the *beitragsfreie* annuity (AB-IPR-2022A §§ 9, 13, 17).
- URL: no specimen is public — the statement is issued to a named policyholder. The statutory field list is read instead as canonical XML.
- Retrieved: **no specimen.** The **obligation** is retrieved: VVG § 155, canonical XML, Stand *zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156*, read 2026-08-30; and the carrier's own references to the document are read in the [S4] pack.
- Used for: one point in the valuation-and-disclosure section, now stated from the statute rather than guessed. § 155 Abs. 1 requires, **for contracts with *Überschussbeteiligung***, the agreed benefit on a claim plus profit share (Nr. 1), the agreed benefit plus **guaranteed** profit share at maturity or annuity start on continued and on paid-up terms (Nrn. 2 and 3), the *Auszahlungsbetrag* on surrender (Nr. 4) and, for contracts written from 1 July 2018, the **sum of premiums paid** (Nr. 5). Two corrections follow: the field list is five items, not four — the sum of premiums paid was missing from the old description — and **the duty is conditional on the contract carrying an *Überschussbeteiligung* at all**, which matters here because delib's base run deliberately switches surplus off. That on a *Pflegerente* the guaranteed benefit is the ***vereinbarte Pflegerente* at the insured *Pflegegrad*, not a sum insured**, is confirmed by the retrieved wording's own minimum/maximum table (§ 1 Abs. 1 e).

(delib-pflegerentenversicherung-s9)=

### S9 — *Tarifblatt* / *Beitragstabelle* for a *Pflegerenten* tariff
- Publisher / doc type: an individual German *Lebensversicherer*; the rate card — premium per unit of *vereinbarte Rente*, by entry age, sex, *Beitragszahlungsdauer* and option set.
- URL: not established. IDEAL's public documents [S4] [S5] state the *Rente* band and the minimum premium but **no rate**; the premium reaches the customer only through a quotation (*Allgemeine Vertragsdaten*, *Informationsblatt*), which is not published.
- Retrieved: **no** — searched on 2026-08-30 and no German *Pflegerenten* rate card was found in public. This is a real market fact, not an environment limit: the carriers publish conditions and product descriptions and withhold the rate card.
- Used for: **still the single most consequential absence in this product, and it stays recorded rather than papered over.** Two retrieved documents narrow it without closing it. (a) The DAV's own *Ergebnisbericht* on DAV 2008 P prints ***exemplarische Beiträge und Aktivendeckungsrückstellungen*** (Anhang 3) on the published first-order bases [R15] — specimen premiums on a published table, not a carrier's tariff. (b) Assekurata's April 2026 study [S14] prints monthly premiums for four ***Pflegetagegeld*** tariffs at a 2 000 € residential benefit: **85 / 117 / 130 / 78 €** at entry age 45 and **134 / 184 / 199 / 215 €** at 55. Halved to delib's 1 000 € scale that is roughly 39–65 € at 45, and this product's own argument says a *Pflegerente* must cost **more** than a *Pflegetagegeld* for the same benefit — so delib's argued 50–100 € band at entry 45 sits where the argument predicts. **That is a consistency check against a neighbouring product, not a premium citation.** `Pflege_DE_S` still has no published *Pflegerenten* premium to reproduce: its *Beitrag* is struck by equivalence on stated `[std]` first-order bases.

(delib-pflegerentenversicherung-s10)=

### S10 — Stiftung Warentest / *Finanztest*, comparative tests of *Pflegezusatzversicherung*
- Publisher / doc type: Stiftung Warentest — **secondary**, not a product document; comparative product test with a scored ranking and a price table.
- URL: `https://www.test.de/Pflegetagegeldversicherungen-im-Vergleich-4837475-0/`
- Retrieved: **partly** — the free landing page and the test's scope were read on 2026-08-30; **the scored ranking and the price table are behind a paywall** (*Testergebnisse für 70 Pflegetagegeldversicherungen freischalten*, 4,90 €), so no score and no rated tariff is cited.
- Used for: one **structural** statement, now sourced from the test's own scope rather than asserted. The comparison covers *"27 Pflegetagegeldversicherungen von 24 privaten Krankenversicherern … jeweils für 45-Jährige und 55-Jährige, insgesamt Ergebnisse für 70 Tarife (Stand: Mai 2023)"* — **Pflegetagegeld only, and no *Pflegerentenversicherung* tariff is in it at all**, which is the concentration this entry always claimed. The page also sizes the gap from the vdek series [R20]: for 2023, 1 139 € a month for the care component and 2 411 € including *Unterkunft* and *Investitionskosten*. **The second claim this entry used to carry — that the tests are consistently critical of *Pflege-Bahr* — is not visible on the free page and is dropped from here**; the *Pflege-Bahr* criticism is now cited to [S12], which states it in the open.

(delib-pflegerentenversicherung-s11)=

### S11 — Verbraucherzentrale, consumer guidance on *Pflegezusatzversicherung*
- Publisher / doc type: Verbraucherzentrale Bundesverband and the *Länder* consumer centres — **secondary**; consumer guidance pages.
- URL: `https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflegeantrag-und-leistungen/ist-eine-pflegezusatzversicherung-eine-sinnvolle-absicherung-fuers-alter-29435`
- Retrieved: **yes** (HTML, read 2026-08-30; the page carries 2026 premium figures).
- Used for: **the consumer-advice position, and this pass corrects how the product documents characterised it.** What the page actually says, on the *Pflegerente*: it is *"in der Regel beitragsstabil: Sowohl der Beitrag als auch der Leistungsumfang werden bei Vertragsbeginn festgeschrieben"*, the annuity is at the policyholder's free disposal, the waiver in claim is usual, the contract *"kann zudem durch Kündigung beendet werden, ohne dass sämtliche Einzahlungen verloren gehen, wie dies bei einer Tagegeld- oder Pflegekostenversicherung der Fall ist"*, insurers *"richten sich häufig nach der Einstufung der sozialen Pflegeversicherung. Andere definieren den Leistungsfall nach einer eigenen Systematik"*, the full annuity is normally reached only *"ab Pflegegrad 4 oder 5"*, and **the premium is *"etwa zwei- bis dreimal so hoch"* as the other forms'**. Every one of those is a claim this product's documents make, and all six are now confirmed from a retrieved page. **The correction:** the entry used to attribute to consumer bodies a warning that *Pflegetagegeld* is the form to avoid. That is not their position. The Verbraucherzentrale warns that premiums on **every** form will rise, and then **recommends the *Pflegetagegeld*** — *"gibt es schon zu geringen Beiträgen und - beim 'richtigen' Anbieter - auch mit guten Leistungen"* — while marking the *Pflegerente* as the expensive option. The form consumer bodies single out to avoid is *Pflege-Bahr* [S12], not *Pflegetagegeld*.

(delib-pflegerentenversicherung-s12)=

### S12 — Finanztip, guidance on *Pflegezusatzversicherung*
- Publisher / doc type: Finanztip — **secondary**; consumer guidance.
- URL: `https://www.finanztip.de/pflegezusatzversicherung/`
- Retrieved: **yes** (HTML, read 2026-08-30).
- Used for: the same class of evidence as S11, and it carries two things the delib documents act on. First, **the product's own central commercial claim, stated by a consumer body**: *"Während bei Pflegetagegeld- und Pflegekosten-Versicherungen die Beiträge mit der Zeit steigen können, ist der Beitrag bei Pflege-Rentenversicherungen für die gesamte Laufzeit festgelegt. Dafür sind diese Tarife jedoch von Anfang an deutlich teurer."* That is the § 163-versus-§ 203 trade [R11] in a consumer sentence. Second, the ***Pflege-Bahr* criticism**, which is where it belongs: because the tariff may refuse nobody, *"verlangen sie einen höheren Beitrag. Denn es ist damit zu rechnen, dass vor allem Menschen mit Erkrankungen dieses Angebot nutzen"* — the anti-selection reading [R8] this product cites the scheme for. Finanztip recommends *Pflegetagegeld* as *"die sinnvollste Variante"* and, *"Aufgrund der hohen Kosten"*, **advises against the *Pflegerente***. The sizing point this entry used to carry — that a top-up should be sized against the *Eigenanteil* rather than a round number — is now cited to [R20], which prints the *Eigenanteil* and its components.

(delib-pflegerentenversicherung-s13)=

### S13 — Comparison portals: Verivox, Check24
- Publisher / doc type: Verivox GmbH; CHECK24 Vergleichsportal GmbH — **secondary**; quote engines.
- URL: not established.
- Retrieved: **no** — deliberately not queried. A portal quotation is generated per enquiry, is not a published document, and cannot be cited as one; running one would produce a number with no retrievable source behind it, which is the opposite of what this pass is for.
- Used for: recording that the **only public route to a premium for a named age, benefit and option set on demand is still not used**, so the premium band the documents print rests on stated arithmetic and is `[std]`, never `[S13]`. What has changed is the surrounding evidence: published premium *ranges* for the neighbouring *Pflegetagegeld* form are now retrieved from [S14] and [S11], and the ratio between the forms — *"etwa zwei- bis dreimal so hoch"* for a *Pflegerente* [S11] — is retrieved too, so the band can be sanity-checked without a quotation.

(delib-pflegerentenversicherung-s14)=

### S14 — Ratings agencies: Morgen & Morgen, Franke und Bornberg, Assekurata
- Publisher / doc type: MORGEN & MORGEN GmbH; Franke und Bornberg GmbH; ASSEKURATA Assekuranz Rating-Agentur GmbH — **secondary**; product ratings and market studies. The retrieved instance is Assekurata's study *Wege zur Pflegevollversicherung mit der Pflegezusatzversicherung*, Köln, April 2026, published by the PKV-Verband.
- URL: `https://www.pkv.de/fileadmin/user_upload/PKV/3_PDFs/Gutachten_Studien/26-04_Assekurata-Studie_Pflegezusatzversicherung.pdf`
- Retrieved: **yes** (PDF, 45 pp., April 2026, read 2026-08-30). Nothing from Morgen & Morgen or Franke und Bornberg was retrieved.
- Used for: three things, and it is the single most useful secondary document in this product. (a) **Market counts at end-2024**, cited by the study to the PKV-Verband: *Pflegetagegeld* **3 021 300** insured, *Pflege-Bahr* **890 091**, *Pflegekosten* **366 100**, against about **4,5 million** persons — **5,4 % of the population** — holding any *Pflegezusatzversicherung*, a figure the study's own footnote 8 marks *"Inklusive Pflegerentenversicherung"*. **The four named classes do not add to the total, and the study does not carve the residue out**, so [S16] and [R22]'s finding survives: there is still no published count of German *Pflegerente* contracts. (b) **Duration**, which this product had no source for at all: the study cites the *BARMER-Pflegereport 2024* for a mean duration of *Pflegebedürftigkeit* of **7,5 years** for 2022, falling to **about five years** where care begins after 60 — **4,0 years for men and 5,7 for women** — and the Caritas figure of **25 months** mean length of stay in a *Pflegeheim*. (c) **A premium benchmark for the neighbouring form** [S9]. It also records, in terms, that *"keine Informationen darüber [existieren], wie lange die Personen in den einzelnen Pflegegraden verweilen"*, because the *Pflegegrade* only date from 2017 — the per-grade sojourn data `Pflege_DE_S` would need. The variation table in `product-spec.md` is still a market-range reconstruction and is **not** rating data. See also [REG-R53].

(delib-pflegerentenversicherung-s16)=

### S16 — PKV-Verband, *Zahlenbericht der privaten Krankenversicherung* and the association's *Pflegezusatzversicherung* statistics
- Publisher / doc type: PKV-Verband — **secondary** for product terms, primary for market counts; annual statistical report and standing statistics pages.
- URL: `https://www.pkv.de/fileadmin/user_upload/PKV/3_PDFs/Publikationen/Zahlenbericht_2024.pdf` (*PKV in Zahlen 2024*); `https://www.pkv.de/wissen/pflegepflichtversicherung/vorsorgen-mit-der-pflegezusatzversicherung/`
- Retrieved: **yes** (PDF, *Zahlenbericht 2024*, and the association's standing *Pflegezusatzversicherung* page, read 2026-08-30). **The *Zahlenbericht*'s figures are laid out as infographics, and the contract counts do not survive text extraction in a form safe to attribute**; the counts this file quotes are therefore taken from [S14], which cites them to the PKV-Verband with the classes named.
- Used for: the **negative** market finding, which the retrieved documents confirm rather than soften. The *Zahlenbericht*'s own product taxonomy for *Zusatzversicherungen* runs *Krankentagegeld*, *Krankenhaustagegeld*, *Pflegezusatzversicherung*, *Geförderte Pflegezusatzversicherung* — a **health-branch** list with no annuity line. The association's consumer page describes exactly three forms of *Pflegezusatzversicherung* — *Pflegetagegeld*, *Pflegekosten* and *Pflege-Bahr* — and **does not mention *Pflegerentenversicherung* at all**, because it is life business and outside the PKV's perimeter. So the only counting of German private LTC top-up cover published on the **health** side counts health-insurance contracts, by insured persons per class, and a *Pflegerente* is not in it — which is the negative finding this entry exists to make, and it survives. **What does not survive is the conclusion the file used to draw from it.** The count exists; it is published on the **life** side, by the GDV, and it is at [R22]. Read this entry together with [R21] and [R22]: the PKV series is silent about the product, the GDV series is not.

---

## Regulatory and actuarial references (product research numbering)

The statutes below are read as **canonical XML** from gesetze-im-internet, which carries the law's
`Stand`. The per-section `__NNN.html` addresses are kept as the human-facing link and are **not**
what was read: they answer 200 with a frameset shell of a few kilobytes containing no statutory
text, and two of them (`__14.html`, `__43.html`) refused the connection outright on 2026-08-30.
Non-statutory entries below carry their own retrieval line.

(delib-pflegerentenversicherung-r1)=

### R1 — SGB XI, *Elftes Buch Sozialgesetzbuch — Soziale Pflegeversicherung*
- Publisher / doc type: Bundesministerium der Justiz / juris; statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/` (index page, 64 kB, retrieved). Text read from `https://www.gesetze-im-internet.de/sgb_11/xml.zip`.
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 2c G v. 24.7.2026 I Nr. 228; read 2026-08-30).
- Used for: the statute that creates the first layer, and the two design principles the whole product rests on — **membership follows health insurance**, so the layer is universal, and the scheme is a ***Teilleistungssystem***, paying defined amounts per *Pflegegrad* rather than the cost of care, with the residue falling on the insured person. One provision now carries real weight for the product documents: **§ 30 (*Dynamisierung*)**, which raised the Fourth Chapter's benefit amounts by **4,5 %** on 1 January 2025 and schedules the next rise for **1 January 2028**, indexed to *"[dem] kumulierten Anstieg der Kerninflationsrate in den letzten drei Kalenderjahren"* and capped at wage growth. That settles a question the documents left open: **the 2025 amounts were still the amounts in force in 2026**, and the uprating is episodic by design, on a three-year step. The *Beitragssatz* figures in the regulatory-context section are not from this reading and stay `[unverified]`.

(delib-pflegerentenversicherung-r2)=

### R2 — SGB XI §§ 14 and 15 — *Begriff der Pflegebedürftigkeit* and the *Pflegegrade*
- Publisher / doc type: Bundesministerium der Justiz / juris; statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/__14.html`, `.../__15.html` (human-facing; `__14.html` refused the connection on 2026-08-30, `__15.html` returns a 13 kB shell). Text read from the law's XML.
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 2c G v. 24.7.2026 I Nr. 228; read 2026-08-30).
- Used for: **the insured event of this product**, and every number the documents print from it is now checked. § 14 Abs. 1 defines *Pflegebedürftigkeit* by *"gesundheitlich bedingte Beeinträchtigungen der Selbständigkeit oder der Fähigkeiten"* which must exist *"auf Dauer, voraussichtlich für mindestens sechs Monate"* — not by minutes of care time, which is what brings cognitive and psychiatric impairment into the assessment on equal terms (§ 14 Abs. 2 Nrn. 2 and 3). § 15 Abs. 2 fixes the **module weights at 10 / 15 / 40 / 20 / 15 %** — Mobilität; the higher of *kognitive und kommunikative Fähigkeiten* or *Verhaltensweisen und psychische Problemlagen*, which share one weighted score under Abs. 3; *Selbstversorgung*; *Bewältigung … krankheits- oder therapiebedingter Anforderungen*; *Gestaltung des Alltagslebens* — and § 15 Abs. 3 the **grade thresholds at 12,5 / 27 / 47,5 / 70 / 90 of 100 total points**. § 15 Abs. 4 carries the *besondere Bedarfskonstellationen* route into grade 5 below 90 points. **All of those tags are removed.** The consequence the model turns on: **the private insurer does not define the insured event and does not assess the claim**, and a *Pflegegrad* is a step function of a continuous state, re-assessed episodically — which is exactly the discrete-state, discrete-time chain `Pflege_DE_S` implements. **What the retrieved wordings correct** is the second half of that sentence as it used to stand: the definition risk is *not* one "no wording can hedge". Both retrieved wordings hedge it, and by the same device — MB/PPV and MB/EPV copy the §§ 14–15 text into the conditions [S1] [S2], and IDEAL's AB-IPR-2022A § 8 pins it to *"den Stand vom 28.03.2021"* and offers a self-contained *Punktesystem* as an alternative [S4]. What no wording can hedge is drift in **assessment practice** under a fixed text [R6], and the risk that a pinned definition parts company with the social insurance the customer actually receives.

(delib-pflegerentenversicherung-r3)=

### R3 — SGB XI §§ 36, 37, 38 — *Pflegesachleistung*, *Pflegegeld*, *Kombinationsleistung*
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/__36.html`, `.../__37.html`, `.../__38.html` (human-facing shells of 7–8 kB). Text read from the law's XML.
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 2c G v. 24.7.2026 I Nr. 228; read 2026-08-30).
- Used for: the first-layer benefits for **care at home**, and the amounts are now read rather than recalled. § 36 Abs. 3: *häusliche Pflegehilfe* up to **796 / 1 497 / 1 859 / 2 299 €** a month at grades 2 to 5. § 37 Abs. 1: *Pflegegeld* **347 / 599 / 800 / 990 €**. Both tables are confirmed exactly as the product specification prints them, and the tags come off. **One claim is corrected**: the *Pflegegeld* is not *"about 44 %"* of the corresponding *Sachleistung* at every grade — the four ratios are **43,6 / 40,0 / 43,0 / 43,1 %**, so the honest statement is *between 40 % and 44 %*. § 36 Abs. 1 and § 37 Abs. 1 both open *"Pflegebedürftige der Pflegegrade 2 bis 5"*, which is the statutory fact behind ***Pflegegrad* 1 receiving neither** and behind the `[std]` decision to insure nothing at grade 1 on the `delib_std` *Leistungsstaffel*. § 38 carries the pro-rata combination.

(delib-pflegerentenversicherung-r4)=

### R4 — SGB XI § 43 (*vollstationäre Pflege*) and § 43c (*Leistungszuschläge*)
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/__43.html`, `.../__43c.html` (human-facing; `__43.html` refused the connection on 2026-08-30). Text read from the law's XML.
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 2c G v. 24.7.2026 I Nr. 228; read 2026-08-30).
- Used for: **the arithmetic of the *Versorgungslücke*, which is the number the product is sized against**, and this reading changes one figure in the product specification. § 43 Abs. 2 confines the *Pflegekasse* to *"die pflegebedingten Aufwendungen einschließlich der Aufwendungen für Betreuung und die Aufwendungen für Leistungen der medizinischen Behandlungspflege"* at **805 / 1 319 / 1 855 / 2 096 €** a month for grades 2 to 5 — confirmed exactly — leaving *Unterkunft und Verpflegung*, *Investitionskosten* and the *Ausbildungsumlage* to the resident and the care-cost residue as the *einrichtungseinheitlicher Eigenanteil*. **The correction: § 43 Abs. 3 sets the grade-1 residential *Zuschuss* at 131 €, not 125 €** — *"einen Zuschuss in Höhe von 131 Euro monatlich"* — the same figure as the § 45b *Entlastungsbetrag* [R5], which is very likely where the old 125 € came from. § 43c confirms the *Leistungszuschläge* at **15 / 30 / 50 / 75 %** of the resident's own care-cost share for up to twelve months, more than twelve, more than twenty-four and more than thirty-six months of benefit — exactly the four steps the specification prints, and the reason the *Eigenanteil* is **highest in the first year** so that a constant annuity progressively over-covers the gap.

(delib-pflegerentenversicherung-r5)=

### R5 — SGB XI § 45b (*Entlastungsbetrag*), § 39 (*Verhinderungspflege*), § 42 (*Kurzzeitpflege*)
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/__45b.html`, `.../__39.html`, `.../__42.html` (human-facing shells). Text read from the law's XML, together with § 42a.
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 2c G v. 24.7.2026 I Nr. 228; read 2026-08-30).
- Used for: the secondary first-layer heads, and the statement that **they do not close the residential funding gap** is now made with the amounts. § 45b Abs. 1: an *Entlastungsbetrag* of *"bis zu 131 Euro monatlich"*, earmarked, for *Pflegebedürftige in häuslicher Pflege* — **so it is a home-care benefit, not one "available in every grade including 1" in every setting**, and the tag comes off with that correction. § 42a Abs. 1: *Verhinderungspflege* (§ 39) and *Kurzzeitpflege* (§ 42) are merged into a *Gemeinsamer Jahresbetrag* of **bis zu 3 539 €** a calendar year for grades 2 to 5. Both are annual or earmarked amounts an order of magnitude below the residential gap [R20], which is the point the entry exists to support.

(delib-pflegerentenversicherung-r6)=

### R6 — SGB XI § 18 (*Begutachtung*) and the *Begutachtungs-Richtlinien* (BRi) of the GKV-Spitzenverband
- Publisher / doc type: statute, and the *Begutachtungs-Richtlinien* issued under it; the operational instrument is the *Neues Begutachtungsassessment* (NBA). **The entry's attribution of the BRi to the GKV-Spitzenverband is wrong and is corrected here**: § 17 Abs. 1 SGB XI gives the power to the ***Medizinischer Dienst Bund***, *"im Benehmen mit dem Spitzenverband Bund der Pflegekassen"* and after consulting, among others, the *Verband der privaten Krankenversicherung e. V.*
- URL: `https://www.gesetze-im-internet.de/sgb_11/` for §§ 17 and 18; the BRi themselves are issued by the Medizinischer Dienst Bund and were not retrieved.
- Retrieved: **statute yes** (canonical XML, §§ 17 and 18, Stand: zuletzt geändert durch Art. 2c G v. 24.7.2026 I Nr. 228; read 2026-08-30). **BRi no** — not retrieved, so no BRi criterion, orientation value or version is cited anywhere.
- Used for: **why this product's claims administration is cheap and its basis risk is not.** § 18 Abs. 1: the *Pflegekassen* commission *"den Medizinischen Dienst oder andere unabhängige Gutachterinnen und Gutachter"* — for the privately insured, MEDICPROOF — so the determination is made by a body that is **not the private insurer**, and the private insurer ordinarily accepts it. The retrieved life wording does exactly that: the policyholder sends the *Gutachten des Versicherungsträgers der Pflegepflichtversicherung* and the insurer decides on it [S4]. The BGH put the same trade in terms in *IV ZR 126/23* (30 April 2025): the insured is spared *"einer zusätzlichen, oftmals belastenden Begutachtung"* while the insurer *"macht sich die[n] Sachverstand des Medizinischen Dienstes … zunutze und erspart die mit einer erneuten Begutachtung verbundenen Aufwendungen"* [REG-R36]. Four consequences the documents carry: the *Nachprüfung* is a documentation exercise rather than the adversarial re-assessment that drives a *Berufsunfähigkeitsrente*'s claims cost, which is why `claim_expense_pp` is set low; the insurer carries **assessment-regime risk**, since any loosening of the BRi raises incidence with no contractual change; a *Höherstufung* is applied for and re-assessed, so grade change is **biometric** in the model rather than elective; and a person sits at a grade until re-assessed, which is what makes the Markov representation a match rather than an approximation.

(delib-pflegerentenversicherung-r7)=

### R7 — SGB XI § 23 — *private Pflegepflichtversicherung*
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/__23.html` (human-facing, 9 kB shell). Text read from the law's XML.
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 2c G v. 24.7.2026 I Nr. 228; read 2026-08-30).
- Used for: one definitional point with a direct modelling consequence — that everyone in the *private Krankenversicherung* must hold a private LTC cover at least equivalent to the SPV's, so **the first layer is the same size for a privately insured person as for a statutorily insured one**, the *Versorgungslücke* is the same for both populations, and `Pflege_DE_S` needs no separate PPV variant.

(delib-pflegerentenversicherung-r8)=

### R8 — SGB XI §§ 126–130, in particular § 127 — *Pflege-Bahr*
- Publisher / doc type: statute (the state-subsidised private LTC top-up introduced by the *Pflege-Neuausrichtungs-Gesetz*).
- URL: `https://www.gesetze-im-internet.de/sgb_11/__127.html` (human-facing, 8 kB shell). Text read from the law's XML, §§ 126–130.
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 2c G v. 24.7.2026 I Nr. 228; read 2026-08-30).
- Used for: two things this product needs, **and the first of them was wrong.**

  **Correction 1 — there is no statutory 10 / 20 / 30 / 40 / 100 % grid.** § 127 Abs. 2 Nr. 4 requires only *"einen vertraglichen Anspruch auf Auszahlung von Geldleistungen für jeden der in § 15 Absatz 3 und 7 aufgeführten Pflegegrade, dabei in Höhe von mindestens 600 Euro für Pflegegrad 5"*, capped so that the tariff benefit *"die zum Zeitpunkt des Vertragsabschlusses jeweils geltende Höhe der Leistungen dieses Buches nicht überschreiten"* may, with indexation to general inflation permitted and *"weitere Leistungen darf der förderfähige Tarif nicht vorsehen"*. That is a **benefit at every grade, a floor at grade 5 and a ceiling at the SGB XI benefit level** — not a percentage schedule. The 10 / 20 / 30 / 40 / 100 shape is a market convention, and the instrument that could fix it is the *brancheneinheitliche Vertragsmuster* the PKV-Verband is **beliehen** to lay down under § 127 Abs. 2 Satz 2 — a document this library has not retrieved. **The `bahr` schedule in `benefit_scale_table.csv` therefore has no statutory citation and is a `[std]` construction like the others**; that is a model-affecting finding and is reported, not silently changed.

  **Correction 2 — § 127 nowhere says *Pflegetagegeld*.** The conclusion survives, the reason changes. Abs. 2 Nr. 1 requires the tariff to provide *"die Kalkulation nach Art der Lebensversicherung gemäß § 146 Absatz 1 Nummer 1 und 2 des Versicherungsaufsichtsgesetzes"* — and § 146 VAG is the **health-insurance** provision, whose Nr. 2 requires *"die Alterungsrückstellung nach § 341f des Handelsgesetzbuchs"*. A *Pflegerentenversicherung* is life business with a *Deckungsrückstellung* under the DeckRV and forms no *Alterungsrückstellung*; and Nr. 4's *"weitere Leistungen darf der förderfähige Tarif nicht vorsehen"* rules out the death benefit and surrender value a *Pflegerente* carries. So ***a Pflegerentenversicherung still cannot be a geförderter Tarif***, and delib still does not implement the *Zulage*.

  **What is confirmed:** the *Zulage* of *"monatlich 5 Euro"* against a minimum contribution of *"monatlich 10 Euro"* (Abs. 1); the *Kontrahierungszwang* and the ban on underwriting (Abs. 2 Nrn. 2 and 3 — a right to insurance for everyone in § 126, and a waiver of *"eine Risikoprüfung und die Vereinbarung von Risikozuschlägen und Leistungsausschlüssen"*); the *Wartezeit* *"auf höchstens fünf Jahre"* (Nr. 6); and the tie of the claim decision to the §§ 18–18c determination (Nr. 5). All four tags come off. The no-underwriting design remains the market's natural experiment on anti-selection, and [S12] now supplies the market's own reading of it.

(delib-pflegerentenversicherung-r9)=

### R9 — *Zweites Pflegestärkungsgesetz* (PSG II)
- Publisher / doc type: reform act, *Zweites Gesetz zur Stärkung der pflegerischen Versorgung und zur Änderung weiterer Vorschriften* **vom 21. Dezember 2015, BGBl. I S. 2424**; the operative changes took effect **1 January 2017**.
- URL: not retrieved as an act. Its content is read where it now lives — SGB XI §§ 14, 15 and 140 as consolidated [R2] — and its citation, date and effect are taken from two retrieved documents that state them: BGH *IV ZR 126/23* of 30 April 2025 and the DAV's *Ergebnisbericht* of 15 January 2025 [R15].
- Retrieved: **indirectly.** The act itself was not opened; **its identifying citation and its effect are no longer `[unverified]`**, because both retrieved documents recite them, the BGH with the *Bundesgesetzblatt* reference.
- Used for: **the structural break that is the largest basis risk in the product**, and every limb of it is now sourced. The act replaced the three *Pflegestufen* with the five *Pflegegrade*, replaced the time-based assessment with the NBA [R6], and introduced the *einrichtungseinheitlicher Eigenanteil* [R4]. **The insured population widened**: the BGH holds that *"[d]urch das Zweite Pflegestärkungsgesetz sind nicht nur der Begriff der Pflegebedürftigkeit, sondern auch seine Definition in den §§ 14, 15 SGB XI gegenüber dem zuvor geltenden Recht deutlich erweitert worden"*, the criteria of § 14 Abs. 2 Nrn. 2 and 3 now scoring what used to count only as *erheblich eingeschränkte Alltagskompetenz* under § 45a a.F. **The series break is measured**: Destatis attributes part of the +730 000 (+15 %) rise in *Pflegebedürftige* between end-2021 and end-2023 to the wider concept, against a demographic expectation of about +100 000 [R18]. **The transitional mapping is § 140 SGB XI**, and the BGH's holding on it is the point [REG-R36]: overleitung does not license the reverse inference, because § 140 Abs. 2 Satz 3 Nr. 2 Buchst. a moves people with *erheblich eingeschränkte Alltagskompetenz* into grade 2 **without any prior Pflegestufe at all**. It remains the reason `Pflege_DE_S` ships an explicitly labelled `[std]` proxy — but see [R15], where the actuarial profession's own response to the break turns out to be public.

(delib-pflegerentenversicherung-r10)=

### R10 — *Pflegeunterstützungs- und -entlastungsgesetz* (PUEG)
- Publisher / doc type: financing and benefit act, 2023.
- URL: not retrieved as an act; its operative content is read where it now lives, in SGB XI as consolidated.
- Retrieved: **no** as an act. **The mechanism it installed is retrieved**: SGB XI § 30 (*Dynamisierung*), canonical XML, Stand: zuletzt geändert durch Art. 2c G v. 24.7.2026 I Nr. 228.
- Used for: the point that the statutory amounts are uprated **episodically by legislation** while the *Eigenanteil* rises every year [R20] — every uprating a one-off catch-up against a continuous drift. **Both halves are now sourced, and the open question is closed.** § 30 Abs. 1 raised the Fourth Chapter's amounts by **4,5 % on 1 January 2025** and schedules the next rise for **1 January 2028**; nothing took effect on 1 January 2026, and the §§ 36, 37, 43, 43c, 45b and 42a amounts read on 2026-08-30 are the 2025 amounts still. Against that, the vdek series has the residential *Eigenanteil* rising **+261 € (nine per cent) in the twelve months to 1 January 2026** alone [R20]. **A three-year statutory step against a nine-per-cent annual drift** is the asymmetry, quantified, and it is the structural argument for the *Leistungsdynamik* option that model point 8 switches on.

(delib-pflegerentenversicherung-r11)=

### R11 — VVG — the contract-law provisions this product runs on
- Publisher / doc type: Bundesministerium der Justiz / juris; statute (§§ 7, 19, 21, 152, 153, 155, 163, 165, 169, 176, 203), with the VVG-InfoV beside it.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` and siblings are the human-facing links and are shells of about 7 kB. Text read from `https://www.gesetze-im-internet.de/vvg_2008/xml.zip` and `.../vvg-infov/xml.zip`.
- Retrieved: **yes** (canonical XML; VVG Stand: zuletzt geändert durch Art. 12 G v. 26.5.2026 I Nr. 156, VVG-InfoV Stand: zuletzt geändert durch Art. 13 G v. 26.5.2026 I Nr. 156; read 2026-08-30).
- Used for: **the product's whole contractual frame, and the comparison that defines it.** § 163 Abs. 1 is the only route by which a life insurer may adjust a premium, and the retrieved text gives all three conditions and the exclusion: the *Leistungsbedarf* must have changed *"nicht nur vorübergehend und nicht voraussehbar"*, the new premium must be *"angemessen und erforderlich … um die dauernde Erfüllbarkeit der Versicherungsleistung zu gewährleisten"*, and *"ein unabhängiger Treuhänder"* must confirm both — with re-setting excluded where the benefits were under-calculated and *"ein ordentlicher und gewissenhafter Aktuar dies … hätte erkennen müssen"*. **§ 203, the health-insurance *Beitragsanpassung*, does not apply**, which is the single load-bearing difference between a *Pflegerente* and a *Pflegetagegeld* and the reason the *Pflegerente* costs more; [S12] states the same trade in consumer terms, and the retrieved life wording recites § 163 almost word for word [S4]. Also: § 7 with the VVG-InfoV for the pre-contractual duties [S5] [S7]; § 19 for the *vorvertragliche Anzeigepflicht* with the **§ 21 Abs. 3 time bar — five years, ten *"[h]at der Versicherungsnehmer die Anzeigepflicht vorsätzlich oder arglistig verletzt"*** (tag removed), which confines the *Gesundheitsprüfung*'s effect on incidence to the first decade of a contract whose claims arrive forty years out; § 152 Abs. 1 for the **30-day** *Widerrufsfrist*; § 153 for the *Überschussbeteiligung* the base run omits; § 165 for the *Beitragsfreistellung*; § 169 for the *Rückkaufswert*; and § 155 for the *Standmitteilung* [S8].

  **The § 169 question is restated, because the entry described the provision wrongly.** There is no "§ 169 exception for covers paying only on death". § 169 Abs. 1 is a **positive scope test**: the *Rückkaufswert* is owed on *"eine Versicherung, die Versicherungsschutz für ein Risiko bietet, bei dem der **Eintritt der Verpflichtung des Versicherers gewiss ist**"*. A *Risikolebensversicherung* falls outside it because the obligation is not certain to arise — and on its face a pure-risk *Pflegerente* does not satisfy the test either. § 176 extends §§ 150–170 *entsprechend* to the *Berufsunfähigkeitsversicherung* and to nothing else. The **same certainty test** governs the *Effektivkosten* duty in § 2 Abs. 1 Nr. 9 VVG-InfoV [S7], so the two questions are one question. **The statutory question stays open**, and the documents keep it open — but it is now informed by a carrier's answer: IDEAL grants a guaranteed *Rückkaufswert* *"nach § 169 des Versicherungsvertragsgesetzes"*, five-year spread floor included, on a product its own conditions call *"eine reine Risikoversicherung ohne Sparprozess"* [S4]. Whether that is the statute applying or the carrier conceding, the documents do not decide.

(delib-pflegerentenversicherung-r12)=

### R12 — VAG §§ 138, 139, 146, and § 341f HGB
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/vag_2016/` (index page, 88 kB, retrieved). Text read from `.../vag_2016/xml.zip` and `.../hgb/xml.zip`.
- Retrieved: **yes** (canonical XML; VAG Stand: zuletzt geändert durch Art. 25 G v. 25.3.2026 I Nr. 81; HGB read from its own XML; read 2026-08-30).
- Used for: § 138 Abs. 1 VAG, which requires life premiums to be calculated *"unter Zugrundelegung angemessener versicherungsmathematischer Annahmen"* and to be *"so hoch …, dass das Lebensversicherungsunternehmen allen seinen Verpflichtungen nachkommen und insbesondere für die einzelnen Verträge ausreichende Deckungsrückstellungen bilden kann"* — the statutory anchor of the five first-order margins in `basis_table.csv`, which bites hardest on the *Pflegewahrscheinlichkeiten*; § 138 Abs. 2 for equal treatment on equal facts, which is the *Gleichbehandlung* limb. § 139 for the *Rückstellung für Beitragsrückerstattung*. **§ 146 to locate the boundary the *Pflegerente* sits on the other side of**: Abs. 1 confines *substitutive Krankenversicherung* to conduct *"nach Art der Lebensversicherung"* with, at Nr. 2, *"die Alterungsrückstellung nach § 341f des Handelsgesetzbuchs"* — and it is precisely those two numbers that § 127 Abs. 2 Nr. 1 SGB XI imports as the *Pflege-Bahr* eligibility test [R8]. § 341f Abs. 1 HGB for the **prospective** *Deckungsrückstellung* the model does not compute, and Abs. 3 for the rule that in health business conducted *nach Art der Lebensversicherung* the *Deckungsrückstellung* **is** the *Alterungsrückstellung* — the single sentence in which the two branches' reserves are told apart.

(delib-pflegerentenversicherung-r13)=

### R13 — DeckRV, *Deckungsrückstellungsverordnung*
- Publisher / doc type: regulation; fixes the *Höchstrechnungszins* and the *Höchstzillmersatz*.
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` (index page, a 6 kB shell — not the text). Text read from `.../deckrv_2016/xml.zip`.
- Retrieved: **yes** (canonical XML, Stand: zuletzt geändert durch Art. 1 V v. 19.7.2024 I Nr. 250 — the amending regulation that set the current rate; read 2026-08-30).
- Used for: the **two cited numbers in the whole pricing basis**, both now read verbatim. § 2 Abs. 1: *"wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen auf **1 Prozent** festgesetzt"*; § 2 Abs. 2: *"gilt der von einem Versicherungsunternehmen zum Zeitpunkt des Vertragsabschlusses verwendete Rechnungszins … für die gesamte Laufzeit des Vertrages"* — so the rate attaches to the cohort at issue, which is what `rechnungszins` models. § 4 Abs. 1: *"Der Zillmersatz darf **25 Promille der Summe aller Prämien** nicht überschreiten"* — confirming both the level `acq_permille` is set exactly at **and its base**, the sum of all premiums rather than the annual premium, which is a listed pitfall. The retrieved carrier wording applies exactly this: *"das Verrechnungsverfahren nach § 4 der Deckungsrückstellungsverordnung … beschränkt [auf] 2,5 % der von Ihnen während der Laufzeit des Vertrags zu zahlenden Beiträge"* [S4]. Tags removed. **What the regulation does not itself state is the date "from 1 January 2025"** — that is the amending regulation's commencement, and it is carried on the `Stand` line above rather than asserted from the text. The rate history the product specification prints is still `[unverified]`. See also [REG-R14], [REG-R15], [REG-R16].

(delib-pflegerentenversicherung-r14)=

### R14 — KVAV, *Krankenversicherungsaufsichtsverordnung*
- Publisher / doc type: the calculation regulation for private health insurance — the *Alterungsrückstellung*, the *Sicherheitszuschlag*, and the *auslösende Faktoren* that trigger a § 203 VVG *Beitragsanpassung*.
- URL: `https://www.gesetze-im-internet.de/kvav/`; text read from `.../kvav/xml.zip`.
- Retrieved: **yes** (canonical XML, 32 sections, Stand: zuletzt geändert durch Art. 6 Abs. 9 G v. 19.12.2018 I 2672; read 2026-08-30). Its counterpart in the *Musterbedingungen* — MB/EPV § 8b, the annual comparison of required against calculated benefits and mortality and the recalculation of every premium in the observation unit on a breach — is retrieved at [S2].
- Used for: **the regime the *Pflegetagegeld* comparison sits under, and never as a rule applying to the modelled product.** It is what makes the competing-forms table's re-rating and ageing-provision rows structural rather than `[unverified]`: a *Pflegetagegeld* is health business calculated under the KVAV, a *Pflegerente* is life business calculated under the DeckRV [R13].

(delib-pflegerentenversicherung-r15)=

### R15 — DAV 2008 P — the German *Pflegetafel*
- Publisher / doc type: Deutsche Aktuarvereinigung e. V. (DAV); standard biometric table with a published derivation paper.
- URL: `https://aktuar.de/content/PDF/Fachwissen/2025-01-15_LV_EB_Herleitung-der-DAV-2008P.pdf` (*Ergebnisbericht des Ausschusses Lebensversicherung — Herleitung der Rechnungsgrundlagen DAV 2008 P für die Pflegerenten(zusatz)versicherung*, Köln, 15 January 2025); `https://aktuar.de/content/PDF/Fachwissen/2025-01-15_LV_EB_Anpassung_DAV2008P_Pflegegrade.pdf` (*Auswirkungen der Pflegereform 2016/2017 auf die Rechnungsgrundlagen DAV2008P*, adopted 10 January 2017, re-adopted 15 January 2025).
- Retrieved: **yes** (both PDFs, 122 pp. and 75 pp., free from the DAV's own site; read 2026-08-30).
- Used for: **the actuarial reference this product turns on — and this pass overturns two claims the entry made about it.**

  **Correction 1 — the bases are public.** The entry said the table *"is the property of the DAV, is not public"*. The DAV publishes the derivation as a free *Ergebnisbericht*, and that report carries the bases themselves in its appendices: *Anhang 1: Rechnungsgrundlagen für die Pflegeversicherung* (p. 85), *Anhang 2: Rechnungsgrundlagen 2. Ordnung* (p. 95), *Anhang 3: Exemplarische Beiträge und Aktivendeckungsrückstellungen* (p. 105). **delib still does not redistribute them and no value from them appears anywhere in this library** — that remains this library's own choice, not a licensing constraint, and the entry now says so honestly.

  **Correction 2 — the *Pflegegrad* vintage problem has been worked.** The entry treated DAV 2008 P as stranded on the superseded *Pflegestufen*. The companion *Ergebnisbericht* does exactly the bridging the entry said was missing: the working group set out *"die Ausscheidewahrscheinlichkeiten der DAV 2008 P so anzupassen, dass sie für neue Pflegerenten(zusatz)versicherungen Anwendung finden können, in denen der neue Pflegebedürftigkeitsbegriff enthalten ist"*, and its § 6.5 prints ***Rechnungsgrundlagen 1. Ordnung für Pflegegrade***. Two things about it matter to this model. It is a ***Stufenmodell*** — bases for *"mindestens Pflegegrad g ist erreicht"*, a threshold structure, **not** a five-state per-grade chain, which is the structure the retrieved carrier product also uses [S4] and **not** the structure `Pflege_DE_S` implements. And the DAV is candid that the underlying data problem is real: *"[z]u Invalidisierungswahrscheinlichkeiten oder gar Invalidensterblichkeiten, für diese fünf Pflegegrade, fehlt naturgemäß jegliche statistische Information"* — the bases are derived from *Pflegestufen* experience through a transition, not observed.

  **What is confirmed:** it is the German market's standard basis for LTC business calculated *nach Art der Lebensversicherung*; it is multi-state, with prevalence, incidence, *Invalidensterblichkeit*, *Aktivensterblichkeit* and *Reaktivierung* all separately derived; and the four properties `model.md` says a replacement must preserve are the properties it has. **What is now also available and was not before** is a published set of prudence loadings for exactly this risk — see the report at [REG-R8] in the note below. See also [REG-R51].

(delib-pflegerentenversicherung-r16)=

### R16 — DAV 2008 T and DAV 2004 R
- Publisher / doc type: DAV; the standard German mortality tables for covers with a death character and for annuities.
- URL: the DAV 2008 T derivation is published at `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf`.
- Retrieved: **no** — the DAV 2008 T derivation was located on the DAV's site on 2026-08-30 but **not opened**, and nothing was located for DAV 2004 R. Neither is needed: this product uses neither table, and the entry exists to say why.
- Used for: two narrow places, and one warning. The **active-life mortality** the shipped Gompertz proxy stands in for is stated to be neither DAV 2008 T nor the DAV 2008 P active-life table, and a *Todesfallleistung* written into a *Pflegerente* is a death cover priced as one. The warning is the one the model's `mort_mult` construction exists to prevent: **DAV 2004 R is built to be prudent about people living *longer*, whereas the annuity in payment on a *Pflegerente* is paid to a heavily impaired population, so using an annuity table here would be prudent in exactly the wrong direction and would materially overprice the benefit.** **Neither table is redistributed here.** See also [REG-R48], [REG-R49].

(delib-pflegerentenversicherung-r18)=

### R18 — Destatis, *Pflegestatistik*
- Publisher / doc type: Statistisches Bundesamt; biennial statutory statistics under SGB XI, reference date 31 December.
- URL: `https://www.destatis.de/DE/Presse/Pressemitteilungen/2024/12/PD24_478_224.html` (press release, 2023 results); `https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/Pflege/Tabellen/pflegebeduerftige-pflegestufe.html` (the *Versorgungsart, Geschlecht und Pflegegrade* table, Stand 18 December 2024). The age-specific *Pflegequoten* are read from a Destatis GENESIS extraction published by sozialpolitik-aktuell.de (`.../PDF-Dateien/abbVI12.pdf`, tables 22421-0001 and 12411-0001).
- Retrieved: **yes** (all three, read 2026-08-30).
- Used for: the prevalence section, and **most of its figures were understated.** Confirmed exactly: **5 688 473** *Pflegebedürftige* at end-2023 against *"knapp 5,0 Millionen"* at end-2021, **+730 000 (+15 %)**; the home/residential split **85,9 % (4 888 882) / 14,1 % (799 591)**; and Destatis's own attribution of much of the rise to the wider § 14 concept [R9], the demographic expectation for 2021→2023 having been *"rund 100 000"*.

  **Correction — the grade distribution.** The stock is **13,8 / 40,4 / 29,6 / 11,8 / 4,3 %** across grades 1 to 5, not the 9 / 44 / 27 / 14 / 6 % the documents printed. The argument the documents build on it survives — `entry_share` should skew lower than the stock — and is if anything strengthened, the two lowest grades now holding 54,2 % of the stock. The table also supplies something the documents did not have: the **residential** grade distribution is **0,5 / 16,6 / 37,3 / 31,1 / 14,3 %**, heavily concentrated in grades 3 to 5, which is direct support for a *Leistungsstaffel* weighted to the upper grades.

  **Correction — the prevalence curve.** The observed *Pflegequoten* for 2023 are **1,2 % (15–60) · 3,6 (60–65) · 5,5 (65–70) · 9,1 (70–75) · 16,4 (75–80) · 30,8 (80–85) · 53,7 (85–90) · 80,2 (90–95) · 94,5 (95+)**. The documents printed *"under 1 % below 60; about 10 % at 75–79; 20 % at 80–84; 40 % at 85–89; 70 % or more at 90 and above"* — **low at every point, by roughly a factor of 1,5 in the seventies and eighties**. The shape claim needs qualifying too: successive five-year ratios are **1,80 · 1,88 · 1,74 · 1,49 · 1,18**, so *"roughly doubles every five years"* holds as an approximation only between about 70 and 90 and breaks down above 90 as the quota saturates. **That matters to the model**, because the incidence proxy's slope is anchored to `ln 2 / 5 = 0.1386`; the observed prevalence slope over 70–90 is nearer `ln 1.8 / 5 = 0.117`. It is reported and not changed — see the note at the end of this file.

(delib-pflegerentenversicherung-r19)=

### R19 — Destatis, *Pflegevorausberechnung*
- Publisher / doc type: Statistisches Bundesamt; official projection of the number of *Pflegebedürftige* (*Pflegevorausberechnung 2023*).
- URL: `https://www.destatis.de/DE/Presse/Pressemitteilungen/2023/03/PD23_124_12.html`
- Retrieved: **yes** (HTML press release, read 2026-08-30).
- Used for: the statement behind the product's commercial case, now with the numbers. On **constant** *Pflegequoten* — pure ageing — the count rises from about 5,0 million at end-2021 to about **5,6 million by 2035 (+14 %)** and **6,8 million by 2055 (+37 %)**, flattening thereafter at about 6,9 million in 2070. **The 6,8 million for 2055 the product specification prints is confirmed exactly and the tag comes off.** A second variant, letting the post-2017 rise in *Pflegequoten* continue in damped form to 2027, gives **6,3 million in 2035 and 7,6 million in 2055 (+53 %)**. The share aged 80 and over rises from 55 % to about 65 %, mostly between 2035 and 2055 — which is the cohort a contract written today at entry age 45 is priced into.

(delib-pflegerentenversicherung-r20)=

### R20 — vdek and BMG material on the *Eigenanteil* in *Pflegeheimen*
- Publisher / doc type: Verband der Ersatzkassen e. V.; the twice-yearly evaluation of the average resident payment by component. Nothing was retrieved from the Bundesministerium für Gesundheit.
- URL: `https://www.vdek.com/presse/pressemitteilungen/2026/eigenanteile-pflegeheim-auswertung/_jcr_content/par/download/file.res/vdek_pm_20260122_Eigenanteile_Pflege.pdf`
- Retrieved: **yes** (PDF, 4 pp., press release of 22 January 2026 on the evaluation as at 1 January 2026; read 2026-08-30).
- Used for: the **level and the structure** of the number the product is sold against, and this is the single largest evidential gain in the product. **The levels, as at 1 January 2026**: total monthly *Eigenbeteiligung* in the first year of a stay **3 245 €** on a national average, up **261 € (nine per cent)** on the year; of which the *einrichtungseinheitlicher Eigenanteil* including *Ausbildungskosten* **1 685 €**, *Unterkunft und Verpflegung* **1 046 €**, and *Investitionskosten* the residual **514 €** (the release prices the *Investitionskosten* relief at 514 € and the *Ausbildungskosten* relief at a further 124 € a month). At the previous reading, 1 July 2025, the total had *"zum ersten Mal die 3.000-Euro-Marke überschritten"* at about 3 108 €, and at 1 January 2025 it was 2 871 €. **The structure**: the release describes *"drei Komponenten"*, folding the *Ausbildungskosten* **into** the EEE rather than listing them as a fourth head, and confirms that only the EEE carries the § 43c *Zuschuss* — *"15 Prozent Zuschuss im ersten Jahr, 30 Prozent im zweiten, 50 Prozent im dritten und 75 Prozent ab dem vierten Aufenthaltsjahr"* — while *Investitionskosten* are *"für alle Pflegeheimbewohnenden in einer Einrichtung - unabhängig von der Aufenthaltsdauer - gleich hoch"*. **These figures stop being the least reliable numbers in the research and become the best-sourced.** They still argue only the order of magnitude of the `[std]` *vereinbarte Rente* of 1 000,00 €, and on the retrieved 2026 level that annuity covers under a third of the first-year gap.

(delib-pflegerentenversicherung-r21)=

### R21 — PKV-Verband statistics on *Pflegezusatzversicherung* and *Pflege-Bahr*
- Publisher / doc type: PKV-Verband; annual counts of subsidised and unsubsidised private LTC top-up contracts.
- URL: the association's own series is at `https://www.pkv.de/fileadmin/user_upload/PKV/3_PDFs/Publikationen/Zahlenbericht_2024.pdf` [S16]; the counts quoted here are read from Assekurata's April 2026 study, which cites them to the PKV-Verband with the classes named [S14].
- Retrieved: **yes, indirectly** (via [S14], read 2026-08-30). See [S16] on why the *Zahlenbericht*'s own infographic layout is not quoted directly.
- Used for: the same counting as [S16], from the regulatory-reference side. **End-2024**: *Pflegetagegeld* **3 021 300** insured, *Pflege-Bahr* **890 091**, *Pflegekosten* **366 100**, against about **4,5 million** persons — **5,4 % of the population** — with any *Pflegezusatzversicherung*. That confirms the product specification's *"of the order of 3,5 to 4,5 million, of which 0,8 to 0,9 million subsidised"* and the tag comes off. The structural finding also holds and is now stated in the source: *"stagnieren die Bestandszuwächse in der Pflegezusatzversicherung in den vergangenen Jahren"*, with the unsubsidised market about three and a half times the *Pflege-Bahr* book.

(delib-pflegerentenversicherung-r22)=

### R22 — GDV life-market statistics
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V.; the annual life-market series — new business and in force by product family, premium income, the *Stornoquote*.
- URL: `https://www.gdv.de/resource/blob/180978/b8ae8eb0b1bf4b15e7cc3354bc231af9/die-deutsche-lebensversicherung-in-zahlen-2024-publikation-pdf-data.pdf` (*Die deutsche Lebensversicherung in Zahlen 2024*).
- Retrieved: **yes** (PDF, read 2026-08-30).
- Used for: **this entry's whole point is reversed, and it is the largest single correction of the pass.** The GDV **does** carve out ***Pflegerentenversicherungen*** as a reported product family, in every table — new business, in-force *Hauptversicherungen*, and *Zusatzversicherungen* separately. At **31 December 2023**:

  | | Contracts | Laufender Beitrag / year | Versicherte Summe |
  |---|---|---|---|
  | *Pflegerentenversicherungen*, main cover | **242 000** (0,3 % of 81,4 m) | **177 Mio. €** (0,3 %) | 29 737 Mio. € (0,8 %) |
  | *Pflegerenten-Zusatzversicherungen* | **762 400** (of 20,7 m riders) | — | 84 218 Mio. € |

  New business 2023 was **5 499** *eingelöste* policies, 0,2 % of the life market by count. **So there is a sourced count of German *Pflegerente* contracts in force**, the claim that there is none is withdrawn from this entry, and research gap 12 is closed. Two readings follow. The product is **an order of magnitude smaller as a stand-alone than as a rider** — three riders for every stand-alone contract — which the composite specification, a stand-alone design, should be read against. And 177 Mio. € over 242 000 contracts is an **average in-force premium of about 61 € a month**, which sits inside the argued 50–100 € band at entry age 45 [S9] — a genuine, if crude, external check on a number that previously had none. See also [REG-R53].

(delib-pflegerentenversicherung-r23)=

### R23 — EStG — the tax provisions
- Publisher / doc type: statute (§ 10 Abs. 1 Nr. 3 and Nr. 3a with Abs. 4; § 3 Nr. 1a; § 22 Nr. 1; § 20 Abs. 1 Nr. 6). No BMF administrative guidance was retrieved.
- URL: `https://www.gesetze-im-internet.de/estg/` (index page, 57 kB, retrieved). Text read from `.../estg/xml.zip`.
- Retrieved: **yes** (canonical XML, read 2026-08-30). BMF guidance: **no**.
- Used for: two statements the product specification has to make honestly, and the first of them is now **fully sourced**. On **premiums**: § 10 Abs. 1 Nr. 3a covers *"Beiträge zu Kranken- und Pflegeversicherungen, soweit diese nicht nach Nummer 3 zu berücksichtigen sind"* — so a private *Pflegerenten* premium is a *sonstige Vorsorgeaufwendung*; § 10 Abs. 4 Satz 1 caps Nr. 3 and Nr. 3a together at **2 800 €** a year, Satz 2 at **1 900 €** for taxpayers with an employer or public contribution to their health cover; and **Satz 4 is the operative sentence**: *"Übersteigen die Vorsorgeaufwendungen im Sinne des Absatzes 1 Nummer 3 die nach den Sätzen 1 bis 3 zu berücksichtigenden Vorsorgeaufwendungen, sind diese abzuziehen und ein Abzug von Vorsorgeaufwendungen im Sinne des Absatzes 1 **Nummer 3a scheidet aus**."* The compulsory health and LTC contributions of Nr. 3 exhaust the ceiling for most employees on their own, so **for most buyers the premium is not deductible at all** — not merely partly. Tags removed, and this is also why the *Pflege-Bahr* subsidy [R8] is a direct payment rather than a further deduction. On **benefits**: § 3 Nr. 1a exempts *"Leistungen aus einer Krankenversicherung, aus einer Pflegeversicherung und aus der gesetzlichen Unfallversicherung"*, and the statute does not say whether a life-branch *Pflegerente* is a *"Pflegeversicherung"* for that purpose; the competing *Ertragsanteil* analysis under § 22 Nr. 1 is equally untested on the retrieved text. **This corpus still cannot say which governs**, and the tag stays with that reason: the statute is silent on the point, and no administrative guidance or authority was retrieved. delib does not model benefit taxation. See also [REG-R41], [REG-R45].

(delib-pflegerentenversicherung-r24)=

### R24 — SGB XII §§ 61–66 (*Hilfe zur Pflege*) and the *Angehörigen-Entlastungsgesetz*
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/sgb_12/` (index page, 48 kB, retrieved). Text read from `.../sgb_12/xml.zip`.
- Retrieved: **yes** (canonical XML, 197 sections, Stand: zuletzt geändert durch Art. 2d G v. 24.7.2026 I Nr. 228; read 2026-08-30). § 61 confirms the means test — *Hilfe zur Pflege* is owed only *"soweit ihnen und ihren nicht getrennt lebenden Ehegatten oder Lebenspartnern nicht zuzumuten ist, dass sie die … Mittel aus dem Einkommen und Vermögen … aufbringen"* — and § 61a carries the SGB XI definition of *Pflegebedürftigkeit* across, so the third layer and the backstop share one trigger. The *Angehörigen-Entlastungsgesetz* itself was not retrieved and its thresholds stay `[unverified]`.
- Used for: the means-tested backstop that completes the three-layer picture, and two consequences the documents draw from it. **A private *Pflegerente* with a *Rückkaufswert* is realisable assets** in the means test before a claim, and the annuity is income during it, so a contract with no surrender value is on that reasoning the more robust design for a buyer whose likely destination is social assistance — an argument for the pure-risk variant that has nothing to do with price. And the *Angehörigen-Entlastungsgesetz* removed the *Elternunterhalt* motive for all but high-earning families, which is one of the reasons the documents give for low market penetration. Every threshold and date is `[unverified]`.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen;
research provenance in `_research/regulatory-actuarial.md`). **That page's own retrieval status is
maintained there and is not restated here.** What the bullets below record is what *this* product's
retrieval established about the instruments those tags point to; where a bullet used to assert an
absence that a document retrieved for this product contradicts, the bullet now says so. Entries
cited by the *Pflegerentenversicherung* documents:

- **REG-R1 / REG-R2 / REG-R3 / REG-R4 / REG-R6** — Solvabilität II, the Delegated Regulation, the 2025 review, the EIOPA risk-free curves and VAG §§ 74–110: the valuation layer that consumes `liability_cf`, cited and never computed. A best estimate is `Σ v(t) liability_cf(t)` plus a risk margin, and **nothing in this library discounts**.
- **REG-R5** — VAG 2016 and its Anlage 1: the *Sparten* boundary that puts a *Pflegerente* in life and a *Pflegetagegeld* in health, which is the whole of [S2] and [R14] restated at statute level.
- **REG-R8** — VAG § 138, *Prämienkalkulation* and *Gleichbehandlung*: the premium-sufficiency requirement that the five first-order margins in `basis_table.csv` answer to; § 138 Abs. 1 is quoted at [R12]. **This bullet used to say that no German *Sicherheitszuschlag* level for a *Pflegetafel* was established. That is no longer true.** The DAV's *Ergebnisbericht* on the *Pflegereform* [R15] publishes them, by minimum *Pflegegrad*: on **incidence**, a *Gesamtzuschlag* of **24,5 / 21,4 / 20,5 / 24,0 / 31,2 %** for PG ≥ 1 to PG = 5 (an *Änderungszuschlag* of 15 / 12 / 10 / 10 / 10 % compounded with a *Schwankungszuschlag* of 8,3 / 8,4 / 9,5 / 12,7 / 19,3 %); on ***Invalidensterblichkeit***, a *Gesamtabschlag* of **28,5 / 24,2 / 24,2 / 24,3 / 25,7 %**; and on ***Aktivensterblichkeit*** a *Gesamtabschlag* of **13,6 %**, carried over unchanged from DAV 2008 P. delib's shipped margins — `inc_margin` 1.25, `care_mort_margin` 0.85, `act_mort_margin` 0.90 — are still `[std]`, and the comparison is reported rather than acted on: see the note at the end of this file.
- **REG-R9 / REG-R10 / REG-R18 / REG-R19** — VAG §§ 139, 140 and 145, the MindZV and the RfBV: the surplus machinery the base run deliberately omits, recorded so that a user adding an *Überschussbeteiligung* knows which regime it sits under.
- **REG-R11** — VAG §§ 141–143: the *Verantwortlicher Aktuar* and the *Treuhänder*, the office that in practice sets the prudence margins this model ships as `[std]` numbers.
- **REG-R14 / REG-R15** — the DeckRV and the *Höchstrechnungszins* rate history: the **1,00 %** for new business from 1 January 2025 that `rechnungszins` carries and the equivalence discounts at — the one genuinely cited pricing assumption in the model.
- **REG-R16 / REG-R20** — DeckRV § 4 *Höchstzillmersätze* and the LVRG cut from 40 ‰ to 25 ‰: the ceiling `acq_permille` sits **exactly at**, so the ceiling binds visibly, and the reason `surrender_table.csv`'s first two years are zero.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins*, the *Zinszusatzreserve* and the *Korridormethode*: named in the valuation pointers as a reserve this model does not compute.
- **REG-R23** — VVG §§ 8 and 152, the 14-day and 30-day *Widerrufsrechte*: absorbed into the first-year lapse rate rather than modelled.
- **REG-R24** — VVG § 153, the *Überschussbeteiligung* and the *hälftige Beteiligung an den Bewertungsreserven*: the article-level carrier for [R11]'s surplus limb, and why a biometric-risk product's surplus is dominated by the *Risikoergebnis*.
- **REG-R25** — VVG §§ 154 and 155, the *Modellrechnung* and the *Standmitteilung*: the article-level carrier for [S8].
- **REG-R27** — VVG § 163, *Prämien- und Leistungsänderung*: **the whole of a *Lebensversicherer*'s re-rating power**, and the provision the product's central commercial claim rests on.
- **REG-R28** — VVG §§ 165–170: the article-level source for the cash values and for the § 169 Abs. 3 five-year cost spread that shapes `surrender_table.csv`. § 169 Abs. 5 admits a *Stornoabzug* only *"wenn er vereinbart, beziffert und angemessen ist"*, and makes a deduction for unamortised acquisition costs *"unwirksam"*. **The shipped value of zero is a `[std]` choice and not what the market does**: the one *Pflegerenten* wording retrieved for this product agrees a *Stornoabzug* of **25 %** of the § 169 value, rising to 50 % after a partial withdrawal, and none on the paid-up conversion [S4]. See the note at the end of this file.
- **REG-R29** — VVG §§ 172–177, *Berufsunfähigkeitsversicherung*: cited only to mark the neighbouring product, whose insurer-run *Nachprüfung* is what makes its claims cost several times this product's.
- **REG-R30** — VVG §§ 19, 21, 37, 38, 157 and 158: the *Anzeigepflicht*, the § 21 Abs. 3 time bar on the insurer's remedies, and the *qualifizierte Mahnung* whose two-week period the model does not carry.
- **REG-R31 / REG-R33 / REG-R35** — the VVG-InfoV cost-disclosure regime, the IDD and BaFin's *Wohlverhaltensaufsicht*: the conduct layer, and why a pure biometric-risk contract carries a euro cost disclosure rather than an *Effektivkosten* figure.
- **REG-R32** — PRIIPs, Regulation (EU) No 1286/2014: **the article-level carrier for the perimeter question **S6** would have carried.** The Regulation excludes life contracts paying only on death or in respect of incapacity, so a pure-risk *Pflegerente* is very likely outside it and a *Beitragsrückgewähr* form very likely inside — `[unverified]`, and the base run is the variant for which no *Basisinformationsblatt* would be expected.
- **REG-R34** — *Test-Achats* and the AGG: **unisex pricing for contracts concluded from 21 December 2012**, the constraint behind `unisex_mix_male = 0.50` and behind model points 1 and 2 pricing identically and projecting differently.
- **REG-R36** — the BGH line of authority on German life contracts. **The point this product cites it for now has a decision on it**: *BGH, Urteil vom 30. April 2025 — IV ZR 126/23* (`https://www.bundesgerichtshof.de/SharedDocs/Entscheidungen/DE/Zivilsenate/IV_ZS/2023/IV_ZR_126-23.pdf`, 19 pp., retrieved 2026-08-30), on an insurer's promise of a *Pflegerente* on classification into *Pflegestufe* I, II or III after PSG II abolished those grades. The holding is stronger than "not judicially mapped": the Senat holds that awarding the annuity on *Pflegegrad* 2 may be an inadmissible **extension** of the subject matter, because *"nicht ausgeschlossen werden kann, dass die Beklagte … in erheblichem Umfang Pflegerenten an solche versicherten Personen zu zahlen hätte, die nicht in eine der Pflegestufen I bis III … eingestuft worden wären"*, and that *"[e]in hinreichender Rückschluss von der Feststellung eines Pflegegrades 2 auf die Einstufung in die Pflegestufe I nach altem Recht … nicht gezogen werden [kann]"* — the § 140 SGB XI *Überleitung* being no help, since § 140 Abs. 2 Satz 3 Nr. 2 Buchst. a moves people into grade 2 on *erheblich eingeschränkte Alltagskompetenz* **with no prior Pflegestufe at all**. The case was remitted, with an adjustment under § 313 Abs. 1 BGB left open. **So the two scales are now judicially held to be non-mappable in that direction**, which sharpens rather than weakens the DAV 2008 P vintage point [R15] — and which the actuarial profession answered by re-deriving the bases rather than by mapping the scales.
- **REG-R41 / REG-R45 / REG-R46** — EStG § 22 Nr. 1 (*Ertragsanteil*), § 20 Abs. 1 Nr. 6 and the ErbStG with SGB V §§ 226, 229, 240: the tax section only — the competing analysis of the benefit, the treatment of a *Todesfallleistung* or a surrender payment, and contributions on an annuity in payment.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the direction-of-prudence argument behind the five first-order margins, and the statement that the tables are the DAV's property.
- **REG-R48 / REG-R49 / REG-R51** — DAV 2008 T, DAV 2004 R and **DAV 2008 P with the *Pflegegrad* break**; REG-R51 is the cross-product carrier for [R15]. **One qualification belongs here**: for DAV 2008 P the "not public" half of that description is wrong — the DAV publishes both the derivation, with the bases in its appendices, and a companion report re-deriving them for the *Pflegegrade*, free from `aktuar.de` [R15]. delib still does not redistribute any of it, by its own choice. Nothing was retrieved for DAV 2008 T or DAV 2004 R [R16], and this product uses neither.
- **REG-R52** — Destatis *Sterbetafeln*, *Generationensterbetafeln*, *Pflegestatistik* and the reuse licence: the intended base for a user-supplied replacement, and the cross-product carrier for [R18].
- **REG-R53** — the German life market in numbers (GDV, BaFin, Assekurata, Map-Report, Morgen & Morgen, Franke und Bornberg): market scale, and the carrier for [S14] and [R22]. **The finding this bullet used to carry — that *Pflegerentenversicherung* is not a separately reported family — is withdrawn.** The GDV reports it as its own line in new business, in-force main covers and riders alike; the figures are at [R22].
- **REG-R54 / REG-R55** — HGB §§ 341–341o with the RechVersV, and IFRS 17: the accounting layers the same expected-cash-flow engine feeds, and the article-level source for the *Deckungsrückstellung* limb of [R12].
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional standards this model's documentation sits under.

---

## Provenance note

Extraction details — which fact was recorded from which document class, the twenty-three sections
of extracted mechanics, and the twenty-one-item gaps-and-caveats register — live in
`_research/pflegerentenversicherung.md`, which is the citation ground truth for the S# and R#
numbering used here and records at its head the blocked-egress conditions the research was done
under, and the re-verification that followed.

The caveats that most affect what these product documents can claim, in the order in which they
constrain the model:

1. **Most of this file has now been read.** Of the **thirty-six** [S#] and [R#] entries, **twenty-seven record a document opened and read** on 2026-08-30 — every statute as canonical XML with its `Stand`, one carrier's complete *Bedingungswerk* and product description, the PKV *Musterbedingungen* for both compulsory and top-up cover, the DAV's own derivation and *Pflegegrad* reports, Destatis, vdek, GDV, Assekurata and two consumer bodies. **Five are still `Retrieved: no`**, each for a stated and different reason, and none of them an environment limit: **S9** (no German *Pflegerenten* rate card is published at all), **S13** (a portal quotation is not a document, and was deliberately not run), **S8** (no *Standmitteilung* specimen is public — the § 155 VVG field list is), **R10** (the PUEG not opened as an act; its operative content read in SGB XI as consolidated), **R16** (neither DAV table is used here, and the derivation was located but not opened). **Four more are partial** and say so on their own lines: **S5** (the *Informationsblatt* is issued with an offer, so no euro cost figure is retrieved), **S10** (the test scores are paywalled), **R6** (the statute yes, the *Begutachtungs-Richtlinien* no) and **R9** (read at second hand, in two documents that recite it). The old note that this product had no research channel at all describes how it was drafted; as a description of where the file now stands it is superseded.
2. **DAV 2008 P is public, and the *Pflegegrad* break has been worked by the profession** [R15] [REG-R51]. Both halves of the old caveat were wrong: the DAV publishes the derivation with the bases in its appendices, and a companion *Ergebnisbericht* re-derives first-order bases **for the *Pflegegrade***. The residual risk is real but narrower and better described: the DAV's own bases are derived from *Pflegestufen* experience by transition, not observed — *"fehlt naturgemäß jegliche statistische Information"* — and its structure is a ***Stufenmodell*** ("at least grade *g*"), not the five-state chain `Pflege_DE_S` implements. The BGH has since held that no inference runs from *Pflegegrad* 2 back to *Pflegestufe* I [REG-R36]. **Every transition rate in `care_table.csv`, `incidence_table.csv` and `mort_table.csv` is still a `[std]` proxy** with a stated shape and anchor — but it is now a proxy for something published, which a user could replace, and that is a different statement from the one this file used to make.
3. **No rate card was found, and none appears to be published** [S9]. `Pflege_DE_S` still reproduces nothing external: its *Beitrag* is an **output** of a stated first-order basis, and the argued 50,00–100,00 € band remains derived arithmetic tagged `[std]` that **must never be cited as a market figure**. What the band now has is two external checks it did not have: the GDV's in-force average of about **61 € a month** across 242 000 contracts [R22], and Assekurata's *Pflegetagegeld* premiums for the same benefit scale [S14] against the consumer bodies' *"etwa zwei- bis dreimal so hoch"* multiplier for the annuity form [S11]. Both are consistent with the band; neither is a citation for it.
4. **No charge level of any kind was established** [S5] [S7], and this gap survives the pass. Not one *Abschlusskostensatz*, administration rate, *Ratenzahlungszuschlag* or *Effektivkosten* value for any *Pflegerenten* tariff: the retrieved wording refers every one of them to an *Informationsblatt zu Versicherungsprodukten* that is issued with a quotation and is not published. Two things did change. The statutory **25 ‰ ceiling** and its base are read verbatim in DeckRV § 4 Abs. 1 and confirmed in the carrier's own § 17 as *"2,5 % der … zu zahlenden Beiträge"* [R13] [S4], so the one cited quantity in `expense_table.csv` is now genuinely cited. And the retrieved wording charges post-annuity administration as a **percentage of the annuity paid**, where delib charges a euro amount per payment — a structural difference worth knowing when the placeholder is replaced.
5. **One carrier's wording is now read in full** [S4] — IDEAL Lebensversicherung's *IDEAL PflegeRente Exklusiv*, conditions AB-IPR-2022A with four sets of *Ergänzende Versicherungsbedingungen*, plus its public *Produktbeschreibung*. **One is not eight**, which is still the difference between this product and its frlib counterpart, so the variation table in `product-spec.md` remains a market-range reconstruction rather than a survey. What has changed is that the representative specification is now checked clause by clause against a real contract, and every place it departs from that contract is marked in `product-spec.md` — including three departures that matter: the *Leistungsstaffel* (the retrieved wording is a **threshold** design, not a percentage grid), the *Stornoabzug* (25 %, not zero) and the territorial clause (assessment confined to the EU, Switzerland and Norway).
6. **Duration and prevalence are now sourced, and both differ from what the documents assumed** [R18] [R19] [S14]. Duration: the *BARMER-Pflegereport 2024*, cited in the retrieved Assekurata study, puts mean duration of *Pflegebedürftigkeit* at **7,5 years** for 2022, falling to about **five years** where care begins after 60 — **4,0 for men, 5,7 for women** — against about **25 months** mean length of stay in a *Pflegeheim*. delib's `care_table.csv` implies a spell *"of the order of three to five years"*, so it sits at the low end for women and about right for men. Prevalence: the observed *Pflegequoten* are materially **higher** than the curve the documents printed, and the "doubles every five years" shape holds only between about 70 and 90. Duration remains the direct multiplier on the liability: a change from four years to five in the mean spell moves the premium by about a quarter. **Per-grade sojourn data still do not exist** — Assekurata says so in terms — which is the input `Pflege_DE_S` most needs and cannot have.
7. **No lapse rate for this product at any duration was established.** The shape in `lapse_table.csv` is argued from the *Zillmerung* [REG-R16] [REG-R28] and nothing else, and the pricing basis carries no lapse at all — which is German first-order practice and is also what keeps the model acyclic.
8. **The § 169 VVG scope question is still open, and it was mis-stated** [R11] [REG-R28]. There is no "exception" for death-only covers: § 169 Abs. 1 is a positive test — the *Rückkaufswert* is owed where *"der Eintritt der Verpflichtung des Versicherers gewiss ist"* — and a pure-risk *Pflegerente* does not obviously satisfy it. The same test governs the *Effektivkosten* duty in § 2 Abs. 1 Nr. 9 VVG-InfoV, so the two are one question. **A carrier's own wording settles it for that carrier, and the one retrieved does**: IDEAL grants a guaranteed § 169 value, five-year spread floor included, on a product it calls *"eine reine Risikoversicherung ohne Sparprozess"* [S4]. The model prices a *Rückkaufswert*, which that wording supports.
9. **The taxation of the benefit is unresolved** [R23] [REG-R41]. Two analyses compete and this corpus cannot choose between them; delib does not model benefit taxation.
10. **The statutory benefit amounts are 2025 values and they were still in force in 2026** [R3] [R4] [R10]. The consolidated SGB XI as at 24 July 2026 carries the same §§ 36, 37, 43, 43c, 45b and 42a amounts, and § 30 Abs. 1 schedules the next uprating for **1 January 2028**. The `[unverified]` tags on the first-layer tables are removed and the year stamps stand. One amount was wrong and is corrected: the grade-1 residential *Zuschuss* of § 43 Abs. 3 is **131 €**, not 125 €. **Any downstream document should still re-check against the current consolidated text, but the year is no longer an open question.**
11. **No BaFin material specific to LTC was located**, and searching again on 2026-08-30 did not change that, which is why R17 is absent from this file altogether and why the supervisor enters only through [REG-R35]. There is no supervisory statement anywhere in these documents about the *Nachprüfung* or about product value for this class. **The *Pflegetafel*-prudence half of that sentence no longer holds**: prudence loadings for exactly this risk are published, not by BaFin but by the DAV [REG-R8] [R15].
12. **The SGB XI, the VVG, the VAG, the EStG and the DeckRV are living texts**, and the *Höchstrechnungszins* changes by instrument [R13] [REG-R15]. Every statutory entry above now carries the `Stand` of the consolidated text that was actually read, which is the version date this file used to assert nowhere. Those `Stand` lines are what a reader should check against: they date the reading, not the law. **A delib citation is now a pointer *and*, where the `Retrieved` line says so, a record of a document opened and read on 2026-08-30 — and no more than that.**

---

## What the retrieved documents say about the shipped model, and what was left alone

This pass changed provenance, not product design. Five retrieved facts bear on numbers the model
implements, and **none of them was acted on**: a model change moves the worked example and the
golden tests with it, and that is a decision to take deliberately rather than as a side effect of
reading a document. They are recorded here so the decision can be taken with the evidence in view.

1. **The `bahr` *Leistungsstaffel* has lost its citation.** `benefit_scale_table.csv` ships
   10 / 20 / 30 / 40 / 100 % as *"the only Leistungsstaffel fixed by German statute"* [R8]. § 127
   SGB XI fixes no such grid — only a benefit at every grade, a floor of 600 € at grade 5 and a
   ceiling at the SGB XI benefit level. The schedule is a market convention. **It is still a
   perfectly good alternative grid to ship; it is no longer a cited one.**
2. **The *Stornoabzug* range is wrong by a factor of five.** The documents give a market range of
   *"nil to about 5 %"* and ship 0 %, with a model point at 5 %. The one retrieved *Pflegerenten*
   wording agrees **25 %**, rising to 50 % after a partial withdrawal [S4] [REG-R28].
3. **Published prudence loadings exist for exactly this risk.** The DAV's incidence *Gesamtzuschlag*
   runs 20,5–31,2 % by minimum *Pflegegrad* against delib's `inc_margin` of 1.25 — close, and now
   corroborated. But its *Invalidensterblichkeit* *Gesamtabschlag* is 24,2–28,5 %, against delib's
   `care_mort_margin` of 0.85, so **the shipped in-care mortality margin is materially less prudent
   than the profession's** [REG-R8] [R15]. `act_mort_margin` 0.90 against 13,6 % is close.
4. **The incidence slope's anchor is measurable and softer than assumed.** `inc_rate`'s exponent is
   anchored to prevalence doubling every five years above 75, `ln 2 / 5 = 0.1386`. The observed
   *Pflegequoten* rise by factors of 1,80 · 1,88 · 1,74 · 1,49 · 1,18 across the five-year bands
   from 70–75 to 95+, i.e. about `ln 1.8 / 5 = 0.117` over the range where the model earns its
   claims, flattening above 90 where the model does not cap until 0.50 [R18].
5. **The model's state structure is not the profession's.** Both the DAV bases [R15] and the
   retrieved carrier product [S4] are **threshold** constructions — *"mindestens Pflegegrad g"* —
   whereas `Pflege_DE_S` runs a five-state per-grade chain with a percentage *Leistungsstaffel*.
   Neither is wrong; they answer different questions, and a user replacing the `[std]` tables with
   DAV bases would be changing the shape of the model and not only its numbers.

One further finding is not a model issue but changes what the documents may say: **the definition
risk this product was described as carrying unhedged is in fact hedged by every wording retrieved**
— MB/PPV and MB/EPV copy the statutory test into the conditions [S1] [S2], and AB-IPR-2022A pins it
to a stated *Stand* [S4]. What is unhedged is drift in assessment practice under a fixed text [R6],
and the gap that opens between a pinned private definition and the moving social insurance beside it.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #delib-pflegerentenversicherung-r10
[R11]: #delib-pflegerentenversicherung-r11
[R12]: #delib-pflegerentenversicherung-r12
[R13]: #delib-pflegerentenversicherung-r13
[R14]: #delib-pflegerentenversicherung-r14
[R15]: #delib-pflegerentenversicherung-r15
[R16]: #delib-pflegerentenversicherung-r16
[R18]: #delib-pflegerentenversicherung-r18
[R19]: #delib-pflegerentenversicherung-r19
[R2]: #delib-pflegerentenversicherung-r2
[R20]: #delib-pflegerentenversicherung-r20
[R21]: #delib-pflegerentenversicherung-r21
[R22]: #delib-pflegerentenversicherung-r22
[R23]: #delib-pflegerentenversicherung-r23
[R3]: #delib-pflegerentenversicherung-r3
[R4]: #delib-pflegerentenversicherung-r4
[R5]: #delib-pflegerentenversicherung-r5
[R6]: #delib-pflegerentenversicherung-r6
[R8]: #delib-pflegerentenversicherung-r8
[R9]: #delib-pflegerentenversicherung-r9
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R25]: #delib-reg-r25
[REG-R28]: #delib-reg-r28
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R51]: #delib-reg-r51
[REG-R53]: #delib-reg-r53
[REG-R8]: #delib-reg-r8
[std]: #delib-std
<!-- END generated citation links -->
