# Product Specification

**Status:** Draft, 2026-08-29; citations re-verified against the primary documents 2026-08-30.

**Scope note.** This is a *standardized composite specification* assembled for reference liability
cash-flow modeling of the German **kapitalbildende Lebensversicherung** — the classic endowment, the
*gemischte Versicherung auf den Todes- und Erlebensfall*, which pays a guaranteed
*Erlebensfallleistung* at the *Ablauf* (maturity) if the *versicherte Person* is then alive and a
*Todesfallleistung* if she dies before it, both increased by the *Überschussbeteiligung*. **It
describes no single insurer's contract.** Source tags — [S#] (primary product documents: AVB,
*Basisinformationsblatt*, *Standmitteilung*, insurer product pages) and [R#] (product-specific
regulatory and actuarial references), both numbered per `_research/kapitallebensversicherung.md` and
resolved in `sources.md`, numbering frozen; and [REG-R#] (the cross-product library
`references/regulatory-and-actuarial-references.md`, whose R1–R56 numbering is separate and also
frozen) — name the instrument a claim should be checked against. **[std]** marks a standardization
introduced for the reference implementation, each with a numbered footnote giving the rationale and,
where one was established, the observed range; [unverified] marks a claim no search corroborated.

**Read this before relying on a citation.** delib was **drafted** under an organisation network
policy that blocked all direct HTTP egress from the build environment — `gesetze-im-internet.de`,
`bafin.de`, `gdv.de`, `aktuar.de`, `dejure.org` and `de.wikipedia.org` were tried and refused — so no
document was retrieved and the first draft rested on `WebSearch` result summaries, a budget exhausted
after twenty-four searches on this product, and on the authoring model's own knowledge of German
insurance law and practice, disciplined by the [std] and [unverified] tags. **That policy has since
been lifted and the citations re-verified against the primary documents.** For this product,
**forty-five of the forty-seven entries in `sources.md` now rest on a document that was opened and
read — 96 %**: the statutory core as canonical XML from `gesetze-im-internet.de` with each
instrument's amendment status (`Stand`) recorded, and the carrier material as PDF, six
*Bedingungswerke* among it. **Two entries were not retrieved at all** — [S8], HTTP 404 at the cited
die Bayerische URL, and [R24], a rechtsportal.de report of the older BGH line answering HTTP 429 —
and several more were retrieved only in part; every entry says which it is. **Where an entry says
`Retrieved: yes`, treat the claim it carries as sound; where it does not, the citation is still a
pointer, not a certificate** — it names the instrument a claim should be checked against and does not
assert that anyone checked it. Re-verification also changed this document: it corrected the surplus
base read from Debeka [S3], the Debeka edition dates, the *Standmitteilung* field list [S2] and the
lapse figures [R20], and each correction is marked where it stands. What it did not change is the
thinness of the insurer-by-insurer parameter sweep — of twenty-six named carriers, seven produced a
document and **three** produced quantified terms. Where a level could not be established it is a
**[std]** parameter with a stated rationale rather than a citation, because a `[std]` number is
honest and a wrong `[S#]` number is not.

**Composite base.** The seven carriers that produced a document are set out in *Variations across
insurers* below: Debeka [S3] [S4] [S5] [S6], Gothaer [S7], die Bayerische [S8] [S9], VPV [S18],
Allianz [S11], ERGO [S12] and ÖSA [S10]. **Only two of those documents are endowment wordings** —
Gothaer's, of 2011, and VPV's, of 2019; the three Debeka *Bedingungswerke* and both die Bayerische
editions are annuity wordings, used only where the rule transfers, which is said wherever a fact is
taken from them. The GDV *Musterbedingungen* [S1] and *Muster-Standmitteilung* [S2] are the market
template, and the GDV states its model conditions are *unverbindlich* and their use purely optional,
so an S1-tagged fact is weaker evidence about a carrier than the same fact from that carrier's own
AVB. Consumer material [S13] [S15] [S16] is context. *Betriebliche Altersversorgung*,
*Gruppenversicherung*, *Sterbegeldversicherung* and *private Krankenversicherung* are outside the
delib library entirely.

---

## Product overview and market role

A German *Kapitallebensversicherung* is **life assurance in Sparte 19 (Leben)** of Anlage 1 to the
VAG [REG-R5], written as an individual contract on a single life against an individual
*Versicherungsschein* — every carrier document located is such a contract, with no subscribing
association anywhere in the chain [S3] [S4] [S5] [S7] [S8], a structural difference from the French
corpus where five of eight carriers used a *contrat de groupe à adhésion facultative*. The
supervisor's own one-sentence definition is that the product "combines a *Risikolebensversicherung*,
which pays on death, with a savings process whose proceeds are paid with interest at the end of the
contract" [R18-family]; Allianz gives the same structure from the manufacturer's side, as "a
guaranteed interest rate, a savings component and death cover in one product" [S11]. Four features
make the German chassis what it is, and each changes the shape of the projected cash flows.

1. **Participation is the default and it is all-or-nothing.** § 153 Abs. 1 VVG entitles the
   policyholder to a share in the surplus **and** in the *Bewertungsreserven* unless participation is
   excluded by express agreement, and such an exclusion can only be made for the whole of it [R1]
   [REG-R24]. There is no partially participating German endowment, and every carrier document located
   is participating [S3] [S7] [S9] [S11].
2. **The surplus is declared as a percentage of the contract's own reserve.** Four retrieved
   wordings agree on the base. Gothaer: "Es werden Jahresanteile zugewiesen. Diese bestehen aus einem
   Risikoanteil in Promille der Versicherungssumme und in Prozent des Risikobeitrags sowie einem
   Ertragsanteil in Prozent des maßgeblichen Deckungskapitals" [S7]. VPV, more precisely still: "Das
   um ein Jahr mit dem Rechnungszins abgezinste Deckungskapital wird mit dem deklarierten
   Zinsüberschussanteilsatz multipliziert" [S18]. Die Bayerische books its *Zinsüberschussanteile* at
   each *Bilanztermin*, being 31 December, **into** the *Deckungskapital* [S9], and Debeka declares in
   percent of the reserve for its annuity chassis too [S3] — so the reserve is both the base of the
   declaration and its destination. This is the single most useful mechanical fact in the corpus.
3. **The reserve is normally *gezillmert*, so it is negative in the early years.** *Zillmerung*
   reduces the *Deckungskapital* by the present value of the acquisition costs not yet recovered, and
   § 4 DeckRV caps the *Zillmersatz* at **25 ‰ — 2,5 % — of the *Beitragssumme***, cut from 40 ‰ by
   the LVRG with effect from 1 January 2015 [R7] [R28] [S15] [REG-R16] [REG-R20]. That negative early
   reserve is why § 169 Abs. 3 VVG needs a *Mindestrückkaufswert* [R2].
4. **The guarantee travels with the contract, not with the calendar.** The *Rechnungszins* is fixed
   at conclusion and stays with the contract for its whole term [REG-R14], so a German endowment
   book is a stack of cohorts running from **4,00 %** (July 1994 to June 2000) down to **0,25 %**
   (2022 to 2024) and back up to **1,00 %** from 1 January 2025 — the first increase in about thirty
   years [REG-R15] [R7] [R15]. The *Sicherungsbedarf* machinery of § 139 VAG exists because of the
   top of that range [R8] [REG-R9], and the *Zinszusatzreserve* for the same reason [REG-R17].

**Market role: a large in-force book with a thin new-business layer.** Allianz says of its own
historic flagship that it "is rarely newly concluded today, because modern annuity insurance typically
offers better flexibility and earnings opportunities" [S11]; the trade characterisation for 2026 is
*"Klassik wird zur Nische"* [R26]; and Assekurata reports business shifting to capital-market-linked
products with fewer guarantees even as surplus participation edges
up [R25]. **No quantification of the shift was established**: GDV publishes new-business
*Beitragssumme* and Annual Premium Equivalent series [R21], but no endowment-specific figure and no
time series showing the effect of the 1 January 2005 *Alterseinkünftegesetz* boundary, so the
market-role argument here is qualitative and is labelled as such. For scale, 2024 German life premium
income on the GDV basis was **+2,8 % to 94,6 Mrd €**, *laufende Beiträge* **66,3 Mrd €** roughly flat,
*Einmalbeitragsgeschäft* about **+10 % to 28 Mrd €** and the contract count **−1,4 % to 80,3 Mio**;
the GDV taxonomy's *Kapitalversicherungen* line is this product, and the BaFin basis gives
life-segment *verdiente Bruttobeiträge* of **90,4 Mrd €** for the same year on a different population,
so the two must never appear in the same table [REG-R53]. Lapse: the GDV publishes one headline
figure, and the retrieved 2024 annual reports it for the **2023** year — "Die Stornoquote (Anzahl)
stieg im Jahr 2023 leicht auf **2,56 %** (Vorjahr: 2,51 %)" [R20]. It is a **count** measure over all
life business, not endowment-specific and not split by duration, so it is a market-level indicator
and not a surrender decrement. The figures previously recorded here — 2,72 % for 2024 and a second
count measure of 1,2 % — are **not in the retrieved publication** and are withdrawn. The supervisory
observation that matters more for this product is BaFin's: some products show "sehr hohen
Stornoquoten ... speziell in den ersten Jahren nach Vertragsabschluss, in denen ein großer Teil der
Kosten anfällt", which BaFin treats as evidence of an inadequate *Kundennutzen* [R18].

Retrieval also supplies the endowment-specific market figures this section previously lacked. At
31 December 2023 the *Kapitalversicherungen (klassisch)* line held **15,7 %** of the in-force book by
annual premium, down from 17,0 %; new regular-premium business in 2023 was **158 Mio €**, a 3,9 %
share; and the count of newly issued classic endowments fell from **1.954,9 thousand (26,8 % of all
new business) in 2000** to 1.354,2 (18,5 %) in 2005, 742,1 (12,1 %) in 2010, 527,2 (10,3 %) in 2015,
392,3 (8,4 %) in 2020 and **325,3 (7,4 %) in 2023** [R20]. That series is the quantitative form of
the qualitative market-role argument: a large in-force book with a thin and still-thinning
new-business layer.

**The charge level is a supervised parameter, not a free one.** BaFin's *Merkblatt 01/2023 (VA)*
requires an appropriate *Kundennutzen* and undertakes to examine closely any undertaking whose
*Effektivkosten* or *Aufwendungen für Versicherungsvermittler* are notably high against industry
norms [R17] [REG-R35], and "Kosten von kapitalbildenden Lebensversicherungen" is a named focus risk
in BaFin's 2026 risk agenda three years later [R18]. **No numerical threshold was established** — not
for *Effektivkosten*, not for commission, not for the required real return — so no figure is
attributed to the *Merkblatt* anywhere in delib, and **every charge level here is [std]**.

---

## Representative specification

The representative design is a single-life, individual, participating endowment with **equal death
and survival sums**, a **level annual *Beitrag* over the full term**, priced and reserved at the
**1,00 % *Höchstrechnungszins*** on a **DAV 2008 T-shaped, medically underwritten** basis,
**gezillmert to the 25 ‰ ceiling**, surplus declared **annually as a percentage of the
*Deckungskapital* at the balance date** and applied by ***verzinsliche Ansammlung***, a **surrender
value equal to the *gezillmert* prospective reserve floored by the five-year-spread
*Mindestrückkaufswert*** less a **pre-declared *Stornoabzug***, a **contractually tabulated
*beitragsfreie Versicherungssumme*** subject to a *Mindestversicherungsleistung* test, and a
**three-year *Selbsttötung* window paying the *Rückkaufswert***. Every choice the corpus does not
source carries a **[std]** tag with the observed range beside it.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | *Gemischte Versicherung auf den Todes- und Erlebensfall*; Sparte 19 (Leben); *überschussberechtigt*; *Neubestand* | [S3] [S7] [S11]; [REG-R5]; [R1]; [REG-R11] |
| Legal wrapper | Individual contract on a single life against an individual *Versicherungsschein*; document pair *Bedingungen* + *Verbraucherinformationen*, with an IPID and a PRIIP-*Basisinformationsblatt* alongside | [S3] [S4] [S5] [S7] [S8]; [S18]; [S6] [S10] [R19] |
| Benefit form (model-point parameter) | `death_ratio` = *Todesfallleistung* ÷ *Erlebensfallleistung*; 1.00 for the endowment proper, lower for a savings-dominant design | 1.00 [S3] [S7] [S11]; ratio as a parameter **[std]** (1) |
| Premium form (model-point parameter) | (i) `prem_term = policy_term` — level *Beitrag* over the whole term; (ii) `prem_term < policy_term` — *abgekürzte Beitragszahlungsdauer*; (iii) `prem_term = 1` — *Einmalbeitrag* | form (i)–(ii) [S3] [R28-family]; the single-premium point **[std]** (2) |
| Lives basis, entry age | Single life — no joint-life basis appears in any located German endowment wording; entry age 25 to 60, an envelope chosen so a 25-year contract issued at the top still matures before age 90 and one at the bottom after the age-62 tax threshold | [S3] [S4] [S5] [S7] [S8]; entry age **not established** for any carrier, envelope **[std]** |
| *Versicherungsdauer* | 12 to 40 years; the composite runs 25 years | tax minimum 12 [R10] [REG-R45]; 20–40 as sold and a 25–35 maximum, both from one fused consumer summary [S11] [S12] [S13] [S15] group; term choice **[std]** (3) |
| *Versicherungssumme* | 50,000 EUR | **not established**; observed minima 2,500 / 5,000 EUR from the same fused summary and probably belonging to a different product; level **[std]** (4) |
| *Rechnungszins* | 1.00% for new business written from 1 January 2025; the model point carries its own cohort's rate | [R7] [R15] [REG-R14] [REG-R15] |
| *Zillmerung* | On, at the 25 ‰ ceiling; the ceiling is a maximum, not a mandate, so a lower or nil *Zillmersatz* is open to a carrier | [R7] [S15] [REG-R16]; **no carrier pair evidences it** — the two [S9] editions are the same tariff two years apart and both are zillmered, so `zillmer_on` = 0 is **[std]** |
| *Überschussverwendung* | *Verzinsliche Ansammlung*; *Bonussystem* and *Beitragsverrechnung* carried as variants | system choice **[std]** (5); the four named systems [R28] [S15] |
| Age basis, sex, *Wartezeit* | Age last birthday at issue, stepping at the policy anniversary **[std]** (6); sex carried for decrements only, since **sex may not enter the premium** — unisex since 21 December 2012; no *Wartezeit* **[std]** (7) | age basis and *Wartezeit* **[std]**; unisex [REG-R34] |
| Anchor model cell | Male 37, *Versicherungsdauer* 25 years, *Beitragszahlungsdauer* 25 years, *Versicherungssumme* 50,000 EUR, `death_ratio` 1.00, annual mode, *Rechnungszins* 1.00%, *gezillmert*, *verzinsliche Ansammlung*, new business | **[std]** (8) |

Footnotes to **[std]** rows:

1. Tax law forces a floor on the death sum but not equality. § 20 Abs. 1 Nr. 6 Satz 6 EStG, read in
   the statute for this pass, disapplies the half-income rule where **both** of two limbs hold: (a)
   in a contract "mit vereinbarter laufender Beitragszahlung in mindestens gleichbleibender Höhe" the
   benefit on the insured event is **less than 50 % of the sum of the premiums payable over the whole
   term** — the *Mindesttodesfallschutz*, or "50 %-Regel"; and (b) that benefit fails, **at the latest
   five years after conclusion**, to exceed the *Deckungskapital* or *Zeitwert* by at least **10 %** of
   the *Deckungskapital*, the *Zeitwert* or the premiums paid [R12] [REG-R45]. § 52 Abs. 28 Satz 8
   applies the provision to contracts concluded after **31 March 2009** or whose first premium was
   paid after that date. Equal sums satisfy limb (a) comfortably at any realistic charge level; a
   savings-dominant design does not. The ratio is therefore a parameter with the floor as a design
   constraint on every model point, one point being written at `death_ratio = 0.60` to exercise it.
   **The tag on the second limb is discharged**: its base is any of the three named, its time
   profile is "spätestens fünf Jahre nach Vertragsabschluss", and the trailing words that would not
   parse are its own second sentence — "Dieser Prozentsatz darf bis zum Ende der Vertragslaufzeit in
   jährlich gleichen Schritten auf Null sinken." The model still checks limb (a) only, at model-point
   build time; limb (b) needs a reserve projection at contract design time and is out of scope.
2. **No source states the range of abbreviated-payment options offered**, so the
   *Beitragszahlungsdauer* is a free model-point parameter. The single-premium point is included
   because *Einmalbeitragsgeschäft* is now roughly 30 % of German life premium income and growing an
   order of magnitude faster than regular premium [REG-R53]; this corpus says nothing about
   single-premium endowment specifically.
3. The corpus contradicts itself: a "minimum term" of 12 years and one of 3 to 5 years both appear in
   the same fused summary, together with the 2,500 / 5,000 EUR minimum sums [S11] [S12] [S13] [S15]
   group, and the second set most likely belongs to a *Sterbegeldversicherung* or a short savings
   contract the same search matched. The honest reading is that the corpus supports **a long-term
   contract of the order of two to three decades and nothing finer**; twelve years is a hard floor
   because it is the condition of the half-income tax rule [R10] [REG-R45].
4. See footnote 3 on the provenance of the observed minima. **No maximum *Versicherungssumme* and no
   premium level of any kind was established.** 50,000 EUR is a round mid-market figure chosen so the
   *Beitragssumme* over 25 years is of the order of the sum insured, which makes both the
   *Mindesttodesfallschutz* test [R12] and the *Zillmerung* visibly material.
5. Four systems are named, and the corpus says that as a rule "either the *verzinsliche Ansammlung* or
   the *Bonussystem*" applies, **without saying which is more common** [R28]; the fourth,
   ***Anlage in Fondsanteilen***, is named by no source and stays [unverified]. Retrieval names all
   four in a carrier's own wording — Gothaer offers *Verzinsliche Ansammlung*, *Barauszahlung*,
   *Gewinnsystem BE* and *Gewinnsystem BS* [S7] — and VPV accumulates with interest as its stated form
   [S18], which is why *verzinsliche Ansammlung* is the base case. **Any statement that one system is
   "the market default" would still be [unverified]**: two wordings are not a market.
6. **No German endowment wording located states an age basis.** Age last birthday is the ordinary
   German convention, adopted without a citation; the alternative worth naming is
   *versicherungstechnisches Alter*. The choice moves the first-year risk premium by up to one year
   of mortality and nothing else; the attained age steps at the anniversary whatever the projection
   step, so a monthly grid does not refine it.
7. **Nothing in the corpus establishes a waiting period for an underwritten German endowment**; German
   *Wartezeit* constructions belong to *Sterbegeldversicherung* and simplified-issue covers. The only
   period that operates like one is the **three-year *Selbsttötung* window** of § 161 VVG [R4]
   [REG-R26], a benefit substitution rather than an exclusion.
8. Issue age 37 with a 25-year term makes the *Ablauf* fall at attained age **62** — the age the
   half-income tax rule requires for contracts concluded after 31 December 2011 [R10] [REG-R45] — and
   comfortably exceeds the twelve-year minimum, so the anchor is a contract a German buyer would
   actually have been sold; and twenty-five rows is a projection a reader can check by hand.


### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| *Bruttobeitrag* | Level over the *Beitragszahlungsdauer*, computed by the model's own equivalence principle on the first-order basis. **No German premium rate table, gross premium scale or tariff grid was located for any carrier** | mechanics [S3] [R28-family]; every premium level **[std]** (9) |
| Premium decomposition | *Sparanteil* + *Risikoanteil* + *Kostenanteil*, the *Risikoanteil* depending on age, health, smoking and dangerous hobbies | [S11] [S12] [S13] [S15] group |
| *Beitragssumme* | Total of all premiums payable over the agreed term = annual *Bruttobeitrag* × *Beitragszahlungsdauer*, before any *Ratenzahlungszuschlag*. Whether the base is measured before or after that loading **was not established**; before gives the smaller cap and is adopted | reference base for the acquisition-cost cap [R7] [S15] and the tax test [R12]; measurement **[std]** |
| Payment frequency | Annual, half-yearly, quarterly, monthly | [S11] [S12] [S13] [S15] group |
| *Ratenzahlungszuschlag* | 2% half-yearly, 3% quarterly, 5% monthly, applied **only** to *unechte unterjährige Beiträge* | market levels [R28]; the *echt*/*unecht* gate [R28]; the single value chosen **[std]** (10) |
| Premium cessation | On death, on *Beitragsfreistellung*, and at the end of the *Beitragszahlungsdauer* | death [S7]; paid-up [R3] [REG-R28] |
| Repricing | The *Bruttobeitrag* of a *kapitalbildende* contract is **not** treated as adjustable in this model. § 163 VVG's adjustment power exists, and whether it reaches *kapitalbildende* premiums in practice or is effectively confined to biometric covers **was not settled** | [REG-R27]; treatment **[std]** (11) |
| *Zahlbeitrag* under *Beitragsverrechnung* | The declared surplus is set off against the premium, so the policyholder pays only part of it. **The *Zahlbeitrag* is not guaranteed** | mechanics [R28]; the guarantee point [REG-R53] [REG-R27] |

9. **This is the sharpest contrast with the frlib corpus**, which had one published attained-age rate
    card for its comparable product. Delib has none: not one German endowment premium rate table,
    underwriting grid or *Risikozuschlag* scale is public, for any carrier. Every premium here is
    computed by the model's own equivalence principle on **[std]** first-order bases, and **no delib
    premium reproduces a published figure**; the pricing equation is in `technical-notes.md`.
10. The three loadings are the customary market levels reported for German life business generally
    [R28]; **no carrier document in this corpus publishes its own scale**, so they are a cited market
    range and any single value chosen is **[std]**. The ***echte* / *unechte* distinction is
    load-bearing**: a contract providing for sub-annual premiums **from the outset** carries **no**
    loading, which attaches only where an annual contract is paid in instalments [R28]. A model
    applying a frequency loading to a genuinely monthly contract is wrong, so the form is a
    model-point column and both are exercised.
11. § 163 VVG permits an adjustment on three cumulative conditions and expressly excludes one to the
    extent the benefits were insufficiently calculated originally [REG-R27]. The implementation treats
    the *Bruttobeitrag* as level and guaranteed and says so; a model point running *Beitragsverrechnung*
    carries a *Zahlbeitrag* below it, and that gap is a discretionary surplus rebate withdrawable
    without invoking § 163 at all [REG-R53].


### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| *Erlebensfallleistung* | The agreed *Versicherungssumme* at the *Ablauftermin* named in the *Versicherungsschein*, **plus** the accumulated *Überschussbeteiligung*; the contract ends with the payment | [S7] § 3 I (3); [S1] § 1 (1); surplus [R1]; reported as a guaranteed part plus a *Schlussüberschuss* and a *Bewertungsreserven* share on the annual *Standmitteilung* [S2] [REG-R25] |
| *Todesfallleistung* | The agreed death sum on death before the *Ablauf*, **plus** the accumulated *Überschussbeteiligung*; the contract ends with the payment, so no further premium falls due | [S7] § 3 I (5); [S1] § 1 (1); [S11]. **Premium cessation is expressly stipulated only in the *Termfixversicherung*** — "Bei Tod der versicherten Person vor dem Ablauftermin werden keine Beiträge mehr fällig" [S7] § 3 II — where the benefit falls due at the fixed date irrespective of survival and the contract does not end on death |
| *Schlussüberschussanteil* | Accrued over the term and paid at the *Ablauf*; treated as payable on death and **not** on surrender in the base run | mechanism [S16] [S3]; **no rate of any kind was established** — level and payability **[std]** (12) |
| *Beteiligung an den Bewertungsreserven* | On termination, half of the amount then determined, allocated by a causation-oriented procedure — **but only to the extent the *Bewertungsreserven* exceed the *Sicherungsbedarf*** from contracts with an interest guarantee | [R1] [R8] [REG-R24] [REG-R9]; **set to zero in the base run** **[std]** (13) |
| *Selbsttötung* | The insurer is *leistungsfrei* where the *versicherte Person* intentionally takes her own life **within three years of conclusion**, unless the act was done in a state excluding free determination of the will caused by a *krankhafte Störung der Geistestätigkeit*; the period may be **extended** by agreement. **The insurer must nevertheless pay the *Rückkaufswert* including *Überschussanteile* under § 169** | [R4] [REG-R26] |
| Acceleration benefit | **None in the base product.** Nothing in the corpus describes a terminal-illness or disability acceleration as a standard feature; the German market attaches a *Berufsunfähigkeits-Zusatzversicherung* as a separate rider, and § 165 VVG's practical note records that such riders are **regularly lost on *Beitragsfreistellung*** [R3] | scope **[std]** |
| Payout alternatives | A *Kapitalwahlrecht* / annuitisation option at the *Ablauf* is a live German feature. **No located endowment wording sets out one**, and no *Rentenfaktor* for an endowment was established | **not modeled**; the annuity chassis is `products/klassische_rentenversicherung/` |

12. **No *Schlussüberschuss* rate of any kind was established** — for any insurer, in any year. The
    corpus establishes what a *Schlussüberschussanteil* is, that it is declared as a percentage of the
    *Deckungskapital* at the allocation date, and that the *Gesamtverzinsung* is the *laufende
    Verzinsung* plus the terminal component [S3] [S16], but **not one number**. The implementation
    accrues a **[std]** terminal rate on the *Deckungskapital* and pays it at maturity and on death,
    and **any *Gesamtverzinsung* printed anywhere in this library is a construction, not a citation**.
    That the terminal share is **not** paid on surrender is likewise **[std]**: the corpus says it is
    allocated at the *Ablauf* "or on some earlier exits" [S16] without saying which, and paying
    nothing is the choice that does not invent an entitlement.
13. The mechanism is established in full and **the amount is not established at all** — not for any
    year, by any insurer [R1] [R8] [R23] [REG-R9] [REG-R24]. In the sustained low-rate environment the
    *Sicherungsbedarf* routinely exhausted the *Bewertungsreserven*, so the exit half share has often
    been nil: on a 3,25 % or 4,00 % *Höchstrechnungszins* it has for most of the last decade exceeded
    the fixed-income valuation reserves outright [REG-R9]. The base run sets the participation to
    **zero**, exposes it as a parameter, and says exactly this. Retrieval narrows the statutory rule:
    § 139 Abs. 3 VAG cuts back only the reserves "aus ... festverzinslichen Anlagen und
    Zinsabsicherungsgeschäften", not the whole of the *Bewertungsreserven* [R8]. The ***Sockelbetrag***
    is **no longer an open question**: three independent retrieved documents carry it — the GDV model
    *Standmitteilung*'s "Sockelbeteiligung an Bewertungsreserven" [S2], die Bayerische's
    *Mindestbeteiligung* [S9], and VPV's "Sie erhalten jedoch einen Mindestwert als Beteiligung an den
    Bewertungsreserven. Diese Mindestbeteiligung an den Bewertungsreserven wird als zusätzlicher
    Schlussgewinn festgelegt" [S18]. It is contractual and declaratory, not statutory; **its size is
    still unobserved**, and all three documents say it can fall away.


### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| *Gesundheitsprüfung* | Retained. § 19 Abs. 1 Satz 1 VVG obliges the applicant to disclose the *gefahrerhebliche Umstände* known to her **that the insurer has asked about in *Textform*** — a question-bounded duty; the provision gives the insurer the right to put health questions and to accept with restrictions or only at an increased premium | [R5] [REG-R30] |
| Rating factors and the *Risikozuschlag* | Age, health status, smoking, dangerous hobbies, smoker differentiation being supported at table level by DAV 2008 T R / NR; carried as `rating_factor`, a multiplier on the risk premium, 1.00 at standard rates. **No German carrier publishes a *Risikozuschlag* scale** | [S11] [S12] [S13] [S15] group; [R14] [REG-R48]; mechanics [R5]; level **[std]** (14) |
| Sex | **Not a rating factor.** Unisex since 21 December 2012; § 20 Abs. 2 Satz 1 AGG, which allowed sex-differentiated pricing on actuarial data, was repealed | [REG-R34] |
| Underwriting is a precondition of the table | DAV 2008 T R and NR are **not suitable for policies written without a *Gesundheitsprüfung*** — a simplified- or guaranteed-issue endowment would need a different basis | [R14] |
| Breach of the *vorvertragliche Anzeigepflicht* | The insurer may adjust the contract retrospectively — excluding the undisclosed risk or raising the premium by a *Risikozuschlag* — instead of refusing to perform; for negligent breach this is the usual outcome. The rights lapse **five years** after conclusion for negligence and **ten years** for intentional or *arglistig* breach | [R5] [REG-R30] |
| Underwriting thresholds | **No age/amount grid was established for any German carrier** | **not modeled** |

14. The blank here is the same one frlib found for France and it has the same cause: the grids are
    not public, and retrieving every source in the corpus did not produce one. `rating_factor` is
    therefore a pure model-point input, exercised on one model point at 1.50 and left at 1.00
    elsewhere. The statutory hook for it is § 19 Abs. 4 Satz 2 VVG, under which the *anderen
    Bedingungen* — an exclusion or a *Risikozuschlag* — become part of the contract retrospectively
    on the insurer's demand, with § 19 Abs. 6 giving the policyholder an immediate right to cancel
    if the change raises the premium by more than **10 Prozent** [R5].

### Charges

| Parameter | Representative value | Basis |
|---|---|---|
| *Abschluss- und Vertriebskosten*, zillmered | 25 ‰ of the *Beitragssumme* — the statutory ceiling, used as the composite's level | ceiling [R7] [S15] [REG-R16]; the choice to sit at the ceiling **[std]** (15) |
| *Höchstzillmersatz* | May not exceed **25 ‰ (2,5 %)** of the *Beitragssumme*, cut from **40 ‰** by the LVRG with effect from 1 January 2015; the rate an undertaking uses at conclusion applies for the whole term, so a pre-2015 contract keeps its 40 ‰ basis | [R7] [S15] [REG-R16] [REG-R20] |
| *Verwaltungskosten* | 3.0% of the *Bruttobeitrag* over the *Beitragszahlungsdauer*, plus 1.5 ‰ of the *Versicherungssumme* p.a. over the whole *Versicherungsdauer* | premium-proportional form established as "a percentage of the ongoing premium" [R28], level **[std]** (16); the sum-proportional form **not established** — gap 17; **[std]** (17) |
| Commission | Initial 25 ‰ of the *Beitragssumme* at conclusion; renewal (*Bestandsprovision*) 1.5% of the *Bruttobeitrag* from year 2 | initial set at the statutory *zillmering* ceiling [R7], which is **not** a commission cap — "Eine Deckelung der Provisionen ist gesetzlich nicht vorgesehen" [R29]; the *Abschluss-/Bestandsprovision* trade-off named at ERGO [R29]; levels **[std]** (18) |
| Insurer expenses | Acquisition 300 EUR per policy at issue over and above commission; maintenance 45 EUR p.a. inflating at 1.8% p.a.; claim expense 120 EUR per death, maturity or surrender claim | **[std]** (18) |
| *Stornoabzug* | A pre-declared schedule falling from 10% of the *Deckungskapital* in years 1–5 to 2.5% from year 16 | one of **three observed shapes**, none of them this one: 5 % of the *Deckungskapital* plus 0/5/10/15 % by *Kapitalmarktsituation*, both decaying linearly to nil over the last ten years [S3] [R30]; 50 € + 0,15 % of premiums paid × years remaining [S9]; 100 € + 0,2 % of (*Versicherungssumme* − *Rückkaufswert*) [S18]; schedule **[std]** (19) |
| *Effektivkosten* | Disclosed, not modeled. **No supervisory threshold exists**; the two observed values are BaFin's finding that in individual cases 2021 new business carried *Effektivkosten* "über vier Prozent" [R18] and the ÖSA BIB's own 5,3 % annual cost impact at twenty years [S10] | [R9] [R17] [R18] [S10] [REG-R31]; treatment **[std]** (20) |

15. Sitting the composite at the statutory ceiling is deliberate: it makes the *Zillmerung* mechanics
    maximally visible, makes the § 169 Abs. 3 floor bite where a real contract's would, and is the one
    acquisition-cost level in the corpus with a citation behind it — as a **ceiling**, not an observed
    level. **No actual acquisition-cost level was established for any German carrier.** The market data
    are that *Abschlusskosten* fell by **7,9 %** after the LVRG, on the Procontra *LV-Check* of
    insurer balance sheets reported in July 2016, against a *Beitragssumme des Neuzugangs* down only
    5,7 % over the same period, so the fall is not a volume effect [R29]. **No named carrier's
    commission rate is established anywhere in this corpus**: the only carrier named in the retrieved
    LVRG reporting is ERGO, and only qualitatively — a stepwise shift under which "eine höhere
    Bestandsprovision dann eine geringere Abschlussprovision ausgleicht" [R29].
16. The corpus establishes exactly one administration-cost form: "it is customary in life insurance
    that ongoing costs are charged annually as a percentage of the ongoing premium and/or as a
    percentage of the *Vertragsguthaben*" [R28]. The **level** is not established, for any carrier.
17. **The sum-insured form was not confirmed by any search result** — gap 17. The composite uses a
    per-mille-of-*Versicherungssumme* charge anyway, for a reason worth stating rather than hiding: the
    *Vertragsguthaben* **is negative in the early years on a *gezillmert* contract**, and a percentage
    of a negative fund is a negative charge. A sum-insured base is the smallest departure from the
    sourced forms that is well defined at every duration.
18. **No carrier charge level is established** — not one *Abschluss-* or *Verwaltungskostenquote*,
    and **no commission rate at all** (gap 7). The single product-level cost disclosure now in the
    corpus is the ÖSA *Basisinformationsblatt* [S10], whose model case (47-year-old, 1.000 € annual
    premium, 20 years) shows total costs of **6.216 €**, an annual cost impact of **5,3 %**, entry
    costs of 2,2 % and ongoing administration of 28,5 % "der Summe aller Anlagebeträge", and a return
    of "2,4 % vor Kosten und -2,9 % nach Kosten" — one product of one public-sector insurer, far too
    narrow to calibrate against but enough to show the order of magnitude BaFin is exercised about.
    The market aggregate that exists is a *Verwaltungskostenquote* of
    **2,4 %** on one 2024 measurement and **2,19 %** on another, spread from under 2 % to over 4 %
    [REG-R53] — a whole-book ratio, not a tariff parameter. The levels above are placeholders sized so
    the first-year acquisition outgo (300 EUR plus 25 ‰ of the *Beitragssumme*) modestly exceeds what
    the *Zillmerung* recovers, producing the new-business strain a real German endowment carries.
19. **Three carriers now publish a quantified *Stornoabzug*, on three incompatible bases, and one of
    the three is sub judice.** Debeka: 5 % of the *Deckungskapital* as an *Ausgleich für kollektiv
    gestelltes Risikokapital*, plus a *kapitalmarktabhängige* deduction of **0 %, 5 %, 10 % or 15 %**
    of the *Deckungskapital* according to which of four *Kapitalmarktsituationen* obtains, both
    components falling **linearly to nil over the last ten years** before maturity and both lapsing
    altogether on a late cancellation after age 62 [S3]; the consumer bodies describe the same clause,
    omitting the nil case, as "5 Prozent ... zusätzlich ... 5, 10 oder 15 Prozent des Deckungskapitals"
    [R30]. Die Bayerische: "50 EUR plus 0,15 %" of the premiums fallen due multiplied by the years
    remaining to the original maturity [S9]. VPV: "100 € für erhöhte Verwaltungsaufwendungen" plus
    "0,2 % der Differenz zwischen Versicherungssumme und dem Rückkaufswert" [S18]. The Debeka clause is
    the subject of a live Verbraucherzentrale collective action [R30] and the BGH **remitted the
    *Angemessenheit* question rather than deciding it** [R22]. Three figures on three bases are not a
    market range; the composite's declining percentage-of-reserve schedule is **[std]**, matching one
    of the three shapes and falling with duration as all three effectively do, which is what
    *Angemessenheit* points towards [R24].
20. The *Effektivkostenquote* (Reduction in Yield) discloses all costs as the reduction they cause in
    the contract's annual yield; the basis is § 7 Abs. 2 und 3 VVG i. V. m. §§ 2 und 3 VVG-InfoV, it
    was introduced by the LVRG and has been mandatory in quotations since 1 January 2015, and under
    PRIIPs it must appear in the *Basisinformationsblatt* [R9] [R19] [REG-R31] [REG-R32].
    **Reproducing one exactly needs the PRIIPs Annex VI algorithm and a specified holding period,
    neither of which delib implements**, so it is a validation target and not an input.


### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| *Rückkaufswert* and its floor | The *Deckungskapital* computed **by recognised actuarial rules**, on the ***Rechnungsgrundlagen der Prämienkalkulation*** — the pricing basis, not a current or reserving basis — **as at the end of the current *Versicherungsperiode***; and on *Kündigung* **at least** the *Mindestrückkaufswert*, the *Deckungskapital* obtained when the *angesetzte Abschluss- und Vertriebskosten* are spread **evenly over the first five contract years** | [R2] [REG-R28]; the even-spread reading **[std]** (21) |
| *Stornoabzug* | Permissible **only if *vereinbart*, *beziffert* and *angemessen***; a deduction for *noch nicht getilgte Abschluss- und Vertriebskosten* is **unwirksam**, with the burden of proof on the insurer. *Beziffert* does **not** require a concrete euro amount at conclusion: an unambiguous calculation procedure free of *Ermessensspielraum* suffices, so a **capital-market-dependent** deduction is lawful in principle | [R2] [R22] [R24] [REG-R28] |
| *Überschussanteile* on surrender | The accumulated *Überschussguthaben* is paid with the *Rückkaufswert*; the investment return earned and the *Überschussbeteiligung* are **included in** the calculation, and the value **can be below the premiums paid, especially in the early contract years** | [S11] [R4] |
| *Beitragsfreistellung* | Conversion into a *prämienfreie Versicherung* **at any time, with effect for the end of the current *Versicherungsperiode***, **provided the agreed *Mindestversicherungsleistung* is reached**, the reduction being available **in whole or in part**. Below the minimum the insurer must instead **pay the *Rückkaufswert* including *Überschussanteile* under § 169** — the election **becomes a surrender** | [R3] [REG-R28]; partial [S7] |
| *Beitragsfreie Versicherungssumme* | Computed by recognised actuarial rules, on the *Rechnungsgrundlagen der Prämienkalkulation*, **on the basis of the *Rückkaufswert* under § 169 Abs. 3 bis 5** — so it **inherits the five-year spreading floor** — and **stated in the contract for each *Versicherungsjahr***; *Prämienrückstände* are netted at the same date | [R3] [REG-R28] |
| *Mindestversicherungsleistung* level | 2,500 EUR | **not established**; **[std]** (22) |
| Insurer termination for arrears | Where the insurer terminates, the insurance is **automatically converted to *prämienfrei***, and in the § 38 Abs. 2 premium-default case the insurer owes what it would have owed had the contract been paid-up at the claim date. German lapse is therefore a **three-way decrement** — surrender, *Beitragsfreistellung* and premium-default conversion — and the implementation models the first as a decrement, the second as a scheduled election and the third **not at all**, §§ 37 and 38 VVG never having been researched (gap 20) | [REG-R28] [REG-R30]; **not modeled** |
| Not researched, and therefore not asserted | **§ 152 VVG** (the 30-day *Widerruf*) and **§§ 37/38 VVG** (arrears). **§ 168 VVG** (the *Kündigung* right and its timing) was read in the re-verification pass with the rest of VVG Kapitel 5, but nothing here is drawn from it. What the corpus does establish is that the value is struck **at the end of the current *Versicherungsperiode*** | gap 20, narrowed; [R2] |
| Supervisory override | Guarantees sit under two write-down powers: a fund-level **5 %** cap under § 222 VAG and an uncapped reduction under § 314 VAG, which also lets the supervisor **temporarily prohibit the *Rückkauf*** | [REG-R12]; **not modeled** |

21. "Gleichmäßige Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf
    Vertragsjahre" [R2] admits two implementations: a **straight-line** amortisation of the charged
    acquisition cost in five equal instalments, and a **five-year Zillmerung** annuitising it over a
    five-year premium-paying period. The composite takes the straight-line reading, which is what the
    words literally say; the difference is quantified in `technical-notes.md`, where it is a pitfall.
22. Neither the *Mindestversicherungsleistung* itself nor any carrier's level was established. The
    2,500 EUR figure is the lower of the two minimum sums the fused consumer summary reports, used only
    as an order of magnitude — and footnote 3 records that those figures probably belong to a different
    product. One model point is written so the test **fails** and the paid-up election converts into a
    surrender, because that branch of § 165 is the one an implementation forgets [R3].

---


## Contractual mechanics

### Überschussbeteiligung — the entitlement, the base and the timing

§ 153 Abs. 1 VVG gives the policyholder a **right** to participate in the *Überschuss* and in the
*Bewertungsreserven*, excludable only by express agreement and only in whole; § 153 Abs. 2 requires
the insurer to operate it by a ***verursachungsorientiertes Verfahren***, or by other comparable
appropriate distribution principles [R1] [REG-R24]. The statute **names the principle and does not
prescribe the algorithm**, which is exactly why the declared rates are insurer-discretionary and why
every level in delib is **[std]** unless a *Tarifblatt* supplies one; the BGH tied that Absatz to
§ 138 Abs. 2 VAG in IV ZR 436/22 of 18 September 2024 [REG-R24] [REG-R8]. A model allocating surplus
**in proportion to each contract's own reserve** is implementing a causation-oriented procedure.

Four wordings fix the base and three fix the timing, and they no longer agree on the second.
**The base is the contract's own reserve.** The *Ertragsanteil* is "in Prozent des maßgeblichen
Deckungskapitals" [S7]; the *Zinsüberschussanteil* is the reserve "um ein Jahr mit dem Rechnungszins
abgezinste" multiplied by the declared rate [S18]; the *Zinsüberschussanteile* are declared in percent
of the reserve and booked into it [S9] [S3]. Both endowment wordings pair that interest component with
a **risk** component on a different base — ‰ of the sum insured and % of the risk premium at Gothaer,
the *Risikojahresbeitrag* at VPV — which is why the model's single reserve-proportional credit is a
[std] simplification of a two-part declaration. **The timing is the balance date**: die Bayerische
allocates at each *Bilanztermin*, being 31 December, and at the end of the accumulation phase, booking
into the *Deckungskapital* [S9] — an annuity wording, a provenance stated wherever the rule is used —
while Gothaer allocates at the policy's own *Stammtag* [S7] and VPV at the start of the policy year
[S18]. **The waiting period varies and the model takes the shortest**: none at die Bayerische ("Der
Anspruch auf Überschussbeteiligung beginnt sofort mit dem Versicherungsschutz") [S9], one year at VPV
[S18], three years for Gothaer's tariff group A [S7] and for Debeka's *Zinsüberschussanteile* [S3].
`surplus_credit_pp` running from `t_start()` is therefore a **[std]** choice among three observed
conventions, not the single sourced fact it was recorded as. **The level is discretionary and may be
zero**: it cannot be guaranteed and depends on capital-market development, the insured risk and costs
[S1] [S3], and "Die Leistung aus der Überschussbeteiligung kann auch Null Euro betragen" [S9] [S1] — the cleanest
sourced justification in the corpus for treating the surplus rate as an insurer-discretionary current
assumption. Carriers and commentators decompose the surplus into four components [S16] [S15] [S17] [R28]:

| Component | Arises when | Minimum policyholder share |
|---|---|---|
| *Zinsüberschuss* | the investment return exceeds the guaranteed *Rechnungszins* | "90 Prozent der nach § 3 Absatz 1 anzurechnenden Kapitalerträge **abzüglich der rechnungsmäßigen Zinsen**", § 6 Abs. 1 MindZV [R6] [REG-R18] |
| *Risikoüberschuss* | mortality experience is better than priced | 90% of the *Risikoergebnis*, raised from 75% by the LVRG with effect from 7 August 2014 [R6] [REG-R18] [REG-R20] |
| *Kostenüberschuss* | the book is administered more cheaply than loaded | MindZV: 50% of the *übriges Ergebnis*, of which the cost result is the main part [R6] [REG-R18] |
| *Schlussüberschussanteil* | long-run results not fully allocated during the term | **no statutory minimum established** [S16] |

**What § 6 Abs. 1 deducts is the *rechnungsmäßige Zinsen* — the technical interest already owed to
the contracts — and that is how the guarantee is taken off the top before the policyholder's interest
share is struck** [R6] [REG-R18]. (The instrument was read for this pass; the *Aufwand für die
Diskontierung der Deckungsrückstellung* recorded here previously is not what § 6 Abs. 1 says.) The
framings differ and the MindZV's is the one to cite: consumer sources say "half of the
*Kostenüberschuss*" and cite it, wrongly, to § 153 Abs. 3 VVG [S16], where § 8 MindZV requires 50 % of
the wider *übriges Ergebnis*, so any statement that the cost surplus specifically carries a 50 %
minimum is [unverified] (gap 6). And **these are minimum allocations to a
provision, not to a contract**: the *Rohüberschuss* reaches the RfB first, the minimum is computed
separately for *Altbestand* and *Neubestand* [R6] [REG-R10] [REG-R11] [REG-R18], and between the RfB
and the policy sits the insurer's annual, discretionary declaration [S3] [S9]. A delib model projects
the **output** of that policy and **must not present the 90/90/50 quotas as if they determined it**.

### Überschussverwendung — how the allocated surplus is applied

Four systems are named, the system is fixed at conclusion, and the precise rules are in the
*Versicherungsbedingungen*, which must be attached to every contract [R28] [S15]:

1. ***Verzinsliche Ansammlung*** — the *Überschussanteile* accumulate with the insurer, bear interest
   at an *Ansammlungszinssatz*, and are paid at termination with the guaranteed *Versicherungssumme*;
   they compound and so raise the maturity benefit [R28], which [S18] states in a wording: the
   *laufende Überschussanteile* "werden verzinslich angesammelt und zusammen mit einer garantierten
   Leistung ausbezahlt". This produces a separate, visible balance, which the GDV model
   *Standmitteilung* reports as the "Bisher erreichte einmalige Zahlung aus laufender
   Überschussbeteiligung" beside the guaranteed part [S2].
2. ***Bonussystem* (*Summenzuwachs*)** — the surplus buys **additional paid-up insurance**, so the sum
   insured itself grows. The corpus does not spell out the purchase mechanics but states the
   consequence precisely: **"compared with the *Bonussystem*, the *verzinsliche Ansammlung* leads to a
   higher payment at maturity, while the *Bonussystem* produces higher death benefits"** [R28] — the
   discriminating test between the two in a projection.
3. ***Beitragsverrechnung*** — the allocation is set off against the premium, so the policyholder pays
   only part of it [R28]. In a projection this **reduces the premium cash flow rather than raising the
   benefit**, which changes the sign of the surplus in the cash flow statement.
4. ***Anlage in Fondsanteilen*** — not established by any search result; [unverified], not implemented.

The corpus says that as a rule either the first or the second applies [R28] and **does not say which
is more common**. The composite runs *verzinsliche Ansammlung* as the **[std]** base case, and the
retrieved wordings support that choice from three directions: VPV accumulates the *laufende
Überschussanteile* with interest and pays them with the guaranteed benefit [S18]; Gothaer offers
*Verzinsliche Ansammlung* as the first of its four named systems and describes *Gewinnsystem BE* as
the one that "vor allem die Leistung Ihrer Versicherung im Erlebensfall verstärkt" [S7]; and die
Bayerische books its *Zinsüberschussanteile* straight into the *Deckungskapital*, calling that form
*Kapitalzuwachs* [S9]. The other two systems are carried as variants.

### The laufende Verzinsung is not a surplus rate on top of the guarantee

This is the commonest arithmetic error in describing a German contract and it is a numbered pitfall in
every affected delib product. The ***laufende Verzinsung*** is the *Garantieverzinsung* **plus** the
*laufende Zinsüberschussbeteiligung*, so a declared 2,70 % on a 1,00 % guarantee implies a **1,70 pp**
surplus credit, not 2,70 pp on top of 1,00 pp [REG-R53]. The rates the research established:

| Basis | Rate | Year | Tag |
|---|---|---|---|
| Allianz, "klassische Lebens- und Rentenversicherungen", *laufende Verzinsung*, held constant | 2.70% | **2025** | [R26] |
| Allianz *Perspektive*, *laufende Verzinsung* | 2.80% | 2025 | [R26] |
| Alte Leipziger, klassische Rentenversicherung, laufend / total | 2.25% / 2.45% | 2025 | [R26] |
| LVM, laufend / total | 2.40% / 3.10% | 2025 | [R26] |
| Market average, klassische private Rentenversicherung, laufend / total | 2.62% / 3.23% (2026); 2.53% / 3.19% (2025) | 2026 / 2025 | [R25] |
| Market average, *Neue Klassik*, laufend / total | 2.65% / 3.32% | 2026 | [R25] |
| Market average, Klassik / Neue Klassik | 2.53% / 2.58% | 2025 | [REG-R53] |
| Market average, 2026, **three incompatible figures** | 2.6–2.7% / 2.87% / 2.54% | 2026 | [REG-R53] |
| *Höchstrechnungszins* | 1.00% | from 2025-01-01 | [R7] [REG-R15] |

**The critical caveat, sharpened by retrieval: not one of these rates is an endowment rate.**
Assekurata's figures are stated by Assekurata itself to be "in der klassischen privaten
Rentenversicherung" [R25]. The 2,70 % the composite uses is **not** on any Allianz page — the three
retrieved Allianz pages state only the 1,00 % *Garantiezins* — but is procontra's report of Allianz's
declaration for "die klassischen Lebens- **und** Rentenversicherungen", i.e. a combined book, and for
**2025**, not 2026 [R26]. So the composite's `decl_rate` is anchored to a one-year-old trade-press
figure for a book that mixes the two products, and **that the endowment shares the annuity's rate is
[unverified]** (gap 2). It is still the closest thing in the corpus to a manufacturer declaration
touching an endowment book, and it sits at the top of a band running from 2,25 % to 2,65 % on the
retrieved evidence, which is why it is kept. For 2026 about **one in three** insurers raised the
*Überschussbeteiligung* [R26]; the caution in the rest is attributed by Assekurata to "weiterhin
vorhandene *stille Lasten* in den Kapitalanlagen sowie vorsichtige Prognosen zur Zinsentwicklung",
and only **eleven** of the companies it surveys still write classic private annuities as new business
at all [R25]. For orientation, § 154 VVG requires a *Modellrechnung* at three rates set by
§ 2 Abs. 3 VVG-InfoV — the *Höchstrechnungszins* × 1,67, and that rate ± one percentage point
[REG-R25] — so at 1,00 % the statutory triple is **1,67 % / 2,67 % / 0,67 %**, and the composite's
2,70 % sits a hair above the middle rate of a German insurer's own statutory illustration.

### Deckungskapital, Zillmerung and the Bewertungsreserven

The ***Deckungskapital*** is the amount that **should** be held to provide the guaranteed benefits;
the ***Deckungsrückstellung*** is the balance-sheet quantity of the amount actually held [R28], and
**delib projects the former and references the latter without specifying it**. It is computed
**prospectively**, at the *Rechnungszins*, on the ***Rechnungsgrundlagen der Prämienkalkulation*** —
the first-order basis, not a current or market basis [R2] [R28] [REG-R47] [REG-R54]. Under § 341f HGB
the *Deckungsrückstellung* is formed at the *versicherungsmathematisch berechneter Wert*, including
profit shares already allocated but **excluding *verzinslich angesammelte Überschussanteile***, and
after deducting the present value of future premiums [REG-R54] — which is exactly why the
*Überschussguthaben* is a separate balance in this model and not part of the reserve.

***Zillmerung*** offsets a contract's one-off acquisition costs against its first premiums. The
***gezillmerte Nettoprämie*** is the annual premium whose present value equals that of the benefits
**plus** the *zillmerfähige Abschlusskosten*; the *Deckungskapital* is correspondingly **reduced by
the present value of the acquisition costs not yet recovered**, so **in the early years a negative
*Deckungskapital* arises** [R28]. The cost is incurred at once because insurers "compensate their
distribution partners with an *Abschlussprovision* as a share of the contractually agreed
*Beitragssumme* at conclusion of the contract, **regardless of whether the customer has already paid
that premium sum**" [R28-family]. And ***Zillmerung is a per-tariff choice a German insurer makes and
publishes***: die Bayerische publishes a *gezillmert* edition (B 520127) and a non-*gezillmert* one
(B 520136) of the **same** tariff [S9], so the implementation must run with *Zillmerung* off too.

The ***Bewertungsreserven*** leg sits alongside the reserve and is not projected. § 153 Abs. 3 VVG
requires the insurer to determine them anew each year, allocate them by a causation-oriented
procedure, and **on termination allocate and pay out half of the amount then determined** [R1]
[REG-R24]; § 139 VAG then cuts that back, permitting participation by **exiting** policyholders **only
to the extent the *Bewertungsreserven* exceed any *Sicherungsbedarf*** — the sum, over contracts with
an *überhöhter Rechnungszins*, of the actuarially valued interest obligation less the
*Deckungsrückstellung* [R8] [REG-R9]. The hinge is § 153 Abs. 3 Satz 3 VVG in its LVRG form [R1]
[REG-R20] and the leading decision **BGH, 20 January 2021, IV ZR 318/19**, which held the cut-back
lawful [R23] [REG-R36]. The base run sets the participation to **zero** (footnote 13) because it is
**path- and balance-sheet-dependent in a way a gross cash flow model cannot reproduce** [REG-R24].

### Rückkaufswert and Stornoabzug — § 169 VVG

The claim arises on termination, **in particular by *Kündigung*, *Rücktritt* or *Anfechtung*** [R2];
also where the insurer is *leistungsfrei* for *Selbsttötung* [R4] and where a *Beitragsfreistellung*
request fails the *Mindestversicherungsleistung* test [R3]. The calculation rule, as the search
summary reported § 169 Abs. 3 VVG, is five requirements at once: a ***Deckungskapital***; computed **by
recognised actuarial rules**; on the ***Rechnungsgrundlagen der Prämienkalkulation***; struck **at the
end of the current *Versicherungsperiode***, not at the cancellation date; and, **on *Kündigung***,
floored by the ***Mindestrückkaufswert*** — the *Deckungskapital* obtained when the *angesetzte
Abschluss- und Vertriebskosten* are spread evenly over the first five contract years [R2] [REG-R28].
For *fondsgebundene* and certain other classes the value is instead a ***Zeitwert*** [R2]; **that
branch governs delib product 3 and not this one.**

**The five-year spreading and the 25 ‰ cap are different rules and delib keeps them apart.** One
search summary conflated them, stating that "according to § 169 Abs. 3 VVG the applied acquisition and
distribution costs must be spread over at least the first five years and must not exceed 2,5 % of the
contractual *Beitragssumme*". They do not come from the same instrument: **§ 169 Abs. 3 VVG fixes *how*
the costs are spread for the surrender floor** — a floor on the **value** — while **§ 4 DeckRV fixes
*how much* may be zillmered at all** — a cap on the **charge** [R2] [R7] [REG-R16] [REG-R28] (gap 5).
A model carrying a zillmerised reserve applies both separately, the tighter binding.

The *Stornoabzug* is subject to three cumulative conditions — ***vereinbart*, *beziffert* und
*angemessen*** — and a deduction for *noch nicht getilgte Abschluss- und Vertriebskosten* is **void**,
with the burden of proof on the insurer [R2] [REG-R28]; that last limb stops an insurer recovering
through the deduction what the five-year spreading denies it. On *Bezifferung* the BGH has held that
the requirement does **not** compel a concrete euro amount at conclusion: **an unambiguous calculation
procedure suffices, provided it leaves the insurer no *Ermessensspielraum* and is free of unilateral
determination rights**, so a capital-market-dependent deduction is lawful in principle and need not be
a constant [R22]. **The citation is now established**: BGH, judgment of **18 March 2026**, Az.
**IV ZR 184/24**, holding the clause to satisfy § 169 Abs. 5 Satz 1 VVG and not to offend § 307
Abs. 1 Satz 2 BGB — "Vielmehr kann der Versicherer auch auf die Regelung eines Berechnungsverfahrens
für den Stornoabzug zurückgreifen" — and remitting the *Angemessenheit* question to the OLG Koblenz
[R22]. The rider about *Ermessensspielraum* is not in the retrieved reports and is dropped. The **older line** required the deduction to be *eindeutig erkennbar*
and struck down clauses that failed to distinguish the *Rückkaufswert* from the *Stornoabzug*, left it
to discretion, or named it only after the *Kündigung* [R24] — **the historical reason delib treats the
*Stornoabzug* as a contractual, pre-declared schedule.**

### Beitragsfreistellung — § 165 VVG

The policyholder may **at any time, with effect for the end of the current *Versicherungsperiode*,
demand conversion into a *prämienfreie Versicherung***, provided the agreed
*Mindestversicherungsleistung* is reached [R3] [REG-R28]. **If it is not reached**, the insurer must
instead pay the *Rückkaufswert* including *Überschussanteile* under § 169 — **below the minimum the
paid-up election becomes a surrender**, and a model that offers *Beitragsfreistellung* without the test
is wrong [R3]. The ***beitragsfreie Versicherungssumme*** is calculated by recognised actuarial rules,
on the *Rechnungsgrundlagen der Prämienkalkulation*, **on the basis of the *Rückkaufswert* under § 169
Abs. 3 bis 5**, and **must be stated in the contract for each *Versicherungsjahr*** [R3] [REG-R28] — so
it is a **function of the surrender value**, **inherits the five-year spreading floor**, and is
**contractual and tabulated at issue** rather than computed at the election.

Both routes are struck at period end and run off the same *Rückkaufswert* base [R2] [R3], but
*Beitragsfreistellung* **keeps the contract alive** with a reduced sum insured, keeps the policyholder
participating in surplus, and pays nothing now, while *Kündigung* **ends** the contract, pays now, and
— uniquely — attracts the *Mindestrückkaufswert* floor § 169 Abs. 3 expresses for the *Kündigung* case
[R2]. The paid-up route also **loses attached *Zusatzversicherungen*** [R3], and the reduction may be
**in whole or in part** [S7]. GDV's headline *Stornoquote* **counts conversion to *beitragsfrei* as
part of the lapse rate** [R20], so that figure is not a surrender rate.

### Selbsttötung — § 161 VVG

In an insurance for the event of death the insurer is ***leistungsfrei*** if the *versicherte Person*
**intentionally takes her own life before three years have elapsed since conclusion**, unless the act
was committed in a state excluding free determination of the will caused by a *krankhafte Störung der
Geistestätigkeit*; the period may be **extended by individual agreement**, and by implication not
shortened; and **where the insurer is *leistungsfrei* it must nevertheless pay the *Rückkaufswert*
including *Überschussanteile* under § 169** [R4] [REG-R26]. **The German rule is a benefit
substitution, not a forfeiture** — unlike art. L. 132-7 of the French Code des assurances, where the
cover is *de nul effet* in the first year and there is no surrender value to fall back on. In a
projection a suicide inside the window is a **surrender-value payment, not a nil payment**, a
duration-dependent *benefit definition* rather than a rate adjustment [REG-R26]. Whether any carrier
extends the period was not established; no carrier's suicide clause was obtained.

---

## Riders and options

**In scope (modeled or parameterized).** The three *Überschussverwendung* systems the corpus
establishes [R28], as a model-point enum with the base run on *verzinsliche Ansammlung* and one point
on each of the others; the ***abgekürzte Beitragszahlungsdauer***, as a `prem_term` shorter than
`policy_term` [S3] [R28-family]; the ***Einmalbeitrag***, as `prem_term = 1` [REG-R53]; the
***Beitragsfreistellung*** election of § 165 VVG, as a scheduled policy year with both branches of the
*Mindestversicherungsleistung* test exercised [R3]; the ***Stornoabzug***, as a pre-declared duration
schedule [S3] [R22] [R24] [R30]; the ***Risikozuschlag***, as a multiplier on the risk premium [R5];
the ***Zillmerung*** switch, because one carrier publishes both editions of one tariff [S9]; and the
***Beteiligung an den Bewertungsreserven***, as a parameter set to zero in the base run [R1] [R8].

**Out of scope, and said so.** The ***Berufsunfähigkeits-Zusatzversicherung*** and every other
*Zusatzversicherung*, separate covers with their own decrements which § 165 VVG's practical note
records are **regularly lost on *Beitragsfreistellung*** [R3]; the ***Unfall-Zusatzversicherung***,
the ***Beleihung*** and the ***Abtretung***, none of which any located German endowment wording
describes; the ***Kapitalwahlrecht* / annuitisation option at the *Ablauf***, because no located
wording sets one out and no *Rentenfaktor* for an endowment was established (the annuity chassis is
`products/klassische_rentenversicherung/`); the ***Anlage in Fondsanteilen*** system, which no source
mentions [unverified]; ***Dynamik***, which would reprice sum and premium together on an exogenous
index; and the ***Vorwegabzug*** of the *Bewertungsreserven* before termination, which § 153 Abs. 3
permits by agreement [R1] and no carrier document evidences.

---

## Variations across insurers

Retrieval reshaped this table more than any other part of the specification. Seven carriers now
produce a document; **three of them produce quantified terms**; and, decisively, **only two of the
documents are endowment wordings at all** — Gothaer [S7] and VPV [S18]. The three Debeka
*Bedingungswerke* turned out to be deferred annuities with fund components, and Debeka's own document
library lists no endowment AVB under its live *Kapitalbildende Lebensversicherung* heading [S6].
Nineteen of the twenty-six named carriers produced nothing at all, and **no URL was guessed for any
of them**.

| Feature | Debeka [S3] [S4] [S5] [S6] | Allianz [S11] | Gothaer [S7] | die Bayerische [S8] [S9] | VPV [S18] | ERGO [S12] | ÖSA [S10] |
|---|---|---|---|---|---|---|---|
| Endowment AVB located | **no** — the three *Bedingungswerke* are deferred annuities with fund components | no | **yes**, 12 pp., version 05.12.2011 | URL only, 404 | **yes**, 26 pp., edition 01.2019 | no | no |
| Edition dates, wording length | all three 2026-07-01; 21 / 19 / 18 pp | n/a | 2011-12-05; 12 pp | 2022 / 2025, annuity siblings, 14 pp each | 2019-01; 26 pp incl. *Verbraucherinformationen* | n/a | 3 pp (BIB) |
| Surplus base published | yes, for the annuity: % of *Deckungskapital* at the start of the month, **monthly**, from year 3 | no | **yes** — *Ertragsanteil* in % of the *Deckungskapital*, *Risikoanteil* in ‰ of the sum insured and % of the risk premium | yes, for the annuity: booked into the *Deckungskapital* | **yes** — reserve discounted one year at the *Rechnungszins* × declared rate; risk surplus on the *Risikojahresbeitrag* | no | no |
| Surplus timing published | yes — monthly, deferred to year 3 | no | **yes** — annually at the *Stammtag*; tariff group A deferred three years | **yes** — 31 December *Bilanztermin*, accruing monthly, no waiting period | **yes** — start of the policy year, one-year *Wartezeit* | no | no |
| Declared *laufende Verzinsung* | not established | 2.70% for **2025**, and only via [R26] — **not on any Allianz page** | not established | not established | not established | not established | not established |
| *Stornoabzug* published | **yes** — 5 % of the *Deckungskapital* + 0/5/10/15 % by *Kapitalmarktsituation*, both decaying to nil over the last 10 years | no | yes, qualitatively; amount in the *Garantiewerttabelle* | **yes** — 50 € + 0,15 % of premiums paid × years remaining | **yes** — 100 € + 0,2 % of (*Versicherungssumme* − *Rückkaufswert*) | no | no |
| *Zillmersatz* visible | no | no | **yes — 4 %**, the pre-LVRG 40 ‰ ceiling | yes — 2,5 %, both editions | yes — 2,5 % | no | no |
| Paid-up clause visible | yes | no | **yes** — full or partial, floor 1.500 EUR | yes — floor 25 EUR monthly annuity | yes | no | no |
| *Selbsttötung* window | n/a | no | **two years**, shorter than § 161 VVG | not established | not established | no | no |
| Product-level cost figures | no | no | no | no | no | no | **yes** — RIY 5,3 % p.a. at 20 years |
| PRIIP-BIB located | no | no | no | no | no | no | **yes** |

Parameter ranges, where more than one observation exists:

| Parameter | Observed range | Who sits where | Tag |
|---|---|---|---|
| *Höchstrechnungszins* by cohort | 0.25% – 4.00%, currently 1.00% | market-wide, by year of issue | [R7] [REG-R15] |
| Declared *laufende Verzinsung* | 2.25% – 2.80% at named carriers (2025); 2.62% annuity market average (2026) | Allianz 2.70% at the top of the named range, Alte Leipziger 2.25% at the bottom; "Neue Klassik" 2.65% | [R25] [R26] [REG-R53] |
| *Höchstzillmersatz* by cohort | 40 ‰ (4 %) before 2015, 25 ‰ (2,5 %) from 1 January 2015 | Gothaer's 2011 wording at 4 %, die Bayerische and VPV at 2,5 % | [R7] [S7] [S9] [S18] [REG-R16] |
| *Ratenzahlungszuschlag* | 2% half-yearly / 3% quarterly / 5% monthly | market convention, no carrier attribution | [R28] |
| *Stornoabzug* | **three incompatible bases**: 0–20% of the *Deckungskapital*; 50 € + 0,15 % of premiums × years remaining; 100 € + 0,2 % of (sum insured − reserve) | Debeka (sub judice), die Bayerische, VPV | [S3] [S9] [S18] [R22] [R30] |
| Surplus *Wartezeit* | none / one year / three years | die Bayerische / VPV / Gothaer tariff group A and Debeka | [S9] [S18] [S7] [S3] |
| *Verwaltungskostenquote*, 2024 | under 2% to over 4%, average 2.19% or 2.4% | whole-book ratios, market-wide | [REG-R53] |
| *Effektivkosten* | "über vier Prozent" in individual cases on 2021 new business; 5,3 % p.a. at 20 years on one BIB model case | BaFin survey; ÖSA | [R18] [S10] |
| Contract term as sold; *Stornoquote* | 12 years (tax minimum) to 40 years; 2.56% (GDV headline, count, 2023) | market-wide; the GDV measure is neither endowment-specific nor by duration | [R10] [S12] [S13]; [R20] |

Three observations follow, and each shapes a composite choice.

1. **The surplus base is now published by four carriers and they agree on it.** The interest surplus
   is a percentage of the *Deckungskapital* at Gothaer, VPV, die Bayerische and Debeka [S7] [S18]
   [S9] [S3], and VPV states the base precisely — the reserve discounted back one year at the
   *Rechnungszins*. What they differ on is **timing**: none at die Bayerische, a one-year *Wartezeit*
   at VPV, three years at Gothaer's tariff group A and at Debeka. Composite: the reserve base, annual
   period-end crediting, and **no** waiting period, the last being a [std] choice among three observed
   ones rather than the single observation it was recorded as.
2. **No carrier publishes a declared rate for an endowment book.** The 2,70 % the composite runs is
   trade-press reporting of Allianz's 2025 declaration for a combined classic life-and-annuity book
   [R26], with the endowment identity [unverified] (gap 2). Three carriers publish a *Stornoabzug*,
   on three different bases, and one of the three is sub judice [S3] [S9] [S18] [R22] [R30].
   Composite: a declining **[std]** schedule on the reserve, which is one of the three shapes and the
   only one the model's state variables can express without new columns. The vintage spread the
   Debeka triple was cited for does not exist — the three wordings share one edition date — and the
   cohort argument is carried instead by DeckRV § 2 Abs. 2 and § 4 Abs. 4, which fix both ceilings at
   conclusion for the whole term [R7], and by Gothaer's 4 % clause [S7].
3. **What does not vary is legal rather than commercial**: participation as an all-or-nothing statutory
   default [R1]; the § 169 calculation rule and its five-year floor [R2]; the § 165 paid-up right and
   its *Mindestversicherungsleistung* test [R3]; the § 161 three-year window paying the *Rückkaufswert*
   [R4]; and the 25 ‰ *Höchstzillmersatz* [R7]. Every one is a statutory fact.

---

## Regulatory context

**Contract law — the VVG.** The product sits in **Kapitel 5 (Lebensversicherung)** of the VVG 2008,
whose provisions are **halbzwingend** under § 171 [R1] [R4] [REG-R22]. Five articles do nearly all of
the work: **§ 153** (*Überschussbeteiligung*: an entitlement excludable only in whole, allocated by a
*verursachungsorientiertes Verfahren*, the *Bewertungsreserven* redetermined annually and half
allocated on termination) [R1] [REG-R24]; **§ 169** (*Rückkaufswert*: the *Deckungskapital* on the
pricing basis at the end of the current *Versicherungsperiode*, floored on *Kündigung* by the
five-year-spread *Mindestrückkaufswert*, with a *Stornoabzug* only if *vereinbart*, *beziffert* and
*angemessen*) [R2] [REG-R28]; **§ 165** (*prämienfreie Versicherung*: the conversion right, the
*Mindestversicherungsleistung* test, the paid-up sum computed on the § 169 value and tabulated per
*Versicherungsjahr*) [R3] [REG-R28]; **§ 161** (*Selbsttötung*: three years, extendable, with the
*Rückkaufswert* payable) [R4] [REG-R26]; and **§ 19** (*vorvertragliche Anzeigepflicht*, with
retrospective adjustment as the usual remedy and five- and ten-year limits) [R5] [REG-R30]. Alongside
them **§ 154** requires a *Modellrechnung* at three interest rates and **§ 155** an annual
*Standmitteilung* in *Textform* disclosing to what extent the profit participation is guaranteed
[REG-R25] — which is why a published *Standmitteilung* specimen is a legitimate primary-source class
here [S2]. **Three provisions the product depends on were never researched** — **§ 152**,
**§§ 37 and 38** and **§ 150** — the drafting pass having reached them with no retrieval channel and
an exhausted search budget, and the re-verification pass having recorded only the sections the
specification cites. **Nothing is asserted about any of the three anywhere in delib**; § 168,
the fourth on that list when it was written, has since been read with the rest of Kapitel 5 and
nothing rests on it either (gap 20, narrowed).

**Prudential — the VAG and the two ministerial regulations.** BaFin supervises German life insurers
under Solvabilität II as transposed into the **VAG**, with no second national supervisor [REG-R5]
[REG-R21]. § 138 Abs. 1 VAG is the pricing sufficiency rule and the reason a German tariff is priced
on **prudent, not best-estimate, bases**: premiums must be set high enough to meet all obligations and
in particular to form adequate *Deckungsrückstellungen*, and funds not deriving from premium payments
may not systematically and permanently support the tariff [REG-R8]. § 139 Abs. 1 VAG is the structural
fact behind the surplus chassis — amounts earmarked for the *Überschussbeteiligung* go out immediately
as *Direktgutschrift* or into the **RfB**, and nowhere else [REG-R9] — with § 140 VAG ringing the RfB
off, its second escape hatch having financed the *Zinszusatzreserve* out of the free RfB during the
low-rate decade [REG-R10] [REG-R17], and the **RfBV** governing the collective part that makes
cross-cohort smoothing possible without breaching § 138 Abs. 2 VAG [REG-R19]. § 143 VAG requires the
undertaking to notify the supervisor of the *Grundsätze für die Berechnung der Prämien und der
Deckungsrückstellungen* including the *Rechnungsgrundlagen* — **which is why a German tariff's
first-order bases exist as a documented, supervisor-visible object and equally why they are not
public** [REG-R11]. The arithmetic is delegated to the **DeckRV** (§ 2 the *Höchstrechnungszins*, § 4
the *Höchstzillmersatz*, § 5 Abs. 3 the *Referenzzins* behind the *Zinszusatzreserve*) [R7] [REG-R14]
[REG-R16] [REG-R17] and the **MindZV** (the 90 / 90 / 50 minimum allocation to the RfB, computed
separately for *Altbestand* and *Neubestand*, the *Direktgutschrift* deducted, a negative minimum
replaced by zero) [R6] [REG-R18]. The *Höchstrechnungszins* is a ministerial regulation because § 88
Abs. 3 VAG empowers the Bundesministerium der Finanzen to fix it — **which is also why the DAV's
annual recommendation is a recommendation and not a decision** [REG-R6] [REG-R14] [REG-R56]; the
1,00 % rate effective 1 January 2025 came from the **Sechste Verordnung zur Änderung von Verordnungen
nach dem Versicherungsaufsichtsgesetz of 19 July 2024**, BGBl. 2024 I Nr. 250 [REG-R15] [R7] [R15]
[R16]. The outer boundary of every guarantee is the *Sicherungsfonds* — **Protektor
Lebensversicherungs-AG**, used once, in the Mannheimer case of 2003, and then as a **portfolio
transferred and continued, not a payout** — with the § 222 VAG five-per-cent haircut and the uncapped
§ 314 VAG reduction power behind it [REG-R12].

**Conduct, disclosure and distribution.** BaFin's *Merkblatt 01/2023 (VA)* requires an appropriate
*Kundennutzen*, a *Renditeziel* achievable with sufficient probability for the defined target market,
and for retirement-provision products a real investment success — a return net of costs exceeding a
justified inflation expectation [R17] [REG-R35]; **no numerical threshold was established anywhere in
it**, and OLG Stuttgart rejected the argument that § 1a VVG obliges an insurer to redesign its own
products [REG-R31]. Cost disclosure runs on two tracks: §§ 2 und 3 VVG-InfoV require the *Abschluss-
und Vertriebskosten* included in the premium to be disclosed **as a single total amount in euro**, with
the *Verwaltungskosten* separately [R9] [REG-R31] — **which is why a German *Produktinformationsblatt*
can be read as a source of actual charge levels in a way a French *encadré* cannot**, and why the
absence of any located German PIB or IPID here is the most valuable gap in the research (gap 9) —
while PRIIPs requires a *Basisinformationsblatt* carrying a total risk indicator, the possible maximum
loss, four graded performance scenarios from a **profession-agreed standard method** for PRIIP
*Kategorie 4*, and the *Effektivkosten* of a specimen contract [R19] [R27] [REG-R32]. Distribution sits
under the IDD as transposed across the GewO, the VAG and the VVG [REG-R33], which is why a German
product's acquisition cost is structurally a commission to a § 34d GewO intermediary.

**Taxation.** The tax rules **do not enter the projected liability cash flows** — delib publishes gross
benefits — but they fix the product's design constraints and its typical term. For contracts concluded
from **1 January 2005**, the *Alterseinkünftegesetz* boundary [REG-R38], the taxable amount is the
***Unterschiedsbetrag*** between the *Versicherungsleistung* and the *Beiträge*, and premiums are not
deductible [R10] [R13] [REG-R45]. **The half-income rule**: where the benefit is paid **after
completion of the 60th year of life and at least twelve years after conclusion**, only **half** the
*Unterschiedsbetrag* is taxable, § 20 Abs. 1 Nr. 6 Satz 2 EStG, and for contracts concluded **after
31 December 2011** the required age is **62**, § **52 Abs. 28 Satz 7** EStG — the locus was an open
question before this pass and was cited to § 52 Abs. 36 Satz 9; it is now read in the statute
[R10] [REG-R45]; the flat *Abgeltungsteuer* then does
**not** apply and the personal marginal rate applies to the half amount, § 32d Abs. 2 Nr. 2 EStG [R10].
The ***Mindesttodesfallschutz*** conditions the halving for contracts concluded from **1 April 2009**
on a *Todesfallleistung* of **at least 50 % of all premiums payable over the whole term**, failing
which the earnings are taxed in full [R12] [REG-R45], the guidance being the **BMF-Schreiben of
1 October 2009, IV C 1 - S 2252/07/0001** [R11]. A German endowment book therefore carries at least
**three tax cohorts** — pre-2005, 2005–2011 and 2012 onwards, with the 1 April 2009 line cutting across
the second — and **delib's composite is a post-2011 contract**. **The pre-2005 regime's conditions were
not established and are not asserted anywhere in delib** (gap 13); what can be said is that before
1 January 2005 the *rechnungsmäßige und außerrechnungsmäßige Zinsen* were entirely free of income tax
on maturity, which is why an *Altvertrag* has an almost nil lapse rate and why the reference model does
not represent that cohort [REG-R45]. On death there is **no insurance-specific German regime**: the
*Todesfallleistung* is an *Erwerb von Todes wegen* under § 3 Abs. 1 Nr. 4 ErbStG at the beneficiary's
own *Steuerklasse* and *Freibetrag* [REG-R46].

**Accounting and professional standards.** The statutory *Deckungsrückstellung* is § 341f HGB — formed
at the *versicherungsmathematisch berechneter Wert*, including profit shares already allocated but
**excluding *verzinslich angesammelte Überschussanteile***, and after deducting the present value of
future premiums, by the **prospective method** — measured against the § 341e HGB standard of *dauernde
Erfüllbarkeit* [REG-R54] [REG-R8]. § 28 RechVersV gives the surplus system its published anatomy: a
***Schlussüberschussanteilfonds*** is formed within the RfB, and the *Anhang* must disclose the RfB's
development and, for individual *Abrechnungsverbände*, the *festgelegte Überschussanteile* and where
applicable the ***Ansammlungszinssatz*** [REG-R54] — **the single most useful published source on a
named insurer's surplus system, and the reason a delib document can cite a declared
*Überschussanteilsatz* at all**. Above the HGB accounts sit Solvabilität II, technical provisions being
a best estimate plus a risk margin with EIOPA publishing the curves monthly and § 83 VAG making their
use binding [REG-R1] [REG-R2] [REG-R4] [REG-R6], and Richtlinie (EU) 2025/2, which first applies on
30 January 2027 [REG-R3]; and IFRS 17 has applied since 1 January 2023, this product being the
archetypal direct-participating contract measured under the variable fee approach [REG-R55]. **This
library computes none of it**: no delib model produces a *Deckungsrückstellung*, a *Zinszusatzreserve*,
an RfB stock, a P&L or an SCR, and the whole accounting and capital layer is **cited, never
specified**. The *Verantwortlicher Aktuar* of § 141 VAG **makes the proposal on the
*Überschussbeteiligung*, which the undertaking must submit to the supervisor and from which it may
depart only on written notification with reasons** — the governance reason German declared rates
cluster as tightly as the market data show [REG-R11] [REG-R56].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-kapitallebensversicherung-r1
[R10]: #delib-kapitallebensversicherung-r10
[R11]: #delib-kapitallebensversicherung-r11
[R12]: #delib-kapitallebensversicherung-r12
[R13]: #delib-kapitallebensversicherung-r13
[R14]: #delib-kapitallebensversicherung-r14
[R15]: #delib-kapitallebensversicherung-r15
[R16]: #delib-kapitallebensversicherung-r16
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
[R28]: #delib-kapitallebensversicherung-r28
[R29]: #delib-kapitallebensversicherung-r29
[R3]: #delib-kapitallebensversicherung-r3
[R30]: #delib-kapitallebensversicherung-r30
[R4]: #delib-kapitallebensversicherung-r4
[R5]: #delib-kapitallebensversicherung-r5
[R6]: #delib-kapitallebensversicherung-r6
[R7]: #delib-kapitallebensversicherung-r7
[R8]: #delib-kapitallebensversicherung-r8
[R9]: #delib-kapitallebensversicherung-r9
[REG-R1]: #delib-reg-r1
[REG-R10]: #delib-reg-r10
[REG-R11]: #delib-reg-r11
[REG-R12]: #delib-reg-r12
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R21]: #delib-reg-r21
[REG-R22]: #delib-reg-r22
[REG-R24]: #delib-reg-r24
[REG-R25]: #delib-reg-r25
[REG-R26]: #delib-reg-r26
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R3]: #delib-reg-r3
[REG-R30]: #delib-reg-r30
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R38]: #delib-reg-r38
[REG-R4]: #delib-reg-r4
[REG-R45]: #delib-reg-r45
[REG-R46]: #delib-reg-r46
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R5]: #delib-reg-r5
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
