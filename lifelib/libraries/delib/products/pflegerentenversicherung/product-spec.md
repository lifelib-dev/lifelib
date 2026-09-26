# Product Specification

**Status:** Draft, 2026-08-29 (research access date 2026-08-29).

**Scope note.** This is a *standardized composite specification* assembled for reference liability
cash-flow modelling of a German **Pflegerentenversicherung** — the individual, privately written,
single-life long-term-care annuity sold by a *Lebensversicherer*, which pays a monthly *Pflegerente*
for as long as the insured holds a contractual *Pflegegrad* (statutory degree of care need). It
describes **no single insurer's product**, and it must not be read as one.

**How this composite differs from its frlib counterpart.**
`frlib/products/temporaire_deces/product-spec.md` is a composite of eight retrieved carriers, seven
of whose contracts were read in full. **This one was drafted with nothing retrieved at all.** Direct
HTTP egress from the build environment was blocked by an organisation network policy, and the
session's `WebSearch` budget was already exhausted when work on this product began, so there was
neither a retrieval channel nor a search channel: the composite below was assembled from **document
classes that exist and are the right kind of document for this product**, and from the mechanics of
German insurance law and actuarial practice as the authoring model knew them, under the discipline
house rule 3 imposes for exactly that case.

**That is how it was drafted, and not where it now stands.** The policy has since been lifted and the
citations re-verified against the primary documents on 2026-08-30. Every statute cited here was read
as canonical XML from gesetze-im-internet with its amendment status (`Stand`) recorded; one carrier's
complete *Bedingungswerk* and *Produktbeschreibung* were read as PDFs, and so were the PKV
*Musterbedingungen* for both the compulsory and the top-up cover, the DAV's own derivation and
*Pflegegrad* reports, and the Destatis, vdek, GDV and Assekurata material. **Twenty-seven of this
product's thirty-six source entries now read `Retrieved: yes`, five read `no`, and four are partial**;
`sources.md` names each and says what stopped it. What has **not** changed is the shape of this file:
one contract is not eight, so the variation table below remains a market-range reconstruction rather
than a survey, and every level in it is still a standardization. What has changed is that the
re-verification corrected claims the drafted text got wrong, each marked where it occurs.
**Read the `Retrieved` line before relying on a tag:** where it says `yes` the document was opened and
the passage read; where it does not, `[R2]` beside a statement about § 15 SGB XI names the instrument
the statement should be checked against and asserts nothing more — a pointer, not a certificate.

Facts carrying a source tag — [S#] (primary product document classes: *Musterbedingungen*, AVB,
*Produktinformationsblatt*, *Basisinformationsblatt*, *Verbraucherinformation*, *Tarifblatt*) and
[R#] (product-specific regulatory and actuarial references), both numbered per
`_research/pflegerentenversicherung.md` and resolved in `sources.md` (numbering frozen, never
renumbered), and [REG-R#] (the cross-product reference library, whose own R-numbering is distinct and
also frozen) — name the instrument the claim belongs to. Values marked **[std]** are standardizations
introduced for the reference implementation; each carries a numbered footnote giving the rationale
and, where the research file recorded one, the observed or argued range. Claims no source could
corroborate are flagged [unverified], and on this product that is most of the specific numbers.

**Out of scope, and said so where it matters.** The *soziale Pflegeversicherung* of SGB XI [R1] and
the *private Pflegepflichtversicherung* of § 23 SGB XI [R7] are the compulsory first layer and are
described, not modelled. *Pflegetagegeldversicherung* and *Pflegekostenversicherung* are written as
*private Krankenversicherung* and are the contrast documents of this file, never its subject [S2].
*Pflege-Bahr*, the subsidised cover of § 127 SGB XI, is confined by statute to a tariff calculated
under § 146 Abs. 1 Nrn. 1 and 2 VAG — health business, with an *Alterungsrückstellung* — and may
carry no benefit beyond the graded *Geldleistung* [R8] [R12]: **a *Pflegerentenversicherung* cannot
be a *geförderter Tarif***, and the *Zulage* is not modelled. (The statute nowhere uses the word
*Pflegetagegeld*, as this note previously said it did.) *Betriebliche Altersversorgung*, *Gruppenversicherung*, *Sterbegeldversicherung* and
institutional risk transfer are outside the delib library entirely. The neighbouring biometric
product is `products/berufsunfaehigkeit/` (`BU_DE_S`), which shares this product's chassis, its
waiver of premium and its multi-state modelling problem, and differs in trigger, in duration and in
the age at which the risk bites.

---

## Product overview and market role

### The three layers of German long-term-care funding

German long-term care is funded in **three layers**, and a *Pflegerentenversicherung* is the third.
The first is **compulsory statutory cover** — the *soziale Pflegeversicherung* (SPV) of SGB XI [R1],
or the *private Pflegepflichtversicherung* (PPV) of § 23 SGB XI for the privately health-insured
[R7]; membership follows health insurance, so the layer is universal, and it is a
***Teilleistungssystem*** by design, paying **defined amounts per *Pflegegrad*** rather than the
cost of care, with the residue falling on the insured person [R1]. That constitutive choice, made in
1994 and never reversed, is why the third layer exists as a market at all. The second layer is **the
insured person's own resources**; the third is **voluntary private top-up** or, failing that,
means-tested *Hilfe zur Pflege* under §§ 61–66 SGB XII [R24]. The private product is sized against
the gap the first layer leaves, and its trigger is **defined by reference to the first layer** [S1]
[S4] — so the trigger is exogenous to the insurer, and the benefit is a *Summenversicherung* payable
irrespective of what care actually costs.

### The statutory first layer, quantified

All amounts per calendar month, read from the consolidated SGB XI on 2026-08-30 (Stand: zuletzt
geändert durch Art. 2c G v. 24.7.2026). They are the amounts § 30 SGB XI uprated by 4,5 % on 1
January 2025 and they were **still in force in 2026**: § 30 Abs. 1 schedules the next rise for **1
January 2028**, so nothing changed on 1 January 2026 and research gap 8 is closed.

| *Pflegegrad* | *Pflegegeld* (cash, informal care) | *Pflegesachleistung* (benefit in kind) | SPV contribution, *vollstationär* |
|---|---|---|---|
| 1 | none | none | 131.00 EUR (flat, not graded) |
| 2 | 347.00 EUR | 796.00 EUR | 805.00 EUR |
| 3 | 599.00 EUR | 1,497.00 EUR | 1,319.00 EUR |
| 4 | 800.00 EUR | 1,859.00 EUR | 1,855.00 EUR |
| 5 | 990.00 EUR | 2,299.00 EUR | 2,096.00 EUR |

Basis: home care § 36 Abs. 3 and § 37 Abs. 1 [R3]; residential care § 43 Abs. 2 and Abs. 3 [R4].
The grade-1 figure was previously printed as 125,00 EUR; § 43 Abs. 3 reads *"einen Zuschuss in Höhe
von 131 Euro monatlich"*.

Three readings drive the private product's design. ***Pflegegrad* 1 is, for cash purposes, uninsured
by the state** — §§ 36 and 37 both open *"Pflegebedürftige der Pflegegrade 2 bis 5"*, leaving 131 €
towards a *Pflegeheim* and, for care **at home**, an earmarked *Entlastungsbetrag* of *"bis zu 131
Euro monatlich"* under § 45b Abs. 1, and nothing else [R3] [R4] [R5] — which is why most private
*Leistungsstaffeln*, and delib's, also pay nothing at grade 1. **The *Pflegegeld* runs between 40 %
and 44 % of the corresponding *Sachleistung*** — 43,6 / 40,0 / 43,0 / 43,1 % at grades 2 to 5 [R3];
the round "about 44 %" this document used to print is right at three grades of four and wrong at
grade 3. That ratio is why roughly five in six *Pflegebedürftige* are cared for at home — **85,9 %
at end-2023, against 14,1 % in *vollstationäre* care** [R18]. And **the residential contribution at
grade 5 (2 096 €) is *lower* than the home *Sachleistung* at grade 5 (2 299 €)** [R3] [R4]: the
facility sets the price and the residue falls on the resident. That asymmetry **is** the
*Versorgungslücke*.

### The *Versorgungslücke* — the number the product is sold against

A resident of a *Pflegeheim* pays, in the vdek's own presentation, **three** components [R4] [R20]:
the ***einrichtungseinheitlicher Eigenanteil*** (EEE) for the care-related cost the SPV contribution
does not meet — **identical for *Pflegegrade* 2 to 5 within one facility** since 2017 [R9], and
**inclusive of the *Ausbildungskosten***, which this document previously listed as a fourth head;
***Unterkunft und Verpflegung***; and ***Investitionskosten***, which the vdek notes are *"für alle
Pflegeheimbewohnenden in einer Einrichtung - unabhängig von der Aufenthaltsdauer - gleich hoch"*.
Only the EEE is equalised across grades and only the EEE is reduced by the § 43c *Leistungszuschläge*
— **15 % / 30 % / 50 % / 75 %** for up to twelve months, more than twelve, more than twenty-four and
more than thirty-six months of benefit [R4], confirmed word for word in § 43c and restated in the
vdek release. The other two are neither capped nor subsidised.

| Line | Amount | Basis |
|---|---|---|
| Average total resident payment, *Pflegeheim*, first year of stay, **1 January 2026** | **3,245.00 EUR/month**, up 261 EUR (9 %) on the year | [R20] |
| of which *einrichtungseinheitlicher Eigenanteil* incl. *Ausbildungskosten* / *Unterkunft und Verpflegung* / *Investitionskosten* | 1,685.00 / 1,046.00 / 514.00 EUR/month | [R20] |
| Comparatives: 1 July 2025 / 1 January 2025 | about 3,108.00 / 2,871.00 EUR/month | [R20] |
| Less: net *gesetzliche Rente* of a median new retiree | of the order of 1,200.00 to 1,600.00 EUR/month | [unverified] |
| **Residual funded from savings, family or *Hilfe zur Pflege*** | **of the order of 1,650.00 to 2,050.00 EUR/month** | **[std]** (A) |

(A) The residual is arithmetic on the two lines above, not an observation; the pension line is still
unsourced. **The *Eigenanteil* figures are no longer the least reliable numbers in the research and
are now among the best sourced** — they are read from the vdek's own evaluation as at 1 January 2026
(gap 15 closed). They are why the market sells *Pflegerenten* of 1 000 € to 1 500 € a month
[unverified], and why delib's `[std]` *vereinbarte Pflegerente* is **1 000,00 € per month**. On the
retrieved 2026 level that annuity covers a little under a third of the first-year gap, which is a
smaller share than the figure implied when this document was written against an assumed 3 000 €;
the *vereinbarte Rente* is a scaling constant and is left where it is, but the reader should not
mistake it for a full solution to the gap.

Two features of the gap matter for the model. **It widens over time**, because the statutory amounts
are uprated episodically — § 30 SGB XI, +4,5 % on 1 January 2025 and nothing again until 1 January
2028 [R1] [R10] — while the *Eigenanteil* rose **nine per cent in the year to 1 January 2026** alone,
the vdek naming *"gestiegene Pflegepersonalkosten"* as the driver [R20]. **A three-year statutory
step against a nine-per-cent annual drift** is the case for the *Leistungsdynamik* option. And **it
is largest in the first year of a stay**, because the § 43c *Zuschläge* rise with length of stay from
15 % to 75 % [R4], so a constant annuity progressively over-covers it; no German wording is known to offer a *decreasing*
care annuity, and delib does not model one.

### The three private forms, and why the *Pflegerente* is one of them

| | *Pflegetagegeldversicherung* | *Pflegekostenversicherung* | ***Pflegerentenversicherung*** |
|---|---|---|---|
| Legal branch | private Krankenversicherung | private Krankenversicherung | ***Lebensversicherung*** |
| Benefit form | agreed cash per *Pflegegrad*, no proof of spend | reimbursement of a share of residual actual cost | agreed **monthly annuity** per *Pflegegrad*, no proof of spend |
| Legal character | *Summenversicherung* | indemnity | *Summenversicherung* |
| Premium re-rating | **possible** under § 203 VVG | possible | **not possible** save on the narrow § 163 VVG route |
| Ageing provision | *Alterungsrückstellung* where written *nach Art der Lebensversicherung*; **none** otherwise | as *Pflegetagegeld* | ***Deckungsrückstellung*** always |
| Surrender value | none in substance | none | **yes**, § 169 VVG, subject to the open question below |
| Waiver of premium in claim | usual | usual | **usual, and contractual** |
| Death benefit | rare | none | **common option** |
| *Pflege-Bahr* eligible | **yes — the only eligible form** | no | **no** |
| Market share / average premium | **dominant** / lowest | negligible / — | small / **highest** |

The branch, benefit-form, re-rating and *Pflege-Bahr* rows follow from [R11], [R14] and [R8] and are
structural. **The market-share and average-premium row is now sourced.** By insured persons at
end-2024, *Pflegetagegeld* is dominant at 3 021 300 against 890 091 subsidised *Pflege-Bahr* and
366 100 *Pflegekosten* [R21] [S14]; the GDV counts 242 000 stand-alone *Pflegerenten* in force at
end-2023, plus 762 400 written as riders [R22]. On price, the consumer bodies put the *Pflegerente*
at *"etwa zwei- bis dreimal so hoch"* as the other forms for comparable cover [S11], and Finanztip
at *"von Anfang an deutlich teurer"* [S12].

**The load-bearing difference is the re-rating power.** A *Pflegetagegeld* is health business: MB/EPV
§ 8b has the insurer compare required against calculated benefits and mortality *at least annually*
per tariff and, on a deviation beyond the *"gesetzlich oder tariflich festgelegte[n] Vomhundertsatz"*,
recalculate **every** premium in the observation unit [S2] [R14], under § 203 VVG [R11]. A
*Pflegerente* is life business, and the only route is § 163 VVG [REG-R27]. **A buyer at 45 who wants
to know what the cover will cost at 80 gets an answer from a *Pflegerente* and does not get one from
a *Pflegetagegeld*** — every consumer comparison reduces to that trade, Finanztip's included: *"ist
der Beitrag bei Pflege-Rentenversicherungen für die gesamte Laufzeit festgelegt. Dafür sind diese
Tarife jedoch von Anfang an deutlich teurer."* [S12] So does the price difference: the *Pflegerente* costs more because the insurer
carries the basis risk on a fifty-year view of a table built on a superseded assessment regime [R15]
[REG-R51]. The second difference is the **ageing provision**: MB/EPV § 1 Abs. 6 carries an
*Alterungsrückstellung* where the tariff is written *nach Art der Lebensversicherung* [S2] under
§ 146 Abs. 1 Nr. 2 VAG [R12], and a tariff written without one has a premium that follows
attained-age risk upward. **The consumer bodies do not put it that starkly**: they warn that
premiums on *every* form will rise and still recommend the *Pflegetagegeld* as the sensible default
[S11] [S12], which is the opposite of the reading this document previously attributed to them. The
third is the **surrender value**, the only one of the three from which a policyholder recovers
anything on lapse — the Verbraucherzentrale puts it as a positive for the annuity form, that it
*"kann zudem durch Kündigung beendet werden, ohne dass sämtliche Einzahlungen verloren gehen, wie
dies bei einer Tagegeld- oder Pflegekostenversicherung der Fall ist"* [S11] [REG-R28] — and which
makes the contract realisable assets in a *Hilfe zur Pflege* means test [R24].

### Market size

**There is a sourced count of German *Pflegerente* contracts in force, and research gap 12 is
closed.** This document used to say there was none, on the reasoning that the PKV-Verband counts
*health*-insurance top-up contracts — which it does, and a *Pflegerente* written by a
*Lebensversicherer* is indeed absent from that series [S16] [R21] — and that the GDV life series does
not carve the product out. **The second half was wrong**: the GDV reports *Pflegerentenversicherungen*
as its own line in new business, in-force main covers and riders alike [R22] [REG-R53].

| Measure | Value | Year | Basis |
|---|---|---|---|
| *Pflegebedürftige* in Germany | 5,688,473 (about 5.0 million at end-2021, +730,000 / +15 %) | end-2023 | [R18] |
| Share cared for at home / in *vollstationäre Dauerpflege* | 85.9 % (4,888,882) / 14.1 % (799,591) | end-2023 | [R18] |
| Projected *Pflegebedürftige*, constant *Pflegequoten* | about 5.6 million (2035) rising to **6.8 million** (+37 %) | 2055 | [R19] |
| Projected on rising *Pflegequoten* | 6.3 million (2035), 7.6 million (2055) | 2055 | [R19] |
| Private LTC top-up cover, health branch | 3,021,300 *Pflegetagegeld*; 890,091 *Pflege-Bahr*; 366,100 *Pflegekosten*; about 4.5 million persons in all, 5.4 % of the population | end-2024 | [R21] [S14] |
| ***Pflegerente* contracts in force, stand-alone** | **242,000** — 0.3 % of 81.4 million life contracts; 177 Mio. EUR annual premium; 29,737 Mio. EUR *versicherte Summe* | end-2023 | [R22] |
| ***Pflegerenten-Zusatzversicherungen*** | **762,400** of 20.7 million riders; 84,218 Mio. EUR *versicherte Summe* | end-2023 | [R22] |
| *Pflegerente* new business | 5,499 policies, 0.2 % of life new business by count | 2023 | [R22] |

Two readings follow from the last three rows. **The product is three times more common as a rider
than as a stand-alone contract**, and this specification models the stand-alone form. And 177 Mio. €
across 242 000 contracts is an **average in-force premium of about 61 € a month**, which is the only
external check this document has on the argued premium band below.

**Distribution across *Pflegegrade*** [R18], read from the Destatis table for end-2023: **13.8 /
40.4 / 29.6 / 11.8 / 4.3 %** across grades 1 to 5 — this document previously printed 9 / 44 / 27 /
14 / 6 %, low at grade 1 and high at grades 4 and 5. The reading is unchanged and strengthened: the
stock is heavily weighted to the lower grades, which is why a *Leistungsstaffel*'s **middle** steps
drive its cost. Among **residents of *Pflegeheime*** the distribution is quite different — **0.5 /
16.6 / 37.3 / 31.1 / 14.3 %**, concentrated in grades 3 to 5 [R18] — which is direct support for a
grid weighted to the upper grades on a product sold against the residential gap.
**Age-specific prevalence** [R18], observed *Pflegequoten* for 2023: **1.2 % (15–60) · 3.6 (60–65) ·
5.5 (65–70) · 9.1 (70–75) · 16.4 (75–80) · 30.8 (80–85) · 53.7 (85–90) · 80.2 (90–95) · 94.5 (95+)**.
This document previously printed a curve about a third to a half lower through the seventies and
eighties. Successive five-year ratios are **1.80 · 1.88 · 1.74 · 1.49 · 1.18**, so the familiar
shorthand — *prevalence roughly doubles every five years* — is a fair approximation **between about
70 and 90 only**, and flattens sharply above 90 as the quota saturates. That curve is what the
product is built on and the reason a level premium from 45 accumulates for thirty-five years before
it starts paying. The *Pflegerente* is the **smallest of the three private forms by contract count
and the largest by average premium** [R22] [S11]; penetration is low because the risk is distant,
because *Hilfe zur Pflege* [R24] is a visible backstop, because the *Angehörigen-Entlastungsgesetz*
removed the *Elternunterhalt* motive for all but high earners from 2020 [R24] [unverified], and
because the products are hard to compare — a point Assekurata makes in its own terms, that buyers
overestimate the premium and that *"stagnieren die Bestandszuwächse"* [S14].

---

## Representative specification

The representative design is a **composite**, not a carrier's tariff. **One carrier's complete
wording has now been read** — IDEAL Lebensversicherung's *IDEAL PflegeRente Exklusiv*, conditions
AB-IPR-2022A, with its public *Produktbeschreibung* beside it [S4] [S5] — so the choices below are no
longer argued only against a reconstructed range. **One wording is not a market survey**, and where
the composite differs from it the difference is now marked *(differs from [S4])* rather than left
unstated. Every choice the corpus still cannot source is a **[std]** standardization with a numbered
rationale.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Individual, single-life, underwritten *Pflegerentenversicherung*; a **stand-alone contract**, not a rider on an endowment or a deferred annuity | [S4] |
| Legal branch | *Lebensversicherung*, written by a *Lebensversicherer*; calculated ***nach Art der Lebensversicherung*** — level premium, prospective *Deckungsrückstellung*, no ordinary re-rating | [R11] [R12]; [REG-R5] [REG-R8] |
| Benefit character | ***Summenversicherung***: an agreed monthly *Pflegerente*, paid without proof of expenditure and irrespective of the care setting | [S4]; setting-independence **[std]** (1) |
| Trigger | The statutory ***Pflegegrad*** determined under §§ 14, 15 SGB XI, normally by the *Medizinischer Dienst* for the statutorily insured or MEDICPROOF for the privately insured. The retrieved wording pins the statutory text to a stated version — *"Wir beziehen uns immer auf den Stand vom 28.03.2021"* — and offers a self-contained *Punktesystem* as an alternative route | [R2] [R6]; [S4]; [REG-R51] |
| Lives basis and cover period | Single life — no joint-life *Pflegerente* is recorded anywhere in the corpus — and **whole of life**: *Versicherungs- und Leistungsdauer lebenslang*, the annuity payable for as long as an insured *Pflegegrad* holds, the contract ending on death | [S4] [S5] |
| Entry ages / age basis | **18 to 65** at entry in the composite, with purchase clustering at **45 to 60**; age last birthday at issue, stepping at the policy anniversary. *(differs from [S4]: the retrieved tariff writes from **18 to 75**, ten years beyond the composite's envelope)* | [S5]; **[std]** (2), (3) |
| *Vereinbarte Pflegerente* | **1 000,00 € per month** at *Pflegegrad* 5; the retrieved tariff's **permitted** band is 250 € to 4 000 € a month, against a market band as *sold* of 1 000 € to 1 500 € | [S5] for the permitted band; sold band [unverified]; **[std]** (4) |
| Currency / sex | EUR; sex is carried for reporting and for the projection basis, but **pricing is unisex** for contracts concluded from 21 December 2012 | [REG-R34]; blend **[std]** (5) |
| *Pflege-Bahr* eligibility | **None**, but not for the reason this table used to give. § 127 SGB XI nowhere says *Pflegetagegeld*. Abs. 2 Nr. 1 requires *"die Kalkulation nach Art der Lebensversicherung gemäß § 146 Absatz 1 Nummer 1 und 2 des Versicherungsaufsichtsgesetzes"* — the **health**-insurance provision, whose Nr. 2 requires an *Alterungsrückstellung* — and Nr. 4 forbids the tariff any benefit beyond the graded *Geldleistung*. A life-branch *Pflegerente* forms a *Deckungsrückstellung*, not an *Alterungsrückstellung*, and carries surrender and death benefits, so it **cannot be a *geförderter Tarif*** | [R8]; [R12] |
| Anchor model cell | Female, entry age 45, *vereinbarte Pflegerente* 1 000,00 €/month, `delib_std` *Leistungsstaffel*, lifelong monthly premium struck by equivalence, no *Wartezeit*, no *Karenzzeit*, no *Dynamik*, no *Todesfallleistung*, no *Stornoabzug* | **[std]** (6) |

Footnotes to **[std]** rows:

1. **Setting-independence is modern practice.** Older wordings paid the full annuity only for
    *vollstationäre* care and a reduced one at home [unverified]; modern practice pays irrespective of
    setting, which is what makes the product a *Summenversicherung*. A setting-dependent benefit would
    need a care-setting state the corpus supplies no transition data for.
2. **Entry ages.** The one retrieved tariff writes from **18 to 75** [S5]; the composite keeps 18–65
    as its envelope, which is now known to be conservative. It takes 45 as the anchor because that is
    the lower edge of the observed *purchase* cluster, not of the permitted band — the two differ by
    thirty years on the retrieved tariff, and conflating them is the commonest error in describing
    this product.
3. No age basis is established for any *Pflegerenten* tariff; German practice uses the
    *versicherungstechnisches Alter* on carrier-specific rounding rules. The composite uses age last
    birthday at entry, the delib registry's convention, and a different rule shifts the projection by
    at most one year of age.
4. **A permitted band is now established** [S5]: the retrieved tariff writes a *vereinbarte Rente*
    of **250 € to 4 000 €** a month, with a minimum of 50 € where only grades 2 and 3 are insured, a
    minimum annual premium of 60 €, and the ceiling applied to the sum of all *Pflegerenten* the
    insurer holds on that life. **The band as *sold* is still unsourced.** 1 000,00 € comes from the
    gap arithmetic above, sits comfortably inside the permitted band, and is a **scaling constant** —
    changing it rescales the whole liability linearly. Against the 2026 *Eigenanteil* of 3 245 €
    [R20] it is a partial cover, not a full one.
5. Unisex pricing is compulsory from 21 December 2012 [REG-R34], and matters more here than on any
    other delib product: **women have materially higher LTC incidence and longer care durations**
    [unverified], so the unisex premium embeds a cross-subsidy whose size depends on the sex mix
    written — itself endogenous to the price. The composite prices on a **50 / 50** blend **[std]**
    and projects on the point's own sex.
6. Entry age 45 gives a long enough pre-claim period for the *Deckungskapital* to be the object it
    is. The anchor is **female** deliberately: the projection then runs the higher-incidence basis
    against a unisex price.
### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium form | **Level monthly *Beitrag*, guaranteed for the life of the contract**, subject only to the narrow § 163 VVG route | [R11]; [REG-R27] |
| Premium-paying period | **Lifelong** in the base case, until death or the start of a waiver. Two alternatives are sold and are carried as options: an *abgekürzte Beitragszahlungsdauer* — the retrieved tariff requires at least **five years** — and a single ***Einmalbeitrag***, which that tariff also allows to be combined with a running premium | [S5]; base choice **[std]** (7) |
| Payment frequency and the *Ratenzahlungszuschlag* | Monthly, quarterly, half-yearly or annual, in advance, all four offered by the retrieved tariff; the instalment loading is **not modelled as a separate charge** but folded into the administration-cost assumption | [S5]; **[std]** (8) |
| Premium level | **No German *Pflegerenten* rate card exists in this corpus.** The premium is struck by **equivalence** on the tariff (*erster Ordnung*) bases at the *Rechnungszins* | [R9] (absent); method [REG-R8] [REG-R47]; level **[std]** (9) |
| Argued premium band, 1 000 € *vereinbarte Rente*, `delib_std` grid, lifelong monthly premium, waiver, no death benefit, no dynamics | entry age 45: about **50,00 € to 100,00 €** per month; entry age 55: about **80,00 € to 160,00 €** per month | **[std]** (9) |
| Rating factors | Attained age at entry; *vereinbarte Rente*; the *Leistungsstaffel*; the premium-paying period; medical acceptance (*Risikozuschlag*). **Occupation is not a rating factor at all** — the sharpest single contrast with *Berufsunfähigkeit* | [S4] [unverified]; occupation [unverified] |
| *Risikozuschlag* | Carried as a model-point multiplier on the gross premium; **1.00** at standard rates. No scale was established | mechanics [S4] [unverified]; value **[std]** (10) |
| *Rechnungszins* | **1,00 %** p.a. — § 2 Abs. 1 DeckRV, *"wird der Höchstzinssatz … auf 1 Prozent festgesetzt"*, for new business written from 1 January 2025; Abs. 2 keeps the rate used at conclusion for the whole term | [R13]; [REG-R14] [REG-R15] |
| Premium cessation and revival | On death, on the start of an insured annuity (*Beitragsbefreiung*), and at the end of an agreed premium-paying period; the obligation **revives** on a *Herabstufung* out of the annuity-paying grades. *(differs from [S4]: the retrieved wording makes the cessation **permanent** after twelve months' continuous annuity at grade 4 or 5, whatever happens to the grade afterwards)* | [S4]; waiver **[std]** (11) |
| Re-rating power | § 163 VVG only: a non-temporary, unforeseeable change in a calculation basis, a new premium that is appropriate and necessary, and an independent *Treuhänder*'s confirmation — and **excluded** where the original calculation was insufficient and a diligent actuary should have seen it | [REG-R27]; [R11] |

7. Three premium-paying periods are sold, and the retrieved tariff sells all three plus a
    combination of the last two [S5]: lifelong; abgekürzt (minimum five years there); and a single
    *Einmalbeitrag*. The composite takes **lifelong**, the form that shows the *Deckungskapital*
    building and running off across the whole risk period; both alternatives are model-point options,
    and the *Einmalbeitrag* is explicitly **not** the base model.
8. German tariffs load monthly, quarterly and half-yearly payment relative to annual [unverified];
    **no level was established** (gap 2), and shipping a loading nobody sourced would put a fabricated
    price difference into the model. The frequency therefore changes the *timing* of premium income
    and nothing else — a listed pitfall, because paying annually in advance is *earlier*, so the
    equivalence premium per month is slightly *lower*, the opposite sign to a real
    *Ratenzahlungszuschlag*.
9. **No German *Pflegerenten* rate card was found, and none appears to be published** (gap 3) — the
    sharpest difference from `frlib/products/temporaire_deces`, which had a published rate card to
    reproduce. The band is derived arithmetic, set out in the research file § 23: a time-weighted
    average benefit of about 52 % of the *vereinbarte Rente* over a spell; about 25 000 € of expected
    nominal benefit per claim; a lifetime probability of reaching an insured grade of about 45 %; a
    mean age at first insured grade of about 82; discounting at 1,00 %; and a gross-to-net ratio
    between **2 and 3**. **It is not a market observation and must never be cited as one.** Three
    external readings, retrieved in this pass, are consistent with it and none of them is a citation
    for it: the GDV's in-force average of about **61 € a month** across 242 000 contracts [R22];
    Assekurata's *Pflegetagegeld* premiums of **85 / 117 / 130 / 78 €** at entry age 45 for a 2 000 €
    residential benefit, which halve to roughly 39–65 € on delib's 1 000 € scale [S14]; and the
    consumer bodies' multiplier of *"etwa zwei- bis dreimal so hoch"* for the annuity form [S11].
10. Underwriting outcomes are documented in kind [S4] [unverified] but **no *Risikozuschlag* scale is
    public**, so the factor is a pure model-point input, multiplying the **premium** and never the
    benefit.
11. Waiver detail that varies and was not established [unverified]: from which grade the waiver runs,
    whether it is full or proportionate, and whether the premium revives on a *Herabstufung*. The
    composite takes **full waiver, from the first month in which any annuity is payable, revived on
    exit from the paying grades** — the market-standard design, and the one that keeps waiver and
    benefit on a single trigger, which is what lets the model publish one `check_waiver()` identity.
### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Benefit | A monthly ***Pflegerente***, paid in advance, as a percentage of the *vereinbarte Pflegerente* set by the insured's current *Pflegegrad* | [S4] |
| ***Leistungsstaffel*** | **0 / 30 / 50 / 75 / 100 %** across *Pflegegrade* 1 to 5 | **[std]** (12) |
| Alternative *Leistungsstaffel* carried | **10 / 20 / 30 / 40 / 100 %** — the *Pflege-Bahr* grid as the market writes it. **It is not fixed by statute**: § 127 Abs. 2 Nr. 4 SGB XI requires only a *Geldleistung* at every *Pflegegrad*, at least **600 €** at grade 5, capped at the SGB XI benefit level, with the percentage schedule left to the PKV-Verband's *brancheneinheitliche Vertragsmuster* under Abs. 2 Satz 2 — a document this library has not retrieved | [R8]; the grid itself **[std]** |
| Care setting, payment start and duration | Setting is **irrelevant to the benefit** — the same annuity is payable at home and in a *Pflegeheim*; payment starts from the month the assessment fixes as the onset of the insured *Pflegebedürftigkeit*, subject to any *Karenzzeit*, and continues to the end of the month in which the grade falls away or the insured dies. The retrieved wording matches on all three points and adds arrears of up to three years | **[std]** (1); [S4] (13) |
| ***Wartezeit*** (from inception) / ***Karenzzeit*** (from onset) | **None / none** in the base case, and the retrieved underwritten tariff also has *Wartezeit* **keine** [S5]. Observed elsewhere: up to **3 years** where present, and § 127 Abs. 2 Nr. 6 SGB XI caps a *Pflege-Bahr Wartezeit* at *"höchstens fünf Jahre"*; *Karenzzeit* commonly none, **3** or **6** months where present | [S5]; [R8] for the five years; other ranges [unverified]; base **[std]** (14) |
| ***Beitragsbefreiung im Leistungsfall*** | **Full**, from the first month in which any annuity is payable; the premium revives on exit from the paying grades | [S4]; detail **[std]** (11) |
| ***Nachprüfung*** | The insurer may require periodic evidence that the *Pflegegrad* persists; the retrieved wording takes that evidence to be the *Gutachten* of the compulsory-cover carrier, i.e. the statutory determination itself | [S4] (15) |
| ***Herabstufung*** / ***Höherstufung*** / ***Reaktivierung*** | The annuity moves to the step of the new grade; if the grade falls below the insured threshold, or the insured recovers to the active state, the annuity **stops** and the premium revives. *(differs from [S4]: after **24 months** of continuous annuity at grade 4 or 5 the retrieved wording pays for life *"auch wenn die Versicherte Person in einen geringeren Pflegegrad eingestuft wird oder die Pflegebedürftigkeit komplett wegfällt"* — a lock-in the composite does not carry, and the "guarantee" variant gap 17 asks about)* | [S4] |
| ***Todesfallleistung*** | **None** in the base case; carried as a switchable *Beitragsrückgewähr* option, which the retrieved tariff writes at **50–80 %** of premiums paid on a running premium and 50–100 % on a single premium | [S4] [S5]; base **[std]** (16) |
| ***Leistungsdynamik*** in payment / ***Beitragsdynamik*** before claim | **Off** in the base case / **not modelled**. The retrieved tariff writes a *Rentendynamik* of **1–5 %** a year, and only for the **first ten years** of the annuity; before the claim, 10 % every three years or 1–5 % a year, *"Dynamik endet nach dem 3. Widerspruch in Folge"* | [S5]; **[std]** (17) |
| Exclusions and territorial scope | Care caused by war, by the insured's intentional act and, variably, by addiction, plus any condition excluded at underwriting. **The territorial question is now answered for one carrier and the answer is sharper than "worldwide"**: cover is worldwide, but a claim arises only if the insured travels *"in die EU, in die Schweiz oder nach Norwegen"* for the assessment, the same applies to every *Nachprüfung*, and the contract **ends** if the insured cannot — a term with real bite for a population that is by definition immobile | [S4] |

12. **The *Leistungsstaffel* is the most important parameter in the product and the one the corpus can
    least support** (gap 6). The observed range, attributed to no carrier: grade 1 **0–10 %**; 2
    **10–30 %**; 3 **30–50 %**; 4 **60–75 %**; 5 **100 %**. **A third shape is now known to be
    written and is not a percentage grid at all**: the retrieved tariff sells three product lines
    that pay the **full** annuity from grade 2, from grade 3, or from grade 4 — a *threshold* design
    [S4] [S5], and the same *Stufenmodell* structure the DAV's own bases use, *"mindestens Pflegegrad
    g ist erreicht"* [R15]. Of the two percentage shapes that recur — the *Pflege-Bahr*
    10 / 20 / 30 / 40 / 100 [R8], and a flatter, higher shape near 0 / 30 / 50 / 75 / 100,
    which is what a *Pflegerente* aimed at the residential gap uses because grades 3 to 5 are where
    residential care happens — the composite takes the second: **grade 1 at 0 %** because grade 1 is
    not a funding event in the statutory scheme either (§§ 36 and 37 both start at grade 2), so
    insuring it adds incidence-heavy, low-severity claims that dominate the claim *count* and not the
    claim *cost*; **grade 2 at 30 %**, the top of its range, because that is where care at home begins
    in earnest; **3 at 50 %** and **4 at 75 %**, mid-range; **5 at 100 %**, the scaling constant. The
    residential grade distribution — 0.5 / 16.6 / 37.3 / 31.1 / 14.3 % [R18] — supports weighting the
    upper steps on a product sold against the residential gap.
13. The statutory determination is often backdated, so a wording keyed to the *effective date* pays
    earlier than one keyed to the *decision date*; the composite keys off the effective date, **and
    the retrieved wording does the same** — entitlement runs *"ab dem Monat, der durch ärztliche
    Feststellung bzw. den für die Pflegekasse zuständigen Medizinischen Dienst als Zeitpunkt des
    Eintritts der versicherten Pflegebedürftigkeit festgestellt wird"*, with arrears payable up to
    three years back [S4].
14. **The pairing between underwriting and waiting periods is near deterministic**: no underwriting
    implies a long *Wartezeit* (the *Pflege-Bahr* design [R8]); underwriting implies none. Both are
    **zero** in the base run and both are exercised by model points, because a *Karenzzeit* on a
    population with heavily elevated mortality removes disproportionately more claims than the same
    period would on a healthy population.
15. The insurer does not define the insured event — the state does, and re-defined it in 2017 [R9] —
    and does not assess the claim [R6], so claims administration is materially cheaper than on a
    *Berufsunfähigkeitsrente* [REG-R29]; the BGH described the same trade in *IV ZR 126/23*, the
    insurer *"macht sich den Sachverstand des Medizinischen Dienstes … zunutze und erspart die mit
    einer erneuten Begutachtung verbundenen Aufwendungen"* [REG-R36]. **The price of that cheapness
    is definition risk — but this document overstated it.** A statutory widening does *not*
    automatically flow through: every wording retrieved for this product hedges that channel, MB/PPV
    and MB/EPV by copying the §§ 14–15 test into the conditions [S1] [S2] and AB-IPR-2022A by pinning
    it to *"den Stand vom 28.03.2021"* [S4]. What remains unhedged is **drift in assessment practice**
    under a fixed text — a loosening of the *Begutachtungs-Richtlinien* raises incidence with no
    contractual change and no re-rating remedy — and the reputational and competitive pressure that
    builds when a pinned private definition parts company with the social insurance beside it.
16. A *Todesfallleistung* — most often a ***Beitragsrückgewähr***, written by the retrieved tariff at
    50–80 % of premiums paid, or 50–100 % on a single premium [S4] [S5] — converts a pure
    biometric cover into a savings-bearing contract: it roughly doubles or more the premium for the
    same annuity **[std]**, because the death benefit is close to certain to be paid whereas the
    annuity is not, and it very likely brings the contract inside the PRIIPs perimeter [REG-R32]. The
    base run omits it so that the LTC mechanics are what the model demonstrates.
17. **The *Leistungsdynamik* is the economically important dynamic**, and its cost is
    counter-intuitively small: the annuity is paid to a population with heavily elevated mortality, so
    a 2 % escalation on an annuity of about four years' expected duration costs of the order of **4 %**
    of its value, not the 15 % or 20 % it would cost on a healthy-life pension. The **Beitragsdynamik**
    is **not modelled at all**.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Health evidence and question catalogue | Full ***Gesundheitsprüfung***, with a catalogue materially **shorter than a *Berufsunfähigkeit* application's**: the risk is driven by conditions that predict dependency in old age — cardiovascular and cerebrovascular disease, diabetes, neurological and psychiatric conditions, early cognitive impairment, musculoskeletal disease | [S4] [unverified] |
| Occupation | **Not a rating factor.** The sharpest single contrast with *Berufsunfähigkeit* | [unverified] |
| Outcomes | Accept at standard rates; accept with a *Risikozuschlag*; accept with a *Leistungsausschluss* for a named condition; defer; decline | [S4] [unverified] |
| Absolute bar and disclosure duty | Existing *Pflegebedürftigkeit* at application is an absolute bar; the *vorvertragliche Anzeigepflicht* of § 19 VVG applies, and § 21 Abs. 3 extinguishes the insurer's remedies *"nach Ablauf von fünf Jahren nach Vertragsschluss"*, or ten *"[h]at der Versicherungsnehmer die Anzeigepflicht vorsätzlich oder arglistig verletzt"* — with the bar not running against claims that arose inside the period | [S4]; [R11]; [REG-R30] |
| Effect of selection on the liability | **Essentially irrelevant to the cost of the benefit.** Claims arrive thirty to forty years after underwriting, and the § 19 time bar confines the *Gesundheitsprüfung*'s effect to the first decade | [R11]; **[std]** (18) |
| Sex / smoker status | Sex may not be a rating factor for contracts concluded from 21 December 2012; smoker status was not established as one for this product | [REG-R34]; [unverified] |

18. This is the **opposite** of *Berufsunfähigkeit*, where selection is a first-order pricing effect
    because claims arrive within the working life. Here it matters only to the early-duration reserve,
    so the model ships **no selection factor at all**.

### Charges

**No charge level of any kind was established for any German *Pflegerenten* tariff** — not one
*Abschlusskostensatz*, not one administration rate, not one *Ratenzahlungszuschlag*, not one
*Effektivkosten* value (gap 2), and no *Produktinformationsblatt* [S5], *Verbraucherinformation*
[S7] or *Tarifblatt* [S9] was located. **Every charge in delib is therefore `[std]`**; only the
statutory *ceiling* is known, and only [unverified].

| Parameter | Representative value | Basis |
|---|---|---|
| ***Abschluss- und Vertriebskosten*** and the *Höchstzillmersatz* | **25 ‰ of the *Beitragssumme***, charged at inception, i.e. exactly at the § 4 DeckRV ceiling: *"Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten"*, cut from 40 ‰ by the LVRG with effect from 1 January 2015. The retrieved wording applies the same rule in the same words — the *Verrechnungsverfahren* of § 4 DeckRV, *"beschränkt [auf] 2,5 % der von Ihnen während der Laufzeit des Vertrags zu zahlenden Beiträge"* | **[std]** (19); [R13]; [S4]; [REG-R16] [REG-R20] |
| *Beitragssumme* for the *Zillmerung* base | Level premium × 12 × (min(premium-end age, **85**) − entry age) | **[std]** (20) |
| ***Verwaltungskosten*** | **3,0 %** of each premium collected, plus **2,00 €** per policy in force per month at inception prices | **[std]** (19) |
| Claims administration / expense inflation | **1,50 €** per annuity payment / **1,5 %** a year | **[std]** (19) |
| Disclosure obligation | § 2 Abs. 1 Nr. 1 VVG-InfoV requires the *einkalkulierte Abschlusskosten* as one total and the *übrige* and *Verwaltungskosten* as shares of the annual premium, and Abs. 2 requires them **in Euro**. The *Effektivkosten* of Nr. 9 are owed only *"bei Lebensversicherungsverträgen, die Versicherungsschutz für ein Risiko bieten, bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist"* — the same test § 169 Abs. 1 VVG uses — so a pure-risk *Pflegerente* carries the euro disclosure and no *Effektivkosten* figure | [R11] [S7]; [REG-R31] |
| Commission | Not disclosed anywhere in the corpus; folded into the acquisition charge | **[std]** (19) |

19. **No observed range exists for any of these.** The levels are round-number placeholders, sized so
    that the acquisition charge on the anchor is of the same order as the first two years' premium.
    Claims administration is set **low**, the one charge with a real argument behind it: the trigger
    is determined by a third party [R6], so the insurer's own claims cost is materially smaller than
    on a *Berufsunfähigkeitsrente* [REG-R29].
20. The *Höchstzillmersatz* is a per-mille of the ***Beitragssumme***, the sum of all premiums payable
    under the contract [REG-R16] — **not** a percentage of the annual premium, and getting that base
    wrong is a listed pitfall. On a lifelong-premium contract the *Beitragssumme* is not finite without
    a convention, so the composite caps the premium term at attained age **85** **[std]**, which makes
    the 25 ‰ ceiling bind visibly rather than notionally.
### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| ***Rückkaufswert*** | Payable on surrender. The base measure is the ***Deckungskapital*** computed on the premium calculation bases, with acquisition costs spread over at least the first **five** contract years as a **floor on the value**, not a cap on the charge | [R11]; [REG-R28] |
| Shipped surrender basis | A table of guaranteed values expressed as a **fraction of premiums paid to date**, by completed policy year — the form in which a German contract states them — **near zero for the first several years** and well below premiums paid for a long time | **[std]** (21) |
| ***Stornoabzug*** | **0 %** in the base run. § 169 Abs. 5 VVG admits a deduction only *"wenn er vereinbart, beziffert und angemessen ist"*, and makes a deduction for unamortised acquisition costs *"unwirksam"*. *(differs from [S4], and materially: the retrieved wording agrees a *Stornoabzug* of **25 %** of the § 169 value, rising to **50 %** after a partial withdrawal, and none on a paid-up conversion)* | [R11] [REG-R28]; level **[std]** (22) |
| ***Beitragsfreistellung*** | The policyholder may at any time demand conversion to a paid-up *Pflegerente* at a reduced *vereinbarte Rente*, computed from the same § 169 value the surrender path uses | [R11]; [REG-R28]; scope **[std]** (23) |
| The open statutory question | § 169 Abs. 1 VVG owes a *Rückkaufswert* on *"eine Versicherung, die Versicherungsschutz für ein Risiko bietet, bei dem der Eintritt der Verpflichtung des Versicherers gewiss ist"* — a **positive scope test**, not an exception for death-only covers as this document previously described it. On its face a pure-risk *Pflegerente* does not satisfy it, and § 176 extends §§ 150–170 only to the *Berufsunfähigkeitsversicherung*. **The statutory question is still open**; the one wording retrieved answers it in practice by granting a guaranteed § 169 value on a product it calls *"eine reine Risikoversicherung ohne Sparprozess"* [S4] | [R11]; [S4]; research gap 9 |
| Lapse and the non-payment path | Voluntary surrender terminates the contract against the *Rückkaufswert* less any *Stornoabzug*; German lapse is in fact a **three-way decrement** — surrender, *Beitragsfreistellung*, and premium-default conversion under § 38 VVG, the last two keeping the policy in force with a reduced benefit and a continuing expense loading | [REG-R28] [REG-R30]; scope **[std]** (23) |
| *Widerruf* / expiry | 30 days — § 152 Abs. 1 VVG, *"[a]bweichend von § 8 Absatz 1 Satz 1 beträgt die Widerrufsfrist 30 Tage"* — with the right lapsing at the latest 24 months and 30 days after conclusion / **none**: the contract runs for life, with no maturity and no survival benefit | [R11]; [REG-R23]; [S4] |

21. **No *Rückkaufswert* table for any German *Pflegerenten* tariff was established.** The composite
    ships guaranteed values as **data** rather than computing a reserve: § 165 VVG requires the
    paid-up benefit to be **stated in the contract for each insurance year** [REG-R28], and computing
    a reserve would break the library's rule that its models publish gross undiscounted cash flows.
    The shipped shape encodes the 25 ‰ *Zillmerung* allowance [REG-R16] and the § 169 Abs. 3
    five-year spread **floor** [REG-R28].
22. **This footnote was wrong by a factor of five, and it is the sharpest single correction in this
    document.** It said the German life-market *Stornoabzug* range runs from nil to about **5 %** of
    the *Deckungskapital* and that none was established for this product. The one *Pflegerenten*
    wording since retrieved agrees **25 %**, rising to **50 %** for a surrender after a partial
    withdrawal, and justifies it as compensating *"die Veränderung der Risikolage des verbleibenden
    Versichertenbestandes"* and the collectively provided risk capital [S4] — a rationale that is
    specific to a biometric-risk book and has no counterpart on a savings product, which is very
    likely why the deduction is so much larger here than the life-market shorthand suggests. **The
    base run is still 0 % and the model point still switches it on at 5 %**; both are `[std]` and
    neither is now a market figure. Changing them is a model decision and was not taken in this pass.
23. **The model implements the surrender path only.** *Beitragsfreistellung* and the § 38
    premium-default conversion both keep the policy in force at a reduced *vereinbarte Rente*, anchored
    to the same § 169 value [REG-R28], and carrying them needs a paid-up ledger for which the corpus
    supplies no take-up split. The model records the bias: the omitted paths would move policies into a
    reduced-benefit ledger that still pays claims, so **the model understates late-duration claims and
    overstates surrender outgo**.

---

## Contractual mechanics

### The benefit trigger — the statutory *Pflegegrad*

**The rule.** The annuity is payable when, and for as long as, the insured holds a *Pflegegrad* at
or above the lowest grade the *Leistungsstaffel* pays on, that grade being the one determined under
§§ 14, 15 SGB XI by the *Medizinischer Dienst* for the statutorily insured or by MEDICPROOF for the
privately insured [R2] [R6], with a fallback assessment by a physician the insurer appoints where
the insured is covered by neither. **The retrieved wording's fallback is not a physician the insurer
appoints** but a self-contained *Punktesystem* offered as an alternative to the SGB XI route, and it
pins the statutory route to the §§ 14–15 text *"[Stand] 28.03.2021"* [S4]. The Verbraucherzentrale
records both patterns in the market — insurers *"richten sich häufig nach der Einstufung der sozialen
Pflegeversicherung. Andere definieren den Leistungsfall nach einer eigenen Systematik"* [S11].

**What it does.** § 14 Abs. 1 defines *Pflegebedürftigkeit* as *"gesundheitlich bedingte
Beeinträchtigungen der Selbständigkeit oder der Fähigkeiten"* which must persist *"auf Dauer,
voraussichtlich für mindestens sechs Monate"*; § 15 Abs. 2 scores six *Module* to *gewichtete
Punkte* on a 0-to-100 scale — *Mobilität* 10 %, cognitive functioning and behaviour **sharing** 15 %
with the higher of the two entering under Abs. 3, *Selbstversorgung* **40 %**, illness- and
therapy-related demands 20 %, daily life and social contact 15 % — with thresholds at
**12,5 / 27 / 47,5 / 70 / 90** points (§ 15 Abs. 3), all read from the statute. A reader from a US or
UK product will recognise an ADL trigger inside the scoring, but the instrument reaches grade 2 on
moderate impairments no two-ADL-failure trigger would catch and scores dementia with no physical
impairment at all. Three consequences reach the model: the insurer **does not define the insured
event**; the insurer **does not assess the claim**, which makes claims administration cheap and
disputes rare; and a *Pflegegrad* is a **step function of a continuous state, re-assessed
episodically** [R6] — exactly a discrete-state, discrete-time Markov chain. **On the first of those,
this document used to add that the insurer therefore carries definition risk "no wording can hedge".
That is not right**: the wordings hedge the statutory-change channel by writing the definition into
the conditions or pinning it to a version date [S1] [S2] [S4], and what is left unhedged is drift in
assessment practice under a fixed text.

**The 2017 break is still the largest basis risk in the product, but it has been worked.** PSG II
(*vom 21. Dezember 2015, BGBl. I S. 2424*) replaced the three *Pflegestufen* with the five
*Pflegegrade* and the time-based assessment with the NBA from 1 January 2017 [R9], deliberately
widening the definition — the BGH puts it as *"deutlich erweitert"*, the § 14 Abs. 2 Nrn. 2 and 3
criteria now scoring what used to count only as *erheblich eingeschränkte Alltagskompetenz*
[REG-R36]. The Senat also holds that **no inference runs from *Pflegegrad* 2 back to *Pflegestufe*
I**, the § 140 *Überleitung* being no help because it moves people into grade 2 with no prior
*Pflegestufe* at all. **What this document did not know is that the actuarial profession answered
the break directly**: the DAV publishes a companion *Ergebnisbericht* re-deriving the DAV 2008 P
*Ausscheidewahrscheinlichkeiten* **for the *Pflegegrade***, and it prints first-order bases for them
[R15]. Two things about those bases matter here. They are a ***Stufenmodell*** — *"mindestens
Pflegegrad g ist erreicht"* — not a five-state per-grade chain. And the DAV is candid that *"[z]u
Invalidisierungswahrscheinlichkeiten oder gar Invalidensterblichkeiten, für diese fünf Pflegegrade,
fehlt naturgemäß jegliche statistische Information"*: the bases are transitions from *Pflegestufen*
experience, not observations. delib's transition rates remain an explicitly labelled `[std]` proxy
shaped on *Pflegegrad* prevalence, and are **not** a reproduction of DAV 2008 P.

### The *Leistungsstaffel*

**The rule.** The contract fixes one number, the *vereinbarte Pflegerente* — the monthly annuity at
the top *Pflegegrad* — and a schedule of percentages of it by grade. Everything else in the benefit
design is a modifier on that schedule.

**What it does.** Time spent at each grade is very unequal — a person entering at grade 2 and
deteriorating spends most of the spell at grades 2 and 3 and only the final months at grade 5
[unverified] — so **the time-weighted average benefit percentage over a spell is far below 100 %**,
about 52 % on the profile the research file works through. Two tariffs with the same 100 % top step
and different middle steps therefore differ in expected cost by more than the headline suggests, and
so does any model that applies an average benefit percentage to an average survival curve. The
middle steps carry the cost because the stock is weighted to the lower grades — 13,8 / 40,4 / 29,6 /
11,8 / 4,3 % across grades 1 to 5 at end-2023 [R18]. **What no source supplies is the time spent at
each grade**: Assekurata says in terms that *"keine Informationen darüber [existieren], wie lange die
Personen in den einzelnen Pflegegraden verweilen"*, the *Pflegegrade* dating only from 2017, so the
52 % figure above stays an argued profile [S14]. What is sourced is the **overall** spell: about five
years where care begins after 60 — 4,0 for men, 5,7 for women — against about 25 months' mean stay in
a *Pflegeheim* [S14].

### *Wartezeit* and *Karenzzeit*

**The rules, and they are two different devices routinely confused in consumer material.** A
***Wartezeit*** runs from **inception of the contract**: care beginning inside it is not covered at
all, or only where it follows an accident. A ***Karenzzeit*** runs from **the onset of
*Pflegebedürftigkeit***: the claim is admitted but the annuity does not start until the deferred
period has run, and some wordings then pay retroactively to onset and some do not. The retrieved
wording has no *Wartezeit* and pays from the assessed month of onset, with arrears up to three years
[S4] [S5].

**What they do.** The *Gesundheitsprüfung* does the screening a *Wartezeit* does in the subsidised
product, which is why *Pflege-Bahr* — § 127 Abs. 2 Nr. 3 SGB XI requires the tariff to waive *"eine
Risikoprüfung und die Vereinbarung von Risikozuschlägen und Leistungsausschlüssen"* — is allowed a
*Wartezeit* of *"höchstens fünf Jahre"* under Nr. 6 [R8], while the underwritten form usually has
none, as the retrieved tariff does not [S5]. The mechanic that matters for the model: **a deferred period on
a population with elevated mortality removes disproportionately more claims than the same period
would on a healthy population**, because a material share of new claimants die inside it — selection
*at onset*, not at underwriting.

### *Beitragsbefreiung im Leistungsfall*

**The rule.** Premiums are waived while the annuity is payable, and the obligation revives if the
annuity stops. This is standard for German *Pflegerenten* and is contractual, not discretionary
[S4].

**What it does.** On a contract issued at 45 and claiming at 82 the waiver removes the remaining
premium stream for the whole paying period — of the order of four years of premium, the same order
as one year of benefit at the modelled levels. Its cost sits inside the level premium and is one
reason a *Pflegerente* is dearer than a *Pflegetagegeld* of nominally equal benefit. The interlock
with the *Leistungsstaffel* is the subtle part: waiver runs from the first grade at which an annuity
is payable, so on the 0 / 30 / 50 / 75 / 100 grid a life at *Pflegegrad* 1 **is in care, receives
nothing, and still pays the premium**, while on the *Pflege-Bahr* grid it is waived — so two tariffs
differing only in whether they insure grade 1 differ in premium *income* as well as benefit outgo,
in opposite directions.

### *Nachprüfung*, *Herabstufung* and *Reaktivierung*

**The rule.** The paying state has **three** exits, not one. A life receiving the annuity may die;
may be downgraded to a lower insured grade, at which the annuity falls to that step; or may be
downgraded below the insured threshold or recover to the active state, at which the annuity stops
and the premium revives [S4]. **Only death is absorbing.**

**What it does.** This is the most important structural fact for an implementation. A model that
treats "in claim" as one state exited only by death **overstates** the liability; one that treats
every downgrade as a termination **understates** it. The model therefore carries the *Pflegegrad*
explicitly and moves lives between grades in both directions. Some tariffs guarantee that an annuity
once granted will not be reduced, and **the retrieved wording is one of them, on a duration
condition rather than outright**: twelve months of continuous annuity at grade 4 or 5 make the
premium waiver permanent, and twenty-four months make the annuity itself payable for life *"auch
wenn die Versicherte Person in einen geringeren Pflegegrad eingestuft wird oder die
Pflegebedürftigkeit komplett wegfällt"* [S4]. Whether that pattern is **common** is still not
established (gap 17), and it matters: on such a wording the paying state is exited only by death
after two years, and the state space collapses for the surviving majority of claims. The composite
models the **unguaranteed** form, the more general one; a user holding the guarantee obtains it by
setting the recovery and downgrade rates to zero — and, on the retrieved wording's shape, would want
to do so only after the first twenty-four months. The *Nachprüfung* itself is a documentation
exercise rather than the adversarial re-assessment that characterises *Berufsunfähigkeit*, because
the evidence is the statutory determination [R6] [S4].

### The level guaranteed *Beitrag*

**The rule.** The *Beitrag* is level and guaranteed for the life of the contract, subject only to §
163 VVG [R11] [REG-R27]. This is the product's defining commercial property and the whole of its
price premium over a *Pflegetagegeld*.

**What it does.** The insurer carries the **basis risk** on a fifty-year view of a table built on a
superseded assessment regime, and § 163 is a narrow escape: it needs a non-temporary, unforeseeable
change in a calculation basis, an appropriate and necessary new premium and a trustee's
confirmation, and is **excluded** to the extent the original calculation was insufficient and a
diligent actuary should have recognised it [REG-R27]. The premium must be prudently calculated and
permanently sufficient under § 138 VAG [REG-R8], which bites hardest on the
*Pflegewahrscheinlichkeiten*. German biometric products are conventionally quoted as a
*Bruttobeitrag* with a lower *Zahlbeitrag* below it, the gap being a discretionary surplus rebate
withdrawable **without invoking § 163 at all** [REG-R27] [REG-R53] — so a level *Zahlbeitrag* is not
the same promise as a level *Bruttobeitrag*. **Whether the *Pflegerente* market quotes the pair as
the *Berufsunfähigkeit* market does was not established** (gap 18); the composite models the
*Bruttobeitrag* and no rebate.

### The *Deckungskapital* as an ageing reserve

**The rule.** The contract is calculated ***nach Art der Lebensversicherung***, so the reserve is a
***Deckungsrückstellung*** under § 341f HGB and the DeckRV [R12] [R13] [REG-R14] [REG-R54] — **not**
an *Alterungsrückstellung*, the private-health-insurance object of § 146 VAG. The precise words are
worth using: *the* Deckungskapital *of a* Pflegerente *is an ageing reserve in economic function and
a* Deckungsrückstellung *in law and in the accounts*.

**What it does.** The annual probability of entering care is negligible before 60, small to 75 and
rises steeply thereafter, so the level premium is far above the risk premium for three or four
decades and far below it afterwards. Issued at 45, the *Deckungskapital* rises for roughly
thirty-five years, peaks in the early eighties where the incidence curve crosses the level premium,
then runs off — later-peaking and smaller relative to premiums paid than an endowment's, and very
much larger than a *Risikolebensversicherung*'s. *Zillmerung* up to 25 ‰ of the *Beitragssumme*
[REG-R16] produces a negative reserve in the earliest years and a correspondingly poor
early-duration surrender value. Two consequences reach the model: **interest sensitivity is the
highest in delib**, because benefits fall on average some thirty-five years after issue; and **lapse
is profitable early and expensive late**, so lapse feeds the premium through the equivalence
principle in a real tariff — while the composite's pricing basis is deliberately **lapse-free**,
because that is German first-order practice and because the house style forbids a pricing quantity
that depends on a behavioural assumption that depends on the path that depends on the premium.

### *Rückkaufswert*, *Beitragsfreistellung* and the *Stornoabzug*

**The rules.** § 169 VVG entitles the policyholder to a surrender value computed as the
*Deckungskapital* on the premium calculation bases, with a floor equal to the value that results
from spreading acquisition and distribution costs evenly over the **first five contract years** — a
floor on the value, not a cap on the charge — and a *Stornoabzug* admissible **only if agreed,
quantified and appropriate**, a deduction for unamortised acquisition costs being expressly
ineffective and the burden of proof lying on the insurer [REG-R28]. § 165 gives an independent right
to *Beitragsfreistellung* at any premium due date, the reduced benefit computed on the same § 169
value and **stated in the contract for each insurance year** [REG-R28].

**What they do, and the open question, restated.** § 169 Abs. 1 is not an exception for death-only
covers — it is a **positive scope test**: the surrender value is owed on a cover *"bei dem der
Eintritt der Verpflichtung des Versicherers gewiss ist"*. A *Risikolebensversicherung* falls outside
it because the obligation is not certain to arise, and on the face of the words a pure-risk
*Pflegerente* does not satisfy it either; § 176 extends §§ 150–170 *entsprechend* to the
*Berufsunfähigkeitsversicherung* and to nothing else. The **same** test governs the *Effektivkosten*
duty in § 2 Abs. 1 Nr. 9 VVG-InfoV, so the disclosure question and the surrender question are one
question. **The statutory point is still open** (gap 9). The one wording retrieved settles it for
that carrier the way this document assumed it would be settled: a guaranteed *Rückkaufswert*
*"nach § 169 des Versicherungsvertragsgesetzes"* with the five-year spread floor, on a product the
same conditions call *"eine reine Risikoversicherung ohne Sparprozess"* [S4]. The composite models a
*Rückkaufswert*, floors it at zero, and exposes the *Stornoabzug* as a parameter — a parameter the
retrieved wording sets at 25 %, not the nil-to-5 % this document assumed.

### *Überschussbeteiligung*

**The rule.** The contract participates in surplus under § 153 VVG and § 139 VAG like any other
German life contract, unless participation is excluded by agreement [R11] [R12] [REG-R24] [REG-R9].

**What it does.** The composition is different from an endowment's: there the surplus is dominated
by the *Zinsergebnis*, while here the reserve is smaller relative to the risk and the biometric
basis is the prudent one, so the ***Risikoergebnis*** dominates. That is the *Sicherheitszuschlag*
between the first- and second-order bases being released as experience emerges [REG-R47],
distributed through the *Rückstellung für Beitragsrückerstattung* under the MindZV and the RfBV
[REG-R10] [REG-R18] [REG-R19]. Application forms [unverified]: *Beitragsverrechnung*, dominant on
biometric-risk products; *verzinsliche Ansammlung*; and a *Bonus* form raising the *vereinbarte
Rente*. **The base run carries no *Überschussbeteiligung* at all**, deliberately: delib publishes
gross undiscounted cash flows, the surplus chassis is demonstrated by
`products/kapitallebensversicherung/`, and a discretionary *Beitragsverrechnung* would need a
declared-rate assumption this corpus cannot supply.

---

## Riders and options

**In scope, modelled or parameterized.** ***Leistungsdynamik im Leistungsbezug*** — escalation of
the annuity in payment; the retrieved tariff writes **1 % to 5 %** a year and confines it to the
**first ten years** of the annuity [S5], where this document previously assumed 1 % to 3 % and no
time limit. Off in the base run, implemented
as an escalation ledger running from the first month the annuity is payable; it is the economically
important dynamic on this product. ***Beitragsrückgewähr*** — a *Todesfallleistung* returning the
premiums paid, off in the base run, implemented in its **gross** form, without an annuity offset.
***Abgekürzte Beitragszahlungsdauer***, premiums to a fixed attained age, typically 65 or 85
[S5], which the retrieved tariff writes as *abgekürzt* with a five-year minimum. ***Einmalbeitrag***,
offered by the retrieved tariff and combinable with a running premium [S5], explicitly **not** the
base model here but carried so the chassis can price it. ***Wartezeit*** and ***Karenzzeit***, both zero in the base run; ***Risikozuschlag***, a
multiplier on the gross premium, 1.00 at standard rates; ***Stornoabzug***, 0 % in the base run. And
an alternative ***Leistungsstaffel***, the *Pflege-Bahr* grid as the market writes it — **not**, as
this document previously said, a statutory one [R8] — shipped beside the composite's own so that the
effect of the middle steps is demonstrable rather than asserted.

**Out of scope, and why.** ***Beitragsdynamik*** — indexation of premium and cover before claim; the
retrieved tariff offers **10 % every three years or 1–5 % a year**, ending *"nach dem 3. Widerspruch
in Folge"* [S5] — is not modelled at all: the acceptance rate on each offer is a
behavioural assumption this corpus cannot support, and a declined-out contract is an absorbing state
needing its own ledger. ***Überschussbeteiligung*** is deliberately omitted.
***Beitragsfreistellung*** and the § 38 VVG premium-default conversion keep the contract in force
with a reduced benefit; the composite treats every voluntary exit as a surrender and records the
bias. A ***Pflegetagegeld*** or ***Pflegekosten*** rider is a different legal branch under a
different supervisory regime [S2] [R14]; ***Pflege-Bahr*** is statutorily unavailable [R8]; bundled
assistance packages carry no material cash flow; and no joint-life *Pflegerente* is in the corpus.

---

## Variations across insurers

**One carrier's *Pflegerenten* document has now been read** — IDEAL's *IDEAL PflegeRente Exklusiv*
[S4] [S5] — where none had been before (gap 14). **One is not eight**, which is still the largest
difference between this specification and its frlib counterpart, where eight carriers' contracts
were read and the variation table has eight columns. What follows is therefore still the **parameter
range the German market is understood to write**, with an attribution column that now distinguishes
the one column that is attributed from the ranges that are not. Naming a carrier against a value no
source supplied would be exactly the fabrication house rule 3 forbids, and no value below is so
named except the retrieved one.

| Parameter | Observed / argued range | Retrieved wording [S4] [S5] | Basis |
|---|---|---|---|
| *Leistungsstaffel*, grades 1 to 5 | 0–10 % / 10–30 % / 30–50 % / 60–75 % / 100 %; the *Pflege-Bahr* grid is 10 / 20 / 30 / 40 / 100 %, a market convention and **not** statutory | **not a percentage grid at all** — three product lines paying 100 % from grade 2, from grade 3, or from grade 4; the same *Stufenmodell* the DAV bases use [R15] | ranges [unverified]; [R8] for what § 127 actually fixes |
| *Wartezeit*, underwritten / *Pflege-Bahr* / *Karenzzeit* | 0 to 3 years, usually waived for accident / up to 5 years / 0, 3 or 6 months | *Wartezeit* **keine** | ranges [unverified]; [R8] for the statutory five-year maximum |
| Entry age / purchase cluster / *vereinbarte Rente* as sold | 18 to 65, some to 70 / 45 to 60 / 1 000 € to 1 500 € per month | entry **18 to 75**; *Rente* permitted **250 € to 4 000 €**, minimum premium 60 €/yr | ranges [unverified]; retrieved column [S5] |
| *Beitragsdynamik* / *Leistungsdynamik* in payment / *Stornoabzug* | 3 % to 5 % / 1 % to 3 % a year / 0 % to about 5 % of the *Deckungskapital* | 10 % every 3 yrs or 1–5 %/yr, ending after three refusals / **1–5 %/yr, first ten years only** / ***25 %*, rising to 50 % after a withdrawal** | ranges [unverified] — **and the *Stornoabzug* range is contradicted by the retrieved wording**; retrieved column [S4] [S5] |
| *Todesfallleistung* / *Beitragszahlungsdauer* | none, *Beitragsrückgewähr*, fixed sum or *Deckungskapital* / lifelong, to 65, to 85 or *Einmalbeitrag* | optional *Beitragsrückgewähr* at 50–80 % of premiums (50–100 % on a single premium) / lifelong or abgekürzt, minimum five years, *Einmalbeitrag* or a combination | ranges [unverified]; retrieved column [S5] |
| Benefit by care setting / *Herabstufung* guarantee / territorial scope | setting-independent (modern) or reduced at home (older wordings) / present in some wordings, absent in others / not previously established | setting-independent / **guaranteed for life after 24 months at grade 4–5**, waiver permanent after 12 / worldwide cover, but assessment and every *Nachprüfung* must take place in the EU, Switzerland or Norway, failing which the contract ends | ranges [unverified]; gap 17; retrieved column [S4] |

**What can be said about carriers.** The delib brief names twenty-six German undertakings, and this
corpus establishes something about exactly **one** *Pflegerenten* writer, IDEAL Lebensversicherung
a.G. — a *Versicherungsverein auf Gegenseitigkeit* of Berlin, whose pack names its own conditions
AB-IPR-2022A and its supervisory *Sicherungsfonds* at Protektor Lebensversicherungs-AG [S4]. The
structural statement stands: ***Pflegetagegeld* is written by the *Krankenversicherer* in that list
and *Pflegerente* by the *Lebensversicherer***, and Stiftung Warentest's comparison of 70
*Pflegetagegeld* tariffs from 24 private **health** insurers contains no *Pflegerente* at all [S10].
Which other undertakings currently write a *Pflegerente* is still not established. **Where the ranges
would have come from:** Franke und Bornberg and Morgen & Morgen rate wordings clause by clause —
neither was retrieved; Assekurata's April 2026 study was, and supplies market counts, durations and
*Pflegetagegeld* premiums rather than *Pflegerenten* clause ranges [S14] [REG-R53]; Stiftung
Warentest and Finanztip publish comparative work, both concentrating on *Pflegetagegeld*, with the
scores paywalled [S10] [S12]; Verivox and Check24 quote on demand and were deliberately not used
[S13].

**What does not vary.** Three things above are legal facts rather than commercial ones and can be
stated without attribution: *Pflegegrad* 5 pays 100 %, which is the definition of the *vereinbarte
Rente* rather than a term; the premium cannot be re-rated outside § 163 VVG, because that is what
writing the cover as *Lebensversicherung* means [R11] [REG-R27]; and a *Pflegerente* cannot be a
*geförderter Tarif* under § 127 SGB XI, whatever its terms, because Abs. 2 Nr. 1 requires the
*Alterungsrückstellung* of § 146 Abs. 1 Nr. 2 VAG and Nr. 4 forbids any further benefit [R8] [R12].

---

## Regulatory context

**Social law — the trigger and the first layer.** SGB XI creates the *soziale Pflegeversicherung*
[R1]; the contribution rate is **3,6 %** of assessable earnings from 1 January 2025 and is still
`[unverified]` here — the rate lives in § 55 SGB XI and was not among the sections read. **The
benefit amounts were checked and did not change on 1 January 2026**: § 30 Abs. 1 uprated them by
4,5 % on 1 January 2025 and schedules the next rise for 1 January 2028 [R1]. §§ 14 and
15 define *Pflegebedürftigkeit* and the five *Pflegegrade* [R2]; §§ 36–38 the home-care benefits
[R3]; §§ 43 and 43c residential care and the *Leistungszuschläge* [R4]; §§ 39, 42 and 45b the
secondary heads [R5]; § 18 and the *Begutachtungs-Richtlinien* the assessment [R6]; § 23 the
compulsory private equivalent [R7]; § 127 the *Pflege-Bahr* subsidy [R8]. The reform acts that
matter are **PSG II**, which introduced the five grades and the *einrichtungseinheitlicher
Eigenanteil* from 1 January 2017 — *vom 21. Dezember 2015, BGBl. I S. 2424* [R9] — and the **PUEG**
of 2023, whose uprating mechanism is now § 30 SGB XI [R10]. §§ 61–66 SGB XII provide the
means-tested backstop, § 61a carrying the SGB XI definition of *Pflegebedürftigkeit* across so that
the third layer and the backstop share one trigger [R24].

**Contract law — the VVG.** § 7 and the VVG-InfoV impose the pre-contractual information duties,
including the euro disclosure of acquisition and administration costs [R11] [REG-R31]. § 19 governs
the *vorvertragliche Anzeigepflicht*, with § 21 Abs. 3 extinguishing the insurer's remedies after
**five years**, ten where the breach was intentional or fraudulent [R11] [REG-R30] — on a product
whose claims arrive forty years after underwriting, the time bar is what confines the
*Gesundheitsprüfung*'s effect on incidence to the first decade. § 152 Abs. 1 gives a **30-day**
*Widerruf* [R11] [REG-R23]; § 153 the
*Überschussbeteiligung* [REG-R24]; § 155 the annual *Standmitteilung* [REG-R25] [S8], **owed only on
contracts carrying an *Überschussbeteiligung*** and listing five items — the benefit on a claim plus
surplus, the benefit plus guaranteed surplus on continued and on paid-up terms, the surrender
payout, and for contracts from 1 July 2018 the sum of premiums paid — which here reports the
guaranteed *vereinbarte Pflegerente* rather than a sum insured; § 163 the whole of a life insurer's
re-rating power [REG-R27]; and §§ 165–170 the paid-up conversion, the surrender value, the five-year
floor and the *Stornoabzug* [REG-R28]. And § 203, the *Beitragsanpassung*
provision that dominates the *Pflegetagegeld* comparison, **applies to health insurance and not to
life insurance** [R11] [R14] — which is the point of the entire comparison in this document.

**Whether Kapitel 6 VVG reaches this product was not established.** §§ 172–177 are the
*Berufsunfähigkeitsversicherung* chapter, and § 177 Abs. 1 extends §§ 173–176 to contracts promising
a benefit for a lasting impairment of **working capacity** [REG-R29]. A *Pflegerente* promises a
benefit for dependency, not for impairment of working capacity, so on the face of it the extension
does not reach it — but the point is [unverified], and it matters: § 174's rule that a cessation of
liability takes effect only after notice in *Textform* and only from the end of the **third month**
following it would, if it applied, put a three-month tail on every *Herabstufung* and every
*Reaktivierung*. **The model does not implement such a tail**, and this is the reason.

**Supervisory law, reserving and the technical rate.** § 138 VAG requires premiums to be prudently
calculated and permanently sufficient [REG-R8]; § 139 governs the *Überschussbeteiligung* and the
*Sicherungsbedarf* test [REG-R9]; §§ 140 and 145 the *Rückstellung für Beitragsrückerstattung*
[REG-R10], with the MindZV [REG-R18] and the RfBV [REG-R19] below them; §§ 141–143 create the
*Verantwortlicher Aktuar* and the *Treuhänder* whose confirmation § 163 VVG requires [REG-R11]; and
§ 146 defines the *substitutive Krankenversicherung* regime, cited only to locate the boundary this
product sits on the other side of [R14]. Above it sits Solvency II, reaching German life business
**through** the VAG [REG-R1] [REG-R2] [REG-R5] [REG-R6], with Directive (EU) 2025/2 effective 30
January 2027 [REG-R3]; nothing here implements a 2027 basis. § 341f HGB requires the
*Deckungsrückstellung* to be computed prospectively on the tariff bases [R12] [REG-R54]. § 2 DeckRV
fixes the *Höchstrechnungszins*, raised to **1,00 % from 1 January 2025** by the Sechste Verordnung
of 19 July 2024 — the first increase in about thirty years — after 0,25 % for 2022–2024 and 0,90 %
for 2017–2021 [REG-R14] [REG-R15]; the rate applies **at contract conclusion and then stays with the
contract for its whole term**, which is why the German in-force book is a stack of cohorts and why
an in-force model point carries its own cohort's rate rather than today's. § 4 DeckRV caps the
*Zillmersatz* at 25 ‰ of the *Beitragssumme*, cut from 40 ‰ from 1 January 2015 by the LVRG
[REG-R16] [REG-R20], and interacts with the independent § 169 VVG five-year floor: the DeckRV
governs what the insurer may **reserve**, § 169 what it must **pay**, both applying separately with
the tighter binding [REG-R28]. § 5 Abs. 3 DeckRV builds the *Referenzzins* behind the
*Zinszusatzreserve* [REG-R17], which this model does not compute.

**Biometric bases.** **DAV 2008 P** is the market-standard first-order basis for German LTC business
on the life chassis [R15] [REG-R51]. It is a **multi-state** table, supplying
*Pflegewahrscheinlichkeiten* by sex, attained age and grade of entry, transitions between grades,
*Reaktivierungswahrscheinlichkeiten*, and, decisively, **separate mortality for active lives and for
lives in care, by grade**. **This document used to say the table is not public. It is**: the DAV
publishes the derivation as a free *Ergebnisbericht*, with the bases themselves in Anhänge 1 to 3,
and a companion report re-deriving them for the *Pflegegrade* [R15]. **delib still does not
redistribute any of it and no value from it appears anywhere in the library** — that is this
library's own choice, not a licensing constraint. It was built on the pre-2017 *Pflegestufen*, and
the BGH has held that no inference runs from a *Pflegegrad* back to a *Pflegestufe* [REG-R36]
[REG-R51]; the profession's answer was to re-derive rather than to map, on a ***Stufenmodell***
structure and from *Pflegestufen* data, because for the five grades *"fehlt naturgemäß jegliche
statistische Information"*. Applying any of it to a five-state per-grade chain is still the
insurer's own work — **the largest single basis risk in the product** (gap 10). The DAV's published
prudence loadings for this risk — an incidence *Gesamtzuschlag* of 20,5 % to 31,2 % by minimum
grade, an *Invalidensterblichkeit* *Gesamtabschlag* of 24,2 % to 28,5 %, and 13,6 % on
*Aktivensterblichkeit* — are recorded in `sources.md` and are **not** implemented here.

Two neighbouring tables enter narrowly: **DAV 2008 T** for a death
benefit written into the contract [R16] [REG-R48]; and **DAV 2004 R** as a **contrast** — an annuity
table is built to be prudent about people living *longer*, whereas the annuity here is paid to a
heavily impaired population, so using an annuity table **would be prudent in exactly the wrong
direction and would materially overprice the benefit** [R16] [REG-R49]. The German two-basis
structure — *erster Ordnung* for pricing and reserving, *zweiter Ordnung* for best estimate, the
*Sicherheitszuschlag* the wedge — is at [REG-R47], and for **care** the direction of prudence is
higher incidence, longer duration in care and **lower** mortality of care recipients.

**Unisex, tax and disclosure.** Sex-based differences in premiums and benefits are prohibited for
contracts concluded from 21 December 2012, following *Test-Achats* and §§ 19, 20 and 33 AGG
[REG-R34]; the tension is sharper here than anywhere else in delib, because the underlying bases are
sex-specific and the sex differential in LTC incidence and duration is large. Premiums are *sonstige
Vorsorgeaufwendungen* under § 10 Abs. 1 Nr. 3a EStG, deductible only within an annual ceiling of the
order of **1 900 €** or **2 800 €** — § 10 Abs. 4 Sätze 1 and 2 EStG, the lower figure applying to
taxpayers with an employer or public contribution to their health cover [R23] — a ceiling the compulsory contributions of Nr. 3 normally exhaust on their own. § 10 Abs. 4 Satz 4
makes the consequence explicit — where the Nr. 3 contributions exceed the ceiling, they are deducted
and *"ein Abzug von Vorsorgeaufwendungen im Sinne des Absatzes 1 Nummer 3a scheidet aus"* — so **in
practice, for most buyers, the premium is not deductible at all**, which is why the *Pflege-Bahr*
*Zulage* was designed as a direct subsidy [R8]. **The taxation of the benefit is unresolved** (gap 13): either exemption
under § 3 Nr. 1a EStG, the analysis universally applied to *Pflegetagegeld*, or *Ertragsanteil*
taxation under § 22 Nr. 1 EStG as a *Leibrente*, the analysis applied to a *Berufsunfähigkeitsrente*
and the one this product's life-assurance form argues for [R23] [REG-R41]. § 3 Nr. 1a exempts
*"Leistungen aus einer Krankenversicherung, aus einer Pflegeversicherung und aus der gesetzlichen
Unfallversicherung"* without saying whether a life-branch *Pflegerente* is a *Pflegeversicherung*
for that purpose; the tag stays because **the statute is silent on the point and no administrative
guidance or authority was retrieved**. **delib does
not model taxation of the benefit** and states the open question instead; a *Todesfallleistung*
follows the ordinary life treatment [REG-R45] [REG-R46]. Whether the product is a **PRIIP** likewise
depends on its own design and **was not established** (gap 16): the Regulation excludes contracts
whose benefits are payable only on death or in respect of incapacity [REG-R32] [unverified], so a
pure-risk form falls inside the exclusion while a *Beitragsrückgewähr* form very likely does not —
which makes the presence or absence of a KID in a carrier's document library **evidence about the
tariff's design**. The IDD conduct layer applies in any event [REG-R33], as does BaFin's
*Wohlverhaltensaufsicht* strand [REG-R35] — though **no BaFin material specific to LTC was located**
(gap 11). The DAV's *Fachgrundsätze* bind its members and the DAV makes the annual
*Höchstrechnungszins* recommendation [REG-R56]; IFRS 17 applies to IFRS reporters with no German
carve-out [REG-R55]; the statutory accounts run on HGB §§ 341–341o, the RechVersV and the BerVersV
[REG-R54].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-pflegerentenversicherung-r1
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
[R24]: #delib-pflegerentenversicherung-r24
[R3]: #delib-pflegerentenversicherung-r3
[R4]: #delib-pflegerentenversicherung-r4
[R5]: #delib-pflegerentenversicherung-r5
[R6]: #delib-pflegerentenversicherung-r6
[R7]: #delib-pflegerentenversicherung-r7
[R8]: #delib-pflegerentenversicherung-r8
[R9]: #delib-pflegerentenversicherung-r9
[REG-R1]: #delib-reg-r1
[REG-R10]: #delib-reg-r10
[REG-R11]: #delib-reg-r11
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R25]: #delib-reg-r25
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
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R46]: #delib-reg-r46
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R51]: #delib-reg-r51
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
