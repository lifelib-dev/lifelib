# Product Specification

**Status:** Draft, 2026-08-29 (sources accessed 2026-08-29); citations re-verified against the
primary documents 2026-08-30.

**Scope note.** This is a *standardized composite specification* assembled for reference liability
cash-flow modeling of a German **klassische aufgeschobene private Rentenversicherung** — the classic
deferred private annuity of *Schicht 3*, in which a premium accumulates in the *Deckungskapital*
(policy reserve) of the insurer's general account at a guaranteed *Rechnungszins* (technical interest
rate), participates in the *Überschussbeteiligung* (profit participation), and is converted at a
contractually fixed *Rentenbeginn* (annuity commencement date) into a lifelong *Leibrente* at a
*Rentenfaktor* (annuity factor) — or taken instead as a lump sum under the *Kapitalwahlrecht*. **It
does not describe any single insurer's contract.** Facts carrying a source tag — [S#] (primary
product documents: AVB, *Verbraucherinformation*, *Kundeninformation*, GDV *Musterbedingungen*,
insurer product pages, surplus declarations) and [R#] (product-specific regulatory and actuarial
references), both numbered per `_research/klassische_rentenversicherung.md` and resolved in
`sources.md` (**numbering frozen, never renumbered**), and [REG-R#] (the cross-product reference
library, whose own numbering is separate and also frozen) — are attributed to the cited document.
Values marked **[std]** are standardizations introduced for the reference implementation, each with
a numbered footnote giving the rationale and, where the research file recorded one, the observed
range. Claims no retrieved document confirms are flagged [unverified].

**Retrieval conditions — read this before relying on a single number below.** This specification
was **drafted** under an organisation network policy that blocked direct HTTP egress from the build
environment: `WebFetch` and `curl` were refused with HTTP 403 for `gesetze-im-internet.de`,
`bafin.de`, `gdv.de`, `aktuar.de` and every insurer host named here, the only channel was
`WebSearch` result summaries, and the session's shared budget was exhausted after eighteen queries
on this product. The first draft therefore rested on the authoring model's own knowledge of German
insurance law and practice, tagged **[std]** wherever it standardized a level and [unverified]
wherever it could not confirm a specific. **That policy has since been lifted, and the citations
were re-verified against the primary documents on 2026-08-30.** Of the forty-three entries in
`sources.md`, **thirty-six now read `Retrieved: yes`** — the VVG, EStG and DeckRV sections read as
canonical XML with each law's amendment *Stand* recorded, and the AVB, *Verbraucherinformationen*,
*Kundeninformationen* and one *Überschussdeklaration* read as PDFs with their § numbering intact.
Four entries were reached only in part: the two DAV documents under a transfer cap and a defective
character mapping [R12] [R13], and two multi-URL entries where one link of each failed [R14] [R19].
Three could not be opened at all: a Zurich product page that answers with an empty body [S17], a
DEVK asset path that refuses with HTTP 403 [S19], and a paywalled trade-press article [R23].
**Read every claim below against its own entry**: where the entry says `Retrieved: yes` the
citation is a document that someone opened at the passage cited; where it does not, the citation
remains a **pointer, not a certificate** — it names the instrument the claim should be checked
against without asserting that anyone checked it. **The re-verification changed things**, and the
entries record what: the annuity-factor basis once attributed to [S8] is not in that document, the
living URL at [S11] now serves a successor design, [S1] leaves the pre-annuity death benefit blank,
and [S4] carries a *Beitragsrückgewähr während der Rentenzahlungszeit* the library had recorded as
unmentioned by any source. Each is stated on its entry in `sources.md`, and `model.md` lists where
the shipped model diverges from a retrieved document. **One of those retractions has not been
carried into the body of this file**: the CosmosDirekt conversion-basis sentence under *The
guarantee is a rate* below still quotes a search summary the retrieved AVB does not contain [S8].
What has **not** changed is the asymmetry this file is built around — **the corpus establishes the
mechanics of this product thoroughly and its levels barely at all.** No charge parameter, no issue
envelope and no behavioural rate was established at any carrier for any year; every one of those is
**[std]** below and none is presented as a market rate. The *Rentenfaktor* levels [R19] [R24] and
the declared surplus rate [S15] the pass did establish are market observations the model does not
adopt, and are labelled as such where they appear.

**The composite draws on ten carriers and one industry body** — the GDV [S1] [S2] [S3] [S10],
Zurich [S4]–[S7] [S16] [S17], CosmosDirekt [S8], NÜRNBERGER [S9], Debeka [S11] [S12], Allianz [S13],
Mecklenburgische [S14], Konzern Versicherungskammer [S15], Stuttgarter [S18] and DEVK [S19] — each
of which is listed with what it establishes, and what it does not, in *Variations across insurers*
below. Where a row there reads "not established", **that is the finding, not an omission**.

---

## Product overview and market role

A *klassische aufgeschobene private Rentenversicherung* is a life insurance contract under the
VVG on a single life in which the insurer's obligation is **an annuity payable for the annuitant's
lifetime, beginning at a contractually fixed date**, with an accumulation period before it [S1]
[S4] [S8] [S9]. The insurer's own placement is *Schicht 3 — Private Vorsorge*: Zurich's scope line
reads "Aufgeschobene Rentenversicherung — **Private Vorsorge (Schicht 3)** und
Rückdeckungsversicherung (Schicht 2)" [S4]. Schicht 3 is the unsubsidised layer of the
*Drei-Schichten-Modell* introduced by the *Alterseinkünftegesetz* from 1 January 2005 [REG-R38]:
no § 10 EStG deduction, no state *Zulage*, no certification under the
*Altersvorsorgeverträge-Zertifizierungsgesetz*. The boundary is visible in the GDV's own taxonomy,
which maintains **separate** model conditions for the *Basisrente* and for certified
*Altersvorsorgeverträge* [S3]; this product is the one **without** a statutory qualification
clause in its title [S1] [S2].

Four features make the German chassis what it is, and each changes the shape of the projected cash
flows.

1. **Two phases with a hard boundary.** The *Aufschubzeit* accumulates a *Deckungskapital*; the
   *Rentenbezugsphase* pays an annuity; the *Rentenbeginn* separates them [S1] [S4] [S8] [S11].
   Three distinct things happen at that one date and a model must sequence all three: the
   accumulated value is struck including surplus and *Bewertungsreserven* [S9]; the *Rentenfaktor*
   is determined by comparing two factors [S4] [S13]; and the *Kapitalwahlrecht* election takes
   effect [S12] [R21].
2. **The guarantee is a rate, and a property of the contract's vintage rather than of the market.**
   The *Rechnungszins* is capped for new business by the *Höchstrechnungszins* of § 2
   *Deckungsrückstellungsverordnung* [R7] [R11] [REG-R14], **and the rate applicable at conclusion
   then stays with the contract for its whole term** [REG-R14]. A German life book is a layered
   stack of guarantee vintages — 4,00 % for 07/1994–06/2000 down to 0,25 % for 2022–2024 and back
   to 1,00 % from 2025 [REG-R15] — so the *Rechnungszins* is a **model-point attribute, not a
   global assumption**. The retrieved wordings show both halves of that. CosmosDirekt's LA 904 A,
   an **01.17** tariff, states *"der tarifliche Garantiesatz von 0,90 Prozent p. a."* [S8] — which
   is exactly the 2017–2021 cap, and so is a contract carrying its own vintage rather than today's.
   An insurer may also guarantee **less** than its vintage cap, and does: Debeka's safest post-2016
   variant guarantees 0,5 % [R22].
3. **The *Rentenfaktor* is a guarantee with upside, not a fixed conversion rate.** It is fixed at
   inception on the *Rechnungsgrundlagen* then in force [R24]; at *Rentenbeginn* a second, current
   factor is computed and **the higher of the two is guaranteed for the annuity payment period**
   [S4]. A model applying only the guaranteed factor understates the benefit whenever the current
   tariff is richer.
4. **The classic tariff is the market's reference chassis rather than a live new-business
   product.** Debeka, Allianz, Zurich and Generali are all reported to have stopped distributing the
   classic form, Debeka replacing it from 1 July 2016 with five "Chance" variants and Allianz with
   the KomfortDynamik premium-guarantee hybrid [R22] [S12] [S13] — yet Zurich publishes a
   *Verbraucherinformation für Konventionelle Versicherungen* for the deferred annuity in the
   **Fassung 01/2026**, on DAV 2004R at a *Rechnungszins* of 1,00 %, having published the same
   wording in Fassung 07/2015 and 01/2025 [S4] [S5] [S7] [S16]. **The tension resolves once the
   distinction between distribution and maintenance is drawn**: what [R22] reports, in 2016, is that
   the carriers stopped *selling* the classic form actively — of Allianz it says only that it would
   offer it *"wenn dies ausdrücklich vom Kunden gewünscht werde"* — while a wording reissued across
   three vintages is plainly still maintained (gap 9, narrowed). That is exactly why the right unit of description is a **composite of a chassis**, and it
   is the role a lifelib reference model is for: the in-force book still runs on this design.

**Market size.** German life insurers, *Pensionskassen* and *Pensionsfonds* together took premium
income of **94,6 Mrd €** in 2024, up 2,8 %, of which *laufende Beiträge* were **66,3 Mrd €**, roughly
flat, and *Einmalbeitragsgeschäft* about **28 Mrd €**, up about 10 %; the contract count fell 1,4 %
to **80,3 Mio** [REG-R53]. On the BaFin basis the life segment's *verdiente Bruttobeiträge* were
**90,4 Mrd €** — a different population on a different basis, and the two must never appear in one
table [REG-R53]. The GDV taxonomy reports *Rentenversicherungen* as one class covering both this
product and the immediate annuity, so **no figure isolating the classic deferred annuity was
established** [REG-R53]. For credited-rate context, the average *laufende Verzinsung* for **2025**
was **2,53 % Klassik / 2,58 % Neue Klassik**; for **2026** the sources give 2,6–2,7 %, 2,87 % and
2,54 % — three incompatible averages [REG-R53].

---

## Representative specification

The representative design is the chassis the corpus supports as a whole: a single-life deferred
annuity on the general account, Schicht 3, against a level recurring premium over a fixed
*Aufschubzeit* [S4] [S11], with *verzinsliche Ansammlung* as the accumulation-phase surplus system
[R24], a *Beitragsrückgewähr* death benefit in the premiums-only form named by the GDV model
wording [S1] [R24], conversion at `max(garantierter, aktueller Rentenfaktor)` [S4] [R24], and
*Rückkaufswert* and *Beitragsfreistellung* as separate decrements under §§ 169 and 165 VVG [R1]
[R2]. **Every number in it that is not source-tagged is [std].**

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-life deferred annuity on the general account (*konventionell*, *klassisch*); profit-participating; Schicht 3 | [S1] [S4] [S8] [S9] [S11] |
| Legal wrapper | Individual contract on the insurer's own AVB. A *Konsortialversicherung* edition of the same wording exists and changes the parties, not the cash flows | [S4] [S5] [S7]; [S6] |
| Lives basis | Single life. The survivor's annuity is a separate *Zusatzversicherung* with its own GDV model conditions, not a benefit of the base contract | [S10] |
| Premium form (model-point parameter) | (i) `laufend` — level recurring premium over the *Aufschubzeit*; (ii) `einmal` — *Einmalbeitrag* | (i) [S11]; (ii) [REG-R53]; split **[std]** (1) |
| Entry ages | 18 to 62 | **[std]** (2) |
| *Aufschubdauer* | 5 to 40 years | **[std]** (2) |
| *Rentenbeginn* age | 62 to 72; representative **67** | **[std]** (2) |
| Age basis | Age last birthday at inception, stepping at the policy anniversary | **[std]** (3) |
| Sex | Recorded, and **may not enter the tariff**: sex-based premium and benefit differences are prohibited for contracts concluded from 21 December 2012 | [REG-R34] |
| Premium envelope | 600 € to 24 000 € a year recurring; 5 000 € to 250 000 € single | **[std]** (2) |
| Anchor model cell | Male, issue age 50, issue year 2026, *Aufschubdauer* 17 years (*Rentenbeginn* at 67), 3 000,00 € recurring annual premium, *Rechnungszins* 1,00 %, *Beitragsrückgewähr* death benefit, *Rentengarantiezeit* 10 years, *Kapitalwahlrecht* take-up 30 % | **[std]** (4) |

1. **The market split between recurring and single premium was not established** (gap 13). The
   aggregate is that *Einmalbeitragsgeschäft* is about 30 % of German life premium income and grew
   about 10 % in 2024 against a flat recurring book [REG-R53]. The recurring form is the one
   [S11]'s accumulation mechanics describe; the single-premium form is a model-point value because
   the aggregate says it cannot be ignored.
2. **The entire issue envelope is unestablished at every carrier** (gap 13): no premium limits, no
   *Aufschubdauer* limits, no entry ages, no *Rentenbeginn* window. These are round-number
   placeholders chosen so the model point table can carry an interior anchor and boundary points
   either side, and should be replaced wholesale by anyone with a *Tarifblatt*. The one age with an
   external anchor is **67**, the *Regelaltersgrenze*.
3. No German source states an age convention for this product; age last birthday, stepping at the
   anniversary, is the delib-wide convention registered as `age_basis = "ALB"` in
   `tests/de_registry.py`, and it matters less here than in a protection product because the
   *Rentenfaktor* rather than a mortality lookup fixes the benefit amount.
4. Issue age 50 with a 17-year *Aufschubzeit* puts four things inside one projection: the whole
   accumulation phase in seventeen rows; the § 20 Abs. 1 Nr. 6 EStG **twelve-year** threshold at
   duration 12 and its **age-62** partner at duration 13 [REG-R45], together the strongest driver of
   German Schicht-3 surrender behaviour; the *Rentenbeginn* at 67; and a payout phase long enough
   for the *Rentengarantiezeit* to expire inside it.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level *Bruttobeitrag* over the *Aufschubzeit*, or a single *Einmalbeitrag* at inception | [S11]; [REG-R53] |
| Premium decomposition | The premium splits into the portion **required for risk and expense cover** and the remainder, the ***Sparbeitrag***, which is what accumulates: the *Deckungskapital* is "the sum of the contributions accumulated at the *Rechnungszins*, **insofar as these are not intended for risk and cost coverage**" | [S11]; from the other side, "from the savings portion, Debeka forms a *Deckungskapital* for the guaranteed benefits" [S12] |
| Payment frequency | Annual, half-yearly, quarterly or monthly | [S4]; **[std]** (5) |
| *Ratenzahlungszuschlag* | Annual 1,000; half-yearly 1,020; quarterly 1,030; monthly 1,050 | **[std]** (5) |
| Premium term | Equal to the *Aufschubdauer* in the representative design; a shorter paying term is a model-point parameter | **[std]** (6) |
| *Dynamik* / *Anpassungsversicherung* | Automatic annual increase of premium and benefit; a documented option with its own condition set, "Besondere Bedingungen für die Anpassungsversicherung in der Rentenversicherung" | [S4]; parameters **[std]** (7) |
| *Zuzahlung* | An ad-hoc additional single premium into a running contract. **Not established by any source in this corpus**; therefore not specified and not modeled | gap 15 |
| Non-payment path | Life insurance does not lose cover on a missed *Folgeprämie*: after a *qualifizierte Mahnung* in Textform with a minimum two-week period, § 166 VVG converts the contract to *prämienfrei* rather than terminating it | [REG-R28] [REG-R30] |

5. **No *Ratenzahlungszuschlag* percentage was established at any German carrier** (gap 14); the
   levels are a monotone [std] ladder in which the monthly mode costs 5 % more than the annual one.
   Note the interaction with *Zillmerung*: § 4 DeckRV takes the *Zillmersatz* on the
   *Beitragssumme*, the sum of all premiums payable [REG-R16], so the loading enters the
   acquisition-charge base as well as the premium.
6. No source establishes whether German tariffs permit a paying term shorter than the deferment; the
   representative design equates them and the model carries `prem_term_y` separately.
7. The *Dynamik* option is **established from a primary document** — a named section of the Zurich
   pack with its own condition set [S4] — but **its increase percentage, its basis, whether fresh
   underwriting applies and how many refusals end it are all unestablished** (gap 15). The
   implementation carries `dynamik_rate`, base 0, with 5 % on one point to exercise the mechanic.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Payment timing | Monthly **in advance** — *"Wir zahlen die Rente monatlich, jeweils zum Monatsersten"* [S9] § 1 Abs. 1. The GDV wording leaves the frequency to agreement, yearly to monthly [S1] § 1 Abs. 1 | [S9]; annual-grid compression **[std]** (8) |
| Conversion capital | The contract value used for annuitisation **includes any *Überschussbeteiligung* and *Bewertungsreserven*, subject to a minimum guaranteed contract value stated in the general contract data** | [S9] |
| *Rentenfaktor* applied | `max(garantierter, aktueller)` — the annuity computed on the bases current at *Rentenbeginn* is compared with the *garantierte Mindestrente* and the higher is paid. At NÜRNBERGER the comparison is made **at every monthly instalment**, not once: *"Wir prüfen bei jeder Monatsrente einzeln … und zahlen immer den höheren Betrag"* | [S9] § 1 Abs. 1; [S14] § 2 Abs. 3 and 6; [S18]; restated by [R24] |
| *garantierter Rentenfaktor* | Fixed at inception on the *Rechnungsgrundlagen* then in force, with a *Sicherheitsabschlag* making it lower than the current factor. Representative 28,00 € per month per 10 000 € at *Rentenbeginn* 67 | mechanic [S11] § 52, [S14] § 2 Abs. 6, [R24]; **level [std]** (9), against a 2025 market average of 24,33–27,18 by term [R24] |
| Its interest basis | **0,1 % p.a.** at one carrier, on that carrier's own annuity table *Debeka 07/16 R (RF)*, against a tariff *Rechnungszins* of 1 % for the guaranteed benefits — a deliberate prudential margin below the *Höchstrechnungszins* | [S11] § 52 Abs. 1 against § 28 Abs. 2 |
| *aktueller Rentenfaktor* | The carrier's **then-current immediate-annuity tariff**: *"maßgeblich sind Rechnungszins und Sterbetafel in der Beitragskalkulation vergleichbarer, dann bei uns zum Verkauf geöffneter Rentenversicherungen mit sofort beginnender Rentenzahlung"*, with a most-favourable rule where several comparables exist and a *Treuhänder* review of the factor | [S9] § 1 Abs. 1; [S14] § 2 Abs. 5; **level [std]** (9), against a 2025 market average of 27,27–30,40 by term [R24] |
| Annuity in payment | The sum of a *garantierte Rente* and an *Überschussrente*; only the guaranteed part is a promise — for the RfB-financed part *"wird die Rentenhöhe jeweils nur für ein Versicherungsjahr zugesagt"* | [S4] § 3 Abs. 7; [R20] |
| *Überschussverwendung* in payment | Policyholder's choice of *konstante*, *teildynamische* or *volldynamische Rente*, elected before the *Rentenbeginn* and not changeable after it. Carrier names: *Garantie-PLUS-Rente* / *Bonus-PLUS-Rente* / *Bonusrente* [S4] § 3 Abs. 7; *teildynamische Bonusrente* / *dynamische Überschussrente* [S9] § 2 Abs. 5 c); *Bonusrente* / *Überschussrente* [S15] | [S4] [S9] [S15]; [R20] [R21] [R24] |
| *Bewertungsreserven* in payment | Participation **continues during the annuity payment period**, allotted at each policy year end from the first — a contractual promise, not a § 153 rule | [S4] § 3 Abs. 2; [S9] § 2 Abs. 5 c); [S15] |
| *Rentengarantiezeit* | 10 years representative; 5, 10, 15, 20, 25 or 30+ offered; typically 15 years for retirement ages 61–70 and 10 for 71 and above; most choose 10 to 20 | [R24]; in the tariff name at NÜRNBERGER [S9]; selectable with a floor at Allianz [S13] |
| Death benefit before *Rentenbeginn* | ***Beitragsrückgewähr*** — *"die eingezahlten Beiträge (Beitragsrückgewähr) ohne Zinsen und ohne die Beiträge etwa eingeschlossener Zusatzversicherungen"* — in the premiums-only form. Documented alternatives: premiums **plus the attributable *Überschussbeteiligung***; the accumulated *Deckungskapital*; the greater of the two; and no benefit at all, which is the GDV base case where no extension is bought | [S8] § 1 Abs. 1; [S4] § 1 Abs. 2–3; [S9] § 1 Abs. 3; three forms [R24]. The GDV model wording leaves § 1 Abs. 3 blank for the carrier to fill [S1] |
| A `max(...)` death benefit | **Established for the classic product**: the contract value plus final surplus and *Bewertungsreserven*, *"mindestens jedoch die sogenannte Beitragsrückgewähr"*. The same clause warns the refund need not equal premiums actually paid — rider premiums are excluded and later contract changes re-base it | [S9] § 1 Abs. 3; hybrid form [S14] § 2 Abs. 9 a) |
| Death benefit timing | Payable on death, with the *Bewertungsreserven* measured for the month of, or before, notification [S15]. Whether the with-surplus form includes the whole *Ansammlungsguthaben* is carrier-specific: at Zurich the *verzinsliche Ansammlung* is paid out on death, surrender or commutation | [S4] § 3 Abs. 6; [S15] § 1.2–1.3 |
| Death after *Rentenbeginn* | Three documented mechanics, and the policyholder chooses among them: the *Rentengarantiezeit*; the survivor's-annuity rider, which begins only **after** any guarantee period expires; and ***Beitragsrückgewähr in der Rentenbezugsphase***, offered **as an alternative to** the *Rentengarantiezeit* — premiums paid less rider premiums less annuities already received at their inception-guaranteed level, the claim lapsing once instalments exceed premiums. **The reference model implements only the *Rentengarantiezeit***; the refund is a known omission, not an absent one | [S4] § 1 Abs. 4–5; [S10] § 1 Abs. 3; [R24] |
| *Kapitalwahlrecht* | The policyholder may take the accumulated capital as a lump sum instead of the annuity at *Rentenbeginn* | [S12] [R6] [R21] |
| Its notice period | Established, and carrier-specific: **three years** before the *Rentenbeginn* where the payout phase carries no death cover, otherwise not before the twelfth policy year or five months before the first annuity date [S4] § 2 Abs. 2–3; after twelve years, five months before at a twelve-year term [S8] § 1 Abs. 2; **two months** [S14] § 2 Abs. 7. The model treats the election as a decision at one known date with no notice mechanic | [S4] [S8] [S14]; simplification **[std]** (11) |

8. Every source describes the annuity as monthly, and one states the timing: *"Wir zahlen die Rente
   monatlich, jeweils zum Monatsersten"* — **monthly in advance** [S9] § 1 Abs. 1. The choice is worth about half a month's interest on the
   annuity's present value and shifts every payout cash flow by one period, so it is adopted
   explicitly: **monthly in advance**, compressed onto the annual grid as one payment at the start
   of each policy year.
9. **Market levels are established and the model's are not them.** [R24] gives 2025 averages of
   24,33–27,18 guaranteed and 27,27–30,40 current, by deferment term to age 67, and [R19] gives a
   current-factor average of 29,09 for 2021 falling to 25,97 for 2022. The values used here —
   guaranteed 28,00 €; current 32,00 € base, 25,50 € low, 35,00 € high, all at *Rentenbeginn* 67 —
   remain **anchors chosen so the worked example reproduces exactly and the `max()` rule is exercised
   in both directions**, not market rates, and the `base` current factor sits above every observed
   average. `model.md` records the divergence; the tables are unchanged.
10. The `max` form is offered as a model-point value because **a classic AVB states it** — the
    contract value plus final surplus and *Bewertungsreserven*, *"mindestens jedoch die sogenannte
    Beitragsrückgewähr"* [S9] § 1 Abs. 3 — and because a German contract is not eligible for the
    § 20 Abs. 1 Nr. 6 half-income treatment unless the *Todesfallleistung* meets the
    *Mindesttodesfallschutz* test [REG-R45]. The base case stays the plain *Beitragsrückgewähr* [S8].
11. Notice periods are documented and range from two months to three years [S4] [S8] [S14]. The
    election is still modelled as taking effect **at** *Rentenbeginn* with no notice mechanic; on an
    annual grid a notice period inside the last policy year moves nothing, but Zurich's three-year
    requirement does not fit inside one year, so this is now a stated simplification rather than a
    consequence of the grid.

### Underwriting and rating

**There is no underwriting.** A deferred annuity's biometric risk is longevity, which underwriting
cannot select against in the insurer's favour, and the pre-*Rentenbeginn* death benefit is the
premiums paid or the accumulated fund, so there is no sum at risk to underwrite — a structural
consequence of the benefit shape [S19] [R24] rather than a documented carrier practice, since **no
source in this corpus states an underwriting rule for a German deferred annuity**. It is tagged
**[std]** because the implementation acts on it: no rating factor, no select period and no
substandard loading anywhere in the model. The *Berufsunfähigkeits-Zusatzversicherung* carried in the
same pre-contractual pack has its own special conditions and its own underwriting [S4]. Rating runs
on entry age and *Aufschubdauer* through the tariff, and **sex may not be a rating factor** for
contracts concluded from 21 December 2012 [REG-R34]. Four statutory rules reach the contract without
being tariff parameters: the *Anzeigepflicht* of § 19 VVG, whose remedies § 21 Abs. 3 VVG
extinguishes *"nach Ablauf von fünf Jahren nach Vertragsschluss"*, ten years where the duty was
breached intentionally or fraudulently, and not at all for insured events occurring inside the
period — confirmed at article level, *Stand: Art. 12 G v. 26.5.2026*; § 157 VVG, under which an age misstatement changes the benefit
in the ratio of the premium for the true age to the agreed premium; § 150 VVG, requiring the written
consent of the insured where a policy is on another person's death above ordinary funeral costs; and
§ 161 VVG, excluding intentional suicide within three years while still requiring payment of the
*Rückkaufswert* including profit shares under § 169 [REG-R26] [REG-R30]. **The model wordings do
apply the rule to this product, and cap it against the death benefit**: [S1] § 5 Abs. 2 pays the
surrender value computed for the date of death, without the *Abzug*, *"allerdings nicht mehr als eine
für den Todesfall vereinbarte Kapitalleistung"* — so in a *Beitragsrückgewähr* design the premium
refund is the ceiling, and the exclusion can only reduce the benefit, never inflate it. [S4] § 6 and
[S8] § 11 do the same. The mechanic is therefore established and is **not modelled**, because a
single deterministic decrement carries no cause of death.

### Charges

**This is the weakest area of the corpus.** No charge parameter was established for this product at
any German carrier (gap 14) — not the *Abschluss- und Vertriebskosten* rate, the *Verwaltungskosten*
in any form, the *Ratenzahlungszuschlag*, the payout-phase administration charge or the
*Effektivkosten* disclosure — and no *Produktinformationsblatt* or *Basisinformationsblatt*
(PRIIP-KID) for a classic deferred annuity appears in the corpus at all. The two figures it does
contain — an *Abschlussprovision* of **1 575 €** on an Allianz specimen quotation, and total costs
relative to the capital formed of **at most 0,95 € per 100 €** — come from third-party analyses of
**Schicht-1 and Schicht-2** variants and are [unverified] as Schicht-3 levels; neither survived the
2026-08-30 retrieval pass, because [R23] is paywalled and [S13] does not carry them, so they now rest
on search summaries alone [R23]. What the retrieved AVB do establish is the **charging mechanism**
rather than any level: four carriers state the *Zillmerverfahren* under § 4 DeckRV with the cap in
identical words, *"auf 2,5 % der … zu zahlenden Beiträge beschränkt"*, the balance of the acquisition
costs spread over the premium-paying term and the other costs over the whole contract [S1] § 14,
[S4] § 11, [S8] § 8, [S9] § 16. Every carrier refers the actual amounts to the *Kostenausweis nach
§ 2 VVG-InfoV* or the *Persönlicher Vorschlag*, neither of which is a public document — which is why
this gap is structural and will not close from published wording.

| Parameter | Representative value | Basis |
|---|---|---|
| Charge structure | **Premium-based deductions, not asset-based ones**, in the classic chassis: costs and the *Risikobeitrag* come out of the premium and the *Sparanteil* forms the *Deckungskapital* — *"die eingezahlten Beiträge abzüglich der tariflichen Kosten und Risikobeiträge"* | [S8] § 1 Abs. 2; [S11] § 27 Abs. 1 |
| *Abschluss- und Vertriebskosten* (α) | **25 ‰ of the *Beitragssumme***, zillmered — charged against the earliest premiums until exhausted | cap [REG-R16]; use of the cap **[std]** (12) |
| Legacy α vintage | **40 ‰** for contracts concluded before 1 January 2015; the rate used at conclusion applies for the whole term | [REG-R16] [REG-R20] |
| *Verwaltungskosten* on premium (β) | 4,0 % of each gross premium | **[std]** (12) |
| *Verwaltungskosten* on the reserve (γ) | 0,20 % p.a. of the *Deckungskapital* | **[std]** (12) |
| *Risikobeitrag* (ρ) | The tariff mortality rate on the net amount at risk, `max(0, death benefit − Deckungskapital)` | structure [S8] § 1 Abs. 2, [S11] § 27 Abs. 1; level follows the table |
| *Stornoabzug* | 2,0 % of the computed surrender value. A deduction is permitted **only if agreed, quantified (*beziffert*) and appropriate (*angemessen*)**, and **a deduction for not-yet-amortised acquisition and distribution costs is void**. Observed market forms: none at all [S8] § 7 Abs. 10, [S9] § 14 Abs. 4; a flat **250 EUR**, waived at attained age 62 or after twenty years [S4] § 10 Abs. 3; **5 % of the *Deckungskapital*** for collectively provided risk capital plus 0/5/10/15 % keyed to the ten-year swap spread, **both tapering linearly to nil over the last ten years of the *Aufschubzeit*** [S11] § 34 Abs. 4–5 | [R1] [REG-R28]; level and flat shape **[std]** (12) |
| Payout-phase administration | 1,5 % of each annuity instalment | **[std]** (12) |
| *Effektivkosten* | Required by the German disclosure regime; **no value established for this product** | gap 14 |

12. **Every charge level above is a placeholder and none is a market rate.** Two have an anchor of a
kind: the α rate is the **statutory ceiling** of § 4 DeckRV — 25 ‰ of the *Beitragssumme* since
1 January 2015, 40 ‰ before [REG-R16] [REG-R20] — though using a ceiling as a tariff rate is a
modelling choice; and the *Stornoabzug* is a percentage because § 169 Abs. 5 requires it to be
*beziffert* and *angemessen* [R1] [REG-R28] and forbids it from recovering unamortised acquisition
costs, which is what makes the § 169 Abs. 3 floor rather than the deduction the operative constraint
on early surrender values. The retrieved wordings show that neither the percentage form nor the
absence of a duration term follows from the statute: two of four carriers levy nothing, one levies a
flat euro amount and one levies percentages that taper to nil. A flat, duration-free rate is
therefore a **modelling simplification** of a documented spread, and calling it a reading of
§ 169 Abs. 5 was wrong. The β, γ and annuity-administration rates have no anchor at all and are
sized so the total load is of the order the one Schicht-1/2 figure implies (0,95 € per 100 € [S13]
[R23]).

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| *Kündigung* / *Rückkaufswert* | Available at any time for the end of the current insurance period while recurring premiums are payable. The base measure is the *Deckungskapital* computed by recognised actuarial rules **on the calculation bases of the premium calculation** | [R1] [REG-R28] |
| **The statutory floor** | § 169 Abs. 3 VVG, at article level: *"bei einer Kündigung des Versicherungsverhältnisses jedoch mindestens der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt; die aufsichtsrechtlichen Regelungen über Höchstzillmersätze bleiben unberührt"* — a floor on the value, not a cap on the charge, and expressly independent of the supervisory *Zillmer* rules. Restated by five carriers | [R1]; [S1] § 12 Abs. 3, [S4] § 10 Abs. 3, [S8] § 7 Abs. 3, [S9] § 16 Abs. 4, [S11] § 34 Abs. 2; [REG-R28] |
| *Stornoabzug* | Permitted only if agreed, quantified and appropriate; a deduction for unamortised acquisition costs is void; the burden of proof is on the insurer | [R1] [REG-R28] |
| § 169 Abs. 6 | The insurer may in defined cases reduce surrender values to be paid out — a solvency valve, **not modeled** | [R1] |
| Surrender in the payout phase | **None.** § 168 Abs. 1 gives the right where *laufende Prämien* are payable, Abs. 2 on a single premium where the occurrence of the obligation is certain; a life annuity already in payment is neither | [REG-R28]; reading **[std]** (13) |
| *Beitragsfreistellung* | The policyholder may **at any time, for the end of the current insurance period**, demand conversion into a premium-free insurance, **provided the agreed *Mindestversicherungsleistung* is reached** | [R2] [REG-R28] |
| Its value | Calculated by recognised actuarial principles **on the calculation basis of the premium calculation, on the basis of the *Rückkaufswert* under § 169 Abs. 3 to 5**, and **stated in the contract for each insurance year** | [R2] [REG-R28] |
| Below the minimum | The insurer must instead pay the surrender value attributable to the insurance, **including profit shares**, under § 169 — a small contract cannot be made paid-up; it is cashed out | [R2] |
| The *Mindestversicherungsleistung* | Contractual, not statutory. Three carrier levels: **25,00 € a month** [S4] footnote 1 and [S9] § 1 Abs. 1; **600,00 € a year** for a partial surrender [S8] § 7 Abs. 2. Representative threshold: a guaranteed annuity of **30,00 € a month** | [S4] [S8] [S9]; level **[std]** (14) |
| Premium-default conversion | § 166 VVG converts automatically to *prämienfrei* rather than terminating cover — German lapse is a **three-way** decrement | [REG-R28] [REG-R30] |

13. No German source says whether a deferred annuity in payment may be surrendered; the reading
follows from § 168 VVG as recorded in the cross-product library
[REG-R28] and from the fact that the insurer's obligation in the payout phase has already occurred,
and the implementation acts on it by setting the lapse rate to zero from *Rentenbeginn*.
14. § 165 VVG makes the paid-up right conditional on a *Mindestversicherungsleistung* [R2], which the
contract fixes; two carriers set it at 25,00 € a month [S4] [S9]. The model's 30,00 € is chosen so one
model point trips it and is cashed out instead of being made paid-up — the branch the statute cares
about — and stays **[std]** because it is picked for that purpose rather than observed.

---

## Contractual mechanics

### The two phases and the *Rentenbeginn* boundary

The contract has two phases separated by the *Rentenbeginn*: the *Aufschubzeit*, over which premiums
are paid and the *Deckungskapital* accumulates, and the *Rentenbezugsphase*, over which the annuity
is paid [S1] [S4] [S8] [S11]. "Eine Aufschubzeit gibt es nur bei aufgeschobenen
Rentenversicherungen" — a deferment period exists only in a deferred annuity contract, the
definitional line separating this product from delib's `sofortrente` [R24].

**Three distinct things happen at the boundary** and a model that collapses them into one step will
get at least one wrong: the accumulated value is struck including surplus and *Bewertungsreserven*
[S9]; the *Rentenfaktor* is determined by comparing the guaranteed factor with the then-current one
[S4] [S13]; and the *Kapitalwahlrecht* election takes effect [S12] [R21]. The technical notes give
the boundary its own numbered position in the processing order for that reason.

### The *Deckungskapital* recursion

The definitional statement comes from an insurer: the *Deckungskapital* is **"the sum of the
contributions accumulated at the *Rechnungszins*, insofar as these are not intended for risk and cost
coverage"** [S11]; Debeka states the same split from the other direction [S12]. Unpacked into the
recursion an implementation carries — and this unpacking is a **reading** of [S11], not a clause the
corpus supplied in this form:

    Deckungskapital(t) = ( Deckungskapital(t-1) + Sparbeitrag(t) ) x (1 + Rechnungszins)
    Sparbeitrag(t)     = Beitrag(t) - Risikobeitrag(t) - Kostenbeitrag(t)

**The ordering of premium credit, charge deduction and interest accrual within a period is not
established by any source in this corpus** and is a [std] decision, stated explicitly in the
technical notes. The implementation credits the premium first, takes the charges next, and accrues
interest on the balance after both — the reading that makes the year-one interest credit largest, and
therefore the one that must be argued rather than assumed. The *Deckungskapital* is what everything
else is defined off: the death benefit in one of the two designs, the basis of the *Rückkaufswert*
[R1] and of the *beitragsfreie Versicherungsleistung* [R2], and — with surplus and
*Bewertungsreserven* added — the capital the *Rentenfaktor* applies to [S9].

### The *Rechnungszins* and the guarantee-vintage stack

The *Rechnungszins* is the rate at which the *Sparbeitrag* is guaranteed to accumulate — *"indem wir
die eingezahlten Beiträge abzüglich der tariflichen Kosten und Risikobeiträge mit dem tariflichen
Garantiesatz von 0,90 Prozent p. a. verzinsen"* [S8] § 1 Abs. 2 — capped for new business by the
*Höchstrechnungszins* of § 2 DeckRV [R7] [R11] [REG-R14]. **The cap and the *Garantiezins* are not
the same thing**, and the GDV says so in terms: *"Der Höchstrechnungszins ist eine Obergrenze für den
maximal zulässigen Rechnungszins, den Lebensversicherer bei der Berechnung ihrer Rückstellungen
nutzen dürfen. Er ist nicht mit dem Garantiezins gleichzusetzen, den Lebensversicherer individuell
auf ihre Produkte gewähren"* [R10]. A carrier may and does guarantee less: 0,5 % at Debeka's safest
2016 variant against a 1,25 % cap [R22], and 0,1 % on Debeka's current *Rentenfaktor* against its own
tariff rate of 1 % [S11] § 52 Abs. 1. **From 1 January 2025 the rate is 1,00 %**, raised from **0,25 %** by the *Sechste
Verordnung zur Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz* of 19 July 2024,
BGBl. 2024 I Nr. 250 [REG-R15], announced in the *Bundesgesetzblatt* on 24 July [R7] [R10] [R11]. The
ordinance itself now reads *"wird der Höchstzinssatz für die Berechnung der Deckungsrückstellungen
auf 1 Prozent festgesetzt"* at a *Stand* of Art. 1 V v. 19.7.2024 [R7]. **This was the first increase
since 1994**, the rate having fallen from 4 % in 1994 to 0,25 % in 2022 [R11], and the DAV recommends
1,0 % for 2026 as well [R8]. The mechanism is standing — DAV recommends, BMF legislates, with a lead
time of about eight months from the November 2023 recommendation to the July 2024 ordinance and
fourteen to effect [R9] — which makes the *Rechnungszins* of a tariff a parameter known well before
it binds. The full rate history is in the cross-product library [REG-R15]; the endpoints and the two
most recent points are corroborated here (gap 7).

**The vintage lock is statutory, not merely customary.** § 2 Abs. 2 Satz 1 DeckRV: *"Bei
Versicherungsverträgen mit Zinsgarantie gilt der von einem Versicherungsunternehmen zum Zeitpunkt des
Vertragsabschlusses verwendete Rechnungszins für die Berechnung der Deckungsrückstellung für die
gesamte Laufzeit des Vertrages."* [R7] One carrier's own packs show the stack forming: DAV 2004R with
**1,25 %** in Fassung 07/2015 [S5] [S6] and **1,00 %** in Fassung 01/2025 and 01/2026 [S7] [S16] [S4].

**The modelling consequence is that the *Rechnungszins* is a model-point attribute, not a global
assumption**, and that a model assuming the guaranteed rate equals the statutory cap is wrong in the
same direction at every carrier (overview, point 2).

### *Überschussbeteiligung* in the *Aufschubphase*, and the *Bewertungsreserven*

*Überschussbeteiligung* is the participation of policyholders in the surpluses of the undertaking
[R24]. Its magnitude depends, in an insurer's own contractual words, on "many influences which are
unpredictable and only limitedly controllable by the company, with the most important influencing
factor being capital-market developments" [S8]. **That disclaimer is why surplus is modelled as a
declaration — an insurer-discretionary current assumption — and never as a guarantee.** The
declaration instrument is an annual document: Bayern-Versicherung, in the Konzern Versicherungskammer
group, publishes its *"Überschussverteilung 2026"* as a standalone 145-page PDF [S15] and every German
life insurer publishes an equivalent. **Rates from that document are now established**, and their form
is itself the point: the *Zinsüberschussanteil* on annuity business of tariff generations 2015–2025 is
declared as **"3 % abzüglich Rechnungszins"** before the *Rentenbeginn* and **"3,35 % abzüglich
Rechnungszins"** during the *Rentenbezug* for 2026, against 2,25 % and 2,5 % for 2025 [S15]. The total
interest credited is therefore 3,00 %, whatever guarantee the contract carries — the German
construction the next paragraph sets out, written into a declaration.

The *Zinsüberschuss* arises **when investment income exceeds the *Rechnungszins***: "when investment
income exceeds the calculation rate, the insurance company generates surpluses in the form of
interest gains" [R24]. That is the direct statement that the *Rechnungszins* is the **hurdle rate**
of the surplus mechanism, and it is the fact behind the commonest arithmetic error in describing a
German contract. [S15] states it as an arithmetic operation rather than a description: the declared
*Zinsüberschussanteil* is a figure **less the *Rechnungszins***. The declared ***laufende Verzinsung*** is the *Garantieverzinsung* **plus** the
*laufende Zinsüberschussbeteiligung*, **not a surplus rate on top of the guarantee** [REG-R53]. On
the 1,00 % vintage a declared 2,55 % means a surplus credit of 1,55 %; on the 2,75 % vintage of 2004
the same declaration means a surplus credit of **nothing at all**, and the contract simply receives
its guarantee. Adding the declared rate to the guaranteed one overstates a modern contract by more
than half and a legacy contract by all of it.

**Three accumulation-phase surplus systems are established.** ***Verzinsliche Ansammlung*** is the
classic default and the representative system: declared surpluses are credited to a separate
***Ansammlungsguthaben*** and accrue with interest, "with the interest credited at the end of each
insurance year and upon termination of the insurance" [R24] — a **second, parallel account** to the
*Deckungskapital*, with its own credited rate, settling at year end and at exit. ***Bonusrente***
buys **additional premium-free annuity** with the declared surplus [R24]; it is established and
**not implemented**, because it is a second full mechanic on the same declaration and carrying both
would double the accumulation-phase state for a choice no source quantifies. **Investment of surplus
in an internal fund** is the Debeka successor design, a variation rather than the representative one
[S12]. ***Beitragsverrechnung*** is the fourth system the German market uses and **no source in this
corpus named it for this product** at drafting; it is now established at Zurich, where the surpluses
are set against the premium due and any excess paid out in cash, available only within a
*Rückdeckungsversicherung* [S4] § 3 Abs. 6 (gap 16 closed). The **four-component decomposition** is only one quarter established here (gap 17), is the
primary subject of the delib `kapitallebensversicherung` file, and has the MindZV's 90 / 90 / 50
minima under it [REG-R18]; the implementation models the credited outcome, not the source
decomposition.

**Bewertungsreserven.** Under **§ 153 Abs. 3 VVG** policyholders participate in the unrealised gains
in the insurer's assets, restated by an insurer's own consumer information as **equal (*hälftige*)
participation** [S4] [R4] [REG-R24]; the **transition to annuity payment is a key point** for it, so
the share crystallises at the boundary, and **participation continues during the payout phase** [S4]
[R4]. The LVRG 2014 restricted distribution to reserves from *festverzinsliche Wertpapiere* and
subjected departing policyholders' share to the *Sicherungsbedarf* test now in § 139 Abs. 3/4 VAG and
§§ 11–12 MindZV [REG-R20] [REG-R18]. The implementation carries the crystallisation at *Rentenbeginn*
as a [std] rate and does **not** implement the *Sicherungsbedarf* test, whose inputs are
balance-sheet quantities a single-policy liability projection does not have.

### The *Todesfallleistung* before *Rentenbeginn*

On death during the *Aufschubzeit* the contract pays a death benefit and ends. **Three designs are
established, all in use** [R24]: ***Beitragsrückgewähr*** — "the insurer refunds all paid premiums
after the death" — with an optional extension, "repayment of the premiums plus the
*Überschussbeteiligung* attributable to them can be agreed", so the choice between a bare and a
with-surplus form is contractual; **payment of the accumulated *Deckungskapital***; and a
***Hinterbliebenenrente***, which has its own GDV model condition set [S10] and is properly a rider.
**The term *Beitragsrückgewähr* appears in the GDV model conditions** [S1], but only in the footnotes:
§ 1 Abs. 3, the death benefit before the *Rentenzahlungsbeginn*, is left blank — *"zahlen wir …"* —
for the carrier to complete, so the model wording names the concept without specifying the benefit.
The carrier wordings do specify it, and a fourth design has to be added to the three above: **no
benefit at all**, which is the GDV base case and Zurich's, where death before the *Rentenzahlungs­
beginn* simply extinguishes the contract unless an extension was bought [S4] § 1 Abs. 2. The
`max(...)` form is **established for the classic product**, not only for the unit-linked sibling:
NÜRNBERGER pays the contract value plus final surplus and *Bewertungsreserven*, *"mindestens jedoch
die sogenannte Beitragsrückgewähr"* [S9] § 1 Abs. 3, and the same clause warns that the refund need
not equal premiums actually paid, since rider premiums are excluded and later contract changes
re-base it. CosmosDirekt's is the bare form, *"die eingezahlten Beiträge (Beitragsrückgewähr) ohne
Zinsen"* [S8] § 1 Abs. 1.

**What the death benefit is not:** there is no separate sum insured anywhere in this product — the
structural difference from delib's `kapitallebensversicherung` and `risikolebensversicherung`, and
why this product carries no underwriting and no rating factor [S19] [R24]. The benefit falls **on death**, with the *Bewertungsreserven* struck for the month of or before
notification [S15], and at Zurich the *verzinsliche Ansammlung* is paid out with it [S4] § 3 Abs. 6;
the implementation pays at the end of the policy year of death, which is a **grid** simplification,
and offers the surplus inclusion as a model-point switch.

### The *Rentenfaktor*, and the narrow channel for reducing it

This is the mechanic the whole product turns on and the best-evidenced thing in the corpus. The
factor determines how much monthly annuity is received per 10 000 € of accumulated capital [R24];
and three carrier wordings state it in those terms — *"wie viel Rente wir Ihnen monatlich je
10.000 Euro des zum Rentenbeginn zur Verfügung stehenden Fondsguthabens zahlen"* [S11] § 52 Abs. 1,
and likewise [S14] § 2 Abs. 5 and [S18]. The teaching illustration is 100 000 € at a factor of 25
yielding 250 € a month [R24], where the 25 is an **example, not a market level**; for market levels
see below:

    monthly_annuity = Kapital(Rentenbeginn) / 10 000 x Rentenfaktor

**Guaranteed at inception.** The *garantierter Rentenfaktor* is fixed in the contract documents on
the *Rechnungsgrundlagen* as at the date of conclusion [R24] — a guarantee given at issue about a
conversion decades later — with a ***Sicherheitsabschlag*** that makes it lower than the current
factor [R24]. **The margin is quantifiable from one carrier**: Debeka computes its guaranteed factor
on *"einen Rechnungszins von 0,1 % p. a. und die unternehmenseigene geschlechtsunabhängige
Sterbetafel „Debeka 07/16 R (RF)""* [S11] § 52 Abs. 1, while the guaranteed benefits of the same
contract run on a *Rechnungszins* of 1 % with the tables *Debeka 01/17 TL* and *Debeka 01/21 R*
[S11] § 28 Abs. 2. A tenth of the tariff rate is the *Sicherheitsabschlag* made concrete: the
guaranteed factor is priced as though the insurer will earn almost nothing on the annuity fund.
Across the market the same margin is visible in the levels — the 2025 average guaranteed factor is
24,33 at a forty-year term against an average current factor of 27,27, about 11 % [R24].

**Current, and the comparison.** The *aktueller Rentenfaktor* is recomputed on the bases in force
when quoted, and NÜRNBERGER says what "current" means operationally: *"maßgeblich sind Rechnungszins
und Sterbetafel in der Beitragskalkulation vergleichbarer, dann bei uns zum Verkauf geöffneter
Rentenversicherungen mit sofort beginnender Rentenzahlung"*, with a definition of comparability, a
named comparable tariff, a rule taking **the highest** factor where several comparables exist, and an
independent *Treuhänder* review of the factor's appropriateness [S9] § 1 Abs. 1. Mecklenburgische
says the same [S14] § 2 Abs. 5. That is why an immediate-annuity document [S16] belongs in this
product's source list — and [S16] shows the two tariffs sharing one basis at one carrier, DAV 2004R
at 1,00 %. **The rule at *Rentenbeginn* is a maximum of two factors**, and NÜRNBERGER states it as an
instalment-by-instalment test: *"Wir prüfen bei jeder Monatsrente einzeln, ob die rechnungsmäßige
Rente samt den in der Aufschubdauer und im Rentenbezug entstandenen Überschüssen höher ist als die
garantierte Mindestrente und zahlen immer den höheren Betrag"* [S9] § 1 Abs. 1; Mecklenburgische puts
it as a floor, *"Wenn die so berechnete Rente geringer ist als die garantierte Mindestrente …, zahlen
wir die garantierte Mindestrente"* [S14] § 2 Abs. 3.

    Rentenfaktor_applied = max( Rentenfaktor_garantiert, Rentenfaktor_aktuell(Rentenbeginn) )

This is a **guarantee with upside**, and it is the mechanic an implementation is most likely to get
wrong in the direction that understates the liability. The factor moves with the *Rechnungszins* and
with the mortality basis, because those are the two things it is computed from [S9] [S11] [S14].
**Market levels are established** and are lower than a modeller might guess. fragfina's 2025 analysis,
all to attained age 67, gives an average **current** factor of 27,27 at a forty-year deferment rising
to 30,40 at fifteen, and an average **guaranteed** factor of 24,33 rising to 27,18, with a lowest
guaranteed observation of 17,72 [R24]. Franke und Bornberg's comparison of the current factor across
carriers gives an average of **29,09 in 2021** falling to **25,97 in 2022**, a drop of 10,73 %, with a
highest of 26,61 and a lowest of 20,43 in 2022 [R19]. **The reference model's factors are `[std]` and
are not these numbers**; `model.md` records the divergence.

**Reducing a guaranteed factor.** Historically, insurers could change guaranteed *Rentenfaktoren* on
a ***Treuhänderklausel*** with an independent *Treuhänder*'s approval, on two triggers: an
**unexpectedly strong increase in life expectancy** and a **sustainable reduction in capital-market
returns** [R17] [R3]. **Currently the clause is used only in older contracts, and the guaranteed
factor can be changed only on the basis of § 163 VVG** [R17] [R3], which requires **three cumulative
conditions**: a change in the *Leistungsbedarf* that is neither temporary nor foreseeable; a newly
set premium that is appropriate and necessary to secure permanent fulfilment; and an *unabhängiger
Treuhänder* who has confirmed both [REG-R27]. Adjustment is **excluded** where the benefits were
insufficiently calculated originally and a diligent actuary should have recognised it — **the insurer
may not reprice its way out of its own mispricing** — and the article permits a **reduction of the
benefit** instead of a premium increase [REG-R27]. **The courts have narrowed it to vanishing point.** The Landgericht Köln held the low-interest phase
**not** a sufficient ground, being entrepreneurial risk that cannot be passed to policyholders —
***LG Köln, 08.02.2023, Az. 26 O 12/22***, against Zurich [R17] [R16] — and the Bundesgerichtshof held
the clause Allianz relied on to reduce a guaranteed *Rentenfaktor* ineffective, ***BGH, 10.12.2025,
Az. IV ZR 34/25*** [R16] [REG-R36]. The scale of what was at stake is on the record: Allianz reduced
guaranteed factors in existing contracts for **about 750 000 policyholders** in 2021, having used the
clause before in **2005 and 2017** [R18]. **The implementation treats the guaranteed factor as fixed
and records § 163 VVG as a model risk** — a treatment the 2025 decision supports rather than merely
approximates.

### The *Rentenphase* and the *Rentengarantiezeit*

The annuity in payment is **the sum of a *garantierte Rente* and an *Überschussrente***: the insurer
sets a value at the start of the payout phase "composed of the *Garantierente* and a surplus share
projected for the whole annuity period" [R20]. **Only the guaranteed part is a promise.** Three
*Überschussverwendung* systems exist and the choice is the policyholder's [R19] [R20] [R24]:

| System | Mechanic |
|---|---|
| ***konstante Rente*** | The payout stays the same over the whole term; the insurer fixes a value at the start of the payout phase from the *Garantierente* plus a surplus share **projected for the whole annuity period**. In practice it can still fluctuate: **if the provider earns less than expected, the annuity falls** [R20]. |
| ***teildynamische Rente*** | The annuity rises regularly by a **fixed percentage** provided the insurer earns corresponding surpluses — a combination in which part of the expected surplus is used under the constant system and part under the dynamic system [R20] [R24]. |
| ***volldynamische (steigende) Rente*** | The annuity **adjusts annually and flexibly to the actual surplus development** [R20]. It starts lowest and rises fastest. |

The ***Bonusrente*** is the mechanism underneath the rising forms — "the ongoing surplus shares are
used partly for an age-dependent *Überschussrente* and partly for an additional premium-free annuity
(*Bonusrente*)" [R24] — and the increment, once bought, is **premium-free and permanent**, which is
what makes a *volldynamische Rente* ratchet rather than fluctuate. **The constant form is not
actually constant**, which is exactly what a model gets wrong by taking a product name literally: the
annuity is set from a **projection**, and if the insurer earns less than projected it is reduced
[R20].

The ***Rentengarantiezeit*** is a guaranteed payment period beginning at *Rentenbeginn*: if the
annuitant dies inside it, **the annuity continues to be paid until the agreed years have expired**.
Both GDV model wordings and NÜRNBERGER's AVB carry the same worked illustration: a ten-year guarantee
with death after three years leaves seven years of instalments payable [S1] § 1 Abs. 4, [S9] § 1
Abs. 5. Two refinements the clause text adds. The remaining instalments may be **commuted to a lump
sum** at the beneficiaries' request — Zurich gives three months and computes the present value at the
payout-phase *Rechnungszins* [S4] § 10 Abs. 14, NÜRNBERGER on application and excluding future
increases [S9] § 1 Abs. 5 — and where a survivor's-annuity rider is also in force the commutation is
not available [S4] § 10 Abs. 15 and the survivor's annuity begins only **after** the guarantee period
expires [S10] § 1 Abs. 3. Durations, typical choices and cost are in the benefit-provisions table
above; the period is carried in the product name at NÜRNBERGER, tariff NIR3301 [S9].

**Its modelling consequence is a decrement-weighting one and it is the pitfall this product hides
best.** Inside the guarantee period the payment obligation does not depend on survival: the
instalment is due to the annuitant or to the survivors either way, so it must be weighted by the
**count that annuitised**, not by the count still alive; outside the period it is weighted by
survivors. The two counts differ by exactly the deaths inside the window, and a model that weights
everything by survivors understates the annuity outgo by that amount while never producing a number
that looks wrong.

### The *Kapitalwahlrecht*

The right to take **the accumulated capital as a lump sum instead of the lifelong annuity** at
*Rentenbeginn* [S1] § 1 Abs. 2, [S4] § 2, [S8] § 1 Abs. 2, and the third of the three things that
happen at that boundary. **Notice periods are established and are long.** Zurich requires the
application *"wenigstens drei Jahre vor Rentenzahlungsbeginn"* where the payout phase carries no death
cover, and otherwise not before the twelfth policy year, or, at exactly a twelve-year *Aufschubzeit*,
not earlier than five months before the first annuity date [S4] § 2 Abs. 2–3. CosmosDirekt ties it to
the same twelve-year tax line [S8] § 1 Abs. 2; Mecklenburgische asks two months [S14] § 2 Abs. 7. The
GDV model wording leaves the period blank for the carrier and notes that § 309 Nr. 13 BGB forbids
requiring more than *Textform* [S1] § 1 Abs. 2. **Partial commutation is also documented** — Zurich
requires the residual annuity to clear the *Mindestrente* and the payout to be at least 2 500 EUR
[S4] § 2 Abs. 4. The reference model treats the election as a decision at one known date and models
no notice mechanic, which is now a simplification of a documented rule.

**The tax consequence of electing it is total, and it is the established part.** The lump sum moves
the contract from the *Ertragsanteil* regime of § 22 EStG [R5] [REG-R41] to § 20 Abs. 1 Nr. 6 EStG
[R6] [REG-R45]: where the **"12/62 rule"** is met — at least 12 years of contract duration and
payment after completion of the 62nd year of life — **only half the *Unterschiedsbetrag* between the
*Versicherungsleistung* and the premiums paid is taxable**, at the **personal marginal rate** under
§ 32d Abs. 2 Nr. 2 EStG, and the *Halbeinkünfteverfahren* applies **only to lump sums and
payout-plan withdrawals, not to monthly annuity payments** — § 20 Abs. 1 Nr. 6 Satz 1 reaches the
difference *"soweit nicht die lebenslange Rentenzahlung gewählt und erbracht wird"* [R6] [REG-R45].
The age limb is **60** in the enacted text of Satz 2 and becomes **62** only through § 52 Abs. 28
Satz 7 EStG, *"für Vertragsabschlüsse nach dem 31. Dezember 2011"* — so the familiar "12/62 rule" is
precisely § 20 Abs. 1 Nr. 6 Satz 2 read with § 52 Abs. 28 Satz 7, and it is 12/60 for a 2005–2011
contract [R6] [REG-R45].

**Contracts concluded before 1 January 2005 are not in the *Halbeinkünfteverfahren* at all.** The
§ 20 Abs. 1 Nr. 6 EStG regime in its *Alterseinkünftegesetz* recast does not reach them; under the
predecessor regime — preserved by § 52 Abs. 28 Satz 5 EStG, which keeps § 20 Abs. 1 Nr. 6 *"in der am
31. Dezember 2004 geltenden Fassung"* in force for those contracts *"auch in allen offenen Fällen"* —
and where the pre-AltEinkG conditions are met (a term of at least twelve years, premiums paid for at
least five, and a minimum death cover) the *rechnungsmäßige und außerrechnungsmäßige Zinsen* contained
in a *Kapitalabfindung* are **entirely free of income tax** [R6] [REG-R45]. That is a better outcome than taxing half the *Unterschiedsbetrag*, not the same
one, and it is what makes an *Altvertrag*'s surrender and commutation rates close to nil. **The
pre-2005 conditions themselves were not established and are asserted nowhere in delib**
[unverified], which is why the reference model does not represent that cohort. Annuity payments run
on the *Ertragsanteil* basis in every cohort.

A German in-force book therefore carries **at least three tax cohorts** — pre-2005, 2005–2011 with
the age test at 60, and 2012 onwards with it at 62 — cut by the *Alterseinkünftegesetz* watershed of
1 January 2005 and the 31 December 2011 line [REG-R38] [REG-R45]. **delib's composite is a post-2011
contract**: `issue_year` is 2026 on the anchor, the table's earliest vintage is 2005, and the
pre-2005 cohort appears in it nowhere.

On the annuity side the whole statutory table is now on the record, at **§ 22 Nr. 1 Satz 3 Buchst. a
Doppelbuchst. bb EStG** — the address [S4]'s own tax notes use. Read off the age completed at the
start of the annuity: 22 % at 60–61, 21 % at 62, 20 % at 63, 19 % at 64, **18 % at 65–66**, 17 % at
67, 16 % at 68, 15 % at 69–70, 14 % at 71, falling to 1 % from 97 [R5]. And, unlike the Schicht-1
*Rentenfreibetrag*, **the percentage is what is frozen**, so surplus increases are taxed at the same
light rate [REG-R41]. [S4] adds two consequences the model does not compute but a reader should know:
returns earned during the *Aufschubzeit* are not taxable at all, and annuities continuing to survivors
under a *Rentengarantiezeit* stay on the *Ertragsanteil* basis.

**The two regimes are why the election is economically live** rather than a formality. **delib
computes no tax anywhere** [REG-R38], so the implementation carries the election as a **take-up
rate** and says explicitly that the rate stands in for a tax comparison the model does not perform.

### The *Rückkaufswert* under § 169 VVG

The surrender right exists and its value is governed by § 169 VVG [R1] [REG-R28]. The base measure is
the ***Deckungskapital*** computed by recognised actuarial rules **on the calculation bases of the
premium calculation** [REG-R28]. The *Zeitwert* rule of Abs. 4 is the boundary rather than the rule
here, because the classic contract's benefit is guaranteed [R1]. **The article-level text is now
read** (gap 12 closed): Abs. 3 Satz 1 defines the surrender value as *"das nach anerkannten Regeln
der Versicherungsmathematik mit den Rechnungsgrundlagen der Prämienkalkulation zum Schluss der
laufenden Versicherungsperiode berechnete Deckungskapital der Versicherung"*, and five carrier
wordings restate it verbatim [S1] § 12 Abs. 3, [S4] § 10 Abs. 3, [S8] § 7 Abs. 3, [S9] § 16 Abs. 4,
[S11] § 34 Abs. 2.

**The floor is the operative constraint, and it is not the *Stornoabzug*.** § 169 Abs. 3 requires at
least the *Deckungskapital* that results from **spreading the charged acquisition and distribution
costs evenly over the first five contract years**, with the supervisory *Zillmer* rules unaffected
[REG-R28]. That is a floor on the **value**, not a cap on the **charge**: the DeckRV governs what the
insurer may reserve and § 169 VVG what it must pay, so a model carrying a zillmered reserve applies
both separately, the tighter binding [REG-R16] [REG-R28]. In the first five contract years of a
zillmered tariff the floor binds by a wide margin, and it is the whole reason a German surrender
value in year two is not simply zero. **The *Stornoabzug*** may then be deducted, and only if
**agreed, quantified (*beziffert*) and appropriate (*angemessen*)** — three cumulative conditions,
the burden of proof on the insurer — while **a deduction in respect of not-yet-amortised *Abschluss-
und Vertriebskosten* is void** [R1] [REG-R28]: the statutory answer to *Zillmerung*, which may not
be recovered from the surrendering policyholder as a named deduction. **Four carrier practices are
now on the record** and they do not agree: none at CosmosDirekt [S8] § 7 Abs. 10 and NÜRNBERGER
[S9] § 14 Abs. 4, both saying so expressly; a flat **250 EUR** at Zurich, waived at attained age 62
or after twenty years, plus a further 10 % of any excess of the surrender value over the death
benefit [S4] § 10 Abs. 3 and 6; and at Debeka **5 % of the *Deckungskapital*** for collectively
provided risk capital together with a 0 / 5 / 10 / 15 % element keyed to the spread between the
ten-year euro zero-coupon swap rate and its own ten-year average, **both falling linearly to nil over
the last ten years of the *Aufschubzeit*** [S11] § 34 Abs. 4–5. The GDV wording leaves the amount
blank [S1] § 12 Abs. 4. **No surrender-value table or charge-recovery schedule is published** — every
wording refers them to the *Persönlicher Vorschlag* or the *Versicherungsschein*.

### *Beitragsfreistellung* under § 165 VVG

The policyholder may **at any time, for the end of the current insurance period, demand that the
insurance be converted into a premium-free insurance, provided the agreed minimum insurance benefit
is reached** [R2] [REG-R28]; the right is statutory and unconditional apart from that threshold, and
**if the minimum is not reached the insurer must instead pay the surrender value attributable to the
insurance, including profit shares, under § 169** [R2] — a small contract cannot be made paid-up, it
is cashed out. **The premium-free benefit is calculated according to recognised principles of
actuarial mathematics, using the calculation basis of the premium calculation, on the basis of the
surrender value under § 169 paragraphs 3 to 5, and must be stated in the contract for each insurance
year** [R2]. Three consequences reach the model: the paid-up value is **derived from the surrender
value**, so a model computing them independently will not reconcile; it uses the **premium basis**,
so the paid-up contract keeps its guarantee vintage; and it is **tabulated per insurance year**.

**The difference from *Kündigung* is the point.** *Beitragsfreistellung* keeps the contract alive —
its guarantee vintage, its *Rechnungszins* and its guaranteed *Rentenfaktor* all survive on a reduced
benefit — while *Kündigung* ends it for the *Rückkaufswert* [R1] [R2]. Where an old contract carries
a high legacy *Rechnungszins*, that difference is worth a great deal, and it is why paid-up
conversion and lapse **must be separate decrements**; German lapse is in fact three-way, § 166 VVG
converting automatically to *prämienfrei* on the insurer's termination and in the § 38
premium-default case rather than ending cover [REG-R28] [REG-R30]. **The
*Mindestversicherungsleistung* is contractual and three carrier levels are established**: 25,00 € a
month at Zurich and NÜRNBERGER, 600,00 € a year for a partial surrender at CosmosDirekt [S4] [S8]
[S9]. Two carriers also **waive the *Stornoabzug* on the paid-up route** although § 165 Abs. 2 refers
to § 169 Abs. 3 **to 5** — *"Bei der Beitragsfreistellung wird kein Abzug erhoben"* [S4] § 10 Abs. 9,
and likewise [S8] § 7 Abs. 7 — which is what the model does.

---

## Riders and options

**In scope and modeled.** The ***Rentengarantiezeit*** as a selectable term in years, base 10 [R24]
[S9] [S13]; the ***Kapitalwahlrecht*** as a take-up rate at *Rentenbeginn* [S12] [R6] [R21]; the
death-benefit **form** switch across the three documented designs [S1] [R24] and the with-surplus
variant [R24]; the ***Dynamik*** as an annual increase rate, base 0 and on for one model point [S4];
***Beitragsfreistellung*** as a deterministic election with the *Mindestversicherungsleistung*
cash-out branch [R2]; and the three payout-phase *Überschussverwendung* systems [R19] [R20] [R24].

**Documented and deliberately not modeled**, each with its reason. The
***Hinterbliebenenrenten-Zusatzversicherung***, published by the GDV as a **separate model condition
set attaching to this contract** [S10] — it needs a second life and no model point carries one. The
***Berufsunfähigkeits-Zusatzversicherung***, a named section with its own conditions in the same
pack [S4] and delib's `berufsunfaehigkeit` product in standalone form. ***Zuzahlung***: **no source
in this corpus named it** (gap 15), the one option the research brief asked for that the corpus does
not support at all. ***Bonusrente*** [S4] [S15] [R24] and ***Beitragsverrechnung*** / ***Barausschüttung*** — the latter
now established, at Zurich, and restricted there to *Rückdeckungsversicherungen* [S4] § 3 Abs. 6, so
gap 16 is closed — as accumulation-phase surplus systems, and surplus **invested in an internal
fund** [S11] [S12]. The § 163 VVG
/ *Treuhänderklausel* adjustment of the guaranteed *Rentenfaktor* [R3] [R17] [REG-R27], and § 169
Abs. 6 **reduction of surrender values** [R1] — both supervised or contested channels with no
published trigger a deterministic model could key off.

---

## Variations across insurers

The corpus supports **structural** variation tables throughout. After the 2026-08-30 retrieval pass it
also supports **quantitative** statements on two of the parameters that matter most — *Rentenfaktor*
levels [R19] [R24] and declared surplus rates [S15] — while charges, entry ages, premium envelopes and
behavioural rates remain unestablished. Where a row reads "not established", that is the finding.

| Carrier | Documents | Status of the classic deferred annuity |
|---|---|---|
| GDV (industry model wording) | [S1] [S2] [S3] [S10] | Model conditions maintained, **Stand 21.07.2025** for the deferred annuity and 14.11.2019 for the survivor's-annuity rider; **expressly non-binding** — *"Diese Bedingungen sind für die Versicherer unverbindlich; ihre Verwendung ist rein fakultativ"* [S1] |
| Zurich Deutscher Herold | [S4] [S5] [S6] [S7] [S16] [S17] | *Verbraucherinformation* published in Fassung **07/2015** [S5] [S6], **01/2025** [S7] [S16] and **01/2026** [S4], on DAV 2004R at 1,25 % then 1,00 %; reported in 2016 among the carriers that had stopped **distributing** the classic product [R22]. A maintained and reissued wording, not a withdrawn one |
| CosmosDirekt (Cosmos Leben, Generali) | [S8] | AVB **LA 904 A (01.17)**; *Beitragsrückgewähr ohne Zinsen* in the *Aufschubzeit*, *Garantiesatz* 0,90 % p. a., **no *Stornoabzug***; Generali reported among those that stopped distributing [R22] |
| NÜRNBERGER | [S9] | AVB for tariff **NIR3301**, *mit Rentengarantiezeit* in the title |
| Debeka | [S11] [S12] | **Withdrawn.** Replaced from 1 July 2016 by five "Chance" variants, the safest guaranteeing **0,5 %** and the riskiest nothing [R22]. The successor is on the record as **B LV 85 (01.07.2026), Tarif CA2I**: a *garantiebasierter* and a *fondsgebundener Baustein*, guaranteed benefits on 1 % and a guaranteed *Rentenfaktor* on 0,1 % [S11] [S12] |
| Allianz | [S13] | **Withdrawn.** Replaced by KomfortDynamik: **60 %, 80 % or 90 % of the premiums paid** guaranteed at *Rentenbeginn*, selectable, 80 % standard [S13] [R22] [R23] |
| Mecklenburgische | [S14] | *Vertragsinformationen* **Version 07.2025** for *Private Rentenversicherung mit flexiblem Fondsanteil (Hybrid)*, B Privat-Rente Flex — a hybrid, not a classic chassis |
| Konzern Versicherungskammer (Bayern-Versicherung) | [S15] | *Überschussverteilung 2026*, 145 pp.: annuity *Zinsüberschussanteil* **3 % less the *Rechnungszins*** before the *Rentenbeginn* and 3,35 % during it for 2026 (2,25 % / 2,5 % for 2025); *Bewertungsreserven* allotted *zur Hälfte* |
| Stuttgarter | [S18] | *Allgemeine Informationen* pack dated 2020, for tariffs written before 2021; **Schicht 2**, a *Direktversicherung* under § 3 Nr. 63 EStG |
| DEVK | [S19] | Unit-linked only; **not retrievable** (HTTP 403), kept as a known reference |

| Design item | Observed variation | Source |
|---|---|---|
| Death benefit before *Rentenbeginn* | **None at all** unless an extension is bought — the GDV and Zurich base case; *Beitragsrückgewähr* premiums-only *ohne Zinsen*; premiums **plus attributable surplus**; the accumulated *Deckungskapital*; **the greater of contract value and refund**; or a *Hinterbliebenenrente* as a rider | [S1] § 1 Abs. 3 (left blank), [S4] § 1 Abs. 2–3, [S8] § 1 Abs. 1, [S9] § 1 Abs. 3, [S10], [R24] |
| Guaranteed *Rentenfaktor* basis | **0,1 % p. a.** on a carrier's own unisex annuity table, against a tariff *Rechnungszins* of 1 % in the same contract | [S11] § 52 Abs. 1 and § 28 Abs. 2 |
| *Rentengarantiezeit* | 5, 10, 15, 20, 25, 30+ years offered; typically 15 at retirement ages 61–70 and 10 at 71+; most choose 10–20; cost 3 € / 15 € / 46 € a month at 10 / 20 / 30 years on a 573 € base | [R24] [S9] [S13] |
| Accumulation surplus system | *Verzinsliche Ansammlung*, *Bonusrente*, internal-fund investment **and *Beitragsverrechnung* / *Barausschüttung*** all established — the last at Zurich, restricted to *Rückdeckungsversicherungen*; also *Erlebensfallbonus* and *Bonussumme* at [S15]. Gap 16 closed | [S4] § 3 Abs. 6; [S15]; [R24] [S12] |
| *Rentenfaktor* levels | 2025 market averages 24,33–27,18 guaranteed and 27,27–30,40 current by deferment term, all to age 67; 2022 current average 25,97 against 29,09 in 2021 | [R24] [R19] |
| Declared surplus rate | One carrier, 2026: total credited interest **3,00 %** before the *Rentenbeginn*, 3,35 % during it | [S15] |
| *Stornoabzug* | None at two carriers; a flat **250 EUR** at a third; **5 % of the *Deckungskapital*** plus a 0–15 % capital-market element, both tapering to nil over the last ten years, at a fourth | [S8] [S9] [S4] [S11] |
| Charge levels, issue envelopes, behavioural rates | **Not established at any carrier for any year** — every carrier refers the amounts to the *Kostenausweis* or the *Persönlicher Vorschlag*, neither public | gaps 13, 14, 20 |

**What does not vary.** Three things are the same everywhere in the corpus and all three are legal
rather than commercial facts: the **two-phase structure with a fixed *Rentenbeginn*** is definitional
[S1] [S4] [S8] [S9] [R24]; the ***Rückkaufswert*** and ***Beitragsfreistellung*** rights are
statutory and *halbzwingend*, §§ 165 to 170 VVG not being variable to the policyholder's detriment
under § 171 VVG [REG-R22] [REG-R28]; and the **unisex tariff** has been compulsory since 21 December
2012 [REG-R34], which is why sex appears nowhere in the pricing of this composite even though the
annuity tables behind it are sex-specific raw material [REG-R47] [REG-R49]. Against that, **the
composite's core is now multiply attested**: the *Rentenfaktor* comparison rule is in the AVB of
NÜRNBERGER [S9], Mecklenburgische [S14] and Stuttgarter [S18]; the conversion input including surplus
and *Bewertungsreserven*, floored at the guaranteed contract value, is [S9] § 1 Abs. 1; the
accumulation recursion is [S8] § 1 Abs. 2; and the five-year surrender floor is restated by five
carriers. What still rests thinly is the **level** side — the declared rate on one carrier's
declaration [S15], the *Rentenfaktor* range on two analyst compilations [R19] [R24], and no charge
level at all.

---
## Regulatory context

**Contract law — the VVG.** German life contract law sits in a separate statute from the prudential
one, and its **Kapitel 5 (§§ 150–171) is *halbzwingend***: §§ 152 Abs. 1 and 2, 153 to 155, 157, 158,
161 and 163 to 170 may not be varied to the policyholder's detriment under § 171 VVG [REG-R22]. That
is why a model may treat the surrender-value floor, the paid-up right and the profit-participation
entitlement as **contractual facts** rather than tariff options. The operative articles are **§ 153**
(*Überschussbeteiligung*, *Bewertungsreserven* under Abs. 3) [R4] [REG-R24]; **§§ 154 and 155** (the
*Modellrechnung*, and the annual *Standmitteilung* disclosing how much of the profit participation is
guaranteed) [REG-R25]; **§ 163** [R3] [R17] [REG-R27]; **§ 165** [R2] [REG-R28]; **§ 166** [REG-R28];
**§ 168** [REG-R28]; **§ 169** [R1] [REG-R28]; **§§ 8 and 152** (*Widerruf*) [REG-R23]; and
**§§ 150, 157, 158 and 161** on consent, age misstatement, risk increase and suicide [REG-R26]
[REG-R30]. The **§ 154 *Modellrechnung*** fixes what a published German illustration looks like:
quantified statements about benefits beyond the guaranteed ones must be accompanied by the possible
*Ablaufleistung* computed on the premium calculation bases at three rates set by § 2 Abs. 3
VVG-InfoV — the *Höchstrechnungszins* times 1,67, that rate plus one point and that rate minus one
[REG-R25] — so at 1,00 % the statutory triple is **1,67 % / 2,67 % / 0,67 %**. The reference
implementation does **not** use those rates; its declared-rate path is a [std] scenario anchored on
observed market averages, and it says so.

**Prudential — the VAG, the DeckRV and the MindZV.** BaFin supervises German life insurers under
Solvabilität II as transposed into the VAG, with no second national supervisor [REG-R21] [REG-R5]
[REG-R6]. Two ministerial regulations carry the arithmetic. The **DeckRV** fixes the
*Höchstrechnungszins* in § 2 [REG-R14] [REG-R15], the *Höchstzillmersätze* in § 4 — **25 ‰ of the
*Beitragssumme*** since 1 January 2015, 40 ‰ before, the rate at conclusion applying for the whole
term [REG-R16] — and the *Referenzzins* behind the ***Zinszusatzreserve*** in § 5 Abs. 3 [REG-R17].
The **MindZV** puts the arithmetic floor under the *Überschussbeteiligung*: **90 %** of the
investment result **less the *Rechnungszinsen***, **90 %** of the risk result and **50 %** of the
remaining result, with the *Direktgutschrift* deducted, *Alt-* and *Neubestand* separate, and a
negative minimum replaced by zero — a minimum **transfer to the RfB**, not a minimum payout [REG-R18]
[REG-R10] [REG-R19]. The **LVRG 2014** produced that shape [REG-R20]. The ***Zinszusatzreserve***
exists in no other jurisdiction in this repository and is why a book of high-vintage annuity
contracts is expensive: it arises where the § 5 Abs. 3 *Referenzzins* falls below a contract's tariff
rate, and the MindZV *Sicherungsbedarf* test compares a Bundesbank month-end swap rate with **the
highest *Rechnungszins* applicable to the contract over the next fifteen years** — a window that
"bites hardest on annuity business" [REG-R17] [REG-R18]. **delib does not compute it**; this document
cites it rather than specifying it.

**Biometric bases.** The mortality basis for every German annuity promise is **DAV 2004 R**, named in
an insurer's own AVB for exactly this product [S8]. It is a ***Generationentafel*** — a
two-dimensional basis in attained age and calendar year containing mortality by birth cohort
including the expected future change [R13] [R15] [REG-R49] — built from a second-order base table, a
first-order base table, second- and first-order mortality trends and an age adjustment
(*Altersverschiebung*) [R12], with **first-order probabilities carrying safety margins relative to
the second-order ("realistic") probabilities in order to assess the risk prudently** [R12]. It has
been in use since June 2004, was intended for new business from 2005, and the DAV **reissued its
derivation guideline on 28 June 2023** [R12] [R13] — which is itself the evidence that no successor
has displaced it, and the fact behind the longevity trigger of the § 163 VVG adjustment right. A
companion in-force table, **DAV 2004 R-Bestand**, exists for annuities already in payment [R14]
[REG-R49].

**The table is the property of the Deutsche Aktuarvereinigung, is not public and is not redistributed
by delib.** The library cites it by name and ships a [std] proxy anchored so its own worked example
reproduces exactly. A replacement must preserve three things: the **generational structure** — a
`q(x, τ)` surface, not a period table, because a period-table proxy priced at a 40-year-old's
annuitisation in 2055 understates the liability by a margin that dwarfs every other assumption in the
model [REG-R49]; the **first-order margin over second order**, which for an annuity runs in **two
dimensions**, level and trend [REG-R47] [REG-R49]; and the **age-adjustment convention** [R12]. The
free, redistributable public analogue is Destatis's *Generationensterbetafeln für Deutschland*
[REG-R52]. The tables are sex-distinct while the tariff sold since *Test-Achats* must be unisex —
C-236/09, 1 March 2011, invalidating the Article 5(2) derogation **with effect from 21 December
2012**, with § 20 Abs. 2 Satz 1 AGG repealed [REG-R34]; **neither half of that sentence was
established by any search in this product's own research** (gap 21). A model point may carry `sex`
for **decrement** purposes and **must not** let it enter the premium or the *Rentenfaktor*.

**Taxation, conduct and accounting.** The annuity is taxed on the ***Ertragsanteil*** under § 22
EStG at **18 % for age 65** [R5] [R24] [REG-R41]; the *Kapitalabfindung* falls under § 20 Abs. 1
Nr. 6 EStG and the *Halbeinkünfteverfahren* on the 12/62 rule [R6] [REG-R45]. **Not established, and
not asserted anywhere in this library**: the rate on the taxable half in the general case, the
*Solidaritätszuschlag*, the inheritance-tax treatment of the death benefit, and the
*Kleinbetragsrente* threshold (gap 23). **delib computes no tax**: every benefit cash flow is gross
of *Kapitalertragsteuer*, *Solidaritätszuschlag* and *Kirchensteuer* [REG-R38]. The pre-contractual
pack — *Verbraucherinformation* [S4]–[S7], *Vertragsinformationen* [S14], *Kundeninformation* [S19],
*Allgemeine Informationen* [S18] — is one object under §§ 6, 7 and 7a–7c VVG with the VVG-InfoV
[REG-R31]; distribution sits under the IDD and § 34d GewO [REG-R33]; BaFin's *Merkblatt 01/2023* on
*Wohlverhaltensaufsicht* governs product governance and value for money [REG-R35]. The statutory
balance sheet is the HGB one of §§ 341–341o HGB with the RechVersV and BerVersV [REG-R54], and its
*Deckungsrückstellung* is **not** the Solvency II best estimate — an insurer carries two liability
measures, and the *Überschussbeteiligung*, the *Zinszusatzreserve* and the *Bewertungsreserven* test
all run on the **HGB** side [REG-R14] [REG-R54]. IFRS 17 would measure this contract under the
variable fee approach [REG-R55]; actuarial work sits under the DAV *Fachgrundsätze* and the § 141 VAG
*Verantwortlicher Aktuar*, a role the MaGo keeps distinct from the *versicherungsmathematische
Funktion* [REG-R56] [REG-R11] [REG-R21]; policyholder protection in a failure runs through
**Protektor** under §§ 221–236 VAG [REG-R12].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-klassische_rentenversicherung-r1
[R10]: #delib-klassische_rentenversicherung-r10
[R11]: #delib-klassische_rentenversicherung-r11
[R12]: #delib-klassische_rentenversicherung-r12
[R13]: #delib-klassische_rentenversicherung-r13
[R14]: #delib-klassische_rentenversicherung-r14
[R15]: #delib-klassische_rentenversicherung-r15
[R16]: #delib-klassische_rentenversicherung-r16
[R17]: #delib-klassische_rentenversicherung-r17
[R18]: #delib-klassische_rentenversicherung-r18
[R19]: #delib-klassische_rentenversicherung-r19
[R2]: #delib-klassische_rentenversicherung-r2
[R20]: #delib-klassische_rentenversicherung-r20
[R21]: #delib-klassische_rentenversicherung-r21
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
[REG-R10]: #delib-reg-r10
[REG-R11]: #delib-reg-r11
[REG-R12]: #delib-reg-r12
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R20]: #delib-reg-r20
[REG-R21]: #delib-reg-r21
[REG-R22]: #delib-reg-r22
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R25]: #delib-reg-r25
[REG-R26]: #delib-reg-r26
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R30]: #delib-reg-r30
[REG-R31]: #delib-reg-r31
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R38]: #delib-reg-r38
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R47]: #delib-reg-r47
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R52]: #delib-reg-r52
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R56]: #delib-reg-r56
[REG-R6]: #delib-reg-r6
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
