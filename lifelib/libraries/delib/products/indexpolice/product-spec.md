# Product Specification

**Status:** Draft, 2026-08-29 (sources assembled); citations re-verified against the primary
documents 2026-08-30.

**Scope note.** This is a *standardized composite specification* assembled for reference liability
cash-flow modeling of a German **indexgebundene Rentenversicherung** — the *Indexpolice*: a deferred
private annuity of *Schicht 3* whose accumulated capital sits in the insurer's *Sicherungsvermögen*
(the ring-fenced general-account cover pool) under a guarantee, and whose annually declared
*Überschuss* (surplus) is **not credited as interest** but spent as an **option budget** buying a
one-year participation in a share index. It does not describe any single insurer's contract.

Facts carrying a source tag — [S#] (primary product documents: AVB, *Produktinformationsblatt*,
*Basisinformationsblatt* (PRIIP-KID), *Verbraucherinformation*, *Standmitteilung*) and [R#]
(product-specific regulatory and actuarial references), both numbered per `_research/indexpolice.md`
and resolved in `sources.md` (same directory; numbering frozen, never renumbered), and [REG-R#] (the
cross-product reference library `references/regulatory-and-actuarial-references.md`, whose own
R-numbering is distinct and also frozen) — name the instrument the claim should be checked against.
Values marked **[std]** are standardizations introduced for the reference implementation; each
**[std]** table row carries a numbered footnote giving the rationale and, where one could be assessed,
the plausible market band. Claims that no retrieved document corroborates are flagged [unverified].

**Read this before reading any number below.** delib was **drafted** with **direct HTTP egress
blocked** and, for this product, with the session's `WebSearch` budget already exhausted: no AVB, no
*Basisinformationsblatt*, no statutory text and no index rulebook was opened, so the first draft
rested on the authoring model's own knowledge of German insurance law and practice, disciplined by
[std] and [unverified] tags. **That policy has since been lifted and this product's citations
re-verified against the primary documents.** Of the 38 entries in `sources.md`, **32 now read
`Retrieved: yes`**, one reads `partly`, and **five read `no`**: a *Produktinformationsblatt* class
that does not exist for a *Schicht 3* contract [S3], the annual parameter notice insurers send to
policyholders and never publish [S5], *Finanztest* behind its paywall [S13], the comparison portals
behind a bot wall [S15], and the rating houses behind their subscription tools [R21]. **A
`Retrieved: yes` entry means the document was opened and the passage it rests on read; anything else
is a pointer rather than a certificate**, and each entry says which it is.

The re-verification moved this document. Two carrier *Bedingungswerke* were read in full [S2] [S7],
so the *Indexbeteiligung* clause set below is quoted rather than reconstructed; the death-benefit
rule was cited to the wrong carrier series and is corrected (footnote 23); and rows that read "not
established" now carry carrier figures. But the **commercial envelope stays [std] throughout** — no
entry-age band and no minimum premium is published by any of the three carriers, so the model points
remain construction. What was never in dispute is the **mechanics** — the financing identity between
declared surplus and option budget, the sum-of-capped-monthly-returns payoff with uncapped negative
months, the annual floor at zero, the permanent lock-in and the annual election — and this document
puts its weight there. Three carrier products are named — **Allianz Zukunftsrente IndexSelect** [S2],
**R+V-PrivatRente IndexInvest** [S7] and **Stuttgarter index-safe** [S8] — all three now
**established** from the carriers' own documents, and no fourth is added.

---

## Product overview and market role

An *Indexpolice* is an **aufgeschobene Rentenversicherung**: a deferred annuity on a single life, with
an *Aufschubphase* running from inception to *Rentenbeginn* and a *Rentenphase* paying a lifelong
*Leibrente* thereafter [S1] [S9]. Premium, reserve, death benefit before *Rentenbeginn*,
*Rückkaufswert*, *Beitragsfreistellung*, *Rentenfaktor*, *Kapitalwahlrecht* and *Rentengarantiezeit* are
the chassis of a *klassische Rentenversicherung* and are documented for that product. **The delta is one
clause set**: how the annually declared *Überschuss* is applied. Three facts decide everything else, and
the first two are the ones secondary descriptions usually get wrong.

**1. The capital is in the general account, not in a fund.** The accumulated *Deckungskapital* sits in
the *Sicherungsvermögen* [REG-R7], exactly as a classic annuity's does: no *Anlagestock*, no unit
account, no policy-level asset allocation. The policyholder owns a **claim on the insurer measured in
euros**, not a number of units; the reserve rolls forward by a recursion, not by a unit price; and the
*Rückkaufswert* is a reserve, not a *Zeitwert* of units [R2] [REG-R28]. **What the index does is define
a payoff, not an investment** — the policyholder is never invested in the index at any moment, and the
insurer buys the option package that hedges the payoff it has itself written [R9] [REG-R7].

A terminological trap follows. In regulatory and accounting vocabulary, *"Lebensversicherungen, bei
denen das Anlagerisiko vom Versicherungsnehmer getragen wird"* — the balance-sheet class containing
*fondsgebundene* **and** *indexgebundene* life insurance — means contracts where the **policyholder
bears the investment risk**. An *Indexpolice* of the kind described here does not belong there, and is
booked and reserved as a **conventional profit-participating contract**, sitting in the Solvency II
line *insurance with profit participation* [R15], [unverified] as to the line-of-business numbering,
which no retrieved document states. **The reading itself is no longer a reading.** § 125 Abs. 5 VAG
requires an *Anlagestock* only "soweit Lebensversicherungsverträge Versicherungsleistungen … **direkt
an einen Aktienindex oder andere Bezugswerte binden**", and § 124 Abs. 2 VAG scopes the whole class by
whether "das Anlagerisiko vom Versicherungsnehmer getragen wird" [R15]. A payoff financed out of
declared surplus, floored at zero and payable in euros from the cover pool is neither. Both retrieved
AVB say the capital is in the *Sicherungsvermögen* in terms — Allianz's KID: "Die Kapitalanlage erfolgt
während der gesamten Versicherungsdauer vollständig durch das Versicherungsunternehmen im
Sicherungsvermögen" [S4]; R+V: "Ihr Policenwert ist Teil des Sicherungsvermögens der R+V
Lebensversicherung AG" [S7]. The cross-product reference library still records the question as open
[REG-R7]; this specification does not. delib therefore uses *Indexpolice* / *Indexbeteiligung* for the
product and reserves *indexgebunden* for its regulatory sense.

**2. The index participation is a form of *Überschussverwendung*, with no independent statutory
footing.** § 153 VVG gives the policyholder a right to participate in the surplus and in the
*Bewertungsreserven* unless participation is excluded, and requires allocation by a
*verursachungsorientiertes Verfahren* or another comparable appropriate method [R1] [REG-R24]. What the
policyholder is legally entitled to is a **share of surplus**; the AVB then say how that share is
applied, and this product's AVB say it is applied by buying a bounded index-linked payoff for one year.
The *Wahlrecht* is therefore an *Überschussverwendungswahlrecht*, and the *Indexbeteiligung* stands or
falls on the contract clause. **That is the correct legal characterisation, and all three carrier
documents now state it in their own words** — Allianz: "Die Überschussbeteiligung eines Jahres kann zum
einen für die Indexpartizipation … verwendet werden" [S4]; R+V finances the participation "mit den …
jährlichen Überschussanteilen sowie mit der jeweiligen jährlichen Mindestbeteiligung an den
Bewertungsreserven" [S7] § 3 Ziffer 9; Stuttgarter: "Es werden 100 % der laufenden Überschüsse für die
Indexbeteiligung verwendet" [S11]. Both AVB add a component this specification did not carry: the
budget is the declared surplus **plus** the year's minimum share of the *Bewertungsreserven*, and
Allianz's is net of *Verwaltungskosten*. The subsection numbering is confirmed against the canonical
text of § 153 VVG, and one correction follows from it: Abs. 4 makes the *Bewertungsreserven* half-share
of Abs. 3 Satz 2 fall due at the **end of the *Ansparphase***, not at termination, for a
*Rentenversicherung* [R1].

**3. The option budget is the declared surplus, and nothing more.** The insurer earns a return on the
*Sicherungsvermögen*; the MindZV forces a minimum share of each result source to the policyholders —
**90 % of the *Kapitalanlageergebnis* after the *Rechnungszinsen* are deducted, 90 % of the
*Risikoergebnis*, 50 % of the *übrige Ergebnis*** [R8] [REG-R18]; the insurer declares an
*Überschussanteilsatz* out of that; and a contract in the index arm has that declared amount **spent on
options instead of credited as interest**. **An Indexpolice therefore does not have a larger risk budget
than a *Klassik* contract of the same vintage under the statutory minimum — the MindZV floor is the
same instrument-wide floor.** That is the most under-appreciated fact about the product and it belongs
on the first page. **But the *declared* rate is a different matter, and the market data contradict the
stronger form of the claim**: Assekurata's 2026 survey puts the average declared *laufender
Überschusszins* on *Indexpolicen* at **3,07 %** against **2,62 %** for classic private annuities and
2,65 % for *Neue Klassik* [R20]. Index tariffs sit in their own *Bestandsgruppen* and *Überschuss­verbände*
([S7] § 13 Ziffer 3), and the declaration for them is currently higher. The identity that holds without
qualification is the narrower one: whatever is declared to *this* contract is spent once — on options
or as interest, never both.

**Why the product exists.** The *Höchstrechnungszins* fell from 4,00 % (1994–2000) through 3,25 %,
2,75 %, 2,25 %, 1,75 %, 1,25 % and 0,90 % to **0,25 % for 2022–2024**, and rose to **1,00 % from
1 January 2025** — the first increase in about thirty years, made by the *Sechste Verordnung zur
Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz* of 19 July 2024, BGBl. 2024 I
Nr. 250 [R7] [R18] [REG-R14] [REG-R15]. At 0,25 % the guaranteed component of a conventional annuity's
return is negligible and the discretionary component is the whole story. An Indexpolice takes that
same discretionary component and, instead of crediting it as a modest certain amount, converts it
into a bounded lottery on an index. **The product is a direct commercial response to a near-zero
guaranteed rate**, and the 2025 rise makes the *sichere Verzinsung* arm relatively more attractive
again; whether observed elections have shifted is [unverified] [R7]. Qualitatively, and not in doubt:
the family emerged in the second half of the 2000s, grew through the low-interest decade as the
guaranteed component shrank towards nothing [R7], became a standard offering across the large and
mid-sized carriers, and was one of the main vehicles of the ***Neue Klassik*** generation [S6] [REG-R53].

**Market size.** There is no industry figure to quote: **no published statistic isolates the German
index-participation segment**. The GDV's *Die deutsche Lebensversicherung in Zahlen 2024* splits the
in-force book at 31.12.2023 into *Renten- und Pensionsversicherungen* 61,8 %, *Kapitalversicherungen
(klassisch)* 15,7 %, *Invaliditätsversicherungen* 9,2 % and *Risikoversicherungen* 6,5 % — with no
index line, and the word "Index" occurring nowhere in the publication except its own table-of-contents
index [R19]. These contracts are counted within conventional annuity business because that is what they
are [R15]. The only counts available are a single carrier's own, and they are press statements rather
than statistics: Allianz reported **400.000** IndexSelect contracts in October 2016 [S12] and "über
500.000" in May 2019 [S16]. The frame it sits in: German life premium income (life insurers, Pensionskassen and
Pensionsfonds, GDV basis) was **+2,8 % to 94,6 Mrd. €** in 2024 — *laufende Beiträge* **66,3 Mrd. €**,
roughly flat, *Einmalbeitragsgeschäft* about **+10 % to 28 Mrd. €** — with the contract count **−1,4 %
to 80,3 Mio.**; on the BaFin basis, life-segment *verdiente Bruttobeiträge* were **90,4 Mrd. €**
[REG-R53]. The two measure different populations on different bases and are never combined. The relevant
market rate is the declared one. Assekurata's 24th *Marktstudie* (March 2026) gives, for 2026,
**2,62 %** *laufende Verzinsung* on classic private annuities (3,23 % including *Schlussüberschüsse*),
**2,65 %** on *Neue Klassik* (3,32 %), **3,07 %** on *Indexpolicen* — "etwa dem Vorjahresniveau" — and
2,49 % on guaranteed fund policies [R20]; the 2026 averages recorded from other surveys in the sibling
delib files (2,6–2,7 %, 2,87 %, 2,54 %) measure different panels and are not combined with these
[REG-R53]. One carrier publishes its own figure directly: Stuttgarter's *sichere Verzinsung* for all
*Indexstichtage* from 1.2.2026 to 31.1.2027 is **2,16 %** [S8]. That declared rate **is** the option
budget [R8].

**The same index module is written on four chassis** — *Schicht 3* private annuity (this document),
*Basisrente*, *Riester* and *Direktversicherung* in *bAV* (outside delib). The wrapper changes the
guarantee requirement [R12] [REG-R43], the tax treatment [R13] [R14] [REG-R41] [REG-R45] and the
accessibility of the capital — and **not the index mechanics**.

---

## Representative specification

The representative design is a **composite** and remains one: it is not a transcription of either
carrier wording, because the two retrieved wordings differ from each other on the payoff itself. The
GDV publishes *Musterbedingungen* for the deferred-annuity chassis but **no model wording for an
index-participation module** — its life catalogue runs to eleven model conditions and nine
*Muster-Standmitteilungen*, and not one of them is an index module [S1]. That is the structural reason
the clause set varies more across insurers here than for any other delib product, and the variation is
now demonstrated rather than asserted: **Allianz caps each month and multiplies the capped sum by a
*Partizipationssatz*** [S2]; **R+V applies a *Beteiligungsquote* to the point-to-point year return of a
house index and has no cap at all** [S7]; **Stuttgarter is a quota design too** [S8]. Every
representative choice below is argued against the plausible band in *Variations across insurers*, and
the choices that a retrieved AVB now settles say so in their Basis column.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-life *aufgeschobene Rentenversicherung*, *Schicht 3*, profit-participating, general account; *Neue Klassik* guarantee architecture | [S1] [S6] [R15] |
| Where the capital sits | *Sicherungsvermögen*; no *Anlagestock*, no units, no policy-level asset allocation | [R15] [REG-R7]; reading argued above |
| *Überschussverwendung* | *Indexbeteiligung* or *sichere Verzinsung*, at the policyholder's **annual** election | [R1]; clause-level wording **[std]** (1) |
| Lives basis | Single life; no joint-life form in this family. Sex may not be a rating factor — unisex since 21 December 2012 | [S1]; [REG-R34] |
| *Eintrittsalter* | 25 to 55 | **[std]** (2) |
| *Rentenbeginn* age | 62 to 70; 67 representative | **[std]** (2) |
| *Aufschubdauer* | 12 to 40 years; 12 is the tax minimum | **[std]** (2); [R14] [REG-R45] |
| Age basis | Age last birthday at inception | **[std]** (3) |
| Underwriting | Light or absent — a short declaration or none, the sum at risk before *Rentenbeginn* being small | [unverified]; **[std]** (4) |
| *Garantieniveau* (*Beitragsgarantie*) | **90 % of the *Beitragssumme***, due at *Rentenbeginn* | **[std]** (5) |
| Guaranteed rate (*Rechnungszins*) | **1,00 %** — the *Höchstrechnungszins* for 2025 and 2026 | [R7] [R18] [REG-R14] [REG-R15] |
| Anchor model cell | *Eintrittsalter* 40, *Rentenbeginn* 67, *Jahresbeitrag* 2 400,00 €, annual mode, Cap design, 90 % *Beitragsgarantie*, full index election in every year | **[std]** (6) |

Footnotes to **[std]** rows:

1. **No index AVB was obtained** [S2] [S7] [S8], and the GDV publishes no model clause for the module
   [S1]. The clause set in *Contractual mechanics* below is reconstructed from the mechanics the research
   file establishes, is attributed to **no carrier**, and is labelled a composite wherever used.
2. **No *Produktinformationsblatt* was located** [S3] [S11] [S15], so no entry-age band, minimum
   premium, term band or maximum sum was established for any carrier. The envelope is an uncontroversial
   **[std]** construction: 25–55 is the mid-career segment this product is sold into, 67 is the German
   statutory retirement age, and the 12-year minimum is the tax threshold of § 20 Abs. 1 Nr. 6 EStG
   [R14] [REG-R45] rather than a product limit.
3. The German market's own *Eintrittsalter* convention is frequently the calendar year of inception less
   the year of birth, stepping on 1 January rather than on the birthday. delib runs **age last birthday**
   across all ten products, the registry fixing one age basis for the library; with the attained age
   stepping on the policy anniversary the two differ by at most one year, and mortality here is a
   **timing** rather than an amount assumption.
4. No underwriting rule of any carrier was established; the reasoning is structural. The *Aufschubphase*
   death benefit is a return of capital rather than a sum at risk, so the *Risikoüberschuss* is small and
   § 161 VVG (*Selbsttötung*, three years) is close to inoperative [R6] [REG-R26].
5. Carriers offer a **choice of *Garantieniveau*** — because **every euro of guarantee not promised is
   a euro that can back risk assets, and therefore a larger option budget**. Three levels are now
   observed in retrieved documents: **90 %** for *Allianz Zukunftsrente IndexSelect* ("Sie haben
   Anspruch darauf, mindestens 90 % Ihres Kapitals zurückzuerhalten") and **80 %** for *IndexSelect
   Plus*, whose *Chancenturbo* is precisely what the released ten points buy [S4]; **90 %** in R+V's
   AVB ("Zum vereinbarten Rentenbeginn entspricht der Policenwert mindestens 90 % der Summe der
   gezahlten Beiträge") [S7] § 1 Ziffer 2; and **85 %** for the Stuttgarter *Basisrente* variant [S11].
   delib's 90 % is the modal observed level. That the menu once ran down to 60 % is the research file's
   recollection and stays [unverified]. **The wrapper decides the floor**: a *Riester* variant must
   guarantee that at least "die eingezahlten Altersvorsorgebeiträge" are available at the start of the
   payout phase under the AltZertG *Beitragserhaltungszusage* — up to 20 % of the *Gesamtbeiträge*
   disregarded where they buy biometric cover — and so has the smallest option budget of the four
   [R12] [REG-R43].
6. *Eintrittsalter* 40 with *Rentenbeginn* 67 gives a 27-year *Aufschubdauer*, long enough for the
   ratchet to compound visibly and short enough to print in one table. The 2 400,00 € *Jahresbeitrag*
   is the research file's 200,00 € per month, taken on the **annual** mode so the anchor is free of the
   *Ratenzahlungszuschlag* and the loading is exercised by the fractionated model points instead.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium form | *Laufender Beitrag*, level, over a *Beitragszahlungsdauer* that may be shorter than the *Aufschubdauer*; an *Einmalbeitrag* form exists and *Zuzahlungen* are permitted | form confirmed [S2] Ziffer 10, [S7] §§ 7–8 (both carry *Zuzahlungen* and *Beitragserhöhungen*); the level and the minimum stay **[std]** |
| Representative premium | **2 400,00 € per year** (200,00 € per month), payable throughout the *Aufschubdauer* | **[std]** (7) |
| Payment frequency and *Ratenzahlungszuschlag* | Annual (no load), half-yearly **2 %**, quarterly **3 %**, monthly **5 %** | menu [unverified]; levels **[std]** (8) |
| *Beitragssumme* | Sum of the premiums payable over the *Beitragszahlungsdauer*, on the **annual-mode** premium — the *Ratenzahlungszuschlag* is a charge for instalments and is not part of it | **[std]** (9) |
| *Dynamik* | Automatic annual increase with a matching benefit increase and a right to decline; each increment is a new tranche with its own guarantee basis | [unverified]; not modeled **[std]** (10) |
| Premium cessation | On death, on surrender, on *Beitragsfreistellung*, and at the end of the *Beitragszahlungsdauer* | [S1] [R3] [REG-R28] |

7. No minimum or maximum premium was established for any carrier [S3] [S15]. 200,00 € a month is a
   plausible mass-market monthly savings premium and is the research file's own **[std]**; the plausible
   band is 50 € to 1 000 € a month.
8. The market convention recorded in the sibling delib research is of this order and is [unverified];
   no carrier's table was seen. It is a **[std]** multiplier on the premium collected.
9. Whether a carrier computes the *Beitragssumme* on the loaded or the unloaded premium was not
   established. delib takes the unloaded reading because the *Beitragssumme* is the base of the
   *Höchstzillmersatz* [REG-R16] and of the *Mindesttodesfallschutz* test [REG-R45], both of which are
   about the substance of the contract rather than how it is billed. The alternative reading raises the
   acquisition charge on a monthly-paying policy by the loading, and is a named pitfall.
10. *Dynamik* is a premium-increase mechanic on an exogenous index, and each increment reopens the
    guarantee basis. Modeling it needs a tranche ledger; the reference implementation has none.

### The index participation module

This is the product, and it is the one table in this document where the mechanics are firm and every
level is **[std]**.

| Parameter | Representative value | Basis |
|---|---|---|
| *Indexjahr* | Twelve months, aligned in the model to the policy year | mechanic [S2] [S5]; alignment **[std]** (11) |
| Observation | The index level is read at thirteen *Beobachtungstage* — one at the start and one per month — and month `m`'s return is `I(m)/I(m−1) − 1` | mechanic firm; convention **[std]** (11) |
| Payoff design | **Cap**: each month's return capped above at `C`, **not floored below**; the twelve summed; the sum floored at zero, never the month | mechanic firm |
| Monthly Cap `C` | **3,00 % per month** | **[std]** (12) |
| *Partizipationsquote* variant | `max(q × (year's index movement), 0)`, no monthly cap | mechanic firm; level **[std]** (13) |
| *Partizipationsquote* `q` | **60 %** on an equity price index; **100 %** on a low-volatility house multi-asset index | **[std]** (13) |
| Base of the participation `G` | The accumulated capital at the **start** of the *Indexjahr*, before that year's premium | **[std]** (14) |
| *Höchststandsicherung* | Whatever is credited is permanently added to the guaranteed capital and enters the base of every later *Indexjahr* | mechanic firm |
| Declared surplus rate `b` (= the option budget) | **2,50 % per year** of `G` | **[std]** (15) |
| *Wahlrecht* | Annual election between the two arms, exercisable without the insurer's consent, without medical evidence and without charge; election as a fraction `w ∈ [0, 1]` of the surplus directed to the index arm | mechanic firm; `w` form **[std]** (16) |
| *Mindest-Cap* | **None** | **[std]** (17) |
| Minimum option budget | **None** — if no surplus is declared the *Indexbeteiligung* buys nothing and the year credits zero whatever the index does | [R1] [R8]; **[std]** (17) |
| Mid-year exit | **No index credit in the year of exit** — death, surrender or annuitisation inside an *Indexjahr* forfeits that year's payoff | **[std]** (18) |
| Index participation in the *Rentenphase* | **None** — the *Wahlrecht* lapses at *Rentenbeginn* | **[std]** (19) |
| Underlying | Parameterised by an explicit monthly-return path with a stated volatility, not by a named index | **[std]** (20) |
| *Ersatzindex* | The insurer may substitute a comparable index on notice if the index ceases to be published, is materially restructured, or ceases to be available on terms on which the hedge can be bought | mechanic firm; procedure **[std]** (21) |

11. The level read is a **closing level, not an average**: monthly movements are "die prozentuale
    Veränderung des Index zwischen 2 Bewertungsstichtagen, die wir Ihnen jährlich mitteilen" [S2]
    Ziffer 3.3 Absatz 2 a), and R+V's *Bewertungsstichtag* is "der letzte Börsentag eines
    Versicherungsjahres in Frankfurt am Main" [S7] § 3 Ziffer 3. An averaging (Asian) reading would
    lower the effective volatility and buy a higher Cap out of the same budget; **neither carrier
    averages**, so delib's closing-level convention is the market's. **The alignment is a genuine
    variation.** For R+V the *Indexjahr* is the *Versicherungsjahr* [S7] § 3 Ziffer 3; for Allianz it
    need not be — Ziffer 3.5 contemplates that "der Beginn des →Indexjahres nicht mit dem Beginn eines
    →Versicherungsjahres übereinstimmt" — and Stuttgarter runs a common calendar window, its published
    quota applying to "alle Indexstichtage vom 1.2.2026 bis 31.1.2027" [S8]. delib's alignment with the
    policy year is R+V's rule and a **[std]** simplification against the other two.
12. **Two cap and quota levels are now established, but not a market distribution.** Allianz's own
    worked example runs at a **Cap of 3,2 %** with a *Partizipationssatz* of **75,00 %**, both
    "exemplarisch gewählt" [S2] [S5]; the 2018 litigation records the cap then in force as 3,3 %
    [S14]. What is still missing is a **panel** — a year's levels across named carriers side by side,
    which only a rating house publishes [R21] and none was reachable. The band quoted throughout —
    **1,5 % to 5,0 % per month, typically 2,5 % to 4,0 %** — remains the research file's assessment
    and is [unverified]; 3,00 % is its midpoint and sits just below Allianz's own illustration.
    **The Cap is not a free parameter**, and the AVB says so: it is set annually "auf der Grundlage
    von Angeboten mehrerer Finanzinstitute" and depends on the surplus, the *Bewertungsreserven*
    *Sockelbetrag* and market factors "wie der Volatilität und der Dividendenrendite des jeweiligen
    Index" [S2] Ziffer 3.3 Absatz 2 b) — so there is exactly one Cap at which the capped-sum payoff
    costs the budget, and the technical notes publish that consistency check.
13. **One quota is published and one illustrated.** Stuttgarter's current *Partizipationsquote* on its
    house multi-asset index is **70 %**, with the *Index-Turbo* options at 120 % and 172 % [S8];
    Allianz illustrates **75,00 %** on the EURO STOXX 50 [S2]. delib's 60 % on an equity price index
    is below both, and its 100 % on the house path is above the one published house-index figure;
    both remain **[std]**, and 50–80 % / 80–120 % remains the research file's assessment,
    [unverified] as a band. The Cap design is the base because it is the design the product's
    reputation and its criticism both rest on; the *Quote* is a switchable variant — and it is R+V's
    and Stuttgarter's actual design, not a hypothetical one.
14. **Settled, and delib's reading is the carriers'.** "Bezugsgröße für die →Indexpartizipation ist
    der →Policenwert zu Beginn des →Indexjahres" [S2] Ziffer 3.3 Absatz 2 e), which expressly
    excludes that year's premiums and *Zuzahlungen*; R+V's *Bezugsgröße* is likewise "der Wert, der ab
    Beginn des Versicherungsjahres … das gesamte Versicherungsjahr vorhanden ist. Dabei werden weitere
    Beiträge und Zuzahlungen während des Versicherungsjahres nicht berücksichtigt" [S7] § 3 Ziffer 2.
    It is the **whole capital at the year start, before that year's premium** — not a sub-account and
    not the accumulated *Überschussguthaben*. The alternative readings are withdrawn, and this is no
    longer a named model risk.
15. The declared rate **is** the option budget [R8], and delib's 2,50 % is now on the low side of the
    evidence rather than at its midpoint: Assekurata's 2026 index-segment average is **3,07 %** [R20]
    and Stuttgarter's own published *sichere Verzinsung* is 2,16 % [S8]. The value is a shipped input
    and is not changed in a provenance pass; `model.md` records the comparison. It is **exogenous** in
    the reference implementation: the feedback from the *Garantieniveau* through the asset mix to the
    declared rate is real, is the whole design logic of *Neue Klassik*, and is **not modeled**. Both
    AVB also add a component delib does not model — the year's **minimum share of the
    *Bewertungsreserven*** is part of the budget alongside the declared surplus [S2] Ziffer 3.3
    Absatz 1, [S7] § 3 Ziffer 9.
16. **A split election is permitted, in 25-percent steps**: "Die Aufteilung kann in 25-Prozentschritten
    erfolgen, wobei die Summe 100 Prozent ergeben muss" [S2] Ziffer 3.1. delib's continuous fraction
    `w` is therefore a **[std]** relaxation of a discrete menu, with all-or-nothing the special case
    `w ∈ {0, 1}`. The notice period is **7 days** before the *Indexstichtag* at both carriers ([S2]
    Ziffer 3.1, [S7] § 2 Ziffer 3) — and the far more consequential question is answered in delib's
    favour: **the Cap is announced before the election deadline**, Allianz notifying the *Caps* and the
    *Partizipationssatz* "spätestens 3 Wochen vor dem Indexstichtag".
17. These are different promises: a *Mindest-Cap* bounds the Cap given a budget, a minimum budget
    bounds the budget — and a *Mindest-Cap* is worthless in a year in which no surplus is declared
    [R1] [R8]. **Neither appears in either retrieved AVB**, and delib assumes neither. Both AVB
    instead carry the opposite provision: index participation is **excluded** for a year in which the
    *Policenwert* does not exceed the *Deckungsrückstellung* required for the guarantee ([S2]
    Ziffer 3.5, [S7] § 2 Ziffer 1), so the budget is not merely unguaranteed but contractually
    switched off when the guarantee binds.
18. **Settled, and delib's [std] is the carriers'.** The participation is credited only "zu Beginn des
    folgenden →Indexjahres" ([S2] Ziffer 3.3 Absatz 1, [S7] § 3 Ziffer 5), R+V's *Bezugsgröße* is by
    definition the value present for the **whole** *Versicherungsjahr* [S7] § 3 Ziffer 2, and on
    surrender Allianz adds only a pro-rata *Schlussüberschussanteil* and *Sockelbetrag* [S2]
    Ziffer 9.2 Absatz 4 — **no pro-rata index credit and no refund of the unspent budget**. The
    behavioural consequence stands: the product rewards surrendering just after an *Indexjahr* end and
    penalises surrendering just before one. A model stepping annually puts every exit at a year end and
    so implicitly assumes the favourable convention; the monthly grid dates the forfeiture instead,
    though the payoff is still not pro-rated and the surrender rate is still unconditional.
19. **Confirmed for Allianz**: the participation runs "**vor Beginn der Rentenzahlung**" only [S2]
    Ziffer 3.3, so the *Wahlrecht* lapses at *Rentenbeginn* and payout-phase surplus is applied to the
    annuity in payment. Whether any other carrier offers index participation in the payout phase is
    still unestablished.
20. **Two German house multi-asset indices are now named in this file** — the *Solactive Multi Anlage
    Stabil Index* (**SOMAS**), built for R+V by Solactive [S7], and the *Stuttgarter M-A-X Multi-Asset
    Index*, alongside a *Stuttgarter Grüne Zukunft Index* [S8] — and the equity underlyings are the
    **EURO STOXX 50** and the **S&P 500**, the latter with a *Währungsfaktor* applied to the year
    return [S2]. **No volatility target and no index-level fee is published for either house index**,
    which is why the model still parameterises the underlying by an explicit table of monthly returns
    with a stated drift and volatility, shipping an equity case, a low-volatility house case and an
    all-zero case, and names no index in any shipped file.
21. **Substitution requires no *unabhängiger Treuhänder*.** Allianz may replace an index "mit Wirkung
    zu Beginn des nächsten →Indexjahres" on material changes it is not responsible for, and if it
    cannot replace one may exclude the participation for subsequent *Indexjahre* [S2] Ziffer 3.7;
    R+V replaces the index "zum nächsten Indexstichtag", choosing one that "dem zu ersetzenden Index
    weitestgehend entspricht", at no cost to the policyholder [S7] § 3 Ziffer 11. **Neither grants a
    *Sonderkündigungsrecht***; R+V instead gives the policyholder a choice whether to continue with the
    new index. Both also carry a suspension clause delib does not model: where no suitable
    capital-market instrument can be bought, the participation is suspended and the budget goes to the
    *Verzinsung* arm [S7] § 3 Ziffer 10. The legal frame is under *Contractual mechanics*.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Benefit at *Rentenbeginn* | The accumulated capital, floored at the **greater of** the *Beitragsgarantie* and the guaranteed capital including every locked-in credit | [R11] [R12]; composition **[std]** |
| Conversion | Lifelong *Leibrente* at the ***greater* of the guaranteed *Rentenfaktor* fixed at issue and the insurer's current factor at *Rentenbeginn*** | chassis fact, two carrier documents in the sibling research; level **[std]** (22) |
| Guaranteed *Rentenfaktor* | **25,00 € per month per 10 000 € of capital** at *Rentenbeginn* 67 | **[std]** (22) |
| *Kapitalwahlrecht* | Lump sum instead of the annuity, applied for **at latest one month before *Rentenbeginn***; once exercised the *Rentenbeginn* may no longer be deferred | [S7] § 1 Ziffer 8; the window is that carrier's |
| Death benefit in the *Aufschubphase* | The accumulated capital **excluding the running *Indexjahr***, floored at **50 % of the *Beitragssumme*** | [S7] § 1 Ziffer 5; floor **[std]** (23) |
| *Selbsttötung* | No liability on a death cover within three years of conclusion or reinstatement; the *Rückkaufswert* is then owed | [R6] [REG-R26] |
| *Schlussüberschussanteil* / *Bewertungsreserven* | Half of the *Bewertungsreserven* determined at the **end of the *Ansparphase*** — § 153 Abs. 4 VVG makes that the relevant date for a *Rentenversicherung*, not the end of the contract — subject to the *Sicherungsbedarf* restriction | [R1] [REG-R9] [REG-R24]; **not modeled** (24) |

22. Taken over from the sibling *klassische Rentenversicherung* **[std]** — and now within 3 % of a
    published figure for an index tariff: Stuttgarter's *Muster-Produktinformationsblatt* for
    *BasisRente index-safe* discloses a guaranteed *Rentenfaktor* of **25,74 € per 10.000 €** on a
    100 €-a-month, age-37-to-67 model case [S11]. The **max-of-two rule is confirmed in a retrieved
    AVB** rather than inherited: "Ergibt sich bei Rentenbeginn auf der Grundlage der Sterbetafel und
    des Rechnungszinses, die wir für den Neuzugang von vergleichbaren sofort beginnenden
    Rentenversicherungen verwenden, eine höhere Rente …, dann wird die höhere Rente garantiert" [S7]
    § 1 Ziffer 4 — and Allianz's Ziffer 1 adds the *Treuhänder* leg for the case where no comparable
    annuity is on sale. R+V also discloses the bases of its guaranteed factor: a *Rechnungszins* of
    **0,1 % p. a.** and "eine auf der DAV-Sterbetafel 2004 R basierende unternehmenseigene vom
    Geschlecht unabhängige Sterbetafel" [S7] § 1 Ziffer 3 — well below the 1,00 % *Höchstrechnungszins*
    that applies to the accumulation guarantee, which is why a *Rentenfaktor* cannot be read off
    `guar_rate`. The base run sets the current factor equal to the guaranteed one,
    so the max-of-two rule is exercised by a test rather than by the base path. A *Rentenfaktor* is the
    arithmetic image of an annuity table plus a guaranteed rate, and the market-standard table is
    **DAV 2004 R**, a *Generationentafel* in attained age **and calendar year** [REG-R49] — the property
    of the Deutsche Aktuarvereinigung, **not public and not redistributed here**. delib ships **[std]**
    proxies and states what a replacement must preserve.
23. **The citation for this row was wrong and is corrected.** The retrieved Zurich
    *Verbraucherinformation* — the [S9] chassis — provides the opposite default: "Ist keine der
    folgenden Erweiterungsmöglichkeiten … eingeschlossen, so erlischt im Falle des Todes der
    versicherten Person die Versicherung, **ohne dass eine Leistung fällig wird**", and where cover is
    agreed the standard form is *Beitragsrückgewähr*, a return of **premiums** [S9]. The
    return-of-accumulated-capital form delib models is R+V's: "Stirbt die versicherte Person vor
    Rentenbeginn, wird der Policenwert, mindestens jedoch 90 % der Summe der gezahlten Beiträge
    fällig" [S7] § 1 Ziffer 5, and Allianz's KID shows the same amount in the death and survival
    scenarios [S4]. **Both shapes are in the market**, and delib models one of them. The 50 % floor is
    a **[std]** representative choice whose statutory basis is narrower than stated: EStG § 20 Abs. 1
    Nr. 6 Satz 6 Buchst. a is written for a "**Kapitallebensversicherungsvertrag**", not for the
    *Rentenversicherung mit Kapitalwahlrecht* that Satz 1 also covers, so reading its 50 % across to
    this product is an inference and stays [unverified] [R14] [REG-R45]. The commencement date is
    exact: § 52 Abs. 28 Satz 8 applies Satz 6 to contracts concluded after 31 March 2009. R+V's own
    floor is 90 % of premiums, comfortably above 50 %. The floor is on in the base run and off on one
    model point, keeping the plain return-of-capital form testable.
24. The *Bewertungsreserven* leg is path- and balance-sheet-dependent in a way a gross liability
    cash-flow model cannot reproduce, and the *Sicherungsbedarf* test [REG-R9] [REG-R18] has for most of
    the last decade reduced the payable half to zero on high-guarantee portfolios. delib models the
    declared *laufende* surplus explicitly and **excludes** these two components, saying so.

### Charges

Nothing about the charge structure is special. Two levels are now established from carrier disclosures
and **delib's acquisition charge turns out to be the market's**; the rest stay **[std]**. The
comparators, both for index tariffs: *Allianz Zukunftsrente IndexSelect*, *Einstiegskosten* "2,5% der
kumulierten Anlagen" plus 1,5 % of the annual payment from year 6, *Verwaltungsgebühren* 3,5 % of the
payment a year plus 1,0 % of the value a year, *Transaktionskosten* 0,1 %, total **1,6 % a year** over
30 years [S4]; *Stuttgarter BasisRente index-safe*, *Abschluss- und Vertriebskosten* 2,50 % of premiums,
*Verwaltungskosten* 9,00 % of premiums plus 0,04 % of the accumulated capital monthly, *Effektivkosten*
**1,80 Prozentpunkte** [S11]. Both sit well inside the "over four percent" level at which BaFin says an
appropriate customer benefit "erscheint zweifelhaft" [R17].

| Parameter | Representative value | Basis |
|---|---|---|
| *Abschluss- und Vertriebskosten* | **2,5 % of the *Beitragssumme***, financed by *Zillmerung*, against a DeckRV § 4 *Höchstzillmersatz* of **25 ‰** ("Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten"), cut from 40 ‰ on 1 January 2015 | **matches both retrieved carrier disclosures** [S4] [S11]; ceiling [R7] [REG-R16] [REG-R20] |
| Acquisition-cost spread | Over the **first five years** | **[std]** (25); [REG-R28] |
| *Verwaltungskosten*, premium-based `β` | **3 % of each gross premium** | **[std]** (26) |
| *Verwaltungskosten*, reserve-based `γ` | **0,25 % of the *Deckungskapital* per year** | **[std]** (26) |
| *Stückkosten* | **36,00 € per policy per year**, inflating at 1,5 % | **[std]** (26) |
| *Stornoabzug* | **2 % of the *Deckungskapital***, subject to the § 169 Abs. 3 floor | **[std]** (27) |
| Option dealing cost and spread | **Inside the Cap**, not a charge line — a wider spread simply produces a lower Cap | structural (28) |
| House-index level fee and volatility-target drag | **Inside the index**, and therefore inside neither the Cap nor the disclosed costs | structural (28) |
| Dividend yield of a price index | **Not a charge at all**, but a permanent give-up of the same order — of the order of 3 % a year on euro-area equity | [unverified]; structural (28) |
| *Effektivkosten* | Required to be disclosed as the *Minderung der Wertentwicklung* to the start of the payout phase; a validation target, not a model input | [R5] [REG-R31] |

25. **Two different rules with two different functions, and delib keeps them apart: the DeckRV governs
    what the insurer may *reserve*** (the *Höchstzillmersatz*, 25 ‰) [REG-R16], while **§ 169 Abs. 3 VVG
    governs what it must *pay*** — at least the *Deckungskapital* obtained by spreading acquisition and
    distribution costs evenly over the first five contract years [REG-R28]. delib's charge profile uses
    the five-year spread, so the floor is satisfied by construction; it is nevertheless computed and
    applied, so a user who shortens the spread sees it bite.
26. Inherited **[std]** from the sibling delib endowment and classic-annuity products, and **below both
    retrieved comparators**: `β = 3 %` of premium sits between Allianz's 3,5 % of the annual payment
    and is far below Stuttgarter's 9,00 % of premiums, while `γ = 0,25 %` of the reserve is a quarter
    of Allianz's 1,0 % of value and about half Stuttgarter's 0,04 % monthly (≈ 0,48 % a year) [S4]
    [S11]. Neither carrier's structure is delib's — Allianz and Stuttgarter both charge on premium
    **and** on value, as delib does, but at higher levels, and Allianz adds a second entry charge of
    1,5 % of the payment from year 6. The values are shipped inputs and are not changed in a
    provenance pass; the effect on the reported *Effektivkosten* is a live sensitivity in
    `technical-notes.md`. The wider frame: the 2024 *Verwaltungskostenquote* was **2,4 %** on one
    measurement and **2,19 %** on another, spread **from under 2 % to over 4 %** [REG-R53], and BaFin
    makes cost a supervisory focus [R16] [R17] [REG-R35].
27. § 169 Abs. 5 VVG permits a deduction **only if it is agreed, quantified and appropriate** — "nur
    berechtigt, wenn er vereinbart, beziffert und angemessen ist" — with a deduction for unredeemed
    acquisition costs expressly ineffective [R2] [REG-R28]. **Both retrieved AVB apply one and both
    put the amount outside the AVB**, which is how the *beziffert* requirement is met in practice:
    R+V states it "in EUR" in the *Verbraucherinformationen* [S7] § 11 Ziffer 2, Allianz in the
    *Versicherungsinformationen* [S2] Ziffer 9.2 Absatz 2 — so **no published deduction level was
    obtained for any index tariff**, and delib's flat 2 % remains **[std]** inside a 0–20 % band.
    Allianz's AVB does disclose the **structure**: the deduction falls away on surrender in the last
    year of the *Aufschubdauer*, and in the last seven years where the insured is at least 55 and the
    contract at least ten years old — a taper delib does not model. Both AVB also carry the § 169
    Abs. 6 power to reduce the surrender value for one year at a time.
28. **These three are the index-specific give-ups, and none appears in any charge table**, so the
    disclosed *Effektivkosten* **understate** the economic give-up relative to holding the index by an
    amount disclosed nowhere — a structural fact about the product class, not a claim about any carrier,
    and the most substantive fair-criticism point in this specification.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| *Rückkaufswert* | The *Deckungskapital* on the calculation bases of the premium calculation, floored by the five-year-spread *Mindestrückkaufswert*, less the *Stornoabzug* | [R2] [REG-R28] |
| Locked-in credits | **Inside** the *Rückkaufswert* — they are guaranteed capital by then, not a contingent entitlement, and § 169 Abs. 7 VVG requires already-allocated *Überschussanteile* to be paid on top of the Abs. 3 amount in any event | [R2]; mechanic firm |
| The running *Indexjahr* | **Not** inside it — the payoff exists only at the year end, and on surrender only a pro-rata *Schlussüberschussanteil* and *Sockelbetrag* are added | [S2] Ziffer 9.2, [S7] § 3 Ziffer 5 (18) |
| *Beitragsfreistellung* | Conversion to a paid-up contract at any time for the end of the current insurance period, **provided the agreed *Mindestversicherungsleistung* is reached** (below it the *Rückkaufswert* is paid instead), on the § 169 Abs. 3–5 value; the index participation continues on the capital and the *Wahlrecht* survives, § 165 Abs. 3 Satz 2 leaving *Überschussbeteiligung* claims untouched | [R3] [REG-R28]; minimum [S7] § 11 Ziffer 9; **not modeled** (29) |
| Premium-default conversion | The insurer's termination converts to *prämienfrei* automatically | [REG-R28] [REG-R30] |
| *Widerruf* / *Kündigung* | 30 days' *Widerruf* for life insurance; *Kündigung* at any time for the end of the current insurance period where *laufende Prämien* are payable | [REG-R23]; [REG-R28] |
| Expiry | There is none — the *Aufschubphase* ends at *Rentenbeginn* with a benefit, not with a lapse | mechanic firm |

29. **German lapse is a three-way decrement** — surrender, *Beitragsfreistellung* and premium-default
    conversion — and the last two keep the policy in force with a reduced benefit and a continuing
    expense loading [REG-R28]. **The reference implementation models surrender only**, because a paid-up
    population's per-policy account diverges from the premium-paying one from the moment of conversion
    and tracking it needs a conversion-cohort ledger. The technical notes say so, state what the paid-up
    path would do, and expose a shortened *Beitragszahlungsdauer* as a model-point column, so the
    deterministic form of the same effect is exercised and tested.

---

## Contractual mechanics

Each subsection states the operative rule, in this document's own words, and says what it does to the
projection. Where a retrieved AVB states a rule in terms, it is now **quoted exactly** and attributed
to the carrier and the edition — *Allianz Zukunftsrente IndexSelect (Plus) E25*, `E---A0025Z0 (014)
12/2025` [S2], and *R+V-IndexInvest-Rentenversicherung* IL55, Stand 01.07.2025 [S7]. A quotation is
evidence about **that** carrier; nothing below generalises a wording to the market on the strength of
one of them.

### The *Überschuss* as an option budget — the financing identity

Each year the insurer declares an *Überschussanteilsatz* out of the surplus its results and the MindZV
permit [R8] [REG-R18]. In the *sichere Verzinsung* arm that rate is credited to the *Deckungskapital* as
interest, on top of the guaranteed *Rechnungszins*. In the *Indexbeteiligung* arm **the same amount is
not credited — it is spent**, becoming the ***Optionsbudget*** with which the insurer buys, for the
coming *Indexjahr*, the option package replicating the promised payoff. With `G` the participating
capital at the start of the *Indexjahr* and `b` the declared rate:

    option budget                       =  b × G
    price of the promised payoff on G   =  b × G      ← the Cap (or the Quote) is set to make this hold

**The Cap is not a marketing parameter. It is the solution of a pricing equation** — which is why caps
move from year to year with no change in the contract, and both retrieved AVB say so in terms. Allianz:
"Den jeweiligen →Cap eines Index legen wir jährlich zu Beginn des →Indexjahres **auf der Grundlage von
Angeboten mehrerer Finanzinstitute** neu fest", the level depending on the year's *Überschussanteile*,
the *Bewertungsreserven* *Sockelbetrag* and "Faktoren des Kapitalmarkts wie der Volatilität und der
Dividendenrendite des jeweiligen Index" [S2] Ziffer 3.3 Absatz 2 b). R+V, on the *Beteiligungsquote*:
"Je niedriger der Preis der Kapitalmarktinstrumente und je höher die Überschussbeteiligung
einschließlich der Mindestbeteiligung an den Bewertungsreserven sind, umso höher ist die
Beteiligungsquote" [S7] § 3 Ziffer 4. **One refinement the AVB force on the identity above**: the budget
is the declared surplus **plus the year's minimum share of the *Bewertungsreserven***, and at Allianz
net of *Verwaltungskosten*; delib models the declared surplus alone. Priced risk-neutrally, the index
arm is worth exactly what the safe arm is worth, the whole difference being the equity risk premium
earned on the option package's delta, less dealing costs. **The product is a redistribution of one
year's surplus across states of the world, not extra return.** And the budget can be zero — "Im
ungünstigsten Fall kann die Überschussbeteiligung Ihres Vertrags der Höhe nach null sein" [S2]
Ziffer 2.1 — in which case the year credits nothing whatever the index does [R1] [R8]. Both AVB go
further and **switch the participation off entirely** for a year in which the *Policenwert* does not
exceed the *Deckungsrückstellung* required for the guarantee ([S2] Ziffer 3.5, [S7] § 2 Ziffer 1).

### The annual *Wahlrecht*

The policyholder elects, once a year and for the coming *Indexjahr* only, between *Indexbeteiligung* and
*sichere Verzinsung*. The election is a contractual right, exercisable without the insurer's consent,
without medical evidence and without charge; doing nothing leaves the policyholder in the arm they were
in.

| Arm | The year's surplus is | Outcome |
|---|---|---|
| *Sichere Verzinsung* | credited to the *Deckungskapital* as interest | certain, positive, immediately guaranteed |
| *Indexbeteiligung* | spent on the index option package | zero in a bad year; a multiple of the surplus in a good one; **never negative** |

**The choice is informed, and the AVB settles it.** The insurer fixes the Cap on market conditions
shortly before the *Indexjahr* starts and the policyholder must elect before it starts; whether the
Cap is announced before the election deadline decides whether the choice is informed or blind. Allianz
notifies the indices, "die Höhe der →Caps der jeweiligen Indizes", the *Partizipationssatz*, the year's
surplus net of *Verwaltungskosten* and the *Bewertungsreserven* *Sockelbetrag* "**spätestens 3 Wochen
vor dem Indexstichtag**", and the election "muss uns **spätestens 7 Tage** vor dem nächsten
→Indexstichtag vorliegen" [S2] Ziffer 3.1; R+V likewise informs the policyholder "jeweils rechtzeitig
vor Beginn eines Versicherungsjahres" and takes the election up to 7 days before it [S7] § 2.
**delib's assumption that the Cap is known at election time is the carriers' rule.** Allianz's default
on silence is not simply "stay where you were": the previous split rolls over only if index
participation was at least 50 %, and otherwise the contract is put to 50 % index participation [S2]
Ziffer 3.2 — a nudge delib does not model. The *Wahlrecht* attaches to the capital, so it survives
*Beitragsfreistellung* [R3] and persists to *Rentenbeginn*, ceasing there ([S2] Ziffer 3.3: "vor Beginn
der Rentenzahlung"). In delib's assumption taxonomy the election is a **behavioural** assumption, not a
contractual or an insurer-discretionary one, and is exposed as a per-year path.

### The *Indexjahr* — the sum of capped monthly returns

**This is the single most important and most misunderstood feature of the product**, and it is now
quotable. Allianz's AVB defines the *maßgebliche Jahresrendite* as follows [S2] Ziffer 3.3
Absatz 2 a):

> "Sie bestimmt sich dadurch, dass die negativen monatlichen Wertentwicklungen und die mit dem
> jeweiligen →Cap (siehe Absatz b)) des gewählten Index gedeckelten positiven, monatlichen
> Wertentwicklungen am Ende eines →Indexjahres aufsummiert werden. Die monatlichen Wertentwicklungen
> entsprechen dabei der prozentualen Veränderung des Index zwischen 2 Bewertungsstichtagen, die wir
> Ihnen jährlich mitteilen. Ergibt sich nach der Aufsummierung eine negative jährliche Summe, setzen
> wir diese auf null."

Negative months in full, positive months capped, the twelve **summed**, the sum floored once at zero:
that is the formula below, clause for clause. The *Indexjahr* is divided into twelve monthly
observation periods. For each month `m` the index level is read at the two *Beobachtungstage* bounding
the month, and

    r(m) = I(m) / I(m−1) − 1
    x(m) = min( r(m), C )              ← capped above at C; NOT floored below
    S    = Σ over m = 1…12 of x(m)     ← summed, NOT compounded
    Indexrendite   = max( S, 0 )       ← the floor is on the YEAR, not on the month
    Indexgutschrift = max( S, 0 ) × G

The three features that define the payoff and must never be separated:

1. **Upside is capped monthly.** A month in which the index rises 8 % contributes `C`, not 8 %.
2. **Downside is not capped at all.** A month in which the index falls 8 % contributes the whole −8 %.
   There is no floor on `x(m)`, only on `S`.
3. **The twelve are summed, not compounded.** Summation is close to compounding for small numbers but
   is not the same, and the contractual formula is a sum.

**Why the asymmetry is the whole story.** The payoff is a *capped cliquet*: the policyholder is long
the index's monthly returns, short a strip of twelve monthly calls struck at `C`, with an annual floor.
Truncating each month's right tail while leaving its left tail intact removes far more expected return
than the cap level suggests. At a monthly standard deviation of 5 % — about 17 % annualised, ordinary
for a broad European equity index — a 3 % cap gives away roughly **one percentage point of expected
return per month**, twelve times a year, against an expected monthly return well under 1 %. The
technical notes do that arithmetic: at those parameters the expected value of a capped month is
**negative**, and the product's positive expectation rests entirely on the annual floor.

**The trap.** The `max(S, 0)` floor operates on the *sum*, not on each month, so it is **not** true that
a year with more up-months than down-months credits something. **It is perfectly ordinary for a year in
which the index finished higher to credit zero** — the research file's constructed Example B is exactly
that case, the index rising 6,44 % and the credit being 0,00 € — and it is a required test.

**And the insurer publishes the same trap, worked, on its own product page.** Allianz sets out two
*Indexjahre* on the EURO STOXX 50 at an exemplary Cap of 3,2 % and *Partizipationssatz* of 75,00 %
[S2] [S5]. In **2020/2021** the twelve monthly movements ran +18,06 % (capped to 3,20 %), +2,26 %,
−2,52 %, +4,45 % (3,20 %), +7,78 % (3,20 %), +1,42 %, +1,63 %, +0,61 %, +0,62 %, +2,62 %, −3,53 % and
+5,00 % (3,20 %) — negative months passing through in full — summing to **15,90 %**, which at 75 % gave
an *Indexpartizipation* of **11,92 %**, against a point-to-point index gain of 43,69 %. In
**2021/2022** the same arithmetic summed to **−26,96 %** and the *maßgebliche Jahresrendite* was
**0 %**. Allianz's own footnote makes delib's arithmetic point for it: "Die Wertentwicklung des EURO
STOXX 50® ergibt sich aus der Differenz der Kurse zu Beginn und zum Ende des Betrachtungszeitraumes,
**nicht aus der Summe der monatlichen Wertentwicklungen**."

**One structural difference from delib's model.** Allianz applies **both** a monthly Cap **and** a
*Partizipationssatz* to the capped sum — "Die →Indexpartizipation ermitteln wir, indem wir die
maßgebliche Jahresrendite … mit dem →Partizipationssatz … multiplizieren" [S2] Ziffer 3.3 Absatz 2.
delib's `cap` payoff form has no participation rate (its `w` is the election share, not a
*Partizipationssatz*) and its `quote` form has no cap, so an Allianz-shaped tariff is **not directly
representable** in the reference implementation. That is a model matter, recorded here and in
`model.md`, and deliberately not acted on in a provenance pass.

### The floor and the *Höchststandsicherung*

An *Indexjahr* can never end below zero: `max(S, 0)` is contractual and universal in this family, and it
is the feature the product is sold on. **The floor is what makes it a life-insurance product rather
than a bet**, and it is genuine — the worst imaginable *Indexjahr* credits zero and leaves the capital
untouched. Whatever *is* credited is **locked in**: at the end of the *Indexjahr* the *Indexgutschrift*
is added to the capital and becomes part of the **guaranteed** capital, no longer at risk in any later
year, earning the guaranteed *Rechnungszins* thereafter like any other part of the *Deckungskapital*,
and entering the base `G` of every subsequent *Indexjahr*. That is the ***Höchststandsicherung***, and
it is what makes the year-by-year floor add up to a path-independent guarantee.

Two consequences. **The ratchet is not free**: each year's option package is a fresh strip on a larger
base whenever the previous year credited something — it finances itself automatically, because the
surplus is declared as a *rate* on that same larger base, which is why the financing identity is
written in rates. And **the guarantee is a floor on the path, not only on the maturity value**: under a
plain maturity guarantee the insurer can recover a bad year with a good one, whereas here every credited
amount is permanent, so the guarantee's cost rises with every good year. A **within-year**
*Höchststandsicherung*, locking in the highest level reached inside the year, is a different and rarer
feature; **no German carrier is established as offering it** and delib implements the annual lock-in only.

### The *Partizipationsquote* variant

Instead of capping each month, the contract credits a fixed fraction `q` of the *year's* index
movement, floored at zero: `Indexrendite = max( q × ( I(12)/I(0) − 1 ), 0 )`. There is no monthly cap
and no monthly asymmetry — a down-month is not penalised relative to an up-month because only the
year's net movement matters — and the whole of the give-up is in `q`. **The two designs are not
equivalent and they fail differently.** The Cap design gives away the *large* monthly moves and is hurt
by volatility even when the year ends well; the *Quote* design gives away a constant fraction in every
state. On the research file's Example A the Cap variant credited **more** (8,90 % against 60 % of a
compounded 13,4548 %); on Example B it credited **nothing** while the *Quote* variant credited 60 % of
6,4402 % — the cleanest possible demonstration that the two are not interchangeable.

### The *Cap-Festlegung* — who sets it, when, and on what

The Cap is fixed **by the insurer, for one *Indexjahr* at a time, before that *Indexjahr* begins**, and
is then binding for its whole length, not adjustable during the year. The determination is a pricing
calculation rather than a discretion in substance, and the directions of movement follow from that:

| If this rises | the Cap | because |
|---|---|---|
| the declared surplus rate (the option budget) | rises | more money buys more upside |
| the index's implied volatility | falls | monthly caps are strips of options, and volatility makes them dearer |
| the index's dividend yield | falls | options are written on the price index; a higher dividend yield lowers the forward |
| the risk-free rate | rises, indirectly | it raises the investment return and hence the surplus available |

**The legal frame, and the distinction this product turns on.** The *Cap-Festlegung* is a unilateral
determination by the insurer of a term deciding the policyholder's return for the coming year, and is
therefore reviewable under **§ 315 BGB** for *billiges Ermessen*: "so ist die getroffene Bestimmung für
den anderen Teil nur verbindlich, wenn sie der Billigkeit entspricht. Entspricht sie nicht der
Billigkeit, so wird die Bestimmung durch Urteil getroffen" (§ 315 Abs. 3 BGB) [R22]. It is **not** an
adjustment under **§ 163 VVG** (*Prämien- und Leistungsänderung*), which lets the insurer reset the
premium where "sich der Leistungsbedarf nicht nur vorübergehend und nicht voraussehbar gegenüber den
Rechnungsgrundlagen der vereinbarten Prämie geändert hat", on an *unabhängiger Treuhänder*'s
confirmation; nor under **§ 164 VVG** (*Bedingungsanpassung*), which needs the clause to have been
declared ineffective "durch höchstrichterliche Entscheidung oder durch bestandskräftigen
Verwaltungsakt" and involves **no trustee at all** [R4] [REG-R27]. **Keeping the three apart is the
most important legal distinction in this product and no delib document may blur it**: redetermining the
Cap exercises a discretion the contract confers, while replacing an ineffective clause changes the
contract. Substituting the index is a third thing again — both retrieved AVB reserve it to the insurer
on material change, with **no trustee and no *Sonderkündigungsrecht*** ([S2] Ziffer 3.7, [S7] § 3
Ziffer 11). **No decided German case on the *Cap-Festlegung* is known**, so the § 315 framing,
doctrinally sound, is untested. German litigation over an Indexpolice does exist — the Verbraucherzentrale
Hamburg sued Allianz over the IndexSelect web advertising and won at first instance (LG München I,
23.03.2018, Az. 37 O 12326/17) before the OLG München dismissed the claim on 04.04.2019 with no
*Revision* admitted [S14] [S16] — but that was a **UWG** case about how the participation was
described, not a review of a cap determination.

### The underlying index, and the move to house indices

The classic underlying is the **EURO STOXX 50** — confirmed as Allianz's, alongside the **S&P 500**,
whose non-euro quotation brings in a *Währungsfaktor* applied to the year return [S2] — and two of its
properties drive the economics. It is
quoted and used as a ***Kursindex*** — a price index, dividends excluded — and options are written on
the price index, so the euro-area dividend yield, of the order of 3 % a year [unverified], **never
reaches the policyholder in any state of the world**: a permanent structural give-up on top of the cap,
invisible to a purchaser comparing the product to "the index". And it is volatile, of the order of
18–22 % annualised [unverified], which makes the monthly cap strip expensive and forces the Cap down.

From the mid-2010s a substantial part of the market replaced it with **bespoke multi-asset indices**,
whose common features are: multi-asset composition, so volatility is structurally lower than an equity
index's; **volatility targeting**, a rule scaling exposure to hold realised volatility at a target often
around 5 % [unverified] — the decisive engineering step, because at a 5 % target the option package
costs a fraction of what it costs on a 20 %-volatility index, so the same budget buys a participation
rate near or above 100 %; an **excess-return construction with an embedded fee** of the order of
0,5–1,5 % a year [unverified], which reduces the return without appearing in any cost disclosure; and a
short live history behind a long backtest. **The honest summary**: the shift moved the give-up from
somewhere the purchaser can see — a 55 % participation rate, a 3 % cap — to somewhere they cannot.
Headline numbers improved; expected outcomes did not necessarily improve with them, because the
financing identity still binds.

**Two such indices are now named from carrier documents**, which is the first evidence in this
specification that the pattern above is real and not a recollection. R+V's underlying is the
***Solactive Multi Anlage Stabil Index* (SOMAS)**, developed for the tariff by R+V and Solactive and
described by the carrier as combining equities, bonds and gold with a "Stabilitätsmechanismus" [S7];
Stuttgarter's are the ***M-A-X Multi-Asset Index*** and a *Grüne Zukunft Index*, the M-A-X described as
investing "in mehreren Anlageklassen, um eine kontinuierliche Wertentwicklung zu erzielen" [S8]. Both
are quota designs, and Stuttgarter's published quota of **70 %** on its house index is far below the
"near or above 100 %" the volatility-target argument predicts, which is a caution against pushing that
argument too far. **No volatility target, no index-level fee and no excess-return construction is
published for either**, so the 5 % target and the 0,5–1,5 % embedded fee remain [unverified] and
nothing about their level is asserted. **No index is named in any shipped delib input file**; the model
parameterises the underlying by an explicit monthly-return path.

### The guarantee at *Rentenbeginn* — *Neue Klassik*

What the contract promises is a ***garantiertes Kapital zu Rentenbeginn***, expressed as a percentage
of the premiums paid — the ***Beitragsgarantie*** — plus every index credit locked in along the way,
and a guaranteed *Rentenfaktor* converting that capital into an annuity. **It is not a guaranteed
annual interest rate on the reserve.** That is the defining feature of *Neue Klassik* and the reason
index products are grouped under that label [S6]: by owing the guarantee only at one future date rather
than at every balance date, the insurer can hold a materially riskier asset mix behind it and generate
the surplus that becomes the option budget. **A model that reserves an Indexpolice as though it
guaranteed the *Rechnungszins* every year overstates the guarantee.** The effective guarantee is
`max( Beitragsgarantie on the premiums paid , guaranteed capital including all locked-in credits )`,
with the second term dominating after a few good years. A projection must carry both, and a test must
assert that the guaranteed capital is monotone non-decreasing.

### Premium and the *Beitragssumme*

The premium is level over the *Beitragszahlungsdauer* and payable annually, half-yearly, quarterly or
monthly, with a *Ratenzahlungszuschlag* for anything but annual. **The premium does not enter the index
formula**: premiums build the capital, while the payoff is struck on `G`, the participating capital at
the *start* of the *Indexjahr*, so premiums paid during a year participate only from the following one.
**Both retrieved AVB say exactly that.** Allianz excludes from the *maßgeblicher Policenwert* "die
Beiträge zur Altersvorsorge mit vereinbartem Zahlungstermin im laufenden →Indexjahr" and *Zuzahlungen*
received after the first month, together with the daily surplus attaching to them [S2] Ziffer 3.3;
R+V's *Bezugsgröße* is "der Wert, der ab Beginn des Versicherungsjahres nach Beitragseingang … das
gesamte Versicherungsjahr vorhanden ist. Dabei werden weitere Beiträge und Zuzahlungen während des
Versicherungsjahres nicht berücksichtigt" [S7] § 3 Ziffer 2. No carrier pro-rates them, and delib's
reading is no longer an assumption.

### Death before *Rentenbeginn*

The *Todesfallleistung* delib models is the **return of the accumulated capital** rather than a sum at
risk, so the *Risikoüberschuss* is small, underwriting is light, and § 161 VVG is close to inoperative
[R6]. **That is one of two shapes in the market, and the retrieved documents show both.** R+V's index
tariff pays "der Policenwert, mindestens jedoch 90 % der Summe der gezahlten Beiträge" [S7] § 1
Ziffer 5, and Allianz's KID shows the same amount in the death and survival scenarios [S4] — the shape
delib models. But the conventional Zurich chassis this specification once cited for it provides the
opposite default: no death benefit at all unless an extension is agreed, and where one is, a
*Beitragsrückgewähr* returning **premiums** rather than capital [S9]. The representative design floors
the benefit at 50 % of the *Beitragssumme*, for the tax reason at footnote 23 [R14] [REG-R45]. Death
mid-*Indexjahr* attracts **no credit in the year of exit**, as for surrender — R+V computing the
*Policenwert* "zum Ende des Monats, in dem der Todestag … liegt" with no index element for the
incomplete year [S7] § 1 Ziffer 5.

### *Rückkaufswert* and *Beitragsfreistellung*

Surrender delivers the *Rückkaufswert* under § 169 VVG: the *Deckungskapital* computed by recognised
actuarial rules on the calculation bases of the premium calculation, floored at the value obtained by
spreading acquisition and distribution costs evenly over the first five contract years, less a
*Stornoabzug* effective only if agreed, quantified and appropriate [R2] [REG-R28]. **Locked-in index
credits are inside the reserve and therefore inside the surrender value** — they are guaranteed capital
by then. **The running *Indexjahr* is not**: a surrender in month 7 forfeits that year's payoff.
*Beitragsfreistellung* under § 165 VVG leaves the capital in place, continues the index participation on
it, preserves the *Wahlrecht*, and gives a reduced guaranteed benefit on the same § 169 value [R3].

### *Rentenbeginn* — *Rentenfaktor* and *Kapitalwahlrecht*

At *Rentenbeginn* the capital is converted at `monthly annuity = capital / 10 000 × Rentenfaktor`, and
the applied factor is the **maximum of the guaranteed factor fixed at issue and the insurer's current
factor at *Rentenbeginn*** — a guarantee with upside. **The index mechanic ends here**: the capital is
fixed, the *Wahlrecht* lapses, and payout-phase surplus is applied to the annuity in payment. The
*Kapitalwahlrecht* takes the capital as a lump sum instead. The annuity itself is out of scope for this
model and belongs to `products/sofortrente/`.

---

## Riders and options

**In scope (modeled or parameterized).** The **annual *Wahlrecht***, as a per-year election fraction `w`,
with four shipped paths — always index, always safe, a constant half-and-half split, and a switch from
the index arm to the safe arm mid-term. The **payoff design**, Cap or *Partizipationsquote*, as a
model-point column, so the two can be compared on an identical index path. The **choice of underlying**,
as a model-point key into an external monthly-return table, with an equity case, a low-volatility house
case and an all-zero case. The ***Kapitalwahlrecht***, deciding whether the terminal capital is reported
as a lump sum or as the annuity it buys. The ***Stornoabzug*** and the **50 % death-benefit floor**, as
model-point switches. And the **shortened *Beitragszahlungsdauer***, the deterministic form of
*Beitragsfreistellung*.

**Out of scope, and said so.** ***Beitragsfreistellung*** as a stochastic decrement (footnote 29);
***Dynamik*** (footnote 10); *Zuzahlungen*; the ***Rentengarantiezeit*** and every other payout-phase
feature, which belong to `products/sofortrente/`; ***Hinterbliebenenrente*** and *Beitragsrückgewähr*;
a ***Berufsunfähigkeits-Zusatzversicherung***, a rider on this chassis in the market and a stand-alone
product in delib (`products/berufsunfaehigkeit/`); the *Schlussüberschussanteil* and the
*Bewertungsreserven* share (footnote 24); and a within-year *Höchststandsicherung*.

---

## Variations across insurers

**This table is now a comparison rather than a record of what could not be compared.** Two carrier AVB
were retrieved in full — Allianz's *Zukunftsrente IndexSelect (Plus) E25*, edition 12/2025 [S2], and
R+V's *IndexInvest-Rentenversicherung* IL55, Stand 01.07.2025 [S7] — and Stuttgarter's published
product documents and current parameters were read, though **its AVB is not published** and its row is
correspondingly thin [S8] [S11]. Three product names are given, all now **established**; **none may add
a fourth**, and a cell reading "not established" means exactly that.

| Feature | Allianz [S2] [S4] [S5] | R+V [S7] | Die Stuttgarter [S8] [S11] | Anyone else | delib **[std]** |
|---|---|---|---|---|---|
| Index AVB obtained; product name | **yes**; Zukunftsrente IndexSelect (Plus) E25 | **yes**; PrivatRente IndexInvest, tariff IL55 | no (AVB unpublished); index-safe | no | composite [S1] |
| Payoff design (Cap / Quote / both) | **monthly Cap *and* a *Partizipationssatz* on the capped sum** | ***Beteiligungsquote* on the year return; no cap** | **quota on the year return; no cap** | not established | Cap; Quote as a switchable variant |
| Cap / quota level, current | Cap **3,2 %** and *Partizipationssatz* **75,00 %**, both illustrative | not published | *Partizipationsquote* **70 %** (Turbo 120 % / 172 %), 1.2.2026–31.1.2027 | not established | 3,00 % monthly; `q` 60 % / 100 % |
| *Mindest-Cap* guaranteed | **none in the AVB** | **none in the AVB** | not established | not established | none |
| Underlying index | EURO STOXX 50, S&P 500 (with a *Währungsfaktor*) | **SOMAS** (Solactive Multi Anlage Stabil Index) | **M-A-X Multi-Asset**, *Grüne Zukunft* | not established | generic, by volatility |
| *Wahlrecht* notice period | election **7 days** before the *Indexstichtag*; splits in 25 % steps | election **7 days** before the *Versicherungsjahrestag* | annual | not established | annual, at the year end |
| Cap announced before the election deadline | **yes** — parameters notified ≥ 3 weeks before | **yes** — "rechtzeitig vor Beginn" | quota published in advance | not established | assumed yes — **correct** |
| Base `G` of the participation | **the *Policenwert* at the start of the *Indexjahr***, excluding that year's premiums | **the *Policenwert* present the whole year**, excluding that year's premiums | not stated (the *budget* is 100 % of *laufende Überschüsse*) | not established | the whole capital at the year start |
| *Garantieniveau* menu | **90 %**; 80 % for IndexSelect Plus | **90 %** | **85 %** (*BasisRente* variant) | not established | 90 % |
| Mid-year exit treatment | **no index credit**; pro-rata *Schlussüberschuss* and *Sockelbetrag* only | **no index credit** (credited at the next year's start) | not established | not established | no credit |
| *Effektivkosten* / total cost | **1,6 % a year** over 30 years; entry 2,5 % of cumulative payments | not retrieved | **1,80 points**; entry 2,50 % of premiums | not established | **[std]**, above |
| *Indexjahr* aligned with the policy year | **not necessarily** | **yes** | **no** — a common 1.2.–31.1. window | not established | aligned |

Parameter bands, restated. Two rows are now placed against real carrier figures; the rest remain
[unverified] assessments and are the reason this specification still carries many **[std]** rows.

| Parameter | Band | Who sits where |
|---|---|---|
| Monthly Cap | 1,5 % – 5,0 %, typically 2,5 % – 4,0 % [unverified] | Allianz illustrates **3,2 %**; 3,3 % recorded in 2018 [S14]; no panel |
| *Partizipationsquote* | 50 % – 80 % on an equity price index; 80 % – 120 % on a house index [unverified] | Allianz illustrates **75,00 %** on equity; Stuttgarter publishes **70 %** on a house index — **below the band** |
| *Garantieniveau* | 80 % / 85 % / 90 % observed; 60 % and 100 % [unverified] | Allianz 90 % / 80 %, R+V 90 %, Stuttgarter 85 %; 100 % statutory for *Riester* [R12] [REG-R43] |
| Declared surplus rate, 2026 | **3,07 % index segment**, 2,62 % Klassik, 2,65 % Neue Klassik | Assekurata survey averages [R20]; Stuttgarter publishes 2,16 % [S8] |
| *Höchstrechnungszins* by cohort | 0,25 % (2022–2024) – 4,00 %; **1,00 % from 2025**, recommended again for 2027 | market-wide [R7] [R18] [REG-R15] |
| Index volatility (annualised) | 15 % – 22 % equity; 5 % – 8 % house index [unverified] | **no target published for either named house index** |
| *Verwaltungskostenquote* 2024; *Ratenzahlungszuschlag* | under 2 % to over 4 %, average 2,19–2,4 %; 2 % / 3 % / 5 % | [REG-R53]; convention [unverified] |
| *Stornoabzug* | 0 % – 20 % of the *Deckungskapital* | **both carriers apply one and neither publishes its level** — it is quantified per contract [R2] |
| *Stornoquote*, market-wide | **2,56 % (2023), 2,51 % (2022)**, by count, all *Hauptversicherungen* | no index-specific rate exists [R19] |

**What does not vary, and what turned out to.** Three things are firm across all three carriers, and
they are the reason a composite is possible at all: **the surplus finances the participation** rather
than sitting beside it; **the year's outcome is floored at zero**, never negative; and **what is
credited is locked in permanently**. The fourth item this section previously listed as invariant —
that monthly returns are capped above and not below — **is not invariant**: it is Allianz's design, and
R+V and Stuttgarter have no monthly cap at all. delib ships both payoff forms, so the model spans the
variation; the specification's choice of the Cap form as representative is a **[std]** choice about
which design to lead with, not a finding about the market.

---

## Regulatory context

**Contract law — VVG.** The hinge is **§ 153**: the policyholder participates in the surplus and in the
*Bewertungsreserven* unless participation is excluded, and such an exclusion can only be made for the
whole of the profit participation; the insurer must allocate by a *verursachungsorientiertes Verfahren*
or another comparable appropriate method; the *Bewertungsreserven* are recomputed annually and half of
the amount determined is paid — **and for a *Rentenversicherung* § 153 Abs. 4 makes the relevant date
the end of the *Ansparphase*, not the end of the contract** — subject to the LVRG's *Sicherungsbedarf*
override [R1] [REG-R24] [REG-R9] [REG-R20]. **§§ 165–170** supply the exit machinery [R2] [R3]
[REG-R28]. **§ 163** (*Prämien- und Leistungsänderung*) permits the insurer to reset the premium where
the ***Leistungsbedarf*** has changed unforeseeably and not merely temporarily against the premium's
calculation bases, the new premium being appropriate and necessary for permanent solvency and an
independent trustee having confirmed both — the policyholder may take a reduced benefit instead — and
**§ 164** (*Bedingungsanpassung*) permits a clause to be replaced **only after it has been declared
ineffective by a highest-court decision or a final administrative act**, and **without any trustee**
[R4] [REG-R27]. Those are the two statutory channels through which this contract's terms can be changed
against the policyholder's will, and **neither of them is the annual Cap**. **§ 161** excludes
suicide within three years, the
*Rückkaufswert* then being owed [R6] [REG-R26]. **§ 155** requires an annual *Standmitteilung* stating
the current status of the policyholder's claims **including profit participation** and disclosing **to
what extent that participation is guaranteed** — which is why a *Standmitteilung* specimen is a
legitimate primary-source class here, and why the research file's gap 4 (no completed *Indexjahr* with
its twelve monthly movements was ever obtained) is its most frustrating absence [S10] [R5] [REG-R25].

**§ 154 and the *Modellrechnung*.** Where the insurer makes quantified statements about possible
benefits beyond the guaranteed ones it must give a *Modellrechnung* on **three** interest rates, which
§ 2 Abs. 3 VVG-InfoV fixes as the *Höchstrechnungszins* × 1,67, that rate plus one point and that rate
minus one point — at a 1,00 % *Höchstrechnungszins*, **1,67 % / 2,67 % / 0,67 %** [R5] [REG-R25]
[REG-R31]. Two things follow from reading § 154 itself. Its Abs. 1 Satz 2 exempts only contracts with
benefits of the § 124 Abs. 2 Satz 2 VAG kind, so **the duty does apply to an Indexpolice** — one more
consequence of the classification at [R15]. And **a *Modellrechnung* for an Indexpolice is intrinsically
awkward**, because the interest assumption drives the option budget, which drives the Cap, which drives
the payoff non-linearly. How German carriers discharge § 154 for this product is **still not
established**: neither retrieved AVB reproduces one.

**Prudential.** § 124 VAG imposes the prudent-person standard with no quantitative investment limits
since 1 January 2016 — permitting derivatives only "sofern diese zur Verringerung von Risiken oder zur
Erleichterung einer effizienten Portfolioverwaltung beitragen" (Abs. 1 Nr. 5) — and § 125 Abs. 5 Nr. 4
ring-fences the *Sicherungsvermögen*, requiring a separate *Anlagestock* section only where life
contracts "**direkt an einen Aktienindex oder andere Bezugswerte binden**" [R9] [R15] [REG-R7].
Buying index options to back an index-participation obligation is the paradigm of a derivative
**hedging a liability the insurer has itself written** — liability and hedge matched by construction,
month for month and cap for cap [R9]. § 139 VAG governs the surplus participation from the supervisory
side and carries the *Sicherungsbedarf* rule [REG-R9]; §§ 140 and 145 govern the RfB [REG-R10]; the
**MindZV** sets the 90 % / 90 % / 50 % minima on the three result sources — § 6 Abs. 1 requiring "90
Prozent der … anzurechnenden Kapitalerträge **abzüglich der rechnungsmäßigen Zinsen**", § 7 90 % of the
*Risikoergebnis* and § 8 50 % of the *übrige Ergebnis*, each floored at zero — so **the guarantee is
funded first and only the excess is shared** [R8] [REG-R18]. The **DeckRV** caps the technical
rate and the *Zillmersatz*
[R7] [REG-R14] [REG-R16], and its § 5 Abs. 3 *Zinszusatzreserve* machinery sits behind the declared rate
this product spends [REG-R17]. Above it all is Solvency II [REG-R1] [REG-R2] [REG-R13].

**Conduct and disclosure.** An Indexpolice is a *Versicherungsanlageprodukt* and therefore a **PRIIP**:
a three-page *Basisinformationsblatt* with a summary risk indicator, four performance scenarios and the
cost tables is required [R10] [REG-R32]. It is a **Category 4** PRIIP: the DAV's *Ergebnisbericht*
records that Ziffer 7 of Anhang II RTS assigns
to that category "Versicherungsanlageprodukte, deren Wertentwicklung teilweise von nicht am Markt
beobachteten Faktoren abhängt" — here the discretionary surplus declaration — with the MRM to be
determined under "einem anerkannten Branchen- oder Regulierungsstandard", which that report supplies
and aligns with the PIA standard used for certified products [R10] [R11] [REG-R32]. Category 4 permits
the insurer's own model for that component, which is why two Indexpolicen with similar mechanics can
publish very different favourable scenarios; the DAV report is generic to Category 4 and says nothing
specific about index mechanics. **A *Basisinformationsblatt* for a German index product was retrieved**
[S4]: risk indicator **1 of 7** at 30 years, a moderate scenario of 2,1 % a year after costs against
3,7 % before, and total costs of **1,6 % a year**. The *Effektivkosten* duty [REG-R31] and **BaFin's
*Merkblatt* 01/2023 (VA)** on *angemessener Kundennutzen* [R16] [REG-R35] complete the frame. The
*Merkblatt* **does not name index products** — it applies to *kapitalbildende Lebensversicherungs­produkte*
as a class and makes the *Effektivkosten* the measure of cost — and BaFin's *Risiken im Fokus 2026*
records that individual products reached *Effektivkosten* "über vier Prozent", above which "erscheint
ein angemessener Kundennutzen zweifelhaft" [R17]. Both retrieved index tariffs sit well below that. A
design that credits zero in a substantial fraction of years while carrying a full acquisition-cost load
is nevertheless exactly what a value-for-money regime exists to interrogate.

**Taxation** — context, not a cash flow; delib publishes gross cash flows and computes no tax. A
*Schicht 3* *Leibrente* is taxed only on its ***Ertragsanteil***, a percentage fixed once and for all by
the age reached at *Rentenbeginn* and read off the statutory table in § 22 Nr. 1 Satz 3 Buchst. a
Doppelbuchst. bb Satz 4 EStG — **17 % at 67, 18 % at 65–66 and 22 % at 60–61** [R13] [REG-R41]. A lump
sum under the *Kapitalwahlrecht* is taxed on the *Unterschiedsbetrag* between the payment and the
premiums paid; where the contract has run at least **twelve years** and the payment falls after the
**62nd** birthday, **only half** that difference is taxable and at the personal marginal rate rather
than by final withholding. **The 62 is a transitional rule, not the enacted text**: § 20 Abs. 1 Nr. 6
Satz 2 EStG says the 60th birthday, and § 52 Abs. 28 Satz 7 substitutes the 62nd "für Vertragsabschlüsse
nach dem 31. Dezember 2011" — so a pre-2012 contract keeps 60. The relief is subject, for contracts
concluded after 31 March 2009 (§ 52 Abs. 28 Satz 8), to the **50 % *Mindesttodesfallschutz***
condition — which § 20 Abs. 1 Nr. 6 Satz 6 Buchst. a states for a "*Kapitallebensversicherungsvertrag*",
so its application to a *Rentenversicherung mit Kapitalwahlrecht* is a reading and stays [unverified]
[R14] [REG-R45]. **The index credits are not separately taxed**:
they are absorbed into the capital as credited, so there is no annual tax event, no *Abgeltungsteuer* on
the year's index gain and no *Teilfreistellung* under the *Investmentsteuergesetz* — the last because
there is no fund. **This tax deferral is one of the two genuine advantages over holding an index fund
directly**, the other being the guarantee. Exercising the *Wahlrecht* is not a change of contract and
does not restart the twelve-year clock [unverified]. The duration-12 / age-62 double threshold is the
strongest single driver of German surrender behaviour and shapes the lapse assumption in the technical
notes [REG-R45].

**The criticism, stated fairly, because a specification that omits it is not a specification.** Its home
is the German consumer publishers and trade press — Finanztip [S12], Stiftung Warentest [S13], the
Verbraucherzentralen [S14] and the trade titles [S16]. **Two of the four were retrieved and are now
quoted**; *Finanztest* stays behind its paywall [S13] and no figure is taken from it. Finanztip's
assessment, from its own press release: returns "von mehr als 4 Prozent sind aber nur schwer zu
erreichen", with "nach Abzug aller Kosten Werte von 0,5 bis 2,5 Prozent" more likely, and "Verbraucher
können oft nicht wirklich nachvollziehen, was sie da eigentlich kaufen" [S12]. The Verbraucherzentrale
Hamburg's, from the release announcing its first-instance win: the participation runs "nicht über die
eingezahlten Beiträge, sondern ausschließlich über die … jährlich zu ermittelnde Überschussbeteiligung",
and the monthly measurement means the annual outcome can fall short of the index "selbst dann …, wenn
der Cap in der Jahresbetrachtung gar nicht überschritten wird" [S14]. **The first of those is this
specification's own characterisation, put by a consumer body; the second is Example B.** Both are
positions, and the litigation they came from was decided the other way on appeal [S16]. The cap's
effect on the expected credit is large and is not
disclosed in a usable form: the purchaser is told the cap, is not told the volatility, and cannot do the
calculation. Negative months are uncapped, which is genuinely counter-intuitive. Against a direct index
investment the product loses on every axis but two — it gives up the dividends of a price index and the
tail of every good month, and adds acquisition, administration and possibly index-level costs — but
**what it gives back is real**: the capital cannot fall, credits lock in permanently, the guarantee is
the insurer's, and the accumulation is tax-deferred with a favourable exit. The Cap is redetermined
annually at the insurer's discretion, constrained in principle by § 315 BGB and by no decided case on
that point [R22]; the move to house indices moved the give-up out of sight, and the two now named
publish no volatility target or index fee [S7] [S8]; and complexity is itself a defect in a retail
product — a point the LG München I accepted in 2018 and the OLG München rejected in 2019 [S14]
[S16]. **The counter-argument, fairly stated**: the relevant benchmark for most purchasers is
not an index fund but the *sichere Verzinsung* arm of the same contract, and against that the index arm
has a higher expected value, cannot do worse than zero in any year, costs nothing extra, and can be
abandoned at any anniversary. The reference implementation lets a reader run that comparison.

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
[R20]: #delib-indexpolice-r20
[R21]: #delib-indexpolice-r21
[R22]: #delib-indexpolice-r22
[R3]: #delib-indexpolice-r3
[R4]: #delib-indexpolice-r4
[R5]: #delib-indexpolice-r5
[R6]: #delib-indexpolice-r6
[R7]: #delib-indexpolice-r7
[R8]: #delib-indexpolice-r8
[R9]: #delib-indexpolice-r9
[REG-R1]: #delib-reg-r1
[REG-R10]: #delib-reg-r10
[REG-R13]: #delib-reg-r13
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R25]: #delib-reg-r25
[REG-R26]: #delib-reg-r26
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R30]: #delib-reg-r30
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R41]: #delib-reg-r41
[REG-R43]: #delib-reg-r43
[REG-R45]: #delib-reg-r45
[REG-R49]: #delib-reg-r49
[REG-R53]: #delib-reg-r53
[REG-R7]: #delib-reg-r7
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
