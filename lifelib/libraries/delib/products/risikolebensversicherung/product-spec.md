# Product Specification

**Status:** Draft, 2026-08-29; citations re-verified against the primary documents 2026-08-30
(22 of the 40 entries in `sources.md` now read `Retrieved: yes` — see below).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of a German **Risikolebensversicherung** (RLV) — the standalone term
assurance that pays a *Todesfallleistung* (death benefit) equal to the agreed *Versicherungssumme*
if the *versicherte Person* dies inside the *Versicherungsdauer* and pays nothing at all otherwise.
**It does not describe any single insurer's product, and it could not have.** Facts carrying a
source tag — [S#] (primary product documents: *Allgemeine Versicherungsbedingungen*,
*Produktinformationsblatt*, *Verbraucherinformation*, insurer product pages) and [R#]
(product-specific regulatory and actuarial references), both numbered per
`_research/risikolebensversicherung.md` and resolved in `sources.md` (same directory; numbering
frozen, never renumbered), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) — name the
instrument the claim should be checked against. Values marked **[std]** are standardizations
introduced for the reference implementation; each **[std]** table row carries a numbered footnote
giving the rationale and, where one can be argued, a plausible range. Claims that no search
corroborated are flagged [unverified].

**Retrieval conditions — read this before relying on a number, because they changed after it was
written.** This specification was **drafted** with direct HTTP egress from the build environment
blocked by an organisation network policy — `gesetze-im-internet.de`, `bafin.de`, `gdv.de`,
`aktuar.de`, `dejure.org`, `buzer.de`, `destatis.de` and `de.wikipedia.org` were all tried and all
refused — and with **the session's shared `WebSearch` budget exhausted before this product's
research began**, so unlike the two sibling delib products this one had *zero* searches of its own.
The first draft therefore rested on the authoring model's own knowledge of German insurance law and
practice, disciplined by **[std]** on every level it standardized and [unverified] on every specific
it could not confirm, with **inherited corroboration** — an instrument search-corroborated for a
sibling delib product while budget remained, carried across with the sibling named — as its only
second-hand evidence.

**That policy has since been lifted and the citations re-verified against the primary documents on
2026-08-30.** In `sources.md`, **22 of this product's 40 entries now read `Retrieved: yes` and 18
still read `no` — 55 %**, against 501 of 805 entries (62 %) across delib as a whole. What came in is
the statutory core and three wordings: the VVG, the MindZV, the DeckRV, the VAG, the AGG, the EStG,
the ErbStG, the VVG-InfoV and the HGB read as canonical XML from `gesetze-im-internet.de` with each
law's amendment status (`Stand`) recorded, the VersStG 2021 in HTML beside them; the GDV
*Musterbedingungen* of 21.07.2025, CosmosDirekt's AVB **LA 803 A (04.26)** and Hannoversche's **T25**
as PDFs; two carrier *Informationsblatt* specimens that print a premium and its costs in euro; and
one carrier's surplus guide. `frlib`'s counterpart could put eight French carriers side by side
because eight *notices d'information* were downloaded and read; where an earlier draft of this
passage said **this document can put none side by side**, it can now put **two, in full, and the
industry template they are both variations on.**

The 18 that did not come in are the carrier sweep and the secondary literature, and they failed in
named ways: Debeka's cited path now answers **HTTP 404**, and the replacement library injects its
document links client-side so nothing is in the served HTML [S6]; Allianz and LV 1871 publish a
product page with no conditions file, the wording reached through a quote flow [S8] [S11]; Dialog
keeps its wordings behind the broker channel [S7]; R+V, NÜRNBERGER, Continentale/Europa and the
seventeen further carriers were not searched for at all once the three wordings had settled the
clause questions [S9] [S10] [S12] [S13]; *Finanztest* publishes a free summary and sells the test,
and the rating houses sell theirs [S16] [S17] [R20]; a comparison-portal result is generated per
query and is not a published document at all [S14], and no address was ever established for the
consumer guide beside it [S15]; and the GDV statistics, the BaFin material, the Solvency II
texts, the case law and the DAV *Sterbetafel* papers — whose four addresses were opened and
confirmed live, but whose text was not read — remain pointers [R12] [R18] [R19] [R22] [R23].

**Where an entry in `sources.md` says `Retrieved: yes`, treat the claim it carries as sound; where it
says `no`, a delib citation is still a pointer, not a certificate** — it names the instrument a claim
should be checked against and does not assert that anyone checked it. Re-verification was not a
formality: it overturned this document's flat denial of any *Rückkaufswert*, corrected the claim that
German term-life charges are structurally undisclosed, replaced a guessed *Nachversicherung* event
list with a carrier's own, and re-titled § 163 VVG. What has **not** changed is that levels are not
observed: apart from one direct writer's published model case [S2], **not one *Bruttobeitrag* or
*Zahlbeitrag* anywhere in this library is a market observation**, and that one case is recorded as a
check rather than adopted as a parameter. Where a mechanic is certain and its level is not, this
document still ships a **[std]** parameter with its arithmetic shown rather than a plausible-looking
figure with a source tag it has not earned.

**Out of scope, and said so where it matters.** *Restschuldversicherung* /
*Restkreditversicherung*, the single-premium bank-sold loan-linked group cover, which shares the
falling sum insured of the *annuitätisch fallende* RLV and nothing else; *Sterbegeldversicherung*,
the small-sum funeral cover written without a *Gesundheitsprüfung*, which carries a *Wartezeit* and
a *Rückkaufswert*; *Risikolebensversicherung mit Beitragsrückgewähr*, which has a savings element by
construction and is economically the endowment of `products/kapitallebensversicherung/`; the
*Berufsunfähigkeits-* and *Unfalltod-Zusatzversicherung* riders, described here as options and not
modeled, the standalone disability contract being `products/berufsunfaehigkeit/`; and *betriebliche
Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung* and *Kollektivverträge*.

---

## Product overview and market role

A German *Risikolebensversicherung* is **life insurance under Kapitel 5 of the VVG**
(*Lebensversicherung*, §§ 150–171) — not accident and not health business, even though it pays only
on death [R1] [R4] [R7] [R8] [REG-R22]. Every general life provision of that chapter applies
unmodified: the 30-day *Widerrufsfrist* of § 152 [R8] [REG-R23], the *vorvertragliche Anzeigepflicht*
of § 19 [R4] [REG-R30], the *Selbsttötung* rule of § 161 [R1] [REG-R26], the *Bezugsberechtigung* of
§ 159 [R7]. It is pure protection: a level *Bruttobeitrag* buys a *Versicherungssumme* for a fixed
term, with **no *Sparanteil* in the endowment's sense, no *Erlebensfallleistung*, no maturity value
and a *Rückkaufswert* that is nil or nominal wherever a wording provides for one at all**. If the
*versicherte Person* survives, nothing is paid and the contract ends [R1] [R2] [S1] [S3] [S4].

Four features make the German chassis different from its French, UK and US siblings, and each one
changes the shape of the projected cash flows.

1. **The premium is level, and there are two of them.** The *Bruttobeitrag* is struck at the
   *Eintrittsalter* and held there for the whole *Beitragszahlungsdauer* [R6] [R10]; what the
   customer is billed is the ***Zahlbeitrag***, the *Bruttobeitrag* less a declared
   *Beitragsverrechnung* — the *Überschussbeteiligung* of § 153 VVG applied as an immediate offset
   against the premium rather than as a credit to an account there is none of [R5] [R9] [S5]. **Only
   the *Bruttobeitrag* is guaranteed**, and the insurer may cut the *Beitragsverrechnung* and raise
   the bill toward it **without any § 163 procedure, without a *Treuhänder* and without a policyholder
   right of objection** [R6] [REG-R27]. This is the single most important legal fact about the German
   term-life premium, and a model carrying only one premium stream cannot represent this product.
2. **The cash value is nil or nominal — and the reason is neither that nothing accumulates nor that
   the contract forbids it.** A level premium against a rising death rate overcharges early and
   undercharges late, and the difference is a *Deckungskapital* that builds, peaks mid-term and runs
   off to exactly zero at expiry — small, and after *Zillmerung* negative or nil through much of the
   term. § 169 Abs. 1 VVG confines the **surrender-value duty on *Kündigung*** to a life insurance
   "bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist", and a term assurance's is
   not [R2] [REG-R28] — so no statutory duty attaches. But the wordings still route there: the GDV
   model conditions and the Hannoversche AVB both **convert the contract into a *beitragsfreie
   Versicherung*** on *Kündigung* and pay a *Rückkaufswert* under § 169, less a *Stornoabzug*, where
   the paid-up sum fails a contractual minimum [S1] [S4]; Cosmos pays nothing at all [S3]. What is
   uniform is the size, and the wordings say why in the same words — the *Kostenverrechnung* leaves
   "keine oder nur geringe Mittel" [S1] [S3]. **"There is no *Sparanteil*, therefore there is no
   reserve" is wrong, and a model built on it fails its own closure check** — and so is "the German
   term product has no surrender value, full stop".
3. **The exclusion list is remarkably short.** Beyond the statutory three-year *Selbsttötung* window
   [R1] and the forfeitures of § 162 VVG [R7], a German RLV wording carries essentially one
   substantive exclusion — the *Kriegsklausel* — plus a nuclear/ABC clause: **no hazardous-sports
   list, no aviation exclusion, no alcohol or narcotics exclusion, no pre-existing-condition
   exclusion**, hazardous activity being handled at underwriting by a *Risikozuschlag*. The French
   *notices* retrieved for `frlib` carry exclusion lists running to a dozen heads or more; **a German
   wording covers all of it by pricing it**, so the German product's claim rate is a mortality
   question where the French product's is partly a coverage question.
4. **There is no living-benefit acceleration in the base design.** Germany has no counterpart to the
   French *perte totale et irréversible d'autonomie*, present in seven of the eight standalone
   `frlib` contracts: one decrement pays one benefit and there is no interlock to get wrong. What
   Germany has instead is a *vorgezogene Todesfallleistung* triggered by a terminal **prognosis**,
   and disability is sold as a rider or as `products/berufsunfaehigkeit/`.

**Where it sits in the market.** The GDV taxonomy puts this product in ***Risikoversicherungen***,
alongside *Kapitalversicherungen*, *Rentenversicherungen*, *fondsgebundene* and *sonstige
Lebensversicherungen* [REG-R53]. **The size of that segment could not be established**: no contract
count, no new business, no premium income, no aggregate *versicherte Summe*, no average sum insured
or premium and — most consequentially for the model — **no segment-specific *Stornoquote*** [R18]
(research gap 13). What can be given is the whole of German life on the GDV basis for 2024: premium
income **+2,8 % to 94,6 Mrd. €**, *laufende Beiträge* **66,3 Mrd. €**, *Einmalbeitragsgeschäft*
about **+10 % to 28 Mrd. €**, contract count **−1,4 % to 80,3 Mio.** [REG-R53]. Two structural
remarks stand in for the missing breakdown, both arithmetic rather than observation: a term
contract's **premium** is tiny relative to its **sum insured**, so the segment is far larger measured
by risk carried than by premium earned and any ranking by premium income understates it; and because
its whole technical result is a *Risikoergebnis*, the MindZV's 90 % minimum allocation [R9] [REG-R18]
binds it more tightly than it binds any savings product.

**Distribution is genuinely three-channel** — tied agents and bank branches [S8] [S9], independent
brokers [S7] [S10] [S11], direct writers [S3] [S4] [S12] — and the channel is visible in the
*Brutto*/*Zahlbeitrag* spread, acquisition cost being the largest thing that differs between them.
The cleanest natural experiment in German life insurance sits in this product: one group runs a
broker-channel carrier and a low-cost direct carrier side by side on the same underwriting and
reserving basis [S12]. **It was not sampled** (research gap 5). And because no German carrier
publishes a rate card, **the comparison portals are a market participant rather than an observer**
[S14]: a tariff's design is shaped by how it ranks in a portal's default query, which is a
*Zahlbeitrag* query — a plausible structural explanation, [unverified], for why the *Zahlbeitrag* is
marketed and the *Bruttobeitrag* merely disclosed, the consumer-protection line running the other way
[S15] [S16] [S17] [R20]. A portal result is generated per query rather than published, so none was
obtained once egress was restored either — which is why **the only German premium figures anywhere in
this library are the ones a carrier prints in its own *Informationsblatt* specimen** [S2], one model
case at one carrier and not a market (gap 1).

---

## Representative specification

The representative design is a **composite**, not a copy of any carrier's tariff — it could not be
otherwise, no carrier's tariff having been read. Every choice below is argued against the
structural range the research file could establish, and where the range itself is unobserved the
row says so rather than implying a distribution nobody measured.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Individual, standalone, medically underwritten, *überschussberechtigte* Risikolebensversicherung; *Neubestand* | [R9] [R11] [R12]; mechanic 1 |
| Legal frame | *Lebensversicherung* under Kapitel 5 VVG (§§ 150–171); not a PRIIP, so no *Basisinformationsblatt* is produced | [R1] [R4] [R7] [R8] [REG-R22]; PRIIP boundary [R17] [unverified] |
| Documents delivered | *Allgemeine Versicherungsbedingungen*; *Verbraucherinformation* pack; *Produktinformationsblatt* under the VVG-InfoV | [S1] [S2] [R17] [REG-R31] |
| Lives basis (model-point parameter) | `lives = 1` single life. `lives = 2` is the *verbundene Leben* form: two *versicherte Personen*, one payment on the **first** death, contract then ends | mechanic 14; **[std]** (1) |
| Contracting structure | Ordinary (*Versicherungsnehmer* insures his own life, names a *Bezugsberechtigter*). The *Über-Kreuz-Versicherung* is an alternative **structure**, not a product: identical cover, identical cash flows, different *Erbschaftsteuer* outcome | [R7] [R15] [REG-R46]; mechanic 14 |
| Three roles | *Versicherungsnehmer* (owns and pays), *versicherte Person* (the life at risk), *Bezugsberechtigter* (receives). Routinely three different people — the normal case here, not the exception | [R7] [REG-R26]; mechanic 1 |
| Consent of the insured life | § 150 Abs. 2 VVG: where the benefit "übersteigt ... den Betrag der gewöhnlichen Beerdigungskosten", that person's ***schriftliche Einwilligung*** is required for the contract to be effective, with an exception for *betriebliche Altersversorgung* and a special rule in Abs. 3 for a parent insuring a minor child | [R7] [REG-R26] |
| *Eintrittsalter* (model-point parameter) | 18 to 65 | envelope **[std]** (2) |
| *Endalter* | 75 | envelope **[std]** (2) |
| *Versicherungsdauer* (model-point parameter) | 5 to 40 years | envelope **[std]** (2) |
| *Beitragszahlungsdauer* (model-point parameter) | Equal to the *Versicherungsdauer* in the base design; an ***abgekürzte Beitragszahlungsdauer*** shorter than the cover period is offered by some tariffs | mechanic 4 [unverified]; envelope **[std]** (2) |
| *Versicherungssumme* | 10 000 € to 50 000 € minimum; high six to low seven figures without special underwriting | envelope **[std]** (2) |
| *Versicherungssumme* shape (model-point parameter) | (i) `konstant`; (ii) `linear_fallend`; (iii) `annuitaet_fallend` — the *Darlehensabsicherung* form, following the outstanding balance of an annuity loan at a nominal rate **agreed at issue** | mechanic 3; all three [unverified] as to any carrier |
| Age basis | *Alter am Jahrestag* (ALB): the attained age at the policy anniversary, `issue_age + t − 1` in policy year `t` | **[std]** (3) |
| Currency and territory | EUR; residence in Germany; worldwide cover subject to the *Kriegsklausel* | mechanic 13 [unverified] |
| *Wartezeit* | **None.** Cover attaches from the agreed *Versicherungsbeginn*; the insurer's protection against anti-selection is the *Gesundheitsprüfung*, not a deferral of cover | mechanic 2 [unverified]; contrast [`frlib` S6] [`frlib` S9] |
| *Widerrufsfrist* | 30 days for life insurance — "Abweichend von § 8 Absatz 1 Satz 1 beträgt die Widerrufsfrist 30 Tage", § 152 Abs. 1 — extending the general 14 days, and lapsing at the outside 24 months and 30 days after conclusion | [R8] [REG-R23] |
| Anchor model cell | Entry age 35, male, non-smoker, *Versicherungssumme* 300 000 € *konstant*, term 25 years, premiums for 25 years, annual mode, standard rates, participating, no options | **[std]** (4) |

Footnotes to **[std]** rows:

1. Single life and *verbundene Leben* are **one chassis parameterised by the number of lives**, not
   two products. Both lives are underwritten and both give the § 150 consent [R7]; the premium sits
   below two single contracts of the same sum, only one benefit ever being paid, and above one.
   **No ratio is asserted** (research gap 15); the model computes the first-death rate from
   `q_first = q_A + q_B − q_A·q_B` under an independence assumption, itself **[std]** and itself an
   understatement for a couple sharing a household, a vehicle and a lifestyle.
2. **Not one of these envelopes was observed** — no carrier's AVB was read and no carrier's issue
   rules are recorded anywhere in the research file (gap 22). They are the ranges German market
   practice is understood to run on, stated as **[std]** so a reader does not mistake them for a
   survey: *Eintrittsalter* 18–65, some carriers to 70 or 75; *Endalter* 75, with 80 and 85 offered;
   *Versicherungsdauer* 5–40 years; *Mindestversicherungssumme* 10 000–50 000 €. **A single
   retrieved AVB would close almost all of this gap.**
3. Germany has no counterpart to the French *différence de millésime*, where the rating age steps on
   1 January irrespective of birth month. German practice is an age at the policy anniversary, which
   is also this model's projection step; on a real-date implementation the offset is at most a few
   months. **[std]**, and the age basis registered for every delib model in `tests/de_registry.py`.
4. **Entry age 35 with a 25-year term** is long enough for the *Deckungskapital* to build and run
   off visibly and short enough to fit one worked-example table; **300 000 €** is the sum at which
   the *Erbschaftsteuer* contrast of mechanic 14 becomes the decisive product-design fact; **male**
   rather than blended on both sides, so the unisex cross-subsidy the model necessarily carries is
   visible in the anchor rather than hidden, with the female twin as model point 2 and the smoker
   twin as model point 3.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium form (model-point parameter) | (i) `laufend` — a **level *Bruttobeitrag*** payable at the start of each of the first `prem_term` policy years; (ii) `einmal` — a single *Einmalbeitrag* at issue | (i) mechanic 4 [R6] [R10]; (ii) **[std]** (5) |
| What is guaranteed | The ***Bruttobeitrag*** — the maximum the policyholder can ever be required to pay, unchanged for the term | [R6] [REG-R27]; mechanic 5 |
| What is billed | The ***Zahlbeitrag*** = *Bruttobeitrag* × (1 − `v`), with `v` the declared *Beitragsverrechnungssatz*. **Not guaranteed** and revisable annually by declaration alone | [R5] [R6] [R9] [S5]; level **[std]** (6) |
| Representative `Zahl / Brutto` ratio | **0.57** | **[std]** (6) |
| Pricing bases (*Rechnungsgrundlagen erster Ordnung*) | DAV 2008 T-shaped mortality with its *Sicherheitszuschläge*, *Rechnungszins*, and α / β / γ expense loadings | [R12] [R10] [REG-R47] [REG-R48]; levels **[std]** (7) |
| *Rechnungszins* | **1,00 %** — the *Höchstrechnungszins* for new business from 1 January 2025, raised from 0,25 % and the first increase since 1994 | [R10] [REG-R14] [REG-R15] |
| *Sicherheitszuschlag* `m` | First-order `q1 = (1 + m) × q2` with **m = 1.25**, so `q1 = 2.25 × q2` | **[std]** (7) |
| Unisex mixing ratio | **50 % male / 50 % female** blend of the sex-distinct base tables, applied to the **tariff** and never to the projection | **[std]** (8); [R13] [REG-R34] |
| Rating factors | Entry age; *Versicherungsdauer*; sum insured; smoker status; occupation; declared hazardous pursuits; health evidence. **Sex may not be a rating factor** for contracts concluded from 21 December 2012 — AGG § 33 Abs. 5 confines the derogation to "Versicherungsverhältnisse, die vor dem 21. Dezember 2012 begründet werden", and § 20 Abs. 2 leaves no actuarial justification open for sex at all. [S3] § 18 confirms the smoker split and prices it, and [S3] § 13 Abs. 5 confirms that occupation, attained *rechnungsmäßiges Alter* and any agreed *Risikozuschlag* price an increase | mechanic 9; unisex [R13] [REG-R34]; [S3] |
| *Risikozuschlag* (model-point parameter) | `rating_factor`, a multiplier on the **mortality basis**; 1.00 at standard rates | mechanics 9; value **[std]** (9) |
| *Zahlweise* (model-point parameter) | `jaehrlich`, `halbjaehrlich`, `vierteljaehrlich`, `monatlich`; annually in advance is the actuarial base case, monthly by *SEPA-Lastschrift* the market's normal choice | mechanic 7 [unverified] |
| *Ratenzahlungszuschlag* | Annual 1.000; half-yearly **1.02**; quarterly **1.03**; monthly **1.05** | **[std]** (10) |
| Premium cessation | On death; at the end of the *Beitragszahlungsdauer*, which may precede the end of the *Versicherungsdauer* | mechanics 4, 17 |
| Premium increase by the insurer | § 163 VVG — titled ***Prämien- und Leistungsänderung***, not *Anpassung der Prämie* — permits a *Neufestsetzung* only where the ***Leistungsbedarf*** has changed "nicht nur vorübergehend und nicht voraussehbar" against the bases of the agreed premium, where the new premium is "angemessen und erforderlich" for *dauernde Erfüllbarkeit*, and where "ein unabhängiger Treuhänder" has confirmed both; barred where the original calculation was inadequate and a careful actuary should have seen it. Abs. 2 gives the policyholder a right to a benefit reduction instead. **On a German RLV *Bruttobeitrag* this route is essentially never used** | [R6] [REG-R27]; non-use [unverified] — no retrieved document reports practice either way |
| *Versicherungsteuer* | **None.** VersStG 2021 § 4 Abs. 1 Nr. 5 Buchst. a exempts a contract creating claims "im Fall des Todes", so the premium bears no insurance premium tax — unlike a French *cotisation* quoted "TTC" | [R16]; mechanic 7 |

5. **The `einmal` form is a [std] construction and no German standalone RLV in the research file is
   written on it.** It is carried because it is the degenerate case of the same equivalence that
   strikes the level premium, so it tests the premium engine at a boundary rather than adding a
   second engine; because the out-of-scope *Restschuldversicherung* is written on it; and because it
   is the only way to exercise `prem_term = 1` against a long `policy_term`. It is **not** evidence
   that a single-premium standalone German RLV is a market form.
6. **The single most consequential [std] number here, and it is not an observation.** No German
   carrier publishes a *Bruttobeitrag*/*Zahlbeitrag* pair; the PIB quotes the applicant's own
   premium [S2]; a portal result is generated per query rather than published [S14]; and
   *Finanztest*, which rates on the *Zahlbeitrag* while separately reporting the *Bruttobeitrag*
   [S16], is exactly the document type that would supply the pair and was not obtained (gap 1). What
   **can** be said: the ratio is below 1 for essentially every participating tariff; it is wider in
   the direct channel, less of the *Bruttobeitrag* being committed to acquisition cost [S3] [S12];
   and a narrow spread is marketed by some tariffs as a selling point [S17]. **The argued range is
   0.45 to 1.00**, and the representative 0.57 is *derived*, not assumed — it falls out of
   `m = 1.25` and the MindZV 90 % minimum [R9]. Changing `m` re-derives it; that is the point.
7. **Every charge and margin level here is [std], but the reason given for that was wrong and is
   corrected** (gap 8). There is indeed no *Effektivkostenquote* — and the regulation says why in
   terms, confining the duty to contracts "bei dem der Eintritt der Verpflichtung des Versicherers
   gewiss ist", § 2 Abs. 1 Nr. 9 VVG-InfoV — and no *Basisinformationsblatt*, because the product is
   not a PRIIP [R17]. **But German term-life charge levels are not "structurally undisclosed".**
   § 2 Abs. 1 Nr. 1 VVG-InfoV requires the *Abschlusskosten* as a single total figure and the other
   costs as a share of the annual premium, § 2 Abs. 2 requires them **in Euro**, and § 4 Abs. 2 puts
   them on the face of the *Informationsblatt zu Versicherungsprodukten* under the heading "Prämie;
   Kosten"; both retrieved wordings point the customer there [S1] § 14 Abs. 1, [S3] § 16 Abs. 1. What
   is missing is a **published rate card**, not disclosure — and one carrier's *Muster* specimen
   prints the figures: for its model case, acquisition cost of **99,98 EUR = 2,41 % of the
   *Tarifbeitragssumme***, other annual costs of **48,52 EUR** of which **35,20 EUR** administration,
   and **1,50 EUR per 100 EUR** of paid-up sum insured while paid up [S2]. **These charges stay
   [std]**: one direct writer's model case is not a market, and the composite is not recalibrated to
   it. The magnitude of the DAV 2008 T *Sicherheitszuschlag* is **not public** —
   the *Richtlinie* regulates the **procedure** for setting it, not the level [R12] [REG-R48] — and
   it determines the spread almost by itself. `m = 1.25` is calibrated so the **derived** ratio lands
   near the market's "about half"; the argued range is **1.0 to 1.5** and the sensitivity is
   tabulated below.
8. **DAV 2008 T is sex-distinct** [R12] [REG-R48] while new business has been unisex since
   21 December 2012 [R13] [REG-R34], so every German unisex term tariff is a blend at **a mixing
   ratio the carrier chooses from its own expected new-business mix** — proprietary, unpublished,
   periodically re-estimated. Female mortality at these ages is roughly half male [unverified], so
   the ratio moves the tariff a great deal, and this is **one of the largest single sources of
   unexplained rate spread between German carriers**. France's analogue is thinner but at least
   published: the Institut des actuaires' working group uses 60/40 [`frlib` R13].
9. **No German carrier publishes a *Risikozuschlag* scale, and neither does any French one**
   [`frlib` mechanic 10]. The German outcome on an impairment is normally a **premium loading
   expressed as a percentage of the risk premium**, not a benefit exclusion, life
   *Leistungsausschlüsse* being used sparingly [unverified]. `rating_factor` therefore multiplies the
   **mortality basis** — first-order and second-order alike — so an impaired life pays more **and is
   expected to claim more**. The alternative reading, in which the loading is pure price and falls
   through to surplus, is a listed pitfall rather than an alternative default.
10. **2 % / 3 % / 5 % is a market convention with no carrier attribution**, inherited from the
    sibling delib research (gap 21). Whether German carriers strike it on the *Bruttobeitrag* or the
    *Zahlbeitrag* was **not established**; the implementation loads the **billed** amount, so the
    guaranteed maximum for a fractional payer is the loaded *Bruttobeitrag* and the
    *Brutto* = *Zahl* + *Verrechnung* identity holds at every frequency.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Death benefit | The *Versicherungssumme* in force for that policy year, from **any cause** — accident or illness alike — subject only to the short exclusion list below | [R1] [R2] [S5] [S15]; mechanic 2 |
| Survival benefit | **None.** If the *versicherte Person* survives the term, nothing is paid and the contract ends | [R1] [R2] [S5] [S15] |
| Benefit form | A **lump sum** paid to the *Bezugsberechtigter* directly, not through the estate where the nomination is effective, so the beneficiary is paid without waiting for probate | [R7] [REG-R26]; [unverified] |
| *Bezugsberechtigung* | Revocable by default; an ***unwiderrufliche*** nomination vests the claim immediately and takes it out of the policyholder's disposal, with insolvency and gift-tax consequences | [R7] [REG-R26] [REG-R46] |
| Benefit schedule (model-point parameter) | `benefit_pp(t) = sum_assured × benefit_factor(t)`, driven by an external schedule table. `konstant` ships `1.0` at every `t`; `linear_fallend` falls by `1/n` a year; `annuitaet_fallend` follows the outstanding balance of an `n`-year annuity loan at an agreed nominal rate | mechanic 3; schedules **[std]** (11) |
| *Selbsttötung* | The insurer is ***leistungsfrei*** where the *versicherte Person* **intentionally takes her own life within three years of conclusion**, unless the act was committed in a state excluding free determination of the will caused by a *krankhafte Störung der Geistestätigkeit*. The period may be **extended by agreement**. Where *leistungsfrei*, the insurer must nevertheless pay the *Rückkaufswert* including *Überschussanteile* under § 169 | [R1] [REG-R26]; inherited corroboration |
| What the § 161 substitution is worth here | **Nil or nominal.** There is no *Rückkaufswert* on this product [R2], so the German three-year rule — a softening on an endowment — is on a term contract **an exclusion in all but name** | [R1] [R2]; mechanics 11, 12 |
| *Tötung durch Leistungsberechtigten* (§ 162 VVG — that is the section's actual heading, not *Herbeiführung des Versicherungsfalles*, which is § 81) | The insurer is *leistungsfrei* where the **policyholder** intentionally and unlawfully brings about the death of the *versicherte Person*; a **beneficiary** who does so is treated as never designated — "gilt die Bezeichnung als nicht erfolgt" | [R7] [REG-R26] |
| *Kriegsklausel* | **Correction — the retrieved wordings exclude rather than restrict.** Both say the benefit is excluded where death is causally connected with *kriegerische Ereignisse*, and that the contract then "erlischt ... ohne dass eine Leistung anfällt. Die Rückzahlung der Beiträge können Sie nicht verlangen" [S3] § 2 Abs. 6 — there is no *Deckungskapital* substitution. What is right is the **passive-risk carve-out**, and it is narrower than "passive war risk remains covered": cover is restored only for a death **outside Germany** where the insured person was exposed to those events without active participation, [S3] adding humanitarian missions and named Bundeswehr deployments; [S4] § 18 Abs. 2 is the same rule in fewer words | mechanic 13; [S3] [S4] |
| Nuclear / ABC clause | A parallel exclusion for death connected with the deliberate use or release of atomic, biological or chemical weapons or substances — and **both wordings gate it on scale and on a *Treuhänder***: it bites only where the act was aimed at endangering **more than 1 000** people and produces an unforeseeable change in the *Leistungsbedarf* such that the promised benefits are no longer securable, "und dies von einem unabhängigen Treuhänder bestätigt wird" [S3] § 2 Abs. 7, [S4] § 18 Abs. 3. **Death in *Wehr-* or *Polizeidienst* or in *innere Unruhen* is expressly covered**, not excluded [S3] § 2 Abs. 5, [S4] § 18 Abs. 1 | mechanic 13; [S3] [S4] |
| Exclusions beyond these | **None** — confirmed against two wordings and the model wording, all of which open with the general rule that liability arises "unabhängig davon, auf welcher Ursache der Versicherungsfall beruht". No hazardous-sports list, no aviation exclusion, no alcohol or narcotics exclusion, no occupational exclusion, no pre-existing-condition exclusion. [S3] adds one head the earlier draft did not have: death connected with a **terrorist act the insured person committed or took part in** | mechanic 13; [S1] [S3] [S4] |
| Settlement | On production of the death certificate and the insurer's claim documents; where the death falls in the first five (ten) years the § 19 remedies remain open | [R4] [REG-R30]; mechanic 9 |
| Prescription | The general BGB limitation applies; **no German decision is cited by date or file number anywhere in this library, and none is invented** | [R23]; research gap 20 |

11. **A model that hard-codes a constant sum insured cannot represent two of the three shapes the
    German market sells**, which is why the schedule is a first-class external input rather than a
    flag. **The schedule parameters themselves were not established** (gap 15): not the nominal rate
    a German *annuitätisch fallende* tariff amortises at, not the residual sum at expiry, not the
    premium reduction relative to the constant shape. A `linear_fallend` schedule reaching zero at
    expiry and an `annuitaet_fallend` schedule at a **3,0 %** nominal rate ship as **[std]**.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Legal frame | § 19 VVG: the applicant must disclose the *gefahrerhebliche Umstände* known to her **that the insurer has asked about in *Textform***, and nothing else. **The duty is question-bounded** — there is no free-standing duty to volunteer | [R4] [REG-R30]; inherited corroboration |
| *Gesundheitsfragen* | Outpatient treatment and consultations over a recent look-back; inpatient treatment, operations and psychotherapy over a longer one; current complaints, medication and pending investigations; height and weight; nicotine consumption | mechanic 9; **look-back periods [unverified], none asserted** (gap 22) |
| Escalation | *Ärztliche Untersuchung*, *Hausarztbericht*, blood tests or an ECG as the sum insured and entry age rise; a *vereinfachte Gesundheitsprüfung* below a stated sum | mechanic 9; **no threshold asserted** (gap 22) |
| *Finanzielle Angemessenheit* | Above a threshold the insurer also underwrites the financial justification — income, existing cover, the loan being protected — to bound over-insurance | mechanic 9 [unverified] |
| *Raucher* / *Nichtraucher* | The largest single rating split after age, and **the qualifying period is now established at twelve months** (gap 22, closed): "Nichtraucher ist, wer mindestens in den letzten zwölf Monaten vor Antragstellung nicht aktiv geraucht oder gedampft hat (nikotinhaltig oder nikotinfrei)", with a parallel *Nicht-Nikotinkonsument* class for nicotine in any other form [S3] § 18 Abs. 2. **The classification is continuing, not fixed at issue**: a switch to smoking is a *Gefahrerhöhung* the policyholder must notify, the insurer may then charge a higher premium **retroactively from the switch** at an unchanged sum insured, and the policyholder may take a benefit reduction instead or, if the premium rises by more than ten per cent, terminate within a month [S3] § 18 Abs. 4–6. That carrier waives its statutory rights to terminate or exclude the increased risk, and checks smoking status only at the claim | mechanic 9; [S3] |
| Actuarial sanction for the split | The DAV publishes ***DAV 2008 T R*** and ***DAV 2008 T NR*** and states they are **suitable for premium calculation** differentiated by smoking status — **but not for policies written without a *Gesundheitsprüfung*** | [R12] [REG-R48]; inherited corroboration |
| Smoker mortality ratio | **2.20** on the best-estimate rate at ages 30–55, reproducing a **premium** ratio near **2.0** once sum-related and per-policy expenses are added back | **[std]** (12) |
| *Berufsgruppen* | Occupation is a rating factor but **far weaker than on a *Berufsunfähigkeitsversicherung***. Most tariffs use a small number of classes, or none below a listed set of hazardous occupations attracting a *Risikozuschlag* or a decline | mechanic 9; **no class list, count or loading asserted** (gap 22) |
| Hazardous pursuits | Parachuting, technical diving, motorsport, mountaineering, combat sports, extended stays in high-risk regions — handled by a *Risikozuschlag* or an individually agreed exclusion at underwriting, **not** by a standing clause | mechanics 9, 13 [unverified] |
| Underwriting outcomes | Accept at standard rates; accept with a *Risikozuschlag* and/or an individually agreed *Leistungsausschluss*, subject to the applicant's acceptance; defer; decline | [R4]; mechanic 9 |
| *Anzeigepflicht* remedies | On a breach the insurer may **adjust the contract retrospectively** — writing in the *Risikozuschlag* or exclusion that would have applied — instead of refusing to perform, and for simple or gross negligence this is the usual outcome | [R4] [REG-R30]; inherited corroboration |
| Time limits on those remedies | **Five years** from conclusion for negligent breach; **ten years** for intentional or *arglistig* breach — and the placement was right: "Die Rechte des Versicherers nach § 19 Abs. 2 bis 4 erlöschen nach Ablauf von fünf Jahren nach Vertragsschluss ... Hat der Versicherungsnehmer die Anzeigepflicht vorsätzlich oder arglistig verletzt, beläuft sich die Frist auf zehn Jahre", § 21 Abs. 3. § 19 carries the duty and the remedies and no period. *Anfechtung wegen arglistiger Täuschung* is preserved by § 22 in one sentence | [R4] [REG-R30] |
| *Vorläufiger Versicherungsschutz* | Provisional cover between application and acceptance, capped in amount and duration and sometimes limited to accidental causes | mechanic 8 [unverified]; French analogue [`frlib` S2] [`frlib` S3] |

12. **No published smoker/non-smoker ratio was obtained** (gap 1). The market's rule of thumb is
    that a smoker pays roughly twice a non-smoker's premium at these ages, and the insured-lives
    smoker gap at working ages is consistently reported in the two-to-three range [unverified];
    **2.20 on mortality is the mid-point of that range**. The gap between 2.20 and the derived
    premium ratio of about 2.04 is the sum-related and per-policy expense element, which does not
    scale with mortality — the reason a mortality ratio and a premium ratio are not the same
    number.

### Charges

**German carriers do not disclose their charge structure for this product, and the absence is
structural** (mechanic 10, research gap 8). Every row below is **[std]**. The *shape* is the
standard German three-part one and is not in doubt; no level for any of them is public.

| Parameter | Representative value | Basis |
|---|---|---|
| α — *Abschluss- und Vertriebskosten* | **25 ‰ of the *Beitragssumme***, incurred at issue and amortised in the tariff | ceiling [R10] [REG-R16]; level **[std]** (13) |
| *Höchstzillmersatz* | The *Zillmersatz* may not exceed **25 ‰ of the *Beitragssumme***, cut from 40 ‰ by the LVRG with effect from 1 January 2015; **the rate in force at conclusion applies for the whole term** | [R10] [REG-R16] [REG-R20]; inherited corroboration |
| Of which *Abschlussprovision* | **20 ‰ of the *Beitragssumme***, the rest being non-commission acquisition cost | **[std]** (13) |
| β — premium-related *Verwaltungskosten* (tariff loading) | **5,0 % of each *Bruttobeitrag*** | **[std]** (13) |
| β — premium-related administration (actual cost) | **3,0 % of each *Zahlbeitrag*** | **[std]** (14) |
| *Bestandspflegeprovision* | **1,0 % of each *Zahlbeitrag*** from policy year 2 | **[std]** (14) |
| γ — sum-related annual *Verwaltungskosten* | **0,30 ‰ of the *Versicherungssumme*** a year, inflating at 2,0 % a year in the cash flow while the tariff loading is level | **[std]** (13) (14) |
| Claim handling | **250 € per death claim** | **[std]** (13) |
| *Effektivkosten* / reduction in yield | **Not owed.** § 2 Abs. 1 Nr. 9 VVG-InfoV confines the duty to a contract "bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist" — the same test as § 169 Abs. 1 VVG. A reduction in yield would also presuppose a yield | [R17] [R2]; mechanic 10 |
| Charge disclosure | **Owed, per contract, in euro.** § 2 Abs. 1 Nr. 1 and Abs. 2 VVG-InfoV require the *Abschlusskosten* as one total and the other costs as a share of the annual premium, the *Verwaltungskosten* separately again; § 4 Abs. 2 puts them on the *Informationsblatt*. What does not exist is a **published rate card** | [R17] [S1] [S2] [S3] |
| Premium tax | **None** — VersStG 2021 § 4 Abs. 1 Nr. 5 Buchst. a exempts a contract creating claims "im Fall des Todes". Note Satz 2: the exemption does not extend to an *Unfallversicherung* rider | [R16] |

13. **No observed range exists for any of these.** The one thing the corpus fixes is the
    *Höchstzillmersatz* ceiling of 25 ‰ [R10] [REG-R16], and the composite **assumes a term tariff
    runs at the cap** — which **may well be wrong**: a slim direct-channel acquisition cost would
    sit far below it [S3] [S12], and this is the single [std] charge most likely to be overstated.
    The 20 ‰ / 5 ‰ split between commission and other acquisition cost exists so the model's
    `commissions` column is not empty and so neither is double-counted against α.
14. **The tariff loading and the actual cost are deliberately different numbers, and the difference
    is the *Kostenüberschuss*.** A German RLV's technical result is *Risikoüberschuss* first and by
    a wide margin, *Kostenüberschuss* second and modest, and *Zinsüberschuss* third and negligible
    (mechanic 6) — the mirror image of the endowment, where the interest result dominates. Modelling
    the tariff's β at 5,0 % and the actual collection cost at 3,0 % makes the cost result appear in
    `net_cf` rather than being assumed away. **It is not returned to the policyholder in the base
    run**: the MindZV's *übriges Ergebnis* limb carries a different minimum share from the
    *Risikoergebnis* limb, and the research file gives no basis on which to split a German term
    tariff's expense result [R9] [REG-R18]. That is a stated simplification and a listed pitfall,
    not an oversight. The 2,0 % inflation on γ against a level tariff loading means the cost result
    narrows over a long term and eventually reverses, which is a real feature of a 25-year contract.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| *Rückkaufswert* | **No statutory duty on *Kündigung*.** § 169 Abs. 1 VVG confines it to a risk "bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist"; a term assurance's is not. **But the wordings still provide one**, at a nil or nominal amount: [S1] § 13 Abs. 8 and [S4] § 13 pay "den Rückkaufswert entsprechend § 169" where the paid-up sum fails a minimum, [S4] as *Deckungskapital* less a **60 % Abzug** with a *Rückkaufswerte* table annexed to the *Versicherungsschein*; [S3] § 15 Abs. 10 pays nothing | [R2] [S1] [S3] [S4] [REG-R28]; **scope limitation verified from the canonical XML** |
| *Beitragsfreistellung* / *beitragsfreie Versicherungssumme* | The right exists under § 165 VVG and **is exercised — but only on a constant sum insured**. [S3] § 15 Abs. 1 computes the paid-up sum from the *Deckungskapital* with § 169 Abs. 3's five-year floor and ends the contract only below **300 €**; [S4] § 13 Abs. 3 uses **2 500 €**. On a **falling** sum insured there is no *Deckungskapital* at all and "eine Beitragsfreistellung ist nicht möglich" [S3]. In the early years the amount is "keine oder nur geringe" on either | [R3] [R2] [S1] [S3] [S4] [REG-R28]; mechanic 11 |
| Effect of a *Kündigung* | **Not pure termination in the model wordings.** [S1] § 13 Abs. 8 and [S4] § 13 Abs. 2 convert the contract, wholly or partly, into a *beitragsfreie Versicherung*; the contract ends, against a *Rückkaufswert* where one exists, only if the paid-up sum fails the minimum. [S3] § 15 Abs. 10 does terminate outright — "fällt kein Rückkaufswert an" — and refunds the unexpired part of a prepaid premium | [R2] [R8] [S1] [S3] [S4]; mechanic 11 |
| Termination by the policyholder | § 168 Abs. 1 VVG: at the end of the current ***Versicherungsperiode***, and § 12 VVG makes that period follow the *Zahlweise* — "falls nicht die Prämie nach kürzeren Zeitabschnitten bemessen ist, der Zeitraum eines Jahres" — so a **monthly-paying contract is terminable monthly**. **Both retrieved carriers give more**: termination "jederzeit zum Ende des laufenden Monats" whatever the *Zahlweise* [S3] § 15 Abs. 9, [S4] § 13 Abs. 1 | [R8] [S3] [S4] [REG-R28] |
| Non-payment path | **§ 166 VVG does not do this work, and its title is *Kündigung des Versicherers*.** Abs. 1 says only that where the **insurer** terminates, "wandelt sich mit der Kündigung die Versicherung in eine prämienfreie Versicherung um", with § 165 applying. The demand machinery is **§ 38 Abs. 1**, and its minimum deadline is **two weeks**, not a month: a *Zahlungsfrist* in *Textform* "die mindestens zwei Wochen betragen muss", itemising the arrears and stating the consequences. § 166 Abs. 3 only obliges the insurer to point out the coming conversion when it sets that deadline | [R8] [REG-R28] |
| What actually happens here | **Not a collapse into simple termination — that reading was wrong.** The conversion produces a real paid-up sum on a constant sum insured and fails only below the carrier's minimum [R3] [S3] [S4]. Where it fails, and on a falling sum insured where no *Deckungskapital* exists at all, the general German lapse path and a plain *Kündigung* do reach the same place | [R3] [R8] [S3] [S4]; mechanic 11 |
| Alternatives carriers offer instead | *Beitragsstundung*, a temporary *Ruhen*, a reduction of the *Versicherungssumme* | mechanic 11 [unverified]; research gap 10 |
| Expiry | Cover ceases at the end of the *Versicherungsdauer*; **nothing is payable**; no maturity value, no renewal beyond the *Endalter* and no conversion into a savings contract in the base design | [R1] [R2] [S5] [S15] |
| Reinstatement | No general contractual reinstatement right is asserted; a lapse is final in the composite | scope **[std]** (16) |
| Effect on the model | Lapse is modelled as a **pure decrement with no benefit attached**, and `claims_lapse` is **0.00 at every duration** — asserted in code on every model point rather than left to prose. **Read this as a best-estimate approximation of a nil-or-nominal amount, not as a structural identity**: a *Beitragsfreistellung* pays nothing at the time in any wording, so the cash flow is right either way, but on a constant-sum tariff the exiting policyholder may keep a small paid-up cover or take a small *Rückkaufswert*, and this model represents neither | [R2] [R3] [R8] [S1] [S3] [S4]; mechanic 11 |

15. **Gap 2, now closed — and it closed against the reading built on it.** § 169 Abs. 1 does turn on
    whether the insurer's obligation is *gewiss*, verbatim, so no surrender-value duty attaches to a
    term assurance on *Kündigung*. **§ 165 carries no such limitation**, and §§ 152 Abs. 2, 161
    Abs. 3 and 165 Abs. 1 Satz 2 each route a term contract to § 169 for the *amount*. What was
    wrong is the sentence that followed: "the practical result is corroborated by **uniform** market
    practice". It is not uniform. The GDV model wording and the Hannoversche AVB both pay a
    *Rückkaufswert*, less a *Stornoabzug*, where the paid-up minimum fails [S1] [S4]; Cosmos pays
    nothing [S3]. **The amount is nil or nominal in every wording; the design is not the same in
    all of them.** France, by contrast, is categorical and better evidenced: art. L. 132-23
    alinéa 1 forbids a *temporaire décès* from carrying a *rachat* or a *réduction* at all, and was
    retrieved in full [`frlib` R3] — so **Germany and France differ here in kind, not only in
    amount**, and a modeller porting this model to France and keeping the § 161 *Rückkaufswert*
    substitution would introduce a benefit French law forbids.
16. Nothing in the research file sets out a reinstatement provision, and a final lapse is also the
    conservative choice on a product with no cash value to reinstate against.

---

## Contractual mechanics

### *Bruttobeitrag* → *Zahlbeitrag*: the *Überschussbeteiligung* as *Beitragsverrechnung*

**This is the central mechanic of the German term product and the one an implementation gets
wrong.** The operative rule, in the form the market states it:

    Zahlbeitrag(t) = Bruttobeitrag × (1 − v(t)),   0 ≤ v(t) < 1

with `v(t)` the declared *Beitragsverrechnungssatz* for the year [R5] [R9] [S5]. **Two carrier
wordings state exactly this identity, independently, and one of them puts numbers on it.** Cosmos:
"Die einzelne Versicherung erhält ab Beginn laufende Überschussanteile, die monatlich zugeteilt
werden. Die Überschussanteile (**Sofortrabatt**) werden **in Prozent des Bruttobeitrags** festgesetzt
und mit den laufenden Beiträgen verrechnet" [S3] § 3 Abs. 2 b. Hannoversche: "Die Versicherungen
erhalten für jedes Versicherungsjahr jeweils zu dessen Beginn einen **Jahresgewinnanteil in
deklarierter Höhe**. Der Jahresgewinnanteil wird **in Prozent des Tarifbeitrags** festgesetzt" and is
credited as a *Sofortgutschrift* against each instalment [S4] § 20 Abs. 3 b. The *Bruttobeitrag* —
which both carriers also call the *Tarifbeitrag* — is computed on **first-order
*Rechnungsgrundlagen*** and is **what the contract guarantees**; the declared share is netted against
it **before billing** rather than credited to an account there is none of. It follows from § 153 VVG's
requirement that the allocation be ***verursachungsorientiert*** on a product with no reserve to
credit [R5] [REG-R24], and both wordings cite § 153 by name in their opening sentence.

**One observed value of `v`, and it is worth stating precisely because the library previously had
none** (research gap 1, closed for one carrier). Cosmos's published *Muster-Informationsblatt* prices
a model case — **age 41 at entry, 19-year term, Bankkaufmann, 100 000 € sum insured** — at a monthly
*Tarifbeitrag* of **18,21 EUR** against a first-year *Zahlbeitrag* of **8,20 EUR**, so
`v = 1 − 8,20/18,21 = 0,550` and the ratio `Zahl/Brutto = 0,450`. The Comfort variant of the same
tariff family gives 23,68 against 10,66, i.e. `v = 0,550` again, and an older specimen of the same
model case gives 19,75 / 8,89 and 25,68 / 11,55 — `v = 0,550` in all four [S2]. **That the rate is
identical across product variants and stable across editions is § 138 VAG's *Gleichbehandlung*
made visible**: one declared rate per *Gewinnverband*, not a per-contract negotiation [R11] [S1].
**This is one direct writer's model case and is not generalised**: `v` is not set from it anywhere in
this library, and the model's `v_d` remains derived from `m` and the MindZV minimum. It is used as a
**check**, and the check is instructive — the observed 0,450 sits at the very bottom of the argued
0.45–1.00 range and well below the representative 0.57.

**Why the spread is wide, and why that is not a compliment.** An RLV's technical result is almost
entirely *Risikoergebnis*, and the MindZV obliges the insurer to allocate at least **90 %** of it to
policyholders [R9] [REG-R18]. So: the insurer prices on `q1 = (1 + m)·q2`, with `q2` the best
estimate for a medically selected portfolio and `m` the aggregate *Sicherheitszuschlag* [R12]; actual
claims run at roughly `q2`, giving a margin of `m/(1 + m)` of the risk element; and at least 90 % of
that margin must go back, *Beitragsverrechnung* being the only route available. **A wide spread is
evidence of a prudent first-order basis, not of a generous insurer**, and a narrow one of a basis
struck close to expected experience — **neither is a quality judgement**, the nuance the consumer
press tends to lose [S15] [S17].

**The counter-intuitive consequence, and the most useful single result in this specification.**
Because 90 % of the extra margin is returned, **raising the prudence of the first-order basis moves
the *Bruttobeitrag* a great deal and the *Zahlbeitrag* hardly at all.** Working the [std] calibration
through three levels of `m` at entry age 35, 300 000 €, 25-year term:

| *Sicherheitszuschlag* `m` | First-order / best-estimate | *Bruttobeitrag* p.a. | *Zahlbeitrag* p.a. | Zahl / Brutto |
|---|---|---|---|---|
| 1.00 | 2.00 | 1,180 EUR | 730 EUR | 0.62 |
| 1.25 | 2.25 | 1,316 EUR | 753 EUR | 0.57 |
| 1.50 | 2.50 | 1,451 EUR | 775 EUR | 0.53 |

The *Bruttobeitrag* moves by **23 %** across that range; the *Zahlbeitrag* by **6 %**. **All six
figures are [std] constructions and none is a market observation**; the *result* they demonstrate is
not a construction — it follows from the MindZV 90 % rule [R9] — and it is why two German carriers
can quote nearly identical *Zahlbeiträge* on very different *Bruttobeiträge*.

**Modelling ruling.** The implementation **derives** the *Zahlbeitrag* from the first-order premium
and the MindZV allocation rather than treating `v` as a free input, so the *Beitragsverrechnungssatz*
is an **output of the surplus mechanic** — which is what it is in the real product — and publishes
**both** premium streams, `net_cf` built from the billed one and the guaranteed one available as the
stress. **The MindZV section numbering is unsettled** between the sibling delib research and the
cross-product reference library, so **no MindZV section number is cited anywhere in this product's
documents**; the three percentages are inherited and used [R9] [REG-R18] (gap 4).

**Three unrelated things are called "netto" in this product** — the *Nettoprämie* of actuarial usage
(the risk premium before loadings), the *Nettobeitrag* of consumer usage (a synonym for the
*Zahlbeitrag*), and the *Nettotarif* of distribution usage (a commission-free tariff sold through
fee-based advice) — **and confusing them is the classic implementation error**. These documents use
***Zahlbeitrag*** and ***Nettoprämie*** and never the bare word *Nettobeitrag*; the three senses are
tabulated in the technical notes, where the notation is fixed [S5] [S15] [S16] [REG-R47] [unverified].

### Only the *Bruttobeitrag* is guaranteed — the asymmetry

§ 163 VVG permits an increase of the ***Bruttobeitrag*** only on an **unforeseen and not merely
temporary** change in the calculation bases, where the adjustment is necessary to safeguard permanent
fulfilment and an **independent *Treuhänder*** confirms it; the policyholder may demand a benefit
reduction instead, and the adjustment is **excluded to the extent the benefits were insufficiently
calculated at the outset and a diligent actuary should have recognised it** — the insurer may not
reprice its way out of its own mispricing [R6] [REG-R27]. **On a German RLV *Bruttobeitrag* that
route is essentially never used** [unverified]. What moves the customer's bill is the
***Überschussdeklaration***: cutting the *Beitragsverrechnung* raises the *Zahlbeitrag* toward the
*Bruttobeitrag* with **no § 163 procedure, no *Treuhänder* and no policyholder remedy**, because no
guaranteed term has changed [R6] and § 153 confers an entitlement to *participate*, not to a level
[R5]. That asymmetry is why the German market publishes both numbers, why the spread is a rated
criterion [S17] [R20], and why a model treating the *Zahlbeitrag* as guaranteed is making a
**behavioural** assumption and must label it as one.

**§ 138 VAG is what makes the *Zahlbeitrag* modellable at all.** *Bei gleichen Voraussetzungen dürfen
Prämien und Leistungen nur nach gleichen Grundsätzen bemessen werden* [R11] [REG-R8] — so an insurer
declares **one rate per tariff generation and rating cell** rather than negotiating individual
discounts, and the *Zahlbeitrag* is a deterministic function of the *Bruttobeitrag* and a declared
rate. It also settles a question the model would otherwise guess: **the declared rate is struck on
the tariff's own unisex basis, not on the individual policy's sex**, so a man and a woman in one
rating cell receive the same declaration though their best-estimate mortality differs. **The unisex
cross-subsidy therefore appears in the projected cash flows rather than in the price**, which is
exactly where German law puts it.

### The premium is level, and the benefit need not be

The premium is struck at the *Eintrittsalter* and held there for the whole *Beitragszahlungsdauer*.
**This is the largest structural difference from the French *temporaire décès***, where every carrier
in the `frlib` corpus whose basis is stated prices on an annually revisable attained-age basis and
none prices level [`frlib` S1, S2, S3, S6, S7, S9, S10]. The German contract is the one an
Anglo-American reader expects; the French one is not. Universality is [unverified] at carrier level
but follows from two things that make no sense on an annually repriced contract: a guaranteed
*Bruttobeitrag* [R6], and a *Zillmerung* regime financing acquisition cost against a reserve a
repriced contract never builds [R10]. Two consequences reach the model. **The contract prefunds** —
the level premium exceeds the rising natural risk premium early and falls short late, so a real if
small *Deckungskapital* results. And **premium and benefit shape decouple**: the premium is flat
while the benefit falls on two of the three shapes, the opposite of the French product where the
premium stream carries the shape of the liability.

The three sums-insured shapes are **one schedule**, `S(t) = S(0) × f(t)` with `f(1) = 1`, priced on
the same underwriting and the same *Rechnungsgrundlagen*: ***konstant*** for a need that does not
amortise; ***linear fallend***, cheap, simple and **a poor match to an annuity loan**, whose balance
falls slowly at first and quickly at the end while a linear schedule does the opposite; and
***annuitätisch fallend***, following the outstanding balance of an annuity loan at a nominal rate
**agreed at issue** — a contractual schedule parameter, **not the borrower's actual loan rate**.
Carriers price the falling shapes lower for the same **initial** sum **mechanically, not as a
discount**. A fourth, **rising** shape is a different mechanic — the *Dynamik* and the
*Nachversicherungsgarantie* — because the premium rises with it and the § 161 clock restarts for the
increment. An ***abgekürzte Beitragszahlungsdauer*** is where the *Deckungskapital* is largest,
everything after the last premium being funded from the reserve [unverified].

### *Selbsttötung* — § 161 VVG, and how it differs from the French rule

| | Germany [R1] | France [`frlib` R1, R3] |
|---|---|---|
| Window | **Three years** from conclusion | **One year** from conclusion |
| Effect inside the window | Insurer *leistungsfrei*; **pays the *Rückkaufswert* instead** | Cover "de nul effet" — **nothing is paid** |
| What the substitution is worth on a term product | **Nil or nominal** — there is no surrender value | Nil by construction — the product may not have one |
| Extension by agreement | **Expressly permitted** | Not provided for; the statutory minimum is the rule |

The two systems reach **nearly the same economic answer by opposite routes**, and the German answer
applies for **three times as long**. Two things the model deliberately cannot represent. **The
mental-illness exception is not a formality** — it is the ground on which German *Selbsttötung*
claims are actually litigated [R23] — so the rule is not a clean contractual switch and a
best-estimate model cannot carry a litigated state of mind; it is applied as a **benefit switch over
the first three policy years on the suicide share of deaths**. And **whether the clock restarts on an
increase is now established for Germany** (gap 9, closed): § 161 itself is silent, running its clock
from *Abschluss des Versicherungsvertrags*, but three wordings say the same thing in the same words —
"Wenn unsere Leistungspflicht durch eine Änderung des Vertrages erweitert wird oder der Vertrag
wiederhergestellt wird, beginnt die Dreijahresfrist bezüglich des geänderten oder wiederhergestellten
Teils neu" [S1] § 5 Abs. 3, [S3] § 2 Abs. 4, [S4] § 19 Abs. 3. **The model restarts it for the
increment only, and that is market practice, not a guess.** The French statute restarts its one-year
clock for the increment in the same way [`frlib` R1].

### The *Rückkaufswert* — why it is nil or nominal, and what does *not* collapse with it

An earlier draft of this section said that terminating a German RLV returns nothing, full stop. **The
retrieved wordings show that is too strong, and the correction matters more than the original claim.**
Two things are true and they are different things.

**One: there is almost nothing to pay out — but it is not nothing.** An RLV has no *Sparanteil* in
the endowment's sense, but a level premium charged against a **rising** mortality rate necessarily
overcharges early and undercharges late, and the difference is held as a *Deckungskapital* that
builds, peaks near the middle of the term and **runs off to exactly zero at expiry** — a low
single-digit percentage of the *Versicherungssumme* at its peak on the [std] calibration, and
**negative or nil through much of the term** after *Zillmerung*. The wordings say this in their own
voice: the *Kostenverrechnung* means that "in der Anfangszeit Ihres Vertrages ... keine oder nur
geringe Mittel" are available, "auch in den Folgejahren ... wegen der benötigten Risikobeiträge"
[S1] § 14 Abs. 4, [S3] § 16 Abs. 4. **Stating "there is no *Sparanteil*, therefore no reserve" is
wrong, and a model built on it will fail its own closure check.**

**Two: no *statutory* duty to pay it out attaches on *Kündigung*** — and this, unlike before, is
read rather than inferred. § 169 Abs. 1 VVG applies where a policy insures "ein Risiko ..., bei dem
der Eintritt der Verpflichtung des Versicherers **gewiss** ist"; a term assurance's is not [R2]
[REG-R28]. Gap 2 is closed and the tag removed.

**But the second point does not carry the first, and the market does not treat it as if it did.**
§ 169 defines the *Rückkaufswert*; it does not abolish it here, and §§ 152 Abs. 2, 161 Abs. 3 and
165 Abs. 1 Satz 2 each send a term contract to it for the amount. The GDV model wording then pays it:
*Kündigung* converts the contract into a *beitragsfreie Versicherung*, and only where that paid-up
sum fails a carrier-set minimum does the policyholder receive "den Rückkaufswert entsprechend § 169
des Versicherungsvertragsgesetzes (VVG)", less a *Stornoabzug* [S1] § 13 Abs. 4 and Abs. 8. The
Hannoversche AVB does the same at a 2 500 € minimum, with an *Abzug* of **60 % des Deckungskapitals**
and a *Rückkaufswerte* table annexed to the *Versicherungsschein* — for every tariff except its two
falling-sum ones, which build no *Deckungskapital* [S4] § 13. Cosmos alone terminates outright:
"Bei einer vollständig gekündigten Versicherung fällt kein Rückkaufswert an und Ihre Versicherung
erlischt" [S3] § 15 Abs. 10. **So the honest statement is about magnitude: on a German term assurance
the surrender value is nil or nominal, and whether a wording pays it at all is a carrier choice.**

***Zillmerung* on a term product is a peculiar thing — and it is optional.** The 25 ‰ cap is a
fraction of the *Beitragssumme*, 25 times the annual premium on a 25-year contract, while the
*Deckungskapital* it is written into is tiny — **so the Zillmer charge is large relative to that
reserve**, and the *gezillmerte Deckungsrückstellung* of a term contract is negative for a long
stretch and never becomes large. **Gap 11's first half is closed**: DeckRV § 4 draws no distinction
between product types, and both the model wording and the Cosmos AVB apply "das Verrechnungsverfahren
nach § 4 der Deckungsrückstellungsverordnung" to a term contract and quote the ceiling as **2,5
Prozent** of the premiums payable over the term [S1] § 14 Abs. 2, [S3] § 16 Abs. 2. Two refinements
the earlier draft lacked. **The clause is conditional**: the GDV model carries it in a footnote as
to be included "nur bei der Verwendung des Zillmerverfahrens", so a carrier need not zillmer at all
[S1]. **And 25 ‰ is not the acquisition cost** — it bounds only the part recovered through
*Zillmerung*, because "die restlichen Abschluss- und Vertriebskosten werden über die gesamte
Beitragszahlungsdauer verteilt" [S1] § 14 Abs. 3, [S3] § 16 Abs. 3. The *Nullstellung* question is
**still not established** [R10] [R21] [REG-R16] (gap 11, second half); **the model publishes no
balance-sheet reserve, so it does not reach these cash flows.**

**What does and does not follow from the small surrender value.** The § 165 paid-up right runs
through a **minimum-benefit test** whose fallback is payment of the *Rückkaufswert* — but the right
itself is live on a constant sum insured and produces a real, small paid-up cover, and only the
**falling**-sum variant is empty, "kalkulationsbedingt kein Deckungskapital" and so "eine
Beitragsfreistellung ist nicht möglich" [S3] § 15 Abs. 4. The insurer-side path is **§ 38 VVG** for
the *Zahlungsfrist* and § 166 VVG for the conversion, not § 166 for both [R3] [R8] [REG-R28]. And
§ 168's termination right runs to the end of each *Versicherungsperiode*, which follows the
*Zahlweise* — so **a monthly-paying contract is terminable monthly**, and **German term-life lapse is
not concentrated at policy anniversaries** the way an annual-mode book's is: a caution for any model
assuming anniversary-only exits, and one the reference implementation now expresses in code rather
than in prose, the projection having moved to a monthly grid. What carriers offer instead — *Beitragsstundung*, a temporary *Ruhen*, a reduction of the
sum insured — is [unverified] (gap 10).

### The *Rechnungsgrundlagen*, and the unisex problem

The mortality basis is ***DAV 2008 T***, with ***DAV 2008 T NR*** and ***DAV 2008 T R*** [R12]
[REG-R48], inherited corroboration: derived over **2006 to 2008** from German insurers' own policy
data with German population statistics; the *Richtlinie* **regulates both the derivation methodology
and the procedure for setting the *Sicherheitszuschläge***; the variants are **suitable for premium
calculation** but **not for policies written without a *Gesundheitsprüfung***; adopted **4 December
2008**, restated as a *Fachgrundsatz* dated **29 November 2022**. **The values are the property of
the Deutsche Aktuarvereinigung, are not public, and are not redistributed here**; the technical notes
ship a [std] proxy and state what a replacement must preserve. **Three structural reasons the
effective first-order margin on a contract written today is large**, none a criticism of the insurer:
the table was derived on 2006–2008 experience and German mortality has improved since; it is applied
to a **medically selected** portfolio in its early durations, where selection is strongest and the
table's own allowance is generic; and the *Sicherheitszuschläge* sit on top of both — so a
first-order to second-order ratio **in the region of two** is entirely plausible. **The ratio is
[std]; the reasoning is not numeric.** A death-cover basis carries **no projected mortality
improvement**, improvement being favourable to the insurer — the exact opposite of the annuity tables
[REG-R49], and the reason a single "German mortality table" does not exist. **Unisex** makes it
worse: DAV 2008 T is sex-distinct, so every German unisex term tariff is a **blend at a mixing ratio
the carrier chooses from its own expected new-business mix**, proprietary and unpublished [R13]
[REG-R34]. And **no German insurer publishes its own basis** — the AVB say the calculation follows
*die anerkannten Regeln der Versicherungsmathematik* and stop there [unverified]. `frlib` reached the
same position for France with one difference: a French carrier published a complete attained-age
gross rate card [`frlib` S3], and **no German carrier publishes anything comparable** (gap 1).

### *Verbundene Leben*, the *Über-Kreuz-Versicherung*, and the decrements

***Risikolebensversicherung auf verbundene Leben*** pays **once, on the first death**, and the
contract then **ends**, leaving the survivor with no cover; both lives are underwritten and both give
the § 150 consent [R7], and **no premium ratio against two single contracts is asserted** (gap 15).
**The separation problem** is the standard consumer-press criticism: on divorce the contract covers
two people who no longer want a joint benefit and cannot halve it, and absent a conversion right into
two single contracts the only exit is termination with nothing back [unverified].

***Über-Kreuz-Versicherung*** is **two contracts, crossed**: A owns and is beneficiary of a contract
on **B's** life and vice versa, each paying on **his own** contract out of **his own** funds. **The
cover is identical to two ordinary single contracts, and the model is indifferent to the structure**
— worth saying so a reader does not go looking for a mechanic that is not there. **The tax outcome is
not identical, and that is the whole point.** Under the ordinary structure the benefit is an
***Erwerb von Todes wegen*** under § 3 Abs. 1 Nr. 4 ErbStG charged against the beneficiary's
*Freibetrag* [R15] [REG-R46]; under the crossed structure A receives a payment under a contract A
owns and paid for, nothing passes from B's estate, and there is **no *Erwerb von Todes wegen***. Two
conditions, both [unverified]: premiums paid **from the surviving partner's own funds, verifiably**,
and the § 150 consent [R7]. On 300 000 € to a **spouse** the 500 000 € *Freibetrag* absorbs it and
the tax is nil; to an **unmarried partner** the *Freibetrag* is 20 000 €, *Steuerklasse* III applies
from 30 %, and the liability is on the order of **84 000 € — 28 % of the sum insured** [R15]
[unverified]. **So it is close to compulsory for unmarried couples and close to pointless for married
ones below the spousal allowance**, which is why a real German RLV book contains a large share of
cross-owned policies [REG-R46]. **Every figure in that arithmetic is [unverified]** (gap 18); the
structural conclusion does not depend on the numbers.

**Two decrements only: death and lapse** — the simplest decrement structure of the ten delib
products. A contract ends on death (benefit paid), on lapse or non-payment (nothing paid), or at the
end of the *Versicherungsdauer* (nothing paid). Two behavioural facts follow and neither is in the
base run. **Anti-selective lapse is real and is not modelled**: healthy lives can re-underwrite into
a cheaper contract and impaired lives cannot, so a term book's mortality drifts up relative to a
table calibrated on the whole cohort. And **the *Zahlbeitrag* is itself a lapse driver**: a cut in
the *Beitragsverrechnung* raises the bill without any change the policyholder agreed to, and his
remedy is to leave [R6] — **so a model that raises the *Zahlbeitrag* toward the *Bruttobeitrag* in a
stress and leaves the lapse assumption unchanged is understating the stress.**

---

## Riders and options

**Parameterized, and off in the base run.** ***Nachversicherungsgarantie*** is **the most important
option on the product**: the policyholder may raise the *Versicherungssumme* **without a new
*Gesundheitsprüfung*** on a named life event. The event families that recur across the German market,
**now established from a carrier wording** (gap 7, closed). [S3] § 13 gives the list in full:
marriage; birth (a multiple birth counting once) or adoption of a child; financing from 50 000 €,
purchase or start of construction of an owner-occupied home; first permanent employment after
finishing study or after finishing vocational training; first self-employment in a chamber-regulated
occupation providing the main income; a permanent rise of at least ten per cent in gross monthly
basic pay; first crossing of the *Beitragsbemessungsgrenze* in the statutory pension scheme; and
exemption from statutory pension insurance as a self-employed craftsman. Note what is **not** on it
and was on the earlier draft's guess: **divorce**, and **loss of other death cover** — neither
appears. The restrictions are equally concrete: an **exercise window of twelve months** after the
event; a per-event cap of **20 % of the original sum insured, at most 50 000 €**, with a minimum
increase of 5 000 €; each event usable once, birth or adoption twice, and **at most five occasions in
all**; and the right ends once the insured person is **older than 50**. It rests while the contract is
not premium-paying, and is barred once a *schwere Krankheit* benefit has been claimed. Some tariffs
add an ***ereignisunabhängige Nachversicherung*** in the first years [unverified] — none of the three
retrieved wordings has one. Actuarially it matters because an increase without underwriting is an
increase in expected claims the increment's tariff does not reflect, bounded only by the trigger and
the caps — [S3] § 13 Abs. 5 prices the increment at the attained *rechnungsmäßiges Alter*, the
recorded occupation, the remaining term and any agreed *Risikozuschlag* — and it is the point at
which the § 161 clock restarts for the increment, which all three wordings say expressly [R1] [S1]
[S3] [S4]. The implementation carries it as an **exercised-increase
schedule** — a cumulative uplift by policy year, the increment repriced at the attained age with its
own three-year window — and ships a `keine` schedule as the base. ***Dynamik*** is **the same
mechanic with a schedule instead of a trigger**, with a right of *Widerspruch* that typically lapses
after a stated number of consecutive objections [unverified], so one input serves both.
***Risikozuschlag*** is `rating_factor` (footnote 9).

**Described, not modeled — and the omissions are deliberate.** ***Verlängerungsoption***, extension
at expiry without renewed underwriting at the tariff then in force. ***Umtauschoption***, conversion
into a *kapitalbildende Lebensversicherung* without a new *Gesundheitsprüfung*; historically common,
now rare. ***Vorgezogene Todesfallleistung***, early payment on medical evidence of terminal illness
with a limited life expectancy — a growing German option and **not a *PTIA*-style disability
acceleration**, the trigger being prognosis, not incapacity. ***Unfalltod-Zusatzversicherung***
(UZV), an additional sum on accidental death within a stated period of the accident; the German
analogue of the French *doublement accidentel*, present at five of eight carriers in the `frlib`
corpus [`frlib` S1, S2, S6, S7, S9]. ***Berufsunfähigkeits-Zusatzversicherung*** (BUZ) and
***Beitragsbefreiung bei Berufsunfähigkeit***, the standalone form being
`products/berufsunfaehigkeit/` under §§ 172–177 VVG [REG-R29]. ***Vorläufiger
Versicherungsschutz***, provisional cover between application and acceptance, capped in amount and
duration and sometimes limited to accidental causes. All [unverified], **none modelled**, and
recorded so a reader knows the omissions are deliberate rather than overlooked.

***Überschussverwendung* forms other than *Beitragsverrechnung*.** Four are used in the German
market for a death-benefit contract. **Correction:** an earlier draft attributed a four-component
surplus vocabulary — *Zins-*, *Risiko-*, *Kosten-* und *übrige Überschüsse* — to a carrier's own page
about this product [S5]. That page uses no such vocabulary. It names **three** sources, and so do the
regulation and both retrieved wordings: the *Risikoergebnis*, the *übrige Ergebnis* and the
*Kapitalanlageergebnis* [R9] [S1] [S3] [S4] — of which, on this product, "stehen ... keine oder
allenfalls geringfügige Beträge zur Verfügung, um Kapital zu bilden" [S3] § 3 Abs. 1 a, so only the
first two are live. **What the carrier page does establish** is that of the four forms below, the
German term market runs on two: "meist eines von zwei Modellen ... den **Todesfallbonus** und den
**Sofortrabatt**" [S5] — and both wordings carry exactly that pair, *Sofortrabatt* while premiums are
paid and *Todesfallbonus* once the contract is paid up [S3] § 3 Abs. 2 b and d, [S4] § 20 Abs. 3 b.
Prevalence beyond that pair is [unverified].

| Form | Mechanic | Effect on the model |
|---|---|---|
| ***Beitragsverrechnung*** | Surplus netted against the *Bruttobeitrag*; the customer pays less | Reduces the billed premium; sum unchanged. **The base design** |
| ***Summenzuwachs*** / *Bonussumme* | Surplus buys additional **paid-up death cover**; the sum grows year by year | Raises the benefit; premium unchanged |
| ***Verzinsliche Ansammlung*** | Surplus accumulates with interest and is paid **in addition** on death | Creates an account value on a product that otherwise has none |
| ***Todesfallbonus*** | A declared bonus sum payable in addition on death | Raises the benefit only in the year of claim |

**The implementation implements *Beitragsverrechnung* only.** *Summenzuwachs* is the one worth
implementing next, being the only one that changes the benefit rather than the premium. A
**non-participating** tariff is possible in law — § 153 VVG permits exclusion by express agreement
[R5] — is **not** the market form and **none was located** [unverified]; it ships as a model-point
value (`surplus_form = keine`) so the participating machinery can be switched off and tested against.

---

## Variations across insurers

**The honest headline: two carriers were sampled, and the industry model wording.** `frlib` put eight
French carriers side by side because eight *notices d'information* were read; the sibling delib
endowment file put six side by side, thinly, from search-result summaries. **This product can now put
two side by side, in full, and read the GDV template they are both variations on.** Two is not a
market, and every "range" in the next table is still argued rather than observed.

| Carrier | Sells an individual RLV | AVB located | Document content established | Any parameter established |
|---|---|---|---|---|
| GDV model wording [S1] | n/a — template | **yes**, Stand 21.07.2025, 18 pp. | **yes, in full** — surplus, *Selbsttötung*, paid-up, *Kündigung*, cost offset | ceiling only: 2,5 % *Zillmersatz* |
| CosmosDirekt [S3] | **yes** | **yes** — LA 803 A (04.26), 11 pp., plus LA 804 A | **yes, in full** — and the fullest of the three on NVG, smoker and exclusions | **yes** [S2]: *Tarifbeitrag* 18,21 €, *Zahlbeitrag* 8,20 €, α 2,41 %, *Rechnungszins* 0,25 % |
| Hannoversche [S4] | **yes** | **yes** — T25, Stand 09/2025, in a 32 pp. pack | **yes, in full** — surplus, *Selbsttötung*, *Kündigung*, 60 % *Abzug*, 2 500 € minimum | 60 % *Stornoabzug*; 2 500 € paid-up minimum |
| HUK-COBURG / HUK24 [S5] | **yes** | no | **guide page retrieved** — the two surplus forms, and the *Tarifbeitrag* as billing ceiling | no |
| Debeka [S6] | asserted | no — cited path now 404s; current library page carries no document links | no | no |
| Dialog [S7] | asserted | no — wordings sit behind the broker channel | no | no |
| Allianz [S8] | asserted | no — product page publishes no conditions file | no | no |
| R+V [S9] | asserted | no | no | no |
| NÜRNBERGER [S10] | asserted | no | no | no |
| LV 1871 [S11] | asserted | no — product page publishes no conditions file | no | no |
| Continentale / Europa [S12] | asserted | no | no | no |
| Seventeen further carriers [S13] | asserted | no | no | no |

**[S13] asserts one thing only — that each of those carriers offers an individual
*Risikolebensversicherung* in Germany.** It exists so this table can state honestly that a market of
this breadth exists and that none of it was sampled. **No [S13] tag appears on any parameter
anywhere in this library.**

Almost every "range" below is still **argued from structure or market knowledge**, not observed. The
"who sits where" column is the point of a variations table, and it is **no longer empty everywhere** —
the rows a retrieved document reaches now name the carrier. That is one or two observations against
a market of forty-odd carriers, so **no range below was widened, narrowed or recalibrated to fit
them**; they are recorded as checks.

| Parameter | Range carried in this specification | Who sits where | Tag |
|---|---|---|---|
| `Zahl / Brutto` ratio | 0.45 to 1.00, representative **0.57** | **CosmosDirekt at 0.450**, on a published model case at age 41 / 19 years / 100 000 €, in four specimens across two editions and two product variants [S2] | **[std]**; observation does not set it |
| *Sicherheitszuschlag* `m` implied | 1.0 to 1.5, representative **1.25** | **not established** | **[std]**, gap 6 |
| Smoker / non-smoker premium ratio | about 1.8 to 2.5, derived **2.04** | **not established** | **[std]**, gap 1 |
| *Eintrittsalter* | 18 to 65, some carriers to 70 or 75 | **not established** | **[std]**, gap 22 |
| *Endalter* | 75, with 80 and 85 offered | **not established** | **[std]**, gap 22 |
| *Versicherungsdauer* | 5 to 40 years | **not established** | **[std]**, gap 22 |
| *Mindestversicherungssumme* | 10 000 to 50 000 € | **not established** | **[std]**, gap 22 |
| Maximum sum without special underwriting | high six to low seven figures | **not established** | **[std]**, gap 22 |
| Smoker qualifying period | **twelve months** before application, no smoking or vaping, nicotine-containing or not; a later switch is a *Gefahrerhöhung* | **CosmosDirekt** [S3] § 18 | gap 22 **partly closed** |
| *Vereinfachte Gesundheitsprüfung* threshold | **not established at all** | **not established** | gap 22 |
| *Berufsgruppen* count | small, or none below a hazardous-occupation list | **not established** | gap 22 |
| *Nachversicherung* event list | nine recurring event families | **CosmosDirekt**: nine events, but not the nine guessed — no divorce, no loss of other cover [S3] § 13 Abs. 1 | gap 7 **closed** |
| *Nachversicherung* cap, window and age limit | 12-month window; 20 % of the original sum, max 50 000 €, min 5 000 €, per event; five occasions in all; ends above age 50 | **CosmosDirekt** [S3] § 13 Abs. 1–4 | gap 7 **closed** |
| *Ratenzahlungszuschlag* | 2 % / 3 % / 5 % | market convention, **no attribution** | **[std]**, gap 21 |
| *Rückkaufswert* | **nil or nominal everywhere; provided for in some wordings and not others** | **CosmosDirekt: none at all** [S3] § 15 Abs. 10. **Hannoversche and the GDV model: paid under § 169 where the paid-up sum fails a minimum**, at Hannoversche less a 60 % *Abzug* [S1] [S4] | [R2]; gap 2 closed, **and the "uniform" claim withdrawn** |
| *Selbsttötung* window | three years, statutory minimum, extendable; **restarts for the increased or reinstated part** | **statutory as to the three years; the restart is uniform across all three retrieved wordings** [S1] [S3] [S4] | [R1]; gap 9 closed |
| *Versicherungssumme* shapes offered | all three at most carriers | **not established** | mechanic 3 |
| *Verbundene Leben* offered | widely | **not established** | mechanic 14 |
| Lapse rate | 2 % to 8 % in early durations, shipped 6 / 4 / 3 % | **not established** | **[std]**, gap 13 |

**Four axes vary structurally, even though none was measured**, and a reader with one retrieved AVB
could place it on them immediately. **Channel, through the spread**: the direct channel pays no
*Abschlussprovision* to an intermediary, so more of the *Bruttobeitrag* is available for
*Beitragsverrechnung* [S3] [S4] [S12], while a large composite with tied-agent and broker
distribution sits at the narrow end [S8] [S9] — structural reasoning, not sourced. **Monoline versus
composite, through the MindZV**: a specialist term-life carrier's *Risikoergebnis* is its **entire**
technical result, so the minimum allocation binds its surplus policy directly rather than competing
with an investment result [S7] [R9]; a composite can move surplus between result sources within the
statutory minima and a monoline cannot. **Wording vintage inside one carrier**: Debeka maintains
several parallel wordings of different vintages within one product family and its
*Überschussbeteiligung* clause numbering is tariff-dependent [S6], which is why **any specific
section number attributed to a German carrier's AVB is [unverified] for that reason alone**. **What
the rating houses actually rate** [S17] [R20] [unverified]: the ***Brutto*/*Zahlbeitrag* spread is
itself a rated criterion** — a wide spread is marked down, because it measures the insurer's
unilateral headroom to raise the billed premium — and so are the ***Nachversicherungsgarantie* event
list, caps and age limit**, which is why the market has converged on a recognisable list. Neither is
used as a numeric parameter anywhere.

**What does not vary**, and all three are legal facts rather than commercial ones: the absence of
any *Rückkaufswert* and expiry without value [R2] [S5] [S15]; the three-year *Selbsttötung* window,
a statutory minimum, extendable by agreement and not shortenable [R1]; and unisex pricing,
compulsory for new business since 21 December 2012 and admitting no carrier variation at all [R13]
[REG-R34].

---

## Regulatory context

**Contract law — the VVG.** The product sits in **Kapitel 5** (*Lebensversicherung*, §§ 150–171),
whose provisions are largely ***halbzwingend*** — a deviation to the policyholder's disadvantage is
ineffective [REG-R22]. **§ 150** requires the insured life's **written consent** where the benefit
exceeds ordinary funeral costs [R7] [REG-R26], and that funeral-cost boundary is what makes
*Sterbegeldversicherung* a distinct product in German law rather than a small RLV — the reason delib
excludes it. **§ 152** gives a 30-day *Widerrufsfrist* [R8] [REG-R23]; **§ 153** the
*verursachungsorientiert* *Überschussbeteiligung* [R5] [REG-R24]; **§ 159** the *Bezugsberechtigung*
[R7]; **§ 161** the *Selbsttötung* rule [R1]; **§ 162** the forfeitures [R7]; and **§§ 165–169** the
paid-up right, the *Kündigung* right, the *Beitragsverzug* machinery and the *Rückkaufswert* [R2]
[R3] [R8] [REG-R28] — all of which, on this product, terminate in nil. **§ 19**'s question-bounded
duty, together with the five-/ten-year extinction of the insurer's remedies under it in **§ 21 Abs. 3**
[unverified], is the whole of the claims-risk story on a term contract [R4] [REG-R30], and **§ 163**'s near-total absence from this product's practice is the point [R6]
[REG-R27].

**Supervisory law — the VAG.** **§ 138 Abs. 1** requires premiums to be set **high enough** that the
undertaking can meet all its obligations and form adequate *Deckungsrückstellungen*, and forbids the
systematic and permanent use of funds not deriving from premiums to support a tariff — **which is
why German first-order bases carry margins that later emerge as *Überschuss*** [REG-R8]. **§ 138
Abs. 2** is the *Gleichbehandlungsgrundsatz* that makes the *Beitragsverrechnung* a per-cell
declaration rather than an individual negotiation [R11] [REG-R8]; the BGH tied it to § 153 Abs. 2
VVG on 18 September 2024, Az. IV ZR 436/22 [REG-R8]. **§ 139** governs participation in the
*Bewertungsreserven* and the *Sicherungsbedarf* test [R11] [REG-R9] — **economically empty on this
product**, the attributable amount scaling with a *Deckungsrückstellung* that is nil or nominal [R5]
[unverified]. **§ 140** governs the RfB [R11] [REG-R10], and **§§ 141–143** the *Verantwortlicher
Aktuar*, the *Treuhänder* and the *Altbestand* / *Neubestand* split of 29 July 1994 that every German
in-force book is organised around [REG-R11]; this specification is written for **Neubestand**.

**Reserving and the surplus regulations.** The **DeckRV** sets the *Höchstrechnungszins* — **1,00 %
for new business from 1 January 2025**, from the *Sechste Verordnung* of 19 July 2024, BGBl. 2024 I
Nr. 250 [R10] [REG-R14] [REG-R15] — and, in § 4, the *Höchstzillmersatz* of **25 ‰ of the
*Beitragssumme***, cut from 40 ‰ by the LVRG with effect from 1 January 2015, the rate in force at
conclusion applying for the whole term [R10] [REG-R16] [REG-R20]. The **MindZV** sets the minimum
allocation to the RfB from the three result sources — **90 % of the *Risikoergebnis*** (raised from
75 % by the LVRG with effect from 7 August 2014), **90 % of the *Kapitalanlageergebnis*** struck
**after** deducting the *Rechnungszinsen*, and **50 % of the *übriges Ergebnis***, with *Alt-* and
*Neubestand* treated separately and a mathematically negative minimum replaced by zero [R9]
[REG-R18]. **The first of those three is the engine of the German term product**, and it is why the
*Brutto*/*Zahlbeitrag* spread is, to a first approximation, a direct function of how prudent the
first-order basis is. **HGB § 341f** and the **RechVersV** govern the statutory
*Deckungsrückstellung* and its presentation [R21] [REG-R54]; the *Zinszusatzreserve* machinery of
DeckRV § 5 Abs. 3 [REG-R17] reaches this product only nominally.

**Conduct and disclosure.** The **VVG-InfoV** prescribes the pre-contractual information duties and
the *Produktinformationsblatt* [R17] [REG-R31]. **There is no *Basisinformationsblatt*: a pure
*Risikolebensversicherung* has no investment component and is therefore not a PRIIP** [R17]
[REG-R32] [unverified]. Two consequences follow, and both are structural absences rather than
missing documents: **there is no *Effektivkosten* figure for a term product**, because a reduction in
yield presupposes a yield; and that is a large part of why German term-life charge levels are
invisible (gap 8). Distribution sits under the **IDD** and § 34d GewO [REG-R33]. **BaFin's
*Merkblatt* 01/2023 (VA) on *Wohlverhaltensaufsicht* and *angemessener Kundennutzen* is expressly
about *kapitalbildende* products and does not reach a pure protection contract** [R19] [REG-R35] —
recorded so a reader does not import an endowment-conduct standard here; **supervisory literature
specific to German term assurance was not located** (gap 14).

**Unisex.** The ECJ held on **1 March 2011** in **C-236/09** (*Test-Achats*) that using sex as a risk
factor in insurance is incompatible with Articles 21 and 23 of the Charter, and invalidated the
Gender Directive's Article 5(2) derogation **with effect from 21 December 2012** [R13] [REG-R34]. On
the German side § 19 AGG carries the civil-law prohibition and expressly names private insurance;
§ 20 Abs. 2 Satz 1 AGG, which had allowed sex-differentiated pricing on actuarial data, was
repealed; § 33 Abs. 5 AGG preserves the old treatment for relationships concluded before that date.
**Letting a `sex` field leak into pricing reproduces a tariff unlawful in Germany since 2012** and is
a numbered modeling pitfall.

**Taxation — and the one tax that reaches this product.** The *Todesfallleistung* is **free of
*Einkommensteuer***: § 20 Abs. 1 Nr. 6 EStG taxes the *Unterschiedsbetrag* on a **survival or
surrender** payment, and a pure death benefit paid to a third party is not investment income of the
policyholder [R14] [REG-R45] [unverified] (gap 16). The 12/62 rule, the *Halbeinkünfteverfahren* and
the **50 % *Mindesttodesfallschutz*** requirement for contracts concluded from 1 April 2009 are rules
about **savings** contracts, and the last exists precisely to stop savings contracts presenting
themselves as death covers — indirect corroboration that the section does not reach a pure one.
Premiums fall among the *sonstige Vorsorgeaufwendungen* deductible under § 10 Abs. 1 Nr. 3a EStG
**within an annual ceiling in practice already exhausted by health and long-term-care
contributions**, so the effective deduction for most taxpayers is nil — **and this is now statute
rather than inference** (gap 17, closed). § 10 Abs. 1 Nr. 3a EStG names the product expressly, among
contributions "zu **Risikoversicherungen, die nur für den Todesfall eine Leistung vorsehen**".
§ 10 Abs. 4 sets the combined ceiling for Nr. 3 and Nr. 3a at **2 800 Euro** a year, or **1 900
Euro** for anyone whose health cover is wholly or partly paid for by an employer or the state — which
is most employees and pensioners — and Satz 4 disposes of the rest: where the Nr. 3 health and
long-term-care contributions already exceed the ceiling, they are deducted in full and "ein Abzug von
Vorsorgeaufwendungen im Sinne des Absatzes 1 Nummer 3a **scheidet aus**" [R14]. What does reach the product is the ***Erbschaftsteuer***:
**Germany has no insurance-specific death-benefit tax regime**, so the benefit is an ordinary
*Erwerb von Todes wegen* under § 3 Abs. 1 Nr. 4 ErbStG at the beneficiary's own *Steuerklasse* and
*Freibetrag* [R15] [REG-R46]. That is the sharpest contrast with France in the whole product: French
law carves life insurance out of ordinary succession through CGI arts. 990 I and 757 B, with a
152 500 € per-beneficiary abattement on premiums paid before the insured's 70th birthday [`frlib`
R14, R15]; **German law does no such thing**, which is why the *Über-Kreuz-Versicherung* exists and
why German term-life tax planning is a **contracting-structure** question rather than a
**beneficiary-designation** one. **The *Erbschaftsteuer* figures are now read in the statute** (gap
18, closed): § 16 Abs. 1's *Freibeträge* are 500 000 € spouse or *Lebenspartner*, 400 000 € children,
200 000 € grandchildren, 100 000 € the rest of class I, 20 000 € classes II and III; § 19 Abs. 1's
rates open at 7 % in class I and 30 % in class III; and § 15 Abs. 1 puts "alle übrigen Erwerber" —
an unmarried partner among them — in class III [R15]. They remain **[std]** illustrations downstream
and are never used as model parameters. And there is **no *Versicherungsteuer***: VersStG 2021 § 4
Abs. 1 Nr. 5 Buchst. a exempts a contract creating claims "im Fall des Todes", so the German premium
bears no premium tax, unlike a French *cotisation* quoted "TTC" [R16].

**Prudential, accounting and case law.** Solvency II reaches German life business **through the
VAG**, not directly [REG-R1] [REG-R2] [REG-R6]; Directive (EU) 2025/2 takes effect on 30 January
2027 and **nothing here implements a 2027 basis** [REG-R3]. **No capital, risk-margin or stress
figure appears anywhere in this product's documents** [R22]. The statutory accounts run on HGB
§§ 341–341o and the RechVersV [REG-R54]; IFRS 17 has applied to IFRS reporters since 1 January 2023
with no German carve-out [REG-R55]. Professional standards sit with the DAV's *Fachgrundsätze* and
its annual *Höchstrechnungszins* recommendation [REG-R56], and the *Rechnungsgrundlagen erster und
zweiter Ordnung* framework — the split this whole product turns on — is set out at [REG-R47]. German
term-life litigation clusters on two questions: whether the applicant's answers to the
*Gesundheitsfragen* were complete and whether the insurer complied with the § 19 Abs. 5 warning
requirement [R4]; and whether a *Selbsttötung* inside the three-year window was committed in a state
excluding free will [R1]. **Not one decision was located for this product, so none is named and none
is invented** [R23] (gap 20). The BGH's adjacent life-insurance authority — the *Stornoabzug*
*Bezifferung* requirement and the *Bewertungsreserven* judgment of 20 January 2021, IV ZR 318/19 —
is recorded in the cross-product library [REG-R36] and establishes that the court decides this area
regularly and nothing about term assurance.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-risikolebensversicherung-r1
[R10]: #delib-risikolebensversicherung-r10
[R11]: #delib-risikolebensversicherung-r11
[R12]: #delib-risikolebensversicherung-r12
[R13]: #delib-risikolebensversicherung-r13
[R14]: #delib-risikolebensversicherung-r14
[R15]: #delib-risikolebensversicherung-r15
[R16]: #delib-risikolebensversicherung-r16
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
[REG-R1]: #delib-reg-r1
[REG-R10]: #delib-reg-r10
[REG-R11]: #delib-reg-r11
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R22]: #delib-reg-r22
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R26]: #delib-reg-r26
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R29]: #delib-reg-r29
[REG-R3]: #delib-reg-r3
[REG-R30]: #delib-reg-r30
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R45]: #delib-reg-r45
[REG-R46]: #delib-reg-r46
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R56]: #delib-reg-r56
[REG-R6]: #delib-reg-r6
[REG-R8]: #delib-reg-r8
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
