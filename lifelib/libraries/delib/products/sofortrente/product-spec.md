# Product Specification

**Status:** Drafted 2026-08-29 with no document retrieved; **re-verified against the primary
documents on 2026-08-30**, when 19 of this product's 32 source entries were opened and read.

**Scope note.** A *representative composite specification* assembled for reference liability
cash-flow modeling of a German **sofortbeginnende private Rentenversicherung** — the *Sofortrente*:
a single *Einmalbeitrag* (single premium) buys a *Leibrente* (life annuity) that begins at once and
is paid for as long as the annuitant lives. **It is not any single insurer's contract**: it is
assembled from four condition sets that do cover this product — NÜRNBERGER's tariff NR3303 [S4],
Zurich Deutscher Herold's pack [S2], CosmosDirekt's LA 904 A [S6] and the GDV's own model conditions
[S1] — and no carrier would recognise the whole of it. [S#] tags name primary product documents
(*Verbraucherinformation*, *Allgemeine Versicherungsbedingungen*, *Produktinformationsblatt*,
*Basisinformationsblatt*, *Überschussverteilung*) and [R#] product-specific regulatory and actuarial
references, both numbered per `_research/sofortrente.md` and resolved in `sources.md` (frozen, never
renumbered); [REG-R#] tags the cross-product library
`references/regulatory-and-actuarial-references.md`, whose R1–R56 numbering is separately frozen.
**[std]** marks a standardization introduced for the reference implementation, each with a numbered
footnote giving its rationale and, where one exists, the observed range; claims no retrieved
document corroborates are flagged [unverified]. German terms of art stay in German, italicised on
first use.

**Retrieval conditions, stated first because they govern every line below.** This file was
**drafted under a policy that blocked all egress**: `WebFetch` and `curl` were refused with HTTP 403
for `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`, `destatis.de`, `eur-lex.europa.eu`
and every insurer host named here, and the session's 200-call `WebSearch` budget was **exhausted
before work on this product began**, so **not one search was run for the *Sofortrente***. The first
draft therefore rested on the authoring model's own knowledge of German insurance law and practice,
disciplined by **[std]** and [unverified] tags and by facts carried over with attribution from a
sibling delib research file, principally `_research/klassische_rentenversicherung.md`, which shares
this product's *Rechnungsgrundlagen* (calculation bases), its surplus chassis and, at two carriers,
its tariff. **That policy has since been lifted and these citations re-verified against the primary
documents.** On 2026-08-30 the insurer condition sets and pre-contractual packs [S2] [S3] [S4] [S5]
[S6] [S8] [S14], one carrier group's *Überschussverteilung* [S10], the GDV's model conditions [S1]
and its survivor's-annuity rider set [S9] were retrieved as PDFs and read, and every statutory
provision this file cites under its own [R#] ids was read as canonical XML from
`gesetze-im-internet.de` with the instrument's amendment *Stand* recorded. **Of the 32 source
entries in `sources.md`, 19 now read `Retrieved: yes` and 12 read `no`**, one ([R20]) being mixed.
The twelve that failed are of four kinds, set out entry by entry there: two pre-contractual classes
of which no carrier publishes a specimen [S11] [S12], plus the *Standmitteilung* an insurer sends to
a policyholder rather than publishes [S15]; DAV material that is not on the open web at all [R8]
[R10] [R11] [R12]; one paywalled market study [R22] and two publisher series not located at any
address [R18] [R25]; and two research artefacts with no single document behind them [S13] [R23].
**A `Retrieved: yes` citation means the document was opened and the passage read; a `Retrieved: no`
citation is still a pointer, not a certificate**, and is marked as one. The re-verification changed
this specification — it withdrew claims the draft got wrong, and each correction is recorded where
it bites rather than gathered here. What it did not change is the shape of the evidence: the corpus
establishes this product's **mechanics** at clause level and its **levels** hardly at all, exactly
one carrier's guaranteed-annuity scale having been located [S8], *no charge parameter and no total
annuity including declared surplus having been established at any German carrier for any year*.
There is therefore still **no insurer-level quantitative comparison anywhere below**, the variations
section is structural rather than numeric, and every euro and percentage describing the
representative design is either **[std]** with its derivation printed, or tagged to a document that
was read, or tagged to a cross-product reference.

**Out of scope.** The **accumulation phase** of a deferred annuity is the separate delib product
`klassische_rentenversicherung`; premium accumulation, the *Deckungskapital* recursion, the
*Rückkaufswert*, *Beitragsfreistellung* and the *Kapitalwahlrecht* belong there. **Schicht 1**
(*Basisrente*) and **Schicht 2** (*Riester-Rente*, bAV) run the same payout machinery under
completely different tax rules [REG-R38]. *Fondsgebundene* and *indexgebundene* payout annuities,
*Sterbegeldversicherung*, *Pflegerentenversicherung*, *Gruppenversicherung*, private
*Krankenversicherung* and institutional pension-risk transfer are all outside this file.

---

## Product overview and market role

A *Sofortrente* is an ordinary German **life insurance contract** under the
*Versicherungsvertragsgesetz* (VVG) [REG-R22], written on the insurer's general account
(*Sicherungsvermögen*) [REG-R7], in the classic (*konventionell*) non-unit-linked form [S2] [S6].
Structurally it is one sentence long: **one payment in at inception; a stream of payments out until
death**, floored by a *Rentengarantiezeit* (guarantee period) or a *Kapitalrückgewähr* (refund of
the unconsumed capital on death) and lifted by a declared, non-guaranteed *Überschussrente* (surplus
annuity). What it sells is the transfer of *Langlebigkeitsrisiko* to an insurer. The
*Versicherungsnehmer* contracts and pays; the *versicherte Person* is the life the annuity depends
on; a *mitversicherte Person* may be named for a *Hinterbliebenenrente*; a *Bezugsberechtigter*
receives whatever falls due after death [REG-R26]. Usually the first three are one person; where
they are not, § 150 VVG requires the insured person's written consent above a threshold expressed in
ordinary funeral costs, and the designation is revocable unless made irrevocably [REG-R26].

**Schicht 3, and why the tax rule is the product.** The *Sofortrente* is a third-layer, unsubsidised
private contract in the *Drei-Schichten-Modell* [REG-R38]: nothing is deductible going in, and only
the ***Ertragsanteil*** — a fixed statutory fraction of each payment, set once by the annuitant's
age at *Rentenbeginn* and never changed — is taxable coming out [R13] [REG-R41]. **For an annuity
commencing at 65 that fraction is 18 %** [R13], the only cell of the statutory table any delib
search corroborated. The asymmetry against the subsidised layers is total: a Schicht-1
*Rentenfreibetrag* is frozen in euros for life, so every later increase — including every increase
in the *Überschussrente* — is fully taxable, whereas in Schicht 3 it is the *percentage* that is
frozen, so surplus increases are taxed at the same light rate [REG-R41]. That is the whole economic
case for the product, and the reason it is bought with money already taxed: an inheritance, a
property sale, a matured endowment, a severance payment, or a *Kapitalwahlrecht* lump sum.

**Its structural role: the pricing primitive of every other German annuity.** Two carriers' AVB
state, in their own contract terms, that the factor at which a deferred contract converts is the
tariff the insurer is then writing **for immediately beginning annuities**. NÜRNBERGER's deferred
tariff NIR3301 is explicit to the point of naming the tariff: the conversion uses "unserem dann
aktuellen Rechnungszins und unserer dann aktuellen unternehmenseigenen anerkannten Sterbetafel …
maßgeblich sind Rechnungszins und Sterbetafel in der Beitragskalkulation vergleichbarer, dann bei
uns zum Verkauf geöffneter Rentenversicherungen **mit sofort beginnender Rentenzahlung**", with
"Beispiel: Zum Zeitpunkt des Abschlusses Ihres Vertrags war in diesem Sinne der Tarif NR3303
vergleichbar" — NR3303 being the carrier's own immediate-annuity tariff [S5] [S4]. Zurich Deutscher
Herold converts accumulated surplus at *Rentenbeginn* "unter Zugrundelegung von Rechnungszins und
Sterbetafel, die zum Zeitpunkt des Übergangs in die Rentenzahlung für diese dann vorgesehen sind"
[S3]. A model of this product is therefore also the conversion engine of
`klassische_rentenversicherung`, `fondsgebundene_rentenversicherung`, `indexpolice`, `basisrente`
and `riester_rente`.

**Market size.** No figure isolates this product: the GDV series separates *Einmalbeiträge* from
*laufende Beiträge* in new business, but that line aggregates *Sofortrenten* with single-premium
endowments, bAV contributions and *Zuzahlungen* [R25]. On the cross-product aggregates, German life
premium income was **+2,8 % to 94,6 Mrd €** in 2024, of which *laufende Beiträge* were
**66,3 Mrd €**, roughly flat, while the ***Einmalbeitragsgeschäft* grew about 10 % to 28 Mrd €**;
the contract count fell 1,4 % to **80,3 Mio** [REG-R53]. Single premium is now roughly **30 %** of
German life premium income and growing an order of magnitude faster than regular premium — the
structural reason this product is live. **No number of *Sofortrente* contracts, no average
*Einmalbeitrag* and no average purchase age was established** (research gap 7).

**The 2025 interest step, which matters more here than anywhere else.** The *Höchstrechnungszins* —
the statutory maximum discount rate for the *Deckungsrückstellung*, and through § 138 Abs. 1 VAG the
effective cap on a new tariff's technical rate [REG-R8] [REG-R14] — fell for thirty years to
**0,25 %** and rose to **1,00 % on 1 January 2025**, the first increase since 1994 [REG-R15]; the
DAV recommended 1,0 % again for 2026 and 2027 [R8] [REG-R56]. For a deferred contract the rate
matters over a thirty-year accumulation; for a *Sofortrente*, **the rate at which the tariff is
struck fixes the buyer's whole income, permanently, on the day of purchase** — worth about **+10 %**
on the guaranteed annuity at 65 and **+12 %** at 60, tapering to **+6 %** at 80 on the [std]
arithmetic below. The direction falls out of the tariff formula [S6] and the statutory rate history
[REG-R15]; **the magnitude is constructed, not observed** (gap 5).

**What it is bought against.** The standard German comparator is a ***Bankauszahlplan***: the same
capital drawn down at a bank until exhausted. The plan **ends** — 100 000 € drawn at 400 € a month
at 2 % is exhausted after 26,9 years, at about age 92 **[std]** (14) — whereas the annuity does not;
the annuity is taxed on 18 % of each instalment [R13] while the plan's interest is taxable in full;
and the annuitant gives up the capital irreversibly and does badly by dying early. The honest
framing: a *Sofortrente* **is insurance against outliving one's money, priced like insurance**. One
market fact does *not* transfer here: the classic **deferred** annuity was withdrawn by Debeka in
2016 and by Allianz, Zurich and Generali before it [S7] [S8], but **no equivalent retreat from the
immediate annuity was established** — and there is a structural reason not to expect one, the
objection to the deferred contract having been a thirty-year interest guarantee where an immediate
annuity's real risk is longevity, which no design removes. An argument, not a finding (gap 14).

---

## Representative specification

**What "representative" means here.** In the sister libraries a composite is the mode of an observed
range across retrieved carriers. That method is **still unavailable** here, but for a narrower
reason than before. The corpus now holds four insurer condition sets that cover the immediate
annuity — NÜRNBERGER's AVB for tariff NR3303 [S4], Zurich Deutscher Herold's *Verbraucherinformation*
for the *sofort beginnende Rentenversicherung* [S2], CosmosDirekt's LA 904 A, whose § 1 covers the
immediate form [S6], and the GDV's own model conditions for it [S1] — so the **mechanics** below are
argued from clause text at named carriers. What no document supplies is a **comparison**: exactly one
carrier's rate scale was located [S8] and no two carriers can be put on the same case, so every level
below remains a construction. Each value is argued from one of exactly three things and
the *Basis* column says which: a mechanic the corpus establishes at clause level at a named carrier;
a statutory or professional rule from the cross-product library; or the modeller's construction,
tagged **[std]** with its arithmetic printed. Where the third applies and no observed range exists
the footnote says so in those words: a **[std]** with no range is weaker than one with a range.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-premium immediate life annuity on the general account, *konventionell*, profit-participating | [S2] [S6]; participation statutory [REG-R24] |
| Legal form | German *Lebensversicherung* under the VVG; *Neubestand* (concluded after 29 July 1994) | [REG-R22]; [REG-R11] |
| Tax layer | Schicht 3 — no *Sonderausgabenabzug*, no *Zulage*, no certification; *Ertragsanteil* on payout | [REG-R38] [REG-R41] [R13] |
| Lives basis | Single life; a second life may be added as a *Hinterbliebenenrenten-Zusatzversicherung* | [S9] |
| Premium form | **One** *Einmalbeitrag*, paid once at inception. No premium stream, no *Beitragsdynamik*, no *Ratenzahlungszuschlag* | [S2] [S6]; structural |
| Entry ages | **60 to 85** | envelope **[std]** (1); one carrier maximum read, 85 [S7] |
| *Einmalbeitrag* | Minimum **10 000 €**; working range **25 000 € – 500 000 €**; representative case **100 000 €** | envelope **[std]** (2); one carrier minimum read, 3 000 € [S7] |
| *Aufschubzeit* (deferment) | **0 years** representative; **0 to 15 years** offered | **[std]** (3) |
| Underwriting | **None.** No medical evidence, no *Gesundheitsprüfung* | **[std]** (4), [unverified] |
| Sex | Tariff **unisex** for business written from 21 December 2012; the profession's tables are sex-distinct | [REG-R34]; [REG-R49] |
| *Rechnungszins* | **1,00 %** for a 2025 or 2026 contract, at or below the *Höchstrechnungszins* of the contract's own vintage | [REG-R14] [REG-R15]; 1,00 % read in three carriers' AVB [S2] [S3] [S4] |
| Anchor model cell | 100 000 €, annuitant male aged 65 (born 1960), inception 2025, *Rechnungszins* 1,00 %, *Rentengarantiezeit* 10 years, monthly *vorschüssig*, *teildynamische Überschussrente* | **[std]** (5) |

1. **One carrier's upper limit is now established and the lower is not**: Allianz gives a
   *Höchsteintrittsalter* of **85 Jahre** for the lifelong form [S7], and [S2]'s bAV wrapper a
   *Mindestrentenalter* of 62, which is a Schicht-2 tax constraint and not a retail one. A typical
   retail window in the sixties remains [unverified]. **60 to 85** is adopted because below 60 the
   *Ertragsanteil* is high enough (22 % at 60 against 18 % at 65 [REG-R41]) to weaken the tax case the
   product exists for, and above 85 the *Rentengarantiezeit* options collapse — a 20-year guarantee at
   85 costs a quarter of the annuity. The boundaries claim to be no carrier's.
2. **One carrier's minimum is now established and it is far below the [std] envelope**: Allianz
   accepts a *Mindesteinmalbeitrag* of **3 000 €** [S7], against the five-figure minimum this
   specification assumed on the argument that fixed per-policy cost swamps a small annuity. The
   envelope is not moved in this pass — one carrier is not a market, and the model points are built
   on it — but it is now known to be conservative at the bottom. No upper limit was established at
   any carrier. **100 000 €** remains the unit German immediate annuities are quoted in — *Rente je
   100 000 € Einmalbeitrag* — while the deferred market quotes a *Rentenfaktor* per 10 000 € [R20];
   Debeka quotes per 50 000 € [S8], so the unit is not uniform either.
3. The variant exists but **no carrier's terms, minimum, maximum or deferment death benefit were
   established**, and the corpus's one candidate turned out not to be one: the Mecklenburgische
   "Rente flex" is a *Private Rentenversicherung mit flexiblem Fondsanteil (Hybrid)*, a unit-linked
   deferred annuity [S14]. Gap 17 therefore closes as a **negative finding**. The design takes
   **0** — which is what makes the contract a *Sofortrente*
   rather than a single-premium deferred annuity — and carries the deferment as a model-point column
   so it can be switched on.
4. A *Sofortrente* is normally written **without medical underwriting**, because the exposure runs
   the wrong way: medical evidence would be used by the applicant, not the insurer, so the selection
   sits in the tariff margin rather than in an individual assessment. **The tag stays**: none of the
   four retrieved condition sets for this product mentions a *Gesundheitsprüfung* either way, and
   silence is not a statement — though [S5] lists "keine Möglichkeit unsererseits zur Risikoprüfung"
   among the features that make an immediate-annuity tariff *comparable*, which is the nearest the
   corpus comes; hence still [unverified]; its converse, the impaired-life *enhanced annuity*, is **not established to exist in
   the German retail market**, and § 19 VVG's *Anzeigepflicht* [REG-R30] is inert where the insurer
   asks nothing.
5. Age 65 is where the corroborated *Ertragsanteil* applies [R13] and where the [std] annuity table
   is anchored; the 10-year guarantee sits at the short end of the market's typical band (15 years to
   age 70, 10 thereafter, most choosing 10 to 20 [R23]) so the certain window fits a readable
   worked-example table; and the 2025 inception puts the cell on the current 1,00 % rate [REG-R15].

### Premiums — the *Einmalbeitrag*

| Parameter | Representative value | Basis |
|---|---|---|
| Premium structure | One *Einmalbeitrag* at inception; **one inflow, at `t = 0`** | [S2] [S6]; structural |
| *Nettoeinmalbeitrag* | `Einmalbeitrag × (1 − α)`. NÜRNBERGER's charge clause states the shape exactly: "Bei Verträgen gegen Einmalbeitrag werden von uns die Abschluss- und Vertriebskosten vollständig zu Vertragsbeginn mit diesem verrechnet. Die übrigen Kosten werden von uns über die gesamte Vertragslaufzeit verteilt" [S4] — α once at inception, β running | [S4]; α **[std]** (6) |
| Acquisition loading α | **2,5 %** of the *Einmalbeitrag*, taken once | **[std]** (6) |
| Annuity administration loading β | **2,0 %** of each annuity payment | **[std]** (6) |
| *Zillmerung* | **Does not apply.** § 4 DeckRV caps the *Zillmersatz* at 25 ‰ of the *Beitragssumme*; there is no premium stream to amortise against | [REG-R16]; structural |
| Further premiums | **None.** No *Zuzahlung* in the representative design | **[std]** (7) |
| Cancellation | *Widerrufsrecht* of 30 days for life insurance, against 14 days generally | [REG-R23] |

6. **No charge *level* was established at any carrier** — not the *Abschluss- und
   Vertriebskosten*, not the administration loading, not an *Effektivkosten* figure [REG-R31], not a
   *Renditeminderung* [REG-R32] (gap 8). The **structure**, by contrast, is now read: NÜRNBERGER
   charges the acquisition and distribution costs "vollständig zu Vertragsbeginn" against the single
   premium and spreads "die übrigen Kosten … über die gesamte Vertragslaufzeit", pointing the reader
   to the § 2 VVG-InfoV *Kostenausweis* for the amounts [S4]; Zurich states the same shape as
   "bereits pauschal bei der Tarifkalkulation berücksichtigt und werden daher nicht gesondert in
   Rechnung gestellt" [S2]. That is exactly α-once-plus-β-running, so the model's charge *shape* is
   sourced and only its two numbers are **[std]**. The product has exactly three charge points, fewer than any
   other delib product: an acquisition charge on the *Einmalbeitrag*, taken once; a running loading
   on each annuity payment, covering the payment run, the annual *Standmitteilung* [REG-R25] and
   proof of life — both of the latter chargeable to the insurer by the AVB, "auf unsere Kosten"
   [S2] [S4]; and an implicit margin inside the *Rechnungsgrundlagen*, which on the retrieved
   evidence sits in the **mortality** basis rather than the interest one, every retrieved tariff
   pricing at its vintage's cap [S2] [S4] [S6] [REG-R14]. α = 2,5 % is argued from a
   single-premium annuity's cost base — a one-off commission plus issue expense, materially below the
   *Zillmerung* of a recurring-premium contract; β = 2,0 % from a per-policy running cost roughly
   constant in euros, which is why 2 % is of the right order on a 100 000 € case and too small on a
   25 000 € one, itself the reason minimum *Einmalbeiträge* exist. **Both are the modeller's view with
   no observed range, because nothing was observed.** The only market benchmark is an insurer-level
   *Verwaltungskostenquote* of 2,4 % or 2,19 % depending on measurement, spread from under 2 % to over
   4 % [REG-R53] — a ratio on premium income, not a product charge.
7. Whether carriers permit a *Zuzahlung* after inception **was not established**; economically a
   top-up is a second annuity purchase at the then-current tariff, and a second model point.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Main benefit | A *Leibrente*: a level **guaranteed** monthly annuity for as long as the annuitant lives | [S6] [S7] [R23] |
| Determination | `R = Einmalbeitrag × (1 − α) / (12 × a12(x, i) × (1 + β))`, `a12` the monthly annuity-due factor at attained age x and *Rechnungszins* i on the **first-order** DAV 2004 R basis for the annuitant's birth cohort | [S6] [R10]; α, β **[std]** (6) |
| Guarantee | The *garantierte Rente* is guaranteed **for life** and is not adjustable; § 163 VVG is the only channel and it is narrow | [S6]; [REG-R27] [R4] |
| Payment frequency | **Monthly** standard; quarterly, half-yearly and annual exist and are read at four sources | [S1] [S2] [S6] [S7] |
| Payment timing | ***Vorschüssig*** — in advance; first instalment at inception. **The retrieved AVB say the market pays in arrears**; the model's convention is not changed in this pass | **[std]** (8) |
| *Überschussrente* | Declared annually out of surplus actually earned; **not guaranteed and reducible** | [R19] [R20] [R21] [R23]; levels **[std]** |
| *Überschussverwendung* | **Three forms in the consumer literature** — *konstant* (also *flexibel*), *teildynamisch*, *volldynamisch* — elected at *Rentenbeginn*, here at inception, **irrevocably**: "Ein Wechsel der Überschussverwendungsarten ist ausgeschlossen" [S4]. *Bonusrente* is a carrier's name for the crediting mechanic, not a fourth category | [R19] [R21]; forms and irrevocability [S2] [S4] [S6] [S10] |
| *Bewertungsreserven* | Participation **continues during the annuity payment period**, currently *hälftig* under § 153 Abs. 3 VVG — read at three carriers | [S2] [S3] [S10]; [REG-R24] |
| *Rentengarantiezeit* | **10 years** representative; 5 / 10 / 15 / 20 / 25 / 30+ offered, or none | [R23] [S5] [S7]; choice **[std]** (5) |
| Death inside it | The annuity **continues to the beneficiaries** until the agreed number of years has expired | [R23] |
| Death after it | **Nothing is payable** unless a *Kapitalrückgewähr* or *Hinterbliebenenrente* was bought | [R23]; structural |
| *Kapital-/Beitragsrückgewähr* | Optional: the *Einmalbeitrag* **less the instalments already paid**, floored at zero — and two AVB confirm the deduction is measured on the **guaranteed** annuity: "bereits gezahlter Renten (bereits gezahlte Renten werden nur in der Höhe der zu Vertragsbeginn garantierten Renten abgezogen)" [S2], "abzgl. der bis zum Todeszeitpunkt gezahlten garantierten Renten" [S6] | [S2] [S6] [R23] (9) |
| *Hinterbliebenenrente* | Optional rider: 60 % or 100 % to a named second life, for that life's remaining lifetime, beginning only **after** any *Rentengarantiezeit* has run out | [S1] [S9]; percentages [unverified] — the model conditions state none |
| Capital option | **None** after *Rentenbeginn*; the annuity may not be commuted at the policyholder's election. "Eine sofort beginnende Rentenversicherung können Sie nicht kündigen" [S4] | [S1] [S2] [S4]; [R1] [REG-R28] |
| Settlement on death | To the *Bezugsberechtigter*, not automatically to the estate | [REG-R26] |

8. **The payment timing is now established, and it contradicts this specification's convention.**
   Two carriers' AVB put the first instalment one payment period *after* inception: NÜRNBERGER, "Die
   erste Rente wird einen Monat nach dem vereinbarten Versicherungsbeginn gezahlt. Die garantierte
   monatliche Rente wird an jedem Monatsersten gezahlt" [S4]; and CosmosDirekt, for which "bei
   Leibrentenversicherungen mit sofort beginnender Rentenzahlung gegen Einmalbeitrag wird die erste
   Rente je nach vereinbarter Rentenzahlungsweise ein Jahr, ein halbes Jahr, ein viertel Jahr oder
   einen Monat nach dem vereinbarten Versicherungsbeginn gezahlt" [S6]. The GDV template pays "an den
   vereinbarten Fälligkeitstagen" and does not settle it [S1]. **The German market convention for a
   *Sofortrente* is therefore payment in arrears, not in advance.** The effect is first-order:
   advance against arrears moves the annuity value by roughly half a month's interest *and* shifts
   every payout cash flow by one period. On the [std] basis at 1,00 %, `a12_due − a12_arrears = 1`,
   so the annuity per 100 000 € at 65 is `100 000 / (12 × 19.426) = 428,99 €` in arrears against
   **407,98 €** in advance — **5,1 %** from a single convention. *Vorschüssig* is nevertheless
   **retained as the [std] convention in this pass**: every arithmetic in the research file, the
   worked example and its golden tests are built on an annuity-due, and moving them is a deliberate
   decision rather than a documentation fix. It is now a convention **known to be the minority one**,
   which is a stronger statement than the gap it replaces (gap 11 closes as a contradiction).
9. **The refund is measured against the *guaranteed* annuity, and two AVB now say so**: "bereits
   gezahlte Renten werden nur in der Höhe der zu Vertragsbeginn garantierten Renten abgezogen" [S2]
   and "abzgl. der bis zum Todeszeitpunkt gezahlten garantierten Renten" [S6]. What the design had
   adopted as an argument — that a guaranteed benefit cannot be defined by reference to a
   discretionary quantity — is the market's rule, and the **[std]** tag on the basis of the netting
   comes off. Both AVB also confirm the floor at zero: once cumulative guaranteed instalments reach
   the *Einmalbeitrag*, "so erlischt der Anspruch" [S2] (gap 10 closes on this point; whether
   carriers permit the refund *combined* with a guarantee period is still not established).

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Medical evidence | **None** | **[std]** (4), [unverified] |
| Rating factors | Attained age at *Rentenbeginn*; birth cohort; the elected options; the *Einmalbeitrag*. **Sex may not be a rating factor** for business written from 21 December 2012 | [S6]; unisex [REG-R34] |
| Mortality basis | **DAV 2004 R at two carriers, a company table at a third.** Zurich Deutscher Herold: "Die Kalkulation … basiert auf der Sterbetafel DAV 2004R (Aggregattafel); es wird ein Rechnungszins in Höhe von 1,00 % verwendet" [S2] [S3]. NÜRNBERGER prices the same product on "die anerkannte Rententafel NÜRNBERGER Tafel 2013 R mit einem garantierten Rechnungszins von 1 % p. a." [S4]. DAV 2004 R is the **profession's reference**, not a mandate [REG-R47] | [S2] [S3] [S4] [R10] [REG-R49] |
| Table type | A ***Generationentafel*** — a two-dimensional basis `q(x, τ)` in attained age and calendar year, **not** a period table; the improvement is **inside** the table | [R10] [REG-R49] |
| First against second order | First-order probabilities carry safety margins relative to the second-order ("realistic") ones. For an annuity, prudent means **lighter** mortality **and a stronger improvement trend** — safety in two dimensions | [R10] [REG-R47] |
| Interest basis | The insurer's own choice **at or below** the cap, § 2 DeckRV setting a maximum and not a rate [REG-R14]. **Every retrieved tariff prices at the cap of its own vintage**: 1,00 % in three 2025/2026 AVB [S2] [S3] [S4], 0,90 % in a 01/2017 one [S6], each equal to the *Höchstrechnungszins* then in force [REG-R15]. No below-cap pricing was observed | [S2] [S4] [S6] [REG-R14] [REG-R15] |
| Anti-selection | Real, and not underwritten away — [S5] lists "keine Möglichkeit unsererseits zur Risikoprüfung" as a defining feature of an immediate-annuity tariff; the table is understood to carry ***Selektionsfaktoren*** for exactly that | [S5]; [REG-R49]; the *Selektionsfaktoren* [unverified] |
| *Altersverschiebung* | DAV 2004 R carries an age-adjustment component; **its convention was not established** | [R10]; gap 12 |

**What delib ships instead of the table.** DAV 2004 R and DAV 2004 R-Bestand are the property of the
Deutsche Aktuarvereinigung, distributed to members rather than published, and **not
redistributable**; `delib` ships **no version of either** and quotes no `q_x`, no improvement rate
and no annuity factor from them [REG-R47] [REG-R49]. The decrement CSV shipped with `Sofort_DE_S` is
a **[std] proxy**, anchored so the worked example reproduces exactly, and **a replacement must
preserve three things**: the **generational** structure — a `q(x, cohort)` surface, because a
period-table proxy applied to a forty-year annuity understates the liability by a margin that dwarfs
every other assumption in the model [REG-R49]; the **first-order margin in both dimensions**, level
and trend [REG-R47]; and the *Altersverschiebung* convention [R10]. Destatis's
*Generationensterbetafeln* are the free public analogue and the intended base [REG-R52]. Of the
*Bestand* variant, the table for the in-force annuity book, **nothing beyond the pairing with the
new-business table was established** [R11] (gap 12) — though it matters here, a
*Sofortrente* being priced once on the new-business table and then spending thirty years in the
*Bestand*.

**The unisex tension bites harder here than on any other delib product.** German annuity tables are
built sex-distinctly while a tariff sold since 21 December 2012 must be unisex [REG-R34] [REG-R49],
and a *Sofortrente* is the purest longevity bet in the market, so a unisex tariff must be struck on
an **assumed portfolio sex mix no insurer publishes**. The realised mix drives the *Risikoergebnis*
the MindZV then shares [REG-R18], and the reference implementation's decrement table is a **unisex
[std] proxy** with a stated mix assumption, described as one (gap 13).

### Charges

| Parameter | Representative value | Basis |
|---|---|---|
| *Abschluss- und Vertriebskosten* α | **2,5 %** of the *Einmalbeitrag*, once | **[std]** (6) |
| Annuity administration loading β | **2,0 %** of each annuity payment | **[std]** (6) |
| *Stornoabzug* | **None, ever.** § 169 Abs. 5 VVG permits a deduction only where agreed, quantified and appropriate — and there is no surrender to deduct from | [REG-R28]; structural |
| *Effektivkosten* (VVG-InfoV) | **Not established** for this product at any carrier | [REG-R31]; gap 8 |
| *Renditeminderung* (PRIIPs) | **Not established**, and whether a payout-only *Sofortrente* is within PRIIPs scope is itself unresolved | [S12] [REG-R32]; gap 8 |
| Effect of both [std] charges | On the [std] gross annuity of 407,98 € at 65 and 1,00 %: `407,98 × 0,975 / 1,02 = 389,99 €` per month per 100 000 €; a 10-year guarantee takes it to about **381 €** | **[std]** (10) |

10. A **constructed illustration**, not a market rate: printing the construction is the only honest
    alternative to printing a fabricated quotation, and **no German carrier's quotation, at any age,
    for any year, appears anywhere in this specification** (gap 5). BaFin's *Merkblatt 01/2023 (VA)*
    on *Wohlverhaltensaufsicht* — which polices *Effektivkosten* against a sector comparison and
    requires a return target for the target market [REG-R35] — **is addressed to *kapitalbildende*
    products**, and whether the supervisor scrutinises *Rentenhöhe* or surplus declarations on a
    payout annuity **was not established** [R18].

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender (*Rückkauf*) | **None once the *Rentenbezug* has begun.** For a *Sofortrente*, whose *Rentenbeginn* is at or within weeks of inception, **the contract is irrevocable from the outset**, and three condition sets say so in terms | [S1] [S2] [S4]; [R1] [R2] [REG-R28] |
| *Rückkaufswert* | **None.** § 169 VVG never engages — its Abs. 1 reaches only a contract on which the insurer's obligation is certain to arise — so there is no surrender-value table, no *Stornoabzug* and no five-year cost-spreading rule to implement | [R2] [REG-R28] |
| Lapse | **None.** A policyholder cannot lapse a contract they cannot terminate and on which no premium is due | [R1]; structural |
| *Beitragsfreistellung* | **None.** § 165 VVG has no application: there is no premium to stop | [R5] [REG-R28] |
| Termination of the contract | On the annuitant's death, subject to any *Rentengarantiezeit* still running, any *Kapitalrückgewähr* then due and any *Hinterbliebenenrente* then beginning | [R23]; structural |
| Insolvency of the insurer | Contracts transfer to **Protektor Lebensversicherungs-AG**, the statutory *Sicherungsfonds* | [REG-R12] |
| *Aufschubzeit* qualification | A deferment gives a pre-*Rentenbeginn* window in which the bar does not yet bite, so a surrender right **may** exist. **No carrier's terms established**; the base run switches the variant off | [R1] [R2]; gap 17 |

**The discrepancy between two delib documents is now resolved, against the research file.** The
research file stated that **§ 168 Abs. 3 VVG** confines the right of termination in a
*Rentenversicherung ohne Kapitalwahlrecht* to the period before the annuity payments start [R1],
flagging the paragraph number as [unverified] (gap 9); the cross-product library reported
**§ 168 Abs. 3** instead as the carve-out excluding Abs. 1 and 2 for a *Basisrentenvertrag* certified
under § 5a AltZertG and where realisation was irrevocably excluded [REG-R28]. **The section has now
been read**, in the canonical XML at Stand zuletzt geändert durch Art. 12 G v. 26.5.2026: [REG-R28]
is right and the research file is wrong. Abs. 3 disapplies Abs. 1 and 2 only for those two pension
cases, and says nothing about *Kapitalwahlrecht* or about the start of payments. The route to the
same conclusion runs through Abs. 1 and 2 themselves. Abs. 1 gives a termination right only where
"laufende Prämien zu zahlen" sind — a *Sofortrente* has none — and Abs. 2 extends it to a single
premium only "bei einer Versicherung, die Versicherungsschutz für ein Risiko bietet, bei dem der
Eintritt der Verpflichtung des Versicherers **gewiss** ist", which a pure *Leibrente* is not. § 169
falls away for the same reason, its Abs. 1 using the identical gateway phrase, so the *Rückkaufswert*
duty is **inapplicable rather than displaced**. The AVB implement exactly this: "Eine sofort
beginnende Rentenversicherung können Sie nicht kündigen. … Die Rückzahlung des Einmalbeitrags können
Sie nicht verlangen" [S4]; "Zu Lebzeiten der versicherten bzw. mitversicherten Person ist eine
Kündigung der Versicherung ausgeschlossen" [S2]; and in the GDV's own template, "Sie können Ihren
Vertrag nicht kündigen. Die Rückzahlung des Einmalbeitrages können Sie nicht verlangen" [S1]. The
**substance** is what it always was: **once the *Rentenbezug* has begun there is no termination right
and no *Rückkaufswert*.** A surrenderable life annuity would be surrendered by exactly those annuitants
expecting to die soon, leaving the insurer with the long-lived; the bar is what makes the mortality
pooling possible. Consequently `Sofort_DE_S` publishes **no surrender-value cells, no lapse
decrement, no paid-up state and no *Stornoabzug***; the only decrement is **death**, and the
behavioural assumption set every other delib product needs is **empty** — a **specification, not a
simplification**.

---

## Contractual mechanics

### The *Einmalbeitrag* and the *Nettoeinmalbeitrag*

**The rule.** The insurer deducts the acquisition and distribution loading and annuitises the
remainder: `Nettoeinmalbeitrag = Einmalbeitrag × (1 − α)` — "Bei Verträgen gegen Einmalbeitrag werden
von uns die Abschluss- und Vertriebskosten vollständig zu Vertragsbeginn mit diesem verrechnet"
[S4]. **What it does:** it fixes, once and
for all, the capital the annuity is struck against — no later accumulation, no *Beitragsdynamik*, no
second netting, so everything downstream is a division of this one number by an annuity factor. It
is also the whole of the product's new-business strain, the acquisition cost falling at `t = 0`
against a single inflow, so the first period carries a large positive `net_cf` and every later
period a negative one.

### *Rentenhöhe* — how the guaranteed annuity is struck

**The rule.** `R_garantiert = Einmalbeitrag × (1 − α) / (12 × a12(x, i) × (1 + β))`, with `a12(x, i)`
the monthly annuity-due factor at attained age `x` and *Rechnungszins* `i` on the **first-order**
annuitant basis for the annuitant's birth cohort [S2] [R10]. **It settles three things.** The
**mortality basis is a first-order annuitant table, DAV 2004 R at some carriers and a company table
at others**: Zurich Deutscher Herold prices this product on "die Sterbetafel DAV 2004R
(Aggregattafel)" [S2] [S3], NÜRNBERGER on "die anerkannte Rententafel NÜRNBERGER Tafel 2013 R" [S4].
No statute names a table [REG-R56], so DAV 2004 R is the profession's benchmark and not a mandate
[REG-R47] [REG-R49]. The **interest basis is the insurer's choice at or below the cap**, § 2 DeckRV
setting a maximum [REG-R14] — but **every retrieved tariff prices at the cap of its own vintage**:
1,00 % in the three 2025/2026 AVB [S2] [S3] [S4], 0,90 % in a 01/2017 one [S6], each equal to the
*Höchstrechnungszins* then in force [REG-R15]. The library previously reported a carrier pricing a
guaranteed factor at 0 %; that claim came from a search summary and **is not in the document**, and
it has been withdrawn. The first-order margin therefore sits, on the retrieved evidence, in the
**mortality** basis rather than the interest one. And the factor is **fixed at inception**, here once
and never revisited, inception and *Rentenbeginn* being the same date.

**The [std] annuity table, and the one market quotation now available to check it against.**
Debeka publishes a *Berechnungsbeispiel* for its own *Sofortrente* on tariff **S1**, Stand
01.01.2025: on a single premium of **50 000 €** with a **20-year *Rentengarantiezeit***, the
guaranteed monthly annuity is 133 € at 60, **151 € at 65** and 159 € at 67 [S8] — that is **302 € per
100 000 € at 65**, a *Rentenfaktor* of 30,2 per 10 000 €. The [std] construction below, on the same
age, rate and guarantee period and net of both [std] charges, gives **349 €** — about **16 % higher
than the one real quotation in the corpus**. The gap is the honest measure of what a constructed
table is worth: it is consistent with the [std] Gompertz–Makeham proxy being lighter than a real
first-order German annuitant basis, with α and β being too small, or with both, and nothing in the
corpus separates the three. **The model is not recalibrated to it in this pass** — doing so would
move the worked example and its golden tests — and the [std] table below is unchanged; the
divergence is recorded here and in `technical-notes.md` so that no reader mistakes the constructed
figures for market rates. Market-average *Rentenfaktoren* for the deferred market, on the same
per-10 000 € unit, were **29,09 €** in 2021 and **25,97 €** in 2022 at the 0,25 % cap [R20], which
brackets the Debeka figure in the right place once the rate step to 1,00 % is allowed for.

No annuity level was established at any carrier for any year when the specification was written, so
the research file **constructs** one on a stated Gompertz–Makeham proxy `mu(x) = A + B·c^x` with
**A = 0,0002**, **B = 1,5 × 10⁻⁵**, **c = 1,10** — life expectancy 24,29 years at 65, `q(65) =
0,00789`, `q(75) = 0,02001`, `q(85) = 0,05078` — a **prudent annuitant** shape of the right order for
a first-order German basis, and **not** DAV 2004 R [R10]. Monthly-in-advance via
`a12 = a_due − 11/24`; charges excluded. Gross annuity per 100 000 €, monthly in advance
**[std]** (11):

| Age at *Rentenbeginn* | 60 | 65 | 70 | 75 | 80 |
|---|---|---|---|---|---|
| i = 0,25 % | 314.43 | 369.64 | 443.58 | 544.89 | 687.02 |
| i = 1,00 % | 352.08 | 407.98 | 482.84 | 585.32 | 728.86 |
| i = 1,75 % | 391.63 | 447.93 | 523.40 | 626.75 | 771.44 |
| `a12` at 1,00 % | 23.669 | 20.426 | 17.259 | 14.237 | 11.433 |
| uplift 0,25 % → 1,00 % | +12.0 % | +10.4 % | +8.9 % | +7.4 % | +6.1 % |

Any cell checks as `100 000 / (12 × a12)`.

11. **[std]**, reproducible from the printed parameters, and **not any carrier's quotation** — and
    now measurably above the one carrier quotation the corpus holds, by about 16 % at 65 [S8]. One of
    the two forces the specification originally named has been withdrawn: no retrieved carrier prices
    below the cap, every one pricing at its vintage's *Höchstrechnungszins* [S2] [S4] [S6], so the
    difference from a real tariff must run through the **first-order mortality margin and the
    charges**. Two forces move it over time: improvement
    inside the *Trendfunktion* raises annuity values for each successive cohort, and any strengthening
    of the first-order margin does the same [R10] [REG-R49]. **Two cohorts buying ten years apart at
    the same *Rechnungszins* would not get the same annuity.**

**What is guaranteed.** The *garantierte Rente* is guaranteed **for life** and is not adjustable.
§ 163 VVG is the only channel for changing a term after conclusion and needs three cumulative
conditions — a change in the *Leistungsbedarf* that is neither temporary nor foreseeable, a new term
appropriate and necessary to secure permanent fulfilment, and an independent *Treuhänder*'s
confirmation — while excluding adjustment to the extent the benefits were insufficiently calculated
in the first place [REG-R27]; the Landgericht Köln held the low-interest phase **not** a sufficient
ground, being entrepreneurial risk (case reference not established) [R4]. A delib model treats the
*garantierte Rente* as **immutable** and records § 163 as a model risk.

### *Rentengarantiezeit*

**The rule.** A guaranteed payment period runs from *Rentenbeginn* — at NÜRNBERGER expressly "ab
Versicherungsbeginn laufenden", which for a *Sofortrente* is the same date [S4]. **If the annuitant
dies inside it, the annuity continues to be paid to the beneficiaries until the agreed number of
years has expired**: "Stirbt die versicherte Person während der Rentengarantiezeit, so wird die
monatliche Rente bis zum Ablauf der Rentengarantiezeit weiter gezahlt" [S4], and in the GDV template
"zahlen wir die vereinbarte Rente auch bei Tod der versicherten Person bis zum Ende der
Rentengarantiezeit" [S1]. Three carrier illustrations of the same arithmetic are now in the corpus —
ten years with death after three leaving seven [S1] [S4], twenty years with death after twelve
leaving eight [S8], and the portal cluster's ten years with death after six [R23]. If the annuitant
survives it, it lapses silently. **What it
does:** it converts the first `n` years from a contingent payment into a **certain** one, which is
the whole modelling consequence — during the guarantee the payment must **not** be decremented for
survival, and after it, it must be. A model applying survival probabilities across the whole stream
understates the liability; one applying none overstates it.

**Where it sits in the market.** A tariff-level design feature carried in the product name at
NÜRNBERGER, in both the deferred form — "… mit aufgeschobener Rentenzahlung **und
Rentengarantiezeit** nach Tarif NIR3301" [S5] — and the immediate one, "… mit sofort beginnender
Rentenzahlung **und Rentengarantiezeit** nach Tarif NR3303" [S4]. In the GDV template it is optional
("Wenn Sie mit uns eine Rentengarantiezeit vereinbart haben") [S1], and at Allianz it is one of the
options for which "müssen Sie eine geringere monatliche Rente akzeptieren oder extra zahlen" [S7] —
so a *Sofortrente* with **no** guarantee period is a real configuration. The claim that the period
"can be set to a minimum" was attributed to Allianz and **is not on the retrieved page**; it has been
withdrawn. Durations offered are **5, 10, 15, 20, 25 or more than 30 years**, typically **15 years for
retirement ages 61–70 and 10 years for 71 and above**, **most choosing 10 to 20** [R23]. What it
costs, on the [std] basis at 1,00 %, age 65, per 100 000 € **[std]** (12):

| *Rentengarantiezeit* | none | 5 y | 10 y | 15 y | 20 y | 25 y | 30 y |
|---|---|---|---|---|---|---|---|
| `a12` | 20.426 | 20.530 | 20.897 | 21.624 | 22.821 | 24.591 | 26.972 |
| Monthly annuity | 407.98 | 405.92 | 398.78 | 385.38 | 365.16 | 338.87 | 308.97 |
| Reduction | — | 0.51 % | 2.26 % | 5.54 % | 10.50 % | 16.94 % | 24.27 % |

12. **[std]**, same basis, `a12` replaced by an annuity-certain-due of `n` years plus an
    `n`-year-deferred life annuity. **The cost rises steeply with age, because the guarantee bites
    sooner**: a 10-year guarantee costs 2,26 % at 65, 4,10 % at 70 and 7,42 % at 75, a 20-year one
    10,50 %, 17,20 % and 26,71 % — which is why the market's typical duration falls with age [R23].
    The corpus's consumer illustration on a *deferred* contract puts the same three at roughly 0,5 %,
    2,6 % and 8,0 % [R23]: consistent in shape, different in level, **neither a tariff**.

**Two settlement forms exist and only one is modelled.** The instalments may continue as they fall
due or the *Restgarantiezeit* may be commuted, and **both AVB that address it make commutation an
election of the claimant rather than the carrier's default**: "Auf Antrag kann der Wert der bis zum
Ablauf der Rentengarantiezeit noch ausstehenden Renten … auch als einmalige Kapitalleistung
ausgezahlt werden" [S4], and "Alternativ steht dem Bezugsberechtigten die Möglichkeit offen, das für
die Rentengarantiezeit zum Todeszeitpunkt zur Verfügung stehende Deckungskapital in einer Summe
ausgezahlt zu erhalten" [S6]. The two are not the same quantity — NÜRNBERGER commutes the outstanding
instalments excluding future increases, CosmosDirekt the *Deckungskapital* — and **no take-up rate
was established**. The model pays the instalments, which is the default in both texts.

### *Kapital-* und *Beitragsrückgewähr*

**The rule.** On death the insurer refunds the *Einmalbeitrag* **less the annuity instalments already
paid**, floored at zero — so the benefit starts at the full *Einmalbeitrag* and runs to nothing over
roughly the period in which the annuitant recovers the capital nominally, on the [std] basis about
**21,5 years** at 65. **The trap inside it:** a *larger* refund means a *smaller* annuity, and a
smaller annuity means the refund runs off more slowly, so the pricing equation is **implicit in R**:

    Einmalbeitrag = 12 × R × a12(x, i) + PV( max(Einmalbeitrag − 12 × R × t, 0) payable on death at t )

It must be **solved**, not evaluated: computing the plain annuity first and then subtracting a refund
cost gets a different — and wrong — answer. On the [std] basis at 1,00 %, age 65, per 100 000 €, the
monthly annuity falls from **407,98 €** to **335,48 €**, **−17,8 %** **[std]** (13) — materially more
than a 20-year guarantee period, and the honest answer to a buyer who asks why the "money-back"
version pays so much less.

13. **[std]**, solving the equation above with deaths at mid-year and the refund discounted from
    mid-year. Market variants — ***volle Beitragsrückgewähr***, a stated percentage, a refund capped
    at a number of years' payments — exist, but **no carrier's variant was established.** The refund
    and the *Rentengarantiezeit* protect the same risk in different shapes and are usually offered as
    alternatives; **which carriers permit the combination was not established** (gap 10), so the design
    treats them as **mutually exclusive [std]** and the model asserts that exclusivity rather than
    silently permitting an unsupported configuration.

### *Hinterbliebenenrente* and its *Anwartschaft*

**The rule.** A second life — the *mitversicherte Person* — is named at inception. While the
annuitant lives, the main annuity is paid and the second life holds an ***Anwartschaft***: a
contingent, not-yet-payable entitlement. On the annuitant's death, if the second life is then alive,
the *Hinterbliebenenrente* begins at a stated percentage and is paid for that life's remaining
lifetime. **If the second life predeceases the annuitant the entitlement lapses and nothing is
refunded** — the cover has been consumed. **What it does:** it makes the contract a
**joint-life-last-survivor** annuity, the liability running
until *both* lives are dead, so the second life's age and sex matter as much as the annuitant's, and
that life is fixed at inception [unverified]. The German market treats the survivor's annuity as a
***Zusatzversicherung*** — "Die Hinterbliebenenrenten-Zusatzversicherung ergänzt die als
Hauptversicherung abgeschlossene Rentenversicherung" [S9] — and the GDV publishes model conditions
for exactly that, for the immediate annuity as well as the deferred one [S1] [S9], so in the
reference implementation it is a **separate module with its own insured life, off in the base run**.
The template settles two mechanics the specification had left open. The rider pays at the main
annuity's own *Fälligkeitstage*, "erstmals an dem Fälligkeitstag, der auf den Tod der versicherten
Person folgt"; and where a *Rentengarantiezeit* is running at the annuitant's death, "zahlen wir die
Hinterbliebenenrente **erst nach Ablauf der Rentengarantiezeit**" — the two floors run in sequence,
not in parallel, which a model combining them must respect. Typical percentages are **60 % and
100 %** [unverified]: **the model conditions state no level at all**, leaving it to the individual
contract, so the source is silent on the point rather than unread, and **no carrier's menu was
established**. On the [std] basis at 1,00 %, annuitant 65 and second life 62 on
the same mortality, per 100 000 € **[std]** (14): 60 % gives `a12` 23.838 and **349,58 €**, −14,3 %;
100 % gives `a12` 26.113 and **319,12 €**, −21,8 %.

14. **[std]**, applying the same mortality to both lives and assuming independence — real joint-life
    pricing uses sex-distinct or portfolio-mix bases and a dependence allowance. The overview's
    payout-plan exhaustion figures are on the same basis.

### Payment frequency and timing

**The rule.** The annuity is **monthly** as standard, with quarterly, half-yearly and annual
frequencies offered — read in four places: "jährlich, halbjährlich, vierteljährlich oder monatlich"
[S1] [S2], "ein Jahr, ein halbes Jahr, ein viertel Jahr oder einen Monat" [S6], and "wahlweise
monatlich, viertel-, halbjährlich oder jährlich" [S7]. The `[unverified]` tag on the non-monthly
options comes off. **On timing the corpus now speaks, and it contradicts this model's convention.**
NÜRNBERGER: "Die erste Rente wird einen Monat nach dem vereinbarten Versicherungsbeginn gezahlt. Die
garantierte monatliche Rente wird an jedem Monatsersten gezahlt" [S4]. CosmosDirekt, for the
immediate form: the first instalment falls "ein Jahr, ein halbes Jahr, ein viertel Jahr oder einen
Monat nach dem vereinbarten Versicherungsbeginn" according to the frequency chosen [S6]. **Both pay
in arrears.** The GDV template pays "an den vereinbarten Fälligkeitstagen" and does not settle it
[S1]. **What it does:** timing fixes the grid of the whole model, a monthly-in-advance stream being
an annuity-**due**, and the two conventions differ by about 5 % of the annuity (footnote 8). The
model **retains *vorschüssig*** in this pass, now labelled as a **[std]** convention known to be the
minority one rather than as a gap; changing it moves the worked example and its golden tests and is a
decision to be taken deliberately. No loading for a non-monthly frequency was established.

### *Überschussbeteiligung* in the *Rentenbezug*

**The rule.** The annuity paid is `garantierte Rente + Überschussrente`. Only the first is a promise;
the second is declared annually out of surplus actually earned and **can move down as well as up**.
Participation is a **statutory right, not a marketing feature**: § 153 VVG entitles the policyholder
to a share of the *Überschuss* and of the *Bewertungsreserven* unless excluded by express agreement,
names the principle — a *verursachungsorientiertes Verfahren* — and **does not prescribe the
algorithm**, which is precisely why every level below is **[std]** [REG-R24]. It **does not stop at
*Rentenbeginn***, and three carriers now say so at clause level. Zurich Deutscher Herold, in both the
immediate and the deferred pack: "An vorhandenen Bewertungsreserven werden Sie während der
Rentenzahlungszeit … beteiligt. Derzeit sieht § 153 Absatz 3 VVG eine hälftige Beteiligung an den
Bewertungsreserven vor" [S2] [S3] [REG-R24]. NÜRNBERGER credits the annual *Bewertungsreserven*
share "zur Erhöhung der bis dahin erreichten Rente, erstmals zum Ende des ersten Versicherungsjahres"
[S4]. And Bayern-Versicherung's declaration allots them "zur Hälfte dem Vertrag", measuring the
amount in payment "jeweils für den Monat vor dem Jahrestag der Versicherung" [S10]. One rule cuts the
other way and is specific to this product: at that carrier, "Rentenversicherungen mit sofort
beginnender Rentenzahlung erhalten keine Mindestbeteiligung" at the *Bewertungsreserven*, and no
*Schlussüberschussbeteiligung* either [S10].

**The *Überschussverwendung* forms**, elected at *Rentenbeginn* — here at inception, once, and
**irrevocably**: "Ein Wechsel der Überschussverwendungsarten ist ausgeschlossen" [S4]. The consumer
literature names **three** — konstant (also *flexibel*), teildynamisch, volldynamisch [R19] [R21] —
and carriers name their own variants on top: *Bonusrente*, *Bonus-PLUS-Rente* and *Garantie-PLUS-Rente*
at Zurich [S2], a *dynamische Überschussrente* and a *teildynamische Bonusrente* at NÜRNBERGER [S4],
"Bonusrente oder Überschussrente" at Bayern-Versicherung [S10]:

| Form | Mechanic | Payment stream |
|---|---|---|
| ***konstante Überschussrente*** | The insurer fixes the total annuity at *Rentenbeginn* from the *garantierte Rente* plus a surplus share **projected for the whole annuity period**, and intends to hold it level [R21] | Highest at outset; flat thereafter **in intention only** |
| ***steigende (volldynamische)*** | The annuity **adjusts annually and flexibly to the actual surplus development** [R21] | Lowest at outset; rises each year surplus is declared |
| ***teildynamische*** | Part of the expected surplus is applied under the constant system and part under the dynamic one, so the annuity rises by a **fixed percentage** provided the insurer earns corresponding surpluses [R21] [R23] | Intermediate at outset; rises at a stated rate, subject to surplus |
| ***Bonusrente*** (the crediting mechanic, not a fourth form) | Declared surplus **buys a paid-up increment of annuity**, permanently added to the payment: "Die jeweils erreichte Rentenhöhe kann nicht mehr sinken" [S4] | Ratchets: each increment, once bought, does not come off |

**The *Bonusrente* is the mechanism underneath the rising forms, not a fourth alternative** [S2] [S4]
[S10]: what makes a *volldynamische Rente* **ratchet rather than fluctuate** is that its increments
are bought as paid-up annuity — "Die jeweils erreichte Rentenhöhe kann nicht mehr sinken" [S4] — so a
model treats it as the crediting mechanism and the three dynamics as the profile. **The single most
important thing to understand about this product: the constant form is not constant**, and this is
now read rather than reported. Finanztip: "In der Praxis kann Deine Rente aber durchaus schwanken.
Denn wenn der Anbieter weniger verdient als erwartet, sinkt Deine Rente. Die Summe, die anfänglich
festgelegt wird, ist nicht garantiert. Daher ist der Begriff „konstante Rente" etwas irreführend."
[R21] CosmosDirekt, in the contract: "Falls wir in einem Jahr nicht ausreichend Überschüsse
erwirtschaften, kann die Zusatzrente reduziert werden" [S6]. Zurich, on its *Garantie-PLUS-Rente*:
"Verringert oder erhöht sich aber die der Berechnung zugrunde liegende Überschussbeteiligung …, so
ändert sich demgemäß auch die Höhe der Rente aus Überschuss" [S2]. And the reason it can be reduced is
structural: during the payout phase the funds reserved in the RfB support "eine lebenslang zahlbare
Rente, deren Höhe jedoch nicht garantiert ist. Die hieraus gezahlten Renten sind jeweils nur für ein
Versicherungsjahr zugesagt" [S2]. **One source disagrees and is not followed**: the GDV's consumer
article asserts that under the flexible and teildynamic forms the annuity "nie unter das zu
Rentenbeginn erreichte Niveau fallen kann" [R19], which the AVB above contradict; the contract
controls. Only
the *garantierte Rente* inside it is guaranteed, and the gap between the two — on typical market
designs of the order of 15 % to 25 % of the payment [unverified] — is the amount at risk. **That
range stays [unverified]**: none of the five retrieved insurer packs, and neither consumer source,
quantifies the gap between the guaranteed and the total annuity, which is why `surplus_init_pct` is a
**[std]** with no observed range. The trade-off across the forms is one of timing, not of amount: the constant form front-loads the
same expected surplus and carries reduction risk, the volldynamic form back-loads it and carries the
risk of dying before collecting. Franke und Bornberg titled its treatment "Die Qual der Wahl" [R20].

**One carrier's payout-phase declaration is now read, and it changes what this section can say.**
Bayern-Versicherung's *Überschussverteilung 2026* [S10] sets, for *Einzel-Rentenversicherungen* of
tariff generations 2015–2025, a *Zinsüberschussanteil* **während des Rentenbezugs** of **"3,35 %
(2,5 %) abzüglich Rechnungszins"** — 3,35 % for 2026 against 2,5 % for 2025, so **2,35 % over a
1,00 % tariff rate** — against "3 % (2,25 %) abzüglich Rechnungszins" before *Rentenbeginn*. The
component split is stated outright: in payment the surplus is a "Zinsüberschussanteil in Prozent des
Deckungskapitals" and "**Ein Risiko- oder Verwaltungskostenüberschussanteil wird nicht gewährt**".
Debeka reports the resulting increase actually granted on its own *Sofortrente*: "Im Jahr 2024
beträgt die Steigerung der Rente 0,75 Prozent" [S8]. Five carriers' *laufende Verzinsung* for 2026,
from Assekurata via Finanztip, are Allianz 2,7 %, Alte Leipziger 2,4 %, AXA 3,0 %, Proxalto 2,7 % and
Nürnberger 2,95 % [R21] [R22]. **None of this is used to set the model's surplus scale**, which stays
**[std]** and uncalibrated (see `technical-notes.md` class (b)); what is gone is the claim that no
rate, no component split and no realised *Rentenanpassung* exists anywhere in the corpus (gap 4
narrows to: no *spread*, and no rate for the carriers this specification is otherwise built on).
The cross-product library's accumulation-side average must be read carefully: the German declared
rate is the ***laufende Verzinsung***, the *Garantieverzinsung* **plus** the *laufende
Zinsüberschussbeteiligung*, **not a surplus rate on top of the guarantee** — 2,53 % Klassik / 2,58 %
Neue Klassik for 2025, with three incompatible figures for 2026 [REG-R53]. Adding a declared rate to
a guaranteed rate is the commonest arithmetic error in describing a German contract.

### Where the surplus comes from

**Three sources, unequally important for an annuity in payment.** The ***Zinsüberschuss*** — actual
investment return over the *Rechnungszins* on the *Deckungsrückstellung* — dominates, the reserve
being large from day one and running off slowly over decades. The ***Risikoüberschuss*** is, for an
annuity, a **longevity** result: positive when annuitants die **faster** than the first-order table
assumed, negative when they live longer, and the one source that can go the wrong way for a whole
cohort at once. The ***Kostenüberschuss*** is small. The statutory floor beneath the insurer's
discretion is the MindZV's 90 / 90 / 50 and the RfB machinery above it, under *Regulatory context*.

**The competition for the same money is first-order here.** The *Überschussrente* is paid from the
same *Rückstellung für Beitragsrückerstattung* that financed the ***Zinszusatzreserve*** (ZZR), the
additional HGB reserve arising when the § 5 Abs. 3 DeckRV *Referenzzins* falls below a contract's
tariff rate [REG-R17]; the build-up suppressed declarations across the market for a decade and the
release should work the other way. On trade-press figures — **never a supervisory source** — the ZZR
stood at about **84 Mrd €** at the 2024 balance-sheet date against a **96 Mrd €** peak at end-2021,
**2024 was the first year since introduction in which insurers had to add nothing at all**, and about
5 Mrd € flowed back with a further 4 Mrd € for 2025, reaching policyholders **through a higher
*Überschussbeteiligung*** [REG-R17]. That release profile is the largest single driver of what a
German annuitant cohort will actually receive over the next decade, and a model projecting a flat
surplus rate is ignoring it.

### The *Aufschubzeit* variant

**The rule.** The *Einmalbeitrag* is paid now and the annuity begins **after a short deferment**,
typically one to fifteen years. **No carrier's terms were established, and the corpus's one candidate
is not one**: the Mecklenburgische "Rente flex" reads in full as a *Private Rentenversicherung mit
flexiblem Fondsanteil (Hybrid)*, a unit-linked deferred annuity that belongs to a different delib
product [S14]. **What it does — three
things at once, which must not be conflated:** interest accrues at the
*Rechnungszins*, so more capital is annuitised; **mortality accrues**, so survivors share the fund of
those who died — the survivorship credit that makes deferral powerful, and the reason the deferment
death benefit is a first-order design question; and the annuity starts at an older age, so `a12` is
smaller for two reasons at once. Two death-benefit forms exist — a **pure deferred annuity** with no
death benefit, and a *Beitragsrückgewähr* form refunding the *Einmalbeitrag* on death before
*Rentenbeginn*, much the more common retail form — and **neither was established for this product**.
On the [std] basis at 1,00 %, age 65, 100 000 €, a five-year deferment raises the monthly annuity
from 407,98 € to **532,48 €** without a deferment death benefit and **508,12 €** with full
*Beitragsrückgewähr* — about +31 % and +25 %, the 4,6 % gap between them being **the price of the
death benefit**, widening to 11,1 % at ten years **[std]** (15: same basis, gross of charges).

### No surrender, no lapse, no *Beitragsfreistellung*

**The rule** and its consequences are set out under *Termination and values*; the **positive**
statement a projection model needs is that the *Sofortrente* is the one German retail life product
whose only decrement is death. Everything else a liability model would ordinarily carry — a
*Rückkaufswert* table, a *Stornoabzug*, a five-year cost-spreading floor [REG-R28], a
*Beitragsfreistellung* conversion, a lapse rate, a dynamic surrender formula, a duration-12 tax
threshold driving surrender behaviour [REG-R45] — is **absent by specification**, and the consumer
warning that follows is the first thing every German consumer page says: the *Einmalbeitrag* is
**irreversibly committed** [R21] [R23].

---

## Riders and options

**In scope, carried as model-point parameters** and specified above: the *Rentengarantiezeit* as an
annuity-certain floor; the *Kapital-/Beitragsrückgewähr*, solved implicitly and **[std]** mutually
exclusive with the guarantee period and the survivor's annuity; the *Hinterbliebenenrente*, **off in
the base run** because the market treats it as a rider with its own condition set [S9]; the
*Aufschubzeit*, its deferment death benefit taking the same refund form, **off in the base run**; the
*Überschussverwendung* form, as an opening surplus percentage and an annual growth rate, both
**[std]**; and payment frequency and timing, so that footnote 8's unestablished convention can be
switched and its 5 % effect measured rather than assumed away.

**Out of scope, said rather than left to be discovered.** ***Bewertungsreserven* participation**
continues throughout the payout phase and is a statutory entitlement [S3] [REG-R24], but it is path-
and balance-sheet-dependent in a way a gross liability cash-flow model cannot reproduce, being
recomputed annually on the HGB accounts and reduced by the *Sicherungsbedarf* test of § 139 VAG and
MindZV §§ 11–13, whose fifteen-year window "bites hardest on annuity business" [REG-R9] [REG-R18];
the reference implementation models the declared *Überschussrente* explicitly and treats the
*Bewertungsreserven* share as an **explicitly excluded component**. Also out: a commuted settlement
of the *Restgarantiezeit* (gap 10); a *Kapitalwahlrecht* or partial commutation after *Rentenbeginn*,
of which there is none [R1]; indexed or inflation-linked annuities and impaired-life (*enhanced*)
annuities, neither established to exist in the German retail market; proof of life, whose failure
suspends payment until the certificate arrives; and the *fondsgebundene Sofortrente*, which belongs
to `fondsgebundene_rentenversicherung`.

---

## Variations across insurers

**This specification still supports no numeric variation table, but the reason has narrowed.**
Retrieval reached five carriers' condition sets and two carriers' product pages, so the **mechanics**
below are sourced per carrier; what no document supplies is a **comparison** — no two carriers'
quotations on the same case, no spread, no charge at any of them — and a table with a rate column per
carrier would still be fabrication. Exactly one carrier's rate scale exists in the corpus, Debeka's
tariff **S1** at Stand 01.01.2025 [S8], and one carrier's minimum ticket and maximum entry age,
Allianz's 3 000 € and 85 years [S7]. The research file names **twenty-eight** German life insurers as
writers of the right kind of business — Allianz, R+V, Debeka, Generali and CosmosDirekt, NÜRNBERGER,
Swiss Life, Zurich Deutscher Herold, ERGO, AXA, HDI, Alte Leipziger, LV 1871, Volkswohl Bund, Konzern
Versicherungskammer and thirteen others [S13] — and for twenty-three of them naming the carrier still
asserts only that it is a German life insurer of the right kind. **The GDV does maintain
*Musterbedingungen* for this product**, and the earlier statement that it does not is withdrawn: its
service index lists *Allgemeine Bedingungen für die Rentenversicherung mit sofort beginnender
Rentenzahlung* (Stand 21.07.2025), a second set for the AltZertG version, and a
*Hinterbliebenenrenten-Zusatzversicherung* rider set for the immediate annuity alongside the deferred
one [S1] [S9] [REG-R37]. The market therefore has an association template of its own to draft from,
and does not need to adapt the deferred one — which closes research gap 3 the other way round.

| Carrier | Document | What it establishes for this product |
|---|---|---|
| Zurich Deutscher Herold | [S2] immediate annuity, Fassung 01/2025 (a Schicht-2 *Direktversicherung* pack); [S3] deferred, Fassung 01/2026 | the *Rechnungsgrundlagen* — "Sterbetafel DAV 2004R (Aggregattafel)", *Rechnungszins* 1,00 % — at both ends of the same carrier's range; the no-termination clause; that the *Überschussrente* is "jeweils nur für ein Versicherungsjahr zugesagt"; *Bewertungsreserven* participation **continuing in the payout phase**, *hälftig*; and from [S3] the conversion of accumulated surplus on the bases in force for the annuity at *Rentenbeginn* |
| NÜRNBERGER | [S4] AVB `gn331303_p`, tariff **NR3303**, edition GN331303_202501 | payment **in arrears** from one month after inception; the company table *NÜRNBERGER Tafel 2013 R* at 1 % p. a.; the *Rentengarantiezeit* with a commutation option; the ratchet and the irrevocable election; the α-once/β-running charge structure; and "Eine sofort beginnende Rentenversicherung können Sie nicht kündigen" |
| NÜRNBERGER | [S5] AVB tariff NIR3301 | the *Rentengarantiezeit* as a **tariff-level feature carried in the product name**, and — decisively — that the deferred contract converts on the bases of the carrier's own *Sofortrente* tariff, **naming NR3303** as the comparable one |
| CosmosDirekt (Generali) | [S6] AVB LA 904 A (01.17) | the *Kapitalrückgewähr* measured on the **guaranteed** annuity; the *Restgarantiezeit* commutation alternative; the standard surplus disclaimer; that the constant form's *Zusatzrente* **can be reduced**; a tariff *Garantiesatz* of 0,90 %, equal to its vintage's cap; and payment **in arrears** for the immediate form |
| Allianz | [S7] KomfortDynamik page; *PrivatSofortRente* page | the product name; *Mindesteinmalbeitrag* **3 000 €**; *Höchsteintrittsalter* **85**; the four payment frequencies. **Neither page carries the two propositions previously attributed to this carrier** |
| Debeka | [S8] B LV 85; *Privatrente* and *Sofortrente* pages | **the corpus's only carrier rate scale** — tariff **S1**, 50 000 €, 20-year guarantee, Stand 01.01.2025, 151 € a month at 65 — plus a realised *Rentenanpassung* of 0,75 % for 2024 and the *Ertragsanteil* at 18 % from the insurer's own page |
| GDV | [S1] [S9] | **model conditions for exactly this product** (Stand 21.07.2025) and a matching survivor's-annuity rider set; the no-termination clause at template level; and the rider's sequencing behind a running *Rentengarantiezeit* |
| Konzern Versicherungskammer | [S10] *Überschussverteilung 2026* | a payout-phase *Zinsüberschussanteil* of **3,35 % less the *Rechnungszins*** for 2026, funded from interest surplus alone; and two rules specific to the *Sofortrente* — no *Schlussüberschussbeteiligung*, no *Mindestbeteiligung* at the *Bewertungsreserven* |

| Feature | Variants that exist | Evidence |
|---|---|---|
| *Rentengarantiezeit* | 5 / 10 / 15 / 20 / 25 / 30+ years, or none; typical 15 years to age 70 and 10 thereafter; most choose 10–20 | envelope [R23]; tariff-level [S4] [S5]; optional in the template [S1]; priced as an option [S7] |
| Settlement inside the guarantee period | instalments continue by default, **or** the claimant may elect a lump sum — of the outstanding instalments [S4] or of the *Deckungskapital* [S6] | [S4] [S6]; **take-up not established** |
| Death benefit menu | *Rentengarantiezeit*, *Kapital-/Beitragsrückgewähr* (Tarif R3T at one carrier), *Hinterbliebenenrente*, *Sterbegeld* capped at 8 000 € in the bAV form, or none | [S2] [S6] [S7]; **no carrier's full menu established** |
| Survivor's annuity | a *Zusatzversicherung* with its own condition set, paid only **after** any *Rentengarantiezeit* expires; 60 % and 100 % are the standard levels [unverified], the model conditions stating none | [S1] [S9] |
| *Überschussverwendung* in payout | konstant (*flexibel*) / teildynamisch / volldynamisch, under carriers' own names; the election is irrevocable | [R19] [R21]; [S2] [S4] [S6] [S10] |
| *Bewertungsreserven* in payout | continue, currently at equal participation; **no *Mindestbeteiligung* and no *Schlussüberschuss* for this product** at one carrier | [S2] [S3] [S4] [S10]; [REG-R24] |
| Interest basis of the guarantee | at or below the *Höchstrechnungszins* [REG-R14]; **every retrieved tariff prices at its vintage's cap** — 1,00 % in 2025/2026, 0,90 % in 01/2017 | [S2] [S3] [S4] [S6] [REG-R15] |
| Payment timing | **in arrears at both carriers whose AVB state it**; the template does not settle it | [S4] [S6]; [S1] |
| *Aufschubzeit* | 0 years (pure *Sofortrente*) or a short deferment | **no carrier's terms located**; [S14] is a hybrid deferred annuity and is not a candidate |

**Parameters whose range is unknown.** The **spread** between the best and worst quotation — one
carrier's scale is now in the corpus [S8], no second; α and β, and with them *Effektivkosten* and
*Renditeminderung*, none of which any retrieved document quantifies; the *Einmalbeitrag* and
entry-age envelopes beyond one carrier's 3 000 € and 85 years [S7]; surplus rates at the carriers
this specification is otherwise built on, one group's declaration having been read [S10] and one
carrier's realised increase [S8]; the split of new business between the *Überschussverwendung* forms;
the take-up of *Kapitalrückgewähr* against *Rentengarantiezeit*, and of the lump-sum commutation
inside the guarantee period; the *Hinterbliebenenrente* percentage menu; and the market's size and
average ticket. **Every one is a gap, not an omission.** A reader who needs to know how German
carriers differ should start with a *Produktinformationsblatt* [S11], Stiftung Warentest's periodic
*Sofortrente* comparison [R21] and the dedicated comparison portals [R23] — in that order, and none
of the three was located on 2026-08-30.

---

## Regulatory context

**Contract law — the VVG.** The contract is an ordinary *Lebensversicherung* under Kapitel 5, whose
provisions are largely *halbzwingend* [REG-R22]. **§ 153** gives the statutory
*Überschussbeteiligung*, names the principle — a *verursachungsorientiertes Verfahren* — without
prescribing the algorithm, and requires the *Bewertungsreserven* to be recomputed annually and
shared, currently *hälftig*, subject to the LVRG's *Sicherungsbedarf* override [REG-R24] [REG-R20]
[S3]. **§ 154** requires a *Modellrechnung* wherever the insurer quantifies benefits beyond the
guaranteed ones — which a *Produktinformationsblatt* quoting a *Gesamtrente* does — at **three rates
fixed by § 2 Abs. 3 VVG-InfoV as the *Höchstrechnungszins* × 1,67, that rate ± one point**, so at
1,00 % the statutory triple is **1,67 % / 2,67 % / 0,67 %** [REG-R25] [REG-R15]. **§ 155** requires
an annual *Standmitteilung* disclosing the current claims including profit participation and **how
much of it is guaranteed**, which makes a published specimen a legitimate primary source class and
its absence here a real gap [REG-R25] [S15]. **§§ 165–170** — *Beitragsfreistellung*, termination,
*Rückkaufswert*, *Stornoabzug* — **do not operate once the *Rentenbezug* has begun** [REG-R28] [R1]
[R2] [R5]; §§ 150 and 159–162 carry consent and the *Bezugsberechtigung* [REG-R26]; and the
*Widerrufsrecht* is 30 days for life insurance [REG-R23].

**Tariff bases — the DeckRV and the DAV.** § 2 DeckRV fixes the *Höchstrechnungszins* and, through
§ 138 Abs. 1 VAG's requirement that premiums fund the reserve, caps the rate at which a new tariff
may be priced [REG-R14] [REG-R8]. **The rate applies at conclusion and stays with the contract for
its whole term** — which is why the German book is a stack of cohorts and every delib model point
carries its cohort's rate: 3,50 % to mid-1994; 4,00 % to mid-2000; 3,25 %; 2,75 %; 2,25 %; 1,75 %;
1,25 %; 0,90 %; 0,25 % for 2022–2024; **1,00 % from 2025**, by the *Sechste Verordnung zur Änderung
von Verordnungen nach dem VAG* of 19 July 2024, BGBl. 2024 I Nr. 250 [REG-R15]. The ministry sets it
on an annual DAV recommendation — **practice, not law** — carrying a ***Sicherheitsabschlag* of
40 %** [REG-R56]. **§ 4 DeckRV's *Höchstzillmersatz* of 25 ‰ does not reach this product**, there
being no *Beitragssumme* [REG-R16]. No statute names a table: the gap between "prudent" and a
specific `q_x` is closed by the *Verantwortlicher Aktuar* under § 141 VAG [REG-R56] [REG-R11], so
**a German biometric basis is soft law with hard consequences** and DAV 2004 R is a benchmark, not a
mandate [REG-R47] [REG-R49]. The unisex rule of C-236/09 and §§ 19, 20 and 33 AGG [REG-R34] binds
the tariff from 21 December 2012 and is set out under *Underwriting and rating*.

**Surplus, the RfB and the supervisor.** The arithmetic floor under the insurer's discretion is the
MindZV: **90 % of the *Kapitalanlageergebnis* less the *Rechnungszinsen*** — the guarantee funded
first, only the excess shared — **90 % of the *Risikoergebnis***, raised from 75 % by the LVRG from
7 August 2014, and **50 % of the *übrige Ergebnis*** [REG-R18] [REG-R20]; the *Direktgutschrift* is
**deducted** and a negative minimum replaced by zero, making it a minimum **transfer to the RfB, not
a minimum payout**. Above it sit § 140 VAG's ring fence [REG-R10], the RfBV's ceiling on the
*ungebundene* part and its *kollektiver Teil* [REG-R19], the § 139 VAG *Sicherungsbedarf* test
[REG-R9], and the § 138 Abs. 2 VAG equal-treatment rule the BGH tied to § 153 VVG in IV ZR 436/22 of
18 September 2024 [REG-R8] [REG-R36] — all computed on the **HGB** accounts [REG-R54], with assets in
the *Sicherungsvermögen* under § 124 VAG's prudent-person principle rather than the AnlV quotas
German market writing routinely misapplies [REG-R7].

**Disclosure and distribution.** The VVG-InfoV prescribes the pre-contractual pack — the
*Verbraucherinformation* / *Vertragsinformationen* / *Allgemeine Informationen* class [S2] [S3]
[S14] — and carries the *Effektivkosten* disclosure [REG-R31]. PRIIPs generates the
*Basisinformationsblatt* with its *Risikoindikator*, four performance scenarios and
*Renditeminderung* [REG-R32] [S12], but **whether a payout-only *Sofortrente* falls inside PRIIPs
scope was not established** (gap 8): it reads as an insurance-based investment product, while its
payout-only character and the absence of a surrender value make the holding-period and "what you
might get back" sections awkward. If one exists it is the **only** public document giving this
product's cost in standardised form, and none was located. Distribution runs under the IDD as
transposed on 20 July 2017 and § 34d GewO [REG-R33].

**Taxation.** The whole cash flow is taxed under **§ 22 EStG** on the *Ertragsanteil* and **none of
it under § 20** [R13] [R14] [REG-R41] [REG-R45]: only the "Ertrag des Rentenrechts" is income, and
the fraction is fixed once by the age at *Rentenbeginn*, "für die gesamte Dauer des Rentenbezugs"
— **18 % at 65** and 22 % at 60, both now checked against the statutory table itself, which runs from
59 % at ages 0–1 to 1 % from age 97 [R13] [REG-R41]. The schedule no longer carries [unverified].
Debeka states the same cell on its own product page: "Das sind zum Beispiel 18 % bei Rentenbeginn mit
Vollendung des 65. Lebensjahrs" [S8]. On the
constructed 389,99 € monthly annuity of footnote 10 the taxable amount is 70,20 €, so the tax is
**17,55 €, 4,5 % of the annuity**, at a 25 % marginal rate and 29,48 €, **7,6 %**, at 42 % **[std]**.
The § 20 Abs. 1 Nr. 6 *Halbeinkünfteverfahren* reaches only *Rentenversicherungen mit
Kapitalwahlrecht* where the lifelong annuity is not taken, capital endowments with a savings element,
and surrenders — none of which a *Sofortrente* can be [R14] [REG-R45] — and requires twelve contract
years plus payment after a birthday which § 20 Abs. 1 Nr. 6 Satz 2 sets at the **60th** and § 52 EStG
raises to the **62nd** for contracts concluded after 31 December 2011; the familiar "12/62" is the
pair, not § 20 alone. **The boundary is the product's main quantitative selling point** against a
*Bankauszahlplan* taxed in full at the *Abgeltungsteuer* rate. A death benefit to a named beneficiary is an ordinary *Erwerb von Todes
wegen* under § 3 Abs. 1 Nr. 4 ErbStG, and a Schicht-3 annuity is **not** a *Versorgungsbezug* under
§ 229 SGB V — though **§ 240 SGB V reverses that for *freiwillig versicherte* members** [REG-R46].
**One of the four open tax questions is now answered.** *Rentengarantiezeit* payments to a
beneficiary **do** keep the *Ertragsanteil* treatment: "Werden Leibrenten nach dem Tod der
versicherten Person während einer Rentengarantiezeit weitergezahlt, unterliegen diese Renten
weiterhin mit dem Ertragsanteil der Einkommensteuer" [S2]. **Still not established:** whether a
*Kapitalrückgewähr* refund is taxable, whether a *Hinterbliebenenrente* is re-based on the survivor's
commencement age — § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb Satz 5 refers annuities on another
person's life to § 55 EStDV, which was not read — and the *Solidaritätszuschlag* (gap 15).

**Prudential and accounting — cited, never specified.** BaFin supervises under Solvabilität II as
transposed into the VAG [REG-R1] [REG-R2] [REG-R5] [REG-R6], with Directive (EU) 2025/2 amending the
regime [REG-R3] and EIOPA publishing the curves [REG-R4]. A German insurer values this book
**twice**: the HGB *Deckungsrückstellung* on the first-order bases, increased by the ZZR [REG-R14]
[REG-R17] [REG-R54], on which the whole surplus system operates; and the Solvency II best estimate at
the EIOPA curve plus a risk margin [REG-R6]. IFRS 17 is a third, group-reporting measure [REG-R55].
**`delib` computes none of them:** the models publish gross best-estimate-style liability cash flows
per model point, income-positive and **undiscounted**, and the discounting, the margins, the
*Deckungsrückstellung* recursion, the ZZR, the RfB stock and the CSM belong to a layer above.

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
[REG-R22]: #delib-reg-r22
[REG-R23]: #delib-reg-r23
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
[REG-R37]: #delib-reg-r37
[REG-R38]: #delib-reg-r38
[REG-R4]: #delib-reg-r4
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R46]: #delib-reg-r46
[REG-R47]: #delib-reg-r47
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R52]: #delib-reg-r52
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
