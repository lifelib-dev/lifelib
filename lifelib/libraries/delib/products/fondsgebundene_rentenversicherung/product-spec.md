# Product Specification

**Status:** Draft, 2026-08-29; citations re-verified against the primary documents 2026-08-30.

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of a German **fondsgebundene Rentenversicherung** (FRV) — the
unit-linked deferred private annuity in which the accumulating capital is a holding of
*Anteileinheiten* (units) in *Investmentfonds* chosen by the policyholder, so that the insurer
guarantees the **number** of units and not their value, and whose single hard financial guarantee
is the *Rentenfaktor* applied at *Rentenbeginn* to whatever the fund is then worth. **It does not
describe any single insurer's product.** [S#] tags are primary product documents (*Allgemeine
Versicherungsbedingungen*, *Produktinformationsblatt*, *Basisinformationsblatt*,
*Verbraucherinformation*) and [R#] product-specific regulatory and actuarial references, both
numbered per `_research/fondsgebundene_rentenversicherung.md` and resolved in `sources.md` (same
directory; numbering frozen, never renumbered); [REG-R#] tags the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose R-numbering is distinct. **[std]**
marks a standardization introduced for the reference implementation, each with a rationale and,
where the research recorded one, the argued range across the German market; [unverified] marks a
claim no retrieved document or search result confirmed.

**Read this before relying on a citation, because the conditions changed after it was written.**
delib was **drafted** under an organisation network policy that blocked all HTTP egress from the
build environment, and on this product the shared `WebSearch` budget was exhausted before its
research began, so the first draft rested on the authoring model's own knowledge of German
insurance law and practice, disciplined by the [std] and [unverified] tags; the few facts
corroborated at one remove came from searches run for sibling delib products and are attributed
to them. **That policy has since been lifted and the citations re-verified against the primary
documents on 2026-08-30.** For this product, **eighteen of the forty-four entries in `sources.md`
now say `Retrieved: yes` — 41 %** — two more say `partly`, and twenty-four still say `no`; across
delib as a whole 501 of 805 entries (62 %) are retrieved, and this product sits below that
because of its carrier sweep, not its statutory core. What came in carries most of what changed
here: one complete German unit-linked *Bedingungswerk* read end to end, DEVK's 195-page
*Kundeninformation* with its *Tarifbestimmungen*, its *Rechnungsgrundlagen* and sixteen
*Basisinformationsblätter* [S2] [S15]; the statutory core as canonical XML from
`gesetze-im-internet.de` with each instrument's amendment status (`Stand`) recorded — the VVG,
the DeckRV, the MindZV, the VAG and the EStG [R1] [R12] [R14] [R15] [R20], the VVG-InfoV in HTML
beside them [R7]; and BaFin's *Merkblatt* and cost survey [R10] [R11] with the DAV's PRIIPs
*Ergebnisbericht* [R18]. What did not come in is the rest of the carrier sweep: for ten named
carriers no address for a *Bedingungswerk* was ever established, the one HDI address tried is a
soft 404, the DAV tables are not public, and the PRIIPs Regulation, the LVRG, the rating studies,
the GDV statistics and the BGH line were never opened. **Where an entry says `Retrieved: yes`,
treat the claim it carries as sound; where it does not, the citation is still a pointer, not a
certificate** — it names the instrument a claim should be checked against, not one anybody
checked. Re-verification was not a formality: it contradicted the death table this document
names, reversed the PRIIPs category, and put a real guaranteed *Rentenfaktor* below the one
modelled, each correction marked where it stands. The **mechanics** below are common ground in
German practice, several of them now read in a real wording, and are written without hedging; the
**levels** are almost entirely **[std]** still, because outside the one carrier that could be
read not one *Abschlusskostenquote*, not one *Verwaltungskostensatz*, not one *Stückkosten*
amount, not one *Effektivkostenquote* and not one *Rentenfaktor* was established at any carrier.

Out of scope: **hybrid and guarantee designs** (*statische* and *dynamische Hybride*, *Zwei-* und
*Drei-Topf-Hybride*, i-CPPI, *Wertsicherungsfonds*), discussed but deliberately not specified
(see *Riders and options*); **indexgebundene Rentenversicherung** (delib `indexpolice`); the
**fondsgebundene Basisrente** and **Riester-Rente** (delib `basisrente`, `riester_rente`); the
**payout phase** (delib `sofortrente`); and **bAV** in all its forms.

---

## Product overview and market role

A *fondsgebundene Rentenversicherung* is a **deferred private annuity whose accumulating value is
a holding of units in investment funds chosen by the policyholder**. The insurer administers the
contract, bears the biometric risk and gives one financial guarantee — the *Rentenfaktor* — but
does not guarantee the value of the fund holding at any point before *Rentenbeginn* [S1]. The
defining sentence, which every German wording expresses in some form, is that **the insurer
guarantees the number of *Anteileinheiten*, not their value**, and everything else follows from
it: no *Rechnungszins* in the accumulation phase, no *Deckungskapital* in the general-account
sense, no *Zinsüberschuss*, no *Bewertungsreserven* worth speaking of, and no investment mismatch
between the insurer's assets and its unit liability, because the VAG requires a separate
*Anlagestock* — a ring-fenced section of the *Sicherungsvermögen* — for each *Anlageart* backing
unit-linked benefits [R15] [REG-R7].

Four consequences distinguish the German chassis from its French, British and American siblings,
and each changes the shape of the projected cash flows:

1. **The charge stack is the product.** A contract with no *Rechnungszins* has nowhere to hide its
   charges, and PRIIPs and the *VVG-Informationspflichtenverordnung* force them onto one page: the
   *einkalkulierte Abschlusskosten* must be disclosed **in euro and as a single total amount**, the
   other costs separately as a share of the annual premium, and the ***Effektivkosten*** — the
   statute's own term, defined in § 2 Abs. 1 Nr. 9 VVG-InfoV as *"die Minderung der Wertentwicklung
   durch Kosten in Prozentpunkten … bis zum Beginn der Auszahlungsphase"* and computed under
   Abs. 6 *"wie der Gesamtkostenindikator nach Anhang VI der Delegierten Verordnung (EU)
   2017/653"* — must be given before conclusion [R7] [REG-R31]. That last cross-reference is what
   makes **the fund's own costs part of the disclosed figure**, and BaFin says so in terms:
   *"Die Fondsmanagementgebühren … gehören zwar zu den Effektivkosten"*, though not to the
   *einkalkulierte Abschlusskosten* [R11]. The requirement is understood to date from 1 January
   2015 with the LVRG `[unverified]` — the date is not in the regulation's text. The first-order
   economics are *fund return minus charges*.
2. **The acquisition charge has a statutory cap, and a shape the market takes from the statute
   rather than one the statute imposes here.** § 4 Abs. 1 Satz 2 DeckRV caps the acquisition cost
   financed against future premiums: *"Der Zillmersatz darf 25 Promille der Summe aller Prämien
   nicht überschreiten"* — 2,5 % of what this document calls the *Beitragssumme*, cut from 40 ‰ by
   the LVRG 2014 `[unverified]` [R12] [R13] [REG-R16] [REG-R20]. The **even spreading over the
   first five contract years is § 169 Abs. 3 VVG**, and Abs. 3 governs the *Deckungskapital*
   branch; it reaches a pure unit-linked contract only through Abs. 4's closing words *"im Übrigen
   gilt Absatz 3"*, that is, to the extent a benefit is guaranteed [R1] [REG-R28]. German tariffs
   nonetheless implement the five-year shape, and one does so in terms [S2]. **What that same
   wording shows is that the shape is not a cliff.** DEVK splits its acquisition cost in two:
   *"einen Teil … in gleichmäßigen Beträgen über einen Zeitraum von fünf Jahren"* and *"[d]en
   anderen Teil … als Prozentsatz während der gesamten Beitragszahlungsdauer"*. This document's
   composite carries one five-year instalment and calls the whole-term percentage
   *beitragsbezogene Verwaltungskosten*; the arithmetic of the premium deduction is the same, the
   label is not, and a reader comparing a delib run with a real *Kostenverrechnung* clause should
   expect the split to be drawn in a different place.
3. **The surrender value is the fund, and nothing else.** § 169 Abs. 4 VVG sends *fondsgebundene
   Versicherungen* to a ***Zeitwert*** rather than a *Deckungskapital* [R1] [REG-R28], and for a
   pure unit-linked contract the *Zeitwert* is the *Fondsguthaben*: no discounting, no mortality
   basis, no *Rechnungszins*, no *Zillmerung* residue, no second-basis *Mindestrückkaufswert*.
   A real wording states it as flatly as the statute does — *"Der Rückkaufswert ist das zum
   Kündigungstermin vorhandene Fondsguthaben"* [S2].
4. **The only guarantee is about the conversion terms, not about the pension.** On a classic
   contract both the capital and the annuity factor are guaranteed, so the annuity is guaranteed.
   Here **only the factor is** — the capital it multiplies is the market's. Any product document
   implying otherwise is wrong, and this is the sentence a specification has to carry [R22].

**Market role.** This **is** the dominant German new-business savings form, and the supervisor says
so: BaFin's *Risiken im Fokus 2026* describes *"die im Neugeschäft dominierenden fondsgebundenen
Produkte"* and sizes the family at about **59 million** *kapitalbildende* contracts in force in
2024, of which **2,4 million** were written that year [R11]. The `[unverified]` tag that stood on
that claim is withdrawn. **No GDV split by *Versicherungsart* was obtained, so no market-share
percentage appears anywhere in this document** [R25] [REG-R53].

The *Höchstrechnungszins* is a large part of the reason. § 2 Abs. 1 DeckRV is written for
*"Versicherungsverträgen **mit Zinsgarantie**"* and sets the rate at **1 Prozent** [R12]
[REG-R14] [REG-R15] — it was 0,25 % through the low-interest decade and is understood to have
been raised with effect from 1 January 2025 `[unverified]`, the commencement date being in the
amending *Verordnung* and not in the DeckRV text. Because the section is confined to
guaranteed-interest contracts, it **has no purchase at all on the accumulation phase of a pure
fondsgebundene contract**, there being no *Zinsgarantie* to cap. It reaches this product only
through the *Rentenfaktor* and through hybrid designs whose guaranteed pot sits in the general
account — and even there an insurer may use less than the maximum: DEVK calculates its guaranteed
*Rentenfaktoren* at **0,0 %** and its other guaranteed obligations at **0,25 %** [S2]. That
asymmetry is what let unit-linked new business grow while classic new business collapsed, and it
is corroborated at the level of market structure by **Debeka, Germany's largest life mutual by
policy count, discontinuing its classic annuity tariff** [S14].

**The supervisor is watching the charge level, and there are now numbers.** BaFin's *Merkblatt
01/2023 (VA)* of 8 May 2023 requires *kapitalbildende Lebensversicherungsprodukte* to offer an
***angemessener Kundennutzen***; requires the manufacturer to formulate a ***Renditeziel*** and to
show with *"geeigneten stochastischen Analysen"* that it is met *"mit hinreichender
Wahrscheinlichkeit"*, targeting for a retirement product a return above a justified inflation
expectation — *"realer Anlageerfolg"*; and warns that a large *Stückkosten* charge expressed as an
absolute euro amount makes the *Effektivkosten* vary sharply with premium size [R10] [REG-R35].
The finding that *Effektivkosten* differ considerably **between providers and products** belongs
not to the *Merkblatt* but to the supervisor's cost surveys [R11], and those surveys supply what
this document previously said did not exist:

- for an **entry age of 37 and a 30-year term — this document's own anchor cell** — the most-sold
  fondsgebundene products showed *Effektivkosten* of **1,90 % weighted mean**, with quartiles at
  **1,30 % / 1,64 % / 2,35 %** (2022 survey, first-half-2021 new business);
- *Effektivkosten* rise as the term shortens, and lie *"signifikant über den Werten der
  klassischen Lebensversicherung"*;
- at **every** age-and-term combination there were insurers above **4 %**;
- a repeat survey in 2025 found them falling since 2021, by more than **0,4 percentage points** in
  the upper quartile at the long, high-volume terms.

The charge stack below is therefore a **supervised** parameter presented as a design decision —
but it is no longer a design decision without a benchmark, and where it is compared with one the
comparison is made explicitly rather than avoided.

---

## Representative specification

The representative design is a **pure fondsgebundene Rentenversicherung with no
*Beitragsgarantie***: single life, *Schicht 3* (unsubsidised private provision), monthly
*Beitrag*, one fund, an *Aufschubzeit* ending at a contractually fixed *Rentenbeginn*, a
*Beitragsrückgewähr* death benefit, a guaranteed *Rentenfaktor* applied as the higher of the
guaranteed and the current factor, a *Rückkaufswert* equal to the *Fondsguthaben* with no
*Stornoabzug*, and *Fondswechsel*, *Zuzahlung*, *Teilentnahme*, *Ablaufmanagement* and
*Beitragsfreistellung* as switchable options.

**Why that design and not another**, in four arguments — arguments rather than observations,
because no carrier-level observation was available:

1. **No guarantee**, because the guarantee technologies of the German market cannot be
   demonstrated honestly in a deterministic projection (see *Riders and options*), and because
   the guarantee-free form is a real and growing market form rather than a simplification of the
   only form sold [S7] [S8] [S9].
2. ***Beitragsrückgewähr* death benefit**, because it is the only death-benefit shape with
   corroboration anywhere in the delib corpus [S2] and the shape that makes the *Risikobeitrag*
   mechanic non-trivial without making it dominant: the net amount at risk is positive early and
   vanishes later, so the model must recompute it every month rather than once.
3. **Acquisition charge at the statutory cap, spread over five years**, because the cap [R12]
   [REG-R16] and the spreading [R1] [REG-R28] are the two acquisition-cost facts with any
   corroboration, and a reference implementation should demonstrate the binding constraint rather
   than an unsourced interior point.
4. **A derived rather than a quoted *Rentenfaktor***, because no market level exists anywhere in
   this corpus and a quoted one would be an invention; the derivation below, from a 0 %
   *Rechnungszins* [S10] and a generational annuitant table [R16] [REG-R49], is checkable
   arithmetic labelled **[std]** at every appearance.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Fondsgebundene Rentenversicherung, deferred, single life, *Schicht 3*; no *Beitragsgarantie*; unit-linked accumulation converted at *Rentenbeginn* | [S1] [S2] [S3]; design **[std]** (1) |
| *Versicherungssparte* | ***Fondsgebundene Lebensversicherung***, Nr. 21 of Anlage 1 VAG, a *Sparte* in its own right, with a segregated *Anlagestock* — a division **of** the *Sicherungsvermögen* under § 125 Abs. 5 VAG | [R15] [REG-R5] [REG-R7] |
| Legal wrapper | Individual contract on the applicant's own life; the *Versicherungsnehmer* and the *versicherte Person* coincide | [S1] |
| Premium form (model-point parameter) | (i) `laufend` — level recurring *Beitrag*, the dominant form; (ii) `einmal` — *Einmalbeitrag* | (i) [S1] [S2]; (ii) **[std]** (2) |
| Payment frequency | Monthly, quarterly, half-yearly or annual; monthly by *SEPA-Lastschrift* is the dominant mode | [S1]; dominance `[unverified]` |
| Entry ages | 18 to 60 | envelope **[std]** (3) |
| *Rentenbeginn* age | 67; the contract may fix any age from 62 to 85 | **62 to 85 confirmed at one carrier** [S2]; tax floor 62 [R20] [REG-R45]; choice **[std]** (4) |
| Minimum *Aufschubzeit* | 12 years, so the contract can reach the § 20 EStG twelve-year threshold | [R20] [REG-R45]; level **[std]** (4) — a real tariff's own minimum is **10 years** [S2] |
| Minimum premium | 25,00 EUR per month, or 5,000.00 EUR as an *Einmalbeitrag* | monthly minimum **confirmed at 25 €** [S2]; single-premium minimum **[std]** and higher than the 1 500 € observed there (3) |
| Age basis | Age last birthday at inception, stepping at each policy anniversary | **[std]** (5) |
| Fund range | One fund in the reference implementation | one fund **[std]** (6). The "50–300 funds" range this document previously asserted is `[unverified]` and is **not** what the one readable tariff offers: **nine** funds from a single house, at least 10 % each, at most five per contract [S2]. Large carriers do offer wide menus including ETFs [S3] |
| *Anteilspreis* and *Bewertungsstichtag* | Units bought and cancelled at the fund's *Rücknahmepreis* (redemption price), the *Ausgabeaufschlag* waived in full, at the month boundary — on a monthly grid the dealing-lag convention disappears | **both limbs confirmed** [S2]: units bought at *"der zum Stichtag … des Monats der Beitragsfälligkeit festgestellte Rücknahmepreis"*, and *"Ausgabeaufschläge und Depotkosten fallen nicht an"*. Grid **[std]** (7) |
| Anchor model cell | Entry age 37, *Rentenbeginn* 67, monthly *Beitrag* 200,00 €, premium term 30 years, *Beitragsrückgewähr*, no options | **[std]** (8) |

Footnotes to **[std]** rows:

1. **One German fondsgebundene *Bedingungswerk* has now been read in full, with its
   *Basisinformationsblätter*** — DEVK's *Kundeninformation* 03101/07/2024 for tariff L/N FR1,
   "DEVK-Fondsrente vario" [S2] [S15]. Its identity row reads *"Fondsgebundene Rentenversicherung
   mit aufgeschobener Rentenzahlung, Beitragsrückgewähr im Todesfall und Kapitaloption"*, which is
   this composite's design almost word for word. **The identity row below still states the product
   class, not that carrier's tariff**: nothing here is DEVK's, and where a DEVK level is quoted it
   is labelled as an observation at one carrier rather than adopted. That a market-standard clause
   inventory exists — the GDV publishes *Musterbedingungen* from which member insurers derive
   their AVB — remains the reason wordings are structurally interchangeable and remains
   `[unverified]`, since only one wording was read [S1] [R23] [REG-R37].
2. The *Einmalbeitrag* form isolates the acquisition-charge mechanic: with no future premiums
   there is nothing to zillmer against, the five-year spread has no work to do, and the whole
   charge falls at inception, at the *Zuzahlungskosten* rate **[std]**.
3. **One envelope is now established, at one carrier.** DEVK's *Tarifbestimmungen* give a minimum
   premium of **25 € monthly, 300 € annual, 1 500 € single** and a *Mindestrente* of 50 € a month
   below which the contract pays a *Kapitalabfindung* instead [S2]. The composite's 25 € monthly
   minimum matches; its 5 000 € single-premium minimum is **[std]** and more than three times the
   observed one. **No entry-age envelope was established anywhere** — entry ages of roughly
   15/18 to the low 60s remain `[unverified]`, and the composite's 18–60 takes the wide end, with
   a model point at entry age 60 and a two-year deferment exercising the boundary.
4. *Rentenbeginn* at 67 matches the *Regelaltersgrenze*, and the **62-to-85 window is confirmed**:
   DEVK's tariff gives *"Rentenbeginn frühester 62 Jahre, spätester 85 Jahre"* [S2]. 62 is a
   **tax** floor rather than a product floor: EStG § 20 Abs. 1 Nr. 6 Satz 2 as enacted names the
   **60th** year of life, and § 52 Abs. 28 raises it — *"Absatz 1 Nummer 6 Satz 2 ist für
   Vertragsabschlüsse nach dem 31. Dezember 2011 mit der Maßgabe anzuwenden, dass die
   Versicherungsleistung nach Vollendung des 62. Lebensjahres des Steuerpflichtigen ausgezahlt
   wird"* — together with a term of at least twelve years [R20] [REG-R45]. **A model point whose
   configuration could not satisfy that test would not be representative of a real sold
   contract**, which is why the minimum deferment is set at twelve years; a real tariff's own
   minimum is ten [S2], so the composite is the stricter of the two and for a stated reason.
5. **No age basis was established for any carrier.** Age last birthday is the convention the
   shipped mortality proxy is indexed on; on a monthly grid the difference from age next birthday
   is a twelve-month shift of one lookup, quantified in the technical notes.
6. Real *Fondsauswahl* menus vary far more widely than this document once claimed. A large carrier
   offers a *"TopFonds-Universum"* of managed strategies, single funds and ETFs [S3]; the one
   tariff whose conditions could be read offers **nine** funds from a single house, with a minimum
   holding of 10 % per fund and at most five funds per contract at application [S2]. With a
   deterministic return a multi-fund split is arithmetically identical to one composite fund at
   the weighted return, so the composite carries **one fund** and represents *Fondswechsel* and
   *Ablaufmanagement* as changes to the assumed return rather than as reallocations. The
   consequence — the model cannot show dispersion between funds — is a listed model risk.
7. **Both conventions are now confirmed at one carrier.** Units are bought at the *Rücknahmepreis*
   — § 14 Abs. 1 AVB — and the *Verbraucherinformation* says outright *"Ausgabeaufschläge und
   Depotkosten fallen nicht an"* [S2]. The *Bewertungsstichtag* convention is more elaborate than
   the composite's single month boundary: DEVK uses the last published price of the preceding
   month at *Rentenbeginn*, the last published price of the month of request on surrender or
   partial withdrawal, the **third** published price after notification of a death, the third
   after a *Fondsshift*, the **fifth** of the month for everything else, and Xetra closing prices
   for ETFs. On a monthly grid those distinctions are immaterial; on a daily one none of them is.
8. Entry age 37 with a 30-year deferment and a 200,00 € monthly *Beitrag* makes the
   *Beitragssumme* exactly 72 000,00 €, the acquisition charge at the statutory cap exactly
   1 800,00 €, and the five-year instalment exactly **30,00 € per month — 15 % of each of the
   first 60 premiums**. The shape of the product is then legible in round numbers and the cliff
   at month 60 is exact.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| *Beitrag* | 200,00 EUR per month, level, payable for 30 years to *Rentenbeginn* | **[std]** (8) |
| *Beitragssumme* | `Beitrag × (12 / prem_mode_months) × premium term` = 72,000.00 EUR — the sum of all premiums **payable**, not paid | definition [R12] [REG-R16] |
| Premium timing | In advance, at the start of each payment period | **[std]** (9) |
| *Ratenzahlungszuschlag* | A loading for paying more often than annually; the composite reads the **instalment stated in the policy** and does not re-apply a loading | mechanic [S1]; level `[unverified]`; treatment **[std]** (9) |
| Premium-paying term | Equal to the *Aufschubzeit* in the base case; a shorter term is permitted and shortens the acquisition-charge spread | **[std]** (10) |
| *Beitragsdynamik* | Optional annual increase of the *Beitrag*; individual increases may normally be declined | mechanic [S1] [S6]; **a real menu is a fixed whole percentage between 3 % and 10 % of the previous year's premium** [S2]; base run 0 % **[std]** (11) |
| *Zuzahlung* | Additional single premium into an existing contract, minimum 500,00 EUR, subject to its own acquisition charge; raises the *Beitragssumme* | mechanic [S6]; **the 500,00 € minimum is confirmed** [S2], the maximum there being set by the board; charge rate **[std]** (12) |
| Premium cessation | On death, on *Storno*, on *Beitragsfreistellung* and at *Rentenbeginn* | [S1] [R3] [REG-R28] |
| Non-payment path | *Mahnung* and, on continued default, conversion to a *beitragsfreie Versicherung* rather than termination, because the contract has a positive value from the first month | [R3] [REG-R28]; treatment **[std]** (13) |

9. Premiums in advance is the German norm and the only convention under which the
   *Beitragsverrechnung* below makes sense: the deductions are taken from a premium that has
   arrived. The *Ratenzahlungszuschlag* is real — German tariffs price an annual premium below
   twelve monthly ones — but **no level was established at any carrier**, the plausible band
   being 0–5 % of the annualised premium. Rather than invent one, the composite treats the model
   point's premium as the **instalment the policy states**, which already contains whatever
   loading the tariff applied. Applying a further loading to it is a listed pitfall.
10. A premium term shorter than the deferment exposes an edge in the statutory spreading rule:
    where it is shorter than five years there are fewer than sixty premiums to spread the
    acquisition charge over. The composite spreads it over `min(60, premium term in months)`
    instalments **[std]**, so the charge is fully taken and no instalment is charged against a
    premium that is not paid.
11. Real tariffs **re-zillmer each accepted increment over its own sixty months**, because an
    increment is optional and cannot be assumed at inception. The composite therefore fixes the
    *Beitragssumme* and the acquisition charge **on the initial premium level**; the direction of
    the bias — the acquisition charge on a dynamic contract is understated — is stated in the
    technical notes.
12. The **500,00 € *Zuzahlung* minimum is confirmed** at one carrier, where the maximum is fixed
    by the board and *Zuzahlungen* are barred inside the *Abrufphase* [S2]. The 2,5 % charge is
    still **[std]**, though its *shape* is confirmed: on a *Zuzahlung*, as on an *Einmalbeitrag*,
    *"entnehmen wir alle Abschluss- und Vertriebskosten sofort dem Beitrag oder der Zuzahlung"*.
13. § 165 Abs. 1 VVG gives the right to demand a *prämienfreie Versicherung* *"jederzeit für den
    Schluss der laufenden Versicherungsperiode … sofern die dafür vereinbarte
    Mindestversicherungsleistung erreicht wird"*, and where it is not, *"hat der Versicherer den
    auf die Versicherung entfallenden Rückkaufswert … nach § 169 zu zahlen"* [R3] [REG-R28]. On a
    unit-linked contract the conversion is trivial — nothing is recomputed, the units stay — so
    the composite routes non-payment to *Beitragsfreistellung* rather than to surrender, which is
    both the statutory default and the economically correct one. **The minimum is statutory in
    kind and contractual in level**, disclosed under § 2 Abs. 1 Nr. 5 VVG-InfoV [R7]; at one
    carrier it is a **minimum *Fondsguthaben* of 2 500 €**, below which the contract is surrendered
    instead [S2]. **The composite carries none**, which understates the decay of small paid-up
    policies by keeping alive contracts a real insurer would close.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Benefit at *Rentenbeginn* | A lifelong monthly annuity, `Fondsguthaben / 10 000 × Rentenfaktor` | [R22]; **the definition confirmed at a carrier** [S2]; factor level **[std]** (14) |
| *Rentenfaktor* rule | `max(garantierter Rentenfaktor, aktueller Rentenfaktor am Rentenbeginn)` — a guarantee **with upside** | **read verbatim in a fondsgebundene AVB** [S2]: *"Der tatsächliche Rentenfaktor ist der höhere Wert aus dem zu Rentenbeginn aktuellen Rentenfaktor und dem zu Vertragsbeginn garantierten Rentenfaktor."* Also [S4] [R22] |
| *Garantierter Rentenfaktor* | 25,00 EUR per month per 10 000 EUR of *Fondsguthaben* at age 67 | **[std]**, derived — and now checkable: a real tariff's guaranteed factor at *Rentenbeginn* 67 is **25,22 / 24,12 / 22,91 / 21,83 €** at deferments of 12 / 20 / 30 / 40 years [S15] (14) |
| Conversion basis | A recognised mortality table — DAV 2004 R, generational, unisex — at an underlying interest rate of 0 % p.a. | **established for a fondsgebundene tariff** [S2]: *"bei der Kalkulation der zu Vertragsbeginn garantierten Rentenfaktoren … einen Zinssatz von 0,0 Prozent"*, on *"Sterbetafel DAV 2004 R"*. Also [S10] [R16] [REG-R49] |
| *Rentengarantiezeit* | 10 years, not priced as a separate option in the composite | mechanic [S1]; **a real menu runs 5 to 25 years with a maximum end age of 87** [S2]; the 0/5/10/15 menu this document previously gave is withdrawn; choice **[std]** |
| *Kapitalwahlrecht* | The *Fondsguthaben* may be taken as a lump sum at *Rentenbeginn* instead of the annuity, on notice | mechanic [S1] [R20]; **notice period six months before the first annuity due date, with partial payments of up to 30 % available up to *Rentenbeginn*** [S2]; take-up **[std]** (15) |
| *Todesfallleistung* before *Rentenbeginn* | `max(Fondsguthaben, Summe der gezahlten Beiträge)` — the *Beitragsrückgewähr* form | **read verbatim** [S2] § 2 Abs. 7. That clause adds a rule the composite does not carry: a *Teilentnahme* reduces the *Beitragsrückgewähr* floor by the amount withdrawn |
| Alternative death-benefit shapes | (i) *Fondsguthaben* alone; (ii) 100/105/110 % of the *Fondsguthaben*; (iii) a *garantierte Mindesttodesfallleistung* fixed at issue | (i)–(iii) mechanic [S1]; percentages `[unverified]`; all four carried as a model-point parameter. **The one wording read offers only the *Beitragsrückgewähr* form before *Rentenbeginn*** and puts its menu in the payout phase instead — *Rentengarantiezeit*, *Kapitalrückgewähr im Rentenbezug*, or none [S2] |
| *Risikobeitrag* | Levied monthly by cancelling units, on the *riskiertes Kapital* = `max(Todesfallleistung − Fondsguthaben, 0)`, priced on a **death** table | **mechanic confirmed** [S2] § 14 Abs. 1: the *Risikobeiträge* are taken from the *Fondsguthaben* at the start of each month, *"nach den anerkannten Regeln der Versicherungsmathematik berechnet"*. Basis DAV 2008 T [R17] [REG-R48] — **but see footnote 17: the one carrier that could be checked uses 65 % of DAV 1994 T**; level **[std]** |
| *Überschussbeteiligung* | Arises from the *Risikoergebnis* and the *übrige Ergebnis* only; credited as additional units, as a charge reduction or as a *Schlussüberschuss* | [R5] [R14] [REG-R9] [REG-R18]; **not projected** (16) |

14. **This is the single most consequential [std] in the document. It was derived rather than
    guessed, and it can now be marked.** The derivation: at a *Rechnungszins* of **0 %** a monthly
    annuity of `R` per 10 000 € payable for an expected `T` years has a present value of
    `12 × T × R` per 10 000 €, so the pre-cost factor is `10 000 / (12 × T)`. On a
    **generational** annuitant table [R16] [REG-R49] a 67-year-old of a cohort now in mid-career
    has an expected annuity duration materially longer than a period table implies; `T` of 25 to
    28 years gives a pre-cost factor between **29,8 and 33,3**. Deducting the payout-phase
    administration charge and a margin for the *Sicherheitsabschlag* and the *Rentengarantiezeit*
    brings the guaranteed factor below that, and the composite takes **25,00 €**.
    **The 0 % *Rechnungszins* is now established for a fondsgebundene tariff** rather than
    transferred from a classic one: DEVK states it in its *Versicherungsmathematische Hinweise*,
    on DAV 2004 R, and calculates its other guaranteed obligations at 0,25 % instead [S2].
    **And the answer is now available.** For the *same* configuration as this document's anchor
    cell — a 37-year-old, 30 annual instalments, *Rentenbeginn* at 67 — that carrier's guaranteed
    *Rentenfaktor* is **22,91 €** per 10 000 €, against the composite's 25,00 € [S15]. The
    composite is therefore **about 9 % generous** at the anchor cell. It is close at short
    deferments and generous at long ones, because the carrier's factor falls with the deferment —
    **25,22 / 24,12 / 22,91 / 21,83 €** at 12 / 20 / 30 / 40 years, all at *Rentenbeginn* 67 —
    which is the generational table showing through: a later birth cohort lives longer at 67. The
    composite's factor varies with the ***Rentenbeginn* age only**, not with the deferment, so it
    reproduces the level roughly and the *gradient* not at all. **That is a model fact and it is
    not changed here**: `rentenfaktor_table.csv`, the worked example and the golden tests move
    together or not at all, and moving them is a decision to take deliberately. Read the other
    way, 25,00 at a 0 % *Rechnungszins* prices the guarantee as though the insurer will hold the
    capital for **33⅓ years** and earn nothing on it — and the market's own answer at the same
    cell is 36⅜ years. Consumer sources use 25 illustratively [R22]; that coincidence was luck,
    and it should no longer be offered as support.
15. **No *Kapitalwahlrecht* take-up rate was established anywhere**, and it is the largest
    behavioural unknown in the product, because the two tax regimes genuinely differ. The base
    run takes the **annuity** with a take-up of 0 % **[std]**, so that the *Rentenfaktor* — the
    only guarantee the contract carries — is the thing the worked example demonstrates. It is not
    an estimate of behaviour and must not be read as one.
16. The investment result belongs to the policyholder by construction, so it never enters the
    insurer's *Rohüberschuss* — and the MindZV says so in its own definition, computing the
    creditable investment income *"ohne die der Lebensversicherung für Rechnung und Risiko der
    Versicherungsnehmer zuzuordnenden Erträge und Aufwendungen"* (§ 3 Abs. 1) [R14] [REG-R18].
    The *Bewertungsreserven* limb of § 153 VVG has nothing to attach to before *Rentenbeginn*, and
    a real wording states it flatly: *"Vor Rentenbeginn entstehen bei der Fondsgebundenen
    Rentenversicherung keine Bewertungsreserven"* [S2] [R5] [REG-R9]. **The MindZV percentages are
    now established** and the tag is removed: 90 % of the *Risikoergebnis* (§ 7), 50 % of the
    *übriges Ergebnis* (§ 8). **And a crediting mechanism is now confirmed at a carrier**, which
    this footnote previously said was not: DEVK pays a premium-paying contract a
    ***Grundüberschussanteil*** *"in Prozent des überschussberechtigten Beitrags"*, converted into
    units and added to the *Fondsguthaben*, while *"[b]eitragsfreie Versicherungen und
    Versicherungen gegen Einmalbeitrag sind vor Rentenbeginn nicht überschussberechtigt"* [S2].
    **No declared rate was established.** Two facts justify continuing to omit the credit rather
    than guessing it: a paid-up contract — model point 7 — would receive nothing anyway, and BaFin
    found in 2025 that *"mehr als die Hälfte der Lebensversicherer … keine
    Risikoüberschussbeteiligung deklariert hat"* [R11]. The composite omits the credit and records
    the bias: omitting it understates the projected *Fondsguthaben*, the honest direction for a
    charge demonstration.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Medical evidence | None on the representative design. A *Beitragsrückgewähr* death benefit puts almost no capital at risk, so a *Gesundheitsprüfung* is not normally required | mechanic [S1]; **[std]** (17) |
| When underwriting appears | Where the death benefit is a *garantierte Mindesttodesfallleistung* or a percentage of the fund materially above 100 %, the excess is death cover and is underwritten | mechanic [S1]; thresholds `[unverified]` |
| Rating factors | Attained age (through the *Risikobeitrag*) and the *Rentenbeginn* age (through the *Rentenfaktor*). **Sex may not be one** | [REG-R34]; [R16] [R17] |
| Occupation, smoker | Not rating factors on a savings tariff | **[std]** |
| Mortality basis for the death charge | A **death** table, first order, unisex — *not* the annuity table. DAV 2008 T is the modern one; the one tariff that could be read prices the *Risikobeitrag* on **65 % of DAV 1994 T** instead | [R17] [REG-R48]; [S2] for the observed basis (17) |
| Mortality basis for the *Rentenfaktor* | **DAV 2004 R**, generational, first order, unisex | **confirmed for a fondsgebundene tariff** [S2]; [R16] [S10] [REG-R49] (17) |
| Best-estimate basis | The second-order versions of the same tables; the wedge between first and second order **is** the *Risikoergebnis* | [REG-R47]; levels **[std]** (18) |

17. **A German FRV carries two mortality bases at once**, and this is where they meet. The
    direction of prudence forks — a death cover is loaded by assuming mortality **higher** than
    expected, an annuity by assuming it **lower** and improving **faster** [REG-R47] — so **a
    model that uses one table for both misprices one of them**. **This is no longer an inference:
    an AVB confirming it has now been read.** DEVK's *Versicherungsmathematische Hinweise* name
    *"für die Rentenleistungen der Fondsgebundenen Rentenversicherung Sterbetafel DAV 2004 R"* and,
    separately, price the *Risikobeiträge* on *"einer mit 65 Prozent gewichteten
    geschlechtsunabhängigen Ausscheideordnung auf Basis der Sterbetafel DAV 1994 T"* [S2].
    **But the death table this document names is contradicted there.** DEVK reserves DAV 2008 T
    for its underwritten *Risiko-Zusatzversicherung* and uses a scaled-down DAV 1994 T for the
    savings contract's own risk charge. Two lessons the specification should carry: on a
    *Beitragsrückgewähr* cover with no underwriting, "first order" can mean **an old heavy table
    scaled down** rather than a modern table loaded up; and the tariff basis is **unisex**, which
    is [REG-R34] showing in a real *Rechnungsgrundlage*. `mort_table.csv` is unaffected — it is a
    proxy for a first-order death basis, whichever table a given carrier starts from.
18. **DAV tables are the property of the Deutsche Aktuarvereinigung, are not public and are not
    redistributed by this library.** They are cited by name; the reference implementation ships
    **[std]** proxies with their anchors stated, and the technical notes say what a replacement
    must preserve — for DAV 2008 T an insured-lives death basis with selection and **no**
    projected improvement, for DAV 2004 R a generational basis with safety in **both** level and
    trend [REG-R47] [REG-R48] [REG-R49].

### Charges

**This is the most important table in the specification, and every level in it is still [std].**
The **structure** is German market practice and is now read in a real wording rather than
asserted [S2]. The **levels** are a design decision — but for the first time they can be set
beside observed ones, and the honest thing is to print the comparison rather than to keep saying
nothing exists.

**What one real tariff charges.** The *Basisinformationsblätter* for DEVK's L FR1 give, for a
1 000 € annual premium [S15]: *Abschluss- und Vertriebskosten* **2,50 % der kumulierten Anlage**;
*Verwaltungskosten* **0,42 % des Werts Ihrer Anlage pro Jahr**, **6,90 % der jeweils eingezahlten
Anlage**, and **18 EUR pro Jahr**; plus *Transaktionskosten* of 0,01 %–0,32 % p.a. and the funds'
own costs. Against that, the composite's `std_gross` carries 2,50 % / 0,30 % p.a. / 4,00 % /
3,00 € per month. **The composite's acquisition rate is the observed one exactly; its ongoing
charges are lighter across the board** — a fund charge about three-quarters of the observed one,
a premium charge under three-fifths, and a policy fee of 36 € a year against 18 €, the one line
where the composite is dearer. Every one of the observed levels falls inside the argued range in
the last column, which is the range doing the work it was built for.

**What the market charges in aggregate.** BaFin's survey puts the *Effektivkosten* of the
most-sold fondsgebundene products at **1,90 % weighted mean** at entry age 37 over 30 years — this
document's anchor cell — with quartiles at **1,30 / 1,64 / 2,35 %** and insurers above **4 %** at
every age-and-term combination [R11]. The DEVK sheet for the same 30-year cell reports a reduction
in yield of **1,4 %–3,4 % p.a.** depending on the chosen fund [S15]. **The composite's stack
implies roughly 1 % p.a.**, which is below the observed lower quartile: `std_gross` is a *cheap*
German unit-linked contract, not an average one, and any statement drawn from it should say so.
Nine of the ten remaining named carriers still supply no charge level of any kind [S3]–[S14]
[S16] [S18] [R23] [R24].

| Charge | German name | Base | Timing and mechanism | Composite level | Argued range |
|---|---|---|---|---|---|
| Acquisition | *Abschluss- und Vertriebskosten* (*Alpha-Kosten*) | *Beitragssumme* | withheld from the premium, spread evenly over the first 60 months | **2.50 %** of the *Beitragssumme* — 1,800.00 EUR, i.e. 30.00 EUR per month | 0 % (*Nettotarif*) to 2.5 % (the statutory cap) |
| Premium admin | *beitragsbezogene Verwaltungskosten* (*Beta-Kosten*) | each gross *Beitrag* | withheld from the premium, whole premium-paying term | **4.00 %** of each premium | 2 % to 10 % |
| Fund admin | *kapitalbezogene Verwaltungskosten* (*Gamma-Kosten*) | *Fondsguthaben* | monthly, by cancelling units | **0.30 % p.a.**, taken as 0.025 % per month | 0.10 % to 1.20 % p.a. |
| Policy fee | *Stückkosten* | per policy | monthly, by cancelling units | **3.00 EUR** per month | 0 to 5 EUR per month |
| Risk charge | *Risikobeitrag* | *riskiertes Kapital* | monthly, by cancelling units | `q_tariff(x)/12 × riskiertes Kapital`, DAV 2008 T proxy | a priced risk, not a load |
| Fund cost | *TER* (*Gesamtkostenquote*) | fund assets | continuously, **inside the unit price** | **0.45 % p.a.**, netted off the assumed gross return | 0.15 % (ETF) to 2.00 % p.a. (active) |
| Trail rebate | *Kickback* / *Bestandsprovision* | fund assets | credited to the *Fondsguthaben*, to the RfB, or retained, where credited at all | **0.00 % p.a.** | **0 % to over 1.20 % p.a. observed**; weighted mean just over 0.30 % p.a. of the *Fondsguthaben* on the third of new business that carries one [R11] |
| Top-up | *Zuzahlungskosten* | each *Zuzahlung* | withheld on receipt | **2.50 %** of the *Zuzahlung* | 0 % to 4 % |
| Fund switch | *Fondswechselgebühr* | per switch beyond a free allowance | on election | **0.00 EUR** (allowance not exhausted) | 0 to 25 EUR |
| Surrender | *Stornoabzug* | *Fondsguthaben* | on *Kündigung* | **0.00 %** | must be *vereinbart*, *beziffert* and *angemessen*. **A real one is a flat euro amount, not a percentage**: 150 € on *Kündigung*, on full *Beitragsfreistellung* and on an early *Rentenbeginn*, waived in the *Abrufphase* and on an already paid-up contract [S2] |
| Annuity admin | *Rentenbezugskosten* | each annuity payment | in payment — **out of scope**, delib `sofortrente` | 1.5 % of each payment | 0 % to 3 % |

**The acquisition charge is the one charge whose level has a real anchor, the composite takes the
cap, and the market appears to take it too.** § 4 Abs. 1 Satz 2 DeckRV: *"Der Zillmersatz darf 25
Promille der Summe aller Prämien nicht überschreiten"*, and Abs. 4 fixes the rate used at
conclusion for the whole term [R12] [REG-R16]; the cut from 40 ‰ and its 1 January 2015
commencement are `[unverified]` and are not in the regulation's text [R13] [REG-R20]. The
composite takes **the cap as the level** because a reference implementation should demonstrate
the binding constraint rather than a guessed interior point — and the one tariff whose figure can
now be read charges **exactly 2,50 % der kumulierten Anlage** [S15], so the choice turns out to
describe the market rather than merely to bound it. A *Nettotarif* — the same contract with the
*Abschluss- und Vertriebskosten* removed and the adviser paid a fee under a separate
*Vergütungsvereinbarung* [S18] — is carried as a **charge variant on the same chassis**, not as a
separate product, and it brackets the range from below. One caution BaFin supplies: on a
*Nettoprodukt* the client's separate fee is a cost that *"nicht in die Effektivkosten
einfließen"* [R10], so a net-versus-gross comparison of the *published* figure overstates the
saving. delib's own `std_netto`-to-`std_gross` gap does not have that defect, because both are
computed on the same measure.

**The two *Verwaltungskosten* are named by their base, and the difference is load-bearing.**
*Beitragsbezogene* charges are a percentage of each gross premium and **stop when premiums
stop**. *Kapitalbezogene* charges are a percentage per annum of the *Fondsguthaben*, taken
monthly by cancelling units, and **continue after premiums stop** — they make a paid-up policy
decay, and in a long contract they dominate the *Effektivkosten* because they compound against
the whole accumulated fund.

**The fund's own TER is inside the unit price and is not a policy charge.** It never appears in
the policy ledger: a model that charges it explicitly double-counts, one that ignores it
overstates the policyholder's return, and the composite **nets it off the assumed gross return**,
which is exactly what it is. It does, however, enter the **disclosed** figure — *"Die
Fondsmanagementgebühren … gehören zwar zu den Effektivkosten"*, though not to the
*einkalkulierte Abschlusskosten* [R11] — which is why a real *Basisinformationsblatt* prints the
insurer's charges and the fund's costs in one column [S15].

**The *Kickback* is set to zero on a passive fund, and that is now a modelling choice rather than
a way round an open question.** Both questions this document listed as unresolved have answers.
BaFin's *Merkblatt* establishes that insurers do receive *Rückvergütungen* out of the fund's
*Verwaltungsvergütung*, that they must test whether the arrangement creates a *Fehlanreiz* to
steer clients into the funds that pay them most, and that they must consider passing the rebate
back — by reducing the calculated costs, by an RfB allocation above the MindZV minimum, by a
*Kostenüberschussanteil*, or by *"einen besonderen Überschussanteil zur Erstattung von
Rückvergütungen"* [R10] [R15] [REG-R33]. One carrier's answer is in its AVB:
*"Rückvergütungen, die wir von den Kapitalanlagegesellschaften erhalten, verwenden wir zur
Deckung etwaiger Verwaltungskostenverluste. Nicht benötigte Teile führen wir unter Beachtung der
Mindestzuführungsverordnung der Rückstellung für Beitragsrückerstattung zu"* [S2]. And the market
picture is quantified: rebates on about a third of new business, weighted mean **just over
0,30 % p.a. of the *Fondsguthaben*** and up to **over 1,20 %**, of which about 52 % is returned on
average through a special *Überschussanteil*, with a further 19 % of business carrying rebates
paid **straight to the intermediary** at about 0,50 % [R11]. **The composite's zero is therefore
not neutral — it models the cheap end of a real and material flow**, and how a credited rebate
enters the PRIIPs cost calculation is the one limb still unresolved [R7] [R8] [REG-R32].

**Commission is an expense, not a charge, and the composite sets it equal to the charge:**
acquisition commission of **2.50 % of the *Beitragssumme* at inception** — exactly the
acquisition charge it will recover over sixty months — plus a 200,00 € issue expense and renewal
commission of 1.5 % of each premium **[std]**. **No German commission scale was established at
any carrier.** The equality is deliberate: it makes the model demonstrate, in one number, the
financing problem the *Höchstzillmersatz* and the five-year spread exist to regulate.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| *Rückkaufswert* | The ***Zeitwert*** under § 169 **Abs. 4** VVG, which on a pure unit-linked contract **is the *Fondsguthaben*** | [R1] [REG-R28]; **and read in an AVB** [S2]: *"Der Rückkaufswert ist das zum Kündigungstermin vorhandene Fondsguthaben."* |
| *Stornoabzug* | **0.00 %.** Permissible under § 169 **Abs. 5** only if *vereinbart*, *beziffert* and *angemessen*; *"[d]ie Vereinbarung eines Abzugs für noch nicht getilgte Abschluss- und Vertriebskosten ist unwirksam"* | [R1] [REG-R28]; level **[std]** (19) |
| *Kündigung* | At any time for the end of the current *Versicherungsperiode* under § 168 Abs. 1 — on a monthly-premium contract, a short notice period rather than an annual one; a real tariff allows it *"jederzeit zum Schluss eines Monats"* [S2]. The right extends to single-premium contracts (Abs. 2) and is excluded only for pension-purpose contracts under Abs. 3, which this product is not | [R2] [REG-R28] |
| Early values | Poor, and **not because of a deduction**: at the composite's levels a contract surrendered in year 3 has had 15 % of every premium taken for acquisition plus the ongoing charges, so the *Rückkaufswert* is well below premiums paid even in a flat market | arithmetic on the [std] stack (20) |
| Protection for the policyholder | Sits **earlier**, in the *Beitragsverrechnung*: because the acquisition charge may only be taken over the first five years, units are bought from the first month and the value is positive from the start | [R1] [REG-R28] (20) |
| *Beitragsfreistellung* | Premiums stop, units stay, premium-based charges stop with the premium, fund-based charges and the *Risikobeitrag* continue by unit cancellation — so the contract **decays** | [R3] [REG-R28] |
| *Widerruf* | **30 days** — § 152 Abs. 1 VVG, *"[a]bweichend von § 8 Absatz 1 Satz 1 beträgt die Widerrufsfrist 30 Tage"*. The amount repayable is the *Rückkaufswert* under § 169 plus the unearned premium (Abs. 2); where the policyholder was not told cover had begun, it is that **or the first year's premiums if more favourable** (Abs. 3) — so it is *not* simply the unit value at cancellation, and after a market fall it can exceed it | [R6] [REG-R23]; **not projected** |
| *Teilentnahme* | A partial withdrawal during the *Aufschubzeit*, subject to a minimum and to a minimum remaining *Fondsguthaben* | mechanic and levels **confirmed at one carrier** [S2]: minimum 500 €, remaining fund at least 1 000 € (premium-paying) or 2 500 € (paid-up), a **40 €** fee waived in the *Abrufphase*, and the *Beitragsrückgewähr* floor reduced by the amount withdrawn. delib's levels **[std]**; the reduction of the death-benefit floor is **not modelled** |

19. The claim that **many unit-linked tariffs have no *Stornoabzug* at all** is `[unverified]`
    and the one tariff that could be read **does** have one. § 169 Abs. 5 VVG makes a deduction
    for unamortised acquisition costs ineffective, but it does not forbid a deduction as such,
    and the burden of proof it is often credited with is contractual rather than statutory —
    DEVK's own clause supplies it: *"Der Stornoabzug ist zulässig, wenn er vereinbart, beziffert
    und angemessen ist. Die Angemessenheit ist im Zweifel von uns nachzuweisen"*, justified by
    the change in the risk profile of the remaining portfolio, by collectively provided risk
    capital and by administration cost — never by unrecovered acquisition cost [S2] [R1]
    [REG-R28]. **The shape matters as much as the level**: DEVK's is a flat **150 €**, not a
    percentage of the fund, so it bites hardest on small contracts, exactly the pattern BaFin
    flags for absolute-euro charges [R10]. The composite's `stornoabzug_pp(t)` is a percentage
    and stays so; that is a model fact, not corrected here. **No BGH decision on *Rückkaufswert*,
    *Kostenverrechnung* or *Stornoabzug* is cited anywhere in this document** [R26] [REG-R36].
20. The relation between the *Zeitwert* branch and the five-year floor **is now readable in the
    statute**, and it favours the second of the two readings this footnote offered. § 169 Abs. 3
    carries the *"gleichmäßige[n] Verteilung der angesetzten Abschluss- und Vertriebskosten auf
    die ersten fünf Vertragsjahre"* as a minimum on the *Deckungskapital* branch; Abs. 4 sends a
    fondsgebundene contract to the *Zeitwert* *"soweit nicht der Versicherer eine bestimmte
    Leistung garantiert; im Übrigen gilt Absatz 3"*. On a contract with no guarantee there is
    therefore **no statutory floor to reach**, and the protection operates through the tariff:
    the *Kostenverrechnung* clause limits what may be withheld, so the units are bought from the
    first month and never have to be given back. That is what the market implements [S2] § 18
    Abs. 2 and what the composite models. **Both readings still produce the same numbers on this
    design**; what has changed is that the reading is no longer a guess.

---

## Contractual mechanics

### The *Beitragsverrechnung* — the operative rule of the accumulation phase

The rule is *what is taken out of each gross premium, in what order, before the remainder buys
units*. The German market order, which the reference implementation follows [S1]: the gross
*Beitrag* `B` arrives at the start of the payment period; the ***Abschluss- und
Vertriebskosten* instalment** `α(t)` is withheld, non-zero only in the first sixty months; the
***beitragsbezogene Verwaltungskosten*** `β × B` are withheld, for the whole premium-paying
term; the remainder is the ***Anlagebeitrag***, and it **buys units at the *Anteilspreis***.
Separately, and **by cancelling units rather than by withholding premium**, the
***kapitalbezogenen Verwaltungskosten*** `γ` are taken on the *Fondsguthaben*, together with the
***Stückkosten*** and the ***Risikobeitrag*** on the net amount at risk.

**That rule is no longer asserted from practice; it is read in a wording.** § 14 Abs. 1 of the
DEVK AVB [S2]: *"Wir führen Ihre Beiträge und Zuzahlungen, soweit sie nicht zur Deckung unserer
Abschluss- und Vertriebskosten und beitragsbezogenen Verwaltungskosten vorgesehen sind
(Sparbeiträge), dem Fondsguthaben zu und rechnen sie … in entsprechende Anteileinheiten um. Bei
dieser Umrechnung wird je gewähltem Fonds der zum Stichtag … des Monats der Beitragsfälligkeit
festgestellte Rücknahmepreis einer Anteileinheit zugrunde gelegt.  … Die zur Deckung des
Todesfallrisikos bestimmten, nach den anerkannten Regeln der Versicherungsmathematik berechneten
Risikobeiträge, die fixen Verwaltungskosten (Stückkosten) und die vom Fondsguthaben abhängigen
Verwaltungskosten entnehmen wir dem Fondsguthaben zu Beginn eines jeden Monats."* Both halves of
the split, the *Sparbeitrag* as the residual, the *Rücknahmepreis*, the monthly timing — and,
below, the composite's contested choice on the *Stückkosten*.

**One qualification the same wording forces on `α(t)`.** DEVK's § 18 Abs. 2 spreads only *"einen
Teil"* of the acquisition cost over five years and takes *"[d]en anderen Teil … als Prozentsatz
während der gesamten Beitragszahlungsdauer"*. So in a real tariff part of the acquisition cost
sits **inside** what this document calls `β`, and the deduction from each premium does not step
down at month 61 by the whole of `α`. The composite's arithmetic is a legitimate parameterisation
of the same total; its **labels** are cleaner than the market's, and the cliff it displays is
sharper than a real one.

**That distinction is the easiest thing on this product to get wrong.** Premium-based charges are
withheld *before* units exist; fund-based charges cancel units that already exist. A paid-up
contract loses the first group entirely and keeps the second in full — which is why it decays.
**A model that nets the fund-based charge out of the premium instead of cancelling units produces
the right answer while premiums are paid and the wrong answer the moment they stop.**

The composite takes the ***Stückkosten* by cancellation**, and the argument for it — that
cancellation is the only rule that behaves identically at every payment frequency and identically
before and after *Beitragsfreistellung*, so the fixed fee cannot silently stop when premiums do —
is now backed by a wording that does the same thing: DEVK takes *"die fixen Verwaltungskosten
(Stückkosten) … dem Fondsguthaben zu Beginn eines jeden Monats"* [S2]. That the German market
also takes it by withholding is `[unverified]`. The alternative gives the same total and a
marginally different unit count, quantified in the technical notes.

### The unit / non-unit split, and what the insurer's cash flow actually is

The policy's value is the ***Fondsguthaben***: the number of *Anteileinheiten* held in each fund,
multiplied by that fund's *Anteilspreis* at the *Bewertungsstichtag* [S17]. **Units are the state
variable and euro are derived**; every operation on the contract is a purchase or a cancellation
of units at a price on a date.

Everything that is *not* the unit holding is a cash flow in the insurer's own accounts: the
charges it withholds or cancels, the *Risikobeitrag* it collects, the excess of a death benefit
over the fund it releases, its expenses and its commission. **The reference model projects the
non-unit cash flows and carries the unit fund only as the base on which they are computed** —
the right emphasis for a liability model, because the unit fund is the policyholder's money
passing through. Every benefit — the death benefit up to the fund, the *Rückkaufswert*, the
*Teilentnahme*, the capital converted at *Rentenbeginn* — is funded by cancelling the
policyholder's own units, so a gross presentation would count the same money twice, and the
insurer's non-unit cost on a death is **exactly the *riskiertes Kapital***. The VAG makes this
structural rather than a modelling convenience: § 124 Abs. 2 Satz 2 Nr. 1 requires the technical
provisions for unit-linked benefits to be represented *"so genau wie möglich durch die
betreffenden Anteile"*, and § 125 Abs. 5 requires *"eine Abteilung des Sicherungsvermögens
(Anlagestock)"* per *Anlageart* to hold them — a ring-fenced division **within** the
*Sicherungsvermögen*, not a pool outside it [R15] [REG-R7]. So **a unit-linked projection has no
investment-mismatch term**. A real wording says the same thing from the policyholder's side:
*"Der Anlagestock besteht aus Anteilen von Fonds, an die die Leistungen aus Ihrem Vertrag
gebunden sind, und wird gesondert von unserem sonstigen Vermögen angelegt"* [S2] — which also
shows that a carrier may call the unit holding a *"fondsgebundenes Deckungskapital"* even though
nothing about it resembles a general-account *Deckungskapital*.

### *Abschluss- und Vertriebskosten* — the cap, the spread and the cliff

Two independent rules combine and a specification has to keep them apart. § 4 DeckRV governs what
an insurer may **reserve**: the *Zillmersatz* may not exceed 25 ‰ of the sum of all premiums, and
the rate used at conclusion applies for the whole term [R12] [REG-R16]. § 169 Abs. 3 VVG governs
what it must **pay** on a *Deckungskapital* contract: at least the reserve that results when the
*angesetzte Abschluss- und Vertriebskosten* are spread evenly over the first five contract years
[R1] [REG-R28]. **On a pure unit-linked contract the second does not apply directly** — Abs. 4
sends it to the *Zeitwert* and holds Abs. 3 in reserve only *"soweit … der Versicherer eine
bestimmte Leistung garantiert"*. What happens instead is that the tariff implements the same
shape inside the *Beitragsverrechnung*: only a fraction of the total may be withheld in each of
the first five years, so units are bought from the first month rather than not at all, and one
carrier says so in its *Kostenverrechnung* clause [S2]. The protection is real; its source is the
tariff, backed by the reserving cap, rather than § 169 Abs. 3 operating on this contract.

The arithmetic on the anchor cell, because it is the shape the model reproduces: *Beitragssumme*
= 200 × 12 × 30 = **72 000,00 €**; acquisition charge at the 2,5 % cap = **1 800,00 €**; spread
over 60 months = **30,00 € per month**, which is **15 % of each of the first 60 premiums** and
**nothing thereafter**. The step at month 61 — the *Anlagebeitrag* jumping from 162,00 € to
192,00 € on an unchanged premium — is the single most legible fact in the projection.

Two derived rules follow. On an **in-force** contract past month 60 the composite's `α` is
**zero**, and so is any acquisition expense: the money was spent, and charging it again is a
listed pitfall. (In a real tariff a whole-term slice of acquisition cost continues; see the
*Beitragsverrechnung* section above.) On an ***Einmalbeitrag*** there are no future premiums to
zillmer against, so the whole charge falls at inception at the *Zuzahlungskosten* rate — and that
is what a real wording does: *"Bei Verträgen gegen Einmalbeitrag und bei Zuzahlungen entnehmen
wir alle Abschluss- und Vertriebskosten sofort dem Beitrag oder der Zuzahlung"* [S2].

### *Todesfallleistung* and the *Risikobeitrag*

Four shapes are used in the German market, in ascending order of the risk they impose on the
insurer: the ***Fondsguthaben*** alone, with no net amount at risk and no *Risikobeitrag*;
***Beitragsrückgewähr***, `max(Fondsguthaben, Summe der gezahlten Beiträge)`; **a percentage of
the *Fondsguthaben***, commonly 100, 105 or 110 % `[unverified]`; and a ***garantierte
Mindesttodesfallleistung***, a stated sum chosen at issue and independent of the fund [S1].

The composite adopts **Beitragsrückgewähr**, and the shape is now read verbatim rather than
corroborated at second hand — *"Die Todesfallleistung ist das zum Stichtag bei Tod vorhandene
Fondsguthaben, mindestens aber die Summe der gezahlten Beiträge (Beitragsrückgewähr)"* [S2] § 2
Abs. 7. It is also the shape that makes the mechanic interesting: the net amount at risk is
`max(Summe der gezahlten Beiträge − Fondsguthaben, 0)`, positive **early, and after a market
fall**, and vanishing once the fund overtakes the premiums paid. **Cumulative premiums paid is
therefore a state variable of this product, not a reporting convenience** — and it is the
premiums *paid*, gross, not the premiums *invested*. § 155 Abs. 1 Nr. 5 VVG makes the same
quantity a mandatory item of the annual statement for contracts written from 1 July 2018
[REG-R25], so it is a reported figure as well as a modelled one. **One refinement the composite
does not carry**: the same clause continues *"Etwaige vorherige Kapitalentnahmen aus dem
Fondsguthaben vermindern die Beitragsrückgewähr entsprechend"*, so on a real contract a
*Teilentnahme* reduces the floor as well as the fund. The composite reduces the fund only, which
**overstates** the death benefit and the net amount at risk on the *Teilentnahme* model point.
The charge is recomputed every month, because both the benefit and the fund move:

    riskiertes Kapital(t) = max( Todesfallleistung(t) − Fondsguthaben(t), 0 )
    Risikobeitrag(t)      = q_tariff(x) / 12 × riskiertes Kapital(t)
    units cancelled       = Risikobeitrag(t) / Anteilspreis(t)

`q_tariff` is a **first-order death table** carrying explicit safety margins, while the
projection's own decrement is the **second-order** best estimate [REG-R47]. **The difference
between them is the *Risikoergebnis***, and it is the source of the *Überschussbeteiligung* the
composite declines to project. A model that uses one table for both makes the risk result
identically zero and loses the mechanic. **Which** first-order table is a matter of tariff, not
of law: DAV 2008 T is the modern death basis [R17] [REG-R48], but the one fondsgebundene tariff
whose bases could be read prices its *Risikobeiträge* on *"einer mit 65 Prozent gewichteten
geschlechtsunabhängigen Ausscheideordnung auf Basis der Sterbetafel DAV 1994 T"* and keeps
DAV 2008 T for its underwritten *Risiko-Zusatzversicherung* [S2]. On an unwritten
*Beitragsrückgewähr* cover, "first order" can be an old heavy table scaled down as easily as a
modern one loaded up.

### The *Rentenfaktor* — the product's only financial guarantee

    monatliche Rente = Fondsguthaben(Rentenbeginn) / 10 000 × Rentenfaktor

100 000 € at a factor of 25 yields 250 € per month — a teaching example, not a market level; the
consumer literature illustrates with 25, and also with 30 against 20 [R22]. **Real guaranteed
factors are now available**, from one carrier's *Basisinformationsblätter*: at *Rentenbeginn* 67,
**25,22 / 24,12 / 22,91 / 21,83 €** per 10 000 € for deferments of 12 / 20 / 30 / 40 years, with
the sister company's a few cents lower [S15]. The *garantierter Rentenfaktor* is fixed in the
contract documents at conclusion and rests on the *Rechnungsgrundlagen* then in force: DAV 2004 R
and a *Rechnungszins* of **0,0 % p.a.**, both now established for a fondsgebundene tariff rather
than transferred from a classic one [S2] [S10] [R16] [REG-R49]. It also depends on the payment
frequency, the chosen death benefit and the age at *Rentenbeginn* [S2]. The *Sicherheitsabschlag*
is why the guaranteed factor is lower than the factor the same insurer would quote for an
immediate annuity today — consumer sources put many guaranteed factors at 50–70 % of the current
one `[unverified]` [R22].

**The rule at *Rentenbeginn* is a maximum of two factors, and it is a guarantee with upside:**

    Rentenfaktor_angewendet = max( Rentenfaktor_garantiert, Rentenfaktor_aktuell )

**This is read in a fondsgebundene AVB, not inferred from a conventional one**: *"Der tatsächliche
Rentenfaktor ist der höhere Wert aus dem zu Rentenbeginn aktuellen Rentenfaktor und dem zu
Vertragsbeginn garantierten Rentenfaktor"*, with the current factor computed *"auf Basis der
Rechnungsgrundlagen eines zu dem Zeitpunkt im Neugeschäft offenen sofortbeginnenden
Rententarifs"* and, if the company has none open, on recognised actuarial principles checked by
an independent *Treuhänder* [S2] § 2 Abs. 2–3. The same clause guarantees the resulting annuity
for its whole duration. Zurich [S4] and the market leader [S3] [R22] are consistent with it.
**A model that applies only the guaranteed factor understates the benefit whenever the current
tariff is richer**, and one model point in the shipped table is configured so that the `max()`
actually bites.

**Reduction of a guaranteed factor.** Insurers could previously change guaranteed
*Rentenfaktoren* under a *Treuhänderklausel*, with an independent external *Treuhänder*'s
approval, on two triggers: an unexpectedly strong increase in life expectancy, and a sustainable
reduction in capital-market returns. **That route is now closed wherever the clause is drafted
asymmetrically.** In **BGH, Urteil vom 10. Dezember 2025 — IV ZR 34/25** a clause in the AVB of a
*fondsgebundene Rentenversicherung* letting the insurer reduce the *Rentenfaktor* named in the
*Versicherungsschein* — the monthly annuity per 10 000 € of *Vertragsguthaben* — **without a
corresponding duty to restore it if circumstances improve** was held **void** under § 308 Nr. 4
BGB and § 307 Abs. 1 Satz 1 BGB, on principles reported to reach all comparable clauses
[REG-R36]. The rule is therefore not that the guaranteed factor is "changeable only under
§ 163 VVG": it is that **a *garantierter Rentenfaktor* is a hard guarantee unless the AVB confers
a *symmetric* adjustment right**, with § 163 VVG the residual statutory route, on its own much
narrower conditions, where the tariff's calculation bases themselves fail [R4] [R22] [REG-R27].
**How narrow that route is, is now readable.** § 163 Abs. 1 requires a change in the
*Leistungsbedarf* that is *"nicht nur vorübergehend und nicht voraussehbar"*, a re-set that is
*"angemessen und erforderlich"* to secure permanent fulfilment, and an independent *Treuhänder*'s
confirmation — and it is primarily a power over the **premium**. Abs. 2 Satz 1 gives the
*policyholder* the choice of a benefit reduction instead of a premium increase; the insurer's own
power to reduce the benefit, under Abs. 2 Satz 2, arises only *"[b]ei einer prämienfreien
Versicherung"*. On a premium-paying contract § 163 is therefore a narrower route to a lower
*Rentenfaktor* than it is usually described as being.
Below that line, **Landgericht Köln, Urteil vom 8. Februar 2023, Az. 26 O 12/22**, against Zurich
and reported as *rechtskräftig*, had already held that the low-interest phase is not a sufficient
ground, being entrepreneurial risk that cannot be passed to policyholders — **the docket this
document previously said could not be established** [R22] [S4]. The same reporting gives **AG
Reinbek, 10. Juli 2024, Az. 14 C 473/23** against Allianz, and records the reductions the case
law is about: Allianz in 2017 for about 700 000 contracts written between July 2001 and December
2011, and again in 2021 by **9 %** across the *Invest*, *InvestGarantie*, *Invest alpha-Balance*,
*IndexSelect* and index and portfolio tariffs; AXA in 2017 for about 100 000 contracts; R+V in
2017 for about 4 000; also VHV and Zurich. Trade press of 4 February 2021 reports the market
leader's position that customers could not successfully object to an adjustment, placing a live
commercial dispute at the largest German life insurer inside the window in which the current
in-force unit-linked book was written [R22].
The composite treats the guaranteed factor as **fixed for the life of the contract**, and after
IV ZR 34/25 that is **the legally correct default rather than a modelling simplification**
[REG-R36]. What remains a model risk is the narrow residue: a § 163 VVG adjustment, and an AVB
that does confer a symmetric right.

### *Rückkaufswert* — the *Zeitwert* branch, and what it removes

§ 169 **Abs. 4** VVG is the *Zeitwert* branch, and it reads: *"Bei fondsgebundenen Versicherungen
und anderen Versicherungen, die Leistungen der in § 124 Absatz 2 Satz 2 des
Versicherungsaufsichtsgesetzes bezeichneten Art vorsehen, ist der Rückkaufswert nach anerkannten
Regeln der Versicherungsmathematik als Zeitwert der Versicherung zu berechnen, soweit nicht der
Versicherer eine bestimmte Leistung garantiert; im Übrigen gilt Absatz 3. Die Grundsätze der
Berechnung sind im Vertrag anzugeben."* [R1] [REG-R28]. For a pure unit-linked contract with no
insurer-given benefit guarantee the *Zeitwert* is **the value of the units held**, and a real
wording says exactly that — *"Der Rückkaufswert ist das zum Kündigungstermin vorhandene
Fondsguthaben"* [S2] § 17 Abs. 3:

    Rückkaufswert(t) = Fondsguthaben(t) − Stornoabzug(t)

What that removes is the whole conventional apparatus: no discounting, no *Rechnungszins*, no
mortality basis, no *Zillmerung* residue, no *Mindestrückkaufswert* computation on a second
basis. It is the largest single modelling simplification in the delib library. **The subsection
designation is now given** — Abs. 4 for the *Zeitwert*, Abs. 3 for the five-year floor, Abs. 5
for the *Stornoabzug*, Abs. 6 for the temporary reduction power — and the `[unverified]` tag that
stood on it is withdrawn.

### *Beitragsfreistellung* — why a paid-up unit-linked policy decays

§ 165 VVG lets the policyholder demand conversion to a *prämienfreie Versicherung* for the end of
the current *Versicherungsperiode* [R3] [REG-R28]. **On a fondsgebundene contract nothing is
converted**: the units stay where they are, premium payment stops, the premium-based charges stop
with it because there are no more premiums to charge them on, and the *kapitalbezogenen
Verwaltungskosten*, the *Stückkosten* and the *Risikobeitrag* continue to be taken by cancelling
units. The paid-up contract therefore **decays** at the fund-based charge rate less the fund's
return, and where the death benefit is a *garantierte Mindesttodesfallleistung* the
*Risikobeitrag* accelerates the decay as the fund falls and the net amount at risk rises — a
feedback the model reproduces automatically and a real product risk. **The decay is stated in the
AVB itself**: on single-premium and paid-up contracts the monthly deductions can mean *"dass das
gesamte Fondsguthaben vor Rentenbeginn aufgebraucht ist und der Versicherungsschutz damit
erlischt"* [S2] § 14 Abs. 2. Insurers accordingly set a minimum *Fondsguthaben* below which
*Beitragsfreistellung* is refused and the contract is surrendered instead — § 165 Abs. 1 VVG
routes a below-minimum request to the *Rückkaufswert*, the minimum is a disclosure item under
§ 2 Abs. 1 Nr. 5 VVG-InfoV, and at one carrier it is **2 500 €** [S2] [R3] [R7]. The composite
carries none, which keeps small paid-up contracts alive longer than a real insurer would.

***Beitragsfreistellung* and *Storno* are two decrements, not one** — different triggers,
different cash flows, different subsequent projections. Conflating them is a listed pitfall.

### *Fondswechsel* and *Ablaufmanagement*

***Fondswechsel*** covers **two distinct operations**, and German wordings use the English words
*Shift* and *Switch* for them: **reallocating the existing *Fondsguthaben***, where units are
cancelled in the old fund and bought in the new one at the same *Bewertungsstichtag*; and
**redirecting future premiums**, leaving the existing holding where it is. One carrier's mapping
is now on record — *"Umschichtung des vorhandenen Fondsguthabens (**Fondsshift**)"* against
*"Neuaufteilung der zukünftigen Sparbeiträge (**Fondsswitch**)"*, with the shift priced at the
third published price after the request and the switch effective three working days into the next
*Versicherungsperiode* [S2] § 19. **Whether that mapping is general across German insurers is
`[unverified]`, and this document still asserts none**: each AVB defines its own terms, and the
reference implementation names the **operations**, not the labels. On fees, two carriers are
consistent and the composite's zero matches both: DEVK states *"[d]iese Umschichtungen sind für
Sie kostenfrei"* for shift, switch and *Ablaufmanagement* alike, and Allianz advertises unlimited
free switching [S2] [S3]. Whether any German tariff charges for a switch is `[unverified]`.

***Ablaufmanagement*** is automatic phased de-risking in the run-up to *Rentenbeginn*: the
*Fondsguthaben* is moved in tranches out of equity funds into money-market or *Wertsicherungs*
funds, or into the insurer's *Sicherungsvermögen*. **The questions this document listed as
unanswered are answered at two carriers, and they answer them differently** — which is why the
parameter is switchable. DEVK runs it as a **default the policyholder may object out of**, over
the **last five years**, in **monthly** tranches on an explicit 1/60, 1/59, 1/58 … schedule, into
*"einen risikoarmen Zielfonds"*, free of charge, with fund switching suspended while it runs
[S2] § 2 Abs. 11 and § 19 Abs. 4. Allianz offers it as an **option**, over the **last three
years** [S3]. With one fund and a deterministic return a reallocation and a change of assumed
return are arithmetically the same thing, so the composite implements it as a **deterministic
glide of the assumed gross return to a money-market assumption over the last 60 months**,
switchable off — which matches the observed default at one carrier and is twice the ramp at the
other.

### *Zuzahlung*, *Teilentnahme* and the *Abrufphase*

A ***Zuzahlung*** is an additional single premium into an existing contract; it buys units at the
*Anteilspreis* on the following *Bewertungsstichtag*, raises the *Beitragssumme* and carries its
own acquisition charge, taken in full on receipt [S2] § 18 Abs. 2. A ***Teilentnahme*** is a
partial withdrawal during the *Aufschubzeit*, modelled as a unit cancellation; it is a partial
surrender with a partial surrender's tax consequences — the carrier's own tax notes confirm that
the half-income treatment *"gilt gleichfalls bei Teilkapitalentnahmen während der Aufschubzeit"*
[S2] [R20] [REG-R45] — and it is an **owner election, not a claim**. **Minima are now established
at one carrier**: *Zuzahlung* at least 500 € with the maximum set by the board and none permitted
in the *Abrufphase*; *Teilauszahlung* at least 500 €, leaving at least 1 000 € (premium-paying) or
2 500 € (paid-up) in the fund, at a **40 € fee** waived in the *Abrufphase* [S2]. A *Zuzahlung*
also **restarts the twelve-year tax clock for the increment**, which the composite does not model.

The ***Abrufphase*** is a window inside which the conversion may be brought forward or deferred,
and both limbs are now measured at one carrier: *Rentenbeginn* may be brought forward by **up to
seven years** subject to the minimum deferment and the *Mindestrente*, at a 150 € *Stornoabzug*,
on six months' notice; and deferred by **up to five years**, one year at a time, but only if the
*Abruftarif* was agreed [S2] § 2 Abs. 5–6. **Deferring changes the *Rentenfaktor***, because the
factor is age-dependent — and the question this document could not answer has a consumer-source
answer: the guaranteed factor *"gilt nämlich nur für das in Deinem Vertrag ursprünglich
festgelegte Ablaufdatum"*, so it too may be restated on deferral `[unverified]` as to how general
that is [R22]. Bringing the annuity forward, by contrast, uses guaranteed factors already printed
in the *Versicherungsschein* [S2]. The composite **fixes the *Rentenbeginn*** and records the
*Abrufphase* as an unmodelled option.

### *Effektivkosten* — the metric that ties the stack together

The statutory term is ***Effektivkosten***, and § 2 Abs. 1 Nr. 9 VVG-InfoV defines them as *"die
Minderung der Wertentwicklung durch Kosten in Prozentpunkten … bis zum Beginn der
Auszahlungsphase"*, owed before conclusion under § 7 VVG [R7] [S16] [REG-R31]; the duty is
understood to date from 1 January 2015 with the LVRG `[unverified]`, the date not being in the
regulation. **Abs. 6 settles the fund-cost question**: they are computed *"wie der
Gesamtkostenindikator nach Anhang VI der Delegierten Verordnung (EU) 2017/653"* with the
contract's own parameters, so the fund's costs enter through Annex VI — which is what makes the
*TER* a policy parameter rather than a fund parameter, and BaFin confirms it in terms [R11].

The PRIIPs form of the figure appears in the *Basisinformationsblatt*, and a real one has now been
read [S15]. It confirms the **three time points — one year, half the recommended holding period
and the end of it**, which on the 30-year sheet are years **1, 15 and 30** — exactly what this
document predicted. It also corrects two things. The sheet does **not** print the four graded
scenarios [R9] describes: for a product with a fund menu, the generic sheet gives ranges and
refers the reader to the option-specific documents, which is the multi-option treatment under the
RTS. And a German Schicht-3 unit-linked annuity is, on the profession's own view, a **PRIIP
Kategorie 4** product rather than a Category 2 one, because cost deductions and biometric
components make its pots inseparable [R18] [R8].

**A third correction, and it removes a duty this document asserted.** § 154 Abs. 1 Satz 2 VVG
disapplies the *Modellrechnung* to *"Verträge, die Leistungen der in § 124 Absatz 2 Satz 2 des
Versicherungsaufsichtsgesetzes bezeichneten Art vorsehen"* — the same formula § 169 Abs. 4 uses
for unit-linked business. **A fondsgebundene Rentenversicherung owes no three-rate
*Modellrechnung*** [REG-R25]; the *Basisinformationsblatt* is what the prospective policyholder
gets in its place. (Where a *Modellrechnung* *is* owed, § 2 Abs. 3 VVG-InfoV now gives the rates
exactly: the *Höchstrechnungszinssatz* × 1,67, that rate + 1 pp and that rate − 1 pp.)

Two warnings the specification must still carry, one of them sharper than before. The reference
implementation does **not** implement Annex VI and does not specify a recommended holding period,
so the reduction in yield it publishes is a **delib-defined** measure on the contract's own path
and is **not** the statutory *Effektivkosten*. And although a market level is now available — a
weighted mean of **1,90 % p.a.** with quartiles at 1,30 / 1,64 / 2,35 % at entry age 37 over 30
years, and a real tariff at 1,4–3,4 % over the same term [R11] [S15] — **any figure the technical
notes produce is still arithmetic on delib's own [std] stack and must never be quoted as a market
figure.** The two may now be printed side by side, which makes it more important, not less, to
say which is which.

---

## Riders and options

**In scope and parameterized.** The **death-benefit shape** `db_form`, carried as a model-point
parameter across all four market shapes, with the *Beitragsrückgewähr* form as the base [S2];
***Beitragsfreistellung***, as a stated month at which premiums cease and the fund-based charges
continue [R3]; ***Zuzahlung*** and ***Teilentnahme***, as a stated month and amount;
***Ablaufmanagement***, as the return glide described above; ***Beitragsdynamik***, as an annual
premium increase with the acquisition charge fixed on the initial level; the ***Kapitalwahlrecht***,
as an election at *Rentenbeginn* that changes the tax treatment and not the amount released; the
***Rentenfaktor*** rule, with both the guaranteed and the current factor as inputs so the `max()`
is exercised; and the ***Stornoabzug***, present at zero and switchable.

**Described and deliberately not implemented — the guarantee technologies.** German insurers wrap
three distinct guarantee designs around this same unit-linked chassis. A ***statisches Hybrid***
(*Zwei-Topf-Hybrid*) splits the premium **once, at inception**, between the *Sicherungsvermögen*
— where a guaranteed pot accretes at the *Rechnungszins* to exactly the guaranteed amount at
*Rentenbeginn* — and free funds; simple, transparent, and at a low *Rechnungszins* it consumes
almost the whole premium for the guarantee. A ***dynamisches Hybrid*** recomputes the split
**periodically**, normally monthly, and its three-pot form inserts a ***Wertsicherungsfonds*** —
a fund with a contractual limit on its loss over a defined period — between the
*Sicherungsvermögen* and the free funds, so money can move out of equities in two steps rather
than one [S7] [S8]. ***i-CPPI*** sets the exposure to the risky fund **per policy and
continuously**, as a multiplier times the cushion between the policy value and the present value
of the guarantee: the most efficient of the three and the most path-dependent [S9]. The
prudential handle on all three is § 124 Abs. 2 Satz 2 Nr. 3 VAG: where the benefits include
*"eine Garantie in Bezug auf das Anlageergebnis"*, the ordinary mixing and spreading rules come
back for the assets covering the additional technical provisions [R15] [REG-R7] — which is why a
hybrid's guaranteed pot behaves like general-account money and the free-fund pot does not.

**Why none is implemented.** Each is a rule for reallocating between a guaranteed pot and a risky
pot **along a path**, and its entire content is what it does when the risky pot falls. A
deterministic projection has one path and it is a smooth one, so a guarantee mechanism modelled
inside it either never triggers — dead code presented as a feature — or triggers on a hand-chosen
shock, which asserts a scenario the model has no basis for. What would have to be added is a
stochastic or at least multi-scenario asset model, a monthly reallocation rule, a guaranteed pot
accreting at a *Rechnungszins*, and a *Wertsicherungsfonds* return model. That is a different
model, and an honest reference implementation says so rather than gesturing at it. **No
reallocation rule, CPPI multiplier, *Wertsicherungsfonds* loss limit or guarantee-pot accretion
rule was established** [S7] [S8] [S9]. **One carrier guarantee menu now is**: Allianz InvestFlex
offers a *Garantieniveau* chosen at conclusion in **10-percentage-point steps from 10 % to 90 %
of premiums paid**, adjustable later under conditions, with 10–60 % on the *Basisrente* and a
statutory 100 % on the *Riester-Rente* [S3]. That replaces the 0/60/80/90/100 % menu this
document previously guessed. It also confirms the premise the composite rests on — that the same
carrier sells the same chassis **with and without** a guarantee, so a guarantee-free model point
is a real product and not an abstraction. What the composite keeps from the hybrid world is the
*Ablaufmanagement* glide — de-risking without a guarantee, and representable deterministically.

**Out of scope entirely.** Attached biometric riders (*Berufsunfähigkeits-Zusatzversicherung*,
*Unfall-Zusatzversicherung*, *Hinterbliebenenrente*, *Pflegeoption*), which are separate delib
products or separate covers on their own bases; the **payout phase** (delib `sofortrente`); and
the *Abrufphase*.

---

## Variations across insurers

**Read this first.** **One carrier is now observed in full and the other ten are not.** DEVK's
complete *Bedingungswerk*, *Tarifbestimmungen*, calculation bases and sixteen
*Basisinformationsblätter* have been read [S2] [S15], and Allianz's product page for InvestFlex
[S3]; for every other carrier named below, no AVB, no *Produktinformationsblatt*, no
*Basisinformationsblatt* and no rate card was retrieved. So the first table below is now **partly**
a table of observations and mostly still a table of absences, and it says which is which. The
second table records the **dimensions along which German carriers differ**, with the range argued
from the mechanics and the statutory bounds — and, where a level has been observed, marked as
observed at one carrier rather than as a market range.

### What is established, carrier by carrier

| Carrier | Established here | Source |
|---|---|---|
| DEVK | **Read in full.** Tariff **L/N FR1**, "DEVK-Fondsrente vario", *Kundeninformation* 03101/07/2024. Death benefit `max(Fondsguthaben, Summe der gezahlten Beiträge)`; *Rentenfaktor* = `max(guaranteed, current)` with the current one on an open immediate-annuity tariff; guaranteed factors **25,22 / 24,12 / 22,91 / 21,83 €** per 10 000 € at deferments of 12 / 20 / 30 / 40 years to *Rentenbeginn* 67; bases DAV 2004 R at **0,0 %** and *Risikobeiträge* on **65 % of DAV 1994 T**; charges 2,50 % acquisition, 6,90 % of premium, 0,42 % p.a. of fund, 18 €/yr; *Stornoabzug* **150 €** flat; reduction in yield 1,4–3,4 % p.a. over 30 years; nine Monega funds; five-year opt-out *Ablaufmanagement* | [S2] [S15], **retrieved** |
| Allianz Leben | **Product page read.** "InvestFlex" is a real *Vorsorgekonzept*, sold in a pure fund-linked and a guarantee variant on one chassis; *Garantieniveau* 10 %–90 % of premiums in 10-pp steps; free unlimited fund and strategy switching; optional three-year *Ablaufmanagement*. The AVB host refuses; **no clause text**. *Treuhänderklausel* position publicly defended in February 2021, and the clause held void in IV ZR 34/25 | [S3] [R22] [REG-R36] |
| Zurich Deutscher Herold | The *Verbraucherinformation* series is titled "für **Konventionelle** Versicherungen", implying a fondsgebundene companion; at *Rentenbeginn* the **higher of two factors** applies. Defendant in **LG Köln 8.2.2023 — 26 O 12/22** on the *Rentenfaktor* | [S4] [R22], via a sibling delib file |
| CosmosDirekt (Cosmos Leben) | Inception annuity factor computed on DAV 2004 R at an interest rate of **currently 0 % p.a.** — stated for the **classic** tariff. Corroborates DEVK's 0 % rather than carrying it | [S10], via a sibling delib file |
| Debeka | **Discontinued its classic annuity tariff** — the market-structure mechanism behind unit-linked dominance | [S14], via a sibling delib file |
| NÜRNBERGER | Publishes per-tariff AVB with codes in an `NIR`/`N` series | [S11], via a sibling delib file |
| AXA, R+V, VHV, LPV | Reduced *Rentenfaktoren* under a *Treuhänderklausel* — AXA about 100 000 contracts in 2017, R+V about 4 000 in 2017; AXA and LPV warned by a consumer body in January 2024. Named only for the case-law context; no product document | [R22] |
| Alte Leipziger, LV 1871, Continentale, HDI, Volkswohl Bund, Stuttgarter, WWK, myLife | **Nothing.** Named as real carriers of the right product, with `[unverified]` product names. The HDI address tried on 2026-08-30 returned the site's 404 page | [S5]–[S9] [S12] [S13] [S18] |

### The dimensions of variation, and the argued range on each

| Parameter | Argued range across the German market | Where the composite sits | Tag |
|---|---|---|---|
| Death-benefit shape | *Fondsguthaben* / *Beitragsrückgewähr* / 100–110 % of fund / guaranteed sum | *Beitragsrückgewähr* | shape **read** [S2]; the four-way range `[unverified]` — the one wording read offers only the *Beitragsrückgewähr* form |
| Acquisition charge | 0 % (*Nettotarif*) to 2.5 % of *Beitragssumme* (the cap) | 2.5 %, the cap | cap [R12] [REG-R16]; **2,50 % observed at one carrier** [S15]; interior **[std]** |
| Acquisition spreading | a five-year instalment plus a whole-term percentage | 60 months, then zero | [R1] [REG-R28] for the statutory shape; **the two-part split observed** [S2] |
| Premium-based admin | 2 % to 10 % of each premium | 4.0 % | **[std]**; **6,90 % observed** [S15] |
| Fund-based admin | 0.10 % to 1.20 % p.a. of *Fondsguthaben* | 0.30 % p.a. | **[std]**; **0,42 % p.a. observed** [S15] |
| *Stückkosten* | 0 to 5 EUR per month | 3.00 EUR | **[std]**; **18 EUR per year — 1,50 €/month — observed** [S15] |
| Fund TER | 0.15 % (ETF) to 2.00 % p.a. (active) | 0.45 % | **[std]**; observed sheets report the funds' costs inside a combined band |
| *Kickback* crediting | none, partial or full; special *Überschussanteil*, RfB allocation, or cost reduction | none (passive fund) | **[std]**; mechanisms [R10], one carrier's rule [S2], market levels [R11] |
| *Effektivkosten* | **1,90 % weighted mean at entry age 37 over 30 years; quartiles 1,30 / 1,64 / 2,35 %; insurers above 4 % at every age-and-term combination** | approx. 1 % p.a. implied by the stack — **below the observed lower quartile** | [R11]; delib level **[std]** |
| Guaranteed *Rentenfaktor* | **25,22 / 24,12 / 22,91 / 21,83 € per 10 000 € at deferments of 12 / 20 / 30 / 40 years to age 67**, at one carrier | 25.00 EUR per 10,000 EUR at age 67, flat in deferment | **[std]**, derived; observed values [S15] |
| Factor rule at *Rentenbeginn* | `max(guaranteed, current)` — appears uniform | `max(guaranteed, current)` | **read verbatim** [S2]; also [S4] [R22] |
| *Rentengarantiezeit* | **5 to 25 years at one carrier**, maximum end age 87 | 10 years, not priced separately | [S2]; choice **[std]** |
| *Beitragsgarantie* | **10 % to 90 % of premiums in 10-pp steps at one carrier**; 0 % on a guarantee-free tariff | 0 % — no guarantee | [S3] for the menu, [S2] for a guarantee-free tariff; choice **[std]** |
| Guarantee technology | none / static hybrid / dynamic 2- or 3-pot / i-CPPI | none | argued above |
| *Ablaufmanagement* | **opt-out default over 5 years at one carrier, optional over 3 years at another** | 5-year monthly glide, switchable | [S2] [S3] |
| Free fund switches | **free and unlimited at both carriers observed** | unlimited within modelled behaviour | [S2] [S3]; that any carrier charges is `[unverified]` |
| *Stornoabzug* | must be *vereinbart*, *beziffert*, *angemessen*; **a flat 150 EUR at one carrier** | zero | [R1] [REG-R28]; observed [S2]; level **[std]** |
| Minimum monthly premium | 25 to 50 EUR | 25 EUR | **25 EUR observed** [S2]; the upper end `[unverified]` |
| Entry ages | roughly 15/18 to the low 60s | 18 to 60 | `[unverified]`; **[std]** |
| *Rentenbeginn* age | **62 to 85 at one carrier**; 62 is the tax floor | 67 | [S2]; tax floor [R20] [REG-R45]; choice **[std]** |
| Distribution model | commission tariff, direct writer, *Nettotarif* / *Honorartarif* | commission tariff, with a *Nettotarif* charge variant on the same chassis | [S10] [S13] [S18] |

**The one dimension worth isolating.** A *Nettotarif* is the same unit-linked contract with the
*Abschluss- und Vertriebskosten* removed from the tariff, the adviser being paid a fee under a
separate *Vergütungsvereinbarung* [S18]. It matters for one modelling reason: **the difference
between a gross tariff's reduction in yield and the same chassis's net reduction in yield *is*
the acquisition-cost load** — the single parameter this specification most needs and that no
document in the corpus supplies. **No net-tariff or gross-tariff figure is established**; the
observation that the gap exists is structural, not numeric. It is carried as a charge variant in
the shipped tables so that a reader can read the difference off the model instead of looking for
it in a document that was not retrieved.

---

## Regulatory context

**Contract law — the VVG.** Six provisions do the work, and **every paragraph number below was
read in the canonical text on 2026-08-30** (*Stand*: zuletzt geändert durch Art. 12 G v.
26.5.2026 I Nr. 156); the `[unverified]` tags they carried are withdrawn. **§ 169 Abs. 4** makes
the *Rückkaufswert* of a fondsgebundene contract the *Zeitwert* *"soweit nicht der Versicherer
eine bestimmte Leistung garantiert; im Übrigen gilt Absatz 3"*; **Abs. 3** carries the even
five-year spreading of the *angesetzte Abschluss- und Vertriebskosten* as a minimum on the
*Deckungskapital* branch; **Abs. 5** permits a *Stornoabzug* only where it is *vereinbart*,
*beziffert* and *angemessen* and makes a deduction for *"noch nicht getilgte Abschluss- und
Vertriebskosten"* ineffective — **the burden of proof on the insurer is contractual, not
statutory**, and a real AVB supplies it [S2]; **Abs. 6** permits a temporary reduction to protect
the fund [R1] [REG-R28]. **§ 168 Abs. 1** lets the policyholder terminate *"jederzeit für den
Schluss der laufenden Versicherungsperiode"*, **Abs. 2** extends the right to single-premium
contracts, and **Abs. 3** withholds it only from pension-purpose contracts this product is not —
paired with § 169 it makes *Storno* a near-frictionless exit at fund value, which is why
unit-linked lapse experience differs from conventional lapse experience [R2] [REG-R28]. **§ 165
Abs. 1** gives the right to a *prämienfreie Versicherung* subject to the agreed
*Mindestversicherungsleistung*, and routes a below-minimum request to the *Rückkaufswert* [R3]
[REG-R28]. **§ 163** is the residual statutory route to a reduced *Rentenfaktor*, on three
cumulative conditions and an independent trustee's confirmation — and it is primarily a power
over the **premium**, the insurer's direct power to cut the benefit arising under Abs. 2 Satz 2
only on a paid-up contract [R4] [R22] [REG-R27]. **§ 153 Abs. 1** entitles the policyholder to a
share of the surplus and of the *Bewertungsreserven* unless excluded by express agreement, and
*"die Überschussbeteiligung kann nur insgesamt ausgeschlossen werden"*; **Abs. 4** makes the end
of the accumulation phase the allocation point for the *Bewertungsreserven* on an annuity; here
the share can only come from the risk and cost results [R5] [REG-R9] [REG-R24]. **§ 7** and
**§ 152** govern pre-contractual information and the *Widerruf*, whose period is **30 days**
[R6] [REG-R23] [REG-R31]. **§ 155** sets the annual statement's contents, including the sum of
premiums paid for contracts written from 1 July 2018 — and **§ 154 Abs. 1 Satz 2 excludes this
product from the *Modellrechnung* altogether** [REG-R25].

**Prudential — the VAG and the reserving regulations.** **Anlage 1 Nr. 21 to the VAG names the
*Sparte* "Fondsgebundene Lebensversicherung"** — not "fonds- und indexgebundene
Lebensversicherung", as this document previously said; index-linked business has no separate line.
That separate *Sparte* is why German statistics and insurers' accounts report it apart [R15]
[REG-R5]. **§ 125 Abs. 5 VAG** requires *"eine Abteilung des Sicherungsvermögens
(Anlagestock)"* per *Anlageart* where benefits are provided in units of an open fund — a division
**within** the *Sicherungsvermögen* — and **§ 124 Abs. 2 Satz 2 Nr. 1** requires the technical
provisions to be represented *"so genau wie möglich durch die betreffenden Anteile"*, so unit
assets and unit liability move together exactly [R15] [REG-R7]. § 138 VAG requires premiums to be
calculated on prudent assumptions and, in Abs. 2, benefits and premiums to be set on the same
principles for like risks [REG-R8]. The **DeckRV** supplies the two numbers that matter: the
*Höchstzillmersatz* of 25 ‰ of the sum of all premiums (§ 4 Abs. 1), which binds; and the
*Höchstrechnungszins* of 1 % (§ 2 Abs. 1), which does **not** — the section applies only *"[b]ei
Versicherungsverträgen mit Zinsgarantie"* [R12] [REG-R14] [REG-R15] [REG-R16]. The **MindZV**
fixes the minimum share of each surplus source credited to policyholders, and **the percentages
are now established**: 90 % of the *Kapitalanlageergebnis* (§ 6), 90 % of the *Risikoergebnis*
(§ 7), 50 % of the *übriges Ergebnis* (§ 8). For this product only the last two can bite, because
§ 3 Abs. 1 computes the creditable investment income *"ohne die der Lebensversicherung für
Rechnung und Risiko der Versicherungsnehmer zuzuordnenden Erträge und Aufwendungen"* [R14]
[REG-R18]. Above it sits Solvency II through the VAG: a best estimate plus a risk margin
[REG-R1] [REG-R2] [REG-R6], with EIOPA publishing the curves [REG-R4] and Directive (EU) 2025/2
first applying on 30 January 2027 [REG-R3]. **Nothing in this library implements a 2027 basis.**

**Disclosure and conduct.** The PRIIPs Regulation — Verordnung (EU) Nr. 1286/2014, with the RTS
in Delegierte Verordnung (EU) 2017/653 as amended by (EU) 2019/1866 and (EU) 2021/2268 — requires
a ***Basisinformationsblatt*** for every packaged retail and insurance-based investment product,
and a fondsgebundene Rentenversicherung is the paradigm German IBIP [R8] [REG-R32]. **Sixteen
actual sheets for this product class have now been read** [S15], and they settle what the
document contains: a **summary risk indicator** — this product is graded *"Risikoklasse 2 bis 5"*
on the 1–7 scale, a range because the class follows the chosen fund; a statement that the product
carries **no protection against market falls**; the **costs the investor bears**, split into
*Einstiegskosten*, *laufende Kosten* and *Transaktionskosten*; and the **reduction in yield** at
**three time points — one year, half the recommended holding period and the end of it**, which on
the 30-year sheet are years **1, 15 and 30**, as this document predicted. Two points must be
corrected. **The four graded scenarios *Stress / pessimistisch / moderat / optimistisch* do not
appear**: on a generic sheet for a fund-menu product the *Performance-Szenarien* heading refers
the reader to the option-specific documents instead, which is the multi-option treatment under the
RTS, and the source that described the four-scenario table is itself no longer retrievable [R9].
And **the categorisation is now known and is not the one this document assumed**: on the
profession's own standard a German Schicht-3 unit-linked annuity is a **PRIIP Kategorie 4**
product, because cost deductions and biometric components make its pots inseparable — decomposition
*"ist bei Versicherungsanlageprodukten im Regelfall nicht möglich"* [R18]. Which is why two
documents for economically similar products can show very different scenario returns, and why
this specification cites **no** scenario return.
Alongside PRIIPs, § 2 Abs. 1 Nr. 1 VVG-InfoV with Abs. 2 requires the *einkalkulierte
Abschlusskosten* to be disclosed **in euro as a single total**, the other costs separately as a
share of the annual premium, and Nr. 7 adds a fondsgebundene-specific duty to describe the
underlying funds and their asset types; Nr. 9 with Abs. 6 defines the ***Effektivkosten*** on the
Annex VI method [R7] [REG-R31]. **The *Modellrechnung* does not apply to this product** — § 154
Abs. 1 Satz 2 VVG excludes contracts of the § 124 Abs. 2 Satz 2 VAG kind — though where it does
apply § 2 Abs. 3 VVG-InfoV prescribes three rates exactly: the *Höchstrechnungszinssatz* × 1,67,
that rate + 1 pp, and that rate − 1 pp [REG-R25]. The IDD-derived *Zuwendungen* rules govern
whether a *Kickback* may be retained, and BaFin's *Merkblatt 01/2023 (VA)* now supplies the
substantive answer as well as the *Value for Money* regime described in the overview [R10] [R15]
[REG-R33] [REG-R35].

**Taxation, and why it drives behaviour.** Three regimes meet on this contract, and the
differences between them are the product's commercial argument and its strongest behavioural
driver. In the **accumulation phase nothing is taxed** — no annual taxation of fund income inside
the wrapper, no *Vorabpauschale*, and **no taxable disposal on a *Fondswechsel*** [R20] [R21]
[REG-R45] — while a direct fund holding is taxed on both, which is why a cost comparison against
a *Depot* is not like-for-like. On the **annuity** only the ***Ertragsanteil*** is taxable, at a
statutory percentage set **once** by the annuitant's completed age at *Rentenbeginn* and never
changed, so every later increase is taxed at the same light rate. The table in § 22 Nr. 1 Satz 3
Buchst. a Doppelbuchst. bb EStG has been read: **18 % at 65–66** — a carrier's own tax notes give
the worked figure, a 10 000 € annuity first paid at 65 being taxable as 1 800 € [S2] — and
**17 % at 67**, which is this document's own *Rentenbeginn* and therefore the rate any tax gloss
on the anchor cell should use. The table runs from 59 % at age 0–1 to 1 % from 97 and is not
reproduced here; the `[unverified]` tag on the other ages is withdrawn [R19] [REG-R41]. On
a **lump sum**, § 20 Abs. 1 Nr. 6 Satz 1 EStG taxes *"der Unterschiedsbetrag zwischen der
Versicherungsleistung und der Summe der auf sie entrichteten Beiträge (Erträge) im Erlebensfall
oder bei Rückkauf des Vertrags"*, and Satz 2 halves it where the contract has run **at least
twelve years** and payment falls after completion of the **62nd** year of life — the enacted text
says the 60th, and § 52 Abs. 28 raises it to 62 *"für Vertragsabschlüsse nach dem 31. Dezember
2011"*, so 12/62 is right for anything modelled here and 12/60 for older contracts. § 32d Abs. 2
Nr. 2 EStG puts that half into the personal marginal rate rather than the flat *Abgeltungsteuer*
[R20] [REG-R45]. **The *Teilfreistellung* is in the same provision, not in the InvStG**, and it is
exact — Satz 9: *"Bei fondsgebundenen Lebensversicherungen sind **15 Prozent** des
Unterschiedsbetrages steuerfrei oder dürfen nicht bei der Ermittlung der Einkünfte abgezogen
werden, **soweit der Unterschiedsbetrag aus Investmenterträgen stammt**"*; a carrier's own tax
notes add the transitional limb, that the investment income must have arisen after 31 December
2017 [S2] [R20] [R21] [REG-R45]. The `[unverified]` tags on the sentence, the percentage and the
conditions are withdrawn. Two further points from the same wording: the half-income treatment
also reaches ***Teilkapitalentnahmen*** during the *Aufschubzeit* and a partial *Kapitalabfindung*
at *Rentenbeginn*; and a *Zuzahlung* or a premium increase **restarts the twelve-year clock for
the increment**, which the composite does not model. Death benefits before *Rentenbeginn* are
income-tax free.

**The behavioural consequence, and the reason this is not merely context.** The twelve-year and
age-62 conditions create a **double threshold** that policyholders wait for: surrenders are
suppressed as it approaches and spike once both limbs are met, and the annuitise-or-commute
election at *Rentenbeginn* is a **tax election**, not a preference. A German Schicht-3 lapse
assumption that is flat in duration has ignored the strongest single driver of German surrender
behaviour [REG-R45]. The reference implementation models it as a duration-and-age-dependent lapse
shape with the threshold named and the level **[std]** — the treatment frlib gives the eight-year
threshold in French *assurance vie*. And the **50 % *Mindesttodesfallschutz* rule** for contracts
concluded from 1 April 2009 is a model-point design constraint rather than a footnote: **how it
applies to a *Rentenversicherung* with and without a *Kapitalwahlrecht* was not established**
`[unverified]` [REG-R45], and the composite's death benefit is not designed to satisfy it.

**Accounting and professional standards.** German statutory reporting runs under HGB §§ 341–341o
and the *RechVersV*, where unit-linked business is reported separately from the general account
[REG-R54]. Under IFRS 17 a fondsgebundene contract is the archetypal direct-participating
contract and would be measured under the **variable fee approach**; the VFA mechanics were not
read and are `[unverified]` [REG-R55]. Actuarial work sits under the DAV's *Fachgrundsätze* and
the responsible actuary's certifications under §§ 141–143 VAG [REG-R11] [REG-R56].

**Living texts.** VVG, VVG-InfoV, DeckRV, MindZV, VAG, EStG and InvStG all change; the PRIIPs RTS
has been amended at least twice, by (EU) 2019/1866 and (EU) 2021/2268, and the reworking with
effect from 1 January 2023 is `[unverified]`; the *Höchstrechnungszins* stands at 1 % under a
regulation amended on 19 July 2024, and its 1 January 2025 commencement is `[unverified]` because
it lies in the amending instrument rather than in the DeckRV; BaFin's focus-risk agenda is annual.
**The paragraph numbers in this document are no longer `[unverified]`**: the VVG, VAG, DeckRV,
MindZV and EStG sections cited above were read in the canonical text on 2026-08-30, with the VVG
at *Stand* 26 May 2026, the DeckRV at 19 July 2024 and the MindZV at 7 July 2020. **Dates are a
different matter** — several of the ones this document gives are legislative-history facts that
do not appear in the consolidated texts, and they still carry their tags. Every citation should
still be re-checked against the instrument before anything here is relied on, but it can now be
checked against a text this library has opened rather than against one it has only named.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-fondsgebundene_rentenversicherung-r1
[R10]: #delib-fondsgebundene_rentenversicherung-r10
[R11]: #delib-fondsgebundene_rentenversicherung-r11
[R12]: #delib-fondsgebundene_rentenversicherung-r12
[R13]: #delib-fondsgebundene_rentenversicherung-r13
[R14]: #delib-fondsgebundene_rentenversicherung-r14
[R15]: #delib-fondsgebundene_rentenversicherung-r15
[R16]: #delib-fondsgebundene_rentenversicherung-r16
[R17]: #delib-fondsgebundene_rentenversicherung-r17
[R18]: #delib-fondsgebundene_rentenversicherung-r18
[R19]: #delib-fondsgebundene_rentenversicherung-r19
[R2]: #delib-fondsgebundene_rentenversicherung-r2
[R20]: #delib-fondsgebundene_rentenversicherung-r20
[R21]: #delib-fondsgebundene_rentenversicherung-r21
[R22]: #delib-fondsgebundene_rentenversicherung-r22
[R23]: #delib-fondsgebundene_rentenversicherung-r23
[R24]: #delib-fondsgebundene_rentenversicherung-r24
[R25]: #delib-fondsgebundene_rentenversicherung-r25
[R26]: #delib-fondsgebundene_rentenversicherung-r26
[R3]: #delib-fondsgebundene_rentenversicherung-r3
[R4]: #delib-fondsgebundene_rentenversicherung-r4
[R5]: #delib-fondsgebundene_rentenversicherung-r5
[R6]: #delib-fondsgebundene_rentenversicherung-r6
[R7]: #delib-fondsgebundene_rentenversicherung-r7
[R8]: #delib-fondsgebundene_rentenversicherung-r8
[R9]: #delib-fondsgebundene_rentenversicherung-r9
[REG-R1]: #delib-reg-r1
[REG-R11]: #delib-reg-r11
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R18]: #delib-reg-r18
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R25]: #delib-reg-r25
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R3]: #delib-reg-r3
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R37]: #delib-reg-r37
[REG-R4]: #delib-reg-r4
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R56]: #delib-reg-r56
[REG-R6]: #delib-reg-r6
[REG-R7]: #delib-reg-r7
[REG-R8]: #delib-reg-r8
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
