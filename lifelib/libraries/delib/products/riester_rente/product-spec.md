# Product Specification

**Status:** Draft, 2026-08-29 (access date for every citation below).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modelling of a German **klassische Riester-Rentenversicherung** — the
general-account deferred annuity, sold to an individual, **certified** as an
*Altersvorsorgevertrag* (the statutory contract type of the AltZertG) and therefore drawing the
state *Zulage* (subsidy) and carrying the statutory 100 % *Beitragsgarantie*. It describes no
single insurer's contract. [S#] and [R#] tags refer to the source list in `sources.md` (numbering
carried from `_research/riester_rente.md` and frozen — never renumbered, with unused ids simply
omitted); [REG-R#] tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R1–R56 numbering is separately
frozen. **[std]** marks a standardization introduced for the reference implementation; each
**[std]** row carries a numbered footnote giving the rationale and, where one exists, the observed
range. [unverified] marks a claim no search result corroborated.

**How this composite is built, and why it is built the other way round from `frlib`'s.** In
`frlib/products/temporaire_deces` the representative design was the carrier whose document published
the most; here that was impossible when this page was drafted and is, unusually, largely
unnecessary. **The carrier evidence is now thin rather than absent**: three wordings were retrieved
and read — the classic GDV *Musterbedingungen* [S2] and two insurer AVB, CosmosDirekt's LA 1005 A
[S4] and Debeka's B LV 94 [S6] — so one full numbered charge basis, two carrier *Rechnungszinsen*
and one *Rentenfaktor* construction are now in hand, while **no *Überschuss* declaration and no
market-wide level was established at any house for any year** (gaps 12, 13). One observation is not
a market, so the composite's levels stay **[std]** and say where they differ from the one tariff in
hand. But the
half of this product that makes it a *Riester* contract rather than a private annuity
is **not a composite at all**: the Zulagen, the eligibility rules, the *Mindesteigenbeitrag*, the
guarantee, the earliest payout age, the 30 % lump-sum cap, the five-year cost spreading, the
*Wechselrecht* and the taxation are **statute, identical for every provider and every chassis** [R1]
[R6] [R7] [R9] [R10] [R12] [R14] [REG-R42] [REG-R43]. The composite therefore takes **every
statutory parameter as fact and makes every carrier parameter [std]**, anchored so the worked
example reproduces exactly.

**Retrieval conditions, stated because a reader of this page alone must learn them here.** This page
was **drafted** with no research channel at all — direct HTTP egress was blocked by an organisation
network policy and the session's `WebSearch` budget was exhausted before this product's research
began — so its first draft rested on the authoring model's own knowledge of German pension and
insurance law, disciplined by tagging every specific number, with a handful of facts inherited from a
sibling `delib` research session [S3] [S4] [S5] [R22] [REG-R44]. It has since been **re-verified
against the primary documents**: the statutes were read as canonical XML with each law's *Stand*
recorded, and the GDV model wordings, two insurer AVB and four statutory
*Produktinformationsblätter* were retrieved as PDFs and read. Of the forty-two source entries behind
this product, **twenty-six now record `Retrieved: yes`** (62 %), two are part-retrieved and fourteen
are not — those fourteen being documents that could not be located rather than documents behind a
paywall, and `sources.md` names each. So a `delib` citation here is a **certificate where its entry
says `Retrieved: yes`, and a pointer where it does not**: treat the statutory half of this page as
read and the carrier levels as provisional. **Out of scope**, named so the boundary is explicit:
*Wohn-Riester* in both limbs [R3] [R13] [R19] [S13]; the **Riester-Fondssparplan** and
**Riester-Banksparplan** [S9]–[S12]; the **fondsgebundene** Riester wrapper [S1], whose chassis is
`products/fondsgebundene_rentenversicherung/`; the **Basisrente** of Schicht 1,
`products/basisrente/`; Riester inside the *betriebliche Altersversorgung*; and
*Gruppenversicherung*.

---

## Product overview and market role

A Riester contract is an ordinary **private-law contract** — here a *Lebensversicherungsvertrag*
governed by the VVG [REG-R22] — that has additionally been **certified** under the
*Altersvorsorgeverträge-Zertifizierungsgesetz* [R1] [R2] [REG-R43]. Certification does not change
the contract's legal nature; every VVG mechanic that reaches a Schicht-3 deferred annuity reaches
this one too, **subject to** three AltZertG overrides. Those three overrides are the whole product:

1. **Money comes in from the state, as a contribution rather than a benefit** [R8] [R9]. § 90
   Abs. 2 EStG has the *Zentrale Zulagenstelle für Altersvermögen* (ZfA) pay the Zulage **to the
   provider**, and "Der Anbieter hat die erhaltenen Zulagen unverzüglich den begünstigten Verträgen
   gutzuschreiben" [R11]; it is then invested and taxed at the end like any other contribution, and
   it never reaches the saver's bank account. Both retrieved carrier wordings go further than the
   statute and apply each Zulage **to increase the insured benefit**, computed at the date of
   receipt on the tariff in force at inception [S2] [S4] — a mechanic this model does not represent,
   crediting the Zulage to the account instead.
2. **A guarantee is compulsory**: AltZertG § 1 Abs. 1 Satz 1 Nr. 3 requires the provider to promise
   "dass zu Beginn der Auszahlungsphase zumindest die eingezahlten Altersvorsorgebeiträge für die
   Auszahlungsphase zur Verfügung stehen und für die Leistungserbringung genutzt werden" [R1]
   [REG-R43]. That the **Zulagen count too** is not settled by the statutory words — EStG § 82
   defines *Altersvorsorgebeiträge* as what the saver pays [R8] — but is settled by the wordings,
   which promise "mindestens die bis dahin gezahlten Beiträge **und die uns zugeflossenen staatlichen
   Zulagen**" [S2] [S4] [S6]. Without the promise there is no certification and so no subsidy, which
   makes the *Beitragsgarantie* the entry ticket rather than a feature.
3. **The exit is closed.** Surrender is permitted by contract law and punished by tax law: a
   *schädliche Verwendung* triggers repayment of **all Zulagen credited and all § 10a relief
   granted**, and taxes the return on the subsidised part [R14] [REG-R42].

In the *Alterseinkünftegesetz* taxonomy [R18] [REG-R38] this is **Schicht 2** — subsidised
supplementary provision, relieved on the way in and taxed **in full** on the way out under
§ 22 Nr. 5 EStG [R12], with no *Ertragsanteil*. Schicht 1 (*Basisrente*) is relieved more
generously and is completely illiquid; Schicht 3 is unrelieved and liquid. Riester sits between
them on both axes, and is in the German market's own description the layer designed for the
employed household of modest income with children. **The subsidy is the product**: stripped of the
Zulagen and the § 10a deduction, a Riester annuity is a *worse* Schicht-3 annuity — the same
general-account chassis, more constraints, full taxation instead of the *Ertragsanteil*.

**Certification is not endorsement, and no document in this library may suggest otherwise.** The
certifying authority is the *Bundeszentralamt für Steuern* (AltZertG § 3 Abs. 1), which took the
function over from the BaFin on **1 July 2010** (§ 14 Abs. 5). It confirms only that a contract's
**terms** satisfy the § 1 criteria, and the statute rules out the wider reading in one sentence
worth quoting rather than paraphrasing — § 3 Abs. 3: "Die Zertifizierungsstelle prüft nicht, ob ein
Altersvorsorge- oder ein Basisrentenvertrag wirtschaftlich tragfähig und die Zusage des Anbieters
erfüllbar ist und ob die Vertragsbedingungen zivilrechtlich wirksam sind." [R2] [S15] [REG-R43].
The *Beitragsgarantie* is accordingly the **provider's own**, and its ability to honour it is an
ordinary solvency question under the VAG [REG-R5] [REG-R6].

### The four certified chassis, and which one this is

| Chassis | Provider | Accumulation | Guarantee met by | Payout | In `delib`? |
|---|---|---|---|---|---|
| **Klassische Riester-Rentenversicherung** | life insurer [S2] [S4]–[S8] [S16] | *Deckungskapital* at the *Rechnungszins*, plus *Überschussbeteiligung* | the general account and the guaranteed interest | lifelong annuity at a *Rentenfaktor* | **yes — `riester_rente`, `Riester_DE_S`** |
| Fondsgebundene Riester-Rentenversicherung | life insurer [S1] | *Anlagestock* units plus a **Garantie-Deckungskapital** held in the insurer's other assets | in the GDV model wording, a **static two-pot split** of each contribution and Zulage [S1]; i-CPPI and the *dynamisches Hybridmodell* are carrier variants the model wording does not describe `[unverified]` | lifelong annuity, the *Anlagestock* units moved into the general account at *Rentenzahlungsbeginn* [S1] | chassis in `fondsgebundene_rentenversicherung` |
| Riester-Fondssparplan; Riester-Banksparplan | *Kapitalverwaltungsgesellschaft* — Union Investment [S9], DWS [S10], Deka [S11]; *Sparkassen* and *Volks- und Raiffeisenbanken* [S12] | fund units; a deposit balance plus a bonus scale | a *Depotsteuerungskonzept* reallocating between a **Sicherungs-** and a **Chancenkomponente** [S9]; trivially on a bank plan, since a deposit cannot fall below its deposits | *Auszahlungsplan* to the 85th year then a lifelong annuity [S9] [S10] | no |
| Wohn-Riester (*Bausparvertrag*, *Darlehen*) | *Bausparkassen* [S13] | savings, then a loan | not applicable | property use plus the *Wohnförderkonto* | no [R13] [R19] |

The model represents the **first row**, for three reasons: the *Beitragsgarantie* there interacts
with an **actuarial** mechanic, the *Rechnungszins*, rather than an asset-allocation algorithm, so
its cost is visible in the recursion instead of hidden in a rebalancing rule; the payout is an
insurance annuity throughout, so the whole contract is one liability; and the GDV still maintains a
**2025-vintage** classic model wording, "Stand: 21.07.2025" — a date now read off page 1 of the
document itself [S2], reached from the association's own index [S3], and itself the finding that the
classic chassis is a live, separately drafted contract type. A carrier wording of the same vintage
exists too: Debeka's B LV 94 carries an edition date of **1 January 2025** [S6].

### Market role, and the fact that this is a closed book

**Riester is closed.** The reform is now visible in the statutes themselves. The AltZertG's *Stand*
line records amendments by "Art. 5 / Art. 6 / Art. 7 **G v. 26.5.2026 I Nr. 156**", and the VVG's by
"Art. 12" of the same act [R26]; AltZertG § 5 now grants certification "nach § 1 Absatz 3 **in der ab
dem 1. Januar 2027 geltenden Fassung**" against a § 1 with new paragraphs 1b, 1c and 1d, and EStG
§ 93 Abs. 3 Satz 2 Nr. 2 adds a *Kleinbetragsrente* limb for "eine monatliche Leistung **ab dem
1. Januar 2027**" under an *Auszahlungsplan*. So an act of **26 May 2026, BGBl. I 2026 Nr. 156**
amended both the certification statute and the contract-law statute with effect from **1 January
2027** — which is the promulgation date and BGBl citation the library previously recorded as not
established. Three cautions hold. The consolidation is **incomplete**: § 5 refers to paragraphs of
§ 1 the retrieved text does not yet contain, so nothing may be asserted about the new contract
forms. The **act's own title was not read**, so no `delib` document may name it. And the
***Altersvorsorgedepot*** as the reform's central vehicle, and the Bundesrat approval date of 8 May
2026, are `[unverified]` and remain carried from [REG-R44]. Existing contracts are grandfathered.
**That changes what this specification is**: it describes a product with a very large in-force book
whose contractual rights survive — exactly what a liability cash-flow model is for — and it is why
the reference implementation's anchor cell is an **in-force** contract at a 1 January 2027 valuation
date rather than a new policy. The product research file, written without a research channel,
recorded the reform status as its most important open question (gap 1); [REG-R44] closes it from
the cross-product sweep, and this document follows [REG-R44].

**Scale.** Everything here is `[unverified]` order-of-magnitude recollection: **no market figure
was established** — the official series was not located in either pass — and gap 2 qualifies all
of it. Of the order of **15 to 16 million** certified contracts existed in the mid-2020s, having
peaked near **16,5 million** in the late 2010s — insurance contracts roughly two thirds of the
count, fund savings plans roughly a fifth, Wohn-Riester a little over a tenth, bank savings plans
the remainder [R25]. **New business had effectively stopped before the statute closed it**, dating
from the 0,25 % *Höchstrechnungszins* regime of 2022 [R22] [REG-R15], when the three large fund
houses withdrew their savings plans and a substantial number of insurers followed. A large minority
of the book — commonly reported at a fifth to a quarter, three to four million contracts — is
***beitragsfrei gestellt***: in force, certified, guaranteed on what was paid, receiving nothing
further [R25] [unverified]. There is **no official statistic for that figure at all**, and it is
nonetheless the most model-relevant market fact here: ***Beitragsfreistellung*, not surrender, is
this product's characteristic exit**, and a model carrying only a lapse rate has mis-specified the
book. Two counting warnings follow: a contract counted as "Riester" in an official statistic **may
be a mortgage** [R19] [S13]; and a Riester annuity of a given gross amount is worth materially
**less** to the saver than a Schicht-3 annuity of the same amount, being taxed in full [R12] rather
than on the *Ertragsanteil* [REG-R41].

---

## Representative specification

Every statutory row below is a fact about the product; every carrier row is **[std]**, because
nothing carrier-specific was established (gap 12). Amounts in prose use German number formatting
(`1 575,00 €`); amounts inside tables and code use `1,575.00`.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type and wrapper | Single-life **klassische Riester-Rentenversicherung**: a deferred general-account annuity, participating (*Überschussbeteiligung*), written as an individual insurance contract under the VVG and certified as an *Altersvorsorgevertrag* — certification being an administrative act on the **tariff**, not on the policy. Layer: **Schicht 2**, relieved in and taxed in full out | [R1] [R2] [R12] [R18] [S2] [S15] [REG-R22] [REG-R38] [REG-R43] |
| Eligibility (a saver attribute, not a policy attribute) | *unmittelbar zulageberechtigt* — the closed list of **§ 10a Abs. 1 EStG**, to which § 79 Satz 1 refers: compulsorily insured in the *gesetzliche Rentenversicherung*, recipients of *Besoldung* and *Amtsbezüge*, certain insurance-free and exempted employees with an equivalent *Versorgungsrecht*, *Beamte* on unpaid leave, and (Satz 3) *Landwirte* and persons in an *Anrechnungszeit*. *Arbeitslosengeld* recipients, parents in *Kindererziehungszeiten* and *geringfügig Beschäftigte* who did not opt out reach the list through the compulsory-insurance limb, not by name. Full *Erwerbsminderungs-* and *Dienstunfähigkeitsrentner* come in through § 10a Abs. 1 Satz 4, **only if they belonged to a favoured group immediately before the benefit and only until the 67th year is completed**. *mittelbar* — § 79 Satz 2: the spouse of an eligible person, no permanent separation, EU/EEA residence, an **own** certified contract whose payout phase has not begun, and at least **60 Euro** paid to it in the contribution year. **Not** eligible: the self-employed outside compulsory insurance and members of the *berufsständische Versorgungswerke*, who are directed to the **Basisrente** instead — so the two subsidised products are **complements addressed to different people, not competitors** | [R7] [R10] [R20] [REG-R42] |
| Entry ages | 16 to the low sixties in practice; no statutory ceiling, but the accumulation must end at or after the earliest payout age | envelope **[std]** (1) |
| Start of the payout phase | Not before the completed **62nd** year of life (AltZertG § 1 Abs. 1 Satz 1 Nr. 2); the completed **60th** for contracts concluded **before 1 January 2012**, by the transitional rule of **§ 14 Abs. 2**, not by § 1. The alternative trigger is a benefit from a statutory old-age scheme beginning earlier. Representative *Rentenbeginn* attained age **67** | [R1] [REG-R43]; representative age now evidenced — AltvPIBV § 14 Abs. 1 Nr. 2 sets the statutory model case at the completed 67th year [R5] — see (2) |
| Sex as a rating factor | **Prohibited by the certification statute itself**: AltZertG § 1 Abs. 1 Satz 1 Nr. 2 requires "eine lebenslange und **unabhängig vom Geschlecht berechnete** Altersversorgung", and both retrieved wordings say so in terms [S2] [S4]. Riester preceded the general German market, which followed *Test-Achats* | [R1] [R23] [REG-R34]; **the 1 January 2006 and 21 December 2012 dates keep their `[unverified]` tags** — a consolidated statute shows the rule, never the date it entered |
| Lives basis | Single life. A survivor's benefit is a rider, not a second life in the base design | [R1] [S16] |
| Benefit form | **Lifelong** *Leibrente* whose payments "müssen während der gesamten Auszahlungsphase gleich bleiben oder steigen" — a falling annuity is not certifiable, nor is a pure drawdown with no lifelong element. Up to twelve monthly payments may be combined into one. The alternative topology, an *Auszahlungsplan* with *Teilkapitalverrentung* from at the latest the **85th** year of life, is the fund and bank chassis's form [S9] [S10] and is **not implemented here** | [R1] [REG-R43] |
| New business | **Closed from 1 January 2027**; in-force contracts grandfathered | [REG-R44] |
| Anchor model cell | In force at 1 January 2027: female, entry age 47 in 2024, attained age 50, duration 3, *Rentenbeginn* 67, *Rechnungszins* 0,25 %, one child born 2010, full *Mindesteigenbeitrag*, 30 % *Teilkapitalauszahlung*, 10-year *Rentengarantiezeit* | **[std]** (3) |

Footnotes to **[std]** rows:

1. No entry-age envelope was established at any carrier (gap 12). Nothing statutory bounds it below;
   the arithmetic bounds it above, since at 0,25 % a short remaining term leaves almost no room for
   charges — late entry is real but structurally hostile, and the model point table carries one.
2. The representative age is no longer a bare **[std]**: AltvPIBV § 14 Abs. 1 Nr. 2 fixes the payout
   start of the statutory *Muster* model case at the completed 67th year [R5], and the retrieved
   Union Investment sheets show it in use [S9]. On the **upper** bound, gap 10 is answered
   contractually rather than statutorily: no statutory ceiling on the start of the payout phase was
   found, but CosmosDirekt's *flexible Altersgrenze* runs "ab der Vollendung des 62. Lebensjahres bis
   maximal zum Alter von **70** Jahren" [S4], and a DWS fund plan says the payout phase begins
   "frühestens ab Ihrem 62., spätestens ab Ihrem **83.** Geburtstag" [S10]. Carriers set the ceiling;
   the statute does not.
3. The anchor is an **in-force** cell for three reasons: the product is closed to new business from
   1 January 2027 [REG-R44], so an in-force cell is what the book contains; a **2024-vintage** tariff
   carries a *Rechnungszins* of **0,25 %** [R22] [REG-R15], the regime the whole guarantee argument
   turns on; and at duration 3 it is still inside the statutory **five-year** acquisition-cost
   spreading window [R1], so the anchor exercises the AltZertG charge rule rather than describing
   it. Model point 2 is the *same contract projected from its own inception*, reconciling the
   anchor's opening balances.

### Contributions

The contribution is the product's most distinctive mechanic and the one a foreign reader is most
likely to get wrong: **it is not a premium the insurer sets, but a statutory minimum the saver must
reach to draw the subsidy, computed from the saver's own income and reduced by the Zulagen.**

| Parameter | Representative value | Basis |
|---|---|---|
| *Mindesteigenbeitrag* | `min(4 % × previous calendar year's beitragspflichtige Einnahmen, 2 100 €) − Zulagenanspruch`, floored at the *Sockelbeitrag*. § 86 Abs. 1 Satz 2 sets it out in that order — 4 % of the prior year's contribution-liable earnings, "jedoch nicht mehr als der in § 10a Absatz 1 Satz 1 genannte Höchstbetrag, vermindert um die Zulage nach den §§ 84 und 85" | [R10] [REG-R42] |
| Percentage | **4 %** (§ 86 Abs. 1 Satz 2). The phase-in at 1 % (2002–03), 2 % (2004–05), 3 % (2006–07) and the 2008 arrival at 4 % are **historic and not in the consolidated text** | [R10]; rate confirmed, history [R17] `[unverified]` |
| Cap on the base; floor on the result | **2 100 €**, the § 10a Abs. 1 Satz 1 ceiling itself — § 86 cross-refers to it rather than restating it, so the two can never diverge. **Where one spouse is only *mittelbar* eligible the ceiling rises by 60 € to 2 160 €** for the deducting spouse (§ 10a Abs. 3 Satz 3). *Sockelbeitrag* **60 €** a year "ab dem Jahr 2005" (§ 86 Abs. 1 Satz 4). That the 2 100 € has **not been raised since 2008** is a historical claim the consolidated text cannot support | [R6] [R10] [REG-R42]; the "since 2008" claim `[unverified]` |
| Reference income; under-payment | The base is the **previous** calendar year's income, so the entitlement for contribution year `t` is a function of income in `t − 1`; and under-payment is **proportional, not a cliff** — § 86 Abs. 1 Satz 6: "Die Kürzung der Zulage ermittelt sich nach dem Verhältnis der Altersvorsorgebeiträge zum Mindesteigenbeitrag." Pay half the minimum, receive half the Zulagen | [R10] [REG-R42] |
| Contribution form (model-point parameter) | (i) `mindest` — the § 86 amount recomputed every year; (ii) `fixed` — a level contractual contribution the saver chose, varied at will | (i) [R10]; (ii) practice [unverified]; both **[std]** (4) |
| Payment frequency and its loading | Annual, half-yearly, quarterly or monthly, normally by SEPA direct debit; fractionation loading 1.0000 / 1.0100 / 1.0200 / 1.0300 | practice [unverified]; loading **[std]** (5) |
| Contribution movements | Three are routine and all three must be representable: an increase restoring the *Mindesteigenbeitrag* after a pay rise; a reduction to the *Sockelbeitrag*; and a complete stop (*Beitragsfreistellung*) | [R10] [R14] [REG-R28] |
| Unsubsidised contributions | Money paid **above** the § 10a ceiling, or in a year of ineligibility, may be paid into the same contract. It enters the account **and the guarantee**, draws **no** Zulage, and is taxed on the *Ertragsanteil* rather than in full | [R12] [REG-R41] |

4. `mindest` is the statutory arithmetic and the base case. `fixed` is retained because German
   Riester tariffs are in practice written with a nominal level contribution and a wide right to
   vary it [unverified], and because the *mittelbar* eligible spouse's contract is a **60 € flat
   contribution drawing a 175 € Grundzulage** [R7] [R10] [REG-R42] — an economically extreme part of
   the book. Neither form was established at any carrier.
5. **One fractionation scale is now established, and it is not the shape the model uses.**
   CosmosDirekt raises its administration charge on the *Eigenbeitrag* — 2,1 % of each contribution —
   by **3,0 / 2,0 / 1,0 percentage points** for monthly, quarterly and half-yearly payment [S4]: an
   addition to a charge **rate**, not a multiplicative loading on the contribution. The model's
   1.0000 / 1.0100 / 1.0200 / 1.0300 scale is therefore still a **[std]** placeholder in both level
   and mechanic. The model treats the loading as a **charge** rather than money credited to the
   account, so raising it never enlarges the guarantee, and on that point the carrier agrees: the
   *Verwaltungskosten* come out of the contribution before it reaches the *Deckungskapital*.

**Worked cases of the § 86 arithmetic**, at the 2018-and-later rates. All rows are `[std] derived`
— exact arithmetic on the [R9] and [R10] inputs, shown so that a reader can redo them:

| Case | Prior-year income | Zulagen | 4 % of income | *Mindesteigenbeitrag* | *Eigenbeitrag* paid | Total into the contract | Zulage share |
|---|---|---|---|---|---|---|---|
| A — single, no children | 40,000.00 | 175.00 | 1,600.00 | 1,425.00 | 1,425.00 | 1,600.00 | 10.94 % |
| B — single, at the cap | 60,000.00 | 175.00 | 2,400.00 → 2,100.00 | 1,925.00 | 1,925.00 | 2,100.00 | 8.33 % |
| C — one child born 2010 | 30,000.00 | 475.00 | 1,200.00 | 725.00 | 725.00 | 1,200.00 | 39.58 % |
| D — two children born from 2008 | 20,000.00 | 775.00 | 800.00 | 25.00 → floor 60.00 | 60.00 | 835.00 | 92.81 % |
| E — *mittelbar* eligible spouse | not applicable | 175.00 | not applicable | 60.00 | 60.00 | 235.00 | 74.47 % |

Three consequences the model must reproduce and a test must assert. **At the *Mindesteigenbeitrag*
the Zulagen do not raise the amount invested; they lower the amount the saver pays** — the total into
the contract is `min(4 % × income, 2 100 €)`, so the Zulagen **substitute** for the saver's own
money, the single most misunderstood feature of the product. **The *Sockelbeitrag* stops binding at
`(60 € + Zulagen) / 4 %`** `[std] derived` — 5 875 € childless, 10 500 € with one pre-2008 child,
13 375 € with one post-2008 child, 20 875 € with two — below which the contribution is a flat 60 €
plus the Zulagen; case D is the product's political case and its actuarial oddity at once, a
household paying **60,00 €** drawing **775,00 €**, a multiple of **12,92×** `[std] derived`. And
**the ceiling binds at `2 100 € / 4 % = 52 500 €`** `[std] derived`, above which the total is frozen
and the subsidy's value falls monotonically with income.

### The Zulagen

**All four current amounts are now read in §§ 84 and 85 EStG** [R9] and their `[unverified]` tags
are removed. The **historic** rates in the first and third rows are a different matter: a
consolidated statute carries only the rate in force, so the 154,00 € *Grundzulage* of 2008–2017 and
both phase-in sequences are `[unverified]` still.

| Component | Amount per year | From | Condition |
|---|---|---|---|
| *Grundzulage* | **175.00**; the 154.00 of 2008–2017 and the 38.00 / 76.00 / 114.00 phase-in over 2002–07 are `[unverified]` | contribution year 2018 — § 84 Satz 1, "ab dem Beitragsjahr 2018 jährlich 175 Euro" | one per eligible saver, own contract; raised by [R21], phased in by [R17], both attributions `[unverified]` |
| *Berufseinsteiger-Bonus* | **200.00**, "einmalig" (§ 84 Satz 2) | first contribution year beginning after 31 Dec 2007 for which a Zulage is claimed (§ 84 Satz 3) | *unmittelbar* eligible under § 79 Satz 1, "das 25. Lebensjahr noch nicht vollendet" at the start of the contribution year. It is **left out of the § 10a *Günstigerprüfung*** (§ 10a Abs. 1 Satz 5) |
| *Kinderzulage*, child born **before** 1 Jan 2008 | **185.00**; the 46.00 / 92.00 / 138.00 phase-in is `[unverified]` | — | per child "für das gegenüber dem Zulageberechtigten Kindergeld **festgesetzt** wird" (§ 85 Abs. 1 Satz 1) |
| *Kinderzulage*, child born **from** 1 Jan 2008 | **300.00** — § 85 Abs. 1 Satz 2, "Für ein nach dem 31. Dezember 2007 geborenes Kind" | — | as above; the entitlement lapses for a year in which the *Kindergeld* is wholly reclaimed (Satz 3) |

**The two *Kinderzulage* rates are a permanent birth-cohort split, not a transition** [R9] [R19]:
a household with a child born in 2006 and one born in 2009 draws 185,00 € and 300,00 €
simultaneously, and a model treating the *Kinderzulage* as a single rate misprices every family
model point that straddles the 2008 boundary. It is **credited to the mother's contract** unless
the parents jointly elect otherwise — § 85 Abs. 2 Satz 1 for married opposite-sex parents, Satz 2
allocating it to the *Kindergeld* recipient for same-sex couples, in both cases with an election
reversible only within the contribution year [R9] [REG-R42] — and it **stops when *Kindergeld*
stops** — normally at the child's 18th birthday, later during education `[unverified]`. So the
Zulage stream on a family contract is a **step function that falls**, typically two or three times
over a contract running thirty or forty years, driven by a household variable the insurance
contract does not observe. That is the most awkward fact in the whole product for a per-policy
projection, and it is why the reference implementation carries the Zulage entitlement as an
**external schedule keyed by model point and projection year** rather than as a scalar.

**The Zulage arrives late.** The saver applies through the provider, normally once, by a
*Dauerzulageantrag*; the ZfA matches the provider's contribution data against the pension
insurance's earnings and *Kindergeld* data and **pays the provider**, who credits the contract
[R11]. The chain is now readable end to end. The claim arises at the end of the contribution year
(§ 88); the application runs to the end of the **second** calendar year after it (§ 89 Abs. 1), or
under a *Dauerzulageantrag* the provider transmits "bis zum Ablauf des auf das Beitragsjahr folgenden
Kalenderjahres" (§ 89 Abs. 3); the ZfA then has the money paid to the provider, who "hat die
erhaltenen Zulagen **unverzüglich** den begünstigten Verträgen gutzuschreiben" (§ 90 Abs. 2). So the
Zulage for year `t` is a cash inflow in `t + 1`, and **the month is prescribed for disclosure
purposes**: AltvPIBV § 9 Abs. 3 requires every *Produktinformationsblatt* calculation to assume "dass
die Zulagen jeweils **am 15. Mai nach dem Beitragsjahr** dem Vertrag gutgeschrieben werden" [R5].
Gap 6 is closed on both limbs it recorded. The credit remains **provisional**: § 90 Abs. 3 lets the
ZfA recognise a wrong entitlement up to the end of the second year after determination, obliges the
provider to debit the account, and has the quarter's reclaims remitted "bis zum zehnten Tag des dem
Kalendervierteljahr folgenden Monats" — so reversals are settled **quarterly**. What is still not
established is the *rate* at which they occur, which is experience data, not statute (gap 16).

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| **Beitragsgarantie** | The wording, as the GDV drafts it: "Wir garantieren, dass zum Rentenzahlungsbeginn (Beginn der Auszahlungsphase) mindestens die bis dahin gezahlten Beiträge und die uns zugeflossenen staatlichen Zulagen für die vereinbarten Leistungen zur Verfügung stehen." Contributions securing *verminderte Erwerbsfähigkeit*, *Dienstunfähigkeit* or *Hinterbliebene* are left out of account, "höchstens jedoch **20 % der Gesamtbeiträge**". It **survives *Beitragsfreistellung*** and is **reduced** by an *Eigenheimbetrag* withdrawal or a *Versorgungsausgleich* deduction | [S2] § 1 Abs. 10 and § 12 Abs. 5, on AltZertG § 1 Abs. 1 Satz 1 Nr. 3 [R1] [REG-R43]; the same words at [S4] § 1 Abs. 2 |
| What the guarantee is **not** | Not a value at any other date; not a floor on the surrender value; not preserved in real terms; not a guarantee of the *annuity*, only of the *capital*; and not extended to the rider premiums | [R1]; see *Contractual mechanics* |
| Conversion capital | `max( Deckungskapital + Überschussguthaben + Schlussüberschussanteil + Bewertungsreserven-Anteil , Σ Eigenbeiträge + Σ Zulagen − carve-out )` | [R1]; which surplus components count **[std]** (6) |
| *Teilkapitalauszahlung* | Up to **30 %** of the capital available at the start of the payout phase, **without** *schädliche Verwendung*; the remainder must be annuitised. AltZertG § 1 Abs. 1 Satz 1 Nr. 4 Buchst. a in terms, and both retrieved wordings implement it — the GDV's at a company-individual percentage footnoted "Maximal 30 Prozent" [S2], CosmosDirekt's at "bis zu 30 vom Hundert" [S4]. Representative election **30 % taken** | [R1] [REG-R43]; election **[std]** (7) |
| Annuity | Lifelong monthly *Leibrente*, paid **monthly in advance**, constant or rising | [R1]; monthly-in-advance `[unverified]` |
| Conversion basis | The **guaranteed *Rentenfaktor*** struck at inception — euros of **monthly** annuity per **10 000 €** of capital converted — is compared at *Rentenbeginn* with the carrier's then-current factor, and the **higher** applies. **Now established for a Riester tariff, and only for part of one** — see (8) | [S6] § 4 Abs. 3; level **[std]** (8), gap 9 |
| Mortality basis for the annuity | The German annuitant table family — **DAV 2004 R**, generational, in its unisex application. **Proprietary, not public, not redistributed here** | [REG-R47] [REG-R49]; proxy **[std]** (9) |
| *Rentengarantiezeit* | Permitted and drafted into the model wording and both carrier wordings; compatible with the constant-or-rising requirement, and the *förderunschädliche* route for an early death in payment. Representative length **10 years** — which is the length the GDV's own worked example uses [S2] § 1 Abs. 7 and Debeka's [S6] § 1 Abs. 5 | [R1] [R14] [S2] [S6]; length **[std]** (10) |
| Surplus in payment | Permitted, but the constant-or-rising requirement constrains which surplus system a Riester contract may use: a system whose declared component can be reduced would make the total annuity fall. Base run **none** — a constant annuity | [R1]; legal reading `[unverified]`; base run **[std]** (10) |
| Death | Before *Rentenbeginn*, **the *Deckungskapital*** — no longer a **[std]** choice but the model wording's own, and named in its title: "Wenn Sie vor dem Rentenzahlungsbeginn sterben, zahlen wir das Deckungskapital" [S2] § 1 Abs. 6, and the same at [S4] § 1 Abs. 4 and [S6] § 1 Abs. 4. Transfer to a **surviving spouse's own certified contract** is *förderunschädlich* (§ 93 Abs. 1 Satz 4 Buchst. c EStG) and, in the GDV wording, free of charge; conversion into a lifelong *Hinterbliebenenrente* is the other *förderunschädliche* route; payment to any other heir is *schädlich* and the *Rückzahlungsbetrag* is deducted first. After *Rentenbeginn*, payments for the remainder of a *Rentengarantiezeit* — which Debeka may commute to the present value of the outstanding instalments [S6] | [R1] [R14] [S2] [S4] [S6]; see (11) |
| *Kleinbetragsrente* | The provider **may** commute the whole capital to a lump sum **without** *schädliche Verwendung*, taxed under the *Fünftelregelung* (§ 22 Nr. 5 Satz 13 EStG → § 34 Abs. 1), with a four-week election to defer payment to 1 January of the following year. **The threshold is 1,5 %, not 1 %**: § 93 Abs. 3 Satz 2 Nr. 1 EStG defines a *Kleinbetragsrente* as one that "1,5 Prozent der monatlichen Bezugsgröße nach § 18 des Vierten Buches Sozialgesetzbuch nicht übersteigt", aggregated across all of the saver's contracts at that provider (Satz 3). On the 3 955,00 € monthly *Bezugsgröße* used here that is **59,33 €**, and the 39,55 € the model implements is **too low** | [R15] [R21] [REG-R42] [REG-R46]; the *Bezugsgröße* itself `[unverified]`; see (12) and gap 7 |

6. **Which surplus components count toward satisfying the *Beitragsgarantie* was not established
   for any Riester tariff** (gap 9), and in particular whether a *Schlussüberschussanteil* — declared
   at *Rentenbeginn*, not a vested balance before it — may close a shortfall. The reference
   implementation **counts all of them**, the provider-favourable reading, and says so; the
   alternative raises the projected guarantee cost and is a named sensitivity in the technical
   notes.
7. German consumer commentary reports the 30 % lump sum as the usual choice `[unverified]`, and
   **gap 10 records that this rests on nothing**. It is adopted for the anchor because it exercises
   the option at its statutory maximum and because the decision is genuinely non-obvious — the lump
   sum is taxed **in full in the year it is paid, with no *Fünftelregelung*** [R12] [R15]. Model
   point 12 takes none.
8. **The construction is now established for a Riester tariff; the level is not.** Debeka's B LV 94
   (01.01.2025) § 4 Abs. 3 defines it in the model's own terms — "Der garantierte Rentenfaktor gibt
   an, wie viel Rente wir Ihnen monatlich je **10.000 Euro** Guthaben … zahlen" — struck on "einen
   Rechnungszins von **0,1 Prozent p. a.** und die unternehmenseigene geschlechtsunabhängige
   Sterbetafel **Debeka 07/16 R (RF)**", compared at *Rentenbeginn* with the factor implied by the
   house's then-current immediate-annuity basis, and "**Die höhere Rente wird ausgezahlt
   (Günstigerprüfung).**" [S6] The denomination, the monthly basis and the higher-of rule are exactly
   what the composite adopted, and the 0,1 % interest basis is the *Sicherheitsabschlag* made
   concrete — close to the 0 % a sibling `delib` file reports for a Schicht-3 tariff. **Two
   qualifications.** In that wording the factor applies only to the capital from further payments,
   the fund holding and further surplus; the annuity from the originally agreed contributions and
   Zulagen is set on the inception basis, so the two-factor construction is a **partial** mechanic
   there and the whole conversion here. And **neither** the GDV model wording nor the CosmosDirekt
   wording contains a *Rentenfaktor* at all [S2] [S4]: they agree the annuity at inception and let
   each Zulage buy an increment on the tariff in force at conclusion. The composite's construction is
   therefore one of at least two live German designs, and the **level** — 29,00 € per 10 000 € per
   month — is **[std]** still. Gap 9 narrows from "not established for any Riester tariff" to "no
   level established, and the design varies by house".
9. The DAV tables are the property of the *Deutsche Aktuarvereinigung*, distributed to members and
   licensees rather than published, and **not redistributable**: `delib` ships none of them and
   quotes no `q(x)` from any of them [REG-R47] [REG-R49]. The shipped table is a **[std] proxy**
   anchored so the worked example reproduces exactly. The one non-optional structural property is
   that the annuity basis is a ***Generationentafel***, two-dimensional in attained age and calendar
   year, because a period-table proxy understates a deferred annuitisation by a margin that dwarfs
   every other assumption in the model [REG-R49].
10. No *Rentengarantiezeit* length and no payout-phase surplus system was established at any carrier
    (gaps 11, 12); ten years is the common German market length `[unverified]`. A constant annuity
    is the base run because the AltZertG constrains which surplus systems are available [R1]; model
    point 12 switches the guarantee period off, making its effect testable by difference.
11. **This footnote recorded a [std] choice that a retrieved document has since confirmed.** The
    GDV model wording is titled "Allgemeine Bedingungen für eine Rentenversicherung **mit Auszahlung
    des Deckungskapitals bei Tod** als Altersvorsorgevertrag im Sinne des AltZertG" [S2] — the death
    benefit is in the document's name — and both retrieved carrier wordings pay the same [S4] [S6].
    The reasoning stands and is now corroborated rather than merely defensible: the *Beitragsgarantie*
    is tested **only at *Rentenbeginn*** [R1], and importing it into the death benefit would create a
    guarantee the statute does not require. The *Deckungskapital* itself is defined in the wording as
    the contributions and Zulagen, **less tariff costs**, accumulated at the *Rechnungszins* — which
    is exactly the model's account, and is also where the Zulagen charge base is settled (15).
12. **The retrieved statute settles the threshold against the composite, and the retrieved model
    wording settles the ordering against it too. Neither has been applied to the model.** The two
    readings were not irreconcilable, only unchecked: § 93 Abs. 3 Satz 2 Nr. 1 EStG says **1,5 %**
    [R15], so the correct threshold on the *Bezugsgröße* used here is **59,33 €** and the model's
    `kleinbetrag_threshold_mth = 39.55` is a third too low. Raising it would make **more** contracts
    commute and shorten the liability, so the composite's choice was prudent but wrong. Separately,
    the model applies the test to the annuity payable **after** an elected *Teilkapitalauszahlung*;
    the GDV wording forbids exactly that — "Eine Abfindung erfolgt nicht, wenn die Leistung nur
    aufgrund einer Teilkapitalauszahlung gemäß Absatz 4 auf eine Kleinbetragsrente sinkt" [S2] § 1
    Abs. 3 — so the test belongs on the annuity **before** the lump sum. Both are model changes: they
    move the worked example and the golden tests, and they are recorded here and deferred rather than
    made silently. What **is** now settled in the composite's favour is who may commute: it is the
    provider's option in both retrieved wordings — "können wir die Rente … abfinden" [S2], "kann die
    Leistung in Form einer einmaligen Kapitalabfindung erfolgen" [S4]. Gap 7 shrinks from three open
    points to one.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Health evidence | **None for the savings contract** — a deferred annuity whose death benefit is the accumulated capital carries no positive sum at risk, so there is nothing to underwrite. A *Berufsunfähigkeits-Zusatzversicherung* or survivor's benefit is separately underwritten on the rider's own basis | design consequence **[std]**; [REG-R29]; rider inventory not established (gap 11) |
| Rating factors | **Entry age and *Rentenbeginn* only.** Sex may not be used [R23] [REG-R34]; smoker status, occupation and health do not enter a savings tariff | [R1] [R23] |
| Eligibility check | Performed by the **ZfA**, not by the insurer: the provider transmits contribution data and the ZfA determines entitlement against the pension insurance's earnings data. Losing eligibility does nothing to the contract — contributions may continue, **unsubsidised**, into the second tax pool | [R7] [R11] [R12] |
| *Rechnungszins* | Chosen by the carrier at or below the *Höchstrechnungszins* in force at conclusion: **0,25 %** from 1 January 2022, **1,00 %** from 1 January 2025. Representative value **0,25 %** for the anchor, a 2024-vintage tariff | [R22] [REG-R14] [REG-R15]; carrier's choice not established (gap 12); representative value **[std]** (13) |

13. The *Höchstrechnungszins* is a **cap on the reserving rate**, not the rate a policy guarantees
    [REG-R14]; a tariff may guarantee less, and no carrier's choice was established. The composite
    uses the cap in force at the tariff's vintage — the highest defensible value, and so the one
    making the guarantee **cheapest**; a lower tariff rate widens the *Garantielücke*, a direction
    the technical notes carry explicitly.

### Charges

**Charge figures now exist in this corpus, and the statement that none did is withdrawn.** Three
retrieved documents carry them. CosmosDirekt's LA 1005 A § 11 is a complete numbered basis:
*Abschluss- und Vertriebskosten* of **1,0 %** of the *Eigenbeiträge* payable over the deferral,
spread over at least five contract years; *Verwaltungskosten* of **2,1 %** of each *Eigenbeitrag*,
**2,1 %** of capital transferred in and **6,0 %** of each *Zuzahlung* or *staatliche Zulage*; a
fractionation loading of **+3,0 / +2,0 / +1,0** percentage points on that 2,1 % for monthly,
quarterly and half-yearly payment; **0,13 %** of the accumulated *Beitragssumme* taken monthly pro
rata from the *Deckungskapital*, also on paid-up contracts; and a payout-phase
*Verwaltungskosten-Rückstellung* of **1,5 %** of the annual annuity [S4]. Union Investment's sheets
disclose *Effektivkosten* of **1,45** and **1,33 Prozentpunkte** with the full § 2a cost list behind
them [S9]. The GDV and Debeka wordings give the **forms** without the levels [S2] [S6].

**Every charge below is nonetheless still [std]**, and the reason has changed: not that nothing is
known, but that **one insurer's tariff is not a market**. The observation now available differs from
the composite in both directions and in mechanic as well as level — see (14) and (15). The
`[unverified]` third-party figures inherited from a sibling session for an Allianz *RiesterRente*
(0,95 € per 100 € of capital formed) and an Allianz *BasisRente* specimen (a 1 575 €
*Abschlussprovision*) [S5] are **superseded** and are cited for nothing.

| Parameter | Representative value | Basis |
|---|---|---|
| Acquisition and distribution costs | Must be spread "gleichmäßig **mindestens auf die ersten fünf Vertragsjahre**, soweit sie nicht als Prozentsatz von den Altersvorsorgebeiträgen abgezogen werden" (AltZertG § 1 Abs. 1 Satz 1 Nr. 8) — and that closing qualifier matters: a percentage-of-contribution charge falls **outside** the spreading rule, which is exactly how all three retrieved wordings treat the charge on a Zulage. The *Höchstzillmersatz* is **25 ‰** of the sum of all premiums, DeckRV § 4 Abs. 1: "Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten" | [R1] [REG-R16] [REG-R43]; the 1 January 2015 effective date `[unverified]` |
| Representative acquisition charge | **2,5 % of the *Beitragssumme*, in five equal instalments in contract years 1 to 5** — against **1,0 % of the *Eigenbeiträge*** at the one carrier now in hand [S4] | **[std]** (14) |
| Administration charge | **4,0 %** of each contribution credited, plus a fixed policy fee of **12,00 € per year** taken from the *Sparbeitrag* while contributions are paid and from the *Deckungskapital* while the contract is *beitragsfrei* — against **2,1 %** of each contribution plus **0,13 %** of the accumulated *Beitragssumme* per year at [S4], the second of which is a fund-based charge the composite has no counterpart for | **[std]** (14) |
| Charge base for the **Zulagen**; *Risikobeitrag* | **The Zulagen are charged. Gap 14 is closed, and the composite's answer is right in kind and wrong in level** — see (15). The *Risikobeitrag* is **zero**, the death benefit being the account value, so the sum at risk is nil by construction | [S2] [S4] [S6] [S9]; level **[std]** (15); (16) |
| Payout-phase loading | Carried **inside the *Rentenfaktor*** as a margin of **30 %** on the actuarially fair factor, not as a separate deduction from each annuity payment. AltZertG § 2a Satz 1 Nr. 1 Buchst. f permits a charge "ab Beginn der Auszahlungsphase als Prozentsatz der gezahlten Leistung", and one carrier levies exactly that — a *Verwaltungskosten-Rückstellung* of **1,5 % of the annual annuity** [S4] | **[std]** (17) |
| *Stornoabzug* on surrender; transfer charge on an *Anbieterwechsel* | **2,0 %** of the account value; **50,00 €**, a fixed euro amount. **The transfer-charge ceiling is now established and gap 8 closes**: AltZertG § 1 Abs. 1 Satz 3 makes it "unzulässig, dass der Anbieter des bisherigen Altersvorsorgevertrags dem Vertragspartner Kosten in Höhe von mehr als **150 Euro** in Rechnung stellt", so the model's 50,00 € sits well inside it — and it is exactly what one fund provider charges [S9], while one insurer charges nothing at all [S4] | § 169 Abs. 5 VVG permits a deduction only "wenn er vereinbart, **beziffert** und angemessen ist" [REG-R28]; [R1] for the cap; both levels **[std]** (14) |
| Disclosed cost measure | ***Effektivkosten*** — "die Minderung der Wertentwicklung des Vertrags bis zum Beginn der Auszahlungsphase durch Kosten in **Prozentpunkten**", **AltvPIBV § 8 Nr. 3 and not the AltZertG**, which never uses the word; computed for the individual offer, on all costs, by a methodology the *Produktinformationsstelle Altersvorsorge* lays down (§ 10 Abs. 5). Two real values are now in this library: **1,45** and **1,33 Prozentpunkte** [S9] | [R5] [S9] [S14] [REG-R43]; no **insurance** value established |
| Risk/return class | ***Chancen-Risiko-Klasse*** 1 to 5, "wobei CRK 1 die niedrigste und CRK 5 die höchste … darstellt" (AltvPIBV § 5 Abs. 2), determined separately for terms of 12, 20, 30 and 40 years from a simulation the *Zertifizierungsstelle* lays down (AltZertG § 3 Abs. 2 Satz 2) and the PIA performs under *Beleihung* (§ 3a) — a feature with **no counterpart in `uslib`, `uklib`, `jplib` or `frlib`**. `delib` does not implement it. **One correction**: the *return scenarios* are public, prescribed in AltvPIBV § 10 (2/3/4/5/6 % before costs for CRK 1–5, and four-scenario sets per class); what is not public is the classification simulation and the *Effektivkosten* methodology. **And a 100 %-guaranteed product does not sit at the low-risk end by construction** — both Union Investment plans carry the statutory *Beitragserhaltungszusage* and one is in **CRK 4** [S9] | [R4] [R5] [S9] [S14] [REG-R43] |

14. Round-number placeholders, and now placeholders **with one observation beside them rather than
    none**. The acquisition rate is set at the § 4 DeckRV cap [REG-R16], a **cap and not a level**,
    on the argument that what binds this product is not the *Höchstzillmersatz* but the AltZertG's
    five-year spreading [R1]. The one retrieved tariff charges **1,0 % of the *Eigenbeiträge*** —
    two and a half times lower than the composite, and on a **narrower** base, since the composite
    applies its 2,5 % to a *Beitragssumme* that includes the Zulagen. Its administration charge is
    **2,1 %** against the composite's 4,0 %, and it takes a **0,13 % of accumulated *Beitragssumme***
    fund charge each year in place of the composite's flat 12,00 €, so the two bases differ in shape
    and not only in size. Its *Stornoabzug* is **nil**, and its transfer charge is **nil** [S4]; a
    fund provider's transfer charge is **50,00 €** [S9], the composite's figure exactly. Debeka's
    *Stornoabzug*, where one is levied, is a **market-value adjustment** of 0 / 5 / 10 / 15 % of the
    *Deckungskapital* keyed to a ten-year swap-rate spread and running off linearly over the last ten
    years of deferral [S6] — a mechanic the composite's flat 2,0 % cannot express. **None of this has
    been applied to the model**: one house is not a market, and a charge change moves the worked
    example and the golden tests. It is recorded so a future calibration starts from evidence.
15. **Gap 14 is closed by four independent documents, and the composite's answer is right in kind
    and wrong in level.** The Zulagen are a charge base. The GDV model wording lists among the
    permitted forms "eines festen Prozentsatzes jedes gezahlten Beitrags **sowie jeder Zulage und
    Zuzahlung**" and "der vereinbarten Beitragssumme **einschließlich Zulagen und Zuzahlung**", and
    adds that acquisition cost on a Zulage is taken **once at inflow**, not spread: "Von Zulagen und
    Zuzahlungen ziehen wir die Abschluss- und Vertriebskosten jeweils einmalig zum Zeitpunkt des
    Zuflusses ab" [S2] § 13 Abs. 2. Debeka drafts the same rule [S6] § 14 Abs. 2. Union Investment
    discloses acquisition cost as a "Prozentsatz der eingezahlten Beiträge (**inkl. Zulagen**)" [S9].
    And CosmosDirekt puts a number on it: **6,0 %** of each Zulage against **2,1 %** of each
    *Eigenbeitrag* [S4] — the Zulagen charged at nearly **three times** the rate. The composite
    charges them **at the same rate as the *Eigenbeitrag***, which the one available observation
    contradicts. It matters exactly where the entry always said it did: in the low-income cases of
    the § 86 table the Zulagen are the **majority** of the contribution. **The model is unchanged**
    and this is flagged rather than fixed.
16. A real product fact, not a simplification: with a death benefit equal to the accumulated capital
    there is no sum at risk and so no *Risikobeitrag* [REG-R47]. A *Beitragsrückgewähr* floor
    **would** create one, which is one reason the composite avoids it.
17. German market *Rentenfaktoren* sit materially below the actuarially fair factor implied by any
    plausible annuitant basis, carrying both the *Sicherheitsabschlag* of a guarantee given decades
    ahead and the payout phase's cost loading — a proposition the 0,1 % interest basis behind
    Debeka's guaranteed factor now makes concrete [S6]. Deducting from each annuity payment **and**
    applying a conservative factor double-counts, so the composite puts the whole loading in the
    factor and takes real payout-phase administration as a per-policy expense cash flow. **The
    German market does the other thing**: AltZertG § 2a Satz 1 Nr. 1 Buchst. f expressly permits a
    payout-phase charge "als Prozentsatz der gezahlten Leistung", CosmosDirekt levies **1,5 % of the
    annual annuity** [S4], and the Muster-PIB has a line for it. The composite's construction remains
    internally consistent and is now visibly a **presentational** standardization rather than a
    market description.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| ***Beitragsfreistellung*** | Contributions stop, the contract stays in force and stays certified, no further Zulagen arrive, and **no subsidy is repaid**. AltZertG § 1 Abs. 1 Satz 1 Nr. 10 Buchst. a gives the right to let the contract lie dormant; § 165 Abs. 1 VVG gives the general contract-law right "jederzeit für den Schluss der laufenden Versicherungsperiode …, **sofern die dafür vereinbarte Mindestversicherungsleistung erreicht wird**" — below which the insurer pays the surrender value instead. **The guarantee survives**: "Die Beitragserhaltungsgarantie … gilt auch bei einer Beitragsfreistellung und bezieht sich auf die gezahlten Beiträge und die zugeflossenen staatlichen Zulagen" [S2] § 12 Abs. 5. The wordings implement it by converting to a paid-up annuity computed on the surrender value [S2] [S4]; the model instead freezes the accumulator and lets the account run on | [R1] [R14] [REG-R28] [S2] [S4] |
| ***Anbieterwechsel*** | A **statutory** right: terminate and have the accumulated capital transferred directly to another certified contract. **Not** a *schädliche Verwendung*, no tax consequence | [R1] [R14] [REG-R43] |
| Notice period and transfer-charge cap | **Both established; gap 8 closes.** Three months to the end of a calendar quarter, or to the start of the payout phase (AltZertG § 1 Abs. 1 Satz 1 Nr. 10 Buchst. b), shortened to 14 days where the pre-payout information came late (§ 7b Abs. 2, drafted at [S2] § 11 Abs. 1). The ceding provider may charge no more than **150 Euro** (§ 1 Abs. 1 Satz 3), and the receiving provider may take at most **50 %** of the transferred subsidised capital into its own acquisition-cost base (Satz 4) | [R1] [R4] [S2] [S4] |
| ***Kündigung*** with payment of the *Rückkaufswert* | Permitted by the VVG and punished by the EStG: the saver receives the surrender value **less** the *Rückzahlungsbetrag* — **all** Zulagen credited and **all** § 10a relief granted — and the growth on the subsidised part becomes taxable | [R14] [REG-R28] [REG-R42] |
| *Rückkaufswert* floor | § 169 Abs. 3 VVG floors it at "mindestens der Betrag des Deckungskapitals, das sich bei **gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre** ergibt" — which the AltZertG's own five-year spreading [R1] already produces, so on a certified contract the § 169 floor is **satisfied by construction**. Both retrieved wordings compute the *Rückkaufswert* on exactly that basis [S2] § 10 Abs. 3, [S4] § 9 Abs. 2 | [R1] [REG-R28] [S2] [S4] |
| Early-duration reality | The surrender value can be, and in the early years of a charged contract usually **is**, **below** the contributions paid. The *Beitragsgarantie* does not floor it — it is tested **once**, at *Rentenbeginn* | [R1] |
| Other *förderunschädliche* exits | *Versorgungsausgleich* on divorce, by internal or external division into the other spouse's certified contract; and an *Altersvorsorge-Eigenheimbetrag*, which from the insurer's side is an early and complete exit terminating the annuity liability. Neither is implemented | [R13] [R14] [R19] `[unverified]` |
| Non-transferability; emigration | § 97 EStG makes the subsidised capital, the subsidised current contributions and the Zulage claim "**nicht übertragbar**" — and that is **all** § 97 says. The protection from attachment is a consequence of it through ZPO § 851 Abs. 1, not a provision of its own, and the separate § 851c route is unavailable to a contract that has agreed a lump sum. The contract wording bars assignment and pledging in terms [S4] § 14 Abs. 2. **Gap 15 closes on emigration**: § 95 applies §§ 93 and 94 correspondingly where the saver's residence is outside the EU/EEA "**ab Beginn der Auszahlungsphase**", so the trigger is the payout phase and not the end of unlimited tax liability. The model implements none of it | [R14] [R16] [REG-R40] |

---

## Contractual mechanics

### Eligibility, the *Mindesteigenbeitrag* and the proportional Kürzung

**Eligibility is annual and is an attribute of the saver.** A saver can be *unmittelbar* eligible in
one year, *mittelbar* in the next and not eligible at all in a third, **without the contract
changing** [R7]; contributions may continue, they are simply unsubsidised, and they move into the
second tax pool [R12]. The rule that decides the whole subsidy stream is therefore a property of the
**person**, not of the contract, and one the insurer does not itself observe — the ZfA does [R11].
The reference implementation carries it as a per-period flag on an external schedule, **[std]**
default "*unmittelbar* eligible throughout", with a dedicated model point exercising a mid-term
lapse.

The contribution rule [R10] [REG-R42], written as the model implements it:

    mindesteigenbeitrag(t) = max( 60 € ,
                                  min( 4 % × income(t − 1), 2 100 € ) − zulage_entitlement(t) )
    eigenbeitrag(t)        = contrib_ratio × mindesteigenbeitrag(t)
    zulage_granted(t)      = zulage_entitlement(t) × min( 1, contrib_ratio )

Three features of the statute drive behaviour and each is a distinct way to get the model wrong. The
base is the **previous** calendar year's contribution-liable earnings. The **Zulage is subtracted**
from it, so a larger subsidy reduces the saver's own payment rather than increasing what the
contract receives. And the sanction for under-payment is **proportional, not a cliff** — an
implementation that treats the minimum as all-or-nothing produces a discontinuity that does not
exist in the statute, and the German book is full of the paths that discontinuity would misprice
[R10] [REG-R42].

### The one-year Zulage lag, and the second lag behind it

**Two distinct lags run in the subsidy chain and they are easy to collapse into one.** The
entitlement for contribution year `t` is computed from income in `t − 1` [R10]; the **cash** arrives
from the ZfA in `t + 1` [R11] [REG-R42]. The reference implementation carries both explicitly:
`income_ref(t) = income(t − 1)` for the entitlement, `zulage_credited(t) = zulage_granted(t − 1)`
for the cash. The one-year cash lag is no longer a bare **[std]**: §§ 88 to 90 EStG put the credit in the year
after the contribution year at the earliest, and **AltvPIBV § 9 Abs. 3 fixes the date at 15 May of
that year** for every statutory disclosure calculation [R5] [R11] — which closes gap 6. What is
standardized is only the compression of a mid-May credit onto the first month of the projection
year.

One consequence is load-bearing and is a numbered pitfall: **the Zulage for the final contribution
year arrives after contributions have stopped**, landing in the conversion year itself, where it
must be credited, counted in the guarantee and included in the conversion capital **before** the
guarantee is tested. Stopping the Zulage stream with the contribution stream silently drops a full
year's subsidy out of both.

### The § 10a *Sonderausgabenabzug* and the *Günstigerprüfung* — and why neither is a cash flow

"Altersvorsorgebeiträge (§ 82) **zuzüglich der dafür nach Abschnitt XI zustehenden Zulage** jährlich
bis zu **2 100 Euro** als Sonderausgaben abziehen" — § 10a Abs. 1 Satz 1 [R6] [REG-R42]. Where one
spouse is only *mittelbar* eligible the ceiling rises by 60 € for the deducting spouse (Abs. 3
Satz 3). The ***Günstigerprüfung*** works exactly as the documents said, by the mechanism they did
not state: where the deduction is the better outcome, "erhöht sich die unter Berücksichtigung des
Sonderausgabenabzugs ermittelte tarifliche Einkommensteuer **um den Anspruch auf Zulage**" (Abs. 2
Satz 1) — the Zulage is added back to the assessed tax, so the saver keeps the **larger** of the two
and not their sum — "In den anderen Fällen scheidet der Sonderausgabenabzug aus. Die
Günstigerprüfung wird **von Amts wegen** vorgenommen." The *Berufseinsteiger-Bonus* is excluded from
the comparison (Abs. 1 Satz 5).

**Only the Zulage is a contract cash flow. The *Günstigerprüfung* top-up is a personal tax refund
and never touches the policy** [REG-R42] — the single most important thing a model author must get
right about the subsidy, and why the model publishes `zulagen` as a column of the cash flow
statement and nothing at all for the § 10a route. The Zulagen route dominates for low incomes and
households with children, the § 10a route for high incomes with no children; **the crossover was not
established** and no crossover figure appears anywhere in this library (gap 5). A *mittelbar*
eligible spouse has no § 10a deduction of their own: § 10a Abs. 3 Satz 2 gives their contributions
and Zulagen to the *unmittelbar* eligible spouse's assessment instead [R6] [R7]. The deduction reaches
the projection in one indirect way only: it is part of what is repaid on a *schädliche Verwendung*
[R14], and therefore part of the reason a Riester lapse assumption should sit materially **below** a
Schicht-3 one.

### The 100 % *Beitragsgarantie*

**What is guaranteed**, in the words of the model wording every German classic Riester tariff is
drafted from: "Wir garantieren, dass zum Rentenzahlungsbeginn (Beginn der Auszahlungsphase)
mindestens die bis dahin **gezahlten Beiträge und die uns zugeflossenen staatlichen Zulagen** für die
vereinbarten Leistungen zur Verfügung stehen" [S2] § 1 Abs. 10, on AltZertG § 1 Abs. 1 Satz 1 Nr. 3
[R1] [REG-R43], less the biometric carve-out — "höchstens jedoch 20 % der Gesamtbeiträge". Note where
the authority for each half sits: the **20 %** and the once-at-*Rentenbeginn* test are statutory; that
the **Zulagen count** is contractual, the statute speaking only of *Altersvorsorgebeiträge*, which
EStG § 82 defines as what the saver pays [R8]. Every wording read here says the Zulagen count [S2]
[S4] [S6]; none of them had to.
In model terms it is a **running accumulator**, not a discounted quantity —
`guar(t + 1) = guar(t) + eigenbeitrag(t) + zulage(t) − carve_out(t)`, frozen once contributions stop
— and at *Rentenbeginn* the conversion capital is `max(account and its surplus components,
guar(T))`. The excess of `guar(T)` over the account, the ***Garantielücke***, is a **cost the
insurer bears out of its own funds** and is the product's signature output. A Riester model in which
the guarantee never binds on any model point has demonstrated nothing, which is why the model point
table carries a low-declared-rate cell on which it bites.

**Six things the guarantee is not**, each of them load-bearing. **Not a value at any other date** —
it is tested once, and before *Rentenbeginn* the surrender value can be, and in the early years
usually is, below the contributions paid. **Not a floor on surrender**: a saver who terminates for
cash gets the *Rückkaufswert*, which the guarantee does not floor, **and** loses the subsidy [R14].
**Not preserved on transfer** — whether the guarantee survives a *Wechsel* is a design question of
the **receiving** contract and is **still not established**, the one limb of gap 8 the statute does
not answer; if the receiving contract's guarantee
runs only on the transferred sum rather than on the original contributions the *Wechselrecht* is
materially less valuable than it appears, and this library cannot say which is right. **Not real**:
it is nominal, and over thirty years at even moderate inflation the floor is worth a fraction of the
contributions in real terms, which is the substance of the most serious criticism of the design.
**Not a guarantee of the annuity** — it is on the **capital**, and what that capital buys is a
separate guarantee, the *garantierter Rentenfaktor*, with which it is routinely conflated. **Not preserved through an *Eigenheimbetrag* or a *Versorgungsausgleich***, both of which reduce it
pro tanto — a limb the library had not carried and which both retrieved wordings state [S2] [S4]. And
**not extended to the risk-cover premiums**, within the statutory 20 % share [R1] [REG-R43], which is why
a Riester contract can carry a *Berufsunfähigkeits-Zusatzversicherung* without the guarantee
reproducing its premiums, and why raising a rider premium must never enlarge it.

### Why the guarantee is the mechanical heart

The guarantee is a **nominal sum, due at a fixed future date, on money paid in over decades**, so
its cost is an interest-rate quantity and nothing else: **to guarantee one euro payable in `n`
years an insurer must immobilise `(1 + i)^−n` of it now**, where `i` is bounded by the
*Höchstrechnungszins* [R22] [REG-R14]. What is left, `1 − (1 + i)^−n`, is the entire budget for
risk assets **and** for every charge the contract will levy.

Stated on the whole contract: for level contributions in advance over `n` years the guaranteed
accumulation is `C × s̈(n, i)`, the guarantee is `C × n`, and the **headroom** is
`s̈(n, i)/n − 1`. All rows `[std] derived`, exact on the [R22] rates; the 0,90 %, 1,75 % and
2,25 % values and their effective dates are themselves `[unverified]` (gap 18):

| Term | 0,25 % (2022–24) | 0,90 % | 1,00 % (from 2025) | 1,75 % | 2,25 % |
|---|---|---|---|---|---|
| 12 years | **1.64 %** | 6.05 % | 6.74 % | 12.14 % | 15.90 % |
| 20 years | **2.67 %** | 10.01 % | 11.20 % | 20.58 % | 27.36 % |
| 30 years | **3.97 %** | 15.24 % | 17.11 % | 32.33 % | 43.82 % |
| 35 years | **4.63 %** | 17.98 % | 20.22 % | 38.76 % | 53.06 % |

On 1 200,00 € a year for thirty years — 36 000,00 € of contributions — the 0,25 % regime produces a
guaranteed accumulation of **37 429,31 €**, a headroom of **1 429,31 €**; the 1,00 % regime produces
**42 159,29 €**, a headroom of **6 159,29 €** `[std] derived`. So at 0,25 % a thirty-year contract
had **under 4 % of contributions** to pay for acquisition, administration, risk and any margin — a
multiple below typical German life charge levels, which made the guarantee not merely expensive but
**arithmetically unfinanceable** on a normally charged tariff. It bites hardest on short terms and
late money, so the product is structurally hostile to late entrants; it **dictates the asset
allocation**, since the equity share is bounded above by a headroom that is a function of `i` and
`n` alone; and **a rate rise repairs it mechanically** — the move to 1,00 % on 1 January 2025
roughly quadrupled the thirty-year headroom, from 3,97 % to 17,11 % `[std] derived`, which is the
arithmetic behind the GDV maintaining a 2025-vintage classic model wording [S2].

One warning about reading the table: it is the arithmetic of the **guaranteed** accumulation, which
is what the insurer must be able to promise. A **best-estimate** projection credits the declared
*laufende Verzinsung*, materially above the *Rechnungszins*, so on a healthy contract the
*Garantielücke* closes long before *Rentenbeginn*. **The guarantee's realised cost is a
declared-rate question, not a *Rechnungszins* question**, and a model that confuses the two reports
a guarantee cost of zero and concludes the mechanic does not matter.

### The five-year cost spreading

Acquisition and distribution costs must be spread "gleichmäßig **mindestens auf die ersten fünf
Vertragsjahre** …, soweit sie nicht als Prozentsatz von den Altersvorsorgebeiträgen abgezogen werden"
[R1] [REG-R43] — a statutory cap on *Zillmerung* aimed at this product specifically, materially
tighter than anything the VVG imposes on a Schicht-3 contract, and, with the *Wechselrecht*, a push
toward lower front-end charges and a thinner acquisition margin `[unverified]` as a market
characterisation. **The closing qualifier is load-bearing and the library had not carried it**: a
charge expressed as a percentage of the contributions falls outside the spreading obligation, which
is why all three retrieved wordings spread the charge on the *Beitragssumme* over five years or
sixty months and take the charge on each Zulage **once, at inflow** [S2] [S4] [S6]. Two model
consequences: the charge basis **cannot front-load the whole acquisition cost into year one**, which
changes the *shape* of the early-duration charge run-off and so of the early-duration surrender
value; and the **commission cash still leaves at issue** while the charge is recovered over five
years, so the new-business strain is carried by the insurer, not by the contract.

### *Rentenbeginn*: conversion, the lump sum and the *Rentenfaktor*

At the contractually fixed *Rentenbeginn*, bounded below by the statutory age [R1], four things
happen in order and the order matters. The **final Zulage** is credited; the **conversion capital**
is struck as the guarantee floor applied to the account's own parts; up to **30 %** may be taken as
a ***Teilkapitalauszahlung*** [R1] [REG-R43], taxed **in full in the year it is paid, with no
*Fünftelregelung*** [R12] [R15], an asymmetry against the *Kleinbetragsrenten-Abfindung* that is why
German consumer literature treats the decision as non-obvious; and the **remainder is annuitised**
into a lifelong, constant-or-rising monthly *Leibrente* at `annuitised_capital / 10 000 € ×
Rentenfaktor`, the higher of the guaranteed and the then-current factor applying. The Riester
*Rentenfaktor* is **unisex from a 2006 vintage** [R23], earlier than the Schicht-3 market, so it is
**not comparable** with a same-vintage Schicht-3 factor for a male life — a comparison German market
commentary makes routinely and wrongly.

### The *Kleinbetragsrente*

Where the monthly annuity would not exceed the statutory threshold — **1,5 % of the monthly
*Bezugsgröße* of § 18 SGB IV**, not the 1 % this library previously chose [R15] — the provider **may**
commute the whole capital to a lump sum, **without** *schädliche Verwendung* [R15] [REG-R42]. The
option is the provider's in both retrieved wordings ("können wir die Rente … abfinden" [S2]), and the
test aggregates all of the saver's contracts at that provider (§ 93 Abs. 3 Satz 3). The *Abfindung*
is taxable in full under § 22 Nr. 5 but under the ***Fünftelregelung***, Satz 13 routing § 93 Abs. 3
payments to § 34 Abs. 1 [R12] [R15]; the deferral election is AltZertG § 1 Abs. 1 Satz 1 Nr. 4
Buchst. a, drafted as a four-week window from the provider's notice with the amount then reserved
"kostenfrei und unverzinst" until 1 January of the following year [S2]. That the *Fünftelregelung*
arrived in 2018 [R21] is `[unverified]`. **This matters far more than the threshold suggests**, which is why the model
carries it as a switch on the anchor decrement rather than as a footnote: the book has a long tail
of small contracts, those run at the *Sockelbeitrag* (§ 86 cases D and E) and those that went
*ruhend* early. Case D contributes 835,00 € a year, so twenty years is **16 700,00 €** of
contributions `[std] derived`; case E contributes 235,00 €, so twenty years is **4 700,00 €** — at
any plausible *Rentenfaktor*, monthly annuities in the tens of euros. **A material fraction of
Riester contracts will never pay an annuity at all.** One ordering question the statute does not
settle, and the composite settled it the wrong way: is the test applied to the annuity the **whole**
conversion capital would buy, or to the annuity payable after an elected *Teilkapitalauszahlung*? The
composite tests the **annuity actually payable**. The GDV model wording forbids precisely that —
"**Eine Abfindung erfolgt nicht, wenn die Leistung nur aufgrund einer Teilkapitalauszahlung gemäß
Absatz 4 auf eine Kleinbetragsrente sinkt.**" [S2] § 1 Abs. 3 — so the test belongs on the annuity
**before** the lump sum. **The model has not been changed**: it is a modelled rule, and changing it
moves the worked example and the golden tests. Gap 7 now records a known answer the model does not
yet implement rather than an open question.

### Death, the *Rückzahlungsbetrag*, *Anbieterwechsel* and *Beitragsfreistellung*

Before *Rentenbeginn* the death benefit is the accumulated capital; the distinctive part is the
**subsidy treatment, not the benefit design** [R14]. Transfer to a **surviving spouse's own
certified contract** is *förderunschädlich*; payment to any other heir is *schädlich*, and the
*Rückzahlungsbetrag* — all Zulagen and all § 10a relief — is deducted before payment, with the
return on the subsidised part becoming taxable `[unverified]`. After *Rentenbeginn*, continuation to
a spouse or payments for the remainder of a *Rentengarantiezeit* are *förderunschädlich*; a lump-sum
death benefit outside those forms is not certifiable at all [R1]. **The model publishes the death
benefit gross**, because the *Rückzahlungsbetrag* is a deduction from what the beneficiary receives
and not a change in the insurer's obligation — the provider withholds and remits it to the ZfA — so
netting it inside the liability stream would confuse a tax collection with a benefit. The same
applies to a surrender. The model publishes the **cumulative Zulagen credited** as a diagnostic,
which is the ZfA-reclaimable limb; the § 10a limb depends on the saver's marginal rate and cannot be
computed from contract data at all.

***Anbieterwechsel*** is a **statutory portability right with no Schicht-3 analogue**: terminate and
have the accumulated capital transferred directly to another certified contract, with no *schädliche
Verwendung* and no tax consequence [R1] [R14] [REG-R43]. A Riester "lapse" is therefore frequently a
**transfer out at full value** rather than a surrender — for the ceding insurer a full-value exit
with no *Stornoabzug*, and for the model a **distinct decrement** that must not be collapsed into
the lapse rate. The notice period is three months to the end of a calendar quarter or to the start of the payout
phase, and the ceding provider may charge no more than **150 Euro** — AltZertG § 1 Abs. 1 Satz 1
Nr. 10 Buchst. b and Satz 3, closing gap 8. One retrieved insurer charges nothing for a transfer
[S4]; one fund provider charges 50,00 € [S9]. ***Beitragsfreistellung*** leaves the contract in force: § 165 VVG gives the
right generally [REG-R28], and the Riester overlay is that the contract stays **certified**, the
guarantee stands on what was paid, no further Zulagen arrive and **no subsidy is repaid** [R14]. It
is a **state change, not a termination** — the guarantee accumulator freezes, the Zulage stream
stops, the account keeps rolling and the fixed charges keep biting. Against a surrender value below
contributions and a *Rückzahlungsbetrag* on the way out, that is why the German book shows
*Beitragsfreistellung* where another market would show surrender [R16].

### The two contribution pools

A single Riester contract can hold **subsidised** and **unsubsidised** contributions at once [R12].
*Geförderte Beiträge* — own contributions up to the § 10a ceiling that attracted a Zulage or a
deduction, plus the Zulagen — are taxed **in full** on the way out; *ungeförderte Beiträge* —
anything above the ceiling, or paid in a year of ineligibility — are taxed on the *Ertragsanteil*
for an annuity or under § 20 Abs. 1 Nr. 6 for a lump sum [R12] [REG-R41] [REG-R45]. The provider
must track the two pools **and their investment return** separately for the life of the contract and
apportion every benefit between them in the *Leistungsmitteilung*. **That statement is now read and
is narrower than the library made it: the *Leistungsmitteilung* is not annual.** § 22 Nr. 5 Satz 7
requires it "Bei **erstmaligem** Bezug von Leistungen, in den Fällen des § 93 Absatz 1 sowie bei
**Änderung** der im Kalenderjahr auszuzahlenden Leistung", after the end of the calendar year and
with the Satz 1 to 3 amounts stated "je gesondert" [R12]. The separate **annual** duty is a different
one — AltZertG § 7a and, in the wording, [S2] § 17 Abs. 1: contributions and Zulagen and their use,
the capital built up, the year's actual costs and the return earned. **Both
pools count for the *Beitragsgarantie***: the guarantee is on what was paid in
and no wording read here distinguishes subsidised from unsubsidised money [R1] [S2] [S4] [S6] — the natural place
for an implementer to go wrong, and a numbered pitfall.

---

## Riders and options

**In scope, modelled or parameterized.** The ***Teilkapitalauszahlung***, a single lump-sum election
capped at 30 % [R1]; the ***Kleinbetragsrenten-Abfindung***, a switch on the anchor decrement whose
trigger the model computes rather than assumes [R15]; the ***Rentengarantiezeit***, which changes
the payment obligation but not the annuity amount and is the *förderunschädliche* route for an early
death in payment [R1] [R14]; the ***Anbieterwechsel***, a full-value exit decrement distinct from
surrender [R1]; ***Beitragsfreistellung***, a per-model-point switch on the year contributions stop;
**unsubsidised over-ceiling contributions**; and a **biometric rider premium**, carried **only** for
its effect on the guarantee — the carve-out capped at 20 % of total contributions [REG-R43].

**Out of scope, and why.** The ***Berufsunfähigkeits-Zusatzversicherung*** itself: its liability is
`products/berufsunfaehigkeit/`'s and its premium is not a cash flow of this model, which carries
only the statutory carve-out that premium creates. The **survivor's annuity** rider, which needs a
second life and has its own GDV condition set [S3]. The ***Auszahlungsplan mit Restverrentung***,
the fund and bank chassis's payout topology [S9]–[S12] — worth naming because it is why a Riester
fund savings plan still ends in an insurance annuity: **the insurance industry receives the
*Restverrentung* capital of the fund industry's contracts**. ***Wohn-Riester*** in both limbs [R13]
[R19] [S13], the *Wohnförderkonto* being a notional tax memorandum carrying **no cash whatsoever**
and the certified *Darlehen* a banking liability; what the model could have represented and
deliberately does not is the *Eigenheimbetrag* **withdrawal**, an early and complete exit at full
value. And **surplus in payment**, because the constant-or-rising requirement constrains which
systems are available [R1] and no declaration level was established.

---

## Variations across insurers

**No carrier-specific parameter was established for any Riester product, at any house, for any
year** (gap 12) — stated first so that no reader takes a silence for a value. But the carrier table
is empty for a second reason too: **this product varies across carriers far less than any other in
`delib`**, because most of what a French *temporaire décès* leaves to the insurer, German statute
fixes for everyone.

### The observed range, parameter by parameter

| Parameter | Set by | Observed variation |
|---|---|---|
| Zulagen amounts; eligibility; *Mindesteigenbeitrag*; *Sockelbeitrag*; the proportional Kürzung; the § 10a ceiling and the *Günstigerprüfung* | statute [R6] [R9] [R10] [REG-R42] | **none — identical for every provider and every chassis** |
| Earliest payout age; lifelong-annuity requirement; 30 % lump-sum cap; five-year cost spreading; *Wechselrecht*; unisex; the 20 % biometric carve-out; taxation of the benefit; *schädliche Verwendung*; the *Rückzahlungsbetrag* | statute [R1] [R12] [R14] [R23] [REG-R42] [REG-R43] | **none** |
| The 100 % *Beitragsgarantie* | statute [R1] [REG-R43] | **none in level**; the *mechanism* varies by chassis |
| *Kleinbetragsrente* threshold | statute [R15] [REG-R42] | **none in level** — 1,5 % of the monthly *Bezugsgröße*, § 93 Abs. 3 Satz 2 Nr. 1 EStG. Whether commutation is mandatory, optional or the saver's right is a contract term, and both retrieved wordings make it the **provider's option** [S2] [S4] |
| Disclosure: PIB, *Effektivkosten*, CRK | statute [R4] [R5] [S14] [REG-R43] | **format none** — the insurance and fund sheets carry the same headings and the same § 2a cost list. The disclosed values do vary and **two are now established**: *Effektivkosten* 1,45 and 1,33 Prozentpunkte, CRK 4 and CRK 2, at one fund house [S9]. **No insurance value was established** |
| *Rechnungszins* | carrier, capped by [R22] [REG-R14] | the current cap is read — **1 Prozent**, DeckRV § 2 Abs. 1 — and fixed for the contract's whole term at the rate used at conclusion (Abs. 2). The 0,25 % regime of 2022–24 is not in the consolidated text and stays at [REG-R15]. **Two carrier choices are now established**: **1,25 %** on a 01.15-vintage tariff [S4] and **0,9 %** on a 01.01.2025-vintage one [S6] — the latter **below** the cap of its vintage, which is the direct evidence for the composite's footnote 13 |
| *Garantierter Rentenfaktor* | carrier | **the construction is established, the level is not.** Debeka's 2025 Riester wording defines a guaranteed factor per 10 000 € of capital on a 0,1 % *Rechnungszins* and its own unisex table, compared with the current factor, higher of the two paid [S6]. But **neither** the GDV model wording **nor** the CosmosDirekt wording has a *Rentenfaktor* at all — they agree the annuity at inception [S2] [S4]. So the design **varies by house**, which the library had not suspected, and no level is established at any house (gap 9) |
| Charges: acquisition, administration, payout-phase, *Effektivkosten*; and the charge base for the Zulagen | carrier | **one complete tariff basis now exists**: 1,0 % of the *Eigenbeiträge* acquisition, 2,1 % of each contribution and **6,0 % of each Zulage** administration, 0,13 % of the accumulated *Beitragssumme* a year, 1,5 % of the annuity in payment, nil *Stornoabzug* and nil transfer charge [S4]. Two more wordings give the **forms** without levels [S2] [S6], and a fund house gives disclosed totals [S9]. **The charge base for the Zulagen is settled — they are charged** (gap 14 closed). **Levels remain unestablished as a range**: one tariff is not a market |
| *Überschussbeteiligung* declarations and surplus system | carrier | **not established** (gap 12) |
| Guarantee **mechanism** | carrier and chassis | the taxonomy is established — general account; *statisches* and *dynamisches Hybridmodell*; i-CPPI; rule-based fund reallocation — but **no carrier's design** |
| Rider inventory (BUZ, survivor's benefit, *Rentengarantiezeit*) | carrier | **not established** (gap 11) |
| Whether the tariff is open to new business | carrier, and now statute | closed to new business from 1 January 2027, the date the amended AltZertG § 5 and EStG § 93 Abs. 3 both point at [R26] [REG-R44]; which houses had already withdrawn, and when, is **not established**. Two houses were still maintaining Riester wordings into 2025 [S2] [S6] |

### The carriers named, and what naming them does and does not assert

| Carrier or provider | Chassis | What is established |
|---|---|---|
| GDV *Musterbedingungen* [S1] [S2] [S3] | both insurance forms | **Both wordings were retrieved and read** at "Stand: 21.07.2025" — 25 pp. classic, 27 pp. unit-linked — from the association's own index, which also lists a third AltZertG set for an **immediate** annuity and separate *Hinterbliebenenrenten-Zusatzversicherung* sets [S3]. They supply the guarantee clause, the 20 % carve-out, the death benefit, the charge **forms** including the Zulagen base, the *Wechsel* notice period, the *Kleinbetragsrente* rules and a ten-year *Rentengarantiezeit* example. **Every level is a company-individual blank**, which is why the composite's carrier parameters stay [std] |
| CosmosDirekt [S4] | classic insurance | **The wording was retrieved**, edition LA 1005 A (01.15), with its specimen PIB. LA 1005 A is the **conditions document number**; the tariff is **R1-A**. It is a separate document family from the house's Schicht-3 (LA 904 A) and Basisrente (LA 1100 A) series. It supplies a *Garantiesatz* of **1,25 % p. a.**, a complete numbered charge basis, **nil** *Stornoabzug* and **nil** transfer charge, a *flexible Altersgrenze* of 62–70, and a bar on assignment and pledging |
| Debeka [S6] | classic with fund surplus | **The wording was retrieved**, edition B LV 94 (01.01.2025) — a Riester tariff drafted after the *Höchstzinssatz* rose. It supplies a *Rechnungszins* of **0,9 %** (below the 1,00 % cap of its vintage), the annuitant table **UNI 2004 R**, the **two-*Rentenfaktor* construction** with a higher-of *Günstigerprüfung* on a 0,1 % basis and the house's own unisex table, an interest-linked **market-value-adjustment *Stornoabzug*** of 0/5/10/15 %, and 60-month acquisition-cost spreading with the charge on each Zulage taken once at inflow. **No charge level**, those being tariff data outside the AVB |
| Allianz [S5]; R+V [S7]; Alte Leipziger [S8] | classic (and unit-linked at [S5] [S8]) | Why each is the right place to look: Allianz is the market-leader comparator; R+V is the one group whose Riester offering spans an insurance and a fund chassis in the **same** distribution network as [S9]; Alte Leipziger is the broker-market comparator. **No document was located for any of the three in this pass** — no tariff code, vintage, clause or new-business status (gap 12). The Allianz cost figures the library used to lean on are `[unverified]` third-party commentary and are now superseded by [S4] and [S9] |
| Union Investment [S9], DWS [S10], Deka [S11] | Riester-Fondssparplan | **Three *Muster*-PIBs were retrieved, two of them with values.** Union Investment: *Zertifizierungsnummern* **006403** and **006407**, CRK **4** and **2**, *Effektivkosten* **1,45** and **1,33 Prozentpunkte**, a full § 2a cost list and a 50,00 € transfer charge; the guarantee is met by a *Depotsteuerungskonzept* over a **Sicherungs-** and a **Chancenkomponente**, not specifically an equity and a bond fund. DWS: structure only, values blank, but an explicit payout window of the 62nd to the **83rd** birthday. Deka: not located. **No reallocation rule, fund name or new-business status** (gaps 11, 12), and the **cash-lock** characterisation is in no retrieved document and keeps its `[unverified]` tag |
| *Sparkassen*; *Volks- und Raiffeisenbanken* [S12] | Riester-Banksparplan | The structurally simplest certified product and the one for which the guarantee costs **nothing at all**, since a deposit balance cannot fall below its deposits — the analytical control case, isolating the guarantee's cost as **return forgone** rather than as a capital charge. **No product, rate or bonus scale** |
| Twenty-plus further life offices [S16] | classic and unit-linked | Named so a follow-up research pass has a list. **No wording was located for any house in that list**, and no parameter anywhere in this library may cite [S16] for a **level** |

---

## Regulatory context

**Two statutes doing different jobs.** The **AltZertG** says what a contract must contain to be
certifiable; the **EStG** says who gets what subsidy and how the benefit is taxed — a *product* rule
in the first, a *money* rule in the second, and confusing them is the commonest error in secondary
writing about this product. § 1 AltZertG fixes the payout age, the *Beitragserhaltungszusage*, the
payout shape, the 30 % lump-sum cap, the five-year cost spreading, the *Wechselrecht* with its
**150 €** charge ceiling and the unisex rule [R1] [REG-R43]; **§ 2a closes the list of charges a
certified contract may levy at all** [R2]; §§ 3, 3a and 5 make certification an administrative act of
the **BZSt** on the **contract type**, with the CRK simulation delegable to the PIA [R2] [S15]
[REG-R43]; § 1 Abs. 1a extends it to a **loan** [R3]; §§ 7 to 7c carry the information duties [R4];
and the **AltvPIBV** carries the sheet's form, its model case, its return scenarios and the
*Effektivkosten* [R5] [S14]. Non-assignability is **not** in the AltZertG — it is EStG § 97 [R16]. The subsidy machinery is EStG Abschnitt XI — § 79 (entitlement)
[R7], §§ 82–83 (contributions and the Zulage) [R8], §§ 84–85 (the amounts) [R9], §§ 86–87 (the
*Mindesteigenbeitrag*) [R10], §§ 89–91 (the ZfA) [R11], §§ 92a–92b (Wohn-Riester) [R13], §§ 93–95
(*schädliche Verwendung*) [R14], § 97 (non-transferability) [R16] — with § 10a carrying the
deduction [R6] and § 22 Nr. 5 the taxation of the benefit [R12], all consolidated for practitioners
in the BMF *Anwendungsschreiben* [R24], **whose date, reference number and content are still not
established** (gap 3). **Gap 4 is closed.** Every paragraph number in that list, and every one in
this document, was checked against the canonical statutory XML on 2026-08-30 and is cited with the
instrument's *Stand*; the `[unverified]` tags that stood on them are gone, and where a number turned
out to be wrong — the 60th-year rule is § 14 Abs. 2 and not § 1, the *Pfändungsschutz* is ZPO § 851
and not EStG § 97, the *Effektivkosten* are AltvPIBV § 8 and not the AltZertG — the citation was
corrected rather than dropped.

**The statutes that shaped the product.** The *Altersvermögensgesetz* and
*Altersvermögensergänzungsgesetz* of 2001 created it for contribution years from 2002, in the same
breath as they **reduced the future replacement rate of the statutory pension** — the pairing is the
whole political logic of the product [R17]. The *Alterseinkünftegesetz* of 2004 created the
three-layer taxonomy [R18] [REG-R38]; the *Eigenheimrentengesetz* of 2008 created Wohn-Riester and
raised the *Kinderzulage* for children born from 2008 [R19]; the
*Altersvorsorge-Verbesserungsgesetz* of 2013 introduced the standardised PIB, capped the *Wechsel*
charge and closed the zero-contribution entitlement of a *mittelbar* eligible spouse [R20]; and the
*Betriebsrentenstärkungsgesetz* of 2017 raised the *Grundzulage* to 175 €, brought the
*Kleinbetragsrenten-Abfindung* under the *Fünftelregelung*, introduced a *Freibetrag* in the
*Grundsicherung im Alter* and removed the double *Krankenversicherung* charge on a bAV-sourced
Riester annuity [R21]. **Every one was a repair to a criticism rather than an extension, and none
changed the *Beitragsgarantie*** — what the 2023 *Fokusgruppe* said had to change [R26], and what
the 2026 reform did by replacing the product [REG-R44].

**Prudential, reserving and tax are cited, never specified.** The *Höchstzinssatz* of § 2 DeckRV —
"auf **1 Prozent** festgesetzt", and fixed for the whole term at the rate used when the contract was
concluded — binds the rate at which the *Deckungsrückstellung* is computed and nothing else [R22]
[REG-R14] [REG-R15]; § 4 Abs. 1 DeckRV caps *Zillmerung* at "**25 Promille** der Summe aller
Prämien" [REG-R16]; § 5 Abs. 3 DeckRV
drives the *Zinszusatzreserve* [REG-R17]; the MindZV floors the transfer to the *Rückstellung für
Beitragsrückerstattung* [REG-R18] [REG-R19]; § 153 VVG gives the individual entitlement to the
*Überschussbeteiligung* and the *hälftige* participation in the *Bewertungsreserven* [REG-R24]; and
above them sit the *Deckungsrückstellung* [REG-R54] and Solvabilität II as transposed by the VAG
[REG-R5] [REG-R6]. On the tax side the benefit is *sonstige Einkünfte* taxed in full under § 22
Nr. 5 to the extent it derives from subsidised contributions [R12], with a
*Werbungskosten-Pauschbetrag* of **102 €** `[unverified]`; a **private** Riester annuity is **not** a
*Versorgungsbezug* and attracts no health or long-term-care contribution for a compulsorily insured
pensioner, while a *freiwillig versichertes* member is assessed on their whole economic capacity,
private annuities expressly included [REG-R46]. **None of it is computed here**: this library
publishes gross, undiscounted, best-estimate-style liability cash flows and stops short of the
discounting, so every discount rate, asset return and declared rate in these documents is **[std]**.

**Conduct, disclosure and the reform track.** The individual *Produktinformationsblatt* with its
individually computed *Effektivkosten* is a **stronger** duty than the product-level VVG-InfoV figure
[R4] [R5] [S14] [REG-R31] [REG-R43]; alongside sit the IDD as transposed [REG-R33], PRIIPs for the
unit-linked chassis [REG-R32], BaFin's *Wohlverhaltensaufsicht* and its expectation of *angemessener
Kundennutzen* [REG-R35], and the BGH line of authority — including its 2025 judgment striking down
asymmetric unilateral reduction of a *Rentenfaktor* [REG-R36], which bears directly on the
two-factor conversion adopted above. The *Fokusgruppe private Altersvorsorge* reported in 2023
recommending that the 100 % *Beitragsgarantie* be relaxed or removed, a securities-account product
admitted, the Zulage simplified into a proportional match and eligibility widened [R26]
`[unverified]` on every element, neither the report nor the 2024 draft bill having been retrieved.
The **enacted** reform, however, is now readable in the statutes it amended: an act of **26 May
2026**, **BGBl. I 2026 Nr. 156**, rewrote AltZertG §§ 1 and 5 and VVG provisions with effect from
**1 January 2027**, and the amended § 5 certifies against § 1 paragraphs 1b, 1c and 1d that the
consolidated text does not yet carry [R26]. So this specification does describe a **legacy** product,
and the promulgation date and BGBl citation it previously said could not be asserted **can** now be —
but the act's **title** was not read and may not be given, and nothing may be asserted about the
content of the new contract forms.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-riester_rente-r1
[R10]: #delib-riester_rente-r10
[R11]: #delib-riester_rente-r11
[R12]: #delib-riester_rente-r12
[R13]: #delib-riester_rente-r13
[R14]: #delib-riester_rente-r14
[R15]: #delib-riester_rente-r15
[R16]: #delib-riester_rente-r16
[R17]: #delib-riester_rente-r17
[R18]: #delib-riester_rente-r18
[R19]: #delib-riester_rente-r19
[R2]: #delib-riester_rente-r2
[R20]: #delib-riester_rente-r20
[R21]: #delib-riester_rente-r21
[R22]: #delib-riester_rente-r22
[R23]: #delib-riester_rente-r23
[R24]: #delib-riester_rente-r24
[R25]: #delib-riester_rente-r25
[R26]: #delib-riester_rente-r26
[R3]: #delib-riester_rente-r3
[R4]: #delib-riester_rente-r4
[R5]: #delib-riester_rente-r5
[R6]: #delib-riester_rente-r6
[R7]: #delib-riester_rente-r7
[R8]: #delib-riester_rente-r8
[R9]: #delib-riester_rente-r9
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R22]: #delib-reg-r22
[REG-R24]: #delib-reg-r24
[REG-R28]: #delib-reg-r28
[REG-R29]: #delib-reg-r29
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R38]: #delib-reg-r38
[REG-R40]: #delib-reg-r40
[REG-R41]: #delib-reg-r41
[REG-R42]: #delib-reg-r42
[REG-R43]: #delib-reg-r43
[REG-R44]: #delib-reg-r44
[REG-R45]: #delib-reg-r45
[REG-R46]: #delib-reg-r46
[REG-R47]: #delib-reg-r47
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R54]: #delib-reg-r54
[REG-R6]: #delib-reg-r6
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
